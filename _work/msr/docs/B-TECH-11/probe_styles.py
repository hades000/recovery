"""Probe the v2 source styles and numbering (scratch, read-only on the source)."""
import re
import sys
from pathlib import Path

import docx

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "22 Microservice Realignment" / "compat"))
import office_write  # noqa: E402

print("GUARD:", office_write._guard.__doc__)

SRC = ROOT / "05 Technical architecture" / "Recovery Workbench Availability Performance and Recovery Design v2.docx"
d = docx.Document(str(SRC))
print("STYLES:", [s.name for s in d.styles])
for p in d.paragraphs:
    if p.style.name == "List Paragraph":
        pPr = p._p.pPr
        xml = pPr.xml if pPr is not None else ""
        print("NUMID", re.findall(r'w:numId w:val="(\d+)"', xml), re.findall(r'w:ilvl w:val="(\d+)"', xml), p.text[:50])
print("HEADING STYLE XML:")
st = d.styles["Heading 1"]
print(st.element.xml[:600])
