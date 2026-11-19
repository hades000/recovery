import openpyxl

ROOT = r'C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14'
path = ROOT + r'\12 Project communication\Recovery Workbench Document Control Sheet v11.xlsx'
wb = openpyxl.load_workbook(path)
ws = wb['Control sheet']
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
    'Recovery Workbench Project Hub v14.html': 'Recovery Workbench Project Hub v16.html',
}
changed = 0
for row in ws.iter_rows(min_row=5, max_row=ws.max_row):
    for cell in row:
        if isinstance(cell.value, str):
            new = cell.value
            for a, b in repl.items():
                new = new.replace(a, b)
            if new != cell.value:
                cell.value = new
                changed += 1
# hub comment
for row in ws.iter_rows(min_row=5, max_row=ws.max_row):
    if row[3].value and 'Project hub' in str(row[3].value):
        row[10].value = ('Version 16 is the ACE re-base of 15 November 2026: 323 live stories, the 30 recovery.v_ace_* views '
                         'and the eight load stories removed. File is in 14 Story Updates.')
        print('hub row', row[0].value, row[4].value)
wb.save(path)
print('cells changed', changed)
