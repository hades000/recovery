"""Build Recovery Workbench Regulatory Requirements Map v3 (D-RCV-60).

Copies v2 to v3 first (compat/office_write.py copy), then changes only:
  - new sheet Read me (first) with the R8.1 header lines, metadata and change log
  - Obligations row 3 version line, headers I/J and cells I/J (columns A-H untouched)
  - new sheet By service
  - new sheet Realignment changes
  - two Key rows and the Key autofilter
  - sheet order, workbook properties
"""
import math
from copy import copy
from pathlib import Path

import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

V3 = Path(r"10 Policy, controls and compliance/Recovery Workbench Regulatory Requirements Map v3.xlsx")
HEAD_FILL = PatternFill("solid", fgColor="DCD3EB")
HEAD_FONT = Font(name="Aptos", size=10, bold=True, color="FF4E297F")
BODY = Font(name="Aptos", size=10, color="FF1F1F1F")
TOP = Alignment(wrap_text=True, vertical="top")

# ---------------------------------------------------------------- obligation owners
O = {
    "REG-01": (
        "P6 rwb-comms; P9 rwb-reporting",
        "P6 rwb-comms (wave 1): CTL-16, CTL-17 - contact at permitted times and places, collector identity and no third-party disclosure, on the notice and contact point (Architecture v5 slide 41; Ownership Map tables notice, template). "
        "P9 rwb-reporting (wave 1): CTL-39 - conduct sample over contacts, notices and decisions on the all-business-events projection (ASM-B-CTRL-32-4).",
    ),
    "REG-02": (
        "P9 rwb-reporting",
        "P9 rwb-reporting (wave 1): CTL-39 - the conduct sample that re-performs contacts, notices and decisions (Architecture v5 slide 41: measures, snapshots, regulatory reports; slide 15: all business events as projections). The Ownership Map has no conduct object (CG-B-CTRL-35-6).",
    ),
    "REG-03": (
        "S9 rwb-partner",
        "S9 rwb-partner (wave 4): CTL-35, CTL-37 - panel, partner users, instructions, results, fees and scorecards, through the partner gateway (Architecture v5 slide 41; Ownership Map tables partner, partner_user, partner_instruction; slide 17 InstructionWorkflow).",
    ),
    "REG-04": (
        "P6 rwb-comms",
        "P6 rwb-comms (wave 1): CTL-14 - the fee and charge wording on the notice template, with merge fields and proof of delivery (Architecture v5 slide 41; Ownership Map tables template, notice; slide 17 NoticeDispatchWorkflow).",
    ),
    "REG-05": (
        "S2 rwb-treatment; P7 rwb-decision",
        "S2 rwb-treatment (wave 2): CTL-26 - the restructuring offer made before the account becomes non-performing (Ownership Map table treatment; slide 18 TreatmentWorkflow). "
        "P7 rwb-decision (wave 1): CTL-04 - the approval of the offer and of the route (Ownership Map table approval; slide 14 ApprovalWorkflow).",
    ),
    "REG-06": (
        "P6 rwb-comms",
        "P6 rwb-comms (wave 1): CTL-14, CTL-15 - the notice before the debt is sold and its proof of delivery (Ownership Map tables template, notice; slide 42 NoticeDelivered to rwb-litigation, rwb-guarantee and rwb-case).",
    ),
    "REG-07": (
        "P3 rwb-case",
        "P3 rwb-case (wave 1): CTL-01, CTL-03 - case creation at 90 days past due, allocation, queue placement and rebalancing (Architecture v5 slide 41; Ownership Map tables recovery_case, case_account, assignment, queue_member; JOB-02 and JOB-03).",
    ),
    "REG-08": (
        "P6 rwb-comms; P9 rwb-reporting",
        "P6 rwb-comms (wave 1): CTL-16 - the contact stop and the vulnerable-customer treatment on notices and messages (Ownership Map tables notice, template; slide 42 DeviationRaised and DeviationCleared). "
        "P9 rwb-reporting (wave 1): CTL-39 - conduct sample (ASM-B-CTRL-32-4; CG-B-CTRL-35-6).",
    ),
    "REG-09": (
        "P6 rwb-comms",
        "P6 rwb-comms (wave 1): CTL-16 - complaint and dispute handling and the contact stop that holds recovery until the dispute closes (Ownership Map table notice; slide 42 DeviationRaised and DeviationCleared).",
    ),
    "REG-10": (
        "S2 rwb-treatment",
        "S2 rwb-treatment (wave 2): CTL-23, CTL-25 - relief scheme terms, settlement and deed-in-lieu, booking and the product type of a restructured hire purchase (Ownership Map table treatment; slide 18 TreatmentWorkflow).",
    ),
    "REG-11": (
        "P1 rwb-source-data; S2 rwb-treatment",
        "P1 rwb-source-data (wave 1): CTL-02 - the ACE view contract, data product freshness and reconciliation that stage and class are read from (Ownership Map tables data_contract, data_product_load, reconciliation_result; JOB-04). "
        "S2 rwb-treatment (wave 2): CTL-25 - the product type and re-age on a restructured hire purchase (Ownership Map table treatment).",
    ),
    "REG-12": (
        "S5 rwb-asset",
        "S5 rwb-asset (wave 2): CTL-27 - asset revaluation, floor price and the re-appraisal schedule (Ownership Map table listing; JOB-19). S1 rwb-valuation (wave 3) owns the valuation record the control reads (CG-B-CTRL-32-3).",
    ),
    "REG-13": (
        "S7 rwb-writeoff; P7 rwb-decision",
        "S7 rwb-writeoff (wave 4): CTL-33 - eligibility, committee and posting (Ownership Map table write_off; JOB-16 write-off scan; slide 20 WriteOffWorkflow). "
        "P7 rwb-decision (wave 1): CTL-04 - the approval required before the write-off is posted (Ownership Map table approval).",
    ),
    "REG-14": (
        "S5 rwb-asset",
        "S5 rwb-asset (wave 2): CTL-30 - assets taken on and held, with their holding period and provisioning schedule (Ownership Map table asset_sale; slide 43 AssetTakenOn; slide 19 AssetDisposalWorkflow).",
    ),
    "REG-15": (
        "S5 rwb-asset",
        "S5 rwb-asset (wave 2): CTL-38 - repossessed vehicles and loss on sale as the control evidence (Ownership Map table asset_sale). "
        "The report in the BOT format itself is P9 rwb-reporting (wave 1; Architecture v5 slide 41 regulatory reports, JOB-15 reporting extract), and no control in this row names it (CG-B-CTRL-35-3; ASM-B-CTRL-35-3).",
    ),
    "REG-16": (
        "S3 rwb-guarantee; P6 rwb-comms",
        "S3 rwb-guarantee (wave 3): CTL-20 - TCG and insurance claims, guarantor notices and pursuit (Ownership Map table guarantee_claim; slide 18 GuaranteeClaimWorkflow). "
        "P6 rwb-comms (wave 1): CTL-15 - the guarantor notice and its proof of delivery (Ownership Map table notice).",
    ),
    "REG-17": (
        "P6 rwb-comms",
        "P6 rwb-comms (wave 1): CTL-14, CTL-15 - the mortgagor notice, its wording and its proof of delivery, which starts the notice period (Ownership Map tables template, notice; slide 42 NoticeDelivered).",
    ),
    "REG-18": (
        "P3 rwb-case",
        "P3 rwb-case (wave 1): CTL-18 - the prescription and stage timers and their breach (Ownership Map table timer; slide 14 CaseWorkflow; slide 43 TimerBreached).",
    ),
    "REG-19": (
        "P6 rwb-comms; S4 rwb-litigation",
        "P6 rwb-comms (wave 1): CTL-15 - the proof of service kept with the notice (Ownership Map table notice). "
        "S4 rwb-litigation (wave 3): CTL-19 - legal actions, filing and hearings (Ownership Map tables legal_action, hearing; slide 19 LitigationWorkflow).",
    ),
    "REG-20": (
        "P6 rwb-comms; S5 rwb-asset",
        "P6 rwb-comms (wave 1): CTL-14, CTL-15 - the notice before termination and before the vehicle is sold, with proof of delivery (Ownership Map tables template, notice). "
        "S5 rwb-asset (wave 2): CTL-38 - repossession and sale records (Ownership Map tables asset_sale, listing).",
    ),
    "REG-21": (
        "S8 rwb-deviation",
        "S8 rwb-deviation (wave 2): CTL-22 - bankruptcy and external seizure screening, the pause and the handling route (Ownership Map table deviation; slide 15 DeviationWorkflow; slide 42 DeviationRaised).",
    ),
    "REG-22": (
        "P4 rwb-access",
        "P4 rwb-access (wave 1): CTL-09, CTL-11 - roles as data, scope, the access log and the masking policy (Ownership Map tables permission, role, masking_rule; slide 14 POST /authorise). Controls Catalog v4 also names CTL-43 (P1 rwb-source-data); the Controls cell is unchanged (CG-B-CTRL-35-5).",
    ),
    "REG-23": (
        "P3 rwb-case",
        "P3 rwb-case (wave 1): CTL-42 - the legal hold and the data-subject request route on the case (Ownership Map endpoint POST /cases/{caseId}/legal-hold; slide 14 CaseWorkflow).",
    ),
    "REG-24": (
        "P4 rwb-access; P5 rwb-document",
        "P4 rwb-access (wave 1): CTL-11 - the masking policy and the security measures on personal data (Ownership Map table masking_rule; slide 14 GET /masking-policies). "
        "P5 rwb-document (wave 1): CTL-12 - retention, document metadata and custody (Ownership Map tables document, document_type, retention_rule; JOB-17).",
    ),
    "REG-25": (
        "S9 rwb-partner",
        "S9 rwb-partner (wave 4): CTL-37 - partner and agency oversight and partner users through the partner gateway (Ownership Map tables partner, partner_user; slide 17). The Ownership Map has no incident, breach or continuity object, endpoint, event, workflow or job, so no service is fixed for the breach-notification step itself (CG-B-CTRL-35-4).",
    ),
    "REG-26": (
        "S6 rwb-debtsale",
        "S6 rwb-debtsale (wave 3): CTL-31, CTL-32 - lots, data room, buyer terms and award; the masking rule is read from P4 rwb-access (Ownership Map tables debt_sale_lot, debt_sale_account, masking_rule; slide 19 DebtSaleWorkflow).",
    ),
    "REG-27": (
        "P1 rwb-source-data",
        "P1 rwb-source-data (wave 1): CTL-02 - the ACE data contract, data product load and reconciliation the credit information is built from (Ownership Map tables data_contract, data_product_load, reconciliation_result; JOB-04). "
        "The outbound credit-bureau file is P2 rwb-integration's outbound item (Ownership Map table outbound_item; slide 43 FileDelivered, FileFailed), and no control in this row names it (CG-B-CTRL-35-3; ASM-B-CTRL-35-3).",
    ),
    "REG-28": (
        "S3 rwb-guarantee",
        "S3 rwb-guarantee (wave 3): CTL-20 - the TCG claim, its documents and its deadline (Ownership Map table guarantee_claim; slide 18 GuaranteeClaimWorkflow; slide 19 legal-action handover to S4).",
    ),
    "REG-29": (
        "P7 rwb-decision",
        "P7 rwb-decision (wave 1): CTL-04, CTL-08 - the approval of the route and the rule package in force (Ownership Map tables approval, rule_package, rule_package_version; slide 14 ApprovalWorkflow; JOB-20 rule promote; slide 43 RulePackageInForce).",
    ),
    "REG-30": (
        "P7 rwb-decision; P4 rwb-access",
        "P7 rwb-decision (wave 1): CTL-04 - the approval at the level and within the limit the regulation sets (Ownership Map table approval; slide 14 ApprovalWorkflow). "
        "P4 rwb-access (wave 1): CTL-05 - the delegation of authority table and the separation-of-duty refusal (Ownership Map table delegation_limit; slide 14 POST /authorise).",
    ),
    "REG-31": (
        "S5 rwb-asset",
        "S5 rwb-asset (wave 2): CTL-28, CTL-29 - the disposal route, floor price, listings and auction rounds (Ownership Map tables listing, asset_sale; slide 19 AssetDisposalWorkflow; slide 43 AuctionResult).",
    ),
    "REG-32": (
        "P7 rwb-decision; P4 rwb-access; S9 rwb-partner",
        "P7 rwb-decision (wave 1): CTL-06 - the central decision ledger and its audit trail (Ownership Map table decision_log_entry; DP-03 rwb.decision-record.v1). "
        "P4 rwb-access (wave 1): CTL-09, CTL-10 - access control, the access log and the six-monthly access review (Ownership Map tables permission, role; JOB-18). "
        "S9 rwb-partner (wave 4): CTL-37 - outsourced partner access through the partner gateway (Ownership Map table partner_user). Controls Catalog v4 also names CTL-43 (P1); the Controls cell is unchanged (CG-B-CTRL-35-5).",
    ),
}

SERVICES = {
    "P1": ("rwb-source-data", "Source data", 1), "P2": ("rwb-integration", "Integration", 1),
    "P3": ("rwb-case", "Case and workflow", 1), "P4": ("rwb-access", "Access and authority", 1),
    "P5": ("rwb-document", "Document", 1), "P6": ("rwb-comms", "Communications", 1),
    "P7": ("rwb-decision", "Decision and rules", 1), "P8": ("rwb-payment", "Payment", 2),
    "P9": ("rwb-reporting", "Reporting", 1), "P10": ("rwb-agent", "Agent", 1),
    "S1": ("rwb-valuation", "Valuation and route", 3), "S2": ("rwb-treatment", "Treatment and offer", 2),
    "S3": ("rwb-guarantee", "Guarantee", 3), "S4": ("rwb-litigation", "Litigation", 3),
    "S5": ("rwb-asset", "Asset", 2), "S6": ("rwb-debtsale", "Debt sale", 3),
    "S7": ("rwb-writeoff", "Write-off", 4), "S8": ("rwb-deviation", "Deviation", 2),
    "S9": ("rwb-partner", "Partner", 4),
}

# order of REG ids for the derived sheets
ORDER = [f"REG-{i:02d}" for i in range(1, 33)]


def services_of(reg):
    cell = O[reg][0]
    return [p.split()[0] for p in cell.split(";")]


def ids(lst):
    return ", ".join(lst)


def write_rows(ws, start, rows, widths=None, header=False):
    for r, row in enumerate(rows, start):
        for c, val in enumerate(row, 1):
            cell = ws.cell(row=r, column=c, value=val)
            cell.font = HEAD_FONT if (header and r == start) else BODY
            cell.alignment = TOP
            if header and r == start:
                cell.fill = HEAD_FILL


def main():
    wb = openpyxl.load_workbook(V3)

    obl = wb["Obligations"]
    bys, byp, key = wb["By source"], wb["By process"], wb["Key"]

    # ---------------- sheet Read me
    rm = wb.create_sheet("Read me", 0)
    rm["A1"] = "SCB Collections and Recovery. Henka Group, 22 November 2026."
    rm["A2"] = "(C) Siam Commercial Bank and Henka Pte Ltd"
    rm["A4"] = "Recovery Workbench Regulatory Requirements Map v3"
    rm["A5"] = ("Version 3, 22 November 2026. D-RCV-60 microservice realignment. 32 obligations, unchanged; "
                "the owner service and its basis are added from the Ownership Map v1 in columns I and J of sheet Obligations.")
    rm["A7"] = "Document control"
    meta = [
        ("Document", "Recovery Workbench Regulatory Requirements Map"),
        ("Version", "3"),
        ("Date", "22 November 2026"),
        ("Supersedes", "Recovery Workbench Regulatory Requirements Map v2.xlsx, same folder, not edited"),
        ("Decision", "D-RCV-60 microservice realignment"),
        ("Tool", "T3 Code / OpenCode / DeepSeek v4.1 Flash"),
        ("Status", "Draft"),
        ("Scope of this version",
         "Regulation to service only. Sheet Obligations keeps columns A to H of version 2 character for character and adds "
         "columns I Owner service and J Service basis. Sheets By source and By process keep every row of version 2. "
         "Sheet Key keeps every row and gains two rows. Sheet By service and sheet Realignment changes are new. "
         "No obligation, ID, number, date, control or business owner is added, removed, renumbered or reworded "
         "(CG-B-CTRL-35-2; ASM-B-CTRL-35-2)."),
        ("Owner service convention",
         "The first service in column I is the service that holds the control evidence for the obligation; the services that "
         "follow are the other owners the Controls cell names, in that order. Every service in column I comes from the controls "
         "in column F, through the Ownership Map v1 and the Controls Catalog v4; the delivery wave of each service is stated in "
         "column J, and no wave column is added (CG-B-CTRL-35-7; ASM-B-CTRL-35-7)."),
        ("Owner column and owner service",
         "Column G Owner keeps the business owner of version 2 (Compliance, Legal, product heads, the write-off committee and so "
         "on). Column I is the service that holds the control evidence. The two are different dimensions and both are kept "
         "(CG-B-CTRL-35-8; ASM-B-CTRL-35-8)."),
        ("Sources read",
         "Recovery Workbench Regulatory Requirements Map v2.xlsx; Recovery Workbench Controls Catalog v4.xlsx (control owner "
         "service); Recovery Workbench Microservice Ownership Map v1.xlsx; Recovery Workbench Architecture v5 Text Extract v1; "
         "Recovery Workbench Temporal and Drools Design Text Extract v1; Recovery Workbench Microservice Story Template and Rules v1."),
        ("Dates",
         "This workbook states no release date. The policy effective date 1 July 2026 in REG-29, REG-31 and in sheet Key is "
         "copied unchanged and is not a release date, so no date is marked (tentative)."),
        ("Approval",
         "No approval of version 2 or of version 3 is recorded in any source of this run; version 3 is issued as Draft "
         "(ASM-B-CTRL-35-1)."),
        ("Notes",
         "The regulation labels are copied character for character, including the Thai regulation codes in REG-30. "
         "The Rule column reference 'Retention classes (DL26)' in REG-24 is copied unchanged; its decision log version is not "
         "stated in this workbook."),
    ]
    write_rows(rm, 8, meta)
    for r in range(8, 8 + len(meta)):
        rm.cell(row=r, column=1).font = Font(name="Aptos", size=10, bold=True, color="FF1F1F1F")

    r0 = 8 + len(meta) + 1
    rm.cell(row=r0, column=1, value="Change log").font = Font(name="Aptos", size=12, bold=True, color="FF4E297F")
    write_rows(rm, r0 + 1, [("Version", "Date", "Change", "Tool"),
                            ("2", "Not specified in the source documents (CG-B-CTRL-35-1; ASM-B-CTRL-35-1)",
                             "Baseline version, superseded by version 3",
                             "Not stated in the source workbook (CG-B-CTRL-35-1; ASM-B-CTRL-35-1)"),
                            ("3", "22 November 2026", "D-RCV-60 microservice realignment",
                             "T3 Code / OpenCode / DeepSeek v4.1 Flash")], header=True)
    rm.cell(row=r0 + 5, column=1,
            value="3, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash")
    rm["A1"].font = Font(name="Aptos", size=16, bold=True, color="FF4E297F")
    rm["A2"].font = Font(name="Aptos", size=10, color="FF404040")
    for coord in ("A4", "A7"):
        rm[coord].font = Font(name="Aptos", size=12, bold=True, color="FF4E297F")
    rm["A5"].font = Font(name="Aptos", size=10, color="FF1F1F1F")
    rm.column_dimensions["A"].width = 30
    rm.column_dimensions["B"].width = 118
    rm.column_dimensions["C"].width = 34
    rm.column_dimensions["D"].width = 56
    for r in range(1, r0 + 6):
        rm.cell(row=r, column=2).alignment = TOP

    # ---------------- sheet Obligations
    obl["A3"] = ("Version 3, 22 November 2026. D-RCV-60. 32 obligations, unchanged; the owner service is added from the "
                 "Ownership Map v1 in columns I and J. The first service named is the one that holds the control evidence.")
    obl["A3"].font = Font(name="Aptos", size=10, color="FF404040")
    for col, title in (("I", "Owner service"), ("J", "Service basis")):
        c = obl[f"{col}4"]
        c.value = title
        c._style = copy(obl["H4"]._style)
    for r in range(5, 37):
        reg = obl.cell(row=r, column=1).value
        if reg not in O:
            raise SystemExit(f"unexpected row {r}: {reg!r}")
        for col, val in (("I", O[reg][0]), ("J", O[reg][1])):
            c = obl[f"{col}{r}"]
            c.value = val
            c._style = copy(obl[f"H{r}"]._style)
            c.alignment = Alignment(wrap_text=True, vertical="top")
        lines = max(math.ceil(len(O[reg][1]) / 72), math.ceil(len(O[reg][0]) / 26))
        old = obl.row_dimensions[r].height or 15
        obl.row_dimensions[r].height = min(max(old, 13.4 * lines), 170)
    obl.column_dimensions["I"].width = 26
    obl.column_dimensions["J"].width = 76
    obl.auto_filter.ref = "A4:J36"

    # ---------------- sheet By service
    bs = wb.create_sheet("By service")
    bs["A1"] = "Obligations by owner service"
    bs["A2"] = ("Obligations by the service that satisfies them, with the delivery wave of that service. 15 services satisfy at "
                "least one obligation. The count is the obligations that name the service; the primary count is those where the "
                "service comes first in sheet Obligations column I.")
    rows = [("Code", "Service", "Service name", "Wave", "Obligations", "Obligation IDs", "Primary count", "Primary for")]
    named, prim = {}, {}
    for reg in ORDER:
        svc = services_of(reg)
        prim[svc[0]] = prim.get(svc[0], []) + [reg]
        for s in svc:
            named.setdefault(s, []).append(reg)
    for code in sorted(named, key=lambda x: (x[0], int(x[1:]))):
        name, label, wave = SERVICES[code]
        rows.append((code, name, label, wave, len(named[code]), ids(named[code]),
                     len(prim.get(code, [])), ids(prim.get(code, []))))
    rows.append(("", "Total", "", "", sum(len(v) for v in named.values()), "32 obligations, 44 service pairs",
                 len(ORDER), "REG-01 to REG-32"))
    write_rows(bs, 4, rows, header=True)
    bs["A4"].fill = HEAD_FILL
    note_r = 5 + len(rows)
    bs.cell(row=note_r, column=1,
            value=("P2 rwb-integration, P8 rwb-payment and P10 rwb-agent own no obligation in this map. P8 owns CTL-40 and "
                   "CTL-41, which answer no obligation here; P2 owns the outbound credit-bureau item that REG-27 reports "
                   "through, where the sheet names no control (CG-B-CTRL-35-3). S1 rwb-valuation owns no control and owns the "
                   "valuation record that CTL-27 checks (REG-12). S9 rwb-partner is wave 4 and REG-03, REG-25 and REG-32 "
                   "name it."))
    bs.cell(row=note_r, column=1).alignment = TOP
    for r, h in ((1, 14), (2, 42)):
        bs.row_dimensions[r].height = h
    bs.column_dimensions["A"].width = 8
    bs.column_dimensions["B"].width = 20
    bs.column_dimensions["C"].width = 24
    bs.column_dimensions["D"].width = 7
    bs.column_dimensions["E"].width = 12
    bs.column_dimensions["F"].width = 58
    bs.column_dimensions["G"].width = 10
    bs.column_dimensions["H"].width = 34
    bs.freeze_panes = "B5"
    bs.auto_filter.ref = f"A4:H{3 + len(rows)}"

    # ---------------- sheet Realignment changes
    rc = wb.create_sheet("Realignment changes")
    rc["A1"] = "Realignment changes in version 3"
    rc["A2"] = "What version 3 changes against version 2, and the decision behind each change. Nothing in columns A to H of sheet Obligations, in sheets By source or By process, or in the rows of sheet Key changes."
    crows = [
        ("#", "Where", "Version 2", "Version 3", "Decision", "Basis"),
        (1, "Sheet Read me (new)", "No read-me sheet; the workbook opens on sheet Obligations.",
         "Sheet Read me opens the workbook with the two header lines of Template and Rules R8.1, the document control rows and the change log.",
         "D-RCV-60", "Template and Rules R8.1 and R8.2; the other documents of this run carry the same read-me sheet."),
        (2, "Sheet Obligations, row 3", "Blank.", "Version line: version 3, 22 November 2026, D-RCV-60, 32 obligations unchanged, owner service added in columns I and J.",
         "D-RCV-60", "R8.2 versioning; the row is the version line used in the Controls Catalog v4."),
        (3, "Sheet Obligations, column I (new)", "Not present.", "Owner service: the service or services that satisfy the obligation, primary first.",
         "D-RCV-60", "Ownership Map v1 sheets Services, Tables, Endpoints, Events, Workflows and activities and Jobs; Architecture v5 slide 41; Controls Catalog v4 columns O and P."),
        (4, "Sheet Obligations, column J (new)", "Not present.", "Service basis: the control, table, endpoint, workflow or job that fixes each owner service, with the delivery wave.",
         "D-RCV-60", "Template and Rules R-PREC; the basis is written out so the owner can be checked."),
        (5, "Sheet Obligations, columns A to H", "32 obligations, 56 control references.", "Unchanged, cell for cell, including the 32 IDs, the 18 regulation sources and the policy effective date 1 July 2026.",
         "D-RCV-60", "Every ID, number and date of the source is kept; only the owner service is new."),
        (6, "Sheet Obligations, filter and freeze", "Autofilter A4:H36; freeze at C5.", "Autofilter A4:J36; freeze at C5 unchanged; column widths I and J set and row heights raised where the basis text needs the space.",
         "D-RCV-60", "Layout only; no cell value of columns A to H changes."),
        (7, "Sheet By service (new)", "Not present.", "15 services that satisfy at least one obligation, with the wave, the count, the obligation IDs and the primary obligations; 44 service pairs in total.",
         "D-RCV-60", "Derived from sheet Obligations column I; the same shape as sheet By owner service of the Controls Catalog v4."),
        (8, "Sheet Realignment changes (new)", "Not present.", "This sheet: one row per change, with the decision and the basis.",
         "D-RCV-60", "Template and Rules R8.1 change-log requirement, at sheet level."),
        (9, "Sheet Key", "Four rows: Status three times, Standard once.", "Six rows: the four rows unchanged, plus Owner service and Wave.",
         "D-RCV-60", "Two new terms are used by columns I and J, so they are defined where the other terms are defined."),
        (10, "Sheet order", "Obligations, By source, By process, Key.", "Read me, Obligations, By source, By process, By service, Realignment changes, Key.",
         "D-RCV-60", "The source sheets keep their relative order; the new sheets sit before Key."),
        (11, "Workbook properties", "Creator and last modified by carry a person label.", "Creator and last modified by are Henka Group; title, subject and description carry version 3, D-RCV-60 and the tool line.",
         "D-RCV-60", "Root AGENTS.md rule 4: no names of people anywhere."),
    ]
    write_rows(rc, 4, crows, header=True)
    rc["A4"].fill = HEAD_FILL
    rc.column_dimensions["A"].width = 6
    rc.column_dimensions["B"].width = 30
    rc.column_dimensions["C"].width = 52
    rc.column_dimensions["D"].width = 62
    rc.column_dimensions["E"].width = 12
    rc.column_dimensions["F"].width = 60
    for r in range(5, 5 + len(crows) - 1):
        rc.row_dimensions[r].height = 80
    rc.freeze_panes = "B5"

    # ---------------- sheet Key
    key["A9"] = "Owner service"
    key["B9"] = "Primary first"
    key["C9"] = ("The service that holds the control evidence for an obligation, from the Ownership Map v1 and the Controls "
                 "Catalog v4; the other services the Controls cell names follow in control order.")
    key["A10"] = "Wave"
    key["B10"] = "0 to 4"
    key["C10"] = ("The delivery wave in which a service is created (Ownership Map v1 sheet Services; Template and Rules R5.6); "
                  "wave 1 is Epic 1.")
    for r in (9, 10):
        for col in "ABC":
            key[f"{col}{r}"]._style = copy(key[f"{col}8"]._style)
            key[f"{col}{r}"].alignment = TOP
    key.auto_filter.ref = "A4:C10"

    # ---------------- sheet order and properties
    order = ["Read me", "Obligations", "By source", "By process", "By service", "Realignment changes", "Key"]
    wb._sheets = [wb[n] for n in order]
    wb.active = 0

    pr = wb.properties
    pr.creator = "Henka Group"
    pr.lastModifiedBy = "Henka Group"
    pr.title = "Recovery Workbench Regulatory Requirements Map v3"
    pr.subject = "D-RCV-60 microservice realignment"
    pr.description = ("Version 3, 22 November 2026. D-RCV-60 microservice realignment. "
                      "Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.")
    pr.keywords = "D-RCV-60; regulatory requirements map; microservice realignment"
    pr.category = "Policy, controls and compliance"

    wb.save(V3)
    print("WROTE", V3)


if __name__ == "__main__":
    main()
