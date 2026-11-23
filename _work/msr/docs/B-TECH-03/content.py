"""Authored per-module content for WP B-TECH-03 (TSD by Module v6). Scratch only."""

# (type, operation, provider, fault path) - cross-module call contracts consumed
REST = "REST"
TMP = "Temporal"
NEX = "Nexus"
SQL = "SQL"
FILE = "File"

C_FAIL = "2 s timeout, breaker; built against the fake (ADR-020)"
T_FAIL = "Workflow retry policy; the caller keeps its state (DP-12)"
E_FAIL = "Retry 1 min, 10 min, 1 h, then `.dlt`; inbox dedupe"
F_FAIL = "Claim-check manifest; retry, then an operations task"
X_FAIL = "Tracked only; outside the Workbench; class X"

MODULES = {
    "P1": {
        "title": "Recovery data engine",
        "owns": "ACE view contract, extension tables, freshness, reconciliation",
        "consumed_rest": [
            (SQL, "SELECT on the 30 `recovery.v_ace_*` views (T1.1, T6.3)", "ACE database",
             "X", "Read-only grant; a direct public.* read fails at the database"),
        ],
        "consumed_temp": [],
        "consumed_events": [],
        "provided_temp": [
            ("Temporal activity", "listEligibleAccounts(businessDate)", "P3 rwb-case", "Contract of T5.2.1; runs on rwb-source-data"),
            ("Temporal activity", "snapshot(page)", "P3 rwb-case, P9 rwb-reporting", "Contract of T5.2.1; runs on rwb-source-data"),
            ("Temporal workflow", "AceIngestCheck", "P1 rwb-source-data", "Started by the ACE batch-complete record or AceDataReady (JOB-04)"),
            ("Temporal workflow", "reconciliation", "P1 rwb-source-data", "JOB-04 daily reconciliation (DP-10)"),
        ],
        "files": [
            ("SQL view contract", "`recovery.v_ace_*` (30 views)", "ACE database, read-only", "SELECT only; grants and the conformance test in T6.3"),
        ],
        "t3_note": ("Every object of T3 that the Ownership Map v1 assigns to P1 lives in schema `rwb_source_data`. Two "
                    "objects are not built as T3 states them: `retention_rule` is P5's table (Ownership Map ruling "
                    "`retention_rule`, ASM-A6-tables-10), and the lake copy target is removed under DP-17 (ADR-018; "
                    "CG-B-TECH-03-1; ASM-B-TECH-03-2). `interaction` is owned here (Ownership Map ruling "
                    "`case_list_row`; DP-18)."),
        "t0_note": ("P1 is the only service that reads ACE tables, through the 30 read-only views, and the only owner of "
                    "the interaction ledger (DP-05, DP-18)."),
    },
    "P2": {
        "title": "Integration",
        "owns": "interface config, file runs, outbound items, ACE integration paths",
        "consumed_rest": [
            (REST, "Fetch an outbound file by ID through a time-limited SAS link", "P5 rwb-document", "C", C_FAIL),
        ],
        "consumed_temp": [],
        "consumed_events": [],
        "provided_temp": [
            ("Temporal activity", "deliverFile(manifest)", "P6 rwb-comms, P8 rwb-payment, P9 rwb-reporting, S6 rwb-debtsale",
             "Contract of T5.2.1; runs on rwb-integration"),
            ("Temporal activity", "receiveFile", "P2 rwb-integration", "Contract of T5.2.1; runs on rwb-integration"),
        ],
        "files": [
            ("Outbound file", "WIN registered mail, daily (INT-14)", "WIN", "16:00 file window, opened by Airflow (JOB-10)"),
            ("Outbound file", "Debt buyer data tape per lot, encrypted (INT-25)", "Debt buyers", "Per awarded lot, encrypted and masked (NFR-041)"),
        ],
        "t3_note": ("T3.1 mixes three kinds of object: the business tables `interface_config`, `outbound_item` and "
                    "`job_catalog` (P2 in the Ownership Map); the platform tables `outbox_event`, `outbox_delivery`, "
                    "`processed_event`, `idempotency_key`, `feature_flag` and `feature_flag_change`, which belong to "
                    "the shared libraries and not to a service schema (DP-09, DP-15); and `efs_ledger_outcome`, which "
                    "the Ownership Map places with P1 (CG-B-TECH-03-2; ASM-B-TECH-03-3). `party_product` is read from "
                    "ACE and is not a table of this service."),
        "t0_note": ("P2 is the only holder of the outbound file adapters and the ACE integration paths; it owns no "
                    "inbound interface since D-RCV-35."),
    },
    "P3": {
        "title": "Case and workflow",
        "owns": "case, CMMN state, queues, tasks, allocation, timers",
        "consumed_rest": [
            (REST, "POST /authorise, GET /me/permissions, GET /doa-limits, GET /masking-policies", "P4 rwb-access",
             "C", C_FAIL + "; the answer is cached and refreshed on the access events"),
        ],
        "consumed_temp": [
            ("Temporal activity", "listEligibleAccounts(businessDate)", "P1 rwb-source-data", "C", T_FAIL),
            ("Temporal child workflow", "RouteDecisionWorkflow", "S1 rwb-valuation", "C", T_FAIL),
            ("Temporal child workflow", "TreatmentWorkflow (stage workflows)", "S2 rwb-treatment", "C", T_FAIL),
            ("Temporal child workflow", "GuaranteeClaimWorkflow", "S3 rwb-guarantee", "C", T_FAIL),
            ("Temporal child workflow", "LitigationWorkflow", "S4 rwb-litigation", "C", T_FAIL),
            ("Temporal child workflow", "AssetDisposalWorkflow", "S5 rwb-asset", "C", T_FAIL),
            ("Temporal child workflow", "DebtSaleWorkflow", "S6 rwb-debtsale", "C", T_FAIL),
            ("Temporal child workflow", "WriteOffWorkflow", "S7 rwb-writeoff", "C", T_FAIL),
            ("Temporal child workflow", "DeviationWorkflow", "S8 rwb-deviation", "C", T_FAIL),
        ],
        "consumed_events": [
            ("", "RouteDecided", "S1"), ("EV-06", "DeviationRaised", "S8"), ("EV-07", "DeviationCleared", "S8"),
            ("EV-11", "TreatmentBooked", "P8"), ("EV-12", "PaymentMissed", "P8"), ("EV-25", "ProceedsMatched", "P8"),
            ("EV-23", "LotAwarded", "S6"), ("EV-22", "AssetTakenOn", "S5"), ("EV-24", "WriteOffApproved", "S7"),
            ("EV-26", "AceDataReady", "P1"), ("EV-30", "RulePackageInForce", "P7"),
        ],
        "provided_temp": [
            ("Temporal workflow", "CaseWorkflow (parent, one per case)", "gateway-bff and the stage services", "DP-12; workflow ID case-{caseId} (T2.4)"),
            ("Temporal workflow", "DailyCaseRun (Schedule plus AceDataReady)", "P3 rwb-case", "JOB-02 and JOB-03 (DP-10)"),
            ("Temporal activity", "allocate, transfer, rebalance", "P3 rwb-case", "DailyCaseRun steps"),
        ],
        "files": [],
        "t3_note": ("T3.1 names four objects that the Ownership Map v1 places in another service: `interaction` is P1's "
                    "(DP-18), and `rule_package`, `rule_package_version`, `rule_row` and `rule_test_case` are P7's "
                    "registry (Architecture v5 slide 41, DMN model registry). T3.1 of this version says P4 for the "
                    "rule package tables, which Architecture v5 and the Ownership Map do not support (CG-B-TECH-03-3; "
                    "ASM-B-TECH-03-4)."),
        "t0_note": ("P3 is the case system of record and the parent of every stage workflow; it owns no rule package "
                    "table since D-RCV-60 (DP-04, DP-12)."),
    },
    "P4": {
        "title": "Access and administration",
        "owns": "Recovery roles as data, scope, masking policy, DoA table, access log",
        "consumed_rest": [
            (REST, "Sign-in and group-to-role mapping (Entra ID)", "ACE Common", "X", X_FAIL),
        ],
        "consumed_temp": [],
        "consumed_events": [],
        "provided_temp": [
            ("Temporal Schedule", "Access review list (six-monthly)", "P4 rwb-access", "JOB-18 (DP-10)"),
        ],
        "files": [],
        "t3_note": ("T3.1 names three objects that the Ownership Map v1 places elsewhere: `lov_value` is P3's reference "
                    "data (DP-07), `partner_user` is S9's (Ownership Map ruling `partner_user`, ASM-A6-tables-6), and "
                    "`rule_package`, `rule_package_version`, `rule_row` and `rule_test_case` are P7's registry "
                    "(CG-B-TECH-03-3). `delegation_limit` stays here (Ownership Map ruling `delegation_limit`, "
                    "ASM-A6-tables-4)."),
        "t0_note": ("P4 is the authorisation provider for all 19 services: the authorise contract and the guard library "
                    "replace the monolith's in-process access check (DP-08)."),
    },
    "P5": {
        "title": "Document hub",
        "owns": "metadata, custody, OCR text and fields, signatures, retention",
        "consumed_rest": [],
        "consumed_temp": [
            ("Temporal child workflow", "Agent run: classify and extract", "P10 rwb-agent", "C", T_FAIL),
        ],
        "consumed_events": [("EV-28", "AgentRunCompleted", "P10")],
        "provided_temp": [
            ("Temporal workflow", "DocumentIntakeWorkflow (OCR, classify, extract)", "P5 rwb-document (intake)", "Runs on rwb-document"),
            ("Temporal activity", "generate, seal", "P5 rwb-document", "Called by P6 rwb-comms and by its own intake"),
            ("Temporal Schedule", "Retention", "P5 rwb-document", "JOB-17, monthly on the first Sunday (DP-10)"),
        ],
        "files": [
            ("Claim-check file", "Document content in Azure Blob with WORM", "P5 rwb-document", "2.8 TB by 2031 (Architecture v5 slide 16)"),
        ],
        "t3_note": ("Every object of T3.1 stays here; `signature_request` is P5's table under the Ownership Map "
                    "(ruling `signature_request`, ASM-A6-tables-11), although TSD P6 v2 defines it."),
        "t0_note": ("P5 holds the claim-check content for every service that stores a document; the other services hold "
                    "the reference only (DP-01, DP-11)."),
    },
    "P6": {
        "title": "Communications",
        "owns": "notices, templates, merge fields, proof of delivery",
        "consumed_rest": [
            (REST, "Notification path for SMS and LINE (INT-17, INT-18)", "ACE Common", "X", X_FAIL),
        ],
        "consumed_temp": [
            ("Temporal activity", "generate letter", "P5 rwb-document", "C", T_FAIL),
            ("Temporal child workflow", "Approval", "P7 rwb-decision", "C", T_FAIL),
            ("Temporal activity", "deliverFile(manifest) for WIN letters", "P2 rwb-integration", "C", T_FAIL),
        ],
        "consumed_events": [
            ("EV-06", "DeviationRaised", "S8"), ("EV-07", "DeviationCleared", "S8"),
            ("EV-10", "TreatmentApproved", "S2"), ("EV-12", "PaymentMissed", "P8"), ("EV-05", "CaseStateChanged", "P3"),
        ],
        "provided_temp": [
            ("Temporal workflow", "NoticeDispatchWorkflow", "P3 rwb-case and the stage services", "Kit template; runs on rwb-comms"),
        ],
        "files": [],
        "t3_note": ("`notice`, `template` and `merge_field` stay here. `signature_request`, which T3.1 lists, is P5's "
                    "(Ownership Map ruling `signature_request`, ASM-A6-tables-11); P6 orchestrates the request through "
                    "P5's contract and holds no signature row."),
        "t0_note": ("P6 owns the notice and template estate; the letter content is a P5 document and the delivery file "
                    "is a P2 file (DP-11, DP-16)."),
    },
    "P7": {
        "title": "Decision center and log",
        "owns": "approvals, central decision ledger, DMN model registry",
        "consumed_rest": [
            (REST, "GET /doa-limits (delegation of authority)", "P4 rwb-access", "C", C_FAIL),
        ],
        "consumed_temp": [],
        "consumed_events": [
            ("EV-08", "DecisionRecorded (from all 19)", "all"), ("EV-13", "NoticeGenerated", "P6"),
            ("EV-28", "AgentRunCompleted", "P10"),
        ],
        "provided_temp": [
            ("Temporal workflow", "ApprovalWorkflow", "P3 rwb-case and the stage services", "Kit template; runs on rwb-decision"),
            ("Temporal Schedule", "Rule promote, 00:01", "P7 rwb-decision", "JOB-20; publishes RulePackageInForce (EV-30)"),
            ("Temporal Schedule", "Chain check, 02:00", "P7 rwb-decision", "JOB-14 hash-chain check"),
        ],
        "files": [
            ("Claim-check file", "Daily ledger seal in immutable storage (WORM)", "P7 rwb-decision", "One seal per business date (Architecture v5 slide 14)"),
        ],
        "t3_note": ("`approval`, `decision_log_entry` and the four rule package tables are P7's under the Ownership Map; "
                    "T3.1 of TSD P3 v3 and TSD P4 v3 place the rule package tables with P4, which Architecture v5 does "
                    "not support (CG-B-TECH-03-3; ASM-B-TECH-03-4)."),
        "t0_note": ("P7 owns the central decision ledger and the rule package registry; every service publishes "
                    "DecisionRecorded to `rwb.decision-record.v1` and evaluates rules locally (DP-03, DP-04)."),
    },
    "P8": {
        "title": "Payments and posting",
        "owns": "payment and proceeds matching, fees, bookings, posting files",
        "consumed_rest": [],
        "consumed_temp": [
            ("Temporal activity", "payments for the business date", "P1 rwb-source-data", "C", T_FAIL),
            ("Temporal activity", "deliverFile(manifest) for the posting file", "P2 rwb-integration", "C", T_FAIL),
        ],
        "consumed_events": [
            ("EV-26", "AceDataReady", "P1"), ("EV-10", "TreatmentApproved", "S2"), ("EV-23", "LotAwarded", "S6"),
            ("", "AssetSold", "S5"), ("EV-24", "WriteOffApproved", "S7"),
        ],
        "provided_temp": [
            ("Temporal activity", "matchPayments, confirmBookings", "P8 rwb-payment", "JOB-07 and JOB-08 as event-started workflows"),
            ("Temporal activity", "postProceeds (saga step)", "P8 rwb-payment", "Called by S2, S5, S6 and S7"),
        ],
        "files": [],
        "t3_note": ("`proceeds` is this service's table. `payment_match_rule`, which T3.1 lists, has no row in the "
                    "Ownership Map Tables sheet; the match rules become the PAYMENT_MATCH rule package of rwb-decision "
                    "(TSD P3 T2.2), so P8 keeps the proceeds rows and no rule table (CG-B-TECH-03-4; ASM-B-TECH-03-5)."),
        "t0_note": ("P8 is the only writer of proceeds and bookings; other services reach it through the postProceeds "
                    "activity, never through its tables (DP-01, DP-11)."),
    },
    "P9": {
        "title": "Reporting",
        "owns": "measures, snapshots, steering dashboard, regulatory reports",
        "consumed_rest": [],
        "consumed_temp": [
            ("Temporal activity", "snapshot(page) for measures", "P1 rwb-source-data", "C", T_FAIL),
            ("Temporal activity", "deliverFile(manifest) for the regulatory extract", "P2 rwb-integration", "C", T_FAIL),
        ],
        "consumed_events": [
            ("EV-08", "DecisionRecorded", "all"), ("", "Every business event of the 19 services (projections)", "all"),
        ],
        "provided_temp": [
            ("Temporal Schedule", "Measures, 01:30", "P9 rwb-reporting", "JOB-15 (DP-10)"),
            ("Temporal activity", "buildRegulatoryExtract", "P9 rwb-reporting", "Triggered by Airflow; no data lake (DP-17)"),
        ],
        "files": [],
        "t3_note": ("`measure_definition`, `measure_snapshot` and `measure_publish` stay here. The projections are built "
                    "from events; there is no data lake copy (DP-17, ADR-018)."),
        "t0_note": ("P9 calls almost nobody and listens widely: it projects from the event stream and reads source data "
                    "through the P1 snapshot activity (Architecture v5 slide 13)."),
    },
    "P10": {
        "title": "Agent runtime",
        "owns": "agent policies, prompts, runs, guardrails, evaluations",
        "consumed_rest": [
            (REST, "Tool: read case facts (read-only)", "P1 rwb-source-data", "C", C_FAIL),
            (REST, "Tool: read extracted document fields (read-only)", "P5 rwb-document", "C", C_FAIL),
            (REST, "Enterprise AI endpoint over a private HTTPS endpoint", "Enterprise AI platform", "X", X_FAIL),
        ],
        "consumed_temp": [],
        "consumed_events": [("EV-16", "DocumentStored (intake)", "P5"), ("EV-01", "CaseCreated (screening)", "P3")],
        "provided_temp": [
            ("Temporal workflow", "AgentRunWorkflow (60 s, then the rule result)", "P5 rwb-document, S1 rwb-valuation, S8 rwb-deviation", "Runs on rwb-agent"),
            ("Temporal activity", "tool gateway: read-only calls for the agent", "P10 rwb-agent", "The only path from the agent to a service"),
        ],
        "files": [],
        "t3_note": ("Every object of T3.1 stays here: the agent estate is P10's alone and no other service reads an "
                    "agent table (DP-01)."),
        "t0_note": ("P10 is the only caller of the enterprise AI endpoint, and it reaches Workbench data only through the "
                    "read-only tool gateway (DP-20)."),
    },
    "S1": {
        "title": "Valuation and route",
        "owns": "valuations, D6 route decision, route agent output",
        "consumed_rest": [
            (REST, "Collateral and appraisals (read-only)", "P1 rwb-source-data", "C", C_FAIL),
        ],
        "consumed_temp": [
            ("Temporal child workflow", "Agent run: route agent", "P10 rwb-agent", "C", T_FAIL),
            ("Temporal child workflow", "Approval", "P7 rwb-decision", "C", T_FAIL),
        ],
        "consumed_events": [("EV-30", "RulePackageInForce", "P7")],
        "provided_temp": [
            ("Temporal workflow", "RouteDecisionWorkflow (child of the case)", "P3 rwb-case", "Child of CaseWorkflow; runs on rwb-valuation"),
        ],
        "files": [],
        "t3_note": ("T3.1 defines `valuation` as a NEW table of this service and `score` as a REUSE ACE object. The "
                    "Ownership Map Tables sheet lists no table owned by S1: `valuation_ext` is P1's, and the "
                    "`rwb_valuation` schema of Architecture v5 slide 41 holds the route decision. The map's Endpoints "
                    "ruling puts the valuation paths with S1, so T5.2.1 lists them here and the table question is "
                    "recorded (CG-B-TECH-03-5; ASM-B-TECH-03-6)."),
        "t0_note": ("S1 owns the D6 route decision and the route agent output; it reaches the case only through the "
                    "RouteDecisionWorkflow child of P3 (DP-12)."),
    },
    "S2": {
        "title": "TDR, settlement and deed in lieu",
        "owns": "treatments, contracts, settlement and deed-in-lieu agreements, plan timers",
        "consumed_rest": [],
        "consumed_temp": [
            ("Temporal child workflow", "Approval", "P7 rwb-decision", "C", T_FAIL),
            ("Temporal activity", "Contract generation and e-signature", "P5 rwb-document", "C", T_FAIL),
            ("Temporal activity", "postProceeds", "P8 rwb-payment", "C", T_FAIL),
            ("Nexus operation", "Restructure calculator", "ACE Common", "X", X_FAIL),
        ],
        "consumed_events": [
            ("EV-11", "TreatmentBooked", "P8"), ("EV-12", "PaymentMissed", "P8"), ("EV-06", "DeviationRaised", "S8"),
        ],
        "provided_temp": [
            ("Temporal workflow", "TreatmentWorkflow; settlement and deed-in-lieu sagas", "P3 rwb-case",
             "Stage workflows of the case; run on rwb-treatment"),
        ],
        "files": [],
        "t3_note": ("`treatment` is this service's table; the TDR plans are read from ACE and are not copied (DP-05)."),
        "t0_note": ("S2 is the pivot of the treatment saga: booking through P8, contract through P5, approval through P7, "
                    "and the ACE restructure calculator through Nexus (Architecture v5 slide 18)."),
    },
    "S3": {
        "title": "Guarantees and guarantors",
        "owns": "TCG and insurance claims, guarantor notices and pursuit",
        "consumed_rest": [],
        "consumed_temp": [
            ("Temporal child workflow", "Guarantor notice", "P6 rwb-comms", "C", T_FAIL),
            ("Temporal child workflow", "Approval", "P7 rwb-decision", "C", T_FAIL),
        ],
        "consumed_events": [("EV-15", "NoticeDelivered", "P6"), ("EV-25", "ProceedsMatched", "P8")],
        "provided_temp": [
            ("Temporal workflow", "GuaranteeClaimWorkflow", "P3 rwb-case", "Stage workflow of the case; runs on rwb-guarantee"),
        ],
        "files": [],
        "t3_note": ("`guarantee_claim` is this service's table; the dated DP04 copies of the claim stay with P1 and are "
                    "read-only here (Ownership Map ruling `dp_guarantee_claim`, ASM-A6-tables-14)."),
        "t0_note": ("S3 pursues the guarantor through P6 notices and P7 approvals; it holds the claim, not the notice "
                    "(DP-01, DP-11)."),
    },
    "S4": {
        "title": "Litigation and enforcement",
        "owns": "legal actions, hearings, judgments, enforcement, LED auction ladder",
        "consumed_rest": [],
        "consumed_temp": [
            ("Temporal activity", "issueInstruction (law firm)", "S9 rwb-partner", "C", T_FAIL),
            ("Temporal child workflow", "Demand notice", "P6 rwb-comms", "C", T_FAIL),
            ("Temporal child workflow", "Approval", "P7 rwb-decision", "C", T_FAIL),
        ],
        "consumed_events": [("EV-15", "NoticeDelivered", "P6"), ("EV-21", "PartnerResultSubmitted", "S9")],
        "provided_temp": [
            ("Temporal workflow", "LitigationWorkflow (years; continues as new)", "P3 rwb-case", "Stage workflow of the case; runs on rwb-litigation"),
        ],
        "files": [],
        "t3_note": ("`legal_action` and `hearing` are this service's tables; the partner result arrives as an event and "
                    "is never written here from a partner table (DP-01, DP-11)."),
        "t0_note": ("S4 runs for years and relies on Continue-As-New; the law-firm instruction is a P9 activity on S9's "
                    "queue (Architecture v5 slide 19)."),
    },
    "S5": {
        "title": "Assets and auction",
        "owns": "assets taken on, holding, floor price, listings, auction rounds",
        "consumed_rest": [],
        "consumed_temp": [
            ("Temporal activity", "issueInstruction (auction vendor)", "S9 rwb-partner", "C", T_FAIL),
            ("Temporal child workflow", "Approval", "P7 rwb-decision", "C", T_FAIL),
            ("Temporal activity", "postProceeds", "P8 rwb-payment", "C", T_FAIL),
        ],
        "consumed_events": [
            ("", "JudgmentRecorded", "S4"), ("", "AuctionResult", "S4"), ("EV-25", "ProceedsMatched", "P8"),
        ],
        "provided_temp": [
            ("Temporal workflow", "AssetDisposalWorkflow", "P3 rwb-case", "Stage workflow of the case; runs on rwb-asset"),
            ("Temporal Schedule", "Re-appraisal, monthly", "S5 rwb-asset", "JOB-19 (DP-10)"),
        ],
        "files": [],
        "t3_note": ("`listing` and `asset_sale` are this service's tables. `asset` is an ACE record read through the read "
                    "path and is not a table of this service; the Ownership Map gives S5 no `asset` row."),
        "t0_note": ("S5 owns the disposal path from the judgment to the proceeds, with the auction vendor instructed "
                    "through S9 and the money posted through P8 (Architecture v5 slide 19)."),
    },
    "S6": {
        "title": "Debt sale",
        "owns": "lots, data room, buyer terms, bids, award, transfer",
        "consumed_rest": [],
        "consumed_temp": [
            ("Temporal activity", "Data room pack", "P5 rwb-document", "C", T_FAIL),
            ("Temporal child workflow", "Approval", "P7 rwb-decision", "C", T_FAIL),
            ("Temporal activity", "deliverFile(manifest) for the buyer file", "P2 rwb-integration", "C", T_FAIL),
            ("Temporal activity", "postProceeds", "P8 rwb-payment", "C", T_FAIL),
        ],
        "consumed_events": [("EV-25", "ProceedsMatched", "P8")],
        "provided_temp": [
            ("Temporal workflow", "DebtSaleWorkflow (saga, pivot at transfer)", "P3 rwb-case", "Stage workflow of the case; runs on rwb-debtsale"),
        ],
        "files": [],
        "t3_note": ("`debt_sale_lot` and `debt_sale_account` are this service's tables; the data room is a P5 document "
                    "set and the buyer tape is a P2 file (DP-11, DP-16)."),
        "t0_note": ("S6 is a saga with the transfer as its pivot; the data room is published through the partner gateway "
                    "and the buyer file leaves through P2 (Architecture v5 slides 13 and 19)."),
    },
    "S7": {
        "title": "Write-off and recovery",
        "owns": "eligibility, committee, posting, recovery after charge-off",
        "consumed_rest": [
            (REST, "GL write-off outcome, read-only", "P1 rwb-source-data", "C", C_FAIL),
        ],
        "consumed_temp": [
            ("Temporal child workflow", "Committee approval", "P7 rwb-decision", "C", T_FAIL),
            ("Temporal activity", "postProceeds", "P8 rwb-payment", "C", T_FAIL),
        ],
        "consumed_events": [("EV-26", "AceDataReady", "P1"), ("EV-25", "ProceedsMatched", "P8")],
        "provided_temp": [
            ("Temporal workflow", "WriteOffWorkflow", "P3 rwb-case", "Stage workflow of the case; runs on rwb-writeoff"),
            ("Temporal Schedule", "Scan, third working day", "S7 rwb-writeoff", "JOB-16 (DP-10)"),
        ],
        "files": [],
        "t3_note": ("`write_off` is this service's table; the GL postings stay in ACE and are read through the P1 contract "
                    "(INT-16, DP-05)."),
        "t0_note": ("S7 owns the write-off and the recovery after charge-off; the committee decision is a P7 child "
                    "workflow and the postings are read from ACE (Architecture v5 slide 20)."),
    },
    "S8": {
        "title": "Deviation handling",
        "owns": "X1-X7 screening, pause, handling, return",
        "consumed_rest": [
            (REST, "Party flags (deceased, bankrupt), read-only", "P1 rwb-source-data", "C", C_FAIL),
        ],
        "consumed_temp": [
            ("Temporal child workflow", "Agent run: screening", "P10 rwb-agent", "C", T_FAIL),
        ],
        "consumed_events": [
            ("EV-01", "CaseCreated (screening)", "P3"), ("EV-26", "AceDataReady", "P1"), ("EV-28", "AgentRunCompleted", "P10"),
        ],
        "provided_temp": [
            ("Temporal workflow", "DeviationWorkflow (child of the case)", "S8 rwb-deviation", "Started by P3 rwb-case"),
        ],
        "files": [],
        "t3_note": ("`deviation` is this service's table; X1 to X7 screening reads the party flags through the P1 "
                    "contract and keeps no copy (DP-05)."),
        "t0_note": ("S8 is the only service that can pause a case: it raises and clears the deviation that P3 listens "
                    "for (Architecture v5 slide 15)."),
    },
    "S9": {
        "title": "Partner management",
        "owns": "panel, partner users, instructions, results, fees, scorecards",
        "consumed_rest": [
            (REST, "Partner upload link (time-limited)", "P5 rwb-document", "C", C_FAIL),
            (REST, "Partner gateway: partner identity and MFA (FAPI 2.0)", "Partner gateway", "X", X_FAIL),
        ],
        "consumed_temp": [],
        "consumed_events": [],
        "provided_temp": [
            ("Temporal workflow", "InstructionWorkflow (SLA timers)", "S9 rwb-partner", "Contract of T5.2.1"),
            ("Temporal activity", "issueInstruction, recordResult", "S9 rwb-partner", "Called by S4 and S5"),
        ],
        "files": [],
        "t3_note": ("`partner`, `partner_instruction` and `partner_user` are this service's tables; internal roles stay "
                    "in P4 and partner users do not (Ownership Map ruling `partner_user`, ASM-A6-tables-6)."),
        "t0_note": ("S9 is the only service reachable from outside the bank: the partner gateway in the DMZ terminates "
                    "partner traffic and S9 owns the panel, the instructions and the results (ADR-019)."),
    },
}

# legacy marker -> (regex, landing text)
LANDS = {
    "DP-01": (r"\brecovery\.|recovery schema", "Owns its tables in `{schema}`; no other service reads them (ADR-014)."),
    "DP-02": (r"recovery_svc", "One login, `{schema}`, with its own connection pool cap."),
    "DP-03": (r"DecisionLogWriter|decision log", "Local decision record plus DecisionRecorded (EV-08) on `rwb.decision-record.v1`."),
    "DP-04": (r"RuleEvaluator|KieBase|Drools|rule package", "Embedded Drools kit; rule packages from `rwb-decision` (C RWB-P7-E1073-CON; ADR-017)."),
    "DP-05": (r"AceSourceQuery|v_ace_|account_ext", "Reads ACE through the `rwb-source-data` contract or its own `v_ace_*` views (ADR-010)."),
    "DP-06": (r"parameter|casewf\.config", "Parameters from the `rwb-case` contract and the client library (H RWB-PLT-E1042-CON)."),
    "DP-07": (r"\bLOV\b|reference data", "Reference data and lists of values from the `rwb-case` contract (H RWB-PLT-E1043-CON)."),
    "DP-08": (r"RecoveryAccessGuard|RW-[A-Z]+|role checks|authoris", "Authorisation through the `rwb-access` authorise contract and the guard library (H RWB-PLT-E1037-CON)."),
    "DP-09": (r"outbox|outbound queue|event", "Outbox and inbox library; CloudEvents on `{topic}` with retry topics and `.dlt`."),
    "DP-10": (r"Quartz|\bJOB-\d", "Temporal Schedules and event-started workflows through the workflow kit (ADR-016)."),
    "DP-11": (r"published interface", "One REST hop, 2 s timeout, breaker; the consumer builds against the provider's fake (ADR-020)."),
    "DP-12": (r"one workflow per case|CaseWorkflow|case workflow", "CaseWorkflow parent with a child workflow per stage."),
    "DP-13": (r"/api/recovery/v1", "REST base `{base}`."),
    "DP-14": (r"rwb\.p\d\.|rwb\.casewf|topic", "Topic `{topic}`, retry topics and `.dlt`; naming library (H RWB-PLT-E1047-CON)."),
    "DP-15": (r"\bV000\d\b|Flyway|migration", "Per-service Flyway sequence in `{schema}`."),
    "DP-16": (r"integration\.adapter|outbound file", "Files through the `rwb-integration` contract (C RWB-P2-E1007-CON)."),
    "DP-17": (r"data lake|INT-19|INT-20", "No data lake: reporting reads events; the lake copy is removed (ADR-018)."),
    "DP-18": (r"ledger", "Interaction ledger owned by `rwb-source-data` (default ruling; DP-18)."),
    "DP-19": (r"ace-web|screen", "Screens composed by gateway-bff; one composite route per screen (H RWB-PLT-N001-CON)."),
    "DP-20": (r"agent client|agent platform|route agent|screening agent|AgentRun", "Agent work through the `rwb-agent` contract (C RWB-P10-TE013-CON)."),
}
CORE = ["DP-01", "DP-02", "DP-03", "DP-08", "DP-09", "DP-13", "DP-14", "DP-15"]
