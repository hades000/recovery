"""Repair a scratch copy of the template so compat/office_write.py md-docx can render it.

Two quirks of this document family:

1. w:name/@w:val of the heading styles is "Heading 1", while python-docx looks a
   built-in heading up as "heading 1"; the copy writes the conventional value.
2. The family has no "List Bullet" style, so add_paragraph(text, style="List Bullet")
   raises. The copy adds one based on "List Paragraph" with the bullet numbering
   (numId 2) that the source document's own bullet list uses.

The source file is never touched.
"""
import shutil
import sys

import docx
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

src, dst = sys.argv[1], sys.argv[2]
shutil.copy2(src, dst)
d = docx.Document(dst)

for s in d.styles:
    el = s.element
    if not el.tag.endswith("}style") or not s.name or not s.name.startswith("Heading "):
        continue
    name = el.find(qn("w:name"))
    if name is not None:
        name.set(qn("w:val"), s.name.lower())

if "List Bullet" not in [s.name for s in d.styles]:
    st = d.styles.add_style("List Bullet", WD_STYLE_TYPE.PARAGRAPH)
    st.base_style = d.styles["List Paragraph"]
    pPr = st.element.get_or_add_pPr()
    numPr = OxmlElement("w:numPr")
    ilvl = OxmlElement("w:ilvl")
    ilvl.set(qn("w:val"), "0")
    num_id = OxmlElement("w:numId")
    num_id.set(qn("w:val"), "2")
    numPr.append(ilvl)
    numPr.append(num_id)
    pPr.insert(0, numPr)

d.save(dst)
check = docx.Document(dst)
print("WROTE", dst)
print("headings", [(s.name, str(s.element.find(qn("w:name")).get(qn("w:val"))))
                   for s in check.styles if s.name and s.name.startswith("Heading")])
print("lookup Heading 1:", check.styles["Heading 1"])
print("lookup List Bullet:", check.styles["List Bullet"])
