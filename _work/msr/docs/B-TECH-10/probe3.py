import docx
from lxml import etree
from docx.oxml.ns import qn

d = docx.Document(r"05 Technical architecture/Recovery Workbench Error Handling and Resilience Standard v3.docx")
t = d.tables[0]
tblPr = t._tbl.tblPr
for child in tblPr:
    tag = child.tag.split("}")[1]
    print(tag, etree.tostring(child).decode()[:700])
    print()
print("grid cols:", [gc.get(qn("w:w")) for gc in t._tbl.tblGrid.findall(qn("w:gridCol"))])
print("first cell p xml:", etree.tostring(t.cell(0, 0).paragraphs[0]._p).decode()[:900])
