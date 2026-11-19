---
title: "Data model: RWB-E1-001 Recovery tables for the 14 data products"
run_id: "INC-009-epic-1-RWB-E1-001"
story: "RWB-E1-001"
epic: "EPIC-001"
stage: "plan"
revision: "v1 (18 Nov 2026): first plan-stage data model. Derived from Physical Schema v6 and the sibling plans; no number is fixed for the migration (D-RUN-07)."
prepared: "2026-11-18"
---

# Data model: RWB-E1-001

One production migration creates the 89 tables this story owns, the data dictionary seed, the 14
`data_product` rows and the `v_data_dictionary` view. The tables it does **not** create are the four
that an earlier-merged story creates (D-RUN-12): `parameter_catalog` and `parameter_value` (RWB-E1-042,
Build Sequence v6 order 3) and `reference_version` and `reference_row` (RWB-E1-043, order 8). Their
dictionary rows are still seeded here (4 `sys_objects`, 53 `sys_fields`), because the dictionary is
this story's deliverable.

Sources: Physical Schema v6 (16 Nov 2026), `requirement/legacy/06-data/recovery-workbench-physical-schema-v6.sql`
(byte-identical repo copy `infra/postgres/schema/03-recovery-physical-schema-v6.sql`), lines 16–6130;
Story v7 `rwb-e1-001-recovery-tables-for-the-14-data-products-v1.md` §§ 11–13; RWB-E1-042 spec
revision 13 §7.1/§7.2/§12.3 and plan v2 `data-model.md` §§ 4.1–4.2; RWB-E1-043 spec revision 10
SPEC-001 and plan v1 `data-model.md` §§ 2–4; the evidence files under `../specify/evidence/`. Short
names are as in `../specify/spec.md` § "Sources and how they are cited".

## 1. Migration file

| Item | Value |
|---|---|
| Path | `backend/src/main/resources/db/modulemigration/recovery/V<seq>__rwb_e1_001_recovery_schema.sql` |
| Name | `V<seq>__rwb_e1_001_recovery_schema.sql`; `<seq>` is the next four-digit number in merge order, assigned by the orchestrator at merge (D-RUN-07; DL v10 D-RCV-28). **No number is fixed here** |
| Line 1 | exactly `-- Story: RWB-E1-001` |
| Line 2 | a header comment citing Physical Schema v6, D-RCV-28 and `../specify/spec.md` revision 4 |
| Sequence | after the RWB-E1-042 and RWB-E1-043 files (Build Sequence v6 orders 3 and 8 precede 9); the E1-044 lint requires a contiguous sequence from `V0001` |
| Transaction | one transaction; Flyway default; no `CREATE INDEX CONCURRENTLY`, no `VACUUM`, no `SET search_path` |
| Re-run | Flyway applies nothing on the second run; a changed checksum fails validation |
| Editing | never edited after merge; a correction takes the next `<seq>`, keeps the story key and adds line 2 `-- Fix: <reason>` |

The file has these statement groups, **in this order** (the order is PS v6's, so a reader can diff the
two files):

1. 89 `CREATE TABLE ${recoverySchema}.<name>` blocks, PS v6 file order, minus the 4 of § 2.3.
2. 91 `ALTER TABLE … ADD CONSTRAINT fk_… FOREIGN KEY` statements, PS v6 file order.
3. 111 `CREATE [UNIQUE] INDEX` statements, PS v6 file order.
4. `CREATE VIEW ${recoverySchema}.v_data_dictionary` (§ 8) and its `COMMENT ON VIEW`.
5. `CREATE OR REPLACE FUNCTION ${recoverySchema}.refuse_change()`; `CREATE TRIGGER
   tr_declog_append_only` on `decision_log_entry`; `CREATE TRIGGER tr_interaction_append_only` on
   `interaction`, both `BEFORE UPDATE OR DELETE … EXECUTE FUNCTION ${recoverySchema}.refuse_change()`.
6. 85 `COMMENT ON TABLE` and 973 `COMMENT ON COLUMN` statements (PS v6 lines 2398–3420 minus the four
   skipped tables).
7. The 14-row `data_product` seed (§ 10.1), at PS v6's position **before** `sys_objects` (the FK needs
   the parent rows).
8. The 123-row `sys_objects` seed.
9. The 1,379-row `sys_fields` seed with T10 applied, then the 3 provisional rows DF-REF-300..302
   (§ 6.3).
10. The 598-row `lov_value`, 54-row `role` and 421-row `permission` seeds.
11. The two `parameter_catalog` rows from § 11 (added in TASK-11, after TASK-10's red test).

No `rule_package` seed and no `delegation_limit` seed (§ 10.3). No `ace_to_date`, `ace_to_boolean`,
`ace_mask_value` or `v_ace_*` view (PS v6 from line 6131, RWB-E1-069). No `GRANT`/`REVOKE`/`CREATE
SCHEMA`/`CREATE EXTENSION`. No `IF NOT EXISTS`, `DROP …`, `CONCURRENTLY` or `ON CONFLICT` except the
two `parameter_catalog` rows (SPEC-019 item 5 requires `ON CONFLICT (param_key) DO NOTHING` there).
The file does not guard against an object that already exists: the § 2.3 list is the complete set of
pre-existing objects, so an unexpected duplicate fails the migration (AC4) rather than being skipped.

`${recoverySchema}` is the only qualifier. A `'public.…'` value inside a string literal is seed data
(297 rows carry `public.account.…` in `source_field`) and is allowed by E1-044's identifier-only,
quote-aware lint (D-RUN-13; E1-044 SPEC-007, T-044-21). No comment or string names a recovery object
with a literal schema.

## 2. Table set

### 2.1 The 89 tables this migration creates (D-RUN-12)

Column definitions, types, widths, nullability, defaults and order are **Physical Schema v6 verbatim**
for every table below; the migration is a mechanical transcription of lines 16–6130 with T1–T11 of
`../specify/spec.md` SPEC-002. The plan does not transcribe 1,075 columns into a second source: § 3
gives the exact DDL for the tables this story's logic reads or writes, and `MigrationDerivationTest`
(TASK-01) proves every table and column against the PS v6 file.

| Group | Tables | Count |
|---|---|---|
| Case and ownership | `recovery_case`, `case_account`, `case_party`, `deviation`, `queue`, `assignment`, `task`, `timer`, `treatment`, `guarantee_claim`, `legal_action`, `notice`, `hearing`, `partner`, `partner_instruction`, `listing`, `asset_sale`, `debt_sale_lot`, `debt_sale_account`, `interaction`, `document`, `document_field`, `document_custody`, `decision_log_entry`, `proceeds`, `write_off`, `case_list_row`, `case_entry_exclusion`, `queue_member`, `queue_measure` | 30 |
| Rules and reference data | `rule_package`, `rule_package_version`, `rule_row`, `delegation_limit`, `lov_value`, `role`, `permission`, `template`, `rule_test_case` | 9 |
| Data product, catalog and dictionary | `data_product`, `data_product_access`, `data_product_load`, `data_contract`, `sys_objects`, `sys_fields`, `sys_field_version` | 7 |
| Operations and integration | `reconciliation_result`, `lake_copy_watermark`, `retention_rule`, `interface_config`, `outbound_item`, `processed_event`, `idempotency_key`, `outbox_event`, `outbox_delivery`, `feature_flag`, `feature_flag_change`, `job_catalog`, `efs_ledger_outcome` | 13 |
| Data product projections | `dp_treatment`, `dp_guarantee_claim` | 2 |
| Masking and role conflicts | `masking_rule`, `role_conflict`, `partner_user` | 3 |
| Documents and approvals | `document_type`, `document_checklist_item`, `case_document_check`, `document_hub_parameter`, `document_intake`, `document_text`, `retention_action`, `merge_field`, `signature_request`, `approval` | 10 |
| Measures | `measure_definition`, `measure_snapshot`, `measure_publish` | 3 |
| Agent | `agent_policy`, `agent_prompt`, `agent_run`, `agent_sample`, `agent_evaluation_run`, `agent_evaluation`, `agent_feedback`, `agent_alert` | 8 |
| Extension tables (D-RCV-35 U3) | `party_ext`, `contact_point_ext`, `account_ext`, `valuation_ext` | 4 |
| **Total** | | **89** |

None of the 20 tables AC1 removes is created: `loan_account`, `account_payment`, `party`,
`contact_point`, `collateral`, `account_collateral`, `collections_history`, `party_product`,
`valuation`, `score`, `asset`, `load_run`, `dq_exception`, `dq_rule`, `source_field_map`,
`source_code_map`, `interface_run`, `interface_signoff`, `tracker_inventory`, `tracker_row`. No
`payment_match_rule` (D-RCV-36 T10).

### 2.2 Schema after the migration (93 tables)

The 89 above plus the four in § 2.3. `parameter_catalog` has 22 PS v6 columns, `parameter_value` 19
plus E1-042's three added columns (T11), `reference_version` 29, `reference_row` 11. Their constraints,
indexes, triggers and `COMMENT ON` statements belong to their own migrations and are not repeated.

### 2.3 D-RUN-12: objects **not** created here

| Object in PS v6 | Owner (Build Sequence v6 order) | What this migration does |
|---|---|---|
| `CREATE TABLE parameter_catalog` (line 1386) | RWB-E1-042 (order 3) | Nothing |
| `CREATE TABLE parameter_value` (line 1413) | RWB-E1-042 | Nothing |
| `CREATE TABLE reference_version` (line 1437) | RWB-E1-043 (order 8) | Nothing |
| `CREATE TABLE reference_row` (line 1471) | RWB-E1-043 | Nothing |
| `ALTER TABLE reference_row ADD CONSTRAINT fk_reference_row_version_id` (line 2242) | RWB-E1-043 | Nothing |
| `CREATE INDEX ix_reference_row_version_id` (line 2347) | RWB-E1-043 | Nothing |
| `COMMENT ON TABLE` × 4 (lines 2426–2429) and `COMMENT ON COLUMN` × 53 on those tables | RWB-E1-042 / RWB-E1-043 | Nothing (4 + 53 = the 57 PS v6 comment statements, finding 018) |
| The 4 `sys_objects` rows and **53** `sys_fields` rows for those tables | **This story** (the dictionary is its deliverable) | **Seeded** |
| `ALTER TABLE retention_rule / document_type / document_checklist_item / document_hub_parameter … REFERENCES reference_version` (lines 2228, 2244, 2245, 2248) | This story (the child tables are its own; the parent exists) | **Created** |

D-RUN-12 is an orchestrator (Claude Code, an AI agent) run decision, not a human ruling; its
ratification is not claimed (OPEN-050). It changes no dictionary row: the 4 objects and 53 fields stay
so the schema after this migration holds 123 `sys_objects` and 1,382 `sys_fields`.

## 3. `data_product` (exact Physical Schema v6 line 815, with T9)

```sql
CREATE TABLE ${recoverySchema}.data_product (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    product_code varchar(25) NOT NULL,
    product_name varchar(80) NOT NULL,
    definition varchar(400) NOT NULL,
    system_of_record varchar(200) NOT NULL,          -- T9 / ASM-E1001-13 (PS v6: varchar(120))
    owner_role varchar(20) NOT NULL,
    owner_user_id uuid,
    refresh_cycle varchar(10) NOT NULL,
    expected_by varchar(20),
    valid_from date NOT NULL,
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid,
    CONSTRAINT uk_data_product UNIQUE (product_code)
);
```

- 17 columns; the 10 business fields are DF-REF-070..079 (`../specify/spec.md` SPEC-006; GAP-E1001-09:
  PS v6 governs, so `id` is the primary key and `product_code` the unique business key).
- `system_of_record varchar(200)` is the **Blocker = Yes** assumption `ASM-E1001-13`: Story v7 §13's
  DP07 value is 139 characters and PS v6/LDM v8 say 120 (`GAP-E1001-17`). A human ruling is required
  before the merge of this migration; this data model does not present the widening as agreed.
- `fk_sys_objects_data_product` is added on `sys_objects.data_product` →
  `data_product(product_code) ON DELETE RESTRICT` (PS v6 line 2237); `sys_objects.data_product` stays
  nullable.
- The `data_product` rows are inserted before `sys_objects` (PS v6 order).
- `apply` updates these rows in place (never inserts or deletes) and sets `valid_from` from the load.

## 4. `sys_objects` and `sys_fields`

### 4.1 `sys_objects` (PS v6 line 900)

| # | Column | Type | Null | Default | Note |
|---|---|---|---|---|---|
| 1 | `id` | `uuid` | NOT NULL | `gen_random_uuid()` | primary key |
| 2 | `object_name` | `varchar(60)` | NOT NULL | — | `uk_sys_objects` unique |
| 3 | `business_name` | `varchar(120)` | NOT NULL | — | — |
| 4 | `subject_area` | `varchar(10)` | NOT NULL | — | CAS, TRT, … |
| 5 | `data_product` | `varchar(10)` | NULL | — | `fk_sys_objects_data_product` |
| 6 | `system_of_record` | `varchar(120)` | NOT NULL | — | PS v6 seed values ("Workbench", "ACE …") |
| 7 | `description` | `varchar(400)` | NOT NULL | — | — |
| 8 | `is_active` | `boolean` | NOT NULL | `true` | standard |
| 9 | `state` | `varchar(40)` | NULL | — | standard |
| 10 | `version` | `integer` | NOT NULL | `1` | standard |
| 11 | `created_at` | `timestamptz` | NOT NULL | `now()` | standard |
| 12 | `created_by` | `uuid` | NULL | — | standard |
| 13 | `updated_at` | `timestamptz` | NOT NULL | `now()` | standard |
| 14 | `updated_by` | `uuid` | NULL | — | standard |

### 4.2 `sys_fields` (PS v6 line 919) and the seed column list

24 columns: `id`, `field_id`, `object_name`, `field_name`, `data_type`, `physical_type`,
`is_mandatory`, `lov_code`, `references_object`, `source_system`, `source_field`, `is_personal`,
`description`, `owner_role`, `refresh_cycle`, `late_behavior`, `interface_id`, `is_active`, `state`,
`version`, `created_at`, `created_by`, `updated_at`, `updated_by`; `uk_sys_fields (field_id)`.

The seed uses PS v6's 12-column insert list, unchanged, exactly:

```sql
INSERT INTO ${recoverySchema}.sys_fields
  (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code,
   references_object, source_system, source_field, is_personal, description)
VALUES ('DF-CAS-001', 'recovery_case', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL,
        false, 'Record identifier of the case');
```

One `INSERT` statement per row (1,382 statements: 1,379 PS v6 rows + 3 provisional). T10 requires the
`is_personal` value to be the literal `true` or `false` in the **eleventh** value position of every
statement, with no `UPDATE … SET is_personal` anywhere in the file. That is what the RWB-TE-011 PDPA
lint parses (TE-011 spec SPEC-TE011-001 (dictionary reader); `GAP-E1001-21`, `ASM-E1001-14`).

### 4.3 The three provisional rows (T11, `ASM-E1001-17`)

| `field_id` | `object_name` | `field_name` | `data_type` | `physical_type` | `is_personal` | Description prefix |
|---|---|---|---|---|---|---|
| `DF-REF-300` | `parameter_value` | `load_id` | `TEXT` | `uuid` | false | `Provisional field ID (RWB-E1-001 ASM-E1001-17).` |
| `DF-REF-301` | `parameter_value` | `content_hash` | `TEXT` | `char(64)` | false | same prefix |
| `DF-REF-302` | `parameter_value` | `rollback_reason` | `TEXT` | `varchar(400)` | false | same prefix |

The columns are the three E1-042 adds to `parameter_value` (E1-042 spec revision 13 §12.3). `char(64)`
is the canonical C3 form (catalog `bpchar(64)`); the same form is used by the nine PS v6 `char(n)`
rows. The rows make C1 1,050/1,050 and C2 1,078/1,078. A ruling that assigns other IDs changes the
seed before merge; if E1-042 drops a column, its row is dropped (`OPEN-NEW-5`).

## 5. Reference tables `lov_value`, `role`, `permission`

| Table | PS v6 line | Key | Columns | Seeded rows |
|---|---|---|---|---|
| `lov_value` | 737 | `uk_lov_value (lov_code, value_code)` | `id`, `lov_code` `varchar(30)`, `value_code` `varchar(30)`, `label_en` `varchar(120)`, `label_th` `varchar(120)`, `sort_order` `integer` default 0, `valid_from` `date`, plus the 7 standard columns | 598 |
| `role` | 756 | `uk_role (role_code)` | `id`, `role_code` `varchar(20)`, `role_name` `varchar(80)`, `role_class` `varchar(15)`, `default_scope` `varchar(8)`, plus the 7 standard columns | 54 |
| `permission` | 773 | none (row identity `id`); `fk_permission_role_id` → `role(id)` | `id`, `role_id` `uuid`, `capability_area` `varchar(30)`, `letters` `varchar(5)` default `'-'`, `matrix_version` `varchar(20)`, plus the 7 standard columns | 421 |

`lov_value` rows are the PS v6 seed, unchanged (DL v10 D-RCV-29; E1-043 revision 10 § "Seed
ownership"). The LOV-REFRESH order used by K5 is PS v6 lines 5035–5038: `DAILY` 1, `WEEKLY` 2,
`MONTHLY` 3, `ON_CHANGE` 4. There is **no** `LOV-ROLE` row; K4 therefore reads active
`role.role_code` values (`ASM-E1001-10`), and the MSG-P1-007 text keeps the name LOV-ROLE because
Story v7 AC9 says so.

`role` is read only for K4 (`select r.roleCode from CatalogRole r where r.active = true`), through
the package-private `CatalogRole` entity and `CatalogRoleRepository`. The table is created and seeded by
this migration; no other module publishes a role-list reader (`ASM-E1001-10`; plan assumption
`PA-E1001-02`).

## 6. Append-only tables and triggers

`decision_log_entry` (PS v6 line 561, 29 columns) and `interaction` (line 452, 36 columns) are created
with their PS v6 columns, keys and indexes. `refuse_change()` and the two triggers follow PS v6 lines
2390–2396:

```sql
CREATE OR REPLACE FUNCTION ${recoverySchema}.refuse_change() RETURNS trigger LANGUAGE plpgsql AS $$ … $$;
CREATE TRIGGER tr_declog_append_only BEFORE UPDATE OR DELETE ON ${recoverySchema}.decision_log_entry
  FOR EACH ROW EXECUTE FUNCTION ${recoverySchema}.refuse_change();
CREATE TRIGGER tr_interaction_append_only BEFORE UPDATE OR DELETE ON ${recoverySchema}.interaction
  FOR EACH ROW EXECUTE FUNCTION ${recoverySchema}.refuse_change();
```

`RecoveryDatabaseIT#decisionLogIsAppendOnly` keeps its assertion; after this story the trigger it
exercises comes from this migration (S1=`false`, S2=`true` stage).

## 7. Extension tables (D-RCV-35 U3)

| Table | Key | Columns | ACE link |
|---|---|---|---|
| `party_ext` | `person_key varchar(255)` primary key | `vulnerable`, `deceased_override`, `bankruptcy`, `fraud_flag` `boolean NOT NULL DEFAULT false`, plus the 7 standard columns | `person_key`, no FK |
| `contact_point_ext` | `contact_key varchar(255)` primary key | `contact_type varchar(10) NOT NULL`, `consent_given` `boolean`, `consent_at`, `verified_at` `timestamptz`, `failed_count` `integer`, `source varchar(20)`, `ck_contact_point_ext_type CHECK (contact_type IN ('PHONE','EMAIL','ADDRESS'))`, plus the 7 standard columns | `contact_key`, no FK |
| `account_ext` | `account_key varchar(255)` primary key | `dispute_open boolean NOT NULL DEFAULT false`, plus the 7 standard columns | `account_key`, no FK |
| `valuation_ext` | `valuation_key varchar(255)` primary key | `accepted` `boolean`, `accepted_at` `timestamptz`, `accepted_by` `uuid`, `valuer_partner_id` `uuid`, `stale_flag` `boolean`, `age_days` `integer`, plus the 7 standard columns | `valuation_key`, no FK |

The seven standard columns are `is_active`, `state`, `version`, `created_at`, `created_by`,
`updated_at`, `updated_by`. These 28 columns are the difference between 1,047 non-standard columns and
1,075 table fields.

## 8. `v_data_dictionary` (SPEC-005, T3)

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

20 columns. Story v7 §12's column list is kept; the PS v6 view's `f.owner_role` is replaced by
`p.owner_role`, and the two system-of-record columns are added (Rulings v2 R2 §3.3, PBR v2 §3 Q2;
`GAP-E1001-03`). It reads no ACE table, creates no view over `public`, and returns active rows only.
`owner_role` and `owner_user_id` are NULL for an object with no data product (the 24 operational
objects), which is expected.

## 9. Constraints, indexes, triggers and comments carried

| Group | PS v6 | This migration | Why |
|---|---|---|---|
| Foreign keys | 92 | **91** | minus `fk_reference_row_version_id` (T8) |
| Indexes | 112 | **111** | minus `ix_reference_row_version_id` (T8) |
| CHECK constraints | 3 | **3** | `ck_rule_package_hit_policy`, `ck_rule_package_version_status`, `ck_contact_point_ext_type` — inline in their tables |
| Append-only triggers | 2 | **2** | `tr_declog_append_only`, `tr_interaction_append_only` + `refuse_change()` |
| `COMMENT ON TABLE` | 89 | **85** | minus the 4 T8 tables |
| `COMMENT ON COLUMN` | 1,026 | **973** | minus the 53 on T8 tables |

Every FK is between recovery tables. **Zero** constraints reference schema `public` (PS v6 has none),
and the 18 ACE link columns are `varchar(255)` and in no FK (BR8): `account_key` on `account_ext`,
`case_account`, `case_entry_exclusion`, `case_list_row`, `debt_sale_account`; `person_key` on
`case_party`, `document`, `interaction`, `notice`, `party_ext`, `signature_request`;
`recovery_case.primary_person_key`; `asset_key` on `asset_sale`, `listing`; `contact_key` on
`contact_point_ext`, `interaction`; `proceeds.payment_code`; `valuation_ext.valuation_key` (primary key,
no FK). `document_intake.file_name` is `varchar(255)` but is not a link and is not counted.

## 10. Seeds

### 10.1 The 14 data products (`ASM-E1001-04`)

`owner_role = 'RW-DATASTEW'`, `owner_user_id = NULL`, `valid_from = DATE '2026-11-30'` for all rows.
`product_code, product_name, definition, system_of_record, refresh_cycle, expected_by` exactly:

| Code | Name | Definition | System of record | Refresh cycle | Expected by |
|---|---|---|---|---|---|
| DP01 | Account and arrears | Loan accounts with balances, interest, fees, days past due, bucket, classification, restructure flag and payments | ACE (ingested from ALS) | DAILY | 08:00 |
| DP02 | Customer and party | Customers, guarantors, co-borrowers and heirs, identity masked to the last four, contact points, consent and flags for vulnerability, death and bankruptcy | ACE (ingested from SCBPDM and the core bank) | DAILY | 08:00 |
| DP03 | Case and ownership | The case, its accounts and parties, status, stage, route, owner, queue, tasks, timers and deviations | Recovery Workbench | ON_CHANGE | As it changes |
| DP04 | Treatment and offers | Restructures, settlements, deeds in lieu, buy-backs and guarantee claims, with terms, approval level and outcome | ACE (ingested from the core bank) for the plan, with the treatment held in the Recovery Workbench | ON_CHANGE | As it changes |
| DP05 | Contact and promises | Every contact, letter, promise and hand-over on the case, in order, including the collections history from EFS | ACE (ingested from EFS) | DAILY | 08:00 |
| DP06 | Collateral and assets | Collateral, appraisals, assets held after repossession or transfer, listings and sale results | ACE (ingested from CCMS, SVAF, AMIS and RPS) | WEEKLY | MON 08:00 |
| DP07 | Legal events and cases | Notices and proof of delivery, lawsuits, court case numbers, hearings, judgments and enforcement | ACE (ingested from LIT and WIN) for the court record and the proof of delivery, with notices and enforcement held in the Recovery Workbench | DAILY | 08:00 |
| DP08 | Partner performance | Partners on the panel, work placed with each, results, fees and scorecards | Recovery Workbench | ON_CHANGE | As it changes |
| DP09 | Debt sale | Debt sale lots, the accounts in each lot, buyers, prices, approval and put-backs | Recovery Workbench | ON_CHANGE | As it changes |
| DP10 | Documents and extracted fields | Documents against the case, the fields read from them, retention class and custody of originals | Recovery Workbench document hub | ON_CHANGE | As it changes |
| DP11 | Scores and route economics | Risk scores, expected return by route, estimated sale price and sale success rate, restructure scheme suggestions | ACE (ingested from COLLINS) | DAILY | 08:00 |
| DP12 | Decision log | One entry per decision with the rule, model and agent versions, inputs, recommendation, approval, actions and outcome | Recovery Workbench | ON_CHANGE | As it changes |
| DP13 | Money and closure | Payments and proceeds matched to the case, write-off postings and recovery after charge-off | ACE (ingested from ALS and GL) | DAILY | 08:00 |
| DP14 | Reference data | Rules, approval limits, lists of values, roles, permissions and letter templates, each versioned | Recovery Workbench, with the ACE lists read through the views | ON_CHANGE | As it changes |

Width check (measured, `../specify/evidence/pdpa_v4_vs_ps_v6-output.txt`): name ≤ 80, definition ≤ 400,
system of record ≤ 200 (DP07 = **139**; DP04 = 97), refresh cycle ≤ 10, expected by ≤ 20. Every value
fits under `ASM-E1001-13`; DP07 does not fit `varchar(120)` (`GAP-E1001-17`, Blocker = Yes).

The PS v6 seed texts (line 3517) are **not** used: they write "Workbench" and "ACE (from ALS via
COLLINS)", which fail BR3/AC7/AC11 (`ASM-E1001-04`, `GAP-E1001-03`). The `sys_objects` seed keeps its
PS v6 values, so `entity_system_of_record` and `product_system_of_record` can differ in the view; AC2
asserts the product column.

### 10.2 `sys_objects` and `sys_fields`

| Table | Rows | Content |
|---|---|---|
| `sys_objects` | 123 | 93 table objects (incl. the 4 T8 tables) + 30 view objects; 99 carry a product, 24 NULL |
| `sys_fields` | 1,379 + 3 = **1,382** | 1,075 table fields (incl. 53 on the T8 tables and the 28 standard extension columns) + 304 `DF-ACE-*` view fields + DF-REF-300..302 |

### 10.3 `is_personal` (Blocker = Yes assumption `ASM-E1001-14`)

`true` for exactly the **526** field IDs listed in `../specify/evidence/is_personal_union_v4.tsv`
(copied to `backend/src/test/resources/dictionary/is-personal-union-v4.tsv`): 14 true in both sources,
4 true in PS v6 only, 508 "Personal data = Yes" in PDPA Inventory v4 only. It includes all 17 PDPA v4
Restricted fields (12 Direct identifier, 5 Sensitive), among them DF-ACE-003, -041, -053, -060, -061,
-116 and DF-EXT-002, -003, -004. The other 856 rows are `false`, including the 26 PS-v6-only fields
DF-REF-274..299 (DF-REF-288 `rule_package_version.author`, DF-REF-289 `.approver` are named in the
ruling ask). No arithmetic is left to the builder: the fixture is the list, and
`DictionarySeedShapeTest` compares the migration's literal `true` set with it.

This is a **Blocker = Yes** gap (`GAP-E1001-18`); a human ruling by the data architect with the DPO is
required before the merge of this migration. The union is the protective reading and may only narrow
by that ruling. No `UPDATE` of `sys_fields` exists in the migration, so the marks cannot be added or
removed by a later load and the TE-011 lint reads every one (SPEC-006 T10; E1-043 SPEC-031).

### 10.4 Seeds deliberately not carried

| Table | Rows | Reason |
|---|---|---|
| `rule_package`, `rule_package_version` | 0 | Story v7 §12/§13 seed list has none; RWB-E1-072 seeds Epic 1 packages in its own migration (`ASM-E1001-03`, `GAP-E1001-05`, `-19`) |
| `delegation_limit` | 0 | DL v10 D-RCV-29; Rulings v2 R3; PBR v2 §4 Q3; content is RWB-E1-038's |
| Every other table | 0 | Story v7 §11 |

## 11. `parameter_catalog` rows added here (SPEC-019 item 5)

`parameter_catalog` exists from RWB-E1-042 (22 PS v6 columns; `uk_parameter_catalog (param_key)`).
This story adds **two** rows in `backend/src/main/resources/config/parameter-catalog.csv` and the same
two rows in the migration with `INSERT … ON CONFLICT (param_key) DO NOTHING`. No `parameter_value` row
is added: the value is the catalog default, which `ParameterService` returns when no value row is in
force (E1-042 §7.2).

One shape for both rows: `kind=BUSINESS`, `value_type=CODE_LIST`, `unit` NULL, `min_value` NULL,
`max_value` NULL, `scope=GLOBAL`, `required=false`, `owner_role=RW-RISK`,
`environments=DEV,SIT,UAT,PROD`, `used_by=recovery.casewf.refdata (RWB-E1-043)`, `secret=false`,
`value_source=TABLE`, `env_property` NULL. Their own `default_value` and `description`:

| `param_key` | `default_value` | `description` |
|---|---|---|
| `rwb.refload.loader.data_product` | `RW-REFADM` | Roles allowed to load the data product catalog |
| `rwb.refload.approver.data_product` | `RW-DATASTEW` | Roles allowed to approve the data product catalog |

The reader is E1-043's P3 `ReferenceLoadAuthority`, which reads both keys through `ParameterService`
(E1-043 revision 10 SPEC-027). P1 `dataengine` reads neither key at runtime, so `used_by` names P3
only; there is no P1 reader and no seam to record (D-RUN-08; reviewer finding 025). `value_source` and
`env_property` are CSV fields, not DB columns, so the migration inserts only
`param_key, kind, value_type, default_value, scope, required, owner_role, environments, used_by,
secret, description`.

No `refdata.columns.data_product` row exists (E1-043's L12 is skipped by design: SPEC-019 item 4), and
no `LOV-REF-TABLE` row is added for `data_product` (D-RUN-11; `GAP-E1001-06` closed).

## 12. The 14 data products as dictionary objects

| Product | Objects that carry it (`sys_objects.data_product`) |
|---|---|
| DP01 | `v_ace_account`, `account_ext`, `v_ace_payment`, `case_account`, `proceeds`, `write_off`, … |
| DP02 | `v_ace_customer`, `party_ext`, `contact_point_ext`, `case_party`, `v_ace_phone`, `v_ace_email`, … |
| DP03 | `recovery_case`, `case_list_row`, `case_entry_exclusion`, `queue`, `queue_member`, `task`, `timer`, `assignment`, `deviation` |
| DP04 | `treatment`, `v_ace_restructure_plan`, `dp_treatment` |
| DP05 | `interaction`, `notice`, `v_ace_collections_activity`, … |
| DP06 | `v_ace_collateral`, `v_ace_asset`, `listing`, `asset_sale`, `valuation_ext`, … |
| DP07 | `legal_action`, `hearing`, `v_ace_legal_case` |
| DP08 | `partner`, `partner_instruction`, `partner_user` |
| DP09 | `debt_sale_lot`, `debt_sale_account` |
| DP10 | `document`, `document_field`, `document_custody`, `document_intake`, `document_text` |
| DP11 | `v_ace_score`, `v_ace_route_economics` |
| DP12 | `decision_log_entry` |
| DP13 | `v_ace_payment`, `proceeds`, `write_off`, `efs_ledger_outcome` |
| DP14 | `lov_value`, `role`, `permission`, `template`, `masking_rule`, `retention_rule`, … |

The exact assignment is PS v6's `sys_objects.data_product` seed, carried unchanged; the 24 objects with
no product are the OPS (13), AGT (8) and RPT (3) objects. This table is orientation only; the seed is
the source.

## 13. Personal data, synthetic data and fixtures

- No customer data is stored by this story. `sys_fields.is_personal` is metadata (a flag), not a
  value; the 526 marks are the deliverable BR7 requires.
- `data_product.owner_user_id` is a staff identifier and is personal by the protective reading
  (DF-REF-076 has no Inventory v4 row; the same pattern is personal elsewhere). The seed leaves it
  NULL; the load file carries a **synthetic** UUID per product; no name, ID number, account number or
  address appears in the migration, the seed, a fixture or a log.
- The test fixture list is field IDs plus object/field names only (schema metadata, no values).
- `reference-loads/data-product/` fixtures (TASK-06, TASK-14) hold synthetic product values only; the
  owner UUIDs are generated per test (`UUID.randomUUID()`), never reused and never real.

## 14. Values, grammar and texts used by the handler

### 14.1 System-of-record grammar (`ASM-E1001-09`)

`S` = one or more upper-case letters or digits (seed: ALS, SCBPDM, EFS, CCMS, SVAF, AMIS, RPS, LIT,
WIN, COLLINS, GL) or the phrase `the core bank`. `L` = `S`, or `S and S`, or `S, S, … and S`.
`Q` = free text without `;`, `(` or `)`. `Q3` = free text without `;`, `(` or `)` and without any name
of the `S` list.

| Form | Whole-value pattern (single spaces) | Seed rows |
|---|---|---|
| F1 | `ACE (ingested from L)` | DP01, DP02, DP05, DP06, DP11, DP13 |
| F2 | `ACE (ingested from L) for Q, with Q held in the Recovery Workbench` | DP04, DP07 |
| F3 | `Recovery Workbench`, optionally followed by ` document hub` or by `, with Q3` | DP03, DP08, DP09, DP10, DP12, DP14 |

F3 is a grammar, not a three-value list: rewording a Workbench qualifier through a catalog load is
accepted, a second source is not. Each of the 14 seed values matches exactly one form. Refused with
MSG-P1-003: `CCMS`; `ACE (ingested from CCMS); SVAF`; `ACE (ingested from CCMS) and CCMS`;
`Recovery Workbench and ACE`; `Recovery Workbench, with SVAF`; `ACE (ingested from )`;
`ACE (ingested from ccms)`; `ACE (ingested from CCMS) (ingested from SVAF)`; `Workbench`; and an empty
value.

### 14.2 LOV-REFRESH

`DAILY` 1, `WEEKLY` 2, `MONTHLY` 3, `ON_CHANGE` 4 (PS v6 lines 5035–5038). K5's `{values}` text is
`DAILY, WEEKLY, MONTHLY, ON_CHANGE`.

### 14.3 Message texts and placeholders

| ID | English | Thai | Placeholders |
|---|---|---|---|
| MSG-P1-003 | `{product} must name one system of record, written ACE (ingested from X) or Recovery Workbench, or both where the product holds both, and one named owner.` | MSG v4 line 77 Thai (written for the older English text), status Proposed (`GAP-E1001-14`) | `{product}` = product code |
| MSG-P1-004 | `The catalog must hold the 14 data products DP01 to DP14. Missing: {products}.` | MSG v4 line 78 | `{products}` = codes, ascending |
| MSG-P1-007 | `Row {row}: {field} must be one of {values}.` | MSG v4 line 81 | `{row}` 1-based data row; `{field}`; `{values}` |
| MSG-P1-011 | `The {source} load for {date} is already complete or running. It was not run again.` | MSG v4 line 85 | `{source}` = `data product catalog`; `{date}` = valid-from ISO date |

Rendered texts the unit tests assert:

- K0-H: `The data_product load was refused: the header must hold the 8 catalog columns. The version in force is unchanged.`
- K0-R (example): `The data_product load was refused: value too long for definition. The version in force is unchanged.`
- K4 (AC9): `Row 4: owner_role must be one of the role codes in LOV-ROLE.`
- K5 (AC9): `Row 5: refresh_cycle must be one of DAILY, WEEKLY, MONTHLY, ON_CHANGE.`

MSG-GEN-001 (`{field}`) and MSG-P3-027 (`{table}`, `{check}`) are already E1-042/E1-043 catalog
entries; this story adds only the four IDs above to `access.internal.FixedMessageCatalog` (EN and TH).

## 15. Test fixtures

| Fixture | Path | Content |
|---|---|---|
| Personal-field list | `TR/dictionary/is-personal-union-v4.tsv` | 526 field IDs (copy of `../specify/evidence/is_personal_union_v4.tsv`), field IDs only |
| Valid catalog (14 rows) | `TR/reference-loads/data-product/valid-14-rows.csv` | the § 10.1 values with synthetic owner UUIDs |
| Missing product | `TR/reference-loads/data-product/missing-dp09.csv` | 13 rows, no DP09 |
| Two systems | `TR/reference-loads/data-product/two-systems-dp06.csv` | DP06 `ACE (ingested from CCMS); SVAF` |
| No owner | `TR/reference-loads/data-product/no-owner-dp11.csv` | DP11 empty `owner_user_id` |
| Bare source | `TR/reference-loads/data-product/bare-source-dp06.csv` | DP06 `CCMS` |
| Bad list values | `TR/reference-loads/data-product/bad-role-and-refresh.csv` | row 4 `DP_OWNER`, row 5 `HOURLY` |
| Empty system (single defect) | `TR/reference-loads/data-product/empty-sor-dp06.csv` | DP06 empty, every other value valid |
| No owner (single defect) | `TR/reference-loads/data-product/no-owner-only-dp11.csv` | DP11 empty, every other value valid |
| Bad header | `TR/reference-loads/data-product/bad-header.csv` | seven columns, one renamed |
| Over-width | `TR/reference-loads/data-product/too-long-definition.csv` | `definition` 401 characters |
| Empty required | `TR/reference-loads/data-product/empty-product-name.csv` | `product_name` empty |
| Repeat | `TR/reference-loads/data-product/valid-14-rows.csv` loaded twice | same bytes (`validFrom` held) |
| Failing migration copy | generated at runtime from the classpath migration | one broken `valuation_ext` statement |

`TR` = `backend/src/test/resources`. `T` = `backend/src/test/java/th/co/scb/ace/demo/recovery`.
