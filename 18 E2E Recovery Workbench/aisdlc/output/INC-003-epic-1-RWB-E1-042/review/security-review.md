---
story: RWB-E1-042
stage: security-review
reviewer: security reviewer (subagent)
tip: 1ffb659
range: develop-recovery...feature/RWB-E1-042-parameter-catalog
date: 2026-11-18
verdict: PASS_WITH_LOW_FINDINGS
counts: 0 Critical, 0 High, 0 Medium, 4 Low
---

# Security review — RWB-E1-042 central configuration service and parameter catalog

**Scope:** the whole story diff `develop-recovery...feature/RWB-E1-042-parameter-catalog` at tip
`1ffb659` (89 files, +7,555/−19), read against `aisdlc/RUN-BRIEF.md`, `AGENTS.md`,
`aisdlc/.github/rules/security-quality-standards.md`, `aisdlc/.github/contexts/backend-standards.md`
(BS-4) and `aisdlc/output/INC-003-epic-1-RWB-E1-042/specify/spec.md` (revision 13).

**Verdict: PASS_WITH_LOW_FINDINGS — mergeable.** No Critical, High or Medium finding. Four Low
findings, two of which are hardening of controls that are correct for the shipped data. The one
new HTTP endpoint carries a method check; maker-checker is enforced in the handler and the database;
the migration is guarded and schema-qualified; no personal data or secret value reaches a response
or a log.

| Severity | Count | Finding |
|---|---|---|
| Critical | 0 | — |
| High | 0 | — |
| Medium | 0 | — |
| Low | 4 | SEC-042-01 … SEC-042-04 |

---

## 1. Findings

### SEC-042-01 (Low) — Unbounded `ParameterCache` growth from an unvalidated `environment` query parameter

**Where:** `backend/src/main/java/th/co/scb/ace/demo/recovery/casewf/config/ParameterCatalogController.java:56,73`
(the `environment` request parameter is taken verbatim and passed to the service) and
`backend/src/main/java/th/co/scb/ace/demo/recovery/casewf/config/ParameterCache.java:49-59`
(`entries.put(cacheKey, ...)`, one entry per `key + "|" + environment`).

**Failure case:** a caller authenticated with any role holding Rules and parameters R (37 of the 37
RW- roles in `interim-capability-grants.csv`, including read-only `RW-AUDIT`, `RW-TRIBE`,
`RW-BIANCA`-style roles) sends
`GET /api/recovery/v1/admin/parameters?environment=e1`, `?environment=e2`, … Each request inserts one
entry for every catalog key (19 today) into a singleton `ConcurrentHashMap`. Expired entries are only
replaced when the same `(key, environment)` pair is read again; `invalidate` only removes the pair a
load touched and `invalidateAll` only runs on a rollback, so entries for environments that are never
requested again are never removed. The key is unbounded (Tomcat accepts query strings up to the
header limit), so repeated requests grow the heap and add 19 database round-trips each, eventually
exhausting heap and the connection pool — an authenticated denial of service from a read-only role.
There is no cross-key cache poisoning: catalog keys cannot contain `|` (the `^[A-Za-z][A-Za-z0-9_.-]{0,99}$`
rule), so the composite key cannot be confused with another key.

**Smallest fix:** in `ParameterCatalogController.list`, reject an `environment` outside
`DEV|SIT|UAT|PROD` (or outside `definition.environments()`) with a 400/422 before the loop; in
`ParameterCache.approved`, remove expired entries (for example
`entries.entrySet().removeIf(e -> !e.getValue().expiresAt().isAfter(now))`) or bound the map size and
clear it when the bound is exceeded. Validating against the four values also matches the database
checks `ck_parameter_catalog_environments` and `ck_parameter_value_environment`.

---

### SEC-042-02 (Low) — Build-time generated-code injection / unescaped catalog fields in `generateParameterKeys`

**Where:** `backend/build.gradle.kts:175-179` (`literal()` escapes only `\` and `"`; `constantName()`
only upper-cases and replaces `.`/`-`), `:207-208` (`row[8].trim()` and `row[12].trim()` are inserted
raw as the `required` and `secret` constructor arguments), `:238-240` (`compileJava` depends on
`generateParameterKeys`). The validating reader `CatalogFileParser` and
`CatalogCompletenessCheckTest` live in `test` and run after compilation.

**Failure case:** the catalog CSV is a reviewed data file, but the generator trusts every token. A
row whose `description` contains a quoted newline (the CSV reader accepts it and
`CatalogFileParser` only checks blank/length) makes the generated
`build/generated/sources/parameterKeys/.../ParameterKeys.java` invalid and breaks the build with a
confusing error. A crafted `required` (column 9), `secret` (column 13) or key can inject Java into
the generated class — for example closing the `ParameterKey` constructor and opening a static
initializer — because the completeness check that would reject the key runs in `test`, after
`compileJava`. CI runs `./gradlew test`, so the generated class is compiled and loaded before any
rejection; the payload then executes on the build runner with its credentials. (The key alone is
upper-cased, which makes a key-only payload harder, but the raw `required`/`secret` fields are
unrestricted.)

**Smallest fix:** in the generator, before writing, validate the row exactly as `CatalogFileParser`
does: `key` matches `^[A-Za-z][A-Za-z0-9_.-]{0,99}$`, `required`/`secret` are `true|false`, `kind`,
`scope`, `value_source` and `value_type` are in their sets; and escape `\n`, `\r`, `\t` and other
control characters in `literal()`. Fail the task with the row number on any violation so the PR
author sees the data error before compilation.

---

### SEC-042-03 (Low) — Credential-name deny-list misses `connection-string`/`pwd`; an ENV catalog row can expose the Blob account key

**Where:** `backend/src/test/java/th/co/scb/ace/demo/recovery/architecture/parameters/CatalogFileParser.java:44-45`
(`CREDENTIAL_WORDS`) and `:270-280` (`namesACredential`), applied by
`CatalogCompletenessRules.rowRules`; the existing credential-bearing Spring property
`rwb.blob.connection-string` is at `backend/src/main/resources/application.yaml:103`; the response
path is `ParameterCatalogController.java:73,79` (`service.inEnvironment` → `valueInForce`).

**Failure case:** the rule refuses an ENV row only when a dot-segment contains one of `password`,
`passwd`, `secret`, `token`, `credential`, `apikey`, `api-key`, `api_key`, `privatekey`,
`private-key`, `private_key`. `rwb.blob.connection-string` has segments `rwb`, `blob`,
`connection-string`; none matches. In Azure that property holds a storage connection string with
`AccountKey=` (the local `.env` holds the Azurite key). Adding a catalog row
`blob.connection,ENVIRONMENT,STRING,,,,,GLOBAL,false,RW-PLATADM,"DEV,SIT,UAT,PROD",...,false,ENV,rwb.blob.connection-string,...`
passes `theRealCatalogIsComplete` and the `GET /admin/parameters` endpoint returns the connection
string as `valueInForce` to every role with Rules and parameters R. No load is involved, so the load
validator cannot stop it; the build check is the only guard. The shipped CSV has no such row today,
so this is a control gap, not a current leak.

**Smallest fix:** add `connection-string`, `connectionstring`, `pwd`, `passphrase` and `sas` to
`CREDENTIAL_WORDS` and to the §7.1 list, or replace the deny-list with an allow-list of the
non-credential property prefixes (`rwb.temporal.*`, `rwb.drools.*`, …). A false positive is handled
by renaming the property, as the spec already says.

---

### SEC-042-04 (Low) — `ParameterVersionApproved` is published inside the approval transaction, not after commit

**Where:** `backend/src/main/java/th/co/scb/ace/demo/recovery/casewf/config/ParameterLoadHandlerImpl.java:191-194`
(`events.publishEvent(approved)` then `afterCommit(...)` only for cache invalidation); the plain
`@EventListener` in `ParameterConfigIT.java:521-524` demonstrates that a normal listener runs
synchronously inside the transaction.

**Failure case:** SPEC-RWB-E1-042-018 says the event is published “after the approval commits”. The
code publishes before the commit; only the cache invalidation is registered `afterCommit`, so the
local cache is safe. A plain listener added by RWB-TE-006 for the outbox, or any notification
listener, would handle an approval that can still roll back at commit (for example a lost connection
after `flush`), announcing or writing an approval that never existed. The same pattern applies to
the rollback event at `:232-233`, which has no listener today.

**Smallest fix:** move the `publishEvent` into the existing `afterCommit` callback (compute the
`ParameterVersionApproved` record before the commit and publish it in the callback), or require every
listener to be `@TransactionalEventListener(phase = AFTER_COMMIT)` and state that in the published
type's Javadoc. The former matches the wording of SPEC-018 and removes the dependence on listener
annotations.

---

## 2. Checked and clean

### Authorization

- **One new endpoint** `GET /api/recovery/v1/admin/parameters` carries
  `@PreAuthorize("@capabilityCheck.require(authentication, 'Rules and parameters', 'R', 'read parameters')")`
  (`ParameterCatalogController.java:51-52`). The bean name `capabilityCheck` matches
  `@Component("capabilityCheck")` on `InterimCapabilityCheck`; `require` throws
  `ApiError.NOT_PERMITTED` with the action text, which the existing `ApiExceptionHandler` renders as
  403 MSG-P4-002. Tests: `ParameterCatalogControllerTest.refusalCarriesTheActionText` (403 and the
  exact action text) and `ParameterConfigIT.readWithoutTheRightIsRefused` (403 through the real
  `SecurityConfig` and JWT decoder).
- **Filter chain:** `SecurityConfig.java:68-81` requires a `RW-` authority for `/api/recovery/**` and
  answers 401 MSG-P4-001 with no token or no Workbench role. The endpoint is not in a `permitAll`
  path; `/actuator/health/**` is the only unauthenticated path and exposes no parameter value.
- **Grants match the matrix:** `interim-capability-grants.csv` was compared with Users, Roles and
  Permissions v4 lines 74-110. `RW-COE` = CRUD, `RW-RISK` = RA, `RW-REFADM`/`RW-PLATADM`/`RW-AUDIT`/
  `RW-TRIBE` = R, `RW-PHONECOL`/`RW-FIELDCOL` = none; `PT-AGENCY` is absent. No over-grant.
- **Load/approve/rollback:** this story exposes no HTTP path for them (D-RUN-10); RWB-E1-043 owns the
  endpoint and the Reference data C/A/U checks (spec §4.3, §16). The handler itself enforces
  maker-checker: `ParameterLoadHandlerImpl.approve:157-159` rejects an approver equal to the author,
  and the migration adds `ck_parameter_value_maker_checker` (`V0001:159-168`) as a second line. The
  flag-off contract is implemented (handler/controller absent; `ObjectProvider` consumers; 404 is
  E43S's for loads). Note the residual risk in §3: the handler trusts caller-supplied user IDs; E43S
  must pass `jwt.sub`.
- **No missing `@PreAuthorize`:** a search of the diff for `@RestController`, `@RequestMapping`,
  `@GetMapping`, `@PostMapping`, `@PutMapping`, `@DeleteMapping` and `@PatchMapping` returns only the
  one controller and its one method.

### SQL injection, identifiers and key-literal rule

- Every repository query is JPQL with `:name` bindings (`ParameterValueRepository.java:17-75`); there
  is no `nativeQuery`, no `EntityManager.createNativeQuery`, no `JdbcTemplate` in main code and no
  string-formatted SQL. `findApproved(keys)` binds an `IN :keys` list.
- `CatalogParameterReaderImpl`, `CatalogSource`, `ParameterKeys` and `ParameterKey` perform no SQL;
  the reader resolves the key through the generated `ParameterKeys.byName` and rejects an unknown,
  wrong-type or PRODUCT key.
- The CSV reader (`CsvRows`) is a pure parser: no file path, no SQL, no identifier use. It rejects a
  quote after a closing quote and an unterminated quote; the load path passes the bytes to
  `ParameterLoadValidator`, which looks the key up by name in `ParameterKeys.all()`.
- The typed-key rule is intact: `CatalogCompletenessRules` refuses a non-literal reader argument,
  a `CatalogParameterReader::get` reference, a `var` local from a reader and an ambiguous receiver;
  the only `ParameterKey.of` in main code is the factory itself (fixtures are test-scope). No
  business value is written as a literal outside the reviewed magic-number baseline.
- The migration is static SQL: statement groups are literal; `${recoverySchema}` is the only
  qualifier; there is no `SET search_path`, no `EXECUTE format(...)` and no identifier built from
  input.

### Personal data and secrets

- `author_user_id`, `approver_user_id`, `created_by` and `updated_by` appear only in
  `ParameterValueEntity`, the repository/handler writes and the migration seed. They are absent from
  `CatalogParameterView`, `ParameterEntry`-style records (`CatalogEntry`), `ParameterLoadResult`,
  `ParameterVersionApproved`, `ParameterLoadRolledBack` and every log line. `CatalogParameterView`
  has no `author`/`approver`/`createdBy`/`updatedBy` component.
- `ParameterStartupCheck` logs only the key name and environment (`:79-80`);
  `InterimVersionDecisionRecorder` logs decision code, table, loadId, keys and validFrom only (`:27-28`);
  `ParameterLoadHandlerImpl` logs only a status-disagreement warning (`:263`); the new
  `ApiExceptionHandler` branch logs the message ID, status, traceId and cause class, never the cause
  message, stack trace, placeholders or detail (`:49-52`).
- The seed identity `00000000-0000-0000-0000-0000000e1042` and the test users
  `00000000-0000-0000-0000-00000000b001/b002/b003`/`a001/a002` are synthetic UUIDs, not people. The
  catalog CSV's `used_by` values are module and story names. No name, email, account number or
  address appears in the diff.
- Secrets: `ace.db.password` is `secret=true`, `value_source=SECRET`, with no default; the DB check
  `ck_parameter_catalog_secret_default` enforces it; the load validator refuses a secret key
  (`ParameterLoadValidator:78-80`); `ParameterService` throws `SecretNotServedException` before any
  database read (`ParameterServiceImpl:95-98`); the GET masks `default`, `valueInForce`, `versionNo`
  and `validFrom` (`ParameterCatalogController:77-80`). The CSV contains the key name only, never a
  value. No secret value is in the migration, the fixtures, the logs or the responses.
- `parameter_value` is not exposed through Spring Data REST: `spring-boot-starter-data-rest` is not
  on the classpath and no `@RepositoryRestResource` exists.

### Cache, errors and flag-off

- The cache holds only the `APPROVED` rows (`ParameterCache:49-58`, `values.approved` filters
  `status = 'APPROVED'`), never a `VALIDATED`/`ROLLED_BACK` row or a secret; the business date is
  resolved per read, so a version starts on its `valid_from` without a rebuild. Invalidation on
  approval is registered `afterCommit` (`ParameterLoadHandlerImpl:193-194`); rollback invalidates all
  after commit (`:233`). Other instances rely on the TTL, as SPEC-009/015 say.
- The GET catches only `DataAccessResourceFailureException` and `CannotCreateTransactionException` and
  renders the status-only 503 of E7 (`ParameterCatalogController:67-69`); `ApiExceptionHandler`
  suppresses the cause text and `ProblemFactory` emits `urn:rwb:problem:unavailable` with no
  `messageCode`/`detail`. The unit test `databaseFailureIsAStatusOnly503` asserts the absence of both.
- Flag `rwb.p3.configservice` is false in `application.yaml` and true in `application-local.yaml`;
  the controller and `ParameterLoadHandlerImpl` carry `@ConditionalOnProperty`; `ParameterServiceImpl`
  and `CatalogParameterReader` stay registered and serve defaults/ENV with no database read when off;
  no bean of `casewf.config` injects `ParameterLoadHandler` by type, so the context starts.

### Migration, grants and module boundary

- One migration, `A backend/src/main/resources/db/modulemigration/recovery/V0001__rwb_e1_042_parameter_catalog_and_seed.sql`;
  `develop-recovery` held only `README.md` in that folder, so `V0001` is the next free number. No
  merged migration is edited.
- Line 1 is `-- Story: RWB-E1-042`; the DDL is guarded (`CREATE TABLE IF NOT EXISTS`, `ADD COLUMN IF
  NOT EXISTS`, `DO` blocks testing `pg_constraint` by name), the folder name and the statement list
  match SPEC-001/002; the seed is `ON CONFLICT (param_key) DO NOTHING` plus `WHERE NOT EXISTS`, and
  the self-check `DO` block is the one of SPEC-006.
- Every object is `${recoverySchema}`-qualified. A search for `public.`, `GRANT`, `REVOKE` and
  `search_path` in the file returns nothing. `RecoveryMigrationLintTest` on this branch is the
  RWB-E1-044 quote-aware lint and is green on the folder.
- **D-RUN-14:** the migration adds no grant and needs none; `rwb_migrator` holds only `USAGE ON SCHEMA
  public` and the non-inheriting `ace_view_owner` membership (`infra/postgres/init/20-grants.sql.inc`),
  and `recovery_svc` gets DML on the new tables through `ALTER DEFAULT PRIVILEGES FOR ROLE
  rwb_migrator IN SCHEMA recovery`.
- **D-RUN-20:** the `PARAMETER` branch stays in `casewf.config.api`; `ParameterLoadHandler` is
  published there (not an `access.api` SPI), no bean implements an `access.api` handler, and no
  P1/P2/P4 → P3 edge is added. The module map gains `casewf.config.api`; `RecoveryBoundaryTest` and
  `ModuleMapLoaderTest` are extended, not relaxed (the four pre-existing named interfaces are still
  asserted).
- No new dependency: `backend/build.gradle.kts` adds tasks, a source directory and JaCoCo
  class-directories only; the `implementation`/`testImplementation` blocks are unchanged.

### Path traversal

- The catalog path is a fixed `layout.projectDirectory.file("src/main/resources/config/parameter-catalog.csv")`;
  the completeness rules walk the fixed `src/main/java` root; the grants file is a fixed
  `classpath:access/interim-capability-grants.csv`; the load reader consumes an `InputStream`, never a
  path; the migration and test paths are constants. No user-controlled path reaches `Files.*` or
  `Resource`.

---

## 3. Residual risks and notes (not counted as findings)

1. **`InterimCapabilityCheck.has` matches only the first character of `right`**
   (`InterimCapabilityCheck.java:50`: `rights.indexOf(right.charAt(0))`). The current caller passes
   the single letter `"R"` and the matrix uses single letters, so the endpoint is correct. A future
   caller of the published `CapabilityCheck` seam that passes `"READ"`, `"RESTORE"` or `"DELETE"`
   would be authorized by a role holding only `R`/`D`; comparing the full token (or rejecting a
   `right` longer than one character) closes the hazard before RWB-E1-037 replaces the
   implementation.
2. **`ParameterKey.of` bypasses the catalog metadata** (`ParameterKey.java:74-77`): it always builds
   `secret=false`, `scope=GLOBAL`, empty range. `ParameterService.get` trusts the key it is given. A
   caller could construct `ParameterKey.of("ace.db.password", String.class)` and the service would
   treat it as non-secret. No `parameter_value` row exists for the secret today and the load path
   refuses secret keys, so nothing is served; resolving the definition from `CatalogSource` by name
   inside `ParameterService` (or making `of` test-scope) removes the bypass.
3. **Maker-checker trusts caller-supplied identities.** `load(..., authorUserId)` and
   `approve(..., approverUserId)` take UUIDs from the caller; the DB check only compares the two
   UUIDs. The spec (§7.4) requires RWB-E1-043 to pass the JWT `sub` for both; if that endpoint ever
   takes either from the request body, the author can approve their own load. The E43S review should
   assert the source of both values.
4. **Cross-environment reads are by design.** `GET /admin/parameters?environment=PROD` from a DEV
   context returns PROD rows if the database holds them; SPEC-007/011 and §7.5 specify the query
   parameter, and the permission matrix has one "Rules and parameters" area, not per-environment
   rights. Each environment is a separate deployment/database, so this is not a finding; confirm the
   SIT/UAT databases are never shared with DEV before go-live.
5. **ENV values are served by design.** The three shipped ENV rows (`rwb.temporal.target`,
   `rwb.temporal.namespace`, `rwb.drools.kiebase-cache-max`) are non-sensitive. The credential-name
   rule (SEC-042-03) is the control that keeps a secret-bearing property out of this list; it needs
   the missing words before the catalog grows.
6. **The `GET` endpoint returns the catalog to every role with R, including read-only case roles**
   (RW-AUDIT, RW-TRIBE, …). The matrix grants R to those roles, so this is intended; the values are
   business configuration, not personal data or secrets.

---

## 4. Evidence

| Check | Command / evidence | Result |
|---|---|---|
| Diff and tip | `git diff --stat develop-recovery...feature/RWB-E1-042-parameter-catalog`; `git log -1` = `1ffb659` | 89 files, +7,555/−19 |
| Only one migration added | `git diff --name-status … -- '*db/modulemigration*'` | `A V0001__rwb_e1_042_parameter_catalog_and_seed.sql` |
| No `public.`/grant in migration | `Select-String -Path V0001… -Pattern 'public\.|GRANT|REVOKE|search_path'` | no matches |
| No new dependency | `git diff … -- backend/build.gradle.kts` | tasks/source set/JaCoCo only |
| Method security enabled | `SecurityConfig.java:47` `@EnableMethodSecurity`; `ParameterCatalogController.java:52` | present |
| 403 path | `ParameterCatalogControllerTest.refusalCarriesTheActionText`; `ParameterConfigIT.readWithoutTheRightIsRefused` | 403 MSG-P4-002 with "read parameters" |
| Secrets masked | `ParameterCatalogControllerTest.secretIsListedWithoutValue`; `ParameterConfigIT.secretIsListedWithoutValue` | no `default`/`valueInForce`/`versionNo` |
| PII absent from logs | `InterimVersionDecisionRecorder.java:27-28`; `ApiExceptionHandler.java:49-52` | no user IDs, no cause text |
| Maker-checker | `ParameterLoadHandlerImpl.java:157-159`; `V0001:159-168`; `ParameterLoadHandlerTest.authorCannotApprove` | both layers |
| Flag-off | `ParameterCatalogController.java:31`; `ParameterLoadHandlerImpl.java:44`; `ParameterServiceImpl.java:39-45` | absent/conditional |
| SQL bindings | `ParameterValueRepository.java:17-75` | `:name` only, no native query |
| Grants vs matrix | `interim-capability-grants.csv` vs Users, Roles and Permissions v4 lines 74-110 | exact match, 37 RW- roles |

No code, test, plan or shared file was modified by this review.

---

# Fix round 1 verification (`8e51eb8`, prior tip `1ffb659`)

**Verdict: PASS — 4/4 findings closed; 0 Critical / 0 High / 0 Medium / 0 Low open; no new
security regression.** The fix commit adds the controller/cache guard, the generator validation,
the widened credential rule and the after-commit event, plus tests. Only the review file was edited
by this re-check; no code, test, plan or shared file was changed.

| Finding | Status | Closure evidence |
|---|---|---|
| SEC-042-01 arbitrary `environment` / unbounded cache | **CLOSED** | `ParameterCatalogController.java:57-58,90-96` validates `requested` against `DEV/SIT/UAT/PROD` before the loop and returns 422 `MSG-GEN-002`, `field=environment`; `ParameterCache.java:56-58` removes expired pairs on every miss. Tests: `ParameterCatalogControllerTest.anUnlistedEnvironmentIsRefused` (422 and `verify(service, never())`), `ParameterCacheTest.anExpiredEntryIsEvicted` (`entryCount()==1`). The key space is now 19 keys × 4 environments; an arbitrary string cannot become a cache key. |
| SEC-042-02 generator injection / unescaped fields | **CLOSED** | `build.gradle.kts:176-215`: `literal()` escapes `\`, `"`, `\n`, `\r`, `\t` and control chars; a `require` loop validates 16 columns, the key regex, `kind`, `value_type`, `scope`, `required`, `secret`, `value_source` and a unique constant name, and fails with a `GradleException` naming the row and column. Manual verification: `.\gradlew generateParameterKeys "-PparameterCatalog=src/test/resources/architecture/fixtures/parameter-checks/catalog/generator-injection.csv"` fails with `parameter-catalog.csv row 2 column 'required' violates true or false` (exit 1); the default task rerun is up to date and succeeds. `ParameterKeysGenerationTest.theGeneratedSourceEscapesStringsAndEmitsLiteralBooleans` checks the real output (no NUL/BEL, balanced quotes per line, no `static {`, no `System.out`). The injection fixture is exercised manually, not by a JUnit test; the build-script validation is the control. |
| SEC-042-03 credential deny-list gap | **CLOSED** | `CatalogFileParser.CREDENTIAL_WORDS` now includes `connection-string`, `connectionstring`, `pwd`, `accountkey`, `passphrase`, `sas-token`; `env-credential.csv` adds c9 `rwb.blob.connection-string`, c10 `rwb.sftp.pwd`, c11 `rwb.security.accountKey` (names only, no values); `CatalogFileParserTest` expects 11 findings. `rwb.blob.connection-string` now fails the credential rule as required. |
| SEC-042-04 event before commit | **CLOSED** | `ParameterLoadHandlerImpl.approveInTransaction` registers `afterCommit(() -> { cache invalidate; events.publishEvent(approved); })`; the event is no longer published inside the transaction, the rollback path publishes no `ParameterVersionApproved`, and the commit callback runs once. Tests: `ParameterLoadHandlerTest.theApprovalEventIsPublishedAfterTheTransaction` (`committedAtPublish` is true), `anApprovalUniqueViolationIs409` (`verify(events, never())`), `ParameterConfigIT.noEventOnARefusedApproval` and the rollback test (no new approval event). |

## New-regression checks

- **Authorization:** the one endpoint's `@PreAuthorize` is unchanged
  (`ParameterCatalogController.java:53`); the new environment check runs after method security, so an
  unauthenticated/unauthorised caller still gets 401/403 and cannot use the 422 path to probe the
  catalog. No new endpoint or `permitAll` rule. The new `FlagOff` IT confirms the handler and endpoint
  are absent, the endpoint answers 404 and the reader still serves defaults.
- **SQL/identifiers:** the new `ParameterValueRepository.lockContent` is a `nativeQuery` with a bound
  `:key` (`select pg_advisory_xact_lock(hashtext(:key))`); no identifier or SQL is built from input.
  `load` now takes the advisory lock inside its own transaction, and `findByContent` filters
  `VALIDATED/APPROVED`, so the duplicate-load race is serialised and a rolled-back load can be
  reloaded. No new SQL injection or dynamic identifier.
- **Build/path:** the only new path input is the build-only Gradle property
  `-PparameterCatalog`; it is not reachable from the runtime or a request. It can read a path chosen
  by the build invoker, who already runs build code; the generator validates the file before writing
  and the output path is fixed. No runtime path traversal.
- **Dependencies:** `build.gradle.kts` changes are the tasks, source set, JaCoCo class directories and
  the catalog override only; no `implementation`/`testImplementation` line was added.
- **Secret/PII:** the new tests use `synthetic-queue`, `q`.repeat and the existing synthetic UUIDs;
  `env-credential.csv` and `generator-injection.csv` carry key/property names and descriptions only.
  No new log line carries a value or a user ID; no new response field exposes `author_user_id`,
  `approver_user_id`, `created_by` or `updated_by`.
- **Non-security observation (track separately):** `approve`'s new `isConstraintViolation` maps any
  `DataIntegrityViolationException` in the cause chain to 409 `MSG-GEN-004`. If the real decision
  recorder (RWB-E1-027) throws a `DataIntegrityViolationException`, the call would report 409 instead
  of the 503 `MSG-P7-003` that SPEC-014 requires. The approval still rolls back and the audit entry
  is not written, so this is an error-mapping issue for the RWB-E1-027/E43S integration, not a
  security bypass.
- **Non-security observation:** the controller hardcodes `Set.of("DEV","SIT","UAT","PROD")` for the
  new validation. These are the four environment codes already enforced by the database checks and
  the catalog, not a business threshold; it is a code-standard point only.

**Final security verdict: PASS.** All four Low findings are closed; no new Critical, High, Medium or
Low security finding. The only residual notes are the package-private `ParameterLoadRolledBack`
event, which is still published inside the rollback transaction and has no production listener
(the `ParameterVersionApproved` finding is closed), the 409/503 error-mapping observation, and the
hardcoded environment list. None blocks the merge.
