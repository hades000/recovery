# RWB-P1-E1065-APP Sandbox database with synthetic recovery data

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P1-E1065-APP |
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
| Ready to start | After RWB-P1-E1001-APP, RWB-P1-E1069-APP |
| Depends on (build) | RWB-P1-E1065-CON, RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, RWB-PLT-E1043-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON, RWB-P1-E1001-APP, RWB-P1-E1069-APP |
| Contract dependencies | RWB-P3-E1043-CON |
| Integration dependencies | None |
| External dependencies | RWB-P1-E1065-DB |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v1.md (FR-P1-001, FR-P1-006, FR-P1-007, FR-P1-008, FR-P1-010, FR-P1-012, FR-P1-013, FR-P1-024, FR-P1-025, FR-P1-029, FR-P1-030) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-065 for rwb-source-data. The sandbox becomes a build tool of this service rather than a step of a monolith pipeline: `tools/sandbox-generator` in package `th.co.scb.ace.workbench.recovery.sourcedata.sandbox`, a separate build module that is never packaged into the service, creates `rwb_sandbox` on the one ACE PostgreSQL server with schema `public` as the ACE test double, schema `recovery` holding the 30 read-only views and schema `rwb_source_data` holding this service's own tables and the four extension tables (DP-01, DP-02, DP-05; Architecture v5 slides 8, 15, 29 and 41). The nine legacy acceptance criteria are copied here word for word and the generator, verifier, export tool and pipeline stage move with them; the login, the grants and the extension tables are RWB-P1-E1065-DB, the contract baseline is RWB-P1-E1065-CON. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **recovery developer (RW-TRIBE)**, I want **a sandbox build tool of rwb-source-data that stands up `rwb_sandbox` on the one ACE PostgreSQL server from the same DDL as SIT, with schema `public` as the ACE test double, schema `recovery` holding the 30 read-only `v_ace_*` views and schema `rwb_source_data` holding this service's own tables and the four extension tables, all filled with synthetic rows**, so that **I can build and test every read before the ACE interfaces are available and without production data, in DEV only and with no second copy of source data**.

This is the application slice of legacy RWB-E1-065, and it owns all nine legacy acceptance criteria. It delivers:

- `tools/sandbox-generator`, Java package `th.co.scb.ace.workbench.recovery.sourcedata.sandbox`, a separate build module that is never packaged into the service artefact;
- `AceSchemaLoader`, `SandboxGenerator`, `ValueFactory`, `ExceptionShapeBuilder`, `SandboxVerifier`, `AccessSeedLoader` and `SandboxExport`, and the sandbox build stage that runs them (DP-15);
- the seed profile as data: seed 20261128, 1,226 Mortgage, 1,296 Hire purchase and 290 SSME cases, 10 cases per exception shape, every value overridable;
- the dictionary-driven fill, so that a schema change reaches the sandbox with no generator change (DP-01, DP-15);
- the lists of values read through the rwb-case reference-data contract (DP-07), and the embedded Drools kit that evaluates the seeded rule packages in the sandbox smoke check (DP-04).

It does not create the 30 `recovery.v_ace_*` views, which are RWB-P1-E1069-APP's; it does not create the `rwb_source_data` login, the grants or the read-only role `rwb_sandbox_read`, which are RWB-P1-E1065-DB's (external dependency X), nor the four extension tables, which are RWB-P1-E1069-DB's; and it writes no table of another service (DP-01). It asserts the views, the tables and the grants those two stories deliver and re-creates none of them.

### 2. Business rationale

SIT reads the real ACE database; DEV has none. Without an ACE-shaped schema the 30 `recovery.v_ace_*` views cannot compile, so no squad can test a source read, the case list, a notice or a report before SIT is connected. Since the realignment, that schema has to stand up inside a single service: rwb-source-data is the one service that holds the views and the ACE read path (Architecture v5 slides 8, 15 and 41), so the sandbox belongs to rwb-source-data and serves the other 18 services through the read contract rather than through a shared database object they each read.

The sandbox applies the ACE schema for the Tier 1 tables, the RWB-ACE-001 DDL for the 14 Tier 2 tables as a fixture, the per-service Flyway baseline and view migrations for this service's tables and the 30 views, and it fills the ACE-shaped tables with synthetic source rows and the service's own tables with synthetic cases across Mortgage, Hire Purchase and SSME, plus the exception shapes the rules must handle (DP-01, DP-02, DP-15).

There is no copy and no load table: `loan_account`, `account_payment`, `party`, `contact_point`, `collateral`, `account_collateral`, `collections_history`, `party_product`, `valuation`, `score`, `asset`, `load_run`, `dq_exception`, `dq_rule`, `source_field_map`, `source_code_map`, `interface_run`, `interface_signoff`, `tracker_inventory` and `tracker_row` do not exist. The generator reads the data dictionary, so a schema change reaches the sandbox with no manual rebuild, and the verifier allows a clear identity number only in the ACE-shaped tables, where ACE itself holds it; schema `recovery` and schema `rwb_source_data` see `id_no_masked` and `id_no_last4` only. Serves REQ-RDF-001 (the 14 data products with one system of record and one owner) and REQ-RDF-010 (no personal data outside its permitted use).

### 3. Preconditions

- RWB-P1-E1001-APP is done: the per-service Flyway baseline creates this service's 13 tables, `data_product`, the 122 `sys_objects` rows, the 1,366 `sys_fields` rows and the four extension tables on rwb-source-data's own sequence (legacy RWB-E1-001 in the target; DP-15).
- RWB-P1-E1069-APP is done: the per-service sequence holds the two view migrations that create the 30 `recovery.v_ace_*` views, their three helper functions and their dictionary rows, and the `ViewConformanceTest` that compares them with the dictionary.
- The ACE schema DDL `15 ACE DB Alignment/ACE Schema PostgreSQL v1.sql` is in the repository. It holds the Tier 1 tables, among them `account`, `payment`, `customer`, `efs_action` and `iam_user`.
- The RWB-ACE-001 DDL for the 14 Tier 2 tables is available in DEV as a fixture (DL43); until it lands, the 14 Section B views and the features that read them stay behind their flags.
- The one ACE PostgreSQL server is reachable from the pipeline, and the DEV instance holds the database `rwb_sandbox`, or the stage creates it as `rwb_sandbox_next` and renames it (RWB-P1-E1065-DB; Architecture v5 slides 8, 9 and 29).
- The read-only database role `rwb_sandbox_read` is delivered by RWB-P1-E1065-DB, and the Entra ID group RWB-DEV-RW-TRIBE maps to it.
- The role to permission matrix rows (roles.txt, Permissions) are available as a seed file for the sandbox.
- A consuming service, starting with rwb-case, can be deployed in DEV against the sandbox database through the rwb-source-data read contract; this story neither deploys it nor changes it.
- RWB-P3-E1043-CON is published with its client library, so a list of values is read as data and never as a constant (DP-07).
- RWB-P1-E1065-CON is published, so the stage contract, the seed profile and the failure contract are fixed before the generator is written.
- Whether the 19-service target keeps one sandbox database per service or one shared sandbox across the 19 services, and where the generator's build module sits relative to the service artefact, are Not specified in the source documents (GAP-0501; ASM-0693). This story is read as one DEV sandbox database per service release, `rwb_sandbox` for rwb-source-data, with the generator as a separate build module of the rwb-source-data repository that the service artefact does not contain.

### 4. Flow

1. Pipeline: on a merge to main that changes the ACE schema DDL, a file under the rwb-source-data migration folder, the dictionary or the seed profile, or on a manual start, runs the sandbox build stage in DEV.
2. Pipeline: creates the database `rwb_sandbox_next` and its three empty schemas, `public`, `recovery` and `rwb_source_data` (RWB-P1-E1065-DB).
3. Pipeline: applies `ACE Schema PostgreSQL v1.sql` (the Tier 1 tables) and the RWB-ACE-001 DDL fixture (the 14 Tier 2 tables) into schema `public`, then the per-service Flyway baseline (this service's 13 tables, the four extension tables and the dictionary) and the two view migrations of RWB-P1-E1069-APP into schema `recovery` (DP-15; RWB-PLT-E1044-CON).
4. SandboxGenerator: reads `sys_objects`, `sys_fields` and the lists of values to learn every table, column, type and list, and reads every list of values through the rwb-case reference-data contract rather than from a constant (DP-07).
5. SandboxGenerator: seeds the Tier 1 and Tier 2 ACE-shaped tables with synthetic rows, including one `ace_batch_run` row per source and business date.
6. SandboxGenerator: creates synthetic cases with seed 20261128: 1,226 Mortgage, 1,296 Hire purchase and 290 SSME (10 percent of the 30 June 2026 inventory; DL15), with their accounts, parties, contact points, collateral, valuations, payments and interactions, linked by business key to the ACE-shaped rows.
7. SandboxGenerator: adds 10 cases for each exception shape in section 8, BR4.
8. SandboxGenerator: seeds the role and permission rows and one synthetic test user reference per role; the roles themselves are reference data of rwb-case (DP-07).
9. SandboxVerifier: checks that the 30 views compile and each returns a row, that every seeded table has rows, that every list-backed column holds list values, that every foreign key resolves, that no clear personal value sits outside schema `public`, and that the boundary accounts exist.
10. Smoke check: the embedded Drools kit evaluates the seeded rule packages against the generated cases and records one decision record per evaluation through the decision-record library (DP-03, DP-04).
11. Pipeline: renames `rwb_sandbox_next` to `rwb_sandbox` under the advisory lock, applies the grants of RWB-P1-E1065-DB, and publishes the build result with the row count per table.
12. Developer or analyst: queries the sandbox with SQL or the export script, or calls the DEV service, without a request to another team.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A table column has no `sys_fields` row | Build fails naming the table and column; previous sandbox kept | None (pipeline result) | AC4 |
| X2 | The reset runs twice for the same commit and seed | The schemas are dropped and recreated; the same seed gives the same rows and counts | None | AC5 |
| X3 | A generated value breaks a constraint | Build fails naming the table and constraint; previous sandbox kept | None (pipeline result) | AC6 |
| X4 | A generated value outside schema `public` matches a personal data pattern | Build fails naming the table and column | None (pipeline result) | AC7 |
| X5 | Accounts sit at the 90 days past due boundary | Accounts at 89 and at 90 days past due are both generated | None | AC8 |
| X6 | A second build starts while one runs | The second build waits on the PostgreSQL advisory lock and runs after the first | None | AC9 |
| X7 | The RWB-ACE-001 DDL fixture is not yet available in DEV | The build stops before the Section B view migration; the Section A views and the service's own tables are still built and published | None (pipeline result) | AC1 |
| X8 | The reference-data read of rwb-case does not answer | The build fails closed before any row is written, names the missing list and keeps the previous sandbox | None (pipeline result) | AC6, section 12.2 |
| X9 | The verifier finds a table, view or grant that RWB-P1-E1065-DB or RWB-P1-E1069-APP delivers and the sandbox does not hold | The build fails on the delivered-objects check and publishes nothing, because the sandbox asserts those objects and never re-creates them | None (pipeline result) | AC1 |

X1 to X7 are the exception paths of RWB-E1-065 carried onto the split; X8 and X9 are the two paths the target adds, one for the reference-data contract and one for the two stories that deliver the views, the grants and the extension tables.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the baseline and the view migrations of two sibling stories and, for Section B, the Tier 2 DDL fixture; it publishes the environment every squad tests in |
| Negotiable | Volumes, seed and exception shapes are properties; the story fixes the generator, the checks and the access |
| Valuable | Every squad builds and tests every view read from the first day with no production data |
| Estimable | One generator tool, one verifier, one pipeline stage, one read-only role |
| Small | Finished inside two weeks with its tests, as the primary slice of the legacy key |
| Testable | Each criterion is a pipeline test or a query against the built sandbox |

### 7. Acceptance criteria

```gherkin
Feature: Sandbox database with synthetic recovery data

  Background:
    Given the sandbox build uses seed 20261128
    Given volumes of 1,226 Mortgage, 1,296 Hire purchase and 290 SSME cases

  Scenario: AC1 The sandbox exists (legacy RWB-E1-065 AC1)
    Given the ACE schema DDL with 22 Tier 1 tables, the RWB-ACE-001 DDL with 14 Tier 2 tables, V0001, V0002 and V0003
    When the sandbox is provisioned
    Then schema public holds the ACE schema, including the 22 Tier 1 tables and the 14 Tier 2 tables
    Then schema recovery holds 92 tables, including party_ext, contact_point_ext, account_ext and valuation_ext
    Then schema recovery holds 30 v_ace_* views and 30 of 30 compile
    Then each of the 30 views returns at least one row
    Then the dictionary holds 122 objects and 1,366 fields
    Then the sandbox holds 2,812 synthetic cases plus 10 cases for each exception shape, across Mortgage, Hire Purchase and SSME
    Then case "RW-2026-000001" has its accounts, parties, interactions and documents linked
    Then none of the 20 tables that left the schema exists in schema recovery: loan_account, account_payment, party, contact_point, collateral, account_collateral, collections_history, party_product, valuation, score, asset, load_run, dq_exception, dq_rule, source_field_map, source_code_map, interface_run, interface_signoff, tracker_inventory and tracker_row

  Scenario: AC2 It is readable and extractable (legacy RWB-E1-065 AC2)
    Given the sandbox
    When a member of RWB-DEV-RW-TRIBE runs "SELECT product_group, count(*) FROM recovery.recovery_case GROUP BY product_group"
    Then the result shows MORTGAGE, HIRE_PURCHASE and SSME with their counts
    Then the export script writes recovery_case to a CSV file without a request to another team
    Then the system refuses an UPDATE by the same database role

  Scenario: AC3 It scales with the schema (legacy RWB-E1-065 AC3)
    Given a test migration, never shipped, adds column "risk_tier varchar(10)" to recovery_case with its sys_fields row and list LOV-RISK-TIER
    When it is applied
    Then the sandbox rebuild fills risk_tier with values from LOV-RISK-TIER on every case
    Then no generator code was changed

  Scenario: AC4 A column with no dictionary entry (legacy RWB-E1-065 AC4)
    Given a dictionary fixture in which the sys_fields row for recovery_case.closure_reason is removed
    When the sandbox build runs
    Then the build fails with "recovery_case.closure_reason has no data dictionary entry"
    Then the previous sandbox stays in use

  Scenario: AC5 The reset is idempotent (legacy RWB-E1-065 AC5)
    Given the sandbox was built for commit "a1b2c3d" with seed 20261128
    When the build runs again for commit "a1b2c3d" and seed 20261128
    Then a fresh schema public and a fresh schema recovery are built in rwb_sandbox_next and swapped in
    Then every seeded table holds the same row count
    Then case "RW-2026-000001" holds the same total_outstanding_at_entry of 1,845,200.00
    Then no row from the first build remains

  Scenario: AC6 A generated value breaks a constraint (legacy RWB-E1-065 AC6)
    Given list LOV-PRODUCT is empty in the seed data
    When the sandbox build runs
    Then the build fails naming table "recovery_case" and column "product_group"
    Then the previous sandbox stays in use

  Scenario: AC7 No clear personal value outside the ACE tables (legacy RWB-E1-065 AC7)
    Given the verifier scans every column of schema recovery tagged is_personal
    When a generated value in recovery.document_field.extracted_value matches the 13-digit national ID pattern with a valid check digit
    Then the build fails naming recovery.document_field.extracted_value
    Then a clear identity number in public.customer is not a failure, because ACE holds it and v_ace_customer exposes id_no_masked and id_no_last4 only
    Then the system publishes no sandbox from that build

  Scenario: AC8 Accounts at the entry boundary (legacy RWB-E1-065 AC8)
    Given the exception shapes include the entry boundary
    When the sandbox is provisioned
    Then 10 accounts in v_ace_account have days_past_due 89 and no case
    Then 10 accounts in v_ace_account have days_past_due 90 and one open case each

  Scenario: AC9 Two builds at once (legacy RWB-E1-065 AC9)
    Given a sandbox build is running for commit "a1b2c3d"
    When a second build starts for commit "e4f5a6b"
    Then the second build waits until the first ends
    Then the sandbox after both holds the data for commit "e4f5a6b"
```

**Target reading.** Every assertion above keeps its legacy wording; what changes is where it runs and who delivers the objects. The sandbox becomes a build tool of rwb-source-data: `tools/sandbox-generator`, package `th.co.scb.ace.workbench.recovery.sourcedata.sandbox`, a separate build module that is never packaged into the service artefact, because a build tool must not read or write another service's tables at run time (DP-01; Architecture v5 slides 8, 15 and 41). It creates `rwb_sandbox` on the one ACE PostgreSQL server in three schemas: schema `public` as the ACE test double (the Tier 1 tables and the RWB-ACE-001 Tier 2 tables), schema `recovery` holding the 30 read-only `v_ace_*` views, and schema `rwb_source_data` holding this service's 13 tables and the four extension tables `party_ext`, `contact_point_ext`, `account_ext` and `valuation_ext` (DP-01, DP-02, DP-05). The legacy line "schema recovery holds 92 tables" keeps its wording as the criterion of RWB-E1-065; in the target those tables sit in schema `rwb_source_data` on the sandbox database, and the criterion is executed against the objects the baseline delivers, not against a second copy.

The DDL the stage applies is the ACE schema file `15 ACE DB Alignment/ACE Schema PostgreSQL v1.sql` and the RWB-ACE-001 Tier 2 DDL held as a fixture, then the per-service Flyway baseline and the two view migrations of RWB-P1-E1069-APP on rwb-source-data's own sequence (DP-15; RWB-PLT-E1044-CON). The lists of values are read through the rwb-case reference-data contract on base `/api/recovery/case/v1` and never from a constant (DP-07; section 12.2). The embedded Drools kit (DP-04) evaluates the seeded rule packages in the sandbox smoke check, so a case that meets an exception shape is also a case the rules can decide. The sandbox is DEV only and is never deployed to SIT, UAT or PROD.

The four extension tables and the 30 views are delivered by RWB-P1-E1069-DB and RWB-P1-E1069-APP; the sandbox asserts them in its verifier and never re-creates them, so the criteria that name those objects are executed once, where they are delivered (X9). No criterion here reaches another service over a contract at run time, so no contract-mock Given line is added, and no legacy line is dropped or reworded.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | No production data in DEV; the sandbox holds synthetic data only | NFR-045; CTL-11 |
| BR2 | The sandbox is built from the same DDL as SIT: the ACE schema for the Tier 1 tables, the RWB-ACE-001 DDL for the 14 Tier 2 tables, and the per-service baseline and view migrations for this service's tables and the 30 views | RWB-E1-001; RWB-E1-069; ADR-001 |
| BR3 | Generated values come from the data dictionary and the lists of values, not from code | sys_fields; lov_value; Principle 1 |
| BR4 | Exception shapes generated: duplicate case for one customer and product (R-UNI-17), deceased customer (R-UNI-05), bankruptcy (R-UNI-07), open deviation, legal hold (R-UNI-20), unmapped product code, collateral with no account, case with three accounts, accounts at 89 and 90 days past due (DL16), withdrawn consent (R-UNI-10) | rules.txt; DL16 |
| BR5 | Case volumes follow the product split of the 30 June 2026 inventory at 10 percent | DL15 |
| BR6 | Every role has a named test user before it has real users | DL39 |
| BR7 | The ACE-shaped tables are a DEV test double for ACE, not a copy of source data: they hold synthetic rows only, they are never deployed to SIT, UAT or production, and no service table is loaded from them by a batch job | D-RCV-35 U1; NFR-045 |
| BR8 | No copy and no load table exists in the sandbox; the 20 tables that left the schema are absent, and every service reads source data only through this service's contract or its own `v_ace_*` views | D-RCV-35; ADR-010 |
| BR9 | A clear identity number is allowed only in the ACE-shaped tables; schema `recovery` and schema `rwb_source_data` hold masked or synthetic values only | D-RCV-35 U4; CTL-11 |

**Where each rule lives in the target.** BR1, BR4, BR5 and BR6 are the seed profile and the verifier of this story and stay as data, not as code. BR2 is the DDL set the stage applies, and it now names the per-service baseline and the two view migrations instead of the monolith's V0001 to V0003 (DP-15). BR3 and BR7 are enforced by the generator and the verifier here; BR7's deployment gate is a check of RWB-P1-E1065-DB, which refuses any target other than DEV. BR8 is asserted here over the built sandbox: the 20 absent tables are absent in every schema of the database, and the service reads source data only through the 30 views (DP-01, DP-05). BR9 is the personal-data pattern check of the verifier, which scans every column tagged `is_personal` outside schema `public`. BR2, BR3, BR8 and BR9 are also proven across the other 18 logins by the integration slice; this story proves them inside rwb-source-data.

### 9. State transitions

None. This story does not change a case status. It changes the sandbox build state in the pipeline: Building, Published or Failed.

| From | Event | Condition | To |
|---|---|---|---|
| no sandbox for the commit | the stage starts | A trigger fires and the advisory lock is free | Building, in `rwb_sandbox_next` |
| Building | the verifier passes | Every check of section 4 step 9 passes | Published: `rwb_sandbox_next` is renamed to `rwb_sandbox` |
| Building | the verifier fails | X1, X3, X4, X6, X8 or X9 | Failed: the previous `rwb_sandbox` stays in use |
| Building | a second build starts | The advisory lock is held | Waiting, then Building after the first ends |
| Published | a schema, dictionary or seed change | A merge to main or a manual start | Building again |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-TRIBE, tribe lead and squad members | Read and extract the sandbox through the read-only role `rwb_sandbox_read`; start a manual build |
| RW-PLATADM, platform administrator | Owns the sandbox database, the pipeline stage and the build result |
| Test users per role | Call the DEV service against the sandbox with their role's rights |
| ACE team lead and ACE DBA | Own the ACE schema DDL used as the test double and the Tier 2 DDL of RWB-ACE-001; approve a change to either |
| Recovery tech lead | Owns the seed profile, the seed value and the schema file properties |
| No approval level from the delegation of authority applies | The story takes no business decision |

The generator's build module and the service artefact are separated on purpose: the module runs in the pipeline under a build identity, the service runs in the cluster under the `rwb_source_data` login, and no credential of either appears in a migration, a script or a runbook.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-ACE-001 to DF-ACE-177 | the 16 Section A views | all 177 fields | Seed source; read |
| DF-ACE-178 to DF-ACE-304 | the 14 Section B views | all 127 fields | Seed source; read |
| DF-CAS-001 to DF-CAS-023, DF-CAS-046 to DF-CAS-055 | recovery_case | all 33 fields | Write |
| DF-CAS-024 to DF-CAS-029 | case_account | all fields | Write |
| DF-CAS-030 to DF-CAS-035 | case_party | all fields | Write |
| DF-CAS-036 to DF-CAS-045 | deviation | all fields | Write |
| DF-INT-001 to DF-INT-029 | interaction | all 29 fields | Write |
| DF-DOC-001 to DF-DOC-033 | document | all fields | Write |
| DF-DOC-012 to DF-DOC-017, DF-DOC-034 and DF-DOC-035 | document_field | all 8 fields | Write |
| DF-EXT-001 to DF-EXT-012 | party_ext | all fields | Write |
| DF-EXT-013 to DF-EXT-026 | contact_point_ext | all fields | Write |
| DF-EXT-027 to DF-EXT-035 | account_ext | all fields | Write |
| DF-EXT-036 to DF-EXT-049 | valuation_ext | all fields | Write |
| DF-REF-034 to DF-REF-038 | role (P4 owner; read as reference data) | all 5 fields | Read |
| DF-REF-040 to DF-REF-044 | permission (P4 owner; read as reference data) | all fields | Read |
| DF-REF-027 | lov_value (P3 owner; read through the reference-data contract) | id | Read |
| DF-REF-028 | lov_value (P3 owner; read through the reference-data contract) | lov_code | Read |
| DF-REF-029 | lov_value (P3 owner; read through the reference-data contract) | value_code | Read |
| DF-REF-097 | sys_fields | field_name | Read |
| DF-REF-098 | sys_fields | data_type | Read |
| DF-REF-105 | sys_fields | is_personal | Read |

The 30 views are `v_ace_account`, `v_ace_payment`, `v_ace_customer`, `v_ace_contact`, `v_ace_ca_relation`, `v_ace_aa_relation`, `v_ace_collateral`, `v_ace_asset`, `v_ace_efs_action`, `v_ace_efs_action_code`, `v_ace_efs_assignment`, `v_ace_bucket_log`, `v_ace_product`, `v_ace_branch`, `v_ace_holiday`, `v_ace_plan`, `v_ace_batch_status`, `v_ace_valuation`, `v_ace_collateral_detail`, `v_ace_npa_asset`, `v_ace_npa_sale`, `v_ace_lawsuit`, `v_ace_hearing`, `v_ace_pod`, `v_ace_write_off`, `v_ace_score`, `v_ace_party_product`, `v_ace_credit_decision`, `v_ace_esign` and `v_ace_iam_group`. The other tables of this service are filled the same way from their `sys_fields` rows; `delegation_limit` stays empty until version DOA-2026.11 is loaded, and `decision_log_entry` and `interaction` receive their rows from running the Workbench jobs against the sandbox. Field IDs are those in the Logical Data Model and Data Dictionary.

**Which side is this story's.** The 22 `DF-` families above are this story's seed: the generator writes those rows into the sandbox and the verifier reads them back. The four `DF-EXT-` families are seeded here into tables that RWB-P1-E1065-DB creates, and the 30 `DF-ACE-` families are seeded here into views that RWB-P1-E1069-APP creates; neither table nor view is created by this story. The dictionary rows `DF-REF-` are this service's own metadata, delivered by the baseline of RWB-P1-E1001-APP.

**Where the case rows live.** The field list above is the legacy list and is kept as it stands, because it is what the sandbox has to produce. The tables it names are not this service's in the target: `recovery_case`, `case_account`, `case_party` and `deviation` belong to rwb-case and rwb-deviation, and `document` and `document_field` to rwb-document (Ownership Map v1). The sandbox database holds three schemas only — `public`, `recovery` and `rwb_source_data` — so the synthetic case is held where this service owns the row: the `case_list_row` projection (case number, product group, status, entry date, days past due and total outstanding), `interaction`, `dp_treatment`, `dp_guarantee_claim` and `efs_ledger_outcome`, with the account, party, collateral and valuation keys carried as business keys. That keeps the generator inside its own schema (DP-01), keeps the sandbox to one service's release, and leaves the case record of rwb-case, the document store of rwb-document and the deviation record of rwb-deviation to their own stories and their own sandbox slices. The SQL text of AC2 and AC5 that names `recovery.recovery_case` is the legacy text and is executed against the sandbox's case projection; the meaning of the criterion, the three product groups with their counts and the one case with its linked rows, is unchanged.

### 12. Contract

#### 12.1 REST operations provided

None. This story delivers a build tool and a pipeline stage; it publishes no operation. The read contract of the service is RWB-P1-E1069-APP's, on base `/api/recovery/source-data/v1` (DP-13), and this story neither adds a path to it nor documents one as provided.

#### 12.2 REST operations consumed

One read, at build time only.

| Method | Path | Owner | Use | Pattern |
|---|---|---|---|---|
| GET | Not specified in the source documents (GAP-0501; ASM-0693); read as `/api/recovery/case/v1/reference-data/{tableCode}` | P3 rwb-case | Every list of values the generator needs, read as data per `tableCode` instead of being written in code, once per build and cached for the run | DP-07; one hop, 2 s timeout, no retry beyond the client default |

The reference-data path of rwb-case is not named in the source set of this run, so the row carries the placeholder and the reading fixed above: the family is read through the published RWB-P3-E1043-CON client library on base `/api/recovery/case/v1`, and the exact path is settled in that contract's review. A read that does not answer fails the build closed before any row is written (X8), and the generator never falls back to a constant or to a copy of a list.

#### 12.3 Events published

None. The topic of the service is `rwb.source-data.events.v1` with event names `rwb.source-data.<Event>.v1` (DP-14), and its two events `AceDataReady` and `AceDataLate` belong to RWB-P1-E1013-APP. A sandbox build is a pipeline run, not a business fact, so it writes no outbox row and publishes nothing.

#### 12.4 Events consumed

None. The service consumes no event in Architecture v5 slide 15 ("none: Airflow call; fallback polls ACE batch record"), and a build tool subscribes to nothing.

#### 12.5 Workflows and activities

None. The sandbox build stage calls no Temporal workflow and no activity, because it runs in the pipeline and not in the cluster; the task queue of the service is `rwb-source-data` in namespace `rwb-recovery`, and the workflows `AceIngestCheck` and `reconciliation` and the activities `listEligibleAccounts` and `snapshot(page)` of Architecture v5 slide 15 are other P1 stories. The only process this story starts is the pipeline job of 12.6.

#### 12.6 Schedules

**Pipeline stage**

| Item | Value |
|---|---|
| Trigger | Merge to main that changes the ACE schema DDL, a file under the rwb-source-data Flyway migration folder, the dictionary or the seed profile; manual start by RW-TRIBE or RW-PLATADM |
| Job name | Sandbox build, a DEV pipeline stage of the rwb-source-data repository; not a scheduled job, not a Temporal Schedule and not in `job_catalog` |
| Schedule | On trigger only |
| Input | `ACE Schema PostgreSQL v1.sql`; the RWB-ACE-001 Tier 2 DDL as a fixture; the per-service Flyway baseline and the two view migrations of RWB-P1-E1069-APP; `sys_objects`, `sys_fields` and the lists of values after migration; the role and permission seed file; the seed profile properties of section 13 |
| Output | Database `rwb_sandbox` with schema `public` (the ACE test double, the Tier 1 and Tier 2 tables), schema `recovery` (the 30 views) and schema `rwb_source_data` (this service's 13 tables and the four extension tables) holding synthetic rows; the build report with the row count per table and the verifier result |
| Events published | None |
| Idempotency key | Commit hash and seed. The same pair produces the same rows |
| Restart behavior | The build works on `rwb_sandbox_next` and renames it to `rwb_sandbox` only after the verifier passes, under one PostgreSQL advisory lock; a failed build leaves the previous sandbox and no partial database |

The stage is the only "schedule" this story has, and it is deliberately not a Temporal Schedule: it is a release activity, not a business timer. The contract of the stage itself — its inputs, outputs, seed profile, failure contract and fixtures — is the deliverable of RWB-P1-E1065-CON.

#### 12.7 Tables owned

None created in schema `rwb_source_data` by this story. The objects the stage stands up in the sandbox database are these, and each keeps its own owner:

| Object in `rwb_sandbox` | Schema | Owner (ownership map) | This story |
|---|---|---|---|
| the ACE-shaped test double: the Tier 1 tables and the 14 Tier 2 tables | `public` | ACE team (schema `public` is ACE's) | Created as a test double from the ACE schema file and the Tier 2 DDL fixture and filled with synthetic rows; never deployed outside DEV |
| the 30 `v_ace_*` views and the three helper functions | `recovery` | View owner `ace_view_owner`; contract owner P1 | **Not created here**: RWB-P1-E1069-APP creates them; the verifier asserts 30 of 30 compile and return a row |
| `party_ext`, `contact_point_ext`, `account_ext`, `valuation_ext` | `rwb_source_data` | P1 | **Not created here**: RWB-P1-E1069-DB creates them; the verifier asserts their columns and keys |
| `case_list_row`, `data_contract`, `data_product`, `data_product_access`, `data_product_load`, `dp_guarantee_claim`, `dp_treatment`, `efs_ledger_outcome`, `interaction`, `reconciliation_result`, `sys_field_version`, `sys_fields`, `sys_objects` — the 13 tables of P1 in the ownership map | `rwb_source_data` | P1 | Created by the per-service baseline that the stage applies; the baseline itself is RWB-P1-E1001-APP's and this story writes no row of it |
| the read-only role `rwb_sandbox_read` and its grants | database | P1 (sandbox), credential by the platform DB owner | **Not created here**: RWB-P1-E1065-DB creates the role and issues the grants |

`lake_copy_watermark` is in the ownership map but has no target, because the data lake is removed (DP-17), so it is not in the 13 and the generator does not seed it. No table of another service is created, altered or read, and no foreign key crosses a schema (DP-01).

#### 12.8 Contract fakes

| Fixture | Serves | Used by |
|---|---|---|
| ACE head fixture | `ACE Schema PostgreSQL v1.sql` | The Tier 1 tables of the test double on every build |
| Tier 2 DDL fixture | The RWB-ACE-001 DDL (DL43) | The 14 Tier 2 tables while RWB-ACE-001 is not deployed in DEV (X7) |
| Reference-data fake | RWB-P3-E1043-CON | Every list of values, answered per `tableCode` with a granted answer, an empty list and a timeout (X8) |
| Delivered-tables fixture | RWB-P1-E1001-APP, RWB-P1-E1069-APP and RWB-P1-E1065-DB | A container with the baseline, the 30 views and the four extension tables, so the verifier asserts the real objects instead of a second definition (X9) |
| Seed profile fixture | RWB-P1-E1065-CON | Seed 20261128, the three volumes, the shape count and the LOV source, so a changed volume is a diff and not a code change |

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | None | 1 operation at build time (`/api/recovery/case/v1` reference data, DP-07) | One hop, 2 s timeout; the exact path is settled in RWB-P3-E1043-CON |
| Kafka | None | None | The topic `rwb.source-data.events.v1` belongs to other P1 stories |
| Temporal | None | None | A pipeline stage, not a workflow; queue `rwb-source-data` is not used here |
| File | None | The DDL files and the CSV export | The ACE schema file and the Tier 2 DDL fixture are read at build time; the export writes a CSV for the read-only role |
| SQL view | The 30 `recovery.v_ace_*` views are seeded and read | The ACE-shaped tables behind them | SELECT and seed only, in DEV only |

### 13. Solution plan

**Package.** Folder `tools/sandbox-generator`, Java package `th.co.scb.ace.workbench.recovery.sourcedata.sandbox`, built as a separate build module of the rwb-source-data repository and never packaged into the service artefact. Service base `/api/recovery/source-data/v1` (not used here), schema `rwb_source_data`, views in schema `recovery`, sandbox database `rwb_sandbox`, build database `rwb_sandbox_next`, topic `rwb.source-data.events.v1` (not published here), Temporal task queue `rwb-source-data` in namespace `rwb-recovery` (not used here).

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

DP-01, DP-05 and DP-15 are the subject of this story: one schema, one read path and one sequence, all exercised by a build tool that runs outside the service. DP-07 is used for every list of values, through the published contract and its fake. DP-03 applies as one decision record per seeded rule evaluation in the smoke check, and DP-04 as the embedded kit that evaluates the seeded packages; the C row of DP-04 (`RWB-P7-E1073-CON`) is not taken by this story, because the smoke check evaluates the packages held in its own fixture and calls no rwb-decision operation, and the contract list of this story is fixed at `RWB-P3-E1043-CON`. DP-13 and DP-19 are named for completeness of the pattern set: this story serves no path and no screen, and their build dependencies stay with the application stories that do.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `AceSchemaLoader` | Service | Applies the Tier 1 tables, the Tier 2 DDL fixture, the per-service baseline and the two view migrations to `rwb_sandbox_next` |
| `SandboxGenerator` | Service | Reads the metadata and writes synthetic rows table by table in foreign key order, in schema `public` first and then in schema `rwb_source_data` |
| `ValueFactory` | Service | Produces a value per data type and list, seeded; synthetic names as "SYN-FIRST-000123"; tokens as random 64-character hex |
| `ExceptionShapeBuilder` | Service | Adds the shapes in BR4, 10 cases each |
| `SandboxVerifier` | Service | View compile and row checks, list, key, personal data pattern, boundary and delivered-objects checks |
| `AccessSeedLoader` | Service | Seeds the role and permission rows and one synthetic test user reference per role, from the reference-data contract |
| `SandboxExport` | Service | Writes a table to CSV for the read-only role |
| `Sandbox build stage` | Job | Pipeline stage: create the database and its three schemas, apply the DDL and the baseline, generate, verify, rename, grant |

**Database.** The stage creates `rwb_sandbox_next` with schema `public`, schema `recovery` and schema `rwb_source_data`, applies the DDL set of section 4 step 3, fills all three schemas, verifies, then renames the database to `rwb_sandbox` from the maintenance connection; RWB-P1-E1065-DB owns the role `rwb_sandbox_read` and the grants, and the pipeline holds one PostgreSQL advisory lock for the whole build. The stage creates no table of the service schema that the baseline does not already create, and it edits no applied migration (DP-15).

**Configuration and reference data.** Properties `rwb.sandbox.seed=20261128`, `rwb.sandbox.cases.mortgage=1226`, `rwb.sandbox.cases.hire-purchase=1296`, `rwb.sandbox.cases.ssme=290`, `rwb.sandbox.shape-count=10`, `rwb.sandbox.ace-schema=15 ACE DB Alignment/ACE Schema PostgreSQL v1.sql`, owned by the recovery tech lead; the lists of values through the reference-data contract (DP-07); the role and permission rows from the seed file of rwb-case. Every value is overridable, and the seed profile document is RWB-P1-E1065-CON's.

**Build steps**

1. `AceSchemaLoader` for the Tier 1 tables and the Tier 2 fixture; stop before the Section B view migration when the Tier 2 DDL is absent.
2. Metadata reader over `sys_objects`, `sys_fields` and the reference-data read, with foreign key order from the relationships.
3. `ValueFactory` per data type and list, seeded; a column with no `sys_fields` row fails the build.
4. `SandboxGenerator` for the ACE-shaped tables, then the case volumes with linked accounts, parties, contact points, collateral, valuations, payments and interactions.
5. `ExceptionShapeBuilder` for the shapes in BR4.
6. `AccessSeedLoader` with a synthetic test user reference per role.
7. `SandboxVerifier`: 30 views compile and return rows, rows per table, list values, foreign keys, personal data patterns outside schema `public` (national ID with check digit, mobile number, email), the 89 and 90 days past due boundary, and the delivered objects of the two sibling stories.
8. The Drools smoke check over the seeded packages, with one decision record per evaluation.
9. The pipeline stage with `rwb_sandbox_next`, the advisory lock, the rename and the grant.
10. Tests for AC1 to AC9 and the access test in the pipeline.

**Feature flag.** `rwb.source-data.sandbox` (enables the DEV profile that points the service at `rwb_sandbox`).

**Done when.** The tests in section 16 pass, `rwb_sandbox` holds the three schemas with the seeded rows, the build report is published with the row count per table, and squads use the sandbox in DEV.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-002 | A test user without the right calls the DEV service | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | A test user calls a sandbox case outside their scope | This case is not in your scope. |

Build failures are reported in the pipeline result with the table and column named; no user message applies. The two message texts are the legacy texts, copied unchanged, and are raised by the guard library of rwb-access on the DEV service; this story raises no message of its own.

### 15. Screens and states

No screen in this story. Developers and analysts read the sandbox with SQL and the export script, and see the build result and row counts in the pipeline run. Screens built in DEV show sandbox cases through the normal endpoints, merged by the gateway-bff composite route (DP-19), which this story neither builds nor changes.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-065-01 | AC1, BR2, BR4, BR5, BR8 | End to end | The Tier 1 and 14 Tier 2 tables; the baseline and the two view migrations; seed 20261128; 2,812 cases plus shapes |
| TC-E1-065-02 | AC2 | End to end | Read-only role query, CSV export and refused UPDATE |
| TC-E1-065-03 | AC3, BR3 | End to end | Test migration adding recovery_case.risk_tier with its dictionary row |
| TC-E1-065-04 | AC4, BR3 | End to end | Dictionary fixture without the DF-CAS-023 row for recovery_case.closure_reason |
| TC-E1-065-05 | AC5 | End to end | Two builds for commit a1b2c3d and seed 20261128 |
| TC-E1-065-06 | AC6 | End to end | Empty LOV-PRODUCT seed |
| TC-E1-065-07 | AC7, BR1, BR9 | End to end | Injected 13-digit value in recovery.document_field.extracted_value; a clear value in public.customer |
| TC-E1-065-08 | AC8, BR4 | End to end | Boundary accounts at 89 and 90 days past due in v_ace_account |
| TC-E1-065-09 | AC9 | End to end | Two builds started together |
| TC-E1-065-10 | Access | Component | Test user with RW-REFADM calls the case read path on the sandbox; refused with MSG-P4-002 |

The legacy test case IDs are kept in order and their Covers and Data are carried onto the split; the legacy level "System" maps to "End to end" and "Access" to "Component", as in the other stories of this run. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID. TC-E1-065-02 and TC-E1-065-01 run against the role that RWB-P1-E1065-DB delivers and the extension tables that RWB-P1-E1069-DB delivers, and TC-E1-065-04 and TC-E1-065-06 against the reference-data fake of section 12.8.

### 17. Guardrails

- No business value in code: the volumes, the seed, the shape count and the schema file are properties, and every list of values is read through the reference-data contract; values come from the dictionary and the lists.
- No personal data in logs, tests, events or prompts: every name, identifier and contact value is synthetic, and the verifier blocks a value that looks real outside schema `public`.
- No read of another service's tables at run time: the generator is a build tool outside the service artefact and is never deployed to SIT, UAT or production (DP-01).
- The sandbox is in DEV only; no copy goes to another environment. The ACE-shaped tables are a test double, not a data copy, and the deployment gate of RWB-P1-E1065-DB refuses any other target.
- No copy and no load table is created: every service reads source data only through this service's contract or its own `v_ace_*` views.
- The 30 views, the four extension tables, the login and the grants are one story's delivery each and one story's test each: this story asserts them and never re-creates them.
- An applied migration is never edited: a correction is a new version on the service sequence (DP-15).
- The embedded Drools kit evaluates packages held in its own fixture: no rule package is downloaded from rwb-decision during a build.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-RDF-001 | 14 data products, each with one system of record and one owner | Business Requirements Epic 1, sections 3.1 and 4 | EP01 | All recovery processes | R-UNI-17, R-UNI-05, R-UNI-07, R-UNI-20, R-UNI-10; DL15, DL16; D-RCV-35 | TC-E1-065-01 to TC-E1-065-06, TC-E1-065-08 to TC-E1-065-10 |
| REQ-RDF-010 | Access per data product by role; personal data masked in line with PDPA | Business Requirements Epic 1, sections 3.1 and 4; Program section 6.7 (NFR-045) | EP01 | All recovery processes | CTL-11; D-RCV-35 U4 | TC-E1-065-07 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-P1-E1065-CON | Contract | H build dependency: the stage contract, the seed profile schema, the database and role contract and the failure contract this story implements |
| RWB-P1-E1065-DB | ACE DB | X external dependency: the database `rwb_sandbox`, the three schemas, the role `rwb_sandbox_read`, the grants this story's criteria assert |
| RWB-P1-E1001-APP | App development | H build dependency: the per-service baseline, this service's 13 tables and the dictionary rows |
| RWB-P1-E1069-APP | App development | H build dependency: the 30 `recovery.v_ace_*` views and their conformance test |
| RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, RWB-PLT-E1043-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON | Contract | H: the decision-record library, the Drools kit, the reference-data library, the per-service Flyway sequence and the gateway-bff composite route |
| RWB-P3-E1043-CON | Contract | C: the rwb-case reference-data contract the lists of values are read from |
| RWB-P1-E1013-APP | App development | Sibling: the freshness reads, the business-day operations and the two events of the service |

### 19. Out of scope

- The database `rwb_sandbox`, its three schemas, the role `rwb_sandbox_read`, the grants and the deployment gate: RWB-P1-E1065-DB; the four extension tables: RWB-P1-E1069-DB.
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
