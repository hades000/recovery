# RWB-ITG-E1065-ITG Sandbox database with synthetic recovery data — integration

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-E1065-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W1 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-065 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP04, DP05, DP07, DP13, DP15, DP19 |
| Parallel lane | L-ITG-W1 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | RWB-P1-E1065-APP, RWB-P4-E1065-APP, RWB-P3-E1065-APP, RWB-S8-E1065-APP, RWB-P5-E1065-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-005, FR-PLT-006, FR-PLT-007, FR-PLT-008) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: integration proof of the split sandbox, carved out of RWB-E1-065 for the wave-1 integration epic. The single `recovery` schema of the monolith becomes the 19 schemas `rwb_case`, `rwb_decision`, `rwb_access`, `rwb_deviation`, `rwb_valuation`, `rwb_treatment`, `rwb_guarantee`, `rwb_litigation`, `rwb_asset`, `rwb_debtsale`, `rwb_writeoff`, `rwb_document`, `rwb_comms`, `rwb_payment`, `rwb_partner`, `rwb_integration`, `rwb_source_data`, `rwb_reporting` and `rwb_agent`, each fed by its own Flyway baseline and its own login, with schema `recovery` keeping only the 30 `recovery.v_ace_*` views and the three helper functions, and the four extension tables moving to `rwb_source_data` (DP-01, DP-05, DP-15). This story stands the split estate up in DEV and proves it; it owns no table. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-ITG-E1065-ITG). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **one `rwb_sandbox` database in DEV that stands up the ACE test double in schema `public` with its 22 Tier 1 and 14 Tier 2 tables, schema `recovery` with only the 30 `recovery.v_ace_*` views and the three helper functions, and the 92 tables of RWB-E1-001 in the 19 `rwb_*` schemas from each service's own Flyway baseline, seeded with synthetic rows through the data dictionary so that every table carries its rows in the schema of the service that owns it and the 2,812-case fixture survives the split intact**, so that **every wave-1 squad tests every view read, the case list, a notice and a report on the schema-per-service estate that will run them, without production data and without waiting for SIT**.

### 2. Business rationale

SIT reads the real ACE database; DEV has none. Without an ACE test double in the sandbox the 30 `recovery.v_ace_*` views cannot compile, so no squad can test a source read, the case list, a notice or a report before SIT is connected. RWB-E1-065 proved that on one `recovery` schema. The target estate no longer has one schema: the ACE database holds one schema and one login per service, with no cross-schema joins, views or foreign keys, and a boundary test in every build fails on any cross-schema reference (Arch v5 slide 29, ADR-014). The sandbox therefore has to stand up the same shape as SIT: the ACE test double in `public`, `recovery` reduced to the 30 read-only views and the three helper functions `recovery.ace_to_date`, `recovery.ace_to_boolean` and `recovery.ace_mask_value`, and the 92 tables of RWB-E1-001 split across 19 `rwb_*` schemas, each table in the schema of its owner under the Ownership Map (DP-01), each schema built by that service's own Flyway baseline (DP-15), and the four extension tables `party_ext`, `contact_point_ext`, `account_ext` and `valuation_ext` in `rwb_source_data` where the Ownership Map puts them (DP-05).

The generator still learns every table, column, type and list from the dictionary — `sys_objects` and `sys_fields` in `rwb_source_data` and `lov_value` in `rwb_case` — so a schema change in any service reaches the sandbox with no manual rebuild and no table ownership written in code (DP-07). The verifier has more to check than before: not one schema but 19, each with its own login, so a table that lands in the wrong schema, a login that reaches another service's tables, a view that stops compiling, a clear personal value in a service schema and a rebuild that does not reproduce the same counts are all failures that only appear across the 19 schemas and the 30 views. This story builds and runs that proof. It serves REQ-RDF-001, because the split makes the one system of record and the one owner of each data product visible in the database itself, and REQ-RDF-010, because each service login sees only its own schema and only `rwb_source_data` sees the views.

None of that is proven by any single service story. A service story seeds its own schema against its own baseline and cannot show that the 19 baselines compose, that the Ownership Map covers the 92 tables without a duplicate or a hole, that the grants hold across logins, or that the same commit and seed still reproduce the 2,812 cases and the `RW-2026-000001` totals. This story writes the harness that proves those properties together, on the real build stage and the real database, and it publishes no operation and owns no table of its own.

### 3. Preconditions

- A PostgreSQL 17 database `rwb_sandbox` exists in DEV and is reachable from the pipeline (RWB-E1-065).
- The 19 Recovery schemas exist with one login each — `rwb_case`, `rwb_decision`, `rwb_access`, `rwb_deviation`, `rwb_valuation`, `rwb_treatment`, `rwb_guarantee`, `rwb_litigation`, `rwb_asset`, `rwb_debtsale`, `rwb_writeoff`, `rwb_document`, `rwb_comms`, `rwb_payment`, `rwb_partner`, `rwb_integration`, `rwb_source_data`, `rwb_reporting` and `rwb_agent` — from the platform DB baseline (Arch v5 slides 29 and 38; RWB-PLT-NF06-DB), and each service's own Flyway baseline is in the repository at the version the build reads (DP-15).
- The 92 tables of RWB-E1-001 are distributed across those schemas under the Ownership Map, and the Map is the only source of the table-to-schema assignment: the build reads `Recovery Workbench Microservice Ownership Map v1` and holds no owner name in code.
- RWB-P1-E1065-APP is done: the generator, the verifier, the value factory, the exception-shape builder, the access seed loader and the build stage exist as a build module outside the ACE services, with the `is_personal` tags and the personal-data patterns it reads from `sys_fields` in `rwb_source_data`.
- RWB-P4-E1065-APP, RWB-P3-E1065-APP, RWB-P5-E1065-APP and RWB-S8-E1065-APP are done: the access rows (`role`, `permission`, `delegation_limit`), the case rows (`recovery_case`, `case_account`, `case_party`), the document rows (`document`, `document_field`) and the deviation rows (`deviation`) are seeded by their owners in their own schemas.
- RWB-P1-E1069-APP is done: the view DDL creates the 30 `recovery.v_ace_*` views and the three helper functions in schema `recovery`, with SELECT granted to the `rwb_source_data` login only.
- The ACE test-double DDL `15 ACE DB Alignment/ACE Schema PostgreSQL v1.sql` is in the repository with the 22 Tier 1 tables, among them `account`, `payment`, `customer`, `efs_action` and `iam_user`; the RWB-ACE-001 DDL for the 14 Tier 2 tables is available in DEV (DL43), and until it lands the 14 Section B views and the features that read them stay behind their flags.
- The Entra ID group RWB-DEV-RW-TRIBE exists and maps to the sandbox read-only database role; the role-to-permission matrix rows are available as a seed file for the sandbox.
- The per-schema seed volumes and the seeding order across the 19 baselines, and the cutover from one `recovery` schema to 19 schemas, are Not specified in the source documents (GAP-0374; ASM-0537).
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7). The harness is written on Day 1 against the five integration stories and is run when the split sandbox is built in DEV; a fake is never used in its place.

### 4. Flow

1. Pipeline: on a merge to main that changes the ACE test-double DDL, any service's Flyway baseline, the view DDL or the dictionary, or on a manual start by RW-TRIBE or RW-PLATADM, runs the sandbox build stage in DEV.
2. Pipeline: creates `rwb_sandbox_next` with schema `public`, schema `recovery` and the 19 `rwb_*` schemas, each schema with its own login.
3. Pipeline: applies the ACE test double (22 Tier 1 tables, then the 14 Tier 2 tables) to `public`; applies the view DDL of RWB-E1-069 (the 30 `v_ace_*` views and the three helper functions, no table) to `recovery`; applies each service's own Flyway baseline to its own schema, 92 tables in total across the 19 schemas (DP-01, DP-15).
4. Harness: runs the preflight of section 13 — `public`, `recovery`, the 19 schemas and their logins, the 22 + 14 test-double tables, the 30 views, the three helper functions, the 92 tables mapped by the Ownership Map and the generator module — and stops before any row is written when an element is missing.
5. SandboxGenerator: reads `sys_objects` and `sys_fields` in `rwb_source_data` and `lov_value` in `rwb_case` to learn every table, column, type, list and `is_personal` tag; it names no table, column, schema or owner itself.
6. SandboxGenerator: seeds the 22 Tier 1 and the 14 Tier 2 tables in `public` with synthetic rows, including one `ace_batch_run` row per source and business date.
7. SandboxGenerator: seeds the 19 schemas table by table in foreign key order, each table in the schema named by the Ownership Map, with seed 20261128 and 1,226 Mortgage, 1,296 Hire purchase and 290 SSME cases plus their accounts, parties, contact points, collateral, valuations, payments and interactions, linked by business key only. The per-schema seed volumes and the order in which the 19 baselines are seeded, and the cutover from the one `recovery` schema of RWB-E1-065, are Not specified in the source documents (GAP-0374; ASM-0537).
8. ExceptionShapeBuilder: adds 10 cases for each exception shape of BR4, each shape's rows in the schema of the table that holds it.
9. AccessSeedLoader: loads the 54 roles, the permission matrix and one named test user per role into `rwb_access`.
10. SandboxVerifier: compiles the 30 views and selects one row from each; checks that every seeded table in every schema has rows; checks every LOV column against `lov_value`; checks that every foreign key resolves inside its own schema and that no cross-schema foreign key, view or join exists in the 19 schemas; scans every `is_personal` column in the 19 schemas for a clear personal value; checks the 89 and 90 days-past-due boundary; and compares the dictionary with the built objects.
11. Pipeline: renames `rwb_sandbox_next` to `rwb_sandbox`, leaves each service login with rights on its own schema only, grants SELECT on schema `recovery` to the `rwb_source_data` login and to role `rwb_sandbox_read`, and publishes the build result with the row count per table per schema and the verifier result.
12. Harness: connects as each of the 19 service logins, reads its own schema, and asserts the refusal on another service's schema and on schema `recovery` for every login except `rwb_source_data`.
13. Harness: reads case "RW-2026-000001" on `GET /api/recovery/case/v1/cases` as a DEV test user of RW-TRIBE, reads its customer and account on `GET /api/recovery/source-data/v1/customers/{id}` and `GET /api/recovery/source-data/v1/accounts/{id}`, and asserts that the case, the party and the account are the seeded rows of their owning schemas.
14. Harness: rebuilds from the same commit `a1b2c3d` and seed 20261128, compares the row count of every table in every schema, and compares the `total_outstanding_at_entry` of "RW-2026-000001".
15. Harness: runs the two failure fixtures of section 13 — a dictionary fixture without the `sys_fields` row of `recovery_case.closure_reason` and an empty `LOV-PRODUCT` seed — asserts the failure text and the previous sandbox still in use, and writes the run report with one row per test case.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A table or column has no `sys_objects` or `sys_fields` row | Build fails naming the table and the column; the previous sandbox stays in use | None (pipeline result) | AC6 |
| X2 | A generated value breaks a constraint | Build fails naming the table and the constraint; the previous sandbox stays in use | None (pipeline result) | AC6 |
| X3 | A table of the 92 maps to no schema, or to two, in the Ownership Map | Build fails naming the table before a row is written | None (pipeline result) | AC2 |
| X4 | A service baseline creates a foreign key, view or join that names another schema | The boundary test fails naming the constraint and the schema; the build stops | None (pipeline result) | AC2 |
| X5 | A service login reaches another service's schema, or a login other than `rwb_source_data` reads schema `recovery` | The database refuses the statement; the report names the login and the schema | None (pipeline result) | AC3 |
| X6 | A view does not compile or returns no row | Build fails; the previous sandbox stays in use | None (pipeline result) | AC4 |
| X7 | A generated value in any `rwb_*` schema matches a personal data pattern | Build fails naming the schema, the table and the column; no sandbox is published from that build | None (pipeline result) | AC4 |
| X8 | The reset runs twice for the same commit and seed | The schemas are dropped and recreated; the same seed gives the same rows and counts in every schema | None | AC5 |
| X9 | A second build starts while one runs | The second build waits on the pipeline lock and runs after the first | None | AC5 |
| X10 | The RWB-ACE-001 DDL for the 14 Tier 2 tables is not yet in DEV | The build stops before the 14 Section B views; the 22 Tier 1 tables, the 16 Section A views and the 19 service schemas are still built and published | None (pipeline result) | AC1, when the Tier 2 DDL is present |

X1 to X2 and X8 to X9 are the exception paths of the legacy story carried onto the split estate; X3 to X7 are the new cross-schema failures that only appear once the tables live in 19 schemas; X10 keeps the Section B gate of DL43.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | The harness is a test project of its own; it needs the five integration stories, the 19 schemas and the build stage, and it owns no schema and no table |
| Negotiable | Fixture size, wait intervals, retry counts and report layout are configuration; the seed, the volumes, the shape count, the dictionary counts and the `RW-2026-000001` totals are fixed by the legacy story |
| Valuable | Proves across the estate what no single service story can prove: 92 tables in the right schemas, 30 views compiling, 19 logins isolated, no clear personal value, and the same commit and seed reproducing the same counts |
| Estimable | One harness project, six test classes, nine fixtures, one build trigger, one rebuild and one report |
| Small | Fits one sprint with the report |
| Testable | Every criterion is asserted on an observable: a row per schema, a grant refusal, a view result, a build failure text, a count comparison, a build state |

### 7. Acceptance criteria

```gherkin
Feature: Sandbox database with synthetic recovery data, proven on the split estate

  Background:
    Given the sandbox build uses seed 20261128
    Given volumes of 1,226 Mortgage, 1,296 Hire purchase and 290 SSME cases
    Given the 19 service schemas each hold their own login

  Scenario: AC1 The split sandbox stands up (new, D-RCV-60)
    Given the ACE test-double DDL with 22 Tier 1 and 14 Tier 2 tables, the view DDL with the 30 v_ace_* views and the three helper functions, and the Flyway baseline of each of the 19 services
    When the sandbox build runs in DEV
    Then schema public holds the 22 Tier 1 tables and the 14 Tier 2 tables
    Then schema recovery holds the 30 v_ace_* views and the three helper functions recovery.ace_to_date, recovery.ace_to_boolean and recovery.ace_mask_value, and no table
    Then the 19 schemas hold the 92 tables of RWB-E1-001, each in the schema of its owner: rwb_case, rwb_decision, rwb_access, rwb_deviation, rwb_valuation, rwb_treatment, rwb_guarantee, rwb_litigation, rwb_asset, rwb_debtsale, rwb_writeoff, rwb_document, rwb_comms, rwb_payment, rwb_partner, rwb_integration, rwb_source_data, rwb_reporting and rwb_agent
    Then the four extension tables party_ext, contact_point_ext, account_ext and valuation_ext are in rwb_source_data
    Then 30 of 30 views compile
    Then the dictionary holds 122 objects and 1,366 fields
    Then the sandbox holds 2,812 synthetic cases plus 10 cases for each exception shape, across Mortgage, Hire Purchase and SSME
    Then case "RW-2026-000001" has its accounts, parties, interactions and documents linked

  Scenario: AC2 Every table and its rows land in the schema of the owner (new, D-RCV-60)
    Given the Ownership Map maps each of the 92 tables to exactly one service schema
    When the generator seeds the tables table by table in foreign key order
    Then every table holds its rows for seed 20261128 in the schema named by the Ownership Map
    Then recovery_case, case_account and case_party hold the case rows in rwb_case
    Then interaction, sys_objects and sys_fields hold the ledger and dictionary rows in rwb_source_data
    Then deviation holds the deviation rows in rwb_deviation
    Then document and document_field hold the document rows in rwb_document
    Then role, permission and delegation_limit hold the access rows in rwb_access
    Then the case total is 2,812 plus 10 cases for each exception shape, unchanged from the monolith baseline
    Then the cases and their accounts, parties, contact points, collateral, valuations, payments and interactions are linked by business key only
    Then no foreign key, view or join in any of the 19 schemas names another schema, and the boundary test passes

  Scenario: AC3 Each service login reads only its own schema and only rwb_source_data reads the views (new, D-RCV-60)
    Given the 19 service logins and the read-only role rwb_sandbox_read
    When a session as login rwb_case selects from rwb_case.recovery_case
    Then the select returns rows
    When the same session selects from rwb_deviation.deviation
    Then the database refuses the select with a permission error
    When a session as login rwb_source_data selects from recovery.v_ace_account
    Then the select returns rows
    When a session as login rwb_case selects from recovery.v_ace_account
    Then the database refuses the select with a permission error
    Then no login other than rwb_source_data holds a grant on schema recovery
    Then rwb_sandbox_read holds SELECT on schema recovery and its UPDATE is refused

  Scenario: AC4 The 30 views compile and return a row and no clear personal value sits in a service schema (new, D-RCV-60)
    Given the split sandbox is built
    When the verifier compiles each of the 30 v_ace_* views and selects one row from each
    Then 30 of 30 compile and each returns at least one row
    When the verifier scans every column tagged is_personal in the 19 service schemas
    Then no value in rwb_case, rwb_source_data, rwb_document, rwb_deviation or any other service schema matches the 13-digit national ID pattern with a valid check digit, a Thai mobile number or an email address
    Then a clear identity number in public.customer is not a failure, because ACE holds it and v_ace_customer exposes id_no_masked and id_no_last4 only
    Then the build publishes no sandbox from a build in which either check fails

  Scenario: AC5 The same commit and seed rebuild to the same rows (new, D-RCV-60)
    Given the sandbox was built for commit "a1b2c3d" with seed 20261128
    When the build runs again for commit "a1b2c3d" and seed 20261128
    Then a fresh schema public, a fresh schema recovery and fresh service schemas are built in rwb_sandbox_next and swapped in
    Then every table in every one of the 19 schemas holds the same row count as the first build
    Then case "RW-2026-000001" holds the same total_outstanding_at_entry of 1,845,200.00
    Then no row from the first build remains
    When a second build starts while the first runs
    Then the second build waits on the pipeline lock and runs after the first

  Scenario: AC6 A missing dictionary entry or a value that breaks a constraint fails the build and keeps the previous sandbox (new, D-RCV-60)
    Given a dictionary fixture in which the sys_fields row for recovery_case.closure_reason is removed
    When the sandbox build runs
    Then the build fails with "recovery_case.closure_reason has no data dictionary entry"
    Then the previous sandbox stays in use
    Given list LOV-PRODUCT is empty in the seed data
    When the sandbox build runs
    Then the build fails naming table "recovery_case" and column "product_group"
    Then the failure names the constraint that the value broke
    Then the previous sandbox stays in use
```

The six criteria are new (D-RCV-60) and test only the split estate. The nine legacy criteria of RWB-E1-065 are owned by RWB-P1-E1065-APP and re-exercised here as the `-ITG` copies of section 16: the legacy AC1 becomes AC1 and AC2, the legacy AC2 becomes AC3, the legacy AC3 stays with the dictionary-driven rebuild of AC1 and the test migration of TC-E1-065-03-ITG, the legacy AC4 and AC6 become AC6, the legacy AC5 becomes AC5, the legacy AC7 becomes AC4, and the legacy AC8 and AC9 are exercised as the boundary fixture and the pipeline lock.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | No production data in DEV; the sandbox holds synthetic data only | NFR-045; CTL-11 |
| BR2 | The sandbox is built from the same DDL as SIT: the ACE test double for the 22 Tier 1 and 14 Tier 2 tables, the view DDL for the 30 views and the three helper functions, and each service's own Flyway baseline for the 92 tables of RWB-E1-001 | RWB-E1-001; RWB-E1-069; ADR-014; DP-01, DP-15 |
| BR3 | Generated values come from the data dictionary and the lists of values, not from code: `sys_objects` and `sys_fields` in `rwb_source_data`, `lov_value` in `rwb_case` | sys_fields; lov_value; Principle 1; DP-07 |
| BR4 | Exception shapes generated: duplicate case for one customer and product (R-UNI-17), deceased customer (R-UNI-05), bankruptcy (R-UNI-07), open deviation, legal hold (R-UNI-20), unmapped product code, collateral with no account, case with three accounts, accounts at 89 and 90 days past due (DL16), withdrawn consent (R-UNI-10) | rules.txt; DL16 |
| BR5 | Case volumes follow the product split of the 30 June 2026 inventory at 10 percent | DL15 |
| BR6 | Every role has a named test user before it has real users | DL39 |
| BR7 | The ACE-shaped tables (22 Tier 1 and 14 Tier 2) are a DEV test double for ACE, not a copy of source data: they hold synthetic rows only, they are never deployed to SIT, UAT or production, and no table in a service schema is loaded from them by a batch job | D-RCV-35 U1; NFR-045 |
| BR8 | No copy and no load table exists in the sandbox; the 20 tables that left the schema stay absent — `loan_account`, `account_payment`, `party`, `contact_point`, `collateral`, `account_collateral`, `collections_history`, `party_product`, `valuation`, `score`, `asset`, `load_run`, `dq_exception`, `dq_rule`, `source_field_map`, `source_code_map`, `interface_run`, `interface_signoff`, `tracker_inventory` and `tracker_row` — and the services read source data only through `recovery.v_ace_*` | D-RCV-35; ADR-010; DP-05 |
| BR9 | A clear identity number is allowed only in the ACE-shaped tables of schema `public`; every service schema holds masked or synthetic values only | D-RCV-35 U4; CTL-11 |
| BR10 | One schema and one login per service: a table lives in the schema of the service named by the Ownership Map, a login holds rights on its own schema only, and no cross-schema foreign key, view or join exists | Arch v5 slide 29; ADR-014; DP-01 |
| BR11 | The split moves tables, it does not copy them: the estate still holds the 92 tables of RWB-E1-001 once, and the four extension tables `party_ext`, `contact_point_ext`, `account_ext` and `valuation_ext` are `rwb_source_data`'s | Ownership Map v1; DP-05 |
| BR12 | Schema `recovery` holds the 30 `v_ace_*` views and the three helper functions and no table; only the `rwb_source_data` login reads it | Arch v5 slide 29; RWB-E1-069 |
| BR13 | The commit hash and the seed are the idempotency key: the same pair produces the same rows, the same counts per schema and the same values | RWB-E1-065 section 12 |

### 9. State transitions

None for a case status. This story does not change a case status; it changes the sandbox build state in the pipeline.

| Item | States |
|---|---|
| Sandbox build | Building, Published, Failed; a failed build leaves the previous `rwb_sandbox` in use |
| Schema set | Created in `rwb_sandbox_next`, verified, then renamed into place as one set; never half-swapped |
| Table seed | Empty after its baseline, seeded, verified, published |
| Service grant | None before the build, own schema after the rename, refused on every other schema |
| Harness run | Not started, running, passed, failed with the failing criterion, the schema and the table named |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of the integration harness | Owns the harness, the fixtures, the run order and the run report |
| rwb-source-data owner (RWB-P1-E1065-APP) | Owns the generator, the verifier, the value factory, the exception shapes, the access seed and the build stage |
| Wave-1 service teams (RWB-P3-E1065-APP, RWB-P4-E1065-APP, RWB-P5-E1065-APP, RWB-S8-E1065-APP) | Own the rows their service seeds and the Flyway baseline of their own schema |
| ACE team lead and ACE DBA | Own the ACE test-double DDL and the Tier 2 DDL of RWB-ACE-001; approve a change to either |
| RW-PLATADM Platform administrator | Owns the sandbox database, the pipeline stage and the pipeline lock |
| RW-TRIBE Tribe lead and squad members | Read and extract the sandbox, start a manual build |
| Test users per role | Call the DEV service against the sandbox with their role's rights |
| Every service login | Reads and writes its own schema only |
| No role | May update or delete a seeded row by hand; only the build writes the sandbox |

### 11. Data

| BR Field ID | Entity (owning schema) | Field | Read or write |
|---|---|---|---|
| DF-ACE-001 to DF-ACE-177 | the 16 Section A views (`recovery`) | all 177 fields | Seed source; read |
| DF-ACE-178 to DF-ACE-304 | the 14 Section B views (`recovery`) | all 127 fields | Seed source; read |
| DF-CAS-001 to DF-CAS-023, DF-CAS-046 to DF-CAS-055 | `recovery_case` (`rwb_case`) | all 33 fields | Write |
| DF-CAS-024 to DF-CAS-029 | `case_account` (`rwb_case`) | all fields | Write |
| DF-CAS-030 to DF-CAS-035 | `case_party` (`rwb_case`) | all fields | Write |
| DF-CAS-036 to DF-CAS-045 | `deviation` (`rwb_deviation`) | all fields | Write |
| DF-INT-001 to DF-INT-029 | `interaction` (`rwb_source_data`) | all 29 fields | Write |
| DF-DOC-001 to DF-DOC-033 | `document` (`rwb_document`) | all fields | Write |
| DF-DOC-012 to DF-DOC-017, DF-DOC-034 and DF-DOC-035 | `document_field` (`rwb_document`) | all 8 fields | Write |
| DF-EXT-001 to DF-EXT-012 | `party_ext` (`rwb_source_data`) | all fields | Write |
| DF-EXT-013 to DF-EXT-026 | `contact_point_ext` (`rwb_source_data`) | all fields | Write |
| DF-EXT-027 to DF-EXT-035 | `account_ext` (`rwb_source_data`) | all fields | Write |
| DF-EXT-036 to DF-EXT-049 | `valuation_ext` (`rwb_source_data`) | all fields | Write |
| DF-REF-034 to DF-REF-038 | `role` (`rwb_access`) | all 5 fields | Write |
| DF-REF-040 to DF-REF-044 | `permission` (`rwb_access`) | all fields | Write |
| DF-REF-027 | `lov_value` (`rwb_case`) | id | Read |
| DF-REF-028 | `lov_value` (`rwb_case`) | lov_code | Read |
| DF-REF-029 | `lov_value` (`rwb_case`) | value_code | Read |
| DF-REF-097 | `sys_fields` (`rwb_source_data`) | field_name | Read |
| DF-REF-098 | `sys_fields` (`rwb_source_data`) | data_type | Read |
| DF-REF-105 | `sys_fields` (`rwb_source_data`) | is_personal | Read |

The 30 views are `v_ace_account`, `v_ace_payment`, `v_ace_customer`, `v_ace_contact`, `v_ace_ca_relation`, `v_ace_aa_relation`, `v_ace_collateral`, `v_ace_asset`, `v_ace_efs_action`, `v_ace_efs_action_code`, `v_ace_efs_assignment`, `v_ace_bucket_log`, `v_ace_product`, `v_ace_branch`, `v_ace_holiday`, `v_ace_plan`, `v_ace_batch_status`, `v_ace_valuation`, `v_ace_collateral_detail`, `v_ace_npa_asset`, `v_ace_npa_sale`, `v_ace_lawsuit`, `v_ace_hearing`, `v_ace_pod`, `v_ace_write_off`, `v_ace_score`, `v_ace_party_product`, `v_ace_credit_decision`, `v_ace_esign` and `v_ace_iam_group`. The other tables of the 92 are filled the same way from their `sys_fields` rows, each in the schema of its owner. `delegation_limit` (`rwb_access`) stays empty until version DOA-2026.11 is loaded, and `decision_log_entry` (`rwb_decision`) and `interaction` receive their rows from running the Workbench jobs against the sandbox. Field IDs are those in the Logical Data Model and Data Dictionary and are copied from RWB-E1-065. The harness owns no schema, no table and no field; `case_list_row` is P1's own table added by RWB-P1-E1001-APP outside the 92 and is counted separately.

### 12. Contract

#### 12.1 REST operations provided

None. The harness is a test project and provides no REST operation.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| GET | `/api/recovery/case/v1/cases` | P3 rwb-case | Lists the sandbox cases in scope for a DEV test user, and holds the seeded "RW-2026-000001" row |
| GET | `/api/recovery/source-data/v1/customers/{id}` | P1 rwb-source-data | Reads the customer of the case through the ACE view contract |
| GET | `/api/recovery/source-data/v1/accounts/{id}` | P1 rwb-source-data | Reads the account of the case through the ACE view contract |

Every call is one hop to the owning service on its own base (DP-11, DP-13) with the 2 s client budget; the harness calls no service through another service and reads no service schema directly except for the grant, view and count assertions of sections 4 and 13.

#### 12.3 Events published

None. The sandbox build publishes no business event; the pipeline result is a build report, not a topic.

#### 12.4 Events consumed

None. The build and the harness consume no Kafka event; the dictionary, the Ownership Map and the seed files are inputs to the build stage.

#### 12.5 Workflows and activities

None. The build is a pipeline stage and starts no Temporal workflow; the seeded case and its rows are written by the generator, and the jobs that later write `decision_log_entry` and `interaction` belong to their owning services.

#### 12.6 Schedules

None. The sandbox build runs on trigger only, is not a scheduled job and is not in `job_catalog` (RWB-E1-065 section 12).

#### 12.7 Tables owned

None. The build creates the database `rwb_sandbox_next` and applies the baselines of the services, and it owns no table: every table it writes belongs to the service whose schema holds it, as listed in section 11 with its owner.

#### 12.8 Contract fakes

None. This is the integration level: the real build stage, the real database, the 19 real schemas and the real view DDL replace the contract fakes of the service stories. The ACE test double in schema `public` is not a contract fake; it is the DEV stand-in for ACE that the legacy story already required and that BR7 scopes to DEV.

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 0 | 3 | The case list and the two source-data reads, one hop each, 2 s (DP-11, DP-13) |
| Kafka | None | None | No event in this story |
| Temporal | None | None | No workflow, activity or Schedule in this story |
| File | None | None | No file in this story; the seed files are build inputs, not an interface |

### 13. Solution plan

**Deliverables.** One build module `tools/sandbox-generator` (Java package `recovery.tools.sandbox`, a separate build module that is never packaged into an ACE service) delivered by RWB-P1-E1065-APP and the four service slices, and one harness project `integration/recovery-w1/sandbox` delivered by this story, with the six test classes `SplitStandUpIT`, `OwnerSchemaIT`, `LoginIsolationIT`, `ViewAndPdpaIT`, `DeterministicRebuildIT` and `FailurePathIT`, the fixtures of this section and the run-report writer.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| SandboxSchemaLoader | Service | Applies the 22 Tier 1 and 14 Tier 2 tables to `public`, the 30 views and the three helper functions to `recovery`, and each service's own Flyway baseline to its own schema |
| OwnershipMapReader | Service | Reads `Recovery Workbench Microservice Ownership Map v1` and resolves each of the 92 tables to exactly one schema; fails on a table with no owner or two |
| SandboxGenerator | Service | Reads the metadata and writes the synthetic rows table by table in foreign key order, schema `public` first and then each service schema |
| ValueFactory | Service | Produces a value per data type and list, seeded; synthetic names as "SYN-FIRST-000123"; tokens as random 64-character hex |
| ExceptionShapeBuilder | Service | Adds the shapes of BR4, 10 cases each, each row in the schema of the table that holds it |
| SandboxVerifier | Service | View compile and row checks, list, key, cross-schema, personal-data pattern, dictionary and boundary checks across the 19 schemas |
| AccessSeedLoader | Service | Loads 54 roles, the permission matrix and one named test user per role into `rwb_access` |
| SandboxExport | Service | Writes a table of any schema to CSV for the read-only role |
| Sandbox build stage | Job | Pipeline stage: create the database and the schemas, apply the DDL and the 19 baselines, seed, verify, rename, grant, publish the build result |
| HarnessRunner | Runner | Preflight, run order, report and exit code |
| GrantProbe | Service | Connects as each of the 19 service logins and as `rwb_sandbox_read` and asserts the reads that must pass and the refusals that must follow |
| ViewProbe | Service | Compiles each of the 30 views and selects one row from each |
| PdpaProbe | Service | Scans every `is_personal` column in the 19 schemas for a national ID with a valid check digit, a Thai mobile number or an email address |
| DeterminismProbe | Service | Reads the row count of every table in every schema and the `RW-2026-000001` totals, rebuilds with the same commit and seed, and compares |
| FailureFixtureDriver | Service | Applies the dictionary fixture and the empty LOV seed, triggers the build, reads the failure text and confirms the previous sandbox is still in use |
| ReportWriter | Service | One row per test case, with the schema, the table, the evidence and the build state |

The first nine components are built by RWB-P1-E1065-APP and the four service slices and are exercised here; the seven harness components are this story's.

**Database.** None of its own. The build creates `rwb_sandbox_next` and renames it to `rwb_sandbox` from the maintenance connection; the harness writes no row itself, and every row it asserts is written by the generator through the dictionary.

**Configuration and reference data**

- Properties `rwb.sandbox.seed=20261128`, `rwb.sandbox.cases.mortgage=1226`, `rwb.sandbox.cases.hire-purchase=1296`, `rwb.sandbox.cases.ssme=290`, `rwb.sandbox.shape-count=10` and `rwb.sandbox.ace-schema=15 ACE DB Alignment/ACE Schema PostgreSQL v1.sql`, owned by the tech lead.
- The Ownership Map version, the service list and the 19 schema names, all as configuration; no owner name, schema name or table name in code.
- The pipeline lock: one PostgreSQL advisory lock held for the whole build, so a second build waits and runs after the first.
- Lists of values come from the seed migration, roles and permissions from the role seed file, and the product groups, the shape codes and the dictionary rows from the dictionary itself; `LOV-RISK-TIER` and the test column `risk_tier` exist only in the never-shipped test migration of TC-E1-065-03.
- The per-schema seed volumes for each of the 19 schemas, the order in which the 19 baselines are seeded and the cutover from the one `recovery` schema of RWB-E1-065 to the 19 schemas are Not specified in the source documents (GAP-0374; ASM-0537); the build reads the per-schema volumes from configuration and writes the order it used into the run report, and the harness asserts the composition rather than an order the sources do not fix.
- The 2 s client budget, the rebuild wait and the report layout.

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

- DP-01 is the change itself: the 92 tables move from one `recovery` schema to 19 `rwb_*` schemas, and the sandbox asserts that no schema holds another service's table.
- DP-15 is the build: one V0001 baseline of the monolith becomes 19 service baselines, applied one per schema and never across schemas.
- DP-05 is where the four extension tables and the 30 views sit: the views stay in schema `recovery`, only the `rwb_source_data` login reads them, and `party_ext`, `contact_point_ext`, `account_ext` and `valuation_ext` are seeded in `rwb_source_data`.
- DP-07 is how the generator learns values: the dictionary and the lists, never a literal in code; the services themselves read the lists through the rwb-case reference-data contract.
- DP-03 and DP-04 are asserted as shape, not authored here: the sandbox stands up the local `decision_record`, `outbox_event` and `processed_event` objects that each service's own baseline creates, and the rule tables that `rwb_decision` owns, so a seeded case can be worked by the real jobs and the local rule kit; no decision record and no rule package is invented by this story, and the dependencies of DP-03 and DP-04 stay with the services.
- DP-13 is the base of the three calls: the case list and the two source-data reads are consumed on `/api/recovery/<short>/v1`, never on the monolith base.
- DP-19 is where the screens sit: no screen is built here, and the DEV screens reach sandbox cases only through the gateway-bff composite route, so the harness calls the three service APIs directly.

The story carries no H, C or X dependency: the build dependencies of DP-03, DP-04, DP-07, DP-15 and DP-19 stay with the service, platform and operations stories this harness proves. The I list names the five stories whose rows and baselines it exercises, and an integration dependency never blocks a build (Template and Rules §R5.4).

**Fixtures**

| Fixture | Content | Used by |
|---|---|---|
| Seed volume | Seed 20261128; 1,226 Mortgage, 1,296 Hire purchase, 290 SSME; 10 cases per exception shape | AC1, AC2, TC-E1-065-01-ITG |
| Golden case | Case "RW-2026-000001" with its accounts, parties, interactions and documents and `total_outstanding_at_entry` 1,845,200.00 | AC1, AC5, TC-E1-065-01-ITG, TC-E1-065-05-ITG |
| Ownership map set | The 92 tables resolved to their 19 schemas, plus one table with no owner and one with two owners for the refusal | AC2, TC-E1-065-01-ITG |
| Grant set | The 19 service logins, `rwb_source_data`, `rwb_sandbox_read` and one user of RW-REFADM | AC3, TC-E1-065-02-ITG, TC-E1-065-10-ITG |
| Dictionary fixture | The dictionary without the `sys_fields` row for `recovery_case.closure_reason` | AC6, TC-E1-065-04-ITG |
| Empty list fixture | `LOV-PRODUCT` empty in the seed data | AC6, TC-E1-065-06-ITG |
| Personal value fixture | An injected 13-digit national ID with a valid check digit in a service-schema personal column, and a clear value in `public.customer` | AC4, TC-E1-065-07-ITG |
| Boundary accounts | 10 accounts at 89 days past due with no case and 10 at 90 days past due with one open case each, on `v_ace_account` | TC-E1-065-08-ITG |
| Test migration | A never-shipped migration adding `recovery_case.risk_tier` with its `sys_fields` row and `LOV-RISK-TIER` | TC-E1-065-03-ITG |
| Two builds | Two builds started together for commits `a1b2c3d` and `e4f5a6b` | AC5, TC-E1-065-05-ITG, TC-E1-065-09-ITG |

**Run order.** Preflight; the split stand-up (AC1); the ownership and row checks per schema (AC2); the grant probes on all 19 logins (AC3); the 30 views and the personal-data scan (AC4); the two builds for the same commit and seed and the counts per schema (AC5); the dictionary and empty-list failures with the previous sandbox confirmed (AC6); the boundary accounts and the test migration; cleanup of the DEV fixtures; the run report. A failing step stops the run and the report names the criterion, the schema, the table and the evidence.

**Done when.** The 16 test cases of section 16 pass on the split sandbox in DEV, 30 of 30 views compile and return a row, the 92 tables sit in their owners' schemas with no cross-schema reference, all 19 logins are isolated and only `rwb_source_data` reads schema `recovery`, no clear personal value exists in a service schema, the same commit and seed reproduce every per-schema count and the 1,845,200.00 total of "RW-2026-000001", and each failure fixture leaves the previous sandbox published.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-002 | A test user without the right calls the DEV service | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | A test user calls a sandbox case outside their scope | This case is not in your scope. |

The two texts are copied unchanged from RWB-E1-065; the story adds no message text. Build failures are reported in the pipeline result with the schema, the table and the column or constraint named; no user message applies.

### 15. Screens and states

No screen in this story. Developers and analysts read the sandbox with SQL and the export script, and see the build result and the row counts per schema in the pipeline. Screens built in DEV show sandbox cases through the normal endpoints of the gateway-bff composite route, which belongs to RWB-PLT-N001 and is out of scope here. The states this story observes are the build, schema set, table seed, grant and harness-run states of section 9.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-065-01-ITG | AC1, AC2, BR2, BR4, BR5, BR8, BR10, BR11 | Integration | 22 Tier 1 and 14 Tier 2 tables in `public`; 30 views and three helper functions in `recovery`; the 19 baselines; seed 20261128; 2,812 cases plus shapes |
| TC-E1-065-02-ITG | AC3 | Integration | Read-only role query, CSV export and refused UPDATE; a service login refused on another schema |
| TC-E1-065-03-ITG | AC1, BR3 | Integration | Test migration adding `recovery_case.risk_tier` with its dictionary row and `LOV-RISK-TIER` |
| TC-E1-065-04-ITG | AC6, BR3 | Integration | Dictionary fixture without the DF-CAS-023 row for `recovery_case.closure_reason` |
| TC-E1-065-05-ITG | AC5 | Integration | Two builds for commit a1b2c3d and seed 20261128 |
| TC-E1-065-06-ITG | AC6 | Integration | Empty `LOV-PRODUCT` seed |
| TC-E1-065-07-ITG | AC4, BR1, BR9 | Integration | Injected 13-digit value in a service-schema personal column; a clear value in `public.customer` |
| TC-E1-065-08-ITG | AC2, BR4 | Integration | Boundary accounts at 89 and 90 days past due on `v_ace_account` |
| TC-E1-065-09-ITG | AC5 | Integration | Two builds started together, the pipeline lock |
| TC-E1-065-10-ITG | AC3 | Contract | Test user of RW-REFADM calls `GET /api/recovery/case/v1/cases` on the sandbox; refused with MSG-P4-002 |
| TC-ITG-E1065-01 | AC1, BR2, BR10, BR11, BR12 | Integration | `public`, `recovery` and the 19 schemas after the build; 92 tables, 30 views, three helper functions, 122 objects and 1,366 fields |
| TC-ITG-E1065-02 | AC2, BR4, BR10, BR11 | Integration | The Ownership Map set; every table and its rows per schema; 2,812 cases; the boundary test on the 19 schemas |
| TC-ITG-E1065-03 | AC3, BR10, BR12 | Integration | The 19 service logins, `rwb_source_data` and `rwb_sandbox_read`; the reads that pass and the refusals |
| TC-ITG-E1065-04 | AC4, BR9, BR12 | Integration | 30 view compiles and one row each; the `is_personal` scan of the 19 schemas; the clear value in `public.customer` |
| TC-ITG-E1065-05 | AC5, BR13 | End to end | Commit a1b2c3d and seed 20261128 twice; per-schema counts and the 1,845,200.00 total of "RW-2026-000001" |
| TC-ITG-E1065-06 | AC6 | Component | The dictionary fixture and the empty `LOV-PRODUCT` seed; the failure text and the previous sandbox |

The full legacy test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. The nine legacy criteria of RWB-E1-065 are owned by RWB-P1-E1065-APP and re-exercised here on the split estate; the legacy test case IDs are kept as `-ITG` copies, and the six new criteria AC1 to AC6 carry TC-ITG-E1065-01 to TC-ITG-E1065-06.

### 17. Guardrails

- No business value in code: the seed, the volumes, the shape count, the per-schema volumes and the test-double path are properties; values come from the dictionary and the lists (BR3, DP-07).
- No table, column, schema or owner name in the generator or the harness: the generator learns them from `sys_objects` and `sys_fields`, and the sandbox learns the owner from the Ownership Map (BR10).
- No personal data in logs, tests or prompts: every name, identifier and contact value is synthetic, and the verifier blocks a value that looks real in any of the 19 schemas, not only in `document_field`.
- The ACE test double is DEV only and never reaches SIT, UAT or production; no copy of the sandbox goes to another environment (BR7).
- No copy and no load table is created, and the 20 tables that left the schema stay absent (BR8).
- One login per service with rights on its own schema only: the grants, not the tool, enforce the boundary, and the harness proves the refusal on every login (BR10, BR12).
- The build is all or nothing: it works on `rwb_sandbox_next`, swaps only after the verifier passes, and a failed build leaves the previous sandbox in use.
- The pipeline lock is held for the whole build; two builds never write the same database at once.
- The harness never uses production data and never points at a SIT, UAT or production database.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-RDF-001 | 14 data products, each with one system of record and one owner | The Ownership Map; the 19 `rwb_*` schemas and their Flyway baselines; `recovery_case`, `case_account`, `case_party`, `interaction`, `document`, `deviation`, `role`, `permission` in their owners' schemas | TC-E1-065-01-ITG, TC-E1-065-03-ITG, TC-E1-065-08-ITG, TC-ITG-E1065-01, TC-ITG-E1065-02 |
| REQ-RDF-010 | Access per data product by role; personal data masked in line with PDPA | One login per schema; `sys_fields.is_personal`; the 30 `recovery.v_ace_*` views with SELECT to `rwb_source_data` only; role `rwb_sandbox_read`; `GET /api/recovery/case/v1/cases` and the two source-data reads | TC-E1-065-02-ITG, TC-E1-065-07-ITG, TC-E1-065-10-ITG, TC-ITG-E1065-03, TC-ITG-E1065-04 |

### 19. Out of scope

- The generator, the verifier, the value factory and the build stage themselves (RWB-P1-E1065-APP), and the rows each service seeds in its own schema (RWB-P3-E1065-APP, RWB-P4-E1065-APP, RWB-P5-E1065-APP, RWB-S8-E1065-APP).
- The 19 schemas, their logins and the per-service Flyway sequence as a deliverable (the per-service DB stories and RWB-PLT-NF06-DB).
- The ACE Tier 2 DDL and the 14 Section B tables of RWB-ACE-001, which the ACE team owns.
- The 30 views, their grants and the view conformance test (RWB-E1-069, RWB-P1-E1069-APP).
- The dictionary content and its change process (RWB-E1-064).
- Masked copies of production data in SIT and UAT (RWB-TE-004).
- The rule scenario build gate (RWB-E1-073) and the performance test harness (RWB-TE-009).
- The PDPA lint for code, tests and logs (RWB-TE-011).
