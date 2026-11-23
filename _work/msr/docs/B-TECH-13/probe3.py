"""Probe the source v2 docx heading style definitions and document defaults."""
import re
import docx

SRC = r"05 Technical architecture\Recovery Workbench Document Management Design v2.docx"


def clean(x):
    s = x.xml
    return re.sub(r'xmlns:[a-z0-9]+="[^"]*"\s*', "", s)


d = docx.Document(SRC)
for s in d.styles:
    if s.name in ("Heading 1", "Heading 2", "Heading 3", "List Paragraph"):
        print("###", s.name, s.style_id)
        print(clean(s.element)[:1600])
        print()

dd = d.styles.element.find("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}docDefaults")
print("### docDefaults")
print(clean(dd)[:1600] if dd is not None else "none")
