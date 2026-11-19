import sys, docx
from docx.document import Document as D
from docx.table import Table
from docx.text.paragraph import Paragraph
d = docx.Document(sys.argv[1])
body = d.element.body
pi = ti = 0
for el in body.iterchildren():
    tag = el.tag.split('}')[1]
    if tag == 'p':
        p = Paragraph(el, d)
        print(f'P{pi} [{p.style.name}] {p.text}')
        pi += 1
    elif tag == 'tbl':
        t = Table(el, d)
        print(f'--- T{ti} style={t.style.name if t.style else None}')
        for ri, r in enumerate(t.rows):
            print(f'  R{ri}: ' + ' | '.join(c.text.replace(chr(10), " / ") for c in r.cells))
        ti += 1
for s in d.sections:
    for h in s.header.paragraphs + s.footer.paragraphs:
        if h.text.strip(): print('HF:', h.text)
