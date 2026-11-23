import docx, re, sys
d = docx.Document(sys.argv[1])
for i, p in enumerate(d.paragraphs[:12]):
    x = re.sub(r' xmlns:[a-z0-9]+="[^"]*"', '', p._p.xml)
    print('=== para', i, p.style.name, '|', p.text[:80])
    print(x[:700])
    print()
