import json

d = json.load(open('_work/msr/plan/split_plan.json', encoding='utf-8'))
legacy = d['legacy']
for k, v in legacy.items():
    if v.get('primary') == 'S6':
        print(k, '|', json.dumps(v, ensure_ascii=False))
print('---- slices owned by S6')
slices = d['slices']
if isinstance(slices, dict):
    for k, v in slices.items():
        s = json.dumps(v, ensure_ascii=False)
        if s.find('"S6"') >= 0:
            print(k, '|', s[:400])
else:
    print(type(slices))
