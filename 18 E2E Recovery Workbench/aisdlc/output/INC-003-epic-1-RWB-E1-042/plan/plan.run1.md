---
title: "Implementation Plan: RWB-E1-042 Central configuration service and parameter catalog"
run_id: "INC-003-epic-1-RWB-E1-042"
story: "RWB-E1-042"
epic: "EPIC-001"
status: "SUCCESS"
revision: "v1 (18 Nov 2026): first plan stage for this run. Written against specify/spec.md revision 13 (spec gate round 12, PASS 0/0/0/0) and the RWB-TE-001 plan v7 package layout, coverage wiring and test names (D-RUN-17), with the RWB-E1-044 plan v1 for the Flyway and migration conventions."
prepared: "2026-11-18"
---

# Implementation Plan: RWB-E1-042 Central configuration service and parameter catalog

Design Source: `NOT_REQUIRED` (UI In Scope: NO; `DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0]` in `../specify/spec.md` §20).

| Field | Value |
|---|---|
| Spec | `../specify/spec.md` revision 13 (1302 lines, file 2026-11-18 06:01:50). Spec gate round 12 `REVIEW-RWB-E1-042-SPEC-014`: `PASS` 0 Critical / 0 High / 0 Medium / 0 Low (`../review/spec-gate-review-12.md`). `status: SUCCESS_WITH_ASSUMPTIONS`; `REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 57] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]`. |
| Story | User Stories Epic 1 Story Files v7, RWB-E1-042 v1 (`legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-042-central-configuration-service-and-parameter-catalog-v1.md`), §1 to §19. |
| Base layout (D-RUN-17) | RWB-TE-001 plan v7 (`../../INC-002-epic-1-RWB-TE-001/plan/plan.md`, `tasks.md`, `data-model.md`; its plan gate round 7 `PASS` 0/0/0/0). RWB-TE-001 merges before this story (Build Sequence v6 order 2; this story order 3). |
| Migration convention | RWB-E1-044 plan v1 (`../../INC-001-epic-1-RWB-E1-044/plan/plan.md`) and its SPEC-001, -007, -014: one file per story, `<seq>` assigned at merge (D-RUN-07, D-RCV-28), lint in `RecoveryMigrationLintTest` made identifier-only and quote-aware. |
| Code base | This repository at `develop-recovery` as read on 18 Nov 2026 (baseline `751909e` plus what RWB-TE-001 and RWB-E1-044 leave). `backend/src/main/java/th/co/scb/ace/demo/recovery/` today holds `platform`, `rules`, `workflow`, `documents` only; `backend/src/main/resources/db/modulemigration/recovery/` holds `README.md` and no `.sql` file. No git command, container or build was run; no file outside `plan/` was written. |
| Paths | Every path below is the file's path in this repository. Paths marked `[TE-001]` exist only after RWB-TE-001 merges (D-RUN-17); paths marked `[E1-044]` depend on the migration lint that story leaves. Nothing from the v2 ACE monorepo layout is assumed. |
| Builder | Implementation Builder in its own git worktree from `develop-recovery` **after** the RWB-TE-001 merge (PRE-7). Commits `RWB-E1-042: <summary>` with the `AISDLC-Run` and `AISDLC-Plan` trailers. |
| Smallest change | One P3 module package pair (`casewf.config`, `casewf.config.api`), one additive P4 seam set, one migration, one catalog CSV, one grants CSV, one build file with two edits, two YAML files, and test-scope tooling plus tests. No new dependency, no new Gradle project, no endpoint for the three load operations (D-RUN-10), no OpenAPI change, no frontend change. |
| One module | **PASS — one ACE module (recovery)**, nested P3 `casewf.config` and additive P4 `access`; see "One-module check (D-RUN-21)". |

## Upstream readiness

| Check | Result |
|---|---|
| Spec status | `SUCCESS_WITH_ASSUMPTIONS`; every rule mapped, 25 open items each with a labelled default, 0 blocking (spec §20) |
| Spec gate | `PASS` round 12, 0 findings; finding 163 resolved on all four items; no regression (`../review/spec-gate-review-12.md` §1, §6) |
| `REQUIREMENT_COVERAGE_RESULT` | 57 of 57 rules covered, `MISSING_RULES: 0`, `CONTRADICTIONS: 0` |
| Clarification log | 28 rows: CLAR-020 `RESOLVED`; CLAR-025 and CLAR-027 `SETTLED` by unratified orchestrator decisions D-RUN-21 and D-RUN-20 (OPEN-050); 25 `OPEN`, none blocking, each with a labelled default in `../specify/assumptions.md` |
| Design evidence | `NOT_REQUIRED`: UI In Scope NO, 0 screens, no Figma link, no `frontend/components.md` |
| Migration | One file, `<seq>` not fixed (D-RUN-07) |
| Base dependency | RWB-E1-044 (order 1) and RWB-TE-001 (order 2) are earlier stories, not seams (D-RUN-08). If the branch is cut before either merges, the plan stops and waits (PRE-6, PRE-7) |

Clarification status: `READY`, 25 open items, none blocking — each OPEN item carries a labelled default in `../specify/assumptions.md`; spec gate 12 passed 0/0/0/0 and records `BLOCKING: 0`. The machine-readable line is in "Status" below.

The planner gate in `.github/rules/planning-execution-gates.md` clears `RESOLVED` items. This spec records its 25 remaining items as `OPEN (non-blocking)` with a labelled default each, because RUN-BRIEF rule 4, L-RCV-03 and `AGENTS.md` §10.6 forbid a question to the user in an automated stage. The plan therefore proceeds on those recorded defaults, cites each one where it changes a file, and treats none as answered: no human approval is claimed anywhere in this plan. The two `SETTLED` rows are cited as orchestrator rulings only.

## Plan-time checks required by the spec

The spec's §12.14 plan inputs R4-6, R5-1, R6-3, R7-1, R7-2, R8-1, R8-2, R9-1, R10-1, R10-2 and R11-1 require checks at plan time. Each is done here; the Builder repeats the ones marked "TASK-00".

| # | Check | Result |
|---|---|---|
| 1 | RWB-E1-043 revision in force (E43S): `PARAMETER` dispatcher branch, `ObjectProvider<ParameterLoadHandler>`, flag-off 404 MSG-P4-003, no `PARAMETER` SPI bean | Read at E43S revision 9 (`spec.md`, 05:58:43) and revision 8 (05:45:08) as `../specify/spec.md` records them: `ParameterLoadBranch` in `casewf.refdata.internal`, E43S SPEC-026, E43S SPEC-030, TC-PB-01, TC-FL-01, GAP-57 settled by D-RUN-20. The names this story publishes are unchanged (`ParameterLoadHandler`, `ParameterLoadResult`, `ParameterKeys`, `ParameterService`, `BusinessDateProvider`, `CatalogParameterReader`). This story changes nothing in E43S and does not depend on an E43S file |
| 2 | RWB-E1-043 imports `casewf.config.api`, not `platform.api` | Confirmed by the same read; the shared-updates row to E43S is carried (`../specify/shared-updates.md` §4, rev 13 row) |
| 3 | D-RUN-18 to D-RUN-21 are **not** ratified | Recorded: OPEN-050 owns ratification. This plan cites them as orchestrator rulings and claims no ratification. CLAR-027 and CLAR-025 stay `SETTLED`, never `RESOLVED` |
| 4 | CLAR-028 (RWB-E1-037 per-table approver keys) is not decided here | Not decided. The literal-only rule of SPEC-003/A-55 stands, and `ParameterKeys.byName` is for P3 callers (SPEC-005). Nothing in this plan designs a computed-key route |
| 5 | `ApiProblemException#error()` callers | Searched `backend/src` on 18 Nov 2026: exactly two call sites, both in `backend/src/main/java/th/co/scb/ace/demo/recovery/platform/internal/ApiExceptionHandler.java` line 35 and line 36, both inside `problem`. After RWB-TE-001 that file is `backend/src/main/java/th/co/scb/ace/demo/recovery/access/internal/ApiExceptionHandler.java`. No other caller exists, so the new form with `error() == null` has one fixed call site to guard (TASK-11, TC-30) |
| 6 | RWB-TE-001 v7 coverage wiring does not take this story's tooling package | RWB-TE-001 plan v7 TASK-01 and "Coverage gate edit" include only `th/co/scb/ace/demo/recovery/architecture/boundary/**`. `architecture/parameters/**` is **not** taken in, so case 1 applies: this story extends the merged filter with its own directory (TASK-21), never replaces it |
| 7 | RWB-TE-001 v7 homes for the moved classes | `ApiError`, `ApiProblemException` → `access/api`; `ApiExceptionHandler`, `ProblemFactory`, `SecurityConfig` → `access/internal`; `RecoveryFlags` → `integration/flags/api`; `RecoveryFlywayConfig` → `casewf/migration`; `RecoveryProperties` deleted. All paths in this plan use those homes (PRE-7) |
| 8 | Baseline literal list for the magic-number ratchet | Not restated here: SPEC-004 and §12.11 require the plan to re-derive it from the code, so TASK-00 re-derives it at the merged base and TASK-04 writes the file. The spec's candidate list (HTTP statuses in `ApiError`, `DroolsRuleEngine` 16 and 0.75f, `PdpaPayloadCodec` 12/128/16/24/32, `PlatformSmokeWorkflow` 5 and 3, `WorkflowIds` strings) is the expected starting set, not an authority |
| 9 | `Parameter` and `ReferenceLoad` shapes in API v4 | Read `api/recovery-api-v4.yaml` lines 4857-4903 (path and its four query parameters `key`, `kind`, `owner`, `environment`), 8832-8846 (`ReferenceLoad`: `id`, `table`, `validFrom`, `status`, `rows`) and 9823-9862 (`Parameter`: 16 fields, `validFrom` `format: date`). They match spec §7.5; no OpenAPI change and no `frontend/src/api/schema.d.ts` regeneration |
| 10 | R10-2 ArchUnit cross-check of the reader-call rule | **Not adopted.** The spec calls it an optional plan option, and the source-level rule of §12.11 plus its unit cases (TC-03 (b) to (i)) carry the requirement. Adopting it would add a second, differently-timed check with no rule to compare against |

## Scope

In scope. Each bullet maps to tasks in `tasks.md` ("Scope bullet to task map").

1. **S-1 Catalog file, parser and the two build checks** — the 19-row `parameter-catalog.csv`, `CatalogFileParser`, `CatalogCompletenessRules` (including the source-level reader-call rule), `MagicNumberScanner` and the reviewed baseline (SPEC-003, -004, §7.1, §12.11). → TASK-01, -02, -03, -04, -05
2. **S-2 Generated typed keys** — the Gradle task, `ParameterKey<T>`, `ParameterKeys` with `all()` and `byName`, and the key-generation drift test (SPEC-005, -024). → TASK-06, -07
3. **S-3 Published interfaces and module placement** — `casewf.config.api` (11 types with `@NamedInterface(name = "config.api", propagate = false)`), the three `access.api` types, the module-map entry and the extended published-surface test (SPEC-017, -026). → TASK-08, -09
4. **S-4 Problem bodies, messages and the capability seam** — `ApiProblemException`'s status-and-message-ID form with `detail`, its rendering and log line in `access.internal`, `FixedMessageCatalog`, `InterimCapabilityCheck` and its grants file (SPEC-020, -022, -025, §10.2). → TASK-10, -11, -12, -13
5. **S-5 Migration, tables and seed** — one `V<seq>__rwb_e1_042_parameter_catalog_and_seed.sql`, guarded DDL, 19 catalog rows and 40 value rows, the self-check block (SPEC-001, -002, -006). → TASK-14, -15
6. **S-6 Parameter read service and cache** — `ParameterService`, the converter, per-environment resolution, the version cache with its TTL, secret refusal, and the `CatalogParameterReader` implementation (SPEC-007, -008, -009, -010, -023, -024). → TASK-16, -17
7. **S-7 Catalog endpoint and readiness** — `GET /admin/parameters` with its four filters and method check, the status-only 503, and the `parameterCatalog` readiness indicator (SPEC-011, -016, -020, -025). → TASK-16, -17, -20
8. **S-8 Load, approve, rollback** — `ParameterLoadValidator` (the twelve checks in order), the canonical hash and idempotency, `ParameterLoadHandlerImpl` with its own transactions, maker-checker, validity recomputation and refusals (SPEC-012, -013, -014, -015, -017). → TASK-18, -19
9. **S-9 Event, decision record and cache refresh** — `ParameterVersionApproved` after commit, `ParameterLoadRolledBack`, the `AFTER_COMMIT` listeners and the `VersionDecisionRecorder` port with `MSG-P7-003` on failure (SPEC-014, -018, -019). → TASK-18, -19, -20
10. **S-10 Feature flag and bean registration** — `rwb.p3.configservice` in both YAML files, `@ConditionalOnProperty` on the conditional beans, `@Value` in the two always-registered beans, and the flag-off contract (SPEC-021, §12.12). → TASK-17, -20
11. **S-11 Privacy, secrets, logging and audit** — no user ID in a log line, event, exception or response; no secret stored or served; AC-VERS written inside the approval transaction (SPEC-010, -019, -027, §12.13). → TASK-11, -17, -19, -25
12. **S-12 Coverage, gates and evidence** — this story's tooling in RWB-TE-001's combined 80% bundle, then the unit, container and coverage runs (§14; D-RCV-40). → TASK-21, -22, -23
13. **S-13 Merge gate and scope evidence** — `./scripts/dev.ps1 test`, scope and guardrail check, no new dependency, no file outside the list (§17, §18). → TASK-24, -25

Out of scope (spec §18; each a named seam owned by a later story, D-RUN-08): the shared reference-load endpoint and its dispatch, `/verify` and the other table codes (RWB-E1-043, D-RUN-10, D-RUN-11), including the flag-off refusal of `PARAMETER`; column definitions per table code (RWB-E1-043); the access-log entry for `GET /admin/parameters` (RWB-E1-039); product-specific values and service levels (RWB-E1-045); the dated flag table (RWB-E1-047); the parameter administration screen (Epic 8, `SCR-39`); the change checklist and audit report (RWB-E2-041); the decision-log store and writer (RWB-E1-008, RWB-E1-027); the outbox (RWB-TE-006); the permission matrix and sessions (RWB-E1-037, RWB-E1-022); moving Temporal and Drools reads to `ParameterService` (RWB-E1-071, RWB-E1-072); the message table (unowned, `OI-E1-042-004`). None is built; each appears only as an interface, an interim implementation or a documented seam.

## One-module check (D-RUN-21)

`AGENTS.md` §7 and §9 ask that a plan "touches one module". Build decision D-RUN-21 (`AI-SDLC-BUILD-LOG.md` decisions table, 18 Nov 2026 05:36, the orchestrator (Claude Code); ratification tracked as OPEN-050, owner the recovery tech lead) settles the reading: **"touches one module" means the ACE module, the recovery module.**

| Check | Result |
|---|---|
| ACE module touched | `recovery` only — every main and test class is under `th.co.scb.ace.demo.recovery` |
| Nested design modules touched | P3 `casewf.config` (main and published `casewf.config.api`); P4 `access.api` and `access.internal` (the three new types, the additive constructor, its rendering and the two interim implementations); P3 `casewf.migration` is read only (the migration folder is not a Java package) |
| Other ACE modules | None. No `common`, `collection`, `platform`, `rules`, `workflow` or `documents` package is created, read or referenced; the packages RWB-TE-001 deletes are not named in any new file |
| Non-Java files touched | `backend/build.gradle.kts` (shared build file), `backend/src/main/resources/config/parameter-catalog.csv`, `backend/src/main/resources/access/interim-capability-grants.csv`, `backend/src/main/resources/application.yaml`, `backend/src/main/resources/application-local.yaml`, one migration under `backend/src/main/resources/db/modulemigration/recovery/` |
| Verdict | **PASS — one module (recovery).** The P3 + P4 plan does not go back to the analyst under AGENTS §7, and it changes neither the common nor the collection module. No analyst or tech-lead approval is claimed |

Module-boundary evidence: `RecoveryBoundaryTest` and `ModulithTest` stay green (TASK-09, TASK-22) with `config.api` added to the `casewf` `published` list; no P4 type refers to a P3 type; no P1, P2 or P4 → P3 edge is added (SPEC-026, TC-45, TC-46).

## Backend Plan

Surface status: **CHANGED**. Unit tests **REQUIRED** (trace SPEC-001 to -027; gate per "Unit test applicability").

### Files added — main, P3 `casewf.config`

Paths are exact. All are new; none exists on `develop-recovery` today and none is created by RWB-TE-001 (TE-001 creates `casewf` with `config.api` reserved, and no class in it).

| Path | Content | Task | SPEC |
|---|---|---|---|
| `backend/src/main/java/th/co/scb/ace/demo/recovery/casewf/config/package-info.java` | `@ApplicationModule` for the P3 sub-package, no named interface | TASK-09 | 026 |
| `backend/src/main/java/th/co/scb/ace/demo/recovery/casewf/config/api/package-info.java` | `@NamedInterface(name = "config.api", propagate = false)` | TASK-09 | 026 |
| `backend/src/main/java/th/co/scb/ace/demo/recovery/casewf/config/api/ParameterService.java` | The two `get` overloads and `entry(String)` | TASK-09 | 007, 017 |
| `backend/src/main/java/th/co/scb/ace/demo/recovery/casewf/config/api/ParameterValue.java` | `record ParameterValue<T>(String key, T value, int versionNo, LocalDate validFrom, String environment)` | TASK-09 | 007 |
| `backend/src/main/java/th/co/scb/ace/demo/recovery/casewf/config/api/ParameterKey.java` | Typed key with the metadata of `data-model.md` §3 and `static <T> ParameterKey<T> of(String, Class<T>)` | TASK-07 | 005 |
| `backend/src/main/java/th/co/scb/ace/demo/recovery/casewf/config/api/CatalogEntry.java` | The catalog-only view of a key (no value) | TASK-09 | 007, 017 |
| `backend/src/main/java/th/co/scb/ace/demo/recovery/casewf/config/api/ParameterNotInForceException.java` | Unchecked; message holds the key only | TASK-09 | 007 |
| `backend/src/main/java/th/co/scb/ace/demo/recovery/casewf/config/api/SecretNotServedException.java` | Unchecked; message holds the key only | TASK-09 | 010 |
| `backend/src/main/java/th/co/scb/ace/demo/recovery/casewf/config/api/ParameterLoadHandler.java` | `TABLE = "PARAMETER"`, `load`, `approve`, `rollback`, `find` | TASK-09 | 017 |
| `backend/src/main/java/th/co/scb/ace/demo/recovery/casewf/config/api/ParameterLoadResult.java` | `record ParameterLoadResult(UUID loadId, String table, LocalDate validFrom, String status, int rows, boolean repeat)` | TASK-09 | 017 |
| `backend/src/main/java/th/co/scb/ace/demo/recovery/casewf/config/api/ParameterVersionApproved.java` | Event record of `data-model.md` §6 | TASK-09 | 018 |
| `backend/src/main/java/th/co/scb/ace/demo/recovery/casewf/config/api/BusinessDateProvider.java` | `LocalDate today()` | TASK-09 | 023 |
| `backend/src/main/java/th/co/scb/ace/demo/recovery/casewf/config/ParameterServiceImpl.java` | Resolution, conversion, ENV reads, flag-off defaults, secret and product refusals | TASK-17 | 007, 008, 010, 022, 023, 024 |
| `backend/src/main/java/th/co/scb/ace/demo/recovery/casewf/config/CatalogParameterReaderImpl.java` | P4 interface implementation, package-private, always registered | TASK-17 | 026 |
| `backend/src/main/java/th/co/scb/ace/demo/recovery/casewf/config/CatalogSource.java` | Bean returning `ParameterKeys.all()`; replaceable in tests | TASK-17 | 005, 016 |
| `backend/src/main/java/th/co/scb/ace/demo/recovery/casewf/config/ParameterCache.java` | Per-instance `(key, environment)` version list, TTL, rebuild | TASK-17 | 009, 018 |
| `backend/src/main/java/th/co/scb/ace/demo/recovery/casewf/config/ParameterValues.java` | The one converter of `data-model.md` §3 | TASK-17 | 005, 007 |
| `backend/src/main/java/th/co/scb/ace/demo/recovery/casewf/config/ParameterCatalogController.java` | `GET /api/recovery/v1/admin/parameters`, filters, method check, E7 catch | TASK-17 | 011, 020, 025 |
| `backend/src/main/java/th/co/scb/ace/demo/recovery/casewf/config/CatalogParameterView.java` | Response record whose JSON matches API v4 `Parameter` | TASK-17 | 011 |
| `backend/src/main/java/th/co/scb/ace/demo/recovery/casewf/config/ParameterStartupCheck.java` | `HealthIndicator` bean `parameterCatalog` | TASK-17 | 016 |
| `backend/src/main/java/th/co/scb/ace/demo/recovery/casewf/config/ParameterLoadHandlerImpl.java` | `load`, `approve`, `rollback`, `find` with their own transactions | TASK-19 | 012..015, 017 |
| `backend/src/main/java/th/co/scb/ace/demo/recovery/casewf/config/ParameterLoadValidator.java` | The twelve §12.5 checks, first failure refuses all | TASK-19 | 012, 014, 015 |
| `backend/src/main/java/th/co/scb/ace/demo/recovery/casewf/config/ParameterContentHash.java` | Canonical form and SHA-256 (§12.6) | TASK-19 | 013 |
| `backend/src/main/java/th/co/scb/ace/demo/recovery/casewf/config/ParameterValidity.java` | `valid_to` recomputation (§12.7) | TASK-19 | 014, 015 |
| `backend/src/main/java/th/co/scb/ace/demo/recovery/casewf/config/CsvRows.java` | RFC 4180 reader shared by the catalog parser and the load file | TASK-02, TASK-19 | 003, 012 |
| `backend/src/main/java/th/co/scb/ace/demo/recovery/casewf/config/ParameterSchemaLimits.java` | Named constants: rollback reason 400, hash length 64 (schema limits, added to the magic-number baseline) | TASK-19 | 004, 015 |
| `backend/src/main/java/th/co/scb/ace/demo/recovery/casewf/config/VersionDecisionRecorder.java` | Non-published port, `@Transactional(propagation = MANDATORY)` | TASK-19 | 019 |
| `backend/src/main/java/th/co/scb/ace/demo/recovery/casewf/config/InterimVersionDecisionRecorder.java` | One structured line, no user ID | TASK-19 | 019, 027 |
| `backend/src/main/java/th/co/scb/ace/demo/recovery/casewf/config/InterimBusinessDateProvider.java` | Today in Asia/Bangkok | TASK-17 | 023 |
| `backend/src/main/java/th/co/scb/ace/demo/recovery/casewf/config/ParameterLoadRolledBack.java` | Package-private event record, published inside the rollback transaction | TASK-19 | 015 |
| `backend/src/main/java/th/co/scb/ace/demo/recovery/casewf/config/ParameterCatalogEntity.java` | `@Entity` for `parameter_catalog`; schema from `hibernate.default_schema` | TASK-17 | 002 |
| `backend/src/main/java/th/co/scb/ace/demo/recovery/casewf/config/ParameterValueEntity.java` | `@Entity` for `parameter_value`, including the three added columns | TASK-17 | 002 |
| `backend/src/main/java/th/co/scb/ace/demo/recovery/casewf/config/ParameterCatalogRepository.java` | `JpaRepository<ParameterCatalogEntity, UUID>`, `findByParamKey` | TASK-17 | 002, 011 |
| `backend/src/main/java/th/co/scb/ace/demo/recovery/casewf/config/ParameterValueRepository.java` | Approved-version, max-version, load and hash queries | TASK-17, TASK-19 | 002, 007, 013..015 |

### Files changed — main, P4 `access` `[TE-001]`

| Path | Change | Task | SPEC |
|---|---|---|---|
| `backend/src/main/java/th/co/scb/ace/demo/recovery/access/api/ApiProblemException.java` | Add the status-and-message-ID constructor with optional `detail` and the four accessors; `error()` returns null for that form; the `ApiError` constructor unchanged | TASK-11 | 022, 025 |
| `backend/src/main/java/th/co/scb/ace/demo/recovery/access/api/MessageResolver.java` | New published interface, `english` and `thai` | TASK-09 | 022 |
| `backend/src/main/java/th/co/scb/ace/demo/recovery/access/api/CapabilityCheck.java` | New published interface, `has` and `require` | TASK-09 | 020 |
| `backend/src/main/java/th/co/scb/ace/demo/recovery/access/api/CatalogParameterReader.java` | New published interface with nested `record Value<T>` and the two `get` overloads | TASK-09 | 026 |
| `backend/src/main/java/th/co/scb/ace/demo/recovery/access/internal/FixedMessageCatalog.java` | `MessageResolver` over the nine IDs of `data-model.md` §7 | TASK-11 | 022 |
| `backend/src/main/java/th/co/scb/ace/demo/recovery/access/internal/InterimCapabilityCheck.java` | `@Component("capabilityCheck")`, reads the grants CSV | TASK-13 | 020 |
| `backend/src/main/java/th/co/scb/ace/demo/recovery/access/internal/ApiExceptionHandler.java` | `problem` keeps the `error()` branch and adds the null-`error()` branch with its single WARN line | TASK-11 | 022, 025, 027 |
| `backend/src/main/java/th/co/scb/ace/demo/recovery/access/internal/ProblemFactory.java` | Render the message-ID form (with and without `detail`) and the status-only form | TASK-11 | 022, 025 |

Not changed: `ApiError` (its four constants stay the 401/403/404 message IDs), `SecurityConfig`, `ApiExceptionHandler.forbidden`, `ApiExceptionHandler.notFound`, `ApiExceptionHandler.unexpected`, `RecoveryFlags`, `integration.flags.*`, `casewf.migration.*`, `casewf.admin.*`, every other main class.

### Files added or changed — resources, build and migration

| Kind | Path | Content | Task | SPEC |
|---|---|---|---|---|
| Add | `backend/src/main/resources/config/parameter-catalog.csv` | Header and the 19 rows of `data-model.md` §2, RFC 4180 quoting, `used_by` separated by `;` | TASK-03 | 003, 005, 024 |
| Add | `backend/src/main/resources/access/interim-capability-grants.csv` | `role,area,rights`; one row per RW- role of Users, Roles and Permissions v4 lines 76-110 | TASK-13 | 020 |
| Add | `backend/src/main/resources/db/modulemigration/recovery/V<seq>__rwb_e1_042_parameter_catalog_and_seed.sql` | Line 1 `-- Story: RWB-E1-042`; the eight statement groups of `data-model.md` §4 | TASK-15 | 001, 002, 006 |
| Edit | `backend/src/main/resources/application.yaml` | `rwb.p3.configservice: ${RWB_P3_CONFIGSERVICE:false}`; `management.endpoint.health.group.readiness.include: readinessState,parameterCatalog` | TASK-17 | 016, 021 |
| Edit | `backend/src/main/resources/application-local.yaml` | `rwb.p3.configservice: ${RWB_P3_CONFIGSERVICE:true}` | TASK-17 | 021 |
| Edit | `backend/build.gradle.kts` | (a) `generateParameterKeys` task, its output directory on `sourceSets.main`, `compileJava` depends on it; (b) the test-output classes of `.../architecture/parameters/**` added to `classDirectories` of both JaCoCo tasks | TASK-07, TASK-21 | 005, 014 |
| Unchanged | `backend/src/main/resources/db/modulemigration/recovery/README.md`, `backend/Dockerfile`, `docker-compose.yml`, `.gitlab-ci.yml`, `scripts/dev.ps1`, `api/recovery-api-v4.yaml`, `frontend/**` | — | — | 001, 011 |

The catalog sits under `backend/src/main/resources/config/` because the Docker build context is `./backend` and copies only `src` (`backend/Dockerfile`; `docker-compose.yml` line 120) — A-26.

### Files added or changed — test scope

`T` = `backend/src/test/java/th/co/scb/ace/demo/recovery`. Every row's path is the exact repository path with that prefix expanded. All tooling is in the test source set, so the main module map, `ModulithTest` and `DO_NOT_INCLUDE_TESTS` never see it.

| Kind | Path | Content | Task | SPEC |
|---|---|---|---|---|
| Edit | `backend/src/test/resources/architecture/recovery-modules.yaml` `[TE-001]` | Add `config.api` to the `casewf` `published` list; nothing else | TASK-08 | 026 |
| Edit | `backend/src/test/java/th/co/scb/ace/demo/recovery/architecture/RecoveryBoundaryTest.java` `[TE-001]` | Extend `publishedSurfaceIsExactlyTheSpecifiedTypes` (T-TE001-14): 11 `casewf.config.api` types; `access.api` gains `MessageResolver`, `CapabilityCheck`, `CatalogParameterReader`, `CatalogParameterReader.Value`; `casewf` named interfaces gain `config.api`. Nothing removed, no assertion relaxed | TASK-08 | 026 |
| Edit | `backend/src/test/java/th/co/scb/ace/demo/recovery/access/internal/ApiExceptionHandlerTest.java` `[TE-001]` | TC-30 forms (a) to (e), with a synthetic marker cause | TASK-10 | 022, 025, 027 |
| Unchanged | `backend/src/test/java/th/co/scb/ace/demo/ModulithTest.java`, `backend/src/test/java/th/co/scb/ace/demo/recovery/architecture/RecoveryMigrationLintTest.java` `[E1-044]`, `backend/src/test/java/th/co/scb/ace/demo/recovery/RecoveryDatabaseIT.java`, `backend/src/test/java/th/co/scb/ace/demo/e2e/PlatformE2ETest.java`, `backend/src/test/java/th/co/scb/ace/demo/testsupport/ApplicationYamlEnvironment.java` `[TE-001]` | — | — | 001, 007, 018, 026 |
| Add | `T/architecture/parameters/JavaLiteralTokenizer.java` | One pass: strips comments, reads string, text-block and char literals, keeps offsets and lines | TASK-02 | 003, 004 |
| Add | `T/architecture/parameters/MagicNumberScanner.java` | Token stream to normalised numeric literals and to string literals | TASK-02 | 004 |
| Add | `T/architecture/parameters/CatalogFileParser.java` | The §7.1 rules: header, types, ranges, defaults, `used_by` grammar, ENV credential rule | TASK-02 | 003, 005 |
| Add | `T/architecture/parameters/CatalogRow.java` | Parsed row record with every catalog column | TASK-02 | 003, 005 |
| Add | `T/architecture/parameters/CatalogCompletenessRules.java` | Key-read scan (including the §12.11 reader-call rule), row rules, drift comparison | TASK-05 | 003, 005 |
| Add | `T/architecture/parameters/MagicNumberBaseline.java` | Reads the baseline CSV, reports a stale entry | TASK-05 | 004 |
| Add | `backend/src/test/resources/architecture/magic-number-baseline.csv` | `path,literal,count,reason,owner` re-derived at TASK-00 | TASK-04 | 004 |
| Add | `backend/src/test/resources/architecture/fixtures/parameter-checks/**` | The fixture corpus of `data-model.md` §8 (not compiled) | TASK-04 | 003, 004 |
| Add | `T/architecture/parameters/JavaLiteralTokenizerTest.java` | TC-43 | TASK-01 | 004 |
| Add | `T/architecture/parameters/MagicNumberScannerTest.java` | TC-43 | TASK-01 | 004 |
| Add | `T/architecture/parameters/CatalogFileParserTest.java` | TC-41, TC-44 | TASK-01 | 003 |
| Add | `T/architecture/parameters/CatalogCompletenessCheckTest.java` | TC-03, TC-21, TC-44, TC-27 (fixture part) | TASK-04 | 003, 005 |
| Add | `T/architecture/parameters/RwbMagicNumberCheckTest.java` | TC-02, TC-25 | TASK-04 | 004 |
| Add | `T/architecture/parameters/ParameterKeysGenerationTest.java` | TC-42 | TASK-06 | 005 |
| Add | `T/casewf/config/ParameterServiceTest.java` | TC-01, TC-09, TC-11, TC-26 (unit) | TASK-16 | 007, 008, 010, 024 |
| Add | `T/casewf/config/ParameterCacheTest.java` | TC-11, TC-28 (unit) | TASK-16 | 009, 018 |
| Add | `T/casewf/config/ParameterStartupCheckTest.java` | TC-04, TC-32 (unit) | TASK-16 | 016 |
| Add | `T/casewf/config/ParameterCatalogControllerTest.java` | TC-24 (403 slice), TC-34 (E7 slice), TC-31 (filter unit) | TASK-16 | 011, 020, 025 |
| Add | `T/casewf/config/CatalogParameterReaderImplTest.java` | TC-46 | TASK-16 | 023, 026 |
| Add | `T/casewf/config/ParameterLoadValidatorTest.java` | TC-05, TC-06, TC-23, TC-36, TC-39 (unit) | TASK-18 | 012, 014, 015 |
| Add | `T/casewf/config/ParameterContentHashTest.java` | TC-16 (hash part) | TASK-18 | 013 |
| Add | `T/casewf/config/ParameterValidityTest.java` | TC-10, TC-11 (recompute part) | TASK-18 | 014, 015 |
| Add | `T/casewf/config/ParameterLoadHandlerTest.java` | TC-17, TC-20, TC-28, TC-29 (unit, with the stub transaction manager) | TASK-18 | 013, 014, 018, 019 |
| Add | `T/casewf/config/StubTransactionManager.java` | Test-scope `AbstractPlatformTransactionManager` that runs `doBegin`/`doCommit`/`doRollback` without a resource, so a real `TransactionTemplate` executes its callback; no new dependency | TASK-18 | 013, 014 |
| Add | `T/casewf/config/ParameterConfigIT.java` | The System cases of `tests/scenarios.md` (`@Tag("recovery-it")`) | TASK-20 | 007..019, 021, 025 |
| Add | `T/casewf/config/ParameterMigrationIT.java` | TC-13, TC-14, TC-27 (`@Tag("recovery-it")`) | TASK-14 | 001, 002, 006 |
| Add | `T/access/internal/InterimCapabilityCheckTest.java` | TC-24 (unit) | TASK-12 | 020 |
| Add | `T/access/internal/MessageResolverTest.java` | TC-30 (EN and TH for every §10.3 ID) | TASK-10 | 022 |

### Tooling design — the two build checks

SPEC-003 and SPEC-004 require the checks to run in `test` (`check` runs it) and the logic to sit in plain test-scope classes measured in the combined 80% bundle. Package `th.co.scb.ace.demo.recovery.architecture.parameters` (the spec allows the rename; this plan keeps it).

- **`JavaLiteralTokenizer`** — one left-to-right pass over a Java source file. It blanks `//` and `/* */` (nesting not expected in Java, counted anyway), keeps `"…"` and `"""…"""` bodies, `'…'` char literals, and preserves offsets and line numbers. A character in a comment is never scanned again.
- **`MagicNumberScanner`** — from the token stream: numeric literals normalised (drop `_`, lower-case `0x`, strip suffixes `L`/`l`/`f`/`F`/`d`/`D`, keep the sign only when unary), and string literals with their text. The unit names the file and line.
- **`CatalogFileParser`** — reads a CSV with `CsvRows`, validates the header exactly, then the §7.1 rules per column: `key` pattern and uniqueness, `kind`, `value_type`, `unit` length, `min`/`max` parse and order, `default_value` presence (with the PRODUCT, secret and ENV exemptions) and parse and range, `scope`, `required`, `owner_role` in the `RW-` set, `environments` as a comma list of DEV/SIT/UAT/PROD, `used_by` by the `;` grammar (trimmed, non-empty, ≤ 100 characters each, ≤ 400 total, no `;` or line break), `secret` implies `value_source=SECRET` and an empty default, `value_source` in TABLE/ENV/SECRET, `env_property` required exactly for ENV and refused by the credential-name rule (split on `.` only; the eleven substrings of §7.1), `description` ≤ 400. Every failure is a `CatalogFinding` with key and column.
- **`CatalogCompletenessRules`** — over a source root and a parsed catalog:
  1. every key read in recovery main code must be catalogued: a `ParameterKeys` constant, a `ParameterKey.of("…", X.class)` call, or the first argument of a reader call (the §12.11 reader-call rule, restated in `data-model.md` §5). A non-literal key, a `::` method reference, a `var` local from a reader name or an ambiguous name is a finding naming the file and line; `Map.get`/`Optional.get` are not key reads; `casewf/config/CatalogParameterReaderImpl.java` is skipped by path;
  2. every row has an owner, a valid kind, type, scope, range, and a default unless PRODUCT/secret/ENV;
  3. `used_by` parses (already a parser rule, re-checked here so a hand-edited file cannot bypass it);
  4. an ENV row's `env_property` passes the credential-name rule;
  5. the drift direction used by TC-27: given `ParameterKeys.all()`, every mirrored column of a persisted row must equal the catalog row.
- **JUnit entry points** — `CatalogCompletenessCheckTest` and `RwbMagicNumberCheckTest` only call the classes above and assert. `RwbMagicNumberCheckTest` scans `backend/src/main/java` for the real run and a fixture root for the negative cases; `allowed` is `0`, `1`, `-1` and every entry of the baseline file.

No parser with type resolution, no ArchUnit for this rule and no new dependency (`AGENTS.md` §4.4; R10-2 not adopted).

### Generated keys (SPEC-005)

`backend/build.gradle.kts` gains one task, `generateParameterKeys` (`DefaultTask`, not a new project):

- input `backend/src/main/resources/config/parameter-catalog.csv`; output `build/generated/sources/parameterKeys/th/co/scb/ace/demo/recovery/casewf/config/api/ParameterKeys.java`;
- `sourceSets.main.get().java.srcDir(layout.buildDirectory.dir("generated/sources/parameterKeys"))`; `compileJava` depends on the task; `sourcesJar`/`processResources` need no change;
- the generated class is `public final class ParameterKeys` with one `public static final ParameterKey<T>` constant per row (constant name = `key` upper-cased, `.` and `-` → `_`), `public static List<ParameterKey<?>> all()` returning an immutable list in file order, and `public static <T> Optional<ParameterKey<T>> byName(String key, Class<T> type)` comparing `key()` and `type()` and returning `Optional.empty()` when absent or the type differs.

The task is build-script code and is outside the coverage bundle (SPEC §12.11, A-38, D-RCV-40). Its output is verified by TC-42 (row-for-row against the CSV), TC-26 (typed constants) and TC-27 (the database copy).

### Migration (SPEC-001, SPEC-002, SPEC-006)

One file, `backend/src/main/resources/db/modulemigration/recovery/V<seq>__rwb_e1_042_parameter_catalog_and_seed.sql`. `<seq>` is the next free four-digit number at merge, assigned by the orchestrator; **this plan fixes no number** (D-RUN-07, D-RCV-28). Line 1 is `-- Story: RWB-E1-042`; line 2 is a header comment citing Physical Schema v6, D-RCV-28 and this spec. The eight statement groups, in order, are `data-model.md` §4: guarded `CREATE TABLE IF NOT EXISTS` for the two tables; `ADD COLUMN IF NOT EXISTS` for `load_id`, `content_hash` and `rollback_reason`; `DO`-block guarded constraint additions by name in `${recoverySchema}`; `CREATE [UNIQUE] INDEX IF NOT EXISTS`; `COMMENT ON`; the 19-row catalog seed with `ON CONFLICT (param_key) DO NOTHING`; the 40-row value seed with `INSERT … SELECT … WHERE NOT EXISTS`; the self-check `DO` block restricted to rows with a default.

Constraints: `${recoverySchema}` is the only qualifier, no `SET search_path`, no `GRANT`/`REVOKE`, forward only, never edited after merge. The seed's `used_by` and `COMMENT ON` text contains `recovery.` inside string literals and comments: that is why PRE-6 requires RWB-E1-044's identifier-only, quote-aware lint (`[E1-044]`, T-044-21) and why TC-15 fails by design on a branch cut before that story. The seed values are **not** changed to avoid the lint.

### Load, approve and rollback (SPEC-012 to SPEC-019)

- `load`: `parse` → the twelve checks of `data-model.md` §7 in file order, first failure refuses all → canonical hash (SHA-256 over the rows sorted by key then environment, each line the key, environment and value joined by a pipe character) → write every row `VALIDATED` with the next `version_no` for its `(key, environment)`, one `load_id`, `content_hash` and `created_by = author_user_id`. Own transaction (`REQUIRES_NEW` through `TransactionTemplate`); the `DataIntegrityViolationException` from `ux_parameter_value_version_all` is caught **outside** the rolled-back transaction and re-read in a second, read-only transaction by `(validFrom, content_hash)`, returning the existing load with `repeat = true`, else 409 MSG-GEN-004.
- `approve`: lock the rows (`SELECT … FOR UPDATE`), the §8 checks, set `APPROVED` with approver and `approved_at`, recompute `valid_to`, call `VersionDecisionRecorder.recorded("AC-VERS", "PARAMETER", loadId, keys, validFrom, approverUserId)`, publish `ParameterVersionApproved`, commit. Any `RuntimeException` from the recorder becomes `ApiProblemException(HttpStatus.SERVICE_UNAVAILABLE, "MSG-P7-003", Map.of(), null, null, cause)` thrown inside the transaction, so the approval rolls back.
- `rollback`: non-blank reason ≤ 400 characters after trim, only an `APPROVED` load, every row with an earlier `APPROVED` version, rows to `ROLLED_BACK` with the reason, `valid_to` recomputed, `ParameterLoadRolledBack` published inside the transaction, cache rebuild on `AFTER_COMMIT`. No event leaves the instance.
- `find`: `Optional<ParameterLoadResult>`, `PROPAGATION_SUPPORTS`, never throws for an unknown id.

Rights (C/A/U), multipart parsing and the HTTP status of success are RWB-E1-043's endpoint (D-RUN-10); this story builds no controller for them.

### Cache, readiness, access, flag

- Cache: `ParameterCache` keeps, per `(key, environment)`, the `APPROVED` rows ordered by `valid_from`; the date is resolved on read, so a version starts on its `valid_from` with no restart and no refresh. Entries expire after `config.cache.ttl-seconds` read through `ParameterService`; while that key's own entry is being rebuilt the generated default 60 is used (re-entrancy guard `PA-E1-042-03`). `ParameterVersionApproved` and `ParameterLoadRolledBack` rebuild the affected entries on `AFTER_COMMIT`. The cache never holds `VALIDATED`, `ROLLED_BACK` or secret rows.
- Readiness: `ParameterStartupCheck` is a `HealthIndicator` bean `parameterCatalog` in the readiness group. For each required GLOBAL non-secret key listed for the running environment it asks the `SPEC-016` question (TABLE: an `APPROVED` row in force on `BusinessDateProvider.today()`, else a default; ENV: does the property resolve). DOWN details: `messageCode` `MSG-P3-032` and a list of `{name, environment}`; one WARN line per missing key with the EN text. The process keeps running (CLAR-012).
- Access: `@PreAuthorize("@capabilityCheck.require(authentication, 'Rules and parameters', 'R', 'read parameters')")`; `InterimCapabilityCheck` registered as `capabilityCheck` and reading `backend/src/main/resources/access/interim-capability-grants.csv`.
- Flag: `rwb.p3.configservice` — `@ConditionalOnProperty(prefix = "rwb.p3", name = "configservice", havingValue = "true")` on `ParameterLoadHandlerImpl` and `ParameterCatalogController`; `@Value("${rwb.p3.configservice:false}")` in `ParameterServiceImpl` and `ParameterStartupCheck`. Off: defaults and ENV only, GET 404, no `ParameterLoadHandler` bean, `CatalogParameterReader` still present. No `RecoveryFlags` change, no properties record.

### Coverage wiring (SPEC-014, §12.11; plan input R6-1)

RWB-TE-001's merged `backend/build.gradle.kts` carries `recoveryClasses` plus a `boundaryToolingClasses` collection that includes only `th/co/scb/ace/demo/recovery/architecture/boundary/**`. This story adds a third collection, `parameterToolingClasses`, from `sourceSets.test.get().output.classesDirs` with include `th/co/scb/ace/demo/recovery/architecture/parameters/**` and excludes `**/*Test.class`, `**/*Test$*.class`, `**/*IT.class`, `**/*IT$*.class`; `classDirectories.setFrom(recoveryClasses, boundaryToolingClasses, parameterToolingClasses)` on **both** `recoveryCoverageReport` and `recoveryCoverageVerification`. `sourceDirectories` gains the test `java.srcDirs` only if TE-001's edit does not already add it. No new task, rule, counter, threshold or exclusion; execution data stays `test`; neither task joins `check` (D-RCV-40). If TASK-00 finds that the merged include already takes the package, TASK-21 makes no edit and records that.

## Frontend Plan

**NOT_APPLICABLE.** UI In Scope NO. Story v7 §15: "No screen in this story"; `SCR-39` is Epic 8 (spec §13, §20; `DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SCREENS: 0]`). `GET /admin/parameters` is backend-only in this story, the OpenAPI file is unchanged, and `frontend/src/api/schema.d.ts` is not regenerated. No file under `frontend/` is added or changed, so no frontend unit-test, coverage, component-inventory or functional-automation task exists. `frontend/components.md` is **NOT_APPLICABLE** and is not written. `npm run check` still runs in the merge gate (TASK-24) to prove the frontend did not regress. Existing screens used unchanged: none in this story, so none needs verification evidence.

## API Plan

`API In Scope: YES`; `API Impact Type: NEW_API_REQUIRED` for the code base (the operation exists in API v4 but not in code). One endpoint is implemented:

| Method and path | operationId | Capability | Success | Errors | Consumer |
|---|---|---|---|---|---|
| `GET /api/recovery/v1/admin/parameters` | `getAdminParameters` | Rules and parameters, R | 200 `Parameter[]` | 401, 403, 503 | Backend-only in this story |

Filters are the API's four query parameters `key` (prefix), `kind`, `owner` and `environment` (else `rwb.environment`). `api/recovery-api-v4.yaml` is **not** changed, so there is no contract regeneration and no `openapi-fetch` change. The three reference-load operations are served through `casewf.config.api.ParameterLoadHandler` and exposed by RWB-E1-043 (D-RUN-10); this story tests them through the interface at the same assertion depth an HTTP test would use (message ID, status, placeholders, `field`, database state — plan input P5). Refusals cross the interface as `access.api.ApiProblemException`, so RWB-E1-043 renders them unchanged.

Contract artefacts: `contracts/backend-apis.json` records the endpoint, the internal interfaces, the problem mapping and the verification tasks. `contracts/frontend-integrations.json` records `NOT_APPLICABLE` with the evidence above (no consumer exists and none changes).

## Unit test applicability

| Surface | Changes | Unit tests | Coverage gate | Trace | Evidence and rationale |
|---|---|---|---|---|---|
| Frontend | NO | NOT_APPLICABLE | NOT_APPLICABLE | §13, §18 | Story v7 §15; no OpenAPI change; no screen or client call; no file under `frontend/` |
| Backend | YES | REQUIRED | `recoveryCoverageVerification`: one `BUNDLE` rule, `LINE`, `INSTRUCTION`, `BRANCH`, `METHOD` each 0.80, over the RWB-TE-001 combined bundle plus `architecture.parameters` (TASK-21); task outside `check` (D-RCV-40), run as `./gradlew test recoveryCoverageVerification` | SPEC-001 to -027 | New service, published interfaces, controller, checks, migration. Unit tests in `test` for `ParameterServiceImpl`, each §12.5 check, the §12.6 hash, the §12.7 recomputation, the cache, `ParameterStartupCheck`, the controller (incl. E7), `ParameterLoadHandlerTest`, `CatalogParameterReaderImpl`, the two build checks, the P4 rendering and the capability seam; the `recovery-it` class does not count toward the gate |

No measured coverage is claimed here. The two expected red-before-green points for the gate are recorded in TASK-22: the bundle is measured at the TASK-00 baseline and again after TASK-19; a counter below 0.80 at the end is reported as a blocker, never as an exclusion or a lowered threshold.

## Execution order (tests before code, `AGENTS.md` rules 3 and 10)

1. TASK-00 pre-flight on the merged RWB-TE-001 and RWB-E1-044 base; baseline counters; re-derived literal list.
2. Red first: TASK-01 (tooling unit tests do not compile), TASK-04 (check tests do not compile), TASK-06 (`ParameterKeys` absent), TASK-08 (published-surface test fails), TASK-10 (TC-30 fails on the missing constructor), TASK-12 (capability test does not compile), TASK-14 (migration IT fails on missing tables), TASK-16 (service tests do not compile), TASK-18 (load tests do not compile).
3. Green, in order: TASK-02 (tooling), TASK-03 (catalog CSV), TASK-05 (check rules), TASK-07 (keys generator), TASK-09 (published surface), TASK-11 (problem forms), TASK-13 (capability seam), TASK-15 (migration), TASK-17 (service, cache, readiness, controller, reader, flag), TASK-19 (load handler, recorder, events).
4. TASK-20 writes and runs the System suite; a red case is fixed in the owning implementation task, never by weakening the assertion.
5. Verification: TASK-21 (coverage wiring), TASK-22 (unit suite and coverage gate), TASK-23 (container suite), TASK-24 (merge gate), TASK-25 (scope, guardrail and evidence check).

Every red run and every green run is saved under `implement/` as command, exit code and the first failing assertion or the final summary line.

## Functional Test Scenarios

| ID | Scenario | Owner | Assignment | Evidence |
|---|---|---|---|---|
| FTS-E1042-01 | A squad member adds a catalog row by pull request; the build regenerates the keys and both checks run; an uncatalogued key or a business literal fails it | Functional Automation Test | **NOT_APPLICABLE** — no UI, no screen and no route; the same behaviour is executed by the build-check unit tests TC-02, TC-03, TC-21, TC-25, TC-41 to TC-44 in `./gradlew test`, which is not a functional-automation result | `implement/unit-tests/report.md` |
| FTS-E1042-02 | A deployment applies the migration once and seeds 19 catalog rows and 40 value rows; a second start applies nothing | API Tester | **NOT_APPLICABLE** — no endpoint; the migration has no HTTP surface and `GET /admin/parameters` does not expose a run. Proven by `ParameterMigrationIT` (TC-13, TC-14) | `implement/backend/it.log`; `backend/build/test-results/recoveryIntegrationTest/` |
| FTS-E1042-03 | A role with Rules and parameters R reads `GET /admin/parameters` and sees each entry with the value in force; a secret is listed without a value; a role without the right is refused with the action text | API Tester | **ASSIGNED** — this is the one operation this story exposes | REST Assured or an `api-tests/` run against the local stack; the response compared with TC-09, TC-24 and TC-31. The interface-only cases (load, approve, rollback, TC-05 to TC-07, TC-10, TC-11, TC-16 to TC-20, TC-23) are **not** API-Tester material until RWB-E1-043 opens the HTTP path; they stay in `ParameterConfigIT` |
| FTS-E1042-04 | Readiness reports DOWN, naming the key and the environment, while a required parameter has no value and no default, and turns UP after a load without a restart | Functional Automation Test | **NOT_APPLICABLE** — a start-up and probe behaviour, proven by `ParameterStartupCheckTest` and TC-32 in the container suite, not by a UI journey | `implement/unit-tests/report.md`; `implement/backend/it.log` |
| HV-E1042-01 | A person with a real RW- role set confirms the 403 refusal and the readiness detail page in SIT, with an identity from RWB-E1-022 and the matrix from RWB-E1-037 (TC-E1-042-12) | Human (QA lead / recovery tech lead) | **BLOCKED by later stories**, never reported as tested | `OI-E1-042-001`; exit criterion in `tests/scenarios.md` |

No functional-automation journey exists because the story adds no screen. This is recorded as `NOT_APPLICABLE` with evidence, not as an executed test.

## Migrations

One migration: `V<seq>__rwb_e1_042_parameter_catalog_and_seed.sql` in `backend/src/main/resources/db/modulemigration/recovery/`. **No number is fixed here** (D-RUN-07); the orchestrator assigns `<seq>` at merge as the next four-digit number, and the lint requires a contiguous sequence from `V0001`. Line 1 is `-- Story: RWB-E1-042`. One file for the story: DDL and seed together (D-RCV-28, E1042-RV-DG-01). The folder is empty today, so this is the first recovery migration unless an earlier story merges one first; in either case the number is the merge-order one. No corrective script is planned; a later fix takes the next sequence, keeps the key and adds `-- Fix: <reason>`.

## Rule tables and reference sources read

`AGENTS.md` §3.2 asks that every threshold, limit, timer, queue, role, template and route come from a versioned reference table. This story **builds** that table: the catalog file is the reference table for parameters, and the generated keys are its only Java reader (SPEC-005). The values it seeds are read from the sources below, not written as literals in code.

| Source (name, version) | What it supplies | Applied in |
|---|---|---|
| Decision Log v10, D-RCV-28 (row DL77) | Migration name pattern, one file per story, `<seq>` at merge, line 1 story key, `${recoverySchema}`, schema `recovery` | SPEC-001, -002; TASK-15 |
| Temporal and Drools Change Register v1 (D-RCV-36), §3.1 | The six keys `temporal.target`, `temporal.namespace`, `temporal.taskqueue.platform`, `temporal.retention.days`, `drools.kiebase.cache.max`, and `rules.testcases.min` with their kinds and defaults | §12.4 rows; TASK-03 |
| Physical Schema v6, lines 1386-1409 (`parameter_catalog`), 1412-1434 (`parameter_value`), 1437-1467 (`reference_version`), 1206-1225 (`outbox_event`) | Column definitions, PK, `uk_parameter_catalog`, `uk_parameter_value`, `is_personal` rows | SPEC-002; `data-model.md` §4 |
| API Specification v4, `getAdminParameters` (line 4857), `postAdminReferenceLoads` (3167), approve (3214), rollback (5004), `Parameter` (9823), `ReferenceLoad` (8832), `RollbackRequest` (9818), `Problem`, `E401`/`E403`/`E422`/`E503` | Route, query parameters, response fields, error set | SPEC-011, -012 to -015, -017, -025; `contracts/backend-apis.json` |
| Users, Roles and Permissions v4, matrix sheet lines 73-110 | The "Rules and parameters" column per RW- role for the interim grants file; Reference data C/A/U are RWB-E1-043's check | SPEC-020; TASK-13 |
| Error and Message Standard v4, rows 68-208 (lines 68, 71, 73, 76, 139, 151, 156, 163-165, 207, 208) | The message IDs and their EN and TH text | SPEC-022; `data-model.md` §7 |
| Data Classification and Personal Data Inventory v4, lines 676-677 (DF-REF-156, -157) and 652-678 (no audit-column rows) | Personal-data classification of author, approver, `created_by`, `updated_by` | SPEC-027; TASK-19, TASK-25 |
| Build Sequence Epic 1 and Epic 2 v6 | Order 1 RWB-E1-044, order 2 RWB-TE-001, order 3 this story, order 8 RWB-E1-043, order 27 RWB-E1-037 | Dependencies and seams; §4.3 of the spec |
| `AGENTS.md` v2, §2-§4, §7, §9 | One migration per story, no literal business value, method check on every endpoint, decision record per change, module boundaries, one-module rule | Whole plan |
| Build log, decisions D-RUN-07 to D-RUN-21 | Migration numbering, dependencies, reference-load ownership, migrations per table, lint scope, handler SPI, parameter reads, `PARAMETER` route, one-module reading | Whole plan |

## Requirement Logic To Task Coverage

`REQ_REF` values are the rows of `../specify/spec.md` "Requirement-to-SPEC Logic Coverage" (57 rows, none merged, dropped or weakened).

| REQ_REF | Mapped SPEC-* | Mapped TASK-* | Coverage Type | Verification | Status |
|---|---|---|---|---|---|
| BR1 | 004, 005, 006, 007 | TASK-03, -05, -07, -15, -17 | DIRECT_IMPLEMENTATION | TC-01, TC-02, TC-25, TC-26 | COVERED |
| BR2 | 003, 005 | TASK-01, -02, -03, -04, -05, -07 | DIRECT_IMPLEMENTATION | TC-03, TC-41, TC-42 | COVERED |
| BR3 | 012, 013, 014, 015 | TASK-15, -18, -19 | DIRECT_IMPLEMENTATION | TC-05, TC-06, TC-16, TC-17 | COVERED |
| BR4 | 014 | TASK-18, -19 | DIRECT_IMPLEMENTATION | TC-07, TC-20, TC-29 | COVERED |
| BR5 | 007, 009 | TASK-16, -17 | DIRECT_IMPLEMENTATION | TC-01, TC-11, TC-28 | COVERED |
| BR6 | 010, 002, 003 | TASK-05, -15, -17 | DIRECT_IMPLEMENTATION | TC-09, TC-44 | COVERED |
| BR7 | 016 | TASK-16, -17 | DIRECT_IMPLEMENTATION | TC-04, TC-32 | COVERED |
| AC1 | 006, 007 | TASK-15, -17 | DIRECT_IMPLEMENTATION | TC-01 | COVERED |
| AC2 | 004 | TASK-04, -05 | DIRECT_IMPLEMENTATION | TC-02 | COVERED |
| AC3 | 003 | TASK-04, -05 | DIRECT_IMPLEMENTATION | TC-03 | COVERED |
| AC4 | 016, 022 | TASK-16, -17 | DIRECT_IMPLEMENTATION | TC-04 | COVERED |
| AC5 | 012, 025 | TASK-18, -19 | DIRECT_IMPLEMENTATION | TC-05 | COVERED |
| AC6 | 012, 025 | TASK-18, -19 | DIRECT_IMPLEMENTATION | TC-06 | COVERED |
| AC7 | 014 | TASK-18, -19 | DIRECT_IMPLEMENTATION | TC-07 | COVERED |
| AC8 | 008, 012, 014 | TASK-15, -17 | DIRECT_IMPLEMENTATION | TC-08 | COVERED |
| AC9 | 010, 011 | TASK-17, -20 | DIRECT_IMPLEMENTATION | TC-09 | COVERED |
| AC10 | 015 | TASK-19, -20 | DIRECT_IMPLEMENTATION | TC-10 | COVERED |
| AC11 | 007, 009, 014 | TASK-16, -17, -19 | DIRECT_IMPLEMENTATION | TC-11 | COVERED |
| X1 | 004 | TASK-04, -05 | DIRECT_IMPLEMENTATION | TC-02 | COVERED |
| X2 | 003 | TASK-04, -05 | DIRECT_IMPLEMENTATION | TC-03 | COVERED |
| X3 | 016 | TASK-16, -17 | DIRECT_IMPLEMENTATION | TC-04, TC-32 | COVERED |
| X4 | 012 | TASK-18, -19 | DIRECT_IMPLEMENTATION | TC-05 | COVERED |
| X5 | 012 | TASK-18, -19 | DIRECT_IMPLEMENTATION | TC-06, TC-23 | COVERED |
| X6 | 014 | TASK-18, -19 | DIRECT_IMPLEMENTATION | TC-07 | COVERED |
| X7 | 010 | TASK-17 | DIRECT_IMPLEMENTATION | TC-09 | COVERED |
| X8 | 015 | TASK-19 | DIRECT_IMPLEMENTATION | TC-10, TC-19 | COVERED |
| X9 | 011, 020 | TASK-12, -13, -17 | DIRECT_IMPLEMENTATION | TC-24 (TC-12 Blocked, `OI-E1-042-001`) | COVERED |
| X10 | 009, 014 | TASK-16, -19 | DIRECT_IMPLEMENTATION | TC-11 | COVERED |
| FL1 | 003, 005 | TASK-03, -05 | INHERITED_EXISTING_BEHAVIOR | Merge review (`AGENTS.md` §8); TC-41, TC-42 | COVERED |
| FL2 | 005, 007 | TASK-07, -17 | DIRECT_IMPLEMENTATION | TC-26, TC-42 | COVERED |
| FL3 | 003, 004 | TASK-05 | DIRECT_IMPLEMENTATION | TC-02, TC-03, TC-21, TC-25 | COVERED |
| FL4 | 001, 006 | TASK-15 | DIRECT_IMPLEMENTATION | TC-13 | COVERED |
| FL5 | 012, 017, 021 | TASK-18, -19 | DIRECT_IMPLEMENTATION | TC-05, TC-16, TC-22 | COVERED |
| FL6 | 012 | TASK-18, -19 | DIRECT_IMPLEMENTATION | TC-05, TC-06, TC-23 | COVERED |
| FL7 | 014 | TASK-19 | DIRECT_IMPLEMENTATION | TC-07, TC-20 | COVERED |
| FL8 | 009, 018 | TASK-16, -17, -19 | DIRECT_IMPLEMENTATION | TC-11, TC-28 | COVERED |
| FL9 | 007 | TASK-07, -17 | DIRECT_IMPLEMENTATION | TC-26 | COVERED |
| FL10 | 011, 020 | TASK-17 | DIRECT_IMPLEMENTATION | TC-24, TC-31 | COVERED |
| PRE1 | 001 | TASK-00, TASK-15 | DIRECT_IMPLEMENTATION (repository precondition) | TC-13, TC-14 | COVERED |
| PRE2 | 003, 006 | TASK-03, TASK-15 | DIRECT_IMPLEMENTATION | TC-13, TC-41 | COVERED |
| PRE3 | 010, 002 | TASK-15, TASK-17 | DIRECT_IMPLEMENTATION | TC-09, TC-14 | COVERED |
| PRE4 | 020, 014 | TASK-13, TASK-19 | DIRECT_IMPLEMENTATION | TC-07, TC-24 (TC-12 Blocked, `OI-E1-042-001`) | COVERED |
| PRE5 | 003, 004 | TASK-05, TASK-22 | DIRECT_IMPLEMENTATION | TC-02, TC-03, TC-21, TC-25 | COVERED |
| ST1 | 012 | TASK-18, -19 | DIRECT_IMPLEMENTATION | TC-05, TC-16 | COVERED |
| ST2 | 014 | TASK-19 | DIRECT_IMPLEMENTATION | TC-07, TC-11 | COVERED |
| ST3 | 015 | TASK-19 | DIRECT_IMPLEMENTATION | TC-10, TC-19 | COVERED |
| AUTH | 020, 014, §16 | TASK-12, -13, -17, -19 | DIRECT_IMPLEMENTATION | TC-07, TC-24 | COVERED |
| CON1 | 011 | TASK-16, -17 | DIRECT_IMPLEMENTATION | TC-09, TC-31 | COVERED |
| CON2 | 012, 013, 017 | TASK-18, -19 | DIRECT_IMPLEMENTATION | TC-16, TC-17, TC-33 | COVERED |
| CON3 | 014, 015, 017, 025 | TASK-11, -18, -19 | DIRECT_IMPLEMENTATION | TC-29, TC-35, TC-36, TC-37, TC-38, TC-39 | COVERED |
| CON4 | 018 | TASK-19 | DIRECT_IMPLEMENTATION | TC-28 | COVERED |
| CON5 | 005, 007, 026 | TASK-07, -09, -17 | DIRECT_IMPLEMENTATION | TC-26, TC-42, TC-45 | COVERED |
| MSG | 022, 025 | TASK-10, -11, -13 | DIRECT_IMPLEMENTATION | TC-24, TC-29, TC-30 | COVERED |
| GR1 | 004 | TASK-04, -05 | DIRECT_IMPLEMENTATION | TC-02, TC-25 | COVERED |
| GR2 | 010, 027 | TASK-05, -11, -17, -19 | DIRECT_IMPLEMENTATION | TC-09, TC-29, TC-30, TC-40 | COVERED |
| GR3 | 026 | TASK-09, -17 | DIRECT_IMPLEMENTATION | TC-45, TC-46 | COVERED |
| GR4 | 009, 012, 003 | TASK-03, -05, -19 | DIRECT_IMPLEMENTATION | TC-16, TC-41 | COVERED |

No row is `BLOCKED`. TC-12 is a test blocked by later stories, not a requirement row; X9 is covered by the seam test TC-24, and TC-12 carries its own exit criterion in `tests/scenarios.md`.

## SPEC to task map

| SPEC | Tasks | Tests |
|---|---|---|
| 001 | TASK-14, -15 | TC-13, TC-14, TC-15 |
| 002 | TASK-14, -15, -17 | TC-13, TC-14, TC-27 |
| 003 | TASK-01, -02, -03, -04, -05 | TC-03, TC-21, TC-41, TC-44 |
| 004 | TASK-01, -02, -04, -05 | TC-02, TC-25, TC-43 |
| 005 | TASK-06, -07, -09, -17 | TC-04, TC-26, TC-27, TC-42 |
| 006 | TASK-14, -15 | TC-01, TC-13, TC-14, TC-27 |
| 007 | TASK-16, -17 | TC-01, TC-11 |
| 008 | TASK-15, -17 | TC-08 |
| 009 | TASK-16, -17, -19 | TC-11, TC-28 |
| 010 | TASK-17 | TC-09 |
| 011 | TASK-16, -17 | TC-09, TC-12 (Blocked), TC-24, TC-31 |
| 012 | TASK-18, -19 | TC-05, TC-06, TC-23 |
| 013 | TASK-18, -19 | TC-16, TC-17, TC-33 |
| 014 | TASK-18, -19 | TC-07, TC-20, TC-29, TC-36, TC-38 |
| 015 | TASK-19 | TC-10, TC-18, TC-19, TC-37, TC-39 |
| 016 | TASK-16, -17 | TC-04, TC-32 |
| 017 | TASK-09, -18, -19 | TC-05, TC-07, TC-10, TC-23, TC-35, TC-40 |
| 018 | TASK-19 | TC-28 |
| 019 | TASK-18, -19 | TC-29 |
| 020 | TASK-12, -13, -17 | TC-12 (Blocked), TC-24 |
| 021 | TASK-17, -20 | TC-22 |
| 022 | TASK-10, -11 | TC-30 |
| 023 | TASK-16, -17 | TC-11, TC-23, TC-46 |
| 024 | TASK-03, -07, -17 | TC-08, TC-26, TC-27 |
| 025 | TASK-11, -17 | TC-05, TC-34 |
| 026 | TASK-08, -09, -17 | TC-45, TC-46 |
| 027 | TASK-11, -17, -19, -25 | TC-09, TC-28, TC-29, TC-30, TC-40 |

No orphan: every SPEC 001 to 027 has at least one task.

## Screen-to-task mapping

`NOT_APPLICABLE`: UI In Scope NO, `DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SCREENS: 0]`, no effective-screen node and no `SCR-*` screen in the spec (`SCR-39` is Epic 8 and out of scope). No screen consolidation task is required; the pre-submit check in `tasks.md` records this.

## Security, privacy and compliance

- **Authentication and authorisation.** The one endpoint carries the method check through `CapabilityCheck.require` naming area "Rules and parameters" and right "R"; a refusal is 403 `MSG-P4-002` with the action text "read parameters" and no value in the body. The interim implementation is deleted by RWB-E1-037, which keeps the bean name `capabilityCheck`. The load, approve and rollback rights (Reference data C/A/U) are RWB-E1-043's check; this story enforces maker-checker inside the interface and in the database regardless of role.
- **Personal data.** `author_user_id`, `approver_user_id`, `created_by`, `updated_by` and the rollback caller are staff identifiers, treated as personal by the protective reading (`CLAR-024`, `CLAR-026`, gaps `E1042-SP-DG-15`, `-17`). They are stored in the two tables and passed only to `VersionDecisionRecorder`; they appear in no log line, event payload, exception message, `ParameterLoadResult` or response. Every test identity is a synthetic UUID; no name, ID number, account number or address appears in code, fixtures, logs or this plan.
- **Secrets.** `ace.db.password` is catalogued with `secret=true`, has no default and no value row, and is refused by the service, the reader and the endpoint. An ENV row may not name a credential-bearing property (the credential-name rule), so a secret cannot leak through the environment path either.
- **Audit.** Author, approver, both timestamps and the rollback reason are in `parameter_value`; `AC-VERS` is written inside the approval transaction through the recorder port, so a failure stops the approval (ADR-009). The access log is RWB-E1-039's and nothing is built for it here.
- **Database access.** Writes go only to `${recoverySchema}` through the recovery Flyway bean; the service reads only its own tables; no `public` table is read or written (D-RCV-35 U4, ADR-010, BND-6). No `GRANT`/`REVOKE` in the migration.
- **Logging.** Structured logs; message ID, check, status, `traceId` and cause **class** only; never a cause message, stack trace, placeholder, field value, user ID or secret (`D-RUN-15`, `SPEC-027`, §12.13).
- **KYC/AML, suitability, delegation of authority.** Not applicable: a parameter is not a credit decision (spec §16).

## Release and rollback

- **Release:** backend only, behind `rwb.p3.configservice` (default `false`, `true` in the local profile). Off, the service serves catalog defaults and ENV values with no database read, GET is 404, and no `ParameterLoadHandler` bean exists; the migration still runs (it is a schema change, not a behaviour change), and readiness checks defaults and ENV only. The orchestrator merges into `develop-recovery` only after `./scripts/dev.ps1 test` exits 0 and `./scripts/dev.ps1 it` exits 0.
- **Rollback:** turn the flag off, or revert the merge request. The migration is forward only and never edited; reverting the code leaves the tables and seed in place, which the previous tag ignores. `clean` stays disabled.
- **Release note item (for the deployer):** the migration creates two tables and seeds 19 catalog rows and 40 value rows on first start. A required `temporal.target` has no default, so an environment without the `rwb.temporal.target` property turns readiness DOWN (by design, `SPEC-016`).
- **Wave order:** RWB-E1-044 then RWB-TE-001 merge first; this story's code gate runs after them (D-RUN-17). The `<seq>` number is assigned at merge.

Nothing in this plan, `tasks.md` or the supporting files claims a human approval or a ratification of D-RUN-18 to D-RUN-21.

## Assumptions

Plan-stage assumptions are in `assumptions.md` (`PA-E1-042-01` to `PA-E1-042-17`). Spec assumptions A-01 to A-56 are carried unchanged and are not re-litigated here.

## Status

```text
PLANNER_STATUS_SUMMARY: Plan ready: 26 tasks (TASK-00..TASK-25) for the catalog file and its two build checks, the generated typed keys, the published P3 and P4 interfaces, the problem and message seams, one guarded migration with its 19-row catalog and 40-row value seed, the read service with its cache, the catalog endpoint and readiness, the load/approve/rollback handler, the flag, the coverage wiring and the gates.
PLANNER_STATUS_DETAIL: SUCCESS [REASON: spec revision 13 passed the gate 0/0/0/0; RWB-TE-001 plan v7 and RWB-E1-044 plan v1 used as the base; every SPEC, AC, BR and exception row mapped to tasks and named tests] [UNBLOCK_ACTION: n/a]
PLANNER_CLARIFICATION_STATUS: READY [OPEN_ITEMS: 25] [UNBLOCK_ACTION: n/a - 25 OPEN items each carry a labelled default in ../specify/assumptions.md; spec gate 12 records BLOCKING: 0; CLAR-025 and CLAR-027 are SETTLED by unratified D-RUN-21 and D-RUN-20 and are not treated as ratified]
PLANNER_DESIGN_SOURCE: NOT_REQUIRED [NOTE: UI In Scope NO; no screen, route or component change; no Figma link needed]
PLAN_REQUIREMENT_COVERAGE_SUMMARY: All 57 requirement-logic rows, SPEC-001 to SPEC-027 and TC-E1-042-01 to TC-E1-042-46 map to tasks and named tests; TC-E1-042-12 stays Blocked with its exit criterion and is not counted as passed.
PLAN_REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 57] [TASK_COVERED_RULES: 57] [MISSING_TASK_RULES: 0] [AMBIGUOUS_TASK_RULES: 0] [CONTRADICTIONS: 0]
GATE_REVIEW: PENDING_ORCHESTRATOR
```
