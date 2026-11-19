import openpyxl, sys, json
wb = openpyxl.load_workbook(sys.argv[1], read_only=True, data_only=True)
print(wb.sheetnames)
for s in ('Entities','Fields'):
    ws = wb[s]
    rows = list(ws.iter_rows(values_only=True))
    for i,r in enumerate(rows[:6]): print(s, i, r[:8])
    print(s, 'total rows', len(rows))
