import openpyxl

p = r"10 Policy, controls and compliance/Recovery Workbench Controls Catalog v4.xlsx"
wb = openpyxl.load_workbook(p)
ws = wb["Controls"]
print("CTL | obligations(column L) | owner")
for r in range(5, ws.max_row + 1):
    cid = ws.cell(row=r, column=1).value
    if cid and str(cid).startswith("CTL"):
        print(cid, "|", ws.cell(row=r, column=12).value, "|", ws.cell(row=r, column=15).value)
