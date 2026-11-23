import json
d = json.load(open('_work/msr/plan/split_plan.json', encoding='utf-8'))
for x in d['slices']:
    if 'W1J01' in x['id'] or 'W1J' in x['legacy']:
        print(json.dumps({k: x[k] for k in ('id', 'legacy', 'title', 'epic', 'wave', 'release', 'owner', 'ready', 'C', 'I', 'H')}, indent=1))
print('--- NFR stories ---')
for x in d['slices']:
    if x['epic'] == 'RWB-ITG-NFR':
        print(json.dumps({k: x[k] for k in ('id', 'legacy', 'title', 'epic', 'wave', 'owner', 'release')}, indent=1))
print('--- new platform N stories ---')
print([x['id'] for x in d['slices'] if x.get('new')][:40])
