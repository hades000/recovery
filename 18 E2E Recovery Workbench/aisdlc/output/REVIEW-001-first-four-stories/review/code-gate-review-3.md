# Code gate review, round 3: REVIEW-001 post-merge remediation

| Field | Value |
|---|---|
| Run | `REVIEW-001-first-four-stories` |
| Scope | Closure of round 2 finding CG2-R001-01 (`code-gate-review-2.md`), plus a fresh review of the round 3 diff and every comment in the branch that describes the lock design |
| Branch | `fix/REVIEW-001-post-merge-review`, worktree `..\rwb-wt\REVIEW-001` |
| Diff range | `82ee322..1bcd3ed` (code tip `976691b`, evidence tip `1bcd3ed`), 2 commits, 3 files |
| Reviewer | Compliance Reviewer, code gate mode, on Claude Opus 5.5. Read only |
| Date | 19 Nov 2026 |
| Rule | D-RUN-09: any finding, Low included, fails the gate |

## 1. What I ran and read

- `./gradlew cleanTest test` in the worktree at `1bcd3ed`, with `RWB_ENVIRONMENT` not set: BUILD SUCCESSFUL,
  431 tests, 0 failed, 0 skipped (summed from `build/test-results/test/*.xml` of my run). This matches the
  README row.
- Not run: the IT suite, Vitest, Playwright, `scripts/dev.ps1`. The diff changes no executable code, so the
  round 2 IT run at `82ee322` (62 tests, 0 failed) still holds for the same code.
- Read: round 1 and round 2 reviews, the whole diff `82ee322..1bcd3ed` and each commit on its own,
  `ParameterValueRepository.java` (lock queries and their Javadocs), `ParameterLoadHandlerImpl.java` (`load`
  content lock `:96`, `approveInTransaction` `:171-174`, `rollback` `:221-228`, `lockKeyEnvironments`
  `:262-270`), the `a6a6dd1` and `35dbf80` diffs (rename and overload history), `implement/README.md`,
  `deviations.md` D-01, `shared-updates.md` SU-05, and the lock comments in `ParameterConfigIT.java`
  (`:623-624`, `:740`, `:788`, `:793`). The worktree was clean before and after.

## 2. Closure of round 2 findings

| Finding | Status | Evidence |
|---|---|---|
| CG2-R001-01 (L) `advisoryLock(String)` Javadoc claimed the H1 lock | Closed | `ParameterValueRepository.java:70-74` now describes the `String` overload as the content lock only: `hashtext` of the key, serialising two loads of the same content and date so the second finds the first as a repeat. Its only caller is `load` (`ParameterLoadHandlerImpl.java:96`, key `validFrom + "\|" + hash`), so this is true. `:78-83` says the `int` overload is the (key, environment) lock on keys from `keyEnvironmentLocksOf`, serialising approvals and rollbacks (H1), taken in the ascending order that query returns (CG-R001-02). The only callers are approve (`:173`) and rollback (`:227`) through `lockKeyEnvironments` (`:269`), which iterates the returned list unchanged; the query orders by `lock_key` (`:66-67`). Commit `976691b` changes Javadoc lines only. This is the fix round 2 asked for |

## 3. Fresh review of the round 3 diff

- Comments and evidence only: `976691b` touches only the two Javadoc blocks in `ParameterValueRepository.java`
  (no annotation, signature or query changed). `1bcd3ed` touches only `implement/README.md` (one row added) and
  `deviations.md` (D-01, one sentence). No test changed.
- D-01's new sentence matches the history: `a6a6dd1` renamed `lockContent` to `advisoryLock` and added the H1
  caller of the `String` overload (`"parameter_value|" + pair`); `35dbf80` moved approve and rollback to the new
  `advisoryLock(int)`, leaving `load` as the only `String` caller. The rest of D-01 is unchanged from round 2.
- README row: commit `976691b`, comment only, 431 tests 0 failed 0 skipped. All confirmed by my run.
- Other lock comments in the branch: `ParameterLoadHandlerImpl.java:262-266` (lock before any row read,
  ascending lock-key order), `ParameterValueRepository.java:60-63` (`keyEnvironmentLocksOf`) and `:29`
  (`lockByLoadId`), and `ParameterConfigIT.java:623-624` and `:740` all agree with the code. No code comment
  names `lockContent` or ties the `String` overload to approvals or rollbacks.
- The INC-003 run artefacts (`docs/ARCHITECTURE.md:185-187`, `implement/shared-updates.md:46`,
  `review/security-review.md:341`) still describe the pre-REVIEW-001 design (`lockContent`, row locks only for
  approve and rollback). They are earlier-run evidence, not changed in this branch, and SU-05 already proposes
  recording the drift against INC-003 through the orchestrator. Round 2 saw the same state; no new evidence, so
  not a finding.
- Commits name the owning story or run, carry the `AISDLC-Run`, `AISDLC-Stage` and `AISDLC-Plan` trailers and
  name the producing model.

## 4. New findings

None.

## 5. Verdict

CG2-R001-01 is closed. The round 3 diff changes comments and evidence text only, every statement in the new
Javadocs, D-01 and the README row matches the code and the commit history, and no other code comment in the
branch contradicts the lock design. The unit suite passes on my own run.

Open items (not findings, carried from round 2): Playwright run of `platform.spec.ts` (M11 ruling); tech lead
ratification of the H4 lines (SU-03); a rollback decision code or confirmation of `AC-VERS` plus outcome (SU-02);
a local `.env` made before this branch needs `RWB_ENVIRONMENT=DEV` (D-04).

CODE_GATE: PASS [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 0]
