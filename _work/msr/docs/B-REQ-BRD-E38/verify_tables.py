from docx import Document
p = r'03 Requirements and specifications/Recovery Workbench Business Requirements Epics 3 to 8 v1.docx'
d = Document(p)
for i, t in enumerate(d.tables):
    print(i, len(t.rows), len(t.columns), '|', ' / '.join(c.text[:28] for c in t.rows[0].cells)[:110])
