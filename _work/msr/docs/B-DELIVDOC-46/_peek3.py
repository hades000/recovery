import openpyxl
wb = openpyxl.load_workbook(r"22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx", data_only=True)
print(wb.sheetnames)
for s in wb.sheetnames:
    ws = wb[s]
    print("===", s, ws.max_row, ws.max_column)
    for r in ws.iter_rows(min_row=1, max_row=min(4, ws.max_row), values_only=True):
        print([str(c)[:40] if c is not None else "" for c in r])
