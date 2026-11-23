import openpyxl

p = r"22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx"
wb = openpyxl.load_workbook(p)
print("SHEETS:", wb.sheetnames)
for ws in wb.worksheets:
    print("=== ", ws.title, ws.max_row, ws.max_column)
    for r in range(1, min(ws.max_row, 4) + 1):
        print("   ", [ws.cell(row=r, column=c).value for c in range(1, min(ws.max_column, 8) + 1)])
ws = wb["Services"]
print("--- services")
for r in range(1, ws.max_row + 1):
    print([ws.cell(row=r, column=c).value for c in range(1, 7)])
