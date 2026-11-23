import openpyxl, json
p = "22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx"
wb = openpyxl.load_workbook(p)
print(wb.sheetnames)
for ws in wb.worksheets:
    print("===", ws.title, ws.max_row, ws.max_column)
    for r in ws.iter_rows(min_row=1, max_row=min(ws.max_row, 8), values_only=True):
        print([str(c)[:50] if c is not None else "" for c in r])
