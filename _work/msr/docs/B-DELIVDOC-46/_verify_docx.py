import zipfile, re, docx
p = "11 Delivery and operations/Recovery Workbench Cutover and Go Live Plan v4.docx"
z = zipfile.ZipFile(p)
blob = b" ".join(z.read(n) for n in z.namelist() if n.endswith(".xml")).decode("utf-8", "ignore")
print("person name present:", "Rajdeep" in blob or "Ghai" in blob)
d = docx.Document(p)
print("paragraphs:", len(d.paragraphs), "tables:", len(d.tables))
print("headings:", [x.text for x in d.paragraphs if x.style.name.startswith("Heading")][:8])
print("first two paragraphs:", [x.text for x in d.paragraphs[:2]])
# table widths sanity
print("table shapes:", [(len(t.rows), len(t.columns)) for t in d.tables])
