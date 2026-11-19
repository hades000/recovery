import io, os, re, os.path

ROOT = r'C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14'
INDEX = os.path.join(ROOT, '12 Project communication', 'Recovery Workbench Document Index v12.md')
text = io.open(INDEX, encoding='utf-8-sig').read()
rows = []
for line in text.split('\n'):
    if not line.strip().startswith('|'):
        continue
    cells = [c.strip() for c in line.strip().strip('|').split('|')]
    if len(cells) < 5 or not re.match(r'^\d+$', cells[0]):
        continue
    files = [f.strip() for f in cells[4].split(',') if f.strip()]
    rows.append((cells[0], cells[1], files))

all_files = {}
for folder in os.listdir(ROOT):
    p = os.path.join(ROOT, folder)
    if os.path.isdir(p) and folder[:2].isdigit():
        for name in os.listdir(p):
            if os.path.isfile(os.path.join(p, name)):
                all_files.setdefault(name, []).append(folder)

stale = []
missing = []
for num, title, files in rows:
    for f in files:
        if f not in all_files:
            missing.append((num, title, f))
            continue
        stem, ext = os.path.splitext(f)
        m = re.match(r'^(.*) v(\d+)$', stem)
        if not m:
            continue
        base, ver = m.group(1), int(m.group(2))
        siblings = []
        for name in all_files:
            s2, e2 = os.path.splitext(name)
            m2 = re.match(r'^(.*) v(\d+)$', s2)
            if m2 and m2.group(1) == base and e2 == ext:
                siblings.append((int(m2.group(2)), name))
        if siblings:
            top = max(siblings)
            if top[0] > ver:
                stale.append((num, title, f, top[1]))
print('rows', len(rows), 'missing', len(missing), 'stale', len(stale))
for x in stale:
    print(x)
print('--- missing ---')
for x in missing[:20]:
    print(x)
