# Set the document properties of the v3 deck: no person name, the realignment decision and the tool line.
import datetime
from pptx import Presentation

P = r"11 Delivery and operations/Recovery Workbench Run Operating Model v3.pptx"
prs = Presentation(P)
cp = prs.core_properties
cp.title = "Recovery Workbench Run Operating Model v3"
cp.subject = "D-RCV-60 microservice realignment"
cp.author = "Henka Group"
cp.last_modified_by = "T3 Code / OpenCode / DeepSeek v4.1 Flash"
cp.category = "Run operating model"
cp.keywords = "D-RCV-60; microservice realignment; run book per service"
cp.comments = ("3, 22 November 2026, D-RCV-60 microservice realignment, "
               "T3 Code / OpenCode / DeepSeek v4.1 Flash")
cp.revision = 3
cp.modified = datetime.datetime(2026, 11, 22, 0, 0, 0)
prs.save(P)
print("PROPS", P)
