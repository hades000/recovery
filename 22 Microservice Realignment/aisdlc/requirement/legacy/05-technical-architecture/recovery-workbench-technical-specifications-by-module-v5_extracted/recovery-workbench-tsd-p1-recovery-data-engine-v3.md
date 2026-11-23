<!-- source: 05 Technical architecture/Recovery Workbench Technical Specifications by Module v5.zip!Recovery Workbench TSD P1 Recovery data engine v3.md -->
<!-- converted: 2026-11-16 from Markdown (extracted) -->

> **Source:** `05 Technical architecture/Recovery Workbench Technical Specifications by Module v5.zip!Recovery Workbench TSD P1 Recovery data engine v3.md`  
> **Converted from:** Markdown (extracted)

# Recovery Workbench P1 Recovery data engine

Technical specification. SCB Collections and Recovery. Henka Group, 15 November 2026.

(C) Siam Commercial Bank and Henka Pte Ltd

## Document control

| Attribute | Value |
|---|---|
| Document title | TSD P1 Recovery data engine |
| Document ID | P1-RWB-TSD-v3 |
| Version | 3 |
| Status | In review |
| Date | 15 November 2026 |
| TSD owner | Solution architect |
| Build squad | TechX recovery squads |
| Change note | D-RCV-35 (U1 to U5): the Workbench takes no inbound source data. P1 reads ACE only through `recovery.v_ace_*` views, owns 4 extension tables, and keeps the freshness stamp, catalog, dictionary, contracts, case list, reconciliation, lake copy, retention and DP04 copies. Supersedes version 2 of 28 October 2026 |

| Document | Type | Relationship |
|---|---|---|
| Recovery Workbench FSD P1 Recovery data engine | FSD | Pair |
| Recovery Workbench Target Architecture | Architecture | Parent |
| Recovery Workbench Physical Schema v5.sql | Data | Source of T3; authoritative for tables, views and dictionary counts |
| Recovery Workbench Logical Data Model and Data Dictionary v7 | Data | Source of T3 field definitions |
| Recovery Workbench ACE Data Tier Map v1 | Data | Frozen tier map and boundary rule |
| Recovery Workbench ACE Source Views v1.sql | Data | View definitions, grants and conformance test |
| Recovery Workbench ACE DB Alignment Change Register v1 | Governance | Decision record for D-RCV-35 |
| Recovery Workbench ACE Team Stories v1 (RWB-ACE-001) | Story | ACE tables and columns the Section B views read |
| Recovery Workbench Event and Messaging Design v3 | Architecture | Source of T5.3 (EV-26, EV-27) |
| Recovery Workbench Batch and Scheduling Design v3 | Architecture | Jobs P1 runs or triggers |
| Recovery Workbench Interface Specifications v3 | Architecture | Source of T5.1 |
| Recovery Workbench API Specification | API | Source of appendix T-A |

### Changes in version 3

| Area | Change |
|---|---|
| Scope | Loads, load checks, data quality rules, source field and code maps and the tracker estate leave P1. ACE ingests every source (U1); the Workbench reads the result |
| T3 data model | 15 objects removed (T3.9). 30 `v_ace_*` views added in two migrations (T3.3, T3.4). 4 extension tables added (T3.5). 13 Workbench tables kept and checked against Physical Schema v5 (T3.6) |
| Keys | `case_list_row.account_id` (uuid, FK to `loan_account`) becomes `account_key` (varchar(255), no FK) |
| T5 | Inbound interfaces are ACE ingestion, not P1 interfaces. LoadCompleted and LoadRefused give way to AceDataReady and AceDataLate |
| T6 | Database grants added: SELECT on the views only |
| Appendix T-A | Tracker endpoints API-P1-004 to 008 retired. API-P1-003 changes from data quality exceptions to reconciliation results. Job, freshness, catalog, dictionary and contract endpoints re-worded |

## Existing capability check

| Capability | Verdict | Owning document | Note |
|---|---|---|---|
| Source data, ingestion and ingestion checks | REUSE | ACE ingestion; RWB-ACE-001 | Every source lands in the ACE database. P1 runs no ingestion check and reads the outcome from `v_ace_batch_status` |
| Read path into ACE | NEW, owned by P1 | ACE Source Views v1.sql; RWB-E1-069 | `recovery.v_ace_*` SELECT-only views. The only read path into ACE |
| Sign-in, access check, audit, PII and SOC logging | REUSE | ACE common module | Called through the published interface |
| Scheduler and batch | REUSE | ACE pattern: Quartz and Spring Batch | Jobs in the Batch and Scheduling Design v3. No new `qrtz_` or `batch_` table |
| Holiday calendar | REUSE | ACE `bot_holiday` | Read through `v_ace_holiday` |
| Outbox and retry | REUSE | Error Handling and Resilience Standard | Through P2 |
| Rules evaluation | REUSE | Rules Engine Design | Through the rules component |

## T1. Architecture overview

P1 Recovery data engine is part of the recovery module in the ACE service: one service, one repository, one front end. It covers:

- the read path into ACE: the 30 `recovery.v_ace_*` views, their grants and the conformance test;
- the 4 extension tables that hold Workbench decisions about ACE records;
- freshness: the stamp of each data product, taken from the ACE batch record;
- the daily case list and its reconciliation to `v_ace_account`;
- the data catalog, data dictionary and data contracts;
- the decision log copy to the data lake, retention rules and the DP04 business-date copies.

P1 loads nothing, copies no source record and transforms no source feed. It reaches other modules only through their published interfaces. It reaches ACE data only through `recovery.v_ace_*`, and other systems only through the outbound data lake extract (INT-19).

### T1.1 Boundary rule

| Rule | Detail |
|---|---|
| One read path | The recovery module reads ACE only through `recovery.v_ace_*` views. A direct `public.*` read in code, a query, a story or a specification is a defect |
| Read only | The views are SELECT only. The recovery schema never writes to `public` |
| No foreign key into ACE | No constraint in schema `recovery` references a table in `public`. ACE uses `ON DELETE CASCADE` on `account`, and a cascade must never reach Workbench case history |
| Business keys | Links to an ACE record are `varchar(255)` business-key columns (`account_key`, `person_key`, `contact_key`, `asset_key`, `valuation_key`, `payment_code`). They carry no foreign key. Integrity is checked by the read model and by reconciliation REC-05 |
| No copy | A Workbench table never holds a column ACE already holds. A snapshot taken at a point in time is allowed only where named (`_at_entry`, the DP04 business-date copies) |
| Enforced by the catalog | The recovery service identity holds SELECT on the views and on nothing in `public` (T6.3), so a direct read fails at the database, not only in review |

## T2. Component design

| Component | Responsibility |
|---|---|
| RecoveryDataEngineController | REST endpoints in appendix T-A; validation; maps errors to problem responses |
| RecoveryDataEngineService | Business logic; calls the rules component; writes the decision log entry before any change |
| RecoveryDataEngineRepository | Reads and writes the module's own tables (T3.5, T3.6) only |
| AceSourceReadRepository | SELECT only on `recovery.v_ace_*`, one read method per view. Names no `public` table. Other recovery modules read ACE data through this repository's published interface |
| AceBatchStatusWatcher | Reads `v_ace_batch_status` per source and business date. On COMPLETED it writes the `data_product_load` stamp and delivers AceDataReady (EV-26). When the source cut-off passes first, it marks the product STALE and publishes AceDataLate (EV-27) |
| Jobs | Case list build and publish (E1-002), JOB-04 daily reconciliation, JOB-13 decision log copy. All start on the ACE batch-complete record or on their schedule. JOB-01 and JOB-09 are retired under D-RCV-35 |
| View migrations | Section A and Section B Flyway migrations (T3.2) and the view conformance test (T6.3) |
| Published interface | Java interface other modules call: freshness, the ACE read methods and the dictionary. No table is read across modules |

## T3. Data model

### T3.0 Standard record columns

Every Workbench table, extension tables included, carries these columns. Views do not.

| Column | Type | Meaning |
|---|---|---|
| is_active | boolean | The active or inactive status of the record |
| state | varchar(40) | Record lifecycle state |
| version | integer | Optimistic lock version |
| created_at | timestamptz | When the record was created |
| created_by | uuid | Who or which service identity created it |
| updated_at | timestamptz | When the record last changed |
| updated_by | uuid | Who or which service identity last changed it |

### T3.1 Data tiers

ACE holds the data, the Workbench holds the case, and a view joins them.

| Tier | Owner | What it holds | In this TSD |
|---|---|---|---|
| 1 | ACE team, read only | ACE tables that exist today. Read through a view, never altered | 16 Section A views (T3.3, T3.4) |
| 2 | ACE team | New ACE tables and columns raised in RWB-ACE-001: 14 tables, 12 columns | 14 Section B views (T3.3, T3.4) |
| 3 | Workbench | 1:1 extension tables keyed by ACE business keys | 4 tables (T3.5) |
| 4 | Workbench | Case, workflow, treatment and the other Workbench tables | 13 P1 tables (T3.6). The rest are owned by other TSDs |

Counts in Physical Schema v5: 92 tables, 30 views, 122 `sys_objects` rows (92 + 30) and 1,366 `sys_fields` rows (D-RCV-35 amending D-RCV-29). No foreign key into `public.*`. No UUID foreign key into a source copy.

### T3.2 Migrations: the two-migration rule

A view cannot be created over a table that does not exist yet, so the views ship in two parts.

| Migration | Contains | Fields | Ships | Until it ships |
|---|---|---:|---|---|
| V0001 baseline | 92 tables, the dictionary seed, `v_data_dictionary` | - | First release | - |
| Section A (proposed V0002, next free sequence at merge) | Helper functions `ace_to_date`, `ace_to_boolean`, `ace_mask_value`; 16 views over ACE tables that exist today | 177 | With RWB-E1-069 | - |
| Section B (proposed V0003, next free sequence after RWB-ACE-001) | 14 views over the Tier 2 tables | 127 | The week RWB-ACE-001 is deployed (DL43) | Features that read a Section B view stay behind their feature flag; the freshness stamp falls back to STALE for every product (T3.7) |

Helper functions:

| Function | Returns | Rule |
|---|---|---|
| `recovery.ace_to_date(text)` | date | Accepts ISO, YYYYMMDD and DD/MM/YYYY. Returns NULL on any other value, so a dirty ACE row never breaks a read |
| `recovery.ace_to_boolean(text)` | boolean | ACE Y/N text flags to boolean |
| `recovery.ace_mask_value(text)` | text | PDPA display mask: last four characters, or first character and domain of an email address |

### T3.3 Source views: inventory

Field IDs are the `sys_fields` rows in Physical Schema v5. Every view field is read only, and its source system is ACE.

| # | View | Section | ACE object | Key the Workbench links on | Fields | Field IDs | Replaces or serves |
|---:|---|---|---|---|---:|---|---|
| 1 | `v_ace_account` | A | `account`, with `product`, `branch` | `account_key` | 42 | DF-ACE-001 to 042 | Replaces `loan_account` |
| 2 | `v_ace_payment` | A | `payment`, with `account` | `payment_code`, `account_key` | 12 | DF-ACE-043 to 054 | Replaces `account_payment` |
| 3 | `v_ace_customer` | A | `customer` | `person_key` (`cif_no`) | 20 | DF-ACE-055 to 074 | Replaces `party` (with `party_ext`) |
| 4 | `v_ace_contact` | A | `phone`, `email`, `address` (union) | `contact_key` (`contact_type:key`) | 9 | DF-ACE-075 to 083 | Replaces `contact_point` (with `contact_point_ext`) |
| 5 | `v_ace_ca_relation` | A | `ca_relation` | `person_key`, `account_key` | 5 | DF-ACE-084 to 088 | Borrower, guarantor and co-borrower roles |
| 6 | `v_ace_aa_relation` | A | `aa_relation` | `parent_account_key`, `child_account_key` | 2 | DF-ACE-089 to 090 | Facility grouping |
| 7 | `v_ace_collateral` | A | `collateral`, with `asset` | `asset_key`, `account_key` | 8 | DF-ACE-091 to 098 | Replaces `collateral` and `account_collateral` (with `v_ace_collateral_detail`) |
| 8 | `v_ace_asset` | A | `asset` | `asset_key` | 9 | DF-ACE-099 to 107 | Collateral asset and held asset |
| 9 | `v_ace_efs_action` | A | `efs_action` | `efs_record_key`, `account_key` | 20 | DF-ACE-108 to 127 | Replaces `collections_history` |
| 10 | `v_ace_efs_action_code` | A | `efs_action_code` | `action_code` | 3 | DF-ACE-128 to 130 | LOV-ACTION-CODE (1,106 values) |
| 11 | `v_ace_efs_assignment` | A | `efs_assignment` | `account_key` | 9 | DF-ACE-131 to 139 | Hand-over and agency history |
| 12 | `v_ace_bucket_log` | A | `bucket_log_snapshot`, with `account` | `account_key`, year, month | 6 | DF-ACE-140 to 145 | Month-end bucket history |
| 13 | `v_ace_product` | A | `product` | `product_code` | 5 | DF-ACE-146 to 150 | Product and product group lists |
| 14 | `v_ace_branch` | A | `branch` | `branch_code` | 4 | DF-ACE-151 to 154 | Branch and region lists |
| 15 | `v_ace_holiday` | A | `bot_holiday` | `holiday_date` | 5 | DF-ACE-155 to 159 | Service level and legal-day calendar (E1-043, E1-045) |
| 16 | `v_ace_plan` | A | `ace_case`, `cfsc_mg_ssme_tdr_case`, `tdr_calculation`, `ai_recommended_plan` | `plan_ref`, `account_key` | 18 | DF-ACE-160 to 177 | Restructure plan reference and status |
| 17 | `v_ace_batch_status` | B | `ace_batch_run` | `source_system`, `business_date` | 9 | DF-ACE-178 to 186 | Freshness stamp and the data-job trigger; replaces `load_run` as the record of a completed feed |
| 18 | `v_ace_valuation` | B | `valuation` | `valuation_key` | 9 | DF-ACE-187 to 195 | SVAF appraisal (with `valuation_ext`) |
| 19 | `v_ace_collateral_detail` | B | `collateral_detail` | `asset_key` | 12 | DF-ACE-196 to 207 | CCMS title, location, insurance and lien rank |
| 20 | `v_ace_npa_asset` | B | `npa_asset` | `asset_key` | 12 | DF-ACE-208 to 219 | AMIS and RPS held asset |
| 21 | `v_ace_npa_sale` | B | `npa_sale` | `npa_sale_key` | 11 | DF-ACE-220 to 230 | AMIS sale, taxes and fees |
| 22 | `v_ace_lawsuit` | B | `lawsuit` | `lawsuit_key`, `account_key` | 13 | DF-ACE-231 to 243 | LIT lawsuit |
| 23 | `v_ace_hearing` | B | `hearing` | `hearing_key`, `lawsuit_key` | 7 | DF-ACE-244 to 250 | LIT hearing |
| 24 | `v_ace_pod` | B | `pod_receipt` | `pod_key`, `account_key` | 10 | DF-ACE-251 to 260 | WIN proof of delivery |
| 25 | `v_ace_write_off` | B | `gl_write_off` | `write_off_key`, `account_key` | 9 | DF-ACE-261 to 269 | GL write-off posting |
| 26 | `v_ace_score` | B | `collins_score` | `score_key`, `account_key` | 10 | DF-ACE-270 to 279 | Replaces `score` |
| 27 | `v_ace_party_product` | B | `party_product` | `person_key`, `account_key` | 6 | DF-ACE-280 to 285 | Replaces `party_product` |
| 28 | `v_ace_credit_decision` | B | `credit_decision` | `credit_decision_key`, `account_key` | 8 | DF-ACE-286 to 293 | NLEADS credit result |
| 29 | `v_ace_esign` | B | `esign_request` | `esign_key`, `account_key` | 7 | DF-ACE-294 to 300 | EasyApp signature reference |
| 30 | `v_ace_iam_group` | B | `iam_group` | `entra_group`, `role_code` | 4 | DF-ACE-301 to 304 | Entra ID group to role |
| | **Total** | | | | **304** | | Section A 177, Section B 127 |

Column lists of the views not detailed in T3.4:

| View | Fields |
|---|---|
| `v_ace_ca_relation` | person_key, account_key, relation_type, amount_of_guarantee, date_of_guarantee |
| `v_ace_aa_relation` | parent_account_key, child_account_key |
| `v_ace_asset` | asset_ref, asset_key, asset_type, description, address, town, post_code, county, country |
| `v_ace_efs_action_code` | action_code, action_name, category |
| `v_ace_efs_assignment` | account_key, assignment_scheme, assignee_code, assignee_name, assignment_start_date, assignment_end_date, assignment_start_total_balance, assignment_end_total_balance, distribution_area |
| `v_ace_bucket_log` | account_key, snapshot_year, snapshot_month, bucket, past_due_amount, snapshot_month_start |
| `v_ace_product` | product_code, product_name, product_type, product_category, product_category_efs |
| `v_ace_branch` | branch_code, branch_name, address, phone |
| `v_ace_holiday` | holiday_date, holiday_year, holiday_name, holiday_name_thai, holiday_weekday |
| `v_ace_plan` | plan_ref, ace_case_id, plan_status, plan_created_at, tdr_calculation_id, plan_published_at, associated_account_id, account_key, booked_at, approved_at, submitted_at, closed_at, closed_reason, ca_approved_at, installments, recommended_installment, recommended_package, plan_status_as_of |
| `v_ace_valuation` | valuation_key, asset_key, appraisal_no, appraisal_type, appraised_value, forced_sale_value, appraisal_date, source_system, data_as_of |
| `v_ace_npa_asset` | asset_ref, asset_key, asset_code, transfer_in_type, from_segment, transfer_in_date, book_value, auction_purchase_price, repossessed_date, stock_date, source_system, data_as_of |
| `v_ace_npa_sale` | npa_sale_key, npa_asset_key, contract_date, sale_date, sale_price, transfer_fee, specific_business_tax, corporate_income_tax, incentive_amount, source_system, data_as_of |
| `v_ace_lawsuit` | lawsuit_key, account_key, lawsuit_no, black_case_no, red_case_no, court_name, claim_amount, filed_date, judgment_date, judgment_amount, lit_status, source_system, data_as_of |
| `v_ace_hearing` | hearing_key, lawsuit_key, hearing_date, hearing_type, next_date, source_system, data_as_of |
| `v_ace_pod` | pod_key, account_key, notice_ref, sent_date, barcode, callback_date, delivery_status, sent_type, source_system, data_as_of |
| `v_ace_write_off` | write_off_key, account_key, amount, posted_date, responsibility_center, cost_center, gl_product, source_system, data_as_of |
| `v_ace_party_product` | person_key, account_no, account_key, product_type, product_status, data_as_of |
| `v_ace_credit_decision` | credit_decision_key, account_key, nleads_ref, credit_result, credit_result_reason, decided_at, source_system, data_as_of |
| `v_ace_esign` | esign_key, account_key, external_ref, requested_at, status, source_system, data_as_of |
| `v_ace_iam_group` | entra_group, role_code, source_system, data_as_of |

Every Section B view carries `source_system` and `data_as_of` (from the Tier 2 `business_date`), so each row shows where it came from and how old it is.

### T3.4 Source views: field definitions

The views that replace a version 2 object, and the batch view P1 reads for freshness. Physical type is the type the view returns. Required is No for every view field, because a view carries no constraint. Source is the ACE column in `public`.

**v_ace_account** (Section A, Tier 1). The ACE account as the Workbench reads it, with product, branch and the ACE batch date. Replaces `loan_account`.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-ACE-001 | account_key | TEXT | varchar(255) | No | None | ACE account.account_key |
| DF-ACE-002 | account_code | TEXT | varchar(255) | No | None | ACE account.account_code |
| DF-ACE-003 | account_name | TEXT | varchar(255) | No | None | ACE account.account_name |
| DF-ACE-004 | account_status | TEXT | varchar(255) | No | None | ACE account.account_status |
| DF-ACE-005 | account_status_date | DATE | date | No | None | ACE account.account_status_date |
| DF-ACE-006 | contract_no | TEXT | varchar(255) | No | None | ACE account.contract_number |
| DF-ACE-007 | contract_date | DATE | date | No | None | ACE account.contract_date |
| DF-ACE-008 | product_key | TEXT | varchar(255) | No | None | ACE account.product_key |
| DF-ACE-009 | product_type | TEXT | varchar(255) | No | None | ACE product.product_type |
| DF-ACE-010 | product_category | TEXT | varchar(255) | No | None | ACE product.product_category |
| DF-ACE-011 | product_category_efs | TEXT | varchar(255) | No | None | ACE product.product_category_efs |
| DF-ACE-012 | branch_code | TEXT | varchar(255) | No | None | ACE account.current_branch |
| DF-ACE-013 | branch_name | TEXT | varchar(255) | No | None | ACE branch.branch_name |
| DF-ACE-014 | oc_code | TEXT | varchar(255) | No | None | ACE account.oc_code |
| DF-ACE-015 | company_code | TEXT | varchar(255) | No | None | ACE account.company_code |
| DF-ACE-016 | collection_officer | TEXT | varchar(255) | No | None | ACE account.collection_officer |
| DF-ACE-017 | collection_phase | TEXT | varchar(255) | No | None | ACE account.collection_phase |
| DF-ACE-018 | days_past_due | NUMBER | integer | No | None | ACE account.delay_days |
| DF-ACE-019 | classification | TEXT | varchar(255) | No | None | ACE account.loan_classification |
| DF-ACE-020 | total_balance | NUMBER | numeric(38,2) | No | None | ACE account.total_balance |
| DF-ACE-021 | accounting_balance | NUMBER | numeric(38,2) | No | None | ACE account.accounting_balance |
| DF-ACE-022 | past_due_amount | NUMBER | numeric(38,2) | No | None | ACE account.past_due_amount |
| DF-ACE-023 | total_interest_fin_charge | NUMBER | numeric(38,2) | No | None | ACE account.total_interest_fin_charge |
| DF-ACE-024 | collections_fee | NUMBER | numeric(38,2) | No | None | ACE account.collections_fee |
| DF-ACE-025 | interest_rate | NUMBER | numeric(7,4) | No | None | ACE account.interest_rate |
| DF-ACE-026 | last_payment_date | DATE | date | No | None | ACE account.last_payment_date |
| DF-ACE-027 | last_payment_amount | NUMBER | numeric(38,2) | No | None | ACE account.last_payment_amount |
| DF-ACE-028 | next_installment_date | DATE | date | No | None | ACE account.next_installment_date |
| DF-ACE-029 | next_installment_amount | NUMBER | numeric(38,2) | No | None | ACE account.next_installment_amount |
| DF-ACE-030 | last_tdr_date | DATE | date | No | None | ACE account.last_tdr_date |
| DF-ACE-031 | tdr_flag | BOOLEAN | boolean | No | None | ACE account.is_restructured, through `ace_to_boolean` |
| DF-ACE-032 | rescheduled_flag | BOOLEAN | boolean | No | None | ACE account.is_rescheduled, through `ace_to_boolean` |
| DF-ACE-033 | number_reschedules | NUMBER | integer | No | None | ACE account.number_reschedules |
| DF-ACE-034 | tdr_aging | NUMBER | integer | No | None | ACE account.tdr_aging |
| DF-ACE-035 | principle_not_reduce | TEXT | varchar(255) | No | None | ACE account.principle_not_reduce |
| DF-ACE-036 | data_as_of | DATE | date | No | None | ACE account.core_banking_system_date |
| DF-ACE-037 | days_since_last_contact | NUMBER | integer | No | None | ACE account.days_since_last_contact |
| DF-ACE-038 | days_since_last_collection_activity | NUMBER | integer | No | None | ACE account.days_since_last_collection_activity |
| DF-ACE-039 | relationship_manager | TEXT | varchar(255) | No | None | ACE account.rm_name |
| DF-ACE-040 | relationship_manager_phone | TEXT | varchar(255) | No | None | ACE account.rm_phone_number |
| DF-ACE-041 | special_memo | TEXT | varchar(255) | No | None | ACE account.special_memo |
| DF-ACE-042 | expiry_date | DATE | date | No | None | ACE account.expiry_date |

`dispute_open` (DF-ACC-029 in version 2) moves to `account_ext`. The 7 ALS columns ACE adds to `account` in RWB-ACE-001 (`business_unit`, `principal_outstanding`, `interest_outstanding`, `fees_outstanding`, `daily_bucket`, `settlement_booked_date`, `settlement_booked_amount`) are not yet in this view. See T3.10, point 1.

**v_ace_payment** (Section A, Tier 1). A payment posted to an ACE account. Replaces `account_payment`.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-ACE-043 | payment_code | TEXT | varchar(255) | No | None | ACE payment.pay_key |
| DF-ACE-044 | account_key | TEXT | varchar(255) | No | None | ACE payment.account_key |
| DF-ACE-045 | payment_date | DATE | date | No | None | ACE payment.pay_date (varchar), through `ace_to_date` |
| DF-ACE-046 | payment_amount | NUMBER | numeric(19,2) | No | None | ACE payment.total_amount |
| DF-ACE-047 | capital_amount | TEXT | varchar(255) | No | None | ACE payment.capital_amount |
| DF-ACE-048 | interest_amount | TEXT | varchar(255) | No | None | ACE payment.payinterest |
| DF-ACE-049 | expense_amount | TEXT | varchar(255) | No | None | ACE payment.payexpenses |
| DF-ACE-050 | commission_amount | TEXT | varchar(255) | No | None | ACE payment.paycommission |
| DF-ACE-051 | payment_channel | TEXT | varchar(255) | No | None | ACE payment.pay_type |
| DF-ACE-052 | description | TEXT | varchar(255) | No | None | ACE payment.description |
| DF-ACE-053 | comments | TEXT | varchar(255) | No | None | ACE payment.comments |
| DF-ACE-054 | data_as_of | DATE | date | No | None | ACE account.core_banking_system_date |

**v_ace_customer** (Section A, Tier 1). An ACE customer. The identity number is never exposed in clear. Replaces `party`, with `party_ext`.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-ACE-055 | cif_no | TEXT | varchar(255) | No | None | ACE customer.person_key |
| DF-ACE-056 | person_key | TEXT | varchar(255) | No | None | ACE customer.person_key |
| DF-ACE-057 | first_name | TEXT | varchar(255) | No | None | ACE customer.first_name |
| DF-ACE-058 | last_name | TEXT | varchar(255) | No | None | ACE customer.surname |
| DF-ACE-059 | date_of_birth | DATE | date | No | None | ACE customer.birth_date |
| DF-ACE-060 | deceased_date | DATE | date | No | None | ACE customer.deceased_date |
| DF-ACE-061 | deceased_flag | BOOLEAN | boolean | No | None | ACE customer.is_deceased, through `ace_to_boolean` |
| DF-ACE-062 | gender | TEXT | varchar(255) | No | None | ACE customer.gender |
| DF-ACE-063 | nationality | TEXT | varchar(255) | No | None | ACE customer.nationality |
| DF-ACE-064 | marital_status | TEXT | varchar(255) | No | None | ACE customer.marital_status |
| DF-ACE-065 | occupation | TEXT | varchar(255) | No | None | ACE customer.occupation |
| DF-ACE-066 | spouse_name | TEXT | varchar(255) | No | None | ACE customer.spouse_name |
| DF-ACE-067 | customer_status | TEXT | varchar(255) | No | None | ACE customer.status |
| DF-ACE-068 | category | TEXT | varchar(255) | No | None | ACE customer.category |
| DF-ACE-069 | country_of_residence | TEXT | varchar(255) | No | None | ACE customer.country_of_residence |
| DF-ACE-070 | is_staff | BOOLEAN | boolean | No | None | ACE customer.is_staff, through `ace_to_boolean` |
| DF-ACE-071 | branch_code | TEXT | varchar(255) | No | None | ACE customer.branch |
| DF-ACE-072 | vat_number | TEXT | varchar(255) | No | None | ACE customer.vat_number |
| DF-ACE-073 | id_no_masked | TEXT | text | No | None | ACE customer.identification_number, through `ace_mask_value` |
| DF-ACE-074 | id_no_last4 | TEXT | text | No | None | ACE customer.identification_number, last four characters |

`id_no_token` (tokenization at load) is removed: there is no load. Role masking at the API (E1-037) replaces it. `party_type`, `id_type` and `segment` are the 3 SCBPDM columns ACE adds to `customer` in RWB-ACE-001; see T3.10, point 1. The Workbench flags move to `party_ext`.

**v_ace_contact** (Section A, Tier 1). ACE phone, email and address in one view, with a type discriminator and a display mask. Replaces `contact_point`, with `contact_point_ext`.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-ACE-075 | contact_type | LOV | varchar(10) | No | PHONE, EMAIL, ADDRESS | Constant per union branch |
| DF-ACE-076 | contact_key | TEXT | varchar(255) | No | None | `contact_type` + ':' + ACE phone_key, email_key or address_key |
| DF-ACE-077 | person_key | TEXT | varchar(255) | No | None | ACE phone, email or address.person_key |
| DF-ACE-078 | contact_value | TEXT | varchar(256) | No | None | ACE phone.phone_number, email.email or address.address |
| DF-ACE-079 | contact_value_masked | TEXT | text | No | None | Same value, through `ace_mask_value` |
| DF-ACE-080 | usage_code | TEXT | varchar(255) | No | None | ACE phone.contact_usage; NULL for email and address |
| DF-ACE-081 | city | TEXT | varchar(255) | No | None | ACE address.city |
| DF-ACE-082 | post_code | TEXT | varchar(20) | No | None | ACE address.zip_code |
| DF-ACE-083 | country | TEXT | varchar(255) | No | None | ACE address.country |

The full `contact_value` is exposed because notices and calls need it. Display masking is E1-037 at the API, and every read is audited.

**v_ace_collateral** (Section A, Tier 1). The ACE collateral link and the asset behind it, one row per account, collateral and asset. With `v_ace_collateral_detail`, replaces `collateral` and `account_collateral`.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-ACE-091 | collateral_no | TEXT | varchar(255) | No | None | ACE collateral.asset_key |
| DF-ACE-092 | asset_key | TEXT | varchar(255) | No | None | ACE collateral.asset_key |
| DF-ACE-093 | account_key | TEXT | varchar(255) | No | None | ACE collateral.account_key |
| DF-ACE-094 | collateral_value | NUMBER | numeric(19,2) | No | None | ACE collateral.collateral_value |
| DF-ACE-095 | register_date | DATE | date | No | None | ACE collateral.register_date |
| DF-ACE-096 | in_active | BOOLEAN | boolean | No | None | ACE collateral.in_active |
| DF-ACE-097 | collateral_type | TEXT | varchar(255) | No | None | ACE asset.asset_type |
| DF-ACE-098 | description | TEXT | varchar(1000) | No | None | ACE asset.description |

**v_ace_collateral_detail** (Section B, Tier 2). CCMS collateral detail as ingested into ACE.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-ACE-196 | asset_key | TEXT | varchar(255) | No | None | ACE collateral_detail.asset_key |
| DF-ACE-197 | title_doc_no | TEXT | varchar(40) | No | None | ACE collateral_detail.title_doc_no |
| DF-ACE-198 | plot_no | TEXT | varchar(20) | No | None | ACE collateral_detail.plot_no |
| DF-ACE-199 | area_text | TEXT | varchar(20) | No | None | ACE collateral_detail.area_text |
| DF-ACE-200 | province | TEXT | varchar(40) | No | None | ACE collateral_detail.province |
| DF-ACE-201 | district | TEXT | varchar(60) | No | None | ACE collateral_detail.district |
| DF-ACE-202 | subdistrict | TEXT | varchar(60) | No | None | ACE collateral_detail.subdistrict |
| DF-ACE-203 | insured_value | NUMBER | numeric(18,2) | No | None | ACE collateral_detail.insured_value |
| DF-ACE-204 | insurance_expiry | DATE | date | No | None | ACE collateral_detail.insurance_expiry |
| DF-ACE-205 | lien_rank | NUMBER | integer | No | None | ACE collateral_detail.lien_rank |
| DF-ACE-206 | source_system | TEXT | varchar(20) | No | None | ACE collateral_detail.source_system |
| DF-ACE-207 | data_as_of | DATE | date | No | None | ACE collateral_detail.business_date |

`occupancy` and `encumbrance_status` (DF-COL-010, DF-COL-011, Workbench-entered in version 2) are not carried by any ACE table or extension table in Physical Schema v5. See T3.10, point 7.

**v_ace_efs_action** (Section A, Tier 1). The EFS action log ACE already ingests. Replaces `collections_history`.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-ACE-108 | efs_record_key | TEXT | varchar(255) | No | None | ACE efs_action.action_id |
| DF-ACE-109 | account_key | TEXT | varchar(255) | No | None | ACE efs_action.account_key |
| DF-ACE-110 | person_key | TEXT | varchar(255) | No | None | ACE efs_action.customer_key |
| DF-ACE-111 | action_code | LOV | varchar(255) | No | LOV-ACTION-CODE | ACE efs_action.action_code |
| DF-ACE-112 | action_code_name | TEXT | varchar(255) | No | None | ACE efs_action.action_code_name |
| DF-ACE-113 | action_date | DATE | date | No | None | ACE efs_action.action_date |
| DF-ACE-114 | contact_at | DATE | timestamp(6) | No | None | ACE efs_action.action_timestamp |
| DF-ACE-115 | user_code | TEXT | varchar(255) | No | None | ACE efs_action.user_code |
| DF-ACE-116 | comments | TEXT | varchar(2000) | No | None | ACE efs_action.comments |
| DF-ACE-117 | is_call | BOOLEAN | boolean | No | None | ACE efs_action.is_call |
| DF-ACE-118 | is_rpc | BOOLEAN | boolean | No | None | ACE efs_action.is_rpc |
| DF-ACE-119 | is_ptp | BOOLEAN | boolean | No | None | ACE efs_action.is_ptp |
| DF-ACE-120 | promise_status | TEXT | varchar(100) | No | None | ACE efs_action.promise_status |
| DF-ACE-121 | promise_eval_status | TEXT | varchar(100) | No | None | ACE efs_action.promise_eval_status |
| DF-ACE-122 | promise_date | DATE | date | No | None | ACE efs_action.settlement_due_date |
| DF-ACE-123 | promise_amount | NUMBER | numeric(19,2) | No | None | ACE efs_action.settle_total_amount |
| DF-ACE-124 | collection_phase | TEXT | varchar(100) | No | None | ACE efs_action.collection_phase |
| DF-ACE-125 | act_date_bucket | NUMBER | integer | No | None | ACE efs_action.act_date_bucket |
| DF-ACE-126 | act_date_past_due_days | NUMBER | integer | No | None | ACE efs_action.act_date_past_due_days |
| DF-ACE-127 | last_tdr_date | DATE | date | No | None | ACE efs_action.last_tdr_date |

`contact_result` and `action_contact_status` are the 2 EFS columns ACE adds to `efs_action` in RWB-ACE-001; see T3.10, point 1.

**v_ace_score** (Section B, Tier 2). The COLLINS score and route estimate as ingested into ACE. Replaces `score`.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-ACE-270 | score_key | TEXT | varchar(255) | No | None | ACE collins_score.score_key |
| DF-ACE-271 | account_key | TEXT | varchar(255) | No | None | ACE collins_score.account_key |
| DF-ACE-272 | model_code | TEXT | varchar(30) | No | None | ACE collins_score.model_code |
| DF-ACE-273 | model_version | TEXT | varchar(20) | No | None | ACE collins_score.model_version |
| DF-ACE-274 | score_value | NUMBER | numeric(12,4) | No | None | ACE collins_score.score_value |
| DF-ACE-275 | estimate_value | NUMBER | numeric(18,2) | No | None | ACE collins_score.estimate_value |
| DF-ACE-276 | route_code | LOV | varchar(4) | No | LOV-ROUTE | ACE collins_score.route_code |
| DF-ACE-277 | scored_at | DATE | date | No | None | ACE collins_score.scored_at |
| DF-ACE-278 | source_system | TEXT | varchar(20) | No | None | ACE collins_score.source_system |
| DF-ACE-279 | data_as_of | DATE | date | No | None | ACE collins_score.business_date |

Version 2 linked a score to a case (`score.case_id`). An ACE score is keyed by account only. The case is reached through `case_account.account_key`.

**v_ace_batch_status** (Section B, Tier 2). The ACE batch record: one row per source system and business date. P1 reads it for the freshness stamp and the data-job trigger.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-ACE-178 | source_system | TEXT | varchar(20) | No | None | ACE ace_batch_run.source_system |
| DF-ACE-179 | business_date | DATE | date | No | None | ACE ace_batch_run.business_date |
| DF-ACE-180 | started_at | DATE | timestamptz(6) | No | None | ACE ace_batch_run.started_at |
| DF-ACE-181 | completed_at | DATE | timestamptz(6) | No | None | ACE ace_batch_run.completed_at |
| DF-ACE-182 | status | TEXT | varchar(12) | No | None | ACE ace_batch_run.status |
| DF-ACE-183 | record_count | NUMBER | bigint | No | None | ACE ace_batch_run.record_count |
| DF-ACE-184 | checksum | TEXT | varchar(64) | No | None | ACE ace_batch_run.checksum |
| DF-ACE-185 | feed_version | TEXT | varchar(20) | No | None | ACE ace_batch_run.feed_version |
| DF-ACE-186 | is_complete | BOOLEAN | boolean | No | None | ACE ace_batch_run.status = 'COMPLETED' |

`(source_system, business_date)` is unique in ACE. A refused feed writes no row, and the previous COMPLETED row stays the latest (RWB-ACE-001, X1). A re-sent business date keeps one row (X3).

### T3.5 Extension tables (Tier 3)

These are 1:1 tables keyed by an ACE business key. They hold Workbench decisions about an ACE record and never a copy of it. Their primary key is the business key: there is no `id`, and there is no foreign key into `public`. Each also carries the T3.0 standard columns, which are in the field counts (49 dictionary fields in all).

**party_ext** (NEW, Tier 3). Workbench flags about an ACE customer, keyed by `person_key`. Read with `v_ace_customer`.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-EXT-001 | person_key | TEXT | varchar(255) | Yes | None | Workbench; business key of `v_ace_customer.person_key` |
| DF-EXT-002 | vulnerable | BOOLEAN | boolean | Yes | None | Workbench |
| DF-EXT-003 | deceased_override | BOOLEAN | boolean | Yes | None | Workbench |
| DF-EXT-004 | bankruptcy | BOOLEAN | boolean | Yes | None | Workbench |
| DF-EXT-005 | fraud_flag | BOOLEAN | boolean | Yes | None | Workbench |

`fraud_flag` was Aric via COLLINS in version 2. It is the one external field that becomes a recovery extension (register section 4). `deceased_override` records a person's confirmation against `v_ace_customer.deceased_flag`; it does not copy it. DF-EXT-006 to 012 are the standard columns.

**contact_point_ext** (NEW, Tier 3). Consent and contact quality for an ACE phone, email or address, keyed by `contact_key`. Read with `v_ace_contact`.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-EXT-013 | contact_key | TEXT | varchar(255) | Yes | None | Workbench; business key `contact_type:key` of `v_ace_contact.contact_key` |
| DF-EXT-014 | contact_type | LOV | varchar(10) | Yes | PHONE, EMAIL, ADDRESS (check constraint) | Workbench |
| DF-EXT-015 | consent_given | BOOLEAN | boolean | Yes | None | Workbench |
| DF-EXT-016 | consent_at | DATE | timestamptz | No | None | Workbench |
| DF-EXT-017 | verified_at | DATE | timestamptz | No | None | Workbench |
| DF-EXT-018 | failed_count | NUMBER | integer | Yes | None | Workbench |
| DF-EXT-019 | source | TEXT | varchar(20) | Yes | None | Workbench; default WORKBENCH |

DF-EXT-020 to 026 are the standard columns. In version 2, `consent_status` used LOV-CONSENT (GIVEN, WITHDRAWN, UNKNOWN). It is now `consent_given` with `consent_at`: no row means unknown, and false with a date means withdrawn.

**account_ext** (NEW, Tier 3). Workbench state about an ACE account, keyed by `account_key`. Read with `v_ace_account`.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-EXT-027 | account_key | TEXT | varchar(255) | Yes | None | Workbench; business key of `v_ace_account.account_key` |
| DF-EXT-028 | dispute_open | BOOLEAN | boolean | Yes | None | Workbench |

DF-EXT-029 to 035 are the standard columns.

**valuation_ext** (NEW, Tier 3). The Workbench decision about an ACE appraisal, keyed by `valuation_key`. Read with `v_ace_valuation` (Section B).

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-EXT-036 | valuation_key | TEXT | varchar(255) | Yes | None | Workbench; business key of `v_ace_valuation.valuation_key` |
| DF-EXT-037 | accepted | BOOLEAN | boolean | Yes | None | Workbench |
| DF-EXT-038 | accepted_at | DATE | timestamptz | No | None | Workbench |
| DF-EXT-039 | accepted_by | USER_REF | uuid | No | None | Workbench |
| DF-EXT-040 | valuer_partner_id | CROSS_REF | uuid | No | None | Workbench; partner |
| DF-EXT-041 | stale_flag | BOOLEAN | boolean | Yes | None | Workbench |
| DF-EXT-042 | age_days | NUMBER | integer | No | None | Workbench |

DF-EXT-043 to 049 are the standard columns. Physical Schema v5 creates no foreign key on `valuer_partner_id`. Its seed types `accepted_by` as CROSS_REF; this TSD reads it as a user reference. See T3.10, point 6.

### T3.6 Workbench tables P1 owns (Tier 4)

Each table below was checked against Physical Schema v5. Where v5 differs from the dictionary seed or from its own comment, the point is listed in T3.10.

**data_product** (NEW). One of the 14 data products, with its single system of record, owner and refresh cycle.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-REF-070 | id | TEXT | uuid | Yes | None | Workbench |
| DF-REF-071 | product_code | LOV | varchar(25) | Yes | LOV-DATA-PRODUCT | Workbench |
| DF-REF-072 | product_name | TEXT | varchar(80) | Yes | None | Workbench |
| DF-REF-073 | definition | TEXT | varchar(400) | Yes | None | Workbench |
| DF-REF-074 | system_of_record | TEXT | varchar(120) | Yes | None | Workbench |
| DF-REF-075 | owner_role | LOV | varchar(20) | Yes | LOV-ROLE | Workbench |
| DF-REF-076 | owner_user_id | USER_REF | uuid | No | None | Workbench |
| DF-REF-077 | refresh_cycle | LOV | varchar(10) | Yes | LOV-REFRESH | Workbench |
| DF-REF-078 | expected_by | TEXT | varchar(20) | No | None | Workbench |
| DF-REF-079 | valid_from | DATE | date | Yes | None | Workbench |

Physical Schema v5 seeds the 14 rows (DEF-01 fixed). Source-fed products name ACE as the system of record, for example DP01 "ACE (from ALS via COLLINS)", DP06 "ACE (from CCMS, SVAF, AMIS and RPS)", DP11 "ACE (from COLLINS)".

**data_product_access** (NEW). Which role may read which data product, by version.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-REF-080 | id | TEXT | uuid | Yes | None | Workbench |
| DF-REF-081 | product_code | LOV | varchar(25) | Yes | LOV-DATA-PRODUCT | Workbench |
| DF-REF-082 | role_code | LOV | varchar(20) | Yes | LOV-ROLE | Workbench |
| DF-REF-083 | can_read | BOOLEAN | boolean | Yes | None | Workbench |
| DF-REF-084 | access_version | TEXT | varchar(20) | Yes | None | Workbench |
| DF-REF-085 | valid_from | DATE | date | Yes | None | Workbench |
| DF-REF-086 | valid_to | DATE | date | No | None | Workbench |

**data_product_load** (NEW). The freshness stamp of a data product for one business date. It is sourced from the ACE batch record (`ace_batch_run`, read through `v_ace_batch_status`). The name is kept from version 2; no Workbench load writes it.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-OPS-001 | id | TEXT | uuid | Yes | None | Workbench |
| DF-OPS-002 | product_code | LOV | varchar(25) | Yes | LOV-DATA-PRODUCT | Workbench |
| DF-OPS-003 | source_system | TEXT | varchar(40) | Yes | None | Workbench, from `v_ace_batch_status.source_system` |
| DF-OPS-004 | business_date | DATE | date | Yes | None | Workbench, from `v_ace_batch_status.business_date` |
| DF-OPS-005 | source_extracted_at | DATE | timestamptz | Yes | None | Workbench, from `v_ace_batch_status.completed_at` |
| DF-OPS-006 | loaded_at | DATE | timestamptz | Yes | None | Workbench; when the stamp was written |
| DF-OPS-007 | status | LOV | varchar(10) | Yes | LOV-FRESHNESS | Workbench |
| DF-OPS-008 | stale_flagged_at | DATE | timestamptz | No | None | Workbench |
| DF-OPS-009 | duplicate_count | NUMBER | integer | Yes | None | Workbench; repeat COMPLETED reads for the same product and date |

Unique on `(product_code, business_date)`. T3.7 gives the rules.

**data_contract** (NEW). A versioned data contract with one source system, as the source arrives through ACE. The contract is the RWB-ACE-001 field appendix for that source and the view columns that read it. The ACE team lead and the source system owner confirm it.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-OPS-010 | id | TEXT | uuid | Yes | None | Workbench |
| DF-OPS-011 | contract_code | TEXT | varchar(20) | Yes | None | Workbench |
| DF-OPS-012 | source_system | TEXT | varchar(80) | Yes | None | Workbench |
| DF-OPS-013 | interface_id | TEXT | varchar(40) | Yes | None | Workbench; the INT numbers ACE ingests for the source |
| DF-OPS-014 | contract_version | NUMBER | integer | Yes | None | Workbench |
| DF-OPS-015 | status | LOV | varchar(10) | Yes | LOV-CONTRACT-STATUS | Workbench |
| DF-OPS-016 | confirmed_by_role | TEXT | varchar(80) | No | None | Workbench |
| DF-OPS-017 | confirmed_on | DATE | date | No | None | Workbench |
| DF-OPS-018 | confirmation_document_ref | ATTACHMENT | varchar(400) | No | None | Workbench |
| DF-OPS-019 | published_at | DATE | timestamptz | No | None | Workbench |
| DF-OPS-020 | published_by | USER_REF | uuid | No | None | Workbench |

**sys_objects** (NEW). The metadata registry of entities: one row per table or view in the data dictionary. 122 rows: 92 tables and 30 views.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-REF-087 | id | TEXT | uuid | Yes | None | Workbench |
| DF-REF-088 | object_name | TEXT | varchar(60) | Yes | None | Workbench |
| DF-REF-089 | business_name | TEXT | varchar(120) | Yes | None | Workbench |
| DF-REF-090 | subject_area | TEXT | varchar(10) | Yes | None | Workbench |
| DF-REF-091 | data_product | TEXT | varchar(10) | No | None | Workbench |
| DF-REF-092 | system_of_record | TEXT | varchar(120) | Yes | None | Workbench |
| DF-REF-093 | description | TEXT | varchar(400) | Yes | None | Workbench |

`data_product` is nullable, and the foreign key to `data_product.product_code` is created (ruling R1, DEF-03). OPS, AGT and RPT objects carry NULL.

**sys_fields** (NEW). The metadata registry of fields: the data dictionary held as data. 1,366 rows: 1,062 table fields and 304 view fields.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-REF-094 | id | TEXT | uuid | Yes | None | Workbench |
| DF-REF-095 | field_id | TEXT | varchar(16) | Yes | None | Workbench |
| DF-REF-096 | object_name | TEXT | varchar(60) | Yes | None | Workbench |
| DF-REF-097 | field_name | TEXT | varchar(60) | Yes | None | Workbench |
| DF-REF-098 | data_type | TEXT | varchar(12) | Yes | None | Workbench |
| DF-REF-099 | physical_type | TEXT | varchar(30) | Yes | None | Workbench |
| DF-REF-100 | is_mandatory | BOOLEAN | boolean | Yes | None | Workbench |
| DF-REF-101 | lov_code | TEXT | varchar(30) | No | None | Workbench |
| DF-REF-102 | references_object | TEXT | varchar(60) | No | None | Workbench |
| DF-REF-103 | source_system | TEXT | varchar(80) | Yes | None | Workbench |
| DF-REF-104 | source_field | TEXT | varchar(80) | No | None | Workbench |
| DF-REF-105 | is_personal | BOOLEAN | boolean | Yes | None | Workbench |
| DF-REF-106 | description | TEXT | varchar(400) | Yes | None | Workbench |
| DF-REF-107 | owner_role | LOV | varchar(20) | No | LOV-ROLE | Workbench |
| DF-REF-108 | refresh_cycle | TEXT | varchar(30) | No | None | Workbench |
| DF-REF-109 | late_behavior | TEXT | varchar(200) | No | None | Workbench |
| DF-REF-110 | interface_id | TEXT | varchar(10) | No | None | Workbench |

For a view field, `source_system` is ACE and `source_field` is the `public` column the view reads, for example `days_past_due` from `public.account.delay_days`. `v_data_dictionary` joins `sys_fields`, `sys_objects` and `data_product`, so that one query answers where a field comes from and who owns it.

**sys_field_version** (NEW). Each version of a field definition, kept when the definition changes.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-REF-111 | id | TEXT | uuid | Yes | None | Workbench |
| DF-REF-112 | field_id | TEXT | varchar(16) | Yes | None | Workbench |
| DF-REF-113 | field_version | NUMBER | integer | Yes | None | Workbench |
| DF-REF-114 | definition | TEXT | jsonb | Yes | None | Workbench |
| DF-REF-115 | change_reason | TEXT | varchar(400) | Yes | None | Workbench |

**case_list_row** (NEW, re-keyed). One row of the daily case list per case account and business date, published to Power BI. Built from `case_account` joined to `v_ace_account` and `v_ace_efs_action` on `account_key`.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-RPT-001 | id | TEXT | uuid | Yes | None | Workbench |
| DF-RPT-002 | business_date | DATE | date | Yes | None | Workbench; the ACE business date of the ALS batch |
| DF-RPT-003 | case_id | CROSS_REF | uuid | Yes | None | Workbench |
| DF-RPT-004 | case_no | TEXT | varchar(18) | Yes | None | Workbench |
| DF-RPT-005 | account_key | TEXT | varchar(255) | Yes | None | Workbench; ACE business key, no foreign key |
| DF-RPT-006 | account_no | TEXT | varchar(20) | Yes | None | Workbench, from `v_ace_account.account_key` |
| DF-RPT-007 | product_group | LOV | varchar(15) | Yes | LOV-PRODUCT | Workbench |
| DF-RPT-008 | stage_code | LOV | varchar(20) | No | LOV-STAGE | Workbench |
| DF-RPT-009 | status | LOV | varchar(20) | Yes | LOV-CASE-STATUS | Workbench |
| DF-RPT-010 | owner_user_id | USER_REF | uuid | No | None | Workbench |
| DF-RPT-011 | queue_code | TEXT | varchar(30) | No | None | Workbench |
| DF-RPT-012 | team_code | LOV | varchar(20) | No | LOV-TEAM | Workbench |
| DF-RPT-013 | route_code | LOV | varchar(4) | No | LOV-ROUTE | Workbench |
| DF-RPT-014 | total_balance | NUMBER | numeric(18,2) | Yes | None | Workbench, from `v_ace_account.total_balance` at the business date |
| DF-RPT-015 | days_past_due | NUMBER | integer | Yes | None | Workbench, from `v_ace_account.days_past_due` at the business date |
| DF-RPT-016 | refreshed_at | DATE | timestamptz | Yes | None | Workbench |
| DF-RPT-017 | last_contact_at | DATE | timestamptz | No | None | Workbench, latest `v_ace_efs_action.contact_at` across the case's accounts |
| DF-RPT-018 | last_action_code | LOV | varchar(10) | No | LOV-ACTION-CODE | Workbench, `v_ace_efs_action.action_code` of that contact |
| DF-RPT-019 | publish_status | LOV | varchar(10) | Yes | LOV-PUBLISH-STATUS | Workbench |

Version 2 held `account_id` (uuid, foreign key to `loan_account`). It is now `account_key` (Appendix B of the register). The row is a published report row for one business date, not a copy of the account. A rebuild for the same date replaces it.

**reconciliation_result** (NEW). The daily reconciliation of the case list to `v_ace_account`, by product group (JOB-04).

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-OPS-118 | id | TEXT | uuid | Yes | None | Workbench |
| DF-OPS-119 | rec_code | TEXT | varchar(6) | Yes | None | Workbench |
| DF-OPS-120 | business_date | DATE | date | Yes | None | Workbench |
| DF-OPS-121 | product_group | LOV | varchar(15) | Yes | LOV-PRODUCT | Workbench |
| DF-OPS-122 | source_count | NUMBER | integer | Yes | None | Workbench; count from `v_ace_account` |
| DF-OPS-123 | workbench_count | NUMBER | integer | Yes | None | Workbench; count from `case_list_row` |
| DF-OPS-124 | source_amount | NUMBER | numeric(18,2) | No | None | Workbench; balance sum from `v_ace_account` |
| DF-OPS-125 | workbench_amount | NUMBER | numeric(18,2) | No | None | Workbench; balance sum from `case_list_row` |
| DF-OPS-126 | variance_count | NUMBER | integer | Yes | None | Workbench |
| DF-OPS-127 | variance_pct | NUMBER | numeric(9,4) | Yes | None | Workbench |
| DF-OPS-128 | tolerance_pct | NUMBER | numeric(9,4) | Yes | None | Workbench; per data product under DL25 |
| DF-OPS-129 | result | LOV | varchar(8) | Yes | LOV-REC-RESULT | Workbench |

| Rec | Compares | Source side |
|---|---|---|
| REC-01 | Accounts at 90 or more days past due against open case accounts | `v_ace_account.days_past_due` at the ALS business date |
| REC-02 | Balance of open case accounts against ACE | `v_ace_account.total_balance` |
| REC-05 | Every business key on a Workbench row resolves in its view (`case_account.account_key`, `case_party.person_key`, the extension keys) | The matching `v_ace_*` view; replaces the foreign key the boundary rule forbids |

REC-01 and REC-02 write `reconciliation_result` rows. A REC-05 orphan raises a break to the data steward. Load-check exceptions and data quality rules leave P1: ACE ingestion checks the feed (Interface Specifications v3).

**lake_copy_watermark** (NEW). How far a copy to the data lake has reached, for example the decision log copy (JOB-13).

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-OPS-130 | id | TEXT | uuid | Yes | None | Workbench |
| DF-OPS-131 | copy_name | TEXT | varchar(40) | Yes | None | Workbench |
| DF-OPS-132 | last_entry_hash | TEXT | char(64) | No | None | Workbench |
| DF-OPS-133 | last_decided_at | DATE | timestamptz | No | None | Workbench |
| DF-OPS-134 | rows_copied_total | NUMBER | bigint | Yes | None | Workbench |
| DF-OPS-135 | business_date | DATE | date | No | None | Workbench |

**retention_rule** (NEW). How long rows of a table or a retention class are kept and what happens at the end, by version. It covers Workbench tables only. ACE retains its own tables.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-REF-116 | id | TEXT | uuid | Yes | None | Workbench |
| DF-REF-117 | product_code | LOV | varchar(25) | Yes | LOV-DATA-PRODUCT | Workbench |
| DF-REF-118 | table_name | TEXT | varchar(60) | Yes | None | Workbench |
| DF-REF-119 | record_class | TEXT | varchar(20) | Yes | None | Workbench |
| DF-REF-120 | retention_months | NUMBER | integer | Yes | None | Workbench |
| DF-REF-121 | age_basis_field | TEXT | varchar(60) | Yes | None | Workbench |
| DF-REF-122 | end_action | LOV | varchar(12) | Yes | LOV-RETENTION-END | Workbench |
| DF-REF-123 | rule_version | TEXT | varchar(20) | Yes | None | Workbench |
| DF-REF-124 | valid_from | DATE | date | Yes | None | Workbench |
| DF-REF-125 | valid_to | DATE | date | No | None | Workbench |
| DF-REF-126 | approved_by | USER_REF | uuid | No | None | Workbench |
| DF-REF-127 | reference_version_id | CROSS_REF | uuid | No | None | Workbench |

**dp_treatment** (NEW). The copy of each treatment for a business date in the DP04 data product.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-TRT-034 | id | TEXT | uuid | Yes | None | Workbench |
| DF-TRT-035 | treatment_id | CROSS_REF | uuid | Yes | None | Workbench |
| DF-TRT-036 | case_id | CROSS_REF | uuid | Yes | None | Workbench |
| DF-TRT-037 | decision_log_id | CROSS_REF | uuid | No | None | Workbench |
| DF-TRT-038 | treatment_type | LOV | varchar(20) | Yes | LOV-TREATMENT | Workbench |
| DF-TRT-039 | proposed_by | LOV | varchar(10) | Yes | LOV-PROPOSER | Workbench |
| DF-TRT-040 | proposed_at | DATE | timestamptz | Yes | None | Workbench |
| DF-TRT-041 | offer_amount | NUMBER | numeric(18,2) | No | None | Workbench |
| DF-TRT-042 | haircut_amount | NUMBER | numeric(18,2) | No | None | Workbench |
| DF-TRT-043 | installments | NUMBER | integer | No | None | Workbench |
| DF-TRT-044 | valid_until | DATE | date | No | None | Workbench |
| DF-TRT-045 | approval_level | LOV | varchar(4) | No | LOV-APPROVAL-LEVEL | Workbench |
| DF-TRT-046 | booked_at | DATE | timestamptz | No | None | Workbench |
| DF-TRT-047 | outcome | LOV | varchar(12) | No | LOV-TRT-OUTCOME | Workbench |
| DF-TRT-048 | outcome_at | DATE | timestamptz | No | None | Workbench |
| DF-TRT-049 | business_date | DATE | date | Yes | None | Workbench |
| DF-TRT-050 | contract_no | TEXT | varchar(20) | No | None | ACE (from ALS), `v_ace_account.contract_no` of the primary account at the business date |
| DF-TRT-051 | contract_date | DATE | date | No | None | ACE (from ALS), `v_ace_account.contract_date` of the primary account at the business date |

DF-TRT-050 and 051 are a declared business-date snapshot for the DP04 product (Tier Map rule 2). See T3.10, point 4.

**dp_guarantee_claim** (NEW). The copy of each guarantee claim for a business date in the DP04 data product.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-TRT-052 | id | TEXT | uuid | Yes | None | Workbench |
| DF-TRT-053 | guarantee_claim_id | CROSS_REF | uuid | Yes | None | Workbench |
| DF-TRT-054 | case_id | CROSS_REF | uuid | Yes | None | Workbench |
| DF-TRT-055 | claim_type | LOV | varchar(25) | Yes | LOV-CLAIM-TYPE | Workbench |
| DF-TRT-056 | claim_deadline | DATE | date | Yes | None | Workbench |
| DF-TRT-057 | claimed_amount | NUMBER | numeric(18,2) | Yes | None | Workbench |
| DF-TRT-058 | filed_at | DATE | date | No | None | Workbench |
| DF-TRT-059 | paid_amount | NUMBER | numeric(18,2) | No | None | Workbench |
| DF-TRT-060 | status | LOV | varchar(12) | Yes | LOV-CLAIM-STATUS | Workbench |
| DF-TRT-061 | business_date | DATE | date | Yes | None | Workbench |

### T3.7 Freshness rules

| Rule | Detail |
|---|---|
| Source of truth | `v_ace_batch_status`, one row per `source_system` and `business_date` |
| Product to source | Each source-fed data product maps to the ACE source systems in its `system_of_record`: DP01 and DP13 to ALS (DP13 also GL), DP02 to SCBPDM, DP05 to EFS, DP06 to CCMS, SVAF, AMIS and RPS, DP07 to LIT and WIN, DP11 to COLLINS. DP03, DP04, DP08, DP09, DP10, DP12 and DP14 are Workbench products, refreshed on change |
| Ready | Every mapped source has `is_complete` true for the expected business date. P1 writes `data_product_load` with status LOADED and delivers EV-26 AceDataReady |
| Late | The source cut-off (configuration, per source) passes before the row completes. P1 sets status STALE, sets `stale_flagged_at` and publishes EV-27 AceDataLate |
| Repeat | A second COMPLETED read for the same product and business date adds 1 to `duplicate_count` and writes nothing else |
| Display | Every screen and API that shows source data shows the `business_date` and status of its product (API-P1-009, API-P1-010) |
| Before Section B | `v_ace_batch_status` does not exist until RWB-ACE-001 lands. Until then every source-fed product shows STALE with no business date, and no data job starts on its own |

### T3.8 Lists of values

Lists used by the P1 tables and views in this TSD.

| List | Values |
|---|---|
| LOV-APPROVAL-LEVEL | L1, L2, L3, L4, L5, L6 |
| LOV-CASE-STATUS | NEW, ASSIGNED, IN_PROGRESS, WAITING_CUSTOMER, WAITING_PARTNER, WAITING_APPROVAL, ON_HOLD, CLOSED |
| LOV-CLAIM-STATUS | PREPARING, FILED, DEFECT, PAID, REJECTED |
| LOV-CLAIM-TYPE | TCG, CREDIT_LIFE_INSURANCE, MORTGAGE_INSURANCE, COLLATERAL_INSURANCE |
| LOV-CONTRACT-STATUS | DRAFT, PUBLISHED, SUPERSEDED |
| LOV-DATA-PRODUCT | DP01, DP02, DP03, DP04, DP05, DP06, DP07, DP08, DP09, DP10, DP11, DP12, DP13, DP14 |
| LOV-FRESHNESS | LOADED, STALE |
| LOV-PRODUCT | MORTGAGE, HIRE_PURCHASE, SSME, UNSECURED |
| LOV-PROPOSER | AGENT, RULE, PERSON |
| LOV-PUBLISH-STATUS | PENDING, HELD, RELEASED |
| LOV-REC-RESULT | PASS, BREAK |
| LOV-REFRESH | DAILY, WEEKLY, MONTHLY, ON_CHANGE |
| LOV-RETENTION-END | ARCHIVE, REVIEW |
| LOV-ROUTE | R1, R2, R3, R4, R5, R6, R7, R8 |
| LOV-STAGE | RESTRUCTURE, SETTLEMENT, DEED_IN_LIEU, GUARANTEE_CLAIM, LITIGATION, ASSET_DISPOSAL, DEBT_SALE, WRITE_OFF, DEVIATIONS |
| LOV-TREATMENT | RESTRUCTURE, SETTLEMENT, DEED_IN_LIEU, BUY_BACK, GUARANTEE_CLAIM, REPOSSESSION, AUCTION, DEBT_SALE, WRITE_OFF, RAMC_TRANSFER, RENTAL |
| LOV-TRT-OUTCOME | KEPT, BROKEN, COMPLETED, CANCELED, DECLINED |
| LOV-ACTION-CODE | Loaded from `v_ace_efs_action_code` (1,106 values) |
| Contact type (check constraint) | PHONE, EMAIL, ADDRESS |

Leave P1 with the objects that used them: LOV-CHANNEL, LOV-COLL-TYPE, LOV-CONSENT, LOV-CONTACT-RESULT, LOV-CONTACT-SRC, LOV-DQ-RULE-TYPE, LOV-DQ-STATUS, LOV-ENCUMBRANCE, LOV-ID-TYPE, LOV-LOAD-STATUS, LOV-OCCUPANCY, LOV-PARTY-TYPE, LOV-SEGMENT, LOV-TRACKER-DECISION, LOV-TRACKER-LOCATION, LOV-TRACKER-STATUS and LOV-UPDATE-CYCLE. Coded values on ACE fields come from ACE. Lists other TSDs still use stay with those TSDs.

### T3.9 Relationships

Foreign keys inside schema `recovery` (Physical Schema v5):

| From | Field | To | Cardinality |
|---|---|---|---|
| case_list_row | case_id | recovery_case | Many to 1 |
| retention_rule | reference_version_id | reference_version | Many to 0 or 1 |
| dp_treatment | treatment_id | treatment | Many to 1 |
| dp_treatment | case_id | recovery_case | Many to 1 |
| dp_treatment | decision_log_id | decision_log_entry | Many to 0 or 1 |
| dp_guarantee_claim | guarantee_claim_id | guarantee_claim | Many to 1 |
| dp_guarantee_claim | case_id | recovery_case | Many to 1 |
| sys_fields | object_name | sys_objects | Many to 1 |
| sys_objects | data_product | data_product | Many to 0 or 1 |

Business-key links to a view (no foreign key, checked by REC-05):

| From | Field | To view | Cardinality |
|---|---|---|---|
| case_list_row | account_key | v_ace_account.account_key | Many to 1 |
| party_ext | person_key | v_ace_customer.person_key | 0 or 1 to 1 |
| contact_point_ext | contact_key | v_ace_contact.contact_key | 0 or 1 to 1 |
| account_ext | account_key | v_ace_account.account_key | 0 or 1 to 1 |
| valuation_ext | valuation_key | v_ace_valuation.valuation_key | 0 or 1 to 1 |
| data_product_load | source_system, business_date | v_ace_batch_status | Many to 1 |
| reconciliation_result | business_date, product_group | v_ace_account (aggregate) | Many to 1 |

Keys between views (ACE's own keys, read through the views):

| From view | Field | To view |
|---|---|---|
| v_ace_payment, v_ace_collateral, v_ace_efs_action, v_ace_efs_assignment, v_ace_bucket_log, v_ace_plan, v_ace_lawsuit, v_ace_pod, v_ace_write_off, v_ace_score, v_ace_credit_decision, v_ace_esign | account_key | v_ace_account |
| v_ace_contact, v_ace_ca_relation, v_ace_efs_action, v_ace_party_product | person_key | v_ace_customer |
| v_ace_collateral, v_ace_valuation, v_ace_collateral_detail, v_ace_npa_asset | asset_key | v_ace_asset |
| v_ace_hearing | lawsuit_key | v_ace_lawsuit |
| v_ace_npa_sale | npa_asset_key | v_ace_npa_asset |

### T3.10 Removed from P1 in version 3

| Version 2 object | Fields | Reason (D-RCV-35) | Read path now |
|---|---:|---|---|
| loan_account | 24 | Copy of ALS data (U1) | `v_ace_account`; `dispute_open` to `account_ext` |
| account_payment | 7 | Copy of ALS data (U1) | `v_ace_payment` |
| party | 13 | Copy of SCBPDM data (U1) | `v_ace_customer`; flags to `party_ext` |
| contact_point | 8 | Copy of SCBPDM data (U1) | `v_ace_contact`; consent and quality to `contact_point_ext` |
| collateral | 13 | Copy of CCMS data (U1) | `v_ace_collateral`, `v_ace_collateral_detail` |
| account_collateral | 4 | Copy of CCMS data (U1) | `v_ace_collateral`; `lien_rank` from `v_ace_collateral_detail` |
| score | 9 | Moves to ACE (U2) | `v_ace_score` |
| collections_history | 10 | Copy of EFS data (U1) | `v_ace_efs_action` |
| load_run | 20 | No inbound load (U1) | ACE batch record, `v_ace_batch_status` |
| dq_exception | 11 | No inbound load (U1) | ACE ingestion checks; REC-01, REC-02, REC-05 for reconciliation |
| dq_rule | 12 | No inbound load (U1) | ACE ingestion checks |
| source_field_map | 11 | No inbound load (U1) | STTM v4 and the RWB-ACE-001 field appendix |
| source_code_map | 8 | No inbound load (U1) | ACE ingestion; list values from ACE |
| tracker_inventory | 26 | Trackers leave system scope (U5) | Cutover plan |
| tracker_row | 9 | Trackers leave system scope (U5) | Cutover plan |

The other removals in register section 5 (`party_product`, `valuation`, `asset`, `interface_run`, `interface_signoff`) were not P1 objects in version 2. Their replacements `v_ace_party_product`, `v_ace_valuation` with `valuation_ext`, and `v_ace_asset` with `v_ace_npa_asset` are in T3.3. Outbound runs move to `outbound_item` and `outbox_delivery` (P2).

### T3.11 Points to correct in Physical Schema v5

Found while checking this TSD against v5. None of them blocks the build. Each goes to the Wave 1 verify agent or to the owning story.

| # | Object | Point | Proposed fix |
|---:|---|---|---|
| 1 | Section B views | The 12 Tier 2 columns on existing ACE tables (7 on `account`, 3 on `customer`, 2 on `efs_action`) are not in `v_ace_account`, `v_ace_customer` or `v_ace_efs_action`, or in any view, in Source Views v1 or v5 | Section B re-creates those three views with the columns appended at the end. CREATE OR REPLACE VIEW allows this. Add the dictionary rows and re-count |
| 2 | `sys_fields` rows for the 30 views | Physical types are placeholders. All Section B fields are `integer`. `tdr_flag`, `deceased_flag` and `is_staff` are TEXT where the view returns boolean. `payment_date` is varchar where the view returns date. `total_balance` is integer where the view returns numeric(38,2) | Re-derive each row from the view definition. T3.4 gives the values for the detailed views |
| 3 | `case_list_row`, `dp_treatment`, `dp_guarantee_claim` | The unique constraint is `UNIQUE (business_date)` alone, which allows one row per day. The `case_list_row.account_key` comment says "unique with business_date". `case_list_row.account_key` is nullable in the DDL but mandatory in the dictionary | `UNIQUE (business_date, account_key)` with `account_key NOT NULL`. `UNIQUE (business_date, treatment_id)` and `UNIQUE (business_date, guarantee_claim_id)` |
| 4 | `dp_treatment.contract_no`, `contract_date`; `data_product_load.source_extracted_at`; DP01 `system_of_record` | Still say "via COLLINS" or "from the COLLINS control record or the file" (DEF-05) | Re-word to ACE (from ALS) and `v_ace_batch_status.completed_at` |
| 5 | `data_product.refresh_cycle` | Still `varchar(10)`. DEF-02 says v5 widens it to varchar(30). The v5 seed values fit (ON_CHANGE) | Widen it, or close DEF-02 as "codes, not labels" |
| 6 | `sys_objects.data_product`; `valuation_ext.accepted_by` | Nullable in the DDL, but the DF-REF-091 seed says mandatory. `accepted_by` is seeded CROSS_REF and should be USER_REF | Correct the two seed rows |
| 7 | `collateral.occupancy`, `encumbrance_status` | Workbench-entered in version 2 (DF-COL-010, 011). No extension table or ACE column holds them in v5 | Owner of the S5 Assets and auction TSD to confirm: drop, or add them to an extension table |
| 8 | Lists of values | v5 still seeds LOV-DQ-RULE-TYPE, LOV-DQ-STATUS, LOV-LOAD-STATUS, LOV-TRACKER-DECISION, LOV-TRACKER-LOCATION, LOV-TRACKER-STATUS and LOV-UPDATE-CYCLE, and no table uses them | Remove the seed rows |
| 9 | `case_list_row.account_no` | Field Gap List v1 maps `loan_account.account_no` to `v_ace_account.account_no`, but the view has no such column. The account number is the ACE business key `account_key` | Name the source `v_ace_account.account_key` in STTM v4, or add `account_no` as an alias in the view |

## T4. State machines and workflow

No case state machine of its own. The module acts on events from P3 and on the ACE batch record, and writes through the decision log. A data product's freshness moves between LOADED and STALE for each business date (T3.7).

## T5. Integration and interfaces

### T5.1 External system interfaces

P1 runs no inbound interface. Every inbound source is ingested by ACE (U1), and P1 reads the result through the view named below. The ACE team owns each inbound interface, its file specification and its ingestion checks (Interface Specifications v3).

| ID | System | Direction | Owner | Read path in the Workbench | Frequency |
|---|---|---|---|---|---|
| INT-01 | Core bank (ALS) | In, into ACE | ACE team | `v_ace_account` | Daily, end of day |
| INT-02 | Core bank (ALS) | In, into ACE | ACE team | `v_ace_payment` | Daily, end of day |
| INT-04 | SCBPDM | In, into ACE | ACE team | `v_ace_customer`, `v_ace_contact`, `v_ace_party_product` | Daily, end of day |
| INT-07 | EFS | In, into ACE | ACE team | `v_ace_efs_action`, `v_ace_efs_assignment` | Daily, end of day |
| INT-08 | COLLINS models | In, into ACE | ACE team | `v_ace_score` | Daily; monthly for some models |
| INT-09 | LIT | In, into ACE | ACE team | `v_ace_lawsuit`, `v_ace_hearing` | Daily, end of day |
| INT-10 | CCMS | In, into ACE | ACE team | `v_ace_collateral`, `v_ace_collateral_detail` | Weekly |
| INT-11 | SVAF | In, into ACE | ACE team | `v_ace_valuation` | Weekly |
| INT-12 | AMIS | In, into ACE | ACE team | `v_ace_npa_asset`, `v_ace_npa_sale` | Monthly |
| INT-13 | RPS | In, into ACE | ACE team | `v_ace_npa_asset` | Weekly |
| INT-15 | WIN | In, into ACE | ACE team | `v_ace_pod` | Weekly |
| INT-16 | GL | In, into ACE | ACE team | `v_ace_write_off` | Monthly |
| New ACE interface (number in Interface Specifications v3) | NLEADS | In, into ACE | ACE team | `v_ace_credit_decision` | As decisions are made |
| New ACE interface (number in Interface Specifications v3) | EasyApp | In, into ACE | ACE team | `v_ace_esign` | As signatures are requested |
| All of the above | ACE batch record | In, into ACE | ACE team | `v_ace_batch_status` | Per source and business date |
| INT-19 | Data lake and Power BI | Out | Workbench | Case list publish (`case_list_row`) and decision log copy (JOB-13) | Daily |

INT-05 (UDP) is not in Interface Specifications v3 and leaves this table. P1 runs no load check: ACE refuses a failed feed, and P1 sees only the last complete business date.

### T5.2 Cross-module interfaces

Calls go through the published Java interfaces: P3 for the case, P7 for the decision log, P4 for access and reference data, P5 for documents and P6 for notices. Other modules read ACE data through P1's AceSourceReadRepository interface, and through no other path.

### T5.3 Events

| Event | Direction | Detail |
|---|---|---|
| EV-26 AceDataReady | Consumed | Raised from `v_ace_batch_status` when a source completes for the expected business date. Starts the case list build and JOB-04, and is passed on to JOB-02, JOB-07, JOB-08 and JOB-16 |
| EV-27 AceDataLate | Published | Raised by P1 when the source cut-off passes before the ACE batch row completes. Consumers: alerts, the stale marker and the data steward |

Payload for both: eventId, occurredAt, schemaVersion, sourceSystem, businessDate, status, completedAt. Each field maps one to one to the view column. LoadCompleted and LoadRefused are retired: no Workbench load exists to raise them.

## T6. Security and access control

### T6.1 RBAC matrix

| Role | Platform administration |
|---|---|
| RW-COE Center of excellence analyst | R |
| RW-DATASTEW Data steward and data product owner | R |
| RW-AUDIT Internal audit | R |
| RW-COMPLY Compliance and PDPA officer | R |
| RW-PLATADM Platform administrator | CRUD |
| RW-SECADM Security administrator | CRUDA |

### T6.2 Authentication and authorization

Entra ID single sign-on through the ACE front end. Each endpoint declares its capability area and right. Scope filters every query. Masking applies to personal fields. Jobs and agents use service identities. The SY-DATALOAD actor is removed (Admin and Access Model v5). The read-only ACE service identity replaces it.

### T6.3 Database grants and the conformance test

| Item | Rule |
|---|---|
| `ace_view_owner` | Dedicated NOLOGIN role. Holds SELECT on the 22 Tier 1 ACE tables, and on the Tier 2 tables once RWB-ACE-001 lands. Owns every `v_ace_*` view |
| Recovery service identity | USAGE on schema `recovery`; SELECT on the views. No SELECT on any `public` table. No INSERT, UPDATE, DELETE or TRUNCATE on any `public` table |
| PUBLIC | REVOKE ALL on schema `recovery` tables |
| Row-level security | A view owned by a definer role runs with that role's privileges. Any row-level security ACE adds later is applied inside the view |
| Personal data | `customer.identification_number` is exposed only as `id_no_masked` and `id_no_last4`. Phone, email and address are exposed in full for notices and calls. Display masking is E1-037 at the API, and every read is audited. The control is the grant plus E1-037 plus the audit log, not the view mask alone |

The conformance test (RWB-E1-069) runs in the pipeline and fails the build if:

1. any `recovery.v_ace_*` view does not compile;
2. any constraint in schema `recovery` references a table outside it;
3. `select * from recovery.v_ace_account where days_past_due > 90` returns no rows in SIT;
4. the recovery role can select a `public` table directly, or can insert, update or delete on any `public` or `recovery` table it should only read;
5. `v_data_dictionary` does not return `days_past_due` sourced from `public.account.delay_days`, or the `sys_objects` and `sys_fields` counts are not 122 and 1,366.

TE-001 is extended so that the module boundary test allows `recovery.v_ace_*` as the only cross-schema read.

## T7. Non-functional requirements

| ID | Requirement | Target | Status |
|---|---|---|---|
| NFR-001 | The case store holds one case per customer and product for every account at 90 or more days past due across Mortgage, Hire Purchase and SSME. | About 23,600 open cases at go-live and 26,500 at the end of 2027, from 3,110 new accounts at 90 days past due a month. Confirmed under DL15 | Proposed from the volume forecast |
| NFR-002 | The system supports the peak number of staff users signed on at once. | About 370 staff online in the busiest hour, of 914 named users | Proposed from the volume forecast |
| NFR-003 | The system supports the peak number of partner users signed on at once across 73 agencies, 11 to 12 law firms, 4 auction vendors and 35 buyers. | About 50 partner users online in the busiest hour, of about 320 named users | Proposed from the volume forecast |
| NFR-004 | The document store holds the annual inbound document volume with its growth rate. | About 860,000 documents in 2027, rising with 15 percent inflow growth a year | Proposed from the volume forecast |
| NFR-005 | The restructure path carries the monthly case volume reaching the Workbench. | About 3,000 restructure accounts a month reach the bank's restructure process today | Proposed |
| NFR-006 | The deed in lieu path carries its target monthly volume. | 1,000 cases a month in 2027, from 685 today | Proposed |
| NFR-007 | The decision log holds one record for every decision on every case for the full retention period without degrading query time. | About 36 GB for the decision log and the interaction ledger by the end of 2031; a single case history query under 2 seconds at that size | Proposed, DL11 |
| NFR-069 | The document hub holds the full recovery document estate as a system of record, including every version and every held document, with storage sized for growth. | About 5.8 million documents and 2.8 TB by the end of 2031, with every version and held document | Proposed, DL11 |
| NFR-070 | The interaction ledger holds every interaction on every open and closed case within its retention period, and reads a single case history inside the user wait. | One case history reads in under 2 seconds with the ledger at its 2031 size | Proposed, DL11 |
| NFR-013 | The ACE batch record for ALS is complete before the working day starts. If it is not, AceDataLate raises an alert. | ACE batch complete by 07:00; the Workbench data jobs start on it. Ingestion time is owned by the ACE team (RWB-ACE-001) | Proposed |
| NFR-014 | Collections (EFS) data is in ACE at start of day. | Start of day, through ACE ingestion | Proposed |
| NFR-015 | Source data read through the views is no more than the agreed lag behind its source, and a decision that must be made the same day uses an event instead. | End of day; in the Workbench the next morning. The views add no lag of their own. Same-day needs are named under DL06 | Proposed |
| NFR-016 | The document intake pipeline processes its throughput in the test environment. | 500 pages per hour | Proposed |
| NFR-017 | Document classification is correct on the labeled sample, and anything below the confidence threshold goes to a review queue. | 90 percent correct | Proposed |
| NFR-018 | The case list reconciles to `v_ace_account` daily. | No unexplained variance; tolerance per data product under DL25 | Proposed, DL25 |
| NFR-019 | The daily rebalancing job completes before the working day starts. | Complete by 07:00 | Proposed, DL11 |

## T8. Requirement traceability

| Requirement | Feature | Story | Test |
|---|---|---|---|
| REQ-RDF-001 | FEAT-RDF-01 | RWB-E1-001, RWB-E1-064, RWB-ACE-001 | TC-E1-001-01, TC-ACE-001-01 |
| REQ-RDF-002 | FEAT-RDF-01 | RWB-E1-069, RWB-ACE-001 | TC-E1-069-02, TC-ACE-001-04 |
| REQ-RDF-003 | FEAT-RDF-01 | RWB-E1-069 (EFS through `v_ace_efs_action`) | TC-E1-069-02 |
| REQ-RDF-004 | FEAT-RDF-01 | RWB-E1-069 Section B, RWB-ACE-001 (CCMS, SVAF) | TC-E1-069-02, TC-ACE-001-08 |
| REQ-RDF-005 | None | None: trackers leave system scope (D-RCV-35 U5); Cutover plan | None |
| REQ-RDF-006 | None | None: trackers leave system scope (D-RCV-35 U5); Cutover plan | None |
| REQ-RDF-007 | FEAT-RDF-01 | RWB-E1-002, RWB-E1-011 | TC-E1-002-01, TC-E1-011-01 |
| REQ-RDF-008 | FEAT-RDF-01 | RWB-E1-011 (reconciliation only; data quality rules move to ACE ingestion) | TC-E1-011-01 |
| REQ-RDF-009 | FEAT-RDF-01 | RWB-E1-015 | TC-E1-015-01 |
| REQ-RDF-010 | FEAT-RDF-01 | RWB-E1-016 | TC-E1-016-01 |
| REQ-RDF-011 | FEAT-RDF-01 | RWB-E1-016, RWB-E1-064 | TC-E1-064-01 |
| REQ-RDF-012 | FEAT-RDF-01 | RWB-E1-013 (P9) | TC-E1-013-01 |
| REQ-RDF-013 | FEAT-RDF-01 | RWB-E1-014, RWB-E1-017 | TC-E1-014-01, TC-E1-017-01 |
| REQ-RDF-014 | FEAT-RDF-01 | RWB-E1-044 | TC-E1-044-01 |

Removed stories that used to trace here: RWB-E1-003, 004, 005, 006, 009, 010, 012 and 051 (register Appendix A). The RTM confirms the test IDs in Wave 4.

## Appendix T-A. API specification

### T-A.1 Endpoint inventory

| ID | Method | Path | Access | First in |
|---|---|---|---|---|
| API-P1-001 | GET | /api/recovery/v1/admin/jobs | Platform administration R | E1 |
| API-P1-002 | POST | /api/recovery/v1/admin/jobs/{jobId}/rerun | Platform administration U | E1 |
| API-P1-003 | GET | /api/recovery/v1/admin/reconciliation/results | Platform administration R | E1 |
| API-P1-009 | GET | /api/recovery/v1/data-products/freshness | Case record R | E1 |
| API-P1-010 | GET | /api/recovery/v1/data-products/{productCode}/records | Case record R | E1 |
| API-P1-011 | GET | /api/recovery/v1/admin/data-products | Platform administration R | E1 |
| API-P1-012 | GET | /api/recovery/v1/admin/data-dictionary/fields | Reference data R | E1 |
| API-P1-013 | PATCH | /api/recovery/v1/admin/data-dictionary/fields/{fieldCode} | Reference data U | E1 |
| API-P1-014 | GET | /api/recovery/v1/admin/data-contracts | Reference data R | E1 |
| API-P1-015 | PATCH | /api/recovery/v1/admin/data-contracts/{contractId} | Reference data U | E1 |
| API-P1-016 | POST | /api/recovery/v1/admin/data-contracts/{contractId}/publish | Reference data U | E1 |

Retired in version 3. The IDs are not reused.

| ID | Version 2 endpoint | Reason |
|---|---|---|
| API-P1-004 | GET /admin/trackers | Trackers leave system scope (D-RCV-35 U5) |
| API-P1-005 | POST /admin/trackers/{trackerId}/loads | No tracker load (U1, U5) |
| API-P1-006 | POST /admin/trackers/{trackerId}/sign-off | Tracker retirement moves to the Cutover plan (U5) |
| API-P1-007 | POST /admin/trackers/{trackerId}/retire | Tracker retirement moves to the Cutover plan (U5) |
| API-P1-008 | GET /admin/trackers/retirement-report | Tracker retirement moves to the Cutover plan (U5) |

API-P1-003 keeps its ID and changes path and purpose. Version 2's GET /admin/data-quality/exceptions listed load-check exceptions and reconciliation breaks. The load checks leave with the load, so only the reconciliation results remain.

### T-A.2 Endpoint detail

#### API-P1-001 GET /admin/jobs

| Item | Value |
|---|---|
| Purpose | List the Workbench data jobs (case list build, JOB-02, JOB-04, JOB-07, JOB-08, JOB-13, JOB-16) with status and the ACE business date each ran for. No load or file job is listed |
| Request | Query: jobCode, status, from, to |
| Response | Job[] |
| Errors | 401, 403, 503 |
| Authorization | Platform administration, right R, scope applied |
| Idempotency | Not applicable |

#### API-P1-002 POST /admin/jobs/{jobId}/rerun

| Item | Value |
|---|---|
| Purpose | Rerun a failed Workbench data job for a business date the ACE batch record shows complete. No source load is rerun: a late or refused feed is fixed by ACE ingestion |
| Request | None |
| Response | Job |
| Errors | 401, 403, 404, 409 (business date not complete in `v_ace_batch_status`, or job running), 503 |
| Authorization | Platform administration, right U, scope applied |
| Idempotency | Idempotency-Key header |

#### API-P1-003 GET /admin/reconciliation/results

| Item | Value |
|---|---|
| Purpose | List the daily reconciliation results and breaks of the case list against `v_ace_account` (REC-01, REC-02), and REC-05 orphan keys |
| Request | Query: recCode, product, result, from, to |
| Response | ReconciliationResult[] |
| Errors | 401, 403, 503 |
| Authorization | Platform administration, right R, scope applied |
| Idempotency | Not applicable |

#### API-P1-009 GET /data-products/freshness

| Item | Value |
|---|---|
| Purpose | Read the freshness stamp of each data product: business date, status (LOADED or STALE) and the ACE batch completion time, taken from `v_ace_batch_status` |
| Request | Query: product, asOf |
| Response | DataProductFreshness[] |
| Errors | 400, 401, 403, 503 |
| Authorization | Case record, right R, scope applied |
| Idempotency | Not applicable |

#### API-P1-010 GET /data-products/{productCode}/records

| Item | Value |
|---|---|
| Purpose | Read the rows of one data product for a case, read through the `v_ace_*` views and the extension tables, masked by role (E1-037), with the product's freshness stamp |
| Request | Query: caseId, page, size |
| Response | DataProductRecordPage |
| Errors | 400, 401, 403, 404, 503 |
| Authorization | Case record, right R, scope applied |
| Idempotency | Not applicable |

#### API-P1-011 GET /admin/data-products

| Item | Value |
|---|---|
| Purpose | List the data catalog entries, with each product's system of record (ACE or the Workbench), owner and refresh cycle |
| Request | Query: product |
| Response | DataProductCatalogEntry[] |
| Errors | 401, 403, 503 |
| Authorization | Platform administration, right R, scope applied |
| Idempotency | Not applicable |

#### API-P1-012 GET /admin/data-dictionary/fields

| Item | Value |
|---|---|
| Purpose | Search the data dictionary: 122 objects (92 tables, 30 views) and 1,366 fields. A view field returns its ACE source column |
| Request | Query: product, entity, field, sourceSystem, page, size |
| Response | DataDictionaryFieldPage |
| Errors | 401, 403, 503 |
| Authorization | Reference data, right R, scope applied |
| Idempotency | Not applicable |

#### API-P1-013 PATCH /admin/data-dictionary/fields/{fieldCode}

| Item | Value |
|---|---|
| Purpose | Change a field definition with a reason, creating a new version. Only the description, owner and late behavior of a view field can change; its type and source follow the view migration |
| Request | DataDictionaryFieldChange |
| Response | DataDictionaryField |
| Errors | 401, 403, 404, 409, 422, 503 |
| Authorization | Reference data, right U, scope applied |
| Idempotency | Not applicable |

#### API-P1-014 GET /admin/data-contracts

| Item | Value |
|---|---|
| Purpose | List the data contracts per source system, as the source arrives through ACE |
| Request | Query: sourceSystem, status |
| Response | DataContract[] |
| Errors | 401, 403, 503 |
| Authorization | Reference data, right R, scope applied |
| Idempotency | Not applicable |

#### API-P1-015 PATCH /admin/data-contracts/{contractId}

| Item | Value |
|---|---|
| Purpose | Record the confirmation of a data contract by the ACE team lead and the source system owner, against the RWB-ACE-001 field appendix |
| Request | DataContractConfirmation |
| Response | DataContract |
| Errors | 401, 403, 404, 409, 422, 503 |
| Authorization | Reference data, right U, scope applied |
| Idempotency | Not applicable |

#### API-P1-016 POST /admin/data-contracts/{contractId}/publish

| Item | Value |
|---|---|
| Purpose | Publish a confirmed data contract |
| Request | None |
| Response | DataContract |
| Errors | 401, 403, 404, 409, 503 |
| Authorization | Reference data, right U, scope applied |
| Idempotency | Idempotency-Key header |

## Appendix T-B. Open technical decisions

| Decision | What is needed |
|---|---|
| DL06 | Which interfaces need same-day data |
| DL11 | Non-functional target values |
| DL25 | Reconciliation tolerance per data product |
| DL35 | Deployment slots |
| DL43 | The ACE team accepts the RWB-ACE-001 scope and dates. Needed by 2026-11-21 for a 30 November release. Blocks the Section B migration, freshness, and every feature that reads a Section B view |
| Register 2.1 | AMIS, RPS, LIT, WIN, GL and COLLINS are ingested by ACE. If any one is not, its view leaves Section B and U1 reopens for that source |

## Document sign-off

| Role | Name | Signature | Date |
|---|---|---|---|
| Solution architect | | | |
| Tech lead | | | |
| ACE team | | | |
| QA lead | | | |
