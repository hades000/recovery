import sys, zipfile, re, html
z = zipfile.ZipFile(sys.argv[1])
part = sys.argv[2] if len(sys.argv) > 2 else 'word/document.xml'
core = z.read('docProps/core.xml').decode('utf-8')
print('core title:', re.findall(r'<dc:title>(.*?)</dc:title>', core))
x = z.read(part).decode('utf-8')
tag = 'w:p' if part.startswith('word') else 'a:p'
for i, p in enumerate(re.findall(r'<%s[ >].*?</%s>' % (tag, tag), x, flags=re.S)):
    t = html.unescape(''.join(re.findall(r'<(?:w|a):t(?: [^>]*)?>([^<]*)</(?:w|a):t>', p)))
    if t.strip():
        print('P%d %s' % (i, t))
