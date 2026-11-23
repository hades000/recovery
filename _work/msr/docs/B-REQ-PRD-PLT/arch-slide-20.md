
Service contracts 7/7 · Write-off, the gateway, and what every service does

IN = what the service accepts; OUT = what it writes and sends; the tag is the call type

IN

OUT

REST  GET/POST /write-offs · POST /write-offs/{id}/submit
EVT  AceDataReady (GL write-off) · ProceedsMatched
TMP  WriteOffWorkflow · Schedule: scan, 3rd working day

DB  writes schema rwb_writeoff: eligibility, committee, posting, recovery after charge-off
EVT  rwb.writeoff.events.v1: WriteOffApproved
TMP  Decision: child: committee approval · Payment: postProceeds
REST  Source data: GL outcome

S7 · rwb-writeoff
Write-off & recovery
queue rwb-writeoff
rwb.writeoff.events.v1

IN

OUT

REST  Browser: /api/recovery/** via App Gateway, session cookie (opaque, 15 min idle)
EVT  ApprovalRequested, TimerBreached → officer inbox push
REST  Partners do not use it: partner gateway → rwb-partner

REST  Owner service, one hop, in parallel for composite screens (2 s timeout, breaker per service)
REST  ACE Common sign-in: session → short-lived user JWT
DB  Redis: sessions only; no business data

gateway-bff
shared platform
Spring Cloud Gateway
Redis session

IN

OUT

EVT  AccessPolicyChanged, DoaLimitChanged, RulePackageInForce → cache refresh
TMP  Own task queue rwb-<svc>; its own Schedules
REST  /health, /metrics for the platform

DB  Own schema: business tables + outbox + inbox + decision_record
EVT  DecisionRecorded → rwb.decision-record.v1 (ledger in rwb-decision)
REST  ACE Common audit and PII logging; OpenTelemetry traces, metrics, logs

Every service
from the service template
and shared libraries

20

Notes: Contracts in full (also in the service catalogue in the appendix):

rwb-writeoff (S7, Write-off & recovery)
IN: REST GET/POST /write-offs; POST /write-offs/{id}/submit | events AceDataReady (GL write-off); ProceedsMatched | Temporal WriteOffWorkflow; Schedule: scan, 3rd working day
OUT: schema rwb_writeoff (eligibility, committee, posting, recovery after charge-off) | topic rwb.writeoff.events.v1: WriteOffApproved | TMP Decision: child: committee approval · Payment: postProceeds | REST Source data: GL outcome

gateway-bff: the only entry for staff screens. Composes at most a few parallel calls; never calls a service that then calls another.

Every service: built from one template (Spring Boot, outbox relay, inbox, Temporal worker, codec, OpenTelemetry, contract tests). Writes its own decision records locally and publishes DecisionRecorded.

Tags: REST = synchronous HTTPS (OpenAPI 3.1); EVT = Kafka topic (CloudEvents, AsyncAPI); TMP = Temporal activity or child workflow on the owner's task queue; NEXUS = Temporal Nexus operation into another namespace; SQL = read-only view; FILE = claim-check file; DB = the service's own schema in the ACE database.

