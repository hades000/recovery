## Read me, version 7 and the change log

SCB Collections and Recovery. Henka Group, 22 November 2026.

(C) Siam Commercial Bank and Henka Pte Ltd

Change log: 7, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash

Version 6, 16 November 2026, D-RCV-36 (Temporal from Epic 3, Quartz and Spring Batch for Epic 1 and Epic 2, embedded Drools) is kept

The eighteen slides of version 6 are kept unchanged, so every section, ID, number and date they carry stays as written (ASM-B-TECH-02-9)

This version adds slides 20 to 29: the 19 services, Kafka, the Temporal layer, the edge, no data lake, the waves and what is still open

Release dates are unchanged and marked tentative (DL48, ASM-B-TECH-02-10); no date is changed and none is raised as a gap

Status: Draft. No approval is recorded for this run (ASM-B-TECH-02-8)

Owners: every service, table, endpoint, event, workflow and job owner in this deck is the code taken from the Microservice Ownership Map v1 (ASM-B-TECH-02-11)

## What the realignment changes, and the ADRs that carry it

One service, one repository, one front end become 19 services inside ACE, one per business module: ADR-013

One schema for everything becomes one schema and one login per service in the ACE PostgreSQL server: ADR-014

Outbox without a broker becomes Kafka business-event topics with outbox, inbox and CloudEvents: ADR-015

One workflow per case becomes a reusable Temporal layer, and Schedules replace Quartz: ADR-016

Rule packages run on embedded Drools in the owning service, with the registry in rwb-decision: ADR-017

The data lake and the Power BI feed (INT-19, INT-20) are removed; rwb-reporting builds from events: ADR-018

The edge is gateway-bff with a Redis session and the partner gateway in the DMZ: ADR-019

Contract first with one hop and a 2 s timeout (ADR-020); Flyway per service (ADR-021); local decision record plus central ledger (ADR-022); observability per service (ADR-023)

## The platform services P1 to P5, and what each owns

P1 rwb-source-data · Source data · wave 1 · owns 18 tables, 18 REST operations, 2 events and 3 jobs; the only reader of the 30 v_ace_* views

P2 rwb-integration · Integration and files · wave 1 · owns 3 tables and 11 REST operations; WIN letters (INT-14) and buyer files (INT-25) leave here

P3 rwb-case · Case and workflow · wave 1 · owns 15 tables, 22 REST operations, 7 events, CaseWorkflow and 3 jobs; it hosts the case router

P4 rwb-access · Access and administration · wave 1 · owns 5 tables, 4 REST operations and 1 job; roles, scope, masking and the DoA table as data

P5 rwb-document · Document hub · wave 1 · owns 12 tables, 17 REST operations, 2 events, DocumentIntakeWorkflow and 2 jobs

Every service has an api and a worker deployment, a schema rwb_<name> with its own login, a topic rwb.<name>.events.v1 and a task queue rwb-<name>

The owner code is the first column of each line, taken from the Ownership Map v1 sheets Services, Tables, Endpoints, Events, Workflows and activities and Jobs

## The platform services P6 to P10, and what each owns

P6 rwb-comms · Communications · wave 1 · owns 3 tables, 11 REST operations, 3 events, NoticeDispatchWorkflow and 1 job

P7 rwb-decision · Decision center and log · wave 1 · owns 6 tables, 19 REST operations, 3 events, ApprovalWorkflow and 3 jobs

P8 rwb-payment · Payments and posting · wave 2 · owns 1 table, 2 REST operations, 3 events and 2 jobs

P9 rwb-reporting · Reporting · wave 1 · owns 3 tables, 1 REST operation and 1 job; its measures come from events, not from a data lake

P10 rwb-agent · Agent runtime · wave 1 · owns 8 tables, 11 REST operations, 1 event and AgentRunWorkflow

Six platform library tables (feature_flag, feature_flag_change, idempotency_key, outbox_event, outbox_delivery, processed_event) are created in every schema and owned by PLT

Four platform jobs are owned by PLT: JOB-05 timer check, JOB-11 outbox sender, JOB-21 stuck workflow scan and JOB-22 smoke workflow

## The stage services S1 to S9, and what each owns

S1 rwb-valuation · Valuation and route · wave 3 · 3 REST operations and RouteDecisionWorkflow (child of the case)

S2 rwb-treatment · TDR, settlement and deed in lieu · wave 2 · 1 table, 4 REST operations, 1 event and TreatmentWorkflow

S3 rwb-guarantee · Guarantees · wave 3 · 1 table, 2 REST operations and GuaranteeClaimWorkflow

S4 rwb-litigation · Litigation and enforcement · wave 3 · 2 tables, 5 REST operations and LitigationWorkflow (years; continues-as-new)

S5 rwb-asset · Assets and auction · wave 2 · 2 tables, 6 REST operations, 1 event, AssetDisposalWorkflow and 1 job

S6 rwb-debtsale · Debt sale · wave 3 · 2 tables, 5 REST operations, 1 event and DebtSaleWorkflow (saga, pivot at transfer)

S7 rwb-writeoff · Write-off and recovery · wave 4 · 1 table, 2 REST operations, 1 event, WriteOffWorkflow and 1 job

S8 rwb-deviation · Deviation handling · wave 2 · 1 table, 2 REST operations, 2 events and DeviationWorkflow (any time)

S9 rwb-partner · Partner management · wave 4 · 3 tables, 6 REST operations, 2 events and InstructionWorkflow

Route services reach the shared capabilities through Temporal, never REST; only rwb-source-data reads the ACE views

## Runtime: one case workflow, with a child for each stage

CaseWorkflow on rwb-case: one per case, entry to closure, workflow ID case-{caseId}, signals from the case router

Each stage is a child workflow on the owner's queue: RouteDecision, Treatment, GuaranteeClaim, Litigation, AssetDisposal, DebtSale, WriteOff, Deviation

Four steps in every stage: receive the event, EvaluateRules in Drools, RecordAndApply in one transaction, wait on a durable timer

Events reach the case through the case router in rwb-case: Kafka consumer group rwb-case, signalWithStart, never a direct call

Approvals come from the kit: ApprovalWorkflow on rwb-decision, routed by the DoA table that rwb-access owns

Continue-As-New at each stage end and at least every 28 days; children use parent close policy ABANDON

Rules run inside an activity, never in workflow code; the answer, the rule ID and the model version go into the decision record

Case, stage and task state stay in rwb_case; Temporal holds no case of record (T1)

## The Temporal layer: five levels, the bottom four reusable

L1 cluster: one per environment on ACE AKS, its own persistence database, UI, metrics and codec server; 1.30 or later for Nexus and Worker Versioning

L2 namespaces: ace-collection and rwb-recovery; a new workbench gets a namespace with its own retention, quotas, certificates and keys

L3 workflow kit: versioned library of Approval, Notify, Document intake, Agent run with rule fallback, Human task with SLA, Saga runner, Scheduled job, Partner instruction

L4 activity contracts: typed interfaces per service on queue rwb-<service>, plus Nexus endpoints; EvaluateRules and RecordAndApply live here, in the owner

L5 domain workflows: CaseWorkflow and the stage workflows, written by each service team

Schedules replace Quartz: rule promote 00:01, measures 01:30, hash-chain check 02:00, smoke 06:00, rebalance 06:30, WIN letters 16:00

Another workbench reuses L1 to L4 and writes only its own L5; no business terms in the L1 to L3 interfaces

Owner: Platform team for L1 to L3 (RWB-PLT-WF and RWB-PLT-LIB); each service team for L4 and L5 (ASM-B-TECH-02-7)

## Kafka: one topic per service, outbox and inbox

One topic per service: rwb.<short>.events.v1, 19 topics, plus the shared rwb.decision-record.v1 that every service publishes DecisionRecorded to

12 partitions, replication factor 3, 7-day retention, key caseId, so one case's events stay in order

CloudEvents 1.0 in binary mode, JSON Schema registry with BACKWARD compatibility, AsyncAPI per topic

Producer: outbox in the service's own schema, idempotent producer, acks=all; consumer: inbox processed_event in the same transaction

Retry 1 minute, 10 minutes, 1 hour, then the dead-letter topic with an alert and a replay tool

The bank Kafka platform ACE already runs for PII logging, with Recovery's own topics and ACLs; Azure Event Hubs Premium is the fallback

Shared topic settings: Not specified in the source documents (CG-B-TECH-02-2; ASM-B-TECH-02-2)

## The edge: gateway-bff and the partner gateway

gateway-bff: the only entry for staff screens, Spring Cloud Gateway, session in Redis, 15-minute idle timeout

The shared App Gateway and WAF route /recovery/* and /api/recovery/* to gateway-bff; / and /api/* stay with ACE

Composite screens: the gateway calls at most a few owners in parallel, one hop each, 2 s timeout and a breaker per service

Partner gateway in the DMZ: FAPI 2.0 in front of rwb-partner; partners never reach gateway-bff

Every service authorises its own object; permission data is cached from rwb-access and checked on every action

Owner: Not specified in the source documents (CG-B-TECH-02-3; ASM-B-TECH-02-3); the edge is epic RWB-PLT-EDGE and sits outside the 19

## Data: one ACE database, 19 schemas, no data lake

One ACE PostgreSQL server: the ACE schemas, schema recovery with the 30 v_ace_* views, and the 19 Recovery schemas

One login per service with grants on its own schema only; no cross-schema joins, views or foreign keys; the boundary test fails the build on any violation

Only rwb-source-data reads the 30 views, through the read-only login rwb_source_data, with a 5 s statement timeout

Flyway per service in its own pipeline; a schema can later move to its own server by changing a connection string

No data lake: INT-19 and INT-20 are removed and rwb-reporting builds measures, snapshots and regulatory extracts from events in rwb_reporting

Workbench tables: 92 on slide 11 of version 6 against 93 rows in the Ownership Map (87 business tables and 6 platform library tables): Not specified in the source documents (CG-B-TECH-02-1; ASM-B-TECH-02-1)

Temporal keeps its persistence in its own database; documents stay in Blob with the write-once container, through rwb-document only

## Delivery: waves 0 to 4, and what is still open

Wave 0 builds the platform once: service template and Helm chart, contract libraries, workflow kit, 19 schemas and logins, topics and ACLs, Temporal 1.30 or later

Wave 1, Epic 1 (30 Nov 2026, tentative): nine services, P1 to P7, P9 and P10

Wave 2, Epics 2 and 3 (31 Dec 2026 and 31 Jan 2027, tentative): P8, S2, S5 and S8

Wave 3, Epics 4 and 5 (28 Feb 2027 and 31 Mar 2027, tentative): S1, S3, S4 and S6

Wave 4, Epics 6 and 7 (30 Apr 2027 and 31 May 2027, tentative): S7 and S9; Epic 8 on 30 Jun 2027, tentative

The wave of each service is the one in the Ownership Map Services sheet; where slide 15 of version 6 puts a service in another epic, the Map governs (CG-B-TECH-02-4; ASM-B-TECH-02-4)

Still open for this version: deployment slots for 38 deployments (CG-B-TECH-02-5; ASM-B-TECH-02-5), repository per service (CG-B-TECH-02-6; ASM-B-TECH-02-6), owner of the cluster and kit (CG-B-TECH-02-7; ASM-B-TECH-02-7)

New decisions of this version: DL44 adopt Arch v5, DL45 service epics plus business-epic tags, DL46 soft ownership by team type, DL47 Epic 1 preservation, DL48 dates unchanged and tentative, DL49 gap and assumption registers (ASM-B-TECH-02-12)
