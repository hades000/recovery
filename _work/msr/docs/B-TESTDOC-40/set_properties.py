"""Set the document properties of the generated .docx to the organisation and the tool.

The source template carries a person name in author and last-modified-by. The new file must
carry no name of a person, so both are replaced and the title, revision and dates are set to
this version. Only the new v3 output is written.
"""
import sys
from datetime import datetime
from pathlib import Path

import docx

P = Path(sys.argv[1])
d = docx.Document(str(P))
cp = d.core_properties
cp.author = "Henka Group"
cp.last_modified_by = "T3 Code / OpenCode / DeepSeek v4.1 Flash"
cp.title = "Recovery Workbench Non Functional Test Plan v3"
cp.subject = "D-RCV-60 microservice realignment"
cp.comments = "Version 3. Supersedes v2 of 28 October 2026. Draft."
cp.category = "Test plan"
cp.keywords = "D-RCV-60; non-functional test plan; 19 services"
cp.revision = 3
cp.modified = datetime(2026, 11, 22, 0, 0, 0)
d.save(str(P))
print("PROPERTIES", P, "author", cp.author, "| last_modified_by", cp.last_modified_by)
