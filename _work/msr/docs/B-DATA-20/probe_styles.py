"""Probe styles of the copied v4 workbook."""
import openpyxl

V4 = "06 Data/Recovery Workbench Data Ownership and Stewardship v4.xlsx"
wb = openpyxl.load_workbook(V4)
for name in wb.sheetnames:
    ws = wb[name]
    print("==", name, ws.dimensions, ws.sheet_view.showGridLines)
    for r in (1, 2, 4, 5):
        c = ws.cell(row=r, column=1)
        print("  row", r, "font", c.font.b, c.font.sz, c.font.color.rgb if c.font.color else None,
              "fill", c.fill.fgColor.rgb if c.fill and c.fill.fgColor else None,
              "align", c.alignment.wrap_text, c.alignment.vertical)
    print("  widths", {k: v.width for k, v in ws.column_dimensions.items()})
    print("  freeze", ws.freeze_panes, "autofilter", ws.auto_filter.ref)
