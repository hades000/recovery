# Plan gate review: RWB-TE-001 (run INC-002-epic-1-RWB-TE-001), round 2

| Field | Value |
|---|---|
| Stage | Compliance Reviewer, plan gate (`planning-execution-gates.md`), round 2 |
| Story | RWB-TE-001 Recovery module folder and boundary test |
| Reviewed | `plan/plan.md` (v2), `plan/tasks.md` (v2), `plan/data-model.md` (v2), `plan/contracts/backend-apis.json`, `plan/contracts/frontend-integrations.json`, `plan/tests/scenarios.md` (v2), `plan/assumptions.md`, `plan/document-gaps.md`, `plan/shared-updates.md`, `plan/agent-run-log.md`; diffed against `plan/*.run1.md` and `plan/tests/scenarios.run1.md` (CR line endings ignored) |
| Checked against | Approved spec v4 (`specify/spec.md`, spec gate round 5 PASS) and `specify/contracts/backend-apis.json`; plan inputs of `review/spec-gate-review-3.md` (1–6) and `review/spec-gate-review-2.md` (1–5, 7); round-1 review `review/plan-gate-review.md`; `AGENTS.md` v2; the code at `backend/` (`build.gradle.kts`, `RecoveryBoundaryTest.java`, `PlatformSmokeWorkflow.java`, the four baseline packages), `scripts/dev.ps1`, `.gitlab-ci.yml` |
| Reviewer | Compliance Reviewer agent (subagent of the Implementation Planner, started by the orchestrator, Claude Code). Read only; this file is the only file written. |

## 1. Round-1 findings

| Finding | Result | Evidence |
|---|---|---|
| PLAN-001 TASK-13 row malformed | **RESOLVED** | The search command moved to note N-1 under the task table (`tasks.md`), referenced from TASK-13 step 2 and `scenarios.md` T-TE001-06. The pipe in the `plan.md` "Plan-time verification" row was also removed. The reviewer counted unescaped `|` per row in every table of all ten plan files with a script. Every row matches its header; there are no mismatches. |
| PLAN-002 TASK-01 `check` wiring verification | **RESOLVED** (with a small residual gap, PLAN-010) | TASK-01 Verification now says `check --dry-run` does not list `:recoveryCoverageVerification`. It lists `:recoveryCoverageReport` only as the finalizer of `test`, and it equals the baseline dry-run that TASK-00 step (4) saves. This matches `backend/build.gradle.kts` (`tasks.named<Test>("test") { … finalizedBy("recoveryCoverageReport") }`; `recoveryCoverageVerification` is registered but not wired to `check`). |
| PLAN-003 T-TE001-13 Run 1 evidence source | **RESOLVED** | TASK-17 and `scenarios.md` T-TE001-13 now quote the line from `backend/build/test-results/test/TEST-th.co.scb.ace.demo.recovery.architecture.RecoveryBoundaryTest.xml`, and `build.gradle.kts` gets no `testLogging` edit. The path matches Gradle's default for the `test` task and the class FQCN (`RecoveryBoundaryTest.java` package `th.co.scb.ace.demo.recovery.architecture`). `build.gradle.kts` has no `testLogging`. `dev.ps1 test` runs `Invoke-Gradle @("test")` and then `Invoke-Npm @("run","check")`, and throws on a non-zero exit (lines 67–74, 114–117). |
| PLAN-004 "stricter BND-5" | **RESOLVED** | `plan.md` "`RecoveryBoundaryTest` changes" and the `tasks.md` pre-submit check now base the replacement on SPEC-009 / SPEC-026 (finding 022, D-RCV-41). They say BND-5 covers 16 libraries and allows them in the own module's client packages `integration.adapter`, `dochub.storage`, `agent.client`. This matches spec SPEC-009 and the spec contract (`"allowedIn": "own module's clientPackages and sub-packages"`). No "stricter" claim remains (grep). |
| PLAN-005 determinism rule empty-selection guard | **RESOLVED in substance**, placement defect (PLAN-008) | New test `determinismRuleSelectsTheSmokeWorkflowImpl` (`plan.md` line 186, TASK-11 step 5, T-TE001-05). The target `th.co.scb.ace.demo.recovery.casewf.workflow.internal.PlatformSmokeWorkflow$Impl` is correct: `PlatformSmokeWorkflow` declares nested `class Impl` (line 32), and the Relocation table moves it to `casewf/workflow/internal`. The rule keeps `allowEmptyShould(true)`, as in the code today. |
| PLAN-006 violation unit | **RESOLVED** | `data-model.md` §4 and `plan.md` "Tooling design" now define a violation as one distinct (origin class, target class) pair per BND rule, and one (check, package or class) pair for MAP. A nested origin counts as its own class. The exact counts are consistent across files: AC1 `bnd1` two, AC4 `bnd4` exactly three, AC5 `bnd5` exactly four, `mapbad` exactly eight. The BND-4 exclusion of the Spring Data types themselves keeps `RecoveryCaseRepository extends Repository` from counting as a violation. That is consistent with the spec contract ("subtype of `org.springframework.data.repository.Repository`"). |
| PLAN-007 BND-5 `{module}` depends on map order | **RESOLVED** (new gap in the fallback, PLAN-009) | `{module}` is now the map module with code `P2`, which is order-independent. Fixture `bnd5` lists P10, P3, then P2, and AC5 asserts `Use integration.api …` on all four lines. PA-04 and PG-02 are updated. SU-P04 still routes PG-01..PG-03 and needs no change. |

Round-1 observations also taken up: the smoke-ID test asserts the format, not the date (`plan.md` line 211). The `beforeAll` hook timeout and the `setup.ts` check are named (`plan.md` line 236).

## 2. Gate structure (re-check)

| Check | Result | Evidence |
|---|---|---|
| Status block, `## Pre-submit checks` | Present; pre-submit check added for row cell counts | `plan.md` §Status; `tasks.md` §"Pre-submit checks" |
| Trace, `BLOCKED_BY`, Verification on every task | Yes, 19 rows TASK-00..TASK-18, six cells each | `tasks.md` task table (script check) |
| Scope bullet → task; SPEC → task → test | Complete: S-1..S-15; SPEC-001..-026 (021 withdrawn) | `tasks.md`; `plan.md` §"SPEC to task map"; `scenarios.md` §5 |
| AC1–AC7, BR1–BR6 → task and named test; counts | Complete; `TOTAL_RULES: 13`, `TASK_COVERED_RULES: 13` consistent in `plan.md`, `tasks.md`, spec | `plan.md` §"Requirement Logic To Task Coverage"; `scenarios.md` §1–§2 |
| Dependency graph | Unchanged, acyclic; TASK-00 and TASK-15 `NONE` | `tasks.md` |
| D-RUN-07 | No migration, no number | `data-model.md` intro |
| D-RUN-08 | Later-story work only as seams (SPEC-016 list, SU-P02/-P03) | `plan.md` §Scope; `shared-updates.md` |
| Tests not skipped or weakened | Held; moved tests keep assertions; Blob literal rule replaced on spec authority | `plan.md` lines 177, 185 |
| Personal data | None. Fixtures, maps and texts hold class and package names only. §5 defaults are local placeholders (`rwb_migrator`, localhost URLs, empty password). | `data-model.md` §3–§5 |
| Attribution | No text says a human approved, accepted or disposed of anything. "Accepted deviation D-RCV-39 / -42" cites source decisions. "Approved spec" refers to the spec gate PASS. HV-01 stays open for a human and is never reported as tested. Triage is attributed to the orchestrator (Claude Code). | grep of `plan/` for approv/accept/dispos/human |

## 3. Findings

### REVIEW-RWB-TE-001-PLAN-008 — Low — The new determinism guard is written in the code task, not in the red task, and the files disagree on where it lives

- **Affects:** `tasks.md` TASK-09 and TASK-11 (step 5, Files, Trace, Verification); `plan.md` §"Files added or changed (backend)" row `T/architecture/RecoveryBoundaryTest.java`; `tests/scenarios.md` T-TE001-05; SPEC-026; AGENTS.md §1 rule 3, §3 rule 10.
- **Evidence:**
  - `determinismRuleSelectsTheSmokeWorkflowImpl` is added in TASK-11 step 5, the green relocation task.
  - T-TE001-05 lists the guard among the tests that are "red before (TASK-09 evidence)". But TASK-09's description and Verification do not include it.
  - The `plan.md` files table gives `RecoveryBoundaryTest.java` to TASK-09 only.
  - TASK-11's Trace (`SPEC-001, -022, -023, -025; ASM-…`) does not name SPEC-026 or T-TE001-05, although the guard proves a SPEC-026 statement.
  - At baseline no class exists under `th.co.scb.ace.demo.recovery.casewf.workflow..` (the code has only `platform`, `rules`, `workflow`, `documents`). Written in TASK-09, the guard would therefore be a genuine red test. Written in TASK-11, it is written after the code it checks. This contradicts the plan's own pre-submit claim "Tests precede code: red runs in TASK-01, -03, -06, -09, -10 before TASK-04, -07, -11".
- **Fix:**
  - Move the guard from TASK-11 step 5 into TASK-09. Add it to TASK-09's description and Verification as red at baseline: "no class `…casewf.workflow.internal.PlatformSmokeWorkflow$Impl` selected".
  - Remove step 5 and the `T/architecture/RecoveryBoundaryTest.java (guard)` file entry from TASK-11, and add "`determinismRuleSelectsTheSmokeWorkflowImpl` green" to the TASK-11 Verification.
  - Leave T-TE001-05 as it is; it then becomes true.

### REVIEW-RWB-TE-001-PLAN-009 — Low — BND-5 `{module}` fallback ("map with no P2") is specified but has no test, and an origin outside every module is undefined

- **Affects:** `data-model.md` §4 BND-5 row; `assumptions.md` PA-04; `tests/scenarios.md` (no case); TASK-06 / TASK-07; SPEC-010; AGENTS.md §3 rule 10.
- **Evidence:**
  - The PLAN-007 fix added a second behaviour: "a map with no `P2` module prints the origin class's own module name".
  - Every fixture map that lacks P2 (`bnd1`, `bnd2`, `vendorx`, `mapbad`) has no client-library use, so BND-5 reports nothing there and the fallback branch never runs. No named test asserts the fallback text.
  - The tooling package is inside the SPEC-020 coverage bundle (`boundaryToolingClasses`), so the branch is also untested changed code. AGENTS.md §3 rule 10 says "A change with no test is not complete".
  - The fallback has no value for an origin class that is under `rootPackage` but in no map module. One example is a class in the root package, which MAP (c) reports separately while BND-5 still evaluates it.
- **Fix:**
  - In `data-model.md` §4, complete the fallback: no P2 module gives the origin's own module name, and an origin in no module gives the origin's package, the same convention as BND-4 for a target outside every module. Update PA-04 to match.
  - Add a named test to `scenarios.md` and TASK-06, for example `BoundaryRulesTest.bnd5TextWithoutP2UsesTheOriginModule`. It evaluates BND-5 over the `bnd5` classes with a fixture map that has no P2 (for example `fixtures/bnd5-nop2.yaml`, listed in TASK-05 and `data-model.md` §3). It asserts the exact line for `SampleService` (`… Use casewf.api or an application event.`).
  - The alternative is to drop the fallback and fail BND-5 with an explicit error when the map has no P2. That also needs a named test.

### REVIEW-RWB-TE-001-PLAN-010 — Low — TASK-00 step (4) produces the baseline that TASK-01 compares against, but no evidence location or verification is given for it

- **Affects:** `tasks.md` TASK-00 (description step 4, Verification) and TASK-01 Verification.
- **Evidence:** The PLAN-002 fix added TASK-00 step (4) "Save `./gradlew check --dry-run` as the baseline task list for TASK-01". TASK-01's Verification depends on "the baseline dry-run saved in TASK-00". The TASK-00 Verification column names only the dependency listing, `implement/backend/preflight.txt` (file listing) and the baseline counters. It gives no file and no check for the dry-run, so the TASK-01 comparison has no fixed input, and the code gate cannot find the evidence.
- **Fix:** Add to the TASK-00 Verification: "`./gradlew check --dry-run` output saved to `implement/backend/check-dryrun-baseline.txt`". In TASK-01 Verification, name the same file and the after-edit output file (for example `implement/backend/check-dryrun-after.txt`), compared by a diff whose result is recorded.

### REVIEW-RWB-TE-001-PLAN-011 — Low — `tasks.md` still names `plan.md` v1 as its source

- **Affects:** `tasks.md` line 10 ("Source: `plan.md` v1 and `../specify/spec.md` v4").
- **Evidence:** `plan.md` is now revision v2 (front matter line 7), and v1 is kept as `plan.run1.md`. `tasks.md` itself is v2 and depends on v2-only content in `plan.md`: the violation unit, the BND-4 Spring Data exclusion, the new guard and the reworded BND-5 replacement. A Builder that follows the stated source could take `plan.run1.md`, which lacks these.
- **Fix:** Change line 10 to "Source: `plan.md` v2 and `../specify/spec.md` v4". Check the other cross-file version references in `data-model.md`, `scenarios.md` and the contracts (`"revision": "v1"` in both contract files is correct, because they did not change in round 2).

## 4. Code claims verified by the reviewer (round 2)

| Claim | Result | Evidence |
|---|---|---|
| Determinism rule keeps `allowEmptyShould(true)` and selects `…workflow..` + `Impl` | Yes | `RecoveryBoundaryTest.java` `workflowImplementationsAreDeterministic` |
| `PlatformSmokeWorkflow` has nested `Impl` | Yes | `PlatformSmokeWorkflow.java` line 32 (`class Impl implements PlatformSmokeWorkflow` inside a public interface, so implicitly public static) |
| No `casewf` package exists at baseline (guard is red there) | Yes | `backend/src/main/java/th/co/scb/ace/demo/recovery/` holds `documents`, `platform`, `rules`, `workflow`, `package-info.java` |
| `check` does not run `recoveryCoverageVerification`; `recoveryCoverageReport` is a finalizer of `test` | Yes | `build.gradle.kts` (test task block; verification task registered with LINE and BRANCH limits only, not wired) |
| No `testLogging` in the build | Yes | grep of `build.gradle.kts` |
| `dev.ps1 test` = `gradlew test` then `npm run check`, throws on failure | Yes | `scripts/dev.ps1` lines 67–74, 114–117 |
| Test JVM time zone fixed (`user.timezone=Asia/Bangkok`), so the format-only smoke assertion is the right choice | Yes | `build.gradle.kts` `tasks.withType<Test>().configureEach` |
| Table rows well-formed | Yes, all files | script count of unescaped pipes per row against the header |

## 5. Observations (not defects)

- **Hard-coded module code `P2` in tooling.** The PLAN-007 fix makes `BoundaryRules` look up the module by the code `P2`. This is not a package literal, so T-TE001-15, SPEC-003 and BR6 ("no recovery package literal in the rule code") are not breached. The module name still comes from the map. AGENTS.md v2 §4 rule 3 supports P2 as the outbound route. It is still a fixed identifier in tooling; if the map ever renumbers modules (D-RCV-02 makes that unlikely), BND-5 text changes. No change is needed.
- **Console text claim in T-TE001-13.** "The console shows only the failed test name" is slightly imprecise. Gradle's default short exception format also prints the exception class and source line, without the message. The conclusion, that the BND-5 line must be read from the JUnit XML, holds. This was not run at review time.
- **Timeout wording.** `plan.md` "Carried plan inputs" R2-1 still says the timeout is "on the `describe`", while the Frontend Plan (line 236) adds the `beforeAll` hook timeout. The Frontend Plan is the fuller statement and does not contradict the earlier one.
- **Fixture exact counts depend on fixture authoring.** For example, `HttpClient.newBuilder().build()` in a field initializer would add a `HttpClient$Builder` target, and calling a `VendorClient` factory would add a `VendorClient` pair. The Builder must write fixture accesses so that each listed class has exactly the listed targets. `data-model.md` §3 already describes them as field declarations only.
- **Contracts unchanged since round 1** (timestamps and content). They remain consistent with the v2 plan. `CON-RWB-TE-001-002` `failureTexts` points to `data-model.md` §4.
- **Coverage credibility, HV-01, one-module reading, characterization tests (PA-07):** unchanged from round 1 and still sound.

## 6. Result

```text
PLAN_GATE: FAIL [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 4]
ROUND_1_FINDINGS: PLAN-001..007 RESOLVED (7/7); residual or new gaps from the fixes recorded as PLAN-008 (from PLAN-005), PLAN-009 (from PLAN-007), PLAN-010 (from PLAN-002)
PLAN_GATE_FINDINGS: REVIEW-RWB-TE-001-PLAN-008..011 (all Low)
PLAN_REQUIREMENT_COVERAGE_RESULT (reviewer check): CONFIRMED [TOTAL_RULES: 13] [TASK_COVERED_RULES: 13] [MISSING_TASK_RULES: 0] [CONTRADICTIONS: 0]
REVIEW_GATE_WARNING: Low-severity review failure does not automatically stop this handoff; unresolved findings may carry downstream. Human disposition required.
```

Overall status: **FAIL** (Low only). Counts: Critical 0, High 0, Medium 0, Low 4.
