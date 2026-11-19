<!-- source: 15 ACE DB Alignment/Recovery Workbench ACE Data Tier Map v1.md -->
<!-- converted: 2026-11-16 from Markdown (copied) -->

> **Source:** `15 ACE DB Alignment/Recovery Workbench ACE Data Tier Map v1.md`  
> **Converted from:** Markdown (copied)

# Recovery Workbench ACE data tier map

SCB Collections and Recovery. Henka Group, 15 November 2026.

(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Document | Recovery Workbench ACE Data Tier Map v1 |
| Purpose | The frozen table-and-column map that every Wave 1 to Wave 5 edit reads: what the Workbench takes from ACE, what the ACE team adds, what the Workbench owns, and what leaves the schema |
| Status | Frozen input. Changes need the data architect and the recovery tech lead, and a new version of this file |
| Decision | D-RCV-35 (U1 to U5) |
| Companions | Recovery Workbench ACE DB Alignment Change Register v1.md; Recovery Workbench ACE Field Gap List v1.xlsx; Recovery Workbench ACE Source Views v1.sql; ACE Schema PostgreSQL v1.sql |
| Counts fixed here | 108 tables to 92 tables, 30 views, 122 dictionary objects, 1,366 dictionary fields |

## 1. The boundary rule

The Workbench never loads source data. Every source record lands in the ACE database through ACE's own ingestion. The recovery module reads it through one surface only:

- `recovery.v_ace_*` views, `SELECT` only, owned by the recovery module and by a dedicated `ace_view_owner` role that holds `SELECT` on the ACE tables.
- The recovery service identity holds `SELECT` on the views and on nothing else, so a direct read of a `public` table fails in the catalog, not only in code review.
- No foreign key from a `recovery` table into a `public` table, because ACE uses `ON DELETE CASCADE` on `account` and a cascade would delete Workbench case history.
- Workbench links to source records are business-key columns (`varchar(255)`), not UUID foreign keys.
- The recovery schema never writes to `public`.

Two migrations, because a view cannot be created over a table that does not exist yet:

| Migration | Contains | Ships |
|---|---|---|
| Section A | 16 views over ACE tables that exist today, 177 fields | With RWB-E1-069, the next free sequence after the V0001 baseline |
| Section B | 14 views over the Tier 2 additions, 127 fields | The week RWB-ACE-001 lands; until then the dependent features stay behind their flags |

## 2. Tier 1 - ACE tables that exist today, read through a view and never altered

| # | ACE table | View | Used for | Note |
|---:|---|---|---|---|
| 1 | `account` | `v_ace_account` | Account, arrears, balances, classification, restructure flag, batch date | `delay_days` becomes `days_past_due`; `core_banking_system_date` becomes `data_as_of` |
| 2 | `payment` | `v_ace_payment` | Payments, proceeds matching | `pay_date` is `varchar`, cast by `ace_to_date` |
| 3 | `customer` | `v_ace_customer` | Party, identity, vulnerability inputs | `identification_number` is masked in the view |
| 4 | `phone` | `v_ace_contact` | Contact point, notice and call inputs | Union with email and address, `contact_type` discriminator |
| 5 | `email` | `v_ace_contact` | Contact point | Same view |
| 6 | `address` | `v_ace_contact` | Contact point, notice address | Same view |
| 7 | `ca_relation` | `v_ace_ca_relation` | Borrower, guarantor and co-borrower roles | |
| 8 | `aa_relation` | `v_ace_aa_relation` | Parent and child accounts | |
| 9 | `collateral` | `v_ace_collateral` | Collateral link and value | |
| 10 | `asset` | `v_ace_asset` | Collateral asset and held asset | |
| 11 | `efs_action` | `v_ace_efs_action` | Collections history and interaction | Replaces `collections_history` |
| 12 | `efs_action_code` | `v_ace_efs_action_code` | Action code list of values | 1,106 values, loaded list |
| 13 | `efs_assignment` | `v_ace_efs_assignment` | Assignment and hand-over history | |
| 14 | `bucket_log_snapshot` | `v_ace_bucket_log` | Monthly bucket history | The daily bucket is a Tier 2 column |
| 15 | `product` | `v_ace_product` | Product and product group lists | |
| 16 | `branch` | `v_ace_branch` | Branch and region lists | |
| 17 | `bot_holiday` | `v_ace_holiday` | Service level and legal-day calendar | E1-043 and E1-045 use this instead of a Workbench list |
| 18 | `iam_user` | none | Sign-on identity, read by the ACE common module | Not read by the recovery module |
| 19 | `ace_case` | `v_ace_plan` | Restructure plan reference and status | E2-002 already reads ACE |
| 20 | `cfsc_mg_ssme_tdr_case` | `v_ace_plan` | Plan booking, approval and closure dates | |
| 21 | `tdr_calculation` | `v_ace_plan` | Published calculation version | |
| 22 | `ai_recommended_plan` | `v_ace_plan` | Recommended installments and package | |
| 23 | Quartz tables `qrtz_*` | none | Scheduler state, shared with ACE | No new `qrtz_` table is created |
| 24 | Spring Batch tables `batch_*` | none | Step execution, shared with ACE | The per-source completion record is `ace_batch_run`, Tier 2 |

Tier 1 tables are never altered by the Workbench. Where ACE already holds a column with a different name or type, the view maps it. Where ACE holds nothing, the field is Tier 2.

## 3. Tier 2 - new ACE tables and columns, owned by the ACE team

The ACE team owns these. The Workbench raises them once, in RWB-ACE-001, with the field appendix. The count is 80 field mappings to 14 new tables and 12 new columns; 79 distinct columns, because `efs_action.contact_result` serves two LDM fields.

| # | ACE object | Kind | Columns | Source | Why ACE does not have it |
|---:|---|---|---:|---|---|
| 1 | `ace_batch_run` | new table | 9 | all | A per-source business date and completion record; the Workbench freshness stamp and the intake trigger read it |
| 2 | `valuation` | new table | 11 | SVAF | ACE holds no appraisal |
| 3 | `collateral_detail` | new table | 15 | CCMS | Title deed, plot, area, province, district, subdistrict, insured value, insurance expiry, lien rank |
| 4 | `npa_asset` | new table | 14 | AMIS, RPS | ACE holds the collateral asset, not the repossessed or purchased asset |
| 5 | `npa_sale` | new table | 13 | AMIS | Sale contract, taxes, fees and incentive |
| 6 | `lawsuit` | new table | 15 | LIT | Court case numbers, claim, judgment and status |
| 7 | `hearing` | new table | 9 | LIT | Hearing date, type and next date |
| 8 | `pod_receipt` | new table | 12 | WIN | Proof of delivery for a notice |
| 9 | `gl_write_off` | new table | 11 | GL | Write-off posting, cost centre and GL product |
| 10 | `collins_score` | new table | 12 | COLLINS | Score, estimate and route, if ACE does not already hold it |
| 11 | `party_product` | new table | 7 | SCBPDM | Customer product holding |
| 12 | `credit_decision` | new table | 10 | NLEADS | Credit result, reason and decision date for a treatment |
| 13 | `esign_request` | new table | 9 | EasyApp | Signature reference and status; the signed file stays in the Workbench document hub |
| 14 | `iam_group` | new table | 7 | Entra ID | Group-to-role mapping; ACE performs the sign-in |
| 15 | `account` | 7 new columns | 7 | ALS | `business_unit`, `principal_outstanding`, `interest_outstanding`, `fees_outstanding`, `daily_bucket`, `settlement_booked_date`, `settlement_booked_amount` |
| 16 | `customer` | 3 new columns | 3 | SCBPDM | `party_type`, `id_type`, `segment` |
| 17 | `efs_action` | 2 new columns | 2 | EFS | `contact_result`, `action_contact_status` |

Every Tier 2 table carries `source_system`, `business_date` and `loaded_at`, so the Workbench can always say where a row came from and how old it is. Every Tier 2 table has an ACE business key with a unique constraint, because the Workbench links to it by key.

Full list with type, nullability, source field and LDM field ID: **Recovery Workbench ACE Field Gap List v1.xlsx**, sheet `ACE additions`.

## 4. Tier 3 - recovery extension tables, Workbench-owned, keyed by ACE business keys

One-to-one tables. They hold Workbench decisions about an ACE record and never a copy of it. They carry the seven standard record columns.

| Table | Key | Columns | Holds |
|---|---|---|---|
| `recovery.party_ext` | `person_key varchar(255)` | `vulnerable`, `deceased_override`, `bankruptcy`, `fraud_flag` | Workbench flags about an ACE customer |
| `recovery.contact_point_ext` | `contact_key varchar(255)` + `contact_type` | `consent_given`, `consent_at`, `verified_at`, `failed_count`, `source` | Consent and contact quality for a phone, email or address |
| `recovery.account_ext` | `account_key varchar(255)` | `dispute_open` | Workbench state about an ACE account |
| `recovery.valuation_ext` | `valuation_key varchar(255)` | `accepted`, `accepted_at`, `accepted_by`, `valuer_partner_id`, `stale_flag`, `age_days` | The Workbench's decision about an ACE appraisal |

## 5. Tier 4 - recovery Workbench tables that stay

88 Workbench-owned tables keep their purpose. Their links to source data change from UUID foreign keys to business-key columns.

The 14 surviving foreign keys into a source record become:

| Table | Old column | New column | Type |
|---|---|---|---|
| `recovery_case` | `primary_customer_id` | `primary_person_key` | `varchar(255)` |
| `case_account` | `account_id` | `account_key` | `varchar(255)` |
| `case_party` | `party_id` | `person_key` | `varchar(255)` |
| `notice` | `party_id` | `person_key` | `varchar(255)` |
| `listing` | `asset_id` | `asset_key` | `varchar(255)` |
| `asset_sale` | `asset_id` | `asset_key` | `varchar(255)` |
| `debt_sale_account` | `account_id` | `account_key` | `varchar(255)` |
| `interaction` | `party_id` | `person_key` | `varchar(255)` |
| `interaction` | `contact_point_id` | `contact_key` (composite: contact_type:key) | `varchar(255)` |
| `document` | `party_id` | `person_key` | `varchar(255)` |
| `proceeds` | `account_payment_id` | `payment_code` | `varchar(255)` |
| `case_list_row` | `account_id` | `account_key` | `varchar(255)` |
| `case_entry_exclusion` | `account_id` | `account_key` | `varchar(255)` |
| `signature_request` | `party_id` | `person_key` | `varchar(255)` |

No foreign key is created on any of these columns. Referential integrity is checked by the read model and by reconciliation rule REC-05, not by the database.

## 6. Removed from the physical schema

| Object | Fields | Reason | Where its content goes |
|---|---:|---|---|
| `loan_account` | 24 | Copy of ALS data | `v_ace_account` |
| `account_payment` | 7 | Copy of ALS data | `v_ace_payment` |
| `party` | 13 | Copy of SCBPDM data | `v_ace_customer` plus `party_ext` |
| `contact_point` | 8 | Copy of SCBPDM data | `v_ace_contact` plus `contact_point_ext` |
| `collateral` | 13 | Copy of CCMS data | `v_ace_collateral` and `v_ace_collateral_detail` |
| `account_collateral` | 4 | Copy of CCMS data | `v_ace_collateral`, `collateral_detail.lien_rank` |
| `collections_history` | 10 | Copy of EFS data | `v_ace_efs_action` |
| `party_product` | 6 | Copy of SCBPDM data | `v_ace_party_product` |
| `valuation` | 12 | Moves to ACE | `v_ace_valuation` plus `valuation_ext` |
| `score` | 9 | Moves to ACE | `v_ace_score` |
| `asset` | 15 | ACE already holds the asset | `v_ace_asset` and `v_ace_npa_asset` |
| `load_run` | 20 | No inbound load | ACE batch record |
| `dq_exception` | 11 | No inbound load | ACE ingestion checks; REC-01 to REC-05 for reconciliation |
| `dq_rule` | 12 | No inbound load | ACE ingestion checks |
| `source_field_map` | 11 | No inbound load | STTM v4 and the ACE field appendix |
| `source_code_map` | 8 | No inbound load | ACE ingestion; LOV values from ACE |
| `interface_run` | 12 | Inbound runs leave; outbound runs stay | `outbound_item` and `outbox_delivery` |
| `interface_signoff` | 7 | Inbound runs leave | ACE team sign-off in RWB-ACE-001 |
| `tracker_inventory` | 26 | Excel and SharePoint trackers leave scope | Cutover plan |
| `tracker_row` | 9 | Excel and SharePoint trackers leave scope | Cutover plan |

20 tables and 237 fields leave, plus 6 columns on retained tables (`treatment` 4, `signature_request` 1, `role` 1) that the six fields moved to ACE, 243 fields in all. `interface_config` stays for outbound interfaces only. `data_product_load` stays as the freshness stamp, sourced from `ace_batch_run`. `reconciliation_result` stays and reconciles the case list to `v_ace_account`.

## 7. Carried mappings

Three examples that every downstream document repeats:

| LDM field | Physical today | Source | Read path v5 |
|---|---|---|---|
| `loan_account.days_past_due` | `loan_account.days_past_due` | ALS `DELAY_DAYS` | `v_ace_account.days_past_due` from `public.account.delay_days` |
| `account_payment.payment_date` | `account_payment.payment_date date` | ALS `Payment_Date` | `v_ace_payment.payment_date` from `recovery.ace_to_date(public.payment.pay_date)` |
| `party.cif_no` | `party.cif_no` | SCBPDM `CIF` | `v_ace_customer.cif_no` from `public.customer.person_key` |

Two type rules the views enforce:

- Text dates in ACE (`payment.pay_date`) become `date` through `recovery.ace_to_date`, which returns NULL rather than failing on an unrecognised value.
- Y/N text flags in ACE (`account.is_restructured`, `customer.is_deceased`) become `boolean` through `recovery.ace_to_boolean`.

One masking rule:

- `customer.identification_number` is exposed as `id_no_masked` and `id_no_last4` only. The full value never leaves ACE. Phone, email and address are exposed in full because notices and calls need them; display masking is E1-037 at the API, and every read is audited.

## 8. Counts

| Item | v4 today | v5 target | Arithmetic |
|---|---:|---:|---|
| Workbench tables | 108 | 92 | 108 - 20 removed + 4 extension |
| Views | 0 | 30 | 16 Tier 1 + 14 Tier 2 |
| Dictionary objects (`sys_objects`) | 108 | 122 | 92 tables + 30 views |
| Dictionary fields (`sys_fields`) | 1,256 | 1,366 | 1,256 - 243 removed + 49 extension + 304 view |
| Foreign keys into `public.*` | 0 | 0 | The boundary rule forbids them |
| UUID foreign keys into a source copy | 23 | 0 | 14 re-keyed, 9 leave with their table |

The exact figures are re-derived from the LDM v7 and the Physical Schema v5 pair; if any of them moves, the register and D-RCV-35 are amended in the same pass.

## 9. Rules for every later edit

1. A Workbench table never holds a column that ACE already holds. If the screen needs it, it reads the view.
2. A Workbench table never holds a copy of a source record. A snapshot taken at case entry is allowed and is named `_at_entry`.
3. A link to a source record is a business key with no foreign key.
4. A new source field is either already in ACE (map it) or goes into RWB-ACE-001 (ask the ACE team). It never becomes a Workbench column.
5. A view field is named for the Workbench, not for ACE. The ACE name appears only in the view definition and the STTM.
6. `recovery.v_ace_*` is the only read path. A direct `public.*` read in a story, spec or query is a defect.
