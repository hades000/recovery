import openpyxl, re, os, json

ROOT = r'C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14'

# tracker mapping
p = os.path.join(ROOT, r'15 ACE DB Alignment\Recovery Workbench ACE DB Alignment Tracker v1.xlsx')
wb = openpyxl.load_workbook(p)
ws = wb['Documents']
MAP = {}
ROWS = []
for r in ws.iter_rows(min_row=2, max_row=ws.max_row, values_only=True):
    cur, new = r[2], r[3]
    ROWS.append((r[0], r[1], cur, new))
    if cur != '(new)':
        MAP[cur.strip()] = new.strip()

# disk index: base name (without folder) -> list of full paths
disk = {}
for folder in sorted(os.listdir(ROOT)):
    fp = os.path.join(ROOT, folder)
    if not os.path.isdir(fp):
        continue
    for f in os.listdir(fp):
        disk.setdefault(f, []).append(os.path.join(folder, f))

def exists(name):
    return name in disk

def latest(base):
    """find highest version on disk for a base name like 'X v3.xlsx'"""
    m = re.match(r'^(.*) v(\d+)\.(\w+)$', base)
    if not m:
        return None
    stem, ext = m.group(1), m.group(3)
    cands = []
    for f in disk:
        mm = re.match(r'^' + re.escape(stem) + r' v(\d+)\.' + re.escape(ext) + r'$', f)
        if mm:
            cands.append((int(mm.group(1)), f))
    if not cands:
        return None
    return max(cands)[1]

print('=== tracker new files missing on disk ===')
missing = []
for n, folder, cur, new in ROWS:
    if new and not exists(new):
        alt = latest(new)
        missing.append((n, cur, new, alt))
        print(n, '|', cur, '->', new, '| on disk:', alt)
print('missing count', len(missing))
