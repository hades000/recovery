# RWB-P1-E1065-APP Sandbox database with synthetic recovery data

**Version 3 changes**

- One shared rwb_sandbox that P1 creates only if absent and never drops, renames or recreates; five published fixture file groups and no case table or case number in P1 (RD-P1-046, RD-P1-021, RD-P1-024; findings 1 to 4, 10 and 12).
- Section B build and gate behaviour, and decision records through the local outbox (RD-P1-043, RD-P1-008; findings 5, 8 and 9).
- Role and test-user seeding moved to RWB-P4-E1065-APP and the case status check to RWB-P3-E1065-APP (findings 6, 14 and 17).
- Shape list restored, in-place reload and build lock stated, and AC10 to AC18 added (findings 7, 10, 11, 13, 15, 16, 18 to 24).
- Batch D: failed builds keep the previous sandbox and tests never reset ledger rows (RD-P1-073); decision records are held in the local decision_record table (RD-P1-068); test case IDs TC-P1-E1065-APP-01 to -09 cited.

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P1-E1065-APP |
| Version | 3 |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-source-data |
| Service epic | RWB-SVC-P1 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-065 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP04, DP05, DP07, DP13, DP15, DP19 |
| Parallel lane | L-P1-A |
| Size | Sized by the squad at refinement |
| Ready to start | After E1001-APP, E1069-APP, E1069-DB and E1065-CON prerequisites |
| Depends on (build) | RWB-P1-E1065-CON, RWB-P1-E1001-APP, RWB-P1-E1069-APP, RWB-P1-E1069-DB, RWB-PLT-E1044-CON, RWB-P3-E1043-CON, RWB-PLT-E1027-CON |
| Contract dependencies | RWB-P1-E1065-CON; RWB-P3-E1043-CON v1 |
| Integration dependencies | None |
| External dependencies | RWB-P1-E1065-DB; RWB-P1-E1069-APP; RWB-P1-E1069-DB; RWB-P7-E1073-CON |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v1.md (FR-P1-001, FR-P1-006, FR-P1-007, FR-P1-008, FR-P1-010, FR-P1-012, FR-P1-013, FR-P1-024, FR-P1-025, FR-P1-029, FR-P1-030) |
| Contract version | Sandbox stage and fixture package of RWB-P1-E1065-CON, version Pending under NEW-ASM-A1; RWB-P3-E1043-CON v1 |
| Open decisions | DL43 (ACE team lead; recommended answer A is the planning basis, RD-P1-043); DL15 (volumes), DL16 (89 and 90 days past due boundary) and DL39 are used as the story states them |
| Readiness decisions | RD-P1-005, RD-P1-008, RD-P1-011, RD-P1-020, RD-P1-021, RD-P1-024, RD-P1-043, RD-P1-046, RD-P1-068, RD-P1-073 |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-065 for rwb-source-data. The sandbox becomes a build tool of this service rather than a step of a monolith pipeline: `tools/sandbox-generator` in package `th.co.scb.ace.workbench.recovery.sourcedata.sandbox`, a separate build module that is never packaged into the service, creates `rwb_sandbox` on the one ACE PostgreSQL server with schema `public` as the ACE test double, schema `recovery` holding the 30 read-only views and schema `rwb_source_data` holding this service's own tables and the four extension tables (DP-01, DP-02, DP-05; Architecture v5 slides 8, 15, 29 and 41). The nine legacy acceptance criteria are copied here word for word and the generator, verifier, export tool and pipeline stage move with them; the login, the grants and the extension tables are RWB-P1-E1065-DB, the contract baseline is RWB-P1-E1065-CON. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P1-E1065-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (37 resolved, 21 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: shared sandbox scope, published seed outputs, DL43 behaviour, in-place reload and acceptance criteria. Agent: S7-stories.

### 1. Story

As a **recovery developer (RW-TRIBE)**, I want **a sandbox build tool of rwb-source-data that stands up `rwb_sandbox` on the one ACE PostgreSQL server from the same DDL as SIT, with schema `public` as the ACE test double, schema `recovery` holding the 30 read-only `v_ace_*` views and schema `rwb_source_data` holding this service's own tables and the four extension tables, all filled with synthetic rows**, so that **I can build and test every read before the ACE interfaces are available and without production data, in DEV only and with no second copy of source data**.

This is the application slice of legacy RWB-E1-065, and it owns all nine legacy acceptance criteria. It delivers:

- `tools/sandbox-generator`, Java package `th.co.scb.ace.workbench.recovery.sourcedata.sandbox`, a separate build module that is never packaged into the service artefact;
- `AceSchemaLoader`, `SandboxGenerator`, `ValueFactory`, `ExceptionShapeBuilder`, `SandboxVerifier` and `SandboxExport`, and the sandbox build stage that runs them (DP-15);
- the seed profile as data: seed 20261128, 1,226 Mortgage, 1,296 Hire purchase and 290 SSME cases, 10 cases per exception shape, every value overridable;
- the dictionary-driven fill, so that a schema change reaches the sandbox with no generator change (DP-01, DP-15);
- the lists of values read through the rwb-case reference-data contract (DP-07), and the embedded Drools kit that evaluates the seeded rule packages in the sandbox smoke check (DP-04).

It does not create the 30 `recovery.v_ace_*` views, which are RWB-P1-E1069-APP's; it does not create the `rwb_source_data` login, the grants or the read-only role `rwb_sandbox_read`, which are RWB-P1-E1065-DB's (external dependency X), nor the four extension tables, which are RWB-P1-E1069-DB's; and it writes no table of another service (DP-01). Role, permission and test-user seeding (the legacy AC10 and BR6) is RWB-P4-E1065-APP's, and the check that a seeded case status change is allowed (AC12) is RWB-P3-E1065-APP's (RD-P1-021). It asserts the views, the tables and the grants those two stories deliver and re-creates none of them.

### 2. Business rationale

The DEV and pipeline-test environments use one shared rwb_sandbox database. P1 builds and seeds only public, recovery and rwb_source_data; each other service seeds only its own schema. A P1 build creates rwb_sandbox if absent and never drops, renames or recreates it. Other rwb_* schemas may exist and are not P1's (RD-P1-046).

The case records belong to rwb-case. P1 publishes deterministic seed fixtures with account_key and person_key values so P3 and the other E1065 slices can join to ACE-shaped rows without P1 creating a case table or case number (RD-P1-021, RD-P1-024, RD-P1-046).

### 3. Preconditions

- The shared DEV or pipeline-test database rwb_sandbox is available. RWB-P1-E1065-DB creates it if absent; no P1 slice drops, renames or recreates it.
- The ACE schema fixture, RWB-ACE-001 Tier 2 fixture, P1 baseline, Section A views and four extension tables are available in the order of RD-P1-043 and RD-P1-046. Section B code is built and tested against the synthetic Tier 2 fixture in DEV and pipeline test.
- The P1 schema is rwb_source_data. The P1-owned tables are those in RD-P1-021. case_list_row is retired, and case, account and party records remain in P3 and their owners' schemas (RD-P1-024).
- RWB-P1-E1065-CON publishes seed-profile.json, case-seed-list.csv, shape-table.csv, the four stage fixtures and tier2-ddl.sql. Consumers use these fixture names.
- RWB-P3-E1043-CON v1 publishes GET /api/recovery/case/v1/admin/lists/{listCode}; each request uses asOf and the Reference data right. The build reads every list named by `sys_fields.lov_code` of a seeded column, with `asOf` equal to the seed business date.
- The build takes a seed business date (time zone Asia/Bangkok) with the commit, profile and seed 20261128; it moves the days past due, the 89 and 90 day shapes and the batch rows (ASM-0558; GAP-2154). Exact build principal and credential source are Pending, owner platform DB owner, tracked as NEW-GAP-S7-03.
- The build reloads seed rows in place in the shared database: one transaction truncates and reloads the ACE-shaped tables of `public` and the generator-seeded P1 tables, leaving tables seeded by a migration and every other schema unchanged (working assumption NEW-ASM-S7-01, following the one-transaction seed of RWB-S8-E1065-APP). A change of the ACE DDL recreates the test-double tables of `public` in the same run.
- The P1 build takes one PostgreSQL advisory lock in `rwb_sandbox`.
- Pending: exact JSON property keys, types, required flags and checksum scope for the seed profile, owner service contract owner, tracked as NEW-GAP-S7-02.
- RWB-P1-E1069-APP applies Section A views in each environment. In SIT, UAT and PROD the Section B migration waits for RWB-ACE-001; its feature flags stay off until the environment gate passes (RD-P1-043).

### 4. Flow

1. The pipeline starts on a merge that changes the ACE schema, P1 migrations, dictionary or seed profile, or on a manual DEV run.
2. The target gate of RWB-P1-E1065-DB refuses a target other than DEV or pipeline test; RWB-P1-E1065-DB creates rwb_sandbox only if absent. The build takes the P1 advisory lock and does not create a replacement database or rename or drop the shared database.
3. Apply the ACE schema, the RWB-ACE-001 fixture, the P1 baseline, Section A views and then Section B views over the fixture in the order of RD-P1-043 and RD-P1-046. The exact legacy V0001 file selection remains Pending under GAP-0566.
4. Read sys_objects and sys_fields, and read each required list through GET /api/recovery/case/v1/admin/lists/{listCode} with asOf before writing seed rows. Any refusal, empty list or timeout fails closed.
5. In one transaction, reload ACE-shaped synthetic rows in public (including one ace_batch_run row per source and business date) and rows in generator-seeded P1 tables of rwb_source_data. Do not write to another rwb_* schema or to a case table.
6. Publish seed-profile.json, case-seed-list.csv and shape-table.csv using the contract version. P3 assigns case numbers when it seeds its own case records.
7. Run dictionary, constraint, key-resolution, shape-count, delivered-object and personal-data checks before the transaction commits. Run the Drools smoke check against the P7 package fixture and expected decisions; while they are not published (CDC-03156) the check is reported Not run and the build is not recorded Verified for AC8.
8. Run Section A view conformance in every environment. Run Section B conformance against the DEV/pipeline fixture; in SIT, UAT and PROD run it only after RWB-ACE-001 lands. With Section B flags off, freshness is STALE with businessDate null and MSG-P1-001 (RD-P1-043).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A column of a seeded table has no sys_fields row | The build fails naming schema, table and column; it publishes no seed output | Pipeline result | AC4, AC11 |
| X2 | The reference-data read answers 401, 403, 404, 503, empty, or times out | The build fails before seed writes; it publishes no seed output | Contract problem in the build report | AC6 |
| X3 | A synthetic value violates a constraint | The transaction rolls back; the build fails naming the table and constraint | Pipeline result | AC4 |
| X4 | A generated value matches a configured personal-data pattern | The build fails naming schema, table and column and does not log the value | Pipeline result | AC7 |
| X5 | The 89 and 90 day boundary or collateral with no account is generated | 89-day accounts and collateral-only rows are account or asset rows; only 90-day rows are case rows | None | AC10 |
| X6 | A second P1 build starts while one runs | The second build waits on the P1 advisory lock and runs after the first | None | AC12 |
| X7 | RWB-ACE-001 has not landed in a non-DEV environment | Section B migration is withheld and its features remain flag-off; freshness returns STALE, null businessDate and MSG-P1-001 | MSG-P1-001 for freshness | AC9 |
| X8 | A delivered view or extension table is missing, or a view does not compile | The build fails naming the object and does not create a replacement | Pipeline result | AC15 |
| X9 | A shape is declared without a count | The count is Pending under NEW-GAP-C2; the interim fixture has one row for it and assigns the remainder to the plain 90-days-past-due shape | Pending | AC3 |
| X10 | `tier2-ddl.sql` is absent in DEV or pipeline test | The build fails and publishes nothing; no partial sandbox is published | Pipeline result | AC16 |
| X11 | The connection drops or the process stops during the load | The transaction rolls back, the previous rows remain, the lock is released and the build is Failed | Pipeline result | AC17 |
| X12 | A rule-package evaluation fails or returns an unexpected decision | The build fails naming the package | Pipeline result | AC8 |
| X13 | The target is not DEV or pipeline test | The stage stops before any database operation | Pipeline result | AC14 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Depends on the shared database, P1 baseline and view and extension-table migrations |
| Negotiable | Fixture values are versioned data; ownership and schema boundaries follow RD-P1 decisions |
| Valuable | Gives P1 and downstream E1065 slices synthetic source rows and stable join fixtures |
| Estimable | Four items stay Pending: profile schema, build identity, target allow-list and rule-package fixture |
| Small | Size is Not specified and remains for squad refinement |
| Testable | Each criterion has a build or fixture assertion; AC1 to AC18 have rows in Test Cases v9 |

### 7. Acceptance criteria

~~~gherkin
Feature: Shared sandbox seed and published fixtures for rwb-source-data

Scenario: AC1 P1 builds only its owned slices of the shared sandbox
  Given rwb_sandbox may already contain other service schemas
  When the P1 build runs in DEV after its ACE, baseline, view and extension-table prerequisites
  Then it creates rwb_sandbox only when absent and never drops, renames or recreates it
  And it writes only public, recovery and rwb_source_data
  And it leaves every other rwb_* schema unchanged
  And public contains the current ACE schema fixture, 14 Tier 2 tables and 12 added columns
  And recovery has 16 Section A views; it has 14 Section B views when the Tier 2 fixture is applied
  And rwb_source_data contains the P1 tables of RD-P1-021 that the migrations at this commit create, the four platform library tables, the library decision_record table and the four extension tables
  And none of loan_account, account_payment, party, contact_point, collateral, account_collateral, collections_history, party_product, valuation, score, asset, load_run, dq_exception, dq_rule, source_field_map, source_code_map, interface_run, interface_signoff, tracker_inventory or tracker_row is a table in recovery or rwb_source_data
  # TC-P1-E1065-APP-10

Scenario: AC2 The case seed list is published for downstream owners
  Given seed 20261128 and a total of 2,812 seeded cases
  When the fixtures are published
  Then case-seed-list.csv has one row per case with shape_id, product_group, account_key, person_key, case_entry_date and total_outstanding
  And every account_key and person_key resolves in public
  And the file contains no case number because rwb-case assigns it
  And the cases split into 1,226 Mortgage, 1,296 Hire purchase and 290 SSME, shaped cases included
  # TC-P1-E1065-APP-11

Scenario: AC3 Shape rows use the published type and count
  Given the shape list of section 8 and the shape-table.csv columns
  When shape-table.csv is published
  Then each row has shape_id, row_type, count, product_group and is_case
  And row_type is case, account only or asset only
  And each listed shape has 10 rows of its stated row type
  And the 89-days-past-due boundary and collateral-with-no-account rows are not cases
  And a shape declared without a count is Pending under NEW-GAP-C2, with one interim row and the remainder assigned to the plain 90-days-past-due shape
  # TC-P1-E1065-APP-12

Scenario: AC4 P1 seeds only its owned tables
  Given the P1 schemas and tables of RD-P1-021
  When the generator writes the seed
  Then no P1 case table, case_list_row, case number or case status row is written
  And no other service schema is written
  And a missing data-dictionary row or a constraint violation fails naming the object and keeps the previous rows
  # TC-P1-E1065-APP-13

Scenario: AC5 Profile fixtures are deterministic and versioned
  Given the same commit, seed 20261128, profile, seed business date, list versions and contract version
  When the build runs twice
  Then seed-profile.json, case-seed-list.csv and shape-table.csv are identical
  And each seeded table has the same row count and the same checksum over its columns other than generated ids and clock columns
  And no row of the first run remains in a reloaded table
  And the checksum algorithm, the excluded columns and the profile property schema remain Pending under NEW-GAP-S7-02
  # TC-P1-E1065-APP-14

Scenario: AC6 Reference-data failure stops the build before seed writes
  Given the reference-data fake and a build identity with the Reference data right (identity Pending under NEW-GAP-S7-03)
  When GET /api/recovery/case/v1/admin/lists/{listCode} with asOf returns 401, 403, 404, 503, an empty list or no answer within its budget
  Then the build fails closed before seed writes and reports the call and listCode
  And no seed output is published and the previous rows remain
  # TC-P1-E1065-APP-15

Scenario: AC7 A personal-data pattern match is rejected
  Given a 13-digit national ID with a valid check digit, or a value matching a configured mobile or email pattern, in a text or jsonb column of a base table of rwb_source_data
  When the verifier scans the schema
  Then the build fails naming schema, table and column, and the value is not written to the log
  And a clear identity value in public is not a failure and recovery views are not scanned
  And the mobile and email patterns and synthetic formats remain Pending under ASM-5269
  # TC-P1-E1065-APP-16

Scenario: AC8 Rule smoke check writes a decision record and fails closed
  Given the P7 rule-package fixture and its expected result for each shape
  When the Drools smoke check evaluates each shape
  Then an unexpected result or evaluation failure fails the build and names the package
  And one outbox_event row is written in rwb_source_data through the local decision-record library for each completed evaluation, so the row count equals the evaluation count
  And each row has event_type rwb.decision.DecisionRecorded.v1, is addressed to rwb.decision-record.v1 and carries the library idempotency key; the relay is off
  And each record is also held in the local decision_record table of rwb_source_data, created by the shared library migration of RWB-PLT-E1027-CON
  And no P1 decision_log_entry or case-creation code is written
  And package versions and expected results are Pending under CDC-03156
  # TC-P1-E1065-APP-17

Scenario: AC9 Section B follows the DL43 deployment gate
  Given the Section B views compile over the synthetic Tier 2 fixture in DEV and pipeline test
  When RWB-ACE-001 is absent from SIT, UAT or PROD
  Then the Section B migration is not applied and its feature flags stay off
  And Section A conformance always runs and Section B conformance runs once the migration is applied
  And freshness is STALE with businessDate null and MSG-P1-001 while the flag is off
  # TC-P1-E1065-APP-18

Scenario: AC10 Accounts at the entry boundary
  Given the exception shapes include the 89 and 90 days past due boundary
  When the build is published
  Then 10 accounts in v_ace_account have days_past_due 89 and none of them is a row of case-seed-list.csv
  And 10 accounts have days_past_due 90 and each appears once in case-seed-list.csv
  # TC-P1-E1065-APP-01

Scenario: AC11 The fill follows the data dictionary
  Given a test migration, never shipped, adds column risk_tier varchar(10) to rwb_source_data.account_ext with its sys_fields row
  When the build runs
  Then every seeded account_ext row holds a value of at most 10 characters in risk_tier
  And no generator code changed
  # TC-P1-E1065-APP-02

Scenario: AC12 Two builds at once
  Given a P1 build for commit "a1b2c3d" holds the P1 advisory lock
  When a build for commit "e4f5a6b" starts
  Then it writes nothing until the first ends
  And after both the reloaded tables hold the rows of commit "e4f5a6b"
  # TC-P1-E1065-APP-03

Scenario: AC13 The sandbox is readable and exportable and not writable by the read role
  Given a member holds rwb_sandbox_read in DEV
  When they count the rows of rwb_source_data.account_ext and export it with SandboxExport
  Then the count equals the build report count and the CSV file has one header row and that many data rows
  And an UPDATE on the table by that role fails with SQLSTATE 42501
  # TC-P1-E1065-APP-04

Scenario: AC14 Only DEV and pipeline test are accepted
  Given a target outside DEV and pipeline test
  When the stage starts
  Then it stops before any database operation and writes nothing
  And no batch job of any service loads a service table from public
  # TC-P1-E1065-APP-05

Scenario: AC15 A delivered object is missing
  Given rwb_source_data.party_ext is absent after migration
  When the verifier runs
  Then the build fails naming rwb_source_data.party_ext, creates no such table and keeps the previous rows
  # TC-P1-E1065-APP-06

Scenario: AC16 The Tier 2 fixture is absent
  Given tier2-ddl.sql is not in the contract package
  When a DEV or pipeline-test build runs
  Then it fails naming the file and publishes no fixture version
  # TC-P1-E1065-APP-07

Scenario: AC17 Failure part way through the load
  Given rows of a previous Verified build and a connection that drops after public is loaded
  When the build ends
  Then its state is Failed, the previous rows of public and rwb_source_data remain and the lock is released
  # TC-P1-E1065-APP-08

Scenario: AC18 Other service schemas are untouched
  Given rwb_sandbox holds rows in schema rwb_case
  When the P1 build reloads its seed
  Then the row counts and table definitions of rwb_case are unchanged
  # TC-P1-E1065-APP-09
~~~

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One rwb_sandbox database is shared per DEV and pipeline-test environment; P1 creates it if absent and never drops, renames or recreates it | RD-P1-046 |
| BR2 | P1 builds and seeds only public, recovery and rwb_source_data; other service slices seed only their own schemas | RD-P1-046; DP-01 |
| BR3 | P1 publishes the case seed, shape and profile fixtures as files; rwb-case assigns case numbers and owns case records | RD-P1-021; RD-P1-024; RD-P1-046 |
| BR4 | Seed 20261128 and total 2,812 cases, 1,226 Mortgage, 1,296 Hire purchase and 290 SSME; shaped cases are inside the total; each shape of the list below has 10 rows; a shape without a count is Pending under NEW-GAP-C2 | RD-P1-046; DL15 |
| BR5 | Lists of values are read through RWB-P3-E1043-CON and are never embedded as constants | DP-07 |
| BR6 | Section B code is built and tested against the fixture; SIT, UAT and PROD wait for RWB-ACE-001 with flags off until the gate passes | RD-P1-043 |
| BR7 | No production data is used in DEV or pipeline test | NFR-045 |
| BR8 | Decision records use the local library and outbox; the DEV relay remains off; P1 does not write decision_log_entry | RD-P1-021; ASM-3710 |
| BR9 | case_list_row, case-list workflows and status changes are outside P1 | RD-P1-024 |
| BR10 | Same commit, profile, seed, business date and list versions give the same rows | ASM-0558; GAP-2154 |
| BR11 | A clear identity number is allowed only in public; base tables of rwb_source_data hold masked or synthetic values | D-RCV-35 U4; CTL-11 |

**Exception shapes (BR4), 10 rows each.**

| Shape | Row type | Rule reference |
|---|---|---|
| Duplicate case for one customer and product | case | R-UNI-17 |
| Deceased customer | case | R-UNI-05 |
| Bankruptcy | case | R-UNI-07 |
| Open deviation | case | owned by rwb-deviation |
| Legal hold | case | R-UNI-20 |
| Unmapped product code | case | - |
| Collateral with no account | asset only | - |
| Case with three accounts | case | extra account rows are NEW-GAP-F12-4 |
| Account at 89 days past due | account only | DL16 |
| Account at 90 days past due | case | DL16 |
| Withdrawn consent | case | R-UNI-10 |

P1 publishes the shape on the fixture rows; the owning service creates its own records. The `shape_id` values are Pending under NEW-GAP-S7-02.

### 9. State transitions

This story changes no case state. The build stage moves from Waiting to Building when the P1 lock is taken, then to Verified or Failed. A Verified build commits the reloaded rows and publishes the versioned fixture files; a Failed build rolls back and keeps the previous rows. It never changes another service's schema. A failed sandbox build leaves the previous sandbox in place and fails the pipeline, and each schema is seeded by its owner's E1065 story (RD-P1-073). No test or harness step deletes or resets ledger rows; tests isolate by their own cases and a fresh UUID per run in business keys, and the only reset is the sandbox rebuild between suites (RD-P1-073). Pending: how this build reloads `interaction` in place when RWB-P1-E1066-OPS AC11 refuses TRUNCATE (mechanism NEW-GAP-S8-8), owner solution architect with the data architect (NEW-GAP-G2-finish-1).

### 10. Authority

| Role | Authority |
|---|---|
| Recovery developer (RW-TRIBE) | Builds the P1 generator and its fixtures |
| Platform DB owner | Owns pipeline credentials and the DEV and pipeline-test target gate; the ACE team owns the shared database (ASM-0695) |
| Solution architect | Confirms the in-place reload working assumption (NEW-ASM-S7-01) |
| Data architect | Owns unresolved shape counts and ACE-to-fixture mappings |
| RWB-P3-E1043-CON owner | Owns the list-read contract; the build identity remains Pending under NEW-GAP-S7-03 |
| P7 rule-package owner | Publishes the fixture and expected result per shape under CDC-03156 |
| Product owner | Owns scope sign-off; epic design sign-off remains Pending |

### 11. Data

| Entity or artefact | Fields or content | This story |
|---|---|---|
| public ACE test double | ACE Tier 1 fixture and 14 Tier 2 tables with 12 added columns | Writes synthetic rows only |
| recovery views | 16 Section A and 14 Section B views | Reads and verifies; never writes a view |
| P1 tables in rwb_source_data | data_contract, data_product, data_product_access, data_product_load, data_product_source, dp_guarantee_claim, dp_treatment, efs_ledger_outcome, interaction, job_run, job_run_check, business_day_readiness, reconciliation_result, sys_field_version, sys_fields, sys_objects; library tables outbox_event, outbox_delivery, processed_event, idempotency_key and decision_record (library migration; its DDL is Pending, owner platform lead, NEW-GAP-F08-7) | Writes synthetic rows only; never reloads rows seeded by a migration (reference and dictionary rows) |
| extension tables | party_ext, contact_point_ext, account_ext, valuation_ext; DF-EXT-001 to DF-EXT-049 | Tables are created by E1069-DB; this story seeds synthetic rows |
| case-seed-list.csv | shape_id, product_group, account_key, person_key, case_entry_date, total_outstanding | One row per seeded case; no case number |
| shape-table.csv | shape_id, row_type, count, product_group, is_case | Case, account-only and asset-only shape rows |
| case_list_row and other case records | Retired from P1; P3 owns case records and case status | No P1 row or write |

### 12. Contract

#### 12.1 REST operations provided

None. This story delivers a build tool and a pipeline stage; it publishes no operation. The read contract of the service is RWB-P1-E1069-APP's, on base `/api/recovery/source-data/v1` (DP-13), and this story neither adds a path to it nor documents one as provided.

#### 12.2 REST operations consumed

One build-time list read through RWB-P3-E1043-CON v1.

| Method | Path | Required inputs | Use and failure |
|---|---|---|---|
| GET | /api/recovery/case/v1/admin/lists/{listCode} | listCode and asOf | Read each list before seed writes; require the Reference data right. 401, 403, 404 MSG-P3-027, 503, empty answer or timeout fail the build closed. The build identity and credential source are Pending under NEW-GAP-S7-03. |

#### 12.3 Events published

The pipeline publishes no business event. A completed Drools evaluation writes one decision record through the local library to outbox_event, addressed to topic rwb.decision-record.v1 with type rwb.decision.DecisionRecorded.v1. The DEV relay remains off (ASM-3710). This story writes no P1 decision_log_entry and no case-creation code.

#### 12.4 Events consumed

None. The service consumes no event in Architecture v5 slide 15 ("none: Airflow call; fallback polls ACE batch record"), and a build tool subscribes to nothing.

#### 12.5 Workflows and activities

None. The sandbox build stage runs in the pipeline and calls no Temporal workflow or activity. The workflows `AceIngestCheck` and `ReconciliationWorkflow` and the activities `reconciliation`, `listEligibleAccounts` and `snapshot(page)` on task queue `rwb-source-data` belong to other P1 stories. The only process this story starts is the pipeline job of 12.6.

#### 12.6 Schedules

The sandbox build is a pipeline stage triggered by a relevant merge or manual DEV run. It is not a Temporal Schedule and creates no job_catalog row. The stage reads the ACE schema, tier2-ddl.sql, the P1 baseline and view migrations, the profile files, dictionary rows and reference-data answers. It writes only public, recovery and rwb_source_data and reports row counts. It reloads rows in one transaction under the P1 advisory lock (NEW-ASM-S7-01); checksum scope is Pending under NEW-GAP-S7-02.

#### 12.7 Tables owned

P1 owns the 16 tables listed in section 11 and the four extension tables delivered by RWB-P1-E1069-DB; the four outbox and idempotency library tables and decision_record are the platform's. P1 does not own case_list_row; the case list is a versioned file fixture and case records are owned by rwb-case. The shared database also contains public, recovery and other services' rwb_* schemas. This story writes only public, recovery and rwb_source_data and never drops or renames the database.

#### 12.8 Contract fakes

| Fixture | Contract content | Consumers |
|---|---|---|
| seed-profile.json | Seed 20261128, total 2,812 cases and the five profile elements of ASM-0694 | P1, P3, P4, P5, S8 and PLT TE004 E1065 slices |
| case-seed-list.csv | One row per case with shape_id, product_group, account_key, person_key, case_entry_date and total_outstanding; no case number | P3, P4, P5, S8 and PLT TE004 |
| shape-table.csv | shape_id, row_type, count, product_group and is_case; missing counts Pending under NEW-GAP-C2 | P1 and downstream E1065 slices |
| Full, empty, refused and timeout fixtures | The four stage responses in ASM-0694 | P1 build and contract tests |
| tier2-ddl.sql | 14 Tier 2 tables and 12 new columns | P1 Section B build and tests |

All fixture files are generated deterministically and versioned with the contract. Exact stage contract and fake library versions are Pending under NEW-ASM-A1. The file artefacts are not an API operation.

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | None | One build-time list read through RWB-P3-E1043-CON v1 | Requires listCode, asOf and the Reference data right |
| Kafka | Decision record through the local outbox library | None | Relay off in DEV; no direct build event |
| Temporal | None | None | Pipeline stage only |
| File | Versioned seed profile, case seed list, shape table and Tier 2 DDL | ACE schema and P1 migration files | Consumers pin fixture versions |
| SQL view | No view | 30 recovery.v_ace_* views | Read and verify only |

### 13. Solution plan

The generator is a separate build module and is never packaged in the service artifact. It reads the five profile elements, versioned fixtures and metadata; it writes synthetic rows only to public and rwb_source_data and reads the 30 recovery views. P3 owns all case records and case numbers.

Build order follows RD-P1-043 and RD-P1-046: ACE schema, P1 service baseline, Section A views, Section B views over tier2-ddl.sql in DEV and pipeline test, then each service's own schema in wave order. Exact legacy V0001 selection and Tier 1 count remain Pending under GAP-0566 and GAP-3168.

The implementation contains:
- AceSchemaLoader for ACE and Tier 2 fixtures;
- SandboxGenerator for synthetic rows in public and P1-owned tables;
- ValueFactory for dictionary-driven values;
- ExceptionShapeBuilder for the shapes of section 8 and shape-table.csv rows;
- SandboxVerifier for dictionary, constraint, key and configured-pattern checks;
- SandboxExport for CSV extracts of seeded tables (comma separated, UTF-8, one header row), without case status or case number;
- a pipeline stage that verifies and writes versioned fixtures.

Property names `rwb.sandbox.seed`, `rwb.sandbox.cases.mortgage`, `rwb.sandbox.cases.hire-purchase`, `rwb.sandbox.cases.ssme` and `rwb.sandbox.shape-count` (values 20261128, 1226, 1296, 290 and 10) are build settings of the stage, not Workbench parameters, so they are not in the parameter catalog. The feature flag `rwb.source-data.sandbox` points the DEV profile at `rwb_sandbox` and is off in every other environment.

Pending: profile schema and checksum scope (NEW-GAP-S7-02); P3 read identity (NEW-GAP-S7-03); target allow-list (NEW-GAP-S7-04); mobile and email patterns and synthetic values (ASM-5269); rule-package fixture and expected outcomes (CDC-03156).

### 14. Validation and messages

Build and fixture failures are pipeline results, not Workbench messages. Read API errors use the published P3 reference-data contract: 401 MSG-P4-001, 403 MSG-P4-002, 404 MSG-P3-027 and 503 per its Problem response. A Section B feature with its flag off answers STALE, businessDate null and MSG-P1-001 (RD-P1-043).

### 15. Screens and states

No screen in this story. Developers and analysts read the sandbox with SQL and the export script, and see the build result and row counts in the pipeline run. Screens built in DEV show sandbox cases through the normal endpoints, merged by the gateway-bff composite route (DP-19), which this story neither builds nor changes.

### 16. Test cases

| Acceptance criteria | Test case |
|---|---|
| AC1 to AC9 | TC-P1-E1065-APP-10 to TC-P1-E1065-APP-18 |
| AC10 to AC18 | TC-P1-E1065-APP-01 to -09 |

The data of TC-P1-E1065-APP-10 to TC-P1-E1065-APP-17 follows the revised criteria in the test case update. The legacy rows TC-P1-E1065-APP-19 to TC-P1-E1065-APP-23 (access check, boundary objects, role seed, reference read and status change) are not evidence for these criteria: their scope moved to RWB-P4-E1065-APP, RWB-P3-E1065-APP or AC1 to AC18.

### 17. Guardrails

- Use synthetic values only; never copy production or SIT data into DEV or pipeline test.
- Write only public, recovery and rwb_source_data; do not write another service schema.
- Never create or seed a case record, case status or case_list_row in P1.
- Do not log personal values or credentials.
- Keep Section B features disabled outside DEV until RWB-ACE-001 is deployed.
- Reload only in one transaction under the P1 lock; never reload migration-seeded rows.
- Treat unresolved profile, identity, gate and pattern details as Pending; do not substitute a guessed value.

### 18. Traceability

| Reference | Use |
|---|---|
| RD-P1-005 | Published service contract and error precedence |
| RD-P1-008 | DecisionRecorded event type |
| RD-P1-021 | P1 table ownership and decision-record handling |
| RD-P1-024 | case_list_row and case-list operations retired from P1 |
| RD-P1-043 | Section B build fixture, deployment gate and stale response |
| RD-P1-046 | Shared sandbox scope and published fixture set |
| Physical Schema v9; LDM v11; Test Cases v9; RTM v9 | Current database, data, test and trace references |
| RD-P1-002; RD-P1-011; RD-P1-020; RD-P1-022 | Workflow names, fake version, sandbox decision records, event owners |
| GAP-0501, GAP-0502, GAP-2137, GAP-3086 | Closed by RD-P1-046 |
| GAP-0566; GAP-3168; GAP-2154; ASM-5269; ASM-0695; NEW-GAP-C2; NEW-GAP-S7-02, -03, -04; NEW-ASM-S7-01 | Open baseline, table count, determinism, patterns, ownership, shape counts, profile, identity, gate and reload details |

### 19. Out of scope

- Creating case records, assigning case numbers, changing case status or building a case list: rwb-case owns these (RD-P1-021, RD-P1-024).
- Creating P1 base tables, extension tables, views, logins or grants: their owning DB and APP stories deliver them.
- Seeding role, permission or test-user rows: RWB-P4-E1065-APP owns this.
- Applying Section B in SIT, UAT or PROD before RWB-ACE-001 lands.
- Publishing an API operation for seed fixtures; they are versioned files.
- Case status checks of the seed: RWB-P3-E1065-APP.
- The database `rwb_sandbox`, P1's three schemas, the role `rwb_sandbox_read`, its grants and the target gate: RWB-P1-E1065-DB; the four extension tables and the view grants: RWB-P1-E1069-DB.
- The contract baseline of the sandbox build, the seed profile schema and the failure contract: RWB-P1-E1065-CON.
- The 30 `recovery.v_ace_*` views, their helper functions and their conformance test: RWB-P1-E1069-APP.
- The per-service baseline, this service's 13 tables and the dictionary rows: RWB-P1-E1001-APP.
- Masked copies of production data in SIT and UAT (RWB-TE-004 in the legacy set).
- The rule scenario build gate (RWB-E1-073 in the legacy set) and the performance test harness (RWB-TE-009 in the legacy set).
- The PDPA lint for code, tests and logs (RWB-TE-011 in the legacy set).
- The ACE ingestion itself and the 14 Tier 2 tables: the ACE team owns them in RWB-ACE-001, and this story holds their DDL as a fixture only.
- The dictionary content and its change process: RWB-P1-E1001-APP for the rows, and RWB-E1-064 of the legacy set for the dictionary of the 14 data products.
- The rule packages themselves and their approval: rwb-decision (P7).
- Any change to the 30-view list: the data architect and the recovery tech lead, with a new version of the ACE Data Tier Map v1.

### 20. Remaining delivery steps

- Size: Not specified; owner squad lead at refinement.
- Epic design sign-off: Pending; owner product owner and design authority.
- CON Done: Pending acceptance of RWB-P1-E1065-CON and the P3 list-read dependency; owner service contract owner.
- Fake published: Pending versioned fixture publication under fakes/rwb-source-data/<contract version>/; owner service contract owner and QA; fake library version NEW-ASM-A1.
- Test data in DEV: Pending the first shared-sandbox build; owner platform DB owner and QA lead.
- Profile schema (NEW-GAP-S7-02), build identity (NEW-GAP-S7-03), target allow-list (NEW-GAP-S7-04) and rule-package fixture (CDC-03156): their owners as in section 10.
