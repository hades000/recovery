import re, base64, zlib, json, sys

p = r'12 Project communication\Recovery Workbench Project Hub v14.html'
s = open(p, encoding='utf-8').read()
print('chars', len(s))
ms = re.findall(r'<script type="application/octet-stream" id="([^"]+)">([^<]*)</script>', s)
print('scripts', len(ms))
names = [m[0] for m in ms]
print('first', names[:3], 'last', names[-3:])
out = {}
for name, b in ms:
    try:
        d = zlib.decompress(base64.b64decode(b), 16 + zlib.MAX_WBITS)
    except Exception as e:
        print(name, 'ERR', e)
        continue
    out[name] = d
    print(name, len(d), d[:160])
json.dump({k: len(v) for k, v in out.items()}, open(r'_work\msr\docs\D2-HUB\sizes.json', 'w'))
for k in list(out)[:3]:
    open(r'_work\msr\docs\D2-HUB\sample_%s.bin' % k, 'wb').write(out[k])
