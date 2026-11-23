import openpyxl

p = r'22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx'
wb = openpyxl.load_workbook(p, data_only=True)
ws = wb['Tables']
for r in ws.iter_rows(min_row=1, values_only=True):
    if r[1] == 'PLT':
        print([str(c)[:90] if c is not None else '' for c in r])
print('--- Jobs PLT ---')
ws = wb['Jobs']
for r in ws.iter_rows(min_row=1, values_only=True):
    if r[1] == 'PLT' or (r[0] and str(r[0]) in ('JOB-05', 'JOB-11', 'JOB-21', 'JOB-22')):
        print([str(c)[:120] if c is not None else '' for c in r])
print('--- Params ---')
ws = wb['Parameters']
for r in ws.iter_rows(min_row=1, values_only=True):
    print([str(c)[:120] if c is not None else '' for c in r])
