import io
import re

files = {
    'E1': r'04 User stories\Recovery Workbench User Stories Epic 1 v7.md',
    'E2': r'04 User stories\Recovery Workbench User Stories Epic 2 v5.md',
    'E38': r'04 User stories\Recovery Workbench User Stories Epics 3 to 8 v2.md',
    'TE': r'04 User stories\Recovery Workbench Technical Enabler Stories v5.md',
    'AD': r'04 User stories\Recovery Workbench Administration Stories v2.md',
    'DM': r'04 User stories\Recovery Workbench Data Migration Stories v2.md',
}
for k, f in files.items():
    txt = io.open(f, encoding='utf-8', errors='replace').read()
    ids = re.findall(r'RWB-(?:E\d|TE|AD|DM|ACE)-\d{3}', txt)
    uniq = sorted(set(ids))
    print(k, 'unique ids', len(uniq), 'first', uniq[:3], 'last', uniq[-3:])
    heads = re.findall(r'^#{2,3} (RWB-[^\n]+)', txt, re.M)
    print('  headings', len(heads), heads[:3])
