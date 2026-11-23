import docx
for p in ["11 Delivery and operations/Recovery Workbench Engineering Practices v6.docx","11 Delivery and operations/Recovery Workbench Cutover and Go Live Plan v4.docx","11 Delivery and operations/Recovery Workbench Cutover and Go Live Plan v3.docx"]:
    d=docx.Document(p); c=d.core_properties
    print(p, "|", c.title, "|", c.author, "|", c.last_modified_by, "|", c.revision, "|", c.created, "|", c.modified, "|", c.comments, "|", c.subject)
