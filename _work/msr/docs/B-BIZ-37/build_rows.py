"""Build the row JSON files for the v6 Case and Workflow Model (B-BIZ-37)."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

HEADER = [
    "SCB Collections and Recovery. Henka Group, 22 November 2026.",
    "(C) Siam Commercial Bank and Henka Pte Ltd",
]

readme = [
    [HEADER[0]],
    [HEADER[1]],
    [],
    ["Recovery Workbench Case and Workflow Model v6"],
    [],
    ["Item", "Value"],
    ["Document", "Recovery Workbench Case and Workflow Model v6"],
    ["Version", "6"],
    ["Status", "Draft"],
    ["Decision", "D-RCV-60"],
    ["Source", "02 Business architecture and process/Recovery Workbench Case and Workflow Model v5.xlsx (read-only)"],
    ["Change", "D-RCV-60 microservice realignment: a CaseWorkflow parent with a child workflow per stage. Every sheet, ID, number and date of v5 is kept unchanged."],
    ["Owner services", "Recovery Workbench Microservice Ownership Map v1 (D-RCV-60)"],
    ["New sheets", "Workflow model (v5); Stage ownership (v5); Case file ownership (v5); Change log; Realignment changes"],
    ["Tool", "T3 Code / OpenCode / DeepSeek v4.1 Flash"],
    ["Date", "22 November 2026"],
    [],
    ["How to read", "The v5 sheets are unchanged: Stages, Elements, Case status, Status transitions, Milestones, Tasks, Event listeners, Sentries and Case file. The new sheets show how the same CMMN model runs on the 19 microservices."],
    ["Workflow source", "Architecture v5 Text Extract v1 slides 25 and 41; Temporal and Drools Design Text Extract v1 slide 13; Microservice Ownership Map v1 (Workflows and activities)."],
    ["Namespace", "rwb-recovery"],
]

wm = [
    ["Workflow model v5: CaseWorkflow parent with a child workflow per stage"],
    ["CaseWorkflow (P3 rwb-case, task queue rwb-case, namespace rwb-recovery, workflow ID = case ID) is the parent from entry to closure. Each stage runs as a child workflow in the service that owns it. The parent forwards events from the case router; children use parent close policy ABANDON; Continue-As-New runs at every stage end and at least every 28 days."],
    ["Version 6, 22 November 2026. D-RCV-60. Previous: Version 5, 16 November 2026."],
    [],
    ["Role", "Workflow", "Stage in the v5 model", "Owner (code)", "Service", "Service epic", "Task queue", "Schema", "Tables owned (Ownership Map)", "Pattern", "Note"],
    ["Parent", "CaseWorkflow", "Case, entry to closure; case router", "P3", "rwb-case", "RWB-SVC-P3", "rwb-case", "rwb_case", "recovery_case, case_party, case_account, case_entry_exclusion, assignment, queue, queue_member, queue_measure, task, timer, parameter_catalog, parameter_value, lov_value, reference_row, reference_version", "DP-12", "One per case; workflow ID = case ID; forwards events from the case router to the running child; Continue-As-New at every stage end and at least every 28 days."],
    ["Child (entry)", "RouteDecisionWorkflow", "Route decision D6, before the first stage", "S1", "rwb-valuation", "RWB-SVC-S1", "rwb-valuation", "rwb_valuation", "None in the Ownership Map; the route outcome is recorded as decision_log_entry (P7) (CG-BIZ-37-1; ASM-BIZ-37-1)", "DP-12, DP-04", "Started with ApprovalWorkflow from the kit on rwb-decision (P7) for the route approval."],
    ["Kit child", "ApprovalWorkflow", "Approvals raised by any stage (route approval S1; DoA approvals S2, S3, S5, S6, S7; rule sign-off)", "P7", "rwb-decision", "RWB-SVC-P7", "rwb-decision", "rwb_decision", "approval, decision_log_entry", "DP-12, DP-04", "Kit template; not a route stage. Routed by authority (DoA) from P4."],
    ["Child", "TreatmentWorkflow", "Restructure, TDR; Settlement; Deed in lieu and voluntary surrender", "S2", "rwb-treatment", "RWB-SVC-S2", "rwb-treatment", "rwb_treatment", "treatment", "DP-12, DP-04", "Settlement and deed in lieu are sagas."],
    ["Child", "GuaranteeClaimWorkflow", "Guarantee claim, D6.5 and D6.6", "S3", "rwb-guarantee", "RWB-SVC-S3", "rwb-guarantee", "rwb_guarantee", "guarantee_claim", "DP-12, DP-04", "None."],
    ["Child", "LitigationWorkflow", "Litigation and enforcement, D7", "S4", "rwb-litigation", "RWB-SVC-S4", "rwb-litigation", "rwb_litigation", "legal_action, hearing", "DP-12, DP-04", "Can run for years; Continue-As-New."],
    ["Child", "AssetDisposalWorkflow", "Asset disposal, D8.1 to D8.3", "S5", "rwb-asset", "RWB-SVC-S5", "rwb-asset", "rwb_asset", "asset_sale, listing", "DP-12, DP-04", "Temporal Schedule: re-appraisal monthly (Architecture v5 slide 19)."],
    ["Child", "DebtSaleWorkflow", "Debt sale, D8.4", "S6", "rwb-debtsale", "RWB-SVC-S6", "rwb-debtsale", "rwb_debtsale", "debt_sale_lot, debt_sale_account", "DP-12, DP-04", "Saga, pivot = transfer."],
    ["Child", "WriteOffWorkflow", "Write off and recover after charge-off, D9", "S7", "rwb-writeoff", "RWB-SVC-S7", "rwb-writeoff", "rwb_writeoff", "write_off", "DP-12, DP-04", "Temporal Schedule: scan, 3rd working day (Architecture v5 slide 20)."],
    ["Child (any time)", "DeviationWorkflow", "Deviations X1 to X7", "S8", "rwb-deviation", "RWB-SVC-S8", "rwb-deviation", "rwb_deviation", "deviation", "DP-12, DP-04", "Can start at any time; pauses the stage clock."],
    ["Parent (always on)", "Universal rules, any state", "Universal rules, any state", "P3 and every service", "rwb-case and every service", "RWB-SVC-P3", "rwb-case", "rwb_case", "See the parent row (P3 case tables)", "DP-04", "R-UNI rules apply in every service; there is no universal-rules child workflow."],
]

st = [
    ["Stage ownership v5: one child workflow per stage, owner from the Ownership Map"],
    ["Each row below is one of the 10 stages in the v5 Stages sheet, unchanged. The realignment adds the child workflow, the owner service, the service epic and the task queue, all taken from the Microservice Ownership Map v1 (D-RCV-60)."],
    ["Version 6, 22 November 2026. D-RCV-60. Previous: Version 5, 16 November 2026."],
    [],
    ["Stage (v5 source)", "Kind (v5)", "Workflow (v5)", "Owner (code)", "Service", "Service epic", "Task queue", "Tables owned (Ownership Map)", "Note"],
    ["Restructure, TDR", "Solution stage", "Child: TreatmentWorkflow", "S2", "rwb-treatment", "RWB-SVC-S2", "rwb-treatment", "treatment", "DP-12: child of CaseWorkflow; settlement and deed-in-lieu sagas share the workflow."],
    ["Settlement", "Solution stage", "Child: TreatmentWorkflow", "S2", "rwb-treatment", "RWB-SVC-S2", "rwb-treatment", "treatment", "DP-12: child of CaseWorkflow."],
    ["Deed in lieu and voluntary surrender", "Solution stage", "Child: TreatmentWorkflow", "S2", "rwb-treatment", "RWB-SVC-S2", "rwb-treatment", "treatment", "DP-12: child of CaseWorkflow; the asset hand-off goes to AssetDisposalWorkflow (S5)."],
    ["Litigation and enforcement, D7", "Enforcement stage", "Child: LitigationWorkflow", "S4", "rwb-litigation", "RWB-SVC-S4", "rwb-litigation", "legal_action, hearing", "DP-12: child of CaseWorkflow; can run for years."],
    ["Guarantee claim, D6.5 and D6.6", "Recovery stage", "Child: GuaranteeClaimWorkflow", "S3", "rwb-guarantee", "RWB-SVC-S3", "rwb-guarantee", "guarantee_claim", "DP-12: child of CaseWorkflow."],
    ["Asset disposal, D8.1 to D8.3", "Recovery stage", "Child: AssetDisposalWorkflow", "S5", "rwb-asset", "RWB-SVC-S5", "rwb-asset", "asset_sale, listing", "DP-12: child of CaseWorkflow."],
    ["Debt sale, D8.4", "Recovery stage", "Child: DebtSaleWorkflow", "S6", "rwb-debtsale", "RWB-SVC-S6", "rwb-debtsale", "debt_sale_lot, debt_sale_account", "DP-12: child of CaseWorkflow; saga, pivot = transfer."],
    ["Write off and recover after charge-off, D9", "Closure stage", "Child: WriteOffWorkflow", "S7", "rwb-writeoff", "RWB-SVC-S7", "rwb-writeoff", "write_off", "DP-12: child of CaseWorkflow."],
    ["Deviations X1 to X7", "Exception stage", "Child: DeviationWorkflow", "S8", "rwb-deviation", "RWB-SVC-S8", "rwb-deviation", "deviation", "DP-12: child of CaseWorkflow; can start at any time and pauses the stage clock."],
    ["Universal rules, any state", "Always on", "No separate child; the parent CaseWorkflow", "P3 and every service", "rwb-case and every service", "RWB-SVC-P3", "rwb-case", "See the parent row (P3 case tables)", "DP-04: R-UNI rules apply in every service; the parent holds the case state."],
]

cf = [
    ["Case file ownership v5: the owner service for each case file item"],
    ["Each row below is one of the 12 case file items in the v5 Case file sheet, unchanged. The realignment adds the owner service, the service epic and the table or contract, taken from the Microservice Ownership Map v1 (D-RCV-60)."],
    ["Version 6, 22 November 2026. D-RCV-60. Previous: Version 5, 16 November 2026."],
    [],
    ["Case file item (v5)", "Holds (v5)", "Comes from (v5)", "Owner (code)", "Service", "Service epic", "Tables or contract (Ownership Map)", "Note (v5)"],
    ["Case record", "Identifier, product, customer, state, owner, queue, entry date, prescription date", "P3 case and workflow", "P3", "rwb-case", "RWB-SVC-P3", "recovery_case, case_party, case_account, case_entry_exclusion", "The case service owns the case record and the case API."],
    ["Account and arrears", "Balance, arrears, days past due, classification", "ALS core and GL, through COLLINS", "P1", "rwb-source-data", "RWB-SVC-P1", "account_ext; ACE view contract", "ACE data is read only through rwb-source-data (DP-05)."],
    ["Collections history", "Contact history, promises, the hand-over at 90 days past due", "EFS, through COLLINS", "P1", "rwb-source-data", "RWB-SVC-P1", "interaction, efs_ledger_outcome", "The interaction ledger is P1 by the R-PREC default ruling (DP-18)."],
    ["Customer and party", "The customer, the parties, the other products they hold", "Customer profile received through COLLINS", "P1", "rwb-source-data", "RWB-SVC-P1", "party_ext, contact_point_ext", "The case link stays P3 case_party."],
    ["Collateral", "Collateral records", "CCMS", "Outside the 19 services (CCMS); target owner not specified in the source documents (CG-BIZ-37-2; ASM-BIZ-37-2)", "Outside the 19 services", "None", "None in the Ownership Map", "CCMS is an outside system; data arrives through the P1 source-data contract (DP-05)."],
    ["Valuation", "Appraisal values", "SVAF", "S1", "rwb-valuation", "RWB-SVC-S1", "None in the Ownership Map; valuation_ext stays P1", "rwb-valuation owns valuations and the D6 route decision (Architecture v5 slide 41); the API row POST /assets/{assetId}/valuations is S1."],
    ["Case and ownership", "State, owner, queue, stage clock", "The Workbench", "P3", "rwb-case", "RWB-SVC-P3", "recovery_case, assignment, queue, queue_member, task, timer", "The case service owns state, queues, tasks and timers."],
    ["Partner and placement", "Agency, law firm and partner placements", "The Workbench", "S9", "rwb-partner", "RWB-SVC-S9", "partner, partner_instruction, partner_user", "The partner service owns the panel, partner users and instructions."],
    ["Tracker content", "The Excel and SharePoint trackers, until they are retired", "Excel and SharePoint trackers, until retired", "Retired", "None", "None", "None", "The trackers are retired; no target service."],
    ["Decision history", "Why the system acted: inputs, rule, version, output", "P7 decision center and log", "P7", "rwb-decision", "RWB-SVC-P7", "decision_log_entry, approval", "The decision service owns the central ledger and approvals."],
    ["Interaction ledger", "What happened with the customer: channel, time, who, offer, promise, payment", "P3 case and workflow, P6 communications", "P1", "rwb-source-data", "RWB-SVC-P1", "interaction, efs_ledger_outcome", "The ledger is P1 (DP-18); P3 serves the case timeline API and P6 records the notice."],
    ["Documents", "Every document attached to or generated on the case", "P5 document hub", "P5", "rwb-document", "RWB-SVC-P5", "document, document_type, document_custody, document_text, document_field, document_intake, case_document_check, signature_request, retention_rule", "The document service owns metadata, custody, OCR, signatures and retention."],
]

chg = [
    ["Change log"],
    [],
    ["Version", "Date", "Change", "Decision", "Tool"],
    ["v6", "22 November 2026", "D-RCV-60 microservice realignment", "D-RCV-60", "T3 Code / OpenCode / DeepSeek v4.1 Flash"],
    [],
    ["v6, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash"],
]

rc = [
    ["Recovery Workbench Case and Workflow Model v6 - realignment changes"],
    [],
    ["v6, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash"],
    [],
    ["Area", "Change", "Source"],
    ["Workflow model", "Added the CaseWorkflow parent on P3 rwb-case and one child workflow per stage: RouteDecisionWorkflow (S1), TreatmentWorkflow (S2), GuaranteeClaimWorkflow (S3), LitigationWorkflow (S4), AssetDisposalWorkflow (S5), DebtSaleWorkflow (S6), WriteOffWorkflow (S7), DeviationWorkflow (S8), with ApprovalWorkflow (P7) from the kit.", "Architecture v5 slides 25 and 41; Temporal and Drools Design slide 13; Ownership Map v1 Workflows and activities"],
    ["Stage ownership", "Added the owner service, service epic, task queue and owned tables for each of the 10 CMMN stages, taken from the Ownership Map v1.", "Ownership Map v1 Tables and Services; R4 naming"],
    ["Case file ownership", "Added the owner service, service epic and table or contract for each of the 12 case file items, taken from the Ownership Map v1.", "Ownership Map v1 Tables; DP-05, DP-18"],
    ["Unchanged", "Every sheet, ID, number and date of v5 is kept unchanged: Stages, Elements, Case status, Status transitions, Milestones, Tasks, Event listeners, Sentries and Case file.", "v5 source"],
    ["Universal rules", "No separate child workflow; R-UNI rules apply in every service and the parent CaseWorkflow holds the case state.", "Temporal and Drools Design slide 13 note"],
    ["Retired content", "The Excel and SharePoint trackers in the Case file sheet have no target service; they are retired.", "v5 source Case file; D-RCV-60"],
    ["Open point", "No S1 table is listed in the Ownership Map for valuations; recorded as CG-BIZ-37-1 / ASM-BIZ-37-1.", "Ownership Map v1 Tables"],
    ["Open point", "CCMS collateral has no target service in the Ownership Map; recorded as CG-BIZ-37-2 / ASM-BIZ-37-2.", "v5 source Case file; Ownership Map v1"],
]

for name, rows in [("readme", readme), ("workflow_model", wm), ("stage_ownership", st),
                   ("case_file_ownership", cf), ("change_log", chg), ("realignment_changes", rc)]:
    p = HERE / f"{name}.json"
    p.write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
    print("WROTE", p)
