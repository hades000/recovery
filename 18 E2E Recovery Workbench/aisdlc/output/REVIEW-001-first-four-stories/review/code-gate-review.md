# Code gate review: REVIEW-001 post-merge remediation

| Field | Value |
|---|---|
| Run | `REVIEW-001-first-four-stories` |
| Scope | The "Fixed in this run" list of `../plan.md` (H1-H4, M1, M4-M6, M9-M11, L1-L3, L9) and INC-002 confirmation findings CONF-TE001-01 and -02, plus a fresh review of the whole diff |
| Branch | `fix/REVIEW-001-post-merge-review`, worktree `..\rwb-wt\REVIEW-001` |
| Diff range | `27567ed..cd2dffa` (code tip `5679889`, evidence tip `cd2dffa`), 22 commits, 51 files |
| Reviewer | Compliance Reviewer, code gate mode, on Claude Opus 5.5, high effort. Read only |
| Date | 19 Nov 2026 |
| Rule | D-RUN-09: any finding, Low included, fails the gate. No finding is accepted |

## 1. What I ran and read

- `./gradlew cleanTest test recoveryCoverageVerification` in the worktree at `cd2dffa`, with `RWB_ENVIRONMENT`
  not set in the shell: BUILD SUCCESSFUL, 430 tests, 0 failed, 0 skipped, coverage verification passed.
  This also shows that no unit test depends on a local `.env` for the environment value.
- Not run: `recoveryIntegrationTest`, Vitest, Playwright, `scripts/dev.ps1`. For those I checked the builder
  logs `final-it.log` (61 tests, 0 failed), `frontend-check.log` (29 tests passed), the red and green files.
- Read: `../plan.md`, `../code-quality-review.md`, INC-002 `review/code-gate-review-confirmation.md`,
  `implement/README.md`, `deviations.md`, `shared-updates.md`, the INC-003 spec and plan for E1-042, the whole
  code and test diff, and the touched classes in full where the diff was not enough.

## 2. Fix list

| Finding | Status | Evidence |
|---|---|---|
| H1 approve and rollback race on one (key, environment) | Closed (see CG-R001-02) | `ParameterLoadHandlerImpl.java:173,227,266-268` take `pg_advisory_xact_lock` on each sorted `parameter_value\|key\|environment` before `lockByLoadId`, inside the `REQUIRES_NEW` transaction on the one JPA transaction manager, so the lock lasts until commit. `ParameterValueRepository.java:62,69`. Red `5c8329d` (red-H1.txt: both new ITs fail), green `a6a6dd1`. `ParameterConfigIT#concurrentApprovalsOfTwoLoadsForOneKeyAreSerialised` and `#rollbackRacingAnApprovalOfTheSameKeyIsSerialised` wait on `pg_stat_activity` lock waits, not sleeps, and check the `valid_to` chain. The changed latch in TC-20 keeps its assertions |
| H2 DEV default for the environment | Closed | `application.yaml:76` `${RWB_ENVIRONMENT}` with no default; `application-local.yaml` no longer sets it; the three `@Value("${rwb.environment}")` lost their default; `PlatformInfoProperties.java:20-24` `@Validated`, `@NotNull`, `@Pattern("DEV\|SIT\|UAT\|PROD")`, registered unconditionally. An empty value from `docker-compose.yml:129` also fails the pattern. Red `9b46cc7`, green `6453715`. Meets AGENTS section 4 rule 11 |
| H3 coverage verification not in CI | Closed | `.gitlab-ci.yml:15` runs `test recoveryCoverageVerification`, commit `b3a5073`. My run shows the task passes |
| H4 unowned paths | Closed | `.gitlab/CODEOWNERS:28-32`, five lines for `@scb-ace/techx-recovery-tech-leads`, an owner already in the register. `OwnershipResolverTest#addendumPathsHaveOwners` resolves one file under each path. `CodeOwnersValidationTest` changes only shift line numbers. Commit `bfab086`. Ratification by the tech lead is open item SU-03, not a gate matter |
| M1 IT job not triggered by casewf Java | Closed (see CG-R001-03) | `.gitlab-ci.yml:61-62`, commit `caf6ee4` |
| M4 rollback event with no listener | Closed | `ParameterLoadRolledBack.java` deleted, no reference left. TC-10 (b) hook moved to the test recorder (D-06), same assertions. Commit `6127b75` |
| M5 rollback writes no decision record | Not closed | Rollback calls the recorder inside its transaction and maps a failure to 503 MSG-P7-003 (`ParameterLoadHandlerImpl.java:255,271-277`; red `370272b`, green `8801633`). The 503 path is right: the exception is thrown inside `requiresNew.execute`, so the rollback is undone and no cache clear is registered. But the record it writes is an approval record: CG-R001-01 |
| M6 outage reported as missing keys; WARN per probe | Closed | `ParameterStartupCheck.java` catches `DataAccessException` and `TransactionException` (connection loss surfaces as `CannotCreateTransactionException`), reports `database: unavailable`, logs only the exception class name, and logs through `changed(...)` with an `AtomicReference`, so each state is logged once. Red `66936a3`, green `131d17c` |
| M9 recursion-guard test could not fail | Closed | `ParameterCacheTest#theTtlReadDoesNotRecurse` now calls back into the same cache. Commit `637fc4c`. Ruling below |
| M10 grants comment understates access | Closed | `infra/postgres/init/20-grants.sql.inc:9-13` now matches the grant on line 20 (`WITH INHERIT FALSE, SET TRUE`). Commit `7481d15`; risk stays under OPEN-051 |
| M11 e2e `goto` hides a callback bug | Closed (see CG-R001-05) | Root cause: `main.tsx` wraps the app in `StrictMode`, and the Playwright `webServer` is `npm run dev` (`playwright.config.ts:21`), so the callback effect ran twice and the second call's catch sent the user to `/recovery`. `App.tsx:24,29` keeps one callback promise per page load; `platform.spec.ts` lost the `goto`. `AuthCallback.test.tsx` asserts the landing page and one call. Commit `a0bd791`. Ruling below |
| L1 dead or speculative code | Closed | `ParameterValueRepository.approved(key, env, productGroup)` and the repeated PRODUCT check deleted (`6d6f509`). Ruling below |
| L2 defensive code | Closed | `cause.getCause() == cause` (redundant: `getCause()` returns null for a self cause), the no-transaction branch of `afterCommit` (only called inside `requiresNew`), `statusOf` and the repeated null test removed. Commit `0f34b34` |
| L3 Javadoc of `InterimBusinessDateProvider` | Closed | Commit `02c15de` |
| L9 generator uses untrimmed cells | Closed | `build.gradle.kts:217-218` trims once before generating. Commit `5679889` |
| CONF-TE001-01 duplicate `published` entry | Closed | `ModuleMapLoader.java:152,162-165`, red `1a44389`, green `61aefc3`. See the INC-002 re-gate |
| CONF-TE001-02 comment and A-4 overstate the test | Closed (see CG-R001-04) | `RecoveryBoundaryTest.java:109-113` and the dated append-only note in INC-002 `plan/plan-addendum.md`, commit `8701e7d` |

## 3. Rulings

- **M9 (red evidence is an uncommitted mutation run): accepted as evidence, finding closed.** The defect was in
  the test, not the code. A committed red would need a broken `ParameterCache.ttl()` on the branch. `red-M9.txt`
  names the exact mutant and shows the old test passing and the new test failing (`StackOverflowError`) against
  it. That is the right evidence for a test that could not fail. The new test also verifies the read-back call.
- **L1 (partly kept): closed.** The plan's fix direction limits the deletion to code "where no test or spec item
  needs" it. The product-group overload, `entry()` and the product branch in `resolve` are named in the approved
  INC-003 `plan/plan.md:159` and tested by `ParameterServiceTest` and TC-31. The two items with no caller and no
  spec need were deleted. Removing the repeated PRODUCT check changes no result, because `resolve` makes the same
  check first.
- **M11 (Playwright not re-run): the unit evidence is enough for this gate.** The Vitest test reproduces the exact
  mechanism under `StrictMode`, and I confirmed that the e2e runs on the dev server, where `StrictMode` doubles
  effects. Removing the `goto` can only make the e2e stricter: if the cause were wrong, the e2e would fail, not
  hide the bug. The Playwright run of `platform.spec.ts` stays an open item for the orchestrator, to run before
  the branch is reported green. If it lands on `/recovery`, M11 reopens.

## 4. Fresh review of the diff

- Lock ordering and transaction scope: the advisory locks are taken first, inside the transaction that does the
  checks, the `valid_to` recompute and the record, and are released at commit. `findApproved(keys)` also returns
  other environments' rows of the same keys, but those groups are already consistent, so Hibernate's dirty check
  writes nothing to them. The only ordering defect is CG-R001-02.
- No test is disabled, skipped or loosened. TC-20 moved its latch and kept every assertion. The H2 test that
  asserted the DEV default now asserts a supplied value, and two tests cover missing and wrong-case values.
- No new dependency (`jakarta.validation` and logback are already on the classpath). No personal data: the new
  log lines carry an exception class name, a key name or an environment. Test values are synthetic.
- No new business literal beyond the DEV/SIT/UAT/PROD list the plan prescribed (L4 is already registered).
  No module boundary change: the `@Value` readers stay in `casewf.config`, the validation sits in
  `integration.internal` (D-03).
- Commits name the owning story and carry the `AISDLC-Run` trailer.

## 5. New findings

| ID | Severity | Where | Defect | Required fix |
|---|---|---|---|---|
| CG-R001-01 | Medium | `ParameterLoadHandlerImpl.java:255`; `InterimVersionDecisionRecorder.java:27-28` | The rollback records decision code `AC-VERS`. The document set defines `AC-VERS` as the decision log entry for a version approval (Build Notes Epic 1 v4, RWB-E1-037/-038; INC-003 SPEC-019). The interim line `Parameter decision recorded decision=AC-VERS table= loadId= keys= validFrom=` is the same for the approval and the rollback of one load, so the decision record says the version was approved when it was rolled back. Recording the missing code as an assumption (D-10, A-01) does not make the record true (AGENTS 3.4; audit logging check) | Make the record state what was decided without inventing a code: for example, add the outcome (`APPROVED` or `ROLLED_BACK`) to the non-published `VersionDecisionRecorder` port and to the interim line, and test that a rollback's record names `ROLLED_BACK` and an approval's names `APPROVED`. Keep the missing rollback code as open item SU-02 |
| CG-R001-02 | Low | `ParameterLoadHandlerImpl.java:262-268`; `ParameterValueRepository.java:69` | The pairs are sorted as strings, but the lock is taken on `hashtext(...)`, a 32-bit hash. If two pair strings ever share a hash, two transactions can take the real locks in opposite orders and deadlock (PostgreSQL then aborts one with 40P01, which is not mapped). The Javadoc and D-01 say the two transactions "cannot deadlock", which is not guaranteed. The chance is very small, but the claim is unconditional | Sort by the lock key the database uses (for example, read the distinct `hashtext` values of the load's pairs, sort them as integers and lock each), or correct the Javadoc and D-01 to state the limit. Keep the existing ITs green |
| CG-R001-03 | Low | `.gitlab-ci.yml:58-63` | The IT job still does not run when only an IT changes. The `changes` list has main-code paths only, so a merge request that edits `ParameterConfigIT`, `ParameterMigrationIT`, `RecoveryMigrationIT` or `RecoveryDatabaseIT` alone merges without running them. This branch itself changed two of them. M1's purpose, running the database ITs when the code they test changes, is only half met | Add the IT sources, for example `backend/src/test/java/**/*IT.java`, to `rules.changes` |
| CG-R001-04 | Low | `RecoveryBoundaryTest.java:113-117` | The comment rewritten for CONF-TE001-02 says "The six type-bearing packages are asserted", but the assertion lists seven (`casewf.config.api` was added by E1-042). The corrected comment is still not accurate | Say "seven", or drop the count |
| CG-R001-05 | Low | Commit `a0bd791`; `implement/red-M11.txt`; `deviations.md` D-09 | M11 is the one fix where a test could show the defect but no red commit came before the fix. The test and the fix are in one commit, and the red run used a hand-edited `App.tsx` that was never committed. D-09 does not record this as a deviation, while the README lists red/green pairs for the others (AGENTS 3.10; plan "each fix starts with a failing test") | Record it in `deviations.md` (what was run, against what, and why no red commit was made), so the record matches the history |

## 6. Verdict

Fifteen of the sixteen fix-list items and both confirmation findings are closed, and the unit suite and coverage
pass on my own run. M5 is not closed, because the rollback's decision record says "approved". Four Low findings
remain. Under D-RUN-09 the gate fails until all five are fixed and re-reviewed.

Open items (not findings): Playwright run of `platform.spec.ts` (M11 ruling); tech lead ratification of the H4
lines (SU-03); a local `.env` made before this branch needs `RWB_ENVIRONMENT=DEV` (D-04).

CODE_GATE: FAIL [CRITICAL: 0] [HIGH: 0] [MEDIUM: 1] [LOW: 4]
