import openpyxl, sys
wb = openpyxl.load_workbook(sys.argv[1], read_only=True, data_only=True)
print(wb.sheetnames)
for s in wb.sheetnames:
    ws = wb[s]
    rows = list(ws.iter_rows(values_only=True))
    print('==', s, len(rows))
    for r in rows[:int(sys.argv[2]) if len(sys.argv)>2 else 4]:
        print(r)
