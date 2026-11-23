# Recovery Workbench Architecture v5 Text Extract v1

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

Source: `Proposed Arch\Recovery Microservice Architecture v5.pptx` (read-only).

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

FPG 19/2559 (Regulations on IT Outsourcing for Business Operations of Financial Institutions): board-approved outsourcing policy and risk framework; notify BOT for private cloud from providers outside the group, seek approval for public cloud used for critical IT, both 30 days before use. Not checked whether later rules supersede it; Compliance to confirm.

Cyber Resilience Assessment Framework (CRAF), issued around 2018: six areas listed. No standalone CRAF document found on bot.or.th; source is a BOT payment systems report.

BOT AI Risk Management Guidelines issued 12 Sep 2025 after public hearing 12-30 Jun 2025 (date from a secondary source; Compliance to confirm).

These are summaries for architecture purposes, not legal advice; Compliance owns the interpretation.

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

## Slide 8

System architecture: every runtime part and how it connects

C4 level 2 for Recovery inside the shared ACE cluster; line style shows the call type

Staff
browser

Azure App Gateway + WAF (shared)   /  and  /api/*  → ACE        /recovery/*  and  /api/recovery/*  → Recovery gateway-bff

ACE AKS CLUSTER · SHARED

ACE

ACE frontend + backend

ACE COMMON (SHARED)

Sign-in & access checks

Audit & PII logging

Shared case view

Restructure calculator

Notification path

Shared entities

gateway-bff
Redis session · JWT

Key Vault · codec server
payload keys (AES-GCM)

Partner gateway
FAPI 2.0 → S9

RECOVERY · 19 SERVICES · namespace rwb-recovery

Case &
control

P3
Case

P7
Decision

P4
Access

S8
Deviation

Routes

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

Shared

P5
Document

P6
Comms

P8
Payment

S9
Partner

P2
Integration

Data & AI

P1
Source data

P9
Reporting

P10
Agent

Kafka
events

Airflow
bank, to discuss

Observability
OpenTelemetry

Temporal (shared)
task queue per service

ACE PostgreSQL · ACE schemas + 30 recovery.v_ace_* views · 19 rwb_* schemas, one login each

Blob (WORM) · documents

Temporal persistence (own DB)

OUTSIDE THE CLUSTER

Partners
law firms, agencies, buyers

Entra ID
sign-in via ACE Common

NSS SMS · LINE OA
via ACE notification path

WIN
daily letters file (INT-14)

Debt buyers
encrypted files (INT-25)

Enterprise AI
private endpoint (INT-23)

SOC / SIEM
via ACE PII logging

Data lake / Power BI
not connected (INT-19/20 removed)

Calls

REST (sync, one hop)

Kafka event

Temporal activity / child / Nexus

SQL view (read-only)

File (claim-check)

8

Notes: Edge: staff reach the shared Azure App Gateway (WAF); / and /api/* go to ACE, /recovery/* and /api/recovery/* go to the Recovery gateway-bff (Spring Cloud Gateway, session in Redis, sign-in through ACE Common). Partners use the partner gateway (FAPI 2.0) that fronts rwb-partner.

Recovery: 19 services in the rwb-recovery namespace, each an api and a worker deployment. Calls: REST from the BFF (one hop); Kafka business-event topics (outbox and relay in each service); Temporal task queue rwb-<service> in namespace rwb-recovery; Nexus to ACE for the restructure calculator.

Data: one ACE PostgreSQL server. ACE schemas and the 30 recovery.v_ace_* views (read only by rwb-source-data); 19 Recovery schemas, one login and connection pool each; Temporal persistence in its own database; documents in Blob with WORM.

Outside: Enterprise AI (INT-23) from rwb-agent; WIN file (INT-14) and debt-buyer files (INT-25) from rwb-integration via MFT/SFTP; SMS and LINE through the ACE notification path; logs to SOC through ACE PII logging. No data lake.

Airflow in the platform row is the bank's enterprise scheduler, replacing Control-M (for discussion). It runs the overnight chain, file windows and report extracts and calls Recovery APIs only; per-case work stays in Temporal.

## Slide 9

System architecture on one page: the full picture

Same design with the detail: Kafka settings, the five Temporal layers, the 19 schemas and a sample event

9

Notes: This is the one-page diagram for the architecture team; the editable source is 'Recovery System Architecture v5.excalidraw' next to this deck, and the high-resolution PNG prints on A3.

Read it top to bottom: staff and partners enter through the shared App Gateway; gateway-bff makes one REST hop to the owning service; each of the 19 services in namespace rwb-recovery publishes to its own Kafka topic, polls its own Temporal task queue and reads and writes only its own rwb_* schema on the ACE PostgreSQL server.

Kafka: topic per service rwb.<name>.events.v1, 12 partitions, replication factor 3, 7-day retention, key caseId, CloudEvents binary mode, outbox and inbox, retry 1 min, 10 min, 1 h then .dlt; Event Hubs Premium is the fallback.

Temporal: shared with ACE, one cluster per environment. L1 cluster, L2 namespaces ace-collection and rwb-recovery, L3 versioned workflow kit, L4 activity contracts and Nexus (restructure.calculate in ACE), L5 domain workflows. Temporal keeps its own persistence database.

Data: only rwb-source-data reads the 30 recovery.v_ace_* views. Documents go to Blob with WORM through rwb-document only. The data lake and Power BI are not connected (INT-19 and INT-20 removed).

Airflow (amber, for discussion): the bank's scheduler, replacing Control-M, sits outside the cluster. (1) It runs the ACE ingestion DAG. (2) Its last task tells rwb-source-data the business date is ready, then waits for DailyCaseRun. (3) It opens the WIN and debt-buyer file windows. (4) It triggers report extracts in rwb-reporting. (5) It runs cutover loads and backfills. It calls APIs only and never reads rwb_* schemas.

The sample PaymentMissed event shows what travels on Kafka: CloudEvents headers, key caseId, IDs and facts only, no personal data.

## Slide 10

Walkthrough: an officer opens a case in about 1.2 seconds

Two services are asked at the same time, one hop each; other tabs load when clicked

Officer browser

App Gateway

gateway-bff

1

ACE Common
sign-in, JWT

2

rwb-case
GET /v1/cases/{id}

rwb-source-data
GET /v1/customers/{id}, /accounts/{id}

3

schema rwb_case (case, stage, tasks)

ACE DB · recovery.v_ace_* views (read-only)

④ merge both answers into the screen

Response budget (95th percentile)

0.15

two calls in parallel 0.6 s

merge 0.3 s

headroom to the 2 s target

gateway and session 0.15 s + slowest call 0.6 s + merge 0.3 s ≈ 1.05 s; budgeted at about 1.2 s

Other tabs load on click, each from its owner, one hop:

Documents
rwb-document

Notices
rwb-comms

Payments
rwb-payment

Legal
rwb-litigation

Screens never chain calls: the gateway asks each owner directly, in parallel, and only for what is on screen.

10

Notes: Steps: (1) the browser calls /api/recovery/cases/{id} through the App Gateway; (2) gateway-bff checks the session in Redis, gets a short-lived JWT through ACE Common sign-in and checks the coarse permission; (3) in parallel it calls rwb-case GET /v1/cases/{id} (case, stage, tasks, timers from schema rwb_case) and rwb-source-data GET /v1/customers/{id} and /v1/accounts/{id} (ACE data through the v_ace_* views, masked by policy); (4) it merges the two answers into the screen model.

Budget (p95): gateway and session 0.15 s, slowest of the two parallel calls 0.6 s, composition and transfer 0.3 s, total about 1.2 s against the 2 s target.

Each service authorises the object itself (OWASP API1 object-level authorisation), using cached permission data from rwb-access. Timeouts 2 s, circuit breaker per downstream, GET retry once with jitter.

## Slide 11

Five call types, each with a fixed contract

What every call between services must follow: transport, contract, identity, failure handling

REST

BFF

svc

Event (Kafka)

svc

topic

group

Temporal

wf

queue

worker

File

svc

Blob

party

SQL view

P1

v_ace_*

|  | REST | Event (Kafka) | Temporal | File | SQL view |
|---|---|---|---|---|---|
| Use when | A person waits for the answer | A fact others may react to | A step in another service, or a long process | Bulk data, or a party outside the bank | Reading ACE data (rwb-source-data only) |
| Transport | HTTPS/JSON, mesh mTLS | Kafka over TLS; CloudEvents 1.0, binary mode | Temporal gRPC over mTLS; queue rwb-<svc> | Blob + MFT/SFTP; PGP for outside parties | PostgreSQL TLS; read-only login |
| Contract | OpenAPI 3.1; /v1 in the path | AsyncAPI 3.0; JSON Schema registry, backward compatible | Typed activity / workflow interface in a contract jar | Manifest: fileId, batchId, sha256, record count | 30 recovery.v_ace_* views (ADR-010) |
| Identity | User JWT from BFF + workload identity | OAUTHBEARER (Entra) or mTLS; topic ACLs | Namespace mTLS; worker identity per service | SAS link, one file, 15 minutes | One login: rwb_source_data |
| Timeout, retry | 2 s; retry GET only (once, jitter); breaker + bulkhead | Retry topics 1 min / 10 min / 1 h, then .dlt + alert | Start-to-close per activity; backoff; heartbeats | Retried by the workflow; checksum on receipt | 5 s statement timeout |
| Duplicates, order | Idempotency-Key on every POST | Key = caseId (order per case); inbox dedupe | Workflow ID = business key; activities idempotent | fileId unique; re-delivery safe | Read only |
| Errors | RFC 9457 problem details | Dead-letter topic; replay tool | Typed failures; non-retryable list; saga undo | FileFailed event; operator retry | Mapped to domain errors by P1 |
| Never | Call chains (depth > 1) | Personal data in events | I/O or PII in workflow code or payloads | Data inside the message | Any other service reading the views |


Every service publishes its contracts (OpenAPI, AsyncAPI, activity jar) before code; contract tests run in every build.

11

Notes: These are engineering standards for every team; the architecture review checks them per service.

REST: depth one only (browser → BFF → owner, or a cached reference read). Commands carry Idempotency-Key; errors as RFC 9457 problem details; Resilience4j circuit breaker and bulkhead per downstream.

Event: Kafka, CloudEvents 1.0 Kafka binding in binary mode (ce_* headers), JSON Schema registry with BACKWARD compatibility, AsyncAPI 3.0 per topic. Transactional outbox in the producer's schema; idempotent producer with acks=all; inbox table (processed_event) in each consumer; retry topics and dead-letter topic with alert.

Temporal: activity and workflow interfaces are published as a contract jar per service; callers import only the interface and call the owner's task queue. Payloads pass through the codec (AES-GCM, keys in Key Vault). Nexus for calls into another namespace (ACE).

File: claim-check. The message carries a SAS link and a manifest, never the data. Outside parties via MFT/SFTP with PGP.

SQL view: only rwb-source-data, read-only login, 30 views, statement timeout.

## Slide 12

Choosing the call type: four questions

Ask in order; the first yes decides

Q1

Is a person waiting on the screen?

no

Q2

Did something happen that others may care about?

no

Q3

Must another service do a step, and we need the result?

no

Q4

Bulk data, or a party outside the bank?

Is it a read, or one quick command in one service?

yes

REST call to the owner
one hop from gateway-bff; 2 s budget

Start a Temporal workflow
return its ID; screen shows progress

yes

no

Publish an event (Kafka)
past tense fact; IDs only; outbox

Temporal activity, child workflow or Nexus
short step / long stage / another workbench

File through rwb-integration
claim-check: link + manifest, never the data

yes

yes

yes

Need ACE data?  Ask rwb-source-data (REST for screens, activity in workflows). Only rwb-source-data reads the SQL views, so a change in ACE is absorbed in one place.

Events announce, Temporal commands, REST answers people: never mix the three.

12

Notes: This decision guide is part of the engineering standard. Typical examples: officer opens a case (REST); a payment is missed (event PaymentMissed); the case workflow needs a route decision (child workflow on rwb-valuation); rwb-litigation needs a law firm instructed (activity issueInstruction on rwb-partner); daily WIN letters (file through rwb-integration); restructure calculation in ACE (Nexus operation).

Anti-patterns rejected in review: REST from one service to another inside a business step (use Temporal); events used as commands (use Temporal); a service reading another service's schema (use its API); a workflow calling REST directly from workflow code (wrap it in an activity).

## Slide 13

Who calls whom: the full connection matrix

Row = the service that starts the interaction; column = the service it calls or listens to

| starts ↓ / target → | P3 | P7 | P4 | S8 | S1 | S2 | S3 | S4 | S5 | S6 | S7 | P5 | P6 | P8 | S9 | P2 | P1 | P9 | P10 | ACE Cmn | ACE DB | Outside |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| P3 Case |  | E | R | T E | T E | T E | T E | T E | T E | T E | T E | E | E | E | E |  | T E |  |  |  |  |  |
| P7 Decision |  |  | R |  |  |  |  |  |  |  |  |  | E |  |  |  |  |  | E |  |  | F |
| P4 Access |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | R |  |  |
| S8 Deviation | E |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | R E |  | T E |  |  |  |
| S1 Valuation |  | T E |  |  |  |  |  |  |  |  |  |  |  |  |  |  | R |  | T |  |  |  |
| S2 Treatment |  | T E |  | E |  |  |  |  |  |  |  | T |  | T E |  |  |  |  |  | N |  |  |
| S3 Guarantee |  | T |  |  |  |  |  |  |  |  |  |  | T E | E |  |  |  |  |  |  |  |  |
| S4 Litigation |  | T |  |  |  |  |  |  |  |  |  |  | T E |  | T E |  |  |  |  |  |  |  |
| S5 Asset |  | T |  |  |  |  |  | E |  |  |  |  |  | T E | T E |  |  |  |  |  |  |  |
| S6 Debt sale |  | T |  |  |  |  |  |  |  |  |  | T |  | T E |  | T |  |  |  |  |  |  |
| S7 Write-off |  | T |  |  |  |  |  |  |  |  |  |  |  | T E |  |  | R E |  |  |  |  |  |
| P5 Document |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | T E |  |  | F |
| P6 Comms | E | T |  | E |  | E |  |  |  |  |  | T |  | E |  | T |  |  |  | R |  |  |
| P8 Payment |  | E |  |  |  | E |  |  | E | E | E |  |  |  |  | T | T E |  |  |  |  |  |
| S9 Partner |  |  |  |  |  |  |  |  |  |  |  | R |  |  |  |  |  |  |  |  |  | R |
| P2 Integration |  |  |  |  |  |  |  |  |  |  |  | R |  |  |  |  |  |  |  |  |  | F |
| P1 Source data |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | S |  |
| P9 Reporting | E |  |  |  |  | E | E |  |  | E | E |  | E |  |  | T | T |  |  |  |  |  |
| P10 Agent | E |  |  |  |  |  |  |  |  |  |  | R E |  |  |  |  | R |  |  |  |  | R |


Cells

T Temporal / N Nexus

R REST

E listens to events

S SQL views

F file

Route services reach shared capabilities through Temporal, never REST; only rwb-source-data touches ACE's tables.

13

Notes: Letters: R = REST call; T = Temporal (activity on the owner's queue or child workflow there); N = Nexus operation into ACE; E = subscribes to the column's Kafka events; S = SQL views; F = file. Built from the per-service contracts on the next slides.

Not shown because every service does it: audit and PII logs to ACE Common (Kafka), DecisionRecorded to rwb-decision, permission data cached from rwb-access, traces to OpenTelemetry.

Reading tips: rwb-case's row shows it orchestrates the route services through Temporal children; rwb-decision and rwb-reporting listen widely (ledger and projections) but call almost nobody; route services call shared capabilities (decision, document, payment, partner, comms) through Temporal, never through REST.

## Slide 14

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

## Slide 15

Service contracts 2/7 · Deviation, source data, reporting

IN = what the service accepts; OUT = what it writes and sends; the tag is the call type

IN

OUT

REST  GET/POST /deviations · POST /deviations/{id}/clear
EVT  CaseCreated (screening) · AceDataReady (deceased, bankrupt flags) · AgentRunCompleted
TMP  DeviationWorkflow (child of case)

DB  writes schema rwb_deviation: X1-X7 screening, pause, handling, return
EVT  rwb.deviation.events.v1: DeviationRaised, DeviationCleared
TMP  Agent: child: screening agent run
REST  Source data: party flags

S8 · rwb-deviation
Deviation handling
queue rwb-deviation
rwb.deviation.events.v1

IN

OUT

REST  GET /customers/{id}, /accounts/{id} · GET /collateral/{id}, /payments?accountId= · GET /freshness (business date) · POST /business-days/{date}/ready (Airflow)
EVT  (none: Airflow call; fallback polls ACE batch record)
TMP  Act: listEligibleAccounts, snapshot(page) · Workflow: AceIngestCheck, reconciliation

DB  writes schema rwb_source_data: ACE view contract, extension tables, freshness, reconciliation
EVT  rwb.source-data.events.v1: AceDataReady, AceDataLate (05:30)
SQL  ACE DB views: SELECT recovery.v_ace_* (30 views)

P1 · rwb-source-data
Source data
queue rwb-source-data
rwb.source-data.events.v1

IN

OUT

REST  GET /dashboards/{id} · GET /reports/{id} · POST /reports/{id}/run (Airflow)
EVT  All business events (projections) · DecisionRecorded
TMP  Schedule: measures 01:30 · Act: buildRegulatoryExtract

DB  writes schema rwb_reporting: measures, snapshots, steering dashboard, regulatory reports
EVT  rwb.reporting.events.v1: ReportPublished
TMP  Source data: snapshot(page) for measures · Integration: deliverFile (regulatory extract)

P9 · rwb-reporting
Reporting
queue rwb-reporting
rwb.reporting.events.v1

15

Notes: Contracts in full (also in the service catalogue in the appendix):

rwb-deviation (S8, Deviation handling)
IN: REST GET/POST /deviations; POST /deviations/{id}/clear | events CaseCreated (screening); AceDataReady (deceased, bankrupt flags); AgentRunCompleted | Temporal DeviationWorkflow (child of case)
OUT: schema rwb_deviation (X1-X7 screening, pause, handling, return) | topic rwb.deviation.events.v1: DeviationRaised, DeviationCleared | TMP Agent: child: screening agent run | REST Source data: party flags

rwb-source-data (P1, Source data)
IN: REST GET /customers/{id}, /accounts/{id}; GET /collateral/{id}, /payments?accountId=; GET /freshness (business date); POST /business-days/{date}/ready (Airflow) | events (none: Airflow call; fallback polls ACE batch record) | Temporal Act: listEligibleAccounts, snapshot(page); Workflow: AceIngestCheck, reconciliation
OUT: schema rwb_source_data (ACE view contract, extension tables, freshness, reconciliation) | topic rwb.source-data.events.v1: AceDataReady, AceDataLate (05:30) | SQL ACE DB views: SELECT recovery.v_ace_* (30 views)

rwb-reporting (P9, Reporting)
IN: REST GET /dashboards/{id}; GET /reports/{id} · POST /reports/{id}/run (Airflow) | events All business events (projections); DecisionRecorded | Temporal Schedule: measures 01:30; Act: buildRegulatoryExtract
OUT: schema rwb_reporting (measures, snapshots, steering dashboard, regulatory reports) | topic rwb.reporting.events.v1: ReportPublished | TMP Source data: snapshot(page) for measures · Integration: deliverFile (regulatory extract)

Tags: REST = synchronous HTTPS (OpenAPI 3.1); EVT = Kafka topic (CloudEvents, AsyncAPI); TMP = Temporal activity or child workflow on the owner's task queue; NEXUS = Temporal Nexus operation into another namespace; SQL = read-only view; FILE = claim-check file; DB = the service's own schema in the ACE database.

## Slide 16

Service contracts 3/7 · Agent, integration, document

IN = what the service accepts; OUT = what it writes and sends; the tag is the call type

IN

OUT

REST  GET /agent-runs/{id} · GET/POST /agent-policies (admin)
EVT  DocumentStored (intake) · CaseCreated (screening)
TMP  AgentRunWorkflow: 60 s, then rule result · Tool gateway: read-only calls for the agent

DB  writes schema rwb_agent: agent policies, prompts, runs, guardrails, evaluations
EVT  rwb.agent.events.v1: AgentRunCompleted
REST  Source data: tool: read case facts · Document: tool: read extracted fields · Enterprise AI endpoint: HTTPS private endpoint

P10 · rwb-agent
Agent runtime
queue rwb-agent
rwb.agent.events.v1

IN

OUT

REST  GET /interface-runs (operations) · POST /interface-runs/{id}/retry
EVT  (none: called as a task)
TMP  Act: deliverFile(manifest), receiveFile · Airflow window: WIN file 16:00, buyer files per lot

DB  writes schema rwb_integration: interface config, file runs, outbound items, ACE integration paths
EVT  rwb.integration.events.v1: FileDelivered, FileFailed
REST  Document: fetch file by ID (SAS link)
FILE  WIN (registered mail): daily outbound file (INT-14) · Debt buyers: per lot, encrypted (INT-25)

P2 · rwb-integration
Integration & files
queue rwb-integration
rwb.integration.events.v1

IN

OUT

REST  POST /documents (returns upload link) · GET /documents/{id}, /cases/{id}/documents · POST /documents/generate
EVT  AgentRunCompleted (classification)
TMP  DocumentIntakeWorkflow: OCR, classify, extract · Act: generate, seal · Schedule: retention

DB  writes schema rwb_document: metadata, custody, OCR text and fields, signatures, retention
EVT  rwb.document.events.v1: DocumentStored, DocumentFieldsExtracted
TMP  Agent: child: classify / extract run
FILE  Azure Blob (WORM): files, 2.8 TB by 2031

P5 · rwb-document
Document hub
queue rwb-document
rwb.document.events.v1

16

Notes: Contracts in full (also in the service catalogue in the appendix):

rwb-agent (P10, Agent runtime)
IN: REST GET /agent-runs/{id}; GET/POST /agent-policies (admin) | events DocumentStored (intake); CaseCreated (screening) | Temporal AgentRunWorkflow: 60 s, then rule result; Tool gateway: read-only calls for the agent
OUT: schema rwb_agent (agent policies, prompts, runs, guardrails, evaluations) | topic rwb.agent.events.v1: AgentRunCompleted | REST Source data: tool: read case facts · Document: tool: read extracted fields · Enterprise AI endpoint: HTTPS private endpoint

rwb-integration (P2, Integration & files)
IN: REST GET /interface-runs (operations); POST /interface-runs/{id}/retry | events (none: called as a task) | Temporal Act: deliverFile(manifest), receiveFile; Airflow window: WIN file 16:00, buyer files per lot
OUT: schema rwb_integration (interface config, file runs, outbound items, ACE integration paths) | topic rwb.integration.events.v1: FileDelivered, FileFailed | REST Document: fetch file by ID (SAS link) | FILE WIN (registered mail): daily outbound file (INT-14) · Debt buyers: per lot, encrypted (INT-25)

rwb-document (P5, Document hub)
IN: REST POST /documents (returns upload link); GET /documents/{id}, /cases/{id}/documents; POST /documents/generate | events AgentRunCompleted (classification) | Temporal DocumentIntakeWorkflow: OCR, classify, extract; Act: generate, seal · Schedule: retention
OUT: schema rwb_document (metadata, custody, OCR text and fields, signatures, retention) | topic rwb.document.events.v1: DocumentStored, DocumentFieldsExtracted | TMP Agent: child: classify / extract run | FILE Azure Blob (WORM): files, 2.8 TB by 2031

Tags: REST = synchronous HTTPS (OpenAPI 3.1); EVT = Kafka topic (CloudEvents, AsyncAPI); TMP = Temporal activity or child workflow on the owner's task queue; NEXUS = Temporal Nexus operation into another namespace; SQL = read-only view; FILE = claim-check file; DB = the service's own schema in the ACE database.

## Slide 17

Service contracts 4/7 · Communications, payment, partner

IN = what the service accepts; OUT = what it writes and sends; the tag is the call type

IN

OUT

REST  POST /notices (request) · GET /cases/{id}/notices
EVT  DeviationRaised / Cleared (contact stop) · TreatmentApproved, PaymentMissed · CaseStateChanged
TMP  NoticeDispatchWorkflow (kit template)

DB  writes schema rwb_comms: notices, templates, merge fields, proof of delivery
EVT  rwb.comms.events.v1: NoticeGenerated, NoticeDispatched, NoticeDelivered
TMP  Document: generate letter · Decision: child: approval · Integration: deliverFile (WIN letters)
REST  ACE Common: notification path (SMS, LINE)

P6 · rwb-comms
Communications
queue rwb-comms
rwb.comms.events.v1

IN

OUT

REST  GET /cases/{id}/payments · POST /proceeds/{id}/allocate (manual)
EVT  AceDataReady · TreatmentApproved, LotAwarded · AssetSold, WriteOffApproved
TMP  Act: matchPayments, confirmBookings · Act: postProceeds (saga step)

DB  writes schema rwb_payment: payment and proceeds matching, fees, bookings, posting files
EVT  rwb.payment.events.v1: TreatmentBooked, PaymentMissed, ProceedsMatched
TMP  Source data: payments for business date · Integration: deliverFile (posting file)

P8 · rwb-payment
Payments & posting
queue rwb-payment
rwb.payment.events.v1

IN

OUT

REST  Staff: GET/POST /partners, /instructions · Partner portal: /partner/v1/* (FAPI 2.0)
EVT  (work arrives as Temporal tasks)
TMP  InstructionWorkflow: SLA timers · Act: issueInstruction, recordResult

DB  writes schema rwb_partner: panel, partner users, instructions, results, fees, scorecards
EVT  rwb.partner.events.v1: InstructionIssued, PartnerResultSubmitted
REST  Document: partner uploads (link) · Partners (law firms, agencies, buyers): via partner gateway, MFA

S9 · rwb-partner
Partner management
queue rwb-partner
rwb.partner.events.v1

17

Notes: Contracts in full (also in the service catalogue in the appendix):

rwb-comms (P6, Communications)
IN: REST POST /notices (request); GET /cases/{id}/notices | events DeviationRaised / Cleared (contact stop); TreatmentApproved, PaymentMissed; CaseStateChanged | Temporal NoticeDispatchWorkflow (kit template)
OUT: schema rwb_comms (notices, templates, merge fields, proof of delivery) | topic rwb.comms.events.v1: NoticeGenerated, NoticeDispatched, NoticeDelivered | TMP Document: generate letter · Decision: child: approval · Integration: deliverFile (WIN letters) | REST ACE Common: notification path (SMS, LINE)

rwb-payment (P8, Payments & posting)
IN: REST GET /cases/{id}/payments; POST /proceeds/{id}/allocate (manual) | events AceDataReady; TreatmentApproved, LotAwarded; AssetSold, WriteOffApproved | Temporal Act: matchPayments, confirmBookings; Act: postProceeds (saga step)
OUT: schema rwb_payment (payment and proceeds matching, fees, bookings, posting files) | topic rwb.payment.events.v1: TreatmentBooked, PaymentMissed, ProceedsMatched | TMP Source data: payments for business date · Integration: deliverFile (posting file)

rwb-partner (S9, Partner management)
IN: REST Staff: GET/POST /partners, /instructions; Partner portal: /partner/v1/* (FAPI 2.0) | events (work arrives as Temporal tasks) | Temporal InstructionWorkflow: SLA timers; Act: issueInstruction, recordResult
OUT: schema rwb_partner (panel, partner users, instructions, results, fees, scorecards) | topic rwb.partner.events.v1: InstructionIssued, PartnerResultSubmitted | REST Document: partner uploads (link) · Partners (law firms, agencies, buyers): via partner gateway, MFA

Tags: REST = synchronous HTTPS (OpenAPI 3.1); EVT = Kafka topic (CloudEvents, AsyncAPI); TMP = Temporal activity or child workflow on the owner's task queue; NEXUS = Temporal Nexus operation into another namespace; SQL = read-only view; FILE = claim-check file; DB = the service's own schema in the ACE database.

## Slide 18

Service contracts 5/7 · Routes 1: valuation, treatment, guarantee

IN = what the service accepts; OUT = what it writes and sends; the tag is the call type

IN

OUT

REST  GET /cases/{id}/valuation · POST /cases/{id}/route-proposals
EVT  RulePackageInForce
TMP  RouteDecisionWorkflow (child of case)

DB  writes schema rwb_valuation: valuations, D6 route decision, route agent output
EVT  rwb.valuation.events.v1: RouteDecided
TMP  Agent: child: route agent · Decision: child: approval
REST  Source data: collateral, appraisals

S1 · rwb-valuation
Valuation & route
queue rwb-valuation
rwb.valuation.events.v1

IN

OUT

REST  GET/POST /treatments · POST /treatments/{id}/offer
EVT  TreatmentBooked, PaymentMissed · DeviationRaised
TMP  TreatmentWorkflow · settlement and DIL sagas

DB  writes schema rwb_treatment: treatments, contracts, settlement and deed-in-lieu agreements, plan timers
EVT  rwb.treatment.events.v1: TreatmentApproved, TreatmentClosed
TMP  Decision: child: approval · Document: contract, e-sign · Payment: postProceeds
NEXUS  ACE Common: restructure calculator (Nexus)

S2 · rwb-treatment
TDR, settlement, DIL
queue rwb-treatment
rwb.treatment.events.v1

IN

OUT

REST  GET/POST /guarantee-claims
EVT  NoticeDelivered · ProceedsMatched
TMP  GuaranteeClaimWorkflow

DB  writes schema rwb_guarantee: TCG and insurance claims, guarantor notices and pursuit
EVT  rwb.guarantee.events.v1: GuaranteeClaimFiled, GuaranteeClaimSettled
TMP  Comms: child: guarantor notice · Decision: child: approval

S3 · rwb-guarantee
Guarantees
queue rwb-guarantee
rwb.guarantee.events.v1

18

Notes: Contracts in full (also in the service catalogue in the appendix):

rwb-valuation (S1, Valuation & route)
IN: REST GET /cases/{id}/valuation; POST /cases/{id}/route-proposals | events RulePackageInForce | Temporal RouteDecisionWorkflow (child of case)
OUT: schema rwb_valuation (valuations, D6 route decision, route agent output) | topic rwb.valuation.events.v1: RouteDecided | TMP Agent: child: route agent · Decision: child: approval | REST Source data: collateral, appraisals

rwb-treatment (S2, TDR, settlement, DIL)
IN: REST GET/POST /treatments; POST /treatments/{id}/offer | events TreatmentBooked, PaymentMissed; DeviationRaised | Temporal TreatmentWorkflow · settlement and DIL sagas
OUT: schema rwb_treatment (treatments, contracts, settlement and deed-in-lieu agreements, plan timers) | topic rwb.treatment.events.v1: TreatmentApproved, TreatmentClosed | TMP Decision: child: approval · Document: contract, e-sign · Payment: postProceeds | NEXUS ACE Common: restructure calculator (Nexus)

rwb-guarantee (S3, Guarantees)
IN: REST GET/POST /guarantee-claims | events NoticeDelivered; ProceedsMatched | Temporal GuaranteeClaimWorkflow
OUT: schema rwb_guarantee (TCG and insurance claims, guarantor notices and pursuit) | topic rwb.guarantee.events.v1: GuaranteeClaimFiled, GuaranteeClaimSettled | TMP Comms: child: guarantor notice · Decision: child: approval

Tags: REST = synchronous HTTPS (OpenAPI 3.1); EVT = Kafka topic (CloudEvents, AsyncAPI); TMP = Temporal activity or child workflow on the owner's task queue; NEXUS = Temporal Nexus operation into another namespace; SQL = read-only view; FILE = claim-check file; DB = the service's own schema in the ACE database.

## Slide 19

Service contracts 6/7 · Routes 2: litigation, asset, debt sale

IN = what the service accepts; OUT = what it writes and sends; the tag is the call type

IN

OUT

REST  GET/POST /legal-actions · GET/POST /hearings
EVT  NoticeDelivered · PartnerResultSubmitted
TMP  LitigationWorkflow (years; continues-as-new)

DB  writes schema rwb_litigation: legal actions, hearings, judgments, enforcement, LED auction ladder
EVT  rwb.litigation.events.v1: LawsuitFiled, JudgmentRecorded, AuctionResult
TMP  Partner: issueInstruction (law firm) · Comms: child: demand notice · Decision: child: approval

S4 · rwb-litigation
Litigation & enforcement
queue rwb-litigation
rwb.litigation.events.v1

IN

OUT

REST  GET/POST /assets, /listings · POST /auction-rounds
EVT  JudgmentRecorded, AuctionResult · ProceedsMatched
TMP  AssetDisposalWorkflow · Schedule: re-appraisal monthly

DB  writes schema rwb_asset: assets taken on, holding, floor price, listings, auction rounds
EVT  rwb.asset.events.v1: AssetTakenOn, AssetSold
TMP  Partner: issueInstruction (auction vendor) · Decision: child: approval · Payment: postProceeds

S5 · rwb-asset
Assets & auction
queue rwb-asset
rwb.asset.events.v1

IN

OUT

REST  GET/POST /lots · POST /lots/{id}/bids · /award
EVT  ProceedsMatched
TMP  DebtSaleWorkflow (saga, pivot = transfer)

DB  writes schema rwb_debtsale: lots, data room, buyer terms, bids, award, transfer
EVT  rwb.debtsale.events.v1: LotAwarded, AccountsTransferred
TMP  Document: data room pack · Decision: child: approval · Integration: deliverFile (buyer file) · Payment: postProceeds

S6 · rwb-debtsale
Debt sale
queue rwb-debtsale
rwb.debtsale.events.v1

19

Notes: Contracts in full (also in the service catalogue in the appendix):

rwb-litigation (S4, Litigation & enforcement)
IN: REST GET/POST /legal-actions; GET/POST /hearings | events NoticeDelivered; PartnerResultSubmitted | Temporal LitigationWorkflow (years; continues-as-new)
OUT: schema rwb_litigation (legal actions, hearings, judgments, enforcement, LED auction ladder) | topic rwb.litigation.events.v1: LawsuitFiled, JudgmentRecorded, AuctionResult | TMP Partner: issueInstruction (law firm) · Comms: child: demand notice · Decision: child: approval

rwb-asset (S5, Assets & auction)
IN: REST GET/POST /assets, /listings; POST /auction-rounds | events JudgmentRecorded, AuctionResult; ProceedsMatched | Temporal AssetDisposalWorkflow; Schedule: re-appraisal monthly
OUT: schema rwb_asset (assets taken on, holding, floor price, listings, auction rounds) | topic rwb.asset.events.v1: AssetTakenOn, AssetSold | TMP Partner: issueInstruction (auction vendor) · Decision: child: approval · Payment: postProceeds

rwb-debtsale (S6, Debt sale)
IN: REST GET/POST /lots; POST /lots/{id}/bids · /award | events ProceedsMatched | Temporal DebtSaleWorkflow (saga, pivot = transfer)
OUT: schema rwb_debtsale (lots, data room, buyer terms, bids, award, transfer) | topic rwb.debtsale.events.v1: LotAwarded, AccountsTransferred | TMP Document: data room pack · Decision: child: approval · Integration: deliverFile (buyer file) · Payment: postProceeds

Tags: REST = synchronous HTTPS (OpenAPI 3.1); EVT = Kafka topic (CloudEvents, AsyncAPI); TMP = Temporal activity or child workflow on the owner's task queue; NEXUS = Temporal Nexus operation into another namespace; SQL = read-only view; FILE = claim-check file; DB = the service's own schema in the ACE database.

## Slide 20

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

## Slide 21

Event broker: Kafka, on the platform ACE already runs

Recovery gets its own business-event topics and access rules, separate from ACE's PII logging topics

Recommended: Apache Kafka on the bank / ACE platform
dedicated Recovery topics and ACLs · fallback: Event Hubs Premium (Kafka API)

Already part of ACE
ACE runs Kafka today (PII logging): no new platform or outsourcing review

Order per case
Record key = caseId, so one case's events arrive in order

Replay from history
A new or repurposed service rebuilds its view from the topic

Many independent listeners
One consumer group per service; the producer never changes

Same code on Azure if needed
Event Hubs Premium speaks the Kafka protocol

|  | Kafka (bank platform) | Event Hubs Premium | Service Bus Premium |
|---|---|---|---|
| Already used by ACE | Yes (PII logging) | No | No |
| Replay history | Yes, retention per topic | Yes, up to 90 days | No: removed when consumed |
| Order per case | Partition key = caseId | Partition key | Sessions |
| Many listeners | Consumer groups | Consumer groups | Topic subscriptions |
| Client code | Kafka client | Same Kafka client | Own SDK |
| Run by | Bank / ACE platform team | Azure (managed) | Azure (managed) |
| Role in this design | Recommended | Fallback | Not chosen |


Kafka: ACE already runs it, it keeps history for replay and reuse, and the same code moves to Event Hubs if ever needed.

21

Notes: Recommendation: host Recovery's business events on the bank Kafka platform that ACE already uses for PII logging, as dedicated topics with their own ACLs, quotas and schema subjects. Fallback: Azure Event Hubs Premium through its Kafka endpoint; the same producer and consumer code works.

Why Kafka for this design: (1) already operated for ACE, so no new platform and no new outsourcing assessment under FPG 19/2559; (2) ordering per case by using caseId as the record key; (3) retention and replay, so a new or repurposed service can rebuild its own view from history, which matters for the reuse goal; (4) independent consumer groups per service; (5) CloudEvents has a standard Kafka binding.

Why not Azure Service Bus: good for command queues with sessions and dead-lettering, but messages are removed once consumed (no replay), it is a new platform for ACE, and it needs its own SDK. Commands between services already go through Temporal, so we do not need a command queue.

To confirm with the ACE platform team: capacity (Recovery volume is small: tens of thousands of events a day), topic naming, ACL model, schema registry, environments.

## Slide 22

How an event travels: 'payment missed' from outbox to three listeners

Exactly-once effect from at-least-once delivery: outbox in the producer, inbox in each consumer

rwb-payment

matchPayments (activity)

rwb_payment: tables + outbox (one transaction)

outbox relay

nothing is lost if Kafka is down

rwb.payment.events.v1
key caseId · 12 partitions · RF 3 · 7 days

partitions (6 of 12 shown); red = PaymentMissed for RC-123

publish

rwb-case
group rwb-case · case router → signal to CaseWorkflow

rwb-treatment
group rwb-treatment · check plan breach

rwb-comms
group rwb-comms · send reminder notice

each consumer: inbox (processed_event) in its own schema, same transaction as its change

On failure

retry 1 min

retry 10 min

retry 1 h

.dlt + alert

ce_specversion: 1.0
ce_type: rwb.payment.PaymentMissed.v1
ce_source: /rwb-payment
ce_id: 01JD…7Q
ce_subject: case/RC-123
traceparent: 00-4bf9…-01
key: RC-123
{ "caseId": "RC-123",
  "treatmentId": "TR-9",
  "dueDate": "2026-11-15",
  "amountDue": 12500.00,
  "daysLate": 3 }

on the wire: headers, key, body (IDs and facts only)

Name
rwb.<service>.events.v1

Envelope
CloudEvents 1.0, binary mode

Schema
JSON Schema registry, backward compatible

Producer
outbox · idempotent · acks=all

Payload
IDs and business facts, no PII

The producer writes once and moves on; each listener reacts in its own time and a duplicate never acts twice.

22

Notes: Producer: rwb-payment's matchPayments activity updates its tables and inserts the event into its outbox table in the same database transaction (schema rwb_payment). The outbox relay publishes it with an idempotent producer (acks=all, min.insync.replicas=2) and marks it sent. If Kafka is down, events wait in the outbox.

Topic: rwb.payment.events.v1, 12 partitions, replication factor 3, 7-day retention, key caseId. CloudEvents 1.0 Kafka binding in binary mode: ce_id, ce_type, ce_source, ce_subject as headers, W3C traceparent header, JSON body validated against the registry (BACKWARD compatibility).

Consumers: one consumer group per service. Each records ce_id in its inbox table (processed_event) in the same transaction as its own change, so a redelivered event has no second effect. Failures go to retry topics (1 min, 10 min, 1 h) and then to the dead-letter topic with an alert and a replay tool.

rwb-case does not act itself: its case router turns the event into a Temporal signal (signalWithStart) on the CaseWorkflow.

## Slide 23

Temporal in five layers: the bottom four are reusable by any workbench

Platform layers are owned once; each workbench writes only its own domain workflows

L5

Domain workflows
CaseWorkflow (rwb-case) · RouteDecision, Treatment, Litigation, AssetDisposal, DebtSale, WriteOff, Deviation

each service team

L4

Service activity contracts
Typed interface per service on queue rwb-<svc>, e.g. Payment.postProceeds, Partner.issueInstruction · Nexus endpoints

each service team

L3

Workflow kit (versioned library)
Approval (maker-checker, DoA) · Notify · Document intake · Agent run + fallback · Human task with SLA · Saga runner · Scheduled job · Partner instruction

platform team

L2

Namespaces
ace-collection · rwb-recovery · next workbench: own retention, quotas, certificates and codec keys

platform team

L1

Temporal cluster
One per environment on ACE AKS; own persistence DB; UI, metrics, codec server; version 1.30+

platform team

ANOTHER WORKBENCH REUSES IT IN FOUR STEPS

1

Get a namespace
platform team sets quotas, certificates and keys

2

Add the workflow kit
e.g. Approval with its own DoA table

3

Call existing services
activity contracts or Nexus, e.g. rwb-comms notice, rwb-document intake

4

Write only its domain workflows
everything below L5 is reused

Rules that keep it reusable
No business terms in L1-L3 interfaces
Kit versioned; workers pinned (Worker Versioning)
All I/O in activities; Continue-As-New at stage ends
Payloads encrypted by the codec (AES-GCM)

green = Recovery-specific (L5, and L4 contracts owned by each service)   blue = shared platform, owned once

A new workbench gets a namespace and composes the kit and existing services: it writes only its own domain workflows.

23

Notes: L1 cluster: one Temporal cluster per environment on the ACE AKS cluster, with its own persistence database, UI, metrics and codec server; operated by the platform team. Upgrade from 1.28.1 to 1.30 or later for Nexus and Worker Versioning.

L2 namespaces: one per workbench (ace-collection, rwb-recovery, and the next one). Namespaces isolate retention, rate limits, certificates and encryption keys. A new workbench is a new namespace, not a new cluster.

L3 workflow kit: a versioned library (semantic versioning) of generic workflow templates with no business terms in their interfaces: Approval (maker-checker, DoA lookup as a parameter), Notify, Document intake, Agent run with rule fallback, Human task with SLA timers, Saga runner, Scheduled job, Partner instruction. Owned by the platform team; ACE can use it too.

L4 activity contracts: every service publishes a contract jar with typed activity interfaces on its task queue rwb-<service>, plus Nexus endpoints for callers in other namespaces. This is what makes a service reusable through Temporal.

L5 domain workflows: CaseWorkflow in rwb-case and stage workflows in the route services; specific to Recovery.

Rules for all layers: deterministic workflow code; all I/O in activities; Continue-As-New at stage ends and at least every 28 days; Worker Versioning for safe upgrades; payload codec AES-GCM.

## Slide 24

Temporal at runtime: one cluster, a namespace per workbench, a queue per service

Workers run inside each service and poll only their own queue; the numbers show four typical calls

TEMPORAL CLUSTER · SHARED, ONE PER ENVIRONMENT (L1)

ace-collection (L2)

ace-case

ace-collect

ace-notify

Nexus handler
restructure.calculate

rwb-recovery (L2) · one task queue per service

rwb-case

rwb-litigation

rwb-partner

rwb-decision

rwb-treatment

rwb-valuation

rwb-guarantee

rwb-deviation

rwb-asset

rwb-debtsale

rwb-writeoff

rwb-payment

rwb-document

rwb-comms

rwb-integration

rwb-agent

rwb-source-data

rwb-reporting

rwb-access

1

2

3

4

Workers live in each service's worker deployment and poll only their own queue; KEDA scales them on backlog.

Codec (AES-GCM, Key Vault) on every client and worker; codec server for the UI.

1

Child workflow
CaseWorkflow starts LitigationWorkflow on rwb-litigation

2

Activity
Litigation calls Partner.issueInstruction on rwb-partner

3

Nexus operation
Treatment calls ACE's restructure calculator across namespaces

4

Signal from an event
PaymentMissed → case router → signalWithStart CaseWorkflow

One cluster, isolated namespaces, one queue per service: a service is reusable through its queue and contract, not its code.

24

Notes: Each Recovery service runs its own Temporal worker in its worker deployment, polling only task queue rwb-<service> in namespace rwb-recovery. KEDA's Temporal scaler adds workers when the queue backlog grows and can scale bursty queues (document OCR, agent runs) to zero.

(1) Child workflow: CaseWorkflow on rwb-case starts LitigationWorkflow on rwb-litigation (parent close policy ABANDON, so the stage survives the parent's Continue-As-New). (2) Activity: LitigationWorkflow calls Partner.issueInstruction on rwb-partner; the worker of rwb-partner executes it and writes its own schema. (3) Nexus: TreatmentWorkflow calls the restructure calculator as a Nexus operation exposed by ace-collection; the namespaces stay isolated. (4) Signal: a Kafka event (PaymentMissed) reaches rwb-case's case router, which uses signalWithStart on the CaseWorkflow.

Data converter: every client and worker uses the payload codec (AES-GCM, keys in Key Vault per namespace); the codec server lets authorised staff read payloads in the Temporal UI.

## Slide 25

How the journey runs: one case workflow, with a child for each stage

The parent tracks the whole case; each stage runs in the service that owns it

CaseWorkflow  one per case, entry to closure · queue rwb-case · signals from the case router

child

Route decision
rwb-valuation + approval on rwb-decision

Deviation
rwb-deviation (any time)

Treatment / guarantee
rwb-treatment · rwb-guarantee

Litigation
rwb-litigation (years)

Asset / debt sale
rwb-asset · rwb-debtsale

Write-off
rwb-writeoff

time

Continue-As-New at every stage end and at least every 28 days

Timers that last for years
Court dates and letter deadlines survive restarts and upgrades

Events become signals
PaymentMissed, NoticeDelivered and others reach the case through the case router

Approvals from the kit
ApprovalWorkflow on rwb-decision, routed by authority (DoA)

Each stage runs on the queue of the service that owns it, so it scales, releases and can be reused with that service.

25

Notes: CaseWorkflow (rwb-case, workflow ID = case ID) is the parent from entry to closure. Each stage is a child workflow started on the owner's task queue: RouteDecisionWorkflow (rwb-valuation, with ApprovalWorkflow from the kit on rwb-decision), DeviationWorkflow (rwb-deviation, can start at any time and pauses the stage clock), TreatmentWorkflow (rwb-treatment) and GuaranteeClaimWorkflow (rwb-guarantee), LitigationWorkflow (rwb-litigation, can run for years), AssetDisposalWorkflow (rwb-asset) and DebtSaleWorkflow (rwb-debtsale), WriteOffWorkflow (rwb-writeoff).

Events from other services reach the case as signals through the case router (signalWithStart), never by direct calls.

History: Continue-As-New at every stage end and at least every 28 days keeps each run far below Temporal's limit of 51,200 events or 50 MB. Children use parent close policy ABANDON so they survive the parent's Continue-As-New.

## Slide 26

Deals that span services: undo before the point of no return, finish after it

Debt sale example: seven steps across five services, no shared transaction

Can still be undone

Must finish: retried until done

1. Reserve accounts
rwb-debtsale

2. Approve sale
rwb-decision

3. Buyer pays
rwb-payment

4. Transfer accounts
rwb-debtsale

5. Post proceeds
rwb-payment

6. Close cases
rwb-case

7. Tell customers
rwb-comms

Point of no return

undo: release accounts

undo: cancel approval

undo: refund buyer

If a step fails after this point it is retried, not undone

Settlement

Agree terms

Approve

Customer pays

Debt released

Post

Close case

Deed in lieu

Value asset

Approve

Sign deed

Title transferred

Book asset

Close case

Every step is a Temporal activity on the owner's queue; at each point of no return the ledger must confirm first.

26

Notes: Saga pattern (microservices.io), orchestrated by DebtSaleWorkflow in rwb-debtsale using the Saga runner from the workflow kit. Each step is a local transaction in one service's own schema, called as an activity on that service's queue. Before the pivot step, each completed step has a compensating activity. The pivot is the point of no return; after it, steps are retried until they succeed.

Strict decision-log mode applies at each pivot: the step waits for the central ledger acknowledgement before executing.

Other sagas: settlement and deed in lieu in rwb-treatment (pivots: debt released once the customer pays; title transfer registered).

## Slide 27

Rules: approved in one place, run inside the service that owns the decision

Business owns the rules; the workflow just asks for the answer

GOVERNED CENTRALLY · rule registry in rwb-decision (P7)

Author
Business writes the DMN decision table

Test
At least 50 test cases pass

Approve
Four-eyes sign-off

Publish
Event RulePackageInForce

RUN IN THE OWNING SERVICE (e.g. rwb-valuation)

Load
GET /rule-models/{n}/{v}, verify checksum, swap in

Evaluate
Inside an activity, under 300 ms

Record
Answer and model version in the decision record

Kafka: RulePackageInForce

Example

RouteDecisionWorkflow asks: which route for case 123?

Route model v14 answers: litigation (reasons L2, L5)

Decision record: v14, inputs, answer, approver

No shared rules server to fail: each service holds its own approved copy, and every answer names the version used.

27

Notes: Today (ADR-012): embedded Drools with XLS decision tables stored in the database; packages ENTRY, EXCLUSION, ALLOCATION, ASSIGNMENT, TRANSFER, RESTRUCTURE, PAYMENT_MATCH, BOOKING_MATCH, UNIVERSAL; route sets total 448 rules. RW-COE authors, RW-RISK approves, at least 50 test scenarios, JOB-20 promotes at 00:01, EV-30 RulePackageInForce refreshes the cache. DoA is reference data (delegation_limit). Rule evaluations 283-318k a month; target < 300 ms.

Proposal: OMG DMN 1.6 decision models (Drools supports DMN at conformance level 3). XLS decision tables are a Drools-native format compiled to DRL, separate from DMN; both run on the same Drools runtime, so tables are converted one at a time with no big bang.

Governance stays central in rwb-decision: authoring, test scenarios, four-eyes approval, effective dating, audit of every version. Evaluation is local: each model has exactly one owning service, which loads it, verifies the checksum, and swaps it atomically, keeping the last good model if a new one fails to load. This avoids a shared rule server on every hot path.

With Temporal: rules run in an activity, never in workflow code, so workflows stay deterministic and replays reuse the recorded result. The model name and version are written into the decision record.

## Slide 28

The decision log: recorded locally at once, then sealed centrally

Every decision can be traced and cannot be quietly changed

1

Saved with the change
The service writes the decision and the change in one transaction

2

Chained
Each record is linked to the one before, so gaps or edits show

3

Collected centrally
rwb-decision reads rwb.decision-record.v1 into the ledger within 5 minutes

4

Sealed daily
A fingerprint is stored in write-once storage

inside each of the 19 services

in rwb-decision (P7)

Strict mode for points of no return
Debt transfer, write-off, auction sale and title transfer wait until the central ledger confirms the record. Everything else carries on at full speed.

What auditors get
One place to search every decision, with the rule version and approver; alerts for missing records; the chain checked every day.

This changes ADR-009, so it needs Risk and Internal Audit sign-off.

28

Notes: Proposal (changes ADR-009): (1) each service writes a decision record in its own schema in the same transaction as the state change, hash-linked to the previous record, plus DecisionRecorded through its outbox to topic rwb.decision-record.v1; (2) rwb-decision consumes it idempotently into the central ledger, with a 5-minute completeness target, gap alerts and chain verification; (3) daily anchor of the ledger hash to immutable (WORM) storage.

Strict mode: irreversible steps (debt transfer, write-off, auction sale, title transfer) wait for the ledger acknowledgement before executing.

Why not today's design: writing the central log synchronously inside every call becomes a distributed transaction once there are 19 services. Needs Risk and Internal Audit sign-off.

## Slide 29

Data: one ACE database, one schema and one login per service

Ownership is enforced by grants, not by separate servers

rwb-case

login rwb_case

schema rwb_case: read and write

rwb-source-data

login rwb_source_data

recovery.v_ace_* views: SELECT only

rwb-litigation

login rwb_litigation

schema rwb_payment: no grant, refused

ACE POSTGRESQL SERVER · PgBouncer pool and connection cap per login

ACE-OWNED

ACE schemas: customer, account, payment, collateral, …

schema recovery: 30 v_ace_* views, SELECT only, for rwb_source_data

19 RECOVERY SCHEMAS · ONE LOGIN EACH

rwb_case

rwb_decision

rwb_access

rwb_deviation

rwb_valuation

rwb_treatment

rwb_guarantee

rwb_litigation

rwb_asset

rwb_debtsale

rwb_writeoff

rwb_document

rwb_comms

rwb_payment

rwb_partner

rwb_integration

rwb_source_data

rwb_reporting

rwb_agent

Temporal persistence: own database

Blob storage with WORM: documents (rwb-document only)

Own schema only
one login per service; grants on its own schema

No cross-schema joins or keys
hold IDs; ask the owner through its contract

Capped connections
PgBouncer pool per login protects ACE

Checked in every build
boundary test fails on a cross-schema reference

Own migrations
Flyway per service, in its own pipeline

Movable later
a schema can move to its own server: change the connection string

Same ACE database, clear ownership: a service writes only its own schema, and only rwb-source-data reads ACE's views.

29

Notes: Physical: the ACE PostgreSQL server (Azure Database for PostgreSQL). ACE's own schemas, plus schema recovery holding the 30 read-only v_ace_* views (ADR-010), plus 19 Recovery schemas rwb_<service>. Temporal keeps its persistence in its own database; documents are in Blob with WORM.

Rules: each service has one database login that owns its schema and has no grant on any other schema; only rwb_source_data has SELECT on the views. No cross-schema joins, views or foreign keys: services hold each other's IDs and use contracts for everything else. Each service runs its own Flyway migrations. A boundary test in every build fails on any cross-schema reference.

Protecting ACE: each login goes through its own PgBouncer pool with a connection cap and statement timeout; heavy reporting runs from rwb-reporting's own projections, not from ACE tables. Per-schema monitoring.

This is the schema-per-service variant of database per service (microservices.io): ownership and isolation are kept, and any schema can later move to its own server by changing its connection string, with no code change.

## Slide 30

What Recovery uses from ACE: the shared ACE Common services

Six connections, each with one owner, one contract and one call type; arrows point from caller to callee

Recovery

ACE Common (ACE team)

1

gateway-bff · rwb-access

REST / OIDC

sign-in, user JWT, group-to-role

Sign-in & access checks

2

all 19 services

Kafka (PII path)

audit and PII access logs → SOC

Audit & PII logging

3

rwb-case

REST

GET /case-summary/{id}

Shared case view (ACE case list)

4

rwb-treatment

Nexus

restructure.calculate (REST fallback)

Restructure calculator

5

rwb-comms

REST

send SMS / LINE message, delivery status

Notification path: NSS SMS, LINE OA

6

rwb-source-data

SQL views

30 recovery.v_ace_* views, read-only

Shared entities in the ACE database

Recovery reuses ACE's sign-in, logging, case view, calculator and notifications instead of building its own.

30

Notes: ACE Common is built and run by the ACE team; Recovery consumes it through versioned contracts (INT-34) with contract tests on both sides.

(1) Sign-in and access checks: gateway-bff and rwb-access use ACE's Entra-based sign-in; Recovery roles, scope, masking and DoA stay as data in rwb-access. (2) Audit and PII logging: every service sends audit and personal-data access logs through ACE's PII Kafka path to the SOC. (3) Shared case view: ACE's case list calls rwb-case GET /case-summary/{id}. (4) Restructure calculator: rwb-treatment calls it as a Nexus operation (REST fallback). (5) Notification path: rwb-comms sends SMS and LINE messages through ACE (NSS, LINE OA); WIN letters go as a file via rwb-integration. (6) Shared entities: customer, account, product, collateral and asset come from the ACE database through the views, read only by rwb-source-data.

## Slide 31

The overnight chain: everything ready before officers start at 07:00

Bank Airflow runs the cross-system chain; inside Recovery each job is a Temporal Schedule or an event

00:00

02:00

04:00

07:00

08:00

10:00

12:00

14:00

16:00

ACE ingestion
ACE · bank Airflow DAG

Rules, ledger, measures
rwb-decision · rwb-reporting

Create & allocate cases
rwb-case

Match payments
rwb-payment

Health check, rebalance
platform · rwb-case

Officers working

Customer letters
rwb-comms → rwb-integration

◆ Airflow: ACE ready (~04:30) → AceDataReady starts the run   ◆ AceDataLate alarm at 05:30   ◆ WIN letters file at 16:00

Temporal Schedules
in the service that owns the job

Started by events
AceDataReady triggers the morning run

Bank Airflow (to discuss)
says 'date ready'; SLA alerts 05:30, 07:00

Officers start at 07:00 with today's cases allocated; if ACE is late, the alarm goes off at 05:30.

31

Notes: ACE ingests the source systems into the ACE database overnight. The bank's Airflow (replacing Control-M; for discussion) runs the ACE ingestion DAG. Its last task calls rwb-source-data (POST /v1/business-days/{date}/ready, idempotent), which checks freshness and publishes AceDataReady; a sensor waits for DailyCaseRun and Airflow raises SLA alerts at 05:30 and 07:00. rwb-source-data still publishes AceDataLate at 05:30 with an alarm and a banner. Fallback if ACE ingestion is still on Control-M at go-live: rwb-source-data polls ACE's batch record, as today.

AceDataReady starts DailyCaseRun in rwb-case (case creation JOB-02, allocation JOB-03 by 07:00), payment matching and booking confirmation in rwb-payment (JOB-07, JOB-08), reconciliation in rwb-source-data (JOB-04) and deviation screening in rwb-deviation.

Temporal Schedules: rule promotion 00:01 (rwb-decision, JOB-20), measures 01:30 (rwb-reporting, JOB-15, from its own projections: no data lake), hash-chain check 02:00 (JOB-14), smoke workflow 06:00 (JOB-22), rebalancing 06:30 (JOB-06), WIN letters 16:00 (rwb-comms with rwb-integration, JOB-10). The ACE shared Quartz tables are no longer used. Full job map in the appendix.

## Slide 32

Where the bank's Airflow fits: at Recovery's edges, not inside it

For discussion: the bank is moving from Control-M to Airflow; this is the use we recommend

AIRFLOW DOES (BANK SCHEDULER)

RECOVERY ENTRY POINT

1

Overnight chain (main use)
ACE ingestion DAG ends with 'business date X ready'; a sensor waits for DailyCaseRun; SLA alerts 05:30 and 07:00

P1 rwb-source-data
publishes AceDataReady

2

Fixed-window file transfers
WIN letters 16:00 (INT-14), debt-buyer encrypted files (INT-25) over MFT; Recovery still builds the files

P2 rwb-integration
file + manifest ready

3

Report and regulatory extracts
JOB-15 at 01:30; rerun any business date; backfills on demand

P9 rwb-reporting
POST /reports/{id}/run

4

One-off bulk work
Cutover loads (tracker inventory), backfills, data-quality and GL reconciliation

P1 · P8 APIs
never their schemas

Interface contract: Airflow → Recovery
POST /v1/business-days/{date}/ready → 202, idempotent on the date  ·  GET /v1/business-days/{date}/status → RUNNING | DONE | LATE
Service APIs only, mTLS with client credentials; Airflow never reads or writes rwb_* schemas

Stays in Temporal and Kafka
Per-case workflows and approvals
Multi-day timers, sagas, deadlines
Reactions to business events
Anything a user waits for
Outbox every minute; timer and stuck checks every 5 min

To agree (for discussion)
Who owns the DAGs: bank platform team or Recovery
When Control-M moves to Airflow
Where Airflow runs: bank platform or ACE cluster
Fallback: poll ACE's batch record while ACE is on Control-M
New ADR replacing the BRD's ADF / Control-M

Airflow says when the bank's data and files are ready; Temporal decides what happens to each case.

32

Notes: Context: the bank's batch scheduling is moving from Control-M to Airflow. The BRD still names ADF and Control-M jobs, and the reference proposal (recovery-architecture.pptx) already puts Airflow on scheduled work and Temporal on multi-step work. This slide is a recommendation to discuss, not a decision.

1 Overnight chain (main use). Airflow runs the ACE ingestion DAG. Its last task calls rwb-source-data: POST /v1/business-days/{date}/ready, idempotent on the business date, answered 202. rwb-source-data checks freshness against the 30 views and publishes AceDataReady, which starts DailyCaseRun in rwb-case and the matching and reconciliation workflows. An Airflow sensor polls GET /v1/business-days/{date}/status until DONE, and Airflow raises SLA alerts at 05:30 and 07:00. This replaces rwb-source-data polling ACE's batch record; the poll stays as the fallback if ACE ingestion is still on Control-M at go-live.

2 Fixed-window file transfers: WIN letters at 16:00 (INT-14) and debt-buyer encrypted files (INT-25) over MFT or SFTP. rwb-integration still builds the files and manifests; Airflow owns the window, the transfer and the retry.

3 Report and regulatory extracts: JOB-15 at 01:30 through POST /v1/reports/{id}/run on rwb-reporting, with a rerun for any business date and backfills.

4 One-off bulk work: cutover loads such as the tracker inventory, backfills, data-quality and GL reconciliation runs, all through service APIs.

Not Airflow: per-case workflows, approvals, multi-day timers, sagas, reactions to business events, anything a user waits for, and high-frequency jobs (outbox every minute, timer and stuck-workflow checks every 5 minutes). These stay in Temporal and Kafka. Airflow never reads or writes rwb_* schemas.

To agree: who owns the DAGs (bank platform team or Recovery), when Control-M moves to Airflow, where Airflow runs, and a new ADR replacing the BRD's ADF/Control-M wording.

## Slide 33

Scale only what is busy: a steady front, an elastic back

All 19 services have the same shape; only the background workers grow

ONE SERVICE, FOR EXAMPLE rwb-document

screen requests

API

API

Front: 2 fixed copies

Its task queue

KEDA
watches the queue

Workers: 0 to many

add / remove

Back: grows with the queue

own schema (ACE DB)

Busy times and places

05:00-07:00 morning run
rwb-case, rwb-payment, rwb-deviation

Document intake and text reading
rwb-document, rwb-agent: bursts of uploads

16:00 letters and notices
rwb-comms, rwb-integration

AI agent runs
rwb-agent: 60 s, or the rule result is used

23.6k → 47k  open cases, today to 2031

~420  concurrent users

64-74k  documents a month

< 2 s  screen target (95%)

Volumes are modest: we split for reuse, ownership and isolation, and add capacity only where work piles up.

33

Notes: Each service is deployed as two parts: an API deployment (2 pods for availability, scaled on CPU or requests if ever needed) and a worker deployment scaled by KEDA on the Temporal task-queue backlog or Kafka consumer lag, down to zero for bursty work such as OCR or agent runs.

Volumes (recovery-architecture.pptx; Volume and Scale Forecast v3; NFR Spec v3): about 23,600 open cases today, 47,389 by 2031; about 420 concurrent users (about 21 requests a second at peak); 64-74k documents a month (2.8 TB by 2031); 283-318k rule evaluations a month.

Cost of 19 services: about 38 small deployments at rest (most workers idle at minimum), one Helm chart and one pipeline template. The ACE database sees capped pools per service.

## Slide 34

When one part fails, the rest keeps working

Example: the litigation service is down

Case

Decision

Access

Deviation

Valuation

Treatment

Guarantee

Litigation

Asset

Debt sale

Write-off

Document

Comms

Payment

Partner

Integration

Source data

Reporting

Agent

Litigation pauses. Its work waits on its queue and topic offset and resumes when it is back. The other 18 keep running.

Kafka down

Events wait in each service's outbox and are sent when it returns. Nothing is lost.

Temporal down

Running journeys pause and resume where they stopped. Screens keep working.

ACE database busy

Each service's pool is capped, so Recovery cannot starve ACE; reports use projections.

AI slow or down

After 60 seconds the rule-based answer is used; officers are never blocked.

Failures are contained by design (queues, outboxes, timeouts, circuit breakers, capped pools), not by luck.

34

Notes: Contained by design: each service has its own schema and login, task queue, consumer group and workers; REST calls have timeouts and circuit breakers; events wait in outboxes and topics; Temporal keeps every running journey.

Litigation down: litigation tabs show 'temporarily unavailable'; LitigationWorkflow tasks wait on queue rwb-litigation and resume when it is back; Kafka keeps its consumer offset; every other route, the case list and payments continue.

Other cases: Kafka down (outboxes hold events), Temporal down (journeys pause and resume; screens still work), ACE database busy (capped pools keep Recovery from starving ACE), AI slow (rule result after 60 s). Full table in the appendix.

## Slide 35

Security in layers: nobody is trusted by default

Six layers from the network edge to the audit trail

Edge

Shared App Gateway with WAF; partners only through the partner gateway (FAPI 2.0)

Sign-in

ACE Common sign-in (Entra ID, MFA) at the shared gateway-bff; 15-minute idle timeout

Service to service

Every call encrypted and identified both ways (mTLS); Kafka ACLs per service

Inside each service

Checks the user's role, scope and DoA on every action (rwb-access data)

Data

One login per schema; personal data masked and encrypted; never in events or workflow payloads

Audit & monitoring

Hash-chained decision log; ACE PII logging to SOC; one trace across services

AI under BOT AI risk rules
guidelines of 12 Sep 2025

Suggests, never decides: a person approves

Model and prompt versions recorded

Personal data masked before it leaves

60-second limit, then the rules decide

Runs only in rwb-agent, easy to switch off

Built on NIST SP 800-204 (zero trust for microservices), OWASP API Top 10 and FAPI 2.0 for partner access.

35

Notes: Zero trust per NIST SP 800-204 (security strategies for microservices) and 800-204A (service mesh): every service-to-service call is mutually authenticated with workload identity and authorised by policy, deny by default. 800-204B (attribute-based access control) informs data scope and DoA checks; 800-204C/204D inform the DevSecOps pipeline and supply-chain controls.

Baseline: Req 8 (shared BFF: opaque tokens to the browser, one login/logout/timeout), Req 9 (each service authorises its own resources - OWASP API1:2023 Broken Object Level Authorization), Req 10 (W3C trace context).

Partners: FAPI 2.0 Security Profile (final Feb 2025) for the partner API - sender-constrained tokens, PAR, strong client authentication; separate DMZ gateway; penetration test before launch.

PDPA: personal data stays in the owning service; events and workflow histories carry IDs; Temporal payload codec encrypts payloads (AES-GCM) with keys in Key Vault; masking rules (P4) enforced in each service.

AI: BOT AI Risk Management Guidelines (Sep 2025) - accountability, lifecycle risk management, explainability, telling customers and offering a human. NFR v3: 60 s then rule result.

v5 specifics: staff sign-in is ACE Common's (Entra ID, MFA) through the shared gateway-bff; each service has its own database login with grants on its own schema only; Kafka topics have per-service ACLs; Temporal namespaces have their own certificates and codec keys.

## Slide 36

Built for reuse: which services other workbenches can pick up

Why we cut by module: generic capabilities can be shared without taking the rest of Recovery

Ready to reuse as is (7)

Document hub
P5 · rwb-document

Communications
P6 · rwb-comms

Decision center & log
P7 · rwb-decision

Access & administration
P4 · rwb-access

Agent runtime
P10 · rwb-agent

Integration & files
P2 · rwb-integration

Reporting
P9 · rwb-reporting

Reusable with configuration (7)

Partner management
S9 · rwb-partner

Payments & posting
P8 · rwb-payment

Deviation handling
S8 · rwb-deviation

Valuation & route
S1 · rwb-valuation

Assets & auction
S5 · rwb-asset

Debt sale
S6 · rwb-debtsale

Source data
P1 · rwb-source-data

Recovery-specific (5)

Case & workflow
P3 · rwb-case

TDR, settlement, DIL
S2 · rwb-treatment

Guarantees
S3 · rwb-guarantee

Litigation & enforcement
S4 · rwb-litigation

Write-off & recovery
S7 · rwb-writeoff

What makes a service reusable
Contract first: OpenAPI, AsyncAPI, activity jar
Workbench ID on every call; no Recovery terms in generic APIs
Versioned: /v1, backward-compatible events, kit semver
Own schema, movable to its own server
Own task queue and Nexus endpoint
Configuration, not code: templates, DoA, rules as data

Example: ACE Collection could send notices through rwb-comms' Nexus endpoint without deploying anything new.

36

Notes: Assessment of reuse potential (for planning, not a commitment):

Ready to reuse as is: Document hub (P5), Communications (P6), Decision center and log with rule registry (P7), Access and administration (P4), Agent runtime (P10), Integration and files (P2), Reporting (P9). These have no Recovery-specific terms in their contracts.

Reusable with configuration: Partner management (S9), Payments and posting (P8), Deviation handling (S8), Valuation (S1), Assets and auction (S5), Debt sale (S6), Source data (P1, as a pattern for reading ACE).

Recovery-specific: Case and workflow (P3, the pattern is reusable), Treatment (S2), Guarantees (S3), Litigation (S4), Write-off (S7).

How another workbench reuses a service: call its REST API or activity contract, or its Nexus endpoint from another namespace; or deploy its own instance with its own schema and configuration.

## Slide 37

Where we change today's design, and why

Ten changes; each becomes a new ADR (ADR-013 onward)

Today

Proposed

recovery-core: one deployable (ADR-001)

19 services, one per BA module

One schema for everything (ADR-002)

ACE database, one schema and login per service

30 views read by any module (ADR-010)

Views read only by rwb-source-data

Outbox without a broker

Outbox + Kafka business-event topics

Central log inside every call (ADR-009)

Local record, then central ledger in rwb-decision

Rules in Excel tables (ADR-012)

DMN decision models, registry in rwb-decision

One endless case workflow (ADR-011)

Workflow kit + stage children + Continue-As-New

ACE's Quartz tables; ADF / Control-M (BRD)

Temporal Schedules in services; bank Airflow runs the chain

Data lake and Power BI feed (INT-19/20)

Removed: reports from rwb-reporting

No circuit breakers

Timeouts, circuit breakers, bulkheads

Kept: same AKS cluster and App Gateway, ACE Common services, gateway-bff, shared Temporal, Blob with WORM, payload codec.

37

Notes: ADR-001/002: one deployable and one schema become 19 services with a schema and login each in the same ACE database. ADR-010: the 30 views stay, but only rwb-source-data reads them. Event and Messaging Design v4: outbox without a broker becomes outbox plus Kafka topics. ADR-009: the central log written inside every call becomes a local record plus central ledger. ADR-012: XLS decision tables become DMN models (same Drools runtime, converted table by table). ADR-011: one long CaseWorkflow becomes workflow kit plus stage children plus Continue-As-New. Batch and Scheduling Design v4: ACE's shared Quartz tables become Temporal Schedules, and the BRD's ADF/Control-M jobs move to the bank's Airflow for the cross-system chain only (for discussion). Interface Specifications v3: INT-19/20 (data lake, Power BI) are removed. Resilience: timeouts, circuit breakers and bulkheads become a standard.

## Slide 38

Getting there: services arrive with the epics that need them

Wave 0 builds the template once; then each epic adds its services

Wave 0 · now
Platform once

Service template + Helm

Contract libraries

Workflow kit (L3)

19 schemas + logins

Kafka topics + ACLs

Temporal 1.30+

Wave 1 · Epic 1
9 services

P1 · Source data

P2 · Integration

P3 · Case

P4 · Access

P5 · Document

P6 · Comms

P7 · Decision

P9 · Reporting

P10 · Agent

Wave 2 · Epics 2-3
+4 services

P8 · Payment

S2 · Treatment

S5 · Asset

S8 · Deviation

Wave 3 · Epics 4-5
+4 services

S1 · Valuation

S3 · Guarantee

S4 · Litigation

S6 · Debt sale

Wave 4 · Epics 6-7
+2 services

S7 · Write-off

S9 · Partner

BOT approval before Wave 1 go-live, if required (FPG 19/2560 cl. 5.5; up to 30 business days)

Build the platform pieces once; then every epic adds only its own services, so nothing is built twice.

38

Notes: Wave 0 is the enabler: service template (Spring Boot, outbox, inbox, Temporal worker, codec, OpenTelemetry), one Helm chart, golden pipeline, contract libraries, the workflow kit, the 19 schemas and logins, Kafka topics and ACLs, Temporal 1.30+.

Waves follow the first epic of each module: Epic 1: P1, P2, P3, P4, P5, P6, P7, P9, P10 (9 services). Epics 2-3: P8, S2, S5, S8 (+4). Epics 4-5: S1, S3, S4, S6 (+4). Epics 6-7: S7, S9 (+2). A service is created when its epic starts, so nothing is built twice.

BOT: if the change is significant under FPG 19/2560 cl. 5.5, BOT approval is needed before Wave 1 go-live (up to 30 business days).

## Slide 39

Six decisions we need from the architecture team

Each has a clear owner; the first three are needed before Wave 0 starts

1

Kafka for business events

Host Recovery's business-event topics on the bank Kafka platform ACE already uses (separate topics and ACLs from PII logging); fallback: Azure Event Hubs Kafka endpoint

Owner: Enterprise Architecture, ACE platform team

2

A schema per service in the ACE database

19 schemas and 19 logins on the ACE PostgreSQL server; connection budget per service; no cross-schema access

Owner: ACE team, DBA

3

Shared Temporal layer

Platform team owns the cluster and the workflow kit; upgrade to 1.30+ for Nexus; namespaces per workbench

Owner: Platform team, ACE team

4

ACE Common contracts

Sign-in, notification path, shared case view adapter, restructure calculator (Nexus), audit and PII logging

Owner: ACE team

5

Decision ledger model

Local record + central ledger in rwb-decision; strict mode for irreversible steps; changes ADR-009

Owner: Risk, Internal Audit

6

BOT approval route

Is this a significant change under FPG 19/2560 cl. 5.5? Lead time up to 30 business days

Owner: Compliance, IT Risk

39

Notes: Decisions (owners in brackets):
1 Kafka for business events: Host Recovery's business-event topics on the bank Kafka platform ACE already uses (separate topics and ACLs from PII logging); fallback: Azure Event Hubs Kafka endpoint (Enterprise Architecture, ACE platform team)
2 A schema per service in the ACE database: 19 schemas and 19 logins on the ACE PostgreSQL server; connection budget per service; no cross-schema access (ACE team, DBA)
3 Shared Temporal layer: Platform team owns the cluster and the workflow kit; upgrade to 1.30+ for Nexus; namespaces per workbench (Platform team, ACE team)
4 ACE Common contracts: Sign-in, notification path, shared case view adapter, restructure calculator (Nexus), audit and PII logging (ACE team)
5 Decision ledger model: Local record + central ledger in rwb-decision; strict mode for irreversible steps; changes ADR-009 (Risk, Internal Audit)
6 BOT approval route: Is this a significant change under FPG 19/2560 cl. 5.5? Lead time up to 30 business days (Compliance, IT Risk)

## Slide 40

Appendix: reference detail

Service, event and job catalogues for the 19 services, architect questions, risks, volumes, standards, regulation and references

40

Notes: Reference material for architects who want the detail. The main storyline does not depend on these slides.

## Slide 41

A1 · Service catalogue: the 19 services

One row per service: module, what it owns, its schema, API, topic, task queue and wave

| Module | Service | Owns | Schema | First API path | Kafka topic | Task queue | Wave |
|---|---|---|---|---|---|---|---|
| P3 | rwb-case | case, CMMN state, queues, tasks, allocation, timers | rwb_case | /cases/{id} | rwb.case.events.v1 | rwb-case | 1 |
| P7 | rwb-decision | approvals, central decision ledger, DMN model registry | rwb_decision | /decisions | rwb.decision.events.v1 | rwb-decision | 1 |
| P4 | rwb-access | Recovery roles as data, scope, masking policy, DoA table, access log | rwb_access | /authorise | rwb.access.events.v1 | rwb-access | 1 |
| S8 | rwb-deviation | X1-X7 screening, pause, handling, return | rwb_deviation | /deviations | rwb.deviation.events.v1 | rwb-deviation | 2 |
| P1 | rwb-source-data | ACE view contract, extension tables, freshness, reconciliation | rwb_source_data | /customers/{id} | rwb.source-data.events.v1 | rwb-source-data | 1 |
| P9 | rwb-reporting | measures, snapshots, steering dashboard, regulatory reports | rwb_reporting | /dashboards/{id} | rwb.reporting.events.v1 | rwb-reporting | 1 |
| P10 | rwb-agent | agent policies, prompts, runs, guardrails, evaluations | rwb_agent | /agent-runs/{id} | rwb.agent.events.v1 | rwb-agent | 1 |
| P2 | rwb-integration | interface config, file runs, outbound items, ACE integration paths | rwb_integration | /interface-runs | rwb.integration.events.v1 | rwb-integration | 1 |
| P5 | rwb-document | metadata, custody, OCR text and fields, signatures, retention | rwb_document | /documents | rwb.document.events.v1 | rwb-document | 1 |
| P6 | rwb-comms | notices, templates, merge fields, proof of delivery | rwb_comms | /notices | rwb.comms.events.v1 | rwb-comms | 1 |
| P8 | rwb-payment | payment and proceeds matching, fees, bookings, posting files | rwb_payment | /cases/{id}/payments | rwb.payment.events.v1 | rwb-payment | 2 |
| S9 | rwb-partner | panel, partner users, instructions, results, fees, scorecards | rwb_partner | /partners | rwb.partner.events.v1 | rwb-partner | 4 |
| S1 | rwb-valuation | valuations, D6 route decision, route agent output | rwb_valuation | /cases/{id}/valuation | rwb.valuation.events.v1 | rwb-valuation | 3 |
| S2 | rwb-treatment | treatments, contracts, settlement and deed-in-lieu agreements, plan timers | rwb_treatment | /treatments | rwb.treatment.events.v1 | rwb-treatment | 2 |
| S3 | rwb-guarantee | TCG and insurance claims, guarantor notices and pursuit | rwb_guarantee | /guarantee-claims | rwb.guarantee.events.v1 | rwb-guarantee | 3 |
| S4 | rwb-litigation | legal actions, hearings, judgments, enforcement, LED auction ladder | rwb_litigation | /legal-actions | rwb.litigation.events.v1 | rwb-litigation | 3 |
| S5 | rwb-asset | assets taken on, holding, floor price, listings, auction rounds | rwb_asset | /assets | rwb.asset.events.v1 | rwb-asset | 2 |
| S6 | rwb-debtsale | lots, data room, buyer terms, bids, award, transfer | rwb_debtsale | /lots | rwb.debtsale.events.v1 | rwb-debtsale | 3 |
| S7 | rwb-writeoff | eligibility, committee, posting, recovery after charge-off | rwb_writeoff | /write-offs | rwb.writeoff.events.v1 | rwb-writeoff | 4 |


41

Notes: Every service follows the same naming: schema rwb_<name> in the ACE database with its own login; REST under /api/recovery/<name>/v1 behind gateway-bff; Kafka topic rwb.<name>.events.v1; Temporal task queue rwb-<name> in namespace rwb-recovery. Wave = the delivery wave in which the service is created (Wave 1 = Epic 1).

## Slide 42

A2 · Event catalogue 1/2

Every business event: producer topic and consuming services (CloudEvents on Kafka, key caseId)

| # | Event | Producer | Topic | Consumers |
|---|---|---|---|---|
| 01 | CaseCreated | rwb-case | rwb.case.events.v1 | rwb-agent, rwb-deviation, rwb-reporting |
| 02 | CaseAllocated | rwb-case | rwb.case.events.v1 | rwb-reporting |
| 03 | CaseAllocationFailed | rwb-case | rwb.case.events.v1 | rwb-case |
| 04 | CaseTransferred | rwb-case | rwb.case.events.v1 | rwb-reporting |
| 05 | CaseStateChanged | rwb-case | rwb.case.events.v1 | rwb-comms, rwb-reporting |
| 06 | DeviationRaised | rwb-deviation | rwb.deviation.events.v1 | rwb-case, rwb-comms, rwb-treatment |
| 07 | DeviationCleared | rwb-deviation | rwb.deviation.events.v1 | rwb-case, rwb-comms |
| 08 | DecisionRecorded | all 19 | rwb.decision-record.v1 | rwb-decision, rwb-reporting |
| 09 | ApprovalRequested | rwb-decision | rwb.decision.events.v1 | gateway-bff (inbox) |
| 10 | TreatmentApproved | rwb-treatment | rwb.treatment.events.v1 | rwb-comms, rwb-payment |
| 11 | TreatmentBooked | rwb-payment | rwb.payment.events.v1 | rwb-case, rwb-treatment |
| 12 | PaymentMissed | rwb-payment | rwb.payment.events.v1 | rwb-case, rwb-treatment, rwb-comms |
| 13 | NoticeGenerated | rwb-comms | rwb.comms.events.v1 | rwb-decision |
| 14 | NoticeDispatched | rwb-comms | rwb.comms.events.v1 | rwb-reporting |
| 15 | NoticeDelivered | rwb-comms | rwb.comms.events.v1 | rwb-litigation, rwb-guarantee, rwb-case |
| 16 | DocumentStored | rwb-document | rwb.document.events.v1 | rwb-agent, rwb-case |
| 17 | DocumentFieldsExtracted | rwb-document | rwb.document.events.v1 | rwb-case |
| 18 | TimerDue | durable timer | — | (retired: timer inside the workflow) |
| 19 | TimerBreached | rwb-case | rwb.case.events.v1 | gateway-bff (inbox) |


42

Notes: Events carry IDs and facts, never personal data. Each producer writes to its outbox in the same transaction as its state change; a relay publishes to its topic. Consumers dedupe through their inbox table. Schemas are versioned in the registry with BACKWARD compatibility; the AsyncAPI document per service is the contract.

## Slide 43

A3 · Event catalogue 2/2

Every business event: producer topic and consuming services (CloudEvents on Kafka, key caseId)

| # | Event | Producer | Topic | Consumers |
|---|---|---|---|---|
| 20 | InstructionIssued | rwb-partner | rwb.partner.events.v1 | partner portal |
| 21 | PartnerResultSubmitted | rwb-partner | rwb.partner.events.v1 | rwb-litigation, rwb-asset, rwb-case |
| 22 | AssetTakenOn | rwb-asset | rwb.asset.events.v1 | rwb-case, rwb-payment |
| 23 | LotAwarded | rwb-debtsale | rwb.debtsale.events.v1 | rwb-case, rwb-payment |
| 24 | WriteOffApproved | rwb-writeoff | rwb.writeoff.events.v1 | rwb-case, rwb-payment, rwb-reporting |
| 25 | ProceedsMatched | rwb-payment | rwb.payment.events.v1 | rwb-case, rwb-asset, rwb-debtsale, rwb-writeoff, rwb-guarantee |
| 26 | AceDataReady | rwb-source-data | rwb.source-data.events.v1 | rwb-case, rwb-payment, rwb-deviation, rwb-writeoff |
| 27 | AceDataLate | rwb-source-data | rwb.source-data.events.v1 | alerts, gateway-bff banner |
| 28 | AgentRunCompleted | rwb-agent | rwb.agent.events.v1 | rwb-decision, rwb-document, rwb-deviation |
| 29 | CaseEvent (signal) | case router | — | CaseWorkflow (Temporal signal) |
| 30 | RulePackageInForce | rwb-decision | rwb.decision.events.v1 | rwb-case, rwb-valuation, rwb-treatment, rwb-payment |
| + | RouteDecided | rwb-valuation | rwb.valuation.events.v1 | rwb-case |
| + | AssetSold | rwb-asset | rwb.asset.events.v1 | rwb-payment, rwb-case |
| + | JudgmentRecorded, AuctionResult | rwb-litigation | rwb.litigation.events.v1 | rwb-asset, rwb-case |
| + | TreatmentClosed, GuaranteeClaim* | rwb-treatment / guarantee | — | rwb-case, rwb-reporting |
| + | AccountsTransferred | rwb-debtsale | rwb.debtsale.events.v1 | rwb-case, rwb-reporting |
| + | AccessPolicyChanged, DoaLimitChanged | rwb-access | rwb.access.events.v1 | all (cache refresh) |
| + | FileDelivered, FileFailed | rwb-integration | rwb.integration.events.v1 | requesting service |


43

Notes: Events carry IDs and facts, never personal data. Each producer writes to its outbox in the same transaction as its state change; a relay publishes to its topic. Consumers dedupe through their inbox table. Schemas are versioned in the registry with BACKWARD compatibility; the AsyncAPI document per service is the contract.

## Slide 44

A4 · Job map: every scheduled or triggered job and its owner

No shared Quartz tables: a Temporal Schedule or event-started workflow in the owning service; bank Airflow triggers the edges

| Job | Name | When | Owner | Mechanism |
|---|---|---|---|---|
| JOB-02 | Case creation | Airflow: ACE data ready | rwb-case | AceDataReady → DailyCaseRun |
| JOB-03 | Morning allocation | after 02, by 07:00 | rwb-case | DailyCaseRun step |
| JOB-04 | Reconciliation | Airflow: ACE data ready | rwb-source-data | event-triggered workflow |
| JOB-05 | Timer check | every 5 min | all | durable timers (retired) |
| JOB-06 | Rebalancing | 06:30 | rwb-case | Schedule |
| JOB-07 | Payment matching | Airflow: ACE data ready | rwb-payment | event-triggered workflow |
| JOB-08 | Booking confirmation | Airflow: ACE data ready | rwb-payment | event-triggered workflow |
| JOB-10 | WIN notices | 16:00 | rwb-comms + integration | Airflow file window + workers |
| JOB-11 | Outbox sender | every minute | every service | outbox relay to Kafka |
| JOB-12 | Document intake | every 15 min | rwb-document | event + KEDA workers |
| JOB-13 | Decision log copy | 01:00 | rwb-decision | ingest is continuous (Kafka) |
| JOB-14 | Hash-chain check | 02:00 | rwb-decision | Schedule |
| JOB-15 | Reporting extract | 01:30 | rwb-reporting | Airflow trigger (no data lake) |
| JOB-16 | Write-off scan | monthly, 3rd working day | rwb-writeoff | Schedule |
| JOB-17 | Retention | monthly, 1st Sunday | rwb-document | Schedule |
| JOB-18 | Access review list | six-monthly | rwb-access | Schedule |
| JOB-19 | Re-appraisal | monthly | rwb-asset | Schedule |
| JOB-20 | Rule promote | 00:01 | rwb-decision | Schedule → RulePackageInForce |
| JOB-21 | Stuck workflow scan | every 5 min | platform | visibility query + alert |
| JOB-22 | Smoke workflow | 06:00 | platform | Schedule |


44

Notes: The ACE shared Quartz and batch tables are no longer used by Recovery. Each job runs in its owning service: a Temporal Schedule (cron, with overlap policy SKIP and catch-up window) or a workflow started by an event such as AceDataReady. The bank's Airflow (replacing Control-M; for discussion) owns only the cross-system edges: it runs the ACE ingestion DAG and signals 'business date ready', so JOB-02, 04, 07 and 08 start from AceDataReady; it opens the WIN and debt-buyer file windows (JOB-10); and it triggers the regulatory extract (JOB-15) with reruns by business date.

## Slide 45

A5 · Questions architects ask 1/2

Short answers; the detail is in the main slides

| Question | Answer |
|---|---|
| Why 19 services and not fewer? | One service per BA module gives each capability its own release, owner and contract, so it can be reused or replaced later (for example Document hub or Communications by ACE Collection) without untangling a shared core. |
| Isn't 19 too many for a team of nine? | They arrive in waves with the epics (9 at Epic 1, 19 by Epic 7). One service template, one Helm chart, one pipeline and shared libraries keep the cost per service low. |
| Why share the ACE database? | It is already run, backed up and approved; ACE data is there. A schema and login per service keeps ownership clear, and any schema can move to its own server later by changing a connection string. |
| Doesn't a shared database couple the services? | Only if they share tables. Rules: write only your own schema, no cross-schema joins or foreign keys, IDs across services, contracts for everything else. A boundary test fails the build on any violation. |
| Who reads ACE's data? | Only rwb-source-data reads the 30 recovery.v_ace_* views (ADR-010). Everyone else asks it through REST or a Temporal activity, so a change in ACE is absorbed in one place. |
| Why Kafka rather than Azure Service Bus? | ACE already runs Kafka, so no new platform or outsourcing review; replay lets a new or repurposed service rebuild its view from history; per-case ordering by key; many independent listeners. |
| What if the Kafka platform cannot host us in time? | Azure Event Hubs Premium speaks the Kafka protocol, so the same client code works. Until then the outbox keeps events safe in each service. |
| Why one Temporal cluster for ACE and Recovery? | Temporal isolates tenants with namespaces and task queues. One cluster per service would be 19 x 4 environments. Workers stay inside each service. |
| The bank is moving to Airflow: why not run everything there? | Airflow suits timed, cross-system batches. It is not built for millions of long-lived case workflows, approvals and timers. So Airflow says the data is ready, opens file windows and runs extracts; Temporal runs each case. For discussion. |


45

Notes: Q: Why 19 services and not fewer?
A: One service per BA module gives each capability its own release, owner and contract, so it can be reused or replaced later (for example Document hub or Communications by ACE Collection) without untangling a shared core.

Q: Isn't 19 too many for a team of nine?
A: They arrive in waves with the epics (9 at Epic 1, 19 by Epic 7). One service template, one Helm chart, one pipeline and shared libraries keep the cost per service low.

Q: Why share the ACE database?
A: It is already run, backed up and approved; ACE data is there. A schema and login per service keeps ownership clear, and any schema can move to its own server later by changing a connection string.

Q: Doesn't a shared database couple the services?
A: Only if they share tables. Rules: write only your own schema, no cross-schema joins or foreign keys, IDs across services, contracts for everything else. A boundary test fails the build on any violation.

Q: Who reads ACE's data?
A: Only rwb-source-data reads the 30 recovery.v_ace_* views (ADR-010). Everyone else asks it through REST or a Temporal activity, so a change in ACE is absorbed in one place.

Q: Why Kafka rather than Azure Service Bus?
A: ACE already runs Kafka, so no new platform or outsourcing review; replay lets a new or repurposed service rebuild its view from history; per-case ordering by key; many independent listeners.

Q: What if the Kafka platform cannot host us in time?
A: Azure Event Hubs Premium speaks the Kafka protocol, so the same client code works. Until then the outbox keeps events safe in each service.

Q: Why one Temporal cluster for ACE and Recovery?
A: Temporal isolates tenants with namespaces and task queues. One cluster per service would be 19 x 4 environments. Workers stay inside each service.

Q: The bank is moving to Airflow: why not run everything there?
A: Airflow suits timed, cross-system batches. It is not built for millions of long-lived case workflows, approvals and timers. So Airflow says the data is ready, opens file windows and runs extracts; Temporal runs each case. For discussion.

## Slide 46

A6 · Questions architects ask 2/2

Short answers; the detail is in the main slides

| Question | Answer |
|---|---|
| How is Temporal reusable by others? | Three reusable layers: the shared cluster, a versioned workflow kit (approval, notice, document intake, agent run, saga, schedule) and service activity contracts. A new workbench gets a namespace and composes them. |
| How do services call each other through Temporal? | A workflow calls a typed activity interface on the owner's task queue, or starts a child workflow there. Across workbenches it uses a Nexus operation. No service imports another's code, only its contract jar. |
| How is data kept consistent without one transaction? | Each step is a local transaction plus an outbox event. Multi-step deals are sagas in Temporal with compensation before the point of no return. |
| How does the case screen stay under 2 s? | The gateway calls rwb-case and rwb-source-data in parallel (one hop each); other tabs load on click from their own services. Budget about 1.2 s. |
| How is personal data kept out of events and workflows? | Events and workflow inputs carry IDs and business facts only; Temporal payloads are encrypted by the codec (AES-GCM, Key Vault keys); masking is applied by rwb-source-data. |
| What stops call chains from growing? | REST is one hop: gateway to service, or a cached reference read (rwb-access, rwb-source-data). Anything longer is a workflow. Trace analysis flags call depth above one. |
| How do you test 19 services? | Contract tests per API, event and activity (OpenAPI, AsyncAPI, contract jars); Temporal replay tests; Testcontainers for Kafka and PostgreSQL; a daily journey smoke workflow (JOB-22). |
| Does this need BOT approval? | Possibly: FPG 19/2560 cl. 5.5 requires prior approval for significant technology change. Compliance to confirm. |


46

Notes: Q: How is Temporal reusable by others?
A: Three reusable layers: the shared cluster, a versioned workflow kit (approval, notice, document intake, agent run, saga, schedule) and service activity contracts. A new workbench gets a namespace and composes them.

Q: How do services call each other through Temporal?
A: A workflow calls a typed activity interface on the owner's task queue, or starts a child workflow there. Across workbenches it uses a Nexus operation. No service imports another's code, only its contract jar.

Q: How is data kept consistent without one transaction?
A: Each step is a local transaction plus an outbox event. Multi-step deals are sagas in Temporal with compensation before the point of no return.

Q: How does the case screen stay under 2 s?
A: The gateway calls rwb-case and rwb-source-data in parallel (one hop each); other tabs load on click from their own services. Budget about 1.2 s.

Q: How is personal data kept out of events and workflows?
A: Events and workflow inputs carry IDs and business facts only; Temporal payloads are encrypted by the codec (AES-GCM, Key Vault keys); masking is applied by rwb-source-data.

Q: What stops call chains from growing?
A: REST is one hop: gateway to service, or a cached reference read (rwb-access, rwb-source-data). Anything longer is a workflow. Trace analysis flags call depth above one.

Q: How do you test 19 services?
A: Contract tests per API, event and activity (OpenAPI, AsyncAPI, contract jars); Temporal replay tests; Testcontainers for Kafka and PostgreSQL; a daily journey smoke workflow (JOB-22).

Q: Does this need BOT approval?
A: Possibly: FPG 19/2560 cl. 5.5 requires prior approval for significant technology change. Compliance to confirm.

## Slide 47

A7 · Risks and how we handle them

Each risk has a mitigation and an owner

| Risk | Impact | Mitigation | Owner |
|---|---|---|---|
| Too many deployables for the team | Slow delivery, on-call load | Waves by epic; service template, one Helm chart, golden pipeline; platform team runs Kafka and Temporal | Delivery lead |
| ACE database capacity | Slow ACE screens or jobs | Connection pools and caps per login; heavy reports from projections; monitor per schema; move a schema out if needed | ACE DBA |
| Schema rules broken over time | Hidden coupling between services | Database grants per schema; boundary test in every build; review of every new grant | Architecture |
| Kafka platform not ready | Events stay in outboxes | Outbox port; Event Hubs Kafka endpoint as fallback | Enterprise Architecture |
| Temporal upgrade from 1.28.1 | No Nexus, no Worker Versioning | Upgrade to 1.30+ in Wave 0 | Platform team |
| Ledger model not accepted by Audit | Back to synchronous central log | Strict mode for irreversible steps; early walkthrough with Audit | Architecture, Audit |
| BOT approval lead time | Wave 1 date slips | Confirm route early; plan up to 30 business days | Compliance |
| ACE Common contracts change | Recovery features break | Versioned contracts and contract tests with the ACE team | ACE team |


47

Notes: Too many deployables for the team: Slow delivery, on-call load. Mitigation: Waves by epic; service template, one Helm chart, golden pipeline; platform team runs Kafka and Temporal (Delivery lead)
ACE database capacity: Slow ACE screens or jobs. Mitigation: Connection pools and caps per login; heavy reports from projections; monitor per schema; move a schema out if needed (ACE DBA)
Schema rules broken over time: Hidden coupling between services. Mitigation: Database grants per schema; boundary test in every build; review of every new grant (Architecture)
Kafka platform not ready: Events stay in outboxes. Mitigation: Outbox port; Event Hubs Kafka endpoint as fallback (Enterprise Architecture)
Temporal upgrade from 1.28.1: No Nexus, no Worker Versioning. Mitigation: Upgrade to 1.30+ in Wave 0 (Platform team)
Ledger model not accepted by Audit: Back to synchronous central log. Mitigation: Strict mode for irreversible steps; early walkthrough with Audit (Architecture, Audit)
BOT approval lead time: Wave 1 date slips. Mitigation: Confirm route early; plan up to 30 business days (Compliance)
ACE Common contracts change: Recovery features break. Mitigation: Versioned contracts and contract tests with the ACE team (ACE team)

## Slide 48

A8 · Volumes are modest; peaks come from the daily batch and document intake

We do not split for throughput; we split so each capability can change, fail and scale on its own

3,110
new cases a month

~21 req/s
414 concurrent staff at peak

48
concurrent partner users (320 total)

64-74k
documents a month; 2.8 TB by 2031

283-318k
rule evaluations a month

55-62k
decision-log entries a month

| Route work a month | Volume |
|---|---|
| Registered letters | 1,909 |
| Lawsuits filed | 667 |
| Repossessions | 720 |
| Debt-sale accounts | ~315 |
| Property sales | 29 |


Service targets (NFR v3)
Screen response < 2 s (p95)
Rule evaluation < 300 ms
AI agent: 60 s, then rule result
99.9% in business hours
RPO/RTO: not yet set

What actually needs to scale
The 05:00-07:00 chain: case creation, payment matching, allocation, rebalance
OCR and document intake: bursts of uploads; 500 pages an hour
Notice generation at 16:00 and court-date timers; AI agent runs
The screens (API tier) are light: 2 small pods per service are enough

Split for ownership and isolation, scale only the hot paths

48

Notes: All figures from Volume and Scale Forecast v3 and NFR Spec v3. Open cases: 23,570 today, 26,479 by end 2027, 47,389 by 2031. New cases ~3,110 a month. 414 concurrent internal users is ~21 requests a second at peak; 320 partner users with 48 concurrent.

Where load concentrates: the overnight/morning chain (case creation and allocation by 07:00), OCR (500 pages an hour target), notice generation (WIN batch 16:00), rule evaluation (283-318k a month).

Implication: a single well-built service could carry this load. The case for splitting is ownership, release independence, failure isolation and regulatory isolation (AI, partner DMZ, audit), not raw throughput. Scaling is by worker pools (KEDA) on the few hot paths.

NFR gap: RPO/RTO are not set in NFR Spec v3; proposed tiers.

## Slide 49

A9 · Standards we apply: recognised by the bank's architects and auditors

Every design choice in this deck points back to one of these

| Standard | What it gives us |
|---|---|
| BIAN Service Landscape v14 | Bank-standard names and boundaries for business capabilities (service domains) |
| Domain-Driven Design: bounded contexts | One model, one owner, one data store per context |
| microservices.io patterns | Decompose by capability; schema per service (a database-per-service variant); saga; transactional outbox; API composition; CQRS; anti-corruption layer |
| NIST SP 800-204, 204A, 204B, 204C | Security for microservices; service mesh; attribute-based access; DevSecOps |
| OWASP API Security Top 10 (2023) | API threat checklist, especially object-level authorisation |
| FAPI 2.0 Security Profile (final Feb 2025) | Partner API security with sender-constrained tokens |
| OpenAPI 3.1 · AsyncAPI 3.x · CloudEvents 1.0 | Machine-readable contracts for REST and events; CNCF event envelope |
| OpenTelemetry · W3C Trace Context | One trace across services, events and workflows (baseline Req 10) |
| OMG DMN 1.6 | Business-readable, executable decision models; Drools conformance level 3 |
| Azure Well-Architected · AKS microservices reference | Platform, scaling, resilience patterns (circuit breaker, bulkhead, claim-check) |
| Temporal durable execution | Long-running business processes as code; used in banking (ANZ home loans, JPMorgan Chase payments) |


49

Notes: Verified 19 Nov 2026 against primary sources (URLs in the references slide).

BIAN: release 14.0 (Feb 2026); service domains are elemental, mutually exclusive and collectively exhaustive business capabilities - a direct basis for service boundaries.
microservices.io (Chris Richardson): decomposition by business capability and subdomain; data patterns.
NIST SP 800-204 (Aug 2019), 204A service mesh (May 2020), 204B ABAC (Aug 2021), 204C DevSecOps (Mar 2022); 204D software supply chain (Feb 2024) also relevant to pipelines.
FAPI 2.0 Security Profile approved Final 19 Feb 2025. OAuth 2.1 is still an IETF draft, so we cite FAPI 2.0 as the binding profile.
CloudEvents graduated in CNCF Jan 2024. AsyncAPI 3.1 is current. W3C Trace Context Level 1 is a Recommendation (Nov 2021).
DMN 1.6 formal Sep 2026; Apache KIE Drools supports DMN at conformance level 3 and DMN 1.6 since 10.2.0. Note XLS decision tables are a Drools-native format, separate from DMN.
Temporal: ANZ case study (home-loan origination); JPMorgan Chase talk at Replay 2024 (payments modernisation).

## Slide 50

A10 · Regulatory constraints shape the design, not just the controls

Bank of Thailand rules and Thai law that this architecture must satisfy

| Regulation | What it asks | How the design responds |
|---|---|---|
| BOT FPG 19/2560 · IT risk management | Board-approved plan and prior BOT approval before first use of a technology or a change that may pose significant risk (cl. 5.5); report significant IT and cyber incidents immediately | Treat the move to microservices as a significant change: submit the plan before Wave 1; incident reporting through SIEM and runbooks |
| BOT FPG 19/2559 · IT outsourcing | Board-approved outsourcing policy; notify BOT for private cloud outside the group, seek approval for public cloud used for critical IT, 30 days before use | All services stay on the bank's Azure tenant and AKS; any new managed service (for example Event Hubs as Kafka fallback) is checked against the outsourcing register |
| BOT Cyber Resilience Assessment Framework | Governance, identify, protect, detect, respond and recover, third-party risk | Zero trust between services, mesh mTLS, WAF, SIEM, tested recovery tiers |
| BOT AI Risk Management Guidelines (12 Sep 2025) | Board accountability, lifecycle risk management, accuracy and explainability, data and cyber controls, telling customers and offering a human | AI isolated in rwb-agent; autonomy levels; human decision on material actions; prompts, outputs and model versions logged |
| Thailand PDPA | Lawful purpose, minimisation, security, retention and data-subject rights | Personal data only in owning services; IDs in events and workflows; Temporal payload encryption; retention jobs |


Programme dependency: under FPG 19/2560 cl. 5.5 the change may need a board-approved plan and BOT approval before Wave 1 (up to 30 business days). Compliance to confirm (decision 6).

50

Notes: FPG 19/2560 (Regulations on IT Risk Management of Financial Institutions), announced 20 Dec 2017, effective 1 Apr 2018. Clause 5.5: first-time use of a technology, or a change that may pose significant risk, needs a board-approved plan submitted to BOT for approval before proceeding; BOT decides within 30 business days. This is a programme dependency: the date for submission belongs in the plan.

FPG 19/2559 (Regulations on IT Outsourcing for Business Operations of Financial Institutions): board-approved outsourcing policy and risk framework; notify BOT for private cloud from providers outside the group, seek approval for public cloud used for critical IT, both 30 days before use. Not checked whether later rules supersede it; Compliance to confirm.

Cyber Resilience Assessment Framework (CRAF), issued around 2018: six areas listed. No standalone CRAF document found on bot.or.th; source is a BOT payment systems report.

BOT AI Risk Management Guidelines issued 12 Sep 2025 after public hearing 12-30 Jun 2025 (date from a secondary source; Compliance to confirm).

These are summaries for architecture purposes, not legal advice; Compliance owns the interpretation.

## Slide 51

A11 · References

Standards and regulation checked against primary sources on 19 November 2026

| Source | Where |
|---|---|
| BIAN v14 service landscape | github.com/bian-official/public · bian.org (v14 release notes, Feb 2026) |
| microservices.io patterns | microservices.io/patterns (database-per-service, saga, transactional-outbox, cqrs, api-composition, anti-corruption-layer, strangler-application, decompose-by-business-capability) |
| NIST SP 800-204 / 204A / 204B / 204C / 204D | csrc.nist.gov/pubs/sp/800/204/final (and /a/, /b/, /c/, /d/) |
| BOT FPG 19/2560 IT risk | bot.or.th/content/dam/bot/fipcs/documents/FPG/2561/EngPDF/25610021.pdf |
| BOT FPG 19/2559 IT outsourcing | bot.or.th/content/dam/bot/fipcs/documents/FPG/2560/EngPDF/25600035.pdf |
| BOT AI Risk Management Guidelines | bot.or.th/th/laws-and-rules/public-hearing/public-hearing-20250612.html |
| Temporal: namespaces, Nexus, limits, schedules | docs.temporal.io/best-practices/managing-namespace · /evaluate/nexus · /workflow-execution/limits · /schedule · /parent-close-policy |
| Temporal Worker Versioning; banking users | temporal.io/changelog · temporal.io/resources/case-studies/anz-story · temporal.io/in-use/payments-modernization-jpmc |
| KEDA Temporal scaler (2.17+) | keda.sh/docs/latest/scalers/temporal/ |
| OMG DMN 1.6; Drools DMN | omg.org/spec/DMN · kie.apache.org/drools/dmn |
| FAPI 2.0 Security Profile | openid.net/specs/fapi-security-profile-2_0-final.html |
| OWASP API Security Top 10 2023 | owasp.org/API-Security/editions/2023/en/0x11-t10/ |
| CloudEvents · AsyncAPI · W3C Trace Context | cncf.io/projects/cloudevents · asyncapi.com/docs/reference · w3.org/TR/trace-context |
| Internal documents | microservice-baseline.pdf; workflow-minimum-requirements.pdf; ADR v3; Event and Messaging Design v4; Batch and Scheduling Design v4; Physical Schema v6; FSDs v3/v4; Volume and Scale Forecast v3; NFR Spec v3; Interface Specifications v3 (INT-14, INT-19/20 removed, INT-23, INT-25, INT-34); Target Architecture v6 |
| Apache Kafka; CloudEvents Kafka binding | kafka.apache.org/documentation · github.com/cloudevents/spec (kafka-protocol-binding.md) |
| Azure Event Hubs for Apache Kafka (fallback) | learn.microsoft.com/azure/event-hubs/azure-event-hubs-apache-kafka-overview |
| Azure: AKS microservices, immutable Blob | learn.microsoft.com/azure/architecture/reference-architectures/containers/aks-microservices · /storage/blobs/immutable-storage-overview |
| Reference proposal | Proposed Arch/recovery-architecture.pptx (six services inside ACE, shared Temporal, recovery-core) |


51

Notes: Verification notes: BIAN names from the v14 semantic API repository; Payment Execution is obsolete in v14 and replaced by Payment Settlement. 'Channel Partner Management' does not exist; v14 has Partner Management, Partner Administration and Partner Agreement. BOT outsourcing regulation is FPG 19/2559. Temporal history limit is 51,200 events or 50 MB. DMN current formal version is 1.6. OAuth 2.1 is still an IETF draft. AsyncAPI current is 3.1. Fiserv is not used as a Temporal reference (no public case study found).
