import re
import docx
from docx.oxml.ns import qn

d = docx.Document(r"05 Technical architecture/Recovery Workbench Error Handling and Resilience Standard v3.docx")
for p in d.part.package.parts:
    if "numbering" in str(p.partname):
        xml = p.blob.decode("utf-8")
        print("num -> abstract:", re.findall(r'<w:num w:numId="(\d+)"[^>]*>\s*<w:abstractNumId w:val="(\d+)"', xml))
        for m in re.finditer(r'<w:abstractNum w:abstractNumId="(\d+)".*?</w:abstractNum>', xml, re.S):
            print("abs", m.group(1), sorted(set(re.findall(r'<w:numFmt w:val="([a-zA-Z]+)"', m.group(0)))))

print("--- direct numPr in body (first three):")
n = 0
for p in d.paragraphs:
    np = p._p.find(".//" + qn("w:numPr"))
    if np is not None:
        print(p.style.name, re.findall(r'w:val="(\d+)"', np.xml), repr(p.text[:60]))
        n += 1
        if n >= 3:
            break

print("Table Grid style:", any(s.name == "Table Grid" for s in d.styles))
print("tables:", len(d.tables))
print("sectPr in body:", len(d.element.body.findall(qn("w:sectPr"))))
