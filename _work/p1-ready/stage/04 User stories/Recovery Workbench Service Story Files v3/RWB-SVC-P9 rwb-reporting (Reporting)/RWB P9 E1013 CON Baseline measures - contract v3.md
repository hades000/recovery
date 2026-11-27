# RWB-P9-E1013-CON Baseline measures - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P9-E1013-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-reporting |
| Service epic | RWB-SVC-P9 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-013 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP05, DP07, DP10, DP11, DP13, DP15, DP17, DP19 |
| Parallel lane | CG-W1 |
| Ready to start | Day 1 |
| Size | Not set; the squad sizes it at refinement (DOR-RWB-P9-E1013-CON-16) |
| Contract version | rwb-reporting.yaml 5.1.0 (API Specification v7), paths under /v1; consumes rwb-source-data.yaml 5.1.0 |
| Depends on (build) | None |
| Contract dependencies | RWB-P1-E1015-CON (published freshness read; RD-P1-022) |
| Integration dependencies | None |
| External dependencies | 05:30 Schedule of RWB-P1-E1015-APP in rwb-source-data, its worker and task queue, registered by the platform workflow and operations stories of the epic; external or operations dependency, not a build dependency (RD-P1-022; RD-P1-040; GAP-0561 closed by RD-P1-041) |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P9 rwb-reporting v1.md (no FR mapped to REQ-RDF-012) |
| Status | Draft (directive resolutions) |
| Readiness decisions | RD-P1-001, RD-P1-002, RD-P1-004, RD-P1-005, RD-P1-010, RD-P1-022, RD-P1-041, RD-P1-061, RD-P1-066 |

**Version 3 changes** (D-RCV-60 P1 developer readiness, RD-P1 register).

- RD-P1-066: Align the JOB-15 start and deployment with the Airflow call and paused Schedule.
- Backfill the published Test Cases v9 cross-references.
- RD-P1-005, RD-P1-061: Pin account-form payments and the 5.1.0 freshness shape.
- The freshness read and the readiness chain are published by RWB-P1-E1015-CON: status `LOADED` or `STALE`, `businessDate` null when never stamped, stamp in use is the latest row (RD-P1-005, RD-P1-022, RD-P1-041; findings #3, #8).
- `listEligibleAccounts` is not a row of this contract (RD-P1-010; finding #4).
- One `messageCode` per status; the key answers of the reference-load element declared (RD-P1-001, RD-P1-004; findings #5, #6).
- Pending: run product codes and completeness logic (GAP-3383, GAP-3434), payment since-entry rule and workload access (GAP-3427), and snapshot activity integration (GAP-3384).

**Change log.** D-RCV-60, 22 November 2026: contract baseline of the baseline-measures capability of rwb-reporting, split from RWB-E1-013. It fixes the two reads on `/api/recovery/reporting/v1` (DP-13) with the definitions read that RWB-P3-E1013-APP consumes, the columns of DF-RPT-031 to DF-RPT-058 in the three tables, the six closed lists, the five consumed rows of rwb-case and rwb-source-data, the decision-record element of DP-03, the 01:30 Schedule of DP-10, the rights of TSD P9 T6.1, the error envelope, the fakes and the absence tests. The data lake, the INT-19 extract and the trailer are removed (DP-17); the plan's C row does not carry the two rwb-source-data rows; and no source gives the path of the definitions read or the approver's type (GAP-2566, GAP-2567, GAP-2569, GAP-2570, GAP-2571, GAP-2572; ASM-4232, ASM-4233, ASM-4235, ASM-4236, ASM-4237, ASM-4238). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P9-E1013-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (14 resolved, 32 cross-document, 14 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead of rwb-reporting**, I want **the published contract baseline of the baseline-measures capability — the two reads on `/api/recovery/reporting/v1`, the three tables' columns and their closed lists, the five consumed rows of rwb-case and rwb-source-data, the decision-record element, the Schedule of the 01:30 run, the rights, the error envelope and the fakes**, so that **RWB-P9-E1013-APP, RWB-P3-E1013-APP, RWB-P1-E1013-APP, the wave 1 harness and the deployment story build against one fixed, testable surface on Day 1 and a measure column, a list value, a consumed row or a read shape can never drift between the four services without a failing build**.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). The legacy story of RWB-E1-013 crossed three boundaries at once inside one module: the definitions, the case and payment facts, and the lake extract. The target splits them, and each boundary is now a contract another team builds against: rwb-case serves the facts, RWB-P3-E1013-APP owns them; rwb-source-data serves the payments and the gate, RWB-P1-E1013-APP owns the payments and RWB-P1-E1015-APP the freshness and the gate (RD-P1-022); rwb-reporting owns the definitions, the snapshot and the publish, and serves the catalog that rwb-case needs so that a band version cannot retire a band a definition still uses.

The baseline also fixes the naming the checks require: schema `rwb_reporting`, login `rwb_reporting`, base `/api/recovery/reporting/v1`, topic `rwb.reporting.events.v1` with its retry and `.dlt` topics, task queue `rwb-reporting` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.reporting` (Template and Rules §R4; context pack P9). It records that this service holds no `v_ace_*` grant and no grant on `rwb_case`, so DP-05 is declared as a prohibition and the ACE data is consumed on the owner's contract only.

Four points are carried as gaps and assumptions rather than decided quietly: the plan's C row is None while the app story consumes five rows (GAP-2567), the Ownership Map gives this service no event while the wave 1 harness names `rwb.reporting.ReportPublished.v1` (GAP-2569), no source gives the path or the shape of the definitions read that rwb-case consumes (GAP-2572), and the legacy story assigns the measures read to Epic 2 while the Ownership Map gives the operation to this service (GAP-2570).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the base, the topic, the queue and the event names follow the platform rule rather than a local choice.
- The platform error envelope, the paging and filter convention and the `Idempotency-Key` rule are the platform baseline (Architecture v5 slide 11); where this document narrows them it says so.
- The ownership of the objects is taken from the Ownership Map only: `measure_definition`, `measure_snapshot` and `measure_publish` are P9's; `recovery_case`, `queue`, `case_account` and the reference rows are P3's; every `v_ace_*` view is P1's; `decision_log_entry` is P7's.
- RWB-P3-E1013-APP, RWB-P3-E1018-CON and RWB-P3-E1043-CON publish the three rwb-case rows this baseline consumes, and RWB-P1-E1015-CON the freshness read of rwb-source-data, with their fakes. The payments read of RWB-P1-E1013-APP has no published shape yet: this baseline is its consumer contract (RD-P1-022), and the shape is Pending (GAP-3426). The two rwb-source-data rows are class C dependencies that the plan's C row does not carry (GAP-2567; ASM-4233).
- The decision-record library of DP-03 and the workflow kit of DP-10 are platform work, named here and built elsewhere.
- The three tables are declared by this baseline and created by the app story's migration; this story creates no table, no column and no migration.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the OpenAPI 3.1 document of rwb-reporting for this capability: the two reads with their query parameters, the answer elements, the paging, the rights and the error responses.
2. Fix the three elements of the tables: the definition columns of DF-RPT-031 to DF-RPT-040, the snapshot columns of DF-RPT-041 to DF-RPT-052 and the publish columns of DF-RPT-053 to DF-RPT-058, with their types, their required flags and the list each of them is declared against.
3. Fix the consumed rows: the case-facts read of RWB-P3-E1013-APP, the case-record read of RWB-P3-E1018-CON, the reference-list read of RWB-P3-E1043-CON, the payments read of RWB-P1-E1013-APP and the freshness read of RWB-P1-E1015-CON, marking every field the sources do not give with the placeholder.
4. Record the decision-record element of DP-03, written before the snapshot rows commit, and the Schedule element of DP-10 with its 01:30 time, its catch-up policy and its no-overlap rule.
5. Record the closed vocabulary of the six lists, the rights of the two reads, the naming baseline and the rule that no measure code, formula, unit or band is a constant of the code.
6. Publish the contract tables of section 12 and the six fakes of 12.8.
7. Add the contract tests: schema validation, the additive rule, the vocabulary, the shapes, the error envelope, the absence of a `v_ace_*` read and of a `recovery_case` property, the absence of a published and of a consumed event, the drift between a fake and the document, and the absence of a lake path.
8. Tag the baseline and hand it to RWB-P9-E1013-APP, RWB-P3-E1013-APP, RWB-P1-E1013-APP, RWB-P9-E1013-OPS and the wave 1 harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A response or a request body fails schema validation | The build fails on the schema lint; a deployed service answers 400 or 500 with the error envelope | MSG-GEN-001 | AC1, AC4 |
| X2 | A property is renamed or removed within major version 1 | The contract test fails; the change needs a new major version | None | AC1, AC2 |
| X3 | A contract fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC6 |
| X4 | A consumed row has a field list the sources do not give | The row carries the placeholder, the gap and the assumption, and the fake is derived from the published document | None | AC3, AC5 |
| X5 | A value outside one of the six closed lists appears in the document or in an example | The vocabulary test fails the build | None | AC2 |
| X6 | The document declares another service's operation as provided, a `v_ace_*` view, a `recovery_case` property or a rule row | The review fails the baseline; the boundary test fails the build | None | AC3 |
| X7 | The document declares an event of this service, a consumed event, a second topic or a lake path | The absence test fails the build | None | AC5 |
| X8 | The rights of a read are not the ones TSD P9 T-A.1 and T6.1 declare | The access test fails the build | MSG-P4-002 | AC4 |
| X9 | The document types `approved_by` as a string while TSD P9 T3.1 types it `uuid`, or the reverse | The baseline carries the TSD type, and the legacy approver reference is carried as a comment on the element | None | AC2, §11 |

X1 to X4 and X6 to X8 are the paths of a contract baseline carried from the platform convention, X5 is the closed vocabulary and X9 is the one type conflict the sources give (GAP-2571; ASM-4237).

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the Ownership Map, the FSD P9 and TSD P9 appendices and the published rows of rwb-case and rwb-source-data only |
| Negotiable | The element names beyond the ones the sources give, the example values and the fake fixtures are settled in the baseline review; the two reads, the tables, the lists, the base, the topic, the queue and the schema are fixed by the target architecture |
| Valuable | Unblocks the app story, the P3 facts story, the P1 payments story, the deployment story and the wave 1 harness on Day 1 |
| Estimable | One OpenAPI document, nine contract tables, six fakes and six new contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the baseline-measures capability of rwb-reporting

  Background:
    Given the service naming rule of the platform library is in force
    Given the ownership of measure_definition, measure_snapshot and measure_publish is P9, of recovery_case and queue is P3 and of every v_ace_* view is P1
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 The two reads are declared on the reporting base with their shapes and their errors (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-reporting is published with this change
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares GET /reports/measures with the query parameters measure, product, route, from and to and a Measure list answer of status 200, and GET /measure-definitions with the query parameter onDate and a definition list answer of status 200, both under the base /api/recovery/reporting/v1 and owned by rwb-reporting
    Then the answers 400, 401, 403, 404, 422 and 503 are declared with one envelope and one message ID per condition
    Then the answers are `application/problem+json` with `messageCode` MSG-GEN-001 for 400 and 422, MSG-P4-001 for 401, MSG-P4-002 for 403, MSG-P4-003 for 404 and MSG-GEN-006 for 503
    Then neither read declares an Idempotency-Key, because neither creates a resource
    Then no operation of the definition load, the run or the rerun is declared by this document beyond the reference-load element it names
    Then every other property of the two reads is copied from the platform convention and is not redefined here

  Scenario: AC2 The three table elements and the six closed lists are fixed (new, D-RCV-60)
    Given the element section of the baseline
    When it is compared with TSD P9 T3.1 and T3.2
    Then the definition element declares the columns of DF-RPT-031 to DF-RPT-040: id, measure_code, name, formula, data_product, unit, definition_version, approved_by, approved_at and valid_from
    Then the snapshot element declares the columns of DF-RPT-041 to DF-RPT-052: id, measure_code, definition_version, business_date, product_group, dimension_code, dimension_value, value, case_count, is_baseline, frozen and published_at
    Then the publish element declares the columns of DF-RPT-053 to DF-RPT-058: id, business_date, status, case_list_count, dashboard_count and held_reason
    Then measure_code, name, formula, data_product, unit and definition_version are required on the definition, measure_code, definition_version, business_date, value, is_baseline and frozen on the snapshot, and business_date, status, case_list_count and dashboard_count on the publish
    Then data_product is declared against LOV-DATA-PRODUCT with DP01 to DP14, unit against LOV-MEASURE-UNIT with COUNT, THB, DAYS and PERCENT, dimension_code against LOV-MEASURE-DIM with ROUTE, AGE_BAND, QUEUE, STAGE and AGENT, product_group against LOV-PRODUCT with MORTGAGE, HIRE_PURCHASE, SSME and UNSECURED, and status against LOV-MEASURE-PUBLISH with PUBLISHED and HELD
    Then approved_by is declared uuid as TSD P9 T3.1 types it, and the legacy approver reference "TRB-0001" is carried as a comment and not as a type
    Then no property is added for a case fact, a band boundary, an account, a payment amount or a lake path, and those facts stay with their owners

  Scenario: AC3 The consumed rows of rwb-case and rwb-source-data are declared and the facts stay there (new, D-RCV-60)
    Given the consumed rows of the baseline
    When they are compared with the Ownership Map and with Architecture v5 slides 29, 37 and 45
    Then the case-facts read is declared as consumed from P3 rwb-case with the nine fact fields, the as-of time, the row count and the reference version, at GET /api/recovery/case/v1/cases/facts
    Then the case-record read is declared as consumed from P3 rwb-case with the account link of a case, and the reference-list read from P3 with the five lists at their version, under RWB-P3-E1018-CON and RWB-P3-E1043-CON
    Then the payments read is declared as consumed from P1 rwb-source-data at GET /api/recovery/source-data/v1/payments?accountKey={accountKey}, with PaymentsAnswer and the RD-P1-061 ordering and 409 refusal
    Then the freshness read is declared at GET /api/recovery/source-data/v1/data-products/freshness?asOf={date} with productCode, businessDate (nullable) and status LOADED or STALE, without a COMPLETE/HOLD member
    Then the two rwb-source-data rows are marked class C and their absence from the plan's C row is recorded (GAP-2567; ASM-4233)
    Then the document declares no v_ace_* path, no v_ace_* property, no recovery_case property and no grant on any rwb_* schema of another owner
    Then each row is one hop with a 2 s budget, a breaker and no retry of its own (DP-11, ADR-020)

  Scenario: AC4 The rights, the error envelope and the reference-load element are fixed (new, D-RCV-60)
    Given the access section of the baseline and TSD P9 T-A.1 and T6.1
    When the two reads and the definition load are compared with them
    Then both reads declare Reporting right R with the scope applied, and the definition load declares Reference data right C on the table measure_definition
    Then RW-BIANAL holds Reporting CRUD, RW-DATASTEW holds Reporting CRU, and RW-TRIBE, RW-FINANCE, RW-AUDIT, RW-COMPLY and RW-PLATADM hold Reporting R as TSD P9 T6.1 gives them, and no other role is given a right
    Then a role without the right is described as refused with MSG-P4-002, and the error envelope carries one message ID per condition
    Then the definition load declares MSG-GEN-001 for a missing or invalid row, MSG-P9-003 for a measure with no definition in force, MSG-P9-001 for a frozen date, MSG-P1-001 for a stale product, MSG-GEN-006 for a held publish and MSG-P7-003 for a failed record
    Then the definition load declares 400 MSG-PLT-N009-03 for a missing, blank or non-UUID Idempotency-Key, 409 MSG-PLT-N009-05 for a key used for another request or still in flight, 503 MSG-PLT-N009-06 for an unavailable key store, and the stored answer for a replay of the same request
    Then the load element is described as the target form of the legacy POST /admin/reference-loads operation, whose path is not specified in the source documents (GAP-2568; ASM-4234)

  Scenario: AC5 The decision record, the Schedule and the absence of an event are fixed (new, D-RCV-60)
    Given the decision, Schedule and event sections of the baseline
    When they are compared with the library schema, the workflow kit and the Ownership Map
    Then one decision record is declared per run with the business date, the definition version in force, the row count, the gate answer, the publish state and the decided-at time
    Then the record is declared as written through the local library on the shared rwb.decision-record.v1 before the snapshot rows commit, and a failed write leaves them unchanged with MSG-P7-003
    Then one Schedule is declared for the run of JOB-15 at 01:30 Asia/Bangkok on queue rwb-reporting in namespace rwb-recovery, with a catch-up of one missed run and no overlapping execution, replacing the Quartz row of the legacy job
    Then the topic rwb.reporting.events.v1 is named with its retry and .dlt topics by the naming rule, and the document declares no event published by this service, no consumed event and no consumer group, while rwb.reporting.ReportPublished.v1 named by the wave 1 harness is recorded as the conflict it is (GAP-2569; ASM-4235)
    Then the absence test fails a build that adds a published event, a consumed event, a second topic, a second Schedule or a lake path (GAP-2566; ASM-4232)

  Scenario: AC6 The six fakes answer the document, the drift test fails a build and the naming baseline holds (new, D-RCV-60)
    Given the fakes and the naming section of the baseline
    When each fake is compared with the read or the element it serves
    Then the rwb-case case-facts fake answers the 120 cases of 2026-11-27 with the nine fact fields, the as-of time and the reference version, and a date with no case
    Then the rwb-case case-record and reference-list fake answers the account link of a case and the five lists at their version, the rwb-source-data fake answers the payments of an account, freshness elements with status LOADED, STALE with a businessDate and STALE with businessDate null, and the record stub answers a healthy chain and a stopped chain
    Then the drift test compares every fake with the document and fails the build on any difference
    Then each of 12.1 to 12.9 is present and names its owner from the Ownership Map, with None where the element is empty
    Then the schema is rwb_reporting, the login is rwb_reporting, the base is /api/recovery/reporting/v1, the queue is rwb-reporting in namespace rwb-recovery and the Java package is th.co.scb.ace.workbench.recovery.reporting
    Then the tables named as owned are measure_definition, measure_snapshot and measure_publish with the library objects, and recovery_case, queue, case_account, every v_ace_* view and decision_log_entry are named as other owners' and consumed only through their contracts

  Scenario: AC9 Each business rule BR1 to BR13 of section 8 is carried by a criterion of this story and by a test case of section 16 (new, D-RCV-60)
    Given the business rules of section 8 and the criteria AC1 to AC6 of this story
    When each rule row is compared with its Covered by column
    Then every rule from BR1 to BR13 names at least one criterion of this story and at least one test case ID of section 16, and no rule is left without a criterion
    Then a rule that is an architecture constraint is carried by a guardrail of section 17 or by a boundary test, and no rule is declared as a constraint without one of them
```

These six criteria are new for the contract baseline and test the artefact only. They restate no business outcome owned by RWB-P9-E1013-APP and they copy no criterion of the legacy story, whose six criteria stay with the app story word for word and whose AC2 and AC6 stay with RWB-ITG-E1013-ITG.

### 8. Business rules

| ID | Rule | Source | Covered by |
|---|---|---|---|
| BR1 | The measures are rwb-reporting's, and the contract declares the columns, the lists and the required flags on the three elements only | Architecture v5 slide 41; TSD P9 T3.1 and T3.2; Ownership Map (three tables owner P9) | AC2; TC-P9-E1013-CON-02 |
| BR2 | The decision record is declared as an element written before the snapshot commits, through the local library on the shared topic; a failed write changes nothing | DP-03; legacy RWB-E1-013 AC5 | AC5; TC-P9-E1013-CON-04; TC-E1-013-05 |
| BR3 | The facts stay with their owners: the contract declares the case and payment rows as consumed, declares no `v_ace_*` property and describes no ACE table read of this service | DP-05 as a prohibition; Architecture v5 slides 29, 37 and 45; GAP-2567 | AC3; TC-P9-E1013-CON-03 |
| BR4 | The measure is data: no measure code, formula, unit, band or threshold is a schema default, an enumeration member of the code or a constant in an example | REQ-RDF-012; Principle 1; legacy BR1 and BR7 | AC4; TC-P9-E1013-CON-07 |
| BR5 | No event of this service is declared, and no consumed event and no consumer group is declared | Ownership Map (P9 events: none); GAP-2569 | AC6; TC-P9-E1013-CON-04 |
| BR6 | No lake path is declared: no INT-19 extract, no trailer, no lake client and no outbound batch element | DP-17; ADR-018; GAP-2566 | AC5; TC-E1-013-07 |
| BR7 | The vocabulary is closed: the six lists are published as enumerated values and no list value is a constant of the code | TSD P9 T3.2; FSD P9 BR-P9-001 | AC2; TC-P9-E1013-CON-02 |
| BR8 | A GET declares no `Idempotency-Key`; the reference-load element of the definition table declares its rule and is carried as the legacy operation's target form | Architecture v5 slide 11; TSD P9 T-A.2; GAP-2568 | AC4; TC-P9-E1013-CON-07 |
| BR9 | No personal data in a schema, an example or a fake: measure codes, dimension values, dates, counts, amounts and a definition version only | Template and Rules v1 §R7.2 (s17); legacy §17 | AC6; TC-P9-E1013-CON-05 |
| BR10 | One REST base, one topic, one queue, one schema and one login per service; the document never declares another service's base or topic as its own | DP-13, DP-14; Template and Rules §R4 | AC1; TC-P9-E1013-CON-01 |
| BR11 | A schema change is additive within major version 1; a breaking change is a new major version | Architecture v5 slide 42 notes (BACKWARD compatibility) | AC6; TC-P9-E1013-CON-05 |
| BR12 | The frozen row is the database's as well as the service's: the contract fixes the `frozen` and `is_baseline` flags and the unique key that makes a snapshot row single | TSD P9 T3.1; legacy BR2 | AC2; TC-E1-013-05 |
| BR13 | The document lists only operations owned by rwb-reporting; a consumed operation is described as consumed and faked, never as provided | Ownership Map; DP-11 | AC1; TC-P9-E1013-CON-01 |

### 9. State transitions

The lifecycle of this document, not of a measure:

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The two reads, the three elements, the six lists, the consumed rows, the decision element, the Schedule and the fakes are described | In review |
| In review | Consumer sign-off | The app story, the P3 facts and reference rows, the P1 payments row, the deployment story and the wave 1 harness accept the document and the fakes | Baselined |
| Baselined | Additive change | A property is added within major version 1, for example an optional dimension filter | Baselined |
| Baselined | Breaking change | A property is removed, renamed or retyped, or a list value changes | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A forbidden element appears | The absence tests of AC3, AC5 and AC6 fail: a `v_ace_*` view, a `recovery_case` property, an event, a consumer group, a second Schedule or a lake path | In review |

The state machine the document describes is the app story's: the definition version in force, the snapshot written, the baseline and frozen flags, the publish state and the run state. This baseline fixes the vocabulary and the enums and moves no measure.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-reporting | Owns the OpenAPI document and the contract tables; tags the baseline |
| Solution architect | Approves a breaking change, a new major version, and the correction of the plan rows this baseline consumes, including the two rwb-source-data rows and the event question |
| Consuming teams (the app story, the P3 facts and reference-data stories, the P1 payments story, the deployment story and the wave 1 harness) | Review and sign off the parts they consume |
| Platform library owner | Owns the error envelope, the paging convention, the naming rule, the decision-record library and the workflow kit this document reuses |
| Data steward | Confirms that no personal data field is declared in an answer, an element or a fake |

The per-service login behind the security scheme is named "the rwb-reporting login (DP-02)" and is not part of this baseline.

Every operation of this baseline is authorised by the rwb-access authorise check (DP-08) before its read or write; the five roles above reach an operation only through that check.

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content | BR Field ID |
|---|---|---|
| Definition element | The columns of DF-RPT-031 to DF-RPT-040: `id`, `measure_code`, `name`, `formula`, `data_product`, `unit`, `definition_version`, `approved_by`, `approved_at`, `valid_from` | BR1 |
| Snapshot element | The columns of DF-RPT-041 to DF-RPT-052: `id`, `measure_code`, `definition_version`, `business_date`, `product_group`, `dimension_code`, `dimension_value`, `value`, `case_count`, `is_baseline`, `frozen`, `published_at` | BR12 |
| Publish element | The columns of DF-RPT-053 to DF-RPT-058: `id`, `business_date`, `status`, `case_list_count`, `dashboard_count`, `held_reason` | BR1 |
| Required flags | The three rows of AC2, with the other properties optional | BR1 |
| Lists | `LOV-DATA-PRODUCT` (DP01 to DP14), `LOV-MEASURE-DIM` (ROUTE, AGE_BAND, QUEUE, STAGE, AGENT), `LOV-MEASURE-PUBLISH` (PUBLISHED, HELD), `LOV-MEASURE-UNIT` (COUNT, THB, DAYS, PERCENT) and `LOV-PRODUCT` (MORTGAGE, HIRE_PURCHASE, SSME, UNSECURED), published as enumerations and read as reference data at their version | BR7 |
| Event data | None of this service: no event is declared (§12.3) | BR5 |
| Decision record | DF-DEC-001 to DF-DEC-031 through the local library, written before the snapshot commits (DP-03) | BR2 |
| Case and payment facts | DF-CAS-001 to DF-CAS-026, `queue` and the reference rows of P3, and the payment facts of the P1 read, declared as consumed and never written, copied or joined here | BR3 |
| Not declared here | `recovery_case`, `queue`, `case_account` and the reference rows (P3), every `v_ace_*` view (P1), `decision_log_entry` (P7), and the dashboard elements of RWB-P9-E2009-APP | BR13 |
| Consumed fields with no source | The path and shape of the definitions read and the field list inside the reference-list read: Not specified in the source documents (GAP-2572; ASM-4238). The approver's type: TSD uuid against the legacy reference "TRB-0001" (GAP-2571; ASM-4237) | BR13 |

The field-level types, lengths and required flags of the added elements are settled in the baseline review and follow TSD P9 T3.1; this story fixes the element names, the vocabulary of AC2 and the optionality rule of BR11. **No new table, no new column and no migration** is declared by this story.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-reporting (P9); base `/api/recovery/reporting/v1` (DP-13).

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| GET | `/reports/measures` | Measure list of status 200 out, filtered by `measure`, `product`, `route`, `from` and `to`; each element carries the measure code, the definition version, the business date, the product group, the dimension code and value, the value or the case count and the freshness stamp (API-P9-001) | Reporting, right R, scope applied | Not declared |
| GET | `/measure-definitions` | The definitions in force on `onDate`, each with its measure code, name, data product, formula, unit and version; the read RWB-P3-E1013-APP consumes | Reporting, right R, scope applied | Not declared |
| The reference-load element of the definition table (operation name and path Not specified in the source documents (GAP-2568; ASM-4234)) | under the same base | A definition file in, the version in force out, with the all-or-nothing rule of BR4 | Reference data, right C, scope applied | `Idempotency-Key`, carried from the legacy operation's rule |

The three answer 400 and 422 with MSG-GEN-001, 401 with MSG-P4-001, 403 with MSG-P4-002, 404 with MSG-P4-003 and 503 with MSG-GEN-006, each as `application/problem+json` with the `messageCode` (RD-P1-004). The reference-load element also answers 400 MSG-PLT-N009-03, 409 MSG-PLT-N009-05 and 503 MSG-PLT-N009-06 for its `Idempotency-Key`, and replays the stored answer for 24 h (RD-P1-001). The published rwb-reporting.yaml 5.1.0 holds `GET /reports/measures` only: the definitions read, the 422 element and the reference-load element are to be added with this baseline. The operation ID API-P9-001 is that of TSD P9 T-A.1 and the paths are those of the target base, not the monolith form. RWB-P9-E2009-CON publishes the delta of this operation — `baselineValue`, the dimension as code and value and the `X-Data-As-Of` freshness header — on top of this baseline, and does not restate it. The definitions read is the legacy `MeasureCatalog` interface turned into a contract, because RWB-P3-E1013-APP consumes it across a service boundary; no source gives its path or its shape, so the path is declared here and the gap is recorded (GAP-2572; ASM-4238). The legacy story assigns `GET /reports/measures` to RWB-E2-009 while the Ownership Map gives it to this service; the shape is declared here for the wave 1 harness and the dashboard's use of it stays RWB-P9-E2009-APP's (GAP-2570; ASM-4236).

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| GET | `/api/recovery/case/v1/cases/facts` | P3 rwb-case | The nine fact fields, the as-of time, the row count and the reference version of one business date (RWB-P3-E1013-APP); faked |
| GET | `/api/recovery/case/v1/cases/{caseId}` family | P3 rwb-case | The case record and its account link (RWB-P3-E1018-CON); faked |
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case | The five closed lists at their version in force (RWB-P3-E1043-CON); faked |
| GET | `/api/recovery/source-data/v1/payments?accountKey={accountKey}` | P1 rwb-source-data | `PaymentsAnswer` of rwb-source-data.yaml 5.1.0. Account-form rows are ordered by `paymentDate` then `paymentCode`; `businessDate` is the DP01 stamp. Interim unpaged. 409 MSG-P1-001 when gated. Pending: since-entry rule and caller identity (GAP-3427). |
| GET | `/api/recovery/source-data/v1/data-products/freshness?asOf={date}` | P1 rwb-source-data | `DataProductFreshness` elements of rwb-source-data.yaml 5.1.0: `productCode`, `businessDate` (nullable, null only when never stamped) and `status` `LOADED` or `STALE`; the stamp in use is the latest row (RWB-P1-E1015-CON). The local run completeness evaluation is Pending (GAP-3434). The gate value COMPLETE or HOLD has no member (GAP-3434); the product codes of the run are Pending (GAP-3383); faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The two rwb-source-data rows are contract dependencies of class C that the plan's C row does not carry, and the absence is recorded (GAP-2567; ASM-4233).

The readiness pair of rwb-source-data is published by RWB-P1-E1015-CON (RD-P1-022) and is not consumed here. The activity `snapshot(page)` on task queue `rwb-source-data` has the measures build of this service as its caller in Temporal Workflow and Activity Catalog v3 (RD-P1-002); whether the run calls it beside the five REST rows is Pending (GAP-3384), and its fields are Pending (GAP-3425; GAP-0563). `listEligibleAccounts` is not consumed: `DailyCaseRun` of rwb-case is its only caller (RD-P1-010).

#### 12.3 Events published

None. The Ownership Map and the context pack give rwb-reporting the topic `rwb.reporting.events.v1` with its retry and `.dlt` topics by the naming rule and no event row, so this baseline declares no event, no producer group and no outbox row, and the absence test of AC5 fails a build that adds one. The wave 1 harness names `rwb.reporting.ReportPublished.v1` on that topic as its freshness signal; the event belongs to whoever publishes it and is recorded as a conflict here (GAP-2569; ASM-4235). The decision record travels on the platform topic `rwb.decision-record.v1` through the library and is not an event of this service. No data lake path, no extract element and no trailer is declared (GAP-2566; ASM-4232).

#### 12.4 Events consumed

None. The run is started by the Airflow report-run call while the Schedule is paused (RD-P1-066), and the facts are read on the five consumed rows; this baseline declares no consumer group, no subscription and no inbox of its own, and the absence test fails a build that adds one. A later source that arrives late is picked up on the next daily call, and the wave 1 harness waits on the reads.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `MeasureRunWorkflow` | Workflow, one execution per business date, declared not built | `rwb-reporting` in namespace `rwb-recovery` | Input: the business date, the baseline date, the definition version in force and the gate answer; output: the row count, the publish state and the outcome. No child workflow and no signal from another service |
| `measureRun` | Activity, the read, compute, freeze and publish step | `rwb-reporting` | The facts, the payments and the gate answer in; the snapshot rows, the record, the publish state and the run outcome out |

No child workflow and no saga exists in this capability. The frozen baseline is not written back to rwb-source-data or to this service: this service serves the measure snapshot for a business date whose ACE batches are complete, and rwb-reporting publishes the baseline and freezes it (GAP-1503). No data lake path and no extract element is declared in this contract (DP-17, GAP-2566). One Temporal Schedule of DP-10 runs MeasureRunWorkflow, and the JOB-15 entry is the Airflow report-run call; the run is at 01:30 Asia/Bangkok and the Schedule is created paused (12.6; RD-P1-066; GAP-3573). The two names are the target design choice of this baseline; the element names of the two activity contracts are Not specified in the source documents (GAP-2577) and carry the review placeholder for the owners of the consumed services; the activity `snapshot(page)` is registered by RWB-P1-E1013-APP for the measures (invocation Pending, GAP-3384), and `listEligibleAccounts` is built by RWB-P1-E1018-APP for rwb-case only and is no element of this baseline (RD-P1-010).

#### 12.6 Schedules

One paused Schedule, declared and registered by the deployment story: the run of JOB-15 at 01:30 Asia/Bangkok for the previous business date, one run per date, catch-up of one missed run, no overlapping execution, on `rwb-reporting` in namespace `rwb-recovery`. It replaces the Quartz row of the legacy job (DP-10). The Schedule ID is a target choice and no source gives it; the legacy job ID JOB-15 is kept in the record and on SCR-44. Airflow calls `POST /reports/{id}/run` at 01:30 Asia/Bangkok for the prior business date. Create the JOB-15 Temporal Schedule paused. Pending final trigger owner: solution architect with the rwb-reporting owner (GAP-3573).

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| measure_definition | P9 (`rwb_reporting`) | The agreed definition of a measure by version, the table the definitions read answers from |
| measure_snapshot | P9 (`rwb_reporting`) | The value of one measure for a date, product and dimension value, with the baseline and frozen flags and the unique key |
| measure_publish | P9 (`rwb_reporting`) | The publish or hold state of a business date with its two counts and its reason |
| decision_record, idempotency_key, outbox_event | PLT library, created in `rwb_reporting` | The local run record, the repeat key and the library object that carries no row because no event is published (§12.3) |

`recovery_case`, `queue`, `case_account` and the reference rows (P3), every `v_ace_*` view (P1), `decision_log_entry` (P7) and the dashboard elements of RWB-P9-E2009-APP are not owned by this baseline; it names them only as consumed rows, and no foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case case-facts fake | The 120 cases of 2026-11-27 with the nine fact fields, the as-of time and the reference version; a date with no case; no answer beyond 2 s | AC3, AC6 |
| rwb-case case-record and reference-list fake | The account link of a case and the five closed lists at their version; a list version that answers nothing | AC3, AC6 |
| rwb-source-data payments and freshness fake | The payments of an account for 2026-11-30 (PaymentsAnswer, RD-P1-061); freshness elements with status `LOADED`, `STALE` with a `businessDate` and `STALE` with `businessDate` null; no answer beyond 2 s | AC3, AC6 |
| Local decision-record stub (`RWB-PLT-E1027-CON`) | A healthy chain and outbox, and a stopped chain | AC5, AC6 |
| gateway-bff composite route fake | The merged SCR-44 answer with the run of 2026-11-27 in its complete state | AC6 |
| Frozen-row fixture | A snapshot row with `frozen = true` and an UPDATE and a DELETE against it | AC2, AC5 |

The fakes are test-only and are replaced by the real services in SIT. The paths of the definitions read and of the reference-load element are derived from this baseline and carry the placeholder until the owners confirm them (GAP-2568, GAP-2572; ASM-4234, ASM-4238).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 3 provided, 5 consumed | The two reads and the reference-load element on `/api/recovery/reporting/v1`; the facts read, the case record read, the reference-list read, the payments read and the freshness read; one hop, 2 s |
| Kafka | 0 published, 0 consumed | No event of this service; the record is the library's on `rwb.decision-record.v1` |
| Temporal | 1 workflow, 1 activity and 1 Schedule declared, 0 registered | `MeasureRunWorkflow`, `measureRun` and the 01:30 Schedule on `rwb-reporting` |
| File | None | No extract, no trailer and no lake path (DP-17) |

### 13. Solution plan

**The CON declares shapes and moves nothing.** It writes no code, no migration and no table, and it changes no measure, no definition and no publish state. What it publishes is one OpenAPI 3.1 document, nine contract tables and six fakes.

**Deliverables.** The additive document `openapi/rwb-reporting-v1.yaml`, the three elements with their required flags, the six lists as published enumerations, the contract README rows for the five consumed rows and their placeholders, the decision-record element, the Schedule element and the six fakes of 12.8.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_reporting`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none; declared as a prohibition |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/reporting/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-17 | Data lake, INT-19, INT-20 | Removed (no data lake); reporting from events into rwb-reporting | none; the absence test is the gap GAP-2566 |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is declared as the element of the run record written before the snapshot commits. DP-07 is declared for the five lists and their version. DP-10 is declared as the Schedule element. DP-11 is declared five times: each in-process interface of the legacy §12 becomes a contract with a fake. DP-13 moves the base and nothing else. DP-17 removes the lake, its extract and its trailer and the absence of a lake element is tested. DP-19 sits behind SCR-44, whose screen model is the edge contract's.

**Dependencies the table adds and the plan does not hold.** The pattern table names the six H rows the plan carries. The two rwb-source-data consumed rows are C dependencies in fact and not in the metadata row (GAP-2567; ASM-4233). No DP-09 row is claimed, because this service declares no event and uses no outbox row (§12.3).

**Build steps**

1. Write the two reads and the reference-load element and validate the additive rule of AC1 in the pipeline.
2. Write the three elements, their required flags and the six lists of AC2, with the placeholder where a type is unstated.
3. Record the five consumed rows of AC3 with their owner, their class and their placeholders.
4. Record the rights, the error envelope and the reference-load element of AC4.
5. Record the decision-record element, the Schedule element and the absence of an event of AC5.
6. Publish the six fakes of AC6 and the drift test.
7. Record the naming baseline and the boundary, then tag the baseline and collect the consumer sign-off.

**Done when.** The OpenAPI document validates in the pipeline, the six contract tests pass, the fakes answer every consumed path and the drift test is green, and the app story, the P3 facts story, the P1 payments story, the deployment story and the wave 1 harness have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required field of a request or a definition row is absent or invalid, or a body fails schema validation | Enter {field}. |
| MSG-P9-001 | The contract describes a publish for a frozen business date | The baseline for {date} is frozen. It cannot be published again. |
| MSG-P1-001 | The contract describes a gate answer that is HOLD for a stale product | {product} is from {date}. Today's load has not arrived. |
| MSG-GEN-006 | The contract describes a held publish | {system} is not available. Try again in a few minutes. |
| MSG-P9-003 | The contract describes a measure listed for a run with no definition in force | {measure} has no approved definition. It is not published. |
| MSG-P7-003 | The decision record cannot be written before the snapshot commits | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | The role lacks the Reporting or the Reference data right the operation declares | You cannot {action} here. Your role does not include it. |
| MSG-P4-001 | No valid session or no Recovery Workbench role (401) | Your session is not valid or you have no Recovery Workbench role. Sign in again or ask your team manager to request one. |
| MSG-P4-003 | The record does not exist or is outside the scope (404) | This case is not in your scope. |
| MSG-PLT-N009-03 | The reference-load element has no valid `Idempotency-Key` | The Idempotency-Key header is required and must be valid for {operation}. |
| MSG-PLT-N009-05 | The key conflicts with another request | The Idempotency-Key conflicts with another request to {operation}. |
| MSG-PLT-N009-06 | The key store is unavailable | The idempotency store for {operation} is unavailable. No changes were saved. Try again in a few minutes. |

The message IDs and the text are the legacy and FSD wording, except MSG-GEN-006, which takes the English text of Error and Message Standard v6; MSG-P4-001, MSG-P4-003 and the three MSG-PLT-N009 codes are the platform answers of RD-P1-001 and RD-P1-004, and no new message is added. MSG-GEN-006 names a system that in the target is the publish step of the read model and not a data lake (GAP-2566; ASM-4232).

### 15. Screens and states

The contract serves SCR-44 Interface and job monitor in its running, held, failed and complete states through the gateway-bff composite route (DP-19). The empty, loading, error and no access states of SCR-44 are Not specified in the source documents (CG-ALL-7822). The route calls rwb-reporting for the run, its publish state and its freshness stamp, rwb-case for the facts state and rwb-source-data for the freshness status (the gate value is Pending, GAP-3434); this baseline fixes the rwb-reporting answers only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON. SCR-37 Steering dashboard and the report built from the snapshot are RWB-P9-E2009-APP's and the Reporting and BI analyst's, and the refusal, held and not-recorded states read the messages of section 14. The empty, loading, error and no access states of SCR-37 are Not specified in the source documents (CG-ALL-7821).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-013-01 | AC1 | Contract | Definition file of 6 rows approved by TRB-0001; the definition element and the definitions read answer it |
| TC-E1-013-03 | AC3 | Contract | JOB-15 on 2026-12-02 for business date 2026-12-01; the snapshot and publish elements, the Schedule element and the absent lake path |
| TC-P9-E1013-CON-07 | AC4 | Contract | TIME_IN_STAGE with no formula; the reference-load element and its MSG-GEN-001 answer |
| TC-E1-013-05 | AC2, AC5 | Contract | JOB-15 rerun for 2026-11-27; the frozen flags, the unique key, the record element and the Schedule |
| TC-E1-013-07 | AC5 | Contract | The held publish element and MSG-GEN-006; the absence of a lake element and of an outbound batch |
| TC-E1-013-08 | AC3, AC4 | Contract | COST_PER_CASE with no definition; the publish element and the MSG-P9-003 answer |
| TC-E1-013-09 | AC4 | Contract | RW-BIANAL calls the reference-load element; 403 with MSG-P4-002 in the envelope |
| TC-P9-E1013-CON-01 | AC1 | Contract | The document validates; the two reads, the base, the query parameters and the seven error answers |
| TC-P9-E1013-CON-02 | AC2 | Contract | The three elements validate with their columns, the required flags and the six closed lists |
| TC-P9-E1013-CON-03 | AC3 | Contract | The five consumed rows and their placeholders; no `v_ace_*`, no `recovery_case` and no rule row |
| TC-P9-E1013-CON-04 | AC5, AC6 | Contract | The decision element, the Schedule element, the absent event and the absence test |
| TC-P9-E1013-CON-05 | AC6 | Contract | The six fakes match the document, a drifted fake fails the build and the naming baseline holds |
| Not specified in the source documents (NEWAC-RWB-P9-E1013-CON-AC9) | AC9 | Contract | Not specified in the source documents (NEWAC-RWB-P9-E1013-CON-AC9) |
| TC-P9-E1013-CON-06 | AC2 | Contract | Boundary of the tables of §12.7: the owned tables only, the consumed rows never written, no foreign key leaves the schema (DP-01) |

The seven legacy cases are the legacy cases of RWB-E1-013 for the criteria this story fixes, in their legacy order, carried as the contract half: their Covers column names the criteria that fix the surface each one exercises, and the business outcome of each is proved by RWB-P9-E1013-APP. The legacy level System maps to `Contract` here because the artefact under test is the contract, and Access maps to `Contract` for the same reason. The six cases `TC-P9-E1013-CON-01` to `-06` are new. **TC-E1-013-02 and TC-E1-013-06 are not here**: they belong to RWB-ITG-E1013-ITG. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. In the staged Test Cases v9.xlsx only TC-E1-013-08 is still a row of this key and the other TC-E1-013 IDs hold rows of RWB-P1-E1013-APP, so the version 3 changes to AC1, AC3, AC4 and AC6 and the rows of this story are the mapped cases in this section.

### 17. Guardrails

- No business value in the contract: the measure codes, the formulas, the units, the bands, the baseline date and the product groups are data, reference data or definition rows, never a schema default or an enumeration member of the code.
- No personal data in a schema, an example or a fake: measure codes, dimension values, dates, counts and amounts only, and every example is synthetic.
- The facts stay with their owners: the document declares no `v_ace_*` path, no `recovery_case` property, no reference-row write and no ACE table read (BR3).
- No lake path, no extract element and no trailer: a build that declares one fails the absence test (BR6).
- One base, one topic, one queue, one schema and one login per service; a document that names another service's base or topic as its own fails the review (DP-13, DP-14).
- The document lists only operations owned by rwb-reporting; a consumed operation is described as consumed and faked, never as provided (DP-01, DP-11).
- No retired element is reintroduced: no Quartz row, no shared job table, no published event and no consumer group (BR5, DP-10).
- The error envelope, the paging convention, the naming rule, the decision-record library and the workflow kit come from the platform; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-RDF-012 | Baseline measures published with definitions agreed by the Tribe | The three elements, the two reads and the five consumed rows on which the baseline is computed | TC-E1-013-01, TC-E1-013-03, TC-P9-E1013-CON-01, TC-P9-E1013-CON-02, TC-P9-E1013-CON-03, TC-P9-E1013-CON-06 |
| NFR-065 | Business measures come from the Workbench records and the decision log | The facts, payments and freshness rows and the record element | TC-E1-013-03, TC-P9-E1013-CON-03 |
| ADR-014 | Schema and login per service | `rwb_reporting` and its own login | TC-P9-E1013-CON-05 |
| ADR-015 | Kafka with outbox, inbox and CloudEvents | The topic named by the naming rule and the absent event | TC-P9-E1013-CON-04 |
| ADR-018 | No data lake; rwb-reporting read model | The publish element and the absent lake path | TC-E1-013-07, TC-P9-E1013-CON-04 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The five consumed rows with their budget and breaker | TC-P9-E1013-CON-03 |
| ADR-022 | Local decision record plus central ledger | The decision-record element | TC-E1-013-05, TC-P9-E1013-CON-04 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E1-013, disposition Split (rework); features FEAT-RDF-19 and FEAT-RPT-01 |
| Legacy criteria | AC1, AC3, AC4, AC5, AC7 and AC8 owned word for word by RWB-P9-E1013-APP; AC2 and AC6 by RWB-ITG-E1013-ITG; this baseline copies none of them |
| Source text | The legacy story, FSD P9 Reporting v3 A2.1 and A2.8, and TSD P9 Reporting v2 T3.1, T3.2 and T-A |
| Test cases | The seven legacy cases as the contract half, and the six new contract cases TC-P9-E1013-CON-01 to -06 |
| Feature and screens | FEAT-RDF-19, FEAT-RPT-01; SCR-44 |
| Decoupling patterns | DP01, DP03, DP05, DP07, DP10, DP11, DP13, DP15, DP17, DP19 |
| Architecture decisions | ADR-014, ADR-015, ADR-018, ADR-020, ADR-022, and ADR-016 for the Schedule |

### 19. Out of scope

- The behaviour behind the two reads, the six calculators, the snapshot, the freeze and the publish state: RWB-P9-E1013-APP.
- The case facts of a business date and their banding: RWB-P3-E1013-APP. The case record and the reference lists: RWB-P3-E1018-CON and RWB-P3-E1043-CON.
- The payments since entry: RWB-P1-E1013-APP. The freshness stamp and the gate answer: RWB-P1-E1015-APP, published in RWB-P1-E1015-CON.
- The registration of the Schedule, the chart, the migration job, the panels, the alerts and the run books: RWB-P9-E1013-OPS.
- The steering dashboard SCR-37, its data set and the agent measures: RWB-P9-E2009-APP.
- The cross-service proof of AC2 and AC6 and the `-ITG` copies of these test cases: RWB-ITG-E1013-ITG.
- The event question, whether this service ever publishes `rwb.reporting.ReportPublished.v1`: an owner decision, recorded as a conflict and not declared here (GAP-2569; ASM-4235).
- The data lake, INT-19 and INT-20, the extract and its trailer: removed by Arch v5 and DP-17, and no baseline rebuilds them.
- The composite route and the screen field list of SCR-44: RWB-PLT-N001-CON and the edge stories.

### Remaining delivery steps

- Agree the payments shape and fake with the rwb-source-data contract owner and close GAP-3426, GAP-3427 and GAP-3518.
- Close GAP-3434, GAP-3383 and GAP-3384 (solution architect).
- Add the definitions read, the 422 and the reference-load element to rwb-reporting.yaml (rwb-reporting tech lead).
- Give this story its rows in Test Cases v9 (QA lead).
- Size the story at refinement (squad).
- Epic design sign-off (solution architect).
- Consumer sign-off, contract Done and the fakes published (rwb-reporting squad).
- Test data in DEV (QA lead).
