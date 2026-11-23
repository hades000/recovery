# Context pack — PLT Platform

Read this pack instead of the full Architecture v5 and Temporal/Drools extracts and the full ownership JSON.

## Platform scope
- 7 platform epics, wave 0: RWB-PLT-TPL, RWB-PLT-LIB, RWB-PLT-WF, RWB-PLT-DB, RWB-PLT-EVT, RWB-PLT-EDGE, RWB-PLT-OBS
- Platform owns shared libraries, the Temporal layer, Kafka platform, ACE DB schemas and logins, edge/gateway, observability and the service template.

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

## Ownership rows owned by PLT
### Tables (6)
- feature_flag
- feature_flag_change
- idempotency_key
- outbox_delivery
- outbox_event
- processed_event

### REST operations provided (5)
- GET /admin/feature-flags
- GET /feature-flags
- PATCH /admin/feature-flags/{flagKey}
- POST /admin/feature-flags
- POST /admin/workflows/smoke

### Events (1)
- EV-18

### Jobs (4)
- JOB-05
- JOB-11
- JOB-21
- JOB-22

### Workflows (1)
- PlatformSmokeWorkflow

## Architecture v5 platform slides

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
## Slide 6

The guardrails: industry standards and Bank of Thailand rules

Every choice in this deck traces back to one of these

Industry standards we follow

BIAN
Bank capability map: one service per capability

Microservice patterns
Schema per service, sagas, outbox (microservices.io)

Zero trust (NIST SP 800-204)
Every call encrypted and checked

Standard contracts
OpenAPI 3.1, AsyncAPI 3, CloudEvents 1.0

Decision models (OMG DMN)
Rules in an industry format, not Excel

OpenTelemetry
One trace across REST, Kafka and Temporal

FAPI 2.0 · OWASP API
Secure partner and internal APIs

Azure Well-Architected
Reference design for services on AKS

Bank of Thailand and Thai law

FPG 19/2560 · IT risk
Prior BOT approval for significant change

FPG 19/2559 · outsourcing
Rules for cloud and third parties

Cyber resilience (CRAF)
Protect, detect, respond, recover

AI risk guidelines (Sep 2025)
Human oversight, explainability

PDPA
Personal data: purpose, minimum, security

BOT may need to approve this change before go-live (FPG 19/2560 cl. 5.5, up to 30 business days): plan for it now.

6

Notes: Verified 19 Nov 2026 against primary sources (URLs in the references slide).

BIAN: release 14.0 (Feb 2026); service domains are elemental, mutually exclusive and collectively exhaustive business capabilities - a direct basis for service boundaries.
microservices.io (Chris Richardson): decomposition by business capability and subdomain; data patterns.
NIST SP 800-204 (Aug 2019), 204A service mesh (May 2020), 204B ABAC (Aug 2021), 204C DevSecOps (Mar 2022); 204D software supply chain (Feb 2024) also relevant to pipelines.
FAPI 2.0 Security Profile approved Final 19 Feb 2025. OAuth 2.1 is still an IETF draft, so we cite FAPI 2.0 as the binding profile.
CloudEvents graduated in CNCF Jan 2024. AsyncAPI 3.1 is current. W3C Trace Context Level 1 is a Recommendation (Nov 2021).
DMN 1.6 formal Sep 2026; Apache KIE Drools supports DMN at conformance level 3 and DMN 1.6 since 10.2.0. Note XLS decision tables are a Drools-native format, separate from DMN.
Temporal: ANZ case study (home-loan origination); JPMorgan Chase talk at Replay 2024 (payments modernisation).

FPG 19/2560 (Regulations on IT Risk Management of Financial Institutions), announced 20 Dec 2017, effective 1 Apr 2018. Clause 5.5: first-time use of a technology, or a change that may pose significant risk, needs a board-approved plan submitted to BOT for approval before proceeding; BOT decides within 30 business days. This is a programme dependency: the date for submission belongs in the plan.

FPG 19/2559 (Regulation…
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

## Temporal and Drools platform slides

## Slide 8

Example: a customer dies, the case pauses, the legal clock does not

S8 deviation X3 (deceased) on case RW-2026-000502

Flag X3
officer or agent, same day

Pause stage clock
prescription keeps running

Route to owner
specialist + Legal

Stop contact
no letters, no calls

Resolve
resume, or re-decide route

Stage clock

Prescription clock

PAUSED

X3 raised 10 Dec

resolved: resume

escalates if not resolved in 10 working days

Temporal can pause one timer and keep another running, so legal deadlines are never missed.

8

Notes: From FSD S8 v3: case RW-2026-000502, X3 raised 10 Dec 2026, paused at state WITH_FCR_OFFICER, contact stopped. Flag: same day; the stage clock pauses while the prescription clock keeps running (R-DEV-01, EV-06). Routing to the owner by code (R-DEV-02 to 06); X3 goes to the specialist and Legal. Contact stop for X1 to X3. Resolve: resume the paused state (R-DEV-18, EV-07) or re-route to the route decision D6 (R-DEV-19). Escalation on SLA breach after 10 working days (R-DEV-20).

In Temporal terms: the deviation is a signal; the workflow pauses its stage timer (TimerScheduler.pause/resume) but not the prescription timer.
## Slide 11

Runtime view: what runs where

Each of the 19 Recovery services has the same shape: its own Temporal worker and queue, an embedded Drools engine, its own schema

Officer / approver
Workbench screens

ONE RECOVERY SERVICE  (e.g. rwb-treatment; all 19 alike)

API
start case, approve

Temporal worker
polls rwb-treatment only

Drools engine
RuleEvaluator, model cache

Activities
EvaluateRules · RecordAndApply

Own schema
state + decision record

Outbox
→ Kafka

TEMPORAL CLUSTER  (shared, one per environment)

Frontend + history
remembers every step

own
persistence DB

Namespace rwb-recovery
one queue per service: rwb-case, rwb-treatment … (19)

ace-collection
Nexus: calculator

RULE GOVERNANCE  (rwb-decision, P7)

Rule models + central ledger
approve, publish EV-30 · seal decision records

1 click

2 poll queue

3 run step

4 ask

5 save

same transaction

Key

Temporal (runs)

Drools (decides)

People / approval

Data and log

ACE

Outside

Temporal remembers and waits; Drools answers inside a step; each service keeps its own state and decision records.

11

Notes: C4 container view, aligned to Recovery Microservice Architecture v5: Recovery stays part of ACE and is cut into 19 services, one per module (P1 to P10, S1 to S9). The slide shows one of them (for example rwb-treatment); all 19 have this shape. Each service packages its own Temporal worker and the embedded Drools runtime (KIE libraries only: drools-engine, drools-mvel, drools-decisiontables, drools-xml-support; no KIE Server, no Business Central, no KJAR - T3).

Temporal: one shared cluster per environment on ACE AKS with its own persistence database (no grant on the ACE database). Namespace rwb-recovery with one task queue per service (rwb-case, rwb-treatment, rwb-litigation and so on); each service's worker polls only its own queue and KEDA scales workers on backlog. ace-collection is ACE's namespace, reached through Nexus (for example the restructure calculator). Version 1.30+ for Nexus and Worker Versioning.

Data: the ACE PostgreSQL server, one schema and one login per service (rwb_<service>); no cross-schema joins. Temporal holds no case of record (T1). Payloads encrypted by the codec (AES-GCM, keys in Key Vault per namespace). Temporal UI behind Entra ID; RW-PLATADM operate, RW-AUDIT read, RW-SECADM decode (break-glass).

One transaction: the service writes its state change, the decision record and the outbox row together. The outbox relay publishes to Kafka (rwb.<service>.events.v1 and rwb.decision-record.v1).

Rules: rwb-decision (P7) governs rule models (author, test, four-…
## Slide 12

Temporal in five layers: Recovery owns the top two, the platform the rest

The bottom layers are owned once by the platform team and reused by every workbench

L5

Domain workflows
CaseWorkflow + stage children: Treatment, Litigation, Debt sale …

each service team

L4

Activity contracts per service
on rwb-<svc>: EvaluateRules, RecordAndApply, Payment.postProceeds · Nexus

each service team

L3

Workflow kit (versioned library)
Approval · Human task with SLA · Saga runner · Scheduled job · Notify · Partner instruction

platform team

L2

Namespaces
ace-collection · rwb-recovery · next workbench: own quotas, certs, keys

platform team

L1

Temporal cluster
one per environment on ACE AKS · own DB · UI · codec server · 1.30+

platform team

Recovery-specific above · shared platform, owned once, below

WHERE S1–S9 USE THE KIT

Approval (DoA)

S1 route · S2, S3, S5–S7 approvals

Human task with SLA

every officer task and escalation

Saga runner

S2 settlement · S5 auction · S6 · S7

Scheduled job

JOB-16 write-off scan · overnight jobs

Partner instruction

law firms, vendors, agencies (S4, S5, S9)

WHERE DROOLS SITS

Inside L4 activities of the owning service, never in workflow code.
Rule models are governed once in rwb-decision and copied to each owner.

Another workbench gets a namespace and the kit, and writes only its own domain workflows.

12

Notes: From Recovery Microservice Architecture v5, slide 23.
L1 cluster: one Temporal cluster per environment on ACE AKS, own persistence database, UI, metrics and codec server; upgrade to 1.30 or later for Nexus and Worker Versioning.
L2 namespaces: one per workbench (ace-collection, rwb-recovery, the next one), each with its own retention, rate limits, certificates and encryption keys.
L3 workflow kit: a versioned library of generic templates with no business terms in their interfaces: Approval (maker-checker, DoA lookup as a parameter), Notify, Document intake, Agent run with rule fallback, Human task with SLA timers, Saga runner, Scheduled job, Partner instruction.
L4 activity contracts: each service publishes typed activity interfaces on its queue rwb-<service>, plus Nexus endpoints for callers in other namespaces. EvaluateRules and RecordAndApply live here, in the service that owns the decision.
L5 domain workflows: CaseWorkflow and the stage workflows.

How S1 to S9 use the kit: Approval for route approval (S1), DoA approvals (S2, S3, S5, S6, S7) and rule sign-off; Human task with SLA for every officer task; Saga runner for settlement and deed in lieu (S2), auction (S5), debt sale (S6) and wr…
## Slide 13

Workflow model: a parent per case, a child per stage, the same four steps for every event

CaseWorkflow on rwb-case tracks the case; each stage runs as a child workflow in the service that owns it

Any stage workflow
on its owner's queue

1  Event arrives
Kafka → case router → signal

2  EvaluateRules
Drools: package, version, rule

3  RecordAndApply
record + state + outbox, one transaction

4  Wait
durable timer or next signal

repeat

PARENT AND CHILDREN  (one queue per owning service)

CaseWorkflow · rwb-case
one per case, entry to closure

starts one child workflow per stage  ↓

Route decision
rwb-valuation  ·  S1

Treatment
rwb-treatment  ·  RES 37 · SET 27 · DIL 37

Guarantee claim
rwb-guarantee  ·  GUA 32

Litigation
rwb-litigation  ·  LIT 79

Asset disposal
rwb-asset  ·  DIS 72

Debt sale
rwb-debtsale  ·  DS 41

Write-off
rwb-writeoff  ·  WO 51

Deviation (any time)
rwb-deviation  ·  DEV 22

Continue-As-New at each stage end, at least every 28 days

The parent tracks the case; each stage runs where its rules and data live, always as receive, ask, record and apply, wait.

13

Notes: Aligned to Recovery Microservice Architecture v5 (slides 23 to 25). CaseWorkflow (workflow ID = case ID; ADR-011 writes it as case-{caseId}) runs on task queue rwb-case in namespace rwb-recovery from entry to closure. Each stage is a child workflow started on the owner's queue: RouteDecisionWorkflow (rwb-valuation, with ApprovalWorkflow from the kit on rwb-decision), TreatmentWorkflow (rwb-treatment: restructure, settlement, deed in lieu), GuaranteeClaimWorkflow (rwb-guarantee), LitigationWorkflow (rwb-litigation), AssetDisposalWorkflow (rwb-asset), DebtSaleWorkflow (rwb-debtsale), WriteOffWorkflow (rwb-writeoff), DeviationWorkflow (rwb-deviation, can start at any time and pauses the stage clock).

Each route set's rules run in the service that owns the stage; UNIVERSAL rules (R-UNI) apply in every service.

Events from other services reach the case through the case router in rwb-case (Kafka consumer, signalWithStart), never by direct calls; the parent forwards them to the running child. Inside every workflow the same four steps repeat: receive, ask Drools (EvaluateRules activity), record and apply in one transaction (RecordAndApply activity), wait.

History: Continue-As-New at every stage end and at least every 28 days keeps each run far below Temporal's limit of 51,200 events or 50 MB. Children use parent close policy ABANDON so they survive the parent's Continue-As-New. Search attributes: CaseId, Stage, ProductGroup, QueueCode.

This replaces the one-lo…
