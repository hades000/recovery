import sys, docx
from docx.oxml.ns import qn
d = docx.Document(sys.argv[1])
body = d.element.body
pi = ti = 0
for el in body.iterchildren():
    if el.tag == qn('w:p'):
        p = docx.text.paragraph.Paragraph(el, d)
        print(f'P{pi} [{p.style.name}] {p.text}')
        pi += 1
    elif el.tag == qn('w:tbl'):
        t = docx.table.Table(el, d)
        print(f'--- T{ti} style={t.style.name if t.style else None}')
        for ri, row in enumerate(t.rows):
            print(f'  R{ri}: ' + ' | '.join(c.text.replace("\n", " / ") for c in row.cells))
        ti += 1
    else:
        print('OTHER', el.tag)
