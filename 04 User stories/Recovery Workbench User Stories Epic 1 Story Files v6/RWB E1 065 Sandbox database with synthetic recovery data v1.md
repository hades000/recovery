# RWB-E1-065 Sandbox database with synthetic recovery data

SCB Collections and Recovery. Henka Group, 15 November 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E1-065 |
| Epic | E1, release 30 November 2026 |
| Module | P1 Recovery data engine |
| Feature | None |
| Requirement IDs | REQ-RDF-001, REQ-RDF-010 |
| BRD section | Business Requirements Epic 1, section 3.1 (story) and section 4 (REQ-RDF-001, REQ-RDF-010); Business Requirements Program, section 6.7 (NFR-045) |
| L3 process | All recovery processes |
| Decision | D-RCV-35 (U1, U4); ADR-010; DL43 |
| Priority | Must |
| Depends on | RWB-E1-001, RWB-E1-069 |
| Status | Ready for build, Section B views behind the RWB-ACE-001 DDL (DL43) |

## 1. Story

As a **Tribe lead and squad member (RW-TRIBE)**, I want **a sandbox database that stands up the ACE schema and the recovery schema from the same DDL as SIT, with synthetic ACE-shaped source rows and synthetic Workbench rows**, so that **I can build and test every view read before the ACE interfaces are available and without production data**.

## 2. Business rationale

SIT reads the real ACE database; DEV has none. Without a local ACE schema the 30 `recovery.v_ace_*` views cannot compile, so no squad can test a source read, the case list, a notice or a report before SIT is connected. The sandbox applies the ACE schema for the 22 Tier 1 tables, the RWB-ACE-001 DDL for the 14 Tier 2 tables, Physical Schema v5 for the 92 recovery tables and the four extension tables, and V0002 and V0003 for the 30 views. It fills the source tables with synthetic rows and the Workbench tables with synthetic cases across Mortgage, Hire Purchase and SSME, and the exception shapes the rules must handle.

There is no copy and no load table: `loan_account`, `account_payment`, `party`, `contact_point`, `collateral`, `account_collateral`, `collections_history`, `party_product`, `valuation`, `score`, `asset`, `load_run`, `dq_exception`, `dq_rule`, `source_field_map`, `source_code_map`, `interface_run`, `interface_signoff`, `tracker_inventory` and `tracker_row` do not exist. The generator reads the data dictionary, so a schema change reaches the sandbox with no manual rebuild, and the verifier allows a clear identity number only in the ACE-shaped tables, where ACE itself holds it; the recovery schema sees `id_no_masked` and `id_no_last4` only. Serves REQ-RDF-001 (the 14 data products in one schema) and REQ-RDF-010 (no personal data outside its permitted use).

## 3. Preconditions

- RWB-E1-001 is done: V0001 creates the 92 tables, `data_product`, the 122 `sys_objects` rows, the 1,366 `sys_fields` rows and the four extension tables.
- RWB-E1-069 is done: V0002 and V0003 create the 30 `recovery.v_ace_*` views and their grants, and CHK-01 compares them with the dictionary.
- The ACE schema DDL `15 ACE DB Alignment/ACE Schema PostgreSQL v1.sql` is in the repository. It holds the 22 Tier 1 tables, among them `account`, `payment`, `customer`, `efs_action` and `iam_user`.
- The RWB-ACE-001 DDL for the 14 Tier 2 tables is available in DEV (DL43); until it lands, the 14 Section B views and the features that read them stay behind their flags.
- A PostgreSQL 17 database `rwb_sandbox` exists in DEV, reachable from the pipeline.
- The Entra ID group RWB-DEV-RW-TRIBE exists and maps to the sandbox read-only database role.
- The role to permission matrix rows (roles.txt, Permissions) are available as a seed file for the sandbox.
- The ACE service can be deployed in DEV against the sandbox database.

## 4. Flow

1. Pipeline: on a merge to main that changes the ACE schema DDL, a recovery Flyway migration or the dictionary, or on a manual start, runs the sandbox build stage in DEV.
2. Pipeline: creates database `rwb_sandbox_next` and two empty schemas, `public` and `recovery`.
3. Pipeline: applies `ACE Schema PostgreSQL v1.sql` (22 Tier 1 tables), then the RWB-ACE-001 DDL (14 Tier 2 tables), then V0001 (92 tables and the dictionary), V0002 (16 Section A views) and V0003 (14 Section B views).
4. SandboxGenerator: reads `sys_objects`, `sys_fields` and `lov_value` to learn every table, column, type and list.
5. SandboxGenerator: seeds the 22 Tier 1 tables and the 14 Tier 2 tables with synthetic rows, including one `ace_batch_run` row per source and business date.
6. SandboxGenerator: creates synthetic cases with seed 20261128: 1,226 Mortgage, 1,296 Hire purchase and 290 SSME (10 percent of the 30 June 2026 inventory; DL15), with their accounts, parties, contact points, collateral, valuations, payments and interactions, linked by business key to the ACE-shaped rows.
7. SandboxGenerator: adds 10 cases for each exception shape in section 8, BR4.
8. SandboxGenerator: loads the 54 roles, the permission matrix and one named test user per role.
9. SandboxVerifier: checks that the 30 views compile and each returns a row, that every seeded table has rows, that every LOV column holds list values, that every foreign key resolves, that no clear personal value sits in schema `recovery`, and that the boundary accounts exist.
10. Pipeline: renames `rwb_sandbox_next` to `rwb_sandbox`, grants SELECT on schema `recovery` to role `rwb_sandbox_read`, and publishes the build result with the row count per table.
11. Developer or analyst: queries the sandbox with SQL or the export script, or calls the DEV service, without a request to another team.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A table column has no `sys_fields` row | Build fails naming the table and column; previous sandbox kept | None (pipeline result) | AC4 |
| X2 | The reset runs twice for the same commit and seed | The schemas are dropped and recreated; the same seed gives the same rows and counts | None | AC5 |
| X3 | A generated value breaks a constraint | Build fails naming the table and constraint; previous sandbox kept | None (pipeline result) | AC6 |
| X4 | A generated value in schema recovery matches a personal data pattern | Build fails naming the table and column | None (pipeline result) | AC7 |
| X5 | Accounts sit at the 90 days past due boundary | Accounts at 89 and at 90 days past due are both generated | None | AC8 |
| X6 | A second build starts while one runs | The second build waits on the pipeline lock and runs after the first | None | AC9 |
| X7 | The RWB-ACE-001 DDL is not yet in DEV | The build stops before V0003; the 16 Section A views and the Workbench tables are still built and published | None (pipeline result) | AC1 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the DDL from RWB-E1-001 and RWB-E1-069 and, for Section B, the Tier 2 DDL of RWB-ACE-001; it publishes the environment every squad tests in |
| Negotiable | Volumes, seed and exception shapes are properties; the story fixes the generator, the checks and the access |
| Valuable | Every squad builds and tests every view read from the first day with no production data |
| Estimable | One generator tool, one verifier, one pipeline stage, one database role |
| Small | Finished inside two weeks with its tests |
| Testable | Each criterion is a pipeline test or a query against the built sandbox |

## 7. Acceptance criteria

```gherkin
Feature: Sandbox database with synthetic recovery data

  Background:
    Given the sandbox build uses seed 20261128
    Given volumes of 1,226 Mortgage, 1,296 Hire purchase and 290 SSME cases

  Scenario: AC1 The sandbox exists
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

  Scenario: AC2 It is readable and extractable
    Given the sandbox
    When a member of RWB-DEV-RW-TRIBE runs "SELECT product_group, count(*) FROM recovery.recovery_case GROUP BY product_group"
    Then the result shows MORTGAGE, HIRE_PURCHASE and SSME with their counts
    Then the export script writes recovery_case to a CSV file without a request to another team
    Then the system refuses an UPDATE by the same database role

  Scenario: AC3 It scales with the schema
    Given a test migration, never shipped, adds column "risk_tier varchar(10)" to recovery_case with its sys_fields row and list LOV-RISK-TIER
    When it is applied
    Then the sandbox rebuild fills risk_tier with values from LOV-RISK-TIER on every case
    Then no generator code was changed

  Scenario: AC4 A column with no dictionary entry
    Given a dictionary fixture in which the sys_fields row for recovery_case.closure_reason is removed
    When the sandbox build runs
    Then the build fails with "recovery_case.closure_reason has no data dictionary entry"
    Then the previous sandbox stays in use

  Scenario: AC5 The reset is idempotent
    Given the sandbox was built for commit "a1b2c3d" with seed 20261128
    When the build runs again for commit "a1b2c3d" and seed 20261128
    Then a fresh schema public and a fresh schema recovery are built in rwb_sandbox_next and swapped in
    Then every seeded table holds the same row count
    Then case "RW-2026-000001" holds the same total_outstanding_at_entry of 1,845,200.00
    Then no row from the first build remains

  Scenario: AC6 A generated value breaks a constraint
    Given list LOV-PRODUCT is empty in the seed data
    When the sandbox build runs
    Then the build fails naming table "recovery_case" and column "product_group"
    Then the previous sandbox stays in use

  Scenario: AC7 No clear personal value outside the ACE tables
    Given the verifier scans every column of schema recovery tagged is_personal
    When a generated value in recovery.document_field.extracted_value matches the 13-digit national ID pattern with a valid check digit
    Then the build fails naming recovery.document_field.extracted_value
    Then a clear identity number in public.customer is not a failure, because ACE holds it and v_ace_customer exposes id_no_masked and id_no_last4 only
    Then the system publishes no sandbox from that build

  Scenario: AC8 Accounts at the entry boundary
    Given the exception shapes include the entry boundary
    When the sandbox is provisioned
    Then 10 accounts in v_ace_account have days_past_due 89 and no case
    Then 10 accounts in v_ace_account have days_past_due 90 and one open case each

  Scenario: AC9 Two builds at once
    Given a sandbox build is running for commit "a1b2c3d"
    When a second build starts for commit "e4f5a6b"
    Then the second build waits until the first ends
    Then the sandbox after both holds the data for commit "e4f5a6b"
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | No production data in DEV; the sandbox holds synthetic data only | NFR-045; CTL-11 |
| BR2 | The sandbox is built from the same DDL as SIT: the ACE schema for the 22 Tier 1 tables, the RWB-ACE-001 DDL for the 14 Tier 2 tables, and V0001 to V0003 for the 92 recovery tables and the 30 views | RWB-E1-001; RWB-E1-069; ADR-001 |
| BR3 | Generated values come from the data dictionary and the lists of values, not from code | sys_fields; lov_value; Principle 1 |
| BR4 | Exception shapes generated: duplicate case for one customer and product (R-UNI-17), deceased customer (R-UNI-05), bankruptcy (R-UNI-07), open deviation, legal hold (R-UNI-20), unmapped product code, collateral with no account, case with three accounts, accounts at 89 and 90 days past due (DL16), withdrawn consent (R-UNI-10) | rules.txt; DL16 |
| BR5 | Case volumes follow the product split of the 30 June 2026 inventory at 10 percent | DL15 |
| BR6 | Every role has a named test user before it has real users | DL39 |
| BR7 | The ACE-shaped tables (22 Tier 1 and 14 Tier 2) are a DEV test double for ACE, not a copy of source data: they hold synthetic rows only, they are never deployed to SIT, UAT or production, and no recovery table is loaded from them by a batch job | D-RCV-35 U1; NFR-045 |
| BR8 | No copy and no load table exists in the sandbox; the 20 tables that left the schema are absent, and the Workbench reads source data only through `recovery.v_ace_*` | D-RCV-35; ADR-010 |
| BR9 | A clear identity number is allowed only in the ACE-shaped tables; schema recovery holds masked or synthetic values only | D-RCV-35 U4; CTL-11 |

## 9. State transitions

None. This story does not change a case status. It changes the sandbox build state in the pipeline: Building, Published or Failed.

## 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-TRIBE, Tribe lead and squad members | Read and extract the sandbox through role `rwb_sandbox_read`; start a manual build |
| RW-PLATADM, platform administrator | Owns the sandbox database and the pipeline stage |
| Test users per role | Call the DEV service against the sandbox with their role's rights |
| ACE team lead and ACE DBA | Own the ACE schema DDL used as the test double and the Tier 2 DDL of RWB-ACE-001; approve a change to either |

## 11. Data

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
| DF-REF-034 to DF-REF-038 | role | all 5 fields | Write |
| DF-REF-040 to DF-REF-044 | permission | all fields | Write |
| DF-REF-027 | lov_value | id | Read |
| DF-REF-028 | lov_value | lov_code | Read |
| DF-REF-029 | lov_value | value_code | Read |
| DF-REF-097 | sys_fields | field_name | Read |
| DF-REF-098 | sys_fields | data_type | Read |
| DF-REF-105 | sys_fields | is_personal | Read |

The 30 views are `v_ace_account`, `v_ace_payment`, `v_ace_customer`, `v_ace_contact`, `v_ace_ca_relation`, `v_ace_aa_relation`, `v_ace_collateral`, `v_ace_asset`, `v_ace_efs_action`, `v_ace_efs_action_code`, `v_ace_efs_assignment`, `v_ace_bucket_log`, `v_ace_product`, `v_ace_branch`, `v_ace_holiday`, `v_ace_plan`, `v_ace_batch_status`, `v_ace_valuation`, `v_ace_collateral_detail`, `v_ace_npa_asset`, `v_ace_npa_sale`, `v_ace_lawsuit`, `v_ace_hearing`, `v_ace_pod`, `v_ace_write_off`, `v_ace_score`, `v_ace_party_product`, `v_ace_credit_decision`, `v_ace_esign` and `v_ace_iam_group`. The other Workbench tables are filled the same way from their `sys_fields` rows; `delegation_limit` stays empty until version DOA-2026.11 is loaded, and `decision_log_entry` and `interaction` receive their rows from running the Workbench jobs against the sandbox. Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

**Pipeline stage**

| Item | Value |
|---|---|
| Trigger | Merge to main that changes the ACE schema DDL, a file under the recovery Flyway migration folder or the dictionary; manual start by RW-TRIBE or RW-PLATADM |
| Job name | Sandbox build, a DEV pipeline stage; not a scheduled job and not in `job_catalog` |
| Schedule | On trigger only |
| Input | `ACE Schema PostgreSQL v1.sql`; the RWB-ACE-001 Tier 2 DDL; V0001, V0002 and V0003; `sys_objects`, `sys_fields` and `lov_value` after migration; the role and permission seed file; properties in section 13 |
| Output | Database `rwb_sandbox` with schema `public` (the ACE schema, including the 22 Tier 1 and 14 Tier 2 tables) and schema `recovery` (92 tables and 30 views) holding synthetic rows; build report with row count per table and the verifier result |
| Events published | None |
| Idempotency key | Commit hash and seed. The same pair produces the same rows |
| Restart behavior | The build works on `rwb_sandbox_next` and renames it to `rwb_sandbox` only after the verifier passes; a failed build leaves the previous sandbox |

**Endpoint used in DEV against the sandbox**

| Method and path | Use | Authorization | Errors |
|---|---|---|---|
| GET /api/recovery/v1/cases | A test user lists sandbox cases in scope | Case record, R | 401 (MSG-P4-001); 403 (MSG-P4-002); 503 |

## 13. Solution plan

- Package: folder `tools/sandbox-generator`, Java package `recovery.tools.sandbox`, built as a separate build module that is not packaged into the ACE service.

| Component | Type | Responsibility |
|---|---|---|
| AceSchemaLoader | Service | Applies the 22 Tier 1 tables, the 14 Tier 2 tables, V0001, V0002 and V0003 to `rwb_sandbox_next` |
| SandboxGenerator | Service | Reads the metadata and writes synthetic rows table by table in foreign key order, in schema public first and then schema recovery |
| ValueFactory | Service | Produces a value per data type and list, seeded; synthetic names as "SYN-FIRST-000123"; tokens as random 64-character hex |
| ExceptionShapeBuilder | Service | Adds the shapes in BR4, 10 cases each |
| SandboxVerifier | Service | View compile and row checks, list, key, personal data pattern and boundary checks |
| AccessSeedLoader | Service | Loads 54 roles, the permission matrix and one test user per role |
| SandboxExport | Service | Writes a table to CSV for the read-only role |
| Sandbox build stage | Job | Pipeline stage: create database, apply the ACE schema, the Tier 2 DDL and V0001 to V0003, generate, verify, rename, grant |

- Database: no new recovery table. The stage creates `rwb_sandbox_next`, applies the ACE schema and the recovery migrations, fills both schemas, verifies, then renames the database to `rwb_sandbox` from the maintenance connection and grants SELECT to role `rwb_sandbox_read` mapped to RWB-DEV-RW-TRIBE. The pipeline holds a PostgreSQL advisory lock for the whole build.
- Configuration and reference data: properties `rwb.sandbox.seed=20261128`, `rwb.sandbox.cases.mortgage=1226`, `rwb.sandbox.cases.hire-purchase=1296`, `rwb.sandbox.cases.ssme=290`, `rwb.sandbox.shape-count=10`, `rwb.sandbox.ace-schema=15 ACE DB Alignment/ACE Schema PostgreSQL v1.sql`, owned by the tech lead; lists of values from the seed migration; roles and permissions from the roles.txt seed file.
- Build steps:
  1. AceSchemaLoader for the 22 Tier 1 tables and the 14 Tier 2 tables; stop before V0003 when the Tier 2 DDL is absent.
  2. Metadata reader over `sys_objects`, `sys_fields` and `lov_value` with foreign key order from the relationships.
  3. ValueFactory per data type and list, seeded; a column with no `sys_fields` row fails the build.
  4. SandboxGenerator for the 22 Tier 1 and 14 Tier 2 tables, then the case volumes with linked accounts, parties, contact points, collateral, valuations, payments and interactions.
  5. ExceptionShapeBuilder for the shapes in BR4.
  6. AccessSeedLoader with a test user per role.
  7. SandboxVerifier: 30 views compile and return rows, rows per table, list values, foreign keys, personal data patterns in schema recovery (national ID with check digit, mobile number, email), and the 89 and 90 days past due boundary.
  8. Pipeline stage with `rwb_sandbox_next`, the rename, the grant and the lock.
  9. Tests for AC1 to AC9 and the access test in the pipeline.
- Feature flag: `rwb.dataengine.sandbox` (enables the DEV profile that points the service at `rwb_sandbox`).
- Done when: the tests in section 16 pass and squads use the sandbox in DEV.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-002 | A test user without the right calls the DEV service | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | A test user calls a sandbox case outside their scope | This case is not in your scope. |

Build failures are reported in the pipeline result with the table and column named; no user message applies.

## 15. Screens and states

No screen in this story. Developers and analysts read the sandbox with SQL and the export script, and see the build result and row counts in the pipeline. Screens built in DEV show sandbox cases through the normal endpoints.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-065-01 | AC1, BR2, BR4, BR5, BR8 | System | 22 Tier 1 and 14 Tier 2 tables; V0001 to V0003; seed 20261128; 2,812 cases plus shapes |
| TC-E1-065-02 | AC2 | System | Read-only role query, CSV export and refused UPDATE |
| TC-E1-065-03 | AC3, BR3 | System | Test migration adding recovery_case.risk_tier with its dictionary row |
| TC-E1-065-04 | AC4, BR3 | System | Dictionary fixture without the DF-CAS-023 row for recovery_case.closure_reason |
| TC-E1-065-05 | AC5 | System | Two builds for commit a1b2c3d and seed 20261128 |
| TC-E1-065-06 | AC6 | System | Empty LOV-PRODUCT seed |
| TC-E1-065-07 | AC7, BR1, BR9 | System | Injected 13-digit value in recovery.document_field.extracted_value; a clear value in public.customer |
| TC-E1-065-08 | AC8, BR4 | System | Boundary accounts at 89 and 90 days past due in v_ace_account |
| TC-E1-065-09 | AC9 | System | Two builds started together |
| TC-E1-065-10 | Access | Access | Test user with RW-REFADM calls GET /cases on the sandbox; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: volumes, seed and shape counts are properties; values come from the dictionary and the lists.
- No personal data in logs, tests or prompts: every name, identifier and contact value is synthetic, and the verifier blocks a value that looks real in schema recovery.
- No read of another module's tables at runtime: the generator is a build tool outside the ACE service and is never deployed to SIT, UAT or production.
- The sandbox is in DEV only; no copy goes to another environment. The ACE-shaped tables are a test double, not a data copy.
- No copy and no load table is created: the Workbench reads source data only through `recovery.v_ace_*`.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-RDF-001 | 14 data products, each with one system of record and one owner | Business Requirements Epic 1, sections 3.1 and 4 | None | All recovery processes | R-UNI-17, R-UNI-05, R-UNI-07, R-UNI-20, R-UNI-10; DL15, DL16; D-RCV-35 | TC-E1-065-01 to TC-E1-065-06, TC-E1-065-08 to TC-E1-065-10 |
| REQ-RDF-010 | Access per data product by role; personal data masked in line with PDPA | Business Requirements Epic 1, sections 3.1 and 4; Program section 6.7 | None | All recovery processes | CTL-11; D-RCV-35 U4 | TC-E1-065-07 |

## 19. Out of scope

- Masked copies of production data in SIT and UAT (RWB-TE-004).
- The rule table test harness (RWB-TE-005) and the performance test harness (RWB-TE-009).
- The PDPA lint for code, tests and logs (RWB-TE-011).
- The ACE ingestion itself and the 14 Tier 2 tables: the ACE team owns them in RWB-ACE-001.
- The 30 views, their grants and the view conformance test: RWB-E1-069.
- The dictionary content and its change process: RWB-E1-064.
