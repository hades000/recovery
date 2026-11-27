SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

# Recovery Workbench P6 Communications

Technical specification. SCB Collections and Recovery. Henka Group, 22 November 2026.

(C) Siam Commercial Bank and Henka Pte Ltd

## Document control

| Attribute | Value |
|---|---|
| Document title | TSD P6 Communications |
| Document ID | P6-RWB-TSD-v3 |
| Version | 3 |
| Status | Draft |
| Date | 22 November 2026 |
| Supersedes | Version 2, 28 October 2026 |
| TSD owner | Solution architect |
| Build squad | TechX recovery squads (GAP-1999; ASM-3225: no squad is named per service) |
| Decision | D-RCV-60 microservice realignment |
| Status note | Draft: no approval of version 3 is recorded (GAP-1998; ASM-3217) |
| Change | 3, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash |

| Document | Type | Relationship |
|---|---|---|
| Recovery Workbench FSD P6 Communications | FSD | Pair |
| Recovery Workbench Target Architecture | Architecture | Parent |
| Recovery Workbench Logical Data Model and Data Dictionary | Data | Source of T3 |
| Recovery Workbench API Specification | API | Source of appendix T-A |
| Recovery Workbench Microservice Ownership Map v1 | Ownership | Owner of every table, endpoint, event, workflow and job in T0 and T5.2 |

## Existing capability check

| Capability | Verdict | Owning document | Note |
|---|---|---|---|
| Sign-in, access check, audit, PII and SOC logging | REUSE | ACE common module | Called through the published interface |
| Scheduler and batch | REUSE | ACE pattern: Quartz and Spring Batch | Jobs in the Batch and Scheduling Design |
| Outbox and retry | REUSE | Error Handling and Resilience Standard | Through P2 |
| Rules evaluation | REUSE | Rules Engine Design | Through the rules component |

Under D-RCV-60 the scheduler and batch row is delivered by the Temporal layer (ADR-016): Temporal Schedules and event-started workflows in the owning service replace the Quartz and Spring Batch jobs (DP-10). The outbox and retry row is delivered by the Kafka outbox, inbox and retry topics (ADR-015; DP-09).

## T0. Service

P6 Communications is one of the 19 services of Architecture v5: `rwb-comms` (service name Communications, module P6, wave 1, service epic `RWB-SVC-P6`). Version 3 adds this section so that the specification is read as the specification of one service: its identity, what it owns, and the decoupling patterns that replace the monolith's in-process calls. Every owner is taken from Microservice Ownership Map v1 and every identifier from Template and Rules R4 (ADR-013, ADR-014).

P6 owns the notice and template estate; the letter content is a P5 document and the delivery file is a P2 file (DP-11, DP-16).

### T0.1 Service identity

| Item | Value |
|---|---|
| Module | P6 Communications |
| Service | `rwb-comms` (Communications) |
| Service epic | `RWB-SVC-P6` |
| Wave | 1 |
| Schema | `rwb_comms` |
| Database login | `rwb_comms`: one login per service, with its own connection pool cap |
| REST base | `/api/recovery/comms/v1` |
| Kafka topic | `rwb.comms.events.v1`, with `.retry` and `.dlt` topics |
| Event names | `rwb.comms.<Event>.v1`, CloudEvents 1.0 in binary mode, key `caseId` |
| Temporal | namespace `rwb-recovery`; task queue `rwb-comms` |
| Java package | `th.co.scb.ace.workbench.recovery.comms` |
| Edge | gateway-bff for the staff screens of this service |
| Contract artefacts | `05 Technical architecture/Recovery Workbench API Specification v5/rwb-comms.yaml`; `05 Technical architecture/Recovery Workbench API Specification v5/asyncapi/rwb-comms.asyncapi.yaml` |
| Suggested owner, app development | TechX (suggested; any team may pick up this story) |
| Suggested owner, ACE DB | ACE team (suggested; any team may pick up this story) |

### T0.2 What this service owns

Architecture v5 slide 41 gives this service: notices, templates, merge fields, proof of delivery. Table T0.2 states the same ownership in the form the Ownership Map uses, with the counts this specification carries. A table that the map assigns to another service is not built here, whatever T3 says (see the note under T3).

| Area | Owner and artefact | Count |
|---|---|---|
| Business tables in `rwb_comms` | `merge_field`, `notice`, `template` | 3 |
| REST operations | appendix T-A and `rwb-comms.yaml` | 11 |
| Events published | EV-13 NoticeGenerated, EV-14 NoticeDispatched, EV-15 NoticeDelivered | 3 |
| Workflows and schedules | NoticeDispatchWorkflow | 1 |
| Jobs | JOB-10 | 1 |

### T0.3 Decoupling patterns applied

The left column is the pattern of Template and Rules R5.5; the middle column quotes the line of this specification that carries the legacy marker, where one is present; the right column is what replaces it in this service.

| DP | Legacy marker in this specification | How the service lands it |
|---|---|---|
| DP-01 | — | Owns its tables in `rwb_comms`; no other service reads them (ADR-014). |
| DP-02 | — | One login, `rwb_comms`, with its own connection pool cap. |
| DP-03 | `…on events from P3 and writes through the decision log.` | Local decision record plus DecisionRecorded (EV-08) on `rwb.decision-record.v1`. |
| DP-07 | `DF-LEG-018 / notice_type / LOV / varchar(25) / Yes / LOV-NOTICE / Workbench` | Reference data and lists of values from the `rwb-case` contract (H RWB-PLT-E1043-CON). |
| DP-08 | `RW-CASEOWN Case owner / CRU / R` | Authorisation through the `rwb-access` authorise contract and the guard library (H RWB-PLT-E1037-CON). |
| DP-09 | `…state machine of its own; the module acts on events from P3 and writes through the decision…` | Outbox and inbox library; CloudEvents on `rwb.comms.events.v1` with retry topics and `.dlt`. |
| DP-10 | `Scheduler and batch / REUSE / ACE pattern: Quartz and Spring Batch / Jobs in the Batch and…` | Temporal Schedules and event-started workflows through the workflow kit (ADR-016). |
| DP-11 | `…reaches other modules only through their published interfaces and other systems only through COLLINS,…` | One REST hop, 2 s timeout, breaker; the consumer builds against the provider's fake (ADR-020). |
| DP-13 | `API-P6-001 / POST / /api/recovery/v1/cases/{caseId}/notices / Litigation C…` | REST base `/api/recovery/comms/v1`. |
| DP-14 | — | Topic `rwb.comms.events.v1`, retry topics and `.dlt`; naming library (H RWB-PLT-E1047-CON). |
| DP-15 | — | Per-service Flyway sequence in `rwb_comms`. |

### T0.4 What this service is not

- It holds no other service's table and no ACE table beyond the read-only `recovery.v_ace_*` views (DP-01, DP-05).
- It runs no shared Quartz job and touches no ACE batch table (DP-10; ADR-016).
- It holds no signature row and no letter content: both are P5's (DP-01; ASM-0077).
- It is not a monolith module: the published Java interface of T2 is replaced by the contract set of T5.2 (DP-11; ADR-020).

## T1. Architecture overview

P6 Communications is delivered as the service `rwb-comms` (module P6, wave 1, service epic `RWB-SVC-P6`): one repository, one pipeline, one schema `rwb_comms` with one login, behind gateway-bff (ADR-013, ADR-014). It covers: letters, notices, SMS, LINE, proof of delivery. It reaches other modules only through the contracts of T5.2 and other systems only through COLLINS, file loads and the ACE paths.

## T2. Component design

| Component | Responsibility |
|---|---|
| CommunicationsController | REST endpoints in appendix T-A; validation; maps errors to problem responses |
| CommunicationsService | Business logic; calls the rules component; writes the decision log entry before any change |
| CommunicationsRepository | Reads and writes the module's tables only |
| Jobs | Temporal Schedules and event-started workflows this service owns (T0.2, T5.2.1; DP-10) |
| Published interface | The contracts of T5.2: REST operations, events and workflows other services call; no table is read across modules (DP-11) |

The published interface of this table is the contract set of T5.2: the REST operations, the events and the workflows, not a Java interface in a shared classpath (DP-11; ADR-020). Components that the Ownership Map places in another service are stated in T0.2 and T5.2 and are built by that service.

## T3. Data model

Every object of T3 that Microservice Ownership Map v1 assigns to `rwb-comms` lives in schema `rwb_comms` with the standard columns of T3.0 (DP-01, DP-15; ADR-014). `notice`, `template` and `merge_field` stay here. `signature_request`, which T3.1 lists, is P5's (Ownership Map ruling `signature_request`, ASM-0077); P6 orchestrates the request through P5's contract and holds no signature row.

### T3.0 Standard record columns

| Column | Type | Meaning |
|---|---|---|
| is_active | boolean | The active or inactive status of the record |
| state | varchar(40) | Record lifecycle state |
| version | integer | Optimistic lock version |
| created_at | timestamptz | When the record was created |
| created_by | uuid | Who or which service identity created it |
| updated_at | timestamptz | When the record last changed |
| updated_by | uuid | Who or which service identity last changed it |

### T3.1 Object and field definitions

**notice** (NEW). A demand, recall or statutory notice and its proof of delivery.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-LEG-015 | id | TEXT | uuid | Yes | None | Workbench |
| DF-LEG-016 | case_id | CROSS_REF | uuid | Yes | None | Workbench |
| DF-LEG-017 | document_id | CROSS_REF | uuid | No | None | Workbench |
| DF-LEG-018 | notice_type | LOV | varchar(25) | Yes | LOV-NOTICE | Workbench |
| DF-LEG-019 | sent_date | DATE | date | No | None | WIN |
| DF-LEG-020 | barcode | TEXT | varchar(40) | No | None | WIN |
| DF-LEG-021 | callback_date | DATE | date | No | None | WIN |
| DF-LEG-022 | delivery_status | LOV | varchar(15) | No | LOV-DELIVERY | WIN |
| DF-LEG-023 | sent_type | LOV | varchar(10) | No | LOV-SENT-TYPE | WIN |
| DF-LEG-030 | party_id | CROSS_REF | uuid | No | None | Workbench |
| DF-LEG-031 | template_id | CROSS_REF | uuid | No | None | Workbench |
| DF-LEG-032 | hold_reason | TEXT | varchar(30) | No | None | Workbench |
| DF-LEG-033 | dispatch_file_id | CROSS_REF | uuid | No | None | Workbench |
| DF-LEG-034 | dispatch_attempts | NUMBER | integer | Yes | None | Workbench |

**template** (NEW). A letter or notice template.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-REF-045 | id | TEXT | uuid | Yes | None | Workbench |
| DF-REF-046 | template_code | TEXT | varchar(30) | Yes | None | Workbench |
| DF-REF-047 | template_version | NUMBER | integer | Yes | None | Workbench |
| DF-REF-048 | language | LOV | varchar(2) | Yes | LOV-LANG | Workbench |
| DF-REF-049 | product_group | LOV | varchar(15) | No | LOV-PRODUCT | Workbench |
| DF-REF-050 | body_ref | ATTACHMENT | varchar(400) | Yes | None | Workbench |
| DF-REF-051 | approved_by_legal | BOOLEAN | boolean | Yes | None | Workbench |
| DF-REF-063 | approved_by | USER_REF | uuid | No | None | Workbench |
| DF-REF-064 | approved_at | DATE | timestamptz | No | None | Workbench |
| DF-REF-065 | valid_from | DATE | date | No | None | Workbench |
| DF-REF-066 | channel | LOV | varchar(15) | No | LOV-CHANNEL | Workbench |
| DF-REF-067 | notice_type | LOV | varchar(25) | No | LOV-NOTICE | Workbench |
| DF-REF-068 | signature_basis | LOV | varchar(20) | No | LOV-SIGNATURE-BASIS | Workbench |
| DF-REF-069 | merge_codes | TEXT | jsonb | No | None | Workbench |

**merge_field** (NEW). A merge code a template may use and the field that supplies its value, by catalog version.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-REF-252 | id | TEXT | uuid | Yes | None | Workbench |
| DF-REF-253 | merge_code | TEXT | varchar(40) | Yes | None | Workbench |
| DF-REF-254 | source_entity | TEXT | varchar(60) | Yes | None | Workbench |
| DF-REF-255 | source_field | TEXT | varchar(60) | Yes | None | Workbench |
| DF-REF-256 | field_id | TEXT | varchar(16) | Yes | None | Workbench |
| DF-REF-257 | is_required | BOOLEAN | boolean | Yes | None | Workbench |
| DF-REF-258 | personal_data | BOOLEAN | boolean | Yes | None | Workbench |
| DF-REF-259 | catalog_version | TEXT | varchar(20) | Yes | None | Workbench |
| DF-REF-260 | valid_from | DATE | date | Yes | None | Workbench |

**signature_request** (NEW). A request for a party to sign a generated document, and its result.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-DOC-096 | id | TEXT | uuid | Yes | None | Workbench |
| DF-DOC-097 | case_id | CROSS_REF | uuid | Yes | None | Workbench |
| DF-DOC-098 | treatment_id | CROSS_REF | uuid | No | None | Workbench |
| DF-DOC-099 | document_id | CROSS_REF | uuid | Yes | None | Workbench |
| DF-DOC-100 | party_id | CROSS_REF | uuid | Yes | None | Workbench |
| DF-DOC-101 | method | LOV | varchar(15) | Yes | LOV-SIGN-METHOD | Workbench |
| DF-DOC-102 | status | LOV | varchar(15) | Yes | LOV-SIGN-STATUS | Workbench |
| DF-DOC-103 | external_ref | TEXT | varchar(60) | No | None | EasyApp |
| DF-DOC-104 | sent_at | DATE | timestamptz | No | None | Workbench |
| DF-DOC-105 | signed_at | DATE | timestamptz | No | None | Workbench |
| DF-DOC-106 | signed_document_id | CROSS_REF | uuid | No | None | Workbench |
| DF-DOC-107 | expires_at | DATE | timestamptz | No | None | Workbench |

### T3.2 Lists of values

| List | Values |
|---|---|
| LOV-CHANNEL | MOBILE, HOME_PHONE, WORK_PHONE, LINE, EMAIL, POSTAL_ADDRESS, CALL, VISIT, SMS, LETTER, PORTAL, BRANCH |
| LOV-DELIVERY | DELIVERED, REFUSED, UNDELIVERABLE, PENDING |
| LOV-LANG | TH, EN |
| LOV-NOTICE | DEMAND, RECALL, STATUTORY_SALE_NOTICE, GUARANTOR_NOTICE |
| LOV-PRODUCT | MORTGAGE, HIRE_PURCHASE, SSME, UNSECURED |
| LOV-SENT-TYPE | BEFORE_NPL, NPL |
| LOV-SIGN-METHOD | E_SIGNATURE, BRANCH, PAPER |
| LOV-SIGN-STATUS | QUEUED, SENT, SIGNED, DECLINED, EXPIRED |
| LOV-SIGNATURE-BASIS | E_SIGNATURE_ALLOWED, WET_INK_REQUIRED |

### T3.3 Relationships

| From | To | Field | Cardinality |
|---|---|---|---|
| notice | case_id | recovery_case | Many to 1 |
| notice | document_id | document | Many to 0 or 1 |
| notice | party_id | party | Many to 0 or 1 |
| notice | template_id | template | Many to 0 or 1 |
| notice | dispatch_file_id | outbound_item | Many to 0 or 1 |
| signature_request | case_id | recovery_case | Many to 1 |
| signature_request | treatment_id | treatment | Many to 0 or 1 |
| signature_request | document_id | document | Many to 1 |
| signature_request | party_id | party | Many to 1 |
| signature_request | signed_document_id | document | Many to 0 or 1 |

## T4. State machines and workflow

No case state machine of its own; the module acts on events from P3 and writes through the decision log.

## T5. Integration and interfaces

### T5.1 External system interfaces

| ID | System | Direction | Approach | Frequency |
|---|---|---|---|---|
| INT-14 | WIN | Out | File | Daily |
| INT-17 | NSS | Out | ACE notification path | As sent |
| INT-18 | LINE OA | Out | ACE notification path | As sent |

### T5.2 Contracts

Version 3 states every cross-module dependency of this module as a contract, so that the service is built against a published artefact and its fake (ADR-020; DP-11). The artefact per call type is: OpenAPI 3.1 for REST, AsyncAPI 3.0 for Kafka, the Temporal interface named here for a workflow or activity, the Interface Specifications manifest for a file, the Nexus operation for the ACE restructure calculator, and a grant on the view for SQL. No row of this section reads another service's table (DP-01). Every consumed contract is class C (Template and Rules R5.4): it never blocks the build, because the consumer builds against the fake, and the real cross-service behaviour is class I work on an integration story. Architecture v5 slides 13 to 20 name a few operations differently from the published files of 22 November 2026; the published file is the artefact the fake is generated from and is the one cited here (GAP-1997; ASM-3224).

#### T5.2.1 Contracts provided

The REST operations of this service are published in `05 Technical architecture/Recovery Workbench API Specification v5/rwb-comms.yaml` (5.0.0, 22 November 2026) under the base `/api/recovery/comms/v1`. Appendix T-A holds the endpoint IDs, the access right and the first release of each one.

| # | Method | Path | operationId |
|---|---|---|---|
| 1 | POST | `/cases/{caseId}/notices` | `postCasesCaseidNotices` |
| 2 | GET | `/notices/{noticeId}` | `getNoticesNoticeid` |
| 3 | GET | `/admin/templates` | `getAdminTemplates` |
| 4 | POST | `/admin/templates` | `postAdminTemplates` |
| 5 | GET | `/admin/templates/{templateId}/content` | `getAdminTemplatesTemplateidContent` |
| 6 | POST | `/admin/templates/{templateId}/approve` | `postAdminTemplatesTemplateidApprove` |
| 7 | POST | `/admin/templates/{templateId}/withdraw` | `postAdminTemplatesTemplateidWithdraw` |
| 8 | POST | `/cases/{caseId}/messages` | `postCasesCaseidMessages` |
| 9 | GET | `/treatments/{treatmentId}/signature-requests` | `getTreatmentsTreatmentidSignatureRequests` |
| 10 | POST | `/treatments/{treatmentId}/signature-requests` | `postTreatmentsTreatmentidSignatureRequests` |
| 11 | POST | `/signature-requests/{requestId}/result` | `postSignatureRequestsRequestidResult` |

Workflows, schedules, files and views this service provides:

| Contract | Type | Called by or target | Note |
|---|---|---|---|
| NoticeDispatchWorkflow | Temporal workflow | P3 rwb-case and the stage services | Kit template; runs on rwb-comms |

Events this service publishes (AsyncAPI 3.0, CloudEvents 1.0):

| Event | EV | Topic | Consumers |
|---|---|---|---|
| NoticeGenerated | EV-13 | `rwb.comms.events.v1` | rwb-decision |
| NoticeDispatched | EV-14 | `rwb.comms.events.v1` | rwb-reporting |
| NoticeDelivered | EV-15 | `rwb.comms.events.v1` | rwb-litigation, rwb-guarantee, rwb-case |

#### T5.2.2 Contracts consumed

| Contract | Type | Provider | Class | Failure path |
|---|---|---|---|---|
| Notification path for SMS and LINE (INT-17, INT-18) | REST | ACE Common | X | Tracked only; outside the Workbench; class X |
| generate letter | Temporal activity | P5 rwb-document | C | Workflow retry policy; the caller keeps its state (DP-12) |
| Approval | Temporal child workflow | P7 rwb-decision | C | Workflow retry policy; the caller keeps its state (DP-12) |
| deliverFile(manifest) for WIN letters | Temporal activity | P2 rwb-integration | C | Workflow retry policy; the caller keeps its state (DP-12) |

Events this service consumes:

| Event | EV | Provider topic | Provider | Class | Failure path |
|---|---|---|---|---|---|
| DeviationRaised | EV-06 | `rwb.deviation.events.v1` | S8 rwb-deviation | C | Retry 1 min, 10 min, 1 h, then `.dlt`; inbox dedupe |
| DeviationCleared | EV-07 | `rwb.deviation.events.v1` | S8 rwb-deviation | C | Retry 1 min, 10 min, 1 h, then `.dlt`; inbox dedupe |
| TreatmentApproved | EV-10 | `rwb.treatment.events.v1` | S2 rwb-treatment | C | Retry 1 min, 10 min, 1 h, then `.dlt`; inbox dedupe |
| PaymentMissed | EV-12 | `rwb.payment.events.v1` | P8 rwb-payment | C | Retry 1 min, 10 min, 1 h, then `.dlt`; inbox dedupe |
| CaseStateChanged | EV-05 | `rwb.case.events.v1` | P3 rwb-case | C | Retry 1 min, 10 min, 1 h, then `.dlt`; inbox dedupe |

#### T5.2.3 Call-type summary

| Call type | Provided | Consumed | Artefact |
|---|---|---|---|
| REST | 11 | 1 | OpenAPI 3.1, one file per service |
| Kafka (events) | 3 | 5 | AsyncAPI 3.0, one file per service |
| Temporal | 1 | 3 | Workflow and activity interfaces, queue `rwb-comms` |
| File | 0 | 0 | Interface Specifications manifest and the SAS link |
| Nexus | 0 | 0 | Nexus operation into ACE |
| SQL | 0 | 0 | Read-only grant on the view |

A contract change is a new version of the artefact, never a code change in the consumer (ADR-020). The provider named in T5.2.2 is the owner in Microservice Ownership Map v1, and the consumer list of each event is the Arch v5 event catalogue on slides 42 and 43.

### T5.3 Events

The event contract of this service is `05 Technical architecture/Recovery Workbench API Specification v5/asyncapi/rwb-comms.asyncapi.yaml`; the shared decision-record contract is `asyncapi/rwb.decision-record.v1.asyncapi.yaml`. Every service publishes DecisionRecorded (EV-08) to `rwb.decision-record.v1` from its outbox in the same transaction as its state change (DP-03, DP-09; ADR-015, ADR-022); consuming services dedupe through their inbox table. Events carry identifiers and facts, never personal data (Event and Messaging Design v4, sheet Rules).

| Event | EV | Direction | Topic |
|---|---|---|---|
| NoticeGenerated | EV-13 | Published | `rwb.comms.events.v1` |
| NoticeDispatched | EV-14 | Published | `rwb.comms.events.v1` |
| NoticeDelivered | EV-15 | Published | `rwb.comms.events.v1` |
| DeviationRaised | EV-06 | Consumed | `rwb.deviation.events.v1` |
| DeviationCleared | EV-07 | Consumed | `rwb.deviation.events.v1` |
| TreatmentApproved | EV-10 | Consumed | `rwb.treatment.events.v1` |
| PaymentMissed | EV-12 | Consumed | `rwb.payment.events.v1` |
| CaseStateChanged | EV-05 | Consumed | `rwb.case.events.v1` |

An event shown with `—` has no number in the numbered catalogue: the Arch v5 catalogue calls these rows `+`, so the number is not specified in the source documents (GAP-1996; ASM-3223).

## T6. Security and access control

### T6.1 RBAC matrix

| Role | Documents | Litigation |
|---|---|---|
| RW-CASEOWN Case owner | CRU | R |
| RW-TEAMMGR Team manager | R | R |
| RW-PHONECOL Phone collector | R | - |
| RW-FIELDCOL Field collector | CR | - |
| RW-RESTRUCT Restructuring officer (FCR) | CRU | - |
| RW-SPECIAL Hardship and vulnerability specialist | CRU | - |
| RW-COMPLAIN Complaint officer | CRU | R |
| RW-FRAUD Fraud investigator | CRU | R |
| RW-LITOFF Litigation officer | CRU | CRUA |
| RW-ENFORCE Enforcement owner | CRU | CRU |
| RW-LEGAL Legal counsel | CRUA | RA |
| RW-SALEOFF Sale officer | CRU | R |
| RW-NPAMGR NPA and asset manager | CRU | R |
| RW-DEBTSALE Debt sale officer | CRU | R |
| RW-WRITEOFF Write-off team member | CRU | R |
| RW-CREDITAD Credit Administration officer | CRU | R |
| RW-GUARANT Guarantee officer | CRU | R |
| RW-AGENCYMG Partner and agency manager | R | R |
| RW-CONDUCT Conduct and QA officer | R | R |
| RW-PRODHEAD Product head (Mortgage, HP, SSME) | R | RA |
| RW-HEADLIT Head of Litigation | R | RA |
| RW-HEADNPA Head of NPA | R | R |
| RW-HEADASL Head of Asset Liquidity | R | R |
| RW-CREDCOMM Credit approval committee member | R | - |
| RW-WOCOMM Write-off committee member | R | - |
| RW-RISK Risk and model risk officer | R | R |
| RW-COE Center of excellence analyst | R | R |
| RW-DATASTEW Data steward and data product owner | R | - |
| RW-AUDIT Internal audit | R | R |
| RW-COMPLY Compliance and PDPA officer | RU | R |
| RW-PLATADM Platform administrator | R | - |
| RW-BIANAL Reporting and BI analyst | - | R |
| RW-TRIBE Tribe lead and squad members | R | R |
| PT-AGENCY Collection agency (OA) user | CR | - |
| PT-LAWFIRM Law firm user | CRU | RU |
| PT-VALUER Valuer | CR | - |
| PT-AUCTION Auction vendor | CR | - |
| PT-BUYER Debt buyer and AMC | R | - |
| PT-RAMC RAMC user | R | - |
| SY-CASEWF Case workflow module | R | R |
| SY-RULES Rules component | R | R |
| SY-DATALOAD Data load from COLLINS | - | U |
| SY-OCR OCR and extraction pipeline | CRU | - |
| SY-AGENT Agent platform | R | R |

### T6.2 Authentication and authorization

Entra ID single sign-on through the ACE front end; each endpoint declares its capability area and right; scope filters every query; masking applies to personal fields; service identities for jobs and agents.

Every operation of T5.2.1 is authorised through the `rwb-access` authorise contract with the role, the scope and the delegation limit of T6.1 (DP-08; C RWB-P4-E1037-CON); the caller caches the answer and refreshes it on AccessPolicyChanged and DoaLimitChanged.

## T7. Non-functional requirements

| ID | Requirement | Target | Status |
|---|---|---|---|
| NFR-049 | Staff authenticate with single sign-on and multi-factor authentication. | Entra ID single sign-on with multi-factor | Proposed |
| NFR-050 | Partner accounts authenticate with multi-factor and are scoped to their own cases. | Multi-factor, scoped | Proposed |
| NFR-051 | Agents run under service identities and are subject to the same role checks as people. | Service identities | Proposed |
| NFR-052 | Secrets are held in the key store and never in code, configuration files or prompts. | No secrets in code or prompts | Proposed |
| NFR-053 | Data is encrypted at rest and in transit. | Encrypted | Proposed |
| NFR-054 | The build pipeline blocks a change that carries a secret, personal data in code, tests or logs, or an unapproved dependency. | Pipeline checks pass | Proposed |
| NFR-055 | Agent outputs are schema checked against an allowed-action list with a confidence threshold, and fall back to rules when the check fails. | Schema check on every output | Proposed |
| NFR-056 | Penetration testing and a security review are completed before the first production release. | Before the first production release and before the partner portal opens to users outside the bank | Proposed, DL11 |

## T8. Requirement traceability

| Requirement | Feature | Story | Test |
|---|---|---|---|
| REQ-OCC-001 | None | Written one epic ahead | With the story |
| REQ-OCC-002 | None | Written one epic ahead | With the story |
| REQ-OCC-003 | FEAT-OCC-01 | RWB-E2-021 | TC-E2-021-01 |
| REQ-OCC-004 | FEAT-OCC-01 | RWB-E2-021 | TC-E2-021-01 |
| REQ-OCC-005 | FEAT-OCC-01 | RWB-E2-021 | TC-E2-021-01 |
| REQ-OCC-006 | FEAT-OCC-01 | RWB-E2-021 | TC-E2-021-01 |
| REQ-OCC-007 | None | Written one epic ahead | With the story |
| REQ-OCC-008 | FEAT-OCC-01 | RWB-E2-021 | TC-E2-021-01 |
| REQ-OCC-009 | FEAT-OCC-01 | RWB-E2-021 | TC-E2-021-01 |
| REQ-OCC-010 | FEAT-OCC-01 | RWB-E2-021 | TC-E2-021-01 |
| REQ-OCC-011 | FEAT-COM-01 | Written one epic ahead | With the story |

## Appendix T-A. API specification

### T-A.1 Endpoint inventory

| ID | Method | Path | Access | First in |
|---|---|---|---|---|
| API-P6-001 | POST | /api/recovery/comms/v1/cases/{caseId}/notices | Litigation C | E2 |
| API-P6-002 | GET | /api/recovery/comms/v1/notices/{noticeId} | Litigation R | E2 |
| API-P6-003 | GET | /api/recovery/comms/v1/admin/templates | Documents R | E1 |
| API-P6-004 | POST | /api/recovery/comms/v1/admin/templates | Documents C | E1 |
| API-P6-005 | GET | /api/recovery/comms/v1/admin/templates/{templateId}/content | Documents R | E1 |
| API-P6-006 | POST | /api/recovery/comms/v1/admin/templates/{templateId}/approve | Documents A | E1 |
| API-P6-007 | POST | /api/recovery/comms/v1/admin/templates/{templateId}/withdraw | Documents A | E1 |
| API-P6-008 | POST | /api/recovery/comms/v1/cases/{caseId}/messages | Case record C | E2 |
| API-P6-009 | POST | /api/recovery/comms/v1/treatments/{treatmentId}/signature-requests | Treatment and offer C | E2 |
| API-P6-010 | GET | /api/recovery/comms/v1/treatments/{treatmentId}/signature-requests | Treatment and offer R | E2 |
| API-P6-011 | POST | /api/recovery/comms/v1/signature-requests/{requestId}/result | Treatment and offer U | E2 |

The operation IDs, paths and operationIds of these endpoints are published in `05 Technical architecture/Recovery Workbench API Specification v5/rwb-comms.yaml`; where an appendix row and the published operation differ, the published operation is the contract of T5.2.1 and the row keeps its ID for traceability (GAP-1997; ASM-3224).

### T-A.2 Endpoint detail

#### API-P6-001 POST /cases/{caseId}/notices

| Item | Value |
|---|---|
| Purpose | Generate a notice from the approved template |
| Request | NoticeRequest |
| Response | Notice |
| Errors | 401, 403, 404, 409, 422, 503 |
| Authorization | Litigation, right C, scope applied |
| Idempotency | Idempotency-Key header |

#### API-P6-002 GET /notices/{noticeId}

| Item | Value |
|---|---|
| Purpose | Read a notice with its dispatch and proof of delivery |
| Request | None |
| Response | Notice |
| Errors | 401, 403, 404, 503 |
| Authorization | Litigation, right R, scope applied |
| Idempotency | Not applicable |

#### API-P6-003 GET /admin/templates

| Item | Value |
|---|---|
| Purpose | List template versions by code, language and state |
| Request | Query: code, language, state, page, size |
| Response | TemplatePage |
| Errors | 401, 403, 503 |
| Authorization | Documents, right R, scope applied |
| Idempotency | Not applicable |

#### API-P6-004 POST /admin/templates

| Item | Value |
|---|---|
| Purpose | Upload a new template version in state DRAFT |
| Request | Multipart: file, templateCode, language, productGroup, channel, noticeType, signatureBasis, mergeCodes |
| Response | Template |
| Errors | 401, 403, 413, 415, 422, 503 |
| Authorization | Documents, right C, scope applied |
| Idempotency | Idempotency-Key header |

#### API-P6-005 GET /admin/templates/{templateId}/content

| Item | Value |
|---|---|
| Purpose | Download a template body |
| Request | None |
| Response | Binary |
| Errors | 401, 403, 404, 503 |
| Authorization | Documents, right R, scope applied |
| Idempotency | Not applicable |

#### API-P6-006 POST /admin/templates/{templateId}/approve

| Item | Value |
|---|---|
| Purpose | Record the Legal approval of a draft template version with its valid from date |
| Request | TemplateApproval |
| Response | Template |
| Errors | 401, 403, 404, 409, 422, 503 |
| Authorization | Documents, right A, scope applied |
| Idempotency | Idempotency-Key header |

#### API-P6-007 POST /admin/templates/{templateId}/withdraw

| Item | Value |
|---|---|
| Purpose | Withdraw an approved template version with a reason |
| Request | TemplateWithdrawal |
| Response | Template |
| Errors | 401, 403, 404, 409, 422, 503 |
| Authorization | Documents, right A, scope applied |
| Idempotency | Idempotency-Key header |

#### API-P6-008 POST /cases/{caseId}/messages

| Item | Value |
|---|---|
| Purpose | Send an SMS or LINE message from an approved template after the conduct check |
| Request | MessageRequest |
| Response | Interaction |
| Errors | 401, 403, 404, 409, 422, 503 |
| Authorization | Case record, right C, scope applied |
| Idempotency | Idempotency-Key header |

#### API-P6-009 POST /treatments/{treatmentId}/signature-requests

| Item | Value |
|---|---|
| Purpose | Send reviewed generated documents for signature by e-signature, branch or paper; copies them to the write-once store and writes the decision log entry |
| Request | SignatureRequestCreate |
| Response | SignatureRequest[] |
| Errors | 401, 403, 404, 409, 422, 503 |
| Authorization | Treatment and offer, right C, scope applied |
| Idempotency | Idempotency-Key header |

#### API-P6-010 GET /treatments/{treatmentId}/signature-requests

| Item | Value |
|---|---|
| Purpose | List the signature requests of a treatment |
| Request | None |
| Response | SignatureRequest[] |
| Errors | 401, 403, 404, 503 |
| Authorization | Treatment and offer, right R, scope applied |
| Idempotency | Not applicable |

#### API-P6-011 POST /signature-requests/{requestId}/result

| Item | Value |
|---|---|
| Purpose | Record a branch or paper signature result with the scanned document |
| Request | SignatureResultRequest |
| Response | SignatureRequest |
| Errors | 401, 403, 404, 409, 422, 503 |
| Authorization | Treatment and offer, right U, scope applied |
| Idempotency | Idempotency-Key header |

## Appendix T-B. Open technical decisions

| Decision | What is needed |
|---|---|
| DL06 | Which interfaces need same-day data |
| DL11 | Non-functional target values |
| DL35 | Deployment slots |

## Document sign-off

| Role | Name | Signature | Date |
|---|---|---|---|
| Solution architect | | | |
| Tech lead | | | |
| ACE team | | | |
| QA lead | | | |
