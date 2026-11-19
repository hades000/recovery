---
title: "Tasks: RWB-TE-001 Recovery module folder and boundary test"
run_id: "INC-002-epic-1-RWB-TE-001"
story: "RWB-TE-001"
revision: "v1 (18 Nov 2026)"
---

# Tasks: RWB-TE-001

Source: `plan.md` v1 and `../specify/spec.md` v4. Paths as in `plan.md` (`R` = `backend/src/main/java/th/co/scb/ace/demo/recovery`, `T` = `backend/src/test/java/th/co/scb/ace/demo/recovery`, `F` = `backend/src/test/java/th/co/scb/ace/boundaryfixture`). Commands run from the worktree root; Gradle commands run in `backend/` with the `JAVA_TOOL_OPTIONS` of RUN-BRIEF. Every red run and every green run is saved under `implement/` as command, exit code and the first failing or final summary line.

Test-first order: TASK-01, -03, -06, -09 and -10 are red before TASK-04, -07 and -11 make them green (AGENTS.md rules 3 and 10). TASK-08 and TASK-15 prove behaviour that Spring Modulith and the ESLint config already have; their breaking fixtures show the rule fires. TASK-12 adds characterization tests for unchanged behaviour at the new homes (PA-07).

## Backend Plan

Unit tests: **REQUIRED** (Trace: SPEC-001..-012, -017, -018, -020, -022..-026). Gate: `./gradlew test recoveryCoverageVerification`, LINE, INSTRUCTION, BRANCH, METHOD ≥ 0.80 (SPEC-020). Tasks TASK-00..TASK-14, TASK-17, TASK-18.

## Frontend Plan

Unit tests: **REQUIRED** (Trace: SPEC-013..-015, -020). Gate: inherited Vitest v8 thresholds 80 × 4 in `frontend/vite.config.ts`, run by `npm run check`. No API contract consumed, so no frontend task waits on a backend contract task. Tasks TASK-15, TASK-16, and TASK-17 run 2.

## Task table

| Task | Description | Files | Trace | BLOCKED_BY | Verification |
|---|---|---|---|---|---|
| TASK-00 | **Pre-flight on the worktree base.** (1) List every file under `R/platform`, `R/rules`, `R/workflow`, `R/documents` and compare with the `plan.md` Relocation table (35 files on 18 Nov 2026). Any extra class from an earlier merged story (for example RWB-E1-044) moves by the same table, or to its own story v7 §13 home; if neither covers it, stop and report (SPEC-022 (g)). (2) Confirm `org.yaml:snakeyaml`, `archunit`, `spring-modulith-core`, `jakarta.persistence-api`, `spring-data-commons`, `mockito-core` on `testCompileClasspath`. (3) Run `./gradlew test recoveryCoverageReport` and save the baseline counters. | none (read only) | SPEC-017, -022 (g); [AUD] A-01 | NONE | `./gradlew --offline -q dependencies --configuration testCompileClasspath` lists the six; file listing saved to `implement/backend/preflight.txt`; baseline `test` exit 0 and counters LINE 133/415, BRANCH 25/92, INSTRUCTION 686/2174, METHOD 41/135 (or the worktree's own numbers, recorded) |
| TASK-01 | **Coverage gate (red).** Edit only the two JaCoCo tasks in `backend/build.gradle.kts`: add `boundaryToolingClasses` (test output, include `th/co/scb/ace/demo/recovery/architecture/boundary/**`, exclude `**/*Test.class`, `**/*Test$*.class`); `classDirectories.setFrom(recoveryClasses, boundaryToolingClasses)` on both; add test `java.srcDirs` to `sourceDirectories`; limits LINE, INSTRUCTION, BRANCH, METHOD at `0.80`; update the description. Execution data, `finalizedBy` and `check` wiring unchanged. | `backend/build.gradle.kts` | SPEC-020; T-TE001-10 | TASK-00 | `./gradlew test recoveryCoverageVerification` exits non-zero at baseline with "Rule violated for bundle" naming the counters below 0.80 (expected red); `./gradlew check` does not run either task (task graph `--dry-run`) |
| TASK-02 | **Real module map.** Write `recovery-modules.yaml` exactly as `../specify/contracts/backend-apis.json` `initialContent` (19 modules, `external` common and collection, 16 `clientLibraries`); no `sourceViews` key. Header comment: story key, D-RCV-37, "change by merge request". | `backend/src/test/resources/architecture/recovery-modules.yaml` | SPEC-002, -025; BR6 | TASK-00 | Parsed by TASK-03 `loadsTheRealMap` (19 modules, P1..P10 and S1..S9, published lists of `data-model.md` §1) |
| TASK-03 | **Loader tests (red).** `ModuleMapLoaderTest` cases of `tests/scenarios.md` T-TE001-01 (valid inline map, real map, `sourceViews` carried opaque, missing file, invalid YAML, duplicate YAML key, missing field, empty `published`, duplicate code, duplicate name, bad code / name / package pattern, `internal` and `internal.x` as published, unknown top-level and nested key, `external` not common and collection, empty or repeated `clientLibraries`). Inline maps written to `@TempDir`. Each error asserts the message starts with the file name and contains the field path. | `T/architecture/boundary/ModuleMapLoaderTest.java` | SPEC-003; BR6; T-TE001-01 | TASK-02 | `./gradlew test --tests "*ModuleMapLoaderTest"` fails to compile (no `ModuleMapLoader`): red recorded |
| TASK-04 | **Loader and model (green).** `ModuleMap` records and `ModuleMapLoader` as `plan.md` "Tooling design": SnakeYAML `SafeConstructor`, `LoaderOptions.setAllowDuplicateKeys(false)`, `IllegalStateException` text `{file}: {fieldPath}: {problem}`, immutable lists, no package literal. | `T/architecture/boundary/ModuleMap.java`, `ModuleMapLoader.java` | SPEC-003; BR6 | TASK-03 | `./gradlew test --tests "*ModuleMapLoaderTest"` green |
| TASK-05 | **Fixture worlds.** Fixture classes, `package-info.java` and fixture maps of `data-model.md` §3 (worlds `passing`, `bnd1`, `bnd2`, `bnd4`, `bnd5`, `vendorx`, `mapbad`, `bnd3fail`, `bnd3pass`, `bnd3cycle`). AC class names (`SampleService`, `CollectorRepository`, `DecisionLogRepository`, `DecisionLogWriter`, `RecoveryCaseEntity`, `vendorx`). Every fixture `@NamedInterface` declares `propagate = false`, except `mapbad` `casewf.timers` which keeps the default (R3-4). Each fixture class has a Javadoc line naming RWB-TE-001 and its purpose. No business value, no personal data. | `F/**`, `backend/src/test/resources/architecture/fixtures/*.yaml` | SPEC-011, -019; §17 guardrails | TASK-00 | `./gradlew compileTestJava` green; review in TASK-18 |
| TASK-06 | **Rule tests (red).** `BoundaryRulesTest`: for each world, import `ClassFileImporter().importPackages(<world root>)` (test classes included), load the world map, evaluate the rule under test, assert the exact SPEC-010 / SPEC-004 lines (scenarios TC-TE-001-01, -02, -04, -05, -07; T-TE001-02, -03, -04, -09; `commonInternalDependencyBreaksBnd2`; `matchesClientLibrary` table test; T-TE001-15 source scan). | `T/architecture/boundary/BoundaryRulesTest.java` | SPEC-004..-006, -008..-011; AC1, AC2, AC4, AC5, AC7; BR1, BR2, BR4..BR6 | TASK-04, TASK-05 | `./gradlew test --tests "*BoundaryRulesTest"` fails to compile (no `BoundaryRules`): red recorded |
| TASK-07 | **Rule factory (green).** `BoundaryRules.all(map)` with `moduleMap`, `bnd1`, `bnd2`, `bnd4`, `bnd5` and `matchesClientLibrary`, as `plan.md` "Tooling design" and `data-model.md` §4. One line per violation, all violations of a rule in one evaluation; BND-1 and BND-2 `allowEmptyShould(true)`; no package literal. | `T/architecture/boundary/BoundaryRules.java` | SPEC-004..-006, -008..-010; BR1, BR2, BR4..BR6 | TASK-06 | `./gradlew test --tests "*BoundaryRulesTest" --tests "*ModuleMapLoaderTest"` green |
| TASK-08 | **BND-3 fixtures.** `ModulithFixtureTest`: `ApplicationModules.of("th.co.scb.ace.boundaryfixture.<world>", location -> true)` for `bnd3fail` (`verify()` throws `Violations`; message names `DecisionLogRepository`), `bnd3pass` (`verify()` passes; `DecisionLogWriter` in named interface `writer`), `bnd3cycle` (`verify()` throws on the cycle). First run settles PA-09: if the fixtures are not imported (no module detected), stop and report before TASK-11 (SPEC-007 stop rule). | `T/architecture/boundary/ModulithFixtureTest.java` | SPEC-007, -011; AC3; BR3; T-TE001-16 | TASK-05 | `./gradlew test --tests "*ModulithFixtureTest"` green; the module list printed by the test shows `recovery`, `recovery.integration`, `recovery.decision` for each world |
| TASK-09 | **`RecoveryBoundaryTest` on the real code (red).** As `plan.md` "`RecoveryBoundaryTest` changes": load the real map, add `moduleMapRule`, `bnd1CollectionBoundary`, `bnd2CommonBoundary`, `bnd4EntitiesAndRepositoriesStayInTheirModule`, `bnd5ClientLibrariesOnlyInClientPackages`, `everyMapModuleHasApiAndInternalPackageInfo`, `publishedSurfaceIsExactlyTheSpecifiedTypes`; delete `blobClientOnlyInDocumentsModule`; retarget `workflowImplementationsAreDeterministic` to `.casewf.workflow..`; keep `noRecoveryClassNamesAPublicTable` unchanged. | `T/architecture/RecoveryBoundaryTest.java` | SPEC-001, -004, -009, -025, -026; BR1..BR6; T-TE001-05, -14 | TASK-07 | `./gradlew test --tests "*RecoveryBoundaryTest"` red on the baseline packages: `moduleMapRule` reports `package th.co.scb.ace.demo.recovery.platform is not in the module map` (and `rules`, `workflow`, `documents`); `everyMapModuleHasApiAndInternalPackageInfo` and the published-surface test fail |
| TASK-10 | **Binding tests (red).** The T-TE001-12 methods only, in `PlatformConfigTest`, `PlatformInfoControllerTest`, `RecoveryFlywayConfigTest`, `SecurityConfigTest` and `DroolsPropertiesTest` at the new paths: bind each new record from the real `application.yaml` through `ApplicationContextRunner` + `ConfigDataApplicationContextInitializer` and assert the default values listed in `tests/scenarios.md` T-TE001-12 (the values `RecoveryProperties` binds today). | the five test classes (paths in `plan.md` "Coverage tests") | SPEC-023; T-TE001-12; plan input R2-4 | TASK-00 | `./gradlew compileTestJava` fails (records and new packages missing): red recorded |
| TASK-11 | **Skeleton, relocation and property split (green).** (1) 61 `package-info.java` of SPEC-001 (`data-model.md` §2). (2) Move 26 main classes and 4 test classes as the `plan.md` tables, changing only `package` / `import` lines, the two visibility changes (`PdpaPayloadCodec` pp, `TemporalProperties` public) and the two `DroolsRuleEngineTest` workbook rows. (3) Add the four property records, each with its own `@EnableConfigurationProperties` registration, replace `RecoveryProperties` reads, delete `RecoveryProperties`. (4) Delete the 8 old `package-info.java` and the empty folders. `TemporalConfig.pdpaPayloadCodec` stays in the same package with `proxyBeanMethods = false` (R3-5). | `R/**`, `T/casewf/**` (moved tests) | SPEC-001, -022, -023, -025; ASM-01..-04, -09 | TASK-09, TASK-10 | `./gradlew test --tests "*RecoveryBoundaryTest" --tests "th.co.scb.ace.demo.ModulithTest"` green; TASK-10 binding tests green; moved tests green with unchanged assertions |
| TASK-12 | **Coverage tests (SPEC-024).** Remaining methods of the 11 classes in `plan.md` "Coverage tests" (`ApiErrorTest`, `ApiExceptionHandlerTest`, `SecurityConfigTest`, `PlatformConfigTest`, `PlatformInfoControllerTest`, `RecoveryFlywayConfigTest`, `TemporalAdminControllerTest`, `TemporalConfigTest`, `WorkflowIdsTest`, `BlobDocumentStoreTest`, `DroolsPropertiesTest`). Synthetic data only; mocks for JDBC, Temporal stubs, Blob clients and `JwtDecoder`; no network, Docker or database. Any class still under 0.80 gets a test at its home; no exclusion, no threshold change. | `T/access/**`, `T/integration/**`, `T/casewf/**`, `T/dochub/**` | SPEC-024; T-TE001-10; [TS] §1 | TASK-11 | `./gradlew test` green; `recoveryCoverageReport.xml` per-class counters reviewed |
| TASK-13 | **Backend gate run.** (1) `./gradlew test` (T-TE001-06): whole suite green, including `ModulithTest`, `RecoveryMigrationLintTest`, moved tests. (2) Old-package search (T-TE001-06): `grep -rnE "th\.co\.scb\.ace\.demo\.recovery\.(platform|rules|workflow|documents)\b" backend/src` finds nothing, and the four folders under `R` and `T` are gone. (3) `./gradlew test recoveryCoverageVerification` (T-TE001-10), run and shown separately from `dev.ps1 test` (R3-3). | none (runs) | SPEC-007, -018, -020, -022 (f), -024 | TASK-01, TASK-08, TASK-12 | (1) exit 0; (2) no match; (3) exit 0 with LINE, INSTRUCTION, BRANCH, METHOD each ≥ 80% as printed; XML and HTML report saved to `implement/backend/coverage/` |
| TASK-14 | **Integration and e2e regression.** `./gradlew recoveryIntegrationTest` (Docker; `RecoveryDatabaseIT`, D-RCV-44, SPEC-022 (h)); `./scripts/dev.ps1 up`, `./scripts/dev.ps1 backend`, `./gradlew e2eTest` (`PlatformE2ETest`: `/platform/info`, `/admin/temporal/health`, smoke). | none (runs) | SPEC-018, -022 (e), (h); T-TE001-11; FTS-01..-03 | TASK-13 | both exit 0; logs saved to `implement/backend/it.log` and `implement/backend/e2e.log` |
| TASK-15 | **Frontend fixture test.** `importBoundary.test.ts` as `plan.md` "Frontend Plan": `// @vitest-environment node`, real `eslint.config.js` through `new ESLint({ cwd })`, `lintText` with `filePath` `src/modules/recovery/caselist/BoundaryFixture.tsx`, the 8 rejected and 7 allowed imports of SPEC-015, `ruleId === "no-restricted-imports"`, guarded `results[0]`, 30 000 ms timeout. | `frontend/src/modules/recovery/__tests__/importBoundary.test.ts` | SPEC-014, -015; AC6; TC-TE-001-06; T-TE001-07 | NONE | `npx vitest run src/modules/recovery/__tests__/importBoundary.test.ts` green (15 cases: each of the 8 rejected imports reports `no-restricted-imports`, none of the 7 allowed does) |
| TASK-16 | **Frontend gate run.** `npm run check` (typecheck, lint, coverage) and `npm run build` in `frontend/`. | none (runs) | SPEC-013, -014, -018, -020; T-TE001-08 | TASK-15 | both exit 0; coverage summary at or above 80 on lines, statements, branches, functions, as printed; `coverage-summary.json` saved |
| TASK-17 | **Negative control of the local merge gate (T-TE001-13).** Three runs of `powershell -NoProfile -File scripts/dev.ps1 test`, recording `$LASTEXITCODE` after each (R3-2). Run 1: uncommitted `R/casewf/internal/BoundaryProbe.java` with a `java.net.http.HttpClient` field. Run 2: backend probe removed; uncommitted `frontend/src/modules/recovery/caselist/BoundaryProbe.tsx` with `import "@/auth/auth";`. Run 3: both removed. | probes only, never committed | SPEC-012 (b); Flow 6; §13 step 7 | TASK-13, TASK-16 | Run 1 exit ≠ 0 and the log line `Rule BND-5 broken: th.co.scb.ace.demo.recovery.casewf.internal.BoundaryProbe depends on java.net.http.HttpClient`; Run 2 Gradle green, `no-restricted-imports` on `BoundaryProbe.tsx`, exit ≠ 0; Run 3 exit 0; `git status --porcelain` shows neither probe; evidence in `implement/merge-gate.md`. HV-01 stays open (not tested). |
| TASK-18 | **Scope, guardrail and evidence check.** (1) Diff touches only the files in `plan.md` (backend list, frontend list); shared file edited: `backend/build.gradle.kts` only; no change to `.gitlab-ci.yml`, `scripts/dev.ps1`, `application*.yaml`, `db/**`, `frontend/package*.json`, `eslint.config.js`, `vite.config.ts`, `tsconfig.json`. (2) No new dependency (diff of `dependencies` output before and after). (3) SPEC-016: no `RecoveryAccessGuard`, no test-only Case record endpoint, no new `MSG-P4-002` use, no BND-6 or `sourceViews` validation, no pipeline change. (4) SPEC-019: maps, fixtures and failure texts hold class and package names only. (5) Unit-test results table (one row per surface) with the native reports. | `implement/` evidence only | SPEC-016, -017, -019; [IEG] | TASK-14, TASK-17 | checklist in `implement/scope-check.md` all ticked with the command output that proves each |

## Scope bullet to task map

| Scope bullet (`plan.md`) | Tasks |
|---|---|
| S-1 Module skeleton | TASK-11 |
| S-2 Relocation | TASK-00, TASK-11 |
| S-3 Property split | TASK-10, TASK-11 |
| S-4 Module map | TASK-02 |
| S-5 Map loader | TASK-03, TASK-04 |
| S-6 Map-driven rules | TASK-06, TASK-07 |
| S-7 Fixtures | TASK-05 |
| S-8 BND-3 proof | TASK-08, TASK-13 |
| S-9 `RecoveryBoundaryTest` | TASK-09 |
| S-10 Coverage gate | TASK-01, TASK-13 |
| S-11 Coverage tests | TASK-12 |
| S-12 Frontend fixture test | TASK-15, TASK-16 |
| S-13 Regression | TASK-13, TASK-14, TASK-16 |
| S-14 Merge gate | TASK-17 |
| S-15 Guardrails, exclusions, evidence | TASK-18 |

## Dependency graph

```text
TASK-00 ─┬─ TASK-01 ────────────────────────────────┐
         ├─ TASK-02 ─ TASK-03 ─ TASK-04 ─┐          │
         ├─ TASK-05 ─────────────────────┼─ TASK-06 ─ TASK-07 ─ TASK-09 ─┐
         │        └─ TASK-08 ───────────────────────┤                    │
         └─ TASK-10 ────────────────────────────────┼────────────────────┴─ TASK-11 ─ TASK-12 ─┐
                                                    └──────────────────────────────────────── TASK-13 ─ TASK-14 ─┐
TASK-15 ─ TASK-16 ─────────────────────────────────────────────────────────────── TASK-17 (needs TASK-13) ─ TASK-18
```

No cycle. TASK-15 and TASK-16 run in parallel with the backend tasks.

## Pre-submit checks

- [x] Every scope bullet S-1..S-15 in `plan.md` maps to at least one `TASK-*` (table above).
- [x] Every active SPEC (001..020, 022..026) maps to at least one task (`plan.md` "SPEC to task map"); SPEC-021 is withdrawn in the spec and has no task; no orphaned `SPEC-*` mapping.
- [x] Every AC (AC1..AC7) and BR (BR1..BR6) maps to tasks and to a named test (`tests/scenarios.md`); X7 / TC-TE-001-08 shown as moved out of scope and checked by TASK-18.
- [x] Every task has a Description, Trace, `BLOCKED_BY` (explicit `NONE` for TASK-00 and TASK-15) and Verification.
- [x] Effective-screen node groups: `NOT_APPLICABLE` (UI In Scope NO, `DESIGN_EVIDENCE_STATUS: NOT_REQUIRED`); no unmapped screen.
- [x] Frontend and backend unit-test applicability recorded as `REQUIRED` with trace and reason in `plan.md` and above.
- [x] Tests precede code: red runs in TASK-01, -03, -06, -09, -10 before TASK-04, -07, -11.
- [x] No migration (D-RUN-07 not exercised); no new dependency; one shared file edited (`backend/build.gradle.kts`).
- [x] Later-story work is a named seam only (SPEC-016 list); no dependency on an unmerged story (D-RUN-08).
- [x] No test is skipped or weakened: `blobClientOnlyInDocumentsModule` is replaced by the stricter BND-5; moved tests keep their assertions.
