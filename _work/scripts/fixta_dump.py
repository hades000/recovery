import zipfile,re,sys
p=sys.argv[1]; part=sys.argv[2] if len(sys.argv)>2 else 'word/document.xml'
z=zipfile.ZipFile(p); x=z.read(part).decode('utf8')
if part.startswith('word'):
    body=x
    i=0
    for m in re.finditer(r'<w:tbl>.*?</w:tbl>|<w:p[ >].*?</w:p>',body,re.S):
        s=m.group(0)
        if s.startswith('<w:tbl>'):
            for r_i,row in enumerate(re.findall(r'<w:tr[ >].*?</w:tr>',s,re.S)):
                cells=[''.join(re.findall(r'<w:t[^>]*>([^<]*)</w:t>',c)) for c in re.findall(r'<w:tc>.*?</w:tc>',row,re.S)]
                print(f'{i} T{r_i}: '+' | '.join(cells))
        else:
            st=re.search(r'<w:pStyle w:val="([^"]+)"',s)
            print(f'{i} [{st.group(1) if st else ""}] '+''.join(re.findall(r'<w:t[^>]*>([^<]*)</w:t>',s)))
        i+=1
else:
    print(' / '.join(re.findall(r'<a:t>([^<]*)</a:t>',x)))
