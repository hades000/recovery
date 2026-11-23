import docx, re, sys
d = docx.Document('09 Testing and quality/Recovery Workbench Test Strategy v2.docx')
for i in (1, 2, 3):
    x = d.paragraphs[i]._p.xml
    x = re.sub(r' xmlns:[a-z0-9]+="[^"]*"', '', x)
    print('=== para', i)
    print(x[:900])
    print()
