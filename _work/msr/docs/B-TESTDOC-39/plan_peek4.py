import json
d = json.load(open('_work/msr/plan/split_plan.json', encoding='utf-8'))
for x in d['slices']:
    if x['legacy'].startswith('W') and 'J' in x['legacy'] and len(x['legacy']) == 5:
        print(x['id'], '|', x['title'], '|', x['owner'], '|', x['ready'])
print()
for x in d['slices']:
    if x['legacy'] in ('N001', 'N002', 'N009', 'N011'):
        print(x['id'], '|', x['title'])
