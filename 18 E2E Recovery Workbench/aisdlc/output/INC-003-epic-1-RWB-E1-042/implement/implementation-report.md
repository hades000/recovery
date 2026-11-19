# Implementation report — RWB-E1-042 central configuration service and parameter catalog

> Orchestrator note (19 Nov 2026): written before the merge. The branch (tip `25c8f94`) was merged at `0b87102`
> on 18 Nov 2026 20:46, so "Not merged" below is as of writing.

Run `INC-003-epic-1-RWB-E1-042` · Stage `implement` · Branch `feature/RWB-E1-042-parameter-catalog`
Worktree `C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\rwb-wt\RWB-E1-042`
Base `develop-recovery` at `7bee04d` (RWB-TE-001 and RWB-E1-044 merged). **Not merged.**

> This file supersedes `report.md`, which records the state before the pre-merge reviews.

```text
IMPLEMENTATION_STATUS_SUMMARY: SUCCESS — 26 tasks (TASK-00..TASK-25) executed, then every Ponytail, security-review and code-gate finding fixed on the same branch, test-first.
IMPLEMENTATION_STATUS_DETAIL: SUCCESS [REASON: at tip 25c8f94: 388 unit and build-check tests green; coverage 91.0 % LINE, 90.7 % INSTRUCTION, 80.9 % BRANCH, 95.8 % METHOD on the merged BUNDLE rule; 59 container tests green; dev.ps1 test exits 0] [UNBLOCK_ACTION: n/a]
IMPLEMENTATION_CLARIFICATION_STATUS: READY [OPEN_ITEMS: 25 carried from the spec, none blocking; TC-E1-042-12 stays Blocked by OI-E1-042-001] [UNBLOCK_ACTION: n/a]
IMPLEMENTATION_DESIGN_SOURCE: NOT_REQUIRED [NOTE: UI In Scope NO; 0 screens; no Figma link]
FRONTEND_STATUS: NOT_APPLICABLE
BACKEND_STATUS: REQUIRED — PASS
GATE_REVIEW: PENDING_ORCHESTRATOR
STATUS: SUCCESS
NEXT_STEP: Human review of implementation evidence, then manually start API Tester with RUN_ID=INC-003-epic-1-RWB-E1-042
```

## Commits

| SHA | Subject |
|---|---|
| `b038730` | catalog file, CSV reader and the two build-check tooling classes |
| `bf2ddcd` | completeness and magic-number build checks with the reviewed baseline |
| `203028f` | generated typed keys and the published config.api and access.api surface |
| `11cd8ce` | problem forms, message catalogue and the interim capability seam |
| `dd4ad63` | one guarded migration for the parameter catalog and its seed |
| `5ad5594` | parameter read service, cache, readiness, catalog endpoint and P4 reader |
| `5777d4f` | load, approve and rollback handler with the decision recorder and cache refresh |
| `1ffb659` | system suite, coverage wiring and the full container suite |
| `8e51eb8` | pre-merge review fixes for the load handler, readiness and the build guards |
| `74e4ccb` | Ponytail closure: narrow the approval conflict mapping, deterministic readiness and rollback tests |
| `9056ed2` | Code-gate CODE-001: an identical repeat of an approved load returns it (check 11 before check 12) |
| `216a696` | Code-gate round 2 CODE2-001: container tests for TC-20, TC-22 and TC-23 |
| **`25c8f94`** | **Code-gate round 2 CODE2-003: stale `isApprovalConflict` comment deleted; review records tracked** |

## Review fixes (commit `8e51eb8`)

Every item below has a test that failed before the fix and passes after. The red run is saved at
`review-fix/red-round.log` (7 failing tests); the green runs are `review-fix/green-round-1.log`, `review-fix/round2/unit-and-coverage.log`, `review-fix/round2/it-full.log`,
`review-fix/unit-and-coverage.log`, `review-fix/it-full.log` and `review-fix/merge-gate.log`.

| Review item | Fix | Test |
|---|---|---|
| Ponytail Must 1 — a rolled-back load blocks the same value | `findByContent` filters `status in ('VALIDATED','APPROVED')` | `ParameterConfigIT#aRolledBackLoadCanBeLoadedAgain` (reload is `VALIDATED`, new load id, approvable) |
| Ponytail Should 2 — a 401-character value answers 409 | `PARAM_VALUE_MAX` check in the validator, 422 MSG-P1-002 `value is longer than 400 characters` | `ParameterLoadValidatorTest#aValueLongerThanTheColumnIsRefused`, `ParameterConfigIT#aValueOverTheColumnWidthIsRefusedWhole` |
| Ponytail Should 3 — a concurrent approval answers 500 | `approve` catches a constraint violation (and any cause under it) and answers 409 MSG-GEN-004 | `ParameterLoadHandlerTest#anApprovalUniqueViolationIs409` |
| Ponytail Should 4 — TC-22 missing | `@Nested FlagOff` context with `rwb.p3.configservice=false`: handler absent, GET 404, reader serves the default, handler implements no `access.api` type | `ParameterConfigIT$FlagOff` (3 tests) |
| Ponytail Should 5 — readiness tested the database clock | the real `parameterCatalog` indicator and the real readiness group are asserted UP on the seed and DOWN with `MSG-P3-032` and `{name, environment}` when a required key has no value and no default | `ParameterConfigIT#readinessIsUpOnTheSeededCatalog`, `#readinessIsDownNamingTheKeyAndEnvironmentWhenNoValueAndNoDefault` |
| Ponytail Should 6 — TC-10(b) missing | a test listener registers a `beforeCommit` failure on `ParameterLoadRolledBack`; the rows stay APPROVED, `rollback_reason` stays NULL, the endpoint still serves the rolled-back-to value | `ParameterConfigIT#failedRollbackCommitLeavesTheRowsApproved` |
| Ponytail Should 7 — dead code | `HASH_HEX_LENGTH`, `missing()`, `ParameterCache.today()`, `MagicNumberBaseline.literals()`/`matcher()` and three unused imports deleted | suite compiles and stays green |
| Ponytail Should 8 — non-UTF-8 decoded with `�` | strict decoder with `CodingErrorAction.REPORT`, refusal `file is not UTF-8` | `ParameterLoadValidatorTest#aNonUtf8FileIsRefused` |
| Nice 9 / SEC-042-01 — unbounded cache growth | the controller validates `environment` against DEV/SIT/UAT/PROD (422 MSG-GEN-002) before any read; the cache evicts expired pairs on every miss | `ParameterCatalogControllerTest#anUnlistedEnvironmentIsRefused`, `ParameterCacheTest#anExpiredEntryIsEvicted` |
| SEC-042-02 — generator trusts catalog fields | the generator validates every row (16 columns, key pattern, kind, value_type, scope, `required`/`secret` strictly `true|false`, value_source, unique constant name) and escapes `\n`, `\r`, `\t` and control characters; a bad row fails with its row number | `review-fix/generator-bad-row.log` (fails: `row 2 column 'required' violates true or false`) and `review-fix/generator-good-row.log`; `ParameterKeysGenerationTest#theGeneratedSourceEscapesStringsAndEmitsLiteralBooleans` |
| SEC-042-03 — credential deny-list misses a connection string | `connection-string`, `connectionstring`, `pwd`, `accountkey`, `passphrase`, `sas-token` added | `CatalogFileParserTest#credentialBearingPropertiesAreRefused` with `rwb.blob.connection-string`, `rwb.sftp.pwd`, `rwb.security.accountKey` |
| SEC-042-04 — the approval event is published inside the transaction | published in the `afterCommit` callback, after the cache invalidation | `ParameterLoadHandlerTest#theApprovalEventIsPublishedAfterTheTransaction` (published only after `doCommit`), `ParameterConfigIT#noEventOnARefusedApproval`, `#rollbackRestoresTheEarlierVersion` (a rollback publishes none) |

Also fixed while closing Must 1: two identical loads now take a `pg_advisory_xact_lock` on the
content hash inside their own transaction, so the second waits for the first and finds it as a repeat
(`ParameterConfigIT#twoConcurrentIdenticalLoadsGiveOneLoadAndOneRepeat`).

## Ponytail closure (commit `74e4ccb`)

| Item | Fix | Test |
|---|---|---|
| New 10 (blocking) â€” `isConstraintViolation` too broad | The 409 MSG-GEN-004 mapping now requires **SQLState `23505` and the index `ux_parameter_value_approved_from`** (message text or Hibernate `ConstraintViolationException#getConstraintName`). A recorder integrity failure keeps 503 MSG-P7-003; an after-commit listener failure or a check-constraint failure is never 409 | `ParameterLoadHandlerTest#aRecorderIntegrityFailureIs503` (503, MSG-P7-003, no placeholders), `#anUnrelatedIntegrityFailureIsNotAConflict` (a `23514` check failure propagates, never 409), `#anApprovalUniqueViolationIs409` (real index + SQLState, 409) |
| New 11 â€” readiness DOWN depended on order/cache state | The test calls `cache.invalidateAll()` after deleting the rows and before it asserts | `ParameterConfigIT#readinessIsDownNamingTheKeyAndEnvironmentWhenNoValueAndNoDefault` |
| New 12 â€” the failed-rollback cache assertion could not tell a rebuild from a hit | The failed rollback verifies `cache.invalidateAll()` was **never** called; the successful rollback verifies it was called **once** and that the repository `approved(...)` is re-read | `ParameterConfigIT#failedRollbackCommitLeavesTheRowsApproved`, `#rollbackRestoresTheEarlierVersion` |
| New 13 â€” the 422 is not in the OpenAPI contract | Recorded, not fixed | `implement/document-gaps.md` `DG-E042-ENV-422`, Blocker = No, owner API owner |
| New 14 â€” the rollback event is published inside the transaction | Recorded, not fixed | `implement/document-gaps.md` `DG-E042-ROLLBACK-EVENT`, Blocker = No, owner the event's future consumer |

## Code-gate fix (commit `9056ed2`)

Answers `review/code-gate-review.md` (FAIL at `74e4ccb`). Details and the commit each review verdict
refers to: `code-gate-fix/README.md`.

| Finding | Fix | Test |
|---|---|---|
| CODE-001 (High) — an identical repeat of an APPROVED load answered 409 `MSG-P3-027` | Check 12 moved to `ParameterLoadValidator#validateApprovalWindow`, called by `ParameterLoadHandlerImpl#load` inside the locked transaction **after** the check-11 repeat lookup (§12.5 order, SPEC-013; DEV-19, first numbered DEV-13) | `ParameterConfigIT#anApprovedLoadRepeatsInsteadOfBeingRefused`, `ParameterLoadHandlerTest#anApprovedLoadRepeatsBeforeTheApprovedFromCheck`; check 12 still refuses a different load: `ParameterLoadHandlerTest#aDifferentLoadStillMeetsTheApprovedFromCheck` (red: `code-gate-fix/red-ParameterLoadHandlerTest.log`), `ParameterLoadValidatorTest#anApprovedVersionOnOrAfterTheDateIsARefusal409`, `ParameterConfigIT#conflictingContentIsRefused` |
| CODE-002 (Low) — review records at the pre-fix tip | Final `ponytail-review.md` and `security-review.md` copied unchanged into `review/`; older copies kept as `*.round1.md` | `code-gate-fix/README.md` |
| CODE-003 (Low) — inconsistent counts | All suites re-run at `9056ed2` (figures since superseded by round 2 below) | `code-gate-fix/*.log` |

## Code-gate round 2 (commits `216a696`, `25c8f94`)

Answers `review/code-gate-review-2.md` (FAIL 0C/0H/0M/3L at `9056ed2`). Details: `code-gate-fix/README.md`.

| Finding | Fix | Test or evidence |
|---|---|---|
| CODE2-001 (Low) — TC-20, TC-22 and TC-23 had no container-level test | Three test cases added to `ParameterConfigIT` and one to `$FlagOff`, as `plan/tests/scenarios.md` names them. No production code changed: all pass on the existing code. | `ParameterConfigIT#concurrentApprovalsGiveOneApprovedAndOne409` (TC-20: a latch holds both approval transactions at the row lock; one APPROVED, one 409 `MSG-GEN-004`); `#flagOnLoadsThroughTheAdapter` and `$FlagOff#flagOffStillStartsAndRefusesParameterLoads` (TC-22: test-only `ParameterLoadBranch` stand-in with `ObjectProvider<ParameterLoadHandler>`; flag on it delegates and returns the handler's `loadId`; flag off 404 `MSG-P4-003`, nothing written); `#unknownKeyEmptyFileAndPastValidFrom` (TC-23: 422 `MSG-P1-002`, 422 `MSG-GEN-001` field `file`, 422 `MSG-P3-027`; nothing written). Logs: `code-gate-fix/round2/it-parameter-config-attempt3.log` (green), `it-full.log` |
| CODE2-002 (Low) — DEV-13 used twice; stale gate-impact note | The code-gate deviation is renumbered **DEV-19** (DEV-13..18 are in `review-fix/deviations-review-fix.md`); the gate-impact note points at `code-gate-fix/test-and-coverage-counts.txt` and `code-gate-fix/round2/` | `deviations.md`, `code-gate-fix/README.md` |
| CODE2-003 (Low) — stale Javadoc at `ParameterLoadHandlerImpl.java:319` | Line deleted | commit `25c8f94` |

## Results (of record: tip `25c8f94`)

| Command | Exit | Result | Log |
|---|---|---|---|
| `./gradlew clean`, then `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/dev.ps1 test` | 0 | Gradle `test` 388 tests, 0 failures, 0 skipped; `npm run check` 28 tests, statements 91.89 % | `code-gate-fix/round2/clean.log`, `code-gate-fix/round2/dev-test.log` |
| `./gradlew recoveryCoverageVerification` | 0 | LINE 2579/2833 = **91.0 %**, INSTRUCTION 14045/15482 = **90.7 %**, BRANCH 1289/1594 = **80.9 %**, METHOD 552/576 = **95.8 %** (one BUNDLE rule, 0.80) | `code-gate-fix/round2/coverage-verification.log`, `code-gate-fix/round2/recoveryCoverageReport.xml` |
| `./gradlew recoveryIntegrationTest` | 0 | 59 tests, 0 failures, 0 skipped: `ParameterConfigIT` 33 + `FlagOff` 4, `ParameterMigrationIT` 4, `RecoveryMigrationIT` 12, `RecoveryDatabaseIT` 6 | `code-gate-fix/round2/it-full.log` |
| `./gradlew generateParameterKeys -PparameterCatalog=<bad fixture>` | 1 | fails with `parameter-catalog.csv row 2 column 'required' violates true or false` (expected failure; run at `8e51eb8`, build script unchanged since) | `review-fix/generator-bad-row.log` |

Counts are derived from the native XML in `code-gate-fix/test-and-coverage-counts.txt`.

**Superseded figures.** At `9056ed2`: the same unit and coverage figures, but 55 container tests
(`ParameterConfigIT` 30 + `FlagOff` 3; `code-gate-fix/it-full.log`). At `74e4ccb`: 386 unit tests; LINE 2579/2831 = 91.1 %, INSTRUCTION
14041/15476 = 90.7 %, BRANCH 1290/1594 = 80.9 %, METHOD 551/575 = 95.8 %; 54 container tests
(`review-fix/round2/`). The earlier status line's "384 tests, 90.8 % INSTRUCTION, 81.1 % BRANCH" and
the `merge-gate.log` / `review-fix/merge-gate.log` runs predate `74e4ccb`. None of them is of record.

`scripts/dev.ps1 e2e` was **not** run: it needs `dev.ps1 up`, which the run rules forbid from the
worktree. `PlatformE2ETest` is unchanged by this story.

## Files

89 files at `1ffb659`; code-gate round 2 touches `ParameterConfigIT` (`216a696`) and one comment line of `ParameterLoadHandlerImpl` plus the two review records (`25c8f94`); the code-gate fix `9056ed2` touches 5 (`ParameterLoadHandlerImpl`, `ParameterLoadValidator` and their three test classes); the review-fix commit touches 18 files (+485/−58): `ParameterValueRepository`,
`ParameterLoadHandlerImpl`, `ParameterLoadValidator`, `ParameterCache`, `ParameterCatalogController`,
`ParameterSchemaLimits`, `build.gradle.kts`, six test classes, the baseline and the two fixture files.

## Migration

`backend/src/main/resources/db/modulemigration/recovery/V0001__rwb_e1_042_parameter_catalog_and_seed.sql`
— line 1 `-- Story: RWB-E1-042`; `<seq>` unfixed (D-RUN-07); one file for the story; unchanged by the
review fixes.

## Not done, and why

- TC-E1-042-12 stays **Blocked** by RWB-E1-022 and RWB-E1-037; never reported as passed.
- No merge, no shared file, no build log, no other story touched.
