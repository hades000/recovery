import zipfile, re
p = "11 Delivery and operations/Recovery Workbench Cutover and Go Live Plan v3.docx"
z = zipfile.ZipFile(p)
s = z.read("word/styles.xml").decode("utf-8")
for m in re.finditer(r'<w:style [^>]*w:styleId="([^"]+)"[^>]*>(.*?)</w:style>', s, re.S):
    if "heading" in m.group(1).lower() or "List" in m.group(1):
        nm = re.search(r'<w:name w:val="([^"]+)"', m.group(2))
        print(m.group(1), "->", nm.group(1) if nm else None)
print("names:", z.namelist())
