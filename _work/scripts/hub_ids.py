import re, io, base64, gzip, json, sys

path = sys.argv[1]
t = io.open(path, encoding='utf-8').read()
m = re.search(r'id="payload">([A-Za-z0-9+/=\s]+)</script>', t)
d = json.loads(gzip.decompress(base64.b64decode(m.group(1))).decode('utf-8'))
for code in ['RWB-E1-001','AC1','AC-P1-001','AC-ALT-P7-014-01','BR-P3-001','DF-ACC-014','MSG-P1-003','FEAT-RDF-01','REQ-RDF-001','TC-E1-001-01']:
    v = d['ids'].get(code)
    if not v:
        print(code, 'MISSING'); continue
    print('===', code, v['k'], 'd', v['d'], 'u', len(v['u']))
    print('t:', repr(v['t'])[:400])
