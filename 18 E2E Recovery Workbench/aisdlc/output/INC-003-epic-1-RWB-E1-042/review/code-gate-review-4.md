# Code gate review, round 4: RWB-E1-042 (RUN_ID `INC-003-epic-1-RWB-E1-042`)

| Field | Value |
|---|---|
| Review ID | `REVIEW-RWB-E1-042-CODE-004` |
| Gate | Code gate, pre-merge, round 4 (re-review after the code-gate fix round 3, documentation only) |
| Story | RWB-E1-042 Central configuration service and parameter catalog (EPIC-001, recovery P3/P4) |
| Range | `git diff develop-recovery...feature/RWB-E1-042-parameter-catalog` (merge base = `develop-recovery` tip `7bee04d`) |
| Tip | `25c8f94` (`25c8f947a46bc9c391f4697f7e4eec6f5a7467d2`). This is the branch ref and the worktree `HEAD`. `git status --short` and `git diff --name-status 25c8f94` in the worktree are both empty. |
| Round 3 | `review/code-gate-review-3.md` (FAIL 0C/0H/0M/1L at `25c8f94`: CODE3-001) |
| Inputs read independently | `implement/deviations.md` (DEV-20 row, its mapping table, the gate-impact note); `implement/review-fix/deviations-review-fix.md`; `implement/code-gate-fix/README.md` (the CODE2-001 row and the "Code-gate round 3" section); `implement/code-gate-fix/shared-updates.md:40`; `round2/it-parameter-config-attempt{1,2,3}.log`; native JUnit XML `backend/build/test-results/{test,recoveryIntegrationTest}` in the worktree; `ParameterConfigIT.java` at `25c8f94` (`TestBeans.RollbackCommitBreaker`) |
| Re-runs | None. Nothing changed in the code, the tests or the build output, so the round-3 recount of the native XML and JaCoCo still applies. |
| Repository | Read only apart from this file. |
| Human sign-off | **Not recorded.** OPEN-016. This review records no approval or acceptance (D-RUN-09). |

## Status

**PASS**: 0 Critical, 0 High, 0 Medium, 0 Low. CODE3-001 is closed, and this round raises no new
finding. The code, tests and build output are the same `25c8f94` set that round 3 checked.

## Round-3 finding: verification

| ID | Round-3 severity | Status | How it was verified (files and logs, not the summary) |
|---|---|---|---|
| CODE3-001 | Low | **Closed** | **Mapping.** `deviations.md:25-34` maps each of the six planned names to a test that exists. I looked up each mapped test in the native XML at `25c8f94`. Each one is a passing `testcase` with no `failure`, `error` or `skipped` element. <br>• T-04 → `ParameterConfigIT#readinessIsDownNamingTheKeyAndEnvironmentWhenNoValueAndNoDefault` (`ParameterConfigIT.xml`)<br>• T-10(b) → `ParameterConfigIT#failedRollbackCommitLeavesTheRowsApproved` (`ParameterConfigIT.xml`)<br>• T-17 → `ParameterLoadHandlerTest#aDifferentLoadStillMeetsTheApprovedFromCheck` (`ParameterLoadHandlerTest.xml`)<br>• T-28 → `ParameterCacheTest#aRebuildAfterTheEventReReadsTheRows` (`ParameterCacheTest.xml`)<br>• T-32 → `ParameterStartupCheckTest#aFutureSeedNeverFailsReadiness`, plus `ParameterConfigIT#readinessIsUpOnTheSeededCatalog` (both XML files)<br>• T-44 → `CatalogCompletenessCheckTest#theCredentialRuleAppliesToEveryEnvRow` (`CatalogCompletenessCheckTest.xml`)<br>**Caveats stated.** (a) T-17 maps to `aDifferentLoadStillMeetsTheApprovedFromCheck` (409 `MSG-P3-027`) and says why it is not `conflictingContentIs409` (that test asserts `MSG-GEN-004` for the index race; it also ran and passed). (b) T-32 is described as having no container-level case of that name or shape; it is covered by the unit test plus the DEV-11 / DEV-16 readiness pair. (c) For T-10(b), the effect column of the DEV-20 row says the failure is forced through a `beforeCommit` synchronization registered from an `@EventListener`, not a `@TransactionalEventListener(BEFORE_COMMIT)`, and cites DEV-08. The source matches: `TestBeans.RollbackCommitBreaker#onRollback` is `@org.springframework.context.event.EventListener` and calls `TransactionSynchronizationManager.registerSynchronization(… beforeCommit …)` (`ParameterConfigIT.java:794-805`). `deviations.md:36-39` lists the other test named in each of the six rows, and each of those exists under its planned name (round-3 XML check). `plan/tests/scenarios.md` was not edited, which is correct. **README sentence.** `code-gate-fix/README.md:12` now states only what the logs show. Attempt 1 ends BUILD FAILED, with `concurrentApprovalsGiveOneApprovedAndOne409() FAILED`, `AssertionError at ParameterConfigIT.java:658` and "37 tests completed, 1 failed" (log lines 31, 156, 178). Attempt 2 ends BUILD FAILED with an `AssertionError` at line 659 (log lines 29, 119). Attempt 3 ends BUILD SUCCESSFUL (log line 155). The README adds "The logs do not show the cause." The README no longer contains the `NullPointerException` / `delegatedObject` claim or the "assertions were not changed" claim, and no other file under `implement/` contains them. |

## Findings (this round)

| ID | Severity | Finding | Evidence | Remediation |
|---|---|---|---|---|
| — | — | None. | — | — |

## Gate checklist (full code gate at `25c8f94`)

| # | Gate | Result | Evidence |
|---|---|---|---|
| 1 | Spec / AC / TC trace | **PASS** | Every name in the scenarios map now resolves, either directly or through DEV-10, DEV-11 or DEV-20, to a test that ran. TC-20, -22 and -23 have their container tests (round 3). TC-E1-042-12 is still **Blocked** and is not reported as passed. |
| 2 | No skipped or weakened test | **PASS** | No change since round 3. 388 / 59 / 13 tests, 0 skipped. |
| 3 | 80 % on all four counters (native) | **PASS** | No change since round 3. LINE 91.0 %, INSTRUCTION 90.7 %, BRANCH 80.9 %, METHOD 95.8 %, recomputed in round 3 from the native JaCoCo XML (SHA-256 `8372e94b…`). The logs carry `TIP=25c8f94…`. Frontend is `NOT_APPLICABLE`: `git diff --name-status develop-recovery...feature/RWB-E1-042-parameter-catalog -- frontend api` is still empty. |
| 4 | Rules as data | **PASS** | No change. |
| 5 | No personal data, no secret value | **PASS** | No change. The DEV-20 text names tests only. |
| 6 | No direct ACE `public` read | **PASS** | No change. |
| 7 | Migration naming and one migration | **PASS** | No change. `V0001__rwb_e1_042_parameter_catalog_and_seed.sql`, line 1 `-- Story: RWB-E1-042`. |
| 8 | Migration seed rows | **PASS (unchanged)** | Round-1 row 8 stands. |
| 9 | `@PreAuthorize` on every endpoint | **PASS (unchanged)** | — |
| 10 | Flag-off contract (SPEC-021) | **PASS (unchanged)** | Round-3 row 10 stands. |
| 11 | Module boundaries (D-RUN-18..21) | **PASS (unchanged)** | No code change. |
| 12 | No new dependency | **PASS (unchanged)** | No code or build change. |
| 13 | Plan file scope and deviations | **PASS** | The deviation IDs are unique. `deviations.md` has rows DEV-01..DEV-12, DEV-19 and DEV-20. `review-fix/deviations-review-fix.md` has rows DEV-13..DEV-18. No ID appears in both files. The references are consistent: the `deviations.md` gate-impact note ("DEV-01..DEV-12, DEV-19 and DEV-20"; "None of DEV-01..DEV-20 …"), `code-gate-fix/README.md:20`, and `code-gate-fix/shared-updates.md:40` for the orchestrator. The fix round edited only run-owned files under `implement/`. No shared file was edited. |
| 14 | Production behaviour unchanged | **PASS** | The worktree has no change since `25c8f94`, and round 3 confirmed that the only main-code change since `9056ed2` is the comment deletion. |
| 15 | `DG-E042-*` gaps | **PASS** | No change. |
| 16 | API Tester stage | **PASS (for information)** | run5 at `25c8f94`, 13/13 (round 3). |
| 17 | AGENTS.md §9 human sign-off | **NOT RECORDED** | OPEN-016. No named human reviewer approval is available or claimed. |

## Candidate document gaps

| Candidate | Document (name, version, section) | Gap | Blocker | Reason |
|---|---|---|---|---|
| None new | — | This round changes run evidence only. | No | Nothing in the document set is silent or contradictory on these points. |

## Verdict

CODE3-001 is fixed. DEV-20 maps each of the six planned test names to a test that ran and passed at
`25c8f94`, and it states the three places where the mapping is not a pure rename (T-17, T-32 and
T-10(b)). The deviation IDs are unique, and every reference to them agrees. The README account of
the TC-20 attempts now says only what the logs show. The worktree is unchanged since `25c8f94`, and
every earlier gate check still holds. This gate review raises no finding. This review records no
approval or acceptance. The AGENTS.md §9 human sign-off is still outstanding (OPEN-016).

CODE_GATE: PASS [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 0]
