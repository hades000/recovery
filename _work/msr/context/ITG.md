# Context pack — ITG Integration

Read this pack instead of the full Architecture v5 and Temporal/Drools extracts and the full ownership JSON.

## Integration scope
- Integration epics: RWB-ITG-W1, RWB-ITG-W2, RWB-ITG-W3, RWB-ITG-W4, RWB-ITG-NFR
- One journey per wave plus the NFR integration epic.

## Naming and shared platform rules
- 19 services inside ACE. One PostgreSQL schema and one login per service.
- Schema `rwb_<short with _>`; REST base `/api/recovery/<short>/v1`; topic `rwb.<short>.events.v1`;
  event name `rwb.<short>.<Event>.v1`; Temporal task queue `rwb-<short>`;
  Java package `th.co.scb.ace.workbench.recovery.<short without hyphen>`.
- Shared topic `rwb.decision-record.v1`; Temporal namespace `rwb-recovery`.
- Kafka with outbox and inbox, CloudEvents envelope. Retry and `.dlt` topics per service.
- Temporal Schedules replace Quartz. Embedded Drools per service; rule packages come from rwb-decision.
- Contract-first REST: one hop, 2 s timeout. No service reads another service's tables.
- No data lake. rwb-reporting builds its read model from events.
- No PII in events, workflow inputs or logs. ACE data only through the owner's contract or `v_ace_*` views.
## Decoupling patterns (DP table, short)
DP-01 own schema only | DP-02 one login per service | DP-03 local decision record + rwb.decision-record.v1 |
DP-04 embedded Drools + rule packages from rwb-decision | DP-05 ACE data through rwb-source-data or v_ace_* |
DP-06 parameters contract of rwb-case | DP-07 reference data contract of rwb-case |
DP-08 authorise contract of rwb-access | DP-09 outbox/inbox + owner topic |
DP-10 Temporal Schedule or event-started workflow | DP-11 REST contract with mock |
DP-12 CaseWorkflow parent with child per stage | DP-13 per-service API base |
DP-14 per-service topic names | DP-15 per-service Flyway |
DP-16 rwb-integration contract | DP-17 no data lake |
DP-18 interaction ledger owned by rwb-source-data | DP-19 gateway-bff composite route |
DP-20 rwb-agent contract.

## Services (19)
| Code | Service | Schema | REST base | Topic | Wave |
|---|---|---|---|---|---|
| P1 | rwb-source-data | rwb_source_data | /api/recovery/source-data/v1 | rwb.source-data.events.v1 | 1 |
| P2 | rwb-integration | rwb_integration | /api/recovery/integration/v1 | rwb.integration.events.v1 | 1 |
| P3 | rwb-case | rwb_case | /api/recovery/case/v1 | rwb.case.events.v1 | 1 |
| P4 | rwb-access | rwb_access | /api/recovery/access/v1 | rwb.access.events.v1 | 1 |
| P5 | rwb-document | rwb_document | /api/recovery/document/v1 | rwb.document.events.v1 | 1 |
| P6 | rwb-comms | rwb_comms | /api/recovery/comms/v1 | rwb.comms.events.v1 | 1 |
| P7 | rwb-decision | rwb_decision | /api/recovery/decision/v1 | rwb.decision.events.v1 | 1 |
| P8 | rwb-payment | rwb_payment | /api/recovery/payment/v1 | rwb.payment.events.v1 | 2 |
| P9 | rwb-reporting | rwb_reporting | /api/recovery/reporting/v1 | rwb.reporting.events.v1 | 1 |
| P10 | rwb-agent | rwb_agent | /api/recovery/agent/v1 | rwb.agent.events.v1 | 1 |
| S1 | rwb-valuation | rwb_valuation | /api/recovery/valuation/v1 | rwb.valuation.events.v1 | 3 |
| S2 | rwb-treatment | rwb_treatment | /api/recovery/treatment/v1 | rwb.treatment.events.v1 | 2 |
| S3 | rwb-guarantee | rwb_guarantee | /api/recovery/guarantee/v1 | rwb.guarantee.events.v1 | 3 |
| S4 | rwb-litigation | rwb_litigation | /api/recovery/litigation/v1 | rwb.litigation.events.v1 | 3 |
| S5 | rwb-asset | rwb_asset | /api/recovery/asset/v1 | rwb.asset.events.v1 | 2 |
| S6 | rwb-debtsale | rwb_debtsale | /api/recovery/debtsale/v1 | rwb.debtsale.events.v1 | 3 |
| S7 | rwb-writeoff | rwb_writeoff | /api/recovery/writeoff/v1 | rwb.writeoff.events.v1 | 4 |
| S8 | rwb-deviation | rwb_deviation | /api/recovery/deviation/v1 | rwb.deviation.events.v1 | 2 |
| S9 | rwb-partner | rwb_partner | /api/recovery/partner/v1 | rwb.partner.events.v1 | 4 |

## REST operations by owner
### P1
- GET /admin/data-contracts
- GET /admin/data-dictionary/fields
- GET /admin/data-products
- GET /admin/data-quality/exceptions
- GET /admin/jobs
- GET /admin/trackers
- GET /admin/trackers/retirement-report
- GET /cases/{caseId}/interactions
- GET /data-products/freshness
- GET /data-products/{productCode}/records
- PATCH /admin/data-contracts/{contractId}
- PATCH /admin/data-dictionary/fields/{fieldCode}
- POST /admin/data-contracts/{contractId}/publish
- POST /admin/jobs/{jobId}/rerun
- POST /admin/trackers/{trackerId}/loads
- POST /admin/trackers/{trackerId}/retire
- POST /admin/trackers/{trackerId}/sign-off
- POST /cases/{caseId}/interactions
### P2
- GET /admin/outbound-items
- GET /admin/outbox/deliveries
- GET /admin/scheduled-jobs
- GET /cases/{caseId}/customer-products
- GET /cases/{caseId}/plan-status
- GET /treatments/{treatmentId}/credit-pack
- GET /treatments/{treatmentId}/credit-result
- POST /admin/interfaces/{interfaceCode}/manual-retirement
- POST /admin/outbound-items/{itemId}/resend
- POST /admin/outbox/deliveries/{deliveryId}/resend
- POST /treatments/{treatmentId}/credit-result
### P3
- GET /admin/change-log
- GET /admin/lists/{listCode}
- GET /admin/parameters
- GET /cases
- GET /cases/export
- GET /cases/{caseId}
- GET /cases/{caseId}/accounts
- GET /cases/{caseId}/next-action
- GET /cases/{caseId}/parties
- GET /cases/{caseId}/timeline
- GET /cases/{caseId}/timers
- GET /me/tasks
- GET /queues
- GET /queues/{queueId}/cases
- PATCH /tasks/{taskId}
- POST /admin/reference-loads
- POST /admin/reference-loads/{loadId}/approve
- POST /admin/reference-loads/{loadId}/rollback
- POST /admin/reference-loads/{loadId}/verify
- POST /cases/{caseId}/legal-hold
- POST /cases/{caseId}/transfer
- POST /queues/{queueId}/placements
### P4
- GET /admin/access-log
- GET /admin/roles
- GET /me/session
- POST /admin/break-glass-grants
### P5
- GET /cases/{caseId}/document-checklist
- GET /cases/{caseId}/documents
- GET /documents
- GET /documents/{documentId}
- GET /documents/{documentId}/content
- GET /intake-items/{intakeItemId}
- GET /intake-items/{intakeItemId}/content
- GET /review-items
- PATCH /documents/{documentId}/fields/{fieldId}
- POST /cases/{caseId}/documents
- POST /cases/{caseId}/field-captures
- POST /cases/{caseId}/generated-documents
- POST /documents/{documentId}/custody
- POST /documents/{documentId}/regenerate
- POST /documents/{documentId}/review
- POST /documents/{documentId}/versions
- POST /intake-items/{intakeItemId}/resolve
### P6
- GET /admin/templates
- GET /admin/templates/{templateId}/content
- GET /notices/{noticeId}
- GET /treatments/{treatmentId}/signature-requests
- POST /admin/templates
- POST /admin/templates/{templateId}/approve
- POST /admin/templates/{templateId}/withdraw
- POST /cases/{caseId}/messages
- POST /cases/{caseId}/notices
- POST /signature-requests/{requestId}/result
- POST /treatments/{treatmentId}/signature-requests
### P7
- GET /admin/rule-package-versions/{versionId}/dry-run
- GET /admin/rule-packages
- GET /admin/rule-packages/change-report
- GET /admin/rule-packages/{packageCode}/versions
- GET /admin/rule-versions
- GET /approvals
- GET /approvals/{approvalId}
- GET /cases/{caseId}/recommendation
- GET /decision-log
- GET /decision-log/{entryId}
- POST /admin/rule-package-versions/{versionId}/approve
- POST /admin/rule-package-versions/{versionId}/rollback
- POST /admin/rule-packages/{packageCode}/versions
- POST /admin/rule-versions
- POST /admin/rule-versions/{versionId}/approve
- POST /admin/rule-versions/{versionId}/rollback
- POST /approvals/{approvalId}/approve
- POST /approvals/{approvalId}/refuse
- POST /approvals/{approvalId}/return
### P8
- GET /proceeds
- POST /proceeds/{proceedsId}/match
### P9
- GET /reports/measures
### P10
- GET /admin/agent-configs
- GET /admin/agent-evaluations
- GET /admin/agent-evaluations/{evaluationId}/report
- GET /admin/agent-metrics
- GET /admin/agent-runs
- GET /cases/{caseId}/agent-outputs
- POST /admin/agent-configs
- POST /admin/agent-configs/{versionId}/approve
- POST /admin/agent-evaluations
- POST /admin/agent-samples
- POST /agent-runs/{runId}/feedback
### S1
- POST /assets/{assetId}/valuations
- POST /assets/{assetKey}/valuations
- POST /cases/{caseId}/route
### S2
- GET /treatments/{treatmentId}
- PATCH /treatments/{treatmentId}
- POST /cases/{caseId}/treatments
- POST /treatments/{treatmentId}/submit
### S3
- PATCH /guarantee-claims/{claimId}
- POST /cases/{caseId}/guarantee-claims
### S4
- GET /legal-actions/{legalActionId}
- PATCH /legal-actions/{legalActionId}
- POST /cases/{caseId}/legal-actions
- POST /legal-actions/{legalActionId}/hearings
- POST /notices/{noticeId}/approve
### S5
- GET /assets
- GET /assets/{assetId}
- GET /assets/{assetKey}
- POST /assets/{assetId}/listings
- POST /assets/{assetKey}/listings
- POST /listings/{listingId}/rounds
### S6
- GET /debt-sale-lots/{lotId}
- GET /partner/data-room/{lotId}
- POST /debt-sale-lots
- POST /debt-sale-lots/{lotId}/award
- POST /partner/data-room/{lotId}/bids
### S7
- POST /write-off-scans
- POST /write-offs/{writeOffId}/committee-decision
### S8
- PATCH /deviations/{deviationId}
- POST /cases/{caseId}/deviations
### S9
- GET /partner/instructions
- GET /partners
- POST /cases/{caseId}/instructions
- POST /partner/instructions/{instructionId}/accept
- POST /partner/instructions/{instructionId}/invoices
- POST /partner/instructions/{instructionId}/results
### PLT
- GET /admin/feature-flags
- GET /feature-flags
- PATCH /admin/feature-flags/{flagKey}
- POST /admin/feature-flags
- POST /admin/workflows/smoke

## Events by owner
- P1: EV-26, EV-27
- P3: EV-01, EV-02, EV-03, EV-04, EV-05, EV-19, EV-29
- P5: EV-16, EV-17
- P6: EV-13, EV-14, EV-15
- P7: EV-08, EV-09, EV-30
- P8: EV-11, EV-12, EV-25
- P10: EV-28
- S2: EV-10
- S5: EV-22
- S6: EV-23
- S7: EV-24
- S8: EV-06, EV-07
- S9: EV-20, EV-21
- PLT: EV-18

## Architecture v5 integration slides

## Slide 1

Recovery Workbench: 19 services inside the ACE platform

Service boundaries, contracts and call types, the event broker and a reusable Temporal layer

For the architecture team   |   v5 · November 2026

Notes: Purpose: agree the target service architecture of Recovery Workbench with the architecture team.

What changed since v4 (feedback from the review): Recovery stays part of ACE (same AKS cluster, App Gateway and ACE Common shared services, as in recovery-architecture.pptx); recovery-core is split further into 19 services, one per business module, so each can be repurposed later; no database per service: Recovery uses the ACE database with one schema per service; no connection to the data lake; Kafka is proposed as the event broker; the Temporal layer is redrawn so it can be reused by other workbenches.

The 19 icons are the 19 Recovery services. The main part is diagrams and contracts; tables are in the appendix.
## Slide 2

At a glance: 19 Recovery services, still part of ACE

Read clockwise from the top left

Recovery Workbench
19 services in ACE

Stays part of ACE

Same AKS cluster and App Gateway as ACE

Uses ACE Common shared services

ACE database; no data lake connection

19 services, one per module

recovery-core split along module lines

Each one reusable or replaceable alone

Own schema, topic and task queue each

Clear contracts between them

REST for screens, one hop only

Kafka events for facts

Temporal for steps and long processes

What we need from you

Kafka topics on the ACE platform

19 schemas and logins in the ACE DB

Owner for the shared Temporal layer

Recovery stays part of ACE: 19 small services on ACE's cluster, ACE's shared services and ACE's database.

2

Notes: Stays inside ACE: same AKS cluster and Azure App Gateway as ACE (path routing /recovery/* and /api/recovery/*), the ACE Common shared services (sign-in and access checks, audit and PII logging, shared case view, shared entities, restructure calculator, notification path), and the ACE PostgreSQL database. Recovery has no connection to the data lake; INT-19/INT-20 are removed.

19 services: recovery-core from the six-service proposal is split along its module lines, one service per BA module P1-P10 and S1-S9. Each has an api and a worker deployment, its own schema and login in the ACE database, its own Kafka topic and its own Temporal task queue.

How they connect: REST for screens (one hop from the BFF), Kafka events for facts, Temporal for steps in another service and long processes, files for outside parties, SQL views only for rwb-source-data reading ACE.

Decisions needed: last slide.
## Slide 3

The recovery journey: from a missed loan to a closed case

Six steps; at step 4 the bank picks one or more of eight routes

1  Enter

Loan 90+ days past due, unless excluded
rwb-source-data

2  Take over

Case created overnight, given to an officer by 07:00
rwb-case

3  Choose route

Valuation and rules propose; an approver signs off
rwb-valuation

4  Work the route

Officers, law firms and buyers act
route services

5  Collect

Money matched to the case and posted
rwb-payment

6  Close

Paid, settled, sold or written off
rwb-case

Step 4 · eight recovery routes (some run together)

Restructure
New terms the customer can pay

rwb-treatment · S2

Settlement
Agreed discount, paid in full or instalments

rwb-treatment · S2

Deed in lieu
Customer hands over the asset

rwb-treatment · S2

Guarantee claim
Claim on guarantors or schemes

rwb-guarantee · S3

Litigation
Court, judgment, enforcement, auction

rwb-litigation · S4

Asset sale
Bank sells foreclosed property

rwb-asset · S5

Debt sale
Loans sold in lots to buyers

rwb-debtsale · S6

Write-off
Removed from the books; recoveries tracked

rwb-writeoff · S7

Always on: special situations · rwb-deviation (S8)
Dispute, hardship, death, fraud, bankruptcy, lost contact or damaged collateral pause the case clock; the legal deadline never pauses.

Always on: approvals, rules and the log · rwb-decision (P7)
50 bank-wide rules apply at every step; every decision is approved within authority and recorded.

A case enters Recovery at 90 days past due and leaves when it is paid, settled, sold or written off.

3

Notes: Entry: accounts at 90+ days past due enter Recovery unless an exclusion applies (deceased, fraud, bankruptcy, active TDR, dispute). Cases are created from the overnight ACE data and allocated by 07:00 (JOB-02, JOB-03).

Route decision (S1, decision D6): valuation and rules propose a route; an approver within their delegated authority (DoA Matrix v2) signs it off; the decision is logged (P7). Routes can run in parallel, for example a guarantee claim alongside litigation.

Always on: deviations X1-X7 (S8) pause the stage clock but never the legal prescription clock (R-DEV-01). Universal rules R-UNI-01 to 50 apply throughout.

The grey label under each route is the service that runs it.
## Slide 4

19 business modules become 19 services, in four groups

One service per module from the functional specifications; each can be reused or replaced on its own

Case & control  (4)

Case & workflow
P3 · rwb-case

Decision center & log
P7 · rwb-decision

Access & administration
P4 · rwb-access

Deviation handling
S8 · rwb-deviation

Recovery routes  (7)

Valuation & route
S1 · rwb-valuation

TDR, settlement, DIL
S2 · rwb-treatment

Guarantees
S3 · rwb-guarantee

Litigation & enforcement
S4 · rwb-litigation

Assets & auction
S5 · rwb-asset

Debt sale
S6 · rwb-debtsale

Write-off & recovery
S7 · rwb-writeoff

Shared capabilities  (5)

Document hub
P5 · rwb-document

Communications
P6 · rwb-comms

Payments & posting
P8 · rwb-payment

Partner management
S9 · rwb-partner

Integration & files
P2 · rwb-integration

Data & AI  (3)

Source data
P1 · rwb-source-data

Reporting
P9 · rwb-reporting

Agent runtime
P10 · rwb-agent

Every service has
api + worker deployment
schema rwb_<name> + DB login
topic rwb.<name>.events.v1
task queue rwb-<name>

Shared platform (not in the 19)
gateway-bff + Redis session
Temporal, shared with ACE
Kafka business-event topics
Airflow, bank scheduler (to discuss)
observability (OpenTelemetry)

19 modules = 19 services: each can be released, scaled, reused or replaced on its own.

4

Notes: Rule: one deployable service per BA module, so that each capability has its own code, release, owner, contract, schema, topic and task queue. This is what makes later reuse possible: another workbench can call or deploy rwb-document, rwb-comms or rwb-decision without taking the rest of Recovery.

Groups are for reading only; they are not deployment units. Shared platform pieces (gateway-bff with Redis, Temporal, Kafka, the bank's Airflow scheduler, observability) are not counted in the 19.

First epic per service: Epic 1: P1, P2, P3, P4, P5, P6, P7, P9, P10. Epics 2-3: P8, S2, S5, S8. Epics 4-5: S1, S3, S4, S6. Epics 6-7: S7, S9.
## Slide 5

From the six-service proposal to 19: only recovery-core is split

Same platform roles as recovery-architecture.pptx; recovery-core is cut along its module lines

REFERENCE PROPOSAL · 6 SERVICES IN ACE

v5 · SHARED PLATFORM + 19 RECOVERY SERVICES

①  gateway-bff
Spring Cloud Gateway · Redis

②  workflow
Temporal, shared with ACE

③  recovery-core
modular monolith: all business modules

④  batch
Airflow: load, validate, report

⑤  document-service
OCR · Blob 2.8 TB

⑥  ai-agent
agents with rule fallback

Kept · shared BFF with Redis session; routes /api/recovery/*

Kept · shared Temporal + reusable workflow kit (L1-L3)

Kept as the bank's Airflow · overnight chain, files, extracts (to discuss)

rwb-document · P5

rwb-agent · P10

split

P3
Case

P7
Decision

P4
Access

S8
Deviation

S1
Valuation

S2
Treatment

S3
Guarantee

S4
Litigation

S5
Asset

S6
Debt sale

S7
Write-off

P6
Comms

P8
Payment

S9
Partner

P2
Integration

P1
Source data

P9
Reporting

Nothing new in the platform: recovery-core is cut along its module lines, so each module becomes its own service.

5

Notes: Reference: recovery-architecture.pptx proposes six services inside ACE: (1) gateway-bff (Spring Cloud Gateway, Redis session), (2) workflow on Temporal shared by ACE and Recovery, (3) recovery-core, a modular monolith holding the business modules on Azure PostgreSQL, (4) batch on Airflow (load, validate, report), (5) document-service (OCR, Blob, 2.8 TB), (6) ai-agent.

v5 keeps roles 1, 2 and 4 as shared platform, keeps 5 and 6 as rwb-document (P5) and rwb-agent (P10), and splits recovery-core into the other 17 module services. Business schedules (case creation, rule promotion, write-off scan) run as Temporal Schedules in the owning service; Role 4 becomes the bank's own Airflow, since the bank is moving from Control-M to Airflow (for discussion): it runs the cross-system overnight chain, fixed-window file transfers, report extracts and one-off bulk loads, and calls services through their APIs, never their schemas.

Why split further: each module becomes a unit that can be reused by another workbench, released alone and scaled alone.
## Slide 7

System context: Recovery lives inside the ACE platform

C4 level 1: people above, ACE platform in the middle, outside systems at the sides

Recovery officers & approvers
Work cases, approve routes

Managers, Risk & Audit
Monitor, review, audit

External partners
Law firms, agencies, valuers, buyers

ACE PLATFORM · SAME AKS CLUSTER, APP GATEWAY AND DATABASE

ACE Collection
collections workbench

Recovery Workbench
19 services + gateway-bff

Temporal · Kafka
shared with ACE

ACE Common
sign-in, logging, case view, calculator, notices

ACE PostgreSQL · ACE schemas + v_ace_* views + 19 Recovery schemas

/recovery/* via App Gateway

partner gateway

case view

own schemas

Recovery → ACE Common: sign-in, logging, notices, restructure calculator

Source systems
COLLINS, ALS, CCMS, GL …

ACE ingestion (overnight)

Data lake / Power BI
not connected

Entra ID
via ACE Common sign-in

Enterprise AI
private endpoint · rwb-agent

NSS SMS · LINE OA
via ACE notification path

WIN · debt buyers
files · rwb-integration

SOC / SIEM
via ACE PII logging (Kafka)

Recovery adds services inside ACE's platform; it reads ACE data through views and never connects to the data lake.

7

Notes: Recovery Workbench runs in the same AKS cluster and behind the same Azure App Gateway as ACE Collection. The App Gateway routes / and /api/* to ACE and /recovery/* and /api/recovery/* to the Recovery gateway-bff.

ACE ingests all source systems (COLLINS, ALS, CCMS, SVAF, AMIS, RPS, LIT, WIN POD, GL, SCBPDM, NLEADS, EasyApp) into the ACE database overnight. Recovery loads no source data itself: rwb-source-data reads ACE data through the 30 read-only recovery.v_ace_* views (ADR-010).

ACE Common (owned by the ACE team, INT-34) gives Recovery: sign-in and access checks (Entra ID), audit and PII logging (PII Kafka to SOC), the shared case view, shared entities, the restructure calculator and the notification path (NSS SMS, LINE OA).

Outside: Enterprise AI private endpoint (INT-23) for rwb-agent; WIN outbound file (INT-14) and debt-buyer files (INT-25) through rwb-integration. No data lake or Power BI connection (INT-19/20 removed).
