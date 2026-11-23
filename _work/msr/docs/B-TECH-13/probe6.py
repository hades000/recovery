"""Probe first-column shading of the 3-column and 4-column tables of the source docx."""
import re
import docx

SRC = r"05 Technical architecture\Recovery Workbench Document Management Design v2.docx"


def shd(cell):
    tcPr = cell._tc.tcPr
    if tcPr is None:
        return None
    el = tcPr.find("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}shd")
    return None if el is None else el.get("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}fill")


d = docx.Document(SRC)
for i, t in enumerate(d.tables):
    print("table", i, "rows", len(t.rows), "cols", len(t.columns))
    print("  header shd:", [shd(c) for c in t.rows[0].cells])
    if len(t.rows) > 1:
        print("  row1   shd:", [shd(c) for c in t.rows[1].cells])
    if len(t.rows) > 2:
        print("  row2   shd:", [shd(c) for c in t.rows[2].cells])
