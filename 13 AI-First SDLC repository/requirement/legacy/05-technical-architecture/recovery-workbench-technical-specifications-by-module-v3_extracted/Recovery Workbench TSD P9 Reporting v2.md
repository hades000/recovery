<!-- source: 05 Technical architecture/Recovery Workbench Technical Specifications by Module v3.zip!Recovery Workbench TSD P9 Reporting v2.md -->
<!-- converted: 2026-11-04 from Markdown (extracted) -->

> **Source:** `05 Technical architecture/Recovery Workbench Technical Specifications by Module v3.zip!Recovery Workbench TSD P9 Reporting v2.md`  
> **Converted from:** Markdown (extracted)

# Recovery Workbench P9 Reporting

Technical specification. SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd

## Document control

| Attribute | Value |
|---|---|
| Document title | TSD P9 Reporting |
| Document ID | P9-RWB-TSD-v2 |
| Version | 2 |
| Status | In review |
| Date | 28 October 2026 |
| TSD owner | Solution architect |
| Build squad | TechX recovery squads |

| Document | Type | Relationship |
|---|---|---|
| Recovery Workbench FSD P9 Reporting | FSD | Pair |
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

P9 Reporting is part of the recovery module in the ACE service: one service, one repository, one front end. It covers: baseline measures, steering dashboard, operational and regulatory reports. It reaches other modules only through their published interfaces and other systems only through COLLINS, file loads and the ACE paths.

## T2. Component design

| Component | Responsibility |
|---|---|
| ReportingController | REST endpoints in appendix T-A; validation; maps errors to problem responses |
| ReportingService | Business logic; calls the rules component; writes the decision log entry before any change |
| ReportingRepository | Reads and writes the module's tables only |
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

**measure_definition** (NEW). The agreed definition of a reported measure, by version.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-RPT-031 | id | TEXT | uuid | Yes | None | Workbench |
| DF-RPT-032 | measure_code | TEXT | varchar(40) | Yes | None | Workbench |
| DF-RPT-033 | name | TEXT | varchar(120) | Yes | None | Workbench |
| DF-RPT-034 | formula | TEXT | varchar(1000) | Yes | None | Workbench |
| DF-RPT-035 | data_product | LOV | varchar(25) | Yes | LOV-DATA-PRODUCT | Workbench |
| DF-RPT-036 | unit | LOV | varchar(10) | Yes | LOV-MEASURE-UNIT | Workbench |
| DF-RPT-037 | definition_version | TEXT | varchar(20) | Yes | None | Workbench |
| DF-RPT-038 | approved_by | USER_REF | uuid | No | None | Workbench |
| DF-RPT-039 | approved_at | DATE | timestamptz | No | None | Workbench |
| DF-RPT-040 | valid_from | DATE | date | Yes | None | Workbench |

**measure_snapshot** (NEW). The value of one measure for a business date, product and dimension value.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-RPT-041 | id | TEXT | uuid | Yes | None | Workbench |
| DF-RPT-042 | measure_code | TEXT | varchar(40) | Yes | None | Workbench |
| DF-RPT-043 | definition_version | TEXT | varchar(20) | Yes | None | Workbench |
| DF-RPT-044 | business_date | DATE | date | Yes | None | Workbench |
| DF-RPT-045 | product_group | LOV | varchar(15) | No | LOV-PRODUCT | Workbench |
| DF-RPT-046 | dimension_code | LOV | varchar(20) | No | LOV-MEASURE-DIM | Workbench |
| DF-RPT-047 | dimension_value | TEXT | varchar(60) | No | None | Workbench |
| DF-RPT-048 | value | NUMBER | numeric(18,4) | Yes | None | Workbench |
| DF-RPT-049 | case_count | NUMBER | integer | No | None | Workbench |
| DF-RPT-050 | is_baseline | BOOLEAN | boolean | Yes | None | Workbench |
| DF-RPT-051 | frozen | BOOLEAN | boolean | Yes | None | Workbench |
| DF-RPT-052 | published_at | DATE | timestamptz | No | None | Workbench |

**measure_publish** (NEW). Whether the day's dashboard data set was published or held after reconciling to the case list.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-RPT-053 | id | TEXT | uuid | Yes | None | Workbench |
| DF-RPT-054 | business_date | DATE | date | Yes | None | Workbench |
| DF-RPT-055 | status | LOV | varchar(10) | Yes | LOV-MEASURE-PUBLISH | Workbench |
| DF-RPT-056 | case_list_count | NUMBER | integer | Yes | None | Workbench |
| DF-RPT-057 | dashboard_count | NUMBER | integer | Yes | None | Workbench |
| DF-RPT-058 | held_reason | TEXT | varchar(200) | No | None | Workbench |

### T3.2 Lists of values

| List | Values |
|---|---|
| LOV-DATA-PRODUCT | DP01, DP02, DP03, DP04, DP05, DP06, DP07, DP08, DP09, DP10, DP11, DP12, DP13, DP14 |
| LOV-MEASURE-DIM | ROUTE, AGE_BAND, QUEUE, STAGE, AGENT |
| LOV-MEASURE-PUBLISH | PUBLISHED, HELD |
| LOV-MEASURE-UNIT | COUNT, THB, DAYS, PERCENT |
| LOV-PRODUCT | MORTGAGE, HIRE_PURCHASE, SSME, UNSECURED |

### T3.3 Relationships

| From | To | Field | Cardinality |
|---|---|---|---|

## T4. State machines and workflow

No case state machine of its own; the module acts on events from P3 and writes through the decision log.

## T5. Integration and interfaces

### T5.1 External system interfaces

| ID | System | Direction | Approach | Frequency |
|---|---|---|---|---|
| INT-19 | Data lake and Power BI | Out | Daily batch | Daily |

### T5.2 Cross-module interfaces

Calls go through the published Java interfaces: P3 for the case, P7 for the decision log, P4 for access and reference data, P5 for documents, P6 for notices.

### T5.3 Events

| Event | Direction |
|---|---|
| None | |

## T6. Security and access control

### T6.1 RBAC matrix

| Role | Reporting |
|---|---|
| RW-CASEOWN Case owner | R |
| RW-TEAMMGR Team manager | R |
| RW-PHONECOL Phone collector | R |
| RW-RESTRUCT Restructuring officer (FCR) | R |
| RW-SPECIAL Hardship and vulnerability specialist | R |
| RW-COMPLAIN Complaint officer | R |
| RW-FRAUD Fraud investigator | R |
| RW-LITOFF Litigation officer | R |
| RW-ENFORCE Enforcement owner | R |
| RW-LEGAL Legal counsel | R |
| RW-SALEOFF Sale officer | R |
| RW-NPAMGR NPA and asset manager | R |
| RW-DEBTSALE Debt sale officer | R |
| RW-WRITEOFF Write-off team member | R |
| RW-CREDITAD Credit Administration officer | R |
| RW-GUARANT Guarantee officer | R |
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
| RW-DATASTEW Data steward and data product owner | CRU |
| RW-FINANCE Finance and CFO delegate | R |
| RW-AUDIT Internal audit | R |
| RW-COMPLY Compliance and PDPA officer | R |
| RW-PLATADM Platform administrator | R |
| RW-REFADM Reference data administrator | R |
| RW-SECADM Security administrator | R |
| RW-BIANAL Reporting and BI analyst | CRUD |
| RW-TRIBE Tribe lead and squad members | R |

### T6.2 Authentication and authorization

Entra ID single sign-on through the ACE front end; each endpoint declares its capability area and right; scope filters every query; masking applies to personal fields; service identities for jobs and agents.

## T7. Non-functional requirements

| ID | Requirement | Target | Status |
|---|---|---|---|
| NFR-064 | Logs, traces and metrics are produced across the workflow, the decision service and the agents. | Across all three | Proposed |
| NFR-065 | Business measures per decision are produced from the decision log and not from a separate count. | From the log | Proposed |
| NFR-066 | Agent acceptance, override rate, latency and cost are measured and reported. | Measured per agent | Proposed |
| NFR-067 | Every scheduled job has a run book, monitoring and an alert to the operations channel. | Every job | Proposed |
| NFR-068 | A failing interface, job or agent raises an alert to a named owner within its target. | Alert within 15 minutes to the named owner | Proposed, DL11 |

## T8. Requirement traceability

| Requirement | Feature | Story | Test |
|---|---|---|---|

## Appendix T-A. API specification

### T-A.1 Endpoint inventory

| ID | Method | Path | Access | First in |
|---|---|---|---|---|
| API-P9-001 | GET | /api/recovery/v1/reports/measures | Reporting R | E2 |

### T-A.2 Endpoint detail

#### API-P9-001 GET /reports/measures

| Item | Value |
|---|---|
| Purpose | Read the business measures by product, route and period |
| Request | Query: measure, product, route, from, to |
| Response | Measure[] |
| Errors | 401, 403, 503 |
| Authorization | Reporting, right R, scope applied |
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
