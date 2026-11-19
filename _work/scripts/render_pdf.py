import pymupdf
doc = pymupdf.open(r'06 Data/Recovery Workbench Entity Relationship Diagram v4.pdf')
for n in (0, 1, 3, 76):
    pix = doc[n].get_pixmap(dpi=90)
    pix.save(r'C:\Users\SahilMore\AppData\Local\Temp\opencode\pdf_p%d.png' % (n + 1))
print('ok')
