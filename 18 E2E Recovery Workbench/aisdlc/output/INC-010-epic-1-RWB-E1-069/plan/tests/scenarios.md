---
title: "Test scenarios: RWB-E1-069 Read-only ACE source views, grants and boundary rule"
run_id: "INC-010-epic-1-RWB-E1-069"
story: "RWB-E1-069"
revision: "v1 (18 Nov 2026): first plan stage for this run, against spec revision 4"
---

# Test scenarios: RWB-E1-069

Every scenario names the task that writes it, the test that runs it, and the level. `recovery-it` runs on `postgres:16.16-alpine` through `recoveryIntegrationTest`; `unit` runs in the `test` task; `build` is a Gradle task result. `ViewConformanceTest` is the single host of SPEC-008 to SPEC-011, SPEC-017, SPEC-019 and SPEC-020 (REVIEW-116). External mode (`RWB_CONFORMANCE_TARGET=external`) runs checks 1-4 only and is never reported as a local result.

Test data is synthetic throughout: `ACC0000017` (delay_days 95), `P0000123`, `X000000005678`, the six `public.payment` rows, the fixture role `rwb_no_grant`, the fixture DDL and the container passwords.

## Conformance and system scenarios

### S-01 AC1 Section A is created and compiles (TC-E1-069-01)

- **Given** a fresh Flyway-mode container (S1 `false`, S2 `false`, probe on) with the RWB-E1-001 migration applied.
- **When** Flyway migrates to the Section A version and the conformance test runs check 1 as `recovery_svc`.
- **Then** exactly 16 `v_ace_*` views exist and no other `v_ace_*` view; `SELECT * FROM ${recoverySchema}.<view> LIMIT 1` returns without error for 16 of 16; the four extension tables `party_ext`, `contact_point_ext`, `account_ext`, `valuation_ext` are present; no Section B view exists.
- **Covers** AC1.2, AC1.3, AC1.4, BR1. **Test** `ViewConformanceTest.check1` and `MigrationFolderCoverageTest`. **Tasks** TASK-08, TASK-09. **Level** recovery-it.

### S-02 AC1 history and re-run (TC-E1-069-01, SPEC-017)

- **Given** S-01's container.
- **When** the test reads `flyway_schema_history_recovery` and then calls `migrate()` a second time.
- **Then** one `success = true` row exists for the RWB-E1-001 file and one for the Section A file, Section A later by `installed_rank`; there is **no** `version = '0'` row; the second run reports `migrationsExecuted = 0`, the history is unchanged, and `recovery` still holds 16 `v_ace_*` views.
- **Covers** AC1.5, AC1.6. **Test** `ViewConformanceTest.historyAtSectionA` and `.rerunIsANoOp`. **Tasks** TASK-07, TASK-08, TASK-09. **Level** recovery-it.

### S-03 X1: a view that does not compile fails check 1 (fixture)

- **Given** S-01's container and a throwaway copy of `v_ace_account` replaced by a view over a dropped synthetic column, added after the migration and never in the migration folder.
- **When** check 1 runs.
- **Then** it fails with ``<view> does not compile: <database error>`` naming the view; the fixture is dropped and the run ends clean.
- **Covers** X1. **Test** `ViewConformanceTest.check1FailingFixture`. **Task** TASK-08. **Level** recovery-it.

### S-04 AC2 `recovery_svc` reads only through the views (TC-E1-069-02)

- **Given** S-01's container with a synthetic `public.account` row inserted as superuser (`ACC0000017`, `delay_days` 95).
- **When** a session as `recovery_svc` selects from `recovery.v_ace_account`, then from `public.account`, then runs INSERT, UPDATE and DELETE on `v_ace_account`.
- **Then** the view select returns the synthetic row with `days_past_due` 95; `public.account` fails with SQLSTATE 42501 and message `permission denied for schema public`; each write fails with SQLSTATE 42501 (`permission denied for view v_ace_account`).
- **Covers** AC2.1, AC2.2, AC2.3, BR1, BR3. **Test** `ViewConformanceTest.accessAsRecoverySvc`. **Tasks** TASK-08, TASK-09. **Level** recovery-it.

### S-05 AC2 catalog facts, checks 4 and 5 (TC-E1-069-02, T-E1-069-16)

- **Given** S-01's container, a `recovery_svc` session and a migration-account session, plus a superuser session for the catalog.
- **When** check 4 runs `has_schema_privilege` and `has_table_privilege` from the migration-account session and repeats the direct-read refusal in the `recovery_svc` session; check 5 runs in the superuser session.
- **Then** `has_schema_privilege('recovery_svc','public','USAGE')` is false; `has_table_privilege('recovery_svc','public.account','SELECT')` is false; `has_table_privilege('recovery_svc','recovery.v_ace_account','INSERT')` is false; no `recovery_svc` privilege exists on any `public` relation or for INSERT, UPDATE, DELETE, TRUNCATE, REFERENCES, TRIGGER on any view; check 5 sees `has_schema_privilege('rwb_migrator','public','USAGE')` true and `'CREATE'` false, zero `public` relations readable by `rwb_migrator`, one `pg_auth_members` row `ace_view_owner`/`rwb_migrator` with `inherit_option = false`, `set_option = true`, `admin_option = false`, and `rolsuper`, `rolcreaterole`, `rolcreatedb`, `rolbypassrls` false. The X5 fixture `GRANT INSERT ON ${recoverySchema}.v_ace_account TO recovery_svc` fails check 4 naming the privilege, and X8 is proven because a new view receives the default DML grant from `20-grants.sql.inc` and the per-view REVOKE removes it before the owner change.
- **Covers** AC2.4, X5, X8, X12. **Test** `ViewConformanceTest.check4` and `.check5`. **Tasks** TASK-08, TASK-09. **Level** recovery-it.

### S-06 AC2 `ace_view_owner` rights (TC-E1-069-02)

- **Given** S-01's container.
- **When** the test reads ownership and privileges of the 16 views and of the 21 Tier 1 tables.
- **Then** `ace_view_owner` owns exactly the 16 views; holds SELECT on each of the 21 tables and no INSERT, UPDATE or DELETE on any; holds no USAGE or CREATE on `recovery`, no EXECUTE on the three helpers, and no privilege on any other `recovery` relation.
- **Covers** AC2.5, BR2. **Test** `ViewConformanceTest.aceViewOwnerRights`. **Tasks** TASK-08, TASK-09, TASK-15. **Level** recovery-it.

### S-07 AC2 `rwb_no_grant` cannot read (TC-E1-069-02)

- **Given** S-01's container and a fixture role `rwb_no_grant` with LOGIN and USAGE on `recovery` only.
- **When** it selects `recovery.v_ace_account`.
- **Then** the statement fails with SQLSTATE 42501 (`permission denied for view v_ace_account`) and `has_table_privilege` is false.
- **Covers** AC2.6. **Test** `ViewConformanceTest.noGrantRole`. **Task** TASK-08. **Level** recovery-it.

### S-08 AC3 Section B and 30 views (TC-E1-069-03)

- **Given** a fresh container with the probe applied and the Section A file applied.
- **When** the Section B file is applied.
- **Then** 14 Section B views exist and 14 of 14 compile; `recovery` holds 30 `v_ace_*` views (16 + 14) and 30 of 30 return a row as `recovery_svc`; the history holds one success row for Section B after the Section A row.
- **Covers** AC3.1, AC3.2, AC3.3, BR1. **Test** `ViewConformanceTest.check1`, `.historyAfterSectionB`. **Tasks** TASK-08, TASK-10, TASK-11. **Level** recovery-it.

### S-09 AC3 X2 main: no `public.valuation` (TC-E1-069-03, T-E1-069-16)

- **Given** a fresh Flyway-mode container with the probe applied and its grants; `DROP TABLE public.valuation` as superuser.
- **When** Flyway migrates to the Section A version and then fully.
- **Then** a `FlywayException` is raised whose cause has SQLSTATE `42P01` and whose message contains `public.valuation` and `does not exist`; 16 `v_ace_*` views exist and none of the 14 Section B names; no `success = true` row exists for the Section B file; the 16 Section A views still return rows as `recovery_svc`.
- **Covers** AC3.4, BR9, X2. **Test** `ViewConformanceTest.x2MissingTier2Table`. **Tasks** TASK-10, TASK-11. **Level** recovery-it.

### S-10 AC3 X2 probe-off (T-E1-069-13)

- **Given** the same container with `RWB_ACE_TIER2_PROBE=false`.
- **When** the same two migrations run.
- **Then** the first failure names `relation "public.ace_batch_run" does not exist`, with the same end-state assertions as S-09.
- **Covers** AC3.4, X2. **Test** `ViewConformanceTest.x2ProbeOff`. **Tasks** TASK-10, TASK-11. **Level** recovery-it.

### S-11 AC4 no constraint references `public` (TC-E1-069-04)

- **Given** S-01's container.
- **When** check 2 lists every `pg_constraint` row in `recovery` and the type of every constrained column.
- **Then** zero rows have `confrelid` outside `recovery` and no constrained column type lives outside `recovery` or `pg_catalog`. The X3 fixture adds `fk_case_account_account_key` to `public.account` after the migration and check 2 fails with `fk_case_account_account_key references public.account; no constraint in recovery may reference another schema`.
- **Covers** AC4.1, AC4.2, BR4, X3. **Test** `ViewConformanceTest.check2` and `.check2FailingFixture`. **Task** TASK-08, TASK-09. **Level** recovery-it.

### S-12 AC5 dictionary (TC-E1-069-05)

- **Given** the full migration on the probe container.
- **When** `v_data_dictionary` is counted by source system and per view, and check 3 runs.
- **Then** 123 objects and 1,382 fields; 1,078 table fields of which 49 on the four extension tables; the 30 `v_ace_*` objects hold 304 fields, 177 Section A and 127 Section B; each view has one `sys_objects` row and one `sys_fields` row per catalog column and every such row has a non-null `is_personal`. The X4 fixture adds `legacy_bucket` to a copy of `v_ace_account` with no `sys_fields` row and check 3 fails with `v_ace_account.legacy_bucket has no data dictionary entry`.
- **Covers** AC5.1, AC5.2, AC5.3, AC5.4, AC5.5, BR5, X4, NFR-040 (only the 304 frozen fields). **Test** `ViewConformanceTest.dictionaryTotals`, `.check3` and `.check3FailingFixture`. **Tasks** TASK-08, TASK-09. **Level** recovery-it. **Note** the whole-dictionary 526 `is_personal` count is RWB-E1-001's assertion, not this story's (PA-E1-069-12).

### S-13 AC6 the dictionary returns `days_past_due` (TC-E1-069-06)

- **Given** S-01's container with `ACC0000017` (`delay_days` 95).
- **When** `v_data_dictionary` is queried for entity `v_ace_account`, field `days_past_due`, and the view is read for the account.
- **Then** the row holds `DF-ACE-018`, `NUMBER`, `integer`, `ACE`, `public.account.delay_days`, `DP01` and `DAILY`; the view returns 95.
- **Covers** AC6. **Test** `ViewConformanceTest.dictionaryRowForDaysPastDue`. **Tasks** TASK-08, TASK-09. **Level** recovery-it.

### S-14 AC7 extension tables (TC-E1-069-07)

- **Given** S-01's container.
- **When** the four tables' columns, keys and constraints are read and a second `party_ext` row for `P0000123` is inserted.
- **Then** `party_ext` 12 columns with `person_key` PK; `contact_point_ext` 14 with `contact_key` PK and `ck_contact_point_ext_type` allowing PHONE, EMAIL, ADDRESS; `account_ext` 9 with `account_key` PK; `valuation_ext` 14 with `valuation_key` PK; 49 columns in all and 49 `sys_fields` rows DF-EXT-001..049; no FK to `public`; no business column copies a column of the view it extends; the second insert fails with 23505 on `party_ext_pkey` and one row remains.
- **Covers** AC1.1, AC7.1, AC7.2, AC7.3, BR4, BR7, X7. **Test** `ViewConformanceTest.extensionTables`. **Tasks** TASK-08, TASK-09. **Level** recovery-it.

### S-15 AC8 BND-6 (TC-E1-069-08)

- **Given** the eight test-scope fixtures in `th.co.scb.ace.demo.recovery.dataengine.internal` and the real recovery main sources.
- **When** `Bnd6RuleTest` and `RecoveryBoundaryTest.noRecoveryClassNamesAPublicTable` run in the `test` task.
- **Then** `AccountReader` fails with `Boundary rule BND-6 broken: AccountReader reads public.account. Read recovery.v_ace_account instead.`; `AccountReaderOnView` passes; `NativeQueryReader`, `UnqualifiedReader`, `QuotedReader` and `PublicAccountEntity` each fail; `JpqlPaymentReader` and `CatalogFilterReader` pass; the real main sources produce no offender, so `PlatformInfoController` stays green.
- **Covers** AC8.1, AC8.2, AC8.3, BR1, BR8, X6. **Test** `Bnd6RuleTest` and `RecoveryBoundaryTest.noRecoveryClassNamesAPublicTable`. **Tasks** TASK-12, TASK-13. **Level** unit.

### S-16 BR6 helper functions (T-E1-069-09, T-E1-069-10)

- **Given** S-01's container.
- **When** the SPEC-002 table is called literally; six synthetic `public.payment` rows are read through `v_ace_payment`; `DateStyle` is set to `SQL, DMY` and `German`; `ace_to_boolean` and `ace_mask_value` are called; `has_function_privilege` is asked of `recovery_svc`, `ace_view_owner` and `rwb_no_grant`.
- **Then** every shape gives the exact date or NULL and no call raises (`2026-02-30`, `20261345`, `31/02/2026`, `0000-01-01`, `00000000` give NULL); the view returns 2026-02-28 for the first row and NULL for the other five; the two date styles do not change the result; `Y`, `' y '`, `yes`, `TRUE`, `1` give true, `N`, `no`, `False`, `0` false, `''`, NULL, `maybe`, `2` NULL; `0000005678` gives `******5678`, `abc` gives `***`, `a@x.co` gives `a***@x.co`, `''` and NULL give NULL; EXECUTE is true for `recovery_svc` and false for `ace_view_owner` and `rwb_no_grant` on all three; X9 is proven because a dirty text date returns NULL and the read succeeds.
- **Covers** BR6, X9. **Test** `ViewConformanceTest.helperFunctions` and `.helperFunctionsThroughTheView`. **Tasks** TASK-08, TASK-09. **Level** recovery-it.

### S-17 BR2 end state after Section B (T-E1-069-14)

- **Given** the full migration.
- **When** ownership and privileges are read again.
- **Then** `ace_view_owner` owns exactly 30 views, holds no USAGE or CREATE on `recovery` and no EXECUTE on the helpers; `recovery_svc` still reads all 30; PUBLIC holds nothing.
- **Covers** AC3.2, BR2. **Test** `ViewConformanceTest.endStateAfterSectionB`. **Tasks** TASK-08, TASK-09, TASK-11. **Level** recovery-it.

### S-18 Data protection of the published interface (T-E1-069-15)

- **Given** S-01's container and the synthetic identification value `X000000005678`.
- **When** `reloptions`, the column list of `v_ace_customer`, the masked read and the `is_personal` counts are checked.
- **Then** no `v_ace_*` view has `security_invoker=true`; `v_ace_customer` has no `identification_number` and no `id_no` column; the view returns `id_no_masked` `*********5678` and `id_no_last4` `5678`; of the 304 DF-ACE fields 304 are non-null, 250 are true (including all 12 Restricted) and 54 false; all fixture values are synthetic.
- **Covers** SPEC-019, NFR-039 (partial), NFR-045, NFR-054. **Test** `ViewConformanceTest.dataProtectionChecks`. **Tasks** TASK-08, TASK-09. **Level** recovery-it.

### S-19 Flyway-mode `RecoveryDatabaseIT`, the E1-001 pin and check 5 (T-E1-069-16)

- **Given** a fresh container built by `10-load-ace-database.sh` with S1 `false`, S2 `false` and the probe on.
- **When** the application context starts and `RecoveryDatabaseIT` runs; `RecoverySchemaMigrationIT` runs through `RecoveryFlywayTestSupport` with `target` at the RWB-E1-001 version; check 5 runs in the superuser session.
- **Then** `recovery_svc` sees 30 `v_ace_*` views created by Flyway, 0 visible `public` tables, 42501 on `public.account`, read-only views owned by `ace_view_owner`, the append-only decision log and the identity separation; the history holds one success row per applied file and no `version = '0'` row; `RecoverySchemaMigrationIT` still sees no `v_ace_*` view and no `ace_to_date` at the RWB-E1-001 version; check 5 passes. X12 is proven because a migration account holding a table privilege or an inheriting membership fails check 5 and T-044-17.
- **Covers** AC1.5, AC3.3, BR2, X12. **Test** `RecoveryDatabaseIT`, `RecoverySchemaMigrationIT`, `ViewConformanceTest.check5`. **Tasks** TASK-07, TASK-14, TASK-15. **Level** recovery-it.

### S-20 Connection-input switch (T-E1-069-17)

- **Given** a stub map with and without `RWB_CONFORMANCE_TARGET=external`.
- **When** `ConformanceTarget.from(map)` is called.
- **Then** absence gives Testcontainers mode; `external` gives external mode with the five variables; a missing or blank variable fails with an `IllegalStateException` naming it and no value; the passwords never appear in the message; `EXTERNAL` is not accepted.
- **Covers** SPEC-008 (ASM-004). **Test** `ConformanceTargetTest`. **Tasks** TASK-01, TASK-02. **Level** unit.

### S-21 Lint seams (T-E1-069-11)

- **Given** the five fixture folders and the merged lint.
- **When** `MigrationSeamRulesTest`, `LintExceptionsLoaderTest` and `RecoveryMigrationLintTest` run.
- **Then** SEAM-E044-01: the `CREATE OR REPLACE VIEW ${recoverySchema}.v_ace_*` statement passes, and `SELECT ... FROM public.t`, `GRANT SELECT ON public.t`, `CREATE VIEW ${recoverySchema}.v_other ... FROM public.t` and `REFERENCES public.t(id)` each give one finding. SEAM-E044-02: the two named `rwb_e1_069` files with recovery-side grants pass; a grant in another key, a third `rwb_e1_069` file, a wrong suffix, `GRANT ... TO rwb_migrator`, a grant on `public`, `GRANT ... ON ALL TABLES` and any other grantee fail; `L-KEY-DUP` names both allowed files. The loader reads the real resource and fails on an unknown key with the file and field path.
- **Covers** §4 step 2, SPEC-014, X11. **Test** `MigrationSeamRulesTest`, `LintExceptionsLoaderTest`, `RecoveryMigrationLintTest`. **Tasks** TASK-03, TASK-04. **Level** unit.

### S-22 `sourceViews` and the migration-folder rules (T-E1-069-12)

- **Given** the real map, the real migration folder and fixture folders.
- **When** `SourceViewsReaderTest` and `MigrationFolderCoverageTest` run.
- **Then** the real key parses to 16 + 14 unique names in story order; missing lists, bad names, duplicates and wrong counts fail with the file and field path; rule 1 holds (every created `v_ace_*` view is listed); rule 2 holds (Section A set equals `sectionA`); rule 3 holds in both states (Section B set equals `sectionB` when the file is present; otherwise no file creates a Section B name); rule 4 holds (BND-6 allows all 30 names).
- **Covers** AC1.4, AC8.3, BR8. **Test** `SourceViewsReaderTest`, `MigrationFolderCoverageTest`. **Tasks** TASK-05, TASK-06, TASK-07. **Level** unit.

### S-23 Local mode switch (SPEC-015)

- **Given** the merged branch.
- **When** the init script, the grants file, `.env.example`, `docker-compose.yml`, `README.md` and the migration-folder `README.md` are read and the fresh container of S-19 is built.
- **Then** no `RWB_LOAD_REFERENCE_VIEWS` branch exists in `10-load-ace-database.sh`; both variables read `false`; the Flyway-mode grants are the named 21 (and 14 probe) tables; the function default privilege names `recovery_svc` only; the D-RUN-14 lines are unchanged; the READMEs name RWB-E1-069 as the owner of the view files and carry no fixed number and the reset note; the schema is empty at init and Flyway writes no version-`0` row. X10 is the P4(d) precondition: if the ACE-side SELECT is missing the views compile but reads fail (`permission denied for table <t>`), which is the environment check EX-02.
- **Covers** SPEC-015(a), -015(b), BR9, X10, NFR-027 (forward only). **Test** script and document review plus S-19. **Tasks** TASK-14, TASK-15, TASK-17. **Level** build and review.

### S-24 Unit gate and coverage (T-E1-069-18)

- **Given** the full change.
- **When** `./gradlew test recoveryCoverageVerification` runs.
- **Then** the one bundle reaches LINE, INSTRUCTION, BRANCH and METHOD at or above 0.80, each new or changed tooling class in `architecture/boundary/**` and `architecture/migration/**` reaches 80% on all four counters, and `RecoveryFlywayTestSupport` is not claimed.
- **Covers** SPEC-020 (unit row). **Task** TASK-16. **Level** build.

## Not executed here

| ID | Check | Owner | Why not executed |
|---|---|---|---|
| EX-01 | The external `ViewConformanceTest` run against DEV and SIT (`RWB_CONFORMANCE_TARGET=external` plus the five variables) as the AC1/AC2 environment evidence | Pipeline owner with the recovery tech lead | No target database in this repository; never reported as a local test (ASM-004, OI-069-L(b)) |
| EX-02 | The ACE DBA applies P4(c)-(d): `rwb_migrator`'s schema ownership or CREATE right, `ace_view_owner`'s USAGE on `public` and SELECT on the 21 Tier 1 (and 14 Tier 2) tables, and the PUBLIC revoke | ACE DBA / environment owner | Environment action outside the repository (OI-069-A); locally supplied by `20-grants.sql.inc` and proven by S-05 and S-06 |
| EX-03 | RWB-ACE-001 is deployed in every environment `main` deploys to before Section B merges | ACE team lead | External dependency (DL43, DG-L16, OI-069-D); the probe is local evidence only |
| EX-04 | Ratification of D-RUN-14 | Recovery tech lead | Orchestrator decision applied as recorded; OI-069-M / OPEN-051 open; no human approval claimed |
| EX-05 | Display masking at the API and the PII access log | RWB-E1-037 and RWB-E1-016 | Out of scope for this story |

## Coverage matrices

### AC clause to scenario

| Clause | Scenario |
|---|---|
| AC1.1 | S-14 |
| AC1.2, AC1.3, AC1.4 | S-01 (AC1.4 also S-22) |
| AC1.5, AC1.6 | S-02 |
| AC2.1, AC2.2, AC2.3 | S-04 |
| AC2.4 | S-05 |
| AC2.5 | S-06 |
| AC2.6 | S-07 |
| AC3.1, AC3.2, AC3.3 | S-08 (AC3.3 also S-19) |
| AC3.4 | S-09, S-10 |
| AC3.5 | S-09 (the consuming stories own the flags) |
| AC4.1, AC4.2 | S-11 |
| AC5.1, AC5.2, AC5.3, AC5.4, AC5.5 | S-12 |
| AC6 | S-13 |
| AC7.1, AC7.2, AC7.3 | S-14 |
| AC8.1, AC8.2, AC8.3 | S-15 (AC8.3 also S-22) |

### Business rule to scenario

| BR | Scenario |
|---|---|
| BR1 | S-01, S-08, S-15 |
| BR2 | S-06, S-17 |
| BR3 | S-04, S-05 |
| BR4 | S-11, S-14 |
| BR5 | S-12 |
| BR6 | S-16 |
| BR7 | S-14 |
| BR8 | S-15, S-22 |
| BR9 | S-09, S-23 |

### Test case to scenario

| Test case | Scenario | Level |
|---|---|---|
| TC-E1-069-01 | S-01, S-02, S-17 | recovery-it |
| TC-E1-069-02 | S-04, S-05, S-06, S-07 | recovery-it |
| TC-E1-069-03 | S-08, S-09, S-10 | recovery-it |
| TC-E1-069-04 | S-11 | recovery-it |
| TC-E1-069-05 | S-12 | recovery-it |
| TC-E1-069-06 | S-13, S-16 | recovery-it |
| TC-E1-069-07 | S-14 | recovery-it |
| TC-E1-069-08 | S-15 | unit |
| T-E1-069-09 | S-16 | recovery-it |
| T-E1-069-10 | S-16 | recovery-it |
| T-E1-069-11 | S-21 | unit |
| T-E1-069-12 | S-22 | unit |
| T-E1-069-13 | S-10 | recovery-it |
| T-E1-069-14 | S-17 | recovery-it |
| T-E1-069-15 | S-18 | recovery-it |
| T-E1-069-16 | S-19 | recovery-it |
| T-E1-069-17 | S-20 | unit |
| T-E1-069-18 | S-24 | build |

### Exceptional case to scenario

| X | Scenario |
|---|---|
| X1 | S-03 |
| X2 | S-09, S-10 |
| X3 | S-11 |
| X4 | S-12 |
| X5 | S-05 |
| X6 | S-15 |
| X7 | S-14 |
| X8 | S-05 |
| X9 | S-16 |
| X10 | S-23, EX-02 |
| X11 | S-21 |
| X12 | S-19 |

### NFR to scenario

| NFR | Coverage |
|---|---|
| NFR-045 synthetic data in DEV | S-13, S-14, S-18 |
| NFR-054 the pipeline blocks personal data in code and tests | S-18 (no personal data in any fixture, migration or log line) |
| NFR-039 party identifiers masked | S-18 partial; display masking RWB-E1-037 |
| NFR-040 data minimisation | S-12 (only the 304 frozen fields) |
| NFR-042 every read of a personal field logged | Not covered: RWB-E1-016 (out of scope) |
| NFR-027 roll back by redeploying the previous tag | S-23; forward-only migrations, a fault is fixed by a corrective file |

### Clarification log

`CLARIFICATION_STATUS: NOT_REQUIRED` (spec `## Clarification Log`). No `CLAR-*` row exists, so no scenario maps to one. The rulings that need owner confirmation are spec assumptions with proposed open items (OI-069-A..M), not clarifications.
