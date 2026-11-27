"""Script build-readiness review per story: the Definition of Ready checklist, AC review and missing ACs
(sandbox prototype, D-RCV-60).

Covers the structural part of a reviewer's report for every story, from the story text and the source
documents only:
  R1 verdict; R2 the 25 items of Definition of Ready and Done v4 section 2 (Pass, Partial, Fail, or Pass (not applicable)),
  each with its evidence and, when --det is given, the detcheck rows (X1-X20) that fall under the item;
  R3 the detcheck gap list of the story; R4 AC review (structural problems per owned criterion);
  R5 missing acceptance criteria (which path or case has no criterion; the Gherkin itself is model work).
What it cannot judge (is a criterion right, a rule's meaning, NFR behaviour, wording) is listed in R7.

Usage: python -I dorcheck.py --root <ROOT> --cache <dir> --out <dir> (--all | --legacy RWB-E1-018 |
       --story-list <file>) [--det <detcheck out dir>] [--jobs 8]
Writes only under --out: review/<story>.md (the format `rulings.py capture --review <out>` reads),
dor.jsonl (one row per story and item), summary.md.
"""
import argparse, json, re, sys, time
from collections import Counter, OrderedDict, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import rwbsrc  # noqa: E402
from detcheck import Story, Sources  # noqa: E402

TOOL = "T3 Code / OpenCode / DeepSeek v4.1 Flash"
DOR_DOC = "Recovery Workbench Definition of Ready and Done v4 section 2"
ROLES_SRC = "02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx"
rwbsrc.SOURCES.setdefault("roles", ROLES_SRC)

ITEMS = OrderedDict([
    (1, "Story"), (2, "Links"), (3, "Acceptance criteria"), (4, "Business rules"), (5, "State transitions"),
    (6, "Authority"), (7, "Data"), (8, "Contract"), (9, "Messages"), (10, "Screens and states"),
    (11, "Guardrails"), (12, "Test cases"), (13, "Out of scope"), (14, "Epic design"), (15, "INVEST"),
    (16, "Size"), (17, "Dependencies"), (18, "Open decisions"), (19, "Test data"), (20, "Reference data"),
    (21, "Contract published"), (22, "Fake published"), (23, "Contract version fixed"),
    (24, "Ownership stated"), (25, "Ready to start")])
# detcheck check -> DoR item (X5 dependency rows go to item 17, see det_item)
X_ITEM = {"X1": 5, "X2": 18, "X3": 7, "X4": 20, "X5": 8, "X6": 8, "X7": 4, "X8": 9, "X9": 12, "X10": 11,
          "X12": 7, "X16": 2, "X17": 10}
RECORD_ITEMS = {14, 16, 21, 22, 23}  # epic design sign-off, size, contract and fake published, contract version
KEYRE = re.compile(r"RWB-[A-Z0-9]+-[A-Z0-9]+-[A-Z]+(?:-\d+)?")
NONE_RE = re.compile(r"^\s*(none|n/?a|not applicable|-|—|–)?\s*\.?\s*$", re.I)


def det_item(r):
    if r.get("check") == "X5" and "dependency" in r.get("title", "").lower():
        return 17
    return X_ITEM.get(r.get("check"))


def rows_of(st, n):
    """Dicts of every table in section or subsection n."""
    return [d for t in st.table_dicts(n) for d in t]


def col(d, *names):
    for k, v in d.items():
        if any(n.lower() in k.lower() for n in names):
            return v
    return ""


def body(st, n):
    """Section text without its heading line."""
    return "\n".join(st.section_text(n).splitlines()[1:]).strip()


class Review:
    def __init__(self, st, src, det_rows, report, story_index, roles):
        self.st, self.src, self.det = st, src, det_rows
        self.report = report or {}
        self.idx, self.roles = story_index, roles
        self.items = OrderedDict((n, {"no": n, "item": name, "problems": [], "gaps": [], "result": None,
                                      "evidence": []}) for n, name in ITEMS.items())
        self.acr = OrderedDict()   # AC -> problems
        self.missing = []          # (covers, why)
        self.text = st.text
        self.ac_text = st.section_text("7")
        self.owned = st.owned_acs()
        self.scen = st.scenarios()

    # helpers
    def p(self, n, sev, msg):
        self.items[n]["problems"].append((sev, msg))

    def ev(self, n, msg):
        self.items[n]["evidence"].append(msg)

    def fixed(self, n, result, msg):
        self.items[n]["result"] = result
        self.items[n]["evidence"].append(msg)

    def ac_has(self, *words):
        t = self.ac_text.lower()
        return any(w.lower() in t for w in words)

    # ------------------------------------------------------------------ items
    def i1(self):
        t = body(self.st, "1")
        m = re.search(r"As an?\s+\*{0,2}(.+?)\*{0,2},?\s+I want\b.*?\bso that\b", t, re.S | re.I)
        if not m:
            self.p(1, "P1", "§1 is not in the form 'As a <role>, I want ..., so that ...'")
            return
        role = m.group(1).strip(" *")
        codes, names = self.roles
        inner = re.findall(r"\b(?:RW|SY|PT|CU)-[A-Z0-9-]*[A-Z0-9]\b", role)
        bare = re.sub(r"\s*\(.*?\)", "", role).strip()
        if role in codes or bare.lower() in names or (inner and all(c in codes for c in inner)):
            self.ev(1, f"§1 role '{role}' is in the roles table")
        else:  # delivery roles (tech lead, platform engineer) are not system roles
            sev = "P2" if self.st.worktype == "APP" else "P3"
            self.p(1, sev, f"§1 role '{role}' is not a role code or role name in Users Roles and Permissions v5")

    def i2(self):
        for k in ("Service", "Service epic", "Legacy key", "PRD reference"):
            v = self.st.meta.get(k, "")
            if not v or NONE_RE.match(v):
                self.p(2, "P2", f"header '{k}' is empty")
        tr = rows_of(self.st, "18")
        if not tr:
            self.p(2, "P2", "§18 has no traceability row")
        else:
            hdr = " ".join(tr[0]).lower()
            for colname, what in (("feature", "feature"), ("l3", "L3 process")):
                if colname not in hdr:
                    if self.st.worktype == "APP":
                        self.p(2, "P3", f"§18 has no {what} column")
                elif not any(col(r, colname) and not NONE_RE.match(col(r, colname)) for r in tr):
                    self.p(2, "P3", f"§18 names no {what}")
            self.ev(2, f"§18 has {len(tr)} traceability rows")

    def owned_elsewhere(self):
        t = re.sub(r"```.*?```", "", self.ac_text, flags=re.S)
        out = set()
        for para in t.split("\n\n"):
            if re.search(r"owned by|carried by|in the (integration|contract|deployment) story", para, re.I):
                out.update(re.findall(r"\bAC\d+\b", para))
        return out

    def i3(self):
        if not self.scen:
            self.p(3, "P1", "§7 has no Gherkin scenario with an AC ID")
            return
        ids = re.findall(r"Scenario(?: Outline)?:\s*(AC[\w-]+)", self.ac_text)
        for d, c in Counter(ids).items():
            if c > 1:
                self.p(3, "P2", f"{d} is used by {c} scenarios")
        for ac, lines in self.scen.items():
            kw = {l.split()[0] for l in lines if l.split()}
            if "Then" not in kw:
                self.p(3, "P1", f"{ac} has no Then")
                self.acr.setdefault(ac, []).append("no Then: the criterion asserts nothing")
            if "When" not in kw:
                self.p(3, "P2", f"{ac} has no When")
                self.acr.setdefault(ac, []).append("no When: the trigger is not stated")
        self.ev(3, f"§7 holds {len(self.scen)} owned criteria in Gherkin")
        elsewhere = self.owned_elsewhere()
        ex = rows_of(self.st, "5")
        if not ex and not NONE_RE.match(body(self.st, "5").split("\n")[0] if body(self.st, "5") else ""):
            self.p(3, "P2", "§5 lists no exception path")
        if ex and not any("covered" in k.lower() for k in ex[0]):
            self.p(3, "P2", "§5 has no 'Covered by' column, so no exception path is tied to a criterion")
            ex = []
        for r in ex:
            xid, cov = col(r, "ID") or "?", col(r, "Covered")
            acs = re.findall(r"\bAC\d+\b", cov)
            if not acs and cov.strip() and not NONE_RE.match(cov):
                self.p(3, "P2", f"exception {xid} is covered by '{cov[:60]}', not by a criterion")
                self.missing.append((f"§5 {xid}: {col(r, 'Trigger')[:120]}", f"covered by '{cov[:60]}' only"))
                continue
            if not acs:
                self.p(3, "P1", f"exception {xid} has no criterion ('{cov or 'empty'}')")
                self.missing.append((f"§5 {xid}: {col(r, 'Trigger')[:120]}", "the exception path has no criterion"))
                continue
            gone = [a for a in acs if a not in self.scen and a not in elsewhere]
            if gone:
                self.p(3, "P2", f"exception {xid} is covered by {', '.join(gone)}, which this story neither owns "
                                f"nor names as owned by another story")
                self.missing.append((f"§5 {xid}: {col(r, 'Trigger')[:120]}",
                                     f"covered by {', '.join(gone)}, which exist nowhere in this story"))
        if ex:
            self.ev(3, f"§5 has {len(ex)} exception paths")

    def i4(self):
        brs = rows_of(self.st, "8")
        if not brs:
            if not NONE_RE.match(body(self.st, "8")[:40] or ""):
                self.ev(4, "§8 has no rule table")
            return
        ids = [col(r, "ID") for r in brs]
        for d, c in Counter(ids).items():
            if d and c > 1:
                self.p(4, "P2", f"rule ID {d} is used {c} times")
        covered = " ".join(col(r, "Covers") for r in rows_of(self.st, "16")) + " " + self.ac_text
        bare = []
        for r in brs:
            i = col(r, "ID")
            if not re.match(r"BR\d+", i or ""):
                self.p(4, "P3", f"rule row '{(i or col(r, 'Rule'))[:40]}' has no BR ID")
                continue
            if not col(r, "Source").strip() or NONE_RE.match(col(r, "Source")):
                self.p(4, "P2", f"{i} names no source")
            if not re.search(rf"\b{i}\b", covered):
                bare.append(i)
        if bare:
            self.p(4, "P2", f"{len(bare)} of {len(brs)} rules are covered by no criterion and no test case: "
                            f"{', '.join(bare)}")
            self.missing.append((f"§8 {', '.join(bare)}", "these rules have no criterion and no test; a rule that "
                                 "is an architecture constraint may belong in a guardrail or boundary test instead"))
        self.ev(4, f"§8 has {len(brs)} rules")

    def i5(self):
        tr = rows_of(self.st, "9")
        if not tr:
            self.ev(5, "§9 has no transition (no status change in this story)")
            return
        status, trans = self.src.case_model()
        labels = {col(r, "Status").strip().lower() for r in status if col(r, "Status")}
        labels |= {c.lower() for c, _ in self.src.lov()[1].get("LOV-CASE-STATUS", [])}
        labels |= {l.lower() for _, l in self.src.lov()[1].get("LOV-CASE-STATUS", [])}
        pairs = set()
        for r in trans:
            fr, to = col(r, "From"), col(r, "To")
            for f in re.split(r",\s*|\s+or\s+", fr):
                pairs.add((f.strip().lower(), to.strip().lower()))
        for r in tr:
            fr, to = col(r, "From").strip(), col(r, "To").strip()
            if fr.lower() in labels and to.lower() in labels and (fr.lower(), to.lower()) not in pairs \
                    and not any(a == fr.lower() and b.startswith("the status") for a, b in pairs):
                self.p(5, "P1", f"§9 move {fr} -> {to} is not a row of Case and Workflow Model v6 (Status transitions)")
        self.ev(5, f"§9 has {len(tr)} transitions")

    def i6(self):
        ar = rows_of(self.st, "10")
        if not ar:
            self.p(6, "P1", "§10 names no role")
            return
        codes, _ = self.roles
        sec = st_text = self.st.section_text("10")
        for c in sorted(set(re.findall(r"\b(?:RW|SY|PT|CU)-[A-Z0-9-]*[A-Z0-9]\b", sec))):
            if codes and c not in codes:
                self.p(6, "P2", f"role {c} in §10 is not in Users Roles and Permissions v5")
        provides = rows_of(self.st, "12.1")
        if provides and self.st.service != "rwb-access" and "authorise" not in self.text.lower():
            self.p(6, "P2", "the story provides REST operations and names no rwb-access authorise check (DP-08)")
        self.ev(6, f"§10 has {len(ar)} roles")

    def i7(self):
        dr = rows_of(self.st, "11")
        if not dr:
            self.p(7, "P2", "§11 has no data table")
            return
        known = {col(r, "BR Field ID") for r in self.src.ldm_fields()}
        bad, nofield = [], 0
        for r in dr:
            f = col(r, "Field ID")
            if not f.strip() or NONE_RE.match(f):
                nofield += 1
                continue
            for m in re.findall(r"DF-[A-Z]+-\d{3}", f):
                if known and m not in known:
                    bad.append(m)
        if nofield:
            self.p(7, "P2", f"{nofield} row(s) of §11 have no BR Field ID")
        if bad:
            self.p(7, "P2", f"BR Field IDs not in LDM v9: {', '.join(sorted(set(bad))[:12])}")
        self.ev(7, f"§11 has {len(dr)} data rows")

    def i8(self):
        if not body(self.st, "4"):
            self.p(8, "P1", "§4 has no flow, so the trigger is not stated")
        for r in rows_of(self.st, "12.1"):
            m = col(r, "Method").upper()
            if m in ("POST", "PUT", "PATCH", "DELETE"):
                idem = col(r, "Idempotency")
                if not idem or NONE_RE.match(idem):
                    self.p(8, "P2", f"{m} {col(r, 'Path')} has no idempotency key")
        for r in rows_of(self.st, "12.3"):
            if any(k.lower() == "key" for k in r) and col(r, "Event").strip() and not col(r, "Key").strip():
                self.p(8, "P2", f"event {col(r, 'Event')} has no key")
        if self.st.sub:
            have = set(self.st.sub)
            missing = [s for s in (f"12.{i}" for i in range(1, 10)) if s not in have]
            if missing:
                self.p(8, "P3", f"§12 lacks subsections {', '.join(missing)}")
        elif not body(self.st, "12"):
            self.p(8, "P1", "§12 is empty")

    def i9(self):
        msgs = rows_of(self.st, "14")
        ids = set()
        for r in msgs:
            i = col(r, "ID")
            ids.update(re.findall(r"MSG-[A-Z0-9]+-\d+", i))
            if not col(r, "Message").strip():
                self.p(9, "P2", f"{i} has no English text in §14")
        used = set(re.findall(r"MSG-[A-Z0-9]+-\d+", "\n".join(self.st.section_text(n) for n in ("5", "7", "10", "12"))))
        miss = sorted(used - ids)
        if miss:
            self.p(9, "P2", f"messages used but not listed in §14: {', '.join(miss)}")
        for n in ("12.3", "12.4"):
            for r in rows_of(self.st, n):
                e = col(r, "Event").strip("` ")
                name = re.split(r"[`\s(]", e)[0] if e else ""
                if "." in name and not re.fullmatch(r"rwb\.[a-z0-9-]+\.[A-Z][A-Za-z0-9]+\.v\d+", name):
                    self.p(9, "P3", f"event name '{name}' does not follow rwb.<short>.<Event>.v1 (DP-14)")
        self.ev(9, f"§14 lists {len(ids)} messages")

    def i10(self):
        t = body(self.st, "15")
        if not t:
            self.p(10, "P2", "§15 is empty")
        elif not re.search(r"SCR-\d+", t) and not re.search(r"no screen|none|not applicable|no user interface", t, re.I):
            self.p(10, "P2", "§15 names no screen and does not say there is none")

    def i11(self):
        t = body(self.st, "17")
        if not re.search(r"^\s*[-*]\s+\S", t, re.M):
            self.p(11, "P1", "§17 lists no guardrail")
        elif "personal data" not in t.lower():
            self.p(11, "P2", "§17 does not state the personal data rule")

    def i12_19(self):
        tcs = rows_of(self.st, "16")
        if not tcs:
            self.p(12, "P1", "§16 has no test case")
            self.p(19, "P2", "§16 has no test data")
            return
        cov = " ".join(col(r, "Covers") for r in tcs)
        for ac in self.scen:
            if not re.search(rf"\b{re.escape(ac)}\b", cov):
                self.p(12, "P1", f"{ac} has no test case in §16")
                self.acr.setdefault(ac, []).append("no test case in §16")
        levels = " ".join(col(r, "Level") for r in tcs).lower()
        if (rows_of(self.st, "12.1") or rows_of(self.st, "12.3") or rows_of(self.st, "12.5")) and "contract" not in levels:
            self.p(12, "P2", "no contract test for the operations, events and activities of §12")
        if rows_of(self.st, "12.7") and "boundary" not in levels:
            self.p(12, "P2", "no boundary test for the tables of §12.7 (ASM-3438)")
        nodata = [col(r, "TC") or "?" for r in tcs if not col(r, "Data").strip()]
        if nodata:
            self.p(19, "P2", f"test cases with no data: {', '.join(nodata[:10])}")
        else:
            self.ev(19, f"every test case in §16 names its data ({len(tcs)})")
        self.ev(12, f"§16 has {len(tcs)} test cases")

    def i13(self):
        if not body(self.st, "19"):
            self.p(13, "P2", "§19 is empty")

    def i14(self):
        self.fixed(14, "Fail", "no signed epic design is recorded in the story or the source documents; confirm "
                               "the sign-off with the epic design record")

    def i15(self):
        rows = rows_of(self.st, "6")
        tests = {col(r, "Test").strip().lower(): col(r, "Result") for r in rows}
        for t in ("independent", "negotiable", "valuable", "estimable", "small", "testable"):
            if not tests.get(t, "").strip():
                self.p(15, "P2", f"INVEST '{t}' has no result in §6")
        small = tests.get("small", "")
        if small and not re.search(r"two weeks|2 weeks|one sprint|a sprint", small, re.I):
            self.p(15, "P3", "INVEST 'Small' does not say it fits two weeks")

    def i16(self):
        v = next((self.st.meta[k] for k in self.st.meta if k.lower() in ("size", "story points", "estimate")), "")
        if v and not NONE_RE.match(v):
            self.ev(16, f"sized: {v}")
        else:
            self.fixed(16, "Fail", "the story carries no size; the squad sizes it at refinement")

    def i17(self):
        keys = []
        for k in ("Depends on (build)", "Contract dependencies", "Integration dependencies", "External dependencies"):
            keys += KEYRE.findall(self.st.meta.get(k, ""))
        missing = sorted({k for k in keys if k not in self.idx})
        if missing:
            self.p(17, "P1", f"dependencies that are not story files: {', '.join(missing[:10])}")
        notdone = []
        for k in sorted(set(keys) - set(missing)):
            bs = self.idx[k][1]
            if bs and not re.match(r"done", bs, re.I) and not k.endswith("-CON"):
                notdone.append(k)
        if notdone:
            self.p(17, "P3", f"{len(notdone)} build dependencies are not done yet ({', '.join(notdone[:6])})")
        self.ev(17, f"{len(set(keys))} dependencies named")

    def i18(self):
        for d in self.report.get("open_dl", []):
            self.ev(18, f"open decision {d}")
        if self.report.get("open_dl"):
            if not any(r.get("check") == "X2" for r in self.det):
                self.p(18, "P3", "open decisions apply; each has an assumption, the decision is still open")

    def i20(self):
        reads = re.findall(r"LOV-[A-Z0-9-]+|`[a-z]+(?:\.[a-z_]+){1,}`", self.text)
        if reads and self.st.service != "rwb-case":
            if not re.search(r"E1042-CON|E1043-CON|parameters contract|reference-data contract", self.text):
                self.p(20, "P2", "reads lists or parameters and names neither the parameters nor the "
                                 "reference-data contract (DP-06, DP-07)")

    def i21_23(self):
        wt = self.st.worktype
        if wt == "CON":
            self.fixed(21, "Pass (not applicable)", "this is the contract story")
            self.fixed(22, "Pass (not applicable)", "this is the contract story; it publishes the fakes")
        else:
            k = self.st.key
            con = re.sub(r"-(APP|OPS|ITG|DB|INF)(-\d+)?$", "-CON", k)
            if con in self.idx:
                bs = self.idx[con][1] or "not stated"
                if re.match(r"done", bs, re.I):
                    self.ev(21, f"{con} is Done")
                else:
                    self.fixed(21, "Fail", f"the contract story {con} exists; its build status is '{bs}', not Done")
            elif any(x.endswith("-CON") for x in KEYRE.findall(self.st.meta.get("Depends on (build)", ""))):
                self.fixed(21, "Fail", "no contract story of this legacy key; the CON stories it depends on are "
                                       "not Done")
            else:
                self.fixed(21, "Fail", f"no contract story {con} and no CON dependency")
            fakes = self.st.section_text("12.8")
            others = {m for r in rows_of(self.st, "12.2") for m in re.findall(r"rwb-[a-z-]*[a-z]", col(r, "Service", "Owner"))}
            lacking = sorted(s for s in others if s not in fakes and s != self.st.service)
            if lacking:
                self.p(22, "P2", f"no contract fake named in §12.8 for {', '.join(lacking)}")
            self.fixed(22, "Fail", "no contract fake library version is recorded as published")
        t = self.st.section_text("3") + self.st.section_text("12")
        if not re.search(r"(contract|OpenAPI|AsyncAPI|schema|jar)[^.\n]{0,60}\b(v\d+\.\d+[\w.]*|version \d[\w.]*)", t, re.I):
            self.fixed(23, "Fail", "the story states no contract version it builds against (only the /v1 path)")

    def i24(self):
        names = ("Owner", "Service", "Producer", "Publisher", "Provider")
        # §12.3 lists what this story's own service publishes, so its owner is stated by the story itself
        for n, what in (("12.7", "table"), ("12.4", "event"), ("12.2", "consumed operation")):
            rows = [r for r in rows_of(self.st, n) if not NONE_RE.match(next(iter(r.values()), "") or "")]
            if rows and not any(x.lower() in k.lower() for k in rows[0] for x in names):
                self.p(24, "P2", f"§{n} has no owner or service column")
                continue
            empty = [r for r in rows if not col(r, *names).strip()]
            if empty:
                self.p(24, "P2", f"{len(empty)} {what} row(s) in §{n} name no owner")
        if re.search(r"rwb_[a-z_]+", self.text):
            own = f"rwb_{self.st.service.replace('rwb-', '').replace('-', '_')}" if self.st.service else ""
            others = sorted(set(re.findall(r"\brwb_[a-z_]+\b", self.st.section_text("13"))) - {own})
            others = [o for o in others if not o.startswith(own) and o not in ("rwb_recovery",)]
            if others and own:
                self.p(24, "P3", f"§13 names other schemas: {', '.join(others[:6])}")

    def i25(self):
        rs = self.st.meta.get("Ready to start", "").strip()
        deps = KEYRE.findall(self.st.meta.get("Depends on (build)", ""))
        if not rs:
            self.p(25, "P2", "header 'Ready to start' is empty")
            return
        if self.st.worktype == "CON" and not rs.lower().startswith("day 1"):
            self.p(25, "P2", f"a contract story is always Day 1; it says '{rs}'")
        if rs.lower().startswith("day 1") and any(not d.endswith("-CON") for d in deps):
            self.p(25, "P2", "Day 1 while it depends on non-contract stories")
        if rs.lower().startswith("after"):
            for k in KEYRE.findall(rs):
                if k not in self.idx:
                    self.p(25, "P1", f"Ready to start waits for {k}, which is not a story file")
                elif k not in deps:
                    self.p(25, "P3", f"Ready to start waits for {k}, which is not in 'Depends on (build)'")
        self.ev(25, f"Ready to start: {rs}")

    # ------------------------------------------------------------------ AC review and missing ACs
    def ac_review(self):
        listed = {i for r in rows_of(self.st, "14") for i in re.findall(r"MSG-[A-Z0-9]+-\d+", col(r, "ID"))}
        for ac, lines in self.scen.items():
            t = "\n".join(lines)
            if self.st.code != "P1" and re.search(r"\bv_ace_\w+", " ".join(l for l in lines if l.startswith("Given"))):
                self.acr.setdefault(ac, []).append("the Given reads an ACE view; this service reads source data "
                                                   "through the rwb-source-data contract (DP-01, DP-05)")
            miss = sorted(set(re.findall(r"MSG-[A-Z0-9]+-\d+", t)) - listed)
            if miss:
                self.acr.setdefault(ac, []).append(f"message {', '.join(miss)} is not in §14")
            if re.search(r"\b(should|may|might|appropriate|correctly|properly|as expected)\b", t, re.I):
                self.acr.setdefault(ac, []).append("vague wording in the steps (should, may, correctly, "
                                                   "as expected); the Then must name a value")

    def gaps_by_type(self):
        t = self.ac_text.lower()
        prov = rows_of(self.st, "12.1")
        if prov:
            need = [c for c in ("401", "403", "404") if c not in t]
            if need:
                self.missing.append((f"error answers {', '.join(need)} of the provided operations",
                                     "no criterion names these status codes"))
            if any(col(r, "Method").upper() in ("POST", "PUT", "PATCH") for r in prov) and \
                    not self.ac_has("idempotency", "replay", "same key", "sent again", "submitted again", "twice"):
                self.missing.append(("replay of a write with the same idempotency key", "no criterion covers a replay"))
        if rows_of(self.st, "12.4") and not self.ac_has("redeliver", "twice", "again", "duplicate", "inbox"):
            self.missing.append(("duplicate delivery of a consumed event", "no criterion covers a redelivered event"))
        if rows_of(self.st, "12.5") and not self.ac_has("retry", "retried", "timeout", "timed out", "time out"):
            self.missing.append(("activity retry and timeout", "no criterion covers a retried or timed-out activity"))
        if rows_of(self.st, "12.2") and not self.ac_has("does not answer", "timeout", "time out", "unavailable",
                                                         "503", "not reachable", "unreachable"):
            self.missing.append(("a consumed call fails or does not answer", "no criterion covers a failed call"))
        if rows_of(self.st, "9") and not self.ac_has("refused", "not allowed", "cannot move", "rejected", "is refused"):
            self.missing.append(("a status change the model does not allow is refused",
                                 "no criterion covers a disallowed transition"))

    # ------------------------------------------------------------------ run
    def run(self):
        for fn in (self.i1, self.i2, self.i3, self.i4, self.i5, self.i6, self.i7, self.i8, self.i9, self.i10,
                   self.i11, self.i12_19, self.i13, self.i14, self.i15, self.i16, self.i17, self.i18, self.i20,
                   self.i21_23, self.i24, self.i25, self.ac_review, self.gaps_by_type):
            try:
                fn()
            except Exception as e:  # a failing check never stops the run (AGENTS.md rule 13)
                self.items[1]["evidence"].append(f"check {fn.__name__} failed: {type(e).__name__}: {e}")
        for r in self.det:
            n = det_item(r)
            if n:
                self.items[n]["gaps"].append(r)
        for it in self.items.values():
            if it["result"]:
                continue
            sev = [s for s, _ in it["problems"]] + [r.get("severity", "P3") for r in it["gaps"]]
            it["result"] = "Fail" if "P1" in sev else "Partial" if sev else "Pass"
        res = [it["result"] for it in self.items.values()]
        p1 = sum(1 for r in self.det if r.get("severity") == "P1")
        self.verdict = ("NOT READY" if "Fail" in res or p1 else "READY WITH GAPS" if "Partial" in res or self.det
                        else "READY")
        # the same rule on the story text alone: items that need records the story files do not hold are left out
        tres = [it["result"] for it in self.items.values() if it["no"] not in RECORD_ITEMS]
        self.text_verdict = ("NOT READY" if "Fail" in tres or p1 else "READY WITH GAPS" if "Partial" in tres
                             or self.det else "READY")
        return self

    # ------------------------------------------------------------------ output
    def md(self):
        st, esc = self.st, (lambda s: str(s).replace("|", "\\|").replace("\n", " "))
        res = Counter(it["result"] for it in self.items.values())
        blk = sorted(r["id"] for r in self.det if r.get("severity") == "P1")
        fails = [f"{it['no']} {it['item']}" for it in self.items.values() if it["result"] == "Fail"]
        L = [f"# Build-readiness review (script) — {st.key} {st.title}", "",
             "SCB Collections and Recovery. Henka Group.", "", f"Tool: {TOOL}. Decision D-RCV-60.", "",
             "| Item | Value |", "|---|---|", f"| Story reviewed | {st.key} ({esc(st.path.name)}) |",
             f"| Review kind | Script checks only: {DOR_DOC}, AC structure, missing-criterion types, detcheck X1-X20 |",
             f"| Service | {esc(st.service)} |", f"| Legacy key | {esc(st.legacy)} |", "",
             "## R1. Verdict", "", f"**{self.verdict}.** Checklist: " +
             ", ".join(f"{k} {res[k]}" for k in ("Pass", "Pass (not applicable)", "Partial", "Fail") if res[k])
             + f". Detcheck rows: {len(self.det)} ({len(blk)} P1). AC review rows: {len(self.acr)}. "
               f"Missing criteria: {len(self.missing)}.", "",
             f"On the story text alone (items {', '.join(map(str, sorted(RECORD_ITEMS)))} left out, they need "
             f"records the story files do not hold): **{self.text_verdict}**.", ""]
        if fails:
            L += ["Failed items: " + "; ".join(fails) + ".", ""]
        L += [f"## R2. Definition of ready — every item of {DOR_DOC}", "",
              "| # | Item | Result | Evidence (story section + document checked) | Gap |", "|---|---|---|---|---|"]
        for it in self.items.values():
            titles = list(OrderedDict.fromkeys(f"{r.get('severity', '')} {r.get('title', '')}" for r in it["gaps"]))
            det_ev = [f"detcheck: {'; '.join(titles[:4])}" + (f" (+{len(titles) - 4} more)" if len(titles) > 4 else "")] if titles else []
            evd = "; ".join([m for _, m in it["problems"]] + it["evidence"] + det_ev) or "—"
            gp = ", ".join(r["id"] for r in it["gaps"][:12]) + (f" (+{len(it['gaps']) - 12})" if len(it["gaps"]) > 12 else "")
            L.append(f"| {it['no']} | {it['item']} | {it['result']} | {esc(evd)} | {gp or '—'} |")
        L += ["", "## R3. Gap list (detcheck rows of this story)", ""]
        for sev, name in (("P1", "Blockers (P1)"), ("P2", "Major (P2)"), ("P3", "Minor (P3)")):
            rows = [r for r in self.det if r.get("severity") == sev]
            L += [f"### R3.{sev[1]} {name} — {len(rows)} rows", "", "| CG id | Title | Check | Gap type | Owner role |",
                  "|---|---|---|---|---|"]
            L += [f"| {r['id']} | {esc(r.get('title', ''))} | {r.get('check', '')} | {r.get('type', '')} | "
                  f"{r.get('owner_role', '')} |" for r in rows]
            L.append("")
        L += ["## R4. AC review — structural problems of the owned criteria", "",
              "| AC | Problem | Improved Given / When / Then (model pass) |", "|---|---|---|"]
        L += [f"| {ac} | {esc('; '.join(ps))} |  |" for ac, ps in self.acr.items()]
        start = max([int(x) for x in re.findall(r"\bAC(\d+)\b", self.text)] or [0]) + 1
        L += ["", "## R5. Missing acceptance criteria", "",
              f"Proposed AC IDs start at AC{start}. The Gherkin is written in the model pass from the sources; the "
              "script names only what has no criterion.", "",
              "| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |", "|---|---|---|---|"]
        L += [f"| AC{start + i} | {esc(c)} ({esc(w)}) | Not specified in the source documents | |"
              for i, (c, w) in enumerate(self.missing)]
        L += ["", "## R7. Assumptions and limits", "",
              "- Script review only. Not judged here: whether a criterion is correct or testable as written, the "
              "meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), "
              "open questions, and the wording of improved or missing criteria. Run the model review for those.",
              "- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, "
              "build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.",
              "- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or "
              "reported falsely. Confirm each R5 row."]
        return "\n".join(L) + "\n"

    def jsonl_rows(self):
        for it in self.items.values():
            yield {"story": self.st.key, "item": it["no"], "name": it["item"], "result": it["result"],
                   "problems": [{"severity": s, "text": m} for s, m in it["problems"]],
                   "evidence": it["evidence"], "gaps": [r["id"] for r in it["gaps"]], "verdict": self.verdict, "text_verdict": self.text_verdict}


def load_roles(src):
    t = src.converted("roles")
    codes, names = set(), set()
    for r in rwbsrc.sheet(t, "Roles"):
        c, n = r.get("Role code", ""), r.get("Role name", "")
        if c:
            codes.add(c)
        if n:
            names.add(n.lower())
    return codes, names


def build_index(root):
    idx = {}
    for p in (root / rwbsrc.TEXT["stories"]).rglob("*.md"):
        k = rwbsrc.story_key_from_name(p.name)
        if not k:
            continue
        bs = ""
        for l in p.read_text(encoding="utf-8", errors="replace").splitlines()[:40]:
            m = re.match(r"\|\s*Build status\s*\|\s*(.*?)\s*\|", l)
            if m:
                bs = m.group(1)
                break
        idx.setdefault(k, (str(p), bs))
    return idx


def _chunk(job):
    root, cache, paths, det, report, overrides = job
    rwbsrc.SOURCES.update(overrides)
    src = Sources(Path(root), cache)
    idx = build_index(Path(root))
    roles = load_roles(src)
    out = []
    for p in paths:
        st = Story(Path(p))
        rv = Review(st, src, det.get(st.key, []), report.get(st.key), idx, roles).run()
        out.append((st.key, rv.md(), list(rv.jsonl_rows()), (rv.verdict, rv.text_verdict), len(rv.acr), len(rv.missing),
                    src.unread))
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--cache", required=True)
    ap.add_argument("--out", required=True)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--all", action="store_true")
    g.add_argument("--legacy")
    g.add_argument("--story-list")
    ap.add_argument("--det", help="detcheck output folder (gaps.jsonl, report.json) of the same stories")
    ap.add_argument("--jobs", type=int, default=1)
    ap.add_argument("--source", action="append", default=[], metavar="KEY=PATH")
    a = ap.parse_args(argv)
    overrides = dict(s.split("=", 1) for s in a.source)
    rwbsrc.SOURCES.update(overrides)
    root, out = Path(a.root).resolve(), Path(a.out).resolve()
    if out == root or root in out.parents:
        sys.exit("--out must be outside ROOT (sandbox only)")
    if out.exists() and any(out.iterdir()):
        sys.exit(f"--out {out} is not empty (never overwrite a run)")
    t0 = time.time()
    if a.story_list:
        paths = [Path(l.strip()) for l in Path(a.story_list).read_text(encoding="utf-8").splitlines() if l.strip()]
    else:
        paths = sorted(p for p in (root / rwbsrc.TEXT["stories"]).rglob("*.md") if rwbsrc.story_key_from_name(p.name))
        if a.legacy:
            tag = a.legacy.replace("RWB-", "").replace("-", "")
            paths = [p for p in paths if f" {tag} " in p.name]
    det, report = defaultdict(list), {}
    if a.det:
        d = Path(a.det)
        for l in (d / "gaps.jsonl").read_text(encoding="utf-8-sig").splitlines():
            if l.strip():
                r = json.loads(l)
                det[r.get("story", "")].append(r)
        if (d / "report.json").exists():
            report = json.loads((d / "report.json").read_text(encoding="utf-8")).get("stories", {})
    jobs = max(1, min(a.jobs, len(paths)))
    size = -(-len(paths) // jobs) if paths else 1
    chunks = [[str(p) for p in paths[i:i + size]] for i in range(0, len(paths), size)]
    args = [(str(root), a.cache, c, {k: det[k] for k in det}, report, overrides) for c in chunks]
    if jobs == 1:
        parts = [_chunk(x) for x in args]
    else:
        from concurrent.futures import ProcessPoolExecutor
        with ProcessPoolExecutor(max_workers=len(chunks)) as ex:
            parts = list(ex.map(_chunk, args))
    (out / "review").mkdir(parents=True)
    allrows, verdicts, unread, seen = [], Counter(), set(), Counter()
    item_res = defaultdict(Counter)
    acr_n = miss_n = 0
    problems = Counter()
    with (out / "dor.jsonl").open("w", encoding="utf-8") as fh:
        for part in parts:
            for key, md, rows, verdict, nacr, nmiss, un in part:
                seen[key] += 1
                name = key if seen[key] == 1 else f"{key} ({seen[key]})"
                (out / "review" / f"{name}.md").write_text(md, encoding="utf-8")
                verdicts[verdict] += 1
                acr_n += nacr
                miss_n += nmiss
                unread.update(un)
                for r in rows:
                    fh.write(json.dumps(r, ensure_ascii=False) + "\n")
                    item_res[(r["item"], r["name"])][r["result"]] += 1
                    for p in r["problems"]:
                        problems[(r["item"], re.sub(r"\b(AC|BR|X|TC-|MSG-|DF-|RWB-)[\w-]*\d[\w-]*", "#", p["text"]))] += 1
    n = sum(verdicts.values())
    L = ["# Script build-readiness review — summary", "", f"Tool: {TOOL}. Decision D-RCV-60.", "",
         f"Stories: {n}. Time: {time.time() - t0:.1f} s. Detcheck rows used: "
         f"{sum(len(v) for v in det.values()) if a.det else 'none (run without --det)'}.", "",
         "| Verdict (all 25 items) | Verdict on the story text (records items left out) | Stories |", "|---|---|---|"]
    L += [f"| {k[0]} | {k[1]} | {v} |" for k, v in verdicts.most_common()]
    L += ["", f"AC review rows: {acr_n}. Missing-criterion rows: {miss_n}.", "",
          "## Checklist results (Definition of Ready and Done v4 section 2)", "",
          "| # | Item | Pass | Partial | Fail | Not applicable |", "|---|---|---|---|---|---|"]
    for (no, name), c in sorted(item_res.items()):
        L.append(f"| {no} | {name} | {c['Pass']} | {c['Partial']} | {c['Fail']} | "
                 f"{c['Pass (not applicable)']} |")
    L += ["", "## Most common problems", "", "| Item | Problem (IDs replaced by #) | Stories |", "|---|---|---|"]
    L += [f"| {no} | {t.replace('|', '/')} | {c} |" for (no, t), c in problems.most_common(40)]
    if unread:
        L += ["", "Sources not read: " + "; ".join(sorted(unread))]
    (out / "summary.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    text = Counter()
    for k, v in verdicts.items():
        text[k[1]] += v
    print(f"{n} stories; on the story text: " + ", ".join(f"{k} {v}" for k, v in text.most_common())
          + f"; AC review {acr_n}, missing criteria {miss_n}; {time.time() - t0:.1f} s -> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
