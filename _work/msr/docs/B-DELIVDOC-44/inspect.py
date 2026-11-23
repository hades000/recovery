import docx, zipfile, sys
p = "11 Delivery and operations/Recovery Workbench Engineering Practices v5.docx"
d = docx.Document(p)
cp = d.core_properties
print("title:", cp.title)
print("author:", cp.author)
print("lastmod:", cp.last_modified_by)
print("subject:", cp.subject)
print("category:", cp.category)
print("comments:", cp.comments)
print("created:", cp.created)
print("modified:", cp.modified)
print("revision:", cp.revision)
print("STYLES:", [(s.name, s.type) for s in d.styles if s.name])
z = zipfile.ZipFile(p)
print("PARTS:", z.namelist())
