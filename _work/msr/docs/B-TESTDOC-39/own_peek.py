import json
from collections import Counter
o = json.load(open('_work/msr/plan/ownership.json', encoding='utf-8'))
codes = ['PLT'] + ['P%d' % i for i in range(1, 11)] + ['S%d' % i for i in range(1, 10)]
for name in ('tables', 'api', 'events', 'workflows', 'jobs'):
    c = Counter(v['owner'] for v in o[name].values())
    print(name, sum(c.values()), {k: c.get(k, 0) for k in codes})
# per service bundle
rows = []
for k in codes:
    rows.append((k,
                 sum(1 for v in o['tables'].values() if v['owner'] == k),
                 sum(1 for v in o['api'].values() if v['owner'] == k),
                 sum(1 for v in o['events'].values() if v['owner'] == k),
                 sum(1 for v in o['workflows'].values() if v['owner'] == k),
                 sum(1 for v in o['jobs'].values() if v['owner'] == k)))
tot = [0] * 5
for r in rows:
    print('| %s | %d | %d | %d | %d | %d |' % r)
    for i in range(5):
        tot[i] += r[i + 1]
print('TOTAL', tot)
# workflows list per owner
for k in codes:
    w = [v['id'] for v in o['workflows'].values() if v['owner'] == k]
    if w:
        print(k, 'workflows:', ', '.join(sorted(w)))
# events per owner names
for k in codes:
    e = sorted(v['id'] for v in o['events'].values() if v['owner'] == k)
    if e:
        print(k, 'events:', len(e), ' '.join(e))
