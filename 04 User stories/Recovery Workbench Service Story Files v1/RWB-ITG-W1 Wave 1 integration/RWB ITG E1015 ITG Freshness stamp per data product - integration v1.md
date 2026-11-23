# RWB-ITG-E1015-ITG Freshness stamp per data product

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-E1015-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W1 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-015 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP02, DP03, DP05, DP07, DP09, DP10, DP11, DP15, DP19 |
| Parallel lane | L-ITG-W1 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | RWB-P1-E1015-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to REQ-RDF-009) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: integration slice of RWB-E1-015 for RWB-ITG-W1. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **QA integration engineer in the release squad**, I want **the end-to-end proof of the RWB-E1-015 freshness stamp and of the daily completeness gate across rwb-source-data (P1), rwb-case (P3), rwb-payment (P8) and rwb-decision (P7)**, so that **the stamp, the late-batch path and the gate are proved on the real services before wave 1 exits**.

### 2. Business rationale

The legacy capability stamps every data product with the business date, start time, completion time and status of the ACE batch it came from, shows that stamp on the case record, and holds a daily data job until every source it reads is COMPLETED. This slice owns nine of its acceptance criteria — AC1, AC2, AC4, AC5, AC6, AC7, AC9, AC10 and AC11 — and proves them on the deployed services instead of on one monolith.

The stamp and the gate cannot be proved by one service story, because they are cross-service by nature. rwb-source-data (P1) reads the ACE batch record and publishes `AceDataReady` (EV-26) and `AceDataLate` (EV-27) on `rwb.source-data.events.v1`, and it owns the freshness resources, the reconciliation and the per-product cut-off check. rwb-case (P3) starts `DailyCaseRun` (JOB-02) when that readiness event arrives, and it owns the case record that shows the stamp in its data panel. rwb-payment (P8) starts payment matching and booking confirmation when the same event arrives. rwb-decision (P7) reads the stamps for the inputs snapshot of a decision entry. A defect in any one of the four — a missing event, a stamp that never turns stale, a gate that releases early — is invisible to the service that owns the code and visible only when the services run together.

**Target delta.** Two legacy statements no longer hold in Arch v5. First, AC1 and AC6 require JOB-07 and JOB-08 to start, but both jobs belong to `rwb-payment` (P8) and P8 is a wave 2 service (Arch v5 slides 17 and 44; Ownership Map, P8 wave 2), while EP01 is wave 1. Wave 1 therefore asserts JOB-02 (P3) and JOB-04 (P1) and defers the P8 start to RWB-ITG-W2. Second, AC9 keeps the released case list in the data lake, but Arch v5 removes the data lake (DP-17) and the released case list is P1's `case_list_row` projection, not a lake copy. Both points are recorded as GAP-0340 and ASM-0434. No service contract is faked anywhere in this slice: every read and every event is the real one that the owners publish.

### 3. Preconditions

- RWB-P1-E1015-APP is done: the freshness stamp, `data_product_load`, the daily completeness gate, the cut-off check, the reconciliation and the events EV-26 and EV-27 run on `rwb-source-data`, and the freshness and job resources are published on base `/api/recovery/source-data/v1`.
- The published contracts of P1 rwb-source-data, P3 rwb-case and P7 rwb-decision are in the contract registry at the versions the wave-1 build publishes; the SIT build runs those versions.
- The harness RWB-ITG-W1J01-ITG is available and its synthetic data set for business date 2026-11-30 is loaded; the set carries the ACE batch rows, the product rows with refresh cycle and expected-by time, and the synthetic case set of the run.
- One SIT environment: namespace `rwb-recovery`, one task queue per service, the SIT Kafka topics with their retry and `.dlt` topics, and the schema registry with the event schemas in force.
- Wave 2 is not deployed: rwb-payment (P8) is absent from SIT, so JOB-07 and JOB-08 cannot start in this suite (exception X8).
- The synthetic data set carries no production data: no real account, no real person, no real case.
- No build dependency: the single integration dependency is the real P1 service, and the story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. FixtureLoader seeds the synthetic ACE batch rows of the W1J01 data set into the SIT ACE batch record that rwb-source-data reads through `recovery.v_ace_batch_status`, and creates the synthetic case set through the rwb-case contract; it writes no service table.
2. It completes the ALS row for business date 2026-11-30 with start 2026-11-30T23:30+07:00 and completion 2026-12-01T05:40+07:00, and calls `POST /api/recovery/source-data/v1/business-days/2026-11-30/ready`, the Airflow edge of P1.
3. rwb-source-data reads the COMPLETED row, writes the DP01 stamp, and publishes `rwb.source-data.AceDataReady.v1`; the harness asserts the event on `rwb.source-data.events.v1` with its CloudEvents ID and the business date.
4. The event starts `DailyCaseRun` (JOB-02) on task queue `rwb-case` and the reconciliation (JOB-04) on task queue `rwb-source-data`; the harness asserts one run per business date on each queue through Temporal visibility in namespace `rwb-recovery`.
5. The harness reads the stamp with `GET /api/recovery/source-data/v1/data-products/freshness` and the product records with `GET /api/recovery/source-data/v1/data-products/DP01/records`, and compares business date, source time, load time and status with the fixture row.
6. AC2: with no COMPLETED row in place and the cut-off control set to 08:00 on 2026-12-01, the cut-off passes, rwb-source-data publishes `rwb.source-data.AceDataLate.v1` for DP01, the stamp in use turns STALE with its stale-flagged-at time, and the alert reaches the data steward and the operations channel; the harness reads the stamp on the case record through `GET /api/recovery/case/v1/cases/{caseId}`.
7. AC4: a FAILED ALS row for 2026-11-30 at 05:20 marks DP01 STALE at once and keeps the previous business date in use, and no daily job starts for the date.
8. AC5: the same COMPLETED row is read again; one stamp row remains with duplicate count 1, and no second event and no second job run appear.
9. AC6 and AC7: the ALS batch completes late at 08:40 and clears the flag to LOADED, and a batch at 07:59 is not flagged at all; both runs are repeated with the clock control.
10. AC9, AC10 and AC11: the gate returns HOLD naming DP05 and source EFS while the EFS row is FAILED and writes no case list row for 2026-11-30, returns COMPLETE when every source a job reads is COMPLETED, and the multi-source product DP06 carries the oldest business date while SVAF is late; then the harness cleans the synthetic rows, the synthetic cases and the fixture files it created.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | No COMPLETED batch for the expected business date at the expected-by time | The stamp in use turns STALE with its stale-flagged-at time, `AceDataLate` is published, the alert goes to the data steward and the operations channel, and the case record shows the stale warning | MSG-P1-001 | AC2 |
| X2 | The batch row is FAILED | The product is STALE at once, the previous business date stays in use, and no daily job starts for the date | MSG-P1-001 | AC4 |
| X3 | A late batch arrives after the stale flag | The status turns LOADED with the new completion time and the jobs start for that business date | None | AC6 |
| X4 | The same COMPLETED batch row is read twice | One stamp row, the duplicate is counted, and no second event and no second job run appear | None | AC5 |
| X5 | The gate holds the day | The gate returns HOLD, names the product and the source, writes no case list row for the date, and alerts the data steward and the team manager group | MSG-P1-001 | AC9 |
| X6 | The gate releases the day | The gate returns COMPLETE and records the business date, the sources read and the completion time; the reconciliation and the case list step of the date run | None | AC10 |
| X7 | A weekly product sits between its batches | The product is not flagged stale on the days between batches; its own weekly cut-off decides its stamp | None | Legacy AC8, owned by RWB-P1-E1015-APP |
| X8 | A P8 workflow cannot start because rwb-payment is wave 2 and not deployed in SIT | The harness records the JOB-07 and JOB-08 start as not run in wave 1 and passes the rest of the run; the start is verified in RWB-ITG-W2 | None | AC1, AC6 (GAP-0340; ASM-0434) |
| X9 | A consumed contract or event schema differs from the version the wave-1 build publishes | The contract probe fails before any stamp assertion, the run is FAILED with the contract and the version named, and no verdict is recorded | MSG-GEN-006 | TC-E1-015-01-ITG (contract probe) |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Proves behaviour that already exists in the wave-1 services; builds no product capability, changes no case, and writes no service table |
| Negotiable | The fixture values, the clock offsets and the harness settings are configuration; the stamp, the stale rule and the gate are fixed by the legacy story |
| Valuable | Wave 1 cannot claim the freshness stamp and the daily gate work until the four services pass the same business date together |
| Estimable | One harness module, one event driver, one clock control, five consumed reads, one gate assertion, one panel assertion |
| Small | Fits one sprint with its test cases |
| Testable | Every criterion is one automated test against the real SIT services, with the failure path and the deferred P8 start recorded |

### 7. Acceptance criteria

```gherkin
Feature: Freshness stamp per data product across the wave-1 services

  Background:
    Given data product "DP01" Account and arrears has refresh cycle "DAILY" and expected-by time 08:00
    Given data product "DP06" Collateral and asset has refresh cycle "WEEKLY" and expected-by time Monday 08:00
    Given the wave-1 services rwb-source-data, rwb-case and rwb-decision are deployed in SIT with their published contracts and no contract fake is in the path
    Given the synthetic data set of the harness RWB-ITG-W1J01-ITG is loaded for business date 2026-11-30

  Scenario: AC1 Freshness from the ACE batch (legacy RWB-E1-015 AC1)
    Given v_ace_batch_status holds source "ALS", business date 2026-11-30, started 2026-11-30T23:30+07:00, completed 2026-12-01T05:40+07:00, status "COMPLETED" and record count 184,500
    When EV-26 AceDataReady is processed and GET /data-products/freshness?product=DP01 is called
    Then data_product_load holds DP01 for 2026-11-30 with source time 2026-11-30T23:30+07:00, load time 2026-12-01T05:40+07:00 and status "LOADED"
    Then FreshnessQuery.stampForRow("DP01", 2026-11-30) returns the same stamp
    Then GET /data/freshness?sourceSystem=ALS returns the same ACE batch row with isComplete true and ageDays 1
    Then JOB-02, JOB-04, JOB-07 and JOB-08 are started for 2026-11-30

  Scenario: AC2 Stale product flagged at the cut-off (legacy RWB-E1-015 AC2)
    Given no COMPLETED ALS row for 2026-11-30 is in v_ace_batch_status at 08:00 on 2026-12-01
    When the DP01 cut-off passes
    Then EV-27 AceDataLate is in the outbox with sourceSystem "ALS", businessDate 2026-11-30 and the latest status
    Then the DP01 stamp for 2026-11-27 is "STALE" with stale_flagged_at 2026-12-01T08:00+07:00
    Then the alert goes to the data steward and the operations channel
    Then the case record view shows the stamp in the data panel with "Account and arrears is from 2026-11-27. Today's ACE batch has not arrived."

  Scenario: AC4 A failed ACE batch marks the product stale at once (legacy RWB-E1-015 AC4)
    Given v_ace_batch_status shows ALS for 2026-11-30 with status "FAILED" at 05:20
    When the row is read
    Then the DP01 stamp for 2026-11-27 is marked "STALE" from 05:20 and EV-27 is published
    Then the stamp for business date 2026-11-27 stays the one in use
    Then no data job is started for 2026-11-30

  Scenario: AC5 The same batch read twice (legacy RWB-E1-015 AC5)
    Given the DP01 stamp for 2026-11-30 is LOADED
    When the same COMPLETED ALS row is read again
    Then data_product_load still holds one DP01 row for 2026-11-30 with duplicate_count 1
    Then no second EV-26 is processed and no data job starts twice

  Scenario: AC6 A late batch clears the stale flag (legacy RWB-E1-015 AC6)
    Given DP01 was flagged "STALE" at 08:00 on 2026-12-01
    When the ALS batch for 2026-11-30 completes at 08:40
    Then EV-26 is raised
    Then DP01 is "LOADED" with load time 2026-12-01T08:40+07:00
    Then JOB-02, JOB-04, JOB-07 and JOB-08 start for 2026-11-30

  Scenario: AC7 A batch one minute before the expected-by time (legacy RWB-E1-015 AC7)
    Given the ALS batch for 2026-11-30 completes at 07:59 on 2026-12-01
    When the freshness step runs at 08:00
    Then the system does not flag DP01 stale

  Scenario: AC9 Daily completeness gate holds the case list (legacy RWB-E1-015 AC9)
    Given at 08:00 on 2026-12-01 the ALS, SCBPDM, LIT, WIN, COLLINS and GL batches for 2026-11-30 are COMPLETED
    Given the EFS batch for 2026-11-30 is FAILED
    When the daily completeness gate runs
    Then it returns HOLD and names DP05 Contact and promises and source "EFS"
    Then the case list step of JOB-04 does not start and no case_list_row for 2026-11-30 is written
    Then the lake keeps the released case list of 2026-11-27
    Then the data steward and the team manager group receive MSG-P1-001 "DP05 Contact and promises is from 2026-11-27. Today's ACE batch has not arrived."

  Scenario: AC10 Daily completeness gate releases when every source is complete (legacy RWB-E1-015 AC10)
    Given at 08:00 on 2026-12-01 every source the day's jobs read is COMPLETED for 2026-11-30
    Given the SVAF batch for 2026-11-30 is absent and no job of the day reads DP06
    When the daily completeness gate runs
    Then it returns COMPLETE and records the business date, the sources read and the completion time
    Then DP06 is not marked stale by the gate, and its own weekly cut-off decides its stamp
    Then JOB-04 starts and the case list step runs for 2026-11-30

  Scenario: AC11 A product fed by several sources (legacy RWB-E1-015 AC11)
    Given v_ace_batch_status shows CCMS COMPLETED for 2026-11-27 and SVAF COMPLETED only up to 2026-11-20
    When the DP06 cut-off passes at MON 08:00 on 2026-11-30
    Then DP06 carries business date 2026-11-20 and status "STALE"
    Then EV-27 names sourceSystem "SVAF"
```

**Target reading.** The `v_ace_*` views and `data_product_load` are read only by rwb-source-data, and every stamp assertion goes through the P1 contract, never through a table. JOB-07 and JOB-08 are rwb-payment (P8, wave 2) and are verified in RWB-ITG-W2; wave 1 asserts JOB-02 (P3) and JOB-04 (P1) only, so the AC1 and AC6 lines that name all four jobs are read as the legacy text with the P8 pair recorded as not run. The released case list of AC9 is P1's `case_list_row`, not a lake copy, because the data lake is removed (GAP-0340; ASM-0434).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every COMPLETED ACE batch row writes one freshness stamp per product it feeds and business date, from `v_ace_batch_status` only, in the same transaction as the event handling | RWB-E1-015 BR1; REQ-RDF-009; BR-P1-014-2 |
| BR2 | A product with no COMPLETED batch for its expected business date by its expected-by time is stale | RWB-E1-015 BR2; data_product.expected_by; DL11 |
| BR3 | A failed ACE batch leaves the previous complete business date in use and marks the product stale at once | RWB-E1-015 BR3; BR-P1-014; EV-27 |
| BR4 | A product fed by more than one source carries the oldest business date among its sources and is STALE while any of them is late | RWB-E1-015 BR4; BR-P1-014-3 |
| BR5 | Every decision records, in its inputs snapshot, the product, business date, load time and status of each data product it read | RWB-E1-015 BR5; REQ-RDF-009; FEAT-DRI-12; DF-DEC-008 |
| BR6 | A repeat read of the same COMPLETED batch row is ignored and counted | RWB-E1-015 BR6; R-UNI-40 |
| BR7 | Expected-by times, refresh cycles and the product-to-source map are data rows, not code | RWB-E1-015 BR7; Principle 1; DT02 |
| BR8 | No daily data job for a business date starts until every source it reads is COMPLETED for that date; when one is not, the case list holds, the previous list stays published and the data steward is alerted | RWB-E1-015 BR8; BR-P1-014-4; FSD P1 A2.14 |
| BR9 | The suite reads no service table: every stamp, product record, job run and case record is read through the owning service's contract, and a table read fails the run | DP-01; DP-11; ADR-020 |
| BR10 | Every cross-service call in the run is one hop on the owner's base with a 2 s timeout, and no call is chained through a second service | DP-11; ADR-020 |
| BR11 | Every event the suite asserts is a CloudEvents 1.0 envelope carrying IDs and facts only; the suite publishes no event of its own | DP-09; ADR-015 |
| BR12 | The freshness stamp carries no case data: it holds product codes, source codes and times only, so the panel assertion reads the product stamp and never a case field beyond the case identity | RWB-E1-015 BR10; DT02 |
| BR13 | The suite runs on synthetic data only and never against production or a production copy; expected-by times, cycles and the product-to-source map come from the fixture and the data rows, not from test code | RWB-E1-015 BR7; Principle 1 |

### 9. State transitions

None. This story does not change a case status. It proves the freshness status of a data product load: LOADED to STALE when the expected batch is missing or failed, and STALE to LOADED when a later COMPLETED batch arrives. The daily gate result is held in the job run, not in a table of its own.

| From | To | Trigger | Evidence the harness reads |
|---|---|---|---|
| LOADED | STALE | The expected batch is missing at the product cut-off, or a FAILED batch row is read | The stamp through the P1 freshness resource, plus `AceDataLate` on `rwb.source-data.events.v1` |
| LOADED | LOADED | A repeat read of the same COMPLETED row | The stamp row and its duplicate count |
| STALE | LOADED | A later COMPLETED batch for the same business date | The stamp through the P1 freshness resource, plus `AceDataReady` |
| HOLD | COMPLETE | Every source the day's jobs read is COMPLETED at the cut-off | The gate result in the run record of the P1 job resource |
| COMPLETE | HOLD | A source the day's jobs read is missing or FAILED at the cut-off | The gate result in the run record of the P1 job resource |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| QA integration engineer, release squad | Runs the harness, seeds and cleans the synthetic data set, reads the verdicts |
| Service owner of rwb-source-data | Answers the readiness call and the freshness, product-record and job reads; publishes EV-26 and EV-27; runs the reconciliation and the cut-off check |
| Service owner of rwb-case | Starts `DailyCaseRun` on the readiness event and answers the case record read for the data panel |
| Service owner of rwb-payment | Owns the payment matching and booking confirmation that wave 1 names but does not run; answers in RWB-ITG-W2 |
| Data steward | Reads the stamps and the gate result (Platform administration R) and receives the stale alert |
| Platform administrator | Reads the stamps and the gate result and receives the operations alert |
| Case roles with Case record R, for example the case owner and the team manager | Read the stamp in the case record data panel |
| Operations | Receives the stale alert on the operations channel and reads the job run |

### 11. Data

| BR Field ID | Entity | Owning schema or view | Field | Read or write |
|---|---|---|---|---|
| DF-ACE-178 | v_ace_batch_status | ACE view, read by rwb-source-data | source_system | Read |
| DF-ACE-179 | v_ace_batch_status | ACE view, read by rwb-source-data | business_date | Read |
| DF-ACE-180 | v_ace_batch_status | ACE view, read by rwb-source-data | started_at | Read |
| DF-ACE-181 | v_ace_batch_status | ACE view, read by rwb-source-data | completed_at | Read |
| DF-ACE-182 | v_ace_batch_status | ACE view, read by rwb-source-data | status | Read |
| DF-ACE-183 | v_ace_batch_status | ACE view, read by rwb-source-data | record_count | Read |
| DF-ACE-185 | v_ace_batch_status | ACE view, read by rwb-source-data | feed_version | Read |
| DF-ACE-186 | v_ace_batch_status | ACE view, read by rwb-source-data | is_complete | Read |
| DF-REF-071 | data_product | rwb_source_data (P1) | product_code | Read through the P1 contract |
| DF-REF-072 | data_product | rwb_source_data (P1) | product_name | Read through the P1 contract |
| DF-REF-077 | data_product | rwb_source_data (P1) | refresh_cycle | Read through the P1 contract |
| DF-REF-078 | data_product | rwb_source_data (P1) | expected_by | Read through the P1 contract |
| DF-OPS-001 to DF-OPS-009 | data_product_load | rwb_source_data (P1) | id, product_code, source_system, business_date, source_extracted_at, loaded_at, status, stale_flagged_at, duplicate_count | Read through the P1 freshness resource; written by P1 only |
| DF-RPT-002 | case_list_row | rwb_source_data (P1) | business_date | Read through the P1 job and case list resources (gate) |
| DF-RPT-019 | case_list_row | rwb_source_data (P1) | publish_status | Read through the P1 job and case list resources (gate) |
| DF-DEC-008 | decision_log_entry | rwb_decision (P7) | inputs_ref | Read through the P7 contract when the snapshot is asserted |

Field IDs are those in the Logical Data Model and Data Dictionary, taken from the field list of the legacy story; no other field is read by this slice. The harness reads and writes nothing directly: every field above is read through the owning service's contract or through the P1 views and resources (DP-01, DP-05), and `data_product_load` and `case_list_row` are written by rwb-source-data only.

The exact fixture composition — the row count of each synthetic batch row, the synthetic case set and the clock offsets of the run — is Not specified in the source documents (GAP-0340; ASM-0434); the fixture is the W1J01 data set, is synthetic, and carries no production value.

### 12. Contract

#### 12.1 REST operations provided

None. The suite provides no REST operation. The reserved names of P2 rwb-integration — `/api/recovery/integration/v1`, `rwb.integration.events.v1`, task queue `rwb-integration` and schema `rwb_integration` — are not used by this story, and no `rwb_integration` table is written.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the run | Budget |
|---|---|---|---|---|
| POST | `/api/recovery/source-data/v1/business-days/{date}/ready` | P1 rwb-source-data | The Airflow readiness trigger that starts the freshness step and the reconciliation for the business date | One hop, 2 s |
| GET | `/api/recovery/source-data/v1/data-products/freshness` | P1 rwb-source-data | The stamp per product and business date, and the gate result of the date | One hop, 2 s |
| GET | `/api/recovery/source-data/v1/data-products/{productCode}/records` | P1 rwb-source-data | The product records of DP01 and DP06 for the business date | One hop, 2 s |
| GET | `/api/recovery/source-data/v1/admin/jobs` | P1 rwb-source-data | The run record of JOB-04 (reconciliation) with its status and the gate result | One hop, 2 s |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The case record of the synthetic set, whose data panel carries the stamp | One hop, 2 s |

Every call is one hop on the owner's base with a 2 s timeout (DP-11, ADR-020), and every path is the path the owning CON story publishes. The suite calls the operations itself; it never reaches a service table and never chains a call through a second service.

#### 12.3 Events published

None. The suite publishes no event; it observes the events that the owners publish and asserts their envelope and their facts.

#### 12.4 Events consumed

| Event | Topic | Owner | Asserted in the run |
|---|---|---|---|
| `rwb.source-data.AceDataReady.v1` | `rwb.source-data.events.v1` | P1 rwb-source-data | The readiness event of the business date that starts `DailyCaseRun` (JOB-02) and the reconciliation (JOB-04); its CloudEvents ID, its source and its business date |
| `rwb.source-data.AceDataLate.v1` | `rwb.source-data.events.v1` | P1 rwb-source-data | The stale alert of AC2 and AC4, with source ALS and business date 2026-11-30, and the multi-source case of AC11 with source SVAF |
| `rwb.case.CaseCreated.v1` | `rwb.case.events.v1` | P3 rwb-case | The case of the synthetic set that the panel assertion reads, so the case and the stamp are tied to the same run |

`rwb.source-data.AceDataReady.v1` and `rwb.source-data.AceDataLate.v1` are published by rwb-source-data and `rwb.case.CaseCreated.v1` by rwb-case; all three carry IDs and facts only (DP-09, ADR-015).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Asserted in the run |
|---|---|---|---|
| `DailyCaseRun` | Workflow, started by AceDataReady | `rwb-case` | One run per business date, started by the readiness event (JOB-02) |
| `AceIngestCheck` | Workflow | `rwb-source-data` | One run per business date, confirming the ACE batch row and the stamp |
| Reconciliation (JOB-04) | Workflow, started by AceDataReady | `rwb-source-data` | One run per business date, with the gate result and the case list step |
| `matchPayments` | Activity | `rwb-payment` | Named for traceability only; rwb-payment is wave 2, so it does not run in this suite (RWB-ITG-W2) |
| `confirmBookings` | Activity | `rwb-payment` | Named for traceability only; rwb-payment is wave 2, so it does not run in this suite (RWB-ITG-W2) |

#### 12.6 Schedules

| Schedule or trigger | Owner | Cadence | Asserted in the run |
|---|---|---|---|
| JOB-02 case creation | P3 rwb-case | AceDataReady starts `DailyCaseRun` | The readiness event starts one case run for the business date |
| JOB-04 reconciliation | P1 rwb-source-data | Event-started workflow | One run per business date, with no shared Quartz table |
| Per-product cut-off check | P1 rwb-source-data | One trigger per product at `data_product.expected_by`, Asia/Bangkok | The cut-off that flags DP01 stale at 08:00 and leaves the 07:59 batch unflagged |

The cut-off is one trigger per product built from the product rows; there is no shared scheduler table (DP-10, ADR-016).

#### 12.7 Tables owned

None. The suite owns no table and never reads another service's schema (DP-01). `data_product_load` and `case_list_row` belong to rwb-source-data, and `case` belongs to rwb-case.

#### 12.8 Contract fakes

| Stub | Replaces | Note |
|---|---|---|
| ACE batch fixture (W1J01) | The ACE batch rows of the SIT date | Synthetic rows only; rwb-source-data reads them through its own `recovery.v_ace_batch_status` view, and the suite never opens the view |
| Airflow readiness stub | The bank Airflow call of the readiness edge | Calls the real P1 readiness operation; it does not replace it |
| Clock control | The system clock at the cut-off | Moves the cut-off of the run to the fixture times; it changes no service behaviour |

No service contract is faked. The P1, P3 and P7 contracts are the deployed ones, and a fake in the path fails the run.

#### 12.9 Call-type summary

| Call type | In this story |
|---|---|
| REST | 0 provided, 5 consumed; every call one hop on the owner's base with a 2 s timeout |
| Kafka | 0 published, 3 consumed and asserted; the owners publish and the harness observes |
| Temporal | 3 workflows and 2 activities named | `DailyCaseRun` on `rwb-case`; `AceIngestCheck` and the JOB-04 reconciliation on `rwb-source-data`; the `matchPayments` and `confirmBookings` activities of `rwb-payment` are named for traceability only and do not run in wave 1 |
| File | None |

### 13. Solution plan

**Deliverables.** One suite module that reuses the harness RWB-ITG-W1J01-ITG: an event driver, a clock control, fixtures for the batch rows and the synthetic case set, the five contract probes, the gate and panel assertions, and an evidence report with one verdict per test case. No service code and no schema change: the suite builds nothing that a service owns.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-02 | `recovery_svc` login | One login per service | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The story itself adds no build dependency on another integration story: it has no H and no C row, and its one integration dependency is RWB-P1-E1015-APP. The dependencies named in the table are the ones the **implementation** stories carry, because the harness observes what those stories build: DP-03 resolves to reading the decision records that the services write, DP-07 to reading the product rows through the deployed P1 and P3 contracts, DP-09 to asserting the owners' CloudEvents on their topics, DP-10 to observing the workflows and the per-product cut-off that RWB-P1-E1015-APP owns, DP-15 to reading the schemas that the DB stories create, and DP-19 to reading the case record panel through gateway-bff.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| BatchFixtureDriver | Test harness | Seeds the synthetic ACE batch rows of the W1J01 set and calls the P1 readiness operation for the business date |
| ClockControl | Test harness | Moves the cut-off and the batch completion times to the fixture values of AC2, AC4, AC6 and AC7 |
| FreshnessProbe | Test harness | Reads the stamp and the product records through the P1 contract and compares business date, source time, load time and status |
| GateProbe | Test harness | Runs the gate for 2026-11-30 and asserts HOLD with the product and the source, then COMPLETE with the recorded sources |
| JobRunProbe | Test harness | Reads the P1 job run and asserts the reconciliation run and the case list step of the date |
| WorkflowProbe | Test harness | Asserts one `DailyCaseRun` and one `AceIngestCheck` run per business date on the owners' queues through Temporal visibility |
| CasePanelProbe | Test harness | Creates the synthetic case through the P3 contract and reads the case record, asserting the stamp and MSG-P1-001 in the data panel |
| EventProbe | Test harness | Asserts the envelope and the facts of the three consumed events, and records the P8 start as not run |
| EvidenceReport | Test harness | Writes one verdict per test case, with the run ID, the contract versions and the fixture set used |

**Topology and fixtures.** One SIT environment with rwb-source-data, rwb-case and rwb-decision on their own bases, schemas and logins (DP-01, DP-02), namespace `rwb-recovery`, the SIT topics and the schema registry; rwb-payment is absent by design (X8). Synthetic fixtures only: the ALS COMPLETED row with record count 184,500, the FAILED row at 05:20, the 07:59 and 08:40 completions, the six COMPLETED sources plus the FAILED EFS row of AC9, the absent SVAF row of AC10, and CCMS to 2026-11-27 with SVAF to 2026-11-20 for AC11.

**Build steps**

1. BatchFixtureDriver and the W1J01 fixtures for the batch rows, the product rows and the synthetic case set; no production value.
2. ClockControl with the four fixture times, and the assertion that no test code holds an expected-by time or a refresh cycle.
3. FreshnessProbe over the freshness resource and the product-record resource, with the LOADED, STALE, duplicate-count and multi-source assertions.
4. WorkflowProbe and EventProbe over the owners' queues and topics, with the CloudEvents ID and the not-run record for JOB-07 and JOB-08.
5. GateProbe with the HOLD and COMPLETE runs, the named product and source, and the no-case-list-row assertion of AC9.
6. JobRunProbe and CasePanelProbe, with the case record read and the MSG-P1-001 panel state.
7. EvidenceReport with one verdict per test case and the contract versions of the run.
8. Clean-up: delete the synthetic cases, the fixture rows and the fixture files, and assert that no fixture row remains.

**Done when.** The twelve test cases of section 16 pass against the SIT wave-1 services, the stamp reads LOADED, STALE and LOADED again across AC1, AC2 and AC6, the gate reads HOLD and COMPLETE on the two fixtures, the case record shows the stale text of MSG-P1-001, the P8 start is recorded as not run, and the clean-up leaves no fixture row behind.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-001 | A product is stale, or the gate holds a job, shown in the case record data panel and the alert | {product} is from {date}. Today's ACE batch has not arrived. |
| MSG-GEN-001 | Malformed product code or date in the query | Enter {field}. |
| MSG-GEN-006 | The store, the view or a contract call is unavailable during the run | {system} is not available. Your request is queued and will be retried. |
| MSG-P4-002 | Role without Case record R | You cannot {action} here. Your role does not include it. |

No new message ID is introduced. The four messages are the legacy texts, copied unchanged, and the harness verdicts are for the release squad only.

### 15. Screens and states

SCR-03 Case record, state Read only: the data panel shows each product's business date and load time, and the Stale input state shows MSG-P1-001 next to the stale product. The suite reads that panel through `GET /api/recovery/case/v1/cases/{caseId}` and asserts the state, and it takes no screenshot and changes no screen. SCR-45 Data quality is Epic 2 and out of scope. The suite also reads the job run through the P1 job resource, which is the Epic 1 surface the data steward uses for the gate result.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-015-09-ITG | Access | Integration | RW-REFADM calls GET /data-products/freshness on the P1 base; refused with MSG-P4-002; end-to-end: real services on the wave 1 contracts |
| TC-E1-015-01-ITG | AC1, BR1 | Integration | ALS batch row for 2026-11-30, started 23:30, completed 05:40; DP01; end-to-end: real services on the wave 1 contracts |
| TC-E1-015-02-ITG | AC2, BR2 | Integration | No COMPLETED ALS row at 08:00; test clock; end-to-end: real services on the wave 1 contracts |
| TC-E1-015-03-ITG | AC3, BR5 | Integration | Decision for RW-2026-000101 reading DP01 and DP06; end-to-end: real services on the wave 1 contracts |
| TC-E1-015-04-ITG | AC4, BR3 | Integration | ALS batch row FAILED at 05:20; end-to-end: real services on the wave 1 contracts |
| TC-E1-015-05-ITG | AC5, BR6 | Integration | Same COMPLETED row read twice; end-to-end: real services on the wave 1 contracts |
| TC-E1-015-06-ITG | AC6 | Integration | Late ALS batch at 08:40 after the stale flag; end-to-end: real services on the wave 1 contracts |
| TC-E1-015-07-ITG | AC7 | Integration | ALS batch at 07:59; end-to-end: real services on the wave 1 contracts |
| TC-E1-015-08-ITG | AC8, BR7 | Integration | Weekly DP06 batch on Monday; check on Thursday; end-to-end: real services on the wave 1 contracts |
| TC-E1-015-10-ITG | AC9, BR8 | Integration | EFS batch FAILED at the 08:00 cut-off; case list step stub; end-to-end: real services on the wave 1 contracts |
| TC-E1-015-11-ITG | AC10, BR8 | Integration | Every source COMPLETED for 2026-11-30; end-to-end: real services on the wave 1 contracts |
| TC-E1-015-12-ITG | AC11, BR4 | Integration | CCMS COMPLETED 2026-11-27; SVAF only to 2026-11-20; end-to-end: real services on the wave 1 contracts |

The twelve legacy test cases are carried as integration copies in the order of the WP, keep the legacy IDs with the `-ITG` suffix, the legacy Covers and the legacy data; the legacy level System maps to Integration and Access to Integration. The copies of TC-E1-015-01-ITG, -02, -04, -05, -06, -07, -09, -10 and -11-ITG are the ones this story signs off; the remaining copies are carried as regression evidence for the end-to-end run. The full Given, When and Then of each legacy test case is in the story test cases tab of the test case workbook under the legacy ID.

### 17. Guardrails

- Synthetic data only: every batch row, product row and case in the run is a W1J01 fixture value, and no production row, extract or copy is loaded into SIT for this story.
- No personal data in stamps, events, logs or fixtures: the stamp carries product codes, source codes and times only, and the synthetic case set carries no real person and no real account.
- No read of another service's tables: every cross-service value comes through the owner's contract, one hop with a 2 s timeout (DP-01, DP-11), and the suite asserts that no process reads `rwb_case` or `rwb_source_data`.
- No business value in test code: expected-by times, refresh cycles, the product-to-source map and the alert channel come from the fixture and the data rows, and the suite reads them back from the P1 contract before it asserts.
- CloudEvents 1.0 IDs and facts only: the suite asserts the envelope and the facts of the three consumed events and publishes none.
- No production access: the suite points at the SIT bases only, and a base that resolves outside SIT fails the run before the first assertion.
- Clean-up always runs: the synthetic cases, the fixture rows and the fixture files are removed at the end of the run, and the suite fails when a fixture row remains.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-RDF-009 | Every data product carries a freshness stamp from the ACE batch record; every decision records the freshness of the data it used | Business Requirements Epic 1, sections 3.1 and 4 | FEAT-RDF-14, FEAT-DRI-12 | All recovery processes; 17 Run the decision center | R-UNI-40; BR-P1-014-2 to BR-P1-014-4 | TC-E1-015-01-ITG to TC-E1-015-12-ITG |

| Trace element | Contract element | Test cases |
|---|---|---|
| RWB-E1-015 (legacy story) | The whole slice: sections 12.2, 12.4, 12.5 and 12.6 | TC-E1-015-01-ITG, TC-E1-015-02-ITG, TC-E1-015-04-ITG, TC-E1-015-05-ITG, TC-E1-015-06-ITG, TC-E1-015-07-ITG, TC-E1-015-09-ITG, TC-E1-015-10-ITG, TC-E1-015-11-ITG |
| RWB-P1-E1015-APP | The P1 resources of 12.2 and the per-product cut-off of 12.6 | TC-E1-015-01-ITG, TC-E1-015-02-ITG, TC-E1-015-04-ITG, TC-E1-015-10-ITG, TC-E1-015-11-ITG |
| ADR-015 (Kafka with outbox, inbox and CloudEvents) | The three consumed events of 12.4 and the empty 12.3 | TC-E1-015-01-ITG, TC-E1-015-02-ITG, TC-E1-015-05-ITG, TC-E1-015-12-ITG |
| ADR-020 (contract-first REST, one hop, 2 s timeout) | The five consumed operations of 12.2 | TC-E1-015-09-ITG, TC-E1-015-10-ITG |
| DP-09 (outbox and inbox, CloudEvents) | The event assertions of 12.4 | TC-E1-015-02-ITG, TC-E1-015-05-ITG |
| DP-10 (Temporal Schedule or event-started workflow) | The workflows of 12.5 and the triggers of 12.6 | TC-E1-015-01-ITG, TC-E1-015-06-ITG, TC-E1-015-10-ITG, TC-E1-015-11-ITG |

### 19. Out of scope

- The P1 build of the stamp, the gate, the cut-off check, the reconciliation and the events (RWB-P1-E1015-APP).
- The P1 contract baseline and the P1 deployment, dashboards and runbook (RWB-P1-E1015-CON and RWB-P1-E1015-OPS).
- The legacy acceptance criteria this slice does not own: AC3 (freshness in the decision log) and AC8 (a weekly product between its batches).
- The P8 wave 2 behaviour, including the JOB-07 and JOB-08 starts of AC1 and AC6 (RWB-ITG-W2).
- The build of the harness RWB-ITG-W1J01-ITG itself; this story reuses it.
- The non-functional epic RWB-ITG-NFR, including the performance and browser tests.
- SCR-45 Data quality (Epic 2).
- The data lake, which is removed (DP-17, ADR-018), and any lake copy of the released case list.
