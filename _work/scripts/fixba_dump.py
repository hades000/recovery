import openpyxl,sys
wb=openpyxl.load_workbook(sys.argv[1])
print('PROPS',wb.properties.title,wb.properties.modified)
for ws in wb:
    print('=== SHEET',ws.title,ws.dimensions)
    for row in ws.iter_rows():
        for c in row:
            if c.value is not None: print(c.coordinate,repr(c.value)[:500])
