# RWB-ITG-E1013-ITG Baseline measures

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-E1013-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W1 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-013 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP05, DP07, DP10, DP11, DP13, DP15, DP17, DP19 |
| Parallel lane | L-ITG-W1 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | RWB-P3-E1018-APP, RWB-P9-E1013-APP, RWB-P3-E1013-APP, RWB-P1-E1013-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to REQ-RDF-012) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: integration slice of RWB-E1-013 for RWB-ITG-W1. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **QA integration engineer**, I want **the baseline measures of RWB-E1-013 proven end to end across rwb-case (P3), rwb-source-data (P1) and rwb-reporting (P9) on their published contracts — the synthetic case set and the ACE batch of business date 2026-11-27 seeded through rwb-case and rwb-source-data, the measure definition of version MD-2026.11 in force, the 01:30 JOB-15 run publishing the baseline, the baseline frozen, and the daily gate holding the publication when the ALS batch of that date is not COMPLETE**, so that **the cross-service criteria no single service can prove are signed off before wave 1 exits**.

### 2. Business rationale

Measures are counted by hand at month end today and each team counts a case differently, so the baseline is only worth having if the chain that produces it is proven on the services that will run it. RWB-E1-013 owns REQ-RDF-012 and the frozen baseline of business date 2026-11-27.

This integration slice owns two of the eight legacy acceptance criteria: **AC2 Baseline published** and **AC6 Batch of the baseline date not complete**. The other six sit with the sibling app stories: **RWB-P9-E1013-APP** owns AC1 (the definition file of 6 rows and the version in force), AC4 (a definition without a formula refused in full), AC5 (the baseline published twice), AC7 (the publish held when the delivery path does not answer) and AC8 (a measure with no definition in force); **RWB-P3-E1013-APP** owns the case-fact side the baseline is counted from — route, stage, queue, entry date and stage clock start of the 120 synthetic cases; **RWB-P1-E1013-APP** owns the ACE view contract, the payments since entry and the freshness and gate side that AC2 and AC6 read through. **RWB-P3-E1018-APP** is the case creation of JOB-02 that fills the synthetic set.

None of the two owned criteria can be signed off inside one service. AC2 needs a case set that rwb-case created, a COMPLETED ALS row that rwb-source-data reads from the ACE views, a definition that rwb-reporting holds in force, a 01:30 run that reads the case facts through the P3 contract and the payments through the P1 contract, and a snapshot that is written once and frozen. AC6 needs the same chain with the gate answering HOLD, no baseline row written and the run record naming the stale product and date. A fake proves the arithmetic of a calculator; it cannot prove that a case created through rwb-case reaches a measure through two contracts, or that a missing ACE batch stops the publication.

The target changes the last hop only. **DP-17 removes the data lake**: there is no INT-19 extract to a lake. rwb-reporting projects the facts from its events and from the P1 snapshot activity and publishes on `rwb.reporting.events.v1` with ReportPublished, and **rwb-integration delivers the regulatory extract**. The measure values, the definition version, the baseline date and the gate are unchanged; the suite therefore asserts the same AC2 and AC6 values and the v5 publication path in place of the lake step (GAP-0339; ASM-0433).

Service contracts are not faked in this story. Every call and every event is made to the real service, on the real base and the real topic, in SIT; the only fakes are the ACE batch fixture and the Airflow trigger that stands in for the bank scheduler.

### 3. Preconditions

- RWB-P3-E1018-APP is done: case creation writes the case record and the case facts of JOB-02 through the rwb-case path, and `GET /api/recovery/case/v1/cases` answers them.
- RWB-P9-E1013-APP is done: measure_definition, measure_snapshot, the definition load, the measures Schedule, the publication on `rwb.reporting.events.v1` and `GET /api/recovery/reporting/v1/reports/measures` exist in rwb_reporting.
- RWB-P3-E1013-APP is done: the case facts of route, stage, queue, entry date and stage clock start are served on the P3 contract for a business date.
- RWB-P1-E1013-APP is done: the 30 `recovery.v_ace_*` views, the ACE batch record, the payments since entry, the freshness and the readiness trigger are served by rwb-source-data.
- Each owner has published its contract: the OpenAPI document of P1, P3 and P9 and the AsyncAPI document of the three consumed topics.
- The harness **RWB-ITG-W1J01-ITG** is available and its synthetic data set is loaded: the 120 open cases of business date 2026-11-27 with 60 Mortgage, 45 Hire purchase and 15 SSME, the payments since entry that total 4,350,000.00 THB, and the ACE batch rows of the fixture dates.
- SIT is in place: namespace `rwb-recovery`, the task queues `rwb-case`, `rwb-source-data` and `rwb-reporting`, the topics `rwb.source-data.events.v1`, `rwb.case.events.v1` and `rwb.reporting.events.v1` with their retry and `.dlt` topics, and the schema registry with BACKWARD compatibility.
- The six definitions of version MD-2026.11 are approved and can be loaded through the P9 path; the baseline date is configured on rwb-reporting as 2026-11-27.
- No production data and no production namespace: the suite runs on synthetic data in SIT only.
- Release 30 November 2026 is tentative, and a date is never a blocker for this story.
- No build dependency: the story is Day 1 under Template and Rules §R5.7, and the four integration dependencies never block a build.
- The v5 publication path replaces the INT-19 lake step; the exact composition of the fixture files is Not specified in the source documents (GAP-0339; ASM-0433).

### 4. Flow

1. Harness: runs the preflight of section 13 — the four services answer their health and contract check, the three topics and their retry and `.dlt` topics exist, the schema registry holds the three event versions, the three task queues are registered in `rwb-recovery`, and the JOB-15 Schedule is present; a missing element stops the run before any test.
2. Harness: seeds the synthetic case set of business date 2026-11-27 through the rwb-case creation path, and seeds the ACE batch rows of the fixture dates through the W1J01 ACE batch fixture, so that the batch record answers a COMPLETED ALS row for 2026-11-27.
3. Harness: loads the measure definition of version MD-2026.11 with the 6 rows through the P9 measure-definition path published by RWB-P9-E1013-APP, and reads the version in force back through `GET /api/recovery/reporting/v1/reports/measures`.
4. Harness: triggers the readiness signal with `POST /api/recovery/source-data/v1/business-days/2026-11-27/ready` through the Airflow trigger stub, and waits for one `rwb.source-data.AceDataReady.v1` on `rwb.source-data.events.v1`.
5. System: rwb-source-data publishes AceDataReady, rwb-case starts DailyCaseRun for JOB-02 and the cases of the date exist, and rwb-case publishes `rwb.case.CaseCreated.v1` on `rwb.case.events.v1` which rwb-reporting projects.
6. Harness: asserts the daily gate and the case facts on the contracts only — `GET /api/recovery/source-data/v1/data-products/freshness` for the gate and `GET /api/recovery/case/v1/cases` for the 120 cases of 2026-11-27, and never reads a service table.
7. Harness: triggers the JOB-15 measures run once for 01:30 on 2026-11-28 through the P9 run path, waits for the workflow to complete, and collects the `rwb.reporting.ReportPublished.v1` events of the run from `rwb.reporting.events.v1`.
8. Harness: asserts AC2 through `GET /api/recovery/reporting/v1/reports/measures` — the rows of business date 2026-11-27 carry definition version MD-2026.11, the baseline flag and the frozen flag; CASES_BY_ROUTE is 120 cases of which 60 are Mortgage; REALIZED_RECOVERY equals the synthetic payments since entry of 4,350,000.00 THB, read through `GET /api/recovery/source-data/v1/payments?accountId={accountId}` and summed by the harness.
9. Harness: asserts AC6 on a second synthetic set with no COMPLETED ALS row for business date 2026-11-27 — the gate answers HOLD, the run writes no baseline row for the date, the run record carries MSG-P1-001 naming "DP03 Case" and 2026-11-26, and the baseline appears at the first JOB-15 run after the ALS batch of 2026-11-27 is COMPLETED.
10. Harness: writes the evidence report of AC2 and AC6 with the payload references, the measure values and the run identifiers, resets the synthetic set to its fixture state for a repeatable rerun, and publishes the evidence to the wave 1 exit gate.

The suite never writes another service's table and never calls another service through a service: every assertion is made on a contract response or on an event, and every write it needs is a call to the owner's own path.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A published contract of P1, P3 or P9 differs from the version the suite was built against (contract drift) | The preflight fails on the contract check, the suite names the service, the operation and the differing element, and no test runs | None | AC2, AC6 |
| X2 | No `rwb.source-data.AceDataReady.v1` arrives after the readiness call | The harness waits out the configured window, records the missing event and fails; DailyCaseRun is not started and the case facts of the date are absent | None | AC2, AC6 |
| X3 | No measure definition is in force for a measure of the configuration | rwb-reporting publishes no value for that measure and lists it in the run record | MSG-P9-003 | AC2 |
| X4 | JOB-15 runs a second time for business date 2026-11-27 | The frozen baseline rows are unchanged and the run record shows the refusal naming 2026-11-27 | MSG-P9-001 | AC2 |
| X5 | The daily gate answers HOLD because the ALS batch of the business date is not COMPLETE | No baseline row is written for the date, the run record names the stale product and date, and the baseline is published by the first run after the batch is COMPLETED | MSG-P1-001 | AC6 |
| X6 | A consumed event lands on the `.dlt` topic | The harness names the event id, the topic and the failure, and fails the criterion that expected the event | None | AC2 |
| X7 | A fixture of the synthetic data set is missing or not idempotent | The preflight stops the run before any test and names the missing fixture file; the suite is never run on a partial set | None | AC2, AC6 |
| X8 | The suite looks for an INT-19 data-lake assertion or a Power BI refresh | The step does not exist: the suite asserts the v5 path instead — ReportPublished on `rwb.reporting.events.v1` and the regulatory extract delivered through rwb-integration | None | AC6 (GAP-0339; ASM-0433) |

X1 to X7 are the failure modes of the chain the two owned criteria assert. X8 is the record that the legacy lake step is not part of the wave 1 suite (DP-17).

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | A test project of its own; it needs the four integration services, the three topics and the Schedule, and it owns no schema, no table and no operation |
| Negotiable | Fixture size, wait windows, retry counts and report layout are configuration; the measure values, the definition version, the baseline date, the message IDs and the run order are fixed by the legacy story |
| Valuable | Proves across services what no single service story can prove: a baseline published once and frozen, and a gate that stops the publication |
| Estimable | One suite, two feature files, four fixture groups, two runs (published, held) and one evidence report |
| Small | Fits one sprint with the report |
| Testable | Every criterion is asserted on an observable: a contract response, an event, a run record or a measure value |

### 7. Acceptance criteria

```gherkin
Feature: Baseline measures, proven across rwb-case, rwb-source-data and rwb-reporting

  Background:
    Given the synthetic case set for business date 2026-11-27 holds 120 open cases: 60 Mortgage, 45 Hire purchase and 15 SSME
    Given age bands are "0-90", "91-180", "181-365", "366-730" and "over 730" days since entry
    Given all wave 1 services are deployed in SIT with their published contracts
    Given the synthetic data set of the harness RWB-ITG-W1J01-ITG is loaded

  Scenario: AC2 Baseline published (legacy RWB-E1-013 AC2)
    Given v_ace_batch_status holds a COMPLETED ALS row for business date 2026-11-27
    When JOB-15 runs at 01:30 on 2026-11-28
    Then measure_snapshot holds rows for business date 2026-11-27 marked baseline and frozen with definition version "MD-2026.11"
    Then "CASES_BY_ROUTE" totals 120 cases, of which 60 are Mortgage
    Then "REALIZED_RECOVERY" equals the sum of synthetic payments since entry, 4,350,000.00 THB

  Scenario: AC6 Batch of the baseline date not complete (legacy RWB-E1-013 AC6)
    Given v_ace_batch_status holds no COMPLETED ALS row for business date 2026-11-27
    When JOB-15 runs at 01:30 on 2026-11-28
    Then the system writes no baseline rows for 2026-11-27
    Then the run record shows MSG-P1-001 naming "DP03 Case" and 2026-11-26
    Then the system publishes the baseline by the first JOB-15 run after the ALS batch for 2026-11-27 is COMPLETED
```

**Target reading.** The views named in the criteria (`v_ace_batch_status`) are read only by rwb-source-data, and the suite asserts them through the P1 contract of RWB-P1-E1013-APP, never by a query of its own. `measure_snapshot` is asserted through `GET /api/recovery/reporting/v1/reports/measures` on the P9 contract of RWB-P9-E1013-APP. The legacy INT-19 step of the data lake is replaced: rwb-reporting publishes on `rwb.reporting.events.v1` and rwb-integration delivers the regulatory extract (GAP-0339; ASM-0433). The measure values, the definition version, the baseline date and the gate are copied unchanged from RWB-E1-013.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Each measure is published only under a definition in force that names its data product, formula, unit and approver | RWB-E1-013 BR1; REQ-RDF-012; Principle 1 |
| BR2 | The baseline is the snapshot of the configured baseline business date and is frozen once written | RWB-E1-013 BR2; REQ-RDF-012; FEAT-RPT-01 |
| BR3 | Measures are computed from Workbench records read through the owning modules, never from a separate count | RWB-E1-013 BR3; NFR-065 |
| BR4 | A measure is computed only from a COMPLETED ACE batch; stale data is not published as the baseline | RWB-E1-013 BR4; CTL-02; MSG-P1-001 rule |
| BR5 | The extract to the data lake holds the publish and alerts on failure, and runs again in the next window | RWB-E1-013 BR5; INT-19 error handling |
| BR6 | Age bands are a reference list | RWB-E1-013 BR6; Principle 1 |
| BR7 | A definition load with any invalid row is refused in full | RWB-E1-013 BR7; refdata.txt change process, step 3 |
| BR8 | The suite reads and writes no schema of its own and never reads another service's tables: every assertion is made on a contract response or an event, and every write it needs is a call to the owner's own path | DP-01, DP-05, DP-11 |
| BR9 | Every call is one hop to the owning service on its own base, with a 2 s client budget; a call that exceeds it fails the criterion and is reported | DP-11, DP-13 |
| BR10 | One event type per owner topic in the CloudEvents 1.0 envelope, keyed caseId, carrying IDs and facts only and no personal data field | ADR-015; Arch v5 slide 42 and slide 43 notes |
| BR11 | The suite runs on synthetic data in SIT only and never points at production data or a production namespace | ADR-018; this story |
| BR12 | No business value in the test code: the measure codes, the definition version, the baseline date, the age bands and the expected totals come from the legacy acceptance criteria and the fixture files | RWB-E1-013 section 17; this story |

BR5 is read with BR10 of RWB-P9-E1013-APP and with DP-17: the publish and the hold stay, the destination is the v5 path — rwb-reporting publishes ReportPublished and rwb-integration delivers the regulatory extract — and no lake assertion is part of the wave 1 suite (GAP-0339; ASM-0433).

### 9. State transitions

None. This story does not change a case status. It sets the baseline flag and the frozen flag on measure_snapshot rows, and the JOB-15 run status (running, complete, failed, held).

The states the suite observes on the services:

| Item | States |
|---|---|
| Measure run (JOB-15) | Scheduled; Running; Complete; Failed; Held |
| `measure_snapshot` baseline flag | Not baseline; baseline, set once for the configured baseline business date |
| `measure_snapshot` frozen flag | Not frozen; frozen, never changed after the baseline write |
| Daily gate | COMPLETE; HOLD when no COMPLETED ALS row exists for the business date |
| Case set of the business date | Created through JOB-02 for the date, or absent |
| Harness run | Not started; running; passed; failed with the failing criterion and the service named |

The suite observes these states and drives none of them; a state it cannot reach is a failed criterion, not a skipped one.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| QA integration engineer | Owns the suite, the fixtures, the run order and the evidence report; runs it in SIT only |
| Service owner of rwb-case (P3) | Owns the case creation, the case facts and their contract the suite calls |
| Service owner of rwb-source-data (P1) | Owns the ACE views, the readiness trigger, the freshness and gate, the payments and the reconciliation |
| Service owner of rwb-reporting (P9) | Owns the measure definition, the snapshot, the baseline and frozen flags, the measures Schedule, the publication and the extract |
| Data steward | Reads the run record, the freshness and the published measures; confirms the definition version in force |
| Platform administrator | May rerun JOB-15 and read the run record; owns the SIT namespace, the queues and the topics |
| Reporting and BI analyst | Reads the published baseline; does not run the suite and changes no definition |
| Operations | Receives the alert of a failed or held run |
| No role | May read a service table, edit a published measure or change a frozen row |

### 11. Data

| BR Field ID | Entity | Field | Source | Read or write |
|---|---|---|---|---|
| DF-RPT-032 to DF-RPT-040 | `measure_definition` (rwb_reporting) | measure_code, name, formula, data_product, unit, definition_version, approved_by, approved_at, valid_from | P9 rwb-reporting, through `GET /api/recovery/reporting/v1/reports/measures` | Read |
| DF-RPT-041 to DF-RPT-052 | `measure_snapshot` (rwb_reporting) | id, measure_code, definition_version, business_date, product_group, dimension_code, dimension_value, value, case_count, is_baseline, frozen, published_at | P9 rwb-reporting, through `GET /api/recovery/reporting/v1/reports/measures` | Read |
| DF-CAS-001 to DF-CAS-026 | `recovery_case`, `case_account` (rwb_case) | the case facts of RWB-E1-013 section 11: id, product_group, status, stage_code, route_code, queue_id, entry_date, stage_clock_start, closed_date, case_id, account_key | P3 rwb-case, through `GET /api/recovery/case/v1/cases` | Read |
| DF-ACE-045, DF-ACE-046 | `v_ace_payment` (`recovery.v_ace_payment`) | payment_date, payment_amount | P1 rwb-source-data, through `GET /api/recovery/source-data/v1/payments?accountId={accountId}` | Read |
| DF-RPT-002, DF-RPT-019 | `case_list_row` (rwb_source_data) | business_date, publish_status | P1 rwb-source-data, through `GET /api/recovery/source-data/v1/data-products/freshness` | Read |

Field IDs are those in the Logical Data Model and Data Dictionary and are copied from RWB-E1-013. Every element above is synthetic for this suite: 120 synthetic cases of business date 2026-11-27, synthetic payments since entry totalling 4,350,000.00 THB, a synthetic ACE batch row, and the definition rows of version MD-2026.11 approved as TRB-0001. No production data is read, copied or derived. The suite owns no table and holds no copy of a service table.

The exact composition of the fixture files is Not specified in the source documents (GAP-0339; ASM-0433); the fixture sizes, files and dates are the ones fixed in section 13.

### 12. Contract

#### 12.1 REST operations provided

None. The suite provides no REST operation. P2 rwb-integration's reserved names `/api/recovery/integration/v1`, `rwb.integration.events.v1`, `rwb-integration` and `rwb_integration` are not used, and the suite writes no rwb_integration table.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| POST | `/api/recovery/source-data/v1/business-days/{date}/ready` | P1 rwb-source-data | Airflow-style readiness trigger for the business date, 2 s budget |
| GET | `/api/recovery/source-data/v1/data-products/freshness` | P1 rwb-source-data | Daily gate for the business date, 2 s budget |
| GET | `/api/recovery/source-data/v1/payments?accountId={accountId}` | P1 rwb-source-data | Realized recovery of the synthetic set for wave 1, 2 s budget |
| GET | `/api/recovery/case/v1/cases` | P3 rwb-case | Case facts of the synthetic set for the business date, 2 s budget |
| GET | `/api/recovery/reporting/v1/reports/measures` | P9 rwb-reporting | Published measures, baseline and frozen flags, definition version, 2 s budget |

Every call is one hop to the owning service on its own base (DP-11, DP-13) with the 2 s client budget. The suite never calls a service through another service and never reads a view or a table of its own.

#### 12.3 Events published

None. The suite publishes no event. Every event asserted in this story is produced by a service and is listed in 12.4.

#### 12.4 Events consumed

| Event | Topic | Owner | Use in this story |
|---|---|---|---|
| `rwb.source-data.AceDataReady.v1` | `rwb.source-data.events.v1` | P1 rwb-source-data | Starts DailyCaseRun in rwb-case (JOB-02); the suite waits for it after the readiness call |
| `rwb.case.CaseCreated.v1` | `rwb.case.events.v1` | P3 rwb-case | Projected into rwb-reporting; the suite counts the cases of the business date |
| `rwb.reporting.ReportPublished.v1` | `rwb.reporting.events.v1` | P9 rwb-reporting | Marks the extract ready for rwb-integration; the suite takes it as the evidence that the run published |

All three are consumed in the CloudEvents 1.0 envelope, keyed caseId, with the inbox dedupe of the consumer and the retry and `.dlt` topics of the owner (ADR-015; Arch v5 slides 42 and 43). The suite asserts on IDs and facts only and writes no payload of its own.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| CaseWorkflow | Workflow | `rwb-case` | Parent per case; the suite observes the case record and the facts it carries |
| DailyCaseRun | Workflow, started by Schedule and by AceDataReady | `rwb-case` | Runs JOB-02 case creation for the business date; the suite waits for its result through the case read |
| listEligibleAccounts | Activity | `rwb-source-data` | Accounts eligible for the business date, the input of the case set |
| snapshot(page) | Activity | `rwb-source-data` | Paged snapshot of the facts rwb-reporting measures from |
| buildRegulatoryExtract | Activity | `rwb-reporting` | Builds the regulatory extract that rwb-integration delivers |

All five are registered by the owning services (RWB-P3-E1013-APP, RWB-P3-E1018-APP, RWB-P1-E1013-APP, RWB-P9-E1013-APP); this story drives them through their own triggers and reads their result on a contract, and it adds no workflow of its own.

#### 12.6 Schedules

| Schedule | Cadence | Registration | Legacy reference |
|---|---|---|---|
| JOB-15 measures | Daily at 01:30, Airflow trigger, no data lake | Registered by the rwb-reporting release and triggered once by the harness through the P9 run path with the same input the cadence uses | JOB-15 Reporting extract |
| JOB-02 case creation | Airflow: ACE data ready | AceDataReady starts DailyCaseRun in rwb-case; the harness drives it with the readiness call | JOB-02 Case creation |
| JOB-04 reconciliation | Airflow: ACE data ready | Event-started workflow in rwb-source-data; the harness observes its freshness result | JOB-04 Reconciliation |

#### 12.7 Tables owned

None. The suite owns no table and never reads another service's schema (DP-01). The tables it exercises belong to `rwb_case`, `rwb_source_data` and `rwb_reporting` and are listed in section 11 with their owners.

#### 12.8 Contract fakes

External stubs only, and no service contract fake:

| Stub | Stands in for | Note |
|---|---|---|
| ACE batch fixture (W1J01) | The ACE batch record the views read | Synthetic rows only, including the COMPLETED ALS row of 2026-11-27 and its absence for the held run |
| Airflow trigger stub | The bank scheduler | Calls `POST /api/recovery/source-data/v1/business-days/{date}/ready` and the P9 run path; it holds no business rule |
| Azurite Blob | The regulatory extract storage | Receives the extract delivered through rwb-integration; the suite asserts the delivery, not a lake |

The three services, their topics, their queues and their Schedules are real. No contract of P1, P3 or P9 is faked.

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 0 | 5 | Readiness trigger, freshness and gate, payments, case facts, published measures; one hop, 2 s (DP-11, DP-13) |
| Kafka | 0 published | 3 event types | AceDataReady, CaseCreated, ReportPublished on the three owner topics, key caseId |
| Temporal | None | 2 workflows, 3 activities | CaseWorkflow, DailyCaseRun; listEligibleAccounts, snapshot(page), buildRegulatoryExtract |
| File | None | 1 | The regulatory extract delivered through rwb-integration |

### 13. Solution plan

**Deliverables.** One JUnit and Testcontainers suite in the W1J01 harness, `integration/recovery-w1/baseline-measures`, with the two feature files of section 7, the four fixture groups below, the evidence report writer and the wave-gate publisher. The suite reuses the W1J01 environment, topic and queue helpers rather than a second harness. No service code and no schema change is part of this story.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| SuiteRunner | Runner | Reads the environment, runs the preflight, orders the two runs, writes the report and the exit code |
| Preflight | Component | Checks the four services, the three topics with retry and `.dlt`, the schema registry versions, the three task queues and the JOB-15 Schedule |
| CaseSetSeeder | Component | Seeds the 120 synthetic cases of 2026-11-27 through the rwb-case creation path and the P1 readiness trigger, and asserts the case facts on the P3 contract |
| MeasureDefinitionSeeder | Component | Loads the 6 rows of version MD-2026.11 through the P9 path published by RWB-P9-E1013-APP and reads the version in force back |
| GateProbe | Component | Calls the freshness and gate operation and asserts COMPLETE for the published run and HOLD for the held run |
| MeasuresProbe | Component | Reads the published measures, the baseline and frozen flags and the definition version on the P9 contract |
| PaymentsProbe | Component | Reads the payments of the synthetic set on the P1 contract and sums them for the REALIZED_RECOVERY comparison |
| EventProbe | Component | Consumes the three owner topics and asserts one event per fact, the key, the envelope and the move to `.dlt` on failure |
| ReportWriter | Component | One row per criterion and per test case, with the evidence references |
| GatePublisher | Component | Publishes the evidence report to the wave 1 exit gate |

**Database.** None of its own. The suite reads nothing directly: every value is taken from a contract response or an event, and every write is a call to the owner's own path.

**Configuration and reference data**

- The service list, the five operations, the three topics with their retry and `.dlt` topics, the three task queues and the namespace `rwb-recovery`, all as configuration.
- The measure codes of the six definitions, the definition version MD-2026.11, the baseline business date 2026-11-27 and the age bands, read from the legacy criteria and the fixture files.
- The fixture dates: the baseline date 2026-11-27, the run date 2026-11-28, the held-run date and its first successful run after the batch.
- The 2 s client budget, the wait windows and the retry counts, as configuration.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-17 | Data lake, INT-19, INT-20 | Removed (no data lake); reporting from events into rwb-reporting | none; gap if the story needs lake data |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

This ITG story adds no build dependency: the H dependencies of DP-03, DP-07, DP-10, DP-15 and DP-19 stay with the service, platform and operations stories whose behaviour the suite proves, and the I list names the four services it exercises without ever blocking a build (Template and Rules §R5.4 and §R5.7). The DP-17 gap is GAP-0339.

**Fixtures**

| Fixture | Content | Used by |
|---|---|---|
| Synthetic case set | 120 open cases of business date 2026-11-27: 60 Mortgage, 45 Hire purchase and 15 SSME, with route, stage, queue, entry date and stage clock start | AC2, AC6, TC-E1-013-02-ITG, TC-E1-013-06-ITG |
| ACE batch fixture | The COMPLETED ALS row of 2026-11-27 for the published run, and its absence for the held run | AC2, AC6 |
| Payments fixture | The synthetic payments since entry totalling 4,350,000.00 THB | AC2 |
| Measure definition fixture | The 6 rows of version MD-2026.11 approved as TRB-0001 | AC2, AC6 |
| Held-run set | The 2026-11-27 set with no COMPLETED ALS row, and the same set after the batch is COMPLETED | AC6 |
| Environment config | Services, operations, topics, queues, schedules and wait windows | All |

**Build steps**

1. Add the suite to the W1J01 harness and read the environment configuration, reusing its topic, queue and report helpers.
2. Write the preflight: the four services, the five operations, the three topics with retry and `.dlt`, the schema versions and the JOB-15 Schedule.
3. Write the case-set seeder and the readiness call, and assert the case facts of 2026-11-27 on the P3 contract.
4. Write the measure-definition seeder through the P9 path and assert version MD-2026.11 in force.
5. Write the gate and payments probes, and the REALIZED_RECOVERY comparison against the synthetic sum.
6. Write the measures probe and the AC2 assertions: roll-up of 120 cases with 60 Mortgage, baseline and frozen flags, definition version.
7. Write the AC6 run: gate HOLD, no baseline row, MSG-P1-001 on the run record, publication at the first run after the batch.
8. Write the report writer, the repeatable reset of the synthetic set and the wave-gate publisher; run the suite twice to prove the fixture is idempotent.

**Done when.** The nine test cases of section 16 pass with their `-ITG` copies on the real services in SIT, AC2 shows the 120 cases with 60 Mortgage and REALIZED_RECOVERY of 4,350,000.00 THB with the baseline and frozen flags set at version MD-2026.11, AC6 shows no baseline row, the HOLD gate and MSG-P1-001 naming "DP03 Case" and 2026-11-26, and the evidence report is published to the wave 1 exit gate.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A definition row lacks a required value | Enter {field}. |
| MSG-P9-001 | The baseline is published again | The baseline for {date} is frozen. It cannot be published again. |
| MSG-P1-001 | The ACE batch for the business date is not COMPLETE | {product} is from {date}. Today's load has not arrived. |
| MSG-GEN-006 | The data lake is unavailable | {system} is not available. Your request is queued and will be retried. |
| MSG-P9-003 | A measure has no definition in force | {measure} has no approved definition. It is not published. |

The five texts are copied unchanged from RWB-E1-013, with the same IDs and the same placeholders. The story adds no message ID and no message text; report lines of the suite are for developers and are not part of the message standard.

### 15. Screens and states

No screen is written by this story and the suite renders nothing: the five operations are called directly and are the only reader surface it uses. The run shows on **SCR-44 Interface and job monitor** in its Running, failed and complete states, which the platform administrator reads; the suite asserts those states through the run record and the freshness answer. **SCR-37 Steering dashboard** is RWB-E2-009 and is out of scope. The states the suite observes on the services are the measure-run, flag, gate and harness states of section 9.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-013-01-ITG | AC1, BR1 | Integration | Definition file of 6 rows approved by TRB-0001; end-to-end: real services on the wave 1 contracts |
| TC-E1-013-02-ITG | AC2, BR2, BR3 | Integration | 120 synthetic cases on 2026-11-27 with known totals; end-to-end: real services on the wave 1 contracts |
| TC-E1-013-03-ITG | AC3, BR5 | Integration | JOB-15 on 2026-12-02 for business date 2026-12-01; end-to-end: real services on the wave 1 contracts |
| TC-E1-013-04-ITG | AC4, BR7 | Integration | TIME_IN_STAGE with no formula; end-to-end: real services on the wave 1 contracts |
| TC-E1-013-05-ITG | AC5, BR2 | Integration | JOB-15 rerun for 2026-11-27; end-to-end: real services on the wave 1 contracts |
| TC-E1-013-06-ITG | AC6, BR4 | Integration | No COMPLETED ALS row for 2026-11-27; end-to-end: real services on the wave 1 contracts |
| TC-E1-013-07-ITG | AC7, BR5 | Integration | Data lake load area stubbed unavailable; end-to-end: real services on the wave 1 contracts |
| TC-E1-013-08-ITG | AC8, BR1 | Integration | COST_PER_CASE with no definition; end-to-end: real services on the wave 1 contracts |
| TC-E1-013-09-ITG | Access | Integration | RW-BIANAL calls POST /admin/reference-loads with table measure_definition; refused with MSG-P4-002; end-to-end: real services on the wave 1 contracts |

The nine legacy test case IDs of RWB-E1-013 are kept as ITG copies with the suffix `-ITG`, in their legacy order, with the legacy Covers text. **TC-E1-013-02-ITG and TC-E1-013-06-ITG are the copies this story signs off**, because AC2 and AC6 are the two criteria it owns; the other copies are regression evidence for the sibling stories — AC1, AC4, AC5, AC7 and AC8 with RWB-P9-E1013-APP, the case facts with RWB-P3-E1013-APP and the ACE, payment and gate side with RWB-P1-E1013-APP. The full test, with its Given, When and Then, stays in the test case master under the legacy ID.

### 17. Guardrails

- Synthetic data only: the 120 cases of 2026-11-27, the synthetic payments of 4,350,000.00 THB and the ACE batch fixture; no production data and no production namespace.
- No personal data in events, logs or fixtures: case IDs, codes, counts and amounts only, and no field marked personal in sys_fields.
- No cross-service table read: every assertion is a contract response or an event, and every write is a call to the owner's own path (DP-01, DP-05).
- No business value in the test code: the measure codes, the definition version, the baseline date, the age bands and the expected totals come from the legacy acceptance criteria and the fixture files (BR12).
- CloudEvents 1.0 on the owner topics, key caseId, IDs and facts only, with the registry's BACKWARD compatibility and the inbox dedupe of the consumer (ADR-015, BR10).
- One hop and a 2 s budget on every call; a service is never called through another service and a timeout fails the criterion instead of being retried into a pass (DP-11, BR9).
- No production access of any kind; the suite refuses an environment that is not SIT.
- Clean-up and idempotent fixtures: the synthetic set is reset to its fixture state after a run, and a second run on the same set gives the same result.
- The lake assertion stays out: the suite asserts the v5 publication and the rwb-integration delivery, and it fails if a lake step is added back (DP-17, GAP-0339).

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases | Stories |
|---|---|---|---|---|
| REQ-RDF-012 | Baseline measures published with definitions agreed by the Tribe | `GET /api/recovery/reporting/v1/reports/measures`, `GET /api/recovery/case/v1/cases`, `GET /api/recovery/source-data/v1/payments?accountId={accountId}`, `GET /api/recovery/source-data/v1/data-products/freshness`, JOB-15 measures | TC-E1-013-02-ITG, TC-E1-013-06-ITG, TC-E1-013-01-ITG, TC-E1-013-05-ITG | RWB-ITG-E1013-ITG; legacy RWB-E1-013; siblings RWB-P9-E1013-APP, RWB-P3-E1013-APP, RWB-P1-E1013-APP, RWB-P3-E1018-APP |
| ADR-015 | Kafka with outbox, inbox and CloudEvents | `rwb.source-data.AceDataReady.v1`, `rwb.case.CaseCreated.v1`, `rwb.reporting.ReportPublished.v1` on the three owner topics | TC-E1-013-02-ITG, TC-E1-013-03-ITG, TC-E1-013-06-ITG | RWB-ITG-E1013-ITG; RWB-P9-E1013-APP, RWB-P1-E1013-APP |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The five consumed operations on the P1, P3 and P9 bases | TC-E1-013-02-ITG, TC-E1-013-06-ITG, TC-E1-013-09-ITG | RWB-ITG-E1013-ITG; RWB-P9-E1013-APP, RWB-P3-E1013-APP, RWB-P1-E1013-APP |
| DP-17 | No data lake; reporting from events into rwb-reporting | `rwb.reporting.ReportPublished.v1` on `rwb.reporting.events.v1`; the regulatory extract through rwb-integration | TC-E1-013-03-ITG, TC-E1-013-07-ITG | RWB-ITG-E1013-ITG; RWB-P9-E1013-APP (GAP-0339) |

The business rules, the legacy sections 1 to 11 and the message table of this story are copied from RWB-E1-013; the requirement, the features FEAT-RDF-19 and FEAT-RPT-01 and the control CTL-02 keep their legacy IDs.

### 19. Out of scope

- The rwb-reporting build itself: the definition load, the snapshot, the flags, the Schedule, the publication and the measures endpoint (RWB-P9-E1013-APP).
- The rwb-case case-fact side: case creation and the case read the suite asserts (RWB-P3-E1013-APP, RWB-P3-E1018-APP).
- The rwb-source-data side: the ACE views, the readiness trigger, the freshness and gate, the payments and the reconciliation (RWB-P1-E1013-APP).
- The contract and AsyncAPI documents of the three consumed topics and the OpenAPI documents of the three services (the CON stories of the key).
- The deployment, the topic provisioning, the queue registration and the Schedule registration (the OPS stories of the key).
- The acceptance criteria this story does not own: AC1, AC3, AC4, AC5, AC7 and AC8, with the sibling app stories.
- The build of the harness W1J01 itself, which is a precondition here and not a deliverable.
- The non-functional epic RWB-ITG-NFR and its performance, resilience and observability criteria.
- SCR-37 Steering dashboard and the measures endpoint read model of RWB-E2-009.
- The data lake and the Power BI feed, removed from the target architecture (DP-17).
