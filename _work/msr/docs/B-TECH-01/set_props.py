"""Set document properties of the new docx: no person name, v4 title and date.

The docx family inherits author and last-modified-by properties from the template.
AGENTS.md rule 4 forbids a person name in any output, so the properties of the new
version are set to the organisation and the tool. Content is untouched.
"""
import sys

import docx

path = sys.argv[1]
d = docx.Document(path)
c = d.core_properties
c.author = "Henka Group"
c.last_modified_by = "T3 Code / OpenCode / DeepSeek v4.1 Flash"
c.title = "Recovery Workbench ACE Architecture Decision v4"
c.subject = "Recovery Workbench ACE architecture decision"
c.comments = "D-RCV-60 microservice realignment. Version 4, 22 November 2026."
c.category = "Architecture decision record"
c.revision = 4
c.modified = c.modified.replace(year=2026, month=11, day=22)
d.save(path)
check = docx.Document(path).core_properties
print("PROPS", path, "|", check.author, "|", check.last_modified_by, "|", check.title,
      "|", check.modified, "|", check.revision)
