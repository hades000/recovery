"""D2-OVR: mark release dates tentative and clean the document properties of the v5 deck."""
import datetime
from pathlib import Path
from pptx import Presentation

OUT = Path(r"12 Project communication/Recovery Workbench Project Overview v5.pptx")
prs = Presentation(OUT)

# Slide 8 is the release plan table (index 7). The Release column is column 1.
table = None
for sh in prs.slides[7].shapes:
    if getattr(sh, "has_table", False) and sh.has_table:
        table = sh.table
if table is None:
    raise SystemExit("release table not found on slide 8")
marked = []
for r in range(1, len(table.rows)):
    cell = table.cell(r, 1)
    txt = cell.text.strip()
    if txt and "(tentative)" not in txt:
        cell.text = f"{txt} (tentative)"
        marked.append(cell.text)
print("MARKED", marked)

cp = prs.core_properties
cp.author = "SCB Collections and Recovery"
cp.last_modified_by = "T3 Code / OpenCode / DeepSeek v4.1 Flash"
cp.title = "Recovery Workbench Project Overview v5"
cp.subject = "SCB Collections and Recovery. Henka Group, 22 November 2026."
cp.comments = "D-RCV-60 microservice realignment. Draft. Supersedes version 4 of 28 October 2026."
cp.category = "Project communication"
cp.keywords = "Recovery Workbench; D-RCV-60; microservice realignment; version 5"
cp.revision = 5
cp.created = datetime.datetime(2026, 11, 22, 0, 0, 0)
cp.modified = datetime.datetime(2026, 11, 22, 0, 0, 0)
prs.save(OUT)
print("SAVED", OUT)
