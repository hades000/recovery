---
title: "Implementation Plan — RWB-TE-001 Recovery module folder and boundary test"
run_id: "INC-002-epic-1-RWB-TE-001"
story: "RWB-TE-001"
jira: "TB0001-1235"
status: "SUCCESS"
---

# Implementation Plan — RWB-TE-001 Recovery module folder and boundary test

Design Source: NOT_REQUIRED (`UI In Scope: NO`, `DESIGN_EVIDENCE_STATUS: NOT_REQUIRED`).

| Field | Value |
|---|---|
| Story | RWB-TE-001 (Jira `TB0001-1235`, epic `TB0001-1234`) |
| RUN_ID | `INC-002-epic-1-RWB-TE-001` |
| Input spec | `output/INC-002-epic-1-RWB-TE-001/specify/spec.md` (`status: SUCCESS`, SPEC-RWB-TE-001-001..020, `CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]`, `REQUIREMENT_COVERAGE_RESULT: SUCCESS [MISSING_RULES: 0] [CONTRADICTIONS: 0]`) |
| Spec contracts | `specify/contracts/backend-apis.json` (CON-RWB-TE-001-001, -002), `specify/contracts/frontend-integrations.json` (CON-RWB-TE-001-F01) |
| Plan contracts | `plan/contracts/backend-apis.json`, `plan/contracts/frontend-integrations.json` (spec contracts plus the plan's pinned names and versions) |
| Governing decisions | D-RCV-02, -05, -06, -10, -11, -16, -19, -20, -21, -23, -28 (3), -36..-43 |
| ACE baseline | `ace-monorepo` `develop` 96b0d1c6 |
| Prepared | 2026-11-16 (v2 re-baseline of the 9 November 2026 plan), Implementation Planner (agent run) |


## v2 re-baseline delta (16 November 2026)

The plan is the 9 November 2026 plan re-based onto document set v14. Scope, task structure and
evidence are unchanged; four additions apply.

| Change | Plan effect | Task |
|---|---|---|
| **BND-6** ACE `public` boundary rule | Add a rule and two fixtures; add the 30 view names to the module map as allowed source objects; add a test and a verification step. | `TASK-RWB-TE-001-21` |
| Decision renumbering | `D-RCV-36` (access guard) is now **D-RCV-52**; `D-RCV-35` (canonical story) is now **D-RCV-51**. References updated. | all |
| Schema and read path | No migration in this story. The map's allowed source objects are `recovery.v_ace_*` (30 views), not ACE `public` tables. | `TASK-RWB-TE-001-03`, `-21` |
| Preserved implementation | The existing BND-1..BND-5 code and evidence are the baseline. The plan does not recreate them; it adds BND-6 and re-verifies. | `TASK-RWB-TE-001-21` |

## Assumptions

| ID | Assumption | Basis |
|---|---|---|
| `ASM-008` | The 21 Tier 1 ACE tables are at the baseline head in DEV/SIT. | E1-069 |
| `ASM-016` | The 30 view names are the allowed source objects. | E1-069; ADR-010 |
| `L-RCV-03` | No question was asked; BND-6 is taken from E1-069 and ADR-010. | No-question rule |
| `L-RCV-04` | The existing BND-1..BND-5 implementation is preserved; only BND-6 is new. | Implementation evidence |

## Plan approval preconditions (not all met at plan time)

The plan is written but **not approved**. Implementation Builder must not start until every row below has a decision and a date. TASK-RWB-TE-001-00 checks them; every build task is `BLOCKED_BY` it.

| ID | Precondition | Owner | State on 2026-11-09 | Evidence when met |
|---|---|---|---|---|
| PRE-1 | Specification approval (backlog and specification gate) | Product Owner | **APPROVED** 2026-11-09 by Chitchaya Muanchonchana (TechX PO); Jira `TB0001-1235` comment 1781003, 2026-11-09 14:14: "No inquiry left for this ticket, This ticket is approved to continue by TechX PO" | Decision and date in `docs/increments/INC-002-epic-1-RWB-TE-001.md` "Owners and approvals" |
| PRE-2 | OPEN-023: approve `vitest` 4.1.12, `@vitest/coverage-v8` 4.1.12, the Gradle `jacoco` plugin (tool 0.8.14), and edits to `frontend/package.json`, `frontend/tsconfig.app.json`, `frontend/eslint.config.js`, new `frontend/vitest.config.ts`, `package-lock.json`, `frontend/package-lock.json`, `backend/build.gradle.kts`; and the new test-scope fixture root package `th.co.scb.ace.recoveryfixture` (outside the module namespace; REVIEW-RWB-TE-001-026) | ACE tech lead | **APPROVED** 2026-11-09 by Pongchai Charoenrungrodkun (ACE and Recovery lead; PIPAT SAENGOW, ACE tech lead, was asked); Jira `TB0001-1235` comment 1781273, 2026-11-09 15:27: "อนุมัติ OPEN-023 สำหรับ RWB-TE-001" | OPEN-023 moved to "Settled" with the ruling and date |
| PRE-3 | Plan approval | Forward Deployed Architect (Jesniphat Pukkham, D-RCV-15) | **APPROVED** 2026-11-09 15:32, given by Jesniphat Pukkham in the AISDLC Claude Code session ("approve plan และ task"), after PRE-1, PRE-2 and plan gate 3 (Low-only) | Decision and date in the increment card |
| PRE-4 | Task approval | Forward Deployed Engineer (Jesniphat Pukkham, D-RCV-15) | **APPROVED** 2026-11-09 15:32, given by Jesniphat Pukkham in the AISDLC Claude Code session ("approve plan และ task"), after PRE-1, PRE-2 and plan gate 3 (Low-only) | Decision and date in the increment card |

If PRE-2 is refused or changes a version or a file, the plan is re-run; the Builder does not substitute another runner or tool.

## Upstream review disposition (human, 2026-11-09)

Spec gate review 3 (`review/spec-gate-review-3.md`): `REVIEW_STATUS: FAIL`, Low only, non-blocking. The human starting this stage accepted the open Low findings as stale text with no scope change:

| Finding | Severity | Human disposition | Effect on plan |
|---|---|---|---|
| REVIEW-RWB-TE-001-001 | Low | Accepted (stale text, superseded BA spec) | None |
| REVIEW-RWB-TE-001-003 | Low | Accepted (stale text, superseded BA spec) | None |
| REVIEW-RWB-TE-001-019 | Low | Accepted (three stale lines). The plan follows SPEC-015 / D-RCV-43 (hand-defined `test` target, not the inferred one of `compliance-validation.md:66`) and SPEC-020 (expected frontend coverage `PASS` with 0/0 recorded as printed) | TASK-15, TASK-17, TASK-19 carry the correct text |

The `FAIL` status and the findings stay visible; they are not relabelled.

### Plan gate 1 (2026-11-09, `review/plan-gate-review.md`)

`REVIEW_STATUS: FAIL`, Medium 2, Low 6, blocking. Human instruction 2026-11-09: fix REVIEW-RWB-TE-001-021..027 as proposed and re-run the plan gate. -028 (CRLF lost in the card and matrix) was fixed by the planner the same day.

| Finding | Sev. | Fix in this plan |
|---|---|---|
| -021 | Medium | Vitest reporter `lcovonly` (no HTML/JS); TASK-17 runs `frontend:check` twice |
| -022 | Medium | `checkstyleMain checkstyleTest` in TASK-02 and TASK-12; line-length note in TASK-04/-06; §Backend Plan Checkstyle |
| -023 | Low | Regex forbids any `..` segment; fixtures `./../x`, `./sub/../../x`, `@/modules/recovery/../cfsc/x` |
| -024 | Low | `LoaderOptions` + `SafeConstructor` in TASK-04 |
| -025 | Low | `bnd3.cycle` fixture; real nested layout; module-detection assertion (TASK-07, -09) |
| -026 | Low | Fixture root added to PRE-2 / OPEN-023, TASK-00 and the TASK-20 ACE notice |
| -027 | Low | `npm install -D ... -w frontend` from the root; `git diff` on both lockfiles (TASK-15); superseded by -029 |

### Plan gate 2 (2026-11-09, `review/plan-gate-review-2.md`)

`REVIEW_STATUS: FAIL`, Medium 1, Low 1, blocking. Human instruction 2026-11-09: fix -029 by checking which lockfile the build uses and making the lockfile CI installs from the one the stop rule checks; fix -030. Same instruction recorded PRE-1 as APPROVED.

| Finding | Sev. | Fix in this plan |
|---|---|---|
| -029 | Medium | CI and `Dockerfile` install from the root lockfile only (checked). TASK-15: root command, then `npm install --package-lock-only --workspaces=false` in `frontend/`; blocking stop rule on the root lockfile + clean root `npm ci`; frontend lockfile sync recorded, non-blocking |
| -030 | Low | Bare `..` added to `forbidden.ts` (11 imports) in TASK-16, plan, scenarios |

### Plan gate 3 (2026-11-09, `review/plan-gate-review-3.md`)

Low-only, not blocking. Human instruction 2026-11-09 (recovery tech lead): fix both text findings without a gate re-run.

| Finding | Sev. | Disposition |
|---|---|---|
| -031 | Low | Fixed: `contracts/frontend-integrations.json` `forbidden` now says every import with a `..` segment at any position, matching the regex |
| -032 | Low | Fixed: increment card PO-gate sentence and stage updated (spec approved 2026-11-09; stage = plan) |

## Change scope (carried from spec)

| Field | Value |
|---|---|
| Change Type | `NEW_STORY` |
| UI In Scope | `NO` |
| Logic In Scope | `YES` (BND-1..BND-5, module-map rule, fixtures) |
| API In Scope | `NO` (`NO_API_CHANGE`; `RecoveryAccessGuard` moved to RWB-E1-022, D-RCV-52) |
| Frontend Changes Required | `YES` (folder, ESLint block, Vitest fixture test; no runtime code) |
| Backend Changes Required | `YES` (`package-info.java` in main scope; all executable classes in test scope) |
| Database / Flyway | None |
| Feature flag | None (build check). Rollback is a revert merge request. |

## Plan-time verification of spec "plan confirms" items

| Item (spec) | Check run at plan time | Result | Plan decision |
|---|---|---|---|
| SPEC-017: ArchUnit and SnakeYAML on the test classpath | `./gradlew dependencies --configuration testRuntimeClasspath --offline` and `--configuration testCompileClasspath` in `ace-monorepo/backend` (2026-11-09) | `com.tngtech.archunit:archunit:1.4.2` (via `spring-modulith-core` 2.1.2) and `org.yaml:snakeyaml:2.7` on both classpaths | **No `testImplementation` line.** No new backend library. |
| SPEC-007: can Modulith import test-scope fixtures | `javap` on `spring-modulith-core-2.1.2.jar` `ApplicationModules` | `of(String, ImportOption)` and `of(Class, ImportOption)` exist | TC-TE-001-03 calls `ApplicationModules.of("<fixture root>", <ImportOption that keeps test classes>)`. Not a stop. Builder re-confirms at TASK-09; if it fails, Builder stops and reports (SPEC-007). |
| SPEC-011: fixture root name | `AppConfig` has `@EnableJpaRepositories(basePackages = "th.co.scb.ace.demo")`; test classes are on the classpath of every ACE `@SpringBootTest` | Fixture repositories or entities under `th.co.scb.ace.demo..` would be scanned by ACE Spring tests | Fixture root **`th.co.scb.ace.recoveryfixture`** (outside `th.co.scb.ace.demo`), so neither Spring Data, JPA, component scan nor `ModulithTest` sees it. |
| SPEC-003/-004: test tooling package | spec "plan names the package" | — | **`th.co.scb.ace.demo.recovery.architecture`** under `backend/src/test/java`: `ModuleMap` (immutable model), `ModuleMapLoader`, `RecoveryBoundaryRules` (rule factory), and the tests. No Spring annotation, entity or repository in it. |
| SPEC-013: placeholder file | spec "file name is a plan detail" | — | `frontend/src/modules/recovery/index.ts` holding one comment line and `export {};` (no runtime statement). |
| SPEC-015: test file name | spec "plan may rename" | — | Keep `frontend/src/modules/recovery/__tests__/importBoundary.test.ts`; fixtures `__fixtures__/forbidden.ts`, `__fixtures__/allowed.ts`. |
| SPEC-017: frontend versions | `npm view vitest@4.1 peerDependencies.vite` → `^6.0.0 \|\| ^7.0.0 \|\| ^8.0.0`; `@vitest/coverage-v8@4.1.12` exists | ACE frontend uses `vite ^8.0.4`; CI image `node:22-trixie` | Pin exact `vitest` **4.1.12** and `@vitest/coverage-v8` **4.1.12** (coverage-v8 requires the same vitest version). Subject to PRE-2. |
| SPEC-020: JaCoCo tool | Gradle cache holds `org.jacoco.agent` 0.8.14; toolchain Java 21; Gradle 9.4.1 | — | `jacoco { toolVersion = "0.8.14" }`. Subject to PRE-2. |
| SPEC-015: one `test` target | `npx nx show project frontend` | **Not run**: no `node_modules` in `ace-monorepo` at plan time | Builder runs it in TASK-15 after `npm ci`; must show exactly one `test` target whose command is `vitest run --coverage`. If Nx infers a second test-like target or merges differently, Builder stops and reports. |
| Which lockfile the build installs from (REVIEW-RWB-TE-001-029) | `.gitlab-ci.yml` jobs `test` and `test_default_branch`; `Dockerfile`; `jenkins/`; `git log` of both lockfiles | CI and `Dockerfile` run `npm ci` at the workspace root only; nothing reads `frontend/package-lock.json`; ACE commit 6f361e4a changed both lockfiles by the same 58 lines | Root lockfile is the blocking check in TASK-15; `frontend/package-lock.json` is synced with `npm install --package-lock-only --workspaces=false` in `frontend/` and recorded, not blocking |
| RWB-E1-044 merge order | `ace-monorepo` `develop` 96b0d1c6: no `recovery` package, no `jacoco` in `backend/build.gradle.kts`; INC-001 has no plan yet | E1-044 not merged | TASK-11 creates the JaCoCo plugin and both recovery tasks (SPEC-RWB-E1-044-015 (d) shape) plus the tooling class directory. Builder re-checks at TASK-01; if E1-044 has merged by then, TASK-11 only adds the class directory and TASK-02 keeps `recovery.casewf.internal.migration`. |

## Scope

Each bullet maps to tasks in `tasks.md`.

| # | Scope bullet | TASK-* |
|---|---|---|
| S1 | Check plan-approval preconditions; create ACE branch; record merge order with RWB-E1-044 | TASK-00, TASK-01 |
| S2 | Main-scope module skeleton: recovery root + 19 nested modules with `api` / `internal` (`package-info.java` only) | TASK-02 |
| S3 | Module map `recovery-modules.yaml` (test resource) | TASK-03 |
| S4 | `ModuleMap` / `ModuleMapLoader` with validation, and its unit test | TASK-04, TASK-05 |
| S5 | Rule factory: module-map rule (a)–(f), BND-1, BND-2, BND-4, BND-5, failure text | TASK-06 |
| S6 | Backend fixtures and fixture maps outside `th.co.scb.ace.demo` | TASK-07 |
| S7 | Rule tests on fixtures (BND-1, -2, -4, -5, map rule, text, empty sets, name boundary) | TASK-08 |
| S8 | BND-3 through Modulith `verify()` on a fixture module set | TASK-09 |
| S9 | `RecoveryBoundaryTest` on real main classes and the real map | TASK-10 |
| S10 | JaCoCo recovery-only coverage tasks incl. test-scope tooling class directory | TASK-11 |
| S11 | Backend regression and coverage gate | TASK-12 |
| S12 | Frontend folder with placeholder | TASK-13 |
| S13 | ESLint recovery allow-list block and fixture ignore | TASK-14 |
| S14 | Vitest + coverage tooling, `test` target in `check`, `tsconfig.app.json` exclude, lockfiles | TASK-15 |
| S15 | Frontend fixture test of the import rule | TASK-16 |
| S16 | Frontend `check` regression and coverage gate | TASK-17 |
| S17 | Guardrails, scope exclusions and shared-file footprint check | TASK-18 |
| S18 | Unit Test Evidence table across both surfaces | TASK-19 |
| S19 | Release readiness: ACE commit/MR record, traceability, notices (ACE team, RWB-E1-044 planner) | TASK-20 |

## Backend Plan

Status: **REQUIRED**. Changes: `package-info.java` in main scope (SPEC-001); test-scope map, loader, rule factory, tests and fixtures (SPEC-002..-012); `backend/build.gradle.kts` JaCoCo (SPEC-017, -020).

### Package and file layout

| Path (under `ace-monorepo/backend/`) | Scope | Content |
|---|---|---|
| `src/main/java/th/co/scb/ace/demo/recovery/package-info.java` | main | `@ApplicationModule(displayName = "Recovery")` (closed, default type) |
| `src/main/java/th/co/scb/ace/demo/recovery/<name>/package-info.java` ×19 | main | `@ApplicationModule` (nested module) |
| `src/main/java/th/co/scb/ace/demo/recovery/<name>/api/package-info.java` ×19 | main | `@NamedInterface("api")` |
| `src/main/java/th/co/scb/ace/demo/recovery/<name>/internal/package-info.java` ×19 | main | no annotation |
| `src/test/resources/architecture/recovery-modules.yaml` | test resource | Map per `data-model.md` |
| `src/test/java/th/co/scb/ace/demo/recovery/architecture/` | test | `ModuleMap`, `ModuleMapLoader`, `RecoveryBoundaryRules`, `RecoveryBoundaryTest`, `ModuleMapLoaderTest`, `RecoveryBoundaryRulesTest`, `RecoveryModulithFixtureTest` |
| `src/test/java/th/co/scb/ace/recoveryfixture/**` | test | Fixture classes (class and package names only) |
| `src/test/resources/architecture/fixtures/*.yaml` | test resource | Fixture maps and invalid loader inputs |
| `build.gradle.kts` | shared | `jacoco` plugin, `recoveryCoverageReport`, `recoveryCoverageVerification` |

`<name>` in this order with codes: `dataengine` P1, `integration` P2, `casewf` P3, `access` P4, `dochub` P5, `comms` P6, `decision` P7, `payments` P8, `reporting` P9, `agent` P10, `valuation` S1, `treatment` S2, `guarantee` S3, `litigation` S4, `asset` S5, `debtsale` S6, `writeoff` S7, `deviation` S8, `partner` S9 (story §13 Package, confirmed in the story file).

Main scope adds 58 `package-info.java` files and nothing else. If `recovery.casewf.internal.migration` exists (RWB-E1-044), it is kept unchanged and gets no `package-info.java` from this story beyond those listed.

### Rule factory design (test scope)

- `RecoveryBoundaryRules.from(ModuleMap)` returns the module-map check and four ArchUnit `ArchRule`s: BND-1, BND-2, BND-4, BND-5. No recovery package literal in the class (BR6).
- Module-map check (SPEC-004) runs first against `JavaClasses` and returns all failures in one result: (a) root sub-package not in the map, counting classes in any sub-package; (b) map module package missing; (c) type other than `package-info` in the root package; (d) `@NamedInterface` package ↔ `published` list in both directions; (e) public type directly in `recovery.<name>` (ignore `package-info`); (f) type-level `@NamedInterface` anywhere under the root. Texts exactly as SPEC-004.
- BND-1 / BND-2: `noClasses().that().resideInAPackage(root..).should().dependOnClassesThat(<under external root and not in a published package>)`, `allowEmptyShould(true)`.
- BND-4: entity = annotated `jakarta.persistence.Entity`; repository = assignable to `org.springframework.data.repository.Repository`; dependency allowed only if in the same recovery module (by map module package).
- BND-5: name-boundary match (`n.equals(e) || n.startsWith(e + ".") || n.startsWith(e + "$")`); allowed only in or under the module's `clientPackages`.
- Failure text (SPEC-010): a custom `ArchCondition` emits `Rule {code} broken: {class} depends on {dependency}. Use {module}.api or an application event.` one line per violation; `{module}` is the target's map name (BND-1, -2, -4) or `integration.adapter` / `agent.client` (BND-5). All violations of a rule are collected in one run.
- BND-3 (SPEC-007): no ArchUnit rule. Real code: existing `ModulithTest` unchanged. Fixtures: `RecoveryModulithFixtureTest` with `ApplicationModules.of("th.co.scb.ace.recoveryfixture.bnd3.<case>", <ImportOption keeping test classes>).verify()` for cases `broken`, `fixed` and `cycle`. Each case copies the real layout: a closed `recovery` module (`@ApplicationModule` on its `package-info`) with nested modules (`@ApplicationModule`), each with `api` (`@NamedInterface("api")`) and `internal`. Before `verify()`, the test asserts that Modulith detected the expected nested modules (by name), so a pass cannot come from modules not being found (REVIEW-RWB-TE-001-025).
- Loader parsing: SnakeYAML 2.x `new Yaml(new SafeConstructor(options))` with `LoaderOptions` (`setAllowDuplicateKeys(false)`); not `LoadSettings` (snakeyaml-engine, not on the classpath; REVIEW-RWB-TE-001-024).
- Checkstyle: ACE applies the Gradle `checkstyle` plugin (13.5.0, severity `error`; LineLength 100, Indentation 4, CustomImportOrder) and CI runs `backend:check`, which includes `checkstyleMain` and `checkstyleTest`. All new main and test Java files must pass it; long failure-text literals are split (concatenation or text block) to stay within 100 characters. No suppression and no checkstyle config change. Pre-existing ACE checkstyle failures are reported as blockers, not fixed (REVIEW-RWB-TE-001-022).

### Coverage (SPEC-020)

- `recoveryCoverageReport` (`JacocoReport`) and `recoveryCoverageVerification` (`JacocoCoverageVerification`), `executionData` from `test`, `mustRunAfter(test)`, not wired to `check` or `build` (D-RCV-28 (3)).
- Class directories: `sourceSets.main.output` filtered to `th/co/scb/ace/demo/recovery/**` **plus** `sourceSets.test.output` filtered to `th/co/scb/ace/demo/recovery/architecture/**`, excluding `**/*Test.class` and `**/*Test$*.class`. Fixtures under `th/co/scb/ace/recoveryfixture/**` are outside both filters.
- Rules: 80% COVEREDRATIO for LINE, INSTRUCTION, BRANCH, METHOD at BUNDLE level.
- Report outputs: XML + HTML under `backend/build/reports/jacoco/recoveryCoverageReport/`.
- Side effect: applying the `jacoco` plugin attaches the agent to every `Test` task (`test`, `testE2E`). Accepted; Builder records `test` duration before and after (spec §Observability).

## Frontend Plan

Status: **REQUIRED** (build configuration and test only; no screen, route, component, state or i18n key).

| Path (under `ace-monorepo/`) | Change |
|---|---|
| `frontend/src/modules/recovery/index.ts` | New placeholder: comment + `export {};` |
| `frontend/eslint.config.js` | Add `"src/modules/recovery/__fixtures__/**"` to the first `ignores` entry; append one block `files: ["src/modules/recovery/**/*.{ts,tsx}"]`, `rules: { "no-restricted-imports": ["error", { patterns: [...] }] }` |
| `frontend/vitest.config.ts` | New: `test.environment: "node"`, `test.include: ["src/modules/recovery/**/*.test.{ts,tsx}"]`, `coverage.provider: "v8"`, `coverage.include: ["src/modules/recovery/**/*.{ts,tsx}"]`, `coverage.exclude: ["src/modules/recovery/__tests__/**", "src/modules/recovery/__fixtures__/**"]`, `coverage.thresholds: { lines: 80, statements: 80, branches: 80, functions: 80 }`, reporters `text`, `json-summary`, `lcovonly` (no HTML/JS output, so `eslint:lint` never sees report files; REVIEW-RWB-TE-001-021), `reportsDirectory: "coverage/recovery"`; `resolve.alias` `@` → `./src` |
| `frontend/package.json` | devDependencies `vitest` `4.1.12`, `@vitest/coverage-v8` `4.1.12`; `nx.targets.test` = `{ "executor": "nx:run-commands", "options": { "command": "vitest run --coverage", "cwd": "{projectRoot}" } }`; `"test"` appended to `nx.targets.check.dependsOn` |
| `frontend/tsconfig.app.json` | `"exclude": ["src/modules/recovery/__tests__", "src/modules/recovery/__fixtures__"]` |
| `package-lock.json`, `frontend/package-lock.json` | Root lockfile (the one CI and `Dockerfile` install from with `npm ci`) updated by `npm install -D --save-exact vitest@4.1.12 @vitest/coverage-v8@4.1.12 -w frontend` from the workspace root; `frontend/package-lock.json` (read by no build step; kept in step by ACE convention and SPEC-017) synced by `npm install --package-lock-only --workspaces=false` in `frontend/`. Root lockfile + clean root `npm ci` is the blocking check; frontend lockfile sync is recorded (REVIEW-RWB-TE-001-027, -029) |
| `frontend/src/modules/recovery/__tests__/importBoundary.test.ts` | Vitest test, ESLint Node API |
| `frontend/src/modules/recovery/__fixtures__/forbidden.ts`, `allowed.ts` | One import per line |

Not changed: `nx.json`, root `package.json`, `.gitlab-ci.yml`, `vite.config.ts`, `tsconfig.json`, `tsconfig.node.json`, every other ESLint block.

### ESLint rule shape (SPEC-014)

Patterns are text matches (the rule does not resolve paths). Acceptance is T-TE001-07, not the exact pattern form. Use one `patterns` entry with `regex` (ESLint 9), not `group` negations: gitignore-style negation cannot re-include a child (`@/components/ui/...`) once a parent (`@/**`) is excluded, so a negation list is fragile. Intended regex:

```text
(?:^|/)\.\.(?:/|$)|^@/(?!(?:components/ui(?:/|$)|lib/utils$|contexts/ApiClientContext$|api/schema$|modules/recovery(?:/|$)|utils/(?!cfsc)[^/]+$))
```

Branch 1 forbids any `..` path segment anywhere in the import text (`../x`, `./../x`, `./sub/../../x`, bare `..`, `@/modules/recovery/../cfsc/x`). `no-restricted-imports` offers no hook to normalise a path before matching, so this is how "normalise, then check" is applied (REVIEW-RWB-TE-001-023): any import that could climb is rejected outright. It is stricter than SPEC-014 (ii) for paths such as `./sub/../x` that would resolve inside the folder; recovery code writes those as `./x` instead. Branch 2 forbids every `@/` import except the allow-list; `@/utils/<file>` is allowed only one level deep and not when the name starts with `cfsc`. `./…` without `..` and third-party imports never match. Checked on 2026-11-09 with node against all T-TE001-07 cases plus the cases above.

Message names the allowed set: `Recovery code may import only @/modules/recovery/**, ./, @/components/ui/**, @/lib/utils, @/utils/<top-level, not cfsc*>, @/contexts/ApiClientContext, @/api/schema (D-RCV-39).`

The recovery folder files must also satisfy the existing blocks (TypeScript recommended, react-hooks). The fixture test asserts only on `ruleId === "no-restricted-imports"` messages, because fixture imports are unused and unresolved.

### Fixture test design (SPEC-015)

- `new ESLint({ cwd: <frontend dir>, ignore: false })` loads the real `eslint.config.js`; `lintFiles` on the two fixture files (their paths are inside `src/modules/recovery/`, so the recovery block applies).
- `forbidden.ts`: 11 imports (`@/hooks/cfsc/x`, `@/api/tdr/config`, `@/pages/x`, `@/utils/cfscCaseList`, `@/modules/other/x`, `../x`, `../../hooks/cfsc/x`, `./../x`, `./sub/../../x`, `@/modules/recovery/../cfsc/x`, bare `..`; 11 imports) → exactly one `no-restricted-imports` error on each line.
- `allowed.ts`: 7 imports (`@/components/ui/button`, `@/lib/utils`, `@/utils/date`, `@/contexts/ApiClientContext`, `@/api/schema`, `@/modules/recovery/casewf/x`, `./sibling`) → zero `no-restricted-imports` messages.
- Locate the frontend dir from `import.meta.url` or `process.cwd()` (target runs with `cwd: {projectRoot}`); no `../` import statements in the test file (the rule applies to it too).

## Integration and cross-layer

No API. No frontend task depends on a backend contract; the two surfaces are independent and can run in parallel after TASK-01. Both run in the existing CI `check` target (`nx affected -t check` on merge requests, `nx run-many -t check` on the default branch; D-RCV-05). The JaCoCo recovery tasks run on demand (outside `check`, D-RCV-28 (3)); their evidence is collected by the Builder.

## Unit Test Applicability

| Surface | Changes Required | Unit Tests | Coverage Gate | Trace | Reason | Tasks |
|---|---|---|---|---|---|---|
| Backend | YES | REQUIRED | 80% LINE, INSTRUCTION, BRANCH, METHOD by `recoveryCoverageVerification` over main `th/co/scb/ace/demo/recovery/**` + test tooling `th/co/scb/ace/demo/recovery/architecture/**` (excl. `*Test`) | SPEC-001..-012, -017, -018, -020 | Executable code is the test-scope loader and rule factory (D-RCV-52, -37, -43) | TASK-05, -08, -09, -10, -12 |
| Frontend | YES | REQUIRED | 80% lines, statements, branches, functions by `@vitest/coverage-v8` on `src/modules/recovery/**/*.{ts,tsx}` excl. `__tests__`, `__fixtures__`. **Expected `PASS` with 0/0 measurable statements recorded exactly as printed** (placeholder only; SPEC-020, D-RCV-43 (3)); the rule is proven by T-TE001-07 | SPEC-013..-015, -020 | Folder + ESLint rule; Vitest test runs ESLint Node API (CLAR-003 A) | TASK-16, -17 |

Final verification across both surfaces: TASK-19.

## Requirement Logic To Task Coverage

| REQ_REF | Mapped SPEC-* | Mapped TASK-* | Coverage Type | Verification | Status |
|---|---|---|---|---|---|
| Flow 1 / §13 step 1 | SPEC-001, -013 | TASK-02, TASK-13 | DIRECT_IMPLEMENTATION | 58 `package-info.java` count; T-TE001-05; `ModulithTest`; T-TE001-08 | COVERED |
| Flow 2 / §13 step 2 | SPEC-002, -003 | TASK-03, TASK-04, TASK-05 | DIRECT_IMPLEMENTATION | T-TE001-01; map diff against `data-model.md` | COVERED |
| BR1 | SPEC-005 | TASK-06, TASK-07, TASK-08 | DIRECT_IMPLEMENTATION | TC-TE-001-01; T-TE001-03 | COVERED |
| BR2 | SPEC-006 | TASK-06, TASK-07, TASK-08 | DIRECT_IMPLEMENTATION | TC-TE-001-02; T-TE001-03 | COVERED |
| BR3 | SPEC-004, -007 | TASK-02, TASK-06, TASK-09, TASK-12 | DIRECT_IMPLEMENTATION (fixture) + INHERITED_EXISTING_BEHAVIOR (`ModulithTest` unchanged) | TC-TE-001-03; T-TE001-02 (d)(e)(f); `ModulithTest` green in T-TE001-06 | COVERED |
| BR4 | SPEC-008 | TASK-06, TASK-07, TASK-08 | DIRECT_IMPLEMENTATION | TC-TE-001-04 (recovery entity/repo and outside-root entity) | COVERED |
| BR5 | SPEC-009 | TASK-03, TASK-06, TASK-07, TASK-08 | DIRECT_IMPLEMENTATION | TC-TE-001-05; T-TE001-09 | COVERED |
| BR6 | SPEC-002, -003, -004 | TASK-03, TASK-04, TASK-06, TASK-08, TASK-10 | DIRECT_IMPLEMENTATION | TC-TE-001-07; T-TE001-01, -02, -05; grep: no recovery package literal in `RecoveryBoundaryRules`/`ModuleMapLoader` | COVERED |
| Flow 3 / §13 step 3–4 | SPEC-010, -011 | TASK-06, TASK-07, TASK-08, TASK-10 | DIRECT_IMPLEMENTATION | TC-TE-001-01..-05, -07; T-TE001-04 | COVERED |
| Flow 4 / §13 step 5 | SPEC-014, -015 | TASK-14, TASK-15, TASK-16 | DIRECT_IMPLEMENTATION | T-TE001-07 | COVERED |
| Flow 5 / §12 / §13 step 6 / X7 / TC-TE-001-08 / MSG-P4-002 | SPEC-016 | TASK-18 | DIRECT_IMPLEMENTATION (exclusion check) | grep: no `RecoveryAccessGuard`, no controller, no `/api/recovery` in diff; moved to RWB-E1-022 | COVERED |
| Flow 6 / §12 Trigger / §13 step 7 | SPEC-012 | TASK-10, TASK-15, TASK-18 | INHERITED_EXISTING_BEHAVIOR (CI `check`) + DIRECT_IMPLEMENTATION (`test` in frontend `check`) | `.gitlab-ci.yml` unchanged in diff; MR pipeline `test` job green (human gap HV-1) | COVERED |
| Flow 7 / §14 | SPEC-010 | TASK-06, TASK-08 | DIRECT_IMPLEMENTATION | T-TE001-04 exact text; TC-TE-001-07 text | COVERED |
| Flow 8 | SPEC-007, -010 | TASK-06, TASK-09 | DIRECT_IMPLEMENTATION | TC-TE-001-03 second case passes; message names `{module}.api` | COVERED |
| §12 Idempotency / Restart | SPEC-012 | TASK-12, TASK-17 | DIRECT_IMPLEMENTATION | Run `./gradlew test --rerun-tasks` twice, same result; no Spring context, no Docker, no DB | COVERED |
| §17 Guardrails | SPEC-011, -019 | TASK-07, TASK-18 | DIRECT_IMPLEMENTATION | Fixture review: class/package names only; PII/secret grep | COVERED |
| §19 Out of scope | SPEC-016 | TASK-18 | DIRECT_IMPLEMENTATION (exclusion check) | Diff has no code owners, contract tests, adapter, agent client | COVERED |

Exception rows (spec §Exceptional-case behaviour): X-B1 → TASK-08 (TC-01); X-B2 → TASK-08 (BND-2 breaking fixture); X-B3 → TASK-09 (TC-03); X-B4 → TASK-08 (TC-04); X-B5 → TASK-08 (TC-05, T-09); X-B6 → TASK-08 (TC-07, T-02); X-B7 → TASK-05 (T-01); X-F1 → TASK-16 (T-07); X7 → TASK-18 (not built).

Resolved clarifications carried: CLAR-001 A → TASK-06/-08 (BND-4 covers ACE `model`/`repository`); CLAR-002 → TASK-14/-16; CLAR-003 A → TASK-15/-16; CLAR-004 A → TASK-03; CLAR-005 A → TASK-09 (Modulith text accepted); CLAR-006 B → TASK-03/-06; CLAR-007 → TASK-18; CLAR-008 → TASK-03; CLAR-009 → TASK-18; CLAR-010 → TASK-02/-13; CLAR-011 → TASK-08 (T-03); CLAR-012 → TASK-01/-02.

## Functional Test Scenarios

| Scenario | Owner | Applicability | Note |
|---|---|---|---|
| API scenarios | API Tester | NOT_APPLICABLE | `API In Scope: NO`, `NO_API_CHANGE`; increment card lists API Tester "Not used" |
| UI workflow scenarios | Functional Automation Test | NOT_APPLICABLE | `UI In Scope: NO`; no screen; card lists FAT "Not used" |
| HV-1: the GitLab MR pipeline `test` job runs the new backend tests and frontend `check` (incl. `test`) on the TE-001 MR | Human verification (recovery tech lead) | Gap requiring human verification | Read the MR pipeline log: `RecoveryBoundaryTest`, `ModulithTest`, `vitest run --coverage` present and green. Not an executed automated test. |
| HV-2: a violation in a real MR fails the pipeline (Flow 7) | Human verification | Gap requiring human verification | Proven locally by fixture tests (TC-*, T-TE001-07); a deliberately broken MR is not required. |

All acceptance (D-RCV-16, TS-RCV-7) is unit-level: see `tests/scenarios.md`.

## Screen-to-task mapping

`NOT_APPLICABLE`: `UI In Scope: NO`, `DESIGN_EVIDENCE_STATUS: NOT_REQUIRED`, 0 screens. No visual-fidelity, screenshot or component-inventory task; `plan/frontend/components.md` not created (agent rule for UI NO).

## Security, privacy, compliance

- Authentication / authorization: none added (D-RCV-52). Audit, KYC/AML, suitability, consent, maker-checker: not applicable (no business data, no runtime path).
- Data protection: fixtures, maps and failure texts hold class and package names only (SPEC-019, BS-4.3); TASK-18 greps the diff.
- Shared-file discipline (CLAUDE.md): only the files in the Backend/Frontend layout tables are touched; TASK-18 compares `git diff --name-only` to that list.
- Never run against a shared database: these tests start no Spring context and no database (TS-RCV-8).

## Risks

| Risk | Mitigation | Task |
|---|---|---|
| ACE tech lead refuses or changes Vitest/JaCoCo (PRE-2) | Re-run planner; no substitution by Builder | TASK-00 |
| Nx merges an inferred `test` target with the hand-defined one | `npx nx show project frontend --json` check; stop on mismatch | TASK-15 |
| New Java files fail ACE checkstyle in CI while `./gradlew test` is green | `checkstyleMain checkstyleTest` in TASK-02 and TASK-12; long strings split | TASK-02, -04, -06, -12 |
| JaCoCo agent on `test` slows ACE suite | Record durations before/after | TASK-12 |
| RWB-E1-044 merges in between | TASK-01 re-checks; TASK-11 switches to "add class directory only"; TASK-02 keeps the migration package | TASK-01, -02, -11 |
| Modulith `verify()` on fixtures behaves differently from main code | Stop and report (SPEC-007) | TASK-09 |
| Existing ACE public types or E1-044 classes break the new rules once merged | `RecoveryBoundaryTest` on real main classes; report, do not loosen rules | TASK-10 |

## Out of scope

SPEC-016: `RecoveryAccessGuard` and its wiring, TC-TE-001-08, MSG-P4-002 (RWB-E1-022); pipeline stages (D-RCV-05); code owners (RWB-TE-002); OpenAPI types and contract tests (RWB-TE-003); common/collection internal boundaries (ACE team); adapter pattern (RWB-E1-007); agent client (RWB-TE-013). Context alignment of FS-1.2 (OPEN-022) is Context Updater work, not a task here.

## Status reporting

```text
PLANNER_STATUS_SUMMARY: Plan and 22 tasks written for RWB-TE-001 (backend skeleton, map, ArchUnit/Modulith rules, JaCoCo; frontend ESLint allow-list with Vitest proof); PO spec approval given (PRE-1); plan approval waits on the v2 re-approval by the FDA and FDE (PRE-3/PRE-4).
PLANNER_STATUS_DETAIL: SUCCESS [REASON: all SPEC-001..020 mapped; PRE-1 approved; PRE-2..PRE-4 pending, enforced by TASK-00] [UNBLOCK_ACTION: ACE tech lead settles OPEN-023; FDA approves plan and FDE approves tasks after a passing plan gate review]
PLANNER_CLARIFICATION_STATUS: READY [OPEN_ITEMS: 0] [UNBLOCK_ACTION: n/a]
PLANNER_DESIGN_SOURCE: NOT_REQUIRED [NOTE: n/a]
PLAN_REQUIREMENT_COVERAGE_SUMMARY: All 17 spec coverage rows and 6 business rules mapped to tasks and tests; no blocked row.
PLAN_REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 17] [TASK_COVERED_RULES: 17] [MISSING_TASK_RULES: 0] [AMBIGUOUS_TASK_RULES: 0] [CONTRADICTIONS: 0]
```

## Status reporting

```text
PLAN_STATUS: SUCCESS
TASKS: 22
SCOPE: one module + named shared files
BLOCKED_TASKS: 0
ASSUMPTIONS: 4
NEXT_STEP: Human plan approval, then start the Implementation Builder on TASK-21 and the re-verification tasks.
```
