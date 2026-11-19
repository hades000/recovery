---
title: "RWB-E1-042 Central configuration service and parameter catalog — documentation index"
run_id: "INC-003-epic-1-RWB-E1-042"
story: "RWB-E1-042"
epic: "EPIC-001"
stage: "docs (final documentation)"
date: "2026-11-18"
status: "DOCUMENTED — code gate round 4 PASS 0/0/0/0 at 25c8f94 (rounds 1-3 FAIL, each fixed and re-gated); nothing accepted; human sign-off not recorded (OPEN-016); no merge"
branch: "feature/RWB-E1-042-parameter-catalog @ 25c8f94 (merge base 7bee04d: RWB-TE-001 and RWB-E1-044 merged)"
sources: "spec revision 13, plan v2, tasks v2, scenarios v2, implementation report, unit-test report, test-and-coverage-counts.txt, API test report, functional test report (N/A), code gate reviews 1-2, security review, ponytail review, deviations"
---

# Central configuration service and parameter catalog (RWB-E1-042)

**DOC ID:** DOC-RWB-E1-042-001 · **Maps to:** SPEC-RWB-E1-042-001..-027; AC1–AC11; BR1–BR7; TASK-00..TASK-25; CODE-01..CODE-30

RWB-E1-042 is the build-order 3 story of EPIC-001 (Build Sequence v6; depends on RWB-E1-044 and
RWB-TE-001). Story file: User Stories Epic 1 Story Files v7,
`rwb-e1-042-central-configuration-service-and-parameter-catalog-v1.md`. In this repository it gives the
recovery module one place where every business parameter and environment setting is defined, typed,
versioned and read:

1. a **catalog file** (`backend/src/main/resources/config/parameter-catalog.csv`, 19 bootstrap rows) is the only
   definition of a parameter; the build turns it into typed `ParameterKeys` and refuses literals and
   uncatalogued keys (BR1, BR2);
2. **one migration** creates or completes `parameter_catalog` and `parameter_value` and seeds the 19
   catalog rows and 40 approved version-1 value rows;
3. **`ParameterService`** returns a typed value with its version for a business date and the running
   environment, with no restart when a new version starts (BR5, AC11);
4. **`ParameterLoadHandler`** validates, versions, approves (maker-checker) and rolls back `PARAMETER`
   loads (BR3, BR4); RWB-E1-043's shared reference-load endpoint will call it (D-RUN-10, D-RUN-20);
5. **`GET /api/recovery/v1/admin/parameters`** lists the catalog with the value in force; secrets are
   listed, never served (BR6);
6. the service is **not ready** while a required parameter has no value in force and no default (BR7);
7. code **outside P3** reads parameters only through P4 `access.api.CatalogParameterReader` (D-RUN-19).

Change classification: `NEW_STORY`; Logic In Scope YES; API In Scope YES (one endpoint, already in
API Specification v4, no change to `api/recovery-api-v4.yaml`); UI In Scope **NO** (story v7 §15 "No
screen in this story"; SCR-39 is Epic 8). Frontend and `api/` are untouched
(`git diff --name-status 7bee04d 25c8f94 -- frontend api` is empty).

## 1. What was built

| Deliverable | Where (repository paths) | SPEC | CODE |
|---|---|---|---|
| Catalog file, 19 rows (13 from the 10 Nov 2026 pack + the six D-RCV-36 keys) | `backend/src/main/resources/config/parameter-catalog.csv` | 003, 005, 024 | CODE-04 |
| Generated typed keys (19 constants, `all()`, `byName`) and the Gradle task `generateParameterKeys` | `backend/build.gradle.kts`; output `build/generated/sources/parameterKeys/.../casewf/config/api/ParameterKeys.java`; `casewf/config/api/ParameterKey.java` | 005 | CODE-06..08 |
| Build checks: catalog completeness, magic numbers (ratchet baseline), credential-name rule | `backend/src/test/java/.../architecture/parameters/`; `backend/src/test/resources/architecture/magic-number-baseline.csv`; fixtures under `architecture/fixtures/parameter-checks/` | 003, 004 | CODE-02, -03, -05 |
| Migration `V<seq>__rwb_e1_042_parameter_catalog_and_seed.sql` | `backend/src/main/resources/db/modulemigration/recovery/` | 001, 002, 006 | CODE-16 |
| `ParameterService`, `ParameterValue`, `CatalogEntry`, exceptions, `BusinessDateProvider` (published, `casewf.config.api`) and their implementations | `casewf/config/api/`, `casewf/config/ParameterServiceImpl.java`, `ParameterValues.java`, `InterimBusinessDateProvider.java`, `CatalogSource.java` | 005, 007, 008, 010, 023, 024 | CODE-10, -17, -18, -20 |
| Per-instance version cache | `casewf/config/ParameterCache.java` | 009, 018 | CODE-19 |
| Readiness indicator `parameterCatalog` | `casewf/config/ParameterStartupCheck.java`; `application.yaml` readiness group | 016 | CODE-22 |
| `GET /admin/parameters` | `casewf/config/ParameterCatalogController.java`, `CatalogParameterView.java` | 011, 020, 025 | CODE-21 |
| Load / approve / rollback / find (`ParameterLoadHandler`) | `casewf/config/api/ParameterLoadHandler.java`, `ParameterLoadResult.java`, `ParameterVersionApproved.java`; `casewf/config/ParameterLoadHandlerImpl.java`, `ParameterLoadValidator.java`, `ParameterContentHash.java`, `ParameterValidity.java`, `ParameterValueEntity.java`, `ParameterValueRepository.java`, `CsvRows.java`, `ParameterSchemaLimits.java` | 012–015, 017 | CODE-01, -24..-28, -30 |
| Decision-record seam (interim) and rollback event | `casewf/config/VersionDecisionRecorder.java`, `InterimVersionDecisionRecorder.java`, `ParameterLoadRolledBack.java` | 019, 027 | CODE-29 |
| P4 seams: `MessageResolver`, `CapabilityCheck`, `CatalogParameterReader` (D-RUN-19); additive `ApiProblemException` constructor and its rendering | `access/api/`; `access/internal/FixedMessageCatalog.java`, `InterimCapabilityCheck.java`, `ProblemFactory.java`, `ApiExceptionHandler.java`; `backend/src/main/resources/access/interim-capability-grants.csv` | 020, 022, 025, 026 | CODE-12..-15 |
| `CatalogParameterReader` implementation | `casewf/config/CatalogParameterReaderImpl.java` | 023, 026 | CODE-23 |
| Module map and published surface | `casewf/config/package-info.java`, `casewf/config/api/package-info.java` (`@NamedInterface(name = "config.api", propagate = false)`), `backend/src/test/resources/architecture/recovery-modules.yaml` | 026 | CODE-09 |
| Feature flag `rwb.p3.configservice` | `application.yaml` (default `false`), `application-local.yaml` (`true`) | 021 | CODE-30 |

Java paths are under `backend/src/main/java/th/co/scb/ace/demo/recovery/` unless they start with
`backend/src/test`. No controller for the load operations, no screen, no frontend file, no new
dependency and no change to the OpenAPI file is part of the delta.

## 2. The endpoint `GET /admin/parameters`

**DOC ID:** DOC-RWB-E1-042-002 · **Maps to:** SPEC-RWB-E1-042-010, -011, -020, -023, -025; AC9; BR6; X7, X9; FL10; CON1; TASK-16, TASK-17; CODE-21; TC-09, TC-24, TC-31, TC-34; TC-12 (Blocked); APT-GETPARAM-001..006

| Item | Value |
|---|---|
| Path | `GET /api/recovery/v1/admin/parameters` (API Specification v4 `getAdminParameters`; `x-module` P3) |
| Registered when | `rwb.p3.configservice=true` (`@ConditionalOnProperty`); otherwise absent and the path answers 404 |
| Method check | `@PreAuthorize("@capabilityCheck.require(authentication, 'Rules and parameters', 'R', 'read parameters')")` |
| Query parameters (all optional) | `key` (prefix), `kind` (`BUSINESS`/`ENVIRONMENT`, case-insensitive), `owner` (exact `owner_role`), `environment` (DEV, SIT, UAT, PROD; default the running `rwb.environment`) |
| Business date | `BusinessDateProvider.today()`; interim: today's date in Asia/Bangkok (SPEC-023) |
| Success | 200, JSON array of `Parameter` (API v4): `key, kind, type, unit, min, max, default, scope, required, owner, environments[], usedBy[], secret, valueInForce, versionNo, validFrom`. Absent values are omitted, not sent as `null` |

**Response rules.**

- One element per catalog row, from the generated keys (never from `parameter_catalog`, SPEC-005).
- `valueInForce`, `versionNo` and `validFrom` are the `APPROVED` row in force on the business date for
  the requested environment; with none in force the catalog default is shown with `versionNo` 0 and no
  `validFrom`. `CODE_LIST` values are rendered comma-joined.
- **Secret rows** (`secret=true`, for example `ace.db.password`): listed with owner, environments and
  used-by; `default`, `valueInForce`, `versionNo` and `validFrom` are absent (SPEC-010, AC9).
- **PRODUCT rows** (for example `ENTRY_DPD`): listed with no value (product values are RWB-E1-045's).

**Errors.**

| Status | When | Body |
|---|---|---|
| 401 | No token, or a token with no RW- role (inherited `SecurityConfig`) | `MSG-P4-001` |
| 403 | Caller lacks Rules and parameters R | `MSG-P4-002`, action text "read parameters" |
| 404 | Flag off (controller not registered) | Spring Boot's empty 404 |
| 422 | `environment` outside DEV/SIT/UAT/PROD, refused **before any read** (SEC-042-01; DEV-14) | `MSG-GEN-002`, `field=environment`, `min=DEV`, `max=PROD`. **Not declared in API v4** (DG-E042-ENV-422) |
| 503 | Data source unreachable (`DataAccessResourceFailureException`, `CannotCreateTransactionException`) | Status-only Problem: `type urn:rwb:problem:unavailable`, `title`, `status`, `traceId`; **no** `messageCode`, no `detail`, no driver text (SPEC-025, E7, CLAR-019) |

Every error body is an RFC 7807 `Problem` rendered by `access.internal.ApiExceptionHandler`. No access-log
entry is written by this story (RWB-E1-039 owns it, spec §4.3). The live RW-PHONECOL refusal test
(TC-E1-042-12) is **Blocked** until RWB-E1-022 sessions and the RWB-E1-037 matrix exist (OI-E1-042-001);
the seam is tested by TC-24 and APT-GETPARAM-003, which do not close it.

## 3. Reading a parameter

**DOC ID:** DOC-RWB-E1-042-003 · **Maps to:** SPEC-RWB-E1-042-005, -007, -008, -009, -010, -023, -024; AC1, AC8, AC11; BR1, BR5; X10; FL2, FL8, FL9; TASK-16, TASK-17; CODE-10, CODE-17..-20; TC-01, TC-08, TC-11, TC-26, TC-28

Inside P3, code reads with a generated key and its own business date:

```java
ParameterValue<Integer> dpd = parameterService.get(ParameterKeys.CASE_ENTRY_DPD, businessDate);
// dpd.value() == 90, dpd.versionNo() == 1, dpd.validFrom() == 2026-11-02 in PROD (seed)
```

Outside P3 (P1, P2, P4), code uses `access.api.CatalogParameterReader` (see `ARCHITECTURE.md` §3).

| Rule | Behaviour |
|---|---|
| Environment | `rwb.environment` (DEV, SIT, UAT, PROD); each environment resolves independently (AC8) |
| Version in force | The `APPROVED` row for (key, environment, product group NULL) with the latest `valid_from` on or before the business date |
| Nothing in force | The generated default with `versionNo 0`, `validFrom null`; with no default, `ParameterNotInForceException` |
| Future version | Resolved on read from the cached version list, so a version starts on its `valid_from` with no restart (AC11, X10) |
| Secret key | `SecretNotServedException`; a secret is never stored as a value row (DB check) |
| `scope=PRODUCT` key | `ParameterNotInForceException` (RWB-E1-045's `ProductParameterService`) |
| ENV-sourced key (`value_source=ENV`) | Read through Spring `Environment` by the property name in the generated key (`rwb.temporal.target`, `rwb.temporal.namespace`, `rwb.drools.kiebase-cache-max`), `versionNo 0` |
| Types | INTEGER `Integer`, DECIMAL `BigDecimal`, BOOLEAN `Boolean`, DATE `LocalDate`, TIME `LocalTime` (`HH:mm`), DURATION `Duration`, STRING/CODE/JSON `String`, CODE_LIST `List<String>` |
| Cache | Per instance, per (key, environment), the ordered `APPROVED` versions; expires after `config.cache.ttl-seconds` (default 60); expired pairs are evicted on every miss; invalidated after an approval or a rollback commits |

Callers record the returned `versionNo` in their own decision inputs (BR5, FL9); that recording is the
engines' stories', not this one's.

## 4. Loading, approving and rolling back values

**DOC ID:** DOC-RWB-E1-042-004 · **Maps to:** SPEC-RWB-E1-042-012..-015, -017, -019, -027; AC5, AC6, AC7, AC10; BR3, BR4; X4, X5, X6, X8; ST1–ST3; CON2, CON3; TASK-18, TASK-19; CODE-01, CODE-24..-29; TC-05..-07, TC-10, TC-16..-20, TC-23, TC-29, TC-33, TC-35..-40; APT-LOAD-001..003, APT-APPROVE-001..003

There is **no HTTP path for these operations in this story** (D-RUN-10). RWB-E1-043's
`POST /admin/reference-loads` (table `PARAMETER`), `/{loadId}/approve` and `/{loadId}/rollback` will call
the published `casewf.config.api.ParameterLoadHandler` through its `PARAMETER` dispatcher branch
(D-RUN-20; `ARCHITECTURE.md` §4). Until then the interface is exercised in tests only.

```java
ParameterLoadResult load(InputStream csv, LocalDate validFrom, UUID authorUserId);
ParameterLoadResult approve(UUID loadId, UUID approverUserId);
ParameterLoadResult rollback(UUID loadId, String reason, UUID userId);
Optional<ParameterLoadResult> find(UUID loadId);
// ParameterLoadResult(loadId, table "PARAMETER", validFrom, status, rows, repeat)
```

**Load file.** UTF-8 (strict decoder) CSV, header `key,environment,value`, at least one row; RFC 4180
quoting (a `CODE_LIST` value with commas is quoted). Values are at most 400 characters.

**Load checks, in order; the first failure refuses the whole load and writes nothing** (spec §12.5):

| # | Check | Refusal |
|---|---|---|
| 1 | File content and `validFrom` present | 422 `MSG-GEN-001` |
| 2 | UTF-8 CSV, correct header, at least one row | 422 `MSG-GEN-001` `field=file` / `MSG-P1-002` |
| 3 | `validFrom` not before the business date | 422 `MSG-P3-027` |
| 4 | Key in the catalog | 422 `MSG-P1-002` |
| 5 | Key loadable (not secret, not PRODUCT, not ENV-sourced) | 422 `MSG-P1-002` |
| 6 | Environment listed for the key | 422 `MSG-P1-002` |
| 7 | Value not blank | 422 `MSG-GEN-001` |
| 8 | Value parses as the type (AC6: "value is not INTEGER") | 422 `MSG-P1-002` |
| 9 | Value within min..max (AC5: `case.entry.dpd` 400 → min 1 max 365); also ≤ 400 characters | 422 `MSG-GEN-002` / `MSG-P1-002` |
| 10 | No duplicate (key, environment) in the file | 422 `MSG-P1-002` |
| 11 | Identical repeat (same `validFrom` and content hash) of a `VALIDATED` or `APPROVED` load | Existing load returned, `repeat = true`, nothing written |
| 12 | No `APPROVED` row of (key, environment) with `valid_from >= validFrom` | 409 `MSG-P3-027` |

Checks 1–10 run in `ParameterLoadValidator#validate`. Checks 11 and 12 run in
`ParameterLoadHandlerImpl#load` inside its own `REQUIRES_NEW` transaction, after a
`pg_advisory_xact_lock` on `validFrom|contentHash`, in the order 11 then 12 (code-gate CODE-001; DEV-19).
A success writes every row `VALIDATED` with the next version number per (key, environment), the author
and one `load_id`. The content hash is SHA-256 over the rows sorted by key then environment, each
`key|environment|value` (unquoted, trimmed), joined by `\n`. A `ROLLED_BACK` load is not a repeat: the
same content can be loaded again.

**Approve.** All rows must be `VALIDATED`. In one transaction: lock the rows; refuse an author approving
own load (409 `MSG-P7-002`, also enforced by `ck_parameter_value_maker_checker`), an approval after
`validFrom` has passed or onto an approved version on or after it (409 `MSG-P3-027`), an approved or
rolled-back load (409 `MSG-GEN-004`); set `APPROVED`, approver and `approved_at`; recompute `valid_to`;
call `VersionDecisionRecorder.recorded("AC-VERS", "PARAMETER", …)` before commit. A recorder failure
rolls everything back and answers 503 `MSG-P7-003`. A concurrent approval answers 409 `MSG-GEN-004`.
After commit: the cache is invalidated and `ParameterVersionApproved` is published.

**Rollback.** `reason` non-blank, at most 400 characters after trim (else 422 `MSG-GEN-001` `field=reason`).
Only an `APPROVED` load (else 409 `MSG-P3-027` "only an approved load can be rolled back"). Every row
needs an earlier `APPROVED` version of its (key, environment) (else 409 `MSG-P3-015`, nothing changes).
Rows become `ROLLED_BACK` with the reason; `valid_to` is recomputed so the earlier version is in force
again (AC10). The cache is invalidated after commit; other instances see it when their entry expires.

**Unknown `loadId`.** `approve` and `rollback` answer 404 `MSG-P4-003`; `find` returns `Optional.empty()`.

**Status values written:** `VALIDATED`, `APPROVED`, `ROLLED_BACK`. `IN_FORCE`, `SUPERSEDED` and `REFUSED`
are allowed by the check constraint but never written; "in force" is derived from the dates.

**Repeat response (contract gap).** The HTTP status of an identical repeat is not stated in API v4. The
spec decides 201 with the existing body (§11.2) and RWB-E1-043 will render it; this is open as
OI-E1-042-011 (`document-gaps.md`).

## 5. The catalog file, generated keys and build checks

**DOC ID:** DOC-RWB-E1-042-005 · **Maps to:** SPEC-RWB-E1-042-003, -004, -005, -024; AC2, AC3; BR1, BR2, BR6; X1, X2; FL1–FL3; GR1; TASK-01..TASK-07; CODE-02..-08; TC-02, TC-03, TC-21, TC-25..-27, TC-41..-44

**Catalog columns** (spec §7.1): key, kind (`BUSINESS`/`ENVIRONMENT`), value_type, unit, min, max,
default, scope (`GLOBAL`/`PRODUCT`), required, owner_role, environments, used_by (`;`-separated), secret,
value_source (`TABLE`/`ENV`), env_property, description. The 19 rows are listed in spec §12.4; owners and
"used by" are labelled assumptions there.

**Generated keys.** `generateParameterKeys` runs before `compileJava`, validates every row (16 columns, key
pattern, enumerated tokens, `required`/`secret` strictly `true|false`, unique constant names), escapes
string content, and fails naming the row and column on a bad row (SEC-042-02). `ParameterKeys` is the
only catalog metadata Java code reads. `-PparameterCatalog=<path>` points the task at another file for
its negative test (DEV-18); the default path is unchanged.

**Build checks** (JUnit, in the `test` task, so every PR runs them):

| Check | Fails the build on | Test |
|---|---|---|
| `CatalogCompletenessCheck` | A key read in recovery main code that the catalog lacks (`ParameterKeys` constant, `ParameterKey.of`, or the string-literal first argument of `CatalogParameterReader.get`); a reader call whose first argument is not one string literal; a catalog row with no owner, a bad kind/type/scope/range, or no default (PRODUCT, secret and ENV rows are exempt from the default rule only); an ENV row whose property name is credential-bearing | `CatalogCompletenessCheckTest`, `CatalogFileParserTest` |
| `RwbMagicNumberCheck` | A numeric literal other than 0, 1, −1 in recovery main code, or a string literal equal to a non-secret catalog default; each finding names file, line and key(s). Existing literals are in a reviewed baseline; an unlisted literal **or a stale baseline entry** fails (ratchet) | `RwbMagicNumberCheckTest`, `JavaLiteralTokenizerTest`, `MagicNumberScannerTest` |
| Generated-keys parity | `ParameterKeys.all()` differs from the parsed catalog file on any column | `ParameterKeysGenerationTest` |
| Catalog/table drift | After every migration in the folder, `parameter_catalog` differs from `ParameterKeys.all()` on any mirrored column | `ParameterMigrationIT#catalogTableEqualsTheGeneratedKeys` |

The credential-name rule (`CatalogFileParser.CREDENTIAL_WORDS`, case-insensitive) refuses an ENV property
name containing `password`, `passwd`, `secret`, `token`, `credential`, `apikey`, `api-key`, `api_key`,
`privatekey`, `private-key`, `private_key` (spec §7.1's eleven) and, since the review fixes,
`connection-string`, `connectionstring`, `pwd`, `accountkey`, `passphrase`, `sas-token` (SEC-042-03;
DEV-15; spec §7.1 is not updated, `shared-updates.md`).

**Adding a parameter.** Add the row by PR, reviewed by the owner (FL1); add a migration in the same story
that inserts the `parameter_catalog` row and, for a GLOBAL TABLE key with a default, its version-1 value
rows; never edit a merged migration. The drift test fails a catalog change merged without its migration.
A key read with a computed name (for example RWB-E1-037's `rwb.refload.approver.<code>`) is refused by
the literal-only rule until a key family or reader method is specified (CLAR-028).

## 6. Operating notes

**DOC ID:** DOC-RWB-E1-042-006 · **Maps to:** SPEC-RWB-E1-042-009, -016, -021, -025; AC4; BR7; X3; TASK-17, TASK-21; CODE-19, CODE-22, CODE-30; TC-04, TC-22, TC-32, TC-34

| Setting | Where | Default | Effect |
|---|---|---|---|
| `rwb.p3.configservice` (env `RWB_P3_CONFIGSERVICE`) | `application.yaml` | `false` (`true` in the local profile) | Off: `ParameterService` and `CatalogParameterReader` serve generated defaults and ENV values only, with no database read; `GET /admin/parameters` and the `ParameterLoadHandler` bean are absent; readiness checks defaults and ENV only. The application still starts. |
| `rwb.environment` (env `RWB_ENVIRONMENT`) | `application.yaml` | `DEV` | The environment whose values are served |
| `config.cache.ttl-seconds` | Catalog row (TABLE, ENVIRONMENT kind) | 60 | Cross-instance refresh delay after an approval or rollback, until RWB-TE-006's outbox |
| Readiness group | `management.endpoint.health.group.readiness.include: readinessState,parameterCatalog` | — | See below |

**Readiness.** The health indicator `parameterCatalog` is DOWN when a required GLOBAL non-secret key
listed for the running environment has (TABLE) no `APPROVED` value in force on the business date and
no default, or (ENV) an unresolved property. DOWN details carry `messageCode MSG-P3-032` and a list of
`{name, environment}` (shown only to authorised callers, `show-details: when-authorized`); one WARN line
per missing key. The process keeps running and turns UP after a load without a restart (CLAR-012). Every
seeded key has a default, so a seeded `valid_from` in the future never fails readiness.

**Outages.** A database outage on `GET /admin/parameters` answers the status-only 503 (§2). Load,
approve and rollback each run in a transaction of their own, so a failure leaves nothing half-written; a
decision-recorder failure on approval answers 503 `MSG-P7-003` with the rows still `VALIDATED`.

**Deployment note.** The migration must be applied by the recovery Flyway bean before the flag is
switched on in an environment. Switching the flag on with an unmigrated schema would make the endpoint
and the readiness check fail on the first read.

No `OPERATIONS.md` is published: the story adds one flag, one readiness indicator, one TTL setting and one
read endpoint, all described above; it adds no job, queue, schedule, monitor or runbook procedure.

## 7. How a developer runs it

**DOC ID:** DOC-RWB-E1-042-007 · **Maps to:** SPEC-RWB-E1-042-001, -014 (coverage wiring via TASK-21); TASK-20..TASK-24

Set the JVM property in the shell first (RUN-BRIEF "Local stack facts"):

```powershell
$env:JAVA_TOOL_OPTIONS="-Djdk.net.unixdomain.tmpdir=$env:USERPROFILE\.gradle\uds"
```

| Check | Command (from `backend/` unless noted) | Result of record at `25c8f94` |
|---|---|---|
| Unit and build checks | `./gradlew test` | 388 tests, 44 classes, 0 failures, 0 skipped |
| Coverage gate (80% × 4) | `./gradlew test recoveryCoverageVerification` | LINE 91.0%, INSTRUCTION 90.7%, BRANCH 80.9%, METHOD 95.8%; exit 0 |
| Container suite (Docker) | `./gradlew recoveryIntegrationTest` or `./scripts/dev.ps1 it` (repo root) | 59 tests, 5 classes: `ParameterConfigIT` 33 + `$FlagOff` 4, `ParameterMigrationIT` 4, `RecoveryMigrationIT` 12, `RecoveryDatabaseIT` 6 |
| Merge gate | `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/dev.ps1 test` (repo root) | exit 0; Gradle `test` plus `npm run check` (28 Vitest tests, unchanged frontend) |
| API contract tests | `./gradlew --init-script "<repo>/aisdlc/output/INC-003-epic-1-RWB-E1-042/api-tests/api-contract-init.gradle" apiTest --rerun-tasks` | 13 tests (`ParameterApiContractIT` 12 + `$FlagOff` 1), run5 at `25c8f94`, exit 0 |
| Generator negative test | `./gradlew generateParameterKeys -PparameterCatalog=<bad fixture>` | fails `row 2 column 'required' violates true or false` (expected) |

`-ExecutionPolicy Bypass` is needed only because the workstation blocks unsigned scripts. `scripts/dev.ps1
e2e` was not run (it needs `dev.ps1 up`, which the run rules forbid from the worktree).

## 8. Status and gates

**DOC ID:** DOC-RWB-E1-042-008 · **Maps to:** SPEC-RWB-E1-042-001..-027; TASK-22..TASK-25

| Gate or check | Result | Evidence |
|---|---|---|
| Spec gate | **PASS** round 12 (spec revision 13), 0/0/0/0 | `../review/spec-gate-review-12.md` |
| Plan gate | **PASS** round 2, 0/0/0/0; 26 tasks TASK-00..-25 | `../review/plan-gate-review-2.md` |
| Code gate round 1 | **FAIL** 0C/1H/0M/2L at `74e4ccb` (CODE-001 approved-repeat 409; CODE-002, -003 evidence) — all closed | `../review/code-gate-review.md` |
| Code gate round 2 | **FAIL** 0C/0H/0M/3L at `9056ed2` (CODE2-001 missing TC-20/22/23 system cases; CODE2-002 DEV-13 clash; CODE2-003 stale Javadoc) — fixed at `216a696`, `25c8f94` | `../review/code-gate-review-2.md`; `../implement/code-gate-fix/README.md` |
| Code gate round 3 | **FAIL** 0C/0H/0M/1L at `25c8f94` (CODE3-001: six planned test names in `scenarios.md` had no rename note) — fixed by DEV-20 (`../implement/deviations.md`, rename table) | `../review/code-gate-review-3.md` |
| Code gate round 4 | **PASS** 0C/0H/0M/0L at `25c8f94`; CODE3-001 closed by DEV-20 and re-reviewed. Each FAIL round was fixed and re-gated; no finding was accepted. Human sign-off still not recorded (OPEN-016) | `../review/code-gate-review-4.md` |
| Backend unit | 388 passed, 0 failed, 0 skipped | `../implement/code-gate-fix/test-and-coverage-counts.txt`; `../implement/code-gate-fix/round2/dev-test.log` |
| Backend coverage | LINE 2579/2833 = 91.0%, INSTRUCTION 14045/15482 = 90.7%, BRANCH 1289/1594 = 80.9%, METHOD 552/576 = 95.8% (one BUNDLE rule at 0.80) | `../implement/code-gate-fix/round2/recoveryCoverageReport.xml`; `coverage-verification.log` |
| Container | 59 passed, 0 failed, 0 skipped | `../implement/code-gate-fix/round2/it-full.log` |
| API tests | **PASSED** 13/13 (4 APIs, 1 controller), run5 at `25c8f94` | `../api-tests/report.md`; `../api-tests/evidence/apiTest-run5.log` |
| Functional automation | **NOT_APPLICABLE**: UI In Scope NO, 0 components, no frontend diff | `../functional-tests/report.md` |
| Security review | **PASS** after fixes: SEC-042-01..04 (Low) closed; no security review covers the commits after `8e51eb8` (the code gate checked that delta) | `../review/security-review.md` |
| Ponytail review | **Ship** at `74e4ccb` | `../review/ponytail-review.md` |
| TC-E1-042-12 | **Blocked** (OI-E1-042-001); never reported as passed | spec §15 |
| Human review / merge | **Not recorded.** No approver, `AGENTS.md` §9 sign-off, merge, release, SIT or UAT result is claimed (OPEN-016; D-RUN-09) | — |

**Documentation snapshot.** Branch `feature/RWB-E1-042-parameter-catalog`, tip `25c8f94`, merge base
`7bee04d`. The branch file is `V0001__rwb_e1_042_parameter_catalog_and_seed.sql`; that number is the
next free one on `develop-recovery` today and is required by the migration lint's contiguity rule, but
the sequence of record is assigned by the orchestrator at merge (D-RUN-07, D-RCV-28). This documentation
writes it as `V<seq>__…` throughout.

## 9. Documents in this folder

| Document | Purpose |
|---|---|
| `README.md` (this file) | What the service is, the endpoint, reading, loads, catalog and build checks, operating notes, how to run it, status. |
| `ARCHITECTURE.md` | Module placement and published surface, `CatalogParameterReader` (D-RUN-19), the `PARAMETER` dispatcher branch seam (D-RUN-20), the migration, transactions/events/cache, problem rendering and the seams to later stories. |
| `COMPLIANCE.md` | AC, BR and SPEC → TASK → CODE → test trace; coverage; reviews; DEV-01..DEV-20; open items with no approval claimed. |
| `assumptions.md` | Documentation-stage assumptions (`A-DOC-E042-*`). |
| `shared-updates.md` | Rows this stage would add to the shared registers; the stage writes none of them. |
| `document-gaps.md` | Document-gap candidates carried or found at documentation (no `DG-nnn` assigned). |

### DOC ID index

| DOC ID | Where | Maps to |
|---|---|---|
| DOC-RWB-E1-042-001 | README §0–1 | SPEC-001..-027; AC1–AC11; BR1–BR7; TASK-00..-25; CODE-01..-30 |
| DOC-RWB-E1-042-002 | README §2 | SPEC-010, -011, -020, -023, -025; AC9; X7, X9; TASK-16, -17; CODE-21; TC-09, -12, -24, -31, -34 |
| DOC-RWB-E1-042-003 | README §3 | SPEC-005, -007..-010, -023, -024; AC1, AC8, AC11; BR1, BR5; TASK-16, -17; CODE-10, -17..-20 |
| DOC-RWB-E1-042-004 | README §4 | SPEC-012..-015, -017, -019, -027; AC5–AC7, AC10; BR3, BR4; TASK-18, -19; CODE-01, -24..-29 |
| DOC-RWB-E1-042-005 | README §5 | SPEC-003..-005, -024; AC2, AC3; BR1, BR2, BR6; TASK-01..-07; CODE-02..-08 |
| DOC-RWB-E1-042-006 | README §6 | SPEC-009, -016, -021, -025; AC4; BR7; TASK-17, -21; CODE-19, -22, -30 |
| DOC-RWB-E1-042-007 | README §7 | SPEC-001, -014; TASK-20..-24 |
| DOC-RWB-E1-042-008 | README §8 | SPEC-001..-027; TASK-22..-25 |
| DOC-RWB-E1-042-009 | ARCHITECTURE §2 | SPEC-026; GR3; D-RUN-21; TASK-08, -09; CODE-09..-12; TC-45 |
| DOC-RWB-E1-042-010 | ARCHITECTURE §3 | SPEC-003, -023, -026; GR3; D-RUN-19; TASK-04, -05, -16, -17; CODE-05, -12, -23; TC-03, -46 |
| DOC-RWB-E1-042-011 | ARCHITECTURE §4 | SPEC-017, -021; FL5; D-RUN-10, D-RUN-18, D-RUN-20; TASK-19, -20; CODE-11, -28; TC-22 |
| DOC-RWB-E1-042-012 | ARCHITECTURE §5 | SPEC-001, -002, -006; FL4; D-RUN-07, D-RCV-28; TASK-14, -15; CODE-16; TC-13..-15, -27 |
| DOC-RWB-E1-042-013 | ARCHITECTURE §6 | SPEC-009, -013..-015, -018, -019; FL8; TASK-17, -19; CODE-19, -24, -28, -29; TC-10, -16, -20, -28, -29, -33 |
| DOC-RWB-E1-042-014 | ARCHITECTURE §7 | SPEC-020, -022, -025, -027; MSG; AUTH; TASK-10..-13; CODE-13..-15; TC-24, -30, -34 |
| DOC-RWB-E1-042-015 | ARCHITECTURE §8 | SPEC-019, -020, -022, -023; §4.3 seams; TASK-11, -13, -17, -19; CODE-12, -15, -20, -29 |
| DOC-RWB-E1-042-016 | COMPLIANCE §2 | AC1–AC11; TC-01..-11; TASK-14..-20 |
| DOC-RWB-E1-042-017 | COMPLIANCE §3 | BR1–BR7; X1–X10; GR1–GR4; TASK-01..-25 |
| DOC-RWB-E1-042-018 | COMPLIANCE §4 | SPEC-001..-027; TASK-00..-25; CODE-01..-30; TC-01..-46 |
| DOC-RWB-E1-042-019 | COMPLIANCE §5 | SPEC-014 (coverage wiring); TASK-21, -22 |
| DOC-RWB-E1-042-020 | COMPLIANCE §6 | TASK-22..-25; CODE-001, CODE2-001..-003; SEC-042-01..-04 |
| DOC-RWB-E1-042-021 | COMPLIANCE §7 | DEV-01..DEV-20; TASK-08..-25 |
| DOC-RWB-E1-042-022 | COMPLIANCE §8 | OI-E1-042-001..-013; OPEN-016, OPEN-050; D-RUN-18..-21; TC-12 |

22 DOC IDs. `document-gaps.md`, `assumptions.md` and `shared-updates.md` carry no DOC ID.
