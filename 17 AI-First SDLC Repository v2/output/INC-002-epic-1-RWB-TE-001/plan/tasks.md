---
title: "Tasks — RWB-TE-001 Recovery module folder and boundary test"
run_id: "INC-002-epic-1-RWB-TE-001"
story: "RWB-TE-001"
jira: "TB0001-1235"
---

# Tasks — RWB-TE-001

Design Source: NOT_REQUIRED (`UI In Scope: NO`).

Plan: `plan.md`. All paths in `ace-monorepo/` unless they start with `output/` or `docs/`. ACE branch `feature/TB0001-1235-recovery-module-boundary` from `develop`; commit message `TB0001-1235: <summary>`. Task IDs are written `TASK-RWB-TE-001-NN`; the short form `TASK-NN` in `plan.md` means the same task.

**Every build task is blocked by TASK-RWB-TE-001-00 (plan-approval preconditions).** Status 2026-11-09: PRE-1 (Product Owner spec approval) **APPROVED** (Chitchaya Muanchonchana, TechX PO, Jira `TB0001-1235` comment 1781003); PRE-2 (OPEN-023) **APPROVED** (Pongchai Charoenrungrodkun, ACE and Recovery lead, comment 1781273); PRE-3 (FDA plan approval) and PRE-4 (FDE task approval) **APPROVED** (Jesniphat Pukkham, 2026-11-09). TASK-00 still re-checks these in the increment card before any build task starts.

## Unit test applicability

| Surface | Status | Trace | Reason | Unit-test tasks |
|---|---|---|---|---|
| Backend | REQUIRED | SPEC-001..-012, -017, -018, -020 | Test-scope loader and rule factory are executable code; main scope is `package-info` only | TASK-RWB-TE-001-05, -08, -09, -10; gate TASK-RWB-TE-001-12 |
| Frontend | REQUIRED | SPEC-013..-015, -020 | ESLint rule proven by Vitest fixture test; coverage expected `PASS` with 0/0 recorded as printed (placeholder only) | TASK-RWB-TE-001-16; gate TASK-RWB-TE-001-17 |

## Task table

### Gate and setup

| TASK ID | Description | Trace (SPEC/FR/NFR) | BLOCKED_BY | Verification |
|---|---|---|---|---|
| TASK-RWB-TE-001-00 | **Plan-approval precondition check.** Confirm in `docs/increments/INC-002-epic-1-RWB-TE-001.md` and `docs/open-items.md` that PRE-1 (Product Owner spec approval), PRE-2 (OPEN-023 settled by the ACE tech lead for `vitest` 4.1.12, `@vitest/coverage-v8` 4.1.12, JaCoCo plugin 0.8.14, and edits to `frontend/package.json`, `frontend/tsconfig.app.json`, `frontend/eslint.config.js`, `frontend/vitest.config.ts`, both lockfiles, `backend/build.gradle.kts`, and the new test-scope fixture root package `th.co.scb.ace.recoveryfixture`), PRE-3 (FDA plan approval) and PRE-4 (FDE task approval) each have a decision and a date. If any is missing, stop with `BLOCKED`. If PRE-2 changes a version or file, stop and ask for a planner re-run. | SPEC-017; D-RCV-15, -40, -43; OPEN-023; GAP-006 | NONE | Builder records the four decisions with dates in `output/INC-002-epic-1-RWB-TE-001/implement/report.md` |
| TASK-RWB-TE-001-01 | **Branch and merge-order check.** Create `feature/TB0001-1235-recovery-module-boundary` from current `develop`. Record: `develop` SHA; whether `backend/src/main/java/th/co/scb/ace/demo/recovery/casewf/internal/migration` exists (RWB-E1-044 merged); whether `backend/build.gradle.kts` already has `jacoco`, `recoveryCoverageReport`, `recoveryCoverageVerification`. Re-run `./gradlew dependencies --configuration testCompileClasspath` and confirm `archunit:1.4.2` and `snakeyaml` still present; if not, stop (SPEC-017 needs approval of a `testImplementation` line). Run `npm ci` at the workspace root. Record a baseline `./gradlew test` duration. | SPEC-001 (c), -017, -020; CLAR-012; D-RCV-43 | TASK-RWB-TE-001-00 | Facts and baseline duration in `implement/report.md` |

### Backend Plan

| TASK ID | Description | Trace (SPEC/FR/NFR) | BLOCKED_BY | Verification |
|---|---|---|---|---|
| TASK-RWB-TE-001-02 | **Main-scope module skeleton.** Create `backend/src/main/java/th/co/scb/ace/demo/recovery/package-info.java` with `@ApplicationModule(displayName = "Recovery")` (closed). For each of `dataengine`, `integration`, `casewf`, `access`, `dochub`, `comms`, `decision`, `payments`, `reporting`, `agent`, `valuation`, `treatment`, `guarantee`, `litigation`, `asset`, `debtsale`, `writeoff`, `deviation`, `partner`: `recovery/<name>/package-info.java` with `@ApplicationModule`, `recovery/<name>/api/package-info.java` with `@NamedInterface("api")`, `recovery/<name>/internal/package-info.java` with no annotation. No other type in main scope. Keep `recovery.casewf.internal.migration` unchanged if it exists. | SPEC-001; FR-RWB-003; CTX-CONSTRAINT-002; BS-1.1, BS-1.2; D-RCV-02, -36; CLAR-010, -012 | TASK-RWB-TE-001-01 | `find backend/src/main/java/th/co/scb/ace/demo/recovery -name package-info.java \| wc -l` = 58; `find … -type f ! -name package-info.java` lists only RWB-E1-044 files (or nothing); `./gradlew compileJava checkstyleMain`; `ModulithTest` green (`./gradlew test --tests th.co.scb.ace.demo.ModulithTest`) |
| TASK-RWB-TE-001-03 | **Module map.** Create `backend/src/test/resources/architecture/recovery-modules.yaml` per `data-model.md` §1: `rootPackage: th.co.scb.ace.demo.recovery`; 19 modules (code, name, `published: [api]`); `clientPackages` P2 `[adapter]`, P10 `[client]`, others `[]`; `external` `common` (`th.co.scb.ace.demo.common`, `[api]`) and `collection` (`th.co.scb.ace.demo.collection`, `[api]`); `clientLibraries` (16 entries). No business value, no personal data. | SPEC-002, -019; BR6; FR-RWB-020; D-RCV-37, -41; CLAR-004 A, -006 B, -008 | TASK-RWB-TE-001-01 | Loaded without error by TASK-RWB-TE-001-05 valid case; reviewer diffs every value against `data-model.md` §1; file is under `src/test/resources` (not in the boot jar: `./gradlew bootJar` and `jar tf` shows no `recovery-modules.yaml`) |
| TASK-RWB-TE-001-04 | **`ModuleMap` and `ModuleMapLoader` (test scope)** in `backend/src/test/java/th/co/scb/ace/demo/recovery/architecture/`. Immutable records; SnakeYAML 2.x `new Yaml(new SafeConstructor(options))` with `LoaderOptions` and `options.setAllowDuplicateKeys(false)` (no arbitrary type construction; `LoadSettings` belongs to snakeyaml-engine and is not on the classpath). Java source passes ACE checkstyle (LineLength 100: split long messages). Fails naming the file and field path on: missing file; invalid YAML; missing/empty required field; duplicate `code` or `name`; pattern breach (`code` `^(P([1-9]\|10)\|S[1-9])$`, `name` `^[a-z][a-z0-9]*$`, published/clientPackages `^[a-z][a-z0-9]*(\.[a-z][a-z0-9]*)*$`, package names valid Java); published entry `internal` or under it; duplicate published entry; unknown field; empty `published` or `clientLibraries`; missing `external.common` or `external.collection`. No package literal in the class. | SPEC-003; BR6; X-B7; FR-RWB-020 | TASK-RWB-TE-001-03 | `grep -n "th\.co\.scb" ModuleMapLoader.java ModuleMap.java` returns nothing; covered by TASK-RWB-TE-001-05 |
| TASK-RWB-TE-001-05 | **Loader unit test** `ModuleMapLoaderTest` (JUnit 5, AssertJ), T-TE001-01: valid map (real map and a small fixture map) → loads; and one fixture YAML per error under `backend/src/test/resources/architecture/fixtures/loader/` (missing file, invalid YAML, missing field, duplicate code, duplicate name, bad pattern, `internal` published, `internal.x` published, unknown field, missing external) → exception message names file and field. Synthetic content only. | SPEC-003; T-TE001-01; X-B7 | TASK-RWB-TE-001-04 | `./gradlew test --tests "th.co.scb.ace.demo.recovery.architecture.ModuleMapLoaderTest"` green |
| TASK-RWB-TE-001-06 | **Rule factory** `RecoveryBoundaryRules` (test scope, same package). From a `ModuleMap`: (1) module-map check SPEC-004 (a)–(f) with the exact texts, ignoring `package-info`; (2) BND-1 and BND-2 (`allowEmptyShould(true)`); (3) BND-4 (`@jakarta.persistence.Entity`, subtypes of `org.springframework.data.repository.Repository`; allowed only within the same recovery module; ACE `model`/`repository`, `samplemodule`, common, collection all forbidden); (4) BND-5 with name-boundary matching (`n == e`, `n` starts with `e.` or `e$`) and `clientPackages` in-or-under; (5) failure text `Rule {code} broken: {class} depends on {dependency}. Use {module}.api or an application event.` one line per violation, all violations per run; `{module}` = target map name (BND-1/-2/-4) or `integration.adapter` / `agent.client` (BND-5). No package literal in the class. Failure-text literals are split (concatenation or text block) to stay within checkstyle LineLength 100; no suppression. | SPEC-004, -005, -006, -008, -009, -010; BR1, BR2, BR4, BR5, BR6; FR-RWB-003; D-RCV-19, -38, -41, -42; CLAR-001 A, -006 B, -011 | TASK-RWB-TE-001-04 | `grep -n "th\.co\.scb" RecoveryBoundaryRules.java` returns nothing; behaviour by TASK-RWB-TE-001-08 |
| TASK-RWB-TE-001-07 | **Backend fixtures** under `backend/src/test/java/th/co/scb/ace/recoveryfixture/` (outside `th.co.scb.ace.demo`, so ACE `@EnableJpaRepositories(basePackages = "th.co.scb.ace.demo")`, entity scan and `ModulithTest` never see them) and fixture maps under `backend/src/test/resources/architecture/fixtures/`. Per rule one breaking and one passing fixture: BND-1 (collection non-published class / `collection.api` class); BND-2 (common non-published / common `api` interface, §13 step 4); BND-4 (other recovery module `@Entity` + repository; an `@Entity` outside the fixture recovery root standing in for ACE `model`; own-module entity passes); BND-5 (`java.net.http.HttpClient` and a `com.azure.storage` stand-in type in `casewf` / same in `integration.adapter`; `java.net.URLEncoder`, `java.net.SocketTimeoutException`, `java.net.URL`, a nested class of a listed class entry); map rule (`vendorx` package; class in root; `@NamedInterface` package not in map; published package without `@NamedInterface`; package with classes only in a sub-package; public class in module base package; non-public class in module base package; type-level `@NamedInterface` in `internal`; map module with no package); empty-set case (collection/common roots with no classes); two violations of one rule. BND-3 module sets under `recoveryfixture.bnd3.broken`, `recoveryfixture.bnd3.fixed` and `recoveryfixture.bnd3.cycle`, each copying the real layout: a closed `recovery` package with `@ApplicationModule` on `package-info`, nested modules with `@ApplicationModule`, each with `api` (`@NamedInterface("api")`) and `internal`. `broken`: module `a` imports `b.internal`; `fixed`: `a` uses `b.writer`, which has `@NamedInterface("writer")` and is listed in the fixture map; `cycle`: `a.api` ↔ `b.api` depend on each other through published packages only. Class and package names only; no Spring stereotype annotations. `com.azure:azure-storage-*` is already on `testRuntimeClasspath` (plan-time check), so the BND-5 fixture uses a real `com.azure.storage` type; no new dependency. | SPEC-011, -019; §13 steps 3–4; §17; BS-4.3 | TASK-RWB-TE-001-03, TASK-RWB-TE-001-04 | `./gradlew compileTestJava checkstyleTest`; reviewer check: no data values, no PII; `grep -rn "@Component\|@Service\|@Configuration\|@RestController" backend/src/test/java/th/co/scb/ace/recoveryfixture` empty |
| TASK-RWB-TE-001-08 | **Rule unit tests** `RecoveryBoundaryRulesTest`: import fixture classes with ArchUnit `ClassFileImporter` (tests included), build rules from fixture maps, assert fail/pass and exact text. Cases: TC-TE-001-01, -02, -04, -05, -07; T-TE001-02 (all SPEC-004 (a)–(f) texts; non-public base-package class passes); T-TE001-03 (`allowEmptyShould`); T-TE001-04 (two violations, one run, text matches SPEC-010); T-TE001-09 (name boundary). | SPEC-004..-006, -008..-011; BR1, BR2, BR4, BR5, BR6; X-B1, X-B2, X-B4, X-B5, X-B6 | TASK-RWB-TE-001-06, TASK-RWB-TE-001-07 | `./gradlew test --tests "th.co.scb.ace.demo.recovery.architecture.RecoveryBoundaryRulesTest"` green |
| TASK-RWB-TE-001-09 | **BND-3 fixture test** `RecoveryModulithFixtureTest` (TC-TE-001-03): `ApplicationModules.of("th.co.scb.ace.recoveryfixture.bnd3.broken", <ImportOption that keeps test classes, e.g. ImportOption.Predefined.ONLY_INCLUDE_TESTS>).verify()` throws (Modulith text names both modules and types); same for `.fixed` passes. `.cycle` throws on the cycle (Modulith behaviour, D-RCV-11). Before each `verify()`, assert that `ApplicationModules` lists the expected nested modules by name (for example `recovery.a`, `recovery.b`), so a pass cannot come from modules not being detected. If Modulith 2.1.2 cannot import the fixtures or does not detect the nested modules, **stop and report** (SPEC-007); do not add an ArchUnit BND-3 rule. | SPEC-007, -011; BR3; Flow 8; X-B3; D-RCV-11, -42; CLAR-005 A | TASK-RWB-TE-001-07 | `./gradlew test --tests "th.co.scb.ace.demo.recovery.architecture.RecoveryModulithFixtureTest"` green |
| TASK-RWB-TE-001-10 | **`RecoveryBoundaryTest`** (plain JUnit 5, untagged, no Spring context): load the real map; import main classes under `th.co.scb.ace.demo..` with `ImportOption.DoNotIncludeTests`; run the module-map check first, then BND-1, -2, -4, -5 (T-TE001-05). If existing main classes (for example RWB-E1-044's) break a rule, report it; do not weaken a rule or the map. | SPEC-001, -004, -012; BR6; Flow 3, Flow 6; TS-RCV-5 | TASK-RWB-TE-001-02, TASK-RWB-TE-001-06 | `./gradlew test --tests "th.co.scb.ace.demo.recovery.architecture.RecoveryBoundaryTest"` green |
| TASK-RWB-TE-001-11 | **JaCoCo recovery coverage** in `backend/build.gradle.kts` (shared file, PRE-2). If absent: `jacoco` plugin, `jacoco { toolVersion = "0.8.14" }`, `recoveryCoverageReport` (`JacocoReport`, XML + HTML) and `recoveryCoverageVerification` (`JacocoCoverageVerification`, BUNDLE rules COVEREDRATIO ≥ 0.80 for LINE, INSTRUCTION, BRANCH, METHOD), `executionData(tasks.test)`, `mustRunAfter(tasks.test)`, not wired into `check`/`build` (SPEC-RWB-E1-044-015 (d) shape). In either case: class directories = main output filtered `th/co/scb/ace/demo/recovery/**` plus test output filtered `th/co/scb/ace/demo/recovery/architecture/**`, excluding `**/*Test.class`, `**/*Test$*.class`; source directories main + test java. No other line of the file changes. | SPEC-017, -020; D-RCV-28 (3), -40, -43; TS-RCV-4 | TASK-RWB-TE-001-01 | `git diff backend/build.gradle.kts` limited to these lines; `./gradlew tasks --all \| grep recoveryCoverage` lists both; `./gradlew check --dry-run` does not list them |
| TASK-RWB-TE-001-12 | **Backend regression and coverage gate.** Run `./gradlew checkstyleMain checkstyleTest` (or `npx nx run backend:check`, as CI does) and `./gradlew test` (whole ACE suite incl. `ModulithTest`, T-TE001-06) then `./gradlew recoveryCoverageReport recoveryCoverageVerification` (T-TE001-10). Run `./gradlew test --rerun-tasks` a second time: same result (idempotency). Record durations vs the TASK-01 baseline. Save `build/test-results/test/*.xml` for recovery tests, the JaCoCo XML/HTML report and console output to `output/INC-002-epic-1-RWB-TE-001/implement/backend/`. Save checkstyle output too. Any failure (including a pre-existing ACE checkstyle failure, reported, not fixed), unexplained skip, or a metric below 80% blocks. | SPEC-012, -018, -020; T-TE001-06, -10; §12 Idempotency; TS-RCV-4, -5, -8 | TASK-RWB-TE-001-05, TASK-RWB-TE-001-08, TASK-RWB-TE-001-09, TASK-RWB-TE-001-10, TASK-RWB-TE-001-11 | Exit codes 0; JaCoCo LINE/INSTRUCTION/BRANCH/METHOD ≥ 80% read from the XML; evidence files present |

### Frontend Plan

| TASK ID | Description | Trace (SPEC/FR/NFR) | BLOCKED_BY | Verification |
|---|---|---|---|---|
| TASK-RWB-TE-001-13 | **Frontend folder.** Create `frontend/src/modules/recovery/index.ts` with one comment line (purpose: recovery module root, D-RCV-10) and `export {};`. No runtime statement. | SPEC-013; FS-1.1; D-RCV-10; CLAR-010 | TASK-RWB-TE-001-01 | `git ls-files frontend/src/modules/recovery` shows the file; `npx nx run frontend:typecheck` green |
| TASK-RWB-TE-001-14 | **ESLint recovery block.** In `frontend/eslint.config.js`: add `"src/modules/recovery/__fixtures__/**"` to the first `ignores` array; append one config object `{ files: ["src/modules/recovery/**/*.{ts,tsx}"], rules: { "no-restricted-imports": ["error", { patterns: [{ regex: "<plan.md §ESLint rule shape>", message: "<allowed set, D-RCV-39>" }] }] } }`. No other block changes. | SPEC-014; FS-1.2 (narrowed); D-RCV-08, -10, -23, -39; CLAR-002; X-F1 | TASK-RWB-TE-001-13 | `git diff frontend/eslint.config.js` shows only the ignore entry and the new block; `npx nx run frontend:eslint:lint` green; behaviour by TASK-RWB-TE-001-16 |
| TASK-RWB-TE-001-15 | **Vitest tooling and `test` target** (shared files, PRE-2). Lockfiles (REVIEW-RWB-TE-001-029). CI (`test`, `test_default_branch`: `npm ci` at the root) and the image build (`Dockerfile`: `COPY . ./`, `npm ci` in `/app`) install only from the **root `package-lock.json`**; no CI, Docker or Jenkins step reads `frontend/package-lock.json`. ACE still keeps it in step with the root file (commit 6f361e4a changed both by the same 58 lines), and SPEC-017 lists both. Steps: (1) from the workspace root `npm install -D --save-exact vitest@4.1.12 @vitest/coverage-v8@4.1.12 -w frontend` (updates `frontend/package.json` and the root lockfile); (2) from `frontend/` `npm install --package-lock-only --workspaces=false` (updates `frontend/package-lock.json` only; installs nothing). **Stop rule (blocking):** the root `package-lock.json` must contain `"node_modules/vitest"` and `"node_modules/@vitest/coverage-v8"` at 4.1.12, and `rm -rf node_modules frontend/node_modules && npm ci` at the root must succeed, as CI runs it; otherwise stop and report. **Sync check (non-blocking for the build):** `frontend/package-lock.json` must contain the same two entries; if step 2 does not produce them, record it in `implement/report.md` and tell the ACE tech lead in the OPEN-023 thread, with no hand edit and no other npm command. `git diff --stat` on both lockfiles: only vitest packages and their transitive dependencies. Create `frontend/vitest.config.ts` (node environment; include `src/modules/recovery/**/*.test.{ts,tsx}`; v8 coverage on `src/modules/recovery/**/*.{ts,tsx}` excluding `__tests__`, `__fixtures__`; thresholds 80 lines/statements/branches/functions; reporters `text`, `json-summary`, `lcovonly` (no HTML/JS report files that `eslint:lint` would lint); `reportsDirectory: "coverage/recovery"`; `@` alias). In `frontend/package.json` add `nx.targets.test` = `nx:run-commands`, `command: "vitest run --coverage"`, `cwd: "{projectRoot}"`, and append `"test"` to `nx.targets.check.dependsOn`. In `frontend/tsconfig.app.json` add `"exclude": ["src/modules/recovery/__tests__", "src/modules/recovery/__fixtures__"]`. `frontend/.prettierignore` already ignores `coverage`, so `check-format` is not affected; `.gitignore` does not, and editing it is outside the approved file list: do not commit `frontend/coverage/` (copy reports to `output/…/implement/frontend/`, then delete the folder). No change to `nx.json`, root `package.json` scripts, `.gitlab-ci.yml`. | SPEC-015, -017, -020; D-RCV-05, -06, -40, -43; CLAR-003 A; REVIEW-RWB-TE-001-015, -019 | TASK-RWB-TE-001-13 | root lockfile holds vitest 4.1.12 entries and a clean root `npm ci` succeeds (as CI and `Dockerfile` run it); `frontend/package-lock.json` sync result recorded; `npx nx show project frontend --json` shows exactly one `test` target, command `vitest run --coverage`, and `check.dependsOn` contains `test`; `git diff --stat` on lockfiles limited to vitest packages and their transitive deps |
| TASK-RWB-TE-001-16 | **Import-rule fixture test** (T-TE001-07). `frontend/src/modules/recovery/__tests__/importBoundary.test.ts` uses `new ESLint({ cwd: <frontend dir>, ignore: false })` with the real config and `lintFiles` on `__fixtures__/forbidden.ts` (`@/hooks/cfsc/x`, `@/api/tdr/config`, `@/pages/x`, `@/utils/cfscCaseList`, `@/modules/other/x`, `../x`, `../../hooks/cfsc/x`, `./../x`, `./sub/../../x`, `@/modules/recovery/../cfsc/x`, bare `..`, one per line (11 imports); the regex forbids any `..` segment, REVIEW-RWB-TE-001-023) and `__fixtures__/allowed.ts` (`@/components/ui/button`, `@/lib/utils`, `@/utils/date`, `@/contexts/ApiClientContext`, `@/api/schema`, `@/modules/recovery/casewf/x`, `./sibling`). Assert, on messages with `ruleId === "no-restricted-imports"` only: exactly one error per forbidden line, at that line; zero on `allowed.ts`; message names the allowed set. The test file itself has no `../` import. | SPEC-014, -015; T-TE001-07; X-F1; CLAR-002, -003 A | TASK-RWB-TE-001-14, TASK-RWB-TE-001-15 | `cd frontend && npx vitest run` green with 2 fixture assertions groups; mutation check: temporarily remove the recovery block → test fails (record, then restore) |
| TASK-RWB-TE-001-17 | **Frontend regression and coverage gate** (T-TE001-08). `npx nx run frontend:check` (runs `vite:build`, `check-format`, `eslint:lint`, `typecheck`, `test`), then run it a second time with `frontend/coverage/` present (use `--skip-nx-cache`): both green. Confirm `frontend/coverage/recovery/` holds no `.js`/`.html` file. Confirm normal lint reports nothing from `__fixtures__`, `typecheck` does not compile `__tests__`/`__fixtures__`, build output has no fixture. Expected coverage: `PASS` with 0/0 measurable statements recorded **exactly as printed** plus the file list (`index.ts`); no invented percentages. Save console output, `coverage/recovery/coverage-summary.json` and `coverage/recovery/lcov.info` to `output/INC-002-epic-1-RWB-TE-001/implement/frontend/`. | SPEC-013..-015, -018, -020; T-TE001-08; D-RCV-43 (3); TS-RCV-4 | TASK-RWB-TE-001-16 | Exit code 0; `grep -rn "__fixtures__" frontend/dist` empty; evidence files present |

### Cross-cutting, compliance and release

| TASK ID | Description | Trace (SPEC/FR/NFR) | BLOCKED_BY | Verification |
|---|---|---|---|---|
| TASK-RWB-TE-001-18 | **Guardrails, exclusions and shared-file footprint.** (1) `git diff --name-only develop...HEAD` equals the union of the Backend and Frontend layout tables in `plan.md` (plus RWB-E1-044 files if merged first); unchanged: `ModulithTest.java`, `application.yaml`, security config, `.gitlab-ci.yml`, Jenkins files, `nx.json`, root `package.json` scripts, other ACE packages. (2) No `RecoveryAccessGuard`, controller, `@RequestMapping`, `/api/recovery`, MSG-P4-002 in the diff (D-RCV-52). (3) No code owners file, contract test, adapter or agent client (SPEC-016). (4) PII/secret scan of the diff (no names, account numbers, tokens, URLs with credentials). (5) Fixtures and maps hold class/package names only. | SPEC-012, -016, -017, -019; §17; §19; D-RCV-05, -36; BS-4.3; CLAR-007, -009 | TASK-RWB-TE-001-12, TASK-RWB-TE-001-17 | Checklist with command output in `implement/report.md` |
| TASK-RWB-TE-001-19 | **Unit Test Evidence table** per `.github/rules/implementation-execution-gates.md`: one row per surface (Backend, Frontend) with Passed/Failed/Skipped and Statements/Branches/Functions/Lines % from the native reports (JaCoCo INSTRUCTION→Statements, METHOD→Functions; Vitest values as printed, 0/0 shown as the tool prints it), Required 80%, Status, Evidence links. No combined average. Any missing report or metric below 80% → `BLOCKED`. | SPEC-018, -020; TS-RCV-4; D-RCV-40, -43 | TASK-RWB-TE-001-12, TASK-RWB-TE-001-17 | Table in `implement/report.md` matches the saved native reports |
| TASK-RWB-TE-001-20 | **Release readiness and trace.** Record ACE branch, commit SHAs and MR link in `output/INC-002-epic-1-RWB-TE-001/implement/`; announce the shared-file edits and the new test-scope fixture root package `th.co.scb.ace.recoveryfixture` to the ACE team (OPEN-023 thread); notify the RWB-E1-044 planner that `build.gradle.kts` now holds the recovery JaCoCo tasks with the tooling class directory (D-RCV-43 (2)); update `requirement/Traceability_Matrix.md` CODE refs. Effective-screen coverage consolidation: `NOT_APPLICABLE` (UI NO, 0 screens) — record that line. Human verification HV-1 (MR pipeline log shows the new tests green) is listed for the recovery tech lead. Commit/push/MR only when the user asks (CLAUDE.md). | SPEC-001..-020 (trace); D-RCV-43; CLAUDE.md two-repository rule | TASK-RWB-TE-001-18, TASK-RWB-TE-001-19 | Files present; matrix rows carry TASK and CODE refs; HV-1 listed in `implement/report.md` |

## Dependency graph (DAG)

```text
00 ─► 01 ─┬─► 02 ───────────────────────────┐
          ├─► 03 ─► 04 ─┬─► 05 ─────────────┤
          │        │    └─► 06 ─┬─► 08 ─────┤
          │        └─► 07 ──────┤           ├─► 12 ─┐
          │             └───────┴─► 09 ─────┤       │
          │        (02,06) ─► 10 ───────────┤       ├─► 18 ─┐
          ├─► 11 ───────────────────────────┘       │       ├─► 20
          └─► 13 ─┬─► 14 ─┐                         ├─► 19 ─┘
                  └─► 15 ─┴─► 16 ─► 17 ─────────────┘
```

No cycle. Backend (02–12) and frontend (13–17) run in parallel after 01; no frontend task depends on a backend contract (no API).

## Requirement and spec coverage

| SPEC | Tasks |
|---|---|
| SPEC-RWB-TE-001-001 | 02, 10, 12 |
| SPEC-RWB-TE-001-002 | 03 |
| SPEC-RWB-TE-001-003 | 04, 05 |
| SPEC-RWB-TE-001-004 | 06, 08, 10 |
| SPEC-RWB-TE-001-005 | 06, 08 |
| SPEC-RWB-TE-001-006 | 06, 08 |
| SPEC-RWB-TE-001-007 | 02, 09, 12 |
| SPEC-RWB-TE-001-008 | 06, 08 |
| SPEC-RWB-TE-001-009 | 03, 06, 08 |
| SPEC-RWB-TE-001-010 | 06, 08 |
| SPEC-RWB-TE-001-011 | 07, 08, 09 |
| SPEC-RWB-TE-001-012 | 10, 12, 18 |
| SPEC-RWB-TE-001-013 | 13, 17 |
| SPEC-RWB-TE-001-014 | 14, 16 |
| SPEC-RWB-TE-001-015 | 15, 16, 17 |
| SPEC-RWB-TE-001-016 | 18 |
| SPEC-RWB-TE-001-017 | 00, 01, 11, 15, 18 |
| SPEC-RWB-TE-001-018 | 12, 17, 19 |
| SPEC-RWB-TE-001-019 | 03, 07, 18 |
| SPEC-RWB-TE-001-020 | 11, 12, 15, 17, 19 |

| FR / NFR / requirement | Tasks |
|---|---|
| FR-RWB-003 (REQ-DRI-006, BR5) | 03, 06, 07, 08 |
| FR-RWB-020 (BR-RWB-014, BR6) | 03, 04, 05, 06, 10 |
| CTX-CONSTRAINT-002, CTX-DELIVERY-004 (modular monolith, build-time boundaries) | 02, 06, 08, 09, 10, 12, 14, 16, 17 |
| CTX-CONSTRAINT-005 (no direct system-of-record call) | 06, 07, 08 |
| NFR: unit coverage 80% (TS-RCV-4, D-RCV-40) | 11, 12, 15, 17, 19 |

The spec references no NFR-* ID; the coverage gate is carried as TS-RCV-4 / D-RCV-40.

## Pre-submit checks

| Check | Result |
|---|---|
| Every scope bullet S1–S19 in `plan.md` maps to at least one TASK | YES (see `plan.md` §Scope) |
| Every in-scope SPEC-RWB-TE-001-001..020 maps to at least one TASK | YES (table above; 20/20) |
| No orphan TASK (each maps to ≥1 SPEC and has a verification) | YES (00–20) |
| Every TASK has explicit `BLOCKED_BY` (`NONE` only for TASK-00) | YES |
| Every spec Requirement-to-SPEC coverage row is in `plan.md` §Requirement Logic To Task Coverage with no `BLOCKED` row | YES (17/17) |
| Every unit-test task is `BLOCKED_BY` its implementation task, names synthetic fixtures and a concrete command | YES (05←04, 08←06/07, 09←07, 10←02/06, 16←14/15) |
| Unmapped effective-screen node groups | NONE — `NOT_APPLICABLE` (UI NO, 0 screens, `DESIGN_EVIDENCE_STATUS: NOT_REQUIRED`) |
| Effective-screen consolidation task before release readiness | `NOT_APPLICABLE`; recorded in TASK-20 |
| Orphaned SPEC-* mappings / dangling references | NONE |
| Placeholder IDs (`DUMMY-*`, `TBD`, `TBA`) | NONE |
| API tasks (spec `NO_API_CHANGE`) | None planned, correctly |
| Plan-approval preconditions | PRE-1 **APPROVED** (Jira `TB0001-1235` comment 1781003); PRE-2 (OPEN-023), PRE-3, PRE-4 **PENDING**; enforced by TASK-00 |
| Real PII, secrets, production data in plan outputs | NONE |

## v2 re-baseline addendum (16 November 2026)

The task table above (TASK-00..20) is preserved. One task is added for BND-6. It is the only new
build task; the rest re-verify the preserved implementation.

| TASK ID | Description | Trace (SPEC/FR/NFR) | BLOCKED_BY | Verification |
|---|---|---|---|---|
| TASK-RWB-TE-001-21 | **BND-6 ACE public-table rule.** Add `publicTableRule` to `RecoveryBoundaryRules` (test scope): scan SQL strings, JPA `@Table`, repository `@Query` and native queries for a qualified ACE table in `public`; allow only the 30 `v_ace_*` view names from `recovery-modules.yaml`. Add fixture `public.account` (fails) and `recovery.v_ace_account` (passes). Add the 30 names to the map's `allowedSourceObjects`. Add the assertion to `RecoveryBoundaryRulesTest` and `RecoveryBoundaryTest`. Update the spec coverage table to `SPEC-RWB-TE-001-021`. | SPEC-021; FR-RWB-013; D-RCV-51, -52; ADR-010; E1-069 | TASK-RWB-TE-001-10 | `./gradlew test --tests "th.co.scb.ace.demo.recovery.architecture.*"` green; negative fixture fails with the exact text; no `public.` in a passing recovery class |

### Updated coverage

| SPEC | Tasks |
|---|---|
| `SPEC-RWB-TE-001-021` | 21 |

| FR / NFR | Tasks |
|---|---|
| FR-RWB-013 (ACE read boundary) | 21 |

### Updated pre-submit checks

| Check | Result |
|---|---|
| Every in-scope SPEC-001..021 maps to a task | YES (21/21) |
| BND-6 has a failing and a passing fixture | YES (TASK-21) |
| No new runtime code, no new endpoint, no new dependency | YES |
| No question asked; assumptions recorded | YES (4) |
