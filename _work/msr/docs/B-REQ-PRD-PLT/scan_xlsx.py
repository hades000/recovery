import zipfile, re, io, sys

p = r'22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx'
try:
    import openpyxl
    wb = openpyxl.load_workbook(p, data_only=True)
    for ws in wb.worksheets:
        print('=== SHEET', ws.title, ws.max_row, ws.max_column)
        for r in ws.iter_rows(min_row=1, max_row=min(ws.max_row, 4), values_only=True):
            print('   ', [str(c)[:40] if c is not None else '' for c in r])
except Exception as e:
    print('ERR', e)
