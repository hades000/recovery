"""Probe the source v2 docx styles: Normal, Heading 1-3, Title; fonts and sizes."""
import re
import docx

SRC = r"05 Technical architecture\Recovery Workbench Document Management Design v2.docx"


def clean(x):
    s = x.xml
    return re.sub(r'xmlns:[a-z0-9]+="[^"]*"\s*', "", s)


d = docx.Document(SRC)
for name in ("Normal", "Title", "Heading 1", "Heading 2", "Heading 3", "List Paragraph"):
    st = d.styles[name]
    print("###", name)
    print(clean(st.element)[:1400])
    print()

print("### docDefaults")
styles_el = d.styles.element
dd = styles_el.find("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}docDefaults")
print(clean(dd)[:1400] if dd is not None else "none")
