import json
p = json.load(open(r"_work/msr/plan/ownership.json", encoding="utf-8"))
print(type(p), list(p.keys())[:40])
for k in list(p.keys())[:6]:
    v = p[k]
    print("=== ", k, type(v))
    print(json.dumps(v, indent=1)[:1200])
