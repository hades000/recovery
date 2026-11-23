SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

# Recovery Workbench S7 Write-off and recovery

Technical specification. SCB Collections and Recovery. Henka Group, 22 November 2026.

(C) Siam Commercial Bank and Henka Pte Ltd

## Document control

| Attribute | Value |
|---|---|
| Document title | TSD S7 Write-off and recovery |
| Document ID | S7-RWB-TSD-v3 |
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
| Recovery Workbench FSD S7 Write-off and recovery | FSD | Pair |
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

S7 Write-off and recovery is one of the 19 services of Architecture v5: `rwb-writeoff` (service name Write-off, module S7, wave 4, service epic `RWB-SVC-S7`). Version 3 adds this section so that the specification is read as the specification of one service: its identity, what it owns, and the decoupling patterns that replace the monolith's in-process calls. Every owner is taken from Microservice Ownership Map v1 and every identifier from Template and Rules R4 (ADR-013, ADR-014).

S7 owns the write-off and the recovery after charge-off; the committee decision is a P7 child workflow and the postings are read from ACE (Architecture v5 slide 20).

### T0.1 Service identity

| Item | Value |
|---|---|
| Module | S7 Write-off and recovery |
| Service | `rwb-writeoff` (Write-off) |
| Service epic | `RWB-SVC-S7` |
| Wave | 4 |
| Schema | `rwb_writeoff` |
| Database login | `rwb_writeoff`: one login per service, with its own connection pool cap |
| REST base | `/api/recovery/writeoff/v1` |
| Kafka topic | `rwb.writeoff.events.v1`, with `.retry` and `.dlt` topics |
| Event names | `rwb.writeoff.<Event>.v1`, CloudEvents 1.0 in binary mode, key `caseId` |
| Temporal | namespace `rwb-recovery`; task queue `rwb-writeoff` |
| Java package | `th.co.scb.ace.workbench.recovery.writeoff` |
| Edge | gateway-bff for the staff screens of this service |
| Contract artefacts | `05 Technical architecture/Recovery Workbench API Specification v5/rwb-writeoff.yaml`; `05 Technical architecture/Recovery Workbench API Specification v5/asyncapi/rwb-writeoff.asyncapi.yaml` |
| Suggested owner, app development | TechX (suggested; any team may pick up this story) |
| Suggested owner, ACE DB | ACE team (suggested; any team may pick up this story) |

### T0.2 What this service owns

Architecture v5 slide 41 gives this service: eligibility, committee, posting, recovery after charge-off. Table T0.2 states the same ownership in the form the Ownership Map uses, with the counts this specification carries. A table that the map assigns to another service is not built here, whatever T3 says (see the note under T3).

| Area | Owner and artefact | Count |
|---|---|---|
| Business tables in `rwb_writeoff` | `write_off` | 1 |
| REST operations | appendix T-A and `rwb-writeoff.yaml` | 2 |
| Events published | EV-24 WriteOffApproved | 1 |
| Workflows and schedules | WriteOffWorkflow | 1 |
| Jobs | JOB-16 | 1 |

### T0.3 Decoupling patterns applied

The left column is the pattern of Template and Rules R5.5; the middle column quotes the line of this specification that carries the legacy marker, where one is present; the right column is what replaces it in this service.

| DP | Legacy marker in this specification | How the service lands it |
|---|---|---|
| DP-01 | — | Owns its tables in `rwb_writeoff`; no other service reads them (ADR-014). |
| DP-02 | — | One login, `rwb_writeoff`, with its own connection pool cap. |
| DP-03 | `…logic; calls the rules component; writes the decision log entry before any change` | Local decision record plus DecisionRecorded (EV-08) on `rwb.decision-record.v1`. |
| DP-07 | — | Reference data and lists of values from the `rwb-case` contract (H RWB-PLT-E1043-CON). |
| DP-08 | `RW-FRAUD Fraud investigator / R` | Authorisation through the `rwb-access` authorise contract and the guard library (H RWB-PLT-E1037-CON). |
| DP-09 | — | Outbox and inbox library; CloudEvents on `rwb.writeoff.events.v1` with retry topics and `.dlt`. |
| DP-10 | `Scheduler and batch / REUSE / ACE pattern: Quartz and Spring Batch / Jobs in the Batch and…` | Temporal Schedules and event-started workflows through the workflow kit (ADR-016). |
| DP-11 | `…reaches other modules only through their published interfaces and other systems only through COLLINS,…` | One REST hop, 2 s timeout, breaker; the consumer builds against the provider's fake (ADR-020). |
| DP-13 | `API-S7-001 / POST / /api/recovery/v1/write-off-scans / Write-off and posting…` | REST base `/api/recovery/writeoff/v1`. |
| DP-14 | — | Topic `rwb.writeoff.events.v1`, retry topics and `.dlt`; naming library (H RWB-PLT-E1047-CON). |
| DP-15 | — | Per-service Flyway sequence in `rwb_writeoff`. |

### T0.4 What this service is not

- It holds no other service's table and no ACE table beyond the read-only `recovery.v_ace_*` views (DP-01, DP-05).
- It runs no shared Quartz job and touches no ACE batch table (DP-10; ADR-016).
- It posts nothing to the GL: the postings stay in ACE and are read through P1 (INT-16).
- It is not a monolith module: the published Java interface of T2 is replaced by the contract set of T5.2 (DP-11; ADR-020).

## T1. Architecture overview

S7 Write-off and recovery is delivered as the service `rwb-writeoff` (module S7, wave 4, service epic `RWB-SVC-S7`): one repository, one pipeline, one schema `rwb_writeoff` with one login, behind gateway-bff (ADR-013, ADR-014). It covers: eligibility, committee, posting, recovery after charge-off. It reaches other modules only through the contracts of T5.2 and other systems only through COLLINS, file loads and the ACE paths.

## T2. Component design

| Component | Responsibility |
|---|---|
| Write-OffAndRecoveryController | REST endpoints in appendix T-A; validation; maps errors to problem responses |
| Write-OffAndRecoveryService | Business logic; calls the rules component; writes the decision log entry before any change |
| Write-OffAndRecoveryRepository | Reads and writes the module's tables only |
| Jobs | Temporal Schedules and event-started workflows this service owns (T0.2, T5.2.1; DP-10) |
| Published interface | The contracts of T5.2: REST operations, events and workflows other services call; no table is read across modules (DP-11) |

The published interface of this table is the contract set of T5.2: the REST operations, the events and the workflows, not a Java interface in a shared classpath (DP-11; ADR-020). Components that the Ownership Map places in another service are stated in T0.2 and T5.2 and are built by that service.

## T3. Data model

Every object of T3 that Microservice Ownership Map v1 assigns to `rwb-writeoff` lives in schema `rwb_writeoff` with the standard columns of T3.0 (DP-01, DP-15; ADR-014). `write_off` is this service's table; the GL postings stay in ACE and are read through the P1 contract (INT-16, DP-05).

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

**write_off** (NEW). A write-off of the balance on a case.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-FIN-010 | id | TEXT | uuid | Yes | None | Workbench |
| DF-FIN-011 | case_id | CROSS_REF | uuid | Yes | None | Workbench |
| DF-FIN-012 | decision_log_id | CROSS_REF | uuid | No | None | Workbench |
| DF-FIN-013 | amount | NUMBER | numeric(18,2) | Yes | None | GL |
| DF-FIN-014 | tax_criteria_met | BOOLEAN | boolean | Yes | None | Workbench |
| DF-FIN-015 | committee_date | DATE | date | No | None | Workbench |
| DF-FIN-016 | posted_date | DATE | date | No | None | GL |
| DF-FIN-017 | responsibility_center | TEXT | varchar(10) | No | None | GL |
| DF-FIN-018 | cost_center | TEXT | varchar(10) | No | None | GL |
| DF-FIN-019 | gl_product | TEXT | varchar(10) | No | None | GL |
| DF-FIN-020 | recovered_after | NUMBER | numeric(18,2) | Yes | None | Workbench |

### T3.2 Lists of values

| List | Values |
|---|---|

### T3.3 Relationships

| From | To | Field | Cardinality |
|---|---|---|---|
| write_off | case_id | recovery_case | Many to 1 |
| write_off | decision_log_id | decision_log_entry | Many to 0 or 1 |

## T4. State machines and workflow

**WRITEOFF.** 51 rules over 27 states. The full table is in the Business Rules and Routing Logic workbook.

| Rule | From | Event | To |
|---|---|---|---|
| R-WO-01 | SCAN_DUE | MONTHLY_SCAN_STARTED | POPULATION_PROPOSED |
| R-WO-02 | SCAN_DUE | ALS_LOAD_FAILED | SCAN_HELD |
| R-WO-03 | SCAN_DUE | TAX_CRITERIA_UNPUBLISHED | SCAN_HELD |
| R-WO-04 | SCAN_HELD | LOAD_RESTORED | SCAN_DUE |
| R-WO-05 | POPULATION_PROPOSED | PACK_BUILT | PACK_PREPARED |
| R-WO-06 | POPULATION_PROPOSED | CASE_HAS_OPEN_DEVIATION | CASE_REMOVED_BY_TEAM |
| R-WO-07 | POPULATION_PROPOSED | TEAM_REMOVED_CASE | CASE_REMOVED_BY_TEAM |
| R-WO-08 | CASE_REMOVED_BY_TEAM | REMOVAL_CLEARED | SCAN_DUE |
| R-WO-09 | PACK_PREPARED | PACK_CHECK_FAILED | PACK_INCOMPLETE |
| R-WO-10 | PACK_INCOMPLETE | PACK_COMPLETED | WITH_COMMITTEE |
| R-WO-11 | PACK_PREPARED | PACK_ROUTED | WITH_COMMITTEE |
| R-WO-12 | PACK_PREPARED | LIMIT_EXCEEDED | ESCALATED_TO_CREDIT_COMMITTEE |
| R-WO-13 | ESCALATED_TO_CREDIT_COMMITTEE | CREDIT_COMMITTEE_APPROVED | APPROVED |
| R-WO-14 | ESCALATED_TO_CREDIT_COMMITTEE | CREDIT_COMMITTEE_REJECTED | RETURNED_TO_PURSUE |
| R-WO-15 | WITH_COMMITTEE | COMMITTEE_APPROVED | APPROVED |
| R-WO-16 | WITH_COMMITTEE | COMMITTEE_REJECTED | RETURNED_TO_PURSUE |
| R-WO-17 | WITH_COMMITTEE | COMMITTEE_DEFERRED | DEFERRED |
| R-WO-18 | WITH_COMMITTEE | DECISION_INCOMPLETE | WITH_COMMITTEE |
| R-WO-19 | DEFERRED | REVIEW_DATE_REACHED | SCAN_DUE |
| R-WO-20 | APPROVED | POSTING_TASK_CREATED | POSTING_PENDING |
| R-WO-21 | POSTING_PENDING | ALS_POSTING_CONFIRMED | POSTED |
| R-WO-22 | POSTING_PENDING | ALS_POSTING_REJECTED | POSTING_REJECTED |
| R-WO-23 | POSTING_REJECTED | REJECTION_CLEARED | POSTING_PENDING |
| R-WO-24 | POSTING_REJECTED | RETRY_LIMIT_REACHED | WRITEOFF_EXCEPTION |
| R-WO-25 | POSTED | PROVISION_RELEASE_RUN | PROVISION_RELEASED |
| and 26 more | | | |

## T5. Integration and interfaces

### T5.1 External system interfaces

| ID | System | Direction | Approach | Frequency |
|---|---|---|---|---|
| None | | | | |

### T5.2 Contracts

Version 3 states every cross-module dependency of this module as a contract, so that the service is built against a published artefact and its fake (ADR-020; DP-11). The artefact per call type is: OpenAPI 3.1 for REST, AsyncAPI 3.0 for Kafka, the Temporal interface named here for a workflow or activity, the Interface Specifications manifest for a file, the Nexus operation for the ACE restructure calculator, and a grant on the view for SQL. No row of this section reads another service's table (DP-01). Every consumed contract is class C (Template and Rules R5.4): it never blocks the build, because the consumer builds against the fake, and the real cross-service behaviour is class I work on an integration story. Architecture v5 slides 13 to 20 name a few operations differently from the published files of 22 November 2026; the published file is the artefact the fake is generated from and is the one cited here (GAP-1997; ASM-3224).

#### T5.2.1 Contracts provided

The REST operations of this service are published in `05 Technical architecture/Recovery Workbench API Specification v5/rwb-writeoff.yaml` (5.0.0, 22 November 2026) under the base `/api/recovery/writeoff/v1`. Appendix T-A holds the endpoint IDs, the access right and the first release of each one.

| # | Method | Path | operationId |
|---|---|---|---|
| 1 | POST | `/write-off-scans` | `postWriteOffScans` |
| 2 | POST | `/write-offs/{writeOffId}/committee-decision` | `postWriteOffsWriteoffidCommitteeDecision` |

Workflows, schedules, files and views this service provides:

| Contract | Type | Called by or target | Note |
|---|---|---|---|
| WriteOffWorkflow | Temporal workflow | P3 rwb-case | Stage workflow of the case; runs on rwb-writeoff |
| Scan, third working day | Temporal Schedule | S7 rwb-writeoff | JOB-16 (DP-10) |

Events this service publishes (AsyncAPI 3.0, CloudEvents 1.0):

| Event | EV | Topic | Consumers |
|---|---|---|---|
| WriteOffApproved | EV-24 | `rwb.writeoff.events.v1` | rwb-case, rwb-payment, rwb-reporting |

#### T5.2.2 Contracts consumed

| Contract | Type | Provider | Class | Failure path |
|---|---|---|---|---|
| GL write-off outcome, read-only | REST | P1 rwb-source-data | C | 2 s timeout, breaker; built against the fake (ADR-020) |
| Committee approval | Temporal child workflow | P7 rwb-decision | C | Workflow retry policy; the caller keeps its state (DP-12) |
| postProceeds | Temporal activity | P8 rwb-payment | C | Workflow retry policy; the caller keeps its state (DP-12) |

Events this service consumes:

| Event | EV | Provider topic | Provider | Class | Failure path |
|---|---|---|---|---|---|
| AceDataReady | EV-26 | `rwb.source-data.events.v1` | P1 rwb-source-data | C | Retry 1 min, 10 min, 1 h, then `.dlt`; inbox dedupe |
| ProceedsMatched | EV-25 | `rwb.payment.events.v1` | P8 rwb-payment | C | Retry 1 min, 10 min, 1 h, then `.dlt`; inbox dedupe |

#### T5.2.3 Call-type summary

| Call type | Provided | Consumed | Artefact |
|---|---|---|---|
| REST | 2 | 1 | OpenAPI 3.1, one file per service |
| Kafka (events) | 1 | 2 | AsyncAPI 3.0, one file per service |
| Temporal | 2 | 2 | Workflow and activity interfaces, queue `rwb-writeoff` |
| File | 0 | 0 | Interface Specifications manifest and the SAS link |
| Nexus | 0 | 0 | Nexus operation into ACE |
| SQL | 0 | 0 | Read-only grant on the view |

A contract change is a new version of the artefact, never a code change in the consumer (ADR-020). The provider named in T5.2.2 is the owner in Microservice Ownership Map v1, and the consumer list of each event is the Arch v5 event catalogue on slides 42 and 43.

### T5.3 Events

The event contract of this service is `05 Technical architecture/Recovery Workbench API Specification v5/asyncapi/rwb-writeoff.asyncapi.yaml`; the shared decision-record contract is `asyncapi/rwb.decision-record.v1.asyncapi.yaml`. Every service publishes DecisionRecorded (EV-08) to `rwb.decision-record.v1` from its outbox in the same transaction as its state change (DP-03, DP-09; ADR-015, ADR-022); consuming services dedupe through their inbox table. Events carry identifiers and facts, never personal data (Event and Messaging Design v4, sheet Rules).

| Event | EV | Direction | Topic |
|---|---|---|---|
| WriteOffApproved | EV-24 | Published | `rwb.writeoff.events.v1` |
| AceDataReady | EV-26 | Consumed | `rwb.source-data.events.v1` |
| ProceedsMatched | EV-25 | Consumed | `rwb.payment.events.v1` |

An event shown with `—` has no number in the numbered catalogue: the Arch v5 catalogue calls these rows `+`, so the number is not specified in the source documents (GAP-1996; ASM-3223).

## T6. Security and access control

### T6.1 RBAC matrix

| Role | Write-off and posting |
|---|---|
| RW-FRAUD Fraud investigator | R |
| RW-DEBTSALE Debt sale officer | R |
| RW-WRITEOFF Write-off team member | CRU |
| RW-CREDITAD Credit Administration officer | CRUA |
| RW-CONDUCT Conduct and QA officer | R |
| RW-PRODHEAD Product head (Mortgage, HP, SSME) | RA |
| RW-WOCOMM Write-off committee member | RA |
| RW-RISK Risk and model risk officer | R |
| RW-COE Center of excellence analyst | R |
| RW-FINANCE Finance and CFO delegate | RA |
| RW-AUDIT Internal audit | R |
| RW-BIANAL Reporting and BI analyst | R |
| RW-TRIBE Tribe lead and squad members | R |
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
| REQ-S7-001 | FEAT-WOF-01 | Written one epic ahead | With the story |
| REQ-S7-002 | FEAT-WOF-01 | Written one epic ahead | With the story |
| REQ-S7-003 | FEAT-WOF-01 | Written one epic ahead | With the story |
| REQ-S7-004 | FEAT-WOF-01 | Written one epic ahead | With the story |
| REQ-S7-005 | FEAT-WOF-01 | Written one epic ahead | With the story |
| REQ-S7-006 | FEAT-WOF-01 | Written one epic ahead | With the story |
| REQ-S7-007 | FEAT-WOF-01 | Written one epic ahead | With the story |
| REQ-S7-008 | FEAT-WOF-01 | Written one epic ahead | With the story |

## Appendix T-A. API specification

### T-A.1 Endpoint inventory

| ID | Method | Path | Access | First in |
|---|---|---|---|---|
| API-S7-001 | POST | /api/recovery/writeoff/v1/write-off-scans | Write-off and posting C | E6 |
| API-S7-002 | POST | /api/recovery/writeoff/v1/write-offs/{writeOffId}/committee-decision | Write-off and posting A | E6 |

The operation IDs, paths and operationIds of these endpoints are published in `05 Technical architecture/Recovery Workbench API Specification v5/rwb-writeoff.yaml`; where an appendix row and the published operation differ, the published operation is the contract of T5.2.1 and the row keeps its ID for traceability (GAP-1997; ASM-3224).

### T-A.2 Endpoint detail

#### API-S7-001 POST /write-off-scans

| Item | Value |
|---|---|
| Purpose | Run the monthly write-off scan for a cut-off date |
| Request | ScanRequest |
| Response | WriteOffScan |
| Errors | 401, 403, 409, 422, 503 |
| Authorization | Write-off and posting, right C, scope applied |
| Idempotency | Idempotency-Key header |

#### API-S7-002 POST /write-offs/{writeOffId}/committee-decision

| Item | Value |
|---|---|
| Purpose | Record the committee decision for a write-off |
| Request | CommitteeDecision |
| Response | DecisionLogEntry |
| Errors | 401, 403, 404, 409, 422, 503 |
| Authorization | Write-off and posting, right A, scope applied |
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
