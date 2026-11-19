---
title: "Tasks: RWB-TE-002 Code owners for the recovery module"
run_id: "INC-004-epic-1-RWB-TE-002"
story: "RWB-TE-002"
revision: "v1 (18 Nov 2026): first tasks file for this repository, written by the continuation of the interrupted plan run; source `plan.md` v2. TASK-00..TASK-11."
---

# Tasks: RWB-TE-002

Source: `plan.md` v2 and `../specify/spec.md` (remediation run 4, 577 lines). Design Source: `NOT_REQUIRED` (UI In Scope: NO; `DESIGN_EVIDENCE_STATUS: NOT_REQUIRED`). `C` = `backend/src/test/java/th/co/scb/ace/demo/recovery/architecture/codeowners`. Commands run from the worktree root; Gradle commands run in `backend/` with the `JAVA_TOOL_OPTIONS` of RUN-BRIEF. Every red and green run is saved under `implement/` as command, exit code and the first failing or final summary line.

## Backend Plan

Surface status: **CHANGED** (test scope and build only). Unit tests: **REQUIRED** (Trace: SPEC-001, -007..-009, -013..-017; BR1..BR7; AC1..AC4, AC7). Gate: `codeOwnersCoverageVerification` at 80% LINE, BRANCH, INSTRUCTION and METHOD over the four helper classes of package `th.co.scb.ace.demo.recovery.architecture.codeowners`, `*Test` classes excluded, execution data from `codeOwnersTest` (SPEC-014). Tasks TASK-00..TASK-11. No main-source class, endpoint, entity or migration.

## Frontend Plan

Surface status: **NOT_APPLICABLE** for implementation and unit tests. Evidence: spec Change Scope "Frontend Changes Required: NO" and "UI In Scope: NO" (`spec.md:25`, `:32`); no file under `frontend/` is added or changed; TASK-09 (1) proves it with `git diff --stat`. Existing `npm run check` (Vitest 80% thresholds in `frontend/vite.config.ts`) must still pass inside TASK-10. No frontend task waits on a backend contract: `NO_API_CHANGE`. `frontend/components.md` is not created (UI In Scope NO).

## Test-first order

1. TASK-00 pre-flight; it stops on a failed precondition.
2. Red: TASK-01 (compile-clean stubs and fixture tests), TASK-02 (live-file tests), TASK-03 (governance tests). Each red run is recorded.
3. Green: TASK-04 (parser, register reader, validator, resolver), then TASK-05 (`.gitlab/` files); TASK-06 (MR template and `AGENTS.md`); TASK-07 (Gradle and CI).
4. Verify: TASK-08 (suite and coverage evidence), TASK-09 (guardrails), TASK-10 (`./scripts/dev.ps1 test`), TASK-11 (handoff).

There is no compile-red task: TASK-01 writes compile-clean stubs, so every red run is an assertion failure and each later task can run single test classes. This applies the TE-001 lesson (PLAN-015) without weakening any test.

## Task table

| Task | Description | Files | Trace | BLOCKED_BY | Verification |
|---|---|---|---|---|---|
| TASK-00 | **Pre-flight, read only.** (1) Confirm `../specify/spec.md` header `Status` is `SUCCESS`; if it still reads `DRAFT`, stop and report SU-P01. (2) Confirm RWB-TE-001 is merged into `develop-recovery`: `backend/src/test/resources/architecture/recovery-modules.yaml`; `backend/src/test/resources/architecture/fixtures/` with at least one file; `backend/src/test/java/th/co/scb/ace/boundaryfixture/`; `backend/src/test/java/th/co/scb/ace/demo/recovery/architecture/boundary/`; and the 19 module packages. Record the merged fixture-root package path and use it for `{te001FixtureRoot}` (PA-01); if the merged path differs from `th/co/scb/ace/boundaryfixture`, use the merged path. If the fixtures sit inside an already owned folder, record that the substitution line is dropped (ASM-TE002-18). (3) Confirm `org.yaml:snakeyaml:2.6` on `testCompileClasspath` and `testRuntimeClasspath`. (4) List every regular file under `backend/src/test/resources/architecture/` and every top-level folder under `backend/src/test/resources/` and `backend/src/test/java/`; compare with the CODEOWNERS block. Stop and report if a file under `architecture/` or `test/java/` would be left unowned under UT-26 (B): R-2 (RWB-E1-042 `magic-number-baseline.csv`). Record, without stopping, the test-resource folders added by earlier stories outside the block: R-3 (RWB-E1-044 `migration-lint/`, `flyway-fixtures/`). (5) Record the `recoveryCoverage*` class include from `backend/build.gradle.kts`: `th/co/scb/ace/demo/recovery/architecture/boundary/**` only means "separate"; a wider `architecture/**` means "wider". Do not edit those tasks. (6) Save the baseline `cd backend; ./gradlew test` exit code and confirm `.gitlab/` is absent. | none (read only) | SPEC-002, -013, -014; P1, P2; PA-01, PA-04, PA-05, PA-06, PA-08 | NONE | `implement/preflight.md` holds (1)-(6) with the command and output; (1) and (2) must pass before any code; `{te001FixtureRoot}` and the coverage case are recorded; a failure stops the build and is reported, not worked around |
| TASK-01 | **Red: stubs and fixture tests.** Add `CodeOwnersFile`, `OwnerRegister`, `CodeOwnersValidator` and `OwnershipResolver` with the signatures and records of `data-model.md` §1.1, each method throwing `UnsupportedOperationException`. Add `CodeOwnersValidationTest` methods for UT-01..UT-11 and UT-23 and `OwnershipResolverTest.specificPatternWinsWithinASection` (UT-19), all `@Tag("codeowners")`. Fixtures go to `@TempDir`; no `.gitlab/` file is created. | `C/CodeOwnersFile.java`, `C/OwnerRegister.java`, `C/CodeOwnersValidator.java`, `C/OwnershipResolver.java`, `C/CodeOwnersValidationTest.java`, `C/OwnershipResolverTest.java` | SPEC-001, -007, -008, -009; UT-01..-11, -19, -23; BR5; AC7 local part | TASK-00 | `cd backend; ./gradlew test --tests "*CodeOwnersValidationTest" --tests "*OwnershipResolverTest"` compiles and fails per fixture case, not with a compile error; red saved to `implement/backend/red-task01.txt` |
| TASK-02 | **Red: live-file tests.** Add UT-12..UT-18, UT-20, UT-25 and UT-26 methods to the same two classes, reading the live `.gitlab/CODEOWNERS` and `.gitlab/codeowners-register.yaml` through `CodeOwnersValidator.repositoryRoot()` and scanning the working tree. They fail because `.gitlab/` does not exist and because `AGENTS.md` §5 still holds `.github/contexts/`. | `C/CodeOwnersValidationTest.java`, `C/OwnershipResolverTest.java` | SPEC-002..-005, -007, -009, -017; AC1..AC4; BR1..BR5, BR7; UT-12..-18, -20, -25, -26 | TASK-01 | same command; every live case fails because the `.gitlab/` files are absent or, before TASK-04, because a helper is still a stub; no compile error; red saved to `implement/backend/red-task02.txt` |
| TASK-03 | **Red: governance tests.** Add `MergeRequestTemplateTest` (UT-21), `AgentsContextPathsTest` (UT-22) and `PipelineDefinitionTest` (UT-24), all `@Tag("codeowners")`. UT-22 reads `AGENTS.md` §5 and fails on `.github/contexts/`; UT-21 fails on the missing template; UT-24 parses `.gitlab-ci.yml` with SnakeYAML and fails on the missing job. | `C/MergeRequestTemplateTest.java`, `C/AgentsContextPathsTest.java`, `C/PipelineDefinitionTest.java` | SPEC-013, -015, -016; A-05, A-10; flow 2; UT-21, -22, -24 | TASK-00 | `cd backend; ./gradlew test --tests "*MergeRequestTemplateTest" --tests "*AgentsContextPathsTest" --tests "*PipelineDefinitionTest"` fails on the missing template, job or AGENTS.md paths (or an unimplemented helper before TASK-04), not with a compile error; red saved to `implement/backend/red-task03.txt` |
| TASK-04 | **Green: parser, register reader, validator and resolver.** Implement `CodeOwnersFile.parse(Path)` and `parse(List<String>)`, `OwnerRegister.read(Path)`, `CodeOwnersValidator.validate(Path, Path, Path)`, `failed(...)` and `repositoryRoot()`, and `OwnershipResolver.resolve(...)` exactly as `data-model.md` §1: grammar, V1-V12, the placeholder and assumed notes, fail-closed register problems and last-match-per-section resolution. Messages exactly `data-model.md` §1.3. No main-source class. | `C/CodeOwnersFile.java`, `C/OwnerRegister.java`, `C/CodeOwnersValidator.java`, `C/OwnershipResolver.java` | SPEC-001, -007, -008, -009; BR5; AC7; UT-01..-11, -19, -23 | TASK-01 | fixture cases green and live cases still red for the missing `.gitlab/` files; `./gradlew test --tests "*CodeOwnersValidationTest" --tests "*OwnershipResolverTest"` output saved to `implement/backend/green-task04.txt`; every message compared with `data-model.md` §1.3 |
| TASK-05 | **Green: governance files.** Write `.gitlab/CODEOWNERS` exactly `data-model.md` §2 with only `{te001FixtureRoot}` substituted, `.gitlab/codeowners-register.yaml` exactly §3 and `.gitlab/host-settings.md` exactly §4 (HC-01..HC-08, status `OPEN — NOT_APPLIED_HERE`, no person). | `.gitlab/CODEOWNERS`, `.gitlab/codeowners-register.yaml`, `.gitlab/host-settings.md` | SPEC-001..-005, -009..-012, -017, -018; BR1..BR7; AC1..AC7 | TASK-02, TASK-04 | resolver cases UT-13..UT-18, UT-20, UT-25 and UT-26 green; UT-12 remains red only on V9 for `/.gitlab/merge_request_templates/`, which TASK-06 creates; the live warnings are the reserved common pattern and the two placeholders; `git diff --stat` lists only these three files |
| TASK-06 | **Green: MR template and AGENTS.md.** Write `.gitlab/merge_request_templates/Default.md` exactly `data-model.md` §5 with the eight headings in order; the `Reviewer` section names no person. Edit `AGENTS.md` §5 only: replace `.github/contexts/` with `aisdlc/.github/contexts/` in the five path cells and write the coding-standard cell as the two `aisdlc/.github/contexts/` files (SPEC-016). | `.gitlab/merge_request_templates/Default.md`, `AGENTS.md` | SPEC-015, -016; A-05, A-10; UT-21, UT-22 | TASK-03, TASK-05 | `cd backend; ./gradlew test --tests "*MergeRequestTemplateTest" --tests "*AgentsContextPathsTest"` green; `./gradlew test --tests "*CodeOwnersValidationTest"` UT-12 green; `git diff --unified=0 AGENTS.md` shows only the §5 cells |
| TASK-07 | **Green: Gradle tasks and CI job.** Append the `codeOwnersTest`, `codeOwnersCoverageReport` and `codeOwnersCoverageVerification` block and the `test` input declaration exactly `data-model.md` §6; add the `codeowners-validation` job exactly §7 after `frontend-check`. No dependency, no `check` wiring, no `scripts/dev.ps1` change. | `backend/build.gradle.kts`, `.gitlab-ci.yml` | SPEC-013, -014; flow 2; PA-03 | TASK-05, TASK-06 | `cd backend; ./gradlew codeOwnersTest` green; `./gradlew codeOwnersCoverageVerification` green at or above 0.80 on LINE, BRANCH, INSTRUCTION and METHOD; `./gradlew check --dry-run` lists no codeowners task; touching `.gitlab/CODEOWNERS` makes `./gradlew test` re-run, recorded as `> Task :test` without `UP-TO-DATE`; `./gradlew test --tests "*PipelineDefinitionTest"` green |
| TASK-08 | **Coverage and suite evidence.** Run `cd backend; ./gradlew codeOwnersTest codeOwnersCoverageVerification` once; save the command, exit code, duration, JaCoCo XML and HTML to `implement/backend/coverage/` and the `implementation-execution-gates.md` results table to `implement/unit-tests/report.md`. The backend row is `PASS` with measured LINE, BRANCH, INSTRUCTION and METHOD; the frontend row is `NOT_APPLICABLE` with the spec scope evidence and `N/A` metrics. No threshold change and no exclusion. | evidence only | SPEC-014; UT-01..UT-26; AC7; BR1..BR7 | TASK-07 | exit 0; `codeOwnersCoverageVerification` prints each counter at or above 0.80; the XML and HTML exist; the results table has one backend row and one frontend `NOT_APPLICABLE` row with native report paths |
| TASK-09 | **Security, privacy, guardrail and scope check.** (1) `git diff --stat develop-recovery...HEAD` lists only the files of `plan.md` and no file under `backend/src/main/`, `frontend/`, `scripts/`, `infra/`, `api/` or `backend/src/main/java/th/co/scb/ace/demo/common/`; the `.gitlab-ci.yml` diff adds only the `codeowners-validation` job, with no browser test runner. (2) Scan every added file, test and `.gitlab/` file for a real e-mail, personal name, phone, 13-digit number, `+66`, token or credential. The test-only synthetic values `@someone`, `someone@example.test` (UT-08 negative data) and `@scb-ace/recovery-leads-typo` (UT-07) are allowed and appear only in the test source, never in the live file or register. No personal name, real e-mail or credential anywhere. (3) Diff `./gradlew dependencies` before and after; no dependency added. (4) Confirm no endpoint, no Spring Security method check and no host token. (5) Confirm no RWB-TE-001 file is edited and no collection or common file is created. (6) Confirm HV-01..HV-11 are still `OPEN — NOT_TESTED_HERE` and not claimed. (7) Confirm no `@Disabled`, `@Ignore`, skip or weakened assertion. | `implement/scope-check.md` | SPEC-008 (V8), -018, -019; story §17; AGENTS.md §4 | TASK-08 | checklist all ticked with command output; no personal data, dependency, out-of-scope diff or claimed host check; a failure stops the build |
| TASK-10 | **Merge-gate regression.** From the worktree root run `powershell -NoProfile -File scripts/dev.ps1 test`; record `$LASTEXITCODE`. Run `cd backend; ./gradlew test` separately and keep the JUnit XML. Confirm the codeowners classes appear in `backend/build/test-results/test/` and `npm run check` passes its 80% thresholds. The pipeline job is not run here (HV-07). | evidence only | SPEC-013 (1), -018; flow 6; UT-01..UT-26 | TASK-08, TASK-09 | both exit 0; log `implement/dev-test.log`; the JUnit XML lists the UT-01..UT-26 methods; the frontend coverage summary is at or above 80 on lines, statements, branches and functions; no pipeline result claimed |
| TASK-11 | **Handoff.** Write `implement/handoff.md` with the local state `BUILT — ACCEPTANCE PENDING HV-01..HV-11`; all eleven HV items as `OPEN — NOT_TESTED_HERE` with their owner; what runs locally (UT-01..UT-26 in `./scripts/dev.ps1 test`) versus what is defined and host-run (`codeowners-validation`, coverage gate); the TASK-08 coverage table; the merge-record condition that the orchestrator writes the `--no-ff` merge commit and `README.md` with the exact sentence, and that the Builder writes neither; OPEN-024, OPEN-038, OPEN-041 and `PROP-OI-1`..`PROP-OI-4`; and no human approval or acceptance. | `implement/handoff.md` | SPEC-018, -019; story §13; §2 measure | TASK-10 | the handoff contains the exact local-state line, eleven open HV rows, the orchestrator merge-record instruction and the open items; a search finds no `Done`, `Accepted` or "§13 met" claim and no named person |

## Scope bullet to task map

| Scope bullet (`plan.md`) | Tasks |
|---|---|
| S-1 Pre-flight on the merged TE-001 base | TASK-00 |
| S-2 Validator, parser, register reader and resolver | TASK-01, TASK-04 |
| S-3 Code owners file | TASK-02, TASK-05 |
| S-4 Owner register | TASK-01, TASK-05 |
| S-5 Host configuration record | TASK-05, TASK-11 |
| S-6 MR template | TASK-03, TASK-06 |
| S-7 AGENTS.md §5 path fix | TASK-03, TASK-06 |
| S-8 Gradle tasks and CI job | TASK-03, TASK-07 |
| S-9 Unit tests UT-01..UT-26 and coverage evidence | TASK-01, TASK-02, TASK-03, TASK-08 |
| S-10 Security, privacy and guardrail checks | TASK-09 |
| S-11 Merge-gate regression run | TASK-10 |
| S-12 Handoff and local completion state | TASK-11 |

## Dependency graph

```text
TASK-00 ─┬─ TASK-03 ─────────────────────────────────┐
         └─ TASK-01 ─┬─ TASK-02 ─┐                   ├─ TASK-06 ─ TASK-07 ─ TASK-08 ─ TASK-09 ─ TASK-10 ─ TASK-11
                     └─ TASK-04 ─┴─ TASK-05 ─────────┘
```

No cycle. TASK-02 and TASK-04 may run in parallel after TASK-01; TASK-03 may run in parallel with TASK-01, TASK-02 and TASK-04. TASK-06 joins TASK-03 and TASK-05, and TASK-07 joins TASK-06. TASK-09 and TASK-10 are evidence tasks and change no code.

## One-module check (D-RUN-21)

`AGENTS.md` §7 and §9 require a plan that touches one module. Build decision D-RUN-21 (`AI-SDLC-BUILD-LOG.md` decisions table, 18 Nov 2026 05:36, the orchestrator (Claude Code)) reads "module" as the ACE module, recovery. This plan changes only the recovery module's test tree in `backend/src/test/java/th/co/scb/ace/demo/recovery/architecture/codeowners/` and repository governance files (`.gitlab/`, `AGENTS.md`, `backend/build.gradle.kts`, `.gitlab-ci.yml`). It creates no file under `th/co/scb/ace/demo/common/` or in the collection module: the `[Common module]` line names a reserved path only (SPEC-004). The plan passes the rule as D-RUN-21 reads it. The definition gap remains OPEN-050 for tech-lead ratification (`document-gaps.md` PG-TE002-02, Blocker = No).

## Pre-submit checks

- [x] Every scope bullet S-1..S-12 in `plan.md` maps to at least one `TASK-*` (table above).
- [x] Every in-scope SPEC-001..SPEC-019 maps to at least one task (`plan.md` "SPEC to task map"); no orphan `SPEC-*`.
- [x] Every AC1..AC7, BR1..BR7, X1..X7 and TC-TE-002-01..08 maps to a test ID or an open HV item (`tests/scenarios.md`); no unmapped acceptance clause.
- [x] Every task has Description, Files, Trace, `BLOCKED_BY` (explicit `NONE` for TASK-00) and Verification.
- [x] Effective-screen node groups: `NOT_APPLICABLE` (UI In Scope NO, `DESIGN_EVIDENCE_STATUS: NOT_REQUIRED`); no `SCR-*` screen and no Figma node in the spec; no consolidation task required.
- [x] Frontend and backend unit-test applicability recorded as `NOT_APPLICABLE` and `REQUIRED` respectively, with trace and reason, in `plan.md` and above.
- [x] Tests precede code: red TASK-01, TASK-02 and TASK-03 run before green TASK-04, TASK-05, TASK-06 and TASK-07; no test is written after the code it checks.
- [x] One-module check passes under D-RUN-21; no file is created in `common/` or `collection/`.
- [x] No migration (D-RUN-07 not exercised); no new dependency; shared files edited only by the Builder's own branch after this plan.
- [x] Later-story work is a named seam only (RWB-TE-003, RWB-TE-010, RWB-TE-011; D-RUN-08); no dependency on an unmerged story except RWB-TE-001, which precondition P1 sequences before this build.
- [x] No test is skipped, disabled or weakened; all 26 UTs are positive or negative cases with exact expected text.
- [x] Plan inputs name every file by exact path on `develop-recovery`, and the TE-001 outputs table names what P1 must supply (`plan.md` "Plan inputs" and "RWB-TE-001 outputs").
- [x] No human approval, acceptance or ratification is claimed; OPEN-024, OPEN-038, OPEN-041, OPEN-050 and `PROP-OI-1`..`PROP-OI-4` stay open; HV-01..HV-11 stay `OPEN — NOT_TESTED_HERE`.
- [x] Every task-table row has exactly six cells and no unescaped `|` inside a cell.
