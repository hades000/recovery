# RWB-ACE-001 ACE DB additions for the Recovery Workbench

SCB Collections and Recovery. Henka Group, 15 November 2026.

(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ACE-001 |
| Owner | ACE team |
| Epic | ACE backlog, release 30 November 2026 |
| Module | ACE ingestion and schema |
| Feature | FEAT-RDF-26 ACE DB additions (ACE team) |
| Requirement IDs | REQ-RDF-001, REQ-RDF-002 |
| Decision | D-RCV-35 (U1, U2); DL43 |
| Priority | Must - critical path for the 30 November release |
| Depends on | None. This story is first on the recovery critical path |
| Blocks | RWB-E1-069, RWB-E1-002, RWB-E1-016, RWB-E1-018, every Tier 2 feature |
| Status | Ready for the ACE team estimate (DL43) |

## 1. Story

As the **ACE team lead**, I want **the tables and columns that the recovery module needs but ACE does not hold added to the ACE database, ingested by the existing ACE ingestion and recorded with a business date**, so that **the recovery module reads one copy of source data through its views, and no recovery load or staging table is built**.

## 2. Business rationale

The recovery module reads source data from ACE (D-RCV-35, ADR-010). ACE already holds account, payment, customer, contact, collateral, the collateral asset, collections activity, assignment, bucket history, product, branch and holiday. It does not hold the appraisal, the CCMS collateral detail, the NPA asset and sale, the lawsuit and hearing, the proof of delivery, the GL write-off, the COLLINS score, the SCBPDM product holding, the NLEADS credit decision, the EasyApp signature reference or the Entra group mapping. It also lacks a per-source business date record and 12 columns on account, customer and efs_action.

This story adds exactly that: 14 tables, 12 columns and the batch record. It is the single dependency that unblocks the recovery data engine, and it is why DL43 is the top item on the programme risk log. Every field is listed in appendix A with its source, type and frequency, so the estimate is a table read, not a discovery.

## 3. Preconditions

- The ACE schema is at the common migration head (V026 at the time of writing).
- The ACE ingestion framework accepts a new source: a file or API contract, a staging-to-target mapper, a batch record writer and a unique business key per target table.
- The ACE DBA role that owns the schema is available for the migration window.
- The recovery role name and the view-owner role name are agreed with the Workbench environment design.
- Each source owner has confirmed the field list in appendix A: SVAF, CCMS, AMIS, RPS, LIT, WIN, GL, COLLINS, SCBPDM, NLEADS, EasyApp and the Entra ID administrator.

## 4. Flow

1. ACE team: applies migration `V027__rwb_ace_001_recovery_source_additions.sql` in DEV. It creates 14 tables and adds 12 columns in one transaction.
2. ACE team: adds one ingestion job per source, each writing its target table and one `ace_batch_run` row per source and business date.
3. ACE team: runs the population check (AC2) against one full file per source, comparing the row count with the trailer.
4. ACE team: runs the ACE regression suite (AC6) and confirms no existing screen, job or report changes.
5. ACE DBA: grants SELECT on the listed tables to the view-owner role, and nothing else (AC4).
6. Recovery squad: creates the Section B views in RWB-E1-069 and reads them.
7. ACE team: repeats steps 1 to 5 in SIT, then PROD in the release window.

## 5. Exception paths

| ID | Trigger | What happens | Covered by |
|---|---|---|---|
| X1 | A source file fails its trailer or checksum | The ingestion writes no row for that source and business date; `ace_batch_run` keeps the previous COMPLETED row as the latest | AC3 |
| X2 | A field in appendix A has no column after the migration | The conformance test fails and names the field ID | AC8 |
| X3 | A source re-sends a business date already loaded | The unique business key rejects the duplicate; the batch record keeps one row for that source and date | AC7 |
| X4 | A new column would change an existing ACE column type | The migration is rejected at review; new columns are additive only | AC1, AC6 |
| X5 | The view-owner role is granted more than SELECT | The grant check fails the security review | AC4 |
| X6 | The migration must be backed out | The down script drops the 14 tables and the 12 columns; no ACE row is touched | AC5 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs nothing from the recovery module; it is the first item on the critical path |
| Negotiable | The field list is fixed by appendix A; the ingestion design is the ACE team's choice |
| Valuable | Removes 14 tables and a load estate from the Workbench, and gives ACE one more complete source set |
| Estimable | 14 tables, 12 columns, 14 ingestion jobs, one grant, one conformance test |
| Small | One migration plus the ingestion jobs; the ACE team sizes it in DL43 |
| Testable | Eight criteria, each one automated test |

## 7. Acceptance criteria

```gherkin
Feature: ACE DB additions for the Recovery Workbench

  Scenario: AC1 Tables and columns deployed
    Given the ACE schema at the common migration head
    When the ACE team applies V027__rwb_ace_001_recovery_source_additions.sql in DEV and then in SIT
    Then public holds the 14 new tables of section 11
    Then account holds 7 new columns, customer 3 and efs_action 2
    Then ace_batch_run has a primary key and the unique key (source_system, business_date)
    Then no existing ACE column is renamed, retyped or dropped

  Scenario: AC2 Every Workbench field is populated
    Given one full source file for each source in appendix A
    When ACE ingests each file for business date 2026-11-30
    Then all 80 appendix A fields hold a value or an explicit null
    Then the row count per target table equals the file trailer count

  Scenario: AC3 Business date and completion recorded
    Given the ALS file for 2026-11-30 is ingested and completes at 04:40
    When the recovery module reads v_ace_batch_status
    Then it returns ALS, 2026-11-30, COMPLETED, the record count and the completion time
    Then a failed run for 2026-12-01 leaves 2026-11-30 as the latest COMPLETED row for ALS

  Scenario: AC4 Read grant only
    Given the view-owner role agreed with the Workbench environment design
    When the ACE DBA applies the grant script
    Then the role may select the 14 new tables and no other table
    Then the 12 new columns on account, customer and efs_action are covered by the existing Tier 1 grant
    Then the role may not insert, update, delete or truncate any table

  Scenario: AC5 Reversible
    Given a copy of PROD with the migration applied
    When the down script runs
    Then the 14 tables and the 12 columns are gone
    Then account, payment, customer and efs_action row counts are unchanged

  Scenario: AC6 Existing ACE reads unaffected
    Given the ACE regression suite
    When it runs after the migration
    Then every existing screen, batch job and report passes
    Then the row counts of account, payment, customer and efs_action are unchanged

  Scenario: AC7 Idempotent reload
    Given a source file already ingested for 2026-11-30
    When the same file is ingested again
    Then no duplicate row is created
    Then ace_batch_run holds one row for that source and business date

  Scenario: AC8 Field appendix matches the migration
    Given the 80 rows of appendix A
    When the conformance test compares them with the deployed columns
    Then 80 of 80 resolve to a column of the right type
    Then no appendix row is missing and no extra mapped column exists
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every table carries `source_system`, `business_date` and `loaded_at`; the business date is the source business date, not the ingest date | D-RCV-35 U2; E1-015 |
| BR2 | Every table has a business key with a unique constraint; the Workbench links by that key and never by a generated id | D-RCV-35 U4 |
| BR3 | New columns on existing ACE tables are additive only; no existing column is renamed, retyped or dropped | D-RCV-35 U3 |
| BR4 | The batch record is one row per source and business date, written even when the source delivers zero rows | E1-015; E1-016 |
| BR5 | Selective grant: the view-owner role reads the listed tables and writes nothing | D-RCV-35 U4; CTL-02 |
| BR6 | A field is in this story only if the Workbench needs it; a field the Workbench does not read is not added | appendix A |

## 9. State transitions

None on a case. This story changes the ACE schema version (V026 to V027) and the ingestion job set (14 jobs added).

## 10. Authority

| Who | What they may do in this story |
|---|---|
| ACE team lead | Owns the story, the estimate and DL43 |
| ACE DBA | Applies the migration and the grant |
| ACE ingestion owner | Adds and schedules the 14 jobs |
| View-owner role | Selects the 21 listed tables; writes nothing |
| Recovery squad | Reads the views only; has no grant on a public table |

## 11. Data

### 11.1 New tables

| Table | Columns | Source | Business key | Fields read by the Workbench |
|---|---:|---|---|---:|
| `ace_batch_run` | 9 | All sources | `(source_system, business_date)` | 0 |
| `valuation` | 11 | SVAF | `valuation_key` | 5 |
| `collateral_detail` | 15 | CCMS | `collateral_detail_key` | 9 |
| `npa_asset` | 14 | AMIS, RPS | `npa_asset_key` | 8 |
| `npa_sale` | 13 | AMIS | `npa_sale_key` | 7 |
| `lawsuit` | 15 | LIT | `lawsuit_key` | 9 |
| `hearing` | 9 | LIT | `hearing_key` | 3 |
| `pod_receipt` | 12 | WIN | `pod_key` | 5 |
| `gl_write_off` | 11 | GL | `write_off_key` | 5 |
| `collins_score` | 12 | COLLINS | `score_key` | 6 |
| `party_product` | 7 | SCBPDM | `(person_key, account_key, product_type, business_date)` | 4 |
| `credit_decision` | 10 | NLEADS | `credit_decision_key` | 4 |
| `esign_request` | 9 | EasyApp | `esign_key` | 1 |
| `iam_group` | 7 | Entra ID | `(entra_group, role_code)` | 1 |

### 11.2 New columns on existing tables

| Table | Column | Type | Source | Field ID |
|---|---|---|---|---|
| `account` | `business_unit` | varchar(10) | ALS | DF-ACC-006 |
| `account` | `principal_outstanding` | numeric(18,2) | ALS | DF-ACC-009 |
| `account` | `interest_outstanding` | numeric(18,2) | ALS | DF-ACC-010 |
| `account` | `fees_outstanding` | numeric(18,2) | ALS | DF-ACC-011 |
| `account` | `daily_bucket` | varchar(10) | ALS | DF-ACC-015 |
| `account` | `settlement_booked_date` | date | ALS | DF-ACC-030 |
| `account` | `settlement_booked_amount` | numeric(18,2) | ALS | DF-ACC-031 |
| `customer` | `party_type` | varchar(15) | SCBPDM | DF-PTY-003 |
| `customer` | `id_type` | varchar(20) | SCBPDM | DF-PTY-006 |
| `customer` | `segment` | varchar(20) | SCBPDM | DF-PTY-009 |
| `efs_action` | `contact_result` | varchar(20) | EFS | DF-INT-008, DF-INT-036 |
| `efs_action` | `action_contact_status` | varchar(20) | EFS | DF-INT-035 |

### 11.3 The 80 fields

Full table, with source field and frequency, is appendix A of this file and sheet `Fields` of the xlsx.

| Table | Fields | Source |
|---|---:|---|
| `customer` | 3 | SCBPDM |
| `account` | 7 | ALS |
| `collateral_detail` | 9 | CCMS |
| `valuation` | 5 | SVAF |
| `npa_asset` | 8 | AMIS, RPS |
| `credit_decision` | 4 | NLEADS |
| `lawsuit` | 9 | LIT |
| `pod_receipt` | 5 | WIN |
| `hearing` | 3 | LIT |
| `npa_sale` | 7 | AMIS |
| `efs_action` | 3 | EFS |
| `collins_score` | 6 | COLLINS |
| `gl_write_off` | 5 | GL |
| `iam_group` | 1 | Entra ID |
| `party_product` | 4 | SCBPDM |
| `esign_request` | 1 | EasyApp |

## 12. Solution plan

1. Migration `V027__rwb_ace_001_recovery_source_additions.sql`: 14 `CREATE TABLE`, 12 `ALTER TABLE ... ADD COLUMN`, the primary keys, the business-key unique constraints and the foreign keys to `account`, `asset`, `customer`, `npa_asset` and `lawsuit` as shown in section 11.
2. Ingestion: one Spring Batch job per source; a shared `BatchRecordWriter` writes `ace_batch_run` once per run.
3. Mapper: one class per source, generated from the STTM v4 gap sheet, with the type casts in section 11.
4. Grant script: `SELECT` on the 21 listed tables to the view-owner role; `REVOKE` from PUBLIC.
5. Conformance test: reads appendix A and `information_schema.columns`, fails on any missing or mismatched column (AC8).
6. Down script: drops the 14 tables and the 12 columns in reverse dependency order.

## 13. Appendix A - the 80 fields

| Field ID | Workbench entity | Source | Source field | ACE column | Type | Frequency | Read through |
|---|---|---|---|---|---|---|---|
| DF-PTY-003 | party.party_type | SCBPDM via COLLINS | - | `customer.party_type` |  | Daily, end of day | `v_ace_customer.party_type` |
| DF-PTY-006 | party.id_type | SCBPDM via COLLINS | - | `customer.id_type` |  | Daily, end of day | `v_ace_customer.id_type` |
| DF-PTY-009 | party.segment | SCBPDM via COLLINS | Segment | `customer.segment` |  | Daily, end of day | `v_ace_customer.segment` |
| DF-ACC-006 | loan_account.business_unit | Core bank (ALS) via COLLINS | BU | `account.business_unit` |  |  | `v_ace_account.business_unit` |
| DF-ACC-009 | loan_account.principal_outstanding | Core bank (ALS) via COLLINS | Principal | `account.principal_outstanding` |  |  | `v_ace_account.principal_outstanding` |
| DF-ACC-010 | loan_account.interest_outstanding | Core bank (ALS) via COLLINS | AINT1 + AINT2 | `account.interest_outstanding` |  |  | `v_ace_account.interest_outstanding` |
| DF-ACC-011 | loan_account.fees_outstanding | Core bank (ALS) via COLLINS | AFEE | `account.fees_outstanding` |  |  | `v_ace_account.fees_outstanding` |
| DF-ACC-015 | loan_account.bucket | Core bank (ALS) via COLLINS | Bucket | `account.daily_bucket` |  |  | `v_ace_account.bucket` |
| DF-ACC-030 | loan_account.settlement_booked_date | Core bank (ALS) via COLLINS | - | `account.settlement_booked_date` |  |  | `v_ace_account.settlement_booked_date` |
| DF-ACC-031 | loan_account.settlement_booked_amount | Core bank (ALS) via COLLINS | - | `account.settlement_booked_amount` |  |  | `v_ace_account.settlement_booked_amount` |
| DF-COL-004 | collateral.title_doc_no | CCMS | Title Deed / Ownership Doc | `collateral_detail.title_doc_no` | varchar(40) | Weekly | `v_ace_collateral_detail.title_doc_no` |
| DF-COL-005 | collateral.plot_no | CCMS | Plot No. | `collateral_detail.plot_no` | varchar(20) | Weekly | `v_ace_collateral_detail.plot_no` |
| DF-COL-006 | collateral.area_text | CCMS | Area | `collateral_detail.area_text` | varchar(20) | Weekly | `v_ace_collateral_detail.area_text` |
| DF-COL-007 | collateral.province | CCMS | Province | `collateral_detail.province` | varchar(40) | Weekly | `v_ace_collateral_detail.province` |
| DF-COL-008 | collateral.district | CCMS | District | `collateral_detail.district` | varchar(60) | Weekly | `v_ace_collateral_detail.district` |
| DF-COL-009 | collateral.subdistrict | CCMS | Subdistrict | `collateral_detail.subdistrict` | varchar(60) | Weekly | `v_ace_collateral_detail.subdistrict` |
| DF-COL-012 | collateral.insured_value | CCMS | Insvalue | `collateral_detail.insured_value` | numeric(18,2) | Weekly | `v_ace_collateral_detail.insured_value` |
| DF-COL-013 | collateral.insurance_expiry | CCMS | - | `collateral_detail.insurance_expiry` | date | Weekly | `v_ace_collateral_detail.insurance_expiry` |
| DF-COL-017 | account_collateral.lien_rank | CCMS | - | `collateral_detail.lien_rank` | integer | Weekly | `v_ace_collateral_detail.lien_rank` |
| DF-COL-021 | valuation.appraisal_no | SVAF | Appraisal No. | `valuation.appraisal_no` | varchar(20) | Weekly | `v_ace_valuation.appraisal_no` |
| DF-COL-022 | valuation.appraisal_type | SVAF | - | `valuation.appraisal_type` | varchar(15) | Weekly | `v_ace_valuation.appraisal_type` |
| DF-COL-023 | valuation.appraised_value | SVAF | Appraised Value | `valuation.appraised_value` | numeric(18,2) | Weekly | `v_ace_valuation.appraised_value` |
| DF-COL-024 | valuation.forced_sale_value | SVAF | Forced Sale Value | `valuation.forced_sale_value` | numeric(18,2) | Weekly | `v_ace_valuation.forced_sale_value` |
| DF-COL-025 | valuation.appraisal_date | SVAF | Appraisal Date | `valuation.appraisal_date` | date | Weekly | `v_ace_valuation.appraisal_date` |
| DF-COL-032 | asset.asset_code | AMIS | Asset Code | `npa_asset.asset_code` | varchar(20) | Monthly | `v_ace_npa_asset.asset_code` |
| DF-COL-034 | asset.transfer_in_type | AMIS | Transfer-in Type | `npa_asset.transfer_in_type` | varchar(20) | Monthly | `v_ace_npa_asset.transfer_in_type` |
| DF-COL-035 | asset.from_segment | AMIS | From Segment | `npa_asset.from_segment` | varchar(20) | Monthly | `v_ace_npa_asset.from_segment` |
| DF-COL-036 | asset.transfer_in_date | AMIS | Ownership Transfer in Date | `npa_asset.transfer_in_date` | date | Monthly | `v_ace_npa_asset.transfer_in_date` |
| DF-COL-037 | asset.book_value | AMIS | Book  Value | `npa_asset.book_value` | numeric(18,2) | Monthly | `v_ace_npa_asset.book_value` |
| DF-COL-038 | asset.auction_purchase_price | AMIS | Auction Purchase Price | `npa_asset.auction_purchase_price` | numeric(18,2) | Monthly | `v_ace_npa_asset.auction_purchase_price` |
| DF-COL-039 | asset.repossessed_date | RPS | ReposessedCarDate | `npa_asset.repossessed_date` | date | Weekly | `v_ace_npa_asset.repossessed_date` |
| DF-COL-040 | asset.stock_date | RPS | STOCK_DATE | `npa_asset.stock_date` | date | Weekly | `v_ace_npa_asset.stock_date` |
| DF-TRT-023 | treatment.nleads_ref | NLEADS | - | `credit_decision.nleads_ref` | varchar(30) | On decision | `v_ace_credit_decision.nleads_ref` |
| DF-TRT-024 | treatment.credit_result | NLEADS | - | `credit_decision.credit_result` | varchar(10) | On decision | `v_ace_credit_decision.credit_result` |
| DF-TRT-025 | treatment.credit_result_reason | NLEADS | - | `credit_decision.credit_result_reason` | varchar(1000) | On decision | `v_ace_credit_decision.credit_result_reason` |
| DF-TRT-026 | treatment.credit_result_at | NLEADS | - | `credit_decision.decided_at` | timestamptz(6) | On decision | `v_ace_credit_decision.decided_at` |
| DF-LEG-005 | legal_action.lawsuit_no | LIT | LAWSUIT_NO / LAWSUIT_RUN | `lawsuit.lawsuit_no` | varchar(30) | Daily, end of day | `v_ace_lawsuit.lawsuit_no` |
| DF-LEG-006 | legal_action.black_case_no | LIT | เลขที่คดีดำ | `lawsuit.black_case_no` | varchar(30) | Daily, end of day | `v_ace_lawsuit.black_case_no` |
| DF-LEG-007 | legal_action.red_case_no | LIT | - | `lawsuit.red_case_no` | varchar(30) | Daily, end of day | `v_ace_lawsuit.red_case_no` |
| DF-LEG-008 | legal_action.court_name | LIT | NCOURT | `lawsuit.court_name` | varchar(120) | Daily, end of day | `v_ace_lawsuit.court_name` |
| DF-LEG-009 | legal_action.claim_amount | LIT | AAMT_SUIT | `lawsuit.claim_amount` | numeric(18,2) | Daily, end of day | `v_ace_lawsuit.claim_amount` |
| DF-LEG-010 | legal_action.filed_date | LIT | - | `lawsuit.filed_date` | date | Daily, end of day | `v_ace_lawsuit.filed_date` |
| DF-LEG-011 | legal_action.judgment_date | LIT | Judgment date | `lawsuit.judgment_date` | date | Daily, end of day | `v_ace_lawsuit.judgment_date` |
| DF-LEG-012 | legal_action.judgment_amount | LIT | - | `lawsuit.judgment_amount` | numeric(18,2) | Daily, end of day | `v_ace_lawsuit.judgment_amount` |
| DF-LEG-013 | legal_action.lit_status | LIT via COLLINS | STATE_RES_NAME | `lawsuit.lit_status` | varchar(200) | Daily, end of day | `v_ace_lawsuit.lit_status` |
| DF-LEG-019 | notice.sent_date | WIN | DDMMYYYY | `pod_receipt.sent_date` | date | Weekly | `v_ace_pod.sent_date` |
| DF-LEG-020 | notice.barcode | WIN | Barcode | `pod_receipt.barcode` | varchar(40) | Weekly | `v_ace_pod.barcode` |
| DF-LEG-021 | notice.callback_date | WIN | DDMMYYYY_callBack | `pod_receipt.callback_date` | date | Weekly | `v_ace_pod.callback_date` |
| DF-LEG-022 | notice.delivery_status | WIN | - | `pod_receipt.delivery_status` | varchar(15) | Weekly | `v_ace_pod.delivery_status` |
| DF-LEG-023 | notice.sent_type | WIN | Sent Type | `pod_receipt.sent_type` | varchar(10) | Weekly | `v_ace_pod.sent_type` |
| DF-LEG-026 | hearing.hearing_date | LIT | - | `hearing.hearing_date` | timestamptz(6) | Daily, end of day | `v_ace_hearing.hearing_date` |
| DF-LEG-027 | hearing.hearing_type | LIT | - | `hearing.hearing_type` | varchar(20) | Daily, end of day | `v_ace_hearing.hearing_type` |
| DF-LEG-029 | hearing.next_date | LIT | - | `hearing.next_date` | timestamptz(6) | Daily, end of day | `v_ace_hearing.next_date` |
| DF-SAL-012 | asset_sale.contract_date | AMIS | Contract Date | `npa_sale.contract_date` | date | Monthly | `v_ace_npa_sale.contract_date` |
| DF-SAL-013 | asset_sale.sale_date | AMIS | Sale Date | `npa_sale.sale_date` | date | Monthly | `v_ace_npa_sale.sale_date` |
| DF-SAL-014 | asset_sale.sale_price | AMIS | Sale Price | `npa_sale.sale_price` | numeric(18,2) | Monthly | `v_ace_npa_sale.sale_price` |
| DF-SAL-015 | asset_sale.transfer_fee | AMIS | Sale Transfer Fee | `npa_sale.transfer_fee` | numeric(18,2) | Monthly | `v_ace_npa_sale.transfer_fee` |
| DF-SAL-016 | asset_sale.specific_business_tax | AMIS | Specific Business Tax | `npa_sale.specific_business_tax` | numeric(18,2) | Monthly | `v_ace_npa_sale.specific_business_tax` |
| DF-SAL-017 | asset_sale.corporate_income_tax | AMIS | Corporate Income Tax | `npa_sale.corporate_income_tax` | numeric(18,2) | Monthly | `v_ace_npa_sale.corporate_income_tax` |
| DF-SAL-019 | asset_sale.incentive_amount | AMIS | Incentive Amount | `npa_sale.incentive_amount` | numeric(18,2) | Monthly | `v_ace_npa_sale.incentive_amount` |
| DF-INT-008 | interaction.contact_result | EFS via COLLINS | Call Result | `efs_action.contact_result` |  | Daily, end of day | `v_ace_efs_action.contact_result` |
| DF-INT-035 | collections_history.action_contact_status | EFS via COLLINS | - | `efs_action.action_contact_status` |  | Daily, end of day | `v_ace_efs_action.action_contact_status` |
| DF-INT-036 | collections_history.contact_result | EFS via COLLINS | Call Result | `efs_action.contact_result` |  | Daily, end of day | `v_ace_efs_action.contact_result` |
| DF-DEC-022 | score.model_code | COLLINS | - | `collins_score.model_code` | varchar(30) | Daily, end of day | `v_ace_score.model_code` |
| DF-DEC-023 | score.model_version | COLLINS | - | `collins_score.model_version` | varchar(20) | Daily, end of day | `v_ace_score.model_version` |
| DF-DEC-024 | score.score_value | COLLINS | - | `collins_score.score_value` | numeric(12,4) | Daily, end of day | `v_ace_score.score_value` |
| DF-DEC-025 | score.estimate_value | COLLINS | - | `collins_score.estimate_value` | numeric(18,2) | Daily, end of day | `v_ace_score.estimate_value` |
| DF-DEC-026 | score.route_code | COLLINS | - | `collins_score.route_code` | varchar(4) | Daily, end of day | `v_ace_score.route_code` |
| DF-DEC-027 | score.scored_at | COLLINS | - | `collins_score.scored_at` | date | Daily, end of day | `v_ace_score.scored_at` |
| DF-FIN-013 | write_off.amount | GL | AMT | `gl_write_off.amount` | numeric(18,2) | Monthly | `v_ace_write_off.amount` |
| DF-FIN-016 | write_off.posted_date | GL | DATE | `gl_write_off.posted_date` | date | Monthly | `v_ace_write_off.posted_date` |
| DF-FIN-017 | write_off.responsibility_center | GL | RC | `gl_write_off.responsibility_center` | varchar(10) | Monthly | `v_ace_write_off.responsibility_center` |
| DF-FIN-018 | write_off.cost_center | GL | OC | `gl_write_off.cost_center` | varchar(10) | Monthly | `v_ace_write_off.cost_center` |
| DF-FIN-019 | write_off.gl_product | GL | PRODUCT | `gl_write_off.gl_product` | varchar(10) | Monthly | `v_ace_write_off.gl_product` |
| DF-REF-039 | role.entra_group | Entra ID | - | `iam_group.entra_group` | varchar(120) | On change | `v_ace_iam_group.entra_group` |
| DF-PTY-024 | party_product.product_type | SCBPDM via COLLINS | - | `party_product.product_type` | varchar(20) | Daily, end of day | `v_ace_party_product.product_type` |
| DF-PTY-025 | party_product.account_no | SCBPDM via COLLINS | - | `party_product.account_key` | varchar(255) | Daily, end of day | `v_ace_party_product.account_no` |
| DF-PTY-026 | party_product.product_status | SCBPDM via COLLINS | - | `party_product.product_status` | varchar(15) | Daily, end of day | `v_ace_party_product.product_status` |
| DF-PTY-027 | party_product.data_as_of | SCBPDM via COLLINS | - | `party_product.business_date` | date | Daily, end of day | `v_ace_party_product.data_as_of` |
| DF-DOC-103 | signature_request.external_ref | EasyApp | - | `esign_request.external_ref` | varchar(60) | On request | `v_ace_esign.external_ref` |

## 14. Tests

| Test | Covers | Level |
|---|---|---|
| TC-ACE-001-01 | AC1 Tables and columns deployed | System |
| TC-ACE-001-02 | AC2 Every field populated | System |
| TC-ACE-001-03 | AC3 Business date and completion | System |
| TC-ACE-001-04 | AC4 Read grant only | System |
| TC-ACE-001-05 | AC5 Reversible | System |
| TC-ACE-001-06 | AC6 Existing ACE reads unaffected | System |
| TC-ACE-001-07 | AC7 Idempotent reload | System |
| TC-ACE-001-08 | AC8 Field appendix matches | System |

## 15. Traceability

| Requirement | Story | Test |
|---|---|---|
| REQ-RDF-001 Recovery data products have one system of record | RWB-ACE-001 | TC-ACE-001-01 to 08 |
| REQ-RDF-002 Recovery reads source data from ACE | RWB-ACE-001, RWB-E1-069 | TC-ACE-001-04, TC-E1-069-02 |
| D-RCV-35 U2 the ACE team owns new ACE tables and columns | RWB-ACE-001 | all |

The field appendix is the contract. If the ACE team changes a column, appendix A and the STTM v4 gap sheet change in the same pull request.