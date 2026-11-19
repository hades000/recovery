---
title: "Unit test evidence — RWB-TE-001"
run_id: "INC-002-epic-1-RWB-TE-001"
story: "RWB-TE-001"
---

# Unit test evidence

## Remediation verification on 2026-11-10

Story-owner comment 1783131 approved the fallback-only BND-4 diagnostic deviation.
The regression assertion failed before the fix and passed afterward. Full backend compilation,
Checkstyle, tests, and all four unchanged coverage thresholds passed.
See [approval, file scope, commands, durations, and bounded review](../remediation-034.md).

| Surface | Passed | Failed | Skipped | Statements % | Branches % | Functions % | Lines % | Required % | Status | Evidence |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| Backend | 740 | 0 | 274 | 96.12% (1488/1548) | 88.82% (151/170) | 100.00% (63/63) | 96.26% (309/321) | 80% | PASS | [Full verification log](./backend/remediation-034/full-verification.log), [JaCoCo XML](./backend/remediation-034/recoveryCoverageReport.xml), [JUnit XML](./backend/remediation-034/test-results/) |
| Frontend | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | NOT_APPLICABLE | Unchanged in this fallback diagnostic remediation; original implementation evidence below |

The backend scope and exclusions are unchanged from the approved original implementation.
Instructions represent statements; methods represent functions. The 274 skipped cases remain the
existing excluded `@e2e` Cucumber scenarios. Prior evidence below is retained, not overwritten.

## Results

| Surface | Passed | Failed | Skipped | Statements % | Branches % | Functions % | Lines % | Required % | Status | Evidence |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| Backend | 738 | 0 | 274 | 95.97% (1478/1540) | 87.95% (146/166) | 100.00% (63/63) | 95.94% (307/320) | 80% | PASS | [Full check output](./backend/verification-rerun-1.log), [rerun output](./backend/verification-rerun-2.log), [JaCoCo XML](./backend/recoveryCoverageReport.xml), [JUnit XML results](./backend/test-results/) |
| Frontend | 2 | 0 | 0 | 100% (0/0) | 100% (0/0) | 100% (0/0) | 100% (0/0) | 80% | PASS | [Final frontend check](./frontend/check-final.log), [coverage summary](./frontend/coverage-summary.json), [LCOV](./frontend/lcov.info) |

The frontend percentages are reproduced exactly as printed by Vitest. The Recovery placeholder
contains no measurable statements, so the native report records 0/0 for each metric. The approved
plan explicitly accepts this result for this increment.

## Backend execution

Working directory: `ace-monorepo/backend`.

| Command | Exit | Duration | Result |
|---|---:|---:|---|
| `DISABLE_SCB_REPO=1 ./gradlew checkstyleMain checkstyleTest test recoveryCoverageReport recoveryCoverageVerification --rerun-tasks` | 0 | 2m 21s | Checkstyle, full test suite, JaCoCo report, and all four 80% thresholds passed |
| `DISABLE_SCB_REPO=1 ./gradlew test --rerun-tasks` | 0 | 2m 8s | Full suite rerun passed |

JaCoCo scope is the approved Recovery production package tree plus the test-scope
`th.co.scb.ace.demo.recovery.architecture` tooling. Test classes and external synthetic fixtures are
excluded. The report uses JaCoCo instructions for statements and methods for functions. The 274
skipped cases belong to `RunCucumberWebTest`; Gradle excludes its `@e2e` tag from the unit-test task.
All Recovery boundary, loader, map, Modulith fixture, and existing `ModulithTest` results are included
in the saved JUnit XML.

The recovery coverage tasks are available but remain opt-in. `./gradlew check --dry-run` did not
include either recovery coverage task. The Recovery module map was also absent from the boot JAR.

## Frontend execution

Working directory: `ace-monorepo/frontend`.

| Command | Exit | Duration | Result |
|---|---:|---:|---|
| `DISABLE_SCB_REPO=1 npx nx run frontend:check --skip-nx-cache --outputStyle=static` | 0 | 3.9s Nx duration | Build, formatting, lint, Vitest, and dependent targets passed after a clean root install |
| `npx vitest run src/modules/recovery/__tests__/importBoundary.test.ts` with the Recovery ESLint block temporarily removed | 1, expected | 1.26s | The forbidden-import test failed with zero violations while the allow-list test passed; the block was restored |
| `npx nx show project frontend --json` | 0 | n/a | One `test` target uses `vitest run --coverage`; `check.dependsOn` includes `test` |

The final Vitest run passed 2 tests. The coverage output contains only `coverage-summary.json` and
`lcov.info`; no HTML or JavaScript coverage artifacts were generated. No fixture paths appeared in
the production build output.

After the clean `npm ci`, the first check attempt hit Vitest's default 5-second timeout while running
the ESLint integration test under Nx concurrency. `vitest.config.ts` now sets a 15-second test
timeout. The check passed on rerun; the first attempt is preserved in
[the timeout log](./frontend/check-after-clean-install-timeout.log).

## Additional validation notes

- `npm ci` from `ace-monorepo/` passed in 191 seconds. npm reported 25 dependency audit findings; no
  audit remediation was in scope.
- `frontend:typecheck` is configured as a successful `echo` target because the project references
  use `noEmit`; it does not run TypeScript. A direct `npx tsc --noEmit --project tsconfig.app.json`
  exited 2 with five TS2554 errors in the unchanged `src/components/DateInput.tsx` at lines 39, 41,
  51, 53, and 72. These baseline errors are not caused by this increment and were not changed.
- Frontend lint and Vite emitted existing warnings in `ActionCodePicker.tsx`, `ApprovalDocStep.tsx`,
  the Vite config, and bundle-size reporting. The check had no lint errors and the production build
  succeeded.

## Evidence files

- Backend command output: `backend/verification-rerun-1.log` and `backend/verification-rerun-2.log`.
- Backend native coverage and test results: `backend/recoveryCoverageReport.xml` and
  `backend/test-results/`.
- Frontend command output, including the mutation result: `frontend/check-final.log`,
  `frontend/check-2.log`, `frontend/check-3.log`, and `frontend/mutation-check.log`.
- Frontend native coverage: `frontend/coverage-summary.json` and `frontend/lcov.info`.
- Clean-install output and the direct TypeScript diagnostic: `frontend/npm-ci.log` and
  `frontend/typecheck-direct.log`.
