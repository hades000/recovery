"""Probe the source v2 docx: bullet numbering, table borders, header/footer, styles."""
import re
import docx
from docx.oxml.ns import qn

SRC = r"05 Technical architecture\Recovery Workbench Document Management Design v2.docx"


def clean(x):
    s = x.xml
    return re.sub(r'xmlns:[a-z0-9]+="[^"]*"\s*', "", s)


d = docx.Document(SRC)
lp = [x for x in d.paragraphs if x.style.name == "List Paragraph"][0]
print("BULLET PARA:", clean(lp._p)[:900])
print("=====")
t = d.tables[0]
print("TBLPR:", clean(t._tbl.tblPr)[:900])
print("=====")
print("CELL:", clean(t.rows[0].cells[0]._tc)[:900])
print("=====")
print("TITLE:", clean(d.paragraphs[1]._p)[:600])
print("=====")
print("H1:", clean(d.paragraphs[6]._p)[:600])
print("=====")
for i, s in enumerate(d.styles):
    try:
        print(i, s.type, repr(s.name), s.style_id)
    except Exception as e:
        print(i, "ERR", e)
