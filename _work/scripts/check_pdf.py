import pymupdf, os
src = r'06 Data/Recovery Workbench Entity Relationship Diagram v4.pdf'
doc = pymupdf.open(src)
print('pages', doc.page_count, 'size', os.path.getsize(src))
for i, page in enumerate(doc):
    txt = page.get_text().strip().replace('\n', ' | ')
    print(i + 1, round(page.rect.width), round(page.rect.height), txt[:160])
for n in (0, 1, 2):
    pix = doc[n].get_pixmap(dpi=100)
    pix.save(r'C:\Users\SahilMore\AppData\Local\Temp\opencode\pdf_p%d.png' % (n + 1))
