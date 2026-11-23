import re, zipfile

SRC = "09 Testing and quality/Recovery Workbench Test Data Plan v3.docx"
z = zipfile.ZipFile(SRC)
s = z.read("word/styles.xml").decode("utf-8")
styles = re.findall(r'w:styleId="([^"]+)"[^>]*>\s*<w:name w:val="([^"]+)"', s)
print("heading/list styles:")
for sid, name in styles:
    if "ead" in sid or "ead" in name or "ist" in sid:
        print(" ", sid, "->", name)
d = z.read("word/document.xml").decode("utf-8")
print("paras:", d.count("<w:p "), d.count("<w:p>"))
print("tables:", d.count("<w:tbl>"))
print("pStyle uses:", sorted(set(re.findall(r'w:pStyle w:val="([^"]+)"', d))))
