"""Make a scratch copy of the source .docx whose built-in style names python-docx can resolve.

The source stores its built-in heading and table styles under display names ("Heading 1",
"Table Grid"), while python-docx looks them up by internal names ("heading 1", "table grid").
Only the style name values are lower-cased in the copy; page setup, fonts, header and footer
and the rest are untouched. The source .docx is never modified.
"""
import shutil
from pathlib import Path

import docx

ROOT = Path(__file__).resolve().parents[4]
SRC = ROOT / "09 Testing and quality/Recovery Workbench Non Functional Test Plan v2.docx"
DST = ROOT / "_work/msr/docs/B-TESTDOC-40/template_v3.docx"

if DST.exists():
    raise SystemExit(f"REFUSED: {DST} exists")
shutil.copy2(SRC, DST)

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
d = docx.Document(str(DST))
fixed = []
for st in d.styles.element.findall(W + "style"):
    name = st.find(W + "name")
    if name is None:
        continue
    val = name.get(W + "val")
    low = (val or "").lower()
    if low in ("heading 1", "heading 2", "heading 3", "heading 4", "heading 5", "heading 6",
               "list bullet", "title", "list paragraph", "table grid"):
        if val != low:
            name.set(W + "val", low)
            fixed.append((val, low))
d.save(str(DST))
print("WROTE", DST.relative_to(ROOT), "renamed", fixed)
