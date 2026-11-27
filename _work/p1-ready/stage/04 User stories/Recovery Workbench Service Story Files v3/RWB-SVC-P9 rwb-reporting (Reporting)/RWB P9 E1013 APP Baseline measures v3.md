# RWB-P9-E1013-APP Baseline measures

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P9-E1013-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-reporting |
| Service epic | RWB-SVC-P9 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Size | To be sized by the squad at refinement |
| Legacy key | RWB-E1-013 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP05, DP07, DP10, DP11, DP13, DP15, DP17, DP19 |
| Parallel lane | L-P9-A |
| Ready to start | Day 1 |
| Depends on (build) | RWB-P9-E1013-CON, RWB-PLT-E1027-CON, RWB-PLT-E1043-CON, RWB-PLT-E1071-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON |
| Contract dependencies | RWB-P3-E1043-CON, RWB-P3-E1018-CON, RWB-P1-E1015-CON |
| Contract version | rwb-reporting.yaml 5.1.0 (API Specification v7), `/v1`; consumes rwb-source-data.yaml 5.1.0 (API Specification v7) |
| Integration dependencies | None |
| External dependencies | RWB-P9-E1013-OPS (not done yet; an external dependency, not a build input of this story); the 05:30 late-check Schedule of RWB-P1-E1015-APP, the rwb-source-data worker, the task queue and the topic registration (RD-P1-022; RD-P1-040; GAP-0561 closed by RD-P1-041) |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P9 rwb-reporting v1.md (no FR mapped to REQ-RDF-012) |
| Status | Draft (directive resolutions) |
| Readiness decisions | RD-P1-001, RD-P1-002, RD-P1-004, RD-P1-005, RD-P1-010, RD-P1-022, RD-P1-041, RD-P1-061, RD-P1-066 |

**Version 3 changes** (D-RCV-60 P1 developer readiness, RD-P1 register).

- RD-P1-066: Align the JOB-15 start and deployment with the Airflow call and paused Schedule.
- Backfill the published Test Cases v9 cross-references.
- RD-P1-005, RD-P1-061: Pin account-form payments and the 5.1.0 freshness shape.
- Freshness stamps and the gate are RWB-P1-E1015-APP's: status `LOADED` or `STALE`, `businessDate` null when never stamped, stamp in use is the latest row; AC17 and AC18 added (RD-P1-005, RD-P1-022, RD-P1-041; finding #3).
- `listEligibleAccounts` is not called by this service; the rules BR1, BR2, BR5 and BR7 are held here only (RD-P1-010, RD-P1-022; finding #4).
- Error answers carry `messageCode`; the key refusals of the definition load and AC19 added (RD-P1-001, RD-P1-004; findings #6, #7).
- Pending: run product codes and completeness logic (GAP-3383, GAP-3434), payment since-entry rule and workload access (GAP-3427), and snapshot activity integration (GAP-3384).

**Change log.** D-RCV-60, 22 November 2026: the rwb-reporting slice of RWB-E1-013, split from the legacy one-module story. The six measures, their versioned definitions in `measure_definition`, the snapshot, the baseline and frozen flags in `rwb_reporting`, the 01:30 run of JOB-15 as a Temporal Schedule on queue `rwb-reporting` (DP-10), the read of case facts and payments on the rwb-case and rwb-source-data contracts (DP-01, DP-05, DP-11) and the two reads on base `/api/recovery/reporting/v1` (DP-13) are this story's. The INT-19 lake extract, its trailer and the lake hold of MSG-GEN-006 are removed by DP-17, the case facts are RWB-P3-E1013-APP's, the payments and the completeness gate are RWB-P1-E1013-APP's, AC2 and AC6 are proved end to end by RWB-ITG-E1013-ITG, and the plan's C row does not carry the rwb-source-data rows (GAP-2566, GAP-2567, GAP-2568, GAP-2569, GAP-2570, GAP-2571, GAP-2572, GAP-2573, GAP-2575; ASM-4232, ASM-4233, ASM-4234, ASM-4235, ASM-4236, ASM-4237, ASM-4238, ASM-4239, ASM-4241). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P9-E1013-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (31 resolved, 33 cross-document, 6 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **Tribe lead (RW-TRIBE)**, I want **cases by route, age and queue, realized recovery, time in stage and turnaround per route published as the baseline, with each definition agreed by the Tribe, held as a versioned data row and computed from the Workbench records read on the contracts of the services that own them**, so that **every later epic is measured against the same frozen baseline and no team counts a case its own way**. The **Reporting and BI analyst (RW-BIANAL)** publishes and the **reference data administrator (RW-REFADM)** loads.

This story is the largest of the four slices of RWB-E1-013. It owns:

- six of the eight legacy acceptance criteria, copied word for word with their origin tag (AC1, AC3, AC4, AC5, AC7, AC8), and the rules, messages and screens they depend on;
- `measure_definition`, `measure_snapshot` and `measure_publish` in schema `rwb_reporting`, with the frozen-row protection and the per-service Flyway migration (DP-01, DP-15);
- one calculator per measure code, each reading facts only on the rwb-case case-facts read and the rwb-source-data payments read, one hop with a 2 s budget (DP-05, DP-11);
- the version of the definition in force on a business date, resolved through the reference-data framework of rwb-case at its version (DP-07);
- the 01:30 run of JOB-15 on `rwb-reporting` in namespace `rwb-recovery`, started by the Airflow report-run call while the Temporal Schedule that replaces the Quartz trigger (DP-10) is created paused (RD-P1-066), with its decision record written before the snapshot changes (DP-03);
- the baseline flag and the frozen flag of business date 2026-11-27, the publish state of a business date, and the freshness stamp the reporting read model carries;
- `GET /reports/measures` and the definitions read on base `/api/recovery/reporting/v1`, and the baseline state of SCR-44 behind the gateway-bff composite route (DP-13, DP-19).

It does not own: the case facts of a business date and their age banding, which are RWB-P3-E1013-APP's; the payments since entry, which are RWB-P1-E1013-APP's; the daily completeness gate and the freshness stamp of a data product, which are RWB-P1-E1015-APP's and published in RWB-P1-E1015-CON (RD-P1-022); AC2 and AC6, which are proved end to end by RWB-ITG-E1013-ITG; the published shapes, the three tables' columns, the closed lists, the consumed rows and the fakes, which are RWB-P9-E1013-CON's; the steering dashboard SCR-37, its data set and the agent measures, which are RWB-P9-E2009-APP's; the data lake and the INT-19 extract, which Arch v5 removes (DP-17); and the deployment, the Schedule registration, the panels and the alerts, which are RWB-P9-E1013-OPS's.

### 2. Business rationale

Measures are counted by hand from spreadsheets at month end today, and each team counts a case differently. Legacy RWB-E1-013 answered this inside one module: the definitions, the case and payment facts, the snapshot, the frozen baseline and the nightly lake extract sat together. Arch v5 splits the same capability along the lines of who owns the facts, so the legacy story becomes four slices: the case facts (P3), the payments and the gate (P1), this service, and the cross-service proof (ITG).

What D-RCV-60 changes here, and why each change is safe:

1. **The measure is data, not code.** Legacy BR1 already said a measure is published only under a definition in force that names its data product, formula, unit and approver. `measure_definition` holds that row with its version and its valid-from date, the six calculators are driven by the row, and no measure code, formula, unit or band is written in Java (REQ-RDF-012; Principle 1; legacy BR7 for the all-or-nothing load).
2. **The facts stay with their owners.** `recovery_case` is P3's and `v_ace_payment` is reached only through rwb-source-data (Architecture v5 slides 29, 37 and 45; DP-01, DP-05). This service reads them on the two published contracts and holds no grant on `rwb_case`, no `v_ace_*` grant and no ACE table.
3. **The clock leaves Quartz.** The Quartz row of JOB-15 becomes a Temporal Schedule on `rwb-reporting` (DP-10; ADR-016), created paused; the run starts once per business date at 01:30 Asia/Bangkok from the Airflow report-run call until the final trigger is ruled (RD-P1-066; GAP-3573).
4. **The run is a recorded decision.** The version of the definition in force, the row count and the business date are recorded through the local decision record before the snapshot changes, so a published number can always be explained (DP-03; ADR-022). NFR-065 asks for measures from Workbench records and the decision log, and this record is the reporting half of it.
5. **The lake is gone.** Arch v5 removes the data lake, INT-19 and INT-20, and rwb-reporting builds its read model in its own schema (DP-17; ADR-018). The publish, the freshness stamp and the hold survive inside `rwb_reporting`; the extract file, its trailer and the lake client do not.

Three consequences are recorded rather than smoothed over. AC3 and AC7 name the lake, the extract file, its trailer and the lake-unavailable hold, and they are owned here, so the story keeps their text word for word and implements the equivalent publish and hold inside its own schema (GAP-2566; ASM-4232). Power BI has no lake to read in the target, and no source says how the 07:30 refresh reaches the snapshot (GAP-2570; ASM-4236). The two rows this service consumes from rwb-source-data — the payments since entry and the daily completeness gate — are class C dependencies in fact but sit in no plan row (GAP-2567; ASM-4233).

### 3. Preconditions

- RWB-P9-E1013-CON is published with its fakes: the two read operations, the three tables' columns of DF-RPT-031 to DF-RPT-058, the six closed lists, the consumed rows, the decision-record element, the rights and the error envelope. Its shapes are fixed on Day 1 and this story builds no surface of its own.
- RWB-P3-E1013-APP answers the facts of a business date on `GET /api/recovery/case/v1/cases/facts` with the as-of time, the row count and the reference version, with its fake, so the six calculators can be built before rwb-case is live.
- RWB-P3-E1018-CON is published with its fake: the case record read and the account link of a case, which is what the payments read of RWB-P1-E1013-APP is called with.
- RWB-P1-E1013-APP builds `GET /api/recovery/source-data/v1/payments?accountKey={accountKey}`, declared in RWB-P1-E1015-CON (RD-P1-061). Pending: since-entry rule and workload access (GAP-3427).
- RWB-P1-E1015-CON publishes `GET /api/recovery/source-data/v1/data-products/freshness` with its fake: query `product` and `asOf`; each element with `productCode`, `businessDate` (null for a never-stamped product) and `status` `LOADED` or `STALE` (RD-P1-005, RD-P1-041). The two rwb-source-data rows are class C dependencies that the plan's C row does not carry (GAP-2567; ASM-4233).
- RWB-P3-E1043-CON is published with its fake: the reference list read of `measure-unit`, `measure-dimension`, `measure-publish`, `product` and `data-product`, each at its version in force. The list codes are those of TSD P9 T3.2 and the read is the reference-data contract of rwb-case (DP-07).
- RWB-PLT-E1027-CON (DP-03), RWB-PLT-E1043-CON (DP-07), RWB-PLT-E1071-CON (DP-10), RWB-PLT-E1044-CON (DP-15) and RWB-PLT-N001-CON (DP-19) are published as platform baselines, so no build item here invents a decision-record, reference-data, workflow, migration or route mechanism.
- Schema `rwb_reporting` exists with its own login and the per-service Flyway sequence, and `measure_definition`, `measure_snapshot` and `measure_publish` are created by this story's migration `V1013__measures.sql` because no DB story sits in this key's story set (DP-15; GAP-2575; ASM-4241).
- The definition file of six rows is prepared with the Tribe lead's approval on each row, and `rwb.reporting.baseline-date` is set to 2026-11-27. The approver reference is "TRB-0001" in the legacy file while TSD P9 T3.1 types `approved_by` as `uuid` (GAP-2571; ASM-4237).
- The ACE business date 2026-11-27 is complete: rwb-source-data holds a `LOADED` stamp of 2026-11-27 for each data product the run requires (the product set is Pending, GAP-3383; the gate value over REST is Pending, GAP-3434), and case creation has run for the date. This story reads that answer and calls no ACE view.
- No approval is needed to build against a Draft contract baseline or an In-review FSD; the contract is tagged by RWB-P9-E1013-CON when its tests pass (ASM-4242).

### 4. Flow

1. RW-REFADM loads the definition file through the reference-load operation of this service for table `measure_definition`, with the approver, the approval date and valid-from 2026-11-21. The operation's path is not specified in the source documents and is declared by RWB-P9-E1013-CON (GAP-2568; ASM-4234).
2. `MeasureDefinitionLoadHandler` checks every row for a measure code, a name, a formula, a data product, a unit, an approver and an approval date against the closed lists of the contract; one invalid row refuses the whole load and no version is put in force (legacy BR7; AC1, AC4).
3. The version in force for a business date is the row set whose `valid_from` is the latest one on or before that date; `MeasureCatalogService` answers it for the date, with each measure's data product and formula, on the definitions read of the contract (AC1).
4. At 01:30 Asia/Bangkok Airflow calls `POST /reports/{id}/run`, which opens the run of JOB-15 for the previous business date on queue `rwb-reporting` (RD-P1-066; legacy §12 trigger); the Temporal Schedule stays paused.
5. `FreshnessGateClient` reads the freshness of rwb-source-data for the business date. A required product with `status` `STALE`, or a gate answer HOLD, leaves the run in its waiting state, writes no baseline row and names the product and its date with MSG-P1-001 (legacy BR4; AC6 proves this end to end in the ITG story; AC17, AC18). How the gate value COMPLETE or HOLD is carried over REST is Pending (GAP-3434), and so are the product codes the run checks and the date shown when `businessDate` is null (GAP-3383).
6. `CaseFactClient` reads the facts of the business date on the rwb-case contract: one row per case with product group, route, stage, queue, entry date, stage clock start, closed date and status, paged, with the as-of time and the reference version. No case table is read (DP-01, DP-11).
7. `PaymentClient` reads the payments since entry of each account of those cases on the rwb-source-data contract, one hop for an account (PaymentsAnswer, RD-P1-061). The account link comes from the case record read of RWB-P3-E1018-CON.
8. The six calculators compute, per definition in force: `CASES_BY_ROUTE`, `CASES_BY_AGE`, `CASES_BY_QUEUE`, `REALIZED_RECOVERY`, `TIME_IN_STAGE` and `TAT_BY_ROUTE`. Each writes one `measure_snapshot` row per measure, product and dimension value with the definition version, the business date and its value or case count (AC1, AC2 in the ITG story).
9. `DecisionRecordWriter` writes one local decision record for the run — definition version, business date, row count, as-of time and the gate answer — before the snapshot rows commit; a failed write changes nothing and the caller sees MSG-P7-003 (DP-03; legacy AC5).
10. `BaselineFreezer` marks the rows of the baseline business date `is_baseline` and `frozen`. The trigger on `measure_snapshot` refuses an UPDATE or a DELETE of a frozen row, and the service refuses the rerun with MSG-P9-001 naming the date (legacy AC5; BR2).
11. `PublishStateRecorder` writes the `measure_publish` row of the business date: `PUBLISHED` with the case-list count and the snapshot count when the two agree, `HELD` with the reason when they do not, and the freshness stamp of the read model (legacy BR5; AC3, AC7).
12. A measure listed for the run with no definition in force is not computed, no value is written for it, and the run record names it with MSG-P9-003 (legacy AC8).
13. A repeated run for the same business date, definition version and dimension replaces nothing that is frozen, writes no second decision record and counts the repeat.
14. `GET /reports/measures` answers the snapshot for a period, and the definitions read answers the catalog for a date; SCR-44 shows the run and its state through the gateway-bff composite route, read only (DP-13, DP-19).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A definition row has no formula or no data product | Load refused in full; no version in force | MSG-GEN-001 | AC4, TC-P9-E1013-APP-07 |
| X2 | The baseline is published a second time | Refused; frozen values unchanged | MSG-P9-001 | AC5, TC-P9-E1013-APP-08 |
| X3 | The gate answer for the baseline date is HOLD, or a data product the run requires reads `STALE` | No baseline row is written; the run waits and names the product and its date | MSG-P1-001 | AC6 (ITG, owned by RWB-ITG-E1013-ITG), X7, AC17, AC18 |
| X4 | The publish cannot complete | The `measure_publish` row is `HELD` with its reason; an alert goes to the operations channel and the next run publishes it | MSG-GEN-006 | AC7, TC-P9-E1013-APP-09 |
| X5 | A measure has no definition in force | No value is written; the run record names the measure | MSG-P9-003 | AC8, TC-E1-013-08 |
| X6 | The decision record cannot be written | The transaction writes nothing: no snapshot row, no publish state and no baseline flag | MSG-P7-003 | AC9, TC-E1-013-12 |
| X7 | The rwb-case or rwb-source-data read does not answer inside 2 s, or its breaker is open | The run waits and retries on the workflow's own schedule; nothing is written and no partial snapshot is published | None (503 on a read) | AC10, §12.2, TC-E1-013-13 |
| X8 | A statement or a test reaches `recovery_case`, a `v_ace_*` view or another service's schema | The grant refuses the statement and the boundary test fails the build | None (pipeline log) | AC11, §17, TC-E1-013-14 |
| X9 | A measure code, formula, unit or band value appears in Java | The guardrail test fails the build | None | AC12, §17, TC-E1-013-15 |
| X10 | A frozen row is updated or deleted, by the service, a script or a person | The trigger refuses the statement and the transaction rolls back | None (database error) | AC13, TC-E1-013-16 |
| X11 | The definition load carries no, a blank or a non-UUID `Idempotency-Key`; a key already used for another request or still in flight; or the key store is unavailable | 400, 409 or 503; no definition row is written | MSG-PLT-N009-03, MSG-PLT-N009-05, MSG-PLT-N009-06 | AC19 |

X1 to X5 are the five exception paths of the legacy story carried onto the split, X6 and X7 are the record and the call types the target adds, X8 and X9 are the boundaries of DP-01 and DP-17, and X10 is the protection legacy BR2 asked the database for. X11 is the platform key rule on the definition load (RD-P1-001). The data lake of legacy X4 has no target system, so X4 is the publish state of the read model (GAP-2566; ASM-4232).

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-P9-E1013-CON and its fakes, the rwb-case facts fake, the rwb-source-data payments and freshness fakes, the reference-list fake and the decision-record stub; needs no live P1, P3 or ACE |
| Negotiable | The activity and component names, the run record shape and the table of the freshness stamp are this story's choice; the measures, the formulas, the unit values, the messages and the columns are fixed |
| Valuable | Every later epic is measured against one frozen baseline computed from Workbench records, and the value of a published number can be explained by its definition version |
| Estimable | Three tables, one migration, one Schedule, one workflow, six calculators, three clients and two reads |
| Small | Fits two weeks with its tests on the fakes, the two P1 and P3 slices having taken the facts out |
| Testable | Each criterion runs on the synthetic 120-case set of the legacy Background, with the six measure totals of AC2 asserted in the ITG story |

### 7. Acceptance criteria

```gherkin
Feature: Baseline measures

  Background:
    Given the synthetic case set for business date 2026-11-27 holds 120 open cases: 60 Mortgage, 45 Hire purchase and 15 SSME
    Given age bands are "0-90", "91-180", "181-365", "366-730" and "over 730" days since entry

  Scenario: AC1 Definitions agreed (legacy RWB-E1-013 AC1)
    Given the rwb-case contract mock returns the reference version in force on 2026-11-21
    Given a definition file of 6 rows for "CASES_BY_ROUTE", "CASES_BY_AGE", "CASES_BY_QUEUE", "REALIZED_RECOVERY", "TIME_IN_STAGE" and "TAT_BY_ROUTE"
    Given each row names its data product, formula, unit and approver "TRB-0001" with approval date 2026-11-20
    When it is loaded with valid from 2026-11-21
    Then definition version "MD-2026.11" is in force with 6 measures
    Then each measure returns its data product and formula through MeasureCatalog

  Scenario: AC3 Power BI data set (legacy RWB-E1-013 AC3)
    Given the rwb-case contract mock returns the case facts of 2026-12-01 and the rwb-source-data contract mock returns the payments of 2026-12-01
    Given the baseline measures are published
    When JOB-15 runs at 01:30 on 2026-12-02
    Then the INT-19 extract for business date 2026-12-01 is in the data lake with freshness stamp 2026-12-01 and the record count in its trailer
    Then the extract holds the baseline rows of 2026-11-27 unchanged
    Then the job monitor records the JOB-15 run with its row count, start and end time

  Scenario: AC4 Definition without a formula refused (legacy RWB-E1-013 AC4)
    Given a definition file where row "TIME_IN_STAGE" has no formula
    When it is loaded
    Then the system refuses the load in full with MSG-GEN-001 naming "formula"
    Then the system puts no definition version in force

  Scenario: AC5 Baseline published twice (legacy RWB-E1-013 AC5)
    Given the gateway-bff contract mock returns the SCR-44 rerun answer for JOB-15
    Given the baseline for 2026-11-27 is frozen
    When JOB-15 is rerun for business date 2026-11-27 from SCR-44
    Then the frozen rows are unchanged
    Then the run record shows MSG-P9-001 naming 2026-11-27

  Scenario: AC7 Data lake unavailable (legacy RWB-E1-013 AC7)
    Given the rwb-source-data contract mock returns the freshness answer for 2026-11-30
    Given the data lake load area does not answer
    When JOB-15 runs at 01:30 on 2026-12-01
    Then the system writes measure_snapshot rows for 2026-11-30 in the Workbench
    Then the system holds the extract and an alert goes to the operations channel with MSG-GEN-006 naming "Data lake"
    Then the system sends the extract by the next JOB-15 run

  Scenario: AC8 Measure with no definition in force (legacy RWB-E1-013 AC8)
    Given the extract configuration lists measure "COST_PER_CASE" with no definition in force
    When JOB-15 runs at 01:30 on 2026-11-30
    Then the system writes no value for "COST_PER_CASE"
    Then the run record shows MSG-P9-003 naming "COST_PER_CASE"

  Scenario: AC9 Decision record not written (target, X6) (new, D-RCV-60)
    Given the decision record for the run of business date 2026-11-27 cannot be written
    When JOB-15 runs for business date 2026-11-27
    Then the system writes no snapshot row, no publish state and no baseline flag
    Then the run outcome shows MSG-P7-003

  Scenario: AC10 Source read not answering in time (target, X7) (new, D-RCV-60)
    Given the rwb-source-data contract mock does not answer inside 2 s for the payments read
    When JOB-15 runs at 01:30 on 2026-11-30
    Then the system writes nothing and publishes no partial snapshot
    Then the run waits and retries on the workflow's own schedule

  Scenario: AC11 Statement outside the owner schema refused (target, X8) (new, D-RCV-60)
    Given a build statement reaches "recovery_case", a "v_ace_*" view or another service's schema
    When the boundary test runs
    Then the grant refuses the statement
    Then the boundary test fails the build

  Scenario: AC12 Measure value in Java refused (target, X9) (new, D-RCV-60)
    Given a measure code, formula, unit or band value appears in Java
    When the guardrail test runs
    Then the guardrail test fails the build

  Scenario: AC13 Frozen row changed (target, X10) (new, D-RCV-60)
    Given the baseline for 2026-11-27 is frozen
    When a frozen row is updated or deleted, by the service, a script or a person
    Then the trigger refuses the statement
    Then the transaction rolls back

  Scenario: AC14 Rules with no criterion (target, BR3, BR4, BR6, BR9, BR10, BR11, BR12, BR13) (new, D-RCV-60)
    Given a run for business date 2026-11-27 whose gate answer is not COMPLETE
    When JOB-15 runs for business date 2026-11-27
    Then no measure is published as the baseline
    Then the decision record is written before the snapshot rows commit, with the definition version, the business date, the row count and the gate answer
    Then a repeated run for the same business date, definition version and dimension writes once and counts the repeat
    Then no person name, address, contact value or identity number enters rwb_reporting, the record, a log or a workflow input
    Then no v_ace_* read, no ACE table and no ACE batch rerun is made by this service

  Scenario: AC15 Provided operation answers 401, 403 or 404 (target) (new, D-RCV-60)
    Given a request to a provided operation without a valid token
    Given the same operation called with a role that lacks its right
    Given the same operation called for a case or run that does not exist
    When the request is made
    Then the answer is 401 with `messageCode` MSG-P4-001 for the request without a valid token
    Then the answer is 403 with `messageCode` MSG-P4-002 for the role that lacks its right
    Then the answer is 404 with `messageCode` MSG-P4-003 for the resource that does not exist
    Then each answer is `application/problem+json`

  Scenario: AC16 Activity retried and timed out at 2 s (target, ADR-020) (new, D-RCV-60)
    Given the rwb-case contract mock does not answer inside 2 s for a read
    When the activity runs
    Then the read retry is Not specified in the source documents (NEWAC-RWB-P9-E1013-APP-AC17)
    Then the activity stops at the 2 s timeout and the run waits

  Scenario: AC17 Stale data product holds the run (target, X3, BR4) (new, D-RCV-60)
    Given the rwb-source-data contract mock returns, for a data product "DP01" that the run requires, status "STALE" with businessDate "2026-11-27"
    When JOB-15 runs for business date 2026-11-30
    Then the system writes no measure_snapshot row and sets no baseline flag
    Then the run is held with MSG-P1-001 naming "DP01" and 2026-11-27

  Scenario: AC18 Never-stamped data product holds the run (target, X3, BR4) (new, D-RCV-60)
    Given the rwb-source-data contract mock returns, for a data product that the run requires, status "STALE" with businessDate null
    When JOB-15 runs for business date 2026-11-30
    Then the system writes no measure_snapshot row and sets no baseline flag
    Then the run is held and names the product

  Scenario: AC19 Definition load with a refused Idempotency-Key (target, X11) (new, D-RCV-60)
    Given the definition load is called without an Idempotency-Key header
    Given a second call reuses the key of an accepted load with another file
    When the requests are made
    Then the first answer is 400 with `messageCode` MSG-PLT-N009-03
    Then the second answer is 409 with `messageCode` MSG-PLT-N009-05
    Then neither call writes a measure_definition row
```

The six criteria are the legacy criteria of RWB-E1-013 word for word, with their origin tag added and nothing else changed: the repeated `Then`, the legacy wording of `it is loaded`, `the data lake load area does not answer` and `the extract configuration` all stand. The added `Given the <service> contract mock returns <x>` lines are the only additions, and they keep every value of the legacy text. **AC2 and AC6 are not here**: they name the frozen baseline values and the completeness gate across services and are proved end to end by RWB-ITG-E1013-ITG, with the case facts in RWB-P3-E1013-APP, the payments in RWB-P1-E1013-APP and the gate in RWB-P1-E1015-APP. Two points are recorded rather than smoothed over. AC3 and AC7 assert a data lake, an INT-19 extract, its trailer and a lake hold, and Arch v5 removes the lake (DP-17): this story keeps the legacy text as the record of intent, and the deliverable it proves is the publish state of business date 2026-12-01, the freshness stamp of the read model and the hold of the same date with its alert and its next-run resend, all inside `rwb_reporting` (GAP-2566; ASM-4232). `MeasureCatalog` in AC1 is the definitions read of §12.1, because the monolith's Java interface no longer exists; the legacy path of the definition load is `POST /admin/reference-loads`, and the target path of the same operation is declared by RWB-P9-E1013-CON (GAP-2568; ASM-4234). Every Power BI destination of the legacy text is read as the reporting read model, and every data lake delivery as a file delivery (GAP-1646). AC9 to AC13 are the target criteria of exceptions X6 to X10 and have no legacy counterpart.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Each measure is published only under a definition in force that names its data product, formula, unit and approver | REQ-RDF-012; Principle 1 |
| BR2 | The baseline is the snapshot of the configured baseline business date and is frozen once written | REQ-RDF-012; FEAT-RPT-01 |
| BR3 | Measures are computed from Workbench records read through the owning modules, never from a separate count | NFR-065 |
| BR4 | A measure is computed only from a COMPLETED ACE batch; stale data is not published as the baseline | CTL-02; MSG-P1-001 rule |
| BR5 | The extract to the data lake holds the publish and alerts on failure, and runs again in the next window | INT-19 error handling |
| BR6 | Age bands are a reference list | Principle 1 |
| BR7 | A definition load with any invalid row is refused in full | refdata.txt change process, step 3 |
| BR8 | The publish and the hold are rows of `measure_publish` in `rwb_reporting`, with the freshness stamp of the read model; the lake, its extract file and its trailer are removed | DP-17; ADR-018; GAP-2566 |
| BR9 | The frozen row is protected twice: the service refuses the rerun with MSG-P9-001 and the database trigger refuses an UPDATE or a DELETE where `frozen = true` | Legacy BR2; TSD P9 T3.1 |
| BR10 | The decision record of a run is written before the snapshot rows commit, with the definition version, the business date, the row count and the gate answer; a failed write changes nothing | DP-03; ADR-022; legacy AC5 |
| BR11 | No person name, address, contact value or identity number enters `rwb_reporting`, the record, a log or a workflow input; the snapshot carries identifiers, codes, dates, counts and amounts only | Template and Rules v1 §R7.2 (s17); legacy §17 |
| BR12 | ACE data reaches this service only on the rwb-source-data contract: no `v_ace_*` read, no ACE table and no ACE batch rerun | DP-05; Architecture v5 slides 29, 37 and 45 |
| BR13 | A repeated run for the same business date, definition version and dimension writes once and counts the repeat | Architecture v5 slide 11; TSD P9 T-A.2 |

BR1 to BR7 are the legacy rules copied character for character. Version 3 of RWB-P1-E1013-APP removes BR1, BR2, BR5 and BR7 from the rwb-source-data slice, so these measure rules are held and enforced by this story only (RD-P1-022). BR5 names a data lake that Arch v5 removes, so the rule is applied as BR8: the publish and the hold survive as a row of `measure_publish` and the freshness stamp of the read model, and the lake destination, the trailer count and the INT-19 adapter are gone (GAP-2566; ASM-4232). BR6 is executed where the band is assigned: the case-fact read of RWB-P3-E1013-APP carries the band code of the version in force, and this service counts it and never bands a case itself.

### 9. State transitions

The case keeps its state with rwb-case; this story moves no case. It sets the baseline flag and the frozen flag of `measure_snapshot`, the state of `measure_publish` and the run state of JOB-15 (legacy §9).

| Object | From | Event | To |
|---|---|---|---|
| measure_definition | none | A load with every row valid | The version is in force from its `valid_from` |
| measure_definition | in force | A load with one invalid row | Unchanged: no version is put in force (AC4) |
| measure_definition | in force | A later version with a later `valid_from` | The later version is in force from its date; earlier snapshots keep their recorded version |
| measure_snapshot | none | The run of a business date completes | Rows written with the definition version and the business date |
| measure_snapshot | written | The business date is the baseline date | `is_baseline = true`, `frozen = true`, and no change is possible afterwards (AC5) |
| measure_snapshot | frozen | An UPDATE or a DELETE | Refused by the trigger; the transaction rolls back |
| measure_publish | none | The counts agree and the snapshot is written | `PUBLISHED` with the freshness stamp (AC3, AC7) |
| measure_publish | none | A source is stale or the counts differ | `HELD` with the reason, and the next run publishes it (AC7) |
| JOB-15 run | waiting | The gate answers COMPLETE | running |
| JOB-15 run | running | The snapshot, the record and the publish commit | complete |
| JOB-15 run | running | A read fails or the record cannot be written | failed, with nothing written (X6, X7) |
| JOB-15 run | waiting | The gate answers HOLD, or a required data product reads `STALE` | held, with MSG-P1-001 naming the product and its date (X3, AC17, AC18) |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-TRIBE, Tribe lead and squad members | Agrees the definitions, is named as approver on each row and reads the baseline (Reporting R) |
| RW-REFADM, reference data administrator | Loads the definition file on the reference-load operation of this service and sees a refused load (Reference data C) |
| RW-BIANAL, Reporting and BI analyst | Publishes the measure set, reads the snapshot and builds the Power BI data set from it (Reporting CRUD) |
| RW-DATASTEW, data steward | Reads the run record, the publish state and the freshness stamp (Reporting CRU) and receives a held publish |
| RW-FINANCE, Finance and CFO delegate | Reads the baseline (Reporting R) |
| RW-PLATADM, platform administrator | Reruns JOB-15 from SCR-44 and reads the run state (Platform administration U) |
| rwb-reporting service identity (the rwb-reporting login, DP-02) | Reads its own three tables, writes the record and the schema rows, calls the P3 and P1 contracts and holds no grant on another `rwb_*` schema and none on a `v_ace_*` view |

The rights are the rows of TSD P9 T6.1; RW-TRIBE holds Reporting R and RW-BIANAL Reporting CRUD there, and no role outside the rows is given a right by this story. DP-08 is not in this key's pattern set: the capability area and the right are declared per operation and the check is the service template's cached permission decision, so this story states the rights and builds no guard of its own. On each operation of base `/api/recovery/reporting/v1` the rwb-access authorise check (DP-08) is called for the capability area and right declared in this table; its identifier is Not specified in the source documents (DOR-RWB-P9-E1013-APP-6).

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-RPT-031 to DF-RPT-040 | measure_definition (P9, `rwb_reporting`) | id, measure_code, name, formula, data_product, unit, definition_version, approved_by, approved_at, valid_from | Write, one row set per version |
| DF-RPT-041 to DF-RPT-052 | measure_snapshot (P9, `rwb_reporting`) | id, measure_code, definition_version, business_date, product_group, dimension_code, dimension_value, value, case_count, is_baseline, frozen, published_at | Write, one row per measure, product and dimension value |
| DF-RPT-053 to DF-RPT-058 | measure_publish (P9, `rwb_reporting`) | id, business_date, status, case_list_count, dashboard_count, held_reason | Write, one row per business date |
| Standard columns | the three tables | `is_active`, `state`, `version`, `created_at`, `created_by`, `updated_at`, `updated_by` | Write, with the optimistic lock of `version` |
| DF-CAS-001, 003, 005, 006, 008, 010, 013, 018, 022 | recovery_case (P3) | id, product_group, status, stage_code, route_code, queue_id, entry_date, stage_clock_start, closed_date | Read on the case-facts contract only; never as a table |
| DF-WRK-002 | queue (P3) | queue_code | Read on the case-facts contract only |
| DF-CAS-025, DF-CAS-026 | case_account (P3) | case_id, account_key | Read on the case-record contract only, to call the payments read per account |
| DF-ACE-045, DF-ACE-046 | `v_ace_payment` (P1) | payment_date, payment_amount | Not read here: the payments arrive on the rwb-source-data read (BR12) |
| DF-DEC-001 to DF-DEC-031 | decision record (PLT library, created in `rwb_reporting`) | the run record | Write, before the snapshot commits |
| Reference rows | reference list of P3 | the values of `LOV-DATA-PRODUCT`, `LOV-MEASURE-UNIT`, `LOV-MEASURE-DIM`, `LOV-PRODUCT` and `LOV-MEASURE-PUBLISH` | Read on the reference-data contract, at their version |

Field IDs are those of the Logical Data Model and Data Dictionary, TSD P9 T3.1 and T3.2 and the legacy Data table. The three tables arrive with this story's migration `V1013__measures.sql` in the per-service Flyway sequence (DP-15; GAP-2575; ASM-4241); the decision record and the idempotency key are platform library objects created in `rwb_reporting` by the library's own migration (DP-03). **Read-model controls:** measure_definition, measure_snapshot and measure_publish are P9's control tables in `rwb_reporting`; the frozen value of a business date is a `measure_snapshot` row marked frozen, and the publish gate is the `measure_publish` row; its column names are Not specified in the source documents (GAP-0255). Queue measures stay with P3 in `rwb_case` and are not copied here. **No personal data:** the rows carry measure codes, dimension codes and values, business dates, counts, amounts, list values and a definition version, and no name, address, contact value, identity number or account number is copied into this schema. An owner or team on a dimension enters this schema as an ID only, keyed from the case-facts read; its display name is resolved in P3 behind the rwb-access masking policy and is never stored here. The measures read `GET /reports/measures` on base `/api/recovery/reporting/v1` is declared in this wave 1 contract for the harness and the catalog consumer; the dashboard, its data set and SCR-37 stay in RWB-P9-E2009-APP, and the connection of any reporting client to the read is an open decision for the PRD step.

### 12. Contract

Contract version built against: v1 (the `/v1` segment of every path in this section and of the base `/api/recovery/reporting/v1`).

#### 12.1 REST operations provided

Owner rwb-reporting (P9); base `/api/recovery/reporting/v1` (DP-13). The shapes and the errors are declared by RWB-P9-E1013-CON.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| GET | `/reports/measures` | Measure[] for the period of the query `measure`, `product`, `route`, `from`, `to`; each element carries the measure code, the definition version, the business date, the product group, the dimension code and value, the value or the case count and the freshness stamp of the read model (API-P9-001) | Reporting, right R, scope applied | Not applicable |
| GET | `/measure-definitions` | The definitions in force on `onDate`, each with its measure code, name, data product, formula, unit and version; the read RWB-P3-E1013-APP consumes | Reporting, right R, scope applied | Not applicable |

The two operations answer `application/problem+json` with one `messageCode` per status (RD-P1-004): 401 MSG-P4-001, 403 MSG-P4-002, 422 MSG-GEN-001 for a period or a date that cannot be read, and 503 MSG-GEN-006 when the store does not answer. The published rwb-reporting.yaml 5.1.0 holds `GET /reports/measures` only, without 422: the definitions read and the 422 element are to be added by RWB-P9-E1013-CON. The operation ID API-P9-001 is that of TSD P9 T-A.1 and the path is the target base, not the monolith form. The definitions read is the legacy `MeasureCatalog` interface turned into a contract, because RWB-P3-E1013-APP consumes it across a service boundary (DP-11); no source document gives its path or its shape, so the path above is declared here and the gap is recorded (GAP-2572; ASM-4238). The legacy story assigns `GET /reports/measures` to RWB-E2-009, while the Ownership Map gives the operation to P9 and the wave 1 harness calls it, so the shape is declared here and the dashboard's use of it, its filters and SCR-37 stay RWB-P9-E2009-APP's (GAP-2570; ASM-4236).

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| GET | `/api/recovery/case/v1/cases/facts` | P3 rwb-case | The facts of one business date: one row per case, paged, with the as-of time, the row count and the reference version (RWB-P3-E1013-APP); faked |
| GET | `/api/recovery/case/v1/cases/{caseId}` family | P3 rwb-case | The case record and its account link, which is what the payments read is called with (RWB-P3-E1018-CON); faked |
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case | The five closed lists at their version in force (RWB-P3-E1043-CON, the plan's C row); faked |
| GET | `/api/recovery/source-data/v1/data-products/freshness?asOf={date}` | P1 rwb-source-data | The freshness of each data product: `productCode`, `businessDate` (nullable) and `status` `LOADED` or `STALE`; the stamp in use is the latest row (RWB-P1-E1015-CON; rwb-source-data.yaml 5.1.0). The local run completeness evaluation is Pending (GAP-3434). The gate value COMPLETE or HOLD has no member in the published answer (GAP-3434); faked |
| GET | `/api/recovery/source-data/v1/payments?accountKey={accountKey}` | P1 rwb-source-data | `PaymentsAnswer` of rwb-source-data.yaml 5.1.0. Account-form rows are ordered by `paymentDate` then `paymentCode`; `businessDate` is the DP01 stamp. Interim unpaged. 409 MSG-P1-001 when gated. Pending: since-entry rule and caller identity (GAP-3427). |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The last two rows are class C dependencies of this story that the plan's C row does not carry, and the absence is recorded (GAP-2567; ASM-4233). The rwb-decision row of the legacy contract is not consumed: the local decision record is this service's and the central ledger behind it is the library's.

#### 12.3 Events published

None. The context pack and the Ownership Map give rwb-reporting the topic `rwb.reporting.events.v1` with its retry and `.dlt` topics by the naming rule (DP-14) and **no event row**; this story therefore declares no event, no producer group and no outbox row, and a build that adds one fails the absence test of the contract baseline. RWB-ITG-E1013-ITG names `rwb.reporting.ReportPublished.v1` on that topic as the freshness signal of its journey, which no owner document gives this service, so the two statements are recorded as a conflict rather than resolved quietly: the event belongs to whoever publishes it and is not declared here (GAP-2569; ASM-4235). The decision record of a run travels on the platform's `rwb.decision-record.v1` through the library, and that is not an event of this service.

#### 12.4 Events consumed

None. This story subscribes to nothing: the run is started by the Airflow report-run call and the facts are read on the two contracts. A run that needs a later source arrives on the next daily call, and the ITG story waits on the reads rather than on an event. A build that declares a consumer group, a subscription or an inbox row of its own fails the absence test.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `MeasureRunWorkflow` | Workflow, one execution per business date | `rwb-reporting` in namespace `rwb-recovery` | Input: the business date, the baseline date, the definition version in force and the gate answer; output: the row count, the publish state and the outcome. No child workflow and no signal from another service |
| `measureRun` | Activity, the step that reads, computes, freezes and publishes | `rwb-reporting` | The facts, the payments and the gate answer in; the snapshot rows, the record, the publish state and the run outcome out, in one transaction per business date |
| `snapshot(page)` | Activity registered by RWB-P1-E1013-APP on `rwb-source-data` | `rwb-source-data` | The measures read of the ACE view contract (RD-P1-002; Temporal Workflow and Activity Catalog v3 names the measures build of this service as its caller). Pending: whether `measureRun` calls it beside the REST reads of 12.2 (GAP-3384) and its fields and cursor (GAP-3425; GAP-0563) |

The two activity names of this service are target design choices and are fixed by no source. `listEligibleAccounts` is not an activity of this capability: it is built by RWB-P1-E1018-APP and called only by `DailyCaseRun` of rwb-case (RD-P1-010), and a build of this service that calls it fails the boundary test. The remote `snapshot(page)` is declared with one hop and a 2 s timeout (ADR-020). The run has one Schedule, JOB-15 at 01:30 Asia/Bangkok, which is paused: Airflow starts the run through the report-run call (RD-P1-066). The baseline is frozen by this run and is not written back to the snapshot provider on rwb-source-data (GAP-1503). The remote activity supplies facts only; no measure code, definition version, baseline date value or total is read from it (GAP-0562).

#### 12.6 Schedules

Airflow calls `POST /reports/{id}/run` at 01:30 Asia/Bangkok for the prior business date. Create the JOB-15 Temporal Schedule paused. Pending final trigger owner: solution architect with the rwb-reporting owner (GAP-3573).

One Temporal Schedule, on `rwb-reporting` in namespace `rwb-recovery`: the run of JOB-15 for the previous business date at 01:30 Asia/Bangkok, one run per business date, with a catch-up policy of one missed run and no overlapping execution. It replaces the Quartz row of the legacy job (DP-10). Its Temporal Schedule ID is a target choice and is not given by any source; the legacy job ID JOB-15 is kept in the run record and on SCR-44. While the Schedule is paused, the one live trigger is the Airflow report-run call (RD-P1-066; GAP-3573; earlier reading GAP-2573, ASM-4239).

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| measure_definition | P9 (`rwb_reporting`) | The agreed definition of a measure by version; written by the load and read by the catalog |
| measure_snapshot | P9 (`rwb_reporting`) | The value of one measure for a date, product and dimension value, with the baseline and frozen flags |
| measure_publish | P9 (`rwb_reporting`) | The publish or hold state of a business date, with the two counts and the reason |
| decision_record, idempotency_key, outbox_event | PLT library, created in `rwb_reporting` | The local record of a run, the repeat key and the library object that carries no row because no event is published (12.3) |

Not owned and never read as a table: `recovery_case`, `queue`, `case_account` and the reference rows (P3), `v_ace_payment` and every `v_ace_*` view (P1), `decision_log_entry` (P7). No foreign key leaves `rwb_reporting` and no join crosses a schema (DP-01). RWB-P9-E2009-CON publishes the delta of `measure_publish` for the steering dashboard on top of this baseline, so the publish state this story writes is extended there and not redefined.

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case case-facts fake | The 120 cases of 2026-11-27 with their product group, band code, route, stage, queue, entry date, stage clock start, closed date and status, the as-of time and the reference version; a date with no case | AC3, AC7, X7 |
| rwb-case case-record and reference-list fake | The account link of a case and the five closed lists at their version | AC1, AC3 |
| rwb-source-data payments and freshness fake | The payments since entry of an account for 2026-11-30 and 2026-12-01 (PaymentsAnswer, RD-P1-061); freshness elements with status `LOADED`, `STALE` with a `businessDate` and `STALE` with `businessDate` null; no answer beyond 2 s | AC3, AC7, X3, X7 |
| Local decision-record stub (`RWB-PLT-E1027-CON`) | A healthy chain and outbox, and a stopped chain | AC5, X6 |
| gateway-bff composite route fake | The merged SCR-44 answer with the run of 2026-11-27 in its complete state | AC5 |
| Frozen-row fixture | A `measure_snapshot` row with `frozen = true`, and an UPDATE and a DELETE against it | AC5, X10 |

The fakes are test-only and are replaced by the real services in SIT. The path of the definitions read and the field list inside it are stubbed from this story's own contract and carry the placeholder until the P3 team confirms them (GAP-2572; ASM-4238).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 5 consumed | The measures read and the definitions read on `/api/recovery/reporting/v1`; the facts read, the case record read, the reference-list read, the freshness read and the payments read; one hop, 2 s |
| Kafka | 0 published, 0 consumed | No event of this story (§12.3, §12.4); the record travels on the platform topic |
| Temporal | 1 workflow, 1 activity, 1 Schedule | `MeasureRunWorkflow`, `measureRun` and the 01:30 Schedule on `rwb-reporting` |
| File | None | No extract file, no trailer and no lake client; the lake is removed (DP-17) |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.reporting`, module `baseline`, Java package `th.co.scb.ace.workbench.recovery.reporting.baseline`; front end `src/modules/recovery/reporting/MeasureRun.tsx`, the fragment SCR-44 embeds, read only.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_reporting`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none; the release holds no `v_ace_*` grant |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/reporting/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-17 | Data lake, INT-19, INT-20 | Removed (no data lake); reporting from events into rwb-reporting | none; the story needs the lake data of its legacy ACs and the removal is the gap GAP-2566 |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

Read one by one: DP-01 is the three tables and the refusal to join any other service's schema; DP-03 is the run record written before the snapshot commits; DP-05 is a boundary, since the payments and the gate arrive on the P1 contract and no `v_ace_*` view is read; DP-07 is live for the five closed lists, read at their version; DP-10 replaces the Quartz row of JOB-15 with the 01:30 Schedule; DP-11 turns the two in-process interfaces of the legacy §12 into contracts with fakes; DP-13 moves the two reads to the service base; DP-15 carries the migration; DP-17 removes the lake, its extract, its trailer and its hold, and the publish and the hold move into `measure_publish`; DP-19 is how SCR-44 shows the run. The six H rows are exactly the plan's, and the two rwb-source-data consumed rows are C in fact and absent from the plan's C row (GAP-2567; ASM-4233).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `MeasureDefinitionLoadHandler` | Service | The all-or-nothing load of a definition file with the BR7 checks and the closed lists |
| `MeasureCatalogService` | Service | The definitions in force on a business date and the answer of the definitions read |
| `MeasureCalculators` | Service | One calculator per measure code, reading facts only on the contracts and never banding a case |
| `MeasureRunWorkflow` and `measureRun` | Workflow and activity | The run of a business date: gate, read, compute, record, write, freeze, publish |
| `SnapshotWriter` and `BaselineFreezer` | Repository | The `measure_snapshot` rows, the baseline and frozen flags, the optimistic lock and the single transaction |
| `DecisionRecordWriter` | Library adapter | The run record, hash-linked and written before any row changes (DP-03) |
| `PublishStateRecorder` | Service | The `measure_publish` row, the two counts, the reason, the freshness stamp and the next-run resend |
| `CaseFactClient`, `PaymentClient`, `FreshnessGateClient`, `ReferenceListClient` | Clients | The five consumed rows, one hop each, 2 s, breaker, no retry of their own |
| `ReportingController` | Controller | The two reads, the capability area and right, the problem mapping and the paging |
| `MeasureRun` | React component | The run and its state on SCR-44, read only; its empty, loading, error and no access states are Not specified in the source documents (CG-ALL-7808); SCR-37 is not built by this story (E2) |

**Database and migrations.** One file in the per-service sequence, `V1013__measures.sql`: the three tables, their unique keys (`measure_code`, `definition_version` on the definition; `measure_code`, `definition_version`, `business_date`, `product_group`, `dimension_code`, `dimension_value` on the snapshot; `business_date` on the publish), and the trigger that refuses an UPDATE or a DELETE of a frozen snapshot row. No column is added for a case fact, a band, an account or a payment: those are the owners' and are read, not copied (DP-01).

**Configuration and reference data.** The baseline business date `rwb.reporting.baseline-date` = 2026-11-27; the six definitions at version MD-2026.11 loaded as rows; the five closed lists read from rwb-case at their version; the 01:30 time of the Schedule, the 2 s budget and the one-hop rule as platform values; feature flag `rwb.reporting.baseline`.

**Build steps**

1. The migration with the frozen trigger; test that an update of a frozen row fails (X10, BR9).
2. `MeasureDefinitionLoadHandler` and `MeasureCatalogService` with the six-row file and the invalid row; tests for AC1 and AC4.
3. `CaseFactClient` and the case-record read against their fakes, with the no-answer and the out-of-time paths (X7).
4. `PaymentClient` and `FreshnessGateClient` against their fakes, with the HOLD, the stale and the never-stamped product (X3, X7, AC17, AC18).
5. The six calculators against the synthetic 120-case set of the Background, with the values of AC2 asserted in the ITG story.
6. `MeasureRunWorkflow` and `measureRun` with the gate, the record, the snapshot, the freeze and the repeat; tests for AC3, AC5 and AC8.
7. `PublishStateRecorder` with the published and the held date, the alert and the next-run resend; test for AC7.
8. `ReportingController` with the two reads, the rights and the problem mapping (AC1, AC3).
9. The boundary and guardrail tests: no statement outside `rwb_reporting`, no `v_ace_*` read, and no measure code, formula, unit or band value in Java (X8, X9).

**Done when.** The tests of section 16 pass, SIT publishes the six measures of 2026-11-27 with definition version MD-2026.11 and freezes them, a rerun leaves the frozen rows unchanged and answers MSG-P9-001, a definition without a formula is refused in full, a held publish names its reason and is published by the next run, and a measure with no definition in force is listed and not published.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A definition row lacks a required value (X1) | Enter {field}. |
| MSG-P9-001 | The baseline is published again (X2) | The baseline for {date} is frozen. It cannot be published again. |
| MSG-P1-001 | The ACE batch for the business date is not COMPLETE (X3) | {product} is from {date}. Today's load has not arrived. |
| MSG-GEN-006 | The publish cannot complete and is held (X4) | {system} is not available. Try again in a few minutes. |
| MSG-P9-003 | A measure has no definition in force (X5) | {measure} has no approved definition. It is not published. |
| MSG-P7-003 | The decision record cannot be written before the snapshot changes (X6) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | A role holds no right on a read or on the definition load | You cannot {action} here. Your role does not include it. |
| MSG-P4-001 | No valid session or no Recovery Workbench role (401) | Your session is not valid or you have no Recovery Workbench role. Sign in again or ask your team manager to request one. |
| MSG-P4-003 | The record does not exist or is outside the scope (404) | This case is not in your scope. |
| MSG-PLT-N009-03 | The definition load has no valid `Idempotency-Key` (X11) | The Idempotency-Key header is required and must be valid for {operation}. |
| MSG-PLT-N009-05 | The key conflicts with another request (X11) | The Idempotency-Key conflicts with another request to {operation}. |
| MSG-PLT-N009-06 | The key store is unavailable (X11) | The idempotency store for {operation} is unavailable. No changes were saved. Try again in a few minutes. |

The five legacy message IDs are copied from the legacy section 14 and FSD P9 A2.1.3.1; MSG-P7-003 and MSG-P4-002 are the platform messages of DP-03 and of the guard, and MSG-P4-001, MSG-P4-003 and the three MSG-PLT-N009 codes are the platform answers of RD-P1-001 and RD-P1-004. MSG-GEN-006 takes the English text of Error and Message Standard v6, which replaces the legacy wording; no new message is added. MSG-GEN-006 names a system that in the target is the reporting read model's publish step and not a data lake (GAP-2566; ASM-4232).

### 15. Screens and states

No new screen. SCR-44 Interface and job monitor shows the JOB-15 run in its running, held, failed and complete states through the gateway-bff composite route (DP-19), and the run record, the publish state and the freshness stamp are its field list's. Its empty, loading, error and no access states are Not specified in the source documents (CG-ALL-7808). Its release state is not shown and no message is defined for a held facts release (GAP-2242). The Tribe lead and the Reporting and BI analyst read the baseline in the report built from the snapshot, and SCR-37 Steering dashboard with its data set is RWB-P9-E2009-APP's; its empty, error and no-access states are Not specified in the source documents (CG-ALL-7807). The refusal, held and not-recorded states read the messages of section 14.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-013-08 | AC8, BR1 | Component | COST_PER_CASE with no definition; no value written and MSG-P9-003 |
| TC-E1-013-09 | Access | Component | RW-BIANAL calls the definition load; refused with MSG-P4-002 and no row written |
| TC-E1-013-10 | §12.2, §12.3, §12.5 | Component | The operations, events and activities of section 12 against their contract fakes; one hop and 2 s each |
| TC-E1-013-11 | §12.7, DP-01 | Component | The three tables and the library objects of §12.7; a statement to any other schema is refused |
| TC-E1-013-12 | AC9, BR3 | Component | Decision record write refused; no snapshot row, publish state or baseline flag, and MSG-P7-003 |
| TC-E1-013-13 | AC10, §12.2 | Component | Payments read not answering inside 2 s; nothing written and no partial snapshot; the run waits |
| TC-E1-013-14 | AC11, BR5 | Component | A statement to recovery_case or a v_ace_* view; the grant refuses it and the boundary test fails the build |
| TC-E1-013-15 | AC12, BR1 | Component | A measure code, formula, unit or band value in Java; the guardrail test fails the build |
| TC-E1-013-16 | AC13, BR6 | Component | A frozen row updated or deleted; the trigger refuses the statement and the transaction rolls back |
| TC-E1-013-17 | AC14, BR3, BR4, BR6, BR9, BR10, BR11, BR12, BR13 | Component | A run whose gate answer is not COMPLETE; the decision record written first, a repeat counted once, no personal data and no ACE read |
| TC-P9-E1013-APP-01 | AC15, §12.2 | Component | A provided operation called without a valid token, by a role without its right and for a missing resource; answers 401, 403 and 404 |
| TC-E1-013-19 | AC16, §12.2 | Component | A read not answering inside 2 s; retry Not specified in the source documents (NEWAC-RWB-P9-E1013-APP-AC17); the activity stops at the 2 s timeout and the run waits |
| TC-P9-E1013-APP-02 | AC17 | Component | DP01 reads STALE with businessDate 2026-11-27; the run is held with MSG-P1-001 |
| TC-P9-E1013-APP-03 | AC18 | Component | A required product reads STALE with businessDate null; the run is held |
| TC-P9-E1013-APP-04 | AC19 | Component | Definition load without a key and with a reused key; 400 and 409, no row |
| TC-P9-E1013-APP-05 | AC1 | Component | Definition file of 6 rows approved by TRB-0001 |
| TC-P9-E1013-APP-06 | AC3 | Component | JOB-15 on 2026-12-02 for business date 2026-12-01 |
| TC-P9-E1013-APP-07 | AC4 | Component | TIME_IN_STAGE with no formula |
| TC-P9-E1013-APP-08 | AC5 | Component | JOB-15 rerun for 2026-11-27 |
| TC-P9-E1013-APP-09 | AC7 | Component | Data lake load area stubbed unavailable |

The seven cases are the legacy cases of RWB-E1-013 for the criteria this story owns, in their legacy order, with the Level column added: the legacy level System maps to `Component` because each runs on the contract fakes, and Access maps to `Component` for the same reason. **TC-E1-013-02 and TC-E1-013-06 are not here**: AC2 and AC6 cross rwb-case, rwb-source-data and rwb-reporting and are proved by RWB-ITG-E1013-ITG as `TC-E1-013-02-ITG` and `TC-E1-013-06-ITG`. In the staged Recovery Workbench Test Cases v9.xlsx only TC-E1-013-08 is a row of this key; the other IDs of this table hold rows of RWB-P1-E1013-APP there, so the rows of this story are the mapped cases in this section, under IDs the test writer assigns. TC-E1-013-10 and TC-E1-013-11 are this story's own contract and boundary tests for section 12 and section 12.7; TC-E1-013-12 to TC-E1-013-16 prove the criteria AC9 to AC13 for exceptions X6 to X10; none of them is a legacy case.

### 17. Guardrails

- No business value in code: the six measure codes, their formulas, the four unit values, the age bands, the product groups and the baseline date are definition rows, reference rows or configuration, never a constant, a default or a branch of the build.
- No personal data in `rwb_reporting`, a workflow input, a log or a test: measure codes, dimension codes, dates, counts, amounts and a definition version only, and every fixture is synthetic.
- ACE data only through the owner's contract: this service holds no `v_ace_*` grant and reads no ACE table, and a build that adds one fails the boundary test (BR12).
- The case stays with rwb-case: no `recovery_case` row, no case status and no band assignment is made here; the band arrives on the fact (BR3, BR6).
- Frozen rows are protected by the trigger as well as by the service, and a build that writes around the trigger fails the review (BR9).
- One base, one topic, one queue, one schema and one login per service; no document or test names another service's base or topic as its own (DP-13, DP-14).
- No retired element is reintroduced: no data lake, no INT-19 extract, no trailer, no Quartz row, no shared job table and no event published by this story (DP-17, §12.3).
- The record is written before the snapshot commits; a build that publishes a measure without its decision record fails the review (DP-03).
- Schema migration: the three tables, their unique keys and the frozen-row trigger are carried in `V1013__measures.sql` in this service's own Flyway sequence (DP-15); the deployment story of this key replays the same sequence and no DB story is raised (GAP-2575).

### 18. Traceability

| Requirement ID | Requirement (short) | Story element | Test cases | Feature | L3 process |
|---|---|---|---|---|---|
| REQ-RDF-012 | Baseline measures published with definitions agreed by the Tribe (BRD Epic 1, sections 3.8 and 4; FEAT-RDF-19, FEAT-RPT-01) | The definition load, the catalog, the six calculators, the snapshot, the frozen baseline and the publish state | TC-P9-E1013-APP-05, TC-P9-E1013-APP-06, TC-P9-E1013-APP-07, TC-P9-E1013-APP-08, TC-P9-E1013-APP-09, TC-E1-013-08 | FEAT-RDF-19, FEAT-RPT-01 | Not specified in the source documents (DOR-RWB-P9-E1013-APP-2) |
| NFR-065 | Business measures come from the Workbench records and the decision log, not a separate count | The two contract reads and the run record | TC-P9-E1013-APP-06, TC-P9-E1013-APP-08 | Not specified in the source documents (DOR-RWB-P9-E1013-APP-2) | Not specified in the source documents (DOR-RWB-P9-E1013-APP-2) |
| NFR-067 | Every scheduled job has a run book, monitoring and an alert | The run record and the publish alert this story writes; the panels and the run book are RWB-P9-E1013-OPS's | TC-P9-E1013-APP-06, TC-P9-E1013-APP-09 | Not specified in the source documents (DOR-RWB-P9-E1013-APP-2) | Not specified in the source documents (DOR-RWB-P9-E1013-APP-2) |
| ADR-014 | Schema and login per service | `rwb_reporting` and its own login | TC-P9-E1013-APP-05 | Not specified in the source documents (DOR-RWB-P9-E1013-APP-2) | Not specified in the source documents (DOR-RWB-P9-E1013-APP-2) |
| ADR-018 | No data lake; rwb-reporting read model from events and records | The `measure_publish` state and the freshness stamp, and the removed extract | TC-P9-E1013-APP-06, TC-P9-E1013-APP-09 | Not specified in the source documents (DOR-RWB-P9-E1013-APP-2) | Not specified in the source documents (DOR-RWB-P9-E1013-APP-2) |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The five consumed rows with their budget and breaker | TC-P9-E1013-APP-06 | Not specified in the source documents (DOR-RWB-P9-E1013-APP-2) | Not specified in the source documents (DOR-RWB-P9-E1013-APP-2) |
| ADR-022 | Local decision record plus central ledger | The run record written before the snapshot | TC-P9-E1013-APP-08 | Not specified in the source documents (DOR-RWB-P9-E1013-APP-2) | Not specified in the source documents (DOR-RWB-P9-E1013-APP-2) |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E1-013, disposition Split (rework); features FEAT-RDF-19 and FEAT-RPT-01 |
| Legacy criteria | AC1, AC3, AC4, AC5, AC7 and AC8 owned word for word by this story; AC2 and AC6 owned end to end by RWB-ITG-E1013-ITG; AC3 and AC7 are proved on `measure_publish` with no lake path or extract element in the contract (GAP-2566) |
| Source text | The legacy story, FSD P9 Reporting v3 A2.1, A2.8 and T3.2 of the TSD, and TSD P9 Reporting v2 T3.1, T3.2 and T-A |
| Test cases | TC-P9-E1013-APP-05 to TC-P9-E1013-APP-09 and TC-E1-013-08; the -ITG copies of -02 and -06 sit in RWB-ITG-E1013-ITG |
| Feature and screens | FEAT-RDF-19, FEAT-RPT-01; SCR-44 (SCR-37 is E2) |
| Decoupling patterns | DP01, DP03, DP05, DP07, DP10, DP11, DP13, DP15, DP17, DP19 |
| Architecture decisions | ADR-014, ADR-018, ADR-020, ADR-022, and ADR-016 for the Schedule |

### 19. Out of scope

- The published shapes, the three tables' columns, the six closed lists, the consumed rows, the decision-record element, the rights, the error envelope and the fakes: RWB-P9-E1013-CON.
- The case facts of a business date and their age banding: RWB-P3-E1013-APP.
- The payments since entry: RWB-P1-E1013-APP. The daily completeness gate and the freshness stamp of a data product: RWB-P1-E1015-APP.
- The cross-service proof of AC2 and AC6 and the `-ITG` copies of these test cases: RWB-ITG-E1013-ITG.
- The steering dashboard SCR-37, its data set, the queue and ageing measures for team managers (FEAT-RPT-02) and benefit realisation tracking against the baseline (FEAT-RPT-06, Epic 6): RWB-P9-E2009-APP and later epics, outside this service's wave 1 slice.
- The data lake, INT-19 and INT-20, the extract file, its trailer and the lake hold: removed by Arch v5 and DP-17, and no story rebuilds them.
- The reference list of rwb-case, its load, its approval and its rollback: RWB-P3-E1043-APP.
- The Schedule registration, the chart, the migration job, the panels, the alerts and the run books: RWB-P9-E1013-OPS.
- The decision log copy to the data lake (RWB-E1-014): retired, with no new story.

### Remaining delivery steps

- Close GAP-3426, GAP-3427 and GAP-3518 and publish the payments shape and fake (rwb-source-data contract owner).
- Close GAP-3434 and GAP-3383 before the gate client is built (solution architect).
- Close GAP-3384 (solution architect).
- Give the criteria of this story their rows in Test Cases v9 (QA lead).
- Size the story at refinement (squad).
- Epic design sign-off (solution architect).
- RWB-P9-E1013-CON Done and its fakes published (rwb-reporting squad).
- Test data in DEV (QA lead).
