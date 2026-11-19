# Recovery Workbench S1 Valuation and route

Technical specification. SCB Collections and Recovery. Henka Group, 15 November 2026.

(C) Siam Commercial Bank and Henka Pte Ltd

## Document control

| Attribute | Value |
|---|---|
| Document title | TSD S1 Valuation and route |
| Document ID | S1-RWB-TSD-v3 |
| Version | 3 |
| Status | In review |
| Date | 15 November 2026 |
| TSD owner | Solution architect |
| Build squad | TechX recovery squads |
| Decision | D-RCV-35 (U1 to U5), ADR-010 |

| Version | Date | Change |
|---|---|---|
| 2 | 28 October 2026 | Module specification with the Workbench valuation and score copies |
| 3 | 15 November 2026 | D-RCV-35: the appraisal is read from `v_ace_valuation` and the score from `v_ace_score`; the Workbench keeps only its decision in `valuation_ext`, keyed by `valuation_key`. The valuation and score copies leave the schema |

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

S1 Valuation and route is part of the recovery module in the ACE service: one service, one repository, one front end. It covers: the D6 route decision with COLLINS return by route and the route agent. It reaches other modules only through their published interfaces, and it reads appraisals and scores only through `recovery.v_ace_valuation` and `recovery.v_ace_score`.

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

The appraisal and the score are ACE records. S1 reads them and holds only its own decision about an appraisal. It has no valuation table and no score table, and it writes nothing to ACE.

**v_ace_valuation** (ACE, read-only; Section B). An SVAF appraisal as ingested into ACE and read through the view. Key: `valuation_key`. 9 fields.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-ACE-187 | valuation_key | TEXT | varchar(255) | Yes | None | ACE `valuation.valuation_key` |
| DF-ACE-188 | asset_key | TEXT | varchar(255) | No | None | ACE `valuation.asset_key` |
| DF-ACE-189 | appraisal_no | TEXT | varchar(20) | Yes | None | ACE `valuation.appraisal_no` |
| DF-ACE-190 | appraisal_type | LOV | varchar(15) | Yes | LOV-APPRAISAL | ACE `valuation.appraisal_type` |
| DF-ACE-191 | appraised_value | NUMBER | numeric(18,2) | Yes | None | ACE `valuation.appraised_value` |
| DF-ACE-192 | forced_sale_value | NUMBER | numeric(18,2) | No | None | ACE `valuation.forced_sale_value` |
| DF-ACE-193 | appraisal_date | DATE | date | Yes | None | ACE `valuation.appraisal_date` |
| DF-ACE-194 | source_system | TEXT | varchar(20) | Yes | None | ACE `valuation.source_system` (SVAF) |
| DF-ACE-195 | data_as_of | DATE | date | Yes | None | ACE `valuation.business_date` |

The view is Section B because ACE holds no appraisal today; it is created the week RWB-ACE-001 lands. Until then the valuation screens and the D6 route rule stay behind their flag. `accepted`, `stale_flag`, `age_days` and the valuer are Workbench decisions and are not in ACE.

**v_ace_score** (ACE, read-only; Section B). A COLLINS score, estimate and route as ingested into ACE. Key: `score_key`. 10 fields.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-ACE-270 | score_key | TEXT | varchar(255) | Yes | None | ACE `collins_score.score_key` |
| DF-ACE-271 | account_key | TEXT | varchar(255) | No | None | ACE `collins_score.account_key` |
| DF-ACE-272 | model_code | TEXT | varchar(30) | Yes | None | ACE `collins_score.model_code` |
| DF-ACE-273 | model_version | TEXT | varchar(20) | Yes | None | ACE `collins_score.model_version` |
| DF-ACE-274 | score_value | NUMBER | numeric(12,4) | No | None | ACE `collins_score.score_value` |
| DF-ACE-275 | estimate_value | NUMBER | numeric(18,2) | No | None | ACE `collins_score.estimate_value` |
| DF-ACE-276 | route_code | LOV | varchar(4) | No | LOV-ROUTE | ACE `collins_score.route_code` |
| DF-ACE-277 | scored_at | DATE | timestamptz | Yes | None | ACE `collins_score.scored_at` |
| DF-ACE-278 | source_system | TEXT | varchar(20) | Yes | None | ACE `collins_score.source_system` (COLLINS) |
| DF-ACE-279 | data_as_of | DATE | date | Yes | None | ACE `collins_score.business_date` |

The view is Section B. The route decision is recorded on the case (`recovery_case.route_code`, `route_state`), not on the score: the score is an input, the decision is Workbench-owned.

**valuation_ext** (NEW). The Workbench decision about an ACE appraisal. Key: `valuation_key`. A 1:1 table with `v_ace_valuation`.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-EXT-036 | valuation_key | TEXT | varchar(255) | Yes | None | ACE `v_ace_valuation.valuation_key` |
| DF-EXT-037 | accepted | BOOLEAN | boolean | Yes | None | Workbench |
| DF-EXT-038 | accepted_at | DATE | timestamptz | No | None | Workbench |
| DF-EXT-039 | accepted_by | CROSS_REF | uuid | No | None | Workbench |
| DF-EXT-040 | valuer_partner_id | CROSS_REF | uuid | No | None | Workbench |
| DF-EXT-041 | stale_flag | BOOLEAN | boolean | Yes | None | Workbench |
| DF-EXT-042 | age_days | NUMBER | integer | No | None | Workbench |

Plus the seven standard record columns, DF-EXT-043 to DF-EXT-049. A missing row means the appraisal is not accepted and is judged stale by its date alone.

The version 2 tables `valuation` and `score` leave Physical Schema v5. Their field IDs DF-COL-018 to DF-COL-027 and DF-DEC-019 to DF-DEC-027 are retired and not reused.

### T3.2 Lists of values

| List | Values |
|---|---|
| LOV-APPRAISAL | MARKET, OFFICIAL, FORCED_SALE, DESKTOP, AGENT_ESTIMATE |
| LOV-ROUTE | R1, R2, R3, R4, R5, R6, R7, R8 |

### T3.3 Relationships

| From | Field | To | Cardinality |
|---|---|---|---|
| valuation_ext | valuation_key | v_ace_valuation | One to one; business key, no foreign key |
| valuation_ext | valuer_partner_id | partner | Many to 0 or 1 |
| v_ace_valuation | asset_key | v_ace_asset | Many to 0 or 1; business key, no foreign key |
| v_ace_score | account_key | v_ace_account | Many to 0 or 1; business key, no foreign key |

No relationship here is a foreign key into ACE. A score or an appraisal that ACE has not ingested has no row to read, and the screen shows the last ACE business date rather than an empty value.

## T4. State machines and workflow

No case state machine of its own; the module acts on events from P3 and writes through the decision log.

## T5. Integration and interfaces

### T5.1 External system interfaces

| ID | System | Direction | Approach | Frequency |
|---|---|---|---|---|
| INT-08 | COLLINS models | In, into ACE | ACE ingestion (ACE team); S1 reads `v_ace_score` | Daily; monthly for some models |
| INT-11 | SVAF | In, into ACE | ACE ingestion (ACE team); S1 reads `v_ace_valuation` | Weekly |
| None | ACE database | In | `recovery.v_ace_valuation` and `recovery.v_ace_score`, SELECT only | As each ACE batch completes |

### T5.2 Cross-module interfaces

Calls go through the published Java interfaces: P3 for the case, P7 for the decision log, P4 for access and reference data, P5 for documents, P6 for notices.

### T5.3 Events

| Event | Direction |
|---|---|
| AceDataReady | Consumed: a new appraisal or score is readable |
| ValuationAccepted | Published: the Workbench accepted an appraisal in `valuation_ext` |

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
| DL06 | Which interfaces need same-day data. Option A (daily batch through COLLINS) is superseded by D-RCV-35 |
| DL11 | Non-functional target values |
| DL35 | Deployment slots |
| DL43 | ACE team acceptance of the RWB-ACE-001 scope and dates; blocks the Tier 2 views this module reads |

## Document sign-off

| Role | Name | Signature | Date |
|---|---|---|---|
| Solution architect | | | |
| Tech lead | | | |
| ACE team | | | |
| QA lead | | | |
