<!-- source: 05 Technical architecture/Recovery Workbench Technical Specifications by Module v4.zip!Recovery Workbench TSD S8 Deviation handling v2.md -->
<!-- converted: 2026-11-16 from Markdown (extracted) -->

> **Source:** `05 Technical architecture/Recovery Workbench Technical Specifications by Module v4.zip!Recovery Workbench TSD S8 Deviation handling v2.md`  
> **Converted from:** Markdown (extracted)

# Recovery Workbench S8 Deviation handling

Technical specification. SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd

## Document control

| Attribute | Value |
|---|---|
| Document title | TSD S8 Deviation handling |
| Document ID | S8-RWB-TSD-v2 |
| Version | 2 |
| Status | In review |
| Date | 28 October 2026 |
| TSD owner | Solution architect |
| Build squad | TechX recovery squads |

| Document | Type | Relationship |
|---|---|---|
| Recovery Workbench FSD S8 Deviation handling | FSD | Pair |
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

S8 Deviation handling is part of the recovery module in the ACE service: one service, one repository, one front end. It covers: x1 to X7: screening, pause, handling, return. It reaches other modules only through their published interfaces and other systems only through COLLINS, file loads and the ACE paths.

## T2. Component design

| Component | Responsibility |
|---|---|
| DeviationHandlingController | REST endpoints in appendix T-A; validation; maps errors to problem responses |
| DeviationHandlingService | Business logic; calls the rules component; writes the decision log entry before any change |
| DeviationHandlingRepository | Reads and writes the module's tables only |
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

**deviation** (NEW). A deviation X1 to X7 raised on a case.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-CAS-036 | id | TEXT | uuid | Yes | None | Workbench |
| DF-CAS-037 | case_id | CROSS_REF | uuid | Yes | None | Workbench |
| DF-CAS-038 | deviation_code | LOV | varchar(3) | Yes | LOV-DEVIATION | Workbench |
| DF-CAS-039 | raised_at | DATE | timestamptz | Yes | None | Workbench |
| DF-CAS-040 | raised_by | LOV | varchar(20) | Yes | LOV-RAISED-BY | Workbench |
| DF-CAS-041 | paused_state | TEXT | varchar(60) | Yes | None | Workbench |
| DF-CAS-042 | handler_user_id | USER_REF | uuid | No | None | Workbench |
| DF-CAS-043 | contact_stop | BOOLEAN | boolean | Yes | None | Workbench |
| DF-CAS-044 | cleared_at | DATE | timestamptz | No | None | Workbench |
| DF-CAS-045 | outcome | LOV | varchar(20) | No | LOV-DEV-OUTCOME | Workbench |

### T3.2 Lists of values

| List | Values |
|---|---|
| LOV-DEV-OUTCOME | RETURNED, RE_ROUTED, CASE_ENDED |
| LOV-DEVIATION | X1, X2, X3, X4, X5, X6, X7 |
| LOV-RAISED-BY | SCREENING_AGENT, RULE, OFFICER, CUSTOMER_CONTACT |

### T3.3 Relationships

| From | To | Field | Cardinality |
|---|---|---|---|
| deviation | case_id | recovery_case | Many to 1 |

## T4. State machines and workflow

**DEVIATION.** 22 rules over 9 states. The full table is in the Business Rules and Routing Logic workbook.

| Rule | From | Event | To |
|---|---|---|---|
| R-DEV-01 | ANY_STATE | DEVIATION_FLAGGED | DEV_FLAGGED |
| R-DEV-02 | DEV_FLAGGED | OWNER_ASSIGNED | DEV_WITH_OWNER |
| R-DEV-03 | DEV_FLAGGED | OWNER_ASSIGNED | DEV_WITH_OWNER |
| R-DEV-04 | DEV_FLAGGED | OWNER_ASSIGNED | DEV_WITH_OWNER |
| R-DEV-05 | DEV_FLAGGED | OWNER_ASSIGNED | DEV_WITH_OWNER |
| R-DEV-06 | DEV_FLAGGED | OWNER_ASSIGNED | DEV_WITH_OWNER |
| R-DEV-07 | DEV_FLAGGED | FLAG_REJECTED | DEV_REJECTED |
| R-DEV-08 | DEV_REJECTED | CLOCK_RESUMED | RESUMED |
| R-DEV-09 | DEV_WITH_OWNER | DEVIATION_RESOLVED | DEV_RESOLVED |
| R-DEV-10 | DEV_WITH_OWNER | DEVIATION_RESOLVED | DEV_REROUTE |
| R-DEV-11 | DEV_WITH_OWNER | INSURANCE_SETTLED | CASE_ENDED |
| R-DEV-12 | DEV_WITH_OWNER | ESTATE_CONFIRMED | DEV_REROUTE |
| R-DEV-13 | DEV_WITH_OWNER | FRAUD_CONFIRMED | DEV_REROUTE |
| R-DEV-14 | DEV_WITH_OWNER | FRAUD_NOT_CONFIRMED | DEV_REROUTE |
| R-DEV-15 | DEV_WITH_OWNER | BANKRUPTCY_FILED | DEV_REROUTE |
| R-DEV-16 | DEV_WITH_OWNER | CONTACT_RESTORED | DEV_RESOLVED |
| R-DEV-17 | DEV_WITH_OWNER | CONTACT_NOT_FOUND | DEV_REROUTE |
| R-DEV-18 | DEV_RESOLVED | CLOCK_RESUMED | RESUMED |
| R-DEV-19 | DEV_REROUTE | ROUTE_REOPENED | ROUTE_D6 |
| R-DEV-20 | DEV_WITH_OWNER | SLA_BREACHED | DEV_WITH_OWNER |
| R-DEV-21 | DEV_FLAGGED | OWNER_ASSIGNED | DEV_WITH_OWNER |
| R-DEV-22 | DEV_WITH_OWNER | DEVIATION_RESOLVED | DEV_REROUTE |

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
| DeviationRaised | Published |
| DeviationCleared | Published |

## T6. Security and access control

### T6.1 RBAC matrix

| Role | Case record |
|---|---|
| RW-CASEOWN Case owner | CRU |
| RW-TEAMMGR Team manager | R |
| RW-PHONECOL Phone collector | R |
| RW-FIELDCOL Field collector | R |
| RW-RESTRUCT Restructuring officer (FCR) | RU |
| RW-SPECIAL Hardship and vulnerability specialist | RU |
| RW-COMPLAIN Complaint officer | RU |
| RW-FRAUD Fraud investigator | RU |
| RW-LITOFF Litigation officer | RU |
| RW-ENFORCE Enforcement owner | RU |
| RW-LEGAL Legal counsel | R |
| RW-SALEOFF Sale officer | RU |
| RW-NPAMGR NPA and asset manager | R |
| RW-DEBTSALE Debt sale officer | RU |
| RW-WRITEOFF Write-off team member | R |
| RW-CREDITAD Credit Administration officer | R |
| RW-GUARANT Guarantee officer | RU |
| RW-AGENCYMG Partner and agency manager | R |
| RW-CONDUCT Conduct and QA officer | R |
| RW-CAPACITY Capacity and workforce planner | R |
| RW-PRODHEAD Product head (Mortgage, HP, SSME) | R |
| RW-HEADLIT Head of Litigation | R |
| RW-HEADNPA Head of NPA | R |
| RW-HEADASL Head of Asset Liquidity | R |
| RW-CREDCOMM Credit approval committee member | R |
| RW-WOCOMM Write-off committee member | R |
| RW-RISK Risk and model risk officer | R |
| RW-COE Center of excellence analyst | R |
| RW-DATASTEW Data steward and data product owner | R |
| RW-FINANCE Finance and CFO delegate | R |
| RW-AUDIT Internal audit | R |
| RW-COMPLY Compliance and PDPA officer | R |
| RW-PLATADM Platform administrator | R |
| RW-BIANAL Reporting and BI analyst | R |
| RW-TRIBE Tribe lead and squad members | R |
| PT-AGENCY Collection agency (OA) user | R |
| PT-LAWFIRM Law firm user | R |
| SY-CASEWF Case workflow module | CRU |
| SY-RULES Rules component | R |
| SY-DATALOAD Data load from COLLINS | CU |
| SY-OCR OCR and extraction pipeline | R |
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
| REQ-DVH-001 | FEAT-DVH-01 | RWB-E1-062 | TC-E1-062-01 |
| REQ-DVH-002 | FEAT-DVH-01 | RWB-E1-062 | TC-E1-062-01 |
| REQ-DVH-003 | FEAT-DVH-01 | RWB-E1-062 | TC-E1-062-01 |
| REQ-DVH-004 | FEAT-DVH-01 | RWB-E1-062 | TC-E1-062-01 |
| REQ-DVH-005 | FEAT-DVH-01 | RWB-E1-062 | TC-E1-062-01 |
| REQ-DVH-006 | FEAT-DVH-01 | RWB-E1-062 | TC-E1-062-01 |
| REQ-DVH-007 | FEAT-DVH-01 | RWB-E1-062 | TC-E1-062-01 |
| REQ-DVH-008 | None | Written one epic ahead | With the story |
| REQ-DVH-009 | FEAT-DVH-01 | RWB-E1-062 | TC-E1-062-01 |
| REQ-DVH-010 | FEAT-DVH-01 | RWB-E1-062 | TC-E1-062-01 |
| REQ-DVH-011 | FEAT-DVF-01 | Written one epic ahead | With the story |
| REQ-S8-001 | FEAT-DVF-01 | Written one epic ahead | With the story |
| REQ-S8-002 | FEAT-DVF-01 | Written one epic ahead | With the story |
| REQ-S8-003 | FEAT-DVF-01 | Written one epic ahead | With the story |
| REQ-S8-004 | FEAT-DVF-01 | Written one epic ahead | With the story |
| REQ-S8-005 | FEAT-DVF-01 | Written one epic ahead | With the story |
| REQ-S8-006 | FEAT-DVF-01 | Written one epic ahead | With the story |
| REQ-S8-007 | FEAT-DVF-01 | Written one epic ahead | With the story |

## Appendix T-A. API specification

### T-A.1 Endpoint inventory

| ID | Method | Path | Access | First in |
|---|---|---|---|---|
| API-S8-001 | POST | /api/recovery/v1/cases/{caseId}/deviations | Case record U | E2 |
| API-S8-002 | PATCH | /api/recovery/v1/deviations/{deviationId} | Case record U | E2 |

### T-A.2 Endpoint detail

#### API-S8-001 POST /cases/{caseId}/deviations

| Item | Value |
|---|---|
| Purpose | Raise a deviation X1 to X7 on the case |
| Request | DeviationRequest |
| Response | Deviation |
| Errors | 401, 403, 404, 409, 422, 503 |
| Authorization | Case record, right U, scope applied |
| Idempotency | Idempotency-Key header |

#### API-S8-002 PATCH /deviations/{deviationId}

| Item | Value |
|---|---|
| Purpose | Record the outcome of a deviation and return or re-route the case |
| Request | DeviationOutcome |
| Response | Deviation |
| Errors | 401, 403, 404, 409, 422, 503 |
| Authorization | Case record, right U, scope applied |
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
