"""Build Recovery Workbench Controls Catalog v4 from the v3 copy. Decision D-RCV-60.
Never edits v3: works only on the copied v4 file.
"""
import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill
from openpyxl.utils import get_column_letter

XLSX = r"10 Policy, controls and compliance\Recovery Workbench Controls Catalog v4.xlsx"
DEC = "D-RCV-60"
TOOL = "T3 Code / OpenCode / DeepSeek v4.1 Flash"
WP = "B-CTRL-32"

NAVY = "FF4E297F"
DARK = "FF262626"
BODY = "FF1F1F1F"
HDR_FILL = PatternFill("solid", fgColor="FFDCD3EB")

SERVICES = {
    "P1": ("rwb-source-data", "Source data", 1),
    "P3": ("rwb-case", "Case and workflow", 1),
    "P4": ("rwb-access", "Access and authority", 1),
    "P5": ("rwb-document", "Document", 1),
    "P6": ("rwb-comms", "Communications", 1),
    "P7": ("rwb-decision", "Decision and rules", 1),
    "P8": ("rwb-payment", "Payment", 2),
    "P9": ("rwb-reporting", "Reporting", 1),
    "S2": ("rwb-treatment", "Treatment and offer", 2),
    "S3": ("rwb-guarantee", "Guarantee", 3),
    "S4": ("rwb-litigation", "Litigation", 3),
    "S5": ("rwb-asset", "Asset", 2),
    "S6": ("rwb-debtsale", "Debt sale", 3),
    "S7": ("rwb-writeoff", "Write-off", 4),
    "S8": ("rwb-deviation", "Deviation", 2),
    "S9": ("rwb-partner", "Partner", 4),
}

# control id -> (owner code, basis)
OWN = {
 "CTL-01": ("P3", "Architecture v5 slide 41 (P3 owns case, CMMN state, queues, tasks); Ownership Map Tables recovery_case, case_account; slide 14 CaseWorkflow; JOB-02 case creation (slide 44). REC-01 to REC-05 and reconciliation_result are P1 rwb-source-data (slide 41; JOB-04)."),
 "CTL-02": ("P1", "Architecture v5 slide 41 (P1 owns the ACE view contract, freshness and reconciliation); Ownership Map Tables data_contract, data_product_load, sys_objects; JOB-01 ACE ingestion retired to the P1 read path (Ownership Map Jobs, Batch and Scheduling Design v4)."),
 "CTL-03": ("P3", "Architecture v5 slide 41 (P3 owns allocation); Ownership Map Tables assignment, queue_member; slide 42 CaseAllocated; JOB-03 morning allocation (slide 44)."),
 "CTL-04": ("P7", "Architecture v5 slide 41 (P7 owns approvals); Ownership Map Tables approval; slide 14 ApprovalWorkflow and POST /approvals/{approvalId}/decide. The DoA limit it reads is P4 rwb-access (delegation_limit, slide 14 GET /doa-limits)."),
 "CTL-05": ("P4", "Architecture v5 slide 41 (P4 owns Recovery roles as data and scope); Ownership Map Tables role, role_conflict, permission. The separation-of-duty refusal is returned by POST /authorise in P4 (slide 14) and enforced at POST /approvals/{approvalId}/decide in P7."),
 "CTL-06": ("P7", "Architecture v5 slide 41 (P7 owns the central decision ledger); Ownership Map Tables decision_log_entry; DP-03 local decision-record library plus rwb.decision-record.v1; ADR-022 local decision record plus central ledger; daily ledger seal to WORM (slide 14)."),
 "CTL-07": ("P7", "Architecture v5 slide 41 (P7 owns approvals and the central decision ledger); Ownership Map Tables decision_log_entry; slide 42 DecisionRecorded to rwb.decision-record.v1; GET /decision-log in P7 (Ownership Map Endpoints)."),
 "CTL-08": ("P7", "Architecture v5 slide 41 (P7 owns the DMN model registry); Ownership Map Tables rule_package, rule_package_version, rule_row; Temporal and Drools design slide 15 (four-eyes, valid-from date, one-call rollback). Reference loads and lists are P3 rwb-case (Ownership Map Endpoints POST /admin/reference-loads, GET /admin/lists/{listCode}); DoA limits are P4 (delegation_limit)."),
 "CTL-09": ("P4", "Architecture v5 slide 41 (P4 owns Recovery roles as data, scope and the access log); slide 14 POST /authorise (role, scope, DoA); Ownership Map Tables permission; GET /admin/access-log in P4."),
 "CTL-10": ("P4", "Architecture v5 slide 41 (P4 owns Recovery roles as data); slide 14 Temporal Schedule access review list (six-monthly); JOB-18 in rwb-access (slide 44); Ownership Map Tables role, permission."),
 "CTL-11": ("P4", "Architecture v5 slide 41 (P4 owns masking policy); Ownership Map Tables masking_rule; slide 14 GET /masking-policies; masking is applied at the edge and in each service through the P4 guard (DP-08)."),
 "CTL-12": ("P5", "Architecture v5 slide 41 (P5 owns metadata, signatures and retention); Ownership Map Tables document, document_type; slide 16 DocumentIntakeWorkflow; POST /documents/{documentId}/versions in P5."),
 "CTL-13": ("P5", "Architecture v5 slide 41 (P5 owns custody); Ownership Map Tables document_custody; JOB-17 retention schedule in rwb-document (slide 44); POST /documents/{documentId}/custody in P5."),
 "CTL-14": ("P6", "Architecture v5 slide 41 (P6 owns notices, templates and merge fields); Ownership Map Tables template, notice; slide 17 NoticeDispatchWorkflow; POST /admin/templates/{templateId}/approve and /withdraw in P6."),
 "CTL-15": ("P6", "Architecture v5 slide 41 (P6 owns proof of delivery); Ownership Map Tables notice; slide 42 NoticeDelivered, consumed by rwb-litigation, rwb-guarantee and rwb-case."),
 "CTL-16": ("P6", "Architecture v5 slide 41 (P6 owns notices and merge fields); slide 17 P6 IN DeviationRaised and DeviationCleared (contact stop); Ownership Map Tables notice. The interaction ledger row it reads is P1 rwb-source-data (interaction, DP-18)."),
 "CTL-17": ("P6", "Architecture v5 slide 41 (P6 owns notices); Ownership Map Tables notice, template; slide 17 POST /cases/{caseId}/messages in P6; consent is checked in P6 before dispatch."),
 "CTL-18": ("P3", "Architecture v5 slide 41 (P3 owns timers); Ownership Map Tables timer; slide 14 CaseWorkflow; slide 43 TimerBreached; GET /cases/{caseId}/timers in P3."),
 "CTL-19": ("S4", "Architecture v5 slide 41 (S4 owns legal actions, hearings, judgments and enforcement); Ownership Map Tables legal_action, hearing; slide 19 LitigationWorkflow; POST /cases/{caseId}/legal-actions in S4."),
 "CTL-20": ("S3", "Architecture v5 slide 41 (S3 owns TCG and insurance claims, guarantor notices and pursuit); Ownership Map Tables guarantee_claim; slide 18 GuaranteeClaimWorkflow; POST /cases/{caseId}/guarantee-claims in S3."),
 "CTL-21": ("S8", "Architecture v5 slide 41 (S8 owns X1-X7 screening, pause, handling and return); Ownership Map Tables deviation; slide 15 DeviationWorkflow; slide 42 DeviationRaised."),
 "CTL-22": ("S8", "Architecture v5 slide 41 (S8 owns X1-X7 screening, pause, handling and return); Ownership Map Tables deviation; slide 15 DeviationWorkflow; slide 42 DeviationRaised and DeviationCleared."),
 "CTL-23": ("S2", "Architecture v5 slide 41 (S2 owns treatments, including settlement and deed-in-lieu agreements); Ownership Map Tables treatment; slide 18 TreatmentWorkflow and POST /treatments/{treatmentId}/submit. The approval it routes to is P7 (slide 18 Decision: child approval)."),
 "CTL-24": ("S2", "Architecture v5 slide 41 (S2 owns treatments and settlement agreements); Ownership Map Tables treatment; slide 18 TreatmentWorkflow; POST /treatments/{treatmentId}/submit in S2."),
 "CTL-25": ("S2", "Architecture v5 slide 41 (S2 owns treatments, contracts and plan timers); Ownership Map Tables treatment; slide 18 TreatmentWorkflow. The booking confirmation it reads is P8 rwb-payment (TreatmentBooked, slide 42)."),
 "CTL-26": ("S2", "Architecture v5 slide 41 (S2 owns treatments and contracts); Ownership Map Tables treatment; slide 18 TreatmentWorkflow. The accounts covered are read through the P3 rwb-case contract (case_account, Ownership Map Tables)."),
 "CTL-27": ("S5", "Architecture v5 slide 41 (S5 owns assets taken on, holding and floor price); JOB-19 re-appraisal schedule in rwb-asset (slide 44); Ownership Map Tables listing. The valuation record itself is S1 rwb-valuation (slide 41; Ownership Map Endpoints POST /assets/{assetKey}/valuations)."),
 "CTL-28": ("S5", "Architecture v5 slide 41 (S5 owns floor price, listings and auction rounds); Ownership Map Tables listing, asset_sale; slide 19 AssetDisposalWorkflow; the approval is P7 (slide 19 Decision: child approval)."),
 "CTL-29": ("S5", "Architecture v5 slide 41 (S5 owns listings); Ownership Map Tables listing, asset_sale; slide 19 AssetDisposalWorkflow; POST /assets/{assetKey}/listings in S5."),
 "CTL-30": ("S5", "Architecture v5 slide 41 (S5 owns assets taken on and holding); Ownership Map Tables asset_sale; slide 43 AssetTakenOn; slide 19 AssetDisposalWorkflow."),
 "CTL-31": ("S6", "Architecture v5 slide 41 (S6 owns lots and the data room); Ownership Map Tables debt_sale_lot; slide 19 DebtSaleWorkflow and POST /debt-sale-lots. The masking rule it applies is P4 rwb-access (masking_rule, DP-08)."),
 "CTL-32": ("S6", "Architecture v5 slide 41 (S6 owns lots, data room and buyer terms); Ownership Map Tables debt_sale_lot; POST /debt-sale-lots/{lotId}/award in S6. Partner users and the partner gateway are S9 rwb-partner (partner_user, slide 17)."),
 "CTL-33": ("S7", "Architecture v5 slide 41 (S7 owns eligibility, committee and posting); Ownership Map Tables write_off; JOB-16 write-off scan schedule in rwb-writeoff (slide 44); POST /write-off-scans in S7; the rule package comes from P7 (DP-04)."),
 "CTL-34": ("S7", "Architecture v5 slide 41 (S7 owns recovery after charge-off); Ownership Map Tables write_off; slide 20 WriteOffWorkflow; POST /write-offs/{writeOffId}/committee-decision in S7."),
 "CTL-35": ("S9", "Architecture v5 slide 41 (S9 owns panel, partner users, instructions, results, fees and scorecards); Ownership Map Tables partner, partner_instruction; slide 17 InstructionWorkflow; POST /cases/{caseId}/instructions in S9."),
 "CTL-36": ("S9", "Architecture v5 slide 41 (S9 owns fees and scorecards); Ownership Map Tables partner_instruction; slide 17 InstructionWorkflow with SLA timers. First in E5 is kept as written; S9 is wave 4 (CG-B-CTRL-32-2; ASM-B-CTRL-32-2)."),
 "CTL-37": ("S9", "Architecture v5 slide 41 (S9 owns panel and partner users); Ownership Map Tables partner, partner_user; slide 17 partner portal through the partner gateway with MFA (R4 edge)."),
 "CTL-38": ("S5", "Architecture v5 slide 41 (S5 owns assets taken on and holding); Ownership Map Tables asset_sale; slide 43 AssetTakenOn; slide 19 AssetDisposalWorkflow."),
 "CTL-39": ("P9", "Architecture v5 slide 41 (P9 owns measures, snapshots and regulatory reports) and slide 15 (all business events as projections). The Ownership Map has no conduct-sample row, so P9 is recorded by derivation (CG-B-CTRL-32-4; ASM-B-CTRL-32-4)."),
 "CTL-40": ("P8", "Architecture v5 slide 41 (P8 owns payment and proceeds matching); Ownership Map Tables proceeds; JOB-07 matchPayments (slide 44); POST /proceeds/{proceedsId}/match in P8."),
 "CTL-41": ("P8", "Architecture v5 slide 41 (P8 owns payment and proceeds matching); Ownership Map Tables proceeds; JOB-07 matchPayments (slide 44); POST /proceeds/{proceedsId}/match in P8."),
 "CTL-42": ("P3", "Architecture v5 slide 41 (P3 owns case and CMMN state); Ownership Map Endpoints POST /cases/{caseId}/legal-hold in P3; slide 14 CaseWorkflow. Access and personal-data policy are P4 rwb-access (masking_rule, permission)."),
 "CTL-43": ("P1", "Architecture v5 slide 41 (P1 owns the ACE view contract); Ownership Map Tables data_contract, data_product_access; slide 9 (only rwb-source-data reads the 30 recovery.v_ace_* views, ADR-010)."),
 "CTL-44": ("P1", "Architecture v5 slide 41 (P1 owns the ACE view contract); Ownership Map Tables sys_objects, sys_fields, sys_field_version, data_contract; slide 9 (the 30 recovery.v_ace_* views, ADR-010)."),
}

READ_ME = [
 ("SCB Collections and Recovery. Henka Group, 22 November 2026.", "title"),
 ("(C) Siam Commercial Bank and Henka Pte Ltd", "sub"),
 ("", ""),
 ("Recovery Workbench Controls Catalog v4. Decision D-RCV-60. Next version of Recovery Workbench Controls Catalog v3.xlsx; every section, ID, number and date of v3 is kept.", "title"),
 ("The 44 control points on the recovery process: what each checks, who performs it, the evidence it produces and how it is tested. The control owner service is added for each control from the Ownership Map v1; no check, type, performer, evidence, test, frequency, rule, obligation, audit finding or first release changes.", "body"),
 ("Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.", "body"),
 ("Status: Draft. This document is issued with no approval recorded (ASM-B-CTRL-32-6).", "body"),
 ("Release: each control states its first release as a business epic (E1 to E8) and no calendar date; the epics are kept unchanged, and every release date of the programme is tentative (Template and Rules R1 U7).", "body"),
 ("", ""),
 ("Change log", "head"),
 ("4, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash", "body"),
 ("v3 (the source of this version; it is not changed by this run).", "body"),
 ("", ""),
 ("What this version holds", "head"),
 ("Controls: 44 controls CTL-01 to CTL-44, unchanged, with two columns added at the right, Owner service and Owner basis.", "body"),
 ("By type: the 8 rows of v3 unchanged: 44 controls, 13 detective and 31 preventive.", "body"),
 ("By release: the 8 rows of v3 unchanged: E1 10, E2 12, E3 7, E4 2, E5 4, E6 4, E7 3, E8 2.", "body"),
 ("By owner service (new): the 16 services that own at least one control, with their delivery wave and control IDs.", "body"),
 ("Realignment changes (new): every change of v4 in one table, with the decision and the basis.", "body"),
 ("", ""),
 ("Counts", "head"),
 ("44 controls by owner service: P1 3, P3 4, P4 4, P5 2, P6 4, P7 4, P8 2, P9 1, S2 4, S3 1, S4 1, S5 5, S6 2, S7 2, S8 2, S9 3.", "body"),
 ("By type, unchanged: Detective Automated 10, Detective Manual 2, Detective Manual with system enforcement 1, Preventive Automated 28, Preventive Automated with officer review 1, Preventive Automated with officer verification 1, Preventive Manual with system enforcement 1.", "body"),
 ("By release, unchanged: E1 10, E2 12, E3 7, E4 2, E5 4, E6 4, E7 3, E8 2.", "body"),
 ("No control is added, retired, renumbered or reworded.", "body"),
 ("", ""),
 ("Sources", "head"),
 ("Recovery Workbench Controls Catalog v3.xlsx, sheets Controls, By type, By release and Key.", "body"),
 ("Recovery Workbench Microservice Ownership Map v1, sheets Services, Tables, Endpoints, Events, Workflows and activities, Jobs and Rulings; _work/msr/plan/ownership.json.", "body"),
 ("Recovery Workbench Architecture v5 Text Extract v1, slides 9, 14 to 20 and 41 to 44.", "body"),
 ("Recovery Workbench Temporal and Drools Design Text Extract v1, slides 15 and 16.", "body"),
 ("Recovery Workbench Microservice Story Template and Rules v1, R1 (U3, U4, U5, U7), R3 (R-PREC and the default rulings), R5.4, R8.1, R8.2 and R9.", "body"),
 ("_work/msr/plan/ids.json: D-RCV-60 and ADR-013 to ADR-023 are the decisions of this run.", "body"),
 ("", ""),
 ("Open points", "head"),
 ("Control owner service is not stated in v3: the sheet gives Performed by as a role or a monolith component. Each control is given one primary owner service from the Ownership Map v1 (CG-B-CTRL-32-1; ASM-B-CTRL-32-1).", "body"),
 ("Controls whose check spans more than one service record the primary owner in column O and the other owner in column P: CTL-01, CTL-04, CTL-08, CTL-27 and CTL-31 (CG-B-CTRL-32-3; ASM-B-CTRL-32-3).", "body"),
 ("CTL-36 first runs in E5 (wave 3) and its owner service S9 rwb-partner is wave 4; First in is kept as written and the conflict is recorded (CG-B-CTRL-32-2; ASM-B-CTRL-32-2).", "body"),
 ("No conduct-sample row exists in the Ownership Map; P9 rwb-reporting is recorded for CTL-39 by derivation (CG-B-CTRL-32-4; ASM-B-CTRL-32-4).", "body"),
 ("Performed by, Evidence and How it is tested keep the v3 naming of monolith components and messages; the owner service records where the check runs in the realigned build (CG-B-CTRL-32-5; ASM-B-CTRL-32-5).", "body"),
 ("The catalog states no calendar release date; the business epic is kept and no date is added (CG-B-CTRL-32-7; ASM-B-CTRL-32-7).", "body"),
 ("Candidate gap rows CG-B-CTRL-32-1 to CG-B-CTRL-32-7 and candidate assumption rows ASM-B-CTRL-32-1 to ASM-B-CTRL-32-7 are written by this work package to _work/msr/gaps and _work/msr/assumptions; step D1 numbers them.", "body"),
]

CHANGES = [
 (1, "Header lines and change log added", "Read me sheet (new, first sheet)",
  "No header lines and no change log in the workbook",
  "Header lines 1 and 2 of Template and Rules R8.1; change-log row naming D-RCV-60 and the tool line",
  "D-RCV-60", "Template and Rules R8.1, R8.2"),
 (2, "Version row added to the Controls sheet", "Controls, row 3",
  "Row 3 blank",
  "Version 4, 22 November 2026, D-RCV-60; 44 controls; owner service added",
  "D-RCV-60", "Template and Rules R8.2"),
 (3, "Control owner service column added", "Controls, column O",
  "No owner service; Performed by gives a role or a system only",
  "One primary owner service per control, taken from the Ownership Map v1",
  "D-RCV-60, ADR-013", "Ownership Map v1 sheets Services, Tables, Endpoints, Events, Workflows and activities, Jobs; Architecture v5 slides 14 to 20 and 41 to 44"),
 (4, "Owner basis column added", "Controls, column P",
  "No basis column",
  "The table, endpoint, event, workflow or job that fixes the owner, and the second owner where the check spans two services",
  "D-RCV-60", "Ownership Map v1; Architecture v5 slides 14 to 20 and 41 to 44"),
 (5, "44 controls kept word for word", "Controls, rows 5 to 48, columns A to N",
  "44 controls CTL-01 to CTL-44",
  "Every ID, L2, process, check, type, how, performer, evidence, test, frequency, rule, obligation, audit finding and first release kept character for character",
  "D-RCV-60", "Template and Rules R8.2 (an existing file is never edited; content is kept)"),
 (6, "By type counts kept", "By type, rows 5 to 12", "8 rows, 44 controls", "Unchanged", "D-RCV-60", "Controls sheet, columns E and F"),
 (7, "By release counts kept", "By release, rows 5 to 12", "8 rows, 44 controls", "Unchanged", "D-RCV-60", "Controls sheet, column N"),
 (8, "By owner service sheet added", "By owner service (new sheet)",
  "No count by service",
  "16 services own at least one control; P2 rwb-integration, S1 rwb-valuation and P10 rwb-agent own none; wave shown per service",
  "D-RCV-60, ADR-013", "Ownership Map v1 sheet Services (wave); Architecture v5 slide 41"),
 (9, "CTL-36 owner service is wave 4 while its first release is E5", "Controls, row of CTL-36",
  "First in E5; no service named",
  "Owner service S9 rwb-partner recorded; First in kept as E5; conflict recorded",
  "D-RCV-60", "Architecture v5 slide 41 (S9 wave 4); Template and Rules R5.6 (EP05 is wave 3); CG-B-CTRL-32-2"),
 (10, "CTL-39 owner service derived", "Controls, row of CTL-39",
  "Performed by: conduct and QA officer; no service",
  "P9 rwb-reporting recorded by derivation; the Ownership Map has no conduct-sample row",
  "D-RCV-60", "Architecture v5 slides 15 and 41; CG-B-CTRL-32-4"),
]

BY_OWNER_NOTE = ("P2 rwb-integration (wave 1), S1 rwb-valuation (wave 3) and P10 rwb-agent (wave 1) own no control point "
                 "in this catalog. S1 owns the valuation record that CTL-27 checks and S5 rwb-asset owns the control "
                 "(Controls column P).")


def head_style(c):
    c.font = Font(bold=True, name="Aptos", size=10, color=NAVY)
    c.fill = HDR_FILL
    c.alignment = Alignment(wrap_text=True, vertical="top")


def body_style(c, bold=False):
    c.font = Font(bold=bold, name="Aptos", size=10, color=BODY)
    c.alignment = Alignment(wrap_text=True, vertical="top")


wb = openpyxl.load_workbook(XLSX)
ws = wb["Controls"]

# --- Controls sheet: version row 3, two new columns ---------------------------------
ws["A3"] = ("Version 4, 22 November 2026. D-RCV-60. 44 controls, unchanged; the control owner service is added "
            "from the Ownership Map v1 in columns O and P.")
ws["A3"].font = Font(name="Aptos", size=9, color=DARK)

ws["O4"] = "Owner service"
ws["P4"] = "Owner basis"
head_style(ws["O4"]); head_style(ws["P4"])

seen = set()
for row in range(5, ws.max_row + 1):
    cid = ws.cell(row=row, column=1).value
    if not cid:
        continue
    code, basis = OWN[cid]
    seen.add(cid)
    name = SERVICES[code][0]
    oc = ws.cell(row=row, column=15, value=f"{code} {name}")
    bc = ws.cell(row=row, column=16, value=basis)
    body_style(oc, bold=True); body_style(bc)

missing = [k for k in OWN if k not in seen]
assert not missing, missing
assert len(seen) == 44, len(seen)

ws.column_dimensions["O"].width = 22
ws.column_dimensions["P"].width = 64

# row height: keep the v3 height, grow only where the new basis needs more lines
import math
for row in range(5, ws.max_row + 1):
    basis = ws.cell(row=row, column=16).value or ""
    need = math.ceil(len(basis) / 62) * 13.6 + 4
    old = ws.row_dimensions[row].height or 15
    ws.row_dimensions[row].height = max(old, round(need, 1))

# --- Read me sheet, first ----------------------------------------------------------
rm = wb.create_sheet("Read me", 0)
rm.column_dimensions["A"].width = 150
for i, (text, kind) in enumerate(READ_ME, start=1):
    c = rm.cell(row=i, column=1, value=text if text else None)
    if kind == "title":
        c.font = Font(bold=True, name="Aptos", size=14, color=NAVY)
        c.alignment = Alignment(wrap_text=True, vertical="top")
    elif kind == "head":
        c.font = Font(bold=True, name="Aptos", size=10, color=NAVY)
    elif kind == "sub":
        c.font = Font(name="Aptos", size=9, color=DARK)
    elif kind == "body":
        c.font = Font(name="Aptos", size=9, color=DARK)
        c.alignment = Alignment(wrap_text=True, vertical="top")

# --- By owner service (new) --------------------------------------------------------
bo = wb.create_sheet("By owner service")
bo.column_dimensions["A"].width = 8
bo.column_dimensions["B"].width = 22
bo.column_dimensions["C"].width = 26
bo.column_dimensions["D"].width = 8
bo.column_dimensions["E"].width = 10
bo.column_dimensions["F"].width = 60
bo["A1"] = "Control owner service"
bo["A1"].font = Font(bold=True, name="Aptos", size=16, color=NAVY)
bo["A2"] = ("Controls by the service that owns the control point, with the delivery wave of that service. "
            "16 services own at least one control.")
bo["A2"].font = Font(name="Aptos", size=10, color=DARK)
for col, head in zip("ABCDEF", ["Code", "Service", "Service name", "Wave", "Controls", "Control IDs"]):
    c = bo[f"{col}4"]; c.value = head; head_style(c)

counts = {}
for cid, (code, _) in OWN.items():
    counts.setdefault(code, []).append(cid)

order = ["P1", "P3", "P4", "P5", "P6", "P7", "P8", "P9", "S2", "S3", "S4", "S5", "S6", "S7", "S8", "S9"]
r = 5
total = 0
for code in order:
    name, short, wave = SERVICES[code]
    ids = sorted(counts[code])
    total += len(ids)
    for col, val in zip("ABCDEF", [code, name, short, wave, len(ids), ", ".join(ids)]):
        c = bo[f"{col}{r}"]; c.value = val
        body_style(c, bold=(col == "A"))
    r += 1
for col, val in zip("ABCDEF", ["", "Total", "", "", total, "CTL-01 to CTL-44"]):
    c = bo[f"{col}{r}"]; c.value = val if val != "" else None
    body_style(c, bold=True)
assert total == 44, total

bo.cell(row=r + 2, column=1, value=BY_OWNER_NOTE).font = Font(name="Aptos", size=9, color=DARK)
bo.cell(row=r + 2, column=1).alignment = Alignment(wrap_text=True, vertical="top")
bo.freeze_panes = "A5"

# --- Realignment changes (new) -----------------------------------------------------
rc = wb.create_sheet("Realignment changes")
rc["A1"] = "Realignment changes"
rc["A1"].font = Font(bold=True, name="Aptos", size=16, color=NAVY)
rc["A2"] = ("Every change of Controls Catalog v4 against v3, with the decision and the basis. "
            "Nothing else in the catalog changes.")
rc["A2"].font = Font(name="Aptos", size=10, color=DARK)
heads = ["#", "Change", "Where", "v3 (source)", "v4 (this version)", "Decision", "Basis"]
widths = [5, 44, 30, 44, 60, 20, 56]
for i, (h, w) in enumerate(zip(heads, widths), start=1):
    c = rc.cell(row=4, column=i, value=h)
    head_style(c)
    rc.column_dimensions[get_column_letter(i)].width = w
for j, row in enumerate(CHANGES, start=5):
    for i, val in enumerate(row, start=1):
        c = rc.cell(row=j, column=i, value=val)
        body_style(c, bold=(i == 1))
rc.freeze_panes = "A5"

# --- Sheet order, properties, save -------------------------------------------------
order_names = ["Read me", "Controls", "By type", "By release", "By owner service", "Realignment changes", "Key"]
wb._sheets = [wb[n] for n in order_names]

props = wb.properties
props.creator = "Henka Group"
props.lastModifiedBy = "Henka Group"
props.title = "Recovery Workbench Controls Catalog v4"
props.subject = "SCB Collections and Recovery"
props.description = f"Version 4, 22 November 2026. {DEC} microservice realignment. Tool: {TOOL}."
props.keywords = f"{DEC}; controls; ownership"
props.category = "Policy, controls and compliance"

wb.save(XLSX)
print("WROTE", XLSX, "sheets:", wb.sheetnames, "controls:", len(seen))
