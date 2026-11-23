import json, sys
sys.stdout.reconfigure(encoding='utf-8')
p = json.load(open('_work/msr/plan/ownership_part_api.json', encoding='utf-8'))
print(type(p), list(p.keys())[:10] if isinstance(p, dict) else len(p))
rows = p['api'] if isinstance(p, dict) and 'api' in p else p
for k, v in (rows.items() if isinstance(rows, dict) else [(x.get('id'), x) for x in rows]):
    print(v.get('owner'), '|', k)
