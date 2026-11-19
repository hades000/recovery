import sys, docx
from docx.table import Table
from docx.text.paragraph import Paragraph
p = sys.argv[1]
d = docx.Document(p)
body = d.element.body
i = 0
for child in body.iterchildren():
    if child.tag.endswith('}p'):
        para = Paragraph(child, d)
        if para.text.strip():
            print("P[%s]: %s" % (para.style.name, para.text))
    elif child.tag.endswith('}tbl'):
        t = Table(child, d)
        i += 1
        print("TABLE %d: %d rows x %d cols" % (i, len(t.rows), len(t.columns)))
        for r in t.rows:
            print("   | " + " | ".join(c.text.strip().replace("\n", " / ") for c in r.cells))
print("---- headers/footers ----")
for s in d.sections:
    for part in (s.header, s.footer):
        for para in part.paragraphs:
            if para.text.strip():
                print("HF:", para.text)
