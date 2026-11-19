import sys, zipfile, re
from xml.etree import ElementTree as ET

p = sys.argv[1]
z = zipfile.ZipFile(p)
xml = z.read('word/document.xml')
root = ET.fromstring(xml)
ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
out = []
for para in root.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p'):
    text = ''.join(t.text or '' for t in para.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t'))
    if text.strip():
        out.append(text.strip())
print('\n'.join(out))
