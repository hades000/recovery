import zipfile, re, sys, html
p = sys.argv[1]
z = zipfile.ZipFile(p)
x = z.read('word/document.xml').decode('utf-8')
body = x.split('<w:body>')[1]
# iterate top-level paragraphs and tables
i = 0
for m in re.finditer(r'<w:p[ >].*?</w:p>|<w:tbl>.*?</w:tbl>', body, re.S):
    blk = m.group(0)
    if blk.startswith('<w:tbl>'):
        for r in re.findall(r'<w:tr[ >].*?</w:tr>', blk, re.S):
            cells = re.findall(r'<w:tc>.*?</w:tc>', r, re.S)
            print('  T| ' + ' | '.join(html.unescape(''.join(re.findall(r'<w:t[^>]*>([^<]*)</w:t>', c))) for c in cells))
    else:
        st = re.search(r'<w:pStyle w:val="([^"]+)"', blk)
        t = html.unescape(''.join(re.findall(r'<w:t[^>]*>([^<]*)</w:t>', blk)))
        if t.strip():
            print(f'[{st.group(1) if st else "-"}] {t}')
