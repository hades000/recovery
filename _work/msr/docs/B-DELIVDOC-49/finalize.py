"""Finishes Resource Plan v3: sheet order, column widths, core properties, name scan (scratch, B-DELIVDOC-49)."""
import re
from pathlib import Path
import openpyxl

V3 = Path(r"11 Delivery and operations/Recovery Workbench Resource Plan and Team Structure v3.xlsx")
V2 = Path(r"11 Delivery and operations/Recovery Workbench Resource Plan and Team Structure v2.xlsx")
TOOL = "T3 Code / OpenCode / DeepSeek v4.1 Flash"

wb = openpyxl.load_workbook(V3)
order = ["Read me", "Team", "People by month", "Structure", "Accountability",
         "Ownership by team type", "Services and squads", "Team types and resources"]
assert set(order) == set(wb.sheetnames), wb.sheetnames
wb._sheets = [wb[n] for n in order]

widths = {
    "Read me": {"A": 44, "B": 34, "C": 96, "D": 52},
    "Ownership by team type": {"A": 34, "B": 46, "C": 48, "D": 82, "E": 74, "F": 56},
    "Services and squads": {"A": 8, "B": 20, "C": 20, "D": 8, "E": 52, "F": 46, "G": 12, "H": 12,
                            "I": 12, "J": 22, "K": 14, "L": 34, "M": 16, "N": 16},
    "Team types and resources": {"A": 26, "B": 44, "C": 62, "D": 22, "E": 70, "F": 44},
}
for name, cols in widths.items():
    ws = wb[name]
    for col, w in cols.items():
        ws.column_dimensions[col].width = w
    ws.freeze_panes = None

p = wb.properties
p.creator = "Henka Group and SCB Collections and Recovery"
p.lastModifiedBy = TOOL
p.title = "Recovery Workbench Resource Plan and Team Structure v3"
p.subject = "D-RCV-60 microservice realignment"
p.description = ("Resource plan and team structure in the 19-service shape. Suggested ownership by team type. "
                 "Decision D-RCV-60. Tool: " + TOOL)
p.keywords = "D-RCV-60; resource plan; team structure; RWB; 19 services"
p.category = "Delivery and operations"
p.revision = 3
wb.save(V3)

# --- verification: kept sheets unchanged, no person name anywhere
name_rx = re.compile(r"\b(?:Mr|Ms|Mrs|Dr)\.?\s+[A-Z]|\b[A-Z][a-z]+\s+[A-Z][a-z]+\b")
allow = {"Collections Recovery", "Recovery Workbench", "Henka Group", "Siam Commercial", "Commercial Bank", "Pte Ltd",
         "Recovery Squad", "Recovery Tech", "Product Owner", "Program Manager", "Business Architect", "Solution Architect",
         "Business Analyst", "Business Lead", "Tech Lead", "Back End", "Front End", "QA Engineer", "Release Owner",
         "Common Module", "Collection Squad", "Data Engineering", "Enterprise AI", "Autonomous Ops", "Business Testers",
         "Reference Data", "Application Owner", "Supporting Teams", "Task Queue", "Draft Status", "Change Log", "Read Me",
         "Story Slices", "Legacy Stories", "Not Specified", "Total Counted", "Shared Teams", "Full Time", "Delivery Lead",
         "Enterprise Architecture", "Acc Arch", "Owner Role", "No Module", "Source Module", "Suggested Owner", "Work Type",
         "Day Work", "Decision Log", "Weekly Status", "Sponsor Reviews", "Business Decisions", "Case Workflow",
         "Data Engine", "Document Hub", "Decision Center", "Debt Sale", "Guarantee Claim", "Rule Package", "Design Sign",
         "Story Ready", "Story Done", "Rule Loads", "Weekly Status", "ACE Common", "ACE Team", "SCB IT", "Debt Recovery",
         "Debt Recovery Management Office", "Business Analyst For", "Release Go", "ACE Database", "Kafka Platform",
         "Service Template", "Service Contract", "Platform Team", "Qa Team", "Devops Team", "Tech Lead Three"}

a = openpyxl.load_workbook(V2)
b = openpyxl.load_workbook(V3)
kept = ["Team", "People by month", "Structure", "Accountability"]
diffs = []
for name in kept:
    wa, wbk = a[name], b[name]
    if (wa.max_row, wa.max_column) != (wbk.max_row, wbk.max_column):
        diffs.append(f"{name}: shape {(wa.max_row, wa.max_column)} -> {(wbk.max_row, wbk.max_column)}")
    for r in range(1, wa.max_row + 1):
        for c in range(1, wa.max_column + 1):
            if wa.cell(r, c).value != wbk.cell(r, c).value:
                diffs.append(f"{name}!{wa.cell(r, c).coordinate}: {wa.cell(r, c).value!r} -> {wbk.cell(r, c).value!r}")
print("KEPT-SHEET DIFFS:", len(diffs))
for d in diffs[:20]:
    print("  ", d)

hits = []
for ws in b.worksheets:
    for row in ws.iter_rows():
        for cell in row:
            if isinstance(cell.value, str):
                for m in name_rx.finditer(cell.value):
                    t = m.group(0)
                    if not any(x.lower() in t.lower() for x in allow):
                        hits.append(f"{ws.title}!{cell.coordinate}: {t} | {cell.value[:90]}")
print("NAME-LIKE HITS:", len(hits))
for h in hits[:40]:
    print("  ", h)

print("SHEETS:", b.sheetnames)
print("PROPS:", b.properties.creator, "|", b.properties.lastModifiedBy, "|", b.properties.title, "|",
      b.properties.revision)
