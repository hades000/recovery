# Plan gate review: RWB-TE-001 (run INC-002-epic-1-RWB-TE-001), round 1

| Field | Value |
|---|---|
| Stage | Compliance Reviewer, plan gate (`planning-execution-gates.md`) |
| Story | RWB-TE-001 Recovery module folder and boundary test |
| Reviewed | `plan/plan.md`, `plan/tasks.md`, `plan/data-model.md`, `plan/contracts/backend-apis.json`, `plan/contracts/frontend-integrations.json`, `plan/tests/scenarios.md`, `plan/assumptions.md`, `plan/document-gaps.md`, `plan/shared-updates.md`, `plan/agent-run-log.md` |
| Checked against | Approved spec v4 (`specify/spec.md`, gate round 5 PASS) and its companion files; plan inputs of `review/spec-gate-review-3.md` (1–6) and `review/spec-gate-review-2.md` (1–5, 7); `AGENTS.md` v2 (baseline document set v14); `CLAUDE.md`; the code at `backend/`, `frontend/`, `scripts/dev.ps1`, `.gitlab-ci.yml` |
| Reviewer | Compliance Reviewer agent (subagent of the orchestrator, Claude Code). Read only; this file is the only file written. |

## 1. Gate structure

| Check | Result | Evidence |
|---|---|---|
| `## Pre-submit checks` present | Yes | `tasks.md` §"Pre-submit checks" |
| Every task has Trace, `BLOCKED_BY` and Verification | Yes in content, but the TASK-13 row is malformed (PLAN-001) | `tasks.md` task table, 19 rows TASK-00..TASK-18 |
| Scope bullet → task map | Complete, S-1..S-15 | `tasks.md` §"Scope bullet to task map"; `plan.md` §Scope |
| SPEC → task map; no orphan SPEC | Complete; SPEC-021 shown withdrawn; every other SPEC-001..-026 has a task and a test | `plan.md` §"SPEC to task map"; `tests/scenarios.md` |
| AC1–AC7 and BR1–BR6 → task and named test | Complete | `plan.md` §"Requirement Logic To Task Coverage"; `tests/scenarios.md` §1, §2 |
| Status block present | Yes, `PLAN_REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 13] …` | `plan.md` §Status |
| Dependency graph acyclic; first tasks `BLOCKED_BY NONE` | Yes (TASK-00, TASK-15) | `tasks.md` §"Dependency graph" |
| D-RUN-07: no migration number fixed | Yes; the story adds no migration | grep of `plan/` for `V0nnn` finds none |
| D-RUN-08: depends only on the repository and earlier stories | Yes; later stories appear only as SU-P02 / SU-P03 notices | `shared-updates.md` |

## 2. Plan inputs carried

| Input | Disposition in plan | Result |
|---|---|---|
| R3-1 filter `isUnnamed()` | T-TE001-14 / PA-05 bounded set over `!isUnnamed()` | Carried |
| R3-2 `powershell -NoProfile -File`, record `$LASTEXITCODE` | TASK-17 | Carried |
| R3-3 coverage verification shown separately | TASK-13 (3) | Carried |
| R3-4 fixture `@NamedInterface(propagate = false)` | `data-model.md` fixture worlds | Carried; `propagate` exists in Modulith 2.1.1 (verified with javap) |
| R3-5 `PdpaPayloadCodec` bean and class in one package | Relocation table | Carried |
| R3-6 | `plan.md` "Carried plan inputs" table | Carried |
| R2-1 node environment and timeout for the ESLint test | Frontend Plan | Carried |
| R2-2 filter on `ruleId`; R2-3 guard `results[0]` | Frontend test design | Carried (`noUncheckedIndexedAccess` is on in `tsconfig.json`) |
| R2-4 one registration per property record | Property split | Carried |
| R2-5 nested fixture tree; R2-7 one-module reading | `data-model.md`; `plan.md` | Carried |

## 3. Code claims verified by the reviewer

| Claim | Result | Evidence |
|---|---|---|
| Relocation table covers every file of the four baseline packages | Yes: 35 files (27 types, 8 `package-info.java`) | `backend/src/main/java/th/co/scb/ace/demo/recovery/{platform,rules,workflow,documents}` |
| No non-Java file names an old package | Yes | `grep -rlE "…recovery\.(platform\|rules\|workflow\|documents)\b" backend/src` lists only `.java` files |
| Visibility after the move (public where crossed, package-private kept) | Correct: `PdpaPayloadCodec` public final; `TemporalProperties` package-private and used only by `TemporalAdminController` in the same package; `PlatformSmokeWorkflow` public; `TimerDueJob` public static | source files |
| Cross-module edges after the move | `casewf.rules` → `integration.flags.api`; `casewf.admin` → `access.api` (ApiError, ApiProblemException); no cycle | `DroolsRuleEngine`, `TemporalAdminController`, `PlatformInfoController` imports |
| BND-5 passes on real code | Yes: only `BlobDocumentStore` uses `com.azure.storage` / `com.azure.identity`; `InetAddress` (TemporalConfig) and `URI` (ProblemFactory) match no entry | sources; SPEC-009 name-boundary match |
| Property records and defaults | Match `backend/src/main/resources/application.yaml` | `data-model.md` §5 |
| `ApplicationModules.of(String, ImportOption)` passes only the given option | Yes | javap, spring-modulith-core 2.1.1 |
| ArchUnit `FailureReport` sorts but does not deduplicate | Yes | javap, archunit 1.5.1 `EvaluationResult.getFailureReport` |
| JaCoCo baseline | INSTRUCTION 686/2174, BRANCH 25/92, LINE 133/415, METHOD 41/135 | `backend/build/reports/jacoco/recoveryCoverageReport.xml` |
| ESLint allow-list cases in the frontend test | Every rejected and allowed import is classified correctly by the D-RCV-39 regex | `frontend/eslint.config.js` |
| Merge-gate script | `dev.ps1 test` runs `gradlew test` then `npm run check`; throws on non-zero | `scripts/dev.ps1` lines 67–74 and the `test` command |
| CI IT trigger still matches the moved `RecoveryFlywayConfig` | Yes (`backend/src/main/java/**/RecoveryFlywayConfig.java`) | `.gitlab-ci.yml` |

## 4. Findings

### REVIEW-RWB-TE-001-PLAN-001 — Low — TASK-13 table row is malformed

- **Affects:** `tasks.md` §"Task table", row TASK-13.
- **Evidence:** The description holds the code span `` `grep -rnE "th\.co\.scb\.ace\.demo\.recovery\.(platform|rules|workflow|documents)\b" backend/src` `` with three unescaped `|`. In a GitHub-flavoured Markdown table a `|` inside a code span still ends the cell. The row has 11 cells against 8 for every other row, so its Files, Trace, `BLOCKED_BY` and Verification values do not sit in their columns. A reader or tool reading the `BLOCKED_BY` column gets `documents)\b" backend/src` …` instead of `TASK-01, TASK-08, TASK-12`. This breaks the gate rule "BLOCKED_BY on every task" for the row.
- **Fix:** Escape the three pipes in that code span as `\|` (rendered as `|`), or move the command out of the table into a note under it and reference the note. Check that each row has exactly six cells.

### REVIEW-RWB-TE-001-PLAN-002 — Low — TASK-01 check-wiring verification fails on unchanged wiring

- **Affects:** `tasks.md` TASK-01 Verification ("`./gradlew check` does not run either task (task graph `--dry-run`)").
- **Evidence:** `backend/build.gradle.kts` lines 105–108: `tasks.named<Test>("test") { … finalizedBy("recoveryCoverageReport") }`. `check` depends on `test`, and Gradle puts finalizer tasks in the task graph, so `./gradlew check --dry-run` lists `:recoveryCoverageReport` today. The check as worded fails even though TASK-01 leaves the wiring unchanged, as SPEC-020 (d) asks.
- **Fix:** Reword the TASK-01 check: `./gradlew check --dry-run` does not list `:recoveryCoverageVerification`; `:recoveryCoverageReport` appears only as the existing finalizer of `test`; the `check` task list is the same as a baseline dry-run taken in TASK-00.

### REVIEW-RWB-TE-001-PLAN-003 — Low — T-TE001-13 Run 1 evidence is not in the console log

- **Affects:** `tasks.md` TASK-17 Verification; `tests/scenarios.md` T-TE001-13 (spec v4 T-TE001-13: "the Gradle log has `Rule BND-5 broken: …`").
- **Evidence:** `backend/build.gradle.kts` has no `testLogging` block, so Gradle's default console output for a failed test is the test name and `java.lang.AssertionError at RecoveryBoundaryTest.java:<line>` (short exception format, no message). `dev.ps1` calls `./gradlew.bat test` with no extra flags (`scripts/dev.ps1` lines 67–74). The `Rule BND-5 broken: …` line is therefore in the JUnit XML and HTML reports, not in the console log TASK-17 tells the Builder to read.
- **Fix:** In TASK-17 and T-TE001-13 (plan), name the evidence source: `backend/build/test-results/test/TEST-th.co.scb.ace.demo.recovery.architecture.RecoveryBoundaryTest.xml` (or `build/reports/tests/test/`), and quote the line from there into `implement/merge-gate.md` together with the console exit code. Do not add `testLogging` to `build.gradle.kts` (TASK-01 limits the build edit to the two JaCoCo tasks).

### REVIEW-RWB-TE-001-PLAN-004 — Low — "BND-5 is stricter" is not true

- **Affects:** `plan.md` §"`RecoveryBoundaryTest` changes" line 185 ("stricter … `com.azure.storage` allowed only in `dochub.storage`"); `tasks.md` §"Pre-submit checks" line 91 ("replaced by the stricter BND-5").
- **Evidence:** The baseline test `blobClientOnlyInDocumentsModule` allows `com.azure.storage..` only in `recovery.documents.internal..` (`RecoveryBoundaryTest.java`). Approved spec v4 SPEC-009 allows every listed library in any `clientPackages` package of the using class's own module: `integration.adapter`, `dochub.storage` and `agent.client`. So BND-5 adds 15 libraries but widens where `com.azure.storage` is allowed from one package to three. The replacement is approved (SPEC-009, SPEC-026, finding 022, D-RCV-41). The pre-submit check "No test is skipped or weakened" rests on the wrong reason.
- **Fix:** Reword both places: BND-5 replaces the baseline test as SPEC-009 / SPEC-026 require (finding 022, D-RCV-41). It covers 16 libraries instead of one. Blob use is allowed in the three map client packages, not only in `dochub.storage`. The only user today is `BlobDocumentStore` in `dochub.storage`. Base the "not weakened" check on that spec authority, not on "stricter".

### REVIEW-RWB-TE-001-PLAN-005 — Low — Retargeted determinism rule has no guard against an empty selection

- **Affects:** `plan.md` §"`RecoveryBoundaryTest` changes"; TASK-11 (retarget to `.casewf.workflow..`).
- **Evidence:** `workflowImplementationsAreDeterministic` keeps `.allowEmptyShould(true)` (`RecoveryBoundaryTest.java`). A mistyped package after the retarget would select no class and pass. Approved spec v4 SPEC-026 states that `PlatformSmokeWorkflow.Impl` "stays under the rule". No task or test in the plan shows that.
- **Fix:** Add to TASK-11 a verification and a test assertion: the classes selected by `resideInAPackage(RECOVERY + ".casewf.workflow..")` with `haveSimpleNameEndingWith("Impl")` include `th.co.scb.ace.demo.recovery.casewf.workflow.internal.PlatformSmokeWorkflow$Impl`. Make no other change to the rule; `allowEmptyShould(true)` stays.

### REVIEW-RWB-TE-001-PLAN-006 — Low — "One line per violation" is not defined, so exact line counts are not fixed

- **Affects:** `data-model.md` §4 (line 60, "One line per violation"); `tests/scenarios.md` (AC4 "three BND-4 lines", `bnd1` two lines, `mapbad` eight lines).
- **Evidence:** ArchUnit gives one `Dependency` per access: field type, constructor or method parameter, method call, and so on. A fixture class with an `HttpClient` field that it also calls yields several dependencies on the same target. `EvaluationResult.getFailureReport` sorts the messages and does not deduplicate them (archunit 1.5.1, verified with javap). Unless the custom `ArchCondition` deduplicates, the line counts depend on how each fixture is written.
- **Fix:** In `data-model.md` §4, define a violation as one distinct (origin class, target class) pair per rule. A nested origin class counts as its own class name, with `$`. The condition emits each pair once. Make the tests assert the exact counts in `scenarios.md` under that definition.

### REVIEW-RWB-TE-001-PLAN-007 — Low — BND-5 `{module}` depends on map order and can point at the wrong module

- **Affects:** `data-model.md` §4 line 65; `assumptions.md` PA-04; `document-gaps.md` PG-02.
- **Evidence:** Approved spec v4 SPEC-010 gives `{module}` for BND-5 as "the allowed client package". The plan sets it to "the module that owns the first `clientPackages` entry in the map". The gap is recorded (PG-02, routed by SU-P04), and the `.api` reason is sound. But the chosen value depends on the order of entries in `recovery-modules.yaml`: reordering the modules changes every BND-5 text, and the tests assert the full text. The value is also not derived from anything the rule means.
- **Fix:** Define `{module}` for BND-5 from a stable map property, not a list position. For example, use the module with code P2 (`integration`), on the authority of `AGENTS.md` v2 §4 rule 3 ("Outbound data leaves through the integration adapters"). Add a `bnd5` fixture case in which the client-package module is not listed first, so the test proves the text does not depend on order. Update PA-04 and PG-02 to match.

## 5. Observations (not defects)

- **Coverage credibility (SPEC-020).** BRANCH is the tight counter: 25/92 at baseline. The plan's coverage tests target the large gaps: `SecurityConfig` 16 branches, `BlobDocumentStore` 14 + `Config` 4, `TemporalAdminController` 10, `RecoveryFlywayConfig` 4, `ProblemFactory` 4. The boundary tooling, added to the bundle by `boundaryToolingClasses`, will be well covered by its own tests. The estimated result is about 79–84%. The fallback rule ("add a test at that class's home") covers the residual gaps not listed by name: `RuleInput` (3/6), `PdpaPayloadCodec` (11/14), `RuleResult`. With `JwtDecoder` mocked, the `SecurityConfig` audience-validator lambda stays uncovered. Credible, not certain.
- **X7 coverage type.** `MOVED_OUT_OF_SCOPE` is neither gate value (`DIRECT_IMPLEMENTATION` / `INHERITED_EXISTING_BEHAVIOR`). The plan says so openly (line 300), and TASK-18 checks the exclusion (D-RCV-52 moved X7 to RWB-E1-022). This matches the approved spec and is not counted as a missing rule.
- **Test-first.** The plan has red runs in TASK-01, -03, -06, -09 and -10 before the code they cover (AGENTS.md §3 rule 10, §1 rule 3). The SPEC-024 coverage tests are characterization tests over moved code, written after the move (PA-07). That is justified for existing behaviour.
- **Smallest change.** The plan reuses `RecoveryBoundaryTest` and `ModulithTest`, and keeps `noRecoveryClassNamesAPublicTable` unchanged. The four existing tests move with their assertions kept. The `DroolsRuleEngineTest` workbook FQCN strings (lines 97–98) are updated, not removed.
- **Frontend test.** If ESLint is created in `beforeAll`, the `describe`-level timeout does not cover the hook (`hookTimeout`). The Builder should set both. `src/test/setup.ts` imports `@/i18n` under the node environment. This is harmless, but the Builder should confirm it on the first run.
- **Clock.** `TemporalAdminController` builds its date from the system clock. A coverage test that asserts a date can fail around midnight; it should assert format, not value.
- **61 `package-info.java` files** (19 × 3 + 4) and the relocation, visibility and property split were verified against the code (§3).
- **HV-01** (GitLab blocks a failing merge request) stays a human item. The plan never reports it as tested (TASK-17, `scenarios.md` §6).
- **Personal data and attribution.** No personal data was found. Triage is attributed to the orchestrator (Claude Code). No plan text says a human approved, accepted or disposed of anything. D-RCV decisions are cited as source decisions.

## 6. Result

```text
PLAN_GATE: FAIL [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 7]
PLAN_GATE_FINDINGS: REVIEW-RWB-TE-001-PLAN-001..007 (all Low)
PLAN_REQUIREMENT_COVERAGE_RESULT (reviewer check): CONFIRMED [TOTAL_RULES: 13] [TASK_COVERED_RULES: 13] [MISSING_TASK_RULES: 0]
REVIEW_GATE_WARNING: Low-severity review failure does not automatically stop this handoff; unresolved findings may carry downstream. Human disposition required.
```

Overall status: **FAIL** (Low only). Counts: Critical 0, High 0, Medium 0, Low 7.
