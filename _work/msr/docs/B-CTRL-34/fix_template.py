"""Make a scratch template copy that compat/office_write.py md-docx can render.

Two quirks of this document family are repaired in the scratch copy only:

1. w:name/@w:val of the heading styles may be "Heading 1", while python-docx looks the
   style up as "heading 1"; the copy writes the conventional Word value.
2. The family may have no "List Bullet" style, so add_paragraph(text, style="List Bullet")
   appends the paragraph and then raises. The copy adds a "List Bullet" style based on
   "List Paragraph", with the bullet numbering the source document uses for its own lists.

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

names = [s.name for s in d.styles]
if "List Bullet" not in names:
    st = d.styles.add_style("List Bullet", WD_STYLE_TYPE.PARAGRAPH)
    st.base_style = d.styles["List Paragraph"] if "List Paragraph" in names else d.styles["Normal"]
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
print("list bullet:", check.styles["List Bullet"])
print("lookup Heading 1:", check.styles["Heading 1"])
