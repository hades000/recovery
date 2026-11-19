---
title: "Data model: RWB-E1-069 Read-only ACE source views, grants and boundary rule"
run_id: "INC-010-epic-1-RWB-E1-069"
story: "RWB-E1-069"
revision: "v1 (18 Nov 2026): first plan stage for this run, against spec revision 4"
---

# Data model: RWB-E1-069

This story publishes a read interface and changes privileges; it creates no table (D-RUN-12). The four extension tables and the dictionary rows are created by the RWB-E1-001 migration and are verified here (SPEC-007). Column lists below are cited from ACE Source Views v1 lines 94-711; the field IDs are the DF-ACE ranges of story §11, which the plan re-counted per view and matched against the source aliases.

## 1. The published read interface: 30 views

Section A = 16 views, 177 columns, `DF-ACE-001..177`. Section B = 14 views, 127 columns, `DF-ACE-178..304`. No primary key, no foreign key, no `security_invoker`, owner `ace_view_owner`, SELECT to `recovery_svc` only.

### Section A (file `V<seq>__rwb_e1_069_ace_source_views.sql`)

| View | DF-ACE | Cols | Source table(s) | Columns (in view order) |
|---|---|---|---|---|
| `v_ace_account` | 001-042 | 42 | `public.account` | account_key, account_code, account_name, account_status, account_status_date, contract_no, contract_date, product_key, product_type, product_category, product_category_efs, branch_code, branch_name, oc_code, company_code, collection_officer, collection_phase, days_past_due, classification, total_balance, accounting_balance, past_due_amount, total_interest_fin_charge, collections_fee, interest_rate, last_payment_date, last_payment_amount, next_installment_date, next_installment_amount, last_tdr_date, tdr_flag, rescheduled_flag, number_reschedules, tdr_aging, principle_not_reduce, data_as_of, days_since_last_contact, days_since_last_collection_activity, relationship_manager, relationship_manager_phone, special_memo, expiry_date |
| `v_ace_payment` | 043-054 | 12 | `public.payment` | payment_code, account_key, payment_date, payment_amount, capital_amount, interest_amount, expense_amount, commission_amount, payment_channel, description, comments, data_as_of |
| `v_ace_customer` | 055-074 | 20 | `public.customer` | cif_no, person_key, first_name, last_name, date_of_birth, deceased_date, deceased_flag, gender, nationality, marital_status, occupation, spouse_name, customer_status, category, country_of_residence, is_staff, branch_code, vat_number, id_no_masked, id_no_last4 |
| `v_ace_contact` | 075-083 | 9 | `public.phone`, `public.email`, `public.address` | contact_type, contact_key, person_key, contact_value, contact_value_masked, usage_code, city, post_code, country |
| `v_ace_ca_relation` | 084-088 | 5 | `public.ca_relation` | person_key, account_key, relation_type, amount_of_guarantee, date_of_guarantee |
| `v_ace_aa_relation` | 089-090 | 2 | `public.aa_relation` | parent_account_key, child_account_key |
| `v_ace_collateral` | 091-098 | 8 | `public.collateral` | collateral_no, asset_key, account_key, collateral_value, register_date, in_active, collateral_type, description |
| `v_ace_asset` | 099-107 | 9 | `public.asset` | asset_ref, asset_key, asset_type, description, address, town, post_code, county, country |
| `v_ace_efs_action` | 108-127 | 20 | `public.efs_action` | efs_record_key, account_key, person_key, action_code, action_code_name, action_date, contact_at, user_code, comments, is_call, is_rpc, is_ptp, promise_status, promise_eval_status, promise_date, promise_amount, collection_phase, act_date_bucket, act_date_past_due_days, last_tdr_date |
| `v_ace_efs_action_code` | 128-130 | 3 | `public.efs_action_code` | action_code, action_name, category |
| `v_ace_efs_assignment` | 131-139 | 9 | `public.efs_assignment` | account_key, assignment_scheme, assignee_code, assignee_name, assignment_start_date, assignment_end_date, assignment_start_total_balance, assignment_end_total_balance, distribution_area |
| `v_ace_bucket_log` | 140-145 | 6 | `public.bucket_log_snapshot` | account_key, snapshot_year, snapshot_month, bucket, past_due_amount, snapshot_month_start |
| `v_ace_product` | 146-150 | 5 | `public.product` | product_code, product_name, product_type, product_category, product_category_efs |
| `v_ace_branch` | 151-154 | 4 | `public.branch` | branch_code, branch_name, address, phone |
| `v_ace_holiday` | 155-159 | 5 | `public.bot_holiday` | holiday_date, holiday_year, holiday_name, holiday_name_thai, holiday_weekday |
| `v_ace_plan` | 160-177 | 18 | `public.ace_case`, `public.cfsc_mg_ssme_tdr_case`, `public.tdr_calculation`, `public.ai_recommended_plan` | plan_ref, ace_case_id, plan_status, plan_created_at, tdr_calculation_id, plan_published_at, associated_account_id, account_key, booked_at, approved_at, submitted_at, closed_at, closed_reason, ca_approved_at, installments, recommended_installment, recommended_package, plan_status_as_of |

### Section B (file `V<seq>__rwb_e1_069_ace_tier2_views.sql`)

| View | DF-ACE | Cols | Source table | Columns (in view order) |
|---|---|---|---|---|
| `v_ace_batch_status` | 178-186 | 9 | `public.ace_batch_run` | source_system, business_date, started_at, completed_at, status, record_count, checksum, feed_version, is_complete |
| `v_ace_valuation` | 187-195 | 9 | `public.valuation` | valuation_key, asset_key, appraisal_no, appraisal_type, appraised_value, forced_sale_value, appraisal_date, source_system, data_as_of |
| `v_ace_collateral_detail` | 196-207 | 12 | `public.collateral_detail` | asset_key, title_doc_no, plot_no, area_text, province, district, subdistrict, insured_value, insurance_expiry, lien_rank, source_system, data_as_of |
| `v_ace_npa_asset` | 208-219 | 12 | `public.npa_asset` | asset_ref, asset_key, asset_code, transfer_in_type, from_segment, transfer_in_date, book_value, auction_purchase_price, repossessed_date, stock_date, source_system, data_as_of |
| `v_ace_npa_sale` | 220-230 | 11 | `public.npa_sale` | npa_sale_key, npa_asset_key, contract_date, sale_date, sale_price, transfer_fee, specific_business_tax, corporate_income_tax, incentive_amount, source_system, data_as_of |
| `v_ace_lawsuit` | 231-243 | 13 | `public.lawsuit` | lawsuit_key, account_key, lawsuit_no, black_case_no, red_case_no, court_name, claim_amount, filed_date, judgment_date, judgment_amount, lit_status, source_system, data_as_of |
| `v_ace_hearing` | 244-250 | 7 | `public.hearing` | hearing_key, lawsuit_key, hearing_date, hearing_type, next_date, source_system, data_as_of |
| `v_ace_pod` | 251-260 | 10 | `public.pod_receipt` | pod_key, account_key, notice_ref, sent_date, barcode, callback_date, delivery_status, sent_type, source_system, data_as_of |
| `v_ace_write_off` | 261-269 | 9 | `public.gl_write_off` | write_off_key, account_key, amount, posted_date, responsibility_center, cost_center, gl_product, source_system, data_as_of |
| `v_ace_score` | 270-279 | 10 | `public.collins_score` | score_key, account_key, model_code, model_version, score_value, estimate_value, route_code, scored_at, source_system, data_as_of |
| `v_ace_party_product` | 280-285 | 6 | `public.party_product` | person_key, account_no, account_key, product_type, product_status, data_as_of |
| `v_ace_credit_decision` | 286-293 | 8 | `public.credit_decision` | credit_decision_key, account_key, nleads_ref, credit_result, credit_result_reason, decided_at, source_system, data_as_of |
| `v_ace_esign` | 294-300 | 7 | `public.esign_request` | esign_key, account_key, external_ref, requested_at, status, source_system, data_as_of |
| `v_ace_iam_group` | 301-304 | 4 | `public.iam_group` | entra_group, role_code, source_system, data_as_of |

### Column rules

| Rule | Where |
|---|---|
| Text dates become dates through `ace_to_date`; a dirty or impossible value returns NULL, never an error | `v_ace_payment.payment_date` is the only `ace_to_date` call ([S2] line 152); other date columns are already `date` in ACE |
| Y/N flags become booleans through `ace_to_boolean` | `v_ace_account.tdr_flag` (`is_restructured`), `rescheduled_flag` (`is_rescheduled`), `v_ace_customer.deceased_flag` (`is_deceased`), `v_ace_customer.is_staff` |
| Identity number is never exposed in clear | `v_ace_customer.id_no_masked` (`ace_mask_value(identification_number)`) and `id_no_last4`; no `identification_number` or `id_no` column |
| Contact values keep a masked copy | `v_ace_contact.contact_value` and `contact_value_masked` (`ace_mask_value` over phone, email, address) |
| Every `public.<table>` qualifier stays; every `recovery.` qualifier is written `${recoverySchema}.` | The 30 bodies; no body is otherwise edited |
| `CREATE OR REPLACE VIEW`, no `security_invoker` | All 30; definer rights (ASM-002, OI-069-H) |

## 2. The four extension tables (created by RWB-E1-001, verified here)

| Table | Cols | PK | Business columns (type, default) | Other |
|---|---|---|---|---|
| `party_ext` | 12 | `person_key varchar(255)` | `vulnerable boolean NOT NULL DEFAULT false`, `deceased_override boolean NOT NULL DEFAULT false`, `bankruptcy boolean NOT NULL DEFAULT false`, `fraud_flag boolean NOT NULL DEFAULT false` | DF-EXT-001..012 |
| `contact_point_ext` | 14 | `contact_key varchar(255)` | `contact_type varchar(10) NOT NULL`, `consent_given boolean NOT NULL DEFAULT false`, `consent_at timestamptz`, `verified_at timestamptz`, `failed_count integer NOT NULL DEFAULT 0`, `source varchar(20) NOT NULL DEFAULT 'WORKBENCH'` | DF-EXT-013..026; `ck_contact_point_ext_type` allows PHONE, EMAIL, ADDRESS |
| `account_ext` | 9 | `account_key varchar(255)` | `dispute_open boolean NOT NULL DEFAULT false` | DF-EXT-027..035 |
| `valuation_ext` | 14 | `valuation_key varchar(255)` | `accepted boolean NOT NULL DEFAULT false`, `accepted_at timestamptz`, `accepted_by uuid`, `valuer_partner_id uuid`, `stale_flag boolean NOT NULL DEFAULT false`, `age_days integer` | DF-EXT-036..049 |

**The seven standard columns** on each table, in this order after the business columns: `is_active boolean NOT NULL DEFAULT true`, `state varchar(40)`, `version integer NOT NULL DEFAULT 1`, `created_at timestamptz NOT NULL DEFAULT now()`, `created_by uuid`, `updated_at timestamptz NOT NULL DEFAULT now()`, `updated_by uuid`. 49 columns in all and 49 `sys_fields` rows.

**Constraints checked**: the exact column set equals the table above; no foreign key references schema `public`; no business column has the same name as a column of the ACE view it extends (`v_ace_customer`, `v_ace_contact`, `v_ace_account`, `v_ace_valuation`); a second `party_ext` row for `P0000123` fails with 23505 on `party_ext_pkey`.

## 3. Dictionary

| Measure | Value | Source of truth |
|---|---|---|
| `v_data_dictionary` objects / fields | 123 / 1,382 | RWB-E1-001 seed: Physical Schema v6 (1,379) plus DF-REF-300..302; DG-L05 |
| Table fields | 1,078, of which 49 on the four extension tables | RWB-E1-001 seed (1,075 + 3); DG-L05 |
| `v_ace_*` objects / fields | 30 / 304 | Story §11; all sources agree |
| Section A / Section B fields | 177 / 127 | Story §11; re-counted per view |
| Extension fields | 49, DF-EXT-001..049 | Story §11, AC7 |
| `is_personal` among the 304 DF-ACE fields | 304 non-null; 250 true; 54 false; all 12 Restricted true | Data Classification Inventory v4; RWB-E1-001's protective union (ASM-E1001-14) |
| `is_personal` in the whole dictionary | 526 true (RWB-E1-001's assertion, TC-E1-001-14 only) | ASM-E1001-14; DG-L24 |

**AC6 row** (`v_ace_account` / `days_past_due`): field ID `DF-ACE-018`; data type `NUMBER`; physical type `integer`; source system `ACE`; source field `public.account.delay_days`; data product `DP01`; refresh cycle `DAILY` (Physical Schema v6 line 5843, 3626 and 3518). A synthetic account `ACC0000017` with `delay_days` 95 reads back as `days_past_due` 95.

**One-to-one match**: each `v_ace_*` view has exactly one `sys_objects` row and one `sys_fields` row per catalog column, and every such row has a non-null `is_personal` (conformance check 3).

## 4. Grant matrix

| Role | On the 30 views | On schema `recovery` | On the three helpers | In `public` | Other |
|---|---|---|---|---|---|
| `ace_view_owner` | Owns all 30; no INSERT, UPDATE, DELETE, TRUNCATE, REFERENCES, TRIGGER | No USAGE and no CREATE after each file's last step; no privilege on any other `recovery` relation | No EXECUTE | USAGE and SELECT on the 21 Tier 1 tables (and the 14 Tier 2 with RWB-ACE-001), granted by the ACE DBA (P4(d)); no write | Holds no other right |
| `recovery_svc` | SELECT on each view; no write of any kind | USAGE | EXECUTE on `ace_to_date`, `ace_to_boolean`, `ace_mask_value` | No USAGE, no privilege on any relation | DML on Workbench tables is outside this story (DG-L25) |
| `PUBLIC` | Nothing | — | No EXECUTE | Nothing (ACE DBA's PUBLIC revoke, P4(d)) | `REVOKE ALL ON ALL TABLES IN SCHEMA ${recoverySchema} FROM PUBLIC` is the first step of the Section A file |
| `rwb_migrator` (migration account) | Owns each view only between its creation and the owner change | Owns schema `recovery`, or may grant CREATE on it (P4(c)); no lingering right | Owns the helpers | `USAGE ON SCHEMA public` and **no** table privilege; no CREATE; membership of `ace_view_owner` `WITH INHERIT FALSE, SET TRUE`, ADMIN false; no superuser, createdb, createrole, bypassrls | Never the ACE DBA role; never a table privilege; never an inheriting membership. D-RUN-14, delivered by RWB-E1-044 v14-7's local init; ratification open (OI-069-M, proposed OPEN-051); no human approval claimed |
| `rwb_no_grant` (test fixture role) | No SELECT, no EXECUTE | USAGE only | No EXECUTE | None | Created by the test with LOGIN; proves PUBLIC holds nothing |

**Per-file privilege sequence** (both files): PUBLIC revoke (A only) → helpers (A only) → EXECUTE revoke/grant → USAGE for `recovery_svc` → transient `USAGE, CREATE` for `ace_view_owner` → view creation → per-view REVOKE from PUBLIC, `recovery_svc`, `ace_view_owner` → per-view SELECT grant to `recovery_svc` **before** the owner change → `ALTER VIEW ... OWNER TO ace_view_owner` → final `REVOKE USAGE, CREATE`. The order is not cosmetic: the owner change fails without CREATE, and the SELECT grant fails after it for a non-inheriting member.

## 5. Migration-folder states and history

| State | Files present | `v_ace_*` views | `flyway_schema_history_recovery` | Who reads this state |
|---|---|---|---|---|
| A only | Section A | 16 | one success row for the RWB-E1-001 file, one for Section A, **no** `version = '0'` row | Between the two merges; `ViewConformanceTest` and `MigrationFolderCoverageTest` assert it |
| A + B | both | 30 | one more success row for Section B, after Section A | After RWB-ACE-001 is deployed; the same tests assert it |
| Re-run | unchanged | unchanged | unchanged; `migrationsExecuted = 0` | SPEC-017 |

`sourceViews.sectionB` holds all 14 names from the first merge; rule 3 of SPEC-013 keeps the build green in the A-only state (no file creates a Section B name), so no test is skipped and no list is edited between merges.

## 6. `sourceViews` resource

`backend/src/test/resources/architecture/recovery-modules.yaml`, top-level key. Model records (test scope, `architecture.boundary`):

| Record | Components |
|---|---|
| `SourceViews` | `List<String> sectionA` (16), `List<String> sectionB` (14), `all()` (30 in story order), `contains(String)` |
| `SourceViewsReader` | `parse(ModuleMap)`, `validateAgainstFolder(SourceViews, Path migrationFolder)`; failures are `IllegalStateException` with `{file}: {fieldPath}: {problem}` |

Validation: both lists present; name pattern `^v_ace_[a-z0-9_]+$`; unique across both; counts 16 and 14. Folder rules: rule 1 (every created `v_ace_*` listed), rule 2 (Section A set equals `sectionA`), rule 3 (Section B set equals `sectionB` when present, otherwise no Section B name created), rule 4 (BND-6 allows all 30 in both states). The RWB-TE-001 `ModuleMapLoader` keeps `sourceViews` opaque and is not changed.

## 7. Lint exception resource

`backend/src/test/resources/db/recovery-migration-lint-exceptions.yaml`:

| Field | Value |
|---|---|
| `storyKey` | `rwb_e1_069` |
| `nonFixFiles` | `__rwb_e1_069_ace_source_views.sql`, `__rwb_e1_069_ace_tier2_views.sql` |
| `grantObjects` | `SCHEMA ${recoverySchema}`, `${recoverySchema}.<object>`, `FUNCTION ${recoverySchema}.<fn>(...)`, `ALL TABLES IN SCHEMA ${recoverySchema}` (REVOKE only) |
| `grantees` | `recovery_svc`, `ace_view_owner`, `PUBLIC` |
| `qualifierSeam` | not data: `public` is admitted only inside `CREATE [OR REPLACE] VIEW ${recoverySchema}.v_ace_*` |

`LintExceptions` + `LintExceptionsLoader` read it; the rules read the model, never the file. `LintExceptionsLoaderTest` pins the real resource and the error text.

## 8. BND-6 derived sets and table-to-view map

| Derived value | How it is derived | Example |
|---|---|---|
| ACE source tables | every `public.<name>` qualifier in the two E1-069 files | 35 distinct qualifier names (21 Tier 1 + 14 Tier 2); `hearing` is also a recovery table and is excluded, leaving 34 enforced names |
| Recovery tables | every `CREATE TABLE ... ${recoverySchema}.<name>` in the recovery folder (E1-042, E1-043, E1-001) | `hearing` is excluded from the ACE set because it is also a recovery table |
| Allowed view names | `SourceViews.all()` from the real map | 30 |
| Table-to-view map | the view whose top-level `FROM` names the table; otherwise the views that `JOIN` it | `phone`, `email`, `address` → `v_ace_contact`; `bot_holiday` → `v_ace_holiday`; `bucket_log_snapshot` → `v_ace_bucket_log`; `pod_receipt` → `v_ace_pod`; `hearing` → `v_ace_hearing` |
| Failure text | `Boundary rule BND-6 broken: <SimpleClassName> reads public.<table>. Read recovery.<view> instead.` | `Boundary rule BND-6 broken: AccountReader reads public.account. Read recovery.v_ace_account instead.` |
| Fallback | a table no view reads | `Read a recovery.v_ace_* view instead.` |

## 9. Tier 2 probe stand-in (RWB-ACE-001, Blocker = No)

`infra/postgres/schema/02-ace-tier2-probe.sql` creates the 14 tables and the 12 columns. `RWB_ACE_TIER2_PROBE=true` (default) loads it; `TASK-15` adds the SELECT stand-in for `ace_view_owner` on the 14 tables in the Flyway-mode branch of `20-grants.sql.inc`.

| Probe object | Section B view | Used by the test |
|---|---|---|
| `public.ace_batch_run` | `v_ace_batch_status` | probe-off X2 first failure names this relation |
| `public.valuation` | `v_ace_valuation` | X2 main case drops it |
| `public.collateral_detail` | `v_ace_collateral_detail` | 30-view read |
| `public.npa_asset` | `v_ace_npa_asset` | 30-view read |
| `public.npa_sale` | `v_ace_npa_sale` | 30-view read |
| `public.lawsuit` | `v_ace_lawsuit` | 30-view read |
| `public.hearing` | `v_ace_hearing` | 30-view read; also a recovery table name, excluded from the ACE set |
| `public.pod_receipt` | `v_ace_pod` | 30-view read |
| `public.gl_write_off` | `v_ace_write_off` | 30-view read |
| `public.collins_score` | `v_ace_score` | 30-view read |
| `public.party_product` | `v_ace_party_product` | 30-view read |
| `public.credit_decision` | `v_ace_credit_decision` | 30-view read |
| `public.esign_request` | `v_ace_esign` | 30-view read |
| `public.iam_group` | `v_ace_iam_group` | 30-view read |
| 12 columns on `account`, `customer`, `efs_action` | none | not in any Section A view; the mapping is RWB-ACE-001 Appendix A and is not carried (DG-L07, OI-069-B) |

In the ACE target the probe is not deployed; Section B merges only after RWB-ACE-001 is deployed in every environment `main` deploys to (DG-L16, DG-L20, OI-069-D). The probe is local evidence only, never a replacement of the dependency.

## 10. Test data and fixtures (all synthetic)

| Value | Use | Synthetic |
|---|---|---|
| `ACC0000017` with `delay_days` 95 | AC6 read through `v_ace_account` | Yes |
| `P0000123` | AC7 duplicate `party_ext` row (23505) | Yes |
| `X000000005678` | AC6 and SPEC-019 mask check: `id_no_masked` `*********5678`, `id_no_last4` `5678` | Yes |
| `public.payment` rows with `pay_date` `2026-02-28`, `2026-02-30`, `20261345`, `31/02/2026`, `garbage`, NULL | SPEC-020 through the view; the first gives 2026-02-28, the others NULL | Yes |
| `rwb_no_grant` role | AC2.6 | Yes |
| `fk_case_account_account_key` to `public.account` | AC4.2 and check 2 fixture | Synthetic DDL |
| copy of `v_ace_account` with column `legacy_bucket` | AC5.5 and check 3 fixture | Synthetic DDL |
| `GRANT INSERT ON ${recoverySchema}.v_ace_account TO recovery_svc` | check 4 fixture | Synthetic grant |
| a view over a dropped synthetic column | check 1 fixture | Synthetic DDL |
| `it-migrator`, `it-recovery`, `it-temporal` | container passwords | Synthetic |

The whole-dictionary `is_personal` count of 526 is never asserted here; E1-069 asserts only the 304 DF-ACE rows (304 non-null, 250 true, 54 false). No real name, ID number, account number or address appears in any fixture, migration, log line or plan file.

## 11. Conformance target inputs (ASM-004)

| Input | Read when | Used for |
|---|---|---|
| `RWB_CONFORMANCE_TARGET=external` | always; absence means Testcontainers | Selects external mode |
| `RWB_DB_URL`, `RWB_DB_USER`, `RECOVERY_SVC_PASSWORD` | external only | check 1 (service identity) |
| `RWB_MIGRATOR_USER`, `RWB_MIGRATOR_PASSWORD` | external only | checks 2-4 (catalog and migration-account facts) |

No credential is written in code, a fixture, a log line or this plan. External mode runs checks 1-4 only: read-only, no fixture, no write, no check 5. The Testcontainers run executes checks 1-5 and the fixtures.
