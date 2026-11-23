import docx
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docx.shared import Pt

p = "06 Data/Recovery Workbench Data Migration Approach v4.docx"
d = docx.Document(p)

def borders(table):
    tblPr = table._tbl.tblPr
    for old in tblPr.findall(qn("w:tblBorders")):
        tblPr.remove(old)
    b = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        e = OxmlElement("w:" + edge)
        e.set(qn("w:val"), "single"); e.set(qn("w:sz"), "4")
        e.set(qn("w:space"), "0"); e.set(qn("w:color"), "808080")
        b.append(e)
    tblPr.append(b)

def header_row(table):
    tr = table.rows[0]._tr
    trPr = tr.get_or_add_trPr()
    h = OxmlElement("w:tblHeader"); trPr.append(h)
    for c in table.rows[0].cells:
        for par in c.paragraphs:
            for r in par.runs:
                r.bold = True

for t in d.tables:
    borders(t)
    header_row(t)

d.save(p)
print("TABLES", len(d.tables))
print("PARAS", len(d.paragraphs))
hi = sum(1 for x in d.paragraphs if x.style.name in ("Heading 1", "Heading 2"))
print("HEADINGS", hi)
print("FIRST", [x.text for x in d.paragraphs[:4]])
