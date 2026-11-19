# Code gate review, round 2: REVIEW-001 post-merge remediation

| Field | Value |
|---|---|
| Run | `REVIEW-001-first-four-stories` |
| Scope | Closure of round 1 findings CG-R001-01 to -05 (`code-gate-review.md`), plus a fresh review of the round 2 diff and the code it touches |
| Branch | `fix/REVIEW-001-post-merge-review`, worktree `..\rwb-wt\REVIEW-001` |
| Diff range | `cd2dffa..82ee322` (code tip `270bf50`, evidence tip `82ee322`), 8 commits, 15 files |
| Reviewer | Compliance Reviewer, code gate mode, on Claude Opus 5.5, high effort. Read only |
| Date | 19 Nov 2026 |
| Rule | D-RUN-09: any finding, Low included, fails the gate |

## 1. What I ran and read

- `./gradlew cleanTest test recoveryCoverageVerification` in the worktree at `82ee322`, with `RWB_ENVIRONMENT`
  not set: BUILD SUCCESSFUL, 431 tests, 0 failed, 0 skipped, coverage verification passed.
- `./gradlew cleanRecoveryIntegrationTest recoveryIntegrationTest` (Testcontainers PostgreSQL 16) at `82ee322`:
  BUILD SUCCESSFUL, 62 tests, 0 failed, 0 skipped (ParameterConfigIT 36, FlagOff 4, RecoveryDatabaseIT 6,
  ParameterMigrationIT 4, RecoveryMigrationIT 12). The result files are from my run: their timestamps are after
  the evidence commit. The full run includes the new lock-order test with every other test, which is the case
  that `270bf50` fixed.
- Not run: Vitest, Playwright, `scripts/dev.ps1`. There is no frontend change in this round.
- Read: round 1 review, `implement/README.md`, `deviations.md` (D-01, D-09, D-10, D-15), `shared-updates.md`,
  `red-CG-R001-01.txt`, `red-CG-R001-02.txt`, `final-test.log`, `final-it.log`, the whole diff and each commit
  on its own, `ParameterLoadHandlerImpl.java` (load, approve, rollback, lock and record paths) and
  `ParameterValueRepository.java` in full, AGENTS section 3 rules 10, 15, 16 and section 4 rule 11.
  The worktree was clean before and after.

## 2. Closure of round 1 findings

| Finding | Status | Evidence |
|---|---|---|
| CG-R001-01 (M) rollback recorded as an approval | Closed | `VersionDecisionRecorder.java:15-16` takes an `outcome`. `ParameterLoadHandlerImpl.java:209` passes `APPROVED` and `:256` passes `ROLLED_BACK`. `InterimVersionDecisionRecorder.java:25-28` logs `outcome=`. The approver ID is still not logged. Red `e84b99a` comes before green `8228d77` (commit order and times 00:57, 00:58). The red commit compiles against the old signature, because the test goes through `InterimVersionDecisionRecorder`. `red-CG-R001-01.txt` shows it failing on the assertion (two identical lines, no `outcome=`), not on compilation. `ParameterLoadHandlerTest#theDecisionRecordNamesTheOutcome` asserts exactly two lines in order (approval `outcome=APPROVED`, rollback `outcome=ROLLED_BACK`) and no approver ID. The mock-based tests (`rollbackRecordsTheDecision`, `interimRecorderIsCalledOnceInsideTheTransaction` and the two recorder-failure tests) now pin the outcome per path. The decision code stays `AC-VERS` under assumption A-01, and the missing rollback code is proposed as an open item (SU-02). This is what round 1 asked for. D-10 and A-01 match the code |
| CG-R001-02 (L) locks sorted by string, taken on `hashtext` | Closed | `ParameterValueRepository.java:65-68` returns the distinct `hashtext('parameter_value\|'\|\|key\|\|'\|'\|\|environment)` values of the load, ordered as integers. `:79-80` `pg_advisory_xact_lock(:key)` with an `int` binds int4, which widens to the same bigint key that `pg_advisory_xact_lock(hashtext(text))` uses, so both overloads share one key space. `ParameterLoadHandlerImpl.java:268-270` locks in the returned order, and the method reference resolves to the `int` overload (unboxing; `String` is not applicable). Deadlock check: approve and rollback are the only callers. Both take every key-environment lock of the load, in one global ascending order, before any row read (`:173`, `:227`). The checks read `countApprovedFrom` and `countApprovedBefore` only for those same pairs. A hash collision collapses two pairs into one lock (`distinct`), which only serialises more. `load` holds only its content lock and waits on nothing that approve or rollback holds, so a collision between a content key and a pair key cannot form a cycle. Red `d10418e` comes before green `35dbf80` (01:09, 01:10). `red-CG-R001-02.txt` fails on `isSorted` with the string-order keys `[-282478707, -1577611500, ...]`. The test discriminates: it first asserts that the string order of the eight fixture pairs is not their lock-key order, using the database's own `hashtext`. It counts the actual `advisoryLock` calls (8) after `clearInvocations`, so the load's content lock is excluded. Then it checks that the refused approval left the rows `VALIDATED` |
| CG-R001-03 (L) IT job not run when only an IT changes | Closed | `.gitlab-ci.yml:64-65` adds `backend/src/test/java/**/*IT.java` and `backend/src/test/resources/flyway-fixtures/**/*`. The five ITs are self-contained classes (no shared IT support class outside `*IT.java`), and the Flyway fixtures are the only IT-only resources. Commit `2ed89d5` |
| CG-R001-04 (L) comment says six, seven asserted | Closed | `RecoveryBoundaryTest.java:113` says "seven". The assertion lists seven packages. Commit `b0e397d` |
| CG-R001-05 (L) M11 red not committed or recorded | Closed | `deviations.md` D-15 records what was run (`npx vitest run src/auth/AuthCallback.test.tsx`), against what (HEAD `App.tsx` with only `export` added), the result (`/recovery` instead of `/recovery/platform`), and why there is no red commit. It states that a red commit was possible and not made. D-09 points to D-15. History is not rewritten. Under the round 1 rulings, an honest record of process history that cannot change without a rewrite is acceptable closure. The M11 Playwright run stays an open item |

### 270bf50 fixture change

It is test-only and touches one method. `from` moved from the business date to `today.plusDays(300)`, and the
`finally` now restores `today` (before, it restored `from`, which then equalled `today`, so the behaviour is the
same). No assertion was removed or loosened: the fixture-discrimination assertion, `hasSize(8)`, `isSorted`, the
`MSG-P3-027` refusal and the `VALIDATED` status check are unchanged. The lock order does not depend on the date,
so the red result at `d10418e` (isolated run) still holds for the moved fixture. The cause given (another test's
later approved version refusing the load by check 12) is consistent with the full run failing and the isolated
run passing. My full run passes. The eight `VALIDATED` rows it leaves at day +300 are not approved, so they do
not affect check 12 or `findApproved` in other tests.

## 3. Fresh review of the round 2 diff

- Red before green: both pairs are in the right order in `git log`, and each red file names its HEAD and command.
- No test is disabled, skipped or weakened. The changed verifications and stubs add the outcome argument. The
  TC-20 latch moved with the rename to `keyEnvironmentLocksOf` and keeps its assertions.
- No new dependency (logback `ListAppender` is already on the test classpath). No personal data: the new log
  field is a fixed outcome word, and the test asserts that the approver ID is absent. No new business literal:
  `APPROVED` and `ROLLED_BACK` are the existing load statuses.
- `{h-schema}` resolves through `hibernate.default_schema: ${rwb.schema}` (`application.yaml:23`).
- AGENTS section 3 rule 15: the locks cover every pair whose rows the approval and rollback checks read, and
  the H1 concurrency ITs still pass. Section 4 rule 11 is not touched in this round.
- Commits name the owning story, carry the `AISDLC-Run` trailer and name the producing model.
- Docs: README, D-01, D-10, D-15, A-01 and SU-02/-04/-05/-06 match the code and the history, except the
  Javadoc in CG2-R001-01.

## 4. New findings

| ID | Severity | Where | Defect | Required fix |
|---|---|---|---|---|
| CG2-R001-01 | Low | `backend/src/main/java/th/co/scb/ace/demo/recovery/casewf/config/ParameterValueRepository.java:70-76` | The Javadoc of `advisoryLock(String)` still says it serialises "approvals and rollbacks of the same (key, environment) (REVIEW-001 H1)". Since `35dbf80` that is false: the only caller of the `String` overload is `load` (`ParameterLoadHandlerImpl.java:96`, content lock), and approvals and rollbacks lock through `advisoryLock(int)` with keys from `keyEnvironmentLocksOf`. The fix that changed the caller left this text, so the comment points a reader to the wrong overload for the H1 lock. Round 1 raised the same kind of defect (CG-R001-04) | Change the `advisoryLock(String)` Javadoc to describe the content lock only, and say on `advisoryLock(int)` that it is the approval and rollback lock (REVIEW-001 H1, CG-R001-02). Comment only; no test change needed |

## 5. Verdict

All five round 1 findings are closed, including the Medium (M5 now records what was decided). The unit suite,
coverage and the full IT suite pass on my own run. The lock-order fix is correct and deadlock-free for the
approve and rollback paths, and the test discriminates. One new Low remains: a Javadoc that the CG-R001-02 fix
made false. Under D-RUN-09 the gate fails until it is fixed and re-reviewed.

Open items (not findings, carried from round 1): Playwright run of `platform.spec.ts` (M11 ruling); tech lead
ratification of the H4 lines (SU-03); a rollback decision code or confirmation of `AC-VERS` plus outcome (SU-02);
a local `.env` made before this branch needs `RWB_ENVIRONMENT=DEV` (D-04).

CODE_GATE: FAIL [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 1]
