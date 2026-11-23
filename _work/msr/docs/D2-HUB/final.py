import json, re
for path in (r'_work\msr\gaps\D2-HUB.jsonl', r'_work\msr\assumptions\D2-HUB.jsonl'):
    rows = [json.loads(l) for l in open(path, encoding='utf-8') if l.strip()]
    print(path, len(rows), 'ids', [r['id'] for r in rows])
    for r in rows:
        assert '\u00c2' not in json.dumps(r, ensure_ascii=False), r['id']

s = open(r'12 Project communication\Recovery Workbench Project Hub v15.html', encoding='utf-8').read()
i = s.index('<header>')
print(repr(s[i:i+420]))
print('--- head ---')
print(s[:220].replace('\n', ' | ')[:220])
