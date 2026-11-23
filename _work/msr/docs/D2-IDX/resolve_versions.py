import os, re

ROOT = os.getcwd()
skip = ('.git', '_work', '22 Microservice Realignment', 'node_modules')

allfiles = {}
for dirpath, dirnames, filenames in os.walk(ROOT):
    dirnames[:] = [d for d in dirnames if d not in skip]
    for f in filenames:
        allfiles.setdefault(f, []).append(os.path.join(dirpath, f))

t = open('12 Project communication/Recovery Workbench Document Index v13.md', encoding='utf-8').read()
rows = []
for line in t.splitlines():
    if line.startswith('| ') and line.count('|') >= 6:
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        if len(cells) == 5 and re.match(r'^\d+$', cells[0]):
            rows.append(cells)

ver = re.compile(r'^(.*?) v(\d+)(\.[A-Za-z0-9]+)$')
out = []
for num, doc, what, std, files in rows:
    parts = [p.strip() for p in files.split(',')]
    line = [num, doc]
    for p in parts:
        base = os.path.basename(p)
        hits = allfiles.get(base, [])
        if not hits:
            line.append(f'MISSING {base}')
            continue
        m = ver.match(base)
        if not m:
            line.append(f'ok {base}')
            continue
        stem, v = m.group(1), int(m.group(2))
        d = os.path.dirname(hits[0])
        try:
            fam = os.listdir(d)
        except OSError:
            fam = []
        fam = [f for f in fam if re.match(re.escape(stem) + r' v\d+\.[A-Za-z0-9]+$', f)]
        best = max([int(re.search(r' v(\d+)\.', f).group(1)) for f in fam] or [v])
        if best > v:
            newest = sorted(f for f in fam if int(re.search(r' v(\d+)\.', f).group(1)) == best)
            line.append(f'NEW v{best}: {", ".join(newest)}')
        else:
            line.append(f'v{v} unchanged')
    out.append(line)

for l in out:
    print(' | '.join(l))
