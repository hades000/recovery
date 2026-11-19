import sys, zipfile, re
z = zipfile.ZipFile(sys.argv[1])
print(z.namelist())
x = z.read('word/document.xml').decode('utf8')
paras = re.findall(r'<w:p[ >].*?</w:p>', x, re.S)
for i, p in enumerate(paras):
    t = ''.join(re.findall(r'<w:t(?: [^>]*)?>([^<]*)</w:t>', p))
    if t.strip(): print(i, t)
print(z.read('docProps/core.xml').decode())
