"""Compact table -> owner map from the Ownership Map."""
import collections
import openpyxl

OWN = "22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx"
wb = openpyxl.load_workbook(OWN)
ws = wb["Tables"]
rows = []
for r in range(2, ws.max_row + 1):
    t = ws.cell(row=r, column=1).value
    if not t:
        continue
    rows.append((str(t), str(ws.cell(row=r, column=2).value), str(ws.cell(row=r, column=3).value)))
print("tables", len(rows))
cnt = collections.Counter(o for _, o, _ in rows)
print(cnt)
for o in sorted(cnt, key=lambda x: (x[0], 0 if not x[1:].isdigit() else int(x[1:]))):
    names = [t for t, ow, _ in rows if ow == o]
    print(o, len(names), ", ".join(names))
