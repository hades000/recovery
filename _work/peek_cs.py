import openpyxl
p = r'C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\12 Project communication\Recovery Workbench Document Control Sheet v11.xlsx'
wb = openpyxl.load_workbook(p)
ws = wb['Control sheet']
print('A1', ws['A1'].value)
print('A2', ws['A2'].value)
for r in list(range(5, 10)) + list(range(126, 137)):
    vals = [ws.cell(row=r, column=c).value for c in (1, 2, 3, 4, 5)]
    print(r, vals, ws.row_dimensions[r].height)
print('key', [[wb['Key'].cell(row=r, column=c).value for c in (1, 2)] for r in range(4, 9)])
print('summary total', [wb['Summary'].cell(row=8, column=c).value for c in range(1, 5)])
