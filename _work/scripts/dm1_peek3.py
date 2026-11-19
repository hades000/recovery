import openpyxl
wb = openpyxl.load_workbook(r'04 User stories/Recovery Workbench ACE Team Stories v1.xlsx', read_only=True, data_only=True)
print(wb.sheetnames)
for s in wb.sheetnames:
    rows = list(wb[s].iter_rows(values_only=True))
    print('==', s, len(rows)); print(rows[0])
    for r in rows:
        if any(isinstance(c,str) and c in ('account','customer','efs_action') for c in r[:2]): print(r)
