import openpyxl
wb = openpyxl.load_workbook('22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx', data_only=True)
ws = wb['Services']
for r in ws.iter_rows(min_row=2, values_only=True):
    print(r)
print('--- read me ---')
for r in wb['Read me'].iter_rows(values_only=True):
    print(r)
