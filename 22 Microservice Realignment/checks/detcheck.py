"""Deterministic build-readiness checks for realigned story files (sandbox prototype, D-RCV-60).

Covers the mechanical part of WP B-P3-01-v3: X1, X3, X4, X5, X6 (events, workflow and activity
names, workflow ID form), X7 (rule IDs exist), X8, X9, X10 (event payload classes), X11, X12,
X16 (FR IDs), X17 (screen states), X19 (cited register IDs), X20, plus open DL items (part of X2).
Judgment checks (X2 conflicts of meaning, X13-X15, X18, DoR, AC review) stay with the model.

Usage:
  python -I detcheck.py --root <ROOT> --cache <dir> --out <dir> --wp <id>
         (--legacy RWB-E1-018 | --all | --story <path> ...) [--start 101 --step 40]
Writes only under --out: gaps.jsonl, assumptions.jsonl, cited.jsonl, report.json, summary.md.
"""
import argparse, difflib, json, re, sys, time
from collections import OrderedDict, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import rwbsrc

def _tcv():
    import re as _re
    m = _re.search(r"(Test Cases v\d+)", rwbsrc.SOURCES['tc'])
    return m.group(1) if m else 'Test Cases'

from rwbsrc import md_tables, split_row

JAVA_RESERVED = set("""abstract assert boolean break byte case catch char class const continue default do double
else enum extends final finally float for goto if implements import instanceof int interface long native new
package private protected public return short static strictfp super switch synchronized this throw throws
transient try void volatile while true false null""".split())

# Words that look like snake_case columns but are object names, not dictionary fields.
NOT_FIELDS_PREFIX = ("ux_", "ix_", "fk_", "pk_", "uq_", "v_ace_", "case_no_seq")
SNAKE = re.compile(r"`([a-z][a-z0-9]*(?:_[a-z0-9]+)+)`")


# ------------------------------------------------------------------------------- story
class Story:
    def __init__(self, path):
        self.path = Path(path)
        self.text = self.path.read_text(encoding="utf-8", errors="replace")
        self.lines = self.text.splitlines()
        m = re.match(r"#\s+(RWB-[A-Z0-9]+-[A-Z0-9]+-[A-Z]+(?:-\d+)?)\s*(.*)", self.lines[0] if self.lines else "")
        self.key = m.group(1) if m else rwbsrc.story_key_from_name(self.path.name) or self.path.stem
        self.title = m.group(2) if m else ""
        self.meta = {}
        for heading, hdr, rows in md_tables(self.text):
            if hdr[:2] == ["Item", "Value"]:
                self.meta = {r[0]: (r[1] if len(r) > 1 else "") for r in rows}
                break
        self.legacy = self.meta.get("Legacy key", "")
        self.service = self.meta.get("Service", "")
        epic = self.meta.get("Service epic", "")
        mm = re.search(r"RWB-SVC-(\w+)", epic)
        self.code = mm.group(1) if mm else (self.key.split("-")[1] if self.key.count("-") >= 3 else "")
        self.worktype = self.key.split("-")[-1] if not re.search(r"-\d+$", self.key) else self.key.split("-")[-2]
        # sections: number -> (start line index, end)
        self.sec = OrderedDict()
        idx = [(i, re.match(r"###\s+(\d+)\.\s*(.*)", l)) for i, l in enumerate(self.lines)]
        idx = [(i, m) for i, m in idx if m]
        for j, (i, m) in enumerate(idx):
            end = idx[j + 1][0] if j + 1 < len(idx) else len(self.lines)
            self.sec[m.group(1)] = (i, end, m.group(2).strip())
        self.sub = OrderedDict()
        sidx = [(i, re.match(r"####\s+(\d+\.\d+)\s*(.*)", l)) for i, l in enumerate(self.lines)]
        sidx = [(i, m) for i, m in sidx if m]
        for j, (i, m) in enumerate(sidx):
            end = sidx[j + 1][0] if j + 1 < len(sidx) else None
            sec_end = self.sec.get(m.group(1).split(".")[0], (0, len(self.lines)))[1]
            self.sub[m.group(1)] = (i, min(end or sec_end, sec_end), m.group(2).strip())

    def section_text(self, n):
        s = self.sub.get(n) if "." in n else self.sec.get(n)
        if not s:
            return ""
        return "\n".join(self.lines[s[0]:s[1]])

    def section_of_line(self, i):
        name = ""
        for n, (a, b, t) in self.sec.items():
            if a <= i < b:
                name = f"§{n} {t}"
        for n, (a, b, t) in self.sub.items():
            if a <= i < b:
                name = f"§{n} {t}"
        return name

    def tables(self, n):
        return list(md_tables(self.section_text(n)))

    def table_dicts(self, n):
        out = []
        for heading, hdr, rows in self.tables(n):
            out.append([dict(zip(hdr, r + [""] * (len(hdr) - len(r)))) for r in rows])
        return out

    def scenarios(self):
        """AC id -> list of lines (from the gherkin block of §7)."""
        t = self.section_text("7")
        out, cur = OrderedDict(), None
        for l in t.splitlines():
            m = re.match(r"\s*Scenario(?: Outline)?:\s*(AC[\w-]+)", l)
            if m:
                cur = m.group(1)
                out[cur] = []
                continue
            if cur and l.strip() and not l.strip().startswith("```"):
                if re.match(r"\s*(Feature|Background):", l):
                    cur = None
                    continue
                out[cur].append(l.strip())
        return out

    def owned_acs(self):
        return list(self.scenarios().keys())


# ------------------------------------------------------------------------------- engine
class Checker:
    def __init__(self, src, wp, out):
        self.src, self.wp, self.out = src, wp, Path(out)
        self.rows, self.asms, self.cited = [], [], []
        self.report = {}
        self.wp_level_done = set()
        self.n = 0

    # row factory --------------------------------------------------------------------
    def add(self, st, check, typ, sev, title, section, description, evidence, proposed,
            owner="Business analyst", source="", area="Story", token="", fix=None, asm=None):
        self.n += 1
        row = OrderedDict(
            id=f"CG-{self.wp}-{self.n}", title=title, source=source, section=section,
            description=description, evidence=evidence, type=typ, area=area, severity=sev,
            needed_by_wave=st.meta.get("Wave", ""), legacy_ref=st.legacy, owner_role=owner,
            asm="", proposed=proposed, wp=self.wp, check=check, story=st.key, auto=True)
        if token:
            row["token"] = token
        if fix:
            row["fix"] = fix
        existing = self.existing(st, token or title)
        if existing:
            row["related"] = existing
        if asm:
            a = OrderedDict(id=row["id"].replace("CG-", "ASM-"), text=asm["text"], why=asm["why"],
                            read=asm.get("read", source), gap=row["id"], applied_in=f"{st.key} {section}",
                            confidence=asm.get("confidence", "Medium"), confirm=asm["confirm"],
                            impact=asm.get("impact", ""), wp=self.wp, story=st.key)
            row["asm"] = a["id"]
            self.asms.append(a)
        self.rows.append(row)
        return row

    def existing(self, st, token):
        """Register rows (GAP and ASM) and earlier WP rows that name this token and this story or
        legacy key. Returned as related IDs; the reviewer decides whether one is the same finding."""
        if not token or len(token) < 4:
            return []
        hits = []
        for key in ("gapreg",):
            for gid, r in self.src.register(key).items():
                blob = " ".join(r.values())
                if token in blob and (st.key in blob or (st.legacy and st.legacy in blob)):
                    hits.append(gid)
        for row in self.src.prior_rows():
            blob = json.dumps(row, ensure_ascii=False)
            if token in blob and (st.key in blob or (st.legacy and st.legacy == row.get("legacy_ref"))):
                hits.append(row.get("id", ""))
        return sorted(set(h for h in hits if h))[:12]

    # ---------------------------------------------------------------------------- run
    def run(self, st):
        t0 = time.time()
        rep = self.report.setdefault(st.key, {"file": str(st.path), "uncited_register_gaps": [],
                                              "open_defects": [], "checks_run": []})
        for fn in (self.x1, self.x3, self.x4, self.x5, self.x6, self.x7, self.x8, self.x9,
                   self.x10, self.x11, self.x12, self.x16, self.x17, self.x19, self.x20, self.x2_open_dl,
                   self.defects):
            try:
                fn(st)
                rep["checks_run"].append(fn.__name__)
            except Exception as e:  # a failing check never stops the run (AGENTS.md rule 13)
                rep.setdefault("check_errors", []).append(f"{fn.__name__}: {type(e).__name__}: {e}")
        rep["seconds"] = round(time.time() - t0, 2)

    # X1 ------------------------------------------------------------------------------
    def x1(self, st):
        lists, vals = self.src.lov()
        codes = {c for c, _ in vals.get("LOV-CASE-STATUS", [])}
        labels = {l.lower(): c for c, l in vals.get("LOV-CASE-STATUS", [])}
        _, trans = self.src.case_model()
        status_words = set(labels) | {c.lower() for c in codes}
        tables = st.table_dicts("9")
        for tbl in tables:
            if not tbl or "From" not in tbl[0] or "To" not in tbl[0]:
                continue
            values = [(r["From"], r["To"], r.get("Event", "")) for r in tbl]
            if not any(v.lower() in status_words for f, to, e in values for v in (f, to)):
                continue  # not a case-status table
            pairs = set()
            for tr in trans:
                tos = tr.get("To", "")
                for f in re.split(r",\s*", tr.get("From", "")):
                    f = f.strip().lower()
                    fs = [w for w in labels if w.startswith("waiting")] if f == "any waiting" else [f]
                    for ff in fs:
                        pairs.add((ff, tos.strip().lower()))
            bad = [(f, to, e) for f, to, e in values
                   for v in (f, to) if v.lower() not in status_words and v.lower() != "none"]
            for f, to, e in sorted(set(bad)):
                wrong = f if f.lower() not in status_words and f.lower() != "none" else to
                self.add(st, "X1", "Conflict", "P1",
                         f"Status '{wrong}' in the state table is not a value of LOV-CASE-STATUS",
                         "§9 State transitions",
                         f"{st.key} §9 has the transition {f} -> {to} on '{e}'. '{wrong}' is not a code or label of "
                         f"LOV-CASE-STATUS, and the Status transitions sheet has no such row.",
                         f"A) {st.key} §9 row '{f} | {e} | ... | {to}'. B) Reference Data v5, Values, LOV-CASE-STATUS: "
                         f"{', '.join(sorted(codes))}. C) Case and Workflow Model v6, Status transitions: no row from {f} to {to}.",
                         "Remove the row or use a status of LOV-CASE-STATUS with a transition of Case and Workflow Model v6 "
                         "(precedence 3 sources agree; no business value is decided here).",
                         owner="Business analyst",
                         source="06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx (Values); "
                                "02 Business architecture and process/Recovery Workbench Case and Workflow Model v6.xlsx (Status transitions)",
                         area="Case status", token=wrong,
                         fix={"kind": "delete_table_row", "match": f"| {f} | {e} |"})
            for f, to, e in values:
                fl, tl = f.lower(), to.lower()
                if fl in status_words and tl in status_words and fl != "none":
                    lf = next((l for l in labels if labels[l].lower() == fl or l == fl), fl)
                    lt = next((l for l in labels if labels[l].lower() == tl or l == tl), tl)
                    if (lf, lt) not in pairs and not any(p[0] == lf and "paused" in p[1] for p in pairs if lt):
                        self.add(st, "X1", "Conflict", "P2",
                                 f"Transition {f} -> {to} is not in Case and Workflow Model v6",
                                 "§9 State transitions",
                                 f"{st.key} §9 moves {f} to {to} on '{e}'; the Status transitions sheet has no such row.",
                                 f"A) {st.key} §9. B) Case and Workflow Model v6, Status transitions.",
                                 "Align §9 with Case and Workflow Model v6, or raise the transition with the business analyst.",
                                 source="02 Business architecture and process/Recovery Workbench Case and Workflow Model v6.xlsx",
                                 area="Case status", token=f"{f} -> {to}")
        # new values added to a closed list
        seen = set()
        all_codes = {c for v in vals.values() for c, _ in v}
        for i, l in enumerate(st.lines):
            for lst in sorted(set(re.findall(r"LOV-[A-Z0-9-]+[A-Z0-9]", l))):  # sorted: set order varies by process
                info = lists.get(lst)
                if not info or "closed" not in info.get("Kind", "").lower():
                    continue
                cs = {c for c, _ in vals.get(lst, [])}
                line_lists = set(re.findall(r"LOV-[A-Z0-9-]+[A-Z0-9]", l))
                for tok in re.findall(r"[\"`]([A-Z][A-Z0-9_]{2,})[\"`]", l):
                    if any(tok in {c for c, _ in vals.get(x, [])} for x in line_lists) or tok in all_codes:
                        continue
                    if not tok.startswith("LOV") and (lst, tok) not in seen:
                        seen.add((lst, tok))
                        where = [st.section_of_line(j) for j, x in enumerate(st.lines) if tok in x]
                        self.add(st, "X1", "Conflict", "P1",
                                 f"The story adds {tok} to the closed list {lst}",
                                 "; ".join(sorted(set(w for w in where if w))),
                                 f"{st.key} adds the value {tok} to {lst} as data. {lst} is a 'Closed list' in Reference Data v5 "
                                 f"(Lists), with the values {', '.join(sorted(cs))}; a closed list gains a value only by a change "
                                 f"of the list, and any service that holds the list as an enum must change too.",
                                 f"A) {st.key} line {i + 1}: '{l.strip()[:200]}'. B) Reference Data v5, Lists, {lst}: Kind "
                                 f"'{info.get('Kind')}'; Values: {', '.join(sorted(cs))}.",
                                 "Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the "
                                 "criterion uses an existing value. Needs a ruling; no edit until then.",
                                 owner="Product owner", area="Lists of values", token=tok,
                                 source="06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx (Lists, Values)")

    # X3 ------------------------------------------------------------------------------
    def x3(self, st):
        fields = self.src.ldm_fields()
        by_table = defaultdict(set)
        by_id = {}
        for r in fields:
            by_table[r.get("Entity", "")].add(r.get("Field", ""))
            if r.get("BR Field ID"):
                by_id[r["BR Field ID"]] = (r.get("Entity", ""), r.get("Field", ""))
        prev = defaultdict(set)
        for r in self.src.ldm_fields(prev=True):
            prev[r.get("Entity", "")].add(r.get("Field", ""))
        known = self.src.known_names()
        flagged = set()
        # index and constraint columns
        for i, l in enumerate(st.lines):
            for m in re.finditer(r"\bON\s+([a-z_][a-z0-9_]*)\s*\(([^)]*)\)", l):
                tbl = m.group(1)
                if tbl not in by_table:
                    continue
                for col in [c.strip(" `") for c in m.group(2).split(",")]:
                    if col and col not in by_table[tbl]:
                        flagged.add(col)
                        close = difflib.get_close_matches(col, sorted(by_table[tbl]), n=3, cutoff=0.5)
                        was = "Outdated" if col in prev.get(tbl, set()) else "Conflict"
                        self.add(st, "X3", was, "P1",
                                 f"Index column {tbl}.{col} is not a field of {tbl} in LDM v9",
                                 st.section_of_line(i),
                                 f"{st.key} builds an index or constraint on {tbl}({m.group(2).strip()}). LDM v9 Fields has no "
                                 f"field {col} on {tbl}" + (" (the field is in v8 and was renamed)" if was == "Outdated" else "") +
                                 (f"; the nearest fields are {', '.join(close)}." if close else "."),
                                 f"A) {st.key} line {i + 1}: '{l.strip()[:220]}'. B) LDM v9 Fields, entity {tbl}: "
                                 f"{', '.join(sorted(by_table[tbl]))[:600]}.",
                                 f"Use the LDM v9 field of {tbl} that holds this meaning" +
                                 (f" (candidate: {close[0]}; confirm against the Meaning column)" if close else "") + ".",
                                 owner="Data", area="Data model", token=col,
                                 source="06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (Fields)",
                                 fix={"kind": "rename_token", "old": col, "candidate": close[0] if close else None,
                                      "table": tbl})
        # other backticked names
        names = defaultdict(list)
        for i, l in enumerate(st.lines):
            if l.startswith("| DP-"):
                continue  # Pattern application table: the legacy-marker column names retired objects on purpose
            for tok in SNAKE.findall(l):
                if re.fullmatch(r"rwb_[a-z_]+", tok) or tok.startswith(NOT_FIELDS_PREFIX) or tok in flagged or tok in known:
                    continue
                names[tok].append(i)
        for tok, where in names.items():
            any_prev = any(tok in s for s in prev.values())
            close = difflib.get_close_matches(tok, sorted(known), n=3, cutoff=0.6)
            self.add(st, "X3", "Outdated" if any_prev else "Missing", "P2",
                     f"Name `{tok}` is not a field or entity in LDM v9 or Data Classification v5",
                     "; ".join(sorted(set(st.section_of_line(i) for i in where))),
                     f"{st.key} names `{tok}` {len(where)} time(s); no entity or field of that name is in LDM v9 Fields or "
                     f"Data Classification v5 Fields" + (" (it is in LDM v8)" if any_prev else "") +
                     (f". Nearest names: {', '.join(close)}." if close else "."),
                     f"A) {st.key} lines {', '.join(str(i + 1) for i in where[:8])}. B) LDM v9 Fields; Data Classification v5 Fields.",
                     "Use the dictionary name, or record the object (index, library table, flag) in the owning document.",
                     owner="Data", area="Data model", token=tok,
                     source="06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (Fields)",
                     fix={"kind": "rename_token", "old": tok, "candidate": close[0] if close else None})
        # field-ID ranges in §11
        for tbl in st.table_dicts("11"):
            for r in tbl:
                fid = r.get("BR Field ID", "")
                ent = r.get("Entity in rwb_case") or next((v for k, v in r.items() if k.startswith("Entity")), "")
                ent = ent.split(" ")[0]
                m = re.fullmatch(r"(DF-[A-Z]+-)(\d+) to (DF-[A-Z]+-)(\d+)", fid.strip())
                ids = []
                if m and m.group(1) == m.group(3):
                    w = len(m.group(2))
                    ids = [f"{m.group(1)}{n:0{w}d}" for n in range(int(m.group(2)), int(m.group(4)) + 1)]
                elif re.fullmatch(r"DF-[A-Z]+-\d+", fid.strip()):
                    ids = [fid.strip()]
                if not ids or ent not in by_table:
                    continue
                wrong = [(x, by_id.get(x, ("(no row)", ""))[0]) for x in ids if by_id.get(x, ("", ""))[0] != ent]
                if wrong:
                    self.add(st, "X3", "Conflict", "P2",
                             f"Field IDs {fid} are not all fields of {ent} in LDM v9",
                             "§11 Data",
                             f"{st.key} §11 maps {fid} to {ent}; LDM v9 gives another entity (or no row) for "
                             f"{len(wrong)} of {len(ids)} IDs.",
                             "A) " + f"{st.key} §11 row '{fid} | {ent}'. B) LDM v9 Fields: " +
                             "; ".join(f"{x} -> {e}" for x, e in wrong[:12]) + ("; ..." if len(wrong) > 12 else ""),
                             "Correct the field ID range to the LDM v9 rows of the entity.",
                             owner="Data", area="Data model", token=fid,
                             source="06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (Fields)")

    # X4 ------------------------------------------------------------------------------
    PARAM = re.compile(r"[Pp]arameters?\s+[`\"]([a-z][a-z0-9_]*(?:\.[a-z0-9_]+){1,5})[`\"]")

    def x4(self, st):
        keys = defaultdict(list)
        for i, l in enumerate(st.lines):
            for k in self.PARAM.findall(l):
                keys[k].append(i)
        cat = self.src.params()
        if keys and cat is None and "params" not in self.wp_level_done:
            self.wp_level_done.add("params")
            wl = self.add(st, "X4", "Missing", "P1", "parameter-catalog.csv is empty, so no parameter key can be checked",
                     "Root file parameter-catalog.csv",
                     "The parameter catalog at the root has no rows (0 bytes). Every story that reads a parameter key "
                     "cites this one row; no key can be confirmed and two names for one parameter cannot be caught.",
                     "parameter-catalog.csv: 0 bytes.",
                     "Publish the parameter catalog with key, owner, type, default and the story that reads each key.",
                     owner="Business analyst", area="Parameters", token="parameter-catalog.csv", source="parameter-catalog.csv")
            wl["wp_level"] = "params"  # one row per run; the parallel merge keeps the first
        corpus = self.src.corpus()
        lists, _ = self.src.lov()
        for k, where in keys.items():
            if cat is not None and k not in cat:
                self.add(st, "X4", "Missing", "P2", f"Parameter key {k} is not in parameter-catalog.csv",
                         "; ".join(sorted(set(st.section_of_line(i) for i in where))),
                         f"{st.key} reads parameter {k}; the catalog has no such key.",
                         f"A) {st.key} lines {', '.join(str(i + 1) for i in where[:6])}. B) parameter-catalog.csv.",
                         "Add the key to the catalog or use the catalog name.", area="Parameters", token=k,
                         source="parameter-catalog.csv")
            head, last = k.rsplit(".", 1)
            pat = re.compile(re.escape(head) + r"\.(" + re.escape(last) + r"_[a-z0-9_]+|[a-z0-9_]+_" + re.escape(last) + r")\b")
            others = defaultdict(set)
            for doc, txt in corpus.items():
                if doc == str(st.path):
                    continue
                for m in pat.finditer(txt):
                    others[f"{head}.{m.group(1)}"].add(doc)
            for other, docs in others.items():
                self.add(st, "X4", "ID collision", "P1", f"Parameter {k} is also written as {other}",
                         "; ".join(sorted(set(st.section_of_line(i) for i in where))),
                         f"{st.key} reads {k}; other documents name what reads as the same threshold {other}. A build "
                         f"against one name fails against the other, and the catalog cannot settle it"
                         + (" because it is empty." if cat is None else "."),
                         f"A) {st.key}: {k}. B) {other} in: " + "; ".join(sorted(Path(d).name for d in docs)[:6]),
                         "Rule one parameter key and record it in parameter-catalog.csv. Needs a ruling; no edit until then.",
                         owner="Business analyst", area="Parameters", token=other,
                         source="; ".join(sorted(Path(d).name for d in docs)[:6]))
        for lst in sorted(set(re.findall(r"LOV-[A-Z0-9-]+[A-Z0-9]", st.text))):
            if lst not in lists:
                self.add(st, "X4", "Missing", "P2", f"List {lst} is not in Reference Data v5",
                         "Story text", f"{st.key} names {lst}; Reference Data v5 Lists has no such list.",
                         f"Reference Data v5, Lists: no row {lst}.", "Use a list of Reference Data v5 or add the list.",
                         area="Lists of values", token=lst,
                         source="06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx (Lists)")

    # X5 ------------------------------------------------------------------------------
    @staticmethod
    def _norm(p):
        return re.sub(r"\{[^}]*\}", "{}", p.strip().strip("`").split("?")[0].rstrip("/"))

    def x5(self, st):
        api = self.src.api()
        by_base = {v["base"]: (k, v) for k, v in api.items() if v["base"]}
        own = api.get(st.service)
        # provided
        t121 = st.section_text("12.1")
        mb = re.search(r"Base `([^`]+)`", t121)
        base = mb.group(1) if mb else (own or {}).get("base", "")
        for tbl in st.table_dicts("12.1"):
            for r in tbl:
                meth, path = r.get("Method", "").upper(), r.get("Path", "").strip("` ")
                if not meth or not path:
                    continue
                if not own:
                    continue
                paths = {self._norm(p): m for p, m in own["paths"].items()}
                np_ = self._norm(path)
                if np_ not in paths or meth not in paths[np_]:
                    self.add(st, "X5", "Missing", "P1", f"{meth} {path} is not in {own['file']}",
                             "§12.1 REST operations provided",
                             f"{st.key} provides {meth} {base}{path}; API Specification v5 {own['file']} has "
                             + ("the path with methods " + ",".join(sorted(paths[np_])) if np_ in paths else "no such path") + ".",
                             f"A) {st.key} §12.1. B) API Specification v5/{own['file']} paths.",
                             "Publish the operation in the owner's yaml through the CON story, or remove it.",
                             owner="Solution architect", area="API and edge", token=f"{meth} {path}",
                             source=f"05 Technical architecture/Recovery Workbench API Specification v5/{own['file']}")
        # consumed
        for tbl in st.table_dicts("12.2"):
            for r in tbl:
                meth, path = r.get("Method", "").upper(), r.get("Path", "").strip("` ")
                if not meth or not path.startswith("/api/"):
                    continue
                hit = next(((b, v) for b, v in by_base.items() if path.startswith(b + "/")), None)
                if not hit:
                    self.add(st, "X5", "Missing", "P1", f"No API Specification v5 yaml has the base of {path}",
                             "§12.2 REST operations consumed", f"{st.key} consumes {meth} {path}; no yaml declares its REST base.",
                             f"A) {st.key} §12.2. B) API Specification v5 yaml REST bases.",
                             "Use the provider's REST base from the Document Index service table.",
                             owner="Solution architect", area="API and edge", token=path)
                    continue
                b, (svc, v) = hit
                rest = self._norm(path[len(b):])
                paths = {self._norm(p): m for p, m in v["paths"].items()}
                if rest not in paths or meth not in paths[rest]:
                    near = difflib.get_close_matches(rest, sorted(paths), n=2, cutoff=0.4)
                    self.add(st, "X5", "Missing", "P1", f"{meth} {path} is not published by {svc}",
                             "§12.2 REST operations consumed",
                             f"{st.key} consumes {meth} {path} from {svc}; {v['file']} has "
                             + (f"the path with {','.join(sorted(paths[rest]))}" if rest in paths else "no such path")
                             + (f". Nearest paths: {', '.join(near)}." if near else "."),
                             f"A) {st.key} §12.2 row '{meth} | {path}'. B) API Specification v5/{v['file']} paths.",
                             f"Publish the operation in {v['file']} through the provider's CON story, or consume a published "
                             "operation. Needs the provider's ruling; no edit until then.",
                             owner="Solution architect", area="API and edge", token=path,
                             source=f"05 Technical architecture/Recovery Workbench API Specification v5/{v['file']}")
        # HTTP statuses without a message ID
        m = re.search(r"Errors?:\s*(.+)", t121)
        if m:
            parts = re.split(r",\s*(?=[1-5]\d\d\b)|;\s*", m.group(1))
            nomsg = [p.strip().rstrip(".") for p in parts if re.match(r"[45]\d\d\b", p.strip()) and "MSG-" not in p]
            if nomsg:
                self.add(st, "X5", "Missing", "P2", "HTTP errors with no message ID: " + "; ".join(nomsg),
                         "§12.1 REST operations provided",
                         f"{st.key} maps {', '.join(nomsg)} with no message ID of the Error and Message Standard v4.",
                         f"A) {st.key} §12.1 Errors line. B) Error and Message Standard v4 §4.",
                         "Map each status to a message ID of the standard (for a store failure the standard's "
                         "system-unavailable message, if it fits; the business analyst confirms).",
                         area="Messages", token="503" if any(p.startswith("503") for p in nomsg) else nomsg[0][:3],
                         source="07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx")
        # story keys exist
        idx = self.src.story_index()
        meta_txt = " ".join(st.meta.values()) + " " + st.section_text("13")
        for k in sorted(set(re.findall(r"RWB-[A-Z0-9]+-[A-Z0-9]+-(?:APP-\d+|APP|CON|OPS|ITG|DB|INF)\b", meta_txt))):
            if k not in idx:
                self.add(st, "X5", "Missing", "P1", f"Story {k} named as a dependency does not exist",
                         "Metadata table; §13 Pattern application",
                         f"{st.key} depends on {k}; no story file of that key is under the service story folder.",
                         f"A) {st.key} metadata or §13. B) 04 User stories/Recovery Workbench Service Story Files v1/: no file.",
                         "Name the story that exists (for example the same capability under another key) or create it.",
                         owner="Solution architect", area="Dependencies", token=k)
        # closed enum in the yaml while the story keeps the list as data
        if own and re.search(r"without a code change|not from code|no Java enum|as data", st.text):
            lists, _ = self.src.lov()
            for lst in sorted(set(re.findall(r"LOV-[A-Z0-9-]+[A-Z0-9]", st.text))):
                cols = [r.get("Field", "") for r in self.src.ldm_fields() if r.get("List of values", "").strip() == lst]
                for col in sorted(set(cols)):
                    camel = re.sub(r"_([a-z0-9])", lambda x: x.group(1).upper(), col)
                    y = own["yaml"]
                    mm = re.search(r"\n(\s+)" + re.escape(camel) + r":\n((?:\1\s+.*\n){0,6})", y)
                    if mm and "enum:" in mm.group(2):
                        self.add(st, "X5", "Conflict", "P1",
                                 f"{own['file']} holds {camel} as a closed enum while the story reads {lst} as data",
                                 "§8 Business rules; §9; §13 Components",
                                 f"{st.key} says {lst} values are data accepted without a code change; {own['file']} "
                                 f"declares {camel} with a fixed enum, so a new list value fails schema validation.",
                                 f"A) {st.key}: '{re.search(r'[^.]*(without a code change|not from code|no Java enum|as data)[^.]*', st.text).group(0).strip()[:200]}'. "
                                 f"B) {own['file']}: {camel} enum. C) Reference Data v5 Lists: {lst} "
                                 f"'{lists.get(lst, {}).get('Kind', '')}'.",
                                 "Rule whether the list is closed (story changes) or data (yaml enum removed). Needs a ruling.",
                                 owner="Solution architect", area="API and edge", token=camel,
                                 source=f"05 Technical architecture/Recovery Workbench API Specification v5/{own['file']}")
                        break

    # X6 ------------------------------------------------------------------------------
    def x6(self, st):
        evs = {r["Event type (ce_type)"]: r for r in self.src.kafka_events()}
        for sub, direction in (("12.3", "Published"), ("12.4", "Consumed")):
            for tbl in st.table_dicts(sub):
                for r in tbl:
                    m = re.search(r"`?(rwb\.[\w.-]+\.v\d+)`?", r.get("Event", ""))
                    if not m:
                        continue
                    ce = m.group(1)
                    cat = evs.get(ce)
                    topic = r.get("Topic", "").strip("` ")
                    alt = [k for k in evs if k.split(".")[-2:] == ce.split(".")[-2:]] if not cat else []
                    if not cat and alt:
                        self.add(st, "X6", "Conflict", "P1", f"Event type {ce} is {alt[0]} in Kafka Catalog v1",
                                 f"§{sub}", f"{st.key} names the event type {ce}; Kafka Catalog v1 Events row "
                                 f"{evs[alt[0]].get('EV row')} gives ce_type {alt[0]} on topic {evs[alt[0]].get('Topic')}.",
                                 f"A) {st.key} §{sub} row '{r.get('Event', '')[:80]}'. B) Kafka Topic and Event Catalog v1, Events row "
                                 f"{evs[alt[0]].get('EV row')}; Envelope sheet ce_type rule.",
                                 f"Use ce_type {alt[0]} (precedence 1 catalog).", owner="Solution architect", area="Events",
                                 token=ce, source="05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (Events)",
                                 fix={"kind": "replace_all", "pairs": [[ce, alt[0]]]})
                        continue
                    if not cat:
                        self.add(st, "X6", "Missing", "P1", f"Event type {ce} is not in Kafka Catalog v1",
                                 f"§{sub}", f"{st.key} {direction.lower()}s {ce}; the Events sheet has no such type.",
                                 f"A) {st.key} §{sub}. B) Kafka Topic and Event Catalog v1, Events.",
                                 "Use the catalogued event type or add it to the catalog.", owner="Solution architect",
                                 area="Events", token=ce,
                                 source="05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx")
                        continue
                    if topic and topic != cat.get("Topic", ""):
                        self.add(st, "X6", "Conflict", "P1", f"{ce} is on topic {cat.get('Topic')} in the catalog, not {topic}",
                                 f"§{sub}", f"{st.key} names topic {topic} for {ce}.",
                                 f"A) {st.key} §{sub}. B) Kafka Catalog v1 Events row {cat.get('EV row')}: topic {cat.get('Topic')}.",
                                 f"Use topic {cat.get('Topic')}.", owner="Solution architect", area="Events", token=ce,
                                 source="05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx",
                                 fix={"kind": "replace", "old": topic, "new": cat.get("Topic")})
                    if direction == "Published":
                        sp = {x.strip().lower() for x in re.split(r",\s*", r.get("Payload (IDs and facts only)", r.get("Payload", ""))) if x.strip()}
                        cp = {x.strip().lower() for x in re.split(r",\s*", cat.get("Payload", "")) if x.strip()}
                        if sp and cp and sp != cp and ce.split(".")[1] in (st.service.replace("rwb-", ""),):
                            self.add(st, "X6", "Conflict", "P2", f"Payload of {ce} differs from Kafka Catalog v1",
                                     f"§{sub}", f"{st.key} payload: {', '.join(sorted(sp))}; catalog: {', '.join(sorted(cp))}.",
                                     f"A) {st.key} §{sub}. B) Kafka Catalog v1 Events row {cat.get('EV row')}.",
                                     "Align the payload with the catalog.", owner="Solution architect", area="Events", token=ce,
                                     source="05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx")
                    elif st.worktype != "ITG":
                        cons = cat.get("Consumers", "")
                        if st.service and st.service not in cons:
                            self.add(st, "X6", "Conflict", "P2", f"{st.service} is not a consumer of {ce} in Kafka Catalog v1",
                                     f"§{sub}", f"{st.key} consumes {ce}; the catalog consumers are: {cons}.",
                                     f"A) {st.key} §{sub}. B) Kafka Catalog v1 Events row {cat.get('EV row')}.",
                                     f"Add {st.service} as a consumer in the catalog (and its ACL), or drop the handler.",
                                     owner="Solution architect", area="Events", token=ce,
                                     source="05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx")
        wfs, acts, _ = self.src.temporal()
        wf = {r.get("Workflow", ""): r for r in wfs}
        act = {re.sub(r"\(.*", "", r.get("Activity", "")).strip(): r for r in acts}
        for tbl in st.table_dicts("12.5"):
            for r in tbl:
                name, typ, q = r.get("Name", "").strip("` "), r.get("Type", ""), r.get("Task queue", "").strip("` ")
                if not name:
                    continue
                if typ.lower().startswith("workflow"):
                    c = wf.get(name)
                    if not c:
                        self.add(st, "X6", "Missing", "P1", f"Workflow {name} is not in Temporal Catalog v1",
                                 "§12.5", f"{st.key} names workflow {name}; the Workflows sheet has no such row.",
                                 f"A) {st.key} §12.5. B) Temporal Catalog v1, Workflows.", "Use the catalogued workflow.",
                                 owner="Solution architect", area="Workflows", token=name,
                                 source="05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx")
                        continue
                    if q and q != c.get("Task queue", ""):
                        self.add(st, "X6", "Conflict", "P1", f"Workflow {name} task queue {q} differs from the catalog",
                                 "§12.5", f"{st.key}: {q}; catalog: {c.get('Task queue')}.",
                                 f"A) {st.key} §12.5. B) Temporal Catalog v1 Workflows row {name}.",
                                 f"Use task queue {c.get('Task queue')}.", owner="Solution architect", area="Workflows", token=name,
                                 source="05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx")
                    # workflow ID form
                    story_form = re.findall(r"workflow ID (?:=|equal to|is) ([^,;)|]+)", st.text)
                    story_form = sorted(set(f.strip() for f in story_form if name in st.text))
                    own_form = [f for f in story_form] if re.search(r"workflow ID", typ + r.get("Purpose", "")) else []
                    cat_started = c.get("Started by", "")
                    cat_forms = re.findall(r"workflow ID = ([^;(]+)|writes ([\w{}-]+)", cat_started)
                    cat_forms = [a or b for a, b in cat_forms]
                    gaps = re.findall(r"GAP-\d{4}", cat_started)
                    stated = own_form or ([] if name != "CaseWorkflow" else story_form)
                    if st.worktype == "ITG" or c.get("Service", "") != st.service:
                        continue  # the owning service's story states the ID form
                    if not re.search(r"workflow ID", typ + " " + r.get("Purpose", "")) and not (
                            re.search(re.escape(name) + r"[^.\n]*workflow ID", st.text)):
                        self.add(st, "X6", "Missing", "P2", f"Workflow ID form and start rule of {name} are not stated",
                                 "§12.5; §4 Flow",
                                 f"{st.key} starts {name} but states no workflow ID form and no duplicate-start policy; "
                                 f"the catalog row reads: '{cat_started[:240]}'.",
                                 f"A) {st.key} §12.5 row {name}. B) Temporal Catalog v1 Workflows row {name}"
                                 + (f" (related {', '.join(gaps)})" if gaps else "") + ".",
                                 "State the workflow ID form (for example one per business date) and the start rule "
                                 "(start or signalWithStart, duplicate-start policy) from the catalog; where the catalog "
                                 "does not give one, it is Not specified in the source documents.",
                                 owner="Solution architect", area="Workflows", token=f"{name} workflow ID",
                                 source="05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (Workflows)")
                    elif len(set(cat_forms)) > 1 or gaps:
                        self.add(st, "X6", "Ambiguous", "P2", f"Two workflow ID forms for {name} in the sources",
                                 "§12.5; §4 Flow",
                                 f"{st.key} uses '{'; '.join(stated) or 'workflow ID = case ID'}'; the catalog names "
                                 f"{' and '.join(cat_forms) or 'more than one form'}"
                                 + (f" and cites {', '.join(gaps)}" if gaps else "") + ".",
                                 f"A) {st.key} §12.5. B) Temporal Catalog v1 Workflows row {name}: '{cat_started[:240]}'.",
                                 "Solution architect rules the one workflow ID form; the story copies it.",
                                 owner="Solution architect", area="Workflows", token=f"{name} workflow ID",
                                 source="05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (Workflows)",
                                 asm={"text": f"{name} is built with the workflow ID form the story writes ('{'; '.join(stated) or 'case ID'}') until the solution architect rules.",
                                      "why": "The catalog carries two forms; no source settles which one wins.",
                                      "confirm": "Solution architect confirms the workflow ID form", "confidence": "Low"})
                elif typ.lower().startswith("activity"):
                    if name not in act:
                        self.add(st, "X6", "Missing", "P2", f"Activity {name} is not in Temporal Catalog v1",
                                 "§12.5", f"{st.key} names activity {name}; the Activities sheet has no such row.",
                                 f"A) {st.key} §12.5. B) Temporal Catalog v1, Activities.",
                                 "Add the activity to the catalog or use a catalogued one.", owner="Solution architect",
                                 area="Workflows", token=name,
                                 source="05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx")

    # X7 ------------------------------------------------------------------------------
    def x7(self, st):
        rules_txt = self.src.converted("rules")
        known = set(re.findall(r"R-[A-Z]+-\d+", rules_txt))
        for rid in sorted(set(re.findall(r"\bR-[A-Z]{2,5}-\d+\b", st.text))):
            if rid not in known:
                self.add(st, "X7", "Missing", "P2", f"Rule {rid} is not in Business Rules v4",
                         "Story text", f"{st.key} cites {rid}; Business Rules and Routing Logic v4 has no such rule.",
                         f"Business Rules v4, Rules: no {rid}.", "Cite a rule of Business Rules v4.", area="Rules", token=rid,
                         source="02 Business architecture and process/Recovery Workbench Business Rules and Routing Logic v4.xlsx")
        corpus = self.src.corpus(exclude_stories=True)
        for lit in sorted(set(re.findall(r"\"((?:EXCL|ENTRY|ENT|ALLOC|RTE)-\d{3})\"", st.section_text("7") + st.section_text("12.8")))):
            # a register naming the ID as a gap, or a test row copied from a story, does not define it
            regs = (rwbsrc.TEXT["gapreg"], rwbsrc.TEXT["asmreg"], rwbsrc.SOURCES["tc"], rwbsrc.SOURCES["rtm"])
            docs = [d for d, t in corpus.items() if lit in t and d not in regs]
            if not docs:
                self.add(st, "X7", "Missing", "P2", f"Rule ID {lit} used in the criteria exists in no current source",
                         "§7 Acceptance criteria; §12.8 Contract fakes",
                         f"{st.key} asserts rule ID {lit}; no current source document (outside the story files) holds it, "
                         "so the test data cannot be built from a source.",
                         f"A) {st.key} §7. B) searched: {len(corpus)} current source documents.",
                         "Take the rule ID from the approved package (RWB-P3-E1073-APP) or mark it as test data.",
                         area="Rules", token=lit)

    # X8 ------------------------------------------------------------------------------
    @staticmethod
    def _nm(s):
        return " ".join(s.replace("’", "'").replace("“", '"').replace("”", '"').split()).strip()

    def x8(self, st):
        msgs = self.src.messages()
        for tbl in st.table_dicts("14"):
            for r in tbl:
                mid, txt = r.get("ID", ""), r.get("Message", "")
                if not mid.startswith("MSG-"):
                    continue
                std = msgs.get(mid)
                if not std:
                    continue  # reported below
                if self._nm(txt) != self._nm(std.get("English", "")):
                    sim = difflib.SequenceMatcher(None, self._nm(txt).lower(), self._nm(std.get("English", "")).lower()).ratio()
                    if sim < 0.45:
                        self.add(st, "X8", "ID collision", "P2", f"{mid} is used with another meaning than the standard's",
                                 "§14 Validation and messages",
                                 f"{st.key} uses {mid} for '{r.get('When', '')}' with the text '{txt}'; the standard holds {mid} "
                                 f"for '{std.get('Raised when', '')}': '{std.get('English')}'.",
                                 f"A) {st.key} §14 row {mid}. B) Error and Message Standard v4 §4 row {mid}.",
                                 "The business analyst adds a new message ID to the standard for the story's use; the story "
                                 "then cites it. Needs a new ID; no edit until it exists.",
                                 area="Messages", token=mid,
                                 source="07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx")
                        continue
                    ph_s = set(re.findall(r"\{\w+\}", txt))
                    ph_c = set(re.findall(r"\{\w+\}", std.get("English", "")))
                    self.add(st, "X8", "Conflict", "P2" if ph_s != ph_c else "P3",
                             f"{mid} text differs from the Error and Message Standard v4",
                             "§14 Validation and messages",
                             f"{st.key} shows '{txt}'; the standard holds '{std.get('English')}' for '{std.get('Raised when', '')}'."
                             + (f" Placeholders differ: story {sorted(ph_s)}, standard {sorted(ph_c)}." if ph_s != ph_c else ""),
                             f"A) {st.key} §14 row {mid}. B) Error and Message Standard v4 §4 row {mid}.",
                             f"Copy the English text of {mid} from the standard; if the story's use differs from "
                             "'Raised when', the business analyst adds a new message ID instead.",
                             area="Messages", token=mid,
                             source="07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx",
                             fix={"kind": "replace_cell", "old": txt, "new": std.get("English", ""), "row": mid})
        for mid in sorted(set(re.findall(r"MSG-[A-Z0-9]+-\d{3}", st.text))):
            if mid not in msgs:
                self.add(st, "X8", "Missing", "P2", f"{mid} is not in the Error and Message Standard v4",
                         "Story text", f"{st.key} cites {mid}; the standard has no such ID.",
                         f"Error and Message Standard v4 §4: no {mid}.", "Add the message to the standard or use an existing ID.",
                         area="Messages", token=mid,
                         source="07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx")

    # X9 ------------------------------------------------------------------------------
    def x9(self, st):
        TCV = _tcv()
        tcs = self.src.test_cases()
        owned = set(st.owned_acs())
        rows = [r for tbl in st.table_dicts("16") for r in tbl if r.get("TC ID", "").startswith("TC-")]
        if not rows:
            return
        missing = [r["TC ID"] for r in rows if r["TC ID"] not in tcs]
        if missing:
            new_story = st.worktype in ("CON", "DB", "INF", "OPS")
            self.add(st, "X9", "Missing", "P3" if new_story else "P2",
                     f"Test cases not in {TCV}: {', '.join(missing)}", "§16 Test cases",
                     f"{st.key} lists {', '.join(missing)}; {TCV} 'Story test cases' has no row for them, so the "
                     "Given, When and expected result are nowhere written.",
                     f"A) {st.key} §16. B) {TCV}, Story test cases: no row.",
                     "Add the rows to the next Test Cases version, with Given, When and Then copied from the criterion they cover.",
                     owner="QA", area="Testing", token=missing[0],
                     source=rwbsrc.SOURCES["tc"] + " (Story test cases)",
                     fix={"kind": "tc_rows", "ids": missing})
        covered = set()
        diff = []
        foreign = []
        for r in rows:
            acs = set(re.findall(r"AC[\w-]*\d+", r.get("Covers", "")))
            covered |= acs
            c = tcs.get(r["TC ID"])
            if c:
                cacs = set(re.findall(r"AC[\w-]*\d+", c.get("Covers", "")))
                if acs and cacs and acs.isdisjoint(cacs):
                    diff.append(f"{r['TC ID']} story {','.join(sorted(acs))} / v8 {','.join(sorted(cacs))}")
            if acs and owned and acs.isdisjoint(owned):
                foreign.append(f"{r['TC ID']} ({','.join(sorted(acs))})")
        if diff:
            self.add(st, "X9", "Conflict", "P3", f"Test cases cover other criteria in {TCV}", "§16 Test cases",
                     f"{st.key} §16 and {TCV} disagree on what {len(diff)} test case(s) cover.",
                     "; ".join(diff), f"Align §16 with {TCV}.", owner="QA", area="Testing", token=diff[0].split()[0],
                     source=rwbsrc.SOURCES["tc"])
        if foreign:
            self.add(st, "X9", "Missing", "P3", "Test cases listed for criteria this story does not own", "§16 Test cases",
                     f"{st.key} §16 lists {', '.join(foreign)}; those criteria are not in this story's §7, so the tests "
                     "belong to the story that owns them.",
                     f"A) {st.key} §7 owns {', '.join(sorted(owned))}. B) §16 rows {', '.join(foreign)}.",
                     "Move the rows to the owning story, or mark them 'run by <owner story>'.", owner="QA", area="Testing",
                     token=foreign[0].split()[0])
        uncovered = sorted(owned - covered, key=lambda a: int(re.sub(r"\D", "", a) or 0))
        if uncovered:
            self.add(st, "X9", "Missing", "P2", f"Criteria with no test case: {', '.join(uncovered)}", "§7; §16",
                     f"{st.key} owns {', '.join(uncovered)} with no test case in §16.",
                     f"{st.key} §7 and §16.", "Add a test case per criterion.", owner="QA", area="Testing", token=uncovered[0])
        # RTM against §18
        rtm = self.src.rtm()
        dif = []
        for tbl in st.table_dicts("18"):
            for r in tbl:
                rid = r.get("Requirement ID", "")
                if rid in rtm:
                    s = set(re.findall(r"TC-[\w-]+\d", r.get("Test cases", "")))
                    rr = rtm[rid]
                    m = set(re.findall(r"TC-[\w-]+\d", rr[10] if len(rr) > 10 else ""))
                    if s and m and s != m:
                        dif.append(f"{rid}: story {', '.join(sorted(s))}; RTM {', '.join(sorted(m))}")
        if dif:
            self.add(st, "X9", "Conflict", "P3", "§18 test lists differ from RTM v7", "§18 Traceability",
                     f"{st.key} §18 and RTM v7 trace different tests for {len(dif)} requirement(s).",
                     "; ".join(dif), "Align §18 and the RTM in their next versions.", owner="QA", area="Testing",
                     token=dif[0].split(":")[0],
                     source="09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (RTM)")

    # X10 -----------------------------------------------------------------------------
    def x10(self, st):
        if not re.search(r"no personal data", st.text, re.I):
            return
        dc = defaultdict(set)
        for r in rwbsrc.sheet(self.src.converted("dclass"), "Fields"):
            if r.get("Personal data", "").strip().lower() not in ("no", ""):
                dc[r.get("Field", "")].add(f"{r.get('Entity')}.{r.get('Field')} {r.get('Classification')} / {r.get('Personal data category')}")
        hits = []
        for tbl in st.table_dicts("12.3"):
            for r in tbl:
                for k in re.split(r",\s*", r.get("Payload (IDs and facts only)", r.get("Payload", ""))):
                    snake = re.sub(r"([A-Z])", lambda m: "_" + m.group(1).lower(), k.strip())
                    if snake in dc:
                        hits.append(f"{k.strip()} ({'; '.join(sorted(dc[snake]))[:160]})")
        for l in st.lines:
            if re.search(r"run reads|log|workflow payload", l, re.I):
                for k in re.findall(r"`([a-z_]+)`", l):
                    if k in dc and not any(h.startswith(k) for h in hits):
                        hits.append(f"{k} ({'; '.join(sorted(dc[k]))[:160]})")
        if hits:
            self.add(st, "X10", "Conflict", "P2", "Fields classed as personal data where the story says none is carried",
                     "§12.3; §17 Guardrails",
                     f"{st.key} says no personal data is carried, but Data Classification v5 classes these as personal data: "
                     + "; ".join(hits[:8]),
                     f"A) {st.key} §12.3 and §17. B) Data Classification v5, Fields.",
                     "State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field.",
                     owner="Compliance", area="Personal data", token=hits[0].split()[0],
                     source="06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (Fields)")

    # X11 -----------------------------------------------------------------------------
    def x11(self, st):
        seen = set()
        for i, l in enumerate(st.lines):
            for pkg in re.findall(r"\b((?:th|com|org)\.[a-z0-9_]+(?:\.[a-z0-9_]+)+)", l):
                bad = [s for s in pkg.split(".") if s in JAVA_RESERVED]
                if bad and pkg not in seen:
                    seen.add(pkg)
                    self.add(st, "X11", "Conflict", "P1", f"Java package {pkg} uses the reserved word '{bad[0]}'",
                             st.section_of_line(i),
                             f"{st.key} names the Java package {pkg}; '{bad[0]}' is a Java reserved word, so the package "
                             "does not compile.",
                             f"A) {st.key} line {i + 1}. B) Java Language Specification reserved words.",
                             "Solution architect rules the package segment for the service (the Service Template "
                             "Specification v1 naming rule); the story copies it. No name is invented here.",
                             owner="Solution architect", area="Platform names", token=pkg)
        for i, l in enumerate(st.lines):
            for f in re.findall(r"`(V[\w.]+__\w+\.sql)`", l):
                if f in seen:
                    continue
                seen.add(f)
                if not re.fullmatch(r"V\d{4}__\w+\.sql", f):
                    self.add(st, "X11", "Conflict", "P3", f"Flyway file {f} is not in the V0001..Vnnnn form",
                             st.section_of_line(i),
                             f"{st.key} names the migration {f}; Service Template Specification v1 §3 gives the Flyway "
                             "sequence V0001 to Vnnnn, owned by the service.",
                             f"A) {st.key} line {i + 1}. B) Service Template Specification v1 §3.1 table row "
                             "'src/main/resources/db/migration'.",
                             "Use the next number of the service's own sequence.", owner="Solution architect",
                             area="Platform names", token=f,
                             source="05 Technical architecture/Recovery Workbench Service Template Specification v1.md")

    # X12 -----------------------------------------------------------------------------
    def x12(self, st):
        if st.code == "P1":
            return
        ace = re.compile(r"(recovery\.v_ace_\w*|\bv_ace_\w+|\baccount_ext\b|\bparty_ext\b)")
        legacy = re.compile(r"(\bJOB-\d+\b|decision log|job record|COLLINS)", re.I)
        has_wf = any(r.get("Type", "").lower().startswith("workflow") for tbl in st.table_dicts("12.5") for r in tbl)
        hits_ace, hits_leg = [], []
        for ac, lines in st.scenarios().items():
            for l in lines:
                if ace.search(l):
                    hits_ace.append(f"{ac}: {l[:120]}")
                if has_wf and legacy.search(l):
                    hits_leg.append(f"{ac}: {l[:120]}")
        for r in (r for tbl in st.table_dicts("16") for r in tbl):
            line = " ".join(r.values())
            if ace.search(line):
                hits_ace.append(f"{r.get('TC ID')}: {r.get('Data', '')[:120]}")
            if has_wf and legacy.search(line):
                hits_leg.append(f"{r.get('TC ID')}: {line[:120]}")
        s4 = st.section_text("4").splitlines()
        for l in s4:
            if ace.search(l) and not re.match(r"\d+\.\s*rwb-source-data:", l.strip()) and not re.search(r"never|no ACE view", l):
                hits_ace.append(f"§4: {l.strip()[:120]}")
        if hits_ace:
            self.add(st, "X12", "Outdated", "P2", "Criteria and test data read ACE views directly",
                     "§4; §7; §16", f"{st.key} is not owned by rwb-source-data, but {len(hits_ace)} criterion, test or flow "
                     "line(s) set up data in an ACE view or extension table instead of the rwb-source-data contract fake.",
                     "; ".join(hits_ace[:10]) + (" ..." if len(hits_ace) > 10 else "") + ". Template and Rules v1 DP-05; ADR-010.",
                     "Write each Given and test-data line against the rwb-source-data contract fake (§12.8).",
                     area="Source access", token="v_ace_", owner="QA",
                     source="22 Microservice Realignment/Recovery Workbench Microservice Story Template and Rules v1.md (DP-05)",
                     fix={"kind": "rewrite_lines", "lines": hits_ace})
        if hits_leg:
            self.add(st, "X12", "Outdated", "P3", "Criteria and tests keep legacy job and decision-log wording",
                     "§7; §16", f"{st.key} names a workflow in §12.5, but {len(hits_leg)} criterion or test line(s) still say "
                     "JOB-nn, 'decision log' or 'job record'.",
                     "; ".join(hits_leg[:10]) + ". Template and Rules v1 DP-03, DP-10.",
                     "Use the workflow name, the decision record and the run record.", area="Source access",
                     token="JOB-", owner="QA", fix={"kind": "rewrite_lines", "lines": hits_leg},
                     source="22 Microservice Realignment/Recovery Workbench Microservice Story Template and Rules v1.md (DP-03, DP-10)")

    # X16 -----------------------------------------------------------------------------
    def x16(self, st):
        prd = self.src.prd(st.code)
        if not prd:
            return
        defs = defaultdict(list)
        for heading, hdr, rows in md_tables(prd):
            for r in rows:
                if r and re.fullmatch(r"FR-[A-Z0-9]+-\d{3}", r[0]):
                    defs[r[0]].append(r[1] if len(r) > 1 else "")
        cited = sorted(set(re.findall(r"FR-[A-Z0-9]+-\d{3}", st.meta.get("PRD reference", "") + st.section_text("18"))))
        for fr in cited:
            if fr.split("-")[1] != st.code:
                continue
            if fr not in defs:
                self.add(st, "X16", "Missing", "P2", f"{fr} is not in the PRD", "Metadata PRD reference",
                         f"{st.key} cites {fr}; PRD {st.code} has no such functional requirement.",
                         f"PRD {st.code} v1 functional table.", "Cite a PRD requirement.", area="Requirements", token=fr)
        dup = {k: v for k, v in defs.items() if len(set(v)) > 1}
        for fr in cited:
            if fr in dup:
                self.add(st, "X16", "ID collision", "P2", f"{fr} has {len(set(dup[fr]))} meanings in the PRD",
                         "Metadata PRD reference",
                         f"PRD {st.code} defines {fr} more than once: " + " / ".join(x[:120] for x in sorted(set(dup[fr]))),
                         f"PRD {st.code} v1 functional table rows {fr}.", "Renumber the duplicate in the PRD's next version.",
                         owner="Business analyst", area="Requirements", token=fr)
        self.report[st.key]["prd_fr_cited"] = cited

    # X17 -----------------------------------------------------------------------------
    def x17(self, st):
        s15 = st.section_text("15")
        spec = self.src.text("screens")
        for scr in sorted(set(re.findall(r"SCR-\d+", s15))):
            m = re.search(re.escape(scr) + r"[^(]*\(([^)]*)\)", s15)
            states = {x.strip().lower() for x in re.split(r";", m.group(1))} if m else set()
            need = ["empty", "loading", "error", "no access"]
            miss_story = [n for n in need if not any(n in s for s in states)] if m else need
            ms = re.search(r"^## " + re.escape(scr) + r"\b.*?(?=^## |\Z)", spec, re.S | re.M)
            miss_spec = [n for n in need if n not in (ms.group(0).lower() if ms else "")]
            if miss_story:
                self.add(st, "X17", "Missing", "P3", f"{scr} has no {', '.join(miss_story)} state in the story",
                         "§15 Screens and states",
                         f"{st.key} lists the states of {scr} as '{m.group(1) if m else 'none'}'; the v3 rule needs empty, "
                         "loading, error and no access." + (f" Screen Specifications v1 also lacks: {', '.join(miss_spec)}." if miss_spec else ""),
                         f"A) {st.key} §15. B) Screen Specifications v1 section {scr}" + (" (not found)" if not ms else "") + ".",
                         "Add the states from the screen specification; a state the specification lacks is Not specified in the source documents.",
                         owner="Business analyst", area="Screens", token=scr,
                         source="07 Screens and experience/Recovery Workbench Screen Specifications v1.md")

    # X19 -----------------------------------------------------------------------------
    def x19(self, st):
        gaps, asms = self.src.register("gapreg"), self.src.register("asmreg")
        for gid in sorted(set(re.findall(r"\bGAP-\d{4}\b", st.text))):
            if gid not in gaps:
                self.add(st, "X19", "Missing", "P3", f"Cited {gid} is not in the Gap Register v1", "Story text",
                         f"{st.key} cites {gid}; the register has no such row.", "Gap Register v1.",
                         "Cite the register row that exists.", area="Registers", token=gid)
        for aid in sorted(set(re.findall(r"\bASM-\d{4}\b", st.text))):
            if aid not in asms:
                self.add(st, "X19", "Missing", "P3", f"Cited {aid} is not in the Assumptions Register v1", "Story text",
                         f"{st.key} cites {aid}; the register has no such row.", "Assumptions Register v1.",
                         "Cite the register row that exists.", area="Registers", token=aid)
        cited = set(re.findall(r"\bGAP-\d{4}\b", st.text))
        unc = []
        for gid, r in gaps.items():
            if gid in cited or r.get("Status", "Open").strip() != "Open":
                continue
            blob = " ".join(v for k, v in r.items() if k not in ("Raised by",))
            if st.key in blob or (st.legacy and re.search(re.escape(st.legacy) + r"\b", blob)):
                unc.append(f"{gid} {r.get('Title', '')[:100]}")
        self.report[st.key]["uncited_register_gaps"] = unc

    # X20 -----------------------------------------------------------------------------
    def x20(self, st):
        best = self.src.doc_versions()
        old = []
        for name, v in best.items():
            for m in re.finditer(re.escape(name) + r" v(\d+)\b", st.text):
                if int(m.group(1)) < v:
                    old.append((f"{name} v{m.group(1)}", f"{name} v{v}"))
        old = sorted(set(old))
        if old:
            self.add(st, "X20", "Outdated", "P3", "Story cites document versions that are not the highest",
                     "Story text", f"{st.key} cites " + "; ".join(f"{a} (highest {b.rsplit(' ', 1)[1]})" for a, b in old) + ".",
                     "Document Index v14.", "Cite the highest version of each document.", area="Versions",
                     token=old[0][0], fix={"kind": "replace_all", "pairs": old},
                     source="12 Project communication/Recovery Workbench Document Index v14.md")

    # X2 (open decisions only) ------------------------------------------------------
    def x2_open_dl(self, st):
        taken, open_ = self.src.decisions()
        idk = next((k for k in (open_[0].keys() if open_ else []) if k.strip().upper() in ("ID", "DL")), None)
        rows = {}
        for r in open_:
            vals = list(r.values())
            if vals and re.fullmatch(r"DL\d+", vals[0]):
                rows[vals[0]] = r
        asm_reg = self.src.register("asmreg")
        for dl in sorted(set(re.findall(r"\bDL\d+\b", st.text)), key=lambda x: int(x[2:])):
            r = rows.get(dl)
            if not r:
                continue
            vals = list(r.values())
            rec = vals[4] if len(vals) > 4 else ""
            have = [a for a, x in asm_reg.items() if re.search(r"\b" + dl + r"\b", " ".join(x.values()))]
            if not have:
                self.add(st, "X2", "Ambiguous", "P2", f"Open decision {dl} has no assumption", "Story text",
                         f"{st.key} depends on {dl} ('{vals[1] if len(vals) > 1 else ''}'), still open in Decision Log v11, "
                         "and neither register holds an assumption for it.",
                         f"Decision Log v11, Open decisions row {dl}: options '{vals[3] if len(vals) > 3 else ''}', "
                         f"recommendation '{rec}'.",
                         f"Owner rules {dl}; until then build on the recommended option.",
                         owner="Product owner", area="Decisions", token=dl,
                         source="01 Decisions and governance/Recovery Workbench Decision Log v11.xlsx (Open decisions)",
                         asm={"text": f"Built on the recommended option of {dl}: {rec}",
                              "why": f"{dl} is open; the Decision Log names this option as the recommendation.",
                              "confirm": f"{vals[5] if len(vals) > 5 else 'Owner'} rules {dl}", "confidence": "Medium"})
            self.report[st.key].setdefault("open_dl", []).append(f"{dl} (assumptions: {', '.join(have[:4]) or 'none'})")

    def defects(self, st):
        t = self.src.converted("storydefects")
        out = []
        for r in rwbsrc.sheet(t, "Defects"):
            if st.legacy and r.get("Story", "") == st.legacy and r.get("Status", "").lower().startswith("open"):
                out.append(f"step {r.get('Step')}: {r.get('What contradicts what', '')[:160]}")
        self.report[st.key]["open_defects"] = out

    # ---------------------------------------------------------------------------- save
    def save(self, stories, seconds):
        self.out.mkdir(parents=True, exist_ok=True)
        new = [r for r in self.rows if not r.get("related")]
        cited = [r for r in self.rows if r.get("related")]
        with (self.out / "gaps.jsonl").open("w", encoding="utf-8") as f:
            for r in self.rows:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        with (self.out / "assumptions.jsonl").open("w", encoding="utf-8") as f:
            for a in self.asms:
                f.write(json.dumps(a, ensure_ascii=False) + "\n")
        with (self.out / "cited.jsonl").open("w", encoding="utf-8") as f:
            for r in cited:
                f.write(json.dumps({"id": r["id"], "story": r["story"], "related": r["related"], "title": r["title"]},
                                   ensure_ascii=False) + "\n")
        (self.out / "report.json").write_text(json.dumps(
            {"stories": self.report, "unread_sources": self.src.unread, "seconds": seconds}, indent=1, ensure_ascii=False),
            encoding="utf-8")
        by = defaultdict(lambda: defaultdict(int))
        for r in self.rows:
            by[r["story"]][r["check"]] += 1
        lines = [f"# Deterministic check summary ({self.wp})", "",
                 f"Stories: {len(stories)}. Rows: {len(self.rows)} ({len(new)} with no related register row, "
                 f"{len(cited)} with related rows). Assumptions: {len(self.asms)}. Time: {seconds:.1f} s.", "",
                 "| Story | " + " | ".join(CHECKS) + " | Total |", "|---|" + "---|" * (len(CHECKS) + 1)]
        for s in stories:
            c = by.get(s.key, {})
            lines.append(f"| {s.key} | " + " | ".join(str(c.get(x, 0)) for x in CHECKS) + f" | {sum(c.values())} |")
        if self.src.unread:
            lines += ["", "Sources not read: " + "; ".join(self.src.unread)]
        (self.out / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


CHECKS = ["X1", "X2", "X3", "X4", "X5", "X6", "X7", "X8", "X9", "X10", "X11", "X12", "X16", "X17", "X19", "X20"]


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--cache", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--wp", default="DET")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--legacy")
    g.add_argument("--all", action="store_true")
    g.add_argument("--story", nargs="+")
    g.add_argument("--story-list", help="a text file with one story path per line (for long lists)")
    ap.add_argument("--start", type=int, default=101)
    ap.add_argument("--jobs", type=int, default=1, help="worker processes; output is the same as --jobs 1")
    ap.add_argument("--source", action="append", default=[], metavar="KEY=PATH",
                    help="read a source from another path, e.g. tc=<sandbox>/Test Cases v9.xlsx (re-check a fixed set)")
    a = ap.parse_args(argv)
    overrides = dict(s.split("=", 1) for s in a.source)
    for k, v in overrides.items():
        if k not in rwbsrc.SOURCES:
            sys.exit(f"--source: unknown key {k}; known: {', '.join(sorted(rwbsrc.SOURCES))}")
        rwbsrc.SOURCES[k] = v  # an absolute path: ROOT / abs == abs
    root = Path(a.root).resolve()
    out = Path(a.out).resolve()
    if out == root or root in out.parents:
        sys.exit("--out must be outside ROOT (sandbox only)")
    src = Sources(root, a.cache)
    if a.story_list:
        a.story = [l.strip() for l in Path(a.story_list).read_text(encoding="utf-8").splitlines() if l.strip()]
    if a.story:
        paths = [Path(p) for p in a.story]
    else:
        base = root / rwbsrc.TEXT["stories"]
        paths = sorted(p for p in base.rglob("*.md") if rwbsrc.story_key_from_name(p.name))
        if a.legacy:
            tag = a.legacy.replace("RWB-", "").replace("-", "")  # RWB-E1-018 -> E1018
            paths = [p for p in paths if f" {tag} " in p.name]
    t0 = time.time()
    ck = Checker(src, a.wp, out)
    ck.n = a.start - 1
    stories = []
    jobs = max(1, min(a.jobs, len(paths)))
    if jobs == 1:
        for p in paths:
            st = Story(p)
            stories.append(st)
            ck.run(st)
    else:
        stories = run_parallel(ck, root, a.cache, a.wp, paths, jobs, overrides)
    ck.save(stories, time.time() - t0)
    print(f"{len(stories)} stories, {len(ck.rows)} rows, {len(ck.asms)} assumptions, {time.time() - t0:.1f} s -> {out}")


def _check_chunk(job):
    """Worker: check one contiguous slice of stories with its own source cache (read-only)."""
    root, cache, wp, paths, overrides = job
    rwbsrc.SOURCES.update(overrides)  # a worker process starts from the module defaults
    ck = Checker(Sources(root, cache), wp, ".")
    keys = []
    for p in paths:
        st = Story(Path(p))
        keys.append(st.key)
        ck.run(st)
    return ck.rows, ck.asms, ck.report, ck.src.unread, keys


def run_parallel(ck, root, cache, wp, paths, jobs, overrides=None):
    """Split the stories into `jobs` contiguous slices, check them in parallel and merge in story order.
    Row IDs are renumbered in order, the assumption IDs follow their rows, and a run-level row
    (wp_level) is kept once, so the result matches a serial run."""
    from concurrent.futures import ProcessPoolExecutor
    from types import SimpleNamespace
    size = -(-len(paths) // jobs)
    chunks = [[str(p) for p in paths[i:i + size]] for i in range(0, len(paths), size)]
    with ProcessPoolExecutor(max_workers=len(chunks)) as ex:
        parts = list(ex.map(_check_chunk, [(str(root), str(cache), wp, c, dict(overrides or {})) for c in chunks]))
    stories, seen_wl = [], set()
    for rows, asms, report, unread, keys in parts:
        idmap = {}
        for r in rows:
            if r.get("wp_level"):
                if r["wp_level"] in seen_wl:
                    continue
                seen_wl.add(r["wp_level"])
            ck.n += 1
            new = f"CG-{wp}-{ck.n}"
            idmap[r["id"]] = new
            r["id"] = new
            ck.rows.append(r)
        for a in asms:
            if a["gap"] not in idmap:
                continue
            a["gap"] = idmap[a["gap"]]
            a["id"] = a["gap"].replace("CG-", "ASM-")
            ck.asms.append(a)
        for r in ck.rows[-len(idmap):] if idmap else []:
            if r.get("asm"):
                r["asm"] = r["id"].replace("CG-", "ASM-")
        for k, v in report.items():
            if k in ck.report:  # two files with one key: merge as the serial run does
                for f, val in v.items():
                    if isinstance(val, list):
                        ck.report[k].setdefault(f, []).extend(val)
                    elif f not in ck.report[k]:
                        ck.report[k][f] = val
            else:
                ck.report[k] = v
        for u in unread:
            if u not in ck.src.unread:
                ck.src.unread.append(u)
        stories += [SimpleNamespace(key=k) for k in keys]
    return stories


class Sources(rwbsrc.Sources):
    """Adds the corpus, PRD and prior-row views used by X4, X7, X16 and de-duplication."""

    def corpus(self, exclude_stories=False):
        k = "_corpus" + ("x" if exclude_stories else "")
        if k in self._t:
            return self._t[k]
        docs = {}
        for key in ("refdata", "ldm", "rules", "casemodel", "tc", "rtm", "declog", "temporal", "kafka", "msgstd"):
            docs[rwbsrc.SOURCES[key]] = self.converted(key)
        for key in ("gapreg", "asmreg", "screens"):
            docs[rwbsrc.TEXT[key]] = self.text(key)
        for p in (self.root / rwbsrc.TEXT["prddir"]).glob("*.md"):
            docs[str(p)] = p.read_text(encoding="utf-8", errors="replace")
        for p in (self.root / "05 Technical architecture").glob("*.md"):
            docs[str(p)] = p.read_text(encoding="utf-8", errors="replace")
        if not exclude_stories:
            pass  # sibling stories are compared by the model check X18, not here
        self._t[k] = docs
        return docs

    def prd(self, code):
        for p in (self.root / rwbsrc.TEXT["prddir"]).glob(f"Recovery Workbench PRD {code} *.md"):
            return p.read_text(encoding="utf-8", errors="replace")
        return ""

    def prior_rows(self):
        if "_prior" not in self._t:
            rows = []
            for p in (self.root / "_work/msr/gaps").glob("*.jsonl"):
                for l in p.read_text(encoding="utf-8", errors="replace").splitlines():
                    try:
                        rows.append(json.loads(l))
                    except ValueError:
                        pass
            self._t["_prior"] = rows
        return self._t["_prior"]


rwbsrc.SOURCES["storydefects"] = "04 User stories/Recovery Workbench Story Defects Epic 1 Epic 2 and Enablers v5.xlsx"

if __name__ == "__main__":
    main()
