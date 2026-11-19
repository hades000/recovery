---
title: "Implementation Plan: RWB-E1-069 Read-only ACE source views, grants and boundary rule"
run_id: "INC-010-epic-1-RWB-E1-069"
story: "RWB-E1-069"
epic: "EPIC-001"
status: "SUCCESS"
revision: "v1 (18 Nov 2026): first plan stage for this run. Written against spec revision 4 (spec gate round 4, PASS 0 Critical / 0 High / 0 Medium / 0 Low, `../review/spec-gate-review-4.md`) and the gated plans of the earlier stories (RWB-TE-001 plan v7 merged; RWB-E1-044 plan v2 PASS; RWB-E1-001 spec Revision 4, plan not yet present)."
prepared: "2026-11-18"
---

# Implementation Plan: RWB-E1-069 Read-only ACE source views, grants and boundary rule

Design Source: `NOT_REQUIRED` (UI In Scope: NO; `DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0]` in `../specify/spec.md`).

| Field | Value |
|---|---|
| Spec | `../specify/spec.md` revision 4. Spec gate round 4: `PASS` 0 Critical / 0 High / 0 Medium / 0 Low (`../review/spec-gate-review-4.md`). `Status: SUCCESS`; `REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 42] [MISSING_RULES: 0] [CONTRADICTIONS: 0]`. |
| Story | Story RWB-E1-069 v1, Epic 1 Story Files v7, 15 Nov 2026 (`rwb-e1-069-read-only-ace-source-views-grants-and-boundary-rule-v1.md`), sections 1-19 read. |
| Base layout (D-RUN-17) | RWB-TE-001 plan v7 (merged in this worktree on 18 Nov 2026: module skeleton, relocation, `architecture.boundary` tooling, coverage includes) and RWB-E1-044 plan v2 (PASS: the migration lint registry, `isAllowedQualifier`, the D-RUN-14 local init). RWB-E1-001 spec Revision 4 (its migration, extension tables, dictionary seed, `RecoverySchemaMigrationIT`). |
| Code baseline | Read on 18 Nov 2026: `backend/src/test/java/th/co/scb/ace/demo/recovery/architecture/RecoveryBoundaryTest.java` (BND-6 is still the line scanner at line 196), `backend/src/test/java/th/co/scb/ace/demo/recovery/architecture/RecoveryMigrationLintTest.java` (pre-E1-044 baseline), `backend/src/test/java/th/co/scb/ace/demo/recovery/RecoveryDatabaseIT.java` (S1 stands at `true`), `backend/src/test/resources/architecture/recovery-modules.yaml` (no `sourceViews`), `backend/build.gradle.kts` lines 130-160 (JaCoCo bundle and `test`-task execution data), `infra/postgres/init/10-load-ace-database.sh`, `infra/postgres/init/20-grants.sql.inc`, `.env.example`, `docker-compose.yml`, `backend/src/main/resources/application.yaml`, the migration-folder `README.md`. No git command and no build was run; no file outside `plan/` was written. |
| Builder | Implementation Builder in its own git worktree from `develop-recovery` **after** RWB-E1-044 and RWB-E1-001 merge (build order 1 and 9; E1-069 is order 10). Commits `RWB-E1-069: <summary>` with the `AISDLC-Run` and `AISDLC-Plan` trailers. |
| Smallest change | Two production migrations (no main Java class), one conformance test class, one conformance-target reader, one `sourceViews` reader and three BND-6 tooling classes, two lint seam changes in RWB-E1-044's tooling, one lint exception resource, the `sourceViews` key, one Flyway test-support factory, the `RecoveryDatabaseIT` rewrite, one inherited IT pin, local init and documentation. No new dependency, endpoint, screen, pipeline or build-file change. |
| Migrations | **2.** `V<seq>__rwb_e1_069_ace_source_views.sql` (Section A) and `V<seq>__rwb_e1_069_ace_tier2_views.sql` (Section B). Line 1 of each is `-- Story: RWB-E1-069`. `<seq>` is assigned at merge (D-RUN-07, D-RCV-28); no number is fixed here; the two are contiguous, A then B. |

## Upstream readiness

| Check | Result |
|---|---|
| Spec status | `SUCCESS` (spec front matter and `## Status`) |
| Spec gate | `PASS` round 4, no finding (`../review/spec-gate-review-4.md` §6) |
| `REQUIREMENT_COVERAGE_RESULT` | `MISSING_RULES: 0`, `CONTRADICTIONS: 0` (42 rules; 30 document gaps DG-L01..L30, all Blocker = No) |
| Clarification log | `CLARIFICATION_STATUS: NOT_REQUIRED` with evidence (spec `## Clarification Log`); no `CLAR-*` row exists |
| Design evidence | `NOT_REQUIRED` (UI In Scope NO): no screen task, no `frontend/components.md`, no screenshot check |
| Production migrations | 2, both with the `V<seq>` placeholder; D-RUN-07 applied; no number written in this plan or the tests |
| Dependency revisions | RWB-E1-044 v14-7 (review-7 PASS), RWB-E1-001 Revision 4 (review-4 PASS), RWB-TE-001 v4 (review-5 PASS) |

`PLANNER_CLARIFICATION_STATUS: READY [OPEN_ITEMS: 0] [UNBLOCK_ACTION: n/a]`. The spec's open items (OI-069-A..M, OPEN-035, OPEN-032) are shared open-item proposals answered by other owners; none is a `CLAR-*` item and none blocks this plan.

## Change scope and surfaces

| Field | Value | Evidence |
|---|---|---|
| Change type | `NEW_STORY` | Spec Change Scope Declaration; no `v_ace_*` view, conformance test or `sourceViews` exists in the code |
| Backend | **CHANGED** — unit tests `REQUIRED` | Two migrations, test-scope tooling, fixtures, local init, docs |
| Frontend | **NOT_APPLICABLE** — no unit-test task | UI In Scope NO; story §15; no file under `frontend/` changes; `contracts/frontend-integrations.json` records the N/A |
| API | `NO_API_CHANGE` — no API task | Story §12 "No endpoint and no event"; `GET /api/recovery/v1/platform/info` unchanged |
| UI | NO | `DESIGN_EVIDENCE_STATUS: NOT_REQUIRED`; no `SCR-*` screen in scope |
| Migrations | **2** — `V<seq>__rwb_e1_069_ace_source_views.sql` (A, first) and `V<seq>__rwb_e1_069_ace_tier2_views.sql` (B, after RWB-ACE-001) | D-RUN-07; no fixed number |
| Shared build files edited | **None** — `backend/build.gradle.kts` is not touched | RWB-TE-001 and RWB-E1-044 already added their tooling directories to the JaCoCo bundle |
| New dependency | None | The plan uses the existing ArchUnit 1.5.1, SnakeYAML 2.6, Flyway 12.4.0, Testcontainers PostgreSQL, JUnit 5 and AssertJ |

## Dependencies and merge order (D-RUN-08)

| Order | Story | What this plan uses | State at plan time |
|---|---|---|---|
| 1 | RWB-E1-044 | Migration lint registry, `LiteralSchemaRule.isAllowedQualifier` (SEAM-E044-01), `L-GRANT`/`L-KEY-DUP` (SEAM-E044-02), the D-RUN-14 rights in `infra/postgres/init/20-grants.sql.inc` | Spec v14-7 PASS; plan v2 PASS; **not merged** in this worktree. TASK-00 stops if absent. |
| 2 | RWB-TE-001 | `architecture.boundary` package (`ModuleMap`, `ModuleMapLoader`, `BoundaryRules`), the real module map, the coverage includes | **Merged** in this worktree on 18 Nov 2026 |
| 9 | RWB-E1-001 | The RWB-E1-001 migration (tables, four extension tables, dictionary seed), S1 and S3, the S2 stage this story takes over, `RecoverySchemaMigrationIT` | Spec Revision 4 PASS; plan not present at plan time; **not merged**. TASK-00 stops if absent. |
| external | RWB-ACE-001 | The 14 Tier 2 tables, 12 `account`/`customer`/`efs_action` columns, SELECT for `ace_view_owner`, PUBLIC revoke | Not deployed. The local Tier 2 probe (`infra/postgres/schema/02-ace-tier2-probe.sql`) is the recorded stand-in (ASM-005, DG-L16, Blocker = No). |

Later-story work is named as a seam and not built: display masking (RWB-E1-037), the PII access log (RWB-E1-016), CI wiring of `recoveryCoverageVerification` (RWB-TE-003/TE-011), Section B feature flags (the consuming stories). D-RUN-12 holds: this story creates no table; the four extension tables and the 92 PS v6 tables belong to the RWB-E1-001 migration, and the two view files create views, helpers and grants only.

## Scope

Each bullet maps to tasks in `tasks.md` ("Scope bullet to task map").

1. **S-1 Section A migration** — the schema-wide PUBLIC revoke, the three helper functions, the 16 Section A views, the Section A grant block, in that order (SPEC-001..004). → TASK-09
2. **S-2 Section B migration** — the 14 Section B views and their grant block, merged only after RWB-ACE-001 is deployed (SPEC-005, -006; DG-L20). → TASK-11
3. **S-3 Conformance evidence** — `ViewConformanceTest`: checks 1-5, fixtures, dictionary totals, extension-table shape, AC6 row, helper functions, data protection, history and re-run, the BR2 end state, external mode (SPEC-008..011, -017, -019, -020). → TASK-07, -08, -10
4. **S-4 BND-6** — the hardened detector, the derived table-to-view map, the fixtures, and `RecoveryBoundaryTest` on the real sources (SPEC-012). → TASK-12, -13
5. **S-5 `sourceViews`** — the 30 names in the module map, the validating reader, the migration-folder rules that hold in both states (SPEC-013). → TASK-05, -06, -07
6. **S-6 Lint seams** — SEAM-E044-01 (`public.` only inside the view statement) and SEAM-E044-02 (`L-GRANT`, `L-KEY-DUP` for key `rwb_e1_069`), with the exception data in one test resource (SPEC-014). → TASK-03, -04
7. **S-7 Local mode switch** — S2 `RWB_LOAD_REFERENCE_VIEWS` default `false`, the init branch deleted, Flyway-mode grants, the README corrections (SPEC-015). → TASK-14, -15, -17
8. **S-8 Flyway-mode tests** — `RecoveryDatabaseIT` moved to S1 `false`, S2 `false`; `RecoverySchemaMigrationIT` pinned to the RWB-E1-001 version (SPEC-015(c)). → TASK-07, -14
9. **S-9 X2 negative test** — the Section B failure without `public.valuation`, the probe-off case, the unchanged Section A state (SPEC-018). → TASK-10, -11
10. **S-10 Data protection of the published interface** — classification of record, masked identity, `is_personal` counts, the definer-rights note (SPEC-019). → TASK-08, -16
11. **S-11 No API, UI or main-code change** — `PlatformInfoController` and `platform.ts` unchanged and green under BND-6 (SPEC-016). → TASK-13, -18
12. **S-12 Gates and evidence** — the 80% four-counter unit gate, the container suite, the e2e regression, the scope check (SPEC-020 and the unit-test row). → TASK-16, -18, -19

Out of scope (spec `## Out of scope`): masking at the API and display masking (RWB-E1-037); the PII access log (RWB-E1-016); the rest of the module map and BND-1..5 (RWB-TE-001); the Tier 2 tables, the 12 ACE columns and the ACE-side grants (RWB-ACE-001 and the ACE DBA); the feature flags of Section B consumers; any change to the frozen 30-view list or a view body beyond the `ace_to_date` body already ruled by SPEC-002 (OI-069-G); DML grants for `recovery_svc` on Workbench tables in SIT and above (DG-L25, OI-069-I); CI wiring of the coverage verification (RWB-TE-003/TE-011); the `is_personal` ruling for the 26 PS-v6-only fields and DF-REF-300..302 (RWB-E1-001's Blocker = Yes gaps).

## One-module check (D-RUN-21)

`AGENTS.md` §7 and §9 ask that a plan "touches one module". Build decision D-RUN-21 (`AI-SDLC-BUILD-LOG.md` decisions table, 18 Nov 2026 05:36, the orchestrator (Claude Code); ratification tracked as OPEN-050, owner the recovery tech lead) settles the reading: **"touches one module" means the ACE module, the recovery module.** This plan applies that reading; it does not re-open it and claims no human ruling.

| Check | Result |
|---|---|
| ACE module touched | `recovery` only. The two migrations write `${recoverySchema}` objects; every test class is under `th.co.scb.ace.demo.recovery` or a fixture package under `th.co.scb.ace.demo`; no main class changes. |
| Nested design modules touched | None in main sources (no Java change). Test scope: `architecture.boundary` (RWB-TE-001's tooling), `architecture.migration` (RWB-E1-044's tooling), `casewf.migration` (test-support only), `dataengine.internal` (AC8 fixtures only). |
| Other ACE modules | None. No `common`, `collection`, `platform`, `rules`, `workflow` or `documents` package is created, read or changed. |
| Non-Java files touched | `backend/src/test/resources/**` (test data), `infra/postgres/init/**` (local infrastructure, not an ACE application module), `.env.example`, `docker-compose.yml`, `README.md`, the migration-folder `README.md`. `backend/build.gradle.kts` is **not** touched (SPEC-020 relies on RWB-TE-001's and RWB-E1-044's includes). |
| Verdict | **PASS — one module (recovery).** No return to the analyst is required on the one-module rule. |

## Carried plan inputs from the earlier stories

| Input | Source | Applied in |
|---|---|---|
| P-1 Test-first red/green with the red command, exit code and first failing assertion saved under `implement/` | RWB-TE-001 plan v7 `tasks.md`; `testing-standards` §5 | Every task in `tasks.md` |
| P-2 Compile-red tasks run directly before their green task, so no other task runs on an uncompiling test source set | RWB-TE-001 plan v7 PLAN-015 | TASK-01/02, TASK-03/04, TASK-05/06, TASK-12/13 |
| P-3 JaCoCo `recoveryCoverageVerification` stays one bundle: all recovery main classes plus RWB-TE-001's `architecture/boundary/**` plus RWB-E1-044's `architecture/migration/**`; execution data from `test` only; not added to `check` | RWB-TE-001 plan v7 TASK-01, "Coverage gate edit"; RWB-E1-044 plan v2 TASK-13; `backend/build.gradle.kts` lines 130-160 | TASK-16 |
| P-4 Binding tests isolated from the process environment through `testsupport.ApplicationYamlEnvironment.isolated()` | RWB-TE-001 plan v7 PLAN-012 | Not needed (no new Spring binding); recorded so the Builder does not import `.env` into the conformance target |
| P-5 Lint tooling: one tokenizer, three views, one ordered registry; `isAllowedQualifier(statement, qualifier)` is the single qualifier extension point; finding text `MSG-P3-016 schema=recovery object=<file>:<line> rule=<RULE-ID> <detail>`; one finding per (rule, file, line, key) | RWB-E1-044 plan v2 "Tooling design" | TASK-03, TASK-04 |
| P-6 Flyway bean: `@Bean(initMethod = "migrate")`; the test clears the init method on the bean definition and reuses `flyway.getConfiguration()` with `target`; settings are never copied | RWB-E1-044 plan v2 "Flyway bean changes"; spec SPEC-018 | TASK-07, TASK-10, TASK-14 |
| P-7 S1 and S3 belong to RWB-E1-001; E1-069 takes S2 only and asserts what the E1-001 file seeds (1,382 `sys_fields`, 1,078 table fields, 526 `is_personal` true in the whole dictionary; 250 true and 54 false among the 304 DF-ACE fields) | Spec SPEC-015(a), SPEC-010, SPEC-019; ASM-017; DG-L27, DG-L30 | TASK-08, TASK-14, TASK-15 |
| P-8 Container: `postgres:16.16-alpine`, `@Tag("recovery-it")`, init copied from `infra/postgres`, synthetic passwords, fails (not skips) without Docker | `RecoveryDatabaseIT` as it stands; C3; DG-L14 | TASK-08, TASK-10, TASK-14, TASK-18 |
| P-9 D-RUN-14 rights are RWB-E1-044 v14-7's local init; E1-069 restates neither and weakens neither; who applies them in SIT/UAT/PROD stays OI-E044-I; OI-069-A carries P4(c)-(d) only | Spec P4, SPEC-014, ASM-016; E1-044 v14-7 SPEC-017, OI-E044-I | TASK-04, TASK-08, TASK-19 |

## Plan-time verification (read only)

| Item | Source or command | Result (18 Nov 2026) |
|---|---|---|
| Base state | file listing of `backend/src/main/java/th/co/scb/ace/demo/recovery/**` and `backend/src/test/**` | RWB-TE-001's merge is present (`casewf/migration/RecoveryFlywayConfig.java`, `architecture/boundary/ModuleMapLoader.java`, 61 `package-info.java`); RWB-E1-044's `architecture/migration` and `RecoveryMigrationRunner` are absent; the migration folder holds only `README.md` |
| BND-6 baseline | `RecoveryBoundaryTest.java` line 196 | Line-by-line scanner; skips lines starting `*` or `//`; no JPA, annotation or unqualified-FROM detection. TASK-13 replaces the method body, not the rule |
| `sourceViews` baseline | `ModuleMap.java` line 10-11, `ModuleMapLoader.java` line 65, `recovery-modules.yaml` | The loader carries `sourceViews` as an opaque `Object`; the real map has no key. TASK-06 adds the key and the reader; the loader is unchanged |
| Lint baseline | `RecoveryMigrationLintTest.java`; E1-044 v14-7 SPEC-016 | Old inline scanner in the worktree; the merged lint will be the registry. TASK-04 applies the seams at the shipped extension point; the fixtures and rules do not change if the class names differ (ASM-011) |
| Coverage wiring | `backend/build.gradle.kts` lines 130-160 | `recoveryClasses` is main output only; both JaCoCo tasks take `executionData(test)`; TE-001's include of `architecture/boundary/**` is the merged form. E1-069 adds no build edit |
| View bodies | `recovery-workbench-ace-source-views-v1.sql` lines 94-711 | 30 views; Section A 16 views / 177 columns, Section B 14 views / 127 columns; the aliases were counted per view and match the DF-ACE ranges of story §11 (account 001-042, payment 043-054, customer 055-074, contact 075-083, ca_relation 084-088, aa_relation 089-090, collateral 091-098, asset 099-107, efs_action 108-127, efs_action_code 128-130, efs_assignment 131-139, bucket_log 140-145, product 146-150, branch 151-154, holiday 155-159, plan 160-177; batch_status 178-186, valuation 187-195, collateral_detail 196-207, npa_asset 208-219, npa_sale 220-230, lawsuit 231-243, hearing 244-250, pod 251-260, write_off 261-269, score 270-279, party_product 280-285, credit_decision 286-293, esign 294-300, iam_group 301-304) |
| Extension tables | Physical Schema v6 lines 2087-2150 | 12 / 14 / 9 / 14 columns; the seven standard columns with the types of SPEC-011; `ck_contact_point_ext_type` |
| AC6 dictionary row | Physical Schema v6 line 5843, line 3626, line 3518 | `DF-ACE-018` = `v_ace_account.days_past_due`, `NUMBER`, `integer`, `ACE`, `public.account.delay_days`; the object row holds `DP01`; `DP01` refreshes `DAILY` |
| `RecoveryDatabaseIT` baseline | `RecoveryDatabaseIT.java` lines 36-46 and 99-103 | S1 stands at `true`; the baseline-row test reads `version = '0'`. TASK-14 replaces the environment and that assertion as SPEC-015(c) and SPEC-017 require |
| Tier 2 probe | `infra/postgres/schema/02-ace-tier2-probe.sql` | 14 `CREATE TABLE` and 12 `ALTER TABLE ... ADD COLUMN`; no grant to `ace_view_owner`. TASK-15 adds the SELECT stand-in for the 14 tables when the probe is on |
| Local init | `10-load-ace-database.sh` lines 31-37; `20-grants.sql.inc` | No S2 branch yet (RWB-E1-001 adds it); line 12 grants SELECT on all `public` tables; line 61 names `ace_view_owner` in the function default privilege. TASK-15 applies the Flyway-mode form |
| Frontend | `frontend/src/modules/recovery/api/platform.ts` | Reads an unchanged response; no change, no frontend task |

## Backend Plan

Surface status: **CHANGED**. Unit tests **REQUIRED** (trace SPEC-001..020; gate below).

`T` = `backend/src/test/java/th/co/scb/ace/demo/recovery`, `M` = `backend/src/main/resources/db/modulemigration/recovery`. Paths are relative to the repository root.

### Files added or changed — production (complete list)

| Kind | Path | Task | SPEC |
|---|---|---|---|
| Add | `M/V<seq>__rwb_e1_069_ace_source_views.sql` | TASK-09 | 001, 002, 003, 004 |
| Add | `M/V<seq>__rwb_e1_069_ace_tier2_views.sql` | TASK-11 | 005, 006 |

Line 1 of each file is `-- Story: RWB-E1-069`. No other main-source file is added or changed (SPEC-016): no Java class, `application.yaml`, `api/recovery-api-v4.yaml`, `frontend/**`, `backend/build.gradle.kts`, `scripts/dev.ps1` or `.gitlab-ci.yml`.

### Files added or changed — test scope, fixtures and test data (complete list)

| Kind | Path | Task | SPEC |
|---|---|---|---|
| Add | `T/ViewConformanceTest.java` | TASK-08, TASK-10 | 008, 009, 010, 011, 017, 018, 019, 020 |
| Add | `T/architecture/boundary/conformance/ConformanceTarget.java` | TASK-02 | 008 (ASM-004) |
| Add | `T/architecture/boundary/conformance/ConformanceTargetTest.java` | TASK-01 | 008 |
| Add | `T/architecture/boundary/SourceViews.java` | TASK-06 | 013 |
| Add | `T/architecture/boundary/SourceViewsReader.java` | TASK-06 | 013 |
| Add | `T/architecture/boundary/SourceViewsReaderTest.java` | TASK-05 | 013 |
| Add | `T/architecture/boundary/MigrationFolderCoverageTest.java` | TASK-07 | 013 |
| Add | `T/architecture/boundary/PublicTableDetector.java` | TASK-13 | 012 |
| Add | `T/architecture/boundary/AceTableCatalog.java` | TASK-13 | 012 |
| Add | `T/architecture/boundary/TableViewMap.java` | TASK-13 | 012 |
| Add | `T/architecture/boundary/Bnd6RuleTest.java` | TASK-12 | 012, 016 |
| Add | `T/dataengine/internal/AccountReader.java`, `AccountReaderOnView.java`, `NativeQueryReader.java`, `UnqualifiedReader.java`, `QuotedReader.java`, `JpqlPaymentReader.java`, `CatalogFilterReader.java`, `PublicAccountEntity.java` (AC8 fixtures, test sources) | TASK-12 | 012 |
| Add | `T/casewf/migration/RecoveryFlywayTestSupport.java` | TASK-07 | 015(c), 018 |
| Add | `backend/src/test/resources/db/recovery-migration-lint-exceptions.yaml` | TASK-03 | 014 |
| Add | `backend/src/test/resources/migration-lint/seam-e1069-01-view-public/**`, `seam-e1069-02-grant-other-key/**`, `seam-e1069-03-third-file/**`, `seam-e1069-04-grant-migrator/**`, `seam-e1069-05-views-pass/**` | TASK-03 | 014 |
| Edit | `T/architecture/RecoveryBoundaryTest.java` — the BND-6 method only (line 194-213): load the real `SourceViews`, build the detector, assert the message. Every other method is unchanged | TASK-13 | 012, 016 |
| Edit | `T/architecture/RecoveryMigrationLintTest.java` — register the five new fixture folders in the fixture list; no assertion changed | TASK-03 | 014 |
| Edit | `T/architecture/migration/LiteralSchemaRule.java`, `GrantRule.java`, `KeyDuplicateRule.java`, `MigrationRules.java`; add `LintExceptions.java` and `LintExceptionsLoader.java` in the same package | TASK-04 | 014 |
| Edit | `T/RecoveryDatabaseIT.java` — S1 `false`, S2 `false`; the view and history assertions of SPEC-015(c) and SPEC-017; every other assertion kept | TASK-14 | 015(c), 017 |
| Edit | `[E1-001] T/dataengine/internal/RecoverySchemaMigrationIT.java` — Flyway built through `RecoveryFlywayTestSupport` with `target` at the RWB-E1-001 version; assertions unchanged | TASK-07 | 015(c) |
| Edit | `backend/src/test/resources/architecture/recovery-modules.yaml` — the `sourceViews` key with 30 names | TASK-06 | 013 |

`[E1-001]` marks a file RWB-E1-001 creates. Its plan is not present at plan time; TASK-00 records the merged path and stops if the class is absent or its mechanism differs in a way the pin cannot absorb (assumption PA-E1-069-03, gap DG-P02).

### Files added or changed — local infrastructure and documentation

| Kind | Path | Task | SPEC |
|---|---|---|---|
| Edit | `infra/postgres/init/10-load-ace-database.sh` — delete the S2 `RWB_LOAD_REFERENCE_VIEWS` branch; keep the probe step, the S1 branch and the grant step | TASK-15 | 015(a) |
| Edit | `infra/postgres/init/20-grants.sql.inc` — Flyway mode: named `GRANT SELECT` on the 21 Tier 1 tables (and, with the probe on, the 14 Tier 2 tables) to `ace_view_owner`; keep `USAGE, CREATE` on `recovery`; narrow the function default privilege to `recovery_svc` only; keep the D-RUN-14 lines and everything else | TASK-15 | 015(b) |
| Edit | `.env.example` — `RWB_LOAD_REFERENCE_VIEWS=false` and the comment | TASK-15 | 015(a) |
| Edit | `docker-compose.yml` — `RWB_LOAD_REFERENCE_VIEWS: ${RWB_LOAD_REFERENCE_VIEWS:-false}` | TASK-15 | 015(a) |
| Edit | `README.md` — "Local versus target" row and the "Decisions taken while setting this up" item 8 | TASK-17 | 015(a), ASM-008 |
| Edit | `M/README.md` — RWB-E1-069 owns the view files; `V<seq>` example with no number fixed; the grant seam | TASK-17 | 015(a), DG-L18 |

Not changed: `backend/build.gradle.kts`, `backend/src/main/resources/application.yaml`, `backend/src/main/resources/application-local.yaml`, `api/recovery-api-v4.yaml`, `frontend/**`, `scripts/dev.ps1`, `.gitlab-ci.yml`, `infra/postgres/schema/**`, `infra/postgres/init/00-roles-and-databases.sh`.

## Migration order and numbering (D-RUN-07, D-RUN-12)

| # | Placeholder name | Ordinal | Contents | Merge condition |
|---|---|---|---|---|
| 1 | `V<seq>__rwb_e1_069_ace_source_views.sql` | A | PUBLIC revoke (step 1), three helpers, 16 views, grant block (steps 2-11) | After RWB-E1-001 merged; takes the next free four-digit number at merge |
| 2 | `V<seq>__rwb_e1_069_ace_tier2_views.sql` | B | 14 views, grant block (steps 5-11; step 1 omitted) | After RWB-ACE-001 is deployed in every environment `main` deploys to (DG-L20, OI-069-D). If its merge is later, it takes the next free number at that merge and stays contiguous |

- **A before B in ordinal and in merge.** Flyway is `outOfOrder(false)` with one history table, so a present lower version cannot be skipped and a lower version cannot arrive after a higher one (DG-L20). The two numbers assigned at merge are adjacent unless they merge in different requests, in which case each takes the next free number and B is still the later version.
- **No number is written in this plan, the tests, the README or the migration files.** The tests read the versions from the file names (SPEC-017).
- **Contiguity** is checked by RWB-E1-044's `L-SEQ-GAP`/`L-SEQ-DUP` over the merged folder; the E1-069 plan adds no number and no fixture number outside `backend/src/test/resources/migration-lint/**` (lint fixtures carry concrete numbers because the lint checks contiguity from the first number).
- **D-RUN-12** holds: neither file creates a table. The four extension tables are created once by the RWB-E1-001 migration (SPEC-007, DG-L01).

### Section A file contents, in order (SPEC-001..004)

Run as the migration account, which holds exactly the D-RUN-14 rights (USAGE on `public` with no table privilege; `ace_view_owner` membership `INHERIT FALSE, SET TRUE`) and owns schema `recovery`, or may grant CREATE on it (P4(a)-(c)).

1. `REVOKE ALL ON ALL TABLES IN SCHEMA ${recoverySchema} FROM PUBLIC` — **first**, before any `v_ace_*` view exists. A REVOKE only; no `GRANT ... ON ALL TABLES`.
2. The three helpers with `CREATE OR REPLACE`, `LANGUAGE sql`, `IMMUTABLE`, each with its `COMMENT ON FUNCTION`: `ace_to_boolean` and `ace_mask_value` as ACE Source Views v1 lines 49-86; `ace_to_date` to the SPEC-002 behaviour table (normalise the three shapes with `substr`, return `iso::date` only when `pg_input_is_valid(iso, 'date')`; NULL for everything else; never raises; `DateStyle` independent).
3. `REVOKE ALL ON FUNCTION` the three from `PUBLIC, ace_view_owner`.
4. `GRANT EXECUTE ON FUNCTION` the three `TO recovery_svc`.
5. `GRANT USAGE ON SCHEMA ${recoverySchema} TO recovery_svc`.
6. `GRANT USAGE, CREATE ON SCHEMA ${recoverySchema} TO ace_view_owner` (transient).
7. The 16 views with `CREATE OR REPLACE VIEW`, no `security_invoker`, every `public.<table>` qualifier kept and every `recovery.` qualifier written `${recoverySchema}.`.
8. Per view: `REVOKE ALL ON ${recoverySchema}.<view> FROM PUBLIC, recovery_svc, ace_view_owner`.
9. Per view: `GRANT SELECT ON ${recoverySchema}.<view> TO recovery_svc` — **before** the owner change.
10. Per view: `ALTER VIEW ${recoverySchema}.<view> OWNER TO ace_view_owner`.
11. `REVOKE USAGE, CREATE ON SCHEMA ${recoverySchema} FROM ace_view_owner`.

No statement on schema `public`, no `GRANT ... ON ALL TABLES`, no role creation, no `SET ROLE`, no grant to `rwb_migrator`, no `SET search_path`, no `CREATE SCHEMA`, no environment name.

### Section B file contents, in order (SPEC-005, -006)

Same header rules. Steps 5-11 of the Section A sequence for the 14 views: idempotent `GRANT USAGE` for `recovery_svc`, transient `USAGE, CREATE` for `ace_view_owner`, per-view REVOKE, per-view SELECT grant before the owner change, owner change, final revoke. Step 1 is omitted because the 16 Section A views are already owned by `ace_view_owner` and a schema-wide REVOKE then fails with `permission denied for table v_ace_*` ([E2] run 3). The helpers and their EXECUTE grants are already in place. The file grants nothing on a Tier 2 table (RWB-ACE-001 does).

## BND-6 rule (SPEC-012)

`RecoveryBoundaryTest.noRecoveryClassNamesAPublicTable` keeps its name and its assertion that the offender list is empty; the detector moves into the RWB-TE-001 tooling package so the coverage gate measures it.

| Detector | Input | What it catches |
|---|---|---|
| (a) qualified `public.<ident>` | each main file whole, comments removed, strings and text blocks kept | `public.account`, `"public"."account"`, `public . account`, concatenations spanning lines |
| (b) JPA annotations | ArchUnit over the imported main classes; the annotation property `schema` | `@Table`, `@SecondaryTable`, `@JoinTable` with `schema = "public"` |
| (c) SQL in annotations and JDBC strings | the text scan of the file, same view as (a) | `@Query`, `@NamedNativeQuery`, `@NamedQuery`, string arguments to `JdbcTemplate` or `JdbcClient` |
| (d) unqualified ACE table after `FROM`, `JOIN`, `UPDATE`, `INTO`, `TABLE` | the text scan | `select delay_days from account`, `FROM "account"`; keywords case-insensitive, identifiers lower case or quoted |

- **Allowed names** are the 30 in `sourceViews` (SPEC-013), read from the module map; no name is written in the test.
- **Exempt** (ASM-013): `information_schema.` and `pg_catalog.` qualifiers and the literal `'public'` used as a catalog filter value, so `PlatformInfoController` stays green.
- **ACE table set** is derived at test time from the `public.<name>` qualifiers in the E1-069 migration files; recovery tables are derived from the `CREATE TABLE` statements of every recovery migration and excluded, so `hearing` (a recovery table and a Section B view source name) is not treated as an ACE table.
- **Failure text**: `Boundary rule BND-6 broken: <SimpleClassName> reads public.<table>. Read recovery.<view> instead.` The `<view>` comes from the derived table-to-view map: the view whose top-level `FROM` names the table, otherwise the views that `JOIN` it, joined with ` or `; for a table no view reads, `Read a recovery.v_ace_* view instead.`
- **Fixtures** (test sources, package `th.co.scb.ace.demo.recovery.dataengine.internal` per ASM-007): `AccountReader` fails naming the class and `public.account`; `AccountReaderOnView` passes; `NativeQueryReader` (`@Query` with `public.account`) fails; `UnqualifiedReader` fails; `QuotedReader` fails; `JpqlPaymentReader` passes; `CatalogFilterReader` passes; `PublicAccountEntity` fails.
- **Where it runs**: the default `test` task. The fixture classes are test sources, so the real rule never scans them; `Bnd6RuleTest` applies the detector to them explicitly.

## `sourceViews` (SPEC-013)

`backend/src/test/resources/architecture/recovery-modules.yaml` gains the top-level key, in the [S1] §11 / [S2] order:

```yaml
sourceViews:
  sectionA: [v_ace_account, v_ace_payment, v_ace_customer, v_ace_contact, v_ace_ca_relation,
             v_ace_aa_relation, v_ace_collateral, v_ace_asset, v_ace_efs_action, v_ace_efs_action_code,
             v_ace_efs_assignment, v_ace_bucket_log, v_ace_product, v_ace_branch, v_ace_holiday, v_ace_plan]
  sectionB: [v_ace_batch_status, v_ace_valuation, v_ace_collateral_detail, v_ace_npa_asset, v_ace_npa_sale,
             v_ace_lawsuit, v_ace_hearing, v_ace_pod, v_ace_write_off, v_ace_score, v_ace_party_product,
             v_ace_credit_decision, v_ace_esign, v_ace_iam_group]
```

- `SourceViewsReader` reads `ModuleMap.sourceViews()` (the RWB-TE-001 loader keeps carrying it as an opaque value; it is not changed), builds a `SourceViews` record and fails with `{file}: {fieldPath}: {problem}` when a list is missing, a name breaks `^v_ace_[a-z0-9_]+$`, a name repeats across both lists, or the counts are not 16 and 14.
- `SourceViewsReader.validateAgainstFolder(SourceViews, Path)` applies the four migration-folder rules that hold before and after the Section B merge: every `v_ace_*` view a recovery migration creates is listed; the set the Section A file creates equals `sectionA`; if the Section B file is present its set equals `sectionB`, otherwise no file creates a `sectionB` name; BND-6 allows all 30 names in both states.
- All 30 names are added at once ([S1] §4 step 5). A change needs the data architect and the recovery tech lead.

## Lint seams in RWB-E1-044's lint (SPEC-014)

- **SEAM-E044-01.** `LiteralSchemaRule.isAllowedQualifier(statement, qualifier)` additionally returns true for `public` only when the statement is `CREATE [OR REPLACE] VIEW ${recoverySchema}.v_ace_<name>`. It never applies to `L-FK-OUTSIDE`, GRANT, REVOKE, ALTER or any other statement. The E1-069 fixture replaces the T-044-02 seam marker: the view statement passes; `SELECT a.id FROM public.t a`, `GRANT SELECT ON public.t TO x`, `CREATE VIEW ${recoverySchema}.v_other AS SELECT ... FROM public.t` and `REFERENCES public.t(id)` fail.
- **SEAM-E044-02.** Scoped to files whose key is `rwb_e1_069`:
  - `L-KEY-DUP` admits exactly two non-fix files, `…__rwb_e1_069_ace_source_views.sql` and `…__rwb_e1_069_ace_tier2_views.sql`; a third file or another suffix fails.
  - `L-GRANT` admits `GRANT` and `REVOKE` whose object is `SCHEMA ${recoverySchema}`, `${recoverySchema}.<object>`, `FUNCTION ${recoverySchema}.<fn>(…)` or (REVOKE only) `ALL TABLES IN SCHEMA ${recoverySchema}`, with grantees only `recovery_svc`, `ace_view_owner` or PUBLIC. A grant on `public`, `GRANT ... ON ALL TABLES`, another grantee, or a GRANT/REVOKE in a file of any other key fails.
- **One data file.** `backend/src/test/resources/db/recovery-migration-lint-exceptions.yaml` holds the story key, the two file-name suffixes, the grant objects and the grantee list. `LintExceptions` + `LintExceptionsLoader` (same package as the rules) read it; `MigrationRules.all()` keeps its no-argument form by loading the classpath resource and gains an `all(LintExceptions)` form for tests. The rules read the data; no key, suffix or grantee is written in rule code.
- **No role grant.** Neither file contains `SET ROLE` or a role-membership grant; the D-RUN-14 rights are RWB-E1-044 v14-7's local init, and `GRANT ... TO rwb_migrator` in a `rwb_e1_069` file fails `L-GRANT` (fixture). `ALTER VIEW ... OWNER TO ace_view_owner` is not a GRANT and is admitted.

## Local mode switch and stand-ins (SPEC-015)

**(a) Ownership.** RWB-E1-001 owns S1 `RWB_LOAD_REFERENCE_SCHEMA` (already `false` at its merge) and S3 `rwb.flyway.enabled: ${RWB_FLYWAY_ENABLED:true}`. This story owns **S2** `RWB_LOAD_REFERENCE_VIEWS`: it flips the default to `false`, deletes the branch from `10-load-ace-database.sh`, and keeps the variable named in `.env.example` and `docker-compose.yml` with `false` as an inert, documented switch (assumption PA-E1-069-09). The flip ships in the same merge as the Section A file.

- From that merge the 30 views come only from the two E1-069 files; init creates none, so the schema is empty at init and Flyway writes **no** version-`0` baseline row (DG-L30).
- `RWB_ACE_TIER2_PROBE` stays `true`.
- README "Local versus target" becomes "Flyway (E1-042, E1-043, E1-001, E1-069 migrations)" with no view stand-in; the migration-folder README names RWB-E1-069 as the owner of the view files (DG-L18).
- Developers run `./scripts/dev.ps1 reset` once, because init scripts run only on an empty volume. README records it.

**(b) Flyway-mode init.**

- Keep: `ALTER SCHEMA recovery OWNER TO rwb_migrator` (P4(c)); `REVOKE ALL ON SCHEMA public FROM PUBLIC`; `GRANT USAGE ON SCHEMA public TO ace_view_owner`; the `recovery_svc` and sequence grants; `GRANT USAGE, CREATE ON SCHEMA recovery TO ace_view_owner` (each E1-069 file revokes both at its last step).
- The D-RUN-14 rights are **not** repeated: `GRANT USAGE ON SCHEMA public TO rwb_migrator` and `GRANT ace_view_owner TO rwb_migrator WITH INHERIT FALSE, SET TRUE` are RWB-E1-044 v14-7 SPEC-017's and stay where that story put them.
- Replace `GRANT SELECT ON ALL TABLES IN SCHEMA public` with the named Tier 1 grants: `account, payment, customer, phone, email, address, ca_relation, aa_relation, collateral, asset, efs_action, efs_action_code, efs_assignment, bucket_log_snapshot, product, branch, bot_holiday, ace_case, cfsc_mg_ssme_tdr_case, tdr_calculation, ai_recommended_plan`.
- With `RWB_ACE_TIER2_PROBE=true`, add the named Tier 2 grants: `ace_batch_run, valuation, collateral_detail, npa_asset, npa_sale, lawsuit, hearing, pod_receipt, gl_write_off, collins_score, party_product, credit_decision, esign_request, iam_group`.
- Default privileges for functions name `recovery_svc` only (today line 61 also names `ace_view_owner`, which would give it EXECUTE on later functions and breach BR2).
- Not in this mode: `GRANT SELECT ON ALL TABLES IN SCHEMA public`, any grant option on a `public` table to `rwb_migrator`, any other role membership for `rwb_migrator`, any `GRANT` in a recovery migration.

Reference mode keeps its current statements and is an untested local deviation (ASM-008, README item 8).

**(c) Integration tests in Flyway mode.** `RecoveryDatabaseIT` moves to S1 `false`, probe on, S2 `false`; every assertion is kept except the version-`0` baseline-row assertion, which is retired with the S2 stage and replaced by the per-file history assertion of SPEC-017 (one `success = true` row for each applied file, no `version = '0'` row) — the one wording difference from RWB-E1-001 (DG-L30, OI-069-L). `ViewConformanceTest` uses the same container definition. `RecoverySchemaMigrationIT` keeps its "no `v_ace_*` view, no `ace_to_date`" assertions and E1-069 pins its Flyway to the RWB-E1-001 version through `RecoveryFlywayTestSupport` (ASM-014).

## Flyway test support and X2 (SPEC-018)

`RecoveryFlywayTestSupport` is a test-scope `BeanDefinitionRegistryPostProcessor` in `T/casewf/migration` (same package as the package-private `RecoveryFlywayConfig`), so it can import the class. It clears `initMethodName` on the `recoveryFlyway` bean definition before instantiation; the test context starts without `migrate()`, and the test gets the **real** `Flyway` bean with the bean's own configuration, then calls `Flyway.configure().configuration(bean.getConfiguration()).target(<version>)`. No setting is copied or restated; `RecoveryFlywayConfig` and `RecoveryMigrationRunner` stay unchanged. It is IT-only, outside the unit coverage bundle, with no unit-coverage claim (REVIEW-122).

X2 main case: a fresh Flyway-mode container with the probe applied and its grants, `DROP TABLE public.valuation` as superuser, migrate to the Section A version, then migrate fully. Assert a `FlywayException` whose cause has SQLSTATE `42P01` and a message containing `public.valuation` and `does not exist`; 16 `v_ace_*` views and none of the 14 Section B names; no `success = true` row for the Section B file; the 16 Section A views still return rows as `recovery_svc`. Probe-off case: `RWB_ACE_TIER2_PROBE=false`, same steps, the first failure names `public.ace_batch_run`, same end state.

### Conformance checks (SPEC-008..011)

| # | Session | Assertion | Failure text |
|---|---|---|---|
| 1 | `recovery_svc` | every `v_ace_*` view returns from `SELECT * ... LIMIT 1`; the count is exact for the migration-folder state (16 or 30) | `<view> does not compile: <database error>` |
| 2 | migration account | no `pg_constraint` row in `recovery` has `confrelid` outside `recovery`; no constrained column type outside `recovery` or `pg_catalog` | `<conname>` references `<schema>.<table>`; no constraint in recovery may reference another schema |
| 3 | migration account | one `sys_objects` row per view, one `sys_fields` row per column, `is_personal` non-null (SPEC-019) | `<view>.<column>` has no data dictionary entry |
| 4 | migration account (catalog calls), `recovery_svc` (direct read) | no USAGE on `public`, no privilege on any `public` relation, no INSERT/UPDATE/DELETE/TRUNCATE/REFERENCES/TRIGGER on a view; the direct read fails with 42501 | recovery_svc holds `<priv>` on `<object>`; the recovery role reads the views only |
| 5 | superuser (catalog) | the D-RUN-14 rights exactly: USAGE on `public` true and CREATE false, zero readable `public` relations, one `ace_view_owner` member row with `inherit_option = false`, `set_option = true`, `admin_option = false`, no superuser/createdb/createrole/bypassrls | the migration account holds more than the D-RUN-14 rights; RWB-E1-044 T-044-17 owns this assertion |

The four failing fixtures (an unreadable view, the FK to `public.account`, `legacy_bucket` with no `sys_fields` row, `GRANT INSERT` on `v_ace_account`) are added on a throwaway container after migration and never in the migration folder. **External mode** (`RWB_CONFORMANCE_TARGET=external`) runs checks 1-4 only: read-only, no fixture, no write, no check 5.

## Frontend Plan

**NOT_APPLICABLE.** UI In Scope NO; `DESIGN_EVIDENCE_STATUS: NOT_REQUIRED`; story §15 "No screen in this story". No file under `frontend/` is added or changed, no frontend unit-test or coverage task is created, and `frontend/components.md` is not required (no affected component, screen or flow). The unchanged frontend is still verified by `npm run check` in the merge gate (TASK-18). `contracts/frontend-integrations.json` records the N/A with this evidence.

## Unit test applicability

| Surface | Changes | Unit tests | Gate | Trace | Evidence and rationale | Test acceptance criteria |
|---|---|---|---|---|---|---|
| Backend | YES | **REQUIRED** | JaCoCo `recoveryCoverageVerification`: **LINE, INSTRUCTION, BRANCH and METHOD** at 0.80, one bundle: all recovery main classes plus RWB-TE-001's `architecture/boundary/**` and RWB-E1-044's `architecture/migration/**`; execution data from `test` only. Each new or changed tooling class in those directories reaches 80% on all four counters | SPEC-001..020 | No main class changes; the new measured logic is test-scope tooling (BND-6 detector, table-to-view map, `sourceViews` reader, conformance target, lint seams) and SQL. SQL behaviour is proved by the `recovery-it` tests, which are not counted toward unit coverage | `./gradlew test recoveryCoverageVerification` passes; XML and HTML saved under `implement/backend/coverage/` |
| Frontend | NO | NOT_APPLICABLE | NOT_APPLICABLE | SPEC-016 | No screen; `platform.ts` reads an unchanged response | N/A |

| Test case | Level | Covers | SPEC | Task |
|---|---|---|---|---|
| TC-E1-069-01 | recovery-it | AC1, BR1, BR2 | 001, 003, 007, 008, 015, 017 | TASK-08, -09 |
| TC-E1-069-02 | recovery-it | AC2, BR3 (and BR2) | 002, 004, 009, 015 | TASK-08, -09 |
| TC-E1-069-03 | recovery-it | AC3, BR1, BR9 | 005, 006, 008, 015, 017, 018 | TASK-08, -09, -10, -11 |
| TC-E1-069-04 | recovery-it | AC4, BR4 | 008 | TASK-08, -09 |
| TC-E1-069-05 | recovery-it | AC5, BR5 | 008, 010 | TASK-08, -09 |
| TC-E1-069-06 | recovery-it | AC6, BR6 | 003, 010, 020 | TASK-08, -09 |
| TC-E1-069-07 | recovery-it | AC7, BR7 | 007, 011 | TASK-08, -09 |
| TC-E1-069-08 | unit (`test`) | AC8, BR8 | 012, 013, 016 | TASK-12, -13 |
| T-E1-069-09 | recovery-it | BR6 literal calls, `ace_to_boolean`, `ace_mask_value`, function privileges | 002, 020 | TASK-08, -09 |
| T-E1-069-10 | recovery-it | BR6 through `v_ace_payment`; `DateStyle` | 002, 020 | TASK-08, -09 |
| T-E1-069-11 | unit | Lint seams SEAM-E044-01/02, §4 step 2 | 001, 014 | TASK-03, -04 |
| T-E1-069-12 | unit | `sourceViews` validation and migration-folder rules | 013 | TASK-05, -06, -07 |
| T-E1-069-13 | recovery-it | X2 probe-off case | 018 | TASK-10, -11 |
| T-E1-069-14 | recovery-it | BR2 end state after Section B | 006, 017 | TASK-10, -11 |
| T-E1-069-15 | recovery-it | Data protection checks | 019 | TASK-08, -09 |
| T-E1-069-16 | recovery-it | Flyway-mode `RecoveryDatabaseIT`; `RecoverySchemaMigrationIT` at the E1-001 version; the D-RUN-14 rights (check 5) | 008, 015, 018 | TASK-07, -08, -14, -15 |
| T-E1-069-17 | unit | Connection-input switch (`RWB_CONFORMANCE_TARGET`) with a stubbed environment | 008 | TASK-01, -02 |
| T-E1-069-18 | build | `./gradlew test recoveryCoverageVerification`, four counters at or above 80% | Unit Test Applicability | TASK-16 |

All `recovery-it` tests run on `postgres:16.16-alpine` (DG-L14), not PostgreSQL 17. API testing: N/A. Functional UI testing: N/A.

## Execution order (tests before code, AGENTS.md rules 3 and 10)

1. TASK-00 pre-flight on the worktree base; stop if E1-044 or E1-001 is not merged.
2. Red first: TASK-01 (compile-red, `ConformanceTarget` absent), TASK-03 (compile-red, lint exceptions absent), TASK-05 (compile-red, reader absent), TASK-07 (`MigrationFolderCoverageTest` red), TASK-08 (`ViewConformanceTest` red), TASK-10 (X2 red), TASK-12 (BND-6 red), TASK-14 (`RecoveryDatabaseIT` red).
3. Green: TASK-02, TASK-04, TASK-06, TASK-09, TASK-11, TASK-13, TASK-15.
4. Verification and evidence: TASK-16 (unit gate and coverage), TASK-17 (documentation), TASK-18 (container suite and e2e), TASK-19 (scope and guardrail check).

Each red run is recorded as command, exit code and first failing assertion under `implement/`.

## Functional Test Scenarios

| ID | Scenario | Owner | Assignment | Evidence |
|---|---|---|---|---|
| FTS-E1-069-01 | A developer adds a recovery class that names `public.account` and the build fails with the BND-6 line naming the class and the table | Functional Automation Test | **NOT_APPLICABLE** — no UI, no screen, no route; the same check executes as the unit test `Bnd6RuleTest` and `RecoveryBoundaryTest` in `./gradlew test`, which is not a functional automation result | `implement/unit-tests/report.md` |
| FTS-E1-069-02 | A deployment applies the Section A migration once and a second start applies nothing; the run is visible in `flyway_schema_history_recovery` | API Tester | **NOT_APPLICABLE** — no endpoint; `GET /api/recovery/v1/platform/info` is unchanged (SPEC-016) | T-E1-069-16 container result; no `api-tests/` run is required |
| FTS-E1-069-03 | A developer runs the conformance test against DEV or SIT and the 30 views, grants and dictionary rows are reported | Functional Automation Test | **NOT_APPLICABLE** as automation; the external run (`RWB_CONFORMANCE_TARGET=external`) is an environment check owned by the pipeline owner (ASM-004, OI-069-L(b)) | `implement/backend/external-run.md` when it happens; never reported as an executed test in this plan |
| HV-E1-069-01 | The environment owner and the ACE DBA apply P4(c)-(d) in SIT, UAT and PROD; who applies P4(a)-(b) stays OI-E044-I | Human (ACE DBA / environment owner / recovery tech lead) | Not testable here (no target databases); never reported as tested | OI-069-A, OI-069-M, OI-069-L |

No functional-automation or API-tester execution is planned: the story adds no screen, route or endpoint. This is recorded as `NOT_APPLICABLE` with the scope evidence above, not as an executed test.

## Requirement Logic To Task Coverage

`REQ_REF` values are the 42 rows of `../specify/spec.md` "Requirement-to-SPEC Logic Coverage" (unchanged, none merged or dropped). The first cell starts with the spec's `REQ_REF` ID; the words after it repeat the spec's requirement-logic statement for readability.

| REQ_REF | Mapped SPEC-* | Mapped TASK-* | Coverage Type | Verification | Status |
|---|---|---|---|---|---|
| AC1.1 Extension tables present | 007, 011 | TASK-08, -09 | INHERITED_EXISTING_BEHAVIOR | `ViewConformanceTest.extensionTables` on the RWB-E1-001-created tables | COVERED |
| AC1.2 16 Section A views created, 16 of 16 compile | 001, 003, 008 | TASK-07, -08, -09 | DIRECT_IMPLEMENTATION | `ViewConformanceTest.check1` and `MigrationFolderCoverageTest` | COVERED |
| AC1.3 One-row select from each of 16 returns | 008 | TASK-08, -09 | DIRECT_IMPLEMENTATION | check 1 as `recovery_svc`, `SELECT * ... LIMIT 1` per view | COVERED |
| AC1.4 No other `v_ace_*` view | 008, 013 | TASK-07, -08, -09 | DIRECT_IMPLEMENTATION | exact count and `SourceViews` rule 2 | COVERED |
| AC1.5 One history row for Section A after the RWB-E1-001 file | 017 | TASK-07, -08, -09 | DIRECT_IMPLEMENTATION | history assertion at `target` = Section A version | COVERED |
| AC1.6 Re-run: already applied, still 16 | 017 | TASK-08, -09 | DIRECT_IMPLEMENTATION | second `migrate()` reports 0 executed | COVERED |
| AC2.1 `recovery_svc` selects rows from `v_ace_account` | 004, 009 | TASK-08, -09 | DIRECT_IMPLEMENTATION | synthetic row read back as `recovery_svc` | COVERED |
| AC2.2 `public.account` to 42501 text | 009, 015 | TASK-08, -09, -15 | DIRECT_IMPLEMENTATION | `permission denied for schema public` in the `recovery_svc` session | COVERED |
| AC2.3 Insert, update, delete on the view to 42501 | 009 | TASK-08, -09 | DIRECT_IMPLEMENTATION | three refused statements | COVERED |
| AC2.4 Three `has_*_privilege` checks false | 009 | TASK-08, -09 | DIRECT_IMPLEMENTATION | catalog calls from the migration-account session | COVERED |
| AC2.5 `ace_view_owner` owns 16, SELECT on 21 Tier 1, no IUD | 004, 009, 015 | TASK-08, -09, -15 | DIRECT_IMPLEMENTATION | ownership and privilege queries | COVERED |
| AC2.6 `rwb_no_grant` cannot select | 009 | TASK-08, -09 | DIRECT_IMPLEMENTATION | fixture role with USAGE on `recovery` only | COVERED |
| AC3.1 14 Section B views compile; 30 = 16 + 14 | 005, 006, 008 | TASK-08, -10, -11 | DIRECT_IMPLEMENTATION | 30 of 30 compile and return a row | COVERED |
| AC3.2 One-row select from each of 30 | 008, 017 | TASK-08, -10, -11 | DIRECT_IMPLEMENTATION | check 1 after the full migration | COVERED |
| AC3.3 One history row for Section B after Section A | 017 | TASK-08, -10, -11 | DIRECT_IMPLEMENTATION | history at the full migration | COVERED |
| AC3.4 Without `public.valuation`: fails naming the relation, no Section B view, 16 unchanged | 018 | TASK-10, -11 | DIRECT_IMPLEMENTATION | X2 main and probe-off cases | COVERED |
| AC3.5 Section B features stay behind flags | 018 | TASK-10, -11 | INHERITED_EXISTING_BEHAVIOR | no such feature exists yet; the owners are consuming stories (Out of scope) | COVERED |
| AC4.1 No constraint names a table or type outside `recovery`; 0 rows | 008 | TASK-08, -09 | DIRECT_IMPLEMENTATION | check 2 | COVERED |
| AC4.2 Fixture FK fails with the story message; merge blocked | 008 | TASK-08, -09 | DIRECT_IMPLEMENTATION | `fk_case_account_account_key` fixture | COVERED |
| AC5.1 Totals by source system (123 / 1,382) | 010 | TASK-08, -09 | DIRECT_IMPLEMENTATION | dictionary totals on the merged seed; PA-E1-069-11 | COVERED |
| AC5.2 30 objects, 304 fields, 177 + 127 | 010 | TASK-08, -09 | DIRECT_IMPLEMENTATION | dictionary queries per view | COVERED |
| AC5.3 Table fields 1,078; 49 on extension tables | 010 | TASK-08, -09 | DIRECT_IMPLEMENTATION | dictionary queries; PA-E1-069-11 | COVERED |
| AC5.4 One `sys_objects` row per view, one `sys_fields` row per column | 008, 010 | TASK-08, -09 | DIRECT_IMPLEMENTATION | check 3 | COVERED |
| AC5.5 `legacy_bucket` fixture fails with the story message | 008 | TASK-08, -09 | DIRECT_IMPLEMENTATION | fixture column on a copy of `v_ace_account` | COVERED |
| AC6 DF-ACE-018 attributes; `ACC0000017` returns 95 | 003, 010 | TASK-08, -09 | DIRECT_IMPLEMENTATION | dictionary row and view read | COVERED |
| AC7.1 Four tables: column counts, PKs, check constraint | 011 | TASK-08, -09 | DIRECT_IMPLEMENTATION | catalog shape of the four tables | COVERED |
| AC7.2 49 columns, 49 fields DF-EXT-001..049; no FK to `public` | 010, 011 | TASK-08, -09 | DIRECT_IMPLEMENTATION | column and dictionary queries | COVERED |
| AC7.3 Duplicate `P0000123` to 23505, one row | 011 | TASK-08, -09 | DIRECT_IMPLEMENTATION | second insert refused | COVERED |
| AC8.1 `AccountReader` on `public.account` fails; on the view passes | 012 | TASK-12, -13 | DIRECT_IMPLEMENTATION | `Bnd6RuleTest` and `RecoveryBoundaryTest` | COVERED |
| AC8.2 Native query on `public.account` fails | 012 | TASK-12, -13 | DIRECT_IMPLEMENTATION | `NativeQueryReader` fixture | COVERED |
| AC8.3 Allowed names read from the module map | 012, 013 | TASK-06, -13 | DIRECT_IMPLEMENTATION | `SourceViewsReader` feeds the detector | COVERED |
| BR1 Read only through 30 SELECT-only views; nothing loaded or copied | 003, 006, 009, 012 | TASK-08, -09, -13 | DIRECT_IMPLEMENTATION | TC-01, -03, -08 | COVERED |
| BR2 `ace_view_owner` owns, SELECT on ACE tables, writes nothing, no other right | 004, 006, 009, 015, 017 | TASK-08, -09, -11, -15 | DIRECT_IMPLEMENTATION | TC-01, -02, T-E1-069-14 | COVERED |
| BR3 `recovery_svc` SELECT only; nothing in `public`; PUBLIC nothing; no view write | 002, 004, 008, 009 | TASK-08, -09 | DIRECT_IMPLEMENTATION | check 4, TC-02 | COVERED |
| BR4 No constraint outside `recovery`; ACE link is `varchar(255)` | 007, 008, 011 | TASK-08, -09 | DIRECT_IMPLEMENTATION | check 2 and the extension shape | COVERED |
| BR5 `sys_objects` and `sys_fields` per view and column | 008, 010 | TASK-08, -09 | DIRECT_IMPLEMENTATION | check 3 | COVERED |
| BR6 `ace_to_date`, `ace_to_boolean` return NULL rather than fail | 002, 020 | TASK-08, -09 | DIRECT_IMPLEMENTATION | T-E1-069-09 and -10 | COVERED |
| BR7 Extension tables: decisions not copies; 1:1; seven standard columns | 007, 011 | TASK-08, -09 | DIRECT_IMPLEMENTATION | AC7 and the column-name comparison with the views | COVERED |
| BR8 BND-6; allow-list from the module map | 012, 013, 016 | TASK-06, -12, -13 | DIRECT_IMPLEMENTATION | TC-08, `PlatformInfoController` fixture | COVERED |
| BR9 Section B after its ACE table; later Flyway sequence | 005, 006, 013, 018 | TASK-10, -11, -19 | DIRECT_IMPLEMENTATION | X2, merge condition, scope check | COVERED |
| §4 step 2 No environment name; `${recoverySchema}`; role names | 001, 014 | TASK-03, -04, -09 | DIRECT_IMPLEMENTATION | lint `L-LITERAL-SCHEMA` and the seam fixtures | COVERED |
| §17 guardrails View list and roles as data; synthetic data; forward only; identity number never in clear | 001, 005, 013, 019 | TASK-06, -08, -09, -19 | DIRECT_IMPLEMENTATION | `sourceViews`, SPEC-019 checks, scope check | COVERED |

No row is `BLOCKED`.

**Coverage type note.** `AC1.1` and `AC3.5` are `INHERITED_EXISTING_BEHAVIOR`: the extension tables are created by the RWB-E1-001 migration and this story verifies them (SPEC-007, DG-L01), and no Section B feature exists yet. Every other row is `DIRECT_IMPLEMENTATION`. The plan gate allows these two values; no row is marked in any other way.

## SPEC to task map

| SPEC | Tasks | Tests |
|---|---|---|
| 001 | TASK-03, -04, -09 | T-E1-069-11; `MigrationFolderCoverageTest` |
| 002 | TASK-08, -09 | T-E1-069-09, -10; TC-06 |
| 003 | TASK-08, -09 | TC-01, TC-06 |
| 004 | TASK-08, -09 | TC-01, TC-02 |
| 005 | TASK-10, -11 | TC-03; T-E1-069-13 |
| 006 | TASK-10, -11 | TC-03; T-E1-069-14 |
| 007 | TASK-08, -09 | TC-01, TC-07 |
| 008 | TASK-07, -08, -09, -14 | TC-01..05; T-E1-069-16, -17 |
| 009 | TASK-08, -09 | TC-02 |
| 010 | TASK-08, -09 | TC-05, TC-06 |
| 011 | TASK-08, -09 | TC-07 |
| 012 | TASK-12, -13 | TC-08; `Bnd6RuleTest` |
| 013 | TASK-05, -06, -07 | T-E1-069-12; `MigrationFolderCoverageTest` |
| 014 | TASK-03, -04 | T-E1-069-11 |
| 015 | TASK-07, -14, -15, -17 | T-E1-069-16; `RecoveryDatabaseIT` |
| 016 | TASK-13, -19 | TC-08; scope check |
| 017 | TASK-08, -09, -10, -11, -14 | TC-01, TC-03; T-E1-069-14 |
| 018 | TASK-07, -10, -11 | TC-03; T-E1-069-13 |
| 019 | TASK-08, -09, -16 | T-E1-069-15 |
| 020 | TASK-08, -09 | T-E1-069-09, -10 |

No orphan: every SPEC 001-020 has at least one task.

## Screen-to-task mapping

`NOT_APPLICABLE`: UI In Scope NO, `DESIGN_EVIDENCE_STATUS: NOT_REQUIRED`, no effective-screen node and no `SCR-*` screen in the spec. `SCR-44` is read only by the platform administrator and is out of scope. No screen consolidation task is required; the pre-submit check in `tasks.md` records this.

## Security, privacy and compliance

- **Database privilege boundary.** BR2 and BR3 are enforced in the catalog: `ace_view_owner` owns the 30 views and holds SELECT on the ACE tables; `recovery_svc` holds SELECT on the views and EXECUTE on the three helpers, nothing in `public`; PUBLIC holds nothing. The migration account holds exactly the D-RUN-14 rights; `GRANT ... TO rwb_migrator` in an E1-069 file fails the lint (SPEC-014).
- **BND-6** is the build-time half: no recovery class may name a `public` table, and `PlatformInfoController` stays green under the ASM-013 exemptions.
- **Personal data.** The published interface carries 250 personal DF-ACE fields, 12 Restricted. `v_ace_customer` exposes the identity number only as `id_no_masked` and `id_no_last4`; `v_ace_contact.contact_value` stays in clear with a masked copy, because display masking is RWB-E1-037's. Every read of a personal field is logged by RWB-E1-016. Definer rights mean any ACE row-level security must be applied inside the view; recorded for the security review (OI-069-H).
- **Synthetic data only.** `ACC0000017` (with `delay_days` 95), `P0000123`, the identification value `X000000005678`, the container passwords `it-migrator` / `it-recovery` and the fixture rows are synthetic. No real name, ID number, account number or address appears in a migration, test, fixture, log line or this plan. No credential is in code; the external mode reads credentials from pipeline variables only.
- **Audit.** No case or decision changes. The migration record is the history table plus the build report. KYC/AML, suitability and approval are not in scope (no business decision).
- **Approval.** Nothing here claims a human approval. D-RUN-14 is the orchestrator's decision, applied as recorded, with ratification open (OI-069-M / OPEN-051).

## Release and rollback

- **Release:** no runtime feature flag for the views; they are the read path, not a feature (story §13). The two migrations apply at deployment through the recovery Flyway step (RWB-E1-044); the Section B file stays out until RWB-ACE-001 is deployed in every environment `main` deploys to.
- **Release note item:** after this merge the local stack builds the 30 views from Flyway, no version-`0` baseline row is written, and a developer must run `./scripts/dev.ps1 reset` once because init scripts run only on an empty volume. Opt-in reference mode (`rwb.flyway.enabled=false`) remains available and untested.
- **Rollback:** forward only (NFR-027; BS-2.3). Redeploying the previous tag applies nothing (Flyway `outOfOrder(false)`, `*:future` default); a wrong view is corrected by a corrective migration with the next sequence, the same story key and line 2 `-- Fix: <reason>` (D-RCV-28). `clean` stays disabled in every environment.
- **Merge gate:** the orchestrator merges into `develop-recovery` only after `./scripts/dev.ps1 test` exits 0 and `./scripts/dev.ps1 it` exits 0 on the branch (D-RCV-44). `recoveryCoverageVerification` is shown separately at the code gate.

## Assumptions

Plan-stage assumptions are in `assumptions.md` (PA-E1-069-01..17). Spec assumptions ASM-001..017 are carried unchanged and are not re-litigated here. Document gaps are in `document-gaps.md` (DG-L01..L30 carried; DG-P01..P03 added by this stage, all Blocker = No).

## Status

```text
PLANNER_STATUS_SUMMARY: Plan ready: 20 tasks (TASK-00..TASK-19) for the two view migrations, the 30-view grants, the extension-table and dictionary evidence, BND-6, the sourceViews key, the two lint seams, the S2 local switch, the Flyway-mode tests and the gates.
PLANNER_STATUS_DETAIL: SUCCESS [REASON: spec revision 4 passed the spec gate round 4 (PASS 0/0/0/0); every SPEC-*, AC clause, BR and TC maps to tasks and named tests] [UNBLOCK_ACTION: n/a]
PLANNER_CLARIFICATION_STATUS: READY [OPEN_ITEMS: 0] [UNBLOCK_ACTION: n/a]
PLANNER_DESIGN_SOURCE: NOT_REQUIRED [NOTE: UI In Scope NO; DESIGN_EVIDENCE_STATUS NOT_REQUIRED]
PLAN_REQUIREMENT_COVERAGE_SUMMARY: 42 requirement-logic rows, SPEC-001..020, AC1..AC8 (31 clauses), BR1..BR9, TC-E1-069-01..08 and T-E1-069-09..18 each map to tasks and named tests; AC1.1 and AC3.5 are inherited existing behaviour with verification evidence.
PLAN_REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 42] [TASK_COVERED_RULES: 42] [MISSING_TASK_RULES: 0] [AMBIGUOUS_TASK_RULES: 0] [CONTRADICTIONS: 0]
GATE_REVIEW: PENDING_ORCHESTRATOR
```
