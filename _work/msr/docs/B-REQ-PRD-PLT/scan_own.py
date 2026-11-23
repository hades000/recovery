import json, io

d = json.load(io.open(r'_work/msr/plan/ownership.json', encoding='utf-8'))
for k in d:
    v = d[k]
    print('===', k, type(v), len(v))
    if isinstance(v, dict):
        for kk, vv in list(v.items())[:3]:
            print('  ', kk, json.dumps(vv)[:300])
    else:
        print(json.dumps(v[:3])[:800])
