import openpyxl

wb = openpyxl.load_workbook("06 Data/Recovery Workbench Source to Target Mapping v5.xlsx")
rm = wb["Read me"]
print("---- Read me")
for r in range(1, rm.max_row + 1):
    v = rm.cell(row=r, column=1).value
    print(f"{r:>2}: {v}")

m = wb["Mapping"]
print("---- Mapping header")
print([m.cell(row=1, column=c).value for c in range(1, 17)])
print("---- sample rows")
for r in (2, 20, 60, 120, 134):
    print([m.cell(row=r, column=c).value for c in (1, 3, 4, 10, 15, 16)])

g = wb["ACE gaps"]
print("---- ACE gaps header")
print([g.cell(row=1, column=c).value for c in range(1, 11)])
print("DF-LEG-006:", [g.cell(row=r, column=c).value for r in range(2, g.max_row + 1)
                      if g.cell(row=r, column=1).value == "DF-LEG-006" for c in range(1, 11)])

mr = wb["Mapping rules"]
print("---- Mapping rules new rows")
for r in range(11, mr.max_row + 1):
    print(r, "|", mr.cell(row=r, column=1).value)
