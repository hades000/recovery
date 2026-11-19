import re, io, base64, gzip, json, sys

path = sys.argv[1]
t = io.open(path, encoding='utf-8').read()
m = re.search(r'id="payload">([A-Za-z0-9+/=\s]+)</script>', t)
d = json.loads(gzip.decompress(base64.b64decode(m.group(1))).decode('utf-8'))
for i, doc in enumerate(d['docs']):
    print(i, '|', doc['ext'], '|', doc['folder'], '|', doc['file'][:70], '| secs', len(doc['secs']), '| h:', ' / '.join(s['h'][:28] for s in doc['secs'][:3]))
