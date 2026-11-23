"""Build the two B-ARCH-EVT outputs (D-RCV-60).

1. 05 Technical architecture/Recovery Workbench Event and Messaging Design v5.xlsx
   The v5 file is created first with compat/office_write.py copy; this script only
   touches the copy. The source sheets Events and Rules are left byte-identical and
   every v5 change lives in a new sheet.
2. 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx
   A new workbook, built here.

Owners, topics, tables and jobs come from the Microservice Ownership Map v1
(_work/msr/plan/ownership.json) and the Architecture v5 text extract.
"""
import math
from datetime import datetime
from pathlib import Path

import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

OUT_DESIGN = Path(r"05 Technical architecture\Recovery Workbench Event and Messaging Design v5.xlsx")
OUT_CATALOG = Path(r"05 Technical architecture\Recovery Workbench Kafka Topic and Event Catalog v1.xlsx")

TOOL = "T3 Code / OpenCode / DeepSeek v4.1 Flash"
H1 = "SCB Collections and Recovery. Henka Group, 22 November 2026."
H2 = "(C) Siam Commercial Bank and Henka Pte Ltd"
DATE = datetime(2026, 11, 22)
P8 = "Not specified in the source documents (CG-B-ARCH-EVT-8; ASM-B-ARCH-EVT-9)"
P9 = "Not specified in the source documents (CG-B-ARCH-EVT-9; ASM-B-ARCH-EVT-10)"
P11 = "Not specified in the source documents (CG-B-ARCH-EVT-11; ASM-B-ARCH-EVT-12)"
P6 = "Not specified in the source documents (CG-B-ARCH-EVT-6; ASM-B-ARCH-EVT-7)"
P5 = "Not specified in the source documents (CG-B-ARCH-EVT-5; ASM-B-ARCH-EVT-6)"

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
TOP = Alignment(vertical="top")

# ------------------------------------------------------------------ services
# code, short, name, wave  (Ownership Map sheet Services)
SERVICES = [
    ("P1", "rwb-source-data", "Source data", 1),
    ("P2", "rwb-integration", "Integration", 1),
    ("P3", "rwb-case", "Case and workflow", 1),
    ("P4", "rwb-access", "Access and authority", 1),
    ("P5", "rwb-document", "Document", 1),
    ("P6", "rwb-comms", "Communications", 1),
    ("P7", "rwb-decision", "Decision and rules", 1),
    ("P8", "rwb-payment", "Payment", 2),
    ("P9", "rwb-reporting", "Reporting", 1),
    ("P10", "rwb-agent", "Agent", 1),
    ("S1", "rwb-valuation", "Valuation and route", 3),
    ("S2", "rwb-treatment", "Treatment and offer", 2),
    ("S3", "rwb-guarantee", "Guarantee", 3),
    ("S4", "rwb-litigation", "Litigation", 3),
    ("S5", "rwb-asset", "Asset", 2),
    ("S6", "rwb-debtsale", "Debt sale", 3),
    ("S7", "rwb-writeoff", "Write-off", 4),
    ("S8", "rwb-deviation", "Deviation", 2),
    ("S9", "rwb-partner", "Partner", 4),
]
CODE = {s[1]: s[0] for s in SERVICES}
WAVE = {s[1]: s[3] for s in SERVICES}
NAME = {s[1]: s[2] for s in SERVICES}
TOPIC = {s[1]: "rwb.%s.events.v1" % s[1].replace("rwb-", "") for s in SERVICES}

V4 = {  # payload words of v4, copied character for character
    "EV-01": "caseId, caseNo, productGroup, accounts, businessDate",
    "EV-02": "caseId, queueId, ownerId, ruleId, ruleVersion",
    "EV-03": "caseId, reason, ruleGap",
    "EV-04": "caseId, fromOwner, toOwner, reasonCode",
    "EV-05": "caseId, fromState, toState, ruleId, decisionLogEntryId",
    "EV-06": "caseId, deviationCode, raisedBy",
    "EV-07": "caseId, deviationCode, outcome",
    "EV-08": "entryId, caseId, decisionCode, approver",
    "EV-09": "approvalId, caseId, level, amount",
    "EV-10": "treatmentId, caseId, terms",
    "EV-11": "treatmentId, bookingRef, businessDate",
    "EV-12": "treatmentId, dueDate, amountDue",
    "EV-13": "noticeId, caseId, type, templateVersion",
    "EV-14": "noticeId, barcode, sentDate",
    "EV-15": "noticeId, deliveredAt, status",
    "EV-16": "documentId, caseId, type, source",
    "EV-17": "documentId, fields, confidence",
    "EV-18": "timerId, caseId, timerType",
    "EV-19": "timerId, caseId, escalateTo",
    "EV-20": "instructionId, partnerId, type, dueOn",
    "EV-21": "instructionId, result, documents",
    "EV-22": "assetId, caseId, source",
    "EV-23": "lotId, buyerId, price",
    "EV-24": "writeOffId, caseId, amount",
    "EV-25": "proceedsId, caseId, amount",
    "EV-26": "sourceSystem (source_system), businessDate (business_date), status, completedAt (completed_at)",
    "EV-27": "sourceSystem (source_system), businessDate (business_date), status, completedAt (completed_at)",
    "EV-28": "runId, agent, caseId, outcome, fallback",
    "EV-29": "caseId, eventType, sourceEventId, businessDate",
    "EV-30": "packageCode, packageVersion, versionId, validFrom, approvedBy",
}

# id, name, topic short, direction, consumers, family, change
EVENTS = [
    ("EV-01", "CaseCreated", "rwb-case", "Published", ["rwb-agent", "rwb-deviation", "rwb-reporting"],
     "Domain event", "Unchanged; event type named (D-RCV-60)"),
    ("EV-02", "CaseAllocated", "rwb-case", "Published", ["rwb-reporting"], "Domain event",
     "Unchanged; event type named (D-RCV-60)"),
    ("EV-03", "CaseAllocationFailed", "rwb-case", "Published", ["rwb-case"], "Domain event",
     "Unchanged; event type named (D-RCV-60)"),
    ("EV-04", "CaseTransferred", "rwb-case", "Published", ["rwb-reporting"], "Domain event",
     "Unchanged; event type named (D-RCV-60)"),
    ("EV-05", "CaseStateChanged", "rwb-case", "Published", ["rwb-comms", "rwb-reporting"], "Domain event",
     "Unchanged; event type named (D-RCV-60)"),
    ("EV-06", "DeviationRaised", "rwb-deviation", "Published", ["rwb-case", "rwb-comms", "rwb-treatment"],
     "Domain event", "Unchanged; event type named (D-RCV-60)"),
    ("EV-07", "DeviationCleared", "rwb-deviation", "Published", ["rwb-case", "rwb-comms"], "Domain event",
     "Unchanged; event type named (D-RCV-60)"),
    ("EV-08", "DecisionRecorded", "rwb-decision", "Published (all 19 producers)", ["rwb-decision", "rwb-reporting"],
     "Domain event (shared topic)", "Topic set: rwb.decision-record.v1 (Arch v5 slide 42 row 08)"),
    ("EV-09", "ApprovalRequested", "rwb-decision", "Published", ["gateway-bff"], "Domain event",
     "Unchanged; event type named (D-RCV-60)"),
    ("EV-10", "TreatmentApproved", "rwb-treatment", "Published", ["rwb-comms", "rwb-payment"], "Domain event",
     "Unchanged; event type named (D-RCV-60)"),
    ("EV-11", "TreatmentBooked", "rwb-payment", "Published", ["rwb-case", "rwb-treatment"], "Domain event",
     "Unchanged; event type named (D-RCV-60)"),
    ("EV-12", "PaymentMissed", "rwb-payment", "Published", ["rwb-case", "rwb-treatment", "rwb-comms"],
     "Domain event", "Unchanged; event type named (D-RCV-60)"),
    ("EV-13", "NoticeGenerated", "rwb-comms", "Published", ["rwb-decision"], "Domain event",
     "Unchanged; event type named (D-RCV-60)"),
    ("EV-14", "NoticeDispatched", "rwb-comms", "Published", ["rwb-reporting"], "Domain event",
     "Unchanged; event type named (D-RCV-60)"),
    ("EV-15", "NoticeDelivered", "rwb-comms", "Published", ["rwb-litigation", "rwb-guarantee", "rwb-case"],
     "Domain event", "Unchanged; event type named (D-RCV-60)"),
    ("EV-16", "DocumentStored", "rwb-document", "Published", ["rwb-agent", "rwb-case"], "Domain event",
     "Unchanged; event type named (D-RCV-60)"),
    ("EV-17", "DocumentFieldsExtracted", "rwb-document", "Published", ["rwb-case"], "Domain event",
     "Unchanged; event type named (D-RCV-60)"),
    ("EV-18", "TimerDue", "", "Retired", [], "Retired (durable timer)",
     "Retired in v5: no event type and no topic (CG-B-ARCH-EVT-1; ASM-B-ARCH-EVT-2)"),
    ("EV-19", "TimerBreached", "rwb-case", "Published", ["gateway-bff"], "Domain event",
     "Unchanged; event type named (D-RCV-60)"),
    ("EV-20", "InstructionIssued", "rwb-partner", "Published", ["partner portal"], "Domain event",
     "Unchanged; event type named (D-RCV-60)"),
    ("EV-21", "PartnerResultSubmitted", "rwb-partner", "Published",
     ["rwb-litigation", "rwb-asset", "rwb-case"], "Domain event",
     "Direction and owner changed: v4 Consumed, Partner portal (CG-B-ARCH-EVT-2; ASM-B-ARCH-EVT-3)"),
    ("EV-22", "AssetTakenOn", "rwb-asset", "Published", ["rwb-case", "rwb-payment"], "Domain event",
     "Unchanged; event type named (D-RCV-60)"),
    ("EV-23", "LotAwarded", "rwb-debtsale", "Published", ["rwb-case", "rwb-payment"], "Domain event",
     "Unchanged; event type named (D-RCV-60)"),
    ("EV-24", "WriteOffApproved", "rwb-writeoff", "Published",
     ["rwb-case", "rwb-payment", "rwb-reporting"], "Domain event", "Unchanged; event type named (D-RCV-60)"),
    ("EV-25", "ProceedsMatched", "rwb-payment", "Published",
     ["rwb-case", "rwb-asset", "rwb-debtsale", "rwb-writeoff", "rwb-guarantee"], "Domain event",
     "Unchanged; event type named (D-RCV-60)"),
    ("EV-26", "AceDataReady", "rwb-source-data", "Published",
     ["rwb-case", "rwb-payment", "rwb-deviation", "rwb-writeoff"], "Domain event",
     "Direction and owner changed: v4 Consumed, ACE ingestion (CG-B-ARCH-EVT-3; ASM-B-ARCH-EVT-4)"),
    ("EV-27", "AceDataLate", "rwb-source-data", "Published", ["alerts", "gateway-bff"], "Domain event",
     "Owner set (P1, Arch v5 slide 43 row 27)"),
    ("EV-28", "AgentRunCompleted", "rwb-agent", "Published",
     ["rwb-decision", "rwb-document", "rwb-deviation"], "Domain event", "Unchanged; event type named (D-RCV-60)"),
    ("EV-29", "CaseEvent", "", "Signal", ["CaseWorkflow (Temporal signal)"], "Temporal signal",
     "Not on Kafka: signal on the workflow ID case-{caseId} (Arch v5 slide 43 row 29)"),
    ("EV-30", "RulePackageInForce", "rwb-decision", "Application event",
     ["rwb-case", "rwb-valuation", "rwb-treatment", "rwb-payment"], "Application event",
     "Transport set: published on rwb.decision.events.v1 (Arch v5 slide 41)"),
    ("", "ApprovalDecided", "rwb-decision", "Published", [P9], "Domain event (v5 catalogue)",
     "New in v5 (Arch v5 slide 41, rwb-decision topic line)"),
    ("", "ReportPublished", "rwb-reporting", "Published", [P9], "Domain event (v5 catalogue)",
     "New in v5 (Arch v5 slide 41, rwb-reporting topic line)"),
    ("", "FileDelivered", "rwb-integration", "Published", ["requesting service"], "Domain event (v5 catalogue)",
     "New in v5 (Arch v5 slide 43, + row)"),
    ("", "FileFailed", "rwb-integration", "Published", ["requesting service"], "Domain event (v5 catalogue)",
     "New in v5 (Arch v5 slide 43, + row)"),
    ("", "RouteDecided", "rwb-valuation", "Published", ["rwb-case"], "Domain event (v5 catalogue)",
     "New in v5 (Arch v5 slide 43, + row)"),
    ("", "TreatmentClosed", "rwb-treatment", "Published", ["rwb-case", "rwb-reporting"], "Domain event (v5 catalogue)",
     "New in v5 (Arch v5 slide 43, + row)"),
    ("", "GuaranteeClaimFiled", "rwb-guarantee", "Published", ["rwb-case", "rwb-reporting"],
     "Domain event (v5 catalogue)", "New in v5 (Arch v5 slide 41; slide 43 GuaranteeClaim*)"),
    ("", "GuaranteeClaimSettled", "rwb-guarantee", "Published", ["rwb-case", "rwb-reporting"],
     "Domain event (v5 catalogue)", "New in v5 (Arch v5 slide 41; slide 43 GuaranteeClaim*)"),
    ("", "LawsuitFiled", "rwb-litigation", "Published", [P9], "Domain event (v5 catalogue)",
     "New in v5 (Arch v5 slide 41, rwb-litigation topic line)"),
    ("", "JudgmentRecorded", "rwb-litigation", "Published", ["rwb-asset", "rwb-case"], "Domain event (v5 catalogue)",
     "New in v5 (Arch v5 slide 43, + row)"),
    ("", "AuctionResult", "rwb-litigation", "Published", ["rwb-asset", "rwb-case"], "Domain event (v5 catalogue)",
     "New in v5 (Arch v5 slide 43, + row)"),
    ("", "AssetSold", "rwb-asset", "Published", ["rwb-payment", "rwb-case"], "Domain event (v5 catalogue)",
     "New in v5 (Arch v5 slide 43, + row)"),
    ("", "AccountsTransferred", "rwb-debtsale", "Published", ["rwb-case", "rwb-reporting"],
     "Domain event (v5 catalogue)", "New in v5 (Arch v5 slide 43, + row)"),
    ("", "AccessPolicyChanged", "rwb-access", "Published", ["all (cache refresh)"], "Domain event (v5 catalogue)",
     "New in v5 (Arch v5 slide 41, rwb-access topic line)"),
    ("", "DoaLimitChanged", "rwb-access", "Published", ["all (cache refresh)"], "Domain event (v5 catalogue)",
     "New in v5 (Arch v5 slide 41, rwb-access topic line)"),
]


def topic_of(short):
    return "rwb.%s.events.v1" % short.replace("rwb-", "")


def ce_type(name, short):
    if short:
        return "rwb.%s.%s.v1" % (short.replace("rwb-", ""), name)
    if name == "CaseEvent":
        return "None (Temporal signal)"
    return "None (retired)"


def owner(ev):
    name, short = ev[1], ev[2]
    if name == "DecisionRecorded":
        return "P7", "Decision and rules"
    if ev[0] == "EV-29":
        return "P3", "Case and workflow"
    if not short:
        return "PLT", "Platform library"
    return CODE[short], NAME[short]


def event_topic(ev):
    name, short = ev[1], ev[2]
    if not short:
        return "None (not on Kafka)"
    if name == "DecisionRecorded":
        return "rwb.decision-record.v1"
    return topic_of(short)


def payload_of(ev):
    return V4.get(ev[0], P8) if ev[0] else P8


def consumers_str(ev):
    cons = ev[4]
    if not cons:
        return "None (retired)"
    if cons == [P9]:
        return P9
    return ", ".join(cons)


def union_consumers(evs):
    out = []
    for e in evs:
        for c in e[4]:
            if c == P9:
                c = "open (%s; CG-B-ARCH-EVT-9; ASM-B-ARCH-EVT-10)" % e[1]
            if c not in out:
                out.append(c)
    return ", ".join(out)


# --------------------------------------------------------------- table writer
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


def readme(wb, title_line, subtitle, change_row, previous_row, what, counts, sources, status=True):
    ws = wb.create_sheet("Read me", 0)
    ws.sheet_properties.tabColor = PURPLE
    ws.column_dimensions["A"].width = 168
    ws["A1"] = H1
    ws["A1"].font = Font(name="Aptos", size=16, bold=True, color=PURPLE)
    ws["A2"] = H2
    ws["A2"].font = Font(name="Aptos", size=10, color="FF404040")
    ws["A4"] = title_line
    ws["A4"].font = SUB_FONT
    ws["A4"].alignment = WRAP
    ws["A5"] = subtitle
    ws["A5"].font = NOTE_FONT
    ws["A5"].alignment = WRAP
    ws["A6"] = "Tool: " + TOOL + "."
    ws["A6"].font = NOTE_FONT
    if status:
        ws["A7"] = "Status: Draft. This document is issued with no approval recorded (ASM-B-ARCH-EVT-1)."
        ws["A7"].font = NOTE_FONT
        ws["A7"].alignment = WRAP
    ws["A9"] = "Change log"
    ws["A9"].font = SUB_FONT
    ws["A10"] = change_row
    ws["A10"].font = Font(name="Aptos", size=10, bold=True)
    ws["A10"].alignment = WRAP
    ws["A11"] = previous_row
    ws["A11"].font = NOTE_FONT
    ws["A11"].alignment = WRAP
    ws["A13"] = "What this version holds"
    ws["A13"].font = SUB_FONT
    r = 14
    for line in what:
        ws.cell(r, 1, line).font = NOTE_FONT
        ws.cell(r, 1).alignment = WRAP
        r += 1
    r += 1
    ws.cell(r, 1, "Counts").font = SUB_FONT
    r += 1
    for line in counts:
        ws.cell(r, 1, line).font = NOTE_FONT
        ws.cell(r, 1).alignment = WRAP
        r += 1
    r += 1
    ws.cell(r, 1, "Sources").font = SUB_FONT
    r += 1
    for line in sources:
        ws.cell(r, 1, line).font = NOTE_FONT
        ws.cell(r, 1).alignment = WRAP
        r += 1
    return ws


# ================================================================ workbook A
def build_design():
    wb = openpyxl.load_workbook(OUT_DESIGN)
    assert wb.sheetnames == ["Events", "Rules"], wb.sheetnames

    p = wb.properties
    p.creator = "SCB Collections and Recovery"
    p.lastModifiedBy = "SCB Collections and Recovery"
    p.title = "Recovery Workbench Event and Messaging Design v5"
    p.subject = "Decision D-RCV-60 microservice realignment"
    p.description = "SCB Collections and Recovery, Henka Group, 22 November 2026."
    p.keywords = "D-RCV-60; event and messaging; Kafka; CloudEvents; v5"
    p.category = "Technical architecture"
    p.created = DATE
    p.modified = DATE

    readme(
        wb,
        "Recovery Workbench Event and Messaging Design v5. Decision D-RCV-60. The next version of v4.",
        "Every ID, number and date of v4 is kept. The Events and Rules sheets are the v4 text exactly as issued "
        "(version 4, 16 November 2026, D-RCV-36) and no cell of them is changed; every change of the realignment "
        "sits in the new sheets listed below.",
        "v5, 22 November 2026, D-RCV-60 microservice realignment, " + TOOL,
        "v4, 16 November 2026, D-RCV-36: the source version, carried forward unchanged (30 entries, 10 rules).",
        [
            "Events v5: the target register. The 30 v4 entries keep their ID, payload words and consumer meaning; "
            "each event type gains the name rwb.<short>.<Event>.v1, its owner service and its one topic, and the "
            "15 event types that exist only in the Architecture v5 service catalogue follow, unnumbered.",
            "Topics: one row per event topic. 19 service topics rwb.<short>.events.v1 and the shared "
            "rwb.decision-record.v1, with owner, wave, settings, event types and consumers.",
            "Dead-letter topics: the 20 dead-letter topics of the set, named by the .dlt suffix the source gives.",
            "Envelope: the CloudEvents 1.0 binary-mode headers, the record key and the payload rule.",
            "Outbox and inbox: the four library objects that give the at-least-once delivery its "
            "exactly-once effect, and the relay that publishes them.",
            "Rules v5 additions: the rules the Kafka target adds, including the replacement of the v4 exception "
            "queue by the retry ladder and the dead-letter topic.",
            "Realignment changes: one row per change, with the v4 value, the v5 value, the basis in source "
            "precedence and the gap or assumption that carries it.",
        ],
        [
            "43 event types on 20 topics: 28 carry an EV row of v4 (EV-18 is retired and EV-29 is a Temporal "
            "signal, so 30 entries give 28 topic events) and 15 exist only in the Architecture v5 service catalogue.",
            "100 Kafka topics: 20 event topics, 60 retry topics (3 per event topic) and 20 dead-letter topics.",
            "19 services publish, the shared topic has 19 producers, and every service creates its own outbox and "
            "inbox in its own schema.",
        ],
        [
            "Recovery Workbench Event and Messaging Design v4, 16 November 2026, D-RCV-36 (the source of this "
            "version).",
            "Recovery Workbench Architecture v5 Text Extract v1, slides 9, 11, 20, 21, 22, 41, 42, 43 and 44.",
            "Recovery Workbench Temporal and Drools Design Text Extract v1, slides 14 and 15.",
            "Recovery Workbench Microservice Ownership Map v1, sheets Services and Events, and "
            "_work/msr/plan/ownership.json.",
            "Recovery Workbench Microservice Story Template and Rules v1, §R4, §R8.1, §R8.2 and §R9.",
            "Candidate gap rows CG-B-ARCH-EVT-1 to CG-B-ARCH-EVT-12 and candidate assumption rows "
            "ASM-B-ARCH-EVT-1 to ASM-B-ARCH-EVT-14 are written by this work package; step D1 renumbers them as "
            "GAP-nnnn and ASM-nnnn.",
        ],
    )

    # ---------------------------------------------------------- Events v5
    rows = []
    for ev in EVENTS:
        name, short = ev[1], ev[2]
        ocode, oname = owner(ev)
        rows.append([
            ev[0] or "new",
            name,
            ce_type(name, short),
            event_topic(ev),
            ocode,
            oname,
            ev[3],
            payload_of(ev),
            consumers_str(ev),
            ev[5],
            ev[6],
        ])
    ws = table(
        wb, "Events v5", "Events inside the Workbench: the v5 register (D-RCV-60)",
        "A row with no EV number is an event type that exists only in the Architecture v5 service catalogue "
        "(slide 41 topic lines and slide 43 + rows); it is keyed by name and not renumbered "
        "(ASM-B-ARCH-EVT-14). Owner and topic are those of the Microservice Ownership Map v1. Consumers are the "
        "consuming services of Architecture v5 slides 42 and 43.",
        ["ID", "Event", "Event type (ce_type)", "Topic", "Owner code", "Owner service", "Direction (v5)",
         "Payload", "Consumers (v5)", "Family", "Change from v4"],
        rows, [11, 24, 34, 26, 8, 20, 16, 44, 34, 22, 40],
    )
    ws["A2"].alignment = WRAP

    # ---------------------------------------------------------- Topics
    by_topic = {}
    for ev in EVENTS:
        t = event_topic(ev)
        if t.startswith("rwb."):
            by_topic.setdefault(t, []).append(ev)

    rows = []
    order = [s[1] for s in SERVICES]
    for short in order:
        t = topic_of(short)
        evs = by_topic.get(t, [])
        rows.append([
            t, "Event topic", CODE[short], short, WAVE[short], 12, 3, "7 days", "caseId",
            ", ".join(e[1] for e in evs), union_consumers(evs),
            "Arch v5 slides 9 and 41 (settings, topic, owner)",
        ])
    rows.append([
        "rwb.decision-record.v1", "Shared event topic", "P7", "shared by the 19 services", 0,
        P6, P6, P6, P6,
        "DecisionRecorded", union_consumers(by_topic.get("rwb.decision-record.v1", [])),
        "Arch v5 slides 20 and 42 row 08; Ownership Map row EV-08 (owner P7)",
    ])
    table(
        wb, "Topics", "Recovery event topics: 20 topics, one per service and the shared decision-record topic",
        "Settings of the service topics are those of Architecture v5 slide 9: 12 partitions, replication factor 3, "
        "7-day retention, cleanup policy delete and record key caseId. Each topic has three retry topics (1 min, "
        "10 min, 1 h) and one dead-letter topic; the retry topic names are not stated by any source "
        "(CG-B-ARCH-EVT-4; ASM-B-ARCH-EVT-5).",
        ["Topic", "Kind", "Owner code", "Owner service", "Wave", "Partitions", "Replication", "Retention", "Key",
         "Event types carried", "Consumers", "Basis"],
        rows, [28, 15, 8, 24, 6, 11, 11, 10, 9, 46, 46, 34],
    )

    # ---------------------------------------------------------- Dead-letter topics
    rows = []
    for short in order:
        t = topic_of(short)
        rows.append([t + ".dlt", t, CODE[short], "Same as its event topic (12)", P5.replace("CG-B-ARCH-EVT-5", "CG-B-ARCH-EVT-5"),
                     "One alert per record; replay tool", "Arch v5 slides 9 and 22 ('.dlt'), RWB-PLT-N002-INF AC2"])
    rows.append(["rwb.decision-record.v1.dlt", "rwb.decision-record.v1", "P7", "Same as its event topic",
                 P5, "One alert per record; replay tool",
                 "Arch v5 slides 9 and 22 ('.dlt'); shared topic settings at CG-B-ARCH-EVT-6"])
    table(
        wb, "Dead-letter topics", "Dead-letter topics: 20, one per event topic",
        "A record that fails the three retry windows goes to the dead-letter topic of its event topic, with one "
        "alert and the replay tool as the recovery path (Arch v5 slide 22). The .dlt suffix is the one the source "
        "gives; the full name is derived from it (ASM-B-ARCH-EVT-6) and its replication factor and retention are "
        "not stated by any source (CG-B-ARCH-EVT-5).",
        ["Dead-letter topic", "Event topic it serves", "Owner code", "Partitions", "Replication and retention",
         "Alert and replay", "Basis"],
        rows, [34, 30, 9, 24, 40, 32, 40],
    )

    # ---------------------------------------------------------- Envelope
    rows = [
        ["Mode", "CloudEvents 1.0, Kafka binding in binary mode: the ce_* attributes travel as headers and the "
                 "body is the JSON payload", "Arch v5 slides 9 and 22"],
        ["ce_specversion", "1.0", "Arch v5 slide 22 (CloudEvents 1.0)"],
        ["ce_id", "The identity of the event. It is the key of the inbox row, so a redelivery is recognised and "
                  "ignored (CG-B-ARCH-EVT-12; ASM-B-ARCH-EVT-13)", "Arch v5 slide 22 (inbox holds ce_id)"],
        ["ce_type", "rwb.<short>.<Event>.v1 of the owning service, for example rwb.case.CaseCreated.v1; "
                    "DecisionRecorded is rwb.decision.DecisionRecorded.v1",
         "Template and Rules §R4; ASM-B-ARCH-EVT-14"],
        ["ce_source", P11, "Arch v5 slide 22 names the header only"],
        ["ce_subject", P11, "Arch v5 slide 22 names the header only"],
        ["traceparent", "W3C Trace Context header, written by the producer and passed through the relay and every "
                        "consumer", "Arch v5 slides 9 and 22"],
        ["Body", "JSON, validated against the schema registry with BACKWARD compatibility; IDs, codes and facts "
                 "only, never personal data", "Arch v5 slide 22; v4 rule Payload"],
        ["Kafka record key", "caseId, so every event of one case is ordered in one partition",
         "Arch v5 slide 9 (key caseId)"],
        ["Schema version", "Carried by ce_type (.v1) and by the registry subject; a consumer accepts the current "
                           "and the previous version (CG-B-ARCH-EVT-10; ASM-B-ARCH-EVT-11)",
         "Arch v5 slide 22; v4 rule Versioning"],
        ["Idempotency key", "ce_id. The inbox table processed_event holds it, and the duplicate count of R-UNI-40 "
                            "is taken from that table (CG-B-ARCH-EVT-12; ASM-B-ARCH-EVT-13)",
         "Arch v5 slide 22; v4 rule Duplicates"],
        ["Producer guarantees", "Idempotent producer with acks=all and min.insync.replicas=2; the relay marks the "
                                "outbox row sent after the broker acknowledges",
         "Arch v5 slide 22 (sample PaymentMissed notes)"],
        ["Consumer groups", "One consumer group per service per topic, so a new consumer never changes the "
                            "producer", "Arch v5 slide 22"],
    ]
    table(
        wb, "Envelope", "The envelope every event carries",
        "Architecture v5 fixes the CloudEvents 1.0 binary mode, the four ce_* headers, the traceparent header, the "
        "JSON body and the record key. The values of ce_source and ce_subject are not stated by any source and are "
        "left to the event naming library RWB-PLT-E1047-CON.",
        ["Item", "Value in v5", "Basis"], rows, [22, 96, 40],
    )

    # ---------------------------------------------------------- Outbox and inbox
    rows = [
        ["outbox_event", "PLT (definition); created in every service schema rwb_*",
         "The event row written in the same transaction as the state change of the producer",
         "One row per event, written with the change or not at all; the relay publishes it and marks it sent",
         "Arch v5 slide 22; DP-09, RWB-PLT-TE006; Ownership Map tables rows outbox_event"],
        ["outbox_delivery", "PLT (definition); created in every service schema",
         "The delivery attempt and the retry state of an outbox row",
         "One row per relay attempt; a broker failure leaves the event in the outbox and the relay retries",
         "Arch v5 slide 22; Ownership Map tables rows outbox_delivery"],
        ["processed_event", "PLT (definition); created in the schema of every consumer",
         "The inbox: the ce_id of every event a service has already applied",
         "ce_id is unique; the row is written in the same transaction as the consumer's own change, so a "
         "redelivery has no second effect (R-UNI-40)",
         "Arch v5 slide 22; DP-09; Ownership Map tables rows processed_event"],
        ["idempotency_key", "PLT (definition); created in every service schema",
         "The stored response of a POST, keyed by the Idempotency-Key header",
         "One row per POST key; a repeat returns the stored response and does not run the change",
         "Arch v5 slide 11; Ownership Map tables rows idempotency_key"],
        ["Outbox relay (JOB-11)", "every service",
         "Inside each service, reading its own outbox",
         "Every minute: publish the unsent rows to the service topic and to rwb.decision-record.v1, then mark "
         "them sent", "Arch v5 slide 44 (JOB-11 outbox sender, every minute, every service)"],
        ["Transaction boundary", "the producing service",
         "One local transaction in the producer's schema",
         "The change, the decision record and the outbox row commit together: no event without the change and no "
         "change without the event. EV-26 and EV-27 stay exempt, because they are raised from the ACE batch record",
         "v4 rule Transactions; Arch v5 slide 22"],
        ["Multi-step outbound work", "P2 rwb-integration",
         "The outbox of rwb_integration",
         "From Epic 3 the multi-step outbound chain writes through the outbox before the external call",
         "v4 rule Outbox; DP-16"],
    ]
    table(
        wb, "Outbox and inbox", "Outbox, inbox and the transaction boundary of an event",
        "The four objects are library objects of the platform (RWB-PLT-TE006) and each service creates its own "
        "copy in its own schema; the Ownership Map holds that ruling for outbox_event, outbox_delivery, "
        "processed_event and idempotency_key.",
        ["Object", "Owner", "Where it lives", "Purpose", "Rule in v5", "Basis"], rows,
        [26, 30, 40, 40, 60, 44],
    )

    # ---------------------------------------------------------- Rules v5 additions
    rows = [
        ["Transport", "Every domain event travels on the Kafka topic of its owning service. The outbox of the "
                      "producer's schema is the transaction boundary and a relay publishes (ADR-015).",
         "Arch v5 slides 9 and 22; ADR-015"],
        ["Topic naming", "rwb.<short>.events.v1, one per service, plus the shared rwb.decision-record.v1. No "
                         "service publishes on another service's topic; the legacy rwb.p<n>. and rwb.casewf. names "
                         "are not provisioned.", "DP-14; RWB-PLT-E1047-CON; Template and Rules §R4"],
        ["Topic settings", "12 partitions, replication factor 3, 7-day retention, cleanup policy delete and record "
                           "key caseId on every event topic; the shared topic takes the same settings "
                           "(CG-B-ARCH-EVT-6; ASM-B-ARCH-EVT-7).", "Arch v5 slide 9"],
        ["Envelope", "CloudEvents 1.0 in binary mode: ce_id, ce_type, ce_source and ce_subject as headers, the "
                     "W3C traceparent header and a JSON body. ce_type is rwb.<short>.<Event>.v1 "
                     "(ASM-B-ARCH-EVT-14).", "Arch v5 slide 22"],
        ["Registry", "A JSON Schema registry with BACKWARD compatibility; the AsyncAPI 3.0 document of the topic "
                     "is the contract; a consumer accepts the current and the previous schema version. No subject "
                     "is named in this version (CG-B-ARCH-EVT-10; ASM-B-ARCH-EVT-11).",
         "Arch v5 slides 9 and 22; v4 rule Versioning"],
        ["Failure", "A consumer failure is retried on the three retry topics (1 min, 10 min, 1 h) and the record "
                    "then goes to the dead-letter topic of its event topic, with one alert and the replay tool as "
                    "the recovery path. The v4 exception queue is the dead-letter topic "
                    "(CG-B-ARCH-EVT-7; ASM-B-ARCH-EVT-8).",
         "Arch v5 slides 9 and 22"],
        ["Delivery and duplicates", "At least once, consumers idempotent; each consumer records ce_id in "
                                    "processed_event in the same transaction as its change, and a repeat is "
                                    "ignored and counted (R-UNI-40) (CG-B-ARCH-EVT-12; ASM-B-ARCH-EVT-13).",
         "Arch v5 slide 22; v4 rules Delivery and Duplicates"],
        ["Transactions", "The event is written in the same transaction as the change. EV-26 and EV-27 stay exempt: "
                         "rwb-source-data raises them from the ACE batch record it reads through "
                         "recovery.v_ace_batch_status, and a read is not a change.",
         "v4 rule Transactions; CG-B-ARCH-EVT-3; ASM-B-ARCH-EVT-4"],
        ["Decision record", "Every service writes its decision record locally in the same transaction and "
                            "publishes DecisionRecorded on rwb.decision-record.v1; rwb-decision consumes it into "
                            "the central ledger within 5 minutes, with gap alerts and chain verification.",
         "Arch v5 slides 20 and 37; DP-03; RWB-PLT-E1027-CON"],
        ["Case router", "An event reaches a case through the case router in rwb-case (a Kafka consumer that calls "
                        "signalWithStart), never by a direct call. EV-29 is the signal itself: it is not a domain "
                        "event and is not written to the outbox.",
         "v4 rule Signals; Temporal and Drools design slide 14"],
        ["Ordering", "Events of one case are processed in the order they were written, by one sequence per case in "
                     "the outbox, and the record key caseId keeps them in one partition.", "Arch v5 slide 9; v4 rule Ordering"],
        ["Platform", "The topics are hosted on the bank Kafka platform ACE already uses, separate from the ACE PII "
                     "logging topics, with one principal per service and ACLs from the event catalogue; Azure "
                     "Event Hubs Premium through its Kafka endpoint is the fallback.",
         "Arch v5 slides 21 and 35; RWB-PLT-N002-INF"],
    ]
    table(
        wb, "Rules v5 additions", "The rules the Kafka target adds to the ten rules of the Rules sheet",
        "The Rules sheet keeps the ten v4 rules word for word. These rows are the rules of the target that the "
        "realignment adds or changes; where a v4 rule is replaced, the row says so and names the gap.",
        ["Rule", "Detail", "Basis"], rows, [24, 104, 40],
    )

    # ---------------------------------------------------------- Realignment changes
    rows = [
        [1, "Event transport", "Domain events are in-process in the ACE service and written to the outbox; there "
                               "is no external event bus (D-RCV-35)",
         "Each service publishes on its own Kafka topic and on rwb.decision-record.v1 through its outbox and a "
         "relay", "Arch v5 slides 9, 21 and 22; ADR-015", "None (the change itself)"],
        [2, "Topic name", "No topic name in v4", "rwb.<short>.events.v1 for the 19 services and the shared "
                                                  "rwb.decision-record.v1", "Template and Rules §R4; DP-14",
         "None"],
        [3, "Event type name", "An event has a name and a module, no type name",
         "rwb.<short>.<Event>.v1; 43 types, of which 15 are new", "Template and Rules §R4", "ASM-B-ARCH-EVT-14"],
        [4, "Retry and dead letter", "A failed consumer retries and then the event goes to the exception queue",
         "Three retry topics (1 min, 10 min, 1 h) and then <topic>.dlt with an alert and a replay tool",
         "Arch v5 slides 9 and 22", "CG-B-ARCH-EVT-4, CG-B-ARCH-EVT-5, CG-B-ARCH-EVT-7; ASM-B-ARCH-EVT-5, "
                                    "ASM-B-ARCH-EVT-6, ASM-B-ARCH-EVT-8"],
        [5, "Delivery guarantee", "At least once, consumers idempotent, event ID and idempotency key",
         "At least once; the inbox records ce_id in the same transaction as the consumer's change; the idempotency "
         "key is ce_id", "Arch v5 slide 22", "CG-B-ARCH-EVT-12; ASM-B-ARCH-EVT-13"],
        [6, "Transactions", "The event is written in the same transaction as the change in the one schema",
         "The same rule in the producer's own schema, with the relay outside the transaction",
         "Arch v5 slide 22", "None"],
        [7, "EV-18 TimerDue", "Published by the Case and workflow module, consumer Rules component",
         "Retired: no event type and no topic; the timer is a durable Temporal timer and PLT owns the capability",
         "Arch v5 slide 42 row 18; Ownership Map", "CG-B-ARCH-EVT-1; ASM-B-ARCH-EVT-2"],
        [8, "EV-21 PartnerResultSubmitted", "Consumed; owning module Partner portal",
         "Published by S9 rwb-partner on rwb.partner.events.v1; consumers rwb-litigation, rwb-asset, rwb-case",
         "Arch v5 slide 43 row 21; Ownership Map", "CG-B-ARCH-EVT-2; ASM-B-ARCH-EVT-3"],
        [9, "EV-26 AceDataReady", "Consumed; ACE ingestion, read through v_ace_batch_status",
         "Published by P1 rwb-source-data on rwb.source-data.events.v1; consumers rwb-case, rwb-payment, "
         "rwb-deviation, rwb-writeoff", "Arch v5 slide 43 row 26; Ownership Map",
         "CG-B-ARCH-EVT-3; ASM-B-ARCH-EVT-4"],
        [10, "EV-27 AceDataLate", "Published by the Recovery data engine from v_ace_batch_status",
         "Published by P1 rwb-source-data on rwb.source-data.events.v1; consumers alerts and the gateway-bff banner",
         "Arch v5 slides 15 and 43 row 27", "None"],
        [11, "EV-29 CaseEvent", "Temporal signal to CaseWorkflow on case-{caseId}",
         "Unchanged: a Temporal signal, not a topic event and not written to the outbox",
         "Arch v5 slide 43 row 29; Temporal and Drools design slide 14", "None"],
        [12, "EV-30 RulePackageInForce", "Application event of the Rules module with no topic",
         "Application event published by P7 rwb-decision on rwb.decision.events.v1, consumed by the services that "
         "load a rule package", "Arch v5 slide 41 (rwb-decision topic line)", "None"],
        [13, "Consumers", "Consumer modules of the monolith: Allocation, ledger, reporting, timers, exception queue",
         "Consumer services of the 19, taken from Arch v5 slides 42 and 43; three types have no stated consumer",
         "Arch v5 slides 42 and 43", "CG-B-ARCH-EVT-9; ASM-B-ARCH-EVT-10"],
        [14, "Event coverage", "30 entries: 26 published, 2 consumed, 1 signal, 1 application event",
         "43 event types on 20 topics: 28 from v4 and 15 that exist only in the Arch v5 catalogue",
         "Arch v5 slides 41, 42 and 43", "CG-B-ARCH-EVT-8; ASM-B-ARCH-EVT-9"],
        [15, "Payload", "References and codes, no personal data",
         "Unchanged; the payload of the 15 new types is fixed by the owning service",
         "v4 rule Payload; Arch v5 slide 22", "CG-B-ARCH-EVT-8; ASM-B-ARCH-EVT-9"],
        [16, "Document version", "Version 4, 16 November 2026, D-RCV-36",
         "Version 5, 22 November 2026, D-RCV-60; the v4 sheets are unchanged",
         "Template and Rules §R8.1 and §R8.2", "None"],
    ]
    table(
        wb, "Realignment changes", "What D-RCV-60 changes in the event and messaging design",
        "One row per change. Source precedence is that of Template and Rules §R3: the Arch v5 catalogue slides win "
        "over the story masters, so a disagreement between v4 and Arch v5 is resolved in favour of Arch v5 and "
        "recorded as a gap and an assumption.",
        ["#", "Item", "v4", "v5", "Basis", "Gap / assumption"], rows, [5, 26, 52, 60, 34, 36],
    )

    wb.save(OUT_DESIGN)
    print("WROTE", OUT_DESIGN, wb.sheetnames)


# ================================================================ workbook B
def build_catalog():
    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    by_topic = {}
    for ev in EVENTS:
        t = event_topic(ev)
        if t.startswith("rwb."):
            by_topic.setdefault(t, []).append(ev)
    order = [s[1] for s in SERVICES]

    read = {}
    for short in order:
        topics = []
        for t, evs in by_topic.items():
            for e in evs:
                if short in e[4] and t not in topics:
                    topics.append(t)
        read[short] = topics
    bff = []
    for t, evs in by_topic.items():
        for e in evs:
            if "gateway-bff" in e[4] and t not in bff:
                bff.append(t)

    readme(
        wb,
        "Recovery Workbench Kafka Topic and Event Catalog v1. Decision D-RCV-60. A new document of the "
        "realignment; it has no earlier version.",
        "The one place where a service finds the name of its topic, of its event types and of its dead-letter "
        "topic, the services that read them, and the envelope and delivery rules that every event follows.",
        "v1, 22 November 2026, D-RCV-60 microservice realignment, " + TOOL,
        "No earlier version exists. The event table it replaces as the contract is Recovery Workbench Event and "
        "Messaging Design v4, 16 November 2026, D-RCV-36, which is carried forward in Event and Messaging "
        "Design v5.",
        [
            "Topics: 20 event topics, one per service plus the shared rwb.decision-record.v1, with owner, wave, "
            "settings, the event types carried and the consumer services.",
            "Retry topics: three per event topic, one per window of 1 min, 10 min and 1 h, 60 in the set, with the "
            "window, the owner and the order of the ladder.",
            "Dead-letter topics: 20, one per event topic, with the alert and the replay path.",
            "Events: 43 event types, with the EV row of the event table where one exists, the event type name, the "
            "topic, the owner, the payload and the consumers.",
            "Not on Kafka: the entries that are not plain topic events (the retired TimerDue, the CaseEvent signal "
            "and the two ACE batch events that are exempt from the transaction rule), and why.",
            "Envelope, Outbox and inbox, Delivery rules: the message format and the delivery behaviour every "
            "producer and consumer implements.",
            "ACLs: the write and read list of every service principal, derived from the producer and consumer "
            "columns of the event catalogue.",
            "Traceability: the decision, the pattern and the slide each part of the catalogue implements.",
        ],
        [
            "100 topics: 20 event topics, 60 retry topics and 20 dead-letter topics.",
            "43 event types: 28 carry an EV row of the v4 event table and 15 exist only in the Architecture v5 "
            "service catalogue.",
            "19 service principals plus gateway-bff; every service writes its own topic and the shared "
            "rwb.decision-record.v1.",
            "12 partitions, replication factor 3, 7-day retention and record key caseId on every event topic.",
        ],
        [
            "Recovery Workbench Architecture v5 Text Extract v1, slides 9, 11, 20, 21, 22, 35, 41, 42, 43 and 44.",
            "Recovery Workbench Event and Messaging Design v4 (16 November 2026, D-RCV-36) and its next version, "
            "Event and Messaging Design v5 (22 November 2026, D-RCV-60).",
            "Recovery Workbench Microservice Ownership Map v1, sheets Services and Events.",
            "Recovery Workbench Temporal and Drools Design Text Extract v1, slides 14 and 15.",
            "RWB-PLT-N002-INF (Kafka topics, retry and dead-letter topics and ACLs) and RWB-PLT-N008-INF (schema "
            "registry with BACKWARD compatibility).",
            "Template and Rules §R4 (naming), §R5.5 DP-09, DP-14 and DP-03 (patterns), §R8.1 and §R8.2 (header and "
            "versioning), §R9 (placeholder).",
            "Candidate gap rows CG-B-ARCH-EVT-1 to CG-B-ARCH-EVT-12 and candidate assumption rows "
            "ASM-B-ARCH-EVT-1 to ASM-B-ARCH-EVT-14 are written by this work package; step D1 renumbers them.",
        ],
    )

    rows = []
    for short in order:
        t = topic_of(short)
        evs = by_topic.get(t, [])
        cons = []
        for e in evs:
            for c in e[4]:
                if c not in cons:
                    cons.append(c)
        rows.append([t, "Event topic", CODE[short], short, WAVE[short], 12, 3, "7 days", "caseId",
                     ", ".join(e[1] for e in evs), union_consumers(evs),
                     "Arch v5 slides 9 and 41; Ownership Map sheet Services"])
    rows.append(["rwb.decision-record.v1", "Shared event topic", "P7", "shared by the 19 services", 0,
                 P6, P6, P6, P6, "DecisionRecorded",
                 union_consumers(by_topic.get("rwb.decision-record.v1", [])),
                 "Arch v5 slides 20 and 42 row 08; Ownership Map sheet Events row EV-08"])
    table(
        wb, "Topics", "Recovery event topics",
        "Settings of an event topic: 12 partitions, replication factor 3, 7-day retention, cleanup policy delete, "
        "record key caseId and CloudEvents 1.0 in binary mode (Arch v5 slide 9). The shared topic carries no "
        "settings of its own in any source (CG-B-ARCH-EVT-6; ASM-B-ARCH-EVT-7).",
        ["Topic", "Kind", "Owner code", "Owner service", "Wave", "Partitions", "Replication", "Retention", "Key",
         "Event types carried", "Consumers", "Basis"],
        rows, [28, 16, 8, 24, 6, 11, 11, 10, 9, 46, 46, 40],
    )

    rows = [
        ["1 min", 20, "1 min after the first failure", "Same as its event topic",
         "Owner of the event topic", "First retry window of a record that a consumer failed."],
        ["10 min", 20, "10 min after the first failure", "Same as its event topic",
         "Owner of the event topic", "Second retry window."],
        ["1 h", 20, "1 h after the first failure", "Same as its event topic",
         "Owner of the event topic", "Third and last retry window; after it the record goes to the dead-letter "
                                     "topic."],
    ]
    table(
        wb, "Retry topics", "Retry topics: three per event topic, 60 in the set",
        "Architecture v5 fixes three retry windows, 1 min, 10 min and 1 h, and RWB-PLT-N002-INF counts three retry "
        "topics per event topic. No source names a retry topic, so the name is left to the platform story and is "
        "not written here (CG-B-ARCH-EVT-4; ASM-B-ARCH-EVT-5); a consumer binds to the retry topics through the "
        "outbox and inbox library and never by name.",
        ["Window", "Topics in the set", "When the record moves", "Partitions", "Owner", "What it is for"],
        rows, [14, 14, 30, 30, 30, 70],
    )
    ws = wb["Retry topics"]
    r = ws.max_row + 2
    ws.cell(r, 1, "Total topics in the set: 20 event topics + 60 retry topics + 20 dead-letter topics = 100 "
                  "(RWB-PLT-N002-INF section 12.9).").font = NOTE_FONT

    rows = []
    for short in order:
        t = topic_of(short)
        rows.append([t + ".dlt", t, CODE[short], "Same as its event topic (12)", P5,
                     "One alert per record; the replay tool is the recovery path",
                     "Arch v5 slides 9 and 22 ('.dlt'); RWB-PLT-N002-INF AC2"])
    rows.append(["rwb.decision-record.v1.dlt", "rwb.decision-record.v1", "P7", "Same as its event topic", P5,
                 "One alert per record; the replay tool is the recovery path",
                 "Arch v5 slides 9 and 22 ('.dlt'); shared topic at CG-B-ARCH-EVT-6"])
    table(
        wb, "Dead-letter topics", "Dead-letter topics: 20, one per event topic",
        "A record that fails the three retry windows goes to the dead-letter topic of its event topic, one alert "
        "is raised and the replay tool puts it back after the cause is fixed (Arch v5 slide 22). The .dlt suffix "
        "is the one the source gives and the name is derived from it (ASM-B-ARCH-EVT-6); replication and "
        "retention are not stated by any source (CG-B-ARCH-EVT-5).",
        ["Dead-letter topic", "Event topic it serves", "Owner code", "Partitions",
         "Replication and retention", "Alert and replay", "Basis"],
        rows, [34, 30, 9, 24, 40, 40, 40],
    )

    rows = []
    for ev in EVENTS:
        name, short = ev[1], ev[2]
        ocode, oname = owner(ev)
        rows.append([
            ev[0] or "new",
            name,
            ce_type(name, short),
            event_topic(ev),
            ocode,
            oname,
            ev[3],
            payload_of(ev),
            consumers_str(ev),
            ev[5],
            ev[6],
        ])
    table(
        wb, "Events", "Event types: 43 on 20 topics",
        "The 28 types that carry an EV row keep the ID, the payload words and the meaning of the v4 event table; "
        "the 15 types with 'new' in the ID column exist only in the Architecture v5 service catalogue and are not "
        "renumbered (ASM-B-ARCH-EVT-14). Owner code and owner service are those of the Microservice Ownership "
        "Map v1.",
        ["EV row", "Event", "Event type (ce_type)", "Topic", "Owner code", "Owner service", "Direction",
         "Payload", "Consumers", "Family", "Basis"],
        rows, [11, 24, 34, 28, 8, 22, 15, 44, 34, 22, 40],
    )

    rows = [
        ["EV-18", "TimerDue", "Retired (Arch v5 slide 42 row 18): the clock is a durable Temporal timer inside "
                              "CaseWorkflow and PLT owns the capability",
         "No producer and no consumer; the rules component of v4 is reached inside the workflow",
         "CG-B-ARCH-EVT-1; ASM-B-ARCH-EVT-2"],
        ["EV-29", "CaseEvent", "A Temporal signal, not a domain event (Arch v5 slide 43 row 29)",
         "The case router in rwb-case signals the workflow with ID case-{caseId}; the signal is not written to the "
         "outbox and no consumer subscribes to it", "Arch v5 slide 43 row 29; Temporal and Drools design slide 14"],
        ["EV-26 and EV-27", "AceDataReady, AceDataLate", "Both are topic events, but neither is written from a "
                                                        "Workbench change: rwb-source-data raises them from the ACE "
                                                        "batch record it reads through recovery.v_ace_batch_status",
         "They stay exempt from the Transactions rule; the read is not a change and writes no outbox row",
         "v4 rule Transactions; Arch v5 slide 43 rows 26 and 27"],
    ]
    table(
        wb, "Not on Kafka", "The entries that are not plain topic events",
        "Three entries need a note because a reader of the event table would otherwise expect a topic and a "
        "producer for them.",
        ["Entry", "Event", "Why it is not a topic event", "What happens instead", "Basis"],
        rows, [16, 26, 66, 56, 40],
    )

    rows = [
        ["Mode", "CloudEvents 1.0, Kafka binding in binary mode: ce_* attributes as headers, JSON body",
         "Arch v5 slides 9 and 22"],
        ["ce_specversion", "1.0", "Arch v5 slide 22"],
        ["ce_id", "The event identity and the inbox key; a redelivery is recognised and ignored",
         "Arch v5 slide 22; CG-B-ARCH-EVT-12; ASM-B-ARCH-EVT-13"],
        ["ce_type", "rwb.<short>.<Event>.v1 of the owning service; rwb.decision.DecisionRecorded.v1 on the shared "
                    "topic", "Template and Rules §R4; ASM-B-ARCH-EVT-14"],
        ["ce_source", P11, "Arch v5 slide 22 names the header only"],
        ["ce_subject", P11, "Arch v5 slide 22 names the header only"],
        ["traceparent", "W3C Trace Context header carried from producer through the relay to every consumer",
         "Arch v5 slides 9 and 22"],
        ["Body", "JSON validated against the registry; IDs, codes and facts only, no personal data",
         "Arch v5 slide 22; v4 rule Payload"],
        ["Kafka record key", "caseId; order is per case", "Arch v5 slide 9"],
        ["Schema version", "In ce_type (.v1) and in the registry subject; the current and the previous version are "
                           "accepted (CG-B-ARCH-EVT-10; ASM-B-ARCH-EVT-11)", "Arch v5 slide 22; v4 rule Versioning"],
        ["Idempotency key", "ce_id (CG-B-ARCH-EVT-12; ASM-B-ARCH-EVT-13)", "Arch v5 slide 22"],
    ]
    table(wb, "Envelope", "CloudEvents 1.0 envelope of every event",
          "Architecture v5 fixes the mode, the headers, the trace header and the key; it does not give a value "
          "form for ce_source or ce_subject.",
          ["Item", "Value", "Basis"], rows, [22, 100, 44])

    rows = [
        ["outbox_event", "PLT; created in every service schema rwb_*",
         "The event row written with the state change of the producer",
         "Written in the same transaction as the change; the relay publishes it and marks it sent",
         "Arch v5 slide 22; DP-09; RWB-PLT-TE006"],
        ["outbox_delivery", "PLT; created in every service schema",
         "Delivery attempt and retry state of an outbox row",
         "One row per attempt; a broker failure leaves the event in the outbox",
         "Arch v5 slide 22; RWB-PLT-TE006"],
        ["processed_event", "PLT; created in the schema of every consumer", "The inbox of a consumer",
         "ce_id is unique and is written in the same transaction as the consumer's change; a repeat is ignored "
         "and counted (R-UNI-40)", "Arch v5 slide 22; DP-09"],
        ["idempotency_key", "PLT; created in every service schema", "The stored response of a POST, keyed by "
                                                                   "Idempotency-Key",
         "A repeat returns the stored response and does not run the change", "Arch v5 slide 11"],
        ["Outbox relay (JOB-11)", "every service", "The relay inside each service",
         "Every minute it publishes the unsent rows to the service topic and to rwb.decision-record.v1",
         "Arch v5 slide 44"],
        ["Transaction boundary", "the producing service", "One local transaction in the producer's schema",
         "The change, the decision record and the outbox row commit together; EV-26 and EV-27 stay exempt",
         "v4 rule Transactions; Arch v5 slide 22"],
    ]
    table(wb, "Outbox and inbox", "Outbox, inbox and the transaction boundary",
          "The four objects are library objects of the platform and each service creates its own copy in its own "
          "schema; the Ownership Map holds that ruling.",
          ["Object", "Owner", "Where it lives", "What it is for", "Rule", "Basis"], rows,
          [26, 30, 40, 46, 60, 40])

    rows = []
    for short in order:
        rt = read[short]
        rows.append([short, CODE[short], "Workload identity of the service, one principal per service",
                     topic_of(short) + " and rwb.decision-record.v1",
                     ", ".join(rt) if rt else "None",
                     "Arch v5 slides 21 and 35; consumers from slides 42 and 43"])
    rows.append(["gateway-bff", "PLT (edge)", "Workload identity of the edge service",
                 "None (the edge publishes no business event)",
                 ", ".join(bff), "Arch v5 slides 42 and 43 (gateway-bff inbox and banner)"])
    table(
        wb, "ACLs", "Principals and ACLs: who writes and who reads",
        "One principal per service, least privilege, separate from the ACE PII logging topics (Arch v5 slides 21 "
        "and 35). The write list is the service's own topic plus the shared rwb.decision-record.v1, because every "
        "service publishes DecisionRecorded. The read list is the consumer column of the event catalogue and "
        "nothing else. rwb.integration.events.v1 is read by the requesting service of a file run, which the "
        "catalogue does not name, and the two access events are read by all services for their cache; both are "
        "granted per use and not per service here.",
        ["Service", "Code", "Principal", "Write topics", "Read topics", "Basis"],
        rows, [24, 10, 48, 50, 80, 40],
    )

    rows = [
        ["Ordering", "Events of one case are processed in the order they were written, by one sequence per case in "
                     "the outbox; the record key caseId keeps them in one partition."],
        ["Delivery", "At least once; consumers are idempotent."],
        ["Duplicates", "Each consumer records ce_id in processed_event in the same transaction as its own change; "
                       "a repeat is ignored and counted (R-UNI-40)."],
        ["Transactions", "The event is written in the same transaction as the change; no event without the change "
                         "and no change without the event. EV-26 and EV-27 are exempt."],
        ["Payload", "References and codes; no personal data."],
        ["Versioning", "An event carries its schema version; consumers accept the current and the previous "
                       "version; the registry is BACKWARD compatible."],
        ["Failure", "Three retry windows (1 min, 10 min, 1 h), then the dead-letter topic of the event topic, one "
                    "alert and the replay tool."],
        ["Signals", "A Temporal signal goes to one workflow ID; it is not a broadcast, not a domain event and not "
                    "written to the outbox."],
        ["Outbox", "The transaction boundary of the producer; the relay publishes every minute and marks the row "
                   "sent."],
        ["Inbox", "One consumer group per service per topic; the inbox row and the consumer's change commit "
                  "together."],
        ["History", "Temporal history is the workflow's own record; it is not an event bus and no consumer "
                    "subscribes to it."],
        ["Schema registry", "JSON Schema with BACKWARD compatibility; the AsyncAPI 3.0 document of the topic is the "
                            "contract; no subject is named in this version (CG-B-ARCH-EVT-10; ASM-B-ARCH-EVT-11)."],
        ["Platform", "Bank Kafka platform ACE already uses, separate topics and ACLs from PII logging; Azure Event "
                     "Hubs Premium through its Kafka endpoint is the fallback."],
    ]
    table(wb, "Delivery rules", "Delivery rules every producer and consumer implements",
          "The first ten rules are the rules of the v4 event table, carried forward; the last three are the "
          "platform rules of Architecture v5. Where a rule is changed, the row names the gap.",
          ["Rule", "Detail"], rows, [24, 130])

    rows = [
        ["ADR-015", "Kafka with outbox, inbox and CloudEvents", "Topics, Envelope, Outbox and inbox, Delivery rules"],
        ["DP-09", "Outbox and inbox library; CloudEvents", "Topics, Envelope, Outbox and inbox"],
        ["DP-14", "rwb.<short>.events.v1 replaces the legacy topic names", "Topics, events column of every row"],
        ["DP-03", "Local decision record and the shared topic rwb.decision-record.v1", "Topics (shared row), "
                                                                                    "Events (EV-08)"],
        ["Arch v5 slide 9", "Kafka settings, key caseId, retry then .dlt", "Topics, Retry topics, "
                                                                           "Dead-letter topics"],
        ["Arch v5 slide 21", "Bank Kafka platform, separate from PII logging, Event Hubs fallback", "ACLs, "
                                                                                                 "Delivery rules"],
        ["Arch v5 slide 22", "CloudEvents binary mode, outbox, inbox, retry and dead letter", "Envelope, Outbox "
                                                                                             "and inbox, Delivery rules"],
        ["Arch v5 slide 41", "One topic per service and the event types of each service", "Topics, Events"],
        ["Arch v5 slides 42 and 43", "Producer and consumers of every event", "Events, ACLs"],
        ["Arch v5 slide 44", "JOB-11 outbox sender, every minute, every service", "Outbox and inbox"],
        ["RWB-PLT-N002-INF", "The 100 topics, the settings, the ACL model", "Topics, Retry topics, Dead-letter "
                                                                           "topics, ACLs"],
        ["RWB-PLT-N008-INF", "Schema registry with BACKWARD compatibility", "Envelope, Delivery rules"],
        ["Template and Rules §R4", "Event name rwb.<short>.<Event>.v1", "Events, Envelope"],
    ]
    table(wb, "Traceability", "What each part of the catalogue implements",
          "Requirement, contract element and the sheets that carry it; the gap and assumption rows are those of "
          "this work package.",
          ["Requirement", "What it fixes", "Where it is carried"], rows, [26, 60, 70])

    p = wb.properties
    p.creator = "SCB Collections and Recovery"
    p.lastModifiedBy = "SCB Collections and Recovery"
    p.title = "Recovery Workbench Kafka Topic and Event Catalog v1"
    p.subject = "Decision D-RCV-60 microservice realignment"
    p.description = "SCB Collections and Recovery, Henka Group, 22 November 2026."
    p.keywords = "D-RCV-60; Kafka; topics; events; CloudEvents; v1"
    p.category = "Technical architecture"
    p.created = DATE
    p.modified = DATE
    wb.save(OUT_CATALOG)
    print("WROTE", OUT_CATALOG, wb.sheetnames)


if __name__ == "__main__":
    build_design()
    build_catalog()
