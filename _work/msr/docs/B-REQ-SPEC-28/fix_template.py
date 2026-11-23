"""Make a scratch copy of the source .docx whose built-in style names python-docx can resolve.

The source v3 docx stores its built-in heading and bullet styles under display names ("Heading 1"),
while python-docx looks them up by the built-in internal names ("heading 1"). The copy renames only the
style name values used by doc.add_heading and the List Bullet style; page setup, fonts, table styles and
the section properties are untouched. The source file is never modified.
"""
import shutil
from pathlib import Path

import docx

ROOT = Path(__file__).resolve().parents[4]
SRC = ROOT / "03 Requirements and specifications/Recovery Workbench Non Functional Specification v3.docx"
DST = ROOT / "_work/msr/docs/B-REQ-SPEC-28/template_v4.docx"
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"

if DST.exists():
    raise SystemExit(f"REFUSED: {DST} exists")
shutil.copy2(SRC, DST)

d = docx.Document(str(DST))
fixed = []
for st in d.styles.element.findall(f"{W}style"):
    name = st.find(f"{W}name")
    if name is None:
        continue
    val = name.get(f"{W}val")
    low = (val or "").lower()
    if low in ("heading 1", "heading 2", "heading 3", "heading 4", "heading 5", "heading 6",
               "list bullet", "title", "list paragraph", "table grid"):
        if val != low:
            name.set(f"{W}val", low)
            fixed.append((val, low))
d.save(str(DST))
print("WROTE", DST.relative_to(ROOT), "renamed", fixed)
