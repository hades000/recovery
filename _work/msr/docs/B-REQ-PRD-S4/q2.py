import json
d = json.load(open('_work/msr/plan/split_plan.json', encoding='utf-8'))
print('keys:', list(d.keys()))
for k in d.keys():
    v = d[k]
    print(k, type(v), len(v) if hasattr(v, '__len__') else '')
stats = d.get('stats')
print('=== stats ===')
print(json.dumps(stats, ensure_ascii=False)[:3000])
