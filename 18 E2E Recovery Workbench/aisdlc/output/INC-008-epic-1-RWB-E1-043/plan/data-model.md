---
title: "Data model: RWB-E1-043 Reference data service with versioned tables"
run_id: "INC-008-epic-1-RWB-E1-043"
revision: "v1 (18 Nov 2026): first plan-stage data model. Version and row tables re-derived column for column from Physical Schema v6 lines 1437-1483; the E1-042 parameter catalog dependency and the 38 added rows from RWB-E1-042 plan v2 data-model sections 2, 4, 7 and 9; the 37 Reference data grant rows from Users, Roles and Permissions v4 lines 73-110. Remediation run 2 (18 Nov 2026): PLAN-001 (catalog CSV comparison moved to TASK-15), PLAN-003 (`V<seq>` for RWB-E1-001) and PLAN-007 (statement groups aligned with `plan.md` and TASK-02) fixed; no data-model content added or removed."
---

# Data model: RWB-E1-043

Two persisted tables in schema `recovery` (`reference_version`, `reference_row`), their append-only triggers, one migration and the 38 `parameter_catalog` rows this story adds. The version and row tables already exist in Physical Schema v6; this story creates them on an empty schema and corrects the one constraint that makes AC1 impossible, so the migration gives one end state on an empty schema and on a PS6 schema (SPEC-001). No `reference_version` or `reference_row` row is seeded: versions are loaded through the endpoint.

Sources: Physical Schema v6 lines 1437-1483 (the two `CREATE TABLE` blocks), 2228-2249 (foreign keys), 2334-2347 (indexes), 3179-3204 (column comments), 3595-3596 (`sys_objects`), 4348-4373 (`sys_fields` DF-REF-159..184); Data Dictionary v8 DF-REF-159..184, DF-REF-028/029, DF-REF-163/164, DF-WRK-038/051/052; story file v7 RWB-E1-043 v2 sections 12 and 13; spec revision 10 SPEC-001, -003, -006, -011, -024, -025, -027, -029, -032; RWB-E1-042 plan v2 `data-model.md` sections 2, 4, 7 and 9; Users, Roles and Permissions v4 lines 73-110; Decision Log v10 D-RCV-28; RWB-E1-044 plan v2 migration conventions.

## 1. Migration file

| Item | Value |
|---|---|
| Path | `backend/src/main/resources/db/modulemigration/recovery/V<seq>__rwb_e1_043_reference_versions.sql` |
| Name | `V<seq>__rwb_e1_043_reference_versions.sql`; `<seq>` is the next free four-digit number at merge, assigned by the orchestrator (D-RUN-07, D-RCV-28). **No number is fixed** |
| Line 1 | `-- Story: RWB-E1-043` |
| Line 2 | `-- Reference version and row tables, append-only guards and 38 parameter catalog rows for RWB-E1-043 (SPEC-001, -029); columns from Physical Schema v6; D-RCV-28.` |
| Qualifier | `${recoverySchema}` only. No `SET search_path`, no `GRANT`, no `REVOKE`, no literal `recovery.`, `ace.` or `public.` outside a string literal |
| Guarding | Every `CREATE TABLE`, `DROP CONSTRAINT`, constraint, index, function and trigger is guarded or `IF NOT EXISTS`, so the file applies on an empty schema and on a schema built from Physical Schema v6 |
| Shape | One file for the story: DDL, triggers and the 38 catalog rows together (D-RCV-28) |
| Forward only | Never edited after merge; a later correction takes the next sequence, keeps `rwb_e1_043` and adds line 2 `-- Fix: <reason>` |

Statement groups, in order:

1. `CREATE TABLE IF NOT EXISTS ${recoverySchema}.reference_version` with the 29 columns of section 3 and `CONSTRAINT uk_reference_version UNIQUE (table_code, version_no)`.
2. `CREATE TABLE IF NOT EXISTS ${recoverySchema}.reference_row` with the 11 columns of section 4 and **no** `uk_reference_row`.
3. `ALTER TABLE ${recoverySchema}.reference_row DROP CONSTRAINT IF EXISTS uk_reference_row` (for a PS6 baseline) and a guarded `DO` block adding `uk_reference_row_version (version_id, row_key)`.
4. Guarded `DO` blocks adding `uk_reference_version_from_hash (table_code, valid_from, content_hash)`, `ck_reference_version_maker_checker`, `ck_reference_version_rollback_reason` and `fk_reference_row_version_id` by name; `CREATE UNIQUE INDEX IF NOT EXISTS ux_reference_version_approved_from` on `(table_code, valid_from) WHERE status = 'APPROVED'`; `CREATE INDEX IF NOT EXISTS ix_reference_version_load_id`; `CREATE INDEX IF NOT EXISTS ix_reference_row_version_id`.
5. `CREATE OR REPLACE FUNCTION ${recoverySchema}.reference_version_append_only()` and `reference_row_append_only()`; `DROP TRIGGER IF EXISTS` then `CREATE TRIGGER` (`BEFORE UPDATE OR DELETE`) on each table.
6. The 38 `parameter_catalog` rows of section 7, `INSERT ... ON CONFLICT (param_key) DO NOTHING`; **no** `parameter_value` row.
7. `COMMENT ON TABLE` and `COMMENT ON COLUMN` only for the story's own meaning; no literal schema.
8. A `DO` self-check: the 38 keys exist, every `rwb.refload.loader.*` and `rwb.refload.approver.*` row is `value_type=CODE_LIST`, `required=false`, `owner_role='RW-RISK'`, and the 12 `refdata.columns.*` rows are `STRING` with `default_value='none'`; raises otherwise.

The migration does not create `parameter_catalog` or `parameter_value` (RWB-E1-042's migration, order 3) and does not touch `lov_value` (RWB-E1-001, order 9; the PS6 local load provides it, GAP-32). It seeds no `reference_version` or `reference_row` row.

## 2. `reference_version` (exact Physical Schema v6, lines 1437-1468)

Column order, type, width, nullability and default are Physical Schema v6's; the `CREATE TABLE IF NOT EXISTS` uses this list verbatim. `reference_version` has 29 columns.

| # | Column | Type | Null | Default | Notes |
|---|---|---|---|---|---|
| 1 | `id` | `uuid` | NOT NULL | `gen_random_uuid()` | PRIMARY KEY |
| 2 | `table_code` | `varchar(30)` | NOT NULL | - | the code as supplied; `uk_reference_version (table_code, version_no)` |
| 3 | `version_no` | `integer` | NOT NULL | - | max + 1 per table under the advisory lock |
| 4 | `version_label` | `varchar(20)` | NULL | - | not written by this story |
| 5 | `valid_from` | `date` | NOT NULL | - | the version's effective date |
| 6 | `valid_to` | `date` | NULL | - | next APPROVED `valid_from` - 1 day, or NULL |
| 7 | `status` | `varchar(15)` | NOT NULL | `'VALIDATED'` | VALIDATED, APPROVED, ROLLED_BACK only |
| 8 | `author_user_id` | `uuid` | NOT NULL | - | staff identifier, personal by the protective reading (DF-REF-166) |
| 9 | `approver_user_id` | `uuid` | NULL | - | staff identifier, personal (DF-REF-167); never the author |
| 10 | `approved_at` | `timestamptz` | NULL | - | set on approval, Asia/Bangkok clock |
| 11 | `row_count` | `integer` | NOT NULL | - | data rows written |
| 12 | `content_hash` | `char(64)` | NOT NULL | - | lower-case hex SHA-256 |
| 13 | `load_id` | `uuid` | NOT NULL | - | the HTTP call's new UUID; the response `id` |
| 14 | `dry_run_counts` | `jsonb` | NULL | - | not written by this story |
| 15 | `rollback_reason` | `varchar(400)` | NULL | - | required when ROLLED_BACK |
| 16 | `change_request_ref` | `varchar(30)` | NULL | - | not written by this story |
| 17 | `impact_summary` | `varchar(1000)` | NULL | - | not written by this story |
| 18 | `test_result` | `varchar(10)` | NULL | - | not written by this story |
| 19 | `rollback_plan` | `varchar(1000)` | NULL | - | not written by this story |
| 20 | `verified_by` | `uuid` | NULL | - | frozen until the `/verify` owner adds its columns in its own migration (GAP-11) |
| 21 | `verified_at` | `timestamptz` | NULL | - | as column 20 |
| 22 | `verify_note` | `varchar(1000)` | NULL | - | as column 20 |
| 23 | `is_active` | `boolean` | NOT NULL | `true` | stays true and is never read by resolution (A-33) |
| 24 | `state` | `varchar(40)` | NULL | - | unused; `status` is the lifecycle column |
| 25 | `version` | `integer` | NOT NULL | `1` | optimistic-lock column, `@Version` |
| 26 | `created_at` | `timestamptz` | NOT NULL | `now()` | |
| 27 | `created_by` | `uuid` | NULL | - | the author on a load; personal (protective reading) |
| 28 | `updated_at` | `timestamptz` | NOT NULL | `now()` | set on approve and rollback |
| 29 | `updated_by` | `uuid` | NULL | - | the approver or rollback caller; personal (protective reading) |

Mapped by `ReferenceVersionEntity`: columns 1-13, 15, 23-29; columns 4, 14, 16-22 stay at their defaults or NULL and are not mapped, so this story cannot write them. `version` is the JPA `@Version`; Hibernate starts a new entity at 0 and increments on each update, which the trigger allows.

## 3. `reference_row` (exact Physical Schema v6, lines 1471-1484)

| # | Column | Type | Null | Default | Notes |
|---|---|---|---|---|---|
| 1 | `id` | `uuid` | NOT NULL | `gen_random_uuid()` | PRIMARY KEY |
| 2 | `version_id` | `uuid` | NOT NULL | - | `fk_reference_row_version_id` to `reference_version (id)` ON DELETE RESTRICT |
| 3 | `row_key` | `varchar(200)` | NOT NULL | - | the key columns joined by a vertical bar, or the 6-digit data row number; unique **per version** |
| 4 | `row_data` | `jsonb` | NOT NULL | - | the typed row values as a JSON object |
| 5 | `is_active` | `boolean` | NOT NULL | `true` | never changed |
| 6 | `state` | `varchar(40)` | NULL | - | unused |
| 7 | `version` | `integer` | NOT NULL | `1` | unused; rows are immutable |
| 8 | `created_at` | `timestamptz` | NOT NULL | `now()` | |
| 9 | `created_by` | `uuid` | NULL | - | the author; personal (protective reading) |
| 10 | `updated_at` | `timestamptz` | NOT NULL | `now()` | never changed (no update) |
| 11 | `updated_by` | `uuid` | NULL | - | never set |

Mapped by `ReferenceRowEntity`: columns 1-4 and 8-9; the rest default and are never written. `row_data` is `Map<String,Object>` with `@JdbcTypeCode(SqlTypes.JSON)`, so a `DATE` is an ISO string, an `INTEGER` a JSON number, a `DECIMAL` a JSON number, a `BOOLEAN` a JSON boolean and `STRING`/`CODE` a JSON string.

**The row key is per version, not global.** Physical Schema v6's `CONSTRAINT uk_reference_row UNIQUE (row_key)` would make a second version of any table impossible (GAP-01; AC1). The migration drops it and adds `CONSTRAINT uk_reference_row_version UNIQUE (version_id, row_key)`. The PS6 index `ix_reference_row_version_id` is kept; the FK is added if the table was created empty. `reference_row` has no `valid_from` or `valid_to`: the version's dates govern.

## 4. Constraints, indexes and triggers

| Name | On | Definition | Purpose |
|---|---|---|---|
| `uk_reference_version` | `reference_version` | `UNIQUE (table_code, version_no)` | one version number per table (PS6) |
| `uk_reference_version_from_hash` | `reference_version` | `UNIQUE (table_code, valid_from, content_hash)` | the idempotent repeat (SPEC-006) |
| `ck_reference_version_maker_checker` | `reference_version` | `CHECK (approver_user_id IS NULL OR approver_user_id <> author_user_id)` | S7 BR4 / CTL-08 |
| `ck_reference_version_rollback_reason` | `reference_version` | `CHECK (status <> 'ROLLED_BACK' OR rollback_reason IS NOT NULL)` | S7-019 AC2 |
| `ux_reference_version_approved_from` | `reference_version` | `UNIQUE INDEX (table_code, valid_from) WHERE status = 'APPROVED'` | one approved version per table and date (S7 section 12, A-16) |
| `ix_reference_version_load_id` | `reference_version` | `INDEX (load_id)` | approve, rollback, dispatch by `loadId` |
| `uk_reference_row_version` | `reference_row` | `UNIQUE (version_id, row_key)` | the row key is per version (GAP-01) |
| `fk_reference_row_version_id` | `reference_row` | `FOREIGN KEY (version_id) REFERENCES reference_version (id) ON DELETE RESTRICT` | no orphan row (PS6) |
| `ix_reference_row_version_id` | `reference_row` | `INDEX (version_id)` | rows of a version (PS6) |

Append-only triggers (S7 sections 13 and 17; A-04, A-33; A-34 is the definition grammar):

| Trigger | Fires | Refuses | Allows |
|---|---|---|---|
| `trg_reference_row_append_only` | `BEFORE UPDATE OR DELETE` on `reference_row` | every UPDATE and every DELETE | nothing; a correction is a new version |
| `trg_reference_version_append_only` | `BEFORE UPDATE OR DELETE` on `reference_version` | every DELETE, and any UPDATE that changes `table_code`, `version_no`, `version_label`, `valid_from`, `author_user_id`, `row_count`, `content_hash`, `load_id`, `dry_run_counts`, `change_request_ref`, `impact_summary`, `test_result`, `rollback_plan`, `verified_by`, `verified_at`, `verify_note`, `is_active`, `state`, `created_at` or `created_by` | `status`, `approver_user_id`, `approved_at`, `valid_to`, `rollback_reason`, `version`, `updated_at`, `updated_by` |

The exemption is narrower than S7 section 13's "the standard columns": `is_active`, `state`, `created_at` and `created_by` are frozen (A-33; gate finding 114). The triggers raise with SQLSTATE `23000` (`integrity_constraint_violation`) and a message that names no row content. `reference_version` DELETE is refused although the spec names only the update trigger (A-04). The frozen `verified_*` columns mean the later `/verify` owner must replace the function in its own migration (GAP-11); this story builds no `/verify`.

## 5. Values, keys, hash and check texts

**Statuses.** `VALIDATED`, `APPROVED`, `ROLLED_BACK` only. `IN_FORCE`, `SUPERSEDED` and `REFUSED` (PS6 LOV-VERSION-STATUS) are never written; "in force" is derived as the APPROVED version with the greatest `valid_from` at or before the business date (A-19; SPEC-011). `is_active` is always true and never read.

**`row_key`.** For a handler code, the `keyColumns()` values joined by a vertical bar; if empty, the definition's `K` columns; if neither, the 6-digit data row number (`%06d`). For a built-in, the definition's `K` columns; if none, the 6-digit row number. The maximum is 200 characters (PS6). `row_key` is unique within the version.

**Column definition.** `refdata.columns.<code>` is a STRING parameter, lower-case code with the underscore kept, default `none`. Grammar: `name:TYPE[:R][:K]` items joined by `;`, `TYPE` in `STRING`, `INTEGER`, `DECIMAL`, `BOOLEAN`, `DATE`, `CODE`; `R` = required, `K` = key column, each at most once and in either order; `none` (or a missing key) means no definition. The value must fit `parameter_value.param_value varchar(400)` (GAP-30). A malformed definition is a 422 refusal; it is not silently treated as `none`.

**Content hash.** Rows sorted by `row_key`; each row a JSON object with sorted keys and type-normalised values (`INTEGER` a number, `DECIMAL` a number with trailing zeros stripped, `BOOLEAN` a boolean, `DATE` an ISO string, `STRING`/`CODE` the trimmed text); a value that does not parse to its type is hashed as its trimmed text; rows joined by a newline; UTF-8; lower-case hex SHA-256 (64 characters). The same rows in a different file order give the same hash (SPEC-006; A-13).

**Check texts for `MSG-P3-027 {check}`.** These are the contract; the message ID and the placeholders are the standard's, the wording of the check is the plan's and is asserted verbatim:

| Case | `{check}` text | HTTP |
|---|---|---|
| Unknown table code | `table code is not a reference table` | 422 |
| Built-in with no definition | `no column definition for the table` | 422 |
| Malformed definition | `the column definition is not valid for the table` | 422 |
| File unreadable | `the file cannot be read` | 422 |
| `validFrom` before the business date | `valid from is before the business date` | 422 on load; 409 on approve (A-17) |
| Approved twin with this `validFrom` | `an approved version already has this valid from` | 409 |
| Row key repeated in the file | `row key repeated` | 422 |
| Approve a non-VALIDATED load | `only a validated load can be approved` | 409 |
| Current-state handler before its date | `it can be approved only on its valid from date <validFrom>` | 409 |
| Rollback a non-APPROVED load | `only an approved load can be rolled back` | 409 |
| Rollback not the latest approved | `only the latest approved version can be rolled back` | 409 |
| Handler without rollback | `rollback is not available for this table` | 409 |
| No business date | `no business date` | 503 |
| No earlier approved version | `MSG-P3-015 {table}` | 409 |

`MSG-GEN-001 {field}` is used for a missing `table`, `file`, `validFrom` or `reason` and for a header-only or zero-byte file (`field=rows`). `MSG-P7-002` for the author approving, `MSG-P7-003` for the decision recorder, `MSG-GEN-004` for the optimistic-lock loss or a defect in `apply`/`onRolledBack`, and `MSG-P4-001/002/003` from `ApiError` for 401/403/404. The failure detail for a row check lists every failed row and column, capped at 100 with the total; `{check}` names the first data row (1-based, header excluded) and column, and the Problem `field` is that column (SPEC-003; AC4 "row 12", `limit_days`).

## 6. E1-042 dependency: `parameter_catalog` and `parameter_value`

This story **reads** the catalog through `casewf.config.api.ParameterService` and `ParameterKeys.byName(String, Class<T>)`; it **writes** only the 38 `parameter_catalog` rows in its own migration. It never reads or writes `parameter_value` directly (RWB-E1-042's table); a value that is not in force, or a secret or PRODUCT value, is resolved by E1-042's service, never by this story.

`parameter_catalog` (22 columns; E1-042 data-model section 4.1; Physical Schema v6 lines 1386-1410): `id`, `param_key`, `kind`, `value_type`, `unit`, `min_value`, `max_value`, `default_value`, `scope`, `required`, `owner_role`, `environments`, `used_by`, `secret`, `description`, `is_active`, `state`, `version`, `created_at`, `created_by`, `updated_at`, `updated_by`. The columns this story's seed writes: `param_key`, `kind`, `value_type`, `default_value`, `scope`, `required`, `owner_role`, `environments`, `used_by`, `secret`, `description`; `id`, `is_active`, `version`, `created_at` and `updated_at` take their defaults; `created_by` and `updated_by` stay NULL (the seed is a reviewed file, not a person).

`parameter_value` (19 Physical Schema v6 columns plus E1-042's `load_id`, `content_hash` and `rollback_reason`): not read directly. `ParameterService` returns the value in force for the key and the business date, the catalog default with `versionNo 0` when no value exists, or throws `ParameterNotInForceException`/`SecretNotServedException`. The cache TTL key `refdata.cache.ttl-seconds` is E1-042 row 2 (INTEGER, 300, required, scope GLOBAL, owner RW-PLATADM).

The references this story consumes, exactly (E1-042 spec revision 13 sections 10.1, 10.2, 12.2, 12.4, 12.7, 12.10, 12.12):

| Type | Package | Use |
|---|---|---|
| `ParameterService` | `casewf.config.api` | definitions, loader/approver lists, TTL; no direct table read |
| `ParameterKeys.byName(String, Class<T>)` | `casewf.config.api` (generated) | dynamic key lookup; empty means missing, never a default |
| `ParameterLoadHandler`, `ParameterLoadResult` | `casewf.config.api` | the PARAMETER branch; `load`, `approve`, `rollback`, `find` |
| `BusinessDateProvider` | `casewf.config.api` | the business date for SPEC-005, -008, -024, -032 |
| `CapabilityCheck` | `access.api` | area C/A/U and the action text |
| `MessageResolver` | `access.api` | problem text for the message-ID form |
| `ApiProblemException` | `access.api` | story refusals; 403 uses the `ApiError` form |
| `ApiError` | `access.api` | `NO_ROLE` (401), `NOT_PERMITTED` (403), `NOT_IN_SCOPE` (404) |
| `FixedMessageCatalog` | `access.internal` | the nine IDs of E1-042 data-model section 7 |
| `InterimCapabilityCheck` | `access.internal` | bean `capabilityCheck`, reads the grants CSV |

No E1-042 type is changed. The E1-042 `VersionDecisionRecorder` is package-private and is not called (GAP-50); this story has its own package-private `ReferenceDecisionRecorder` in `casewf.refdata.internal` (A-43).

## 7. `parameter_catalog` rows added by RWB-E1-043 (38)

All rows: `kind=BUSINESS`, `scope=GLOBAL`, `required=false`, `environments=DEV,SIT,UAT,PROD`, `used_by=recovery.casewf.refdata`, `secret=false`, `value_source=TABLE`, `unit`/`min_value`/`max_value` empty, `env_property` empty; `description` is a plan-written one-line text (no source text exists; PG-E1-043-04). The 12 `refdata.columns.*` rows have `value_type=STRING`, `default_value=none`, `owner_role=RW-REFADM`. The 26 list rows have `value_type=CODE_LIST`, `owner_role=RW-RISK`; the `parameter` row differs in its default only.

| # | `param_key` | `value_type` | `default_value` | `owner_role` | Purpose |
|---|---|---|---|---|---|
| 1 | `refdata.columns.product` | STRING | `none` | RW-REFADM | PRODUCT definition |
| 2 | `refdata.columns.region` | STRING | `none` | RW-REFADM | REGION definition |
| 3 | `refdata.columns.exposure_band` | STRING | `none` | RW-REFADM | EXPOSURE_BAND definition |
| 4 | `refdata.columns.role` | STRING | `none` | RW-REFADM | ROLE definition |
| 5 | `refdata.columns.team` | STRING | `none` | RW-REFADM | TEAM definition |
| 6 | `refdata.columns.queue` | STRING | `none` | RW-REFADM | QUEUE definition |
| 7 | `refdata.columns.service_level` | STRING | `none` | RW-REFADM | SERVICE_LEVEL definition |
| 8 | `refdata.columns.document_type` | STRING | `none` | RW-REFADM | DOCUMENT_TYPE definition |
| 9 | `refdata.columns.template` | STRING | `none` | RW-REFADM | TEMPLATE definition |
| 10 | `refdata.columns.delegation_limit` | STRING | `none` | RW-REFADM | DELEGATION_LIMIT definition |
| 11 | `refdata.columns.legal_period` | STRING | `none` | RW-REFADM | LEGAL_PERIOD definition |
| 12 | `refdata.columns.product_parameter` | STRING | `none` | RW-REFADM | PRODUCT_PARAMETER definition |
| 13 | `rwb.refload.loader.product` | CODE_LIST | `RW-REFADM` | RW-RISK | loader list |
| 14 | `rwb.refload.loader.region` | CODE_LIST | `RW-REFADM` | RW-RISK | loader list |
| 15 | `rwb.refload.loader.exposure_band` | CODE_LIST | `RW-REFADM` | RW-RISK | loader list |
| 16 | `rwb.refload.loader.role` | CODE_LIST | `RW-REFADM` | RW-RISK | loader list |
| 17 | `rwb.refload.loader.team` | CODE_LIST | `RW-REFADM` | RW-RISK | loader list |
| 18 | `rwb.refload.loader.queue` | CODE_LIST | `RW-REFADM` | RW-RISK | loader list |
| 19 | `rwb.refload.loader.service_level` | CODE_LIST | `RW-REFADM` | RW-RISK | loader list |
| 20 | `rwb.refload.loader.document_type` | CODE_LIST | `RW-REFADM` | RW-RISK | loader list |
| 21 | `rwb.refload.loader.template` | CODE_LIST | `RW-REFADM` | RW-RISK | loader list |
| 22 | `rwb.refload.loader.delegation_limit` | CODE_LIST | `RW-REFADM` | RW-RISK | loader list |
| 23 | `rwb.refload.loader.legal_period` | CODE_LIST | `RW-REFADM` | RW-RISK | loader list |
| 24 | `rwb.refload.loader.product_parameter` | CODE_LIST | `RW-REFADM` | RW-RISK | loader list |
| 25 | `rwb.refload.loader.parameter` | CODE_LIST | `RW-COE,RW-REFADM` | RW-RISK | PARAMETER loader list |
| 26 | `rwb.refload.approver.product` | CODE_LIST | `RW-RISK` | RW-RISK | approver list |
| 27 | `rwb.refload.approver.region` | CODE_LIST | `RW-RISK` | RW-RISK | approver list |
| 28 | `rwb.refload.approver.exposure_band` | CODE_LIST | `RW-RISK` | RW-RISK | approver list |
| 29 | `rwb.refload.approver.role` | CODE_LIST | `RW-RISK` | RW-RISK | approver list |
| 30 | `rwb.refload.approver.team` | CODE_LIST | `RW-RISK` | RW-RISK | approver list |
| 31 | `rwb.refload.approver.queue` | CODE_LIST | `RW-RISK` | RW-RISK | approver list |
| 32 | `rwb.refload.approver.service_level` | CODE_LIST | `RW-RISK` | RW-RISK | approver list |
| 33 | `rwb.refload.approver.document_type` | CODE_LIST | `RW-RISK` | RW-RISK | approver list |
| 34 | `rwb.refload.approver.template` | CODE_LIST | `RW-RISK` | RW-RISK | approver list |
| 35 | `rwb.refload.approver.delegation_limit` | CODE_LIST | `RW-RISK` | RW-RISK | approver list |
| 36 | `rwb.refload.approver.legal_period` | CODE_LIST | `RW-RISK` | RW-RISK | approver list |
| 37 | `rwb.refload.approver.product_parameter` | CODE_LIST | `RW-RISK` | RW-RISK | approver list |
| 38 | `rwb.refload.approver.parameter` | CODE_LIST | `RW-COE,RW-RISK` | RW-RISK | PARAMETER approver list |

Counts: 12 + 13 + 13 = 38. The same 38 rows go into `config/parameter-catalog.csv` (with the E1-042 16-column header) and into the migration's `INSERT ... ON CONFLICT (param_key) DO NOTHING`. `ReferenceMigrationIT` (TASK-01/TASK-02) asserts only that the 38 keys exist with their `value_type`, `default_value` and `owner_role`, because the CSV holds 19 rows until TASK-04 writes the other 38; the database-to-CSV equality is `ReferenceLoadIT#catalogRowsMatchTheCatalogFile` in TASK-15, after TASK-04. No `parameter_value` row is seeded: the catalog defaults are served with `versionNo 0` (E1-042 SPEC-007). The 12 definitions are loaded through the PARAMETER branch and approved before the first table load; the 26 list keys cannot be carried by any PARAMETER load (SPEC-026), so their values are these defaults (A-39). A handler code's two list keys come with its owning story, in the same two places (SPEC-025).

## 8. `access/interim-capability-grants.csv` rows added by RWB-E1-043 (37)

Header of E1-042's file: `role,area,rights`. This story adds one row per RW- role for area `Reference data`; no `Rules and parameters` row changes. `rights` is the union of the matrix letters and the A of A-08, written in the order C, R, U, D, A. The source is Users, Roles and Permissions v4 lines 73-110 (Reference data column) plus the six A additions of A-08 (RW-RISK, RW-COE, RW-DATASTEW, RW-TEAMMGR, RW-COMPLY, RW-SECADM). No partner role (PT-*) has a Reference data right.

| Role | Rights | Source and note |
|---|---|---|
| RW-CASEOWN | R | matrix |
| RW-TEAMMGR | RA | matrix R plus A (A-08; S7-019 flow step 4) |
| RW-PHONECOL | R | matrix |
| RW-FIELDCOL | R | matrix |
| RW-RESTRUCT | R | matrix |
| RW-SPECIAL | R | matrix |
| RW-COMPLAIN | R | matrix |
| RW-FRAUD | R | matrix |
| RW-LITOFF | R | matrix |
| RW-ENFORCE | R | matrix |
| RW-LEGAL | RU | matrix |
| RW-SALEOFF | R | matrix |
| RW-NPAMGR | R | matrix |
| RW-DEBTSALE | R | matrix |
| RW-WRITEOFF | R | matrix |
| RW-CREDITAD | R | matrix |
| RW-GUARANT | R | matrix |
| RW-AGENCYMG | RU | matrix |
| RW-CONDUCT | R | matrix |
| RW-CAPACITY | R | matrix |
| RW-PRODHEAD | R | matrix |
| RW-HEADLIT | R | matrix |
| RW-HEADNPA | R | matrix |
| RW-HEADASL | R | matrix |
| RW-CREDCOMM | R | matrix |
| RW-WOCOMM | R | matrix |
| RW-RISK | RA | matrix R plus A (A-08; S7 section 10 "Assumed") |
| RW-COE | CRUDA | matrix CRUD plus A (A-08; E1-042 CLAR-013) |
| RW-DATASTEW | RUA | matrix RU plus A (A-08; S7-001 flow step 9; GAP-46) |
| RW-FINANCE | R | matrix |
| RW-AUDIT | R | matrix |
| RW-COMPLY | RUA | matrix RU plus A (A-08; S7-037 line 46) |
| RW-PLATADM | R | matrix |
| RW-REFADM | CRUD | matrix |
| RW-SECADM | RA | matrix R plus A (A-08; S7-037 line 46) |
| RW-BIANAL | R | matrix |
| RW-TRIBE | R | matrix |

37 rows. The A rows are assumptions, not source grants (A-08; GAP-14, GAP-46); RWB-E1-037 replaces the file and the implementation. The grants file carries no role literal in Java; `ReferenceLoadAuthority` reads the CSV through `CapabilityCheck` (no role code in code).

## 9. P4 types added (published set)

`access.api` (published; D-RUN-18, D-RUN-20): `ListOfValuesReader` (`Set<String> activeCodes(String lovCode)`); `ReferenceTableHandler` with `tableCode()`, `ValidationReport validate(ReferenceLoadFile)`, `int apply(UUID, ReferenceLoadFile, LocalDate)`, `List<String> keyColumns()`, `Optional<HandlerMessage> repeatMessage(ReferenceLoadFile)`, `boolean supportsRollback()`, `void onRolledBack(UUID, UUID, ReferenceLoadFile, LocalDate)`, `List<String> changeSummary(ReferenceLoadFile)`, `Dating dating()`, nested `enum Dating { DATED, CURRENT_STATE }`; `ReferenceLoadFile(String tableCode, LocalDate validFrom, List<String> columns, List<Map<String, Object>> rows)`; `HandlerMessage(String messageCode, Map<String, String> placeholders)`; `ValidationReport(List<RowCheckFailure> failures)` with `ok()`; `RowCheckFailure(int row, String column, String messageCode, Map<String, String> placeholders)`. `ReferenceLoadFile.rows` holds the typed values; `row` 0 means the file as a whole. No P4 class implements the SPI; `PARAMETER` is not an SPI handler.

`access.internal` (not published): `LovValueReader` implements `ListOfValuesReader` over `lov_value` (`lov_code`, `is_active`). It reads no other table and holds no business value.

The T-TE001-14 expected sets after this story: `access.api` = the E1-042 merged set plus `ListOfValuesReader`, `ReferenceTableHandler`, `ReferenceTableHandler.Dating`, `ReferenceLoadFile`, `HandlerMessage`, `ValidationReport`, `RowCheckFailure`; `casewf` named interfaces = `api`, `config.api`, `refdata.api`, `rules`, `timers`, `workflow`; `casewf.refdata.api` = `ReferenceVersionRegistry`, `ReferenceDataService`, `ReferenceDataReaders`, `ReferenceVersion`, `VersionedRows`, `NoVersionInForceException`; every other published package as TE-001 and E1-042 leave it.

## 10. Personal data and synthetic data

| Field | Classification | Handling |
|---|---|---|
| `reference_version.author_user_id` (DF-REF-166) | staff identifier, personal by the protective reading | stored; returned by the Java `versions()` read; never logged, never in an HTTP response, never in an audit event |
| `reference_version.approver_user_id` (DF-REF-167) | staff identifier, personal | as above; DB CHECK approver not the author |
| `reference_version.created_by`, `updated_by` | staff identifier, personal by the protective reading | stored; never logged |
| `reference_row.row_data` | synthetic reference values only | no customer or personal value is loaded by this story's tests |
| Audit and decision lines | no personal data | no user ID, row content, reason or customer identifier; only table, version, loadId, message ID, trace ID and the handler `changeSummary` field IDs |

Every test identity is a synthetic UUID generated for the test (`U-REF-01`, `U-RSK-01`, `U-RSK-02` in the story are labels, not values). No real customer name, ID number, account number or address appears in a table, fixture, log or this file. The seed rows have no user ID: `created_by` and `updated_by` are NULL and `author_user_id`/`approver_user_id` are not seeded because `reference_version` has no seed.

## 11. Seed ownership

| Rows | Owner | Evidence |
|---|---|---|
| `reference_version`, `reference_row` | none by migration; loaded through the endpoint | story section 13 "Configuration and reference data" |
| The 38 `parameter_catalog` rows of section 7 | this story (catalog file and migration) | E1-042 section 4.1 "Catalog change merged" row, CLAR-003; SPEC-029 |
| The 37 Reference data grant rows of section 8 | this story (grants file) | SPEC-027; A-08 |
| The 12 table contents and their definitions | the table's story: DELEGATION_LIMIT RWB-E1-038; ROLE/TEAM/QUEUE RWB-E1-019; DOCUMENT_TYPE RWB-E1-025; PRODUCT_PARAMETER/SERVICE_LEVEL RWB-E1-045; TEMPLATE RWB-E1-046; LEGAL_PERIOD Legal; PRODUCT/REGION/EXPOSURE_BAND unowned (GAP-43) | spec section 22; story sections 13 and 19 |
| A handler code's `rwb.refload.loader/approver.<code>` and optional `refdata.columns.<code>` | the owning story (catalog file and its own migration) | SPEC-025 |
| `lov_value` LOV-REF-TABLE | RWB-E1-001's own migration (`V<seq>` assigned at merge, D-RUN-07); the PS6 local load provides the rows until then | PS6; GAP-32; D-RUN-08 |
