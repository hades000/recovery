import re, zipfile

SRC = "09 Testing and quality/Recovery Workbench Test Data Plan v3.docx"
z = zipfile.ZipFile(SRC)
for name in z.namelist():
    if "footer" in name or "header" in name:
        t = z.read(name).decode("utf-8")
        txt = "".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", t))
        print(name, "->", repr(txt))
d = z.read("word/document.xml").decode("utf-8")
print("body text:", "".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", d))[:400])
