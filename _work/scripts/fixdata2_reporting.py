import openpyxl
P = '06 Data/Recovery Workbench Reporting and Analytics Data Model v3.xlsx'
wb = openpyxl.load_workbook(P)
F = wb['Facts']; D = wb['Dimensions']
assert F['F4'].value == 'Load or refresh'
F['F4'] = 'Refresh'
assert D['A5'].value == 'dim_date' and D['A6'].value == 'dim_product'
D['B5'] = 'Calendar with bank holidays and business days; holidays read through v_ace_holiday'
D['B6'] = 'Mortgage, hire purchase, SSME and the product codes; product codes read through v_ace_product'
wb.properties.title = 'Recovery Workbench Reporting and Analytics Data Model v3'
wb.save(P)
print('ok')
