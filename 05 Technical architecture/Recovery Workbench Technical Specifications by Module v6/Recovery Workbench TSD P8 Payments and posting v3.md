SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

# Recovery Workbench P8 Payments and posting

Technical specification. SCB Collections and Recovery. Henka Group, 22 November 2026.

(C) Siam Commercial Bank and Henka Pte Ltd

## Document control

| Attribute | Value |
|---|---|
| Document title | TSD P8 Payments and posting |
| Document ID | P8-RWB-TSD-v3 |
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
| Recovery Workbench FSD P8 Payments and posting | FSD | Pair |
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

P8 Payments and posting is one of the 19 services of Architecture v5: `rwb-payment` (service name Payment, module P8, wave 2, service epic `RWB-SVC-P8`). Version 3 adds this section so that the specification is read as the specification of one service: its identity, what it owns, and the decoupling patterns that replace the monolith's in-process calls. Every owner is taken from Microservice Ownership Map v1 and every identifier from Template and Rules R4 (ADR-013, ADR-014).

P8 is the only writer of proceeds and bookings; other services reach it through the postProceeds activity, never through its tables (DP-01, DP-11).

### T0.1 Service identity

| Item | Value |
|---|---|
| Module | P8 Payments and posting |
| Service | `rwb-payment` (Payment) |
| Service epic | `RWB-SVC-P8` |
| Wave | 2 |
| Schema | `rwb_payment` |
| Database login | `rwb_payment`: one login per service, with its own connection pool cap |
| REST base | `/api/recovery/payment/v1` |
| Kafka topic | `rwb.payment.events.v1`, with `.retry` and `.dlt` topics |
| Event names | `rwb.payment.<Event>.v1`, CloudEvents 1.0 in binary mode, key `caseId` |
| Temporal | namespace `rwb-recovery`; task queue `rwb-payment` |
| Java package | `th.co.scb.ace.workbench.recovery.payment` |
| Edge | gateway-bff for the staff screens of this service |
| Contract artefacts | `05 Technical architecture/Recovery Workbench API Specification v5/rwb-payment.yaml`; `05 Technical architecture/Recovery Workbench API Specification v5/asyncapi/rwb-payment.asyncapi.yaml` |
| Suggested owner, app development | TechX (suggested; any team may pick up this story) |
| Suggested owner, ACE DB | ACE team (suggested; any team may pick up this story) |

### T0.2 What this service owns

Architecture v5 slide 41 gives this service: payment and proceeds matching, fees, bookings, posting files. Table T0.2 states the same ownership in the form the Ownership Map uses, with the counts this specification carries. A table that the map assigns to another service is not built here, whatever T3 says (see the note under T3).

| Area | Owner and artefact | Count |
|---|---|---|
| Business tables in `rwb_payment` | `proceeds` | 1 |
| REST operations | appendix T-A and `rwb-payment.yaml` | 2 |
| Events published | EV-11 TreatmentBooked, EV-12 PaymentMissed, EV-25 ProceedsMatched | 3 |
| Workflows and schedules | none in the Ownership Map sheet; T5.2.1 names matchPayments, confirmBookings, postProceeds (saga step) | 2 |
| Jobs | JOB-07, JOB-08 | 2 |

### T0.3 Decoupling patterns applied

The left column is the pattern of Template and Rules R5.5; the middle column quotes the line of this specification that carries the legacy marker, where one is present; the right column is what replaces it in this service.

| DP | Legacy marker in this specification | How the service lands it |
|---|---|---|
| DP-01 | — | Owns its tables in `rwb_payment`; no other service reads them (ADR-014). |
| DP-02 | — | One login, `rwb_payment`, with its own connection pool cap. |
| DP-03 | `…on events from P3 and writes through the decision log.` | Local decision record plus DecisionRecorded (EV-08) on `rwb.decision-record.v1`. |
| DP-07 | `DF-FIN-005 / source / LOV / varchar(12) / Yes / LOV-PROCEEDS-SRC…` | Reference data and lists of values from the `rwb-case` contract (H RWB-PLT-E1043-CON). |
| DP-08 | `RW-FRAUD Fraud investigator / R` | Authorisation through the `rwb-access` authorise contract and the guard library (H RWB-PLT-E1037-CON). |
| DP-09 | `…state machine of its own; the module acts on events from P3 and writes through the decision…` | Outbox and inbox library; CloudEvents on `rwb.payment.events.v1` with retry topics and `.dlt`. |
| DP-10 | `Scheduler and batch / REUSE / ACE pattern: Quartz and Spring Batch / Jobs in the Batch and…` | Temporal Schedules and event-started workflows through the workflow kit (ADR-016). |
| DP-11 | `…reaches other modules only through their published interfaces and other systems only through COLLINS,…` | One REST hop, 2 s timeout, breaker; the consumer builds against the provider's fake (ADR-020). |
| DP-13 | `API-P8-001 / GET / /api/recovery/v1/proceeds / Write-off and posting R / E2` | REST base `/api/recovery/payment/v1`. |
| DP-14 | — | Topic `rwb.payment.events.v1`, retry topics and `.dlt`; naming library (H RWB-PLT-E1047-CON). |
| DP-15 | — | Per-service Flyway sequence in `rwb_payment`. |

### T0.4 What this service is not

- It holds no other service's table and no ACE table beyond the read-only `recovery.v_ace_*` views (DP-01, DP-05).
- It runs no shared Quartz job and touches no ACE batch table (DP-10; ADR-016).
- It holds no matching rule: the match rules are a rule package of rwb-decision (DP-04; ASM-3221).
- It is not a monolith module: the published Java interface of T2 is replaced by the contract set of T5.2 (DP-11; ADR-020).

## T1. Architecture overview

P8 Payments and posting is delivered as the service `rwb-payment` (module P8, wave 2, service epic `RWB-SVC-P8`): one repository, one pipeline, one schema `rwb_payment` with one login, behind gateway-bff (ADR-013, ADR-014). It covers: payment and proceeds matching, fees, posting files. It reaches other modules only through the contracts of T5.2 and other systems only through COLLINS, file loads and the ACE paths.

## T2. Component design

| Component | Responsibility |
|---|---|
| PaymentsAndPostingController | REST endpoints in appendix T-A; validation; maps errors to problem responses |
| PaymentsAndPostingService | Business logic; calls the rules component; writes the decision log entry before any change |
| PaymentsAndPostingRepository | Reads and writes the module's tables only |
| Jobs | Temporal Schedules and event-started workflows this service owns (T0.2, T5.2.1; DP-10) |
| Published interface | The contracts of T5.2: REST operations, events and workflows other services call; no table is read across modules (DP-11) |

The published interface of this table is the contract set of T5.2: the REST operations, the events and the workflows, not a Java interface in a shared classpath (DP-11; ADR-020). Components that the Ownership Map places in another service are stated in T0.2 and T5.2 and are built by that service.

## T3. Data model

Every object of T3 that Microservice Ownership Map v1 assigns to `rwb-payment` lives in schema `rwb_payment` with the standard columns of T3.0 (DP-01, DP-15; ADR-014). `proceeds` is this service's table. `payment_match_rule`, which T3.1 lists, has no row in the Ownership Map Tables sheet; the match rules become the PAYMENT_MATCH rule package of rwb-decision (TSD P3 T2.2), so P8 keeps the proceeds rows and no rule table (GAP-1994; ASM-3221).

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

**proceeds** (NEW). Money received on a case and what it was matched to.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-FIN-001 | id | TEXT | uuid | Yes | None | Workbench |
| DF-FIN-002 | case_id | CROSS_REF | uuid | Yes | None | Workbench |
| DF-FIN-003 | treatment_id | CROSS_REF | uuid | No | None | Workbench |
| DF-FIN-004 | account_payment_id | CROSS_REF | uuid | No | None | Workbench |
| DF-FIN-005 | source | LOV | varchar(12) | Yes | LOV-PROCEEDS-SRC | Workbench |
| DF-FIN-006 | amount | NUMBER | numeric(18,2) | Yes | None | Core bank (ALS) via COLLINS |
| DF-FIN-007 | received_date | DATE | date | Yes | None | Core bank (ALS) via COLLINS |
| DF-FIN-008 | matched_to | LOV | varchar(15) | Yes | LOV-MATCH | Workbench |
| DF-FIN-009 | posting_ref | TEXT | varchar(40) | No | None | Core bank (ALS) via COLLINS |

**payment_match_rule** (NEW). A rule for matching a payment to a plan installment, by version.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-REF-261 | id | TEXT | uuid | Yes | None | Workbench |
| DF-REF-262 | rule_code | TEXT | varchar(20) | Yes | None | Workbench |
| DF-REF-263 | rule_version | TEXT | varchar(20) | Yes | None | Workbench |
| DF-REF-264 | match_type | LOV | varchar(15) | Yes | LOV-MATCH-TYPE | Workbench |
| DF-REF-265 | amount_tolerance_pct | NUMBER | numeric(5,2) | Yes | None | Workbench |
| DF-REF-266 | window_days_before | NUMBER | integer | Yes | None | Workbench |
| DF-REF-267 | window_days_after | NUMBER | integer | Yes | None | Workbench |
| DF-REF-268 | grace_days | NUMBER | integer | Yes | None | Workbench |
| DF-REF-269 | partial_floor_pct | NUMBER | numeric(5,2) | No | None | Workbench |
| DF-REF-270 | priority | NUMBER | integer | Yes | None | Workbench |
| DF-REF-271 | valid_from | DATE | date | Yes | None | Workbench |
| DF-REF-272 | valid_to | DATE | date | No | None | Workbench |
| DF-REF-273 | approved_by | USER_REF | uuid | No | None | Workbench |

### T3.2 Lists of values

| List | Values |
|---|---|
| LOV-MATCH | INSTALLMENT, SETTLEMENT, FEE, SALE_PROCEEDS, UNMATCHED |
| LOV-MATCH-TYPE | EXACT, WINDOW, PARTIAL |
| LOV-PROCEEDS-SRC | CUSTOMER, LED, AUCTION, BUYER, AGENCY, INSURER, GUARANTOR |

### T3.3 Relationships

| From | To | Field | Cardinality |
|---|---|---|---|
| proceeds | case_id | recovery_case | Many to 1 |
| proceeds | treatment_id | treatment | Many to 0 or 1 |
| proceeds | account_payment_id | account_payment | Many to 0 or 1 |

## T4. State machines and workflow

No case state machine of its own; the module acts on events from P3 and writes through the decision log.

## T5. Integration and interfaces

### T5.1 External system interfaces

| ID | System | Direction | Approach | Frequency |
|---|---|---|---|---|
| INT-02 | Core bank (ALS) | In | COLLINS batch | Daily, end of day |
| INT-03 | Core bank (ALS) | Out | Booked by the officer; confirmed on the next day's load | As approved |
| INT-16 | GL | In | File load | Monthly |

### T5.2 Contracts

Version 3 states every cross-module dependency of this module as a contract, so that the service is built against a published artefact and its fake (ADR-020; DP-11). The artefact per call type is: OpenAPI 3.1 for REST, AsyncAPI 3.0 for Kafka, the Temporal interface named here for a workflow or activity, the Interface Specifications manifest for a file, the Nexus operation for the ACE restructure calculator, and a grant on the view for SQL. No row of this section reads another service's table (DP-01). Every consumed contract is class C (Template and Rules R5.4): it never blocks the build, because the consumer builds against the fake, and the real cross-service behaviour is class I work on an integration story. Architecture v5 slides 13 to 20 name a few operations differently from the published files of 22 November 2026; the published file is the artefact the fake is generated from and is the one cited here (GAP-1997; ASM-3224).

#### T5.2.1 Contracts provided

The REST operations of this service are published in `05 Technical architecture/Recovery Workbench API Specification v5/rwb-payment.yaml` (5.0.0, 22 November 2026) under the base `/api/recovery/payment/v1`. Appendix T-A holds the endpoint IDs, the access right and the first release of each one.

| # | Method | Path | operationId |
|---|---|---|---|
| 1 | GET | `/proceeds` | `getProceeds` |
| 2 | POST | `/proceeds/{proceedsId}/match` | `postProceedsProceedsidMatch` |

Workflows, schedules, files and views this service provides:

| Contract | Type | Called by or target | Note |
|---|---|---|---|
| matchPayments, confirmBookings | Temporal activity | P8 rwb-payment | JOB-07 and JOB-08 as event-started workflows |
| postProceeds (saga step) | Temporal activity | P8 rwb-payment | Called by S2, S5, S6 and S7 |

Events this service publishes (AsyncAPI 3.0, CloudEvents 1.0):

| Event | EV | Topic | Consumers |
|---|---|---|---|
| TreatmentBooked | EV-11 | `rwb.payment.events.v1` | rwb-case, rwb-treatment |
| PaymentMissed | EV-12 | `rwb.payment.events.v1` | rwb-case, rwb-treatment, rwb-comms |
| ProceedsMatched | EV-25 | `rwb.payment.events.v1` | rwb-case, rwb-asset, rwb-debtsale, rwb-writeoff, rwb-guarantee |

#### T5.2.2 Contracts consumed

| Contract | Type | Provider | Class | Failure path |
|---|---|---|---|---|
| payments for the business date | Temporal activity | P1 rwb-source-data | C | Workflow retry policy; the caller keeps its state (DP-12) |
| deliverFile(manifest) for the posting file | Temporal activity | P2 rwb-integration | C | Workflow retry policy; the caller keeps its state (DP-12) |

Events this service consumes:

| Event | EV | Provider topic | Provider | Class | Failure path |
|---|---|---|---|---|---|
| AceDataReady | EV-26 | `rwb.source-data.events.v1` | P1 rwb-source-data | C | Retry 1 min, 10 min, 1 h, then `.dlt`; inbox dedupe |
| TreatmentApproved | EV-10 | `rwb.treatment.events.v1` | S2 rwb-treatment | C | Retry 1 min, 10 min, 1 h, then `.dlt`; inbox dedupe |
| LotAwarded | EV-23 | `rwb.debtsale.events.v1` | S6 rwb-debtsale | C | Retry 1 min, 10 min, 1 h, then `.dlt`; inbox dedupe |
| AssetSold | — | `rwb.asset.events.v1` | S5 rwb-asset | C | Retry 1 min, 10 min, 1 h, then `.dlt`; inbox dedupe |
| WriteOffApproved | EV-24 | `rwb.writeoff.events.v1` | S7 rwb-writeoff | C | Retry 1 min, 10 min, 1 h, then `.dlt`; inbox dedupe |

#### T5.2.3 Call-type summary

| Call type | Provided | Consumed | Artefact |
|---|---|---|---|
| REST | 2 | 0 | OpenAPI 3.1, one file per service |
| Kafka (events) | 3 | 5 | AsyncAPI 3.0, one file per service |
| Temporal | 2 | 2 | Workflow and activity interfaces, queue `rwb-payment` |
| File | 0 | 0 | Interface Specifications manifest and the SAS link |
| Nexus | 0 | 0 | Nexus operation into ACE |
| SQL | 0 | 0 | Read-only grant on the view |

A contract change is a new version of the artefact, never a code change in the consumer (ADR-020). The provider named in T5.2.2 is the owner in Microservice Ownership Map v1, and the consumer list of each event is the Arch v5 event catalogue on slides 42 and 43.

### T5.3 Events

The event contract of this service is `05 Technical architecture/Recovery Workbench API Specification v5/asyncapi/rwb-payment.asyncapi.yaml`; the shared decision-record contract is `asyncapi/rwb.decision-record.v1.asyncapi.yaml`. Every service publishes DecisionRecorded (EV-08) to `rwb.decision-record.v1` from its outbox in the same transaction as its state change (DP-03, DP-09; ADR-015, ADR-022); consuming services dedupe through their inbox table. Events carry identifiers and facts, never personal data (Event and Messaging Design v4, sheet Rules).

| Event | EV | Direction | Topic |
|---|---|---|---|
| TreatmentBooked | EV-11 | Published | `rwb.payment.events.v1` |
| PaymentMissed | EV-12 | Published | `rwb.payment.events.v1` |
| ProceedsMatched | EV-25 | Published | `rwb.payment.events.v1` |
| AceDataReady | EV-26 | Consumed | `rwb.source-data.events.v1` |
| TreatmentApproved | EV-10 | Consumed | `rwb.treatment.events.v1` |
| LotAwarded | EV-23 | Consumed | `rwb.debtsale.events.v1` |
| AssetSold | — | Consumed | `rwb.asset.events.v1` |
| WriteOffApproved | EV-24 | Consumed | `rwb.writeoff.events.v1` |

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

## Appendix T-A. API specification

### T-A.1 Endpoint inventory

| ID | Method | Path | Access | First in |
|---|---|---|---|---|
| API-P8-001 | GET | /api/recovery/payment/v1/proceeds | Write-off and posting R | E2 |
| API-P8-002 | POST | /api/recovery/payment/v1/proceeds/{proceedsId}/match | Write-off and posting U | E4 |

The operation IDs, paths and operationIds of these endpoints are published in `05 Technical architecture/Recovery Workbench API Specification v5/rwb-payment.yaml`; where an appendix row and the published operation differ, the published operation is the contract of T5.2.1 and the row keeps its ID for traceability (GAP-1997; ASM-3224).

### T-A.2 Endpoint detail

#### API-P8-001 GET /proceeds

| Item | Value |
|---|---|
| Purpose | List receipts with their match status |
| Request | Query: matched, from, to, page, size |
| Response | ProceedsPage |
| Errors | 401, 403, 503 |
| Authorization | Write-off and posting, right R, scope applied |
| Idempotency | Not applicable |

#### API-P8-002 POST /proceeds/{proceedsId}/match

| Item | Value |
|---|---|
| Purpose | Match a receipt to a case and account |
| Request | MatchRequest |
| Response | Proceeds |
| Errors | 401, 403, 404, 409, 422, 503 |
| Authorization | Write-off and posting, right U, scope applied |
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
