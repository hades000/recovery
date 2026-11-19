---
title: "Implementation Plan: RWB-E1-043 Reference data service with versioned tables"
run_id: "INC-008-epic-1-RWB-E1-043"
story: "RWB-E1-043"
epic: "EPIC-001"
status: "SUCCESS"
revision: "v1 (18 Nov 2026): first plan stage for this run, written after spec revision 10 passed spec gate round 10 (PASS 0 Critical / 0 High / 0 Medium / 0 Low, `../review/spec-gate-review-10.md`). No earlier plan exists in this run (the previous attempt failed before writing). Built on RWB-TE-001 plan v7, RWB-E1-044 plan v2 and RWB-E1-042 plan v2; no number is fixed for the migration (D-RUN-07)."
prepared: "2026-11-18"
---

# Implementation Plan: RWB-E1-043 Reference data service with versioned tables

Design Source: `NOT_REQUIRED` (UI In Scope: NO; `DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0]` in `../specify/figma/figma_report.md` and `../specify/spec.md`).

| Field | Value |
|---|---|
| Spec | `../specify/spec.md` revision 10 (file 2026-11-18 07:48:54). Spec gate round 10 `REVIEW-RWB-E1-043-SPEC-010`: `PASS` 0 Critical / 0 High / 0 Medium / 0 Low (`../review/spec-gate-review-10.md`). `status: SUCCESS_WITH_ASSUMPTIONS`; `REQUIREMENT_COVERAGE_SUMMARY: 49 requirement rows mapped, built and tested here; 16 requirement lines assigned to other stories or open owners`; `REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 49] [COVERED_RULES: 49] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 40]`. The 40 source contradictions are settled in the spec; this plan introduces no new one. |
| Story | User Stories Epic 1 Story Files v7, RWB-E1-043 v2 (`requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-043-reference-data-service-with-versioned-tables-v2.md`), sections 1 to 19. |
| Base layout (D-RUN-17) | RWB-TE-001 plan v7 (`../../INC-002-epic-1-RWB-TE-001/plan/plan.md`, `tasks.md`, `data-model.md`; its plan gate round 7 `PASS` 0/0/0/0). TE-001 merges first (Build Sequence v6 order 2). |
| Migration convention | RWB-E1-044 plan v2 (`../../INC-001-epic-1-RWB-E1-044/plan/plan.md`, `tasks.md`, `data-model.md`; plan gate round 2 `PASS`) and its SPEC-001, -007, -014: one file per story, `<seq>` assigned at merge (D-RUN-07, D-RCV-28), identifier-only quote-aware lint in `RecoveryMigrationLintTest` (T-044-21). |
| Parameter catalog and seams | RWB-E1-042 plan v2 (`../../INC-003-epic-1-RWB-E1-042/plan/plan.md`, `tasks.md`, `data-model.md`; plan gate round 2 `PASS`), built against its spec revision 13: `casewf.config.api` types, `access.api` types, `parameter_catalog` and `parameter_value`, `config/parameter-catalog.csv` (19 rows), `access/interim-capability-grants.csv`, `FixedMessageCatalog` (nine IDs), `CatalogFileParser` and `CatalogCompletenessRules`. E1-042 merges before this story (Build Sequence order 3; this story order 8). |
| Code base | This repository as read on 18 Nov 2026 (the pre-TE-001 layout today: `backend/src/main/java/th/co/scb/ace/demo/recovery/{platform,rules,workflow,documents}`; `backend/src/main/resources/db/modulemigration/recovery/README.md` and no `.sql` file; `backend/build.gradle.kts`; `backend/src/main/resources/application.yaml` and `application-local.yaml`; `infra/postgres/init/**`; `infra/postgres/schema/03-recovery-physical-schema-v6.sql`). No git command, container or build was run; no file outside `aisdlc/output/INC-008-epic-1-RWB-E1-043/plan/` was written. |
| Paths | Every path below is the file's path in this repository. Paths marked `[TE-001]` exist only after RWB-TE-001 merges; `[E1-044]` marks the migration lint and Flyway runner that story leaves; `[E1-042]` marks files and types that story leaves. Nothing from the v2 ACE monorepo layout is assumed. |
| Builder | Implementation Builder in its own git worktree from `develop-recovery` **after** RWB-TE-001, RWB-E1-044 and RWB-E1-042 merge (PRE-1..PRE-3). Commits `RWB-E1-043: <summary>` with the `AISDLC-Run` and `AISDLC-Plan` trailers. |
| Smallest change | One P3 package pair (`casewf.refdata`, `casewf.refdata.api`), seven additive P4 types (the LOV read interface, the five handler SPI types and the interim LOV reader), three controller operations in one P3 controller, one migration, 38 catalog rows, 37 Reference data grant rows, one flag key, and test scope. No new dependency, no build-file edit, no OpenAPI change, no frontend change, no new Gradle project. |
| One module | **PASS - one ACE module (recovery)**, nested P3 `casewf.refdata` and additive P4 `access`; see "One-module check (D-RUN-21)". No analyst or tech-lead approval is claimed. |

## Upstream readiness

| Check | Result |
|---|---|
| Spec status | `SUCCESS_WITH_ASSUMPTIONS`; every in-scope rule mapped, 46 labelled assumptions (A-32 withdrawn), 59 gaps, 0 blocking |
| Spec gate | `PASS` round 10, 0 findings (`../review/spec-gate-review-10.md`); findings 159 and 160 resolved; no resolved finding reopened |
| `REQUIREMENT_COVERAGE_RESULT` | 49 of 49 rules covered, `MISSING_RULES: 0`; the 40 source contradictions are settled by precedence, orchestrator rulings or labelled assumptions |
| Clarification log | 20 rows, all `RESOLVED` or `RESOLVED_BY_ASSUMPTION`; `CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]`; no `OPEN` row |
| Design evidence | `NOT_REQUIRED`: UI In Scope NO, 0 screens, no Figma link, no `frontend/components.md` |
| Migration | One file, `<seq>` not fixed (D-RUN-07) |
| Base dependency | RWB-TE-001 (order 2), RWB-E1-044 (order 1) and RWB-E1-042 (order 3) are earlier stories, not seams (D-RUN-08, D-RUN-17). The plan stops if any is absent (PRE-1..PRE-3) |

`PLANNER_CLARIFICATION_STATUS: READY [OPEN_ITEMS: 0] [UNBLOCK_ACTION: n/a]`. The spec has no `OPEN` clarification row. The owner-acceptance items (A-01, A-07, A-08, A-09/A-34, A-16, A-17, A-27, A-31, A-33, A-37, A-38, A-39, A-40, A-41, A-42) and the unratified orchestrator rulings (D-RUN-08, D-RUN-10, D-RUN-11, D-RUN-12, D-RUN-18, D-RUN-19, D-RUN-20, D-RUN-21 and the 2026-11-18 triage) are carried open; none is accepted or ratified here, and OPEN-050 stays open (owner: recovery tech lead).

## Base and dependency outputs (read, not rebuilt)

| Output | What this plan takes | Where applied |
|---|---|---|
| `aisdlc/output/INC-002-epic-1-RWB-TE-001/plan/plan.md` v7, `tasks.md`, `data-model.md` | Module map, P3 `casewf` and P4 `access` homes, the package-private module records, `RecoveryBoundaryTest` and `BoundaryRules`, `T-TE001-14` (`publishedSurfaceIsExactlyTheSpecifiedTypes`), `T/testsupport/ApplicationYamlEnvironment.java`, the combined JaCoCo bundle (`recoveryClasses` + `boundaryToolingClasses`), `RecoveryMigrationLintTest` position. Merges first (D-RUN-17). | TASK-00, TASK-05, TASK-06, TASK-16 |
| `aisdlc/output/INC-001-epic-1-RWB-E1-044/plan/plan.md` v2, `tasks.md`, `data-model.md` | `RecoveryFlywayConfig` in P3 `casewf.migration`, `MigrationPropertiesConfig`, `RecoveryMigrationRunner`, `RecoveryMigrationProperties`, the identifier-only quote-aware `RecoveryMigrationLintTest` (T-044-21), `migrationToolingClasses` in both JaCoCo tasks, the `${recoverySchema}` migration folder and `README.md`. Order 1. | TASK-00, TASK-02, TASK-16 |
| `aisdlc/output/INC-003-epic-1-RWB-E1-042/plan/plan.md` v2, `tasks.md`, `data-model.md` | `casewf.config.api` (`ParameterService`, `ParameterKeys.byName(String, Class<T>)`, `ParameterLoadHandler`, `ParameterLoadResult`, `BusinessDateProvider`), `access.api` (`MessageResolver`, `CapabilityCheck`, `ApiProblemException` status-and-message-ID form, `ApiError`, `CatalogParameterReader`), `access.internal` (`FixedMessageCatalog`, `InterimCapabilityCheck` bean `capabilityCheck`, `ApiExceptionHandler`, `ProblemFactory`), `parameter_catalog` (22 columns) and `parameter_value` (19 + 3 columns), `config/parameter-catalog.csv` (19 rows), `access/interim-capability-grants.csv`, `CatalogFileParser` and `CatalogCompletenessRules` in `architecture/parameters`, `parameterToolingClasses` in both JaCoCo tasks. Order 3. | TASK-00, TASK-04, TASK-06, TASK-08, TASK-10, TASK-12, TASK-14, TASK-16 |
| `../specify/spec.md` revision 10, `contracts/backend-apis.json` revision 10, `contracts/frontend-integrations.json` revision 8 | The 32 SPEC rows, 49 requirement rows, 40 test IDs, SEC-01..17, CLAR-001..020, the three operations and their error sets, the handler contract, the check order and the module scope | Whole plan |
| `aisdlc/docs/decisions/d-rcv-35-ace-db-alignment.md`, `d-rcv-36-temporal-and-drools.md`, `requirement/legacy/05-technical-architecture/recovery-workbench-architecture-decision-records-v3.md`, `requirement/legacy/01-decisions-and-governance/recovery-workbench-decision-log-v10-xlsx.md` | D-RCV-28 (migration), D-RCV-35 U4 (views only), D-RCV-36 (no rule table), ADR-010 (database roles), ADR-012 (Drools) | TASK-02, TASK-19 |

## Plan-time checks (read only)

| # | Check | Result (18 Nov 2026) |
|---|---|---|
| 1 | TE-001 v7 homes | P3 `casewf` with `api`, `config.api`, `rules`, `timers`, `workflow`; P4 `access.api` with `ApiError`, `ApiProblemException`, `MessageResolver`, `CapabilityCheck`, `CatalogParameterReader`; P4 `access.internal` with `ApiExceptionHandler`, `ProblemFactory`, `SecurityConfig`, `InterimCapabilityCheck`, `FixedMessageCatalog`, `LovValueReader` (to be added here). The old `platform`, `rules`, `workflow`, `documents` packages are deleted by TE-001. |
| 2 | `[E1-044]` migration lint | `backend/src/test/java/th/co/scb/ace/demo/recovery/architecture/RecoveryMigrationLintTest.java` is the identifier-only, quote-aware version (T-044-21). The current pre-merge file is line-based and would flag `recovery.` inside a string; the plan's seed `used_by` and `description` values are literals, so the branch must be cut after E1-044 (PRE-2). |
| 3 | `[E1-042]` names in force | Spec revision 13 `section 12.2`, `section 12.7`, `section 12.10`, `section 12.12`: `ParameterService`, `ParameterKeys.byName(String key, Class<T> type)`, `ParameterLoadHandler`, `ParameterLoadResult`, `BusinessDateProvider`, `MessageResolver.english/thai`, `CapabilityCheck.has/require`, `ApiProblemException(HttpStatus, String, Map, String, String, Throwable)` with `status()`, `messageId()`, `field()`, `detail()`, `ApiError`; shared update R6 asks for stable names. |
| 4 | E1-042 message catalog | `access.internal.FixedMessageCatalog` holds nine IDs: `MSG-P3-032`, `MSG-GEN-002`, `MSG-P1-002`, `MSG-GEN-001`, `MSG-P7-002`, `MSG-P3-015`, `MSG-P3-027`, `MSG-GEN-004`, `MSG-P7-003` (E1-042 data-model section 7). All story message IDs this plan uses for production paths are there; `MSG-P4-001/002/003` stay in `ApiError`. Fixture handler IDs are supplied by a test resolver (TASK-15). |
| 5 | `ApiProblemException#error()` callers | Exactly two, both in `ApiExceptionHandler.problem` (`platform/internal` today, `access/internal` after TE-001). This plan adds no caller of `error()`; the status-and-message-ID form from E1-042 is used for story messages; `ApiError.NO_ROLE`/`NOT_IN_SCOPE`/`NOT_PERMITTED` forms are used for 401/404/403. |
| 6 | `CatalogCompletenessRules` and dynamic keys | The E1-042 rule scans a `ParameterKeys` constant, a `ParameterKey.of("...", X.class)` call and the first argument of a reader call (`CatalogParameterReader.get`, `ParameterService.get`). `ParameterKeys.byName(String, Class<T>)` is not one of the scanned forms (E1-042 plan v2 "Tooling design"), so this story's per-code lookups do not trip it. TASK-00 re-reads the merged rule; if the merged rule does scan `byName`, the builder stops and reports (PG-E1-043-06), because the spec A-26 requires those lookups. |
| 7 | POI for XLSX | `org.drools:drools-decisiontables:10.2.0` POM declares `org.apache.poi:poi-ooxml` with no `test` scope (`poi-ooxml-5.4.1` and `poi-5.4.1` are in the local Gradle cache). POI is on the compile and runtime classpath transitively, so no new dependency is declared (A-21; AGENTS section 4.4). |
| 8 | Hibernate JSON mapping | Hibernate ORM 7.4.13 (`org.hibernate.orm:hibernate-core`) supports `org.hibernate.annotations.JdbcTypeCode` and `org.hibernate.type.SqlTypes.JSON`; Jackson 3 is on the runtime classpath through Boot 4.1. `reference_row.row_data` is mapped as `Map<String, Object>` with `@JdbcTypeCode(SqlTypes.JSON)`. |
| 9 | Migration folder | `backend/src/main/resources/db/modulemigration/recovery/` holds `README.md` only today; no `.sql` file exists, so no `<seq>` can be inferred. The plan uses `V<seq>__rwb_e1_043_reference_versions.sql` (D-RUN-07). |
| 10 | Catalog CSV | `config/parameter-catalog.csv` is created by E1-042 with 19 rows and the 16-column header (`key,kind,value_type,unit,min_value,max_value,default_value,scope,required,owner_role,environments,used_by,secret,value_source,env_property,description`). This story adds 38 rows for 57 total. The `refdata.cache.ttl-seconds` row (E1-042 row 2) is the TTL source. |
| 11 | Grants CSV | `access/interim-capability-grants.csv` is created by E1-042 with header `role,area,rights` and one row per RW- role for area `Rules and parameters`. This story adds one row per RW- role for area `Reference data` (37 rows), from Users, Roles and Permissions v4 lines 73-110 plus the six A roles of A-08. |
| 12 | Flag keys | `application.yaml` has `rwb.p3.temporal` and `rwb.p3.drools` as `@ConditionalOnProperty` inputs; `application-local.yaml` sets them `true`. `rwb.p3.refdata-versions` is new and follows the same shape; `RefdataSettings` binds it (A-44). |
| 13 | API v4 shapes | `ReferenceLoad` (`api/recovery-api-v4.yaml` lines 8832-8846) has `id` (uuid), `table`, `validFrom` (date), `status`, `rows` (integer). `RollbackRequest` (line 9818) has `reason`. The three operations are at lines 3167, 3214 and 5004. No OpenAPI edit. |
| 14 | Boundary test after E1-042 | `[TE-001] T/architecture/RecoveryBoundaryTest.java` carries `publishedSurfaceIsExactlyTheSpecifiedTypes` (T-TE001-14); E1-042 extends the expected sets with its eleven `casewf.config.api` types, four `access.api` entries and `config.api`. This plan adds six public P3 types, seven `access.api` entries (six types plus `ReferenceTableHandler.Dating`) and `refdata.api`. |
| 15 | `scripts/dev.ps1` | `test` runs `Invoke-Gradle test` then `Invoke-Npm run check`; `it` runs `Invoke-Gradle recoveryIntegrationTest`. Gradle runs in `backend/` with `$env:JAVA_TOOL_OPTIONS="-Djdk.net.unixdomain.tmpdir=$env:USERPROFILE\.gradle\uds"`. |
| 16 | One-module reading | D-RUN-21 (`AI-SDLC-BUILD-LOG.md` decisions table, 18 Nov 2026 05:36, orchestrator Claude Code; not ratified, OPEN-050) reads "touches one module" as the ACE module (recovery). This P3 + P4 plan stays inside `th.co.scb.ace.demo.recovery`; no `common` or `collection` change. |

## Scope

In scope (each bullet maps to tasks in `tasks.md`):

1. **S-1 Migration:** one `V<seq>__rwb_e1_043_reference_versions.sql` with the two version/row tables exactly as Physical Schema v6, the changed row key, the constraints, indexes and append-only triggers, and the 38 `parameter_catalog` rows (SPEC-001, SPEC-029). -> TASK-01, TASK-02
2. **S-2 Catalog file:** 38 rows in `config/parameter-catalog.csv`: 12 `refdata.columns.<code>` definitions (default `none`), 13 `rwb.refload.loader.<code>` and 13 `rwb.refload.approver.<code>` lists (SPEC-029). -> TASK-03, TASK-04
3. **S-3 Published surface:** P3 `refdata.api` (six types), P4 `access.api` LOV read interface and five handler SPI types, P4 interim `LovValueReader`, module map and T-TE001-14 extension (SPEC-002, SPEC-019, SPEC-025). -> TASK-05, TASK-06
4. **S-4 Column definitions and row check:** `ReferenceTableColumns` (grammar `name:TYPE[:R][:K]`), `ReferenceRowCheck` (required, type, unknown column, row key, detail), `ContentHasher` (canonical SHA-256), `ReferenceLoadFileReader` (CSV RFC 4180 and XLSX first sheet) (SPEC-003, SPEC-006, SPEC-015). -> TASK-07, TASK-08
5. **S-5 Registry:** published `ReferenceVersionRegistry` (`recordVersion`, `approve`, `rollback`, `versionByLoadId`), the version numbering, idempotency, maker-checker, `valid_to` recomputation, optimistic lock, rollback rules, handler apply/onRolledBack, AC-VERS recorder, after-commit cache eviction and audit (SPEC-004..010, SPEC-024, SPEC-025, SPEC-032). -> TASK-11, TASK-12
6. **S-6 Read side:** `ReferenceDataService`, `ReferenceDataReaders` (`forReader`, `enabled`), `ReferenceRowCache`, `ReferenceVersionLogger`, `ReaderLogGate`, `NoVersionInForceException`, the counter and the ERROR line (SPEC-011..014). -> TASK-09, TASK-10
7. **S-7 HTTP and authority:** `ReferenceLoadController` (three operations, multipart, `@PreAuthorize`), `ReferenceLoadDispatcher`, `ParameterLoadBranch`, `ActorIdResolver`, `ReferenceLoadAuthority`, `ReferenceLoadAudit` and adapter, `ReferenceLoadView`, `RollbackRequest` (SPEC-015..018, SPEC-020, SPEC-024..028, SPEC-030). -> TASK-13, TASK-14
8. **S-8 Rights and flag data:** the 37 Reference data rows in `interim-capability-grants.csv`, the 26 list keys and 12 definition keys in the catalog, and `rwb.p3.refdata-versions` in both YAML files (SPEC-018, SPEC-027, SPEC-029). -> TASK-04, TASK-06, TASK-14
9. **S-9 Boundary:** `refdata.api` in the module map, the three `RecoveryBoundaryTest` rules, the published-surface sets and the fixture negative case (SPEC-019). -> TASK-05, TASK-06
10. **S-10 Unit tests and coverage:** the red/green pairs, the combined 80% bundle and the unit gate (SPEC-001..032). -> TASK-07..TASK-16
11. **S-11 System, security, flag and migration suites:** `ReferenceLoadIT`, `ReferenceLifecycleIT`, `ReferenceReadIT`, `ReferenceSecurityIT`, `ReferenceFlagIT`, `ReferenceMigrationIT` and the test handlers/fixtures (SPEC-001..032; TC-E1-043-01..11, SEC-01..17). -> TASK-15, TASK-17
12. **S-12 Merge, scope and evidence:** `./scripts/dev.ps1 test`, `./scripts/dev.ps1 it`, the scope/guardrail/evidence check, the unit results table and the open items (SPEC-017, SPEC-019, SPEC-028). -> TASK-18, TASK-19

Out of scope (each a named seam owned by a later story, D-RUN-08; none is built here): `/verify` (GAP-11); `GET /admin/lists/{listCode}` and its HTTP read (GAP-34, open item); the content of the 12 reference tables and their column definitions (RWB-E1-038, -019, -025, -045, -046, Legal; PRODUCT, REGION and EXPOSURE_BAND have no named owner, GAP-43); the `sys_fields` handler and the runtime `is_personal` protection (RWB-E1-064, open item RW-COMPLY); the QUEUE/QUEUE_MEMBER handlers and `QueueVersionApplier` (RWB-E1-019); the real `BusinessDateProvider` over `v_ace_batch_status` (the story after RWB-E1-069, A-01); the persistent decision log (RWB-E1-027) and access log (RWB-E1-039); the permission matrix (RWB-E1-037); the actor/session identity (RWB-E1-022); the admin screens SCR-39, SCR-40 and SCR-42 (Epic 8); rule packages and rule tables (RWB-E1-072, -073); the change checklist and audit report (RWB-E2-041); the daily data quality report (RWB-E1-011); the message table (GAP-06). The two operations not built are recorded in `contracts/backend-apis.json` `notBuiltHere`.

## One-module check (D-RUN-21)

`AGENTS.md` sections 7 and 9 ask that a plan "touches one module". Build decision D-RUN-21 (`AI-SDLC-BUILD-LOG.md` decisions table, 18 Nov 2026 05:36, orchestrator Claude Code; ratification tracked as OPEN-050, owner the recovery tech lead) settles the reading: **"touches one module" means the ACE module, the recovery module.**

| Check | Result |
|---|---|
| ACE module touched | `recovery` only - every main and test class is under `th.co.scb.ace.demo.recovery` |
| Nested design modules touched | P3 `casewf.refdata` (main and published `casewf.refdata.api`); P4 `access.api` and `access.internal` (the LOV read interface, the five SPI types and the interim `LovValueReader`), additive only; P3 `casewf.config` is consumed through its published `casewf.config.api` only |
| Other ACE modules | None. No `common`, `collection`, `platform`, `rules`, `workflow` or `documents` package is created, read or referenced; the packages TE-001 deletes are not named in a new file |
| Non-Java files touched | `backend/src/main/resources/config/parameter-catalog.csv` (38 rows), `backend/src/main/resources/access/interim-capability-grants.csv` (37 rows), `backend/src/main/resources/application.yaml`, `backend/src/main/resources/application-local.yaml`, one migration under `backend/src/main/resources/db/modulemigration/recovery/`, the test resource `backend/src/test/resources/architecture/recovery-modules.yaml` (one entry) and the `backend/src/test/resources/reference-loads/` fixture corpus |
| Shared build file | `backend/build.gradle.kts` is **not** changed: this story adds no dependency, no Gradle task and no new tooling package; the combined JaCoCo bundle already takes every main recovery class plus the TE-001, E1-044 and E1-042 tooling packages, and `RecoveryBoundaryTest` is a test class excluded by `**/*Test.class` |
| Verdict | **PASS - one module (recovery).** The P3 + P4 plan does not go back to the analyst under AGENTS section 7, and it changes neither the common nor the collection module. D-RUN-21 is not ratified; no tech-lead approval is claimed |

Module-boundary evidence: `RecoveryBoundaryTest` and `ModulithTest` stay green (TASK-06, TASK-16) with `refdata.api` published; no P4 type refers to a P3 type; no P1, P2 or P4 to P3 edge is added (SPEC-019, TC-BD-01).

## Frontend Plan

**NOT_APPLICABLE.** UI In Scope NO. Story v7 section 15: "No screen in this story"; SCR-39, SCR-40 and SCR-42 are Epic 8 (story v7 section 19; spec section 19). The three endpoints are backend-only and called by HTTP clients; `contracts/frontend-integrations.json` records the N/A with this evidence. No file under `frontend/` is added or changed, so no frontend unit-test, coverage, component-inventory or functional-automation task exists. `plan/frontend/components.md` is **not written**. `npm run check` still runs in the merge gate (TASK-18) to prove the frontend did not regress; the OpenAPI file and `frontend/src/api/schema.d.ts` are not regenerated.

## Backend Plan

Surface status: **CHANGED**. Unit tests **REQUIRED** (trace SPEC-001..032; gate per "Unit test applicability"). All paths are exact; `R` = `backend/src/main/java/th/co/scb/ace/demo/recovery`, `T` = `backend/src/test/java/th/co/scb/ace/demo/recovery`, `M` = `backend/src/main/resources`, `TR` = `backend/src/test/resources`.

### Files added - main, P3 `casewf.refdata`

| Kind | Path | Content | Task | SPEC |
|---|---|---|---|---|
| Add | `R/casewf/refdata/package-info.java` | `@ApplicationModule` for the P3 sub-package | TASK-06 | 019 |
| Add | `R/casewf/refdata/api/package-info.java` | `@NamedInterface(name = "refdata.api", propagate = false)` | TASK-06 | 019 |
| Add | `R/casewf/refdata/internal/package-info.java` | Internal marker for the P3 sub-package; no named interface | TASK-06 | 019 |
| Add | `R/casewf/refdata/api/ReferenceVersionRegistry.java` | `recordVersion`, `approve`, `rollback`, `versionByLoadId` | TASK-06 | 024 |
| Add | `R/casewf/refdata/api/ReferenceDataService.java` | `rows`, `versionInForce`, `versions` (story v7 section 12) | TASK-06 | 011 |
| Add | `R/casewf/refdata/api/ReferenceDataReaders.java` | `forReader(String readerName)`, `enabled()` | TASK-06 | 014 |
| Add | `R/casewf/refdata/api/ReferenceVersion.java` | Record: id, tableCode, versionNo, validFrom, validTo, status, authorUserId, approverUserId, approvedAt, rowCount, contentHash, plus the additive `rollbackReason` (PG-E1-043-01) | TASK-06 | 011 |
| Add | `R/casewf/refdata/api/VersionedRows.java` | Record: tableCode, versionNo, validFrom, rows | TASK-06 | 011 |
| Add | `R/casewf/refdata/api/NoVersionInForceException.java` | Unchecked; `(String tableCode, LocalDate businessDate)`; message holds the table and date only | TASK-06 | 012 |
| Add | `R/casewf/refdata/internal/ReferenceVersionRegistryImpl.java` | The published interface implementation: load checks, numbering, hash/idempotency, approve, rollback, `versionByLoadId`; `@Transactional`; `@EnableConfigurationProperties(RefdataSettings.class)` | TASK-12 | 004..010, 024, 025, 032 |
| Add | `R/casewf/refdata/internal/ReferenceDataServiceImpl.java` | Reader-bound `ReferenceDataService`: by-date resolution, cache, reader log, no-version alert | TASK-10 | 011..014 |
| Add | `R/casewf/refdata/internal/ReferenceDataReadersImpl.java` | `ReferenceDataReaders`: name pattern, `forReader`, `enabled()` | TASK-10 | 014 |
| Add | `R/casewf/refdata/internal/ReferenceTableHandlers.java` | Start-up map `tableCode -> access.api.ReferenceTableHandler`; duplicate or `PARAMETER` fails start-up | TASK-08 | 025 |
| Add | `R/casewf/refdata/internal/ReferenceRowCache.java` | `(tableCode, businessDate)` entry, TTL from `refdata.cache.ttl-seconds`, only APPROVED, evict on approve/rollback | TASK-10 | 013 |
| Add | `R/casewf/refdata/internal/ReaderLogGate.java` | Suppresses a repeated `(reader, table, version, businessDate)` line within one cache TTL | TASK-10 | 014 |
| Add | `R/casewf/refdata/internal/ReferenceVersionLogger.java` | One INFO `event=REFERENCE_READ` line per read; one ERROR `event=REFERENCE_READ_FAILED` line and the counter when no version is in force | TASK-10 | 012, 014 |
| Add | `R/casewf/refdata/internal/ReferenceTableColumns.java` | Reads `refdata.columns.<code>` through `ParameterService`; parses `name:TYPE[:R][:K]`; `none` means no definition | TASK-08 | 002, 003, 029 |
| Add | `R/casewf/refdata/internal/ReferenceRowCheck.java` | Required, type, unknown column, row-key, length and duplicate checks; typed values; nested `Column`/`PreparedRow`/`PreparedRows`/`Failure` | TASK-08 | 003 |
| Add | `R/casewf/refdata/internal/ContentHasher.java` | Canonical row JSON sorted by `row_key`, lower-case hex SHA-256 | TASK-08 | 006 |
| Add | `R/casewf/refdata/internal/RefdataSettings.java` | Package-private `@ConfigurationProperties(prefix = "rwb.p3")` record `(boolean refdataVersions)`; default false | TASK-10 | 018 |
| Add | `R/casewf/refdata/internal/ReferenceDecisionRecorder.java` | Package-private port `recorded(String decisionCode, String table, UUID loadId, LocalDate validFrom, UUID approverUserId)`, `@Transactional(propagation = MANDATORY)` | TASK-12 | 008 |
| Add | `R/casewf/refdata/internal/LoggingReferenceDecisionRecorder.java` | One INFO `event=DECISION_RECORDED` line, no user ID | TASK-12 | 008 |
| Add | `R/casewf/refdata/internal/ReferenceLoadAudit.java` | Package-private port with `Event(operation, table, loadId, right, outcome, messageCode, traceId, changes)` | TASK-12 | 028 |
| Add | `R/casewf/refdata/internal/LoggingReferenceLoadAudit.java` | One `event=REFERENCE_LOAD_AUDIT` line per load, approve and rollback, DONE and REFUSED; no user ID, row content or reason | TASK-12 | 028 |
| Add | `R/casewf/refdata/internal/ReferenceLoadController.java` | `POST /api/recovery/v1/admin/reference-loads`, `.../{loadId}/approve`, `.../{loadId}/rollback`; multipart; `@PreAuthorize`; `@ConditionalOnExpression`; 201/200; 4xx audit; `Idempotency-Key` accepted | TASK-14 | 015, 016, 018, 020, 024, 028 |
| Add | `R/casewf/refdata/internal/ReferenceLoadDispatcher.java` | Load by `table`, approve/rollback by `loadId`; `PARAMETER` to the branch; registry otherwise; 404 for an off branch; `@ConditionalOnExpression` | TASK-14 | 018, 030 |
| Add | `R/casewf/refdata/internal/ParameterLoadBranch.java` | `ObjectProvider<ParameterLoadHandler>`; `load`, `approve`, `rollback`, `find`; `rwb.refload.*` key guard; 404 when the bean is absent; no `access.api` type | TASK-14 | 026, 030 |
| Add | `R/casewf/refdata/internal/ActorIdResolver.java` | `oid` when a UUID, else `sub` when a UUID, else 401 `ApiError.NO_ROLE` | TASK-14 | 015, 016, 024 |
| Add | `R/casewf/refdata/internal/ReferenceLoadFileReader.java` | CSV RFC 4180 UTF-8 and XLSX first sheet to `access.api.ReferenceLoadFile`; header, short/long row, BOM, zero-byte; a key-column reader for the PARAMETER guard | TASK-08 | 015, 026 |
| Add | `R/casewf/refdata/internal/ReferenceLoadAuthority.java` | Bean `referenceLoadAuthority`: area C/A/U through `CapabilityCheck.require`; per-table loader/approver list; unknown load passes the table right; 403 with the action text; REFUSED audit | TASK-14 | 027 |
| Add | `R/casewf/refdata/internal/ReferenceLoadView.java` | Package-private response record `(UUID id, String table, LocalDate validFrom, String status, int rows)` matching API v4 `ReferenceLoad` | TASK-14 | 015, 016, 024 |
| Add | `R/casewf/refdata/internal/RollbackRequest.java` | Package-private record `(String reason)` matching API v4 `RollbackRequest` | TASK-14 | 024 |
| Add | `R/casewf/refdata/internal/ReferenceVersionEntity.java` | JPA entity for `reference_version`; `@Version` on `version`; `rollbackReason`; no schema literal | TASK-12 | 001, 007, 008, 024 |
| Add | `R/casewf/refdata/internal/ReferenceRowEntity.java` | JPA entity for `reference_row`; `row_data` as `Map<String,Object>` with `@JdbcTypeCode(SqlTypes.JSON)` | TASK-12 | 001, 007 |
| Add | `R/casewf/refdata/internal/ReferenceVersionRepository.java` | JPA repository: by loadId, by table, approved windows, max version, advisory lock, valid_to recompute reads | TASK-12 | 007..011, 024 |
| Add | `R/casewf/refdata/internal/ReferenceRowRepository.java` | JPA repository: rows by version id ordered by `row_key` | TASK-12 | 007, 011 |

### Files added or changed - main, P4 `access` `[TE-001]`

| Kind | Path | Content | Task | SPEC |
|---|---|---|---|---|
| Add | `R/access/api/ListOfValuesReader.java` | `Set<String> activeCodes(String lovCode)` | TASK-06 | 002, 019 |
| Add | `R/access/api/ReferenceTableHandler.java` | The SPI of SPEC-025: `tableCode`, `validate`, `apply`, `keyColumns`, `repeatMessage`, `supportsRollback`, `onRolledBack`, `changeSummary`, `dating`, nested `enum Dating` | TASK-06 | 025 |
| Add | `R/access/api/ReferenceLoadFile.java` | Record `(String tableCode, LocalDate validFrom, List<String> columns, List<Map<String, Object>> rows)` | TASK-06 | 025 |
| Add | `R/access/api/HandlerMessage.java` | Record `(String messageCode, Map<String, String> placeholders)` | TASK-06 | 025 |
| Add | `R/access/api/ValidationReport.java` | Record `(List<RowCheckFailure> failures)` with `ok()` | TASK-06 | 025 |
| Add | `R/access/api/RowCheckFailure.java` | Record `(int row, String column, String messageCode, Map<String, String> placeholders)`; row 0 is file level | TASK-06 | 025 |
| Add | `R/access/internal/LovValueReader.java` | Interim `ListOfValuesReader`; `JdbcTemplate` reads `lov_value` by `lov_code` and `is_active`; no other table | TASK-06 | 002, 019 |

### Files added or changed - resources and migration

| Kind | Path | Content | Task | SPEC |
|---|---|---|---|---|
| Add | `M/db/modulemigration/recovery/V<seq>__rwb_e1_043_reference_versions.sql` | Line 1 `-- Story: RWB-E1-043`; line 2 a header comment; the guarded DDL, constraints, indexes, triggers and the 38 catalog rows of `data-model.md` sections 1 and 7 | TASK-02 | 001, 029 |
| Edit | `M/config/parameter-catalog.csv` `[E1-042]` | Add the 38 rows of `data-model.md` section 7 after the 19 E1-042 rows; no existing row changes | TASK-04 | 029 |
| Edit | `M/access/interim-capability-grants.csv` `[E1-042]` | Add one `role,Reference data,rights` row per RW- role (37 rows) from `data-model.md` section 8; no `Rules and parameters` row changes | TASK-14 | 027 |
| Edit | `M/application.yaml` | `rwb.p3.refdata-versions: ${RWB_P3_REFDATA_VERSIONS:false}` | TASK-14 | 018 |
| Edit | `M/application-local.yaml` | `rwb.p3.refdata-versions: ${RWB_P3_REFDATA_VERSIONS:true}` | TASK-14 | 018 |

### Files added or changed - test scope

| Kind | Path | Content | Task | SPEC |
|---|---|---|---|---|
| Add | `T/casewf/refdata/ReferenceMigrationIT.java` | TC-MG-01, TC-CAT-01 migration part: empty schema, PS6 baseline, re-run, every column/constraint/index/trigger, negatives, 38 rows | TASK-01, TASK-15 | 001, 029 |
| Add | `T/casewf/refdata/ReferenceLoadIT.java` | TC-E1-043-02, -04, -06, -07, -10, -11, TC-BR1, TC-HD-01, -03, -05, TC-PB-01, -02, TC-RP-01, TC-FD-01, SEC-02, -05, -06, -11, -15, -16 | TASK-15 | 002..006, 015, 020, 025..030 |
| Add | `T/casewf/refdata/ReferenceLifecycleIT.java` | TC-E1-043-01, -05, -08, -09, TC-RB-01, -02, TC-HD-04, TC-TM-01..05, TC-DR-01, SEC-03, -04, -07, -08, -09, -10, -12, -13, -14, -17 | TASK-15 | 004..010, 024, 025, 028, 031, 032 |
| Add | `T/casewf/refdata/ReferenceReadIT.java` | TC-E1-043-03, -09; read by date, cache, log gate, counter, versions | TASK-15 | 011..014 |
| Add | `T/casewf/refdata/ReferenceSecurityIT.java` | SEC-01 reflection and SEC-02..17 at endpoint level; the action text of every 403 | TASK-15 | 015, 016, 024, 027, 028 |
| Add | `T/casewf/refdata/ReferenceFlagIT.java` | TC-FL-01: four flag combinations, read beans, write refusal, branch 404 | TASK-15 | 018 |
| Add | `T/casewf/refdata/ReferenceTestData.java` | Synthetic UUIDs, JWT builders, fixed business date, JDBC inserts for synthetic handler list keys, test tables; no personal data | TASK-15 | 023, 027 |
| Add | `T/casewf/refdata/ReferenceTestClock.java` | Mutable `Clock` for the cache TTL and reader-log gate unit tests; no Spring context | TASK-09, TASK-10 | 013, 014 |
| Add | `T/casewf/refdata/ReferenceTestHandlers.java` | Test `@TestConfiguration` handlers: `test_table`, `test_dictionary`, `test_current`, `test_current_2`, `data_product`, dated test handler | TASK-15 | 025, 031, 032 |
| Add | `T/casewf/refdata/internal/ReferenceTableHandlersTest.java` | TC-HD-02; handler lookup | TASK-07 | 025 |
| Add | `T/casewf/refdata/internal/ReferenceTableColumnsTest.java` | Grammar, `none`, unknown key, malformed definition | TASK-07 | 002, 003 |
| Add | `T/casewf/refdata/internal/ReferenceRowCheckTest.java` | Required, type, unknown, duplicate, detail cap, row key | TASK-07 | 003 |
| Add | `T/casewf/refdata/internal/ContentHasherTest.java` | Canonical form, sorted keys, normalisation, unparseable text | TASK-07 | 006 |
| Add | `T/casewf/refdata/internal/ReferenceLoadFileReaderTest.java` | CSV quoting, BOM, short/long rows, header-only, zero-byte, XLSX first sheet | TASK-07 | 015 |
| Add | `T/casewf/refdata/internal/ReferenceRowCacheTest.java` | Only APPROVED, TTL, evict, exception not cached | TASK-09 | 013 |
| Add | `T/casewf/refdata/internal/ReaderLogGateTest.java` | Repeat within TTL suppressed, new after expiry | TASK-09 | 014 |
| Add | `T/casewf/refdata/internal/ReferenceVersionLoggerTest.java` | One line per read, no user ID or row content, ERROR and counter on no version | TASK-09 | 012, 014 |
| Add | `T/casewf/refdata/internal/ReferenceDataServiceImplTest.java` | Version by date, statuses never served, `versions` newest first with `rollbackReason` | TASK-09 | 011, 032 |
| Add | `T/casewf/refdata/internal/ReferenceDataReadersImplTest.java` | Name pattern, invalid name, `enabled()` | TASK-09 | 014, 018 |
| Add | `T/casewf/refdata/internal/ReferenceVersionRegistryTest.java` | Numbering, repeat, early repeat, approve checks, current-state, `valid_to`, rollback rules, recorder failure, handler calls, flag off | TASK-11 | 004..010, 024, 025, 032 |
| Add | `T/casewf/refdata/internal/ReferenceDecisionRecorderTest.java` | MANDATORY propagation; one line, no user ID | TASK-11 | 008 |
| Add | `T/casewf/refdata/internal/ReferenceLoadAuditTest.java` | Line fields, DONE/REFUSED, no user ID or content | TASK-11 | 028 |
| Add | `T/casewf/refdata/internal/StubTransactionManager.java` | Test-scope `AbstractPlatformTransactionManager` with no resource, so a real `TransactionTemplate` runs | TASK-11 | 008 |
| Add | `T/casewf/refdata/internal/ReferenceLoadAuthorityTest.java` | Area and table rights, unknown load, list key missing/empty, 403 form and action, audit | TASK-13 | 027 |
| Add | `T/casewf/refdata/internal/ReferenceLoadDispatcherTest.java` | PARAMETER, handler and built-in routing, 404, missing params | TASK-13 | 018, 030 |
| Add | `T/casewf/refdata/internal/ParameterLoadBranchTest.java` | Load/approve/rollback to the handler, absent bean 404, pass-through, `rwb.refload.*` guard | TASK-13 | 026, 030 |
| Add | `T/casewf/refdata/internal/ActorIdResolverTest.java` | `oid` first, `sub` second, neither 401 | TASK-13 | 015, 016, 024 |
| Add | `T/casewf/refdata/internal/ReferenceLoadControllerTest.java` | MVC slice: 201/200, body shape, 422, 404, 409, 503; no filters | TASK-13 | 015, 016, 020, 024 |
| Add | `T/architecture/parameters/ReferenceCatalogRowsTest.java` | 57 rows, 38 new keys and metadata, 19 unchanged, no duplicate, descriptions | TASK-03 | 029 |
| Add | `T/recoveryfixture/access/AccessFixture.java` | Test-scope fixture importing `casewf.refdata.api` to prove the access-to-casewf rule fires | TASK-05 | 019 |
| Add | `T/recoveryfixture/dataengine/DataEngineFixture.java` | Test-scope fixture importing `casewf.refdata.api` to prove the dataengine-to-casewf rule fires | TASK-05 | 019 |
| Edit | `T/architecture/RecoveryBoundaryTest.java` `[TE-001]` | `publishedSurfaceIsExactlyTheSpecifiedTypes` extended; `refdataApiIsNamed`; the three rules; the fixture negative test | TASK-05 | 019 |
| Edit | `TR/architecture/recovery-modules.yaml` `[TE-001]` | Add `refdata.api` to the `casewf` `published` list; nothing else | TASK-05 | 019 |
| Add | `TR/reference-loads/` | CSV fixtures: `region.csv`, `exposure-band.csv`, `service-level-bad-row.csv`, `header-only.csv`, `quoted.csv`, `short-row.csv`, `parameter-definition.csv`, `parameter-load.csv`, `parameter-guarded.csv`, `empty.csv`; XLSX built at test runtime | TASK-07, TASK-15 | 003, 006, 015 |

### Files explicitly not changed

`backend/build.gradle.kts` (no dependency, task or coverage-filter edit; TASK-00 confirms); `api/recovery-api-v4.yaml`; every file under `frontend/`; `scripts/dev.ps1`; `.gitlab-ci.yml`; `docker-compose.yml`; `backend/Dockerfile`; `infra/**`; `[TE-001] T/architecture/RecoveryMigrationLintTest.java` (the migration must pass it as merged); `[TE-001] T/RecoveryDatabaseIT.java`; `T/.../e2e/PlatformE2ETest.java`; `T/.../ModulithTest.java`; `[TE-001] T/testsupport/ApplicationYamlEnvironment.java`; `[E1-042] R/casewf/config/ParameterLoadHandlerImpl.java`, `ParameterCatalogController.java`, `FixedMessageCatalog.java`, `InterimCapabilityCheck.java`; `[E1-042] R/access/internal/ApiExceptionHandler.java`, `ProblemFactory.java` (no change beyond E1-042); `[E1-042] R/access/api/ApiProblemException.java`.

## Migration

One migration: `backend/src/main/resources/db/modulemigration/recovery/V<seq>__rwb_e1_043_reference_versions.sql`. **No number is fixed** (D-RUN-07); the orchestrator assigns `<seq>` at merge as the next four-digit number in merge order (D-RCV-28), and the lint requires a contiguous sequence from `V0001`. Line 1 is `-- Story: RWB-E1-043`; line 2 is a header comment citing Physical Schema v6, D-RCV-28 and this spec. The file is the only non-fix file for this story. It is forward only and is never edited after merge; a later correction takes the next sequence, keeps the key and adds line 2 `-- Fix: <reason>`.

The file has eight statement groups, in order (`data-model.md` sections 1 to 6):

1. `CREATE TABLE IF NOT EXISTS ${recoverySchema}.reference_version` with the 29 Physical Schema v6 columns and `uk_reference_version (table_code, version_no)`.
2. `CREATE TABLE IF NOT EXISTS ${recoverySchema}.reference_row` with the 11 Physical Schema v6 columns and no `uk_reference_row` (the old global key makes AC1 impossible, GAP-01).
3. `ALTER TABLE ${recoverySchema}.reference_row DROP CONSTRAINT IF EXISTS uk_reference_row` and `ALTER TABLE ${recoverySchema}.reference_version DROP CONSTRAINT IF EXISTS uk_reference_version_from_hash` (the second is a no-op unless a partial run left it); a guarded `DO` block adds `uk_reference_row_version (version_id, row_key)`.
4. Guarded `DO` blocks add, by name, `uk_reference_version_from_hash (table_code, valid_from, content_hash)`, `ck_reference_version_maker_checker`, `ck_reference_version_rollback_reason` and `fk_reference_row_version_id`; `CREATE UNIQUE INDEX IF NOT EXISTS ux_reference_version_approved_from` on `(table_code, valid_from) WHERE status = 'APPROVED'`; `CREATE INDEX IF NOT EXISTS ix_reference_version_load_id`; `CREATE INDEX IF NOT EXISTS ix_reference_row_version_id`.
5. `CREATE OR REPLACE FUNCTION ${recoverySchema}.reference_version_append_only()` and `reference_row_append_only()`; `DROP TRIGGER IF EXISTS` then `CREATE TRIGGER` on each table (`BEFORE UPDATE OR DELETE`).
6. `INSERT INTO ${recoverySchema}.parameter_catalog (...) VALUES (...) ON CONFLICT (param_key) DO NOTHING` for the 38 rows of `data-model.md` section 7; **no** `parameter_value` row.
7. `COMMENT ON TABLE`/`COMMENT ON COLUMN` only where it adds the story's meaning; no literal schema.
8. A `DO` self-check that the 38 keys exist and every `rwb.refload.loader.*`/`rwb.refload.approver.*` row is `CODE_LIST`, `required=false`, owner `RW-RISK`; raises otherwise.

No `CREATE SCHEMA`, `CREATE ROLE`, `GRANT`, `REVOKE` or `SET search_path`; no `R__` file; `${recoverySchema}` is the only qualifier. The catalog `used_by` and `description` strings contain `recovery.casewf.refdata`; that is why E1-044's identifier-only, quote-aware lint is required (PRE-2; T-044-21). The file seeds no row in `reference_version` or `reference_row` and no `lov_value`.

## Rule tables and reference sources read

`AGENTS.md` section 3.2 asks that every threshold, limit, timer, queue, role, template and route come from a versioned reference table. This story reads:

| Source (name, version) | What it supplies | Applied in |
|---|---|---|
| Story file v7 RWB-E1-043 v2, sections 7, 8, 9, 12, 13, 16, 17 | AC1-AC10, BR1-BR9, the three operations, the package, the build steps, the 11 test cases, the guardrails | Whole plan |
| Physical Schema v6, lines 1437-1483 (`reference_version`, `reference_row`), 2228-2249 (FKs), 2334-2347 (indexes), 3179-3204 (column comments), 3595-3596 (`sys_objects`), 4348-4373 (`sys_fields` DF-REF-159..184) | Every table and column, the old row key, the FK and index names, the dictionary rows | SPEC-001; `data-model.md` sections 3-4; TASK-02 |
| Decision Log v10, D-RCV-28 (migration name, `<seq>` at merge, line 1 story key, `${recoverySchema}`, no GRANT/REVOKE) | The migration convention | SPEC-001; TASK-02 |
| API Specification v4.0.0, `postAdminReferenceLoads` (3167), approve (3214), rollback (5004), `ReferenceLoad` (8832), `RollbackRequest` (9818), `Problem`, E401/E403/E422/E503 | Routes, request fields, response fields, error set | SPEC-015, 016, 024; `contracts/backend-apis.json`; TASK-14 |
| Error and Message Standard v4, lines 68, 71, 139, 151, 163, 164, 207, 208 | `MSG-GEN-001`, `MSG-GEN-004`, `MSG-P3-015`, `MSG-P3-027`, `MSG-P4-002`, `MSG-P7-002`, `MSG-P7-003` and their text | SPEC-020; TASK-14 |
| Users, Roles and Permissions v4, matrix lines 73-110 (Reference data column) | The per-role Reference data rights; the six A roles of A-08 | SPEC-027; `data-model.md` section 8; TASK-14 |
| Physical Schema v6 LOV-REF-TABLE seed (lines 5125-5149) and `lov_value` | The 12 built-in codes and the rule/HOLIDAY codes the service refuses (GAP-04) | SPEC-002, 021; TASK-06, TASK-08 |
| Data Dictionary v8 DF-REF-159..184, DF-REF-028/029, DF-REF-163/164, DF-WRK-038/051/052 | Field names, types and the dated/current-state reading | SPEC-001, 011, 032; `data-model.md` |
| RWB-E1-042 spec revision 13, sections 10.1, 10.2, 12.2, 12.4, 12.7, 12.10, 12.12, 12.14 T-2 and R7-1; RWB-E1-042 plan v2 `data-model.md` sections 2, 4, 7, 9 | The consumed interfaces, the message IDs, `parameter_catalog`/`parameter_value`, the grants file, the catalog file, the nine message IDs, `ParameterKeys.byName`, the TTL key | SPEC-003, 013, 017, 020, 026, 027, 029; TASK-06, TASK-08, TASK-10, TASK-12, TASK-14 |
| RWB-TE-001 plan v7, `tasks.md`, `data-model.md`; RWB-E1-044 plan v2, `tasks.md`, `data-model.md` | Module homes, module map, coverage bundle, `ApplicationYamlEnvironment`, migration lint and Flyway runner | TASK-00, TASK-05, TASK-06, TASK-16 |
| Build log decisions D-RUN-07, D-RUN-08, D-RUN-10, D-RUN-11, D-RUN-12, D-RUN-18, D-RUN-19, D-RUN-20, D-RUN-21 (orchestrator, not ratified; OPEN-050) | Migration numbering, seams, shared endpoint, handler registry, one file per table, SPI in P4, parameter reads, `PARAMETER` branch, one-module reading | Whole plan |
| `AGENTS.md` v2, sections 2-4, 7, 9 | One migration per story, no literal business value, method check on every endpoint, decision record, module boundaries, one-module rule | Whole plan |
| Testing standards v2.0, sections 1-6; implementation gates | Levels, `recovery-it`, synthetic data, coverage rules, evidence | TASK-15..TASK-19 |

No business value, role or threshold is written as a literal in Java: the table codes come from `lov_value` and the handler beans, the column definitions and the loader/approver lists from `parameter_catalog`, the TTL from `parameter_catalog`, the flag from `application.yaml`, and the roles from the grants file. The three route paths are the API Specification v4 paths, written in the controller as the existing controllers write theirs; API v4 is the source of record for routes and no reference table for routes exists (the A-06 split).

## Unit test applicability

| Surface | Changes | Unit tests | Coverage gate | Trace | Evidence and rationale |
|---|---|---|---|---|---|
| Frontend | NO | NOT_APPLICABLE | NOT_APPLICABLE | Story section 15; spec section 19 | No screen, no route, no client call; no file under `frontend/`; the OpenAPI file and `schema.d.ts` are unchanged |
| Backend | YES | REQUIRED | `recoveryCoverageVerification`: one `BUNDLE` rule, `LINE`, `INSTRUCTION`, `BRANCH`, `METHOD` each 0.80 over the TE-001 combined bundle plus `architecture/parameters` (E1-042) and `architecture/migration` (E1-044); this story adds no tooling package and no build-file edit (TASK-00 confirms) | SPEC-001..032 | New service, registry, controller, dispatcher, branch, authority, audit, recorder, cache, logger, checks, hasher, file reader, entities, repositories and migration. Unit tests in `test` for every class; the `recovery-it` classes do not count toward the gate |

No measured coverage is claimed here. TASK-16 runs the gate and reports the four counters; a counter below 0.80 is a blocker, never an exclusion or a lowered threshold.

## Execution order (tests before code, AGENTS.md rules 3 and 10)

1. TASK-00 pre-flight on the merged TE-001, E1-044 and E1-042 base; baseline counters; `check --dry-run`.
2. Red first: TASK-01 (migration IT fails on missing tables), TASK-03 (catalog rows absent), TASK-05 (published surface absent), TASK-07 (domain classes absent), TASK-09 (read classes absent), TASK-11 (registry classes absent), TASK-13 (HTTP classes absent).
3. Green, in order: TASK-02 (migration), TASK-04 (catalog), TASK-06 (published surface), TASK-08 (domain), TASK-10 (read), TASK-12 (registry), TASK-14 (HTTP and flag).
4. TASK-15 writes and runs the System, security and flag suites; a red case is fixed in the owning green task, never by weakening the assertion.
5. Verification: TASK-16 (unit suite and coverage gate), TASK-17 (container suite), TASK-18 (merge gate), TASK-19 (scope, guardrail and evidence).

Every red run and every green run is saved under `implement/` as command, exit code and the first failing assertion or the final summary line. TASK-01 is red at runtime (missing tables); the other red tasks are red by compile or assertion and run directly before their green task so the test source set compiles again before the next task.

## Functional Test Scenarios

| ID | Scenario | Owner | Assignment | Evidence |
|---|---|---|---|---|
| FTS-E1043-01 | A RW-REFADM loads a REGION file (201 VALIDATED), a RW-RISK user approves it (200 APPROVED), the same RW-REFADM rolls it back with a reason (200 ROLLED_BACK); a second identical load returns the same body; a role without the right gets 403 `MSG-P4-002` with the action text; an empty file gets 422 `MSG-GEN-001` `rows` | API Tester | **ASSIGNED** - the three admin operations are the only HTTP surface; run against the local stack with `api-tests/` evidence | `api-tests/` report with each status, `messageCode`, `field` and the audit line; compare with TC-E1-043-02, -07, -10, TC-RB-01 and SEC-05 |
| FTS-E1043-02 | An operator loads one of the 12 reference tables and approves it; the version in force changes only from its `validFrom`; a row failure refuses the whole file; the version log and audit lines name the table and version | Functional Automation Test | **NOT_APPLICABLE** - no UI or screen; the same checks are executed by `ReferenceLoadIT` and `ReferenceLifecycleIT` (`recovery-it`), which is not a functional-automation result | `implement/backend/it.log`; JUnit XML |
| FTS-E1043-03 | Two consumers read two tables on start and each writes one line per table; a table with no version in force stops the run and raises one ERROR line and the counter | Functional Automation Test | **NOT_APPLICABLE** - no HTTP or UI surface for the read path; executed by `ReferenceReadIT` | `implement/backend/it.log` |
| FTS-E1043-04 | Any UI journey | Functional Automation Test | **NOT_APPLICABLE** - UI In Scope NO; SCR-39/40/42 are Epic 8 | - |
| HV-E1043-01 | The 12 reference tables each have version 1 approved in SIT, with content and definitions from their owning stories | Human (QA lead and table owners) | **BLOCKED by later stories** (RWB-E1-038, -019, -025, -045, -046, Legal; PRODUCT/REGION/EXPOSURE_BAND unowned, GAP-43); never reported as tested | `shared-updates.md` R10; GAP-43 |
| HV-E1043-02 | A real RW- identity and the matrix from RWB-E1-022/RWB-E1-037 confirm the 403 refusal and the action text in SIT | Human (QA lead, access owner) | **BLOCKED by later stories**; the interim grants file and `ActorIdResolver` are the seam | R8, R9; A-07, A-08 |
| HV-E1043-03 | The `sys_fields` handler protects `is_personal` against a load and a rollback | Human (RW-COMPLY, RWB-E1-064 owner) | **BLOCKED by RWB-E1-064**; this story builds the registry and generic checks only | R3; A-36; GAP-38 |
| HV-E1043-04 | The recovery tech lead ratifies D-RUN-18, D-RUN-19, D-RUN-20 and D-RUN-21 | Human (recovery tech lead) | **OPEN**, not tested; OPEN-050 | `shared-updates.md` R24; OPEN-050 |
| HV-E1043-05 | The API owner retags the three operations from P4 to P3 (GAP-53) and adds the 404/500 rows of GAP-48 | Human (API owner) | **OPEN**, not tested | GAP-48, GAP-53; `shared-updates.md` R18 |

No functional-automation journey exists because the story adds no screen; this is recorded as `NOT_APPLICABLE` with evidence, not as an executed test. FTS-E1043-01 is the only API-Tester assignment.

## Requirement Logic To Task Coverage

`REQ_REF` values are the 49 rows of `../specify/spec.md` "Requirement-to-SPEC Logic Coverage"; none is merged, dropped or weakened. The 16 lines owned by another story stay in the spec table and are not restated here.

| REQ_REF | Mapped SPEC-* | Mapped TASK-* | Coverage Type | Verification | Status |
|---|---|---|---|---|---|
| S7 BR1; D36 line 145 | 002, 021, 025 | TASK-04, -06, -08, -12, -14 | DIRECT_IMPLEMENTATION | TC-BR1, TC-HD-03, TC-HD-04; `ReferenceTableColumnsTest` | COVERED |
| S7 BR2 | 001, 007 | TASK-02, -12 | DIRECT_IMPLEMENTATION | TC-E1-043-01, -07; `ReferenceVersionRegistryTest#versionNumberIsMaxPlusOne` | COVERED |
| S7 BR3; R-UNI-38 | 011, 032 | TASK-10, -12, -15 | DIRECT_IMPLEMENTATION | TC-E1-043-01, -05; TC-TM-01..05; `ReferenceDataServiceImplTest#versionInForceByDate` | COVERED |
| S7 BR3, BR8, section 9 row 4; S7-019 BR3, AC2, AC9; DD8 DF-REF-163/164 | 010, 011, 024, 025, 032 | TASK-12, -15 | DIRECT_IMPLEMENTATION | TC-E1-043-01; TC-TM-01..05; TC-RB-01 | COVERED |
| S7 BR4; CTL-08 | 008, 001 | TASK-02, -12, -15 | DIRECT_IMPLEMENTATION | TC-E1-043-02; SEC-12; the DB CHECK in TC-MG-01 | COVERED |
| S7 BR5 | 003, 004, 005, 007 | TASK-08, -12, -15 | DIRECT_IMPLEMENTATION | TC-E1-043-04, -10; TC-HD-01; `ReferenceRowCheckTest` | COVERED |
| S7 BR6 sentence 1 | 005 | TASK-12, -15 | DIRECT_IMPLEMENTATION | TC-E1-043-06 | COVERED |
| S7 BR6 sentence 2 (registry part) | 001, 008, 011 | TASK-02, -12, -15 | DIRECT_IMPLEMENTATION | TC-E1-043-01; TC-TM-01; `versions()` returns the earlier version | COVERED |
| S7 BR7; REQ-CWC-016 | 014 | TASK-10, -15 | DIRECT_IMPLEMENTATION | TC-E1-043-03; `ReferenceVersionLoggerTest` | COVERED |
| S7 BR8 | 010 | TASK-12, -15 | DIRECT_IMPLEMENTATION | TC-E1-043-01; TC-TM-02 | COVERED |
| S7 BR9 | 012 | TASK-10, -15 | DIRECT_IMPLEMENTATION | TC-E1-043-09; `ReferenceDataServiceImplTest#noVersionInForceLogsAndCounts` | COVERED |
| S7 X1 / AC2 / AC5 | 008, 011 | TASK-12, -15 | DIRECT_IMPLEMENTATION | TC-E1-043-02, -05; SEC-12 | COVERED |
| S7 X2 / AC4 | 003 | TASK-08, -15 | DIRECT_IMPLEMENTATION | TC-E1-043-04; `ReferenceRowCheckTest#requiredAndTypeFailuresNameRowAndColumn` | COVERED |
| S7 X3 / AC6 | 005 | TASK-12, -15 | DIRECT_IMPLEMENTATION | TC-E1-043-06 | COVERED |
| S7 X4 / AC7 | 006, 025 | TASK-08, -12, -15 | DIRECT_IMPLEMENTATION | TC-E1-043-07; TC-RP-01; `ContentHasherTest` | COVERED |
| S7 X5 / AC8 | 009 | TASK-12, -15 | DIRECT_IMPLEMENTATION | TC-E1-043-08; the optimistic-lock path | COVERED |
| S7 X6 / AC9 | 012 | TASK-10, -15 | DIRECT_IMPLEMENTATION | TC-E1-043-09 | COVERED |
| S7 X7 / AC10 | 004 | TASK-08, -12, -15 | DIRECT_IMPLEMENTATION | TC-E1-043-10 | COVERED |
| S7 AC1 | 007, 010, 011 | TASK-12, -15 | DIRECT_IMPLEMENTATION | TC-E1-043-01; `ReferenceReadIT#versionsAreIndependentAndReadable` | COVERED |
| S7 AC3 | 014, 021 | TASK-10, -15 | DIRECT_IMPLEMENTATION | TC-E1-043-03; two consumers, one line each | COVERED |
| S7 section 9 row 3 | 008 | TASK-12, -15 | DIRECT_IMPLEMENTATION | TC-E1-043-02 | COVERED |
| S7 section 9 row 4; FR-RWB-011 "load/rollback path" | 024 | TASK-12, -15 | DIRECT_IMPLEMENTATION | TC-RB-01, TC-RB-02; TC-TM-03, -04 | COVERED |
| S7 section 10 RW-REFADM, RW-COE | 027 | TASK-04, -14, -15 | DIRECT_IMPLEMENTATION | SEC-05, SEC-06; TC-E1-043-11 | COVERED |
| S7 section 10 RW-RISK; API4 approve | 027 | TASK-04, -14, -15 | DIRECT_IMPLEMENTATION | SEC-07, SEC-08, SEC-17; `ReferenceLoadAuthorityTest` | COVERED |
| S7 sections 11, 17 | 001, 002 | TASK-02, -06, -08 | DIRECT_IMPLEMENTATION | TC-BD-01, TC-BR1; the entities and the LOV read | COVERED |
| S7 section 12 load | 015, 006 | TASK-14, -15 | DIRECT_IMPLEMENTATION | TC-E1-043-02, -04, -06, -07, -10, -11 | COVERED |
| S7 section 12 approve | 016, 008 | TASK-14, -15 | DIRECT_IMPLEMENTATION | TC-E1-043-02, -05, -08 | COVERED |
| S7 section 12 interfaces | 007..012, 024, 025 | TASK-06, -08, -10, -12 | DIRECT_IMPLEMENTATION | TC-BD-01; `ReferenceVersionRegistryTest`; `ReferenceDataServiceImplTest` | COVERED |
| S7 section 13 DB | 001 | TASK-01, -02 | DIRECT_IMPLEMENTATION | TC-MG-01 | COVERED |
| S7 section 13 step 2 | 003, 029 | TASK-04, -08 | DIRECT_IMPLEMENTATION | TC-CAT-01; TC-E1-043-04 | COVERED |
| S7 section 13 cache | 013 | TASK-10 | DIRECT_IMPLEMENTATION | TC-E1-043-03; `ReferenceRowCacheTest` | COVERED |
| S7 section 13 step 6 (logger) | 014 | TASK-10 | DIRECT_IMPLEMENTATION | TC-E1-043-03 | COVERED |
| S7 section 13 step 7; D-RUN-10; D-RUN-11 | 015, 016, 024, 025, 026, 030 | TASK-06, -12, -14, -15 | DIRECT_IMPLEMENTATION | TC-HD-01..05, TC-PB-01, TC-PB-02 | COVERED |
| S7 section 13 flag | 018 | TASK-06, -14, -15 | DIRECT_IMPLEMENTATION | TC-FL-01 | COVERED |
| S7 section 13 done-when (boundary) | 019 | TASK-05, -06 | DIRECT_IMPLEMENTATION | TC-BD-01; `ModulithTest` | COVERED |
| S7 section 14 | 020 | TASK-14, -15 | DIRECT_IMPLEMENTATION | TC-E1-043-11; SEC-05..11; the action text | COVERED |
| S7 section 16 TC-11; TC7 TC-E1-043-11 | 015, 027, 028 | TASK-14, -15 | DIRECT_IMPLEMENTATION | TC-E1-043-11; `ReferenceLoadAuditTest` | COVERED |
| S7 section 17 | 001, 013, 014, 019, 021, 023 | TASK-02, -05, -08, -10, -14, -19 | DIRECT_IMPLEMENTATION | TC-BD-01; TC-E1-043-03; the scope check | COVERED |
| API4 approve "decision log entry AC-VERS" | 008 | TASK-12, -15 | DIRECT_IMPLEMENTATION | TC-DR-01; `ReferenceDecisionRecorderTest` | COVERED |
| REQ FR-RWB-011; REQ-DRI-011 | 001..013, 024 | TASK-02..TASK-14 | DIRECT_IMPLEMENTATION | TC-E1-043-01..11; TC-RB-01, -02 | COVERED |
| REQ-CWC-006 | 002, 007, 025 | TASK-04, -06, -08, -12 | DIRECT_IMPLEMENTATION | TC-BR1, TC-HD-03; the ROLE, TEAM and QUEUE codes | COVERED |
| REQ FR-RWB-012; BS-4.4 | 028 | TASK-14, -15 | DIRECT_IMPLEMENTATION | TC-E1-043-11; SEC-05; the audit line | COVERED |
| REQ NFR-RWB-005 | 015, 016, 024, 027, 028 | TASK-14, -15 | DIRECT_IMPLEMENTATION | SEC-01..17; the 403 action text | COVERED |
| REQ NFR-RWB-006 | 014, 023, 028 | TASK-10, -14, -15 | DIRECT_IMPLEMENTATION | TC-E1-043-03; the audit and logger unit tests | COVERED |
| REQ NFR-RWB-008 | 012, 014, 028 | TASK-10, -14 | DIRECT_IMPLEMENTATION | TC-E1-043-03, -09; the counter and ERROR line | COVERED |
| REQ NFR-RWB-009 | 018 | TASK-06, -14 | DIRECT_IMPLEMENTATION | TC-FL-01 | COVERED |
| AUD A-06 | 013, 018, 027, 029 | TASK-04, -06, -10, -14 | DIRECT_IMPLEMENTATION | TC-CAT-01; TC-FL-01; the no-literal check in TASK-19 | COVERED |
| DL10 D-RCV-29 (registry part) | 025, 027, 028, 031 | TASK-06, -08, -12, -14, -15 | DIRECT_IMPLEMENTATION | TC-HD-04; the `changeSummary` audit; the registry part only | COVERED |
| Existing platform | inherited | TASK-00, -05, -18 | INHERITED_EXISTING_BEHAVIOR | `ModulithTest`, `RecoveryMigrationLintTest`, `SecurityConfig`, `ApiExceptionHandler`; TC-BD-01 | COVERED |

No row is `BLOCKED`. The 16 lines owned by another story are listed in the spec and are not counted here; they are seams, not tasks.

## SPEC to task map

| SPEC | Tasks | Tests |
|---|---|---|
| 001 | TASK-01, -02, -12, -19 | TC-MG-01; TC-E1-043-01 |
| 002 | TASK-06, -08, -12 | TC-BR1; TC-HD-03 |
| 003 | TASK-07, -08 | TC-E1-043-04; `ReferenceTableColumnsTest`; `ReferenceRowCheckTest` |
| 004 | TASK-07, -08, -14 | TC-E1-043-10 |
| 005 | TASK-12, -15 | TC-E1-043-06; `ReferenceVersionRegistryTest` |
| 006 | TASK-08, -12, -15 | TC-E1-043-07; TC-RP-01; `ContentHasherTest` |
| 007 | TASK-12, -15 | TC-E1-043-01; `ReferenceVersionRegistryTest` |
| 008 | TASK-12, -15 | TC-E1-043-02, -05, -08; TC-TM-05; TC-DR-01 |
| 009 | TASK-12, -15 | TC-E1-043-08 |
| 010 | TASK-12, -15 | TC-E1-043-01; TC-TM-02 |
| 011 | TASK-10, -12, -15 | TC-E1-043-01, -05; `ReferenceDataServiceImplTest` |
| 012 | TASK-10, -15 | TC-E1-043-09 |
| 013 | TASK-10, -15 | TC-E1-043-03; `ReferenceRowCacheTest` |
| 014 | TASK-10, -15 | TC-E1-043-03; `ReferenceVersionLoggerTest`; `ReaderLogGateTest` |
| 015 | TASK-14, -15 | TC-E1-043-02, -04, -06, -07, -10, -11; TC-FD-01 |
| 016 | TASK-14, -15 | TC-E1-043-02, -05, -08; SEC-12 |
| 017 | TASK-14, -15 | TC-E1-043-01, -05, -09; TC-PB-02 |
| 018 | TASK-06, -14, -15 | TC-FL-01 |
| 019 | TASK-05, -06, -19 | TC-BD-01; `ModulithTest` |
| 020 | TASK-14, -15 | TC-E1-043-11; SEC-05..11 |
| 021 | TASK-08, -19 | TC-BR1; TC-HD-03; the scope check |
| 022 | TASK-15, -19 | the SIT seam is checked, not built (GAP-43) |
| 023 | TASK-15, -19 | synthetic UUIDs and codes; no personal data in the tests |
| 024 | TASK-12, -15 | TC-RB-01, TC-RB-02; TC-TM-03, -04 |
| 025 | TASK-06, -08, -12, -14 | TC-HD-01..05; TC-RP-01; TC-PB-01 |
| 026 | TASK-14, -15 | TC-PB-01, TC-PB-02; SEC-15 |
| 027 | TASK-04, -14, -15 | SEC-05..11, SEC-17; TC-E1-043-11 |
| 028 | TASK-14, -15 | TC-E1-043-11; `ReferenceLoadAuditTest`; `ReferenceDecisionRecorderTest` |
| 029 | TASK-03, -04, -19 | TC-CAT-01; `ReferenceCatalogRowsTest` |
| 030 | TASK-14, -15 | TC-PB-01, TC-PB-02; TC-HD-01, -05 |
| 031 | TASK-12, -15, -19 | TC-HD-04; the registry part only |
| 032 | TASK-12, -15 | TC-TM-01..05 |

No orphan: every SPEC 001 to 032 has at least one task.

## Screen-to-task mapping

`NOT_APPLICABLE`: UI In Scope NO, `DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0]`, no effective-screen node and no `SCR-*` screen in the spec. `SCR-39`, `SCR-40` and `SCR-42` are Epic 8 and out of scope. No screen consolidation task is required; the pre-submit check in `tasks.md` records this.

## Security, privacy and compliance

- **Authentication and authorisation.** The three operations carry `@PreAuthorize` expressions naming bean `referenceLoadAuthority`, area `Reference data` and right C, A or U (AGENTS section 3.3; BS-3.2). The area right goes through E1-042's `CapabilityCheck.require`; the per-table right reads `rwb.refload.loader.<code>` (load, rollback) or `rwb.refload.approver.<code>` (approve) through `ParameterService`; a missing key or empty value refuses (fail closed). The 403 body is `MSG-P4-002` with `{action}` "load reference data", "approve reference data" or "roll back reference data", not "do this" (A-45; finding 142). SEC-01 is a reflection test over every handler method; SEC-02..17 cover 401, 403, 404, maker-checker and the actor claim.
- **No self-granting.** `ParameterLoadBranch` refuses the whole PARAMETER load with 422 `MSG-P1-002` before calling RWB-E1-042 if any `key` starts with `rwb.refload.`; the lists can change only by a reviewed catalog-file change and the matching migration row until RWB-E1-037 (SPEC-026; A-39; SEC-15).
- **Personal data.** `author_user_id` and `approver_user_id` are staff identifiers, treated as personal by the protective reading (DF-REF-166/167; A-30). They are stored in `reference_version` and returned only by the Java `versions()`/`versionInForce()` reads, never in a log line, audit event, decision line, exception message or HTTP response (the response has no user field). Every test identity is a synthetic UUID; no name, ID number, account number or address appears in code, fixtures, logs or this plan.
- **Secrets.** None. The story stores no secret; the catalog rows are not secret; no credential is in the migration, the CSV files or a log. The `rwb.refload.*` keys cannot be loaded, so a PARAMETER approver cannot widen its own list.
- **Audit.** One `event=REFERENCE_LOAD_AUDIT` line per load, approve and rollback, DONE and REFUSED, with operation, table, loadId, area, right, outcome, messageCode, traceId and the handler `changeSummary` items; no user ID, row content or reason (SPEC-028; BS-4.4; FR-RWB-012). A refusal is not attributable to an actor until RWB-E1-039 (GAP-42; DPO open item). The approval writes `event=DECISION_RECORDED decisionCode=AC-VERS` inside the transaction through the package-private port; a failure rolls the approval back with 503 `MSG-P7-003` (ADR-009; A-43; RWB-E1-027 replaces the adapter).
- **Database access.** Writes go only to `${recoverySchema}` through the recovery Flyway bean; the service reads only `lov_value`, `parameter_catalog`/`parameter_value` through `ParameterService` and its own two tables; no `public` table is read or written (D-RCV-35 U4; ADR-010; BND-6). No `GRANT`/`REVOKE` in the migration. The append-only triggers refuse DELETE on both tables and UPDATE on `reference_row` and on the frozen `reference_version` columns.
- **Observability.** `event=REFERENCE_READ` one line per read window, `event=REFERENCE_READ_FAILED` with `MSG-P3-027` and the counter `rwb.refdata.no_version_in_force` tagged `table` when no version is in force; `event=REFERENCE_LOAD_AUDIT`; `event=DECISION_RECORDED`. No user ID, row content or customer identifier in any line (BS-4.6).
- **PDPA and dictionary.** The `sys_fields` handler and the runtime `is_personal` protection are RWB-E1-064's (open item RW-COMPLY); this story builds the registry and generic checks only and states the requirement in `shared-updates.md` (SPEC-031).
- **KYC/AML, suitability, delegation of authority.** Not applicable: a reference-data version is not a credit decision (spec NFR table; story section 10).

## Release and rollback

- **Release:** backend only, behind `rwb.p3.refdata-versions` (default `false`, `true` in the local profile; `RWB_P3_REFDATA_VERSIONS` in the environment). The controller and dispatcher are mapped when `rwb.p3.refdata-versions` or `rwb.p3.configservice` is on; a request to a branch whose flag is off gets 404 `MSG-P4-003`. The read beans (`ReferenceDataService`, `ReferenceDataReaders`) and `ReferenceTableHandlers` exist whatever the flag; `ReferenceDataReaders.enabled()` returns the flag; the registry's write methods refuse when it is off. The migration always runs when the Flyway bean runs; it creates the two tables, the triggers and 38 catalog rows, and seeds no reference version or row.
- **First use:** the 12 column definitions are loaded through the PARAMETER branch and approved before the first table load (SPEC-029); the content of the 12 tables comes from their owning stories (seam; GAP-43). A built-in table with no definition is refused 422 "no column definition for the table".
- **Rollback:** turn the flag off, or revert the merge request. The migration is forward only and is never edited; the previous tag ignores the new tables and catalog rows. `clean` stays disabled. The 38 catalog rows stay (they are inert without the code); a release that must remove them needs a new migration and a reviewed catalog change.
- **Release note item (for the deployer):** the migration creates `reference_version` and `reference_row` with append-only triggers, changes the row key from global to per-version, and adds 38 parameter catalog rows; `RWB_P3_REFDATA_VERSIONS` defaults to `false`, so the endpoints are absent until the flag is on; the SIT exit for the 12 table contents waits on later stories.
- **Merge:** the orchestrator merges into `develop-recovery` only after `./scripts/dev.ps1 test` exits 0 and `./scripts/dev.ps1 it` exits 0 (TASK-18, TASK-17); the `<seq>` is assigned at merge (D-RUN-07).

Nothing in this plan, `tasks.md` or the supporting files claims a human approval or a ratification of D-RUN-18 to D-RUN-21; OPEN-050 stays open.

## Assumptions

Plan-stage assumptions are in `assumptions.md` (`PA-E1-043-01` to `PA-E1-043-18`). Spec assumptions A-01 to A-46 are carried unchanged and are not re-litigated here. The owner-acceptance items and the unratified orchestrator rulings stay open; none is accepted.

## Status

```text
PLANNER_STATUS_SUMMARY: Plan ready: 20 tasks (TASK-00..TASK-19) for one guarded migration with the reference version/row tables and 38 catalog rows, the P3 refdata service and registry, the P4 LOV read and handler SPI, the three load/approve/rollback endpoints, the PARAMETER branch, rights and audit, the read cache and version log, the boundary rules, the unit and System suites, the coverage gate and the merge gate.
PLANNER_STATUS_DETAIL: SUCCESS [REASON: spec revision 10 passed its gate 0/0/0/0; RWB-TE-001 plan v7, RWB-E1-044 plan v2 and RWB-E1-042 plan v2 are the base; every SPEC, AC, BR, TC, SEC and CLAR is mapped to a task and a named test; no row is BLOCKED] [UNBLOCK_ACTION: n/a]
PLANNER_CLARIFICATION_STATUS: READY [OPEN_ITEMS: 0] [UNBLOCK_ACTION: n/a - the spec has no OPEN CLAR row; the owner-acceptance items and D-RUN-18..21 remain open and unratified, OPEN-050]
PLANNER_DESIGN_SOURCE: NOT_REQUIRED [NOTE: UI In Scope NO; no screen, route or component change]
PLAN_REQUIREMENT_COVERAGE_SUMMARY: All 49 requirement-logic rows, SPEC-001..032 and TC-E1-043-01..11 map to tasks and named tests; the 16 lines owned by other stories stay seams; the 40 source contradictions stay settled in the spec.
PLAN_REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 49] [TASK_COVERED_RULES: 49] [MISSING_TASK_RULES: 0] [AMBIGUOUS_TASK_RULES: 0] [CONTRADICTIONS: 0]
GATE_REVIEW: PENDING_ORCHESTRATOR
```
