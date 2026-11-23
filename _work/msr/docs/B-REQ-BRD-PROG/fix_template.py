"""Make a scratch copy of a source .docx whose built-in style names python-docx can resolve.

The source .docx stores the built-in heading styles with their display names ("Heading 1"),
while python-docx looks them up by the built-in internal names ("heading 1"). The copy renames
only the style identifiers used by doc.add_heading/List Bullet; page setup, fonts and the rest
are untouched. The source file is never modified.
"""
import shutil
import sys
from pathlib import Path

import docx

ROOT = Path(__file__).resolve().parents[4]
SRC = ROOT / "03 Requirements and specifications/Recovery Workbench Business Requirements Program v4.docx"
DST = ROOT / "_work/msr/docs/B-REQ-BRD-PROG/template_v5.docx"

if DST.exists():
    raise SystemExit(f"REFUSED: {DST} exists")
shutil.copy2(SRC, DST)

d = docx.Document(str(DST))
fixed = []
for st in d.styles.element.findall(
        "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}style"):
    name = st.find("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}name")
    if name is None:
        continue
    val = name.get("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val")
    low = (val or "").lower()
    if low in ("heading 1", "heading 2", "heading 3", "heading 4", "heading 5", "heading 6",
               "list bullet", "title", "list paragraph", "table grid"):
        if val != low:
            name.set("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val", low)
            fixed.append((val, low))
d.save(str(DST))
print("WROTE", DST.relative_to(ROOT), "renamed", fixed)
