import openpyxl

p = r"10 Policy, controls and compliance/Recovery Workbench Regulatory Requirements Map v2.xlsx"
wb = openpyxl.load_workbook(p)
ws = wb["Obligations"]
for coord in ("A5", "F5", "H5"):
    c = ws[coord]
    print(coord, "font", c.font.b, c.font.sz, c.font.color.rgb if c.font.color else None,
          "| fill", c.fill.patternType, "| align", c.alignment.wrap_text, c.alignment.vertical,
          "| numfmt", c.number_format)
print("row heights:", {r: ws.row_dimensions[r].height for r in range(1, 10)})
print("sheet_state:", [(s.title, s.sheet_state) for s in wb.worksheets])
print("tab colors:", [(s.title, s.sheet_properties.tabColor) for s in wb.worksheets])
print("default row height:", ws.sheet_format.defaultRowHeight)
