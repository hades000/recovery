"""Build Recovery Workbench Data Quality and Reconciliation Rules v4 from the copied v3.

The source has three sheets: Load checks (98 retired rows), Reconciliations (REC-01 to
REC-09) and Quality measures (6 measures). Every source cell is kept as it is except
three cells: Reconciliations!B12 and C12 (REC-08 compared a retired decision-log copy)
and Quality measures!B7 (Timeliness named a Workbench read of the ACE batch). New
columns, notes and one new sheet carry the D-RCV-60 per-service reconciliation, with
every owner taken from the Microservice Ownership Map v1.
"""
from copy import copy as _copy
from pathlib import Path

import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

V4 = "06 Data/Recovery Workbench Data Quality and Reconciliation Rules v4.xlsx"
OWN = "22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx"
DEC = "D-RCV-60"
TOOL = "T3 Code / OpenCode / DeepSeek v4.1 Flash"

TITLE_FONT = Font(bold=True, size=16, color="4E297F")
SUB_FONT = Font(size=10, color="404040")
HDR_FONT = Font(bold=True, size=10, color="4E297F")
HDR_FILL = PatternFill("solid", fgColor="DCD3EB")
BODY_FONT = Font(size=10, color="1F1F1F")
NOTE_FONT = Font(italic=True, size=10, color="404040")
WRAP = Alignment(wrap_text=True, vertical="top")
THIN = Side(style="thin", color="BFBFBF")
BOX = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)

# ---------------------------------------------------------------- ownership map
owb = openpyxl.load_workbook(OWN)
osvc = owb["Services"]
service_name = {str(r[0]): str(r[1]) for r in osvc.iter_rows(min_row=2, values_only=True) if r and r[0]}
service_schema = {str(r[0]): str(r[4]) for r in osvc.iter_rows(min_row=2, values_only=True) if r and r[0]}
assert len(service_name) == 19, len(service_name)
otab = owb["Tables"]
table_owner = {str(r[0]): str(r[1]) for r in otab.iter_rows(min_row=2, values_only=True) if r and r[0]}
assert table_owner["reconciliation_result"] == "P1"
assert table_owner["decision_log_entry"] == "P7"
assert table_owner["notice"] == "P6"
print("ownership map read:", len(service_name), "services,", len(table_owner), "tables")

# ---------------------------------------------------------------- changed cells
CHANGED = {
    ("Reconciliations", "B12"):
        "Local decision record of each of the 19 services (rwb.decision-record.v1, via the rwb-decision contract)",
    ("Reconciliations", "C12"):
        "Central decision ledger, rwb-decision (decision_log_entry), with its hash chain",
    ("Quality measures", "B7"):
        "The ACE batch for the business date is complete when rwb-source-data reads it and publishes AceDataReady",
}

# ---------------------------------------------------------------- Reconciliations
REC_COLS = [
    ("Owner (D-RCV-60)", 40),
    ("Per-service reconciliation (D-RCV-60)", 42),
]
REC_OWNER = {
    5: "P3 rwb-case (recovery_case, case_entry_exclusion) · P1 rwb-source-data (case_list_row; runs JOB-04)",
    6: "P3 rwb-case (case_account) · P1 rwb-source-data (case_list_row; runs JOB-04)",
    7: "S2 rwb-treatment (treatment)",
    8: "P8 rwb-payment (proceeds)",
    9: "P6 rwb-comms (notice) · P1 rwb-source-data (reads recovery.v_ace_pod)",
    10: "S7 rwb-writeoff (write_off)",
    11: "S5 rwb-asset (asset_sale, listing)",
    12: "P7 rwb-decision (decision_log_entry)",
    13: "P1 rwb-source-data (ACE view side) · P3 rwb-case, P8 rwb-payment, S5 rwb-asset, S6 rwb-debtsale (the keys they hold)",
}
REC_POINTER = {
    5: "Rows P3 and P1 on the Per-service reconciliation sheet",
    6: "Rows P3 and P1 on the Per-service reconciliation sheet",
    7: "Row S2 on the Per-service reconciliation sheet",
    8: "Row P8 on the Per-service reconciliation sheet",
    9: "Row P6 on the Per-service reconciliation sheet",
    10: "Row S7 on the Per-service reconciliation sheet",
    11: "Row S5 on the Per-service reconciliation sheet",
    12: "Row P7 on the Per-service reconciliation sheet",
    13: "Rows P1, P3, P8, S5 and S6 on the Per-service reconciliation sheet",
}
REC_NOTES = [
    "D-RCV-60 (v4). Each row is answered by the service that holds the Workbench side, and no service reads another service table: "
    "rwb-source-data (P1) keeps the ACE side and the JOB-04 run, and every other side is taken through the owner contract, one hop with a 2 s timeout "
    "(DP-01, DP-05, DP-11; ADR-014; CG-B-DATA-25-1, CG-B-DATA-25-2; ASM-B-DATA-25-1, ASM-B-DATA-25-2).",
    "REC-08 no longer compares a copy: the decision-log copy to the data lake is retired with RWB-E1-014 and the row compares the 19 local decision records "
    "with the central ledger (JOB-13 continuous ingest, JOB-14 hash-chain check at 02:00; CG-B-DATA-25-3; ASM-B-DATA-25-3). "
    "The numbering of REC-05 and REC-09 collides with RWB-E1-011 and is recorded on the Per-service reconciliation sheet (CG-B-DATA-25-6; ASM-B-DATA-25-6).",
]

# ---------------------------------------------------------------- Quality measures
QM_COLS = [("Owner service (D-RCV-60)", 54)]
QM_OWNER = {
    5: "Every service (own schema) · P1 rwb-source-data (ACE view contract)",
    6: "P3 rwb-case (lov_value, reference_row) · P1 rwb-source-data (ACE code lists)",
    7: "P1 rwb-source-data (freshness, AceDataReady)",
    8: "P1 rwb-source-data (reconciliation_result) · every service (its own breaks)",
    9: "P3 rwb-case (recovery_case, case_account)",
    10: "P1 rwb-source-data (ACE view contract) · the owning service of each Workbench table",
}
QM_NOTE = ("D-RCV-60 (v4). Each measure is reported per service on the data quality console: a service measures its own schema, and rwb-source-data measures "
           "the ACE views and the freshness for every service (CG-B-DATA-25-2, CG-B-DATA-25-9; ASM-B-DATA-25-2, ASM-B-DATA-25-9).")

# ---------------------------------------------------------------- Load checks note
LC_NOTES = [
    "D-RCV-60 (v4). The 98 load checks stay retired and unchanged: ACE ingestion (RWB-ACE-001) keeps them, and rwb-source-data (P1) is the only service that reads "
    "the 30 recovery.v_ace_* views, so no other service repeats a load check (DP-05; Architecture v5 slide 41, P1 OUT).",
    "Per-service reconciliation starts after a load has been accepted: see the Per-service reconciliation sheet.",
]

# ---------------------------------------------------------------- per-service sheet
PS_HEAD = ["Service", "Service name", "Schema", "Owns in its schema (Ownership Map, sheet Tables)",
           "Reconciles its own rows, and against what", "Key", "Tolerance", "When",
           "Break and result route", "Pattern", "Basis"]
PH = "Not specified in the source documents (CG-B-DATA-25-5; ASM-B-DATA-25-5)"
PS_ROWS = [
    ["P1", "rwb-source-data", "rwb_source_data",
     "account_ext, case_list_row, contact_point_ext, data_contract, data_product, data_product_access, data_product_load, "
     "dp_guarantee_claim, dp_treatment, efs_ledger_outcome, interaction, lake_copy_watermark, party_ext, reconciliation_result, "
     "sys_field_version, sys_fields, sys_objects, valuation_ext",
     "REC-01 and REC-02 (account count and balance by product against recovery.v_ace_account) over case_list_row and interaction; "
     "the business-key orphan check of REC-09 over its own case_list_row, interaction, party_ext, account_ext, contact_point_ext and valuation_ext keys; "
     "freshness of the 30 recovery.v_ace_* views before AceDataReady",
     "account_key, person_key, contact_key, valuation_key, payment_code; business date; product group",
     "Zero unexplained (REC-01); zero (REC-02); zero orphans for every key it holds (REC-09)",
     "Daily, JOB-04 Reconciliation as an event-started workflow on rwb-source-data, started by AceDataReady",
     "Break list to the data steward, the platform administrator and the team managers; the run writes reconciliation_result in rwb_source_data and answers readers on its own contract",
     "DP-01, DP-05, DP-09, DP-18",
     "Ownership Map v1 sheet Tables (P1); Architecture v5 slide 41 (ACE view contract, freshness, reconciliation) and slide 44 (JOB-04); ADR-014; ASM-B-DATA-25-1"],
    ["P2", "rwb-integration", "rwb_integration",
     "interface_config, job_catalog, outbound_item",
     "every outbound_item it delivers against the file run it records and the FileDelivered or FileFailed event it publishes; the manifest of the reconciliation "
     "and data quality extracts it hands on",
     "interface run id; manifest; business date",
     PH,
     "On each file window: WIN notices at 16:00 and the buyer files per lot",
     "Owning service first: P2 rwb-integration, on its interface-run read for operations; a failed delivery is retried from the outbound item",
     "DP-09, DP-16",
     "Ownership Map v1 sheet Tables (P2); Architecture v5 slide 16 (interface config, file runs, outbound items; FileDelivered, FileFailed) and slide 31 (WIN 16:00, buyer files per lot); ASM-B-DATA-25-1"],
    ["P3", "rwb-case", "rwb_case",
     "assignment, case_account, case_entry_exclusion, case_party, lov_value, parameter_catalog, parameter_value, queue, queue_measure, queue_member, "
     "recovery_case, reference_row, reference_version, task, timer",
     "REC-01: the accounts excluded at entry and the open case accounts it answers on its contract; the business-key orphan check of REC-09 over "
     "case_account, case_party and recovery_case keys; one case per customer per product (Quality measures, Uniqueness)",
     "case id, account_key, person_key, product group; business date",
     "Zero unexplained (REC-01); one case per customer per product, 100 percent (Quality measures, Uniqueness)",
     "Daily after DailyCaseRun (JOB-02 case creation, JOB-03 morning allocation by 07:00)",
     "Owning service first: P3 rwb-case, with the break list to the data steward; the case-list publish status is set on its case-list publish contract",
     "DP-01, DP-06, DP-07, DP-12",
     "Ownership Map v1 sheet Tables (P3); Architecture v5 slides 41 and 44 (JOB-02, JOB-03); Quality measures (Uniqueness); REC-01; ASM-B-DATA-25-1"],
    ["P4", "rwb-access", "rwb_access",
     "delegation_limit, masking_rule, permission, role, role_conflict",
     "each role against its permission set and against the conflicting role pairs; every masking_rule against the data it masks; every delegation_limit against "
     "the role and level it is granted to",
     "role id, permission code, delegation level, table or column masked",
     PH,
     "On every AccessPolicyChanged and DoaLimitChanged on rwb.access.events.v1",
     "Owning service first: P4 rwb-access",
     "DP-08",
     "Ownership Map v1 sheet Tables (P4); Architecture v5 slide 41 (roles as data, scope, masking policy, DoA table) and slide 43 (AccessPolicyChanged, DoaLimitChanged); ASM-B-DATA-25-1"],
    ["P5", "rwb-document", "rwb_document",
     "case_document_check, document, document_checklist_item, document_custody, document_field, document_hub_parameter, document_intake, document_text, "
     "document_type, retention_action, retention_rule, signature_request",
     "each document against its WORM file, its OCR text and extracted fields, its checklist item, its signature request and the retention action due from its retention_rule",
     "document id, case id, retention date",
     PH,
     "On DocumentStored and DocumentFieldsExtracted; retention at the date its retention_rule sets",
     "Owning service first: P5 rwb-document",
     "DP-01, DP-09",
     "Ownership Map v1 sheet Tables (P5); Architecture v5 slide 16 (metadata, custody, OCR text and fields, signatures, retention; DocumentStored, DocumentFieldsExtracted; Azure Blob WORM; Schedule: retention); ASM-B-DATA-25-1"],
    ["P6", "rwb-comms", "rwb_comms",
     "merge_field, notice, template",
     "REC-05 (notice barcodes): the notices it sent to WIN against the barcodes returned in recovery.v_ace_pod, read by rwb-source-data and taken through its "
     "contract; every notice against its template and merge fields",
     "notice id, case id, barcode, person_key",
     "Zero after three days (REC-05)",
     "Daily, after the WIN 16:00 window (JOB-10)",
     "Owning service first: P6 rwb-comms; platform administrator on the REC-05 break",
     "DP-05, DP-09",
     "Ownership Map v1 sheet Tables (P6); Architecture v5 slide 41 (notices, templates, merge fields, proof of delivery) and slide 44 (JOB-10 WIN notices 16:00); REC-05; ASM-B-DATA-25-1"],
    ["P7", "rwb-decision", "rwb_decision",
     "approval, decision_log_entry, rule_package, rule_package_version, rule_row, rule_test_case",
     "REC-08: the local decision records written by all 19 services on rwb.decision-record.v1 against the central decision_log_entry; rule_package_version in "
     "force against the rule registry; the hash chain of the ledger",
     "entry id, case id, previous hash, rule package version",
     "Zero (REC-08); every entry listed",
     "Nightly (REC-08) and the 02:00 hash-chain check (JOB-14)",
     "Owning service first: P7 rwb-decision, with the break list to the data steward",
     "DP-03, DP-09",
     "Ownership Map v1 sheet Tables (P7); Architecture v5 slide 41 (central decision ledger, DMN model registry) and slide 44 (JOB-13 continuous ingest, JOB-14 hash-chain check 02:00); Template and Rules R6 (RWB-E1-014 retired); REC-08; ASM-B-DATA-25-3"],
    ["P8", "rwb-payment", "rwb_payment",
     "proceeds",
     "REC-04: the payments in recovery.v_ace_payment, read by rwb-source-data and taken through its contract, against the proceeds it matched to cases; "
     "ProceedsMatched and TreatmentBooked",
     "payment_code, case id, account_key",
     "Unmatched held on the exception list (REC-04)",
     "Daily, payment matching (JOB-07) and booking confirmation (JOB-08) after AceDataReady",
     "Owning service first: P8 rwb-payment; reconciliation agent and Credit Administration on the REC-04 break",
     "DP-05, DP-09",
     "Ownership Map v1 sheet Tables (P8); Architecture v5 slide 41 (payment and proceeds matching) and slide 44 (JOB-07, JOB-08); REC-04; ASM-B-DATA-25-8"],
    ["P9", "rwb-reporting", "rwb_reporting",
     "measure_definition, measure_publish, measure_snapshot",
     "each measure_snapshot for a business date against its measure_definition and against the case list it reads; measure_publish holds the publish state "
     "of the day; ReportPublished on rwb.reporting.events.v1",
     "measure id, business date, product group",
     "Reconciliation breaks cleared within one day, 100 percent (Quality measures, Accuracy)",
     "Daily at the 01:30 measures Schedule (JOB-15), from its own projections",
     "Owning service first: P9 rwb-reporting, with the break list to the data steward",
     "DP-09, DP-17",
     "Ownership Map v1 sheet Tables (P9); Architecture v5 slide 41 (measures, snapshots, steering dashboard, regulatory reports), slide 44 (JOB-15) and slide 31 (measures at 01:30 from its own projections: no data lake); ADR-018; ASM-B-DATA-25-1"],
    ["P10", "rwb-agent", "rwb_agent",
     "agent_alert, agent_evaluation, agent_evaluation_run, agent_feedback, agent_policy, agent_prompt, agent_run, agent_sample",
     "every agent_run that completed against AgentRunCompleted, its evaluation run and the guardrail alerts it raised; no personal data in a prompt, a run input or a log",
     "agent run id, case id, policy version",
     PH,
     "On AgentRunCompleted",
     "Owning service first: P10 rwb-agent",
     "DP-09, DP-20",
     "Ownership Map v1 sheet Tables (P10); Architecture v5 slide 16 (agent policies, prompts, runs, guardrails, evaluations; AgentRunCompleted) and slide 42 (AgentRunCompleted consumers); ASM-B-DATA-25-1"],
    ["S1", "rwb-valuation", "rwb_valuation",
     "Not specified in the source documents (CG-B-DATA-25-7; ASM-B-DATA-25-7)",
     "the D6 route decision and the route agent output it holds against the case and the RouteDecided event it publishes",
     "case id, route decision, valuation id",
     PH,
     "On RouteDecided",
     "Owning service first: S1 rwb-valuation",
     "DP-09, DP-20",
     "Architecture v5 slide 41 (valuations, the D6 route decision, the route agent output) and slide 43 (RouteDecided); Ownership Map v1 sheet Tables has no S1 row; ASM-B-DATA-25-7"],
    ["S2", "rwb-treatment", "rwb_treatment",
     "treatment",
     "REC-03: the treatments it approved against the plans booked in recovery.v_ace_plan, read by rwb-source-data and taken through its contract; "
     "TreatmentApproved, TreatmentBooked and TreatmentClosed",
     "treatment id, case id, account_key",
     "Zero after two days (REC-03)",
     "Daily, once rwb-treatment is in the environment (wave 2)",
     "Owning service first: S2 rwb-treatment; the officer task on the REC-03 break",
     "DP-05, DP-09",
     "Ownership Map v1 sheet Tables (S2); Architecture v5 slide 41 (treatments, contracts, agreements, plan timers) and slide 42 (TreatmentApproved, TreatmentBooked); REC-03; ASM-B-DATA-25-8"],
    ["S3", "rwb-guarantee", "rwb_guarantee",
     "guarantee_claim",
     "each guarantee_claim against the guarantor notice and the TCG or insurance outcome, and against the ProceedsMatched recovery it may receive",
     "claim id, case id, guarantor; claim amount",
     PH,
     "On the claim event and on NoticeDelivered",
     "Owning service first: S3 rwb-guarantee",
     "DP-09",
     "Ownership Map v1 sheet Tables (S3); Architecture v5 slide 41 (TCG and insurance claims, guarantor notices and pursuit) and slide 43 (GuaranteeClaim*, ProceedsMatched consumers); ASM-B-DATA-25-1"],
    ["S4", "rwb-litigation", "rwb_litigation",
     "hearing, legal_action",
     "each legal_action and hearing against the judgment and the auction ladder result it records, and against the asset sale the auction produces",
     "legal action id, hearing id, case id",
     PH,
     "On JudgmentRecorded and AuctionResult",
     "Owning service first: S4 rwb-litigation",
     "DP-09",
     "Ownership Map v1 sheet Tables (S4); Architecture v5 slide 41 (legal actions, hearings, judgments, enforcement, LED auction ladder) and slide 43 (JudgmentRecorded, AuctionResult); ASM-B-DATA-25-1"],
    ["S5", "rwb-asset", "rwb_asset",
     "asset_sale, listing",
     "REC-07: the assets taken on against the assets in recovery.v_ace_npa_asset, read by rwb-source-data and taken through its contract; each listing and "
     "auction round against AssetSold; the business-key orphan check of REC-09 over its asset_key rows",
     "asset id, asset_key, case id",
     "Zero (REC-07)",
     "Weekly (REC-07); on AssetSold and AuctionResult",
     "Owning service first: S5 rwb-asset; Head of NPA on the REC-07 break",
     "DP-05, DP-09",
     "Ownership Map v1 sheet Tables (S5); Architecture v5 slide 41 (assets taken on, holding, floor price, listings, auction rounds) and slide 43 (AssetTakenOn, AssetSold); REC-07; ASM-B-DATA-25-1"],
    ["S6", "rwb-debtsale", "rwb_debtsale",
     "debt_sale_account, debt_sale_lot",
     "each lot award against the accounts it transferred (LotAwarded, AccountsTransferred) and against the proceeds booked for the lot",
     "lot id, account_key, case id",
     PH,
     "On LotAwarded and AccountsTransferred",
     "Owning service first: S6 rwb-debtsale",
     "DP-09",
     "Ownership Map v1 sheet Tables (S6); Architecture v5 slide 41 (lots, data room, buyer terms, bids, award, transfer) and slide 43 (LotAwarded, AccountsTransferred); ASM-B-DATA-25-1"],
    ["S7", "rwb-writeoff", "rwb_writeoff",
     "write_off",
     "REC-06: the write-offs it approved against the postings in recovery.v_ace_write_off, read by rwb-source-data and taken through its contract; "
     "WriteOffApproved and the committee decision it holds",
     "write-off id, write_off_key, case id, account_key",
     "Zero (REC-06)",
     "Monthly (REC-06)",
     "Owning service first: S7 rwb-writeoff; Credit Administration on the REC-06 break",
     "DP-05, DP-09",
     "Ownership Map v1 sheet Tables (S7); Architecture v5 slide 41 (eligibility, committee, posting, recovery after charge-off) and slide 43 (WriteOffApproved); REC-06; ASM-B-DATA-25-1"],
    ["S8", "rwb-deviation", "rwb_deviation",
     "deviation",
     "each deviation it raised against its screening result and its clearance (DeviationRaised, DeviationCleared); the party flags it screened on, taken from the rwb-source-data contract",
     "deviation id, case id; screening rule",
     PH,
     "On DeviationRaised and DeviationCleared",
     "Owning service first: S8 rwb-deviation",
     "DP-05, DP-09",
     "Ownership Map v1 sheet Tables (S8); Architecture v5 slide 15 (X1-X7 screening, pause, handling, return; DeviationRaised, DeviationCleared) and slide 42; ASM-B-DATA-25-1"],
    ["S9", "rwb-partner", "rwb_partner",
     "partner, partner_instruction, partner_user",
     "each partner_instruction against the result submitted (InstructionIssued, PartnerResultSubmitted) and against the fee or scorecard it holds for the instruction",
     "instruction id, partner id, case id",
     PH,
     "On InstructionIssued and PartnerResultSubmitted",
     "Owning service first: S9 rwb-partner",
     "DP-09",
     "Ownership Map v1 sheet Tables (S9); Architecture v5 slide 41 (panel, partner users, instructions, results, fees, scorecards) and slide 43 (InstructionIssued, PartnerResultSubmitted); ASM-B-DATA-25-1"],
]

SPLIT_HEAD = ["REC", "Check", "ACE side, read by", "Workbench side owner", "Result and break route", "Change in v4"]
SPLIT_ROWS = [
    ["REC-01", "Accounts at 90 days past due or more, less the accounts excluded at entry, against the open cases and the case list rows; count by product",
     "P1 rwb-source-data (recovery.v_ace_account)",
     "P3 rwb-case (recovery_case, case_entry_exclusion) and P1 rwb-source-data (case_list_row)",
     "P1 writes reconciliation_result and the case-list publish is held through the P3 contract; break list to the data steward",
     "P3 owns the exclusion and open-case side and answers it on its contract; P1 reads no rwb_case table (CG-B-DATA-25-1)"],
    ["REC-02", "Balances against the balances on the case accounts and the case list rows; sum by product",
     "P1 rwb-source-data (recovery.v_ace_account)",
     "P1 rwb-source-data (case_list_row) and P3 rwb-case (case_account)",
     "P1 writes reconciliation_result; break list to the data steward",
     "The balances come from the case-list projection of P1 and the case accounts from the P3 contract (CG-B-DATA-25-1)"],
    ["REC-03", "Approved treatments whose plan is booked in recovery.v_ace_plan; count and amount",
     "P1 rwb-source-data (recovery.v_ace_plan)",
     "S2 rwb-treatment (treatment)",
     "S2 owns the Workbench side and answers it on its contract; how its result reaches reconciliation_result is Not specified in the source documents (CG-B-DATA-25-4; ASM-B-DATA-25-4); officer task on a break",
     "S2 answers the treatment side; no slice of RWB-E1-011 owns it (CG-B-DATA-25-8; ASM-B-DATA-25-8)"],
    ["REC-04", "Payments in recovery.v_ace_payment against the proceeds matched to cases; count and amount",
     "P1 rwb-source-data (recovery.v_ace_payment)",
     "P8 rwb-payment (proceeds)",
     "P8 owns the Workbench side and answers it on its contract; how its result reaches reconciliation_result is Not specified in the source documents (CG-B-DATA-25-4; ASM-B-DATA-25-4); reconciliation agent and Credit Administration on a break",
     "P8 answers the proceeds side; no slice of RWB-E1-011 owns it (CG-B-DATA-25-8; ASM-B-DATA-25-8)"],
    ["REC-05", "Notices sent to WIN against the barcodes returned in recovery.v_ace_pod; count",
     "P1 rwb-source-data (recovery.v_ace_pod)",
     "P6 rwb-comms (notice)",
     "P6 owns the notice side and answers it on its contract; platform administrator on a break",
     "P6 answers the notice side on its contract; this document numbers the check REC-05 while RWB-E1-011 numbers the business-key check REC-05 (CG-B-DATA-25-6; ASM-B-DATA-25-6)"],
    ["REC-06", "Write-offs approved in the Workbench against the postings in recovery.v_ace_write_off; count and amount",
     "P1 rwb-source-data (recovery.v_ace_write_off)",
     "S7 rwb-writeoff (write_off)",
     "S7 owns the Workbench side and answers it on its contract; Credit Administration on a break",
     "S7 answers the write-off side on its contract (CG-B-DATA-25-1)"],
    ["REC-07", "Assets taken on in the Workbench against the assets in recovery.v_ace_npa_asset; count",
     "P1 rwb-source-data (recovery.v_ace_npa_asset)",
     "S5 rwb-asset (asset_sale, listing)",
     "S5 owns the Workbench side and answers it on its contract; Head of NPA on a break",
     "S5 answers the asset side on its contract (CG-B-DATA-25-1)"],
    ["REC-08", "The local decision records of the 19 services against the central decision ledger; count and last hash",
     "None: P7 rwb-decision holds the ledger and the shared topic rwb.decision-record.v1",
     "P7 rwb-decision (decision_log_entry) and the local record of every service",
     "P7 on a break, with the break list to the data steward; the hash-chain check runs at 02:00 (JOB-14)",
     "The decision-log copy to the data lake is retired with RWB-E1-014; the check compares the local records with the ledger (CG-B-DATA-25-3; ASM-B-DATA-25-3)"],
    ["REC-09", "Every account_key, person_key, asset_key and payment_code on a Workbench table against the matching view row; business key, count and amount",
     "P1 rwb-source-data (v_ace_account, v_ace_customer, v_ace_asset, v_ace_payment)",
     "The owning service of each table: P1 rwb-source-data (case_list_row, interaction, party_ext, account_ext, contact_point_ext, valuation_ext), P3 rwb-case (case_account, case_party), P8 rwb-payment (proceeds), S5 rwb-asset (asset_sale, listing), S6 rwb-debtsale (debt_sale_account)",
     "Each service lists its own orphans; P1 holds the ACE view side and answers on its contract; data steward, and the ACE team where the row is missing in ACE",
     "Each service checks its own keys (CG-B-DATA-25-1); this document numbers the check REC-09 while RWB-E1-011 numbers it REC-05 (CG-B-DATA-25-6; ASM-B-DATA-25-6)"],
]
NUM_HEAD = ["Check", "This document (v3 and v4)", "RWB-E1-011 and the realigned stories"]
NUM_ROWS = [
    ["Accounts at 90 days past due or more; balances; treatments; payments", "REC-01 to REC-04", "REC-01 to REC-04"],
    ["Notices sent to WIN, barcodes in recovery.v_ace_pod", "REC-05", "REC-09"],
    ["Write-offs approved against postings in recovery.v_ace_write_off", "REC-06", "REC-06"],
    ["Assets taken on against recovery.v_ace_npa_asset", "REC-07", "REC-07"],
    ["Decision log against the central ledger", "REC-08", "REC-08"],
    ["Business keys on the Workbench tables against the views", "REC-09", "REC-05"],
]

# ---------------------------------------------------------------- read me sheet
README = [
    ("SCB Collections and Recovery. Henka Group, 22 November 2026.", TITLE_FONT),
    ("(C) Siam Commercial Bank and Henka Pte Ltd", BODY_FONT),
    ("", None),
    ("Recovery Workbench Data Quality and Reconciliation Rules v4", TITLE_FONT),
    ("Next version of Recovery Workbench Data Quality and Reconciliation Rules v3.xlsx. "
     f"Decision {DEC} microservice realignment.", SUB_FONT),
    (f"Tool: {TOOL}.", SUB_FONT),
    ("", None),
    ("Change log", HDR_FONT),
    ("v4, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash", BODY_FONT),
    ("", None),
    ("What changed in v4", HDR_FONT),
    ("1. Reconciliations sheet: two columns are added at the end. Owner (D-RCV-60) names the service that holds the Workbench side, taken from the "
     "Microservice Ownership Map v1 sheet Tables; Per-service reconciliation (D-RCV-60) points at the row of the new sheet that carries the rule. "
     "Columns A to G keep their values except B12 and C12.", BODY_FONT),
    ("2. Reconciliations sheet, REC-08: the decision-log copy it compared is the copy to the data lake, retired with RWB-E1-014, and JOB-13 is now a "
     "continuous Kafka ingest. The row compares the 19 local decision records on rwb.decision-record.v1 with the central decision_log_entry of P7, still "
     "on count and last hash, nightly, with the 02:00 hash-chain check (JOB-14).", BODY_FONT),
    ("3. Per-service reconciliation sheet: new. One row per service of the Ownership Map gives its schema, the tables it owns, the part of each check it "
     "runs over its own rows, the contract it reads, the key, the tolerance, the cadence, the break and result route, the pattern and the basis. A second "
     "block splits the nine reconciliations across their owning services, and a third records the REC-05 and REC-09 numbering collision with RWB-E1-011.", BODY_FONT),
    ("4. Quality measures sheet: one column is added at the end, Owner service (D-RCV-60). The Timeliness meaning now reads from the freshness of "
     "rwb-source-data and from AceDataReady, because only rwb-source-data reads the ACE batch (DP-05).", BODY_FONT),
    ("5. Load checks sheet: unchanged, cell for cell. Two notes below the table record that the 98 checks stay retired to ACE ingestion and that only "
     "rwb-source-data reads the 30 recovery.v_ace_* views.", BODY_FONT),
    ("6. Read me: this sheet is new and carries the header of Template and Rules section R8.1 and the change-log row.", BODY_FONT),
    ("", None),
    ("What did not change", HDR_FONT),
    ("The 98 load checks keep their IDs, interface, source, data product, check, tolerance, failure action, owner and status, and not one of their cells "
     "changes. REC-01 to REC-09 keep their IDs, source side, Workbench side (except REC-08), compared-on, tolerance, cadence and break route (except REC-08). "
     "The six quality measures keep their names, meanings (except Timeliness) and targets. Every ID and number is copied character for character, including "
     "DQ-001 to DQ-098, REC-01 to REC-09, INT-01 to INT-16, DP01 to DP13, v_ace_account, v_ace_plan, v_ace_payment, v_ace_write_off, v_ace_npa_asset, "
     "v_ace_pod, v_ace_efs_action_code and v_ace_product.", BODY_FONT),
    ("The source carries no version number and no release date, so no date is changed and no release date is marked (tentative).", BODY_FONT),
    ("", None),
    ("Counts", HDR_FONT),
    ("Changed source cells: 3, Reconciliations!B12 and C12 and Quality measures!B7. Appended cells: 2 headers and 18 values on Reconciliations, 1 header and "
     "6 values on Quality measures. New sheet: 19 service rows, 9 reconciliation split rows and a 6-row numbering block. Notes: 2 on Load checks, 2 on "
     "Reconciliations, 1 on Quality measures.", BODY_FONT),
    ("", None),
    ("Open points", HDR_FONT),
    ("CG-B-DATA-25-1 to CG-B-DATA-25-9 and ASM-B-DATA-25-1 to ASM-B-DATA-25-9 in the Gap and Assumption registers hold the questions this version leaves "
     "open. Each is cited on the sheet it affects, and the build note under _work/msr/docs/B-DATA-25/ maps each one to its cell.", BODY_FONT),
]


def put(ws, r, c, value, font=None, fill=None, like=None, border=None):
    cell = ws.cell(row=r, column=c, value=value)
    if like is not None:
        cell._style = _copy(like._style)
    if font is not None:
        cell.font = font
    if fill is not None:
        cell.fill = fill
    if border is not None:
        cell.border = border
    cell.alignment = WRAP
    return cell


def section(ws, r, title, note, head, rows, widths=None, note2=None):
    ws.cell(row=r, column=1, value=title).font = TITLE_FONT
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=len(head))
    ws.cell(row=r + 1, column=1, value=note).font = SUB_FONT
    ws.cell(row=r + 1, column=1).alignment = WRAP
    ws.merge_cells(start_row=r + 1, start_column=1, end_row=r + 1, end_column=len(head))
    ws.row_dimensions[r + 1].height = 40
    hr = r + 3
    for i, h in enumerate(head, start=1):
        c = put(ws, hr, i, h, font=HDR_FONT, fill=HDR_FILL)
        c.border = BOX
    for j, row in enumerate(rows, start=hr + 1):
        for i, v in enumerate(row, start=1):
            put(ws, j, i, v, font=BODY_FONT, border=BOX)
    end = hr + len(rows)
    if note2:
        ws.cell(row=end + 1, column=1, value=note2).font = NOTE_FONT
        ws.cell(row=end + 1, column=1).alignment = WRAP
        ws.merge_cells(start_row=end + 1, start_column=1, end_row=end + 1, end_column=len(head))
        ws.row_dimensions[end + 1].height = 28
        end += 1
    return end


wb = openpyxl.load_workbook(V4)
assert wb.sheetnames == ["Load checks", "Reconciliations", "Quality measures"], wb.sheetnames

# ---------------------------------------------------------------- changed cells
for (sheet, addr), value in CHANGED.items():
    wb[sheet][addr] = value
print("changed cells", len(CHANGED))

# ---------------------------------------------------------------- Reconciliations
ws = wb["Reconciliations"]
assert ws.max_row == 13 and ws.max_column == 7, (ws.max_row, ws.max_column)
hdr, body = ws["A4"], ws["A5"]
for i, (name, width) in enumerate(REC_COLS, start=8):
    c = put(ws, 4, i, name, like=hdr)
    c.border = BOX
    ws.column_dimensions[get_column_letter(i)].width = width
for r in range(5, 14):
    put(ws, r, 8, REC_OWNER[r], like=body)
    put(ws, r, 9, REC_POINTER[r], like=body)
ws.auto_filter.ref = "A4:I13"
for k, text in enumerate(REC_NOTES):
    c = ws.cell(row=15 + k, column=1, value=text)
    c.font = NOTE_FONT
    c.alignment = WRAP
    ws.merge_cells(start_row=15 + k, start_column=1, end_row=15 + k, end_column=7)
    ws.row_dimensions[15 + k].height = 44
print("Reconciliations rows", ws.max_row)

# ---------------------------------------------------------------- Quality measures
ws = wb["Quality measures"]
assert ws.max_row == 10 and ws.max_column == 3, (ws.max_row, ws.max_column)
hdr, body = ws["A4"], ws["A5"]
c = put(ws, 4, 4, QM_COLS[0][0], like=hdr)
c.border = BOX
ws.column_dimensions["D"].width = QM_COLS[0][1]
for r in range(5, 11):
    put(ws, r, 4, QM_OWNER[r], like=body)
ws.auto_filter.ref = "A4:D10"
c = ws.cell(row=12, column=1, value=QM_NOTE)
c.font = NOTE_FONT
c.alignment = WRAP
ws.merge_cells(start_row=12, start_column=1, end_row=12, end_column=4)
ws.row_dimensions[12].height = 44
print("Quality measures rows", ws.max_row)

# ---------------------------------------------------------------- Load checks notes
ws = wb["Load checks"]
assert ws.max_row == 102 and ws.max_column == 10, (ws.max_row, ws.max_column)
for k, text in enumerate(LC_NOTES):
    c = ws.cell(row=104 + k, column=1, value=text)
    c.font = NOTE_FONT
    c.alignment = WRAP
    ws.merge_cells(start_row=104 + k, start_column=1, end_row=104 + k, end_column=10)
    ws.row_dimensions[104 + k].height = 30
print("Load checks rows", ws.max_row)

# ---------------------------------------------------------------- per-service sheet
ws = wb.create_sheet("Per-service reconciliation")
ws.sheet_view.showGridLines = False
for i, w in enumerate((10, 20, 18, 44, 62, 30, 30, 34, 46, 16, 62), start=1):
    ws.column_dimensions[get_column_letter(i)].width = w
end = section(
    ws, 1, "Per-service reconciliation (D-RCV-60)",
    "One row per service. Each service owns its schema and its login (ADR-014) and no service reads another service table (DP-01), so each service reconciles "
    "the part of a check that covers its own rows and answers the other services, and rwb-source-data, on its contract. Where the source states no tolerance the "
    "cell carries the placeholder of Template and Rules R9 (CG-B-DATA-25-4, CG-B-DATA-25-5; ASM-B-DATA-25-4, ASM-B-DATA-25-5).",
    PS_HEAD, PS_ROWS)
print("per-service rows", len(PS_ROWS), "end", end)

end = section(
    ws, end + 2, "The nine reconciliations and their per-service owner (D-RCV-60)",
    "The nine rows of the Reconciliations sheet, split by the service that holds each side. rwb-source-data reads the ACE views for every row (DP-05) and keeps "
    "the JOB-04 run and reconciliation_result; the Workbench side belongs to the owner, and the run takes it through that owner contract, one hop with a 2 s timeout (DP-11).",
    SPLIT_HEAD, SPLIT_ROWS)
print("split rows", len(SPLIT_ROWS), "end", end)

end = section(
    ws, end + 2, "REC numbering (D-RCV-60)",
    "The source numbers the notice-barcode check REC-05 and the business-key check REC-09; RWB-E1-011 and every realigned story slice number the business-key "
    "check REC-05 and the notice-barcode check REC-09. v4 keeps the source IDs (Template and Rules R8.2 and root rule 8) and states the mapping here. The "
    "collision is CG-B-DATA-25-6 and ASM-B-DATA-25-6; a row cites the check by name wherever the number would be ambiguous.",
    NUM_HEAD, NUM_ROWS, widths=None,
    note2="No reconciliation ID is renumbered in v4. Step D1 aligns this document and the story set on one numbering, as ASM-B-DATA-25-6 records.")
print("numbering rows", len(NUM_ROWS), "end", end)

# ---------------------------------------------------------------- read me sheet
ws = wb.create_sheet("Read me", 0)
ws.sheet_view.showGridLines = False
ws.column_dimensions["A"].width = 132
for i, (text, font) in enumerate(README, start=1):
    if text == "":
        continue
    c = ws.cell(row=i, column=1, value=text)
    if font is not None:
        c.font = font
    c.alignment = Alignment(wrap_text=True, vertical="top")
    if font is TITLE_FONT or font is HDR_FONT:
        ws.row_dimensions[i].height = 18

# Read me first, then the three source sheets in their order, then the new sheet.
order = ["Read me", "Load checks", "Reconciliations", "Per-service reconciliation", "Quality measures"]
wb._sheets = [wb[n] for n in order]

wb.save(V4)
print("WROTE", V4)
print("sheets", wb.sheetnames)
