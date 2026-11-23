import json

d = json.load(open('_work/msr/plan/ownership.json', encoding='utf-8'))
for sect in ('events', 'workflows', 'jobs'):
    print('=====', sect)
    for k, v in d[sect].items():
        s = json.dumps(v, ensure_ascii=False)
        if '"S6"' in s or 'debtsale' in s.lower():
            print(k, '|', s[:700])
            print()
print('===== tables (debtsale)')
for k, v in d['tables'].items():
    s = json.dumps(v, ensure_ascii=False)
    if 'debtsale' in s.lower() or '"S6"' in s:
        print(k, '|', s[:500])
print('===== rulings mentioning S6/debt sale')
for r in d['rulings']:
    s = json.dumps(r, ensure_ascii=False)
    if 'S6' in s or 'debt sale' in s.lower():
        print(s[:600])
