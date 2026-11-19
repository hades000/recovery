import re, io, base64, gzip, json, sys, collections

path = sys.argv[1]
t = io.open(path, encoding='utf-8').read()
m = re.search(r'id="payload">([A-Za-z0-9+/=\s]+)</script>', t)
d = json.loads(gzip.decompress(base64.b64decode(m.group(1))).decode('utf-8'))
print('docs', len(d['docs']), 'ids', len(d['ids']), 'files', len(d['files']), 'fmeta', len(d['fmeta']))
print('kinds', d['kinds'])
print('ids sample', list(d['ids'].items())[:5])
# kinds of ids
kc = collections.Counter()
for k, v in d['ids'].items():
    if isinstance(v, dict):
        kc[v.get('k') or v.get('kind') or '?'] += 1
    else:
        kc[type(v).__name__] += 1
print('id kinds', kc)
# count docs by folder
fc = collections.Counter(x['folder'] for x in d['docs'])
for k in sorted(fc): print(' ', k, fc[k])
print('files sample', list(d['files'].items())[:3])
print('fmeta sample', list(d['fmeta'].items())[:3])
