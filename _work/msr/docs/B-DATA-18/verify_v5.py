"""Verify v5 against v4: every v4 cell identical except the recorded change."""
import json

import openpyxl

V4 = "06 Data/Recovery Workbench Source to Target Mapping v4.xlsx"
V5 = "06 Data/Recovery Workbench Source to Target Mapping v5.xlsx"

a = openpyxl.load_workbook(V4)
b = openpyxl.load_workbook(V5)

assert b.sheetnames == ["Read me"] + a.sheetnames, b.sheetnames
problems = []
changed = []
for name in a.sheetnames:
    wa, wb = a[name], b[name]
    if (wa.max_row, wa.max_column) != (wb.max_row, wb.max_column):
        if name != "Mapping rules" and name != "Mapping" and name != "ACE gaps":
            problems.append(f"{name}: size changed {wa.max_row}x{wa.max_column} -> {wb.max_row}x{wb.max_column}")
    for r in range(1, wa.max_row + 1):
        for c in range(1, wa.max_column + 1):
            va = wa.cell(row=r, column=c).value
            vb = wb.cell(row=r, column=c).value
            if va != vb:
                changed.append((name, wa.cell(row=r, column=1).value, wa.cell(row=1, column=c).value, va, vb))

print("changed v4 cells:", len(changed))
for x in changed:
    print(" ", x)

# mapping target schema distribution
m = b["Mapping"]
dist = {}
for r in range(2, m.max_row + 1):
    key = (m.cell(row=r, column=15).value, m.cell(row=r, column=16).value)
    dist[key] = dist.get(key, 0) + 1
print("target schema distribution:", json.dumps({f"{k[0]} / {k[1]}": v for k, v in sorted(dist.items())}, indent=1))
print("mapping rows", m.max_row - 1, "sum", sum(dist.values()))
missing = [r for r in range(2, m.max_row + 1) if not m.cell(row=r, column=15).value]
print("rows without target schema:", missing)

g = b["ACE gaps"]
print("ace gaps rows", g.max_row - 1, "cols 9/10 filled:",
      sum(1 for r in range(2, g.max_row + 1) if g.cell(row=r, column=9).value and g.cell(row=r, column=10).value))

bs = b["By source"]
for r in range(2, bs.max_row + 1):
    if bs.cell(row=r, column=1).value == "Aric via COLLINS":
        print("Aric row:", [bs.cell(row=r, column=c).value for c in range(1, 9)])

mr = b["Mapping rules"]
print("rules rows", mr.max_row - 1)

rm = b["Read me"]
print("Read me first two:", rm["A1"].value, "|", rm["A2"].value)
print("Read me change log:", rm["A9"].value)
print("problems:", problems)
