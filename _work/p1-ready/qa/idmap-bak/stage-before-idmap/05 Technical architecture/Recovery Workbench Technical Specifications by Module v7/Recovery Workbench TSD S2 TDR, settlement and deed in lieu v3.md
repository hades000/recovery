SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

# Recovery Workbench S2 TDR, settlement and deed in lieu

Technical specification. SCB Collections and Recovery. Henka Group, 22 November 2026.

(C) Siam Commercial Bank and Henka Pte Ltd

## Document control

| Attribute | Value |
|---|---|
| Document title | TSD S2 TDR, settlement and deed in lieu |
| Document ID | S2-RWB-TSD-v3 |
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
| Recovery Workbench FSD S2 TDR, settlement and deed in lieu | FSD | Pair |
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

S2 TDR, settlement and deed in lieu is one of the 19 services of Architecture v5: `rwb-treatment` (service name Treatment and offer, module S2, wave 2, service epic `RWB-SVC-S2`). Version 3 adds this section so that the specification is read as the specification of one service: its identity, what it owns, and the decoupling patterns that replace the monolith's in-process calls. Every owner is taken from Microservice Ownership Map v1 and every identifier from Template and Rules R4 (ADR-013, ADR-014).

S2 is the pivot of the treatment saga: booking through P8, contract through P5, approval through P7, and the ACE restructure calculator through Nexus (Architecture v5 slide 18).

### T0.1 Service identity

| Item | Value |
|---|---|
| Module | S2 TDR, settlement and deed in lieu |
| Service | `rwb-treatment` (Treatment and offer) |
| Service epic | `RWB-SVC-S2` |
| Wave | 2 |
| Schema | `rwb_treatment` |
| Database login | `rwb_treatment`: one login per service, with its own connection pool cap |
| REST base | `/api/recovery/treatment/v1` |
| Kafka topic | `rwb.treatment.events.v1`, with `.retry` and `.dlt` topics |
| Event names | `rwb.treatment.<Event>.v1`, CloudEvents 1.0 in binary mode, key `caseId` |
| Temporal | namespace `rwb-recovery`; task queue `rwb-treatment` |
| Java package | `th.co.scb.ace.workbench.recovery.treatment` |
| Edge | gateway-bff for the staff screens of this service |
| Contract artefacts | `05 Technical architecture/Recovery Workbench API Specification v5/rwb-treatment.yaml`; `05 Technical architecture/Recovery Workbench API Specification v5/asyncapi/rwb-treatment.asyncapi.yaml` |
| Suggested owner, app development | TechX (suggested; any team may pick up this story) |
| Suggested owner, ACE DB | ACE team (suggested; any team may pick up this story) |

### T0.2 What this service owns

Architecture v5 slide 41 gives this service: treatments, contracts, settlement and deed-in-lieu agreements, plan timers. Table T0.2 states the same ownership in the form the Ownership Map uses, with the counts this specification carries. A table that the map assigns to another service is not built here, whatever T3 says (see the note under T3).

| Area | Owner and artefact | Count |
|---|---|---|
| Business tables in `rwb_treatment` | `treatment` | 1 |
| REST operations | appendix T-A and `rwb-treatment.yaml` | 4 |
| Events published | EV-10 TreatmentApproved, TreatmentClosed | 2 |
| Workflows and schedules | TreatmentWorkflow | 1 |
| Jobs | none | 0 |

### T0.3 Decoupling patterns applied

The left column is the pattern of Template and Rules R5.5; the middle column quotes the line of this specification that carries the legacy marker, where one is present; the right column is what replaces it in this service.

| DP | Legacy marker in this specification | How the service lands it |
|---|---|---|
| DP-01 | — | Owns its tables in `rwb_treatment`; no other service reads them (ADR-014). |
| DP-02 | — | One login, `rwb_treatment`, with its own connection pool cap. |
| DP-03 | `…logic; calls the rules component; writes the decision log entry before any change` | Local decision record plus DecisionRecorded (EV-08) on `rwb.decision-record.v1`. |
| DP-07 | `DF-TRT-004 / treatment_type / LOV / varchar(20) / Yes / LOV-TREATMENT / Workbench` | Reference data and lists of values from the `rwb-case` contract (H RWB-PLT-E1043-CON). |
| DP-08 | `RW-CASEOWN Case owner / CRU` | Authorisation through the `rwb-access` authorise contract and the guard library (H RWB-PLT-E1037-CON). |
| DP-09 | — | Outbox and inbox library; CloudEvents on `rwb.treatment.events.v1` with retry topics and `.dlt`. |
| DP-10 | `Scheduler and batch / REUSE / ACE pattern: Quartz and Spring Batch / Jobs in the Batch and…` | Temporal Schedules and event-started workflows through the workflow kit (ADR-016). |
| DP-11 | `…reaches other modules only through their published interfaces and other systems only through COLLINS,…` | One REST hop, 2 s timeout, breaker; the consumer builds against the provider's fake (ADR-020). |
| DP-13 | `API-S2-001 / POST / /api/recovery/v1/cases/{caseId}/treatments / Treatment and…` | REST base `/api/recovery/treatment/v1`. |
| DP-14 | — | Topic `rwb.treatment.events.v1`, retry topics and `.dlt`; naming library (H RWB-PLT-E1047-CON). |
| DP-15 | — | Per-service Flyway sequence in `rwb_treatment`. |

### T0.4 What this service is not

- It holds no other service's table and no ACE table beyond the read-only `recovery.v_ace_*` views (DP-01, DP-05).
- It runs no shared Quartz job and touches no ACE batch table (DP-10; ADR-016).
- It holds no contract document: P5 generates and seals it and S2 keeps the reference (DP-11).
- It is not a monolith module: the published Java interface of T2 is replaced by the contract set of T5.2 (DP-11; ADR-020).

## T1. Architecture overview

S2 TDR, settlement and deed in lieu is delivered as the service `rwb-treatment` (module S2, wave 2, service epic `RWB-SVC-S2`): one repository, one pipeline, one schema `rwb_treatment` with one login, behind gateway-bff (ADR-013, ADR-014). It covers: treatment record, contracts, booking, plan timers. It reaches other modules only through the contracts of T5.2 and other systems only through COLLINS, file loads and the ACE paths.

## T2. Component design

| Component | Responsibility |
|---|---|
| TdrSettlementAndDeedInLieuController | REST endpoints in appendix T-A; validation; maps errors to problem responses |
| TdrSettlementAndDeedInLieuService | Business logic; calls the rules component; writes the decision log entry before any change |
| TdrSettlementAndDeedInLieuRepository | Reads and writes the module's tables only |
| Jobs | Temporal Schedules and event-started workflows this service owns (T0.2, T5.2.1; DP-10) |
| Published interface | The contracts of T5.2: REST operations, events and workflows other services call; no table is read across modules (DP-11) |

The published interface of this table is the contract set of T5.2: the REST operations, the events and the workflows, not a Java interface in a shared classpath (DP-11; ADR-020). Components that the Ownership Map places in another service are stated in T0.2 and T5.2 and are built by that service.

## T3. Data model

Every object of T3 that Microservice Ownership Map v1 assigns to `rwb-treatment` lives in schema `rwb_treatment` with the standard columns of T3.0 (DP-01, DP-15; ADR-014). `treatment` is this service's table; the TDR plans are read from ACE and are not copied (DP-05).

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

**treatment** (NEW; TDR plans REUSE ACE TDRCalculation). A resolution put to the customer or carried out on the case, with its terms and outcome.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-TRT-001 | id | TEXT | uuid | Yes | None | Workbench |
| DF-TRT-002 | case_id | CROSS_REF | uuid | Yes | None | Workbench |
| DF-TRT-003 | decision_log_id | CROSS_REF | uuid | No | None | Workbench |
| DF-TRT-004 | treatment_type | LOV | varchar(20) | Yes | LOV-TREATMENT | Workbench |
| DF-TRT-005 | proposed_by | LOV | varchar(10) | Yes | LOV-PROPOSER | Workbench |
| DF-TRT-006 | proposed_at | DATE | timestamptz | Yes | None | Workbench |
| DF-TRT-007 | offer_amount | NUMBER | numeric(18,2) | No | None | Workbench |
| DF-TRT-008 | haircut_amount | NUMBER | numeric(18,2) | No | None | Workbench |
| DF-TRT-009 | installments | NUMBER | integer | No | None | ACE |
| DF-TRT-010 | valid_until | DATE | date | No | None | Workbench |
| DF-TRT-011 | approval_level | LOV | varchar(4) | No | LOV-APPROVAL-LEVEL | Workbench |
| DF-TRT-012 | booked_at | DATE | timestamptz | No | None | Core bank (ALS) via COLLINS |
| DF-TRT-013 | outcome | LOV | varchar(12) | No | LOV-TRT-OUTCOME | Workbench |
| DF-TRT-014 | outcome_at | DATE | timestamptz | No | None | Workbench |
| DF-TRT-023 | nleads_ref | TEXT | varchar(30) | No | None | NLEADS |
| DF-TRT-024 | credit_result | LOV | varchar(10) | No | LOV-CREDIT-RESULT | NLEADS |
| DF-TRT-025 | credit_result_reason | TEXT | varchar(1000) | No | None | NLEADS |
| DF-TRT-026 | credit_result_at | DATE | timestamptz | No | None | NLEADS |
| DF-TRT-027 | interest_rate | NUMBER | numeric(7,4) | No | None | Workbench |
| DF-TRT-028 | booking_difference | TEXT | jsonb | No | None | Workbench |
| DF-TRT-029 | first_due_date | DATE | date | No | None | Workbench |
| DF-TRT-030 | signature_status | LOV | varchar(12) | No | LOV-TRT-SIGNATURE | Workbench |
| DF-TRT-031 | installment_amount | NUMBER | numeric(18,2) | No | None | Workbench |
| DF-TRT-032 | installments_paid | NUMBER | integer | Yes | None | Workbench |
| DF-TRT-033 | installment_shortfall | NUMBER | numeric(18,2) | No | None | Workbench |

### T3.2 Lists of values

| List | Values |
|---|---|
| LOV-APPROVAL-LEVEL | L1, L2, L3, L4, L5, L6 |
| LOV-CREDIT-RESULT | APPROVED, REFUSED |
| LOV-PROPOSER | AGENT, RULE, PERSON |
| LOV-TREATMENT | RESTRUCTURE, SETTLEMENT, DEED_IN_LIEU, BUY_BACK, GUARANTEE_CLAIM, REPOSSESSION, AUCTION, DEBT_SALE, WRITE_OFF, RAMC_TRANSFER, RENTAL |
| LOV-TRT-OUTCOME | KEPT, BROKEN, COMPLETED, CANCELED, DECLINED |
| LOV-TRT-SIGNATURE | PENDING, SIGNED, NOT_SIGNED |

### T3.3 Relationships

| From | To | Field | Cardinality |
|---|---|---|---|
| treatment | case_id | recovery_case | Many to 1 |
| treatment | decision_log_id | decision_log_entry | Many to 0 or 1 |

## T4. State machines and workflow

**RESTRUCTURE.** 37 rules over 18 states. The full table is in the Business Rules and Routing Logic workbook.

| Rule | From | Event | To |
|---|---|---|---|
| R-RES-01 | ROUTE_APPROVED_RESTRUCTURE | ROUTE_APPROVED | PROPOSED_IN_COLLINS |
| R-RES-02 | PROPOSED_IN_COLLINS | RESTRUCTURE_PROPOSED | IN_FCR_QUEUE |
| R-RES-03 | PROPOSED_IN_COLLINS | NO_PROPOSAL_RETURNED | BACK_TO_ROUTE_DECISION |
| R-RES-04 | IN_FCR_QUEUE | CASE_PICKED_UP | WITH_FCR_OFFICER |
| R-RES-05 | IN_FCR_QUEUE | QUEUE_SLA_BREACHED | IN_FCR_QUEUE |
| R-RES-06 | WITH_FCR_OFFICER | AFFORDABILITY_REQUIRED | AFFORDABILITY_IN_ACE |
| R-RES-07 | AFFORDABILITY_IN_ACE | AFFORDABILITY_PASSED | WITH_FCR_OFFICER |
| R-RES-08 | AFFORDABILITY_IN_ACE | AFFORDABILITY_FAILED | BACK_TO_ROUTE_DECISION |
| R-RES-09 | WITH_FCR_OFFICER | OFFER_PREPARED | OFFER_WITH_CUSTOMER |
| R-RES-10 | WITH_FCR_OFFICER | OFFER_PREPARED | AWAITING_CREDIT_APPROVAL |
| R-RES-11 | AWAITING_CREDIT_APPROVAL | CREDIT_APPROVED | OFFER_WITH_CUSTOMER |
| R-RES-12 | AWAITING_CREDIT_APPROVAL | CREDIT_DECLINED | DECLINED_BY_CREDIT |
| R-RES-13 | AWAITING_CREDIT_APPROVAL | APPROVAL_SLA_BREACHED | AWAITING_CREDIT_APPROVAL |
| R-RES-14 | DECLINED_BY_CREDIT | DECLINE_RECORDED | BACK_TO_ROUTE_DECISION |
| R-RES-15 | OFFER_WITH_CUSTOMER | CUSTOMER_COUNTER_OFFERED | WITH_FCR_OFFICER |
| R-RES-16 | OFFER_WITH_CUSTOMER | CUSTOMER_SIGNED | WITH_OPS_BOOKING |
| R-RES-17 | OFFER_WITH_CUSTOMER | CUSTOMER_DECLINED | RETURNED_TO_COLLINS |
| R-RES-18 | OFFER_WITH_CUSTOMER | OFFER_EXPIRED | RETURNED_TO_COLLINS |
| R-RES-19 | OFFER_WITH_CUSTOMER | DEVIATION_RAISED | OFFER_WITH_CUSTOMER |
| R-RES-20 | RETURNED_TO_COLLINS | PRIOR_STATUS_RESTORED | BACK_TO_ROUTE_DECISION |
| R-RES-21 | WITH_OPS_BOOKING | BOOKING_SUBMITTED | WITH_OPS_BOOKING |
| R-RES-22 | WITH_OPS_BOOKING | BOOKING_CONFIRMED | BOOKED_IN_ALS_NLEADS |
| R-RES-23 | WITH_OPS_BOOKING | BOOKING_REJECTED | WITH_OPS_BOOKING |
| R-RES-24 | WITH_OPS_BOOKING | NLEADS_CALLBACK_MISSING | WITH_OPS_BOOKING |
| R-RES-25 | BOOKED_IN_ALS_NLEADS | SCHEDULE_SET | PLAN_RUNNING |
| and 12 more | | | |

**SETTLEMENT.** 27 rules over 15 states. The full table is in the Business Rules and Routing Logic workbook.

| Rule | From | Event | To |
|---|---|---|---|
| R-SET-01 | ROUTE_APPROVED_SETTLEMENT | ROUTE_APPROVED | PAYOFF_AND_RANGE_SET |
| R-SET-02 | PAYOFF_AND_RANGE_SET | RANGE_SET | WITH_FCR_OFFICER_SET |
| R-SET-03 | PAYOFF_AND_RANGE_SET | PAYOFF_STALE | PAYOFF_AND_RANGE_SET |
| R-SET-04 | WITH_FCR_OFFICER_SET | OFFER_PREPARED | OFFER_WITH_CUSTOMER_SET |
| R-SET-05 | WITH_FCR_OFFICER_SET | OFFER_PREPARED | AWAITING_APPROVAL_SET |
| R-SET-06 | AWAITING_APPROVAL_SET | APPROVAL_GRANTED | OFFER_WITH_CUSTOMER_SET |
| R-SET-07 | AWAITING_APPROVAL_SET | APPROVAL_REFUSED | DECLINED_BY_APPROVER_SET |
| R-SET-08 | DECLINED_BY_APPROVER_SET | DECLINE_RECORDED | RETURNED_TO_ROUTE_SET |
| R-SET-09 | OFFER_WITH_CUSTOMER_SET | CUSTOMER_COUNTER_OFFERED | WITH_FCR_OFFICER_SET |
| R-SET-10 | OFFER_WITH_CUSTOMER_SET | CUSTOMER_SIGNED | WITH_OPS_SETTLEMENT |
| R-SET-11 | OFFER_WITH_CUSTOMER_SET | OFFER_EXPIRED | RETURNED_TO_ROUTE_SET |
| R-SET-12 | OFFER_WITH_CUSTOMER_SET | DEVIATION_RAISED | OFFER_WITH_CUSTOMER_SET |
| R-SET-13 | WITH_OPS_SETTLEMENT | SETTLEMENT_BOOKED | AWAITING_PAYMENT |
| R-SET-14 | AWAITING_PAYMENT | PAYMENT_RECEIVED | PAYMENT_CLEARED |
| R-SET-15 | AWAITING_PAYMENT | PAYMENT_RECEIVED | PAYMENT_PART_RECEIVED |
| R-SET-16 | AWAITING_PAYMENT | PAYMENT_UNMATCHED | AWAITING_PAYMENT |
| R-SET-17 | AWAITING_PAYMENT | PAYMENT_DEADLINE_PASSED | RETURNED_TO_ROUTE_SET |
| R-SET-18 | PAYMENT_PART_RECEIVED | FINAL_INSTALLMENT_RECEIVED | PAYMENT_CLEARED |
| R-SET-19 | PAYMENT_PART_RECEIVED | INSTALLMENT_MISSED | RETURNED_TO_ROUTE_SET |
| R-SET-20 | PAYMENT_CLEARED | CLEARANCE_CONFIRMED | COLLATERAL_RELEASE_REQUESTED |
| R-SET-21 | COLLATERAL_RELEASE_REQUESTED | COLLATERAL_RELEASED | CASE_CLOSED_SETTLED |
| R-SET-22 | COLLATERAL_RELEASE_REQUESTED | TITLE_DOCUMENTS_MISSING | COLLATERAL_RELEASE_REQUESTED |
| R-SET-23 | CASE_CLOSED_SETTLED | PAYMENT_REVERSED | PAYMENT_REVERSED |
| R-SET-24 | PAYMENT_REVERSED | REVERSAL_RECORDED | RETURNED_TO_ROUTE_SET |
| R-SET-25 | WITH_FCR_OFFICER_SET | OFFER_PREPARED | UNMATCHED_EXCEPTION |
| and 2 more | | | |

**DEEDINLIEU.** 37 rules over 20 states. The full table is in the Business Rules and Routing Logic workbook.

| Rule | From | Event | To |
|---|---|---|---|
| R-DIL-01 | ROUTE_APPROVED_DIL | ROUTE_APPROVED | EARLY_READINESS_CHECK |
| R-DIL-02 | EARLY_READINESS_CHECK | ENCUMBRANCE_CLEAR | VALUATION_ORDERED |
| R-DIL-03 | EARLY_READINESS_CHECK | REGISTRATION_CHECK_PASSED | VALUATION_ORDERED |
| R-DIL-04 | EARLY_READINESS_CHECK | ENCUMBRANCE_UNRESOLVED | ENCUMBRANCE_BLOCKED |
| R-DIL-05 | ENCUMBRANCE_BLOCKED | ENCUMBRANCE_CLEARED | VALUATION_ORDERED |
| R-DIL-06 | ENCUMBRANCE_BLOCKED | HOLD_EXPIRED | RETURNED_TO_ROUTE_DIL |
| R-DIL-07 | VALUATION_ORDERED | FAST_LANE_SELECTED | AWAITING_VALUER |
| R-DIL-08 | VALUATION_ORDERED | PRELIMINARY_VALUATION_USED | VALUATION_ACCEPTED |
| R-DIL-09 | AWAITING_VALUER | VALUATION_RECEIVED | VALUATION_ACCEPTED |
| R-DIL-10 | AWAITING_VALUER | ACCESS_REFUSED | VALUATION_ACCEPTED |
| R-DIL-11 | AWAITING_VALUER | VALUER_SLA_BREACHED | AWAITING_VALUER |
| R-DIL-12 | VALUATION_ACCEPTED | VALUE_ACCEPTED | WITH_FCR_OFFICER_DIL |
| R-DIL-13 | WITH_FCR_OFFICER_DIL | TERMS_AGREED | TRANSFER_PRICE_SET |
| R-DIL-14 | TRANSFER_PRICE_SET | PRICE_INSIDE_FLOOR | OFFER_WITH_CUSTOMER_DIL |
| R-DIL-15 | TRANSFER_PRICE_SET | PRICE_BELOW_FLOOR | AWAITING_SECOND_SIGNATURE |
| R-DIL-16 | AWAITING_SECOND_SIGNATURE | SECOND_SIGNATURE_GIVEN | OFFER_WITH_CUSTOMER_DIL |
| R-DIL-17 | AWAITING_SECOND_SIGNATURE | SECOND_SIGNATURE_REFUSED | RETURNED_TO_ROUTE_DIL |
| R-DIL-18 | OFFER_WITH_CUSTOMER_DIL | CUSTOMER_ACCEPTED | WITH_FIELD_INSPECTION |
| R-DIL-19 | OFFER_WITH_CUSTOMER_DIL | CUSTOMER_ACCEPTED | WITH_FIELD_INSPECTION |
| R-DIL-20 | OFFER_WITH_CUSTOMER_DIL | CUSTOMER_WITHDREW | RETURNED_TO_ROUTE_DIL |
| R-DIL-21 | OFFER_WITH_CUSTOMER_DIL | OFFER_EXPIRED | RETURNED_TO_ROUTE_DIL |
| R-DIL-22 | WITH_FIELD_INSPECTION | INSPECTION_COMPLETED | ASSET_UNLOCK_DECISION |
| R-DIL-23 | ASSET_UNLOCK_DECISION | AUTO_UNLOCK_PASSED | AWAITING_TRANSFER |
| R-DIL-24 | ASSET_UNLOCK_DECISION | AUTO_UNLOCK_FAILED | AWAITING_APPROVER_SUMMARY |
| R-DIL-25 | AWAITING_APPROVER_SUMMARY | APPROVER_RELEASED | AWAITING_TRANSFER |
| and 12 more | | | |

## T5. Integration and interfaces

### T5.1 External system interfaces

| ID | System | Direction | Approach | Frequency |
|---|---|---|---|---|
| INT-03 | Core bank (ALS) | Out | Booked by the officer; confirmed on the next day's load | As approved |
| INT-26 | NLEADS | Out | Submitted by the officer in NLEADS | As needed |
| INT-34 | ACE common module | Both | Published module interface | Per request |

### T5.2 Contracts

Version 3 states every cross-module dependency of this module as a contract, so that the service is built against a published artefact and its fake (ADR-020; DP-11). The artefact per call type is: OpenAPI 3.1 for REST, AsyncAPI 3.0 for Kafka, the Temporal interface named here for a workflow or activity, the Interface Specifications manifest for a file, the Nexus operation for the ACE restructure calculator, and a grant on the view for SQL. No row of this section reads another service's table (DP-01). Every consumed contract is class C (Template and Rules R5.4): it never blocks the build, because the consumer builds against the fake, and the real cross-service behaviour is class I work on an integration story. Architecture v5 slides 13 to 20 name a few operations differently from the published files of 22 November 2026; the published file is the artefact the fake is generated from and is the one cited here (GAP-1997; ASM-3224).

#### T5.2.1 Contracts provided

The REST operations of this service are published in `05 Technical architecture/Recovery Workbench API Specification v5/rwb-treatment.yaml` (5.0.0, 22 November 2026) under the base `/api/recovery/treatment/v1`. Appendix T-A holds the endpoint IDs, the access right and the first release of each one.

| # | Method | Path | operationId |
|---|---|---|---|
| 1 | POST | `/cases/{caseId}/treatments` | `postCasesCaseidTreatments` |
| 2 | GET | `/treatments/{treatmentId}` | `getTreatmentsTreatmentid` |
| 3 | PATCH | `/treatments/{treatmentId}` | `patchTreatmentsTreatmentid` |
| 4 | POST | `/treatments/{treatmentId}/submit` | `postTreatmentsTreatmentidSubmit` |

Workflows, schedules, files and views this service provides:

| Contract | Type | Called by or target | Note |
|---|---|---|---|
| TreatmentWorkflow; settlement and deed-in-lieu sagas | Temporal workflow | P3 rwb-case | Stage workflows of the case; run on rwb-treatment |

Events this service publishes (AsyncAPI 3.0, CloudEvents 1.0):

| Event | EV | Topic | Consumers |
|---|---|---|---|
| TreatmentApproved | EV-10 | `rwb.treatment.events.v1` | rwb-comms, rwb-payment |
| TreatmentClosed | — | `rwb.treatment.events.v1` | rwb-case, rwb-reporting |

#### T5.2.2 Contracts consumed

| Contract | Type | Provider | Class | Failure path |
|---|---|---|---|---|
| Approval | Temporal child workflow | P7 rwb-decision | C | Workflow retry policy; the caller keeps its state (DP-12) |
| Contract generation and e-signature | Temporal activity | P5 rwb-document | C | Workflow retry policy; the caller keeps its state (DP-12) |
| postProceeds | Temporal activity | P8 rwb-payment | C | Workflow retry policy; the caller keeps its state (DP-12) |
| Restructure calculator | Nexus operation | ACE Common | X | Tracked only; outside the Workbench; class X |

Events this service consumes:

| Event | EV | Provider topic | Provider | Class | Failure path |
|---|---|---|---|---|---|
| TreatmentBooked | EV-11 | `rwb.payment.events.v1` | P8 rwb-payment | C | Retry 1 min, 10 min, 1 h, then `.dlt`; inbox dedupe |
| PaymentMissed | EV-12 | `rwb.payment.events.v1` | P8 rwb-payment | C | Retry 1 min, 10 min, 1 h, then `.dlt`; inbox dedupe |
| DeviationRaised | EV-06 | `rwb.deviation.events.v1` | S8 rwb-deviation | C | Retry 1 min, 10 min, 1 h, then `.dlt`; inbox dedupe |

#### T5.2.3 Call-type summary

| Call type | Provided | Consumed | Artefact |
|---|---|---|---|
| REST | 4 | 0 | OpenAPI 3.1, one file per service |
| Kafka (events) | 2 | 3 | AsyncAPI 3.0, one file per service |
| Temporal | 1 | 3 | Workflow and activity interfaces, queue `rwb-treatment` |
| File | 0 | 0 | Interface Specifications manifest and the SAS link |
| Nexus | 0 | 0 | Nexus operation into ACE |
| SQL | 0 | 0 | Read-only grant on the view |

A contract change is a new version of the artefact, never a code change in the consumer (ADR-020). The provider named in T5.2.2 is the owner in Microservice Ownership Map v1, and the consumer list of each event is the Arch v5 event catalogue on slides 42 and 43.

### T5.3 Events

The event contract of this service is `05 Technical architecture/Recovery Workbench API Specification v5/asyncapi/rwb-treatment.asyncapi.yaml`; the shared decision-record contract is `asyncapi/rwb.decision-record.v1.asyncapi.yaml`. Every service publishes DecisionRecorded (EV-08) to `rwb.decision-record.v1` from its outbox in the same transaction as its state change (DP-03, DP-09; ADR-015, ADR-022); consuming services dedupe through their inbox table. Events carry identifiers and facts, never personal data (Event and Messaging Design v4, sheet Rules).

| Event | EV | Direction | Topic |
|---|---|---|---|
| TreatmentApproved | EV-10 | Published | `rwb.treatment.events.v1` |
| TreatmentClosed | — | Published | `rwb.treatment.events.v1` |
| TreatmentBooked | EV-11 | Consumed | `rwb.payment.events.v1` |
| PaymentMissed | EV-12 | Consumed | `rwb.payment.events.v1` |
| DeviationRaised | EV-06 | Consumed | `rwb.deviation.events.v1` |

An event shown with `—` has no number in the numbered catalogue: the Arch v5 catalogue calls these rows `+`, so the number is not specified in the source documents (GAP-1996; ASM-3223).

## T6. Security and access control

### T6.1 RBAC matrix

| Role | Treatment and offer |
|---|---|
| RW-CASEOWN Case owner | CRU |
| RW-TEAMMGR Team manager | R |
| RW-RESTRUCT Restructuring officer (FCR) | CRUA |
| RW-SPECIAL Hardship and vulnerability specialist | CRU |
| RW-COMPLAIN Complaint officer | R |
| RW-FRAUD Fraud investigator | R |
| RW-LITOFF Litigation officer | R |
| RW-LEGAL Legal counsel | R |
| RW-GUARANT Guarantee officer | CRU |
| RW-CONDUCT Conduct and QA officer | R |
| RW-PRODHEAD Product head (Mortgage, HP, SSME) | RA |
| RW-CREDCOMM Credit approval committee member | RA |
| RW-RISK Risk and model risk officer | R |
| RW-COE Center of excellence analyst | R |
| RW-AUDIT Internal audit | R |
| RW-BIANAL Reporting and BI analyst | R |
| RW-TRIBE Tribe lead and squad members | R |
| SY-CASEWF Case workflow module | R |
| SY-RULES Rules component | R |
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
| REQ-S2-001 | FEAT-TRT-01 | Written one epic ahead | With the story |
| REQ-S2-002 | FEAT-TRT-01 | Written one epic ahead | With the story |
| REQ-S2-003 | FEAT-TRT-01 | Written one epic ahead | With the story |
| REQ-S2-004 | FEAT-TRT-01 | Written one epic ahead | With the story |
| REQ-S2-005 | FEAT-TRT-01 | Written one epic ahead | With the story |
| REQ-S2-006 | FEAT-TRT-01 | Written one epic ahead | With the story |
| REQ-S2-007 | FEAT-TRT-01 | Written one epic ahead | With the story |
| REQ-S2-008 | FEAT-TRT-01 | Written one epic ahead | With the story |
| REQ-S2-009 | FEAT-TRT-01 | Written one epic ahead | With the story |
| REQ-S2-010 | FEAT-TRT-01 | Written one epic ahead | With the story |

## Appendix T-A. API specification

### T-A.1 Endpoint inventory

| ID | Method | Path | Access | First in |
|---|---|---|---|---|
| API-S2-001 | POST | /api/recovery/treatment/v1/cases/{caseId}/treatments | Treatment and offer C | E2 |
| API-S2-002 | GET | /api/recovery/treatment/v1/treatments/{treatmentId} | Treatment and offer R | E2 |
| API-S2-003 | PATCH | /api/recovery/treatment/v1/treatments/{treatmentId} | Treatment and offer U | E3 |
| API-S2-004 | POST | /api/recovery/treatment/v1/treatments/{treatmentId}/submit | Treatment and offer U | E3 |

The operation IDs, paths and operationIds of these endpoints are published in `05 Technical architecture/Recovery Workbench API Specification v5/rwb-treatment.yaml`; where an appendix row and the published operation differ, the published operation is the contract of T5.2.1 and the row keeps its ID for traceability (GAP-1997; ASM-3224).

### T-A.2 Endpoint detail

#### API-S2-001 POST /cases/{caseId}/treatments

| Item | Value |
|---|---|
| Purpose | Open a restructure, settlement or deed in lieu treatment |
| Request | TreatmentRequest |
| Response | Treatment |
| Errors | 401, 403, 404, 409, 422, 503 |
| Authorization | Treatment and offer, right C, scope applied |
| Idempotency | Idempotency-Key header |

#### API-S2-002 GET /treatments/{treatmentId}

| Item | Value |
|---|---|
| Purpose | Read a treatment with its terms, status and booking |
| Request | None |
| Response | Treatment |
| Errors | 401, 403, 404, 503 |
| Authorization | Treatment and offer, right R, scope applied |
| Idempotency | Not applicable |

#### API-S2-003 PATCH /treatments/{treatmentId}

| Item | Value |
|---|---|
| Purpose | Change the terms of a draft treatment |
| Request | TreatmentUpdate |
| Response | Treatment |
| Errors | 401, 403, 404, 409, 422, 503 |
| Authorization | Treatment and offer, right U, scope applied |
| Idempotency | Not applicable |

#### API-S2-004 POST /treatments/{treatmentId}/submit

| Item | Value |
|---|---|
| Purpose | Submit a treatment for approval |
| Request | None |
| Response | Approval |
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
