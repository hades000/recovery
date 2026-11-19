import re, os, shutil
from copy import copy
import openpyxl

ROOT = r'C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14'
IDX = os.path.join(ROOT, r'12 Project communication\Recovery Workbench Document Index v12.md')
SRC = os.path.join(ROOT, r'12 Project communication\Recovery Workbench Document Control Sheet v10.xlsx')
DST = os.path.join(ROOT, r'12 Project communication\Recovery Workbench Document Control Sheet v11.xlsx')

# --- index rows ---
row_re = re.compile(r'^\| (\d+) \| (.+?) \| (.+?) \| (.+?) \| (.+?) \|$')
IDXROWS = {}
for line in open(IDX, encoding='utf-8').read().split('\n'):
    m = row_re.match(line)
    if m:
        IDXROWS[int(m.group(1))] = (m.group(2), m.group(5))

shutil.copyfile(SRC, DST)
wb = openpyxl.load_workbook(DST)
ws = wb['Control sheet']

LAST = ws.max_row          # 127
data = []
for r in range(5, LAST + 1):
    vals = [ws.cell(row=r, column=c).value for c in range(1, 12)]
    data.append((vals, ws.row_dimensions[r].height or 29.6))
TEMPLATE = [copy(ws.cell(row=5, column=c)._style) for c in range(1, 12)]

# --- update existing rows from the index ---
mismatch = []
for vals, h in data:
    rid = int(vals[0])
    vals[0] = rid
    if rid not in IDXROWS:
        raise SystemExit('id %s in control sheet but not in index' % rid)
    doc, files = IDXROWS[rid]
    if vals[3] != doc:
        mismatch.append((rid, vals[3], doc))
    vals[4] = files
if mismatch:
    print('document-name differences (control sheet kept):')
    for m in mismatch:
        print('  ', m)

NEW = {
 124: ('1. Build start', 'Control', 'Data architect, recovery tech lead, ACE team lead', 'SCB sponsor'),
 125: ('1. Build start', 'Data', 'SCB data steward, ACE team, TechX', 'SCB data owner'),
 126: ('1. Build start', 'Data', 'SCB data steward, ACE team, TechX', 'SCB data owner'),
 127: ('1. Build start', 'Technical', 'SCB IT architecture, ACE team, TechX', 'SCB IT architecture'),
 128: ('1. Build start', 'Technical', 'SCB IT architecture, ACE team, TechX', 'SCB IT architecture'),
 129: ('3. Supporting', 'Data', 'SCB data steward, ACE team, TechX', 'SCB data owner'),
 130: ('1. Build start', 'Backlog', 'TechX squads; SCB business leads for acceptance criteria', 'SCB product owner'),
 131: ('2. Business sign-off', 'Decisions', 'Sponsors and decision owners', 'SCB sponsor'),
 132: ('2. Business sign-off', 'Decisions', 'Sponsors and decision owners', 'SCB sponsor'),
}

rows = []
for vals, h in data:
    if vals[2] == 'Control':
        vals[10] = 'Controlling row: D-RCV-35 (U1 to U5), signed 15 November 2026. Every other row in this sheet is read against this register.'
    rows.append((int(vals[0]), vals, h))

for rid, (pri, layer, rev, sign) in NEW.items():
    doc, files = IDXROWS[rid]
    vals = [rid, pri, layer, doc, files, rev, sign, None, 'Not started', None, '']
    h = 42.4 if (len(files) > 58 or rid == 124) else 29.6
    if rid == 124:
        vals[10] = 'Controlling row: D-RCV-35 (U1 to U5), signed 15 November 2026. Every other row in this sheet is read against this register.'
    rows.append((rid, vals, h))

RANK = {'1. Build start': 1, '2. Business sign-off': 2, '3. Supporting': 3}
rows.sort(key=lambda x: (0 if x[0] == 124 else 1, RANK[x[1][1]], x[0]))

# --- rewrite ---
for i, (rid, vals, h) in enumerate(rows):
    r = 5 + i
    for c in range(1, 12):
        cell = ws.cell(row=r, column=c)
        cell._style = copy(TEMPLATE[c - 1])
        cell.value = vals[c - 1]
    ws.row_dimensions[r].height = h

last_row = 4 + len(rows)

ws['A2'] = ('%d documents in upload order. Update the SharePoint, review and sign-off columns as each moves. '
            'The controlling row is the ACE DB alignment change register, D-RCV-35, signed 15 November 2026.' % len(rows))
ws.auto_filter.ref = 'A4:K%d' % last_row

# extend the two existing drop-downs to the new last row
for dv in ws.data_validations.dataValidation:
    col = str(dv.sqref).split(':')[0][0]
    dv.sqref = openpyxl.worksheet.cell_range.MultiCellRange('%s5:%s%d' % (col, col, last_row))

# summary ranges
sm = wb['Summary']
for r in range(5, 8):
    for c in range(2, 5):
        cell = sm.cell(row=r, column=c)
        cell.value = cell.value.replace('$127', '$%d' % last_row)

wb.save(DST)
print('saved', DST, 'rows', len(rows), 'last row', last_row)

