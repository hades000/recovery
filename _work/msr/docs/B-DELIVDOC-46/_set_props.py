"""Replace the person name and the version in the core properties of the new version only."""
import datetime
import sys

import docx

path = sys.argv[1]
d = docx.Document(path)
cp = d.core_properties
cp.title = "Recovery Workbench Cutover and Go Live Plan v4"
cp.subject = "Cutover and go-live plan per wave for the 19 Recovery services (D-RCV-60)"
cp.author = "SCB Collections and Recovery, Henka Group"
cp.last_modified_by = "T3 Code / OpenCode / DeepSeek v4.1 Flash"
cp.category = "Delivery and operations"
cp.comments = "Version 4. D-RCV-60 microservice realignment. Draft, no approval recorded."
cp.keywords = "Recovery Workbench; cutover; go-live; D-RCV-60"
cp.revision = 4
cp.created = datetime.datetime(2026, 11, 22, 9, 0, 0)
cp.modified = datetime.datetime(2026, 11, 22, 9, 0, 0)
cp.last_printed = datetime.datetime(2026, 11, 22, 9, 0, 0)
d.save(path)
c = docx.Document(path).core_properties
print("title:", c.title)
print("author:", c.author)
print("lastmod:", c.last_modified_by)
print("revision:", c.revision)
print("created:", c.created)
print("modified:", c.modified)
