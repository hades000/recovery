# Recovery Workbench S7 Write-off and recovery

Technical specification. SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd

## Document control

| Attribute | Value |
|---|---|
| Document title | TSD S7 Write-off and recovery |
| Document ID | S7-RWB-TSD-v2 |
| Version | 2 |
| Status | In review |
| Date | 28 October 2026 |
| TSD owner | Solution architect |
| Build squad | TechX recovery squads |

| Document | Type | Relationship |
|---|---|---|
| Recovery Workbench FSD S7 Write-off and recovery | FSD | Pair |
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

S7 Write-off and recovery is part of the recovery module in the ACE service: one service, one repository, one front end. It covers: eligibility, committee, posting, recovery after charge-off. It reaches other modules only through their published interfaces and other systems only through COLLINS, file loads and the ACE paths.

## T2. Component design

| Component | Responsibility |
|---|---|
| Write-OffAndRecoveryController | REST endpoints in appendix T-A; validation; maps errors to problem responses |
| Write-OffAndRecoveryService | Business logic; calls the rules component; writes the decision log entry before any change |
| Write-OffAndRecoveryRepository | Reads and writes the module's tables only |
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

### T5.2 Cross-module interfaces

Calls go through the published Java interfaces: P3 for the case, P7 for the decision log, P4 for access and reference data, P5 for documents, P6 for notices.

### T5.3 Events

| Event | Direction |
|---|---|
| WriteOffApproved | Published |

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
| API-S7-001 | POST | /api/recovery/v1/write-off-scans | Write-off and posting C | E6 |
| API-S7-002 | POST | /api/recovery/v1/write-offs/{writeOffId}/committee-decision | Write-off and posting A | E6 |

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
