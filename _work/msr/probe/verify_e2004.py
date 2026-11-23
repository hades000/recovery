import json, re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
p = ROOT / "04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W2 Wave 2 integration/RWB ITG E2004 ITG Treatment entity and plan timers data model - integration v1.md"
t = p.read_text(encoding="utf-8")
META = ["Story key","Work type","Suggested owner","Service","Service epic","Wave","Business epic","Release","Legacy key","Legacy disposition","Build status","Patterns applied","Parallel lane","Ready to start","Depends on (build)","Contract dependencies","Integration dependencies","External dependencies","PRD reference","Status"]
SECTIONS = ["Story","Business rationale","Preconditions","Flow","Exception paths","INVEST check","Acceptance criteria","Business rules","State transitions","Authority","Data","Contract","Solution plan","Validation and messages","Screens and states","Test cases","Guardrails","Traceability","Out of scope"]
fails = []
first = t.splitlines()[0]
if first != "# RWB-ITG-E2004-ITG Treatment entity and plan timers data model": fails.append("title line: " + first)
head = t.split("### 1.", 1)[0]
rows = [r.strip() for r in re.findall(r"^\|\s*([^|]+?)\s*\|", head, re.M)]
got = [r for r in rows if r in META]
if got != META: fails.append("meta rows: " + str([r for r in META if r not in got]))
heads = re.findall(r"^### (\d+)\. (.+?)\s*$", t, re.M)
if [h[1] for h in heads[:19]] != SECTIONS: fails.append("sections: " + str([h[1] for h in heads[:19]]))
if [int(h[0]) for h in heads[:19]] != list(range(1, 20)): fails.append("section numbers")
for line in t.splitlines():
    if re.match(r"^\s*Scenario:\s*AC\d+", line) and not line.rstrip().endswith("(new, D-RCV-60)"):
        fails.append("AC without tag: " + line.strip()[:70])
if len(re.findall(r"^\s*Scenario: AC\d+", t, re.M)) != 9: fails.append("scenario count")
SHORTS = {"source-data","integration","case","access","decision","payment","reporting","agent","valuation","treatment","guarantee","litigation","asset","debtsale","writeoff","deviation","partner","document","comms"}
for rx in [r"\brwb\.([a-z-]+)\.events\.v1\b", r"/api/recovery/([a-z-]+)/v1\b", r"\bqueue rwb-([a-z-]+)\b"]:
    for m in re.finditer(rx, t):
        if m.group(1) not in SHORTS: fails.append("bad short: " + m.group(0))
if re.search(r"/api/recovery/v1/", t): fails.append("monolith base")
bad = [w for w in ["Jira","jira","atlassian","Co-Authored-By","Claude Code"] if w in t]
if bad: fails.append("forbidden: " + str(bad))
for m in re.finditer(r"\b[\w.+-]+@[\w-]+\.[\w.]+\b", t):
    fails.append("email: " + m.group(0))
ids = set()
for f in ("gaps","assumptions"):
    for line in (ROOT/"_work/msr"/f/"B-ITG-W2-01.jsonl").read_text(encoding="utf-8").splitlines():
        if line.strip(): ids.add(json.loads(line)["id"])
for c in set(re.findall(r"\b(?:CG|ASM)-[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*-\d+\b", t)):
    if c not in ids: fails.append("dangling cite: " + c)
if "D-RCV-60" not in t or "T3 Code / OpenCode / DeepSeek v4.1 Flash" not in t: fails.append("change log")
frag = json.loads((ROOT/"_work/msr/fragments/RWB-ITG-E2004-ITG.json").read_text(encoding="utf-8"))
need = ["id","epic","service","wt","lane","ready","owner","business_epic","wave","release","legacy","disposition","H","C","I","X","acs","tcs","reqs","ops_provided","ops_consumed","events_published","events_consumed","workflows","prd_ref","gaps","assumptions","file"]
miss = [k for k in need if k not in frag]
if miss: fails.append("fragment keys: " + str(miss))
if frag["file"] != str(p.relative_to(ROOT)).replace("\\","/"): fails.append("fragment file path")
if len(frag["tcs"]) != 16: fails.append("tcs count")
print("FAILS:", len(fails))
for f in fails: print(" -", f)
sys.exit(1 if fails else 0)
