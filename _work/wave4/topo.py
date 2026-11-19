import openpyxl
p = r"11 Delivery and operations\Recovery Workbench Build Sequence Epic 1 and Epic 2 v5.xlsx"
wb = openpyxl.load_workbook(p, data_only=True)
ws = wb["Sequence"]
pos = {}
rows = []
for r in range(5, ws.max_row + 1):
    key = ws.cell(r, 2).value
    dep = ws.cell(r, 7).value or ""
    pos[key] = r - 4
    rows.append((r, key, dep))
print("forward refs:")
for r, key, dep in rows:
    for d in [x.strip() for x in dep.split(",") if x.strip()]:
        if d in pos and pos[d] > pos[key]:
            print("  ", key, pos[key], "->", d, pos[d])
print("unknown deps:")
known = set(pos)
for r, key, dep in rows:
    for d in [x.strip() for x in dep.split(",") if x.strip()]:
        if d not in known:
            print("  ", key, "->", d)
