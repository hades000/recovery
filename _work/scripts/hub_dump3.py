import re, io, base64, gzip, json, sys

path = sys.argv[1]
t = io.open(path, encoding='utf-8').read()
m = re.search(r'id="payload">([A-Za-z0-9+/=\s]+)</script>', t)
d = json.loads(gzip.decompress(base64.b64decode(m.group(1))).decode('utf-8'))
print('--- docs with inzip ---')
for i, doc in enumerate(d['docs']):
    if doc['inzip']:
        print(i, '|', doc['folder'], '|', doc['file'], '| inzip:', doc['inzip'], '| secs', len(doc['secs']))
print('--- user stories docs ---')
for i, doc in enumerate(d['docs']):
    if doc['folder'].startswith('04'):
        print(i, '|', doc['file'], '| secs', len(doc['secs']), '| inzip', doc['inzip'])
print('--- blob check ---')
m2 = re.search(r'id="f0">([A-Za-z0-9+/=\s]+)</script>', t)
raw = gzip.decompress(base64.b64decode(m2.group(1)))
print(len(raw), raw[:80])
print('files -> blob idx', list(d['files'].items())[:5])
print('fmeta', list(d['fmeta'].items())[:2])
