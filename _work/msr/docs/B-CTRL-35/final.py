import openpyxl, os
p2 = r"10 Policy, controls and compliance/Recovery Workbench Regulatory Requirements Map v2.xlsx"
p3 = r"10 Policy, controls and compliance/Recovery Workbench Regulatory Requirements Map v3.xlsx"
print("v2 size", os.path.getsize(p2), "| v3 size", os.path.getsize(p3))
wb = openpyxl.load_workbook(p3)
o = wb["Obligations"]
print("rows 5-36 filled:", all(o.cell(row=r, column=9).value and o.cell(row=r, column=10).value for r in range(5, 37)))
print("row36:", o.cell(row=36, column=1).value, "|", o.cell(row=36, column=9).value)
k = wb["Key"]
print("key rows:", [k.cell(row=r, column=1).value for r in range(4, k.max_row + 1)], k.max_row)
rm = wb["Read me"]
print("rm row1/2 ok:", rm["A1"].value.startswith("SCB Collections and Recovery. Henka Group, 22 November 2026."), rm["A2"].value == "(C) Siam Commercial Bank and Henka Pte Ltd")
found = any("3, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash" == c.value
            for row in rm.iter_rows() for c in row)
print("change-log string present:", found)
bs = wb["By service"]
print("by service data rows:", bs.max_row, "| sum E:", bs["E20"].value, "| sum G:", bs["G20"].value)
