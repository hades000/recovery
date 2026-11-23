"""Build Recovery Workbench Temporal Workflow and Activity Catalog v1 (new document)."""
import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
P = ROOT / "05 Technical architecture" / "Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx"

NAVY = PatternFill("solid", fgColor="1F3864")
H = dict(font=Font(bold=True, color="FFFFFF"), fill=NAVY,
         alignment=Alignment(wrap_text=True, vertical="top"))

PL_SCHED = "Not specified in the source documents (CG-B-ARCH-WF-1; ASM-B-ARCH-WF-8)"
PL_TO = "Not specified in the source documents (CG-B-ARCH-WF-2; ASM-B-ARCH-WF-10)"
PL_PAY = "Not specified in the source documents (CG-B-ARCH-WF-3; ASM-B-ARCH-WF-6)"
PL_WF4 = "Not specified in the source documents (CG-B-ARCH-WF-4; ASM-B-ARCH-WF-7)"

SERVICES = [
    ("P1", "rwb-source-data", "Source data"), ("P2", "rwb-integration", "Integration"),
    ("P3", "rwb-case", "Case and workflow"), ("P4", "rwb-access", "Access and authority"),
    ("P5", "rwb-document", "Document"), ("P6", "rwb-comms", "Communications"),
    ("P7", "rwb-decision", "Decision and rules"), ("P8", "rwb-payment", "Payment"),
    ("P9", "rwb-reporting", "Reporting"), ("P10", "rwb-agent", "Agent"),
    ("S1", "rwb-valuation", "Valuation and route"), ("S2", "rwb-treatment", "Treatment and offer"),
    ("S3", "rwb-guarantee", "Guarantee"), ("S4", "rwb-litigation", "Litigation"),
    ("S5", "rwb-asset", "Asset"), ("S6", "rwb-debtsale", "Debt sale"),
    ("S7", "rwb-writeoff", "Write-off"), ("S8", "rwb-deviation", "Deviation"),
    ("S9", "rwb-partner", "Partner"),
]

WF_HEAD = ["Workflow", "Kind", "Owner (code)", "Service", "Task queue", "Started by", "Steps (from the source)",
           "Hands back", "Activities called", "History, versioning and limits", "Source"]

WORKFLOWS = [
    ("CaseWorkflow", "Parent workflow, one per case", "P3", "rwb-case", "rwb-case",
     "The case router in rwb-case: the inbox consumes the case event and calls signalWithStart; workflow ID = case ID (Temporal design slide 13; ADR-011 writes case-{caseId}, see CG-B-ARCH-WF-7)",
     "Tracks the case from entry to closure, forwards every event to the running stage child, and starts one child workflow per stage; the four steps repeat: receive, ask Drools, record and apply, wait",
     "- (the parent stays until the case closes)",
     "EvaluateRules, RecordAndApply; starts one stage child per stage",
     "Continue-As-New at every stage end and at least every 28 days; children use parent close policy ABANDON; search attributes CaseId, Stage, ProductGroup, QueueCode",
     "Temporal design slide 13; Arch v5 slide 14"),
    ("DailyCaseRun", "Event-started workflow (a Schedule is named beside it)", "P3", "rwb-case", "rwb-case",
     "AceDataReady, published when the business date is signalled (JOB-02); Architecture v5 slide 14 also names a Schedule (CG-B-ARCH-WF-5; ASM-B-ARCH-WF-11)",
     "Creates cases for accounts that reached 90 days past due and attaches history (JOB-02); places new cases in queues and gives owners by rule (JOB-03) by 07:00",
     "CaseCreated, CaseAllocated, CaseAllocationFailed",
     "EvaluateRules, RecordAndApply; allocate, transfer, rebalance",
     "One run per business date; workflow ID not specified (CG-B-ARCH-WF-1; ASM-B-ARCH-WF-8)",
     "Arch v5 slides 14 and 44; Temporal design slide 14"),
    ("RouteDecisionWorkflow", "Stage child workflow", "S1", "rwb-valuation", "rwb-valuation",
     "The case reaches route decision D6, or the case is reopened (ROUTE_D6_REOPEN); started by CaseWorkflow as a child",
     "1 order the appraisal if stale; 2 read the value and flag outliers; 3 the case owner accepts the value; 4 return by route and payoff; 5 the route agent recommends; 6 approve within the delegated limit or at committee; 7 start route R1 to R8 and its timers",
     "RouteDecided to rwb-case",
     "EvaluateRules, RecordAndApply; child AgentRunWorkflow (route agent); child ApprovalWorkflow (DoA)",
     "Continue-As-New at stage end and at least every 28 days",
     "Temporal design slide 17; Arch v5 slide 18"),
    ("TreatmentWorkflow", "Stage child workflow", "S2", "rwb-treatment", "rwb-treatment",
     "ROUTE_APPROVED with route R1 (restructure), R2 (settlement) or R3 (deed in lieu)",
     "1 COLLINS proposal; 2 FCR officer review, 2 working days; 3 ACE affordability check; 4 offer sent, valid 14 days; 5 customer signs and ops books; 6 payment-plan timers; 7 a missed payment starts the cure period",
     "TreatmentApproved, TreatmentClosed; a broken plan returns the case to D6",
     "EvaluateRules, RecordAndApply; child ApprovalWorkflow; child Document (contract, e-sign); Payment postProceeds; Nexus restructure calculator in ace-collection; settlement and deed in lieu run as sagas on the kit Saga runner",
     "Continue-As-New at stage end and at least every 28 days",
     "Temporal design slide 18; Arch v5 slide 18"),
    ("GuaranteeClaimWorkflow", "Stage child workflow", "S3", "rwb-guarantee", "rwb-guarantee",
     "A guarantee is found at takeover and the claim deadline timer starts (R-GUA-01)",
     "1 claim deadline timer; 2 the agent assembles the claim; 3 officer approves, 3 working days; 4 submit to TCG; 5 query, part pay or reject; 6 paid: record subrogation; 7 residual back to D6",
     "GuaranteeClaimFiled, GuaranteeClaimSettled",
     "EvaluateRules, RecordAndApply; child ApprovalWorkflow; child NoticeDispatchWorkflow (guarantor notice)",
     "Continue-As-New at stage end and at least every 28 days",
     "Temporal design slide 19; Arch v5 slide 18"),
    ("LitigationWorkflow", "Stage child workflow", "S4", "rwb-litigation", "rwb-litigation",
     "Litigation route approved (R-LIT-01), or a restructure or settlement plan breaks (R-LIT-02)",
     "1 notices generated and sent; 2 notice period starts on proof of delivery; 3 pack checked for defects; 4 law firm chosen and instructed; 5 filing, hearings, judgment; 6 asset trace and writ, 10 working days; 7 auction 100/90/80/70%",
     "LawsuitFiled, JudgmentRecorded, AuctionResult",
     "EvaluateRules, RecordAndApply; Partner issueInstruction (law firm); child NoticeDispatchWorkflow (demand notice); child ApprovalWorkflow",
     "Runs for years; Continue-As-New at stage end and at least every 28 days",
     "Temporal design slide 20; Arch v5 slide 19"),
    ("AssetDisposalWorkflow", "Stage child workflow", "S5", "rwb-asset", "rwb-asset",
     "An asset is taken on from repossession, deed in lieu or LED (R-DIS-01/02/03, EV-22)",
     "1 holding age and provisions; 2 re-appraise at 12 months (JOB-19); 3 the pricing agent recommends; 4 floor approved and listed; 5 rounds step to the floor; 6 buyer pays in 5 days; 7 title transfer and proceeds",
     "AssetTakenOn, AssetSold",
     "EvaluateRules, RecordAndApply; Partner issueInstruction (auction vendor); child ApprovalWorkflow; Payment postProceeds",
     "Continue-As-New at stage end and at least every 28 days",
     "Temporal design slide 21; Arch v5 slide 19"),
    ("DebtSaleWorkflow", "Stage child workflow (saga)", "S6", "rwb-debtsale", "rwb-debtsale",
     "The monthly sale cycle opens, or a residual arrives from disposal (R-DS-01)",
     "1 select accounts; 2 lot priced, committee 5 working days; 3 masked tape and data room; 4 buyer KYC and licence, 3 working days; 5 award against reserve and cap; 6 settle, transfer and post GL; 7 sold: close the case",
     "LotAwarded, AccountsTransferred",
     "EvaluateRules, RecordAndApply; Document data-room pack; child ApprovalWorkflow; Integration deliverFile (buyer file); Payment postProceeds; kit Saga runner with the pivot at transfer, in strict mode",
     "Continue-As-New at stage end and at least every 28 days; strict mode waits for the central ledger",
     "Temporal design slide 22; Arch v5 slide 19"),
    ("WriteOffWorkflow", "Stage child workflow (saga)", "S7", "rwb-writeoff", "rwb-writeoff",
     "JOB-16 on the third working day after AceDataReady (R-WO-01)",
     "1 scan proposes the population; 2 pack built in 3 working days; 3 committee decides; 4 post to ALS and GL; 5 release provision and feed; 6 agency or sale after; 7 retention then close (JOB-17)",
     "WriteOffApproved",
     "EvaluateRules, RecordAndApply; child ApprovalWorkflow (committee); Payment postProceeds; strict mode at the posting",
     "Continue-As-New at stage end and at least every 28 days; strict mode waits for the central ledger",
     "Temporal design slide 23; Arch v5 slide 20"),
    ("DeviationWorkflow", "Stage child workflow, may start at any time", "S8", "rwb-deviation", "rwb-deviation",
     "An agent or officer flags it (EV-06 starts screening), or universal rules R-UNI-04 to 09 fire",
     "1 flag raised the same day; 2 pause the stage clock only; 3 route to the owner by code; 4 stop contact for X1 to X3; 5 the owner works the case; 6 resume or re-route; 7 escalate after 10 working days",
     "DeviationRaised, DeviationCleared; CaseWorkflow pauses and resumes the stage clock",
     "EvaluateRules, RecordAndApply; child AgentRunWorkflow (screening agent run)",
     "Continue-As-New at stage end and at least every 28 days; the prescription clock never pauses",
     "Temporal design slide 24; Arch v5 slide 15"),
    ("InstructionWorkflow", "Domain workflow on the kit (partner instruction)", "S9", "rwb-partner", "rwb-partner",
     "A case needs a law firm, auction vendor, collection agency or valuer",
     "1 onboard the partner and terms; 2 the scorecard picks the partner; 3 instruction sent and the partner clock starts; 4 result through the portal the same day; 5 no reply: chase, then recall; 6 fees approved; 7 monthly scorecard, exit",
     "No event of its own; the result returns to the calling workflow as the activity result",
     "EvaluateRules, RecordAndApply; issueInstruction, recordResult; kit SLA timers",
     "Kit template with SLA timers; stage end and at least every 28 days",
     "Temporal design slide 25; Arch v5 slide 17"),
    ("ApprovalWorkflow", "Kit template (maker-checker, DoA lookup as a parameter)", "P7", "rwb-decision", "rwb-decision",
     "A stage workflow that needs a DoA approval, as a child; or rule sign-off inside rwb-decision",
     "Maker-checker approval with the DoA limit read through the rwb-access contract; approver, level and final call are written on the decision record",
     "ApprovalDecided",
     "EvaluateRules, RecordAndApply; DoA limits from rwb-access",
     "Kit template; Continue-As-New at stage end and at least every 28 days",
     "Arch v5 slides 14 and 17; Temporal design slide 12"),
    ("NoticeDispatchWorkflow", "Kit template (notify)", "P6", "rwb-comms", "rwb-comms",
     "A notice request (POST /notices), or a stage workflow that needs a letter",
     "Generate the letter in rwb-document; approve the notice where a rule requires it; dispatch through ACE (SMS, LINE) or as a WIN file through rwb-integration deliverFile",
     "NoticeGenerated, NoticeDispatched, NoticeDelivered",
     "EvaluateRules, RecordAndApply; Document generate; child ApprovalWorkflow; Integration deliverFile",
     "Kit template; Continue-As-New at stage end and at least every 28 days",
     "Arch v5 slide 17; Temporal design slide 12"),
    ("DocumentIntakeWorkflow", "Workflow started by an event, with KEDA workers", "P5", "rwb-document", "rwb-document",
     "An event from the scanner folder, SFTP or mailbox pickup (JOB-12), or a child start from a stage workflow",
     "OCR, classify and extract; then generate and seal; custody in Azure Blob (WORM)",
     "DocumentStored, DocumentFieldsExtracted",
     "EvaluateRules, RecordAndApply; generate, seal; child AgentRunWorkflow (classify and extract run)",
     "Continue-As-New at stage end and at least every 28 days; KEDA scales workers on backlog",
     "Arch v5 slide 16; Temporal design slide 12"),
    ("AgentRunWorkflow", "Kit template (agent run with rule fallback)", "P10", "rwb-agent", "rwb-agent",
     "DocumentStored (classification) or CaseCreated (screening); started as a child by a stage workflow for the route agent or the pricing agent",
     "The agent runs with read-only tool calls; after 60 s the rule result is used (R-UNI-32)",
     "AgentRunCompleted",
     "EvaluateRules, RecordAndApply; read-only tool gateway calls (the source names the gateway and not the activity)",
     "60 s limit before the rule fallback; Continue-As-New at stage end and at least every 28 days",
     "Arch v5 slide 16; Temporal design slides 12 and 28"),
    ("PlatformSmokeWorkflow", "Platform workflow", "PLT", "PLT platform", "rwb-platform",
     "Schedule smoke workflow at 06:00 (JOB-22), as platform-smoke-{yyyymmdd} on rwb-platform",
     "Runs the daily journey smoke across the services (JOB-22)",
     "A smoke result; when none is produced the platform administrator is alerted",
     PL_WF4 + "(the source names the smoke run and not what it calls)",
     "One run per day; workflow ID platform-smoke-{yyyymmdd}",
     "Arch v5 slide 44; Batch v4 JOB-22; Temporal design slide 31"),
    ("AceIngestCheck", "Workflow", "P1", "rwb-source-data", "rwb-source-data",
     "POST /business-days/{date}/ready from Airflow (idempotent)",
     "Checks the freshness of the ACE data for the business date and publishes AceDataReady; raises AceDataLate at 05:30 with an alarm and a banner",
     "AceDataReady, AceDataLate",
     PL_WF4 + "(the source names the workflow and not its activities)",
     "One run per business date",
     "Arch v5 slides 15, 31 and 32"),
    ("reconciliation", "Workflow", "P1", "rwb-source-data", "rwb-source-data",
     "AceDataReady",
     "Reconciles accounts at 90 days past due against open cases and balances against the core bank (JOB-04); breaks are listed for the data steward",
     "The break list for the data steward; no event of its own is stated in the source",
     PL_WF4 + "(the source names the workflow and not its activities)",
     "One run per business date",
     "Arch v5 slide 15; Batch v4 JOB-04"),
    (PL_PAY, "Event-started workflow", "P8", "rwb-payment", "rwb-payment",
     "AceDataReady, after JOB-02",
     "Runs the matchPayments activity: matches payments to plans and settlements and raises missed payments (JOB-07)",
     "PaymentMissed, TreatmentBooked",
     "EvaluateRules, RecordAndApply; matchPayments",
     "One run per business date; workflow name and ID not specified (CG-B-ARCH-WF-3; ASM-B-ARCH-WF-6)",
     "Arch v5 slides 17 and 44; Temporal design slide 14"),
    (PL_PAY, "Event-started workflow", "P8", "rwb-payment", "rwb-payment",
     "AceDataReady, after JOB-02",
     "Runs the confirmBookings activity: matches approved treatments to bookings in the ACE account view through the rwb-source-data contract (JOB-08)",
     "TreatmentBooked, ProceedsMatched",
     "EvaluateRules, RecordAndApply; confirmBookings",
     "One run per business date; workflow name and ID not specified (CG-B-ARCH-WF-3; ASM-B-ARCH-WF-6)",
     "Arch v5 slides 17 and 44; Batch v4 JOB-08"),
]

ACT_HEAD = ["Activity", "Kind", "Service", "Task queue", "Purpose", "Called by", "Retry and timeout", "Source"]

RETRY = "1 s initial interval, back-off 2, 10 attempts (Temporal design slides 14 and 28)"
ACTIVITIES = [
    ("EvaluateRules", "Activity, universal in every service", "every service (19)", "rwb-<short>",
     "RuleEvaluator.evaluate(packageCode, facts, onDate) returns RuleResult(packageCode, packageVersion, ruleId, outputs); Drools runs only inside an activity, so a replay reuses the recorded result",
     "Every workflow, at each decision point", RETRY + "; NoPackageInForce is non-retryable. Start-to-close timeout and heartbeat: " + PL_TO,
     "Temporal design slides 14, 27 and 28"),
    ("RecordAndApply", "Activity, universal in every service", "every service (19)", "rwb-<short>",
     "Writes the decision record, the state change and the outbox row in one transaction (R-UNI-39); nothing moves if any part fails",
     "Every workflow, after each rule answer", RETRY + ". Start-to-close timeout and heartbeat: " + PL_TO,
     "Temporal design slides 13, 14 and 28"),
    ("listEligibleAccounts(businessDate)", "Activity", "P1", "rwb-source-data",
     "Lists the accounts eligible for a business date for case creation", "DailyCaseRun (JOB-02)",
     RETRY + ". Timeout and heartbeat: " + PL_TO, "Arch v5 slide 15"),
    ("snapshot(page)", "Activity", "P1", "rwb-source-data",
     "Reads a page of the ACE view contract for the measures and the reporting projections",
     "rwb-reporting through the P1 contract; the measures build", RETRY + ". Timeout and heartbeat: " + PL_TO,
     "Arch v5 slides 15 and 19"),
    ("allocate", "Activity", "P3", "rwb-case",
     "Places new cases in queues and gives owners by rule (JOB-03)", "DailyCaseRun",
     RETRY + ". Timeout and heartbeat: " + PL_TO, "Arch v5 slide 14"),
    ("transfer", "Activity", "P3", "rwb-case",
     "Moves a case to another queue or owner and writes CaseTransferred", "CaseWorkflow (case transfer and queue change)",
     RETRY + ". Timeout and heartbeat: " + PL_TO, "Arch v5 slides 14 and 44"),
    ("rebalance", "Activity", "P3", "rwb-case",
     "Moves cases from owners above the cap or absent (JOB-06)", "Schedule rebalancing (JOB-06)",
     RETRY + ". Timeout and heartbeat: " + PL_TO, "Arch v5 slides 14 and 44; Batch v4 JOB-06"),
    ("matchPayments", "Activity", "P8", "rwb-payment",
     "Matches payments to plans and settlements and raises missed payments (JOB-07)",
     "The event-started payment workflow of JOB-07", RETRY + ". Timeout and heartbeat: " + PL_TO,
     "Arch v5 slide 17; Temporal design slide 14"),
    ("confirmBookings", "Activity", "P8", "rwb-payment",
     "Matches approved treatments to bookings in the ACE account view (JOB-08)",
     "The event-started payment workflow of JOB-08", RETRY + ". Timeout and heartbeat: " + PL_TO,
     "Arch v5 slide 17"),
    ("postProceeds", "Activity (saga step)", "P8", "rwb-payment",
     "Posts proceeds and the GL outcome for a settlement, an auction sale, a debt sale or a write-off",
     "Settlement saga (S2), auction saga (S5), DebtSaleWorkflow (S6), WriteOffWorkflow (S7)",
     RETRY + ". At a point of no return the step waits for the central ledger. Timeout and heartbeat: " + PL_TO,
     "Arch v5 slides 18, 19, 20 and 26"),
    ("generate", "Activity", "P5", "rwb-document",
     "Generates a letter or document from a template", "NoticeDispatchWorkflow; DocumentIntakeWorkflow",
     RETRY + ". Timeout and heartbeat: " + PL_TO, "Arch v5 slide 16"),
    ("seal", "Activity", "P5", "rwb-document",
     "Seals the document and records custody and retention", "DocumentIntakeWorkflow; NoticeDispatchWorkflow",
     RETRY + ". Timeout and heartbeat: " + PL_TO, "Arch v5 slide 16"),
    ("OCR, classify, extract", "Workflow steps (the activity split is not stated)", "P5", "rwb-document",
     "Reads the scanned or received document, classifies it and extracts its fields",
     "DocumentIntakeWorkflow", PL_WF4 + "(the source names the steps OCR, classify and extract and not separate activities)",
     "Arch v5 slide 16"),
    ("deliverFile(manifest)", "Activity", "P2", "rwb-integration",
     "Delivers a file with a manifest: WIN letters, buyer files, posting files, the regulatory extract",
     "NoticeDispatchWorkflow; DebtSaleWorkflow; rwb-reporting; WriteOffWorkflow posting file",
     RETRY + ". The file is idempotent by fileId and checked by checksum. Timeout and heartbeat: " + PL_TO,
     "Arch v5 slides 16 and 19"),
    ("receiveFile", "Activity", "P2", "rwb-integration",
     "Receives an inbound file for an interface run and records the run",
     "Interface runs (GET /interface-runs, POST /interface-runs/{id}/retry)",
     RETRY + ". The file is idempotent by fileId. Timeout and heartbeat: " + PL_TO,
     "Arch v5 slide 16"),
    ("issueInstruction", "Activity", "S9", "rwb-partner",
     "Sends an instruction to a partner and starts the partner clock (EV-20)",
     "LitigationWorkflow (law firm); AssetDisposalWorkflow (auction vendor); a case that needs a valuer or an agency",
     RETRY + ". Timeout and heartbeat: " + PL_TO, "Arch v5 slides 19 and 25"),
    ("recordResult", "Activity", "S9", "rwb-partner",
     "Records the partner result, or its absence, and starts the chase and recall timers",
     "InstructionWorkflow", RETRY + ". Timeout and heartbeat: " + PL_TO, "Arch v5 slide 17; Temporal design slide 25"),
    ("buildRegulatoryExtract", "Activity", "P9", "rwb-reporting",
     "Builds the regulatory extract from the service's own projections, with no data lake",
     "The 01:30 Airflow trigger through POST /reports/{id}/run (JOB-15)",
     RETRY + ". Timeout and heartbeat: " + PL_TO, "Arch v5 slides 15, 32 and 44"),
    ("restructure calculator", "Nexus operation into another namespace", "ACE (ace-collection)", "n/a",
     "Calculates the restructure terms for a proposal",
     "TreatmentWorkflow", "n/a (Nexus call; the source gives no timeout)", "Arch v5 slides 11, 12 and 19"),
]

SCH_HEAD = ["Job", "Schedule (name in the source)", "Owner (code)", "Service", "Task queue",
            "Trigger or calendar (from the source)", "Starts", "Overlap and catch-up", "Note", "Source"]

SCHEDULES = [
    ("JOB-06", "rebalancing", "P3", "rwb-case", "rwb-case", "Daily 06:30",
     "The activity rebalance on rwb-case; the workflow it runs in is " + PL_WF4,
     "SKIP, catch-up window",
     "Moves cases from owners above the cap or absent", "Arch v5 slides 14 and 44"),
    ("JOB-10", "WIN notices", "P6", "rwb-comms", "rwb-comms", "Daily 16:00; the bank's Airflow opens the WIN file window",
     "NoticeDispatchWorkflow, then deliverFile in rwb-integration", "SKIP, catch-up window",
     "rwb-comms owns the notice and the 16:00 window; rwb-integration delivers the file (CG-A6-flows-6; ASM-A6-flows-8)",
     "Arch v5 slides 17, 31 and 44"),
    ("JOB-14", "chain check", "P7", "rwb-decision", "rwb-decision", "Daily 02:00",
     PL_WF4 + "(the source names the Schedule and not the workflow it starts)", "SKIP, catch-up window",
     "Checks the hash chain of the central ledger", "Arch v5 slides 14 and 44; Temporal design slide 16"),
    ("JOB-16", "write-off scan", "S7", "rwb-writeoff", "rwb-writeoff",
     "Monthly, 3rd working day, after AceDataReady",
     "WriteOffWorkflow", "SKIP, catch-up window",
     "A cron expression cannot express the working-day gate, so the workflow checks AceDataReady (CG-A6-flows-9; ASM-A6-flows-12)",
     "Arch v5 slides 20 and 44; Temporal design slide 23"),
    ("JOB-17", "retention", "P5", "rwb-document", "rwb-document", "Monthly, 1st Sunday",
     PL_WF4 + " (the source names the Schedule and not the workflow it starts)", "SKIP, catch-up window",
     "Lists records past retention for review", "Arch v5 slides 16 and 44"),
    ("JOB-18", "access review list", "P4", "rwb-access", "rwb-access", "Every six months",
     PL_WF4 + " (the source names the Schedule and not the workflow it starts)", "SKIP, catch-up window",
     "Produces role holder lists for recertification", "Arch v5 slides 14 and 44"),
    ("JOB-19", "re-appraisal", "S5", "rwb-asset", "rwb-asset", "Monthly",
     PL_WF4 + " (the source names the Schedule and not the workflow it starts)", "SKIP, catch-up window",
     "Raises re-appraisal orders for assets due", "Arch v5 slides 19 and 44"),
    ("JOB-20", "rule promote", "P7", "rwb-decision", "rwb-decision", "Daily 00:01",
     "The activity that sets the APPROVED versions with today's valid-from date to IN_FORCE and the previous version to SUPERSEDED, then publishes RulePackageInForce, is " + PL_WF4,
     "SKIP, catch-up window", "Owning services fetch the model, verify the checksum and swap it in",
     "Arch v5 slides 14 and 44; Temporal design slide 15"),
    ("JOB-21", "stuck workflow scan", "PLT", "PLT platform", "rwb-platform", "Every 5 minutes",
     "No workflow: a visibility query over namespace rwb-recovery, then an alert", "SKIP, catch-up window",
     "Stuck panel marked stale, incident raised, no zero published; rwb-platform has no service row (CG-B-ARCH-WF-6; ASM-B-ARCH-WF-12)",
     "Arch v5 slide 44; Batch v4 JOB-21"),
    ("JOB-22", "smoke workflow", "PLT", "PLT platform", "rwb-platform", "Daily 06:00",
     "PlatformSmokeWorkflow, as platform-smoke-{yyyymmdd}", "SKIP, catch-up window",
     "No smoke result for the day raises an alert to the platform administrator", "Arch v5 slide 44; Batch v4 JOB-22"),
]

TQ_HEAD = ["Item", "Kind", "Owner", "Value", "Note", "Source"]
QUEUES = [
    ("rwb-recovery", "Namespace", "PLT platform", "rwb-recovery",
     "One namespace per workbench: own retention, rate limits, certificates and encryption keys", "Temporal design slide 12"),
    ("Temporal cluster", "Cluster", "PLT platform",
     "One per environment on ACE AKS with its own persistence database, UI, metrics and codec server, 1.30 or later",
     "No grant on the ACE database", "Temporal design slides 11 and 12"),
]
for code, svc, name in SERVICES:
    QUEUES.append((svc, "Task queue", f"{code} {svc}", f"rwb-{svc[4:]}",
                   f"Worker of {name}; it polls only this queue and KEDA scales it on backlog", "Arch v5 slide 41; Temporal design slide 11"))
QUEUES += [
    ("rwb-platform", "Task queue", "PLT platform", "rwb-platform",
     "Platform smoke (JOB-22) and the stuck workflow scan (JOB-21); not one of the 19 service queues (CG-B-ARCH-WF-6; ASM-B-ARCH-WF-12)",
     "Batch v4 JOB-21 and JOB-22; Arch v5 slide 44"),
    ("ace-collection", "Namespace", "ACE", "ace-collection",
     "Reached through a Nexus operation (the restructure calculator); the namespaces stay isolated", "Temporal design slides 11, 12 and 24"),
    ("Payload codec server", "Component", "PLT platform", "AES-GCM, keys in Key Vault per namespace",
     "No personal data in history; search attributes limited to CaseId, Stage, ProductGroup and QueueCode", "Temporal design slides 11 and 27"),
    ("Temporal UI", "Component", "PLT platform",
     "Behind Entra ID: RW-PLATADM operates, RW-AUDIT reads, RW-SECADM decodes (break-glass)",
     "Access follows the same roles as the rest of Recovery", "Temporal design slide 11"),
]

RULE_HEAD = ["#", "Rule", "Applies to", "Value", "Source"]
RULES = [
    (1, "Deterministic workflow code", "All workflows", "No database, system clock, random, network or Drools call in workflow code", "Temporal design slide 27"),
    (2, "All I/O in activities", "All workflows", "Every read, write and rule evaluation is an activity; the workflow only decides the order", "Temporal design slide 27"),
    (3, "Activity retry", "All activities", "1 s initial interval, back-off 2, 10 attempts", "Temporal design slides 14 and 28"),
    (4, "Non-retryable failure", "EvaluateRules", "NoPackageInForce stops at once and raises the stuck-case alert; it is never retried", "Temporal design slide 28"),
    (5, "Activity timeout and heartbeat", "All activities", "Start-to-close timeout, schedule-to-close timeout and heartbeat interval: " + PL_TO, "Arch v5 slide 11; Temporal design slides 14 and 28"),
    (6, "Continue-As-New", "All workflows", "At every stage end and at least every 28 days, far below the 51,200-event and 50 MB limit", "Temporal design slide 13 note"),
    (7, "Parent close policy", "Every stage child", "ABANDON, so a child survives the parent's Continue-As-New", "Temporal design slide 13 note"),
    (8, "Search attributes", "All workflows", "CaseId, Stage, ProductGroup and QueueCode only; no personal data", "Temporal design slides 13 and 27"),
    (9, "Payload codec", "All workflows", "AES-GCM through the codec service, keys in Key Vault per namespace; history never holds clear personal data", "Temporal design slides 11 and 27"),
    (10, "History retention", "Closed workflows", "30 days, then archived to Blob (E2-039)", "Temporal design slide 27"),
    (11, "Versioning", "All workflows", "Worker Versioning plus Workflow.getVersion; the replay gate (E2-040) replays recorded histories in every build", "Temporal design slide 27"),
    (12, "Strict mode at a point of no return", "S6 debt transfer, S7 write-off posting, S5 auction sale, S4 title transfer", "The step waits until the central ledger in rwb-decision confirms the decision record", "Temporal design slide 26"),
    (13, "AI agent fallback", "AgentRunWorkflow", "After 60 s the rule answer is used (R-UNI-32)", "Temporal design slide 28"),
    (14, "Kafka unavailable", "Every producer", "Events wait in the outbox; retry topics 1 min, 10 min and 1 h, then the dead-letter topic with an alert", "Temporal design slide 28"),
    (15, "Schedule overlap", "Every Schedule", "Overlap policy SKIP with a catch-up window", "Arch v5 slide 44 notes"),
    (16, "Worker scaling", "Every service", "KEDA scales workers on task-queue backlog", "Temporal design slide 11"),
    (17, "Temporal version", "The cluster", "1.30 or later, for Nexus and Worker Versioning", "Temporal design slides 11 and 32"),
    (18, "No Quartz", "All scheduled work", "No Quartz and no ACE qrtz_* or batch_* tables; a job is a Temporal Schedule or an event-started workflow (ADR-016, DP-10)", "Arch v5 slide 44; plan DP-10"),
    (19, "No case of record in Temporal", "All workflows", "Case data stays in the own schema rwb_<short>; Temporal holds no case of record (T1)", "Temporal design slide 2 note"),
    (20, "Case workflow ID", "CaseWorkflow", "Workflow ID = case ID (ADR-011 writes case-{caseId}; the difference is CG-B-ARCH-WF-7, ASM-B-ARCH-WF-13)", "Temporal design slides 13 and 30"),
]

OPEN_HEAD = ["#", "Open point", "What it is", "Suggested owner role", "Where it bites", "Source"]
OPEN = [
    (1, "ADR-011: child workflow per stage", "The design runs a parent CaseWorkflow with one child per stage; ADR-011 still describes one long workflow", "Recovery tech lead", "Blocks the start of Epic 3", "Temporal design slide 32"),
    (2, "ADR-009: record locally, seal centrally", "Merges WriteDecisionLog and ApplyState into one RecordAndApply activity; needs Risk and Internal Audit sign-off", "RW-RISK with Internal Audit", "Activity contract of every service", "Temporal design slide 32"),
    (3, "Packages for S1 and S3 to S9", "448 rules exist and the package codes are Phase 2", "RW-COE with the architect", "EvaluateRules callers in S1 and S3 to S9", "Temporal design slide 32"),
    (4, "Route numbering R4 and R5", "R-LIT-01 starts litigation on route R4; Case Journeys v3 calls R4 the guarantee claim and R5 litigation", "Business analyst", "RouteDecisionWorkflow and the stage child names", "Temporal design slide 32"),
    (5, "XLS tables or DMN 1.6", "The same Drools runtime runs both; the move is table by table", "RW-COE with RW-RISK", "EvaluateRules inputs and the rule registry", "Temporal design slide 32"),
    (6, "Temporal 1.30 or later, jobs as Schedules, no Quartz", "Nexus and Worker Versioning need 1.30 or later; jobs become Schedules in the owning service", "Platform team", "Every Schedule row and the platform stories", "Temporal design slide 32"),
]

READ_ME = [
    "SCB Collections and Recovery. Henka Group, 22 November 2026.",
    "(C) Siam Commercial Bank and Henka Pte Ltd",
    "",
    "Recovery Workbench Temporal Workflow and Activity Catalog v1 (D-RCV-60). New document.",
    "Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.",
    "",
    "Change log",
    "v1, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash",
    "",
    "What this catalog is",
    "One row per Temporal construct of the target: every workflow, every activity contract, every Schedule, every task queue and namespace, and the platform rules that apply to all of them. A story file takes its section 12.5 (workflows and activities), section 12.6 (Schedules) and section 12.9 (call types) from this catalog.",
    "The catalog adds no design of its own. Every row cites the source that states it. A value no source states carries the placeholder of Template and Rules section R9, with the gap and assumption rows that own the decision.",
    "",
    "Counts",
    "Workflows: 20 rows. 18 are named in a source: 11 domain workflows (CaseWorkflow, DailyCaseRun, the eight stage workflows of S1 to S8 and InstructionWorkflow), 2 rwb-source-data workflows (AceIngestCheck, reconciliation), 4 kit templates (ApprovalWorkflow, NoticeDispatchWorkflow, DocumentIntakeWorkflow, AgentRunWorkflow) and the platform smoke workflow. 2 rows carry the placeholder: the event-started payment workflows of JOB-07 and JOB-08.",
    "Activities: 19 rows. 2 are universal in every service (EvaluateRules, RecordAndApply), 15 are named service activities, 1 row covers the OCR, classify and extract steps whose activity split is not stated, and 1 is the Nexus operation into ace-collection.",
    "Schedules: 10 (JOB-06, JOB-10, JOB-14, JOB-16, JOB-17, JOB-18, JOB-19, JOB-20, JOB-21, JOB-22). Task queues: 20 (the 19 service queues and rwb-platform), with the namespaces rwb-recovery and ace-collection. Platform rules: 20. Open points carried from the design: 6.",
    "",
    "How to read a row",
    "Workflows. Kind gives the role of the workflow: parent, stage child, event-started, kit template or platform. Started by is the trigger the source states. Hands back is the event the service publishes or the result the caller receives. Activities lists what the workflow calls; EvaluateRules and RecordAndApply appear in every row because the four-step loop (receive, ask Drools, record and apply, wait) repeats inside every workflow.",
    "Activities. The retry policy is 1 s initial interval, back-off 2 and 10 attempts for every activity (Temporal design slides 14 and 28), and NoPackageInForce is non-retryable. The start-to-close timeout and the heartbeat interval are " + PL_TO + ". A service publishes its activities as a typed contract jar on its own task queue; a caller in another namespace uses a Nexus operation instead.",
    "Schedules. The Schedule ID of every Schedule is " + PL_SCHED + ". The trigger or calendar is the v4 time or cadence, unchanged; the overlap policy SKIP with a catch-up window is stated once for all Schedules on Architecture v5 slide 44. Where the source does not name the workflow or activity that a Schedule starts, the Starts cell carries the placeholder " + PL_WF4 + ".",
    "",
    "Status",
    "Draft. No approval is recorded for this version (ASM-B-ARCH-WF-1).",
    "Release dates: this document states none. Every release date it quotes from a related document stays (tentative).",
    "",
    "Sources and precedence",
    "Precedence follows Template and Rules section R3 (R-PREC). Short forms used in the sheets: Arch v5 = Recovery Workbench Architecture v5 Text Extract v1 (slides 11 to 20 and 41 to 44); Temporal design = Recovery Workbench Temporal and Drools Design Text Extract v1 (slides 11 to 32); Ownership Map = Recovery Workbench Microservice Ownership Map v1; Batch v4 and Batch v5 = Recovery Workbench Batch and Scheduling Design v4 and v5.",
    "Architecture v5 slide 41 gives one task queue per service in namespace rwb-recovery; slides 14 to 20 give the Temporal contract of each service; slide 44 is the job map. Temporal design slide 11 gives the runtime view, slide 12 the five layers and the kit, slides 13 to 28 the workflow model, the activities, the failure behaviour and the platform rules, and slide 32 the open points.",
    "",
    "Gaps and assumptions cited in this document",
    "CG-B-ARCH-WF-1 Schedule identifiers and calendars; CG-B-ARCH-WF-2 activity timeouts; CG-B-ARCH-WF-3 the event-started payment workflow; CG-B-ARCH-WF-4 the work started by six Schedules and three workflows; CG-B-ARCH-WF-5 DailyCaseRun as Schedule and event; CG-B-ARCH-WF-6 the rwb-platform task queue; CG-B-ARCH-WF-7 the case workflow ID; CG-A6-flows-6 WIN notices; CG-A6-flows-9 write-off scan. Assumptions: ASM-B-ARCH-WF-1 to ASM-B-ARCH-WF-13 and ASM-A6-flows-8 and 12.",
    "",
    "Related documents",
    "Recovery Workbench Batch and Scheduling Design v5, in this folder, is the job-to-mechanism design that every Schedule row serves; the full job detail (times, dependencies, failure rules) stays there.",
]


def table(wb, name, head, rows, widths, first=False):
    ws = wb.create_sheet(name)
    ws.append(head)
    for c in ws[1]:
        c.font = H["font"]; c.fill = H["fill"]; c.alignment = H["alignment"]
    for r in rows:
        ws.append(list(r))
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[openpyxl.utils.get_column_letter(i)].width = w
    for row in ws.iter_rows(min_row=2, max_row=ws.max_row, max_col=len(head)):
        for c in row:
            c.alignment = Alignment(wrap_text=True, vertical="top")
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = f"A1:{openpyxl.utils.get_column_letter(len(head))}{ws.max_row}"
    return ws


def main():
    wb = openpyxl.Workbook()
    wb.remove(wb.active)

    rm = wb.create_sheet("Read me")
    for line in READ_ME:
        rm.append([line])
    rm.column_dimensions["A"].width = 135
    for n, line in enumerate(READ_ME, 1):
        c = rm.cell(row=n, column=1)
        c.alignment = Alignment(wrap_text=True, vertical="top")
        if n in (1, 2):
            c.font = Font(bold=True, size=13 if n == 1 else 11)
            c.alignment = Alignment(wrap_text=False)
        elif line in ("Change log", "What this catalog is", "Counts", "How to read a row", "Status",
                      "Sources and precedence", "Gaps and assumptions cited in this document", "Related documents"):
            c.font = Font(bold=True)

    table(wb, "Workflows", WF_HEAD, WORKFLOWS, [34, 26, 8, 16, 16, 48, 62, 36, 46, 42, 34])
    table(wb, "Activities", ACT_HEAD, ACTIVITIES, [26, 26, 18, 18, 52, 40, 60, 30])
    table(wb, "Schedules", SCH_HEAD, SCHEDULES, [9, 18, 8, 16, 16, 34, 52, 20, 46, 34])
    table(wb, "Task queues and namespaces", TQ_HEAD, QUEUES, [24, 16, 18, 46, 62, 34])
    table(wb, "Platform rules", RULE_HEAD, RULES, [5, 34, 34, 74, 34])
    table(wb, "Open points", OPEN_HEAD, OPEN, [5, 34, 62, 28, 34, 30])

    wb.properties.creator = "SCB Collections and Recovery"
    wb.properties.lastModifiedBy = "SCB Collections and Recovery"
    wb.properties.title = "Recovery Workbench Temporal Workflow and Activity Catalog v1"
    wb.properties.subject = "D-RCV-60 microservice realignment"
    wb.save(P)
    print("SAVED", P, wb.sheetnames)
    print("rows", {ws.title: ws.max_row for ws in wb.worksheets})


if __name__ == "__main__":
    main()
