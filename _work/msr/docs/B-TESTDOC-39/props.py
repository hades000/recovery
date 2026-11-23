import docx
d = docx.Document('09 Testing and quality/Recovery Workbench Test Strategy v2.docx')
cp = d.core_properties
for f in ('author', 'last_modified_by', 'title', 'subject', 'category', 'comments', 'keywords',
          'created', 'modified', 'revision'):
    print(f, '=', repr(getattr(cp, f)))
