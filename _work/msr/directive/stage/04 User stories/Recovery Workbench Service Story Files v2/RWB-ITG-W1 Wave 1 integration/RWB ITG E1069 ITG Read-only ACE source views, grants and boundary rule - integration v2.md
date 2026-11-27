# RWB-ITG-E1069-ITG Read-only ACE source views, grants and boundary rule — integration

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-E1069-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W1 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-069 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP02, DP03, DP05, DP06, DP07, DP08, DP11, DP15, DP19 |
| Parallel lane | L-ITG-W1 |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-ITG-E1069-ITG-16) |
| Depends on (build) | None |
| Contract dependencies | Not specified in the source documents (DOR-RWB-ITG-E1069-ITG-21) |
| Contract version | v1 (the /v1 path of the three operations in section 12.2) |
| Integration dependencies | RWB-P1-E1069-APP, RWB-P4-E1069-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-001, FR-PLT-002, FR-PLT-010, FR-PLT-011, FR-PLT-012, FR-PLT-013, FR-PLT-027) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-069 for the wave-1 integration epic. The single `recovery` schema of the monolith is split: the 30 `recovery.v_ace_*` views stay in schema `recovery` with `ace_view_owner` as their owner, the 92 tables move to the 19 `rwb_*` schemas with one login each (DP-01, DP-02, DP-15), only `rwb_source_data` holds SELECT on the views (DP-05) and the four extension tables move to `rwb_source_data`. The boundary becomes two-part (BND-6 halves A and B): no class names a `public` table, and no class outside rwb-source-data names a `v_ace_*` view or another service's schema (DP-11 for every other service). This story builds the harness that proves the grant matrix and both halves of the boundary on the real 19 logins in SIT, and it owns no schema. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (8 resolved, 37 cross-document, 3 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the read-only ACE source views, the grant matrix and the boundary rule of the monolith proven on the real split in SIT: the 30 `recovery.v_ace_*` views in schema `recovery` read only through the `rwb_source_data` login, each of the other 18 service logins confined to its own schema and holding nothing on the views or in `public`, no constraint or table name crossing a schema, the four extension tables in `rwb_source_data` 1:1 on the ACE key, and boundary rule BND-6 refusing both a `public` table and a `v_ace_*` view named outside rwb-source-data**, so that **one copy of ACE source data serves 19 services without a second copy, without a write path into ACE data, and with a build that fails on a breach instead of a review that hopes**.

### 2. Business rationale

The Workbench takes no inbound source data and keeps no copy of it. RWB-E1-069 proved that against one schema: 30 SELECT-only views over the ACE tables, one view owner, one service role and boundary rule BND-6 in RWB-TE-001. In the target the schema is split 19 ways, and every property that story proved is now a property of the split rather than of one schema: the views stay in `recovery` because they read ACE's own tables (Arch v5 slides 8 and 9, "ACE schemas + 30 recovery.v_ace_* views · 19 rwb_* schemas"), the 92 tables move to the 19 `rwb_*` schemas with one login each (DP-01, DP-02, DP-15; Arch v5 slides 8 and 41), only `rwb_source_data` holds SELECT on the views (Arch v5 slides 8, 9, 11 and 45; DP-05), and the four extension tables sit in `rwb_source_data` (Ownership Map; Arch v5 slide 41).

The boundary now has two halves. Half A is the legacy rule: no class in the Workbench names a table in schema `public`. Half B is new: no class outside rwb-source-data names a `v_ace_*` view or another service's schema, and every other service reaches ACE data through the source-data contract or a Temporal activity (DP-11; Arch v5 slides 11, 12, 13 and 45). A single service story cannot prove either half for 19 services, and no service story may read the other 18 schemas to find out — which is exactly why this story exists. It is the one place allowed to hold 19 logins, connect as each of them and assert the catalog.

Serves REQ-RDF-002 (ACE source data read only through the views) and REQ-DRI-006 (no component calls a system of record directly). The measure is every one of the 19 logins passing its row of the grant matrix and both halves of BND-6 in one SIT run, with zero cross-schema reads found.

### 3. Preconditions

- SIT holds the ACE head with the 21 Tier 1 tables of RWB-E1-069 and the 14 Tier 2 tables that RWB-ACE-001 adds, among them `public.account`, `public.payment`, `public.customer` and `public.efs_action`.
- Schema `recovery` holds the 30 `v_ace_*` views and the three helper functions `recovery.ace_to_date`, `recovery.ace_to_boolean` and `recovery.ace_mask_value`, owned by `ace_view_owner` (RWB-P1-E1069-APP, RWB-P4-E1069-APP).
- The 92 tables of the legacy schema sit in the 19 `rwb_*` schemas: `rwb_source_data`, `rwb_case`, `rwb_access`, `rwb_document`, `rwb_comms`, `rwb_decision`, `rwb_reporting`, `rwb_agent`, `rwb_integration`, `rwb_payment`, `rwb_treatment`, `rwb_asset`, `rwb_deviation`, `rwb_valuation`, `rwb_guarantee`, `rwb_litigation`, `rwb_debtsale`, `rwb_writeoff` and `rwb_partner`, and the four extension tables `party_ext`, `contact_point_ext`, `account_ext` and `valuation_ext` sit in `rwb_source_data`.
- The 19 schemas and their logins are created in SIT by the platform DB story RWB-PLT-NF06-DB, with names fixed in the Environment and Deployment Design (Arch v5 slide 8, "19 rwb_* schemas, one login each").
- The module map of RWB-TE-001 is in the repository, with `recovery-modules.yaml` read by `RecoveryBoundaryTest`, and it holds `sourceViews`, the 30 view names the rule allows.
- The two integration services are deployed in SIT on their published wave 1 contracts: P1 `rwb-source-data` with `GET /accounts/{id}` and `GET /customers/{id}`, and P4 `rwb-access` with `POST /authorise` (RWB-P1-E1069-APP, RWB-P4-E1069-APP).
- The module map, the 30-view list and the schema names are configuration; the harness writes no business value into its code.
- The 19 login names (one per `rwb_*` schema), the grant matrix on the 30 views after the split and the two-part boundary rule (BND-6 halves A and B) are Not specified in the source documents (GAP-0377; ASM-0543).
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7). The harness is written on Day 1 and is run in SIT once the logins exist; a fake is never used in place of a real login, and the harness never points at a production database.

### 4. Flow

1. Harness: reads its run file — the SIT connection strings of the 19 logins, the 30-view list from the module map and the schema names. The 19 login names, the grant matrix on the 30 views after the split and the two-part boundary rule are Not specified in the source documents (GAP-0377; ASM-0543); the run file carries them once and every probe reads the file, never a constant.
2. Harness: runs the preflight of section 13 — 19 logins reachable, 30 views present in schema `recovery`, `sourceViews` present in the module map, the four extension tables present in `rwb_source_data`. One missing item stops the run before the first test.
3. Grant-matrix probe: connects as `rwb_source_data` and selects one row from each of the 30 views, then from `public.account`, then runs insert, update and delete on `recovery.v_ace_account`.
4. Grant-matrix probe: connects as `ace_view_owner` and reads the catalog for the ownership of the 30 views and for SELECT on the ACE tables the views read.
5. Grant-matrix probe: connects as each of the other 18 logins in turn, reads a table in its own schema, then attempts the 30 views, `public.account` and a table of another service's schema.
6. Schema-boundary probe: scans every constraint in the 19 `rwb_*` schemas for a referenced table, type or schema outside its own, lists every table name across the 19 schemas and schema `recovery` for a duplicate, and confirms that schema `recovery` holds no service table.
7. Extension-key probe: lists the columns, the primary keys and the check of the four extension tables in `rwb_source_data`, counts their dictionary fields, and attempts a second `party_ext` row for person_key "P0000123" inside a transaction it rolls back.
8. Boundary-test runner: runs `RecoveryBoundaryTest` in the split tree with the fixture class on `public.account`, the same class on `recovery.v_ace_account` from a module outside rwb-source-data, a class of rwb-case on a table of `rwb_source_data`, and the same class against the source-data contract, with the allowed view list read from the module map.
9. Dictionary probe: connects as `rwb_source_data` and counts one `sys_objects` row per view and one `sys_fields` row per column of the 30 views.
10. Harness: reads the two source-data operations and the authorise check the boundary runner needs, so that the pass of half B is proven on the contract and not on a mock.
11. Harness: reconciles the findings — 19 logins, 30 views, four extension tables, zero cross-schema constraints, zero duplicate table names, zero grants to PUBLIC — and writes the run report naming every login, view, table and class it touched.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | One of the 19 logins is missing in SIT | The preflight stops the run and names the login and its schema; no test is reported as passed | Run report: login rwb_case is not reachable in SIT | AC3 |
| X2 | A view does not compile after the split | The owning migration fails, names the view and the ACE column, and no view of that run exists | Pipeline log: v_ace_account does not compile: column a.core_banking_system_date does not exist | AC1 |
| X3 | `rwb_source_data` holds a privilege in `public`, or any DML on a view | The probe fails and names the login, the privilege and the object | rwb_source_data holds SELECT on public.account; only SELECT on the 30 views is granted | AC2 |
| X4 | One of the other 18 logins reads a view, `public` or another service's schema | The probe fails and names the login, the object and the grant that allowed it | rwb_case reads recovery.v_ace_account; only rwb_source_data reads the views | AC3 |
| X5 | A constraint references another schema, or a table name sits in two schemas | The scan fails and names the constraint or the doubled table | fk_case_account_account_key references public.account; no constraint in an rwb_* schema may reference another schema | AC4 |
| X6 | A second row is written for an ACE key already in an extension table | The write is refused, the first row is unchanged and the transaction is rolled back | SQLSTATE 23505 duplicate key value violates unique constraint party_ext_pkey | AC5 |
| X7 | A class names a `public` table, a `v_ace_*` view outside rwb-source-data, or another service's table | The build fails with BND-6 and names the class and the object | Boundary rule BND-6 broken: AccountReader names recovery.v_ace_account outside rwb-source-data. Call the source-data contract instead. | AC6 |

X1 to X7 are the exception paths of RWB-E1-069 carried onto the split, with X1 and X4 added for the 18 logins that did not exist in the monolith and X7 widened to the second half of the boundary.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | A test project of its own; it needs the 19 logins, the 30 views and the module map, and it owns no schema, no table and no grant |
| Negotiable | Probe layout, report layout, run-file format and the order inside one AC are the harness's choice; the 30 view names, the helper functions, the four extension tables and the two message texts are fixed by RWB-E1-069 |
| Valuable | Proves for 19 services what no single service can: one read path, no privilege in `public`, no cross-schema constraint, no second copy and a build that fails on both halves of the boundary |
| Estimable | One harness project, six probes, five fixtures, one run file and one report |
| Small | Fits one sprint with the report |
| Testable | Every criterion is one catalog query, one refused statement with its SQLSTATE, one scan result or one build verdict |

### 7. Acceptance criteria

```gherkin
Feature: Read-only ACE source views, grants and boundary rule, proven on the 19 logins of the split

  Background:
    Given the environment is SIT with synthetic data
    Given the ACE schemas hold the 21 Tier 1 tables and the 14 Tier 2 tables of RWB-E1-069, among them public.account, public.payment and public.customer
    Given schema recovery holds the 30 v_ace_* views, owned by ace_view_owner, and the three helper functions
    Given the 19 rwb_* schemas exist with one login each and the 92 tables sit in them

  Scenario: AC1 The 30 views stay in schema recovery, compile and answer through the rwb_source_data login (new, D-RCV-60)
    Given the 92 tables have left schema recovery for the 19 rwb_* schemas and the 30 views did not move
    When the harness counts the views in schema recovery whose name starts with v_ace_
    Then the count is 30, all 30 compile, and no v_ace_* view exists in any rwb_* schema
    When the harness selects one row from each of the 30 views on the rwb_source_data login
    Then each of the 30 statements returns a row and no statement exceeds the 5 s statement timeout
    Then no view carries a primary key or a foreign key into an rwb_* schema
    Then schema recovery holds the 30 views and the three helper functions and no service table

  Scenario: AC2 rwb_source_data holds SELECT on the views and no privilege in public (new, D-RCV-60)
    Given the grant matrix on the 30 views after the split is loaded from the run file
    Then has_schema_privilege('rwb_source_data', 'recovery', 'USAGE') is true
    Then has_table_privilege('rwb_source_data', 'recovery.v_ace_account', 'SELECT') is true, and the same holds for each of the 30 views
    Then has_schema_privilege('rwb_source_data', 'public', 'USAGE') is false
    Then has_table_privilege('rwb_source_data', 'public.account', 'SELECT') is false
    When the same login runs insert, update and delete on recovery.v_ace_account
    Then each statement fails with SQLSTATE 42501 and no row of any view changes
    Then ace_view_owner owns the 30 views, holds SELECT on the ACE tables the views read and holds no INSERT, UPDATE or DELETE on any of them
    Then the test role "rwb_no_grant" cannot select recovery.v_ace_account, because PUBLIC holds no privilege on it

  Scenario: AC3 The other 18 logins reach neither the views nor public and read only their own schema (new, D-RCV-60)
    Given the 18 logins other than rwb_source_data: rwb_case, rwb_access, rwb_document, rwb_comms, rwb_decision, rwb_reporting, rwb_agent, rwb_integration, rwb_payment, rwb_treatment, rwb_asset, rwb_deviation, rwb_valuation, rwb_guarantee, rwb_litigation, rwb_debtsale, rwb_writeoff and rwb_partner
    Then each login is reachable in SIT and each one's own schema is named in the run file
    When each login selects from recovery.v_ace_account and from public.account
    Then each statement fails with SQLSTATE 42501
    When each login selects from a table in its own schema
    Then the statement returns without error
    When each login selects from a table in another service's schema
    Then the statement fails with SQLSTATE 42501
    Then has_schema_privilege(<login>, 'recovery', 'USAGE') is false and has_schema_privilege(<login>, 'public', 'USAGE') is false for all 18
    Then PUBLIC holds no privilege of any kind on the 30 views, on schema recovery or on schema public

  Scenario: AC4 No constraint leaves its own schema and no table name sits in two schemas (new, D-RCV-60)
    Given the 19 rwb_* schemas are at the head of their Flyway sequences
    When the harness lists every constraint in the 19 rwb_* schemas
    Then the scan returns 0 rows for any foreign key, check, unique or exclusion constraint that names a table, a type or a schema outside its own
    Then the scan returns 0 rows for a constraint whose referenced object sits in another rwb_* schema or in schema public
    When the harness lists every table name of the 19 rwb_* schemas and of schema recovery
    Then the scan returns 0 rows for a table name that sits in two schemas
    Then the scan returns 0 service tables in schema recovery
    When a branch adds a foreign key from rwb_case.case_account.account_key to public.account
    Then the scan fails with "fk_case_account_account_key references public.account; no constraint in an rwb_* schema may reference another schema"
    Then the merge check reports status failed and the merge is blocked

  Scenario: AC5 The four extension tables sit in rwb_source_data and stay 1:1 on the ACE key (new, D-RCV-60)
    Given the four extension tables party_ext, contact_point_ext, account_ext and valuation_ext are in rwb_source_data
    When the harness lists their columns, primary keys and constraints
    Then party_ext holds 12 columns with person_key as its primary key
    Then contact_point_ext holds 14 columns with contact_key as its primary key and the check ck_contact_point_ext_type
    Then account_ext holds 9 columns with account_key as its primary key
    Then valuation_ext holds 14 columns with valuation_key as its primary key
    Then the four tables hold 49 columns in all and 49 dictionary fields, DF-EXT-001 to DF-EXT-049
    Then no constraint on any of the four tables references a table outside rwb_source_data
    When the Workbench writes a second party_ext row for person_key "P0000123"
    Then the write fails with SQLSTATE 23505 and party_ext holds one row for "P0000123"

  Scenario: AC6 Boundary rule BND-6 refuses public and refuses the views outside rwb-source-data (new, D-RCV-60)
    Given the module map recovery-modules.yaml holds sourceViews, the 30 view names the rule allows
    Given the fixture class "recovery.dataengine.internal.AccountReader" holds a query on "public.account"
    When the pipeline runs the boundary-test runner
    Then the build fails with boundary rule BND-6, "AccountReader" and "public.account"
    When the same class queries "recovery.v_ace_account" from a module outside rwb-source-data
    Then the build fails with boundary rule BND-6, because only rwb-source-data is allowed to name a v_ace_* view
    When a class of rwb-case names a table of rwb_source_data
    Then the build fails with boundary rule BND-6, because no service names another service's schema
    When the same class names no table and calls GET /api/recovery/source-data/v1/accounts/{id} instead
    Then the build passes, with the scope check of POST /api/recovery/access/v1/authorise for the reader's data-product scope (scope name: Not specified in the source documents (ACR-RWB-ITG-E1069-ITG-AC6))
    Then the view names the rule allows are read from the module map, not written in the runner

  Scenario: AC7 The 92 tables sit in the 19 rwb_* schemas, and grants and the 30-view list change only by migration (new, D-RCV-60)
    Given the 19 rwb_* schemas exist with one login each
    When the harness counts the tables in the 19 rwb_* schemas
    Then the count is 92 and party_ext, contact_point_ext, account_ext and valuation_ext sit in rwb_source_data
    When a branch edits a grant already applied by a Flyway migration
    Then the merge is blocked
    When a branch changes the 30-view list or either half of BND-6 with no migration and no rule change approved by the recovery tech lead and the data architect
    Then the merge is blocked
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The 30 `recovery.v_ace_*` views stay in schema `recovery` after the split, owned by `ace_view_owner`, and they are the only read path to ACE source data | Arch v5 slides 8 and 9; ADR-010; DP-05 |
| BR2 | The 92 tables of the legacy schema sit in the 19 `rwb_*` schemas with one login each, and four of them — the extension tables — in `rwb_source_data` | Arch v5 slides 8 and 41; DP-01, DP-02, DP-15; Ownership Map |
| BR3 | `rwb_source_data` holds USAGE on schema `recovery` and SELECT on the 30 views, no privilege of any kind in schema `public`, and no INSERT, UPDATE, DELETE or TRUNCATE on a view | Arch v5 slide 11 (SQL view: read-only login); DP-05 |
| BR4 | Each of the other 18 service logins holds USAGE on its own schema only: no privilege on the 30 views, none in `public`, none in another service's schema, and PUBLIC holds nothing anywhere | Arch v5 slides 8, 11 and 45; DP-01, DP-02 |
| BR5 | Every view carries one `sys_objects` row and one `sys_fields` row per column, held in `rwb_source_data` | RWB-E1-069 BR5; RWB-E1-064 |
| BR6 | No constraint in an `rwb_*` schema references a table, a type or a schema outside it; no table name sits in two schemas; schema `recovery` holds no service table | RWB-E1-069 BR4; ADR-010; DP-01 |
| BR7 | The four extension tables sit in `rwb_source_data`, hold a Workbench decision about an ACE record and never a copy of an ACE column, and are 1:1 with the ACE record on the ACE business key | RWB-E1-069 BR7; Ownership Map; DF-EXT-001 to DF-EXT-049 |
| BR8 | Boundary rule BND-6 has two halves. Half A: no class names a table in schema `public`. Half B: no class outside rwb-source-data names a `v_ace_*` view or another service's schema. The allowed view list is read from the module map | REQ-DRI-006; RWB-TE-001; Arch v5 slides 11, 12, 13 and 45 |
| BR9 | A service other than rwb-source-data reaches ACE data through the source-data REST contract or a Temporal activity, one hop, 2 s client budget, never through the views and never through another service's tables | DP-05, DP-11; Arch v5 slides 11 to 13 and 45 |
| BR10 | A change to the 30-view list, to the grant matrix or to either half of BND-6 is a migration plus a rule change, approved by the recovery tech lead and the data architect; an applied grant is never edited | RWB-E1-069 BR9; DP-15 |

### 9. State transitions

None for a case status. This story reads, attempts and asserts; it changes no business row.

The schema, grant and run states the harness observes:

| Item | States |
|---|---|
| `recovery.v_ace_*` | Present and compiling, or absent and named; owned by `ace_view_owner` throughout |
| `rwb_*` schema | Created and on its Flyway head, or not created and named by the preflight |
| Grant | Held, refused with SQLSTATE 42501, or granted to PUBLIC — which is a failure in every schema |
| Constraint | Inside its own schema, or crossing a schema — which is a failure and blocks the merge |
| Extension row | One row per ACE key, or the second row refused with SQLSTATE 23505 |
| Boundary verdict | Pass, or fail with the class and the object named |
| Harness run | Not started, running, passed, or failed with the criterion, the login and the object named |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of the integration harness | Owns the harness, the run file, the fixtures and the run report |
| ACE DBA and ACE schema owner | Own schema `public`, the 30 views and the grants; approve nothing in this story, supply the grants |
| rwb-source-data owner (RWB-P1-E1069-APP, RWB-P4-E1069-APP) | Owns the views' contract, the extension tables in `rwb_source_data` and the source-data operations the harness calls |
| rwb-access owner (RWB-P4-E1069-APP) | Owns the authorise check the boundary pass relies on |
| Platform DB owner (RWB-PLT-NF06-DB) | Owns the 19 schemas and the 19 logins the harness connects as |
| Recovery tech lead and data architect | Approve a change to the 30-view list, the grant matrix or either half of BND-6 |
| RW-AUDIT, internal audit | Reads the grant matrix, the view list and the run report |
| RW-PLATADM, platform administrator | Reads the deployment result and the run report; may not change a grant |
| RW-DATASTEW, data steward | Reads the dictionary rows for the 30 views |
| No role | May write a view, copy ACE data or grant a privilege to PUBLIC |

The harness holds no schema and no grant of its own: it connects as the 19 existing logins, and the only write it attempts is the duplicate extension row of AC5, which is rolled back in the same transaction.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-ACE-001 to DF-ACE-304 | the 30 `recovery.v_ace_*` views | all 304 fields, one row per view | Read |
| DF-EXT-001 to DF-EXT-012 | `rwb_source_data.party_ext` | all 12 fields | Read; the duplicate write is refused |
| DF-EXT-013 to DF-EXT-026 | `rwb_source_data.contact_point_ext` | all 14 fields | Read |
| DF-EXT-027 to DF-EXT-035 | `rwb_source_data.account_ext` | all 9 fields | Read |
| DF-EXT-036 to DF-EXT-049 | `rwb_source_data.valuation_ext` | all 14 fields | Read |
| DF-REF-097, DF-REF-098, DF-REF-105 | reference values carried on the source-data response | the three reference fields | Read |
| Not specified in the source documents (DOR-RWB-ITG-E1069-ITG-7) | schema `recovery` | no service table | None |

Field IDs are those in the Logical Data Model and Data Dictionary and are copied from RWB-E1-069. The harness owns no schema, no table and no field: `v_data_dictionary` and the `sys_objects` and `sys_fields` rows are read on the `rwb_source_data` login, and the four extension tables are read on that login too. The 30 views keep the field split of the legacy story: 177 fields in Section A over the ACE tables that exist and 127 in Section B over the tables RWB-ACE-001 adds, 304 in all. The three reference values are the codes the source-data response already carries; the harness asserts the code and never resolves a list itself (DP-07).

### 12. Contract

#### 12.1 REST operations provided

None. The harness is a test project and provides no REST operation.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| GET | `/api/recovery/source-data/v1/accounts/{id}` | P1 rwb-source-data | The account "ACC0000017" behind `v_ace_account`, read on the contract rather than the view, so that half B of AC6 passes on the real response |
| GET | `/api/recovery/source-data/v1/customers/{id}` | P1 rwb-source-data | The customer behind the party of person_key "P0000123", read on the same contract for the same pass |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | The scope check of AC6 for the reader that calls the two source-data operations |

Every call is one hop to the owning service on its own base (DP-11) with the 2 s client budget; the harness calls no service through another service and calls no path outside the three above.

#### 12.3 Events published

None. The harness publishes no business event and the grant matrix publishes nothing.

#### 12.4 Events consumed

None. No event carries a grant or a schema fact; the run reads the catalog and the contracts only.

#### 12.5 Workflows and activities

None. The harness starts no workflow. A service that reads ACE data inside a workflow does it in an activity on the source-data contract (DP-11); this story asserts the rule and adds no workflow.

#### 12.6 Schedules

None. The run is started by hand or by the wave 1 integration pipeline; no Schedule is registered and no job of the job map is touched.

#### 12.7 Tables owned

None. The harness owns no table. The objects it reads and the login it reads them on:

| Data | Owner | Reached through |
|---|---|---|
| the 30 `v_ace_*` views | schema `recovery`; view owner `ace_view_owner`; contract owner P1 rwb-source-data | the `rwb_source_data` login and the P1 source-data contract |
| `party_ext`, `contact_point_ext`, `account_ext`, `valuation_ext` | P1 rwb-source-data | the `rwb_source_data` login |
| `sys_objects`, `sys_fields`, `v_data_dictionary` | P1 rwb-source-data | the `rwb_source_data` login |
| the 88 other tables of the 19 schemas | each service's own owner, per the Ownership Map | the catalog only; no row is read |
| scope and role data behind the authorise check | P4 rwb-access | the P4 authorise contract |

#### 12.8 Contract fakes

No fake replaces a service in the SIT run. This is the integration level: the 19 real logins, the real 30 views and the real contracts replace the fakes of the app stories. The ACE tables of SIT are the only stand-in for an outside system, and they are the schema the ACE team owns.

The contract fakes of the two services whose contracts this story calls are listed below. The published version of the contract fake library is Not specified in the source documents (DOR-RWB-ITG-E1069-ITG-22).

| Fake | Contract it stands for | Use in this story |
|---|---|---|
| rwb-source-data contract fake | `/api/recovery/source-data/v1` | Replaced by the real service in the SIT run |
| rwb-access contract fake | `/api/recovery/access/v1` | Replaced by the real service in the SIT run |

The criteria, test data and flow lines that name an ACE view or an extension table test the real grants, views and keys. They are run against the real objects in SIT, not against the rwb-source-data contract fake, because a contract fake cannot prove a database privilege or constraint.

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 0 | 3 | Two source-data reads and the authorise check; one hop, 2 s (DP-11) |
| Kafka | None | None | No topic in this story |
| Temporal | None | None | No workflow, activity or Schedule in this story |
| File | None | None | No file in this story |
| SQL view | None | 30 views | Read only by the `rwb_source_data` login, 5 s statement timeout (Arch v5 slide 11) |

### 13. Solution plan

**Deliverables.** One test project `integration/recovery-w1/source-views`, with the grant-matrix probe, the boundary-test runner, the dictionary probe, the schema-boundary probe, the extension-key probe and the report writer, its run file and its fixtures.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| HarnessRunner | Runner | Preflight, run order, report, exit code |
| GrantMatrixProbe | Service | Connects as the 19 logins; reads the catalog and asserts SELECT on the 30 views for `rwb_source_data`, denial for the other 18, no privilege in `public`, own-schema-only reads, PUBLIC empty and DML refused with SQLSTATE 42501 |
| ViewOwnerProbe | Service | Asserts that `ace_view_owner` owns the 30 views and holds SELECT only on the ACE tables they read |
| SchemaBoundaryProbe | Service | Scans every constraint in the 19 `rwb_*` schemas and the table names across the 19 schemas and `recovery` |
| ExtensionKeyProbe | Service | Asserts the columns, keys and check of the four extension tables in `rwb_source_data` and the duplicate person_key refusal |
| BoundaryRunner | Service | Runs `RecoveryBoundaryTest` with the three fixtures of AC6 and reads `sourceViews` from the module map |
| DictionaryProbe | Service | Counts one `sys_objects` row per view and one `sys_fields` row per column on the `rwb_source_data` login |
| ReportWriter | Service | One row per test case, with the login, the object and the verdict, and no row data |

**Database.** None of its own. The harness creates no schema, no table and no grant; it connects as the 19 logins that already exist, and its one write attempt is refused by the primary key and rolled back. The schema `rwb_source_data` is owned by P1 rwb-source-data (section 12.7); the owner of the test role "rwb_no_grant" is Not specified in the source documents (DOR-RWB-ITG-E1069-ITG-24).

**Configuration and reference data**

- SIT, the 19 login names (from the Environment and Deployment Design), the 19 schema names and the 30-view list (from the module map).
- The 19 login names, the grant matrix on the 30 views after the split and the two-part boundary rule: Not specified in the source documents (GAP-0377; ASM-0543).
- The 5 s statement timeout, the 2 s client budget, the report layout and the run-file format.
- The synthetic values the fixtures reuse: account "ACC0000017" with delay_days 95, person_key "P0000123", the test role "rwb_no_grant" and the fixture class "AccountReader".

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-02 | `recovery_svc` login | One login per service | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-08 | RecoveryAccessGuard | Authorise contract of rwb-access and the guard library | H RWB-PLT-E1037-CON; C RWB-P4-E1037-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The ten rows above are the pattern rows of §R5.5 with their wording. The story carries no H, C or X dependency: the build dependencies of DP-03, DP-06, DP-07, DP-08, DP-15 and DP-19 stay with the service, platform and operations stories this harness proves. DP-01, DP-02 and DP-15 are the subject of the run — the 19 schemas and their logins; DP-05 is what the grant matrix enforces — one login on the views; DP-08 is the authorise check of AC6; DP-07 is the reference code the source-data response carries, which the harness asserts and never resolves; DP-03, DP-06 and DP-19 are named for completeness and are exercised by no criterion here. The I list names the two services whose behaviour it exercises, and an integration dependency never blocks a build (Template and Rules §R5.4).

**Fixtures**

| Fixture | Content | Used by |
|---|---|---|
| Login matrix | The 19 logins with their schema names, read from the run file | AC2, AC3, TC-ITG-E1069-02, TC-ITG-E1069-03 |
| View list | `sourceViews` from `recovery-modules.yaml`, 30 names | AC1, AC2, AC6, TC-E1-069-01-ITG, TC-ITG-E1069-01 |
| No-grant role | The test role "rwb_no_grant" with no grant anywhere | AC2, TC-E1-069-02-ITG |
| Account fixture | Account "ACC0000017" with delay_days 95 | AC1, TC-E1-069-06-ITG |
| Extension fixture | `party_ext` with one row for person_key "P0000123", and the duplicate insert | AC5, TC-E1-069-07-ITG, TC-ITG-E1069-05 |
| Boundary classes | "AccountReader" on `public.account`, on `recovery.v_ace_account` outside rwb-source-data, on the source-data contract; a rwb-case class on an `rwb_source_data` table | AC6, TC-E1-069-08-ITG, TC-ITG-E1069-06 |

**Run order.** Preflight on the 19 logins, the 30 views, the module map and the four extension tables; AC1 on the view count and the 30 reads; AC2 as `rwb_source_data` and as `ace_view_owner`; AC3 across the other 18 logins; AC4 on the constraint scan and the table-name scan; AC5 on the four extension tables and the duplicate; AC6 on the boundary runner with its four fixtures; the dictionary probe; the report. A failing step stops the run and the report names the criterion, the login, the object and the evidence. The duplicate insert is rolled back before the report is written.

**Done when.** The 14 test cases of section 16 pass in SIT on the real 19 logins, every one of the 19 logins passes its row of the grant matrix, both halves of BND-6 fail on their fixtures and pass on the source-data contract, no constraint and no table name crosses a schema, the four extension tables sit in `rwb_source_data` and refuse a second row for one ACE key, and the report names all 19 logins, 30 views and four extension tables with no grant to PUBLIC.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| Conformance check 1 | A view does not compile | v_ace_account does not compile: column a.core_banking_system_date does not exist |
| Conformance check 2 | A constraint references another schema | fk_case_account_account_key references public.account; no constraint in recovery may reference another schema |
| Conformance check 3 | A view has no dictionary row | v_ace_account.legacy_bucket has no data dictionary entry |
| Conformance check 4 | A service login holds a privilege in `public` or can write a view | rwb_case holds SELECT on public.account; only rwb_source_data reads the views |
| Build log | A class names a `public` table, a `v_ace_*` view outside rwb-source-data, or another service's table | Boundary rule BND-6 broken: AccountReader reads public.account. Read recovery.v_ace_account instead. / Boundary rule BND-6 broken: AccountReader names recovery.v_ace_account outside rwb-source-data. Call the source-data contract instead. |
| SQLSTATE 42501 | A login without the grant selects or writes | permission denied for schema public |
| SQLSTATE 23505 | A second row for one ACE key in an extension table | duplicate key value violates unique constraint party_ext_pkey |

No `MSG-` ID applies: this story has no user-facing message. The pipeline, SQLSTATE and build log texts are copied from RWB-E1-069 with the second half of BND-6 added, and they are for developers, not part of the message standard.

### 15. Screens and states

No screen in this story, and the harness renders nothing: it reads the catalog, the contracts and the build verdict. The platform administrator reads the deployment result and the run report under Platform administration R, and the data steward reads the dictionary rows for the 30 views. The states the harness observes are the schema, grant, constraint and run states of section 9.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-069-01-ITG | AC1, BR1 | Integration | SIT; the 30 views in schema `recovery` and the 19 schemas; a repeated run of the same read |
| TC-E1-069-02-ITG | AC2, AC3, BR3, BR4 | Integration | Sessions as the 19 service logins, `ace_view_owner` and the test role "rwb_no_grant" in SIT |
| TC-E1-069-03-ITG | AC1, BR1 | Integration | The 30-view probe in SIT, with the 14 Section B views included |
| TC-E1-069-04-ITG | AC4, BR6 | Integration | A branch adding `fk_case_account_account_key` to `public.account`; the constraint scan over the 19 `rwb_*` schemas |
| TC-E1-069-05-ITG | AC1, BR5 | Integration | 122 objects and 1,366 fields; a view column with no `sys_fields` row |
| TC-E1-069-06-ITG | AC1, BR5 | Integration | Account "ACC0000017" with delay_days 95; the dictionary query on the `rwb_source_data` login |
| TC-E1-069-07-ITG | AC5, BR7 | Integration | The duplicate person_key "P0000123" in `rwb_source_data.party_ext`; the column list of the four tables |
| TC-E1-069-08-ITG | AC6, BR8 | Integration | The fixture AccountReader on `public.account`, on `recovery.v_ace_account` and on the source-data contract; the native query fixture |
| TC-ITG-E1069-01 | AC1, BR1, BR5 | Integration | SIT; 30 views, one row each on the `rwb_source_data` login, and no `v_ace_*` view in an `rwb_*` schema |
| TC-ITG-E1069-02 | AC2, BR3 | Integration | The grant matrix on the 30 views; insert, update and delete on `recovery.v_ace_account`; `ace_view_owner` ownership |
| TC-ITG-E1069-03 | AC3, BR4 | Integration | The 18 logins in turn: own-schema read, view read, `public` read, cross-schema read, PUBLIC empty |
| TC-ITG-E1069-04 | AC4, BR6 | Integration | The constraint scan and the table-name scan across the 19 `rwb_*` schemas and schema `recovery`, and the tables of section 12.7 |
| TC-ITG-E1069-05 | AC5, BR7 | Integration | The four extension tables in `rwb_source_data` and the second row for person_key "P0000123" |
| TC-ITG-E1069-06 | AC6, BR8, BR9 | Integration | The boundary runner with four classes and `sourceViews` from the module map |
| TC-ITG-E1069-07 | AC7, BR2, BR10 | Integration | SIT; the 19 `rwb_*` schemas, the 92 tables and the applied Flyway grant migrations |

The legacy acceptance criteria of RWB-E1-069 are owned by RWB-P1-E1069-APP and RWB-P4-E1069-APP and are re-exercised here on the split, on the real 19 logins; the legacy test case IDs are kept as ITG copies with the suffix `-ITG` and their legacy data, and the new criteria AC1 to AC7 carry TC-ITG-E1069-01 to TC-ITG-E1069-07. The full test, with its Given, When and Then, is in the Recovery Workbench Test Cases workbook, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the 30 view names, the 19 logins, the schema names, the report layout and the timeouts are configuration; the run file carries them once.
- No personal data in the run file, the report, the logs or the fixtures: the fixtures reuse account "ACC0000017", person_key "P0000123" and the test role, and the report carries login names, object names and verdicts, never a row value.
- The harness owns no schema, no table and no grant; it connects as the 19 existing logins and writes nothing that survives the run.
- No service reads another service's schema and no service but rwb-source-data names a `v_ace_*` view (DP-01, DP-05); both halves of BND-6 fail the build, and the check is a regression test, not a review.
- No write path into ACE data: INSERT, UPDATE and DELETE on a view are refused by the database and asserted in every run.
- No privilege for PUBLIC anywhere, and no `GRANT ... ON ALL TABLES` in any migration that touches the views.
- The 30-view list is read from the module map, never from the runner; a change to it is a rule change, not a test change.
- The harness never uses production data, never points at a production database and never connects as a production schema owner.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-RDF-002 | Account balance, arrears, payments and classification for every account at 90 or more days past due are read from ACE through `v_ace_account` and `v_ace_payment`, current to the previous working day | the 30 `recovery.v_ace_*` views, the SELECT-only grant to `rwb_source_data`, `ace_view_owner`, the source-data reads of 12.2 | TC-E1-069-01-ITG, TC-E1-069-03-ITG, TC-E1-069-05-ITG, TC-E1-069-06-ITG, TC-ITG-E1069-01, TC-ITG-E1069-02 |
| REQ-DRI-006 | No component calls a system of record directly | boundary rule BND-6 halves A and B, the `sourceViews` list in the module map, the P1 source-data contract, the P4 authorise check | TC-E1-069-02-ITG, TC-E1-069-04-ITG, TC-E1-069-07-ITG, TC-E1-069-08-ITG, TC-ITG-E1069-03, TC-ITG-E1069-04, TC-ITG-E1069-05, TC-ITG-E1069-06 |

The legacy story is RWB-E1-069, disposition Split (rework). RWB-P1-E1069-APP and RWB-P4-E1069-APP are its build owners in the target services; this ITG story is the proof over them and holds no acceptance criterion of its own beyond the six new ones.

### 19. Out of scope

- The per-service DB stories and the platform DB story: RWB-PLT-NF06-DB creates the 19 schemas and logins, and each service's DB story creates its own tables.
- The 30 view definitions, the three helper functions and the migration of the views (RWB-P1-E1069-APP, RWB-P4-E1069-APP); this story proves them, it does not write them.
- ACE Tier 2 and RWB-ACE-001: the 14 Tier 2 tables, the 12 columns it adds to `account`, `customer` and `efs_action`, and the SELECT grants on them stay with the ACE team.
- The data dictionary content and its maintenance: RWB-E1-064, with the metadata rows of RWB-E1-001; this story counts the rows and adds none.
- Masking at the API and the PII access log: RWB-E1-037 and RWB-E1-016.
- The rest of RWB-TE-001: this story runs boundary rule BND-6 and the `sourceViews` list and changes neither.
- Any change to the 30-view list, the grant matrix or either half of BND-6: the data architect and the recovery tech lead, with a new version of the ACE Data Tier Map v1.
