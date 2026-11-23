import json
from collections import Counter
d = json.load(open('_work/msr/plan/split_plan.json', encoding='utf-8'))
s = d['slices']
print('slice keys:', list(s[0].keys()))
print('sample:', json.dumps(s[0], indent=1))
print('releases:', Counter(x.get('release') for x in s))
print('waves:', Counter(x.get('wave') for x in s))
print('itg slices:', [x['id'] for x in s if '-ITG' in x['id'] or x.get('wt') == 'ITG'][:40])
print('itg count:', sum(1 for x in s if x.get('wt') == 'ITG'))
