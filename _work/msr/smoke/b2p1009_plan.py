import json, pathlib
p = pathlib.Path("_work/msr/plan/split_plan.json")
d = json.loads(p.read_text(encoding="utf-8"))
s = {x["id"]: x for x in d["slices"]}
x = s.get("RWB-P1-DM010-APP")
print(json.dumps({k: x.get(k) for k in ("id", "scope", "wt", "release", "file", "acs", "preserved", "delta", "legacy", "H", "C", "I", "X")}, indent=1))
print("legacy row:", json.dumps(d["legacy"].get("RWB-DM-010"), indent=1))
