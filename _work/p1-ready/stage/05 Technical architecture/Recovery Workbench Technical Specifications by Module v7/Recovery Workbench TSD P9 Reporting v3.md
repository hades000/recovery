SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

# Recovery Workbench P9 Reporting

Technical specification. SCB Collections and Recovery. Henka Group, 22 November 2026.

(C) Siam Commercial Bank and Henka Pte Ltd

## Document control

| Attribute | Value |
|---|---|
| Document title | TSD P9 Reporting |
| Document ID | P9-RWB-TSD-v3 |
| Version | 3 |
| Status | Draft |
| Date | 22 November 2026 |
| Supersedes | Version 2, 28 October 2026 |
| TSD owner | Solution architect |
| Build squad | TechX recovery squads (GAP-1999; ASM-3225: no squad is named per service) |
| Decision | D-RCV-60 microservice realignment |
| Status note | Draft: no approval of version 3 is recorded (GAP-1998; ASM-3217) |
| Change | 3, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash |

| Document | Type | Relationship |
|---|---|---|
| Recovery Workbench FSD P9 Reporting | FSD | Pair |
| Recovery Workbench Target Architecture | Architecture | Parent |
| Recovery Workbench Logical Data Model and Data Dictionary | Data | Source of T3 |
| Recovery Workbench API Specification | API | Source of appendix T-A |
| Recovery Workbench Microservice Ownership Map v1 | Ownership | Owner of every table, endpoint, event, workflow and job in T0 and T5.2 |

## Existing capability check

| Capability | Verdict | Owning document | Note |
|---|---|---|---|
| Sign-in, access check, audit, PII and SOC logging | REUSE | ACE common module | Called through the published interface |
| Scheduler and batch | REUSE | ACE pattern: Quartz and Spring Batch | Jobs in the Batch and Scheduling Design |
| Outbox and retry | REUSE | Error Handling and Resilience Standard | Through P2 |
| Rules evaluation | REUSE | Rules Engine Design | Through the rules component |

Under D-RCV-60 the scheduler and batch row is delivered by the Temporal layer (ADR-016): Temporal Schedules and event-started workflows in the owning service replace the Quartz and Spring Batch jobs (DP-10). The outbox and retry row is delivered by the Kafka outbox, inbox and retry topics (ADR-015; DP-09).

## T0. Service

P9 Reporting is one of the 19 services of Architecture v5: `rwb-reporting` (service name Reporting, module P9, wave 1, service epic `RWB-SVC-P9`). Version 3 adds this section so that the specification is read as the specification of one service: its identity, what it owns, and the decoupling patterns that replace the monolith's in-process calls. Every owner is taken from Microservice Ownership Map v1 and every identifier from Template and Rules R4 (ADR-013, ADR-014).

P9 calls almost nobody and listens widely: it projects from the event stream and reads source data through the P1 snapshot activity (Architecture v5 slide 13).

### T0.1 Service identity

| Item | Value |
|---|---|
| Module | P9 Reporting |
| Service | `rwb-reporting` (Reporting) |
| Service epic | `RWB-SVC-P9` |
| Wave | 1 |
| Schema | `rwb_reporting` |
| Database login | `rwb_reporting`: one login per service, with its own connection pool cap |
| REST base | `/api/recovery/reporting/v1` |
| Kafka topic | `rwb.reporting.events.v1`, with `.retry` and `.dlt` topics |
| Event names | `rwb.reporting.<Event>.v1`, CloudEvents 1.0 in binary mode, key `caseId` |
| Temporal | namespace `rwb-recovery`; task queue `rwb-reporting` |
| Java package | `th.co.scb.ace.workbench.recovery.reporting` |
| Edge | gateway-bff for the staff screens of this service |
| Contract artefacts | `05 Technical architecture/Recovery Workbench API Specification v5/rwb-reporting.yaml`; `05 Technical architecture/Recovery Workbench API Specification v5/asyncapi/rwb-reporting.asyncapi.yaml` |
| Suggested owner, app development | TechX (suggested; any team may pick up this story) |
| Suggested owner, ACE DB | ACE team (suggested; any team may pick up this story) |

### T0.2 What this service owns

Architecture v5 slide 41 gives this service: measures, snapshots, steering dashboard, regulatory reports. Table T0.2 states the same ownership in the form the Ownership Map uses, with the counts this specification carries. A table that the map assigns to another service is not built here, whatever T3 says (see the note under T3).

| Area | Owner and artefact | Count |
|---|---|---|
| Business tables in `rwb_reporting` | `measure_definition`, `measure_publish`, `measure_snapshot` | 3 |
| REST operations | appendix T-A and `rwb-reporting.yaml` | 1 |
| Events published | none | 0 |
| Workflows and schedules | none in the Ownership Map sheet; T5.2.1 names Measures, 01:30, buildRegulatoryExtract | 2 |
| Jobs | JOB-15 | 1 |

### T0.3 Decoupling patterns applied

The left column is the pattern of Template and Rules R5.5; the middle column quotes the line of this specification that carries the legacy marker, where one is present; the right column is what replaces it in this service.

| DP | Legacy marker in this specification | How the service lands it |
|---|---|---|
| DP-01 | — | Owns its tables in `rwb_reporting`; no other service reads them (ADR-014). |
| DP-02 | — | One login, `rwb_reporting`, with its own connection pool cap. |
| DP-03 | `…on events from P3 and writes through the decision log.` | Local decision record plus DecisionRecorded (EV-08) on `rwb.decision-record.v1`. |
| DP-07 | `DF-RPT-035 / data_product / LOV / varchar(25) / Yes / LOV-DATA-PRODUCT…` | Reference data and lists of values from the `rwb-case` contract (H RWB-PLT-E1043-CON). |
| DP-08 | `RW-CASEOWN Case owner / R` | Authorisation through the `rwb-access` authorise contract and the guard library (H RWB-PLT-E1037-CON). |
| DP-09 | `…state machine of its own; the module acts on events from P3 and writes through the decision…` | Outbox and inbox library; CloudEvents on `rwb.reporting.events.v1` with retry topics and `.dlt`. |
| DP-10 | `Scheduler and batch / REUSE / ACE pattern: Quartz and Spring Batch / Jobs in the Batch and…` | Temporal Schedules and event-started workflows through the workflow kit (ADR-016). |
| DP-11 | `…reaches other modules only through their published interfaces and other systems only through COLLINS,…` | One REST hop, 2 s timeout, breaker; the consumer builds against the provider's fake (ADR-020). |
| DP-13 | `API-P9-001 / GET / /api/recovery/v1/reports/measures / Reporting R / E2` | REST base `/api/recovery/reporting/v1`. |
| DP-14 | — | Topic `rwb.reporting.events.v1`, retry topics and `.dlt`; naming library (H RWB-PLT-E1047-CON). |
| DP-15 | — | Per-service Flyway sequence in `rwb_reporting`. |
| DP-17 | `INT-19 / Data lake and Power BI / Out / Daily batch…` | No data lake: reporting reads events; the lake copy is removed (ADR-018). |

### T0.4 What this service is not

- It holds no other service's table and no ACE table beyond the read-only `recovery.v_ace_*` views (DP-01, DP-05).
- It runs no shared Quartz job and touches no ACE batch table (DP-10; ADR-016).
- It holds no data lake and no source copy: the projections are built from events (DP-17; ADR-018).
- It is not a monolith module: the published Java interface of T2 is replaced by the contract set of T5.2 (DP-11; ADR-020).

## T1. Architecture overview

P9 Reporting is delivered as the service `rwb-reporting` (module P9, wave 1, service epic `RWB-SVC-P9`): one repository, one pipeline, one schema `rwb_reporting` with one login, behind gateway-bff (ADR-013, ADR-014). It covers: baseline measures, steering dashboard, operational and regulatory reports. It reaches other modules only through the contracts of T5.2 and other systems only through COLLINS, file loads and the ACE paths.

## T2. Component design

| Component | Responsibility |
|---|---|
| ReportingController | REST endpoints in appendix T-A; validation; maps errors to problem responses |
| ReportingService | Business logic; calls the rules component; writes the decision log entry before any change |
| ReportingRepository | Reads and writes the module's tables only |
| Jobs | Temporal Schedules and event-started workflows this service owns (T0.2, T5.2.1; DP-10) |
| Published interface | The contracts of T5.2: REST operations, events and workflows other services call; no table is read across modules (DP-11) |

The published interface of this table is the contract set of T5.2: the REST operations, the events and the workflows, not a Java interface in a shared classpath (DP-11; ADR-020). Components that the Ownership Map places in another service are stated in T0.2 and T5.2 and are built by that service.

## T3. Data model

Every object of T3 that Microservice Ownership Map v1 assigns to `rwb-reporting` lives in schema `rwb_reporting` with the standard columns of T3.0 (DP-01, DP-15; ADR-014). `measure_definition`, `measure_snapshot` and `measure_publish` stay here. The projections are built from events; there is no data lake copy (DP-17, ADR-018).

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

### T5.2 Contracts

Version 3 states every cross-module dependency of this module as a contract, so that the service is built against a published artefact and its fake (ADR-020; DP-11). The artefact per call type is: OpenAPI 3.1 for REST, AsyncAPI 3.0 for Kafka, the Temporal interface named here for a workflow or activity, the Interface Specifications manifest for a file, the Nexus operation for the ACE restructure calculator, and a grant on the view for SQL. No row of this section reads another service's table (DP-01). Every consumed contract is class C (Template and Rules R5.4): it never blocks the build, because the consumer builds against the fake, and the real cross-service behaviour is class I work on an integration story. Architecture v5 slides 13 to 20 name a few operations differently from the published files of 22 November 2026; the published file is the artefact the fake is generated from and is the one cited here (GAP-1997; ASM-3224).

#### T5.2.1 Contracts provided

The REST operations of this service are published in `05 Technical architecture/Recovery Workbench API Specification v5/rwb-reporting.yaml` (5.0.0, 22 November 2026) under the base `/api/recovery/reporting/v1`. Appendix T-A holds the endpoint IDs, the access right and the first release of each one.

| # | Method | Path | operationId |
|---|---|---|---|
| 1 | GET | `/reports/measures` | `getReportsMeasures` |

Workflows, schedules, files and views this service provides:

| Contract | Type | Called by or target | Note |
|---|---|---|---|
| Measures, 01:30 | Temporal Schedule | P9 rwb-reporting | JOB-15 (DP-10) |
| buildRegulatoryExtract | Temporal activity | P9 rwb-reporting | Triggered by Airflow; no data lake (DP-17) |

Events this service publishes (AsyncAPI 3.0, CloudEvents 1.0):

None published by this service: Architecture v5 slide 15 names ReportPublished on `rwb.reporting.events.v1` and the AsyncAPI document of 22 November 2026 does not carry it yet (GAP-1996; ASM-3223).

#### T5.2.2 Contracts consumed

| Contract | Type | Provider | Class | Failure path |
|---|---|---|---|---|
| snapshot(page) for measures | Temporal activity | P1 rwb-source-data | C | Workflow retry policy; the caller keeps its state (DP-12) |
| deliverFile(manifest) for the regulatory extract | Temporal activity | P2 rwb-integration | C | Workflow retry policy; the caller keeps its state (DP-12) |

Events this service consumes:

| Event | EV | Provider topic | Provider | Class | Failure path |
|---|---|---|---|---|---|
| DecisionRecorded | EV-08 | `all 19 service topics` | all | C | Retry 1 min, 10 min, 1 h, then `.dlt`; inbox dedupe |
| Every business event of the 19 services (projections) | — | `all 19 service topics` | all | C | Retry 1 min, 10 min, 1 h, then `.dlt`; inbox dedupe |

#### T5.2.3 Call-type summary

| Call type | Provided | Consumed | Artefact |
|---|---|---|---|
| REST | 1 | 0 | OpenAPI 3.1, one file per service |
| Kafka (events) | 0 | 2 | AsyncAPI 3.0, one file per service |
| Temporal | 2 | 2 | Workflow and activity interfaces, queue `rwb-reporting` |
| File | 0 | 0 | Interface Specifications manifest and the SAS link |
| Nexus | 0 | 0 | Nexus operation into ACE |
| SQL | 0 | 0 | Read-only grant on the view |

A contract change is a new version of the artefact, never a code change in the consumer (ADR-020). The provider named in T5.2.2 is the owner in Microservice Ownership Map v1, and the consumer list of each event is the Arch v5 event catalogue on slides 42 and 43.

### T5.3 Events

The event contract of this service is `05 Technical architecture/Recovery Workbench API Specification v5/asyncapi/rwb-reporting.asyncapi.yaml`; the shared decision-record contract is `asyncapi/rwb.decision-record.v1.asyncapi.yaml`. Every service publishes DecisionRecorded (EV-08) to `rwb.decision-record.v1` from its outbox in the same transaction as its state change (DP-03, DP-09; ADR-015, ADR-022); consuming services dedupe through their inbox table. Events carry identifiers and facts, never personal data (Event and Messaging Design v4, sheet Rules).

| Event | EV | Direction | Topic |
|---|---|---|---|
| DecisionRecorded | EV-08 | Consumed | `all 19 service topics` |
| Every business event of the 19 services (projections) | — | Consumed | `all 19 service topics` |

An event shown with `—` has no number in the numbered catalogue: the Arch v5 catalogue calls these rows `+`, so the number is not specified in the source documents (GAP-1996; ASM-3223). Architecture v5 slide 15 names ReportPublished on `rwb.reporting.events.v1`; there is no AsyncAPI operation for this service yet (GAP-1996; ASM-3223).

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

Every operation of T5.2.1 is authorised through the `rwb-access` authorise contract with the role, the scope and the delegation limit of T6.1 (DP-08; C RWB-P4-E1037-CON); the caller caches the answer and refreshes it on AccessPolicyChanged and DoaLimitChanged.

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
| API-P9-001 | GET | /api/recovery/reporting/v1/reports/measures | Reporting R | E2 |

The operation IDs, paths and operationIds of these endpoints are published in `05 Technical architecture/Recovery Workbench API Specification v5/rwb-reporting.yaml`; where an appendix row and the published operation differ, the published operation is the contract of T5.2.1 and the row keeps its ID for traceability (GAP-1997; ASM-3224).

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
