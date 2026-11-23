import json

d = json.load(open('_work/msr/plan/split_plan.json', encoding='utf-8'))
print('top keys:', list(d.keys()))
stats = d.get('stats')
print('stats:', json.dumps(stats, ensure_ascii=False)[:2000] if not isinstance(stats, (int, str)) else stats)
legacy = d.get('legacy')
print('legacy type:', type(legacy), len(legacy) if hasattr(legacy, '__len__') else '')
if isinstance(legacy, dict):
    ks = list(legacy.keys())[:5]
    print('legacy sample keys:', ks)
    print(json.dumps(legacy[ks[0]], ensure_ascii=False)[:800])
elif isinstance(legacy, list):
    print(json.dumps(legacy[0], ensure_ascii=False)[:800])
