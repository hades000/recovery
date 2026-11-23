import re, json, base64, zlib
p = r'12 Project communication\Recovery Workbench Project Hub v15.html'
s = open(p, encoding='utf-8').read()
m = re.search(r'<script type="application/octet-stream" id="payload">([^<]*)</script>', s)
M = json.loads(zlib.decompress(base64.b64decode(m.group(1)), 16 + zlib.MAX_WBITS).decode('utf-8'))
want = ('Document Index', 'Control Sheet', 'Team Start Pack', 'Executive Presentation CTO', 'Project Overview')
for d in M['docs']:
    if d['folder'].startswith('12') and any(w in d['file'] for w in want):
        print(f"{d['file']:65s} -> {d.get('nf')}")
print('setfiles', len(M['setfiles']), 'folders', len(M['setfolders']))
print('nf count', sum(1 for d in M['docs'] if d.get('nf')))
for x in M['setfiles']:
    if '12 Project communication' in x['file']:
        print('  ', x['wp'], x['file'])
