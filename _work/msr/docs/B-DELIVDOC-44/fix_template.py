"""Make a template copy that compat/office_write.py md-docx can render.

The document family stores w:name/@w:val of the heading styles as "Heading 1" while python-docx
looks the style up as "heading 1", so add_heading raises KeyError. The copy writes the
conventional Word value "heading 1". The copy also gains a "List Bullet" paragraph style with
no numbering reference, so add_paragraph(..., style="List Bullet") works; the family has no
numbering definitions, so the bullet glyph is left to the style.

The source document is never modified.
"""
import shutil
import sys

import docx
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml.ns import qn

src, dst = sys.argv[1], sys.argv[2]
shutil.copy2(src, dst)
d = docx.Document(dst)

for s in d.styles:
    el = s.element
    if not el.tag.endswith("}style") or not s.name or not s.name.startswith("Heading "):
        continue
    el.find(qn("w:name")).set(qn("w:val"), s.name.lower())

if "List Bullet" not in [s.name for s in d.styles]:
    st = d.styles.add_style("List Bullet", WD_STYLE_TYPE.PARAGRAPH)
    st.base_style = d.styles["List Paragraph"]
    st.paragraph_format.left_indent = 360000
    st.paragraph_format.first_line_indent = -180000

d.save(dst)
check = docx.Document(dst)
print("WROTE", dst)
print("headings", [(s.name, str(s.element.find(qn("w:name")).get(qn("w:val"))))
                   for s in check.styles if s.name and s.name.startswith("Heading")])
print("lookup Heading 1:", check.styles["Heading 1"])
print("list bullet:", check.styles["List Bullet"])
