"""Make a scratch copy of the source .docx whose built-in style names python-docx can resolve.

The source docx stores the built-in heading styles under their display names ("Heading 1"),
while python-docx looks them up by the built-in internal names ("heading 1"). The copy renames
only the style names used by doc.add_heading and the table style; page setup, fonts and the
section properties are the source's, and the source file is never modified.
"""
import shutil
from pathlib import Path

import docx

ROOT = Path(__file__).resolve().parents[4]
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
SRC = ROOT / "03 Requirements and specifications/Recovery Workbench Business Requirements Epic 1 v4.docx"
DST = ROOT / "_work/msr/docs/B-REQ-BRD-E1/template_v5.docx"

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
               "list bullet", "list paragraph", "title", "table grid"):
        if val != low:
            name.set(f"{W}val", low)
            fixed.append((val, low))
d.save(str(DST))
print("WROTE", DST.relative_to(ROOT), "renamed", fixed)
