from docx import Document
p = r'03 Requirements and specifications/Recovery Workbench Business Requirements Epics 3 to 8 v1.docx'
d = Document(p)
paras = d.paragraphs
print('paragraphs', len(paras), 'tables', len(d.tables))
for para in paras[:8]:
    print(repr(para.style.name), '|', para.text[:90])
print('---- headings ----')
hs = [x.text for x in paras if x.style.name.startswith('Heading')]
print(len(hs))
for h in hs[:20]:
    print(h[:80])
print('first table rows', len(d.tables[0].rows), 'cells', [c.text for c in d.tables[0].rows[0].cells])
