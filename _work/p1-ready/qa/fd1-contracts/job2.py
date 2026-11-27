import openpyxl
wb = openpyxl.load_workbook('../../stage/05 Technical architecture/Recovery Workbench Service Contract Catalog v3.xlsx')
ws = wb['Jobs']
for r in ws.iter_rows(values_only=True):
    if r[0] in ('Job', 'JOB-07', 'JOB-08'): print(r)
for r in wb['Temporal contracts'].iter_rows(values_only=True):
    if r[1] and ('ooking' in str(r[1]) or 'rwb-payment' in str(r[2])): print(r)
