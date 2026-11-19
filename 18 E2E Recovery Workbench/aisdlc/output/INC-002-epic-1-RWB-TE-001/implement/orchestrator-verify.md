# Orchestrator verification: RWB-TE-001 pre-merge

Branch `feature/RWB-TE-001-module-boundary`, tip `55f1ed4` (content of `90550d3` plus the code-gate
fixes). Worktree `rwb-wt/RWB-TE-001`. All commands below were run by the orchestrator (Claude Code),
not taken from the builder's report.

| # | Command | Result | Evidence |
|---|---|---|---|
| 1 | `backend> ./gradlew cleanTest test recoveryCoverageVerification` | exit 0, BUILD SUCCESSFUL in 2m 57s, tests re-executed (not UP-TO-DATE) | `orchestrator-verify-unit.log` |
| 2 | JaCoCo bundle counters after run 1 | LINE 693/711 = 97.47%; INSTRUCTION 3661/3762 = 97.32%; BRANCH 244/256 = 95.31%; METHOD 188/192 = 97.92% | `recoveryCoverageReport.xml` in the worktree build |
| 3 | `backend> ./gradlew recoveryIntegrationTest` | exit 0, BUILD SUCCESSFUL in 1m 14s, `RecoveryDatabaseIT` 6/6 | `orchestrator-verify-it.log` |
| 4 | Main stack `./scripts/dev.ps1 up`; worktree backend `bootRun` on :8080 | Started; `/api/recovery/v1/platform/info` returned 401 without a token (endpoint secured) | `backend/e2e-backend.log` |
| 5 | `backend> ./gradlew --no-daemon e2eTest` | exit 0, BUILD SUCCESSFUL in 52s; `PlatformE2ETest` 6 tests, 0 failures | `backend/e2e.log`, `backend/build/test-results/e2eTest` |
| 6 | `./scripts/dev.ps1 test` at the final tip | exit 0; backend BUILD SUCCESSFUL in 4m 11s; frontend 28/28; coverage statements 91.89%, branches 88.09%, functions 82.35%, lines 91.66% | `backend/task17-final-devps-test.log` |

Notes:

- The `bootRun` Gradle task ends with a non-zero exit when the app is stopped after e2e. That is the
  stop signal, not a test failure; the e2e task itself is run 5 and exited 0.
- The machine was under memory pressure; `GRADLE_OPTS` and `JAVA_TOOL_OPTIONS` were bounded for these
  runs (`-Xmx512m` / `-Xmx768m`). This is a workstation condition, not a repository change.
- `backend/gradlew.bat` disappeared from the worktree between runs (DEV-02 again). It is tracked and
  was restored with `git checkout -- backend/gradlew.bat` before each run; no commit deletes it.
- CODE-001 and CODE-007 are closed by runs 5 and 6. CODE-003/005/006 are closed by the builder's
  commit `55f1ed4` and `plan/plan-addendum.md`. CODE-002/004/008 are recorded in the addendum and
  the merge message.
