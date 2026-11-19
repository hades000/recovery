import re, os

ROOT = r'C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14'
P = os.path.join(ROOT, r'12 Project communication\Recovery Workbench Document Index v12.md')
txt = open(P, encoding='utf-8').read()
row_re = re.compile(r'^\| (\d+) \| (.+?) \| (.+?) \| (.+?) \| (.+?) \|$')
listed = set()
for line in txt.split('\n'):
    m = row_re.match(line)
    if m:
        for n in m.group(5).split(','):
            listed.add(n.strip())
print('listed count', len(listed))

folders = ['01 Decisions and governance', '02 Business architecture and process',
           '03 Requirements and specifications', '04 User stories', '05 Technical architecture',
           '06 Data', '07 Screens and experience', '08 AI and agents', '09 Testing and quality',
           '10 Policy, controls and compliance', '11 Delivery and operations',
           '12 Project communication', '15 ACE DB Alignment']

cur = {}
for folder in folders:
    d = os.path.join(ROOT, folder)
    for f in os.listdir(d):
        if not os.path.isfile(os.path.join(d, f)):
            continue
        m = re.match(r'^(.*) v(\d+)\.(\w+)$', f)
        key = (m.group(1), m.group(3)) if m else (f, '')
        v = int(m.group(2)) if m else -1
        if key not in cur or v > cur[key][0]:
            cur[key] = (v, f)

un = sorted(v[1] for v in cur.values() if v[1] not in listed)
print('current-version files on disk not listed:', len(un))
for f in un:
    print('  ', f)
