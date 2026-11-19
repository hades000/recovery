<!-- source: 05 Technical architecture/Recovery Workbench Technical Specifications by Module v3.zip!Recovery Workbench TSD S1 Valuation and route v2.md -->
<!-- converted: 2026-11-16 from Markdown (extracted) -->

> **Source:** `05 Technical architecture/Recovery Workbench Technical Specifications by Module v3.zip!Recovery Workbench TSD S1 Valuation and route v2.md`  
> **Converted from:** Markdown (extracted)

# Recovery Workbench S1 Valuation and route

Technical specification. SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd

## Document control

| Attribute | Value |
|---|---|
| Document title | TSD S1 Valuation and route |
| Document ID | S1-RWB-TSD-v2 |
| Version | 2 |
| Status | In review |
| Date | 28 October 2026 |
| TSD owner | Solution architect |
| Build squad | TechX recovery squads |

| Document | Type | Relationship |
|---|---|---|
| Recovery Workbench FSD S1 Valuation and route | FSD | Pair |
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

S1 Valuation and route is part of the recovery module in the ACE service: one service, one repository, one front end. It covers: d6 route decision with COLLINS return by route and the route agent. It reaches other modules only through their published interfaces and other systems only through COLLINS, file loads and the ACE paths.

## T2. Component design

| Component | Responsibility |
|---|---|
| ValuationAndRouteController | REST endpoints in appendix T-A; validation; maps errors to problem responses |
| ValuationAndRouteService | Business logic; calls the rules component; writes the decision log entry before any change |
| ValuationAndRouteRepository | Reads and writes the module's tables only |
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

**valuation** (NEW). An appraisal of collateral or an asset.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-COL-018 | id | TEXT | uuid | Yes | None | Workbench |
| DF-COL-019 | collateral_id | CROSS_REF | uuid | No | None | Workbench |
| DF-COL-020 | asset_id | CROSS_REF | uuid | No | None | Workbench |
| DF-COL-021 | appraisal_no | TEXT | varchar(20) | Yes | None | SVAF |
| DF-COL-022 | appraisal_type | LOV | varchar(15) | Yes | LOV-APPRAISAL | SVAF |
| DF-COL-023 | appraised_value | NUMBER | numeric(18,2) | Yes | None | SVAF |
| DF-COL-024 | forced_sale_value | NUMBER | numeric(18,2) | No | None | SVAF |
| DF-COL-025 | appraisal_date | DATE | date | Yes | None | SVAF |
| DF-COL-026 | valuer_partner_id | CROSS_REF | uuid | No | None | Workbench |
| DF-COL-027 | accepted | BOOLEAN | boolean | Yes | None | Workbench |
| DF-COL-043 | stale_flag | BOOLEAN | boolean | Yes | None | Workbench |
| DF-COL-044 | age_days | FORMULA | integer | No | None | Workbench |

**score** (REUSE ACE). A score or estimate COLLINS returns for an account or case.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-DEC-019 | id | TEXT | uuid | Yes | None | Workbench |
| DF-DEC-020 | account_id | CROSS_REF | uuid | No | None | Workbench |
| DF-DEC-021 | case_id | CROSS_REF | uuid | No | None | Workbench |
| DF-DEC-022 | model_code | TEXT | varchar(30) | Yes | None | COLLINS |
| DF-DEC-023 | model_version | TEXT | varchar(20) | Yes | None | COLLINS |
| DF-DEC-024 | score_value | NUMBER | numeric(12,4) | No | None | COLLINS |
| DF-DEC-025 | estimate_value | NUMBER | numeric(18,2) | No | None | COLLINS |
| DF-DEC-026 | route_code | LOV | varchar(4) | No | LOV-ROUTE | COLLINS |
| DF-DEC-027 | scored_at | DATE | date | Yes | None | COLLINS |

### T3.2 Lists of values

| List | Values |
|---|---|
| LOV-APPRAISAL | MARKET, OFFICIAL, FORCED_SALE, DESKTOP, AGENT_ESTIMATE |
| LOV-ROUTE | R1, R2, R3, R4, R5, R6, R7, R8 |

### T3.3 Relationships

| From | To | Field | Cardinality |
|---|---|---|---|
| valuation | collateral_id | collateral | Many to 0 or 1 |
| valuation | asset_id | asset | Many to 0 or 1 |
| valuation | valuer_partner_id | partner | Many to 0 or 1 |
| score | account_id | loan_account | Many to 0 or 1 |
| score | case_id | recovery_case | Many to 0 or 1 |

## T4. State machines and workflow

No case state machine of its own; the module acts on events from P3 and writes through the decision log.

## T5. Integration and interfaces

### T5.1 External system interfaces

| ID | System | Direction | Approach | Frequency |
|---|---|---|---|---|
| None | | | | |

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
| REQ-S1-001 | FEAT-VAL-01 | Written one epic ahead | With the story |
| REQ-S1-002 | FEAT-VAL-01 | Written one epic ahead | With the story |
| REQ-S1-003 | FEAT-VAL-01 | Written one epic ahead | With the story |
| REQ-S1-004 | FEAT-VAL-01 | Written one epic ahead | With the story |
| REQ-S1-005 | FEAT-VAL-01 | Written one epic ahead | With the story |
| REQ-S1-006 | FEAT-VAL-01 | Written one epic ahead | With the story |
| REQ-S1-007 | FEAT-VAL-01 | Written one epic ahead | With the story |
| REQ-S1-008 | FEAT-VAL-01 | Written one epic ahead | With the story |

## Appendix T-A. API specification

### T-A.1 Endpoint inventory

| ID | Method | Path | Access | First in |
|---|---|---|---|---|
| API-S1-001 | POST | /api/recovery/v1/cases/{caseId}/route | Treatment and offer U | E4 |

### T-A.2 Endpoint detail

#### API-S1-001 POST /cases/{caseId}/route

| Item | Value |
|---|---|
| Purpose | Submit the route decision for approval, with an override reason where it departs from the recommendation |
| Request | RouteRequest |
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
