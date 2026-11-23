"""Check the docx for any leftover person name or e-mail anywhere in the package."""
import re
import sys
import zipfile

BAD = re.compile(rb'Rajdeep|Ghai|@[a-z0-9.-]+\.[a-z]{2,}', re.I)
path = sys.argv[1]
z = zipfile.ZipFile(path)
for n in z.namelist():
    data = z.read(n)
    for m in BAD.finditer(data):
        s = max(0, m.start() - 60)
        print('HIT', n, data[s:m.end() + 60])
print('files', len(z.namelist()))
