# Ponytail review — RWB-E1-042 parameter catalog

What this change does: RWB-E1-042 adds the recovery module's versioned parameter catalog — a 19-row CSV catalog with two build checks and generated typed keys, the published `casewf.config.api` and `access.api.CatalogParameterReader`, one Flyway migration with 19 catalog rows and 40 seeded values, a per-instance read cache and readiness indicator, `GET /api/recovery/v1/admin/parameters`, and the load/approve/rollback handler with the `AC-VERS` decision hook. The flag `rwb.p3.configservice` gates the database-backed path; the endpoint and the handler are absent when it is off. The frontend and the OpenAPI file are unchanged.

## Must fix

1. **A rolled-back load blocks the same value from being loaded again** (`backend/src/main/java/th/co/scb/ace/demo/recovery/casewf/config/ParameterValueRepository.java:69-75`, `ParameterLoadHandlerImpl.java:90-104`)
   - **What this is:** `load` asks `findByContent(validFrom, hash)` whether this exact CSV and date were loaded before, and returns that load with `repeat = true`.
   - **Problem:** the query matches rows in every status. After a load is approved and rolled back, the same CSV for the same `validFrom` finds the ROLLED_BACK rows and returns them as an identical repeat. The caller gets a load that `approve` refuses because its status is not VALIDATED, so the value can never be loaded again. SPEC-013 and §12.5 check 11 allow a repeat only for a VALIDATED or APPROVED load.
   - **Fix:** add `and v.status in ('VALIDATED', 'APPROVED')` to the `findByContent` query. The same query serves the unique-violation re-read, so one edit covers both paths.
   - **If we skip it:** a rollback followed by a reload of the same value is impossible; the operator must change a value or the date to get past it.

## Should fix

2. **A value over 400 characters answers "someone else changed this record"** (`.../ParameterLoadValidator.java:85-99`, `.../ParameterLoadHandlerImpl.java:97-105`)
   - **What this is:** `param_value` is `varchar(400)`; the validator checks blank, type and range, but not length. `load` catches every `DataIntegrityViolationException` as a possible identical repeat and otherwise throws 409 MSG-GEN-004.
   - **Problem:** a 401-character value for `temporal.taskqueue.platform` (STRING, TABLE, loadable) fails the insert; the catch re-reads by content, finds nothing, and answers 409 "Someone else changed this record. Reload it to see their change." Reloading never helps — the value is simply too long. Every other load refusal is 422.
   - **Fix:** refuse `value.trim().length() > 400` in the validator with MSG-P1-002, using a named limit next to `ROLLBACK_REASON_MAX`. Then only the unique-index race reaches the catch.
   - **If we skip it:** operators get a wrong, unactionable message and open support tickets for a value they cannot fix from that message.

3. **Two approvals of the same key and date can answer 500 instead of 409** (`.../ParameterLoadHandlerImpl.java:149-196`, migration `V0001__rwb_e1_042_parameter_catalog_and_seed.sql:224-226`)
   - **What this is:** `approve` checks `countApprovedFrom(key, environment, validFrom)` and then updates the rows. The partial unique index `ux_parameter_value_approved_from` is the only guard across loads.
   - **Problem:** two loads for the same key, environment and date, approved at the same time, both pass the check because neither sees the other's uncommitted row. The second update violates the index at flush or commit and `DataIntegrityViolationException` escapes `requiresNew.execute`, so the caller gets a 500. SPEC-014 says a concurrent or repeated approval gets 409 MSG-GEN-004.
   - **Fix:** catch `DataIntegrityViolationException` around the approve transaction and throw 409 MSG-GEN-004.
   - **If we skip it:** a rare but real 500 on the admin approve path, and the spec's 409 contract is unmet.

4. **No test starts the application with the flag off (TC-22)** (`.../ParameterConfigIT.java:59-60`)
   - **What this is:** every system test sets `rwb.p3.configservice=true`; flag-off behaviour is tested only at unit level (`ParameterServiceTest`, `ParameterStartupCheckTest`).
   - **Problem:** nothing proves `@ConditionalOnProperty` removes `ParameterLoadHandlerImpl` and `ParameterCatalogController`, that `GET /admin/parameters` answers 404, or that `CatalogParameterReader` still serves a default. A typo in the property would expose the unfinished load operations and the build would stay green.
   - **Fix:** add one `@SpringBootTest(properties = "rwb.p3.configservice=false")` (no database needed for the bean assertions) that asserts `ObjectProvider<ParameterLoadHandler>.getIfAvailable() == null`, the GET 404, and the reader's default; or add a second context to the IT.
   - **If we skip it:** the story's guardrail (AGENTS §3.13, SPEC-021) is unverified.

5. **The readiness test checks the database clock, not readiness** (`.../ParameterConfigIT.java:183-186,475-477`)
   - **What this is:** `readinessIsUpOnTheSeededCatalog` runs `SELECT now()` and asserts the result is not null.
   - **Problem:** the readiness group in `application.yaml` (`include: readinessState,parameterCatalog`) and the `parameterCatalog` indicator are never exercised. A misspelled bean name or a broken indicator passes the suite. TC-32's system half (future-dated row, moved business date) is also missing.
   - **Fix:** inject `HealthEndpoint` or the `parameterCatalog` bean and assert UP on the seeded catalog, then remove a required approved value and assert DOWN with `MSG-P3-032`.
   - **If we skip it:** readiness can be broken in production with a green suite.

6. **No test forces the rollback's commit to fail (TC-10(b))** (`.../ParameterConfigIT.java:389-405`, `.../ParameterLoadHandlerImpl.java:230-234`)
   - **What this is:** the spec asks for a test-only `@TransactionalEventListener(BEFORE_COMMIT)` on `ParameterLoadRolledBack` that throws, proving the rows stay APPROVED and the cache is not rebuilt.
   - **Problem:** the rollback's after-commit invalidation and the rollback-on-commit-failure path are untested; the event is published but has no listener at all. Moving `cache.invalidateAll()` inside the transaction would still pass the suite.
   - **Fix:** add the test listener and the failed-commit case to `ParameterConfigIT`, asserting the rows are still APPROVED and the cache still serves the rolled-back version.
   - **If we skip it:** the one transaction boundary the spec singles out is unverified.

7. **Dead code** (`.../ParameterSchemaLimits.java:14-15`, `.../ParameterLoadHandlerImpl.java:26-27,278-281`, `.../ParameterCache.java:91-94`, `.../MagicNumberBaseline.java:184-197`)
   - **What this is:** `HASH_HEX_LENGTH`, `missing(String)`, `ParameterCache.today()`, `MagicNumberBaseline.literals()` and `matcher()`, and two imports are never used.
   - **Problem:** each is read and maintained for nothing; `HASH_HEX_LENGTH` suggests a hash check that is not there.
   - **Fix:** delete them, with the now-unused `Matcher` import.
   - **If we skip it:** dead weight in a story whose point is exactness.

8. **A non-UTF-8 file is decoded with replacement characters** (`.../ParameterLoadValidator.java:47`)
   - **What this is:** `new String(content, StandardCharsets.UTF_8)` silently replaces malformed bytes with U+FFFD.
   - **Problem:** a CSV saved in a legacy encoding with a non-ASCII byte in a STRING value is stored with `�`; the spec's check 2 says a non-UTF-8 file is refused. The current loadable STRING keys make this rare.
   - **Fix:** decode with `UTF_8.newDecoder().onMalformedInput(CodingErrorAction.REPORT)` and refuse MSG-P1-002.
   - **If we skip it:** a wrong value is stored silently.

## Nice to have

9. **The environment filter can grow the cache without bound** (`.../ParameterCatalogController.java:56,73`, `.../ParameterCache.java:49-59`)
   - **What this is:** any `environment` string becomes part of a cache key; expired entries are only replaced when the same key is requested again.
   - **Problem:** an authorized reader can add one entry per key per distinct string, for the life of the process. At the expected small admin load this is not reached.
   - **Fix:** validate `environment` against DEV/SIT/UAT/PROD, or against the key's `environments`, before use.
   - **If we skip it:** slow memory growth only under abuse.

Verdict: fix 1 before merge; then 2 and 3.
Lean: -30 lines possible.
Not checked: production database grants for the two new tables and the multi-instance behaviour of the per-instance cache; the container suite ran as `recovery_svc` and passed.

## Fix round 1 verification

Commit `8e51eb8` (prior tip `1ffb659`). I re-read the current code and tests, not the claims. The unit suite and `recoveryIntegrationTest` pass with no skips: 29 `ParameterConfigIT`, 3 `ParameterConfigIT$FlagOff`, and all unit classes; JaCoCo is 91.1% line and 81.1% branch.

| Finding | Verdict | Evidence |
|---|---|---|
| 1 | **Closed** | `findByContent` now filters `VALIDATED`/`APPROVED`; the advisory lock makes identical loads serial; `aRolledBackLoadCanBeLoadedAgain` reloads and re-approves; `twoConcurrentIdenticalLoads...` passes. |
| 2 | **Closed** | `PARAM_VALUE_MAX=400` check in the validator; `aValueLongerThanTheColumnIsRefused` and the IT both get 422 MSG-P1-002. |
| 3 | **Partly closed** | The unique-index race now returns 409 (`anApprovalUniqueViolationIs409`), but the broad catch introduced new finding 10. |
| 4 | **Closed** | `ParameterConfigIT$FlagOff` starts with the flag off: handler absent, GET 404, reader default 90 with version 0; 3 tests pass. |
| 5 | **Closed, test fragile** | The real `parameterCatalog` indicator and the `readiness` endpoint group are asserted UP and DOWN; see finding 11. |
| 6 | **Rows closed, cache unproven** | `RollbackCommitBreaker` forces the commit failure; rows stay APPROVED and `rollback_reason` is null; see finding 12. |
| 7 | **Closed** | The unused constant, methods and imports are gone; the baseline now records `400` twice. |
| 8 | **Closed** | Strict UTF-8 decoder refuses a malformed byte with 422 MSG-P1-002; `aNonUtf8FileIsRefused` passes. |
| 9 | **Closed** | `requireAllowedEnvironment` runs before any read; `anUnlistedEnvironmentIsRefused` verifies no service call; expired cache entries are evicted. See finding 13 for the contract delta. |

### New findings

10. **A recorder database failure becomes 409 instead of 503** (`backend/src/main/java/th/co/scb/ace/demo/recovery/casewf/config/ParameterLoadHandlerImpl.java:151-160,200-205,308-318`)
    - **What this is:** the new outer catch walks the cause chain of every `RuntimeException` from `approve` and turns any `DataIntegrityViolationException` into 409 MSG-GEN-004.
    - **Problem:** the recorder wrapper throws `ApiProblemException(MSG-P7-003, cause)`. A real decision-log writer's `flush()` (SPEC-019) throws a `DataIntegrityViolationException`; the walk finds it in the cause chain and returns 409 "someone else changed this record" instead of 503 MSG-P7-003. An after-commit listener failure is likewise reported as 409 although the approval committed, and a two-node cause cycle makes the walk loop forever. The current tests only throw `IllegalStateException`.
    - **Fix:** catch `DataIntegrityViolationException` directly around `values.flush()` (line 198) and throw 409 there; rethrow `ApiProblemException` before any cause check; delete or bound `isConstraintViolation`. Add a unit case where the recorder throws a `DataIntegrityViolationException` and assert 503 MSG-P7-003.
    - **If we skip it:** the next recorder implementation breaks the 503 contract; an after-commit failure looks like a duplicate approval.

11. **The readiness DOWN test depends on method order** (`backend/src/test/java/th/co/scb/ace/demo/recovery/casewf/config/ParameterConfigIT.java:196-227`)
    - **What this is:** the DOWN test deletes the `refdata.cache.ttl-seconds` PROD row and then calls the indicator; the UP test reads the same key first and caches the seeded 300.
    - **Problem:** JUnit's method order is deterministic but not guaranteed. The 10:58 run happened to run DOWN before UP; if UP runs first, the cache returns 300 and the DOWN assertion fails. The test passes by order, not isolation.
    - **Fix:** inject `ParameterCache` and call `invalidateAll()` after the delete, or use a required key no other test reads.
    - **If we skip it:** a method addition or JUnit upgrade turns the suite red.

12. **The failed-rollback test does not prove the cache is intact** (`.../ParameterConfigIT.java:262-283`)
    - **What this is:** after the forced commit failure the test reads 57 through the controller; the DB row is also 57.
    - **Problem:** a cache rebuilt from the DB would return the same 57, so the assertion cannot tell a rebuild from a cache hit. Moving `cache.invalidateAll()` inside the transaction would still pass.
    - **Fix:** spy `ParameterCache` and verify `invalidateAll` is never called after the failed rollback, or update the row to 58 by JDBC after the failure and assert the read is still 57.
    - **If we skip it:** the TC-10(b) cache claim remains unverified.

13. **The new 422 is not in the API contract** (`.../ParameterCatalogController.java:85-98`; `api/recovery-api-v4.yaml` `getAdminParameters` responses)
    - **What this is:** an unlisted `environment` now returns 422 MSG-GEN-002, but the OpenAPI lists 200/401/403/503 and `shared-updates.md` has no row for it.
    - **Problem:** the contract changes silently; a generated client or the API owner does not know the new response, and "environment must be between DEV and PROD" is a range message for a set. The security review accepted the control, so this is a contract note, not a code bug.
    - **Fix:** record the 422 delta for the OpenAPI owner in the shared updates, or use a documented response and a set-membership message.
    - **If we skip it:** contract drift.

14. **The event test's label says the opposite of its assertion** (`backend/src/test/java/th/co/scb/ace/demo/recovery/casewf/config/ParameterLoadHandlerTest.java:244`)
    - **What this is:** `committedAtPublish` is true when the commit happened before the publish, but the assertion's description says "published before the commit".
    - **Problem:** the test name and the code prove after-commit; the label says before. A reader can misread what is verified.
    - **Fix:** change the description to "published after the commit".
    - **If we skip it:** a confusing test only.

**Final verdict: not ship yet.** Fix 10 before merge; 11 and 12 are test-only and should go in the same round; 13 and 14 are follow-ups. After 10, the product paths are ready to ship.

## Fix round 2 verification

Commit `74e4ccb` (prior tip `8e51eb8`). Re-read the code and tests, not the claims.

Results: `./gradlew test` 386 tests, 0 failures; `recoveryIntegrationTest` 29 `ParameterConfigIT` + 3 `FlagOff` + 4 `ParameterMigrationIT` + 12 `RecoveryMigrationIT` + 6 `RecoveryDatabaseIT`, 0 failures, 0 skipped; `recoveryCoverageVerification` passes with LINE 91.1% (2579/2831), INSTRUCTION 90.7% (14041/15476), BRANCH 80.9% (1290/1594), METHOD 95.8% (551/575) — all four ≥80.

| Item | Verdict | Evidence |
|---|---|---|
| New 10 | **Closed** | `isApprovalConflict` now requires SQLState `23505` **and** `ux_parameter_value_approved_from` (message text or Hibernate `ConstraintViolationException#getConstraintName`). The three tests pass: `anApprovalUniqueViolationIs409` (23505 + index → 409), `aRecorderIntegrityFailureIs503` (recorder DIVE → 503 MSG-P7-003), `anUnrelatedIntegrityFailureIsNotAConflict` (23514 check → the DIVE propagates, never 409). An after-commit listener failure is not 409 by the same narrow check; it is code-inspected, not separately tested. |
| New 11 | **Closed** | `ParameterConfigIT.readinessIsDown...` calls `cacheSpy.invalidateAll()` after deleting the row and before the assertion; the result no longer depends on whether `readinessIsUp` ran first. |
| New 12 | **Closed** | The failed rollback verifies `cacheSpy.invalidateAll()` was never called; the successful rollback verifies one call, then the read returns 90 and `valueRepository.approved(...)` is re-read. |
| New 13 | **Recorded** | `implement/document-gaps.md` `DG-E042-ENV-422`, Blocker No; the 422 is requested from the API owner through `shared-updates.md` and remains open with OI-E1-042-011. |
| New 14 | **Recorded, but different item** | `DG-E042-ROLLBACK-EVENT`, Blocker No, records the rollback event still being published inside the transaction. It is not my New 14: the test label at `ParameterLoadHandlerTest.java:288` still says `as("published before the commit")` while the assertion proves the commit happened before the publish. This is a one-line test-description typo, not a behaviour change. |

No test weakening: the previous tests are kept and strengthened; the new tests are added; no skip or exclusion was introduced.

**Final verdict: Ship.** The product closure is clean; the remaining notes are a test-label typo, an optional after-commit-listener-failure test, and the 2-node cause-cycle guard in `isApprovalConflict` (a custom exception chain, not a JDBC/Hibernate one) — none blocks the merge.
