# RWB-P1-E1016-DB Access control per data product and catalog entries - ACE DB

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Version 3 changes**

- RD-P1-025 changes the baseline to 123 objects and 1,379 fields; RD-P1-026 adds the RW-COMPLY/DP02 seed row (review #3, #11).
- RD-P1-020 and RD-P1-045 define access-version replay and forward-only migrations (review #12, #15).
- Updated the catalog grain, ownership checks, migration names and seed coverage (review #1, #4, #6, #13, #14, #18, #20, #21).
- The catalog's access block holds only rows in force; the role list is read as `roleCode` from rwb-access.yaml 5.1.0; the governed-field check of RD-P1-025 and the corrective script per migration of RD-P1-045 are added (AC18, AC19; review #2, #6, #8, #12, #15, #16, #22, #24).
- Finishing pass (requests W2-tests-1064, W6-registers-0504; test case backfill): the Test Cases v9 database cases are cited. RD-P1-063 names this slice for the authorise interim rules; it makes no authorise call, so those rules are carried by the APP and CON stories.



| Item | Value |
|---|---|
| Story key | RWB-P1-E1016-DB |
| Work type | DB (ACE DB) |
| Suggested owner | ACE team (suggested; any team may pick up this story) |
| Service | rwb-source-data |
| Service epic | RWB-SVC-P1 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-016 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP02, DP05, DP07, DP08, DP11, DP19 |
| Parallel lane | L-P1-J |
| Ready to start | After RWB-P1-E1001-APP, RWB-P1-E1069-DB and RWB-PLT-E1044-CON; role-list contract fake available |
| Size | Not specified in the source documents (DOR-RWB-P1-E1016-DB-16) |
| Depends on (build) | RWB-P1-E1001-APP, RWB-P1-E1069-DB, RWB-PLT-E1044-CON |
| Contract dependencies | RWB-P4-E1037-CON; rwb-access.yaml 5.1.0 `GET /admin/roles` (role list and its fake) |
| Contract version | rwb-source-data.yaml 5.1.0 (API Specification v7) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v1.md (FR-P1-004, FR-P1-006, FR-P1-012, FR-P1-013, FR-P1-024, FR-P1-025, FR-P1-026, FR-P1-027, FR-P1-030) |
| Readiness decisions | RD-P1-020, RD-P1-021, RD-P1-025, RD-P1-026, RD-P1-043, RD-P1-045, RD-P1-063 |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-016 for the ACE database work of rwb-source-data. RWB-P1-E1001-APP already creates `data_product`, `data_product_access`, `sys_objects`, `sys_fields` and `sys_field_version` in schema `rwb_source_data` with its own migration, so this story delivers the database slice that is still missing: the three indexes the access check and the catalog read need, the read model `v_data_product_catalog`, the seed of `data_product_access` version "DPA-2026.11" with the rows the sources give, the dictionary baseline presence check (at least 123 objects and 1,379 fields) and the schema checks; it creates no table and holds no masking row (DP-01, DP-02, DP-15; Architecture v5 slides 29 and 41). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P1-E1016-DB). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: dictionary baseline, seed, migration and ownership checks aligned to final rulings. Tool: T3 Code.

### 1. Story

As a **P1 database engineer**, I want **the three indexes on `data_product_access`, `sys_fields` and `sys_objects` that the access check and the catalog read need, the read model `v_data_product_catalog` that joins the dictionary to the product and its access rows without naming another service's table, the seed of `data_product_access` version "DPA-2026.11" for the roles and products the sources give, the at-least 123-object and 1,379-field baseline conformance check that fails the build on a mismatch, and the schema checks that prove no constraint names `public` or another `rwb_*` schema and the login owns `rwb_source_data` only**, so that **a role's access row is found by an index instead of a scan, the catalog entry is one read model instead of four joins in code, and the seven-row access seed is a database fact that a pipeline test can prove**.

This is the database slice of legacy RWB-E1-016 for rwb-source-data. It delivers:

- the three indexes: `ix_data_product_access_product_role` on `data_product_access(product_code, role_code, valid_from)`, `ix_sys_fields_object_field` on `sys_fields(object_name, field_name)` and `ix_sys_objects_product` on `sys_objects(data_product)`;
- the read model `v_data_product_catalog`, one row per product field, joining `sys_fields`, `sys_objects` and `data_product`, with the access block from `data_product_access` in force, and with the retention class left to the service because it is P5's and is read through P5's contract, not by SQL;
- the seed of `data_product_access` version "DPA-2026.11": RW-CASEOWN and RW-AUDIT read DP02; RW-PHONECOL reads DP01, DP02, DP03 and DP05 and has no row for DP06;
- the dictionary baseline presence check (at least 123 objects and 1,379 fields), extended to the seed: every seeded product and every seeded role resolves;
- the schema checks: no constraint names `public` or another `rwb_*` schema, and the login owns `rwb_source_data` only;
- the migration set on rwb-source-data's per-service Flyway sequence, with a repeated run that changes nothing (DP-15).

It creates no table: `data_product`, `data_product_access`, `sys_objects`, `sys_fields` and `sys_field_version` are RWB-P1-E1001-APP's, and the four extension tables are RWB-P1-E1069-DB's (slice-boundary gap: GAP-0484; ASM-0676). It does not own `masking_rule` and does not create it, and it reads no masking row by SQL (GAP-0481; ASM-0673). It writes no application code and no REST operation.

### 2. Business rationale

The legacy story proved access control with one schema, one role model and one guard in the same process. In the target the same controls work across 19 schemas and 19 logins, where ownership is enforced by grants and not by separate servers (Architecture v5 slide 29). Two of the controls become cheaper and one becomes testable. Cheaper: the access check and the catalog read are the two hottest reads of the capability, and neither had a supporting index when the estate was one schema with one planner and one set of statistics. Testable: the access version in force is a row with a valid-from date, so a pipeline check can assert exactly which roles read which product on which date, instead of reading a configuration file.

The read model is the second reason. The catalog entry joins four P1 tables, and the fifth thing it shows, the retention class, belongs to rwb-document (Ownership Map v1: `retention_rule` to P5). A join to `rwb_document.retention_rule` would be a cross-schema read the boundary rule forbids, so the model stops at P1's four tables and the service merges P5's answer (DP-01; GAP-0481; ASM-0673).

Serves REQ-RDF-010 (access per data product by role) and REQ-RDF-011 (one catalog entry per data product). The business value is not restated here: this story adds none, it makes the two reads of the app story exact and fast.

### 3. Preconditions

- The per-service Flyway sequence of rwb-source-data exists with its own history table in schema `rwb_source_data`, and the baseline has been applied on it (DP-15; RWB-PLT-E1044-CON).
- RWB-P1-E1001-APP is done: `data_product` with the 14 rows DP01 to DP14, `data_product_access`, `sys_objects` with its 123 baseline rows, `sys_fields` with its 1,379 baseline rows, `sys_field_version` and `data_contract` exist in `rwb_source_data`, and the read model `v_data_dictionary` is in place.
- RWB-P1-E1069-APP and RWB-P1-E1069-DB are done or in flight: the 30 `recovery.v_ace_*` views exist and the login holds SELECT on each of them, for the APP story's ACE read criteria.
- The login `rwb_source_data` exists in DEV and SIT, owns schema `rwb_source_data` and no other schema, and has no table, sequence or function privilege in `public` (DP-02; Architecture v5 slides 11 and 29). PostgreSQL schema `public` USAGE is not asserted here.
- The role list and product list are data: product codes come from `data_product`; role codes are `Role.roleCode` of `GET /api/recovery/access/v1/admin/roles` (rwb-access.yaml 5.1.0) and its published fake. Pending: the fake version, owner rwb-access, GAP-0983; the pipeline's identity and permission for the call, owner rwb-access owner, GAP-3447.
- Physical Schema v9 already lists the three indexes of this story; the view `v_data_product_catalog` is not yet in its view script (requested from the data architect).
- The complete `data_product_access` seed is not given by the sources: only the seven rows of section 11 are specified, and the rest is Not specified in the source documents (GAP-0482; ASM-0674).
- The source data product seed starts on 2026-11-30 while DPA-2026.11 starts on 2026-11-20. Pending: whether the catalog filters by `data_product.valid_from`, owner data architect, tracked as GAP-3440.
- No approval is required to run a Draft migration on a development database; the migration is released to SIT only after its tests in Test Cases v9 pass.

### 4. Flow

1. The ACE database engineer checks out the rwb-source-data migration folder and confirms the highest applied version on the service sequence (RWB-P1-E1001-APP's baseline and its dictionary migration).
2. The engineer writes the index migration: the three indexes of section 13, on the tables RWB-P1-E1001-APP created, with `CREATE INDEX IF NOT EXISTS` semantics on the service sequence and no change to any column.
3. The engineer writes the read-model migration: `v_data_product_catalog`, one row per product field, joining `sys_fields` to `sys_objects` to `data_product`, with the access block read from `data_product_access` where the version is in force; the view names no table outside `rwb_source_data` and carries no `retention_rule` column.
4. The engineer writes the seed migration for version "DPA-2026.11": the seven rows of section 11, each with its product code, role code, `can_read` true, the version label, the valid-from date and a null valid-to date; no row for DP06 and no other role or product.
5. The pipeline applies the three migrations in order on the service sequence, first to an empty schema and then to a copy of the SIT schema.
6. The pipeline runs the dictionary conformance check: the E1001 baseline migration is present, every baseline object name and field ID is present, the counts are at least 123 objects and 1,379 fields, and every seeded `product_code` has one `data_product` row and every seeded `role_code` appears in the rwb-access role list of the published fake.
7. The pipeline runs the schema checks: no constraint of `rwb_source_data` names `public` or another `rwb_*` schema, the login owns `rwb_source_data` only, and no migration of this story creates a table RWB-P1-E1001-APP already creates.
8. The pipeline runs the seed check in a transaction it rolls back: the version in force on 2026-11-20 holds exactly the seven rows, no row for DP06 as RW-PHONECOL exists, and the catalog read returns active data products; whether it filters `data_product.valid_from` remains Pending under GAP-3440.
9. The engineer records each migration in the release notes of the sequence with its version number and its checksum.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | An index migration runs before the table it indexes exists | The statement fails on the missing relation and the stage stops; no index is recorded | Pipeline error, no message id | AC15 |
| X2 | A migration of this story tries to create a table RWB-P1-E1001-APP already creates | The check fails the build and names the table and the owning story; no table is created | Pipeline error, no message id | AC7 |
| X3 | The read model names a table outside `rwb_source_data`, or a `retention_rule` column | The schema check fails the build and names the view and the object | Check finding, no message id | AC13 |
| X4 | A seeded row names a product code with no `data_product` row, or a role code outside the rwb-access role list | The pipeline fails with `Seed check failed: {productCode} or {roleCode} is not in the published list` and names the row | Pipeline log text; no message ID | AC4 |
| X5 | A second row is written for the same product, role and version | The unique key of `data_product_access` refuses it with SQLSTATE 23505 and the first row is unchanged | SQLSTATE 23505 duplicate key value violates unique constraint | AC3, AC11 |
| X6 | A constraint of `rwb_source_data` names `public` or another `rwb_*` schema | The schema check fails the build and names the constraint and the referenced object | Check finding, no message id | AC5 |
| X7 | The login owns a schema other than `rwb_source_data` | The schema check fails the build and names the login and the schema | Check finding, no message id | AC14 |
| X8 | A migration is applied a second time | Flyway reports the version as already applied; no index, row or view changes | None | AC7 |

X5 and X6 are the legacy paths of RWB-E1-016 carried onto the split; X1 to X4, X7 and X8 are the paths the slice boundary and the per-service sequence add.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Three migrations on the service's own sequence, on tables another P1 story already created; nothing to build against and no application code |
| Negotiable | Index names follow the platform naming library; the three column sets are fixed by the access check and the two catalog reads |
| Valuable | The access row is found by an index, the catalog entry is one read model, and the version in force is a testable database fact |
| Estimable | Three indexes, one view, seven seed rows and the pipeline checks |
| Small | Days, not weeks, with the catalogue checks |
| Testable | Every criterion in section 7 is one catalogue query, one pipeline run, or one rolled-back write |

### 7. Acceptance criteria

```gherkin
Feature: The indexes, the catalog read model and the DPA-2026.11 access seed of rwb-source-data

  Background:
    Given the E1001 baseline migration and dictionary rows are applied in schema rwb_source_data
    Given the login rwb_source_data owns schema rwb_source_data and no other schema
    Given the role list is supplied by GET /api/recovery/access/v1/admin/roles from RWB-P4-E1037-CON

  Scenario: AC1 The three lookup indexes exist with their listed columns
    Given the three index migrations are applied
    When pg_indexes is queried for schema rwb_source_data
    Then ix_data_product_access_product_role exists on data_product_access with columns product_code, role_code and valid_from in that order
    Then ix_sys_fields_object_field exists on sys_fields with columns object_name and field_name in that order
    Then ix_sys_objects_product exists on sys_objects with data_product as its column
    Then all three indexes are non-unique

  Scenario: AC2 The catalog read model keeps one row per active product field
    Given the read-model and seed migrations are applied and the business date in Asia/Bangkok is 2026-11-30
    When v_data_product_catalog is queried for DP02
    Then each active field_id appears once with its product, object and field properties
    Then system_of_record is "ACE (ingested from SCBPDM and the core bank)" on every DP02 row
    Then access_rows is one JSON array holding exactly the rows of RW-AUDIT, RW-CASEOWN, RW-COMPLY and RW-PHONECOL
    Then inactive products, objects, fields and access rows are absent
    Then the view names only data_product, sys_objects, sys_fields and data_product_access in rwb_source_data
    Then no retention_class column is present

  Scenario: AC3 The DPA-2026.11 seed contains the seven sourced rows
    Given the seed migration is applied
    When data_product_access is queried for access_version DPA-2026.11
    Then RW-CASEOWN and RW-AUDIT each have can_read true on DP02
    Then RW-COMPLY has can_read true on DP02
    Then RW-PHONECOL has can_read true on DP01, DP02, DP03 and DP05
    Then RW-PHONECOL has no row on DP06
    Then exactly seven rows are present and every row has valid_from 2026-11-20 and valid_to null

  Scenario: AC4 The conformance check verifies the complete E1001 baseline and governed additions
    Given the E1001 baseline and this story migrations are applied in SIT
    When DictionaryConformanceCheck runs
    Then the E1001 baseline migration has a Flyway history row
    Then every baseline object name and field_id is present
    Then the counts are at least 123 sys_objects rows and 1,379 sys_fields rows, including 304 ACE view fields
    Then every field added after the baseline has a sys_field_version row from an approved governed load
    Then every seeded product_code exists in data_product and every seeded role_code is a roleCode of the role-list fake
    When the role-list fake cannot be reached
    Then the check fails and names RWB-P4-E1037-CON without recording a successful migration

  Scenario: AC5 No constraint crosses the rwb_source_data schema boundary
    Given the applied schema rwb_source_data
    When the catalogue is queried for every constraint of that schema
    Then no constraint references public or another rwb_* schema
    Then every foreign key references a table in rwb_source_data
    When a branch adds a foreign key to another schema
    Then SchemaBoundaryCheck fails and names the constraint and referenced object

  Scenario: AC6 The service login owns only its schema and has no foreign object privileges
    Given the login rwb_source_data and the service logins in the platform database
    When OwnershipCheck queries schema ownership and object privileges
    Then rwb_source_data owns schema rwb_source_data only
    Then it has no privilege on another rwb_* schema and no table, sequence or function privilege in public
    Then the check does not assert USAGE on schema public

  Scenario: AC7 The migration set stays within the owned slice and repeats without changes
    Given RWB-P1-E1001-APP created data_product, data_product_access, sys_objects, sys_fields and sys_field_version
    When this story migration set is applied in sequence
    Then no migration runs CREATE TABLE, ALTER TABLE or DROP TABLE for those five tables and their column and constraint definitions are unchanged
    Then a second Flyway run has no pending migration and changes no index, row or view
    Then no migration creates or reads masking_rule, role or permission
    Then this story creates no table

  Scenario: AC9 An applied migration is corrected by a new version
    Given a migration of this story is applied and its checksum is recorded
    When a branch changes the applied migration text
    Then the pipeline refuses the changed checksum and names the migration version
    Then the correction is a new migration on the same sequence and the applied file remains unchanged

  Scenario: AC10 A duplicate access seed row is refused
    Given the DPA-2026.11 seed
    When a second row for DP02, RW-AUDIT and DPA-2026.11 is inserted
    Then SQLSTATE 23505 is returned and the first row remains unchanged

  Scenario: AC11 A future access row is not returned before its start date
    Given a rolled-back DPA-2026.12 row for DP06 and RW-PHONECOL with valid_from 2026-12-15
    When the in-force query runs for business date 2026-12-14 in Asia/Bangkok
    Then no row is returned for DP06 and RW-PHONECOL
    When the query runs for business date 2026-12-15
    Then the row is returned

  Scenario: AC12 Other service logins and ungranted roles cannot read the model or access table
    Given another rwb_* service login, a no-grant role and PUBLIC
    When any of them selects from v_data_product_catalog or data_product_access
    Then SQLSTATE 42501 is returned

  Scenario: AC13 A read model that names a foreign object fails
    Given a branch where v_data_product_catalog joins an object outside rwb_source_data
    When SchemaBoundaryCheck runs
    Then the build fails and names the view and foreign object

  Scenario: AC14 A second owned schema fails the ownership check
    Given a test database where rwb_source_data owns a second schema
    When OwnershipCheck runs
    Then the build fails and names rwb_source_data and the second schema

  Scenario: AC15 An index migration before its table fails without a successful history row
    Given a test schema without sys_fields
    When the index migration runs
    Then it fails, leaves no index from that migration and records no successful Flyway history row

  Scenario: AC16 Inactive rows are excluded from the catalog read model
    Given one inactive product, object, field and access row
    When v_data_product_catalog is queried
    Then none of those inactive rows appears

  Scenario: AC17 Read-model column names and types match the published source columns
    Given the applied v_data_product_catalog view
    When information_schema.columns is queried
    Then every projected column name and type matches its source-table definition
    Then access_rows is JSONB and retention_class is absent

  Scenario: AC18 A superseded access row leaves the access block
    Given a rolled-back version DPA-2026.12 valid from 2026-12-15 that replaces the DP02 row of RW-AUDIT, with valid_to 2026-12-14 on the DPA-2026.11 row
    When v_data_product_catalog is queried for DP02 on business date 2026-12-15
    Then access_rows holds one RW-AUDIT row, of DPA-2026.12
    When it is queried on business date 2026-12-14
    Then access_rows holds one RW-AUDIT row, of DPA-2026.11

  Scenario: AC19 The seed does not overwrite an existing key
    Given a row (DP02, RW-AUDIT, DPA-2026.11) already exists with can_read false and no Flyway history row for the seed
    When the seed migration runs
    Then it fails with SQLSTATE 23505, the stored row is unchanged and no other seed row is written
```

The numbering preserves AC9 from the v2 file; AC8 was a review activity, so its coverage check is a review checklist in section 16 rather than a runtime acceptance criterion. Section 16 cites the Test Cases v9 case of every criterion.

### 8. Business rules

| ID | Rule | Source | Covered by |
|---|---|---|---|
| BR1 | A role reads a data product only through a `data_product_access` row in force for that role and product | REQ-RDF-010; FEAT-RDF-15 | AC3, AC11 |
| BR2 | The access row is found by product, role and valid-from date, and the index `ix_data_product_access_product_role` serves that lookup | FSD P1 A2.15; TSD P1 T6.3 | AC1 |
| BR3 | Each data product has one catalog row per field, with the product, its system of record, its owner and its access rows; the retention class is P5's and arrives through P5's contract | REQ-RDF-011; Ownership Map v1 | AC2 |
| BR4 | No constraint of `rwb_source_data` names `public` or another `rwb_*` schema; a link to an ACE record is a business key with no foreign key | D-RCV-35 U4; ADR-010; DP-01 | AC5 |
| BR5 | One login per service: `rwb_source_data` owns its own schema and holds no grant on another | DP-02; Architecture v5 slide 29 | AC6 |
| BR6 | Masking rows are rwb-access's: this story creates no `masking_rule` row and reads none by SQL | Ownership Map v1; DL26 (open; assumptions ASM-0247, ASM-0264, ASM-0275, ASM-0355); DP-08 | AC7 |
| BR7 | An access row is in force when `valid_from <= business_date` and (`valid_to` is null or `business_date <= valid_to`) in Asia/Bangkok; at most one row per product and role is in force on a date. The apply handler of RWB-P1-E1016-APP sets `valid_to` on a replaced row; this story seeds and reads | REQ-RDF-010; FSD P1 A2.15; RD-P1-020 | AC3, AC11, AC18 |
| BR8 | An applied migration is never edited; a correction is a new version on the same sequence, and a seed does not overwrite an existing key | DP-15; RWB-PLT-E1044-CON; RD-P1-045 | AC9, AC19 |

**Where each rule lives in the target.** BR1, BR2, BR3, BR4, BR5 and BR7 are this story's objects and checks: the seed, the index, the read model, the constraint scan and the ownership check. BR6 is the boundary this story must not cross: the masking rows stay in `rwb_access` and the app story reads the answer, so no column of `masking_rule` appears in the read model (GAP-0481; ASM-0673). BR8 is the rule of the per-service sequence, and the repeated-run criterion proves it. The section 16 review checklist traces every rule to a criterion and a v9 test; AC9 refuses a change to an applied migration (BR8).

Related register rows: GAP-0341 (catalog composition) and GAP-0483 (access-load ownership) are resolved by directive; GAP-1501 (where masking rules are held) and GAP-1510 (classification and retention values) stay open business decisions and change nothing in this story's objects.

### 9. State transitions

None in the runtime sense: a table has no state machine and this story changes no business row. The states this story moves through are the migration states of the service's Flyway history and the states of an access version.

| Item | States |
|---|---|
| a migration of this story | Pending, applied or failed; an applied version is never edited and a correction uses a new migration |
| an access version | Seeded, in force from its valid-from date, superseded by a later version, never deleted |
| an access row | In force, or not yet in force because its valid-from date is later than the business date |
| the read model | Absent, created, replaced by a corrected view in a later version |
| the login | Present and owning its own schema, or absent and named by the preflight; never a member of another service's login role |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| P1 database engineer | Writes and runs the migration set and the checks |
| ACE team lead and ACE DBA | Own schema `public` and the database; approve index and view changes on the ACE server |
| Recovery tech lead and data architect | Approve a change to the column sets of the three indexes and to the read model |
| Recovery migration account | Applies this story's migrations in DEV and SIT |
| rwb-source-data owner (RWB-P1-E1016-APP) | Owns the two operations that read these objects; writes no index, no view and no seed row |
| rwb-access (P4) | Owns the role list and the masking rows; supplies the role list this story validates against |
| rwb-document (P5) | Owns the retention class the catalog entry carries; this story creates no retention column |
| Platform release operator | Runs the migration sequence and publishes its release evidence |
| RW-AUDIT, internal audit | No database access; sees access data only through the operations of RWB-P1-E1016-APP or its audit evidence |
| RW-DATASTEW, data steward | No database access; reads the catalog through `GET /admin/data-products` of RWB-P1-E1016-APP |
| No approval level of the delegation of authority applies | A schema change is not a credit decision |

The login is `rwb_source_data` (Architecture v5 slides 11 and 29; DP-02). Its credential and rotation are held by the platform, and no credential appears in a migration, a script or a runbook.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-REF-080 | data_product_access | id | Seed (one row per product, role and version) |
| DF-REF-081 | data_product_access | product_code | Seed: DP02 for RW-CASEOWN and RW-AUDIT; DP01, DP02, DP03 and DP05 for RW-PHONECOL |
| DF-REF-082 | data_product_access | role_code | Seed: RW-CASEOWN, RW-AUDIT, RW-PHONECOL |
| DF-REF-083 | data_product_access | can_read | Seed: true on all seven rows |
| DF-REF-084 | data_product_access | access_version | Seed: "DPA-2026.11" |
| DF-REF-085 | data_product_access | valid_from | Seed: 2026-11-20 |
| DF-REF-086 | data_product_access | valid_to | Seed: null |
| DF-REF-071, DF-REF-072, DF-REF-073, DF-REF-074, DF-REF-075, DF-REF-077, DF-REF-078 | data_product | product_code, product_name, definition, system_of_record, owner_role, refresh_cycle, expected_by | Read by the read model; the rows are RWB-P1-E1001-APP's |
| DF-REF-088, DF-REF-090, DF-REF-091, DF-REF-092 | sys_objects | object_name, subject_area, data_product, system_of_record | Read by the read model |
| DF-REF-095 to DF-REF-100, DF-REF-103, DF-REF-104, DF-REF-105 | sys_fields | field_id, object_name, field_name, data_type, physical_type, is_mandatory, source_system, source_field, is_personal | Read by the read model |
| DF-REF-119 | retention_rule (P5) | record_class | **Not read here**: the class crosses P5's contract, not a join |

The seven seed rows in full:

| product_code | role_code | can_read | access_version | valid_from | valid_to | BR Field ID |
|---|---|---|---|---|---|---|
| DP02 | RW-CASEOWN | true | DPA-2026.11 | 2026-11-20 | null | DF-REF-080 to DF-REF-086 |
| DP02 | RW-AUDIT | true | DPA-2026.11 | 2026-11-20 | null | DF-REF-080 to DF-REF-086 |
| DP01 | RW-PHONECOL | true | DPA-2026.11 | 2026-11-20 | null | DF-REF-080 to DF-REF-086 |
| DP02 | RW-PHONECOL | true | DPA-2026.11 | 2026-11-20 | null | DF-REF-080 to DF-REF-086 |
| DP02 | RW-COMPLY | true | DPA-2026.11 | 2026-11-20 | null | DF-REF-080 to DF-REF-086 |
| DP03 | RW-PHONECOL | true | DPA-2026.11 | 2026-11-20 | null | DF-REF-080 to DF-REF-086 |
| DP05 | RW-PHONECOL | true | DPA-2026.11 | 2026-11-20 | null | DF-REF-080 to DF-REF-086 |

No row for DP06 and no other role or product is seeded: the sources give these seven rows only, and the rest of the version is Not specified in the source documents (GAP-0482; ASM-0674). The valid-from date 2026-11-20 is the date the legacy story's background uses for the version in force. The read-model object v_data_product_catalog is not an LDM v9 or Data Classification v5 entity or field; it is the read model of this story and carries no BR Field ID. The data steward closes the rest of DPA-2026.11 by a later approved load; no row is granted by default.

The view joins `data_product.product_code` varchar(25) to `sys_objects.data_product` varchar(10) (Physical Schema v9). Pending: whether the widths are aligned, owner data architect, GAP-3448; the join works as written.

### 12. Contract

#### 12.1 REST operations provided

None. This is a database story and publishes no operation.

#### 12.2 REST operations consumed

None at run time. The seed is validated against the rwb-access role list through the published contract in the pipeline, not by the database.

#### 12.3 Events published

None. The topic of the service is `rwb.source-data.events.v1` with event names `rwb.source-data.<Event>.v1` (DP-14), and this story publishes nothing on it.

#### 12.4 Events consumed

None.

#### 12.5 Workflows and activities

None.

#### 12.6 Schedules

None. The migration set runs in the release pipeline, not on a Temporal Schedule.

#### 12.7 Tables owned

| Table | Schema | Owner (Ownership Map v1) | This story |
|---|---|---|---|
| data_product | rwb_source_data | P1 | **Not created here**: RWB-P1-E1001-APP created it; the read model reads active product rows |
| data_product_access | rwb_source_data | P1 | **Not created here**: RWB-P1-E1001-APP created it; this story adds `ix_data_product_access_product_role` and the seven seed rows |
| sys_objects | rwb_source_data | P1 | **Not created here**: adds `ix_sys_objects_product`; the read model reads its 123 baseline rows |
| sys_fields | rwb_source_data | P1 | **Not created here**: adds `ix_sys_fields_object_field`; the read model reads its 1,379 baseline rows |
| sys_field_version | rwb_source_data | P1 | **Not touched here**: RWB-P1-E1001-APP created it and a later story writes it |
| data_contract | rwb_source_data | P1 | **Not touched here**: RWB-P1-E1001-APP created it |
| v_data_product_catalog | rwb_source_data | P1 | **Created here**: the read model of section 13, with no `retention_rule` column and no object outside the schema; a read-model object, not an LDM v9 or Data Classification v5 entity |
| party_ext, contact_point_ext, account_ext, valuation_ext | rwb_source_data | P1 | Not touched: RWB-P1-E1069-DB creates them |
| masking_rule, role, permission | rwb_access | P4 | **Not created and not read**: the role list crosses the contract in the pipeline check |

No table of another service is read, created or altered, and no foreign key crosses a schema (DP-01). This story creates no table (GAP-0484; ASM-0676).

#### 12.8 Contract fakes

| Fixture | Serves | Used by |
|---|---|---|
| Delivered-tables fixture | RWB-P1-E1001-APP | A container at that story's migration, so the indexes, the view and the seed are tested against the real tables |
| rwb-access role-list stub | RWB-P4-E1037-CON | The role codes the conformance check validates the seed against |
| Product list fixture | `data_product` of the baseline | The 14 product codes the seed and the read model are checked against |

A database story uses no service contract fake; the three fixtures above stand in for the two neighbouring stories and for the role list.

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | None | None | No operation in this story |
| Kafka | None | None | No topic in this story |
| Temporal | None | None | No workflow, activity or Schedule |
| File | None | None | Migrations are deployed by the release pipeline, not by a file interface |
| SQL view | `v_data_product_catalog` in `rwb_source_data` | The four P1 tables behind it | SELECT only, no other service's schema, and no retention join |

### 13. Solution plan

**Sequencing.** rwb-source-data's Flyway sequence is owned by the platform (DP-15). This story's three migrations sit after RWB-P1-E1001-APP's baseline and dictionary migration:

| Position on the sequence | File | Contents |
|---|---|---|
| earlier | from RWB-P1-E1001-APP | Schema `rwb_source_data`, its tables, the 14 product rows, the 123 and 1,379 baseline dictionary rows and `v_data_dictionary` |
| next | `V<seq>__rwb_p1_e1016_access_indexes.sql` | The three indexes |
| next | `V<seq>__rwb_p1_e1016_product_catalog_view.sql` | `v_data_product_catalog` |
| next | `V<seq>__rwb_p1_e1016_access_seed.sql` | The seven rows of version "DPA-2026.11" |

Each file follows `V<seq>__rwb_p1_e1016_<name>.sql` and starts with `-- Story: RWB-P1-E1016-DB` (D-RCV-28). An applied migration is never edited; a correction uses a new version on the same sequence (RD-P1-045). This delivery supplies no rollback migration; a correction uses a new forward migration. A seed migration fails on an existing key unless Flyway records that version as already applied. The states of a migration are Pending, Applied and Failed. Corrective forward script per file (RD-P1-045):

| Applied file | Correction |
|---|---|
| access indexes | New `V<next>__rwb_p1_e1016_access_indexes_fix.sql` that drops the wrong index and creates the right one; dropping follows the expand-only rule |
| product catalog view | New `V<next>__rwb_p1_e1016_product_catalog_view_fix.sql` with `CREATE OR REPLACE VIEW`; a column is not removed or retyped in the same release |
| access seed | New `V<next>__rwb_p1_e1016_access_seed_fix.sql` that sets the wrong row inactive or adds a later access version; no row is deleted |

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-02 | `recovery_svc` login | One login per service | none |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-08 | RecoveryAccessGuard | Authorise contract of rwb-access and the guard library | H RWB-PLT-E1037-CON; C RWB-P4-E1037-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-01, DP-02 and DP-05 are the subject of this story: one schema, one login and the read path of the views. DP-08 is why the role list is validated through a contract in the pipeline instead of a local list. DP-07, DP-11 and DP-19 are named for completeness of the pattern set: this story calls no contract at run time, starts no workflow and serves no screen.

**Indexes**

```sql
CREATE INDEX IF NOT EXISTS ix_data_product_access_product_role
    ON rwb_source_data.data_product_access (product_code, role_code, valid_from);

CREATE INDEX IF NOT EXISTS ix_sys_fields_object_field
    ON rwb_source_data.sys_fields (object_name, field_name);

CREATE INDEX IF NOT EXISTS ix_sys_objects_product
    ON rwb_source_data.sys_objects (data_product);
```

No index is unique, because the unique key of `data_product_access` on (product_code, role_code, access_version) already exists and a second unique index would duplicate it; no column or constraint changes.

**Read model** (shape; the file itself is written in the migration folder)

```sql
CREATE OR REPLACE VIEW rwb_source_data.v_data_product_catalog AS
SELECT p.product_code, p.product_name, p.definition, p.owner_role, p.system_of_record,
       p.refresh_cycle, p.expected_by,
       o.object_name, o.subject_area, o.system_of_record AS object_system_of_record,
       f.field_id, f.field_name, f.data_type, f.physical_type, f.is_mandatory,
       f.source_system, f.source_field, f.is_personal, a.access_rows
  FROM rwb_source_data.data_product p
  JOIN rwb_source_data.sys_objects o ON o.data_product = p.product_code AND o.is_active
  JOIN rwb_source_data.sys_fields f ON f.object_name = o.object_name AND f.is_active
  LEFT JOIN LATERAL (
       SELECT COALESCE(jsonb_agg(jsonb_build_object('roleCode', a.role_code, 'canRead', a.can_read, 'accessVersion', a.access_version, 'validFrom', a.valid_from, 'validTo', a.valid_to) ORDER BY a.role_code, a.access_version), '[]'::jsonb) AS access_rows
         FROM rwb_source_data.data_product_access a
        WHERE a.product_code = p.product_code AND a.is_active
          AND a.valid_from <= (CURRENT_TIMESTAMP AT TIME ZONE 'Asia/Bangkok')::date
          AND (a.valid_to IS NULL OR (CURRENT_TIMESTAMP AT TIME ZONE 'Asia/Bangkok')::date <= a.valid_to)
  ) a ON true
 WHERE p.is_active;
```

The view names four tables, all in `rwb_source_data`, filters inactive product, object, field and access rows, returns one row per active product field, and carries no `retention_class` column: the class is P5's and the service merges it from P5's contract (GAP-0481; ASM-0673). The `access_rows` JSON array is aggregated to keep the field grain; it holds only rows in force on the date in Asia/Bangkok, by the same rule the APP access check applies (BR7). Which business date applies is Pending, GAP-3443. Tests of AC2 and AC18 set the database clock of the test container. The array feeds no property of the published catalog entry beyond its field grain: the APP story returns `access` as capability area and right (RD-P1-005).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `V<seq>__rwb_p1_e1016_access_indexes.sql` | Migration | The three indexes on the existing tables |
| `V<seq>__rwb_p1_e1016_product_catalog_view.sql` | Migration | `v_data_product_catalog`, four P1 tables, no retention column |
| `V<seq>__rwb_p1_e1016_access_seed.sql` | Migration | The seven rows of version "DPA-2026.11" |
| `DictionaryConformanceCheck` | Pipeline check | Baseline IDs present; at least 123 objects and 1,379 fields; every later field has a `sys_field_version` row; every seeded product and role resolves |
| `SchemaBoundaryCheck` | Pipeline check | No constraint names `public` or another `rwb_*` schema; the view names only its own schema |
| `OwnershipCheck` | Pipeline check | The login owns `rwb_source_data` only; no table of this story's list is created here; no `masking_rule` object |

**Build steps**

1. The index migration with the three indexes and a catalog check of their names, uniqueness and column order (AC1).
2. The read-model migration with its four-table join, a check that no object outside the schema is named, and a fixture that adds a `retention_rule` column and fails (AC2).
3. The seed migration for DPA-2026.11, with a test that counts seven rows and asserts the absence of a DP06 row for RW-PHONECOL (AC3).
4. The `DictionaryConformanceCheck` on the at-least 123 and 1,379 baseline counts and on the seed, with a failing fixture for role RW-UNKNOWN (AC4).
5. The `SchemaBoundaryCheck` over the catalogue, with a fixture that adds a foreign key to another schema (AC5).
6. The `OwnershipCheck` with sessions as the login and as a no-grant role, and a check that the five E1001 tables are unchanged and that no `masking_rule` object exists in the schema (AC6, AC7).
7. A repeated-run test of the whole set on a copy of the SIT schema, and the release note with the three versions and checksums (AC7).

**Done when.** The migration set applies twice without a change, the three indexes exist with their columns, `v_data_product_catalog` returns one row per product field and names four P1 tables, DPA-2026.11 holds its seven rows including RW-COMPLY on DP02 and no RW-PHONECOL row on DP06, the conformance and schema checks pass, and the tests in section 16 pass.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| Conformance check 1 | The E1001 baseline migration or a baseline object / field ID is missing, or counts are below 123 objects or 1,379 fields | Dictionary conformance failed: {objectCount} objects and {fieldCount} fields; baseline requires all E1001 IDs and at least 123 objects and 1379 fields |
| Conformance check 2 | A seeded row names an unknown product or role | Seed check failed: {productCode} or {roleCode} is not in the published list |
| Schema check 1 | A constraint names `public` or another `rwb_*` schema | fk_data_product_access_product references another schema; no constraint in rwb_source_data may reference another schema |
| Schema check 2 | The read model names an object outside its schema or a retention column | v_data_product_catalog names {object}; the catalog read model reads its own schema only |
| Ownership check | The login owns another schema, or a table of the story exists twice | Ownership check failed: {login} owns {schema} |
| SQLSTATE 23505 | A second row for the same product, role and version | duplicate key value violates unique constraint |
| Role list check | The role list cannot be read | Role list unavailable: RWB-P4-E1037-CON |

The pipeline texts are for developers and are not part of the message standard. The application handler owns MSG-P1-002; this story's checks use their own log texts.

### 15. Screens and states

No screen is owned by this story. Migration output and checksums appear in the release pipeline and Flyway history. A data steward reads the catalog through `GET /admin/data-products` of RWB-P1-E1016-APP, never through SQL.

### 16. Test cases

Test Cases v9 holds the database cases cited below. TC-P1-E1016-APP-27, TC-P1-E1016-CON-27, TC-P1-E1016-APP-28 to TC-P1-E1016-APP-34 belong to the application and contract slices; they do not prove this database story's migration criteria.

| Criterion | Test reference | Data or assertion |
|---|---|---|
| AC1 to AC7, AC9 to AC19 | TC-P1-E1016-DB-16, TC-E1-016-19 to TC-E1-016-22, TC-P1-E1016-DB-01, TC-P1-E1016-DB-04 to TC-P1-E1016-DB-15 | The Gherkin scenario under the matching criterion in section 7 |
| BR1 to BR8 coverage review | Review checklist; no test case ID | Every business rule names a section 7 criterion and a v9 test reference, except BR8's migration checksum check which maps to AC9 |


### 17. Guardrails

- No business value in a constraint or a seed: the seven rows are the rows the sources give, the index columns follow the two reads, and every other value stays data in `data_product_access` and in rwb-access.
- No personal data in a migration, a script, a test fixture or a runbook: the seed holds product codes and role codes, the read model holds field names and tags, and the test keys P0000102 and DP01 are synthetic.
- No cross-schema read and no cross-schema key: the read model names four tables of `rwb_source_data`, no constraint names `public` or another `rwb_*` schema, and the retention class crosses P5's contract, not a join (DP-01).
- ACE data only through the owner's contract or the `recovery.v_ace_*` views: this story creates no ACE object and reads no ACE table (DP-05, ADR-010).
- One login per service: `rwb_source_data` owns its own schema and holds no grant on another (DP-02; Architecture v5 slide 29).
- Masking rows are never created or read here: `masking_rule`, `role` and `permission` are rwb-access's, and the role list reaches the pipeline through the published contract (DP-08; GAP-0481; ASM-0673).
- This story creates no table: E1001 owns the five baseline tables and E1069-DB owns the four extension tables (GAP-0484; ASM-0676).
- An applied migration is never edited: a correction is a new version, and a wrong index is dropped by a later version, never by an edit.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | Rules | Test cases |
|---|---|---|---|---|---|
| REQ-RDF-010 | Access per data product by role through the views; personal data masked by role under PDPA | Business Requirements Epic 1, sections 3.1 and 4 | FEAT-RDF-15 | CTL-09, CTL-11; DL26; BR-P1-015-2; BR-P1-015-3 | TC-P1-E1016-DB-16, TC-E1-016-19 to TC-E1-016-22, TC-P1-E1016-DB-01, TC-P1-E1016-DB-04 to TC-P1-E1016-DB-15; legacy regression TC-P1-E1016-APP-27, TC-P1-E1016-APP-28, TC-P1-E1016-APP-31, TC-P1-E1016-APP-33 |
| REQ-RDF-011 | Catalog entry per data product with definition, owner, system of record, refresh and retention | Business Requirements Epic 1, sections 3.1 and 4 | FEAT-RDF-16 | CTL-08; BR-P1-002-2; BR-P1-016-2 | TC-P1-E1016-DB-16, TC-E1-016-19 to TC-E1-016-22, TC-P1-E1016-DB-01, TC-P1-E1016-DB-04 to TC-P1-E1016-DB-15; legacy regression TC-P1-E1016-CON-27 |
| REQ-ACA-006 | Every read of personal data is logged, and a read that cannot be logged is refused | Business Requirements Epic 1, sections 3.1 and 4 | FEAT-RDF-15 | CTL-11; BR-P1-015-4 | TC-P1-E1016-DB-16, TC-E1-016-19 to TC-E1-016-22, TC-P1-E1016-DB-01, TC-P1-E1016-DB-04 to TC-P1-E1016-DB-15 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-P1-E1001-APP | App development | Creates the five tables, the 14 product rows and the dictionary this story indexes, views and seeds |
| RWB-P1-E1016-APP | App development | Reads these objects through the two operations and applies the masking answer; writes no index, view or seed row |
| RWB-P1-E1016-CON | Contract | Sibling of the same legacy key: the catalog entry schema this read model fills |
| RWB-P1-E1069-DB | ACE DB | The four extension tables and the grants on the 30 views |
| RWB-P1-E1069-APP | App development | The view SQL that the login reads and the schema check names |
| RWB-P4-E1037-CON | Contract | The role list and the masking answer; this story reads neither table |
| RWB-P4-E1016-APP | App development | Answers `GET /admin/roles`, which the conformance check reads through its published fake |
| RWB-P5 (rwb-document) | Service | Owns the retention class the catalog entry carries; no join is created here |
| RWB-PLT-E1044-CON | Contract | The per-service Flyway sequence and its version allocation |

### 19. Out of scope

- The five tables, the 14 product rows and the 123 object / 1,379 field baseline: RWB-P1-E1001-APP.
- The two read operations, the access check and the catalog service: RWB-P1-E1016-APP.
- The contract document and the read schemas: RWB-P1-E1016-CON.
- The role to permission matrix, the masking rows and the role list: rwb-access (P4); this story creates none and reads none.
- The retention rule, its values and its class code: rwb-document (P5); only the class crosses the contract.
- The four extension tables and the grants on the 30 views: RWB-P1-E1069-DB, with the view SQL in RWB-P1-E1069-APP.
- The rest of the `data_product_access` seed beyond the seven rows the sources give: a later approved load through the reference-data contract (GAP-0482; ASM-0674).
- The validation check of the access load at the application layer: RWB-P1-E1016-APP; this story supplies the table and the unique key.
- Performance tuning beyond the three indexes: the non-functional work.
- The source-data v2 folder contains this DB story and no E1016 OPS story; deployment remains in the service release pipeline.

### 20. Remaining delivery steps

- Size: Not specified; owner P1 delivery lead.
- EP01 design sign-off: Pending; owner product owner.
- RWB-P1-E1016-CON Done: Pending; owner contract owner.
- Role-list fake version: Pending; owner rwb-access service owner, GAP-0983.
- Pipeline identity and permission for the role-list call: Pending; owner rwb-access owner, GAP-3447.
- `v_data_product_catalog` in the Physical Schema view script: Pending; owner data architect (REQUEST).
- Width of `sys_objects.data_product` (GAP-3448) and the business date of the in-force test (GAP-3443): Pending; owners data architect and solution architect.
- Test data in DEV: Pending; owner QA lead.
- Whether the catalog filters data products by `valid_from`: Pending, owner data architect, GAP-3440.
- Next Flyway sequence numbers: Pending; owner platform release operator.
- Remaining access-matrix rows: Pending; owner data steward, GAP-0482 / ASM-0674.
- Section B view tests run in DEV and the pipeline; the related read feature stays off until RWB-ACE-001, owner ACE team (RD-P1-043).
