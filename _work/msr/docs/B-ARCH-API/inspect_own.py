import json
from pathlib import Path
import openpyxl
ROOT = Path(__file__).resolve().parents[4]
p = ROOT / "22 Microservice Realignment" / "Recovery Workbench Microservice Ownership Map v1.xlsx"
wb = openpyxl.load_workbook(p, data_only=True)
print(wb.sheetnames)
for ws in wb.worksheets:
    print("==", ws.title, ws.max_row, ws.max_column)
    for r in ws.iter_rows(min_row=1, max_row=3, values_only=True):
        print("   ", r)
