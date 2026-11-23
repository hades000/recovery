import zipfile, re
p='06 Data/Recovery Workbench Data Migration Approach v3.docx'
x=zipfile.ZipFile(p).read('word/styles.xml').decode('utf-8')
for m in re.finditer(r'w:styleId="([^"]+)"(.*?)</w:style>', x, re.S):
    nm = re.search(r'<w:name w:val="([^"]+)"', m.group(2))
    print(m.group(1), '|', nm.group(1) if nm else '')
