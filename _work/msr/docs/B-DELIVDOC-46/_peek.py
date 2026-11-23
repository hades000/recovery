import json
p = json.load(open(r"_work/msr/plan/split_plan.json", encoding="utf-8"))
print(type(p), list(p.keys()))
for k in p:
    if k not in ("legacy", "slices"):
        print("=== ", k)
        print(json.dumps(p[k])[:3000])
print("LEGACY COUNT", len(p.get("legacy", {})))
print("SLICES", len(p.get("slices", [])))
for k, v in list(p.get("legacy", {}).items())[:3]:
    print("---", k)
    print(json.dumps(v, indent=1)[:1500])
