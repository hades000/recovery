import re, base64, zlib, json

p = r'12 Project communication\Recovery Workbench Project Hub v14.html'
s = open(p, encoding='utf-8').read()
m = re.search(r'<script type="application/octet-stream" id="payload">([^<]*)</script>', s)
b = base64.b64decode(m.group(1))
d = zlib.decompress(b, 16 + zlib.MAX_WBITS)
print('len', len(d))
open(r'_work\msr\docs\D2-HUB\payload.bin', 'wb').write(d)
print(d[:600])
try:
    j = json.loads(d)
    print('JSON keys', list(j)[:30] if isinstance(j, dict) else type(j), len(j))
except Exception as e:
    print('not json', e)
