"""B-DELIVDOC-45: build Release Plan v5 from the v4 copy (never touches the source)."""
import math
from pathlib import Path
import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

ROOT = Path(r"C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14")
OUT = ROOT / "11 Delivery and operations" / "Recovery Workbench Release Plan v5.xlsx"

HDR_FILL = PatternFill("solid", fgColor="DCD3EB")
TITLE_FONT = Font(bold=True, size=16, name="Aptos")
SUB_FONT = Font(size=10, name="Aptos")
HDR_FONT = Font(bold=True, size=10, name="Aptos")
BODY_FONT = Font(size=10, name="Aptos")
THIN = Side(style="thin", color="BFBFBF")
BOX = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
WRAP = Alignment(wrap_text=True, vertical="top")

TOOL = "T3 Code / OpenCode / DeepSeek v4.1 Flash"


def est_height(values, widths):
    lines = 1
    for v, w in zip(values, widths):
        if v is None:
            continue
        chars = len(str(v))
        lines = max(lines, math.ceil(chars / max(8, (w - 2) * 1.05)))
    return max(15, min(150, 13.0 * lines))


def put(ws, row, values, header=False, widths=None):
    for i, v in enumerate(values, 1):
        c = ws.cell(row=row, column=i, value=v)
        c.font = HDR_FONT if header else BODY_FONT
        c.alignment = WRAP
        c.border = BOX
        if header:
            c.fill = HDR_FILL
    if widths:
        ws.row_dimensions[row].height = est_height(values, widths)
    return row + 1


def table(ws, start_row, header, rows, widths):
    r = put(ws, start_row, header, header=True, widths=widths)
    for row in rows:
        r = put(ws, r, row, widths=widths)
    return r


def set_widths(ws, widths):
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w


wb = openpyxl.load_workbook(OUT)

# ------------------------------------------------------------------ Read me
ws = wb.create_sheet("Read me", 0)
widths = [24, 22, 46, 40]
set_widths(ws, widths)
ws["A1"] = "SCB Collections and Recovery. Henka Group, 22 November 2026."
ws["A2"] = "(C) Siam Commercial Bank and Henka Pte Ltd"
for a in ("A1", "A2"):
    ws[a].font = Font(size=11, name="Aptos")
ws["A4"] = "Recovery Workbench Release Plan v5 (D-RCV-60)."
ws["A4"].font = TITLE_FONT
ws["A5"] = ("Eight monthly releases inside the 8-month horizon, from 30 November 2026 to 30 June 2027. "
            "Every release date is tentative (DL48).")
ws["A5"].font = SUB_FONT
ws["A6"] = "Tool: " + TOOL + "."
ws["A6"].font = SUB_FONT
ws["A7"] = "Version 5; 22 November 2026; Status Draft (no approval recorded; CG-B-DELIVDOC-45-6; ASM-B-DELIVDOC-45-6)."
ws["A7"].font = SUB_FONT

ws["A9"] = "Change log"
ws["A9"].font = Font(bold=True, size=12, name="Aptos")
table(ws, 10,
      ["Version", "Date", "Change", "Tool"],
      [["v4", "15 November 2026",
        "Source version. Five sheets kept word for word: Releases, Modules by release, Gates, Calendar, Release rules "
        "(the source records no change log and no tool line; CG-B-DELIVDOC-45-7).", "Not recorded in the source"],
       ["v5", "22 November 2026", "D-RCV-60 microservice realignment", TOOL]],
      widths)

ws["A13"] = ("Change log row: v5, 22 November 2026, D-RCV-60 microservice realignment, " + TOOL)
ws["A13"].font = BODY_FONT
ws["A13"].alignment = Alignment(wrap_text=True, vertical="top")
ws.merge_cells("A13:D13")
ws.row_dimensions[13].height = 30

ws["A15"] = "What version 5 changes"
ws["A15"].font = Font(bold=True, size=12, name="Aptos")
changes = [
    "The five sheets of version 4 are kept with every section, ID, number and date unchanged. The only additions to them are note rows, gate G7 and release rules 8 to 11.",
    "Each release is placed in one delivery wave on the Waves sheet: Wave 0 platform before E1, Wave 1 E1, Wave 2 E2 and E3, Wave 3 E4 and E5, Wave 4 E6, E7 and E8 (Architecture v5 slide 38; Template and Rules R5.6).",
    "Each of the 19 services is named with its wave, schema, REST base, Kafka topic and task queue from the Ownership Map v1, and with the release that version 4 gives its module, on the Services by release sheet.",
    "Gate G7 Contract published is added to the Gates sheet: a consumer builds against a published contract and its fake, and never waits for the provider's build (Architecture v5 slide 11; Template and Rules R5.4 class C).",
    "Release rules 8 to 11 are added: the tentative date, the wave of each release, one creation per service, and contract first.",
    "Every release date is the version 4 date, unchanged, and it is tentative (DL48). No date was raised as a gap (Template and Rules U7).",
    "The Features and Stories counts of version 4 are kept as they stand; they are monolith-era counts and are not restated per service (CG-B-DELIVDOC-45-4; ASM-B-DELIVDOC-45-4).",
    "Owners are service codes of the Ownership Map v1 and team types only. No person is named (AGENTS.md rule 4).",
]
r = 16
for c in changes:
    ws.cell(row=r, column=1, value="- " + c).font = BODY_FONT
    ws.cell(row=r, column=1).alignment = Alignment(wrap_text=True, vertical="top")
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=4)
    ws.row_dimensions[r].height = est_height([c], [132])
    r += 1

r += 1
ws.cell(row=r, column=1, value="Sheets in this version").font = Font(bold=True, size=12, name="Aptos")
r += 1
table(ws, r,
      ["Sheet", "What it holds", "New in v5", "Source"],
      [["Read me", "Header, version, status, change log and what changed", "All of it", "Template and Rules R8.1"],
       ["Releases", "The eight monthly releases, epics 1 to 8, with dates, content, users and notes", "Note rows only", "Version 4"],
       ["Waves", "The five delivery waves, their releases, dates, services and entry and exit", "All of it", "Architecture v5 slide 38; Template and Rules R5.6"],
       ["Services by release", "The 19 services, their wave, release, schema, REST base, topic and queue", "All of it", "Ownership Map v1 Services sheet; version 4 Modules by release"],
       ["Modules by release", "When each of the 19 modules is delivered", "One note row", "Version 4"],
       ["Gates", "The gates between releases, G1 to G6, plus G7", "Gate G7", "Version 4; Architecture v5 slide 11"],
       ["Calendar", "The dates of every epic activity", "One note row", "Version 4"],
       ["Release rules", "The rules that apply to every release, 1 to 7, plus 8 to 11", "Rules 8 to 11", "Version 4; Architecture v5 slide 38"]],
      widths)

# ------------------------------------------------------------------ Waves
ws = wb.create_sheet("Waves", 1)
widths = [8, 18, 24, 34, 34, 10, 11, 46, 54]
set_widths(ws, widths)
ws["A1"] = "Delivery waves inside the 8-month horizon"
ws["A1"].font = TITLE_FONT
ws["A2"] = ("Wave 0 builds the platform once; each wave then adds the services of its epics. Every date is the version 4 "
            "date, unchanged and tentative (DL48).")
ws["A2"].font = SUB_FONT

wave_rows = [
    ["0", "Platform and NF", "None. The platform work completes before the E1 release",
     "Before the E1 go decision, 27 November 2026 (tentative)",
     "None. Seven platform epics: RWB-PLT-TPL, RWB-PLT-LIB, RWB-PLT-WF, RWB-PLT-DB, RWB-PLT-EVT, RWB-PLT-EDGE, RWB-PLT-OBS",
     "0", "0",
     "Service template and Helm chart, contract libraries, workflow kit, 19 schemas and logins, Kafka topics and ACLs, Temporal 1.30+, edge and observability",
     "Entry: the architecture decisions and the BOT route are confirmed (Architecture v5 slide 39). Exit: one service from the template, one schema, one login and one topic proven in DEV before the E1 build starts (CG-B-DELIVDOC-45-2; ASM-B-DELIVDOC-45-2)"],
    ["1", "EP01", "E1", "30 November 2026 (tentative)",
     "P1, P2, P3, P4, P5, P6, P7, P9, P10", "9", "9",
     "Foundation 1: source data, integration, case, access, document, comms, decision, reporting and the agent runtime in shadow",
     "Entry: the Wave 0 exit and gate G7 on the nine service contracts. Exit: gates G3, G4 and G5 for E1"],
    ["2", "EP02, EP03", "E2, E3", "31 December 2026 (tentative); 31 January 2027 (tentative)",
     "P8, S2, S5, S8", "4", "13",
     "Foundation 2, then settle, deed in lieu and assets",
     "Entry: the E1 release and gate G7 on the four contracts. Exit: gates G3 to G5 for E2 and then for E3"],
    ["3", "EP04, EP05", "E4, E5", "28 February 2027 (tentative); 31 March 2027 (tentative)",
     "S1, S3, S4, S6", "4", "17",
     "Route decision with the route agent, guarantees, litigation and the debt sale lot data",
     "Entry: the E3 release and gate G7 on the four contracts. Exit: gates G3 to G5 for E4 and then for E5"],
    ["4", "EP06, EP07, EP08", "E6, E7, E8",
     "30 April 2027 (tentative); 31 May 2027 (tentative); 30 June 2027 (tentative)",
     "S7, S9", "2", "19",
     "Debt sale and write-off, deviations and partners, administration and hardening",
     "Entry: the E5 release and gate G7 on the two contracts. Exit: gates G3 to G5 for E6, E7 and E8; the last release closes the 8-month horizon"],
    ["All", "EP01 to EP08", "E1 to E8, eight monthly releases", "30 November 2026 to 30 June 2027 (tentative)",
     "19 services, one per BA module", "19", "19",
     "The programme completes within the 8-month horizon of U7",
     "Every release keeps its version 4 date, unchanged and tentative (DL48)"],
]
end = table(ws, 4,
            ["Wave", "Business epics", "Releases", "Release dates (tentative)", "Services created in the wave (Architecture v5)",
             "Services", "Cumulative services", "What the wave delivers", "Entry and exit"],
            wave_rows, widths)

notes = [
    "Notes",
    "Waves follow Architecture v5 slide 38 (Wave 1 = Epic 1, Wave 2 = Epics 2-3, Wave 3 = Epics 4-5, Wave 4 = Epics 6-7) and the W-MAP of Template and Rules R5.6 (EP01 wave 1; EP02 and EP03 wave 2; EP04 and EP05 wave 3; EP06, EP07 and EP08 wave 4). The two sources agree on the wave of every releasable epic.",
    "A wave starts at the first release of its first epic: Wave 2 at E2, Wave 3 at E4, Wave 4 at E6. A wave covers two or three monthly releases, so its later release carries the close of the earlier epic (CG-B-DELIVDOC-45-1; ASM-B-DELIVDOC-45-1).",
    "Version 4 gives S4 rwb-litigation notice approval in E2, while Architecture v5 creates S4 in Wave 3. The W-MAP rule keeps that work in E2; the conflict and the position are CG-B-DELIVDOC-45-8 and ASM-B-DELIVDOC-45-8.",
    "Version 4 gives later work to Wave 1 services in later releases (P3, P4, P5, P6, P7, P9 and P10 all appear again in E2 or later). That is the W-MAP rule: the story keeps its business-epic wave and the service is not recreated.",
    "Owner: each wave is owned for readiness by the service owner code of the Ownership Map v1 for its services and by the team types of Template and Rules R5.3. No person is named (AGENTS.md rule 4; CG-B-DELIVDOC-45-5; ASM-B-DELIVDOC-45-5).",
    "Sources: Architecture v5 Text Extract v1 slides 11, 38, 39 and 41; Template and Rules R3, R4, R5.3, R5.6, R5.7 and U7; Ownership Map v1 Services sheet; Recovery Workbench Release Plan v4 Releases, Modules by release and Calendar sheets.",
]
r = end + 1
for i, n in enumerate(notes):
    c = ws.cell(row=r, column=1, value=n)
    c.font = Font(bold=True, size=11, name="Aptos") if i == 0 else BODY_FONT
    c.alignment = Alignment(wrap_text=True, vertical="top")
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=9)
    ws.row_dimensions[r].height = 15 if i == 0 else est_height([n], [250])
    r += 1
ws.freeze_panes = "A5"

# ------------------------------------------------------------------ Services by release
ws = wb.create_sheet("Services by release", 2)
widths = [8, 14, 22, 6, 26, 20, 14, 30, 26, 16, 52, 34]
set_widths(ws, widths)
ws["A1"] = "The 19 services, their wave and their release"
ws["A1"].font = TITLE_FONT
ws["A2"] = ("Module, service, name, wave, schema, REST base, Kafka topic and task queue are the Ownership Map v1 Services "
            "sheet. The release is the version 4 Modules by release text, unchanged; the date is tentative (DL48).")
ws["A2"].font = SUB_FONT

STD = ("CON and APP: TechX (suggested; any team may pick up this story). "
       "DB: ACE team (suggested; any team may pick up this story). "
       "OPS: DevOps team (suggested; any team may pick up this story)")
svc = [
    ["P1", "rwb-source-data", "Source data", "1", "E1", "30 November 2026 (tentative)", "rwb_source_data", "/api/recovery/source-data/v1", "rwb.source-data.events.v1", "rwb-source-data", STD, "Interaction ledger owner (R3 default ruling)"],
    ["P2", "rwb-integration", "Integration", "1", "E1", "30 November 2026 (tentative)", "rwb_integration", "/api/recovery/integration/v1", "rwb.integration.events.v1", "rwb-integration", STD, ""],
    ["P3", "rwb-case", "Case and workflow", "1", "E1 core, E2 screens", "30 November 2026 (tentative)", "rwb_case", "/api/recovery/case/v1", "rwb.case.events.v1", "rwb-case", STD, "Parameters, reference data and the case list API (R3 default rulings)"],
    ["P4", "rwb-access", "Access and authority", "1", "E1; E2 partners; E8 full administration", "30 November 2026 (tentative)", "rwb_access", "/api/recovery/access/v1", "rwb.access.events.v1", "rwb-access", STD, "Full administration closes in E8"],
    ["P5", "rwb-document", "Document", "1", "E1 store and OCR; E2 generation", "30 November 2026 (tentative)", "rwb_document", "/api/recovery/document/v1", "rwb.document.events.v1", "rwb-document", STD, ""],
    ["P6", "rwb-comms", "Communications", "1", "E1 notices; E2 dispatch; E4 self-service", "30 November 2026 (tentative)", "rwb_comms", "/api/recovery/comms/v1", "rwb.comms.events.v1", "rwb-comms", STD, "Self-service arrives in E4"],
    ["P7", "rwb-decision", "Decision and rules", "1", "E1 log; E2 routing; E3 center", "30 November 2026 (tentative)", "rwb_decision", "/api/recovery/decision/v1", "rwb.decision.events.v1", "rwb-decision", STD, "Rule package registry (R3 default ruling)"],
    ["P8", "rwb-payment", "Payment", "2", "E2 matching; E4", "31 December 2026 (tentative)", "rwb_payment", "/api/recovery/payment/v1", "rwb.payment.events.v1", "rwb-payment", STD, ""],
    ["P9", "rwb-reporting", "Reporting", "1", "E1 baseline; E2 dashboard", "30 November 2026 (tentative)", "rwb_reporting", "/api/recovery/reporting/v1", "rwb.reporting.events.v1", "rwb-reporting", STD, ""],
    ["P10", "rwb-agent", "Agent", "1", "E1 shadow; E2 L1", "30 November 2026 (tentative)", "rwb_agent", "/api/recovery/agent/v1", "rwb.agent.events.v1", "rwb-agent", STD, "Agent runtime runs in shadow from E1"],
    ["S1", "rwb-valuation", "Valuation and route", "3", "E4", "28 February 2027 (tentative)", "rwb_valuation", "/api/recovery/valuation/v1", "rwb.valuation.events.v1", "rwb-valuation", STD, ""],
    ["S2", "rwb-treatment", "Treatment and offer", "2", "E2 foundations; E3", "31 December 2026 (tentative)", "rwb_treatment", "/api/recovery/treatment/v1", "rwb.treatment.events.v1", "rwb-treatment", STD, "Settlement and deed in lieu close in E3"],
    ["S3", "rwb-guarantee", "Guarantee", "3", "E4", "28 February 2027 (tentative)", "rwb_guarantee", "/api/recovery/guarantee/v1", "rwb.guarantee.events.v1", "rwb-guarantee", STD, ""],
    ["S4", "rwb-litigation", "Litigation", "3", "E2 notices; E5", "31 December 2026 (tentative)", "rwb_litigation", "/api/recovery/litigation/v1", "rwb.litigation.events.v1", "rwb-litigation", STD, "Service created in Wave 3; E2 notice approval is the W-MAP conflict (CG-B-DELIVDOC-45-8)"],
    ["S5", "rwb-asset", "Asset", "2", "E3; E4", "31 January 2027 (tentative)", "rwb_asset", "/api/recovery/asset/v1", "rwb.asset.events.v1", "rwb-asset", STD, "Auction rounds and RAMC close in E4"],
    ["S6", "rwb-debtsale", "Debt sale", "3", "E5 data; E6 screens", "31 March 2027 (tentative)", "rwb_debtsale", "/api/recovery/debtsale/v1", "rwb.debtsale.events.v1", "rwb-debtsale", STD, ""],
    ["S7", "rwb-writeoff", "Write-off", "4", "E6", "30 April 2027 (tentative)", "rwb_writeoff", "/api/recovery/writeoff/v1", "rwb.writeoff.events.v1", "rwb-writeoff", STD, ""],
    ["S8", "rwb-deviation", "Deviation", "2", "E2 screening; E7", "31 December 2026 (tentative)", "rwb_deviation", "/api/recovery/deviation/v1", "rwb.deviation.events.v1", "rwb-deviation", STD, "X1 to X7 end to end in E7"],
    ["S9", "rwb-partner", "Partner", "4", "E6 panel; E7 scoring", "30 April 2027 (tentative)", "rwb_partner", "/api/recovery/partner/v1", "rwb.partner.events.v1", "rwb-partner", STD, "Partner scoring, conduct and the field app close in E7"],
]
end = table(ws, 4,
            ["Module", "Service", "Name", "Wave", "Release in version 4 (unchanged)", "First release date (tentative)",
             "Schema", "REST base", "Kafka topic", "Task queue", "Suggested owners of the story types (R5.3)", "Note"],
            svc, widths)

notes = [
    "Notes",
    "Every service is created once, in the first release of its wave: P1, P2, P3, P4, P5, P6, P7, P9 and P10 in Wave 1 (E1); P8, S2, S5 and S8 in Wave 2 (E2); S1, S3, S4 and S6 in Wave 3 (E4); S7 and S9 in Wave 4 (E6) (Architecture v5 slide 38).",
    "A service with work in a later release keeps its schema, its REST base, its topic and its queue; only its stories join the later release, under the W-MAP rule of Template and Rules R5.6.",
    "Owners: the service and its owner code are the Ownership Map v1 Services sheet. The story-type owners are Template and Rules R5.3. No person is named (AGENTS.md rule 4).",
    "Sources: Ownership Map v1 Services sheet; Architecture v5 Text Extract v1 slides 38 and 41; Template and Rules R3, R4, R5.2, R5.3, R5.6 and R5.7; Recovery Workbench Release Plan v4 Modules by release sheet.",
]
r = end + 1
for i, n in enumerate(notes):
    c = ws.cell(row=r, column=1, value=n)
    c.font = Font(bold=True, size=11, name="Aptos") if i == 0 else BODY_FONT
    c.alignment = Alignment(wrap_text=True, vertical="top")
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=12)
    ws.row_dimensions[r].height = 15 if i == 0 else est_height([n], [280])
    r += 1
ws.freeze_panes = "A5"

# ------------------------------------------------------------------ existing sheets: note rows, G7, rules 8-11
ws = wb["Releases"]
r = 13
extra = [
    ("Note", "Release dates: every date in this sheet is tentative (DL48; D-RCV-60). The dates are the version 4 dates, unchanged."),
    ("Waves", "Each release sits in one delivery wave: E1 Wave 1; E2 and E3 Wave 2; E4 and E5 Wave 3; E6, E7 and E8 Wave 4, with the Wave 0 platform work before E1. See the Waves sheet (Architecture v5 slide 38; Template and Rules R5.6; CG-B-DELIVDOC-45-1; ASM-B-DELIVDOC-45-1)."),
    ("Owners", "Owners are service codes of the Ownership Map v1 and team types only; no person is named (AGENTS.md rule 4; CG-B-DELIVDOC-45-5; ASM-B-DELIVDOC-45-5)."),
    ("Counts", "The Features and Stories columns are kept as version 4 states them; they are monolith-era counts and are not restated per service (CG-B-DELIVDOC-45-4; ASM-B-DELIVDOC-45-4)."),
]
for label, text in extra:
    a = ws.cell(row=r, column=1, value=label)
    a.font = HDR_FONT
    a.alignment = WRAP
    b = ws.cell(row=r, column=2, value=text)
    b.font = BODY_FONT
    b.alignment = WRAP
    ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=15)
    ws.row_dimensions[r].height = est_height([text], [180])
    r += 1

ws = wb["Modules by release"]
r = 24
a = ws.cell(row=r, column=1, value="Note")
a.font = HDR_FONT
b = ws.cell(row=r, column=2, value="Each module is one service in Architecture v5 and the Ownership Map v1. The service name, schema, REST base, topic, queue, wave and release date are on the Services by release sheet; the release text here is version 4 and is unchanged.")
b.font = BODY_FONT
b.alignment = WRAP
ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=3)
ws.row_dimensions[r].height = 45

ws = wb["Gates"]
r = 11
row = ["G7", "Contract published", "Before a consumer starts its build",
       "The OpenAPI, AsyncAPI and activity contracts of the service are published with a fake, and a contract test runs in every build. A consumer builds against the fake and never waits for the provider's build (Architecture v5 slide 11; Template and Rules R5.4 class C, new, D-RCV-60)",
       "The code owner of the owning service with the solution architect (suggested; any team may pick up this story). CG-B-DELIVDOC-45-3; ASM-B-DELIVDOC-45-3"]
put(ws, r, row, widths=[7, 18, 26, 70, 40])

ws = wb["Calendar"]
r = 53
a = ws.cell(row=r, column=1, value="Note")
a.font = HDR_FONT
b = ws.cell(row=r, column=2, value="Every date in this sheet is tentative (DL48) and unchanged from version 4. The wave of each epic is on the Waves sheet: E1 Wave 1; E2 and E3 Wave 2; E4 and E5 Wave 3; E6, E7 and E8 Wave 4.")
b.font = BODY_FONT
b.alignment = WRAP
ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=4)
ws.row_dimensions[r].height = 45

ws = wb["Release rules"]
rules = [
    ["8", "Every release date in this plan is tentative (DL48). The dates are the version 4 dates and no date moves (Template and Rules U7)"],
    ["9", "A release belongs to one delivery wave: E1 is Wave 1; E2 and E3 are Wave 2; E4 and E5 are Wave 3; E6, E7 and E8 are Wave 4. The Wave 0 platform work completes before the E1 release (Architecture v5 slide 38; Template and Rules R5.6)"],
    ["10", "A service is created once, in the first release of its wave, and is not built twice. Its later work joins later releases under its own contract (Architecture v5 slide 38 note; Template and Rules R5.2, R5.6)"],
    ["11", "Contract first: a service publishes its REST, event and activity contracts with fakes before a consumer builds, and gate G7 checks it. A consumer is never blocked by a provider's build (Architecture v5 slide 11; Template and Rules R5.4 class C)"],
]
r = 12
for row in rules:
    put(ws, r, row, widths=[7, 110])
    r += 1

# keep sheet order: Read me first, then the version 4 sheets, Waves and Services after Releases
order = ["Read me", "Releases", "Waves", "Services by release", "Modules by release", "Gates", "Calendar", "Release rules"]
wb._sheets = [wb[n] for n in order]
wb.properties.title = "Recovery Workbench Release Plan v5"
wb.properties.subject = "D-RCV-60 microservice realignment"
wb.properties.version = "v5"
wb.save(OUT)
print("WROTE", OUT)
for name in wb.sheetnames:
    print("  sheet:", name)
