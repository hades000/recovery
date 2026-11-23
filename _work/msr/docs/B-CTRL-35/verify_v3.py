import json
import openpyxl

SRC = r"10 Policy, controls and compliance/Recovery Workbench Regulatory Requirements Map v2.xlsx"
DST = r"10 Policy, controls and compliance/Recovery Workbench Regulatory Requirements Map v3.xlsx"
a = openpyxl.load_workbook(SRC)
b = openpyxl.load_workbook(DST)

print("v2 sheets:", a.sheetnames)
print("v3 sheets:", b.sheetnames)

# Obligations A-H identical
oa, ob = a["Obligations"], b["Obligations"]
bad = []
for r in range(1, 37):
    for c in range(1, 9):
        va, vb = oa.cell(row=r, column=c).value, ob.cell(row=r, column=c).value
        if r == 3:
            continue
        if va != vb:
            bad.append((oa.cell(row=r, column=c).coordinate, va, vb))
print("Obligations A-H diffs (row 3 excluded):", bad)

# By source / By process identical
for name in ("By source", "By process"):
    wa, wb2 = a[name], b[name]
    d = [(r, c) for r in range(1, wa.max_row + 1) for c in range(1, wa.max_column + 1)
         if wa.cell(row=r, column=c).value != wb2.cell(row=r, column=c).value]
    print(name, "max_row", wa.max_row, wb2.max_row, "diffs:", d)

# Key
ka, kb = a["Key"], b["Key"]
print("Key diffs rows1-8:", [(r, c) for r in range(1, 9) for c in range(1, 4)
                             if ka.cell(row=r, column=c).value != kb.cell(row=r, column=c).value])
print("Key rows 9-10:", [[kb.cell(row=r, column=c).value for c in range(1, 4)] for r in (9, 10)])

# Obligations new columns
print("row3:", ob["A3"].value)
print("headers I/J:", ob["I4"].value, "|", ob["J4"].value)
for r in range(5, 37):
    print(ob.cell(row=r, column=1).value, "=>", ob.cell(row=r, column=9).value)
print("autofilter:", ob.auto_filter.ref, "freeze:", ob.freeze_panes)

# By service
bs = b["By service"]
print("--- By service")
for r in range(1, bs.max_row + 1):
    print(r, [bs.cell(row=r, column=c).value for c in range(1, 9)])

print("--- properties")
pr = b.properties
print(pr.creator, "|", pr.lastModifiedBy, "|", pr.title, "|", pr.subject)
print("--- person name scan")
hit = []
for ws in b.worksheets:
    for row in ws.iter_rows():
        for c in row:
            if isinstance(c.value, str) and ("Rajdeep" in c.value or "Ghai" in c.value):
                hit.append(c.coordinate)
print("hits:", hit)
