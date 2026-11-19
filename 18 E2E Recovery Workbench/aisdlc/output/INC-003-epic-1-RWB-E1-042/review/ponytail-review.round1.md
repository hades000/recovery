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
