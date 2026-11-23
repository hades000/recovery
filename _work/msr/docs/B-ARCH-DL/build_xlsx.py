"""Build Recovery Workbench Decision Log v11 from v10 (WP B-ARCH-DL, D-RCV-60).

Never edits the source: v11 is created by compat/office_write.py copy first, then this
script changes the copy only.
"""
import math
from copy import copy
from datetime import datetime
from pathlib import Path

import openpyxl
from openpyxl.styles import Alignment, Font
from openpyxl.utils import get_column_letter

OUT = Path(r"01 Decisions and governance\Recovery Workbench Decision Log v11.xlsx")
TOOL = "T3 Code / OpenCode / DeepSeek v4.1 Flash"
H1 = "SCB Collections and Recovery. Henka Group, 22 November 2026."
H2 = "(C) Siam Commercial Bank and Henka Pte Ltd"
PLACE = "Not specified in the source documents (CG-B-ARCH-DL-1; ASM-B-ARCH-DL-2)"
DATE = datetime(2026, 11, 22)

wb = openpyxl.load_workbook(OUT)

# ---------------------------------------------------------------- properties
p = wb.properties
p.creator = "SCB Collections and Recovery"
p.lastModifiedBy = "SCB Collections and Recovery"
p.title = "Recovery Workbench Decision Log v11"
p.subject = "Decision D-RCV-60 microservice realignment"
p.description = "SCB Collections and Recovery, Henka Group, 22 November 2026."
p.keywords = "D-RCV-60; decision log; v11"
p.category = "Governance"

# ---------------------------------------------------------------- Read me sheet
readme = wb.create_sheet("Read me", 0)
readme.column_dimensions["A"].width = 150
readme["A1"] = H1
readme["A2"] = H2
readme["A3"] = None
readme["A4"] = ("Recovery Workbench Decision Log v11. Decision D-RCV-60. The next version of v10: "
                "every ID, number and date of v10 is kept, and only the rows this change log names change.")
readme["A5"] = "Tool: " + TOOL + "."
readme["A6"] = None
readme["A7"] = "Change log"
readme["A8"] = ("v11, 22 November 2026, D-RCV-60 microservice realignment, " + TOOL)
readme["A9"] = "v10, 15 November 2026: the source version, carried forward (41 open decisions, 22 decisions taken)."
readme["A10"] = None
readme["A11"] = "What changed in v11"
readme["A12"] = ("Decisions taken: D-RCV-60 and DL44 to DL49 are added, dated 22 November 2026; the sheet then holds "
                 "29 decisions taken.")
readme["A13"] = ("Decisions taken: D-RCV-36 is marked amended at T1 and T2 by D-RCV-60, in its Decision cell and its "
                 "\"What it means for the build\" cell; no other word of the row is changed.")
readme["A14"] = ("Open decisions and By owner: an owner label that named an individual in v10 now carries the "
                 "placeholder of Template and Rules \u00a7R9 (CG-B-ARCH-DL-1; ASM-B-ARCH-DL-2). Counts, earliest dates "
                 "and decision IDs are unchanged.")
readme["A15"] = ("Release dates named in a row carry (tentative) (DL48; ASM-B-ARCH-DL-6). A date a row is needed by is "
                 "not a release date and is unchanged.")
readme["A16"] = "Sheet counts: 41 open decisions, 29 decisions taken, 31 owner rows."
readme["A17"] = None
readme["A18"] = ("Source: Recovery Workbench Decision Log v10, 15 November 2026. Owner codes, services, tables, "
                 "endpoints, events, workflows and jobs are taken from the Microservice Ownership Map v1.")
readme["A1"].font = Font(name="Aptos", size=16, bold=True, color="FF4E297F")
readme["A2"].font = Font(name="Aptos", size=10, color="FF404040")
for ref in ("A4", "A5", "A9", "A12", "A13", "A14", "A15", "A16", "A18"):
    readme[ref].font = Font(name="Aptos", size=10, color="FF404040")
    readme[ref].alignment = Alignment(wrap_text=True, vertical="top")
readme["A7"].font = Font(name="Aptos", size=12, bold=True, color="FF4E297F")
readme["A8"].font = Font(name="Aptos", size=10, bold=True)
readme["A11"].font = Font(name="Aptos", size=12, bold=True, color="FF4E297F")

# ---------------------------------------------------------------- Open decisions
od = wb["Open decisions"]
od["A4"] = ("Owner labels that named an individual in v10 carry the placeholder of Template and Rules \u00a7R9 "
            "(CG-B-ARCH-DL-1; ASM-B-ARCH-DL-2); every other cell of the row is unchanged.")
od["A4"].font = Font(name="Aptos", size=9, color="FF404040")
od["A4"].alignment = Alignment(wrap_text=True, vertical="top")
od.column_dimensions["F"].width = 44

owner_cells = {
    "DL01": PLACE,
    "DL02": PLACE,
    "DL03": PLACE + " with the architecture team",
    "DL04": PLACE,
    "DL05": PLACE,
    "DL06": PLACE,
    "DL07": PLACE,
    "DL08": PLACE,
    "DL09": PLACE,
    "DL12": PLACE,
    "DL13": PLACE + " with TechX and Henka",
    "DL14": PLACE + " and the product owner",
    "DL20": "Solution architect with " + PLACE,
    "DL35": PLACE,
    "DL37": PLACE,
}
row_of = {}
for r in range(6, od.max_row + 1):
    key = od.cell(r, 1).value
    if key:
        row_of[str(key).strip()] = r
for key, val in owner_cells.items():
    od.cell(row_of[key], 6).value = val

# release dates named in a row are marked tentative
def mark(row, col, old, new):
    cell = od.cell(row, col)
    text = cell.value
    if isinstance(text, str) and old in text:
        cell.value = text.replace(old, new, 1)
        return True
    print("NOT FOUND", old, "in", cell.coordinate)
    return False

mark(row_of["DL03"], 5, "in March 2027", "in March 2027 (tentative)")
mark(row_of["DL34"], 9, "release on 29 November", "release on 29 November (tentative)")
mark(row_of["DL43"], 3, "for a 30 November release", "for a 30 November release (tentative)")
mark(row_of["DL43"], 9, "The 30 November release moves", "The 30 November release (tentative) moves")

# ---------------------------------------------------------------- Decisions taken
dt = wb["Decisions taken"]
dt["A2"] = str(dt["A2"].value).replace("22 decisions already taken", "29 decisions already taken", 1)

r36 = row_of_dt = None
for r in range(6, dt.max_row + 1):
    if str(dt.cell(r, 1).value).strip() == "D-RCV-36":
        row_of_dt = r
assert row_of_dt, "D-RCV-36 row not found"
r36 = row_of_dt

dt.cell(r36, 2).value = str(dt.cell(r36, 2).value) + " (T1 and T2 amended by D-RCV-60)"
dt.cell(r36, 5).value = str(dt.cell(r36, 5).value) + (
    " Amended by D-RCV-60: T1 and T2 are amended so that a case workflow runs on the Temporal task queue of the "
    "service that owns it (rwb-<short>, namespace rwb-recovery) and scheduled work becomes a Temporal Schedule or an "
    "event-started workflow in the owning service as that service is realigned (DP-10), with JOB-05 kept behind the "
    "TimerScheduler port until Epic 3 (CG-B-ARCH-DL-2; ASM-B-ARCH-DL-3)."
)

new_rows = [
    (
        "D-RCV-60",
        "D-RCV-60 ruled: the Recovery Workbench adopts Architecture v5 as the target and realigns every document, "
        "story and diagram to it (1): 19 services inside ACE, one per business module, each with its own schema "
        "rwb_<name>, login, REST base /api/recovery/<short>/v1, Kafka topic rwb.<short>.events.v1 and Temporal task "
        "queue rwb-<short> in namespace rwb-recovery (2); one epic per service, plus 7 platform and 5 integration "
        "epics, with the business epic EP01 to EP08 carried as a tag on every story (3); ownership is a suggestion by "
        "team type and no story is assigned to an individual (4); an Epic 1 story already built or in build keeps its "
        "base ID and its content word for word, and the microservice change goes into a separate delta story (5); "
        "release dates are unchanged and tentative, and the programme finishes within eight months (6); gaps and "
        "assumptions go to the Gap Register and the Assumptions Register, and every document cites CG-<WP>-<n> and "
        "ASM-<WP>-<n> where a source value is missing (7); ADR-013 to ADR-023 are added, each superseding or "
        "amending the decision named after the dash (8); D-RCV-36 T1 and T2 are amended, because a workflow runs on "
        "the task queue of the service that owns it and scheduled work becomes a Temporal Schedule or an "
        "event-started workflow in the owning service (9). This adds DL44 to DL49 and amends D-RCV-36 T1 and T2.",
        "Recovery tech lead with the solution architect",
        "Every document, story and diagram of the Workbench is realigned to the 19 services RWB-SVC-P1 to "
        "RWB-SVC-S9, to the wave map, to the lane and Day-1 rules, and to the ownership recorded in the Microservice "
        "Ownership Map v1. ADR-013 supersedes the single-service decision and ADR-014 replaces the one-schema "
        "position with a schema and login per service; DT07 (one service, one repository, one front end) and DT08 "
        "(modular monolith) no longer apply. The stories already in build are untouched until a delta story is "
        "picked up.",
    ),
    (
        "DL44",
        "Adopt Architecture v5: 19 services inside ACE, one per business module, each with its own schema and login in "
        "the one ACE database, its own REST base, Kafka topic and Temporal task queue, and the 30 ACE views read only "
        "by rwb-source-data.",
        "Recovery tech lead with the solution architect",
        "The service catalogue, the service epics and the story split follow the 19 services of Architecture v5 "
        "slides 41 to 44. ADR-013 records the move to 19 services and ADR-014 the schema and login per service.",
    ),
    (
        "DL45",
        "One epic per service (19), plus 7 platform epics and 5 integration epics; every story also carries its "
        "business epic EP01 to EP08 as a tag.",
        "Product owner",
        "Story IDs follow RWB-<scope>-<legacy compact>-<work type> and every story names its service epic and its "
        "business epic. The story sets, the epic overviews and the Service Story Catalog are built per service epic.",
    ),
    (
        "DL46",
        "Ownership of a story is a suggestion by team type only: CON and APP to TechX, DB to the ACE team, INF to SCB "
        "IT infrastructure, OPS to the DevOps team, ITG to TechX with harness and NFR stories to QA; no story is "
        "assigned to a person and any team may pick up any story.",
        "Product owner with the IT lead",
        "Every story carries the fixed phrase of its work type and 'any team may pick up this story'. The owning "
        "service, table, endpoint, event, workflow and job come from the Microservice Ownership Map v1, not from a "
        "person.",
    ),
    (
        "DL47",
        "Epic 1 preservation: a story already built or in build keeps its base ID and its content word for word, its "
        "legacy sections sit under 'As built (monolith)', and the microservice change is a separate delta story. "
        "RWB-TE-001, RWB-TE-002, RWB-TE-003, RWB-E1-042, RWB-E1-043 and RWB-E1-044 are preserved; RWB-E1-001 is "
        "must-change; RWB-E1-014 and RWB-TE-007 are retired.",
        "Recovery tech lead",
        "Built code is not changed until a delta story is picked up. The Change Register records each change. "
        "Dependencies on RWB-E1-014 are dropped, and dependencies on RWB-TE-007 point to RWB-PLT-E1071-CON.",
    ),
    (
        "DL48",
        "Dates are unchanged from the source documents and every release date is marked tentative; a release date is "
        "never raised as a gap; the programme finishes within eight months.",
        "Product owner",
        "Every next-version document carries the source date unchanged and appends (tentative) to each release date. "
        "A date the build needs is raised as a gap only where a story cannot be finished without it.",
    ),
    (
        "DL49",
        "Gaps and assumptions are held in two registers, the Gap Register and the Assumptions Register, numbered once "
        "as GAP-nnnn and ASM-nnnn at the register step; until then every document cites the candidate CG-<WP>-<n> and "
        "ASM-<WP>-<n> where a source value is missing.",
        "Business analyst with the solution architect",
        "No document invents a value. Where a source is silent the placeholder of Template and Rules \u00a7R9 is "
        "written and a gap row and an assumption row are raised by the work package that found it.",
    ),
]

widths = {1: 10, 2: 64, 3: 13, 4: 28, 5: 60}
last = r36
for offset, (ident, decision, taken, meaning) in enumerate(new_rows, start=1):
    r = r36 + offset
    values = [ident, decision, DATE, taken, meaning]
    for col, val in enumerate(values, start=1):
        cell = dt.cell(r, col)
        cell.value = val
        src = dt.cell(r36, col)
        cell.font = copy(src.font)
        cell.fill = copy(src.fill)
        cell.border = copy(src.border)
        cell.alignment = copy(src.alignment)
        cell.number_format = src.number_format
    lines = max(math.ceil(len(str(v)) / (widths[c] * 1.05)) for c, v in enumerate(values, start=1))
    dt.row_dimensions[r].height = min(320, max(30, lines * 13.2 + 6))
dt.auto_filter.ref = f"A5:E{last + len(new_rows)}"

# ---------------------------------------------------------------- By owner
bo = wb["By owner"]
bo["A4"] = ("Owner labels that named an individual in v10 carry the placeholder of Template and Rules \u00a7R9 "
            "(CG-B-ARCH-DL-1; ASM-B-ARCH-DL-2); the count, the earliest date and the decision IDs of each row are "
            "unchanged, so the sheet still reads 31 owners and 41 open decisions.")
bo["A4"].font = Font(name="Aptos", size=9, color="FF404040")
bo["A4"].alignment = Alignment(wrap_text=True, vertical="top")
bo.column_dimensions["A"].width = 56

bo_owner = {
    "K. Tee": PLACE,
    "K. Tee with K. Bell": PLACE,
    "K. Book": PLACE,
    "K. Book with the architecture team": PLACE + " with the architecture team",
    "K. Pipat": PLACE,
    "K. Book with K. Pipat": PLACE,
    "K. Tee with TechX and Henka": PLACE + " with TechX and Henka",
    "Solution architect with K. Book": "Solution architect with " + PLACE,
    "K. Tee with K. Book": PLACE,
    "K. Tee with K. Jao": PLACE,
    "K. Tee with K. Book and the product owner": PLACE + " and the product owner",
    "K. Tony with K. Book": PLACE,
}
hits = 0
for r in range(6, bo.max_row + 1):
    cell = bo.cell(r, 1)
    key = str(cell.value).strip() if cell.value is not None else ""
    if key in bo_owner:
        cell.value = bo_owner[key]
        hits += 1
assert hits == len(bo_owner), f"By owner: replaced {hits} of {len(bo_owner)}"

wb.save(OUT)
print("WROTE", OUT, "sheets:", wb.sheetnames, "open rows:", od.max_row, "taken rows:", dt.max_row,
      "owner rows:", bo.max_row)
