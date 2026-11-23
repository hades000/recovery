import collections, re, zipfile

SRC = "09 Testing and quality/Recovery Workbench Test Data Plan v3.docx"
z = zipfile.ZipFile(SRC)
d = z.read("word/document.xml").decode("utf-8")
print("numId in body:", collections.Counter(re.findall(r'w:numId w:val="(\d+)"', d)))
n = z.read("word/numbering.xml").decode("utf-8")
print("num ids:", re.findall(r'<w:num w:numId="(\d+)"', n))
print("abstract:", re.findall(r'<w:abstractNum w:abstractNumId="(\d+)"', n))
print("bullet in numbering:", n.count('w:val="bullet"'))
