# RWB-P1-E1069-DB Read-only ACE source views, grants and boundary rule - ACE DB

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P1-E1069-DB |
| Work type | DB (ACE DB) |
| Suggested owner | ACE team (suggested; any team may pick up this story) |
| Service | rwb-source-data |
| Service epic | RWB-SVC-P1 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-069 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP02, DP03, DP05, DP06, DP07, DP08, DP11, DP15, DP19 |
| Parallel lane | L-P1-R |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-P1-E1069-DB-16) |
| Depends on (build) | None |
| Contract dependencies | None: this DB story publishes and consumes no API contract, so no contract story, no contract fake library version and no contract version apply |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v1.md (FR-P1-001, FR-P1-002, FR-P1-005) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-069 for the ACE database work of rwb-source-data. The single `recovery` schema of the monolith is replaced by one schema and one login per service (DP-01, DP-02; Architecture v5 slides 8, 9 and 29): the 30 `recovery.v_ace_*` views stay in schema `recovery`, owned by `ace_view_owner`, and only the `rwb_source_data` login holds SELECT on them; the four extension tables `party_ext`, `contact_point_ext`, `account_ext` and `valuation_ext` move with the service into schema `rwb_source_data`. The grant block of legacy section 12 is reused with the schema fixed to `recovery` and the service role renamed `rwb_source_data`. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P1-E1069-DB). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (17 resolved, 29 cross-document, 2 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As an **ACE database engineer**, I want **the `rwb_source_data` login of this service and the grants it holds, the view owner `ace_view_owner` with SELECT on the 21 Tier 1 and 14 Tier 2 ACE tables, SELECT on each of the 30 `recovery.v_ace_*` views and nothing of any kind in `public`, the four extension tables `party_ext`, `contact_point_ext`, `account_ext` and `valuation_ext` in schema `rwb_source_data` with their primary keys, their standard record columns, the `ck_contact_point_ext_type` check and their 49 field IDs, and a schema in which no constraint names `public` and every link to an ACE record is a `varchar(255)` business key with no foreign key**, so that **one copy of ACE source data serves the Workbench without a second copy, without a write path into ACE data, and with a catalog that refuses a breach instead of a review that hopes**.

This is the database slice of legacy RWB-E1-069. It delivers:

- the `rwb_source_data` login of this service, and the grant set it holds: USAGE on schema `recovery`, SELECT on each of the 30 views, one GRANT and one ALTER VIEW OWNER per view, no privilege in `public` and no write on a view (DP-02, DP-05);
- the view owner `ace_view_owner`: USAGE on schema `public` and SELECT on the 21 Tier 1 tables of section 11, SELECT on the 14 Tier 2 tables once RWB-ACE-001 lands, the ownership of the 30 views, and no DML;
- the four extension tables in schema `rwb_source_data`, with their columns, their primary keys, the `ck_contact_point_ext_type` check and the 49 field IDs `DF-EXT-001` to `DF-EXT-049`, including the stale flag and age in days of `valuation_ext` (`DF-EXT-041`, `DF-EXT-042`), which this service writes until an owning function is assigned, with the appraisal stale rule held as data: 365 days from the appraisal date to the business date;
- the schema privileges and the PUBLIC revokes;
- the schema checks: no constraint in `rwb_source_data` names `public`, and every ACE link is a `varchar(255)` business key with no foreign key;
- the migration set on rwb-source-data's per-service Flyway sequence (DP-15), with a repeated run that changes nothing.

It does not create, alter or own the view SQL, the conformance test or the read contract: those are RWB-P1-E1069-APP. It does not prove the grant matrix across the 19 logins: that is RWB-ITG-E1069-ITG. It writes no application code and no REST operation.

### 2. Business rationale

The legacy story proved the boundary against one schema: 30 SELECT-only views over the ACE tables, one view owner, one service role, boundary rule BND-6 and a conformance test in the pipeline. In the target the same objects must work across 19 schemas and 19 logins, where the ownership rule is enforced by grants and not by separate servers (Architecture v5 slide 29: "Ownership is enforced by grants, not by separate servers").

This story is the grant and ownership half of that proof. It fixes who may read the views (the `rwb_source_data` login of this service and no other), who owns them (`ace_view_owner`, which holds SELECT on the ACE tables they read and nothing else), and where the Workbench's own decisions about an ACE record live (the four extension tables, in the service's own schema, keyed by the ACE business key and holding no copy of an ACE column). Everything else follows from those three facts: a direct read of a `public` table fails at the database, a write on a view fails at the database, a second row for one ACE key fails on the primary key, and no service can reach another service's rows because each login is granted on its own schema only (DP-01, DP-02; Architecture v5 slides 8, 11, 29 and 45).

Serves REQ-RDF-002 (ACE source data read only through the views) and REQ-DRI-006 (no component calls a system of record directly). The measure is the one the legacy story set: 100 percent of pipeline runs in which every view compiles, every grant is as specified and the conformance test passes (FSD P1 A2.1.1). The business value is not restated here: this story adds no new one.

### 3. Preconditions

- The per-service Flyway sequence of rwb-source-data exists with its own history table in schema `rwb_source_data`, and the baseline version has been applied on it (DP-15; RWB-PLT-E1044-CON).
- The 19 `rwb_*` schemas and their logins are created in DEV and SIT by the platform DB story RWB-PLT-NF06-DB, with the names fixed in the Environment and Deployment Design; the login of this service is `rwb_source_data` (Architecture v5 slides 11 and 29). Where the login already exists, this story asserts it and issues the grants; where it does not, it is created once for this service and never a second time.
- The credential of the login and its rotation are held by the platform, and no credential appears in a migration, a script or a runbook. That the platform DB story rather than this story issues the credential is Not specified in the source documents (GAP-0568; ASM-0809).
- Schema `recovery` exists and holds the 30 `recovery.v_ace_*` views and the three helper functions `recovery.ace_to_date`, `recovery.ace_to_boolean` and `recovery.ace_mask_value`, created by RWB-P1-E1069-APP on the same sequence; the grant migrations of this story are applied after the views they grant on.
- The ACE schema in DEV and SIT is at the head that holds the 21 Tier 1 tables of section 11, among them `account`, `payment`, `customer` and `efs_action` (ACE Schema PostgreSQL v1.sql; legacy RWB-E1-069 §3).
- The recovery migration account holds the ACE DBA role for the release window, so it can grant on schema `public`, create a role and set a view owner (RWB-E1-044; legacy RWB-E1-069 §3).
- The four extension tables are taken verbatim from Physical Schema v7 (legacy RWB-E1-069 §13) with the field IDs of TSD P1 T3.5: `DF-EXT-001` to `DF-EXT-012` on `party_ext`, `DF-EXT-013` to `DF-EXT-026` on `contact_point_ext`, `DF-EXT-027` to `DF-EXT-035` on `account_ext` and `DF-EXT-036` to `DF-EXT-049` on `valuation_ext`.
- The 30-view list is frozen in the ACE Data Tier Map v1 and in `recovery_views.sql`; this story grants on those 30 names and on no other object (legacy RWB-E1-069 §13).
- For the 14 Tier 2 tables only: RWB-ACE-001 is deployed in DEV and SIT (DL43), and its migration grants SELECT on those tables to `ace_view_owner`; until then the Tier 2 grant of this story is not applied and the Section B views stay behind their flags. The batch-status freshness source (`v_ace_batch_status`) stays behind its flag with the Section B views; the fallback freshness source (CG-9) is confirmed before system test.
- No approval is required to run a Draft migration on a development database; the migration is released to SIT only after the tests in section 16 pass.

### 4. Flow

1. The ACE database engineer checks out the rwb-source-data migration folder and confirms the highest applied version on the service sequence (the baseline).
2. The engineer writes the first migration: the four extension tables, copied from Physical Schema v7 with their primary keys, their standard record columns and the `ck_contact_point_ext_type` check (BR7).
3. The engineer writes the Section A grant migration, run as the ACE schema owner: USAGE on schema `public` and SELECT on the 21 Tier 1 tables for `ace_view_owner`, one ALTER VIEW OWNER statement per view, USAGE on schema `recovery` and one SELECT grant per view for `rwb_source_data`, and the PUBLIC revoke (legacy RWB-E1-069 §12).
4. The engineer writes the Section B grant migration: SELECT on the 14 Tier 2 tables for `ace_view_owner`, one ALTER VIEW OWNER statement per Section B view, one SELECT grant per view for `rwb_source_data`; it is applied only after RWB-ACE-001 is reported deployed (BR9).
5. The engineer writes the schema checks of the pipeline: no constraint in `rwb_source_data` names `public`, every ACE link column is a `varchar(255)` business key with no foreign key, and the login holds no privilege outside its own schema and schema `recovery`.
6. The migration pipeline applies the baseline, this story's migrations and the two view migrations of RWB-P1-E1069-APP in the fixed order on the sequence, first to an empty schema and then to a copy of the SIT schema.
7. The pipeline runs the grant checks: a session as `rwb_source_data` selects one row from each of the 30 views, is refused on `public.account` with SQLSTATE 42501, and is refused on insert, update and delete on a view; a session as `ace_view_owner` is checked for ownership and for SELECT only; the test role `rwb_no_grant` is refused on a view.
8. The pipeline runs the duplicate-key test in a transaction it rolls back, and records the result; a repeated run of any migration changes nothing.
9. The engineer records each migration in the release notes of the sequence, with its version number and its checksum.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A grant migration runs before the view migration it grants on | The statement fails on the missing relation and the stage stops; no grant is recorded | Pipeline error, no message id | AC8 |
| X2 | The login `rwb_source_data` does not exist when the grant runs | The statement fails on the missing role; the login is created once for this service, by this story's migration or by the platform DB story, and the grant is re-run | Database error, no message id | AC1 |
| X3 | The login holds a privilege in `public`, or a write on a view | The grant check fails the build and names the privilege and the object | recovery_svc holds SELECT on public.account; the recovery role reads the views only | AC2, AC3 |
| X4 | A constraint in `rwb_source_data` names a table in `public` | The schema check fails the build and names the constraint | fk_case_account_account_key references public.account; no constraint in recovery may reference another schema | AC7 |
| X5 | An ACE link column is not `varchar(255)`, or carries a foreign key | The schema check fails the build and names the column | Check finding, no message id | AC7 |
| X6 | A second row is written for an ACE key already in an extension table | The write is refused; the first row is unchanged | SQLSTATE 23505 duplicate key value violates unique constraint party_ext_pkey | AC6 |
| X7 | An extension table already exists in the sequence | The repeatable check refuses to create it twice and the migration is marked as already applied | Pipeline error, no message id | AC8 |
| X8 | A migration is applied a second time | Flyway reports the version as already applied; no object, row or grant changes | None | AC8 |

X3, X4 and X6 are the legacy exception paths X5, X3 and X7 of RWB-E1-069 carried onto the split, with the role renamed and the schema named `rwb_source_data`; X1, X2, X5, X7 and X8 are the paths the per-service sequence and the 19-login split add.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | One migration for the four tables and two grant migrations, on the service's own sequence; nothing to build against and no application code |
| Negotiable | Constraint and index names follow the platform naming library; the column set, the primary keys, the check and the grant list are fixed by the legacy story and the TSD |
| Valuable | The read path of 19 services is granted from one place, and the Workbench's own decisions about an ACE record have a schema that cannot write to ACE |
| Estimable | Four tables, one check, two grant migrations, one PUBLIC revoke and five schema checks |
| Small | Days, not weeks, with the catalogue checks |
| Testable | Every criterion in section 7 is one catalogue query, one refused statement with its SQLSTATE, or one pipeline run |

### 7. Acceptance criteria

```gherkin
Feature: The login, the grants and the four extension tables of rwb-source-data

  Background:
    Given the ACE schema in DEV holds the 21 Tier 1 tables of section 11, among them public.account, public.payment, public.customer and public.efs_action
    Given schema recovery holds the 30 v_ace_* views and the three helper functions, created by RWB-P1-E1069-APP
    Given schema rwb_source_data exists on the per-service Flyway baseline (DP-15)

  Scenario: AC1 The rwb_source_data login exists and holds its own schema only (new, D-RCV-60)
    Given the login "rwb_source_data" of this service and the other 18 service logins of the platform DB story
    When the catalogue is queried for the login's memberships and schema ownership
    Then the login exists in DEV and SIT and is a member of no other service's login role
    Then it owns schema rwb_source_data and owns no other schema
    Then it holds USAGE on schema recovery, and no USAGE on schema public
    Then it holds no grant on any other rwb_* schema
    Then no credential and no password appears in a migration, a script or a runbook

  Scenario: AC2 The login reads each of the 30 views and is refused on public.account (new, D-RCV-60)
    Given the 30 recovery.v_ace_* views and the SELECT grant on each of them
    When a session as "rwb_source_data" selects one row from each of the 30 views
    Then each of the 30 statements returns without error
    When the same session selects from public.account
    Then the statement fails with SQLSTATE 42501 "permission denied for schema public"
    Then has_schema_privilege('rwb_source_data', 'public', 'USAGE') is false
    Then has_table_privilege('rwb_source_data', 'public.account', 'SELECT') is false
    Then a test role "rwb_no_grant" cannot select recovery.v_ace_account, because PUBLIC holds no privilege on it

  Scenario: AC3 The login holds no write on any view (new, D-RCV-60)
    Given the SELECT grant on the 30 views
    When the session runs insert, update and delete on recovery.v_ace_account
    Then each statement fails with SQLSTATE 42501 and no row of any view changes
    Then no INSERT, UPDATE, DELETE or TRUNCATE privilege appears for the login on any of the 30 views
    Then the migration grants one view at a time and holds no "GRANT SELECT ON ALL TABLES IN SCHEMA recovery"
    Then "REVOKE ALL ON ALL TABLES IN SCHEMA recovery FROM PUBLIC" is in the migration and PUBLIC holds nothing on any of the 30 views

  Scenario: AC4 ace_view_owner owns the views and holds SELECT on the ACE tables only (new, D-RCV-60)
    Given the 21 Tier 1 tables of section 11 and, after RWB-ACE-001, the 14 Tier 2 tables
    When the catalogue is queried for the view owner
    Then "ace_view_owner" owns each of the 30 views, through one ALTER VIEW OWNER statement per view
    Then it holds USAGE on schema public and SELECT on the 21 Tier 1 tables named in section 11
    Then it holds SELECT on the 14 Tier 2 tables once RWB-ACE-001 is applied
    Then it holds no INSERT, UPDATE or DELETE on any of those tables
    Then it holds no right in schema recovery other than the views it owns

  Scenario: AC5 The four extension tables exist with their keys, the contact-type check and 49 columns (new, D-RCV-60)
    Given schema rwb_source_data at the migration that creates the four extension tables
    When the pipeline lists the four tables and their columns
    Then party_ext holds 12 columns with person_key as its primary key
    Then contact_point_ext holds 14 columns with contact_key as its primary key and the check ck_contact_point_ext_type that contact_type is PHONE, EMAIL or ADDRESS
    Then account_ext holds 9 columns with account_key as its primary key
    Then valuation_ext holds 14 columns with valuation_key as its primary key
    Then the four tables hold 49 columns in all and 49 dictionary fields, DF-EXT-001 to DF-EXT-049
    Then each of the four tables carries is_active, state, version, created_at, created_by, updated_at and updated_by

  Scenario: AC6 A duplicate ACE business key is refused with SQLSTATE 23505 (new, D-RCV-60)
    Given one row in party_ext for person_key "P0000123" and one row in account_ext for account_key "ACC0000017"
    When a second party_ext row is written for person_key "P0000123" inside a transaction
    Then the write fails with SQLSTATE 23505 and the message names party_ext_pkey
    Then party_ext holds one row for "P0000123"
    When a second row is written for the same contact_key and the same valuation_key
    Then each write fails with SQLSTATE 23505 and each table holds one row for that key
    Then the transaction is rolled back and no row of the test survives

  Scenario: AC7 No constraint names public and every ACE link is a business key (new, D-RCV-60)
    Given the applied schema rwb_source_data
    When the catalogue is queried for every constraint of the schema
    Then no foreign key, check, unique or exclusion constraint names a table, a type or a schema outside rwb_source_data
    Then no foreign key of the schema names public.account or any other table in schema public
    Then person_key, contact_key, account_key and valuation_key are varchar(255) columns with no foreign key
    When a branch adds a foreign key from account_ext.account_key to public.account
    Then the pipeline check fails and names the constraint and public.account
    Then the merge is blocked

  Scenario: AC8 The migration set is the per-service sequence and a repeated run changes nothing (new, D-RCV-60)
    Given the service's own Flyway sequence after the baseline
    When the migration set of this story is applied in order
    Then each migration is recorded once in the service's Flyway history with its version and checksum
    Then a second run reports no pending migration and changes no object, no row and no grant
    Then no file carries a "${recoverySchema}" token or an environment name: the schema is the fixed recovery
    Then a repeated GRANT changes nothing and a repeated REVOKE changes nothing
    Then no monolith migration name is reused on the sequence
```

These eight criteria are new and prove only the database artefacts in the story title: the login, the grants, the view owner, the four extension tables and the schema boundary. No legacy acceptance criterion text is repeated here. The legacy criteria these grants and tables answer are AC1, AC2, AC3, AC4 and AC7 of RWB-E1-069 — the view sets and their compilation, the read-only role, the constraint rule and the four extension tables — and they are proven end to end across the 19 real logins in RWB-ITG-E1069-ITG; AC5, AC6 and AC8 of the legacy story are the dictionary, the delay-day mapping and the build rule, and they belong to RWB-P1-E1069-APP.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The recovery module reads ACE source data only through the 30 SELECT-only `recovery.v_ace_*` views: 16 now over tables ACE holds, 14 when RWB-ACE-001 lands. It loads, copies and transforms nothing | D-RCV-35 U1, U4; ADR-010 |
| BR2 | A view is owned by `ace_view_owner`, which holds SELECT on the ACE tables it reads and writes nothing. It holds no right in schema `recovery` other than the views it owns | D-RCV-35 U4; CTL-02 |
| BR3 | On ACE source data the `rwb_source_data` login holds SELECT on the views and no privilege of any kind in `public`; PUBLIC holds nothing; no INSERT, UPDATE, DELETE or TRUNCATE is granted on a view. Its DML on the Workbench's own tables is granted by V0001 and is outside this story | D-RCV-35 U4; BR-P1-001-4; CTL-02 |
| BR4 | No constraint in schema `rwb_source_data` or schema `recovery` references a table or a type outside it. A link to an ACE record is a `varchar(255)` business-key column with no foreign key, because ACE cascades deletes on `account` | D-RCV-35 U4; BR-P1-001-3; ADR-010 |
| BR5 | Every view carries one `sys_objects` row and one `sys_fields` row per column, with the ACE source field and the data product | BR-P1-001; RWB-E1-064 |
| BR6 | A text date in ACE becomes a date through `recovery.ace_to_date`, and a Y/N flag becomes a boolean through `recovery.ace_to_boolean`; both return NULL rather than fail a read | BR-P1-001-7 |
| BR7 | An extension table holds a Workbench decision about an ACE record and never a copy of an ACE column. It is 1:1 with the ACE record on the ACE business key and carries the seven standard record columns | BR-P1-001-5 |
| BR8 | Boundary rule BND-6: no recovery class names a table in schema `public`; the only source objects it may name are the 30 `recovery.v_ace_*` views, read from the module map | REQ-DRI-006; RWB-TE-001 |
| BR9 | A Section B object is created only after its ACE table exists. Until then the feature that reads it stays behind its flag, and the Section B grant is a later Flyway version | ADR-010; DL43 |

**Rule coverage.** BR1 is covered by AC2 and TC-E1-069-02; BR2 by AC4 and TC-E1-069-02; BR3 by AC2, AC3 and TC-E1-069-02; BR4 by AC7 with TC-E1-069-04 and TC-E1-069-08; BR7 by AC5 and AC6 with TC-E1-069-05 and TC-E1-069-07; BR9 by AC4 with TC-E1-069-03. BR5, BR6 and BR8 have no criterion in this story: BR5 is asserted here and delivered in RWB-P1-E1001-APP, BR6 is delivered in RWB-P1-E1069-APP, and BR8 is a build rule of RWB-P1-E1069-APP.

**Where each rule lives in the target.** BR2, BR3 and BR7 are this story's: the ownership, the grant set and the four tables are the objects it creates and the statements it runs, and the login of BR3 is the `rwb_source_data` login of the target (DP-02; Architecture v5 slides 11 and 29). BR4 is split by schema — the constraint scan over `rwb_source_data` runs here, the scan over schema `recovery` and over the 19 `rwb_*` schemas runs in RWB-P1-E1069-APP and RWB-ITG-E1069-ITG. BR1 and BR5 are asserted here and delivered elsewhere: the view SQL is RWB-P1-E1069-APP's and the dictionary rows are RWB-P1-E1001-APP's. BR6 is delivered by the helper functions of the Section A migration, in RWB-P1-E1069-APP. BR8 is a build rule and lives in that story's build, not in the database. BR9 is the order in which the Section B grants are applied, and this story is the one that applies them.

The view conformance test of RWB-E1-069 ('Read-only ACE grant', version 4 section 10) sits with this P1 DB slice, the only holder of the grant. The P4 slice keeps the role and masking checks, and the per-service boundary test is the cross-schema check.

**Decision DL43.** Under the programme directive the recommended answer of DL43 is accepted: yes, the scope and dates as in RWB-ACE-001. ASM-0193, ASM-0737, ASM-0748 and ASM-0816 are confirmed. This does not report RWB-ACE-001 as deployed: BR9 and the Tier 2 precondition of section 3 still apply.

**Schema split (GAP-0557; ASM-0794 to ASM-0798, confirmed).** The built migration `V0001__rwb_e1_001_recovery_schema.sql` in schema `recovery` is kept as built and is not rewritten. P1's 13 own tables and the dictionary seed come from one new Flyway file of RWB-P1-E1001-APP on the rwb-source-data sequence, after the service baseline. The schema and the login are both `rwb_source_data`. This story creates the four extension tables; RWB-P1-E1001-APP seeds their 49 dictionary fields DF-EXT-001 to DF-EXT-049 and creates none of these tables. The data product catalog, the dictionary tables and the `v_data_dictionary` read model stay in `rwb_source_data`, and this story adds no REST operation.

### 9. State transitions

None in the runtime sense: a table has no state machine and this story changes no business row. The states this story moves through are the migration states of the service's Flyway history (pending, applied, failed, undone), one per version of this story's set.

| Item | States |
|---|---|
| a migration of this story | Pending, applied, failed, undone; an applied version is never edited |
| the login | Present and granted, or absent and named by the preflight; never a member of another service's login role |
| a grant | Held on a view or a table, refused with SQLSTATE 42501, or granted to PUBLIC, which is a failure in every schema |
| an extension row | One row per ACE key, or the second row refused with SQLSTATE 23505 |
| a constraint | Inside `rwb_source_data`, or naming `public`, which is a failure that blocks the merge |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The ACE database engineer (any team, per U3) | Writes and runs the migration set, the grant migrations and the schema checks |
| ACE team lead and ACE DBA | Own schema `public`; approve the 21 Tier 1 table list and grant SELECT to `ace_view_owner` (RWB-ACE-001); supply the ACE DBA role for the release window |
| Recovery tech lead and data architect | Approve a change to the 30-view list, which is frozen in the ACE Data Tier Map v1, and to the grant list |
| Recovery migration account | Applies this story's migrations and the view migrations in the fixed order in DEV and SIT |
| rwb-source-data owner (RWB-P1-E1069-APP) | Owns the view SQL and the read contract that run on these grants; writes no grant of its own |
| Platform DB owner (RWB-PLT-NF06-DB) | Owns the 19 schemas, the 19 logins and the credential policy |
| RW-PLATADM, platform administrator | Reads the deployment result on SCR-44 Migration runs (Platform administration R); may not change a grant |
| RW-AUDIT, internal audit | Reads the view list and the grants (Platform administration R) |
| RW-DATASTEW, data steward | Reads the dictionary rows of the four extension tables (Data product catalog R) |
| No approval level from the delegation of authority applies | A schema change is not a credit decision |

The login is named `rwb_source_data` (Architecture v5 slides 11 and 29; DP-02). Its credential and the rotation policy are held by the platform DB owner, and no personal name and no credential appears in a migration, a script or a runbook.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-EXT-001 to DF-EXT-012 | party_ext | person_key, vulnerable, deceased_override, bankruptcy, fraud_flag, is_active, state, version, created_at, created_by, updated_at, updated_by | Create (table) |
| DF-EXT-013 to DF-EXT-026 | contact_point_ext | contact_key, contact_type, consent_given, consent_at, verified_at, failed_count, source, is_active, state, version, created_at, created_by, updated_at, updated_by | Create (table) |
| DF-EXT-027 to DF-EXT-035 | account_ext | account_key, dispute_open, is_active, state, version, created_at, created_by, updated_at, updated_by | Create (table) |
| DF-EXT-036 to DF-EXT-049 | valuation_ext | valuation_key, accepted, accepted_at, accepted_by, valuer_partner_id, stale_flag, age_days, is_active, state, version, created_at, created_by, updated_at, updated_by | Create (table) |
| DF-ACE-001 to DF-ACE-304 | the 30 recovery.v_ace_* views | all 304 fields, 177 Section A and 127 Section B | Not created here; SELECT granted to the login, and SELECT held by ace_view_owner on the ACE tables behind them |
| Not specified in the source documents (DOR-RWB-P1-E1069-DB-7) | the 21 Tier 1 ACE tables of section 11 | account, payment, customer, phone, email, address, ca_relation, aa_relation, collateral, asset, efs_action, efs_action_code, efs_assignment, bucket_log_snapshot, product, branch, bot_holiday, ace_case, cfsc_mg_ssme_tdr_case, tdr_calculation, ai_recommended_plan | Not created and not altered; SELECT granted to ace_view_owner |
| Not specified in the source documents (DOR-RWB-P1-E1069-DB-7) | the 14 Tier 2 ACE tables of RWB-ACE-001 | ace_batch_run, valuation, collateral_detail, npa_asset, npa_sale, lawsuit, hearing, pod_receipt, gl_write_off, collins_score, party_product, credit_decision, esign_request, iam_group | Not created and not altered; SELECT granted to ace_view_owner once RWB-ACE-001 lands |

Field IDs are those in the Logical Data Model and Data Dictionary and are copied from legacy RWB-E1-069 §11 and TSD P1 T3.5. The 49 extension-table columns are this story's: it creates them and nothing else. The 304 view fields are not this story's: the view SQL that defines them is RWB-P1-E1069-APP's, and this story grants on the views and never selects their rows into a table of its own.

Counts as the legacy story and the TSD give them: 122 `sys_objects` rows (92 tables and 30 views) and 1,366 `sys_fields` rows (1,062 table fields and 304 view fields), of which 49 sit on the four extension tables. Those rows are rwb-source-data's own metadata, delivered with RWB-P1-E1001-APP; this story writes none of them.

### 12. Contract

**12.1 REST operations provided**

None. This is a database story and publishes no operation.

**12.2 REST operations consumed**

None.

**12.3 Events published**

None. The topic of the service is `rwb.source-data.events.v1` with event names `rwb.source-data.<Event>.v1` (DP-14), and this story publishes nothing on it.

**12.4 Events consumed**

None.

**12.5 Workflows and activities**

None.

**12.6 Schedules**

None. The migration set runs in the release pipeline, not on a Temporal Schedule.

**12.7 Tables owned**

| Table | Schema | Owner (ownership map) | Created or altered here |
|---|---|---|---|
| party_ext | rwb_source_data | P1 | Created: 12 columns, primary key `person_key` varchar(255) |
| contact_point_ext | rwb_source_data | P1 | Created: 14 columns, primary key `contact_key` varchar(255), check `ck_contact_point_ext_type` |
| account_ext | rwb_source_data | P1 | Created: 9 columns, primary key `account_key` varchar(255) |
| valuation_ext | rwb_source_data | P1 | Created: 14 columns, primary key `valuation_key` varchar(255) |

No table of another service and no `v_ace_*` view is created, altered or dropped here, and no service table other than these four is in this story. The 30 views are objects of schema `recovery`, created by RWB-P1-E1069-APP and owned by `ace_view_owner`; this story grants on them and writes no view definition. The dictionary tables `sys_objects`, `sys_fields` and `data_product` are rwb-source-data's own and are delivered with RWB-P1-E1001-APP; this story writes no row of them.

**12.8 Contract fakes**

| Fixture | Serves | Used by |
|---|---|---|
| `recovery_views.sql` fixture | The Physical Schema folder: the 30 view definitions | The grant migrations name the 30 views from this list and grant on no other object |
| Delivered-views fixture | RWB-P1-E1069-APP | A container with the baseline, schema `recovery`, the 30 views and the three helper functions, so the grants are tested against the real views without a second definition |
| ACE head fixture | ACE Schema PostgreSQL v1.sql | The 21 Tier 1 tables the view owner is granted on |
| No-grant role | The test role `rwb_no_grant` with no grant anywhere | AC2 |

A database story uses no service contract fake; the four fixtures above stand in for the two neighbouring stories and for the ACE head.

**12.9 Call-type summary**

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | None | None | No operation in this story |
| Kafka | None | None | No topic in this story |
| Temporal | None | None | No workflow, activity or Schedule |
| File | None | None | Migrations are deployed by the release pipeline, not by a file interface |
| SQL view | 30 `recovery.v_ace_*` views, SELECT granted to the `rwb_source_data` login | The 21 Tier 1 tables and the 14 Tier 2 tables, read by `ace_view_owner` through the views only | SQL only: SELECT, never a write, and no statement in this story reads another service's schema |

### 13. Solution plan

**Sequencing.** rwb-source-data's Flyway sequence is owned by the platform; the V0001 baseline creates the schema, the history table and the standard record columns (DP-15). This story adds the extension-table migration and the two grant migrations, and the two view migrations of RWB-P1-E1069-APP sit between them:

| Position on the sequence | File | Contents |
|---|---|---|
| baseline | from the platform DB story | Schema `rwb_source_data`, history table, standard record columns |
| next | `..._rwb_e1_069_extension_tables.sql` | The four extension tables, their primary keys and the `ck_contact_point_ext_type` check |
| next | `V0002__rwb_e1_069_ace_source_views.sql` (RWB-P1-E1069-APP) | The three helper functions and the 16 Section A views in schema `recovery` |
| next | `..._rwb_e1_069_ace_source_views_grant.sql` | The Section A grant block: `ace_view_owner`, the 21 Tier 1 tables, the view ownership, the login's SELECT on the 16 views and the PUBLIC revoke |
| next | `V0003__rwb_e1_069_ace_tier2_views.sql` (RWB-P1-E1069-APP) | The 14 Section B views |
| next | `..._rwb_e1_069_ace_tier2_views_grant.sql` | The Section B grant: SELECT on the 14 Tier 2 tables for `ace_view_owner`, the view ownership and the login's SELECT on the 14 views |

The legacy migration names `V0002__rwb_e1_069_ace_source_views.sql` and `V0003__rwb_e1_069_ace_tier2_views.sql` are recorded as the source of the objects they hold; the exact version numbers of this story's three migrations are assigned by the sequence owner at build time, and no monolith version number is reused. Until RWB-ACE-001 is reported deployed, the last two positions are not applied and the features that read a Section B view stay behind their flags (BR9).

The platform dependency of the sequence is `RWB-PLT-E1044-CON`: it is not in this story's "Depends on (build)" list, which the Work Package fixes as None, so it is recorded here as a note and not as a metadata dependency (GAP-0568; ASM-0811).

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

DP-01, DP-02, DP-05 and DP-15 are the subject of this story: one schema, one login, one read path and one sequence. DP-03, DP-06, DP-07, DP-08, DP-11 and DP-19 are named for completeness of the pattern set: this story writes no decision record, calls no contract, starts no workflow and serves no screen, and their build dependencies stay with the application story.

Screen SCR-44 is not part of this story. This story serves no screen, so it has no empty, loading, error or no-access state; any such state for SCR-44 is owned by the story that builds that screen.

**Grant block (the legacy section 12 block, with the schema fixed and the login renamed)**

```sql
GRANT USAGE ON SCHEMA public TO ace_view_owner;
GRANT SELECT ON public.account, public.payment, public.customer, public.phone, public.email,
     public.address, public.ca_relation, public.aa_relation, public.collateral, public.asset,
     public.efs_action, public.efs_action_code, public.efs_assignment,
     public.bucket_log_snapshot, public.product, public.branch, public.bot_holiday,
     public.ace_case, public.cfsc_mg_ssme_tdr_case, public.tdr_calculation,
     public.ai_recommended_plan
     TO ace_view_owner;

ALTER VIEW recovery.v_ace_account OWNER TO ace_view_owner;
-- one ALTER VIEW OWNER statement for each of the 16 views

GRANT USAGE ON SCHEMA recovery TO rwb_source_data;
GRANT SELECT ON recovery.v_ace_account TO rwb_source_data;
-- one GRANT per view, 16 in the Section A grant and 30 in all; never GRANT SELECT ON ALL TABLES IN SCHEMA recovery

REVOKE ALL ON ALL TABLES IN SCHEMA recovery FROM PUBLIC;
```

The Section B grant adds, once RWB-ACE-001 is deployed:

```sql
GRANT SELECT ON public.ace_batch_run, public.valuation, public.collateral_detail,
     public.npa_asset, public.npa_sale, public.lawsuit, public.hearing, public.pod_receipt,
     public.gl_write_off, public.collins_score, public.party_product,
     public.credit_decision, public.esign_request, public.iam_group
     TO ace_view_owner;

ALTER VIEW recovery.v_ace_batch_status OWNER TO ace_view_owner;
-- one ALTER VIEW OWNER statement for each of the 14 views

GRANT SELECT ON recovery.v_ace_batch_status TO rwb_source_data;
-- one GRANT per view for the 14 Section B views
```

No `GRANT ... ON ALL TABLES` appears in any migration that touches the views, PUBLIC receives nothing, and the login receives no write privilege on a view and no privilege at all in `public`.

**Table definitions** (verbatim from Physical Schema v7, legacy RWB-E1-069 §13)

- `party_ext`: `person_key` varchar(255) primary key, `vulnerable`, `deceased_override`, `bankruptcy`, `fraud_flag` boolean NOT NULL DEFAULT false, `is_active` boolean NOT NULL DEFAULT true, `state` varchar(40), `version` integer NOT NULL DEFAULT 1, `created_at` and `updated_at` timestamptz NOT NULL DEFAULT now(), `created_by` and `updated_by` uuid.
- `contact_point_ext`: `contact_key` varchar(255) primary key, `contact_type` varchar(10) NOT NULL, `consent_given` boolean NOT NULL DEFAULT false, `consent_at` and `verified_at` timestamptz, `failed_count` integer NOT NULL DEFAULT 0, `source` varchar(20) NOT NULL DEFAULT 'WORKBENCH', `is_active`, `state`, `version`, `created_at`, `created_by`, `updated_at`, `updated_by`, and the check `ck_contact_point_ext_type` that `contact_type` is PHONE, EMAIL or ADDRESS.
- `account_ext`: `account_key` varchar(255) primary key, `dispute_open` boolean NOT NULL DEFAULT false, `is_active`, `state`, `version`, `created_at`, `created_by`, `updated_at`, `updated_by`.
- `valuation_ext`: `valuation_key` varchar(255) primary key, `accepted` boolean NOT NULL DEFAULT false, `accepted_at` timestamptz, `accepted_by` and `valuer_partner_id` uuid, `stale_flag` boolean NOT NULL DEFAULT false, `age_days` integer, `is_active`, `state`, `version`, `created_at`, `created_by`, `updated_at`, `updated_by`.

The four tables hold 49 columns in all, which are the 49 fields `DF-EXT-001` to `DF-EXT-049`. The primary key of each is the ACE business key: there is no `id` column and there is no foreign key into `public`, and `valuer_partner_id` carries no foreign key (TSD P1 T3.5).

**Schema privileges and revokes.** The login owns schema `rwb_source_data`, which carries USAGE and the table privileges the application story needs. On the ACE side it holds USAGE on schema `recovery` and SELECT on each of the 30 views, and nothing else: no USAGE on `public`, no privilege on a `public` table, no write on a view, and no grant on another service's schema. PUBLIC is revoked on all tables of schema `recovery`, and no grant to PUBLIC is written in any migration of this story.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `..._rwb_e1_069_extension_tables.sql` | Migration | The four extension tables, their primary keys, their standard record columns and the `ck_contact_point_ext_type` check |
| `..._rwb_e1_069_ace_source_views_grant.sql` | Migration | The Section A grant: `ace_view_owner`, the 21 Tier 1 tables, the 16 view owners, the login's SELECT on the 16 views, the PUBLIC revoke |
| `..._rwb_e1_069_ace_tier2_views_grant.sql` | Migration | The Section B grant: the 14 Tier 2 tables, the 14 view owners and the login's SELECT on the 14 views |
| `SchemaBoundaryCheck` | Pipeline check | No constraint in `rwb_source_data` names a schema outside it; every ACE link is `varchar(255)` with no foreign key |
| `GrantCheck` | Pipeline check | The login's grants, the view owner's ownership and privileges, the refusals with SQLSTATE 42501 and PUBLIC empty |
| `ExtensionKeyCheck` | Pipeline check | The four tables' columns, primary keys, the check, the 49 field IDs and the duplicate-key refusal |

**Build steps**

1. The extension-table migration with the four tables, their primary keys and the check, and a failing fixture for a duplicate name (AC5, AC7).
2. The Section A grant migration with the 21 Tier 1 table names, the 16 view owners, the 16 SELECT grants and the PUBLIC revoke; a fixture that asserts no `ALL TABLES` grant and no grant in `public` (AC2, AC3, AC4).
3. The Section B grant migration, wired to run only after RWB-ACE-001 is reported deployed (AC2, AC4, BR9).
4. The `SchemaBoundaryCheck` over the catalogue, with a fixture that adds a foreign key to `public.account` (AC7).
5. The `GrantCheck` as a container test with sessions as the login, `ace_view_owner` and the test role `rwb_no_grant`, which owns no schema (AC1, AC2, AC3, AC4).
6. The `ExtensionKeyCheck` with the duplicate-key fixtures, rolled back in the same transaction (AC5, AC6).
7. A repeated-run test of the whole set on a copy of the SIT schema (AC8).
8. The release note of the sequence, with the version numbers and the checksums of the three migrations.

**Done when.** The migration set applies twice without a change, the catalogue checks pass, the login holds SELECT on the 30 views and nothing else, `ace_view_owner` owns the 30 views and holds SELECT on the 21 Tier 1 and 14 Tier 2 ACE tables with no DML, the four extension tables hold their 49 columns and refuse a second row for one ACE key, no constraint in `rwb_source_data` names `public`, and the tests in section 16 pass.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| Conformance check 1 | A view does not compile | v_ace_account does not compile: column a.core_banking_system_date does not exist |
| Conformance check 2 | A constraint references `public` | fk_case_account_account_key references public.account; no constraint in recovery may reference another schema |
| Conformance check 3 | A view has no dictionary row | v_ace_account.legacy_bucket has no data dictionary entry |
| Conformance check 4 | The service login holds a privilege in `public` or can write a view | recovery_svc holds SELECT on public.account; the recovery role reads the views only |
| Build log | A recovery class names a `public` table | Boundary rule BND-6 broken: AccountReader reads public.account. Read recovery.v_ace_account instead. |
| SQLSTATE 42501 | The service login selects a public table or writes a view | permission denied for schema public |
| SQLSTATE 23505 | A second row for one ACE key in an extension table | duplicate key value violates unique constraint party_ext_pkey |
| Check finding, no message id | A constraint of `rwb_source_data` names a schema outside it | The pipeline check names the constraint and the referenced object; the key is removed |

The five conformance, build-log and SQLSTATE texts are copied from RWB-E1-069, character for character, including the role name `recovery_svc` they carry, which is the `rwb_source_data` login of the target (DP-02). They are pipeline and build log texts for developers and are not part of the message standard. No `MSG-` ID applies to this story: it has no user-facing message, and the messages of the application layer are raised by RWB-P1-E1069-APP and by the guard library.

### 15. Screens and states

No screen. The result of a migration is visible in the release pipeline and in the service's Flyway history (pending, applied, failed, undone, each with a version and a checksum). The platform administrator reads the deployment result under Platform administration R and on SCR-44 Interface and job monitor, and the data steward reads the dictionary rows of the four extension tables. Nothing in this story is shown to a user directly: the four tables are read through the application and its contract, never through SQL on a screen. SCR-44 states empty, loading, error and no access are Not specified in the source documents (CG-ALL-2348).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-069-01 | AC8; regression evidence for legacy AC1 on the migration history | End to end | Clean PostgreSQL 17 container: ACE Schema PostgreSQL v1.sql, the baseline, then this story's migrations and the two view migrations in order; a repeated run |
| TC-E1-069-02 | AC2, AC3, AC4; regression evidence for legacy AC2 | Component | Sessions as rwb_source_data, ace_view_owner and a test role with no grant in SIT |
| TC-E1-069-03 | AC2, AC4; regression evidence for legacy AC3 on the Section B grant | End to end | Tier 2 probe with the 14 tables; the Section B grant applied after RWB-ACE-001 is reported deployed |
| TC-E1-069-04 | AC7; regression evidence for legacy AC4 | End to end | Branch adding a foreign key from account_ext.account_key to public.account |
| TC-E1-069-05 | AC5; regression evidence for legacy AC5 on the 49 extension-table fields | End to end | 122 objects and 1,366 fields; the 49 dictionary fields DF-EXT-001 to DF-EXT-049 |
| TC-E1-069-06 | None of the new criteria; regression evidence only, for the dictionary mapping the grant does not change | End to end | Account ACC0000017 with delay_days 95; dictionary query |
| TC-E1-069-07 | AC5, AC6; regression evidence for legacy AC7 | End to end | Duplicate person_key P0000123 in party_ext; column list of the four tables |
| TC-E1-069-08 | AC7; regression evidence for legacy AC8 on the boundary the grants enforce | End to end | Fixture AccountReader on public.account and on recovery.v_ace_account; native query fixture |

This story owns no legacy acceptance criterion, so the eight rows above are the legacy test cases of RWB-E1-069 listed as regression evidence: their IDs, their data and their level are kept, the legacy level "System" maps to "End to end" and "Access" to "Component", and the Covers column names this story's own criteria only where the legacy case exercises the artefacts in this story's title. The legacy criteria themselves are owned by RWB-P1-E1069-APP and proven across the 19 logins in RWB-ITG-E1069-ITG. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in a constraint: the check `ck_contact_point_ext_type` is business-neutral and comes from the legacy physical schema; every other business value, the masking answer and the authorise decision are data read by the application, not constants in a migration.
- No personal data in a migration, a script, a test fixture or a runbook: the four tables hold business keys and flags only, `person_key` is a business key and never a name, and the test values `P0000123` and `ACC0000017` are synthetic.
- No read of another schema and no key into another schema: `rwb_source_data` objects reference `rwb_source_data` objects only, and a key to `public.account` is forbidden because ACE cascades deletes on `account` (DP-01, BR4).
- One login per service: `rwb_source_data` is the only grantee on the 30 views, and no other login is granted on them (DP-02; Architecture v5 slide 29).
- No write path into ACE data: no INSERT, UPDATE, DELETE or TRUNCATE is granted on a view, and the four extension tables hold Workbench decisions only.
- No privilege for PUBLIC anywhere, and no `GRANT ... ON ALL TABLES` in any migration that touches the views.
- The schema is the fixed `recovery`: no `${recoverySchema}` token and no environment name survives in a migration (DP-15).
- An applied migration is never edited: a correction is a new version, and a wrong grant is revoked by a later version, never by an edit.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | Rules | Test cases |
|---|---|---|---|---|---|
| REQ-RDF-002 | Account balance, arrears, payments and classification for every account at 90 or more days past due are read from ACE through `v_ace_account` and `v_ace_payment`, current to the previous working day | Business Requirements Epic 1, sections 3.1 and 4 | FEAT-RDF-01 | D-RCV-35 U4; BR-P1-001-2; BR-P1-001-3; BR-P1-001-4 | TC-E1-069-01, TC-E1-069-02, TC-E1-069-05, TC-E1-069-06 |
| REQ-DRI-006 | No component calls a system of record directly | Business Requirements Program, sections 5.2 and 7 | FEAT-RDF-01 | ADR-010; DL43; BR-P1-001-3 | TC-E1-069-04, TC-E1-069-05, TC-E1-069-07, TC-E1-069-08 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-P1-E1069-APP | App development | Sibling of the same legacy key: the view SQL, the conformance test and the read contract that run on these grants; its two view migrations sit between this story's migrations on the sequence |
| RWB-P1-E1001-APP | App development | H sibling: the `rwb_source_data` baseline and the dictionary rows of the four extension tables |
| RWB-P1-ACE001-DB | ACE DB | The 14 Tier 2 tables and their SELECT grant to `ace_view_owner` |
| RWB-P4-E1069-APP | App development | Sibling of the same legacy key: the masking policy rows and the boundary of rwb-access; it holds no grant on the views and creates none of these tables |
| RWB-ITG-E1069-ITG | Integration | Proves the grant matrix across the 19 logins, both halves of boundary rule BND-6 and the four extension tables end to end |
| RWB-ACE-001 | ACE DB story (legacy) | The ACE team's 14 Tier 2 tables and its grant to `ace_view_owner` (DL43) |
| RWB-PLT-NF06-DB | ACE DB | The 19 schemas, the 19 logins and the credential policy |
| RWB-PLT-N011 | Not specified in the source documents (GAP-0111) | The migrator roles; no role name is invented |
| RWB-PLT-E1044-CON | Contract | The per-service Flyway sequence and its version allocation, recorded as a note in section 13 |

### 19. Out of scope

- The view SQL of the 16 Section A and 14 Section B views, the three helper functions and the view conformance test: RWB-P1-E1069-APP.
- The ACE read contract, the authorise-and-mask hop and the read path of the other 18 services: RWB-P1-E1069-APP.
- The proof of the grant matrix across the 19 logins and the second half of boundary rule BND-6 (no `v_ace_*` view named outside rwb-source-data, no other service's schema named): RWB-ITG-E1069-ITG.
- The 14 Tier 2 tables and the 12 columns that RWB-ACE-001 adds to `account`, `customer` and `efs_action`: the ACE team owns them, and this story neither creates nor alters them.
- The masking policy rows and the masking answer: rwb-access, RWB-P4-E1069-APP (DP-08).
- The dictionary content and its maintenance: RWB-P1-E1001-APP for the metadata rows and RWB-E1-064 in the legacy set for the dictionary of the 14 data products.
- The application code, the read operations and the response shape: RWB-P1-E1069-APP.
- The freshness stamp, the case list, the reconciliation, the data products and the business-day operations: the other P1 stories, among them RWB-P1-E1013-APP.
- Any change to the 30-view list or to the grant list: the data architect and the recovery tech lead, with a new version of the ACE Data Tier Map v1.
- Performance tuning beyond the primary keys named here: the non-functional work.
