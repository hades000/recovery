import io
import glob
import docx

files = [
    r'05 Technical architecture\Recovery Workbench Technical Specifications by Module v3\Recovery Workbench TSD P1 Recovery core and data.docx',
]
files += glob.glob(r'05 Technical architecture\Recovery Workbench Technical Specifications by Module v3\*.docx')
for f in files:
    try:
        d = docx.Document(f)
    except Exception as e:
        print('ERR', f, e)
        continue
    print('=' * 20, f)
    for p in d.paragraphs:
        t = p.text.strip()
        if t:
            print(t)
    for ti, table in enumerate(d.tables):
        print('--- table', ti)
        for row in table.rows:
            print(' | '.join(c.text.strip().replace('\n', ' ') for c in row.cells))
    break
