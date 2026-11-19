import zipfile, re, openpyxl, os
from xml.dom import minidom
os.chdir(r'C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\06 Data')
def title(p):
    return re.search(r'<dc:title>([^<]*)', zipfile.ZipFile(p).read('docProps/core.xml').decode()).group(1)
files = ['Recovery Workbench Data Migration Approach v3.docx', 'Recovery Workbench Data Classification and Personal Data Inventory v4.xlsx',
 'Recovery Workbench Reference Data and Lists of Values v4.xlsx', 'Recovery Workbench Reporting and Analytics Data Model v3.xlsx',
 'Recovery Workbench Volume and Scale Forecast v3.xlsx', 'Recovery Workbench Volume and Scale Forecast v3.pptx',
 'Recovery Workbench Data Ownership and Stewardship v3.xlsx']
for f in files:
    z = zipfile.ZipFile(f); assert z.testzip() is None
    for n in z.namelist():
        if n.endswith('.xml') or n.endswith('.rels'): minidom.parseString(z.read(n))
    print('TITLE OK' if title(f) == f.rsplit('.', 1)[0] else 'TITLE BAD', f)
d = zipfile.ZipFile(files[0]).read('word/document.xml').decode()
t = ''.join(re.findall(r'<w:t(?: [^>]*)?>([^<]*)</w:t>', d))
print('MIG', 'RWB-E1-012' not in t, 'Cutover plan (U5)' in t, 'notices and proof' not in t, 'DL43' in t, 'superseded by D-RCV-35' in t)
wb = openpyxl.load_workbook(files[1]); F = wb['Fields']
olds = {'primary_customer_id', 'account_id', 'party_id', 'asset_id', 'contact_point_id', 'account_payment_id'}
print('DC old names left:', [F.cell(r,1).value for r in range(5, F.max_row+1) if F.cell(r,3).value in olds and not F.cell(r,2).value.startswith('v_ace')])
print('DC', wb['Summary']['C7'].value, wb['Summary']['C11'].value, wb['Identifiers'].max_row, wb['Identifiers']['A2'].value[:12], wb['Handling']['C5'].value[:60])
L = openpyxl.load_workbook(files[2])['Lists']
print('RD', L['E8'].value[:50], '|', L['E114'].value, '|', sum('(Section B, after RWB-ACE-001)' in str(L.cell(r,5).value) for r in range(5, L.max_row+1)))
wb = openpyxl.load_workbook(files[3]); print('RPT', wb['Facts']['F4'].value, '|', wb['Dimensions']['B5'].value, '|', wb['Dimensions']['B6'].value)
wb = openpyxl.load_workbook(files[4]); print('VOL', wb['Read path']['C16'].value, '|', [(wb['ACE growth'].cell(r,4).value, wb['ACE growth'].cell(r,5).value) for r in (21,22,23)])
s8 = zipfile.ZipFile(files[5]).read('ppt/slides/slide8.xml').decode(); print('PPT I33', 'I33' in s8, 'I34' in s8, s8.count('<a:tr '))
O = openpyxl.load_workbook(files[6])
for r in range(5, 19): print('OWN', O['Ownership'].cell(r,1).value, O['Ownership'].cell(r,11).value, '|', O['Ownership'].cell(r,7).value, '|', O['Ownership'].cell(r,6).value if r == 11 else '')
for r in range(5, 12): print('QM', [c.value for c in O['Quality measures'][r]])
