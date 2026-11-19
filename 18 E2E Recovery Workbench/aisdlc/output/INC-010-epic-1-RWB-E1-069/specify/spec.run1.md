---
title: "Technical Specification — RWB-E1-069 Read-only ACE source views, grants and boundary rule"
run_id: "INC-010-epic-1-RWB-E1-069"
story: "RWB-E1-069"
status: "SUCCESS"
---

# Technical Specification — RWB-E1-069 Read-only ACE source views, grants and boundary rule

| Field | Value |
|---|---|
| Story | RWB-E1-069. Epic E1. Module P1 Recovery data engine. Feature FEAT-RDF-01. Priority Must. |
| RUN_ID | `INC-010-epic-1-RWB-E1-069` |
| Increment card | `aisdlc/docs/increments/INC-010-epic-1-RWB-E1-069.md`. Build order 10 of 72 (Build Sequence v6). |
| Source requirement | [S1] Story RWB-E1-069 v1, from Epic 1 Story Files v7, dated 15 Nov 2026 |
| Upstream IDs | REQ-RDF-002, REQ-DRI-006 → BR-RWB-013 → FR-RWB-013 (`aisdlc/requirement/Traceability_Matrix.md` row 010). D-RCV-35 U1 and U4. ADR-010. DL43. |
| Depends on | RWB-E1-001 (V0001; INC-009, not built). RWB-TE-001 (module map; INC-002). RWB-E1-044 (Flyway; INC-001, baseline exists under audit A-04). RWB-ACE-001 (external, ACE team; Section B only). |
| Blocks | RWB-E1-002, RWB-E1-016, RWB-E1-018 |
| Gate | **The spec gate returned FAIL** (`../review/spec-gate-review.md`: 3 High, 6 Medium, 7 Low). The handoff is blocked until the findings are remediated and re-reviewed, or explicitly accepted. |
| Status | `SUCCESS` as the specifier first wrote it. Every AC and BR is mapped. The 21 document gaps are recorded in `document-gaps.md`. None is a blocker: each is settled by the RUN-BRIEF precedence rule or by a documented default. |
| Prepared | 2026-11-17, by the Technical Specifier (agent run). There is no `_v2-baseline` for this RUN_ID, so this is the first specification. |

## Sources

Paths marked `legacy/` are relative to `<docset>/17 AI-First SDLC Repository v2/requirement/legacy/`.

| Tag | Document, version | Path |
|---|---|---|
| S1 | Story RWB-E1-069 v1, Epic 1 Story Files v7, 15 Nov 2026 | `legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-069-read-only-ace-source-views-grants-and-boundary-rule-v1.md` |
| S2 | Recovery Workbench ACE Source Views v1 | `legacy/15-ace-db-alignment/recovery-workbench-ace-source-views-v1.sql` |
| S3 | Recovery Workbench Physical Schema v6, 16 Nov 2026 | `legacy/06-data/recovery-workbench-physical-schema-v6.sql` |
| S4 | ACE Team Stories v1, story RWB-ACE-001 | `legacy/04-user-stories/recovery-workbench-ace-team-stories-v1.md` |
| S5 | Story RWB-E1-001 v1, Epic 1 Story Files v7 | `legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-001-recovery-tables-for-the-14-data-products-v1.md` |
| S6 | RWB-E1-001 Specification Rulings v2 | `legacy/01-decisions-and-governance/recovery-workbench-rwb-e1-001-specification-rulings-v2.md` |
| S7 | Architecture Decision Records v3, ADR-010 | `legacy/05-technical-architecture/recovery-workbench-architecture-decision-records-v3.md` |
| S8 | Decision Log v10 (DL43) | `legacy/01-decisions-and-governance/recovery-workbench-decision-log-v10-xlsx.md` |
| S9 | Client decision D-RCV-35, ACE DB alignment | `aisdlc/docs/decisions/d-rcv-35-ace-db-alignment.md` |
| S10 | D-RCV-28, D-RCV-34, D-RCV-37 | `aisdlc/docs/decisions/INC-001-decisions.md` |
| S11 | Build Notes Epic 1 v6 | `legacy/04-user-stories/recovery-workbench-build-notes-epic-1-v6.md` |
| S12 | Environment and Deployment Design v4 | `legacy/05-technical-architecture/recovery-workbench-environment-and-deployment-design-v4-docx.md` |
| S13 | Security and Access Design v4 | `legacy/05-technical-architecture/recovery-workbench-security-and-access-design-v4-docx.md` |
| S14 | Build Sequence Epic 1 and Epic 2 v6 | `legacy/11-delivery-and-operations/recovery-workbench-build-sequence-epic-1-and-epic-2-v6-xlsx.md` |
| S15 | ACE Schema PostgreSQL v1 | `legacy/15-ace-db-alignment/ace-schema-postgresql-v1.sql` |
| C1 | backend-context (CONTEXT-20261116) | `aisdlc/.github/contexts/backend-context.md` |
| C2 | backend-standards (BS-*) | `aisdlc/.github/contexts/backend-standards.md` |
| C3 | testing-standards | `aisdlc/.github/contexts/testing-standards.md` |
| E1 | Phase 0 standards audit (A-02, A-04) | `aisdlc/evidence/phase0-standards-audit.md` |
| R1 | Repository README ("Local vs target"; "Decisions taken while setting this up" 1–7) | `README.md` |
| T1 | RWB-TE-001 v2 spec (SPEC-RWB-TE-001-002, -021) | `aisdlc/output/INC-002-epic-1-RWB-TE-001/_v2-baseline/specify/spec.md` |

**Code baseline, read only (audit A-04).** All paths are under `backend/src/`:
- `main/java/th/co/scb/ace/demo/recovery/platform/internal/RecoveryFlywayConfig.java`
- `test/java/th/co/scb/ace/demo/recovery/architecture/RecoveryBoundaryTest.java`
- `test/java/th/co/scb/ace/demo/recovery/architecture/RecoveryMigrationLintTest.java`
- `test/java/th/co/scb/ace/demo/recovery/RecoveryDatabaseIT.java`
- `PlatformInfoController.java`
- `main/resources/db/modulemigration/recovery/README.md`

The local database init is in `infra/postgres/init/` (`00-roles-and-databases.sh`, `10-load-ace-database.sh` and `20-grants.sql.inc`) and `infra/postgres/schema/02-ace-tier2-probe.sql`.

## User story intent interpretation

The recovery module reads ACE source data only through 30 `recovery.v_ace_*` views, and it can only SELECT from them. Section A has 16 views and 177 fields over tables that ACE holds today. Section B has 14 views and 127 fields over the tables that RWB-ACE-001 adds ([S1] §1, §2; [S9] U1, U4; [S7] ADR-010).

The boundary is enforced in two places:
- **In the catalog.** `ace_view_owner` owns the views. `recovery_svc` holds SELECT on the views and no privilege in `public`. PUBLIC holds nothing.
- **In the build.** Boundary rule BND-6 fails the build when a recovery class names a `public` table ([S1] §2).

The story owns no business row, no endpoint and no screen ([S1] §9, §12, §15). It delivers the following:
- two migrations;
- one conformance test class;
- the hardened BND-6 rule and the `sourceViews` list;
- the scoped migration-lint exception that lets the two files exist under D-RCV-28.

## Change Scope Declaration

| Item | Value |
|---|---|
| Change Type | `NEW_STORY`. Row 010 of the trace chain says "No current spec/plan". No v_ace view migration, conformance test or `sourceViews` exists in the code. |
| UI In Scope | NO. [S1] §15 says "No screen in this story". SCR-44 only reads the deployment result, outside this story. |
| Logic In Scope | YES. It covers the grants, the read boundary, BND-6, the conformance checks and the migration-lint rule. |
| API In Scope | NO. [S1] §12 says "No endpoint and no event". |
| API Impact Type | `NO_API_CHANGE` |
| Impacted Existing Nodes | `RecoveryBoundaryTest` (BND-6 hardened), `RecoveryMigrationLintTest` (scoped exception) and `RecoveryDatabaseIT` (extended to Flyway mode). The local stand-in `infra/postgres/init/20-grants.sql.inc` gets a Flyway-mode branch (SPEC-015). |
| New Nodes Required | YES. The changes are listed below. |
| Inherited Existing Behavior | `RecoveryFlywayConfig` settings (BS-2.3); the D-RCV-28 lint rules for every other story; `PlatformInfoController` and its `visiblePublicTables` = 0 contract; BND-5 and the Temporal determinism rules; the four extension tables and the dictionary rows created by V0001 (RWB-E1-001). |
| Frontend Changes Required | NO. `frontend/src/modules/recovery/api/platform.ts` reads `database.visiblePublicTables`, and that response is unchanged. |
| Backend Changes Required | YES. The changes are SQL migrations, test classes and a test resource. No main-source Java class is expected to change. |

New nodes:
- two migration files;
- `ViewConformanceTest`;
- the `sourceViews` key in `backend/src/test/resources/architecture/recovery-modules.yaml`;
- the BND-6 test fixtures;
- the migration-lint exception resource.

## Entry trigger and preconditions

- **Trigger.** The pipeline step `migrate` runs at deployment (RWB-E1-044). Locally, Flyway runs at application start and in `RecoveryDatabaseIT` ([S1] §12; `RecoveryFlywayConfig`).
- **P1.** V0001 of RWB-E1-001 has been applied. It created the recovery tables, including the four extension tables, the dictionary rows and `v_data_dictionary` ([S1] §3, §4 step 1; [S5]). Locally this is not yet true (INC-009 is not built). It is a build-order dependency. See DG-L17.
- **P2.** The ACE schema holds the 21 Tier 1 tables. Verified: all 21 names in [S1] §11 exist in [S15].
- **P3.** The roles `ace_view_owner` and `recovery_svc` exist ([S1] §3). Locally, `00-roles-and-databases.sh` creates them. This story does not create roles (DG-L09).
- **P4.** For the duration of the release window, the migration account can do three things ([S1] §3): grant on schema `public`, grant SELECT on the source tables, and set a view owner.
- **P5.** The module map exists at the D-RCV-37 path ([S1] §3; [S10] D-RCV-37). It is absent locally (audit A-02). See DG-L17 and ASM-006.
- **P6.** Section B only: RWB-ACE-001 is deployed ([S1] §3; [S8] DL43). Locally, `02-ace-tier2-probe.sql` (with `RWB_ACE_TIER2_PROBE=true`) stands in for it ([R1] "Local vs target").

## Backend Specification

### Specification items

| SPEC ID | Specification | Source |
|---|---|---|
| `SPEC-RWB-E1-069-001` | **Section A migration file.** Named `V<seq>__rwb_e1_069_ace_source_views.sql` and placed in `backend/src/main/resources/db/modulemigration/recovery/`. Line 1 is `-- Story: RWB-E1-069`. The file has no `SET search_path`, which `RecoveryMigrationLintTest` forbids. Every recovery object is written with the `${recoverySchema}.` qualifier. `<seq>` is the next free four-digit sequence at merge; it is `0002` when it merges directly after V0001. The file holds no environment name. | [S1] §4 steps 1–2, §12; [S10] D-RCV-28; C2 BS-2.3; DG-L04, DG-L15 |
| `SPEC-RWB-E1-069-002` | **Helper functions.** The file carries `ace_to_date`, `ace_to_boolean` and `ace_mask_value` exactly as written in [S2] lines 31–86, as `CREATE OR REPLACE FUNCTION ${recoverySchema}.<name>`. If V0001 has already created them, the statement leaves them as they are. The file then revokes EXECUTE on the three functions from PUBLIC and grants EXECUTE to `recovery_svc` (see the note below). | [S1] §4 step 1, BR6; [S1] §12 "PUBLIC holds nothing"; DG-L02; ASM-003 |
| `SPEC-RWB-E1-069-003` | **The 16 Section A views (A1–A16).** They are copied verbatim from [S2] lines 94–452. Only the `recovery.` qualifier changes, to `${recoverySchema}.`. Every `public.<table>` qualifier stays as it is. [S3] lines 6199–6564 hold the same 30 view bodies; a diff of the A1–B14 ranges is empty. No other `v_ace_*` view is created. The views have no primary key and no foreign key. | [S1] §4 step 1, §12, §13; AC1 |
| `SPEC-RWB-E1-069-004` | **Section A grant block.** The statements run in the order listed below. No `ON ALL TABLES` grant is issued to `recovery_svc`. | [S1] §12, BR2, BR3; [S7] ADR-010; DG-L11, DG-L12 |
| `SPEC-RWB-E1-069-005` | **Section B migration file.** Named `V<seq>__rwb_e1_069_ace_tier2_views.sql`, with the same header rules as SPEC-001. `<seq>` is the next free sequence when the file merges. It merges only after RWB-ACE-001 is deployed in the environments that main deploys to. A file in the Flyway location cannot be "skipped" and applied later, because the configuration sets `outOfOrder(false)` and has one history table (DG-L20). In this repository the Tier 2 probe stands in for RWB-ACE-001, so the file is built and tested here (ASM-005). | [S1] §4 steps 7–8, §13 step 7, BR9; `RecoveryFlywayConfig` |
| `SPEC-RWB-E1-069-006` | **The 14 Section B views (B1–B14) and their grants.** They are copied verbatim from [S2] lines 461–711, with the same qualifier rule as SPEC-003. The grant pattern is SPEC-004 steps 4–7 for the 14 views. V0003 grants no SELECT on a Tier 2 table: RWB-ACE-001 grants that to `ace_view_owner` ([S1] §4 step 6; [S4] flow step 5). | [S1] §4 step 7, §12; AC3 |
| `SPEC-RWB-E1-069-007` | **Extension tables are verified, not created.** `party_ext`, `contact_point_ext`, `account_ext` and `valuation_ext` ship in V0001. Neither E1-069 file creates or alters them. The tests (SPEC-011) prove the shape that [S1] §13 and [S3] lines 2087–2154 define. | [S1] §4 step 1; [S5]; [S3] header; DG-L01 |
| `SPEC-RWB-E1-069-008` | **`ViewConformanceTest`.** Placed in `backend/src/test/java/th/co/scb/ace/demo/recovery/` and tagged `@Tag("recovery-it")`. It runs on Testcontainers PostgreSQL 16 (`postgres:16.16-alpine`) after Flyway, and it uses the [S1] §14 message texts. Each check has a failing fixture ([S1] §13 step 4). The four checks are listed below. | [S1] §4 step 4, §13, §14; X1, X3, X4, X5; C3; DG-L14 |
| `SPEC-RWB-E1-069-009` | **Access tests (AC2).** The tests open JDBC sessions as three roles. For `rwb_no_grant`, the test fixture creates the role with LOGIN and gives it USAGE on schema `recovery` only, so that the failure is caused by the missing view privilege and not by schema access. The detailed assertions are listed below. | [S1] AC2, BR2, BR3, X5 |
| `SPEC-RWB-E1-069-010` | **Dictionary tests (AC5, AC6).** The checks are listed below. | [S1] AC5, AC6, BR5; DG-L05 |
| `SPEC-RWB-E1-069-011` | **Extension-table tests (AC7).** The checks are listed below. | [S1] AC7, BR7, X7; [S3] lines 2087–2154 |
| `SPEC-RWB-E1-069-012` | **BND-6 hardening in `RecoveryBoundaryTest`.** This extends the existing `bnd6`-style rule. It does not add a second rule class elsewhere (audit A-04). The full rule is set out in the BND-6 subsection below. | [S1] AC8, BR8, X6, §13, §14; E1 A-02; T1 SPEC-021 |
| `SPEC-RWB-E1-069-013` | **Module map `sourceViews`.** The top-level key `sourceViews` is added to `backend/src/test/resources/architecture/recovery-modules.yaml` ([S10] D-RCV-37). It is a list of the 30 view names in [S1] §11, in that order. It is the only allowed-source list. The test fails if the list does not equal, as a set, the views created by the E1-069 migration files. The rest of the map belongs to RWB-TE-001 ([S1] §19). | [S1] §4 step 5, §13; T1 ASM-016; ASM-006 |
| `SPEC-RWB-E1-069-014` | **Scoped migration-lint exception.** `RecoveryMigrationLintTest` reads a test resource, `backend/src/test/resources/db/recovery-migration-lint-exceptions.yaml`. The resource has one entry, set out in the lint subsection below. For every other story key the lint behaves as it does now. | [S9] §3.2, §8.2; [S1] §12; [S10] D-RCV-28; C2 BS-2.2, BS-2.5, BS-2.6; DG-L03 |
| `SPEC-RWB-E1-069-015` | **Local stand-in for P4 and the integration test.** The details are set out in the local stand-in subsection below. | [S1] §3; [R1] "Local vs target"; DG-L13, DG-L17 |
| `SPEC-RWB-E1-069-016` | **No API, UI or main-code change.** `PlatformInfoController` stays as it is and must stay green under the hardened BND-6. Its reads of `information_schema.views` and `information_schema.tables` are allowed, including the count filtered on the literal `'public'` (decision below). | [S1] §12, §15; [R1] decision 6; [S10] D-RCV-28 (2) |

### SPEC-002: why EXECUTE is revoked and granted

A caller of a view needs EXECUTE on the functions that the view calls. PostgreSQL grants EXECUTE to PUBLIC by default. The file therefore revokes EXECUTE from PUBLIC and grants it explicitly to `recovery_svc`.

### SPEC-004: Section A grant block, in order

1. `GRANT USAGE ON SCHEMA public TO ace_view_owner`.
2. `GRANT SELECT ON` the 21 Tier 1 tables listed in [S1] §12 `TO ace_view_owner`. Name the tables. Never use `ON ALL TABLES IN SCHEMA public`.
3. `GRANT CREATE ON SCHEMA ${recoverySchema} TO ace_view_owner`. This is temporary: PostgreSQL requires a new owner to hold CREATE on the schema.
4. For each of the 16 views: `REVOKE ALL ON ${recoverySchema}.<view> FROM PUBLIC, recovery_svc`. This removes any default-privilege grant. The local `20-grants.sql.inc` sets `ALTER DEFAULT PRIVILEGES ... GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO recovery_svc`, and views are covered by `ON TABLES`.
5. `ALTER VIEW ${recoverySchema}.<view> OWNER TO ace_view_owner`, once for each view.
6. `GRANT SELECT ON ${recoverySchema}.<view> TO recovery_svc`, once for each view.
7. `REVOKE CREATE ON SCHEMA ${recoverySchema} FROM ace_view_owner`. After this, `ace_view_owner` holds no privilege on schema `recovery` (BR2).
8. `GRANT USAGE ON SCHEMA ${recoverySchema} TO recovery_svc`.
9. `REVOKE ALL ON ALL TABLES IN SCHEMA ${recoverySchema} FROM PUBLIC`.

### SPEC-008: the four conformance checks

1. **Compile check.** Every `v_ace_*` view in schema `recovery` returns from `SELECT * FROM <view> LIMIT 1`. The test asserts the exact view count: 16 after Section A, 30 after Section B. A failure names the view and the database error, using the form "`<view>` does not compile: `<error>`".
2. **Constraint check.** No constraint in `recovery` (`pg_constraint`) references a relation or type in another schema. This covers `confrelid` and the columns' type namespaces. The failure text is "`<conname>` references `<schema>.<table>`; no constraint in recovery may reference another schema".
3. **Dictionary check.** Each `v_ace_*` view has one `sys_objects` row, and each of its columns has one `sys_fields` row. The failure text is "`<view>.<column>` has no data dictionary entry".
4. **Privilege check.** `recovery_svc` holds no privilege on any relation in `public`, and has no USAGE on `public`. It holds no INSERT, UPDATE, DELETE, TRUNCATE, REFERENCES or TRIGGER on any `v_ace_*` view. The failure text is "recovery_svc holds `<priv>` on `<object>`; the recovery role reads the views only".

### SPEC-009: access assertions

- **As `recovery_svc`:**
  - `SELECT` from `v_ace_account` returns rows. A synthetic row is inserted by the test as a superuser.
  - `SELECT` from `public.account` fails with 42501.
  - `INSERT`, `UPDATE` and `DELETE` on `v_ace_account` each fail with 42501.
  - `has_schema_privilege('recovery_svc','public','USAGE')` is false.
  - `has_table_privilege('recovery_svc','public.account','SELECT')` is false.
  - `has_table_privilege('recovery_svc','recovery.v_ace_account','INSERT')` is false.
- **`ace_view_owner`:**
  - owns the 16 (later 30) views;
  - holds SELECT on the 21 (later 35) source tables;
  - holds no INSERT, UPDATE or DELETE on them;
  - holds no privilege on schema `recovery` (BR2).
- **`rwb_no_grant`:** `SELECT` on `v_ace_account` fails with 42501, and `has_table_privilege` is false.

**Message text for the `public.account` failure.** [S1] AC2 expects the text "permission denied for schema public". That text is produced only when USAGE on schema `public` is not held through PUBLIC. ACE owns schema `public`, so this is an ACE DBA precondition (DG-L13). Locally, `20-grants.sql.inc` provides it. The test asserts SQLSTATE 42501, and also the message text whenever `has_schema_privilege('public','USAGE')` is false for PUBLIC.

### SPEC-010: dictionary assertions

- The 30 `v_ace_*` objects hold 304 fields: 177 in Section A (DF-ACE-001..177) and 127 in Section B (DF-ACE-178..304).
- The field ID ranges match [S1] §11 for each view.
- The four extension tables hold 49 fields, DF-EXT-001..049.
- Each view has a one-to-one match between its catalog columns and its `sys_fields` rows.
- `v_data_dictionary` for `v_ace_account.days_past_due` returns the following values:

  | Column | Value |
  |---|---|
  | field ID | DF-ACE-018 |
  | data type | NUMBER |
  | physical type | integer |
  | source system | ACE |
  | source field | `public.account.delay_days` |
  | data product | DP01 |
  | refresh cycle | DAILY |

- A synthetic ACE account `ACC0000017` with `delay_days` 95 reads back as `days_past_due` 95 through the view.

The totals of 122 objects and 1,366 fields belong to V0001. They are asserted as the values that the RWB-E1-001 specification fixes (`INHERITED_EXISTING_BEHAVIOR`; [R1] decision 7).

### SPEC-011: extension-table assertions

| Table | Columns | Primary key | Other checks |
|---|---|---|---|
| `party_ext` | 12 | `person_key` | — |
| `contact_point_ext` | 14 | `contact_key` | Check `ck_contact_point_ext_type` allows PHONE, EMAIL and ADDRESS |
| `account_ext` | 9 | `account_key` | — |
| `valuation_ext` | 14 | `valuation_key` | — |

- The four tables hold 49 columns in total.
- No foreign key on the four tables references schema `public`.
- A second `party_ext` row for the synthetic key `P0000123` fails with 23505 on `party_ext_pkey`, and exactly one row remains.

### SPEC-012: the BND-6 rule

**Detection.** The rule scans the recovery main sources, `src/main/java/th/co/scb/ace/demo/recovery/**`. It reads each whole file with comments removed, not line by line, so it catches the following:
- (a) `public.<ident>` with optional spaces and quotes, such as `"public"."account"` or `public . account`, inside string literals, text blocks and concatenated strings that span lines;
- (b) a JPA `@Table`, `@SecondaryTable` or `@JoinTable` with `schema = "public"`;
- (c) SQL inside `@Query`, `@NamedNativeQuery` and `@NamedQuery`, and string arguments to `JdbcTemplate` or `JdbcClient`;
- (d) an unqualified ACE source table name after `FROM`, `JOIN`, `UPDATE`, `INTO` or `TABLE` (see the A-02 decision below).

**Allowed names.** The allowed names are read from `sourceViews` in the module map (SPEC-013). They are not written into the test.

**Not flagged.** References qualified with `information_schema.` or `pg_catalog.`, and the string literal `'public'` used as a catalog filter value. This follows [S10] D-RCV-28 (2).

**Failure message.** The message follows [S1] §14 exactly: "Boundary rule BND-6 broken: `<SimpleClassName>` reads public.`<table>`. Read recovery.`<view>` instead." `<view>` is `v_ace_<table>` when that name is in `sourceViews`. Otherwise the message ends "Read a recovery.v_ace_* view instead."

**Fixtures.** The fixtures are test-only classes under a fixture package (ASM-007):
- `AccountReader` reading `public.account` fails;
- the same class reading `recovery.v_ace_account` passes;
- a native query `select delay_days from public.account` fails;
- an unqualified `select delay_days from account` fails;
- a copy of the `PlatformInfoController` query pattern passes.

**Where it runs.** The rule runs in the default `test` task.

### SPEC-014: the lint exception entry

The entry is `storyKey: rwb_e1_069`, citing `D-RCV-35 §3.2/§8.2`. It allows exactly three things, and only in files whose name carries `rwb_e1_069`:
- (a) up to two non-fix files for the key;
- (b) the qualifier `public.`;
- (c) `GRANT`, `REVOKE` and `ALTER VIEW ... OWNER TO`.

Even in those files, the literal qualifiers `recovery.` and `ace.` still fail.

### SPEC-015: local stand-in and integration test

**(a) Flyway-mode init.** When `RWB_LOAD_REFERENCE_SCHEMA=false`, `20-grants.sql.inc` gives `rwb_migrator` three things. Together they stand in for "the ACE DBA role for the release window":
- `USAGE ON SCHEMA public WITH GRANT OPTION`;
- `SELECT ... WITH GRANT OPTION` on the 35 source tables;
- membership of `ace_view_owner`.

In this mode it does not pre-grant `USAGE`/`CREATE` on `recovery` to `ace_view_owner`, nor `SELECT ON ALL TABLES IN SCHEMA public` to it; V0002 does that work. Reference mode is unchanged. The breadth of the reference-mode grant is recorded as a local deviation, ASM-008.

**(b) `RecoveryDatabaseIT`.** It is extended with a Flyway-mode container: ACE v1, the Tier 2 probe, `RWB_LOAD_REFERENCE_SCHEMA=false`, then V0001 + E1-069 files. It hosts SPEC-008 to SPEC-011. Its existing reference-mode tests stay as they are.

**(c) Tier 2 probe off.** A second Flyway-mode container runs with the Tier 2 probe off. It proves that V0003 fails with "relation public.valuation does not exist" and leaves the 16 Section A views unchanged (X2).

### Decision on audit A-02: the `PlatformInfoController` read is permitted

1. BR8 forbids a recovery class to *name a table in schema `public`* ([S1] BR8). `information_schema.tables` is an SQL-standard catalog view. It is neither a `public` table nor ACE source data.
2. D-RCV-28 (2) allows the `information_schema` and `pg_catalog` qualifiers explicitly ([S10]).
3. ADR-010's "nothing else" restricts *privileges* ([S7]). `information_schema` returns only the objects that the caller holds a privilege on. The query therefore reads no ACE data. It proves the boundary: `visiblePublicTables` must be 0, which `PlatformE2ETest` asserts.
4. The endpoint is a recorded local operational endpoint ([R1] decision 6).

The hardened rule must keep this class green (SPEC-016).

### Decision on audit A-02: unqualified names (design derived from the audit, not from [S1])

At run time the catalog is the backstop:
- `recovery_svc` has `search_path=recovery` (`00-roles-and-databases.sh`).
- `recovery_svc` has no USAGE on `public`.

An unqualified `account` therefore fails to resolve, with 42P01 or 42501.

At build time, detector (d) flags an unqualified name that is in the ACE source-table set but is not a recovery table:
- **ACE source-table set.** It is derived at test time from the `public.<name>` qualifiers in the E1-069 migration files, the only files the lint lets carry them. It is not a new literal list.
- **Recovery tables.** They are derived from the `CREATE TABLE` statements in the recovery migrations.

Today the only name in both sets is `hearing`: `recovery.hearing` in [S3], and ACE Tier 2 `public.hearing` in [S4]. Unqualified, `hearing` resolves to `recovery.hearing` and is allowed.

## Field-level behavior matrix

There is no user-entered field. The published read interface is the views. Columns are cited, not copied: per-view field IDs are in [S1] §11, and each column definition is in the [S2] view body.

| Object | Source of each column | Editable | Constraint |
|---|---|---|---|
| 16 Section A views (177 fields, DF-ACE-001..177) | [S2] A1–A16 over the 21 Tier 1 tables | No (SELECT only) | No PK or FK. Text dates go through `ace_to_date` and Y/N flags through `ace_to_boolean`, both returning NULL rather than failing (BR6). `v_ace_customer` exposes `id_no_masked` and `id_no_last4` only ([S1] §17). |
| 14 Section B views (127 fields, DF-ACE-178..304) | [S2] B1–B14 over the 14 Tier 2 tables of RWB-ACE-001 | No | Same rules as Section A. Created only after RWB-ACE-001 (BR9). |
| `v_ace_account.days_past_due` | `public.account.delay_days` ([S2] A1; [S3] DF-ACE-018) | No | integer |
| 4 extension tables (49 fields, DF-EXT-001..049) | Created by V0001; shape per [S1] §13 and [S3] | Written by later stories ([S1] §11) | 1:1 on the ACE business key, `varchar(255)`. No FK into `public` (BR4, BR7). |
| `sourceViews` (module map) | [S1] §11 view list, frozen in ACE Data Tier Map v1 ([S1] §13) | Changed only by the data architect and the recovery tech lead ([S1] §10) | Exactly 30 names, equal to the migrated set |

## Status-transition matrix

The story changes no case status ([S1] §9). Schema states:

| Source state | Condition | Target state |
|---|---|---|
| `recovery` at V0001 | Section A file applied successfully | 16 views, Section A grants, history row for the Section A version |
| `recovery` at V0001 | Section A file fails (X1) | Transaction rolled back. No view from the run exists; V0001 objects are unchanged. |
| Section A applied | RWB-ACE-001 deployed, Section B file applied | 30 views, history row for the Section B version |
| Section A applied | Section B applied without the Tier 2 tables (X2) | Rolled back. 16 views unchanged; Section B features stay behind their flags. |
| Any applied version | Same version run again | Flyway reports "already applied" and nothing changes ([S1] AC1, §12 Idempotency) |

## Exceptional-case behavior

| ID | Trigger | Behaviour | Check | SPEC |
|---|---|---|---|---|
| X1 | A Section A view does not compile | Migration rolls back. Pipeline log names the view and the column. | Conformance check 1 | 003, 008 |
| X2 | Section B applied before RWB-ACE-001 | Fails with "relation public.valuation does not exist". The 16 views are unchanged. | IT (SPEC-015 c) | 005, 006 |
| X3 | A recovery constraint references `public` | Conformance check 2 fails and the merge is blocked | Fixture FK `fk_case_account_account_key` | 008 |
| X4 | A view column has no `sys_fields` row | Conformance check 3 fails and names `v_ace_account.legacy_bucket` | Fixture column | 008, 010 |
| X5 | `recovery_svc` holds a `public` privilege or a write on a view | Conformance check 4 fails and names the privilege | Fixture grant | 004, 008, 009 |
| X6 | A recovery class names a `public` table | Build fails with the BND-6 message | Fixture `AccountReader` | 012 |
| X7 | A second extension row for one ACE key | 23505 on `party_ext_pkey`; the first row is unchanged | IT | 011 |
| X8 (derived) | A default privilege grants DML on a new view to `recovery_svc` | Removed by the per-view `REVOKE ALL` before the owner change | Conformance check 4 | 004 |
| X9 (derived) | Lint run over the E1-069 files without the exception | Would fail on `public.`, GRANT and the second file. The exception admits only this key. | Lint test with a fixture of another key carrying `public.`, which must fail | 014 |

## API change assessment

| Item | Value |
|---|---|
| Impact type | `NO_API_CHANGE`. [S1] §12 says "No endpoint and no event". |
| Contract delta | None. `contracts/backend-apis.json` records the non-HTTP contracts: migrations, grants and module map. |
| Backward compatibility | `GET /api/recovery/v1/platform/info` is unchanged. `visiblePublicTables` stays 0 under the new grants. |

## Frontend Specification

No frontend change. UI In Scope = NO. There is no screen ([S1] §15) and no API delta. Per-screen design documentation is N/A.

## Requirement-to-SPEC Logic Coverage

| REQ_REF | Requirement Logic Statement | Mapped SPEC-* | Coverage Type | Implementation Notes | Status |
|---|---|---|---|---|---|
| AC1 | 16 Section A views compile, are applied once and are idempotent; extension tables present; no other view | 001, 003, 007, 008 | DIRECT | Extension tables verified, not created (DG-L01) | COVERED |
| AC2 | `recovery_svc` reads only through the views; 42501 on `public` and on writes; `rwb_no_grant` is denied | 004, 009 | DIRECT | Message text depends on the ACE DBA revoking PUBLIC USAGE on `public` (DG-L13) | COVERED |
| AC3 | 14 Section B views compile after RWB-ACE-001; 30 of 30; failure without `public.valuation` | 005, 006, 015 | DIRECT | Merge gated on RWB-ACE-001; probe stands in locally (DG-L16, DG-L20) | COVERED |
| AC4 | No recovery constraint references `public` | 008 | DIRECT | Check 2 with fixture FK | COVERED |
| AC5 | Every view has dictionary rows (30/304/177/127; 49 ext) | 008, 010 | DIRECT | Totals 122/1,366 inherited from V0001 | COVERED |
| AC5 (totals) | 1,366 fields over 122 objects | 010 | INHERITED_EXISTING_BEHAVIOR | Seeded by V0001 (RWB-E1-001). [R1] decision 7 notes 123/1,379 in [S3]; RWB-E1-001 settles which. | COVERED |
| AC6 | `days_past_due` comes from `delay_days`; DF-ACE-018 attributes | 003, 010 | DIRECT | Dictionary row from V0001; value read through the view | COVERED |
| AC7 | Four extension tables 1:1 on the ACE key; 49 columns; 23505 on duplicate | 007, 011 | DIRECT | — | COVERED |
| AC8 | BND-6 allows only `recovery.v_ace_*`, read from the module map; fails on `public.account` and on native query | 012, 013 | DIRECT | Extends the existing rule (A-04) | COVERED |
| BR1 | Read only through the 30 SELECT-only views; nothing loaded or copied | 003, 006, 012 | DIRECT | — | COVERED |
| BR2 | `ace_view_owner` owns the views, SELECT on the ACE tables, writes nothing, no other right in `recovery` | 004, 009 | DIRECT | Transient CREATE grant, revoked in the same migration (DG-L12) | COVERED |
| BR3 | `recovery_svc`: SELECT on the views only on ACE data; nothing in `public`; PUBLIC nothing; no write on a view; DML on Workbench tables is outside scope | 002, 004, 008, 009 | DIRECT | DML on Workbench tables is granted by V0001 (DG-L10) | COVERED |
| BR4 | No constraint references outside `recovery`; ACE link is a `varchar(255)` key | 007, 008, 011 | DIRECT | — | COVERED |
| BR5 | `sys_objects` row and one `sys_fields` row per column | 008, 010 | DIRECT | Rows shipped by V0001 | COVERED |
| BR6 | `ace_to_date` and `ace_to_boolean` return NULL rather than fail | 002, 003 | DIRECT | Function bodies verbatim from [S2] | COVERED |
| BR7 | Extension tables hold decisions, not copies; 1:1; seven standard record columns | 007, 011 | DIRECT | — | COVERED |
| BR8 | BND-6: no recovery class names a `public` table; allow-list from the module map | 012, 013, 016 | DIRECT | A-02 hardening | COVERED |
| BR9 | Section B only after its ACE table exists; later Flyway sequence | 005, 006 | DIRECT | DG-L20 | COVERED |
| §4 step 2 | No environment name; `${recoverySchema}`; role names from [S12] | 001, 014 | DIRECT | [S12] line 64 fixes the role names | COVERED |
| §17 guardrails | View list and role names as data; synthetic data; forward-only | 001, 005, 010, 011, 013 | DIRECT | Synthetic keys `ACC0000017` and `P0000123` | COVERED |

## Unit Test Applicability

| Surface | Changes Required | Unit Tests | Coverage Gate | Requirement/SPEC References | Evidence and Rationale | Test Acceptance Criteria |
|---|---|---|---|---|---|---|
| Frontend | NO | NOT_APPLICABLE | NOT_APPLICABLE | SPEC-016 | No screen ([S1] §15). `platform.ts` consumes an unchanged response. | N/A |
| Backend | YES | REQUIRED | 80% for lines and branches, the counters that `recoveryCoverageVerification` enforces in `backend/build.gradle.kts` (C2 BS-7.2). Instructions and methods are reported, not gated. on any changed recovery main-source class. No main class is expected to change, so the gate must not regress. | SPEC-001..015 | The deliverables are SQL, test rules and a test resource. Each rule has a positive and a negative fixture ([S1] §13 step 4). | The tests are listed below, with the evidence required by `.github/rules/implementation-execution-gates.md`. |

Backend tests:
- **Unit level, `test` task:**
  - BND-6: positive, negative, native-query, unqualified-name and catalog-exemption cases;
  - lint exception: an allowed key, and a disallowed key with `public.`;
  - `sourceViews` equality.
- **`recovery-it` level:** SPEC-008 to SPEC-011 and SPEC-015 (b) and (c).

| Test case | Covers | SPEC |
|---|---|---|
| TC-E1-069-01 | AC1, BR1, BR2 | 001, 003, 007, 008 |
| TC-E1-069-02 | AC2, BR3 | 004, 009 |
| TC-E1-069-03 | AC3, BR9 | 005, 006, 015 |
| TC-E1-069-04 | AC4, BR4 | 008 |
| TC-E1-069-05 | AC5, BR5 | 008, 010 |
| TC-E1-069-06 | AC6, BR6 | 010 |
| TC-E1-069-07 | AC7, BR7 | 011 |
| TC-E1-069-08 | AC8, BR8 | 012, 013, 016 |

TC-E1-069-01 runs on PostgreSQL 16, not 17 (DG-L14).

API testing: N/A (no API). Functional UI testing: N/A (no UI).

## Clarification Log

`CLARIFICATION_STATUS: NOT_REQUIRED`

Evidence: every conflict in `document-gaps.md` is settled in one of two ways. Either the RUN-BRIEF precedence applies (D-RCV-35 → ADR v3 → Decision Log v10 → story files v7 → older), or there is a documented default. Proposed open items for owner confirmation are in `shared-updates.md`. Under L-RCV-03 no question is asked.

## Status

- `MCP_STATUS_SUMMARY: No Jira, Confluence, GitLab or Figma MCP is connected (RUN-BRIEF rule 5); the story has no UI, so no design evidence is needed.`
- `MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]`
- `CHANGE_CLASSIFICATION_SUMMARY: A new story with backend database, grant and build-rule logic only; no UI and no API.`
- `CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: NO] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: NO] [API_IMPACT: NO_API_CHANGE] [REASON: no prior SPEC for RWB-E1-069; migrations, grants and BND-6 only]`
- `REQUIREMENT_COVERAGE_SUMMARY: All 8 ACs, 9 business rules, the step-2 rule and the guardrails are mapped; no rule is missing.`
- `REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 20] [COVERED_RULES: 20] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]`
  - Source contradictions are recorded as document gaps DG-L01..L21 and are settled by precedence. None is left open in the spec.
- `DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0] [UNBLOCK_ACTION: n/a]`
