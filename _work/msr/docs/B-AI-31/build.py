"""Build 08 AI and agents/Recovery Workbench Agent Catalog and Specifications v3.xlsx (D-RCV-60).

The v3 file is created first with compat/office_write.py copy, then only the copy is changed:
Read me (new, first), Agents v3 (new), Service summary (new) and Realignment changes (new) are
added. The two source sheets, Agents and Decision steps, are never touched: they are the v2 text
exactly as issued, so every v2 ID, number, autonomy level and epic is kept cell for cell.

Every owner comes from the Microservice Ownership Map v1 (_work/msr/plan/ownership.json).
No value is invented: where no source names the owning service, the basis cell cites the
CG/ASM row that carries the reading.
"""
import math
from datetime import datetime
from pathlib import Path

import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

OUT = Path(r"08 AI and agents\Recovery Workbench Agent Catalog and Specifications v3.xlsx")

TOOL = "T3 Code / OpenCode / DeepSeek v4.1 Flash"
H1 = "SCB Collections and Recovery. Henka Group, 22 November 2026."
H2 = "(C) Siam Commercial Bank and Henka Pte Ltd"
DATE = datetime(2026, 11, 22)
CHANGE = "v3, 22 November 2026, D-RCV-60 microservice realignment, " + TOOL

# ------------------------------------------------------------------ styles
PURPLE = "FF4E297F"
TITLE_FONT = Font(name="Aptos", size=14, bold=True, color=PURPLE)
SUB_FONT = Font(name="Aptos", size=10, bold=True, color=PURPLE)
NOTE_FONT = Font(name="Aptos", size=9, color="FF404040")
HDR_FONT = Font(name="Aptos", size=9, bold=True, color="FFFFFFFF")
HDR_FILL = PatternFill("solid", fgColor=PURPLE)
BODY_FONT = Font(name="Aptos", size=9, color="FF262626")
ALT_FILL = PatternFill("solid", fgColor="FFF3EFF9")
THIN = Side(style="thin", color="FFD9D2E6")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
WRAP = Alignment(wrap_text=True, vertical="top")

# ------------------------------------------------------------------ services (Ownership Map sheet Services)
SERVICES = {
    "P1": ("rwb-source-data", "Source data", 1),
    "P2": ("rwb-integration", "Integration", 1),
    "P3": ("rwb-case", "Case and workflow", 1),
    "P4": ("rwb-access", "Access and authority", 1),
    "P5": ("rwb-document", "Document", 1),
    "P6": ("rwb-comms", "Communications", 1),
    "P7": ("rwb-decision", "Decision and rules", 1),
    "P8": ("rwb-payment", "Payment", 2),
    "P9": ("rwb-reporting", "Reporting", 1),
    "P10": ("rwb-agent", "Agent", 1),
    "S1": ("rwb-valuation", "Valuation and route", 3),
    "S2": ("rwb-treatment", "Treatment and offer", 2),
    "S3": ("rwb-guarantee", "Guarantee", 3),
    "S4": ("rwb-litigation", "Litigation", 3),
    "S5": ("rwb-asset", "Asset", 2),
    "S6": ("rwb-debtsale", "Debt sale", 3),
    "S7": ("rwb-writeoff", "Write-off", 4),
    "S8": ("rwb-deviation", "Deviation", 2),
    "S9": ("rwb-partner", "Partner", 4),
}

RUNTIME = ("P10 rwb-agent: AgentRunWorkflow on task queue rwb-agent, 60 s then the rule result; "
           "schema rwb_agent; topic rwb.agent.events.v1 (Arch v5 slide 16; Ownership Map sheet "
           "Workflows and activities)")

# ------------------------------------------------------------------ owning service per agent
OWNER = {
    "Intake agent": ("P5",
        "Arch v5 slide 16 (P5 IN: DocumentIntakeWorkflow; TMP Agent: child: classify / extract run; "
        "EVT AgentRunCompleted (classification)); Decision steps P5; Ownership Map v1 sheet Services (P5, wave 1)"),
    "Screening agent": ("S8",
        "Arch v5 slide 15 (S8 OUT: TMP Agent: child: screening agent run); FSD S8 FEAT-DVH-07 "
        "(deviation screening agent at L1); Decision steps X1-X7"),
    "Settlement and restructure agent": ("S2",
        "Decision steps D5.2, D5.3 and D6.4 (Run by Settlement and restructure agent; first in E3); "
        "FSD S2 (treatment.proposed_by = Agent, rule or person); Arch v5 slide 18 (S2 rwb-treatment, TreatmentWorkflow). "
        "No service contract names a settlement agent child (CG-B-AI-31-1; ASM-B-AI-31-1)"),
    "Valuation agent": ("S1",
        "Decision step D6.1 (Run by Valuation agent; first in E3); Arch v5 slide 18 (S1 owns the valuations "
        "and the D6 route decision); FSD S1 (D6 route decision). No service contract names a valuation agent "
        "child (CG-B-AI-31-2; ASM-B-AI-31-3)"),
    "Pricing agent": ("S5",
        "Decision steps D8.2 and D8.3; FSD S5 R-DIS-19 and R-DIS-28 (Pricing agent); Arch v5 slide 19 "
        "(S5 rwb-asset, AssetDisposalWorkflow)"),
    "Route agent": ("S1",
        "Arch v5 slide 18 (S1 OUT: TMP Agent: child: route agent; rwb_valuation holds the route agent output); "
        "FSD S1 FEAT-VAL-07; Decision step D6.3"),
    "Guarantee claim agent": ("S3",
        "Decision step D6.5; FSD S3 R-GUA-04 (claim preparation agent); Arch v5 slide 18 "
        "(S3 rwb-guarantee, GuaranteeClaimWorkflow)"),
    "Reconciliation agent": ("P8",
        "Decision step P8; FSD P8 FEAT-PAY-02 (exception list for the reconciliation agent); Arch v5 slide 17 "
        "(P8 rwb-payment, Act: matchPayments, Act: confirmBookings)"),
    "Legal document agent": ("S4",
        "Decision steps D7.2 and D7.4; FSD S4 R-LIT-21 (return the pack to the legal document agent); "
        "Arch v5 slide 19 (S4 rwb-litigation, LitigationWorkflow)"),
    "Debt sale agent": ("S6",
        "Decision step D8.4; FSD S6 R-DS-04 (lot agent estimate); Arch v5 slide 19 "
        "(S6 rwb-debtsale, DebtSaleWorkflow)"),
    "Write-off agent": ("S7",
        "Decision steps D9.2 and D9.3; FSD S7 R-WO-05 (write-off agent prepares the pack); Arch v5 slide 20 "
        "(S7 rwb-writeoff, WriteOffWorkflow)"),
    "Tracing agent": ("S9",
        "Decision steps X6 and D7.5 (Run by Tracing agent; Mode Partner); FSD S9 FEAT-PRM-05 (partner results "
        "onto the case); Arch v5 slide 17 (S9 rwb-partner, InstructionWorkflow, Act: issueInstruction). "
        "No source names the owning service (CG-B-AI-31-3; ASM-B-AI-31-4)"),
}

# ------------------------------------------------------------------ table writer
def table(wb, name, title, note, headers, rows, widths, index=None, note2=None):
    ws = wb.create_sheet(name) if index is None else wb.create_sheet(name, index)
    ws.sheet_properties.tabColor = PURPLE
    ws["A1"] = title
    ws["A1"].font = TITLE_FONT
    ws["A2"] = note
    if note2:
        ws["A3"] = note2
        ws["A3"].font = NOTE_FONT
        ws["A3"].alignment = WRAP
        hdr_row = 5
    else:
        hdr_row = 4
    ws["A2"].font = NOTE_FONT
    ws["A2"].alignment = WRAP
    for c, h in enumerate(headers, start=1):
        cell = ws.cell(hdr_row, c, h)
        cell.font = HDR_FONT
        cell.fill = HDR_FILL
        cell.alignment = Alignment(wrap_text=True, vertical="center")
        cell.border = BORDER
        ws.column_dimensions[get_column_letter(c)].width = widths[c - 1]
    ws.row_dimensions[hdr_row].height = 30
    for i, row in enumerate(rows):
        r = hdr_row + 1 + i
        for c, val in enumerate(row, start=1):
            cell = ws.cell(r, c, val)
            cell.font = BODY_FONT
            cell.alignment = WRAP
            cell.border = BORDER
            if i % 2 == 1:
                cell.fill = ALT_FILL
        lines = 1
        for c, val in enumerate(row, start=1):
            if val:
                lines = max(lines, math.ceil(len(str(val)) / max(8, widths[c - 1] * 1.05)))
        ws.row_dimensions[r].height = min(300, max(15, lines * 12.6 + 4))
    ws.freeze_panes = ws.cell(hdr_row + 1, 1)
    ws.auto_filter.ref = "%s%d:%s%d" % ("A", hdr_row, get_column_letter(len(headers)), hdr_row + len(rows))
    return ws


def readme(wb):
    ws = wb.create_sheet("Read me", 0)
    ws.sheet_properties.tabColor = PURPLE
    ws.column_dimensions["A"].width = 168
    ws["A1"] = H1
    ws["A1"].font = Font(name="Aptos", size=16, bold=True, color=PURPLE)
    ws["A2"] = H2
    ws["A2"].font = Font(name="Aptos", size=10, color="FF404040")
    ws["A4"] = ("Recovery Workbench Agent Catalog and Specifications v3. Decision D-RCV-60. "
                "The next version of v2.")
    ws["A4"].font = SUB_FONT
    ws["A4"].alignment = WRAP
    ws["A5"] = ("Every agent, decision step, mode, autonomy level and epic (Shadow from, Live from) of v2 is "
                "kept. The Agents and Decision steps sheets are the v2 text exactly as issued and no cell of "
                "them is changed; the change the realignment needs, one owning service per agent, sits in the "
                "new sheets listed below.")
    ws["A5"].font = NOTE_FONT
    ws["A5"].alignment = WRAP
    ws["A6"] = "Tool: " + TOOL + "."
    ws["A6"].font = NOTE_FONT
    ws["A7"] = ("Status: Draft. The source records no approval, so v3 is issued as Draft "
                "(CG-B-AI-31-4; ASM-B-AI-31-2).")
    ws["A7"].font = NOTE_FONT
    ws["A7"].alignment = WRAP
    ws["A9"] = "Change log"
    ws["A9"].font = SUB_FONT
    ws["A10"] = CHANGE
    ws["A10"].font = Font(name="Aptos", size=10, bold=True)
    ws["A10"].alignment = WRAP
    ws["A11"] = ("v2: the source version, carried forward unchanged (12 agents, 25 decision steps, no version "
                 "row in the source).")
    ws["A11"].font = NOTE_FONT
    ws["A11"].alignment = WRAP
    ws["A13"] = "What this version holds"
    ws["A13"].font = SUB_FONT
    what = [
        "Agents (source sheet, 16 rows): the v2 catalog exactly as issued, 12 agents across the ten behaviour "
        "columns Agent, Watches, Does, Inputs, May call, May decide alone, Escalates, Measured on, Live and "
        "Shadow from. No cell of it is changed.",
        "Decision steps (source sheet, 29 rows): the v2 table exactly as issued, 25 sub-decisions with Step, "
        "Sub-decision, Mode, Run by, Model, Autonomy at go-live, Target and First in. No cell of it is changed.",
        "Agents v3 (new sheet, 12 rows): every v2 behaviour column word for word, plus the owning service "
        "(code, service, service epic, wave), the runtime host, the decision steps the agent serves and the "
        "basis of the owner.",
        "Service summary (new sheet, 13 rows): which service owns which agent, with the count and the decision "
        "steps. P10 rwb-agent hosts all 12 runs and owns no business agent.",
        "Realignment changes (new sheet, 12 rows): one row per change with the v2 value, the v3 value, the "
        "basis in source precedence (R-PREC) and the gap or assumption that carries it.",
    ]
    r = 14
    for line in what:
        ws.cell(r, 1, line).font = NOTE_FONT
        ws.cell(r, 1).alignment = WRAP
        r += 1
    r += 1
    ws.cell(r, 1, "Counts").font = SUB_FONT
    r += 1
    counts = [
        "12 agents, 25 decision steps and 12 owning-service rows; 11 services own at least one agent "
        "(P5, P8 and S1 to S9); 2 agents sit on S1 rwb-valuation (Valuation and Route).",
        "No agent is owned by P1, P2, P3, P4, P6, P7, P9 or the platform library. P10 rwb-agent is the "
        "runtime host of all 12 agents and owns no business agent.",
        "Owning service: 9 of the 12 agents are named by an Architecture v5 service contract or an FSD feature. "
        "The Settlement and restructure agent (S2), the Valuation agent (S1) and the Tracing agent (S9) are read "
        "from the decision steps they serve; the last two carry their own assumption (ASM-B-AI-31-3, "
        "ASM-B-AI-31-4).",
        "Gap rows written: 4 (CG-B-AI-31-1 to CG-B-AI-31-4). Assumption rows written: 4 "
        "(ASM-B-AI-31-1 to ASM-B-AI-31-4). Numbering to GAP-nnnn and ASM-nnnn is left to step D1.",
    ]
    for line in counts:
        ws.cell(r, 1, line).font = NOTE_FONT
        ws.cell(r, 1).alignment = WRAP
        r += 1
    r += 1
    ws.cell(r, 1, "Sources").font = SUB_FONT
    r += 1
    sources = [
        "Recovery Workbench Agent Catalog and Specifications v2.xlsx (source, never edited).",
        "22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx and "
        "_work/msr/plan/ownership.json: services and waves, agent tables, /admin/agent-* endpoints and "
        "AgentRunWorkflow.",
        "22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (slides 15 to 20 and 41).",
        "22 Microservice Realignment/Recovery Workbench Microservice Story Template and Rules v1.md "
        "(sections R1, R3, R4, R8 and R9).",
        "FSD modules P5, P8 and S1 to S9 v3/v4 (converted text) for the sub-decision each agent serves.",
        "New decisions use the IDs in _work/msr/plan/ids.json. This document adds no architecture decision, "
        "so ADR-013 to ADR-023 and DL44 to DL49 are not used here; the one decision it cites is D-RCV-60.",
        "This document carries no release date, so no date is marked (tentative); the Shadow from and Live from "
        "columns are epic numbers, not dates, and are copied unchanged.",
    ]
    for line in sources:
        ws.cell(r, 1, line).font = NOTE_FONT
        ws.cell(r, 1).alignment = WRAP
        r += 1
    return ws


def main():
    wb = openpyxl.load_workbook(OUT)
    assert wb.sheetnames == ["Agents", "Decision steps"], wb.sheetnames

    ws_a = wb["Agents"]
    ws_d = wb["Decision steps"]
    a_hdr = [c.value for c in ws_a[4]]
    d_hdr = [c.value for c in ws_d[4]]
    assert a_hdr == ["Agent", "Watches", "Does", "Inputs", "May call", "May decide alone", "Escalates",
                     "Measured on", "Live", "Shadow from"], a_hdr
    assert d_hdr == ["Step", "Sub-decision", "Mode", "Run by", "Model", "Autonomy at go-live", "Target",
                     "First in"], d_hdr

    agents = []
    for r in range(5, ws_a.max_row + 1):
        row = [c.value for c in ws_a[r]]
        if row[0] is None:
            continue
        agents.append(row)
    assert len(agents) == 12, len(agents)

    steps = []
    for r in range(5, ws_d.max_row + 1):
        row = [c.value for c in ws_d[r]]
        if row[0] is None:
            continue
        steps.append(row)
    assert len(steps) == 25, len(steps)

    # decision steps each agent serves, in sheet order
    served = {}
    for s in steps:
        for name in OWNER:
            if name in (s[3] or ""):
                served.setdefault(name, []).append(s[0])

    # ---------------------------------------------------------- Agents v3
    rows = []
    for a in agents:
        name = a[0]
        assert name in OWNER, name
        code = OWNER[name][0]
        svc, sname, wave = SERVICES[code]
        rows.append([name, code, svc, sname, "RWB-SVC-" + code, str(wave),
                     a[1], a[2], a[3], a[4], a[5], a[6], a[7], a[8], a[9],
                     RUNTIME, ", ".join(served.get(name, [])), OWNER[name][1]])
    table(
        wb, "Agents v3",
        "The 12 agents with their owning service (D-RCV-60)",
        "One row per agent of the Agents sheet, in the same order. The behaviour columns are the v2 words "
        "exactly; the owning service is the service whose decision steps the agent serves, taken from the "
        "Ownership Map v1 sheet Services, and P10 rwb-agent is the runtime host of every run.",
        ["Agent", "Owning service (code)", "Owning service", "Service name", "Service epic", "Wave",
         "Watches", "Does", "Inputs", "May call", "May decide alone", "Escalates", "Measured on", "Live",
         "Shadow from", "Runtime host (v3)", "Decision steps served (v2)", "Basis of the owner (v3)"],
        rows,
        [26, 10, 18, 20, 13, 6, 30, 40, 30, 34, 32, 34, 26, 8, 9, 44, 16, 60])

    # ---------------------------------------------------------- Service summary
    names_by_code = {}
    steps_by_code = {}
    for a in agents:
        code = OWNER[a[0]][0]
        names_by_code.setdefault(code, []).append(a[0])
        steps_by_code.setdefault(code, []).extend(served.get(a[0], []))
    order = ["P5", "P8", "P10", "S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8", "S9"]
    summ = []
    total = 0
    for code in order:
        svc, sname, wave = SERVICES[code]
        names = names_by_code.get(code, [])
        n = len(names)
        total += n
        summ.append([code, svc, sname, "RWB-SVC-" + code, str(wave),
                     "; ".join(names) if names else "None (runtime host for all 12 agents)",
                     str(n),
                     ", ".join(steps_by_code.get(code, [])) if steps_by_code.get(code) else "-",
                     ("Arch v5 slide 16; Ownership Map v1 sheets Services, Workflows and activities, Tables and Endpoints"
                      if code == "P10" else "Owners of the Agents v3 sheet")])
    summ.append(["", "", "", "", "", "11 services own 12 agents; P10 hosts all 12 runs", str(total), "", ""])
    table(
        wb, "Service summary",
        "Agents per service (D-RCV-60)",
        "The owning service of every agent of the Agents sheet, with the count of agents it owns and the "
        "decision steps they serve. A service that owns no agent is not listed except P10, the runtime host.",
        ["Service code", "Service", "Service name", "Service epic", "Wave", "Agents owned", "Count",
         "Decision steps served", "Basis"],
        summ, [11, 18, 20, 13, 6, 46, 6, 18, 52])

    # ---------------------------------------------------------- Realignment changes
    chg = [
        [1, "Agent owning service",
         "No service per agent: the 12 agents carry behaviour, autonomy and epic only (Agents sheet)",
         "One owning service per agent, from the business service that serves its decision steps (Agents v3)",
         "Arch v5 slides 15 to 20 and 41; Ownership Map v1 sheets Services and Workflows and activities",
         "CG-B-AI-31-1; ASM-B-AI-31-1"],
        [2, "Agent runtime",
         "The agent platform is described with no service",
         "P10 rwb-agent: AgentRunWorkflow on task queue rwb-agent, 60 s then the rule result; schema rwb_agent; "
         "topic rwb.agent.events.v1",
         "Arch v5 slide 16; Ownership Map v1 sheet Workflows and activities (AgentRunWorkflow, P10), Tables "
         "(agent_* , P10), Endpoints (/admin/agent-*, P10)",
         "None (the change itself)"],
        [3, "Owner of the intake agent",
         "Not stated",
         "P5 rwb-document",
         "Arch v5 slide 16 (P5 IN: DocumentIntakeWorkflow; TMP Agent: child: classify / extract run)",
         "None"],
        [4, "Owner of the screening agent",
         "Not stated",
         "S8 rwb-deviation",
         "Arch v5 slide 15 (S8 OUT: TMP Agent: child: screening agent run); FSD S8 FEAT-DVH-07",
         "None"],
        [5, "Owner of the route agent",
         "Not stated",
         "S1 rwb-valuation",
         "Arch v5 slide 18 (rwb_valuation holds the route agent output; TMP Agent: child: route agent); "
         "FSD S1 FEAT-VAL-07",
         "None"],
        [6, "Owner of the valuation agent",
         "Not stated",
         "S1 rwb-valuation",
         "Decision step D6.1; Arch v5 slide 18 (S1 owns the valuations); FSD S1 (D6 route decision)",
         "CG-B-AI-31-2; ASM-B-AI-31-3"],
        [7, "Owner of the tracing agent",
         "Not stated",
         "S9 rwb-partner",
         "Decision steps X6 and D7.5; FSD S9 FEAT-PRM-05; Arch v5 slide 17 (S9 InstructionWorkflow)",
         "CG-B-AI-31-3; ASM-B-AI-31-4"],
        [8, "Owners of the other seven agents",
         "Not stated",
         "Settlement and restructure S2; Pricing S5; Guarantee claim S3; Reconciliation P8; Legal document S4; "
         "Debt sale S6; Write-off S7",
         "Decision steps; FSD module features; Arch v5 slides 17 to 20",
         "CG-B-AI-31-1; ASM-B-AI-31-1"],
        [9, "Autonomy, mode, model, target and epic",
         "12 agents, 25 decision steps, autonomy at go-live and target per step, Shadow from and Live from epics",
         "Unchanged: every value is kept word for word in the Agents and Decision steps sheets",
         "Agents sheet; Decision steps sheet",
         "None"],
        [10, "Naming and epics",
         "No service name, epic or wave",
         "Service names rwb-<short>, service epic RWB-SVC-<code> and the wave of the Ownership Map",
         "Template and Rules v1 R4; Ownership Map v1 sheet Services",
         "None"],
        [11, "Two agents on one service",
         "No service, so no sharing",
         "Valuation agent and Route agent both sit on S1 rwb-valuation; S1 has one contract baseline story",
         "Arch v5 slide 18 (S1: valuations, D6 route decision, route agent output)",
         "None"],
        [12, "Header, change log and status",
         "No header lines and no change-log row in the workbook; no approval recorded",
         "Read me rows 1 and 2 are the header of Template and Rules R8.1; the change-log row is the D-RCV-60 row; "
         "status Draft",
         "Template and Rules v1 R8.1 and R8.2",
         "CG-B-AI-31-4; ASM-B-AI-31-2"],
    ]
    table(
        wb, "Realignment changes",
        "What D-RCV-60 changes in the agent catalog and specifications",
        "One row per change. Source precedence is that of Template and Rules R3: the Architecture v5 catalogue "
        "slides first, then the Temporal and Drools design, then the Architecture v5 narrative. The owning "
        "service of every row is the Microservice Ownership Map v1.",
        ["#", "Item", "v2", "v3", "Basis", "Gap / assumption"],
        chg, [5, 30, 52, 62, 60, 30])

    # ---------------------------------------------------------- Read me last, moved to front
    readme(wb)

    p = wb.properties
    p.creator = "SCB Collections and Recovery"
    p.lastModifiedBy = "SCB Collections and Recovery"
    p.title = "Recovery Workbench Agent Catalog and Specifications v3"
    p.subject = "Decision D-RCV-60 microservice realignment"
    p.description = "SCB Collections and Recovery, Henka Group, 22 November 2026."
    p.keywords = "D-RCV-60; agent catalog; owning service; autonomy; rwb-agent"
    p.category = "AI and agents"
    p.created = DATE
    p.modified = DATE

    assert wb.sheetnames == ["Read me", "Agents", "Decision steps", "Agents v3", "Service summary",
                             "Realignment changes"], wb.sheetnames
    wb.save(OUT)
    print("WROTE", OUT)
    print("agents", len(agents), "steps", len(steps), "owners", total)


if __name__ == "__main__":
    main()
