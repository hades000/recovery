import openpyxl
p = r"05 Technical architecture/Recovery Workbench Service Catalog v1.xlsx"
wb = openpyxl.load_workbook(p, data_only=True)
for ws in wb.worksheets:
    print("==", ws.title, ws.max_row, ws.max_column)
    for r in list(ws.iter_rows(values_only=True))[:3]:
        print("   ", [("" if c is None else str(c))[:60] for c in r])
