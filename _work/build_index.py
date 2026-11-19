import openpyxl, re, os, io

ROOT = r'C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14'
IDX = os.path.join(ROOT, r'12 Project communication\Recovery Workbench Document Index v11.md')

# --- tracker map ---
p = os.path.join(ROOT, r'15 ACE DB Alignment\Recovery Workbench ACE DB Alignment Tracker v1.xlsx')
ws = openpyxl.load_workbook(p)['Documents']
MAP = {}
for r in ws.iter_rows(min_row=2, max_row=ws.max_row, values_only=True):
    if r[2] != '(new)':
        MAP[r[2].strip()] = r[3].strip()

# --- disk ---
disk = set()
for folder in os.listdir(ROOT):
    fp = os.path.join(ROOT, folder)
    if os.path.isdir(fp):
        for f in os.listdir(fp):
            disk.add(f)

def latest(base):
    m = re.match(r'^(.*) v(\d+)\.(\w+)$', base)
    if not m:
        return None
    stem, ext = m.group(1), m.group(3)
    c = []
    for f in disk:
        mm = re.match(r'^' + re.escape(stem) + r' v(\d+)\.' + re.escape(ext) + r'$', f)
        if mm:
            c.append((int(mm.group(1)), f))
    return max(c)[1] if c else None

fallbacks = {}
def resolve(name):
    name = name.strip()
    new = MAP.get(name, name)
    if new in disk:
        return new
    alt = latest(new)
    if alt:
        fallbacks[name] = (new, alt)
        return alt
    if name in disk:
        return name
    return new

src = open(IDX, encoding='utf-8').read()
out_lines = []
row_re = re.compile(r'^\| (\d+) \| (.+?) \| (.+?) \| (.+?) \| (.+?) \|$')

for line in src.split('\n'):
    m = row_re.match(line.rstrip('\r'))
    if m:
        rid, doc, what, std, files = m.groups()
        names = [x.strip() for x in files.split(',')]
        mapped = [resolve(n) for n in names]
        line = '| %s | %s | %s | %s | %s |' % (rid, doc, what, std, ', '.join(mapped))
    out_lines.append(line)

txt = '\n'.join(out_lines)
txt = txt.replace('SCB Collections and Recovery. Henka Group, 2 November 2026.',
                  'SCB Collections and Recovery. Henka Group, 15 November 2026.')
txt = txt.replace(
    'Every asset in the document set, who reads it and the file that holds it. Functional and technical specifications are one file per module, in the two specification archives.',
    'Every asset in the document set at its current version, who reads it and the file that holds it. Functional and technical specifications are one file per module, in the two specification archives. The ACE DB alignment pack in section 15 is the controlling change for the 15 November 2026 re-base, recorded as D-RCV-35.')

# --- new section after Data ---
anchor = '\n## Technical\n'
new_sec = '''
## ACE DB alignment

Read by: Data architect, ACE team, recovery tech lead, data engineering.

| # | Document | What it is | Standard | Files |
|---|---|---|---|---|
| 124 | ACE DB alignment change register | The decision record for the re-base on the ACE database: decisions U1 to U5 as D-RCV-35, the document edit plan, the story disposition and the defects found. The controlling document for the pack. | MADR | Recovery Workbench ACE DB Alignment Change Register v1.md |
| 125 | ACE data tier map | The frozen table and column map: which ACE tables are read as they are, which the ACE team adds, which extension tables the Workbench owns, which tables leave, and every re-keyed foreign key. | ISO/IEC/IEEE 29148, bank TSD section T3 | Recovery Workbench ACE Data Tier Map v1.md |
| 126 | ACE field gap list | All 133 external fields with their disposition, the 80 fields the ACE team must add, mapped to table and column, with the reconciliation of the counts. | Henka excel rules | Recovery Workbench ACE Field Gap List v1.xlsx |
| 127 | ACE source views | The 30 read-only v_ace_* view definitions, the helper functions, the grants and the conformance test, in two sections: one over ACE tables that exist today, one over the ACE additions. | ISO/IEC/IEEE 29148, bank TSD section T3 | Recovery Workbench ACE Source Views v1.sql |
| 128 | ACE schema DDL and extract | The 62 ACE tables as runnable PostgreSQL DDL, generated from the ACE workbook, with a 547-row extract, one row per ACE column, for grep and agent use. | ISO/IEC/IEEE 29148 | ACE Schema PostgreSQL v1.sql, ACE Schema Extract v1.csv, ACE-data-schema_20261104.xlsx |
| 129 | ACE DB alignment tracker | The working list for the alignment: 82 documents with size, wave, owner and status, 334 stories with their disposition, the 9 decisions and the 4 defects. | Henka excel rules | Recovery Workbench ACE DB Alignment Tracker v1.xlsx |
'''
txt = txt.replace(anchor, new_sec + anchor, 1)

# --- ACE team stories row in Backlog, after row 55 ---
lines = txt.split('\n')
for i, line in enumerate(lines):
    if line.startswith('| 55 | User stories, Epic 2 |'):
        lines.insert(i + 1, '| 130 | ACE team stories | RWB-ACE-001, the one story the ACE team builds: the 14 new tables, the 12 new columns and the 80-row field appendix, with acceptance criteria on population, freshness and reversibility. | Connextra form, INVEST, Gherkin | Recovery Workbench ACE Team Stories v1.md, Recovery Workbench ACE Team Stories v1.xlsx |')
        break
else:
    raise SystemExit('row 55 anchor not found')
txt = '\n'.join(lines)

dst = os.path.join(ROOT, r'12 Project communication\Recovery Workbench Document Index v12.md')
open(dst, 'w', encoding='utf-8', newline='\n').write(txt)

print('written', dst)
print('fallbacks (target missing, used latest on disk):')
for k, v in fallbacks.items():
    print('  ', k, '->', v[0], '(missing) => using', v[1])
