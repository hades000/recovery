<!-- source: 05 Technical architecture/Recovery Workbench Technical Specifications by Module v3.zip!Recovery Workbench TSD S6 Debt sale v2.md -->
<!-- converted: 2026-11-16 from Markdown (extracted) -->

> **Source:** `05 Technical architecture/Recovery Workbench Technical Specifications by Module v3.zip!Recovery Workbench TSD S6 Debt sale v2.md`  
> **Converted from:** Markdown (extracted)

# Recovery Workbench S6 Debt sale

Technical specification. SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd

## Document control

| Attribute | Value |
|---|---|
| Document title | TSD S6 Debt sale |
| Document ID | S6-RWB-TSD-v2 |
| Version | 2 |
| Status | In review |
| Date | 28 October 2026 |
| TSD owner | Solution architect |
| Build squad | TechX recovery squads |

| Document | Type | Relationship |
|---|---|---|
| Recovery Workbench FSD S6 Debt sale | FSD | Pair |
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

S6 Debt sale is part of the recovery module in the ACE service: one service, one repository, one front end. It covers: lot building, data room, buyer terms, award, transfer. It reaches other modules only through their published interfaces and other systems only through COLLINS, file loads and the ACE paths.

## T2. Component design

| Component | Responsibility |
|---|---|
| DebtSaleController | REST endpoints in appendix T-A; validation; maps errors to problem responses |
| DebtSaleService | Business logic; calls the rules component; writes the decision log entry before any change |
| DebtSaleRepository | Reads and writes the module's tables only |
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

**debt_sale_lot** (NEW). A lot of accounts offered to debt buyers.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-SAL-020 | id | TEXT | uuid | Yes | None | Workbench |
| DF-SAL-021 | lot_no | TEXT | varchar(15) | Yes | None | Workbench |
| DF-SAL-022 | cut_off_date | DATE | date | Yes | None | Workbench |
| DF-SAL-023 | segment | LOV | varchar(20) | Yes | LOV-SEGMENT | Workbench |
| DF-SAL-024 | reserve_price | NUMBER | numeric(18,2) | No | None | Workbench |
| DF-SAL-025 | buyer_partner_id | CROSS_REF | uuid | No | None | Workbench |
| DF-SAL-026 | buyer_class | LOV | varchar(10) | No | LOV-BUYER-CLASS | Workbench |
| DF-SAL-027 | signing_date | DATE | date | No | None | Workbench |
| DF-SAL-028 | approval_authority | TEXT | varchar(60) | No | None | Workbench |
| DF-SAL-029 | payment_terms | TEXT | varchar(400) | No | None | Workbench |
| DF-SAL-030 | status | LOV | varchar(12) | Yes | LOV-LOT-STATUS | Workbench |

**debt_sale_account** (NEW). An account in a debt sale lot.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-SAL-031 | id | TEXT | uuid | Yes | None | Workbench |
| DF-SAL-032 | lot_id | CROSS_REF | uuid | Yes | None | Workbench |
| DF-SAL-033 | account_id | CROSS_REF | uuid | Yes | None | Workbench |
| DF-SAL-034 | borrower_code | TEXT | varchar(20) | No | None | Workbench |
| DF-SAL-035 | outstanding | NUMBER | numeric(18,2) | Yes | None | Core bank (ALS) via COLLINS |
| DF-SAL-036 | selling_price | NUMBER | numeric(18,2) | No | None | Workbench |
| DF-SAL-037 | put_back_status | LOV | varchar(12) | No | LOV-PUTBACK | Workbench |

### T3.2 Lists of values

| List | Values |
|---|---|
| LOV-BUYER-CLASS | AMC, NON_AMC |
| LOV-LOT-STATUS | BUILDING, OFFERED, AWARDED, TRANSFERRED, CLOSED |
| LOV-PUTBACK | NONE, CLAIMED, ACCEPTED, REJECTED |
| LOV-SEGMENT | RETAIL, SSME, CORPORATE |

### T3.3 Relationships

| From | To | Field | Cardinality |
|---|---|---|---|
| debt_sale_lot | buyer_partner_id | partner | Many to 0 or 1 |
| debt_sale_account | lot_id | debt_sale_lot | Many to 1 |
| debt_sale_account | account_id | loan_account | Many to 1 |

## T4. State machines and workflow

**DEBTSALE.** 41 rules over 29 states. The full table is in the Business Rules and Routing Logic workbook.

| Rule | From | Event | To |
|---|---|---|---|
| R-DS-01 | LOT_CANDIDATE_SELECTED | DEBT_SALE_CYCLE_OPENED | LOT_BUILT |
| R-DS-02 | LOT_CANDIDATE_SELECTED | ACCOUNT_EXCLUDED | CASE_EXCLUDED |
| R-DS-03 | CASE_EXCLUDED | EXCLUSION_CLEARED | BACK_TO_CASE_LIST |
| R-DS-04 | LOT_BUILT | LOT_PRICED | LOT_WITH_COMMITTEE |
| R-DS-05 | LOT_BUILT | LOT_TOO_THIN | LOT_BUILT |
| R-DS-06 | LOT_WITH_COMMITTEE | LOT_APPROVED_BY_COMMITTEE | LOT_APPROVED |
| R-DS-07 | LOT_WITH_COMMITTEE | RESERVE_RAISED | LOT_WITH_COMMITTEE |
| R-DS-08 | LOT_WITH_COMMITTEE | LOT_REFUSED | LOT_WITHDRAWN |
| R-DS-09 | LOT_WITHDRAWN | ACCOUNTS_RETURNED | BACK_TO_CASE_LIST |
| R-DS-10 | LOT_APPROVED | TAPE_BUILD_RUN | TAPE_PREPARED |
| R-DS-11 | TAPE_PREPARED | MASKING_CHECK_FAILED | TAPE_REJECTED |
| R-DS-12 | TAPE_REJECTED | TAPE_REBUILT | TAPE_PREPARED |
| R-DS-13 | TAPE_PREPARED | MASKING_CHECK_PASSED | DATA_ROOM_OPEN |
| R-DS-14 | DATA_ROOM_OPEN | BUYER_REQUESTED_ACCESS | BUYER_PENDING_KYC |
| R-DS-15 | BUYER_PENDING_KYC | KYC_PASSED | BUYER_CLEARED |
| R-DS-16 | BUYER_PENDING_KYC | KYC_FAILED | BUYER_REJECTED |
| R-DS-17 | BUYER_CLEARED | BIDDING_WINDOW_OPENED | BIDDING_OPEN |
| R-DS-18 | BIDDING_OPEN | BID_SUBMITTED | BIDS_RECEIVED |
| R-DS-19 | BIDS_RECEIVED | BIDDING_WINDOW_CLOSED | AWARD_PENDING |
| R-DS-20 | BIDS_RECEIVED | BEST_BID_BELOW_RESERVE | BID_BELOW_RESERVE |
| R-DS-21 | BID_BELOW_RESERVE | LOT_REOFFERED | BIDDING_OPEN |
| R-DS-22 | BID_BELOW_RESERVE | LOT_NOT_CLEARED | LOT_WITHDRAWN |
| R-DS-23 | AWARD_PENDING | AWARD_CONFIRMED | LOT_AWARDED |
| R-DS-24 | LOT_AWARDED | SETTLEMENT_TERM_STARTED | SETTLEMENT_PENDING |
| R-DS-25 | SETTLEMENT_PENDING | BUYER_SETTLED | SETTLED |
| and 16 more | | | |

## T5. Integration and interfaces

### T5.1 External system interfaces

| ID | System | Direction | Approach | Frequency |
|---|---|---|---|---|
| INT-25 | Debt buyers | Out | File through the data room | Per lot |

### T5.2 Cross-module interfaces

Calls go through the published Java interfaces: P3 for the case, P7 for the decision log, P4 for access and reference data, P5 for documents, P6 for notices.

### T5.3 Events

| Event | Direction |
|---|---|
| LotAwarded | Published |

## T6. Security and access control

### T6.1 RBAC matrix

| Role | Debt sale |
|---|---|
| RW-SALEOFF Sale officer | R |
| RW-NPAMGR NPA and asset manager | R |
| RW-DEBTSALE Debt sale officer | CRUA |
| RW-WRITEOFF Write-off team member | R |
| RW-CREDITAD Credit Administration officer | R |
| RW-AGENCYMG Partner and agency manager | R |
| RW-CONDUCT Conduct and QA officer | R |
| RW-PRODHEAD Product head (Mortgage, HP, SSME) | RA |
| RW-HEADNPA Head of NPA | R |
| RW-HEADASL Head of Asset Liquidity | RA |
| RW-RISK Risk and model risk officer | R |
| RW-COE Center of excellence analyst | R |
| RW-FINANCE Finance and CFO delegate | R |
| RW-AUDIT Internal audit | R |
| RW-BIANAL Reporting and BI analyst | R |
| RW-TRIBE Tribe lead and squad members | R |
| PT-BUYER Debt buyer and AMC | RU |
| PT-RAMC RAMC user | R |
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
| REQ-S6-001 | FEAT-DBS-01 | Written one epic ahead | With the story |
| REQ-S6-002 | FEAT-DBS-01 | Written one epic ahead | With the story |
| REQ-S6-003 | FEAT-DBS-01 | Written one epic ahead | With the story |
| REQ-S6-004 | FEAT-DBS-05 | Written one epic ahead | With the story |
| REQ-S6-005 | FEAT-DBS-05 | Written one epic ahead | With the story |
| REQ-S6-006 | FEAT-DBS-05 | Written one epic ahead | With the story |
| REQ-S6-007 | FEAT-DBS-05 | Written one epic ahead | With the story |
| REQ-S6-008 | FEAT-DBS-05 | Written one epic ahead | With the story |
| REQ-S6-009 | FEAT-DBS-05 | Written one epic ahead | With the story |

## Appendix T-A. API specification

### T-A.1 Endpoint inventory

| ID | Method | Path | Access | First in |
|---|---|---|---|---|
| API-S6-001 | POST | /api/recovery/v1/debt-sale-lots | Debt sale C | E5 |
| API-S6-002 | GET | /api/recovery/v1/debt-sale-lots/{lotId} | Debt sale R | E5 |
| API-S6-003 | POST | /api/recovery/v1/debt-sale-lots/{lotId}/award | Debt sale A | E6 |
| API-S6-004 | GET | /api/recovery/v1/partner/data-room/{lotId} | Partner portal R | E5 |
| API-S6-005 | POST | /api/recovery/v1/partner/data-room/{lotId}/bids | Partner portal C | E5 |

### T-A.2 Endpoint detail

#### API-S6-001 POST /debt-sale-lots

| Item | Value |
|---|---|
| Purpose | Create a lot from eligible accounts |
| Request | LotRequest |
| Response | DebtSaleLot |
| Errors | 401, 403, 409, 422, 503 |
| Authorization | Debt sale, right C, scope applied |
| Idempotency | Idempotency-Key header |

#### API-S6-002 GET /debt-sale-lots/{lotId}

| Item | Value |
|---|---|
| Purpose | Read a lot with its accounts, reserve and bids |
| Request | None |
| Response | DebtSaleLot |
| Errors | 401, 403, 404, 503 |
| Authorization | Debt sale, right R, scope applied |
| Idempotency | Not applicable |

#### API-S6-003 POST /debt-sale-lots/{lotId}/award

| Item | Value |
|---|---|
| Purpose | Award a lot to a buyer after the bids close |
| Request | AwardRequest |
| Response | DecisionLogEntry |
| Errors | 401, 403, 404, 409, 422, 503 |
| Authorization | Debt sale, right A, scope applied |
| Idempotency | Idempotency-Key header |

#### API-S6-004 GET /partner/data-room/{lotId}

| Item | Value |
|---|---|
| Purpose | Read the lot tape and documents for an admitted buyer |
| Request | None |
| Response | DataRoom |
| Errors | 401, 403, 404, 503 |
| Authorization | Partner portal, right R, scope applied |
| Idempotency | Not applicable |

#### API-S6-005 POST /partner/data-room/{lotId}/bids

| Item | Value |
|---|---|
| Purpose | Submit a bid on a lot |
| Request | BidRequest |
| Response | Bid |
| Errors | 401, 403, 404, 409, 422, 503 |
| Authorization | Partner portal, right C, scope applied |
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
