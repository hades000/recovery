---
title: "Implementation Plan: RWB-TE-002 Code owners for the recovery module"
run_id: "INC-004-epic-1-RWB-TE-002"
story: "RWB-TE-002"
epic: "EPIC-001"
status: "SUCCESS"
revision: "v1 (18 Nov 2026): first plan for this repository. The v2 plan in `../_v2-baseline/plan/` named ACE monorepo and GitHub host work; it is history only and is not reused (D-RUN-05)."
prepared: "2026-11-18"
---

# Implementation Plan: RWB-TE-002 Code owners for the recovery module

Design Source: `NOT_REQUIRED` (UI In Scope: NO; `DESIGN_EVIDENCE_STATUS: NOT_REQUIRED` in spec.md).

| Field | Value |
|---|---|
| Spec | `../specify/spec.md` (remediation run 4, 577 lines). Spec gate round 5 `REVIEW-RWB-TE-002-SG-2026111805`: `PASS` 0/0/0/0 (`../review/spec-gate-review-5.md`). Rounds 1–4 read: `spec-gate-review.md` (0C/2H/6M/3L), `-2` (5L), `-3` (1L), `-4` (2L); all SG-001..SG-019 resolved. |
| Upstream story | RWB-TE-001, gated plan v7 (`../../INC-002-epic-1-RWB-TE-001/plan/plan.md`, plan gate round 7 `PASS` 0/0/0/0), being built on `feature/RWB-TE-001-module-boundary`. RWB-TE-002 is built and merged after it (precondition P1; Build Sequence v6 order 2 before order 4; D-RUN-01, D-RUN-06, D-RUN-17). |
| Code base | This repository as read on 18 Nov 2026 (`backend/`, `.gitlab-ci.yml`, `scripts/dev.ps1`, `AGENTS.md`, file listings). No code, git state or shared file changed by this stage. |
| Builder | Implementation Builder (medium effort, D-RUN-16) in its own worktree on `feature/RWB-TE-002-code-owners` from `develop-recovery` **after RWB-TE-001 is merged**; commits `RWB-TE-002: <summary>` with trailers `AISDLC-Run: INC-004-epic-1-RWB-TE-002` and `AISDLC-Plan: aisdlc/output/INC-004-epic-1-RWB-TE-002/plan/plan.md` (CLAUDE.md). Evidence goes to `aisdlc/output/INC-004-epic-1-RWB-TE-002/implement/`. |
| Smallest change | Four governance files under `.gitlab/`; one test-scope package (4 helper classes, 5 test classes); one block appended to `backend/build.gradle.kts`; one job added to `.gitlab-ci.yml`; one table fixed in `AGENTS.md`. No main-source class, endpoint, migration, dependency, frontend file or script change. |
| One-module check | Touches only the recovery module of ACE plus repository governance files (D-RUN-21). No file is created or changed under `common/` or `collection/`; the `[Common module]` line names a path and creates nothing (SPEC-004). Passes AGENTS.md §7/§9 as D-RUN-21 reads it. |

## Upstream readiness

| Check | Result |
|---|---|
| Spec gate | `PASS` round 5, no open finding, no new document gap (`spec-gate-review-5.md` §6). |
| Spec status | Header still reads `DRAFT — awaiting spec gate re-review` (`spec.md:13`); build log row 2026-11-18T00:59:53 records "Spec left as gated (header DRAFT); the gate review is the record of the pass". For planning, the gate PASS 0/0/0/0 plus the coverage result below is the equivalent ready state (`planning-execution-gates.md` "or equivalent ready state"; PA-04). `implementation-execution-gates.md` line 67 still needs `Status: SUCCESS` in `spec.md` before build: proposal SU-P01 for the orchestrator; TASK-00 (1) stops the build without it. |
| `REQUIREMENT_COVERAGE_RESULT` | `SUCCESS [TOTAL_RULES: 38] [COVERED_RULES: 38] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]` (`spec.md:570`). |
| Clarification log | CLAR-001..CLAR-011 all `RESOLVED`; `CLARIFICATION_STATUS: RESOLVED [CLAR_OPEN: 0]` (`spec.md:572`). CLAR-001 is resolved for this repository; its ACE part is OPEN-038, an open item and not a `CLAR` item. |
| Design evidence | `NOT_REQUIRED`: no screen tasks, no `frontend/components.md`, no screen-coverage consolidation task. |
| Migration | None. D-RUN-07 not exercised (UT-15 uses a synthetic name never written to disk). |
| Dependencies | Only RWB-TE-001 outputs (table "RWB-TE-001 outputs this plan depends on"). D-RUN-08 holds. |

`PLANNER_CLARIFICATION_STATUS: READY [OPEN_ITEMS: 0] [UNBLOCK_ACTION: n/a]`. The spec's open items (OPEN-024, OPEN-038, OPEN-041, proposed PROP-OI-1..3) are shared open-item rows, not `CLAR-*` items; none blocks the local build (spec "Local completion state").

## RWB-TE-001 outputs this plan depends on

Read from TE-001 plan v7 (`plan.md` "Files added or changed (backend)", "Coverage gate edit"; `assumptions.md` PA-01, PA-02). TASK-00 confirms each on the merged code.

| TE-001 output (plan v7) | Used here for | If the merged code differs |
|---|---|---|
| Module map `backend/src/test/resources/architecture/recovery-modules.yaml` (TE-001 TASK-02) | `[Recovery module]` line; V9; UT-15, UT-26 (A) | Same path is fixed by D-RCV-37 and TE-001 spec v4 SPEC-002; a different path is a TE-001 defect: stop (TASK-00). |
| Fixture maps `backend/src/test/resources/architecture/fixtures/<world>.yaml` (TASK-05) | `[Recovery module]` line `/backend/src/test/resources/architecture/fixtures/`; UT-26 (B) | Folder empty or absent: stop (V9 would fail). |
| Backend fixture root `F` = `backend/src/test/java/th/co/scb/ace/boundaryfixture` (TE-001 PA-01, TASK-05) | Substitution `{te001FixtureRoot}` = `th/co/scb/ace/boundaryfixture` (PA-01) | Use the merged path and record it (spec CLAR-011); if the fixtures sit inside an already owned folder, drop the line (ASM-TE002-18). UT-26 holds either way. |
| Tooling package `th.co.scb.ace.demo.recovery.architecture.boundary` (TE-001 PA-02) | The codeowners package `…architecture.codeowners` is a different package (spec "Components") | Same package name would be a conflict: stop. |
| `recoveryCoverageReport` / `recoveryCoverageVerification` class dirs = recovery main classes + test output `th/co/scb/ace/demo/recovery/architecture/boundary/**` only (TE-001 TASK-01) | Case recorded as the spec asks (`spec.md` "Components"): **separate** — codeowners classes are not counted in `recoveryCoverage*`; they are measured only by `codeOwnersCoverage*`. This story does not edit those two tasks. | If the merged include is wider (`architecture/**`), codeowners classes are also counted there; record it in `implement/backend/preflight.txt`; still no edit to those tasks. |
| `RecoveryBoundaryTest` and `ModulithTest` import main classes only (`DO_NOT_INCLUDE_TESTS`; `ModulithTest` unchanged) | Test-scope codeowners classes are never scanned as module code (ASM-TE002-13) | If a test import is found, stop and report. |
| 19 module packages and the relocated classes (TE-001 TASK-11) | Covered by the two directory patterns of the recovery main and test packages; UT-14 inputs | No CODEOWNERS change needed for any TE-001 package name. |
| `backend/build.gradle.kts` edited by TE-001 (JaCoCo tasks only) | TE-002 appends a new block after the existing tasks; nothing above it changes | Rebase on the merged file; no conflict expected (append only). |

## Scope

In scope (each bullet maps to tasks in `tasks.md`, "Scope bullet to task map"):

1. **S-1 Pre-flight on the merged TE-001 base** (precondition P1, P2, spec status). → TASK-00
2. **S-2 Validator, parser, register reader and resolver** in test scope, rules V1–V12 (SPEC-007, -008, -009). → TASK-01, TASK-04
3. **S-3 Code owners file** `.gitlab/CODEOWNERS`, exact spec block with the one substitution (SPEC-001..-005, -017). → TASK-02, TASK-05
4. **S-4 Owner register** `.gitlab/codeowners-register.yaml`, exact spec block (SPEC-009). → TASK-01, TASK-05
5. **S-5 Host configuration record** `.gitlab/host-settings.md`, HC-01..HC-08 with HV links (SPEC-006, -010, -011, -012, -018). → TASK-05, TASK-11
6. **S-6 MR template** `.gitlab/merge_request_templates/Default.md` (SPEC-015, A-10). → TASK-03, TASK-06
7. **S-7 AGENTS.md §5 path fix** (SPEC-016, A-05). → TASK-03, TASK-06
8. **S-8 Gradle tasks and CI job** `codeOwnersTest`, `codeOwnersCoverageReport`, `codeOwnersCoverageVerification`, `codeowners-validation` (SPEC-013, -014). → TASK-03, TASK-07
9. **S-9 Unit tests UT-01..UT-26, coverage evidence ≥ 80%** (SPEC-014). → TASK-01, -02, -03, TASK-08
10. **S-10 Security, privacy and guardrail checks** (story §17; SPEC-008 V8; AGENTS.md §4). → TASK-09
11. **S-11 Merge-gate regression run** `./scripts/dev.ps1 test`. → TASK-10
12. **S-12 Handoff: human-verification items and local completion state** (SPEC-018, -019). → TASK-11

Out of scope (SPEC-019, unchanged): TE-001 boundary test; collection code owners; TE-010 browser runner; common test folder; package-level AGENTS.md and separate coding standard (PROP-OI-3); host owner-existence check (HC-08/HV-07); running `codeowners-validation` in a pipeline (HV-07); creating `main`/`develop` or test MRs; the orchestrator's merge record (spec §5: merge commit message and `README.md`, written by the orchestrator at merge, never by the Builder).

### Paths the spec gate asked the planner to decide

Spec gate reviews 1–3 "Plan inputs" asked for a decision on files the spec block does not name. The spec block is exact ("nothing else in the block changes", `spec.md:259`), so none is added; each decision is recorded:

| Path | Decision | Basis |
|---|---|---|
| `backend/src/test/java/th/co/scb/ace/demo/ModulithTest.java`, `…/demo/e2e/`, `api/recovery-api-v4.yaml`, `frontend/src/api/schema.d.ts` | Owned in `[Recovery module]` (already in the spec block) | ASM-TE002-08, -18 |
| `backend/src/main/resources/application.yaml`, `application-local.yaml` | Unowned in this story | ACE service settings file shared by every module, not a recovery folder; same class as `AceRecoveryApplication.java` in the spec's unowned row (`spec.md:537`); a later reviewed MR may add it (BR7). PA-06 |
| `frontend/src/i18n/index.ts` | Unowned in this story | Shell i18n bootstrap shared by all frontend modules (the recovery namespace files live in `frontend/src/modules/recovery/i18n/`, which is owned); same class as `frontend/src/{components/ui,lib,contexts}` (`spec.md:537`). PA-06 |
| `infra/postgres/init/` | Unowned in this story | Spec out-of-scope row `infra/` (`spec.md:537`). PA-06 |
| Test resources added by earlier stories outside the block (RWB-E1-044 `backend/src/test/resources/migration-lint/`, `flyway-fixtures/`; RWB-E1-042 `backend/src/test/resources/architecture/magic-number-baseline.csv`) | Not added by this plan; handled by TASK-00 (4)/(5) and SU-P04 | PA-05 |

## Plan-time verification (read only)

| Item | Method | Result |
|---|---|---|
| SnakeYAML on test classpaths (P2) | TE-001 plan v7 "Plan-time verification": `./gradlew --offline -q dependencies --configuration testCompileClasspath` | `org.yaml:snakeyaml:2.6` present through the Spring Boot starters (an `implementation` dependency, so also on `testRuntimeClasspath`). TASK-00 (3) re-runs both configurations. No dependency added. |
| Existing test task wiring | `backend/build.gradle.kts` lines 100–108 | `test` excludes only `recovery-it` and `e2e`, so tag `codeowners` runs in `gradlew test`, hence in `./scripts/dev.ps1 test` (`scripts/dev.ps1` lines 114–116). JaCoCo applies its agent to every `Test` task, so `codeOwnersTest` produces execution data. |
| Test working directory | Existing `RecoveryMigrationLintTest` (`Path.of("src/main/resources/…")`) | Gradle runs tests in `backend/`; repository root = parent (spec SPEC-013). |
| Paths in the block | Directory listing 18 Nov 2026 | Exist today: every pattern except `…/demo/common/` (reserved), `architecture/recovery-modules.yaml`, `architecture/fixtures/`, `…/boundaryfixture/` (all TE-001) and the new `.gitlab/` files. `backend/gradle/wrapper/` holds two files; `frontend/e2e/platform.spec.ts`; `db/modulemigration/recovery/README.md`; `.claude/agents/`; all six `aisdlc/.github/contexts/` targets of SPEC-016. |
| Line endings | `.gitattributes` (`* text=auto`) | `CODEOWNERS` has no extension and may be checked out with CRLF on Windows. The parser reads with `Files.readAllLines` (accepts `\n` and `\r\n`); no `.gitattributes` change. |
| CI file shape | `.gitlab-ci.yml` | Stages `verify`, `integration`; jobs use flow-style maps; SnakeYAML `SafeConstructor` parses it (UT-24). |
| Up-to-date checking | Gradle task inputs | `test` and `codeOwnersTest` read files outside the source set (`.gitlab/`, `AGENTS.md`, `.gitlab-ci.yml`), so an edit to them alone would leave `test` UP-TO-DATE locally. TASK-07 declares them as task inputs (PA-03). |

## Backend Plan

Surface status: **CHANGED** (test scope and build only). Unit tests **REQUIRED**: 80% LINE, BRANCH, INSTRUCTION (statements), METHOD (functions), bundle over test-output classes `th/co/scb/ace/demo/recovery/architecture/codeowners/**` excluding `**/*Test.class` and `**/*Test$*.class`, by `codeOwnersCoverageVerification` with execution data from `codeOwnersTest` (SPEC-014).

`C` = `backend/src/test/java/th/co/scb/ace/demo/recovery/architecture/codeowners`.

### Files added or changed

| Kind | Path | Task | SPEC |
|---|---|---|---|
| Add | `C/CodeOwnersFile.java` (parser; records `Section`, `Entry`; syntax and orphan-entry lines) | TASK-01 (stub), TASK-04 | 001, 007, 008 |
| Add | `C/OwnerRegister.java` (SnakeYAML reader; records `Owner`, `ReservedPattern`; problems) | TASK-01 (stub), TASK-04 | 009 |
| Add | `C/CodeOwnersValidator.java` (V1–V12; record `Finding`, enum `Level`; `repositoryRoot()`) | TASK-01 (stub), TASK-04 | 008 |
| Add | `C/OwnershipResolver.java` | TASK-01 (stub), TASK-04 | 007 |
| Add | `C/CodeOwnersValidationTest.java` (UT-01..UT-12, UT-23) | TASK-01, TASK-02 | 001, 004, 005, 008, 009, 017 |
| Add | `C/OwnershipResolverTest.java` (UT-13..UT-20, UT-25, UT-26) | TASK-01, TASK-02 | 002..005, 007, 017 |
| Add | `C/MergeRequestTemplateTest.java` (UT-21) | TASK-03 | 015 |
| Add | `C/AgentsContextPathsTest.java` (UT-22) | TASK-03 | 016 |
| Add | `C/PipelineDefinitionTest.java` (UT-24) | TASK-03 | 013 |
| Add | `.gitlab/CODEOWNERS` | TASK-05 | 001..005, 017 |
| Add | `.gitlab/codeowners-register.yaml` | TASK-05 | 009 |
| Add | `.gitlab/host-settings.md` | TASK-05 | 006, 010, 011, 012, 018 |
| Add | `.gitlab/merge_request_templates/Default.md` | TASK-06 | 015 |
| Edit | `AGENTS.md` (§5 table path cells only) | TASK-06 | 016 |
| Edit | `backend/build.gradle.kts` (block appended after `recoveryCoverageVerification`) | TASK-07 | 013, 014 |
| Edit | `.gitlab-ci.yml` (job `codeowners-validation` added after `frontend-check`) | TASK-07 | 013 |
| Evidence (not code) | `aisdlc/output/INC-004-epic-1-RWB-TE-002/implement/…` | TASK-00, -08..-11 | 014, 018 |

Not changed: any file under `backend/src/main/`, `frontend/`, `scripts/`, `infra/`, `api/`; `recoveryCoverageReport`, `recoveryCoverageVerification`, the existing `test` block, `recoveryIntegrationTest`, `e2eTest`; `dependencies { }`; `backend-unit`, `frontend-check`, `backend-recovery-it`; `.gitattributes`; `README.md`; `CLAUDE.md`; every RWB-TE-001 file. No file under `backend/src/main/java/th/co/scb/ace/demo/common/`.

### Design (test scope)

Full types, grammar, message texts and file contents are in `data-model.md`. In short:

- **Parser** `CodeOwnersFile.parse(Path)` / `parse(List<String>)`: per line (1-based), blank or `#` → skip; `^\[([^\[\]]+)\]$` (after stripping trailing whitespace) → section header, name kept as written; otherwise split on whitespace: first token = pattern, rest = owners; an entry before any header is an orphan (V2); a line starting with `[` that is not a valid header (for example `^[A]`, `[A][2]`, `[A] @x`) or with `^` is a syntax error (V1). Missing file → X9.
- **Register** `OwnerRegister.read(Path)`: SnakeYAML `new Yaml(new SafeConstructor(new LoaderOptions()))`; missing file, YAML error, missing `owners`, a missing or blank field among the five, `status` outside {`ASSUMED`, `PLACEHOLDER`, `CONFIRMED`}, duplicate handle, and a `reservedPatterns` entry without `pattern` or `basis` → problem text (V11, fail closed).
- **Validator** `CodeOwnersValidator.validate(Path repoRoot, Path codeOwners, Path register)`: runs V1–V12 and the placeholder/assumed notes; collects every finding; `failed(findings)` = any `ERROR`. Messages exactly as the spec table "Validation rules".
- **Resolver** `OwnershipResolver.resolve(CodeOwnersFile, Collection<String> changedPaths)` → `LinkedHashMap<String section, Set<String> owners>` in file order: for each path and each section, the last matching entry's owners are added (union across paths, PA-07). Directory pattern (`/…/`): path starts with the pattern minus its leading `/`; file pattern: equal. No match → no section. Pure, deterministic.
- **Repository root**: `Path.of("").toAbsolutePath().getParent()`, checked by the presence of `.gitlab-ci.yml` (PA-10). Every repository-relative path is built with `/` separators, so Windows `\` never reaches a comparison (PA-13).

### Code owners file content

Exactly the spec block (`spec.md:262-318`) with one substitution: line 276 `{te001FixtureRoot}` → `th/co/scb/ace/boundaryfixture`, giving

`/backend/src/test/java/th/co/scb/ace/boundaryfixture/ @scb-ace/techx-recovery-tech-leads`

Evidence: TE-001 plan v7 `plan.md` "Files added or changed (backend)" (`F = backend/src/test/java/th/co/scb/ace/boundaryfixture`) and `assumptions.md` PA-01. TASK-00 (2) checks the merged tree; the full resulting file is in `data-model.md` §2. Nothing else in the block changes.

### Gradle and CI (defined here, run on the host)

As SPEC-013 and SPEC-014; exact text in `data-model.md` §6 and §7. `codeOwnersTest` and the two codeowners JaCoCo tasks are not wired into `check` (as `recoveryCoverageVerification`, D-RCV-28 (3), D-RCV-40). The only touch on the existing `test` task is an extra `tasks.named<Test>("test") { inputs.files(...) }` block declaring the live governance files as inputs, so that `./scripts/dev.ps1 test` re-runs the codeowners tests when only those files change (PA-03). The CI job is checked as a definition by UT-24; it is never reported as run here (HV-07).

## Frontend Plan

Surface status: **NOT_APPLICABLE** for implementation and unit tests. Evidence: spec Change Scope "Frontend Changes Required: NO" and "UI In Scope: NO" (`spec.md:25`, `:32`); no file under `frontend/` is added or changed (verified by TASK-09 (5) `git diff --stat` on `frontend/`). The code owners file only names frontend paths. Unchanged dependency: `npm run check` (Vitest 80% thresholds in `frontend/vite.config.ts`) must still pass inside `./scripts/dev.ps1 test` (TASK-10). No frontend task waits on a backend contract: there is no contract change. `frontend/components.md`: not created (UI In Scope NO).

## Unit test applicability

| Surface | Changes Required | Unit Tests | Coverage Gate | Trace | Evidence and reason |
|---|---|---|---|---|---|
| Backend | YES (test scope + build) | REQUIRED | 80% LINE, BRANCH, INSTRUCTION, METHOD on the codeowners package (`codeOwnersCoverageVerification`) | BR1–BR7, AC1–AC4, AC7, X2, X3, X6; SPEC-001..005, -007..009, -013..017 | New hand-written logic in the backend test tree (spec "Unit Test Applicability"). Tests TASK-01..03, verification TASK-08. Final results table: TASK-08 (`implementation-execution-gates.md`). |
| Frontend | NO | NOT_APPLICABLE | NOT_APPLICABLE (metrics `N/A`) | — | No frontend file changes (spec `:217`). Regression only: `npm run check` in TASK-10. |

## Execution order (tests before code, AGENTS.md rules 3 and 10)

1. TASK-00 pre-flight (stops on a failed precondition).
2. Red: TASK-01 (compile stubs with no logic + fixture tests), TASK-02 (live-file tests), TASK-03 (governance tests). Each red run is recorded. Stubs let the test source set compile, so every later task can run single test classes (lesson from TE-001 PLAN-015).
3. Green: TASK-04 (logic) → TASK-05 (`.gitlab/` files) ; TASK-06 (template, AGENTS.md) ; TASK-07 (Gradle, CI).
4. Verify: TASK-08 (codeowners suite + coverage evidence), TASK-09 (guardrails), TASK-10 (`./scripts/dev.ps1 test`), TASK-11 (handoff).

## Functional Test Scenarios

| Scenario | Assigned to | Status |
|---|---|---|
| API scenarios | API Tester | `NOT_APPLICABLE`: `NO_API_CHANGE`, no endpoint (`contracts/backend-apis.json`; story §14, §16). |
| UI / user-workflow scenarios | Functional Automation Test | `NOT_APPLICABLE`: no screen, route or component (story §15). |
| Host behaviour: AC1 clause 2, AC3 blocked, AC5, AC6, AC7 host part, X1, X4, X5, X7, flows 3, 4, 7, story §2 measure, §13 "Done when", pipeline run of `codeowners-validation` | Human verification on the ACE host (owner: ACE team repository administrator with the recovery tech lead) | HV-01..HV-11, each `OPEN — NOT_TESTED_HERE` (spec SPEC-018; PROP-OI-2). Not executed tests and never reported as passed by any stage. |

Repository-level automated checks are the unit tests UT-01..UT-26 (`tests/scenarios.md`), run by `gradlew test` inside `./scripts/dev.ps1 test`.

## Requirement Logic To Task Coverage

`REQ_REF` values are the 38 rows of the spec table "Requirement-to-SPEC Logic Coverage". All rows are `DIRECT_IMPLEMENTATION`. "HV" = human verification on the ACE host, open, not tested here.

| REQ_REF | Mapped SPEC-* | Mapped TASK-* | Coverage Type | Verification | Status |
|---|---|---|---|---|---|
| BR1 | SPEC-002 | TASK-00, -02, -05 | DIRECT_IMPLEMENTATION | UT-13, UT-14, UT-26 | COVERED |
| BR2 | SPEC-003 | TASK-02, -05 | DIRECT_IMPLEMENTATION | UT-15, UT-26 | COVERED |
| BR3 | SPEC-004 | TASK-01, -02, -04, -05 | DIRECT_IMPLEMENTATION | UT-10, UT-16 | COVERED |
| BR4 | SPEC-005 | TASK-01, -02, -04, -05 | DIRECT_IMPLEMENTATION | UT-18, UT-23; HV-08 | COVERED |
| BR5 | SPEC-001, -007, -008 | TASK-01, -04 | DIRECT_IMPLEMENTATION | UT-06, UT-19 | COVERED |
| BR6 | SPEC-006, -010, -011, -012 | TASK-05, -11 | DIRECT_IMPLEMENTATION | HC-01..HC-05 in `host-settings.md` (review in TASK-05); HV-01, HV-03, HV-04, HV-05 | COVERED |
| BR7 | SPEC-005, -009 | TASK-02, -05 | DIRECT_IMPLEMENTATION | UT-18, UT-23 | COVERED |
| AC1 (clause 1) | SPEC-002, -007 | TASK-02, -04, -05 | DIRECT_IMPLEMENTATION | UT-13 | COVERED |
| AC1 (clause 2) | SPEC-006, -018 | TASK-05, -11 | DIRECT_IMPLEMENTATION | HV-01 | COVERED |
| AC2 | SPEC-004, -007 | TASK-02, -04, -05 | DIRECT_IMPLEMENTATION | UT-16; HV-02 | COVERED |
| AC3 (required) | SPEC-007 | TASK-02, -04, -05 | DIRECT_IMPLEMENTATION | UT-17 | COVERED |
| AC3 (blocked) | SPEC-006, -018 | TASK-05, -11 | DIRECT_IMPLEMENTATION | HV-03 | COVERED |
| AC4 | SPEC-003, -007 | TASK-02, -04, -05 | DIRECT_IMPLEMENTATION | UT-15 | COVERED |
| AC5 | SPEC-010, -018 | TASK-05, -11 | DIRECT_IMPLEMENTATION | HC-04; HV-04 | COVERED |
| AC6 | SPEC-011, -018 | TASK-05, -11 | DIRECT_IMPLEMENTATION | HC-05; HV-05 | COVERED |
| AC7 | SPEC-008, -009, -013 | TASK-01, -04, -05, -11 | DIRECT_IMPLEMENTATION | UT-07; HC-08; HV-07 | COVERED |
| X1 | SPEC-006, -018 | TASK-05, -11 | DIRECT_IMPLEMENTATION | HV-01 | COVERED |
| X2 | SPEC-004, -007 | TASK-02, -04, -05 | DIRECT_IMPLEMENTATION | UT-16 | COVERED |
| X3 | SPEC-007, -018 | TASK-02, -04, -05, -11 | DIRECT_IMPLEMENTATION | UT-17; HV-03 | COVERED |
| X4 | SPEC-010, -018 | TASK-05, -11 | DIRECT_IMPLEMENTATION | HV-04 | COVERED |
| X5 | SPEC-011, -018 | TASK-05, -11 | DIRECT_IMPLEMENTATION | HV-05 | COVERED |
| X6 | SPEC-008, -013 | TASK-01, -04, -11 | DIRECT_IMPLEMENTATION | UT-07 (exact text `line {n}: owner @scb-ace/recovery-leads-typo not found`); HV-07 | COVERED |
| X7 / TC-TE-002-08 | SPEC-018 | TASK-11 | DIRECT_IMPLEMENTATION | HV-06 (follows story §16, SP-DG-06) | COVERED |
| Flow 1 | SPEC-001..005, -017 | TASK-02, -05 | DIRECT_IMPLEMENTATION | UT-12, UT-25 | COVERED |
| Flow 2 | SPEC-013, -014 | TASK-03, -07, -08 | DIRECT_IMPLEMENTATION | UT-24 (definition); TASK-08 evidence run; HV-07 (pipeline run) | COVERED |
| Flow 3 | SPEC-006, -010, -011, -012 | TASK-05, -11 | DIRECT_IMPLEMENTATION | HC-01..HC-06; HV-01..HV-05 | COVERED |
| Flow 4 | SPEC-018 | TASK-11 | DIRECT_IMPLEMENTATION | HV-02 | COVERED |
| Flow 5 | SPEC-007, -018 | TASK-02, -04, -05, -11 | DIRECT_IMPLEMENTATION | UT-13..UT-18; HV-02 | COVERED |
| Flow 6 | SPEC-008, -013 | TASK-01, -04, -11 | DIRECT_IMPLEMENTATION | UT-07, UT-09; HV-07 | COVERED |
| Flow 7 | SPEC-006, -018 | TASK-05, -11 | DIRECT_IMPLEMENTATION | HV-03 | COVERED |
| §12 Contract | SPEC-001..013 | TASK-02, -04, -05, -07 | DIRECT_IMPLEMENTATION | UT-12, UT-20 (idempotency), UT-24; rows above | COVERED |
| §14 Messages | SPEC-008, -018 | TASK-01, -04, -11 | DIRECT_IMPLEMENTATION | UT-07 (build text exact); HV-01 (host text) | COVERED |
| §2 Measure | SPEC-018 | TASK-11 | DIRECT_IMPLEMENTATION | HV-10 | COVERED |
| §13 Done when | SPEC-018 | TASK-11 | DIRECT_IMPLEMENTATION | HV-01..HV-11; local end state `BUILT — ACCEPTANCE PENDING HV-01..HV-11`, never Done | COVERED |
| §17 Guardrails | SPEC-001, -002, -003, -008, -009 | TASK-01, -02, -04, -05, -09 | DIRECT_IMPLEMENTATION | UT-08, UT-26; TASK-09 scan | COVERED |
| §19 Out of scope | SPEC-019 | TASK-09, -11 | DIRECT_IMPLEMENTATION | TASK-09 (5)–(7) diff checks: no collection/common file, no TE-001 file, no pipeline browser runner | COVERED |
| A-05 | SPEC-016, -017, -019 | TASK-03, -05, -06 | DIRECT_IMPLEMENTATION | UT-22; `[Repository standards]` owns `/AGENTS.md` (UT-12 V9) | COVERED |
| A-10 | SPEC-001, -015 | TASK-03, -05, -06 | DIRECT_IMPLEMENTATION | UT-21; HV-09 | COVERED |

38 of 38 rows mapped; none `BLOCKED`.

## SPEC to task map

| SPEC | Tasks | Tests / verification |
|---|---|---|
| SPEC-RWB-TE-002-001 | TASK-01, -02, -04, -05 | UT-01..UT-06, UT-12 |
| SPEC-RWB-TE-002-002 | TASK-00, -02, -05 | UT-13, UT-14, UT-26 |
| SPEC-RWB-TE-002-003 | TASK-02, -05 | UT-15, UT-26 |
| SPEC-RWB-TE-002-004 | TASK-01, -02, -04, -05 | UT-10, UT-16 |
| SPEC-RWB-TE-002-005 | TASK-01, -02, -04, -05 | UT-18, UT-23; HV-08 |
| SPEC-RWB-TE-002-006 | TASK-05, -11 | HV-01, HV-03, HV-07 |
| SPEC-RWB-TE-002-007 | TASK-01, -02, -04 | UT-13..UT-20 |
| SPEC-RWB-TE-002-008 | TASK-01, -02, -04 | UT-01..UT-12, UT-23 |
| SPEC-RWB-TE-002-009 | TASK-01, -04, -05 | UT-07, UT-11 |
| SPEC-RWB-TE-002-010 | TASK-05, -11 | HV-04 |
| SPEC-RWB-TE-002-011 | TASK-05, -11 | HV-05 |
| SPEC-RWB-TE-002-012 | TASK-05, -11 | HV-01..HV-05 |
| SPEC-RWB-TE-002-013 | TASK-03, -07, -08, -10 | UT-01..UT-26 in `dev.ps1 test`; UT-24; HV-07 |
| SPEC-RWB-TE-002-014 | TASK-01..03, -07, -08 | Coverage evidence ≥ 80% × 4 (TASK-08); HV-07 |
| SPEC-RWB-TE-002-015 | TASK-03, -06 | UT-21; HV-09 |
| SPEC-RWB-TE-002-016 | TASK-03, -06 | UT-22 |
| SPEC-RWB-TE-002-017 | TASK-02, -05, -09 | UT-11, UT-12, UT-25; HV-11 |
| SPEC-RWB-TE-002-018 | TASK-05, -11 | HV-01..HV-11 (open) |
| SPEC-RWB-TE-002-019 | TASK-09, -11 | TASK-09 diff checks |

No orphan SPEC; no task without a SPEC (`tasks.md` "Pre-submit checks").

## Screen-to-task mapping

`NOT_APPLICABLE`: UI In Scope NO; no Figma node and no `SCR-*` screen in the spec. No consolidation task for screen coverage is needed.

## Rule tables and migrations read

- Rule data read by this story: `.gitlab/CODEOWNERS` and `.gitlab/codeowners-register.yaml` (versioned files it creates). No database rule table, threshold, timer or route (AGENTS.md §3.2 not exercised).
- Migration scripts: none. Reference data: none.

## Security, privacy and compliance

- No person, e-mail, membership, token or credential in any file, test, fixture or log (story §17; AGENTS.md §4.1, §4.7). Owners are group handles only (V8). Synthetic test handle: `@scb-ace/recovery-leads-typo` (story AC7). Synthetic paths only; UT-15 and UT-16 never write the file they name.
- No endpoint, so no Spring Security method check (AGENTS.md §3.3 not exercised); authority is a repository right (story §10), documented in `host-settings.md` and verified on the host (HV items).
- No host API or token is used. The host owner-existence check stays HC-08/HV-07 and must fail closed when built in ACE (ASM-TE002-06).
- Placeholder and assumed handles (OPEN-038) are allowed at the local merge only under the spec's merge-record condition, which the orchestrator carries out (spec §5). TASK-11 hands this to the orchestrator; the Builder writes neither carrier.
- Audit: findings name line, pattern and owner; JUnit XML is the build-log record. No financial action, KYC, AML or consent scope.
- Checks: TASK-09.

## Release and rollback

No feature flag (story §13: a file and a test have no runtime path). Rollback is a revert MR of the four `.gitlab/` files, the `AGENTS.md` table and the build and CI blocks, approved per SPEC-005 and SPEC-017; host settings are reverted by the administrator from `host-settings.md`. The orchestrator merges into `develop-recovery` only after `./scripts/dev.ps1 test` exits 0 on the branch (TASK-10) and the code gate passes, with `git merge --no-ff --no-commit`, then adds `README.md`, then commits (spec §5; spec gate review 5 observation 1; build log 2026-11-18T00:59:53). Local end state: `BUILT — ACCEPTANCE PENDING HV-01..HV-11`.

## Risks

| ID | Risk | Control |
|---|---|---|
| R-1 | RWB-TE-001's merged fixture root or map path differs from its plan v7. | TASK-00 (2) uses the merged path (CLAR-011) and records it; V9 and UT-26 fail on a wrong line. |
| R-2 | RWB-E1-042 (build order 3) merges before RWB-TE-002 and adds `backend/src/test/resources/architecture/magic-number-baseline.csv`, which no line of the spec block owns, so UT-26 (B) would fail. | TASK-00 (4) stops before any code and reports; no unsanctioned line is added and UT-26 is not weakened. SU-P04 (a) asks the orchestrator to merge TE-002 first or route a one-line spec amendment; if TE-002 merges first, E1-042's own MR adds the line (UT-26 forces it on rebase). |
| R-3 | RWB-E1-044 (wave A, merged before TE-002 under D-RUN-17) adds recovery test-resource folders `migration-lint/` and `flyway-fixtures/` under `backend/src/test/resources/` that the spec block does not own. No test fails, but BR1 ("test folders") would leave them unowned. | TASK-00 (5) records them; SU-P04 (b) proposes open item `PROP-OI-4` (follow-up line by a reviewed MR per BR7, or a TE-002 spec amendment before host use). Not a stop: the spec block is exact (`spec.md:259`). |
| R-4 | Later stories add files under the UT-26 scope (RWB-TE-003 `backend/src/test/java/th/co/scb/ace/tooling/recoveryapi/`) or new root folders (RWB-TE-011 `/tools/pdpa-lint/`). | Their MR adds the line; UT-26 and V9 make the omission visible. SU-P04 (c). |
| R-5 | Gradle reports `test` UP-TO-DATE after an edit to `.gitlab/` only. | Inputs declared (PA-03); TASK-07 verification proves the re-run. |

## Assumptions

`assumptions.md` PA-01..PA-14. Document gaps: `document-gaps.md` (no new gap; SP-DG-01..10 carried, none a blocker).

## Status

```text
PLANNER_STATUS_SUMMARY: Plan for RWB-TE-002 in this repository: 12 tasks (TASK-00..TASK-11), tests first, four .gitlab files, one test-scope package, Gradle and CI definitions, AGENTS.md fix; host behaviour stays as 11 open human-verification items.
PLANNER_STATUS_DETAIL: SUCCESS [REASON: spec gate PASS 0/0/0/0, all CLAR resolved, 38/38 rules mapped] [UNBLOCK_ACTION: n/a for planning; build needs RWB-TE-001 merged and spec Status SUCCESS (SU-P01)]
PLANNER_CLARIFICATION_STATUS: READY [OPEN_ITEMS: 0] [UNBLOCK_ACTION: n/a]
PLANNER_DESIGN_SOURCE: NOT_REQUIRED [NOTE: n/a]
PLAN_REQUIREMENT_COVERAGE_SUMMARY: All 38 spec coverage rows map to tasks; 26 unit tests cover the locally testable rules; host-only rows map to host-settings.md and HV-01..HV-11.
PLAN_REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 38] [TASK_COVERED_RULES: 38] [MISSING_TASK_RULES: 0] [AMBIGUOUS_TASK_RULES: 0] [CONTRADICTIONS: 0]
FRONTEND_UNIT_TESTS: NOT_APPLICABLE [REASON: no frontend file changes]
BACKEND_UNIT_TESTS: REQUIRED [GATE: 80% LINE/BRANCH/INSTRUCTION/METHOD on recovery.architecture.codeowners via codeOwnersCoverageVerification]
TE001_SUBSTITUTION: {te001FixtureRoot} = th/co/scb/ace/boundaryfixture (TE-001 plan v7 F, PA-01; confirmed on merged code at TASK-00)
LOCAL_COMPLETION_STATE: BUILT — ACCEPTANCE PENDING HV-01..HV-11 (never Done until HV-01..HV-11 pass on the ACE host)
NEXT_STEP: Plan gate (review/plan-gate-review.md). Build only after RWB-TE-001 merges into develop-recovery and spec.md shows Status SUCCESS.
```
