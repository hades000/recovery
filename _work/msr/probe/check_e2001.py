import json, re, io
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
story = ROOT / "04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W2 Wave 2 integration/RWB ITG E2001 ITG EFS hand-over with full history - integration v1.md"
legacy = ROOT / "04 User stories/Recovery Workbench User Stories Epic 2 Story Files v5/RWB E2 001 EFS hand over with full history from the COLLINS load v1.md"
t = story.read_text(encoding="utf-8")
L = legacy.read_text(encoding="utf-8")
fails=[]
lines=t.splitlines()
if lines[0] != "# RWB-ITG-E2001-ITG EFS hand-over with full history": fails.append("first line")
if lines[1].strip() != "": fails.append("blank line 2")
if not lines[2].startswith("SCB Collections and Recovery. Henka Group, 22 November 2026."): fails.append("header1")
if lines[3].strip() != "(C) Siam Commercial Bank and Henka Pte Ltd": fails.append("header2")
heads = re.findall(r"(?m)^### (\d+)\. (.+)$", t)
want = ["Story","Business rationale","Preconditions","Flow","Exception paths","INVEST check","Acceptance criteria","Business rules","State transitions","Authority","Data","Contract","Solution plan","Validation and messages","Screens and states","Test cases","Guardrails","Traceability","Out of scope"]
got = [h[1].strip() for h in heads]
if got != want: fails.append(f"headings {got}")
# metadata
meta = t.split("| Item | Value |",1)[1].split("\n\n",1)[0]
rows = re.findall(r"(?m)^\| ([^|]+?) \|", meta)
want_rows = ["Item","Story key","Work type","Suggested owner","Service","Service epic","Wave","Business epic","Release","Legacy key","Legacy disposition","Build status","Patterns applied","Parallel lane","Ready to start","Depends on (build)","Contract dependencies","Integration dependencies","External dependencies","PRD reference","Status"]
if [r.strip() for r in rows] != want_rows: fails.append(f"meta rows {[r.strip() for r in rows]}")
# scenarios
sc = re.findall(r"(?m)^\s*Scenario: (AC\d+)(.*)$", t)
print("scenarios:", [(a,b.strip()) for a,b in sc])
for a,b in sc:
    b=b.strip()
    if not (re.search(r"\(legacy RWB-E2-001 AC\d\)$", b) or b.endswith("(new, D-RCV-60)")): fails.append(f"tag {a}")
# verbatim legacy blocks
def block(txt, start, end):
    i = txt.index(start); j = txt.index(end, i)
    return txt[i:j].rstrip("\n")
pairs = [("Scenario: AC1 Case from the ACE data","Scenario: AC2 Repeat run"),
         ("Scenario: AC3 Late ACE batch","Scenario: AC4 Account linked"),
         ("Scenario: AC5 Customer not in the ACE customer data","Scenario: AC6 Cases created"),
         ("Scenario: AC6 Cases created on the next good batch","Scenario: AC7 Decision log write fails")]
for s,e in pairs:
    lb = block(L,s,e)
    # story block ends at next scenario
    m = re.search(r"(?m)^\s*Scenario: "+re.escape(s.split("Scenario: ")[1])+r".*$", t)
    if not m: fails.append(f"missing {s}"); continue
    start_idx = m.start()
    nxt = re.search(r"(?m)^\s*Scenario: AC", t[m.end():])
    sb = t[start_idx: m.end()+ (nxt.start() if nxt else 0)].rstrip("\n")
    # normalise: strip origin tag from scenario line of story, compare scenario titles
    l_lines = [x.rstrip() for x in lb.splitlines()]
    s_lines = [x.rstrip() for x in sb.splitlines()]
    s_lines[0] = re.sub(r" \(legacy RWB-E2-001 AC\d\)$","",s_lines[0])
    if l_lines != s_lines:
        fails.append(f"not verbatim: {s}")
        for a,b in zip(l_lines,s_lines):
            if a!=b: fails.append("  legacy: "+a+" || story: "+b)
# forbidden
if re.search(r"(?i)\bjira\b|atlassian\.net", t): fails.append("issue tracker mention")
if re.search(r"/api/recovery/v1/", t): fails.append("monolith base")
if re.search(r"[\w.+-]+@[\w-]+\.[\w.]+", t): fails.append("email")
# change log
if "D-RCV-60" not in t or "Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash." not in t: fails.append("changelog")
print("FAILS:", fails if fails else "none")
