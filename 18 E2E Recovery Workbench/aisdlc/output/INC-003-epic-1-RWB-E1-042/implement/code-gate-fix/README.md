# Code-gate fix round — RWB-E1-042

Run `INC-003-epic-1-RWB-E1-042` · round 1 answers `review/code-gate-review.md` (FAIL 0C/1H/0M/2L at
`74e4ccb`); round 2 answers `review/code-gate-review-2.md` (FAIL 0C/0H/0M/3L at `9056ed2`).
Final tip: **`25c8f94`** (`25c8f947a46bc9c391f4697f7e4eec6f5a7467d2`) on
`feature/RWB-E1-042-parameter-catalog`. Not merged, not pushed.

## Round 2 (tip `25c8f94`, logs in `round2/`)

| ID | Status | What was done | Evidence |
|---|---|---|---|
| CODE2-001 (Low) | **Fixed** in `216a696` | The three container-level cases that TASK-20 requires, named as `plan/tests/scenarios.md` names them. TC-20: two threads approve one load, a `CountDownLatch` holds both inside `lockByLoadId` until both have arrived (no sleep), one gets `APPROVED` and the other 409 `MSG-GEN-004`, and the rows end `APPROVED`. TC-23: unknown key (422 `MSG-P1-002`), empty file (422 `MSG-GEN-001`, field `file`) and a past `validFrom` (422 `MSG-P3-027`), with the `parameter_value` row count unchanged. TC-22: a test-only `ParameterLoadBranch` adapter takes `ObjectProvider<ParameterLoadHandler>`; flag on, it delegates and the `loadId` is the handler's; flag off, it throws 404 `MSG-P4-003` and nothing is written. No production code changed. | `ParameterConfigIT#concurrentApprovalsGiveOneApprovedAndOne409`, `#unknownKeyEmptyFileAndPastValidFrom`, `#flagOnLoadsThroughTheAdapter`, `ParameterConfigIT$FlagOff#flagOffStillStartsAndRefusesParameterLoads`. What the saved logs show: `round2/it-parameter-config-attempt1.log` ends `BUILD FAILED` with `ParameterConfigIT > concurrentApprovalsGiveOneApprovedAndOne409() FAILED`, `java.lang.AssertionError at ParameterConfigIT.java:658` (37 tests completed, 1 failed); `-attempt2.log` ends `BUILD FAILED` with the same test and an `AssertionError` at line 659; `-attempt3.log` ends `BUILD SUCCESSFUL`. The logs do not show the cause. The test as committed is in `216a696`, and `round2/it-full.log` is the full suite at the final tip. |
| CODE2-002 (Low) | **Fixed** | The code-gate deviation is renumbered **DEV-19** in `../deviations.md` (DEV-13..DEV-18 stay in `../review-fix/deviations-review-fix.md`). The gate-impact note now points at `test-and-coverage-counts.txt` and `round2/`. | `../deviations.md` |
| CODE2-003 (Low) | **Fixed** in `25c8f94` | The stale one-line Javadoc above `isApprovalConflict` is deleted. The final `ponytail-review.md` and `security-review.md` are tracked in the worktree in the same commit. | `git show 25c8f94` |

### Code-gate round 3 (documentation only; no code, test, plan or run log changed)

| ID | Status | What was done | Evidence |
|---|---|---|---|
| CODE3-001 (Low) | **Fixed** as **DEV-20** | Six test names in `plan/tests/scenarios.md` (T-E1-042-04, -10(b), -17, -28, -32, -44) match no test. Each name was checked against the native JUnit XML at `25c8f94` (all six absent), and the test that covers the case was found by reading what it asserts. `DEV-20` in `../deviations.md` holds the table: planned name, the test that ran, and the result file. T-32 has no container-level case of that name (unit test plus the DEV-11 / DEV-16 readiness pair), and T-17's match is `aDifferentLoadStillMeetsTheApprovedFromCheck`, not `conflictingContentIs409` (that one asserts `MSG-GEN-004`). The plan itself is not edited. | `../deviations.md` DEV-20 and its table |

### Final figures at `25c8f94` (the one set of record)

| Item | Result | Log |
|---|---|---|
| `gradlew clean`, then `scripts/dev.ps1 test` | exit 0; Gradle `test` 44 classes, **388** tests, 0 failures, 0 skipped | `round2/clean.log`, `round2/dev-test.log` |
| `gradlew recoveryCoverageVerification` | exit 0 (one BUNDLE rule, 0.80 on four counters) | `round2/coverage-verification.log` |
| JaCoCo LINE | 2579/2833 = **91.0 %** | `round2/recoveryCoverageReport.xml` (same SHA-256 as the native report) |
| JaCoCo INSTRUCTION | 14045/15482 = **90.7 %** | same |
| JaCoCo BRANCH | 1289/1594 = **80.9 %** | same |
| JaCoCo METHOD | 552/576 = **95.8 %** | same |
| `gradlew recoveryIntegrationTest` | exit 0; 5 classes, **59** tests, 0 failures, 0 skipped: `ParameterConfigIT` 33 + `$FlagOff` 4, `ParameterMigrationIT` 4, `RecoveryMigrationIT` 12, `RecoveryDatabaseIT` 6 | `round2/it-full.log` |
| API contract suite (`apiTest`, run5) | exit 0; 13 tests (12 + `$FlagOff` 1), 0 failures | `../../api-tests/evidence/apiTest-run5.log` |
| Counts derived from the native XML | — | `test-and-coverage-counts.txt` |

The unit and coverage numbers equal the `9056ed2` numbers: round 2 adds container tests and deletes one
comment line, so no executable main code changed. The section below is round 1 and is **superseded**
where it differs (55 container tests at `9056ed2`).

## Round 1 (tip `9056ed2`)

## Findings

| ID | Status | What was done | Evidence |
|---|---|---|---|
| CODE-001 (High) | **Fixed** in `9056ed2` | Check 11 (identical repeat) runs before check 12 (`countApprovedFrom`) inside the locked load transaction; check 12 moved to `ParameterLoadValidator#validateApprovalWindow`, called by the handler after the repeat lookup (DEV-19; first numbered DEV-13, renumbered in round 2). | `ParameterConfigIT#anApprovedLoadRepeatsInsteadOfBeingRefused` (approve, re-submit, same `loadId`, `repeat=true`, `APPROVED`, still one row); `ParameterLoadHandlerTest#anApprovedLoadRepeatsBeforeTheApprovedFromCheck`; check 12 still refuses a different load: `ParameterLoadHandlerTest#aDifferentLoadStillMeetsTheApprovedFromCheck`, `ParameterLoadValidatorTest#anApprovedVersionOnOrAfterTheDateIsARefusal409`, `ParameterConfigIT#conflictingContentIsRefused`. Red: `red-ParameterLoadHandlerTest.log` (call removed → `aDifferentLoadStillMeetsTheApprovedFromCheck` fails, 19 run, 1 failed). The approved-repeat tests are red on `74e4ccb` by construction: there check 12 ran inside `validate`, before the repeat lookup, and answered 409. |
| CODE-002 (Low) | **Fixed** (evidence copy) | The final `ponytail-review.md` and `security-review.md` were copied unchanged (SHA-256 identical) from the worktree's `aisdlc/output/INC-003-epic-1-RWB-E1-042/review/` into `review/`; the older copies are kept as `review/ponytail-review.round1.md` and `review/security-review.round1.md`. | See the verdict table below. |
| CODE-003 (Low) | **Fixed** | Unit, coverage, verification and the whole recovery IT suite re-run at `9056ed2`; `implementation-report.md`, `unit-tests/report.md` and `integration/contract-and-migration.md` now carry the one set of figures below; older figures are marked superseded. | Logs in this folder. |

## Which commit each review verdict refers to

| File | Section | Commit reviewed | Verdict as written |
|---|---|---|---|
| `review/security-review.md` | first review | `1ffb659` | `PASS_WITH_LOW_FINDINGS` (SEC-042-01..04, all Low) |
| `review/security-review.md` | "Fix round 1 verification" | `8e51eb8` (prior tip `1ffb659`) | **PASS** — 4/4 closed, 0/0/0/0 open |
| `review/ponytail-review.md` | first review | `1ffb659` | "fix 1 before merge; then 2 and 3" |
| `review/ponytail-review.md` | second section | `8e51eb8` (prior tip `1ffb659`) | not ship yet: fix 10; 11, 12 same round |
| `review/ponytail-review.md` | last section | `74e4ccb` (prior tip `8e51eb8`) | **Ship** |
| `review/code-gate-review.md` | — | `74e4ccb` | FAIL 0C/1H/0M/2L |

No review on disk covers `9056ed2` (this round's CODE-001 change). The security verdict's last
commit is `8e51eb8`; `74e4ccb` and `9056ed2` were not security-reviewed. The orchestrator's code-gate
re-run is the review of `9056ed2`.

## Figures at `9056ed2` (round 1; superseded by the `25c8f94` set above)

| Item | Result | Log |
|---|---|---|
| `./scripts/dev.ps1 test` (after `gradlew clean`) | exit 0; Gradle `test` 388 tests, 0 failures, 0 skipped; `npm run check` 28 tests, statements 91.89 % | `dev-test.log`, `clean.log` |
| `./gradlew recoveryCoverageVerification` | exit 0 (one BUNDLE rule, 0.80 on four counters) | `coverage-verification.log` |
| JaCoCo LINE | 2579/2833 = **91.0 %** | `recoveryCoverageReport.xml` (copy of the native report) |
| JaCoCo INSTRUCTION | 14045/15482 = **90.7 %** | same |
| JaCoCo BRANCH | 1289/1594 = **80.9 %** | same |
| JaCoCo METHOD | 552/576 = **95.8 %** | same |
| `./gradlew recoveryIntegrationTest` | exit 0; 55 tests, 0 failures, 0 skipped: `ParameterConfigIT` 30 + `$FlagOff` 3, `ParameterMigrationIT` 4, `RecoveryMigrationIT` 12, `RecoveryDatabaseIT` 6 | `it-full.log` |
| Counts derived from the native XML | — | `test-and-coverage-counts.txt` |

`it-full.log` carries Hikari "connection refused / connection closed" WARN lines at context shutdown,
after the Testcontainers database stops; they are teardown noise, not test failures (exit 0, 0 failures).

`it-parameter-config.log` (18:55) is from the interrupted earlier session, run on the uncommitted tree
for `ParameterConfigIT` only. It is superseded by `it-full.log`.

## Other files

- `shared-updates.md` — rows for the orchestrator (traceability, RWB-E1-043 note).
- `../deviations.md` — DEV-19 added (first numbered DEV-13, renumbered in round 2, CODE2-002).
