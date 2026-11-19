import io

ROOT = r'C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14'
path = ROOT + r'\12 Project communication\Recovery Workbench Document Index v12.md'
text = io.open(path, encoding='utf-8-sig').read()
repl = {
    'Recovery Workbench Release Plan v3.pptx': 'Recovery Workbench Release Plan v4.pptx',
    'Recovery Workbench Release Plan v3.xlsx': 'Recovery Workbench Release Plan v4.xlsx',
    'Recovery Workbench Dependency Map v2.xlsx': 'Recovery Workbench Dependency Map v3.xlsx',
    'Recovery Workbench Build Sequence Epic 1 and Epic 2 v4.xlsx': 'Recovery Workbench Build Sequence Epic 1 and Epic 2 v5.xlsx',
    'Recovery Workbench Story Build Order v1.docx': 'Recovery Workbench Story Build Order v2.docx',
    'Recovery Workbench Risks Assumptions Issues and Dependencies v2.xlsx': 'Recovery Workbench Risks Assumptions Issues and Dependencies v3.xlsx',
    'Recovery Workbench Cutover and Go Live Plan v2.docx': 'Recovery Workbench Cutover and Go Live Plan v3.docx',
    'Recovery Workbench Story Defects Epic 1 Epic 2 and Enablers v2.xlsx': 'Recovery Workbench Story Defects Epic 1 Epic 2 and Enablers v3.xlsx',
    'Recovery Workbench Controls Catalog v2.xlsx': 'Recovery Workbench Controls Catalog v3.xlsx',
}
for a, b in repl.items():
    if a not in text:
        print('not found', a)
    text = text.replace(a, b)
old = ('| 116 | Project hub for the squads | Every story, build note, code, term and original file in one page that works with no network and no sign-in. '
       'The v16 rebuild on the ACE re-base is outstanding; the v15 build in 14 Story Updates predates it. | Henka writing rules | Recovery Workbench Project Hub v14.html |')
new = ('| 116 | Project hub for the squads | Every story, build note, code, term and original file in one page that works with no network and no sign-in. '
       'Version 16 is the ACE re-base of 15 November 2026: 323 live stories, the 30 recovery.v_ace_* views and the eight load stories removed. | Henka writing rules | '
       '14 Story Updates\\Recovery Workbench Project Hub v16.html |')
if old not in text:
    print('hub row not found')
text = text.replace(old, new)
io.open(path, 'w', encoding='utf-8', newline='\n').write(text)
print('updated index')
