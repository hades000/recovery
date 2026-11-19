# REVIEW-001 implement: post-merge review remediation

RUN_ID `REVIEW-001-first-four-stories`, stage `implement`. Branch `fix/REVIEW-001-post-merge-review`, created
from `develop-recovery` 27567ed. The task list is the "Fixed in this run" section of `../plan.md`; the findings
are in `../code-quality-review.md`. The two CONF-TE001 items come from
`../../INC-002-epic-1-RWB-TE-001/review/code-gate-review-confirmation.md` §7 and were added by the orchestrator.
"Registered" rows (M2, M3, M7, M8, L4-L8, L10, L11) were not touched.

## Results

| Finding | Commits | Test that proves it | Result |
|---|---|---|---|
| H1 concurrent approve/rollback of one key | red `5c8329d`, green `a6a6dd1` | `ParameterConfigIT#concurrentApprovalsOfTwoLoadsForOneKeyAreSerialised`, `#rollbackRacingAnApprovalOfTheSameKeyIsSerialised` (red-H1.txt, green-H1.txt) | Fixed |
| H2 silent DEV default for the environment | red `9b46cc7`, green `6453715` | `PlatformInfoControllerTest#aMissingEnvironmentFailsAtStartup`, `#anEnvironmentOutsideTheListFailsAtStartup` (red-H2.txt, green-H2.txt) | Fixed; local `.env` needs `RWB_ENVIRONMENT=DEV` (D-04) |
| H3 coverage verification not in CI | `b3a5073` | `.gitlab-ci.yml` `backend-unit` runs `test recoveryCoverageVerification`; final-test.log | Fixed |
| H4 unowned paths | `bfab086` | `OwnershipResolverTest#addendumPathsHaveOwners`, `CodeOwnersValidationTest#liveFileAndRegisterPass` | Fixed; ratification at MR (SU-03) |
| M1 database ITs not triggered by casewf Java | `caf6ee4` | `.gitlab-ci.yml` `backend-recovery-it` `rules.changes` | Fixed |
| M4 rollback event with no listener | `6127b75` | `ParameterLoadHandlerTest#rollbackRecordsTheDecision` (no event), `ParameterConfigIT#failedRollbackCommitLeavesTheRowsApproved` (hook moved, D-06) | Fixed |
| M5 rollback writes no decision record | red `370272b`, green `8801633` | `ParameterLoadHandlerTest#rollbackRecordsTheDecision`, `#rollbackRecorderFailureIs503` (red-M5.txt, green-M5.txt) | Fixed; decision code is an assumption (D-10) |
| M6 outage reported as missing keys, WARN per probe | red `66936a3`, green `131d17c` | `ParameterStartupCheckTest#aDatabaseOutageIsReportedAsUnavailable`, `#theSameStateIsLoggedOnce` (red-M6.txt, green-M6.txt) | Fixed |
| M9 recursion test cannot fail | `637fc4c` | `ParameterCacheTest#theTtlReadDoesNotRecurse`; mutation evidence in red-M9.txt | Fixed (test-only, D-08) |
| M10 grants comment understates the migrator's access | `7481d15` | Comment only; risk to OPEN-051 (SU-01) | Fixed |
| M11 e2e `page.goto` hides a callback bug | `a0bd791` | `frontend/src/auth/AuthCallback.test.tsx` (red against the old code: red-M11.txt) | Root cause fixed; Playwright not run (D-09) |
| L1 dead or speculative code | `6d6f509` | `ParameterServiceTest` (overload and PRODUCT still covered) | Partly fixed by design (D-02) |
| L2 defensive code for impossible cases | `0f34b34` | `ParameterLoadHandlerTest`, `ParameterStartupCheckTest` | Fixed |
| L3 Javadoc says "configured time zone" | `02c15de` | Javadoc only | Fixed |
| L9 generator uses untrimmed cells | `5679889` | `ParameterKeysGenerationTest`; generated `ParameterKeys.java` is byte-identical | Fixed |
| CONF-TE001-01 duplicate `published` entry accepted | red `1a44389`, green `61aefc3` | `ModuleMapLoaderTest#duplicatePublishedIsRejected` (red-CONF-TE001-01.txt, green-CONF-TE001-01.txt) | Fixed (published lists only, D-11) |
| CONF-TE001-02 comment and A-4 overstate the test | `8701e7d` | Comment in `RecoveryBoundaryTest` and append-only note in INC-002 `plan/plan-addendum.md` A-4 | Fixed |

## Code gate remediation (`../review/code-gate-review.md`, CG-R001-01 to -05)

| Finding | Commits | Test that proves it | Result |
|---|---|---|---|
| CG-R001-01 (M) rollback recorded as an approval | red `e84b99a`, green `8228d77` | `ParameterLoadHandlerTest#theDecisionRecordNamesTheOutcome`, `#rollbackRecordsTheDecision` (red-CG-R001-01.txt) | Fixed; the record carries `APPROVED` or `ROLLED_BACK` (D-10); the rollback code stays SU-02 |
| CG-R001-02 (L) lock order by string, lock taken on the hash | red `d10418e`, green `35dbf80`, test fixture `270bf50` | `ParameterConfigIT#keyEnvironmentLocksAreTakenInAscendingLockKeyOrder` (red-CG-R001-02.txt); H1 ITs and TC-20 keep their assertions (TC-20's latch is on the renamed lock-key query). Test fixture moved 300 days ahead in `270bf50`, see D-01 | Fixed; locks taken in ascending `hashtext` order; D-01 and the Javadoc corrected |
| CG-R001-03 (L) IT job not run when only an IT changes | `2ed89d5` | `.gitlab-ci.yml` `backend-recovery-it` `rules.changes` | Fixed |
| CG-R001-04 (L) boundary comment counts six packages | `b0e397d` | Comment only (`RecoveryBoundaryTest`) | Fixed |
| CG-R001-05 (L) M11 has no red commit | evidence commit | `deviations.md` D-15 | Recorded |
| CG2-R001-01 (L, gate round 2) `advisoryLock(String)` Javadoc still claimed the H1 lock | `976691b` | Comment only; D-01 rename sentence corrected; `cleanTest test`: 431 tests, 0 failed, 0 skipped | Fixed |

## Final runs (worktree, after the code gate remediation; code tip `270bf50`)

| Run | Log | Result |
|---|---|---|
| `.\gradlew.bat cleanTest test recoveryCoverageVerification` | `final-test.log` | 431 tests, 0 failed, 0 skipped. Coverage LINE 92.10%, INSTRUCTION 91.69%, BRANCH 81.47% (80.9% at the E1-042 merge), METHOD 96.53%; all at or above 80%, verification passed |
| `.\gradlew.bat cleanRecoveryIntegrationTest recoveryIntegrationTest` (Testcontainers PostgreSQL 16) | `final-it.log` | 62 tests, 0 failed (ParameterConfigIT 36 + FlagOff 4, RecoveryDatabaseIT 6, ParameterMigrationIT 4, RecoveryMigrationIT 12) |
| `npm run check` (frontend), not re-run: no frontend change since | `frontend-check.log` | typecheck and lint clean; 4 files, 29 tests passed; coverage of `src/modules/recovery/**`: statements 91.89%, branches 88.09%, functions 82.35%, lines 91.66% |
| `codeOwnersTest codeOwnersCoverageVerification` (H4) | in the H4 commit run | Passed |

Not run: Playwright (`frontend/e2e`) and `scripts/dev.ps1 up/backend/e2e`, which the brief forbids. The orchestrator
runs Playwright after merge.

## Files

- `deviations.md`: deviations D-01 to D-15, the M11 root cause, assumptions A-01 to A-04.
- `shared-updates.md`: proposed text for open-items (including proposed open items), Traceability_Matrix, build log, INDEX and AGENTS §11.
- `red-*.txt` / `green-*.txt`: test-first evidence for each pair (Hikari shutdown noise removed).
