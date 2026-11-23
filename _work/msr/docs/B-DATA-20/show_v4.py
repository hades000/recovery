"""Print the v4 workbook for review."""
import openpyxl

V4 = "06 Data/Recovery Workbench Data Ownership and Stewardship v4.xlsx"
wb = openpyxl.load_workbook(V4)
for ws in wb.worksheets:
    print("=" * 100)
    print(ws.title, ws.dimensions, "freeze", ws.freeze_panes, "filter", ws.auto_filter.ref)
    for r in range(1, ws.max_row + 1):
        vals = [("" if ws.cell(row=r, column=c).value is None else str(ws.cell(row=r, column=c).value))
                for c in range(1, ws.max_column + 1)]
        if any(vals):
            print(r, " | ".join(vals))
