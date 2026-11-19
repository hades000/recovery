import re, io, base64, gzip, json, sys

path = sys.argv[1]
t = io.open(path, encoding='utf-8').read()
m = re.search(r'id="payload">([A-Za-z0-9+/=\s]+)</script>', t)
d = json.loads(gzip.decompress(base64.b64decode(m.group(1))).decode('utf-8'))
hits = 0
for i, doc in enumerate(d['docs']):
    for j, s in enumerate(doc['secs']):
        if re.search(r'developer action|dev action|Developer Action', s['t'], re.I):
            print(i, doc['file'], '|', s['h'], '|', s['t'][:300].replace('\n', ' '))
            hits += 1
print('hits', hits)
# section headings of a story doc
for doc in d['docs']:
    if 'RWB E1 001' in doc['file'] or 'Epic 1 v8' in doc['file']:
        print('DOC', doc['file'], len(doc['secs']))
        print([s['h'] for s in doc['secs']][:40])
        print(doc['secs'][0]['t'][:800])
        break
