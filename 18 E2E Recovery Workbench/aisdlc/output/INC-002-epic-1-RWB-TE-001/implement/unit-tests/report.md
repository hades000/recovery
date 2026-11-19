# Unit test evidence: RWB-TE-001 (run INC-002-epic-1-RWB-TE-001)

All commands ran in `rwb-wt/RWB-TE-001` with
`JAVA_TOOL_OPTIONS=-Djdk.net.unixdomain.tmpdir=%USERPROFILE%\.gradle\uds` for Gradle.
The headline tables below are the final, post-review numbers; the earlier snapshot is kept and
labelled in "Pre-fix snapshot" rather than deleted.

## Results (final)

| Surface | Passed | Failed | Skipped | Statements % | Branches % | Functions % | Lines % | Required % | Status | Evidence |
|---|---|---|---|---|---|---|---|---|---|---|
| Backend | 141 | 0 | 0 | 97.31 (INSTRUCTION) | 95.31 | 97.91 (METHOD) | 97.46 | 80 | PASS | `backend/review1-green.log`, `backend/review1-suites.txt`, `backend/coverage/recoveryCoverageReport.xml`, `backend/coverage/html/` |
| Frontend | 28 | 0 | 0 | 91.89 | 88.09 | 82.35 | 91.66 | 80 | PASS | `frontend/review1-check.log`, `frontend/coverage-summary.json`, `frontend/lcov.info`; import test 18/18 in `frontend/review1-vitest.log` |
| UI / design | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | NOT_APPLICABLE | UI In Scope NO, `DESIGN_EVIDENCE_STATUS: NOT_REQUIRED` (spec.md) |

Backend metric names map to the native counters: statements = INSTRUCTION, functions = METHOD,
branches = BRANCH, lines = LINE (JaCoCo). No metric is `NOT_SUPPORTED`; JaCoCo provides all four.

Per-class note: every class is at or above 80% on lines; `SecurityConfig` is 62.5% on branches (5/8)
because the audience validator's branches need a real token from the JWKS endpoint, which the test
scope forbids (no network). The bundle branch gate is 95.31%.

## Commands

| Surface | Command | Working directory | Exit | Time | Native report |
|---|---|---|---|---|---|
| Backend | `./gradlew.bat --offline cleanTest test recoveryCoverageVerification` | `backend/` | 0 | 2 m 59 s | `backend/review1-green.log`; `backend/build/reports/jacoco/recoveryCoverageReport.xml` + HTML, copied to `backend/coverage/` |
| Backend (red, TASK-01, pre-fix) | `./gradlew.bat --offline test recoveryCoverageVerification` | `backend/` | 1 | 9 s | `backend/task01-red.log` |
| Backend (moved suite, pre-fix) | `./gradlew.bat --offline test` | `backend/` | 0 | — | `backend/task11-green.log`, `backend/task13-suites.txt` |
| Backend (integration) | `./gradlew.bat --offline recoveryIntegrationTest` | `backend/` | 0 | 1 m 27 s | `backend/it.log`, `RecoveryDatabaseIT` 6/6 |
| Frontend | `npx vitest run src/modules/recovery/__tests__/importBoundary.test.ts` | `frontend/` | 0 | 3.5 s | `frontend/review1-vitest.log` (18/18) |
| Frontend | `npm run check` | `frontend/` | 0 | 5.4 s | `frontend/review1-check.log`, `frontend/coverage-summary.json`, `frontend/lcov.info` |
| Frontend | `npm run build` | `frontend/` | 0 | 0.5 s | `frontend/review1-build.log` |

## Coverage scope

Backend: every main class under `th/co/scb/ace/demo/recovery/**` plus the test-scope tooling package
`th/co/scb/ace/demo/recovery/architecture/boundary/**` (`ModuleMap`, `ModuleMapLoader`,
`BoundaryRules` and its conditions), excluding `**/*Test.class`, `**/*Test$*.class` and the fixture
root `th/co/scb/ace/boundaryfixture/**`. No main class is excluded. Execution data is the `test` task
only. This is the approved scope of `plan.md` and SPEC-020, unchanged since TASK-01.

Frontend: `src/modules/recovery/**` excluding `__tests__` and `i18n`, the inherited configuration in
`frontend/vite.config.ts` (SPEC-020, D-RCV-40). No exclusion was added.

## Backend suite breakdown

22 suites, **141** tests, 0 failures, 0 errors (`backend/review1-suites.txt`), including
`ModulithTest` (2), `RecoveryBoundaryTest` (11), `RecoveryMigrationLintTest` (3), the four moved
tests (`QuartzTimerSchedulerTest` 3, `DroolsRuleEngineTest` 4, `PdpaPayloadCodecTest` 7,
`PlatformSmokeWorkflowTest` 1), the SPEC-024 classes (`ApiErrorTest` 3,
`ApiExceptionHandlerTest` 8, `SecurityConfigTest` 11, `PlatformConfigTest` 2,
`PlatformInfoControllerTest` 2, `RecoveryFlywayConfigTest` 5, `TemporalAdminControllerTest` 7,
`TemporalConfigTest` 6, `WorkflowIdsTest` 2, `BlobDocumentStoreTest` 11, `DroolsPropertiesTest` 1,
`RuleFactsTest` 4) and the boundary tooling tests (`BoundaryRulesTest` 17,
`ModuleMapLoaderTest` 28, `ModulithFixtureTest` 3).

## Review fix round 1 re-run

After the pre-merge review fixes (rebased red `35d5ec0`, green `90550d3`): `./gradlew cleanTest test
recoveryCoverageVerification` exit 0 with 141 tests, 0 failures; coverage LINE 97.46%, INSTRUCTION
97.31%, BRANCH 95.31%, METHOD 97.91%. Frontend: `importBoundary.test.ts` 18 tests, `npm run check`
28 tests, `npm run build` exit 0; coverage lines 91.66%, statements 91.89%, branches 88.09%,
functions 82.35%. Evidence: `backend/review1-green.log`, `backend/review1-suites.txt`,
`frontend/review1-vitest.log`, `frontend/review1-check.log`, `frontend/review1-build.log`.

## Code gate fix round 2

CODE-005/CODE-006 only change the test-strength of `RecoveryBoundaryTest`; both new assertions pass on
the current code (they close gaps, they are not regressions). `RecoveryBoundaryTest` 11/11 in
`backend/codegate-code005-006.log` at commit `55f1ed4`. The full backend and frontend suites were not
re-run for this test-only edit beyond that class; the orchestrator runs `dev.ps1 test` at the final
tip (CODE-007). Evidence refresh: CODE-003.

## Pre-fix snapshot (superseded, kept for the record)

Headline at TASK-18 before the two review rounds:

| Surface | Passed | Failed | Skipped | Statements % | Branches % | Functions % | Lines % | Required % | Status | Evidence |
|---|---|---|---|---|---|---|---|---|---|---|
| Backend | 140 | 0 | 0 | 97.32 (INSTRUCTION) | 95.31 | 97.92 (METHOD) | 97.47 | 80 | PASS | `backend/task13-coverage.log`, `backend/task13-suites.txt` |
| Frontend | 25 | 0 | 0 | 91.89 | 88.09 | 82.35 | 91.66 | 80 | PASS | `frontend/task16-check.log` |
| UI / design | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | NOT_APPLICABLE | UI In Scope NO |

## Failures

None in the final runs. Every red run is kept as evidence under `backend/task*-red.log`,
`backend/review1-red.log` and `frontend/review1-red.log`.
