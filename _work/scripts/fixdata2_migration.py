import zipfile, re, shutil, os
from xml.dom import minidom
P = "06 Data/Recovery Workbench Data Migration Approach v3.docx"
z = zipfile.ZipFile(P)
parts = {n: z.read(n) for n in z.namelist()}
infos = z.infolist()
z.close()
x = parts['word/document.xml'].decode('utf8')
def rep(old, new):
    global x
    assert x.count(old) == 1, (old, x.count(old))
    x = x.replace(old, new)
rep('File extract, then retired (RWB-E1-012)', 'File extract, then retired through the Cutover plan (U5)')
rep('Lawsuits, hearings, notices and proof of delivery', 'Lawsuits, hearings and proof of delivery')
rep('<w:t>Which legacy systems are kept</w:t>',
    '<w:t>Which legacy systems are kept, and what the Workbench reads from each. Option A is superseded by D-RCV-35: the read path is the SELECT-only recovery.v_ace_* views, not a direct read of ACE or COLLINS</w:t>')
# DL43 row: copy the DL29 (last) row, then make DL29 keepNext
i = x.find('<w:t>DL29</w:t>')
rs = x.rfind('<w:tr>', 0, i); re_ = x.find('</w:tr>', i) + len('</w:tr>')
row29 = x[rs:re_]
row43 = row29.replace('<w:t>DL29</w:t>', '<w:t>DL43</w:t>').replace(
    '<w:t>Closed: EFS contact history is read through v_ace_efs_action, so no migration decision is needed</w:t>',
    '<w:t>Open with the ACE team lead, needed by 2026-11-21: the ACE team accepts the RWB-ACE-001 scope and dates (14 new ACE tables, 12 new columns). The Tier 2 reads this approach names depend on it</w:t>')
assert row43 != row29 and row43.count('DL43') == 1
row29k = row29.replace('<w:keepNext w:val="false"/>', '<w:keepNext/>')
x = x[:rs] + row29k + row43 + x[re_:]
parts['word/document.xml'] = x.encode('utf8')
minidom.parseString(parts['word/document.xml'])
tmp = P + '.tmp'
with zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as o:
    for inf in infos:
        o.writestr(inf, parts[inf.filename])
os.replace(tmp, P)
print('ok')
