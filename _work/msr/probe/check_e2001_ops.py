import json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
own = json.load(open(ROOT/"_work/msr/plan/ownership.json", encoding="utf-8"))
t = (ROOT/"04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W2 Wave 2 integration/RWB ITG E2001 ITG EFS hand-over with full history - integration v1.md").read_text(encoding="utf-8")
sec = t.split("#### 12.2 REST operations consumed",1)[1].split("#### 12.3",1)[0]
fails = []
n = 0
for r in [x for x in sec.splitlines() if x.startswith("| GET") or x.startswith("| POST")]:
    cells = [c.strip().strip("`") for c in r.strip("|").split("|")]
    method, path = cells[0], cells[1]
    n += 1
    m = own["api"].get(f"{method} /{path.split('/v1/',1)[1]}")
    if not m:
        fails.append("miss " + path)
    elif m["owner"] != cells[2].split()[0]:
        fails.append(f'owner {path}: {m["owner"]} vs {cells[2]}')
print("rows", n, "FAILS:", fails if fails else "none")
