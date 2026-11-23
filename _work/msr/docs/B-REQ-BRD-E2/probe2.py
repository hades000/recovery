import docx

p = "03 Requirements and specifications/Recovery Workbench Business Requirements Epic 2 v3.docx"
d = docx.Document(p)
body = d.element.body
from docx.table import Table
from docx.text.paragraph import Paragraph
items = []
for child in body.iterchildren():
    tag = child.tag.split("}")[-1]
    if tag == "p":
        par = Paragraph(child, d)
        if par.text.strip():
            items.append(("P", par.style.name, par.text[:90]))
    elif tag == "tbl":
        t = Table(child, d)
        items.append(("T", "", f"{len(t.rows)}x{len(t.columns)} | " + " / ".join(c.text[:18] for c in t.rows[0].cells)))
print("blocks", len(items), "paragraphs", sum(1 for i in items if i[0]=="P"), "tables", sum(1 for i in items if i[0]=="T"))
for i in items[:14]:
    print(i)
print("...")
for i in items[-6:]:
    print(i)
print("headings:", [i[2][:60] for i in items if i[0]=="P" and i[1].startswith("Heading")])
