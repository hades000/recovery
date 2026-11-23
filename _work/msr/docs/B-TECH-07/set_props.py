"""Set the document properties of the new .docx and check the built file.

The family inherits author and last-modified-by from version 3, which carries a person's
name; AGENTS.md rule 4 forbids a person name in any output, so the properties of the new
version are set to the organisation and the tool. Content is untouched.
"""
import sys

import docx

path = sys.argv[1]
d = docx.Document(path)
c = d.core_properties
c.author = "Henka Group"
c.last_modified_by = "T3 Code / OpenCode / DeepSeek v4.1 Flash"
c.title = "Recovery Workbench rules engine design"
c.subject = "Recovery Workbench rules engine design"
c.comments = "D-RCV-60 microservice realignment. Version 4, 22 November 2026."
c.category = "Technical architecture"
c.revision = 4
c.modified = c.modified.replace(year=2026, month=11, day=22)
d.save(path)

chk = docx.Document(path)
p = chk.core_properties
print("PROPS", p.author, "|", p.last_modified_by, "|", p.title, "|", p.revision, "|", p.modified)
print("paragraphs", len(chk.paragraphs), "tables", len(chk.tables))
print("first 3 paragraphs:", [x.text for x in chk.paragraphs[:3]])
heads = [x.text for x in chk.paragraphs if x.style.name.startswith("Heading")]
print("headings", len(heads), heads[:4])
