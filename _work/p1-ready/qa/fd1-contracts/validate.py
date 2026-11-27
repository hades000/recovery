import glob, os, re, yaml
os.chdir(os.path.join('..', '..', 'stage', '05 Technical architecture', 'Recovery Workbench API Specification v7'))
M = ('get','put','post','patch','delete')
files = glob.glob('*.yaml') + glob.glob('asyncapi/*.yaml')
docs = {f.replace(os.sep,'/'): yaml.safe_load(open(f, encoding='utf-8')) for f in files}
def walk(o):
    if isinstance(o, dict):
        for k, v in o.items():
            if k == '$ref': yield v
            else: yield from walk(v)
    elif isinstance(o, list):
        for v in o: yield from walk(v)
def resolve(doc, ptr):
    cur = doc
    for part in [p.replace('~1','/').replace('~0','~') for p in ptr.strip('/').split('/') if p]:
        cur = cur[part]
    return cur
bad = []; nref = 0
for name, d in docs.items():
    for r in walk(d):
        nref += 1
        file, _, ptr = r.partition('#')
        target = name if not file else os.path.normpath(os.path.join(os.path.dirname(name), file)).replace(os.sep,'/')
        try: resolve(docs[target], ptr)
        except Exception as e: bad.append((name, r))
ids = {}
for name, d in docs.items():
    if not isinstance(d.get('paths'), dict): continue
    for p, v in d['paths'].items():
        for m, o in v.items():
            if m not in M: continue
            ids.setdefault((name, o.get('operationId')), []).append(p)
            declared = [x.get('name') or x['$ref'].split('/')[-1] for x in o.get('parameters', [])]
            for ph in re.findall(r'\{(\w+)\}', p):
                if ph not in declared: bad.append((name, m, p, 'path parameter not declared', ph))
            if len(set(declared)) != len(declared): bad.append((name, m, p, 'duplicate parameter'))
            codes = [int(c) for c in o['responses']]
            if not any(c < 300 for c in codes): bad.append((name, m, p, 'no success'))
bad += [('dup operationId', k, v) for k, v in ids.items() if len(v) > 1]
pat = re.compile(r'^MSG-[A-Z0-9]+(?:-[A-Z0-9]+)*-[0-9]{2,3}$')
for x in ('MSG-PLT-N009-03','MSG-PLT-N009-05','MSG-PLT-N009-06','MSG-GEN-001','MSG-P1-001'):
    assert pat.match(x), x
old = sum(open(f, encoding='utf-8').read().count('(-[A-Z0-9]+)*-') for f in files)
print('files', len(docs), 'refs', nref, 'old patterns', old, 'problems', bad)
