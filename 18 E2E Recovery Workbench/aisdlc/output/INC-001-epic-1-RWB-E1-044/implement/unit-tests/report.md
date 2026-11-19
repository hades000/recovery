# Unit test evidence: RWB-E1-044

Run: `INC-001-epic-1-RWB-E1-044`. Commands run from `backend/` (worktree
`C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\rwb-wt\RWB-E1-044`) with
`$env:JAVA_TOOL_OPTIONS="-Djdk.net.unixdomain.tmpdir=$env:USERPROFILE\.gradle\uds"` and
`GRADLE_OPTS=-Xmx512m` (RUN-BRIEF).

## Commands and results (code-gate fix, final)

| Surface | Command | Working directory | Exit | Tests | Time |
|---|---|---|---|---|---|
| Backend unit + coverage gate | `./gradlew test recoveryCoverageVerification` | `backend/` | 0 | 243 passed, 0 failed, 0 skipped, 27 classes | 3m 00s |
| Backend container (separate, not a unit surface) | `./gradlew recoveryIntegrationTest` | `backend/` | 0 | 18 passed (12 `RecoveryMigrationIT` + 6 `RecoveryDatabaseIT`), 0 failed, 0 skipped | 2m 15s |

Final evidence: `implement/code-gate-fix/unit-coverage.log` and `unit-coverage` counters below.
The pre-code-gate-fix round-5 snapshot (242 tests) is cited in `implement/review-fix/round5/`
(`unit-coverage.log`, `counters.txt`, `recoveryCoverageReport.xml`): LINE 94.86, INSTRUCTION 94.28,
BRANCH 86.26, METHOD 97.98. The first-round snapshot (226 tests, 94.57 / 93.99 / 86.51 / 97.68) in
`implement/backend/coverage/` is **pre-fix** and is kept only as history.

## Coverage scope

`recoveryCoverageReport` / `recoveryCoverageVerification` measure one combined `BUNDLE`:
every main class under `th/co/scb/ace/demo/recovery/**` (untested classes included), RWB-TE-001's
boundary tooling, and this story's `architecture/migration/**` test-output classes. The two tooling
directories exclude `*Test` and `*IT` classes only (RWB-TE-001 SPEC-020 (b); SPEC-014 case 1). No
main class is excluded and no threshold is lowered. Execution data is the `test` task only; the
container suite does not contribute coverage.

| Metric | Covered | Missed | Ratio | Required | Result |
|---|---|---|---|---|---|
| INSTRUCTION (statements) | 7091 | 432 | 0.9426 | 0.80 | PASS |
| BRANCH | 630 | 102 | 0.8607 | 0.80 | PASS |
| LINE | 1333 | 73 | 0.9481 | 0.80 | PASS |
| METHOD (functions) | 339 | 7 | 0.9798 | 0.80 | PASS |

## Required results table

| Surface | Passed | Failed | Skipped | Statements % | Branches % | Functions % | Lines % | Required % | Status | Evidence |
|---------|--------|--------|---------|--------------|------------|-------------|---------|------------|--------|----------|
| Backend (main + test-scope tooling, one combined bundle) | 243 | 0 | 0 | 94.26 | 86.07 | 97.98 | 94.81 | 80 | PASS | `implement/code-gate-fix/unit-coverage.log`, coverage XML from the same run; round-5 snapshot cited in `implement/review-fix/round5/` |
| Frontend | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | NOT_APPLICABLE | UI In Scope NO; `DESIGN_EVIDENCE_STATUS: NOT_REQUIRED`; story v7 §15 "No new screen in this story"; no file under `frontend/` changes (`plan.md` Frontend Plan; `plan/contracts/frontend-integrations.json`). `npm run check` still ran in the merge gate and passed (28 Vitest tests) |

## Failures and notes

- No unit test failed and none is skipped.
- The 7 uncovered methods are record accessors and one branch of the runner/reader; all four
  counters are above the gate. No exclusion was added to reach this result.
- The one code-gate test added after round 5 (`LiteralSchemaRuleTest`) is a `*Test` class and is
  excluded from the coverage bundle by the existing tooling filter.
- The container suite is reported separately: it fails (not skips) without Docker and does not
  replace unit coverage.
