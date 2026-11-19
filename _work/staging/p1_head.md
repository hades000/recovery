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
| Decision | D-RCV-35 (U1 to U5), ADR-010 |

| Version | Date | Change |
|---|---|---|
| 2 | 28 October 2026 | Module specification with COLLINS and file loads, load checks, data quality rules, tracker inventory and the freshness stamp |
| 3 | 15 November 2026 | D-RCV-35: the Workbench loads no source data (U1). T3 is re-drawn around the 30 read-only `recovery.v_ace_*` views, the 4 extension tables keyed by ACE business keys (U3), and freshness read from `v_ace_batch_status`. The 11 source copies, the 9 load, data quality and tracker tables, and the inbound interfaces leave the module. API-P1-003 to API-P1-008 are retired |

| Document | Type | Relationship |
|---|---|---|
| Recovery Workbench FSD P1 Recovery data engine | FSD | Pair |
| Recovery Workbench Target Architecture | Architecture | Parent |
| Recovery Workbench Logical Data Model and Data Dictionary v7 | Data | Source of T3 and the 1,366 dictionary fields |
| Recovery Workbench Physical Schema v5 | Data | Source of the T3 physical types, the extension tables and the views |
| Recovery Workbench ACE Data Tier Map v1 | Data | Frozen table-and-column map, tiers 1 to 4 and the removals |
| Recovery Workbench ACE Source Views v1.sql | Data | The 30 view definitions, the helper functions, the grants and the conformance test |
| Recovery Workbench ACE DB Alignment Change Register v1 | Governance | Decision record for this version |
| Recovery Workbench API Specification | API | Source of appendix T-A |

## Existing capability check

| Capability | Verdict | Owning document | Note |
|---|---|---|---|
| Inbound source data (ALS, SCBPDM, UDP, AAL, EFS, COLLINS, LIT, CCMS, SVAF, AMIS, RPS, WIN, GL, NLEADS, EasyApp, Entra ID) | REUSE | ACE ingestion, RWB-ACE-001 (ACE team) | ACE lands every source row. The Workbench runs no load, no file check, no data quality rule and no sign-off |
| Read path into ACE source data | REUSE | RWB-E1-069, this document | 30 SELECT-only `recovery.v_ace_*` views. No direct `public` read and no write |
| Freshness and the intake trigger | NEW | This document | The stamp is built from `v_ace_batch_status`; ACE owns the batch record |
| Scheduler and batch | REUSE | ACE pattern: Quartz and Spring Batch | No new `qrtz_` or `batch_` table; jobs trigger on the ACE batch-complete record |
| Reconciliation of the case list | NEW | This document | Case list to `v_ace_account` by product group |
| Data dictionary held as data | NEW | This document | 92 tables and 30 views, 1,366 fields |
| Outbox and retry | REUSE | Error Handling and Resilience Standard | Through P2 |
| Rules evaluation | REUSE | Rules Engine Design | Through the rules component |

## T1. Architecture overview

P1 Recovery data engine is part of the recovery module in the ACE service: one service, one repository, one front end. It covers the read model over the ACE views, the four extension tables, freshness, reconciliation, the data dictionary and the publication of the case list. It no longer covers a source load.

The boundary rule frames the module. ACE ingests every source row. The recovery module reads ACE only through `recovery.v_ace_*` SELECT-only views, adds only its own tables and columns, and writes nothing to `public`. There is no foreign key from a Workbench table into ACE, because ACE uses `ON DELETE CASCADE` on `account` and a cascade would delete recovery history. A link to a source record is a business key: `account_key`, `person_key`, `asset_key`, `payment_code`, `contact_key` or `valuation_key`.

P1 reaches other modules only through their published interfaces. It reaches ACE only through the views in T3.1.1.

## T2. Component design

| Component | Responsibility |
|---|---|
| RecoveryDataEngineController | REST endpoints in appendix T-A; validation; maps errors to problem responses |
| RecoveryDataEngineService | Business logic; calls the rules component; writes the decision log entry before any change |
| RecoveryDataEngineRepository | Reads and writes the module's own tables; never a `public` table |
| AceViewReader | The only component in the module that queries `recovery.v_ace_*`; returns read-only records with `data_as_of` |
| FreshnessMonitor | Reads `v_ace_batch_status`, writes the `data_product_load` stamp and publishes AceDataReady or AceDataLate |
| ReconciliationService | Reconciles the case list to `v_ace_account` by product group and writes `reconciliation_result` |
| DictionaryService | Maintains `sys_objects`, `sys_fields`, `sys_field_version` and serves the dictionary screens |
| ExtensionWriter | Writes `party_ext`, `contact_point_ext`, `account_ext` and `valuation_ext`; one row per ACE business key, no copy of ACE data |
| Jobs | Quartz and Spring Batch jobs the module owns; each triggers on an ACE batch-complete record, not on a fixed clock |
| Published interface | Java interface other modules call; no table is read across modules |

The load adapter, the data quality rule engine and the tracker loader of version 2 are removed with their tables. Their checks are now ACE ingestion checks (RWB-ACE-001) or reconciliation rules REC-01 to REC-09.

## T3. Data model

### T3.0 Standard record columns

| Column | Type | Meaning |
|---|---|---|
| is_active | boolean | The active or inactive status of the record |
| state | varchar(40) | Record lifecycle state |
| version | integer | Optimistic lock version |
| created_at | timestamptz | When the record was created |
| created_by | uuid | Who or which service identity created it |
| updated_at | timestamptz | When the record last changed |
| updated_by | uuid | Who or which service identity last changed it |

The 30 ACE views are read-only and carry no standard record columns; their columns are the ACE data as the Workbench reads it. Every Workbench table and every extension table carries the seven columns above.

### T3.1 Object and field definitions

The module's model has three parts:

1. The 30 ACE source views. P1 does not own them; it is the only way P1 reads ACE.
2. The four extension tables. P1 owns them; each is 1:1 with an ACE record, keyed by its business key.
3. The Workbench metadata and operations tables that stay. P1 owns them; they hold the dictionary, the data products, the freshness stamp, reconciliation, retention and the case list snapshot.

#### T3.1.1 ACE source views, the only read path

One view per ACE object family, so a developer is told which view to read and cannot wander into `public`. Section A holds 16 views over tables ACE has today and ships with RWB-E1-069 as V0002. Section B holds 14 views over the RWB-ACE-001 additions and ships as V0003 once the ACE change lands; until then the features that need them stay behind their flags.

Every view is owned by `ace_view_owner`, which holds SELECT on the ACE tables it reads. The recovery service identity holds SELECT on the views and on nothing else in `public`.

| # | View | Section | ACE object or objects read | Key the Workbench links on | What the Workbench reads it for |
|---:|---|---|---|---|---|
| 1 | `v_ace_account` | A, plus B columns | `account`, `product`, `branch` | `account_key` | Account, balances, arrears, days past due, classification, restructure flag, `data_as_of` |
| 2 | `v_ace_payment` | A | `payment`, `account` | `payment_code` | Payments posted to an account, for proceeds matching |
| 3 | `v_ace_customer` | A, plus B columns | `customer` | `person_key` | Party identity, masked to the last four, and vulnerability inputs |
| 4 | `v_ace_contact` | A | `phone`, `email`, `address` (union) | `contact_key` (`contact_type:key`) | Contact point, consent basis, notice address |
| 5 | `v_ace_ca_relation` | A | `ca_relation` | `person_key` and `account_key` | Borrower, guarantor and co-borrower roles |
| 6 | `v_ace_aa_relation` | A | `aa_relation` | `parent_account_key`, `child_account_key` | Parent and child accounts of a grouped facility |
| 7 | `v_ace_collateral` | A | `collateral`, `asset` | `asset_key` | Collateral link, value and type |
| 8 | `v_ace_asset` | A | `asset` | `asset_key` | The collateral asset record |
| 9 | `v_ace_efs_action` | A, plus B columns | `efs_action` | `efs_record_key` | Collections history, contact result and promise |
| 10 | `v_ace_efs_action_code` | A | `efs_action_code` | `action_code` | Action code list, 1,106 values |
| 11 | `v_ace_efs_assignment` | A | `efs_assignment` | `account_key` | Assignment and hand-over history |
| 12 | `v_ace_bucket_log` | A | `bucket_log_snapshot`, `account` | `account_key` | Monthly bucket history |
| 13 | `v_ace_product` | A | `product` | `product_code` | Product and product group lists |
| 14 | `v_ace_branch` | A | `branch` | `branch_code` | Branch and region lists |
| 15 | `v_ace_holiday` | A | `bot_holiday` | `holiday_date` | Service level and legal-day calendar |
| 16 | `v_ace_plan` | A | `ace_case`, `cfsc_mg_ssme_tdr_case`, `tdr_calculation`, `ai_recommended_plan`, `account` | `plan_ref` | Plan reference, status, booking and approval dates, published calculation |
| 17 | `v_ace_batch_status` | B | `ace_batch_run` | `source_system` and `business_date` | Freshness, record count and the intake trigger |
| 18 | `v_ace_valuation` | B | `valuation` | `valuation_key` | SVAF appraisal number, values and date |
| 19 | `v_ace_collateral_detail` | B | `collateral_detail` | `asset_key` | Title deed, plot, area, location, insurance and lien rank |
| 20 | `v_ace_npa_asset` | B | `npa_asset` | `asset_key` | NPA asset, transfer in, book value and auction price |
| 21 | `v_ace_npa_sale` | B | `npa_sale` | `npa_sale_key` | NPA sale contract, taxes, fees and incentive |
| 22 | `v_ace_lawsuit` | B | `lawsuit` | `lawsuit_key` | Court case numbers, claim, judgment and status |
| 23 | `v_ace_hearing` | B | `hearing` | `hearing_key` | Hearing date, type and next date |
| 24 | `v_ace_pod` | B | `pod_receipt` | `pod_key` | Proof of delivery for a notice |
| 25 | `v_ace_write_off` | B | `gl_write_off` | `write_off_key` | GL write-off posting, cost centre and GL product |
| 26 | `v_ace_score` | B | `collins_score` | `score_key` | COLLINS score, estimate and route |
| 27 | `v_ace_party_product` | B | `party_product` | `person_key` and `account_key` | Customer product holding |
| 28 | `v_ace_credit_decision` | B | `credit_decision` | `credit_decision_key` | NLEADS credit result, reason and decision date |
| 29 | `v_ace_esign` | B | `esign_request` | `esign_key` | EasyApp signature request and status |
| 30 | `v_ace_iam_group` | B | `iam_group` | `entra_group` | Group-to-role mapping used at sign-in |

Two rules apply to every view:

- A view field is named for the Workbench, not for ACE. The ACE name appears only in the view definition and the STTM. `account.delay_days` becomes `days_past_due`; `payment.pay_date` becomes `payment_date` through `ace_to_date`; `customer.person_key` becomes `cif_no` and `person_key`.
- A view casts and masks; it does not decide. `ace_to_date` returns NULL on an unrecognised text date. `ace_to_boolean` turns Y/N into boolean. `v_ace_customer` exposes `id_no_masked` and `id_no_last4` only; the clear identity number never leaves ACE. `v_ace_contact.contact_value` is in full because notices and calls need it, and display masking is E1-037 at the API.

Section B adds 12 columns to views that already exist, through `CREATE OR REPLACE VIEW` in V0003: `v_ace_account` gains `business_unit`, `principal_outstanding`, `interest_outstanding`, `fees_outstanding`, `daily_bucket`, `settlement_booked_date` and `settlement_booked_amount`; `v_ace_customer` gains `party_type`, `id_type` and `segment`; `v_ace_efs_action` gains `contact_result` and `action_contact_status`. A feature that reads one of the 12 stays behind its flag until V0003 is applied.

The full field list of every view, with types and BR field IDs DF-ACE-001 to DF-ACE-304, is in Logical Data Model and Data Dictionary v7. The view definition is the contract: a change to a column a view reads is a change to that contract.

#### T3.1.2 Extension tables

Each extension table holds Workbench decisions about an ACE record and never a copy of it. The row exists only while the Workbench has something to say about the ACE record; a missing row means the defaults (no flag set, no consent recorded, no acceptance). No existing ACE table is altered.

**party_ext** (NEW). Workbench flags about an ACE customer, keyed by `person_key`. A 1:1 table.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-EXT-001 | person_key | TEXT | varchar(255) | Yes | None | ACE `v_ace_customer.person_key` |
| DF-EXT-002 | vulnerable | BOOLEAN | boolean | Yes | None | Workbench |
| DF-EXT-003 | deceased_override | BOOLEAN | boolean | Yes | None | Workbench |
| DF-EXT-004 | bankruptcy | BOOLEAN | boolean | Yes | None | Workbench |
| DF-EXT-005 | fraud_flag | BOOLEAN | boolean | Yes | None | Workbench |

Plus the seven standard record columns in T3.0, DF-EXT-006 to DF-EXT-012. `deceased_override` is set only when a person confirms a death that the ACE record does not show; `deceased_flag` itself is read from `v_ace_customer`.

**contact_point_ext** (NEW). Consent and contact quality for an ACE phone, email or address, keyed by `contact_key`. A 1:1 table.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-EXT-013 | contact_key | TEXT | varchar(255) | Yes | None | ACE `v_ace_contact.contact_key` |
| DF-EXT-014 | contact_type | LOV | varchar(10) | Yes | LOV-CONTACT-TYPE | ACE `v_ace_contact.contact_type` |
| DF-EXT-015 | consent_given | BOOLEAN | boolean | Yes | None | Workbench |
| DF-EXT-016 | consent_at | DATE | timestamptz | No | None | Workbench |
| DF-EXT-017 | verified_at | DATE | timestamptz | No | None | Workbench |
| DF-EXT-018 | failed_count | NUMBER | integer | Yes | None | Workbench |
| DF-EXT-019 | source | TEXT | varchar(20) | Yes | None | Workbench |

Plus the seven standard record columns, DF-EXT-020 to DF-EXT-026. The primary key is `contact_key`, so a phone, email and address row cannot collide.

**account_ext** (NEW). Workbench state about an ACE account, keyed by `account_key`. A 1:1 table.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-EXT-027 | account_key | TEXT | varchar(255) | Yes | None | ACE `v_ace_account.account_key` |
| DF-EXT-028 | dispute_open | BOOLEAN | boolean | Yes | None | Workbench |

Plus the seven standard record columns, DF-EXT-029 to DF-EXT-035. `dispute_open` was `loan_account.dispute_open` before D-RCV-35.

**valuation_ext** (NEW). The Workbench decision about an ACE appraisal, keyed by `valuation_key`. A 1:1 table.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-EXT-036 | valuation_key | TEXT | varchar(255) | Yes | None | ACE `v_ace_valuation.valuation_key` |
| DF-EXT-037 | accepted | BOOLEAN | boolean | Yes | None | Workbench |
| DF-EXT-038 | accepted_at | DATE | timestamptz | No | None | Workbench |
| DF-EXT-039 | accepted_by | CROSS_REF | uuid | No | None | Workbench |
| DF-EXT-040 | valuer_partner_id | CROSS_REF | uuid | No | None | Workbench |
| DF-EXT-041 | stale_flag | BOOLEAN | boolean | Yes | None | Workbench |
| DF-EXT-042 | age_days | NUMBER | integer | No | None | Workbench |

Plus the seven standard record columns, DF-EXT-043 to DF-EXT-049. `stale_flag` and `age_days` are computed daily from `v_ace_valuation.appraisal_date`.

#### T3.1.3 Workbench metadata and operations tables

**data_product** (KEPT). One of the 14 data products, with its single system of record, owner and refresh cycle. Seven name ACE as the system of record, ingested from the source; seven name the Workbench.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-REF-070 | id | TEXT | uuid | Yes | None | Workbench |
| DF-REF-071 | product_code | LOV | varchar(25) | Yes | LOV-DATA-PRODUCT | Workbench |
| DF-REF-072 | product_name | TEXT | varchar(80) | Yes | None | Workbench |
| DF-REF-073 | definition | TEXT | varchar(400) | Yes | None | Workbench |
| DF-REF-074 | system_of_record | TEXT | varchar(120) | Yes | None | Workbench |
| DF-REF-075 | owner_role | LOV | varchar(20) | Yes | LOV-ROLE | Workbench |
| DF-REF-076 | owner_user_id | USER_REF | uuid | No | None | Workbench |
| DF-REF-077 | refresh_cycle | LOV | varchar(30) | Yes | LOV-REFRESH | Workbench |
| DF-REF-078 | expected_by | TEXT | varchar(20) | No | None | Workbench |
| DF-REF-079 | valid_from | DATE | date | Yes | None | Workbench |

`system_of_record` reads "ACE (ingested from ALS)" or "Recovery Workbench". `refresh_cycle` is `varchar(30)` so "By versioned load" fits (DEF-02).

**data_product_access** (KEPT). Which role may read which data product, by version.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-REF-080 | id | TEXT | uuid | Yes | None | Workbench |
| DF-REF-081 | product_code | LOV | varchar(25) | Yes | LOV-DATA-PRODUCT | Workbench |
| DF-REF-082 | role_code | LOV | varchar(20) | Yes | LOV-ROLE | Workbench |
| DF-REF-083 | can_read | BOOLEAN | boolean | Yes | None | Workbench |
| DF-REF-084 | access_version | TEXT | varchar(20) | Yes | None | Workbench |
| DF-REF-085 | valid_from | DATE | date | Yes | None | Workbench |
| DF-REF-086 | valid_to | DATE | date | No | None | Workbench |

**data_product_load** (KEPT). The freshness stamp of a data product for one ACE business date. It is the only stamp the Workbench holds; it is built from `v_ace_batch_status` and never from a file.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-OPS-001 | id | TEXT | uuid | Yes | None | Workbench |
| DF-OPS-002 | product_code | LOV | varchar(25) | Yes | LOV-DATA-PRODUCT | Workbench |
| DF-OPS-003 | source_system | TEXT | varchar(40) | Yes | None | ACE `v_ace_batch_status.source_system` |
| DF-OPS-004 | business_date | DATE | date | Yes | None | ACE `v_ace_batch_status.business_date` |
| DF-OPS-005 | source_extracted_at | DATE | timestamptz | Yes | None | ACE `v_ace_batch_status.completed_at` |
| DF-OPS-006 | loaded_at | DATE | timestamptz | Yes | None | Workbench, when the stamp was written |
| DF-OPS-007 | status | LOV | varchar(10) | Yes | LOV-FRESHNESS | Workbench, from `v_ace_batch_status.is_complete` |
| DF-OPS-008 | stale_flagged_at | DATE | timestamptz | No | None | Workbench |
| DF-OPS-009 | duplicate_count | NUMBER | integer | Yes | None | ACE `v_ace_batch_status.record_count` against the view count |

One row per product and business date. A product is STALE when its ACE batch is incomplete, late or failed; the monitor raises AceDataLate and the case screens show the last good date.

**data_contract** (KEPT). A versioned data contract with the ACE team for one view family or outbound interface, confirmed by the ACE team lead.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-OPS-010 | id | TEXT | uuid | Yes | None | Workbench |
| DF-OPS-011 | contract_code | TEXT | varchar(20) | Yes | None | Workbench |
| DF-OPS-012 | source_system | TEXT | varchar(80) | Yes | None | Workbench |
| DF-OPS-013 | interface_id | TEXT | varchar(40) | Yes | None | Workbench |
| DF-OPS-014 | contract_version | NUMBER | integer | Yes | None | Workbench |
| DF-OPS-015 | status | LOV | varchar(10) | Yes | LOV-CONTRACT-STATUS | Workbench |
| DF-OPS-016 | confirmed_by_role | TEXT | varchar(80) | No | None | Workbench |
| DF-OPS-017 | confirmed_on | DATE | date | No | None | Workbench |
| DF-OPS-018 | confirmation_document_ref | ATTACHMENT | varchar(400) | No | None | Workbench |
| DF-OPS-019 | published_at | DATE | timestamptz | No | None | Workbench |
| DF-OPS-020 | published_by | USER_REF | uuid | No | None | Workbench |

`interface_id` holds the interface code (INT-01 to INT-34) or the view family it covers, for example `v_ace_valuation`. The ACE team's acceptance of RWB-ACE-001 is the contract for Section B.

**sys_objects** (KEPT). The metadata registry of entities: one row per object in the data dictionary, 92 tables and 30 views.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-REF-087 | id | TEXT | uuid | Yes | None | Workbench |
| DF-REF-088 | object_name | TEXT | varchar(60) | Yes | None | Workbench |
| DF-REF-089 | business_name | TEXT | varchar(120) | Yes | None | Workbench |
| DF-REF-090 | subject_area | TEXT | varchar(10) | Yes | None | Workbench |
| DF-REF-091 | data_product | TEXT | varchar(10) | Yes | None | Workbench |
| DF-REF-092 | system_of_record | TEXT | varchar(120) | Yes | None | Workbench |
| DF-REF-093 | description | TEXT | varchar(400) | Yes | None | Workbench |

**sys_fields** (KEPT). The metadata registry of fields: the data dictionary held as data, 1,366 rows.

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
| DF-REF-107 | owner_role | LOV | varchar(20) | No | None | Workbench |
| DF-REF-108 | refresh_cycle | TEXT | varchar(30) | No | None | Workbench |
| DF-REF-109 | late_behavior | TEXT | varchar(200) | No | None | Workbench |
| DF-REF-110 | interface_id | TEXT | varchar(10) | No | None | Workbench |

**sys_field_version** (KEPT). Each version of a field definition, kept when the definition changes.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-REF-111 | id | TEXT | uuid | Yes | None | Workbench |
| DF-REF-112 | field_id | TEXT | varchar(16) | Yes | None | Workbench |
| DF-REF-113 | field_version | NUMBER | integer | Yes | None | Workbench |
| DF-REF-114 | definition | TEXT | jsonb | Yes | None | Workbench |
| DF-REF-115 | change_reason | TEXT | varchar(400) | Yes | None | Workbench |

**reconciliation_result** (KEPT). The daily reconciliation of the case list to `v_ace_account` by product group. `source_count` and `source_amount` are read from the view, not from a loaded copy.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-OPS-118 | id | TEXT | uuid | Yes | None | Workbench |
| DF-OPS-119 | rec_code | TEXT | varchar(6) | Yes | None | Workbench |
| DF-OPS-120 | business_date | DATE | date | Yes | None | Workbench |
| DF-OPS-121 | product_group | LOV | varchar(15) | Yes | LOV-PRODUCT | Workbench |
| DF-OPS-122 | source_count | NUMBER | integer | Yes | None | ACE `v_ace_account` |
| DF-OPS-123 | workbench_count | NUMBER | integer | Yes | None | Workbench |
| DF-OPS-124 | source_amount | NUMBER | numeric(18,2) | No | None | ACE `v_ace_account.total_balance` |
| DF-OPS-125 | workbench_amount | NUMBER | numeric(18,2) | No | None | Workbench |
| DF-OPS-126 | variance_count | NUMBER | integer | Yes | None | Workbench |
| DF-OPS-127 | variance_pct | NUMBER | numeric(9,4) | Yes | None | Workbench |
| DF-OPS-128 | tolerance_pct | NUMBER | numeric(9,4) | Yes | None | Workbench |
| DF-OPS-129 | result | LOV | varchar(8) | Yes | LOV-REC-RESULT | Workbench |

**lake_copy_watermark** (KEPT). How far a copy to the data lake has reached, for example the decision log copy.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-OPS-130 | id | TEXT | uuid | Yes | None | Workbench |
| DF-OPS-131 | copy_name | TEXT | varchar(40) | Yes | None | Workbench |
| DF-OPS-132 | last_entry_hash | TEXT | char(64) | No | None | Workbench |
| DF-OPS-133 | last_decided_at | DATE | timestamptz | No | None | Workbench |
| DF-OPS-134 | rows_copied_total | NUMBER | bigint | Yes | None | Workbench |
| DF-OPS-135 | business_date | DATE | date | No | None | Workbench |

**retention_rule** (KEPT). How long rows of a table or a retention class are kept and what happens at the end, by version.

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

A retention rule may name a view in `table_name`; the rule then applies to the Workbench rows that copy nothing from it, never to ACE.

**case_list_row** (KEPT). One row of the daily case list per case account and business date, published to Power BI. `account_key` replaces the `account_id` foreign key.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-RPT-001 | id | TEXT | uuid | Yes | None | Workbench |
| DF-RPT-002 | business_date | DATE | date | Yes | None | Workbench |
| DF-RPT-003 | case_id | CROSS_REF | uuid | Yes | None | Workbench |
| DF-RPT-004 | case_no | TEXT | varchar(18) | Yes | None | Workbench |
| DF-RPT-005 | account_key | TEXT | varchar(255) | Yes | None | ACE `v_ace_account.account_key` |
| DF-RPT-006 | account_no | TEXT | varchar(20) | Yes | None | ACE `v_ace_account.account_code` |
| DF-RPT-007 | product_group | LOV | varchar(15) | Yes | LOV-PRODUCT | Workbench |
| DF-RPT-008 | stage_code | LOV | varchar(20) | No | LOV-STAGE | Workbench |
| DF-RPT-009 | status | LOV | varchar(20) | Yes | LOV-CASE-STATUS | Workbench |
| DF-RPT-010 | owner_user_id | USER_REF | uuid | No | None | Workbench |
| DF-RPT-011 | queue_code | TEXT | varchar(30) | No | None | Workbench |
| DF-RPT-012 | team_code | LOV | varchar(20) | No | LOV-TEAM | Workbench |
| DF-RPT-013 | route_code | LOV | varchar(4) | No | LOV-ROUTE | Workbench |
| DF-RPT-014 | total_balance | NUMBER | numeric(18,2) | Yes | None | ACE `v_ace_account.total_balance` |
| DF-RPT-015 | days_past_due | NUMBER | integer | Yes | None | ACE `v_ace_account.days_past_due` |
| DF-RPT-016 | refreshed_at | DATE | timestamptz | Yes | None | Workbench |
| DF-RPT-017 | last_contact_at | DATE | timestamptz | No | None | ACE `v_ace_efs_action.contact_at` |
| DF-RPT-018 | last_action_code | LOV | varchar(10) | No | None | ACE `v_ace_efs_action.action_code` |
| DF-RPT-019 | publish_status | LOV | varchar(10) | Yes | None | LOV-PUBLISH-STATUS |

**dp_treatment** (KEPT). The snapshot of each treatment for a business date in the DP04 data product. It is a Workbench reporting snapshot, not a source copy.

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
| DF-TRT-045 | approval_level | LOV | varchar(4) | No | None | LOV-APPROVAL-LEVEL |
| DF-TRT-046 | booked_at | DATE | timestamptz | No | None | Workbench |
| DF-TRT-047 | outcome | LOV | varchar(12) | No | LOV-TRT-OUTCOME | Workbench |
| DF-TRT-048 | outcome_at | DATE | timestamptz | No | None | Workbench |
| DF-TRT-049 | business_date | DATE | date | Yes | None | Workbench |
| DF-TRT-050 | contract_no | TEXT | varchar(20) | No | None | DEF-05 snapshot; live value in `v_ace_account.contract_no` |
| DF-TRT-051 | contract_date | DATE | date | No | None | DEF-05 snapshot; live value in `v_ace_account.contract_date` |

`contract_no` and `contract_date` are the DEF-05 carried snapshot. The live values are read from `v_ace_account`; the owning story either drops the two columns or states why the snapshot is kept.

**dp_guarantee_claim** (KEPT). The snapshot of each guarantee claim for a business date in the DP04 data product.

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

The 20 tables that leave P1 are listed in the Tier Map section 6: the 11 source copies (`loan_account`, `account_payment`, `party`, `contact_point`, `collateral`, `account_collateral`, `collections_history`, `party_product`, `valuation`, `score`, `asset`) and the 9 load, data quality and tracker tables (`load_run`, `dq_exception`, `dq_rule`, `source_field_map`, `source_code_map`, `interface_run`, `interface_signoff`, `tracker_inventory`, `tracker_row`). Their field IDs are retired and are not reused.

### T3.2 Lists of values

| List | Values |
|---|---|
| LOV-APPROVAL-LEVEL | L1, L2, L3, L4, L5, L6 |
| LOV-CASE-STATUS | NEW, ASSIGNED, IN_PROGRESS, WAITING_CUSTOMER, WAITING_PARTNER, WAITING_APPROVAL, ON_HOLD, CLOSED |
| LOV-CLAIM-STATUS | PREPARING, FILED, DEFECT, PAID, REJECTED |
| LOV-CLAIM-TYPE | TCG, CREDIT_LIFE_INSURANCE, MORTGAGE_INSURANCE, COLLATERAL_INSURANCE |
| LOV-CONTRACT-STATUS | DRAFT, PUBLISHED, SUPERSEDED |
| LOV-CONTACT-TYPE | PHONE, EMAIL, ADDRESS |
| LOV-DATA-PRODUCT | DP01, DP02, DP03, DP04, DP05, DP06, DP07, DP08, DP09, DP10, DP11, DP12, DP13, DP14 |
| LOV-FRESHNESS | LOADED, STALE |
| LOV-PRODUCT | MORTGAGE, HIRE_PURCHASE, SSME, UNSECURED |
| LOV-PROPOSER | AGENT, RULE, PERSON |
| LOV-PUBLISH-STATUS | PENDING, HELD, RELEASED |
| LOV-REC-RESULT | PASS, BREAK |
| LOV-REFRESH | DAILY, WEEKLY, MONTHLY, ON_CHANGE, BY_VERSION |
| LOV-RETENTION-END | ARCHIVE, REVIEW |
| LOV-ROLE | The roles in the Admin and Access Model |
| LOV-ROUTE | R1, R2, R3, R4, R5, R6, R7, R8 |
| LOV-STAGE | RESTRUCTURE, SETTLEMENT, DEED_IN_LIEU, GUARANTEE_CLAIM, LITIGATION, ASSET_DISPOSAL, DEBT_SALE, WRITE_OFF, DEVIATIONS |
| LOV-TREATMENT | RESTRUCTURE, SETTLEMENT, DEED_IN_LIEU, BUY_BACK, GUARANTEE_CLAIM, REPOSSESSION, AUCTION, DEBT_SALE, WRITE_OFF, RAMC_TRANSFER, RENTAL |
| LOV-TRT-OUTCOME | KEPT, BROKEN, COMPLETED, CANCELED, DECLINED |

Six lists leave with their tables: LOV-DQ-RULE-TYPE, LOV-DQ-STATUS, LOV-LOAD-STATUS, LOV-TRACKER-DECISION, LOV-TRACKER-LOCATION, LOV-TRACKER-STATUS and LOV-UPDATE-CYCLE. The reference values that came from a loaded list, such as product, branch, action code and holiday, are read from their ACE view.

### T3.3 Relationships

| From | Field | To | Cardinality |
|---|---|---|---|
| party_ext | person_key | v_ace_customer | One to one, business key, no foreign key |
| contact_point_ext | contact_key | v_ace_contact | One to one, business key, no foreign key |
| account_ext | account_key | v_ace_account | One to one, business key, no foreign key |
| valuation_ext | valuation_key | v_ace_valuation | One to one, business key, no foreign key |
| case_list_row | case_id | recovery_case | Many to 1 |
| case_list_row | account_key | v_ace_account | Many to 0 or 1, business key, no foreign key |
| retention_rule | reference_version_id | reference_version | Many to 0 or 1 |
| dp_treatment | treatment_id | treatment | Many to 1 |
| dp_treatment | case_id | recovery_case | Many to 1 |
| dp_treatment | decision_log_id | decision_log_entry | Many to 0 or 1 |
| dp_guarantee_claim | guarantee_claim_id | guarantee_claim | Many to 1 |
| dp_guarantee_claim | case_id | recovery_case | Many to 1 |

No relationship in this table is a foreign key into ACE. The 14 re-keyed foreign keys of the retained tables are listed in the Tier Map section 5 and are owned by the module that holds the table.

