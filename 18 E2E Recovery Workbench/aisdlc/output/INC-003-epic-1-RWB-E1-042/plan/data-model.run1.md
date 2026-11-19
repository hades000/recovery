---
title: "Data model: RWB-E1-042"
run_id: "INC-003-epic-1-RWB-E1-042"
revision: "v1 (18 Nov 2026): first data model for this run, matching plan.md v1 and specify/spec.md revision 13."
---

# Data model: RWB-E1-042

Two persisted tables in schema `recovery`, three added columns, one migration, one catalog file and one grants file. The catalog file is the single source of parameter metadata; `parameter_catalog` is its persisted mirror for the foreign key, Physical Schema v6 and SQL consumers, and **no Java code reads it** (SPEC-005, A-29). No field of this story holds customer data; author, approver and audit user IDs are staff identifiers and are treated as personal (SPEC-027).

Sources: Physical Schema v6 lines 1386-1409 (`parameter_catalog`), 1412-1434 (`parameter_value`), 1206-1225 (`outbox_event`); spec §7.1, §7.2, §7.3, §12.3 to §12.7; Decision Log v10 D-RCV-28; RWB-E1-044 plan v1 (migration conventions).

## 1. Migration file

| Item | Value |
|---|---|
| Path | `backend/src/main/resources/db/modulemigration/recovery/V<seq>__rwb_e1_042_parameter_catalog_and_seed.sql` |
| Name | `V<seq>__rwb_e1_042_parameter_catalog_and_seed.sql`; `<seq>` is the next free four-digit number at merge, assigned by the orchestrator (D-RUN-07, D-RCV-28). **No number is fixed** |
| Line 1 | `-- Story: RWB-E1-042` |
| Line 2 | `-- Parameter catalog and seed for RWB-E1-042 (spec SPEC-001, -002, -006); columns from Physical Schema v6; D-RCV-28.` |
| Qualifier | `${recoverySchema}` only. No `SET search_path`, no `GRANT`, no `REVOKE`, no literal `recovery.`, `ace.` or `public.` |
| Guarding | Every `CREATE TABLE`, `ADD COLUMN`, constraint and index is guarded, so the file applies both on an empty schema and on a schema built from Physical Schema v6 (SPEC-001) |
| Shape | One file for the story: DDL and seed together (D-RCV-28, `E1042-RV-DG-01`) |
| Forward only | Never edited after merge; a later fix takes the next sequence, keeps the key and adds `-- Fix: <reason>` |

Statement groups, in order:

1. `CREATE TABLE IF NOT EXISTS ${recoverySchema}.parameter_catalog` and `… .parameter_value`, columns exactly as Physical Schema v6 (see §4).
2. `ALTER TABLE ${recoverySchema}.parameter_value ADD COLUMN IF NOT EXISTS` for `load_id uuid`, `content_hash char(64)` and `rollback_reason varchar(400)`.
3. Guarded constraint additions: a `DO` block per constraint testing `pg_constraint` by name in `${recoverySchema}`.
4. `CREATE [UNIQUE] INDEX IF NOT EXISTS` for the four indexes of §4.
5. `COMMENT ON TABLE` and `COMMENT ON COLUMN` for both tables and the three added columns.
6. The 19 catalog rows: `INSERT … ON CONFLICT (param_key) DO NOTHING`.
7. The 40 value rows: one per GLOBAL, non-secret, `value_source=TABLE` key with a default, per listed environment, with `INSERT … SELECT … WHERE NOT EXISTS` on `(param_key, environment, product_group)`.
8. The self-check `DO` block: raises an exception when a required GLOBAL non-secret row with a default lacks an approved value for a listed environment; restricted to rows with `default_value IS NOT NULL`, so `temporal.target` (ENV, no default) does not fail it.

## 2. Catalog file `backend/src/main/resources/config/parameter-catalog.csv`

Header exactly: `key,kind,value_type,unit,min_value,max_value,default_value,scope,required,owner_role,environments,used_by,secret,value_source,env_property,description`.

The first 13 columns and `description` come from the 10 Nov pack; `value_source` and `env_property` are added (A-03). A field holding a comma or a quote is quoted per RFC 4180. `used_by` uses `;` between entries (finding 130, A-35).

| # | key | kind | value_type | unit | min | max | default_value | scope | required | owner_role | used_by | secret | value_source | env_property |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `case.entry.dpd` | BUSINESS | INTEGER | CALENDAR_DAYS | 1 | 365 | `90` | GLOBAL | true | RW-COE | `recovery.casewf.casecreation` | false | TABLE | |
| 2 | `refdata.cache.ttl-seconds` | ENVIRONMENT | INTEGER | SECONDS | | | `300` | GLOBAL | true | RW-PLATADM | `recovery.casewf.refdata` | false | TABLE | |
| 3 | `config.cache.ttl-seconds` | ENVIRONMENT | INTEGER | SECONDS | | | `60` | GLOBAL | false | RW-PLATADM | `recovery.casewf.config` | false | TABLE | |
| 4 | `caselist.export.maxrows` | BUSINESS | INTEGER | COUNT | | | `10000` | GLOBAL | false | RW-COE | `recovery.casewf.caselist` | false | TABLE | |
| 5 | `ace.db.password` | ENVIRONMENT | STRING | | | | | GLOBAL | false | RW-PLATADM | `ACE common module` | true | SECRET | |
| 6 | `recon.caselist.tolerance.pct` | BUSINESS | DECIMAL | PERCENT | | | `0.00` | GLOBAL | false | RW-COE | `recovery.dataengine.caselist` | false | TABLE | |
| 7 | `caselist.allocation.wait.until` | BUSINESS | TIME | TIME_OF_DAY | | | `07:15` | GLOBAL | false | RW-COE | `recovery.casewf.caselist` | false | TABLE | |
| 8 | `servicelevel.required-statuses` | BUSINESS | CODE_LIST | | | | `"NEW,ASSIGNED,IN_PROGRESS,WAITING_CUSTOMER,WAITING_PARTNER,WAITING_APPROVAL"` | GLOBAL | true | RW-COE | `recovery.casewf.refdata.product` | false | TABLE | |
| 9 | `ENTRY_DPD` | BUSINESS | INTEGER | DAYS | | | | PRODUCT | true | RW-PRODHEAD | `recovery.casewf.casecreation; recovery.casewf.allocation` | false | TABLE | |
| 10 | `EXCLUSION_LIST` | BUSINESS | CODE_LIST | | | | | PRODUCT | true | RW-PRODHEAD | `recovery.casewf.casecreation; recovery.casewf.allocation` | false | TABLE | |
| 11 | `NOTICE_PERIOD_DAYS` | BUSINESS | INTEGER | DAYS | 1 | 365 | | PRODUCT | true | RW-PRODHEAD | `recovery.casewf.timers` | false | TABLE | |
| 12 | `CURE_PERIOD_DAYS` | BUSINESS | INTEGER | DAYS | | | | PRODUCT | true | RW-PRODHEAD | `recovery.casewf.timers` | false | TABLE | |
| 13 | `EXPOSURE_BAND_SET` | BUSINESS | CODE_LIST | | | | | PRODUCT | true | RW-PRODHEAD | `recovery.casewf.allocation` | false | TABLE | |
| 14 | `temporal.target` | ENVIRONMENT | STRING | | | | | GLOBAL | true | RW-PLATADM | `recovery.casewf.workflow (RWB-E1-070, RWB-E1-071)` | false | ENV | `rwb.temporal.target` |
| 15 | `temporal.namespace` | ENVIRONMENT | STRING | | | | `rwb-recovery` | GLOBAL | false | RW-PLATADM | `recovery.casewf.workflow (RWB-E1-070, RWB-E1-071)` | false | ENV | `rwb.temporal.namespace` |
| 16 | `temporal.taskqueue.platform` | ENVIRONMENT | STRING | | | | `rwb-platform` | GLOBAL | false | RW-PLATADM | `recovery.casewf.workflow (RWB-E1-070, RWB-E1-071)` | false | TABLE | |
| 17 | `temporal.retention.days` | ENVIRONMENT | INTEGER | DAYS | | | `30` | GLOBAL | false | RW-PLATADM | `recovery.casewf.workflow (RWB-E1-070, RWB-E1-071); RWB-E2-039` | false | TABLE | |
| 18 | `drools.kiebase.cache.max` | ENVIRONMENT | INTEGER | COUNT | | | `20` | GLOBAL | false | RW-PLATADM | `recovery.casewf.rules (RWB-E1-072)` | false | ENV | `rwb.drools.kiebase-cache-max` |
| 19 | `rules.testcases.min` | BUSINESS | INTEGER | COUNT | | | `50` | GLOBAL | false | RW-COE | `RWB-E1-073` | false | TABLE | |

All rows list `DEV,SIT,UAT,PROD`. `description` is required by §7.1 but no source gives its text; the plan writes one short line per row derived from the key name and its source column in spec §12.4, adding no business rule, and the owner may reword it in review (`PA-E1-042-06`, gap `PG-E1042-01`).

Ten rows are GLOBAL, non-secret, `value_source=TABLE` **with a default** (1, 2, 3, 4, 6, 7, 8, 16, 17, 19) and give the 40 seeded value rows. `temporal.namespace` and `drools.kiebase.cache.max` are ENV with a default: the default is documentation for the property, and no value row is seeded for them.

## 3. Key model (generated, `casewf.config.api`)

`ParameterKey<T>` is immutable and carries every catalog column. Constant names are the key upper-cased with `.` and `-` replaced by `_` (`CASE_ENTRY_DPD`, `RULES_TESTCASES_MIN`).

| Accessor | Type | From the catalog | Notes |
|---|---|---|---|
| `name()` | `String` | `key` | |
| `kind()` | `Kind` (`BUSINESS`, `ENVIRONMENT`) | `kind` | |
| `type()` | `Class<T>` | `value_type` | INTEGER `Integer`, DECIMAL `BigDecimal`, BOOLEAN `Boolean`, DATE `LocalDate`, TIME `LocalTime`, DURATION `Duration`, CODE_LIST `List<String>` (unchecked cast at the single construction point), STRING/CODE/JSON `String` |
| `unit()` | `String` | `unit` | empty when absent |
| `min()`, `max()` | `String` | `min_value`, `max_value` | raw text, empty when absent; compared after conversion |
| `defaultValue()` | `String` | `default_value` | raw text, `null` when absent; converted by `ParameterValues` |
| `scope()` | `Scope` (`GLOBAL`, `PRODUCT`) | `scope` | |
| `required()` | `boolean` | `required` | |
| `ownerRole()` | `String` | `owner_role` | |
| `environments()` | `List<String>` | `environments` | immutable, in file order |
| `usedBy()` | `List<String>` | `used_by` | split on `;` and trimmed |
| `secret()` | `boolean` | `secret` | |
| `valueSource()` | `ValueSource` (`TABLE`, `ENV`, `SECRET`) | `value_source` | generated only, not a DB column |
| `envProperty()` | `String` | `env_property` | `null` when absent |
| `description()` | `String` | `description` | |

`static <T> ParameterKey<T> of(String name, Class<T> type)` builds an ad-hoc key with no metadata, for fixture modules and the completeness check's `ParameterKey.of` rule. Production code reads only the generated constants.

`ParameterKeys` (generated) adds `static List<ParameterKey<?>> all()` (file order, immutable) and `static <T> Optional<ParameterKey<T>> byName(String key, Class<T> type)` (empty when absent or the type differs).

**One converter.** `ParameterValues.convert(ParameterKey<?>, String)` in `casewf.config` turns catalog text into the typed value and is the only place conversion lives: `ParameterServiceImpl`, `ParameterLoadValidator` and `ParameterStartupCheck` all call it, so the load check and the read path cannot disagree about a value.

## 4. Tables

### 4.1 `parameter_catalog` (columns as Physical Schema v6 lines 1386-1409)

| Column | Type | Constraint | Notes |
|---|---|---|---|
| `id` | `uuid` | PK, default `gen_random_uuid()` | |
| `param_key` | `varchar(100)` | NOT NULL, `uk_parameter_catalog UNIQUE (param_key)` | the catalog `key` |
| `kind` | `varchar(20)` | NOT NULL, `ck_parameter_catalog_kind` (BUSINESS, ENVIRONMENT) | |
| `value_type` | `varchar(20)` | NOT NULL, `ck_parameter_catalog_value_type` (STRING, INTEGER, DECIMAL, BOOLEAN, DATE, TIME, DURATION, CODE, CODE_LIST, JSON) | |
| `unit` | `varchar(20)` | | |
| `min_value`, `max_value` | `varchar(100)` | | raw catalog text |
| `default_value` | `varchar(400)` | `ck_parameter_catalog_secret_default` (a secret has no default) | |
| `scope` | `varchar(20)` | NOT NULL, `ck_parameter_catalog_scope` (GLOBAL, PRODUCT) | |
| `required` | `boolean` | NOT NULL | |
| `owner_role` | `varchar(50)` | NOT NULL | an RW- role code |
| `environments` | `varchar(100)` | NOT NULL, `ck_parameter_catalog_environments` (comma list of DEV, SIT, UAT, PROD) | |
| `used_by` | `varchar(400)` | NOT NULL | stored exactly as written |
| `secret` | `boolean` | NOT NULL | |
| `description` | `varchar(400)` | | |
| `created_at`, `updated_at` | `timestamptz` | NOT NULL, default `now()` | |
| `created_by`, `updated_by` | `uuid` | | seeded rows: the seed identity; personal by the protective reading (SPEC-027) |
| `version` | `bigint` | NOT NULL, default 0 | optimistic lock; written by migrations only |

Written by migrations only, never at run time. Editable through the API: none.

### 4.2 `parameter_value` (columns as Physical Schema v6 lines 1412-1434, plus the three added)

| Column | Type | Constraint | Load | Approve | Rollback |
|---|---|---|---|---|---|
| `id` | `uuid` | PK, default `gen_random_uuid()` | generated | — | — |
| `param_key` | `varchar(100)` | NOT NULL, `fk_parameter_value_catalog` → `parameter_catalog.param_key` | CSV `key` | — | — |
| `environment` | `varchar(10)` | NOT NULL, `ck_parameter_value_environment` (DEV, SIT, UAT, PROD) | CSV `environment` | — | — |
| `param_value` | `varchar(400)` | NOT NULL | CSV `value`, trimmed, unquoted | — | — |
| `product_group` | `varchar(50)` | | NULL (PARAMETER loads are GLOBAL) | — | — |
| `version_no` | `integer` | NOT NULL, `ck_parameter_value_version` (>= 1) | max over all statuses for `(key, environment, product_group NULL)` + 1 | — | — |
| `valid_from` | `date` | NOT NULL, `ck_parameter_value_dates` (`valid_to` NULL or >= `valid_from`) | `validFrom` | — | — |
| `valid_to` | `date` | | NULL | recomputed (§5.3) | recomputed |
| `status` | `varchar(20)` | NOT NULL, `ck_parameter_value_status` (VALIDATED, APPROVED, IN_FORCE, SUPERSEDED, ROLLED_BACK, REFUSED) | `VALIDATED` | `APPROVED` | `ROLLED_BACK` |
| `author_user_id` | `uuid` | NOT NULL; personal (DF-REF-156) | author | — | — |
| `approver_user_id` | `uuid` | `ck_parameter_value_maker_checker` (NULL or <> author); personal (DF-REF-157) | NULL | approver | — |
| `approved_at` | `timestamptz` | `ck_parameter_value_approved_at` (APPROVED and IN_FORCE need it) | NULL | `now()` | unchanged |
| `load_id` | `uuid` | `ix_parameter_value_load`; NULL only for seeded rows | one UUID per load | — | — |
| `content_hash` | `char(64)` | `ck_parameter_value_load_hash` (`(load_id IS NULL) = (content_hash IS NULL)`, `^[0-9a-f]{64}$`) | SHA-256 of the load | — | — |
| `rollback_reason` | `varchar(400)` | `ck_parameter_value_rollback_reason` (ROLLED_BACK needs one) | NULL | NULL | `reason` |
| `created_at` | `timestamptz` | NOT NULL, default `now()` | default | — | — |
| `created_by` | `uuid` | | author user ID; seed: the seed identity; personal (protective reading) | — | — |
| `is_active` | `boolean` | NOT NULL, default true | true | unchanged | unchanged |
| `state` | `varchar(20)` | | NULL | NULL | NULL |
| `version` | `bigint` | NOT NULL, default 0 | 0 | +1 | +1 |
| `updated_at` | `timestamptz` | | default | `now()` | `now()` |
| `updated_by` | `uuid` | | author | approver | rollback caller; personal (protective reading) |

`is_active` is never changed and never read by this story; "in force" comes only from `status` and the dates. `state` is unused (`status` is the lifecycle column).

### 4.3 Constraints and indexes added by the migration

`uk_parameter_catalog (param_key)`, `ck_parameter_catalog_scope`, `ck_parameter_catalog_kind`, `ck_parameter_catalog_value_type`, `ck_parameter_catalog_environments`, `ck_parameter_catalog_secret_default`, `uk_parameter_value` (as Physical Schema v6 defines it), `ck_parameter_value_environment`, `ck_parameter_value_status`, `ck_parameter_value_dates`, `ck_parameter_value_version`, `ck_parameter_value_maker_checker`, `ck_parameter_value_approved_at`, `ck_parameter_value_load_hash`, `ck_parameter_value_rollback_reason`, `fk_parameter_value_catalog`.

| Index | Definition | Purpose |
|---|---|---|
| `ix_parameter_value_in_force` | `(param_key, environment, valid_from) WHERE status = 'APPROVED'` | the read and the cache |
| `ix_parameter_value_load` | `(load_id)` | approve, rollback, find |
| `ux_parameter_value_version_all` | `UNIQUE (param_key, environment, COALESCE(product_group,'*'), version_no)` | the version number, because v6's `uk_parameter_value` treats NULL product groups as distinct |
| `ux_parameter_value_approved_from` | `UNIQUE (param_key, environment, COALESCE(product_group,'*'), valid_from) WHERE status IN ('APPROVED','IN_FORCE')` | one approved version per start date |

The pack's `ix_parameter_value_lookup` is not carried (product values are RWB-E1-045's).

### 4.4 Seeded rows

| Item | Value |
|---|---|
| Catalog rows | 19, one per §2 row, `INSERT … ON CONFLICT (param_key) DO NOTHING` |
| Value rows | 40: the ten GLOBAL, non-secret, TABLE rows with a default, one per environment |
| `version_no` | 1 |
| `status` | `APPROVED` |
| `valid_from` | `2026-11-02` (A-04) |
| `author_user_id`, `created_by` | `00000000-0000-0000-0000-0000000e1042` (synthetic seed identity, not a person; A-05) |
| `approver_user_id` | NULL (the baseline is approved by the reviewed catalog PR) |
| `approved_at` | `now()` at migration time |
| `load_id`, `content_hash` | NULL (only a load carries them) |
| `is_active`, `state` | `true`, NULL |
| `created_at` | the migration time |

No value row exists for `ace.db.password`, for a PRODUCT key or for an ENV key.

## 5. Load model

### 5.1 Load file

UTF-8 CSV per RFC 4180, parsed by the same `CsvRows` reader as the catalog file. Header exactly `key,environment,value`; at least one data row. A field holding a comma, a quote or a line break is quoted, as CODE_LIST values such as `servicelevel.required-statuses` need.

### 5.2 The twelve checks, in order; the first failure refuses the whole load

| # | Check | Refusal |
|---|---|---|
| 1 | file content and `validFrom` present | 422 `MSG-GEN-001` `{field}` |
| 2 | CSV with the exact header and at least one row | 422 `MSG-GEN-001` `{field}=file` / `MSG-P1-002` `{check}="file is not a CSV with header key,environment,value"` |
| 3 | `validFrom` not before `BusinessDateProvider.today()` | 422 `MSG-P3-027` `{table}=PARAMETER, {check}="valid from is before the business date"` |
| 4 | key in the catalog (a `ParameterKeys.byName` hit) | 422 `MSG-P1-002` `{check}="key <k> is not in the catalog"` |
| 5 | key loadable: not secret, not PRODUCT, not ENV | 422 `MSG-P1-002` `{check}="key <k> cannot be loaded as a value"` |
| 6 | environment listed for the key | 422 `MSG-P1-002` `{check}="environment <e> is not listed for <k>"` |
| 7 | value not blank | 422 `MSG-GEN-001` `{field}="value of <k>"` |
| 8 | value parses as the type | 422 `MSG-P1-002` `{check}="value is not <TYPE>"` |
| 9 | value within `min..max` | 422 `MSG-GEN-002` `{field}=<k>, {min}, {max}` |
| 10 | no duplicate `(key, environment)` in the file | 422 `MSG-P1-002` `{check}="duplicate row for <k> <e>"` |
| 11 | identical repeat (the hash matches a `VALIDATED` or `APPROVED` load) | existing load, `repeat = true`, nothing written |
| 12 | no `APPROVED` row of `(key, environment)` with `valid_from >= validFrom` | 409 `MSG-P3-027` `{check}="an approved version from <date> exists for <k> <e>"` |

All refusals are `access.api.ApiProblemException` with status, message ID, placeholders and `field`; `detail` is always null (the load refuses on the first failure).

### 5.3 Canonical form, hash and validity

- Value stored as loaded, trimmed, after RFC 4180 unquoting.
- Hash input: the rows sorted by key, then environment, each line `key|environment|value`, joined with `\n`, UTF-8, SHA-256, lower-case hex. Stored in `parameter_value.content_hash` on every row of the load.
- Idempotency key `(PARAMETER, validFrom, content_hash)`.
- `valid_to` recomputation after every approval or rollback, per affected `(key, environment, product_group NULL)`: order the `APPROVED` rows by `valid_from`; each row's `valid_to` is the next row's `valid_from` minus one day; the last row's `valid_to` is NULL. Rows in other statuses keep NULL.
- `load`, `approve` and `rollback` each run in their own `REQUIRES_NEW` transaction through `TransactionTemplate`; `find` is `PROPAGATION_SUPPORTS`. The load's unique-violation catch sits outside the rolled-back transaction and re-reads in a second read-only transaction.

## 6. Event and result models

| Type | Fields | Published |
|---|---|---|
| `ParameterLoadResult` | `UUID loadId`, `String table` = `PARAMETER`, `LocalDate validFrom`, `String status`, `int rows`, `boolean repeat` | returned by the handler; maps to API v4 `ReferenceLoad` on RWB-E1-043's side |
| `ParameterVersionApproved` (published, `casewf.config.api`) | `UUID loadId`, `List<String> paramKeys`, `LocalDate validFrom`, `List<Version{String paramKey, String environment, int versionNo}> versions`, `java.time.Instant occurredAt` | in-process application event after commit; no approver ID |
| `ParameterLoadRolledBack` (package-private, `casewf.config`) | `UUID loadId`, `List<String> paramKeys`, `LocalDate validFrom` | in-process event inside the rollback transaction, handled `AFTER_COMMIT` |
| `CatalogEntry` (published) | `String key`, `String kind`, `String type`, `String unit`, `String min`, `String max`, `String defaultValue`, `String scope`, `boolean required`, `String owner`, `List<String> environments`, `List<String> usedBy`, `boolean secret` | returned by `ParameterService.entry(String)` |

`repeat` has no field in API v4 `ReferenceLoad`; the flag stays internal until the API owner records it (`OI-E1-042-011`; gap `PG-E1042-02`).

## 7. Message catalog (`access.internal.FixedMessageCatalog`)

Nine IDs, each in EN and TH, copied verbatim from Error and Message Standard v4 at the line the spec names. No text is restated in this plan, because the Standard is the source of record and the Thai text is "Proposed" until DL10 approves it.

| ID | Used for | Placeholders | Standard v4 line |
|---|---|---|---|
| `MSG-P3-032` | readiness: required parameter missing | `name`, `environment` | 156 |
| `MSG-GEN-002` | value out of range | `field`, `min`, `max` | 69 |
| `MSG-P1-002` | load refused at a check | `source`, `date`, `check` | 76 |
| `MSG-GEN-001` | required input empty | `field` | 68 |
| `MSG-P7-002` | approver is the author | none | 207 |
| `MSG-P3-015` | no earlier version to roll back to | `table` | 139 |
| `MSG-P3-027` | load check failed; nothing in force | `table`, `check` | 151 |
| `MSG-GEN-004` | concurrent change | none | 71 |
| `MSG-P7-003` | approval not taken: the decision could not be recorded | none | 208 |

`MSG-P4-001`, `MSG-P4-002`, `MSG-P4-003` and `MSG-P3-036` stay in `ApiError` and are not duplicated here. `MSG-GEN-006` is **not** used: its text promises a retry neither the approval nor the read makes.

## 8. Build-check fixture corpus (`backend/src/test/resources/architecture/fixtures/parameter-checks/`)

Not compiled. `main/` holds Java sources the completeness and literal checks read; `catalog/` holds CSV files the parser and the row rules read; `baseline/` holds baseline files for the ratchet cases.

| Folder or file | Content | Case |
|---|---|---|
| `main/recovery/casewf/casecreation/EntryRule.java` | `int threshold = 90;` in a method | AC2, X1, TC-02 |
| `main/recovery/dataengine/caselist/ToleranceReader.java` | A field, a constructor parameter, a static call, a non-literal key, a method reference and a `var` local, one per method, with `allocation.retry.limit` or `config.cache.ttl-seconds` | TC-03 (b) to (f), (h) |
| `main/recovery/casewf/config/CatalogParameterReaderImpl.java` | A non-literal reader call (the path exemption) | TC-03 (i) |
| `main/recovery/casewf/caselist/LimitsReader.java` | A `Map<String, Integer>` and an `Optional` with `get(...)` on each | TC-03 (g) |
| `main/recovery/casewf/caselist/OtherReads.java` | A `ParameterKey.of("allocation.retry.limit", Integer.class)` call | TC-03 (a) |
| `catalog/product-row.csv` | A PRODUCT row with no default and a full owner, type and range | TC-21 pass |
| `catalog/product-row-no-owner.csv` | The same row without `owner_role` | TC-21 fail |
| `catalog/used-by-broken.csv` | `a;;b`, `a;`, `;a`, blank, 101 characters, a line break — one row each | TC-41 (b) |
| `catalog/env-credential.csv` | Eight ENV rows with credential-bearing `env_property` values and two clean ones | TC-44 |
| `catalog/drift.csv` | The real catalog with one default changed | TC-27 |
| `baseline/stale.csv` | A baseline entry for a literal no longer present | TC-25 |
| `baseline/valid.csv` | A baseline entry that matches | TC-25 |

No fixture holds personal data, a credential or a production value. `main/` sources are never compiled.

## 9. Interim capability grants (`backend/src/main/resources/access/interim-capability-grants.csv`)

Header `role,area,rights`. One row per RW- role of Users, Roles and Permissions v4 lines 76-110 with that role's "Rules and parameters" rights, area written exactly `Rules and parameters`. The spec names RW-COE `CRUD`, RW-RISK `RA`, RW-REFADM `R`, RW-PLATADM `R`, RW-TRIBE `R`, RW-AUDIT `R` and RW-PHONECOL none; the Builder reads the remaining rows from the matrix. `rights` is a letter set; `require` tests membership of the requested right; an empty `rights` cell means no right. RWB-E1-037 replaces the implementation and deletes this file.

## 10. Personal data and synthetic data

| Field | Classification | Handling |
|---|---|---|
| `parameter_value.author_user_id`, `approver_user_id` | staff identifier, personal "Yes" (Inventory v4 DF-REF-156, -157) | stored and passed to `VersionDecisionRecorder` only; never logged, published, returned or put in an exception message |
| `parameter_value.created_by`, `updated_by`; `parameter_catalog.created_by`, `updated_by` | personal by the protective reading (no Inventory row; the same columns elsewhere are personal) | as above; never logged |
| rollback caller (the `updated_by` of a rolled-back row) | personal by the same reading | as above |
| `param_value`, `default_value`, `description`, `used_by`, `env_property` | not personal | no customer value, no credential, no account number; `ace.db.password` is a key name, never a value |

Every test user ID is a synthetic UUID generated for the test. No real name, ID number, account number, address or production value appears in the catalog, the fixtures, the seed or this data model.
