import docx
d = docx.Document('09 Testing and quality/Recovery Workbench Test Strategy v3.docx')
print('paras', len(d.paragraphs), 'tables', len(d.tables))
for i, p in enumerate(d.paragraphs[:8]):
    print(i, p.style.name, '|', p.text[:90])
print('---')
for i, t in enumerate(d.tables):
    print('table', i, len(t.rows), 'x', len(t.columns), '|', t.rows[0].cells[0].text, '/', t.rows[0].cells[-1].text)
print('--- headings ---')
for p in d.paragraphs:
    if p.style.name.startswith('Heading'):
        print(p.style.name, '|', p.text)
