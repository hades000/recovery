import re, json
t = open(r'04 User stories/Recovery Workbench Build Notes Epic 2 v3.md', encoding='utf-8').read()
src = re.findall(r'(?m)^## (RWB-E2-\d+) ', t)
plan = json.load(open(r'_work/msr/plan/split_plan.json', encoding='utf-8'))['legacy']
pk = [k for k in plan if k.startswith('RWB-E2')]
print('src', len(src), 'plan', len(pk))
print('in src not plan', sorted(set(src) - set(pk)))
print('in plan not src', sorted(set(pk) - set(src)))
