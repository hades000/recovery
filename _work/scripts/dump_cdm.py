import io
import openpyxl

p = r'06 Data\Recovery Workbench Conceptual Data Model v5.xlsx'
wb = openpyxl.load_workbook(p, data_only=True)
out = io.open(r'_work\analysis\cdm.txt', 'w', encoding='utf-8')
out.write('sheets: %s\n' % wb.sheetnames)
for ws in wb.worksheets:
    out.write('\n=== %s (%d x %d) ===\n' % (ws.title, ws.max_row, ws.max_column))
    for r in ws.iter_rows(values_only=True):
        if any(c is not None for c in r):
            out.write('|'.join(str(c) if c is not None else '' for c in r) + '\n')
out.close()

# ACE column distribution in LDM entities
wb2 = openpyxl.load_workbook(r'06 Data\Recovery Workbench Logical Data Model and Data Dictionary v6.xlsx', data_only=True)
ws = wb2['Entities']
from collections import Counter
c = Counter()
rows = [r for r in ws.iter_rows(min_row=5, values_only=True) if r[0]]
for r in rows:
    c[str(r[6])] += 1
print(c)
