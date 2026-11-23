import json
d = json.load(open("_work/msr/plan/ownership.json", encoding="utf-8"))
print(list(d.keys()))
for k, v in d.items():
    print(k, type(v), len(v) if hasattr(v, "__len__") else "")
