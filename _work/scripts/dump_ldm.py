import io
import openpyxl

p = r'06 Data\Recovery Workbench Logical Data Model and Data Dictionary v6.xlsx'
wb = openpyxl.load_workbook(p, data_only=True)
ws = wb['Fields']
rows = [r for r in ws.iter_rows(min_row=5, values_only=True) if r[0]]
out = io.open(r'_work\analysis\ldm_external.txt', 'w', encoding='utf-8')
out.write('fields %d\n' % len(rows))
ext = [r for r in rows if r[11] and str(r[11]).strip() not in ('Workbench', 'None', '')]
out.write('external fields %d\n' % len(ext))
for r in ext:
    out.write('|'.join(str(x) if x is not None else '' for x in r) + '\n')
out.write('\n=== sources sheet ===\n')
ws2 = wb['Sources']
for r in ws2.iter_rows(min_row=5, values_only=True):
    if r[0]:
        out.write('|'.join(str(x) if x is not None else '' for x in r) + '\n')
out.close()

out2 = io.open(r'_work\analysis\ldm_entities_full.txt', 'w', encoding='utf-8')
ws3 = wb['Entities']
for r in ws3.iter_rows(min_row=5, values_only=True):
    if r[0]:
        out2.write('|'.join(str(x) if x is not None else '' for x in r) + '\n')
out2.close()
print('done')
