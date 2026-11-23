
Service contracts 1/7 · Case and control: case, decision, access

IN = what the service accepts; OUT = what it writes and sends; the tag is the call type

IN

OUT

REST  GET /cases/{id}, /cases?queue= · POST /cases/{id}/actions · GET /tasks · POST /tasks/{id}/complete · GET /case-summary/{id} (for ACE shared case view)
EVT  RouteDecided · DeviationRaised / Cleared · PaymentMissed, TreatmentBooked, ProceedsMatched · LotAwarded, AssetTakenOn, WriteOffApproved · AceDataReady, RulePackageInForce
TMP  CaseWorkflow (parent, one per case) · DailyCaseRun (Schedule + AceDataReady) · Act: allocate, transfer, rebalance

DB  writes schema rwb_case: case, CMMN state, queues, tasks, allocation, timers
EVT  rwb.case.events.v1: CaseCreated, CaseAllocated, CaseAllocationFailed, CaseTransferred, CaseStateChanged, TimerBreached
TMP  Source data: listEligibleAccounts(businessDate) · Valuation: child: RouteDecisionWorkflow · Treatment: child: stage workflows · Litigation, Asset, Debt sale, Write-off, Guarantee: child · Deviation: child: DeviationWorkflow
REST  Access: authorise (cached)

P3 · rwb-case
Case & workflow
queue rwb-case
rwb.case.events.v1

IN

OUT

REST  GET /decisions?caseId= · POST /approvals/{id}/decide · POST /rule-models · GET /rule-models/{n}/{v}
EVT  DecisionRecorded (from all 19) · NoticeGenerated (approval) · AgentRunCompleted
TMP  ApprovalWorkflow (kit template) · Schedules: rule promote 00:01, chain check 02:00

DB  writes schema rwb_decision: approvals, central decision ledger, DMN model registry
EVT  rwb.decision.events.v1: ApprovalRequested, ApprovalDecided, RulePackageInForce
REST  Access: DoA limits
FILE  Immutable storage: daily ledger seal (WORM)

P7 · rwb-decision
Decision center & log
queue rwb-decision
rwb.decision.events.v1

IN

OUT

REST  POST /authorise (role, scope, DoA) · GET /me/permissions · GET /doa-limits · /masking-policies
EVT  (none: reference data owner)
TMP  Schedule: access review list (six-monthly)

DB  writes schema rwb_access: Recovery roles as data, scope, masking policy, DoA table, access log
EVT  rwb.access.events.v1: AccessPolicyChanged, DoaLimitChanged
REST  ACE Common: sign-in, group-to-role (Entra)

P4 · rwb-access
Access & administration
queue rwb-access
rwb.access.events.v1

14

Notes: Contracts in full (also in the service catalogue in the appendix):

rwb-case (P3, Case & workflow)
IN: REST GET /cases/{id}, /cases?queue=; POST /cases/{id}/actions; GET /tasks · POST /tasks/{id}/complete; GET /case-summary/{id} (for ACE shared case view) | events RouteDecided; DeviationRaised / Cleared; PaymentMissed, TreatmentBooked, ProceedsMatched; LotAwarded, AssetTakenOn, WriteOffApproved; AceDataReady, RulePackageInForce | Temporal CaseWorkflow (parent, one per case); DailyCaseRun (Schedule + AceDataReady); Act: allocate, transfer, rebalance
OUT: schema rwb_case (case, CMMN state, queues, tasks, allocation, timers) | topic rwb.case.events.v1: CaseCreated, CaseAllocated, CaseAllocationFailed, CaseTransferred, CaseStateChanged, TimerBreached | TMP Source data: listEligibleAccounts(businessDate) · Valuation: child: RouteDecisionWorkflow · Treatment: child: stage workflows · Litigation, Asset, Debt sale, Write-off, Guarantee: child · Deviation: child: DeviationWorkflow | REST Access: authorise (cached)

rwb-decision (P7, Decision center & log)
IN: REST GET /decisions?caseId=; POST /approvals/{id}/decide; POST /rule-models · GET /rule-models/{n}/{v} | events DecisionRecorded (from all 19); NoticeGenerated (approval); AgentRunCompleted | Temporal ApprovalWorkflow (kit template); Schedules: rule promote 00:01, chain check 02:00
OUT: schema rwb_decision (approvals, central decision ledger, DMN model registry) | topic rwb.decision.events.v1: ApprovalRequested, ApprovalDecided, RulePackageInForce | REST Access: DoA limits | FILE Immutable storage: daily ledger seal (WORM)

rwb-access (P4, Access & administration)
IN: REST POST /authorise (role, scope, DoA); GET /me/permissions; GET /doa-limits · /masking-policies | events (none: reference data owner) | Temporal Schedule: access review list (six-monthly)
OUT: schema rwb_access (Recovery roles as data, scope, masking policy, DoA table, access log) | topic rwb.access.events.v1: AccessPolicyChanged, DoaLimitChanged | REST ACE Common: sign-in, group-to-role (Entra)

Tags: REST = synchronous HTTPS (OpenAPI 3.1); EVT = Kafka topic (CloudEvents, AsyncAPI); TMP = Temporal activity or child workflow on the owner's task queue; NEXUS = Temporal Nexus operation into another namespace; SQL = read-only view; FILE = claim-check file; DB = the service's own schema in the ACE database.

