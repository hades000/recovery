import zipfile, re
p = "11 Delivery and operations/Recovery Workbench Engineering Practices v5.docx"
z = zipfile.ZipFile(p)
s = z.read("word/styles.xml").decode("utf-8")
for m in re.finditer(r'<w:style [^>]*w:styleId="([^"]+)"[^>]*>(.*?)</w:style>', s, re.S):
    if "heading" in m.group(1).lower():
        nm = re.search(r'<w:name w:val="([^"]+)"', m.group(2))
        print(m.group(1), "->", nm.group(1) if nm else None)
print("numIds:", sorted(set(re.findall(r'<w:numId w:val="(\d+)"', z.read("word/numbering.xml").decode("utf-8")))))
