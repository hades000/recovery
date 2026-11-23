"""Probe docDefaults size/font and body paragraph spacing of the source v2 docx."""
import re
import docx
from lxml import etree

SRC = r"05 Technical architecture\Recovery Workbench Document Management Design v2.docx"


def clean(x):
    s = x.xml if hasattr(x, "xml") else etree.tostring(x, pretty_print=True).decode()
    return re.sub(r'xmlns:[a-z0-9]+="[^"]*"\s*', "", s)


d = docx.Document(SRC)
dd = d.styles.element.find("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}docDefaults")
print("### docDefaults")
print(clean(dd)[:1600])
print()
body = d.paragraphs[19]
print("### body para")
print(clean(body._p)[:900])
print()
print("### table rows x cols", [(len(t.rows), len(t.columns)) for t in d.tables])
