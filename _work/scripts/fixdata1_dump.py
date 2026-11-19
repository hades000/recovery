import sys, openpyxl
p = sys.argv[1]
wb = openpyxl.load_workbook(p)
print('sheets', wb.sheetnames, 'title', wb.properties.title)
for ws in wb.worksheets:
    if len(sys.argv) > 2 and ws.title not in sys.argv[2:]:
        continue
    print('\n=== %s (%d x %d)' % (ws.title, ws.max_row, ws.max_column))
    for row in ws.iter_rows():
        vals = [(c.coordinate, c.value) for c in row if c.value is not None]
        if vals:
            print(' | '.join('%s=%s' % (a, str(b).replace('\n', '\n')) for a, b in vals))
