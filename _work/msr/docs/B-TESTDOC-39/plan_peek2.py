import json
from collections import Counter, defaultdict
d = json.load(open('_work/msr/plan/split_plan.json', encoding='utf-8'))
s = d['slices']
itg = [x for x in s if x.get('wt') == 'ITG']
print('ITG epics:', Counter(x['epic'] for x in itg))
print('ITG by epic+release:')
for k, v in sorted(Counter((x['epic'], x['release']) for x in itg).items()):
    print('  ', k, v)
# wave -> release for non-ITG
print('release by wave (all):')
for k, v in sorted(Counter((x['wave'], x['release']) for x in s).items()):
    print('  W%s %-18s %s' % (k[0], k[1], v))
print()
# CON stories per service
con = [x for x in s if x.get('wt') == 'CON']
print('CON count', len(con))
print('CON by scope:', Counter(x['scope'] for x in con))
print('sample CON:', [(x['id'], x['epic']) for x in con[:8]])
# day1 counts by owner
d1 = [x for x in s if x.get('ready') == 'Day 1']
print('day1 by owner:', Counter(x['owner'] for x in d1))
