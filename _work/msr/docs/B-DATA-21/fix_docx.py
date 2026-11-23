import docx
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

p = "06 Data/Recovery Workbench Data Migration Approach v4.docx"
d = docx.Document(p)
body = d.element.body

def ptext(el):
    return "".join(n.text or "" for n in el.iter() if n.tag.endswith("}t"))

removed = 0
prev = None
for el in list(body.iterchildren()):
    if el.tag.endswith("}p"):
        t = ptext(el)
        if t.startswith("\u2022 ") and prev is not None and ptext(prev) == t[2:]:
            body.remove(el)
            for n in prev.iter():
                if n.tag.endswith("}t") and n.text == t[2:]:
                    n.text = t
                    break
            removed += 1
            continue
        prev = el
    elif el.tag.endswith("}tbl"):
        prev = None
    else:
        prev = None

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

for t in d.tables:
    borders(t)
    tr = t.rows[0]._tr
    tr.get_or_add_trPr().append(OxmlElement("w:tblHeader"))
    for c in t.rows[0].cells:
        for par in c.paragraphs:
            for r in par.runs:
                r.bold = True

d.save(p)
d = docx.Document(p)
print("REMOVED DUPES", removed, "TABLES", len(d.tables), "PARAS", len(d.paragraphs))
for x in d.paragraphs[14:22]:
    print(repr(x.text)[:90], x.style.name)
