# Plan gate review: RWB-TE-001 (run INC-002-epic-1-RWB-TE-001), round 3

| Field | Value |
|---|---|
| Stage | Compliance Reviewer, plan gate (`planning-execution-gates.md`), round 3 |
| Story | RWB-TE-001 Recovery module folder and boundary test |
| Reviewed | `plan/plan.md` (v3), `plan/tasks.md` (v3), `plan/data-model.md` (v3), `plan/tests/scenarios.md` (v3), `plan/assumptions.md`, `plan/document-gaps.md`, `plan/shared-updates.md`, `plan/contracts/backend-apis.json`, `plan/contracts/frontend-integrations.json`, `plan/agent-run-log.md` (round 3 section) |
| Checked against | Approved spec v4 (`specify/spec.md`, spec gate round 5 PASS); round-1 and round-2 reviews (`review/plan-gate-review.md`, `review/plan-gate-review-2.md`); `AGENTS.md` v2; `AI-SDLC-BUILD-LOG.md` D-RUN-01..18; the code (`backend/build.gradle.kts`, `backend/src/main/resources/application.yaml`, `RecoveryBoundaryTest.java`, the four baseline packages `platform`, `rules`, `workflow`, `documents`), `scripts/dev.ps1`, `.env.example`, `.gitlab-ci.yml`; the RWB-E1-042 and RWB-E1-044 specs (D-RUN-17/18 interaction only); source documents AI Assisted Development Approach v1 and Story file v7 (RWB-TE-001 v1) |
| Reviewer | Compliance Reviewer agent, started by the orchestrator (Claude Code). Read only; this file is the only file written. |

## 1. Earlier findings

| Finding | Result | Evidence |
|---|---|---|
| PLAN-001 TASK-13 row malformed | **RESOLVED** (held) | Note N-1 under the task table (`tasks.md` lines 46–52). A script count of unescaped `\|` per row against the header, over all ten plan files, finds no mismatch. |
| PLAN-002 TASK-01 `check` wiring | **RESOLVED** (held) | TASK-01 Verification still states `check --dry-run` does not list `:recoveryCoverageVerification`, compared with the TASK-00 baseline. |
| PLAN-003 T-TE001-13 Run 1 evidence | **RESOLVED** (held) | TASK-17 names `backend/build/test-results/test/TEST-th.co.scb.ace.demo.recovery.architecture.RecoveryBoundaryTest.xml`; no `testLogging` edit. |
| PLAN-004 "stricter BND-5" | **RESOLVED** (held) | grep of `plan/` for "stricter": the only hit is PA-05, which is unrelated to BND-5. |
| PLAN-005 determinism guard | **RESOLVED** (held) | Guard `determinismRuleSelectsTheSmokeWorkflowImpl` present (`plan.md` "`RecoveryBoundaryTest` changes"). |
| PLAN-006 violation unit | **RESOLVED** (held) | `data-model.md` §4 (line 61) defines one distinct (origin, target) pair per BND rule. |
| PLAN-007 BND-5 `{module}` order | **RESOLVED** (held) | `{module}` is the map module with code `P2` (`data-model.md` line 66). |
| PLAN-008 guard written in the green task | **RESOLVED** | TASK-09 description and red Verification now include `determinismRuleSelectsTheSmokeWorkflowImpl`. TASK-11 step 5 and its `RecoveryBoundaryTest.java (guard)` file entry are removed. The TASK-11 Trace adds SPEC-026 and T-TE001-05, and its Verification keeps "guard green". The `tasks.md` line 12 claim "TASK-01, -03, -06, -09 and -10 are red before TASK-04, -07 and -11" is now true for the guard. |
| PLAN-009 BND-5 fallback untested | **RESOLVED as asked**, residual recorded as PLAN-013 | `data-model.md` line 66: "a map with no `P2` module prints the origin class's own module name, and an origin class in no map module prints the origin's package". New map `bnd5-nop2.yaml` (`data-model.md` line 50; TASK-05 "9 maps, including bnd5-nop2.yaml"). New named test `BoundaryRulesTest.bnd5TextWithoutP2UsesTheOriginModule` (`scenarios.md` line 50; TASK-06). PA-04 updated. |
| PLAN-010 dry-run baseline evidence | **RESOLVED** | TASK-00 Verification names `implement/backend/check-dryrun-baseline.txt`. TASK-01 Verification names `check-dryrun-after.txt` and a recorded diff. |
| PLAN-011 `tasks.md` source version | **RESOLVED** | `tasks.md` line 10: "Source: `plan.md` v3 and `../specify/spec.md` v4". |

## 2. Gate structure (re-check)

| Check | Result | Evidence |
|---|---|---|
| Status block, `## Pre-submit checks` | Present | `plan.md` §Status; `tasks.md` §"Pre-submit checks" |
| Every file, test and task named | Yes (19 tasks TASK-00..18; every task has Files, Trace, BLOCKED_BY, Verification) | `tasks.md` task table; `plan.md` file tables |
| Tests before code | Yes in the dependency graph; one sequencing defect in the red steps (PLAN-015) | `tasks.md` graph and BLOCKED_BY |
| SPEC → task → test | Complete for SPEC-001..026 (021 withdrawn); the new fallback test is missing from the SPEC-010 map rows (PLAN-013) | `plan.md` "SPEC to task map" line 315; `scenarios.md` §5 |
| AC1–AC7, BR1–BR6 → task and named test | `TOTAL_RULES: 13`, `TASK_COVERED_RULES: 13`, consistent in `plan.md`, `tasks.md` and the spec | `plan.md` §"Requirement Logic To Task Coverage" |
| One module | PA-12 reading (ACE module = recovery) kept; conflicts with another story's reading in this run (PLAN-016) | `assumptions.md` PA-12 |
| No new dependency | Yes. SnakeYAML 2.6 is already on the classpath (Gradle cache, Spring Boot managed); no `build.gradle.kts` dependency line is added | TASK-01 edits only the two JaCoCo tasks |
| No migration (D-RUN-07) | Yes | `data-model.md` intro; no `V*.sql` in any file table |
| D-RUN-08 seams only | Yes (SPEC-016 list, SU-P02/-P03) | `shared-updates.md` |
| Tests not skipped or weakened | Held. One assertion set cannot pass under the merge-gate command (PLAN-012); the fix must not weaken it | `scenarios.md` T-TE001-12 |
| Personal data | None. Maps, fixtures and texts hold class and package names; §5 defaults are local placeholders | `data-model.md` §3–§5 |
| Attribution | No text records a human approval, acceptance or disposition. Triage is attributed to the orchestrator (Claude Code) | grep of `plan/` for approv/accept/dispos/human |

## 3. Findings

### REVIEW-RWB-TE-001-PLAN-012 — Medium — The T-TE001-12 binding tests fail under `./scripts/dev.ps1 test`, the SPEC-012 (b) merge gate, because `dev.ps1` exports `.env` into the test JVM's environment

- **Affects:** `tasks.md` TASK-10, TASK-11, TASK-13, TASK-17 (Runs 2 and 3); `tests/scenarios.md` T-TE001-12 and T-TE001-13; `data-model.md` §5; SPEC-012 (b), SPEC-023; D-RUN-06.
- **Evidence:**
  - The binding tests read the real `application.yaml` through `ConfigDataApplicationContextInitializer` (`scenarios.md` line 54; TASK-10). `application.yaml` binds from environment placeholders: line 76 `temporal: ${RWB_P3_TEMPORAL:false}`, line 77 `drools: ${RWB_P3_DROOLS:false}`, line 82 `password: ${RWB_MIGRATOR_PASSWORD:}`.
  - The asserted values are the placeholder defaults: "`temporal=false`, `drools=false` … empty password" (`scenarios.md` T-TE001-12, from `data-model.md` §5).
  - `scripts/dev.ps1` lines 86–87 run `Initialize-EnvFile` (copies `.env.example` to `.env` when missing) and `Import-EnvFile` before the command switch. `Import-EnvFile` (lines 44–49) sets every entry with `[Environment]::SetEnvironmentVariable(..., "Process")`. Line 114 `"test"` then runs `Invoke-Gradle @("test")`, whose test JVM inherits that environment.
  - `.env.example` line 19 `RWB_P3_TEMPORAL=true`, line 20 `RWB_P3_DROOLS=true`, line 8 `RWB_MIGRATOR_PASSWORD` set to a non-empty local placeholder.
  - Result under `dev.ps1 test`: `PlatformConfigTest.bindsFlagsFromApplicationYaml` binds `temporal=true`, `drools=true` and fails; `RecoveryFlywayConfigTest.bindsSchemaAndFlywayFromApplicationYaml` binds a non-empty password and fails. TASK-17 Run 2 ("Gradle green") and Run 3 (exit 0), and therefore the SPEC-012 (b) local merge gate ("`./scripts/dev.ps1 test` exit 0") and D-RUN-06, cannot pass.
  - The plan does not see this because TASK-13 runs `./gradlew test` directly and CI (`.gitlab-ci.yml` backend-unit: `./gradlew --no-daemon test recoveryCoverageReport`) loads no `.env`. The T-TE001-12 phrase "the values `RecoveryProperties` binds today" is also ambiguous: under `dev.ps1` today it binds `true`.
- **Fix:**
  - Isolate every T-TE001-12 context from the process environment and system properties so that only `application.yaml` and its placeholder defaults apply. For example, remove the `systemEnvironment` property source (and system properties) from the context's environment in an initializer that runs before `ConfigDataApplicationContextInitializer`, or supply a `StandardEnvironment` subclass with no system sources to the `ApplicationContextRunner`. State the mechanism in `plan.md` "Coverage tests" and TASK-10.
  - Apply the same isolation to any other test context that reads `application.yaml` (for example the `SecurityConfigTest` MVC slice), or state why its assertions do not depend on `.env` keys.
  - Add to TASK-13 (or TASK-17 Run 2) a verification that the binding tests pass with the `.env.example` values exported, for example by running the backend tests through `./scripts/dev.ps1 test`.
  - Pin T-TE001-12 wording to "the `application.yaml` placeholder defaults". Do not edit `.env.example` and do not weaken or drop the assertions.

### REVIEW-RWB-TE-001-PLAN-013 — Low — The fallback branches are not all asserted, and the plan claims they are

- **Affects:** `data-model.md` §3 (bnd4 world) and §4 BND-5 row; `assumptions.md` PA-04; `tests/scenarios.md` line 50 and §5; `plan.md` "SPEC to task map" row 010 (line 315); TASK-06; SPEC-010; AGENTS.md §3 rule 10.
- **Evidence:**
  - BND-5 "origin in no map module → origin's package": the branch runs in the nop2 evaluation (`PartnerHttpAdapter`, in `integration.adapter`, is in no module of `bnd5-nop2.yaml`), but `bnd5TextWithoutP2UsesTheOriginModule` asserts only the `SampleService` line (`scenarios.md` line 50) and no exact count. The origin-package text is never asserted.
  - BND-4/1/2 "target outside every module and external root → its package": the bnd4 world's outside-root entity is `collection.internal.CollectorEntity`, which is under the external `collection` root, so its text is "Use collection.api". No fixture target is outside every module and external root, so the package branch never runs.
  - Yet `data-model.md` §4 says "Both branches are tested (bnd5 and bnd5-nop2 maps)" and PA-04 says both fallbacks are tested "by `bnd5TextWithoutP2UsesTheOriginModule` and the BND-4 convention". Both overstate the coverage.
  - The new test is not listed in the SPEC-010 rows of `plan.md` line 315 or `scenarios.md` §5.
- **Fix:**
  - Make `bnd5TextWithoutP2UsesTheOriginModule` assert the full nop2 line set with an exact count, including the `PartnerHttpAdapter` lines ending `Use th.co.scb.ace.boundaryfixture.bnd5.recovery.integration.adapter.api or an application event.` (the `{module}.api` template filled with the origin's package).
  - Add a bnd4 entity outside every module and external root (or another world's equivalent) and assert its package text; or drop the package convention and fail explicitly, with a named test.
  - Correct `data-model.md` §4 and PA-04 to state exactly what is tested, and add the test to the SPEC-010 rows.

### REVIEW-RWB-TE-001-PLAN-014 — Low — T-TE001-15 as written cannot pass: every tooling file declares the recovery package

- **Affects:** `tests/scenarios.md` T-TE001-15 (line 57) and the BR6 row (line 36); TASK-06, TASK-07; SPEC-003; BR6.
- **Evidence:** T-TE001-15 asserts "no occurrence of `th.co.scb.ace.demo.recovery`" in the source files of `T/architecture/boundary/` except `*Test.java`. Those files (`ModuleMap`, `ModuleMapLoader`, `BoundaryRules`, …) live in package `th.co.scb.ace.demo.recovery.architecture.boundary`, so each begins `package th.co.scb.ace.demo.recovery.architecture.boundary;`. The test is red forever, or the Builder must weaken it, which AGENTS.md §4 rule 5 forbids.
- **Fix:** Define the check precisely: exclude the `package` declaration and `import` lines, or match only string literals and annotation values. Keep it a named, failing-capable assertion (for example, a seeded literal in a scratch copy proves it fires).

### REVIEW-RWB-TE-001-PLAN-015 — Low — Red steps break the test compile for tasks that must run tests in between

- **Affects:** `tasks.md` TASK-03, TASK-04, TASK-05, TASK-07, TASK-08, TASK-09, TASK-10 (BLOCKED_BY and Verification); dependency graph (line 81).
- **Evidence:**
  - TASK-10 is BLOCKED_BY TASK-00 only, and its red Verification is "`./gradlew compileTestJava` fails (records and new packages missing)". That state lasts until TASK-11. If TASK-10 is written as early as the graph allows, the test source set does not compile, so the Verification runs of TASK-04, -05, -07, -08 and -09 (including TASK-09's red assertion run and the PLAN-008 guard) cannot run as specified.
  - TASK-03's compile-red likewise breaks TASK-05's `compileTestJava` check until TASK-04 is done.
- **Fix:** Make TASK-10 BLOCKED_BY TASK-08 and TASK-09 and run it immediately before TASK-11. Order TASK-05's compile check after TASK-04, or state in the task notes that compile-red tasks run directly before their green task.

### REVIEW-RWB-TE-001-PLAN-016 — Low — The "one module" reading is unsettled across this run and has no owner

- **Affects:** `assumptions.md` PA-12; `shared-updates.md`; `aisdlc/docs/open-items.md` (no entry); AGENTS.md §7, §9.
- **Evidence:**
  - PA-12 reads "touches one module" as the ACE module (recovery). On that reading the plan passes the Plan-approved gate.
  - The RWB-E1-042 spec in this run (rev 8, CLAR-025) reads the same rule the other way: "plan touches two modules (P3 and P4), AGENTS §7 → analyst before any code".
  - This plan touches P2, P3, P4, P5 and every module's `package-info`, and the story file gives the story's module as "P2 Integration" (Story file v7, RWB-TE-001 v1 line 18). Under the E1-042 reading this plan goes back to the analyst.
  - The plan records the reading as an assumption but raises no open item for the tech lead (AGENTS.md §9 "Plan approved" owner) and no shared update asking the orchestrator to apply one reading to every story.
- **Fix:** Add a `shared-updates.md` row asking the orchestrator (Claude Code) to settle one reading for all stories in the run, and an open item in `aisdlc/docs/open-items.md` for the tech lead. Keep PA-12 until it is settled. See GC-1.

## 4. Code claims verified

| Claim | True? | Evidence |
|---|---|---|
| 35 files in the four baseline packages (27 classes, 8 `package-info`) | Yes | file listing of `R/platform`, `R/rules`, `R/workflow`, `R/documents` |
| Cross-module edges after the move: `DroolsRuleEngine` → `RecoveryFlags`; `TemporalAdminController` → `ApiError` / `ApiProblemException` (plus `TemporalProperties`, `PlatformSmokeWorkflow`, `WorkflowIds` in its own module) | Yes | imports of both classes |
| `PdpaPayloadCodec` used only by `TemporalConfig` and its own package's tests, so package-private is safe | Yes | grep |
| `QuartzTimerScheduler` package-private; `TimerDueJob` public static | Yes | source |
| `DroolsProperties` uses the nested `Registration` pattern | Yes | source |
| Nested types `RuleEngine.RuleCompilationException`, `TimerScheduler.TimerDue`, `DocumentStore.StoredDocument`, `DocumentStore.DocumentImmutableException` | Yes | source |
| BND-5 clean on the real code (only `BlobDocumentStore` uses `com.azure.storage`; `java.net.URI` / `InetAddress` match no entry) | Yes | grep of `R/` imports against the 16 library entries |
| Determinism rule keeps `allowEmptyShould(true)` | Yes | `RecoveryBoundaryTest.java` |
| No `testLogging`; `test` finalizedBy `recoveryCoverageReport`; `recoveryCoverageVerification` not wired to `check` | Yes | `build.gradle.kts` |
| `RecoveryFlywayConfig` is `@ConditionalOnProperty(rwb.flyway.enabled, matchIfMissing=true)` with `@Bean(initMethod="migrate")` | Yes | source. Note: a binding test must not instantiate this configuration (it would migrate); TASK-10 binds the record only, which is correct |
| `application.yaml` defaults `temporal=false`, `drools=false`, empty password | Yes as defaults; overridden by `.env` under `dev.ps1` (PLAN-012) | `application.yaml` lines 76, 77, 82 |
| No other file in the repository (outside run outputs and build folders) names the old packages `recovery.platform/rules/workflow/documents` | Yes | grep of `*.md, *.yaml, *.yml, *.kts, *.ps1, *.json` |
| Frontend items (`src/auth/auth.tsx`, `@types/node` in tsconfig types, coverage excludes `__tests__`) | Yes | frontend sources and config |

## 5. D-RUN-17 and D-RUN-18

- **D-RUN-17 (TE-001 merges before E1-044).** Consistent. The E1-044 spec is aligned to TE-001 v4 and handles both a conditional and an unconditional registration of `RecoveryMigrationProperties`. The TASK-00 example "for example RWB-E1-044" (a story that might merge first) is stale under D-RUN-17 but harmless.
- **D-RUN-18 (reference-load handler SPI in P4 `access.api`, added by a later story).** The plan does not make that addition impossible. `access` publishes `[api]` in the module map, so a new type in `access.api` needs no map change. The P3 → P4 edge already exists and P4 depends on neither P1 nor P3. The T-TE001-14 (a) expected set for `access.api` (`backend-apis.json` `publishedJavaTypesAfterRelocation`: `[ApiError, ApiProblemException]`) is exact, so RWB-E1-043 must extend it in the same merge request. SU-P02 requires this generically, and the E1-042 spec already states E1-043 extends it (A-41). T-TE001-14 (b) concerns `casewf` only. No finding; see observation below.

## 6. Observations (not defects)

- **SU-P02 examples predate D-RUN-18.** They do not name the E1-043 `access.api` SPI. The generic rule covers it; adding the example would help the E1-043 planner.
- **Hard-coded module code `P2` in tooling** (round-2 observation) still stands and is not a package literal; it is unaffected by PLAN-014 once the check excludes the `package` line.
- **Fixture exact counts depend on fixture authoring** (round-2 observation) also applies to the new `bnd5-nop2` assertions under PLAN-013.

## 7. Document-gap candidates

| ID | Gap | Citation 1 | Citation 2 | Blocker |
|---|---|---|---|---|
| GC-1 | "Module" in the one-module plan rule is undefined: the rule can be read as the ACE module (recovery) or as one of the 19 design modules. The two readings give opposite Plan-approved results, and two stories in this run already use different readings. | AI Assisted Development Approach v1 §5 ("A plan that touches more than one module … goes back to the analyst") and §7 (Plan approved: "touches one module") | AI Assisted Development Approach v1 §3.1 ("The Workbench is the recovery module of the ACE service"), against Story file v7 RWB-TE-001 v1 (Module "P2 Integration"; §13 step 1 creates the 19 design modules), with the opposite reading applied in the RWB-E1-042 spec CLAR-025 | No. The story file itself requires touching every design module; PA-12 records the reading, and the orchestrator can settle it for the run (PLAN-016). |

## 8. Result

```text
PREVIOUS_FINDINGS: PLAN-001..011 RESOLVED (11/11); residual from the PLAN-009 fix recorded as PLAN-013
PLAN_GATE_FINDINGS: REVIEW-RWB-TE-001-PLAN-012 (Medium), PLAN-013..016 (Low)
PLAN_REQUIREMENT_COVERAGE_RESULT (reviewer check): CONFIRMED [TOTAL_RULES: 13] [TASK_COVERED_RULES: 13] [MISSING_TASK_RULES: 0] [CONTRADICTIONS: 0]
D_RUN_18_COMPATIBILITY: CONFIRMED (access.api extension possible; E1-043 extends the T-TE001-14 (a) set in its own merge request)
```

Overall status: **FAIL** (a Medium finding blocks the Builder). Counts: Critical 0, High 0, Medium 1, Low 4.

PLAN_GATE: FAIL [CRITICAL: 0] [HIGH: 0] [MEDIUM: 1] [LOW: 4]
