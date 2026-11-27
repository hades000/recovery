import csv, glob, os, collections, yaml
rows = list(csv.DictReader(open('../../editlog/FD1-contracts.csv', encoding='utf-8')))
print(len(rows), collections.Counter(r['action'] for r in rows), len({r['edit_id'] for r in rows}))
A = '../../stage/05 Technical architecture/Recovery Workbench API Specification v7'
changed = []
for f in glob.glob(A + '/**/*.yaml', recursive=True):
    rel = os.path.relpath(f, A)
    b = open(os.path.join('before-api', rel), 'rb').read(); a = open(f, 'rb').read()
    if a != b:
        crlf = (b'\r\n' in b, b'\r\n' in a)
        stray = a.count(b'\n') - a.count(b'\r\n') if crlf[0] else a.count(b'\r\n')
        changed.append((rel.replace(os.sep, '/'), crlf[0] == crlf[1], stray))
    yaml.safe_load(a.decode('utf-8'))
print(len(changed), 'changed; eol problems:', [c for c in changed if not c[1] or c[2]])
import difflib
for name in ('rwb-source-data.yaml',):
    a = open(os.path.join('before-api', name), encoding='utf-8').read().splitlines()
    b = open(os.path.join(A, name), encoding='utf-8').read().splitlines()
    d = list(difflib.unified_diff(a, b, n=0, lineterm=''))
    print(name, 'removed', sum(l.startswith('-') and not l.startswith('---') for l in d), 'added', sum(l.startswith('+') and not l.startswith('+++') for l in d))
d = yaml.safe_load(open(os.path.join(A, 'rwb-source-data.yaml'), encoding='utf-8'))
for p in ('/payments', '/customers/{personKey}', '/admin/jobs', '/data-products/{productCode}/records', '/efs-history'):
    for m, o in d['paths'][p].items():
        print(m, p, sorted(o['responses']), [x.get('name') for x in o.get('parameters', []) if 'name' in x])
s = d['components']['schemas']
print(len(s['Customer']['properties']), len(s['Account']['properties']), s['Collateral']['properties']['detail']['type'], list(s['Collateral']['properties']['detail']['properties'])[:3], s['BatchStatusAnswer']['properties']['checksum'])
