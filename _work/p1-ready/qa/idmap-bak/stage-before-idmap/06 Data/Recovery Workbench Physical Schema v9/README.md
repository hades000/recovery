SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

# Recovery Workbench Physical Schema v9

| Item | Value |
|---|---|
| Version | 9 |
| Date | 27 November 2026 |
| Change log | v9 · 27 November 2026 · D-RCV-60 P1 developer readiness (RD-P1 register) · targeted edits. Earlier: 7, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash |
| Source | `06 Data/Recovery Workbench Physical Schema v6.sql` (read only, 16 November 2026, version 6) |
| Decision | D-RCV-60: adopt Architecture v5 and realign the documents (Physical Schema, LDM and ERD) |
| Tool | T3 Code / OpenCode / DeepSeek v4.1 Flash |
| Tables | 95 distinct tables (93 in the source, less `case_list_row` and `lake_copy_watermark`, plus `data_product_source`, `job_run`, `job_run_check` and `business_day_readiness`); 167 CREATE TABLE statements across the 19 files |
| Views | 32 views: 30 read-only ACE views plus the data dictionary view and the product catalog view |
| Foreign keys | 92 in the source; 44 kept inside one owner, 47 cut at an owner boundary after the `case_list_row` cut is retired, plus 3 keys on the new P1 tables (83 statements across the 19 files) |
| Indexes | 112 from the source, less the 2 of `case_list_row`, plus 9 added P1 indexes (119) |
| Dictionary comments | 163 `COMMENT ON TABLE` and 1651 `COMMENT ON COLUMN` statements across the 19 files, including the migration provenance columns |
| Seed rows | 2619 INSERT statements |

## 1. What this folder is

The Physical Schema v6 was one file in one `recovery` schema. Architecture v5 slides 12, 20, 29 and 41 put one schema and one login per service inside the single ACE database, so this version splits the same DDL into 19 `rwb_<name>.sql` files, one per service in the Ownership Map. Every table, column, constraint, index, comment, seed row and view of v6 is carried over unchanged; the only changes are the schema name, the foreign keys that cross an owner boundary, and the placement of the four platform library objects.

The source text is never edited. Each file states the source it came from and the change log row.

## 2. Files

| File | Code | Service | Wave | Schema | Tables owned | Hosted PLT tables | Library objects | FK kept | Indexes |
|---|---|---|---|---|---|---|---|---|---|
| `rwb_source_data.sql` | P1 | rwb-source-data | 1 | `rwb_source_data` | 20 | 0 | 4 | 8 | 26 |
| `rwb_integration.sql` | P2 | rwb-integration | 1 | `rwb_integration` | 3 | 2 | 4 | 2 | 4 |
| `rwb_case.sql` | P3 | rwb-case | 1 | `rwb_case` | 15 | 0 | 4 | 15 | 27 |
| `rwb_access.sql` | P4 | rwb-access | 1 | `rwb_access` | 5 | 0 | 4 | 3 | 5 |
| `rwb_document.sql` | P5 | rwb-document | 1 | `rwb_document` | 12 | 0 | 4 | 11 | 30 |
| `rwb_comms.sql` | P6 | rwb-comms | 1 | `rwb_comms` | 3 | 0 | 4 | 3 | 9 |
| `rwb_decision.sql` | P7 | rwb-decision | 1 | `rwb_decision` | 6 | 0 | 4 | 8 | 14 |
| `rwb_payment.sql` | P8 | rwb-payment | 2 | `rwb_payment` | 1 | 0 | 4 | 2 | 7 |
| `rwb_reporting.sql` | P9 | rwb-reporting | 1 | `rwb_reporting` | 3 | 0 | 4 | 2 | 4 |
| `rwb_agent.sql` | P10 | rwb-agent | 1 | `rwb_agent` | 8 | 0 | 4 | 6 | 11 |
| `rwb_valuation.sql` | S1 | rwb-valuation | 3 | `rwb_valuation` | 0 | 0 | 4 | 2 | 4 |
| `rwb_treatment.sql` | S2 | rwb-treatment | 2 | `rwb_treatment` | 1 | 0 | 4 | 2 | 6 |
| `rwb_guarantee.sql` | S3 | rwb-guarantee | 3 | `rwb_guarantee` | 1 | 0 | 4 | 2 | 5 |
| `rwb_litigation.sql` | S4 | rwb-litigation | 3 | `rwb_litigation` | 2 | 0 | 4 | 3 | 7 |
| `rwb_asset.sql` | S5 | rwb-asset | 2 | `rwb_asset` | 2 | 0 | 4 | 3 | 7 |
| `rwb_debtsale.sql` | S6 | rwb-debtsale | 3 | `rwb_debtsale` | 2 | 0 | 4 | 3 | 7 |
| `rwb_writeoff.sql` | S7 | rwb-writeoff | 4 | `rwb_writeoff` | 1 | 0 | 4 | 2 | 6 |
| `rwb_deviation.sql` | S8 | rwb-deviation | 2 | `rwb_deviation` | 1 | 0 | 4 | 2 | 5 |
| `rwb_partner.sql` | S9 | rwb-partner | 4 | `rwb_partner` | 3 | 0 | 4 | 4 | 7 |
| `recovery_views.sql` | P1 | rwb-source-data | 1 | `rwb_source_data` and `recovery` | 0 | 0 | 0 | 0 | 0 |

`recovery_views.sql` holds the data dictionary view and the product catalog view in `rwb_source_data` and the 30 ACE views in `recovery`. No table is created there.

## 3. Source coverage

The counts in this table describe the v6 source. Version 9 changes against it are in section 12.

| Source object | Count | Where it goes |
|---|---|---|
| Tables | 93 | the file of the owner in the Ownership Map |
| Views | 31 | `recovery_views.sql` |
| Foreign keys | 92 | kept when both tables share an owner, otherwise cut to a plain uuid column |
| Indexes | 112 | the file of the table owner |
| Table and column comments | 89 and 1026 | the file of the table owner |
| Seed INSERT statements | 2584 | the file of the table owner |
| Schema, search path, pgcrypto | 1 | every file creates its own schema and sets its own search path |

The four extension tables (`party_ext`, `contact_point_ext`, `account_ext`, `valuation_ext`) have column comments in v6 but no `COMMENT ON TABLE`; that is kept as found (GAP-0113).

## 4. Ownership

Ownership is taken from `22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx`, sheet Tables, for all 93 tables. The 19 service rows and the wave order are from sheet Services.

| Code | Service | Wave | Schema | Login | REST base | Topic | Queue |
|---|---|---|---|---|---|---|---|
| P1 | rwb-source-data | 1 | `rwb_source_data` | `rwb_source_data` | `/api/recovery/source-data/v1` | `rwb.source-data.events.v1` | `rwb-source-data` |
| P2 | rwb-integration | 1 | `rwb_integration` | `rwb_integration` | `/api/recovery/integration/v1` | `rwb.integration.events.v1` | `rwb-integration` |
| P3 | rwb-case | 1 | `rwb_case` | `rwb_case` | `/api/recovery/case/v1` | `rwb.case.events.v1` | `rwb-case` |
| P4 | rwb-access | 1 | `rwb_access` | `rwb_access` | `/api/recovery/access/v1` | `rwb.access.events.v1` | `rwb-access` |
| P5 | rwb-document | 1 | `rwb_document` | `rwb_document` | `/api/recovery/document/v1` | `rwb.document.events.v1` | `rwb-document` |
| P6 | rwb-comms | 1 | `rwb_comms` | `rwb_comms` | `/api/recovery/comms/v1` | `rwb.comms.events.v1` | `rwb-comms` |
| P7 | rwb-decision | 1 | `rwb_decision` | `rwb_decision` | `/api/recovery/decision/v1` | `rwb.decision.events.v1` | `rwb-decision` |
| P8 | rwb-payment | 2 | `rwb_payment` | `rwb_payment` | `/api/recovery/payment/v1` | `rwb.payment.events.v1` | `rwb-payment` |
| P9 | rwb-reporting | 1 | `rwb_reporting` | `rwb_reporting` | `/api/recovery/reporting/v1` | `rwb.reporting.events.v1` | `rwb-reporting` |
| P10 | rwb-agent | 1 | `rwb_agent` | `rwb_agent` | `/api/recovery/agent/v1` | `rwb.agent.events.v1` | `rwb-agent` |
| S1 | rwb-valuation | 3 | `rwb_valuation` | `rwb_valuation` | `/api/recovery/valuation/v1` | `rwb.valuation.events.v1` | `rwb-valuation` |
| S2 | rwb-treatment | 2 | `rwb_treatment` | `rwb_treatment` | `/api/recovery/treatment/v1` | `rwb.treatment.events.v1` | `rwb-treatment` |
| S3 | rwb-guarantee | 3 | `rwb_guarantee` | `rwb_guarantee` | `/api/recovery/guarantee/v1` | `rwb.guarantee.events.v1` | `rwb-guarantee` |
| S4 | rwb-litigation | 3 | `rwb_litigation` | `rwb_litigation` | `/api/recovery/litigation/v1` | `rwb.litigation.events.v1` | `rwb-litigation` |
| S5 | rwb-asset | 2 | `rwb_asset` | `rwb_asset` | `/api/recovery/asset/v1` | `rwb.asset.events.v1` | `rwb-asset` |
| S6 | rwb-debtsale | 3 | `rwb_debtsale` | `rwb_debtsale` | `/api/recovery/debtsale/v1` | `rwb.debtsale.events.v1` | `rwb-debtsale` |
| S7 | rwb-writeoff | 4 | `rwb_writeoff` | `rwb_writeoff` | `/api/recovery/writeoff/v1` | `rwb.writeoff.events.v1` | `rwb-writeoff` |
| S8 | rwb-deviation | 2 | `rwb_deviation` | `rwb_deviation` | `/api/recovery/deviation/v1` | `rwb.deviation.events.v1` | `rwb-deviation` |
| S9 | rwb-partner | 4 | `rwb_partner` | `rwb_partner` | `/api/recovery/partner/v1` | `rwb.partner.events.v1` | `rwb-partner` |

Twelve Owning-Map rulings move a table away from the module that declared it in a TSD (ASM-0067 to ASM-0081). This folder applies the ruling, not the TSD: `interaction` and `efs_ledger_outcome` to P1, `delegation_limit` to P4, `lov_value` to P3, `partner_user` to S9, `retention_rule` and `signature_request` to P5, `rule_package*` and `rule_test_case` to P7, `job_catalog` to P2, `timer` to P3, `valuation_ext` to P1, and the feature flags to the platform library.

## 5. Cross-service references (FK cuts)

A foreign key is kept only when both tables have the same owner in the Ownership Map. The 48 keys below crossed an owner boundary in the source (the `case_list_row` key is retired with its table), so the column stays a plain uuid and integrity is through the owner's API contract (or the shared event). The Ownership Map sheet `FK cuts` was generated empty in v1 (it has the header row only), so the list is derived from sheet Tables (GAP-0107; ASM-0178).

| # | From table | From service | Column | To table | To service | Becomes |
|---|---|---|---|---|---|---|
| 1 | `deviation` | rwb-deviation (S8) | `case_id` | `recovery_case` | rwb-case (P3) | plain uuid; integrity through the rwb-case contract |
| 2 | `timer` | rwb-case (P3) | `treatment_id` | `treatment` | rwb-treatment (S2) | plain uuid; integrity through the rwb-treatment contract |
| 3 | `treatment` | rwb-treatment (S2) | `case_id` | `recovery_case` | rwb-case (P3) | plain uuid; integrity through the rwb-case contract |
| 4 | `treatment` | rwb-treatment (S2) | `decision_log_id` | `decision_log_entry` | rwb-decision (P7) | plain uuid; integrity through the rwb-decision contract |
| 5 | `guarantee_claim` | rwb-guarantee (S3) | `case_id` | `recovery_case` | rwb-case (P3) | plain uuid; integrity through the rwb-case contract |
| 6 | `legal_action` | rwb-litigation (S4) | `case_id` | `recovery_case` | rwb-case (P3) | plain uuid; integrity through the rwb-case contract |
| 7 | `legal_action` | rwb-litigation (S4) | `law_firm_id` | `partner` | rwb-partner (S9) | plain uuid; integrity through the rwb-partner contract |
| 8 | `notice` | rwb-comms (P6) | `case_id` | `recovery_case` | rwb-case (P3) | plain uuid; integrity through the rwb-case contract |
| 9 | `notice` | rwb-comms (P6) | `document_id` | `document` | rwb-document (P5) | plain uuid; integrity through the rwb-document contract |
| 10 | `notice` | rwb-comms (P6) | `dispatch_file_id` | `outbound_item` | rwb-integration (P2) | plain uuid; integrity through the rwb-integration contract |
| 11 | `partner_instruction` | rwb-partner (S9) | `case_id` | `recovery_case` | rwb-case (P3) | plain uuid; integrity through the rwb-case contract |
| 12 | `debt_sale_lot` | rwb-debtsale (S6) | `buyer_partner_id` | `partner` | rwb-partner (S9) | plain uuid; integrity through the rwb-partner contract |
| 13 | `interaction` | rwb-source-data (P1) | `case_id` | `recovery_case` | rwb-case (P3) | plain uuid; integrity through the rwb-case contract |
| 14 | `interaction` | rwb-source-data (P1) | `decision_log_id` | `decision_log_entry` | rwb-decision (P7) | plain uuid; integrity through the rwb-decision contract |
| 15 | `interaction` | rwb-source-data (P1) | `treatment_id` | `treatment` | rwb-treatment (S2) | plain uuid; integrity through the rwb-treatment contract |
| 16 | `interaction` | rwb-source-data (P1) | `proceeds_id` | `proceeds` | rwb-payment (P8) | plain uuid; integrity through the rwb-payment contract |
| 17 | `document` | rwb-document (P5) | `case_id` | `recovery_case` | rwb-case (P3) | plain uuid; integrity through the rwb-case contract |
| 18 | `document` | rwb-document (P5) | `template_id` | `template` | rwb-comms (P6) | plain uuid; integrity through the rwb-comms contract |
| 19 | `document` | rwb-document (P5) | `treatment_id` | `treatment` | rwb-treatment (S2) | plain uuid; integrity through the rwb-treatment contract |
| 20 | `decision_log_entry` | rwb-decision (P7) | `case_id` | `recovery_case` | rwb-case (P3) | plain uuid; integrity through the rwb-case contract |
| 21 | `proceeds` | rwb-payment (P8) | `case_id` | `recovery_case` | rwb-case (P3) | plain uuid; integrity through the rwb-case contract |
| 22 | `proceeds` | rwb-payment (P8) | `treatment_id` | `treatment` | rwb-treatment (S2) | plain uuid; integrity through the rwb-treatment contract |
| 23 | `write_off` | rwb-writeoff (S7) | `case_id` | `recovery_case` | rwb-case (P3) | plain uuid; integrity through the rwb-case contract |
| 24 | `write_off` | rwb-writeoff (S7) | `decision_log_id` | `decision_log_entry` | rwb-decision (P7) | plain uuid; integrity through the rwb-decision contract |
| 25 | `case_list_row` | rwb-source-data (P1) | `case_id` | `recovery_case` | rwb-case (P3) | plain uuid; integrity through the rwb-case contract |
| 26 | `retention_rule` | rwb-document (P5) | `reference_version_id` | `reference_version` | rwb-case (P3) | plain uuid; integrity through the rwb-case contract |
| 27 | `dp_treatment` | rwb-source-data (P1) | `treatment_id` | `treatment` | rwb-treatment (S2) | plain uuid; integrity through the rwb-treatment contract |
| 28 | `dp_treatment` | rwb-source-data (P1) | `case_id` | `recovery_case` | rwb-case (P3) | plain uuid; integrity through the rwb-case contract |
| 29 | `dp_treatment` | rwb-source-data (P1) | `decision_log_id` | `decision_log_entry` | rwb-decision (P7) | plain uuid; integrity through the rwb-decision contract |
| 30 | `dp_guarantee_claim` | rwb-source-data (P1) | `guarantee_claim_id` | `guarantee_claim` | rwb-guarantee (S3) | plain uuid; integrity through the rwb-guarantee contract |
| 31 | `dp_guarantee_claim` | rwb-source-data (P1) | `case_id` | `recovery_case` | rwb-case (P3) | plain uuid; integrity through the rwb-case contract |
| 32 | `outbox_event` | platform library (PLT) | `case_id` | `recovery_case` | rwb-case (P3) | plain uuid; integrity through the rwb-case contract |
| 33 | `outbox_delivery` | platform library (PLT) | `task_id` | `task` | rwb-case (P3) | plain uuid; integrity through the rwb-case contract |
| 34 | `document_type` | rwb-document (P5) | `reference_version_id` | `reference_version` | rwb-case (P3) | plain uuid; integrity through the rwb-case contract |
| 35 | `document_checklist_item` | rwb-document (P5) | `reference_version_id` | `reference_version` | rwb-case (P3) | plain uuid; integrity through the rwb-case contract |
| 36 | `case_document_check` | rwb-document (P5) | `case_id` | `recovery_case` | rwb-case (P3) | plain uuid; integrity through the rwb-case contract |
| 37 | `case_document_check` | rwb-document (P5) | `last_event_id` | `outbox_event` | platform library (PLT) | plain uuid; integrity through the platform library contract |
| 38 | `document_hub_parameter` | rwb-document (P5) | `reference_version_id` | `reference_version` | rwb-case (P3) | plain uuid; integrity through the rwb-case contract |
| 39 | `document_intake` | rwb-document (P5) | `partner_id` | `partner` | rwb-partner (S9) | plain uuid; integrity through the rwb-partner contract |
| 40 | `document_intake` | rwb-document (P5) | `case_id` | `recovery_case` | rwb-case (P3) | plain uuid; integrity through the rwb-case contract |
| 41 | `retention_action` | rwb-document (P5) | `decision_log_id` | `decision_log_entry` | rwb-decision (P7) | plain uuid; integrity through the rwb-decision contract |
| 42 | `signature_request` | rwb-document (P5) | `case_id` | `recovery_case` | rwb-case (P3) | plain uuid; integrity through the rwb-case contract |
| 43 | `signature_request` | rwb-document (P5) | `treatment_id` | `treatment` | rwb-treatment (S2) | plain uuid; integrity through the rwb-treatment contract |
| 44 | `approval` | rwb-decision (P7) | `case_id` | `recovery_case` | rwb-case (P3) | plain uuid; integrity through the rwb-case contract |
| 45 | `approval` | rwb-decision (P7) | `delegation_limit_id` | `delegation_limit` | rwb-access (P4) | plain uuid; integrity through the rwb-access contract |
| 46 | `agent_run` | rwb-agent (P10) | `case_id` | `recovery_case` | rwb-case (P3) | plain uuid; integrity through the rwb-case contract |
| 47 | `agent_run` | rwb-agent (P10) | `decision_log_id` | `decision_log_entry` | rwb-decision (P7) | plain uuid; integrity through the rwb-decision contract |
| 48 | `agent_feedback` | rwb-agent (P10) | `decision_log_id` | `decision_log_entry` | rwb-decision (P7) | plain uuid; integrity through the rwb-decision contract |

The cut is written twice in each affected file: a trailing comment on the column and a note block at the end of the file. The constraint name from v6 is recorded there so the original key can be traced.

Three of the 48 cuts have both tables in the same output file (`outbox_event.case_id` and `outbox_delivery.task_id` in `rwb_case.sql`, `case_document_check.last_event_id` in `rwb_document.sql`). They are still cut, because the library object is identical in all 19 schemas and must not carry conditional foreign keys (ASM-0180).

## 6. Platform library objects

The Ownership Map gives six tables to PLT, the platform library. Architecture v5 slide 20 and DP-09 make the outbox, inbox and idempotency objects part of every service schema, and the library is not one of the 19 services.

| Object | Owner | Emitted in | Reason |
|---|---|---|---|
| `outbox_event` | PLT | all 19 files | RWB-PLT-TE006-CON; DP-09; Ownership Map ruling ASM-0074 |
| `outbox_delivery` | PLT | all 19 files | same |
| `processed_event` | PLT | all 19 files | same |
| `idempotency_key` | PLT | all 19 files | same |
| `feature_flag` | PLT | `rwb_integration.sql` only | platform library; rwb-integration serves the admin API (ruling ASM-0039) |
| `feature_flag_change` | PLT | `rwb_integration.sql` only | same |

The four per-schema objects carry no foreign key to a business table. Their one shared key, `processed_event.event_id` to `outbox_event.id`, is kept inside each schema. The placement is a realignment decision, not a source value (GAP-0109; ASM-0180).

`decision_record` (Architecture v5 slide 20; RD-P1-068 rule 8). Every service, `rwb_source_data` included, has a local decision record table. The shared library migration of RWB-PLT-E1027-CON creates it once per schema, so no file in this folder creates it. Its DDL is Pending, owner platform lead (library owner), NEW-GAP-F08-7; until then the library's own migration runs in the Testcontainers build.

## 7. Views

- `rwb_source_data.v_data_dictionary` is the v6 `v_data_dictionary` view, re-qualified to the three P1 tables it reads (`sys_fields`, `sys_objects`, `data_product`).
- The 30 `recovery.v_ace_*` views stay in schema `recovery` and are read only. This follows Architecture v5 slide 29, which keeps `recovery.v_ace_*` SELECT-only for `rwb_source_data`, and DP-05, which allows a service to read ACE only through the rwb-source-data contract or its own ACE views (GAP-0110; ASM-0181).
- The three helper functions (`ace_to_date`, `ace_to_boolean`, `ace_mask_value`) stay in schema `recovery` because the views call them.
- The grants block stays a comment (GAP-0111) and the 19 logins are created by RWB-PLT-NF06. Only the login `rwb_source_data` is granted SELECT on the 30 views, one GRANT per view; no other service reads the views (ACE single-reader rule).

## 8. Objects with a note

| Object | Note |
|---|---|
| `lake_copy_watermark` | Not created (RD-P1-021, RD-P1-024): the data lake is removed (Architecture v5 slide 37; DP-17). The former DDL is kept as comment text; its dictionary rows are marked retired (GAP-0114). |
| `case_list_row` | Not created (RD-P1-024): rwb-case holds the case list. The former DDL is kept as comment text; its dictionary rows are marked retired. |
| `rwb_valuation.sql` | rwb-valuation owns no table. `valuation_ext` stays in rwb_source_data (ruling ASM-0081) and route economics come from ACE through the rwb-source-data contract. The file holds the schema, the library objects and a note (GAP-0108; ASM-0179). |
| `decision_log_entry`, `interaction` | The append-only trigger `refuse_change()` and its two triggers are kept with the owning service (`rwb_decision.sql`, `rwb_source_data.sql`). |

## 9. Run order and Flyway

1. `rwb_<name>.sql` for each service, in wave order: P1 to P10 and S1 to S9 by table above. Each file is self-contained in its own schema.
2. `recovery_views.sql` after `rwb_source_data.sql`, because the dictionary view reads three P1 tables. The ACE views read only `public` tables.

Per-service Flyway (DP-15, ADR-021): one `V0001` baseline per schema. The source split V0001 tables and dictionary, V0002 Tier 1 views and V0003 Tier 2 views; the per-service sequence is not fixed in the source documents (GAP-0112; ASM-0183).

## 10. Gaps and assumptions

| ID | Gap | Assumption |
|---|---|---|
| GAP-0107 / ASM-0178 | The Ownership Map sheet `FK cuts` has only a header, while 48 cross-owner foreign keys exist in v6. | The cuts are derived from sheet Tables: a difference in owner means a cut. |
| GAP-0108 / ASM-0179 | rwb-valuation owns no table in the map. | The service reads ACE through the rwb-source-data contract and keeps no local table until a TSD adds one. |
| GAP-0109 / ASM-0180 | The map does not say where the six PLT tables live after the split. | The four outbox, inbox and idempotency objects go in every service schema; the two feature-flag tables go in rwb_integration. |
| GAP-0110 / ASM-0181 | The map does not say which schema holds the 30 ACE views. | They stay in schema `recovery`, read only, as Architecture v5 slide 29 describes. |
| GAP-0111 / ASM-0182 | The source grants use `:recovery_role` and `:ace_view_owner` placeholders; the 19 logins are not in the SQL. | The grants block stays a commented template; RWB-PLT-NF06 and RWB-PLT-N011 create the 19 logins and privileges. |
| GAP-0112 / ASM-0183 | The per-service Flyway sequence is not specified. | One V0001 per schema (DP-15); the view file follows the source V0002 and V0003 sections. |
| GAP-0113 / ASM-0184 | The four extension tables have no `COMMENT ON TABLE` in v6. | Kept as found; the column comments still feed the data dictionary. |
| GAP-0114 / ASM-0185 | `lake_copy_watermark` has an owner but no target. | Not created; the former DDL is kept as comment text and the dictionary rows are marked retired. |

## 11. Checks

- Every one of the 91 source tables that is still created appears in exactly one service file, except the four library objects, which appear in all 19.
- Every one of the 31 source views appears once in `recovery_views.sql`.
- Every foreign key kept inside a file points to a table created in that file; no file references another service's schema.
- Every index, comment and seed row points to a table created in the same file.
- The two header lines and the D-RCV-60 change-log row are at the top of every file.

## 12. Version 9 changes (D-RCV-60 P1 developer readiness, RD-P1 register)

| Change | Files | Decision or story |
|---|---|---|
| `case_list_row` and `lake_copy_watermark` retired from executable DDL; dictionary rows marked retired (`is_active` false, `state` RETIRED) | rwb_source_data.sql | RD-P1-021, RD-P1-024, RD-P1-025 |
| New `data_product_source` with 12 seed rows; core bank source code of DP02 and DP04 Pending (ASM-5695) | rwb_source_data.sql | RD-P1-021 |
| New `job_run`, `job_run_check`, `business_day_readiness` | rwb_source_data.sql | RD-P1-020 |
| `data_product.system_of_record` widened to varchar(200) and the 14 seed values replaced | rwb_source_data.sql | RD-P1-025 |
| `uk_interaction_case_seq`, `contact_point_ext.person_key` and its check, and nine indexes | rwb_source_data.sql | RWB-P1-E1011, E1016, E1066, E1068, E2022, E2034 |
| `migration_source` and `migrated_at` once on each of the 49 tables that receive migrated rows (`case_list_row` is no longer one) | rwb_*.sql | RD-P1-027 |
| ACE view field types in `sys_fields` aligned to the explicit casts of the views (92 fields) | rwb_source_data.sql | review findings on RWB-P1-E1013, E1018, E1055, AD018 |
| Grants block: single reader `rwb_source_data` | recovery_views.sql | ACE single-reader rule |
| `interaction.document_id` (nullable uuid, no foreign key) with its comment and dictionary row DF-INT-030 | rwb_source_data.sql | NEW-GAP-S8-12; ledger contract `documentId` |
| `v_data_product_catalog` added; commented grants block gains the Section B table grant and the ownership note | recovery_views.sql | RWB-P1-E1016-DB, RWB-P1-E1069-DB |
| `is_personal` set true for 13 person key fields and `job_run.requested_by`; physical types of 13 ACE view fields corrected; failed-contact count-once rule in the `processed_event` and `failed_count` descriptions | rwb_source_data.sql | Data Classification v6; ACE Field Gap List v2; RD-P1-070 |
| Local `decision_record`: created by the library migration, not by these files (section 6) | README.md | RD-P1-068 rule 8 |

The dictionary seed holds 127 object rows and 1,409 field rows: the 123 and 1,379 baseline, `data_product_source` (1 and 3), and the rows added by later story migrations (3 objects and 25 fields of the run and readiness tables, DF-EXT-050 and DF-INT-030).

