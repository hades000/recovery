import openpyxl

p = r"10 Policy, controls and compliance/Recovery Workbench Regulatory Requirements Map v2.xlsx"
wb = openpyxl.load_workbook(p)
print("SHEETS:", wb.sheetnames)
pr = wb.properties
print("props creator=", pr.creator, "| lastMod=", pr.lastModifiedBy, "| title=", pr.title, "| subject=", pr.subject, "| desc=", pr.description, "| created=", pr.created, "| modified=", pr.modified)
for ws in wb.worksheets:
    print("=== SHEET", ws.title, "dims", ws.dimensions, "max_row", ws.max_row, "max_col", ws.max_column)
    print("  merged:", [str(m) for m in ws.merged_cells.ranges])
    print("  freeze:", ws.freeze_panes, "autofilter:", ws.auto_filter.ref)
    print("  col widths:", {k: v.width for k, v in ws.column_dimensions.items()})
    for row in ws.iter_rows(min_row=1, max_row=min(ws.max_row, 5)):
        print("  ", [(c.coordinate, (str(c.value)[:38] if c.value is not None else None)) for c in row])
