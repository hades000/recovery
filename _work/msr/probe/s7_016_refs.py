import json, io
d = json.load(io.open("_work/msr/plan/split_plan.json", encoding="utf-8"))
s = {x["id"]: x for x in d["slices"]}
for k in ("RWB-S7-E6028-CON", "RWB-PLT-E1027-CON", "RWB-PLT-N001-CON", "RWB-S6-E5024-APP", "RWB-S6-E6001-APP", "RWB-S6-E6005-APP", "RWB-S6-E6012-APP", "RWB-S6-E6010-APP", "RWB-S9-E6034-APP", "RWB-ITG-E6028-ITG", "RWB-S7-E6027-APP", "RWB-S7-E6018-APP"):
    x = s.get(k)
    print(k, "->", (x["title"], x["wt"], x["scope"]) if x else "MISSING")
