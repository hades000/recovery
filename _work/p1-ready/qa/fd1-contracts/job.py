import openpyxl, re
wb = openpyxl.load_workbook('../../stage/05 Technical architecture/Recovery Workbench Service Contract Catalog v3.xlsx')
for ws in wb:
    for row in ws.iter_rows():
        t = ' | '.join(str(c.value) for c in row if c.value is not None)
        if re.search(r'JOB-08|BookingMatch|booking', t, re.I):
            print(ws.title, row[0].row, t[:400])
