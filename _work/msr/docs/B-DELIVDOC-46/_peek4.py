import openpyxl
wb = openpyxl.load_workbook(r"22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx", data_only=True)
ws = wb["Services"]
for r in ws.iter_rows(values_only=True):
    print(r)
print("---README---")
for r in wb["Read me"].iter_rows(values_only=True):
    print(r)
