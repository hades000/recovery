import docx, re
d = docx.Document('09 Testing and quality/Recovery Workbench Test Strategy v2.docx')
for s in d.styles:
    if s.type == 1:
        el = s.element
        nm = el.find('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}name')
        print(repr(s.name), '->', nm.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val') if nm is not None else None)
print('has Table Grid:', any(s.name == 'Table Grid' for s in d.styles))
