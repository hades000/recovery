import sys
import openpyxl

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
wb = openpyxl.load_workbook("06 Data/Recovery Workbench Source to Target Mapping v5.xlsx")
g = wb["ACE gaps"]
for r in range(2, g.max_row + 1):
    if g.cell(row=r, column=1).value == "DF-LEG-006":
        print("DF-LEG-006:", [g.cell(row=r, column=c).value for c in range(1, 11)])
mr = wb["Mapping rules"]
print("---- rules")
for r in range(11, mr.max_row + 1):
    print(r, "|", mr.cell(row=r, column=1).value, "|", str(mr.cell(row=r, column=2).value)[:80])
