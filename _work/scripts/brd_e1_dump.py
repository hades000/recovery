import sys, docx
from docx.table import Table
from docx.text.paragraph import Paragraph
d = docx.Document(sys.argv[1])
body = d.element.body
ti = 0
for i, el in enumerate(body.iterchildren()):
    tag = el.tag.split('}')[1]
    if tag == 'p':
        p = Paragraph(el, d)
        print(f'[{i}] P<{p.style.name}> {p.text}')
    elif tag == 'tbl':
        t = Table(el, d)
        print(f'[{i}] TABLE {ti} <{t.style.name if t.style else None}>')
        for r in t.rows:
            print('   | ' + ' | '.join(c.text.replace("\n"," / ") for c in r.cells))
        ti += 1
    else:
        print(f'[{i}] {tag}')
