import io
import openpyxl

p = r'01 Decisions and governance\Recovery Workbench Decision Log v8.xlsx'
wb = openpyxl.load_workbook(p, data_only=True)
out = io.open(r'_work\analysis\decision_log.txt', 'w', encoding='utf-8')
out.write('sheets: %s\n' % wb.sheetnames)
for ws in wb.worksheets:
    out.write('\n=== %s (%d x %d) ===\n' % (ws.title, ws.max_row, ws.max_column))
    for r in ws.iter_rows(values_only=True):
        if any(c is not None for c in r):
            out.write('|'.join(str(c) if c is not None else '' for c in r) + '\n')
out.close()
print('done')
