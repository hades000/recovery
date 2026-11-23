import re, json
p = r'12 Project communication\Recovery Workbench Project Hub v14.html'
s = open(p, encoding='utf-8').read()
# all script tags that are NOT application/octet-stream
scripts = re.findall(r'<script(?![^>]*application/octet-stream)[^>]*>(.*?)</script>', s, re.S)
print('n scripts', len(scripts), [len(x) for x in scripts])
js = '\n/* ---- */\n'.join(scripts)
open(r'_work\msr\docs\D2-HUB\shell.js', 'w', encoding='utf-8').write(js)
j = json.load(open(r'_work\msr\docs\D2-HUB\payload.bin', encoding='utf-8'))
print('n docs', len(j['docs']))
for i, d in enumerate(j['docs']):
    if any(k in (d['name'] + d['file'] + d['folder']).lower() for k in ['hub', 'document index', 'project communication', 'read me', 'run summary']):
        print(i, d['folder'], '|', d['file'], '|', d['ext'], '|', d['inzip'])
