import io
import openpyxl

p = r'ACE schema\ACE-data-schema_20261104.xlsx'
wb = openpyxl.load_workbook(p, data_only=True)
skip = {'Migrations', 'Sequences'}
out = io.open(r'_work\analysis\ace_columns.txt', 'w', encoding='utf-8')
for name in wb.sheetnames:
    if name == 'Overview' or name in skip:
        continue
    ws = wb[name]
    out.write('### %s\n' % name)
    for r in ws.iter_rows(values_only=True):
        if r and r[0]:
            out.write('|'.join(str(x) if x is not None else '' for x in r[:8]) + '\n')
out.close()
print('done')
