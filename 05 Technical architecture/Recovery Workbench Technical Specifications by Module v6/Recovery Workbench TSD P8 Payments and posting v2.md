# Recovery Workbench P8 Payments and posting

Technical specification. SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd

## Document control

| Attribute | Value |
|---|---|
| Document title | TSD P8 Payments and posting |
| Document ID | P8-RWB-TSD-v2 |
| Version | 2 |
| Status | In review |
| Date | 28 October 2026 |
| TSD owner | Solution architect |
| Build squad | TechX recovery squads |

| Document | Type | Relationship |
|---|---|---|
| Recovery Workbench FSD P8 Payments and posting | FSD | Pair |
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

P8 Payments and posting is part of the recovery module in the ACE service: one service, one repository, one front end. It covers: payment and proceeds matching, fees, posting files. It reaches other modules only through their published interfaces and other systems only through COLLINS, file loads and the ACE paths.

## T2. Component design

| Component | Responsibility |
|---|---|
| PaymentsAndPostingController | REST endpoints in appendix T-A; validation; maps errors to problem responses |
| PaymentsAndPostingService | Business logic; calls the rules component; writes the decision log entry before any change |
| PaymentsAndPostingRepository | Reads and writes the module's tables only |
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

### T5.2 Cross-module interfaces

Calls go through the published Java interfaces: P3 for the case, P7 for the decision log, P4 for access and reference data, P5 for documents, P6 for notices.

### T5.3 Events

| Event | Direction |
|---|---|
| TreatmentBooked | Published |
| PaymentMissed | Published |
| ProceedsMatched | Published |

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
| API-P8-001 | GET | /api/recovery/v1/proceeds | Write-off and posting R | E2 |
| API-P8-002 | POST | /api/recovery/v1/proceeds/{proceedsId}/match | Write-off and posting U | E4 |

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
