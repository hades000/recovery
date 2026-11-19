import zipfile, re
z = zipfile.ZipFile(r'C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\12 Project communication\Recovery Workbench Document Control Sheet v11.xlsx')
x = z.read('xl/worksheets/sheet1.xml').decode('utf8')
rs = [int(m) for m in re.findall(r'<row r="(\d+)"', x)]
print('rows written', len(rs), 'min', min(rs), 'max', max(rs))
print('missing', [i for i in range(1, 137) if i not in rs])
print('tail', x[-500:])
