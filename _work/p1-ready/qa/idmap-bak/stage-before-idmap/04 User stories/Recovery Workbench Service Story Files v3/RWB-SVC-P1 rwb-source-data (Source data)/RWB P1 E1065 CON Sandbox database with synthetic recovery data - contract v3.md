# RWB-P1-E1065-CON Sandbox database with synthetic recovery data

**Version 3 changes**

- One shared rwb_sandbox that no slice renames or recreates; the build database, rename and "one database per service release" wording are removed (RD-P1-046; findings 2, 8 and 12).
- Five published fixture file groups, the consumed list read on its published path, and the elements that are not P1's (run order and field registry) stated (RD-P1-046; findings 1, 3, 4 and 5).
- Stage contract completed with idempotency key, restart, lock, build report, failure table, grant matrix and stage states; AC9 to AC15 added (findings 6 to 17, 20 to 23).
- Roles, dependencies, event owner and traceability corrected (RD-P1-022, RD-P1-043; findings 18, 19, 21, 24 and 25).
- Batch D: failed builds keep the previous sandbox and tests never reset ledger rows (RD-P1-073); test case IDs TC-P1-E1065-CON-10 to -16 cited.

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P1-E1065-CON |
| Version | 3 |
| Work type | CON (Contract) |
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
| Parallel lane | CG-W1 |
| Ready to start | Day 1, against the published list-read contract of RWB-P3-E1043-CON and its fake |
| Size | Not specified in the source documents (DOR-RWB-P1-E1065-CON-16); the squad sizes it at refinement |
| Depends on (build) | None |
| Contract dependencies | C: RWB-P3-E1043-CON v1 (list of values read) |
| Contract version | Sandbox stage and fixture contract published as one versioned package at fakes/rwb-source-data/<contract version>/; version number Pending under NEW-ASM-A1; consumes RWB-P3-E1043-CON v1 |
| Integration dependencies | None |
| External dependencies | RWB-P1-E1065-APP; RWB-P1-E1065-DB; RWB-P1-E1069-APP; RWB-P1-E1069-DB |
| Wave 1 contract-test harness and synthetic test data | Not specified in the source documents (GAP-0384) |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v1.md (FR-P1-001, FR-P1-006, FR-P1-007, FR-P1-008, FR-P1-010, FR-P1-012, FR-P1-013, FR-P1-024, FR-P1-025, FR-P1-029, FR-P1-030) |
| Readiness decisions | RD-P1-004, RD-P1-005, RD-P1-011, RD-P1-021, RD-P1-022, RD-P1-024, RD-P1-043, RD-P1-046, RD-P1-073 |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-065 for rwb-source-data. The sandbox of the legacy story becomes a build tool of this service, so its interface is published as a contract before the tool is written: the stage contract (trigger, inputs, outputs, idempotency key, restart behaviour), the seed profile schema, the database and role contract for `rwb_sandbox` with schema `public`, schema `recovery` and schema `rwb_source_data`, the failure contract and the four fixtures that stand in for the neighbouring stories (DP-01, DP-05, DP-07, DP-15; Architecture v5 slides 8, 15, 29 and 41). The nine legacy acceptance criteria stay with RWB-P1-E1065-APP; this story owns the six contract criteria only. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P1-E1065-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (16 resolved, 19 cross-document, 6 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: shared sandbox contract, deterministic file fixtures, stage, failure and grant contract. Agent: S7-stories.

### 1. Story

As a **recovery developer (RW-TRIBE)**, I want **the published contract baseline of the sandbox build of rwb-source-data: the stage document that fixes its trigger, its inputs, its outputs, its idempotency key and its restart behaviour, the seed profile schema whose every value is data, the database and role contract of the shared `rwb_sandbox` with P1's three schemas and the DEV read role, the failure contract that fails closed, the published fixture files, and the contract tables of section 12**, so that **the generator, the verifier, the ACE database work and the contract tests can be built in parallel on Day 1 against a fixed, testable interface instead of a description in a pipeline script**.

This is the contract slice of legacy RWB-E1-065. It delivers:

- the stage contract: trigger, inputs, outputs, idempotency key, restart, lock and build report of the P1 sandbox stage;
- the seed profile contract: seed 20261128, total 2,812 cases and the five profile elements of ASM-0694, with the field-level schema Pending under NEW-GAP-S7-02;
- the database and role contract: the shared database `rwb_sandbox`, P1's schemas `public`, `recovery` and `rwb_source_data`, the DEV read role `rwb_sandbox_read` and its grant matrix; DEV and pipeline test only, no production data;
- the failure contract, which fails closed and publishes no fixture version from a failed build;
- the published fixtures: `seed-profile.json`, `case-seed-list.csv`, `shape-table.csv`, the four stage fixtures (full, empty, refused, timeout) and `tier2-ddl.sql`, versioned with the contract, and the drift rule that fails a build when a fixture leaves the contract;
- the contract tables of section 12, each with its owner.

It builds nothing: no generator, no verifier, no migration, no database. It defines the interface those artefacts must satisfy, and the app story, the ACE DB story and the tests of this legacy key read it.

### 2. Business rationale

The contract describes one shared rwb_sandbox database per DEV and pipeline-test environment. P1 creates it if absent and never drops, renames or recreates it. P1 owns only public, recovery and rwb_source_data; every other E1065 slice seeds only its own rwb_* schema (RD-P1-046).

The cross-service join surface is a versioned file set. P1 publishes a seed profile, one row per case in case-seed-list.csv, shape-table.csv, four stage fixtures and the RWB-ACE-001 Tier 2 DDL fixture. Case numbers are assigned by rwb-case; P1 publishes no case number. These files replace the unfixed case-list operation and let each consumer use the same deterministic seed (RD-P1-021, RD-P1-024, RD-P1-046).

### 3. Preconditions

- RWB-P3-E1043-CON v1 publishes GET /api/recovery/case/v1/admin/lists/{listCode}, with listCode, asOf and the Reference data right.
- RWB-P1-E1065-APP, RWB-P1-E1065-DB, RWB-P1-E1069-APP and RWB-P1-E1069-DB use the shared rwb_sandbox database and write only public, recovery and rwb_source_data.
- RD-P1-046 is the source for the fixture set and consumer list. The contract publishes files, not an operation.
- The total seed is 2,812 cases for seed 20261128. The five profile elements are seed, product volumes, shape count, list-of-values source and personal-data pattern rule.
- Pending: JSON property keys, field types, lengths, required flags and checksum scope, owner service contract owner, tracked as NEW-GAP-S7-02.
- Every shape of the section 11 list has 10 rows. A shape added without a count is Pending, owner data architect, tracked as NEW-GAP-C2.
- Fake library version is Pending under NEW-ASM-A1; its working path is fakes/rwb-source-data/<contract version>/.
- The lists the build reads are those named by `sys_fields.lov_code` of the seeded columns, each with `asOf` equal to the seed business date. The build identity and credential source are Pending under NEW-GAP-S7-03.
- DL43 is open with the ACE team lead; its recommended answer A (scope and dates as in RWB-ACE-001) is the planning basis, so `tier2-ddl.sql` follows RWB-ACE-001 (RD-P1-043).

### 4. Flow

1. Publish the stage interface and shared-database boundary.
2. Publish seed-profile.json with the five elements of ASM-0694, seed 20261128 and total 2,812.
3. Publish case-seed-list.csv with one row per case and no case number.
4. Publish shape-table.csv with shape_id, row_type, count, product_group and is_case.
5. Publish the four stage fixtures: full, empty, refused and timeout.
6. Publish tier2-ddl.sql with the 14 Tier 2 tables and 12 new columns.
7. Pin each fixture file to the contract package version and run drift tests against all named consumers.
8. Mark any field-level schema or missing shape count Pending; do not create values not fixed by RD-P1-046.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The stage contract omits an interface element | Contract test fails and names the element | Contract test result | AC1 |
| X2 | A seed-profile element is absent or has an invalid value | Contract test fails naming the property; unresolved schema details remain Pending | Contract test result | AC2 |
| X3 | A P1 slice touches a schema outside public, recovery or rwb_source_data | Contract test fails and names the schema | Contract test result | AC1 |
| X4 | A fixture drifts from the published file contract | Contract test fails naming the file and field or shape | Contract test result | AC7, AC8 |
| X5 | The Section B fixture is unavailable in DEV or pipeline test | Build fails and publishes no fixture version; in SIT, UAT and PROD Section B waits for RWB-ACE-001 and flags stay off | Pipeline result | AC7, AC10 |
| X6 | A consumer uses a case number from the P1 fixture | Contract test fails; P3 assigns case numbers | Contract test result | AC3, AC5 |
| X7 | A shape is declared without a count | Count is Pending under NEW-GAP-C2; interim one row for it with the remainder to plain 90-days-past-due | Pending | AC6 |
| X8 | The list read answers 401, 403, 404 MSG-P3-027, 503, an empty list or no answer within 2 s | Build fails before any seed write | Build report names the call and listCode | AC10 |
| X9 | A delivered view or extension table is missing, a view does not compile, a column has no dictionary row or a constraint is violated | Build fails and creates no replacement object | Build report names the object | AC10 |
| X10 | A second P1 build starts while one runs | It waits on the P1 advisory lock | None | AC1 |
| X11 | The target is not DEV or pipeline test | Stage stops before any database operation | Build report names target and host | AC10 |
| X12 | A fixture or contract element changes under the same version | Compatibility test fails naming the change | Contract test result | AC12 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Depends on the published P3 reference-data contract and the P1 build owners |
| Negotiable | Fixture values are versioned data; ownership and scope follow RD-P1-046 |
| Valuable | Consumers share one stable case-seed and shape-file contract |
| Estimable | The profile and report field schema and the build identity remain Pending |
| Small | Size is Not specified and remains for squad refinement |
| Testable | Contract drift is checked against versioned files and named consumers |

### 7. Acceptance criteria

~~~gherkin
Feature: Shared sandbox stage and seed-fixture contract

Scenario: AC1 The stage contract describes the shared sandbox
  Given the stage contract of section 12.6
  When a contract test reads it
  Then it states trigger, inputs, outputs, idempotency key, restart, lock and build report, and a copy with any one removed fails naming it
  And the database is rwb_sandbox, created only if absent, and no slice drops, renames or recreates it
  And P1 builds and checks only public, recovery and rwb_source_data, and other rwb_* schemas may exist and are not P1's
  And build order is ACE schema, service baseline, Section A, Section B over tier2-ddl.sql, then each service schema in wave order
  And outputs include per-table row counts and a checksum whose scope is Pending under NEW-GAP-S7-02
  # TC-P1-E1065-CON-01

Scenario: AC2 The seed profile contains the five ruled elements
  Given seed-profile.json for seed 20261128
  When the profile is validated
  Then it describes the seed, product volumes, shape count, list-of-values source and personal-data pattern rule
  And the total case count is 2,812
  And property keys, types, lengths and required flags remain Pending under NEW-GAP-S7-02
  # TC-P1-E1065-CON-02

Scenario: AC3 The case seed list does not assign case numbers
  Given the case seed file for seed 20261128
  When the contract test reads case-seed-list.csv
  Then there is one row per seeded case
  And each row contains shape_id, product_group, account_key, person_key, case_entry_date and total_outstanding
  And it contains no case number because rwb-case assigns case numbers
  # TC-P1-E1065-CON-03

Scenario: AC4 The shape table has the ruled columns and row types
  Given shape-table.csv
  When the contract test validates its header and rows
  Then each row contains shape_id, row_type, count, product_group and is_case
  And row_type is case, account only or asset only
  And 89-day accounts and collateral-with-no-account rows are not cases
  And each shape of section 11 has count 10, with the 89 and the 90 days past due shapes as separate rows
  And shaped cases are inside the total of 2,812
  # TC-P1-E1065-CON-04

Scenario: AC5 Consumers use the published fixture names
  Given the P3, P4, P5 and S8 E1065 consumers and PLT TE004
  When their fixture references are checked against this contract version
  Then they read seed-profile.json, case-seed-list.csv, shape-table.csv and tier2-ddl.sql by name
  And no consumer expects a P1 case number, case table or API operation, and RWB-S8-E1065-APP reads the file
  And no consumer takes the migration run order or the personal-data field registry from this contract: the run order is in section 12.6 and the registry stays with its owner under GAP-1435
  # TC-P1-E1065-CON-05

Scenario: AC6 Shape count gaps stay visible
  Given a shape is added to the shape list without a count
  When shape-table.csv is generated
  Then the count is Pending under NEW-GAP-C2 with owner data architect
  And the interim output has one row for that shape, with the remainder of the 2,812 assigned to the plain 90-days-past-due shape
  # TC-P1-E1065-CON-06

Scenario: AC7 The Tier 2 and stage fixtures are complete
  Given tier2-ddl.sql and the four stage fixtures
  When contract tests compare them with RD-P1-043 and ASM-0694
  Then tier2-ddl.sql has 14 Tier 2 tables and 12 new columns
  And the four fixtures are full, empty, refused and timeout
  And Section B is tested against the fixture in DEV and pipeline test
  And SIT, UAT and PROD wait for RWB-ACE-001 with flags off
  # TC-P1-E1065-CON-08

Scenario: AC8 A fixture with an undeclared shape is refused
  Given a versioned fixture package
  When a file adds, removes or changes a declared shape
  Then the contract test fails naming the file and shape
  # TC-P1-E1065-CON-09

Scenario: AC9 The consumed list read matches the rwb-case contract
  Given RWB-P3-E1043-CON v1 and its fake
  When the consumer contract test calls GET /api/recovery/case/v1/admin/lists/{listCode} with asOf for each listCode named by a seeded column
  Then each request and 200 answer match the published schema
  # TC-P1-E1065-CON-10

Scenario Outline: AC10 Every failure of the stage maps to one result
  Given the failure <case>
  When the stage runs against it
  Then the build is recorded Failed, the report names <named>, no fixture version is published and no schema outside public, recovery and rwb_source_data changes

  Examples:
    | case | named |
    | list read answers 401, 403, 404 MSG-P3-027, 503, empty or nothing within 2 s | the call and listCode |
    | tier2-ddl.sql is absent | the file |
    | a delivered view or extension table is missing | the object |
    | a column has no sys_fields row | schema.table.column |
    | a value matches a personal-data pattern | schema.table.column and not the value |
    | the target is not DEV or pipeline test | target and host |
  # TC-P1-E1065-CON-11

Scenario: AC11 Consumers can pin the contract
  Given the contract and fixtures published at one version
  When the consumer tests of RWB-P1-E1065-APP, RWB-P1-E1065-DB, RWB-P3-E1065-APP, RWB-P4-E1065-APP, RWB-P5-E1065-APP, RWB-S8-E1065-APP and RWB-PLT-TE004-APP run
  Then every file and element each of them names exists at that version
  # TC-P1-E1065-CON-12

Scenario: AC12 A breaking change under the same version is refused
  Given a published contract version
  When a database name, schema, role, failure check or fixture column changes without a new version
  Then the compatibility test fails and names the change
  # TC-P1-E1065-CON-13

Scenario: AC13 The grant matrix denies what it does not give
  Given the grant matrix of section 12.7
  When it is compared with a fixture that grants INSERT, a grant on schema public or a grant to PUBLIC to rwb_sandbox_read
  Then the test fails naming the grant
  # TC-P1-E1065-CON-14

Scenario: AC14 The seed outputs are deterministic
  Given the same commit, profile, seed 20261128, seed business date and list versions
  When the seed files are generated twice
  Then seed-profile.json, case-seed-list.csv and shape-table.csv are identical
  And product volumes are 1,226 Mortgage, 1,296 Hire purchase and 290 SSME, 2,812 in total
  # TC-P1-E1065-CON-15

Scenario: AC15 Fixtures hold no personal data
  Given the published fixtures
  When the national ID pattern with a valid check digit is applied to every value
  Then no value matches, and an injected match fails the test naming the file and column without logging the value
  # TC-P1-E1065-CON-16
~~~

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One shared rwb_sandbox exists per DEV or pipeline-test environment; P1 creates it if absent and no slice drops, renames or recreates it | RD-P1-046 |
| BR2 | P1 works only in public, recovery and rwb_source_data; each other slice seeds only its own rwb_* schema | RD-P1-046; DP-01 |
| BR3 | P1 publishes file fixtures, not a case-list API; rwb-case assigns case numbers and owns case records | RD-P1-021; RD-P1-024; RD-P1-046 |
| BR4 | The profile carries seed 20261128 and total 2,812 cases with the five elements of ASM-0694 | RD-P1-046 |
| BR5 | Shape counts come from the existing APP shape list; absent counts are Pending under NEW-GAP-C2 | RD-P1-046 |
| BR6 | The fixture set includes full, empty, refused, timeout and tier2-ddl.sql fixtures | RD-P1-043; ASM-0694 |
| BR7 | The contract and fakes are versioned; fake library version remains Pending under NEW-ASM-A1 | RD-P1-011 |
| BR8 | Section B is built against a synthetic fixture and deployed outside DEV only after the ACE dependency gate passes | RD-P1-043 |
| BR9 | The idempotency key of a build is commit, profile, seed 20261128, seed business date and list versions; the checksum scope is Pending | ASM-0558; GAP-2154; NEW-GAP-S7-02 |
| BR10 | Only rwb_source_data reads the ACE views in service environments; rwb_sandbox_read is the DEV-only exception | D-RCV-60; Security and Access Design v6 |

### 9. State transitions

| Object | States and moves |
|---|---|
| contract baseline | Draft to In review to Baselined, once the P1 app and DB stories and the consumers accept file names and schemas; a breaking change needs a new package version |
| P1 sandbox stage | Waiting to Building (lock taken); Building to Verified or Failed; Verified publishes the fixture version; Failed publishes nothing |

The status model of a case is not part of this contract.

### 10. Authority

| Role | Authority |
|---|---|
| Service contract owner | Publishes the stage interface and fixture schemas; fake version remains Pending under NEW-ASM-A1 |
| Data architect | Owns shape counts and data mappings |
| RWB-P3-E1043-CON owner | Owns the reference-data read contract |
| Platform DB owner | Owns build credentials and the target gate; the ACE team owns the shared database (ASM-0695) |
| Recovery developer (RW-TRIBE) | Starts the stage manually in DEV |
| Platform administrator (RW-PLATADM) | Starts the stage manually and reads the build report |
| Product owner | Owns epic sign-off; sign-off remains Pending |
| QA lead | Owns consumer drift tests and Test Cases v9 additions |

### 11. Data

| Fixture | Schema or fields | Status |
|---|---|---|
| seed-profile.json | Seed 20261128; total 2,812; product volumes; shape count; list-of-values source; personal-data pattern rule | Five profile elements; JSON keys and field-level types Pending under NEW-GAP-S7-02 |
| case-seed-list.csv | shape_id, product_group, account_key, person_key, case_entry_date, total_outstanding | One row per seeded case; no case number |
| shape-table.csv | shape_id, row_type, count, product_group, is_case | row_type is case, account only or asset only; missing count Pending under NEW-GAP-C2 |
| Stage fixtures | full, empty, refused, timeout | Four fixtures under ASM-0694 |
| tier2-ddl.sql | 14 Tier 2 tables and 12 new columns | DEV and pipeline-test fixture under RD-P1-043 |

**Shape list** (taken from the legacy exception shapes of RWB-P1-E1065-APP; 10 rows each): duplicate case for one customer and product; deceased customer; bankruptcy; open deviation; legal hold; unmapped product code; collateral with no account (asset rows); case with three accounts; account at 89 days past due (account rows); account at 90 days past due (case rows); withdrawn consent. The `shape_id` values are Pending under NEW-GAP-S7-02.

**Build report** (one per run): commit, profile, seed, seed business date, list versions, per-table row counts, checksum, check results and state. Its file format is Pending under NEW-GAP-S7-02.

### 12. Contract

#### 12.1 REST operations provided

None. The sandbox build is a pipeline stage and publishes no operation; the read contract of the service on base `/api/recovery/source-data/v1` is RWB-P1-E1069-APP's, and this contract adds no path to it (DP-13).

#### 12.2 REST operations consumed

| Method | Path | Owner | Contracted use |
|---|---|---|---|
| GET | /api/recovery/case/v1/admin/lists/{listCode} | RWB-P3-E1043-CON v1 | Build-time list read with listCode and asOf, using the Reference data right, one hop, 2 s. 401 MSG-P4-001, 403 MSG-P4-002, 404 MSG-P3-027, 503, an empty list or a timeout fails closed (RD-P1-004). Build identity and credential source are Pending under NEW-GAP-S7-03. |

#### 12.3 Events published

None. The topic of the service is `rwb.source-data.events.v1` with event names `rwb.source-data.<Event>.v1` (DP-14), and the events `AceDataReady` and `AceDataLate` belong to RWB-P1-E1015-APP (published in RWB-P1-E1015-CON). A build result is published in the pipeline, not on the topic.

#### 12.4 Events consumed

None. The service consumes no event (Architecture v5 slide 15), and the stage subscribes to none.

#### 12.5 Workflows and activities

None. The stage calls no Temporal workflow and no activity; the task queue `rwb-source-data` in namespace `rwb-recovery` is not used by this contract.

#### 12.6 Schedules

The stage is triggered by a relevant merge or a manual DEV run. It is not a Temporal Schedule, Quartz job or job_catalog row.

| Element | Contract |
|---|---|
| Database | Shared rwb_sandbox per DEV or pipeline-test environment; create only if absent |
| Scope | P1 builds and checks only public, recovery and rwb_source_data; other rwb_* schemas may exist |
| Inputs | ACE schema, tier2-ddl.sql, P1 baseline and view migrations, metadata, profile and reference-data answers |
| Outputs | Versioned fixture files, per-table row counts and a checksum |
| Publication | No drop, rename or recreation of rwb_sandbox |
| Idempotency key | Commit, profile, seed 20261128, seed business date and list versions |
| Restart | Seed rows are reloaded in one transaction on public and the generator-seeded P1 tables; tables seeded by a migration are not reloaded; a failed or restarted run leaves the previous rows (working assumption NEW-ASM-S7-01) |
| Lock | One PostgreSQL advisory lock for the P1 build, taken in rwb_sandbox; a second build waits |
| Build report | Fields of section 11 |
| Failure | A failed apply, seed or check records Failed, keeps the previous seed rows and publishes no fixture version. A failed sandbox build leaves the previous sandbox in place and fails the pipeline, and each schema is seeded by its owner's E1065 story (RD-P1-073). No test or harness step deletes or resets ledger rows; tests isolate by their own cases and a fresh UUID per run in business keys, and the only reset is the sandbox rebuild between suites (RD-P1-073). |

#### 12.7 Tables owned

This contract creates no table. It names these shared objects and their owners:

| Object | Owner | Contract scope |
|---|---|---|
| database rwb_sandbox | ACE team (ASM-0695) | Shared database, created by P1 only if absent; never dropped, renamed or recreated by a slice |
| public ACE test double | ACE team | Synthetic Tier 1 and 14 Tier 2 tables |
| recovery views | rwb-source-data | 16 Section A views and 14 Section B views, with the Section B gate |
| rwb_source_data | P1 | P1-owned tables and four extension tables |
| other rwb_* schemas | Each service owner | May exist; P1 does not create, seed or alter them |
| case records and case numbers | rwb-case | Not part of this contract |
| role rwb_sandbox_read | Platform DB owner | DEV only |

**Grant matrix.**

| Grantee | recovery | rwb_source_data | public | Writes |
|---|---|---|---|---|
| rwb_source_data (service login) | USAGE; SELECT on the views | Own schema; extension tables SELECT, INSERT, UPDATE | None | No write on a view |
| ace_view_owner (NOLOGIN) | Owns the views | None | SELECT on the source tables of the views | None |
| rwb_sandbox_read (DEV only) | USAGE, SELECT | USAGE, SELECT | None | None |
| PUBLIC and other service logins | None | None | No grant added | None |

#### 12.8 Contract fakes

| Fixture | Serves | Used by |
|---|---|---|
| seed-profile.json | Seed 20261128, 2,812 cases and five profile elements | P1 and downstream E1065 slices |
| case-seed-list.csv | Case join keys and shape per seeded case; no case number | P3, P4, P5, S8 and PLT TE004 |
| shape-table.csv | Shape types and counts | P1 and downstream E1065 slices |
| full, empty, refused and timeout | Stage fixture states | P1 build and contract tests |
| tier2-ddl.sql | 14 Tier 2 tables and 12 new columns | DEV and pipeline test Section B build |

Files are generated deterministically and versioned with the contract. Fake library version is Pending under NEW-ASM-A1. Consumers include P3/P4/P5/S8 E1065 and PLT TE004.

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | None for fixtures | One P3 list read at build time | Files, not an operation, are the cross-service seed contract |
| Kafka | None | None | The build publishes no event |
| Temporal | None | None | Pipeline stage only |
| File | Five fixture groups | ACE schema and P1 migrations | Files are versioned with the contract package |
| SQL view | None | 30 recovery.v_ace_* views | P1 reads and verifies only |

### 13. Solution plan

**Deliverables.** The stage interface, seed-profile.json, case-seed-list.csv, shape-table.csv, the full/empty/refused/timeout fixtures and tier2-ddl.sql.

**Fixture and compatibility rules.** The case seed list contains no case number; rwb-case assigns it. The shape table identifies case, account-only and asset-only rows. Shaped cases are within the total 2,812. An 89-days-past-due boundary row and a collateral-with-no-account row are not cases. A shape without a count is Pending under NEW-GAP-C2; the interim output has one row for it and assigns the remainder to the plain 90-days-past-due shape.

**Versioning.** The fixture package is published under fakes/rwb-source-data/<contract version>/. The exact library version remains Pending under NEW-ASM-A1. Field-level JSON schema and checksum scope remain Pending under NEW-GAP-S7-02.

**Build order.** ACE schema, service baseline, Section A, Section B over the synthetic Tier 2 fixture, then each service schema in wave order (RD-P1-043 and RD-P1-046). The stage never creates a replacement database.

### 14. Validation and messages

This contract defines file and pipeline results, not user-facing messages, and publishes no operation. The consumed P3 list read uses its published problem responses (401 MSG-P4-001, 403 MSG-P4-002, 404 MSG-P3-027, 503). Any refusal, empty list or timeout fails the build before seed publication. The legacy access messages of the case read path belong to the P3 slice.

### 15. Screens and states

No screen. The contract is read by the three consuming stories, whose state machines it fixes: the stage states of section 9 and the baseline states Draft, In review and Baselined. Nothing in this contract is shown to a user of the Workbench; the sandbox is read with SQL and the export script.

### 16. Test cases

Test Cases v9 holds TC-P1-E1065-CON-01 to -06 and -08 to -16 for AC1 to AC15. TC-P1-E1065-CON-07 is a legacy row and is not evidence for these criteria.

| Acceptance criteria | Test case |
|---|---|
| AC1 to AC6 | TC-P1-E1065-CON-01 to -06 |
| AC7, AC8 | TC-P1-E1065-CON-08, -09 |
| AC9 to AC15 | TC-P1-E1065-CON-10 to -16 |

### 17. Guardrails

- Treat the database as shared and never drop, rename or recreate it.
- Publish only synthetic fixtures; never include production data.
- P1 does not publish a case number, case table or case-status contract.
- Mark missing schema fields and shape counts Pending with the listed owners.
- Publish fakes only under the pinned contract version.

### 18. Traceability

| Reference | Use |
|---|---|
| RD-P1-005 | P3 published list contract and error precedence |
| RD-P1-011 | Versioned fake path and fake version handling |
| RD-P1-021 | P1 table ownership |
| RD-P1-024 | Case list and case status removed from P1 |
| RD-P1-043 | Section B fixture and deployment gate |
| RD-P1-046 | Shared sandbox and seed fixture set |
| ASM-0694 | Stage fixtures and five profile elements |
| NEW-GAP-C2 | Missing shape counts |
| RD-P1-004; RD-P1-022 | Problem answers of the consumed read; owner of AceDataReady and AceDataLate |
| DL43 | Recommended answer A is the planning basis of the Section B fixture |
| GAP-0501, GAP-0502, GAP-2137, GAP-3086 | Closed by RD-P1-046 |
| GAP-1435; GAP-3168; GAP-0566; GAP-0503; GAP-2154 | Field registry; Tier 1 count; baseline file; read role; seed and business date |
| NEW-GAP-S7-02; NEW-GAP-S7-03; NEW-ASM-S7-01 | Profile and report schema; build identity; in-place reload |
| REQ-RDF-001; REQ-RDF-010; RTM v9 | Requirement trace; matrix rows follow the test case update |

### 19. Out of scope

- A REST endpoint that returns the seed profile, case list or shape table.
- Case numbers, P3 case records, status transitions, case-list workflows or schedules.
- The exact Tier 1 table count and legacy V0001 decision; these remain under GAP-3168 and GAP-0566.
- The identity that reads P3 lists at build time; Pending under NEW-GAP-S7-03.
- The migration run order beyond section 12.6 and the personal-data field registry of the masked copy: their owners (GAP-1435).
- The generator, the verifier, the export tool and the pipeline stage itself: RWB-P1-E1065-APP.
- The database `rwb_sandbox`, P1's three schemas, the role `rwb_sandbox_read` and its grants: RWB-P1-E1065-DB; the four extension tables and the view grants: RWB-P1-E1069-DB.
- The 30 `recovery.v_ace_*` views and their helper functions: RWB-P1-E1069-APP.
- The per-service baseline, this service's 13 tables and the dictionary rows: RWB-P1-E1001-APP.
- The implementation of the reference-data contract of rwb-case: RWB-P3-E1043-CON, which this contract consumes and fakes.
- The rule packages and the decisions they take: rwb-decision (P7), consumed through the embedded kit and not defined here.
- Any change to a database name, a schema name, the read-only role or a failure check: the solution architect and the recovery tech lead, with a new baseline.
- The screens, the composite route and the DEV service: gateway-bff and the screen owners (DP-19).

### 20. Remaining delivery steps

- Size: Not specified; owner squad lead at refinement.
- Epic design sign-off: Pending; owner product owner and design authority.
- CON Done: Pending; owner service contract owner after fixture and schema acceptance.
- Fake published: Pending versioned fixture publication under fakes/rwb-source-data/<contract version>/; owner service contract owner and QA; version NEW-ASM-A1.
- Test data in DEV: Pending the first shared-sandbox seed; owner platform DB owner and QA lead.
- Profile and report schema (NEW-GAP-S7-02) and build identity (NEW-GAP-S7-03): owner service contract owner and platform DB owner.
