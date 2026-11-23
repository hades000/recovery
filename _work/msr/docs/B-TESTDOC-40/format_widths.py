"""Set a proportional column width per table of the generated .docx.

md-docx gives every table equal columns, which makes the wide per-service tables unreadable
(a 5-column table with a long "Load and data" cell). This sets a fixed layout and a width per
column for the 15 tables of the new file: total 6.69 inches, the usable A4 width of the template.
Only the file given on the command line is written.
"""
import sys
from pathlib import Path

import docx
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches

SPEC = [
    [1.55, 5.14],                      # 0 document control
    [0.85, 1.25, 3.0, 1.59],           # 1 change log
    [1.25, 2.2, 2.15, 1.09],           # 2 section 1 tests
    [2.5, 4.19],                       # 3 who runs them
    [0.95, 1.15, 2.15, 1.45, 0.99],    # 4 6.1 response time
    [0.95, 1.15, 2.1, 1.85, 0.64],     # 5 6.2 rules and agents
    [0.95, 1.15, 1.4, 2.0, 1.19],      # 6 6.3 events and workflows
    [0.95, 1.15, 0.95, 2.2, 1.44],     # 7 6.4 data and restore
    [0.95, 1.15, 2.8, 1.79],           # 8 6.5 security
    [0.9, 1.0, 1.45, 0.75, 1.6, 0.99], # 9 section 7 journeys
    [0.9, 1.3, 1.9, 1.7, 0.89],        # 10 section 8 platform
    [0.7, 1.7, 1.9, 2.39],             # 11 section 9 waves
    [0.8, 1.6, 1.0, 1.3, 0.45, 1.54],  # 12 10.1 legacy keys
    [1.4, 5.29],                       # 13 10.2 NFR coverage
    [1.3, 0.85, 2.8, 0.9, 0.84],       # 14 section 11 registers
]

P = Path(sys.argv[1])
d = docx.Document(str(P))
if len(d.tables) != len(SPEC):
    raise SystemExit(f"REFUSED: {len(d.tables)} tables, {len(SPEC)} widths")

W = qn("w:w")
for t, spec in zip(d.tables, SPEC):
    if len(t.columns) != len(spec):
        raise SystemExit(f"REFUSED: table {len(t.columns)} columns vs {len(spec)} widths")
    t.autofit = False
    tbl_pr = t._tbl.tblPr
    for old in tbl_pr.findall(qn("w:tblLayout")):
        tbl_pr.remove(old)
    layout = OxmlElement("w:tblLayout")
    layout.set(qn("w:type"), "fixed")
    tbl_pr.append(layout)
    for i, w in enumerate(spec):
        t.columns[i].width = Inches(w)
        for row in t.rows:
            row.cells[i].width = Inches(w)
    grid = t._tbl.tblGrid
    for i, col in enumerate(grid.findall(qn("w:gridCol"))):
        col.set(W, str(int(spec[i] * 1440)))
d.save(str(P))
print("WIDTHS", P, "tables", len(d.tables), "inches", [round(sum(s), 2) for s in SPEC])
