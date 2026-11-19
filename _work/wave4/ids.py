import sys, openpyxl, re
p = sys.argv[1]
wb = openpyxl.load_workbook(p, data_only=True)
for ws in wb.worksheets:
    print("SHEET:", repr(ws.title), ws.dimensions)
    hdr = [c.value for c in ws[1]]
    print("HDR1:", hdr)
    hdr2 = [c.value for c in ws[2]]
    print("HDR2:", hdr2)
    print("rows", ws.max_row)
    # collect ids
    ids = []
    for r in range(1, ws.max_row+1):
        for c in range(1, min(ws.max_column, 4)+1):
            v = ws.cell(r, c).value
            if isinstance(v, str) and re.match(r"^RWB-[A-Z0-9]+-\d+$", v.strip()):
                ids.append(v.strip()); break
    print("n ids", len(ids))
    print(ids)
