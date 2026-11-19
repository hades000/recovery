# RWB-E1-069 Read-only ACE source views, grants and boundary rule

SCB Collections and Recovery. Henka Group, 15 November 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E1-069 |
| Epic | E1, release 30 November 2026 |
| Module | P1 Recovery data engine |
| Feature | FEAT-RDF-01 Create the recovery tables, extension tables and read-only ACE views |
| Requirement IDs | REQ-RDF-002, REQ-DRI-006 |
| BRD section | Business Requirements Epic 1, section 3.1 (story) and section 4 (REQ-RDF-002); Business Requirements Program, sections 5.2 and 7 (REQ-DRI-006) |
| L3 process | All recovery processes |
| Decision | D-RCV-35 (U1, U4); ADR-010; DL43 |
| Priority | Must |
| Depends on | RWB-E1-001 (V0001); RWB-ACE-001 for the 14 Section B views (DL43) |
| Blocks | RWB-E1-002, RWB-E1-016, RWB-E1-018 |
| Status | Ready for build |

## 1. Story

As a **recovery developer (RW-TRIBE)**, I want **the recovery module to read ACE source data only through SELECT-only recovery.v_ace_* views, with the database grants and the build-time rule that enforce the boundary**, so that **there is one copy of source data, the Workbench cannot alter or copy it, and a direct read of an ACE table fails in the database and in the build**.

## 2. Business rationale

The Workbench takes no inbound source data. ACE ingests every source, and the recovery module reads it through 30 SELECT-only views: 16 over the ACE tables that exist today, 177 fields, and 14 over the tables RWB-ACE-001 adds, 127 fields. The views are owned by a dedicated role that holds SELECT on the ACE tables; the recovery service role holds SELECT on the views and no privilege on anything in `public`. PUBLIC holds no privilege, and no write is granted on a view. The Workbench keeps its own decisions about an ACE record in four extension tables keyed by the ACE business key, never in a copy of an ACE column.

The boundary is enforced twice: by the catalog, where a direct `public` read is refused, and by boundary rule BND-6 in RWB-TE-001, which fails the build when a recovery class names a `public` table. Serves REQ-RDF-002 (account balance, arrears, payments and classification read from ACE through `v_ace_account` and `v_ace_payment`) and REQ-DRI-006 (no component calls a system of record directly); applies D-RCV-35 U1 and U4 and ADR-010. The measure is 100 percent of pipeline runs in which every view compiles and the conformance test passes.

## 3. Preconditions

- RWB-E1-001 is done: V0001 created the recovery tables, the three helper functions `recovery.ace_to_date`, `recovery.ace_to_boolean` and `recovery.ace_mask_value`, the dictionary rows and the view `v_data_dictionary`.
- RWB-E1-044 is done: Flyway runs in the ACE pipeline and takes the schema name from the parameter `recoverySchema`, fixed to `recovery` in every environment (D-RCV-28).
- The ACE schema in DEV and SIT is at the head that holds the 21 Tier 1 tables of section 11, among them `account`, `payment`, `customer` and `efs_action` (ACE Schema PostgreSQL v1.sql).
- The roles `ace_view_owner` and `recovery_svc` exist in DEV and SIT, with the names fixed in the Environment and Deployment Design. The recovery migration account holds the ACE DBA role for the release window, so it can grant on schema `public` and set a view owner (RWB-E1-044).
- The module map of RWB-TE-001 is in the repository, with `recovery-modules.yaml` read by `RecoveryBoundaryTest`.
- For the 14 Section B views only: RWB-ACE-001 is deployed in DEV and SIT and its 14 Tier 2 tables exist (DL43). Until then the features that read a Section B view stay behind their flags.

## 4. Flow

1. Recovery developer: takes Section A of `15 ACE DB Alignment/Recovery Workbench ACE Source Views v1.sql` into `V0002__rwb_e1_069_ace_source_views.sql`: the 16 views, the three helper functions and the grant block. The four extension tables ship in V0001 with RWB-E1-001, which runs first; this story verifies them rather than creating them.
2. Recovery developer: writes no environment name in the file. The schema is `${recoverySchema}` and the two role names come from the Environment and Deployment Design (D-RCV-28; RWB-E1-044).
3. Pipeline: applies V0001 then V0002 in DEV, then in SIT.
4. Pipeline: runs the conformance test: 16 of 16 views compile, no constraint in `recovery` references `public`, every view has dictionary rows, and `recovery_svc` has no privilege in `public` and no write on a view.
5. Recovery developer: adds boundary rule BND-6 to `RecoveryBoundaryTest` in RWB-TE-001 and the 30 view names to `recovery-modules.yaml` as the only allowed source objects.
6. ACE team: applies RWB-ACE-001 with the 14 Tier 2 tables, and its migration grants SELECT on those tables to `ace_view_owner` (DL43).
7. Recovery developer: writes `V0003__rwb_e1_069_ace_tier2_views.sql` with the 14 Section B views and one SELECT grant per view to `recovery_svc`. The dictionary rows for the 14 views ship with V0001, as the 16 Section A rows do.
8. Pipeline: applies V0003 in DEV and SIT; 30 of 30 views compile and the features that read a Section B view come out from behind their flags.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A Section A view does not compile | The V0002 stage rolls back; no view from that run exists; the extension tables from V0001 are unchanged; the stage names the view and the ACE column | Pipeline log: v_ace_account does not compile: column a.core_banking_system_date does not exist | AC1 |
| X2 | V0003 is applied before RWB-ACE-001 | The stage fails; no Section B view is created; the 16 Section A views and their features are unchanged | Pipeline log: relation public.valuation does not exist | AC3 |
| X3 | A recovery constraint references a table in `public` | The conformance test fails and the merge is blocked | fk_case_account_account_key references public.account; no constraint in recovery may reference another schema | AC4 |
| X4 | A view has no `sys_objects` row or a column has no `sys_fields` row | The conformance test fails and names the view and the column | v_ace_account.legacy_bucket has no data dictionary entry | AC5 |
| X5 | `recovery_svc` holds a privilege in `public`, or a write on a view | The conformance test fails and names the privilege and the object | recovery_svc holds SELECT on public.account; the recovery role reads the views only | AC2 |
| X6 | A recovery class names a table in `public` | The build fails with boundary rule BND-6 and the class is named | Boundary rule BND-6 broken: AccountReader reads public.account. Read recovery.v_ace_account instead. | AC8 |
| X7 | A second row is written for an ACE key already in an extension table | The write is refused; the first row is unchanged | SQLSTATE 23505 duplicate key value violates unique constraint party_ext_pkey | AC7 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs V0001 and, for Section B, the ACE tables RWB-ACE-001 adds; it publishes the read path every later story uses |
| Negotiable | The view names and fields are frozen in the ACE Data Tier Map v1 and the ACE Source Views file; the migration order and the test harness are the squad's choice |
| Valuable | One copy of source data, a boundary the database enforces, and no load estate to build |
| Estimable | Two migrations, four extension tables, one conformance test class, one boundary rule |
| Small | Fits in one sprint with its tests |
| Testable | Each criterion is one pipeline run or one catalog query |

## 7. Acceptance criteria

```gherkin
Feature: Read-only ACE source views, grants and boundary rule

  Background:
    Given the ACE schema in DEV holds the 21 Tier 1 tables of section 11, among them public.account, public.payment, public.customer and public.efs_action
    Given the recovery schema holds the tables, the three helper functions and the dictionary rows of V0001
    Given the roles "ace_view_owner" and "recovery_svc" exist in DEV and SIT

  Scenario: AC1 The 16 Section A views compile
    When the pipeline applies V0002__rwb_e1_069_ace_source_views.sql in DEV and then in SIT
    Then the migration creates party_ext, contact_point_ext, account_ext and valuation_ext
    Then the migration creates the 16 Section A views of section 11 and 16 of 16 compile
    Then a select of one row from each of the 16 views returns without error
    Then no other v_ace_* view exists in schema recovery
    Then the Flyway history holds one applied row for V0002 after V0001
    When the pipeline runs V0002 again in SIT
    Then Flyway reports V0002 as already applied and schema recovery still holds 16 v_ace_* views

  Scenario: AC2 The recovery role reads only through the views
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

  Scenario: AC3 The 14 Section B views compile after RWB-ACE-001
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

  Scenario: AC4 No recovery constraint references public
    Given schema recovery is at V0002
    When the conformance test lists every constraint in schema recovery
    Then no foreign key, check, unique or exclusion constraint names a table or a type outside schema recovery
    Then the test returns 0 rows for a constraint whose referenced table sits in schema public
    When a branch adds a foreign key from case_account.account_key to public.account
    Then the test fails with "fk_case_account_account_key references public.account; no constraint in recovery may reference another schema"
    Then the merge is blocked

  Scenario: AC5 Every view has dictionary rows
    Given V0001, V0002 and V0003 are applied in SIT
    When a developer counts v_data_dictionary by source system
    Then 1,366 fields over 122 objects are returned
    Then the 30 objects named v_ace_* hold 304 fields, 177 in Section A and 127 in Section B
    Then 1,062 table fields are returned and 49 of them sit on the four extension tables
    Then each v_ace_* view has one sys_objects row and one sys_fields row per column
    When a branch adds a column "legacy_bucket" to recovery.v_ace_account with no sys_fields row
    Then the conformance test fails with "v_ace_account.legacy_bucket has no data dictionary entry"

  Scenario: AC6 The dictionary returns days_past_due from the ACE delay days
    Given V0001 and V0002 are applied in SIT
    Given one ACE account "ACC0000017" has delay_days 95
    When a developer queries v_data_dictionary for entity "v_ace_account" and field "days_past_due"
    Then the row holds field ID "DF-ACE-018", data type "NUMBER" and physical type "integer"
    Then the row holds source system "ACE" and source field "public.account.delay_days"
    Then the row holds data product "DP01" and refresh cycle "DAILY"
    Then select days_past_due from recovery.v_ace_account for "ACC0000017" returns 95

  Scenario: AC7 The four extension tables are 1:1 on the ACE key
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

  Scenario: AC8 The boundary test allows only recovery.v_ace_*
    Given a class "recovery.dataengine.internal.AccountReader" with a query on "public.account"
    When the pipeline runs RecoveryBoundaryTest
    Then the build fails with boundary rule BND-6, "AccountReader" and "public.account"
    When the class queries "recovery.v_ace_account" instead
    Then the build passes
    When a class in "recovery.dataengine.internal" holds the native query "select delay_days from public.account"
    Then the build fails with boundary rule BND-6
    Then the view names the rule allows are read from the module map, not written in the test
```

## 8. Business rules

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
| BR9 | A Section B view is created only after its ACE table exists. Until then the feature that reads it stays behind its flag, and V0003 is a later Flyway sequence | ADR-010; DL43 |

## 9. State transitions

None. This story does not change a case status. It moves schema `recovery` through two Flyway versions (V0002 now, V0003 with RWB-ACE-001), changes the privileges of two database roles and owns no business row.

## 10. Authority

| Who | What they may do in this story |
|---|---|
| Recovery squad (RW-TRIBE) | Writes V0002, V0003 and boundary rule BND-6 |
| ACE team lead and ACE DBA | Own schema `public`; approve the 21 Tier 1 table list and grant SELECT to `ace_view_owner` (RWB-ACE-001) |
| Recovery tech lead and data architect | Approve a change to the 30-view list, which is frozen in the ACE Data Tier Map v1 |
| Recovery migration account | Applies V0002 and V0003 and runs the conformance test in DEV and SIT |
| RW-PLATADM, platform administrator | Reads the deployment result on SCR-44 Migration runs (Platform administration R); may not change a grant |
| RW-AUDIT, internal audit | Reads the view list and the grants (Platform administration R) |
| RW-DATASTEW, data steward | Reads the dictionary rows for the views (Data product catalog R) |
| No approval level from the delegation of authority applies | The story takes no business decision |

## 11. Data

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
| DF-EXT-001 to DF-EXT-012 | party_ext | all 12 fields | Create (table); a later story writes it |
| DF-EXT-013 to DF-EXT-026 | contact_point_ext | all 14 fields | Create (table); a later story writes it |
| DF-EXT-027 to DF-EXT-035 | account_ext | all 9 fields | Create (table); a later story writes it |
| DF-EXT-036 to DF-EXT-049 | valuation_ext | all 14 fields | Create (table); a later story writes it |

Field IDs are those in the Logical Data Model and Data Dictionary.

**Source tables.** Section A reads 21 ACE tables: `account`, `payment`, `customer`, `phone`, `email`, `address`, `ca_relation`, `aa_relation`, `collateral`, `asset`, `efs_action`, `efs_action_code`, `efs_assignment`, `bucket_log_snapshot`, `product`, `branch`, `bot_holiday`, `ace_case`, `cfsc_mg_ssme_tdr_case`, `tdr_calculation` and `ai_recommended_plan`. Section B reads 14, all added by RWB-ACE-001: `ace_batch_run`, `valuation`, `collateral_detail`, `npa_asset`, `npa_sale`, `lawsuit`, `hearing`, `pod_receipt`, `gl_write_off`, `collins_score`, `party_product`, `credit_decision`, `esign_request` and `iam_group`.

## 12. Contract

No endpoint and no event. The contract is the migration set and the grant.

| Item | Value |
|---|---|
| Migration V0002 | `V0002__rwb_e1_069_ace_source_views.sql`: the four extension tables, the 16 Section A views, the Section A grant |
| Migration V0003 | `V0003__rwb_e1_069_ace_tier2_views.sql`: the 14 Section B views, the Section B grant |
| Published interface | The 30 `recovery.v_ace_*` views: one row per ACE object, no primary key, no foreign key. Every module reads source data here and nowhere else |
| Grantees | `ace_view_owner` owns the views and holds SELECT on the ACE tables; `recovery_svc` holds SELECT on the views only; PUBLIC holds nothing |
| Trigger | The pipeline step `migrate` at deployment (RWB-E1-044) |
| Idempotency | The Flyway version. An applied version is never applied again; a repeated GRANT changes nothing |
| Restart | A failed migration rolls back. A fix is merged as a new version; V0003 waits until RWB-ACE-001 is deployed |
| Output | Applied objects in schema `recovery`; rows in `flyway_schema_history_recovery`; a pass or a named failure from the conformance test |

**Grant block in V0002** (run as the ACE schema owner; the 16 ALTER VIEW OWNER statements are one per view)

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

GRANT USAGE ON SCHEMA recovery TO recovery_svc;
GRANT SELECT ON recovery.v_ace_account TO recovery_svc;
-- one GRANT per view, 16 in V0002 and 30 in all; never GRANT SELECT ON ALL TABLES IN SCHEMA recovery

REVOKE ALL ON ALL TABLES IN SCHEMA recovery FROM PUBLIC;
```

## 13. Solution plan

**Packages and files.** Migration files in `ace-service/src/main/resources/db/migration/recovery` (RWB-E1-044). Boundary rule in the test source of the recovery module, beside `RecoveryBoundaryTest` (RWB-TE-001). The view definitions are taken verbatim from `15 ACE DB Alignment/Recovery Workbench ACE Source Views v1.sql`; the four extension tables verbatim from `06 Data/Recovery Workbench Physical Schema v5.sql`.

| Component | Type | Responsibility |
|---|---|---|
| V0002__rwb_e1_069_ace_source_views.sql | Migration | Four extension tables, 16 Section A views, Section A grant |
| V0003__rwb_e1_069_ace_tier2_views.sql | Migration | 14 Section B views and their SELECT grant |
| ViewConformanceTest | Test | Four checks: every view compiles, no constraint references `public`, every view has dictionary rows, `recovery_svc` has no privilege in `public` and no write on a view |
| SourceViewBoundaryRule | ArchUnit rule in RecoveryBoundaryTest | Boundary rule BND-6: a recovery class names no table in schema `public` |
| recovery-modules.yaml | Rule table | Gains `sourceViews`, the 30 view names that BND-6 allows |
| recovery.v_ace_* | Published read interface | The only source read for every module |

**Database.** V0002 creates four tables and 16 views; V0003 creates 14 views. No table in schema `recovery` gains a foreign key into `public`, and no ACE table is altered. The extension tables are:

- `party_ext`: person_key varchar(255) primary key, vulnerable, deceased_override, bankruptcy, fraud_flag boolean NOT NULL DEFAULT false, is_active boolean NOT NULL DEFAULT true, state varchar(40), version integer NOT NULL DEFAULT 1, created_at and updated_at timestamptz NOT NULL DEFAULT now(), created_by and updated_by uuid.
- `contact_point_ext`: contact_key varchar(255) primary key, contact_type varchar(10) NOT NULL, consent_given boolean NOT NULL DEFAULT false, consent_at and verified_at timestamptz, failed_count integer NOT NULL DEFAULT 0, source varchar(20) NOT NULL DEFAULT 'WORKBENCH', is_active, state, version, created_at, created_by, updated_at, updated_by, and the check `ck_contact_point_ext_type` that contact_type is PHONE, EMAIL or ADDRESS.
- `account_ext`: account_key varchar(255) primary key, dispute_open boolean NOT NULL DEFAULT false, is_active, state, version, created_at, created_by, updated_at, updated_by.
- `valuation_ext`: valuation_key varchar(255) primary key, accepted boolean NOT NULL DEFAULT false, accepted_at timestamptz, accepted_by and valuer_partner_id uuid, stale_flag boolean NOT NULL DEFAULT false, age_days integer, is_active, state, version, created_at, created_by, updated_at, updated_by.

**Configuration and reference data.** The roles `ace_view_owner` and `recovery_svc` and their names are fixed in the Environment and Deployment Design. The schema is `${recoverySchema}`, fixed to `recovery` (D-RCV-28). The 30-view list is frozen in the ACE Data Tier Map v1 and copied into `recovery-modules.yaml`; a change needs the data architect and the recovery tech lead. Section B features keep their own flags.

**Build steps**

1. V0002: the four extension tables, copied from Physical Schema v5 with their primary keys and the contact type check (AC7).
2. V0002: the 16 Section A views, copied from the ACE Source Views file, using the V0001 helper functions (AC1).
3. V0002: the grant block of section 12, with one GRANT and one ALTER VIEW OWNER per view and no `ALL TABLES` grant (AC2).
4. ViewConformanceTest with its four checks and a failing fixture for each (AC1 to AC5).
5. Boundary rule BND-6 in RecoveryBoundaryTest, reading `sourceViews` from the module map, with a fixture class on `public.account` and the same class on `recovery.v_ace_account` (AC8).
6. V0003: the 14 Section B views, copied from the ACE Source Views file, and one SELECT grant per view (AC3).
7. A pipeline stage for V0003 that runs only after RWB-ACE-001 is reported deployed; before that the stage is skipped and the Section B features stay behind their flags (AC3).
8. Tests for AC1 to AC8, including the access test on `recovery_svc` and a test role with no grant.

**Feature flag.** None for the views; they are the read path, not a feature. Each Section B feature keeps the flag it already has until V0003 is applied.

**Done when.** The tests in section 16 pass, SIT holds 30 compiling views and four extension tables, and the pipeline of main shows the conformance test and boundary rule BND-6 in its report.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| Conformance check 1 | A view does not compile | v_ace_account does not compile: column a.core_banking_system_date does not exist |
| Conformance check 2 | A constraint references `public` | fk_case_account_account_key references public.account; no constraint in recovery may reference another schema |
| Conformance check 3 | A view has no dictionary row | v_ace_account.legacy_bucket has no data dictionary entry |
| Conformance check 4 | `recovery_svc` holds a privilege in `public` or can write a view | recovery_svc holds SELECT on public.account; the recovery role reads the views only |
| Build log | A recovery class names a `public` table | Boundary rule BND-6 broken: AccountReader reads public.account. Read recovery.v_ace_account instead. |
| SQLSTATE 42501 | `recovery_svc` selects a public table or writes a view | permission denied for schema public |
| SQLSTATE 23505 | A second row for one ACE key in an extension table | duplicate key value violates unique constraint party_ext_pkey |

No `MSG-` ID applies: this story has no user-facing message. Pipeline and build log text is for developers and is not part of the message standard.

## 15. Screens and states

No screen in this story. The platform administrator reads the deployment result in the pipeline run and on SCR-44 Interface and job monitor, which shows V0002 and V0003 with their status and the conformance result under Platform administration R. A developer reads the conformance test and boundary rule BND-6 in the pull request checks.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-069-01 | AC1, BR1, BR2 | System | Clean PostgreSQL 17 container: ACE Schema PostgreSQL v1.sql, V0001, then V0002; a repeated V0002 run |
| TC-E1-069-02 | AC2, BR3 | Access | Sessions as recovery_svc, ace_view_owner and a test role with no grant in SIT |
| TC-E1-069-03 | AC3, BR1, BR9 | System | Tier 2 probe with the 14 tables; then V0003 on a database without public.valuation |
| TC-E1-069-04 | AC4, BR4 | System | Branch adding fk_case_account_account_key to public.account |
| TC-E1-069-05 | AC5, BR5 | System | 122 objects and 1,366 fields; a view column with no sys_fields row |
| TC-E1-069-06 | AC6, BR6 | System | Account ACC0000017 with delay_days 95; dictionary query |
| TC-E1-069-07 | AC7, BR7 | System | Duplicate person_key P0000123 in party_ext; column list of the four tables |
| TC-E1-069-08 | AC8, BR8 | System | Fixture AccountReader on public.account and on recovery.v_ace_account; native query fixture |

The full test, with its Given, When and Then, is added to Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: the view list and the role names are configuration and data, not constants in a service.
- No personal data in logs, tests or prompts: test rows are synthetic; the customer view returns `id_no_masked` and `id_no_last4` only and never the clear identity number.
- No read of a `public` table and no write to an ACE table: the database grants and boundary rule BND-6 enforce it, and a breach is a defect.
- The views are forward only in PROD; a wrong view is corrected by a new migration, never by editing an applied one.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-RDF-002 | Account balance, arrears, payments and classification for every account at 90 or more days past due are read from ACE through `v_ace_account` and `v_ace_payment`, current to the previous working day | Business Requirements Epic 1, sections 3.1 and 4 | FEAT-RDF-01 | All recovery processes | D-RCV-35 U4; BR-P1-001-2; BR-P1-001-3 | TC-E1-069-01, TC-E1-069-02, TC-E1-069-03, TC-E1-069-05, TC-E1-069-06 |
| REQ-DRI-006 | No component calls a system of record directly | Business Requirements Program, sections 5.2 and 7 | FEAT-RDF-01 | All recovery processes | ADR-010; DL43 | TC-E1-069-04, TC-E1-069-08 |
| D-RCV-35 U4 | The Workbench reads ACE only through the views and holds no copy | Decision log, D-RCV-35 section 6.1; ADR-010 | FEAT-RDF-01 | All recovery processes | ADR-010; CTL-02 | TC-E1-069-01 to TC-E1-069-08 |

## 19. Out of scope

- The 14 Tier 2 tables and the 12 columns that RWB-ACE-001 adds to `account`, `customer` and `efs_action`: the ACE team owns them, and this story neither creates nor alters them.
- The features that read a Section B view: their own stories, behind their flags until V0003 is applied.
- Masking at the API and the PII access log: RWB-E1-037 and RWB-E1-016.
- The data dictionary content and its maintenance: RWB-E1-001 for the metadata rows and RWB-E1-064 for the dictionary of the 14 data products.
- The rest of RWB-TE-001: this story adds boundary rule BND-6 and the `sourceViews` list only.
- Any change to the 30-view list: the data architect and the recovery tech lead, with a new version of the ACE Data Tier Map v1.
