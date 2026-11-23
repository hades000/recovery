"""B-REQ-BRD-E2 helper 2: give the generated tables the source document's grid and header row.

The md-docx writer creates borderless tables with plain first rows. This pass adds the same
single-line border set the source document uses, repeats the first row as the header row and
sets that row bold. It runs on the new output file only.
"""
import sys
from pathlib import Path

import docx
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

PATH = Path(sys.argv[1])
if not PATH.exists():
    raise SystemExit(f"missing {PATH}")

doc = docx.Document(str(PATH))


def borders():
    b = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        e = OxmlElement(f"w:{edge}")
        e.set(qn("w:val"), "single")
        e.set(qn("w:color"), "auto")
        e.set(qn("w:sz"), "4")
        b.append(e)
    return b


count = 0
for t in doc.tables:
    pr = t._tbl.tblPr
    if pr.find(qn("w:tblBorders")) is None:
        pr.insert_element_before(borders(), "w:shd", "w:tblLayout", "w:tblCellMar", "w:tblLook",
                                 "w:tblCaption", "w:tblDescription")
    if t.rows:
        tr = t.rows[0]._tr
        trPr = tr.get_or_add_trPr()
        if trPr.find(qn("w:tblHeader")) is None:
            trPr.append(OxmlElement("w:tblHeader"))
        for cell in t.rows[0].cells:
            for p in cell.paragraphs:
                for r in p.runs:
                    r.bold = True
    count += 1

doc.save(str(PATH))
print("PATCHED", count, "tables in", PATH)
