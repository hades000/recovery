<!-- source: 04 User stories/Recovery Workbench ACE Team Stories v1.xlsx -->
<!-- converted: 2026-11-16 from XLSX -->

> **Source:** `04 User stories/Recovery Workbench ACE Team Stories v1.xlsx`  
> **Converted from:** XLSX

## Story

| Story key | RWB-ACE-001 |
|---|---|
| Title | ACE DB additions for the Recovery Workbench |
| Owner | ACE team |
| Epic | ACE backlog, release 30 November 2026 |
| Feature | FEAT-RDF-26 ACE DB additions (ACE team) |
| Requirement IDs | REQ-RDF-001, REQ-RDF-002 |
| Decision | D-RCV-35 (U1, U2); DL43 |
| Priority | Must - critical path |
| Depends on | None |
| Blocks | RWB-E1-069, RWB-E1-002, RWB-E1-016, RWB-E1-018 |
| Status | Ready for the ACE team estimate (DL43) |
| Story | As the ACE team lead, I want the tables and columns the recovery module needs but ACE does not hold added to ACE, ingested by the existing ingestion and recorded with a business date, so that the recovery module reads one copy of source data through its views. |

## Fields

| Field ID | Workbench entity | Workbench field | Source system | Source field | ACE table | ACE column | Type | Frequency | Read through |
|---|---|---|---|---|---|---|---|---|---|
| DF-PTY-003 | party | party_type | SCBPDM via COLLINS |  | customer | party_type |  | Daily, end of day | v_ace_customer.party_type |
| DF-PTY-006 | party | id_type | SCBPDM via COLLINS |  | customer | id_type |  | Daily, end of day | v_ace_customer.id_type |
| DF-PTY-009 | party | segment | SCBPDM via COLLINS | Segment | customer | segment |  | Daily, end of day | v_ace_customer.segment |
| DF-ACC-006 | loan_account | business_unit | Core bank (ALS) via COLLINS | BU | account | business_unit |  |  | v_ace_account.business_unit |
| DF-ACC-009 | loan_account | principal_outstanding | Core bank (ALS) via COLLINS | Principal | account | principal_outstanding |  |  | v_ace_account.principal_outstanding |
| DF-ACC-010 | loan_account | interest_outstanding | Core bank (ALS) via COLLINS | AINT1 + AINT2 | account | interest_outstanding |  |  | v_ace_account.interest_outstanding |
| DF-ACC-011 | loan_account | fees_outstanding | Core bank (ALS) via COLLINS | AFEE | account | fees_outstanding |  |  | v_ace_account.fees_outstanding |
| DF-ACC-015 | loan_account | bucket | Core bank (ALS) via COLLINS | Bucket | account | daily_bucket |  |  | v_ace_account.bucket |
| DF-ACC-030 | loan_account | settlement_booked_date | Core bank (ALS) via COLLINS |  | account | settlement_booked_date |  |  | v_ace_account.settlement_booked_date |
| DF-ACC-031 | loan_account | settlement_booked_amount | Core bank (ALS) via COLLINS |  | account | settlement_booked_amount |  |  | v_ace_account.settlement_booked_amount |
| DF-COL-004 | collateral | title_doc_no | CCMS | Title Deed / Ownership Doc | collateral_detail | title_doc_no | varchar(40) | Weekly | v_ace_collateral_detail.title_doc_no |
| DF-COL-005 | collateral | plot_no | CCMS | Plot No. | collateral_detail | plot_no | varchar(20) | Weekly | v_ace_collateral_detail.plot_no |
| DF-COL-006 | collateral | area_text | CCMS | Area | collateral_detail | area_text | varchar(20) | Weekly | v_ace_collateral_detail.area_text |
| DF-COL-007 | collateral | province | CCMS | Province | collateral_detail | province | varchar(40) | Weekly | v_ace_collateral_detail.province |
| DF-COL-008 | collateral | district | CCMS | District | collateral_detail | district | varchar(60) | Weekly | v_ace_collateral_detail.district |
| DF-COL-009 | collateral | subdistrict | CCMS | Subdistrict | collateral_detail | subdistrict | varchar(60) | Weekly | v_ace_collateral_detail.subdistrict |
| DF-COL-012 | collateral | insured_value | CCMS | Insvalue | collateral_detail | insured_value | numeric(18,2) | Weekly | v_ace_collateral_detail.insured_value |
| DF-COL-013 | collateral | insurance_expiry | CCMS |  | collateral_detail | insurance_expiry | date | Weekly | v_ace_collateral_detail.insurance_expiry |
| DF-COL-017 | account_collateral | lien_rank | CCMS |  | collateral_detail | lien_rank | integer | Weekly | v_ace_collateral_detail.lien_rank |
| DF-COL-021 | valuation | appraisal_no | SVAF | Appraisal No. | valuation | appraisal_no | varchar(20) | Weekly | v_ace_valuation.appraisal_no |
| DF-COL-022 | valuation | appraisal_type | SVAF |  | valuation | appraisal_type | varchar(15) | Weekly | v_ace_valuation.appraisal_type |
| DF-COL-023 | valuation | appraised_value | SVAF | Appraised Value | valuation | appraised_value | numeric(18,2) | Weekly | v_ace_valuation.appraised_value |
| DF-COL-024 | valuation | forced_sale_value | SVAF | Forced Sale Value | valuation | forced_sale_value | numeric(18,2) | Weekly | v_ace_valuation.forced_sale_value |
| DF-COL-025 | valuation | appraisal_date | SVAF | Appraisal Date | valuation | appraisal_date | date | Weekly | v_ace_valuation.appraisal_date |
| DF-COL-032 | asset | asset_code | AMIS | Asset Code | npa_asset | asset_code | varchar(20) | Monthly | v_ace_npa_asset.asset_code |
| DF-COL-034 | asset | transfer_in_type | AMIS | Transfer-in Type | npa_asset | transfer_in_type | varchar(20) | Monthly | v_ace_npa_asset.transfer_in_type |
| DF-COL-035 | asset | from_segment | AMIS | From Segment | npa_asset | from_segment | varchar(20) | Monthly | v_ace_npa_asset.from_segment |
| DF-COL-036 | asset | transfer_in_date | AMIS | Ownership Transfer in Date | npa_asset | transfer_in_date | date | Monthly | v_ace_npa_asset.transfer_in_date |
| DF-COL-037 | asset | book_value | AMIS | Book  Value | npa_asset | book_value | numeric(18,2) | Monthly | v_ace_npa_asset.book_value |
| DF-COL-038 | asset | auction_purchase_price | AMIS | Auction Purchase Price | npa_asset | auction_purchase_price | numeric(18,2) | Monthly | v_ace_npa_asset.auction_purchase_price |
| DF-COL-039 | asset | repossessed_date | RPS | ReposessedCarDate | npa_asset | repossessed_date | date | Weekly | v_ace_npa_asset.repossessed_date |
| DF-COL-040 | asset | stock_date | RPS | STOCK_DATE | npa_asset | stock_date | date | Weekly | v_ace_npa_asset.stock_date |
| DF-TRT-023 | treatment | nleads_ref | NLEADS |  | credit_decision | nleads_ref | varchar(30) | On decision | v_ace_credit_decision.nleads_ref |
| DF-TRT-024 | treatment | credit_result | NLEADS |  | credit_decision | credit_result | varchar(10) | On decision | v_ace_credit_decision.credit_result |
| DF-TRT-025 | treatment | credit_result_reason | NLEADS |  | credit_decision | credit_result_reason | varchar(1000) | On decision | v_ace_credit_decision.credit_result_reason |
| DF-TRT-026 | treatment | credit_result_at | NLEADS |  | credit_decision | decided_at | timestamptz(6) | On decision | v_ace_credit_decision.decided_at |
| DF-LEG-005 | legal_action | lawsuit_no | LIT | LAWSUIT_NO / LAWSUIT_RUN | lawsuit | lawsuit_no | varchar(30) | Daily, end of day | v_ace_lawsuit.lawsuit_no |
| DF-LEG-006 | legal_action | black_case_no | LIT | เลขที่คดีดำ | lawsuit | black_case_no | varchar(30) | Daily, end of day | v_ace_lawsuit.black_case_no |
| DF-LEG-007 | legal_action | red_case_no | LIT |  | lawsuit | red_case_no | varchar(30) | Daily, end of day | v_ace_lawsuit.red_case_no |
| DF-LEG-008 | legal_action | court_name | LIT | NCOURT | lawsuit | court_name | varchar(120) | Daily, end of day | v_ace_lawsuit.court_name |
| DF-LEG-009 | legal_action | claim_amount | LIT | AAMT_SUIT | lawsuit | claim_amount | numeric(18,2) | Daily, end of day | v_ace_lawsuit.claim_amount |
| DF-LEG-010 | legal_action | filed_date | LIT |  | lawsuit | filed_date | date | Daily, end of day | v_ace_lawsuit.filed_date |
| DF-LEG-011 | legal_action | judgment_date | LIT | Judgment date | lawsuit | judgment_date | date | Daily, end of day | v_ace_lawsuit.judgment_date |
| DF-LEG-012 | legal_action | judgment_amount | LIT |  | lawsuit | judgment_amount | numeric(18,2) | Daily, end of day | v_ace_lawsuit.judgment_amount |
| DF-LEG-013 | legal_action | lit_status | LIT via COLLINS | STATE_RES_NAME | lawsuit | lit_status | varchar(200) | Daily, end of day | v_ace_lawsuit.lit_status |
| DF-LEG-019 | notice | sent_date | WIN | DDMMYYYY | pod_receipt | sent_date | date | Weekly | v_ace_pod.sent_date |
| DF-LEG-020 | notice | barcode | WIN | Barcode | pod_receipt | barcode | varchar(40) | Weekly | v_ace_pod.barcode |
| DF-LEG-021 | notice | callback_date | WIN | DDMMYYYY_callBack | pod_receipt | callback_date | date | Weekly | v_ace_pod.callback_date |
| DF-LEG-022 | notice | delivery_status | WIN |  | pod_receipt | delivery_status | varchar(15) | Weekly | v_ace_pod.delivery_status |
| DF-LEG-023 | notice | sent_type | WIN | Sent Type | pod_receipt | sent_type | varchar(10) | Weekly | v_ace_pod.sent_type |
| DF-LEG-026 | hearing | hearing_date | LIT |  | hearing | hearing_date | timestamptz(6) | Daily, end of day | v_ace_hearing.hearing_date |
| DF-LEG-027 | hearing | hearing_type | LIT |  | hearing | hearing_type | varchar(20) | Daily, end of day | v_ace_hearing.hearing_type |
| DF-LEG-029 | hearing | next_date | LIT |  | hearing | next_date | timestamptz(6) | Daily, end of day | v_ace_hearing.next_date |
| DF-SAL-012 | asset_sale | contract_date | AMIS | Contract Date | npa_sale | contract_date | date | Monthly | v_ace_npa_sale.contract_date |
| DF-SAL-013 | asset_sale | sale_date | AMIS | Sale Date | npa_sale | sale_date | date | Monthly | v_ace_npa_sale.sale_date |
| DF-SAL-014 | asset_sale | sale_price | AMIS | Sale Price | npa_sale | sale_price | numeric(18,2) | Monthly | v_ace_npa_sale.sale_price |
| DF-SAL-015 | asset_sale | transfer_fee | AMIS | Sale Transfer Fee | npa_sale | transfer_fee | numeric(18,2) | Monthly | v_ace_npa_sale.transfer_fee |
| DF-SAL-016 | asset_sale | specific_business_tax | AMIS | Specific Business Tax | npa_sale | specific_business_tax | numeric(18,2) | Monthly | v_ace_npa_sale.specific_business_tax |
| DF-SAL-017 | asset_sale | corporate_income_tax | AMIS | Corporate Income Tax | npa_sale | corporate_income_tax | numeric(18,2) | Monthly | v_ace_npa_sale.corporate_income_tax |
| DF-SAL-019 | asset_sale | incentive_amount | AMIS | Incentive Amount | npa_sale | incentive_amount | numeric(18,2) | Monthly | v_ace_npa_sale.incentive_amount |
| DF-INT-008 | interaction | contact_result | EFS via COLLINS | Call Result | efs_action | contact_result |  | Daily, end of day | v_ace_efs_action.contact_result |
| DF-DEC-022 | score | model_code | COLLINS |  | collins_score | model_code | varchar(30) | Daily, end of day | v_ace_score.model_code |
| DF-DEC-023 | score | model_version | COLLINS |  | collins_score | model_version | varchar(20) | Daily, end of day | v_ace_score.model_version |
| DF-DEC-024 | score | score_value | COLLINS |  | collins_score | score_value | numeric(12,4) | Daily, end of day | v_ace_score.score_value |
| DF-DEC-025 | score | estimate_value | COLLINS |  | collins_score | estimate_value | numeric(18,2) | Daily, end of day | v_ace_score.estimate_value |
| DF-DEC-026 | score | route_code | COLLINS |  | collins_score | route_code | varchar(4) | Daily, end of day | v_ace_score.route_code |
| DF-DEC-027 | score | scored_at | COLLINS |  | collins_score | scored_at | date | Daily, end of day | v_ace_score.scored_at |
| DF-FIN-013 | write_off | amount | GL | AMT | gl_write_off | amount | numeric(18,2) | Monthly | v_ace_write_off.amount |
| DF-FIN-016 | write_off | posted_date | GL | DATE | gl_write_off | posted_date | date | Monthly | v_ace_write_off.posted_date |
| DF-FIN-017 | write_off | responsibility_center | GL | RC | gl_write_off | responsibility_center | varchar(10) | Monthly | v_ace_write_off.responsibility_center |
| DF-FIN-018 | write_off | cost_center | GL | OC | gl_write_off | cost_center | varchar(10) | Monthly | v_ace_write_off.cost_center |
| DF-FIN-019 | write_off | gl_product | GL | PRODUCT | gl_write_off | gl_product | varchar(10) | Monthly | v_ace_write_off.gl_product |
| DF-REF-039 | role | entra_group | Entra ID |  | iam_group | entra_group | varchar(120) | On change | v_ace_iam_group.entra_group |
| DF-INT-035 | collections_history | action_contact_status | EFS via COLLINS |  | efs_action | action_contact_status |  | Daily, end of day | v_ace_efs_action.action_contact_status |
| DF-INT-036 | collections_history | contact_result | EFS via COLLINS | Call Result | efs_action | contact_result |  | Daily, end of day | v_ace_efs_action.contact_result |
| DF-PTY-024 | party_product | product_type | SCBPDM via COLLINS |  | party_product | product_type | varchar(20) | Daily, end of day | v_ace_party_product.product_type |
| DF-PTY-025 | party_product | account_no | SCBPDM via COLLINS |  | party_product | account_key | varchar(255) | Daily, end of day | v_ace_party_product.account_no |
| DF-PTY-026 | party_product | product_status | SCBPDM via COLLINS |  | party_product | product_status | varchar(15) | Daily, end of day | v_ace_party_product.product_status |
| DF-PTY-027 | party_product | data_as_of | SCBPDM via COLLINS |  | party_product | business_date | date | Daily, end of day | v_ace_party_product.data_as_of |
| DF-DOC-103 | signature_request | external_ref | EasyApp |  | esign_request | external_ref | varchar(60) | On request | v_ace_esign.external_ref |

## Tables

| Table | Column | Type | Nullable | Key | Source | Field ID |
|---|---|---|---|---|---|---|
| ace_batch_run | id | bigint | YES | PK | All sources |  |
| ace_batch_run | source_system | varchar(20) | NO |  | All sources |  |
| ace_batch_run | business_date | date | NO |  | All sources |  |
| ace_batch_run | started_at | timestamptz(6) | NO |  | All sources |  |
| ace_batch_run | completed_at | timestamptz(6) | YES |  | All sources |  |
| ace_batch_run | status | varchar(12) | NO |  | All sources |  |
| ace_batch_run | record_count | bigint | YES |  | All sources |  |
| ace_batch_run | checksum | varchar(64) | YES |  | All sources |  |
| ace_batch_run | feed_version | varchar(20) | YES |  | All sources |  |
| collateral_detail | id | bigint | YES | PK | CCMS |  |
| collateral_detail | collateral_detail_key | varchar(255) | NO |  | CCMS |  |
| collateral_detail | asset_key | varchar(255) | NO | FK | CCMS |  |
| collateral_detail | title_doc_no | varchar(40) | YES |  | CCMS | DF-COL-004 |
| collateral_detail | plot_no | varchar(20) | YES |  | CCMS | DF-COL-005 |
| collateral_detail | area_text | varchar(20) | YES |  | CCMS | DF-COL-006 |
| collateral_detail | province | varchar(40) | YES |  | CCMS | DF-COL-007 |
| collateral_detail | district | varchar(60) | YES |  | CCMS | DF-COL-008 |
| collateral_detail | subdistrict | varchar(60) | YES |  | CCMS | DF-COL-009 |
| collateral_detail | insured_value | numeric(18,2) | YES |  | CCMS | DF-COL-012 |
| collateral_detail | insurance_expiry | date | YES |  | CCMS | DF-COL-013 |
| collateral_detail | lien_rank | integer | YES |  | CCMS | DF-COL-017 |
| collateral_detail | source_system | varchar(20) | NO |  | CCMS |  |
| collateral_detail | business_date | date | NO |  | CCMS |  |
| collateral_detail | loaded_at | timestamptz(6) | NO |  | CCMS |  |
| valuation | id | bigint | YES | PK | SVAF |  |
| valuation | valuation_key | varchar(255) | NO |  | SVAF |  |
| valuation | asset_key | varchar(255) | NO | FK | SVAF |  |
| valuation | appraisal_no | varchar(20) | YES |  | SVAF | DF-COL-021 |
| valuation | appraisal_type | varchar(15) | YES |  | SVAF | DF-COL-022 |
| valuation | appraised_value | numeric(18,2) | YES |  | SVAF | DF-COL-023 |
| valuation | forced_sale_value | numeric(18,2) | YES |  | SVAF | DF-COL-024 |
| valuation | appraisal_date | date | YES |  | SVAF | DF-COL-025 |
| valuation | source_system | varchar(20) | NO |  | SVAF |  |
| valuation | business_date | date | NO |  | SVAF |  |
| valuation | loaded_at | timestamptz(6) | NO |  | SVAF |  |
| npa_asset | id | bigint | YES | PK | AMIS, RPS |  |
| npa_asset | npa_asset_key | varchar(255) | NO |  | AMIS, RPS |  |
| npa_asset | asset_key | varchar(255) | NO | FK | AMIS, RPS |  |
| npa_asset | asset_code | varchar(20) | YES |  | AMIS, RPS | DF-COL-032 |
| npa_asset | transfer_in_type | varchar(20) | YES |  | AMIS, RPS | DF-COL-034 |
| npa_asset | from_segment | varchar(20) | YES |  | AMIS, RPS | DF-COL-035 |
| npa_asset | transfer_in_date | date | YES |  | AMIS, RPS | DF-COL-036 |
| npa_asset | book_value | numeric(18,2) | YES |  | AMIS, RPS | DF-COL-037 |
| npa_asset | auction_purchase_price | numeric(18,2) | YES |  | AMIS, RPS | DF-COL-038 |
| npa_asset | repossessed_date | date | YES |  | AMIS, RPS | DF-COL-039 |
| npa_asset | stock_date | date | YES |  | AMIS, RPS | DF-COL-040 |
| npa_asset | source_system | varchar(20) | NO |  | AMIS, RPS |  |
| npa_asset | business_date | date | NO |  | AMIS, RPS |  |
| npa_asset | loaded_at | timestamptz(6) | NO |  | AMIS, RPS |  |
| npa_sale | id | bigint | YES | PK | AMIS |  |
| npa_sale | npa_sale_key | varchar(255) | NO |  | AMIS |  |
| npa_sale | npa_asset_key | varchar(255) | NO | FK | AMIS |  |
| npa_sale | contract_date | date | YES |  | AMIS | DF-SAL-012 |
| npa_sale | sale_date | date | YES |  | AMIS | DF-SAL-013 |
| npa_sale | sale_price | numeric(18,2) | YES |  | AMIS | DF-SAL-014 |
| npa_sale | transfer_fee | numeric(18,2) | YES |  | AMIS | DF-SAL-015 |
| npa_sale | specific_business_tax | numeric(18,2) | YES |  | AMIS | DF-SAL-016 |
| npa_sale | corporate_income_tax | numeric(18,2) | YES |  | AMIS | DF-SAL-017 |
| npa_sale | incentive_amount | numeric(18,2) | YES |  | AMIS | DF-SAL-019 |
| npa_sale | source_system | varchar(20) | NO |  | AMIS |  |
| npa_sale | business_date | date | NO |  | AMIS |  |
| npa_sale | loaded_at | timestamptz(6) | NO |  | AMIS |  |
| lawsuit | id | bigint | YES | PK | LIT |  |
| lawsuit | lawsuit_key | varchar(255) | NO |  | LIT |  |
| lawsuit | account_key | varchar(255) | NO | FK | LIT |  |
| lawsuit | lawsuit_no | varchar(30) | YES |  | LIT | DF-LEG-005 |
| lawsuit | black_case_no | varchar(30) | YES |  | LIT | DF-LEG-006 |
| lawsuit | red_case_no | varchar(30) | YES |  | LIT | DF-LEG-007 |
| lawsuit | court_name | varchar(120) | YES |  | LIT | DF-LEG-008 |
| lawsuit | claim_amount | numeric(18,2) | YES |  | LIT | DF-LEG-009 |
| lawsuit | filed_date | date | YES |  | LIT | DF-LEG-010 |
| lawsuit | judgment_date | date | YES |  | LIT | DF-LEG-011 |
| lawsuit | judgment_amount | numeric(18,2) | YES |  | LIT | DF-LEG-012 |
| lawsuit | lit_status | varchar(200) | YES |  | LIT | DF-LEG-013 |
| lawsuit | source_system | varchar(20) | NO |  | LIT |  |
| lawsuit | business_date | date | NO |  | LIT |  |
| lawsuit | loaded_at | timestamptz(6) | NO |  | LIT |  |
| hearing | id | bigint | YES | PK | LIT |  |
| hearing | hearing_key | varchar(255) | NO |  | LIT |  |
| hearing | lawsuit_key | varchar(255) | NO | FK | LIT |  |
| hearing | hearing_date | timestamptz(6) | NO |  | LIT | DF-LEG-026 |
| hearing | hearing_type | varchar(20) | YES |  | LIT | DF-LEG-027 |
| hearing | next_date | timestamptz(6) | YES |  | LIT | DF-LEG-029 |
| hearing | source_system | varchar(20) | NO |  | LIT |  |
| hearing | business_date | date | NO |  | LIT |  |
| hearing | loaded_at | timestamptz(6) | NO |  | LIT |  |
| pod_receipt | id | bigint | YES | PK | WIN |  |
| pod_receipt | pod_key | varchar(255) | NO |  | WIN |  |
| pod_receipt | account_key | varchar(255) | NO | FK | WIN |  |
| pod_receipt | notice_ref | varchar(60) | YES |  | WIN |  |
| pod_receipt | sent_date | date | YES |  | WIN | DF-LEG-019 |
| pod_receipt | barcode | varchar(40) | YES |  | WIN | DF-LEG-020 |
| pod_receipt | callback_date | date | YES |  | WIN | DF-LEG-021 |
| pod_receipt | delivery_status | varchar(15) | YES |  | WIN | DF-LEG-022 |
| pod_receipt | sent_type | varchar(10) | YES |  | WIN | DF-LEG-023 |
| pod_receipt | source_system | varchar(20) | NO |  | WIN |  |
| pod_receipt | business_date | date | NO |  | WIN |  |
| pod_receipt | loaded_at | timestamptz(6) | NO |  | WIN |  |
| gl_write_off | id | bigint | YES | PK | GL |  |
| gl_write_off | write_off_key | varchar(255) | NO |  | GL |  |
| gl_write_off | account_key | varchar(255) | NO | FK | GL |  |
| gl_write_off | amount | numeric(18,2) | NO |  | GL | DF-FIN-013 |
| gl_write_off | posted_date | date | YES |  | GL | DF-FIN-016 |
| gl_write_off | responsibility_center | varchar(10) | YES |  | GL | DF-FIN-017 |
| gl_write_off | cost_center | varchar(10) | YES |  | GL | DF-FIN-018 |
| gl_write_off | gl_product | varchar(10) | YES |  | GL | DF-FIN-019 |
| gl_write_off | source_system | varchar(20) | NO |  | GL |  |
| gl_write_off | business_date | date | NO |  | GL |  |
| gl_write_off | loaded_at | timestamptz(6) | NO |  | GL |  |
| collins_score | id | bigint | YES | PK | COLLINS |  |
| collins_score | score_key | varchar(255) | NO |  | COLLINS |  |
| collins_score | account_key | varchar(255) | NO | FK | COLLINS |  |
| collins_score | model_code | varchar(30) | NO |  | COLLINS | DF-DEC-022 |
| collins_score | model_version | varchar(20) | NO |  | COLLINS | DF-DEC-023 |
| collins_score | score_value | numeric(12,4) | YES |  | COLLINS | DF-DEC-024 |
| collins_score | estimate_value | numeric(18,2) | YES |  | COLLINS | DF-DEC-025 |
| collins_score | route_code | varchar(4) | YES |  | COLLINS | DF-DEC-026 |
| collins_score | scored_at | date | NO |  | COLLINS | DF-DEC-027 |
| collins_score | source_system | varchar(20) | NO |  | COLLINS |  |
| collins_score | business_date | date | NO |  | COLLINS |  |
| collins_score | loaded_at | timestamptz(6) | NO |  | COLLINS |  |
| party_product | id | bigint | YES | PK | SCBPDM |  |
| party_product | person_key | varchar(255) | NO | FK | SCBPDM |  |
| party_product | account_key | varchar(255) | NO |  | SCBPDM | DF-PTY-025 |
| party_product | product_type | varchar(20) | NO |  | SCBPDM | DF-PTY-024 |
| party_product | product_status | varchar(15) | NO |  | SCBPDM | DF-PTY-026 |
| party_product | business_date | date | NO |  | SCBPDM | DF-PTY-027 |
| party_product | loaded_at | timestamptz(6) | NO |  | SCBPDM |  |
| credit_decision | id | bigint | YES | PK | NLEADS |  |
| credit_decision | credit_decision_key | varchar(255) | NO |  | NLEADS |  |
| credit_decision | account_key | varchar(255) | NO | FK | NLEADS |  |
| credit_decision | nleads_ref | varchar(30) | YES |  | NLEADS | DF-TRT-023 |
| credit_decision | credit_result | varchar(10) | YES |  | NLEADS | DF-TRT-024 |
| credit_decision | credit_result_reason | varchar(1000) | YES |  | NLEADS | DF-TRT-025 |
| credit_decision | decided_at | timestamptz(6) | YES |  | NLEADS | DF-TRT-026 |
| credit_decision | source_system | varchar(20) | NO |  | NLEADS |  |
| credit_decision | business_date | date | NO |  | NLEADS |  |
| credit_decision | loaded_at | timestamptz(6) | NO |  | NLEADS |  |
| esign_request | id | bigint | YES | PK | EasyApp |  |
| esign_request | esign_key | varchar(255) | NO |  | EasyApp |  |
| esign_request | account_key | varchar(255) | NO | FK | EasyApp |  |
| esign_request | external_ref | varchar(60) | YES |  | EasyApp | DF-DOC-103 |
| esign_request | requested_at | timestamptz(6) | YES |  | EasyApp |  |
| esign_request | status | varchar(20) | YES |  | EasyApp |  |
| esign_request | source_system | varchar(20) | NO |  | EasyApp |  |
| esign_request | business_date | date | NO |  | EasyApp |  |
| esign_request | loaded_at | timestamptz(6) | NO |  | EasyApp |  |
| iam_group | id | bigint | YES | PK | Entra ID |  |
| iam_group | iam_group_key | varchar(255) | NO |  | Entra ID |  |
| iam_group | entra_group | varchar(120) | NO |  | Entra ID | DF-REF-039 |
| iam_group | role_code | varchar(20) | NO |  | Entra ID |  |
| iam_group | source_system | varchar(20) | NO |  | Entra ID |  |
| iam_group | business_date | date | NO |  | Entra ID |  |
| iam_group | loaded_at | timestamptz(6) | NO |  | Entra ID |  |
| account | business_unit | varchar(10) | YES |  | ALS | DF-ACC-006 |
| account | principal_outstanding | numeric(18,2) | YES |  | ALS | DF-ACC-009 |
| account | interest_outstanding | numeric(18,2) | YES |  | ALS | DF-ACC-010 |
| account | fees_outstanding | numeric(18,2) | YES |  | ALS | DF-ACC-011 |
| account | daily_bucket | varchar(10) | YES |  | ALS | DF-ACC-015 |
| account | settlement_booked_date | date | YES |  | ALS | DF-ACC-030 |
| account | settlement_booked_amount | numeric(18,2) | YES |  | ALS | DF-ACC-031 |
| customer | party_type | varchar(15) | YES |  | SCBPDM | DF-PTY-003 |
| customer | id_type | varchar(20) | YES |  | SCBPDM | DF-PTY-006 |
| customer | segment | varchar(20) | YES |  | SCBPDM | DF-PTY-009 |
| efs_action | contact_result | varchar(20) | YES |  | EFS | DF-INT-008, DF-INT-036 |
| efs_action | action_contact_status | varchar(20) | YES |  | EFS | DF-INT-035 |

## Acceptance criteria

| AC | Title | Gherkin |
|---|---|---|
| AC1 | Tables and columns deployed | Given the ACE schema at the common migration head, when V027 is applied in DEV and SIT, then the 14 tables and 12 columns exist, ace_batch_run has its keys, and no existing column changes. |
| AC2 | Every Workbench field is populated | Given one full file per source, when ACE ingests each for 2026-11-30, then all 80 fields hold a value or an explicit null and each target count equals the trailer. |
| AC3 | Business date and completion recorded | Given the ALS file for 2026-11-30 completes at 04:40, when the Workbench reads v_ace_batch_status, then it returns ALS, 2026-11-30, COMPLETED, the count and the time; a later failed run does not replace it. |
| AC4 | Read grant only | Given the view-owner role, when the grant is applied, then it selects the 14 new tables and writes nothing; the 12 new columns are covered by the Tier 1 grant. |
| AC5 | Reversible | Given a copy with the migration applied, when the down script runs, then the 14 tables and 12 columns are gone and ACE row counts are unchanged. |
| AC6 | Existing ACE reads unaffected | Given the ACE regression suite, when it runs after the migration, then every existing screen, job and report passes. |
| AC7 | Idempotent reload | Given a file already ingested for a business date, when it is ingested again, then no duplicate row exists and one batch row remains. |
| AC8 | Field appendix matches | Given the 80 appendix rows, when the conformance test runs, then 80 of 80 resolve to a column of the right type. |

## Tests

| Test | Covers | Level | Data |
|---|---|---|---|
| TC-ACE-001-01 | AC1 Tables and columns deployed | System | One full file per source, business date 2026-11-30; SIT ACE schema at V027 |
| TC-ACE-001-02 | AC2 Every Workbench field is populated | System | One full file per source, business date 2026-11-30; SIT ACE schema at V027 |
| TC-ACE-001-03 | AC3 Business date and completion recorded | System | One full file per source, business date 2026-11-30; SIT ACE schema at V027 |
| TC-ACE-001-04 | AC4 Read grant only | System | One full file per source, business date 2026-11-30; SIT ACE schema at V027 |
| TC-ACE-001-05 | AC5 Reversible | System | One full file per source, business date 2026-11-30; SIT ACE schema at V027 |
| TC-ACE-001-06 | AC6 Existing ACE reads unaffected | System | One full file per source, business date 2026-11-30; SIT ACE schema at V027 |
| TC-ACE-001-07 | AC7 Idempotent reload | System | One full file per source, business date 2026-11-30; SIT ACE schema at V027 |
| TC-ACE-001-08 | AC8 Field appendix matches | System | One full file per source, business date 2026-11-30; SIT ACE schema at V027 |
