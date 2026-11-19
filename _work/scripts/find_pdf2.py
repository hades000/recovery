import pymupdf
doc = pymupdf.open(r'06 Data/Recovery Workbench Entity Relationship Diagram v4.pdf')
# find the page where business_unit appears (v_ace_account Section B fields)
for i, page in enumerate(doc):
    if 'business_unit' in page.get_text():
        print('business_unit on page', i + 1)
        page.get_pixmap(dpi=90).save(r'C:\Users\SahilMore\AppData\Local\Temp\opencode\pdf_sb.png')
        break
doc[95].get_pixmap(dpi=90).save(r'C:\Users\SahilMore\AppData\Local\Temp\opencode\pdf_notation.png')
print('ok')
