<!-- source: 15 ACE DB Alignment/Recovery Workbench ACE Field Gap List v1.xlsx -->
<!-- converted: 2026-11-16 from XLSX -->

> **Source:** `15 ACE DB Alignment/Recovery Workbench ACE Field Gap List v1.xlsx`  
> **Converted from:** XLSX

## Summary

| Recovery Workbench ACE field gap list v1 |  |  |
|---|---|---|
| SCB Collections and Recovery. Henka Group, 15 November 2026. Frozen input to RWB-ACE-001, LDM v7 and STTM v4. |  |  |
| Source: Logical Data Model and Data Dictionary v6, 133 fields with an external source. Decision: D-RCV-35. |  |  |
| Amended 15 November 2026 (coordinator decision D4): DF-DEC-006 decision_log_entry.model_version re-classed from ACE reuse to ACE new, because collins_score is a Tier 2 table. DF-PTY-016 read path is v_ace_contact.contact_value. Primary keys are NOT NULL; UK marks the business key. |  |  |
| Disposition | Fields | Meaning |
| ACE reuse | 51 | Already in ACE. Read through a v_ace_* view; no new column. |
| ACE new | 81 | Not in ACE. RWB-ACE-001 asks the ACE team for the table or column. |
| Recovery extension | 1 | A Workbench flag about an ACE record, in a Tier 3 extension table. |
| Workbench | 0 | Entered or recorded in the Workbench; no ACE ingestion. |
| Total | 133 |  |
| By source system |  |  |
| Source system | Fields | ACE new |
| Core bank (ALS) via COLLINS | 36 | 7 |
| AMIS | 15 | 13 |
| SCBPDM via COLLINS | 13 | 7 |
| EFS via COLLINS | 11 | 3 |
| CCMS | 11 | 9 |
| LIT | 11 | 11 |
| COLLINS | 7 | 7 |
| SVAF | 5 | 5 |
| WIN | 5 | 5 |
| GL | 5 | 5 |
| ACE | 4 | 0 |
| NLEADS | 4 | 4 |
| RPS | 2 | 2 |
| Aric via COLLINS | 1 | 0 |
| LIT via COLLINS | 1 | 1 |
| Entra ID | 1 | 1 |
| EasyApp | 1 | 1 |
| By ACE object (ACE new only) |  |  |
| ACE object | Fields |  |
| collateral_detail | 9 |  |
| lawsuit | 9 |  |
| npa_asset | 8 |  |
| account | 7 |  |
| npa_sale | 7 |  |
| collins_score | 7 |  |
| valuation | 5 |  |
| pod_receipt | 5 |  |
| gl_write_off | 5 |  |
| credit_decision | 4 |  |
| party_product | 4 |  |
| customer | 3 |  |
| hearing | 3 |  |
| efs_action | 3 |  |
| iam_group | 1 |  |
| esign_request | 1 |  |

## Fields

| Field ID | Entity | Field | Data type | Data product | Source system | Source field | Disposition | ACE object column | Read path | Note |
|---|---|---|---|---|---|---|---|---|---|---|
| DF-CAS-003 | recovery_case | product_group | LOV | DP03 | Core bank (ALS) via COLLINS | Product_Category_Host | ACE reuse | product.product_category | v_ace_account.product_category | Via account.product_key. |
| DF-CAS-014 | recovery_case | dpd_at_entry | NUMBER | DP03 | Core bank (ALS) via COLLINS | DELAY_DAYS | ACE reuse | account.delay_days | v_ace_account.days_past_due | Name mapped in the view. |
| DF-CAS-016 | recovery_case | total_outstanding_at_entry | NUMBER | DP03 | Core bank (ALS) via COLLINS | TOTAL_BALANCE | ACE reuse | account.total_balance | v_ace_account.total_balance |  |
| DF-CAS-046 | recovery_case | plan_ref | TEXT | DP03 | ACE |  | ACE reuse | ace_case.case_business_id | v_ace_plan.plan_ref | ACE restructure case reference; confirm the identifier with the ACE team. |
| DF-CAS-047 | recovery_case | plan_status | LOV | DP03 | ACE |  | ACE reuse | ace_case.current_station_name | v_ace_plan.plan_status | Derived from the ACE case station; confirm the status list. |
| DF-CAS-048 | recovery_case | plan_status_as_of | DATE | DP03 | ACE |  | ACE reuse | cfsc_mg_ssme_tdr_case.approval_completed_timestamp | v_ace_plan.plan_status_as_of |  |
| DF-PTY-002 | party | cif_no | TEXT | DP02 | SCBPDM via COLLINS | CIF | ACE reuse | customer.person_key | v_ace_customer.cif_no | ACE business key. |
| DF-PTY-003 | party | party_type | LOV | DP02 | SCBPDM via COLLINS |  | ACE new | customer.party_type | v_ace_customer.party_type | Confirm whether customer.category already carries individual or juristic. |
| DF-PTY-004 | party | first_name | TEXT | DP02 | SCBPDM via COLLINS |  | ACE reuse | customer.first_name | v_ace_customer.first_name |  |
| DF-PTY-005 | party | last_name | TEXT | DP02 | SCBPDM via COLLINS |  | ACE reuse | customer.surname | v_ace_customer.last_name |  |
| DF-PTY-006 | party | id_type | LOV | DP02 | SCBPDM via COLLINS |  | ACE new | customer.id_type | v_ace_customer.id_type | Not in ACE today. |
| DF-PTY-007 | party | id_no_token | TEXT | DP02 | SCBPDM via COLLINS |  | ACE reuse | customer.identification_number | v_ace_customer.id_no_masked | Held in clear in ACE. Masked in the view; role masking replaces tokenization (E1-037). |
| DF-PTY-008 | party | date_of_birth | DATE | DP02 | SCBPDM via COLLINS |  | ACE reuse | customer.birth_date | v_ace_customer.date_of_birth |  |
| DF-PTY-009 | party | segment | LOV | DP02 | SCBPDM via COLLINS | Segment | ACE new | customer.segment | v_ace_customer.segment | Not in ACE today. |
| DF-PTY-021 | party | fraud_flag | BOOLEAN | DP02 | Aric via COLLINS |  | Recovery extension | recovery.party_ext.fraud_flag | recovery.party_ext | Workbench-owned flag keyed by person_key. |
| DF-PTY-016 | contact_point | value_token | TEXT | DP02 | SCBPDM via COLLINS |  | ACE reuse | phone.phone_number / email.email / address.address | v_ace_contact.contact_value | Union view with contact_type. |
| DF-ACC-002 | loan_account | account_no | TEXT | DP01 | Core bank (ALS) via COLLINS | ACCOUNT_KEY / iacct / AccNo | ACE reuse | account.account_key | v_ace_account.account_no | ACE business key. |
| DF-ACC-003 | loan_account | contract_no | TEXT | DP01 | Core bank (ALS) via COLLINS | ContractNo | ACE reuse | account.contract_number | v_ace_account.contract_no |  |
| DF-ACC-004 | loan_account | product_code | LOV | DP01 | Core bank (ALS) via COLLINS | acct_prd_cd | ACE reuse | product.product_key | v_ace_account.product_code |  |
| DF-ACC-005 | loan_account | product_category_efs | TEXT | DP01 | EFS via COLLINS | Product_Category_EFS | ACE reuse | product.product_category_efs | v_ace_account.product_category_efs |  |
| DF-ACC-006 | loan_account | business_unit | LOV | DP01 | Core bank (ALS) via COLLINS | BU | ACE new | account.business_unit | v_ace_account.business_unit | ALS gap. |
| DF-ACC-007 | loan_account | contract_date | DATE | DP01 | Core bank (ALS) via COLLINS | CONTRACT_DATE | ACE reuse | account.contract_date | v_ace_account.contract_date |  |
| DF-ACC-008 | loan_account | interest_rate | NUMBER | DP01 | Core bank (ALS) via COLLINS | INTEREST_RATE | ACE reuse | account.interest_rate | v_ace_account.interest_rate | ACE numeric(38,2); view casts to numeric(7,4). |
| DF-ACC-009 | loan_account | principal_outstanding | NUMBER | DP01 | Core bank (ALS) via COLLINS | Principal | ACE new | account.principal_outstanding | v_ace_account.principal_outstanding | ALS gap. ACE holds total_balance only. |
| DF-ACC-010 | loan_account | interest_outstanding | NUMBER | DP01 | Core bank (ALS) via COLLINS | AINT1 + AINT2 | ACE new | account.interest_outstanding | v_ace_account.interest_outstanding | ALS gap. |
| DF-ACC-011 | loan_account | fees_outstanding | NUMBER | DP01 | Core bank (ALS) via COLLINS | AFEE | ACE new | account.fees_outstanding | v_ace_account.fees_outstanding | ALS gap. |
| DF-ACC-012 | loan_account | total_balance | NUMBER | DP01 | Core bank (ALS) via COLLINS | TOTAL_BALANCE | ACE reuse | account.total_balance | v_ace_account.total_balance |  |
| DF-ACC-013 | loan_account | accounting_balance | NUMBER | DP01 | Core bank (ALS) via COLLINS | ACCOUNTING_BALANCE | ACE reuse | account.accounting_balance | v_ace_account.accounting_balance |  |
| DF-ACC-014 | loan_account | days_past_due | NUMBER | DP01 | Core bank (ALS) via COLLINS | DELAY_DAYS | ACE reuse | account.delay_days | v_ace_account.days_past_due | LDM and STTM worked example. |
| DF-ACC-015 | loan_account | bucket | LOV | DP01 | Core bank (ALS) via COLLINS | Bucket | ACE new | account.daily_bucket | v_ace_account.bucket | ALS gap. bucket_log_snapshot is monthly. |
| DF-ACC-016 | loan_account | classification | LOV | DP01 | Core bank (ALS) via COLLINS |  | ACE reuse | account.loan_classification | v_ace_account.classification |  |
| DF-ACC-017 | loan_account | last_payment_date | DATE | DP01 | Core bank (ALS) via COLLINS | LAST_PAYMENT_DATE | ACE reuse | account.last_payment_date | v_ace_account.last_payment_date |  |
| DF-ACC-018 | loan_account | next_installment_date | DATE | DP01 | Core bank (ALS) via COLLINS | NEXT_INSTALLMENT_DATE | ACE reuse | account.next_installment_date | v_ace_account.next_installment_date |  |
| DF-ACC-019 | loan_account | tdr_flag | BOOLEAN | DP01 | Core bank (ALS) via COLLINS | TDR list | ACE reuse | account.is_restructured | v_ace_account.tdr_flag | varchar Y/N cast to boolean in the view. |
| DF-ACC-020 | loan_account | last_tdr_date | DATE | DP01 | Core bank (ALS) via COLLINS | Last_TDR_Date | ACE reuse | account.last_tdr_date | v_ace_account.last_tdr_date |  |
| DF-ACC-021 | loan_account | data_as_of | DATE | DP01 | Core bank (ALS) via COLLINS | ms_data_dt | ACE reuse | account.core_banking_system_date | v_ace_account.data_as_of | The ACE batch date. |
| DF-ACC-030 | loan_account | settlement_booked_date | DATE | DP01 | Core bank (ALS) via COLLINS |  | ACE new | account.settlement_booked_date | v_ace_account.settlement_booked_date | ALS gap. |
| DF-ACC-031 | loan_account | settlement_booked_amount | NUMBER | DP01 | Core bank (ALS) via COLLINS |  | ACE new | account.settlement_booked_amount | v_ace_account.settlement_booked_amount | ALS gap. |
| DF-ACC-024 | account_payment | payment_code | TEXT | DP01 | Core bank (ALS) via COLLINS | Payment_Code | ACE reuse | payment.pay_key | v_ace_payment.payment_code | ACE business key. |
| DF-ACC-025 | account_payment | payment_date | DATE | DP01 | Core bank (ALS) via COLLINS | Payment_Date | ACE reuse | payment.pay_date | v_ace_payment.payment_date | pay_date is varchar; the view casts to date. |
| DF-ACC-026 | account_payment | payment_amount | NUMBER | DP01 | Core bank (ALS) via COLLINS | Payment_Amount | ACE reuse | payment.total_amount | v_ace_payment.payment_amount |  |
| DF-ACC-027 | account_payment | payment_channel | LOV | DP01 | Core bank (ALS) via COLLINS |  | ACE reuse | payment.pay_type | v_ace_payment.payment_channel | Confirm the code list with the ACE team. |
| DF-ACC-028 | account_payment | data_as_of | DATE | DP01 | Core bank (ALS) via COLLINS | ms_data_dt | ACE reuse | account.core_banking_system_date | v_ace_payment.data_as_of | Read from the account snapshot; no new payment column. |
| DF-COL-002 | collateral | collateral_no | TEXT | DP06 | CCMS |  | ACE reuse | asset.asset_key | v_ace_collateral.collateral_no | ACE business key. |
| DF-COL-003 | collateral | collateral_type | LOV | DP06 | CCMS |  | ACE reuse | asset.asset_type | v_ace_collateral.collateral_type |  |
| DF-COL-004 | collateral | title_doc_no | TEXT | DP06 | CCMS | Title Deed / Ownership Doc | ACE new | collateral_detail.title_doc_no | v_ace_collateral_detail.title_doc_no | CCMS gap. |
| DF-COL-005 | collateral | plot_no | TEXT | DP06 | CCMS | Plot No. | ACE new | collateral_detail.plot_no | v_ace_collateral_detail.plot_no | CCMS gap. |
| DF-COL-006 | collateral | area_text | TEXT | DP06 | CCMS | Area | ACE new | collateral_detail.area_text | v_ace_collateral_detail.area_text | CCMS gap. |
| DF-COL-007 | collateral | province | LOV | DP06 | CCMS | Province | ACE new | collateral_detail.province | v_ace_collateral_detail.province | CCMS gap. |
| DF-COL-008 | collateral | district | TEXT | DP06 | CCMS | District | ACE new | collateral_detail.district | v_ace_collateral_detail.district | CCMS gap. |
| DF-COL-009 | collateral | subdistrict | TEXT | DP06 | CCMS | Subdistrict | ACE new | collateral_detail.subdistrict | v_ace_collateral_detail.subdistrict | CCMS gap. |
| DF-COL-012 | collateral | insured_value | NUMBER | DP06 | CCMS | Insvalue | ACE new | collateral_detail.insured_value | v_ace_collateral_detail.insured_value | CCMS gap. |
| DF-COL-013 | collateral | insurance_expiry | DATE | DP06 | CCMS |  | ACE new | collateral_detail.insurance_expiry | v_ace_collateral_detail.insurance_expiry | CCMS gap. |
| DF-COL-017 | account_collateral | lien_rank | NUMBER | DP06 | CCMS |  | ACE new | collateral_detail.lien_rank | v_ace_collateral_detail.lien_rank | Moves from account_collateral to the collateral grain. |
| DF-COL-021 | valuation | appraisal_no | TEXT | DP06 | SVAF | Appraisal No. | ACE new | valuation.appraisal_no | v_ace_valuation.appraisal_no | SVAF gap; new ACE table. |
| DF-COL-022 | valuation | appraisal_type | LOV | DP06 | SVAF |  | ACE new | valuation.appraisal_type | v_ace_valuation.appraisal_type | SVAF gap. |
| DF-COL-023 | valuation | appraised_value | NUMBER | DP06 | SVAF | Appraised Value | ACE new | valuation.appraised_value | v_ace_valuation.appraised_value | SVAF gap. |
| DF-COL-024 | valuation | forced_sale_value | NUMBER | DP06 | SVAF | Forced Sale Value | ACE new | valuation.forced_sale_value | v_ace_valuation.forced_sale_value | SVAF gap. |
| DF-COL-025 | valuation | appraisal_date | DATE | DP06 | SVAF | Appraisal Date | ACE new | valuation.appraisal_date | v_ace_valuation.appraisal_date | SVAF gap. |
| DF-COL-031 | asset | asset_ref | TEXT | DP06 | AMIS | Asset ID | ACE reuse | asset.asset_key | v_ace_asset.asset_ref | ACE business key. |
| DF-COL-032 | asset | asset_code | TEXT | DP06 | AMIS | Asset Code | ACE new | npa_asset.asset_code | v_ace_npa_asset.asset_code | AMIS gap. |
| DF-COL-033 | asset | asset_type | LOV | DP06 | AMIS | Asset Type | ACE reuse | asset.asset_type | v_ace_asset.asset_type |  |
| DF-COL-034 | asset | transfer_in_type | LOV | DP06 | AMIS | Transfer-in Type | ACE new | npa_asset.transfer_in_type | v_ace_npa_asset.transfer_in_type | AMIS gap. |
| DF-COL-035 | asset | from_segment | LOV | DP06 | AMIS | From Segment | ACE new | npa_asset.from_segment | v_ace_npa_asset.from_segment | AMIS gap. |
| DF-COL-036 | asset | transfer_in_date | DATE | DP06 | AMIS | Ownership Transfer in Date | ACE new | npa_asset.transfer_in_date | v_ace_npa_asset.transfer_in_date | AMIS gap. |
| DF-COL-037 | asset | book_value | NUMBER | DP06 | AMIS | Book  Value | ACE new | npa_asset.book_value | v_ace_npa_asset.book_value | AMIS gap. |
| DF-COL-038 | asset | auction_purchase_price | NUMBER | DP06 | AMIS | Auction Purchase Price | ACE new | npa_asset.auction_purchase_price | v_ace_npa_asset.auction_purchase_price | AMIS gap. |
| DF-COL-039 | asset | repossessed_date | DATE | DP06 | RPS | ReposessedCarDate | ACE new | npa_asset.repossessed_date | v_ace_npa_asset.repossessed_date | RPS gap. |
| DF-COL-040 | asset | stock_date | DATE | DP06 | RPS | STOCK_DATE | ACE new | npa_asset.stock_date | v_ace_npa_asset.stock_date | RPS gap. |
| DF-TRT-009 | treatment | installments | NUMBER | DP04 | ACE |  | ACE reuse | ai_recommended_plan.months | v_ace_plan.installments |  |
| DF-TRT-012 | treatment | booked_at | DATE | DP04 | Core bank (ALS) via COLLINS |  | ACE reuse | cfsc_mg_ssme_tdr_case.plan_setup_completed_timestamp | v_ace_plan.booked_at | Booking date derived from the ACE plan; confirm. |
| DF-TRT-023 | treatment | nleads_ref | TEXT | DP04 | NLEADS |  | ACE new | credit_decision.nleads_ref | v_ace_credit_decision.nleads_ref | NLEADS gap; new ACE table. |
| DF-TRT-024 | treatment | credit_result | LOV | DP04 | NLEADS |  | ACE new | credit_decision.credit_result | v_ace_credit_decision.credit_result | NLEADS gap. |
| DF-TRT-025 | treatment | credit_result_reason | TEXT | DP04 | NLEADS |  | ACE new | credit_decision.credit_result_reason | v_ace_credit_decision.credit_result_reason | NLEADS gap. |
| DF-TRT-026 | treatment | credit_result_at | DATE | DP04 | NLEADS |  | ACE new | credit_decision.decided_at | v_ace_credit_decision.decided_at | NLEADS gap. |
| DF-LEG-005 | legal_action | lawsuit_no | TEXT | DP07 | LIT | LAWSUIT_NO / LAWSUIT_RUN | ACE new | lawsuit.lawsuit_no | v_ace_lawsuit.lawsuit_no | LIT gap. |
| DF-LEG-006 | legal_action | black_case_no | TEXT | DP07 | LIT | เลขที่คดีดำ | ACE new | lawsuit.black_case_no | v_ace_lawsuit.black_case_no | LIT gap. |
| DF-LEG-007 | legal_action | red_case_no | TEXT | DP07 | LIT |  | ACE new | lawsuit.red_case_no | v_ace_lawsuit.red_case_no | LIT gap. |
| DF-LEG-008 | legal_action | court_name | TEXT | DP07 | LIT | NCOURT | ACE new | lawsuit.court_name | v_ace_lawsuit.court_name | LIT gap. |
| DF-LEG-009 | legal_action | claim_amount | NUMBER | DP07 | LIT | AAMT_SUIT | ACE new | lawsuit.claim_amount | v_ace_lawsuit.claim_amount | LIT gap. |
| DF-LEG-010 | legal_action | filed_date | DATE | DP07 | LIT |  | ACE new | lawsuit.filed_date | v_ace_lawsuit.filed_date | LIT gap. |
| DF-LEG-011 | legal_action | judgment_date | DATE | DP07 | LIT | Judgment date | ACE new | lawsuit.judgment_date | v_ace_lawsuit.judgment_date | LIT gap. |
| DF-LEG-012 | legal_action | judgment_amount | NUMBER | DP07 | LIT |  | ACE new | lawsuit.judgment_amount | v_ace_lawsuit.judgment_amount | LIT gap. |
| DF-LEG-013 | legal_action | lit_status | TEXT | DP07 | LIT via COLLINS | STATE_RES_NAME | ACE new | lawsuit.lit_status | v_ace_lawsuit.lit_status | LIT gap. |
| DF-LEG-019 | notice | sent_date | DATE | DP07 | WIN | DDMMYYYY | ACE new | pod_receipt.sent_date | v_ace_pod.sent_date | WIN gap. |
| DF-LEG-020 | notice | barcode | TEXT | DP07 | WIN | Barcode | ACE new | pod_receipt.barcode | v_ace_pod.barcode | WIN gap. |
| DF-LEG-021 | notice | callback_date | DATE | DP07 | WIN | DDMMYYYY_callBack | ACE new | pod_receipt.callback_date | v_ace_pod.callback_date | WIN gap. |
| DF-LEG-022 | notice | delivery_status | LOV | DP07 | WIN |  | ACE new | pod_receipt.delivery_status | v_ace_pod.delivery_status | WIN gap. |
| DF-LEG-023 | notice | sent_type | LOV | DP07 | WIN | Sent Type | ACE new | pod_receipt.sent_type | v_ace_pod.sent_type | WIN gap. |
| DF-LEG-026 | hearing | hearing_date | DATE | DP07 | LIT |  | ACE new | hearing.hearing_date | v_ace_hearing.hearing_date | LIT gap. |
| DF-LEG-027 | hearing | hearing_type | LOV | DP07 | LIT |  | ACE new | hearing.hearing_type | v_ace_hearing.hearing_type | LIT gap. |
| DF-LEG-029 | hearing | next_date | DATE | DP07 | LIT |  | ACE new | hearing.next_date | v_ace_hearing.next_date | LIT gap. |
| DF-SAL-012 | asset_sale | contract_date | DATE | DP06 | AMIS | Contract Date | ACE new | npa_sale.contract_date | v_ace_npa_sale.contract_date | AMIS gap. |
| DF-SAL-013 | asset_sale | sale_date | DATE | DP06 | AMIS | Sale Date | ACE new | npa_sale.sale_date | v_ace_npa_sale.sale_date | AMIS gap. |
| DF-SAL-014 | asset_sale | sale_price | NUMBER | DP06 | AMIS | Sale Price | ACE new | npa_sale.sale_price | v_ace_npa_sale.sale_price | AMIS gap. |
| DF-SAL-015 | asset_sale | transfer_fee | NUMBER | DP06 | AMIS | Sale Transfer Fee | ACE new | npa_sale.transfer_fee | v_ace_npa_sale.transfer_fee | AMIS gap. |
| DF-SAL-016 | asset_sale | specific_business_tax | NUMBER | DP06 | AMIS | Specific Business Tax | ACE new | npa_sale.specific_business_tax | v_ace_npa_sale.specific_business_tax | AMIS gap. |
| DF-SAL-017 | asset_sale | corporate_income_tax | NUMBER | DP06 | AMIS | Corporate Income Tax | ACE new | npa_sale.corporate_income_tax | v_ace_npa_sale.corporate_income_tax | AMIS gap. |
| DF-SAL-019 | asset_sale | incentive_amount | NUMBER | DP06 | AMIS | Incentive Amount | ACE new | npa_sale.incentive_amount | v_ace_npa_sale.incentive_amount | AMIS gap. |
| DF-SAL-035 | debt_sale_account | outstanding | NUMBER | DP09 | Core bank (ALS) via COLLINS | OS By Acct | ACE reuse | account.total_balance | v_ace_account.total_balance | Balance at the debt sale cut-off date; no new column. |
| DF-INT-007 | interaction | action_code | LOV | DP05 | EFS via COLLINS | Actioncode ID | ACE reuse | efs_action.action_code | v_ace_efs_action.action_code |  |
| DF-INT-008 | interaction | contact_result | LOV | DP05 | EFS via COLLINS | Call Result | ACE new | efs_action.contact_result | v_ace_efs_action.contact_result | Not in ACE today. |
| DF-DEC-006 | decision_log_entry | model_version | TEXT | DP12 | COLLINS |  | ACE new | collins_score.model_version | v_ace_score.model_version | COLLINS score gap (D4). Same ACE column as DF-DEC-023, collins_score.model_version; read at decision time. |
| DF-DEC-022 | score | model_code | TEXT | DP11 | COLLINS |  | ACE new | collins_score.model_code | v_ace_score.model_code | COLLINS score gap. |
| DF-DEC-023 | score | model_version | TEXT | DP11 | COLLINS |  | ACE new | collins_score.model_version | v_ace_score.model_version | COLLINS score gap. |
| DF-DEC-024 | score | score_value | NUMBER | DP11 | COLLINS |  | ACE new | collins_score.score_value | v_ace_score.score_value | COLLINS score gap. |
| DF-DEC-025 | score | estimate_value | NUMBER | DP11 | COLLINS |  | ACE new | collins_score.estimate_value | v_ace_score.estimate_value | COLLINS score gap. |
| DF-DEC-026 | score | route_code | LOV | DP11 | COLLINS |  | ACE new | collins_score.route_code | v_ace_score.route_code | COLLINS score gap. |
| DF-DEC-027 | score | scored_at | DATE | DP11 | COLLINS |  | ACE new | collins_score.scored_at | v_ace_score.scored_at | COLLINS score gap. |
| DF-FIN-006 | proceeds | amount | NUMBER | DP13 | Core bank (ALS) via COLLINS | Payment_Amount | ACE reuse | payment.total_amount | v_ace_payment.payment_amount |  |
| DF-FIN-007 | proceeds | received_date | DATE | DP13 | Core bank (ALS) via COLLINS | Payment_Date | ACE reuse | payment.pay_date | v_ace_payment.payment_date | varchar cast to date in the view. |
| DF-FIN-009 | proceeds | posting_ref | TEXT | DP13 | Core bank (ALS) via COLLINS |  | ACE reuse | payment.pay_key | v_ace_payment.payment_code | Confirm as the posting reference. |
| DF-FIN-013 | write_off | amount | NUMBER | DP13 | GL | AMT | ACE new | gl_write_off.amount | v_ace_write_off.amount | GL gap. |
| DF-FIN-016 | write_off | posted_date | DATE | DP13 | GL | DATE | ACE new | gl_write_off.posted_date | v_ace_write_off.posted_date | GL gap. |
| DF-FIN-017 | write_off | responsibility_center | TEXT | DP13 | GL | RC | ACE new | gl_write_off.responsibility_center | v_ace_write_off.responsibility_center | GL gap. |
| DF-FIN-018 | write_off | cost_center | TEXT | DP13 | GL | OC | ACE new | gl_write_off.cost_center | v_ace_write_off.cost_center | GL gap. |
| DF-FIN-019 | write_off | gl_product | TEXT | DP13 | GL | PRODUCT | ACE new | gl_write_off.gl_product | v_ace_write_off.gl_product | GL gap. |
| DF-REF-039 | role | entra_group | TEXT | DP14 | Entra ID |  | ACE new | iam_group.entra_group | v_ace_iam_group.entra_group | Entra ID gap; new ACE table. ACE owns the group-to-role mapping because ACE performs the sign-in. |
| DF-INT-031 | collections_history | account_no | TEXT | DP05 | EFS via COLLINS |  | ACE reuse | efs_action.account_key | v_ace_efs_action.account_no |  |
| DF-INT-032 | collections_history | efs_record_key | TEXT | DP05 | EFS via COLLINS |  | ACE reuse | efs_action.action_id | v_ace_efs_action.efs_record_key |  |
| DF-INT-033 | collections_history | contact_at | DATE | DP05 | EFS via COLLINS |  | ACE reuse | efs_action.action_timestamp | v_ace_efs_action.contact_at |  |
| DF-INT-034 | collections_history | action_code | LOV | DP05 | EFS via COLLINS | Actioncode ID | ACE reuse | efs_action.action_code | v_ace_efs_action.action_code |  |
| DF-INT-035 | collections_history | action_contact_status | TEXT | DP05 | EFS via COLLINS |  | ACE new | efs_action.action_contact_status | v_ace_efs_action.action_contact_status | Not in ACE today. |
| DF-INT-036 | collections_history | contact_result | LOV | DP05 | EFS via COLLINS | Call Result | ACE new | efs_action.contact_result | v_ace_efs_action.contact_result | Shared with DF-INT-008. |
| DF-INT-037 | collections_history | promise_amount | NUMBER | DP05 | EFS via COLLINS |  | ACE reuse | efs_action.settle_total_amount | v_ace_efs_action.promise_amount |  |
| DF-INT-038 | collections_history | promise_date | DATE | DP05 | EFS via COLLINS |  | ACE reuse | efs_action.settlement_due_date | v_ace_efs_action.promise_date |  |
| DF-TRT-050 | dp_treatment | contract_no | TEXT | DP04 | Core bank (ALS) via COLLINS | ContractNo | ACE reuse | account.contract_number | v_ace_account.contract_no |  |
| DF-TRT-051 | dp_treatment | contract_date | DATE | DP04 | Core bank (ALS) via COLLINS | CONTRACT_DATE | ACE reuse | account.contract_date | v_ace_account.contract_date |  |
| DF-PTY-024 | party_product | product_type | TEXT | DP02 | SCBPDM via COLLINS |  | ACE new | party_product.product_type | v_ace_party_product.product_type | SCBPDM gap; new ACE table. |
| DF-PTY-025 | party_product | account_no | TEXT | DP02 | SCBPDM via COLLINS |  | ACE new | party_product.account_key | v_ace_party_product.account_no | SCBPDM gap. |
| DF-PTY-026 | party_product | product_status | LOV | DP02 | SCBPDM via COLLINS |  | ACE new | party_product.product_status | v_ace_party_product.product_status | SCBPDM gap. |
| DF-PTY-027 | party_product | data_as_of | DATE | DP02 | SCBPDM via COLLINS |  | ACE new | party_product.business_date | v_ace_party_product.data_as_of | SCBPDM gap. |
| DF-DOC-103 | signature_request | external_ref | TEXT | DP10 | EasyApp |  | ACE new | esign_request.external_ref | v_ace_esign.external_ref | EasyApp gap; new ACE table. ACE receives the signature call-back, so the reference belongs with the ingestion, not on the Workbench document. |

## ACE additions

| ACE table | Column | Type | Nullable | Key | Source system | LDM field IDs | Note |
|---|---|---|---|---|---|---|---|
| ace_batch_run | id | bigint | NO | PK | all sources |  | New table. The Workbench freshness stamp (E1-015) and the intake trigger (E1-016, E1-018) read it. |
| ace_batch_run | source_system | varchar(20) | NO | UK (source_system, business_date) | all sources |  | New table. The Workbench freshness stamp (E1-015) and the intake trigger (E1-016, E1-018) read it. |
| ace_batch_run | business_date | date | NO | UK (source_system, business_date) | all sources |  | New table. The Workbench freshness stamp (E1-015) and the intake trigger (E1-016, E1-018) read it. |
| ace_batch_run | started_at | timestamptz(6) | NO |  | all sources |  | New table. The Workbench freshness stamp (E1-015) and the intake trigger (E1-016, E1-018) read it. |
| ace_batch_run | completed_at | timestamptz(6) | YES |  | all sources |  | New table. The Workbench freshness stamp (E1-015) and the intake trigger (E1-016, E1-018) read it. |
| ace_batch_run | status | varchar(12) | NO |  | all sources |  | New table. The Workbench freshness stamp (E1-015) and the intake trigger (E1-016, E1-018) read it. |
| ace_batch_run | record_count | bigint | YES |  | all sources |  | New table. The Workbench freshness stamp (E1-015) and the intake trigger (E1-016, E1-018) read it. |
| ace_batch_run | checksum | varchar(64) | YES |  | all sources |  | New table. The Workbench freshness stamp (E1-015) and the intake trigger (E1-016, E1-018) read it. |
| ace_batch_run | feed_version | varchar(20) | YES |  | all sources |  | New table. The Workbench freshness stamp (E1-015) and the intake trigger (E1-016, E1-018) read it. |
| collateral_detail | id | bigint | NO | PK | CCMS |  | New table. lien_rank moves from account_collateral to the collateral grain. |
| collateral_detail | collateral_detail_key | varchar(255) | NO | UK | CCMS |  | New table. lien_rank moves from account_collateral to the collateral grain. |
| collateral_detail | asset_key | varchar(255) | NO | FK asset.asset_key | CCMS |  | New table. lien_rank moves from account_collateral to the collateral grain. |
| collateral_detail | title_doc_no | varchar(40) | YES |  | CCMS | DF-COL-004 | New table. lien_rank moves from account_collateral to the collateral grain. |
| collateral_detail | plot_no | varchar(20) | YES |  | CCMS | DF-COL-005 | New table. lien_rank moves from account_collateral to the collateral grain. |
| collateral_detail | area_text | varchar(20) | YES |  | CCMS | DF-COL-006 | New table. lien_rank moves from account_collateral to the collateral grain. |
| collateral_detail | province | varchar(40) | YES |  | CCMS | DF-COL-007 | New table. lien_rank moves from account_collateral to the collateral grain. |
| collateral_detail | district | varchar(60) | YES |  | CCMS | DF-COL-008 | New table. lien_rank moves from account_collateral to the collateral grain. |
| collateral_detail | subdistrict | varchar(60) | YES |  | CCMS | DF-COL-009 | New table. lien_rank moves from account_collateral to the collateral grain. |
| collateral_detail | insured_value | numeric(18,2) | YES |  | CCMS | DF-COL-012 | New table. lien_rank moves from account_collateral to the collateral grain. |
| collateral_detail | insurance_expiry | date | YES |  | CCMS | DF-COL-013 | New table. lien_rank moves from account_collateral to the collateral grain. |
| collateral_detail | lien_rank | integer | YES |  | CCMS | DF-COL-017 | New table. lien_rank moves from account_collateral to the collateral grain. |
| collateral_detail | source_system | varchar(20) | NO |  | CCMS |  | New table. lien_rank moves from account_collateral to the collateral grain. |
| collateral_detail | business_date | date | NO |  | CCMS |  | New table. lien_rank moves from account_collateral to the collateral grain. |
| collateral_detail | loaded_at | timestamptz(6) | NO |  | CCMS |  | New table. lien_rank moves from account_collateral to the collateral grain. |
| valuation | id | bigint | NO | PK | SVAF |  | New table. Accepted, stale and valuer fields stay in recovery.valuation_ext. |
| valuation | valuation_key | varchar(255) | NO | UK | SVAF |  | New table. Accepted, stale and valuer fields stay in recovery.valuation_ext. |
| valuation | asset_key | varchar(255) | NO | FK asset.asset_key | SVAF |  | New table. Accepted, stale and valuer fields stay in recovery.valuation_ext. |
| valuation | appraisal_no | varchar(20) | YES |  | SVAF | DF-COL-021 | New table. Accepted, stale and valuer fields stay in recovery.valuation_ext. |
| valuation | appraisal_type | varchar(15) | YES |  | SVAF | DF-COL-022 | New table. Accepted, stale and valuer fields stay in recovery.valuation_ext. |
| valuation | appraised_value | numeric(18,2) | YES |  | SVAF | DF-COL-023 | New table. Accepted, stale and valuer fields stay in recovery.valuation_ext. |
| valuation | forced_sale_value | numeric(18,2) | YES |  | SVAF | DF-COL-024 | New table. Accepted, stale and valuer fields stay in recovery.valuation_ext. |
| valuation | appraisal_date | date | YES |  | SVAF | DF-COL-025 | New table. Accepted, stale and valuer fields stay in recovery.valuation_ext. |
| valuation | source_system | varchar(20) | NO |  | SVAF |  | New table. Accepted, stale and valuer fields stay in recovery.valuation_ext. |
| valuation | business_date | date | NO |  | SVAF |  | New table. Accepted, stale and valuer fields stay in recovery.valuation_ext. |
| valuation | loaded_at | timestamptz(6) | NO |  | SVAF |  | New table. Accepted, stale and valuer fields stay in recovery.valuation_ext. |
| npa_asset | id | bigint | NO | PK | AMIS, RPS |  | New table. AMIS for property, RPS for vehicles. |
| npa_asset | npa_asset_key | varchar(255) | NO | UK | AMIS, RPS |  | New table. AMIS for property, RPS for vehicles. |
| npa_asset | asset_key | varchar(255) | NO | FK asset.asset_key | AMIS, RPS |  | New table. AMIS for property, RPS for vehicles. |
| npa_asset | asset_code | varchar(20) | YES |  | AMIS, RPS | DF-COL-032 | New table. AMIS for property, RPS for vehicles. |
| npa_asset | transfer_in_type | varchar(20) | YES |  | AMIS, RPS | DF-COL-034 | New table. AMIS for property, RPS for vehicles. |
| npa_asset | from_segment | varchar(20) | YES |  | AMIS, RPS | DF-COL-035 | New table. AMIS for property, RPS for vehicles. |
| npa_asset | transfer_in_date | date | YES |  | AMIS, RPS | DF-COL-036 | New table. AMIS for property, RPS for vehicles. |
| npa_asset | book_value | numeric(18,2) | YES |  | AMIS, RPS | DF-COL-037 | New table. AMIS for property, RPS for vehicles. |
| npa_asset | auction_purchase_price | numeric(18,2) | YES |  | AMIS, RPS | DF-COL-038 | New table. AMIS for property, RPS for vehicles. |
| npa_asset | repossessed_date | date | YES |  | AMIS, RPS | DF-COL-039 | New table. AMIS for property, RPS for vehicles. |
| npa_asset | stock_date | date | YES |  | AMIS, RPS | DF-COL-040 | New table. AMIS for property, RPS for vehicles. |
| npa_asset | source_system | varchar(20) | NO |  | AMIS, RPS |  | New table. AMIS for property, RPS for vehicles. |
| npa_asset | business_date | date | NO |  | AMIS, RPS |  | New table. AMIS for property, RPS for vehicles. |
| npa_asset | loaded_at | timestamptz(6) | NO |  | AMIS, RPS |  | New table. AMIS for property, RPS for vehicles. |
| npa_sale | id | bigint | NO | PK | AMIS |  | New table. AMIS sale contract, taxes and fees. |
| npa_sale | npa_sale_key | varchar(255) | NO | UK | AMIS |  | New table. AMIS sale contract, taxes and fees. |
| npa_sale | npa_asset_key | varchar(255) | NO | FK npa_asset.npa_asset_key | AMIS |  | New table. AMIS sale contract, taxes and fees. |
| npa_sale | contract_date | date | YES |  | AMIS | DF-SAL-012 | New table. AMIS sale contract, taxes and fees. |
| npa_sale | sale_date | date | YES |  | AMIS | DF-SAL-013 | New table. AMIS sale contract, taxes and fees. |
| npa_sale | sale_price | numeric(18,2) | YES |  | AMIS | DF-SAL-014 | New table. AMIS sale contract, taxes and fees. |
| npa_sale | transfer_fee | numeric(18,2) | YES |  | AMIS | DF-SAL-015 | New table. AMIS sale contract, taxes and fees. |
| npa_sale | specific_business_tax | numeric(18,2) | YES |  | AMIS | DF-SAL-016 | New table. AMIS sale contract, taxes and fees. |
| npa_sale | corporate_income_tax | numeric(18,2) | YES |  | AMIS | DF-SAL-017 | New table. AMIS sale contract, taxes and fees. |
| npa_sale | incentive_amount | numeric(18,2) | YES |  | AMIS | DF-SAL-019 | New table. AMIS sale contract, taxes and fees. |
| npa_sale | source_system | varchar(20) | NO |  | AMIS |  | New table. AMIS sale contract, taxes and fees. |
| npa_sale | business_date | date | NO |  | AMIS |  | New table. AMIS sale contract, taxes and fees. |
| npa_sale | loaded_at | timestamptz(6) | NO |  | AMIS |  | New table. AMIS sale contract, taxes and fees. |
| lawsuit | id | bigint | NO | PK | LIT |  | New table. LIT court record. |
| lawsuit | lawsuit_key | varchar(255) | NO | UK | LIT |  | New table. LIT court record. |
| lawsuit | account_key | varchar(255) | NO | FK account.account_key | LIT |  | New table. LIT court record. |
| lawsuit | lawsuit_no | varchar(30) | YES |  | LIT | DF-LEG-005 | New table. LIT court record. |
| lawsuit | black_case_no | varchar(30) | YES |  | LIT | DF-LEG-006 | New table. LIT court record. |
| lawsuit | red_case_no | varchar(30) | YES |  | LIT | DF-LEG-007 | New table. LIT court record. |
| lawsuit | court_name | varchar(120) | YES |  | LIT | DF-LEG-008 | New table. LIT court record. |
| lawsuit | claim_amount | numeric(18,2) | YES |  | LIT | DF-LEG-009 | New table. LIT court record. |
| lawsuit | filed_date | date | YES |  | LIT | DF-LEG-010 | New table. LIT court record. |
| lawsuit | judgment_date | date | YES |  | LIT | DF-LEG-011 | New table. LIT court record. |
| lawsuit | judgment_amount | numeric(18,2) | YES |  | LIT | DF-LEG-012 | New table. LIT court record. |
| lawsuit | lit_status | varchar(200) | YES |  | LIT | DF-LEG-013 | New table. LIT court record. |
| lawsuit | source_system | varchar(20) | NO |  | LIT |  | New table. LIT court record. |
| lawsuit | business_date | date | NO |  | LIT |  | New table. LIT court record. |
| lawsuit | loaded_at | timestamptz(6) | NO |  | LIT |  | New table. LIT court record. |
| hearing | id | bigint | NO | PK | LIT |  | New table. LIT hearing, one row per hearing. |
| hearing | hearing_key | varchar(255) | NO | UK | LIT |  | New table. LIT hearing, one row per hearing. |
| hearing | lawsuit_key | varchar(255) | NO | FK lawsuit.lawsuit_key | LIT |  | New table. LIT hearing, one row per hearing. |
| hearing | hearing_date | timestamptz(6) | NO |  | LIT | DF-LEG-026 | New table. LIT hearing, one row per hearing. |
| hearing | hearing_type | varchar(20) | YES |  | LIT | DF-LEG-027 | New table. LIT hearing, one row per hearing. |
| hearing | next_date | timestamptz(6) | YES |  | LIT | DF-LEG-029 | New table. LIT hearing, one row per hearing. |
| hearing | source_system | varchar(20) | NO |  | LIT |  | New table. LIT hearing, one row per hearing. |
| hearing | business_date | date | NO |  | LIT |  | New table. LIT hearing, one row per hearing. |
| hearing | loaded_at | timestamptz(6) | NO |  | LIT |  | New table. LIT hearing, one row per hearing. |
| pod_receipt | id | bigint | NO | PK | WIN |  | New table. WIN proof of delivery. The notice itself stays in recovery.notice. |
| pod_receipt | pod_key | varchar(255) | NO | UK | WIN |  | New table. WIN proof of delivery. The notice itself stays in recovery.notice. |
| pod_receipt | account_key | varchar(255) | NO | FK account.account_key | WIN |  | New table. WIN proof of delivery. The notice itself stays in recovery.notice. |
| pod_receipt | notice_ref | varchar(60) | YES |  | WIN |  | New table. WIN proof of delivery. The notice itself stays in recovery.notice. |
| pod_receipt | sent_date | date | YES |  | WIN | DF-LEG-019 | New table. WIN proof of delivery. The notice itself stays in recovery.notice. |
| pod_receipt | barcode | varchar(40) | YES |  | WIN | DF-LEG-020 | New table. WIN proof of delivery. The notice itself stays in recovery.notice. |
| pod_receipt | callback_date | date | YES |  | WIN | DF-LEG-021 | New table. WIN proof of delivery. The notice itself stays in recovery.notice. |
| pod_receipt | delivery_status | varchar(15) | YES |  | WIN | DF-LEG-022 | New table. WIN proof of delivery. The notice itself stays in recovery.notice. |
| pod_receipt | sent_type | varchar(10) | YES |  | WIN | DF-LEG-023 | New table. WIN proof of delivery. The notice itself stays in recovery.notice. |
| pod_receipt | source_system | varchar(20) | NO |  | WIN |  | New table. WIN proof of delivery. The notice itself stays in recovery.notice. |
| pod_receipt | business_date | date | NO |  | WIN |  | New table. WIN proof of delivery. The notice itself stays in recovery.notice. |
| pod_receipt | loaded_at | timestamptz(6) | NO |  | WIN |  | New table. WIN proof of delivery. The notice itself stays in recovery.notice. |
| gl_write_off | id | bigint | NO | PK | GL |  | New table. GL posting. The write-off decision stays in recovery.write_off. |
| gl_write_off | write_off_key | varchar(255) | NO | UK | GL |  | New table. GL posting. The write-off decision stays in recovery.write_off. |
| gl_write_off | account_key | varchar(255) | NO | FK account.account_key | GL |  | New table. GL posting. The write-off decision stays in recovery.write_off. |
| gl_write_off | amount | numeric(18,2) | NO |  | GL | DF-FIN-013 | New table. GL posting. The write-off decision stays in recovery.write_off. |
| gl_write_off | posted_date | date | YES |  | GL | DF-FIN-016 | New table. GL posting. The write-off decision stays in recovery.write_off. |
| gl_write_off | responsibility_center | varchar(10) | YES |  | GL | DF-FIN-017 | New table. GL posting. The write-off decision stays in recovery.write_off. |
| gl_write_off | cost_center | varchar(10) | YES |  | GL | DF-FIN-018 | New table. GL posting. The write-off decision stays in recovery.write_off. |
| gl_write_off | gl_product | varchar(10) | YES |  | GL | DF-FIN-019 | New table. GL posting. The write-off decision stays in recovery.write_off. |
| gl_write_off | source_system | varchar(20) | NO |  | GL |  | New table. GL posting. The write-off decision stays in recovery.write_off. |
| gl_write_off | business_date | date | NO |  | GL |  | New table. GL posting. The write-off decision stays in recovery.write_off. |
| gl_write_off | loaded_at | timestamptz(6) | NO |  | GL |  | New table. GL posting. The write-off decision stays in recovery.write_off. |
| collins_score | id | bigint | NO | PK | COLLINS |  | New table, only if ACE does not already hold the score. |
| collins_score | score_key | varchar(255) | NO | UK | COLLINS |  | New table, only if ACE does not already hold the score. |
| collins_score | account_key | varchar(255) | NO | FK account.account_key | COLLINS |  | New table, only if ACE does not already hold the score. |
| collins_score | model_code | varchar(30) | NO |  | COLLINS | DF-DEC-022 | New table, only if ACE does not already hold the score. |
| collins_score | model_version | varchar(20) | NO |  | COLLINS | DF-DEC-006, DF-DEC-023 | New table, only if ACE does not already hold the score. |
| collins_score | score_value | numeric(12,4) | YES |  | COLLINS | DF-DEC-024 | New table, only if ACE does not already hold the score. |
| collins_score | estimate_value | numeric(18,2) | YES |  | COLLINS | DF-DEC-025 | New table, only if ACE does not already hold the score. |
| collins_score | route_code | varchar(4) | YES |  | COLLINS | DF-DEC-026 | New table, only if ACE does not already hold the score. |
| collins_score | scored_at | date | NO |  | COLLINS | DF-DEC-027 | New table, only if ACE does not already hold the score. |
| collins_score | source_system | varchar(20) | NO |  | COLLINS |  | New table, only if ACE does not already hold the score. |
| collins_score | business_date | date | NO |  | COLLINS |  | New table, only if ACE does not already hold the score. |
| collins_score | loaded_at | timestamptz(6) | NO |  | COLLINS |  | New table, only if ACE does not already hold the score. |
| party_product | id | bigint | NO | PK | SCBPDM |  | New table. SCBPDM product holding. |
| party_product | person_key | varchar(255) | NO | UK (person_key, account_key, product_type, business_date); FK customer.person_key | SCBPDM |  | New table. SCBPDM product holding. |
| party_product | account_key | varchar(255) | NO | UK (person_key, account_key, product_type, business_date) | SCBPDM | DF-PTY-025 | New table. SCBPDM product holding. |
| party_product | product_type | varchar(20) | NO | UK (person_key, account_key, product_type, business_date) | SCBPDM | DF-PTY-024 | New table. SCBPDM product holding. |
| party_product | product_status | varchar(15) | NO |  | SCBPDM | DF-PTY-026 | New table. SCBPDM product holding. |
| party_product | business_date | date | NO | UK (person_key, account_key, product_type, business_date) | SCBPDM | DF-PTY-027 | New table. SCBPDM product holding. |
| party_product | loaded_at | timestamptz(6) | NO |  | SCBPDM |  | New table. SCBPDM product holding. |
| credit_decision | id | bigint | NO | PK | NLEADS |  | New table. NLEADS credit result for a treatment. |
| credit_decision | credit_decision_key | varchar(255) | NO | UK | NLEADS |  | New table. NLEADS credit result for a treatment. |
| credit_decision | account_key | varchar(255) | NO | FK account.account_key | NLEADS |  | New table. NLEADS credit result for a treatment. |
| credit_decision | nleads_ref | varchar(30) | YES |  | NLEADS | DF-TRT-023 | New table. NLEADS credit result for a treatment. |
| credit_decision | credit_result | varchar(10) | YES |  | NLEADS | DF-TRT-024 | New table. NLEADS credit result for a treatment. |
| credit_decision | credit_result_reason | varchar(1000) | YES |  | NLEADS | DF-TRT-025 | New table. NLEADS credit result for a treatment. |
| credit_decision | decided_at | timestamptz(6) | YES |  | NLEADS | DF-TRT-026 | New table. NLEADS credit result for a treatment. |
| credit_decision | source_system | varchar(20) | NO |  | NLEADS |  | New table. NLEADS credit result for a treatment. |
| credit_decision | business_date | date | NO |  | NLEADS |  | New table. NLEADS credit result for a treatment. |
| credit_decision | loaded_at | timestamptz(6) | NO |  | NLEADS |  | New table. NLEADS credit result for a treatment. |
| esign_request | id | bigint | NO | PK | EasyApp |  | New table. EasyApp signature reference and status; the signed file stays in the Workbench document hub. |
| esign_request | esign_key | varchar(255) | NO | UK | EasyApp |  | New table. EasyApp signature reference and status; the signed file stays in the Workbench document hub. |
| esign_request | account_key | varchar(255) | NO | FK account.account_key | EasyApp |  | New table. EasyApp signature reference and status; the signed file stays in the Workbench document hub. |
| esign_request | external_ref | varchar(60) | YES |  | EasyApp | DF-DOC-103 | New table. EasyApp signature reference and status; the signed file stays in the Workbench document hub. |
| esign_request | requested_at | timestamptz(6) | YES |  | EasyApp |  | New table. EasyApp signature reference and status; the signed file stays in the Workbench document hub. |
| esign_request | status | varchar(20) | YES |  | EasyApp |  | New table. EasyApp signature reference and status; the signed file stays in the Workbench document hub. |
| esign_request | source_system | varchar(20) | NO |  | EasyApp |  | New table. EasyApp signature reference and status; the signed file stays in the Workbench document hub. |
| esign_request | business_date | date | NO |  | EasyApp |  | New table. EasyApp signature reference and status; the signed file stays in the Workbench document hub. |
| esign_request | loaded_at | timestamptz(6) | NO |  | EasyApp |  | New table. EasyApp signature reference and status; the signed file stays in the Workbench document hub. |
| iam_group | id | bigint | NO | PK | Entra ID |  | New table. Entra ID group to Workbench role mapping. Business key (entra_group, role_code); iam_group_key is the Entra group object ID and repeats when one group maps to more than one role. |
| iam_group | iam_group_key | varchar(255) | NO |  | Entra ID |  | New table. Entra ID group to Workbench role mapping. Business key (entra_group, role_code); iam_group_key is the Entra group object ID and repeats when one group maps to more than one role. |
| iam_group | entra_group | varchar(120) | NO | UK (entra_group, role_code) | Entra ID | DF-REF-039 | New table. Entra ID group to Workbench role mapping. Business key (entra_group, role_code); iam_group_key is the Entra group object ID and repeats when one group maps to more than one role. |
| iam_group | role_code | varchar(20) | NO | UK (entra_group, role_code) | Entra ID |  | New table. Entra ID group to Workbench role mapping. Business key (entra_group, role_code); iam_group_key is the Entra group object ID and repeats when one group maps to more than one role. |
| iam_group | source_system | varchar(20) | NO |  | Entra ID |  | New table. Entra ID group to Workbench role mapping. Business key (entra_group, role_code); iam_group_key is the Entra group object ID and repeats when one group maps to more than one role. |
| iam_group | business_date | date | NO |  | Entra ID |  | New table. Entra ID group to Workbench role mapping. Business key (entra_group, role_code); iam_group_key is the Entra group object ID and repeats when one group maps to more than one role. |
| iam_group | loaded_at | timestamptz(6) | NO |  | Entra ID |  | New table. Entra ID group to Workbench role mapping. Business key (entra_group, role_code); iam_group_key is the Entra group object ID and repeats when one group maps to more than one role. |
| account | business_unit | varchar(10) | YES |  | ALS | DF-ACC-006 | New column on an existing ACE table. |
| account | principal_outstanding | numeric(18,2) | YES |  | ALS | DF-ACC-009 | New column on an existing ACE table. |
| account | interest_outstanding | numeric(18,2) | YES |  | ALS | DF-ACC-010 | New column on an existing ACE table. |
| account | fees_outstanding | numeric(18,2) | YES |  | ALS | DF-ACC-011 | New column on an existing ACE table. |
| account | daily_bucket | varchar(10) | YES |  | ALS | DF-ACC-015 | New column on an existing ACE table. |
| account | settlement_booked_date | date | YES |  | ALS | DF-ACC-030 | New column on an existing ACE table. |
| account | settlement_booked_amount | numeric(18,2) | YES |  | ALS | DF-ACC-031 | New column on an existing ACE table. |
| customer | party_type | varchar(15) | YES |  | SCBPDM | DF-PTY-003 | New column on an existing ACE table. |
| customer | id_type | varchar(20) | YES |  | SCBPDM | DF-PTY-006 | New column on an existing ACE table. |
| customer | segment | varchar(20) | YES |  | SCBPDM | DF-PTY-009 | New column on an existing ACE table. |
| efs_action | contact_result | varchar(20) | YES |  | EFS | DF-INT-008, DF-INT-036 | New column on an existing ACE table. |
| efs_action | action_contact_status | varchar(20) | YES |  | EFS | DF-INT-035 | New column on an existing ACE table. |

## Counts

| Item | v4 today | v5 target | Arithmetic |
|---|---|---|---|
| Workbench tables | 108 | 92 | 108 - 20 removed + 4 extension |
| Views | 0 | 30 | 16 Tier 1 + 14 Tier 2 |
| Dictionary objects | 108 | 122 | 92 tables + 30 views |
| Dictionary fields | 1256 | 1366 | 1256 - 243 removed + 49 extension + 304 view |
| Source fields with an external source | 133 | 133 | 51 ACE reuse + 81 ACE new + 1 extension |
| New ACE tables (RWB-ACE-001) | 0 | 14 |  |
| New ACE columns (RWB-ACE-001) | 0 | 12 | account 7, customer 3, efs_action 2 |
| New ACE columns in total | 0 | 166 | 154 in the 14 new tables + 12 on existing tables |
| Foreign keys into public.* | 0 | 0 | Boundary rule |
| UUID foreign keys into a source copy | 23 | 0 | 14 re-keyed, 9 leave with their table |
| Distinct ACE columns behind the ACE-new fields | 0 | 79 | 81 fields; efs_action.contact_result serves DF-INT-008 and DF-INT-036, and collins_score.model_version serves DF-DEC-006 and DF-DEC-023 |
| ACE tables the 30 views read (ace_view_owner SELECT grant) | 0 | 35 | 21 Tier 1 tables read by Section A + 14 Tier 2 tables (D2) |
