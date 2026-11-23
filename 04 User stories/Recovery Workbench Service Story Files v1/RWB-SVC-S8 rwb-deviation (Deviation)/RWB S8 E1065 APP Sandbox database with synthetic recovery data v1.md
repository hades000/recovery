# RWB-S8-E1065-APP Sandbox database with synthetic recovery data

SCB Collections and Recovery. Henka Group, 22 November 2026.
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
| Depends on (build) | None |
| Contract dependencies | RWB-P1-E1065-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S8 rwb-deviation v1.md (no FR mapped to REQ-RDF-001, REQ-RDF-010) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-065 for rwb-deviation. The monolith seeded 92 tables in one `recovery` schema from one pipeline stage; in the target every service seeds its own slice, in its own schema, and reads no other service's table (DP-01). This story is the deviation slice of the sandbox: the `deviation` table of `rwb_deviation` filled with synthetic deviations X1 to X7 attached to the synthetic cases by business key, driven by the data dictionary and the lists of values, verified, and exercised once in the embedded Drools kit. It is a secondary slice of the legacy key: the nine legacy acceptance criteria and the generator, verifier, export tool and stage itself stay word for word with RWB-P1-E1065-APP, the stage contract is RWB-P1-E1065-CON, and this story owns no legacy criterion. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **recovery developer (RW-TRIBE)**, I want **the rwb-deviation slice of the DEV sandbox — `deviation` in `rwb_deviation` filled with synthetic deviations X1 to X7 on the seeded synthetic cases, every value drawn from the data dictionary and the lists of values in force and never from production data**, so that **I can build and test every deviation pause, contact stop, route and clear against a realistic deviation estate from Day 1, before SIT is connected and without a copy of source data**.

This story delivers, inside `rwb-deviation` only:

- the `deviation-seed` module of `tools/sandbox-generator`, Java package `th.co.scb.ace.workbench.recovery.deviation.sandbox`, a separate build module that is never packaged into the service artefact;
- `DeviationSeedGenerator`, `ShapeSeeder`, `DecisionRecordSeeder`, `RuleSmokeCheck`, `DeviationSeedVerifier` and `SandboxExport` (section 13);
- the seed profile values as data — seed 20261128, the three product volumes and a shape count of 10, all from the stage contract and every one overridable;
- the dictionary-driven fill of `deviation` (DP-01), the list values read as rows and never as code (DP-07), one local decision record per seeded raise through the decision-record library (DP-03) and one embedded-kit evaluation of R-DEV-01 to R-DEV-06 per seeded row (DP-04).

It does not build the sandbox stage, the ACE schema test double, the 30 `v_ace_*` views, the read-only role or the grants — those are RWB-P1-E1065-APP and RWB-P1-E1065-DB, whose contract RWB-P1-E1065-CON is this story's C dependency. It does not seed the case estate, the interactions or the documents: those are RWB-P3-E1065-APP and RWB-P5-E1065-APP, and this story consumes the case references they publish through the seed profile and reads none of their tables (GAP-3086; ASM-5261).

### 2. Business rationale

DEV has no ACE database and no case data, so before the sandbox no squad could test a source read, a case list or a report (legacy section 2). The realignment changes who seeds what: the recovery schema of 92 tables becomes 19 schemas with one owner each, and no service may seed or read another service's tables (DP-01, DP-02). The deviation estate is the clearest case of that rule — `deviation` is S8's single table, and its rows are the only thing in the whole sandbox that a deviation screen, the pause of a stage clock, a contact stop or a route decision can be tested against (context pack ownership rows; TSD S8 T3.1).

Three facts shape the slice.

1. **The shapes are the point.** Legacy BR4 asks for 10 cases of each exception shape, and three of the ten are deviations: an open deviation, a deceased customer and a bankruptcy. The deceased shape is the one the architecture uses as its worked example — X3 raised, the stage clock paused, the prescription clock still running, contact stopped (Architecture v5 slide 8; FSD S8 A2.12). Without those rows no test of R-DEV-01, of the contact stop of X1 to X3 or of the return point is possible.
2. **Every value is data.** Legacy BR3 and BR5 fix it: volumes, seed and shapes are properties and values come from the dictionary and the lists, so a schema change reaches the sandbox with no manual rebuild. In the target the same rule is DP-01 and DP-15: the fill reads `sys_fields` and `lov_value` and writes the service's own schema on its own Flyway sequence.
3. **No production data, no personal data.** Legacy BR1, BR7 and BR9 serve REQ-RDF-010: the deviation slice holds synthetic rows only, and the verifier blocks a value that looks real. `handler_user_id` is a synthetic user reference, because a deviation names its handler and the handler is a person.

The slice therefore serves REQ-RDF-001 (the deviation data product with one system of record and one owner — this service, in `rwb_deviation`) and REQ-RDF-010 (no personal data outside its permitted use). It changes no rule, no list and no state of the DEV route set.

### 3. Preconditions

- The per-service Flyway baseline of `rwb_deviation` has run: `deviation` exists with DF-CAS-036 to DF-CAS-045 and the standard record columns of TSD S8 T3.0, and the outbox, inbox and idempotency tables of the platform event library are in the schema (DP-15).
- RWB-P1-E1065-CON is published: the stage contract, the seed profile schema, the database and read-only-role contract and the failure contract. This story builds against its fake; the operation names and field names beyond the four rows of section 12.2 are Not specified in the source documents (GAP-3086; ASM-5263).
- The dictionary rows for `deviation` and the three lists are present in the sandbox after the stage's baseline, seeded from the Logical Data Model and Data Dictionary v8 and TSD S8 T3.2; the seeder validates every code against those rows at seed time and never against a constant (ASM-5262).
- The case-reference fixture of the seed profile lists the 2,812 synthetic case references of the stage — 1,226 MORTGAGE, 1,296 HIRE_PURCHASE and 290 SSME (10 percent of the 30 June 2026 inventory; DL15) — with the 10 references of each exception shape and the routed state each paused in. This story reads that fixture and never a table of rwb-case (ASM-5261).
- The stage properties are readable: `rwb.sandbox.seed=20261128`, the three volumes, `rwb.sandbox.shape-count=10` (legacy section 13). Every value is overridable and none is a constant of the module.
- A PostgreSQL 17 instance reachable from the pipeline exists in DEV, and the stage creates `rwb_sandbox_next` and renames it to `rwb_sandbox` under one advisory lock (RWB-P1-E1065-CON).
- The embedded Drools kit of RWB-PLT-E1072-CON is on the service template, and the DEV route set is held in the build fixture at its version in force (DP-04; ASM-5263).
- The decision-record library of RWB-PLT-E1027-CON is on the service template; the outbox relay is not started in DEV, so a seeded decision record stays local to `rwb_deviation` (DP-03).
- No approval is needed to build against a Draft contract baseline; the contract is tagged by RWB-P1-E1065-CON when its tests pass.

### 4. Flow

1. Pipeline: on a merge to main that changes a file under the `rwb_deviation` migration folder, the dictionary, the seed profile or the case-reference fixture, or on a manual start by RW-TRIBE or RW-PLATADM, the stage runs in DEV.
2. Stage: creates `rwb_sandbox_next` with the three schemas of the stage contract — `public` as the ACE test double, `recovery` for the read-only views, `rwb_deviation` for this service (RWB-P1-E1065-CON).
3. Stage: applies the ACE schema DDL and the Tier 2 DDL fixture into `public`, the per-service Flyway baseline of `rwb_deviation` (with the dictionary rows and the three lists) and the view migrations of the sandbox (DP-15).
4. `MetadataReader`: reads `sys_objects`, `sys_fields` and `lov_value` to learn every column, type and list of `deviation`; a column with no `sys_fields` row stops the seed and names the table and the column (legacy X1, AC4).
5. `ShapeSeeder`: reads the case-reference fixture, selects the references marked with an exception shape, and maps each deviation shape to its code as the sources publish it — the deceased customer to X3 (FSD S8 A2.12; Architecture v5 slide 8) and the bankruptcy to X5 (FSD S8 A2.14) — while the open-deviation shape and the four remaining codes take their code from LOV-DEVIATION at the version in force (ASM-5264).
6. `DeviationSeedGenerator`: writes one `deviation` row per shaped reference, in foreign-key order, with `case_id` as the fixture's business key, `deviation_code` from the shape, `raised_at` from the business date of the seed, `raised_by` from LOV-RAISED-BY, `paused_state` from the routed state the fixture gives the case, `handler_user_id` a synthetic user reference, `contact_stop` true for X1 to X3, `cleared_at` and `outcome` null while open, and `state` "DEV_FLAGGED" as R-DEV-01 leads (TSD S8 T4).
7. `DecisionRecordSeeder`: writes one local decision record per seeded raise through the decision-record library, first in the transaction, naming R-DEV-01 and the package version in force; no outbox row is written because no relay runs in DEV (DP-03).
8. `RuleSmokeCheck`: evaluates R-DEV-01 and the owner-assignment rules R-DEV-02 to R-DEV-06 in the embedded kit for every seeded row, compares the projected owner with the shape, and fails the build on a mismatch (DP-04).
9. `DeviationSeedVerifier`: row count per code, list values at the version in force, contact stop on X1 to X3, `cleared_at` on open and cleared rows, every case reference present in the fixture, the personal-data pattern scan, and the absence of any table of another service in `rwb_deviation`.
10. Stage: renames `rwb_sandbox_next` to `rwb_sandbox`, applies the grant of the read-only role of the stage contract, and publishes the build report with the row count per table and the verifier result; a developer or analyst then queries the sandbox with SQL or the export script.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A `deviation` column has no `sys_fields` row | The build fails naming the table and the column; the previous sandbox stays in use | None (pipeline result) | AC3 |
| X2 | The build runs twice for the same commit and seed | The schema is dropped and recreated; the same seed gives the same rows and counts | None | AC5 |
| X3 | A generated value breaks a constraint | The build fails naming the table and the constraint; the previous sandbox stays in use | None (pipeline result) | AC2 |
| X4 | A generated value in `rwb_deviation` matches a personal data pattern | The build fails naming the table and the column; no sandbox is published | None (pipeline result) | AC7 |
| X5 | A shaped case reference resolves to no case in the fixture | The build fails naming the reference; the previous sandbox stays in use | None (pipeline result) | AC4 |
| X6 | A second build starts while one runs | The second build waits on the stage's advisory lock and runs after the first | None | AC5 |
| X7 | A list in force is empty or the list rows are not readable | The build fails closed before a row is written and names the list; the module never falls back to a constant or to a copy of a list | None (pipeline result) | AC2 |
| X8 | The case-reference fixture is absent or holds no shaped reference | The build stops before the seed and publishes nothing, because this story owns no case reference of its own | None (pipeline result) | AC1, AC4 |
| X9 | A component, a statement or a test reaches `rwb_case`, a `v_ace_*` view or another service's schema | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | Section 17, AC1 |

X1 to X6 are the exception paths of RWB-E1-065 carried onto the deviation slice; X7 to X9 are the paths the split adds, one for the lists, one for the case references this service does not own, and one for the schema boundary.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds on Day 1 against the RWB-P1-E1065-CON fake, the dictionary rows of its own schema and the case-reference fixture, and waits for no in-lane story |
| Negotiable | The component names, the fixture shape and the verifier's message wording are this story's; the codes, the lists, the seed and the volumes are rows and properties |
| Valuable | Every deviation read, pause, contact stop, route and clear is testable in DEV from the first day, with no production data and no other team's data |
| Estimable | One seed module, one shape seeder, one decision-record step, one smoke check, one verifier and one export path |
| Small | Fits one sprint as the secondary slice of the legacy key, beside RWB-P1-E1065-APP, RWB-P3-E1065-APP and RWB-P5-E1065-APP |
| Testable | Every criterion is a query against the built schema, a build-failure case or one embedded-kit evaluation |

### 7. Acceptance criteria

```gherkin
Feature: Sandbox database with synthetic recovery data — the rwb-deviation slice

  Background:
    Given the RWB-P1-E1065-CON stage contract mock returns the seed profile with seed 20261128, 1,226 Mortgage, 1,296 Hire purchase and 290 SSME case references, a shape count of 10 and the case-reference fixture
    Given the dictionary fixture returns the 10 fields of deviation (DF-CAS-036 to DF-CAS-045) and LOV-DEVIATION with X1 to X7, LOV-RAISED-BY and LOV-DEV-OUTCOME at the version in force

  Scenario: AC1 The deviation slice of the sandbox exists (new, D-RCV-60)
    Given the per-service baseline of rwb_deviation has run and the stage holds the case-reference fixture
    When the sandbox build runs
    Then schema rwb_deviation holds deviation with its 10 fields and the standard record columns
    Then every shaped reference of the fixture carries one deviation row and no row exists for a reference the fixture does not list
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
    Then a dictionary fixture without the sys_fields row for deviation.cleared_at fails the build with "deviation.cleared_at has no data dictionary entry" and the previous sandbox stays in use

  Scenario: AC4 The exception shapes carry their deviation rows (new, D-RCV-60)
    Given the case-reference fixture marks 10 references for each shape of legacy BR4, among them the deceased shape, the bankruptcy shape and the open-deviation shape
    When the build completes
    Then each deceased reference carries deviation "X3" with contact_stop true
    Then each bankruptcy reference carries deviation "X5" with contact_stop false
    Then each open-deviation reference carries one open row whose code is in LOV-DEVIATION and whose cleared_at is null
    Then the estate holds at least one open deviation of every code X1 to X7
    Then a shaped reference that resolves to no case in the fixture fails the build and names the reference

  Scenario: AC5 The reset is idempotent (new, D-RCV-60)
    Given the sandbox was built for commit "a1b2c3d" with seed 20261128
    When the build runs again for commit "a1b2c3d" and seed 20261128
    Then a fresh rwb_sandbox_next with a fresh rwb_deviation schema is built and swapped in
    Then deviation holds the same row count and the same count per code
    Then case reference "RW-2026-000001" holds the same deviation code and the same raised_at
    Then no row from the first build remains
    Then a second build that starts while one runs waits on the stage lock and runs after the first

  Scenario: AC6 It is readable, extractable and not writable (new, D-RCV-60)
    Given the sandbox and the read-only role of the stage contract
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
    Then the system publishes no sandbox from that build
    Then handler_user_id holds a synthetic user reference and no name, contact value or identity number

  Scenario: AC8 The seeded deviations pass the rules smoke check (new, D-RCV-60)
    Given the DEV route set at its version in force, with R-DEV-01 and R-DEV-02 to R-DEV-06, held in the build fixture
    When the smoke check runs in the embedded kit after the seed
    Then every seeded open deviation satisfies R-DEV-01 and is recorded in state "DEV_FLAGGED"
    Then the owner projected for code "X1" is the complaint officer "RW-COMPLAIN" from R-DEV-02 and for code "X4" the fraud investigator "RW-FRAUD" from R-DEV-04
    Then one local decision record per seeded raise exists in rwb_deviation, written before the row, and no rwb.deviation.events.v1 event is published
    Then a mismatch between a seeded row and the rule outcome fails the build
```

The eight criteria are new, tagged "(new, D-RCV-60)", and test only the deviation slice of the sandbox. The nine legacy criteria of RWB-E1-065 are owned word for word by RWB-P1-E1065-APP, which carries the stage, the generator and all nine; this story owns none of them. The values reused here are the ones the sources publish: seed 20261128 and the three volumes (legacy BR5, DL15), the shape count 10 (legacy BR4), the codes X1 to X7 and the three lists (TSD S8 T3.2), X3 as the deceased customer (FSD S8 A2.12; Architecture v5 slide 8), X5 as the bankruptcy (FSD S8 A2.14), the contact stop on X1 to X3 (FSD S8 A2.5; Architecture v5 slide 8) and "RW-FRAUD" for X4 (legacy AC4). Two points are recorded rather than smoothed over: the case references come from the seed profile and not from rwb-case (GAP-3086; ASM-5261), and the number of deviations per case is not published (ASM-5264).

### 8. Business rules

| ID | Rule | What this story does with it | Source |
|---|---|---|---|
| BR1 | No production data in DEV; the sandbox holds synthetic data only | The seeder writes synthetic rows only, on synthetic case references | NFR-045; CTL-11 |
| BR2 | The sandbox is built from the same DDL as SIT | The stage applies the ACE DDL and the per-service baseline of `rwb_deviation`; this slice seeds only what its own migrations created (DP-15) | RWB-E1-001; RWB-E1-069; ADR-001 |
| BR3 | Generated values come from the data dictionary and the lists of values, not from code | `MetadataReader` and `ValueFactory` read `sys_fields` and `lov_value`; a code, a list value or a state is never a constant (DP-07) | sys_fields; lov_value; Principle 1 |
| BR4 | Exception shapes generated: duplicate case for one customer and product (R-UNI-17), deceased customer (R-UNI-05), bankruptcy (R-UNI-07), open deviation, legal hold (R-UNI-20), unmapped product code, collateral with no account, case with three accounts, accounts at 89 and 90 days past due (DL16), withdrawn consent (R-UNI-10) | Carries the three deviation shapes of the ten — open deviation, deceased X3, bankruptcy X5 — and asserts them; the other seven are the case estate's (RWB-P3-E1065-APP) | rules.txt; DL16 |
| BR5 | Case volumes follow the product split of the 30 June 2026 inventory at 10 percent | Reads the volumes from the seed profile; seeds no case and counts its own rows per code | DL15 |
| BR6 | Every role has a named test user before it has real users | Not seeded here: roles, permissions and test users are the reference data of rwb-case and rwb-access, and the stage seeds them | DL39 |
| BR7 | The ACE-shaped tables are a DEV test double, never a data copy, and no service table is loaded from them | No deviation row comes from `public`; this service holds no ACE table and no `v_ace_*` grant (DP-05 as a prohibition) | D-RCV-35 U1; NFR-045 |
| BR8 | No copy and no load table exists; every service reads source data only through the owner's contract or its own views | `rwb_deviation` holds `deviation` and nothing copied from another service, and the case reference is a fixture key | D-RCV-35; ADR-010 |
| BR9 | A clear identity number is allowed only in the ACE-shaped tables | `handler_user_id` is a synthetic user reference and the verifier blocks a real-looking value in `rwb_deviation` | D-RCV-35 U4; CTL-11 |

The rules applied to the seeded rows are rows of the DEV route set, not of this story: R-DEV-01 moves a deviation in any state to `DEV_FLAGGED` and is the state the seeder writes; R-DEV-02 assigns X1 to the complaint officer; R-DEV-03 assigns X2 and X3 to the specialist, with Legal joining X3 for the estate claim; R-DEV-04 assigns X4 to the fraud investigator (FSD S8 A2.4.3.1; TSD S8 T4). R-DEV-05 and R-DEV-06 are rows of the same set whose codes and owner roles no source read prints, so the smoke check evaluates them from the fixture and asserts no value of its own (GAP-3086; ASM-5265).

### 9. State transitions

None for a case: this story changes no case status, no clock and no contact stop of a running case. It changes the sandbox build state in the pipeline.

| From | Event | Condition | To |
|---|---|---|---|
| no sandbox for the commit | the stage starts | A trigger fires and the advisory lock is free | Building, in `rwb_sandbox_next` |
| Building | the seeder and the verifier pass | Every check of section 4 steps 6 to 9 passes | Published: `rwb_sandbox_next` is renamed to `rwb_sandbox` |
| Building | any check fails | X1 to X8 | Failed: the previous `rwb_sandbox` stays in use |
| Building | a second build starts | The advisory lock is held | Waiting, then Building after the first ends |
| Published | a migration, dictionary, seed or fixture change | A merge to main or a manual start | Building again |

The `deviation` rows themselves are written in one state and not transitioned: every seeded open row carries `state` "DEV_FLAGGED", the state R-DEV-01 leads to, and the owner of R-DEV-02 to R-DEV-06 is projected and compared, not applied. `DEV_WITH_OWNER`, `DEV_REJECTED`, `DEV_RESOLVED`, `DEV_REROUTE`, `RESUMED`, `ROUTE_D6` and `CASE_ENDED` are rows of the same set that only a live signal produces (TSD S8 T4), and no seeded row publishes the event that would produce one.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-TRIBE, tribe lead and squad members | Read and extract the deviation estate through the read-only role of the stage contract; start a manual build |
| RW-PLATADM, platform administrator | Owns the sandbox database, the pipeline stage and the build result |
| Recovery tech lead | Owns the seed profile, the seed value, the shape count and the schema file properties |
| Test users per role | Call the DEV service against the sandbox with their role's rights; the write guard of AC6 refuses an identity without the Case record right U |
| RW-DATASTEW, data steward and data product owner | Owns the deviation data product and the dictionary rows the seeder reads |
| No approval level from the delegation of authority applies | The story takes no business decision |

The seed module and the service artefact are separated on purpose: the module runs in the pipeline under a build identity, the service runs in the cluster under the `rwb_deviation` login (DP-02), and no credential of either appears in a migration, a script or a runbook.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-CAS-036 | deviation (S8, `rwb_deviation`) | id | Write, a synthetic UUID |
| DF-CAS-037 | deviation (S8, `rwb_deviation`) | case_id | Write, the business key of the fixture |
| DF-CAS-038 | deviation (S8, `rwb_deviation`) | deviation_code | Write, from LOV-DEVIATION |
| DF-CAS-039 | deviation (S8, `rwb_deviation`) | raised_at | Write, from the business date of the seed |
| DF-CAS-040 | deviation (S8, `rwb_deviation`) | raised_by | Write, from LOV-RAISED-BY |
| DF-CAS-041 | deviation (S8, `rwb_deviation`) | paused_state | Write, the routed state of the fixture |
| DF-CAS-042 | deviation (S8, `rwb_deviation`) | handler_user_id | Write, a synthetic user reference |
| DF-CAS-043 | deviation (S8, `rwb_deviation`) | contact_stop | Write |
| DF-CAS-044 | deviation (S8, `rwb_deviation`) | cleared_at | Write, null while open |
| DF-CAS-045 | deviation (S8, `rwb_deviation`) | outcome | Write, from LOV-DEV-OUTCOME where set |
| Standard columns | deviation (S8, `rwb_deviation`) | `is_active`, `state`, `version`, `created_at`, `created_by`, `updated_at`, `updated_by` | Write |
| DF-REF-027, DF-REF-028, DF-REF-029 | lov_value (in the seeded dictionary) | id, lov_code, value_code | Read, the three lists at the version in force |
| DF-REF-097, DF-REF-098, DF-REF-105 | sys_fields (in the seeded dictionary) | field_name, data_type, is_personal | Read, the columns, their types and the personal flag |
| The case reference | case-reference fixture (P3's estate, read as a fixture) | case reference, product group, shape, routed state | Read from the seed profile, never from `rwb_case` |

Field IDs are those of TSD S8 T3.1 and the Logical Data Model and Data Dictionary.

**What this story writes and what it does not.** It writes `deviation` rows and its own local decision record, and nothing else. It creates no table and no column: the dictionary additions it needs are the baseline's, and a dictionary change is a new migration on the service sequence (DP-15). No personal data is written beyond a synthetic user reference: no name, address, contact value or identity number enters a deviation row, and `handler_user_id` is a reference to a synthetic test user.

### 12. Contract

#### 12.1 REST operations provided

None. This story delivers a seed module and a pipeline stage and publishes no operation. The two operations of the service — `POST /cases/{caseId}/deviations` (API-S8-001) and `PATCH /deviations/{deviationId}` (API-S8-002) — belong to the raise and clear stories of this service on base `/api/recovery/deviation/v1` (DP-13); AC6 asserts the guard of the write path against the sandbox and builds nothing of it.

#### 12.2 REST operations consumed

One contract read at build time; no runtime call.

| Operation | Path | Owner | Use |
|---|---|---|---|
| The stage, seed-profile and failure contract read of RWB-P1-E1065-CON (operation name and field names Not specified in the source documents (GAP-3086; ASM-5263)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | The seed profile, the three volumes, the shape count, the case-reference fixture, the database and read-only-role contract and the failure contract, at build time; faked |

One row, one hop, no retry beyond the client default, and read once per build. The register of the lists is not called: LOV-DEVIATION, LOV-RAISED-BY and LOV-DEV-OUTCOME are rows of this service's dictionary, published in TSD S8 T3.2 and seeded with the baseline, so DP-07 applies as a rule of the seed and not as a call, and the C row of DP-07 (`RWB-P3-E1043-CON`) is not taken (GAP-3086; ASM-5262).

#### 12.3 Events published

None. A sandbox build is a pipeline run and not a business fact, so the seed writes no outbox row and publishes nothing. The two events of the service, `rwb.deviation.DeviationRaised.v1` (EV-06) and `rwb.deviation.DeviationCleared.v1` (EV-07) on `rwb.deviation.events.v1` (DP-14), belong to the raise and clear steps of the Epic 2 stories; the local decision record the seeder writes is a library write, not a Kafka write.

#### 12.4 Events consumed

None. The seed subscribes to no topic, holds no consumer group and writes no inbox row: it is a build step, and the inbox table of DP-09 is present in `rwb_deviation` for the consumers other stories of this service add.

#### 12.5 Workflows and activities

None. The stage is a pipeline job and calls no Temporal workflow and no activity. `DeviationWorkflow` on queue `rwb-deviation` in namespace `rwb-recovery` is this service's and belongs to the raise, pause, handling and clear steps; the seed writes the state a raise leads to and starts no workflow.

#### 12.6 Schedules

**Pipeline stage**

| Item | Value |
|---|---|
| Trigger | Merge to main that changes a `rwb_deviation` migration, the dictionary, the seed profile or the case-reference fixture; manual start by RW-TRIBE or RW-PLATADM |
| Job name | Sandbox build, a DEV pipeline stage of the rwb-deviation repository; not a scheduled job, not a Temporal Schedule and not in `job_catalog` |
| Schedule | On trigger only |
| Input | The ACE schema DDL and the Tier 2 DDL fixture; the per-service Flyway baseline and view migrations; `sys_objects`, `sys_fields` and `lov_value`; the seed profile and the case-reference fixture of RWB-P1-E1065-CON |
| Output | Database `rwb_sandbox` with schema `rwb_deviation` holding the synthetic `deviation` rows and their local decision records, the build report with the row count per table and the verifier result |
| Events published | None |
| Idempotency key | Commit hash and seed. The same pair produces the same rows and the same counts |
| Restart behavior | The build works on `rwb_sandbox_next` and renames it only after the verifier passes, under one advisory lock; a failed build leaves the previous sandbox |

The stage is the only schedule this story has, and it is deliberately not a Temporal Schedule: it is a release activity, not a business timer. The service owns no job in the ownership rows (Jobs 0).

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
| RWB-P1-E1065-CON stage fake | Seed 20261128, the three volumes, a shape count of 10, the case-reference fixture, the three-schema and read-only-role contract, and a failure contract | AC1, AC4, AC5, AC6 |
| Dictionary fixture | The 10 `deviation` fields, the standard columns, LOV-DEVIATION, LOV-RAISED-BY and LOV-DEV-OUTCOME; a variant with no `sys_fields` row for `cleared_at`; a variant with an empty LOV-DEVIATION | AC2, AC3 |
| Case-reference fixture | 2,812 references with their product group, shape and routed state; a shaped reference that resolves to no case; a fixture with no shaped reference | AC1, AC4 |
| Rule-package fixture | The DEV route set at its version in force with R-DEV-01 to R-DEV-06 and a variant where the owner of X1 is not the complaint officer | AC8 |
| Personal-data fixture | A 13-digit national ID with a valid check digit in `paused_state`; a clear identity number in `public.customer` | AC7 |
| Read-only role fake | A granted SELECT on `rwb_deviation` for the sandbox role, a refused UPDATE, and an identity without Case record right U | AC6 |

The fakes are test-only, are replaced by the real contracts in SIT, and carry no personal data: every deviation, case reference and user reference in them is synthetic.

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | None | 1 contract read at build time (`/api/recovery/source-data/v1`, DP-19 library) | One hop; the operation name and field names are settled in RWB-P1-E1065-CON |
| Kafka | None | None | `rwb.deviation.events.v1` belongs to the raise and clear stories |
| Temporal | None | None | A pipeline stage, not a workflow; queue `rwb-deviation` is not used here |
| File | None | The dictionary and case-reference fixtures, the CSV export | Read at build time; the export writes one CSV for the read-only role |
| SQL | `deviation` and the local decision record are seeded and read | `sys_fields`, `lov_value` in the sandbox | INSERT and SELECT only, in DEV only |

### 13. Solution plan

**Package.** Folder `tools/sandbox-generator`, Java package `th.co.scb.ace.workbench.recovery.deviation.sandbox`, a separate build module of the rwb-deviation repository that is never packaged into the service artefact. Service base `/api/recovery/deviation/v1` (not used here), schema `rwb_deviation`, sandbox database `rwb_sandbox`, build database `rwb_sandbox_next`, topic `rwb.deviation.events.v1` (not published here), Temporal task queue `rwb-deviation` in namespace `rwb-recovery` (not used here).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `MetadataReader` | Service | Reads `sys_objects`, `sys_fields` and `lov_value` for `deviation`; a column with no dictionary row fails the build |
| `ShapeSeeder` | Service | Selects the shaped references of the fixture and maps each deviation shape to its code in LOV-DEVIATION |
| `DeviationSeedGenerator` | Service | Writes one `deviation` row per shaped reference in foreign-key order, with its code, actor, paused state, contact stop, handler and state |
| `ValueFactory` | Service | Produces a value per data type and list, seeded; synthetic user references for `handler_user_id` |
| `DecisionRecordSeeder` | Service | Writes one local decision record per seeded raise through the decision-record library, before the row (DP-03) |
| `RuleSmokeCheck` | Service | Evaluates R-DEV-01 to R-DEV-06 in the embedded kit for every seeded row and compares the projected owner with the shape (DP-04) |
| `DeviationSeedVerifier` | Service | Counts per code, list values, contact stop, cleared date, reference resolution, personal-data pattern and schema boundary |
| `SandboxExport` | Service | Writes `deviation` to CSV for the read-only role |

**Database and migrations.** No new table and no new column from this story: the `deviation` table and its dictionary rows arrive with the per-service baseline of `rwb_deviation`, and the sandbox stage applies that baseline (DP-15). The seeder writes rows only, and an applied migration is never edited: a dictionary addition is a new version on the service sequence.

**Configuration and reference data.** The stage properties `rwb.sandbox.seed=20261128`, `rwb.sandbox.cases.mortgage=1226`, `rwb.sandbox.cases.hire-purchase=1296`, `rwb.sandbox.cases.ssme=290`, `rwb.sandbox.shape-count=10` and `rwb.sandbox.fixture` come from RWB-P1-E1065-CON and are owned by the recovery tech lead; the three lists and the dictionary rows are read from the sandbox after the baseline (DP-07); the route set is held in the build fixture at its version in force (DP-04). No value of them is a constant of the module.

**Build steps**

1. `MetadataReader` over the dictionary, stopping on a column with no row (AC3, X1).
2. `ShapeSeeder` over the case-reference fixture, with X3 for the deceased shape and X5 for the bankruptcy shape (AC4).
3. `DeviationSeedGenerator` for the shaped references, one open row each, and the code coverage of X1 to X7 (AC1, AC2, AC4).
4. `DecisionRecordSeeder` for one local decision record per raise (AC8).
5. `RuleSmokeCheck` over the seeded rows in the embedded kit, with the owner comparison (AC8).
6. `DeviationSeedVerifier`, including the personal-data pattern scan and the schema-boundary test (AC1, AC2, AC7, X9).
7. `SandboxExport` and the read-only grant assertion of the stage contract (AC6).
8. The stage with `rwb_sandbox_next`, the advisory lock, the rename and the build report (AC5).
9. Tests for AC1 to AC8 and the access case in the pipeline.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision | H RWB-PLT-E1072-CON; C RWB-P7-E1073-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

This is a secondary slice: the metadata "Depends on (build)" stays `None` and "Contract dependencies" stays `RWB-P1-E1065-CON` exactly as the Work Package fixes them, so the platform contracts that DP-03, DP-04, DP-07, DP-15 and DP-19 name arrive with the service template and are not written into the H row (GAP-3086; ASM-5263).

- **DP-01** is the subject: one schema, one table, one sequence, and a case reference carried as a fixture key. A statement on `rwb_case` or on a `v_ace_*` view fails the boundary test. **DP-15** puts the dictionary and the table on the service sequence, never in the shared baseline.
- **DP-03** is one local decision record per seeded raise, written by the library before the row, so a seeded deviation is a deviation with a record. **DP-04** is the smoke check: the package is held in the fixture at its version and evaluated in the embedded kit, so the sandbox proves the route set against real rows; its C row (`RWB-P7-E1073-CON`) is not taken because no rwb-decision operation is called.
- **DP-07** applies as a rule of the seed: the three lists are rows of this service's dictionary, published in TSD S8 T3.2, and no code value is written in the module; the C row of DP-07 is not taken for the same reason.
- **DP-05** applies as a prohibition: this service holds no `v_ace_*` grant and its slice needs no ACE product, so the seed writes nothing in schema `public` and reads nothing there.
- **DP-13** gives the sandbox's DEV service its base, and **DP-19** is the route a screen reads the seeded estate through; this story serves neither and builds neither.

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

The deviation screens of this service — SCR-06 Raise deviation and SCR-08 Deviation queue — show the seeded rows through the service in DEV, one hop through the gateway-bff composite route of DP-19, which merges the deviation answer of this service with the case state of rwb-case. Their states, their fields and their masking belong to those stories and to RWB-PLT-N001-CON; the seeded rows make every state of them demonstrable on Day 1.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-065-01 | AC1 and AC4 for the deviation slice: the table, its fields, one row per shaped reference and no foreign table. The case, ACE and document halves belong to RWB-P3-E1065-APP, RWB-P1-E1065-APP and RWB-P5-E1065-APP | End to end | The baseline of rwb_deviation; seed 20261128; the case-reference fixture with 2,812 references plus shapes |
| TC-E1-065-02 | AC6: a read-only query by code, the CSV export and a refused UPDATE on `deviation` | End to end | Read-only role query grouped by deviation_code; CSV export; refused UPDATE |
| TC-E1-065-03 | AC3: the dictionary-driven fill on the deviation table | End to end | Test migration adding `deviation.deviation_band` with its dictionary row and LOV-DEV-BAND |
| TC-E1-065-04 | AC3: a column with no dictionary row fails the build | End to end | Dictionary fixture without the `sys_fields` row for `deviation.cleared_at` |
| TC-E1-065-05 | AC5: idempotent reset of the deviation slice, and the second build waits | End to end | Two builds for commit a1b2c3d and seed 20261128; a second build started with a1b2c3d |
| TC-E1-065-06 | AC2: list values at the version in force and a fail-closed empty list. The case-side column of the legacy case is RWB-P3-E1065-APP's | End to end | Empty LOV-DEVIATION seed; a value outside LOV-RAISED-BY |
| TC-E1-065-07 | AC7: the personal-data pattern scan and the synthetic handler | End to end | Injected 13-digit value in `deviation.paused_state`; a clear value in `public.customer` |
| TC-E1-065-08 | AC4: the exception shapes of the deviation estate, with X3 contact stopped and X5 not. The 89 and 90 days past due boundary is RWB-P3-E1065-APP's | End to end | 10 references per shape; deceased X3; bankruptcy X5; open deviation |
| TC-E1-065-09 | AC5: two builds at once wait on the stage lock | End to end | Two builds started together for a1b2c3d and e4f5a6b |
| TC-E1-065-10 | AC6: the write refusal of an identity without Case record right U | Component | Test user with RW-REFADM calls `POST /cases/{caseId}/deviations` on the sandbox; refused with 403 and MSG-P4-002 |

The ten legacy cases of RWB-E1-065 are kept in order with the Level column added, and each names the slice of the deviation estate this story answers: the seeded rows and their shapes for TC-E1-065-01 and TC-E1-065-08, the lists for TC-E1-065-06, the dictionary for TC-E1-065-03 and TC-E1-065-04, the reset for TC-E1-065-05 and TC-E1-065-09, the personal-data check for TC-E1-065-07, and the read and the refusal for TC-E1-065-02 and TC-E1-065-10. The legacy table publishes no level, so one is assigned per case: legacy "System" maps to End to end because the stage spans schemas and fixtures, and "Access" maps to Component (GAP-3086; ASM-5267). The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same ID. No `-ITG` copy is written here: the same values across rwb-case, rwb-deviation and rwb-source-data are RWB-ITG-E1065-ITG's.

### 17. Guardrails

- No business value in code: the seed, the volumes, the shape count and the fixture are properties of the stage contract, and every code, actor value, outcome and state is a row of the dictionary and the lists. A build check fails on a code, a list value or a state in the source.
- No personal data in logs, tests, events or prompts: every case reference, user reference and value is synthetic, and the verifier blocks a value that looks real in `rwb_deviation`.
- ACE data only through the owner's contract or a `v_ace_*` view: this service holds no `v_ace_*` grant, reads no ACE table and needs no ACE product, so the seed writes nothing in schema `public`.
- No cross-schema read and no cross-schema key: `deviation` is the whole estate, `case_id` is a reference to the fixture, and a statement on `rwb_case`, `rwb_document` or a `v_ace_*` view fails the boundary test (DP-01).
- No copy and no load table: the 20 tables that left the schema are absent from `rwb_deviation`, and no row of it is loaded from `public` or from another service's table (DP-05, DP-17).
- One event owner per fact: the seed publishes nothing, and a build that writes an outbox row fails the acceptance test (DP-09 as a prohibition).
- The sandbox is in DEV only and never reaches SIT, UAT or production; the stage contract's deployment gate refuses any other target.
- An applied migration is never edited, and the dictionary changes by a new version on the service sequence (DP-15).
- No retired element is reintroduced: no Quartz row, no shared job table, no monolith base and no data-lake export.

### 18. Traceability

| Requirement ID | Requirement (short) | Story element | Test cases |
|---|---|---|---|
| REQ-RDF-001 | 14 data products, each with one system of record and one owner (Business Requirements Epic 1, sections 3.1 and 4) | The deviation data product seeded in its owner's schema, with one row per shaped case reference | TC-E1-065-01, TC-E1-065-08 |
| REQ-RDF-010 | Access per data product by role; personal data masked in line with PDPA (Program section 6.7; NFR-045) | The synthetic handler, the pattern scan and the read-only role | TC-E1-065-02, TC-E1-065-07, TC-E1-065-10 |
| D-RCV-60 DP-01 | One schema per service; no other service's table is read or seeded | `deviation` in `rwb_deviation`; the boundary test | TC-E1-065-01 |
| D-RCV-60 DP-03 | A local decision record per change, through the library | `DecisionRecordSeeder` | TC-E1-065-01 |
| D-RCV-60 DP-04 | The rule set is evaluated in the embedded kit with the package in force | `RuleSmokeCheck` | TC-E1-065-01 |
| D-RCV-60 DP-07 | Lists are data, read at their version | LOV-DEVIATION, LOV-RAISED-BY, LOV-DEV-OUTCOME | TC-E1-065-03, TC-E1-065-06 |
| D-RCV-60 DP-15 | Per-service Flyway, no edit of an applied migration | The baseline the seed runs on | TC-E1-065-03 |

| Legacy reference | Where it is kept |
|---|---|
| Legacy story RWB-E1-065 — BR1, BR3, BR4, BR5, BR7, BR8, BR9; the seed properties and the volumes; the shape list; exception X5 (boundary) and X1 to X3 | Sections 3, 4, 5, 8, 9, 11, 13 |
| Legacy criteria AC1 to AC9 | Owned by RWB-P1-E1065-APP; the deviation half of AC1, AC2, AC3, AC4, AC5, AC7 and AC8 is re-proved here with new criteria (section 7) |
| TC-E1-065-01 to TC-E1-065-10 | Section 16 |
| MSG-P4-002, MSG-P4-003 | Section 14 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-P1-E1065-CON | Contract | C: the stage, seed-profile, database and role and failure contract this story builds against, and its fake |
| RWB-P1-E1065-APP | App development | Sibling primary slice: the stage, the generator, the ACE test double and the nine legacy criteria; this story carries the deviation part only |
| RWB-P1-E1065-DB | ACE DB | Sibling: the database, the read-only role and the grants; this story asserts the grant and creates neither |
| RWB-P3-E1065-APP | App development | Sibling: the case estate the deviation references point at, and the case-reference fixture |
| RWB-P5-E1065-APP | App development | Sibling: the document estate the deviation shapes use as evidence |
| RWB-ITG-E1065-ITG | Integration | The end-to-end proof of the sandbox values across the five services |

### 19. Out of scope

- The sandbox stage, the generator, the ACE schema test double, the 30 `v_ace_*` views, the export tool and the nine legacy criteria: RWB-P1-E1065-APP.
- The stage contract, the seed profile schema, the database and role contract and the failure contract: RWB-P1-E1065-CON.
- The database `rwb_sandbox`, its schemas, the read-only role `rwb_sandbox_read`, the grants and the deployment gate: RWB-P1-E1065-DB.
- The case estate and the case-reference fixture: RWB-P3-E1065-APP. The document estate: RWB-P5-E1065-APP. The interaction, role and permission rows: RWB-P1-E1065-APP and the rwb-case and rwb-access reference data.
- Raising, pausing, routing, contact stopping, handling and clearing a deviation, and the two write operations of the service: the Epic 2 and Epic 7 stories of this service (FEAT-DVH-01 to FEAT-DVH-09, FEAT-DVF-01 to FEAT-DVF-10).
- The deviation screens SCR-06 and SCR-08 and their states: the other stories of this service.
- Masked copies of production data in SIT and UAT (RWB-TE-004 in the legacy set), the rule scenario build gate (RWB-E1-073), the performance harness (RWB-TE-009) and the PDPA lint (RWB-TE-011).
- The ACE ingestion itself and the 14 Tier 2 tables: the ACE team owns them in RWB-ACE-001, and this story holds no ACE object.
- The dictionary content and its change process (RWB-E1-064 in the legacy set); the rule packages and their approval: rwb-decision (P7).
- The end-to-end proof of these values across rwb-case, rwb-deviation and rwb-source-data: RWB-ITG-E1065-ITG.
