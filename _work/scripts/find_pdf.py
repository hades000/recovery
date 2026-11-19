import pymupdf
doc = pymupdf.open(r'06 Data/Recovery Workbench Entity Relationship Diagram v4.pdf')
hits = {}
for i, page in enumerate(doc):
    t = page.get_text()
    for key in ('All 104 references', 'The 30 ACE source views', 'Notation and legend'):
        if key in t and key not in hits:
            hits[key] = i
print(hits)
for key, i in hits.items():
    pix = doc[i].get_pixmap(dpi=90)
    name = key.split()[1] if key.startswith('The') else key.split()[0]
    pix.save(r'C:\Users\SahilMore\AppData\Local\Temp\opencode\pdf_hit_%s.png' % name)
