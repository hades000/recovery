<!-- source: 05 Technical architecture/Recovery Workbench Technical Specifications by Module v3/Recovery Workbench TSD S2 TDR, settlement and deed in lieu v2.md -->
<!-- converted: 2026-11-04 from Markdown (copied) -->

> **Source:** `05 Technical architecture/Recovery Workbench Technical Specifications by Module v3/Recovery Workbench TSD S2 TDR, settlement and deed in lieu v2.md`  
> **Converted from:** Markdown (copied)

# Recovery Workbench S2 TDR, settlement and deed in lieu

Technical specification. SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd

## Document control

| Attribute | Value |
|---|---|
| Document title | TSD S2 TDR, settlement and deed in lieu |
| Document ID | S2-RWB-TSD-v2 |
| Version | 2 |
| Status | In review |
| Date | 28 October 2026 |
| TSD owner | Solution architect |
| Build squad | TechX recovery squads |

| Document | Type | Relationship |
|---|---|---|
| Recovery Workbench FSD S2 TDR, settlement and deed in lieu | FSD | Pair |
| Recovery Workbench Target Architecture | Architecture | Parent |
| Recovery Workbench Logical Data Model and Data Dictionary | Data | Source of T3 |
| Recovery Workbench API Specification | API | Source of appendix T-A |

## Existing capability check

| Capability | Verdict | Owning document | Note |
|---|---|---|---|
| Sign-in, access check, audit, PII and SOC logging | REUSE | ACE common module | Called through the published interface |
| Scheduler and batch | REUSE | ACE pattern: Quartz and Spring Batch | Jobs in the Batch and Scheduling Design |
| Outbox and retry | REUSE | Error Handling and Resilience Standard | Through P2 |
| Rules evaluation | REUSE | Rules Engine Design | Through the rules component |

## T1. Architecture overview

S2 TDR, settlement and deed in lieu is part of the recovery module in the ACE service: one service, one repository, one front end. It covers: treatment record, contracts, booking, plan timers. It reaches other modules only through their published interfaces and other systems only through COLLINS, file loads and the ACE paths.

## T2. Component design

| Component | Responsibility |
|---|---|
| TdrSettlementAndDeedInLieuController | REST endpoints in appendix T-A; validation; maps errors to problem responses |
| TdrSettlementAndDeedInLieuService | Business logic; calls the rules component; writes the decision log entry before any change |
| TdrSettlementAndDeedInLieuRepository | Reads and writes the module's tables only |
| Jobs | Quartz and Spring Batch jobs the module owns |
| Published interface | Java interface other modules call; no table is read across modules |

## T3. Data model

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

### T5.2 Cross-module interfaces

Calls go through the published Java interfaces: P3 for the case, P7 for the decision log, P4 for access and reference data, P5 for documents, P6 for notices.

### T5.3 Events

| Event | Direction |
|---|---|
| TreatmentApproved | Published |

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
| API-S2-001 | POST | /api/recovery/v1/cases/{caseId}/treatments | Treatment and offer C | E2 |
| API-S2-002 | GET | /api/recovery/v1/treatments/{treatmentId} | Treatment and offer R | E2 |
| API-S2-003 | PATCH | /api/recovery/v1/treatments/{treatmentId} | Treatment and offer U | E3 |
| API-S2-004 | POST | /api/recovery/v1/treatments/{treatmentId}/submit | Treatment and offer U | E3 |

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
