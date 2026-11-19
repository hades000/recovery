<!-- source: E1-042 Migration and Clarifications/RWB-E1-042 Clarification Pack.md -->
<!-- converted: 2026-11-16 from Markdown (copied) -->

> **Source:** `E1-042 Migration and Clarifications/RWB-E1-042 Clarification Pack.md`  
> **Converted from:** Markdown (copied)

# RWB-E1-042 — Migration files and build clarifications

**Prepared:** 10 November 2026  
**Story:** RWB-E1-042 Central configuration service and parameter catalog  
**Audience:** Client review and build team  
**Status:** For review; no client specification has been changed

This pack answers the review points and provides the two requested migration files. All new material is in this folder. Nothing under the client's specification or repository documentation set has been edited.

## Answers in brief

1. **Migration files.** `sql/V042_1__parameter_catalog.sql` and `sql/V042_2__parameter_seed.sql` are provided and tested. Because D-RCV-28 requires one file per story, commit the consolidated `sql/V0042__rwb_e1_042_parameter_catalog_and_seed.sql` unless a migration-lint exception is approved. The seed has 13 catalog rows and 28 value rows; the full Epic 1 catalog remains OI-E1-042-003.
2. **`POST /admin/reference-loads`.** The user chooses **one table code** from LOV-REF-TABLE, not a database table, not a column, and not a type. One call carries one file for one code. The handler owns the target table and the column mapping; the caller never supplies `{dbTable}.{dbColumn}`. `PARAMETER` uses `key,environment,value`. Other codes have their own headers; several are still undefined and are listed in §3.4.
3. **Flow #2 build.** There are two different CSVs. `config/parameter-catalog.csv` is build-time: it defines keys and generates `ParameterKeys` and the seed. The uploaded `key,environment,value` file is run-time: it changes values only and cannot add a key. A new key needs a reviewed PR and a release; a new value needs a load and an approval.
4. **TC-E1-042-12.** Correct status is **Blocked**, not Failed and not Pass. The 403 path arrives with E1-022 and the permission matrix with E1-037, both after the E1-042 build window. Do not mock a role. OI-E1-042-001 tracks it with a measurable exit criterion.
5. **Messages.** The message table does not exist and is unowned; “E1-043 #9” points to the ninth Messages row of the reference-data register, not to an E1-043 story item. Use the fixed-text resolver with one seam, exact English, proposed Thai (pending DL10), and tests that assert the message ID and placeholders. OI-E1-042-004 tracks the table.

---

## 1. What is in this folder

| Path | Purpose | Commit? |
|---|---|---|
| `sql/V042_1__parameter_catalog.sql` | Requested DDL file: `parameter_catalog`, `parameter_value`, constraints, foreign key, indexes and comments. | Review copy only; see §2.1 |
| `sql/V042_2__parameter_seed.sql` | Requested seed file, generated from `config/parameter-catalog.csv`. | Review copy only; see §2.1 |
| `sql/V0042__rwb_e1_042_parameter_catalog_and_seed.sql` | The same content as one D-RCV-28-compliant migration: DDL plus seed. | **Yes — recommended** |
| `config/parameter-catalog.csv` | The bootstrap catalog input. Thirteen rows. | Yes, under `config/` in the code repository |
| `config/messages-e1-042.csv` | Fixed message catalog for the temporary resolver (§6). | Yes, under `config/` until the message table exists |
| `tools/Generate-ParameterSeed.ps1` | Reference generator: CSV → `V042_2__parameter_seed.sql`. | Yes, under `build-tools/` or `tools/` |
| `tools/Assemble-V0042.ps1` | Builds the consolidated single migration from the two review files. | Yes |
| `tests/test_migrations.sh` | PostgreSQL verification: clean install, re-run, split files, baseline overlap, eight negative tests and the deployment guard. | Yes |
| `evidence/migration-test-output.txt` | The output of the verification run. | Yes, as test evidence |

The SQL uses **no literal schema name**. It uses the Flyway placeholder `${recoverySchema}` throughout.

---

## 2. Migration files

### 2.1 File naming: the requested names and the migration lint

The two requested names are the names in story §13, but they do **not** satisfy the migration rule that was ruled after the story was written (D-RCV-28, recorded in RWB-E1-044):

| Rule | Source | Effect on `V042_1` / `V042_2` |
|---|---|---|
| Recovery Flyway files are named `V<seq>__<story>_<name>.sql`, with a four-digit sequence taken in merge order | D-RCV-28; RWB-E1-044 §13 | `V042_1__...` and `V042_2__...` fail the name pattern. |
| One migration file per story; the lint fails when a story key appears in two files | RWB-E1-044 BR3, AC6 | Two files carrying `RWB-E1-042` fail the lint. |
| Line 1 is `-- Story: <story key>` | D-RCV-28; `AGENTS.md` §2 | Both files satisfy this. |

**Recommendation:** commit `V0042__rwb_e1_042_parameter_catalog_and_seed.sql`. It contains exactly the same DDL and seed as the two review files, with one story header. The generator can still produce the seed section separately at build time and concatenate it; `tools/Assemble-V0042.ps1` does that here.

If the team requires the two-file split, record a migration-lint exception and get the tech lead to approve it. This is **OI-E1-042-002**.

### 2.2 Schema placeholder

The files use `${recoverySchema}`, per D-RCV-28 and RWB-E1-044 §13. The same file runs in every environment.

One configuration point needs correcting before deployment. RWB-E1-044 §12 shows:

```properties
spring.flyway.placeholders.schema=${RWB_SCHEMA}
```

That defines a placeholder named `schema`, not `recoverySchema`. To resolve `${recoverySchema}`, the property must be:

```properties
spring.flyway.placeholders.recoverySchema=${RWB_SCHEMA}
```

Otherwise Flyway sends the literal `${recoverySchema}` to PostgreSQL and the migration fails. This is **OI-E1-042-009**.

### 2.3 Baseline overlap: RWB-E1-001 already creates both tables

`V0001__rwb_e1_001_recovery_schema.sql` is written from Recovery Workbench Physical Schema v4 and already contains `parameter_catalog` and `parameter_value`. A plain `CREATE TABLE` in this story would fail with “relation already exists”.

The migration is therefore **guarded**:

- `CREATE TABLE IF NOT EXISTS` creates the full definition when the baseline is absent.
- A `DO` block adds each E1-042 constraint, foreign key and unique rule only when it is missing.
- Indexes use `CREATE INDEX IF NOT EXISTS`.

The verification run applies the file on top of a simulated V0001 baseline and confirms that it adds the foreign key and five catalog checks without error (§8).

**Pre-flight queries for an existing environment.** Run these before the migration. If any returns a row, fix the data first; the new constraint will fail otherwise.

```sql
-- 1. Duplicate versions for a global key (the baseline unique key treats NULLs as distinct)
SELECT param_key, environment, COALESCE(product_group, '*') AS product_group_key,
       version_no, count(*) AS rows
FROM recovery.parameter_value
GROUP BY 1, 2, 3, 4
HAVING count(*) > 1;

-- 2. Values whose catalog key is missing
SELECT pv.param_key, count(*) AS rows
FROM recovery.parameter_value pv
LEFT JOIN recovery.parameter_catalog c ON c.param_key = pv.param_key
WHERE c.param_key IS NULL
GROUP BY pv.param_key;

-- 3. Secrets that carry a default value
SELECT param_key FROM recovery.parameter_catalog
WHERE secret AND default_value IS NOT NULL;

-- 4. Approved rows with no approval timestamp
SELECT id, param_key FROM recovery.parameter_value
WHERE status IN ('APPROVED', 'IN_FORCE') AND approved_at IS NULL;

-- 5. Two approved versions at the same valid-from date
SELECT param_key, environment, COALESCE(product_group, '*') AS product_group_key,
       valid_from, count(*) AS rows
FROM recovery.parameter_value
WHERE status IN ('APPROVED', 'IN_FORCE')
GROUP BY 1, 2, 3, 4
HAVING count(*) > 1;

-- 6. Catalog rows whose kind, value_type, scope or environments the new checks reject
SELECT param_key, kind FROM recovery.parameter_catalog
WHERE kind NOT IN ('BUSINESS', 'ENVIRONMENT');

SELECT param_key, value_type FROM recovery.parameter_catalog
WHERE value_type NOT IN ('STRING', 'INTEGER', 'DECIMAL', 'BOOLEAN', 'DATE', 'TIME',
                         'DURATION', 'CODE', 'CODE_LIST', 'JSON');

SELECT param_key, scope FROM recovery.parameter_catalog
WHERE scope NOT IN ('GLOBAL', 'PRODUCT');

SELECT param_key, environments FROM recovery.parameter_catalog
WHERE environments IS NOT NULL AND environments <> ''
  AND environments !~ '^(DEV|SIT|UAT|PROD)(,(DEV|SIT|UAT|PROD))*$';

-- 7. Values whose environment or status the new checks reject
SELECT id, param_key, environment FROM recovery.parameter_value
WHERE environment NOT IN ('DEV', 'SIT', 'UAT', 'PROD');

SELECT id, param_key, status FROM recovery.parameter_value
WHERE status NOT IN ('VALIDATED', 'APPROVED', 'IN_FORCE', 'SUPERSEDED', 'ROLLED_BACK', 'REFUSED');
```

### 2.4 What the DDL enforces, and what it deliberately does not

| Level | Rule | Why |
|---|---|---|
| `parameter_catalog` | Unique `param_key` | One definition per key. |
| `parameter_catalog` | `scope IN ('GLOBAL','PRODUCT')` | LOV-PARAM-SCOPE. |
| `parameter_catalog` | `kind IN ('BUSINESS','ENVIRONMENT')` | Separates business parameters from environment settings. |
| `parameter_catalog` | `value_type` in the ten approved types | The type drives the load check; a new type needs a migration. |
| `parameter_catalog` | `environments` is a comma-separated subset of `DEV,SIT,UAT,PROD` | The load check reads this list. |
| `parameter_catalog` | A secret cannot have a default value | BR6: a secret is listed, never stored in the table. |
| `parameter_value` | Environment, status and date checks | LOV-ENVIRONMENT, LOV-VERSION-STATUS, no end before start. |
| `parameter_value` | `version_no >= 1` | Version 1 is the seed; the first human load starts at version 2. |
| `parameter_value` | Approver is never the author | BR4 maker-checker, enforced even if the service check is bypassed. |
| `parameter_value` | An `APPROVED` or `IN_FORCE` row has `approved_at` | No approved row without an approval timestamp. |
| `parameter_value` | Foreign key to `parameter_catalog.param_key` | A runtime load cannot invent a key. |
| `parameter_value` | **NULL-safe** unique `(param_key, environment, product_group, version_no)` | The baseline unique constraint treats NULL `product_group` as distinct; the expression index closes that hole. |
| `parameter_value` | One approved version per key, environment, product group and `valid_from` | The database guard behind the 409 rule. |
| `parameter_value` | Lookup indexes for the story read | `(param_key, environment, valid_from)` and the product-group lookup. |

**Deliberately not in the database:** the min/max range check. `min_value` and `max_value` are text and their meaning depends on `value_type` (INTEGER, DECIMAL, DATE, TIME, CODE_LIST, JSON). A single SQL `CHECK` cannot parse all of them safely. `ParameterLoadChecks` performs the typed range check and refuses the whole load with MSG-GEN-002. The database enforces the structural rules; the service enforces the typed rules.

### 2.5 Seed scope: what is in `V042_2`, and what is not

The seed contains **13 catalog rows** and **28 value rows** (7 keys × 4 environments).

| Key | Scope | Default | Value rows | Owner | Source |
|---|---|---|---|---|---|
| `case.entry.dpd` | GLOBAL | `90` | 4 | RW-COE | E1-042 §3, AC1, DL16 |
| `refdata.cache.ttl-seconds` | GLOBAL | `300` | 4 | RW-PLATADM | E1-042 §3, AC8, DL11 |
| `config.cache.ttl-seconds` | GLOBAL | `60` | 4 | RW-PLATADM | E1-042 §13, assumed DL11 |
| `caselist.export.maxrows` | GLOBAL | `10000` | 4 | RW-COE | E1-042 §3, assumed DL11 |
| `ace.db.password` | GLOBAL | none (secret) | 0 | RW-PLATADM | E1-042 AC9, DL26 |
| `recon.caselist.tolerance.pct` | GLOBAL | `0.00` | 4 | RW-COE | E1-002 §3, assumed DL25 |
| `caselist.allocation.wait.until` | GLOBAL | `07:15` | 4 | RW-COE | E1-002 §3 |
| `servicelevel.required-statuses` | GLOBAL | six statuses | 4 | RW-COE | E1-045 BR3, assumed DL22 |
| `ENTRY_DPD` | PRODUCT | none | 0 | RW-PRODHEAD | E1-045 BR2 |
| `EXCLUSION_LIST` | PRODUCT | none | 0 | RW-PRODHEAD | E1-045 BR2 |
| `NOTICE_PERIOD_DAYS` | PRODUCT | none | 0 | RW-PRODHEAD | E1-045 BR2 |
| `CURE_PERIOD_DAYS` | PRODUCT | none | 0 | RW-PRODHEAD | E1-045 BR2 |
| `EXPOSURE_BAND_SET` | PRODUCT | none | 0 | RW-PRODHEAD | E1-045 BR2 |

Why this set and not the full Epic 1 catalog:

1. **The source file is not in the pack.** The story's source of truth is `config/parameter-catalog.csv`; the full Epic 1 version is not in this document set. This is **OI-E1-042-003**.
2. **Only rows with a documented default and owner are seeded.** The corpus names many parameters but does not give a default, type, range or owner for most of them. Inventing those values would violate the repository rule “do not present inferred behaviour as an approved requirement” (`AGENTS.md` §4.9).
3. **Product-scope rows carry no values by design.** Their values are `PRODUCT_PARAMETER` rows read through `ProductParameterService` (E1-045), not `parameter_value` rows.
4. **Negative fixtures stay out.** `allocation.retry.limit` is deliberately absent because AC3/TC-E1-042-03 use it as the key the catalog must **not** list.
5. **`case.entry.dpd_threshold` is not seeded.** It is a second name for the same concept (§7, OI-E1-042-006). Seeding both would create two competing keys.

The seed is generated, not hand-edited:

```powershell
# From the pack root
powershell -NoProfile -ExecutionPolicy Bypass -File .\tools\Generate-ParameterSeed.ps1

# Rebuild the D-RCV-28 single file
powershell -NoProfile -ExecutionPolicy Bypass -File .\tools\Assemble-V0042.ps1
```

When the full `config/parameter-catalog.csv` lands, replace the bootstrap CSV, rerun the generator, and commit the new `V0042`. The generator keeps the SQL shape and the deployment guard.

### 2.6 Applying the migration

**Through Flyway (the real path):**

1. Put the file in `recovery/src/main/resources/db/migration/recovery/`.
2. Set `RWB_SCHEMA` and `spring.flyway.placeholders.recoverySchema=${RWB_SCHEMA}`.
3. Keep `spring.flyway.table=flyway_schema_history_recovery`, `validate-on-migrate=true`, `out-of-order=false`, `clean-disabled=true`.
4. Start the service or run the pipeline `migrate` step. Flyway applies it once and records the checksum.
5. Verify the counts and constraints with the queries in §8.

**Manual run for a review environment:**

```powershell
# Replace the placeholder for a one-off psql run; do not commit the replaced file.
$sql = (Get-Content .\sql\V0042__rwb_e1_042_parameter_catalog_and_seed.sql -Raw) `
  -replace '\$\{recoverySchema\}', 'recovery'
[System.IO.File]::WriteAllText(
  (Join-Path (Get-Location) 'sql\.tmp_V0042_recovery.sql'),
  $sql,
  (New-Object System.Text.UTF8Encoding($false)))

psql -v ON_ERROR_STOP=1 -h $HOST -U $USER -d $DB -f .\sql\.tmp_V0042_recovery.sql
Remove-Item .\sql\.tmp_V0042_recovery.sql
```

The seed uses `valid_from = DATE '2026-11-30'`, the E1 release date. If the release date moves, change it in the CSV/generator, not in the generated SQL.

---

## 3. Contract 12 — how `POST /admin/reference-loads` decides what to update

### 3.1 The direct answer

The caller chooses **one table code**, not a database table, not a column, and not a Java type.

- `table` is a required multipart field. Its value must be a code in **LOV-REF-TABLE** (25 codes) **and** have a registered handler.
- One POST carries **one file for one code**. Loading three codes means three calls with the same `validFrom`.
- The server routes the code to the handler registered for that code. The handler owns the target table, the column names, the key columns and the row checks.
- The caller **never** supplies a `{dbTable}.{dbColumn}` mapping. A user-supplied mapping would be a SQL-injection and data-governance hole.
- `kind` (`BUSINESS`, `ENVIRONMENT`) and `value_type` (`INTEGER`, `STRING`, …) do **not** choose a table. `value_type` is used by the handler to parse and range-check each value.

So the choice is **by table code**, not by database table and not by type. If the user interface asks the user to pick something, it must ask for a table code from LOV-REF-TABLE, and the code must have a handler; otherwise the load is refused.

```text
Caller:  table = one LOV-REF-TABLE code          file = one file for that code
         validFrom = one date

Server:  code -> registry -> handler for that code
         handler -> header schema -> row checks -> its own target table
```

### 3.2 Why the endpoint appears to update many tables

The endpoint is a versioned load service with **one handler per table code**. The physical target differs by code. That is why it looks like a generic “update any table” endpoint; it is not.

| # | Code | Physical target | Handler / owner | CSV template status |
|---:|---|---|---|---|
| 1 | `PRODUCT` | `reference_version` + `reference_row` (E1-045); E1-001 maps it to `data_product` | E1-043 registry + product checks | Partial; target disputed (OI-E1-042-010) |
| 2 | `REGION` | `reference_version` + `reference_row` | E1-043 generic registry | Not formally defined |
| 3 | `EXPOSURE_BAND` | `reference_version` + `reference_row` | E1-043 generic registry | Not formally defined |
| 4 | `ROLE` | `reference_version` + `reference_row`; no applier to `role` | E1-043 generic registry | Not formally defined |
| 5 | `TEAM` | `reference_version` + `reference_row` | E1-043 generic registry | Not formally defined |
| 6 | `QUEUE` | `reference_row`, then `queue` via `QueueVersionApplier` | E1-019 | Not defined; E1-019 owns it |
| 7 | `QUEUE_MEMBER` | `reference_row`, then `queue_member` | E1-019 | Not defined; E1-019 owns it |
| 8 | `SERVICE_LEVEL` | `reference_version` + `reference_row` | E1-045 | **Not defined**; E1-045 owns it |
| 9 | `DOCUMENT_TYPE` | `document_type` | P5 `DocumentTypeLoader` | Partial; E1-025 owns it |
| 10 | `DOCUMENT_CHECKLIST` | `document_checklist_item` | P5 `ChecklistLoader` | **Not defined**; E1-040 owns it |
| 11 | `RETENTION_CLASS` | `retention_class` | P5 `RetentionClassLoader` | Partial; E1-041 owns it |
| 12 | `TEMPLATE` | `template` | `TemplateLoadHandler` | Partial; E1-046 owns it |
| 13 | `DELEGATION_LIMIT` | `delegation_limit` | `DelegationLimitLoader` | **Not defined**; E1-038 owns it |
| 14 | `PERMISSION` | `permission` | `PermissionMatrixLoader` | Partial; E1-037 owns it |
| 15 | `MASKING_RULE` | `masking_rule` | `MaskingRuleLoader` | Partial; E1-037 owns it |
| 16 | `PARTNER_USER` | `partner_user` | `PartnerUserLoader` | Partial; Epic 2 owns it |
| 17 | `LEGAL_PERIOD` | `reference_version` + `reference_row` | E1-043 generic registry | Not formally defined |
| 18 | `HOLIDAY` | `reference_version` + `reference_row` | E1-043 generic registry | Not formally defined |
| 19 | `PRODUCT_PARAMETER` | `reference_version` + `reference_row` | E1-045 | **Not defined**; E1-045 owns it |
| 20 | `PARAMETER` | **`parameter_value` directly** | `ParameterLoadHandler` (E1-042) | **Defined: `key,environment,value`** |
| 21 | `ENTRY` | `rule_row` + `rule_version` through `POST /admin/rule-versions` | E1-029 | Not this endpoint |
| 22 | `EXCLUSION` | `rule_row` + `rule_version` | E1-029 | Not this endpoint |
| 23 | `ALLOCATION` | `rule_row` + `rule_version` | E1-029 | Not this endpoint |
| 24 | `ASSIGNMENT` | `rule_row` + `rule_version` | E1-029 | Not this endpoint |
| 25 | `TRANSFER` | `rule_row` + `rule_version` | E1-029 | Not this endpoint |

The first 20 are reference-data codes; the last five are rule-table codes and are loaded through the rule-version endpoint, not this one. `DOCUMENT_HUB_PARAMETER` is named in the API description but has **no LOV-REF-TABLE row**; see OI-E1-042-010.

**Adding a code is not a data load.** A new code needs all of: a LOV-REF-TABLE row, a registered handler, a `ReferenceTableSchemas` entry, a target table migration if the handler owns a table, and a release. Adding a LOV row alone does not make the code loadable.

### 3.3 The `PARAMETER` CSV: exact format and mapping

```csv
key,environment,value
case.entry.dpd,PROD,91
refdata.cache.ttl-seconds,PROD,300
```

| CSV column | Target column | Check / behaviour |
|---|---|---|
| `key` | `parameter_value.param_key` | Must exist in `parameter_catalog.param_key`. Unknown key refuses the whole load with MSG-P1-002. |
| `environment` | `parameter_value.environment` | `DEV`, `SIT`, `UAT` or `PROD`; must be one the catalog line lists in `environments`. |
| `value` | `parameter_value.param_value` | Parsed as the catalog `value_type`; must fall inside `min_value`..`max_value` inclusive. Wrong type = MSG-P1-002; out of range = MSG-GEN-002. |
| — | `parameter_value.product_group` | `NULL`. The `PARAMETER` code is global. Product-scoped values use `PRODUCT_PARAMETER` (E1-045), not this code. |
| — | `parameter_value.version_no` | Next number for the key and environment. The seed is version 1. |
| — | `parameter_value.valid_from` | The request `validFrom`. It must not be before the business date; equal is allowed. |
| — | `parameter_value.valid_to` | `NULL` on load. Approving a successor sets the replaced row’s `valid_to` to the day before the new `valid_from`. |
| — | `parameter_value.status` | `VALIDATED` on load; `APPROVED` after the approve call. |
| — | `parameter_value.author_user_id` | The signed-in loader. |
| — | `parameter_value.approver_user_id`, `approved_at` | Set only by the approve call. The approver must differ from the author. |

The catalog definition (type, range, default, owner) is **not** in this file. It comes from `config/parameter-catalog.csv` through a reviewed pull request and the generated migration. A runtime upload cannot add a key.

**A gap to decide:** `parameter_value` has no `load_id`, but the approve endpoint is `POST /admin/reference-loads/{loadId}/approve`. The handler needs a durable link from the load to the rows it created. Options are in §3.7 and OI-E1-042-008.

### 3.4 CSV formats for the other codes

There is **no single CSV schema for all codes**, and there is **no consolidated template register in the pack** (OI-E1-042-005). Each owning story defines the header; the handler enforces it.

**Defined or partially defined column sets:**

| Code | CSV columns stated in the pack | Target |
|---|---|---|
| `PARAMETER` | `key,environment,value` | `parameter_value` |
| `PERMISSION` | `role_code,capability_area,letters,matrix_version` | `permission` (`role_code` resolves to `role_id`) |
| `MASKING_RULE` | `role_code,field_id,unmasked,masking_version` | `masking_rule` |
| `DOCUMENT_TYPE` | `doc_type_code,label_en,label_th,write_once,retention_class,field_definitions,legal_signoff_by,legal_signoff_date,npa_signoff_by,npa_signoff_date` | `document_type` |
| `TEMPLATE` | `template_code,language,product_group,channel,notice_type,signature_basis,body_ref,merge_codes,approver,approval_date` | `template` (`approver`→`approved_by`, `approval_date`→`approved_at`) |
| `RETENTION_CLASS` | `class_code,period_months,end_action` | `retention_class` |
| `PARTNER_USER` | `partner_identity,partner_id,role,valid_from,valid_to` | `partner_user` (`partner_identity`→`identity_ref`, `role`→`role_code`) |
| `PRODUCT` | `product_code,product_name,definition,owner_role,system_of_record,refresh_cycle,expected_by,owner_user_id` | `reference_row` (E1-045) or `data_product` (E1-001); target disputed |
| `TRACKER_INVENTORY` | `tracker_code,team_code,tracker_name,location_type,location_ref,owner_user_id,field_list,update_cycle,target_product,decision,decision_reason` | `tracker_inventory` |
| `DQ_RULE` | `rule_code,rule_version,rule_name,product_code,target_entity,rule_type,rule_params,valid_from,valid_to,approved_by,test_case_id` | `dq_rule` |
| `RETENTION_RULE` | `product_code,table_name,record_class,retention_months,age_basis_field,rule_version,valid_from,valid_to,approved_by` | `retention_rule` |
| `DATA_PRODUCT_ACCESS` | `product_code,role_code,can_read,access_version,valid_from,valid_to` | `data_product_access` |
| `MEASURE_DEFINITION` | `measure_code,name,formula,data_product,unit,definition_version,approver,approval_date` | `measure_definition` |
| `SYS_FIELDS` | `field_id,owner_role,refresh_cycle,late_behavior,interface_id` | `sys_fields` |
| `PAYMENT_MATCH_RULE` | `rule_code,priority,match_type,amount_tolerance,window_days_before,window_days_after,partial_floor,rule_version` | `payment_match_rule` |

**Not defined in the pack.** These need the owning story to publish the template before a load can be built:

| Code | Owning story | What is known | Proposed header (not approved) |
|---|---|---|---|
| `PRODUCT_PARAMETER` | RWB-E1-045 | Product group, parameter code, value, unit | `product_group,parameter_code,value,unit` |
| `SERVICE_LEVEL` | RWB-E1-045 | Product group, case status, limit, unit, warn percent, escalate-to role | `product_group,case_status,limit,unit,warn_percent,escalate_to_role` |
| `QUEUE` | RWB-E1-019 | Team, role, method, capacity cap, overflow queue | `queue_code,queue_name,team_code,role_code,assignment_method,capacity_cap,overflow_queue_code` |
| `QUEUE_MEMBER` | RWB-E1-019 | Queue, user, capacity, skill codes | `queue_code,user_ref,capacity,skill_codes` |
| `DELEGATION_LIMIT` | RWB-E1-038 | One row per decision code and approval level | `decision_code,approval_level,product_group,principal_limit,loss_pct_limit,min_price_pct_fmv,holder_user_ref,substitute_user_ref,limit_version` |
| `DOCUMENT_CHECKLIST` | RWB-E1-040 | Stage, route, document type, required, sort order | `stage_code,route_code,document_type,required,sort_order` |
| `MERGE_FIELD` | RWB-E1-046 | Merge code, source entity, source field, field ID, required, personal data | `merge_code,source_entity,source_field,field_id,is_required,personal_data` |
| `REGION`, `EXPOSURE_BAND`, `ROLE`, `TEAM`, `HOLIDAY`, `LEGAL_PERIOD` | RWB-E1-043 (generic registry) | Rows are stored as JSON in `reference_row.row_data`; no formal header | The handler’s `ReferenceTableSchemas` entry must publish the keys |

The proposed headers are a starting point for the owning story, not an approved contract. Do not build a loader against them until the owner confirms.

### 3.5 What the caller cannot do

- Cannot name a database table instead of a table code.
- Cannot name a column, or supply a `{dbTable}.{dbColumn}` mapping.
- Cannot load two codes in one call or one workbook sheet.
- Cannot add a parameter key through a value load. An unknown key refuses the whole load.
- Cannot use a code that is in LOV-REF-TABLE but has no registered handler.
- Cannot choose a code by `kind` or `value_type`; those are attributes of a parameter, not routing keys.

### 3.6 Request, response and errors

**Request:** `multipart/form-data`

| Field | Type | Required | Notes |
|---|---|---|---|
| `file` | binary | Yes (prose) | CSV or XLSX, one sheet. The PARAMETER template is CSV. |
| `table` | string | Yes (prose) | One LOV-REF-TABLE code. |
| `validFrom` | string, date | Yes (prose) | ISO 8601. Not before the business date; equal is allowed. |

The OpenAPI schema has no `required:` array; the prose makes all three required. Add `required` and `format: date` to the schema. This is **OI-E1-042-011**.

**Response:** `201 ReferenceLoad`

```json
{ "id": "<uuid>", "table": "PARAMETER", "validFrom": "2026-12-10", "status": "VALIDATED", "rows": 2 }
```

**Errors:** 401 MSG-P4-001; 403 MSG-P4-002; 409 MSG-P3-027 (same table and `validFrom` with different content while an approved version exists); 422 MSG-GEN-001 / MSG-GEN-002 / MSG-P1-002 / MSG-P3-027; 503 (message ID to be decided; MSG-GEN-006 is the candidate).

**Idempotency:** the server computes a SHA-256 content hash over the rows sorted by key. The natural key is `(table_code, valid_from, content_hash)`. An identical repeat returns the existing load and writes nothing. Do not return 409 for an identical repeat; 409 is for different content at an already-approved `validFrom`.

**Decision needed:** the pack is inconsistent on the repeat status. E1-043 says “returns the existing load” without a status; the OpenAPI declares only 201; several downstream stories say 409. Recommended: **201 with the same body** for an identical repeat, **409** only for a content conflict. Record the choice in the API specification.

### 3.7 Approve, rollback and the `loadId` link

| Operation | Path | Right | Success | Refusals |
|---|---|---|---|---|
| Load | `POST /admin/reference-loads` | Reference data C | 201 `ReferenceLoad` (VALIDATED) | 401, 403, 409, 422, 503 |
| Approve | `POST /admin/reference-loads/{loadId}/approve` | Reference data A | 200 `ReferenceLoad` (APPROVED) | 401, 403, 404, 409 author = approver (MSG-P7-002), 503 |
| Rollback | `POST /admin/reference-loads/{loadId}/rollback` | Reference data U | 200 `ReferenceLoad` (ROLLED_BACK) | 401, 403, 404, 409 no earlier version (MSG-P3-015), 422 empty reason, 503 |
| Verify | `POST /admin/reference-loads/{loadId}/verify` | Reference data U | 200 `ReferenceLoad` | 401, 403, 404, 422 empty note or before `validFrom`, 503 |

**The `loadId` gap.** `parameter_value` has `id` but no `load_id`. The `reference_version` table has `load_id`, but the `PARAMETER` handler writes `parameter_value` directly and does not create a `reference_version` row. So the approve path cannot resolve a `PARAMETER` load by `{loadId}`. Choose one:

- **A (recommended):** add `load_id uuid` to `parameter_value`, indexed, and write one value per load. The approve/rollback path resolves rows by `load_id`. This is a schema addition to the story; it needs a migration and a physical-schema update.
- **B:** write a `reference_version` header for every `PARAMETER` load with `table_code='PARAMETER'` and use its `load_id`; `parameter_value` still needs a link, so this alone does not close the gap.
- **C:** use the first `parameter_value.id` as the load id. Not recommended; a load can contain many rows and the link is fragile.

This is **OI-E1-042-008**.

---

## 4. Flow #2 build — build-time CSV or runtime CSV?

Both exist. They are different files with different jobs. This is the source of the confusion.

| | Catalog file | Value file |
|---|---|---|
| Path | `config/parameter-catalog.csv` in the repository | Uploaded to `POST /admin/reference-loads` |
| When | Build time and deployment | Run time |
| Changed by | Squad member through a reviewed pull request; the owner approves | RW-COE through a checked, approved load |
| What it changes | The **definition** of a key: kind, type, unit, range, default, scope, required, owner, environments, used by | The **value** of a key that already exists |
| What it produces | `ParameterKeys` class; the `V042_2` seed; the catalog rows | `parameter_value` version rows |
| Can it add a key? | **Yes** | **No.** An unknown key refuses the whole load with MSG-P1-002. |
| Can it change a type or range? | Yes, through a reviewed PR and a migration | No. The catalog line is the check. |
| Needs a release? | Yes | No |

**Build step 2** reads the repository catalog and generates a typed class. It does **not** read the runtime upload. The runtime upload has only `key,environment,value`; it has no type, owner, range or default, so it cannot generate a typed class.

A generated class looks like this (the exact package and naming come from the generator):

```java
// GENERATED from config/parameter-catalog.csv. Do not edit.
package recovery.casewf.config.api;

public final class ParameterKeys {
    private ParameterKeys() {}

    public static final ParameterKey<Integer> CASE_ENTRY_DPD =
        ParameterKey.of("case.entry.dpd", Integer.class);
    public static final ParameterKey<Integer> REFDATA_CACHE_TTL_SECONDS =
        ParameterKey.of("refdata.cache.ttl-seconds", Integer.class);
    public static final ParameterKey<Integer> CONFIG_CACHE_TTL_SECONDS =
        ParameterKey.of("config.cache.ttl-seconds", Integer.class);
    public static final ParameterKey<Integer> CASELIST_EXPORT_MAXROWS =
        ParameterKey.of("caselist.export.maxrows", Integer.class);
    public static final ParameterKey<String> ACE_DB_PASSWORD =
        ParameterKey.of("ace.db.password", String.class);
    // ... one constant per catalog line
}
```

Application code reads a value only through `ParameterService` with one of these constants and a business date:

```java
ParameterValue<Integer> entry = parameterService.get(
        ParameterKeys.CASE_ENTRY_DPD, businessDate);
int dpd = entry.value();          // 90
int version = entry.versionNo();  // 1
```

The two build checks complete the loop:

- **`RwbMagicNumberCheck`** fails on numeric and string business literals in the recovery packages. Allowed: `0`, `1`, `-1` and test code. It names the file, the line and the catalog key whose default equals the literal.
- **`CatalogCompletenessCheck`** compares the keys read through `ParameterService` with the catalog file. It fails on a key that is missing, or a catalog line with no owner or no default.

**One exception to “no default”:** the five `PRODUCT`-scope rows have no default by design, because their values are `PRODUCT_PARAMETER` rows. `CatalogCompletenessCheck` must exempt `scope='PRODUCT'` or the build will fail on a correct catalog. This is **OI-E1-042-007**.

**In one sentence:** the build-time CSV defines the keys and generates the class and the seed; the runtime CSV changes the value of a key that already exists. A new parameter is a pull request and a release; a new value is a load and an approval, with no release.

---

## 5. TC-E1-042-12 — the role test is Blocked, not Failed

### 5.1 What the test does

`TC-E1-042-12` calls `GET /admin/parameters` as **RW-PHONECOL** and expects **403** with **MSG-P4-002**. RW-PHONECOL holds `Reference data R` but **not** `Rules and parameters R`. That is the discriminating case: it proves the endpoint is protected by the correct capability area, not merely by “some role check”.

### 5.2 Why it cannot run in the E1-042 build window

| Dependency | Delivered by | When | Why it blocks the test |
|---|---|---|---|
| SSO, MFA, session roles, `AccessCheck`, endpoint interceptor | **RWB-E1-022** | Window 2, item #31, 16–27 November 2026 | The 403 path does not exist in Window 1. |
| Permission matrix as data, `RULES_AND_PARAMETERS = -` for RW-PHONECOL | **RWB-E1-037** | Window 2, item #33, 16–27 November 2026 | The matrix the test assumes is not loaded. |
| Role rows and `role.entra_group` per environment | RWB-E1-019 / environment setup | Window 2 | RW-PHONECOL cannot resolve to a session without the group mapping. |

RWB-E1-042 is Window 1, item #3, 2–13 November 2026. It finishes before E1-022 and E1-037 start. The dependency chain is E1-042 → E1-043 → E1-019 → E1-022 → E1-037.

The Physical Schema v4 seed does not close the gap:

- 421 `permission` rows for 49 of 54 roles, against the 756 rows (54 roles × 14 areas) that E1-037 requires.
- No rows with `letters = '-'`; five roles have no rows at all.
- Every row uses `matrix_version = '1'`, not `PM-2026.11`.
- `role.entra_group` is null for every role, so no session can resolve.

RW-PHONECOL has no `RULES_AND_PARAMETERS` row. Under E1-022, absence of a letter is equivalent to `-`, so the **expected 403 is design-correct**, but the **Given** of the test (“the permission matrix is in force”) is not met.

### 5.3 Correct status and disposition

Record **Blocked**, not Pass and not Fail. The repository test standard defines unmet prerequisites as Blocked, not Failed. If the test-management tool requires a second label, use **Deferred** rather than **Ignored**, so the test stays visible in the regression suite and cannot be forgotten. Do not add a mock role or a temporary permit: it would weaken the access test and violate `AGENTS.md` §4.5 (“disable, skip or weaken a test” is forbidden). Stub the identity provider if needed, but resolve roles from the real `role`/`permission` tables and use the real `AccessCheck`.

This is **OI-E1-042-001**.

### 5.4 Exit criterion

After E1-037 loads `PM-2026.11` in SIT (756 rows = 54 roles × 14 areas, dashes allowed) and E1-022 resolves RW-PHONECOL from `RWB-SIT-RW-PHONECOL`:

1. Call `GET /api/recovery/v1/admin/parameters` as RW-PHONECOL.
2. Expect HTTP **403**, `Content-Type: application/problem+json`, `messageCode = MSG-P4-002`.
3. Expect `detail` to name the action **`read parameters`** and no parameter array or secret value.
4. Expect one refusal event with area `RULES_AND_PARAMETERS`, right `R`, result `REFUSED`.
5. Record **Pass** only on that evidence. Any 200, 401 or other message code is **Fail**.

The `{action}` value for MSG-P4-002 is not pinned in E1-042. Use `read parameters`, matching E1-022's `read roles` pattern.

**Traceability gap:** E1-042 §18 cites only TC-E1-042-01 to TC-E1-042-11 and omits TC-12. Add TC-12 to the traceability row when the test is executed.

---

## 6. Messages — fixed text until the message table exists

### 6.1 Finding: there is no message table, and “E1-043 #9” is an ambiguous reference

Physical Schema v4 has **no** `message`, `message_catalog` or `sys_message` table, no `MSG-` column, and no `MESSAGE` code in LOV-REF-TABLE. No story in the pack creates one.

The review note says “[E1-043 (#9)]”. That reference is ambiguous:

- E1-043 BR1 item 9 is `TEMPLATE`, not Messages.
- E1-043 serves 13 table codes; `MESSAGE` is not one of them.
- LOV-REF-TABLE has 25 codes; none is `MESSAGE`.
- The ninth row of the **“Other reference data”** register in Recovery Workbench Reference Data and Lists of Values v3 is “Messages — screen and letter messages in English and Thai — owner: product owner; Legal and Compliance for customer wording — specified in Error and Message Standard; DL10.”

The intent of the review note is right: use fixed text now. The gap is ownership: the message table is an **unowned reference-data deliverable**. Record it as **OI-E1-042-004** and assign an owner. The natural owner is E1-043 (versioned reference data), with a `MESSAGE` LOV code and a handler; alternatively, a new Window 2 story.

### 6.2 What to do now

Use a fixed-text resolver with **one seam**. Controllers and services pass the message ID and placeholders; they never hold the sentence.

- `MessageResolver.resolve(messageId, args)` returns `{ messageId, textEn, textTh, ruleId }`.
- `FixedMessageCatalog` reads `config/messages-e1-042.csv`; `TableMessageCatalog` will read the message table later.
- Switch with `rwb.messages.source=fixed|table`. The IDs and placeholders do not change across the switch.
- Tests assert the **message ID** and the **placeholders**, not the English sentence. One golden contract test asserts the exact EN and TH text against the standard.
- Unknown message ID is a startup/build failure; do not invent a fallback code.
- English and Thai must have the same placeholder set.

The fixed text is exactly the text in story §14 and the Error and Message Standard:

| ID | English | Proposed Thai (pending DL10) |
|---|---|---|
| `MSG-P3-032` | `Parameter {name} has no value for {environment}. The service did not start.` | `พารามิเตอร์ {name} ยังไม่มีค่าสำหรับ {environment} ระบบจึงไม่เริ่มทำงาน` |
| `MSG-GEN-002` | `{field} must be between {min} and {max}.` | `{field} ต้องอยู่ระหว่าง {min} ถึง {max}` |
| `MSG-P1-002` | `The {source} load for {date} was refused: {check}. The previous load is still in use.` | `ระบบไม่รับข้อมูล {source} ของวันที่ {date} เนื่องจาก {check} ยังคงใช้ข้อมูลชุดก่อนหน้า` |
| `MSG-GEN-001` | `Enter {field}.` | `กรุณากรอก {field}` |
| `MSG-P7-002` | `You prepared this decision, so you cannot approve it.` | `คุณเป็นผู้จัดทำรายการนี้ จึงไม่สามารถอนุมัติได้` |
| `MSG-P3-015` | `There is no earlier version of {table} to return to.` | `ไม่มีฉบับก่อนหน้าของ {table} ให้ย้อนกลับ` |
| `MSG-P4-002` | `You cannot {action} here. Your role does not include it.` | `คุณไม่สามารถ{action}ได้ เนื่องจากบทบาทของคุณไม่มีสิทธิ์นี้` |
| `MSG-P4-001` | `You have no Recovery Workbench role. Ask your team manager to request one.` | `คุณยังไม่มีบทบาทใน Recovery Workbench กรุณาขอจากหัวหน้าทีมของคุณ` |
| `MSG-GEN-006` | `{system} is not available. Your request is queued and will be retried.` | `{system} ไม่พร้อมใช้งาน คำขอของคุณถูกจัดคิวและจะลองใหม่` |

Two corrections to the earlier note:

1. **Proposed Thai exists for all seven E1-042 messages.** Only DL10 approval is missing. The earlier statement “Thai text is not available” was inaccurate.
2. **`MSG-P4-001` is used by the 401 response but is missing from E1-042 §14.** Add it to the fixed catalog.

The API `Problem` schema carries both `messageCode` and `messageTh`. A fixed-English-only resolver leaves `messageTh` empty and fails a strict contract test; use the proposed Thai, labelled “proposed, pending DL10”.

### 6.3 Exit criterion for OI-E1-042-004

A `message` reference table (or `reference_row` with `table_code='MESSAGE'`) is created by a migration and loaded with the nine IDs above. `rwb.messages.source=table` in SIT. `MessageResolver` reads it by ID with no code change. A contract test proves EN and TH for every ID, with identical placeholders. `MessageLiteralCheck` reports zero hard-coded sentences. `GET /admin/parameters` as RW-PHONECOL returns 403 with `messageCode=MSG-P4-002` and a non-empty `messageTh`.

---

## 7. Open items register

| ID | Status | Open item | Why it matters | Linked to | Exit criterion |
|---|---|---|---|---|---|
| **OI-E1-042-001** | Open — test blocked | `TC-E1-042-12` cannot run in the E1-042 build window. The 403 path is delivered by E1-022 and the matrix it reads is loaded by E1-037; both are Window 2, after E1-042. The Physical Schema seed has 421/756 permission rows, no `-` rows, `matrix_version='1'`, and null `role.entra_group`. | The access test needs a real session and the approved matrix. A mock role would weaken the test. | **RWB-E1-022, RWB-E1-037** (secondary: E1-019, E1-043) | After E1-037 loads `PM-2026.11` and E1-022 resolves `RWB-SIT-RW-PHONECOL`, run the test. Expect 403, `problem+json`, `MSG-P4-002`, action `read parameters`, no parameter array/secret, one refusal event. Record Pass only on that evidence. Until then: **Blocked**. |
| **OI-E1-042-002** | Open — before commit | Requested migration names `V042_1` / `V042_2` fail D-RCV-28 (four-digit sequence, one file per story). | The migration lint will fail the build. | D-RCV-28, RWB-E1-044, RWB-E1-001 | Commit `V0042__rwb_e1_042_parameter_catalog_and_seed.sql`, or record a lint exception and get tech-lead approval for the split. |
| **OI-E1-042-003** | Open — data gap | The full Epic 1 `config/parameter-catalog.csv` is not in the client pack. This folder supplies a 13-row bootstrap catalog, not the full set. | The generator and `CatalogCompletenessCheck` need the full catalog; several required parameters are missing. | E1-042 §3 and build step 4; every Epic 1 story that names a parameter | Add the full CSV, rerun `Generate-ParameterSeed.ps1`, replace `V042_2`/`V0042`, and prove `CatalogCompletenessCheck` has zero findings. |
| **OI-E1-042-004** | Open — dependency / temporary deviation | The message table does not exist in Physical Schema v4 and no story owns it. E1-042 uses a fixed catalog. The “E1-043 #9” reference points to the ninth Messages row of the reference-data register; E1-043's own item 9 is `TEMPLATE` and its 13 codes exclude `MESSAGE`. | Wording changes must be data loads, not code releases; the API returns `messageTh`. | New message-table story or an E1-043 scope addition; Error and Message Standard v3; RWB-E1-022 for `MSG-P4-001` | The message table is created and loaded with the nine IDs; `rwb.messages.source=table`; a contract test proves EN/TH and placeholders; `MessageLiteralCheck` has zero findings. |
| **OI-E1-042-005** | Open — documentation | No consolidated per-code CSV template register. Each handler owns its header; several codes have no defined header. | A loader cannot be built safely from an undefined template; users cannot know what to upload. | RWB-E1-043, each owning table story | Publish one template per LOV-REF-TABLE code with header, types, key columns and target, approved by the table owner. Start with `PRODUCT_PARAMETER`, `SERVICE_LEVEL`, `QUEUE`, `QUEUE_MEMBER`, `DELEGATION_LIMIT`, `DOCUMENT_CHECKLIST`. |
| **OI-E1-042-006** | Open — decision | Parameter naming conflicts: `case.entry.dpd` vs `case.entry.dpd_threshold` vs `ENTRY_DPD`; `legal.prescription.warn.days` (180) vs `prescription.warning-days` (90); `recon.caselist.tolerance.pct` vs `recon.tolerance.pct`. | Two keys for one concept produce two owners and two values; the completeness check can pass while the wrong key is read. | DL16, DL22, DL25; E1-002, E1-028, E1-045, Epic 2 | One approved key per concept. Record the decision in the decision log, update the catalog CSV and the reading code, and add a regression test that the retired key is absent. |
| **OI-E1-042-007** | Open — build tool | `PRODUCT`-scope catalog rows have no `default_value` by design, but `CatalogCompletenessCheck` is specified to fail on a catalog line with no default. | A correct product catalog would fail the build. | E1-042 build step 3; E1-045 | `CatalogCompletenessCheck` exempts `scope='PRODUCT'` from the default requirement (and still requires owner, type and range). Add a fixture with a product-scope row. |
| **OI-E1-042-008** | Open — contract/schema | `parameter_value` has no `load_id`, but the approve endpoint is `{loadId}/approve`. The `PARAMETER` handler writes `parameter_value` directly, so the load cannot be resolved by `loadId`. | Approve and rollback cannot find the rows a load created; the maker-checker flow is not implementable as specified. | E1-042 §12; E1-043 approve/rollback; Physical Schema v4 | Add `load_id uuid` (indexed) to `parameter_value` and write one value per load, **or** create a `parameter_load` header table. Update the physical schema and add an approve/rollback integration test. |
| **OI-E1-042-009** | Open — deployment config | `spring.flyway.placeholders.schema` defines `schema`, not `recoverySchema`; the SQL uses `${recoverySchema}`. | The placeholder is not replaced and the migration fails. | RWB-E1-044 §12; D-RCV-28 | Set `spring.flyway.placeholders.recoverySchema=${RWB_SCHEMA}` in every environment and prove a clean migration run. |
| **OI-E1-042-010** | Open — cross-story | `PRODUCT` has two targets in the pack (`reference_row` in E1-045, `data_product` in E1-001); `DOCUMENT_HUB_PARAMETER` is named in the API but has no LOV-REF-TABLE row; `RETENTION_CLASS` writes a table that Physical Schema v4 does not define. | A load either writes the wrong store, is refused as an unknown code, or fails on a missing table. | E1-001, E1-043, E1-045, E1-024, E1-041, P5 | One target per code, recorded in `ReferenceTableSchemas`; add the missing LOV rows + handlers or remove the names from the API description; add the missing table migration. |
| **OI-E1-042-011** | Open — API contract hardening | The OpenAPI operation has no `required:` array, `table` has no LOV enum, `validFrom` has no `format: date`, and the repeat-load status is inconsistent (201 only vs 200 vs 409). | Validators do not enforce the contract; clients cannot tell whether an identical repeat is a success or a conflict. | API Specification v2; E1-043 §12; RWB-E1-042 §12 | Add `required: [file, table, validFrom]`, `x-list-of-values: LOV-REF-TABLE` on `table`, `format: date` on `validFrom`, and record 201 for first load / 201 same body for identical repeat / 409 for different content at an approved `validFrom`. Add contract tests. |

---

## 8. Verification evidence

The SQL was executed against **PostgreSQL 17-alpine** in a Docker container. The test script and the full output are in `tests/` and `evidence/`.

| Test | Result |
|---|---|
| Consolidated migration on a clean schema | 13 catalog rows, 28 value rows, 9 `parameter_value` constraints, 4 E1-042 indexes |
| Re-run of the consolidated migration | Counts unchanged; idempotent |
| Split review files on a clean schema | 13 catalog rows, 28 value rows |
| E1-001 baseline overlap (tables already exist) | Adds the FK and five catalog checks without error; seed applies |
| Duplicate global version with NULL `product_group` | Refused by `ux_parameter_value_version_all` |
| Approver = author | Refused by `ck_parameter_value_maker_checker` |
| Secret with a default value | Refused by `ck_parameter_catalog_secret_default` |
| Value for an unknown key | Refused by `fk_parameter_value_catalog` |
| `APPROVED` row with no `approved_at` | Refused by `ck_parameter_value_approved_at` |
| `valid_to` before `valid_from` | Refused by `ck_parameter_value_dates` |
| Second approved version at the same `valid_from` | Refused by `ux_parameter_value_approved_from` |
| Invalid environment | Refused by `ck_parameter_value_environment` |
| Deployment guard with a required key and no value | Refused with “seed incomplete” |

The full output ends with:

```text
ok: deployment guard refused a required key with no value

ALL MIGRATION TESTS PASSED
```

To rerun:

```powershell
docker run --rm -d --name rwb-e1-042-pg -e POSTGRES_PASSWORD=test -e POSTGRES_DB=rwb `
  -v "${PWD}\sql:/work/sql:ro" -v "${PWD}\tests:/work/tests:ro" postgres:17-alpine
# wait for pg_isready, then:
docker exec rwb-e1-042-pg sh -c "tr -d '\r' < /work/tests/test_migrations.sh > /tmp/t.sh && bash /tmp/t.sh"
```

**Post-migration checks for a real environment:**

```sql
SELECT count(*) AS catalog_rows FROM recovery.parameter_catalog;          -- expect 13 for this seed
SELECT count(*) AS value_rows   FROM recovery.parameter_value;            -- expect 28 for this seed

SELECT param_key, environment, param_value, version_no, status, valid_from
FROM recovery.parameter_value
WHERE param_key = 'case.entry.dpd'
ORDER BY environment, valid_from;

SELECT conname FROM pg_constraint
WHERE conrelid = 'recovery.parameter_value'::regclass
ORDER BY conname;

SELECT indexname FROM pg_indexes
WHERE schemaname = 'recovery' AND tablename IN ('parameter_catalog','parameter_value')
ORDER BY indexname;
```

The counts are for the bootstrap seed. After the full CSV lands, the expected counts change; the structural checks stay the same.

---

## 9. Decisions requested from the client

| # | Decision | Recommended answer |
|---:|---|---|
| 1 | Commit the two requested files, or the single D-RCV-28 file? | Commit `V0042__rwb_e1_042_parameter_catalog_and_seed.sql`; keep the split as review copies. If the split is mandatory, approve a lint exception in writing. |
| 2 | Confirm the Flyway placeholder property. | `spring.flyway.placeholders.recoverySchema=${RWB_SCHEMA}`. |
| 3 | Resolve the parameter naming conflicts (entry threshold, prescription warning, reconciliation tolerance). | One key per concept; record in the decision log and update the catalog before SIT. |
| 4 | Who owns the message table, and when? | Assign it to E1-043 (with a `MESSAGE` code) or a new Window 2 story; use the fixed resolver meanwhile. |
| 5 | Defer TC-E1-042-12 to E1-037 exit? | Yes. Record Blocked with OI-E1-042-001; execute after `PM-2026.11` and the RW-PHONECOL group are in SIT. |
| 6 | Who publishes the missing CSV templates? | The owning stories: E1-045 (`PRODUCT_PARAMETER`, `SERVICE_LEVEL`), E1-019 (`QUEUE`, `QUEUE_MEMBER`), E1-038 (`DELEGATION_LIMIT`), E1-040 (`DOCUMENT_CHECKLIST`). |
| 7 | How is a `PARAMETER` load linked to `{loadId}`? | Add `load_id uuid` to `parameter_value` (recommended) or a `parameter_load` header table. |
| 8 | Repeat-load status: 201 or 200, and when is 409 correct? | 201 with the same body for an identical repeat; 409 only for different content at an approved `validFrom`. Record it in the API specification. |
| 9 | Is `PRODUCT` written to `reference_row` or `data_product`? | One target, recorded in `ReferenceTableSchemas`; E1-045's `reference_row` is the current direction for the load, while `data_product` remains the data-product catalog. |

---

## Appendix A — Epic 1 parameter candidates not in the bootstrap seed

These keys are named in the Epic 1 and Epic 2 stories but are **not** in the 13-row bootstrap seed. They are listed so the client can complete `config/parameter-catalog.csv` under OI-E1-042-003. They are **candidates**, not approved rows: confirm the owner, type, unit, range, required flag and default with the owning story before adding them.

| Key | Documented default | Type | Source | Note |
|---|---|---|---|---|
| `allocation.deviation.queue.code` | `DEV-HANDLER` (assumed) | STRING | E1-020 | Candidate |
| `allocation.exception.queue.code` | `RWB-EXC` (assumed) | STRING | E1-020 | Candidate |
| `appraisal.max.age` | `365` (assumed) | INTEGER | E1-009 | Candidate |
| `booking.missing.grace_loads` | `1` | INTEGER | Epic 2 | Candidate; key uses `_` |
| `case.entry.dpd_threshold` | `90` (assumed) | INTEGER | Epic 2 | **Conflict** with `case.entry.dpd` |
| `caserecord.section.timeout.ms` | `3000` (assumed) | INTEGER | E1-023, E1-035 | Candidate |
| `caseview.deviation-timeout-ms` | `2000` | INTEGER | Epic 2 | Candidate |
| `efs.history.action.codes` | every `LOV-ACTION-CODE` (assumed) | CODE_LIST | E1-004 | Candidate |
| `jobs.allocation.deadline` | `07:00` | TIME | TE-007 | Candidate |
| `jobs.catch-up.max-dates` | `5` (assumed) | INTEGER | TE-007 | Candidate |
| `jobs.timer-check.cron` | `0 0/5 * * * ?` | STRING | TE-007 | Candidate |
| `legal.prescription.warn.days` | `180` (assumed) | INTEGER | E1-028 | **Conflict** with `prescription.warning-days` |
| `load.hold.tolerance.pct` | `0.50` (assumed) | DECIMAL | E1-003, E1-009 | Candidate |
| `load.movement.tolerance.pct` | `10.00` (assumed) | DECIMAL | E1-003, E1-004, E1-009 | Candidate |
| `load.retry.interval` | `60` | INTEGER | E1-003 | Candidate |
| `load.sample.size` | `50` | INTEGER | E1-003 | Candidate |
| `load.window.end` | `09:00` | TIME | E1-003 | Candidate |
| `load.window.end.INT-07` | `08:00` (assumed) | TIME | E1-004 | Candidate |
| `plan.warn-days` | `3` (assumed) | INTEGER | Epic 2 | Candidate |
| `prescription.warning-days` | `90` (assumed) | INTEGER | Epic 2 | **Conflict** with `legal.prescription.warn.days` |
| `queue.cap.max` | `500` (assumed), range 1–500 | INTEGER | E1-019 | Candidate |
| `queueview.page-size.default` | `50` | INTEGER | Epic 2 | Candidate |
| `queueview.page-size.max` | `200` | INTEGER | Epic 2 | Candidate |
| `recon.efs.alert_pct` | `0.1` (assumed) | DECIMAL | Epic 2 | Candidate |
| `recon.efs.clean_days_required` | `10` | INTEGER | Epic 2 | Candidate |
| `recon.tolerance.pct` | `0.00` (assumed) | DECIMAL | E1-011 | **Conflict** with `recon.caselist.tolerance.pct` |
| `restructure.max_breaks` | `2` | INTEGER | Epic 2 | Candidate |
| `rules.testcases.min` | `50` (assumed) | INTEGER | E1-029 | Candidate |
| `timeline.source-timeout-ms` | `2000` | INTEGER | Epic 2 | Candidate |
| `timeline.type.order` | decision, status change, assignment, transfer, contact, document | CODE_LIST | E1-035 | Candidate |
| `tracker.file.max.mb` | `20` (assumed) | INTEGER | E1-010 | Candidate |
| `tracker.inventory.teams` | TDR, DIL, LIT, NPA, DEBT_SALE, WRITE_OFF (assumed) | CODE_LIST | E1-005, E1-012 | Candidate |
| `tracker.retire.parallel.days` | `2` | INTEGER | E1-012 | Candidate |
| `transfer.bulk.max` | `50` (assumed) | INTEGER | Epic 2 | Candidate |

The 92 environment settings and `rwb.*` properties named in the stories are also candidates, but they are platform configuration owned by RW-PLATADM and should be added by that owner, not by the business catalog review. They are deliberately not listed here to keep the business review readable.

---

## 10. Summary

- The two requested SQL files are provided, tested, and also assembled into the D-RCV-28-compliant single migration. Commit the single file unless a lint exception is approved.
- The DDL is complete and guarded against the E1-001 baseline; it enforces key uniqueness, typed value metadata, environment/status/date rules, maker-checker, the foreign key, NULL-safe version uniqueness and one approved version per valid-from date.
- The seed is generated from a 13-row bootstrap catalog CSV and produces 28 value rows. It is deliberately conservative: only documented defaults and owners are seeded. The full Epic 1 catalog remains OI-E1-042-003.
- `POST /admin/reference-loads` is a **table-code** endpoint, one code per call. The user does not choose a database table or a column, and cannot supply a `{dbTable}.{dbColumn}` mapping. `PARAMETER` uses `key,environment,value`.
- The build-time CSV and the runtime CSV are different files. The build generates `ParameterKeys` and the seed; the runtime upload changes values only.
- TC-E1-042-12 is **Blocked**, not Failed, until E1-022 and E1-037 deliver the session roles and the permission matrix. Do not mock the role.
- Messages use a fixed-text resolver with one seam. Proposed Thai exists for all messages; only DL10 approval is missing. The message table is unowned and must be assigned.
- Eleven open items are recorded; the three that most affect SIT are the full catalog CSV, the role test, and the `loadId` link.
