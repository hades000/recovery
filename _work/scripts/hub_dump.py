import re, io, base64, gzip, json, sys

path = sys.argv[1]
t = io.open(path, encoding='utf-8').read()
m = re.search(r'id="payload">([A-Za-z0-9+/=\s]+)</script>', t)
print('payload chars', len(m.group(1)))
d = json.loads(gzip.decompress(base64.b64decode(m.group(1))).decode('utf-8'))
print('top keys', list(d.keys()))
for k, v in d.items():
    if isinstance(v, list):
        print(' ', k, len(v))
    elif isinstance(v, dict):
        print(' ', k, 'dict', list(v.keys())[:10])
    else:
        print(' ', k, repr(v)[:120])
print('docs', len(d['docs']))
print(json.dumps(d['docs'][0], ensure_ascii=False)[:1500])
ids = re.findall(r'id="(f\d+)"', t)
print('blob ids', len(ids), ids[:5], ids[-3:])
for doc in d['docs']:
    if 'files' in doc:
        print('doc with files', json.dumps({k: doc[k] for k in doc if k != 'secs'}, ensure_ascii=False)[:500])
        break
