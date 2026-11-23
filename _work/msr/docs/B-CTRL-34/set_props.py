"""Set document properties on the new version only (no person names, D-RCV-60 stamped)."""
import sys

import docx

path = sys.argv[1]
d = docx.Document(path)
cp = d.core_properties
print("before:", repr(cp.author), repr(cp.last_modified_by), repr(cp.title))
cp.author = "Henka Group"
cp.last_modified_by = "Henka Group"
cp.title = "Recovery Workbench Personal Data Protection Design v3"
cp.subject = "D-RCV-60 microservice realignment. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash."
cp.comments = "Version 3, 22 November 2026. Supersedes version 2. Status Draft."
cp.revision = 3
d.save(path)
c2 = docx.Document(path).core_properties
print("after:", repr(c2.author), repr(c2.last_modified_by), repr(c2.title))
