<!-- source: 05 Technical architecture/Recovery Workbench Technical Specifications by Module v4.zip!Recovery Workbench TSD P4 Access and administration v2.md -->
<!-- converted: 2026-11-16 from Markdown (extracted) -->

> **Source:** `05 Technical architecture/Recovery Workbench Technical Specifications by Module v4.zip!Recovery Workbench TSD P4 Access and administration v2.md`  
> **Converted from:** Markdown (extracted)

# Recovery Workbench P4 Access and administration

Technical specification. SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd

## Document control

| Attribute | Value |
|---|---|
| Document title | TSD P4 Access and administration |
| Document ID | P4-RWB-TSD-v2 |
| Version | 2 |
| Status | In review |
| Date | 28 October 2026 |
| TSD owner | Solution architect |
| Build squad | TechX recovery squads |

| Document | Type | Relationship |
|---|---|---|
| Recovery Workbench FSD P4 Access and administration | FSD | Pair |
| Recovery Workbench Target Architecture | Architecture | Parent |
| Recovery Workbench Logical Data Model and Data Dictionary | Data | Source of T3 |
| Recovery Workbench API Specification | API | Source of appendix T-A |

## Existing capability check

| Capability | Verdict | Owning document | Note |
|---|---|---|---|
| Sign-in, access check, audit, PII and SOC logging | REUSE | ACE common module | Called through the published interface |
| Scheduler and batch | REUSE | ACE pattern: Quartz and Spring Batch | Jobs in the Batch and Scheduling Design |
| Outbox and retry | REUSE | Error Handling and Resilience Standard | Through P2 |
| Rules evaluation | NEW | Rules Engine Design | Decision table evaluator |

## T1. Architecture overview

P4 Access and administration is part of the recovery module in the ACE service: one service, one repository, one front end. It covers: roles, permissions, scope, masking, delegation of authority table, access log. It reaches other modules only through their published interfaces and other systems only through COLLINS, file loads and the ACE paths.

## T2. Component design

| Component | Responsibility |
|---|---|
| AccessAndAdministrationController | REST endpoints in appendix T-A; validation; maps errors to problem responses |
| AccessAndAdministrationService | Business logic; calls the rules component; writes the decision log entry before any change |
| AccessAndAdministrationRepository | Reads and writes the module's tables only |
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

**role** (EXTEND ACE RBAC). A Workbench role, held as data.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-REF-034 | id | TEXT | uuid | Yes | None | Workbench |
| DF-REF-035 | role_code | TEXT | varchar(20) | Yes | None | Workbench |
| DF-REF-036 | role_name | TEXT | varchar(80) | Yes | None | Workbench |
| DF-REF-037 | role_class | LOV | varchar(15) | Yes | LOV-ROLE-CLASS | Workbench |
| DF-REF-038 | default_scope | LOV | varchar(8) | Yes | LOV-SCOPE | Workbench |
| DF-REF-039 | entra_group | TEXT | varchar(120) | No | None | Entra ID |

**permission** (EXTEND ACE RBAC). What a role may do in one capability area.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-REF-040 | id | TEXT | uuid | Yes | None | Workbench |
| DF-REF-041 | role_id | CROSS_REF | uuid | Yes | None | Workbench |
| DF-REF-042 | capability_area | LOV | varchar(30) | Yes | LOV-CAPABILITY | Workbench |
| DF-REF-043 | letters | TEXT | varchar(5) | Yes | None | Workbench |
| DF-REF-044 | matrix_version | TEXT | varchar(20) | Yes | None | Workbench |

**delegation_limit** (NEW). An approval limit by decision, level, product and amount.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-REF-016 | id | TEXT | uuid | Yes | None | Workbench |
| DF-REF-017 | decision_code | LOV | varchar(8) | Yes | LOV-DECISION | Workbench |
| DF-REF-018 | approval_level | LOV | varchar(4) | Yes | LOV-APPROVAL-LEVEL | Workbench |
| DF-REF-019 | product_group | LOV | varchar(15) | Yes | LOV-PRODUCT | Workbench |
| DF-REF-020 | principal_limit | NUMBER | numeric(18,2) | No | None | Workbench |
| DF-REF-021 | loss_pct_limit | NUMBER | numeric(5,2) | No | None | Workbench |
| DF-REF-022 | min_price_pct_fmv | NUMBER | numeric(5,2) | No | None | Workbench |
| DF-REF-023 | holder_user_id | USER_REF | uuid | No | None | Workbench |
| DF-REF-024 | substitute_user_id | USER_REF | uuid | No | None | Workbench |
| DF-REF-025 | valid_from | DATE | date | Yes | None | Workbench |
| DF-REF-026 | valid_to | DATE | date | No | None | Workbench |
| DF-REF-055 | limit_version | TEXT | varchar(20) | Yes | None | Workbench |
| DF-REF-056 | regulation_item | TEXT | varchar(10) | Yes | None | Workbench |
| DF-REF-057 | applies_when | TEXT | varchar(40) | No | None | Workbench |
| DF-REF-058 | max_loss_amount | NUMBER | numeric(18,2) | No | None | Workbench |
| DF-REF-059 | max_delay_count | NUMBER | integer | No | None | Workbench |
| DF-REF-060 | min_price_pct_principal | NUMBER | numeric(5,2) | No | None | Workbench |
| DF-REF-061 | min_received_pct | NUMBER | numeric(5,2) | No | None | Workbench |
| DF-REF-062 | max_term_years | NUMBER | numeric(4,1) | No | None | Workbench |

**lov_value** (NEW). A value in a list of values.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-REF-027 | id | TEXT | uuid | Yes | None | Workbench |
| DF-REF-028 | lov_code | TEXT | varchar(30) | Yes | None | Workbench |
| DF-REF-029 | value_code | TEXT | varchar(30) | Yes | None | Workbench |
| DF-REF-030 | label_en | TEXT | varchar(120) | Yes | None | Workbench |
| DF-REF-031 | label_th | TEXT | varchar(120) | No | None | Workbench |
| DF-REF-032 | sort_order | NUMBER | integer | Yes | None | Workbench |
| DF-REF-033 | valid_from | DATE | date | Yes | None | Workbench |

**rule_row** (NEW). One versioned routing rule or sentry.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-REF-001 | id | TEXT | uuid | Yes | None | Workbench |
| DF-REF-002 | rule_id | TEXT | varchar(20) | Yes | None | Workbench |
| DF-REF-003 | rule_version | TEXT | varchar(20) | Yes | None | Workbench |
| DF-REF-004 | route_set | LOV | varchar(15) | Yes | LOV-ROUTE-SET | Workbench |
| DF-REF-005 | from_state | TEXT | varchar(60) | Yes | None | Workbench |
| DF-REF-006 | event_code | TEXT | varchar(60) | Yes | None | Workbench |
| DF-REF-007 | condition_expr | TEXT | varchar(1000) | No | None | Workbench |
| DF-REF-008 | action_text | TEXT | varchar(1000) | Yes | None | Workbench |
| DF-REF-009 | to_state | TEXT | varchar(60) | Yes | None | Workbench |
| DF-REF-010 | owner_role | LOV | varchar(20) | Yes | LOV-ROLE | Workbench |
| DF-REF-011 | timer_spec | TEXT | varchar(60) | No | None | Workbench |
| DF-REF-012 | valid_from | DATE | date | Yes | None | Workbench |
| DF-REF-013 | valid_to | DATE | date | No | None | Workbench |
| DF-REF-014 | approved_by | USER_REF | uuid | Yes | None | Workbench |
| DF-REF-015 | test_case_id | TEXT | varchar(20) | Yes | None | Workbench |
| DF-REF-052 | rule_table | LOV | varchar(15) | No | LOV-RULE-TABLE | Workbench |
| DF-REF-053 | row_order | NUMBER | integer | No | None | Workbench |
| DF-REF-054 | target_queue_code | TEXT | varchar(30) | No | None | Workbench |

**masking_rule** (NEW). Which role sees which personal data field unmasked, by version.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-REF-198 | id | TEXT | uuid | Yes | None | Workbench |
| DF-REF-199 | role_code | LOV | varchar(20) | Yes | LOV-ROLE | Workbench |
| DF-REF-200 | field_id | TEXT | varchar(16) | Yes | None | Workbench |
| DF-REF-201 | unmasked | BOOLEAN | boolean | Yes | None | Workbench |
| DF-REF-202 | masking_version | TEXT | varchar(20) | Yes | None | Workbench |
| DF-REF-203 | valid_from | DATE | date | Yes | None | Workbench |
| DF-REF-204 | valid_to | DATE | date | No | None | Workbench |

**role_conflict** (NEW). A pair of roles one person may not hold together, by version.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-REF-205 | id | TEXT | uuid | Yes | None | Workbench |
| DF-REF-206 | role_code | LOV | varchar(20) | Yes | LOV-ROLE | Workbench |
| DF-REF-207 | conflicts_with | TEXT | varchar(30) | Yes | None | Workbench |
| DF-REF-208 | reason | TEXT | varchar(200) | Yes | None | Workbench |
| DF-REF-209 | conflict_version | TEXT | varchar(20) | Yes | None | Workbench |
| DF-REF-210 | valid_from | DATE | date | Yes | None | Workbench |
| DF-REF-211 | valid_to | DATE | date | No | None | Workbench |

**partner_user** (NEW). A partner user's identity bound to one partner firm and one partner role.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-REF-212 | id | TEXT | uuid | Yes | None | Workbench |
| DF-REF-213 | identity_ref | TEXT | varchar(64) | Yes | None | Workbench |
| DF-REF-214 | partner_id | CROSS_REF | uuid | Yes | None | Workbench |
| DF-REF-215 | role_code | LOV | varchar(20) | Yes | LOV-ROLE | Workbench |
| DF-REF-216 | valid_from | DATE | date | Yes | None | Workbench |
| DF-REF-217 | valid_to | DATE | date | No | None | Workbench |

### T3.2 Lists of values

| List | Values |
|---|---|
| LOV-APPROVAL-LEVEL | L1, L2, L3, L4, L5, L6 |
| LOV-CAPABILITY | CASE_RECORD, QUEUE_AND_ALLOCATION, TREATMENT_AND_OFFER, LITIGATION, ASSET_AND_DISPOSAL, DEBT_SALE, WRITE_OFF_AND_POSTING, DOCUMENTS, RULES_AND_PARAMETERS, REFERENCE_DATA, DECISION_LOG, PARTNER_PORTAL, REPORTING, PLATFORM_ADMINISTRATION |
| LOV-PRODUCT | MORTGAGE, HIRE_PURCHASE, SSME, UNSECURED |
| LOV-ROLE-CLASS | BANK_USER, PARTNER_USER, NON_HUMAN_ACTOR |
| LOV-ROUTE-SET | RESTRUCTURE, SETTLEMENT, DEED_IN_LIEU, GUARANTEE_CLAIM, LITIGATION, ASSET_DISPOSAL, DEBT_SALE, WRITE_OFF, DEVIATIONS, UNIVERSAL_RULES |
| LOV-RULE-TABLE | ENTRY, EXCLUSION, ALLOCATION, ASSIGNMENT, TRANSFER |
| LOV-SCOPE | OWN, TEAM, REGION, ALL |

### T3.3 Relationships

| From | To | Field | Cardinality |
|---|---|---|---|
| permission | role_id | role | Many to 1 |
| partner_user | partner_id | partner | Many to 1 |

## T4. State machines and workflow

No case state machine of its own; the module acts on events from P3 and writes through the decision log.

## T5. Integration and interfaces

### T5.1 External system interfaces

| ID | System | Direction | Approach | Frequency |
|---|---|---|---|---|
| INT-21 | Entra ID and the bank IAM | In | ACE sign-in | At each sign-in |
| INT-22 | PII Kafka, audit and SOC logs | Out | ACE logging | As they happen |

### T5.2 Cross-module interfaces

Calls go through the published Java interfaces: P3 for the case, P7 for the decision log, P4 for access and reference data, P5 for documents, P6 for notices.

### T5.3 Events

| Event | Direction |
|---|---|
| None | |

## T6. Security and access control

### T6.1 RBAC matrix

| Role | Rules and parameters | Reference data | Platform administration |
|---|---|---|---|
| RW-CASEOWN Case owner | R | R | - |
| RW-TEAMMGR Team manager | R | R | - |
| RW-PHONECOL Phone collector | - | R | - |
| RW-FIELDCOL Field collector | - | R | - |
| RW-RESTRUCT Restructuring officer (FCR) | R | R | - |
| RW-SPECIAL Hardship and vulnerability specialist | R | R | - |
| RW-COMPLAIN Complaint officer | R | R | - |
| RW-FRAUD Fraud investigator | R | R | - |
| RW-LITOFF Litigation officer | R | R | - |
| RW-ENFORCE Enforcement owner | R | R | - |
| RW-LEGAL Legal counsel | R | RU | - |
| RW-SALEOFF Sale officer | R | R | - |
| RW-NPAMGR NPA and asset manager | R | R | - |
| RW-DEBTSALE Debt sale officer | R | R | - |
| RW-WRITEOFF Write-off team member | R | R | - |
| RW-CREDITAD Credit Administration officer | R | R | - |
| RW-GUARANT Guarantee officer | R | R | - |
| RW-AGENCYMG Partner and agency manager | R | RU | - |
| RW-CONDUCT Conduct and QA officer | R | R | - |
| RW-CAPACITY Capacity and workforce planner | R | R | - |
| RW-PRODHEAD Product head (Mortgage, HP, SSME) | R | R | - |
| RW-HEADLIT Head of Litigation | R | R | - |
| RW-HEADNPA Head of NPA | R | R | - |
| RW-HEADASL Head of Asset Liquidity | R | R | - |
| RW-CREDCOMM Credit approval committee member | R | R | - |
| RW-WOCOMM Write-off committee member | R | R | - |
| RW-RISK Risk and model risk officer | RA | R | - |
| RW-COE Center of excellence analyst | CRUD | CRUD | R |
| RW-DATASTEW Data steward and data product owner | R | RU | R |
| RW-FINANCE Finance and CFO delegate | R | R | - |
| RW-AUDIT Internal audit | R | R | R |
| RW-COMPLY Compliance and PDPA officer | R | RU | R |
| RW-PLATADM Platform administrator | R | R | CRUD |
| RW-REFADM Reference data administrator | R | CRUD | - |
| RW-SECADM Security administrator | R | R | CRUDA |
| RW-BIANAL Reporting and BI analyst | R | R | - |
| RW-TRIBE Tribe lead and squad members | R | R | - |
| SY-CASEWF Case workflow module | R | R | - |
| SY-RULES Rules component | R | R | - |
| SY-DATALOAD Data load from COLLINS | - | R | - |
| SY-OCR OCR and extraction pipeline | - | R | - |
| SY-AGENT Agent platform | R | R | - |

### T6.2 Authentication and authorization

Entra ID single sign-on through the ACE front end; each endpoint declares its capability area and right; scope filters every query; masking applies to personal fields; service identities for jobs and agents.

## T7. Non-functional requirements

| ID | Requirement | Target | Status |
|---|---|---|---|
| NFR-039 | Party identifiers are masked at rest in the case store, and on every screen and every agent call, by role. | Masked at rest and in use | Proposed |
| NFR-040 | Each screen and each agent receives only the personal data it needs. | Data minimization per screen and per agent | Proposed |
| NFR-041 | The debt sale data tape is masked before it reaches the data room. | Masked tape | Proposed |
| NFR-042 | Every read of the case store, the document store and the data lake copy is logged. | Every read | Proposed |
| NFR-043 | A data subject access, correction or erasure request is answered inside the statutory period. | Statutory period, Not set as a working service level | Open, DL26 |
| NFR-044 | Consent state per channel is held and applied, and statutory notices continue when consent is withdrawn. | Applied on every send | Proposed |
| NFR-045 | No production data is used in the development environment, and the user acceptance environment uses masked copies. | Synthetic in development, masked in user acceptance | Proposed |
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
| REQ-ACA-001 | FEAT-ACA-01 | RWB-E1-022 | TC-E1-022-01 |
| REQ-ACA-002 | FEAT-ACA-01 | RWB-E1-022 | TC-E1-022-01 |
| REQ-ACA-003 | FEAT-ACA-01 | RWB-E1-022 | TC-E1-022-01 |
| REQ-ACA-004 | FEAT-ACA-01 | RWB-E1-022 | TC-E1-022-01 |
| REQ-ACA-005 | FEAT-ACA-01 | RWB-E1-022 | TC-E1-022-01 |
| REQ-ACA-006 | FEAT-ACA-01 | RWB-E1-022 | TC-E1-022-01 |
| REQ-ACA-007 | FEAT-ACA-01 | RWB-E1-022 | TC-E1-022-01 |
| REQ-ACA-008 | FEAT-ACA-01 | RWB-E1-022 | TC-E1-022-01 |
| REQ-ACA-009 | FEAT-ACA-01 | RWB-E1-022 | TC-E1-022-01 |
| REQ-ACA-010 | FEAT-ACA-01 | RWB-E1-022 | TC-E1-022-01 |
| REQ-ACA-011 | None | Written one epic ahead | With the story |
| REQ-ACA-012 | None | Written one epic ahead | With the story |
| REQ-ACA-013 | FEAT-ADM-01 | Written one epic ahead | With the story |

## Appendix T-A. API specification

### T-A.1 Endpoint inventory

| ID | Method | Path | Access | First in |
|---|---|---|---|---|
| API-P4-001 | GET | /api/recovery/v1/admin/rule-versions | Rules and parameters R | E1 |
| API-P4-002 | POST | /api/recovery/v1/admin/rule-versions | Rules and parameters C | E1 |
| API-P4-003 | POST | /api/recovery/v1/admin/rule-versions/{versionId}/approve | Rules and parameters A | E1 |
| API-P4-004 | GET | /api/recovery/v1/admin/lists/{listCode} | Reference data R | E1 |
| API-P4-005 | POST | /api/recovery/v1/admin/reference-loads | Reference data C | E1 |
| API-P4-006 | POST | /api/recovery/v1/admin/reference-loads/{loadId}/approve | Reference data A | E1 |
| API-P4-007 | GET | /api/recovery/v1/admin/roles | Platform administration R | E1 |
| API-P4-008 | GET | /api/recovery/v1/admin/access-log | Platform administration R | E1 |
| API-P4-009 | POST | /api/recovery/v1/admin/reference-loads/{loadId}/verify | Reference data U | E1 |
| API-P4-010 | POST | /api/recovery/v1/admin/reference-loads/{loadId}/rollback | Reference data U | E1 |
| API-P4-011 | POST | /api/recovery/v1/admin/rule-versions/{versionId}/rollback | Rules and parameters U | E1 |
| API-P4-012 | GET | /api/recovery/v1/me/session | None R | E1 |
| API-P4-013 | POST | /api/recovery/v1/admin/break-glass-grants | Platform administration C | E1 |

### T-A.2 Endpoint detail

#### API-P4-001 GET /admin/rule-versions

| Item | Value |
|---|---|
| Purpose | List rule versions by route set with status and valid from date |
| Request | Query: routeSet, status |
| Response | RuleVersion[] |
| Errors | 401, 403, 503 |
| Authorization | Rules and parameters, right R, scope applied |
| Idempotency | Not applicable |

#### API-P4-002 POST /admin/rule-versions

| Item | Value |
|---|---|
| Purpose | Load a new rule version from a validated file |
| Request | Multipart: file, routeSet, validFrom |
| Response | RuleVersion |
| Errors | 401, 403, 409, 422, 503 |
| Authorization | Rules and parameters, right C, scope applied |
| Idempotency | Idempotency-Key header |

#### API-P4-003 POST /admin/rule-versions/{versionId}/approve

| Item | Value |
|---|---|
| Purpose | Approve a loaded rule version |
| Request | None |
| Response | RuleVersion |
| Errors | 401, 403, 404, 409, 503 |
| Authorization | Rules and parameters, right A, scope applied |
| Idempotency | Idempotency-Key header |

#### API-P4-004 GET /admin/lists/{listCode}

| Item | Value |
|---|---|
| Purpose | Read a list of values with its versions |
| Request | None |
| Response | ListOfValues |
| Errors | 401, 403, 404, 503 |
| Authorization | Reference data, right R, scope applied |
| Idempotency | Not applicable |

#### API-P4-005 POST /admin/reference-loads

| Item | Value |
|---|---|
| Purpose | Load reference data: lists, queues, timers, templates, delegation limits |
| Request | Multipart: file, table, validFrom |
| Response | ReferenceLoad |
| Errors | 401, 403, 409, 422, 503 |
| Authorization | Reference data, right C, scope applied |
| Idempotency | Idempotency-Key header |

#### API-P4-006 POST /admin/reference-loads/{loadId}/approve

| Item | Value |
|---|---|
| Purpose | Approve a reference data load |
| Request | None |
| Response | ReferenceLoad |
| Errors | 401, 403, 404, 409, 503 |
| Authorization | Reference data, right A, scope applied |
| Idempotency | Idempotency-Key header |

#### API-P4-007 GET /admin/roles

| Item | Value |
|---|---|
| Purpose | List roles with permissions and scope |
| Request | None |
| Response | Role[] |
| Errors | 401, 403, 503 |
| Authorization | Platform administration, right R, scope applied |
| Idempotency | Not applicable |

#### API-P4-008 GET /admin/access-log

| Item | Value |
|---|---|
| Purpose | Search the access log |
| Request | Query: user, from, to, event, page, size |
| Response | AccessLogPage |
| Errors | 401, 403, 503 |
| Authorization | Platform administration, right R, scope applied |
| Idempotency | Not applicable |

#### API-P4-009 POST /admin/reference-loads/{loadId}/verify

| Item | Value |
|---|---|
| Purpose | Record the verification of a reference data version after its valid from date |
| Request | VerifyRequest |
| Response | ReferenceLoad |
| Errors | 401, 403, 404, 409, 422, 503 |
| Authorization | Reference data, right U, scope applied |
| Idempotency | Idempotency-Key header |

#### API-P4-010 POST /admin/reference-loads/{loadId}/rollback

| Item | Value |
|---|---|
| Purpose | Roll back an approved reference data version to the version before it |
| Request | RollbackRequest |
| Response | ReferenceLoad |
| Errors | 401, 403, 404, 409, 422, 503 |
| Authorization | Reference data, right U, scope applied |
| Idempotency | Idempotency-Key header |

#### API-P4-011 POST /admin/rule-versions/{versionId}/rollback

| Item | Value |
|---|---|
| Purpose | Roll back a rule version in force to the previous version of the same rule table |
| Request | RollbackRequest |
| Response | RuleVersion |
| Errors | 401, 403, 404, 409, 422, 503 |
| Authorization | Rules and parameters, right U, scope applied |
| Idempotency | Idempotency-Key header |

#### API-P4-012 GET /me/session

| Item | Value |
|---|---|
| Purpose | Read the caller's resolved session: roles, scope, matrix and conflict versions, partner and break-glass state |
| Request | None |
| Response | Session |
| Errors | 401, 503 |
| Authorization | None, right R, scope applied |
| Idempotency | Not applicable |

#### API-P4-013 POST /admin/break-glass-grants

| Item | Value |
|---|---|
| Purpose | Activate a break-glass grant approved in the bank IAM for an open incident, area, right, scope and reason |
| Request | BreakGlassActivation |
| Response | BreakGlassGrant |
| Errors | 401, 403, 409, 422, 503 |
| Authorization | Platform administration, right C, scope applied |
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
