"""Post-process the generated .docx: table borders, header-row repeat, cell text size.

The source template defines no table style, so the generated tables would print without
borders. This script only formats the file it is given (the new v3 output) and never
touches the source.
"""
import sys
from pathlib import Path

import docx
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt

P = Path(sys.argv[1])


def borders(table):
    tbl_pr = table._tbl.tblPr
    for old in tbl_pr.findall(qn("w:tblBorders")):
        tbl_pr.remove(old)
    b = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        el = OxmlElement(f"w:{edge}")
        el.set(qn("w:val"), "single")
        el.set(qn("w:sz"), "4")
        el.set(qn("w:space"), "0")
        el.set(qn("w:color"), "808080")
        b.append(el)
    tbl_pr.append(b)


def repeat_header(row):
    tr_pr = row._tr.get_or_add_trPr()
    el = OxmlElement("w:tblHeader")
    el.set(qn("w:val"), "true")
    tr_pr.append(el)


d = docx.Document(str(P))
for t in d.tables:
    borders(t)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    repeat_header(t.rows[0])
    for r, row in enumerate(t.rows):
        for cell in row.cells:
            for p in cell.paragraphs:
                for run in p.runs:
                    run.font.size = Pt(8.5)
                    if r == 0:
                        run.font.bold = True
    # first column slightly narrower on wide tables is left to Word autofit
    t.autofit = True
d.save(str(P))
print("FORMATTED", P, "tables", len(d.tables))
