"""Build the row blocks for the v4 workbook (D-RCV-60). Writes JSON only; the copy is changed by build_v4.py."""
import json
from pathlib import Path

DOCS = Path(__file__).resolve().parent

# ---------------------------------------------------------------- Service volumes
HEAD_SV = ["Code", "Service", "Wave", "Volume driver", "Volume, 2027", "Unit", "Basis",
           "Kafka topic", "Task queue", "Consumers of its events"]

NS5 = "Not specified in the source documents (CG-B-DATA-26-5; ASM-B-DATA-26-5)"
NS4 = "Not specified in the source documents (CG-B-DATA-26-4; ASM-B-DATA-26-4)"

SERVICES = [
    ("P1", "rwb-source-data", 1,
     "Eligible accounts listed for each business day and the ACE view reads behind the screens",
     "=Inputs!C5+Inputs!C6+Inputs!C8", "accounts a day",
     "Inputs!C5, C6 and C8 (active inventory); the peak view read rate is Read path!B10",
     "rwb.source-data.events.v1", "rwb-source-data",
     "rwb-case, rwb-payment, rwb-deviation, rwb-writeoff"),
    ("P2", "rwb-integration", 1,
     "WIN registered-letter file (INT-14) and the debt-buyer files (INT-25)",
     "=Inputs!C26", "registered letters a month",
     "Inputs!C26; one WIN outbound file a day (JOB-10)",
     "rwb.integration.events.v1", "rwb-integration",
     "the service that requested the file (FileDelivered, FileFailed)"),
    ("P3", "rwb-case", 1,
     "New cases created, allocated and rebalanced (JOB-02, JOB-03, JOB-06), with the parent CaseWorkflow per case",
     "='Five years'!C5/12", "cases a month",
     "Five years!C5 / 12, the 2027 inflow",
     "rwb.case.events.v1", "rwb-case",
     "rwb-agent, rwb-deviation, rwb-reporting, gateway-bff (inbox)"),
    ("P4", "rwb-access", 1,
     "Authorise calls behind every screen action, served from the permission cache",
     "='Users and load'!E8", "requests a second at peak",
     "Users and load!E8; one authorise call per request, cached per session",
     "rwb.access.events.v1", "rwb-access",
     "all 19 services (cache refresh on AccessPolicyChanged and DoaLimitChanged)"),
    ("P5", "rwb-document", 1,
     "Documents stored, OCR and classified (JOB-12, DocumentIntakeWorkflow)",
     "='Five years'!E5/12", "documents a month",
     "Five years!E5 / 12, the 2027 document additions",
     "rwb.document.events.v1", "rwb-document",
     "rwb-agent, rwb-case"),
    ("P6", "rwb-comms", 1,
     "Notices generated and dispatched; WIN letters at 16:00 (JOB-10)",
     "=Inputs!C26", "registered letters a month",
     "Inputs!C26; SMS and LINE go through ACE Common and are not counted here",
     "rwb.comms.events.v1", "rwb-comms",
     "rwb-decision, rwb-reporting, rwb-litigation, rwb-guarantee, rwb-case"),
    ("P7", "rwb-decision", 1,
     "Decision records collected into the central ledger, approvals and rule promotion (JOB-14, JOB-20)",
     "='Five years'!H5/12", "decision-log entries a month",
     "Five years!H5 / 12; the ledger is fed by DecisionRecorded from all 19 services",
     "rwb.decision.events.v1", "rwb-decision",
     "gateway-bff (inbox); rwb-case, rwb-valuation, rwb-treatment, rwb-payment (RulePackageInForce)"),
    ("P8", "rwb-payment", 2,
     "Payment matching and booking confirmation (JOB-07, JOB-08)",
     NS5, "payments a month",
     "No payment count on Inputs; the match and the booking run once per business day from AceDataReady",
     "rwb.payment.events.v1", "rwb-payment",
     "rwb-case, rwb-treatment, rwb-comms, rwb-asset, rwb-debtsale, rwb-writeoff, rwb-guarantee"),
    ("P9", "rwb-reporting", 1,
     "Measures published at 01:30 (JOB-15) and the regulatory extract",
     1, "measure publish a day",
     "Slide 44 JOB-15; the dashboard and report read volume is not specified (CG-B-DATA-26-5; ASM-B-DATA-26-5)",
     "rwb.reporting.events.v1", "rwb-reporting", NS4),
    ("P10", "rwb-agent", 1,
     "Agent runs: screening on CaseCreated and classification on DocumentStored (AgentRunWorkflow)",
     "=('Five years'!C5+'Five years'!E5)/12", "agent runs a month",
     "Five years!C5 and E5 / 12; one run for each new case and one for each document (slide 16)",
     "rwb.agent.events.v1", "rwb-agent",
     "rwb-decision, rwb-document, rwb-deviation"),
    ("S1", "rwb-valuation", 3,
     "Appraisals and the D6 route decision (RouteDecisionWorkflow) for each new case",
     "='Five years'!C5*0.5/12", "valuations a month",
     "ACE growth!B6 basis: one appraisal for every second new case",
     "rwb.valuation.events.v1", "rwb-valuation", "rwb-case"),
    ("S2", "rwb-treatment", 2,
     "Accounts under restructure monitored and the treatment plans (TreatmentWorkflow)",
     "=Inputs!C30", "accounts under restructure",
     "Inputs!C30, a stock at 30 June 2026, not a monthly flow",
     "rwb.treatment.events.v1", "rwb-treatment",
     "rwb-comms, rwb-payment"),
    ("S3", "rwb-guarantee", 3,
     "Guarantee and insurance claims and guarantor notices (GuaranteeClaimWorkflow)",
     NS5, "claims a month",
     "No guarantee count on Inputs or Route activity",
     "rwb.guarantee.events.v1", "rwb-guarantee",
     "rwb-case, rwb-reporting"),
    ("S4", "rwb-litigation", 3,
     "Lawsuits filed and the hearings that follow (LitigationWorkflow, years)",
     "=Inputs!C24", "lawsuits a month",
     "Inputs!C24; two hearings for each lawsuit (ACE growth!B11 basis)",
     "rwb.litigation.events.v1", "rwb-litigation",
     "rwb-asset, rwb-case"),
    ("S5", "rwb-asset", 2,
     "Vehicles repossessed, properties taken on, held and sold (AssetDisposalWorkflow)",
     "=Inputs!C25", "assets a month",
     "Inputs!C25 a month; holdings Inputs!C27 and property sales Inputs!C28",
     "rwb.asset.events.v1", "rwb-asset",
     "rwb-case, rwb-payment"),
    ("S6", "rwb-debtsale", 3,
     "Accounts sold in debt sales, with lots, bids and the award (DebtSaleWorkflow, saga)",
     "='Route activity'!B9", "accounts a month",
     "Route activity!B9 (Inputs!C29 / 12); the number of lots is not specified (CG-B-DATA-26-5; ASM-B-DATA-26-5)",
     "rwb.debtsale.events.v1", "rwb-debtsale",
     "rwb-case, rwb-payment, rwb-reporting"),
    ("S7", "rwb-writeoff", 4,
     "Write-offs scanned monthly (JOB-16) and posted (WriteOffWorkflow)",
     "='Five years'!C5*0.3/12", "write-offs a month",
     "ACE growth!B13 basis: three write-offs for every ten new cases",
     "rwb.writeoff.events.v1", "rwb-writeoff",
     "rwb-case, rwb-payment, rwb-reporting"),
    ("S8", "rwb-deviation", 2,
     "Deviation screening after CaseCreated and AceDataReady (DeviationWorkflow)",
     "='Five years'!C5/12", "screenings a month",
     "One screening for each new case (slide 15); the share of cases that raise a deviation is not specified (CG-B-DATA-26-5; ASM-B-DATA-26-5)",
     "rwb.deviation.events.v1", "rwb-deviation",
     "rwb-case, rwb-comms, rwb-treatment"),
    ("S9", "rwb-partner", 4,
     "Partner users served through the partner gateway (InstructionWorkflow, SLA timers)",
     "=Inputs!C33", "partner users",
     "Inputs!C33; the instruction and result volume is not specified (CG-B-DATA-26-5; ASM-B-DATA-26-5)",
     "rwb.partner.events.v1", "rwb-partner",
     "partner portal; rwb-litigation, rwb-asset, rwb-case"),
]

CHECKS_HEAD = ["", "", "", "Item", "Value", "Unit", "Check"]
CHECKS = [
    ("New cases a month, 2027", "='Five years'!C5/12", "cases a month",
     "Equals the P3 row; slide 48 states 3,110 a month, higher because the source divides accounts by 1.2 (CG-B-DATA-26-6; ASM-B-DATA-26-6)"),
    ("Documents a month, 2027", "='Five years'!E5/12", "documents a month",
     "Equals the P5 row; slide 48 gives 64-74k, the same range"),
    ("Decision-log entries a month, 2027", "='Five years'!H5/12", "entries a month",
     "Equals the P7 row; slide 48 gives 55-62k, slightly below the computed rate (CG-B-DATA-26-6; ASM-B-DATA-26-6)"),
    ("Rule evaluations a month, 2027", "='Five years'!D5*Inputs!C21", "evaluations a month",
     "Evaluated inside the owning service, never on a shared rule server (DP-04); slide 48 gives 283-318k, slightly below the computed rate (CG-B-DATA-26-6; ASM-B-DATA-26-6)"),
    ("Peak requests a second", "='Users and load'!E8", "requests a second",
     "Slide 48 gives about 21; the two agree"),
    ("Events a day across the 19 topics", "Tens of thousands", "events",
     "Architecture v5 slide 21 note; the capacity is to confirm with the ACE platform team (CG-B-DATA-26-4; ASM-B-DATA-26-4)"),
    ("Task queues", 19, "queues", "One per service in namespace rwb-recovery"),
    ("Topics", 20, "topics", "19 rwb.<name>.events.v1 plus the shared rwb.decision-record.v1"),
]

sv = [
    ["Service volumes, 2027 (D-RCV-60)"],
    ["The forecast on the other sheets, split by the service that owns each driver. Every figure is a cell on Inputs, Monthly, "
     "Five years or Route activity, so the totals on those sheets do not move. Owner, topic and queue come from the Ownership "
     "Map v1 sheet Services; the wave is the Arch v5 wave. No driver is shared between two services."],
    [],
    HEAD_SV,
]
sv += [list(r) for r in SERVICES]
sv += [
    [],
    ["Totals and cross-checks"],
    CHECKS_HEAD,
]
sv += [["", "", ""] + list(r) for r in CHECKS]

# ---------------------------------------------------------------- Topics and queues
TOPIC_HEAD = ["Topic", "Producer", "Events published", "Partitions", "Replication factor", "Retention",
              "Record key", "Consumer groups", "Retry", "Dead letter"]
RETRY = "1 min, 10 min, 1 h"
HOT = "05:00-07:00 chain (hot)"

TOPICS = [
    ("rwb.source-data.events.v1", "P1 rwb-source-data", "AceDataReady, AceDataLate (05:30)",
     "rwb-case, rwb-payment, rwb-deviation, rwb-writeoff"),
    ("rwb.integration.events.v1", "P2 rwb-integration", "FileDelivered, FileFailed",
     "the service that requested the file"),
    ("rwb.case.events.v1", "P3 rwb-case",
     "CaseCreated, CaseAllocated, CaseAllocationFailed, CaseTransferred, CaseStateChanged, TimerBreached",
     "rwb-agent, rwb-deviation, rwb-reporting; gateway-bff (inbox)"),
    ("rwb.access.events.v1", "P4 rwb-access", "AccessPolicyChanged, DoaLimitChanged",
     "all 19 services (cache refresh)"),
    ("rwb.document.events.v1", "P5 rwb-document", "DocumentStored, DocumentFieldsExtracted",
     "rwb-agent, rwb-case"),
    ("rwb.comms.events.v1", "P6 rwb-comms", "NoticeGenerated, NoticeDispatched, NoticeDelivered",
     "rwb-decision, rwb-reporting, rwb-litigation, rwb-guarantee, rwb-case"),
    ("rwb.decision.events.v1", "P7 rwb-decision", "ApprovalRequested, ApprovalDecided, RulePackageInForce",
     "gateway-bff (inbox); rwb-case, rwb-valuation, rwb-treatment, rwb-payment"),
    ("rwb.payment.events.v1", "P8 rwb-payment", "TreatmentBooked, PaymentMissed, ProceedsMatched",
     "rwb-case, rwb-treatment, rwb-comms, rwb-asset, rwb-debtsale, rwb-writeoff, rwb-guarantee"),
    ("rwb.reporting.events.v1", "P9 rwb-reporting", "ReportPublished", NS4),
    ("rwb.agent.events.v1", "P10 rwb-agent", "AgentRunCompleted",
     "rwb-decision, rwb-document, rwb-deviation"),
    ("rwb.valuation.events.v1", "S1 rwb-valuation", "RouteDecided", "rwb-case"),
    ("rwb.treatment.events.v1", "S2 rwb-treatment", "TreatmentApproved, TreatmentClosed",
     "rwb-comms, rwb-payment"),
    ("rwb.guarantee.events.v1", "S3 rwb-guarantee", "GuaranteeClaimFiled, GuaranteeClaimSettled",
     "rwb-case, rwb-reporting"),
    ("rwb.litigation.events.v1", "S4 rwb-litigation", "LawsuitFiled, JudgmentRecorded, AuctionResult",
     "rwb-asset, rwb-case"),
    ("rwb.asset.events.v1", "S5 rwb-asset", "AssetTakenOn, AssetSold", "rwb-case, rwb-payment"),
    ("rwb.debtsale.events.v1", "S6 rwb-debtsale", "LotAwarded, AccountsTransferred",
     "rwb-case, rwb-payment, rwb-reporting"),
    ("rwb.writeoff.events.v1", "S7 rwb-writeoff", "WriteOffApproved",
     "rwb-case, rwb-payment, rwb-reporting"),
    ("rwb.deviation.events.v1", "S8 rwb-deviation", "DeviationRaised, DeviationCleared",
     "rwb-case, rwb-comms, rwb-treatment"),
    ("rwb.partner.events.v1", "S9 rwb-partner", "InstructionIssued, PartnerResultSubmitted",
     "partner portal; rwb-litigation, rwb-asset, rwb-case"),
    ("rwb.decision-record.v1 (shared)", "all 19 services", "DecisionRecorded",
     "rwb-decision, rwb-reporting"),
]

QUEUE_HEAD = ["Task queue", "Service", "Wave", "Workflows on the queue", "Activities",
              "Schedules and event-started work", "Scale note"]
QUEUES = [
    ("rwb-source-data", "P1 rwb-source-data", 1, "AceIngestCheck, reconciliation",
     "listEligibleAccounts, snapshot(page)", "JOB-04 started by AceDataReady",
     "Snapshot pages for the 01:30 measures and for the composite screens"),
    ("rwb-integration", "P2 rwb-integration", 1, "none (activities only)",
     "deliverFile(manifest), receiveFile", "JOB-10 file window at 16:00 from Airflow; buyer files per lot",
     "One file a day plus one for each lot"),
    ("rwb-case", "P3 rwb-case", 1, "CaseWorkflow (parent, one per case), DailyCaseRun",
     "allocate, transfer, rebalance",
     "JOB-02 and JOB-03 from AceDataReady, JOB-06 rebalancing 06:30", HOT),
    ("rwb-access", "P4 rwb-access", 1, "none", "authorise, permission cache refresh",
     "JOB-18 access review, six-monthly", "Light: cached permission reads"),
    ("rwb-document", "P5 rwb-document", 1, "DocumentIntakeWorkflow",
     "OCR, classify, extract, generate, seal",
     "JOB-12 intake every 15 min, JOB-17 retention monthly",
     "OCR target 500 pages an hour; KEDA on backlog"),
    ("rwb-comms", "P6 rwb-comms", 1, "NoticeDispatchWorkflow",
     "generate letter (P5), approval child (P7), deliverFile (P2)",
     "JOB-10 notices at 16:00", "Burst at 16:00"),
    ("rwb-decision", "P7 rwb-decision", 1, "ApprovalWorkflow", "rule governance, ledger seal (WORM)",
     "JOB-20 rule promote 00:01, JOB-14 chain check 02:00, JOB-13 continuous ingest",
     "Steady; DecisionRecorded collected within 5 minutes"),
    ("rwb-payment", "P8 rwb-payment", 2, "none (activities only)",
     "matchPayments, confirmBookings, postProceeds",
     "JOB-07 and JOB-08 from AceDataReady", HOT),
    ("rwb-reporting", "P9 rwb-reporting", 1, "none (Schedule)", "buildRegulatoryExtract",
     "JOB-15 measures at 01:30, Airflow trigger", "One publish a day"),
    ("rwb-agent", "P10 rwb-agent", 1, "AgentRunWorkflow",
     "screening, classification and extraction runs, 60 s then rule result",
     "Started by CaseCreated and DocumentStored", "Bursty; 60 s cap per run"),
    ("rwb-valuation", "S1 rwb-valuation", 3, "RouteDecisionWorkflow",
     "valuation, route agent child, approval child", "Child of the case", "One per new case"),
    ("rwb-treatment", "S2 rwb-treatment", 2, "TreatmentWorkflow", "settlement and DIL sagas, postProceeds step",
     "Child of the case; plan timers as durable timers", "Long-running"),
    ("rwb-guarantee", "S3 rwb-guarantee", 3, "GuaranteeClaimWorkflow", "guarantor notice child, approval child",
     "Child of the case", "Low volume"),
    ("rwb-litigation", "S4 rwb-litigation", 3, "LitigationWorkflow", "issueInstruction (law firm), demand notice",
     "Child of the case, years; continues-as-new", "Longest-running workflows"),
    ("rwb-asset", "S5 rwb-asset", 2, "AssetDisposalWorkflow", "issueInstruction (auction vendor), postProceeds",
     "JOB-19 re-appraisal monthly", "Monthly peaks"),
    ("rwb-debtsale", "S6 rwb-debtsale", 3, "DebtSaleWorkflow (saga, pivot = transfer)",
     "deliverFile (buyer file), postProceeds", "Per lot", "Per lot, not daily"),
    ("rwb-writeoff", "S7 rwb-writeoff", 4, "WriteOffWorkflow", "committee approval child, postProceeds",
     "JOB-16 scan, monthly on the 3rd working day", "Monthly peak"),
    ("rwb-deviation", "S8 rwb-deviation", 2, "DeviationWorkflow", "screening agent child",
     "Started by CaseCreated and AceDataReady", "Can start at any time; pauses the stage clock"),
    ("rwb-partner", "S9 rwb-partner", 4, "InstructionWorkflow", "issueInstruction, recordResult",
     "Per instruction", "SLA timers on the partner gateway"),
]

PLATFORM = [
    ["Platform settings"],
    ["Item", "Value", "Note"],
    ["Temporal namespace", "rwb-recovery",
     "One task queue per service; the ACE namespace ace-collection is reached through Nexus (restructure calculator)"],
    ["Temporal cluster", "Shared with ACE, one per environment",
     "Own persistence database; workers scaled by KEDA on backlog (ADR-016)"],
    ["Partitions", 12, "Every business-event topic (slide 34)"],
    ["Replication factor", 3, "Every business-event topic (slide 34)"],
    ["Retention", "7 days", "Replay for a new or repurposed service (slide 21)"],
    ["Record key", "caseId", "One case's events stay in order (slide 21)"],
    ["Envelope", "CloudEvents 1.0, Kafka binary mode",
     "ce_id, ce_type, ce_source, ce_subject and traceparent headers; JSON body against the registry, BACKWARD (ADR-015)"],
    ["Delivery", "Outbox in the producer, inbox in each consumer",
     "Exactly-once effect from at-least-once delivery (DP-09, RWB-PLT-TE006)"],
    ["Dead letter", "<topic>.dlt", "After the three retries; alerts the owning service"],
    ["Capacity", "Tens of thousands of events a day",
     "Small; the platform team confirms the quota (CG-B-DATA-26-4; ASM-B-DATA-26-4)"],
    ["Shared topic", "rwb.decision-record.v1",
     "DecisionRecorded from all 19 services into the central ledger in rwb-decision (DP-03, ADR-022)"],
]

tq = [
    ["Topics and queues (D-RCV-60)"],
    ["Every service has one business-event topic and one Temporal task queue; the decision record has one shared topic. "
     "Names follow DP-14 and the service table in Template and Rules R4. Settings are Architecture v5 slide 34 (12 partitions, "
     "replication factor 3, 7 days, key caseId, retry 1 min, 10 min, 1 h, then .dlt) and the event catalogue on slides 42 and 43."],
    [],
    ["Business-event topics"],
    TOPIC_HEAD,
]
tq += [[t, p, e, 12, 3, "7 days", "caseId", c, RETRY, t.split(" (")[0] + ".dlt"] for t, p, e, c in TOPICS]
tq += [[], ["Task queues"], QUEUE_HEAD]
tq += [list(r) for r in QUEUES]
tq += [[]]
tq += PLATFORM

# ---------------------------------------------------------------- Read me
READ_ME = [
    ["SCB Collections and Recovery. Henka Group, 22 November 2026."],
    ["(C) Siam Commercial Bank and Henka Pte Ltd"],
    [],
    ["Recovery Workbench Volume and Scale Forecast v4"],
    ["Next version of 06 Data/Recovery Workbench Volume and Scale Forecast v3.xlsx. Decision D-RCV-60 "
     "(adopt Architecture v5 and realign the documents and stories)."],
    ["Every figure, ID, unit and date of v3 is kept. The realignment adds the per-service volumes, topics and queues, "
     "and changes five cells whose wording was written for one monolith."],
    [],
    ["Change log"],
    ["v4, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash"],
    [],
    ["What changed in v4"],
    ["Service volumes (new sheet): 19 rows, one per owning service, each with its driver, the 2027 volume, the unit, the "
     "basis cell in this workbook, its topic, its task queue and its consumers. No driver is shared, so the totals on "
     "Inputs, Monthly, Five years and Route activity do not move (CG-B-DATA-26-1; ASM-B-DATA-26-1)."],
    ["Topics and queues (new sheet): the 19 service topics plus the shared rwb.decision-record.v1 with partitions, "
     "replication, retention, record key, consumer groups, retry and dead letter; then the 19 task queues with their "
     "workflows, activities, Schedules and scale note; then the platform settings (CG-B-DATA-26-4; ASM-B-DATA-26-4)."],
    ["Read path!A2: only rwb-source-data holds the grant on the 30 recovery.v_ace_* views; every other service asks P1 "
     "(CG-B-DATA-26-2; ASM-B-DATA-26-2)."],
    ["Read path!C15: the lake refresh is gone; the three Workbench jobs are case creation and allocation (JOB-02, JOB-03), "
     "reconciliation (JOB-04) and the WIN notice file (JOB-10), each a Temporal Schedule or an event-started workflow in "
     "its own service (CG-B-DATA-26-3; ASM-B-DATA-26-3)."],
    ["Read path!C16 and Inputs!G7: the freshness stamp and the v_ace_account read are named against rwb-source-data "
     "(CG-B-DATA-26-2; ASM-B-DATA-26-2)."],
    ["Key!C10: a view read is a SELECT by rwb-source-data on behalf of a screen or a workflow, not a read by the "
     "Workbench or by a lake refresh (CG-B-DATA-26-2; ASM-B-DATA-26-2)."],
    [],
    ["What did not change"],
    ["Inputs: 34 rows, I01 to I34, with every value, unit, kind, source and effect unchanged."],
    ["Monthly (14 months), Five years (2027 to 2031), Users and load, ACE growth (the 14 tables and 12 columns), Route "
     "activity and Key: every formula, figure and label unchanged."],
    ["The 14 new ACE tables and 12 columns of ACE growth, the account inventory on Inputs (I01 to I07), the 173,807 "
     "restructure accounts (I26) and the document storage on Five years keep the values v3 carries."],
    ["The source holds no release date, so no date is marked (tentative) and no date is raised as a gap: the dates in "
     "the workbook are bank data dates (30 June 2026, 6 July 2026, the July 2025 to June 2026 averages) and they are "
     "copied unchanged."],
    [],
    ["Sheets"],
    ["Read me, Inputs, Monthly, Five years, Users and load, Read path, Service volumes, Topics and queues, ACE growth, "
     "Route activity, Key."],
    [],
    ["Open register rows"],
    ["CG-B-DATA-26-1 / ASM-B-DATA-26-1: the forecast is written for one monolith; the per-service volumes are new."],
    ["CG-B-DATA-26-2 / ASM-B-DATA-26-2: one service reads the ACE views, not the Workbench."],
    ["CG-B-DATA-26-3 / ASM-B-DATA-26-3: the lake refresh is gone and the three jobs are Schedules in their own services."],
    ["CG-B-DATA-26-4 / ASM-B-DATA-26-4: the source has no topic, partition, retention or consumer figures."],
    ["CG-B-DATA-26-5 / ASM-B-DATA-26-5: no demand figure for payment, guarantee, partner instructions, the report read "
     "volume, the number of lots or the deviation share."],
    ["CG-B-DATA-26-6 / ASM-B-DATA-26-6: Arch v5 slide 48 states 3,110 new cases a month; the source computes cases as "
     "accounts divided by 1.2, which is lower, and the document, entry and evaluation totals follow it. The source "
     "formula is kept."],
    ["CG-B-DATA-26-7 / ASM-B-DATA-26-7: three scheduled Workbench jobs in v3 against the 21 jobs of the Arch v5 job map."],
    [],
    ["Counts"],
    ["19 services: 10 platform (P1 to P10) and 9 route (S1 to S9); 20 topics (19 service topics plus the shared "
     "rwb.decision-record.v1); 19 task queues."],
    ["Changed v3 cells: 5 (Read path!A2, C15, C16; Inputs!G7; Key!C10). Appended: Service volumes 19 rows and 8 check "
     "rows; Topics and queues 20 topic rows, 19 queue rows and 11 platform rows."],
    ["Candidate gap rows: 7, CG-B-DATA-26-1 to CG-B-DATA-26-7. Candidate assumption rows: 7, ASM-B-DATA-26-1 to "
     "ASM-B-DATA-26-7. Numbering to GAP-nnnn and ASM-nnnn is left to step D1."],
]

for name, rows in (("rows_service_volumes.json", sv), ("rows_topics_queues.json", tq), ("rows_read_me.json", READ_ME)):
    (DOCS / name).write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
    print("wrote", name, len(rows), "rows")
