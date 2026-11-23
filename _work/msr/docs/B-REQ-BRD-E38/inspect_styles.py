import zipfile, re
p = r'03 Requirements and specifications/Recovery Workbench Epics 3 to 8 Specification v3.docx'
z = zipfile.ZipFile(p)
x = z.read('word/styles.xml').decode('utf-8')
for m in re.finditer(r'<w:style [^>]*w:styleId="([^"]+)"[^>]*>(.{0,400}?)</w:style>', x, re.S):
    sid, body = m.group(1), m.group(2)
    n = re.search(r'<w:name w:val="([^"]+)"', body)
    print(sid, '|', n.group(1) if n else '')
