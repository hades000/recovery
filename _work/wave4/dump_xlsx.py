import sys, openpyxl
p = sys.argv[1]
wb = openpyxl.load_workbook(p, data_only=False)
for ws in wb.worksheets:
    print("="*80)
    print("SHEET:", repr(ws.title), "dims", ws.dimensions, "max_row", ws.max_row, "max_col", ws.max_column)
    print("merged:", [str(m) for m in ws.merged_cells.ranges])
    for row in ws.iter_rows(min_row=1, max_row=min(ws.max_row, 200)):
        vals = []
        for c in row:
            if c.value is not None:
                vals.append("%s=%r" % (c.coordinate, c.value))
        if vals:
            print(" | ".join(vals))
