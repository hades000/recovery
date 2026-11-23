"""C-DEF scratch: put the Realignment v5 sheet first and set its column widths.

Touches only the v5 output this WP created; the copied Defects sheet is left alone.
"""
from pathlib import Path

import openpyxl

ROOT = Path(__file__).resolve().parents[4]
DST = ROOT / "04 User stories" / "Recovery Workbench Story Defects Epic 1 Epic 2 and Enablers v5.xlsx"
SRC = ROOT / "04 User stories" / "Recovery Workbench Story Defects Epic 1 Epic 2 and Enablers v4.xlsx"

wb = openpyxl.load_workbook(DST)
ws = wb["Realignment v5"]
if wb.sheetnames[0] != "Realignment v5":
    wb.move_sheet(ws, offset=-(wb.sheetnames.index("Realignment v5")))
for col, width in {"A": 10, "B": 24, "C": 9, "D": 46, "E": 46, "F": 14, "G": 26, "H": 52, "I": 30, "J": 90}.items():
    ws.column_dimensions[col].width = width
ws.freeze_panes = "A18"
wb.active = 0
wb.save(DST)

# confirm the copied Defects sheet still matches v4 cell for cell
a = openpyxl.load_workbook(SRC, data_only=True)["Defects"]
b = openpyxl.load_workbook(DST, data_only=True)["Defects"]
diff = []
for r in range(1, max(a.max_row, b.max_row) + 1):
    for c in range(1, max(a.max_column, b.max_column) + 1):
        if a.cell(row=r, column=c).value != b.cell(row=r, column=c).value:
            diff.append((r, c))
print("sheets", openpyxl.load_workbook(DST, data_only=True).sheetnames)
print("defects rows", b.max_row, "diffs", diff[:5], len(diff))
print("realignment rows", ws.max_row)
