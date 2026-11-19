import openpyxl
wb = openpyxl.load_workbook(r'15 ACE DB Alignment/Recovery Workbench ACE Field Gap List v1.xlsx', read_only=True, data_only=True)
for r in wb['Fields'].iter_rows(min_row=2, values_only=True):
    if r[8] and r[8].split('.')[0] in ('account','customer','efs_action') and r[7]=='ACE new':
        print(r)
print()
for r in wb['ACE additions'].iter_rows(min_row=2, values_only=True):
    if r[0] in ('account','customer','efs_action'): print(r)
for r in wb['Fields'].iter_rows(min_row=2, values_only=True):
    if r[0] in ('DF-DEC-006',): print(r)
