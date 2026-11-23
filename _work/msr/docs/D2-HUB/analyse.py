import json, os, re
from pathlib import Path

ROOT = Path('.').resolve()
payload = json.load(open(r'_work\msr\docs\D2-HUB\payload.bin', encoding='utf-8'))
docs = payload['docs']

verrx = re.compile(r'^(.*?)\s+v(\d+)(\.[^.]+)$')

def fam(name):
    base = name.rsplit('/', 1)[-1]
    m = verrx.match(base)
    if m:
        return m.group(1), int(m.group(2)), m.group(3)
    return base.rsplit('.', 1)[0] if '.' in base else base, 0, ('.' + base.rsplit('.', 1)[1] if '.' in base else '')

# build folder index of files on disk
idx = {}
for p in ROOT.iterdir():
    if p.is_dir() and re.match(r'^\d\d ', p.name):
        for f in p.rglob('*'):
            if f.is_file():
                rel = f.relative_to(ROOT).as_posix()
                folder = rel.rsplit('/', 1)[0]
                idx.setdefault(folder, []).append(rel)

print('folders', len(idx))
missing, newer, same = [], [], 0
rows = []
for d in docs:
    folder, file = d['folder'], d['file']
    base = file.rsplit('/', 1)[-1]
    f, v, ext = fam(base)
    cands = []
    for rel in idx.get(folder, []):
        b = rel.rsplit('/', 1)[-1]
        cf, cv, cext = fam(b)
        if cf == f and cext == ext:
            cands.append((cv, rel))
    if not cands:
        missing.append((folder, file))
    else:
        cv, rel = max(cands)
        if cv > v:
            newer.append((folder, file, rel))
            rows.append((folder, file, rel))
        else:
            same += 1

print('same', same, 'newer', len(newer), 'missing', len(missing))
for x in missing:
    print('MISSING', x)
print('--- newer sample')
for x in newer[:40]:
    print(x)
json.dump([{'folder': a, 'old': b, 'new': c} for a, b, c in rows], open(r'_work\msr\docs\D2-HUB\newer.json', 'w'), indent=1)
