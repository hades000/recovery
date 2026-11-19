import zipfile, shutil, os, tempfile
from xml.dom import minidom
P = '01 Decisions and governance/Recovery Workbench Admin and Access Model v5.docx'
OLD = 'it has no direct read of a public ACE table and no write on any table, so a direct public read fails in the catalog.'
NEW = 'it has no direct read of a public ACE table and no write on any ACE table or view, so a direct read of a public table fails at the database.'
zin = zipfile.ZipFile(P)
x = zin.read('word/document.xml').decode('utf-8')
assert x.count(OLD) == 1
x = x.replace(OLD, NEW)
minidom.parseString(x.encode('utf-8'))  # validate
fd, tmp = tempfile.mkstemp(suffix='.docx', dir=os.path.dirname(P)); os.close(fd)
with zipfile.ZipFile(tmp, 'w') as zout:
    for item in zin.infolist():
        data = x.encode('utf-8') if item.filename == 'word/document.xml' else zin.read(item.filename)
        zout.writestr(item, data, compress_type=item.compress_type)
zin.close()
shutil.move(tmp, P)
print('ok')
