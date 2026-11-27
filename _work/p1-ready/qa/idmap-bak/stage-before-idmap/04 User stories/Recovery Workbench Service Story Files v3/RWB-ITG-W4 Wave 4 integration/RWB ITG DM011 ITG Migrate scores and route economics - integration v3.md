# RWB-ITG-DM011-ITG Migrate scores and route economics

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Version 3 changes**

- JOB-04 is started by the readiness call as a child of `AceIngestCheck`; the invalid rerun call is removed (RD-P1-012, RD-P1-040; findings #1, #12).
- `case_list_row` is removed: the case list is read from rwb-case and account data through the P1 account-page read, path pending (RD-P1-024; NEW-GAP-B3; #4).
- Route code and route state are read from rwb-case; the valuation operation did not exist (RD-P1-027; #3); migrated rows carry `migration_source` and `migrated_at`.
- The key listing on the real services is pending (GAP-1508, NEW-GAP-S2B-03; #2).
- Freshness, readiness, rights, messages and contract version aligned to rwb-source-data.yaml 5.1.0; AC8 added (#5 to #8, #11).
- Finishing pass: test case IDs of Test Cases v9 cited in place of the placeholders.
- A repeated readiness call answers 202 and starts nothing once every due source is stamped and the run has ended (RD-P1-065, register XD-11).
- The reconciliation result reads are cited as published in rwb-source-data.yaml 5.1.0 (`getAdminReconciliationResults`, RD-P1-063).

| Item | Value |
|---|---|
| Story key | RWB-ITG-DM011-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W4 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-DM-011 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP05, DP15, DP19 |
| Parallel lane | L-ITG-W4 |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-ITG-DM011-ITG-16); the squad sizes it at refinement |
| Depends on (build) | RWB-P1-DM011-APP (not done; the harness runs on its contract fake until it lands) |
| Contract dependencies | RWB-P1-E1015-CON (readiness, freshness and the account-page read), RWB-P1-E1011-CON (reconciliation result reads), RWB-P1-E1016-CON (data product records); the CON stories of rwb-case, rwb-reporting and rwb-access: Not specified in the source documents |
| Contract version built against | rwb-source-data.yaml 5.1.0 (API Specification v7); rwb-case, rwb-reporting and rwb-access 5.1.0 |
| Contract fake library version | rwb-source-data: `fakes/rwb-source-data/5.1.0/` (RD-P1-011), not yet recorded as published; other services: Not specified in the source documents (DOR-RWB-ITG-DM011-ITG-22) |
| Integration dependencies | RWB-P1-DM011-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |
| Readiness decisions | RD-P1-001, RD-P1-004, RD-P1-005, RD-P1-011, RD-P1-012, RD-P1-022, RD-P1-024, RD-P1-027, RD-P1-040, RD-P1-041, RD-P1-042, RD-P1-065, RD-P1-063 |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-DM-011 for the wave 4 cutover reconciliation harness. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-ITG-DM011-ITG). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (19 resolved, 8 cross-document, 3 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3; cutover reconciliation harness aligned to the readiness chain, the removal of the P1 case list, the migration field mapping and the published reads.

### 1. Story

As a **RW-DATASTEW, data steward**, I want **a repeatable wave 4 cutover reconciliation harness that proves the route each open case carries and the route economics baseline survive cutover, that each measure snapshot keeps its dimension, its value and its baseline flag, and that no COLLINS score is copied because the score, its estimate and its route are read from ACE, against the owning services' published contracts and their fakes**, so that **the baseline and the route history survive cutover while every business key on a migrated record is proven against its ACE view row and every orphan is on a list with a reason and two owners**.

This story builds the harness and the evidence, and nothing else. The real records are extracted by RWB-P1-DM011-APP as files, the route facts loaded by rwb-case and the baseline snapshots by rwb-reporting on their own Flyway sequences (DP-15; RD-P1-027); P1 loads no row and holds no `case_list_row` (RD-P1-024). The reconciliation is JOB-04 of RWB-P1-E1011-APP (RD-P1-022). This harness depends on it only as an I dependency and its stub answers until it lands. The story builds no production endpoint, no table, no workflow, no schedule and no screen; it reads the owning services' published contracts, asserts what they answer, and writes a report per business date.

### 2. Business rationale

The route a case carries and the route economics baseline behind it are what the bank uses to argue, months later, that a case was worked on the path the policy required and at the return the models expected. If the route code, the route state or the baseline flag of a snapshot is lost in cutover, the case opens on the wrong path, the return on the route cannot be defended to the committee, and the measure that steering reads for the day is a number with no baseline behind it. The failure is quiet as well: a cutover load that runs clean and reconciles to nothing still looks like a successful cutover until an officer tries to work the case, and a score that was copied instead of read starts to disagree with ACE on the first COLLINS model refresh.

The same story carries the opposite risk. A COLLINS score that is copied into the Workbench at cutover becomes a second source of truth for a model output the bank does not own, and it goes stale without anybody noticing; so the score, its estimate and its route stay where ACE holds them and are read through rwb-source-data's contract every time (DP-05), and the harness asserts that nothing of the three is stored on a migrated record.

The harness is decoupled the way the services are. ACE data is read only through rwb-source-data's data-product contract (DP-05), never from another service's schema and never by a direct view read (DP-01); the route code and route state of the case are read from rwb-case, which loads and holds them (RD-P1-027); the measures and their snapshots are read from rwb-reporting, which owns measures and snapshots; the case is read from rwb-case, which owns the case; each owner's cutover load runs on its own Flyway sequence (DP-15); the legacy story names the SCR-45 Data quality console, which this harness neither builds nor calls, and where a screen would compose these reads the path is the gateway-bff composite route (DP-19); every call is one hop on `/api/recovery/<short>/v1` with a 2 s budget (DP-11). It carries DL25 and the zero-tolerance rule on the migrated data into evidence rather than restating them.

### 3. Preconditions

- The published contracts of P9 rwb-reporting (the measures read), P3 rwb-case (the case read with its route code and route state, and the case list), P1 rwb-source-data (rwb-source-data.yaml 5.1.0: DP01 and DP11 records, freshness, readiness call and status, reconciliation result reads, account-page read) and P4 rwb-access (authorise) are in the contract registry, and a stub set is generated from each one.
- The data product catalog holds DP01 Account and arrears and DP11 Scores and route economics, each with one system of record, so account_key and the score row have one named owner before a key is resolved (FSD P1 v3, A2.2 and line 293).
- The reconciliation result reads are published (`getAdminReconciliationResults`, RD-P1-063). Pending: the path and maximum keys per call of the P1 account-page read, owner solution architect (NEW-GAP-B3).
- The harness caller of the readiness call holds Platform administration U; the caller of the record and freshness reads holds Case record R, and of the readiness status and reconciliation result reads Platform administration R. A key field that the record read returns with `masked` true fails the run and is reported.
- The rwb-case and rwb-reporting cutover loads, each on its own Flyway sequence (DP-15), have run in SIT for the business date under test, or the stub of §12.8 answers in its place on Day 1.
- RWB-P1-DM011-APP owns the extract and the clean-day count and JOB-04 of RWB-P1-E1011-APP owns the reconciliation (RD-P1-022); until they land, the cutover extract fixture and the reconciliation extract fixture stand in for its output.
- The harness environment and its base hosts, the synthetic cutover extract fixture and its field layout, the break-list fields, the extract format and its retention, the pass or fail gate and the seeding set: Not specified in the source documents (GAP-0451; ASM-0643).
- The synthetic case, the synthetic keys, the synthetic route code and route state, the measure snapshot and the business date are held in the fixture as data, not written in code.
- No build dependency. Day 1, with the stubs in place from the first run; the one wait is RWB-P1-DM011-APP, which replaces its stub and never blocks the lane.

### 4. Flow

1. Harness: loads the cutover extract fixture for business date 2026-12-31: open case RW-2026-001101 with route code RT-SYN-011 and route state RS-SYN-001, the account key ACC-SYN-001101 and the person key PERS-SYN-001101, the case on the case list of rwb-case, and one measure snapshot with measure_code MSR-SYN-011, definition_version 1, product_group PG-SYN-A, dimension_code DIM-SYN-A and its baseline flag. On Day 1, before the cutover load is in SIT, the stub of §12.8 returns the same records.
2. Harness: starts the chain for business date 2026-12-31 with `POST /api/recovery/source-data/v1/business-days/{date}/ready` and a UUID `Idempotency-Key` (202), and waits until `AceIngestCheck` has stamped the ALS batch and its child `ReconciliationWorkflow` (`recon-2026-12-31`, JOB-04) has completed, after rwb-case answers its allocation or at 07:15 (RD-P1-040). The harness never reruns JOB-04: `POST /admin/jobs/{jobId}/rerun` takes the run uuid of a FAILED run only (RD-P1-012).
3. Harness: reads the case through `GET /api/recovery/case/v1/cases/{caseId}` and asserts the case number and that it is open, and reads the case list through `GET /api/recovery/case/v1/cases` (RD-P1-024).
4. Harness: asserts on the case read the route code RT-SYN-011 and route state RS-SYN-001, unchanged from the fixture, with `migration_source` and `migrated_at`.
5. Harness: reads the snapshots through `GET /api/recovery/reporting/v1/reports/measures` for business date 2026-12-31 and asserts measure_code MSR-SYN-011, definition_version 1, product_group PG-SYN-A, dimension_code DIM-SYN-A and the baseline flag on the snapshot.
6. Harness: resolves each key through `GET /api/recovery/source-data/v1/data-products/{productCode}/records?caseId={caseId}`: DP01 for account_key ACC-SYN-001101 and every other account of the case, and DP11 for the score row, with `GET /api/recovery/source-data/v1/data-products/freshness?product=DP01` for `status`, `businessDate` and `loadedAt`. The account data of the accounts on the case list is read through the P1 account-page read (RD-P1-024); its path is pending (NEW-GAP-B3).
7. Harness: asserts that no COLLINS score, estimate or route is stored on a migrated record, and that the score, its estimate and its route the report quotes are the values the same DP11 read returns on that hop.
8. Harness: reads the break list from the reconciliation extract fixture for the business date, with one row per orphan, its reason and its two owners, and reads the REC rows through `GET /api/recovery/source-data/v1/admin/reconciliation/results?from=2026-12-31&to=2026-12-31`; the legacy story states that the breaks are listed on the reconciliation extract and that there is no screen. P1 stores no key-level break row (RD-P1-022): on the real services the key listing is pending the break-detail store (GAP-1508, NEW-GAP-S2B-03).
9. Harness: repeats the readiness call for the same business date with a new UUID `Idempotency-Key`, asserts no second set of result rows and compares the break list and the counts of cases and measure snapshots with the first run. The repeated call answers 202 with the stored state and starts nothing; a second run of the date exists only through the rerun of a FAILED run (RD-P1-065 rule 3, register XD-11).
10. Harness: calls `POST /api/recovery/access/v1/authorise` as a synthetic caller with role RW-OFF and no Platform administration right, and asserts 403 with MSG-P4-002; then sends the readiness call as that caller and asserts 403 with `messageCode` MSG-P4-002, no reconciliation run started and no break row written.
11. Harness: writes one run report per business date, keyed by story and business date, naming the contract version of each hop, whether the hop was a stub or the owner, the counts, the break rows and the criteria of section 7.

### 5. Exception paths

| ID | Trigger | What the harness asserts | Message | ITG test case | Covered by |
|---|---|---|---|---|---|
| X1 | A stub answers a shape the published contract does not allow | The run fails at that hop and the report names the service, the operation and the contract version; no criterion is marked passed | None | TC-DM-011-01-ITG (ITG AC2) | AC2 |
| X2 | The cutover extract fixture lacks a required key or the route code on a migrated record | The run fails and the report names the case and the missing field; a record without a key or without a route code is never reported as reconciled | None | TC-DM-011-01-ITG (ITG AC2) | AC2 |
| X3 | A key has no view row and the extract does not list it | The run fails on AC1 and the report names the case, the key type and the key value, so a suppressed break is a failure and not a pass | None | TC-DM-011-02-ITG (ITG AC1, ITG AC3) | AC1, AC3 |
| X4 | A repeated run lists the same break twice | The run fails on AC4 and the report names the two rows and the business date | None | TC-DM-011-03-ITG (ITG AC4) | AC4 |
| X5 | The ALS batch is late (no ALS stamp, so JOB-04 is not started), or the product read answers `status` `STALE` | The readiness status reads `LATE`, or the freshness read answers `STALE` (`businessDate` null when never stamped); the run is reported as not run, never as passed | MSG-P1-001 | Test Cases v9: TC-DM-011-02-ITG, TC-DM-011-09-ITG | AC1, AC8 |
| X6 | A caller without the Platform administration right starts a run | The run fails on AC4 and the report names the caller role and the operation; a run that started is reported as started | MSG-P4-002 (expected, and missing) | TC-DM-011-04-ITG (ITG AC4) | AC4 |
| X7 | The counts the owner returns disagree with the extract | The run fails on AC4 and the report names each count and its two values | None | TC-DM-011-03-ITG (ITG AC4) | AC4 |
| X8 | A migrated record or the report holds a stored COLLINS score, estimate or route | The run fails on AC3 and the report names the record, the field and the DP11 read it should have used | None | TC-DM-011-01-ITG (ITG AC3) | AC3 |
| X9 | The measure snapshot loses its baseline flag, or the case loses its route code or route state | The run fails on AC2 and the report names the snapshot or the case, the field and the values it read on the two hops | None | TC-DM-011-01-ITG (ITG AC2) | AC2 |

The report text is for the wave entry check and is not part of the message standard. The business messages the run touches are in section 14 and are asserted by ID and by their substituted values.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Runs against the published contracts and the stubs from Day 1; the only wait is RWB-P1-DM011-APP, and its stub answers until it lands |
| Negotiable | The fixture layout, the break-list fields, the report shape and the gate are configuration agreed at the wave entry check, not business values in code |
| Valuable | The route, the route state and the baseline flag are proven to survive cutover, no COLLINS output is copied, and every orphan is on a list with a reason and two owners, before wave 4 opens |
| Estimable | One runner, one stub set, two fixtures, one key resolver, one no-copy assertion and one report |
| Small | Fits in one sprint with its four tests |
| Testable | Each criterion runs against the stubs and again against the real owner as the I story lands |

### 7. Acceptance criteria

```gherkin
Feature: Migrate scores and route economics - wave 4 cutover reconciliation harness

  Background:
    Given the synthetic cutover extract holds open case "RW-2026-001101" with route code "RT-SYN-011" and route state "RS-SYN-001"
    Given the case carries account_key "ACC-SYN-001101" and person_key "PERS-SYN-001101"
    Given the cutover extract holds one measure snapshot with measure_code "MSR-SYN-011", definition_version "1", product_group "PG-SYN-A" and dimension_code "DIM-SYN-A"
    Given the rwb-source-data contract fake answers one row for account_key "ACC-SYN-001101" and one score row under DP11
    Given ReconciliationWorkflow "recon-2026-12-31" (JOB-04) has completed for business date "2026-12-31" as the child of AceIngestCheck

  Scenario: AC1 Reconcile the business keys (legacy RWB-DM-011 AC2)
    Given the migrated records
    When the harness resolves the keys of the migrated records for business date "2026-12-31"
    Then every business key on a migrated record resolves to its view row, account_key and person_key included
    And each orphan is listed for the data steward and the ACE team in the run report
    And on the real services no key-level REC-05 row is read, because rwb-source-data stores none (GAP-1508, NEW-GAP-S2B-03)

  Scenario: AC2 The route and the baseline flag survive cutover (new, D-RCV-60)
    Given the migrated records for business date "2026-12-31"
    When the harness reads case "RW-2026-001101" from the rwb-case contract and the measure snapshots from the rwb-reporting contract
    Then the case keeps route code "RT-SYN-011" and route state "RS-SYN-001"
    And the snapshot for measure_code "MSR-SYN-011" keeps definition_version "1", business_date "2026-12-31", product_group "PG-SYN-A" and dimension_code "DIM-SYN-A"
    And the snapshot keeps its value and its baseline flag
    And the run report names the route code, the route state and the baseline flag it read, with the contract version of each hop

  Scenario: AC3 A key resolves in one hop, an orphan is listed with its reason, and no COLLINS value is copied (new, D-RCV-60)
    Given the rwb-case contract fake answers case "RW-2026-001101" on its case list with account_key "ACC-SYN-001177" for business date "2026-12-31"
    And the rwb-source-data contract fake answers no row for account_key "ACC-SYN-001177"
    When the harness resolves the key through the rwb-source-data data-product contract in one hop with a 2 s budget
    Then the break list of the reconciliation extract fixture holds one row for case "RW-2026-001101" with key type "ACCOUNT", key value "ACC-SYN-001177" and reason "NO_ACE_ROW"
    And the row names the owner role "RW-DATASTEW" and the ACE team as the second owner, and the run report names both
    And the score row under DP11 is read through the rwb-source-data data-product contract on that hop
    And no COLLINS score, its estimate and its route are stored on a migrated record or in the run report
    And on the real services the listing of this key is pending the break-detail store (GAP-1508, NEW-GAP-S2B-03)

  Scenario: AC4 A repeated run is deterministic and a caller without the right is refused (new, D-RCV-60)
    Given the reconciliation for business date "2026-12-31" has run once
    And a synthetic user with role "RW-OFF" and no Platform administration right
    When POST /business-days/2026-12-31/ready is called again with a new UUID Idempotency-Key and the synthetic user then calls it with another UUID Idempotency-Key
    Then the repeated call starts nothing: no second ReconciliationWorkflow run for "2026-12-31", because every due source of the date is stamped and the run has ended
    And the break list holds exactly one row for account_key "ACC-SYN-001177"
    And no second set of reconciliation result rows exists for 2026-12-31
    And the counts of cases and measure snapshots equal the first run
    And the run report holds one entry per business date and not one per run
    And the answer to the synthetic user is 403 with a problem body whose messageCode is "MSG-P4-002" and no run starts for that user

  Scenario: AC5 The harness owns no table and writes no row (new, D-RCV-60)
    Given the reconciliation for business date "2026-12-31" has run once
    When the harness completes the run for business date "2026-12-31"
    Then the harness creates no table and writes no row in any service schema
    And the run report names the contract version of each hop it read

  Scenario: AC6 Each business rule BR1 to BR7 is covered by a criterion and a test case (new, D-RCV-60)
    Given the business rules BR1 to BR7 in section 8
    When the wave entry check reads the rule coverage line and section 16
    Then each of BR1 to BR7 names at least one criterion in section 7 and one test case row in section 16

  Scenario: AC7 A consumed call that fails or does not answer stops the run at that hop (new, D-RCV-60)
    Given the rwb-source-data DP01 record read fake answers 503 with messageCode "MSG-GEN-006", or does not answer within 2 s, for business date 2026-12-31
    When the harness calls the consumed contract for that hop
    Then the run fails at that hop and the run report names the hop and the contract version of the hop
    And the unanswered call is never treated as an empty result

  Scenario: AC8 A late or never stamped batch is reported as not run (new, RD-P1-040, RD-P1-041)
    Given the readiness status fake answers status "LATE" for business date "2026-12-31"
    And the freshness fake answers DP01 with status "STALE" and businessDate null
    When the harness runs for business date "2026-12-31"
    Then the run report records "not run" with DP01, the business date and "MSG-P1-001"
    And no key is resolved, no break row is asserted and the run is not marked passed
```

Legacy AC1 and AC3 belong to RWB-P1-DM011-APP, and the eight criteria above are the ones this ITG story owns. At cutover P1 extracts the route facts and measure snapshots, loads no row of its own (the legacy case list rows are not migrated, RD-P1-024), hands the route facts to rwb-case and the baseline snapshots to rwb-reporting as files with checksums, and copies no COLLINS score (GAP-0541; GAP-2175). The legacy dump's source and format, the handover locations, the retention of the legacy tables and the location of the data steward's sign-off are Not specified in the source documents (GAP-2175).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every business key on a migrated case or measure snapshot resolves to its ACE view row before the record is served | REQ-RDF-007; DL25 |
| BR2 | Every break is listed with a reason the data product owner can see, and no break is suppressed | REQ-RDF-008 |
| BR3 | Zero tolerance: a BREAK result or a new REC-05 orphan resets the clean-day count, and wave 4 does not open while one migrated record has an unresolved key | DL25; DL25 option A applied by RD-P1-042, `recon.tolerance.pct` v1 = 0.00; no P1 publish status (RD-P1-024) |
| BR4 | ACE data is read only through the rwb-source-data contract and the recovery.v_ace_* views behind it, and never copied | D-RCV-35; ADR-010 |
| BR5 | The COLLINS score, its estimate and its route are read from v_ace_score and are never stored on a migrated record | Legacy RWB-DM-011 AC1; D-RCV-35 (U1) |
| BR6 | An open case keeps its route code and its route state from cutover, and a measure snapshot keeps its dimension, its value and its baseline flag | Legacy RWB-DM-011 AC1; DL25 |
| BR7 | Each service applies its own Flyway sequence in its own schema | DP-15; ADR-021 |

The harness asserts these rules and changes none of them.

Rule coverage: BR1 by AC1, AC3, TC-DM-011-02-ITG; BR2 by AC3, AC4, exception X3, TC-DM-011-02-ITG and TC-DM-011-03-ITG; BR3 by AC1, exception X3, TC-DM-011-02-ITG; BR4 by AC3, TC-DM-011-02-ITG; BR5 by AC3, exception X8, TC-DM-011-01-ITG; BR6 by AC2, exception X9, TC-DM-011-01-ITG; BR7 by AC5 (new, D-RCV-60), TC-DM-011-05-ITG. DL25 option A is applied by RD-P1-042 pending the data lead's confirmation, consistent with ASM-0728, ASM-0735, ASM-0743 and ASM-2602.

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Route state RS-SYN-001 | Reconciliation for the business date with every key resolved | `recon-2026-12-31` completes and every account_key and person_key has a DP01 or DP02 row | RS-SYN-001, unchanged |
| Route state RS-SYN-001 | Reconciliation for the business date with one orphan | account_key ACC-SYN-001177 has no DP01 row | RS-SYN-001, unchanged, and the orphan is listed |
| Route state RS-SYN-001 | A listed orphan resolves and is reconciled | A DP01 row appears for the key and the reconciliation of a later business date runs, or a FAILED run of the date is rerun | The break is no longer listed; the route state is unchanged |

The harness changes no state. Every change in the table is made by the owner: P3 rwb-case holds the case with its route code and route state, P9 rwb-reporting holds the measures and their snapshots, and P1 rwb-source-data writes the reconciliation result and the break list. The harness reads, asserts and reports; a value it had set by hand would prove nothing, so the report names the owner and the operation behind every value it asserts.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-DATASTEW, data steward | Reads the reconciliation result for a business date; holds Platform administration R and Case record R; owns the break list with the ACE team. Does not start or rerun a run |
| Harness caller | Holds Platform administration U for the readiness call, Platform administration R for the status and result reads and Case record R for the record and freshness reads |
| Harness caller, measures read | Holds Reporting R (rwb-reporting.yaml 5.1.0) |
| RW-COE, RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-SECADM | Read the same reconciliation evidence; each holds Platform administration R |
| QA lead | Owns the harness configuration, the fixtures, the report shape and the pass or fail gate |
| Integration lead | Owns the harness code, the stub set and the swap from a stub to the real service |
| The owning services' identities | P1 rwb-source-data runs JOB-04 as a child of `AceIngestCheck` and writes the reconciliation result, P9 rwb-reporting answers the measures read, P3 rwb-case holds the case and its route facts, and P4 rwb-access answers the authorisation; they make every change the harness asserts |
| No delegation of authority level applies | The harness takes no business decision; authorisation is answered by rwb-access |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 to DF-CAS-023 and DF-CAS-046 to DF-CAS-055 | recovery_case | case_no, product_group, primary_person_key, status, stage_code; route_state (DF-CAS-007) and route_code (DF-CAS-008) are the carried route facts | Read through the rwb-case contract |
| DF-RPT-001 to DF-RPT-019 | case_list_row (retired, RD-P1-024) | Not migrated and not read | None; the case list is read from rwb-case |
| DF-RPT-041 to DF-RPT-052 | measure_snapshot | measure_code, definition_version, business_date, product_group, dimension_code, baseline flag | Read through the rwb-reporting contract |
| Standard column | recovery_case, measure_snapshot | migration_source, migrated_at (RD-P1-027) | Read through the owning contract |

Field IDs are those in the Logical Data Model and Data Dictionary v9, and the three rows above are the ones the legacy story carries. In LDM v9, DF-CAS-024 to DF-CAS-029 belong to case_account, DF-CAS-030 to DF-CAS-035 to case_party and DF-CAS-036 to DF-CAS-045 to deviation, so the recovery_case row leaves them out. The case and the case list are P3's (RD-P1-024) and the measure snapshot is P9's; the harness reads each of them through its owner's contract and never from a table. The route code and the route state are DF-CAS-008 and DF-CAS-007 (RD-P1-027), asserted as the values the rwb-case read returns. The ACE side of the keys is DP01 Account and arrears for account_key and DP02 Customer and party for person_key, and the score, its estimate and its route are the DP11 Scores and route economics row over v_ace_score, each read through the rwb-source-data data-product contract (FSD P1 v3, lines 283, 284 and 293), never from a view and never from a table. The harness owns no table and writes no row. Reference lists and parameters are read through the reference-data contract under DP-06 and DP-07; the parameter names are Not specified in the source documents (DOR-RWB-ITG-DM011-ITG-20).

### 12. Contract

#### 12.1 REST operations provided

None. The harness is a test runner and provides no REST operation.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| GET | `/api/recovery/reporting/v1/reports/measures` | P9 rwb-reporting | The measure snapshots with measure_code, definition_version, business_date, product_group, dimension_code, value and the baseline flag (AC2) |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The case number, the open state, the route code and the route state of the case (AC1, AC2) |
| GET | `/api/recovery/case/v1/cases` | P3 rwb-case | The case list, which replaces the P1 case list row (AC3) |
| GET | Path pending (NEW-GAP-B3) | P1 rwb-source-data | The account-page read for the accounts on the case list (AC3) |
| GET | `/api/recovery/source-data/v1/data-products/{productCode}/records?caseId={caseId}` | P1 rwb-source-data | The DP01 account rows and the DP11 score row that carries the score, its estimate and its route (AC1, AC3) |
| GET | `/api/recovery/source-data/v1/data-products/freshness?product=DP01` | P1 rwb-source-data | `status`, `businessDate` and `loadedAt` of the product (AC1, AC8) |
| POST | `/api/recovery/source-data/v1/business-days/{date}/ready` | P1 rwb-source-data | Start `AceIngestCheck`, whose child is JOB-04, with a UUID `Idempotency-Key`; 202 (AC1, AC4) |
| GET | `/api/recovery/source-data/v1/business-days/{date}/status` | P1 rwb-source-data | `RUNNING`, `DONE` or `LATE` for the business date (AC8) |
| GET | `/api/recovery/source-data/v1/admin/reconciliation/results` | P1 rwb-source-data | The REC rows of the business date (AC1, AC3); pending in the yaml file (RWB-P1-E1011-CON) |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | The right and the refusal path (AC4) |

Every call is one hop on the owner's base `/api/recovery/<short>/v1` with a 2 s budget (DP-11, DP-13). No operation is invented in this story: each path is the owner's published operation, and the P4 refusal is the authorise operation the architecture publishes as its IN contract (Architecture v5 slide 14), every error of rwb-source-data is an `application/problem+json` body with `messageCode` (RD-P1-004), and where a screen would compose these reads the path would be the gateway-bff composite route (DP-19). The score is never read from a view by the harness; it arrives on the DP11 hop of the rwb-source-data contract (DP-05).

#### 12.3 Events published

None. The harness publishes no Kafka event; it writes its report to the wave record.

#### 12.4 Events consumed

None. The harness starts JOB-04 through the readiness call, not through an event, and reads the route, the measures and the score through the same contracts rather than from a topic.

#### 12.5 Workflows and activities

None added. JOB-04, `ReconciliationWorkflow` on rwb-source-data (Architecture v5 slides 15 and 44), workflow ID `recon-{businessDate}`, runs as the child of `AceIngestCheck` (RD-P1-040) and is exercised through the readiness call. S1's RouteDecisionWorkflow and P9's measures Schedule are named here and left alone: the harness reads the route facts already on the case and the snapshot the Schedule already wrote, and it starts, signals, reschedules or changes neither of them. No workflow, activity or Schedule is created or changed by this story.

#### 12.6 Schedules

None. The harness starts the chain for the business date under test with the readiness call and sets no cron. The measures Schedule at 01:30 stays with rwb-reporting and is not touched.

#### 12.7 Tables owned

None. The harness owns no schema and no table (DP-01); the case, its route facts and the case list are P3's, the reconciliation result is P1's and the measures and snapshots are P9's.

#### 12.8 Contract fakes

| Fake | Contract | Stubbed answer in the run |
|---|---|---|
| Stub for rwb-source-data | `fakes/rwb-source-data/5.1.0/`: the P1 operations of §12.2 | DP01 returns one row for ACC-SYN-001101 and no row for ACC-SYN-001177, DP11 returns the score row with its score, its estimate and its route, freshness returns `status` LOADED, business date 2026-12-31 with a load time, the readiness call answers 202, the status answers DONE, and the result read returns the REC rows of the date |
| Stub for rwb-reporting | `GET /reports/measures` | One snapshot for measure_code MSR-SYN-011, definition_version 1, business_date 2026-12-31, product_group PG-SYN-A, dimension_code DIM-SYN-A, with its value and a baseline flag |
| Stub for rwb-case | `GET /cases/{caseId}`, `GET /cases` | The case RW-2026-001101, open, with its case number, route code RT-SYN-011 and route state RS-SYN-001, and on the case list with account_key ACC-SYN-001177 |
| Stub for rwb-access | `POST /authorise` | Allows RW-DATASTEW with Platform administration R; refuses RW-OFF with 403 and MSG-P4-002 |
| Cutover extract fixture | The migrated records of the legacy story | The case with its route code and route state, the measure snapshot with its dimension, its value and its baseline flag, and the migration_source and migrated_at of each record; the orphan account_key ACC-SYN-001177 is on the case list answer of the rwb-case fake |
| Reconciliation extract fixture | The break list of the reconciliation | One row for case RW-2026-001101 with key type ACCOUNT, key value ACC-SYN-001177, reason NO_ACE_ROW, owner role RW-DATASTEW and the ACE team as second owner |

Each stub is generated from the published contract and its version is pinned in the run report, so a contract change shows up as a run failure and not as a silent pass. The harness environment and its base hosts, the fixture layout, the break-list fields, the extract format and its retention and the gate are Not specified in the source documents (GAP-0451; ASM-0643).

#### 12.9 Call-type summary

| Call type | In this story |
|---|---|
| REST | 0 provided, 10 consumed, one hop each on `/api/recovery/<short>/v1` with a 2 s budget (DP-11, DP-13) |
| Kafka | None published and none consumed; the run is triggered by an operation and read back through the same contracts |
| Temporal | None added; `ReconciliationWorkflow` (JOB-04) is exercised as the child of `AceIngestCheck`, while S1's RouteDecisionWorkflow and P9's measures Schedule are read only and left alone |
| File | The cutover extract fixture and the reconciliation extract fixture, both read as files |

### 13. Solution plan

**Package.** Folder `itg/recovery`, package `th.co.scb.ace.workbench.recovery.itg`, test scope only; not part of any deployed service.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The platform H dependencies in the table above (RWB-PLT-E1044-CON and RWB-PLT-N001-CON) are recorded here and are not repeated in the metadata H field of this story, which stays empty as the plan requires: the platform waves deliver both contracts, and this harness carries no build dependency of its own. The one blocking relationship is the I story RWB-P1-DM011-APP, which replaces its stub; until it is live the run uses the stub, and a stub pass is reported as a stub pass.

**Harness components**

| Component | Type | Responsibility |
|---|---|---|
| JourneyRunner | Job | Runs the criteria of section 7 in order for a business date and holds the run lock |
| StubSet | Fake | The four stubs of §12.8 generated from the published contracts, with the contract version pinned |
| CutoverExtractFixture | Fixture | The synthetic case with its route code and route state, the measure snapshot and the orphan account_key, with migration_source and migrated_at |
| RouteAndBaselineAssertion | Service | Compares the route read and the measures read with the fixture: route code, route state, measure_code, definition_version, business_date, product_group, dimension_code, value and the baseline flag |
| KeyResolver | Service | Resolves every business key through DP01 and DP02 with the freshness read, reads the DP11 score row, and names each key that does not resolve |
| NoCopyAssertion | Service | Fails the run where a migrated record or the report holds a stored COLLINS score, estimate or route, and pins the DP11 read the report quotes |
| BreakListAssertion | Service | Compares the read result with the reconciliation extract fixture: one row per orphan, its reason and its two owners, and one row only on a repeated run |
| EvidenceReport | Service | Writes one report per business date keyed by story, and holds the pass or fail gate |

**Environment and test data.** SIT, against the stubs from Day 1 and the real services as the I story lands, on the synthetic case RW-2026-001101, route code RT-SYN-011, route state RS-SYN-001, account_key ACC-SYN-001101, person_key PERS-SYN-001101, measure snapshot MSR-SYN-011 at definition_version 1 for product_group PG-SYN-A and dimension_code DIM-SYN-A, orphan account_key ACC-SYN-001177 and business date 2026-12-31. In SIT the records come from the rwb-case and rwb-reporting cutover loads on their own Flyway sequences (DP-15). The environment and its base hosts, the fixture layout, the break-list fields, the extract format and its retention, the gate and the seeding set are not specified in the source documents (GAP-0451; ASM-0643). The harness seeds nothing by hand and never writes a schema row.

**Build steps**

1. Generate the four stubs from the published contracts and pin each contract version in the run report; fail the run on a mismatch (X1).
2. Build the CutoverExtractFixture and the ReconciliationExtractFixture, and prove both are read for business date 2026-12-31 (X2).
3. Build the JourneyRunner for AC1: send the readiness call with a UUID Idempotency-Key, wait for `recon-2026-12-31`, read the case through rwb-case, resolve account_key and person_key through DP01 and DP02 with the freshness read, and list each orphan (X5).
4. Add the RouteAndBaselineAssertion for AC2: route code RT-SYN-011 and route state RS-SYN-001 from the rwb-case read, and measure_code, definition_version, business_date, product_group, dimension_code, value and the baseline flag from the rwb-reporting read (X9).
5. Add the NoCopyAssertion and the DP11 read for AC3: one hop with a 2 s budget, the orphan row with reason NO_ACE_ROW and both owners, and no stored score, estimate or route on a migrated record or in the report (X3, X8).
6. Add AC4: repeat the readiness call for the same business date, assert one break row, equal counts of cases and measure snapshots, and one report entry per business date (X4, X7).
7. Add the access path for AC4 through `POST /api/recovery/access/v1/authorise`, then the EvidenceReport and the gate, and swap a stub for the real owner as its I story lands (X6).

**Feature switch.** None. The harness has no production flag and runs in the test environment only.

**Done when.** The tests of section 16 pass against the fakes and again against RWB-P1-DM011-APP when it lands, and the wave entry check holds a run report keyed by story and business date that names the route code, the route state, the baseline flag, the DP11 score read and every break with its reason and its two owners.

### 14. Validation and messages

| ID | Type | Message |
|---|---|---|
| MSG-P1-001 | Warning | {product} is from {date}. Today's load has not arrived. |
| MSG-P1-012 | Warning | The case list for {date} does not reconcile to ALS for {product}: a difference of {variance} accounts, {pct} percent. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |

The harness asserts the message ID and the substituted values on the answer it reads, and owns no message text. MSG-P1-012 is raised by rwb-source-data only for a REC-01 or REC-02 BREAK (RD-P1-042), and the harness asserts it only against a BREAK fixture.

### 15. Screens and states

The legacy story names SCR-45 Data quality with the states loading and breaks, and it states that the breaks are listed on the reconciliation extract. This harness builds neither the screen nor the console: the data steward and the ACE team read the extract as a file. The states the harness asserts on that extract are: loading, breaks (the breaks are listed on the reconciliation extract), empty (Not specified in the source documents (CG-ALL-1050)), error (Not specified in the source documents (CG-ALL-1050)) and no access (Not specified in the source documents (CG-ALL-1050)).

| State | What the extract holds |
|---|---|
| No break | One line for the business date with the counts of cases and measure snapshots, and no break row |
| Break | One row per orphan with the case number, the key type, the key value, the reason, the data steward and the ACE team as owners |

The harness renders no screen. What the wave entry check looks at instead is the run report, whose environment, layout, extract format and retention are Not specified in the source documents (GAP-0451; ASM-0643). The harness pack, meaning the environment and base hosts per hop, the cutover extract fixture layout, the reconciliation extract format and retention, and the pass or fail gate, is agreed at the wave 4 entry check (GAP-0451).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-DM-011-01-ITG | AC1 (legacy, the extraction RWB-P1-DM011-APP owns); ITG AC2, ITG AC3 | Integration | The synthetic cutover extract RW-2026-001101 with route code RT-SYN-011, route state RS-SYN-001 and measure snapshot MSR-SYN-011, and no stored COLLINS value |
| TC-DM-011-02-ITG | AC2 (legacy); ITG AC1, ITG AC3 | Integration | One account_key ACC-SYN-001177 on the case list answer with no row in the rwb-source-data contract fake, and the DP11 score row read on the same hop |
| TC-DM-011-03-ITG | AC3 (legacy, owned by RWB-P1-DM011-APP); ITG AC4 | Integration | Two readiness calls for business date 2026-12-31 |
| TC-DM-011-04-ITG | Access; ITG AC4 | Component | RW-OFF caller without Platform administration R |
| TC-DM-011-05-ITG | AC5 (new, D-RCV-60); BR7 | Integration | The harness run for business date 2026-12-31 with no table written and no row written |
| TC-DM-011-06-ITG | AC6 (new, D-RCV-60); BR1 to BR7 | Guardrail | Not specified in the source documents (NEWAC-RWB-ITG-DM011-ITG-AC5) |
| TC-DM-011-07-ITG | AC7 (new, D-RCV-60) | Integration | Not specified in the source documents (NEWAC-RWB-ITG-DM011-ITG-AC6) |
| TC-DM-011-02-ITG, TC-DM-011-01-ITG, TC-DM-011-08-ITG, TC-DM-011-03-ITG, TC-DM-011-04-ITG, TC-DM-011-09-ITG, TC-DM-011-07-ITG | New ITG AC8 and the changed assertions of ITG AC1 to AC4 and AC7 | Integration | Values of section 7 |

The Covers column names the legacy AC the copy derives from and the ITG AC it asserts; the cutover assertions of TC-DM-011-03-ITG stay with RWB-P1-DM011-APP, and the ITG copy asserts only the determinism of the repeated run and the one report per business date. The full legacy test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx under the same legacy test case ID.

### 17. Guardrails

- No business value in code: the synthetic keys, the route code, the route state, the measure snapshot, the business date, the fixture contents, the break reasons and the report layout are data.
- No personal data in logs, fixtures or reports: every key is synthetic and no customer record is read at all.
- No read of another service's schema and no direct view read: the case comes from rwb-case, its route facts from rwb-case, the measures from rwb-reporting, and the ACE side of the keys and the score from the rwb-source-data contract (DP-01, DP-05).
- Nothing of the COLLINS score is stored: the score, its estimate and its route are read on the DP11 hop every time, and a stored copy fails the run rather than being reported as a pass.
- One hop and a 2 s budget per call, with a circuit breaker per downstream, so the harness fails where a screen would (DP-11).
- A stub pass is never reported as a real pass: the report names the contract version and whether the hop was a stub or the owner.
- The harness never runs against UAT or production, and it never writes a row by hand.
- A failing criterion is fixed in the service that owns it or reported as a gap; it is never waived in the script.

### 18. Traceability

| Item | Source | Where it lands |
|---|---|---|
| Legacy story RWB-DM-011 Migrate scores and route economics | Recovery Workbench Data Migration Stories v4, lines 716 to 796 | Sections 1, 3, 11 and 19 of this file |
| Legacy AC2 Reconcile the business keys, verbatim | The same, lines 741 to 745 | Section 7, AC1, marked (legacy RWB-DM-011 AC2) |
| Legacy AC1 and AC3, and the four legacy test cases TC-DM-011-01 to TC-DM-011-04 | The same, lines 735 to 751 and 789 to 794 | AC1 and AC3 stay with RWB-P1-DM011-APP (section 19); the four cases are copied as -ITG in section 16 |
| DF-CAS-001 to DF-CAS-055, DF-RPT-001 to DF-RPT-019, DF-RPT-041 to DF-RPT-052 | Logical Data Model and Data Dictionary v9 | Section 11 |
| DP01 Account and arrears, DP02 Customer and party, DP11 Scores and route economics, each with one system of record | FSD P1 v3, lines 283, 284 and 293 | Sections 3, 11 and 12.2 |
| S1 rwb-valuation, its IN read `GET /cases/{id}/valuation` and the D6 route decision | Architecture v5 Text Extract v1 slides 18 and 41 | Section 12.5; the migrated route facts are read from rwb-case (RD-P1-027) |
| P9 rwb-reporting, which owns measures and snapshots, with its Schedule at 01:30 | Architecture v5 Text Extract v1 slides 15 and 41 | Sections 11, 12.2 and 12.5 |
| JOB-04 Reconciliation, event-triggered on rwb-source-data | Architecture v5 Text Extract v1 slides 15, 44 and the job map | Section 12.5 |
| DL25, zero tolerance on the migrated data | Decision Log, DL25 | Section 8, BR1 to BR3 |
| D-RCV-35 and ADR-010, ACE data only through the views | Decision Log, D-RCV-35; ADR-010 | Section 8, BR4 and BR5; sections 12.2 and 12.8 |
| DP-05, DP-15 and DP-19 | Template and Rules v1 §R5.5 | Section 13, pattern application |

### 19. Out of scope

- RWB-P1-DM011-APP: the migration, the reconciliation, the break list and legacy AC1 and AC3. The cutover load of the records into `rwb_source_data` and the schemas of the other owners is theirs, on their own Flyway sequences.
- The production code of S1 rwb-valuation, P9 rwb-reporting, P3 rwb-case and P1 rwb-source-data, and their CON, APP and DB stories: the route decision, the measures and snapshots, the case and the reconciliation are built there.
- S1's RouteDecisionWorkflow and P9's measures Schedule: named in section 12.5 and left alone; the harness reads what they already wrote.
- SCR-45 Data quality and the break console the legacy story names; the harness renders no screen and reads the reconciliation extract as a file.
- The cutover plan, the data steward sign-off and the legacy read-only period of legacy AC3.
- ACE ingestion and the 30 views (RWB-ACE-001), and the COLLINS model refresh itself.
- Platform deployment and configuration.
- The other four data migration keys of this wave.

### 20. Remaining delivery steps

- Size the story (RW-TRIBE).
- Record the signed epic design of EP08 (product owner).
- Publish the rwb-source-data 5.1.0 fake and add the reconciliation result reads to the yaml file (rwb-source-data contract owner).
- Settle the break-detail store (rwb-source-data data architect; GAP-1508, NEW-GAP-S2B-03).
- Fix the path and maximum keys per call of the P1 account-page read (solution architect; NEW-GAP-B3).
- Add the authorise path to the rwb-access yaml (rwb-access contract owner).
- Provide the stubs and synthetic fixtures in DEV (integration lead).
- Add the new and changed test case rows in Test Cases v9 and the Requirements Traceability Matrix (test writer).
