import docx
from docx.oxml.ns import qn
from lxml import etree

d = docx.Document(r"05 Technical architecture/Recovery Workbench Error Handling and Resilience Standard v3.docx")
t = d.tables[1]
hdr = t.cell(0, 0)
body = t.cell(1, 0)
for name, cell in (("hdr", hdr), ("body", body)):
    p = cell.paragraphs[0]
    print(name, "p style", p.style.name if p.style is not None else None,
          "align", p.alignment)
    for r in p.runs:
        print("   run", repr(r.text[:30]), "bold", r.bold, "italic", r.italic,
              "font", r.font.name, "size", r.font.size)
print("tblW:", t._tbl.tblPr.find(qn("w:tblW")).attrib)
print("borders present:", t._tbl.tblPr.find(qn("w:tblBorders")) is not None)
trPr = t.rows[0]._tr.find(qn("w:trPr"))
print("trPr:", etree.tostring(trPr).decode()[:300] if trPr is not None else None)
tcPr = hdr._tc.find(qn("w:tcPr"))
print("hdr tcPr:", etree.tostring(tcPr).decode()[-400:] if tcPr is not None else None)
