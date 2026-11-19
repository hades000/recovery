import re, os, collections
import openpyxl

ROOT = r'C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14'
IDX = os.path.join(ROOT, r'12 Project communication\Recovery Workbench Document Index v12.md')
CS = os.path.join(ROOT, r'12 Project communication\Recovery Workbench Document Control Sheet v11.xlsx')

disk = set()
for folder in os.listdir(ROOT):
    fp = os.path.join(ROOT, folder)
    if os.path.isdir(fp):
        disk.update(os.listdir(fp))

row_re = re.compile(r'^\| (\d+) \| (.+?) \| (.+?) \| (.+?) \| (.+?) \|$')
idx = {}
for line in open(IDX, encoding='utf-8').read().split('\n'):
    m = row_re.match(line)
    if m:
        idx[int(m.group(1))] = (m.group(2), m.group(5))

print('== index ==')
print('rows', len(idx), 'ids 1..132 complete:', sorted(idx) == list(range(1, 133)))
print('sections', len(re.findall(r'^## ', open(IDX, encoding='utf-8').read(), re.M)))
files = [f.strip() for _, v in idx.items() for f in v[1].split(',')]
print('file refs', len(files), 'missing', [f for f in files if f not in disk])
print('dupes', [f for f, c in collections.Counter(files).items() if c > 1])
print('non-ascii', any(ord(ch) > 127 for ch in open(IDX, encoding='utf-8').read()))

print('== control sheet ==')
wb = openpyxl.load_workbook(CS)
ws = wb['Control sheet']
print('max_row', ws.max_row, 'autofilter', ws.auto_filter.ref)
rows = [[ws.cell(row=r, column=c).value for c in range(1, 12)] for r in range(5, ws.max_row + 1)]
print('data rows', len(rows))
cids = [r[0] for r in rows]
print('ids match index:', sorted(cids) == list(range(1, 133)), 'dupes', [i for i, c in collections.Counter(cids).items() if c > 1])
badf = [(r[0], r[4]) for r in rows if r[4] != idx[r[0]][1]]
print('files differ from index', badf)
badd = [(r[0], r[3], idx[r[0]][0]) for r in rows if r[3] != idx[r[0]][0]]
print('names differ from index', len(badd), badd)
print('first row', rows[0][:6])
print('priorities', collections.Counter(r[1] for r in rows))
print('empty pri/layer/rev/sign', [r[0] for r in rows if not all([r[1], r[2], r[3], r[4], r[5], r[6]])])
print('status values', collections.Counter(r[8] for r in rows))
print('comments row', [(r[0], r[10]) for r in rows if r[10]])
print('A2', ws['A2'].value)
sm = wb['Summary']
for r in range(4, 9):
    print('S', [sm.cell(row=r, column=c).value for c in range(1, 5)])
print('DV', [(str(dv.sqref), dv.formula1) for dv in ws.data_validations.dataValidation])
print('sheets', wb.sheetnames)

