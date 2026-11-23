import json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
own = json.load(open(ROOT/"_work/msr/plan/ownership.json", encoding="utf-8"))
frag = json.load(open(ROOT/"_work/msr/fragments/RWB-ITG-E2001-ITG.json", encoding="utf-8"))
story = ROOT/"04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W2 Wave 2 integration/RWB ITG E2001 ITG EFS hand-over with full history - integration v1.md"
t = story.read_text(encoding="utf-8")
shorts = {"source-data","integration","case","access","document","comms","decision","payment","reporting","agent","valuation","treatment","guarantee","litigation","asset","debtsale","writeoff","deviation","partner"}
fails=[]
# ops
for op in frag["ops_consumed"]:
    m = re.match(r"^(GET|POST|PATCH|PUT|DELETE) (/api/recovery/([a-z-]+)/v1/(.*))$", op)
    if not m: fails.append("bad op form: "+op); continue
    method, path, short, rest = m.groups()
    if short not in shorts: fails.append("bad short: "+op)
    key = f"{method} /{rest}"
    if key not in own["api"]: fails.append(f"op not in map: {op} -> {key}")
# events
for ev in frag["events_consumed"]:
    m = re.match(r"^rwb\.([a-z-]+)\.([A-Za-z]+)\.v1$", ev)
    if not m: fails.append("bad event: "+ev); continue
    if m.group(1) not in shorts: fails.append("bad event short: "+ev)
# story-level path checks
for m in re.finditer(r"/api/recovery/([a-z-]+)/v1", t):
    if m.group(1) not in shorts: fails.append("bad story short "+m.group(0))
for m in re.finditer(r"\brwb\.([a-z-]+)\.events\.v1\b", t):
    if m.group(1) not in shorts: fails.append("bad topic "+m.group(0))
# owners named next to each §12.2 row
sec = t.split("#### 12.2 REST operations consumed",1)[1].split("#### 12.3",1)[0]
rows = [r for r in sec.splitlines() if r.startswith("| GET") or r.startswith("| POST")]
print("12.2 rows:", len(rows))
code = {"P1":"P1","P2":"P2","P3":"P3","P4":"P4","P7":"P7"}
for r in rows:
    cells=[c.strip() for c in r.strip("|").split("|")]
    method, path = cells[0], cells[1]
    owner_cell = cells[2]
    mapped = own["api"].get(f"{method} /{path.split('/v1/',1)[1]}")
    if not mapped: fails.append(f"map miss {method} {path}")
    else:
        code_in_row = owner_cell.split()[0]
        if mapped["owner"] != code_in_row: fails.append(f"owner mismatch {path}: map {mapped['owner']} vs row {code_in_row}")
# tables narrative
print("interaction", own["tables"]["interaction"]["owner"], "efs_ledger_outcome", own["tables"]["efs_ledger_outcome"]["owner"], "reconciliation_result", own["tables"]["reconciliation_result"]["owner"], "recovery_case", own["tables"]["recovery_case"]["owner"], "case_account", own["tables"]["case_account"]["owner"], "decision_log_entry", own["tables"]["decision_log_entry"]["owner"], "processed_event", own["tables"]["processed_event"]["owner"])
# jobs / workflows
print("JOB-02", own["jobs"]["JOB-02"]["owner"], "JOB-06", own["jobs"]["JOB-06"]["owner"], "JOB-14", own["jobs"]["JOB-14"]["owner"])
print("CaseWorkflow", own["workflows"]["CaseWorkflow"]["owner"])
# citations
ids=set()
for kind in ("gaps","assumptions"):
    for p in (ROOT/"_work/msr"/kind).glob("*.jsonl"):
        for l in p.read_text(encoding="utf-8").splitlines():
            if l.strip(): ids.add(json.loads(l)["id"])
for c in set(re.findall(r"\b(?:CG|ASM)-[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*-\d+\b", t)):
    if c not in ids: fails.append("uncited "+c)
print("fragment keys:", list(frag))
print("FAILS:", fails if fails else "none")
