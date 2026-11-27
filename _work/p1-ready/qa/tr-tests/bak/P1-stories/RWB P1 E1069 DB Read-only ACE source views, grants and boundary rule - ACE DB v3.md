# RWB-P1-E1069-DB Read-only ACE source views, grants and boundary rule - ACE DB

**Version 3 changes**

- Acceptance criteria rewritten so that they can pass on PostgreSQL (public schema USAGE not asserted, view writes 55000 or 42501), with AC9 to AC20 added for the single reader, indirect paths, extension-table DML, defaults, exception paths, Section B and corrections (findings 1, 2, 11, 13, 15, 16 and 18).
- The login is created by RWB-PLT-NF06-DB only; statements on `public` and `recovery` are not run by the service migrator, and their identity is Pending under NEW-GAP-S7-05 (findings 3, 4 and 5).
- Explicit extension-table grants without DELETE (RD-P1-048), classified columns named, the stale rule removed and forward-only migrations with Pending, Applied and Failed states (RD-P1-045; findings 7, 14, 17 and 18).
- Grant block, names, versions, dependencies and test cases aligned to Physical Schema v9, LDM v11, Security and Access Design v6 and Test Cases v9; RD-P1-021, RD-P1-043 and RD-P1-046 applied (findings 6, 8, 9, 10, 12, 19, 20, 21 and 22).
- Finishing pass: test case IDs TC-P1-E1069-DB-01 to -12 of Test Cases v9 cited for AC9 to AC20; the owner of the Tier 2 table grant is noted as Pending (NEW-GAP-S11-13).

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P1-E1069-DB |
| Version | 3 |
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
| Ready to start | After RWB-PLT-NF06-DB, RWB-PLT-E1044-CON, RWB-P1-E1001-APP and the Section A view migration of RWB-P1-E1069-APP; Section B after the ACE dependency gate |
| Size | Not specified in the source documents (DOR-RWB-P1-E1069-DB-16) |
| Depends on (build) | RWB-PLT-NF06-DB, RWB-PLT-E1044-CON, RWB-P1-E1001-APP, RWB-P1-E1069-APP |
| Contract dependencies | None: this DB story publishes and consumes no API contract, so no contract story, no contract fake library version and no contract version apply |
| Integration dependencies | None |
| External dependencies | RWB-P1-ACE001-DB (Section B tables and their grant to ace_view_owner); ACE DBA for statements on public and recovery (NEW-GAP-S7-05); DL43 (ACE team lead; recommended answer A is the planning basis) |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v1.md (FR-P1-001, FR-P1-002, FR-P1-005) |
| Readiness decisions | RD-P1-021, RD-P1-043, RD-P1-045, RD-P1-046, RD-P1-048 |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-069 for the ACE database work of rwb-source-data. The single `recovery` schema of the monolith is replaced by one schema and one login per service (DP-01, DP-02; Architecture v5 slides 8, 9 and 29): the 30 `recovery.v_ace_*` views stay in schema `recovery`, owned by `ace_view_owner`, and only the `rwb_source_data` login holds SELECT on them; the four extension tables `party_ext`, `contact_point_ext`, `account_ext` and `valuation_ext` move with the service into schema `rwb_source_data`. The grant block of legacy section 12 is reused with the schema fixed to `recovery` and the service role renamed `rwb_source_data`. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P1-E1069-DB). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (18 resolved, 29 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: view grants, execution identity, extension-table grants, forward-only migrations, acceptance criteria and test case mapping. Agent: S7-stories.

### 1. Story

As a **recovery developer (RW-TRIBE) acting as the ACE database engineer**, I want **the grants of the `rwb_source_data` login of this service, the view owner `ace_view_owner` with SELECT on the 21 Tier 1 and 14 Tier 2 ACE tables, SELECT on each of the 30 `recovery.v_ace_*` views and no table privilege in `public`, the four extension tables `party_ext`, `contact_point_ext`, `account_ext` and `valuation_ext` in schema `rwb_source_data` with their primary keys, their standard record columns, the `ck_contact_point_ext_type` check and their 49 field IDs, and a schema in which no constraint names `public` and every link to an ACE record is a `varchar(255)` business key with no foreign key**, so that **one copy of ACE source data serves the Workbench without a second copy, without a write path into ACE data, and with a catalog that refuses a breach instead of a review that hopes**.

This is the database slice of legacy RWB-E1-069. It delivers:

- the grant set of the `rwb_source_data` login that RWB-PLT-NF06-DB creates: USAGE on schema `recovery`, SELECT on each of the 30 views, one GRANT and one ALTER VIEW OWNER per view, no table privilege in `public` and no write on a view (DP-02, DP-05); this story creates no login;
- the view owner `ace_view_owner`: USAGE on schema `public` and SELECT on the 21 Tier 1 tables of section 11, SELECT on the 14 Tier 2 tables once RWB-ACE-001 lands, the ownership of the 30 views, and no DML;
- the four extension tables in schema `rwb_source_data`, with their columns, their primary keys, the `ck_contact_point_ext_type` check and the 49 field IDs `DF-EXT-001` to `DF-EXT-049`; `valuation_ext.stale_flag` and `age_days` (`DF-EXT-041`, `DF-EXT-042`) are created as columns only, and their writer is not ruled (GAP-1509);
- explicit SELECT, INSERT and UPDATE grants on the four extension tables to `rwb_source_data`, and no DELETE (RD-P1-048: P1 never deletes these rows);
- the schema privileges and the PUBLIC revokes;
- the schema checks: no constraint in `rwb_source_data` names `public`, and every ACE link is a `varchar(255)` business key with no foreign key;
- the migration set on rwb-source-data's per-service Flyway sequence (DP-15), with a repeated run that changes nothing.

It does not create, alter or own the view SQL, the conformance test or the read contract: those are RWB-P1-E1069-APP. It does not prove the grant matrix across the 19 logins: that is RWB-ITG-E1069-ITG. It writes no application code and no REST operation.

### 2. Business rationale

The legacy story proved the boundary against one schema: 30 SELECT-only views over the ACE tables, one view owner, one service role, boundary rule BND-6 and a conformance test in the pipeline. In the target the same objects must work across 19 schemas and 19 logins, where the ownership rule is enforced by grants and not by separate servers (Architecture v5 slide 29: "Ownership is enforced by grants, not by separate servers").

This story is the grant and ownership half of that proof. It fixes who may read the views (the `rwb_source_data` login of this service and no other), who owns them (`ace_view_owner`, which holds SELECT on the ACE tables they read and nothing else), and where the Workbench's own decisions about an ACE record live (the four extension tables, in the service's own schema, keyed by the ACE business key and holding no copy of an ACE column). Everything else follows from those three facts: a direct read of a `public` table fails at the database, a write on a view fails at the database, a second row for one ACE key fails on the primary key, and no service can reach another service's rows because each login is granted on its own schema only (DP-01, DP-02; Architecture v5 slides 8, 11, 29 and 45).

Serves REQ-RDF-002 (ACE source data read only through the views) and REQ-DRI-006 (no component calls a system of record directly). The measure is the one the legacy story set: 100 percent of pipeline runs in which every view compiles, every grant is as specified and the conformance test passes (FSD P1 A2.1.1). The business value is not restated here: this story adds no new one.

### 3. Preconditions

- The per-service Flyway sequence of rwb-source-data exists with its history table in schema `rwb_source_data`, and the baseline of RWB-P1-E1001-APP has been applied on it (DP-15; RWB-PLT-E1044-CON).
- RWB-PLT-NF06-DB has created the 19 `rwb_*` schemas and logins; the login of this service is `rwb_source_data` and owns schema `rwb_source_data` (Security and Access Design v6; Environment and Deployment Design v7). This story never creates a login; a missing login fails the grant (X2).
- The credential of the login and its rotation are held by the platform, and no credential appears in a migration, a script or a runbook (GAP-0568; ASM-0809).
- The service migrator `rwb_source_data_migrator` of RWB-PLT-N011-DB holds no right in schema `public` or schema `recovery`. Role creation, grants on `public` and `recovery` and ALTER VIEW OWNER are applied by a database principal that holds those rights. Pending: that principal, its execution location and whether those files run on the service sequence, owner ACE DBA with platform DB owner, tracked as NEW-GAP-S7-05.
- RWB-P1-E1069-APP creates the three helper functions and the views in schema `recovery`. Apply order: extension tables, Section A views, Section A grants, Section B views, Section B grants.
- The ACE schema in DEV and SIT holds the 21 Tier 1 tables of section 11, among them `account`, `payment`, `customer` and `efs_action` (ACE Schema PostgreSQL v1.sql).
- Section B: in DEV and pipeline test the 14 Tier 2 tables and 12 columns come from `tier2-ddl.sql` of RWB-P1-E1065-CON. In SIT, UAT and PROD no Section B view or grant is applied until RWB-ACE-001 has landed in that environment (ACE dependency gate); RWB-P1-ACE001-DB grants SELECT on the 14 tables to `ace_view_owner`. Pending: confirmation that RWB-P1-ACE001-DB is the one owner of that grant statement and this story only asserts it, owner solution architect (NEW-GAP-S11-13). DL43 stays the ACE team lead's decision; recommended answer A (scope and dates as in RWB-ACE-001) is the planning basis (RD-P1-043).
- The four extension tables are those of Physical Schema v9 `rwb_source_data.sql` with LDM v11 field IDs `DF-EXT-001` to `DF-EXT-012` (`party_ext`), `DF-EXT-013` to `DF-EXT-026` (`contact_point_ext`), `DF-EXT-027` to `DF-EXT-035` (`account_ext`) and `DF-EXT-036` to `DF-EXT-049` (`valuation_ext`). Columns that later stories add (`contact_point_ext.person_key`, `DF-EXT-050`, RWB-P1-E2022-APP; `migration_source` and `migrated_at`, RWB-P1-DM005-APP and RWB-P1-DM006-APP) are not this story's.
- The 30-view list is frozen in the ACE Data Tier Map v2 and in `recovery_views.sql` of Physical Schema v9, whose grants block names `rwb_source_data` as the single reader; this story grants on those 30 names and on no other object.
- No approval is required to run a Draft migration on a development database; a migration is released to SIT only after the tests of section 16 pass.

### 4. Flow

1. The ACE database engineer confirms the highest applied version on the rwb-source-data sequence and that the logins `rwb_source_data` and `rwb_source_data_migrator` exist.
2. Extension-table migration, applied by the service migrator: the four tables with their primary keys, standard record columns and `ck_contact_point_ext_type`, then GRANT SELECT, INSERT, UPDATE on the four tables to `rwb_source_data`. No DELETE is granted.
3. RWB-P1-E1069-APP applies the three helper functions and the 16 Section A views.
4. Section A grant file, one transaction, applied by the privileged principal of NEW-GAP-S7-05: create `ace_view_owner` NOLOGIN if it does not exist; USAGE on schema `public` and SELECT on the 21 Tier 1 tables for `ace_view_owner`; one ALTER VIEW OWNER per Section A view (run by a superuser, or with CREATE on schema `recovery` granted to `ace_view_owner` and revoked in the same transaction); USAGE on schema `recovery` and one SELECT grant per view for `rwb_source_data`; REVOKE ALL ON ALL TABLES IN SCHEMA recovery FROM PUBLIC.
5. Section B grant file, after the Section B views: the same pattern for the 14 views and SELECT on the 14 Tier 2 tables for `ace_view_owner` (in ACE environments granted by RWB-P1-ACE001-DB and asserted here; in DEV and pipeline test granted over the fixture). It runs in DEV and pipeline test now and elsewhere only after the ACE dependency gate.
6. The pipeline runs the grant, ownership, membership, extension-table, boundary and duplicate-key checks of section 7; test roles are created and dropped by the test.
7. The pipeline runs the files a second time and Flyway validate.
8. The release note records each file with its version, checksum and corrective forward script (RD-P1-045).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A grant file runs before the views it grants on | The file fails on the missing relation, its transaction rolls back and no grant, role change or applied history row remains | Database error, no message id | AC14 |
| X2 | The login `rwb_source_data` does not exist when a grant runs | The file fails naming the role; no login is created here (RWB-PLT-NF06-DB) | Database error, no message id | AC15 |
| X3 | The service login holds a table privilege in `public` or a write on a view, or another login holds a view privilege | The grant check fails the build and names the role, privilege and object | {role} holds {privilege} on {object} | AC2, AC3, AC9, AC10 |
| X4 | A constraint in `rwb_source_data` references an object outside the schema | The boundary check fails and names the constraint and object | {constraint} references {object}; no constraint in rwb_source_data may reference another schema | AC7 |
| X5 | An ACE link column is not `varchar(255)`, or carries a foreign key | The check fails and names the column | Check finding, no message id | AC7 |
| X6 | A second row is written for an ACE key already in an extension table | The write is refused; the first row is unchanged | SQLSTATE 23505 | AC6 |
| X7 | An extension table already exists when the table migration runs | The migration fails (SQLSTATE 42P07), creates none of the other tables and records nothing as applied | Database error, no message id | AC16 |
| X8 | The set is run a second time | No pending migration; no object, row or grant changes | None | AC8 |
| X9 | RWB-ACE-001 has not landed in SIT, UAT or PROD | No Section B grant is applied; Section B flags stay off | Pipeline result | AC17 |
| X10 | An applied migration file is edited | Flyway validate fails with a checksum mismatch naming the version; no statement runs | Pipeline result | AC19 |
| X11 | A grant or ownership is wrong after apply | A new forward version revokes or reassigns it; no applied file is edited and no down script exists | Pipeline result | AC20 |
| X12 | `contact_type` is not PHONE, EMAIL or ADDRESS | The write is refused | SQLSTATE 23514 (23502 for null) | AC12 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the platform logins, the service baseline and the view migrations of RWB-P1-E1069-APP; Section B needs the ACE dependency gate outside DEV |
| Negotiable | Constraint and index names follow the platform naming library; the column set, the primary keys, the check and the grant list are fixed by the legacy story and the TSD |
| Valuable | The read path of 19 services is granted from one place, and the Workbench's own decisions about an ACE record have a schema that cannot write to ACE |
| Estimable | Four tables, one check, three migration files and the schema checks; the privileged principal is Pending under NEW-GAP-S7-05 |
| Small | Days, not weeks, with the catalogue checks |
| Testable | Every criterion in section 7 is one catalogue query, one refused statement with its SQLSTATE, or one pipeline run |

### 7. Acceptance criteria

```gherkin
Feature: The grants and the four extension tables of rwb-source-data

  Background:
    Given the ACE schema in DEV holds the 21 Tier 1 tables of section 11, among them public.account, public.payment, public.customer and public.efs_action
    Given schema recovery holds the three helper functions and the 16 Section A views of RWB-P1-E1069-APP, and the 14 Section B views where Section B is applied
    Given schema rwb_source_data exists on the rwb-source-data Flyway baseline (DP-15)

  Scenario: AC1 The rwb_source_data login holds its own schema and the view read only
    Given the login "rwb_source_data" and the other 18 service logins of RWB-PLT-NF06-DB
    When the catalogue is queried for its memberships, schema ownership and privileges
    Then the login is a member of no role, including ace_view_owner and pg_read_all_data
    And it owns schema rwb_source_data and no other schema
    And it holds USAGE on schema recovery, no table privilege on any table of schema public and no grant on any other rwb_* schema
    And no credential or password appears in a migration, a script or a runbook
    # TC-E1-069-12

  Scenario: AC2 The login reads each applied view and is refused on public.account
    Given the Section A grants are applied
    When a session as "rwb_source_data" selects each of the 16 Section A views with LIMIT 1
    Then 16 of 16 statements return without error, with zero or more rows
    When the same session selects from public.account
    Then the statement fails with SQLSTATE 42501
    And has_table_privilege('rwb_source_data', <table>, 'SELECT') is false for every table of schema public
    And the test role "rwb_no_grant", created and dropped by the test, cannot select recovery.v_ace_account
    # TC-E1-069-13

  Scenario: AC3 The login holds no write on any view
    Given the SELECT grant on each applied view
    When the catalogue is queried
    Then has_table_privilege is false for INSERT, UPDATE, DELETE and TRUNCATE for "rwb_source_data" on every applied view
    When the session runs insert, update and delete on recovery.v_ace_account
    Then each statement fails with SQLSTATE 55000 or 42501 and the row counts of the ACE tables behind the view are unchanged
    And the grant file grants one view at a time and holds no "GRANT SELECT ON ALL TABLES IN SCHEMA recovery"
    And it holds "REVOKE ALL ON ALL TABLES IN SCHEMA recovery FROM PUBLIC" and PUBLIC holds nothing on any view
    # TC-E1-069-14

  Scenario: AC4 ace_view_owner owns the Section A views and holds SELECT on the ACE tables only
    Given the Section A grants are applied
    When the catalogue is queried for the view owner
    Then "ace_view_owner" is NOLOGIN and no service login is a member of it
    And it owns the 16 Section A views
    And it holds USAGE on schema public and SELECT on exactly the 21 Tier 1 tables of section 11 among the ACE tables
    And it holds no INSERT, UPDATE or DELETE on any of them
    And it holds no CREATE on schema recovery or schema public after the migration
    # TC-E1-069-15

  Scenario: AC5 The four extension tables match Physical Schema v9
    Given the extension-table migration is applied
    When information_schema.columns and pg_constraint are compared with Physical Schema v9
    Then name, type, length, nullability and default match for the 49 columns DF-EXT-001 to DF-EXT-049, and no other column exists at this version
    And party_ext holds 12 columns with primary key person_key, contact_point_ext 14 with contact_key, account_ext 9 with account_key and valuation_ext 14 with valuation_key
    And ck_contact_point_ext_type allows contact_type PHONE, EMAIL or ADDRESS
    And each table carries is_active, state, version, created_at, created_by, updated_at and updated_by
    # TC-E1-069-16

  Scenario: AC6 A duplicate ACE business key is refused with SQLSTATE 23505
    Given one row each in party_ext ("P0000123"), contact_point_ext ("PHONE:PH-0001"), account_ext ("ACC0000017") and valuation_ext ("VAL-0001")
    When a second row with the same key is written to each table inside a transaction
    Then each write fails with SQLSTATE 23505 naming party_ext_pkey, contact_point_ext_pkey, account_ext_pkey or valuation_ext_pkey
    And each table holds one row for that key
    And the transaction is rolled back and no test row survives
    # TC-E1-069-17

  Scenario: AC7 No constraint leaves the schema and every ACE link is a business key
    Given the applied schema rwb_source_data
    When the catalogue is queried for every constraint of the schema
    Then no constraint references a table, type or schema outside rwb_source_data
    And person_key, contact_key, account_key and valuation_key are varchar(255) columns with no foreign key
    When a branch adds foreign key fk_test_account_ext_account from account_ext.account_key to public.account
    Then the pipeline check fails with "fk_test_account_ext_account references public.account; no constraint in rwb_source_data may reference another schema"
    And the merge is blocked
    # TC-E1-069-18

  Scenario: AC8 The files are on the per-service sequence and a repeated run changes nothing
    Given an empty database and a SIT copy holding synthetic rows only
    When the extension-table file and the Section A grant file are applied and then run again
    Then each file is recorded once with its version and checksum
    And the second run applies no migration, and the grant, ownership and column snapshots are identical before and after
    And each file is named V<next>__rwb_p1_e1069_<name>.sql with the header line "-- Story: RWB-P1-E1069-DB"
    And no file holds a "${recoverySchema}" token, an environment name or a monolith version number, and no U*.sql or down script exists
    # TC-E1-069-19

  Scenario: AC9 Only one service login reads the views
    Given the grants are applied in SIT, UAT or PROD
    When login rwb_case selects recovery.v_ace_account
    Then it fails with SQLSTATE 42501
    And the only grantees of each view are its owner ace_view_owner and rwb_source_data
    And rwb_sandbox_read holds no grant outside DEV; in DEV and pipeline test it is the one documented exception of Security and Access Design v6
    # TC-P1-E1069-DB-01

  Scenario: AC10 No indirect read path exists
    Given the 19 service logins
    When role memberships and PUBLIC privileges are listed
    Then no service login is a member of ace_view_owner or pg_read_all_data
    And PUBLIC holds no privilege on any view or extension table
    # TC-P1-E1069-DB-02

  Scenario: AC11 The service login has the ruled DML on the extension tables
    Given the extension tables are created by the service migrator and are not owned by rwb_source_data
    When rwb_source_data inserts, selects and updates a synthetic row in each table
    Then each statement succeeds
    When rwb_source_data deletes that row, or rwb_case selects party_ext
    Then the statement fails with SQLSTATE 42501
    # TC-P1-E1069-DB-03

  Scenario: AC12 A bad contact type is refused
    Given contact_point_ext
    When a row is written with contact_type "FAX", "phone" or ""
    Then it fails with SQLSTATE 23514, a null contact_type fails with SQLSTATE 23502 and no row is written
    And rows with PHONE, EMAIL and ADDRESS are accepted
    # TC-P1-E1069-DB-04

  Scenario: AC13 Column defaults
    Given an insert of the primary key only, plus contact_type for contact_point_ext
    When the row is read back
    Then the boolean flags are false, is_active is true, version is 1, failed_count is 0, source is "WORKBENCH" and created_at and updated_at are set
    # TC-P1-E1069-DB-05

  Scenario: AC14 A grant before its view changes nothing
    Given a database without the Section A views
    When the Section A grant file runs
    Then it fails on the missing relation, the transaction rolls back and no grant, role change or applied history row remains
    # TC-P1-E1069-DB-06

  Scenario: AC15 A missing login stops the grant
    Given login rwb_source_data does not exist
    When the Section A grant file runs
    Then it fails naming the role, no grant remains and no login is created
    # TC-P1-E1069-DB-07

  Scenario: AC16 An existing table stops the table migration
    Given party_ext already exists
    When the extension-table migration runs
    Then it fails with SQLSTATE 42P07, none of the other three tables is created and nothing is recorded as applied
    # TC-P1-E1069-DB-08

  Scenario: AC17 Section B is held until the ACE dependency gate passes
    Given RWB-ACE-001 has not landed in SIT
    When the deployment runs
    Then no Section B grant is applied, the Section A grants are unchanged and the Section B flags stay off
    # TC-P1-E1069-DB-09

  Scenario: AC18 Section B grants after the Section B views
    Given the 14 Section B views over tier2-ddl.sql in DEV or pipeline test, or over RWB-ACE-001 after the gate
    When the Section B grant file runs
    Then ace_view_owner owns the 14 views and holds SELECT and no write on the 14 Tier 2 tables
    And rwb_source_data selects 14 of 14 views and PUBLIC holds nothing on them
    # TC-P1-E1069-DB-10

  Scenario: AC19 An edited applied migration is refused
    Given an applied file of this story is edited
    When Flyway validate runs
    Then it fails with a checksum mismatch naming the version and no statement runs
    # TC-P1-E1069-DB-11

  Scenario: AC20 A wrong grant is corrected by a forward version
    Given SELECT on recovery.v_ace_account was granted to rwb_case by mistake
    When the corrective version revokes it
    Then has_table_privilege('rwb_case', 'recovery.v_ace_account', 'SELECT') is false
    And the SELECT grants to rwb_source_data are unchanged
    # TC-P1-E1069-DB-12
```

AC1 to AC20 prove only the database artefacts in the story title: the grants, the view owner, the four extension tables and the schema boundary. No legacy acceptance criterion text is repeated here. The legacy criteria these grants and tables answer are AC1, AC2, AC3, AC4 and AC7 of RWB-E1-069 — the view sets and their compilation, the read-only role, the constraint rule and the four extension tables — and they are proven end to end across the 19 real logins in RWB-ITG-E1069-ITG; AC5, AC6 and AC8 of the legacy story are the dictionary, the delay-day mapping and the build rule, and they belong to RWB-P1-E1069-APP.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | rwb-source-data reads ACE source data only through the 30 SELECT-only `recovery.v_ace_*` views: 16 now over tables ACE holds, 14 when RWB-ACE-001 lands. It loads, copies and transforms nothing | D-RCV-35 U1, U4; ADR-010; D-RCV-60 |
| BR2 | A view is owned by `ace_view_owner`, which is NOLOGIN, holds SELECT on the ACE tables it reads and writes nothing. After a migration it holds no right in schema `recovery` other than the views it owns | D-RCV-35 U4; CTL-02 |
| BR3 | On ACE source data the `rwb_source_data` login holds SELECT on the views and no table privilege in `public`; PUBLIC holds nothing; no write is granted on a view; no other service login holds a view privilege (`rwb_sandbox_read` is a DEV-only exception). On the four extension tables the login holds SELECT, INSERT and UPDATE and no DELETE | D-RCV-35 U4; D-RCV-60; Security and Access Design v6; RD-P1-048; CTL-02 |
| BR4 | No constraint in schema `rwb_source_data` or schema `recovery` references a table or a type outside it. A link to an ACE record is a `varchar(255)` business-key column with no foreign key, because ACE cascades deletes on `account` | D-RCV-35 U4; BR-P1-001-3; ADR-010 |
| BR5 | Every view carries one `sys_objects` row and one `sys_fields` row per column, with the ACE source field and the data product | BR-P1-001; RWB-E1-064 |
| BR6 | A text date in ACE becomes a date through `recovery.ace_to_date`, and a Y/N flag becomes a boolean through `recovery.ace_to_boolean`; both return NULL rather than fail a read | BR-P1-001-7 |
| BR7 | An extension table holds a Workbench decision about an ACE record and never a copy of an ACE column. It is 1:1 with the ACE record on the ACE business key and carries the seven standard record columns | BR-P1-001-5 |
| BR8 | Boundary rule BND-6: no recovery class names a table in schema `public`; the only source objects it may name are the 30 `recovery.v_ace_*` views, read from the module map | REQ-DRI-006; RWB-TE-001 |
| BR9 | A Section B grant is applied only after its ACE table exists: in DEV and pipeline test over `tier2-ddl.sql`, elsewhere after the ACE dependency gate; until then the feature that reads it stays behind its flag | ADR-010; DL43; RD-P1-043 |
| BR10 | Migrations are forward-only: Pending, Applied or Failed; each file names its corrective forward script; no undo file or down script exists | RD-P1-045; RWB-PLT-E1044-CON |

**Rule coverage.** BR1: AC2 and AC9. BR2: AC4 and AC18. BR3: AC2, AC3, AC9, AC10 and AC11. BR4: AC7. BR7: AC5, AC6 and AC13. BR9: AC17 and AC18. BR10: AC8, AC19 and AC20. BR5 is delivered by RWB-P1-E1001-APP; BR6 and BR8 are delivered by RWB-P1-E1069-APP.

**Where each rule lives in the target.** BR2, BR3 and BR7 are this story's: the ownership, the grant set and the four tables are the objects it creates and the statements it runs, and the login of BR3 is the `rwb_source_data` login of the target (DP-02; Architecture v5 slides 11 and 29). BR4 is split by schema — the constraint scan over `rwb_source_data` runs here, the scan over schema `recovery` and over the 19 `rwb_*` schemas runs in RWB-P1-E1069-APP and RWB-ITG-E1069-ITG. BR1 and BR5 are asserted here and delivered elsewhere: the view SQL is RWB-P1-E1069-APP's and the dictionary rows are RWB-P1-E1001-APP's. BR6 is delivered by the helper functions of the Section A migration, in RWB-P1-E1069-APP. BR8 is a build rule and lives in that story's build, not in the database. BR9 is the order in which the Section B grants are applied, and this story is the one that applies them.

The grant checks of the legacy 'Read-only ACE grant' test sit with this P1 DB slice; the view conformance test is RWB-P1-E1069-APP's. The P4 slice keeps the role and masking checks, and the per-service boundary test is the cross-schema check.

**Decision DL43.** The recommended answer A (yes, the scope and dates as in RWB-ACE-001) is the planning basis; the ACE team lead keeps the decision (RD-P1-043). ASM-0193, ASM-0737, ASM-0748 and ASM-0816 are confirmed. This does not report RWB-ACE-001 as deployed: BR9 and the Tier 2 precondition of section 3 still apply.

**Schema split (GAP-0557; ASM-0794 to ASM-0798, confirmed).** The as-built migration `V0001__rwb_e1_001_recovery_schema.sql` in schema `recovery` is kept as built and is not rewritten; it is not the service baseline of this sequence. P1's own tables and the dictionary seed come from one new Flyway file of RWB-P1-E1001-APP on the rwb-source-data sequence, after the service baseline. The schema and the login are both `rwb_source_data`. This story creates the four extension tables; RWB-P1-E1001-APP seeds their 49 dictionary fields DF-EXT-001 to DF-EXT-049 and creates none of these tables. The data product catalog, the dictionary tables and the `v_data_dictionary` read model stay in `rwb_source_data`, and this story adds no REST operation.

### 9. State transitions

A table has no state machine and this story changes no business row. The states are the migration states of the service Flyway history: Pending, Applied and Failed. There is no undone state (RD-P1-045).

| Item | States |
|---|---|
| a migration of this story | Pending, Applied, Failed; an applied version is never edited; a correction is a new forward version |
| the login | Present and granted, or absent and the grant fails naming it; never a member of ace_view_owner or a predefined read role |
| a grant | Held on a view or a table, or refused with SQLSTATE 42501; a PUBLIC grant is a failure |
| an extension row | One row per ACE key, or the second row refused with SQLSTATE 23505 |
| a constraint | Inside `rwb_source_data`, or a reference outside it, which is a failure that blocks the merge |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The ACE database engineer (any team, per U3) | Writes and runs the migration set, the grant migrations and the schema checks |
| ACE team lead and ACE DBA | Own schema `public`; approve the 21 Tier 1 table list and grant SELECT to `ace_view_owner` (RWB-ACE-001); supply the ACE DBA role for the release window |
| Recovery tech lead and data architect | Approve a change to the 30-view list, which is frozen in the ACE Data Tier Map v1, and to the grant list |
| Service migrator `rwb_source_data_migrator` (RWB-PLT-N011-DB) | Applies the extension-table migration; holds no right in `public` or `recovery` |
| Privileged database principal (Pending, NEW-GAP-S7-05) | Applies the role creation, the grants on `public` and `recovery` and the ownership changes |
| rwb-source-data owner (RWB-P1-E1069-APP) | Owns the view SQL and the read contract that run on these grants; writes no grant of its own |
| Platform DB owner (RWB-PLT-NF06-DB) | Owns the 19 schemas, the 19 logins and the credential policy |
| RW-PLATADM, platform administrator | Reads the deployment result in the release pipeline; may not change a grant |
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

The dictionary rows are metadata of rwb-source-data delivered with RWB-P1-E1001-APP: LDM v11 holds `DF-EXT-001` to `DF-EXT-050` (the fiftieth is `contact_point_ext.person_key`, added by RWB-P1-E2022-APP) and 304 view fields (177 Section A, 127 Section B). This story writes none of them.

Classification (Data Classification and Personal Data Inventory v6): `party_ext.vulnerable`, `deceased_override` and `bankruptcy` are Sensitive and Restricted; `person_key` is an indirect identifier, Confidential; `fraud_flag` is Confidential. Direct access to these tables is limited to the grants of section 13, copies outside production hold synthetic or masked values only, and no test uses production data.

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
| `recovery_views.sql` of Physical Schema v9 | The view definitions and the single-reader grants block | The grant files name the views from this list and grant on no other object |
| Delivered-views fixture | RWB-P1-E1069-APP | A container with the baseline, schema `recovery`, the views and the three helper functions, so the grants are tested against the real views |
| ACE head fixture | ACE Schema PostgreSQL v1.sql | The 21 Tier 1 tables the view owner is granted on |
| `tier2-ddl.sql` | RWB-P1-E1065-CON | Section B tables in DEV and pipeline test |
| No-grant role | The test role `rwb_no_grant`, created and dropped by the test | AC2 |

A database story uses no service contract fake; the fixtures above stand in for the neighbouring stories and for the ACE head.

**12.9 Call-type summary**

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | None | None | No operation in this story |
| Kafka | None | None | No topic in this story |
| Temporal | None | None | No workflow, activity or Schedule |
| File | None | None | Migrations are deployed by the release pipeline, not by a file interface |
| SQL view | 30 `recovery.v_ace_*` views, SELECT granted to the `rwb_source_data` login | The 21 Tier 1 tables and the 14 Tier 2 tables, read by `ace_view_owner` through the views only | SQL only: SELECT, never a write, and no statement in this story reads another service's schema |

### 13. Solution plan

**Sequencing.** The files sit on the rwb-source-data Flyway sequence (DP-15); version numbers are assigned by the sequence owner at build time. Files follow `V<next>__rwb_p1_e1069_<name>.sql` with the header line `-- Story: RWB-P1-E1069-DB` (RD-P1-045). One executing identity per file.

| Order | File | Executing identity | Contents | Corrective forward script |
|---|---|---|---|---|
| baseline | RWB-P1-E1001-APP and platform | platform | Schema `rwb_source_data` and its tables | not this story |
| 1 | `V<next>__rwb_p1_e1069_extension_tables.sql` | service migrator | The four extension tables and their DML grants | a new version; an empty table is dropped only before any row and with the release owner's approval |
| 2 | RWB-P1-E1069-APP Section A views | as NEW-GAP-S7-05 | Helper functions and 16 views | RWB-P1-E1069-APP |
| 3 | `V<next>__rwb_p1_e1069_section_a_grants.sql` | privileged principal (NEW-GAP-S7-05) | Role, `public` grants, ownership, view grants, PUBLIC revoke | REVOKE or ALTER VIEW OWNER in a new version |
| 4 | RWB-P1-E1069-APP Section B views | as NEW-GAP-S7-05 | 14 views | RWB-P1-E1069-APP |
| 5 | `V<next>__rwb_p1_e1069_section_b_grants.sql` | privileged principal (NEW-GAP-S7-05) | Tier 2 grants, ownership, view grants | REVOKE or ALTER VIEW OWNER in a new version |

In DEV and pipeline test all five positions apply in this order over the fixture. In SIT, UAT and PROD positions 4 and 5 are applied only after the ACE dependency gate (RD-P1-043). Pending: how the pipeline holds positions 4 and 5 back without blocking later versions on the sequence, owner platform sequence owner, tracked as NEW-GAP-S7-06. The legacy file names `V0002__rwb_e1_069_ace_source_views.sql` and `V0003__rwb_e1_069_ace_tier2_views.sql` are the source of the objects only and are not reused.

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

**Grant block (Section A)**

```sql
-- run by the privileged principal (NEW-GAP-S7-05), one transaction
DO $$ BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'ace_view_owner') THEN
    CREATE ROLE ace_view_owner NOLOGIN;
  END IF;
END $$;

GRANT USAGE ON SCHEMA public TO ace_view_owner;
GRANT SELECT ON public.account, public.payment, public.customer, public.phone, public.email,
     public.address, public.ca_relation, public.aa_relation, public.collateral, public.asset,
     public.efs_action, public.efs_action_code, public.efs_assignment,
     public.bucket_log_snapshot, public.product, public.branch, public.bot_holiday,
     public.ace_case, public.cfsc_mg_ssme_tdr_case, public.tdr_calculation,
     public.ai_recommended_plan
     TO ace_view_owner;

-- ownership change: run by a superuser, or GRANT CREATE ON SCHEMA recovery TO ace_view_owner first and REVOKE it at the end of the transaction
ALTER VIEW recovery.v_ace_account OWNER TO ace_view_owner;
-- one ALTER VIEW OWNER statement for each of the 16 views

GRANT USAGE ON SCHEMA recovery TO rwb_source_data;
GRANT SELECT ON recovery.v_ace_account TO rwb_source_data;
-- one GRANT per view, 16 in the Section A grant and 30 in all; never GRANT SELECT ON ALL TABLES IN SCHEMA recovery

REVOKE ALL ON ALL TABLES IN SCHEMA recovery FROM PUBLIC;
```

The extension-table migration, run by the service migrator, adds:

```sql
GRANT SELECT, INSERT, UPDATE ON rwb_source_data.party_ext TO rwb_source_data;
GRANT SELECT, INSERT, UPDATE ON rwb_source_data.contact_point_ext TO rwb_source_data;
GRANT SELECT, INSERT, UPDATE ON rwb_source_data.account_ext TO rwb_source_data;
GRANT SELECT, INSERT, UPDATE ON rwb_source_data.valuation_ext TO rwb_source_data;
```

The Section B grant adds, after the Section B views (in DEV and pipeline test over the fixture; elsewhere after the ACE dependency gate, where the table grant is already made by RWB-P1-ACE001-DB and is repeated harmlessly):

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

No `GRANT ... ON ALL TABLES` appears in any migration that touches the views, PUBLIC receives nothing, and the login receives no write privilege on a view and no table privilege in `public`.

**Table definitions** (Physical Schema v9 `rwb_source_data.sql`, without the columns later stories add)

- `party_ext`: `person_key` varchar(255) primary key, `vulnerable`, `deceased_override`, `bankruptcy`, `fraud_flag` boolean NOT NULL DEFAULT false, `is_active` boolean NOT NULL DEFAULT true, `state` varchar(40), `version` integer NOT NULL DEFAULT 1, `created_at` and `updated_at` timestamptz NOT NULL DEFAULT now(), `created_by` and `updated_by` uuid.
- `contact_point_ext`: `contact_key` varchar(255) primary key, `contact_type` varchar(10) NOT NULL, `consent_given` boolean NOT NULL DEFAULT false, `consent_at` and `verified_at` timestamptz, `failed_count` integer NOT NULL DEFAULT 0, `source` varchar(20) NOT NULL DEFAULT 'WORKBENCH', `is_active`, `state`, `version`, `created_at`, `created_by`, `updated_at`, `updated_by`, and the check `ck_contact_point_ext_type` that `contact_type` is PHONE, EMAIL or ADDRESS.
- `account_ext`: `account_key` varchar(255) primary key, `dispute_open` boolean NOT NULL DEFAULT false, `is_active`, `state`, `version`, `created_at`, `created_by`, `updated_at`, `updated_by`.
- `valuation_ext`: `valuation_key` varchar(255) primary key, `accepted` boolean NOT NULL DEFAULT false, `accepted_at` timestamptz, `accepted_by` and `valuer_partner_id` uuid, `stale_flag` boolean NOT NULL DEFAULT false, `age_days` integer, `is_active`, `state`, `version`, `created_at`, `created_by`, `updated_at`, `updated_by`.

The four tables hold 49 columns in all, which are the 49 fields `DF-EXT-001` to `DF-EXT-049`. The primary key of each is the ACE business key: there is no `id` column and there is no foreign key into `public`, and `valuer_partner_id` carries no foreign key (TSD P1 T3.5).

**Schema privileges and revokes.** The login owns schema `rwb_source_data` (RWB-PLT-NF06-DB). Schema ownership gives no table privilege, so the table grants above are explicit. On the ACE side the login holds USAGE on schema `recovery` and SELECT on each applied view, and no table privilege in `public` (schema USAGE that PostgreSQL gives through PUBLIC is not asserted), no write on a view and no grant on another service schema. In DEV and pipeline test `rwb_sandbox_read` of RWB-P1-E1065-DB may select the views; it holds nothing outside DEV (Security and Access Design v6). No migration of this story grants anything to PUBLIC.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `V<next>__rwb_p1_e1069_extension_tables.sql` | Migration | The four extension tables, keys, standard record columns, `ck_contact_point_ext_type` and the DML grants |
| `V<next>__rwb_p1_e1069_section_a_grants.sql` | Migration | `ace_view_owner`, the 21 Tier 1 tables, the 16 view owners, the login SELECT on the 16 views, the PUBLIC revoke |
| `V<next>__rwb_p1_e1069_section_b_grants.sql` | Migration | The 14 Tier 2 tables, the 14 view owners and the login SELECT on the 14 views |
| `SchemaBoundaryCheck` | Pipeline check | No constraint in `rwb_source_data` names a schema outside it; every ACE link is `varchar(255)` with no foreign key |
| `GrantCheck` | Pipeline check | Login grants, ownership, memberships, PUBLIC, the other service logins and the refusals with SQLSTATE 42501 |
| `ExtensionKeyCheck` | Pipeline check | The four tables' columns, primary keys, the check, the 49 field IDs and the duplicate-key refusal |

**Build steps**

1. The extension-table migration with its grants, and fixtures for an existing table, a duplicate key, a bad contact type and the defaults (AC5, AC6, AC11, AC12, AC13, AC16).
2. The Section A grant file with the role guard, the 21 table grants, the 16 ownership changes, the 16 SELECT grants and the PUBLIC revoke; fixtures for a missing view and a missing login (AC1 to AC4, AC14, AC15).
3. The Section B grant file, wired to the Section B gate of RD-P1-043 (AC17, AC18).
4. `SchemaBoundaryCheck` with a fixture foreign key to `public.account` (AC7).
5. `GrantCheck` as a container test with sessions as the login and `rwb_case`, membership queries and the test role `rwb_no_grant` (AC2, AC3, AC9, AC10, AC20).
6. A repeated-run and edited-file test of the whole set (AC8, AC19).
7. The release note with version numbers, checksums and corrective scripts.

**Done when.** AC1 to AC20 pass; in DEV and pipeline test both sections are applied; in SIT, UAT and PROD Section A is applied and accepted on its own, and Section B waits for the ACE dependency gate.

### 14. Validation and messages

| ID | When | Result |
|---|---|---|
| Grant check | A role holds a privilege the grant matrix does not give | {role} holds {privilege} on {object} |
| Boundary check | A constraint references an object outside the schema | {constraint} references {object}; no constraint in rwb_source_data may reference another schema |
| SQLSTATE 42501 | A select without the privilege, such as the service login on public.account | PostgreSQL insufficient privilege; assert the SQLSTATE, not the server text |
| SQLSTATE 55000 or 42501 | A write on a view | The statement is refused; no row changes |
| SQLSTATE 23505 | A second row for one ACE key | Names the primary key of the table |
| SQLSTATE 23514 or 23502 | A bad or null contact type | The write is refused |
| SQLSTATE 42P07 | An extension table already exists | The migration fails |

These are pipeline and database results for developers; no `MSG-` ID applies and no user-facing message is raised by this story. The legacy texts that carry `recovery_svc` or `fk_case_account_account_key` are not used.

### 15. Screens and states

No screen. The result of a migration is visible in the release pipeline and in the service Flyway history (Pending, Applied, Failed, each with version and checksum). This story feeds no SCR-44 panel; any screen state belongs to the story that builds that screen.

### 16. Test cases

| Acceptance criteria | Test case (Test Cases v9) |
|---|---|
| AC1 | TC-E1-069-12 |
| AC2 | TC-E1-069-13 |
| AC3 | TC-E1-069-14 |
| AC4 | TC-E1-069-15 |
| AC5 | TC-E1-069-16 |
| AC6 | TC-E1-069-17 |
| AC7 | TC-E1-069-18 |
| AC8 | TC-E1-069-19 |
| AC9 to AC20 | TC-P1-E1069-DB-01 to -12 |

The legacy rows TC-E1-069-01 to -08 are not evidence for this story: Test Cases v9 uses those IDs for the criteria of RWB-P1-E1069-APP. The data of TC-E1-069-12 to -19 follows the revised criteria in the test case update.

### 17. Guardrails

- No business value in a constraint: the check `ck_contact_point_ext_type` is business-neutral and comes from the legacy physical schema; every other business value, the masking answer and the authorise decision are data read by the application, not constants in a migration.
- No real personal data in a migration, a script, a test fixture or a runbook: test keys such as `P0000123` and `ACC0000017` are synthetic. `party_ext` holds Sensitive columns (vulnerable, deceased_override, bankruptcy): access only through the grants of section 13, and copies outside production are synthetic or masked.
- No read of another schema and no key into another schema: `rwb_source_data` objects reference `rwb_source_data` objects only, and a key to `public.account` is forbidden because ACE cascades deletes on `account` (DP-01, BR4).
- One login per service: `rwb_source_data` is the only service login granted on the views; `rwb_sandbox_read` exists as a DEV-only exception and no other grant exists (DP-02; D-RCV-60).
- No DELETE on the extension tables (RD-P1-048) and no undo or down script (RD-P1-045).
- No write path into ACE data: no INSERT, UPDATE, DELETE or TRUNCATE is granted on a view, and the four extension tables hold Workbench decisions only.
- No privilege for PUBLIC anywhere, and no `GRANT ... ON ALL TABLES` in any migration that touches the views.
- The schema is the fixed `recovery`: no `${recoverySchema}` token and no environment name survives in a migration (DP-15).
- An applied migration is never edited: a correction is a new version, and a wrong grant is revoked by a later version, never by an edit.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | Rules | Test cases |
|---|---|---|---|---|---|
| REQ-RDF-002 | Account balance, arrears, payments and classification for every account at 90 or more days past due are read from ACE through `v_ace_account` and `v_ace_payment`, current to the previous working day | Business Requirements Epic 1, sections 3.1 and 4 | FEAT-RDF-01 | D-RCV-35 U4; BR-P1-001-2; BR-P1-001-3; BR-P1-001-4 | TC-E1-069-12 to -15, TC-E1-069-19 |
| REQ-DRI-006 | No component calls a system of record directly | Business Requirements Program, sections 5.2 and 7 | FEAT-RDF-01 | ADR-010; DL43; BR-P1-001-3 | TC-E1-069-18 |

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

| Reference | Use |
|---|---|
| RD-P1-021 | P1 table ownership; the extension tables are P1's |
| RD-P1-043 | Section B build fixture and ACE dependency gate |
| RD-P1-045 | Forward-only migrations and corrective scripts |
| RD-P1-046 | Shared sandbox and its DEV-only read role |
| RD-P1-048 | Extension tables are REVIEW only for retention, so no DELETE is granted |
| NEW-GAP-S7-05; NEW-GAP-S7-06 | Privileged principal; Section B hold-back on the sequence |
| GAP-1509; GAP-0568; GAP-3156 | Stale writer; credential and grant list; legacy grant block |

### 19. Out of scope

- The view SQL of the 16 Section A and 14 Section B views, the three helper functions and the view conformance test: RWB-P1-E1069-APP.
- The ACE read contract, the authorise-and-mask hop and the read path of the other 18 services: RWB-P1-E1069-APP.
- The proof of the grant matrix across the 19 logins and the second half of boundary rule BND-6 (no `v_ace_*` view named outside rwb-source-data, no other service's schema named): RWB-ITG-E1069-ITG.
- The 14 Tier 2 tables and the 12 columns that RWB-ACE-001 adds to `account`, `customer` and `efs_action`: the ACE team owns them, and this story neither creates nor alters them.
- The masking policy rows and the masking answer: rwb-access, RWB-P4-E1069-APP (DP-08).
- The dictionary content and its maintenance: RWB-P1-E1001-APP for the metadata rows and RWB-E1-064 in the legacy set for the dictionary of the 14 data products.
- The application code, the read operations and the response shape: RWB-P1-E1069-APP.
- The freshness stamp, the reconciliation, the data products and the business-day operations: the other P1 stories, among them RWB-P1-E1015-APP. P1 holds no case list (RD-P1-024).
- The login, the schema and their credential: RWB-PLT-NF06-DB; the SELECT grant on the 14 Tier 2 tables in ACE environments: RWB-P1-ACE001-DB.
- Any change to the 30-view list or to the grant list: the data architect and the recovery tech lead, with a new version of the ACE Data Tier Map v1.
- Performance tuning beyond the primary keys named here: the non-functional work.

### 20. Remaining delivery steps

- Size: Not specified (DOR-RWB-P1-E1069-DB-16); owner squad lead at refinement.
- Epic design sign-off: Pending; owner product owner and design authority.
- Privileged principal for the grant files (NEW-GAP-S7-05) and Section B hold-back (NEW-GAP-S7-06): owner ACE DBA, platform DB owner and sequence owner.
- Test data in DEV: Pending shared sandbox and tier2-ddl.sql fixture load; owner platform DB owner and QA.
- Test cases: rows for AC9 to AC20 and update of TC-E1-069-12 to -19; owner QA lead.
