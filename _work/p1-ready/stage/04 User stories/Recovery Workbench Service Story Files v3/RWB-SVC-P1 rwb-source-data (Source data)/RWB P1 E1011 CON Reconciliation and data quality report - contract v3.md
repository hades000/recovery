# RWB-P1-E1011-CON Reconciliation and data quality report

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P1-E1011-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-source-data |
| Service epic | RWB-SVC-P1 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-011 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Epic design sign-off | Not specified in the source documents (DOR-RWB-P1-E1011-CON-14) |
| Size | Not specified in the source documents (DOR-RWB-P1-E1011-CON-16) |
| Contract version | API Specification v7 `rwb-source-data.yaml` 5.1.0 (RD-P1-005); provider fake 5.1.0; Temporal contract jar major 1; BACKWARD compatibility within major 1 |
| Patterns applied | DP01, DP02, DP03, DP05, DP06, DP07, DP10, DP11, DP14, DP15, DP17, DP19 |
| Parallel lane | CG-W1 |
| Ready to start | After RWB-P1-E1015-CON defines the parent boundary and the platform template and workflow kit are available |
| Depends on (build) | RWB-PLT-TPL, RWB-PLT-E1047-CON, RWB-PLT-WF, RWB-PLT-E1071-CON, RWB-P1-E1015-CON |
| Contract dependencies | RWB-P1-E1015-CON, RWB-P3-E1042-CON, RWB-P3-E1043-CON; rwb-case dated allocation, open-case and exclusion reads (GAP-3273, GAP-2234, GAP-3411). RWB-P1-AD018-CON owns the separate job API. |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v1.md (FR-P1-008, FR-P1-010, FR-P1-018, FR-P1-019, FR-P1-020, FR-P1-021, FR-P1-022, FR-P1-023) |
| Readiness decisions | RD-P1-001, RD-P1-002, RD-P1-003, RD-P1-004, RD-P1-005, RD-P1-006, RD-P1-008, RD-P1-011, RD-P1-012, RD-P1-020, RD-P1-022, RD-P1-024, RD-P1-025, RD-P1-028, RD-P1-040, RD-P1-042, RD-P1-069 |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-011 for rwb-source-data. The reconciliation is published as one resource on `/api/recovery/source-data/v1`, with a typed workflow and activity contract on task queue `rwb-source-data` in namespace `rwb-recovery` and one consumed event, `rwb.source-data.AceDataReady.v1` (DP-10, DP-11, DP-14). The two lake extracts and the Power BI data set are removed, and rwb-reporting reads the results through this contract (DP-17; GAP-0495; ASM-0687). The path, the result element names and the workflow name are fixed here (GAP-0497; ASM-0689). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P1-E1011-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (16 resolved, 43 cross-document, 2 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Version 3 changes**

- RD-P1-005/011 pin the API, Temporal jar and provider fixtures for the result reads (RWB-P1-E1011-CON#1–#3, #8, #14–#17, #21–#22).
- RD-P1-001/004/006/012/024 assign errors, authorisation and job operations to the platform and AD018 contracts (RWB-P1-E1011-CON#4–#5, #19–#20, #23–#24).
- RD-P1-002/022/028/040/042 keep the E1015 child start, align dated dependencies and close the result enum (RWB-P1-E1011-CON#6–#7, #9–#13, #18).
- Finishing pass (RD-P1-069; request W3-messages; test case backfill): break detail stays aggregate-only, REC-04 and REC-06 are rwb-payment's, and Test Cases v9 IDs and the current resilience standard are cited.

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: applied RD-P1-001, RD-P1-002, RD-P1-003, RD-P1-004, RD-P1-005, RD-P1-006, RD-P1-008, RD-P1-011, RD-P1-012, RD-P1-020, RD-P1-022, RD-P1-024, RD-P1-025, RD-P1-028, RD-P1-040, RD-P1-042.

### 1. Story

As a **solution architect (CON document owner role)**, I want **a versioned OpenAPI contract and provider fake for the two reconciliation reads and a typed contract for the E1015-triggered child workflow**, so that **the consuming slices can build against the same schemas before the implementation is available**.

The CON authoring persona is a project role. The runtime reader is RW-DATASTEW with Platform administration R and scope applied.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout follows DP-11 and ADR-020. The E1015 child workflow replaces the shared Quartz job (DP-10, ADR-016). The versioned reads and workflow interface let consumers catch a schema change in contract tests.

Known consumers are RWB-P1-E1011-APP, RWB-P1-E1011-OPS, RWB-P1-AD019-APP, RWB-P3-AD019-APP, RWB-P1-DM003-APP, RWB-P1-DM012-APP and RWB-ITG-E1011-ITG. Pin the contract and fake in the consuming build. Pending: identify the rwb-reporting consumer story and authorise its service identity, owner reporting service owner, tracked as GAP-3419.

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the base path, the topic and the event names follow the platform rule (DP-13, DP-14).
- The workflow kit and the `rwb-recovery` namespace exist (RWB-PLT-WF, RWB-PLT-E1071-CON), so the child workflow and activity contract is declared against the kit's version and build ID; E1015 owns the parent ingest workflow.
- AD018 owns the job API, including its Idempotency-Key behavior (RD-P1-001/012/024).
- The platform error envelope and message catalogue are the baseline; the CloudEvents envelope is specified by E1015-CON.
- This story owns API-P1-003 and the reconciliation detail read.
- Contract review can begin against the platform artefacts listed in the header.

### 4. Flow

1. Declare both reads and shared Problem responses in API Specification v7 `rwb-source-data.yaml` 5.1.0 (RD-P1-005).
2. Describe the aggregate row from DF-OPS-118 through DF-OPS-129 and resolve the detail and page dependencies in section 12.
3. Publish the E1015 child-workflow and single activity types through contract jar major 1.
4. Publish versioned provider fixtures and pin the consumed rwb-case fakes.
5. Run OpenAPI schema lint, fixture verification, Temporal contract tests and compatibility checks against the tagged major 1 baseline.
6. Tag the baseline after consumer sign-off.

### 5. Exception paths

| ID | Trigger | Outcome | Covered by |
|---|---|---|---|
| X1 | Malformed syntax, unsupported list value or reversed date range | 400 MSG-GEN-001, 400 MSG-GEN-007 or 422 MSG-GEN-003 per section 12.1 | AC1 |
| X2 | Right or scope not granted | 403 MSG-P4-002 Problem | AC6 |
| X3 | Detail UUID absent | 404 MSG-P4-003 Problem | AC11 |
| X6 | Child input missing the business date | Reject before scheduling the activity | AC3 |
| X7 | Fixture drifts from the contract | Provider verification fails the build | AC7, AC11 |
| X9 | Credentials absent or dependency unavailable | 401 MSG-P4-001 or 503 MSG-GEN-006 Problem | AC14, AC18 |

X4 and X5 belong to the AD018 rerun contract. X8 is withdrawn with the placeholder requirement. For an unavailable result store the Problem carries MSG-GEN-006; this read does not enqueue a job.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Requires the platform artefacts and parent workflow contract in the header |
| Negotiable | Open-case reads and detail schema require provider agreement before publication |
| Valuable | Unblocks the consumers listed in section 2 |
| Estimable | Two result reads in the shared YAML, one Temporal contract and versioned fakes |
| Small | Pending squad sizing |
| Testable | Every criterion is tested against an artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Reconciliation contract

  Scenario: AC1 Read schema and query Problem
    Given the OpenAPI contract and version-matched fake
    When both GET operations are linted and a list query uses from=2026-12-01 and to=2026-11-30
    Then both declare typed inputs and outputs and the query returns a 422 Problem with messageCode MSG-GEN-003

  Scenario: AC2 Aggregate dictionary mapping
    Given the result schema and DF-OPS-118 through DF-OPS-129
    When the schema is validated against the property table in section 11
    Then required values have the declared types and lengths and sourceAmount and workbenchAmount accept null
    And recCode accepts REC-01 and REC-02 and result accepts PASS and BREAK

  Scenario: AC3 Typed child contract
    Given Temporal contract jar major 1
    When both the E1015 parent and E1011 worker compile against its types
    Then the workflow type is ReconciliationWorkflow, the single activity is reconciliation and the input carries businessDate and startedBy
    And an input without businessDate is rejected before activity scheduling

  Scenario: AC4 ALS-stamp handoff
    Given E1015 commits the COMPLETED ALS stamp for 2026-11-30
    When the workflow task schedules its children
    Then it starts recon-2026-11-30 on rwb-source-data with ABANDON and USE_EXISTING
    And the E1011 worker has no Kafka listener for AceDataReady

  Scenario: AC5 Consumed inputs
    Given fake catalog answers for 2026-11-30
    When the activity reads the parameters and product LOV
    Then it receives tolerance 0.00, threshold 90, allocation deadline 07:15 and all four LOV-PRODUCT values
    And the dated case-read contract evidence is pending GAP-3273 and GAP-3411

  Scenario: AC6 Forbidden read Problem
    Given an authenticated caller lacks Platform administration R or the applicable scope
    When either read is requested
    Then the 403 response is application/problem+json with type, title, status 403, messageCode MSG-P4-002 and a 32-hex traceId
    And the response includes no result data

  Scenario: AC7 Provider fake version and coverage
    Given the result-read contract tagged 5.1.0
    When provider verification runs against the 5.1.0 fixtures
    Then fixture drift or a missing documented response mapping fails the build

  Scenario: AC8 Tolerance is returned
    Given an aggregate has tolerance_pct 0.1000
    When it is returned by either read
    Then tolerancePct is present and numerically equals 0.1000

  Scenario: AC9 OpenAPI ownership and read headers
    Given the P1 OpenAPI document
    When contract lint inspects the reconciliation operations
    Then there are two GETs under the P1 base, neither carries Idempotency-Key or If-Match, and each uses the shared Problem responses

  Scenario: AC10 Activity retries
    Given the contract jar policy starts at 1 s with coefficient 2 and ten maximum attempts
    When all ten attempts fail
    Then the workflow fails and the activity commits no partial result set

  Scenario: AC11 Fixture response matrix
    Given the versioned fake of both reads
    When requests exercise each documented success and Problem response
    Then every answer validates against its operation in OpenAPI

  Scenario: AC12 Paging beyond one page
    Given more dated aggregates than a page can contain
    When the default list request is exercised
    Then ordering, page boundaries and date defaults match the published page contract
    And the fixture asserts the values once GAP-3412 is resolved

  Scenario: AC13 Empty result page
    Given the date filter matches no aggregate rows
    When the list is read
    Then the answer is 200 and the page has zero items

  Scenario: AC14 Missing credentials and unavailable result store
    Given an unauthenticated read and an authorised read whose result store is unavailable
    When each request is sent
    Then the respective responses are 401 MSG-P4-001 and 503 MSG-GEN-006 Problems

  Scenario: AC15 Kafka cannot trigger this workflow
    Given an AceDataReady record omits businessDate or carries an unlisted status
    When it appears on rwb.source-data.events.v1
    Then E1011 has no subscription, new workflow or local dead-letter record for it

  Scenario: AC16 Breaking change gate
    Given the most recent tagged major 1 OpenAPI contract
    When a reconciliation field is removed, renamed or retyped, or its enum changes incompatibly
    Then the schema compatibility check fails the merge

  Scenario: AC17 Consumer verification
    Given AD019 and the other confirmed consumers pin the result-read fake to 5.1.0
    When their contract suites request aggregate rows and detail
    Then the aggregate fields validate and the orphan-detail assertion awaits GAP-3413

  Scenario: AC18 Consumed client timeout
    Given an rwb-case dependency fake delays beyond 2 s
    When the worker calls the dependency
    Then its caller times out at 2 s, the activity retry policy applies, and exhaustion fails the run without result writes
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One REST base per service: `/api/recovery/source-data/v1`; the document declares no other service's path | DP-13; Arch v5 slide 41 notes |
| BR2 | E1015 owns AceDataReady and AceDataLate. The reconciliation child has no Kafka intake. | RD-P1 register and section 12 |
| BR3 | E1015-CON owns the typed CloudEvents 1.0 schema; E1011 produces decision records through DP-03. | RD-P1 register and section 12 |
| BR4 | AD018 owns the rerun contract including the canonical UUID Idempotency-Key. Both result reads are idempotent GETs. | RD-P1 register and section 12 |
| BR5 | Each error uses the shared RD-P1-004 Problem with the operation and trigger mapping of section 12.1. | RD-P1 register and section 12 |
| BR6 | A schema change is additive within major version 1; a breaking change is a new major version | Arch v5 slide 42 notes |
| BR7 | Only P1 operations are published in the P1 OpenAPI. Consumed dated case, parameter and LOV operations retain their rwb-case owner. | RD-P1 register and section 12 |
| BR8 | Read date-specific tolerance, entry threshold and allocation wait from the parameter catalog, and product/result codes from the LOV definitions. | RD-P1 register and section 12 |
| BR9 | No lake element exists in the contract: the result is read, never extracted (DP-17) | Arch v5 slides 2 and 37; DP-17 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The two reads, child workflow contract and fakes are drafted | In review |
| In review | Consumer sign-off | Confirmed consumers sign off on the contract and fakes | Baselined |
| Baselined | Additive change | An element is added within major version 1 | Baselined |
| Baselined | Breaking change | An element is removed, renamed or retyped, or the workflow name changes | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-source-data | Owns the document, the workflow contract and the fakes; tags the baseline |
| Solution architect | Approves a breaking change and a new major version |
| Confirmed consumers in section 2 | Review and sign off on the parts they consume |
| Platform workflow owner | Owns the workflow kit, the namespace and the worker versioning rule the contract reuses |
| Data steward | Confirms that no personal data field is declared in a break row; E1015-CON owns the event schema |

HTTP uses `entraId` OpenID Connect and `x-capability` area Platform administration, right R. The `rwb_source_data` login is for the database.

Use rwb-access `POST /authorise` for the Platform administration R check and scope. RW-DATASTEW and other approved roles with that grant can read. Service-to-service callers need the same scoped grant. The pending reporting identity is tracked in section 2.

### 11. Data

| Wire field | Type or format | Nullability | BR Field ID |
|---|---|---|---|
| `resultId` | string, UUID | Required | DF-OPS-118 |
| `recCode` | string, length 6, REC-01 or REC-02 | Required | DF-OPS-119 |
| `businessDate` | string, date | Required | DF-OPS-120 |
| `productGroup` | string, max length 15, MORTGAGE, HIRE_PURCHASE, SSME or UNSECURED | Required | DF-OPS-121 |
| `sourceCount` | integer | Required | DF-OPS-122 |
| `workbenchCount` | integer | Required | DF-OPS-123 |
| `sourceAmount` | number, numeric(18,2), baht | Nullable | DF-OPS-124 |
| `workbenchAmount` | number, numeric(18,2), baht | Nullable | DF-OPS-125 |
| `varianceCount` | integer | Required | DF-OPS-126 |
| `variancePct` | number, numeric(9,4), percent | Required | DF-OPS-127 |
| `tolerancePct` | number, numeric(9,4), percent | Required | DF-OPS-128 |
| `result` | string, max length 8, PASS or BREAK | Required | DF-OPS-129 |

A completed run produces eight aggregates across the two aggregate codes and four product groups. The workflow summary carries aggregate outcomes and the REC-05 orphan count. Pending: durable break-detail store and locator for the detail response, including REC-05 orphans, owner P1 data architect with the contract owner, tracked as GAP-1508 and GAP-3413. The existing aggregate schema is limited to REC-01 and REC-02. GAP-0575 and RD-P1-010 settle the candidate-read response. Do not create a legacy exception table or insert REC-05 into `reconciliation_result`. Interim: the result reads answer aggregates and consumers assert counts; no P1 v1 read serves REC-09 break rows or held proof-of-delivery rows (GAP-0577, GAP-1508) (RD-P1-069).

### 12. Contract

#### 12.1 REST operations provided

| Method | Path | Success | Errors |
|---|---|---|---|
| GET | `/admin/reconciliation/results` | 200, result page filtered by `recCode`, `product`, `result`, `from`, `to` | 400, 401, 403, 422, 503 |
| GET | `/admin/reconciliation/results/{resultId}` | 200, aggregate result with detail subject to the storage contract | 400, 401, 403, 404, 503 |

API-P1-003 uses base `/api/recovery/source-data/v1`. Both reads require Platform administration R with scope applied. `resultId` is the UUID from DF-OPS-118. Aggregate codes are REC-01 and REC-02, `product` uses LOV-PRODUCT and `result` uses LOV-REC-RESULT (PASS, BREAK). Dates are ISO dates on `business_date`. Pending: publish result-specific page envelope, sort, page and date defaults and limits, owner P1 contract owner, tracked as GAP-3412.

Invalid date or UUID syntax answers 400 MSG-GEN-001, unsupported list values answer 400 MSG-GEN-007, and `from` later than `to` answers 422 MSG-GEN-003. Missing credentials answer 401 MSG-P4-001, refused scope or right answers 403 MSG-P4-002, a missing UUID answers 404 MSG-P4-003, and an unavailable result store answers 503 MSG-GEN-006. Error responses use `application/problem+json` (RD-P1-004). Required members are `type`, `title`, `status`, `messageCode` and `traceId` (W3C 32-hex). Optional members are `detail`, `instance`, `messageTh`, `field` and `errors`. The `errors` array contains `{field, messageCode, detail}` entries only for 400 or 422 with multiple failing inputs. GET carries neither Idempotency-Key nor If-Match (RD-P1-001/006).

AD018 alone publishes the job list and rerun operations (RD-P1-012/020/024).

#### 12.2 REST operations consumed

- Pending: paged rwb-case open-case key read for the business date (including case-account and case-party keys), owner rwb-case service owner, tracked as GAP-3273.
- Pending: rwb-case allocation status and exclusion operations, including paths, payloads, paging and provider fakes, owner rwb-case service owner, tracked as GAP-0337 and GAP-3411. The contract also needs to define the dated open-case balances and eligible account set for REC-02. GAP-2234 tracks the exclusion dependency in this contract.

RWB-P3-E1042-CON supplies `GET /api/recovery/case/v1/parameters/{key}` for `recon.tolerance.pct`, `case.entry.dpd` and `caselist.allocation.wait.until` (RD-P1-028). RWB-P3-E1043-CON supplies `GET /api/recovery/case/v1/admin/lists/{listCode}` with `asOf` for LOV-PRODUCT and LOV-REC-RESULT (Reference data R). Pin the provider fakes and use a one-hop 2 s timeout with a breaker. Pending: parameter effective-date query shape and service-identity grant, owner rwb-case service owner, tracked as GAP-2213 and GAP-3420.

#### 12.3 Events published

E1015-CON publishes `rwb.source-data.AceDataReady.v1` and `rwb.source-data.AceDataLate.v1` on `rwb.source-data.events.v1`. The E1011 APP writes a DP-03 decision record using `rwb.decision.DecisionRecorded.v1` on `rwb.decision-record.v1`. This CON defines no additional event (RD-P1-003/008).

#### 12.4 Events consumed

None. `ReconciliationWorkflow` is a child of E1015's `AceIngestCheck`, started after the ALS stamp. E1011 does not consume `AceDataReady` (RD-P1-022, RD-P1-024).

#### 12.5 Workflows and activities

`ReconciliationWorkflow` (`recon-{businessDate}`) registers one activity, `reconciliation`, on task queue `rwb-source-data` in namespace `rwb-recovery` (contract jar major 1). The child input is `{businessDate, startedBy}`. E1015 starts it with parent close policy ABANDON in the workflow task that commits the ALS stamp (source status COMPLETED), using USE_EXISTING and ALLOW_DUPLICATE. Before REC-01, use durable timers to poll the rwb-case allocation answer every `recon.allocation.poll.minutes` (5 in the values file, ASM-5708). Proceed at ALLOCATION_COMPLETE YES or the `caselist.allocation.wait.until` limit (07:15 Asia/Bangkok, rwb-case parameter) when the contract is readable. An unreadable answer blocks the checks and produces no result rows (RD-P1-042).

The activity retry policy is initial interval 1 s, coefficient 2, maximum 10 attempts (Error Handling and Resilience Standard v5). Each remote call is one hop with a 2 s caller timeout and a breaker per downstream. Pending: activity start-to-close budget for the whole reconciliation, owner solution architect, tracked as GAP-3414. The workflow ends FAILED when retries are exhausted, preserving any previously committed result set. Pending: reconciliation-specific non-retryable types, owner solution architect, tracked as GAP-3414.

Build the typed workflow and activity interfaces with the shared Temporal contract jar major 1. The workflow returns the aggregate outcomes and orphan count. Cross-service consumers use the REST reads.

#### 12.6 Schedules

None. E1015 `AceIngestCheck` starts this child after the ALS stamp. E1011 registers no Schedule and consumes no Kafka event (RD-P1-022, RD-P1-024).

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| `reconciliation_result` | RWB-P1-E1011-APP | Aggregate results by check, date and product |
| `interaction`, `party_ext`, `contact_point_ext`, `account_ext`, `valuation_ext` | P1 | Read-only REC-05 key checks |
| `data_product_load` | RWB-P1-E1015-APP | Parent stamp |
| `job_run`, `job_run_check` | RWB-P1-AD018-APP | Job and check projection when AD018 is released |

Only P1 reads the ACE views. rwb-case records are reached by published API rather than schema. Retired P1 case-list objects remain marked retired in the dictionary baseline (RD-P1-025).

#### 12.8 Contract fakes

**Provider fakes.** Pin API and WireMock fake to 5.1.0 under `fakes/rwb-source-data/5.1.0/` (working location ASM-5690). Cover both GET reads: 200 page, 200 empty page, 200 detail, 400 syntax/LOV, 401, 403, 422 reversed dates, 404 unknown UUID and 503 store outage where applicable. Include BREAK and PASS and all four product groups. Pin a fake child activity in contract jar major 1 `testFixtures`, returning the summary and typed failures. Detail and dependent response fixtures are pending GAP-3412, GAP-3413 and GAP-3414.

**Consumed fakes.** RWB-P3-E1042-CON provides the three parameter values, RWB-P3-E1043-CON provides the product and result enums, and the E1069 view fixture covers a complete ALS date and an ACE read failure. The dated rwb-case allocation/key/exclusion fake is pending GAP-3273 and GAP-3411.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided | API-P1-003 and detail; consumed rwb-case inputs and authorise are listed above |
| Kafka | No intake | E1015 owns the source-data topic events; APP uses DP-03 for its decision record |
| Temporal | 1 workflow, 1 activity | `recon-{businessDate}` on `rwb-source-data` in `rwb-recovery` |
| File | None | No extract, no lake target, no Power BI data set (DP-17) |

### 13. Solution plan

**Deliverables.** Both GET operations and the shared components in API Specification v7 `rwb-source-data.yaml` 5.1.0 (RD-P1-005), the typed Temporal contract jar major 1 and its test fixtures, and the 5.1.0 WireMock fake.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-02 | `recovery_svc` login | One login per service | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-17 | Data lake, INT-19, INT-20 | Removed (no data lake); reporting from events into rwb-reporting | none; gap if the story needs lake data |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-11 applies to the two published GETs and their fixtures. E1015 retains the ingest and Kafka contracts. DP-17 removes the legacy extract.

**Build steps**

1. Add the two read operations, entraId capability, dictionary fields and shared Problems to the P1 OpenAPI document.
2. Publish the Temporal interfaces and verify the E1015 child input and retry policy.
3. Add the provider and consumed fixtures in section 12.8 and run provider validation.
4. Run OpenAPI lint and backward compatibility diff against the previous tagged major 1 document, starting with 5.0.0 for the addition of the reads. Verify each confirmed consumer against the pinned fake.
5. Record consumer sign-off and tag the published baseline.

**Done when.** The API and jar validate; provider and consumer verification pass; the contract and fake are published at the pinned versions.

### 14. Validation and messages

The status-to-Problem mapping is in section 12.1. MSG-GEN-006 identifies the unavailable system. Pending: GET-specific unavailable wording without a queued-request promise, owner Error and Message Standard owner, tracked as GAP-3418. Thai localisation approval remains pending DL10. AD018 owns the rerun Problem mapping including MSG-P1-001.

### 15. Screens and states

The contract serves the admin result list rendered through the gateway-bff composite route (DP-19) and the rwb-reporting dashboard that reads the same operations. The screen field list and the composite route specification belong to the platform edge story and to rwb-reporting; this story fixes only the case of the merge, which is the result row and its break rows. No Power BI report is in scope. Screens named by this story: the admin result list only; the rwb-reporting dashboard reads the same operations and is not a screen of this story.

### 16. Test cases

| TC reference | Covers | Data |
|---|---|---|
| TC-P1-E1011-CON-01, TC-P1-E1011-CON-03, TC-P1-E1011-CON-04, TC-P1-E1011-CON-07, TC-P1-E1011-CON-11, TC-P1-E1011-CON-17, TC-P1-E1011-CON-18, TC-P1-E1011-CON-20, TC-P1-E1011-CON-21 | AC1, AC2, AC6, AC8, AC9, AC11, AC13, AC14 | Two GETs, dictionary mapping, empty result, permission and full Problem coverage |
| TC-P1-E1011-CON-03 to TC-P1-E1011-CON-05, TC-P1-E1011-CON-15, TC-P1-E1011-CON-22 | AC3, AC4, AC10, AC15 | Child jar, ALS stamp, activity retry and no Kafka trigger |
| TC-P1-E1011-CON-06, TC-P1-E1011-CON-25 | AC5, AC18 | Date-specific parameters, four products, two results and timeout for each rwb-case fake |
| TC-P1-E1011-CON-16, TC-P1-E1011-CON-19, TC-P1-E1011-CON-23, TC-P1-E1011-CON-24 | AC7, AC12, AC16, AC17 | Pinned provider and consumer fake, paging once specified and compatibility diff |

### 17. Guardrails

- No business value in code or in the contract: the tolerance, the entry threshold and the waiting periods stay parameters, and the product groups and the result list stay reference data.
- Keep names, account numbers and production identifiers out of contract examples and fakes. Detail data classification is pending GAP-3413.
- ACE data only through the owner's contract or `recovery.v_ace_*` views: the document names no ACE table and no `rwb_*` schema other than `rwb_source_data`.
- No cross-schema read and no cross-schema key: the contract names only P1's tables, and no element of it is a foreign key into another schema (DP-01).
- One REST base, one topic, one task queue per service; a document that names another service's base, topic or queue fails the review (DP-13, DP-14).
- No lake element: an extract, a lake target or a Power BI data set in the document fails AC7 (DP-17).
- Every example is synthetic; no production payload is copied into a schema or a fake.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-RDF-007 | Account counts and business keys reconcile to ACE | Result schema, ReconciliationWorkflow and reconciliation | TC-P1-E1011-CON-01, TC-P1-E1011-CON-03 to TC-P1-E1011-CON-07, TC-P1-E1011-CON-11, TC-P1-E1011-CON-15 to TC-P1-E1011-CON-25 |
| REQ-RDF-008 | Reconciliation breaks and referential completeness are reported to the data product owner | Detail read and run summary | TC-P1-E1011-CON-01, TC-P1-E1011-CON-03 to TC-P1-E1011-CON-07, TC-P1-E1011-CON-11, TC-P1-E1011-CON-15 to TC-P1-E1011-CON-25 |
| REQ-CWC-004 | Exclusion rules are data | Dated exclusion read | TC-P1-E1011-CON-01, TC-P1-E1011-CON-03 to TC-P1-E1011-CON-07, TC-P1-E1011-CON-11, TC-P1-E1011-CON-15 to TC-P1-E1011-CON-25 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | One-hop contract calls with 2 s timeout | TC-P1-E1011-CON-11, TC-P1-E1011-CON-19, TC-P1-E1011-CON-23, TC-P1-E1011-CON-24 |

### 19. Out of scope

- The implementation of the checks, the workflow and the read operations (RWB-P1-E1011-APP).
- Deployment, worker and alerts belong to RWB-P1-E1011-OPS.
- Job operations and rerun belong to RWB-P1-AD018-CON.
- The rwb-case case query, parameter and reference-data contracts: consumed and faked, never defined here.
- REC-03 and business-key checks beyond the open-case dependency belong to their owning stories. REC-04 and REC-06 are computed by the rwb-payment daily reconciliation (RWB-P8-E4050-APP); this contract's results hold REC-01 and REC-02, and REC-05 is checked by this service only (RD-P1-069).
- The rwb-reporting dashboard and its own document.
- Any lake extract or Power BI data set, which the target removes (DP-17; GAP-0495).


### Remaining delivery steps

- Size: pending refinement; owner squad.
- Epic design sign-off: pending; owner product owner.
- Contract marked Done and published: pending; owner contract owner.
- Fake published: pending; owner contract owner.
- Test data loaded in DEV: pending; owner data engineer.
