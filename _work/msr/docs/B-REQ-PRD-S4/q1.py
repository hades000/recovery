import json
d = json.load(open('_work/msr/plan/ownership.json', encoding='utf-8'))
for sec in ['events', 'jobs', 'workflows']:
    print('===', sec, '===')
    for k, v in d[sec].items():
        s = json.dumps(v, ensure_ascii=False)
        if '"S4"' in s:
            print(k, '->', s[:600])
print('=== rulings mentioning S4 ===')
for r in d['rulings']:
    s = json.dumps(r, ensure_ascii=False)
    if 'S4' in s:
        print(s[:600])
print('=== rulings ===')
for r in d['rulings']:
    print(json.dumps(r, ensure_ascii=False)[:400])
