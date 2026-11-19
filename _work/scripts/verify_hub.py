import base64
import gzip
import hashlib
import io
import json
import os
import re
import subprocess
import tempfile

ROOT = r'C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14'
HUB = os.path.join(ROOT, '14 Story Updates', 'Recovery Workbench Project Hub v16.html')
html = io.open(HUB, encoding='utf-8').read()

m = re.search(r'id="payload">([A-Za-z0-9+/=\s]+)</script>', html)
payload = json.loads(gzip.decompress(base64.b64decode(m.group(1))).decode('utf-8'))
print('docs', len(payload['docs']), 'ids', len(payload['ids']), 'files', len(payload['files']))
print('kinds', len(payload['kinds']), 'folders', len(set(d['folder'] for d in payload['docs'])))
bad = []
for code, v in payload['ids'].items():
    if not (0 <= v['d'][0] < len(payload['docs'])):
        bad.append((code, 'd'))
    if not v['u']:
        bad.append((code, 'u'))
    for di, si in v['u']:
        if not (0 <= di < len(payload['docs']) and 0 <= si < len(payload['docs'][di]['secs'])):
            bad.append((code, 'u-index'))
print('bad id entries', len(bad), bad[:5])
print('removed stories present', [k for k in ['RWB-E1-003', 'RWB-E1-004', 'RWB-E1-005', 'RWB-E1-006',
                                              'RWB-E1-009', 'RWB-E1-010', 'RWB-E1-012', 'RWB-E1-051',
                                              'RWB-E2-023'] if k in payload['ids']])

# blobs
blobs = dict((int(x), b) for x, b in re.findall(r'id="f(\d+)">([A-Za-z0-9+/=\s]+)</script>', html))
print('blob blocks', len(blobs))
missing = [n for n in payload['files'] if payload['files'][n] not in blobs]
print('files without blob', missing[:5])
ok = 0
for name, idx in payload['files'].items():
    meta = payload['fmeta'][name]
    path = os.path.join(ROOT, meta['folder'], name)
    raw = io.open(path, 'rb').read()
    got = gzip.decompress(base64.b64decode(blobs[idx]))
    if hashlib.sha256(raw).hexdigest() != hashlib.sha256(got).hexdigest():
        print('MISMATCH', name)
        break
    ok += 1
print('blobs verified', ok, 'of', len(payload['files']))

# JS syntax: every script without a type
scripts = re.findall(r'<script(?![^>]*type="application/octet-stream")[^>]*>(.*?)</script>', html, re.S)
print('code scripts', len(scripts))
tmp = tempfile.mkdtemp()
for i, code in enumerate(scripts):
    p = os.path.join(tmp, 's%d.js' % i)
    io.open(p, 'w', encoding='utf-8').write(code)
    r = subprocess.run(['node', '--check', p], capture_output=True, text=True)
    if r.returncode != 0:
        print('SYNTAX ERROR script', i, r.stderr[:800])
        break
else:
    print('all scripts parse')

# spot checks
for code in ['RWB-E1-001', 'RWB-E1-069', 'RWB-ACE-001', 'D-RCV-35', 'DL43', 'DF-ACE-018']:
    v = payload['ids'].get(code)
    print(code, bool(v), v['k'] if v else '', v['t'][:90] if v else '')
print('html MB', round(os.path.getsize(HUB) / 1048576, 2))
