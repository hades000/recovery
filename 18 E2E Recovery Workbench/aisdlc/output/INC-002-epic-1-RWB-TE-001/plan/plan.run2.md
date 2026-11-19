---
title: "Implementation Plan: RWB-TE-001 Recovery module folder and boundary test"
run_id: "INC-002-epic-1-RWB-TE-001"
story: "RWB-TE-001"
epic: "EPIC-001"
status: "SUCCESS"
revision: "v2 (18 Nov 2026): plan gate round 1 findings PLAN-001..007 fixed; v1 kept as plan.run1.md. Planned against spec v4 (spec gate round 5 PASS)"
prepared: "2026-11-18"
---

# Implementation Plan: RWB-TE-001 Recovery module folder and boundary test

Design Source: `NOT_REQUIRED` (UI In Scope: NO; `DESIGN_EVIDENCE_STATUS: NOT_REQUIRED` in spec.md).

| Field | Value |
|---|---|
| Spec | `../specify/spec.md` v4. Spec gate round 5: `PASS` 0/0/0/0 (`../review/spec-gate-review-5.md`). `Status: SUCCESS`; `REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 13] [MISSING_RULES: 0] [CONTRADICTIONS: 0]`. |
| Carried plan inputs | Spec gate round 3 "Plan inputs" 1–6 and round 2 plan inputs 1–5 and 7 (table "Carried plan inputs" below). Round-1 plan inputs 1–11 are already in the spec; the relevant ones are applied again where they name a file. |
| Code base | This repository as read on 18 Nov 2026 (`backend/`, `frontend/`, `scripts/dev.ps1`, `.gitlab-ci.yml`). No git run, no file outside `plan/` and `review/` written. |
| Builder | Implementation Builder, in its own git worktree on `feature/RWB-TE-001-module-boundary` from `develop-recovery`; commits `RWB-TE-001: <summary>` with the `AISDLC-Run` and `AISDLC-Plan` trailers (CLAUDE.md). |
| Smallest change | Extend `RecoveryBoundaryTest` and keep `ModulithTest` unchanged; one tooling package (three test-scope classes); move classes without behaviour change; one shared file edited (`backend/build.gradle.kts`); one frontend test file. No new dependency, endpoint, migration, pipeline, script or frontend config change. |

## Upstream readiness

| Check | Result |
|---|---|
| Spec status | `SUCCESS` (spec front matter and "Status reporting") |
| Spec gate | `PASS` round 5, no open finding |
| `REQUIREMENT_COVERAGE_RESULT` | `MISSING_RULES: 0`, `CONTRADICTIONS: 0` |
| Clarification log | CLAR-001..-016 all `RESOLVED` (CLAR-007 resolved by moving out of scope, CLAR-013/-014 by labelled assumption, CLAR-016 with HV-01 open for a human). No `OPEN` row. |
| Design evidence | `NOT_REQUIRED` (UI In Scope NO): no screen tasks, no `frontend/components.md`. |
| Migration | None. D-RUN-07 not exercised. |

`PLANNER_CLARIFICATION_STATUS: READY [OPEN_ITEMS: 0] [UNBLOCK_ACTION: n/a]`. The two spec open items (SU-02, SU-13) are shared open-item rows, not `CLAR-*` items; neither blocks.

## Scope

In scope (each bullet maps to tasks in `tasks.md`):

1. **S-1 Module skeleton:** 19 module packages with `api` and `internal` `package-info.java`, plus the four other initial published packages (SPEC-001). → TASK-11
2. **S-2 Relocation:** every class of `platform`, `rules`, `workflow`, `documents` moves to its design home, with the two visibility changes; the four packages are deleted (SPEC-022, SPEC-025). → TASK-00, TASK-11
3. **S-3 Property split:** `RecoveryProperties` replaced by four package-private records binding the same keys (SPEC-023). → TASK-10, TASK-11
4. **S-4 Module map:** `backend/src/test/resources/architecture/recovery-modules.yaml` (SPEC-002). → TASK-02
5. **S-5 Map loader:** test-scope `ModuleMapLoader` and its model (SPEC-003). → TASK-03, TASK-04
6. **S-6 Map-driven rules:** module-map rule, BND-1, BND-2, BND-4, BND-5 with the SPEC-010 failure text (SPEC-004..-006, -008..-010). → TASK-06, TASK-07
7. **S-7 Fixtures:** backend fixture worlds and fixture maps (SPEC-011). → TASK-05
8. **S-8 BND-3 proof:** Modulith fixture worlds; `ModulithTest` unchanged (SPEC-007). → TASK-08, TASK-13
9. **S-9 `RecoveryBoundaryTest` on the real code:** rules from the real map, Blob literal rule replaced, determinism rule retargeted, published surface test (SPEC-026, SPEC-025). → TASK-09
10. **S-10 Coverage gate:** four JaCoCo counters at 0.80 and the tooling class directory (SPEC-020). → TASK-01, TASK-13
11. **S-11 Coverage tests** for the relocated classes (SPEC-024). → TASK-12
12. **S-12 Frontend fixture test** for the D-RCV-39 rule (SPEC-013..-015). → TASK-15, TASK-16
13. **S-13 Regression** of unit, Modulith, migration lint, integration, e2e and frontend checks (SPEC-018). → TASK-13, TASK-14, TASK-16
14. **S-14 Merge gate:** negative control on `./scripts/dev.ps1 test` (SPEC-012 (b)); HV-01 left open (SPEC-012 (c)). → TASK-17
15. **S-15 Guardrails, scope exclusions and evidence** (SPEC-016, -017, -019). → TASK-18

Out of scope (SPEC-016): `RecoveryAccessGuard` and TC-TE-001-08 (RWB-E1-022, D-RCV-52), pipeline changes (D-RCV-05), code owners (RWB-TE-002), OpenAPI types and contract tests (RWB-TE-003), common and collection internals (DL05 option A), the adapter pattern (RWB-E1-007), the agent client (RWB-TE-013), BND-6 and `sourceViews` validation (RWB-E1-069), `TimerScheduler` / `RuleEngine` signature alignment (RWB-E1-028, RWB-E1-072). Each is a seam owned by a later story (D-RUN-08) and is not built.

**One-module reading (round 2, plan input 7).** AGENTS.md §7 and §9 ask that a plan "touches one module". This plan reads "module" as the ACE module, the recovery module, as AGENTS.md §2–§3 do. The story itself creates all 19 nested design modules ([S] §13 step 1) and the relocation moves code into P2, P3, P4 and P5, all inside `th.co.scb.ace.demo.recovery`. No common, collection or other ACE module is touched.

## Carried plan inputs

| Input | Content | Where applied |
|---|---|---|
| R3-1 | Modulith 2.1.1 always adds the unnamed base-package interface. Filter `isUnnamed()`; do not assert an exact set of four. | T-TE001-14 (`publishedSurfaceIsExactlyTheSpecifiedTypes`), TASK-09; PA-05 |
| R3-2 | Run `powershell -NoProfile -File scripts/dev.ps1 test` and record the process exit code. | T-TE001-13, TASK-17 |
| R3-3 | `dev.ps1 test` does not run `recoveryCoverageVerification`; show T-TE001-10 separately. | TASK-13 (separate command and evidence) |
| R3-4 | Fixture `package-info` files declare `propagate = false`, except the fixture that tests the default. | TASK-05 (all fixture worlds), world `mapbad` (`casewf.timers` keeps the default) |
| R3-5 | `PdpaPayloadCodec` narrowing: keep `TemporalConfig.pdpaPayloadCodec` in the same package with `proxyBeanMethods = false`. | TASK-11 (both in `casewf.workflow.internal`; `TemporalConfig` already `proxyBeanMethods = false`) |
| R3-6 / R2-6 | `@NamedInterface(name = …, propagate = false)` exists in Spring Modulith 2.1.1. | Verified at plan time with `javap` on `spring-modulith-api-2.1.1.jar`: members `value()`, `name()`, `propagate()`. |
| R2-1 | Vitest: `// @vitest-environment node` docblock and a timeout covering the first load of `typescript-eslint`. | TASK-15 (docblock; `testTimeout` 30 000 ms on the `describe`) |
| R2-2 | Assert on `ruleId === "no-restricted-imports"` for both sets. | TASK-15 |
| R2-3 | `noUncheckedIndexedAccess`: guard `results[0]`. | TASK-15 |
| R2-4 | Each SPEC-023 record needs its own `@EnableConfigurationProperties` registration. | TASK-11 (table "Property split") |
| R2-5 | TC-TE-001-03 fixture tree mirrors the real nesting: fixture `recovery` package with `@ApplicationModule`, nested `integration` and `decision` with `@ApplicationModule`. | TASK-05 worlds `bnd3fail`, `bnd3pass`, `bnd3cycle` |
| R2-7 | One-module reading stated in the plan. | "Scope" above |

## Plan-time verification (read only)

| Item | Command or source | Result (18 Nov 2026) |
|---|---|---|
| SnakeYAML for the loader | `./gradlew --offline -q dependencies --configuration testCompileClasspath` (with `JAVA_TOOL_OPTIONS` per RUN-BRIEF) | `org.yaml:snakeyaml:2.6` present (through Spring Boot). Also `archunit 1.5.1`, `spring-modulith-core 2.1.1`, `spring-data-commons 4.1.2`, `jakarta.persistence-api 3.2.0`, `mockito-core 5.23.0`. No new dependency. |
| Modulith imports test-scope fixtures (SPEC-007 stop rule, ASM-05) | `javap -c` on `spring-modulith-core-2.1.1.jar`, `ApplicationModules.of(String, ImportOption)` | The private constructor passes the given `ImportOption` to `ClassFileImporter.withImportOption` and adds nothing else; `DoNotIncludeTests` is only the default of the overloads without an option. An option that accepts every location imports fixtures. The stop rule does not fire. TASK-08 confirms on first run. |
| `NamedInterface` API in core | `javap` on `org.springframework.modulith.core.NamedInterface`, `ApplicationModule` | `getName()`, `isUnnamed()`, `ApplicationModule.getNamedInterfaces()`, `getBasePackage()` exist (T-TE001-14). |
| Quartz job store (ASM-06) | `backend/src/main/resources/application.yaml` | `spring.quartz.job-store-type: memory`. No persisted recovery job exists in this repository; the `TimerDueJob` rename needs no data step. |
| Old-package references outside Java | search of `*.md`, `*.yaml`, `*.yml`, `*.kts`, `*.ps1`, `*.json` (excluding `aisdlc/output`, increment cards, `node_modules`) for `recovery.platform`, `recovery.rules`, `recovery.workflow` or `recovery.documents` | None. Only Java files and the `DroolsRuleEngineTest` workbook strings name the old packages. |
| Earlier story code in the four packages (SPEC-022 (g)) | file listing of `backend/src/main/java/th/co/scb/ace/demo/recovery/` | 35 files: 27 classes and 8 `package-info.java`, all in the Relocation table. RWB-E1-044 (build order 1) is specified but not merged. TASK-00 repeats the check on the worktree base. |
| Frontend probe target for T-TE001-13 | `frontend/src/auth/auth.tsx` | Exists, so `import "@/auth/auth";` type-checks and only `lint` fails. |

## Backend Plan

Surface status: **CHANGED**. Unit tests **REQUIRED** (80% LINE, INSTRUCTION, BRANCH, METHOD at bundle level over all of `th/co/scb/ace/demo/recovery/**` main classes plus the tooling package).

### Files added or changed (backend)

Paths are relative to the repository root. `R` = `backend/src/main/java/th/co/scb/ace/demo/recovery`, `T` = `backend/src/test/java/th/co/scb/ace/demo/recovery`, `F` = `backend/src/test/java/th/co/scb/ace/boundaryfixture`.

| Kind | Path | Task | SPEC |
|---|---|---|---|
| Edit | `backend/build.gradle.kts` (the two JaCoCo tasks only) | TASK-01 | 020 |
| Add | `backend/src/test/resources/architecture/recovery-modules.yaml` | TASK-02 | 002 |
| Add | `T/architecture/boundary/ModuleMap.java` (model records) | TASK-04 | 003 |
| Add | `T/architecture/boundary/ModuleMapLoader.java` | TASK-04 | 003 |
| Add | `T/architecture/boundary/BoundaryRules.java` (rule factory) | TASK-07 | 004..006, 008..010 |
| Add | `T/architecture/boundary/ModuleMapLoaderTest.java` | TASK-03 | 003 |
| Add | `T/architecture/boundary/BoundaryRulesTest.java` | TASK-06 | 004..006, 008..011 |
| Add | `T/architecture/boundary/ModulithFixtureTest.java` | TASK-08 | 007, 011 |
| Add | `F/<world>/…` fixture classes and `package-info.java` (worlds in `data-model.md` §3) | TASK-05 | 011 |
| Add | `backend/src/test/resources/architecture/fixtures/<world>.yaml` (8 maps; `data-model.md` §3) | TASK-05 | 011 |
| Edit | `T/architecture/RecoveryBoundaryTest.java` | TASK-09 | 026, 025, 001, 009 |
| Unchanged | `backend/src/test/java/th/co/scb/ace/demo/ModulithTest.java`, `T/architecture/RecoveryMigrationLintTest.java`, `T/RecoveryDatabaseIT.java`, `backend/src/test/java/th/co/scb/ace/demo/e2e/PlatformE2ETest.java` | — | 007, 018 |
| Move + edit | 26 main class files moved; 8 `package-info.java` and `RecoveryProperties.java` deleted (Relocation table below) | TASK-11 | 022, 023 |
| Add | 61 `package-info.java` (19 × module, `api`, `internal`; plus `casewf/rules`, `casewf/timers`, `casewf/workflow`, `integration/flags/api`) | TASK-11 | 001 |
| Add | 4 property records (table "Property split") | TASK-11 | 023 |
| Move | 4 test files (table "Tests that move") | TASK-11 | 022 (f) |
| Add | 11 coverage and binding test classes (table "Coverage tests") | TASK-10, TASK-12 | 023, 024 |

Not changed: `.gitlab-ci.yml`, `scripts/dev.ps1`, `application.yaml`, `application-local.yaml`, `backend/src/main/resources/db/**`, `AceRecoveryApplication.java`, `R/package-info.java`, any endpoint contract.

### Tooling design (test scope)

Package `th.co.scb.ace.demo.recovery.architecture.boundary` (PA-02). Under `T`, so main-class imports (`DO_NOT_INCLUDE_TESTS`) and `ModulithTest` never see it.

- `ModuleMap` — immutable records `ModuleMap(String source, String rootPackage, List<Module> modules, List<External> external, List<String> clientLibraries, Object sourceViews)`, `Module(String code, String name, List<String> published, List<String> clientPackages)`, `External(String name, String rootPackage, List<String> published)`; helpers `modulePackage(Module)`, `moduleOf(String packageName)`. Lists copied with `List.copyOf`.
- `ModuleMapLoader.load(Path file)` — SnakeYAML 2.6 `new Yaml(new SafeConstructor(options))` with `LoaderOptions.setAllowDuplicateKeys(false)`. Every error is an `IllegalStateException` with the text `{file}: {fieldPath}: {problem}` (for example `recovery-modules.yaml: modules[2].code: duplicate value P3`). Checks are exactly those of SPEC-003 and the contract schema: missing file, invalid YAML, duplicate YAML key, required field missing or empty, `code` / `name` repeated, pattern broken (`code` `^(P([1-9]|10)|S[1-9])$`, `name` `^[a-z][a-z0-9]*$`, relative package `^[a-z][a-z0-9]*(\.[a-z][a-z0-9]*)*$`, Java package for `rootPackage`), `published` entry `internal` or under it, `published` empty, `external` not exactly `common` and `collection`, `clientLibraries` empty or repeated, unknown key at any level. `sourceViews` is the one accepted extra top-level key: kept as the raw parsed object, not validated. No package literal.
- `BoundaryRules` — `static List<ArchRule> all(ModuleMap map)` returning, in order, `moduleMap(map)`, `bnd1(map)`, `bnd2(map)`, `bnd4(map)`, `bnd5(map)`; package-private `static boolean matchesClientLibrary(String entry, String className)` (`className.equals(entry) || startsWith(entry + ".") || startsWith(entry + "$")`). Each rule is an ArchUnit rule with a custom `ArchCondition` that reports each violation once as one line of SPEC-010 text, all lines in one evaluation. A violation is one distinct (origin class, target class) pair per rule, so several accesses from one class to one target give one line (ArchUnit itself does not deduplicate); a nested origin class counts as its own class (`$` name). BND-4 treats as entity or repository a class annotated `@jakarta.persistence.Entity` or assignable to `org.springframework.data.repository.Repository`, excluding the Spring Data types in `org.springframework.data..` themselves, so a repository extending `Repository` is not a violation of its own; BND-1 and BND-2 use `allowEmptyShould(true)` (D-RCV-19). The module-map rule uses `ArchCondition.finish` for the checks that need every class first (SPEC-004 (a), (b)). Texts: `data-model.md` §4. No package literal.

### Relocation table (SPEC-022, SPEC-023, SPEC-025)

Old and new paths under `R`. "pp" = package-private. Only `package` and `import` lines change, except the two visibility changes and the property split.

| Old file | New file | Module | Visibility change |
|---|---|---|---|
| `rules/api/RuleEngine.java`, `RuleInput.java`, `RuleOutcome.java`, `RuleResult.java`, `CompiledRulePackage.java` | `casewf/rules/<same>.java` | P3 | none (public) |
| `rules/internal/DroolsRuleEngine.java`, `DroolsProperties.java` | `casewf/rules/<same>.java` | P3 | none (pp) |
| `platform/api/TimerScheduler.java` | `casewf/timers/TimerScheduler.java` | P3 | none |
| `platform/internal/QuartzTimerScheduler.java` | `casewf/timers/internal/QuartzTimerScheduler.java` | P3 | none (class pp, `TimerDueJob` public) |
| `workflow/api/WorkflowIds.java` | `casewf/workflow/WorkflowIds.java` | P3 | none |
| `workflow/internal/PlatformSmokeWorkflow.java` | `casewf/workflow/internal/PlatformSmokeWorkflow.java` | P3 | none (public) |
| `workflow/internal/PdpaPayloadCodec.java` | `casewf/workflow/internal/PdpaPayloadCodec.java` | P3 | **public → pp** (class and constructor) |
| `workflow/internal/TemporalConfig.java` | `casewf/workflow/internal/TemporalConfig.java` | P3 | none |
| `workflow/internal/TemporalProperties.java` | `casewf/workflow/internal/TemporalProperties.java` | P3 | **pp → public** |
| `workflow/internal/TemporalAdminController.java` | `casewf/admin/TemporalAdminController.java` | P3 | none |
| `platform/internal/RecoveryFlywayConfig.java` | `casewf/migration/RecoveryFlywayConfig.java` | P3 | none; parameter type becomes `RecoveryMigrationProperties` |
| `platform/api/RecoveryFlags.java` | `integration/flags/api/RecoveryFlags.java` | P2 | none |
| `platform/internal/PlatformConfig.java` | `integration/flags/PlatformConfig.java` | P2 | none; registers and reads `RecoveryFlagProperties` |
| `platform/internal/PlatformInfoController.java` | `integration/internal/PlatformInfoController.java` | P2 | none; reads `PlatformInfoProperties` |
| `platform/api/ApiError.java`, `ApiProblemException.java` | `access/api/<same>.java` | P4 | none |
| `platform/internal/ApiExceptionHandler.java`, `ProblemFactory.java` | `access/internal/<same>.java` | P4 | none |
| `platform/internal/SecurityConfig.java` | `access/internal/SecurityConfig.java` | P4 | none; reads `RecoverySecurityProperties` |
| `platform/internal/RecoveryProperties.java` | deleted (split, next table) | — | — |
| `documents/api/DocumentStore.java` | `dochub/api/DocumentStore.java` | P5 | none |
| `documents/internal/BlobDocumentStore.java` | `dochub/storage/BlobDocumentStore.java` | P5 | none |
| `platform/package-info.java`, `platform/api/package-info.java`, `rules/…`, `rules/api/…`, `workflow/…`, `workflow/api/…`, `documents/…`, `documents/api/…` (8 files) | deleted | — | — |

After the move the cross-module type dependencies of main code are exactly `casewf.rules` → `integration.flags.api` (`DroolsRuleEngine` → `RecoveryFlags`) and `casewf.admin` → `access.api` (`TemporalAdminController` → `ApiError`, `ApiProblemException`) (SPEC-022 (d)). No cycle. `ApiExceptionHandler` keeps `@RestControllerAdvice(basePackages = "th.co.scb.ace.demo.recovery")`; component scan from `AceRecoveryApplication` (`th.co.scb.ace.demo`) still finds every bean; workflow type `PlatformSmokeWorkflow` and queue `rwb-platform` are unchanged (SPEC-022 (e)).

### Property split (SPEC-023; plan input R2-4)

| New record (pp, `@ConfigurationProperties`) | Path | Prefix and components (keys unchanged) | Registered by | Read by |
|---|---|---|---|---|
| `RecoveryFlagProperties(boolean temporal, boolean drools)` | `R/integration/flags/RecoveryFlagProperties.java` | `rwb.p3`: `temporal`, `drools` | `@EnableConfigurationProperties` on `PlatformConfig` | `PlatformConfig.recoveryFlags` |
| `PlatformInfoProperties(String environment, String schema)` | `R/integration/internal/PlatformInfoProperties.java` | `rwb`: `environment`, `schema` | nested `@Configuration(proxyBeanMethods = false) @EnableConfigurationProperties static class Registration` (the existing `DroolsProperties` pattern) | `PlatformInfoController` |
| `RecoveryMigrationProperties(String schema, Flyway flyway)`, nested `Flyway(boolean enabled, String url, String user, String password, String location)` | `R/casewf/migration/RecoveryMigrationProperties.java` | `rwb`: `schema`, `flyway.*` | `@EnableConfigurationProperties` on `RecoveryFlywayConfig` | `RecoveryFlywayConfig` |
| `RecoverySecurityProperties(String issuer, String jwkSetUri, String audience, String rolesClaim, List<String> corsOrigins)` | `R/access/internal/RecoverySecurityProperties.java` | `rwb.security`: same five keys | `@EnableConfigurationProperties` on `SecurityConfig` | `SecurityConfig` |

Names are a plan choice (PA-06). Defaults, validation and keys carry over unchanged; `RecoveryProperties` had no validation annotation. The `RecoveryProperties` Javadoc rule ("no module reads another's") moves into the four records' Javadoc.

### Tests that move (SPEC-022 (f))

| Old | New | Change |
|---|---|---|
| `T/platform/internal/QuartzTimerSchedulerTest.java` | `T/casewf/timers/internal/QuartzTimerSchedulerTest.java` | `package`, `import` |
| `T/rules/internal/DroolsRuleEngineTest.java` | `T/casewf/rules/DroolsRuleEngineTest.java` | `package`, `import`, and the workbook rows: line 97 `Import` → `th.co.scb.ace.demo.recovery.casewf.rules.RuleInput, th.co.scb.ace.demo.recovery.casewf.rules.RuleOutcome`; line 98 `Variables` → `th.co.scb.ace.demo.recovery.casewf.rules.RuleOutcome outcome` |
| `T/workflow/internal/PdpaPayloadCodecTest.java` | `T/casewf/workflow/internal/PdpaPayloadCodecTest.java` | `package`, `import` |
| `T/workflow/internal/PlatformSmokeWorkflowTest.java` | `T/casewf/workflow/internal/PlatformSmokeWorkflowTest.java` | `package`, `import` |

Assertions are not edited. No test is skipped or weakened.

### `RecoveryBoundaryTest` changes (SPEC-026)

- Load the real map with `ModuleMapLoader.load(Path.of("src/test/resources/architecture/recovery-modules.yaml"))` (Gradle runs tests in `backend/`, as the existing `SOURCES` path already assumes). Import main classes from `map.rootPackage()` with `DO_NOT_INCLUDE_TESTS`.
- Add one test per rule of `BoundaryRules.all(map)`: `moduleMapRule`, `bnd1CollectionBoundary`, `bnd2CommonBoundary`, `bnd4EntitiesAndRepositoriesStayInTheirModule`, `bnd5ClientLibrariesOnlyInClientPackages`.
- Add `everyMapModuleHasApiAndInternalPackageInfo` (SPEC-001 (b), SPEC-025): for every map module, `package-info.java` exists in its base, `api` and `internal` source folders under `backend/src/main/java`. It checks source files, as the existing `SOURCES` scan does, because javac writes no `package-info.class` for the unannotated `internal` file (PA-03); the base file must carry `@ApplicationModule` and the `api` file `@NamedInterface(name = "api", propagate = false)`, which the module-map rule also checks in bytecode.
- Add `publishedSurfaceIsExactlyTheSpecifiedTypes` (T-TE001-14, PA-05).
- Delete `blobClientOnlyInDocumentsModule`; BND-5 replaces it because SPEC-009 and SPEC-026 require it (spec gate finding 022, D-RCV-41). BND-5 covers 16 client libraries instead of one and, as the approved spec defines, allows each of them in the using module's own client packages (`integration.adapter`, `dochub.storage`, `agent.client`), not only in the storage package. The only user today is `BlobDocumentStore` in `dochub.storage`.
- `workflowImplementationsAreDeterministic`: package `RECOVERY + ".workflow.."` → `RECOVERY + ".casewf.workflow.."`; nothing else changes (it keeps `allowEmptyShould(true)`). New guard `determinismRuleSelectsTheSmokeWorkflowImpl`: the classes in `RECOVERY + ".casewf.workflow.."` whose simple name ends with `Impl` include `th.co.scb.ace.demo.recovery.casewf.workflow.internal.PlatformSmokeWorkflow$Impl`, so a mistyped package cannot make the rule pass on an empty selection (SPEC-026: `PlatformSmokeWorkflow.Impl` stays under the rule). `noRecoveryClassNamesAPublicTable`: unchanged (RWB-E1-069 owns it).

### Coverage gate edit (SPEC-020)

In `backend/build.gradle.kts` only:

- Add a file collection of the tooling classes: `sourceSets.test.get().output.classesDirs`, include `th/co/scb/ace/demo/recovery/architecture/boundary/**`, exclude `**/*Test.class` and `**/*Test$*.class`. Fixtures (`th/co/scb/ace/boundaryfixture/**`) and `RecoveryBoundaryTest` are outside the include, so they are not measured.
- Both `recoveryCoverageReport` and `recoveryCoverageVerification`: `classDirectories.setFrom(recoveryClasses, boundaryToolingClasses)`; `sourceDirectories` adds `sourceSets.test.get().java.srcDirs` so the report shows tooling source.
- `recoveryCoverageVerification`: limits `LINE`, `INSTRUCTION`, `BRANCH`, `METHOD`, each `minimum = 0.80`; description text updated.
- Unchanged: execution data from `test` only; `test` `finalizedBy` the report; neither task added to `check` (D-RCV-28 (3), D-RCV-40); no main class excluded. CI keeps running only the report (D-RCV-05; audit A-09 with RWB-TE-003 / RWB-TE-011, SU-10).

Baseline (spec): LINE 133/415, BRANCH 25/92, INSTRUCTION 686/2174, METHOD 41/135. Expected `FAIL` after TASK-01 and `PASS` after TASK-12.

### Coverage tests (SPEC-024) and binding tests (SPEC-023, T-TE001-12)

All JUnit 5, in the `test` task, untagged, no Docker, no database, no network, synthetic data only, each class Javadoc naming RWB-TE-001 and its purpose (testing-standards §2). Package-private classes are tested from their own package.

| Test class (path under `T`) | Classes covered | Scenarios |
|---|---|---|
| `access/api/ApiErrorTest.java` | `ApiError`, `ApiProblemException` | code and status per constant; placeholder fill in English and Thai; no placeholder; exception copies placeholders and keeps cause and message code |
| `access/internal/ApiExceptionHandlerTest.java` | `ApiExceptionHandler`, `ProblemFactory` | `ApiProblemException` → status, `type`, `messageCode`, `messageTh`; `AccessDeniedException` → 403 MSG-P4-002; `NoResourceFoundException` → 404 MSG-P4-003; other exception → 500 with no detail; `traceId` null without tracer, null with tracer and no span, set with a mocked span; `write` sets status, `application/problem+json`, UTF-8 and body (`MockHttpServletResponse`) |
| `access/internal/SecurityConfigTest.java` | `SecurityConfig`, `RecoverySecurityProperties` | MVC slice (`spring-boot-starter-webmvc-test`, `spring-security-test`) with a test-only controller nested in the test class and a mocked `JwtDecoder` bean returning synthetic `Jwt`s: no token → 401 MSG-P4-001; token without an `RW-` role → 401 MSG-P4-001; `RW-` role but method check denies → 403 MSG-P4-002; roles claim mapped to authorities, missing claim → none; CORS preflight from a configured origin allowed, other origin refused; `/actuator/health` open; `jwtDecoder` bean built from the properties without a network call; binding of `rwb.security.*` from the real `application.yaml` (T-TE001-12) |
| `integration/flags/PlatformConfigTest.java` | `PlatformConfig`, `RecoveryFlagProperties`, `RecoveryFlags` | `ApplicationContextRunner`: flags from properties (both on, both off); binding from the real `application.yaml` gives `temporal=false`, `drools=false` (T-TE001-12) |
| `integration/internal/PlatformInfoControllerTest.java` | `PlatformInfoController`, `PlatformInfoProperties` | `info()` with a mocked `JdbcTemplate` returns service, environment, flags and the three counts for the configured schema; binding from the real `application.yaml` gives `environment=DEV`, `schema=recovery` (T-TE001-12) |
| `casewf/migration/RecoveryFlywayConfigTest.java` | `RecoveryFlywayConfig`, `RecoveryMigrationProperties` | `recoveryFlyway(...)` called directly, `migrate` never called: schema and default schema, history table `flyway_schema_history_recovery`, placeholder `recoverySchema`, `cleanDisabled`, location; user set with own URL, user set without URL (falls back to `DataSourceProperties`), no user (uses the `DataSource`); binding from the real `application.yaml` gives `schema=recovery`, `flyway.location=classpath:db/modulemigration/recovery`, `flyway.enabled=true` (T-TE001-12) |
| `casewf/admin/TemporalAdminControllerTest.java` | `TemporalAdminController` | `health()` with mocked stubs: namespace, state, retention days, three queues with poller counts; `UNAVAILABLE` and `DEADLINE_EXCEEDED` → `ApiProblemException` WORKFLOW_UNAVAILABLE (503 MSG-P3-036); other status rethrown; `WorkflowServiceException` with an unavailable cause → 503, other cause rethrown; `smoke()` on a `TestWorkflowEnvironment` client returns an ID matching `platform-smoke-` plus eight digits (format asserted, not the date, because the controller reads the system clock) and type `PlatformSmokeWorkflow`; a second call returns the same ID |
| `casewf/workflow/internal/TemporalConfigTest.java` | `TemporalConfig`, `TemporalProperties`, `SmokeActivities` | `ApplicationContextRunner` with `rwb.p3.temporal=true` and a loopback target: stubs, codec, client (namespace, identity) and worker factory beans are created without a connection; flag off → none of them; `startWorkers` with a mocked event and mocked `WorkerFactory` calls `start`; `SmokeActivities.answer` returns the probe ID; `hostName()` returns a value |
| `casewf/workflow/WorkflowIdsTest.java` | `WorkflowIds` | `caseWorkflowId` format; queue and namespace constants |
| `dochub/storage/BlobDocumentStoreTest.java` | `BlobDocumentStore`, its `Config`, `BlobProperties` | mocked Blob clients: standard put (headers, no condition, digest and size); legal put with `If-None-Match: *`; legal overwrite (`BLOB_ALREADY_EXISTS`) → `DocumentImmutableException`; other storage error rethrown; container created once; get present, absent (`BLOB_NOT_FOUND`), other error rethrown; `Config`: connection string, endpoint with credential (no network call), neither → `IllegalStateException` |
| `casewf/rules/DroolsPropertiesTest.java` | `DroolsProperties` and its `Registration` | binding of `rwb.drools.kiebase-cache-max` from the real `application.yaml` (20) |

"From the real `application.yaml`" means an `ApplicationContextRunner` with `ConfigDataApplicationContextInitializer`, so the test reads the same file and keys that `RecoveryProperties` read before the split, with environment placeholders at their defaults; the asserted values are those defaults. If any class is still below 80% after these tests, the Builder adds a test at that class's home. No class is excluded and no threshold is lowered ([IEG]).

## Frontend Plan

Surface status: **CHANGED (test only)**. Unit tests **REQUIRED**; the coverage gate is inherited (80% lines, statements, branches, functions on `src/modules/recovery/**` excluding `__tests__` and `i18n`).

| Kind | Path | Task | SPEC |
|---|---|---|---|
| Add | `frontend/src/modules/recovery/__tests__/importBoundary.test.ts` | TASK-15 | 014, 015 |
| Unchanged | `frontend/eslint.config.js`, `frontend/vite.config.ts`, `frontend/tsconfig.json`, `frontend/package.json`, `frontend/package-lock.json`, every runtime file under `frontend/src/` | — | 013, 014 |

Design of the test (SPEC-015, ASM-07, plan inputs R2-1..R2-3):

- First line `// @vitest-environment node`. Imports only `eslint` (`ESLint`), `node:url` and `node:path`; no `@/` or `../` import, so the file itself passes the D-RCV-39 rule it lives under.
- `new ESLint({ cwd: <frontend root from import.meta.url> })`, which loads the real `frontend/eslint.config.js`.
- `lintText(source, { filePath: "src/modules/recovery/caselist/BoundaryFixture.tsx" })` for each fixture source, a one-line `import … from "<path>";` held as a string constant.
- Rejected set, each must give exactly one message with `ruleId === "no-restricted-imports"`: `@/modules/collection/worklist/WorkList`, `../../collection/worklist/WorkList`, `@/hooks/cfsc/x`, `@/api/tdr/config`, `@/pages/x`, `@/utils/cfscCaseList`, `@/modules/other/x`, `../x`.
- Allowed set, each must give no `no-restricted-imports` message: `@/components/ui/button`, `@/lib/utils`, `@/utils/date`, `@/contexts/ApiClientContext`, `@/api/schema`, `@/modules/recovery/casewf/x`, `./sibling`.
- `results[0]` guarded (`noUncheckedIndexedAccess`): the test fails with a clear message when ESLint returns no result.
- Timeout 30 000 ms for the first `typescript-eslint` load: on the `describe` block and, if the `ESLint` instance is created in `beforeAll`, also as that hook's timeout (a `describe` timeout does not cover hooks). The first run confirms that `src/test/setup.ts` (imports `@/i18n`) loads under the node environment.
- Runs in `npm run check` (`coverage` script) and in CI `frontend-check`; `npm run build` (`tsc --noEmit`) type-checks it.

No API contract is consumed, so no frontend task waits on a backend contract task. Frontend and backend run in parallel; TASK-17 needs both.

## Unit test applicability

| Surface | Changes | Unit tests | Gate | Trace | Reason |
|---|---|---|---|---|---|
| Backend | YES | REQUIRED | JaCoCo `recoveryCoverageVerification`: LINE, INSTRUCTION, BRANCH, METHOD ≥ 80%, bundle, all recovery main classes plus tooling | SPEC-001..-012, -017, -018, -020, -022..-026 | Every baseline class is relocated, so all are changed code; new tooling is test-scope code in the gate |
| Frontend | YES (test only) | REQUIRED | Vitest v8 thresholds 80 × 4 in `frontend/vite.config.ts` (inherited) | SPEC-013..-015, -020 | One new test file proves the inherited D-RCV-39 rule; runtime code unchanged; coverage measured on the existing code (baseline 91.89 / 88.09 / 82.35 / 91.66) |

Final coverage evidence (TASK-18) follows `implementation-execution-gates.md`: one results row per surface, with the native reports (`backend/build/reports/jacoco/recoveryCoverageReport.xml` and HTML; `frontend/coverage/coverage-summary.json`, `lcov.info`).

## Execution order (tests before code, AGENTS.md rules 3 and 10)

1. TASK-00 pre-flight on the worktree base.
2. Red first: TASK-01 (coverage gate fails at baseline), TASK-03 (loader tests do not compile), TASK-06 (rule tests fail), TASK-09 (real-code boundary tests fail on the baseline packages), TASK-10 (binding tests do not compile).
3. Green: TASK-04, TASK-07, then TASK-11 (relocation, skeleton, property split).
4. TASK-08 (BND-3 fixtures) and TASK-15 (frontend) prove behaviour that already exists in Spring Modulith and ESLint: they pass when written, and their breaking fixtures show the rule fires.
5. TASK-12 adds characterization tests for unchanged behaviour at the new homes (PA-07).
6. Verification: TASK-13, TASK-14, TASK-16, TASK-17; evidence TASK-18.

The red runs are recorded as evidence (command, exit code, first failing assertion).

## Functional Test Scenarios

| ID | Scenario | Owner | Scope | Evidence |
|---|---|---|---|---|
| FTS-01 | `GET /api/recovery/v1/platform/info` answers as before after `PlatformInfoController` moves to `integration.internal` (status, body fields, 401 without token) | API Tester | Existing `PlatformE2ETest` (tag `e2e`) against the local stack; no new API test, `NO_API_CHANGE` | `api-tests/` report with the `./gradlew e2eTest` output |
| FTS-02 | `GET /api/recovery/v1/admin/temporal/health` and `POST /api/recovery/v1/admin/workflows/smoke` answer as before after `TemporalAdminController` moves to `casewf.admin` | API Tester | Existing `PlatformE2ETest` | as FTS-01 |
| FTS-03 | Recovery Flyway bean still migrates the empty recovery schema after the move to `casewf.migration` | Implementation Builder (integration) | Existing `RecoveryDatabaseIT` (tag `recovery-it`, D-RCV-44) | `implement/backend/it.log` |
| FTS-04 | UI journeys | Functional Automation Test | `NOT_APPLICABLE`: UI In Scope NO, no screen, route or component changes; the frontend change is a unit test | — |
| HV-01 | GitLab blocks a merge request whose pipeline fails | Human (ACE platform / DevOps owner) | Not testable here (no GitLab MCP); never reported as tested | Open item SU-13 |

## Requirement Logic To Task Coverage

`REQ_REF` values are the spec's "Requirement-to-SPEC Logic Coverage" rows.

| REQ_REF | Mapped SPEC-* | Mapped TASK-* | Coverage Type | Verification | Status |
|---|---|---|---|---|---|
| AC1 / X1 / TC-TE-001-01 | SPEC-005, -010, -011 | TASK-05, -06, -07 | DIRECT_IMPLEMENTATION | `BoundaryRulesTest.collectionInternalDependencyBreaksBnd1` | COVERED |
| AC2 / TC-TE-001-02 | SPEC-006, -011 | TASK-05, -06, -07 | DIRECT_IMPLEMENTATION | `BoundaryRulesTest.commonApiDependencyPassesEveryRule` | COVERED |
| AC3 / X2 / TC-TE-001-03 | SPEC-007, -011 | TASK-05, -08, -13 | DIRECT_IMPLEMENTATION (fixture test) / INHERITED_EXISTING_BEHAVIOR (`ModulithTest`) | `ModulithFixtureTest.internalDependencyBetweenModulesFailsVerify`, `.publishedWriterDependencyPassesVerify`; `ModulithTest.modulesRespectTheirBoundaries` green after TASK-11. Accepted deviation D-RCV-42 (Modulith text). | COVERED |
| AC4 / X3 / TC-TE-001-04 | SPEC-008, -011 | TASK-05, -06, -07 | DIRECT_IMPLEMENTATION | `BoundaryRulesTest.foreignEntityAndRepositoryBreakBnd4` | COVERED |
| AC5 / X4 / TC-TE-001-05 | SPEC-009, -011 | TASK-05, -06, -07 | DIRECT_IMPLEMENTATION | `BoundaryRulesTest.clientLibraryOutsideClientPackageBreaksBnd5` | COVERED |
| AC6 / X5 / TC-TE-001-06 | SPEC-014, -015 | TASK-15, -16 | DIRECT_IMPLEMENTATION (test) / INHERITED_EXISTING_BEHAVIOR (rule) | `importBoundary.test.ts` rejected set (first two rows are AC6). Accepted deviation D-RCV-39 (rule name, `@/` path). | COVERED |
| AC7 / X6 / TC-TE-001-07 | SPEC-003, -004, -010 | TASK-05, -06, -07 | DIRECT_IMPLEMENTATION | `BoundaryRulesTest.packageMissingFromTheMapFails` (text ends with `recovery.vendorx is not in the module map`) | COVERED |
| X7 / TC-TE-001-08 / MSG-P4-002 / Flow 5 / §13 step 6 | SPEC-016 | TASK-18 | MOVED_OUT_OF_SCOPE (D-RCV-52; neither gate value applies, see note) | TASK-18 check: no `RecoveryAccessGuard`, no test-only Case record endpoint, no new MSG-P4-002 use added by this story | COVERED (as an exclusion) |
| BR1 | SPEC-005 | TASK-06, -07, -09 | DIRECT_IMPLEMENTATION | TC-TE-001-01; T-TE001-03; `RecoveryBoundaryTest.bnd1CollectionBoundary` | COVERED |
| BR2 | SPEC-006 | TASK-06, -07, -09 | DIRECT_IMPLEMENTATION | TC-TE-001-02; `BoundaryRulesTest.commonInternalDependencyBreaksBnd2`; T-TE001-03; `RecoveryBoundaryTest.bnd2CommonBoundary` | COVERED |
| BR3 | SPEC-004 (d)–(f), -007 | TASK-07, -08, -09, -11, -13 | DIRECT_IMPLEMENTATION / INHERITED_EXISTING_BEHAVIOR (`ModulithTest`) | TC-TE-001-03; T-TE001-16; T-TE001-02; T-TE001-14; `ModulithTest` | COVERED |
| BR4 | SPEC-008 | TASK-06, -07, -09 | DIRECT_IMPLEMENTATION | TC-TE-001-04; `RecoveryBoundaryTest.bnd4EntitiesAndRepositoriesStayInTheirModule` | COVERED |
| BR5 | SPEC-009, -022 | TASK-06, -07, -09, -11 | DIRECT_IMPLEMENTATION | TC-TE-001-05; T-TE001-09; `RecoveryBoundaryTest.bnd5ClientLibrariesOnlyInClientPackages`; T-TE001-13 run 1 | COVERED |
| BR6 | SPEC-002, -003, -004, -026 | TASK-02, -04, -06, -07, -09 | DIRECT_IMPLEMENTATION | TC-TE-001-07; T-TE001-01; T-TE001-15 (no recovery package literal in tooling); every fixture world uses its own root through the same rules | COVERED |
| Flow 1 / §13 step 1 | SPEC-001, -013, -022 | TASK-11, -09 | DIRECT_IMPLEMENTATION (backend) / INHERITED_EXISTING_BEHAVIOR (frontend folder) | `RecoveryBoundaryTest.everyMapModuleHasApiAndInternalPackageInfo`, `moduleMapRule`; frontend folder exists | COVERED |
| Flow 2 / §13 step 2 | SPEC-002, -003 | TASK-02, -03, -04 | DIRECT_IMPLEMENTATION | T-TE001-01 `ModuleMapLoaderTest` | COVERED |
| Flow 3, 7, 8 / §13 steps 3–4 / §14 | SPEC-004..-011 | TASK-05, -06, -07, -08 | DIRECT_IMPLEMENTATION | TC-TE-001-01..-05, -07; T-TE001-02..-04, -09 | COVERED |
| Flow 4 / §13 step 5 | SPEC-014, -015 | TASK-15, -16 | INHERITED_EXISTING_BEHAVIOR (rule) / DIRECT_IMPLEMENTATION (fixture test) | T-TE001-07, -08 | COVERED |
| Flow 6 / §13 step 7 | SPEC-012 | TASK-13, -16, -17 | INHERITED_EXISTING_BEHAVIOR (CI jobs) / DIRECT_IMPLEMENTATION (local merge gate) | T-TE001-13 three runs; HV-01 open for a human | COVERED (HV-01 open) |
| §17 Guardrails | SPEC-011, -019 | TASK-05, -18 | DIRECT_IMPLEMENTATION | TASK-18 review of fixtures, maps and failure text: class and package names only, synthetic values | COVERED |
| §19 Out of scope | SPEC-016 | TASK-18 | DIRECT_IMPLEMENTATION (exclusion check) | TASK-18 diff check against the SPEC-016 list | COVERED |
| Card / AUD A-01 | SPEC-022, -023 | TASK-00, -10, -11, -12 | DIRECT_IMPLEMENTATION | T-TE001-05, -06, -12, -14; `ModulithTest` | COVERED |

Note on X7: the planning gate allows `DIRECT_IMPLEMENTATION` or `INHERITED_EXISTING_BEHAVIOR`. Neither is true for work that D-RCV-52 moved to RWB-E1-022. The row is kept visible with its real status, and TASK-18 checks that this story does not build it.

## SPEC to task map

| SPEC | Tasks | Tests |
|---|---|---|
| 001 | TASK-11, -09 | T-TE001-05 (`everyMapModuleHasApiAndInternalPackageInfo`, `moduleMapRule`) |
| 002 | TASK-02 | T-TE001-01 (`loadsTheRealMap`), T-TE001-05 |
| 003 | TASK-03, -04 | T-TE001-01, T-TE001-15 |
| 004 | TASK-06, -07, -09 | TC-TE-001-07, T-TE001-02, T-TE001-05 |
| 005 | TASK-06, -07, -09 | TC-TE-001-01, T-TE001-03, -04 |
| 006 | TASK-06, -07, -09 | TC-TE-001-02, T-TE001-03, `commonInternalDependencyBreaksBnd2` |
| 007 | TASK-08, -13 | TC-TE-001-03, T-TE001-16, T-TE001-06 (`ModulithTest`) |
| 008 | TASK-06, -07, -09 | TC-TE-001-04 |
| 009 | TASK-06, -07, -09 | TC-TE-001-05, T-TE001-09, T-TE001-05 |
| 010 | TASK-06, -07 | TC-TE-001-01, -04, -05, -07, T-TE001-04 |
| 011 | TASK-05 | all fixture tests |
| 012 | TASK-13, -16, -17 | T-TE001-13; HV-01 (human) |
| 013 | TASK-16 | T-TE001-08 |
| 014 | TASK-15, -16 | T-TE001-07 |
| 015 | TASK-15 | TC-TE-001-06, T-TE001-07 |
| 016 | TASK-18 | scope check |
| 017 | TASK-00, -18 | dependency diff check |
| 018 | TASK-13, -14, -16 | T-TE001-06, -08, -11 |
| 019 | TASK-05, -18 | guardrail check |
| 020 | TASK-01, -13, -16 | T-TE001-08, -10 |
| 021 | — (withdrawn) | `noRecoveryClassNamesAPublicTable` kept unchanged (TASK-09) |
| 022 | TASK-00, -11 | T-TE001-05, -06, -11, -14 |
| 023 | TASK-10, -11 | T-TE001-12 |
| 024 | TASK-12 | T-TE001-10 |
| 025 | TASK-09, -11 | T-TE001-05, -14 |
| 026 | TASK-09 | T-TE001-05 |

## Screen-to-task mapping

`NOT_APPLICABLE`: UI In Scope NO, `DESIGN_EVIDENCE_STATUS: NOT_REQUIRED`, no effective-screen node or `SCR-*` screen in the spec. No screen consolidation task is needed; the pre-submit check records this.

## Security, privacy and compliance

- No endpoint, permission or authentication behaviour changes. `SecurityConfig` and the two controllers move package only; `SecurityConfigTest` and the e2e suite show the behaviour is unchanged.
- Personal data: none. Fixtures, maps and failure text hold class and package names only; test data is synthetic (AGENTS.md §4.7).
- No secret: no new property, and binding tests read placeholder defaults only (`RWB_TEMPORAL_CODEC_KEY` stays empty in tests; codec tests generate a random key as today).
- Audit, KYC/AML, suitability, approval: not applicable to a build-time enabler.

## Release and rollback

Build-time check with no runtime flag ([S] §13). Rollback is a revert merge request. The orchestrator merges into `develop-recovery` only after `./scripts/dev.ps1 test` exits 0 on the branch (SPEC-012 (b), D-RUN-06). `recoveryCoverageVerification` is shown separately at the code gate (R3-3).

## Assumptions

Plan-stage assumptions are in `assumptions.md` (PA-01..PA-12). Spec assumptions ASM-01..ASM-09 are carried unchanged.

## Status

```text
PLANNER_STATUS_SUMMARY: Plan ready: 19 tasks (TASK-00..TASK-18) for the module skeleton, relocation, map-driven boundary rules, fixtures, coverage lift and the AC6 frontend test.
PLANNER_STATUS_DETAIL: SUCCESS [REASON: spec v4 passed the gate; every SPEC, AC and BR mapped to tasks and named tests] [UNBLOCK_ACTION: n/a]
PLANNER_CLARIFICATION_STATUS: READY [OPEN_ITEMS: 0] [UNBLOCK_ACTION: n/a]
PLANNER_DESIGN_SOURCE: NOT_REQUIRED [NOTE: UI In Scope NO]
PLAN_REQUIREMENT_COVERAGE_SUMMARY: BR1-BR6 and AC1-AC7 each map to tasks and named tests; X7 is shown as moved out of scope.
PLAN_REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 13] [TASK_COVERED_RULES: 13] [MISSING_TASK_RULES: 0] [AMBIGUOUS_TASK_RULES: 0] [CONTRADICTIONS: 0]
```
