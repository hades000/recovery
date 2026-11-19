# Technical Specification — RWB-E1-001 Recovery tables for the 14 data products

| Field | Value |
|---|---|
| Story | RWB-E1-001 — Recovery tables for the 14 data products |
| Epic / module | E1 (release 30 November 2026) / P1 Recovery data engine |
| RUN_ID | `INC-009-epic-1-RWB-E1-001` |
| Source requirement | Story file v7 (15 Nov 2026), `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-001-recovery-tables-for-the-14-data-products-v1.md`; increment card `docs/increments/INC-009-epic-1-RWB-E1-001.md` |
| Upstream IDs | REQ-RDF-001; FEAT-RDF-01, FEAT-RDF-02; `BR-RWB-013` / `FR-RWB-013` (Traceability Matrix §3, row 009); TC-E1-001-01 to TC-E1-001-12 |
| Governing decisions | D-RCV-35 (U1–U5) and D-RCV-36 (change register A.5, A.7, row 18); ADR-010; D-RCV-28 and D-RCV-29 (Decision Log v10); RWB-E1-001 Specification Rulings v2 (status Proposed) R1–R4 |
| Status | Spec gate round 1 `FAIL` (3 High, 6 Medium, 4 Low; `../review/spec-gate-review.md`) — remediation and re-review required |
| Prepared | 2026-11-17 |
| Author | Technical Specifier (agent run) |
| Approval | Product Owner (TBC); Compliance Reviewer spec gate (`../review/spec-gate-review.md`) |

## Sources and how they are cited

Short names used below. All `requirement/legacy/` paths are in the read-only document set
`17 AI-First SDLC Repository v2/requirement/legacy/`.

| Short name | Document (version) | Path |
|---|---|---|
| Story v7 | RWB-E1-001 story file v1 inside Epic 1 Story Files v7 | `04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-001-recovery-tables-for-the-14-data-products-v1.md` |
| PS v6 | Recovery Workbench Physical Schema v6 (16 Nov 2026) | `06-data/recovery-workbench-physical-schema-v6.sql` (byte-identical copy in `infra/postgres/schema/03-recovery-physical-schema-v6.sql`) |
| DL v10 | Recovery Workbench Decision Log v10 | `01-decisions-and-governance/recovery-workbench-decision-log-v10-xlsx.md` (D-RCV-28 line 77, D-RCV-29 line 78, D-RCV-36 line 84) |
| D-RCV-36 CR | D-RCV-36 Temporal and Drools change register | `aisdlc/docs/decisions/d-rcv-36-temporal-and-drools.md` (A.5, A.7, row 18) |
| D-RCV-35 | D-RCV-35 ACE DB alignment | `aisdlc/docs/decisions/d-rcv-35-ace-db-alignment.md` |
| Rulings v2 | RWB-E1-001 Specification Rulings v2 (Proposed) | `01-decisions-and-governance/recovery-workbench-rwb-e1-001-specification-rulings-v2.md` |
| MSG v4 | Error and Message Standard v4 | `07-screens-and-experience/recovery-workbench-error-and-message-standard-v4-docx.md` |
| API v4 | API Specification v4 | `api/recovery-api-v4.yaml` (repo copy), `/admin/reference-loads` line 3167 |
| E1-043 v7 / E1-042 v7 / E1-072 v7 | Story files in Epic 1 Story Files v7 | same folder as Story v7 |
| Baseline code | Repository as of 17 Nov 2026 | `RecoveryFlywayConfig`, `RecoveryMigrationLintTest`, `RecoveryDatabaseIT`, `infra/postgres/init/10-load-ace-database.sh`, `README.md` |

**Counting method** (used for every count in this spec). A Python parser read PS v6 lines 1–6130: every
`CREATE TABLE <name> (...)` block (columns = lines that are not `CONSTRAINT` or comments), every
single-line `INSERT INTO sys_objects` and `INSERT INTO sys_fields` statement (quote-aware value split),
and every `CREATE OR REPLACE VIEW recovery.v_ace_*`. Columns were compared with `sys_fields` by
object, field name and `physical_type`, with the seven standard columns (`is_active`, `state`,
`version`, `created_at`, `created_by`, `updated_at`, `updated_by`) treated separately. Result:

| Measure | PS v6 (this spec) | Story v7 (= Physical Schema v5) |
|---|---|---|
| Tables | 93 = 89 Workbench + 4 extension | 92 = 88 + 4 |
| `sys_objects` rows | 123 = 93 tables + 30 views (99 with a data product, 24 without: OPS 13, AGT 8, RPT 3) | 122 (98 + 24) |
| `sys_fields` rows | 1,379 = 1,075 on tables + 304 on views | 1,366 = 1,062 + 304 |
| Table fields | 1,075 = 1,026 on the 89 Workbench tables + 49 on the 4 extension tables | 1,062 = 1,013 + 49 |
| Non-standard table columns | 1,047 (every one has exactly one `sys_fields` row with the same physical type) | — |
| Duplicate `field_id` or (object, field) pairs | 0 | — |

The 28-row difference between 1,075 and 1,047 is the seven standard columns of each extension table,
which PS v6 records in `sys_fields` (extension tables have no `id`). On all other tables the standard
columns have no `sys_fields` row. Scripts and outputs: `evidence/count_v6.py`, `evidence/lint_v6.py`
(run with `python -I <script> <path to PS v6>`). PS v6 minus v5 = {`rule_package`, `rule_package_version`}; v5 minus
v6 = {`payment_match_rule`} (D-RCV-36 CR A.7 and T10).

## v2 baseline delta

No earlier RWB-E1-001 run exists in `output/` (no `_v2-baseline` folder). This is the first spec.

## Assumptions

Full list with evidence in `assumptions.md`. The ones that shape the design:

| ID | Assumption | Basis | Effect if wrong |
|---|---|---|---|
| `ASM-E1001-01` | The table set and dictionary counts are those of PS v6 (93 / 123 / 1,379; conformance 1,075 + 1,047), not the story's 92 / 122 / 1,366 / 1,062. | D-RCV-36 CR A.7 and row 18 (tier 1) outrank DL v10 D-RCV-29 "as held in … Physical Schema v5" and Story v7 §11. Story v7 §11 itself names PS v6 as the source. | Only the expected numbers in the tests change; the derivation rule (SPEC-002) is unchanged. |
| `ASM-E1001-02` | The migration takes the next free four-digit `<seq>` at merge; it is `V0001` when no other recovery migration has merged first. | DL v10 D-RCV-28 (tier 3) names the E1-001 baseline `V0001`; squad D-RCV-34 and the merge-order map (`V0003`) are not in DL v10 (OPEN-017) and the map says "a plan, not an allocation". | If another story merges first, the number changes and SPEC-001 rule (b) applies. |
| `ASM-E1001-03` | V0001 seeds the dictionary, `data_product`, `lov_value`, `role` and `permission` from PS v6, and no `rule_package` or `delegation_limit` rows. | DL v10 D-RCV-29 lists exactly these seeds; Rulings v2 R3 and PS v6 line 5773 (no `delegation_limit` rows); E1-072 v7 seeds its own package codes. | If the 8 PS v6 `rule_package` rows belong in V0001, add PS v6 lines 5340–5348 to the seed (one-section change). |
| `ASM-E1001-04` | The `data_product` seed uses the Story v7 §13 values, not the PS v6 seed wording. | Story v7 §13 says the seed is "inserted by the migration and repeated in the first catalog load file"; the PS v6 wording ("ACE (from ALS via COLLINS)", "Workbench") would fail BR3. | The seed rows change; no structural change. |
| `ASM-E1001-05` | `ReferenceTableHandler`, `ReferenceLoadFile` and `ValidationReport` are published by RWB-E1-043 with the Story v7 §12 signature, and RWB-E1-043 calls `validate` on load and `apply` on approval. | Story v7 §3 precondition and §12; E1-043 v7 does not define the interface (gap `GAP-E1001-07`). | The handler adapts to the published seam; ACs 3, 7–11 and TC-E1-001-11 run when INC-008 is built. |
| `ASM-E1001-06` | Messages MSG-P1-003, -004, -007 and -011 are held as fixed English text in code until a message table exists. | No message table in PS v6; README decision 5; E1-042 pack OI-E1-042-004. | Moving them to a message table is a data change; the IDs and texts stay. |
| `L-RCV-03` | No question was asked. Ambiguities are recorded here, in `document-gaps.md` and in `shared-updates.md`. | No-question rule. | A wrong default is visible at the spec and plan gates. |

## Change Scope Declaration

| Field | Value |
|---|---|
| Change Type | `NEW_STORY` |
| UI In Scope | `NO` — Story v7 §15: "No screen in this story". |
| Logic In Scope | `YES` — catalog validation (BR2, BR3, BR5, list values), versioned apply, conformance test. |
| API In Scope | `YES` — the story's catalog load uses the existing `POST /admin/reference-loads` (API v4) with `table = data_product`. No endpoint is added or changed. |
| API Impact Type | `NO_API_CHANGE` |
| Impacted Existing Nodes | `backend/src/main/resources/db/modulemigration/recovery/` (first file); `RecoveryMigrationLintTest` (string-literal rule, SPEC-011); `RecoveryDatabaseIT` and the local start path while `RWB_LOAD_REFERENCE_SCHEMA=true` (SPEC-010); RWB-E1-043 load/approve flow (handler registration); `RecoveryFlags` (`rwb.p1.data-catalog`). |
| New Nodes Required | `YES` — `V<seq>__rwb_e1_001_recovery_schema.sql`; nested module `dataengine` with `catalog` (`DataProduct`, `DataProductRepository`, `DataProductCatalogHandler`, `DataProductCatalogMessages`); `DataDictionaryConformanceTest`; `RecoverySchemaMigrationIT` (tag `recovery-it`). |
| Inherited Existing Behavior | `RecoveryFlywayConfig` (history table `flyway_schema_history_recovery`, `${recoverySchema}`, `baselineOnMigrate(true)`, baseline `0`, `createSchemas(false)`, clean disabled); local init roles and grants (`00-roles-and-databases.sh`, `20-grants.sql.inc`); Problem error body (`ApiError`, `ProblemFactory`); MSG-P4-002 handling; method security. |
| Frontend Changes Required | `NO` |
| Backend Changes Required | `YES` — migration, entity, repository, handler, flag, tests. |

## Requirement-to-SPEC Logic Coverage

| REQ_REF | Requirement Logic Statement | Mapped SPEC-* | Coverage Type | Implementation Notes | Status |
|---|---|---|---|---|---|
| BR1 | Every table and view column has exactly one dictionary row with field ID, types, source and meaning. | SPEC-RWB-E1-001-006, -009 | DIRECT | Seeds 1,379 rows; conformance test on tables; view columns are checked by RWB-E1-069 (BR9). | COVERED |
| BR2 | Workbench data is held in the 14 data products DP01–DP14. | SPEC-RWB-E1-001-004, -006, -013 | DIRECT | Seed 14 rows; load must hold exactly DP01–DP14 (MSG-P1-004). | COVERED |
| BR3 | One system of record in the stated form and one named owner per product. | SPEC-RWB-E1-001-013 | DIRECT | Rule SOR-1 to SOR-4; owner user ID required; MSG-P1-003. | COVERED |
| BR4 | Catalog values are a versioned load; a load with any exception is refused in full. | SPEC-RWB-E1-001-013, -014 | DIRECT | `validate` writes nothing; `apply` is one transaction. | COVERED |
| BR5 | A multi-source product names ACE and its sources; a bare source name is refused. | SPEC-RWB-E1-001-013 | DIRECT | SOR rules; completeness of the source list is not machine-checked (`ASM-E1001-09`). | COVERED |
| BR6 | Parameterised schema, one migration per story, forward only. | SPEC-RWB-E1-001-001, -002, -008, -011 | DIRECT | `${recoverySchema}` only; lint. | COVERED |
| BR7 | Personal fields carry `is_personal = true`. | SPEC-RWB-E1-001-006 | DIRECT | Seeded from PS v6 as written. | COVERED |
| BR8 | No constraint into `public`; ACE links are `varchar(255)` keys with no FK. | SPEC-RWB-E1-001-003 | DIRECT | 16 key columns, all `varchar(255)`, none in an FK (PS v6). | COVERED |
| BR9 | V0001 seeds the dictionary for tables and the 30 views before the views exist. | SPEC-RWB-E1-001-006, -002 | DIRECT | 30 view objects and 304 view fields seeded; no view created. | COVERED |
| AC1 | Schema deployed: table set, removed tables absent, no constraint into public, business keys, conformance. | SPEC-RWB-E1-001-002, -003, -009, -010 | DIRECT | Counts per PS v6 (`ASM-E1001-01`). | COVERED |
| AC2 | `v_data_dictionary` returns the stated rows for `v_ace_account.days_past_due` and `account_ext.dispute_open`. | SPEC-RWB-E1-001-005, -006 | DIRECT | View per Story v7 §12 / Rulings v2 R2. | COVERED |
| AC3 | After the catalog load, 14 rows with the stated DP01, DP03 and DP06 values. | SPEC-RWB-E1-001-013, -014 | DIRECT | End-to-end needs the E1-043 seam (`ASM-E1001-05`). | COVERED |
| AC4 | A failing statement rolls the whole migration back; no successful history row. | SPEC-RWB-E1-001-007 | DIRECT | One transaction. | COVERED |
| AC5 | Conformance test fails on a column with no dictionary row and on a type mismatch, with the stated texts. | SPEC-RWB-E1-001-009 | DIRECT | Messages fixed. | COVERED |
| AC6 | A re-run applies nothing and leaves counts unchanged. | SPEC-RWB-E1-001-008 | DIRECT | Counts 123 / 1,379 (`ASM-E1001-01`). | COVERED |
| AC7 | Two systems of record (DP06) and no owner (DP11) refuse the load with MSG-P1-003 for both. | SPEC-RWB-E1-001-013, -015 | DIRECT | All findings reported. | COVERED |
| AC8 | 13 rows without DP09 refuse the load with MSG-P1-004 naming DP09. | SPEC-RWB-E1-001-013, -015 | DIRECT | — | COVERED |
| AC9 | Owner role and refresh cycle outside their lists refuse the load with two MSG-P1-007 texts. | SPEC-RWB-E1-001-013, -015 | DIRECT | LOV-ROLE resolved through `role` (`ASM-E1001-10`). | COVERED |
| AC10 | The same file again writes nothing and returns MSG-P1-011. | SPEC-RWB-E1-001-014, -015 | DIRECT | Content hash equals the version in force. | COVERED |
| AC11 | A bare source name ("CCMS") refuses the load with the MSG-P1-003 text. | SPEC-RWB-E1-001-013, -015 | DIRECT | Rule SOR-4. | COVERED |
| X1–X3 | Migration failure, conformance failure, re-run. | SPEC-RWB-E1-001-007, -008, -009 | DIRECT | Pipeline log only. | COVERED |
| X4–X7 | Catalog refusals and repeat file. | SPEC-RWB-E1-001-013, -014, -015 | DIRECT | — | COVERED |
| X8 / TC-E1-001-11 | A role without Reference data C gets 403 with MSG-P4-002. | SPEC-RWB-E1-001-016 | INHERITED | Enforced by the E1-043 endpoint method check; this story adds the access test case. | COVERED |
| §10 Authority | RW-REFADM loads (C); RW-DATASTEW confirms (U); pipeline identity migrates. | SPEC-RWB-E1-001-014, -016 | DIRECT | Approval right conflict recorded (`GAP-E1001-08`). | COVERED |
| §12 Contract | View columns; handler interface; 422/403 responses; idempotency; migration trigger/restart. | SPEC-RWB-E1-001-005, -012, -013, -014, -015 | DIRECT | — | COVERED |
| §13 Solution plan | Components, database, feature flag, build steps 1–7. | SPEC-RWB-E1-001-001 to -017 | DIRECT | Path and package per repo (`GAP-E1001-10`). | COVERED |
| §17 Guardrails | No business value in code; no personal data; no ACE table read; no constraint into public; dictionary reads only recovery tables. | SPEC-RWB-E1-001-003, -005, -017 | DIRECT | — | COVERED |
| §19 Out of scope | `v_ace_*` views, grants and view conformance (E1-069); freshness (E1-015); access/masking (E1-016); retention (E1-017); dictionary endpoint (E1-064). | SPEC-RWB-E1-001-002 | DIRECT | Excluded explicitly. | COVERED |

## User story intent interpretation

Create the recovery schema's tables and the data dictionary as one forward-only migration taken from
PS v6, publish the dictionary as a view, and let the reference data administrator load the catalog
of the 14 data products as versioned reference data that is refused in full on any error. The story
creates no screen, reads no ACE table and creates no `v_ace_*` view (Story v7 §15, §17, §19).

## Entry trigger and preconditions

| Trigger | Preconditions |
|---|---|
| Recovery Flyway runs at application start (`RecoveryFlywayConfig`, `initMethod = "migrate"`) in each environment; in SIT and above through the second pipeline step (OPEN-013 resolution). | Schema `recovery` exists and is empty of Workbench tables (DBA creates it, `createSchemas(false)`; OPEN-014 resolution); extension `pgcrypto` exists (local: `10-load-ace-database.sh`); `rwb_migrator` holds DDL; RWB-E1-044 Flyway bean present (baseline A-04). |
| `POST /admin/reference-loads` with `table = data_product` (API v4) and approval of that load (E1-043). | RWB-E1-043 built and the `data_product` handler registered; `data_product` accepted as a table code (`GAP-E1001-06`); flag `rwb.p1.data-catalog` on; caller holds Reference data C. |
| Query of `v_data_dictionary` by a developer or data steward. | Read access to schema `recovery` (Story v7 §3). |

## Detailed design

### SPEC-RWB-E1-001-001 Migration file identity

- Location `backend/src/main/resources/db/modulemigration/recovery/` (repo baseline and RUN-BRIEF;
  Story v7 §13's `db/migration/recovery` is superseded, `GAP-E1001-10`).
- Name `V<seq>__rwb_e1_001_recovery_schema.sql`; line 1 exactly `-- Story: RWB-E1-001`; no line 2
  `-- Fix:`. One non-fix file for the story; no `R__` file (D-RCV-28; `RecoveryMigrationLintTest`).
- `<seq>`: (a) `0001` when no recovery migration has merged before it (DL v10 D-RCV-28); (b) otherwise
  the next free number, and the file then omits any table, index, trigger or seed row that an earlier
  merged recovery migration already created, so that the end state equals SPEC-002. The lint's
  contiguous-sequence rule applies. Tests identify the migration by its script name and
  `success = true` in `flyway_schema_history_recovery`, not by a version literal.
- The story's "Flyway version 1.001" (Story v7 §9, §12, AC4, AC6) is read as "the version of this
  migration" (`GAP-E1001-04`).

### SPEC-RWB-E1-001-002 Derivation from Physical Schema v6

The migration body is PS v6 lines 16–6130 in file order, transformed as follows and nothing else:

| # | PS v6 content | Treatment |
|---|---|---|
| T1 | Lines 10–12 `CREATE SCHEMA IF NOT EXISTS recovery`, `SET search_path TO recovery`, `CREATE EXTENSION IF NOT EXISTS pgcrypto` | Removed. Schema is created by the DBA (`createSchemas(false)`); `SET search_path` is forbidden (lint); the extension is an environment precondition. |
| T2 | Every reference to a recovery object (table, view, constraint target, index target, trigger target, function, `COMMENT ON` target, `INSERT INTO`) | Qualified as `${recoverySchema}.<name>`. No literal `recovery.`, `ace.` or `public.` outside string literals. |
| T3 | Line 2156 `CREATE VIEW v_data_dictionary` | Replaced by SPEC-005. |
| T4 | Lines 3516–3531 `data_product` seed | Replaced by SPEC-006 seed values (`ASM-E1001-04`). |
| T5 | Lines 5340–5348 `rule_package` seed | Not carried (`ASM-E1001-03`, `GAP-E1001-05`). |
| T6 | From line 6131: `v_ace_*` views, `ace_to_date`, `ace_to_boolean`, `ace_mask_value` and the commented grants (line 6823) | Not carried. RWB-E1-069 owns them (Story v7 §3, §19). |
| T7 | Any `GRANT` / `REVOKE` | None (lint; grants are the init script's `ALTER DEFAULT PRIVILEGES` locally and the view story's in SIT+). |

Nothing else is added: no `IF NOT EXISTS`, no `DROP`, no `CONCURRENTLY`, no data outside schema
`${recoverySchema}` (Story v7 §17).

### SPEC-RWB-E1-001-003 Table set, constraints and business keys

- Exactly the 93 `CREATE TABLE` statements of PS v6: 89 Workbench tables (including `data_product`,
  `sys_objects`, `sys_fields`, `rule_package`, `rule_package_version`) and the extension tables
  `party_ext`, `contact_point_ext`, `account_ext`, `valuation_ext` (D-RCV-35 U3; names to be confirmed
  under OPEN-033).
- None of the 20 tables named in AC1, and no `payment_match_rule` (D-RCV-36 T10).
- The 92 foreign keys of PS v6 §"References between tables" (from line 2182), all between recovery
  tables; the 112 indexes; the CHECK constraints on `rule_package.hit_policy`,
  `rule_package_version.status` and `contact_point_ext.contact_type`; `refuse_change()` and the triggers
  `tr_declog_append_only` and `tr_interaction_append_only` (PS v6 line 2389); the `COMMENT ON`
  statements (from line 2398).
- No constraint references schema `public` (PS v6 has none). The 16 ACE link columns
  (`account_key` ×5, `person_key` ×6, `asset_key` ×2, `contact_key` ×2, `payment_code` ×1) are
  `varchar(255)` and take part in no foreign key (BR8).

### SPEC-RWB-E1-001-004 `data_product` table

As PS v6 line 815: `id uuid PRIMARY KEY DEFAULT gen_random_uuid()`, `product_code varchar(25) NOT
NULL` with `uk_data_product UNIQUE (product_code)`, `product_name varchar(80) NOT NULL`,
`definition varchar(400) NOT NULL`, `system_of_record varchar(120) NOT NULL`, `owner_role
varchar(20) NOT NULL`, `owner_user_id uuid`, `refresh_cycle varchar(10) NOT NULL`, `expected_by
varchar(20)`, `valid_from date NOT NULL`, and the seven standard columns. Story v7 §13 names
`product_code` as primary key; PS v6 governs because Story v7 §11 counts 10 dictionary fields
DF-REF-070 to 079 including `id` (`GAP-E1001-09`). `fk_sys_objects_data_product` references
`data_product (product_code)` and `sys_objects.data_product` stays nullable (Rulings v2 R1; Story v7
§13). The `data_product` rows are inserted before `sys_objects` (PS v6 line 3516).

### SPEC-RWB-E1-001-005 `v_data_dictionary`

Created by the migration, reading only `sys_fields`, `sys_objects` and `data_product`:

```sql
CREATE VIEW ${recoverySchema}.v_data_dictionary AS
SELECT o.object_name AS entity, f.field_name AS field, f.field_id, f.data_type, f.physical_type,
       f.is_mandatory, f.lov_code, f.references_object, f.source_system, f.source_field,
       f.is_personal, o.data_product, o.system_of_record AS entity_system_of_record,
       p.system_of_record AS product_system_of_record, p.refresh_cycle, p.owner_role,
       p.owner_user_id, f.late_behavior, f.interface_id, f.description
FROM ${recoverySchema}.sys_fields f
JOIN ${recoverySchema}.sys_objects o ON o.object_name = f.object_name
LEFT JOIN ${recoverySchema}.data_product p ON p.product_code = o.data_product AND p.is_active
WHERE f.is_active AND o.is_active;
```

Columns per Story v7 §12; `owner_role` from `data_product` and the two system-of-record columns per
Rulings v2 R2 §3.3. The PS v6 view (`f.owner_role`, no system-of-record columns) is not used
(`GAP-E1001-03`).

### SPEC-RWB-E1-001-006 Seed rows

| Table | Rows | Source |
|---|---|---|
| `data_product` | 14: DP01–DP14 with code, name, definition, system of record, refresh cycle and expected-by exactly as Story v7 §13 seed table; `owner_role = 'RW-DATASTEW'`; `owner_user_id` NULL; `valid_from = DATE '2026-11-30'` | Story v7 §13 |
| `sys_objects` | 123 as PS v6 (93 tables, 30 `v_ace_*` views; 24 with NULL `data_product`) | PS v6; D-RCV-36 |
| `sys_fields` | 1,379 as PS v6, including DF-EXT-001 to 049, DF-REF-274 to 299 and the 304 `DF-ACE-*` view fields | PS v6; D-RCV-36 CR A.5 |
| `lov_value` | 598 as PS v6 (from line 4684) | DL v10 D-RCV-29 |
| `role` | 54 as PS v6 (from line 5284) | DL v10 D-RCV-29 |
| `permission` | 421 as PS v6 (from line 5350) | DL v10 D-RCV-29 |
| `delegation_limit` | 0 | DL v10 D-RCV-29; Rulings v2 R3 |
| `rule_package`, `rule_package_version` | 0 | `ASM-E1001-03` |
| Every other table | 0 | Story v7 §11 ("tables only; no rows") |

No seed row carries personal data. `owner_user_id` values exist only in environment load files
(synthetic users in DEV and SIT, Story v7 §3).

### SPEC-RWB-E1-001-007 Atomic migration

The file runs in one PostgreSQL transaction (Flyway default; SPEC-002 forbids non-transactional
statements). If any statement fails, Flyway reports the failing statement, no object or row of the
migration remains, and `flyway_schema_history_recovery` has no row with `success = true` for it
(AC4, X1). A restart applies the whole file again (Story v7 §12 "Restart").

### SPEC-RWB-E1-001-008 Re-run and checksum

A second `migrate` on a schema where the migration is applied applies nothing; `sys_objects` stays at
123 and `sys_fields` at 1,379 (AC6, X3). A changed checksum on the applied file fails Flyway
validation (Story v7 §12 "Idempotency"; AGENTS §4.6: a merged migration is never edited).

### SPEC-RWB-E1-001-009 `DataDictionaryConformanceTest`

Runs against the Flyway-built schema (SPEC-010) and compares `information_schema.columns` for every
base table in `${recoverySchema}` with `sys_fields` rows whose `object_name` is that table:

| Check | Pass condition (PS v6) | Failure text (Story v7 AC5) |
|---|---|---|
| C1 column → field | Every column except the seven standard columns has exactly one `sys_fields` row: 1,047 of 1,047. | `<table>.<column> has no data dictionary entry` |
| C2 field → column | Every `sys_fields` row on a table names an existing column: 1,075 of 1,075 (includes the 28 extension-table standard columns). | `<field_id> has no column <table>.<field>` (`ASM-E1001-11`) |
| C3 type | For each matched pair, the normalised column type equals `physical_type` (`varchar(n)`, `numeric(p,s)`, `integer`, `bigint`, `boolean`, `date`, `timestamptz`, `uuid`, `text`, `jsonb`, arrays as `<type>[]`). | `<field_id> physical type <expected> expected, <actual> found` |

The test reports every failure, not only the first. Views are out of scope (BR9; RWB-E1-069). Proof
fixtures: an extra `account_ext.branch_code` column and `account_ext.dispute_open` altered to `text`
on a throwaway container schema, never in the migration folder.

### SPEC-RWB-E1-001-010 Build and test path for the schema

- `RecoverySchemaMigrationIT` (tag `recovery-it`, Testcontainers `postgres:16.16-alpine`, the repo
  `infra/postgres/init` scripts) starts with `RWB_LOAD_REFERENCE_SCHEMA=false`, so init creates only the
  roles, schema `recovery`, `pgcrypto` and the default privileges, and recovery Flyway applies the
  migration to an empty schema as `rwb_migrator`. It proves AC1, AC2 (with a synthetic catalog row
  update for DP01), AC4, AC5, AC6 and SPEC-002 exclusions (no `v_ace_*` view, no function
  `ace_to_date`).
- While `RWB_LOAD_REFERENCE_SCHEMA=true` (local default until V0001–V0003 exist, README "Local versus
  target"), PS v6 is already loaded at init, `baselineOnMigrate` baselines at `0`, and the migration
  would fail with "relation already exists" (`RecoveryFlywayConfig`). Therefore no start path may run
  recovery Flyway on a schema built by the reference load once the migration exists: on that path
  `rwb.flyway.enabled=false`. `RecoveryDatabaseIT` stays on the reference-load path for its view and
  grant assertions until RWB-E1-069; its Flyway baseline assertion moves to `RecoverySchemaMigrationIT`,
  which asserts the stronger condition (the migration row with `success = true` in
  `flyway_schema_history_recovery`). No assertion is removed without that replacement. (`ASM-E1001-07`,
  `GAP-E1001-11`.)
- End state, outside this story: when RWB-E1-069 ships V0002/V0003, `RWB_LOAD_REFERENCE_SCHEMA=false`
  becomes the default and Flyway builds the schema from scratch (README; migration folder README).

### SPEC-RWB-E1-001-011 Migration lint: string literals

PS v6 holds 297 `sys_fields` rows whose `source_field` is a string such as `'public.account.delay_days'`
(AC2 requires this value). `RecoveryMigrationLintTest` today flags any `public.<x>` outside `--`
comments, so the migration would fail the lint. The literal-schema and `SET search_path` checks ignore
the content of single-quoted SQL string literals (with `''` escapes). Existing negative cases stay
and still fail (`SELECT * FROM public.account`); a new case proves that
`INSERT … VALUES ('public.account.delay_days')` passes and `INSERT INTO public.x` fails. This narrows
the rule to schema references; it does not remove a check (BS-2.6; `GAP-E1001-12`).

### SPEC-RWB-E1-001-012 Module, entity and repository

- New nested module `th.co.scb.ace.demo.recovery.dataengine` with `api/` and `internal/` (P1 name
  `dataengine` per the TE-001 module map in `output/INC-002-epic-1-RWB-TE-001/_v2-baseline/specify/spec.md`).
  Story v7 §13 package `recovery.dataengine.catalog` maps to `dataengine.internal.catalog`; only the
  handler bean is exposed to RWB-E1-043 through its published interface.
- `DataProduct` (JPA entity on `${recoverySchema}.data_product`, schema from `rwb.schema`) and
  `DataProductRepository` (find all active, find by `product_code`). No other module reads
  `data_product` directly (BND-4).

### SPEC-RWB-E1-001-013 `DataProductCatalogHandler.validate`

Implements `ReferenceTableHandler` for table code `data_product` (`tableCode()` returns
`"data_product"`). Reads the file rows, writes nothing, and returns every finding in row order:

| Check | Rule | Message |
|---|---|---|
| K1 | The set of `product_code` values equals DP01–DP14, each once. | MSG-P1-004, `{products}` = missing codes in ascending order |
| K2 | `system_of_record` passes SOR-1 to SOR-4. | MSG-P1-003, `{product}` = the code |
| K3 | `owner_user_id` is present and a UUID. | MSG-P1-003 |
| K4 | `owner_role` is an active `role.role_code` (LOV-ROLE, `ASM-E1001-10`). | MSG-P1-007, `{field}` = `owner_role`, `{values}` = "the role codes in LOV-ROLE" |
| K5 | `refresh_cycle` is an active `LOV-REFRESH` value (DAILY, WEEKLY, MONTHLY, ON_CHANGE). | MSG-P1-007, `{values}` = the list in sort order |

System-of-record rules (BR3, BR5; AC3, AC7, AC11 and the Story v7 §13 seed values):

- SOR-1: the value starts with `ACE (ingested from ` followed by a non-empty source list and `)`, or
  starts with `Recovery Workbench`.
- SOR-2: after an `ACE (ingested from …)` prefix, any remainder must name `Recovery Workbench`
  (DP04, DP07); otherwise it is a second system of record (AC7 `ACE (ingested from CCMS); SVAF`).
- SOR-3: the value holds at most one `ACE (ingested from` and no `;`.
- SOR-4: anything else, including a bare source name (`CCMS`, AC11), is refused.

Row numbers count data rows from 1. Column schema, required fields and type checks belong to the
generic RWB-E1-043 load checks (E1-043 v7 §4 step 3).

### SPEC-RWB-E1-001-014 `DataProductCatalogHandler.apply` and idempotency

- Called by RWB-E1-043 when the load version is approved (Story v7 §4 steps 9–10; `ASM-E1001-05`).
- In one transaction, updates the 14 rows matched by `product_code` with the file values and
  `valid_from`, increments `version`, sets `updated_at` and `updated_by`; returns 14. Any failure rolls
  back all 14 (BR4). No row is inserted or deleted after the seed (`ASM-E1001-08`).
- A file whose content hash equals the version in force writes nothing and is answered with
  MSG-P1-011 (`{source}` = "data product catalog", `{date}` = valid from) (Story v7 §12, AC10).
  Hash and version history are RWB-E1-043's (`reference_version`, `reference_row`).

### SPEC-RWB-E1-001-015 Refusal response

A refused load returns HTTP 422 `application/problem+json` (API v4 `E422`, `Problem`): `messageCode`
= the code of the first finding (file-level K1 before row-level K2–K5); `detail` = every finding text
in order, so AC7 shows both DP06 and DP11 and AC9 shows both row 4 and row 5. The MSG-P1-011 repeat is
not an error (Story v7 §12) and returns the existing `ReferenceLoad` with the message in its response
as RWB-E1-043 defines for repeats (`GAP-E1001-13`).

Message texts (English, Story v7 §14):

| ID | Text |
|---|---|
| MSG-P1-003 | `{product} must name one system of record, written ACE (ingested from X) or Recovery Workbench, or both where the product holds both, and one named owner.` |
| MSG-P1-004 | `The catalog must hold the 14 data products DP01 to DP14. Missing: {products}.` |
| MSG-P1-007 | `Row {row}: {field} must be one of {values}.` |
| MSG-P1-011 | `The {source} load for {date} is already complete or running. It was not run again.` |

Thai text: from MSG v4 for P1-004, P1-007, P1-011; none exists for the Story v7 wording of P1-003
(`GAP-E1001-14`, OPEN-005). Held in code per `ASM-E1001-06`; tests assert `messageCode` and the
English text.

### SPEC-RWB-E1-001-016 Authority

- The load endpoint's method check (Reference data C) is RWB-E1-043's; this story adds the access case
  TC-E1-001-11: RW-DATASTEW (Reference data `RU` in the PS v6 permission seed, no `C`) calling the load
  with `table = data_product` gets 403 with MSG-P4-002. RW-REFADM holds `CRUD` (PS v6) and may load.
  No role holds Reference data `A` in the PS v6 seed.
- Approval: Story v7 §10 has RW-DATASTEW confirm (U); E1-043 v7 and API v4 require Reference data A,
  which no role holds. Unresolved in the documents (`GAP-E1001-08`); the end-to-end approval test uses
  whatever approver RWB-E1-043 implements and is recorded as blocked if none.
- The migration runs as `rwb_migrator` (ADR-010); the application identity `recovery_svc` has DML only.

### SPEC-RWB-E1-001-017 Feature flag and guardrails

- `rwb.p1.data-catalog` (default `false`) in `RecoveryFlags`. Off: the handler is not registered, so a
  load with `table = data_product` gets RWB-E1-043's unknown-table refusal (previous path). The
  migration and the view are not behind the flag (Story v7 §13).
- No product value, owner, role or refresh cycle as a code literal except the 14 codes DP01–DP14 that
  BR2 fixes, and the message texts under `ASM-E1001-06`.
- No class names an ACE `public` table (BND-6). No personal data in tests, fixtures or logs; owner user
  IDs in tests are random UUIDs.

## Field-level behaviour matrix

| Object | Field | Source | Create / update | Rule |
|---|---|---|---|---|
| `data_product` | `product_code` | Seed, load file | Seed insert; never changed by load | DP01–DP14 (K1); unique |
| `data_product` | `product_name`, `definition` | Seed, load file | Seed; updated by `apply` | NOT NULL; checked by E1-043 schema check |
| `data_product` | `system_of_record` | Seed, load file | Seed; updated by `apply` | SOR-1 to SOR-4 (K2) |
| `data_product` | `owner_role` | Seed, load file | Seed `RW-DATASTEW`; updated by `apply` | Active role code (K4) |
| `data_product` | `owner_user_id` | Load file | NULL in seed; set by `apply` | Required in the file (K3); synthetic in DEV/SIT |
| `data_product` | `refresh_cycle` | Seed, load file | Seed; updated by `apply` | LOV-REFRESH (K5) |
| `data_product` | `expected_by` | Seed, load file | Seed; updated by `apply` | Free text up to 20 |
| `data_product` | `valid_from` | Load request | Seed 2026-11-30; set by `apply` | From the load's valid from |
| `data_product` | standard columns | System | `version` +1, `updated_at`, `updated_by` on `apply` | — |
| `sys_objects`, `sys_fields` | all | Migration | Seed only | Later changes are reference loads (D-RCV-29); not in this story |
| `v_data_dictionary` | all | View | Read only | SPEC-005 |

## Status-transition matrix

| Object | From | Event | To | Source |
|---|---|---|---|---|
| Recovery schema (Flyway) | baseline `0` or none | Migration applied | this migration `success = true` | Story v7 §9 |
| Recovery schema (Flyway) | none | Migration fails | unchanged; no success row | AC4 |
| Data product catalog | seed (version 1) | Load approved and applied | next version, 14 rows updated | Story v7 §9; E1-043 |
| Data product catalog | version in force | Same file loaded | unchanged; MSG-P1-011 | AC10 |
| Data product catalog | version in force | Load refused | unchanged | AC7–AC9, AC11 |

No case status changes (Story v7 §9).

## Exceptional-case behaviour

| ID | Case | Behaviour | Evidence |
|---|---|---|---|
| X1 | Statement fails in the migration | Rollback; failing statement in the log; no success row | SPEC-007 |
| X2 | Column without dictionary row, field without column, or type mismatch | Conformance test fails with the C1–C3 texts | SPEC-009 |
| X3 | Migration already applied | Nothing applied | SPEC-008 |
| X4 | No / two / bare system of record, or no owner | 422, MSG-P1-003 per product, nothing written | SPEC-013, -015 |
| X5 | Not exactly DP01–DP14 | 422, MSG-P1-004 naming the missing codes | SPEC-013, -015 |
| X6 | Owner role or refresh cycle outside its list | 422, MSG-P1-007 per row and field | SPEC-013, -015 |
| X7 | Same file again | Nothing written, MSG-P1-011 | SPEC-014 |
| X8 | Caller without Reference data C | 403, MSG-P4-002 | SPEC-016 |
| X9 | Recovery Flyway started on a schema built by the reference load | Not allowed: `rwb.flyway.enabled=false` on that path | SPEC-010 |
| X10 | Flag `rwb.p1.data-catalog` off | `data_product` load refused as an unknown table by RWB-E1-043 | SPEC-017 |

## API change assessment

No endpoint, schema or response is added or changed. The story uses `POST /admin/reference-loads`
(`postAdminReferenceLoads`, x-module P4, Reference data C, x-first-release E1) and its approve
operation, both built by RWB-E1-043. The `table` parameter is a free string, so `data_product` needs
no API change. `ReferenceLoad` and `Problem` are used as defined. API v4 names "ReferenceTableLoader"
for P5 tables while Story v7 §12 names `ReferenceTableHandler`; the seam's name is RWB-E1-043's
(`GAP-E1001-07`). Contracts: `contracts/backend-apis.json`.

## Unit Test Applicability

| Surface | Changes Required | Unit Tests | Coverage Gate | Requirement/SPEC References | Evidence and Rationale | Test Acceptance Criteria |
|---|---|---|---|---|---|---|
| Frontend | NO | NOT_APPLICABLE | NOT_APPLICABLE | Story v7 §15 | No screen, route, component or i18n key. | None. |
| Backend | YES — migration, `dataengine` catalog classes, lint refinement, conformance test | REQUIRED | 80% lines, branches, statements and functions on `th.co.scb.ace.demo.recovery.dataengine` and the changed lint code | SPEC-001 to SPEC-017; AC1–AC11; BR1–BR9 | Handler rules K1–K5 and SOR-1 to SOR-4, the apply transaction, the message formatting and the lint rule are hand-written logic. JUnit 5 with AssertJ; JaCoCo. | Each of K1–K5 and SOR-1 to SOR-4 has a pass and a fail case (AC7, AC8, AC9, AC11 data from Story v7 §16); all findings reported in row order; `validate` writes nothing; `apply` rolls back all rows on failure; MSG-P1-011 on equal hash; lint passes a quoted `public.` value and fails a `public.` reference. |

Separately required integration tests (tag `recovery-it`) stay in scope: `RecoverySchemaMigrationIT`
and `DataDictionaryConformanceTest` (AC1, AC2, AC4, AC5, AC6) and the end-to-end load tests (AC3,
AC7–AC11, TC-E1-001-11) once RWB-E1-043 is built. They are not replaced by unit tests.

## Test scenarios

| Test case | AC / BR | Level | Expected (this spec) | Runs when |
|---|---|---|---|---|
| TC-E1-001-01 | AC1, BR1, BR6, BR8 | IT | 93 tables (89 + 4); none of the 20 removed tables; no `payment_match_rule`; 0 constraints into `public`; 16 key columns `varchar(255)` in no FK; conformance 1,047/1,047 and 1,075/1,075; no `v_ace_*` view | This story |
| TC-E1-001-02 | AC2, BR1 | IT | DF-ACE-018 row as AC2 with `product_system_of_record` "ACE (ingested from ALS)", `refresh_cycle` DAILY, `owner_role` RW-DATASTEW, synthetic owner UUID; DF-EXT-028 row as AC2 | This story (owner set by test fixture); end-to-end after E1-043 |
| TC-E1-001-03 | AC3, BR2, BR3, BR5 | Unit + IT | 14 rows; DP01, DP03, DP06 values as AC3 | Unit now; end-to-end after E1-043 |
| TC-E1-001-04 | AC4 | IT | Copy of the migration with a failing `valuation_ext` statement on a throwaway schema: none of its tables, no success row | This story |
| TC-E1-001-05 | AC5, BR1 | IT | Both AC5 texts | This story |
| TC-E1-001-06 | AC6 | IT | Second migrate applies 0; 123 / 1,379 unchanged | This story |
| TC-E1-001-07 | AC7 | Unit + IT | 422, MSG-P1-003 for DP06 and DP11 | Unit now; end-to-end after E1-043 |
| TC-E1-001-08 | AC8 | Unit + IT | 422, MSG-P1-004 "Missing: DP09." | as above |
| TC-E1-001-09 | AC9 | Unit + IT | 422, two MSG-P1-007 texts (DP_OWNER, HOURLY) | as above |
| TC-E1-001-10 | AC10 | IT | Second load writes nothing; MSG-P1-011 | after E1-043 |
| TC-E1-001-11 | X8 | Access | RW-DATASTEW 403 MSG-P4-002 | after E1-043 |
| TC-E1-001-12 | AC11 | Unit + IT | 422, MSG-P1-003 text for DP06 "CCMS" | Unit now; end-to-end after E1-043 |
| Lint | SPEC-011 | Unit | Quoted `public.` passes; schema reference fails | This story |

All test data is synthetic (random UUIDs, no names or account numbers).

## Guardrails and out of scope

- Out of scope (Story v7 §19): the 30 `v_ace_*` views, their helper functions, grants and the view
  conformance test (RWB-E1-069, V0002/V0003); freshness (RWB-E1-015); access per data product, PDPA
  masking and the catalog entry screen (RWB-E1-016); retention (RWB-E1-017); Stage 2 products (Epic
  2); the dictionary endpoint and field versions (RWB-E1-064); rule package content (RWB-E1-072);
  `delegation_limit` content (RWB-E1-038).
- Not rebuilt (phase0 audit A-04): `RecoveryFlywayConfig`, the lint (refined only, SPEC-011), init
  scripts, `ApiError`/`ProblemFactory`.
- Never: a literal schema name, `SET search_path`, `GRANT`, a constraint into `public`, a read of an
  ACE table, a `DROP` in the migration, editing the migration after merge.

## Clarification Log

| CLAR_ID | Requirement/Spec References | Question or Gap | Implementation Impact | BA/User Response | Status | Resulting SPEC-* |
|---|---|---|---|---|---|---|
| CLAR-001 | Story v7 AC1, AC6, §11; PS v6; D-RCV-36 CR A.7 | Story counts 92/122/1,366/1,062 are the v5 counts; PS v6 gives 93/123/1,379/1,075. | Test expectations. | D-RCV-36 (tier 1) governs: PS v6 counts (`ASM-E1001-01`; README decision 7 already notes 123/1,379). | RESOLVED | SPEC-003, -006, -008, -009 |
| CLAR-002 | DL v10 D-RCV-28; decision register D-RCV-34; merge-order map | V0001 or V0003? | File name. | DL v10 (tier 3) over squad decision and map: next free at merge, V0001 if first (`ASM-E1001-02`). | RESOLVED | SPEC-001 |
| CLAR-003 | README; `RecoveryFlywayConfig`; `RecoveryDatabaseIT` | How the migration coexists with `RWB_LOAD_REFERENCE_SCHEMA=true`. | Local start and IT would fail. | Flyway-only IT for this story; Flyway off on the reference-load path; end state Flyway from scratch after E1-069 (`ASM-E1001-07`). | RESOLVED | SPEC-010 |
| CLAR-004 | DL v10 D-RCV-29; Story v7 §13 | Which seeds belong in V0001? | Seed sections. | D-RCV-29 list: dictionary, `data_product`, `lov_value`, `role`, `permission`; no `delegation_limit`, no `rule_package` (`ASM-E1001-03`). | RESOLVED | SPEC-006 |
| CLAR-005 | Story v7 §13; PS v6 seed; Rulings v2 R4 | Three different `data_product` seed versions. | Seed values. | Story v7 §13 (`ASM-E1001-04`). | RESOLVED | SPEC-006 |
| CLAR-006 | Story v7 §12; Rulings v2 R2; PS v6 line 2156 | PS v6 view lacks the system-of-record columns and reads `owner_role` from `sys_fields`. | AC2 would fail. | Story v7 §12 and R2 govern. | RESOLVED | SPEC-005 |
| CLAR-007 | Story v7 §3, §12; E1-043 v7; API v4 | `ReferenceTableHandler` is not defined by E1-043 v7. | Handler wiring. | Build against the Story v7 §12 signature; INC-008 publishes the seam (`ASM-E1001-05`). | RESOLVED (dependency) | SPEC-013, -014 |
| CLAR-008 | `RecoveryMigrationLintTest`; PS v6 `sys_fields` | 297 seed values contain `public.` and fail the lint. | Migration cannot merge. | Lint ignores string-literal content; tests prove both directions. | RESOLVED | SPEC-011 |
| CLAR-009 | Story v7 §10; E1-043 v7; API v4 line 3232 | Who approves a `data_product` load? | End-to-end AC3 approval step. | Not settled by the documents; open item proposed. | OPEN (non-blocking for this spec) | SPEC-016 |
| CLAR-010 | Story v7 §14; MSG v4 line 77; PS v6 (no message table) | MSG-P1-003 wording and Thai; no message table. | Message source. | Story v7 wording, held in code (`ASM-E1001-06`); Thai under OPEN-005. | RESOLVED | SPEC-015 |

`CLARIFICATION_STATUS: RESOLVED_WITH_OPEN_ITEM` — nine items are settled by precedence or a labelled
assumption; CLAR-009 needs an owner ruling and does not block the spec. No question was asked.

## Status reporting

```text
MCP_STATUS_SUMMARY: NOT_APPLICABLE — no Jira, Confluence, GitLab or Figma MCP is connected (RUN-BRIEF rule 5); sources read from the document set.
MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]
CHANGE_CLASSIFICATION_SUMMARY: One baseline recovery migration from Physical Schema v6, the dictionary view, the data product catalog handler and the conformance test; no screen; no API change.
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: NO] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: YES] [API_IMPACT: NO_API_CHANGE] [REASON: uses the existing reference-load endpoint with table data_product]
REQUIREMENT_COVERAGE_SUMMARY: 9 business rules, 11 ACs, 8 exception paths, authority, contract, solution plan, guardrails and out of scope mapped in 28 rows.
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 28] [COVERED_RULES: 28] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0 unresolved; 14 document conflicts settled by precedence in document-gaps.md]
DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0] [UNBLOCK_ACTION: n/a]
CLARIFICATION_STATUS: RESOLVED_WITH_OPEN_ITEM [OPEN_ITEMS: 1 (CLAR-009, non-blocking)]
NEXT_STEP: Spec gate (Compliance Reviewer), then human review and the Implementation Planner.
```
