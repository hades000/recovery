"""Scratch verification for B-REQ-PRD-S7: citations, id sets, counts, header, dates, headings."""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
WORK = ROOT / "_work" / "msr"
PRD = ROOT / "03 Requirements and specifications" / "PRD" / "Recovery Workbench PRD S7 rwb-writeoff v1.md"

t = PRD.read_text(encoding="utf-8")
lines = t.splitlines()
fails = []

# 1 header lines
if "SCB Collections and Recovery. Henka Group, 22 November 2026." not in lines[0]:
    fails.append("header line 1")
if "(C) Siam Commercial Bank and Henka Pte Ltd" not in lines[1]:
    fails.append("header line 2")

# 2 change log row
if "| 1 | 22 November 2026 | D-RCV-60 microservice realignment | T3 Code / OpenCode / DeepSeek v4.1 Flash |" not in t:
    fails.append("change-log row")

# 3 citations resolve
ids = set()
for p in list((WORK / "gaps").glob("*.jsonl")) + list((WORK / "assumptions").glob("*.jsonl")):
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            try:
                ids.add(json.loads(line)["id"])
            except Exception:
                pass
cite = re.compile(r"\b(?:CG|ASM)-[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*-\d+\b")
missing = sorted({c for c in cite.findall(t) if c not in ids})
if missing:
    fails.append(f"unresolved citations: {missing}")

# 4 id sets and counts
def ids_in(prefix):
    return sorted(set(re.findall(rf"\b{prefix}-\d{{3}}\b", t)))

caps = ids_in("CAP-S7"); frs = ids_in("FR-S7"); nfrs = ids_in("NFR-S7"); acs = ids_in("AC-S7")
for name, got, expect in (("CAP", caps, 17), ("FR", frs, 41), ("NFR", nfrs, 36), ("AC", acs, 26)):
    if len(got) != expect:
        fails.append(f"{name} count {len(got)} != {expect}")
    gaps = [f"{name}-S7-{i:03d}" for i in range(1, expect + 1)]
    if got != gaps:
        fails.append(f"{name} ids not contiguous from 001")

# 5 every FR appears in the FR table (section 6) and every AC in section 11.1
fr_table = t.split("# 6. Functional requirements", 1)[1].split("# 7. Non-functional requirements", 1)[0]
for i in range(1, 42):
    fid = f"FR-S7-{i:03d}"
    if f"| {fid} |" not in fr_table:
        fails.append(f"{fid} not a row of section 6")
ac_table = t.split("## 11.1 Acceptance criteria", 1)[1].split("## 11.2", 1)[0]
for i in range(1, 27):
    aid = f"AC-S7-{i:03d}"
    if f"| {aid} |" not in ac_table:
        fails.append(f"{aid} not a row of section 11.1")

# 6 every FR referenced by an AC exists; every AC referenced in 11.2 exists
for ref in sorted(set(re.findall(r"\bFR-S7-\d{3}\b", ac_table))):
    if ref not in frs:
        fails.append(f"AC table refers to unknown {ref}")
for ref in sorted(set(re.findall(r"\bNFR-S7-\d{3}\b", ac_table))):
    if ref not in nfrs:
        fails.append(f"AC table refers to unknown {ref}")

# 7 every FR has a BR and one of BR-051..059
fr_rows = [l for l in fr_table.splitlines() if l.startswith("| FR-S7-")]
for row in fr_rows:
    cells = [c.strip() for c in row.split("|")]
    if len(cells) < 9:
        fails.append(f"short FR row: {cells[1]}")
        continue
    if not re.fullmatch(r"BR-05[1-9]", cells[4]):
        fails.append(f"{cells[1]} has no BR-05x in the BR column: {cells[4]}")
    if not re.fullmatch(r"REQ-S7-00[1-8]", cells[5]):
        fails.append(f"{cells[1]} has no FSD REQ in the REQ column: {cells[5]}")
    if cells[3] not in caps:
        fails.append(f"{cells[1]} names unknown capability {cells[3]}")

# 8 BR coverage
brs = set(re.findall(r"\bBR-05[1-9]\b", fr_table))
for i in range(51, 60):
    if f"BR-0{i}" not in brs:
        fails.append(f"BR-0{i} has no FR")

# 9 no release date altered, every one tentative
for d in ("31 January 2027", "28 February 2027", "31 March 2027", "30 April 2027", "31 May 2027", "30 June 2027"):
    for m in re.finditer(re.escape(d), t):
        tail = t[m.end():m.end() + 20]
        if "(tentative)" not in tail and d in ("30 April 2027",):
            fails.append(f"release date {d} not marked tentative at {m.start()}")

# 10 service facts
for good in ("rwb_writeoff", "/api/recovery/writeoff/v1", "rwb.writeoff.events.v1", "rwb-writeoff",
             "th.co.scb.ace.workbench.recovery.writeoff"):
    if good not in t:
        fails.append(f"service fact missing: {good}")
if re.search(r"/api/recovery/v1", t):
    fails.append("old monolith API base")

# 11 no issue tracker reference
for bad in ("Jira", "jira", "atlassian"):
    if bad in t:
        fails.append(f"issue-tracker reference: {bad}")

# 12 sections present in order
heads = [l for l in lines if re.match(r"^# \d+\. ", l)]
want = ["# 1. Document control and change log", "# 2. Product overview and relationship to ACE", "# 3. Personas and roles",
        "# 4. User journeys", "# 5. Capabilities and features", "# 6. Functional requirements",
        "# 7. Non-functional requirements", "# 8. Data requirements", "# 9. Integration points",
        "# 10. Release slicing proposal", "# 11. Acceptance criteria and validation evidence",
        "# 12. Open questions", "# 13. Approval"]
if heads != want:
    fails.append(f"section headings differ: {heads}")

print("PRD lines:", len(lines))
print("CAPs", len(caps), "FRs", len(frs), "NFRs", len(nfrs), "ACs", len(acs))
print("FAILS:", len(fails))
for f in fails:
    print(" -", f)
sys.exit(1 if fails else 0)
