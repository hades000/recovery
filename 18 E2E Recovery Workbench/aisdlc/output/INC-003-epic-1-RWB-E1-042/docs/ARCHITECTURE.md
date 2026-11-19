---
title: "RWB-E1-042 Central configuration service and parameter catalog — architecture"
run_id: "INC-003-epic-1-RWB-E1-042"
story: "RWB-E1-042"
stage: "docs (final documentation)"
date: "2026-11-18"
status: "DOCUMENTED against branch tip 25c8f94"
---

# Architecture — configuration service and parameter catalog

Sections 2–8 carry `DOC-RWB-E1-042-009`..`-015`; §1 is their shared context.

## 1. Context

| Fact | Value | Source |
|---|---|---|
| Service | ACE service, recovery module, one repository and one front end | AGENTS.md §2 |
| Story module | P3 Case and workflow, `th.co.scb.ace.demo.recovery.casewf.config`; published `casewf.config.api` | story v7 §13; RWB-TE-001 spec v4 SPEC-022, SU-08 (a) |
| P4 additions | `access.api.MessageResolver`, `CapabilityCheck`, `CatalogParameterReader` (+ nested `Value`); additive `ApiProblemException` constructor; rendering in `access.internal` | SU-08 (c), (d); D-RUN-19 |
| Tables | `${recoverySchema}.parameter_catalog`, `${recoverySchema}.parameter_value` (Physical Schema v6 lines 1386–1434, plus three columns) | SPEC-002 |
| Dependency direction | P3 may depend on P2 and P4, never the reverse; P1, P2 and P4 never import `casewf.config` | TE1S SPEC-022 (d); SU-14 |
| "One module" | Read as the ACE module (recovery): the P3 + P4 change does not go back to the analyst | D-RUN-21 (orchestrator decision, **unratified**, OPEN-050) |
| Flag | `rwb.p3.configservice`, default `false` | SPEC-021 |

```text
                 build time                                   run time
 parameter-catalog.csv ──► generateParameterKeys ──► ParameterKeys (casewf.config.api)
        │                                                  │
        ├── CatalogCompletenessCheck / RwbMagicNumberCheck │ (only metadata source)
        │                                                  ▼
        └── migration V<seq> ──► parameter_catalog    ParameterServiceImpl ◄── ParameterCache ◄── parameter_value
                                 parameter_value  ▲        ▲         ▲                                 ▲
                                                  │        │         └── CatalogParameterReaderImpl ◄── P1/P2/P4 callers
                                                  │        └── ParameterCatalogController (GET /admin/parameters)
                                                  │        └── ParameterStartupCheck (readiness)
                                                  └── ParameterLoadHandlerImpl ◄── RWB-E1-043 PARAMETER branch (later)
```

## 2. Module placement and published surface

**DOC ID:** DOC-RWB-E1-042-009 · **Maps to:** SPEC-RWB-E1-042-026; GR3; CON5; D-RUN-21; TASK-08, TASK-09; CODE-09..CODE-12; TC-45; DEV-02..DEV-05, DEV-07

**`casewf.config.api`** (declared by `package-info.java` with
`@NamedInterface(name = "config.api", propagate = false)`, listed as `config.api` under `casewf` in
`backend/src/test/resources/architecture/recovery-modules.yaml`) publishes eleven types:
`ParameterService`, `ParameterValue`, `ParameterKey`, `ParameterKeys` (generated), `CatalogEntry`,
`ParameterNotInForceException`, `SecretNotServedException`, `BusinessDateProvider`,
`ParameterLoadHandler`, `ParameterLoadResult`, `ParameterVersionApproved` (plus the nested record
`ParameterVersionApproved$Version`, DEV-03).

**`access.api`** gains exactly three types, `MessageResolver`, `CapabilityCheck` and
`CatalogParameterReader` (plus `CatalogParameterReader$Value`), and one additive constructor on the
existing `ApiProblemException`.

Everything else is package-private in `casewf.config` or `access.internal`. `RecoveryBoundaryTest#publishedSurfaceIsExactlyTheSpecifiedTypes`
asserts the exact set, so any additional public type fails the build (TC-45); `ModulithTest` asserts the
module edges.

Framework constraints that shaped this (recorded deviations, none weakens an assertion):

- `casewf/config/package-info.java` carries **no** `@ApplicationModule`: with it, Spring Modulith 2.1.1
  registers a nested module and rejects its legal P3 → P4 edges (DEV-02).
- Spring Modulith 2.1.1 does not surface a `@NamedInterface` two package levels down, so the boundary
  test reads `config.api` from the module map and the `package-info.java` (DEV-04; OI-E1-042-013).
- `ParameterKey` metadata accessors `kind()`, `scope()`, `valueSource()` return catalog tokens as
  `String`, not public enums, to keep the published surface at eleven types (DEV-07).
- There is **no** JPA entity or repository for `parameter_catalog`: no Java code reads that table
  (SPEC-005; DEV-01). The generated keys are the only catalog metadata at run time.

## 3. `CatalogParameterReader` — the P4 read interface (D-RUN-19)

**DOC ID:** DOC-RWB-E1-042-010 · **Maps to:** SPEC-RWB-E1-042-003, -023, -026; GR3; D-RUN-19; TASK-04, TASK-05, TASK-16, TASK-17; CODE-05, CODE-12, CODE-23; TC-03, TC-46

**Why it exists.** P1 (for example RWB-E1-011, `recon.tolerance.pct`) and P4 (RWB-E1-037,
`rwb.refload.approver.*`) need parameters, but may not depend on P3 (TE1S SPEC-022 (d)). Orchestrator
decision **D-RUN-19** (build log, 2026-11-18T05:10:44; **not ratified**, OPEN-050, CLAR-027) places a read
interface in P4 `access.api` and implements it in P3. P3 callers keep using `ParameterService`.

```java
// th.co.scb.ace.demo.recovery.access.api
public interface CatalogParameterReader {
    <T> Value<T> get(String key, Class<T> type, LocalDate businessDate);  // caller holds a business date (e.g. P1 batch)
    <T> Value<T> get(String key, Class<T> type);                          // business date from BusinessDateProvider (e.g. P4)
    record Value<T>(String key, T value, int versionNo, LocalDate validFrom, String environment) {}
}
```

| Aspect | Behaviour |
|---|---|
| Implementation | `casewf.config.CatalogParameterReaderImpl`, package-private, **always registered** whatever the flag; delegates only to `ParameterService`; logs nothing, caches nothing of its own (uses the SPEC-009 cache) |
| Scope | GLOBAL values for the running environment, same resolution as `ParameterService.get` (approved row in force, else default with `versionNo 0`) |
| Flag off | Serves generated defaults and ENV values only (asserted by `ParameterConfigIT$FlagOff#theReaderStillServesTheDefault`) |
| Errors (JDK types only, so callers need no P3 type) | unknown key or wrong type → `IllegalArgumentException`; `scope=PRODUCT` → `IllegalArgumentException`; `secret=true` → `IllegalStateException`; nothing in force and no default → `NoSuchElementException`. The message holds the key only |
| Build rule | `CatalogCompletenessCheck` treats the first argument of a reader call as a key read: it must be one string literal naming a catalogued key; a non-literal argument, a `::` reference, a `var` alias or a doubly-typed name fails the build naming file and line. `CatalogParameterReaderImpl` is exempt by path (§12.11) |
| Evidence | `CatalogParameterReaderImplTest` (8 tests, TC-46); `CatalogCompletenessCheckTest` reader-call cases (TC-03); the P1 fixture `fixtures/parameter-checks/main/recovery/dataengine/caselist/ToleranceReader.java` |

**Limitation.** A computed key such as `rwb.refload.approver.<code>` cannot pass the literal-only rule.
RWB-E1-037 must specify a key family or a dedicated reader method (CLAR-028); nothing is decided here.

## 4. The `PARAMETER` dispatcher branch seam (D-RUN-20) and the flag-off contract

**DOC ID:** DOC-RWB-E1-042-011 · **Maps to:** SPEC-RWB-E1-042-017, -021; FL5; CON2, CON3; D-RUN-10, D-RUN-11, D-RUN-18, D-RUN-20; TASK-19, TASK-20; CODE-11, CODE-28; TC-22

**Ownership.** RWB-E1-043 (Build Sequence order 8) owns the shared reference-load endpoint and its
dispatch by table code (D-RUN-10, D-RUN-11). D-RUN-18 publishes a reference-load handler SPI in P4
`access.api` for handlers **outside** P3. **D-RUN-20** (build log, 2026-11-18T05:34:56; orchestrator
decision, **not ratified**, OPEN-050) settles that `PARAMETER`, which is P3's, is **not** an SPI handler:

```text
RWB-E1-043 dispatcher ─┬─ table = PARAMETER ──► ParameterLoadBranch (casewf.refdata.internal, P3, RWB-E1-043)
                       │                          └─ ObjectProvider<ParameterLoadHandler>.getIfAvailable()
                       │                               ├─ present ─► ParameterLoadHandler.load/approve/rollback/find
                       │                               └─ absent  ─► 404 MSG-P4-003, nothing written
                       └─ other tables ──► P4 access.api SPI handlers (RWB-E1-043's registry)
```

| Rule | What this story guarantees |
|---|---|
| Branch name | `ParameterLoadHandler.TABLE = "PARAMETER"` |
| No SPI bean | `ParameterLoadHandlerImpl` implements no `access.api` type (asserted: `ParameterConfigIT$FlagOff#theHandlerImplementsNoAccessApiType`); RWB-E1-043 makes a `PARAMETER` SPI bean fail start-up |
| No new edge | The branch sits in P3 and calls `casewf.config.api` inside P3 |
| Errors | Every refusal is an `access.api.ApiProblemException` with status, message ID, placeholders and field; the branch renders it unchanged |
| Transactions | Each method runs in its own transaction (`REQUIRES_NEW`), so the endpoint gets a committed result or an exception |
| Flag off | `ParameterLoadHandlerImpl` is `@ConditionalOnProperty(rwb.p3.configservice=true)`; no bean of `casewf.config` depends on it; consumers obtain it only through `ObjectProvider` and refuse `PARAMETER` with 404 `MSG-P4-003` |
| Proof here | A **test-only** stand-in `ParameterConfigIT.TestBeans.ParameterLoadBranch` with the same shape: `#flagOnLoadsThroughTheAdapter` (delegates, returns the handler's `loadId`) and `$FlagOff#flagOffStillStartsAndRefusesParameterLoads` (404 `MSG-P4-003`, nothing written). Added in code-gate round 2 (CODE2-001) |

The real `ParameterLoadBranch`, the multipart parsing, the C/A/U capability checks and the HTTP success
status are RWB-E1-043's (E43S SPEC-018, -026, -030; TC-PB-01, TC-FL-01). Out of scope here.

## 5. The migration `V<seq>__rwb_e1_042_parameter_catalog_and_seed.sql`

**DOC ID:** DOC-RWB-E1-042-012 · **Maps to:** SPEC-RWB-E1-042-001, -002, -006; FL4; PRE-1, PRE-6; D-RUN-07, D-RUN-13, D-RCV-28; TASK-14, TASK-15; CODE-16; TC-13, TC-14, TC-15, TC-27

| Item | Value |
|---|---|
| Name | `V<seq>__rwb_e1_042_parameter_catalog_and_seed.sql`. `<seq>` is the next free four-digit number **in merge order**, assigned by the orchestrator at merge (D-RUN-07, D-RCV-28). On the branch the file is `V0001__…` because the lint requires a contiguous sequence from `V0001` and the folder held only `README.md`; renumber at merge if another migration lands first |
| Folder | `backend/src/main/resources/db/modulemigration/recovery/` (recovery Flyway bean, history table `flyway_schema_history_recovery`) |
| Line 1 | `-- Story: RWB-E1-042` |
| Count | The story's only migration; DDL and seed in one file; 381 lines |
| Schema | Only `${recoverySchema}` qualifies objects; no `SET search_path`, no `GRANT`/`REVOKE`, no `public.` reference. `recovery.` text appears only inside quoted `used_by` and `COMMENT ON` literals, which the RWB-E1-044 lint ignores (D-RUN-13) |
| Idempotent DDL | Every statement is guarded, so it runs on an empty schema **and** on a schema already built from Physical Schema v6 (local init with `RWB_LOAD_REFERENCE_SCHEMA=true`) |

**Statements, in order.**

1. `CREATE TABLE IF NOT EXISTS` `parameter_catalog` and `parameter_value`, columns exactly as Physical
   Schema v6 (type, width, nullability, default, order).
2. `ALTER TABLE parameter_value ADD COLUMN IF NOT EXISTS load_id uuid, content_hash char(64),
   rollback_reason varchar(400)` (pack option A; OI-E1-042-008; Physical Schema update requested).
3. Guarded constraints (`DO` blocks testing `pg_constraint` by name): `uk_parameter_catalog`,
   `ck_parameter_catalog_scope`, `_kind`, `_value_type`, `_environments`, `_secret_default` (a secret has
   no default); `uk_parameter_value`, `ck_parameter_value_environment`, `_status`, `_dates`, `_version`,
   `_maker_checker` (approver NULL or ≠ author), `_approved_at`, `_load_hash`
   (`(load_id IS NULL) = (content_hash IS NULL)`, hex 64), `_rollback_reason`; FK
   `fk_parameter_value_catalog`.
4. Indexes: `ix_parameter_value_in_force` (partial, `APPROVED`), `ix_parameter_value_load`,
   `ux_parameter_value_version_all` (NULL product group as `'*'`), `ux_parameter_value_approved_from`
   (partial, `APPROVED`/`IN_FORCE`; its violation is the concurrent-approval 409).
5. `COMMENT ON` tables and columns.
6. 19 catalog rows, `INSERT … ON CONFLICT (param_key) DO NOTHING`.
7. 40 value rows (10 GLOBAL, non-secret, TABLE keys with a default × 4 environments): version 1,
   `APPROVED`, `valid_from 2026-11-02`, author = synthetic seed identity
   `00000000-0000-0000-0000-0000000e1042`, approver NULL, `load_id` NULL; `WHERE NOT EXISTS` guarded.
8. Self-check `DO` block: raises if a required GLOBAL non-secret row **with a default** lacks an approved
   value for a listed environment.

**Privileges.** No GRANT: `recovery_svc` receives DML through the default privileges for `rwb_migrator`
objects (`infra/postgres/init/20-grants.sql.inc`).

**Rules for later changes.** A merged migration is never edited (AGENTS §4.6). A changed default or a
new key needs a new migration in the story that changes the catalog file; the drift test (TC-27) fails
otherwise. A changed default never changes an approved value row; only a load does (BR3).

**Evidence.** `ParameterMigrationIT` (4 tests): `#emptySchemaGetsTablesConstraintsIndexesAndSeed`
(TC-13, every v6 column), `#physicalSchemaSixGetsTheAdditions` (TC-14),
`#catalogTableEqualsTheGeneratedKeys` (TC-27), `#theSeedIdentityIsSynthetic`;
`RecoveryMigrationLintTest#migrationsFollowTheRecoveryRules` (TC-15, RWB-E1-044's lint, unchanged).

## 6. Transactions, events and the cache

**DOC ID:** DOC-RWB-E1-042-013 · **Maps to:** SPEC-RWB-E1-042-009, -013, -014, -015, -018, -019; FL8; TASK-17, TASK-19; CODE-19, CODE-24, CODE-28, CODE-29; TC-10, TC-16, TC-20, TC-28, TC-29, TC-33; DEV-08, DEV-13, DEV-19

| Operation | Transaction | Concurrency guard | After commit |
|---|---|---|---|
| `load` | `TransactionTemplate`, `PROPAGATION_REQUIRES_NEW`; checks 1–10 before, 11–12 and the inserts inside | `pg_advisory_xact_lock(hashtext(validFrom + "\|" + contentHash))` (native query, PostgreSQL-only, bound parameter; DEV-13) serialises identical loads; a unique violation is re-read in a separate read-only transaction and answered as a repeat, else 409 `MSG-GEN-004` | — |
| `approve` | `REQUIRES_NEW`: lock rows → checks → `APPROVED` → recompute `valid_to` → `VersionDecisionRecorder.recorded(...)` (joins with `MANDATORY`) | `SELECT … FOR UPDATE` (`@Lock(PESSIMISTIC_WRITE)`), `version` column, `ux_parameter_value_approved_from`; a 23505 on that index is 409 `MSG-GEN-004`, any other integrity failure is not | Cache invalidated, then `ParameterVersionApproved` published (SEC-042-04) |
| `rollback` | `REQUIRES_NEW`: lock rows → checks → `ROLLED_BACK` + reason → recompute `valid_to` | row lock, `version` | Cache invalidated; `ParameterLoadRolledBack` is published **inside** the transaction (DG-E042-ROLLBACK-EVENT) |
| `find` | Repository read, no write | — | — |

**Why a transaction synchronization, not `@TransactionalEventListener`.** Spring Modulith's persistent
event-publication registry is triggered by `@TransactionalEventListener` and writes
`recovery.event_publication`, a table Physical Schema v6 does not have and this story may not create
outside its one migration. The handler therefore registers its own `afterCommit` synchronization for the
cache invalidation and the approval event (DEV-08; DG-E1042-IM-01; OI-E1-042-012). Behaviour matches the
spec: rebuild only after commit, none on a refusal, none on a failed commit (TC-10 (b), TC-28, TC-29).

**Event `ParameterVersionApproved`** (published, in-process only; outbox is RWB-TE-006's):
`loadId`, `paramKeys[]`, `validFrom`, `versions[{paramKey, environment, versionNo}]`, `occurredAt`. No
approver ID, no personal data. Not yet in Event and Messaging Design v4 (update requested, CLAR-016).

**Cache.** `ParameterCache` holds per (key, environment) the ordered `APPROVED` versions, resolves the
date on read, expires entries after `config.cache.ttl-seconds` and evicts expired pairs on every miss.
It never holds `VALIDATED` or `ROLLED_BACK` rows or secrets. Other instances converge within the TTL.

## 7. Problem rendering, messages and the capability seam

**DOC ID:** DOC-RWB-E1-042-014 · **Maps to:** SPEC-RWB-E1-042-020, -022, -025, -027; MSG; AUTH; X9; TASK-10..TASK-13; CODE-13..CODE-15; TC-24, TC-30, TC-34; DEV-06, DEV-09

**`ApiProblemException`** (`access.api`) gains
`ApiProblemException(HttpStatus status, String messageId, Map<String,String> placeholders, String field, String detail, Throwable cause)`
with `status()`, `messageId()`, `field()`, `detail()`; `error()` is null for this form. Guards: `status`
required; `messageId` null only for 503, and then no placeholders, field or detail. P3 code raises it and
never calls `ProblemFactory`.

**`ApiExceptionHandler.problem`** keeps its `ApiError` branch; for the new form it calls
`ProblemFactory`: with a message ID → `type urn:rwb:problem:<id>`, `title`, `status`, `detail` (override or
EN text), `messageCode`, `messageTh`, `field`, `traceId`; without → the status-only 503. It logs one WARN
line: message ID (or `none`), status, `traceId`, cause class and the fixed text "cause suppressed"; never
the cause message, stack trace, placeholders, field value or detail (D-RUN-15). It takes
`ObjectProvider<MessageResolver>` so the inherited `SecurityConfigTest` slice still starts (DEV-06).

**`MessageResolver`** (`access.api`) with the interim `FixedMessageCatalog` (`access.internal`) holds EN
and TH text from Error and Message Standard v4 for `MSG-P3-032`, `MSG-GEN-001`, `-002`, `-004`,
`MSG-P1-002`, `MSG-P7-002`, `-003`, `MSG-P3-015`, `-027` (the `MSG-P4-*` IDs are existing `ApiError`
constants). A message-table story swaps the implementation (OI-E1-042-004).

**`CapabilityCheck`** (`access.api`): `has(auth, area, right)` and `require(auth, area, right, action)`,
which returns true or throws `ApiProblemException(ApiError.NOT_PERMITTED, {action})` → 403 `MSG-P4-002`
with the action text. Interim implementation `InterimCapabilityCheck`, bean name **`capabilityCheck`**
(the SpEL expression depends on it), reads `backend/src/main/resources/access/interim-capability-grants.csv`
(`role,area,rights`, the Rules and parameters column of Users, Roles and Permissions v4; for example
RW-COE CRUD, RW-PHONECOL none). `ParameterCatalogControllerTest` runs the real `@PreAuthorize` seam
(DEV-09).

## 8. Seams to later stories

**DOC ID:** DOC-RWB-E1-042-015 · **Maps to:** SPEC-RWB-E1-042-019, -020, -022, -023; spec §4.3; D-RUN-08; TASK-11, TASK-13, TASK-17, TASK-19; CODE-12, CODE-15, CODE-20, CODE-29

| Seam | Built now | Filled by | Without changing callers |
|---|---|---|---|
| Reference-load endpoint, dispatch, C/A/U rights | `ParameterLoadHandler` (no controller) | RWB-E1-043 (order 8) | §4 |
| Decision log `AC-VERS` | `VersionDecisionRecorder` (package-private port), interim one-line log with no user ID, `Propagation.MANDATORY` | RWB-E1-027 writer (a new implementation in `casewf.config` calling P7 `DecisionLogWriter`) | yes |
| Outbox for `ParameterVersionApproved` (and the rollback event) | In-process event, TTL refresh | RWB-TE-006 | yes; the rollback event must then move after commit (DG-E042-ROLLBACK-EVENT) |
| Permission matrix, sessions | `CapabilityCheck` + grants file | RWB-E1-037 (keeps bean name `capabilityCheck`, deletes the file), RWB-E1-022 | yes; then TC-E1-042-12 runs |
| ACE business date (`v_ace_batch_status`) | `BusinessDateProvider`, interim Asia/Bangkok date | The story reading that view (P3 → P1 read, allowed under D-RUN-18) | yes |
| Message table | `MessageResolver` + `FixedMessageCatalog` | Unowned (OI-E1-042-004) | yes |
| Flag table with removal date | `rwb.p3.configservice` property | RWB-E1-047 | yes |
| Access-log entry for `GET /admin/parameters` | Nothing | RWB-E1-039 | yes |
| Product values | PRODUCT rows only; loads refused | RWB-E1-045 `ProductParameterService` | yes |
| Temporal / Drools reads | ENV catalog rows for the existing properties | RWB-E1-071, RWB-E1-072 | yes |
