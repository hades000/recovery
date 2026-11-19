import re, io, base64, gzip, json, sys

path = sys.argv[1]
t = io.open(path, encoding='utf-8').read()
m = re.search(r'id="payload">([A-Za-z0-9+/=\s]+)</script>', t)
d = json.loads(gzip.decompress(base64.b64decode(m.group(1))).decode('utf-8'))
s = d['ids']['RWB-E1-001']['t']
print(repr(s))
print([hex(ord(c)) for c in s[30:80]])
# check all text for replacement chars
bad = 0
for doc in d['docs']:
    for sec in doc['secs']:
        if '\ufffd' in sec['t']:
            bad += 1
print('sections with U+FFFD:', bad)
