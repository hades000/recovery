import json
d = json.load(open('_work/msr/plan/split_plan.json', encoding='utf-8'))
leg = d['legacy']
print('sample legacy keys:', list(leg.keys())[:5])
k0 = list(leg.keys())[0]
print(json.dumps(leg[k0], ensure_ascii=False)[:1500])
print('=== S4 legacy ===')
for k, v in leg.items():
    s = json.dumps(v, ensure_ascii=False)
    if v.get('service') == 'S4' or '"S4"' in s:
        print(k, '->', s[:1200])
