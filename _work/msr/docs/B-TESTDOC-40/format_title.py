"""Give the title lines of the generated .docx the look of the source title block.

The source sets its title lines as plain paragraphs with direct font sizes (26 pt bold for the
product name, 17 pt for the document name, 10 pt for the date line). The converter writes them
as plain paragraphs, so this script restores the three sizes on the new file only.
"""
import sys
from pathlib import Path

import docx
from docx.shared import Pt

P = Path(sys.argv[1])
d = docx.Document(str(P))

want = {
    "Recovery Workbench": (Pt(26), True),
    "Non-functional test plan": (Pt(17), False),
}
seen = 0
for p in d.paragraphs:
    txt = p.text.strip()
    if txt in want:
        size, bold = want[txt]
        for r in p.runs:
            r.font.size = size
            r.font.bold = bold
        seen += 1
    elif txt.startswith("SCB Collections and Recovery. Henka Group,") or txt.startswith("(C) Siam"):
        for r in p.runs:
            r.font.size = Pt(10)
        seen += 1
d.save(str(P))
print("TITLE FORMAT", P, "paragraphs touched", seen)
