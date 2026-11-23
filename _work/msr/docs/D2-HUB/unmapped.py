import re, json, base64, zlib
p = r'12 Project communication\Recovery Workbench Project Hub v15.html'
s = open(p, encoding='utf-8').read()
m = re.search(r'<script type="application/octet-stream" id="payload">([^<]*)</script>', s)
M = json.loads(zlib.decompress(base64.b64decode(m.group(1)), 16 + zlib.MAX_WBITS).decode('utf-8'))
no = [d for d in M['docs'] if not d.get('nf')]
print('total', len(M['docs']), 'with nf', len(M['docs']) - len(no), 'without', len(no))
for d in no:
    print(' -', d['folder'], '|', d['file'])
