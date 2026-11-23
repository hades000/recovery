import openpyxl
p = r"05 Technical architecture/Recovery Workbench Service Catalog v1.xlsx"
wb = openpyxl.load_workbook(p, data_only=True)
ws = wb["Resources"]
print("Resources rows:", ws.max_row)
for r in ws.iter_rows(min_row=ws.max_row - 7, values_only=True):
    print([("" if c is None else str(c))[:70] for c in r])
print("sheets:", wb.sheetnames)
ws = wb["Events published"]
for r in ws.iter_rows(min_row=2, values_only=True):
    if r[2] in ("ApprovalDecided", "ReportPublished"):
        print(r[0], r[2], "->", r[4])
