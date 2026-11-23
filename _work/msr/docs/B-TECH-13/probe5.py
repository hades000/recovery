"""Probe table cell run properties (size, colour, bold) in the source v2 docx."""
import re
import docx

SRC = r"05 Technical architecture\Recovery Workbench Document Management Design v2.docx"


def clean(x):
    s = x.xml
    return re.sub(r'xmlns:[a-z0-9]+="[^"]*"\s*', "", s)


d = docx.Document(SRC)
t = d.tables[0]
print("HEADER CELL 0,0:")
print(clean(t.rows[0].cells[0]._tc)[:1200])
print("\nBODY CELL 1,0:")
print(clean(t.rows[1].cells[0]._tc)[:1200])
print("\nBODY CELL 1,1:")
print(clean(t.rows[1].cells[1]._tc)[:1200])
