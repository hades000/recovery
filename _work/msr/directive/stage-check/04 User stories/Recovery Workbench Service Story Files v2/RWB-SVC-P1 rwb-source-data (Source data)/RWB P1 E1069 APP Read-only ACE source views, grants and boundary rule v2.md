# RWB-P1-E1069-APP Read-only ACE source views, grants and boundary rule

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P1-E1069-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-source-data |
| Service epic | RWB-SVC-P1 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-069 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Not specified in the source documents (DOR-RWB-P1-E1069-APP-16); sized by the squad at refinement |
| Patterns applied | DP01, DP02, DP03, DP05, DP06, DP07, DP08, DP11, DP15, DP19 |
| Parallel lane | L-P1-A |
| Ready to start | After RWB-P1-E1001-APP, RWB-P1-ACE001-DB, RWB-P1-E1069-DB |
| Depends on (build) | RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1037-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON, RWB-P1-E1001-APP, RWB-P1-ACE001-DB |
| Contract dependencies | RWB-P3-E1042-CON, RWB-P3-E1043-CON, RWB-P4-E1037-CON |
| Integration dependencies | None |
| External dependencies | RWB-P1-E1069-DB |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v1.md (FR-P1-001, FR-P1-002, FR-P1-005) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-069 for rwb-source-data. The 30 `recovery.v_ace_*` views stay in schema `recovery` with `ace_view_owner` as their owner and are read by the `rwb_source_data` login only (DP-02, DP-05; Architecture v5 slides 11 and 29); the view SQL, the conformance test and the ACE read contract move to this story, the login, the grant block and the four extension tables to RWB-P1-E1069-DB, and the proof across the 19 logins to RWB-ITG-E1069-ITG. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P1-E1069-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (18 resolved, 35 cross-document, 3 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **recovery developer (RW-TRIBE)**, I want **the 30 SELECT-only `recovery.v_ace_*` views created on rwb-source-data's own migration sequence, the view conformance test that fails the build on a compile error, a constraint into `public`, a missing dictionary row or a grant outside the views, the ACE read contract that every other service and every agent calls, and the authorise-and-mask hop that every read takes before it returns an ACE-sourced field**, so that **there is one copy of source data, the Workbench cannot alter or copy it, and a direct read of an ACE table fails in the database and in the build**.

This is the application slice of legacy RWB-E1-069. It owns:

- the view SQL of the 16 Section A and 14 Section B views, taken from `recovery_views.sql` of the Physical Schema folder, and the two migrations that apply them on rwb-source-data's per-service Flyway sequence (DP-15);
- the view conformance test of the legacy story, with its four checks and its named failures;
- the ACE read contract served over the views on base `/api/recovery/source-data/v1` (DP-05, DP-11, DP-13): `GET /customers/{id}`, `GET /accounts/{id}` and `GET /collateral/{id}`;
- the authorise-and-mask hop of DP-08 to rwb-access (P4) that every read takes once, one hop, 2 s timeout, before a field is returned;
- the read path that every other service and every agent calls, and boundary rule BND-6 over this service's own package, with the 30 view names as the only allowed source objects.

It does not create the `rwb_source_data` login, the `GRANT` statements, the view owner `ace_view_owner` or the four extension tables: they are RWB-P1-E1069-DB (external dependency X). It does not prove the grant matrix across the 19 logins, or the second half of boundary rule BND-6 outside this service: that is RWB-ITG-E1069-ITG. It creates no table of its own, and it reads no table of another service (DP-01).

### 2. Business rationale

The Workbench takes no inbound source data. ACE ingests every source, and the recovery module reads it through 30 SELECT-only views: 16 over the ACE tables that exist today, 177 fields, and 14 over the tables RWB-ACE-001 adds, 127 fields, 304 in all. The views are owned by a dedicated role that holds SELECT on the ACE tables; the service login holds SELECT on the views and no privilege on anything in `public`. PUBLIC holds no privilege, and no write is granted on a view. The Workbench keeps its own decisions about an ACE record in four extension tables keyed by the ACE business key, never in a copy of an ACE column (legacy RWB-E1-069 §2).

In the target the boundary is enforced in three places instead of two. The catalog refuses a direct `public` read, because only the `rwb_source_data` login holds SELECT on the views and no login holds anything in `public` (Architecture v5 slides 8, 9, 11 and 29; ADR-010). Boundary rule BND-6 fails this service's build when a class of `th.co.scb.ace.workbench.recovery.sourcedata` names a `public` table. And every other service reaches ACE data only through this story's read contract, because only rwb-source-data reads the views at all (Architecture v5 slides 8, 9, 13, 41 and 45; DP-05, DP-11), so a change in ACE is absorbed in one place instead of nineteen.

Serves REQ-RDF-002 (account balance, arrears, payments and classification read from ACE through `v_ace_account` and `v_ace_payment`) and REQ-DRI-006 (no component calls a system of record directly); applies DP-01, DP-02, DP-05, DP-08 and DP-11 and ADR-010. The measure is 100 percent of pipeline runs in which every view compiles and the conformance test passes (FSD P1 A2.1.1).

### 3. Preconditions

- RWB-P1-E1001-APP is done: the `rwb_source_data` baseline holds P1's tables, the dictionary rows in `sys_objects` and `sys_fields`, the view `v_data_dictionary` and the data product rows (legacy RWB-E1-069 §3, RWB-E1-001 in the target).
- The per-service Flyway sequence of rwb-source-data exists with its own history table in schema `rwb_source_data`, and the baseline version has been applied on it (DP-15; RWB-PLT-E1044-CON).
- The ACE schema in DEV and SIT is at the head that holds the 21 Tier 1 tables of section 11, among them `account`, `payment`, `customer` and `efs_action` (ACE Schema PostgreSQL v1.sql; legacy RWB-E1-069 §3).
- The recovery migration account holds the ACE DBA role for the release window, so it can create a view in schema `recovery` and set a view owner (RWB-E1-044; legacy RWB-E1-069 §3).
- The roles `ace_view_owner` and the login `rwb_source_data` exist in DEV and SIT, with the grant block delivered by RWB-P1-E1069-DB as a commented template (its placeholders :recovery_role and :ace_view_owner are not role names, and the template creates no logins); the 19 schemas and logins come from RWB-PLT-NF06 and the migrator roles from RWB-PLT-N011 (DP-02; Architecture v5 slides 11 and 29).
- The Section B views (`V0003`, 14 Tier 2 tables) and the batch-status freshness source stay behind their feature flags until RWB-ACE-001 lands; the fallback freshness source (CG-9) is confirmed before system test (GAP-1505).
- The view definitions are available in `recovery_views.sql` of the Physical Schema folder; a view definition is copied from there and never rewritten by hand (legacy RWB-E1-069 §13).
- The module map of the service template is in the repository, and `recovery-modules.yaml` holds `sourceViews`, the 30 view names that BND-6 allows (legacy RWB-E1-069 §4 step 5; RWB-TE-001 in the target).
- RWB-P4-E1037-CON is published and the rwb-access guard library is on the classpath, so the authorise hop of DP-08 runs against the published contract and its fake from Day 1 (`POST /api/recovery/access/v1/authorise`, one hop, 2 s).
- RWB-P3-E1042-CON and RWB-P3-E1043-CON are published with their client libraries, so a parameter and a list of values are read as data and never as a constant (DP-06, DP-07).
- For the 14 Section B views only: RWB-ACE-001 is deployed in DEV and SIT and its 14 Tier 2 tables exist (DL43; the build dependency RWB-P1-ACE001-DB). Until then the features that read a Section B view stay behind their flags.
- The split of this legacy key across three stories, and the position of the two view migrations on the service sequence, are Not specified in the source documents (GAP-0566; ASM-0807); the maker of every view definition and its checksum come from `recovery_views.sql`.
- The appraisal age rule is held as data: an appraisal more than 365 days old at the business date is stale. Until the owning function is assigned, this story writes `valuation_ext.stale_flag` (DF-EXT-041) and `valuation_ext.age_days` (DF-EXT-042) as the only writer (FSD P1 OQ-P1-05 and A2.6; ASM-A6-tables-15).
- The account and arrears read is the four views keyed by `account_key` at the ACE business date, answered in the field order of the field IDs; a late case is answered from `v_ace_batch_status` and MSG-P1-001 with no parameter read. The per-source cut-off is revisited only when it is agreed as a rwb-case parameter.

### 4. Flow

1. Recovery developer: takes the 16 Section A view definitions and the three helper functions `recovery.ace_to_date`, `recovery.ace_to_boolean` and `recovery.ace_mask_value` from `recovery_views.sql` into the Section A migration of the service sequence, and writes no environment name in the file: the schema is the fixed `recovery` and the two role names come from the Environment and Deployment Design (TSD P1 T3.2; legacy RWB-E1-069 §4 steps 1 and 2).
2. Recovery developer: adds the second view migration for the 14 Section B views, and one SELECT grant per view is issued by RWB-P1-E1069-DB, not here (legacy RWB-E1-069 §4 step 7).
3. Pipeline: applies the baseline, then the Section A migration in DEV and then in SIT, on the service's own sequence (DP-15).
4. Pipeline: runs `ViewConformanceTest`: every view compiles, no constraint in schema `recovery` references `public`, every view has one `sys_objects` row and one `sys_fields` row per column, and the service login holds no privilege in `public` and no write on a view (legacy RWB-E1-069 §4 step 4).
5. Recovery developer: writes boundary rule BND-6 over the package of this service and adds the 30 view names to `recovery-modules.yaml` as the only allowed source objects (legacy RWB-E1-069 §4 step 5).
6. ACE team: applies RWB-ACE-001 with the 14 Tier 2 tables, and its migration grants SELECT on those tables to `ace_view_owner` (DL43, assumptions ASM-0193, ASM-0737, ASM-0748 and ASM-0816; tracked in RWB-P1-E1069-DB).
7. Pipeline: applies the Section B migration in DEV and SIT after RWB-ACE-001 is reported deployed; 30 of 30 views compile and the features that read a Section B view come out from behind their flags (legacy RWB-E1-069 §4 step 8).
8. Recovery developer: serves the three read operations on `/api/recovery/source-data/v1` from `AceSourceReadRepository`, each one a SELECT on a view and nothing else; every read calls `POST /api/recovery/access/v1/authorise` once with the caller identity, the area, the right and the field IDs it is about to return, and returns the field clear or masked as answered (DP-08, DP-11).
9. Every other service and every agent reaches ACE data in step 8 and never in a view of its own (Architecture v5 slides 13, 41 and 45); a service that names a view fails its own boundary rule in RWB-ITG-E1069-ITG.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A Section A view does not compile | The Section A stage of the service sequence rolls back; no view from that run exists; the step names the view and the ACE column | Pipeline log: v_ace_account does not compile: column a.core_banking_system_date does not exist | AC1 |
| X2 | The Section B migration is applied before RWB-ACE-001 | The stage fails; no Section B view is created; the 16 Section A views and their features are unchanged | Pipeline log: relation public.valuation does not exist | AC3 |
| X3 | A recovery constraint references a table in `public` | The conformance test fails and the merge is blocked | fk_case_account_account_key references public.account; no constraint in recovery may reference another schema | AC4 |
| X4 | A view has no `sys_objects` row or a column has no `sys_fields` row | The conformance test fails and names the view and the column | v_ace_account.legacy_bucket has no data dictionary entry | AC5 |
| X5 | The service login holds a privilege in `public`, or a write on a view | The conformance test fails and names the privilege and the object | recovery_svc holds SELECT on public.account; the recovery role reads the views only | AC2 |
| X6 | A class of this service names a table in `public` | The build fails with boundary rule BND-6 and the class is named | Boundary rule BND-6 broken: AccountReader reads public.account. Read recovery.v_ace_account instead. | AC8 |
| X7 | A read asks for a field ID that the authorise answer does not cover | The field is returned masked; the read itself succeeds and no value is returned clear | None; the answer carries a marker per field ID, never text | AC9 |
| X8 | The authorise call does not answer inside 2 s | The read is refused with 503 and no field is returned; no answer is guessed from a stale cache | MSG-P4-002 from the guard library; no body from this service | AC10 |

X1 to X6 are the exception paths of RWB-E1-069 carried onto the split; X7 and X8 are the two paths the authorise hop of DP-08 adds. A second row for one ACE key in an extension table (legacy X7, SQLSTATE 23505) is RWB-P1-E1069-DB's path and is tested there. The view conformance test of RWB-E1-069 (AC1 to AC5) is this story's; the cross-schema check is the per-service boundary test (AC4 and AC8); the role and masking checks stay with RWB-P4-E1069-APP.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the published rwb-access, parameters and reference-data contracts and their fakes from Day 1; needs the `rwb_source_data` baseline and, for Section B, the ACE tables RWB-ACE-001 adds; it publishes the read path every later story uses |
| Negotiable | The view names and fields are frozen in the ACE Data Tier Map v1 and `recovery_views.sql`; the migration order, the test harness and the response shape are the squad's choice behind the contract |
| Valuable | One copy of source data, a boundary the database and the build enforce, one read path for 18 other services, and no load estate to build |
| Estimable | Two view migrations, three helper functions, one conformance test class, one boundary rule, one repository, three read operations and one authorise client |
| Small | Fits one sprint with its tests, as the primary slice of the legacy key |
| Testable | Every criterion in section 7 is one pipeline run, one catalog query or one refused statement with its SQLSTATE |

### 7. Acceptance criteria

```gherkin
Feature: Read-only ACE source views, grants and boundary rule

  Background:
    Given the ACE schema in DEV holds the 21 Tier 1 tables of section 11, among them public.account, public.payment, public.customer and public.efs_action
    Given the recovery schema holds the tables and the dictionary rows of V0001, and the three helper functions arrive with V0002
    Given the roles "ace_view_owner" and "recovery_svc" exist in DEV and SIT

  Scenario: AC1 The 16 Section A views compile (legacy RWB-E1-069 AC1)
    When the pipeline applies V0002__rwb_e1_069_ace_source_views.sql in DEV and then in SIT
    Then the migration creates party_ext, contact_point_ext, account_ext and valuation_ext
    Then the migration creates the 16 Section A views of section 11 and 16 of 16 compile
    Then a select of one row from each of the 16 views returns without error
    Then no other v_ace_* view exists in schema recovery
    Then the Flyway history holds one applied row for V0002 after V0001
    When the pipeline runs V0002 again in SIT
    Then Flyway reports V0002 as already applied and schema recovery still holds 16 v_ace_* views

  Scenario: AC2 The recovery role reads only through the views (legacy RWB-E1-069 AC2)
    Given V0002 is applied in SIT
    When a session as "recovery_svc" selects from recovery.v_ace_account
    Then the select returns rows
    When the same session selects from public.account
    Then the statement fails with SQLSTATE 42501 "permission denied for schema public"
    When the same session runs insert, update and delete on recovery.v_ace_account
    Then each statement fails with SQLSTATE 42501
    Then has_schema_privilege('recovery_svc', 'public', 'USAGE') is false
    Then has_table_privilege('recovery_svc', 'public.account', 'SELECT') is false
    Then has_table_privilege('recovery_svc', 'recovery.v_ace_account', 'INSERT') is false
    Then "ace_view_owner" owns the 16 views and holds SELECT on the 21 Tier 1 tables, and holds no INSERT, UPDATE or DELETE on any of them
    Then a test role "rwb_no_grant" cannot select recovery.v_ace_account, because PUBLIC holds no privilege on it

  Scenario: AC3 The 14 Section B views compile after RWB-ACE-001 (legacy RWB-E1-069 AC3)
    Given RWB-ACE-001 is applied in SIT and the 14 Tier 2 tables exist in public, among them public.ace_batch_run and public.valuation
    When the pipeline applies V0003__rwb_e1_069_ace_tier2_views.sql in SIT
    Then the migration creates the 14 Section B views of section 11 and 14 of 14 compile
    Then schema recovery holds 30 v_ace_* views, 16 Section A and 14 Section B, and 30 of 30 compile
    Then a select of one row from each of the 30 views returns without error
    Then the Flyway history holds one applied row for V0003 after V0002
    When the pipeline applies V0003 on a database where public.valuation does not exist
    Then the stage fails and names "relation public.valuation does not exist"
    Then no Section B view is created and the 16 Section A views are unchanged
    Then the features that read a Section B view stay behind their flags

  Scenario: AC4 No recovery constraint references public (legacy RWB-E1-069 AC4)
    Given schema recovery is at V0002
    When the conformance test lists every constraint in schema recovery
    Then no foreign key, check, unique or exclusion constraint names a table or a type outside schema recovery
    Then the test returns 0 rows for a constraint whose referenced table sits in schema public
    When a branch adds a foreign key from case_account.account_key to public.account
    Then the test fails with "fk_case_account_account_key references public.account; no constraint in recovery may reference another schema"
    Then the merge is blocked and the pipeline log holds the failing constraint name

  Scenario: AC5 Every view has dictionary rows (legacy RWB-E1-069 AC5)
    Given V0001, V0002 and V0003 are applied in SIT
    When a developer counts v_data_dictionary by source system
    Then 1,366 fields over 122 objects are returned
    Then the 30 objects named v_ace_* hold 304 fields, 177 in Section A and 127 in Section B
    Then 1,062 table fields are returned and 49 of them sit on the four extension tables
    Then each v_ace_* view has one sys_objects row and one sys_fields row per column
    When a branch adds a column "legacy_bucket" to recovery.v_ace_account with no sys_fields row
    Then the conformance test fails with "v_ace_account.legacy_bucket has no data dictionary entry"

  Scenario: AC6 The dictionary returns days_past_due from the ACE delay days (legacy RWB-E1-069 AC6)
    Given V0001 and V0002 are applied in SIT
    Given one ACE account "ACC0000017" has delay_days 95
    When a developer queries v_data_dictionary for entity "v_ace_account" and field "days_past_due"
    Then the row holds field ID "DF-ACE-018", data type "NUMBER" and physical type "integer"
    Then the row holds source system "ACE" and source field "public.account.delay_days"
    Then the row holds data product "DP01" and refresh cycle "DAILY"
    Then select days_past_due from recovery.v_ace_account for "ACC0000017" returns 95

  Scenario: AC7 The four extension tables are 1:1 on the ACE key (legacy RWB-E1-069 AC7)
    Given V0002 is applied in SIT
    When the pipeline lists the four extension tables and their columns
    Then party_ext holds 12 columns with person_key as its primary key
    Then contact_point_ext holds 14 columns with contact_key as its primary key and a check that contact_type is PHONE, EMAIL or ADDRESS
    Then account_ext holds 9 columns with account_key as its primary key
    Then valuation_ext holds 14 columns with valuation_key as its primary key
    Then the four tables hold 49 columns in all and 49 dictionary fields, DF-EXT-001 to DF-EXT-049
    Then no foreign key on any of the four tables references a table in schema public
    When the Workbench writes a second party_ext row for person_key "P0000123"
    Then the write fails with SQLSTATE 23505 and party_ext holds one row for "P0000123"

  Scenario: AC8 The boundary test allows only recovery.v_ace_* (legacy RWB-E1-069 AC8)
    Given a class "recovery.dataengine.internal.AccountReader" with a query on "public.account"
    When the pipeline runs RecoveryBoundaryTest
    Then the build fails with boundary rule BND-6, "AccountReader" and "public.account"
    When the class queries "recovery.v_ace_account" instead
    Then the build passes
    When a class in "recovery.dataengine.internal" holds the native query "select delay_days from public.account"
    Then the build fails with boundary rule BND-6
    Then the view names the rule allows are read from the module map, not written in the test

  Scenario: AC9 A field the authorise answer does not cover is returned masked (exception X7) (new, D-RCV-60)
    Given the authorise answer does not cover one field ID of recovery.v_ace_account
    When a read asks for that field ID
    Then the read succeeds
    Then that field is returned masked
    Then the answer carries a marker for that field ID and holds no value in clear

  Scenario: AC10 An authorise call that does not answer inside 2 s refuses the read (exception X8) (new, D-RCV-60)
    Given the authorise call does not answer inside 2 s
    When a read of recovery.v_ace_account is requested
    Then the read is refused with 503
    Then no field is returned and no answer is taken from a stale cache
    Then the error is MSG-P4-002 from the guard library, and no body comes from this service

  Scenario: AC11 A change to an applied view version is refused (section 9, DP-15) (new, D-RCV-60)
    Given V0002__rwb_e1_069_ace_source_views.sql is applied in SIT
    When a correction is attempted by editing the applied V0002 file instead of adding a new version
    Then the change is refused and the applied version V0002 is not edited
    Then the correction is accepted only as a new migration version
    Then the stage that refuses the change and its failure text are Not specified in the source documents (NEWAC-RWB-P1-E1069-APP-AC11)
```

**Target reading.** The assertions of AC1 to AC8 keep their legacy wording, apart from the V0001 Given line of AC1 and the merge line of AC4; AC9 to AC11 are added; what changes for the legacy criteria is where they run. `V0002__rwb_e1_069_ace_source_views.sql` (the 16 Section A views and the three helper functions, per TSD P1 T3.2) and `V0003__rwb_e1_069_ace_tier2_views.sql` (the 14 Section B views) become the next two versions of rwb-source-data's per-service Flyway sequence (DP-15), and the views they create stay in schema `recovery`, owned by `ace_view_owner`, because that is where the 30 views live and who owns them (DP-05, ADR-010); the role named `recovery_svc` in the legacy criteria is the `rwb_source_data` login of the target (DP-02; Architecture v5 slides 11 and 29). The grant block, the schema privileges, the `ace_view_owner` ownership and the four extension tables that AC1, AC2, AC3 and AC7 assert are delivered by RWB-P1-E1069-DB (external dependency X), so those assertions are executed against the objects and grants that story ships, not against a second copy; the dictionary counts and the field mapping of AC5 and AC6 are rwb-source-data's own rows in `sys_objects`, `sys_fields` and `data_product`, delivered with RWB-P1-E1001-APP; and boundary rule BND-6 of AC8 runs in this service's build and again across the other 18 logins in RWB-ITG-E1069-ITG. None of AC1 to AC8 reaches another service over a contract, so no contract-mock Given line is added to them; AC9 and AC10 exercise the authorise call. No legacy line is dropped. The 19 service login names are taken from the Environment and Deployment Design when it is issued. Until then, the other 18 service logins hold no privilege on PUBLIC or on the 30 views, PUBLIC holds nothing, and BND-6 is two build rules: no class names `public`, and no class outside rwb-source-data names a `v_ace_*` view or another service's schema.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The recovery module reads ACE source data only through the 30 SELECT-only `recovery.v_ace_*` views: 16 now over tables ACE holds, 14 when RWB-ACE-001 lands. It loads, copies and transforms nothing | D-RCV-35 U1, U4; ADR-010 |
| BR2 | A view is owned by `ace_view_owner`, which holds SELECT on the ACE tables it reads and writes nothing. It holds no right in schema `recovery` other than the views it owns | D-RCV-35 U4; CTL-02 |
| BR3 | On ACE source data `recovery_svc` holds SELECT on the views and no privilege of any kind in `public`; PUBLIC holds nothing; no INSERT, UPDATE, DELETE or TRUNCATE is granted on a view. Its DML on the Workbench's own tables is granted by V0001 and is outside this story | D-RCV-35 U4; BR-P1-001-4; CTL-02 |
| BR4 | No constraint in schema `recovery` references a table or a type outside it. A link to an ACE record is a `varchar(255)` business-key column with no foreign key, because ACE cascades deletes on `account` | D-RCV-35 U4; BR-P1-001-3; ADR-010 |
| BR5 | Every view carries one `sys_objects` row and one `sys_fields` row per column, with the ACE source field and the data product | BR-P1-001; RWB-E1-064 |
| BR6 | A text date in ACE becomes a date through `recovery.ace_to_date`, and a Y/N flag becomes a boolean through `recovery.ace_to_boolean`; both return NULL rather than fail a read | BR-P1-001-7 |
| BR7 | An extension table holds a Workbench decision about an ACE record and never a copy of an ACE column. It is 1:1 with the ACE record on the ACE business key and carries the seven standard record columns | BR-P1-001-5 |
| BR8 | Boundary rule BND-6: no recovery class names a table in schema `public`; the only source objects it may name are the 30 `recovery.v_ace_*` views, read from the module map | REQ-DRI-006; RWB-TE-001 |
| BR9 | A Section B view is created only after its ACE table exists. Until then the feature that reads it stays behind its flag, and the Section B migration is a later Flyway version | ADR-010; DL43 |

**Where each rule lives in the target.** BR1, BR2, BR3 and BR7 are the grant and ownership rules, and the objects and statements that enforce them are RWB-P1-E1069-DB's; this story only asserts them through the conformance test and its own read path, and the role named `recovery_svc` in BR2 and BR3 is the `rwb_source_data` login of the target (DP-02; Architecture v5 slides 11 and 29). BR4 is a rule about schema `recovery`, so its constraint scan runs here, over the views' own schema, and repeats over the 19 `rwb_*` schemas in RWB-ITG-E1069-ITG. BR5 and BR6 are answered inside this service: the dictionary rows are rwb-source-data's own, and the three helper functions `ace_to_date`, `ace_to_boolean` and `ace_mask_value` ship with the Section A migration (TSD P1 T3.2). BR7 is RWB-P1-E1069-DB's tables. BR8 is this service's build rule, with the 30 view names in `recovery-modules.yaml`; the second half of the boundary, no `v_ace_*` view named outside rwb-source-data and no other service's schema named anywhere, is proven in RWB-ITG-E1069-ITG. BR9 is the deployment order of the Section B migration, and the flag on each Section B feature stays with its own story.

### 9. State transitions

None. This story does not change a case status. It moves the service's Flyway sequence through two versions (Section A now, Section B with RWB-ACE-001) and changes no business row.

| From | Event | Condition | To |
|---|---|---|---|
| a view absent from schema `recovery` | the Section A or Section B migration | Every statement compiles against the ACE head | The view exists, compiles and answers a select of one row |
| a Section B view absent | the Section B migration | RWB-ACE-001 is reported deployed | The 14 Section B views exist; the feature flags of their readers may be switched on |
| a branch that names `public` in a class | the build | Boundary rule BND-6 sees the reference | The build fails and no artifact is produced |
| an applied view version | a correction | A fix is needed | A new version is merged; the applied version is never edited |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Recovery squad (RW-TRIBE) | Writes the two view migrations, the conformance test, the read contract and boundary rule BND-6 |
| ACE team lead and ACE DBA | Own schema `public`; approve the 21 Tier 1 table list and grant SELECT to `ace_view_owner` (RWB-ACE-001); supply the ACE DBA role for the release window |
| Recovery tech lead and data architect | Approve a change to the 30-view list, which is frozen in the ACE Data Tier Map v1 |
| Recovery migration account | Applies the two migrations and runs the conformance test in DEV and SIT |
| rwb-access (P4) | Owns the authorise and masking answer this read takes before it returns a field (DP-08) |
| RW-PLATADM, platform administrator | Reads the deployment result on SCR-44 Migration runs (Platform administration R); may not change a grant |
| RW-AUDIT, internal audit | Reads the view list and the grants (Platform administration R) |
| RW-DATASTEW, data steward | Reads the dictionary rows for the views (Data product catalog R) |
| No approval level from the delegation of authority applies | The story takes no business decision |

The login used by the read path is `rwb_source_data` (Architecture v5 slides 11 and 29; DP-02), and the grants it holds are issued by RWB-P1-E1069-DB. This story writes no grant statement and holds no credential.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-ACE-001 to DF-ACE-042 | v_ace_account | all 42 fields | Read |
| DF-ACE-043 to DF-ACE-054 | v_ace_payment | all 12 fields | Read |
| DF-ACE-055 to DF-ACE-074 | v_ace_customer | all 20 fields | Read |
| DF-ACE-075 to DF-ACE-083 | v_ace_contact | all 9 fields | Read |
| DF-ACE-084 to DF-ACE-088 | v_ace_ca_relation | all 5 fields | Read |
| DF-ACE-089 to DF-ACE-090 | v_ace_aa_relation | all 2 fields | Read |
| DF-ACE-091 to DF-ACE-098 | v_ace_collateral | all 8 fields | Read |
| DF-ACE-099 to DF-ACE-107 | v_ace_asset | all 9 fields | Read |
| DF-ACE-108 to DF-ACE-127 | v_ace_efs_action | all 20 fields | Read |
| DF-ACE-128 to DF-ACE-130 | v_ace_efs_action_code | all 3 fields | Read |
| DF-ACE-131 to DF-ACE-139 | v_ace_efs_assignment | all 9 fields | Read |
| DF-ACE-140 to DF-ACE-145 | v_ace_bucket_log | all 6 fields | Read |
| DF-ACE-146 to DF-ACE-150 | v_ace_product | all 5 fields | Read |
| DF-ACE-151 to DF-ACE-154 | v_ace_branch | all 4 fields | Read |
| DF-ACE-155 to DF-ACE-159 | v_ace_holiday | all 5 fields | Read |
| DF-ACE-160 to DF-ACE-177 | v_ace_plan | all 18 fields | Read |
| DF-ACE-178 to DF-ACE-186 | v_ace_batch_status | all 9 fields | Read |
| DF-ACE-187 to DF-ACE-195 | v_ace_valuation | all 9 fields | Read |
| DF-ACE-196 to DF-ACE-207 | v_ace_collateral_detail | all 12 fields | Read |
| DF-ACE-208 to DF-ACE-219 | v_ace_npa_asset | all 12 fields | Read |
| DF-ACE-220 to DF-ACE-230 | v_ace_npa_sale | all 11 fields | Read |
| DF-ACE-231 to DF-ACE-243 | v_ace_lawsuit | all 13 fields | Read |
| DF-ACE-244 to DF-ACE-250 | v_ace_hearing | all 7 fields | Read |
| DF-ACE-251 to DF-ACE-260 | v_ace_pod | all 10 fields | Read |
| DF-ACE-261 to DF-ACE-269 | v_ace_write_off | all 9 fields | Read |
| DF-ACE-270 to DF-ACE-279 | v_ace_score | all 10 fields | Read |
| DF-ACE-280 to DF-ACE-285 | v_ace_party_product | all 6 fields | Read |
| DF-ACE-286 to DF-ACE-293 | v_ace_credit_decision | all 8 fields | Read |
| DF-ACE-294 to DF-ACE-300 | v_ace_esign | all 7 fields | Read |
| DF-ACE-301 to DF-ACE-304 | v_ace_iam_group | all 4 fields | Read |
| DF-EXT-001 to DF-EXT-012 | party_ext | all 12 fields | Create (table); RWB-P1-E1069-DB creates it and a later story writes it |
| DF-EXT-013 to DF-EXT-026 | contact_point_ext | all 14 fields | Create (table); RWB-P1-E1069-DB creates it and a later story writes it |
| DF-EXT-027 to DF-EXT-035 | account_ext | all 9 fields | Create (table); RWB-P1-E1069-DB creates it and a later story writes it |
| DF-EXT-036 to DF-EXT-049 | valuation_ext | all 14 fields | Create (table); RWB-P1-E1069-DB creates it and a later story writes it |

Field IDs are those in the Logical Data Model and Data Dictionary.

Names such as `ace_view_owner`, `v_data_dictionary`, `recovery_svc` and `ace_to_date` are physical database objects (roles, views and functions). They are not LDM fields or entities in LDM v9 or Data Classification v5.

**Which side is this story's.** The 30 `DF-ACE-` rows are this story's: the view SQL defines those columns, the conformance test asserts their compilation and their dictionary row, and the three read operations return them. The four `DF-EXT-` rows belong to RWB-P1-E1069-DB, which creates the tables with their primary keys, their standard record columns and the `ck_contact_point_ext_type` check; this story creates none of them and copies none of their columns.

**Source tables.** Section A reads 21 ACE tables: `account`, `payment`, `customer`, `phone`, `email`, `address`, `ca_relation`, `aa_relation`, `collateral`, `asset`, `efs_action`, `efs_action_code`, `efs_assignment`, `bucket_log_snapshot`, `product`, `branch`, `bot_holiday`, `ace_case`, `cfsc_mg_ssme_tdr_case`, `tdr_calculation` and `ai_recommended_plan`. Section B reads 14, all added by RWB-ACE-001: `ace_batch_run`, `valuation`, `collateral_detail`, `npa_asset`, `npa_sale`, `lawsuit`, `hearing`, `pod_receipt`, `gl_write_off`, `collins_score`, `party_product`, `credit_decision`, `esign_request` and `iam_group`.

### 12. Contract

**12.1 REST operations provided**

The three read operations of the ACE read path on base `/api/recovery/source-data/v1` (DP-13), one per read family of the views. Each returns the columns of its view for one business key, with the personal fields masked or clear as the authorise answer says (12.2).

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| GET | `/customers/{id}` | The customer behind `v_ace_customer`, with `id_no_masked` and `id_no_last4` only and never the clear identity number | Any authenticated caller with a Workbench role and a right on the data product of the customer, over the authorise contract | Idempotent by id and business date |
| GET | `/accounts/{id}` | The account behind `v_ace_account`, with its arrears, balance and classification fields | As above, on the data product of the account | Idempotent by id and business date |
| GET | `/collateral/{id}` | The collateral and asset behind `v_ace_collateral`, with `v_ace_collateral_detail` once the Section B view is deployed | As above, on the data product of the collateral | Idempotent by id and business date |

`GET /payments?accountId=`, `GET /business-days/{date}/ready`, `GET /business-days/{date}/status` and `GET /data-products/freshness` are not in this story: they are RWB-P1-E1013-APP (Architecture v5 slide 15, OUT and IN lines). The admin operations of the module (`/admin/jobs`, `/admin/reconciliation/results`, `/admin/data-products`, `/admin/data-dictionary/fields`, `/admin/data-contracts`, `/admin/lists` and the freshness read) belong to the other P1 stories; this story adds none of them and changes no path of theirs.

The response field names and the problem body of the three operations are Not specified in the source documents (GAP-0566; ASM-0807); the story fixes the rule, one row per business key with the view's columns, and leaves the names to the contract in RWB-P1-E1069-CON.

**12.2 REST operations consumed**

| Method | Path | Owner | Use | Pattern |
|---|---|---|---|---|
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | Once per read: the caller identity from the session, the capability area, the right, the case reference and the field IDs about to be returned; the answer names the decision code, the matrix version and the masking version, with a marker per field ID | DP-08, DP-11; one hop, 2 s timeout, cached per call only |

The answer carries no value, and this service returns the value clear or masked as answered. A refusal is passed on with the rwb-access message; a call that does not answer inside 2 s refuses the read with 503 and returns no field (X8). No other service is called at run time: the parameters and the lists of values reach this service through the client libraries of rwb-case (DP-06, DP-07), and the ACE data is read in this service's own view (DP-01, DP-05).

**12.3 Events published**

None. The topic of the service is `rwb.source-data.events.v1` with event names `rwb.source-data.<Event>.v1` (DP-14), and its two events `AceDataReady` and `AceDataLate` belong to RWB-P1-E1013-APP (Architecture v5 slides 15 and 41). This story publishes no event and writes no outbox row of its own.

**12.4 Events consumed**

None. A view migration is a deployment step, not a reaction to an event, and Architecture v5 slide 15 gives the service no consumed event ("none: Airflow call; fallback polls ACE batch record").

**12.5 Workflows and activities**

None. The two migrations, the conformance test and the three reads are synchronous steps. The Temporal activities `listEligibleAccounts` and `snapshot(page)` and the workflows `AceIngestCheck` and `reconciliation` of Architecture v5 slide 15 are other P1 stories; the task queue of this service is `rwb-source-data` in namespace `rwb-recovery`, and this story starts no workflow and no activity on it.

**12.6 Schedules**

None. No Temporal Schedule and no Quartz job sits in this story.

**12.7 Tables owned**

| Object | Schema | Owner | This story |
|---|---|---|---|
| the 30 `v_ace_*` views | `recovery` | View owner `ace_view_owner`; contract owner P1 rwb-source-data | Created by this story's two migrations; the view itself is a SELECT-only projection with no primary key and no foreign key |
| `sys_objects`, `sys_fields`, `data_product`, `v_data_dictionary` | `rwb_source_data` | P1 | Read by the conformance test and by AC5 and AC6; the rows are delivered with RWB-P1-E1001-APP and no row is written here |
| `party_ext`, `contact_point_ext`, `account_ext`, `valuation_ext` | `rwb_source_data` | P1 | **Not created here**: RWB-P1-E1069-DB creates them; this story asserts their columns and their dictionary fields only |

No table of another service is read and no foreign key crosses a schema (DP-01). No service table sits in schema `recovery`, which holds the 30 views and the three helper functions and nothing else.

**Contract version built against.** REST v1, carried in the path (Service Contract Catalog v1, section 3.4): the consumed contracts on `/api/recovery/access/v1` (RWB-P4-E1037-CON) and `/api/recovery/case/v1` (RWB-P3-E1042-CON, RWB-P3-E1043-CON). The operations this story provides are on `/api/recovery/source-data/v1`.

**12.8 Contract fakes**

| Fake | Serves | Stubs used by this story |
|---|---|---|
| RWB-P4-E1037-CON fake (with the RWB-PLT-E1037-CON guard library) | `POST /api/recovery/access/v1/authorise` | A granted read with every field clear, a granted read with personal fields masked, a refused read, a no-row field and a timeout, each with the masking version |
| RWB-P3-E1042-CON fake | The parameters contract | The parameter that gates the Section B read path while the Section B view is absent |
| RWB-P3-E1043-CON fake | The reference-data contract | The lists of values the response carries as codes |
| Delivered-grants fixture | RWB-P1-E1069-DB | A container with schema `recovery`, the 30 views, the `rwb_source_data` login, `ace_view_owner` and the test role `rwb_no_grant`, so AC1, AC2, AC3 and AC7 run against the real grants without a second copy |
| `recovery_views.sql` fixture | The Physical Schema folder | The 30 view definitions and their checksums, so a rewritten view is a diff |

**12.9 Call-type summary**

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 3 operations on `/api/recovery/source-data/v1` | 1 operation (`POST /api/recovery/access/v1/authorise`) | OpenAPI 3.1, one hop, 2 s timeout, breaker per downstream (DP-11) |
| Kafka | None | None | The topic `rwb.source-data.events.v1` and its two events belong to RWB-P1-E1013-APP |
| Temporal | None | None | No workflow, activity or Schedule in this story |
| File | None | None | The view definitions are read at build time from `recovery_views.sql`, not at run time |
| SQL view | 30 `recovery.v_ace_*` views | The 21 Tier 1 ACE tables and, after RWB-ACE-001, the 14 Tier 2 tables, read only through those views | SELECT only, 5 s statement timeout, one login `rwb_source_data` (Architecture v5 slide 11) |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.sourcedata`, modules `views` and `read`, with the published types in `...sourcedata.api`. Service base `/api/recovery/source-data/v1`, schema `rwb_source_data`, views in schema `recovery`, topic `rwb.source-data.events.v1` (not published here), Temporal task queue `rwb-source-data` in namespace `rwb-recovery` (not used here).

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

DP-05 is this story's own pattern: rwb-source-data is the one service that reads the `v_ace_*` views, and it publishes them onward as a contract. DP-02 is used, not delivered: the login and the grants are RWB-P1-E1069-DB's. DP-03 applies as one decision record per refused or masked read answered through the guard library, and this story adds no event of its own. DP-19 applies to the composite route of the screens that read a customer or an account, which this story serves and does not build.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `V0002__rwb_e1_069_ace_source_views.sql` (legacy name; the next version on the service sequence) | Migration | The three helper functions and the 16 Section A views, copied from `recovery_views.sql` |
| `V0003__rwb_e1_069_ace_tier2_views.sql` (legacy name; the version after it) | Migration | The 14 Section B views, copied from `recovery_views.sql` |
| `ViewConformanceTest` | Test | Four checks: every view compiles, no constraint references `public`, every view has dictionary rows, the service login has no privilege in `public` and no write on a view |
| `AceSourceReadRepository` | Repository | SELECT only on `recovery.v_ace_*`, one read method per view; names no `public` table and no other schema |
| `SourceReadService` | Service | Resolves the business key, reads the view, takes the authorise answer, applies the marker per field and returns the row |
| `AccessGuardClient` | Client | The rwb-access authorise contract through the guard library: one hop, 2 s timeout, no stale cache (DP-08, DP-11) |
| `SourceReadController` | Controller | The three read operations on `/api/recovery/source-data/v1`; RFC 9457 problem details |
| `SourceViewBoundaryRule` | ArchUnit rule in `RecoveryBoundaryTest` | Boundary rule BND-6 over this service's package: no class names a table in schema `public` |
| `recovery-modules.yaml` | Rule table | Gains `sourceViews`, the 30 view names that BND-6 allows |

**Migrations and sequence (DP-15).** The two view migrations sit on rwb-source-data's own Flyway sequence, after the baseline, in this order: Section A (helper functions and 16 views), then Section B (14 views). The legacy file names are kept as the source of the objects; the exact version numbers are assigned by the sequence owner at build time, and no monolith version number is reused. The statements create objects in schema `recovery` and are run under the ACE DBA role for the release window; the schema name is written as the fixed `recovery`, and no environment name appears in a file. The grant statements of the legacy migration are **not** in these files: they are RWB-P1-E1069-DB's migration, applied on the same sequence.

**Database.** This story creates 30 views and three helper functions in schema `recovery` and no table. It adds no foreign key, no index and no column to any table. The four extension tables are created by RWB-P1-E1069-DB, and the dictionary rows of the views come with RWB-P1-E1001-APP.

**Configuration and reference data**

- The 30-view list is frozen in the ACE Data Tier Map v1 and copied into `recovery-modules.yaml`; a change needs the data architect and the recovery tech lead.
- The view definitions are taken verbatim from `recovery_views.sql`; a rewritten view is a diff and fails its fixture.
- The three helper functions are `recovery.ace_to_date`, `recovery.ace_to_boolean` and `recovery.ace_mask_value`, with the rules of TSD P1 T3.2.
- The authorise contract, its 2 s budget and the masking answer are configuration of the guard library, not constants in this service (DP-08).
- The read path is a REST contract on `/api/recovery/source-data/v1` and not a shared Java interface, so the other 18 services and the agents reach ACE data through it and never through a view of their own (Architecture v5 slides 11, 13 and 45; DP-05, DP-11; GAP-0567; ASM-0808).
- The Section B read path stays behind the flag of the feature that reads it until the Section B migration is applied (BR9).
- The boundary rule is written once, in this service's build, and the module map it reads is the only place the 30 view names are listed; the proof over the other 18 logins is the integration slice (GAP-0566; ASM-0812).

**Build steps**

1. The Section A migration with the three helper functions and the 16 views, copied from `recovery_views.sql`, and its fixture against the ACE head (AC1).
2. `ViewConformanceTest` with its four checks and a failing fixture for each: a view that does not compile, a foreign key into `public`, a view column with no `sys_fields` row, and a privilege or a write found on the login (AC1 to AC5).
3. The Section B migration with the 14 views, and a pipeline stage that runs only after RWB-ACE-001 is reported deployed (AC3).
4. `AceSourceReadRepository` with one read method per view; a test that the service names no `public` table and no other schema (AC4, AC8).
5. `SourceReadService` with the authorise hop, the marker per field, the masked default and the 503 on a timeout (12.2, X7, X8).
6. The three read operations on the contract, with RFC 9457 problem details and the cache key of the read (12.1).
7. Boundary rule BND-6 and `recovery-modules.yaml`, with a fixture class on `public.account`, the same class on `recovery.v_ace_account`, and the module map read at run time (AC8).
8. The delivered-grants fixture that runs AC1, AC2, AC3 and AC7 against the objects and grants of RWB-P1-E1069-DB, so the criteria are tested once, where they are delivered.

**Feature flag.** None for the views: they are the read path, not a feature. Each Section B feature keeps the flag it already has until the Section B migration is applied (BR9); this story adds no flag of its own.

**Done when.** The tests in section 16 pass, SIT holds 30 compiling views and the three helper functions in schema `recovery`, the conformance test and boundary rule BND-6 appear in the pipeline report of main, and the three read operations answer against the grants delivered by RWB-P1-E1069-DB with the authorise answer of rwb-access.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| Conformance check 1 | A view does not compile | v_ace_account does not compile: column a.core_banking_system_date does not exist |
| Conformance check 2 | A constraint references `public` | fk_case_account_account_key references public.account; no constraint in recovery may reference another schema |
| Conformance check 3 | A view has no dictionary row | v_ace_account.legacy_bucket has no data dictionary entry |
| Conformance check 4 | The service login holds a privilege in `public` or can write a view | recovery_svc holds SELECT on public.account; the recovery role reads the views only |
| Build log | A class names a `public` table | Boundary rule BND-6 broken: AccountReader reads public.account. Read recovery.v_ace_account instead. |
| SQLSTATE 42501 | The service login selects a public table or writes a view | permission denied for schema public |
| SQLSTATE 23505 | A second row for one ACE key in an extension table | duplicate key value violates unique constraint party_ext_pkey |
| MSG-P4-002 | The authorise answer refuses the read | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The access entry of the read cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The five conformance, build-log and SQLSTATE texts are the legacy ones, unchanged, and are for developers; they are not part of the message standard. No `MSG-` ID of this story is new: MSG-P4-002 and MSG-P7-003 are raised by the rwb-access guard library on the authorise hop (DP-08), and a read refused because the authorise call timed out returns 503 with no body from this service (X8).

### 15. Screens and states

No screen in this story. The platform administrator reads the deployment result in the pipeline run and on SCR-44 Interface and job monitor, which shows the two view versions with their status and the conformance result under Platform administration R. A developer reads the conformance test and boundary rule BND-6 in the pull request checks. The customer and account panels of the case screen reach this service through the gateway-bff composite route (DP-19), which calls rwb-case and rwb-source-data in parallel, one hop each; the rendering of a masked field belongs to the screen owner.

States of SCR-44 Interface and job monitor: empty, loading, error and no access are not specified in the source documents (CG-ALL-2342).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-069-01 | AC1, BR1, BR2 | End to end | Clean PostgreSQL 17 container: ACE Schema PostgreSQL v1.sql, V0001, then V0002; a repeated V0002 run |
| TC-E1-069-02 | AC2, BR3 | Component | Sessions as recovery_svc, ace_view_owner and a test role with no grant in SIT |
| TC-E1-069-09 | AC9 | Component | A read of a field ID that the authorise answer does not cover, in SIT |
| TC-E1-069-10 | AC10 | Component | An authorise call that does not answer inside 2 s, in SIT |
| TC-E1-069-11 | AC11 | End to end | V0002 applied in SIT; a branch that edits the applied V0002 file |
| TC-E1-069-03 | AC3, BR1, BR9 | End to end | Tier 2 probe with the 14 tables; then V0003 on a database without public.valuation |
| TC-E1-069-04 | AC4, BR4 | End to end | Branch adding fk_case_account_account_key to public.account |
| TC-E1-069-05 | AC5, BR5 | End to end | 122 objects and 1,366 fields; a view column with no sys_fields row |
| TC-E1-069-06 | AC6, BR6 | End to end | Account ACC0000017 with delay_days 95; dictionary query |
| TC-E1-069-07 | AC7, BR7 | End to end | Duplicate person_key P0000123 in party_ext; column list of the four tables |
| TC-E1-069-08 | AC8, BR8 | End to end | Fixture AccountReader on public.account and on recovery.v_ace_account; native query fixture |

The legacy test case IDs, Covers and Data are kept in order and character for character; the legacy level "System" maps to "End to end" and "Access" to "Component", as in the other stories of this run. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. TC-E1-069-02 and TC-E1-069-07 run against the grants and the four extension tables that RWB-P1-E1069-DB delivers, and the authorise hop of every read is tested at Component level inside the read operations of section 12.1. The `-ITG` copies of these cases belong to RWB-ITG-E1069-ITG and are not listed here.

### 17. Guardrails

- No business value in code: the view list, the role names and the schema name are configuration and data, not constants in a service; `recovery-modules.yaml` carries the 30 view names and the boundary rule reads them.
- Personal data never appears in logs, tests, events or prompts: test rows are synthetic; the customer view returns `id_no_masked` and `id_no_last4` only and never the clear identity number; the authorise answer carries a marker and a version, never a value.
- The reads carry personal data, handled as Data Classification v5 states: `v_ace_branch.address`, `v_ace_branch.phone` and `v_ace_asset.address` (Customer data, Confidential) are shown within the role's scope, and a log carries a code or an id only, never the customer value; `v_ace_customer.id_no_masked` (Direct identifier, Restricted) is masked unless the role may see it, is never in an event, a workflow input or a log, and its read is audited through the ACE Common PII path.
- No read of a `public` table and no write to an ACE table: the database grants and boundary rule BND-6 enforce it, and a breach is a defect.
- ACE data only through the owner's contract or `v_ace_*` views: this service reads the views and no other schema, and every other service reads this service's contract (DP-01, DP-05).
- One hop and 2 s on the authorise call; a slow answer refuses the read and returns no field (DP-11).
- The views are forward only in PROD; a wrong view is corrected by a new migration, never by editing an applied one (DP-15).
- The grants, the login and the four extension tables are one story's delivery and one story's test: this story asserts them and never re-creates them.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-RDF-002 | Account balance, arrears, payments and classification for every account at 90 or more days past due are read from ACE through `v_ace_account` and `v_ace_payment`, current to the previous working day | Business Requirements Epic 1, sections 3.1 and 4 | FEAT-RDF-01 | All recovery processes | D-RCV-35 U4; BR-P1-001-2; BR-P1-001-3 | TC-E1-069-01, TC-E1-069-02, TC-E1-069-03, TC-E1-069-05, TC-E1-069-06 |
| REQ-DRI-006 | No component calls a system of record directly | Business Requirements Program, sections 5.2 and 7 | FEAT-RDF-01 | All recovery processes | ADR-010; DL43 | TC-E1-069-04, TC-E1-069-08 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-P1-E1001-APP | App development | H build dependency: the `rwb_source_data` baseline, the dictionary rows and `v_data_dictionary` |
| RWB-P1-ACE001-DB | ACE DB | H build dependency: the 14 Tier 2 tables the Section B views read |
| RWB-P1-E1069-DB | ACE DB | X external dependency: the login, the grant block, `ace_view_owner` and the four extension tables this story's criteria assert |
| RWB-P4-E1069-APP | App development | Sibling of the same legacy key: the masking policy rows and the boundary of rwb-access; it owns no view, no grant and no extension table |
| RWB-ITG-E1069-ITG | Integration | Proves the grant matrix across the 19 logins and both halves of boundary rule BND-6 |
| RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1037-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON | Contract | H: the decision-record library, the parameters and reference-data libraries, the guard library, the per-service Flyway sequence and the gateway-bff composite route |
| RWB-P3-E1042-CON, RWB-P3-E1043-CON, RWB-P4-E1037-CON | Contract | C: the rwb-case parameters and reference-data contracts and the rwb-access authorise contract |
| RWB-P1-E1013-APP | App development | Sibling: the freshness reads and the business-day operations of the service |

### 19. Out of scope

- The `rwb_source_data` login, the grant block, the schema privileges, the PUBLIC revokes, the view owner `ace_view_owner` with its SELECT on the 21 Tier 1 and 14 Tier 2 ACE tables, and the four extension tables: RWB-P1-E1069-DB.
- The proof of the grant matrix across the 19 logins and the second half of boundary rule BND-6 (no `v_ace_*` view named outside rwb-source-data, no other service's schema named): RWB-ITG-E1069-ITG.
- The 14 Tier 2 tables and the 12 columns that RWB-ACE-001 adds to `account`, `customer` and `efs_action`: the ACE team owns them, and this story neither creates nor alters them.
- The masking policy rows and the masking answer itself: rwb-access, RWB-P4-E1069-APP (DP-08); this story takes the answer and applies the marker.
- The dictionary content and its maintenance: RWB-P1-E1001-APP for the metadata rows and RWB-E1-064 in the legacy set for the dictionary of the 14 data products.
- The freshness stamp, the case list, the reconciliation, the data products and their contracts, and the business-day operations: the other P1 stories, among them RWB-P1-E1013-APP.
- The features that read a Section B view: their own stories, behind their flags until the Section B migration is applied.
- The screens that show a customer, an account or a collateral record: gateway-bff and the screen owners (DP-19).
- The rest of RWB-TE-001 in the target: this story adds boundary rule BND-6 and the `sourceViews` list only.
- Any change to the 30-view list: the data architect and the recovery tech lead, with a new version of the ACE Data Tier Map v1.
