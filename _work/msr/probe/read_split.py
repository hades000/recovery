import json, sys

p = r"_work/msr/plan/split_plan.json"
data = json.load(open(p, encoding="utf-8"))
print(type(data))
if isinstance(data, dict):
    print(list(data.keys())[:40])

def walk(node):
    if isinstance(node, dict):
        if node.get("id") in {"RWB-P4-AD007-APP","RWB-P4-AD007-CON","RWB-P4-AD008-APP","RWB-P4-AD009-APP","RWB-P4-AD009-CON","RWB-P4-AD010-APP","RWB-P4-AD011-APP","RWB-P4-AD011-CON"}:
            yield node
        for v in node.values():
            yield from walk(v)
    elif isinstance(node, list):
        for v in node:
            yield from walk(v)

seen=set()
for n in walk(data):
    if n["id"] in seen: continue
    seen.add(n["id"])
    print("=====", n["id"])
    print(json.dumps(n, indent=1, ensure_ascii=False)[:4000])
