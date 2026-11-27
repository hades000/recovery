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
| Legacy key | RWB-E1-013 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP05, DP07, DP10, DP11, DP13, DP15, DP17, DP19 |
| Parallel lane | L-P9-A |
| Ready to start | Day 1 |
| Depends on (build) | RWB-P9-E1013-CON, RWB-PLT-E1027-CON, RWB-PLT-E1043-CON, RWB-PLT-E1071-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON |
| Contract dependencies | RWB-P3-E1043-CON, RWB-P3-E1018-CON |
| Integration dependencies | None |
| External dependencies | RWB-P9-E1013-OPS |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P9 rwb-reporting v1.md (no FR mapped to REQ-RDF-012) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the rwb-reporting slice of RWB-E1-013, split from the legacy one-module story. The six measures, their versioned definitions in `measure_definition`, the snapshot, the baseline and frozen flags in `rwb_reporting`, the 01:30 run of JOB-15 as a Temporal Schedule on queue `rwb-reporting` (DP-10), the read of case facts and payments on the rwb-case and rwb-source-data contracts (DP-01, DP-05, DP-11) and the two reads on base `/api/recovery/reporting/v1` (DP-13) are this story's. The INT-19 lake extract, its trailer and the lake hold of MSG-GEN-006 are removed by DP-17, the case facts are RWB-P3-E1013-APP's, the payments and the completeness gate are RWB-P1-E1013-APP's, AC2 and AC6 are proved end to end by RWB-ITG-E1013-ITG, and the plan's C row does not carry the rwb-source-data rows (GAP-2566, GAP-2567, GAP-2568, GAP-2569, GAP-2570, GAP-2571, GAP-2572, GAP-2573, GAP-2575; ASM-4232, ASM-4233, ASM-4234, ASM-4235, ASM-4236, ASM-4237, ASM-4238, ASM-4239, ASM-4241). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P9-E1013-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As the **Tribe lead (RW-TRIBE)**, with the **Reporting and BI analyst (RW-BIANAL)** publishing and the **reference data administrator (RW-REFADM)** loading, I want **cases by route, age and queue, realized recovery, time in stage and turnaround per route published as the baseline, with each definition agreed by the Tribe, held as a versioned data row and computed from the Workbench records read on the contracts of the services that own them**, so that **every later epic is measured against the same frozen baseline and no team counts a case its own way**.

This story is the largest of the four slices of RWB-E1-013. It owns:

- six of the eight legacy acceptance criteria, copied word for word with their origin tag (AC1, AC3, AC4, AC5, AC7, AC8), and the rules, messages and screens they depend on;
- `measure_definition`, `measure_snapshot` and `measure_publish` in schema `rwb_reporting`, with the frozen-row protection and the per-service Flyway migration (DP-01, DP-15);
- one calculator per measure code, each reading facts only on the rwb-case case-facts read and the rwb-source-data payments read, one hop with a 2 s budget (DP-05, DP-11);
- the version of the definition in force on a business date, resolved through the reference-data framework of rwb-case at its version (DP-07);
- the 01:30 run of JOB-15 as a Temporal Schedule on `rwb-reporting` in namespace `rwb-recovery`, replacing the Quartz trigger (DP-10), with its decision record written before the snapshot changes (DP-03);
- the baseline flag and the frozen flag of business date 2026-11-27, the publish state of a business date, and the freshness stamp the reporting read model carries;
- `GET /reports/measures` and the definitions read on base `/api/recovery/reporting/v1`, and the baseline state of SCR-44 behind the gateway-bff composite route (DP-13, DP-19).

It does not own: the case facts of a business date and their age banding, which are RWB-P3-E1013-APP's; the payments since entry, the daily completeness gate and the freshness stamp of a data product, which are RWB-P1-E1013-APP's; AC2 and AC6, which are proved end to end by RWB-ITG-E1013-ITG; the published shapes, the three tables' columns, the closed lists, the consumed rows and the fakes, which are RWB-P9-E1013-CON's; the steering dashboard SCR-37, its data set and the agent measures, which are RWB-P9-E2009-APP's; the data lake and the INT-19 extract, which Arch v5 removes (DP-17); and the deployment, the Schedule registration, the panels and the alerts, which are RWB-P9-E1013-OPS's.

### 2. Business rationale

Measures are counted by hand from spreadsheets at month end today, and each team counts a case differently. Legacy RWB-E1-013 answered this inside one module: the definitions, the case and payment facts, the snapshot, the frozen baseline and the nightly lake extract sat together. Arch v5 splits the same capability along the lines of who owns the facts, so the legacy story becomes four slices: the case facts (P3), the payments and the gate (P1), this service, and the cross-service proof (ITG).

What D-RCV-60 changes here, and why each change is safe:

1. **The measure is data, not code.** Legacy BR1 already said a measure is published only under a definition in force that names its data product, formula, unit and approver. `measure_definition` holds that row with its version and its valid-from date, the six calculators are driven by the row, and no measure code, formula, unit or band is written in Java (REQ-RDF-012; Principle 1; legacy BR7 for the all-or-nothing load).
2. **The facts stay with their owners.** `recovery_case` is P3's and `v_ace_payment` is reached only through rwb-source-data (Architecture v5 slides 29, 37 and 45; DP-01, DP-05). This service reads them on the two published contracts and holds no grant on `rwb_case`, no `v_ace_*` grant and no ACE table.
3. **The clock becomes a Schedule.** The Quartz row of JOB-15 becomes a Temporal Schedule on `rwb-reporting`, started once per business date at 01:30 Asia/Bangkok (DP-10; ADR-016).
4. **The run is a recorded decision.** The version of the definition in force, the row count and the business date are recorded through the local decision record before the snapshot changes, so a published number can always be explained (DP-03; ADR-022). NFR-065 asks for measures from Workbench records and the decision log, and this record is the reporting half of it.
5. **The lake is gone.** Arch v5 removes the data lake, INT-19 and INT-20, and rwb-reporting builds its read model in its own schema (DP-17; ADR-018). The publish, the freshness stamp and the hold survive inside `rwb_reporting`; the extract file, its trailer and the lake client do not.

Three consequences are recorded rather than smoothed over. AC3 and AC7 name the lake, the extract file, its trailer and the lake-unavailable hold, and they are owned here, so the story keeps their text word for word and implements the equivalent publish and hold inside its own schema (GAP-2566; ASM-4232). Power BI has no lake to read in the target, and no source says how the 07:30 refresh reaches the snapshot (GAP-2570; ASM-4236). The two rows this service consumes from rwb-source-data — the payments since entry and the daily completeness gate — are class C dependencies in fact but sit in no plan row (GAP-2567; ASM-4233).

### 3. Preconditions

- RWB-P9-E1013-CON is published with its fakes: the two read operations, the three tables' columns of DF-RPT-031 to DF-RPT-058, the six closed lists, the consumed rows, the decision-record element, the rights and the error envelope. Its shapes are fixed on Day 1 and this story builds no surface of its own.
- RWB-P3-E1013-APP answers the facts of a business date on `GET /api/recovery/case/v1/cases/facts` with the as-of time, the row count and the reference version, with its fake, so the six calculators can be built before rwb-case is live.
- RWB-P3-E1018-CON is published with its fake: the case record read and the account link of a case, which is what the payments read of RWB-P1-E1013-APP is called with.
- RWB-P1-E1013-APP answers `GET /api/recovery/source-data/v1/payments?accountId={accountId}` and `GET /api/recovery/source-data/v1/data-products/freshness?asOf={date}`, with their fakes. Neither row is in this story's contract-dependency metadata, which carries the two P3 rows only (GAP-2567; ASM-4233).
- RWB-P3-E1043-CON is published with its fake: the reference list read of `measure-unit`, `measure-dimension`, `measure-publish`, `product` and `data-product`, each at its version in force. The list codes are those of TSD P9 T3.2 and the read is the reference-data contract of rwb-case (DP-07).
- RWB-PLT-E1027-CON (DP-03), RWB-PLT-E1043-CON (DP-07), RWB-PLT-E1071-CON (DP-10), RWB-PLT-E1044-CON (DP-15) and RWB-PLT-N001-CON (DP-19) are published as platform baselines, so no build item here invents a decision-record, reference-data, workflow, migration or route mechanism.
- Schema `rwb_reporting` exists with its own login and the per-service Flyway sequence, and `measure_definition`, `measure_snapshot` and `measure_publish` are created by this story's migration `V1013__measures.sql` because no DB story sits in this key's story set (DP-15; GAP-2575; ASM-4241).
- The definition file of six rows is prepared with the Tribe lead's approval on each row, and `rwb.reporting.baseline-date` is set to 2026-11-27. The approver reference is "TRB-0001" in the legacy file while TSD P9 T3.1 types `approved_by` as `uuid` (GAP-2571; ASM-4237).
- The ACE business date 2026-11-27 is complete: rwb-source-data answers COMPLETE for the date and holds a COMPLETED ALS row behind it, and case creation has run for the date. This story reads that answer and calls no ACE view.
- No approval is needed to build against a Draft contract baseline or an In-review FSD; the contract is tagged by RWB-P9-E1013-CON when its tests pass (ASM-4242).

### 4. Flow

1. RW-REFADM loads the definition file through the reference-load operation of this service for table `measure_definition`, with the approver, the approval date and valid-from 2026-11-21. The operation's path is not specified in the source documents and is declared by RWB-P9-E1013-CON (GAP-2568; ASM-4234).
2. `MeasureDefinitionLoadHandler` checks every row for a measure code, a name, a formula, a data product, a unit, an approver and an approval date against the closed lists of the contract; one invalid row refuses the whole load and no version is put in force (legacy BR7; AC1, AC4).
3. The version in force for a business date is the row set whose `valid_from` is the latest one on or before that date; `MeasureCatalogService` answers it for the date, with each measure's data product and formula, on the definitions read of the contract (AC1).
4. At 01:30 Asia/Bangkok the Temporal Schedule opens the run of JOB-15 for the previous business date on queue `rwb-reporting` (DP-10; legacy §12 trigger).
5. `FreshnessGateClient` asks rwb-source-data for the gate answer of the business date. HOLD leaves the run in its waiting state, writes no baseline row and names the product and its date with MSG-P1-001 (legacy BR4; AC6 proves this end to end in the ITG story).
6. `CaseFactClient` reads the facts of the business date on the rwb-case contract: one row per case with product group, route, stage, queue, entry date, stage clock start, closed date and status, paged, with the as-of time and the reference version. No case table is read (DP-01, DP-11).
7. `PaymentClient` reads the payments since entry of each account of those cases on the rwb-source-data contract, one hop for an account. The account link comes from the case record read of RWB-P3-E1018-CON.
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
| X1 | A definition row has no formula or no data product | Load refused in full; no version in force | MSG-GEN-001 | AC4, TC-E1-013-04 |
| X2 | The baseline is published a second time | Refused; frozen values unchanged | MSG-P9-001 | AC5, TC-E1-013-05 |
| X3 | The gate answer for the baseline date is HOLD | No baseline row is written; the run waits and names the product and its date | MSG-P1-001 | AC6 (ITG), X7 |
| X4 | The publish cannot complete | The `measure_publish` row is `HELD` with its reason; an alert goes to the operations channel and the next run publishes it | MSG-GEN-006 | AC7, TC-E1-013-07 |
| X5 | A measure has no definition in force | No value is written; the run record names the measure | MSG-P9-003 | AC8, TC-E1-013-08 |
| X6 | The decision record cannot be written | The transaction writes nothing: no snapshot row, no publish state and no baseline flag | MSG-P7-003 | BR3, TC-E1-013-05 |
| X7 | The rwb-case or rwb-source-data read does not answer inside 2 s, or its breaker is open | The run waits and retries on the workflow's own schedule; nothing is written and no partial snapshot is published | None (503 on a read) | §12.2, TC-E1-013-02 |
| X8 | A statement or a test reaches `recovery_case`, a `v_ace_*` view or another service's schema | The grant refuses the statement and the boundary test fails the build | None (pipeline log) | §17, BR5 |
| X9 | A measure code, formula, unit or band value appears in Java | The guardrail test fails the build | None | §17, BR1 |
| X10 | A frozen row is updated or deleted, by the service, a script or a person | The trigger refuses the statement and the transaction rolls back | None (database error) | BR6, TC-E1-013-05 |

X1 to X5 are the five exception paths of the legacy story carried onto the split, X6 and X7 are the record and the call types the target adds, X8 and X9 are the boundaries of DP-01 and DP-17, and X10 is the protection legacy BR2 asked the database for. The data lake of legacy X4 has no target system, so X4 is the publish state of the read model (GAP-2566; ASM-4232).

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
```

The six criteria are the legacy criteria of RWB-E1-013 word for word, with their origin tag added and nothing else changed: the repeated `Then`, the legacy wording of `it is loaded`, `the data lake load area does not answer` and `the extract configuration` all stand. The added `Given the <service> contract mock returns <x>` lines are the only additions, and they keep every value of the legacy text. **AC2 and AC6 are not here**: they name the frozen baseline values and the completeness gate across services and are proved end to end by RWB-ITG-E1013-ITG, with the case facts in RWB-P3-E1013-APP and the payments and the gate in RWB-P1-E1013-APP. Two points are recorded rather than smoothed over. AC3 and AC7 assert a data lake, an INT-19 extract, its trailer and a lake hold, and Arch v5 removes the lake (DP-17): this story keeps the legacy text as the record of intent, and the deliverable it proves is the publish state of business date 2026-12-01, the freshness stamp of the read model and the hold of the same date with its alert and its next-run resend, all inside `rwb_reporting` (GAP-2566; ASM-4232). `MeasureCatalog` in AC1 is the definitions read of §12.1, because the monolith's Java interface no longer exists; the legacy path of the definition load is `POST /admin/reference-loads`, and the target path of the same operation is declared by RWB-P9-E1013-CON (GAP-2568; ASM-4234).

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

BR1 to BR7 are the legacy rules copied character for character. BR5 names a data lake that Arch v5 removes, so the rule is applied as BR8: the publish and the hold survive as a row of `measure_publish` and the freshness stamp of the read model, and the lake destination, the trailer count and the INT-19 adapter are gone (GAP-2566; ASM-4232). BR6 is executed where the band is assigned: the case-fact read of RWB-P3-E1013-APP carries the band code of the version in force, and this service counts it and never bands a case itself.

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
| JOB-15 run | waiting | The gate answers HOLD | held, with MSG-P1-001 naming the product and its date (X3) |

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

The rights are the rows of TSD P9 T6.1; RW-TRIBE holds Reporting R and RW-BIANAL Reporting CRUD there, and no role outside the rows is given a right by this story. DP-08 is not in this key's pattern set: the capability area and the right are declared per operation and the check is the service template's cached permission decision, so this story states the rights and builds no guard of its own.

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

Field IDs are those of the Logical Data Model and Data Dictionary, TSD P9 T3.1 and T3.2 and the legacy Data table. The three tables arrive with this story's migration `V1013__measures.sql` in the per-service Flyway sequence (DP-15; GAP-2575; ASM-4241); the decision record and the idempotency key are platform library objects created in `rwb_reporting` by the library's own migration (DP-03). **No personal data:** the rows carry measure codes, dimension codes and values, business dates, counts, amounts, list values and a definition version, and no name, address, contact value, identity number or account number is copied into this schema.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-reporting (P9); base `/api/recovery/reporting/v1` (DP-13). The shapes and the errors are declared by RWB-P9-E1013-CON.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| GET | `/reports/measures` | Measure[] for the period of the query `measure`, `product`, `route`, `from`, `to`; each element carries the measure code, the definition version, the business date, the product group, the dimension code and value, the value or the case count and the freshness stamp of the read model (API-P9-001) | Reporting, right R, scope applied | Not applicable |
| GET | `/measure-definitions` | The definitions in force on `onDate`, each with its measure code, name, data product, formula, unit and version; the read RWB-P3-E1013-APP consumes | Reporting, right R, scope applied | Not applicable |

The two operations answer 401, 403 with MSG-P4-002, 422 for a period or a date that cannot be read, and 503 when the store does not answer. The operation ID API-P9-001 is that of TSD P9 T-A.1 and the path is the target base, not the monolith form. The definitions read is the legacy `MeasureCatalog` interface turned into a contract, because RWB-P3-E1013-APP consumes it across a service boundary (DP-11); no source document gives its path or its shape, so the path above is declared here and the gap is recorded (GAP-2572; ASM-4238). The legacy story assigns `GET /reports/measures` to RWB-E2-009, while the Ownership Map gives the operation to P9 and the wave 1 harness calls it, so the shape is declared here and the dashboard's use of it, its filters and SCR-37 stay RWB-P9-E2009-APP's (GAP-2570; ASM-4236).

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| GET | `/api/recovery/case/v1/cases/facts` | P3 rwb-case | The facts of one business date: one row per case, paged, with the as-of time, the row count and the reference version (RWB-P3-E1013-APP); faked |
| GET | `/api/recovery/case/v1/cases/{caseId}` family | P3 rwb-case | The case record and its account link, which is what the payments read is called with (RWB-P3-E1018-CON); faked |
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case | The five closed lists at their version in force (RWB-P3-E1043-CON, the plan's C row); faked |
| GET | `/api/recovery/source-data/v1/data-products/freshness?asOf={date}` | P1 rwb-source-data | The gate answer of the business date: COMPLETE or HOLD, with each product, its date and its status (RWB-P1-E1013-APP); faked |
| GET | `/api/recovery/source-data/v1/payments?accountId={accountId}` | P1 rwb-source-data | The payments since entry of an account, one hop per account (RWB-P1-E1013-APP); faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The last two rows are class C dependencies of this story that the plan's C row does not carry, and the absence is recorded (GAP-2567; ASM-4233). The rwb-decision row of the legacy contract is not consumed: the local decision record is this service's and the central ledger behind it is the library's.

#### 12.3 Events published

None. The context pack and the Ownership Map give rwb-reporting the topic `rwb.reporting.events.v1` with its retry and `.dlt` topics by the naming rule (DP-14) and **no event row**; this story therefore declares no event, no producer group and no outbox row, and a build that adds one fails the absence test of the contract baseline. RWB-ITG-E1013-ITG names `rwb.reporting.ReportPublished.v1` on that topic as the freshness signal of its journey, which no owner document gives this service, so the two statements are recorded as a conflict rather than resolved quietly: the event belongs to whoever publishes it and is not declared here (GAP-2569; ASM-4235). The decision record of a run travels on the platform's `rwb.decision-record.v1` through the library, and that is not an event of this service.

#### 12.4 Events consumed

None. This story subscribes to nothing: the run is started by its Schedule and the facts are read on the two contracts. A run that needs a later source arrives on the next Schedule tick, and the ITG story waits on the reads rather than on an event. A build that declares a consumer group, a subscription or an inbox row of its own fails the absence test.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `MeasureRunWorkflow` | Workflow, one execution per business date | `rwb-reporting` in namespace `rwb-recovery` | Input: the business date, the baseline date, the definition version in force and the gate answer; output: the row count, the publish state and the outcome. No child workflow and no signal from another service |
| `measureRun` | Activity, the step that reads, computes, freezes and publishes | `rwb-reporting` | The facts, the payments and the gate answer in; the snapshot rows, the record, the publish state and the run outcome out, in one transaction per business date |
| `listEligibleAccounts`, `snapshot(page)` | Activities registered by RWB-P1-E1013-APP on `rwb-source-data` | `rwb-source-data` | Declared as the measures consumer's activities in that story; this flow reaches the payments and the facts on the two REST reads of 12.2 and calls neither on its happy path |

The two activity names of this service are target design choices and are fixed by no source; the remote pair is named so that a reader sees where the P1 hooks sit and that this story does not call them (GAP-2567; ASM-4233).

#### 12.6 Schedules

One Temporal Schedule, on `rwb-reporting` in namespace `rwb-recovery`: the run of JOB-15 for the previous business date at 01:30 Asia/Bangkok, one run per business date, with a catch-up policy of one missed run and no overlapping execution. It replaces the Quartz row of the legacy job (DP-10). Its Temporal Schedule ID is a target choice and is not given by any source; the legacy job ID JOB-15 is kept in the run record and on SCR-44. The bank's Airflow chain that "triggers report extracts in rwb-reporting" (Architecture v5 slide 9) is not wired to this run, and the one trigger that exists is the Schedule (GAP-2573; ASM-4239).

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
| rwb-source-data payments and freshness fake | The payments since entry of an account for 2026-11-30 and 2026-12-01, the gate answer COMPLETE and HOLD, a stale product with its date, no answer beyond 2 s | AC3, AC7, X3, X7 |
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

Read one by one: DP-01 is the three tables and the refusal to join `rwb_case`; DP-03 is the run record written before the snapshot commits; DP-05 is a boundary, since the payments and the gate arrive on the P1 contract and no `v_ace_*` view is read; DP-07 is live for the five closed lists, read at their version; DP-10 replaces the Quartz row of JOB-15 with the 01:30 Schedule; DP-11 turns the two in-process interfaces of the legacy §12 into contracts with fakes; DP-13 moves the two reads to the service base; DP-15 carries the migration; DP-17 removes the lake, its extract, its trailer and its hold, and the publish and the hold move into `measure_publish`; DP-19 is how SCR-44 shows the run. The six H rows are exactly the plan's, and the two rwb-source-data consumed rows are C in fact and absent from the plan's C row (GAP-2567; ASM-4233).

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
| `MeasureRun` | React component | The run and its state on SCR-44, read only |

**Database and migrations.** One file in the per-service sequence, `V1013__measures.sql`: the three tables, their unique keys (`measure_code`, `definition_version` on the definition; `measure_code`, `definition_version`, `business_date`, `product_group`, `dimension_code`, `dimension_value` on the snapshot; `business_date` on the publish), and the trigger that refuses an UPDATE or a DELETE of a frozen snapshot row. No column is added for a case fact, a band, an account or a payment: those are the owners' and are read, not copied (DP-01).

**Configuration and reference data.** The baseline business date `rwb.reporting.baseline-date` = 2026-11-27; the six definitions at version MD-2026.11 loaded as rows; the five closed lists read from rwb-case at their version; the 01:30 time of the Schedule, the 2 s budget and the one-hop rule as platform values; feature flag `rwb.reporting.baseline`.

**Build steps**

1. The migration with the frozen trigger; test that an update of a frozen row fails (X10, BR9).
2. `MeasureDefinitionLoadHandler` and `MeasureCatalogService` with the six-row file and the invalid row; tests for AC1 and AC4.
3. `CaseFactClient` and the case-record read against their fakes, with the no-answer and the out-of-time paths (X7).
4. `PaymentClient` and `FreshnessGateClient` against their fakes, with the HOLD and the stale product (X3, X7).
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
| MSG-GEN-006 | The publish cannot complete and is held (X4) | {system} is not available. Your request is queued and will be retried. |
| MSG-P9-003 | A measure has no definition in force (X5) | {measure} has no approved definition. It is not published. |
| MSG-P7-003 | The decision record cannot be written before the snapshot changes (X6) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | A role holds no right on a read or on the definition load | You cannot {action} here. Your role does not include it. |

The five legacy message IDs and the text are copied unchanged from the legacy section 14 and FSD P9 A2.1.3.1; MSG-P7-003 and MSG-P4-002 are the platform messages of DP-03 and of the guard, and no message is reworded and none is added. MSG-GEN-006 names a system that in the target is the reporting read model's publish step and not a data lake, and the text of the legacy message stands as it is (GAP-2566; ASM-4232).

### 15. Screens and states

No new screen. SCR-44 Interface and job monitor shows the JOB-15 run in its running, held, failed and complete states through the gateway-bff composite route (DP-19), and the run record, the publish state and the freshness stamp are its field list's. The Tribe lead and the Reporting and BI analyst read the baseline in the report built from the snapshot, and SCR-37 Steering dashboard with its data set is RWB-P9-E2009-APP's. The refusal, held and not-recorded states read the messages of section 14.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-013-01 | AC1, BR1 | Component | Definition file of 6 rows approved by TRB-0001; the version in force and the catalog answer |
| TC-E1-013-03 | AC3, BR5 | Component | JOB-15 on 2026-12-02 for business date 2026-12-01; the publish state, the freshness stamp and the run record |
| TC-E1-013-04 | AC4, BR7 | Component | TIME_IN_STAGE with no formula; the load refused in full and no version in force |
| TC-E1-013-05 | AC5, BR2 | Component | JOB-15 rerun for 2026-11-27; the frozen rows unchanged and MSG-P9-001 |
| TC-E1-013-07 | AC7, BR8 | Component | The publish held with its reason and the alert; the next run publishing it |
| TC-E1-013-08 | AC8, BR1 | Component | COST_PER_CASE with no definition; no value written and MSG-P9-003 |
| TC-E1-013-09 | Access | Component | RW-BIANAL calls the definition load; refused with MSG-P4-002 and no row written |

The seven cases are the legacy cases of RWB-E1-013 for the criteria this story owns, in their legacy order, with the Level column added: the legacy level System maps to `Component` because each runs on the contract fakes, and Access maps to `Component` for the same reason. **TC-E1-013-02 and TC-E1-013-06 are not here**: AC2 and AC6 cross rwb-case, rwb-source-data and rwb-reporting and are proved by RWB-ITG-E1013-ITG as `TC-E1-013-02-ITG` and `TC-E1-013-06-ITG`. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID; no `-ITG` copy of a case is written by this story.

### 17. Guardrails

- No business value in code: the six measure codes, their formulas, the four unit values, the age bands, the product groups and the baseline date are definition rows, reference rows or configuration, never a constant, a default or a branch of the build.
- No personal data in `rwb_reporting`, a workflow input, a log or a test: measure codes, dimension codes, dates, counts, amounts and a definition version only, and every fixture is synthetic.
- ACE data only through the owner's contract: this service holds no `v_ace_*` grant and reads no ACE table, and a build that adds one fails the boundary test (BR12).
- The case stays with rwb-case: no `recovery_case` row, no case status and no band assignment is made here; the band arrives on the fact (BR3, BR6).
- Frozen rows are protected by the trigger as well as by the service, and a build that writes around the trigger fails the review (BR9).
- One base, one topic, one queue, one schema and one login per service; no document or test names another service's base or topic as its own (DP-13, DP-14).
- No retired element is reintroduced: no data lake, no INT-19 extract, no trailer, no Quartz row, no shared job table and no event published by this story (DP-17, §12.3).
- The record is written before the snapshot commits; a build that publishes a measure without its decision record fails the review (DP-03).

### 18. Traceability

| Requirement ID | Requirement (short) | Story element | Test cases |
|---|---|---|---|
| REQ-RDF-012 | Baseline measures published with definitions agreed by the Tribe (BRD Epic 1, sections 3.8 and 4; FEAT-RDF-19, FEAT-RPT-01) | The definition load, the catalog, the six calculators, the snapshot, the frozen baseline and the publish state | TC-E1-013-01, TC-E1-013-03, TC-E1-013-04, TC-E1-013-05, TC-E1-013-07, TC-E1-013-08 |
| NFR-065 | Business measures come from the Workbench records and the decision log, not a separate count | The two contract reads and the run record | TC-E1-013-03, TC-E1-013-05 |
| NFR-067 | Every scheduled job has a run book, monitoring and an alert | The run record and the publish alert this story writes; the panels and the run book are RWB-P9-E1013-OPS's | TC-E1-013-03, TC-E1-013-07 |
| ADR-014 | Schema and login per service | `rwb_reporting` and its own login | TC-E1-013-01 |
| ADR-018 | No data lake; rwb-reporting read model from events and records | The `measure_publish` state and the freshness stamp, and the removed extract | TC-E1-013-03, TC-E1-013-07 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The five consumed rows with their budget and breaker | TC-E1-013-03 |
| ADR-022 | Local decision record plus central ledger | The run record written before the snapshot | TC-E1-013-05 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E1-013, disposition Split (rework); features FEAT-RDF-19 and FEAT-RPT-01 |
| Legacy criteria | AC1, AC3, AC4, AC5, AC7 and AC8 owned word for word by this story; AC2 and AC6 owned end to end by RWB-ITG-E1013-ITG |
| Source text | The legacy story, FSD P9 Reporting v3 A2.1, A2.8 and T3.2 of the TSD, and TSD P9 Reporting v2 T3.1, T3.2 and T-A |
| Test cases | TC-E1-013-01, -03, -04, -05, -07, -08 and -09; the -ITG copies of -02 and -06 sit in RWB-ITG-E1013-ITG |
| Feature and screens | FEAT-RDF-19, FEAT-RPT-01; SCR-44 (SCR-37 is E2) |
| Decoupling patterns | DP01, DP03, DP05, DP07, DP10, DP11, DP13, DP15, DP17, DP19 |
| Architecture decisions | ADR-014, ADR-018, ADR-020, ADR-022, and ADR-016 for the Schedule |

### 19. Out of scope

- The published shapes, the three tables' columns, the six closed lists, the consumed rows, the decision-record element, the rights, the error envelope and the fakes: RWB-P9-E1013-CON.
- The case facts of a business date and their age banding: RWB-P3-E1013-APP.
- The payments since entry, the daily completeness gate and the freshness stamp of a data product: RWB-P1-E1013-APP.
- The cross-service proof of AC2 and AC6 and the `-ITG` copies of these test cases: RWB-ITG-E1013-ITG.
- The steering dashboard SCR-37, its data set, the queue and ageing measures for team managers (FEAT-RPT-02) and benefit realisation tracking against the baseline (FEAT-RPT-06, Epic 6): RWB-P9-E2009-APP and later epics, outside this service's wave 1 slice.
- The data lake, INT-19 and INT-20, the extract file, its trailer and the lake hold: removed by Arch v5 and DP-17, and no story rebuilds them.
- The reference list of rwb-case, its load, its approval and its rollback: RWB-P3-E1043-APP.
- The Schedule registration, the chart, the migration job, the panels, the alerts and the run books: RWB-P9-E1013-OPS.
- The decision log copy to the data lake (RWB-E1-014): retired, with no new story.
