"""B-REQ-BRD-E2 helper 1: make a template copy whose heading style names python-docx can find.

The source document stores builtin heading styles under their display names ("Heading 1"),
while python-docx looks them up under the internal names ("heading 1"). The copy keeps every
font, margin and numbering definition and only rewrites the w:name value of the heading styles.
The source file is never touched.
"""
from pathlib import Path

import docx
from docx.oxml.ns import qn

SRC = Path("03 Requirements and specifications/Recovery Workbench Business Requirements Epic 2 v2.docx")
DST = Path("_work/msr/docs/B-REQ-BRD-E2/template-base.docx")

if DST.exists():
    raise SystemExit(f"REFUSED: {DST} exists")

doc = docx.Document(str(SRC))
changed = []
for style in doc.styles:
    sid = style.element.get(qn("w:styleId")) or ""
    if sid.lower().startswith("heading"):
        n = style.element.find(qn("w:name"))
        if n is not None:
            cur = n.get(qn("w:val"))
            low = cur.lower()
            if cur != low:
                n.set(qn("w:val"), low)
                changed.append((sid, cur, low))
doc.save(str(DST))
print("WROTE", DST, "renamed", changed)

probe = docx.Document(str(DST))
probe.add_heading("probe", 1)
probe.add_heading("probe", 2)
print("heading styles usable:", [s.name for s in probe.styles if s.name.lower().startswith("heading")])
