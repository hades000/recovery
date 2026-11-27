# RWB-P1-E1016-DB Access control per data product and catalog entries - ACE DB

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

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
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v1.md (FR-P1-004, FR-P1-006, FR-P1-012, FR-P1-013, FR-P1-024, FR-P1-025, FR-P1-026, FR-P1-027, FR-P1-030) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-016 for the ACE database work of rwb-source-data. RWB-P1-E1001-APP already creates `data_product`, `data_product_access`, `sys_objects`, `sys_fields` and `sys_field_version` in schema `rwb_source_data` with its own migration, so this story delivers the database slice that is still missing: the three indexes the access check and the catalog read need, the read model `v_data_product_catalog`, the seed of `data_product_access` version "DPA-2026.11" with the rows the sources give, the 122/1,366 dictionary conformance check and the schema checks; it creates no table and holds no masking row (DP-01, DP-02, DP-15; Architecture v5 slides 29 and 41). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P1-E1016-DB). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As an **ACE database engineer**, I want **the three indexes on `data_product_access`, `sys_fields` and `sys_objects` that the access check and the catalog read need, the read model `v_data_product_catalog` that joins the dictionary to the product and its access rows without naming another service's table, the seed of `data_product_access` version "DPA-2026.11" for the roles and products the sources give, the 122 object and 1,366 field conformance check that fails the build on a mismatch, and the schema checks that prove no constraint names `public` or another `rwb_*` schema and the login owns `rwb_source_data` only**, so that **a role's access row is found by an index instead of a scan, the catalog entry is one read model instead of four joins in code, and the access version in force is a database fact that a pipeline test can prove**.

This is the database slice of legacy RWB-E1-016 for rwb-source-data. It delivers:

- the three indexes: `ix_data_product_access_product_role` on `data_product_access(product_code, role_code, valid_from)`, `ix_sys_fields_object_field` on `sys_fields(object_name, field_name)` and `ix_sys_objects_product` on `sys_objects(data_product)`;
- the read model `v_data_product_catalog`, one row per product field, joining `sys_fields`, `sys_objects` and `data_product`, with the access block from `data_product_access` in force, and with the retention class left to the service because it is P5's and is read through P5's contract, not by SQL;
- the seed of `data_product_access` version "DPA-2026.11": RW-CASEOWN and RW-AUDIT read DP02; RW-PHONECOL reads DP01, DP02, DP03 and DP05 and has no row for DP06;
- the 122/1,366 dictionary conformance check, extended to the seed: every seeded product and every seeded role resolves;
- the schema checks: no constraint names `public` or another `rwb_*` schema, and the login owns `rwb_source_data` only;
- the migration set on rwb-source-data's per-service Flyway sequence, with a repeated run that changes nothing (DP-15).

It creates no table: `data_product`, `data_product_access`, `sys_objects`, `sys_fields` and `sys_field_version` are RWB-P1-E1001-APP's, and the four extension tables are RWB-P1-E1069-DB's (slice-boundary gap: GAP-0484; ASM-0676). It does not own `masking_rule` and does not create it, and it reads no masking row by SQL (GAP-0481; ASM-0673). It writes no application code and no REST operation.

### 2. Business rationale

The legacy story proved access control with one schema, one role model and one guard in the same process. In the target the same controls work across 19 schemas and 19 logins, where ownership is enforced by grants and not by separate servers (Architecture v5 slide 29). Two of the controls become cheaper and one becomes testable. Cheaper: the access check and the catalog read are the two hottest reads of the capability, and neither had a supporting index when the estate was one schema with one planner and one set of statistics. Testable: the access version in force is a row with a valid-from date, so a pipeline check can assert exactly which roles read which product on which date, instead of reading a configuration file.

The read model is the second reason. The catalog entry joins four P1 tables, and the fifth thing it shows, the retention class, belongs to rwb-document (Ownership Map v1: `retention_rule` to P5). A join to `rwb_document.retention_rule` would be a cross-schema read the boundary rule forbids, so the model stops at P1's four tables and the service merges P5's answer (DP-01; GAP-0481; ASM-0673).

Serves REQ-RDF-010 (access per data product by role) and REQ-RDF-011 (one catalog entry per data product). The business value is not restated here: this story adds none, it makes the two reads of the app story exact and fast.

### 3. Preconditions

- The per-service Flyway sequence of rwb-source-data exists with its own history table in schema `rwb_source_data`, and the baseline has been applied on it (DP-15; RWB-PLT-E1044-CON).
- RWB-P1-E1001-APP is done: `data_product` with the 14 rows DP01 to DP14, `data_product_access`, `sys_objects` with its 122 rows, `sys_fields` with its 1,366 rows, `sys_field_version` and `data_contract` exist in `rwb_source_data`, and the read model `v_data_dictionary` is in place.
- RWB-P1-E1069-APP and RWB-P1-E1069-DB are done or in flight: the 30 `recovery.v_ace_*` views exist and the login holds SELECT on each of them, so AC8 of the legacy story can run.
- The login `rwb_source_data` exists in DEV and SIT, owns schema `rwb_source_data` and no other schema, and holds no privilege in `public` (DP-02; Architecture v5 slides 11 and 29).
- The role list and the product list are data: role codes come from rwb-access's role list and product codes from `data_product`. This story writes neither and validates the seed against both, the role list through the published contract (DP-07, DP-08).
- The complete `data_product_access` seed is not given by the sources: only the six rows of section 11 are specified, and the rest is Not specified in the source documents (GAP-0482; ASM-0674).
- No approval is required to run a Draft migration on a development database; the migration is released to SIT only after the tests in section 16 pass.

### 4. Flow

1. The ACE database engineer checks out the rwb-source-data migration folder and confirms the highest applied version on the service sequence (RWB-P1-E1001-APP's baseline and its dictionary migration).
2. The engineer writes the index migration: the three indexes of section 13, on the tables RWB-P1-E1001-APP created, with `CREATE INDEX IF NOT EXISTS` semantics on the service sequence and no change to any column.
3. The engineer writes the read-model migration: `v_data_product_catalog`, one row per product field, joining `sys_fields` to `sys_objects` to `data_product`, with the access block read from `data_product_access` where the version is in force; the view names no table outside `rwb_source_data` and carries no `retention_rule` column.
4. The engineer writes the seed migration for version "DPA-2026.11": the six rows of section 11, each with its product code, role code, `can_read` true, the version label, the valid-from date and a null valid-to date; no row for DP06 and no other role or product.
5. The pipeline applies the three migrations in order on the service sequence, first to an empty schema and then to a copy of the SIT schema.
6. The pipeline runs the dictionary conformance check: `v_data_dictionary` returns 122 objects and 1,366 fields, and every seeded `product_code` has one `data_product` row and every seeded `role_code` appears in the rwb-access role list of the published fake.
7. The pipeline runs the schema checks: no constraint of `rwb_source_data` names `public` or another `rwb_*` schema, the login owns `rwb_source_data` only, and no migration of this story creates a table RWB-P1-E1001-APP already creates.
8. The pipeline runs the seed check in a transaction it rolls back: the version in force on 2026-11-20 holds exactly the six rows, a seventh row for DP06 as RW-PHONECOL does not exist, and the catalog read returns 14 products.
9. The engineer records each migration in the release notes of the sequence with its version number and its checksum.

### 5. Exception paths

| ID | Trigger | What happens | Message |
|---|---|---|---|
| X1 | An index migration runs before the table it indexes exists | The statement fails on the missing relation and the stage stops; no index is recorded | Pipeline error, no message id |
| X2 | A migration of this story tries to create a table RWB-P1-E1001-APP already creates | The check fails the build and names the table and the owning story; no table is created | Pipeline error, no message id |
| X3 | The read model names a table outside `rwb_source_data`, or a `retention_rule` column | The schema check fails the build and names the view and the object | Check finding, no message id |
| X4 | A seeded row names a product code with no `data_product` row, or a role code outside the rwb-access role list | The conformance check fails the build and names the row | MSG-P1-002, raised by the application load path, not by the migration |
| X5 | A second row is written for the same product, role and version | The unique key of `data_product_access` refuses it with SQLSTATE 23505 and the first row is unchanged | SQLSTATE 23505 duplicate key value violates unique constraint |
| X6 | A constraint of `rwb_source_data` names `public` or another `rwb_*` schema | The schema check fails the build and names the constraint and the referenced object | Check finding, no message id |
| X7 | The login owns a schema other than `rwb_source_data` | The schema check fails the build and names the login and the schema | Check finding, no message id |
| X8 | A migration is applied a second time | Flyway reports the version as already applied; no index, row or view changes | None |

X5 and X6 are the legacy paths of RWB-E1-016 carried onto the split; X1 to X4, X7 and X8 are the paths the slice boundary and the per-service sequence add.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Three migrations on the service's own sequence, on tables another P1 story already created; nothing to build against and no application code |
| Negotiable | Index names follow the platform naming library; the three column sets are fixed by the access check and the two catalog reads |
| Valuable | The access row is found by an index, the catalog entry is one read model, and the version in force is a testable database fact |
| Estimable | Three indexes, one view, six seed rows and three pipeline checks |
| Small | Days, not weeks, with the catalogue checks |
| Testable | Every criterion in section 7 is one catalogue query, one pipeline run, or one rolled-back write |

### 7. Acceptance criteria

```gherkin
Feature: The indexes, the catalog read model and the access seed of rwb-source-data

  Background:
    Given schema rwb_source_data is at the baseline of RWB-P1-E1001-APP with data_product, data_product_access, sys_objects, sys_fields and sys_field_version
    Given the login rwb_source_data owns schema rwb_source_data and no other schema
    Given the rwb-access role list is the published list of the authorise contract

  Scenario: AC1 The three indexes exist with their columns (new, D-RCV-60)
    Given the index migration of this story is applied on the service sequence
    When the catalogue is queried for the indexes of schema rwb_source_data
    Then ix_data_product_access_product_role exists on data_product_access with the columns (product_code, role_code, valid_from) in that order
    Then ix_sys_fields_object_field exists on sys_fields with the columns (object_name, field_name) in that order
    Then ix_sys_objects_product exists on sys_objects with the column (data_product)
    Then no index of this story is unique and no index changes a column or a constraint
    Then the access check by product and role uses ix_data_product_access_product_role in the plan

  Scenario: AC2 The read model returns one row per product field (new, D-RCV-60)
    Given the read-model migration is applied
    When v_data_product_catalog is queried for product DP01
    Then one row is returned per DP01 field of sys_fields, with object_name, field_name, field_id, data_type, is_personal and source_field
    Then each row carries product_code DP01, product_name, owner_role, system_of_record "ACE (ingested from ALS)" and refresh_cycle "DAILY"
    Then each row carries the access block: the role codes of data_product_access in force for DP01 with can_read, access_version and valid_from
    Then the view names sys_fields, sys_objects, data_product and data_product_access and no other table
    Then the view carries no retention_class column, and the retention class is merged by the service from the P5 contract

  Scenario: AC3 The DPA-2026.11 seed holds the six given rows and no DP06 row (new, D-RCV-60)
    Given the seed migration is applied
    When data_product_access is queried for access_version "DPA-2026.11"
    Then RW-CASEOWN holds one row for DP02 with can_read true
    Then RW-AUDIT holds one row for DP02 with can_read true
    Then RW-PHONECOL holds one row each for DP01, DP02, DP03 and DP05 with can_read true
    Then RW-PHONECOL holds no row for DP06 and no row of the version names a product outside DP01 to DP14
    Then the version holds six rows in all and each row names the version, a valid-from date and a null valid-to date
    Then the rest of the seed is not written, because it is not specified, and the later load is a separate change

  Scenario: AC4 The dictionary conformance check returns 122 objects and 1,366 fields (new, D-RCV-60)
    Given the baseline and this story's migrations are applied in SIT
    When the pipeline runs the conformance check
    Then v_data_dictionary returns 122 objects and 1,366 fields, of which 304 are view fields with source system "ACE"
    Then every seeded product_code has one data_product row
    Then every seeded role_code appears in the rwb-access role list
    When a branch seeds a row for role "RW-UNKNOWN" on DP02
    Then the check fails and names the row and the role

  Scenario: AC5 No constraint names public or another rwb_* schema (new, D-RCV-60)
    Given the applied schema rwb_source_data
    When the catalogue is queried for every constraint of the schema
    Then no foreign key, check, unique or exclusion constraint names a table, a type or a schema outside rwb_source_data
    Then no constraint names public.account or any other table in schema public
    Then the only foreign keys of the schema are the ones inside rwb_source_data, including sys_objects to data_product
    When a branch adds a foreign key from data_product_access.product_code to another service's table
    Then the check fails and names the constraint
    Then the merge is blocked

  Scenario: AC6 The login owns rwb_source_data only and holds no privilege outside it (new, D-RCV-60)
    Given the login rwb_source_data and the 19 service logins of the platform DB story
    When the catalogue is queried for the login's schema ownership and memberships
    Then the login owns rwb_source_data and owns no other schema
    Then it holds no grant on any other rwb_* schema and no USAGE on schema public
    Then it holds USAGE on schema recovery and SELECT on each of the 30 views
    Then no credential and no password appears in a migration, a script or a runbook

  Scenario: AC7 The slice boundary holds, the migration repeats and no masking row is created (new, D-RCV-60)
    Given RWB-P1-E1001-APP has created data_product, data_product_access, sys_objects, sys_fields and sys_field_version
    When this story's migration set is applied in order
    Then no migration creates, alters or drops any of those five tables and each is recorded once with its version and checksum
    Then a second run reports no pending migration and changes no index, no row and no view
    Then no migration creates, alters or reads masking_rule, role or permission
    Then the story adds no table of its own and its object count is three indexes, one view and six seed rows
```

These seven criteria are new and prove only the database artefacts in the story title: the indexes, the read model, the seed and the checks. No legacy acceptance criterion text is repeated here. The legacy criteria these artefacts answer are AC1, AC3, AC5, AC6, AC8, AC10 and AC11 of RWB-E1-016 - the granted read, the denied read, the out-of-scope case, the no-rule answer, the role-not-yet-in-force refusal, the catalog counts and the "Workbench" refusal - and they are proven by RWB-P1-E1016-APP against this story's objects. AC2, AC4, AC7 and AC9 of the legacy story are the catalog entry, the load validation, the log failure and the grant test, owned by RWB-P1-E1016-APP and RWB-P1-E1016-CON. The slice boundary, the missing part of the seed and the masking ownership are recorded as GAP-0484, GAP-0482 and GAP-0481.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A role reads a data product only through a `data_product_access` row in force for that role and product | REQ-RDF-010; FEAT-RDF-15 |
| BR2 | The access row is found by product, role and valid-from date, and the index `ix_data_product_access_product_role` serves that lookup | FSD P1 A2.15; TSD P1 T6.3 |
| BR3 | Each data product has one catalog row per field, with the product, its system of record, its owner and its access rows; the retention class is P5's and arrives through P5's contract | REQ-RDF-011; Ownership Map v1 |
| BR4 | No constraint of `rwb_source_data` names `public` or another `rwb_*` schema; a link to an ACE record is a business key with no foreign key | D-RCV-35 U4; ADR-010; DP-01 |
| BR5 | One login per service: `rwb_source_data` owns its own schema and holds no grant on another | DP-02; Architecture v5 slide 29 |
| BR6 | Masking rows are rwb-access's: this story creates no `masking_rule` row and reads none by SQL | Ownership Map v1; DL26; DP-08 |
| BR7 | An access version is in force from its valid-from date; a row with a later date is not in force and the read is refused until that date | REQ-RDF-010; FSD P1 A2.15 |
| BR8 | An applied migration is never edited; a correction is a new version on the same sequence | DP-15; RWB-PLT-E1044-CON |

**Where each rule lives in the target.** BR1, BR2, BR3, BR4, BR5 and BR7 are this story's objects and checks: the seed, the index, the read model, the constraint scan and the ownership check. BR6 is the boundary this story must not cross: the masking rows stay in `rwb_access` and the app story reads the answer, so no column of `masking_rule` appears in the read model (GAP-0481; ASM-0673). BR8 is the rule of the per-service sequence, and the repeated-run criterion proves it.

### 9. State transitions

None in the runtime sense: a table has no state machine and this story changes no business row. The states this story moves through are the migration states of the service's Flyway history and the states of an access version.

| Item | States |
|---|---|
| a migration of this story | Pending, applied, failed, undone; an applied version is never edited |
| an access version | Seeded, in force from its valid-from date, superseded by a later version, never deleted |
| an access row | In force, or not yet in force because its valid-from date is later than the business date |
| the read model | Absent, created, replaced by a corrected view in a later version |
| the login | Present and owning its own schema, or absent and named by the preflight; never a member of another service's login role |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The ACE database engineer (any team, per U3) | Writes and runs the migration set and the checks |
| ACE team lead and ACE DBA | Own schema `public` and the database; approve index and view changes on the ACE server |
| Recovery tech lead and data architect | Approve a change to the column sets of the three indexes and to the read model |
| Recovery migration account | Applies this story's migrations in DEV and SIT |
| rwb-source-data owner (RWB-P1-E1016-APP) | Owns the two operations that read these objects; writes no index, no view and no seed row |
| rwb-access (P4) | Owns the role list and the masking rows; supplies the role list this story validates against |
| rwb-document (P5) | Owns the retention class the catalog entry carries; this story creates no retention column |
| RW-PLATADM, platform administrator | Reads the deployment result on SCR-44 Migration runs (Platform administration R); may not change an index |
| RW-AUDIT, internal audit | Reads the access rows and the seed version (Platform administration R) |
| RW-DATASTEW, data steward | Reads the catalog read model (Data product catalog R) |
| No approval level of the delegation of authority applies | A schema change is not a credit decision |

The login is `rwb_source_data` (Architecture v5 slides 11 and 29; DP-02). Its credential and rotation are held by the platform, and no credential appears in a migration, a script or a runbook.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-REF-080 | data_product_access | id | Seed (one row per product, role and version) |
| DF-REF-081 | data_product_access | product_code | Seed: DP02 for RW-CASEOWN and RW-AUDIT; DP01, DP02, DP03 and DP05 for RW-PHONECOL |
| DF-REF-082 | data_product_access | role_code | Seed: RW-CASEOWN, RW-AUDIT, RW-PHONECOL |
| DF-REF-083 | data_product_access | can_read | Seed: true on all six rows |
| DF-REF-084 | data_product_access | access_version | Seed: "DPA-2026.11" |
| DF-REF-085 | data_product_access | valid_from | Seed: 2026-11-20 |
| DF-REF-086 | data_product_access | valid_to | Seed: null |
| DF-REF-071, DF-REF-072, DF-REF-074, DF-REF-075, DF-REF-077, DF-REF-078 | data_product | product_code, product_name, system_of_record, owner_role, refresh_cycle, expected_by | Read by the read model; the rows are RWB-P1-E1001-APP's |
| DF-REF-088, DF-REF-091, DF-REF-092 | sys_objects | object_name, data_product, system_of_record | Read by the read model |
| DF-REF-095, DF-REF-097, DF-REF-098, DF-REF-103, DF-REF-104, DF-REF-105 | sys_fields | field_id, field_name, data_type, source_system, source_field, is_personal | Read by the read model |
| DF-REF-119 | retention_rule (P5) | record_class | **Not read here**: the class crosses P5's contract, not a join |

The six seed rows in full:

| product_code | role_code | can_read | access_version | valid_from | valid_to |
|---|---|---|---|---|---|
| DP02 | RW-CASEOWN | true | DPA-2026.11 | 2026-11-20 | null |
| DP02 | RW-AUDIT | true | DPA-2026.11 | 2026-11-20 | null |
| DP01 | RW-PHONECOL | true | DPA-2026.11 | 2026-11-20 | null |
| DP02 | RW-PHONECOL | true | DPA-2026.11 | 2026-11-20 | null |
| DP03 | RW-PHONECOL | true | DPA-2026.11 | 2026-11-20 | null |
| DP05 | RW-PHONECOL | true | DPA-2026.11 | 2026-11-20 | null |

No row for DP06 and no other role or product is seeded: the sources give these six rows only, and the rest of the version is Not specified in the source documents (GAP-0482; ASM-0674). The valid-from date 2026-11-20 is the date the legacy story's background uses for the version in force.

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
| data_product | rwb_source_data | P1 | **Not created here**: RWB-P1-E1001-APP created it; the read model reads its 14 rows |
| data_product_access | rwb_source_data | P1 | **Not created here**: RWB-P1-E1001-APP created it; this story adds `ix_data_product_access_product_role` and the six seed rows |
| sys_objects | rwb_source_data | P1 | **Not created here**: adds `ix_sys_objects_product`; the read model reads its 122 rows |
| sys_fields | rwb_source_data | P1 | **Not created here**: adds `ix_sys_fields_object_field`; the read model reads its 1,366 rows |
| sys_field_version | rwb_source_data | P1 | **Not touched here**: RWB-P1-E1001-APP created it and a later story writes it |
| data_contract | rwb_source_data | P1 | **Not touched here**: RWB-P1-E1001-APP created it |
| v_data_product_catalog | rwb_source_data | P1 | **Created here**: the read model of section 13, with no `retention_rule` column and no object outside the schema |
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
| earlier | from RWB-P1-E1001-APP | Schema `rwb_source_data`, its tables, the 14 product rows, the 122 and 1,366 dictionary rows and `v_data_dictionary` |
| next | `..._rwb_e1_016_product_access_indexes.sql` | The three indexes |
| next | `..._rwb_e1_016_product_catalog_view.sql` | `v_data_product_catalog` |
| next | `..._rwb_e1_016_product_access_seed.sql` | The six rows of version "DPA-2026.11" |

No monolith version number is reused and an applied migration is never edited (BR8).

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
       f.source_system, f.source_field, f.is_personal,
       a.role_code, a.can_read, a.access_version, a.valid_from, a.valid_to
  FROM rwb_source_data.data_product p
  JOIN rwb_source_data.sys_objects o ON o.data_product = p.product_code
  JOIN rwb_source_data.sys_fields f ON f.object_name = o.object_name
  LEFT JOIN rwb_source_data.data_product_access a
         ON a.product_code = p.product_code AND a.can_read
;
```

The view names four tables, all in `rwb_source_data`, and carries no `retention_class` column: the class is P5's and the service merges it from P5's contract (GAP-0481; ASM-0673). The "in force" filter is applied by the reading query on `valid_from` and `valid_to` against the business date, so the view stays a plain projection and the date is never a constant in the database.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `..._rwb_e1_016_product_access_indexes.sql` | Migration | The three indexes on the existing tables |
| `..._rwb_e1_016_product_catalog_view.sql` | Migration | `v_data_product_catalog`, four P1 tables, no retention column |
| `..._rwb_e1_016_product_access_seed.sql` | Migration | The six rows of version "DPA-2026.11" |
| `DictionaryConformanceCheck` | Pipeline check | 122 objects and 1,366 fields; every seeded product and role resolves |
| `SchemaBoundaryCheck` | Pipeline check | No constraint names `public` or another `rwb_*` schema; the view names only its own schema |
| `OwnershipCheck` | Pipeline check | The login owns `rwb_source_data` only; no table of this story's list is created here; no `masking_rule` object |

**Build steps**

1. The index migration with the three indexes and a plan check that the access lookup uses `ix_data_product_access_product_role` (AC1).
2. The read-model migration with its four-table join, a check that no object outside the schema is named, and a fixture that adds a `retention_rule` column and fails (AC2).
3. The seed migration for DPA-2026.11, with a test that counts six rows and asserts the absence of a DP06 row for RW-PHONECOL (AC3).
4. The `DictionaryConformanceCheck` on the 122 and 1,366 counts and on the seed, with a failing fixture for role RW-UNKNOWN (AC4).
5. The `SchemaBoundaryCheck` over the catalogue, with a fixture that adds a foreign key to another schema (AC5).
6. The `OwnershipCheck` with sessions as the login and as a no-grant role, and a check that the five E1001 tables are unchanged and that no `masking_rule` object exists in the schema (AC6, AC7).
7. A repeated-run test of the whole set on a copy of the SIT schema, and the release note with the three versions and checksums (AC7).

**Done when.** The migration set applies twice without a change, the three indexes exist with their columns, `v_data_product_catalog` returns one row per product field and names four P1 tables, DPA-2026.11 holds its six rows and no DP06 row, the conformance and schema checks pass, and the tests in section 16 pass.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| Conformance check 1 | The dictionary does not return 122 objects or 1,366 fields | Dictionary conformance failed: {objectCount} objects and {fieldCount} fields, expected 122 and 1366 |
| Conformance check 2 | A seeded row names an unknown product or role | Seed check failed: {productCode} or {roleCode} is not in the published list |
| Schema check 1 | A constraint names `public` or another `rwb_*` schema | fk_data_product_access_product references another schema; no constraint in rwb_source_data may reference another schema |
| Schema check 2 | The read model names an object outside its schema or a retention column | v_data_product_catalog names {object}; the catalog read model reads its own schema only |
| Ownership check | The login owns another schema, or a table of the story exists twice | Ownership check failed: {login} owns {schema} |
| SQLSTATE 23505 | A second row for the same product, role and version | duplicate key value violates unique constraint |
| MSG-P1-002 | The application load path refuses a version at a check | The {source} load for {date} was refused: {check}. The previous load is still in use. |

The pipeline texts are for developers and are not part of the message standard. No `MSG-` ID is new: MSG-P1-002 is raised by the application handler of RWB-P1-E1016-APP when a load reaches the database, and this story's checks use their own log texts.

### 15. Screens and states

No screen. The result of a migration is visible in the release pipeline and in the service's Flyway history, each version with its checksum. The platform administrator reads the deployment result under Platform administration R and on SCR-44 Interface and job monitor; the data steward reads the catalog read model through `GET /admin/data-products` of RWB-P1-E1016-APP and never through SQL on a screen. Nothing in this story is shown to a user directly.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-016-01 | AC1, AC3; regression evidence for the granted read of the legacy story | Component | RW-AUDIT; DP02 seed row; case RW-2026-000102; synthetic customer P0000102 |
| TC-E1-016-02 | AC2, AC4; regression evidence for the legacy catalog entry | Component | DP01; six views and account_ext; DF-ACE-018; access block of DP01 |
| TC-E1-016-03 | AC3, AC4; regression evidence for the legacy denied read | Component | RW-PHONECOL with no DP06 row; product DP06 |
| TC-E1-016-04 | AC4; regression evidence for the legacy load validation | Component | A seeded row for role RW-UNKNOWN on DP02 |
| TC-E1-016-05 | AC3, AC7; regression evidence for the legacy out-of-scope case | Component | RW-CASEOWN row on DP02; the app story's scope filter |
| TC-E1-016-06 | AC2, AC4; regression evidence for the legacy no-rule answer | Component | RW-COMPLY absent from the seed; no masking row created here |
| TC-E1-016-07 | AC7; regression evidence for the legacy log failure | Component | No database object of this story writes the PII access log |
| TC-E1-016-08 | AC3, AC7; regression evidence for the legacy row-not-yet-in-force | Component | A rolled-back DPA-2026.12 row with valid_from 2026-12-15; business date 2026-12-14 |
| TC-E1-016-09 | AC5, AC6; the refusals of the schema checks | Component | A catalog read for RW-TRIBE at the app layer; a foreign key to another schema at the database |
| TC-E1-016-10 | AC6, AC7; regression evidence for the legacy grant test | Component | The login rwb_source_data; SELECT on the 30 views; SELECT on public.account refused; all 30 views |
| TC-E1-016-11 | AC4; regression evidence for the legacy catalog counts | Component | 30 views; 122 objects and 1,366 fields |
| TC-E1-016-12 | AC2, AC5; regression evidence for the legacy "Workbench" refusal | Component | A sys_objects row setting v_ace_customer to Workbench |

This story owns no legacy acceptance criterion, so the twelve rows above are the legacy test cases of RWB-E1-016 listed as regression evidence: their IDs, their data and their order are kept character for character, and the Covers column names this story's own criteria only where the legacy case exercises the artefacts in this story's title - the seed, the read model, the indexes or a schema check. The legacy level "System" maps to "Component" and "Access" to "Component", because each case is proven at the object it exercises and not end to end. The legacy criteria themselves are owned by RWB-P1-E1016-APP and RWB-P1-E1016-CON. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in a constraint or a seed: the six rows are the rows the sources give, the index columns follow the two reads, and every other value stays data in `data_product_access` and in rwb-access.
- No personal data in a migration, a script, a test fixture or a runbook: the seed holds product codes and role codes, the read model holds field names and tags, and the test keys P0000102 and DP01 are synthetic.
- No cross-schema read and no cross-schema key: the read model names four tables of `rwb_source_data`, no constraint names `public` or another `rwb_*` schema, and the retention class crosses P5's contract, not a join (DP-01).
- ACE data only through the owner's contract or the `recovery.v_ace_*` views: this story creates no ACE object and reads no ACE table (DP-05, ADR-010).
- One login per service: `rwb_source_data` owns its own schema and holds no grant on another (DP-02; Architecture v5 slide 29).
- Masking rows are never created or read here: `masking_rule`, `role` and `permission` are rwb-access's, and the role list reaches the pipeline through the published contract (DP-08; GAP-0481; ASM-0673).
- This story creates no table: the five tables are RWB-P1-E1001-APP's and the four extension tables are RWB-P1-E1069-DB's (GAP-0484; ASM-0676).
- An applied migration is never edited: a correction is a new version, and a wrong index is dropped by a later version, never by an edit.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | Rules | Test cases |
|---|---|---|---|---|---|
| REQ-RDF-010 | Access per data product by role through the views; personal data masked by role under PDPA | Business Requirements Epic 1, sections 3.1 and 4 | FEAT-RDF-15 | CTL-09, CTL-11; DL26; BR-P1-015-2; BR-P1-015-3 | TC-E1-016-01, TC-E1-016-03, TC-E1-016-06, TC-E1-016-08, TC-E1-016-10 |
| REQ-RDF-011 | Catalog entry per data product with definition, owner, system of record, refresh and retention | Business Requirements Epic 1, sections 3.1 and 4 | FEAT-RDF-16 | CTL-08; BR-P1-002-2; BR-P1-016-2 | TC-E1-016-02, TC-E1-016-11, TC-E1-016-12 |
| REQ-ACA-006 | Every read of personal data is logged, and a read that cannot be logged is refused | Business Requirements Epic 1, sections 3.1 and 4 | FEAT-RDF-15 | CTL-11; BR-P1-015-4 | TC-E1-016-07 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-P1-E1001-APP | App development | Creates the five tables, the 14 product rows and the dictionary this story indexes, views and seeds |
| RWB-P1-E1016-APP | App development | Reads these objects through the two operations and applies the masking answer; writes no index, view or seed row |
| RWB-P1-E1016-CON | Contract | Sibling of the same legacy key: the catalog entry schema this read model fills |
| RWB-P1-E1069-DB | ACE DB | The four extension tables and the grants on the 30 views |
| RWB-P1-E1069-APP | App development | The view SQL that the login reads and the schema check names |
| RWB-P4-E1037-CON | Contract | The role list and the masking answer; this story reads neither table |
| RWB-P5 (rwb-document) | Service | Owns the retention class the catalog entry carries; no join is created here |
| RWB-PLT-E1044-CON | Contract | The per-service Flyway sequence and its version allocation |

### 19. Out of scope

- The five tables, the 14 product rows and the 1,366 dictionary rows: RWB-P1-E1001-APP.
- The two read operations, the access check and the catalog service: RWB-P1-E1016-APP.
- The contract document and the read schemas: RWB-P1-E1016-CON.
- The role to permission matrix, the masking rows and the role list: rwb-access (P4); this story creates none and reads none.
- The retention rule, its values and its class code: rwb-document (P5); only the class crosses the contract.
- The four extension tables and the grants on the 30 views: RWB-P1-E1069-DB, with the view SQL in RWB-P1-E1069-APP.
- The rest of the `data_product_access` seed beyond the six rows the sources give: a later approved load through the reference-data contract (GAP-0482; ASM-0674).
- The validation check of the access load at the application layer: RWB-P1-E1016-APP; this story supplies the table and the unique key.
- Performance tuning beyond the three indexes: the non-functional work.
- A separate OPS story for this legacy key: none is raised; the migration set deploys with the service pipeline.
