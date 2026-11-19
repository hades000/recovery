<!-- source: 05 Technical architecture/Recovery Workbench Technical Specifications by Module v5.zip!Recovery Workbench TSD S3 Guarantees and guarantors v2.md -->
<!-- converted: 2026-11-16 from Markdown (extracted) -->

> **Source:** `05 Technical architecture/Recovery Workbench Technical Specifications by Module v5.zip!Recovery Workbench TSD S3 Guarantees and guarantors v2.md`  
> **Converted from:** Markdown (extracted)

# Recovery Workbench S3 Guarantees and guarantors

Technical specification. SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd

## Document control

| Attribute | Value |
|---|---|
| Document title | TSD S3 Guarantees and guarantors |
| Document ID | S3-RWB-TSD-v2 |
| Version | 2 |
| Status | In review |
| Date | 28 October 2026 |
| TSD owner | Solution architect |
| Build squad | TechX recovery squads |

| Document | Type | Relationship |
|---|---|---|
| Recovery Workbench FSD S3 Guarantees and guarantors | FSD | Pair |
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

S3 Guarantees and guarantors is part of the recovery module in the ACE service: one service, one repository, one front end. It covers: tCG and insurance claims, guarantor notices and pursuit. It reaches other modules only through their published interfaces and other systems only through COLLINS, file loads and the ACE paths.

## T2. Component design

| Component | Responsibility |
|---|---|
| GuaranteesAndGuarantorsController | REST endpoints in appendix T-A; validation; maps errors to problem responses |
| GuaranteesAndGuarantorsService | Business logic; calls the rules component; writes the decision log entry before any change |
| GuaranteesAndGuarantorsRepository | Reads and writes the module's tables only |
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

**guarantee_claim** (NEW). A claim against a Thai Credit Guarantee Corporation guarantee or an insurer.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-TRT-015 | id | TEXT | uuid | Yes | None | Workbench |
| DF-TRT-016 | case_id | CROSS_REF | uuid | Yes | None | Workbench |
| DF-TRT-017 | claim_type | LOV | varchar(25) | Yes | LOV-CLAIM-TYPE | Workbench |
| DF-TRT-018 | claim_deadline | DATE | date | Yes | None | Workbench |
| DF-TRT-019 | claimed_amount | NUMBER | numeric(18,2) | Yes | None | Workbench |
| DF-TRT-020 | filed_at | DATE | date | No | None | Workbench |
| DF-TRT-021 | paid_amount | NUMBER | numeric(18,2) | No | None | Workbench |
| DF-TRT-022 | status | LOV | varchar(12) | Yes | LOV-CLAIM-STATUS | Workbench |

### T3.2 Lists of values

| List | Values |
|---|---|
| LOV-CLAIM-STATUS | PREPARING, FILED, DEFECT, PAID, REJECTED |
| LOV-CLAIM-TYPE | TCG, CREDIT_LIFE_INSURANCE, MORTGAGE_INSURANCE, COLLATERAL_INSURANCE |

### T3.3 Relationships

| From | To | Field | Cardinality |
|---|---|---|---|
| guarantee_claim | case_id | recovery_case | Many to 1 |

## T4. State machines and workflow

**GUARANTEE.** 32 rules over 17 states. The full table is in the Business Rules and Routing Logic workbook.

| Rule | From | Event | To |
|---|---|---|---|
| R-GUA-01 | GUARANTEE_DETECTED | GUARANTEE_FOUND | DEADLINE_TIMER_RUNNING |
| R-GUA-02 | GUARANTEE_DETECTED | CONDITIONS_NOT_MET | NOT_ELIGIBLE |
| R-GUA-03 | NOT_ELIGIBLE | CONDITIONS_LATER_MET | DEADLINE_TIMER_RUNNING |
| R-GUA-04 | DEADLINE_TIMER_RUNNING | PREPARATION_DUE | CLAIM_PREPARATION |
| R-GUA-05 | DEADLINE_TIMER_RUNNING | CLAIM_DEADLINE_MISSED | DEADLINE_MISSED |
| R-GUA-06 | DEADLINE_TIMER_RUNNING | GUARANTOR_NOTICE_DUE | GUARANTOR_NOTICE |
| R-GUA-07 | CLAIM_PREPARATION | CHECKLIST_COMPLETE | CLAIM_APPROVAL |
| R-GUA-08 | CLAIM_PREPARATION | CHECKLIST_INCOMPLETE | CLAIM_DEFECT_HOLD |
| R-GUA-09 | CLAIM_PREPARATION | CLAIM_DEADLINE_MISSED | DEADLINE_MISSED |
| R-GUA-10 | CLAIM_DEFECT_HOLD | DOCUMENT_SUPPLIED | CLAIM_PREPARATION |
| R-GUA-11 | CLAIM_DEFECT_HOLD | DEADLINE_WARNING | CLAIM_APPROVAL |
| R-GUA-12 | CLAIM_APPROVAL | CLAIM_APPROVED | CLAIM_SUBMITTED |
| R-GUA-13 | CLAIM_APPROVAL | CLAIM_SENT_BACK | CLAIM_PREPARATION |
| R-GUA-14 | CLAIM_SUBMITTED | TCG_QUERY_RAISED | TCG_QUERY |
| R-GUA-15 | TCG_QUERY | QUERY_ANSWERED | CLAIM_SUBMITTED |
| R-GUA-16 | TCG_QUERY | QUERY_UNANSWERED | CLAIM_REJECTED |
| R-GUA-17 | CLAIM_SUBMITTED | CLAIM_REJECTED_BY_TCG | CLAIM_REJECTED |
| R-GUA-18 | CLAIM_REJECTED | RESUBMISSION_POSSIBLE | CLAIM_PREPARATION |
| R-GUA-19 | CLAIM_REJECTED | RESUBMISSION_NOT_POSSIBLE | RESIDUAL_TO_ROUTE |
| R-GUA-20 | CLAIM_SUBMITTED | PART_PAYMENT_RECEIVED | CLAIM_PART_PAID |
| R-GUA-21 | CLAIM_PART_PAID | BALANCE_CLAIMED | CLAIM_SUBMITTED |
| R-GUA-22 | CLAIM_SUBMITTED | FULL_PAYMENT_RECEIVED | CLAIM_PAID |
| R-GUA-23 | CLAIM_PAID | SUBROGATION_DUE | SUBROGATION_POSITION |
| R-GUA-24 | CLAIM_PART_PAID | SUBROGATION_DUE | SUBROGATION_POSITION |
| R-GUA-25 | SUBROGATION_POSITION | RESIDUAL_REMAINS | RESIDUAL_TO_ROUTE |
| and 7 more | | | |

## T5. Integration and interfaces

### T5.1 External system interfaces

| ID | System | Direction | Approach | Frequency |
|---|---|---|---|---|
| INT-29 | Thai Credit Guarantee Corporation | Both | Not available today; entered and filed by the guarantee officer | As needed |

### T5.2 Cross-module interfaces

Calls go through the published Java interfaces: P3 for the case, P7 for the decision log, P4 for access and reference data, P5 for documents, P6 for notices.

### T5.3 Events

| Event | Direction |
|---|---|
| None | |

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
| REQ-S3-001 | FEAT-GUA-01 | Written one epic ahead | With the story |
| REQ-S3-002 | FEAT-GUA-01 | Written one epic ahead | With the story |
| REQ-S3-003 | FEAT-GUA-01 | Written one epic ahead | With the story |
| REQ-S3-004 | FEAT-GUA-01 | Written one epic ahead | With the story |
| REQ-S3-005 | FEAT-GUA-01 | Written one epic ahead | With the story |
| REQ-S3-006 | FEAT-GUA-01 | Written one epic ahead | With the story |
| REQ-S3-007 | FEAT-GUA-01 | Written one epic ahead | With the story |

## Appendix T-A. API specification

### T-A.1 Endpoint inventory

| ID | Method | Path | Access | First in |
|---|---|---|---|---|
| API-S3-001 | POST | /api/recovery/v1/cases/{caseId}/guarantee-claims | Treatment and offer C | E4 |
| API-S3-002 | PATCH | /api/recovery/v1/guarantee-claims/{claimId} | Treatment and offer U | E4 |

### T-A.2 Endpoint detail

#### API-S3-001 POST /cases/{caseId}/guarantee-claims

| Item | Value |
|---|---|
| Purpose | Open a guarantee or TCG claim |
| Request | GuaranteeClaimRequest |
| Response | GuaranteeClaim |
| Errors | 401, 403, 404, 409, 422, 503 |
| Authorization | Treatment and offer, right C, scope applied |
| Idempotency | Idempotency-Key header |

#### API-S3-002 PATCH /guarantee-claims/{claimId}

| Item | Value |
|---|---|
| Purpose | Record the claim result |
| Request | GuaranteeClaimUpdate |
| Response | GuaranteeClaim |
| Errors | 401, 403, 404, 409, 422, 503 |
| Authorization | Treatment and offer, right U, scope applied |
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
