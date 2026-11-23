import openpyxl

p = r"10 Policy, controls and compliance/Recovery Workbench Controls Catalog v4.xlsx"
wb = openpyxl.load_workbook(p)
print("SHEETS:", wb.sheetnames)
ws = wb["Controls"]
for r in range(1, 6):
    print(r, [ws.cell(row=r, column=c).value for c in range(1, 17)])
print("---- CTL to owner")
for r in range(5, ws.max_row + 1):
    a = ws.cell(row=r, column=1).value
    if a and str(a).startswith("CTL"):
        print(ws.cell(row=r, column=1).value, "|", ws.cell(row=r, column=2).value, "|", str(ws.cell(row=r, column=15).value), "|", str(ws.cell(row=r, column=16).value)[:160])
print("---- By owner service")
if "By owner service" in wb.sheetnames:
    w = wb["By owner service"]
    for r in range(1, w.max_row + 1):
        print(r, [w.cell(row=r, column=c).value for c in range(1, 7)])
