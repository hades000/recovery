import json, sys
from pathlib import Path
sys.path.insert(0, "22 Microservice Realignment/compat")
from common import SERVICES

print(json.dumps(SERVICES, indent=1)[:3000])

own = json.load(open("_work/msr/plan/ownership.json", encoding="utf-8"))
print(list(own.keys()))
tables = own["tables"]
dump = json.load(open("_work/msr/docs/B-DATA-18/v4_dump.json", encoding="utf-8"))
ents = []
for r in dump["Mapping"][1:]:
    e = r[2]
    if e not in ents:
        ents.append(e)
for e in ents:
    t = tables.get(e)
    print(e, "->", (t["owner"] if t else "MISSING"), (t["basis"][:80] if t else ""))
print("owner keys sample", list(own.keys())[:5])
