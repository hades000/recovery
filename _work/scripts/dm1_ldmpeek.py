import openpyxl
from collections import Counter
wb = openpyxl.load_workbook(r'06 Data/Recovery Workbench Logical Data Model and Data Dictionary v7.xlsx')
print(wb.properties.title, wb.properties.modified, wb.properties.creator)
f = [r for r in wb['Fields'].iter_rows(min_row=5, values_only=True) if r[0]]
ents = {r[0]: r for r in wb['Entities'].iter_rows(min_row=5, values_only=True) if r[0]}
c = Counter()
for r in f:
    if not r[1].startswith('v_ace_') and not r[1].endswith('_ext') and r[11] != 'Workbench':
        c[r[1]] += 1; print(r[0], r[1], r[2], r[11], r[12])
print(sum(c.values()), c)
print(Counter(r[11] for r in f))
for r in wb['Loaded lists'].iter_rows(values_only=True): print(r)
lv = [r for r in wb['Lists of values'].iter_rows(min_row=5, values_only=True) if r[0]]
print(len(lv), len(set(r[0] for r in lv)))
for r in lv:
    if r[0] in ('LOV-INTERFACE-RUN','LOV-TRANSPORT','LOV-LOAD-STATUS'): print(r)
print(wb['Fields'].max_column, [wb['Fields'].cell(row=4,column=i).value for i in range(1,17)])
print([ (ws.title, ws.max_row, ws.max_column) for ws in wb])
