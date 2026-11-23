import json
p = "_work/msr/plan/split_plan.json"
d = json.load(open(p, encoding="utf-8"))
print("keys:", list(d.keys()))
print("stats:", json.dumps(d.get("stats"), indent=1)[:3000])
print("legacy keys count:", len(d.get("legacy", {})))
