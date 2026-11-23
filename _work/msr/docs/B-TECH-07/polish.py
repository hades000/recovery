"""Match the look of the family: title block, body, bullets and table text of version 3.

compat/office_write.py md-docx writes body paragraphs in Normal and the title lines as
Heading 1. Version 3 has a Normal-style title block, 10 pt body text and bullet lists, and
its tables use 9 pt cells with a 9 pt bold header. This sets the same direct formatting on
the built file; the paragraph styles are kept, so bullets stay bullets.
"""
import sys

import docx
from docx.shared import Pt, RGBColor


def fmt(p, size, bold, color):
    for r in p.runs or [p.add_run("")]:
        r.font.name = "Aptos"
        r.font.size = Pt(size)
        r.font.bold = bold
        r.font.color.rgb = RGBColor.from_string(color)


path = sys.argv[1]
d = docx.Document(path)
para = d.paragraphs

# header lines of Template and Rules R8.1
fmt(para[0], 10, False, "404040")
para[0].paragraph_format.space_after = Pt(0)
fmt(para[1], 10, False, "404040")
para[1].paragraph_format.space_after = Pt(6)

# title block of version 3: 26 pt bold 4E297F, then 17 pt 604A7B, both Normal
assert para[2].text == "Recovery Workbench", para[2].text
assert para[3].text == "Rules engine design", para[3].text
para[2].style = d.styles["Normal"]
fmt(para[2], 26, True, "4E297F")
para[2].paragraph_format.space_after = Pt(6)
para[3].style = d.styles["Normal"]
fmt(para[3], 17, False, "604A7B")
para[3].paragraph_format.space_after = Pt(18)

# body text and bullets: keep the style, set the run formatting
for p in para[4:]:
    if p.style.name in ("Normal", "List Bullet"):
        fmt(p, 10, False, "1F1F1F")

# table text: 9 pt, bold brand-colour header row
for t in d.tables:
    for i, row in enumerate(t.rows):
        for cell in row.cells:
            for p in cell.paragraphs:
                fmt(p, 9, i == 0, "4E297F" if i == 0 else "1F1F1F")

d.save(path)
c = docx.Document(path)
print("SAVED", path)
print("paragraphs", len(c.paragraphs), "tables", len(c.tables))
print("header", c.paragraphs[0].runs[0].font.size.pt, c.paragraphs[0].runs[0].font.color.rgb)
print("title", c.paragraphs[2].text, c.paragraphs[2].runs[0].font.size.pt, c.paragraphs[2].runs[0].font.bold)
print("body", c.paragraphs[5].runs[0].font.size.pt, c.paragraphs[5].runs[0].font.color.rgb)
print("bullets", [(p.style.name, p.runs[0].font.size.pt) for p in c.paragraphs if p.style.name == "List Bullet"][:3])
print("cell", c.tables[1].cell(0, 0).paragraphs[0].runs[0].font.size.pt,
      c.tables[1].cell(1, 0).paragraphs[0].runs[0].font.size.pt)
