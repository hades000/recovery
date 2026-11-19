import sys, zipfile, re
f = sys.argv[1]
z = zipfile.ZipFile(f)
x = z.read('word/document.xml').decode('utf-8')
print(z.read('docProps/core.xml').decode('utf-8')[-600:])
body = x.split('<w:body>')[1]
# paragraphs, mark tables
idx = 0
for m in re.finditer(r'<w:p[ >].*?</w:p>|<w:tbl>|</w:tbl>|<w:tr[ >]|</w:tr>', body, re.S):
    s = m.group(0)
    if s == '<w:tbl>': print('[TBL]'); continue
    if s == '</w:tbl>': print('[/TBL]'); continue
    if s.startswith('<w:tr'): print('  [TR]'); continue
    if s == '</w:tr>': continue
    t = ''.join(re.findall(r'<w:t(?: [^>]*)?>([^<]*)</w:t>', s))
    if t.strip(): print(idx, t)
    idx += 1
