import re, docx
d = docx.Document('03 Requirements and specifications/Recovery Workbench Business Requirements Epic 2 v2.docx')
x = d.tables[0]._tbl.tblPr.xml
print('has borders:', 'tblBorders' in x)
x = re.sub(r'xmlns:[^=]+="[^"]+" ?', '', x)
print(x[:900])
