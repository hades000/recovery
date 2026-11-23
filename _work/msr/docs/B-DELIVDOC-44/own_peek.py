import openpyxl
wb = openpyxl.load_workbook("22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx", data_only=True)
print("SHEETS:", wb.sheetnames)
for ws in wb.worksheets:
    print("==", ws.title, ws.max_row, ws.max_column)
    for row in ws.iter_rows(min_row=1, max_row=min(6, ws.max_row), values_only=True):
        print("   ", row)
