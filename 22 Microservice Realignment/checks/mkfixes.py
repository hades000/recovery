"""Turn deterministic findings into exact fix records (sandbox prototype, D-RCV-60).

A finding becomes a fix only when a source already decides the new text:
  - X20 versions            -> Document Index v14 (or the version this fix set itself produces)
  - X6 event type           -> Kafka Topic and Event Catalog v1
  - X8 wording drift (P3)   -> Error and Message Standard v4 (same placeholders only)
  - X1 status row           -> Case and Workflow Model v6 and Reference Data v5 (row removed)
  - X3 renamed column       -> LDM v9 field confirmed in CONFIRMED_RENAMES (meaning checked by a reviewer)
  - X12 ACE-view Givens and legacy job wording -> the story's own contract-mock and workflow terms
  - X9 missing test cases   -> Given/When/Then copied from the criterion that owns them
  - DECIDED                 -> decisions taken (Decision Log v11) quoted in the fix
Everything else is HELD with the owner role, or WORDING (new text needed: the model drafts it).

Usage: python -I mkfixes.py --root <ROOT> --det <det out dir> --out <dir> --legacy RWB-E1-018
Writes only under --out: fixes.jsonl, disposition.jsonl, disposition.md.
"""
import argparse, json, re, sys
from collections import OrderedDict, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import rwbsrc
from detcheck import Story, Sources

# A rename is applied only when a reviewer has checked the LDM v9 meaning against the story's use.
CONFIRMED_RENAMES = {
    "primary_customer_id": ("primary_person_key",
                            "LDM v9 Fields DF-CAS-004 recovery_case.primary_person_key 'ACE person_key of the borrower the "
                            "case is opened for'; Relationships row recovery_case.primary_person_key -> v_ace_customer"),
}

# Decisions taken that settle a story rule. old -> new, with the decision quoted.
DECIDED = [
    {"finding": "BR12 against D-RCV-30", "decided_by": "Decision Log v11, Decisions taken, D-RCV-30",
     "old": "The primary account is the linked account with the highest `total_balance` on the business date; a tie breaks on the lowest `account_key`",
     "new": "The primary account is the account the case was opened on; accounts grouped later onto the case are non-primary rows (D-RCV-30)"},
]

TC_HEADERS = ["Test case", "Story", "Epic", "Module", "Covers", "Test", "Level", "Given", "When", "Expected result",
              "Data", "In regression", "Status", "Later home", "Service", "Story key (new)", "Test level", "Origin"]


class Gen:
    def __init__(self, root, det, legacy):
        self.root = Path(root)
        self.det = det
        self.rows = [json.loads(l) for l in (Path(det) / "gaps.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
        self.stories = {}
        for r in self.rows:
            pass
        base = self.root / rwbsrc.TEXT["stories"]
        tag = legacy.replace("RWB-", "").replace("-", "")
        for p in sorted(base.rglob("*.md")):
            if f" {tag} " in p.name and rwbsrc.story_key_from_name(p.name):
                st = Story(p)
                self.stories[st.key] = st
        self.fixes, self.disp = [], []
        self.n = 0
        self.produced = {}  # document name -> version produced by this fix set
        self.x20_rows = []

    def rel(self, st):
        return str(st.path.relative_to(self.root)).replace("\\", "/")

    def fix(self, st_or_rel, finding, op, source, **kw):
        rel = st_or_rel if isinstance(st_or_rel, str) else self.rel(st_or_rel)
        key = (rel, op, kw.get("old"), kw.get("new"))
        for f in self.fixes:
            if (f["file"], f["op"], f.get("old"), f.get("new")) == key:
                if finding not in f["finding"]:
                    f["finding"] += ", " + finding
                return f["fix_id"]
        self.n += 1
        f = OrderedDict(fix_id=f"F-{self.n:03d}", finding=finding, file=rel, op=op, source=source)
        f.update(kw)
        self.fixes.append(f)
        return f["fix_id"]

    def dispose(self, row, status, detail, fix_ids=()):
        self.disp.append(OrderedDict(id=row["id"], story=row["story"], check=row["check"], severity=row["severity"],
                                     type=row["type"], title=row["title"], status=status, fixes=list(fix_ids),
                                     owner=row.get("owner_role", ""), detail=detail))

    # ---------------------------------------------------------------------------------------------
    def run(self):
        # 1. test-case rows first: they decide the Test Cases version that X20 then cites
        tc_rows = [r for r in self.rows if r["check"] == "X9" and r.get("fix", {}).get("kind") == "tc_rows"]
        tc_ids = sorted({i for r in tc_rows for i in r["fix"]["ids"]})
        self.tc_held = {}
        made = self.tc_fix(tc_ids)
        for r in tc_rows:
            got = [i for i in r["fix"]["ids"] if i in made]
            if got and len(got) == len(r["fix"]["ids"]):
                self.dispose(r, "FIXED", f"rows {', '.join(got)} added to the next Test Cases version", [made[g] for g in got])
            elif got:
                self.dispose(r, "PARTLY FIXED", f"rows {', '.join(got)} added; others need an owning criterion", [made[g] for g in got])
            elif any(i in self.tc_held for i in r["fix"]["ids"]):
                self.dispose(r, "HELD", "; ".join(self.tc_held[i] for i in r["fix"]["ids"] if i in self.tc_held))
            else:
                self.dispose(r, "WORDING", "no criterion in the document set owns these IDs yet; the model drafts the rows")
        for r in self.rows:
            if r in tc_rows:
                continue
            st = self.stories.get(r["story"])
            if st is None:
                self.dispose(r, "HELD", "story file not in the fix scope")
                continue
            if r["check"] == "X20":  # planned last, on the text the other fixes leave
                self.x20_rows.append((r, st))
                continue
            handler = getattr(self, "h_" + r["check"].lower(), None)
            if handler is None or not handler(r, st):
                self.dispose(r, "HELD", r["proposed"])
        self.decided()
        self.x20_all()

    # X20 -------------------------------------------------------------------------------------------
    def x20_all(self):
        """Version references, with the hold rules of x20_fixes (history lines, claims about a version, file names
        that do not exist). Planned on each file's text after every other fix of it, so an exact whole-line
        replace never meets a line another fix changed. A document this fix set produces (Test Cases v9) wins."""
        if not self.x20_rows:
            return
        import x20_fixes
        from apply_fixes import apply_text
        best = dict(rwbsrc.Sources(self.root, Path(self.det) / "_x20cache").doc_versions())
        best.update(self.produced)
        pats = x20_fixes.make_pats(best)
        on_disk = x20_fixes.files_on_disk(self.root)
        for name, v in self.produced.items():  # a version this run writes counts as existing
            on_disk.update({f"recovery workbench {name} v{v}{ext}".lower() for ext in (".xlsx", ".docx", ".md")})
        for r, st in self.x20_rows:
            rel = self.rel(st)
            work = st.text
            for f in self.fixes:
                if f["file"] == rel and f["op"] in ("replace", "delete_line", "insert_after"):
                    work = apply_text(work, f)
            fx, held, _ = x20_fixes.plan_file(work, rel, st.key, pats, on_disk, finding=r["id"],
                                              source="12 Project communication/Recovery Workbench Document Index v14.md")
            ids = [self.fix(st, r["id"], "replace", f["source"], old=f["old"], new=f["new"], count=f["count"]) for f in fx]
            why = "; ".join(sorted({f"line {h['line']}: {h['reason']}" for h in held}))
            if ids and not held:
                self.dispose(r, "FIXED", "version references raised", ids)
            elif ids:
                self.dispose(r, "PARTLY FIXED", f"version references raised; held: {why}", ids)
            else:
                self.dispose(r, "HELD", f"held: {why}" if why else r["proposed"])

    # X6 --------------------------------------------------------------------------------------------
    def h_x6(self, r, st):
        f = r.get("fix")
        if not f:
            return False
        ids = []
        for old, new in f.get("pairs", [[f.get("old"), f.get("new")]]):
            n = st.text.count(old)
            if n:
                ids.append(self.fix(st, r["id"], "replace", r["source"], old=old, new=new, count=n))
        if ids:
            self.dispose(r, "FIXED", "event type copied from the catalog", ids)
            return True
        return False

    # X8 --------------------------------------------------------------------------------------------
    def h_x8(self, r, st):
        f = r.get("fix")
        if not f or r["severity"] != "P3" or r["type"] != "Conflict":
            if f and r["type"] == "Conflict":
                self.dispose(r, "WORDING", "placeholders differ from the standard; the sentence that fills them must be "
                                           "reworded with the standard's placeholders (model drafts, reviewer checks)")
                return True
            return False
        old = f"| {f['old']} |"
        n = st.text.count(old)
        if n != 1:
            self.dispose(r, "HELD", f"message text found {n} times; not applied")
            return True
        i = self.fix(st, r["id"], "replace", r["source"], old=old, new=f"| {f['new']} |")
        self.dispose(r, "FIXED", "English text copied from the Error and Message Standard v4", [i])
        return True

    # X1 --------------------------------------------------------------------------------------------
    def h_x1(self, r, st):
        f = r.get("fix")
        if not f or f.get("kind") != "delete_table_row":
            return False
        lines = [l for l in st.lines if l.startswith(f["match"])]
        if len(lines) != 1:
            return False
        i = self.fix(st, r["id"], "delete_line", r["source"], old=lines[0])
        self.dispose(r, "FIXED", "row removed; the model has no such status or transition", [i])
        return True

    # X3 --------------------------------------------------------------------------------------------
    def h_x3(self, r, st):
        f = r.get("fix") or {}
        if f.get("kind") != "rename_token" or f.get("old") not in CONFIRMED_RENAMES:
            return False
        new, why = CONFIRMED_RENAMES[f["old"]]
        ids = []
        for s in self.stories.values():
            n = len(re.findall(r"\b" + re.escape(f["old"]) + r"\b", s.text))
            if n:
                ids.append(self.fix(s, r["id"], "replace", f"06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx ({why})",
                                    old=f["old"], new=new, count=n))
        self.dispose(r, "FIXED", f"{f['old']} -> {new} in every file of the legacy key ({why})", ids)
        return True

    def h_x2(self, r, st):
        return False

    # X12 -------------------------------------------------------------------------------------------
    def section_lines(self, st, nums):
        out = []
        for n in nums:
            s = st.sub.get(n) if "." in n else st.sec.get(n)
            if s:
                out += list(range(s[0], s[1]))
        return out

    def h_x12(self, r, st):
        if st.worktype == "ITG" and r["token"] == "v_ace_":
            self.dispose(r, "HELD", "the integration story seeds ACE rows through the P1 data set; the QA lead rules whether "
                                    "its Givens stay on the views or move to the P1 contract")
            return True
        ids = []
        idx = self.section_lines(st, ["7", "16"])
        if r["token"] == "JOB-":
            jobmap = {}
            for tbl in st.table_dicts("12.5") + st.table_dicts("12.6"):
                for row in tbl:
                    name = row.get("Name") or row.get("Schedule") or ""
                    for j in re.findall(r"JOB-\d+", " ".join(row.values())):
                        if re.fullmatch(r"[A-Z]\w+", name.strip("` ")):
                            jobmap.setdefault(j, name.strip("` "))
            terms = []
            for j, wf in jobmap.items():
                terms.append((re.compile(r"\b" + j + r"\b"), wf))
            if "run record" in st.text:
                terms.append((re.compile(r"\bthe job record\b"), "the run record"))
            if "decision record" in st.text:
                terms.append((re.compile(r"\b[Dd]ecision log\b"), lambda m: "Decision record" if m.group(0)[0] == "D" else "decision record"))
            for i in idx:
                l = st.lines[i]
                if l.startswith("| DP-"):
                    continue
                new = l
                for pat, rep in terms:
                    new = pat.sub(rep, new)
                if new != l:
                    ids.append(self.fix(st, r["id"], "replace",
                                        "Template and Rules v1 DP-03 and DP-10; the story's own §12.5 and §4 terms",
                                        old=l, new=new, count=st.text.count(l)))
            left = [st.lines[i] for i in idx if re.search(r"\bJOB-\d+|job record|decision log", st.lines[i], re.I)
                    and not st.lines[i].startswith("| DP-") and not any(f.get("old") == st.lines[i] for f in self.fixes)]
            self.dispose(r, "FIXED" if ids and not left else ("PARTLY FIXED" if ids else "HELD"),
                         "legacy words replaced by the story's workflow, run-record and decision-record terms"
                         + (f"; {len(left)} line(s) left: no term in the story" if left else ""), ids)
            return True
        # ACE views in criteria and test data -> the story's contract mock wording
        mock = "the rwb-source-data contract mock returns"
        if mock not in st.text:
            return False
        scen = st.scenarios()
        for ac, lines in scen.items():
            mocks = [l for l in lines if l.startswith("Given " + mock)]
            for l in lines:
                m = re.match(r"Given v_ace_account holds (.*)", l)
                if m:
                    ids_in = set(re.findall(r"\b[AP]-\d{4}\b|\d[\d,]*\.\d\d", l))
                    dup = [x for x in mocks if set(re.findall(r"\b[AP]-\d{4}\b|\d[\d,]*\.\d\d", x)) <= ids_in]
                    full = self.full_line(st, l)
                    ids.append(self.fix(st, r["id"], "replace", "Template and Rules v1 DP-05; ADR-010; the story's §12.8 contract fakes",
                                        old=full, new=full.replace("Given v_ace_account holds", "Given " + mock), count=1))
                    for d in dup:
                        ids.append(self.fix(st, r["id"], "delete_line", "the merged Given holds every value of this line",
                                            old=self.full_line(st, d)))
                elif " in account_ext" in l:
                    full = self.full_line(st, l)
                    ids.append(self.fix(st, r["id"], "replace", "Template and Rules v1 DP-05; ADR-010",
                                        old=full, new=full.replace(" in account_ext", " in the rwb-source-data contract mock"), count=1))
        for i in self.section_lines(st, ["16"]):
            l = st.lines[i]
            new = re.sub(r"`v_ace_account` ", "rwb-source-data contract mock: ", l)
            new = new.replace(" in `v_ace_account`", " in the rwb-source-data contract mock")
            new = new.replace(" true in account_ext", " true in the rwb-source-data contract mock")
            if new != l:
                ids.append(self.fix(st, r["id"], "replace", "Template and Rules v1 DP-05; ADR-010", old=l, new=new, count=1))
        left = [st.lines[i] for i in self.section_lines(st, ["7", "16"])
                if re.search(r"v_ace_|account_ext|party_ext", st.lines[i])
                and not any(f.get("old") == st.lines[i] for f in self.fixes)]
        self.dispose(r, "FIXED" if ids and not left else ("PARTLY FIXED" if ids else "HELD"),
                     "Givens and test data moved to the rwb-source-data contract mock the story already uses"
                     + (f"; {len(left)} line(s) left for the model: " + " / ".join(x.strip()[:70] for x in left) if left else ""), ids)
        return True

    @staticmethod
    def full_line(st, stripped):
        hits = [l for l in st.lines if l.strip() == stripped]
        return hits[0] if len(hits) == 1 else stripped

    # X9 test-case rows -----------------------------------------------------------------------------
    def tc_fix(self, ids):
        made = {}
        tcpath = "09 Testing and quality/Recovery Workbench Test Cases v8.xlsx"
        rows = []
        for tid in ids:
            users = [s for s in self.stories.values() for tbl in s.table_dicts("16") for r in tbl if r.get("TC ID") == tid]
            cover = None
            for s in self.stories.values():
                for tbl in s.table_dicts("16"):
                    for r in tbl:
                        if r.get("TC ID") == tid:
                            cover = cover or (s, r)
            if not cover:
                continue
            covers = {re.sub(r"\s+", "", ",".join(re.findall(r"AC\d+", r.get("Covers", ""))))
                      for s in users for tbl in s.table_dicts("16") for r in tbl if r.get("TC ID") == tid}
            if len(covers) > 1:
                self.tc_held[tid] = f"ID collision: {len(users)} stories list {tid} for different criteria ({'; '.join(sorted(covers))})"
                continue
            s0, row0 = cover
            acs = re.findall(r"AC\d+", row0.get("Covers", ""))
            owner = next(((s, ac) for s in [s0] + [x for x in self.stories.values() if x is not s0] for ac in acs if ac in s.scenarios()), None)
            if not owner:
                continue
            os_, ac = owner
            lines = [self.reword(os_, l) for l in os_.scenarios()[ac]]
            given = "; ".join(l[6:] for l in lines if l.startswith("Given "))
            when = "; ".join(l[5:] for l in lines if l.startswith("When "))
            then = "; ".join(l[5:] for l in lines if l.startswith("Then "))
            title = next((l for l in os_.section_text("7").splitlines() if re.match(r"\s*Scenario:\s*" + ac + r"\b", l)), "")
            title = re.sub(r"\s*Scenario:\s*" + ac + r"\s*", "", title).split(" (legacy")[0]
            row = {"Test case": tid, "Story": os_.legacy, "Epic": os_.legacy.split("-")[1], "Module": s0.code,
                   "Covers": ac, "Test": title, "Level": "System" if "End to end" in row0.get("Level", "") else row0.get("Level", ""),
                   "Given": given, "When": when, "Expected result": then, "Data": row0.get("Data", ""),
                   "In regression": "", "Status": "Draft", "Later home": "", "Service": s0.service,
                   "Story key (new)": "; ".join(sorted(s.key for s in users)), "Test level": row0.get("Level", ""),
                   "Origin": f"D-RCV-60 build-readiness fix; criterion {ac} of {os_.key}; 'In regression' Not specified in the source documents"}
            rows.append(row)
        if rows:
            fid = self.fix(tcpath, "X9", "xlsx_append", f"Given/When/Then copied from the owning criterion",
                           sheet="Story test cases", header_row_hint="Test case", key="Test case", rows=rows)
            for r in rows:
                made[r["Test case"]] = fid
            self.produced["Test Cases"] = 9
        return made

    def reword(self, st, l):
        """Apply the same legacy-word and ACE-view rewrites to a criterion line copied into a test case."""
        jm = {}
        for tbl in st.table_dicts("12.5") + st.table_dicts("12.6"):
            for row in tbl:
                name = (row.get("Name") or row.get("Schedule") or "").strip("` ")
                for j in re.findall(r"JOB-\d+", " ".join(row.values())):
                    if re.fullmatch(r"[A-Z]\w+", name):
                        jm.setdefault(j, name)
        for j, wf in jm.items():
            l = re.sub(r"\b" + j + r"\b", wf, l)
        if "run record" in st.text:
            l = l.replace("the job record", "the run record")
        return l

    # Decisions taken ---------------------------------------------------------------------------------
    def decided(self):
        for d in DECIDED:
            ids = []
            for s in self.stories.values():
                n = s.text.count(d["old"])
                if n:
                    ids.append(self.fix(s, d["finding"], "replace", d["decided_by"], old=d["old"], new=d["new"], count=n))
            self.disp.append(OrderedDict(id=d["finding"], story="(all files of the legacy key)", check="X2",
                                         severity="P1", type="Conflict", title=d["finding"],
                                         status="FIXED" if ids else "HELD", fixes=ids, owner="Business analyst",
                                         detail=f"decided by {d['decided_by']}; AC3 and AC12 still assert is_primary by balance order and are left to the model's AC review"))

    def save(self, out):
        out = Path(out)
        out.mkdir(parents=True, exist_ok=True)
        with (out / "fixes.jsonl").open("w", encoding="utf-8") as f:
            for x in self.fixes:
                f.write(json.dumps(x, ensure_ascii=False) + "\n")
        with (out / "disposition.jsonl").open("w", encoding="utf-8") as f:
            for x in self.disp:
                f.write(json.dumps(x, ensure_ascii=False) + "\n")
        c = defaultdict(int)
        for x in self.disp:
            c[x["status"]] += 1
        lines = ["# Finding disposition", "", ", ".join(f"{k}: {v}" for k, v in sorted(c.items())) +
                 f". Fix records: {len(self.fixes)}.", "",
                 "| Finding | Story | Check | Sev | Status | Fixes | Owner | Detail |", "|---|---|---|---|---|---|---|---|"]
        order = {"P1": 0, "P2": 1, "P3": 2}
        for x in sorted(self.disp, key=lambda x: (x["status"] != "HELD", order.get(x["severity"], 3), x["story"])):
            lines.append(f"| {x['id']} {x['title'][:70]} | {x['story']} | {x['check']} | {x['severity']} | {x['status']} | "
                         f"{', '.join(x['fixes'])} | {x['owner']} | {x['detail'][:160].replace('|', '/')} |")
        (out / "disposition.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"{len(self.fixes)} fix records; " + ", ".join(f"{k} {v}" for k, v in sorted(c.items())))


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--det", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--legacy", required=True)
    a = ap.parse_args(argv)
    g = Gen(a.root, a.det, a.legacy)
    g.run()
    g.save(a.out)


if __name__ == "__main__":
    main()
