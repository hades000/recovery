import openpyxl

p = r"10 Policy, controls and compliance/Recovery Workbench Regulatory Requirements Map v3.xlsx"
wb = openpyxl.load_workbook(p)
print("active:", wb.active.title)
rm = wb["Read me"]
for r in range(1, rm.max_row + 1):
    vals = [rm.cell(row=r, column=c).value for c in range(1, 5)]
    if any(v is not None for v in vals):
        print(r, vals)
print("--- Realignment changes")
rc = wb["Realignment changes"]
for r in range(1, rc.max_row + 1):
    print(r, [rc.cell(row=r, column=c).value for c in range(1, 5)])
print("widths A/B:", rm.column_dimensions["A"].width, rm.column_dimensions["B"].width)
