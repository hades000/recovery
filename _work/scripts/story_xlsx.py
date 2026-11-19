import io
import openpyxl

for f in [r'04 User stories\Recovery Workbench User Stories Epic 1 v7.xlsx',
          r'04 User stories\Recovery Workbench User Stories Epics 3 to 8 v2.xlsx',
          r'04 User stories\Recovery Workbench Administration Stories v2.xlsx',
          r'04 User stories\Recovery Workbench Data Migration Stories v2.xlsx']:
    wb = openpyxl.load_workbook(f, data_only=True)
    print('=' * 10, f)
    print(wb.sheetnames)
    for ws in wb.worksheets[:3]:
        print('---', ws.title, ws.max_row, ws.max_column)
        for r in ws.iter_rows(min_row=1, max_row=5, values_only=True):
            print([str(c)[:30] if c is not None else '' for c in r])
