SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

# Recovery Workbench S8 Deviation handling

Technical specification. SCB Collections and Recovery. Henka Group, 22 November 2026.

(C) Siam Commercial Bank and Henka Pte Ltd

## Document control

| Attribute | Value |
|---|---|
| Document title | TSD S8 Deviation handling |
| Document ID | S8-RWB-TSD-v3 |
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
| Recovery Workbench FSD S8 Deviation handling | FSD | Pair |
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

S8 Deviation handling is one of the 19 services of Architecture v5: `rwb-deviation` (service name Deviation, module S8, wave 2, service epic `RWB-SVC-S8`). Version 3 adds this section so that the specification is read as the specification of one service: its identity, what it owns, and the decoupling patterns that replace the monolith's in-process calls. Every owner is taken from Microservice Ownership Map v1 and every identifier from Template and Rules R4 (ADR-013, ADR-014).

S8 is the only service that can pause a case: it raises and clears the deviation that P3 listens for (Architecture v5 slide 15).

### T0.1 Service identity

| Item | Value |
|---|---|
| Module | S8 Deviation handling |
| Service | `rwb-deviation` (Deviation) |
| Service epic | `RWB-SVC-S8` |
| Wave | 2 |
| Schema | `rwb_deviation` |
| Database login | `rwb_deviation`: one login per service, with its own connection pool cap |
| REST base | `/api/recovery/deviation/v1` |
| Kafka topic | `rwb.deviation.events.v1`, with `.retry` and `.dlt` topics |
| Event names | `rwb.deviation.<Event>.v1`, CloudEvents 1.0 in binary mode, key `caseId` |
| Temporal | namespace `rwb-recovery`; task queue `rwb-deviation` |
| Java package | `th.co.scb.ace.workbench.recovery.deviation` |
| Edge | gateway-bff for the staff screens of this service |
| Contract artefacts | `05 Technical architecture/Recovery Workbench API Specification v5/rwb-deviation.yaml`; `05 Technical architecture/Recovery Workbench API Specification v5/asyncapi/rwb-deviation.asyncapi.yaml` |
| Suggested owner, app development | TechX (suggested; any team may pick up this story) |
| Suggested owner, ACE DB | ACE team (suggested; any team may pick up this story) |

### T0.2 What this service owns

Architecture v5 slide 41 gives this service: X1-X7 screening, pause, handling, return. Table T0.2 states the same ownership in the form the Ownership Map uses, with the counts this specification carries. A table that the map assigns to another service is not built here, whatever T3 says (see the note under T3).

| Area | Owner and artefact | Count |
|---|---|---|
| Business tables in `rwb_deviation` | `deviation` | 1 |
| REST operations | appendix T-A and `rwb-deviation.yaml` | 2 |
| Events published | EV-06 DeviationRaised, EV-07 DeviationCleared | 2 |
| Workflows and schedules | DeviationWorkflow | 1 |
| Jobs | none | 0 |

### T0.3 Decoupling patterns applied

The left column is the pattern of Template and Rules R5.5; the middle column quotes the line of this specification that carries the legacy marker, where one is present; the right column is what replaces it in this service.

| DP | Legacy marker in this specification | How the service lands it |
|---|---|---|
| DP-01 | — | Owns its tables in `rwb_deviation`; no other service reads them (ADR-014). |
| DP-02 | — | One login, `rwb_deviation`, with its own connection pool cap. |
| DP-03 | `…logic; calls the rules component; writes the decision log entry before any change` | Local decision record plus DecisionRecorded (EV-08) on `rwb.decision-record.v1`. |
| DP-07 | `DF-CAS-038 / deviation_code / LOV / varchar(3) / Yes / LOV-DEVIATION / Workbench` | Reference data and lists of values from the `rwb-case` contract (H RWB-PLT-E1043-CON). |
| DP-08 | `RW-CASEOWN Case owner / CRU` | Authorisation through the `rwb-access` authorise contract and the guard library (H RWB-PLT-E1037-CON). |
| DP-09 | — | Outbox and inbox library; CloudEvents on `rwb.deviation.events.v1` with retry topics and `.dlt`. |
| DP-10 | `Scheduler and batch / REUSE / ACE pattern: Quartz and Spring Batch / Jobs in the Batch and…` | Temporal Schedules and event-started workflows through the workflow kit (ADR-016). |
| DP-11 | `…reaches other modules only through their published interfaces and other systems only through COLLINS,…` | One REST hop, 2 s timeout, breaker; the consumer builds against the provider's fake (ADR-020). |
| DP-13 | `API-S8-001 / POST / /api/recovery/v1/cases/{caseId}/deviations / Case record…` | REST base `/api/recovery/deviation/v1`. |
| DP-14 | — | Topic `rwb.deviation.events.v1`, retry topics and `.dlt`; naming library (H RWB-PLT-E1047-CON). |
| DP-15 | — | Per-service Flyway sequence in `rwb_deviation`. |
| DP-19 | `…repository, one front end. It covers: x1 to X7: screening, pause, handling, return. It reaches…` | Screens composed by gateway-bff; one composite route per screen (H RWB-PLT-N001-CON). |

### T0.4 What this service is not

- It holds no other service's table and no ACE table beyond the read-only `recovery.v_ace_*` views (DP-01, DP-05).
- It runs no shared Quartz job and touches no ACE batch table (DP-10; ADR-016).
- It does not stop a case by writing case state: it raises the deviation event that P3 acts on (EV-06).
- It is not a monolith module: the published Java interface of T2 is replaced by the contract set of T5.2 (DP-11; ADR-020).

## T1. Architecture overview

S8 Deviation handling is delivered as the service `rwb-deviation` (module S8, wave 2, service epic `RWB-SVC-S8`): one repository, one pipeline, one schema `rwb_deviation` with one login, behind gateway-bff (ADR-013, ADR-014). It covers: x1 to X7: screening, pause, handling, return. It reaches other modules only through the contracts of T5.2 and other systems only through COLLINS, file loads and the ACE paths.

## T2. Component design

| Component | Responsibility |
|---|---|
| DeviationHandlingController | REST endpoints in appendix T-A; validation; maps errors to problem responses |
| DeviationHandlingService | Business logic; calls the rules component; writes the decision log entry before any change |
| DeviationHandlingRepository | Reads and writes the module's tables only |
| Jobs | Temporal Schedules and event-started workflows this service owns (T0.2, T5.2.1; DP-10) |
| Published interface | The contracts of T5.2: REST operations, events and workflows other services call; no table is read across modules (DP-11) |

The published interface of this table is the contract set of T5.2: the REST operations, the events and the workflows, not a Java interface in a shared classpath (DP-11; ADR-020). Components that the Ownership Map places in another service are stated in T0.2 and T5.2 and are built by that service.

## T3. Data model

Every object of T3 that Microservice Ownership Map v1 assigns to `rwb-deviation` lives in schema `rwb_deviation` with the standard columns of T3.0 (DP-01, DP-15; ADR-014). `deviation` is this service's table; X1 to X7 screening reads the party flags through the P1 contract and keeps no copy (DP-05).

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

**deviation** (NEW). A deviation X1 to X7 raised on a case.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-CAS-036 | id | TEXT | uuid | Yes | None | Workbench |
| DF-CAS-037 | case_id | CROSS_REF | uuid | Yes | None | Workbench |
| DF-CAS-038 | deviation_code | LOV | varchar(3) | Yes | LOV-DEVIATION | Workbench |
| DF-CAS-039 | raised_at | DATE | timestamptz | Yes | None | Workbench |
| DF-CAS-040 | raised_by | LOV | varchar(20) | Yes | LOV-RAISED-BY | Workbench |
| DF-CAS-041 | paused_state | TEXT | varchar(60) | Yes | None | Workbench |
| DF-CAS-042 | handler_user_id | USER_REF | uuid | No | None | Workbench |
| DF-CAS-043 | contact_stop | BOOLEAN | boolean | Yes | None | Workbench |
| DF-CAS-044 | cleared_at | DATE | timestamptz | No | None | Workbench |
| DF-CAS-045 | outcome | LOV | varchar(20) | No | LOV-DEV-OUTCOME | Workbench |

### T3.2 Lists of values

| List | Values |
|---|---|
| LOV-DEV-OUTCOME | RETURNED, RE_ROUTED, CASE_ENDED |
| LOV-DEVIATION | X1, X2, X3, X4, X5, X6, X7 |
| LOV-RAISED-BY | SCREENING_AGENT, RULE, OFFICER, CUSTOMER_CONTACT |

### T3.3 Relationships

| From | To | Field | Cardinality |
|---|---|---|---|
| deviation | case_id | recovery_case | Many to 1 |

## T4. State machines and workflow

**DEVIATION.** 22 rules over 9 states. The full table is in the Business Rules and Routing Logic workbook.

| Rule | From | Event | To |
|---|---|---|---|
| R-DEV-01 | ANY_STATE | DEVIATION_FLAGGED | DEV_FLAGGED |
| R-DEV-02 | DEV_FLAGGED | OWNER_ASSIGNED | DEV_WITH_OWNER |
| R-DEV-03 | DEV_FLAGGED | OWNER_ASSIGNED | DEV_WITH_OWNER |
| R-DEV-04 | DEV_FLAGGED | OWNER_ASSIGNED | DEV_WITH_OWNER |
| R-DEV-05 | DEV_FLAGGED | OWNER_ASSIGNED | DEV_WITH_OWNER |
| R-DEV-06 | DEV_FLAGGED | OWNER_ASSIGNED | DEV_WITH_OWNER |
| R-DEV-07 | DEV_FLAGGED | FLAG_REJECTED | DEV_REJECTED |
| R-DEV-08 | DEV_REJECTED | CLOCK_RESUMED | RESUMED |
| R-DEV-09 | DEV_WITH_OWNER | DEVIATION_RESOLVED | DEV_RESOLVED |
| R-DEV-10 | DEV_WITH_OWNER | DEVIATION_RESOLVED | DEV_REROUTE |
| R-DEV-11 | DEV_WITH_OWNER | INSURANCE_SETTLED | CASE_ENDED |
| R-DEV-12 | DEV_WITH_OWNER | ESTATE_CONFIRMED | DEV_REROUTE |
| R-DEV-13 | DEV_WITH_OWNER | FRAUD_CONFIRMED | DEV_REROUTE |
| R-DEV-14 | DEV_WITH_OWNER | FRAUD_NOT_CONFIRMED | DEV_REROUTE |
| R-DEV-15 | DEV_WITH_OWNER | BANKRUPTCY_FILED | DEV_REROUTE |
| R-DEV-16 | DEV_WITH_OWNER | CONTACT_RESTORED | DEV_RESOLVED |
| R-DEV-17 | DEV_WITH_OWNER | CONTACT_NOT_FOUND | DEV_REROUTE |
| R-DEV-18 | DEV_RESOLVED | CLOCK_RESUMED | RESUMED |
| R-DEV-19 | DEV_REROUTE | ROUTE_REOPENED | ROUTE_D6 |
| R-DEV-20 | DEV_WITH_OWNER | SLA_BREACHED | DEV_WITH_OWNER |
| R-DEV-21 | DEV_FLAGGED | OWNER_ASSIGNED | DEV_WITH_OWNER |
| R-DEV-22 | DEV_WITH_OWNER | DEVIATION_RESOLVED | DEV_REROUTE |

## T5. Integration and interfaces

### T5.1 External system interfaces

| ID | System | Direction | Approach | Frequency |
|---|---|---|---|---|
| None | | | | |

### T5.2 Contracts

Version 3 states every cross-module dependency of this module as a contract, so that the service is built against a published artefact and its fake (ADR-020; DP-11). The artefact per call type is: OpenAPI 3.1 for REST, AsyncAPI 3.0 for Kafka, the Temporal interface named here for a workflow or activity, the Interface Specifications manifest for a file, the Nexus operation for the ACE restructure calculator, and a grant on the view for SQL. No row of this section reads another service's table (DP-01). Every consumed contract is class C (Template and Rules R5.4): it never blocks the build, because the consumer builds against the fake, and the real cross-service behaviour is class I work on an integration story. Architecture v5 slides 13 to 20 name a few operations differently from the published files of 22 November 2026; the published file is the artefact the fake is generated from and is the one cited here (GAP-1997; ASM-3224).

#### T5.2.1 Contracts provided

The REST operations of this service are published in `05 Technical architecture/Recovery Workbench API Specification v5/rwb-deviation.yaml` (5.0.0, 22 November 2026) under the base `/api/recovery/deviation/v1`. Appendix T-A holds the endpoint IDs, the access right and the first release of each one.

| # | Method | Path | operationId |
|---|---|---|---|
| 1 | POST | `/cases/{caseId}/deviations` | `postCasesCaseidDeviations` |
| 2 | PATCH | `/deviations/{deviationId}` | `patchDeviationsDeviationid` |

Workflows, schedules, files and views this service provides:

| Contract | Type | Called by or target | Note |
|---|---|---|---|
| DeviationWorkflow (child of the case) | Temporal workflow | S8 rwb-deviation | Started by P3 rwb-case |

Events this service publishes (AsyncAPI 3.0, CloudEvents 1.0):

| Event | EV | Topic | Consumers |
|---|---|---|---|
| DeviationRaised | EV-06 | `rwb.deviation.events.v1` | rwb-case, rwb-comms, rwb-treatment |
| DeviationCleared | EV-07 | `rwb.deviation.events.v1` | rwb-case, rwb-comms |

#### T5.2.2 Contracts consumed

| Contract | Type | Provider | Class | Failure path |
|---|---|---|---|---|
| Party flags (deceased, bankrupt), read-only | REST | P1 rwb-source-data | C | 2 s timeout, breaker; built against the fake (ADR-020) |
| Agent run: screening | Temporal child workflow | P10 rwb-agent | C | Workflow retry policy; the caller keeps its state (DP-12) |

Events this service consumes:

| Event | EV | Provider topic | Provider | Class | Failure path |
|---|---|---|---|---|---|
| CaseCreated (screening) | EV-01 | `rwb.case.events.v1` | P3 rwb-case | C | Retry 1 min, 10 min, 1 h, then `.dlt`; inbox dedupe |
| AceDataReady | EV-26 | `rwb.source-data.events.v1` | P1 rwb-source-data | C | Retry 1 min, 10 min, 1 h, then `.dlt`; inbox dedupe |
| AgentRunCompleted | EV-28 | `rwb.agent.events.v1` | P10 rwb-agent | C | Retry 1 min, 10 min, 1 h, then `.dlt`; inbox dedupe |

#### T5.2.3 Call-type summary

| Call type | Provided | Consumed | Artefact |
|---|---|---|---|
| REST | 2 | 1 | OpenAPI 3.1, one file per service |
| Kafka (events) | 2 | 3 | AsyncAPI 3.0, one file per service |
| Temporal | 1 | 1 | Workflow and activity interfaces, queue `rwb-deviation` |
| File | 0 | 0 | Interface Specifications manifest and the SAS link |
| Nexus | 0 | 0 | Nexus operation into ACE |
| SQL | 0 | 0 | Read-only grant on the view |

A contract change is a new version of the artefact, never a code change in the consumer (ADR-020). The provider named in T5.2.2 is the owner in Microservice Ownership Map v1, and the consumer list of each event is the Arch v5 event catalogue on slides 42 and 43.

### T5.3 Events

The event contract of this service is `05 Technical architecture/Recovery Workbench API Specification v5/asyncapi/rwb-deviation.asyncapi.yaml`; the shared decision-record contract is `asyncapi/rwb.decision-record.v1.asyncapi.yaml`. Every service publishes DecisionRecorded (EV-08) to `rwb.decision-record.v1` from its outbox in the same transaction as its state change (DP-03, DP-09; ADR-015, ADR-022); consuming services dedupe through their inbox table. Events carry identifiers and facts, never personal data (Event and Messaging Design v4, sheet Rules).

| Event | EV | Direction | Topic |
|---|---|---|---|
| DeviationRaised | EV-06 | Published | `rwb.deviation.events.v1` |
| DeviationCleared | EV-07 | Published | `rwb.deviation.events.v1` |
| CaseCreated (screening) | EV-01 | Consumed | `rwb.case.events.v1` |
| AceDataReady | EV-26 | Consumed | `rwb.source-data.events.v1` |
| AgentRunCompleted | EV-28 | Consumed | `rwb.agent.events.v1` |

An event shown with `—` has no number in the numbered catalogue: the Arch v5 catalogue calls these rows `+`, so the number is not specified in the source documents (GAP-1996; ASM-3223).

## T6. Security and access control

### T6.1 RBAC matrix

| Role | Case record |
|---|---|
| RW-CASEOWN Case owner | CRU |
| RW-TEAMMGR Team manager | R |
| RW-PHONECOL Phone collector | R |
| RW-FIELDCOL Field collector | R |
| RW-RESTRUCT Restructuring officer (FCR) | RU |
| RW-SPECIAL Hardship and vulnerability specialist | RU |
| RW-COMPLAIN Complaint officer | RU |
| RW-FRAUD Fraud investigator | RU |
| RW-LITOFF Litigation officer | RU |
| RW-ENFORCE Enforcement owner | RU |
| RW-LEGAL Legal counsel | R |
| RW-SALEOFF Sale officer | RU |
| RW-NPAMGR NPA and asset manager | R |
| RW-DEBTSALE Debt sale officer | RU |
| RW-WRITEOFF Write-off team member | R |
| RW-CREDITAD Credit Administration officer | R |
| RW-GUARANT Guarantee officer | RU |
| RW-AGENCYMG Partner and agency manager | R |
| RW-CONDUCT Conduct and QA officer | R |
| RW-CAPACITY Capacity and workforce planner | R |
| RW-PRODHEAD Product head (Mortgage, HP, SSME) | R |
| RW-HEADLIT Head of Litigation | R |
| RW-HEADNPA Head of NPA | R |
| RW-HEADASL Head of Asset Liquidity | R |
| RW-CREDCOMM Credit approval committee member | R |
| RW-WOCOMM Write-off committee member | R |
| RW-RISK Risk and model risk officer | R |
| RW-COE Center of excellence analyst | R |
| RW-DATASTEW Data steward and data product owner | R |
| RW-FINANCE Finance and CFO delegate | R |
| RW-AUDIT Internal audit | R |
| RW-COMPLY Compliance and PDPA officer | R |
| RW-PLATADM Platform administrator | R |
| RW-BIANAL Reporting and BI analyst | R |
| RW-TRIBE Tribe lead and squad members | R |
| PT-AGENCY Collection agency (OA) user | R |
| PT-LAWFIRM Law firm user | R |
| SY-CASEWF Case workflow module | CRU |
| SY-RULES Rules component | R |
| SY-DATALOAD Data load from COLLINS | CU |
| SY-OCR OCR and extraction pipeline | R |
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
| REQ-DVH-001 | FEAT-DVH-01 | RWB-E1-062 | TC-E1-062-01 |
| REQ-DVH-002 | FEAT-DVH-01 | RWB-E1-062 | TC-E1-062-01 |
| REQ-DVH-003 | FEAT-DVH-01 | RWB-E1-062 | TC-E1-062-01 |
| REQ-DVH-004 | FEAT-DVH-01 | RWB-E1-062 | TC-E1-062-01 |
| REQ-DVH-005 | FEAT-DVH-01 | RWB-E1-062 | TC-E1-062-01 |
| REQ-DVH-006 | FEAT-DVH-01 | RWB-E1-062 | TC-E1-062-01 |
| REQ-DVH-007 | FEAT-DVH-01 | RWB-E1-062 | TC-E1-062-01 |
| REQ-DVH-008 | None | Written one epic ahead | With the story |
| REQ-DVH-009 | FEAT-DVH-01 | RWB-E1-062 | TC-E1-062-01 |
| REQ-DVH-010 | FEAT-DVH-01 | RWB-E1-062 | TC-E1-062-01 |
| REQ-DVH-011 | FEAT-DVF-01 | Written one epic ahead | With the story |
| REQ-S8-001 | FEAT-DVF-01 | Written one epic ahead | With the story |
| REQ-S8-002 | FEAT-DVF-01 | Written one epic ahead | With the story |
| REQ-S8-003 | FEAT-DVF-01 | Written one epic ahead | With the story |
| REQ-S8-004 | FEAT-DVF-01 | Written one epic ahead | With the story |
| REQ-S8-005 | FEAT-DVF-01 | Written one epic ahead | With the story |
| REQ-S8-006 | FEAT-DVF-01 | Written one epic ahead | With the story |
| REQ-S8-007 | FEAT-DVF-01 | Written one epic ahead | With the story |

## Appendix T-A. API specification

### T-A.1 Endpoint inventory

| ID | Method | Path | Access | First in |
|---|---|---|---|---|
| API-S8-001 | POST | /api/recovery/deviation/v1/cases/{caseId}/deviations | Case record U | E2 |
| API-S8-002 | PATCH | /api/recovery/deviation/v1/deviations/{deviationId} | Case record U | E2 |

The operation IDs, paths and operationIds of these endpoints are published in `05 Technical architecture/Recovery Workbench API Specification v5/rwb-deviation.yaml`; where an appendix row and the published operation differ, the published operation is the contract of T5.2.1 and the row keeps its ID for traceability (GAP-1997; ASM-3224).

### T-A.2 Endpoint detail

#### API-S8-001 POST /cases/{caseId}/deviations

| Item | Value |
|---|---|
| Purpose | Raise a deviation X1 to X7 on the case |
| Request | DeviationRequest |
| Response | Deviation |
| Errors | 401, 403, 404, 409, 422, 503 |
| Authorization | Case record, right U, scope applied |
| Idempotency | Idempotency-Key header |

#### API-S8-002 PATCH /deviations/{deviationId}

| Item | Value |
|---|---|
| Purpose | Record the outcome of a deviation and return or re-route the case |
| Request | DeviationOutcome |
| Response | Deviation |
| Errors | 401, 403, 404, 409, 422, 503 |
| Authorization | Case record, right U, scope applied |
| Idempotency | Not applicable |

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
