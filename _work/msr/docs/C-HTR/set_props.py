"""Set the core properties of the new docx only, and read back what the document holds.

The source file carries a person name in its properties; the new version names no person,
so the properties are replaced with the document and the tool line.
"""
import datetime
import docx

PATH = "04 User stories/Recovery Workbench How To Read The Acceptance Criteria v2.docx"
d = docx.Document(PATH)
cp = d.core_properties
cp.title = "Recovery Workbench How To Read The Acceptance Criteria v2"
cp.subject = "How to read the acceptance criteria of the 19 Recovery services (D-RCV-60)"
cp.author = "SCB Collections and Recovery, Henka Group"
cp.last_modified_by = "T3 Code / OpenCode / DeepSeek v4.1 Flash"
cp.category = "User stories"
cp.comments = "Version 2. D-RCV-60 microservice realignment. Draft, no approval recorded."
cp.keywords = "Recovery Workbench; acceptance criteria; slices; origin tags; D-RCV-60"
cp.revision = 2
cp.created = datetime.datetime(2026, 11, 22, 9, 0, 0)
cp.modified = datetime.datetime(2026, 11, 22, 9, 0, 0)
cp.last_printed = datetime.datetime(2026, 11, 22, 9, 0, 0)
d.save(PATH)

c = docx.Document(PATH).core_properties
print("title:", c.title)
print("author:", c.author)
print("lastmod:", c.last_modified_by)
print("revision:", c.revision)
