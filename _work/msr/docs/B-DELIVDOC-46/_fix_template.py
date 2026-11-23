"""Make a template copy that compat/office_write.py md-docx can render.

The document family stores w:name/@w:val of the heading styles as "Heading 1" while python-docx
looks the style up as "heading 1", so add_heading raises KeyError. The copy writes the
conventional Word value "heading 1" and adds a "List Bullet" paragraph style, so the helper
renders the new version. The source document is never modified.
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
print("lookup Heading 1:", check.styles["Heading 1"].name)
print("lookup List Bullet:", check.styles["List Bullet"].name)
