import os, re, json, io, sys

ROOT = r'C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14'
FOLDERS = ['01 Decisions and governance', '02 Business architecture and process',
           '03 Requirements and specifications', '04 User stories', '05 Technical architecture',
           '06 Data', '07 Screens and experience', '08 AI and agents', '09 Testing and quality',
           '10 Policy, controls and compliance', '11 Delivery and operations',
           '12 Project communication', '15 ACE DB Alignment']

VER = re.compile(r'^(.*) v(\d+)$')

def family(stem):
    m = VER.match(stem)
    if m:
        return m.group(1), int(m.group(2))
    return stem, 0

picked = {}
for folder in FOLDERS:
    full = os.path.join(ROOT, folder)
    for name in os.listdir(full):
        p = os.path.join(full, name)
        if not os.path.isfile(p):
            continue
        if name.startswith('~$') or name.lower().endswith('.tmp'):
            continue
        stem, ext = os.path.splitext(name)
        base, ver = family(stem)
        key = (folder, base, ext.lower())
        if key not in picked or ver > picked[key][0]:
            picked[key] = (ver, name, os.path.getsize(p))

rows = []
for (folder, base, ext), (ver, name, size) in sorted(picked.items()):
    rows.append({'folder': folder, 'file': name, 'base': base, 'ver': ver, 'size': size})

# drop hubs and the template copies of old index/control? keep current only
rows = [r for r in rows if 'Project Hub' not in r['file']]
print('files', len(rows), 'MB', round(sum(r['size'] for r in rows) / 1048576, 1))
for r in rows:
    print(r['folder'][:2], '|', r['file'], '|', round(r['size']/1024), 'KB')
json.dump(rows, io.open(r'_work\scripts\manifest_candidate.json', 'w', encoding='utf-8'), indent=1)
