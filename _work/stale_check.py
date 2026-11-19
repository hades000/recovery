import re, os

ROOT = r'C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14'
IDX = os.path.join(ROOT, r'12 Project communication\Recovery Workbench Document Index v12.md')
disk = set()
for folder in os.listdir(ROOT):
    fp = os.path.join(ROOT, folder)
    if os.path.isdir(fp):
        disk.update(os.listdir(fp))

row_re = re.compile(r'^\| (\d+) \| (.+?) \| (.+?) \| (.+?) \| (.+?) \|$')
stale = []
for line in open(IDX, encoding='utf-8').read().split('\n'):
    m = row_re.match(line)
    if not m:
        continue
    for f in [x.strip() for x in m.group(5).split(',')]:
        mm = re.match(r'^(.*) v(\d+)\.(\w+)$', f)
        if not mm:
            continue
        stem, v, ext = mm.group(1), int(mm.group(2)), mm.group(3)
        newer = []
        for g in disk:
            gm = re.match(r'^' + re.escape(stem) + r' v(\d+)\.' + re.escape(ext) + r'$', g)
            if gm and int(gm.group(1)) > v:
                newer.append(g)
        if newer:
            stale.append((m.group(1), f, sorted(newer)))
print('rows referencing a version older than one on disk:', len(stale))
for s in stale:
    print('  ', s)
