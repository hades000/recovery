"""B-BIZ-38 - build Recovery Workbench Users Roles and Permissions v5.xlsx from the v4 copy.

Run after:
  python -I "22 Microservice Realignment/compat/office_write.py" copy
    "02 Business architecture and process/Recovery Workbench Users Roles and Permissions v4.xlsx"
    "02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx"

Never opens the v4 source. Adds to the copy, and edits no existing cell value:
  - "Read me" sheet at position 0: the R8.1 header, the change log row, what changed,
    what did not change, owners, contract stories, open points, counts
  - Roles O..: one new column K, Enforcing services (D-RCV-60), computed from the row's letters
  - Access flow: two new rows (Review 3 = JOB-18, Break-glass 5 = AccessPolicyChanged)
  - Separation of duty: one note row (role_conflict in rwb_access)
  - Single sign-on: one note row (group to role resolved by rwb-access)
  - Systems by role: one note row (ACE data through P1's contract or v_ace_* views)
  - Key: six new rows (column K, two new sheets, tentative releases, access check, version v5)
  - two new sheets at the end: "Authorise contract" and "Area owners"
  - document properties: no person name
"""
from copy import copy
from pathlib import Path

import openpyxl
from openpyxl.styles import Alignment, Font
from openpyxl.utils import get_column_letter

ROOT = Path(__file__).resolve().parents[4]
TARGET = ROOT / "02 Business architecture and process" / "Recovery Workbench Users Roles and Permissions v5.xlsx"

TOOL = "T3 Code / OpenCode / DeepSeek v4.1 Flash"
CHANGE_ROW = "5, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash"
CG = "CG-B-BIZ-38-{}".replace("{}", "")
AS = "ASM-B-BIZ-38-{}".replace("{}", "")


def ph(cg, asm):
    """R9 placeholder string."""
    return f"Not specified in the source documents (CG-B-BIZ-38-{cg}; ASM-B-BIZ-38-{asm})"


def clone(src, dst):
    dst.font = copy(src.font)
    dst.fill = copy(src.fill)
    dst.border = copy(src.border)
    dst.alignment = copy(src.alignment)
    dst.number_format = src.number_format
    dst.protection = copy(src.protection)


# ---------------------------------------------------------------- area to owner
# Every owner from the Microservice Ownership Map v1 (Services, Tables, Endpoints,
# Jobs, Events and Parameters sheets) and Architecture v5 slides 14, 41, 42, 43, 44.
AREAS = {
    # area: (list of (service code, service label), what the owner holds)
    "Case record": ([("P3", "P3 rwb-case")],
                    "recovery_case, case_account, case_party, task, timer (Tables); "
                    "EV-01 CaseCreated, EV-04 CaseTransferred (Events); GET /cases/{id} (Endpoints)"),
    "Queue and allocation": ([("P3", "P3 rwb-case")],
                             "queue, queue_member, assignment, queue_measure (Tables); "
                             "JOB-03 morning allocation, JOB-06 rebalancing (Jobs)"),
    "Treatment and offer": ([("S2", "S2 rwb-treatment")],
                            "treatment (Tables); EV-10 TreatmentApproved (Events); "
                            "TreatmentWorkflow (Workflows and activities)"),
    "Litigation": ([("S4", "S4 rwb-litigation")],
                   "legal_action, hearing (Tables); LitigationWorkflow; JudgmentRecorded and AuctionResult "
                   "(Architecture v5 slide 43, additions row); Partner instruction in the kit (S4)"),
    "Asset and disposal": ([("S5", "S5 rwb-asset")],
                           "asset_sale, listing (Tables); EV-22 AssetTakenOn (Events); "
                           "JOB-19 re-appraisal (Jobs); AssetDisposalWorkflow"),
    "Debt sale": ([("S6", "S6 rwb-debtsale")],
                  "debt_sale_lot, debt_sale_account (Tables); EV-23 LotAwarded (Events); "
                  "DebtSaleWorkflow"),
    "Write-off and posting": ([("S7", "S7 rwb-writeoff")],
                              "write_off (Tables); EV-24 WriteOffApproved (Events); WriteOffWorkflow; "
                              "JOB-16 write-off scan (Jobs)"),
    "Documents": ([("P5", "P5 rwb-document")],
                  "document, document_custody, document_text, signature_request, retention_rule "
                  "(Tables); EV-16 and EV-17 (Events); DocumentIntakeWorkflow; JOB-12 document intake, "
                  "JOB-17 retention (Jobs)"),
    "Rules and parameters": ([("P7", "P7 rwb-decision"), ("P3", "P3 rwb-case")],
                             "rule_package, rule_package_version, rule_row, rule_test_case (P7); "
                             "parameter_catalog, parameter_value (P3; contract RWB-P3-E1042-CON); "
                             "JOB-20 rule promote"),
    "Reference data": ([("P3", "P3 rwb-case")],
                       "reference_row, reference_version, lov_value (Tables); contract RWB-P3-E1043-CON; "
                       "R-PREC default ruling, DP-07"),
    "Decision log": ([("P7", "P7 rwb-decision")],
                     "decision_log_entry, approval (Tables); EV-08 DecisionRecorded on "
                     "rwb.decision-record.v1; JOB-14 hash-chain check"),
    "Partner portal": ([("S9", "S9 rwb-partner")],
                       "partner, partner_instruction, partner_user (Tables); EV-20 InstructionIssued, "
                       "EV-21 PartnerResultSubmitted (Events); InstructionWorkflow"),
    "Reporting": ([("P9", "P9 rwb-reporting")],
                  "measure_definition, measure_snapshot, measure_publish (Tables); JOB-15 reporting "
                  "extract (Jobs)"),
    "Platform administration": ([("P2", "P2 rwb-integration"), ("PLT", "PLT platform library")],
                                "interface_config, outbound_item, job_catalog (P2); feature_flag, "
                                "feature_flag_change (PLT, R-PREC default ruling)"),
}

AREA_TABLE = [
    ("Case record", "P3 rwb-case", "rwb_case", "/api/recovery/case/v1"),
    ("Queue and allocation", "P3 rwb-case", "rwb_case", "/api/recovery/case/v1"),
    ("Treatment and offer", "S2 rwb-treatment", "rwb_treatment", "/api/recovery/treatment/v1"),
    ("Litigation", "S4 rwb-litigation", "rwb_litigation", "/api/recovery/litigation/v1"),
    ("Asset and disposal", "S5 rwb-asset", "rwb_asset", "/api/recovery/asset/v1"),
    ("Debt sale", "S6 rwb-debtsale", "rwb_debtsale", "/api/recovery/debtsale/v1"),
    ("Write-off and posting", "S7 rwb-writeoff", "rwb_writeoff", "/api/recovery/writeoff/v1"),
    ("Documents", "P5 rwb-document", "rwb_document", "/api/recovery/document/v1"),
    ("Rules and parameters", "P7 rwb-decision (rules) + P3 rwb-case (parameters)",
     "rwb_decision; rwb_case", "/api/recovery/decision/v1; /api/recovery/case/v1"),
    ("Reference data", "P3 rwb-case", "rwb_case", "/api/recovery/case/v1"),
    ("Decision log", "P7 rwb-decision", "rwb_decision", "/api/recovery/decision/v1"),
    ("Partner portal", "S9 rwb-partner", "rwb_partner", "/api/recovery/partner/v1"),
    ("Reporting", "P9 rwb-reporting", "rwb_reporting", "/api/recovery/reporting/v1"),
    ("Platform administration", "P2 rwb-integration + PLT platform library", "rwb_integration",
     "/api/recovery/integration/v1"),
]


def permission_rows(wb):
    """Read the Permissions tab as {role: {area: letters}} and the area order."""
    ws = wb["Permissions"]
    areas = [ws.cell(4, c).value for c in range(4, 18)]
    out, counts = {}, {a: 0 for a in areas}
    for r in range(5, 59):
        role = ws.cell(r, 1).value
        row = {}
        for i, a in enumerate(areas):
            v = ws.cell(r, 4 + i).value
            v = "" if v is None else str(v).strip()
            row[a] = v
            if v and v != "-":
                counts[a] += 1
        out[role] = row
    return areas, out, counts


def enforcing(row, role):
    """Column K value: P4 plus the service of each area the role holds a letter in."""
    if role.startswith("PT-LED"):
        return ("No Workbench capability area held: reached by filing and result interfaces, not by a "
                "Workbench login (Roles tab, First release)")
    if role.startswith("CU-"):
        return ("No Workbench capability area held: reached through the bank channels (Roles tab, "
                "First release)")
    labels = []
    for area, letters in row.items():
        if letters and letters != "-":
            for code, label in AREAS[area][0]:
                if code not in [c for c, _ in labels]:
                    labels.append((code, label))
    out = ["P4 rwb-access"] + [label for _code, label in labels]
    return "; ".join(out)


def build_readme(wb):
    ws = wb.create_sheet("Read me", 0)
    ws.column_dimensions["A"].width = 168
    values = [
        ("SCB Collections and Recovery. Henka Group, 22 November 2026.", "h"),
        ("(C) Siam Commercial Bank and Henka Pte Ltd", "h"),
        ("", ""),
        ("Recovery Workbench Users Roles and Permissions v5 (D-RCV-60 microservice realignment)", "t"),
        (f"Tool: {TOOL}. Status: Draft. Supersedes v4 of 15 November 2026.", ""),
        ("Source: Recovery Workbench Users Roles and Permissions v4.xlsx. Every sheet, role row, letter, number "
         "and date of v4 is kept word for word. The realignment adds this sheet, the Authorise contract and Area "
         "owners sheets at the end, one column on the Roles tab, two rows on the Access flow tab and one note row "
         "on each of the Separation of duty, Single sign-on and Systems by role tabs.", ""),
        ("", ""),
        ("Change log", "s"),
        ("Version | Date | Change | Decision | Tool", "b"),
        (f"| 5 | 22 November 2026 | D-RCV-60 microservice realignment | D-RCV-60 | {TOOL} |", "b"),
        ("| 4 | 15 November 2026 | the COLLINS data load actor is removed under D-RCV-35 (U1); SY-RECOVERY added; "
         "supersedes v3 | D-RCV-35 | not named in the source |", "b"),
        (f"Change-log row (Template and Rules R8.1): {CHANGE_ROW}", "b"),
        ("", ""),
        ("What changed in v5", "s"),
        ("1. New sheet Authorise contract: the one access contract of the target architecture. P4 rwb-access "
         "provides POST /authorise, GET /me/permissions, GET /doa-limits and GET /masking-policies; every service "
         "checks the object itself with cached permission data, a 2 s timeout and a circuit breaker (Architecture "
         "v5 slides 14, 35 and 41; Template and Rules DP-08).", "b"),
        ("2. New sheet Area owners: the 14 capability areas of the Permissions tab, each with the service that owns "
         "its data and its enforcement, taken from the Microservice Ownership Map v1 (Tables, Endpoints, Events, "
         "Jobs and Parameters sheets).", "b"),
        ("3. Roles tab: one new column K, Enforcing services (D-RCV-60), computed from the letters the role already "
         "holds on the Permissions tab. No existing cell changes.", "b"),
        ("4. Access flow tab: two rows added. Review step 3 is the six-monthly JOB-18 access review list, a "
         "Temporal Schedule in rwb-access. Break-glass step 5 is AccessPolicyChanged, published so every service "
         "refreshes its cached permissions and DoA limits.", "b"),
        ("5. Separation of duty tab: one note row. The eight pairs are rows in rwb_access.role_conflict, owned by "
         "P4; the grant check and the sign-in check read the same rows.", "b"),
        ("6. Single sign-on tab: one note row. rwb-access resolves each Entra ID group above to a role code at "
         "sign-in through ACE Common group-to-role (Architecture v5 slides 14, 30 and 41).", "b"),
        ("7. Systems by role tab: one note row. ACE and TDR data reaches a role through the contract of P1 "
         "rwb-source-data or the recovery.v_ace_* views, never by a direct table read (DP-05).", "b"),
        ("8. Key tab: six rows added, for column K, the two new sheets, the tentative-release rule, the access "
         "check and version v5.", "b"),
        ("", ""),
        ("What did not change", "s"),
        ("All 54 role rows of the Roles tab, with every role code, name, class, group, unit, description, L1 "
         "process, screen, default scope and first release.", "b"),
        ("The permission matrix: 54 roles against 14 capability areas, every letter of every row. Every approve "
         "right still works within the delegation of authority table.", "b"),
        ("The 8 separation-of-duty pairs, the 15 access-flow rows, the 49 single sign-on rows and the 37 "
         "systems-by-role rows of the bank roles.", "b"),
        ("The Counts tab (blank in v4, kept as it is), the 16 Key rows of v4, the Roles tab note row of 15 "
         "November 2026 and the Key version row v4.", "b"),
        ("No date is added, changed or removed. v4 states no release date. The release labels E1 to E8 are copied "
         "unchanged, and every one of them is tentative (D-RCV-60, U7).", "b"),
        ("No table, column, function, message or rule name of the source is renamed.", "b"),
        ("", ""),
        ("Owners (Microservice Ownership Map v1)", "s"),
        (f"Every owner named in v5 is taken from the Microservice Ownership Map v1 Services, Tables, Endpoints, "
         f"Jobs, Events and Parameters sheets, or from Architecture v5 slides 14, 35, 41, 42, 43 and 44. P4 "
         f"rwb-access owns the roles, permissions, role conflicts, masking, DoA limits and the access log.", "b"),
        ("Where v4 says 'the Workbench', v5 names the service behind it and leaves the v4 sentence in place.", "b"),
        ("", ""),
        ("Contract stories (Template and Rules DP-08, R5.4 and R5.7)", "s"),
        ("RWB-P4-E1037-CON: the rwb-access contract, P4, wave 1, Day 1.", "b"),
        ("RWB-PLT-E1037-CON: the access guard library every service builds against.", "b"),
        ("Every service carries the contract as a C dependency and builds against its fake, so no service waits "
         "for P4 to be built.", "b"),
        ("", ""),
        ("Open points (placeholders of Template and Rules R9)", "s"),
        (f"1. Request and response schema of the four authorise operations: {ph(1, 1)}.", "b"),
        (f"2. Contract name of the sign-in read, /me/permissions or /me/session: {ph(2, 2)}.", "b"),
        (f"3. Cache lifetime and the rule on a failed authorise call: {ph(3, 3)}.", "b"),
        (f"4. DoA limit amounts: {ph(4, 4)}.", "b"),
        (f"5. Masking rules per role, area and field group: {ph(5, 5)}.", "b"),
        (f"6. Partner user to role mapping between S9 and P4: {ph(6, 6)}.", "b"),
        (f"7. Access log table in rwb_access: {ph(7, 7)}.", "b"),
        (f"8. Credential of the six non-human actors: {ph(8, 8)}.", "b"),
        (f"9. Counts tab values: {ph(9, 9)}.", "b"),
        (f"10. Scope values, Own/Team/All/Placed cases against the legacy REGION: {ph(10, 10)}.", "b"),
        (f"11. Approval and status of this document: {ph(11, 11)}.", "b"),
        ("", ""),
        ("Counts of this version", "s"),
        ("Sheets: 11 (the 8 sheets of v4 in the v4 order, plus Read me, Authorise contract and Area owners).", "b"),
        ("Roles: 54, of which 37 bank users, 7 partner users, 4 customer parties and 6 non-human actors "
         "(unchanged).", "b"),
        ("Capability areas: 14 (unchanged). Separation-of-duty pairs: 8 (unchanged). Access-flow rows: 17 (15 "
         "of v4 plus 2).", "b"),
    ]
    r = 1
    for text, kind in values:
        cell = ws.cell(r, 1, text)
        if kind == "h":
            cell.font = Font(bold=False, size=11)
        elif kind == "t":
            cell.font = Font(bold=True, size=14)
        elif kind == "s":
            cell.font = Font(bold=True, size=12)
        elif kind == "b":
            cell.font = Font(bold=False, size=11)
        cell.alignment = Alignment(wrap_text=False, vertical="top")
        r += 1
    ws.sheet_view.showGridLines = True
    return ws


def add_role_column(wb):
    ws = wb["Roles"]
    assert ws.max_row == 58 and ws.max_column == 10, (ws.max_row, ws.max_column)
    head = ws.cell(4, 11, "Enforcing services (D-RCV-60)")
    clone(ws.cell(4, 10), head)
    head.font = Font(bold=True)
    ws.column_dimensions["K"].width = 62
    areas, perms, _counts = permission_rows(wb)
    n = 0
    for r in range(5, 59):
        role = ws.cell(r, 1).value
        cell = ws.cell(r, 11, enforcing(perms[role], role))
        clone(ws.cell(r, 10), cell)
        cell.alignment = Alignment(wrap_text=True, vertical="top")
        n += 1
    ws.auto_filter.ref = "A4:K58"
    return n


def add_flow_rows(wb):
    ws = wb["Access flow"]
    assert ws.max_row == 19, ws.max_row
    rows = [
        ("Review", 3, "rwb-access (P4)",
         "Temporal Schedule JOB-18 (six-monthly) publishes the list of every holder of every role; the role owner "
         "recertifies from it and a holder not recertified is removed",
         "Workbench (rwb-access)"),
        ("Break-glass", 5, "rwb-access (P4)",
         "Publishes AccessPolicyChanged on rwb.access.events.v1 so every service refreshes its cached permissions "
         "and DoA limits; the grant ends when its window ends",
         "Workbench (rwb-access)"),
    ]
    r = 20
    for a, b, c, d, e in rows:
        for col, val in enumerate((a, b, c, d, e), start=1):
            cell = ws.cell(r, col, val)
            clone(ws.cell(19, col), cell)
            if col == 4:
                cell.alignment = Alignment(wrap_text=True, vertical="top")
        r += 1
    ws.auto_filter.ref = "A4:E21"
    return len(rows)


def add_note_rows(wb):
    n = 0
    ws = wb["Separation of duty"]
    for col, val in enumerate(
        ("Note", "Held as data",
         "The pairs above are rows of rwb_access.role_conflict, owned by P4 rwb-access (Ownership Map v1 Tables "
         "sheet). The grant check and the sign-in check read the same rows, and a change publishes "
         "AccessPolicyChanged on rwb.access.events.v1 (D-RCV-60)."), start=1):
        cell = ws.cell(13, col, val)
        clone(ws.cell(12, col), cell)
        cell.alignment = Alignment(wrap_text=True, vertical="top")
    ws.auto_filter.ref = "A4:C13"
    n += 1

    ws = wb["Single sign-on"]
    cell = ws.cell(54, 1,
                   "Note - group to role: rwb-access (P4) resolves each Entra ID group above to a role code at "
                   "sign-in through ACE Common group-to-role (Architecture v5 slides 14, 30 and 41). The group "
                   "names above are kept exactly as they are (D-RCV-60).")
    clone(ws.cell(53, 1), cell)
    cell.alignment = Alignment(wrap_text=False, vertical="top")
    ws.auto_filter.ref = "A4:G54"
    n += 1

    ws = wb["Systems by role"]
    cell = ws.cell(42, 1,
                   "Note - ACE and TDR: in the target architecture a role reaches ACE and TDR data through the "
                   "contract of P1 rwb-source-data or the recovery.v_ace_* views it owns, never by a direct read of "
                   "an ACE table (Architecture v5 slide 41; Template and Rules DP-05; D-RCV-60). The R and R/W "
                   "marks above are kept unchanged.")
    clone(ws.cell(41, 1), cell)
    cell.alignment = Alignment(wrap_text=False, vertical="top")
    ws.auto_filter.ref = "A4:R42"
    n += 1
    return n


def add_key_rows(wb):
    ws = wb["Key"]
    assert ws.max_row == 20, ws.max_row
    rows = [
        ("Column", "Enforcing services (D-RCV-60)",
         "The services that enforce a role's rights: P4 rwb-access for the role, scope, DoA and masking data, plus "
         "the service that owns each capability area the role holds a letter in. Derived from the role's own row of "
         "the Permissions tab and from the Area owners tab; no value of the role row changes."),
        ("Sheet", "Authorise contract",
         "The contract of P4 rwb-access: the operations every service calls, the events, the schedule, the tables, "
         "the fake and the check sequence (D-RCV-60; Template and Rules DP-08)."),
        ("Sheet", "Area owners",
         "The owner of each of the 14 capability areas of the Permissions tab, taken from the Microservice "
         "Ownership Map v1."),
        ("Release", "Tentative",
         "Every release E1 to E8 and every date in this document is tentative (D-RCV-60, U7). v4 states no release "
         "date and none is added or changed."),
        ("Note", "Access check",
         "Role, scope, DoA and masking are held by P4 rwb-access. Each service checks the object itself with cached "
         "permission data, a 2 s timeout and a circuit breaker per downstream (Architecture v5 slides 14, 35 and 41)."),
        ("Version", "v5", "22 November 2026. Supersedes v4"),
    ]
    r = 21
    for a, b, c in rows:
        for col, val in enumerate((a, b, c), start=1):
            cell = ws.cell(r, col, val)
            clone(ws.cell(20, col), cell)
            if col == 3:
                cell.alignment = Alignment(wrap_text=True, vertical="top")
        r += 1
    ws.auto_filter.ref = "A4:C26"
    return len(rows)


def style_row(ws, r, kind, ref_row=None):
    for col in range(1, ws.max_column + 1):
        cell = ws.cell(r, col)
        cell.alignment = Alignment(wrap_text=True, vertical="top")
        cell.font = Font(bold=(kind == "h"), size=11)


def build_authorise(wb):
    ws = wb.create_sheet("Authorise contract")
    widths = {"A": 30, "B": 44, "C": 34, "D": 44, "E": 44, "F": 46}
    for k, v in widths.items():
        ws.column_dimensions[k].width = v
    rows = []

    def line(vals, kind=""):
        rows.append((vals, kind))

    line(["Authorise contract of P4 rwb-access (D-RCV-60)"], "t")
    line(["The one access contract of the target architecture: every service asks rwb-access, then checks the "
          "object itself. Owner P4 rwb-access (Microservice Ownership Map v1 Services, Endpoints and Tables "
          "sheets; Architecture v5 slides 14, 35 and 41). REST base /api/recovery/access/v1; schema rwb_access; "
          "topic rwb.access.events.v1; task queue rwb-access; wave 1. Patterns DP-08 and DP-11 of the Template "
          "and Rules; contract stories RWB-P4-E1037-CON and RWB-PLT-E1037-CON."])
    line([])

    line(["A1. REST operations provided by rwb-access"], "s")
    line(["Operation", "Purpose", "Caller", "Inputs named in a source", "Response", "Note"], "h")
    line(["POST /authorise",
          "Decide one action of one subject on one object, with the scope and the DoA limit applied",
          "every service, through the access guard library (RWB-PLT-E1037-CON)",
          "role, scope and DoA (Architecture v5 slide 14); the object is the record the calling service holds; the "
          f"request body is {ph(1, 1)}",
          f"the decision with the effective scope and the DoA limit; the body is {ph(1, 1)}",
          "cached reference read; 2 s timeout; circuit breaker per downstream (Architecture v5 slide 35); a POST "
          "is not retried"])
    line(["GET /me/permissions",
          "Resolve the signed-in user's roles, each with its scope, masking and DoA limit, at sign-in",
          "gateway-bff; every service",
          f"the subject of the JWT; the exact request body is {ph(1, 1)}",
          f"roles with scope, masking policy, DoA limit and policy version; the body is {ph(1, 1)}",
          f"Architecture v5 slides 14 and 41 name /me/permissions; the API catalogue names GET /me/session for "
          f"the same read, and the resolution of the two names is {ph(2, 2)}"])
    line(["GET /doa-limits",
          "Read the DoA limit of a role for a product and an action",
          "P7 rwb-decision (ApprovalWorkflow DoA lookup); the services with an approval step",
          "role, product group, action and business date are implied by the delegation_limit rows; the parameters "
          f"are {ph(1, 1)}",
          f"the limit in force with its version and effective dates; the amounts are {ph(4, 4)}",
          "delegation_limit is owned by P4 (Ownership Map v1); P7 reads it through this operation (Architecture v5 "
          "slide 14, P7 OUT 'REST Access: DoA limits')"])
    line(["GET /masking-policies",
          "Read the masking rule of a role for an area and a field group",
          "every service, before it renders personal data",
          f"role, area and field group; the parameters are {ph(1, 1)}",
          f"mask type and field list for the role; the rules themselves are {ph(5, 5)}",
          "masking_rule is owned by P4 (Ownership Map v1); a field with no rule is masked (Compliance sets the "
          "values, DL26)"])
    line(["GET /admin/roles",
          "List the role rows and their permission rows",
          "RW-SECADM (role owner); RW-REFADM and RW-AUDIT (read)",
          "filter and page", "role rows",
          "API Specification v4, x-module P4 (Ownership Map v1 Endpoints)"])
    line(["GET /admin/access-log",
          "Query the access log",
          "RW-SECADM; RW-AUDIT; RW-COMPLY",
          "subject, date range, area and outcome",
          "access log rows, with no personal data value",
          f"the log is named by Architecture v5 slides 14 and 41; the table name, columns and retention are "
          f"{ph(7, 7)}"])
    line(["POST /admin/break-glass-grants",
          "Open a break-glass grant naming the incident, area, scope and reason",
          "RW-PLATADM requests it; RW-SECADM approves it",
          "incident, area, scope, reason and window",
          "grant ID and expiry",
          "Access flow tab, Break-glass steps 1 to 4; the grant ends when its window ends"])
    line(["GET /me/session",
          "Read the current session (the API Specification v4 name of the sign-in read)",
          "gateway-bff", "none", "session, roles and expiry",
          f"kept for the v4 catalogue; whether the two names are one operation is {ph(2, 2)}, and "
          f"ASM-B-BIZ-38-2 reads them as one"])
    line([])

    line(["A2. REST operations consumed by rwb-access"], "s")
    line(["Operation", "Provider", "Purpose", "Call type", "On failure", "Note"], "h")
    line(["Sign-in, user JWT and group to role", "ACE Common (ACE team), through gateway-bff",
          "Entra ID sign-in with MFA, and the group membership that resolves to a role code", "REST / OIDC",
          "no token and no session: the request ends at the gateway with 401",
          "Architecture v5 slide 14 (P4 OUT) and slide 30"])
    line(["None other", "-",
          "rwb-access reads no other service; the role, permission, conflict, masking and DoA data it serves is "
          "its own", "-", "-", "Architecture v5 slide 14: events none, the reference-data owner"])
    line([])

    line(["A3. Events published (topic rwb.access.events.v1, CloudEvents)"], "s")
    line(["Event", "Key", "Published when", "Consumers", "Payload", "Note"], "h")
    line(["AccessPolicyChanged", "roleCode",
          "a role, permission, role-conflict, scope or masking row changes, including a break-glass grant",
          "all 19 services (cache refresh); gateway-bff",
          "role code, policy version and the changed areas; no personal data",
          "Architecture v5 slide 43 additions row; no EV number is assigned in the source"])
    line(["DoaLimitChanged", "roleCode + product group",
          "a delegation_limit row changes, or a new DoA rule version is in force (DOA-2026.11 to DOA-2027.01)",
          "P7 rwb-decision (ApprovalWorkflow); the services with an approval step",
          "limit, version and effective dates", "Architecture v5 slide 43 additions row"])
    line([])

    line(["A4. Events consumed"], "s")
    line(["None. rwb-access is the reference-data owner for access, so it consumes no event (Architecture v5 "
          "slide 14: events none)."])
    line([])

    line(["A5. Workflow and schedule"], "s")
    line(["Item", "Type", "When", "Task queue", "Purpose", "Note"], "h")
    line(["JOB-18 access review list", "Temporal Schedule", "six-monthly", "rwb-access",
          "publish the list of every holder of every role for the role owner to recertify (Access flow, Review "
          "steps 1 to 3)", "Architecture v5 slide 44; Ownership Map v1 Jobs"])
    line(["Workflow", "none", "-", "-",
          "no workflow is specified for rwb-access; the authorise call is a synchronous read", "Architecture v5 "
          "slide 14 lists a Schedule only"])
    line([])

    line(["A6. Tables owned (schema rwb_access, owner P4)"], "s")
    line(["Table", "Holds", "Written by", "Read by", "Note"], "h")
    line(["role", "role code, name, class, group, unit, default scope and first release — the Roles tab",
          "a versioned reference load with an approver", "GET /me/permissions, POST /authorise",
          "Ownership Map v1 Tables"])
    line(["permission", "the 54 roles against the 14 capability areas, letters C R U D A or - — the Permissions tab",
          "a versioned reference load with an approver (RW-SECADM)", "POST /authorise", "Ownership Map v1 Tables"])
    line(["role_conflict", "the eight separation-of-duty pairs — the Separation of duty tab",
          "a versioned reference load with an approver", "the grant check and the sign-in check",
          "Ownership Map v1 Tables"])
    line(["masking_rule", "the masking rule per role, area and field group", "a versioned reference load with an "
          "approver (RW-COMPLY, DL26)", "GET /masking-policies", "Ownership Map v1 Tables"])
    line(["delegation_limit", "the DoA limit per role, product and action, with its version and effective dates",
          "a DoA change with an approver; publishes DoaLimitChanged", "GET /doa-limits",
          f"Ownership Map v1 Tables; the amounts are {ph(4, 4)}"])
    line(["access log", "every sign-in, authorise decision, refusal and break-glass action, append-only",
          "the service on every decision", "GET /admin/access-log",
          f"named by Architecture v5 slides 14 and 41; the table name, columns and retention are {ph(7, 7)}"])
    line([])

    line(["A7. Contract fake and the build rule"], "s")
    line(["Fake", "Covers", "Fixtures", "Used by", "Note"], "h")
    line(["rwb-access stub v1",
          "POST /authorise, GET /me/permissions, GET /doa-limits, GET /masking-policies",
          "54 role fixtures taken from the Roles tab; allow and deny per area; unknown role; policy version "
          "mismatch; a 2 s timeout",
          "the contract tests of every service (C dependency on RWB-P4-E1037-CON)",
          "contract first: the fake is generated from the OpenAPI document of the contract story, so no service "
          "waits for P4 to be built (Template and Rules R5.7 rule 2; DP-08)"])
    line([])

    line(["A8. Call-type summary"], "s")
    line(["Call type", "Use in the authorise path", "Rule", "Note"], "h")
    line(["REST", "POST /authorise; GET /me/permissions, /doa-limits, /masking-policies; the four administration "
          "operations of A1",
          "one hop; 2 s timeout; circuit breaker per downstream; GET retry once with jitter; POST not retried",
          "Architecture v5 slide 35 note"])
    line(["Kafka", "AccessPolicyChanged and DoaLimitChanged to every service; audit and PII logs on the ACE PII path",
          "CloudEvents, outbox in the same transaction, key roleCode, BACKWARD schema",
          "Architecture v5 slides 30 and 43"])
    line(["Temporal", "JOB-18 access review list only", "Schedule in rwb-access, namespace rwb-recovery",
          "Architecture v5 slide 44"])
    line(["File", "None", "-", "-"])
    line([])

    line(["A9. Check sequence on every action"], "s")
    line(["Step", "What happens", "Source"], "h")
    line(["1", "Sign-in at gateway-bff with Entra ID and MFA; an idle session ends after 15 minutes",
          "Architecture v5 slides 30 and 35"])
    line(["2", "ACE Common returns the group membership; rwb-access resolves each Entra ID group of the Single "
          "sign-on tab to a role code, one group per role per environment",
          "Architecture v5 slides 14, 30 and 41; Single sign-on tab"])
    line(["3", "The service resolves the subject's roles, scope, DoA limit and masking from rwb-access and caches "
          f"the answer; the cache lifetime is {ph(3, 3)}",
          "Architecture v5 slide 35: cached permission data from rwb-access"])
    line(["4", "The service checks the object itself (OWASP API1 object-level authorisation) against the scope the "
          "answer names: Own, Team, All or Placed cases",
          "Architecture v5 slide 35; Key tab of this document"])
    line(["5", "An approve action is compared with the DoA limit for the role, product and action; above the limit "
          "the action routes to the approver role through ApprovalWorkflow in P7",
          "Architecture v5 slide 14 (P7 IN); Temporal and Drools design, L3 kit Approval template"])
    line(["6", "Personal data is masked by the masking rule before it leaves the service; a field with no rule is "
          "masked", "Architecture v5 slides 35 and 41"])
    line(["7", "The decision, the role code, the policy version, the area and the outcome go to the access log and "
          "to the ACE PII path (Kafka to the SOC)", "Architecture v5 slides 30, 35 and 41"])
    line(["8", "A change of role, permission, scope, masking or DoA publishes AccessPolicyChanged or "
          "DoaLimitChanged; every service refreshes its cache on the event", "Architecture v5 slides 14, 41 and 43"])
    line([])

    line(["A10. Refusal and failure model"], "s")
    line(["Case", "Response", "Message", "Seen by"], "h")
    line(["No token, or a session that has ended", "401", "MSG-P4-001", "the user"])
    line(["The role holds no letter in the area", "403", "MSG-P4-002", "the user"])
    line(["The record is outside the role's scope", "404, and the excluded count is never shown", "MSG-P4-003",
          "the user"])
    line(["An approve action above the DoA limit", "the action is routed to the approver role named for the limit",
          "-", "the user and the approver"])
    line(["rwb-access does not answer inside 2 s, or the circuit is open",
          "the action is refused and logged, which is the fail-closed reading recorded as ASM-B-BIZ-38-3; the "
          "source states the timeout and the breaker but not the outcome (CG-B-BIZ-38-3)", "-",
          "the user and RW-PLATADM"])
    line(["An unknown role code, or a policy version the caller does not hold", "the action is refused and logged",
          "-", "RW-SECADM"])
    line(["Message IDs are those of the access story RWB-E1-037 and are kept unchanged."])
    line([])

    line(["A11. Owner, dependency and wave"], "s")
    line(["Item", "Value"], "h")
    line(["Owner", "P4 rwb-access (Microservice Ownership Map v1 Services sheet; Architecture v5 slides 14, 35 "
          "and 41)"])
    line(["Contract stories", "RWB-P4-E1037-CON for P4 rwb-access; RWB-PLT-E1037-CON for the access guard library "
          "(Template and Rules DP-08)"])
    line(["Consumers", "all 19 services; gateway-bff; the Approval template of the workflow kit in P7"])
    line(["Wave and readiness", "wave 1 (P4, Architecture v5 slide 41); the contract is Day 1 and every consumer "
          "builds against its fake (Template and Rules R5.4 and R5.7)"])
    line(["Non-human actors", f"the six SY roles of the Roles tab are authorised on the same path; their credential "
          f"is {ph(8, 8)} (Architecture v5 slide 35: mTLS, identified both ways)"])
    line(["Partner roles", f"the seven PT roles are held as role rows by P4 while the partner user record is S9 "
          f"rwb-partner; the mapping is {ph(6, 6)} (Ownership Map v1 ruling)"])

    r = 1
    for vals, kind in rows:
        for col, val in enumerate(vals, start=1):
            cell = ws.cell(r, col, val)
            if kind == "t":
                cell.font = Font(bold=True, size=14)
                cell.alignment = Alignment(wrap_text=False, vertical="top")
            elif kind == "s":
                cell.font = Font(bold=True, size=12)
                cell.alignment = Alignment(wrap_text=False, vertical="top")
            elif kind == "h":
                cell.font = Font(bold=True, size=11)
                cell.alignment = Alignment(wrap_text=True, vertical="top")
            else:
                cell.font = Font(bold=False, size=10)
                cell.alignment = Alignment(wrap_text=True, vertical="top")
        r += 1
    ws.freeze_panes = "A3"
    return ws


def build_areas(wb):
    ws = wb.create_sheet("Area owners")
    for k, v in {"A": 30, "B": 40, "C": 22, "D": 34, "E": 78, "F": 16}.items():
        ws.column_dimensions[k].width = v
    _areas, perms, counts = permission_rows(wb)
    ws.cell(1, 1, "Capability areas of the Permissions tab and the service that owns each one (D-RCV-60)").font = \
        Font(bold=True, size=14)
    ws.cell(2, 1, "Every owner is taken from the Microservice Ownership Map v1 (Services, Tables, Endpoints, "
                  "Jobs, Events and Parameters sheets) and Architecture v5 slide 41. The letters of the "
                  "Permissions tab are not changed; this sheet says where each area's data and enforcement live.")
    ws.cell(2, 1).alignment = Alignment(wrap_text=False, vertical="top")
    head = ["Capability area", "Owning service", "Schema", "REST base",
            "What the owner holds (Ownership Map v1)", "Roles with a letter in this area (of 54)"]
    for col, val in enumerate(head, start=1):
        ws.cell(4, col, val).font = Font(bold=True, size=11)
        ws.cell(4, col).alignment = Alignment(wrap_text=True, vertical="top")
    r = 5
    for area, service, schema, base in AREA_TABLE:
        for col, val in enumerate((area, service, schema, base, AREAS[area][1], counts[area]), start=1):
            cell = ws.cell(r, col, val)
            cell.alignment = Alignment(wrap_text=True, vertical="top")
        r += 1
    # the matrix itself is not one of the 14 areas
    for col, val in enumerate((
        "Not an area of the matrix: the role, permission, scope, DoA and masking data itself",
        "P4 rwb-access", "rwb_access", "/api/recovery/access/v1",
        "role, permission, role_conflict, masking_rule, delegation_limit (Tables); POST /authorise, "
        "GET /me/permissions, /doa-limits, /masking-policies (Architecture v5 slide 14); JOB-18 access review",
        "54 (every role is resolved here)"), start=1):
        cell = ws.cell(r, col, val)
        cell.alignment = Alignment(wrap_text=True, vertical="top")
        cell.font = Font(italic=True, size=11)
    r += 2
    ws.cell(r, 1, "Note - partner and customer roles: the seven PT roles and the four CU roles are held as role "
                  "rows by P4, while the partner user record is owned by S9 rwb-partner (Ownership Map v1 "
                  f"ruling) and a customer reaches the Workbench through the bank channels; the mapping of a "
                  f"partner user to role codes is {ph(6, 6)}.").alignment = Alignment(wrap_text=False,
                                                                                   vertical="top")
    r += 1
    ws.cell(r, 1, "Note - derived counts: the last column counts the non-dash letters of each column of the "
                  "Permissions tab, so it is a count of roles, not of rights. It is computed here and no cell of "
                  "the Permissions tab changes.").alignment = Alignment(wrap_text=False, vertical="top")
    ws.auto_filter.ref = f"A4:F{4 + len(AREA_TABLE) + 1}"
    ws.freeze_panes = "B5"
    return ws


def main():
    wb = openpyxl.load_workbook(TARGET)
    n_col = add_role_column(wb)
    n_flow = add_flow_rows(wb)
    n_note = add_note_rows(wb)
    n_key = add_key_rows(wb)
    build_authorise(wb)
    build_areas(wb)
    build_readme(wb)
    p = wb.properties
    p.creator = "Henka Group"
    p.lastModifiedBy = "Henka Group"
    p.title = "Recovery Workbench Users Roles and Permissions v5"
    p.subject = "D-RCV-60 microservice realignment"
    p.description = f"D-RCV-60 microservice realignment. Tool: {TOOL}. Status Draft, 22 November 2026."
    p.keywords = "Recovery Workbench; roles; permissions; rwb-access; D-RCV-60"
    wb.active = 0
    wb.save(TARGET)
    print(f"roles_column={n_col} flow_rows={n_flow} note_rows={n_note} key_rows={n_key} "
          f"sheets={[s.title for s in wb]}")


if __name__ == "__main__":
    main()
