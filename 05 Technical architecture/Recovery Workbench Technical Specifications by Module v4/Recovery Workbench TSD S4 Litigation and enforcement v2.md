# Recovery Workbench S4 Litigation and enforcement

Technical specification. SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd

## Document control

| Attribute | Value |
|---|---|
| Document title | TSD S4 Litigation and enforcement |
| Document ID | S4-RWB-TSD-v2 |
| Version | 2 |
| Status | In review |
| Date | 28 October 2026 |
| TSD owner | Solution architect |
| Build squad | TechX recovery squads |

| Document | Type | Relationship |
|---|---|---|
| Recovery Workbench FSD S4 Litigation and enforcement | FSD | Pair |
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

S4 Litigation and enforcement is part of the recovery module in the ACE service: one service, one repository, one front end. It covers: notices, law firm instruction, hearings, judgment, enforcement. It reaches other modules only through their published interfaces and other systems only through COLLINS, file loads and the ACE paths.

## T2. Component design

| Component | Responsibility |
|---|---|
| LitigationAndEnforcementController | REST endpoints in appendix T-A; validation; maps errors to problem responses |
| LitigationAndEnforcementService | Business logic; calls the rules component; writes the decision log entry before any change |
| LitigationAndEnforcementRepository | Reads and writes the module's tables only |
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

**legal_action** (NEW). A notice, lawsuit, appeal, enforcement or bankruptcy action on a case.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-LEG-001 | id | TEXT | uuid | Yes | None | Workbench |
| DF-LEG-002 | case_id | CROSS_REF | uuid | Yes | None | Workbench |
| DF-LEG-003 | law_firm_id | CROSS_REF | uuid | No | None | Workbench |
| DF-LEG-004 | action_type | LOV | varchar(20) | Yes | LOV-LEGAL-TYPE | Workbench |
| DF-LEG-005 | lawsuit_no | TEXT | varchar(30) | No | None | LIT |
| DF-LEG-006 | black_case_no | TEXT | varchar(30) | No | None | LIT |
| DF-LEG-007 | red_case_no | TEXT | varchar(30) | No | None | LIT |
| DF-LEG-008 | court_name | TEXT | varchar(120) | No | None | LIT |
| DF-LEG-009 | claim_amount | NUMBER | numeric(18,2) | No | None | LIT |
| DF-LEG-010 | filed_date | DATE | date | No | None | LIT |
| DF-LEG-011 | judgment_date | DATE | date | No | None | LIT |
| DF-LEG-012 | judgment_amount | NUMBER | numeric(18,2) | No | None | LIT |
| DF-LEG-013 | lit_status | TEXT | varchar(200) | No | None | LIT via COLLINS |
| DF-LEG-014 | status | LOV | varchar(15) | Yes | LOV-LEGAL-STATUS | Workbench |

**hearing** (NEW). A court hearing on a legal action.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-LEG-024 | id | TEXT | uuid | Yes | None | Workbench |
| DF-LEG-025 | legal_action_id | CROSS_REF | uuid | Yes | None | Workbench |
| DF-LEG-026 | hearing_date | DATE | timestamptz | Yes | None | LIT |
| DF-LEG-027 | hearing_type | LOV | varchar(20) | No | LOV-HEARING | LIT |
| DF-LEG-028 | outcome | LOV | varchar(20) | No | LOV-HEARING-OUTCOME | Workbench |
| DF-LEG-029 | next_date | DATE | timestamptz | No | None | LIT |

### T3.2 Lists of values

| List | Values |
|---|---|
| LOV-HEARING | FIRST_HEARING, WITNESS, JUDGMENT_READING, MEDIATION |
| LOV-HEARING-OUTCOME | HELD, ADJOURNED, SETTLED, JUDGMENT |
| LOV-LEGAL-STATUS | OPEN, FILED, JUDGMENT, ENFORCING, CLOSED, WITHDRAWN |
| LOV-LEGAL-TYPE | NOTICE, CIVIL_CASE, APPEAL, ENFORCEMENT, BANKRUPTCY_PETITION, LED_AUCTION |

### T3.3 Relationships

| From | To | Field | Cardinality |
|---|---|---|---|
| legal_action | case_id | recovery_case | Many to 1 |
| legal_action | law_firm_id | partner | Many to 0 or 1 |
| hearing | legal_action_id | legal_action | Many to 1 |

## T4. State machines and workflow

**LITIGATION.** 79 rules over 38 states. The full table is in the Business Rules and Routing Logic workbook.

| Rule | From | Event | To |
|---|---|---|---|
| R-LIT-01 | LIT_ROUTE_APPROVED | ROUTE_APPROVED | NOTICE_GENERATED |
| R-LIT-02 | LIT_ROUTE_APPROVED | TREATMENT_BROKEN | NOTICE_GENERATED |
| R-LIT-03 | NOTICE_GENERATED | TEMPLATE_SELECTED | NOTICE_DISPATCHED |
| R-LIT-04 | NOTICE_GENERATED | TEMPLATE_WITHDRAWN | NOTICE_BLOCKED |
| R-LIT-05 | NOTICE_GENERATED | CONTACT_STOP_APPLIED | NOTICE_BLOCKED |
| R-LIT-06 | NOTICE_BLOCKED | TEMPLATE_REPLACED | NOTICE_GENERATED |
| R-LIT-07 | NOTICE_DISPATCHED | PROOF_OF_DELIVERY_RECEIVED | WITH_CUSTOMER_NOTICE_PERIOD |
| R-LIT-08 | NOTICE_DISPATCHED | PROOF_WINDOW_EXPIRED | NOTICE_UNSERVED |
| R-LIT-09 | NOTICE_DISPATCHED | DELIVERY_FAILED | NOTICE_UNSERVED |
| R-LIT-10 | NOTICE_UNSERVED | ALTERNATE_SERVICE_ORDERED | NOTICE_DISPATCHED |
| R-LIT-11 | NOTICE_UNSERVED | PRESCRIPTION_WARNING | PACK_ASSEMBLY |
| R-LIT-12 | WITH_CUSTOMER_NOTICE_PERIOD | CUSTOMER_PAID_IN_FULL | CASE_CLOSED |
| R-LIT-13 | WITH_CUSTOMER_NOTICE_PERIOD | CUSTOMER_REQUESTED_TREATMENT | TO_TREATMENT |
| R-LIT-14 | WITH_CUSTOMER_NOTICE_PERIOD | CUSTOMER_DISPUTED | DEVIATION_HOLD |
| R-LIT-15 | WITH_CUSTOMER_NOTICE_PERIOD | NOTICE_PERIOD_EXPIRED | PACK_ASSEMBLY |
| R-LIT-16 | PACK_ASSEMBLY | PACK_COMPLETE | PACK_VERIFIED |
| R-LIT-17 | PACK_ASSEMBLY | PACK_INCOMPLETE | PACK_DEFECT_HOLD |
| R-LIT-18 | PACK_DEFECT_HOLD | DOCUMENT_RETRIEVED | PACK_ASSEMBLY |
| R-LIT-19 | PACK_DEFECT_HOLD | DOCUMENT_UNRECOVERABLE | PACK_VERIFIED |
| R-LIT-20 | PACK_DEFECT_HOLD | PRESCRIPTION_WARNING | PACK_VERIFIED |
| R-LIT-21 | PACK_VERIFIED | OFFICER_REJECTED_PACK | PACK_ASSEMBLY |
| R-LIT-22 | PACK_VERIFIED | CONDUCT_CHECK_FAILED | NOTICE_BLOCKED |
| R-LIT-23 | PACK_VERIFIED | PACK_APPROVED | FIRM_SELECTION |
| R-LIT-24 | FIRM_SELECTION | FIRM_MATCHED | FIRM_INSTRUCTED |
| R-LIT-25 | FIRM_SELECTION | NO_FIRM_AVAILABLE | FIRM_ESCALATED |
| and 54 more | | | |

## T5. Integration and interfaces

### T5.1 External system interfaces

| ID | System | Direction | Approach | Frequency |
|---|---|---|---|---|
| INT-09 | LIT | In | COLLINS batch | Daily, end of day |
| INT-33 | Legal Execution Department and courts | In | Through the law firms in the partner portal | As entered |

### T5.2 Cross-module interfaces

Calls go through the published Java interfaces: P3 for the case, P7 for the decision log, P4 for access and reference data, P5 for documents, P6 for notices.

### T5.3 Events

| Event | Direction |
|---|---|
| None | |

## T6. Security and access control

### T6.1 RBAC matrix

| Role | Litigation |
|---|---|
| RW-CASEOWN Case owner | R |
| RW-TEAMMGR Team manager | R |
| RW-COMPLAIN Complaint officer | R |
| RW-FRAUD Fraud investigator | R |
| RW-LITOFF Litigation officer | CRUA |
| RW-ENFORCE Enforcement owner | CRU |
| RW-LEGAL Legal counsel | RA |
| RW-SALEOFF Sale officer | R |
| RW-NPAMGR NPA and asset manager | R |
| RW-DEBTSALE Debt sale officer | R |
| RW-WRITEOFF Write-off team member | R |
| RW-CREDITAD Credit Administration officer | R |
| RW-GUARANT Guarantee officer | R |
| RW-AGENCYMG Partner and agency manager | R |
| RW-CONDUCT Conduct and QA officer | R |
| RW-PRODHEAD Product head (Mortgage, HP, SSME) | RA |
| RW-HEADLIT Head of Litigation | RA |
| RW-HEADNPA Head of NPA | R |
| RW-HEADASL Head of Asset Liquidity | R |
| RW-RISK Risk and model risk officer | R |
| RW-COE Center of excellence analyst | R |
| RW-AUDIT Internal audit | R |
| RW-COMPLY Compliance and PDPA officer | R |
| RW-BIANAL Reporting and BI analyst | R |
| RW-TRIBE Tribe lead and squad members | R |
| PT-LAWFIRM Law firm user | RU |
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
| REQ-S4-001 | FEAT-LIT-01 | Written one epic ahead | With the story |
| REQ-S4-002 | FEAT-LIT-01 | Written one epic ahead | With the story |
| REQ-S4-003 | FEAT-LIT-01 | Written one epic ahead | With the story |
| REQ-S4-004 | FEAT-LIT-01 | Written one epic ahead | With the story |
| REQ-S4-005 | FEAT-LIT-01 | Written one epic ahead | With the story |
| REQ-S4-006 | FEAT-LIT-01 | Written one epic ahead | With the story |
| REQ-S4-007 | FEAT-LIT-01 | Written one epic ahead | With the story |
| REQ-S4-008 | FEAT-LIT-01 | Written one epic ahead | With the story |
| REQ-S4-009 | FEAT-LIT-01 | Written one epic ahead | With the story |
| REQ-S4-010 | FEAT-LIT-01 | Written one epic ahead | With the story |

## Appendix T-A. API specification

### T-A.1 Endpoint inventory

| ID | Method | Path | Access | First in |
|---|---|---|---|---|
| API-S4-001 | POST | /api/recovery/v1/notices/{noticeId}/approve | Litigation A | E2 |
| API-S4-002 | POST | /api/recovery/v1/cases/{caseId}/legal-actions | Litigation C | E5 |
| API-S4-003 | GET | /api/recovery/v1/legal-actions/{legalActionId} | Litigation R | E5 |
| API-S4-004 | PATCH | /api/recovery/v1/legal-actions/{legalActionId} | Litigation U | E5 |
| API-S4-005 | POST | /api/recovery/v1/legal-actions/{legalActionId}/hearings | Litigation U | E5 |

### T-A.2 Endpoint detail

#### API-S4-001 POST /notices/{noticeId}/approve

| Item | Value |
|---|---|
| Purpose | Approve a generated notice for dispatch |
| Request | None |
| Response | Notice |
| Errors | 401, 403, 404, 409, 503 |
| Authorization | Litigation, right A, scope applied |
| Idempotency | Idempotency-Key header |

#### API-S4-002 POST /cases/{caseId}/legal-actions

| Item | Value |
|---|---|
| Purpose | Open a legal action and its pack |
| Request | LegalActionRequest |
| Response | LegalAction |
| Errors | 401, 403, 404, 409, 422, 503 |
| Authorization | Litigation, right C, scope applied |
| Idempotency | Idempotency-Key header |

#### API-S4-003 GET /legal-actions/{legalActionId}

| Item | Value |
|---|---|
| Purpose | Read a legal action with pack, instruction, hearings and judgment |
| Request | None |
| Response | LegalAction |
| Errors | 401, 403, 404, 503 |
| Authorization | Litigation, right R, scope applied |
| Idempotency | Not applicable |

#### API-S4-004 PATCH /legal-actions/{legalActionId}

| Item | Value |
|---|---|
| Purpose | Record a filing, judgment or enforcement step |
| Request | LegalActionUpdate |
| Response | LegalAction |
| Errors | 401, 403, 404, 409, 422, 503 |
| Authorization | Litigation, right U, scope applied |
| Idempotency | Not applicable |

#### API-S4-005 POST /legal-actions/{legalActionId}/hearings

| Item | Value |
|---|---|
| Purpose | Add a hearing date |
| Request | HearingRequest |
| Response | Hearing |
| Errors | 401, 403, 404, 422, 503 |
| Authorization | Litigation, right U, scope applied |
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
