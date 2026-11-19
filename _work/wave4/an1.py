import openpyxl, collections, re
p = r"11 Delivery and operations\Recovery Workbench Build Sequence Epic 1 and Epic 2 v4.xlsx"
wb = openpyxl.load_workbook(p, data_only=True)
ws = wb["Sequence"]
rows = []
for r in range(5, ws.max_row+1):
    rows.append([ws.cell(r,c).value for c in range(1,12)])
print("n rows", len(rows))
by = collections.Counter()
for r in rows:
    by[r[4]] += 1
print(by)
print("E1", sum(1 for r in rows if r[1].startswith("RWB-E1")))
print("E2", sum(1 for r in rows if r[1].startswith("RWB-E2")))
print("TE", sum(1 for r in rows if r[1].startswith("RWB-TE")))
print("windows", collections.Counter(r[7] for r in rows))
print("E1 in window1:", [r[1] for r in rows if r[7]=='Window 1' and r[1].startswith('RWB-E1')])
print("critical:", [r[1] for r in rows if r[10]])
