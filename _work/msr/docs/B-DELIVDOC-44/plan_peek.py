import json
d = json.load(open("_work/msr/plan/split_plan.json", encoding="utf-8"))
print(list(d.keys()))
print(json.dumps(d.get("stats"), indent=1)[:3000])
