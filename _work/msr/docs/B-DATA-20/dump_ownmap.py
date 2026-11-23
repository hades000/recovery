"""Dump the Ownership Map workbook."""
import openpyxl

OWN = "22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx"
wb = openpyxl.load_workbook(OWN)
print(wb.sheetnames)
for ws in wb.worksheets:
    print("=" * 100)
    print(ws.title, ws.dimensions)
    for r in range(1, ws.max_row + 1):
        vals = [("" if ws.cell(row=r, column=c).value is None else str(ws.cell(row=r, column=c).value))
                for c in range(1, ws.max_column + 1)]
        print(r, " | ".join(vals))
