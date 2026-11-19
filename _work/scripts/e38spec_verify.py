import zipfile, re, html, openpyxl, xml.dom.minidom as md
R=r"C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\03 Requirements and specifications\Recovery Workbench Epics 3 to 8 Specification v3"
z=zipfile.ZipFile(R+'.docx'); assert z.testzip() is None
for n in z.namelist():
    if n.endswith('.xml') or n.endswith('.rels'): md.parseString(z.read(n))
x=z.read('word/document.xml').decode()
rows=[[html.unescape(''.join(re.findall(r'<w:t[^>]*>([^<]*)</w:t>',c))) for c in re.findall(r'<w:tc>.*?</w:tc>',r,re.S)] for r in re.findall(r'<w:tr[ >].*?</w:tr>',x,re.S)]
dfeat={r[1].split(' ')[0]:r[3] for r in rows if len(r)==4 and r[1].startswith('FEAT-')}
dint={r[0]:r[1:] for r in rows if len(r)==5 and r[0].startswith('INT-')}
wb=openpyxl.load_workbook(R+'.xlsx'); print(wb.sheetnames)
xf={r[2]:r[5] for r in wb['Features'].iter_rows(min_row=5,values_only=True)}
xi={r[1]:(r[2],r[4],r[5],r[6]) for r in wb['Integrations'].iter_rows(min_row=5,values_only=True)}
mm=[k for k in dfeat if dfeat[k]!=xf.get(k)]
print('docx features',len(dfeat),'xlsx',len(xf),'mismatch',mm)
print('int mismatch',[k for k in dint if tuple(dint[k])!=xi.get(k)])
txt=html.unescape(''.join(re.findall(r'<w:t[^>]*>([^<]*)</w:t>',x)))
for w in ['File load',"next day's load",'loan_account','account_payment','collections_history','contact_point ','28 October']:
    print(w, txt.count(w))
