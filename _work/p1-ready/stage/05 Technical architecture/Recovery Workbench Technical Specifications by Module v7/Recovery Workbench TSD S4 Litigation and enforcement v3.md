SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

# Recovery Workbench S4 Litigation and enforcement

Technical specification. SCB Collections and Recovery. Henka Group, 22 November 2026.

(C) Siam Commercial Bank and Henka Pte Ltd

## Document control

| Attribute | Value |
|---|---|
| Document title | TSD S4 Litigation and enforcement |
| Document ID | S4-RWB-TSD-v3 |
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
| Recovery Workbench FSD S4 Litigation and enforcement | FSD | Pair |
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

S4 Litigation and enforcement is one of the 19 services of Architecture v5: `rwb-litigation` (service name Litigation, module S4, wave 3, service epic `RWB-SVC-S4`). Version 3 adds this section so that the specification is read as the specification of one service: its identity, what it owns, and the decoupling patterns that replace the monolith's in-process calls. Every owner is taken from Microservice Ownership Map v1 and every identifier from Template and Rules R4 (ADR-013, ADR-014).

S4 runs for years and relies on Continue-As-New; the law-firm instruction is a P9 activity on S9's queue (Architecture v5 slide 19).

### T0.1 Service identity

| Item | Value |
|---|---|
| Module | S4 Litigation and enforcement |
| Service | `rwb-litigation` (Litigation) |
| Service epic | `RWB-SVC-S4` |
| Wave | 3 |
| Schema | `rwb_litigation` |
| Database login | `rwb_litigation`: one login per service, with its own connection pool cap |
| REST base | `/api/recovery/litigation/v1` |
| Kafka topic | `rwb.litigation.events.v1`, with `.retry` and `.dlt` topics |
| Event names | `rwb.litigation.<Event>.v1`, CloudEvents 1.0 in binary mode, key `caseId` |
| Temporal | namespace `rwb-recovery`; task queue `rwb-litigation` |
| Java package | `th.co.scb.ace.workbench.recovery.litigation` |
| Edge | gateway-bff for the staff screens of this service |
| Contract artefacts | `05 Technical architecture/Recovery Workbench API Specification v5/rwb-litigation.yaml`; `05 Technical architecture/Recovery Workbench API Specification v5/asyncapi/rwb-litigation.asyncapi.yaml` |
| Suggested owner, app development | TechX (suggested; any team may pick up this story) |
| Suggested owner, ACE DB | ACE team (suggested; any team may pick up this story) |

### T0.2 What this service owns

Architecture v5 slide 41 gives this service: legal actions, hearings, judgments, enforcement, LED auction ladder. Table T0.2 states the same ownership in the form the Ownership Map uses, with the counts this specification carries. A table that the map assigns to another service is not built here, whatever T3 says (see the note under T3).

| Area | Owner and artefact | Count |
|---|---|---|
| Business tables in `rwb_litigation` | `hearing`, `legal_action` | 2 |
| REST operations | appendix T-A and `rwb-litigation.yaml` | 5 |
| Events published | JudgmentRecorded, AuctionResult | 2 |
| Workflows and schedules | LitigationWorkflow | 1 |
| Jobs | none | 0 |

### T0.3 Decoupling patterns applied

The left column is the pattern of Template and Rules R5.5; the middle column quotes the line of this specification that carries the legacy marker, where one is present; the right column is what replaces it in this service.

| DP | Legacy marker in this specification | How the service lands it |
|---|---|---|
| DP-01 | — | Owns its tables in `rwb_litigation`; no other service reads them (ADR-014). |
| DP-02 | — | One login, `rwb_litigation`, with its own connection pool cap. |
| DP-03 | `…logic; calls the rules component; writes the decision log entry before any change` | Local decision record plus DecisionRecorded (EV-08) on `rwb.decision-record.v1`. |
| DP-07 | `DF-LEG-004 / action_type / LOV / varchar(20) / Yes / LOV-LEGAL-TYPE / Workbench` | Reference data and lists of values from the `rwb-case` contract (H RWB-PLT-E1043-CON). |
| DP-08 | `RW-CASEOWN Case owner / R` | Authorisation through the `rwb-access` authorise contract and the guard library (H RWB-PLT-E1037-CON). |
| DP-09 | — | Outbox and inbox library; CloudEvents on `rwb.litigation.events.v1` with retry topics and `.dlt`. |
| DP-10 | `Scheduler and batch / REUSE / ACE pattern: Quartz and Spring Batch / Jobs in the Batch and…` | Temporal Schedules and event-started workflows through the workflow kit (ADR-016). |
| DP-11 | `…reaches other modules only through their published interfaces and other systems only through COLLINS,…` | One REST hop, 2 s timeout, breaker; the consumer builds against the provider's fake (ADR-020). |
| DP-13 | `API-S4-001 / POST / /api/recovery/v1/notices/{noticeId}/approve / Litigation…` | REST base `/api/recovery/litigation/v1`. |
| DP-14 | — | Topic `rwb.litigation.events.v1`, retry topics and `.dlt`; naming library (H RWB-PLT-E1047-CON). |
| DP-15 | — | Per-service Flyway sequence in `rwb_litigation`. |

### T0.4 What this service is not

- It holds no other service's table and no ACE table beyond the read-only `recovery.v_ace_*` views (DP-01, DP-05).
- It runs no shared Quartz job and touches no ACE batch table (DP-10; ADR-016).
- It instructs no partner itself: the law-firm instruction runs on S9's queue (DP-11).
- It is not a monolith module: the published Java interface of T2 is replaced by the contract set of T5.2 (DP-11; ADR-020).

## T1. Architecture overview

S4 Litigation and enforcement is delivered as the service `rwb-litigation` (module S4, wave 3, service epic `RWB-SVC-S4`): one repository, one pipeline, one schema `rwb_litigation` with one login, behind gateway-bff (ADR-013, ADR-014). It covers: notices, law firm instruction, hearings, judgment, enforcement. It reaches other modules only through the contracts of T5.2 and other systems only through COLLINS, file loads and the ACE paths.

## T2. Component design

| Component | Responsibility |
|---|---|
| LitigationAndEnforcementController | REST endpoints in appendix T-A; validation; maps errors to problem responses |
| LitigationAndEnforcementService | Business logic; calls the rules component; writes the decision log entry before any change |
| LitigationAndEnforcementRepository | Reads and writes the module's tables only |
| Jobs | Temporal Schedules and event-started workflows this service owns (T0.2, T5.2.1; DP-10) |
| Published interface | The contracts of T5.2: REST operations, events and workflows other services call; no table is read across modules (DP-11) |

The published interface of this table is the contract set of T5.2: the REST operations, the events and the workflows, not a Java interface in a shared classpath (DP-11; ADR-020). Components that the Ownership Map places in another service are stated in T0.2 and T5.2 and are built by that service.

## T3. Data model

Every object of T3 that Microservice Ownership Map v1 assigns to `rwb-litigation` lives in schema `rwb_litigation` with the standard columns of T3.0 (DP-01, DP-15; ADR-014). `legal_action` and `hearing` are this service's tables; the partner result arrives as an event and is never written here from a partner table (DP-01, DP-11).

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

**legal_action** (NEW). A notice, lawsuit, appeal, enforcement or bankruptcy action on a case.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-LEG-001 | id | TEXT | uuid | Yes | None | Workbench |
| DF-LEG-002 | case_id | CROSS_REF | uuid | Yes | None | Workbench |
| DF-LEG-003 | law_firm_id | CROSS_REF | uuid | No | None | Workbench |
| DF-LEG-004 | action_type | LOV | varchar(20) | Yes | LOV-LEGAL-TYPE | Workbench |
| DF-LEG-005 | lawsuit_no | TEXT | varchar(30) | No | None | LIT |
| DF-LEG-006 | black_case_no | TEXT | varchar(30) | No | None | LIT |
| DF-LEG-007 | red_case_no | TEXT | varchar(30) | No | None | LIT |
| DF-LEG-008 | court_name | TEXT | varchar(120) | No | None | LIT |
| DF-LEG-009 | claim_amount | NUMBER | numeric(18,2) | No | None | LIT |
| DF-LEG-010 | filed_date | DATE | date | No | None | LIT |
| DF-LEG-011 | judgment_date | DATE | date | No | None | LIT |
| DF-LEG-012 | judgment_amount | NUMBER | numeric(18,2) | No | None | LIT |
| DF-LEG-013 | lit_status | TEXT | varchar(200) | No | None | LIT via COLLINS |
| DF-LEG-014 | status | LOV | varchar(15) | Yes | LOV-LEGAL-STATUS | Workbench |

**hearing** (NEW). A court hearing on a legal action.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-LEG-024 | id | TEXT | uuid | Yes | None | Workbench |
| DF-LEG-025 | legal_action_id | CROSS_REF | uuid | Yes | None | Workbench |
| DF-LEG-026 | hearing_date | DATE | timestamptz | Yes | None | LIT |
| DF-LEG-027 | hearing_type | LOV | varchar(20) | No | LOV-HEARING | LIT |
| DF-LEG-028 | outcome | LOV | varchar(20) | No | LOV-HEARING-OUTCOME | Workbench |
| DF-LEG-029 | next_date | DATE | timestamptz | No | None | LIT |

### T3.2 Lists of values

| List | Values |
|---|---|
| LOV-HEARING | FIRST_HEARING, WITNESS, JUDGMENT_READING, MEDIATION |
| LOV-HEARING-OUTCOME | HELD, ADJOURNED, SETTLED, JUDGMENT |
| LOV-LEGAL-STATUS | OPEN, FILED, JUDGMENT, ENFORCING, CLOSED, WITHDRAWN |
| LOV-LEGAL-TYPE | NOTICE, CIVIL_CASE, APPEAL, ENFORCEMENT, BANKRUPTCY_PETITION, LED_AUCTION |

### T3.3 Relationships

| From | To | Field | Cardinality |
|---|---|---|---|
| legal_action | case_id | recovery_case | Many to 1 |
| legal_action | law_firm_id | partner | Many to 0 or 1 |
| hearing | legal_action_id | legal_action | Many to 1 |

## T4. State machines and workflow

**LITIGATION.** 79 rules over 38 states. The full table is in the Business Rules and Routing Logic workbook.

| Rule | From | Event | To |
|---|---|---|---|
| R-LIT-01 | LIT_ROUTE_APPROVED | ROUTE_APPROVED | NOTICE_GENERATED |
| R-LIT-02 | LIT_ROUTE_APPROVED | TREATMENT_BROKEN | NOTICE_GENERATED |
| R-LIT-03 | NOTICE_GENERATED | TEMPLATE_SELECTED | NOTICE_DISPATCHED |
| R-LIT-04 | NOTICE_GENERATED | TEMPLATE_WITHDRAWN | NOTICE_BLOCKED |
| R-LIT-05 | NOTICE_GENERATED | CONTACT_STOP_APPLIED | NOTICE_BLOCKED |
| R-LIT-06 | NOTICE_BLOCKED | TEMPLATE_REPLACED | NOTICE_GENERATED |
| R-LIT-07 | NOTICE_DISPATCHED | PROOF_OF_DELIVERY_RECEIVED | WITH_CUSTOMER_NOTICE_PERIOD |
| R-LIT-08 | NOTICE_DISPATCHED | PROOF_WINDOW_EXPIRED | NOTICE_UNSERVED |
| R-LIT-09 | NOTICE_DISPATCHED | DELIVERY_FAILED | NOTICE_UNSERVED |
| R-LIT-10 | NOTICE_UNSERVED | ALTERNATE_SERVICE_ORDERED | NOTICE_DISPATCHED |
| R-LIT-11 | NOTICE_UNSERVED | PRESCRIPTION_WARNING | PACK_ASSEMBLY |
| R-LIT-12 | WITH_CUSTOMER_NOTICE_PERIOD | CUSTOMER_PAID_IN_FULL | CASE_CLOSED |
| R-LIT-13 | WITH_CUSTOMER_NOTICE_PERIOD | CUSTOMER_REQUESTED_TREATMENT | TO_TREATMENT |
| R-LIT-14 | WITH_CUSTOMER_NOTICE_PERIOD | CUSTOMER_DISPUTED | DEVIATION_HOLD |
| R-LIT-15 | WITH_CUSTOMER_NOTICE_PERIOD | NOTICE_PERIOD_EXPIRED | PACK_ASSEMBLY |
| R-LIT-16 | PACK_ASSEMBLY | PACK_COMPLETE | PACK_VERIFIED |
| R-LIT-17 | PACK_ASSEMBLY | PACK_INCOMPLETE | PACK_DEFECT_HOLD |
| R-LIT-18 | PACK_DEFECT_HOLD | DOCUMENT_RETRIEVED | PACK_ASSEMBLY |
| R-LIT-19 | PACK_DEFECT_HOLD | DOCUMENT_UNRECOVERABLE | PACK_VERIFIED |
| R-LIT-20 | PACK_DEFECT_HOLD | PRESCRIPTION_WARNING | PACK_VERIFIED |
| R-LIT-21 | PACK_VERIFIED | OFFICER_REJECTED_PACK | PACK_ASSEMBLY |
| R-LIT-22 | PACK_VERIFIED | CONDUCT_CHECK_FAILED | NOTICE_BLOCKED |
| R-LIT-23 | PACK_VERIFIED | PACK_APPROVED | FIRM_SELECTION |
| R-LIT-24 | FIRM_SELECTION | FIRM_MATCHED | FIRM_INSTRUCTED |
| R-LIT-25 | FIRM_SELECTION | NO_FIRM_AVAILABLE | FIRM_ESCALATED |
| and 54 more | | | |

## T5. Integration and interfaces

### T5.1 External system interfaces

| ID | System | Direction | Approach | Frequency |
|---|---|---|---|---|
| INT-09 | LIT | In | COLLINS batch | Daily, end of day |
| INT-33 | Legal Execution Department and courts | In | Through the law firms in the partner portal | As entered |

### T5.2 Contracts

Version 3 states every cross-module dependency of this module as a contract, so that the service is built against a published artefact and its fake (ADR-020; DP-11). The artefact per call type is: OpenAPI 3.1 for REST, AsyncAPI 3.0 for Kafka, the Temporal interface named here for a workflow or activity, the Interface Specifications manifest for a file, the Nexus operation for the ACE restructure calculator, and a grant on the view for SQL. No row of this section reads another service's table (DP-01). Every consumed contract is class C (Template and Rules R5.4): it never blocks the build, because the consumer builds against the fake, and the real cross-service behaviour is class I work on an integration story. Architecture v5 slides 13 to 20 name a few operations differently from the published files of 22 November 2026; the published file is the artefact the fake is generated from and is the one cited here (GAP-1997; ASM-3224).

#### T5.2.1 Contracts provided

The REST operations of this service are published in `05 Technical architecture/Recovery Workbench API Specification v5/rwb-litigation.yaml` (5.0.0, 22 November 2026) under the base `/api/recovery/litigation/v1`. Appendix T-A holds the endpoint IDs, the access right and the first release of each one.

| # | Method | Path | operationId |
|---|---|---|---|
| 1 | POST | `/notices/{noticeId}/approve` | `postNoticesNoticeidApprove` |
| 2 | POST | `/cases/{caseId}/legal-actions` | `postCasesCaseidLegalActions` |
| 3 | GET | `/legal-actions/{legalActionId}` | `getLegalActionsLegalactionid` |
| 4 | PATCH | `/legal-actions/{legalActionId}` | `patchLegalActionsLegalactionid` |
| 5 | POST | `/legal-actions/{legalActionId}/hearings` | `postLegalActionsLegalactionidHearings` |

Workflows, schedules, files and views this service provides:

| Contract | Type | Called by or target | Note |
|---|---|---|---|
| LitigationWorkflow (years; continues as new) | Temporal workflow | P3 rwb-case | Stage workflow of the case; runs on rwb-litigation |

Events this service publishes (AsyncAPI 3.0, CloudEvents 1.0):

| Event | EV | Topic | Consumers |
|---|---|---|---|
| JudgmentRecorded | — | `rwb.litigation.events.v1` | rwb-asset, rwb-case |
| AuctionResult | — | `rwb.litigation.events.v1` | rwb-asset, rwb-case |

#### T5.2.2 Contracts consumed

| Contract | Type | Provider | Class | Failure path |
|---|---|---|---|---|
| issueInstruction (law firm) | Temporal activity | S9 rwb-partner | C | Workflow retry policy; the caller keeps its state (DP-12) |
| Demand notice | Temporal child workflow | P6 rwb-comms | C | Workflow retry policy; the caller keeps its state (DP-12) |
| Approval | Temporal child workflow | P7 rwb-decision | C | Workflow retry policy; the caller keeps its state (DP-12) |

Events this service consumes:

| Event | EV | Provider topic | Provider | Class | Failure path |
|---|---|---|---|---|---|
| NoticeDelivered | EV-15 | `rwb.comms.events.v1` | P6 rwb-comms | C | Retry 1 min, 10 min, 1 h, then `.dlt`; inbox dedupe |
| PartnerResultSubmitted | EV-21 | `rwb.partner.events.v1` | S9 rwb-partner | C | Retry 1 min, 10 min, 1 h, then `.dlt`; inbox dedupe |

#### T5.2.3 Call-type summary

| Call type | Provided | Consumed | Artefact |
|---|---|---|---|
| REST | 5 | 0 | OpenAPI 3.1, one file per service |
| Kafka (events) | 2 | 2 | AsyncAPI 3.0, one file per service |
| Temporal | 1 | 3 | Workflow and activity interfaces, queue `rwb-litigation` |
| File | 0 | 0 | Interface Specifications manifest and the SAS link |
| Nexus | 0 | 0 | Nexus operation into ACE |
| SQL | 0 | 0 | Read-only grant on the view |

A contract change is a new version of the artefact, never a code change in the consumer (ADR-020). The provider named in T5.2.2 is the owner in Microservice Ownership Map v1, and the consumer list of each event is the Arch v5 event catalogue on slides 42 and 43.

### T5.3 Events

The event contract of this service is `05 Technical architecture/Recovery Workbench API Specification v5/asyncapi/rwb-litigation.asyncapi.yaml`; the shared decision-record contract is `asyncapi/rwb.decision-record.v1.asyncapi.yaml`. Every service publishes DecisionRecorded (EV-08) to `rwb.decision-record.v1` from its outbox in the same transaction as its state change (DP-03, DP-09; ADR-015, ADR-022); consuming services dedupe through their inbox table. Events carry identifiers and facts, never personal data (Event and Messaging Design v4, sheet Rules).

| Event | EV | Direction | Topic |
|---|---|---|---|
| JudgmentRecorded | — | Published | `rwb.litigation.events.v1` |
| AuctionResult | — | Published | `rwb.litigation.events.v1` |
| NoticeDelivered | EV-15 | Consumed | `rwb.comms.events.v1` |
| PartnerResultSubmitted | EV-21 | Consumed | `rwb.partner.events.v1` |

An event shown with `—` has no number in the numbered catalogue: the Arch v5 catalogue calls these rows `+`, so the number is not specified in the source documents (GAP-1996; ASM-3223). Architecture v5 slide 19 names LawsuitFiled on `rwb.litigation.events.v1`; the AsyncAPI document of 22 November 2026 does not carry it (GAP-1996; ASM-3223).

## T6. Security and access control

### T6.1 RBAC matrix

| Role | Litigation |
|---|---|
| RW-CASEOWN Case owner | R |
| RW-TEAMMGR Team manager | R |
| RW-COMPLAIN Complaint officer | R |
| RW-FRAUD Fraud investigator | R |
| RW-LITOFF Litigation officer | CRUA |
| RW-ENFORCE Enforcement owner | CRU |
| RW-LEGAL Legal counsel | RA |
| RW-SALEOFF Sale officer | R |
| RW-NPAMGR NPA and asset manager | R |
| RW-DEBTSALE Debt sale officer | R |
| RW-WRITEOFF Write-off team member | R |
| RW-CREDITAD Credit Administration officer | R |
| RW-GUARANT Guarantee officer | R |
| RW-AGENCYMG Partner and agency manager | R |
| RW-CONDUCT Conduct and QA officer | R |
| RW-PRODHEAD Product head (Mortgage, HP, SSME) | RA |
| RW-HEADLIT Head of Litigation | RA |
| RW-HEADNPA Head of NPA | R |
| RW-HEADASL Head of Asset Liquidity | R |
| RW-RISK Risk and model risk officer | R |
| RW-COE Center of excellence analyst | R |
| RW-AUDIT Internal audit | R |
| RW-COMPLY Compliance and PDPA officer | R |
| RW-BIANAL Reporting and BI analyst | R |
| RW-TRIBE Tribe lead and squad members | R |
| PT-LAWFIRM Law firm user | RU |
| SY-CASEWF Case workflow module | R |
| SY-RULES Rules component | R |
| SY-DATALOAD Data load from COLLINS | U |
| SY-AGENT Agent platform | R |

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
| REQ-S4-001 | FEAT-LIT-01 | Written one epic ahead | With the story |
| REQ-S4-002 | FEAT-LIT-01 | Written one epic ahead | With the story |
| REQ-S4-003 | FEAT-LIT-01 | Written one epic ahead | With the story |
| REQ-S4-004 | FEAT-LIT-01 | Written one epic ahead | With the story |
| REQ-S4-005 | FEAT-LIT-01 | Written one epic ahead | With the story |
| REQ-S4-006 | FEAT-LIT-01 | Written one epic ahead | With the story |
| REQ-S4-007 | FEAT-LIT-01 | Written one epic ahead | With the story |
| REQ-S4-008 | FEAT-LIT-01 | Written one epic ahead | With the story |
| REQ-S4-009 | FEAT-LIT-01 | Written one epic ahead | With the story |
| REQ-S4-010 | FEAT-LIT-01 | Written one epic ahead | With the story |

## Appendix T-A. API specification

### T-A.1 Endpoint inventory

| ID | Method | Path | Access | First in |
|---|---|---|---|---|
| API-S4-001 | POST | /api/recovery/litigation/v1/notices/{noticeId}/approve | Litigation A | E2 |
| API-S4-002 | POST | /api/recovery/litigation/v1/cases/{caseId}/legal-actions | Litigation C | E5 |
| API-S4-003 | GET | /api/recovery/litigation/v1/legal-actions/{legalActionId} | Litigation R | E5 |
| API-S4-004 | PATCH | /api/recovery/litigation/v1/legal-actions/{legalActionId} | Litigation U | E5 |
| API-S4-005 | POST | /api/recovery/litigation/v1/legal-actions/{legalActionId}/hearings | Litigation U | E5 |

The operation IDs, paths and operationIds of these endpoints are published in `05 Technical architecture/Recovery Workbench API Specification v5/rwb-litigation.yaml`; where an appendix row and the published operation differ, the published operation is the contract of T5.2.1 and the row keeps its ID for traceability (GAP-1997; ASM-3224).

### T-A.2 Endpoint detail

#### API-S4-001 POST /notices/{noticeId}/approve

| Item | Value |
|---|---|
| Purpose | Approve a generated notice for dispatch |
| Request | None |
| Response | Notice |
| Errors | 401, 403, 404, 409, 503 |
| Authorization | Litigation, right A, scope applied |
| Idempotency | Idempotency-Key header |

#### API-S4-002 POST /cases/{caseId}/legal-actions

| Item | Value |
|---|---|
| Purpose | Open a legal action and its pack |
| Request | LegalActionRequest |
| Response | LegalAction |
| Errors | 401, 403, 404, 409, 422, 503 |
| Authorization | Litigation, right C, scope applied |
| Idempotency | Idempotency-Key header |

#### API-S4-003 GET /legal-actions/{legalActionId}

| Item | Value |
|---|---|
| Purpose | Read a legal action with pack, instruction, hearings and judgment |
| Request | None |
| Response | LegalAction |
| Errors | 401, 403, 404, 503 |
| Authorization | Litigation, right R, scope applied |
| Idempotency | Not applicable |

#### API-S4-004 PATCH /legal-actions/{legalActionId}

| Item | Value |
|---|---|
| Purpose | Record a filing, judgment or enforcement step |
| Request | LegalActionUpdate |
| Response | LegalAction |
| Errors | 401, 403, 404, 409, 422, 503 |
| Authorization | Litigation, right U, scope applied |
| Idempotency | Not applicable |

#### API-S4-005 POST /legal-actions/{legalActionId}/hearings

| Item | Value |
|---|---|
| Purpose | Add a hearing date |
| Request | HearingRequest |
| Response | Hearing |
| Errors | 401, 403, 404, 422, 503 |
| Authorization | Litigation, right U, scope applied |
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
