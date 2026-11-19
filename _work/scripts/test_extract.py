import os, sys
sys.path.insert(0, r'_work\scripts\hubgen')
import extract

ROOT = r'C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14'
tests = [
    r'01 Decisions and governance\Recovery Workbench Admin and Access Model v5.docx',
    r'01 Decisions and governance\Recovery Workbench Decision Log v9.xlsx',
    r'02 Business architecture and process\Recovery Workbench Business Architecture v4.pptx',
    r'07 Screens and experience\Recovery Workbench Screen Specifications v1.html',
    r'04 User stories\Recovery Workbench User Stories Epic 1 v8.md',
    r'06 Data\Recovery Workbench Physical Schema v5.sql',
    r'04 User stories\Recovery Workbench ACE Team Stories v1.md',
]
for rel in tests:
    p = os.path.join(ROOT, rel)
    secs = extract.extract_file(p, os.path.splitext(p)[1])
    print('===', rel, 'secs', len(secs), 'chars', sum(len(s['t']) for s in secs))
    for s in secs[:3]:
        print('  [%s] %s | %s' % (s['l'], s['h'][:70], s['t'][:120].replace('\n', ' / ')))
