import re, os, collections

ROOT = r'C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14'
P = os.path.join(ROOT, r'12 Project communication\Recovery Workbench Document Index v12.md')

disk = {}
for folder in os.listdir(ROOT):
    fp = os.path.join(ROOT, folder)
    if os.path.isdir(fp):
        for f in os.listdir(fp):
            disk.setdefault(f, []).append(folder)

txt = open(P, encoding='utf-8').read()
row_re = re.compile(r'^\| (\d+) \| (.+?) \| (.+?) \| (.+?) \| (.+?) \|$')
rows = []
for line in txt.split('\n'):
    m = row_re.match(line)
    if m:
        rows.append(m.groups())

print('rows', len(rows))
ids = [r[0] for r in rows]
dup_ids = [i for i, c in collections.Counter(ids).items() if c > 1]
print('duplicate ids', dup_ids)
print('id range', min(map(int, ids)), max(map(int, ids)))
missing_ids = sorted(set(range(1, 131)) - set(map(int, ids)))
print('ids not used 1..130', missing_ids)

files = []
bad = []
for r in rows:
    for n in [x.strip() for x in r[4].split(',')]:
        files.append(n)
        if n not in disk:
            bad.append((r[0], n))
print('file references', len(files))
print('missing on disk', bad)

dupf = [f for f, c in collections.Counter(files).items() if c > 1]
print('files referenced more than once', dupf)

nonascii = [(i + 1, c) for i, ch in enumerate(txt) for c in [ch] if ord(c) > 127]
print('non-ascii chars', len(nonascii), nonascii[:5])

print('sections', re.findall(r'^## (.+)$', txt, flags=re.M))
print('empty what/std cells', [r[0] for r in rows if not r[2].strip() or not r[3].strip()])

# tracker cross-check: every planned new file that exists must be listed
import openpyxl
p = os.path.join(ROOT, r'15 ACE DB Alignment\Recovery Workbench ACE DB Alignment Tracker v1.xlsx')
ws = openpyxl.load_workbook(p)['Documents']
notlisted = []
for r in ws.iter_rows(min_row=2, max_row=ws.max_row, values_only=True):
    new = r[3].strip()
    if new in disk and new not in files:
        notlisted.append((r[0], new))
print('planned new files existing but not listed', notlisted)
