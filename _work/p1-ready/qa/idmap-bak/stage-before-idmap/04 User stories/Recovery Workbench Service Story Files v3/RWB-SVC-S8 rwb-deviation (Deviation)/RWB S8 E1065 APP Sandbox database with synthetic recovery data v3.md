# RWB-S8-E1065-APP Sandbox database with synthetic recovery data

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S8-E1065-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-deviation |
| Service epic | RWB-SVC-S8 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-065 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP04, DP05, DP07, DP13, DP15, DP19 |
| Parallel lane | L-S8-E |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-S8-E1065-APP-16) |
| Depends on (build) | None |
| Contract dependencies | RWB-P1-E1065-CON |
| Contract version | The versioned fixture files of the RWB-P1-E1065-CON contract package (`seed-profile.json`, `case-seed-list.csv`, `shape-table.csv` and the stage fixtures); package version Pending (ASM-5690) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S8 rwb-deviation v1.md (no FR mapped to REQ-RDF-001, REQ-RDF-010) |
| Epic design sign-off | Not specified in the source documents (DOR-RWB-S8-E1065-APP-14); no signed epic design record is recorded in the story or the source documents |
| Status | Draft (directive resolutions) |
| Readiness decisions | RD-P1-021, RD-P1-046, RD-P1-073 |

**Version 3 changes.**

- D-RCV-60 P1 developer readiness (RD-P1 register). Specified per-owner seeding and preservation of the previous sandbox on failure. Applied the follow-up v9 citation corrections. Backfilled 12 mapped v9 test case IDs. RD-P1-073.
- Shared sandbox (RD-P1-046): this slice applies only the `rwb_deviation` sequence with the rwb-deviation login, seeds only `rwb_deviation` in one transaction and never creates, renames, drops or recreates `rwb_sandbox` (findings 1 and 4).
- The input is the versioned fixture files of RWB-P1-E1065-CON, not a stage contract operation; shape counts come from `shape-table.csv` (RD-P1-046; findings 3 and 6).
- The published files carry no `case_id` and no routed state: both are Pending under NEW-GAP-F17-1 and the criteria run on a test-only case-reference fixture (finding 2).
- The `rwb_deviation` DEV read-only role is not P1's `rwb_sandbox_read`; its name is Pending under NEW-GAP-F17-2 (finding 5).
- AC12 added for the schema boundary of the shared sandbox; role seed ownership restated (RD-P1-021; findings 7 and 8).

**Change log.** D-RCV-60, 27 November 2026: D-RCV-60 P1 developer readiness (RD-P1 register).

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-065 for rwb-deviation. The monolith seeded 92 tables in one `recovery` schema from one pipeline stage; in the target every service seeds its own slice, in its own schema, and reads no other service's table (DP-01). This story is the deviation slice of the sandbox: the `deviation` table of `rwb_deviation` filled with synthetic deviations X1 to X7 attached to the synthetic cases by business key, driven by the data dictionary and the lists of values, verified, and exercised once in the embedded Drools kit. It is a secondary slice of the legacy key: the nine legacy acceptance criteria and the generator, verifier, export tool and stage itself stay word for word with RWB-P1-E1065-APP, the stage contract is RWB-P1-E1065-CON, and this story owns no legacy criterion. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-S8-E1065-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (23 resolved, 29 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **recovery developer (RW-TRIBE)**, I want **the rwb-deviation slice of the DEV sandbox — `deviation` in `rwb_deviation` filled with synthetic deviations X1 to X7 on the seeded synthetic cases, every value drawn from the data dictionary and the lists of values in force and never from production data**, so that **I can build and test every deviation pause, contact stop, route and clear against a realistic deviation estate from Day 1, before SIT is connected and without a copy of source data**.

This story delivers, inside `rwb-deviation` only:

- the `deviation-seed` module of `tools/sandbox-generator`, Java package `th.co.scb.ace.workbench.recovery.deviation.sandbox`, a separate build module that is never packaged into the service artefact;
- `DeviationSeedGenerator`, `ShapeSeeder`, `DecisionRecordSeeder`, `RuleSmokeCheck`, `DeviationSeedVerifier` and `SandboxExport` (section 13);
- the seed profile values as data — seed 20261128 and the three product volumes from `seed-profile.json` and the count per shape from `shape-table.csv` of RWB-P1-E1065-CON (RD-P1-046), every one overridable;
- the dictionary-driven fill of `deviation` (DP-01), the list values read as rows and never as code (DP-07), one local decision record per seeded raise through the decision-record library (DP-03) and one embedded-kit evaluation of R-DEV-01 to R-DEV-06 per seeded row (DP-04).

It does not build the sandbox database, the ACE schema test double, the 30 `v_ace_*` views, the P1 read-only role or its grants — those are RWB-P1-E1065-APP and RWB-P1-E1065-DB, which build and seed only `public`, `recovery` and `rwb_source_data` (RD-P1-046). Its C dependency is the versioned fixture files of RWB-P1-E1065-CON. It does not seed the case estate, the interactions or the documents: those are RWB-P3-E1065-APP, RWB-P1-E1065-APP and RWB-P5-E1065-APP, and this story reads none of their tables (GAP-3086; ASM-5261).

### 2. Business rationale

DEV has no ACE database and no case data, so before the sandbox no squad could test a source read, a case list or a report (legacy section 2). The realignment changes who seeds what: the recovery schema of 92 tables becomes 19 schemas with one owner each, and no service may seed or read another service's tables (DP-01, DP-02). The deviation estate is the clearest case of that rule — `deviation` is S8's single table, and its rows are the only thing in the whole sandbox that a deviation screen, the pause of a stage clock, a contact stop or a route decision can be tested against (context pack ownership rows; TSD S8 T3.1).

Three facts shape the slice.

1. **The shapes are the point.** Legacy BR4 asks for 10 cases of each exception shape, and three of the ten are deviations: an open deviation, a deceased customer and a bankruptcy. The deceased shape is the one the architecture uses as its worked example — X3 raised, the stage clock paused, the prescription clock still running, contact stopped (Architecture v5 slide 8; FSD S8 A2.12). Without those rows no test of R-DEV-01, of the contact stop of X1 to X3 or of the return point is possible.
2. **Every value is data.** Legacy BR3 and BR5 fix it: volumes, seed and shapes are properties and values come from the dictionary and the lists, so a schema change reaches the sandbox with no manual rebuild. In the target the same rule is DP-01 and DP-15: the fill reads `sys_fields` and `lov_value` and writes the service's own schema on its own Flyway sequence.
3. **No production data, no personal data.** Legacy BR1, BR7 and BR9 serve REQ-RDF-010: the deviation slice holds synthetic rows only, and the verifier blocks a value that looks real. `handler_user_id` is a synthetic user reference, because a deviation names its handler and the handler is a person.

The slice therefore serves REQ-RDF-001 (the deviation data product with one system of record and one owner — this service, in `rwb_deviation`) and REQ-RDF-010 (no personal data outside its permitted use). It changes no rule, no list and no state of the DEV route set.

### 3. Preconditions

- The shared DEV sandbox `rwb_sandbox` exists with `public`, `recovery` and `rwb_source_data` built by RWB-P1-E1065; this story does not create it. The rwb-deviation sequence has run on `rwb_deviation` with the rwb-deviation login, after the P1 build and in the wave order of Architecture v5 slide 41 (RD-P1-046): `deviation` exists with DF-CAS-036 to DF-CAS-045 and the standard record columns of TSD S8 T3.0, and the outbox, inbox and idempotency tables of the platform event library are in the schema (DP-15).
- RWB-P1-E1065-CON is published as versioned files of its contract package, not as an operation (RD-P1-046): `seed-profile.json` (seed 20261128, total 2,812 cases, product volumes), `case-seed-list.csv` (shape_id, product_group, account_key, person_key, case_entry_date, total_outstanding; no case number), `shape-table.csv` (shape_id, row_type, count, product_group, is_case) and the stage fixtures full, empty, refused and timeout. The package version is Pending (ASM-5690).
- The dictionary rows for `deviation` and the three lists are present in the sandbox after the rwb-deviation sequence, seeded from the Logical Data Model and Data Dictionary v9 and TSD S8 T3.2; the seeder validates every code against those rows at seed time and never against a constant (ASM-5262).
- The seed profile gives the volumes 1,226 MORTGAGE, 1,296 HIRE_PURCHASE and 290 SSME (10 percent of the 30 June 2026 inventory; DL15), 2,812 cases in total. `case-seed-list.csv` carries no `case_id` and no routed state, and rwb-case assigns the case numbers when it seeds (RD-P1-046). Pending: the published source of `case_id` and of the routed state for each shaped row, owner rwb-case service owner with the data architect, tracked as NEW-GAP-F17-1. Until it is closed, this module runs on its own test-only case-reference fixture, which gives each shaped row of `case-seed-list.csv` a synthetic `case_id` and routed state, and it never reads a table of rwb-case (ASM-5261).
- The seed values are readable: `rwb.sandbox.seed=20261128` and the three volumes from `seed-profile.json`, and the count per shape from `shape-table.csv` (10 for each shape in legacy BR4; where no count is given the value is Pending under GAP-3278). Every value is overridable and none is a constant of the module.
- A PostgreSQL 17 instance reachable from the pipeline holds the shared `rwb_sandbox` in DEV and in the pipeline test environment; the rwb-deviation login has USAGE on `rwb_deviation` only (RD-P1-046; DP-01).
- The embedded Drools kit of RWB-PLT-E1072-CON is on the service template, and the DEV route set is held in the build fixture at its version in force (DP-04; ASM-5263).
- The decision-record library of RWB-PLT-E1027-CON is on the service template; the outbox relay is not started in DEV, so a seeded decision record stays local to `rwb_deviation` (DP-03).
- No approval is needed to build against a Draft contract baseline; the contract is tagged by RWB-P1-E1065-CON when its tests pass.

### 4. Flow

1. Pipeline: on a merge to main that changes a file under the `rwb_deviation` migration folder, the dictionary, the pinned fixture package version or the test-only case-reference fixture, or on a manual start by RW-TRIBE or RW-PLATADM, the rwb-deviation seed step runs in DEV or the pipeline test environment.
2. Seed step: connects to the shared `rwb_sandbox` with the rwb-deviation login and takes one advisory lock for the rwb-deviation seed; it creates no database and changes no other schema, and it fails naming the database when `rwb_sandbox` is absent (RD-P1-046).
3. Seed step: applies the rwb-deviation Flyway sequence to `rwb_deviation`, with the dictionary rows and the three lists (DP-15). It applies no ACE DDL, no Tier 2 DDL and no view migration.
4. `MetadataReader`: reads `sys_objects`, `sys_fields` and `lov_value` to learn every column, type and list of `deviation`; a column with no `sys_fields` row stops the seed and names the table and the column (legacy X1, AC4).
5. `ShapeSeeder`: reads `seed-profile.json`, `case-seed-list.csv` and `shape-table.csv`, selects the rows whose `shape_id` is a deviation shape, takes `case_id` and the routed state from the test-only case-reference fixture (NEW-GAP-F17-1), and maps each deviation shape to its code as the sources publish it — the deceased customer to X3 (FSD S8 A2.12; Architecture v5 slide 8) and the bankruptcy to X5 (FSD S8 A2.14) — while the open-deviation shape and the four remaining codes take their code from LOV-DEVIATION at the version in force (ASM-5264).
6. `DeviationSeedGenerator`: in one transaction on `rwb_deviation`, deletes the rows of the previous seed run and writes one `deviation` row per shaped row, with `case_id` from the fixture, `deviation_code` from the shape, `raised_at` from the business date of the seed, `raised_by` from LOV-RAISED-BY, `paused_state` from the routed state of the fixture, `handler_user_id` a synthetic user reference, `contact_stop` true for X1 to X3, `cleared_at` and `outcome` null while open, and `state` "DEV_FLAGGED" as R-DEV-01 leads (TSD S8 T4).
7. `DecisionRecordSeeder`: writes one local decision record per seeded raise through the decision-record library, first in the transaction, naming R-DEV-01 and the package version in force; no outbox row is written because no relay runs in DEV (DP-03).
8. `RuleSmokeCheck`: evaluates R-DEV-01 and the owner-assignment rules R-DEV-02 to R-DEV-06 in the embedded kit for every seeded row, compares the projected owner with the shape, and fails the step on a mismatch (DP-04).
9. `DeviationSeedVerifier`: row count per code, list values at the version in force, contact stop on X1 to X3, `cleared_at` on open and cleared rows, every `case_id` present in the case-reference fixture, the personal-data pattern scan, and the absence of any table of another service in `rwb_deviation`.
10. Seed step: commits only when every check passes (otherwise the transaction is rolled back and the rows of the previous run stay), grants SELECT on `rwb_deviation` to the rwb-deviation DEV read-only role (a role other than `rwb_sandbox_read`; name Pending under NEW-GAP-F17-2), and publishes the build report with the row count per table and the verifier result.
11. Each E1065 schema owner seeds its own schema. A seed failure rolls back the rwb_deviation transaction, fails the pipeline and leaves the previous sandbox in place (RD-P1-073 rule 2).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A `deviation` column has no `sys_fields` row | The seed step fails naming the table and the column; its transaction is rolled back and the `rwb_deviation` rows of the previous run stay | None (pipeline result) | AC3 |
| X2 | The seed step runs twice for the same commit and seed | The seed rows of `rwb_deviation` are deleted and written again in one transaction; the same seed gives the same rows and counts; no database or schema is dropped | None | AC5 |
| X3 | A generated value breaks a constraint | The seed step fails naming the table and the constraint; its transaction is rolled back and the rows of the previous run stay | None (pipeline result) | AC2 |
| X4 | A generated value in `rwb_deviation` matches a personal data pattern | The seed step fails naming the table and the column; its transaction is rolled back and the rwb-deviation slice of that run is not published | None (pipeline result) | AC7 |
| X5 | A shaped row of `case-seed-list.csv` has no `case_id` or routed state in the case-reference fixture | The seed step fails naming the `shape_id` and the account key; its transaction is rolled back | None (pipeline result) | AC4 |
| X6 | A second rwb-deviation seed step starts while one runs | The second step waits on the rwb-deviation seed advisory lock and runs after the first | None | AC5, AC9 |
| X7 | A list in force is empty or the list rows are not readable | The build fails closed before a row is written and names the list; the module never falls back to a constant or to a copy of a list | None (pipeline result) | AC2 |
| X8 | `seed-profile.json`, `case-seed-list.csv`, `shape-table.csv` or the case-reference fixture is absent or unreadable, or no row carries a deviation shape | The seed step stops before the seed and writes nothing, because this story owns no case reference of its own | None (pipeline result) | AC1, AC4, AC11 |
| X9 | A component, a statement or a test reaches `rwb_case`, a `v_ace_*` view or another service's schema | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | Section 17, AC1 |

X1 to X6 are the exception paths of RWB-E1-065 carried onto the deviation slice; X7 to X9 are the paths the split adds, one for the lists, one for the fixture files and case references this service does not own, and one for the schema boundary.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds on Day 1 against the versioned fixture files of RWB-P1-E1065-CON, the dictionary rows of its own schema and the test-only case-reference fixture, and waits for no in-lane story |
| Negotiable | The component names, the fixture shape and the verifier's message wording are this story's; the codes, the lists, the seed and the volumes are rows and properties |
| Valuable | Every deviation read, pause, contact stop, route and clear is testable in DEV from the first day, with no production data and no other team's data |
| Estimable | One seed module, one shape seeder, one decision-record step, one smoke check, one verifier and one export path |
| Small | Fits one sprint as the secondary slice of the legacy key, beside RWB-P1-E1065-APP, RWB-P3-E1065-APP and RWB-P5-E1065-APP |
| Testable | Every criterion is a query against the built schema, a build-failure case or one embedded-kit evaluation |

### 7. Acceptance criteria

```gherkin
Feature: Sandbox database with synthetic recovery data — the rwb-deviation slice

  Background:
    Given the RWB-P1-E1065-CON fixture files seed-profile.json (seed 20261128, 1,226 Mortgage, 1,296 Hire purchase and 290 SSME, 2,812 in total), case-seed-list.csv and shape-table.csv with a count of 10 per deviation shape
    Given the shared rwb_sandbox built by RWB-P1-E1065 and the test-only case-reference fixture that gives each shaped row a case_id and a routed state
    Given the dictionary fixture returns the 10 fields of deviation (DF-CAS-036 to DF-CAS-045) and LOV-DEVIATION with X1 to X7, LOV-RAISED-BY and LOV-DEV-OUTCOME at the version in force

  Scenario: AC1 The deviation slice of the sandbox exists (new, D-RCV-60)
    Given the rwb-deviation sequence has run on rwb_deviation and the seed step holds the fixture files and the case-reference fixture
    When the rwb-deviation seed step runs
    Then schema rwb_deviation holds deviation with its 10 fields and the standard record columns
    Then every shaped row carries one deviation row with the case_id of the fixture and no row exists for a case_id the fixture does not list
    Then none of the 20 tables that left the schema exists in rwb_deviation, and no table of another service, among them recovery_case, interaction, document and rule_row, exists in the schema

  Scenario: AC2 Every seeded value is a value of the list in force (new, D-RCV-60)
    Given the lists at the version in force: LOV-DEVIATION with X1 to X7, LOV-RAISED-BY and LOV-DEV-OUTCOME
    When the build completes
    Then every deviation_code is one of X1 to X7, every raised_by is one of SCREENING_AGENT, RULE, OFFICER and CUSTOMER_CONTACT, and every outcome is one of RETURNED, RE_ROUTED and CASE_ENDED where it is set
    Then contact_stop is true on every seeded row of X1, X2 and X3 and false on every seeded row of X4 to X7
    Then every open row has cleared_at null and every state is a state of the DEV route set
    Then an empty LOV-DEVIATION, or list rows that are not readable, fails the build before a row is written and names the list

  Scenario: AC3 The seed follows the data dictionary (new, D-RCV-60)
    Given a test migration, never shipped, adds column "deviation_band varchar(10)" to deviation with its sys_fields row and list LOV-DEV-BAND
    When it is applied and the build reruns
    Then every seeded row holds deviation_band with a value from LOV-DEV-BAND and no generator code was changed
    Then a dictionary fixture without the sys_fields row for deviation.cleared_at fails the step with "deviation.cleared_at has no data dictionary entry" and the rows of the previous run stay

  Scenario: AC4 The exception shapes carry their deviation rows (new, D-RCV-60)
    Given shape-table.csv gives a count of 10 for the deceased shape, the bankruptcy shape and the open-deviation shape, and the case-reference fixture gives each of those rows a case_id
    When the build completes
    Then each deceased reference carries deviation "X3" with contact_stop true
    Then each bankruptcy reference carries deviation "X5" with contact_stop false
    Then each open-deviation reference carries one open row whose code is in LOV-DEVIATION and whose cleared_at is null
    Then the estate holds at least one open deviation of every code X1 to X7
    Then a shaped row with no case_id in the case-reference fixture fails the step and names its shape_id and account key

  Scenario: AC5 The reset is idempotent (new, D-RCV-60)
    Given the rwb-deviation seed step ran for commit "a1b2c3d" with seed 20261128
    When the step runs again for commit "a1b2c3d" and seed 20261128
    Then the seed rows of rwb_deviation are deleted and written again in one transaction, and rwb_sandbox is not dropped, renamed or recreated
    Then deviation holds the same row count and the same count per code
    Then the row of the first case_id of the case-reference fixture holds the same deviation code and the same raised_at
    Then no row from the first run remains
    Then a second seed step that starts while one runs waits on the rwb-deviation seed lock and runs after the first

  Scenario: AC6 It is readable, extractable and not writable (new, D-RCV-60)
    Given the seeded rwb_deviation schema and the rwb-deviation DEV read-only role (a role other than "rwb_sandbox_read")
    When a member of RWB-DEV-RW-TRIBE runs "SELECT deviation_code, count(*) FROM rwb_deviation.deviation GROUP BY deviation_code"
    Then the result shows the codes X1 to X7 with their counts
    Then the export script writes deviation to a CSV file without a request to another team
    Then an UPDATE on rwb_deviation.deviation by the same role is refused
    Then a test user without the Case record right U calls POST /api/recovery/deviation/v1/cases/{caseId}/deviations and is refused with 403 and MSG-P4-002 before any row is written

  Scenario: AC7 No clear personal value in the deviation slice (new, D-RCV-60)
    Given the verifier scans every text column of rwb_deviation and every column the dictionary tags is_personal
    When a seeded value in deviation.paused_state matches the 13-digit national ID pattern with a valid check digit
    Then the build fails naming deviation.paused_state
    Then a clear identity number in public.customer is not a failure, because ACE holds it and this service reads no ACE table
    Then the transaction is rolled back and no rwb-deviation row of that run is published
    Then handler_user_id holds a synthetic user reference and no name, contact value or identity number

  Scenario: AC8 The seeded deviations pass the rules smoke check (new, D-RCV-60)
    Given the DEV route set at its version in force, with R-DEV-01 and R-DEV-02 to R-DEV-06, held in the build fixture
    When the smoke check runs in the embedded kit after the seed
    Then every seeded open deviation satisfies R-DEV-01 and is recorded in state "DEV_FLAGGED"
    Then the owner projected for code "X1" is the complaint officer "RW-COMPLAIN" from R-DEV-02 and for code "X4" the fraud investigator "RW-FRAUD" from R-DEV-04
    Then one local decision record per seeded raise exists in rwb_deviation, written before the row, and no rwb.deviation.events.v1 event is published
    Then a mismatch between a seeded row and the rule outcome fails the build

  Scenario: AC9 Two seed steps started together wait on the seed lock (new, D-RCV-60)
    Given two rwb-deviation seed steps are started together for a1b2c3d and e4f5a6b
    When the second step starts
    Then the second step waits on the rwb-deviation seed lock and runs after the first commits or rolls back

  Scenario: AC10 The rules of section 8 hold on the built sandbox (new, D-RCV-60)
    Given the rwb-deviation seed step has completed with its build report
    When the verifier and the seeder report on the built sandbox
    Then the seeder wrote synthetic rows only, on synthetic case references, and no row comes from public or from a v_ace_* view
    Then the row counts of rwb_deviation are published in the build report after the rwb-deviation sequence
    Then no code, list value or state is a constant in the seeder, and each is read from sys_fields and lov_value
    Then no test user row and no copy or load table exist in rwb_deviation
    Then handler_user_id holds a synthetic user reference and the verifier blocks a real-looking value in rwb_deviation

  Scenario: AC11 A missing or unreadable input stops the seed step (new, D-RCV-60)
    Given seed-profile.json, case-seed-list.csv or shape-table.csv is absent or unreadable, or the stage fixture is refused or timeout, or the dictionary rows are not readable
    When the rwb-deviation seed step runs
    Then the step fails before any row is written and names the file or the dictionary read that failed
    Then the rwb_deviation rows of the previous run stay and no other schema is touched

  Scenario: AC12 The seed stays inside its own schema of the shared sandbox (new, RD-P1-046)
    Given the shared rwb_sandbox holds public, recovery, rwb_source_data and other rwb_* schemas
    When the rwb-deviation seed step runs with the rwb-deviation login
    Then only rows of rwb_deviation change and the database is not created, dropped, renamed or recreated
    Then an INSERT into rwb_source_data.interaction or rwb_case.recovery_case by that login is refused by the database and fails the boundary test
```

The twelve criteria are new, tagged "(new, D-RCV-60)", and test only the deviation slice of the sandbox. The nine legacy criteria of RWB-E1-065 are owned word for word by RWB-P1-E1065-APP, which carries the stage, the generator and all nine; this story owns none of them. The values reused here are the ones the sources publish: seed 20261128 and the three volumes (legacy BR5, DL15), the shape count 10 (legacy BR4; `shape-table.csv`), the codes X1 to X7 and the three lists (TSD S8 T3.2), X3 as the deceased customer (FSD S8 A2.12; Architecture v5 slide 8), X5 as the bankruptcy (FSD S8 A2.14), the contact stop on X1 to X3 (FSD S8 A2.5; Architecture v5 slide 8) and "RW-FRAUD" for X4 (legacy AC4). Two points are recorded rather than smoothed over: `case_id` and the routed state have no published source yet and come from a test-only fixture, not from rwb-case (NEW-GAP-F17-1; GAP-3086; ASM-5261), and the number of deviations per case is not published (ASM-5264).

Open decisions that apply to this story are DL15 (assumption ASM-5264) and DL39. Each decision is still open; whether each assumption is confirmed is Not specified in the source documents (DOR-RWB-S8-E1065-APP-18).

### 8. Business rules

| ID | Rule | What this story does with it | Source |
|---|---|---|---|
| BR1 | No production data in DEV; the sandbox holds synthetic data only | The seeder writes synthetic rows only, on synthetic case references | NFR-045; CTL-11 |
| BR2 | The sandbox is built from the same DDL as SIT | This slice applies only the `rwb_deviation` sequence after the P1 build of the shared `rwb_sandbox` and seeds only what its own migrations created (DP-15; RD-P1-046); the row counts are published in the build report (GAP-0374) | RWB-E1-001; RWB-E1-069; ADR-001 |
| BR3 | Generated values come from the data dictionary and the lists of values, not from code | `MetadataReader` and `ValueFactory` read `sys_fields` and `lov_value`; a code, a list value or a state is never a constant (DP-07) | sys_fields; lov_value; Principle 1 |
| BR4 | Exception shapes generated: duplicate case for one customer and product (R-UNI-17), deceased customer (R-UNI-05), bankruptcy (R-UNI-07), open deviation, legal hold (R-UNI-20), unmapped product code, collateral with no account, case with three accounts, accounts at 89 and 90 days past due (DL16), withdrawn consent (R-UNI-10) | Carries the three deviation shapes of the ten — open deviation, deceased X3, bankruptcy X5 — and asserts them; the other seven are the case estate's (RWB-P3-E1065-APP) | rules.txt; DL16 |
| BR5 | Case volumes follow the product split of the 30 June 2026 inventory at 10 percent | Reads the volumes from `seed-profile.json`; seeds no case and counts its own rows per code | DL15; RD-P1-046 |
| BR6 | Every role has a named test user before it has real users | Not seeded here: role and permission rows are the seed of rwb-access (RD-P1-021) and each service seeds only its own schema (RD-P1-046); the owner of the DEV test identity per role is the platform administrator per the directive resolution of GAP-0896, and it is not a row of this slice | DL39; RD-P1-021 |
| BR7 | The ACE-shaped tables are a DEV test double, never a data copy, and no service table is loaded from them | No deviation row comes from `public`; this service holds no ACE table and no `v_ace_*` grant (DP-05 as a prohibition) | D-RCV-35 U1; NFR-045 |
| BR8 | No copy and no load table exists; every service reads source data only through the owner's contract or its own views | `rwb_deviation` holds `deviation` and nothing copied from another service, and the case reference is a fixture key | D-RCV-35; ADR-010 |
| BR9 | A clear identity number is allowed only in the ACE-shaped tables | `handler_user_id` is a synthetic user reference and the verifier blocks a real-looking value in `rwb_deviation` | D-RCV-35 U4; CTL-11 |

The rules applied to the seeded rows are rows of the DEV route set, not of this story: R-DEV-01 moves a deviation in any state to `DEV_FLAGGED` and is the state the seeder writes; R-DEV-02 assigns X1 to the complaint officer; R-DEV-03 assigns X2 and X3 to the specialist, with Legal joining X3 for the estate claim; R-DEV-04 assigns X4 to the fraud investigator (FSD S8 A2.4.3.1; TSD S8 T4). R-DEV-05 and R-DEV-06 are rows of the same set whose codes and owner roles no source read prints, so the smoke check evaluates them from the fixture and asserts no value of its own (GAP-3086; ASM-5265).

### 9. State transitions

None for a case: this story changes no case status, no clock and no contact stop of a running case. It changes the state of the rwb-deviation seed step in the pipeline.

| From | Event | Condition | To |
|---|---|---|---|
| not seeded for the commit | the seed step starts | A trigger fires, `rwb_sandbox` exists and the rwb-deviation seed lock is free | Seeding, in `rwb_deviation` |
| Seeding | the seeder and the verifier pass | Every check of section 4 steps 6 to 9 passes | Published: the transaction is committed |
| Seeding | any check fails | X1 to X8 | Failed: the transaction is rolled back and the rows of the previous run stay |
| Seeding | a second step starts | The seed lock is held | Waiting, then Seeding after the first ends |
| Published | a migration, dictionary or fixture change | A merge to main or a manual start | Seeding again |

The `deviation` rows themselves are written in one state and not transitioned: every seeded open row carries `state` "DEV_FLAGGED", the state R-DEV-01 leads to, and the owner of R-DEV-02 to R-DEV-06 is projected and compared, not applied. `DEV_WITH_OWNER`, `DEV_REJECTED`, `DEV_RESOLVED`, `DEV_REROUTE`, `RESUMED`, `ROUTE_D6` and `CASE_ENDED` are rows of the same set that only a live signal produces (TSD S8 T4), and no seeded row publishes the event that would produce one. `DEV_FLAGGED` is a state of the route set, not a value of LOV-RAISED-BY, and this story adds no value to LOV-RAISED-BY.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-TRIBE, tribe lead and squad members | Read and extract the deviation estate through the rwb-deviation DEV read-only role (name Pending under NEW-GAP-F17-2); start a manual seed run |
| RW-PLATADM, platform administrator | Owns the pipeline step and the build result; the shared database is created by the P1 build and is not dropped by any slice |
| Recovery tech lead | Owns the seed profile and shape table values published by RWB-P1-E1065-CON and the schema file properties |
| Test users per role | Call the DEV service against the sandbox with their role's rights; the write guard of AC6 refuses an identity without the Case record right U |
| RW-DATASTEW, data steward and data product owner | Owns the deviation data product and the dictionary rows the seeder reads |
| No approval level from the delegation of authority applies | The story takes no business decision |

The seed module and the service artefact are separated on purpose: the module runs in the pipeline under a build identity, the service runs in the cluster under the `rwb_deviation` login (DP-02), and no credential of either appears in a migration, a script or a runbook.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-CAS-036 | deviation (S8, `rwb_deviation`) | id | Write, a synthetic UUID |
| DF-CAS-037 | deviation (S8, `rwb_deviation`) | case_id | Write, from the test-only case-reference fixture until NEW-GAP-F17-1 names the published source |
| DF-CAS-038 | deviation (S8, `rwb_deviation`) | deviation_code | Write, from LOV-DEVIATION |
| DF-CAS-039 | deviation (S8, `rwb_deviation`) | raised_at | Write, from the business date of the seed |
| DF-CAS-040 | deviation (S8, `rwb_deviation`) | raised_by | Write, from LOV-RAISED-BY |
| DF-CAS-041 | deviation (S8, `rwb_deviation`) | paused_state | Write, the routed state of the case-reference fixture (NEW-GAP-F17-1) |
| DF-CAS-042 | deviation (S8, `rwb_deviation`) | handler_user_id | Write, a synthetic user reference |
| DF-CAS-043 | deviation (S8, `rwb_deviation`) | contact_stop | Write |
| DF-CAS-044 | deviation (S8, `rwb_deviation`) | cleared_at | Write, null while open |
| DF-CAS-045 | deviation (S8, `rwb_deviation`) | outcome | Write, from LOV-DEV-OUTCOME where set |
| Standard columns | deviation (S8, `rwb_deviation`) | `is_active`, `state`, `version`, `created_at`, `created_by`, `updated_at`, `updated_by` | Write |
| DF-REF-027, DF-REF-028, DF-REF-029 | lov_value (in the seeded dictionary) | id, lov_code, value_code | Read, the three lists at the version in force |
| DF-REF-097, DF-REF-098, DF-REF-105 | sys_fields (in the seeded dictionary) | field_name, data_type, is_personal | Read, the columns, their types and the personal flag |
| The seed rows | `case-seed-list.csv`, `shape-table.csv`, `seed-profile.json` (RWB-P1-E1065-CON) and the test-only case-reference fixture | shape_id, product_group, account_key, person_key, count, seed, case_id, routed state | Read from the files, never from `rwb_case` |

Field IDs are those of TSD S8 T3.1 and the Logical Data Model and Data Dictionary.

**What this story writes and what it does not.** It writes `deviation` rows and its own local decision record, and nothing else. It creates no table and no column: the dictionary additions it needs are the baseline's, and a dictionary change is a new migration on the service sequence (DP-15). No personal data is written beyond a synthetic user reference: no name, address, contact value or identity number enters a deviation row, and `handler_user_id` is a reference to a synthetic test user.

### 12. Contract

#### 12.1 REST operations provided

None. This story delivers a seed module and a pipeline step and publishes no operation. The two operations of the service — `POST /cases/{caseId}/deviations` (API-S8-001) and `PATCH /deviations/{deviationId}` (API-S8-002) — belong to the raise and clear stories of this service on base `/api/recovery/deviation/v1` (DP-13); AC6 asserts the guard of the write path against the sandbox and builds nothing of it.

#### 12.2 REST operations consumed

None. This story calls no operation of any service, at build time or at run time. It reads the versioned fixture files of the RWB-P1-E1065-CON contract package: `seed-profile.json`, `case-seed-list.csv`, `shape-table.csv` and the stage fixtures full, empty, refused and timeout (RD-P1-046). The package version is Pending (ASM-5690). The register of the lists is not called: LOV-DEVIATION, LOV-RAISED-BY and LOV-DEV-OUTCOME are rows of this service's dictionary, published in TSD S8 T3.2 and seeded with the baseline, so DP-07 applies as a rule of the seed and not as a call, and the C row of DP-07 (`RWB-P3-E1043-CON`) is not taken (GAP-3086; ASM-5262).

#### 12.3 Events published

None. A sandbox build is a pipeline run and not a business fact, so the seed writes no outbox row and publishes nothing. The two events of the service, `rwb.deviation.DeviationRaised.v1` (EV-06) and `rwb.deviation.DeviationCleared.v1` (EV-07) on `rwb.deviation.events.v1` (DP-14), belong to the raise and clear steps of the Epic 2 stories; the local decision record the seeder writes is a library write, not a Kafka write.

#### 12.4 Events consumed

None. The seed subscribes to no topic, holds no consumer group and writes no inbox row: it is a build step, and the inbox table of DP-09 is present in `rwb_deviation` for the consumers other stories of this service add.

#### 12.5 Workflows and activities

None. The seed step is a pipeline job and calls no Temporal workflow and no activity. `DeviationWorkflow` on queue `rwb-deviation` in namespace `rwb-recovery` is this service's and belongs to the raise, pause, handling and clear steps; the seed writes the state a raise leads to and starts no workflow.

#### 12.6 Schedules

**Pipeline stage**

| Item | Value |
|---|---|
| Trigger | Merge to main that changes a `rwb_deviation` migration, the dictionary, the pinned fixture package version or the case-reference fixture; manual start by RW-TRIBE or RW-PLATADM |
| Job name | rwb-deviation sandbox seed step, a DEV and pipeline test step of the rwb-deviation repository; not a scheduled job, not a Temporal Schedule and not in `job_catalog` |
| Schedule | On trigger only |
| Input | The shared `rwb_sandbox`; the rwb-deviation Flyway sequence; `sys_objects`, `sys_fields` and `lov_value`; `seed-profile.json`, `case-seed-list.csv`, `shape-table.csv` and the case-reference fixture |
| Output | Schema `rwb_deviation` of `rwb_sandbox` holding the synthetic `deviation` rows and their local decision records, the build report with the row count per table and the verifier result |
| Events published | None |
| Idempotency key | Commit hash, seed and fixture package version. The same values produce the same rows and the same counts |
| Restart behavior | The seed runs in one transaction on `rwb_deviation` under the rwb-deviation seed advisory lock; a failed run is rolled back and leaves the rows of the previous run; the database is never renamed or recreated |

The seed step is the only schedule this story has, and it is deliberately not a Temporal Schedule: it is a release activity, not a business timer. The service owns no job in the ownership rows (Jobs 0).

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| deviation | S8 (`rwb_deviation`) | Created by the baseline; rows written by the seeder and read by the verifier and the smoke check |
| local decision record (decision-record library) | PLT library, written in `rwb_deviation` | One record per seeded raise, first in the transaction (DP-03) |
| outbox_event | PLT library, created in `rwb_deviation` | Present; this story writes no row of it |
| processed_event | PLT library, created in `rwb_deviation` | Present for the consumers of other stories; no row written here |
| idempotency_key | PLT library, created in `rwb_deviation` | Present for the write operations; no row written here |

Not owned and never created or read as a table: `recovery_case`, `case_account`, `case_party` (P3), `interaction` (P1), `document`, `document_field` (P5), `rule_row` and `decision_log_entry` (P7), `agent_policy` (P10), and the ACE tables of schema `public`. No foreign key leaves `rwb_deviation`; `case_id` is a reference carried from the fixture (DP-01).

#### 12.8 Contract fakes

| Fake | Documents | Used by |
|---|---|---|
| RWB-P1-E1065-CON fixture files | `seed-profile.json`, `case-seed-list.csv`, `shape-table.csv` and the stage fixtures full, empty, refused and timeout; library path `fakes/rwb-source-data/<contract version>/` (ASM-5690), version Pending | AC1, AC4, AC5, AC11 |
| Dictionary fixture | The 10 `deviation` fields, the standard columns, LOV-DEVIATION, LOV-RAISED-BY and LOV-DEV-OUTCOME; a variant with no `sys_fields` row for `cleared_at`; a variant with an empty LOV-DEVIATION | AC2, AC3 |
| Case-reference fixture (test-only, of this module) | A synthetic `case_id` and routed state for each shaped row of `case-seed-list.csv`; a variant with a shaped row that has none (NEW-GAP-F17-1) | AC1, AC4, AC5 |
| Rule-package fixture | The DEV route set at its version in force with R-DEV-01 to R-DEV-06 and a variant where the owner of X1 is not the complaint officer | AC8 |
| Personal-data fixture | A 13-digit national ID with a valid check digit in `paused_state`; a clear identity number in `public.customer` | AC7 |
| Read-only role fixture | A granted SELECT on `rwb_deviation` for the rwb-deviation DEV read-only role, a refused UPDATE, and an identity without Case record right U | AC6 |
| rwb-source-data contract fake | Not used by this story: DP-05 applies as a prohibition, so no read through rwb-source-data is made; fake library version Not specified in the source documents (DOR-RWB-S8-E1065-APP-22) | none |

The fakes are test-only, are replaced by the real contracts in SIT, and carry no personal data: every deviation, case reference and user reference in them is synthetic.

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | None | None | No call to any service (RD-P1-046) |
| Kafka | None | None | `rwb.deviation.events.v1` belongs to the raise and clear stories |
| Temporal | None | None | A pipeline step, not a workflow; queue `rwb-deviation` is not used here |
| File | None | The RWB-P1-E1065-CON fixture files, the dictionary and case-reference fixtures, the CSV export | Read at build time; the export writes one CSV for the read-only role |
| SQL | `deviation` and the local decision record are seeded and read | `sys_fields`, `lov_value` in the sandbox | INSERT and SELECT only, in DEV only |

### 13. Solution plan

**Package.** Folder `tools/sandbox-generator`, Java package `th.co.scb.ace.workbench.recovery.deviation.sandbox`, a separate build module of the rwb-deviation repository that is never packaged into the service artefact. Service base `/api/recovery/deviation/v1` (not used here), schema `rwb_deviation` (owned by this service), shared sandbox database `rwb_sandbox` (created by the P1 build, never renamed or recreated by this story), topic `rwb.deviation.events.v1` (not published here), Temporal task queue `rwb-deviation` in namespace `rwb-recovery` (not used here).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `MetadataReader` | Service | Reads `sys_objects`, `sys_fields` and `lov_value` for `deviation`; a column with no dictionary row fails the build |
| `ShapeSeeder` | Service | Reads the fixture files and the case-reference fixture, selects the deviation shapes and maps each to its code in LOV-DEVIATION |
| `DeviationSeedGenerator` | Service | Writes one `deviation` row per shaped reference in foreign-key order, with its code, actor, paused state, contact stop, handler and state |
| `ValueFactory` | Service | Produces a value per data type and list, seeded; synthetic user references for `handler_user_id` |
| `DecisionRecordSeeder` | Service | Writes one local decision record per seeded raise through the decision-record library, before the row (DP-03) |
| `RuleSmokeCheck` | Service | Evaluates R-DEV-01 to R-DEV-06 in the embedded kit for every seeded row and compares the projected owner with the shape (DP-04) |
| `DeviationSeedVerifier` | Service | Counts per code, list values, contact stop, cleared date, reference resolution, personal-data pattern and schema boundary |
| `SandboxExport` | Service | Writes `deviation` to CSV for the read-only role |

**Database and migrations.** No new table and no new column from this story: the `deviation` table and its dictionary rows arrive with the per-service baseline of `rwb_deviation`, and this story's seed step applies that sequence with the rwb-deviation login (DP-15; RD-P1-046). The DEV grant script of the seed step grants SELECT on `rwb_deviation` to the rwb-deviation DEV read-only role (NEW-GAP-F17-2). The seeder writes rows only, and an applied migration is never edited: a dictionary addition is a new version on the service sequence.

**Configuration and reference data.** `rwb.sandbox.seed=20261128`, `rwb.sandbox.cases.mortgage=1226`, `rwb.sandbox.cases.hire-purchase=1296` and `rwb.sandbox.cases.ssme=290` are taken from `seed-profile.json`, the count per shape from `shape-table.csv`, and `rwb.sandbox.fixture` names the case-reference fixture; the three lists and the dictionary rows are read from the sandbox after the baseline (DP-07); the route set is held in the build fixture at its version in force (DP-04). No value of them is a constant of the module. The fixture package version of RWB-P1-E1065-CON is Pending (ASM-5690).

**Build steps**

1. `MetadataReader` over the dictionary, stopping on a column with no row (AC3, X1).
2. `ShapeSeeder` over the fixture files and the case-reference fixture, with X3 for the deceased shape and X5 for the bankruptcy shape (AC4).
3. `DeviationSeedGenerator` for the shaped references, one open row each, and the code coverage of X1 to X7 (AC1, AC2, AC4).
4. `DecisionRecordSeeder` for one local decision record per raise (AC8).
5. `RuleSmokeCheck` over the seeded rows in the embedded kit, with the owner comparison (AC8).
6. `DeviationSeedVerifier`, including the personal-data pattern scan and the schema-boundary test (AC1, AC2, AC7, X9).
7. `SandboxExport`, the DEV grant script and the grant assertion on `rwb_deviation` (AC6).
8. The seed step with the rwb-deviation seed lock, the single transaction, the rollback and the build report (AC5, AC9, AC11, AC12).
9. Tests for AC1 to AC12 and the access case in the pipeline.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision | H RWB-PLT-E1072-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

This is a secondary slice: the metadata "Depends on (build)" stays `None` and "Contract dependencies" stays `RWB-P1-E1065-CON` exactly as the Work Package fixes them, so the platform contracts that DP-03, DP-04, DP-07, DP-15 and DP-19 name arrive with the service template and are not written into the H row (GAP-3086; ASM-5263).

- **DP-01** is the subject: one schema, one table, one sequence, and a case reference carried as a fixture key. A statement on `rwb_case` or on a `v_ace_*` view fails the boundary test. `rwb_case` is owned by rwb-case and is named here only as a boundary; this service reads and writes none of it. **DP-15** puts the dictionary and the table on the service sequence, never in the shared baseline.
- **DP-03** is one local decision record per seeded raise, written by the library before the row, so a seeded deviation is a deviation with a record. **DP-04** is the smoke check: the package is held in the fixture at its version and evaluated in the embedded kit, so the sandbox proves the route set against real rows; no C row is taken because no rwb-decision operation is called.
- **DP-07** applies as a rule of the seed: the three lists are rows of this service's dictionary, published in TSD S8 T3.2, and no code value is written in the module; the C row of DP-07 is not taken for the same reason.
- **DP-05** applies as a prohibition: this service holds no `v_ace_*` grant and its slice needs no ACE product, so the seed writes nothing in schema `public` and reads nothing there.
- **DP-13** gives the sandbox's DEV service its base, and **DP-19** is the route a screen reads the seeded estate through; this story serves neither and builds neither. SCR-06 and SCR-08 are not built here, so this story specifies no empty, loading, error or no access state for them.

**Done when.** The tests of section 16 pass, `rwb_sandbox` holds the `deviation` rows for every shaped reference with the counts per code, every value is a value of the list in force, the dictionary-driven fill survives the test migration unchanged, the smoke check projects the owner of each code, the verifier blocks a personal value and a broken reference, the migration applies cleanly on an empty `rwb_deviation`, and no statement outside the schema exists in the build.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-002 | A test user without the Case record right U calls the deviation write operation on the sandbox (AC6) | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | A test user calls a sandbox case outside their scope | This case is not in your scope. |
| None | A seed or verifier failure (X1 to X8) | No message: the build report names the table, the column, the constraint, the list or the reference, and the previous sandbox stays |

The two message texts are the legacy texts, copied unchanged; they are raised by the guard library of rwb-access on the DEV service and this story raises no message of its own. Build failures are reported in the pipeline result with the failing object named, and the failure contract is RWB-P1-E1065-CON's. Errors on the write path are RFC 9457 problem responses with `messageId` and `detail`, and the HTTP mapping of MSG-P4-002 is 403 and of MSG-P4-003 is 403 or 404 as the case story fixes it.

### 15. Screens and states

No screen in this story. Developers and analysts read the deviation estate with SQL and the export script and see the build result and the row counts in the pipeline run.

The deviation screens of this service — SCR-06 Raise deviation and SCR-08 Deviation queue — show the seeded rows through the service in DEV, one hop through the gateway-bff composite route of DP-19, which merges the deviation answer of this service with the case state of rwb-case. Their states, their fields and their masking belong to those stories and to RWB-PLT-N001-CON; the seeded rows make every state of them demonstrable on Day 1. SCR-06 empty, loading, error and no access states: Not specified in the source documents (CG-ALL-11328). SCR-08 loading state: as in Screen Specifications v1 SCR-08; SCR-08 empty, error and no access states: Not specified in the source documents (CG-ALL-11329).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-S8-E1065-APP-01 | AC1 | End to end | AC1 The deviation slice of the sandbox exists (new, D-RCV-60) |
| TC-S8-E1065-APP-10 | AC2 | Component | AC2 Every seeded value is a value of the list in force (new, D-RCV-60) |
| TC-S8-E1065-APP-02 | AC3 | End to end | AC3 The seed follows the data dictionary (new, D-RCV-60) |
| TC-S8-E1065-APP-03 | AC4 | End to end | AC4 The exception shapes carry their deviation rows (new, D-RCV-60) |
| TC-S8-E1065-APP-04 | AC5 | End to end | AC5 The reset is idempotent (new, D-RCV-60) |
| TC-S8-E1065-APP-05 | AC6 | End to end | AC6 It is readable, extractable and not writable (new, D-RCV-60) |
| TC-S8-E1065-APP-06 | AC7 | End to end | AC7 No clear personal value in the deviation slice (new, D-RCV-60) |
| TC-S8-E1065-APP-11 | AC8 | Component | AC8 The seeded deviations pass the rules smoke check (new, D-RCV-60) |
| TC-S8-E1065-APP-07 | AC9 | End to end | AC9 Two seed steps started together wait on the seed lock (new, D-RCV-60) |
| TC-E1-065-12 | Section 12.7 table boundary: the owned tables of `rwb_deviation` only, with no statement on another service's table or a `v_ace_*` view | End to end | The baseline of rwb_deviation; a statement on `rwb_case` or on a `v_ace_*` view |
| TC-S8-E1065-APP-08 | AC10 | End to end | AC10 The rules of section 8 hold on the built sandbox (new, D-RCV-60) |
| TC-E1-065-15 | AC11: a consumed call that fails or does not answer stops the build before any row is written | End to end | Stage contract mock and dictionary fixture set to not answer, then to return an error |
| TC-S8-E1065-APP-09 | AC12 | End to end | AC12 The seed stays inside its own schema of the shared sandbox (new, RD-P1-046) |

The ten legacy cases of RWB-E1-065 are kept in order with the Level column added, and each names the slice of the deviation estate this story answers: the seeded rows and their shapes for TC-E1-065-01 and TC-S8-E1065-APP-11, the lists for TC-E1-065-06, the dictionary for TC-E1-065-03 and TC-E1-065-04, the reset for TC-E1-065-05 and TC-E1-065-09, the personal-data check for TC-E1-065-07, and the read and the refusal for TC-S8-E1065-APP-10 and TC-E1-065-10. The legacy table publishes no level, so one is assigned per case: legacy "System" maps to End to end because the stage spans schemas and fixtures, and "Access" maps to Component (GAP-3086; ASM-5267). The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same ID. No `-ITG` copy is written here: the same values across rwb-case, rwb-deviation and rwb-source-data are RWB-ITG-E1065-ITG's.


### 17. Guardrails

- No business value in code: the seed, the volumes and the shape counts come from the fixture files of RWB-P1-E1065-CON, and every code, actor value, outcome and state is a row of the dictionary and the lists. A build check fails on a code, a list value or a state in the source.
- No personal data in logs, tests, events or prompts: every case reference, user reference and value is synthetic, and the verifier blocks a value that looks real in `rwb_deviation`.
- ACE data only through the owner's contract or a `v_ace_*` view: this service holds no `v_ace_*` grant, reads no ACE table and needs no ACE product, so the seed writes nothing in schema `public`.
- No cross-schema read and no cross-schema key: `deviation` is the whole estate, `case_id` is a reference to the fixture, and a statement on `rwb_case`, `rwb_document` or a `v_ace_*` view fails the boundary test (DP-01).
- No copy and no load table: the 20 tables that left the schema are absent from `rwb_deviation`, and no row of it is loaded from `public` or from another service's table (DP-05, DP-17).
- One event owner per fact: the seed publishes nothing, and a build that writes an outbox row fails the acceptance test (DP-09 as a prohibition).
- The sandbox is in DEV and the pipeline test environment only and never reaches SIT, UAT or production; the seed step refuses any other target. The step never creates, drops, renames or recreates `rwb_sandbox` (RD-P1-046).
- An applied migration is never edited, and the dictionary changes by a new version on the service sequence (DP-15).
- No retired element is reintroduced: no Quartz row, no shared job table, no monolith base and no data-lake export.

### 18. Traceability

| Requirement ID | Feature | L3 process | Requirement (short) | Story element | Test cases |
|---|---|---|---|---|---|
| REQ-RDF-001 | Not specified in the source documents (DOR-RWB-S8-E1065-APP-2) | Not specified in the source documents (DOR-RWB-S8-E1065-APP-2) | 14 data products, each with one system of record and one owner (Business Requirements Epic 1, sections 3.1 and 4) | The deviation data product seeded in its owner's schema, with one row per shaped case reference | TC-E1-065-01, TC-S8-E1065-APP-11 |
| REQ-RDF-010 | Not specified in the source documents (DOR-RWB-S8-E1065-APP-2) | Not specified in the source documents (DOR-RWB-S8-E1065-APP-2) | Access per data product by role; personal data masked in line with PDPA (Program section 6.7; NFR-045) | The synthetic handler, the pattern scan and the read-only role | TC-S8-E1065-APP-10, TC-E1-065-07, TC-E1-065-10 |
| D-RCV-60 DP-01 | Not specified in the source documents (DOR-RWB-S8-E1065-APP-2) | Not specified in the source documents (DOR-RWB-S8-E1065-APP-2) | One schema per service; no other service's table is read or seeded | `deviation` in `rwb_deviation`; the boundary test | TC-E1-065-01, TC-E1-065-12 |
| D-RCV-60 DP-03 | Not specified in the source documents (DOR-RWB-S8-E1065-APP-2) | Not specified in the source documents (DOR-RWB-S8-E1065-APP-2) | A local decision record per change, through the library | `DecisionRecordSeeder` | TC-E1-065-01, TC-E1-065-11 |
| D-RCV-60 DP-04 | Not specified in the source documents (DOR-RWB-S8-E1065-APP-2) | Not specified in the source documents (DOR-RWB-S8-E1065-APP-2) | The rule set is evaluated in the embedded kit with the package in force | `RuleSmokeCheck` | TC-E1-065-01, TC-E1-065-11 |
| D-RCV-60 DP-07 | Not specified in the source documents (DOR-RWB-S8-E1065-APP-2) | Not specified in the source documents (DOR-RWB-S8-E1065-APP-2) | Lists are data, read at their version | LOV-DEVIATION, LOV-RAISED-BY, LOV-DEV-OUTCOME | TC-E1-065-03, TC-E1-065-06 |
| D-RCV-60 DP-15 | Not specified in the source documents (DOR-RWB-S8-E1065-APP-2) | Not specified in the source documents (DOR-RWB-S8-E1065-APP-2) | Per-service Flyway, no edit of an applied migration | The baseline the seed runs on | TC-E1-065-03 |

| Legacy reference | Where it is kept |
|---|---|
| Legacy story RWB-E1-065 — BR1, BR3, BR4, BR5, BR7, BR8, BR9; the seed properties and the volumes; the shape list; exception X5 (boundary) and X1 to X3 | Sections 3, 4, 5, 8, 9, 11, 13 |
| Legacy criteria AC1 to AC9 | Owned by RWB-P1-E1065-APP; the deviation half of AC1, AC2, AC3, AC4, AC5, AC7 and AC8 is re-proved here with new criteria (section 7) |
| TC-E1-065-01 to TC-E1-065-10 | Section 16 |
| MSG-P4-002, MSG-P4-003 | Section 14 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-P1-E1065-CON | Contract | C: the versioned fixture files this story reads (`seed-profile.json`, `case-seed-list.csv`, `shape-table.csv`, stage fixtures) |
| RWB-P1-E1065-APP | App development | Sibling primary slice: builds and seeds `public`, `recovery` and `rwb_source_data` and carries the nine legacy criteria; this story carries the deviation part only |
| RWB-P1-E1065-DB | ACE DB | Sibling: creates `rwb_sandbox` if absent with its three P1 schemas and `rwb_sandbox_read`; it grants nothing on `rwb_deviation` |
| RWB-P3-E1065-APP | App development | Sibling: seeds the case estate and assigns the case numbers; the published source of `case_id` for this slice is Pending (NEW-GAP-F17-1) |
| RWB-P5-E1065-APP | App development | Sibling: the document estate the deviation shapes use as evidence |
| RWB-ITG-E1065-ITG | Integration | The end-to-end proof of the sandbox values across the five services |

### 19. Out of scope

- The ACE schema test double, the 30 `v_ace_*` views, the P1 generator, the export tool and the nine legacy criteria: RWB-P1-E1065-APP.
- The stage contract and the published fixture files: RWB-P1-E1065-CON.
- The database `rwb_sandbox`, the schemas `public`, `recovery` and `rwb_source_data`, the role `rwb_sandbox_read` and its grants: RWB-P1-E1065-DB.
- The case estate: RWB-P3-E1065-APP. The document estate: RWB-P5-E1065-APP. The interaction rows: RWB-P1-E1065-APP. The role and permission rows: rwb-access (RD-P1-021).
- Raising, pausing, routing, contact stopping, handling and clearing a deviation, and the two write operations of the service: the Epic 2 and Epic 7 stories of this service (FEAT-DVH-01 to FEAT-DVH-09, FEAT-DVF-01 to FEAT-DVF-10).
- The deviation screens SCR-06 and SCR-08 and their states: the other stories of this service.
- Masked copies of production data in SIT and UAT (RWB-TE-004 in the legacy set), the rule scenario build gate (RWB-E1-073), the performance harness (RWB-TE-009) and the PDPA lint (RWB-TE-011).
- The ACE ingestion itself and the 14 Tier 2 tables: the ACE team owns them in RWB-ACE-001, and this story holds no ACE object.
- The dictionary content and its change process (RWB-E1-064 in the legacy set); the rule packages and their approval: rwb-decision (P7).
- The end-to-end proof of these values across rwb-case, rwb-deviation and rwb-source-data: RWB-ITG-E1065-ITG.

### 20. Remaining delivery steps

- Size the story at refinement (squad).
- Record the epic design sign-off (recovery tech lead).
- RWB-P1-E1065-CON Done and its fixture files published with a version (rwb-source-data contract owner).
- Close NEW-GAP-F17-1, the published source of `case_id` and routed state (rwb-case service owner with the data architect).
- Name the `rwb_deviation` DEV read-only role, NEW-GAP-F17-2 (platform DB owner).
- Add and update the test case rows in Test Cases v9 and the RTM (test lead).
- Load the synthetic data in DEV (platform administrator).
