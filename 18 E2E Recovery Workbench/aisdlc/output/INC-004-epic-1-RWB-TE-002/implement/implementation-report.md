# Implementation report: RWB-TE-002 Code owners for the recovery module

RUN_ID `INC-004-epic-1-RWB-TE-002`. Branch `feature/RWB-TE-002-code-owners` (worktree `rwb-wt/RWB-TE-002`), contains `develop-recovery` `0b87102` (merged at `a3af237`; original base `7bee04d`), final code tip `d018cf7`. Design Source: `NOT_REQUIRED`.

## Final tip `d018cf7` (current figures; everything below this section is superseded history)

Figures at `c740d25` (33 / 421 tests; 95.71/95.83/96.83/100) are superseded; their logs are in `implement/backend/superseded-c740d25/`.

Branch `feature/RWB-TE-002-code-owners`, tip `d018cf73c75d635fe2304fc5cd19e8c04e4d7576`, which contains `develop-recovery` `0b87102` (RWB-E1-042) through the merge `a3af237`. Remediation of the pre-merge reviews (D-RUN-09, D-RUN-25): red tests `1948f97`, green and addendum lines `c740d25`; code gate round 1 (CODE1-001..003): red `f61f133`, green `d018cf7`. Details: `plan-addendum.md`, `deviations.md` DEV-08, DEV-10, DEV-11.

| Commit | Kind |
|---|---|
| `1948f97` | Red: `emptyOwnerListStillChecksEveryOwner`, `dotSegmentPatternsAreRejected`, `noHigherPrecedenceCodeOwnersFileExists` (a repository-state guard, red only through a temporary uncommitted probe file, DEV-10), `addendumPathsHaveOwners`, F8 cache-key assertion, four reserved-pattern warnings in `liveFileAndRegisterPass` (`backend/red-remediation.txt`) |
| `a3af237` | Merge of `develop-recovery` (RWB-E1-042); UT-26 then red on `magic-number-baseline.csv` (`backend/red-magic-number.txt`, EXITCODE=1, 32 tests, 1 failed) |
| `c740d25` | Green: V7 fail closed, V4 dot segments, `codeOwnersTest` never up to date (+ guard test `codeOwnersTestIsNeverUpToDate`), CI cache key, D-RUN-25 addendum lines (CODEOWNERS 55 to 66 lines), two reserved patterns |
| `f61f133` | Red, code gate round 1 CODE1-001: `emptySegmentAndColonPatternsAreRejected`, `patternResolvingOutsideTheRootMatchesNoFile` (`backend/red-code1-001.txt`, EXITCODE=1, 35 tests, 2 failed) |
| `d018cf7` | Green: V4 rejects `//` and `:`, V9 requires the target under the repository root (CODE1-001); `host-settings.md` HC-09 (CODE1-002) |

| Run (at `d018cf7`) | Command | Exit | Result | Log |
|---|---|---|---|---|
| Codeowners suite + 80% gate | `gradlew --no-daemon clean codeOwnersTest codeOwnersCoverageVerification codeOwnersCoverageReport` | 0 | 35 tests, 0 failures, 0 errors, 0 skipped | `backend/final-tip-codeowners.log`, `backend/final-tip-counts.txt` |
| Backend unit suite | `gradlew --no-daemon test` (tags `recovery-it`, `e2e` excluded) | 0 | 423 tests, 0 failures, 0 errors, 0 skipped (now includes RWB-E1-042's tests) | `backend/final-tip-test.log`, `backend/final-tip-counts.txt` |
| Scope | `git diff --name-status develop-recovery` | - | 16 files; none under `frontend/`, `api/` or `backend/src/main/` | `backend/final-tip-scope.txt` |

UT-01..UT-26 run as 35 JUnit methods (28 original, 4 pre-merge remediation tests, 1 Nice-3 guard, 2 code gate round 1 tests); the list is in `backend/final-tip-counts.txt`.

Coverage, codeowners helper classes (`CodeOwnersFile`, `OwnerRegister`, `CodeOwnersValidator`, `OwnershipResolver`, with nested types), native JaCoCo XML `backend/coverage-final/codeOwnersCoverageReport.xml`:

| Counter | Missed | Covered | % | Gate 80 |
|---|---|---|---|---|
| LINE | 9 | 204 | 95.77 | PASS |
| BRANCH | 5 | 117 | 95.90 | PASS |
| INSTRUCTION | 41 | 1262 | 96.85 | PASS |
| METHOD | 0 | 43 | 100.00 | PASS |

| Surface | Status | Tests | Fail | Skipped | LINE | BRANCH | INSTRUCTION | METHOD |
|---|---|---|---|---|---|---|---|---|
| Backend (codeowners package) | PASS | 35 | 0 | 0 | 95.77 | 95.90 | 96.85 | 100.00 |
| Frontend | NOT_APPLICABLE | N/A | N/A | N/A | N/A | N/A | N/A | N/A |

Frontend and IT suites were not run at the final tip: `backend/final-tip-scope.txt` shows no change under `frontend/`, `api/` or `backend/src/main/`. The last frontend run is the superseded `dev-test.log` at `ae61b08`; the E1-042 post-merge `dev.ps1 test` and `it` on `develop-recovery` passed (build log 21:07).

```text
IMPLEMENTATION_STATUS: SUCCESS [TASKS: TASK-00..TASK-11 + D-RUN-25 remediation] [LOCAL_STATE: BUILT — ACCEPTANCE PENDING HV-01..HV-11]
BACKEND_UNIT_TESTS: PASS [TESTS: 35 codeowners / 423 backend] [LINE: 95.77] [BRANCH: 95.90] [INSTRUCTION: 96.85] [METHOD: 100.00]
FRONTEND_UNIT_TESTS: NOT_APPLICABLE [REASON: no frontend file changes, backend/final-tip-scope.txt]
OPEN: F3 placeholder groups (OPEN-038, recorded gap, Blocker No); F5 (PROP-OI-4); addendum ratification by the tech lead (IM-SU-04)
GATE_REVIEW: PENDING_ORCHESTRATOR (code gate not run by this stage)
```

---

## Superseded history (tip `ae61b08`, before the review remediation)

## Commits (tests first)

| Commit | Task | Kind |
|---|---|---|
| `9f2ece0` | TASK-01..03 | Red: 28 tests + compile-clean stubs; 28/28 fail, no compile error (`backend/red-task01-03.txt`) |
| `f28ada1` | TASK-04 | Green: parser, register reader, validator, resolver; fixture tests green, live tests red (`backend/green-task04.txt`) |
| `3e281c2` | TASK-05 | `.gitlab/CODEOWNERS` (spec block, line-for-line compared, 55 lines, one substitution), register, host settings; UT-12 red only on V9 for the template folder (`backend/green-task05.txt`) |
| `b9fe59b` | TASK-06 | MR template, AGENTS.md §5 cells; UT-12, UT-21, UT-22 green (`backend/green-task06.txt`) |
| `ae61b08` | TASK-07 | Gradle block and CI job exactly as `data-model.md` §6/§7; UT-24 green; `check --dry-run` lists no codeowners task; a CODEOWNERS-only edit re-runs `test` (`backend/task07-verification.txt`) |

## Code units

| CODE | File (under `backend/src/test/java/th/co/scb/ace/demo/recovery/architecture/codeowners/` unless stated) | TASK | SPEC |
|---|---|---|---|
| CODE-TE002-01 | `CodeOwnersFile.java` | TASK-04 | 001, 007, 008 |
| CODE-TE002-02 | `OwnerRegister.java` | TASK-04 | 009 |
| CODE-TE002-03 | `CodeOwnersValidator.java` | TASK-04 | 008 |
| CODE-TE002-04 | `OwnershipResolver.java` | TASK-04 | 007 |
| CODE-TE002-05 | `CodeOwnersValidationTest`, `OwnershipResolverTest`, `MergeRequestTemplateTest`, `AgentsContextPathsTest`, `PipelineDefinitionTest` | TASK-01..03 | 001..005, 007..009, 013, 015..017 |
| CODE-TE002-06 | `.gitlab/CODEOWNERS`, `.gitlab/codeowners-register.yaml`, `.gitlab/host-settings.md` | TASK-05 | 001..006, 009..012, 017, 018 |
| CODE-TE002-07 | `.gitlab/merge_request_templates/Default.md`, `AGENTS.md` §5 | TASK-06 | 015, 016 |
| CODE-TE002-08 | `backend/build.gradle.kts` (appended block), `.gitlab-ci.yml` (`codeowners-validation`) | TASK-07 | 013, 014 |

## [Superseded, ae61b08] Tests

- Codeowners suite: 28 JUnit methods (UT-01..UT-26; UT-01 has two methods, X8 register texts have `registerProblemsFailClosed`), all pass, 0 skipped. `cd backend; ./gradlew codeOwnersTest codeOwnersCoverageVerification`, exit 0, 29 s (`backend/coverage.log`).
- Full regression (TASK-10), run once at tip `ae61b08`: `powershell -NoProfile -File scripts/dev.ps1 test`, exit 0, 157 s (`dev-test.log`). Backend `gradlew test`: 271 tests, 0 failures, 0 errors, 0 skipped (JUnit XML in `backend/build/test-results/test/`, 5 codeowners suites present). Frontend `npm run check`: typecheck, lint, Vitest 28/28; coverage statements 91.89, branches 88.09, functions 82.35, lines 91.66 (all ≥ 80).

## [Superseded, ae61b08] Coverage (native JaCoCo XML `backend/coverage/codeOwnersCoverageReport.xml`; counters in `backend/coverage/counters.txt`; log `backend/coverage.log`)

| Counter | Missed | Covered | % |
|---|---|---|---|
| LINE | 9 | 200 | 95.69 |
| BRANCH | 5 | 113 | 95.76 |
| INSTRUCTION | 41 | 1242 | 96.80 |
| METHOD | 0 | 43 | 100.00 |

## [Superseded, ae61b08] Unit test results table (TASK-08; `unit-tests/report.md` could not be written by this run, so the table is here)

| Surface | Status | Tests | Fail | Skipped | LINE | BRANCH | INSTRUCTION | METHOD | Native report |
|---|---|---|---|---|---|---|---|---|---|
| Backend (codeowners package) | PASS | 28 | 0 | 0 | 95.69 | 95.76 | 96.80 | 100.00 | `backend/coverage/codeOwnersCoverageReport.xml`, `backend/coverage/html/` |
| Frontend | NOT_APPLICABLE | N/A | N/A | N/A | N/A | N/A | N/A | N/A | none: spec "Frontend Changes Required: NO" (`spec.md:25`); no `frontend/` file changed; `npm run check` regression passed in `dev-test.log` |

## Other evidence

`preflight.md` (TASK-00 and the RWB-E1-042 path table), `scope-check.md` (TASK-09), `handoff.md` (TASK-11), `deviations.md` (DEV-01..DEV-07), `document-gaps.md` (IM-DG-01, IM-DG-02), `assumptions.md` (IA-01..IA-05), `shared-updates.md` (IM-SU-01..IM-SU-03). Logs of the earlier unattended run are kept apart in `_superseded-opencode/` and are not evidence.

## Status (superseded by the final tip section above)

```text
IMPLEMENTATION_STATUS: SUCCESS [TASKS: TASK-00..TASK-11] [LOCAL_STATE: BUILT — ACCEPTANCE PENDING HV-01..HV-11]
BACKEND_UNIT_TESTS: PASS [TESTS: 28] [LINE: 95.69] [BRANCH: 95.76] [INSTRUCTION: 96.80] [METHOD: 100.00]
FRONTEND_UNIT_TESTS: NOT_APPLICABLE [REASON: no frontend file changes]
REGRESSION: ./scripts/dev.ps1 test exit 0 at ae61b08
RISK: UT-26 fails once RWB-E1-042 is merged unless the block gains a line for architecture/magic-number-baseline.csv (DEV-01, IM-SU-01)
GATE_REVIEW: PENDING_ORCHESTRATOR
NEXT_STEP: Human review of implementation evidence, then manually start API Tester with RUN_ID=INC-004-epic-1-RWB-TE-002 (API and UI scenarios are NOT_APPLICABLE for this story)
```
