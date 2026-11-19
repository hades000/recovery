# Implementation report: RWB-TE-001 (run INC-002-epic-1-RWB-TE-001)

Stage: implement. Story: RWB-TE-001 Recovery module folder and boundary test (EPIC-001).
Plan: `../plan/plan.md` v7, `../plan/tasks.md` v7. Spec: `../specify/spec.md` v4.
Worktree: `rwb-wt/RWB-TE-001`, branch `feature/RWB-TE-001-module-boundary`, base `8675a5c`.

## Result

`IMPLEMENT_STATUS: SUCCESS` for every task the builder could execute. One task (TASK-14 end-to-end)
is `BLOCKED` on its e2e half by the run rule that forbids `scripts/dev.ps1 up` from the worktree; the
Testcontainers half passed. See `deviations.md` DEV-01.

| Gate | Result |
|---|---|
| `./gradlew test recoveryCoverageVerification` | exit 0; LINE 97.46%, INSTRUCTION 97.31%, BRANCH 95.31%, METHOD 97.91% (each ≥ 0.80) |
| `./gradlew test` | exit 0; 141 tests, 0 failures, 0 errors |
| `./gradlew recoveryIntegrationTest` | exit 0; `RecoveryDatabaseIT` 6 tests, 0 failures |
| `npm run check` | exit 0; 28 tests; lines 91.66%, statements 91.89%, branches 88.09%, functions 82.35% |
| `npm run build` | exit 0 |
| Old-package search (N-1) | no match; the four baseline packages are gone |
| No new dependency | `dependencies` diff empty (see `backend/deps-diff.txt`) |

## Surfaces

| Surface | Change | Unit tests | Status |
|---|---|---|---|
| Backend | YES (relocation, module skeleton, tooling, property split, coverage gate) | REQUIRED, 141 tests | PASS |
| Frontend | YES (test only) | REQUIRED, 28 tests | PASS |
| UI / design | NO (`UI In Scope: NO`, `DESIGN_EVIDENCE_STATUS: NOT_REQUIRED`) | N/A | NOT_APPLICABLE |
| API contract | `NO_API_CHANGE`; two controllers move package only | inherited e2e | NO_API_CHANGE |

## Test-first evidence

| Pair | Red commit / evidence | Green commit / evidence |
|---|---|---|
| TASK-01 | `fe88d50` (inherited), `backend/task01-red.log`: four counters below 0.80 | TASK-13 run, `backend/task13-coverage.log` |
| TASK-02/03 → TASK-04 | `440b3c6`, `backend/task03-red.log`: no `ModuleMapLoader` | `e04fce3`, `backend/task04-green.log` |
| TASK-05 | `53510fb`, `backend/task05-green.log`: fixtures compile | — |
| TASK-06 → TASK-07 | `c4a6ae4`, `backend/task06-red.log`: no `BoundaryRules` | `e34f42a`, `backend/task07-green.log` |
| TASK-08 | `220138d` (fixture proof; passes when written, as Spring Modulith owns the behaviour) | — |
| TASK-09 → TASK-11 | `220138d`, `backend/task09-red.log`: baseline packages, skeleton and surface fail | `5df3097`, `backend/task11-green.log` |
| TASK-10 → TASK-11 | `220138d`, `backend/task10-red.log`: new packages and records absent | `5df3097`, binding tests in `backend/task11-green.log` |
| TASK-12 | — (characterization tests, plan PA-07) | `8bad2e7`, `backend/task13-coverage.log` |
| TASK-15/16 | — (proves the inherited rule) | `473f0af`, `frontend/task15-vitest.log`, `frontend/task16-check.log`, `frontend/task16-build.log` |

The SHAs in this table are the original commits. The branch was rebased on 18 Nov (`3cb6c9d` →
`90550d3`, content-identical; the review-fix pair is now `35d5ec0`/`90550d3`), and the code-gate fix
is `55f1ed4`.

## CODE-* traceability

| CODE | Unit | TASK | SPEC | Test |
|---|---|---|---|---|
| CODE-RWB-TE-001-001 | `backend/build.gradle.kts` coverage tasks | TASK-01 | SPEC-020 | T-TE001-10 (`backend/task01-red.log`, `backend/task13-coverage.log`) |
| CODE-RWB-TE-001-002 | `backend/src/test/resources/architecture/recovery-modules.yaml` | TASK-02 | SPEC-002, -025 | `ModuleMapLoaderTest.loadsTheRealMap` |
| CODE-RWB-TE-001-003 | `ModuleMap.java` | TASK-04 | SPEC-003 | `ModuleMapLoaderTest` |
| CODE-RWB-TE-001-004 | `ModuleMapLoader.java` | TASK-04 | SPEC-003 | `ModuleMapLoaderTest` (28 tests) |
| CODE-RWB-TE-001-005 | `BoundaryRules.java` | TASK-07 | SPEC-004..-010 | `BoundaryRulesTest` (17 tests) |
| CODE-RWB-TE-001-006 | `boundaryfixture/**` fixture worlds | TASK-05 | SPEC-011, -019 | every `BoundaryRulesTest` world, `ModulithFixtureTest` |
| CODE-RWB-TE-001-007 | `architecture/fixtures/*.yaml` (9 maps) | TASK-05 | SPEC-011 | as CODE-006 |
| CODE-RWB-TE-001-008 | `RecoveryBoundaryTest.java` | TASK-09 | SPEC-001, -004, -009, -025, -026 | its 11 tests, real main classes |
| CODE-RWB-TE-001-009 | `ModulithFixtureTest.java` | TASK-08 | SPEC-007, -011 | its 3 tests |
| CODE-RWB-TE-001-010 | 61 `package-info.java` (19 modules × 3, plus 4 published) | TASK-11 | SPEC-001 | `RecoveryBoundaryTest.everyMapModuleHasApiAndInternalPackageInfo`, `moduleMapRule` |
| CODE-RWB-TE-001-011 | 26 relocated main classes (11 files carry a move and an edit) | TASK-11 | SPEC-022 | `ModulithTest`, `RecoveryBoundaryTest`, moved tests |
| CODE-RWB-TE-001-012 | `RecoveryFlagProperties`, `PlatformInfoProperties`, `RecoveryMigrationProperties`, `RecoverySecurityProperties` | TASK-11 | SPEC-023 | the five T-TE001-12 binding tests |
| CODE-RWB-TE-001-013 | 4 moved test classes | TASK-11 | SPEC-022 (f) | unchanged assertions, `backend/task11-green.log` |
| CODE-RWB-TE-001-014 | 11 coverage test classes (plus `RuleFactsTest`) | TASK-12 | SPEC-024 | `backend/coverage/recoveryCoverageReport.xml` |
| CODE-RWB-TE-001-015 | `testsupport/ApplicationYamlEnvironment.java` | TASK-10 | SPEC-023; PLAN-012 | used by the five binding tests |
| CODE-RWB-TE-001-016 | `frontend/src/modules/recovery/__tests__/importBoundary.test.ts` | TASK-15 | SPEC-014, -015 | 18 cases (11 rejected + 7 allowed), `frontend/review1-vitest.log`; case-count change in `../plan/plan-addendum.md` A-3 |
| CODE-RWB-TE-001-017 | `ModuleMapLoaderTest.java` | TASK-03 | SPEC-003 | 28 tests |
| CODE-RWB-TE-001-018 | `BoundaryRulesTest.java` | TASK-06 | SPEC-004..-011 | 17 tests |

## Scope

Edited shared files: `backend/build.gradle.kts` (coverage gate, planned) and
`frontend/eslint.config.js` (SEC-TE001-01 tightening, DEV-08; `../plan/plan-addendum.md` A-1).
No change to `.gitlab-ci.yml`, `scripts/dev.ps1`, `application*.yaml`, `db/**`,
`frontend/package*.json`, `vite.config.ts`, `tsconfig.json`, `.env.example`. No new dependency,
endpoint or migration.

## Review fix round 1

Pre-merge reviews: `../review/ponytail-review.md` (2 Must, 1 Should, 2 Nice) and
`../review/security-review.md` (SEC-TE001-01, Medium). Commits: `bedecbd` (tests, red),
`3cb6c9d` (fixes, green). Branch head after the round: `3cb6c9d`.

| Finding | Fix | Evidence |
|---|---|---|
| Ponytail Must 1: `ApiError` re-encoded, Thai `messageTh` mojibake | `access/api/ApiError.java` restored from `8675a5c`'s `platform/api/ApiError.java`; the file now differs from the base in the `package` line only (195 Thai code points, verified). The three `Â§` comments in `ApiExceptionHandler`, `TemporalAdminController` and `PlatformSmokeWorkflowTest` restored to `§`. | `backend/review1-green.log`, `backend/review1-suites.txt` |
| Ponytail Must 2: BND-1/BND-2 accepted sub-packages of a published external package | `BoundaryRules.ExternalCondition` compares the target package exactly (`equals(external.rootPackage() + "." + entry)`). New `bnd2` fixtures: `common/api/internal/SecretHelper` used by `SampleSecretReader` (fails), and `common/api/CustomerLookup` used by `SampleLookupUser` (passes). `BoundaryRulesTest` asserts both lines and the passing control. `RecoveryBoundaryTest` needs no change; the text is unchanged. | `backend/review1-red.log` (failing), `backend/review1-green.log` |
| Ponytail Should 3: Thai tests asserted only the Latin placeholder | `ApiErrorTest` and `ApiExceptionHandlerTest` now assert the exact Thai `NOT_PERMITTED` string with `{action}` filled; both failed on the mojibake file before the restore (`backend/review1-red.log`). | `backend/review1-green.log` |
| Ponytail Nice 4: five same-package imports | Removed from `DroolsRuleEngine`; they were genuinely unused. | compile + tests |
| Ponytail Nice 5: `moduleFor` unused map parameter | Helper deleted; the BND-1/BND-2 text uses `external.name()` directly. | compile + tests |
| SEC-TE001-01: D-RCV-39 bypass with `..` behind an allowed prefix | `frontend/eslint.config.js` gains a `..` rejection, `regex: "^(?!\\.\\./).*\\.\\."`. The leading-`../` group already reports that form, so the guard keeps one message per import; the union rejects every specifier containing a `..` segment. Three cases added to `importBoundary.test.ts`; all failed before the rule (`frontend/review1-red.log`) and pass after (`frontend/review1-vitest.log`). No existing rule changed or weakened. | `frontend/review1-vitest.log`, `frontend/review1-check.log` |

Files changed in the round: `access/api/ApiError.java`, `access/internal/ApiExceptionHandler.java`,
`casewf/admin/TemporalAdminController.java`, `casewf/rules/DroolsRuleEngine.java`,
`casewf/workflow/internal/PlatformSmokeWorkflowTest.java`,
`architecture/boundary/BoundaryRules.java`, `frontend/eslint.config.js`, the four `bnd2` fixtures,
`BoundaryRulesTest.java`, `ApiErrorTest.java`, `ApiExceptionHandlerTest.java`,
`importBoundary.test.ts`.

Re-run after the fixes:

| Check | Result |
|---|---|
| `./gradlew cleanTest test recoveryCoverageVerification` | exit 0, 179 s; 141 tests, 0 failures, 0 errors |
| Coverage (bundle) | LINE 97.46%, INSTRUCTION 97.31%, BRANCH 95.31%, METHOD 97.91% (each ≥ 0.80) |
| `npx vitest run importBoundary.test.ts` | exit 0; 18 tests |
| `npm run check` | exit 0; 28 tests; lines 91.66%, statements 91.89%, branches 88.09%, functions 82.35% |
| `npm run build` | exit 0, 463 ms |

## Code gate fix round 2

Code gate: `../review/code-gate-review.md` (1 Medium CODE-001, 7 Low). The builder fixed CODE-003,
-005, -006 and recorded CODE-002/-004/-008; CODE-001 (e2e) and CODE-007 (`dev.ps1 test` at the tip)
are run by the orchestrator. Commit `55f1ed4` (`RecoveryBoundaryTest`, +13/-3).

| Finding | Fix | Evidence |
|---|---|---|
| CODE-003 stale headline counts and scope text | `unit-tests/report.md` headline is 141 backend / 28 frontend with the earlier 140/25 snapshot kept and labelled pre-fix; `scope-check.md` shows 230 changed files and `frontend/eslint.config.js` as a changed shared file; this report's gate, surface, CODE and Scope sections refreshed. | `backend/review1-suites.txt`, `frontend/review1-check.log` |
| CODE-005 literal published-package set | `RecoveryBoundaryTest.PUBLISHED_PACKAGES` is derived from `MAP.modules()` × `published`; the exact per-package type map is unchanged. A guard asserts the map still lists the six type-bearing packages; a map/annotation mismatch now changes the compared map and fails closed. | `backend/codegate-code005-006.log` |
| CODE-006 `casewf` named interfaces did not require `api` | Asserts `api`, `rules`, `timers`, `workflow`. Spring Modulith 2.1.1 reports `casewf.api` from its annotated `package-info` even though the package holds no type, so no exclusion is recorded. | `backend/codegate-code005-006.log` |
| CODE-002/-004/-008 spec/plan drift | Recorded in `../plan/plan-addendum.md` (A-1 eslint tightening and DEV-08; A-2 `RuleFactsTest` and `mapbad.CaseEventType`; A-3 the 18-case test list; A-4 the published-surface test strength). The gated spec and plan are not edited. | addendum |

`RecoveryBoundaryTest` 11/11 at `55f1ed4`; the full backend/frontend suites are the round-1 results
above, re-run at `90550d3`, and the branch tip after this round is `55f1ed4`.

## Status lines

```
IMPLEMENT_MCP_STATUS_SUMMARY: RWB-TE-001 implemented: module skeleton and relocation, map-driven boundary rules with fixtures, coverage gate, binding and coverage tests; both unit gates pass.
IMPLEMENT_MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]
IMPLEMENT_DESIGN_SOURCE: NOT_REQUIRED [NOTE: UI In Scope NO]
UI_FIDELITY_SUMMARY: No screen in scope; backend-only build enabler.
UI_FIDELITY_RESULT: NOT_APPLICABLE [TOTAL_NODES: 0] [MATCHED_NODES: 0] [MISSING_NODE_ARTIFACTS: 0] [STYLE_MISMATCHES: 0] [TEXT_MISMATCHES: 0] [CONTRADICTIONS: 0]
```
