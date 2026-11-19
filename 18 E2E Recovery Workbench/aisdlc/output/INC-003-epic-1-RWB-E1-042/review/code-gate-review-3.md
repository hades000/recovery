# Code gate review, round 3: RWB-E1-042 (RUN_ID `INC-003-epic-1-RWB-E1-042`)

| Field | Value |
|---|---|
| Review ID | `REVIEW-RWB-E1-042-CODE-003` |
| Gate | Code gate, pre-merge, round 3 (re-review after the code-gate fix round 2) |
| Story | RWB-E1-042 Central configuration service and parameter catalog (EPIC-001, recovery P3/P4) |
| Range | `git diff develop-recovery...feature/RWB-E1-042-parameter-catalog` (merge base = `develop-recovery` tip `7bee04d`) |
| Tip | `25c8f94` (`25c8f947a46bc9c391f4697f7e4eec6f5a7467d2`); worktree `rwb-wt/RWB-E1-042` is at that commit, and `git status --short` is empty |
| Round 2 | `review/code-gate-review-2.md` (FAIL 0C/0H/0M/3L at `9056ed2`) |
| Inputs read independently | `git show --stat 216a696 25c8f94`; `git diff 9056ed2 216a696` (test only) and `git diff 9056ed2 25c8f94 -- backend/src/main backend/build.gradle.kts`; `ParameterConfigIT.java` and `ParameterLoadHandlerImpl.java` (`approve`, `approveInTransaction`) at `25c8f94`; native JUnit XML `backend/build/test-results/{test,recoveryIntegrationTest,apiTest}` and native `backend/build/reports/jacoco/recoveryCoverageReport.xml` in the worktree; `implement/code-gate-fix/README.md`, `test-and-coverage-counts.txt`, `shared-updates.md`, every log in `round2/`; `implement/deviations.md`, `implement/review-fix/deviations-review-fix.md`; `implementation-report.md`, `unit-tests/report.md`, `integration/contract-and-migration.md`, `implement/report.md`; `api-tests/report.md`, `api-tests/evidence/apiTest-run5.log`; `specify/spec.md` rev 13 §15 (TC-20, -22, -23); `plan/tests/scenarios.md` v2 |
| Re-runs | None. No Gradle task was run. Every count below was recomputed from the native XML on disk; no claim looked doubtful enough to rerun. |
| Repository | Read only apart from this file. No shared file, evidence log, spec, plan, code or test was edited. |
| Human sign-off | **Not recorded.** AGENTS.md §9 is unavailable in this run (OPEN-016). This review records no approval or acceptance (D-RUN-09). |

## Status

**FAIL** (Low only): 0 Critical, 0 High, 0 Medium, 1 Low. CODE2-002 and CODE2-003 are closed. The
substance of CODE2-001 is also closed: the three container tests exist, assert what the spec requires
and pass at `25c8f94`. One part of the round-2 remediation for CODE2-001 was not done. That is the
renamed-test note for the six scenario-map names that match no test, and it is raised again as
CODE3-001. Every other code-gate check holds at `25c8f94`. The only production change since `9056ed2`
is the deletion of one comment line.

REVIEW_GATE_WARNING: Low-severity review failure does not automatically stop this handoff; unresolved findings may carry downstream. Human disposition required.

## Round-2 findings: verification

| ID | Round-2 severity | Status | How it was verified (files and logs, not the summary) |
|---|---|---|---|
| CODE2-001 | Low | **Closed for the three tests; the rename note is still open (CODE3-001)** | **TC-20.** `ParameterConfigIT#concurrentApprovalsGiveOneApprovedAndOne409` exists under the name in `scenarios.md` row T-E1-042-20. It creates one VALIDATED load, then stubs the `@MockitoSpyBean` `valueRepository.lockByLoadId(loadId)` with a `CountDownLatch(2)`. Each thread counts down and waits up to 20 s for the other, and only then calls the real repository answer. Both approvals are therefore inside their own `REQUIRES_NEW` transaction (`approveInTransaction`, `ParameterLoadHandlerImpl:175-182`) before either takes the `PESSIMISTIC_WRITE` row lock. No sleep decides the order, and if one thread never arrives the test fails. The test asserts 2 outcomes, exactly one `ParameterLoadResult` with status `APPROVED`, exactly one `ApiProblemException` with status 409 and `MSG-GEN-004`, and a final row status of `APPROVED`. Production gives 409 `MSG-GEN-004` on both paths: after the lock, at `:181-182`, and on the unique-index race, at `:167-169`. **TC-22.** `ParameterConfigIT#flagOnLoadsThroughTheAdapter` loads through the test-only `TestBeans.ParameterLoadBranch`, which takes an `ObjectProvider<ParameterLoadHandler>` and throws 404 `MSG-P4-003` when the provider is empty (spec §15 TC-22 (b)). It asserts a non-null `loadId`, status `VALIDATED`, that `handler.find(loadId)` returns the same result, and that the row is `VALIDATED`. `ParameterConfigIT$FlagOff#flagOffStillStartsAndRefusesParameterLoads` asserts that `getIfAvailable()` is null, that the branch throws 404 `MSG-P4-003`, and that the `parameter_value` row count is unchanged. The other TC-22 clauses are still covered by the existing `$FlagOff` tests (`theHandlerAndTheEndpointAreAbsent`, `theReaderStillServesTheDefault`, `theHandlerImplementsNoAccessApiType`). With the flag off, the context starts, which proves that no `casewf.config` bean has a hard dependency on the handler. **TC-23.** `ParameterConfigIT#unknownKeyEmptyFileAndPastValidFrom` asserts three refusals: 422 `MSG-P1-002` for the unknown key; 422 `MSG-GEN-001` with field `file` for the empty file; 422 `MSG-P3-027` with placeholder `table=PARAMETER` for `validFrom` = today − 1. It also asserts that the `parameter_value` count after the three refusals equals the count before them. This matches spec §15 TC-23. **Native XML.** All four test cases are in `TEST-…ParameterConfigIT.xml` and `TEST-…ParameterConfigIT$FlagOff.xml` with no failure. **Attempts.** `round2/it-parameter-config-attempt1.log` and `-attempt2.log` show `concurrentApprovalsGiveOneApprovedAndOne409` FAILED with `AssertionError at ParameterConfigIT.java:658`. That line is the `filteredOn(ParameterLoadResult)` assertion. The README's explanation (a spy NPE inside the test, so both outcomes were exceptions) fits that line, but the NPE text itself is not in the logs, and the test source at the time of those attempts is not kept. `-attempt3.log` is BUILD SUCCESSFUL, and the final assertions are the ones listed above. **Location note.** The flag-off case is in the nested class `ParameterConfigIT$FlagOff`, not directly in `ParameterConfigIT`. The README records this, and it is acceptable for a JUnit `@Nested` class. **Not done:** the renamed-test note that round 2 asked for (CODE3-001). |
| CODE2-002 | Low | **Closed** | `implement/deviations.md` now holds DEV-01..DEV-12 and **DEV-19** (`:22`). `review-fix/deviations-review-fix.md` holds DEV-13..DEV-18 (`:8-13`). No ID appears in both files. Under `implement/`, every reference to the check-12 reorder cites DEV-19: `deviations.md:22,26-30`, `implementation-report.md:81` ("DEV-19, first numbered DEV-13") and `:92`, `code-gate-fix/README.md:13,40,81`, and `code-gate-fix/shared-updates.md:40-41`, which tells the orchestrator to cite DEV-19 and not DEV-13. The only remaining `DEV-13` is the review-fix advisory-lock deviation, which is correct. The gate-impact note (`deviations.md:30-34`) now points at `code-gate-fix/test-and-coverage-counts.txt` and `round2/`. |
| CODE2-003 | Low | **Closed** | `git diff 9056ed2 25c8f94 -- backend/src/main` is a single deleted line in `ParameterLoadHandlerImpl.java`: `/** True when the failure, or any cause under it, is a data-integrity violation. */`. Only the narrowed `isApprovalConflict` Javadoc remains. |

## Findings (this round)

| ID | Severity | Finding | Evidence | Remediation |
|---|---|---|---|---|
| CODE3-001 | Low | **The scenarios map still names six tests that do not exist, and no renamed-test note maps them to the real ones.** Round 2 (CODE2-001, remediation, last sentence) asked for a renamed-test note for TC-04, -10(b), -17, -28, -32 and -44. `code-gate-fix/README.md` marks CODE2-001 **Fixed** but does not address this part. No file under `implement/` maps the six names: a search for "renam" finds only DEV-15 and the DEV-19 renumbering. I checked the native XML (`test`, `recoveryIntegrationTest`, `apiTest`). These six names, cited in `plan/tests/scenarios.md`, appear in no testcase: `ParameterConfigIT#readinessDownNamesKeyAndEnvironment` (T-04), `#rollbackRebuildsOnlyAfterCommit` (T-10(b)), `ParameterLoadHandlerTest#differentContentWhereApprovedExistsIs409` (T-17), `ParameterCacheTest#eventRebuildsTheEntry` (T-28), `ParameterConfigIT#futureSeedNeverFailsReadiness` (T-32) and `CatalogCompletenessCheckTest#credentialRuleAppliesToEveryEnvRow` (T-44). DEV-11 explains the system-level gaps for T-04 and T-32. The other four are renames, so a reader or the Traceability Manager cannot get from TC to test. Each of the six TCs still has at least one other named test that passes. Behaviour is unaffected, so the severity stays Low. | `review/code-gate-review-2.md` CODE2-001 remediation and checklist row 1; `plan/tests/scenarios.md:22,28,35,46,50,62`; native JUnit XML at `25c8f94`; `implement/code-gate-fix/README.md:12` | Add a short rename table to `implement/deviations.md`, or to the traceability rows in `code-gate-fix/shared-updates.md`, that maps each of the six scenario names to the actual `class#method`. One example is TC-10(b) → `ParameterConfigIT#failedRollba…`, as in `implementation-report.md:52`. Cite DEV-11 for the T-04 and T-32 system halves. No code change is needed. |

## Gate checklist (full code gate at `25c8f94`)

| # | Gate | Result | Evidence |
|---|---|---|---|
| 1 | Spec / AC / TC trace | **PASS (CODE3-001)** | TC-20, TC-22 and TC-23 now have their planned system-level tests, under the names in `scenarios.md`. Round-2 row 1 counted 3 missing system-level cases; that count is now 0. The six unmapped renames remain (CODE3-001). Every TC has at least one passing test. TC-E1-042-12 is still **Blocked** and is not reported as passed. |
| 2 | No skipped or weakened test | **PASS** | The `9056ed2..25c8f94` test diff adds 4 test methods and 1 test bean. It removes no assertion and changes no existing assertion (the only other changed line is the class Javadoc TC list). The diff has no `@Disabled`, `@Ignore` or `assumeTrue`. Every suite has 0 skipped tests. |
| 3 | 80 % on all four counters (native) | **PASS** | I recounted from the native JUnit XML. `test`: 44 files, **388** tests, 0 failures, 0 errors, 0 skipped. `recoveryIntegrationTest`: 5 files, **59** tests (`ParameterConfigIT` 33, `$FlagOff` 4, `ParameterMigrationIT` 4, `RecoveryMigrationIT` 12, `RecoveryDatabaseIT` 6), 0/0/0. `apiTest`: **13** (`ParameterApiContractIT` 12 + `$FlagOff` 1), 0/0/0. The XML timestamps (13:21–13:29Z) come after the commit time (20:16 +0700 = 13:16Z). The native JaCoCo report-level counters are INSTRUCTION 14045/15482 = **90.7 %**, BRANCH 1289/1594 = **80.9 %**, LINE 2579/2833 = **91.0 %**, METHOD 552/576 = **95.8 %**. The native report and `round2/recoveryCoverageReport.xml` both have SHA-256 `8372e94b…d992738dd`. Line 1 of `round2/clean.log`, `dev-test.log`, `coverage-verification.log` and `it-full.log` is `TIP=25c8f947…7467d2`, and each log has `EXITCODE=0` and BUILD SUCCESSFUL. Line 1 of `apiTest-run5.log` names tip `25c8f94`, and the log has `EXITCODE=0`. These figures equal `test-and-coverage-counts.txt`, `implementation-report.md:11,99,101`, `unit-tests/report.md:6-23`, `integration/contract-and-migration.md:5-11` and `api-tests/report.md:26`. Superseded figures are labelled as superseded. Frontend is `NOT_APPLICABLE`: `git diff --name-status develop-recovery...feature/RWB-E1-042-parameter-catalog -- frontend api` is empty. |
| 4 | Rules as data (AGENTS §3.2, §4.8) | **PASS** | The round adds no main-code literal; the only main change is a comment deletion. The new literals (`MSG-*` IDs, synthetic CSV rows) are test assertions and fixtures. |
| 5 | No personal data, no secret value | **PASS** | A scan of the added test lines for emails, 10–13-digit runs, `password`, `secret` and `token` found nothing. The tests use the existing synthetic `AUTHOR` and `APPROVER` IDs and synthetic parameter rows. No log line was added. |
| 6 | No direct ACE `public` read | **PASS** | No change. The new tests read only `parameter_value` through the recovery-schema `JdbcTemplate`. |
| 7 | Migration naming and one migration | **PASS** | At `25c8f94`, the folder holds `README.md` and one migration, `V0001__rwb_e1_042_parameter_catalog_and_seed.sql`, whose line 1 is `-- Story: RWB-E1-042`. The migration did not change in `9056ed2..25c8f94` (`git diff --stat` on `backend/src/main/resources` is empty). D-RCV-28 / D-RUN-07: the orchestrator renumbers at merge if needed. |
| 8 | Migration seed rows | **PASS (unchanged)** | The migration and the catalog CSV are unchanged since round 1, so round-1 row 8 stands. |
| 9 | `@PreAuthorize` on every endpoint | **PASS (unchanged)** | No endpoint was added or changed. |
| 10 | Flag-off contract (SPEC-021) | **PASS** | It is now proven at container level in both directions (CODE2-001 above). `ParameterLoadBranch` is test-only (`TestBeans` in `src/test`) and is not a production P4 SPI bean, which is consistent with D-RUN-10/-20. DEV-17 (the GET 404 body is not asserted, because E43S owns that body) remains accurate. |
| 11 | Module boundaries (D-RUN-18..21) | **PASS** | No main-code type, import or bean changed in `216a696` or `25c8f94`. The test adapter lives in the `casewf.config` test package and reaches the handler only through the published `ParameterLoadHandler` interface. Round-2 row 11 stands. |
| 12 | No new dependency | **PASS** | `backend/build.gradle.kts` did not change in `9056ed2..25c8f94`. Across the full range from `develop-recovery`, the diff adds or removes no `implementation`, `api`, `testImplementation`, `runtimeOnly`, `compileOnly` or plugin line. The new test code uses only JDK, Mockito, AssertJ and Spring classes that are already on the classpath. |
| 13 | Plan file scope and deviations | **PASS (CODE3-001)** | `216a696` changes only `ParameterConfigIT.java`. `25c8f94` changes `ParameterLoadHandlerImpl.java` (−1 comment line) and adds `aisdlc/output/INC-003-epic-1-RWB-E1-042/review/ponytail-review.md` and `security-review.md`. Each of these two files has the same SHA-256 on the branch as the main-repo `review/` copy (`08e99bbf…b000601d`, `5944a645…ac12fd61`). The deviation IDs are unique (CODE2-002). No shared file was edited. |
| 14 | Production behaviour unchanged since `9056ed2` | **PASS** | `git diff 9056ed2 25c8f94 -- backend/src/main backend/build.gradle.kts` is the single comment deletion and nothing else. The unit and coverage counters are identical to the `9056ed2` set, which is consistent with that. |
| 15 | `DG-E042-*` gaps | **PASS** | No change. The fix round adds no gap. |
| 16 | API Tester stage | **PASS (for information)** | `api-tests/report.md` run5 at `25c8f94`: 13/13, exit 0. The native `apiTest` XML gives the same 13. |
| 17 | AGENTS.md §9 human sign-off | **NOT RECORDED** | OPEN-016. No named human reviewer approval is available or claimed. |

## Candidate document gaps

| Candidate | Document (name, version, section) | Gap | Blocker | Reason |
|---|---|---|---|---|
| None new | — | This round changes tests and evidence only. The TC-20, -22 and -23 tests follow spec rev 13 §15 as written. CODE3-001 is an inconsistency inside the run's own artefacts, not a document-set gap. | No | No document in the set is silent or contradictory on these points. |

## Verdict

The three container tests that round 2 found missing now exist under their planned names. They
assert what the spec requires: a deterministic latched race with one APPROVED and one 409
`MSG-GEN-004`, the PARAMETER-branch adapter refusing with 404 `MSG-P4-003` when the flag is off and
delegating when it is on, and three 422 refusals with no rows written. All of them pass in the
native XML at `25c8f94`. The deviation IDs are unique, and the stale Javadoc is gone. The figures of
record (388 unit, 59 IT, 13 API; LINE 91.0, INSTRUCTION 90.7, BRANCH 80.9, METHOD 95.8) equal the
native JUnit and JaCoCo output, and each log names tip `25c8f94`. No production behaviour changed,
and the migration, rules-as-data, personal-data, boundary and dependency checks still hold. One Low
remains: the renamed-test note that round 2 asked for. It does not block the merge, but it needs a
human disposition. This review records no approval or acceptance.

CODE_GATE: FAIL [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 1]
