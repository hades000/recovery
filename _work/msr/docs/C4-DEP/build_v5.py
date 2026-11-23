"""C4-DEP: build Dependency Map v5 from the v4 copy. Never touches the source workbooks."""
import collections
import json
import math
from pathlib import Path

import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

ROOT = Path(r"C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14")
OUT = ROOT / "11 Delivery and operations" / "Recovery Workbench Dependency Map v5.xlsx"
CAT = ROOT / "04 User stories" / "Recovery Workbench Service Story Catalog v1.xlsx"
OWN = ROOT / "22 Microservice Realignment" / "Recovery Workbench Microservice Ownership Map v1.xlsx"
SRC = ROOT / "11 Delivery and operations" / "Recovery Workbench Dependency Map v4.xlsx"
PLAN = ROOT / "_work" / "msr" / "plan" / "split_plan.json"
SCRATCH = ROOT / "_work" / "msr" / "docs" / "C4-DEP"

TOOL = "T3 Code / OpenCode / DeepSeek v4.1 Flash"
DEC = "D-RCV-60"
CG = "CG-C4-DEP-"
ASM = "ASM-C4-DEP-"

HDR_FILL = PatternFill("solid", fgColor="DCD3EB")
TITLE_FONT = Font(bold=True, size=16, name="Aptos")
SUB_FONT = Font(size=10, name="Aptos")
HDR_FONT = Font(bold=True, size=10, name="Aptos")
BODY_FONT = Font(size=10, name="Aptos")
SEC_FONT = Font(bold=True, size=12, name="Aptos")
THIN = Side(style="thin", color="BFBFBF")
BOX = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
WRAP = Alignment(wrap_text=True, vertical="top")

CLASS = {
    "H": ("Same service, or a platform CON story", "Only H on a non-CON story (same lane)"),
    "C": ("Another service's CON story", "No"),
    "I": ("The real cross-service behaviour. Allowed only on ITG stories", "ITG only"),
    "X": ("External or team-type work (DB, INF or OPS story of the same legacy key, outside systems)", "No; tracked"),
}
CLASS_EFFECT = [
    ("H", "Builds after the same-service CON story, or after the in-lane story it names; the lane sets the order and its depth is at most 4."),
    ("C", "Builds against the published contract and its fake; the provider's build never blocks this one and gate G7 checks that the contract is published first."),
    ("I", "Runs the real call end to end, after both services answer on their contracts; it sits only on an ITG story."),
    ("X", "Never blocks; tracked weekly with the external owner and the build runs on the stated assumption behind a flag."),
]

SVC_CODE = {
    "rwb-source-data": "P1", "rwb-integration": "P2", "rwb-case": "P3", "rwb-access": "P4",
    "rwb-document": "P5", "rwb-comms": "P6", "rwb-decision": "P7", "rwb-payment": "P8",
    "rwb-reporting": "P9", "rwb-agent": "P10", "rwb-valuation": "S1", "rwb-treatment": "S2",
    "rwb-guarantee": "S3", "rwb-litigation": "S4", "rwb-asset": "S5", "rwb-debtsale": "S6",
    "rwb-writeoff": "S7", "rwb-deviation": "S8", "rwb-partner": "S9",
    "platform": "PLT", "integration": "ITG",
}
E2EP = {"E1": "EP01", "E2": "EP02", "E3": "EP03", "E4": "EP04", "E5": "EP05", "E6": "EP06"}

DP_TABLE = [
    ("DP-01", "`recovery.<table>` or \u201crecovery schema\u201d",
     "Owner's schema `rwb_<name>`; never read another service's tables", "none", []),
    ("DP-02", "`recovery_svc` login", "One login per service", "none", []),
    ("DP-03", "DecisionLogWriter, decision log",
     "Local decision-record library and topic `rwb.decision-record.v1`", "H RWB-PLT-E1027-CON",
     ["RWB-PLT-E1027-CON"]),
    ("DP-04", "RuleEvaluator, Drools",
     "Embedded Drools kit; rule packages from rwb-decision",
     "H RWB-PLT-E1072-CON; C RWB-P7-E1073-CON", ["RWB-PLT-E1072-CON", "RWB-P7-E1073-CON"]),
    ("DP-05", "AceSourceQuery, `v_ace_*`, account_ext",
     "Read through rwb-source-data's contract or the service's own ACE views", "none", []),
    ("DP-06", "Parameters, casewf.config",
     "Parameters contract of rwb-case and the client library",
     "H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON", ["RWB-PLT-E1042-CON", "RWB-P3-E1042-CON"]),
    ("DP-07", "Reference data, LOV", "Reference-data contract of rwb-case",
     "H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON", ["RWB-PLT-E1043-CON", "RWB-P3-E1043-CON"]),
    ("DP-08", "RecoveryAccessGuard", "Authorise contract of rwb-access and the guard library",
     "H RWB-PLT-E1037-CON; C RWB-P4-E1037-CON", ["RWB-PLT-E1037-CON", "RWB-P4-E1037-CON"]),
    ("DP-09", "Application event, EV-nn, outbox",
     "Outbox and inbox library; Kafka topic of the owner; CloudEvents", "H RWB-PLT-TE006-CON",
     ["RWB-PLT-TE006-CON"]),
    ("DP-10", "Quartz, JOB-nn",
     "Temporal Schedule or event-started workflow through the workflow kit", "H RWB-PLT-E1071-CON",
     ["RWB-PLT-E1071-CON"]),
    ("DP-11", "In-process call, published interface",
     "REST contract with mock; one hop; 2 s timeout", "none (C from the legacy dependency)", []),
    ("DP-12", "One workflow per case", "CaseWorkflow parent with a child workflow per stage", "none", []),
    ("DP-13", "`/api/recovery/v1`", "`/api/recovery/<short>/v1`", "none", []),
    ("DP-14", "`rwb.p<n>.` or `rwb.casewf.` topic names",
     "`rwb.<short>.events.v1`; naming library", "H RWB-PLT-E1047-CON", ["RWB-PLT-E1047-CON"]),
    ("DP-15", "V0001 baseline, migration",
     "Per-service Flyway sequence in the service's own schema", "H RWB-PLT-E1044-CON",
     ["RWB-PLT-E1044-CON"]),
    ("DP-16", "`recovery.integration.adapter`", "rwb-integration contract", "C RWB-P2-E1007-CON",
     ["RWB-P2-E1007-CON"]),
    ("DP-17", "Data lake, INT-19, INT-20",
     "Removed (no data lake); reporting from events into rwb-reporting",
     "none; gap if the story needs lake data", []),
    ("DP-18", "Interaction ledger", "Ledger owned by rwb-source-data (default ruling)", "none", []),
    ("DP-19", "Screen, ace-web", "gateway-bff composite route", "H RWB-PLT-N001-CON",
     ["RWB-PLT-N001-CON"]),
    ("DP-20", "Agent client", "rwb-agent contract", "C RWB-P10-TE013-CON", ["RWB-P10-TE013-CON"]),
]

WAVE0 = [
    ("Kafka hosting for the business-event topics, with ACLs kept separate from PII logging",
     "Enterprise Architecture, ACE platform team", "No v4 DEP row"),
    ("19 schemas and 19 logins on the ACE PostgreSQL server, with a connection budget per service",
     "ACE team, DBA", "No v4 DEP row"),
    ("The shared Temporal layer: cluster, workflow kit, 1.30+ for Nexus, one namespace per workbench",
     "Platform team, ACE team", "DEP-36 covers the version approval only"),
    ("ACE common contracts: sign-in, notification path, shared case view adapter, restructure calculator, audit and PII logging",
     "ACE team", "Covered by DEP-04"),
    ("The decision ledger model: local record plus a central ledger, strict mode for irreversible steps",
     "Risk, Internal Audit", "No v4 DEP row"),
    ("The BOT approval route under FPG 19/2560 cl. 5.5, lead time up to 30 business days",
     "Compliance, IT Risk", "No v4 DEP row"),
]

TRACK_STEPS = [
    ("6", "Every story-to-story row carries one class of Template and Rules R5.4: H, C, I or X. The class decides what may block a build: only H, and only on a non-CON story in the same lane."),
    ("7", "A C row never blocks. The consumer builds against the provider's published contract and its fake, and the contract test runs in every build (gate G7)."),
    ("8", "An I row sits only on an ITG story and starts after both services answer on their contracts. An X row never blocks; it is tracked with its external owner and the build runs on the stated assumption."),
    ("9", "Each week the program manager reviews the open external rows (class X) and every C row whose provider is in a later wave. A row late by more than five working days goes to the sponsor review with its effect on the wave."),
]


def est_height(values, widths):
    lines = 1
    for v, w in zip(values, widths):
        if v is None:
            continue
        lines = max(lines, math.ceil(len(str(v)) / max(8, (w - 2) * 1.05)))
    return max(15, min(150, 13.0 * lines))


def put(ws, row, values, header=False, widths=None, start=1):
    for i, v in enumerate(values, start):
        c = ws.cell(row=row, column=i, value=v)
        c.font = HDR_FONT if header else BODY_FONT
        c.alignment = WRAP
        c.border = BOX
        if header:
            c.fill = HDR_FILL
    if widths:
        ws.row_dimensions[row].height = est_height(values, widths)
    return row + 1


def table(ws, start_row, header, rows, widths, start=1):
    r = put(ws, start_row, header, header=True, widths=widths, start=start)
    for row in rows:
        r = put(ws, r, row, widths=widths, start=start)
    return r


def set_widths(ws, widths):
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w


def title_block(ws, title, subtitle, span, widths):
    ws["A1"] = title
    ws["A1"].font = TITLE_FONT
    ws["A2"] = subtitle
    ws["A2"].font = SUB_FONT
    ws["A2"].alignment = Alignment(wrap_text=True, vertical="top")
    ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=span)
    ws.row_dimensions[2].height = est_height([subtitle], [sum(widths[:span])])


def notes(ws, start_row, items, span, widths):
    r = start_row
    for i, text in enumerate(items):
        c = ws.cell(row=r, column=1, value=text)
        c.font = SEC_FONT if (i == 0 and text == "Notes") else BODY_FONT
        c.alignment = Alignment(wrap_text=True, vertical="top")
        ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=span)
        ws.row_dimensions[r].height = 15 if (i == 0 and text == "Notes") else est_height([text], [sum(widths[:span])])
        r += 1
    return r


# ------------------------------------------------------------------ read the sources
cat = openpyxl.load_workbook(CAT, read_only=True, data_only=True)
stories = collections.OrderedDict()
for row in cat["Stories"].iter_rows(min_row=2, values_only=True):
    if row[0]:
        stories[row[0]] = row
deps = [row for row in cat["Dependencies"].iter_rows(min_row=2, values_only=True) if row[0]]
legacy_map = {}
for row in cat["Legacy map"].iter_rows(min_row=2, values_only=True):
    if row[0]:
        legacy_map[row[0]] = [x.strip() for x in str(row[2] or "").split(";") if x.strip()]
cat.close()

own = openpyxl.load_workbook(OWN, read_only=True, data_only=True)
services = [r for r in own["Services"].iter_rows(min_row=2, values_only=True) if r[0]]
own.close()

plan = json.loads(PLAN.read_text(encoding="utf-8"))
lg_plan = plan["legacy"]

src = openpyxl.load_workbook(SRC, read_only=True, data_only=True)
legacy_rows = [r for r in src["Story dependencies"].iter_rows(min_row=5, max_row=329, values_only=True) if r[0]]
dep_rows = [r for r in src["Dependencies"].iter_rows(min_row=5, max_row=40, values_only=True) if r[0]]
src.close()

# ------------------------------------------------------------------ derived data
out_deps = collections.defaultdict(list)
for s, t, c in deps:
    out_deps[s].append((t, c))

by_class = collections.Counter(c for s, t, c in deps)
by_code_out = collections.Counter()
by_code_in = collections.Counter()
by_wave_class = collections.Counter()
cross = collections.Counter()
for s, t, c in deps:
    a, b = stories[s], stories[t]
    ca, cb = SVC_CODE[a[4]], SVC_CODE[b[4]]
    wa, wb_ = int(a[6]), int(b[6])
    by_code_out[(ca, c)] += 1
    by_code_in[(cb, c)] += 1
    by_wave_class[(wa, c)] += 1
    rel = "same" if wa == wb_ else ("later" if wb_ > wa else "earlier")
    cross[(c, rel)] += 1

h_to_con = sum(1 for s, t, c in deps if c == "H" and stories[t][2] == "Contract")
h_to_app = sum(1 for s, t, c in deps if c == "H" and stories[t][2] != "Contract")
h_to_plt_con = sum(1 for s, t, c in deps if c == "H" and stories[t][2] == "Contract" and stories[t][4] == "platform")
x_same = sum(1 for s, t, c in deps if c == "X" and stories[t][4] == stories[s][4])
x_plt = sum(1 for s, t, c in deps if c == "X" and stories[t][4] != stories[s][4])
x_app = sum(1 for s, t, c in deps if c == "X" and stories[t][2] == "App development")
dep_stories = {s for s, t, c in deps}
none_dep = [stories[k] for k in stories if k not in dep_stories]
none_by_wt = collections.Counter(r[2] for r in none_dep)
itg_stories = len({s for s, t, c in deps if c == "I"})
con_stories = sum(1 for k, v in stories.items() if v[2] == "Contract")
day1 = sum(1 for k, v in stories.items() if str(v[12]).strip() == "Day 1")

# legacy trace
trace = []
for a, title_a, b in [(r[0], r[1], r[2]) for r in legacy_rows]:
    sa = legacy_map.get(a) or lg_plan.get(a, {}).get("slices", [])
    sb = legacy_map.get(b) or lg_plan.get(b, {}).get("slices", [])
    hits = [(s, t, c) for s in sa for (t, c) in out_deps.get(s, []) if t in sb]
    da = lg_plan.get(a, {}).get("disposition", "")
    db = lg_plan.get(b, {}).get("disposition", "")
    classes = sorted({c for s, t, c in hits})
    if hits:
        status, note, nrows = "Carried", "", len(hits)
    elif b == "RWB-TE-007" and any(t == "RWB-PLT-E1071-CON" for s in sa for (t, c) in out_deps.get(s, [])):
        red = [(s, t, c) for s in sa for (t, c) in out_deps.get(s, []) if t == "RWB-PLT-E1071-CON"]
        status = "Carried by redirect"
        note = ("RWB-TE-007 is retired; Template and Rules R6 points dependencies on it to RWB-PLT-E1071-CON, "
                "and the new stories carry that row.")
        classes, nrows = ["H"], len(red)
    elif da.startswith("Retired") or db.startswith("Retired"):
        status, nrows = "Dropped", 0
        note = f"{a if da.startswith('Retired') else b} is retired ({DEC}; Template and Rules R6); the dependency is dropped."
    else:
        status, nrows = "Not carried", 0
        note = f"No v5 row connects a new story of {a} to a new story of {b} ({CG}2; {ASM}2)."
    trace.append([a, b, title_a, stories[sb[0]][1] if sb and sb[0] in stories else "", len(sa), nrows,
                  ", ".join(classes), status, note])
trace_status = collections.Counter(r[7] for r in trace)

# ------------------------------------------------------------------ workbook
wb = openpyxl.load_workbook(OUT)

# ---------------- 1. Read me
ws = wb.create_sheet("Read me", 0)
widths = [30, 18, 62, 20]
set_widths(ws, widths)
ws["A1"] = "SCB Collections and Recovery. Henka Group, 22 November 2026."
ws["A2"] = "(C) Siam Commercial Bank and Henka Pte Ltd"
for a in ("A1", "A2"):
    ws[a].font = Font(size=11, name="Aptos")
ws["A4"] = "Recovery Workbench Dependency Map v5 (D-RCV-60)."
ws["A4"].font = TITLE_FONT
ws["A5"] = ("36 dependencies on parties outside the recovery squads, and the story dependency graph of the "
            f"realignment: {len(deps):,} rows, each in class H, C, I or X.")
ws["A5"].font = SUB_FONT
ws["A5"].alignment = Alignment(wrap_text=True, vertical="top")
ws.merge_cells("A5:C5")
ws.row_dimensions[5].height = 30
ws["A6"] = "Tool: " + TOOL + "."
ws["A6"].font = SUB_FONT
ws["A7"] = (f"Version 5; 22 November 2026; Status Draft (no approval of the v4 map or of this version is recorded in "
            f"the sources; {ASM}6).")
ws["A7"].font = SUB_FONT
ws["A7"].alignment = Alignment(wrap_text=True, vertical="top")
ws.merge_cells("A7:C7")
ws.row_dimensions[7].height = 28

ws["A9"] = "Change log"
ws["A9"].font = SEC_FONT
table(ws, 10, ["Version", "Date", "Change", "Tool"],
      [["v4", "16 November 2026",
        "Source version: 36 external dependencies and 325 story-level dependencies rebuilt from the Epic 1 v9, Epic 2 v7 "
        "and Technical Enabler Stories v7 masters. The source records no change log and no tool line.",
        "Not recorded in the source"],
       ["v5", "22 November 2026", "D-RCV-60 microservice realignment", TOOL]],
      widths)
ws["A13"] = f"Change log row: v5, 22 November 2026, {DEC} microservice realignment, {TOOL}"
ws["A13"].font = BODY_FONT
ws["A13"].alignment = Alignment(wrap_text=True, vertical="top")
ws.merge_cells("A13:D13")
ws.row_dimensions[13].height = 15

ws["A15"] = "What version 5 changes"
ws["A15"].font = SEC_FONT
changes = [
    "Every sheet of version 4 is kept with every section, ID, number and date unchanged: Dependencies (DEP-01 to DEP-36), "
    "the 325-row Story dependencies sheet, By team and epic, How they are tracked. Every source cell compares equal "
    "between v4 and v5.",
    "Each of the 36 external dependencies now carries its class: X, external or team-type work (Template and Rules R5.4), "
    "its effect on the build (No; tracked) and its business epic in the v5 vocabulary (E1 to EP01, and so on). Columns A "
    "to I keep the version 4 text.",
    f"The story dependency graph is replaced on a new sheet, Story dependencies v5: {len(deps):,} rows over "
    f"{len(dep_stories):,} stories, each row in class H, C, I or X. The version 4 sheet is kept unchanged and renamed "
    "Story dependencies v4, so the 325 legacy rows stay readable.",
    f"Each row names the service code of both ends from the Ownership Map v1, the wave of both ends, and whether the row "
    f"points at an earlier wave, the same wave or a later wave. The {cross[('C', 'later')]} C rows that point at a later "
    "wave are the ones a consumer builds against the published fake.",
    f"A new sheet, Legacy dependency trace, maps all {len(trace)} version 4 story dependencies to the v5 rows that carry "
    f"them: {trace_status['Carried']} carried, {trace_status['Carried by redirect']} carried by the R6 redirect, "
    f"{trace_status['Dropped']} dropped with a retired story and {trace_status['Not carried']} not carried and raised as "
    f"a gap ({CG}2; {ASM}2).",
    "A new sheet, Dependency classes, holds the four classes with what each one blocks, the checks the graph was put "
    "through, the 20 decoupling patterns of the DP table with the rows each one accounts for, and the six Wave 0 "
    "platform dependencies of Architecture v5 slide 39.",
    "A new sheet, By service and class, counts the rows each service consumes and provides, by class and by wave. A new "
    "sheet, Owners, lists the 19 services of the Ownership Map v1, the owner of each work type and the external owner "
    "roles.",
    "No release date is stated on any sheet, so no date is marked tentative here. The Needed by dates of the 36 external "
    "rows are dependency dates, copied from version 4 unchanged (Template and Rules U7; DL48; ASM-C4-DEP-10).",
    "Owners are service codes of the Ownership Map v1 and the external team and party roles of version 4 only. No person "
    "is named (AGENTS.md rule 4).",
]
r = 16
for ch in changes:
    ws.cell(row=r, column=1, value="- " + ch).font = BODY_FONT
    ws.cell(row=r, column=1).alignment = Alignment(wrap_text=True, vertical="top")
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=4)
    ws.row_dimensions[r].height = est_height([ch], [122])
    r += 1

r += 1
ws.cell(row=r, column=1, value="The graph in numbers").font = SEC_FONT
r += 1
table(ws, r, ["Item", "Count", "What it means"],
      [["Rows in Story dependencies v5", f"{len(deps):,}", "One row per dependency between two new stories"],
       ["H rows", f"{by_class['H']:,}", "Same service or a platform CON story; the only class that blocks a build, on a non-CON story in the same lane"],
       ["C rows", f"{by_class['C']:,}", "Another service's CON story; never blocks, built against the contract and its fake"],
       ["I rows", f"{by_class['I']:,}", "Real cross-service behaviour, on the ITG stories only"],
       ["X rows", f"{by_class['X']:,}", "External or team-type work; tracked, never blocking"],
       ["Stories with at least one row", f"{len(dep_stories):,}", f"of {len(stories):,}; the other {len(none_dep):,} carry no row and rest on the service template or on the team-type story of their own key ({CG}5; {ASM}5)"],
       ["CON stories", str(con_stories), "A CON story has no build dependency (Template and Rules R5.7 rule 1)"],
       ["Day 1 stories", str(day1), "Ready on Day 1 in the Service Story Catalog v1"],
       ["External dependencies", str(len(dep_rows)), "DEP-01 to DEP-36 on the Dependencies sheet, all class X"]],
      widths)
ws.freeze_panes = "A4"

# ---------------- 2. Dependencies (kept, three columns added)
ws = wb["Dependencies"]
widths = [9, 18, 60, 8, 12, 34, 12, 46, 9, 10, 14, 14]
set_widths(ws, widths)
for i, h in enumerate(["Class (R5.4)", "Blocks the build?", "Business epic (v5)"], 10):
    c = ws.cell(row=4, column=i, value=h)
    c.font = HDR_FONT
    c.fill = HDR_FILL
    c.alignment = WRAP
    c.border = BOX
for row in range(5, 41):
    epic = str(ws.cell(row=row, column=4).value or "").strip()
    for col, val in ((10, "X"), (11, "No; tracked"), (12, E2EP.get(epic, ""))):
        c = ws.cell(row=row, column=col, value=val)
        c.font = BODY_FONT
        c.alignment = WRAP
        c.border = BOX
ws.auto_filter.ref = "A4:L40"
notes(ws, 42, [
    "Notes",
    "Class X applies to all 36 rows: every dependency is on a team or a party outside the 19 recovery services (Template and Rules R5.4). Columns A to I keep the version 4 text and every ID, number and date is unchanged.",
    "Business epic (v5): E1 to EP01, E2 to EP02, E3 to EP03, E4 to EP04, E5 to EP05, E6 to EP06 (Template and Rules U1 and R5.6; ASM-C4-DEP-8). The For epic column keeps the version 4 text.",
    "The Needed by dates are the version 4 dates, unchanged. They are dependency dates and not release dates, so none is marked tentative (Template and Rules U7; DL48; ASM-C4-DEP-10).",
    f"Architecture v5 slide 39 names six Wave 0 dependencies. DEP-04 covers the ACE common contracts and DEP-36 covers the Temporal and Drools version approval; the other five have no row here (Kafka hosting and ACLs, the 19 schemas and logins, the Temporal namespaces, the decision ledger model, the BOT approval route). They are listed on the Dependency classes sheet ({CG}4; {ASM}4); no new DEP ID is created in this version.",
    "Owner: the external team or party in column F, as version 4 states it. Service owners are the Ownership Map v1 codes on the Owners sheet. No person is named (AGENTS.md rule 4).",
], 12, widths)

# ---------------- 3. Dependency classes
ws = wb.create_sheet("Dependency classes", 2)
widths = [12, 26, 44, 34, 30, 16]
set_widths(ws, widths)
title_block(ws, "Dependency classes H, C, I and X",
            f"Template and Rules R5.4 applied to the {len(deps):,} rows of the realigned graph. The class decides what may "
            f"block a build; the decoupling patterns of R5.5 decide where the row comes from ({DEC}).", 6, widths)

r = 4
for i in range(1, 7):
    c = ws.cell(row=r, column=i, value=["Class", "Meaning (Template and Rules R5.4)", "", "Blocks the build?", "Rows in v5", "Share"][i - 1])
    c.font = HDR_FONT
    c.fill = HDR_FILL
    c.alignment = WRAP
    c.border = BOX
ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=3)
r += 1
for k in "HCIX":
    meaning, blocks = CLASS[k]
    c = ws.cell(row=r, column=1, value=k)
    c.font = HDR_FONT
    c.border = BOX
    c.alignment = WRAP
    ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=3)
    for col, val in ((2, meaning), (4, blocks), (5, by_class[k]), (6, f"{by_class[k] / len(deps):.1%}")):
        c = ws.cell(row=r, column=col, value=val)
        c.font = BODY_FONT
        c.alignment = WRAP
        c.border = BOX
    ws.row_dimensions[r].height = est_height([meaning], [70])
    r += 1
c = ws.cell(row=r, column=1, value="All")
c.font = HDR_FONT
c.border = BOX
ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=3)
for col, val in ((2, "The four classes"), (4, ""), (5, len(deps)), (6, "100.0%")):
    c = ws.cell(row=r, column=col, value=val)
    c.font = BODY_FONT
    c.alignment = WRAP
    c.border = BOX
r += 2

ws.cell(row=r, column=1, value="What the four classes mean for the plan").font = SEC_FONT
r += 1
for k, text in CLASS_EFFECT:
    c = ws.cell(row=r, column=1, value=f"{k}: {text}")
    c.font = BODY_FONT
    c.alignment = Alignment(wrap_text=True, vertical="top")
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=6)
    ws.row_dimensions[r].height = est_height([text], [150])
    r += 1
r += 1

ws.cell(row=r, column=1, value="What the graph was checked against").font = SEC_FONT
r += 1
for i in range(1, 7):
    c = ws.cell(row=r, column=i, value=["Class", "Rule", "", "Result", "Detail", ""][i - 1])
    c.font = HDR_FONT
    c.fill = HDR_FILL
    c.alignment = WRAP
    c.border = BOX
ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=3)
ws.merge_cells(start_row=r, start_column=5, end_row=r, end_column=6)
r += 1
checks = [
    ("H", "H points only to the same service or to a platform CON story", "0 breaches",
     f"{h_to_con:,} rows to a CON story ({h_to_plt_con:,} of them a platform CON); {h_to_app} to a same-service APP story"),
    ("C", "C points only to another service's CON story", "0 breaches",
     f"{by_class['C']:,} rows; {cross[('C', 'later')]} point at a service built in a later wave, built against its fake"),
    ("I", "I sits only on an ITG story", "0 breaches", f"{by_class['I']:,} rows on {itg_stories} ITG stories"),
    ("X", "X points to team-type work (DB, INF, OPS) of the same legacy key, or to an outside system",
     f"{x_app} rows to a platform APP enabler",
     f"{x_same} rows inside the same service, {x_plt} to platform technical-enabler work ({CG}3; {ASM}3)"),
    ("-", "No duplicate story-and-target row", "0", f"{len(deps):,} distinct rows"),
    ("-", "Every target is a story of the Service Story Catalog v1", "0 missing",
     f"{len(deps):,} rows over {len(dep_stories):,} stories"),
    ("-", "The class of every row is one of H, C, I, X", "0 other values", "Four classes only (Template and Rules R5.4)"),
]
for k, rule, res, detail in checks:
    ws.cell(row=r, column=1, value=k).font = BODY_FONT
    ws.cell(row=r, column=1).border = BOX
    ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=3)
    for col, val in ((2, rule), (4, res), (5, detail)):
        c = ws.cell(row=r, column=col, value=val)
        c.font = BODY_FONT
        c.alignment = WRAP
        c.border = BOX
    ws.merge_cells(start_row=r, start_column=5, end_row=r, end_column=6)
    ws.row_dimensions[r].height = est_height([rule, detail], [70, 46])
    r += 1
r += 1

ws.cell(row=r, column=1, value="Decoupling patterns and the rows they account for (Template and Rules R5.5)").font = SEC_FONT
r += 1
r = table(ws, r, ["DP", "Legacy marker", "Microservice pattern", "Dependency added (R5.5)", "Rows in v5"],
          [[dp, marker, pattern, dep, sum(1 for s, t, c in deps if t in targets) if targets else 0]
           for dp, marker, pattern, dep, targets in DP_TABLE], widths)
r += 1

ws.cell(row=r, column=1, value="The service template baseline").font = SEC_FONT
r += 1
for i in range(1, 7):
    c = ws.cell(row=r, column=i, value=["Item", "Rule", "", "Effect", "Count", ""][i - 1])
    c.font = HDR_FONT
    c.fill = HDR_FILL
    c.alignment = WRAP
    c.border = BOX
ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=3)
r += 1
baseline = [
    ("Baseline",
     "Every non-CON story takes the service template, and the template already carries the H contracts of DP-03, DP-06, DP-07, DP-08, DP-14, DP-15 and DP-19",
     f"Counted once here, not repeated on all {len(stories) - con_stories:,} non-CON stories ({CG}1; {ASM}1)", "7 contracts"),
    ("CON stories", "A CON story has no build dependency (Template and Rules R5.7 rule 1)",
     "0 CON rows in the graph", f"{con_stories} stories"),
    ("Day 1", "A story is Day 1 when its H rows point only at CON stories (R5.7 rule 8)",
     "Ready on Day 1 in the Service Story Catalog v1", f"{day1:,} stories"),
]
for item, rule, effect, count in baseline:
    ws.cell(row=r, column=1, value=item).font = BODY_FONT
    ws.cell(row=r, column=1).border = BOX
    ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=3)
    for col, val in ((2, rule), (4, effect), (5, count)):
        c = ws.cell(row=r, column=col, value=val)
        c.font = BODY_FONT
        c.alignment = WRAP
        c.border = BOX
    ws.row_dimensions[r].height = est_height([rule, effect], [70, 34])
    r += 1
r += 1

ws.cell(row=r, column=1, value="Wave 0 platform dependencies named on Architecture v5 slide 39").font = SEC_FONT
r += 1
for i in range(1, 7):
    c = ws.cell(row=r, column=i, value=["Class", "What is needed", "", "Owner role", "Covered by a v4 DEP row?", ""][i - 1])
    c.font = HDR_FONT
    c.fill = HDR_FILL
    c.alignment = WRAP
    c.border = BOX
ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=3)
ws.merge_cells(start_row=r, start_column=5, end_row=r, end_column=6)
r += 1
for text, owner, covered in WAVE0:
    ws.cell(row=r, column=1, value="X").font = BODY_FONT
    ws.cell(row=r, column=1).border = BOX
    ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=3)
    for col, val in ((2, text), (4, owner), (5, covered)):
        c = ws.cell(row=r, column=col, value=val)
        c.font = BODY_FONT
        c.alignment = WRAP
        c.border = BOX
    ws.merge_cells(start_row=r, start_column=5, end_row=r, end_column=6)
    ws.row_dimensions[r].height = est_height([text, owner, covered], [70, 34, 46])
    r += 1
r += 1

notes(ws, r, [
    "Notes",
    "Class H blocks a build only when the target is not a CON story and the pair sit in one lane (Template and Rules R5.4 and R5.7). A lane is a connected group of non-CON stories linked by H, and its depth is at most 4 (R5.7 rule 5).",
    "Class C never blocks: the consumer builds against the provider's published contract and its fake, and gate G7 checks that the contract is published before the consumer starts.",
    "Class I sits only on the ITG stories of the integration epics RWB-ITG-W1 to RWB-ITG-W4 and RWB-ITG-NFR.",
    "Class X is tracked weekly with its owner outside the services; the build runs on the stated assumption behind a flag (How they are tracked, step 5).",
    f"Rows by wave order: {cross[('H', 'earlier')]:,} H, {cross[('C', 'earlier')]} C, {cross[('I', 'earlier')]} I and {cross[('X', 'earlier')]} X rows point at an earlier wave; {cross[('H', 'same')]:,} H, {cross[('C', 'same')]} C, {cross[('I', 'same')]} I and {cross[('X', 'same')]} X rows sit inside one wave; {cross[('C', 'later')]} C rows point at a later wave and are the ones a consumer builds against a fake.",
    f"The six Wave 0 rows are the dependencies of Architecture v5 slide 39. Five of them have no row in the version 4 external table, which holds DEP-04 and, in part, DEP-36 ({CG}4; {ASM}4).",
    "Sources: Template and Rules R5.4, R5.5, R5.7; Service Story Catalog v1 Dependencies sheet; Ownership Map v1 Services sheet; Architecture v5 Text Extract v1 slides 38, 39, 41 and 44.",
], 6, widths)
ws.freeze_panes = "A4"

# ---------------- 4. Story dependencies v5
ws = wb.create_sheet("Story dependencies v5", 3)
widths = [22, 40, 15, 14, 16, 8, 6, 22, 40, 14, 16, 8, 6, 6, 14, 10, 22]
set_widths(ws, widths)
ws["A1"] = "Story dependencies v5"
ws["A1"].font = TITLE_FONT
ws["A2"] = (f"{len(deps):,} story-level dependencies of the realignment, rebuilt from the Dependencies sheet of Recovery "
            f"Workbench Service Story Catalog v1 on 22 November 2026. Each row is one dependency; the story on the right is "
            f"finished or contracted first, and the class says whether it blocks. H {by_class['H']:,}, C {by_class['C']:,}, "
            f"I {by_class['I']:,}, X {by_class['X']:,}.")
ws["A2"].font = SUB_FONT
ws["A2"].alignment = Alignment(wrap_text=True, vertical="top")
ws.merge_cells("A2:Q2")
ws.row_dimensions[2].height = 30
hdr = ["Story", "Story title", "Story epic", "Story work type", "Story service", "Code", "Wave",
       "Depends on", "Depends-on title", "Depends-on work type", "Depends-on service", "Code", "Wave", "Class",
       "Blocks the build?", "Wave order", "Owner (suggested)"]
r = table(ws, 4, hdr, [], widths)
for s, t, c in deps:
    a, b = stories[s], stories[t]
    wa, wb_ = int(a[6]), int(b[6])
    order = "Same wave" if wa == wb_ else ("Later wave" if wb_ > wa else "Earlier wave")
    r = put(ws, r, [s, a[1], a[5], a[2], a[4], SVC_CODE[a[4]], wa, t, b[1], b[2], b[4], SVC_CODE[b[4]], wb_, c,
                    CLASS[c][1], order, str(a[3]).split(" (suggested")[0]], widths=widths)
ws.auto_filter.ref = f"A4:Q{r - 1}"
ws.freeze_panes = "B5"
notes(ws, r + 1, [
    "Notes",
    "Classes are Template and Rules R5.4: H same service or a platform CON story; C another service's CON story, built against the contract and its fake; I the real cross-service behaviour, ITG stories only; X external or team-type work. Only H blocks a build, and only on a non-CON story in the same lane.",
    "Code and wave are the Ownership Map v1 Services sheet for the 19 services (P1 to P10, S1 to S9); PLT and ITG stand for the platform and integration epics of Template and Rules R5.1 and R5.2. The platform work is Wave 0; an ITG story carries the wave of its integration epic (ASM-C4-DEP-9).",
    f"The service template already carries the H contracts of DP-03, DP-06, DP-07, DP-08, DP-14, DP-15 and DP-19 on every non-CON story; they are counted once on the Dependency classes sheet and not repeated here ({CG}1; {ASM}1).",
    "Owner (suggested) is the fixed phrase of Template and Rules R5.3 with its qualifying sentence removed, so the column stays short; any team may pick up any story (U3). No person is named.",
    "Source: Recovery Workbench Service Story Catalog v1, sheets Stories and Dependencies (read-only). The version 4 sheet is kept next to this one as Story dependencies v4.",
], 17, widths)

# ---------------- 5. Story dependencies v4 (kept, renamed)
ws = wb["Story dependencies"]
ws.title = "Story dependencies v4"
notes(ws, 331, [
    "Notes",
    f"Kept unchanged from version 4 with every story ID, title and row. It is the trace base of the Legacy dependency trace sheet and of the {len(deps):,} rows on Story dependencies v5 ({ASM}7).",
    "The master versions this sheet cites (Epic 1 v9, Epic 2 v7, Technical Enabler Stories v7) are the masters of 16 November 2026; the realignment does not re-derive them, so they stay as written.",
    "The realigned graph, with the H, C, I and X classes, is on Story dependencies v5.",
], 3, [14, 58, 18])

# ---------------- 6. Legacy dependency trace
ws = wb.create_sheet("Legacy dependency trace", 5)
widths = [20, 20, 44, 44, 9, 9, 10, 18, 60]
set_widths(ws, widths)
title_block(ws, "Legacy dependency trace",
            f"All {len(trace)} story-level dependencies of version 4, each mapped to the v5 rows that carry it: "
            f"{trace_status['Carried']} carried, {trace_status['Carried by redirect']} carried by the R6 redirect to "
            f"RWB-PLT-E1071-CON, {trace_status['Dropped']} dropped with a retired story and {trace_status['Not carried']} "
            f"not carried ({CG}2).", 9, widths)
end = table(ws, 4, ["Legacy story", "Legacy depends on", "Title (version 4)", "Title of the dependency (first new story)",
                    "New stories", "New rows", "Classes", "Status", "Note"], trace, widths)
notes(ws, end + 1, [
    "Notes",
    "A row is Carried when at least one new story of the legacy story depends, in any class, on a new story of the legacy dependency; the count in New rows is that number.",
    "Dropped means one of the two legacy stories is retired under Template and Rules R6: RWB-E1-014 (no data lake in Architecture v5) and RWB-TE-007 (Quartz replaced by Temporal Schedules). Where a new story carries RWB-PLT-E1071-CON, the R6 redirect is counted as Carried by redirect.",
    f"Not carried rows are recorded as a gap rather than papered over: see {CG}2 and {ASM}2 and the RWB-E1-056, RWB-TE-009 and RWB-TE-010 rows above.",
    "Sources: Recovery Workbench Dependency Map v4, Story dependencies sheet (read-only); Service Story Catalog v1, Legacy map and Dependencies sheets; split_plan.json, legacy dispositions only.",
], 9, widths)
ws.freeze_panes = "A5"

# ---------------- 7. By service and class
ws = wb.create_sheet("By service and class", 6)
widths = [8, 22, 6, 8, 8, 8, 8, 10, 8, 8, 8, 8, 10]
set_widths(ws, widths)
title_block(ws, "Dependencies by service and class",
            f"Rows each service consumes (out) and provides (in), by class, over the {len(deps):,} rows of Story "
            f"dependencies v5. Codes, names and waves are the Ownership Map v1 Services sheet; PLT and ITG are the "
            f"platform and integration epics.", 13, widths)
def svc_key(s):
    return (int(s[3]), s[0][0], int(s[0][1:]))


rows = []
for code, name, wave in [(s[0], s[1], int(s[3])) for s in sorted(services, key=svc_key)] + \
                        [("PLT", "platform epics", 0), ("ITG", "integration epics", "1 to 4")]:
    out = [by_code_out[(code, k)] for k in "HCIX"]
    inn = [by_code_in[(code, k)] for k in "HCIX"]
    rows.append([code, name, wave] + out + [sum(out)] + inn + [sum(inn)])
rows.append(["All", "Total", ""] + [by_class[k] for k in "HCIX"] + [len(deps)] + [by_class[k] for k in "HCIX"] + [len(deps)])
end = table(ws, 4, ["Code", "Service", "Wave", "Out H", "Out C", "Out I", "Out X", "Out total",
                    "In H", "In C", "In I", "In X", "In total"], rows, widths)
end += 1
ws.cell(row=end, column=1, value="Rows by wave and class").font = SEC_FONT
end += 1
wr = []
for w in sorted({int(stories[s][6]) for s, t, c in deps}):
    wr.append([w, f"Wave {w}"] + [by_wave_class[(w, k)] for k in "HCIX"] + [sum(by_wave_class[(w, k)] for k in "HCIX")])
wr.append(["All", "All waves"] + [by_class[k] for k in "HCIX"] + [len(deps)])
end = table(ws, end, ["Wave", "Label", "H", "C", "I", "X", "Total"], wr, widths)
end += 1
ws.cell(row=end, column=1, value="External dependencies by business epic").font = SEC_FONT
end += 1
ee = collections.Counter(E2EP.get(str(r[3]).strip(), "") for r in dep_rows)
er = [[e, E2EP.get(e, e), ee.get(e, 0)] for e in sorted(ee)]
er.append(["All", "EP01 to EP06", sum(ee.values())])
end = table(ws, end, ["Epic", "Business epic (v5)", "DEP rows"], er, widths)
notes(ws, end + 1, [
    "Notes",
    "Out counts the rows where the service owns the story on the left; In counts the rows where the service owns the story on the right. Both totals equal the row count of Story dependencies v5.",
    f"P3 rwb-case is the largest provider: {by_code_in[('P3', 'C')]} C rows point at its parameters and reference-data contracts, which is the R3 default ruling for E1-042 and E1-043.",
    f"PLT provides {by_code_in[('PLT', 'H')]:,} H rows: the platform CON stories of the service template, the workflow kit, the event kit, the naming library and gateway-bff.",
    "Wave is the service wave of Architecture v5 slide 38 and the Ownership Map v1: 1 for P1, P2, P3, P4, P5, P6, P7, P9 and P10; 2 for P8, S2, S5 and S8; 3 for S1, S3, S4 and S6; 4 for S7 and S9; 0 for the platform epics. The integration epics are not a service and follow the wave of the stories they carry (ASM-C4-DEP-9).",
], 13, widths)
ws.freeze_panes = "C5"

# ---------------- 8. By team and epic (kept)
ws = wb["By team and epic"]
notes(ws, 15, [
    "Notes",
    "Counts are the 36 external dependencies of the Dependencies sheet, unchanged from version 4: 18 before E1, 9 before E2, 1 before E3, 3 before E4, 3 before E5 and 2 before E6. All 36 are class X (Template and Rules R5.4).",
    "The story-to-story graph is counted by service and class on the By service and class sheet, not here.",
], 10, [24, 7, 7, 7, 7, 7, 7, 7, 7, 8])

# ---------------- 9. How they are tracked (kept, steps 6 to 9 added)
ws = wb["How they are tracked"]
r = 10
for num, text in TRACK_STEPS:
    put(ws, r, [num, text], widths=[7, 100])
    r += 1
notes(ws, r + 1, [
    "Notes",
    "Steps 1 to 5 are the version 4 text, unchanged, and apply to the 36 external rows. Steps 6 to 9 add the four classes and the weekly review of the C and X rows.",
], 2, [7, 100])

# ---------------- 10. Owners
ws = wb.create_sheet("Owners", 9)
widths = [8, 20, 18, 6, 18, 30, 28, 16]
set_widths(ws, widths)
title_block(ws, "Owners of the dependencies",
            "The 19 services of the Ownership Map v1 with their wave, schema, REST base, topic and queue, the owner of each "
            "work type, and the external owner roles of the Dependencies sheet. No person is named.", 8, widths)
end = table(ws, 4, ["Code", "Service", "Name", "Wave", "Schema", "REST base", "Topic", "Queue"],
            [[s[0], s[1], s[2], s[3], s[4], s[5], s[6], s[7]] for s in sorted(services, key=lambda x: (int(x[3]), x[0]))],
            widths)
end += 1
ws.cell(row=end, column=1, value="Owner by work type (Template and Rules R5.3)").font = SEC_FONT
end += 1
for i, h in enumerate(["Work type", "Name", "", "", "Suggested owner"]):
    c = ws.cell(row=end, column=i + 1, value=h)
    c.font = HDR_FONT
    c.fill = HDR_FILL
    c.alignment = WRAP
    c.border = BOX
ws.merge_cells(start_row=end, start_column=5, end_row=end, end_column=8)
end += 1
for wt, name, owner in [
        ("CON", "Contract", "TechX (suggested; any team may pick up this story)"),
        ("APP", "App development", "TechX (suggested; any team may pick up this story)"),
        ("DB", "ACE DB", "ACE team (suggested; any team may pick up this story)"),
        ("INF", "Infrastructure", "SCB IT infrastructure (suggested; any team may pick up this story)"),
        ("OPS", "DevOps", "DevOps team (suggested; any team may pick up this story)"),
        ("ITG", "Integration", "TechX (suggested; any team may pick up this story). Harness and NFR stories: QA team (suggested; any team may pick up this story)")]:
    for col, val in ((1, wt), (2, name)):
        c = ws.cell(row=end, column=col, value=val)
        c.font = BODY_FONT
        c.alignment = WRAP
        c.border = BOX
    c = ws.cell(row=end, column=5, value=owner)
    c.font = BODY_FONT
    c.alignment = WRAP
    c.border = BOX
    ws.merge_cells(start_row=end, start_column=5, end_row=end, end_column=8)
    ws.row_dimensions[end].height = est_height([owner], [112])
    end += 1
end += 1
ws.cell(row=end, column=1, value="External owner roles (Dependencies sheet)").font = SEC_FONT
end += 1
ext = collections.Counter(str(r[1]) for r in dep_rows)
epics = collections.defaultdict(set)
dec = collections.defaultdict(set)
for row in dep_rows:
    epics[str(row[1])].add(str(row[3]).strip())
    for d in str(row[6] or "").split(","):
        d = d.strip()
        if d and d != "None":
            dec[str(row[1])].add(d)
for i, h in enumerate(["Owner role", "", "DEP rows", "Business epics and decisions"]):
    c = ws.cell(row=end, column=i + 1, value=h)
    c.font = HDR_FONT
    c.fill = HDR_FILL
    c.alignment = WRAP
    c.border = BOX
ws.merge_cells(start_row=end, start_column=1, end_row=end, end_column=2)
ws.merge_cells(start_row=end, start_column=4, end_row=end, end_column=8)
end += 1
for k, v in sorted(ext.items()):
    c = ws.cell(row=end, column=1, value=k)
    c.font = BODY_FONT
    c.alignment = WRAP
    c.border = BOX
    ws.merge_cells(start_row=end, start_column=1, end_row=end, end_column=2)
    c = ws.cell(row=end, column=3, value=v)
    c.font = BODY_FONT
    c.alignment = WRAP
    c.border = BOX
    text = ", ".join(E2EP.get(e, e) for e in sorted(epics[k])) + " | " + (", ".join(sorted(dec[k])) or "no decision")
    c = ws.cell(row=end, column=4, value=text)
    c.font = BODY_FONT
    c.alignment = WRAP
    c.border = BOX
    ws.merge_cells(start_row=end, start_column=4, end_row=end, end_column=8)
    ws.row_dimensions[end].height = est_height([text], [100])
    end += 1
notes(ws, end + 1, [
    "Notes",
    "Class X rows are owned outside the 19 services: the ACE team, the collection squad, the architecture team, data engineering, SCB IT security, the AI teams, the business and the partners (Template and Rules R5.4).",
    "A service owner is the code and the name of the Ownership Map v1 Services sheet. Every story carries a suggested owner by work type only, and any team may pick up any story (Template and Rules U3, R5.3).",
], 8, widths)

# ---------------- order, properties, save
order = ["Read me", "Dependencies", "Dependency classes", "Story dependencies v5", "Story dependencies v4",
         "Legacy dependency trace", "By service and class", "By team and epic", "How they are tracked", "Owners"]
wb._sheets = [wb[n] for n in order]
wb.properties.title = "Recovery Workbench Dependency Map v5"
wb.properties.subject = f"{DEC} microservice realignment"
wb.properties.creator = "SCB Collections and Recovery"
wb.properties.lastModifiedBy = TOOL
wb.properties.version = "v5"
wb.active = 0
wb.save(OUT)

stats = {
    "rows": len(deps), "by_class": dict(by_class), "stories": len(stories), "dep_stories": len(dep_stories),
    "none_dep": len(none_dep), "none_by_wt": dict(none_by_wt), "con_stories": con_stories, "day1": day1,
    "h_to_con": h_to_con, "h_to_app": h_to_app, "h_to_plt_con": h_to_plt_con,
    "x_same": x_same, "x_plt": x_plt, "x_app": x_app, "itg_stories": itg_stories,
    "cross": {f"{k[0]}-{k[1]}": v for k, v in cross.items()},
    "trace_status": dict(trace_status), "trace": len(trace), "legacy_rows": len(legacy_rows), "dep_rows": len(dep_rows),
    "out": {f"{k[0]}-{k[1]}": v for k, v in by_code_out.items()}, "in": {f"{k[0]}-{k[1]}": v for k, v in by_code_in.items()},
}
(SCRATCH / "stats-v5.json").write_text(json.dumps(stats, indent=1), encoding="utf-8")
print("WROTE", OUT)
print(json.dumps({k: stats[k] for k in ("rows", "by_class", "dep_stories", "none_dep", "trace_status", "trace")}, indent=1))
for n in wb.sheetnames:
    print("  sheet:", n)
