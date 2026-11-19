<!-- source: 06 Data/Recovery Workbench Source to Target Mapping v3.xlsx -->
<!-- converted: 2026-11-16 from XLSX -->

> **Source:** `06 Data/Recovery Workbench Source to Target Mapping v3.xlsx`  
> **Converted from:** XLSX

## Mapping

| Source field to Workbench field |  |  |  |  |  |  |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 110 fields that arrive from another system, with the source field, the transformation and the refresh. The system owners confirm each source field. |  |  |  |  |  |  |  |  |  |  |  |  |
| Data product | Entity | Field | Data type | Physical type | Mandatory | Source system | Path | Source field | Transformation | Refresh | Interface | Status |
| DP03 | recovery_case | product_group | LOV | varchar(15) | Yes | Core bank (ALS) | COLLINS | Product_Category_Host | Source code mapped to LOV-PRODUCT through the code map; an unmapped code is held in the exception list | Daily, end of day | INT-01, INT-02 | To confirm with the system owner |
| DP03 | recovery_case | dpd_at_entry | NUMBER | integer | Yes | Core bank (ALS) | COLLINS | DELAY_DAYS | Converted to integer; amounts in THB | Daily, end of day | INT-01, INT-02 | To confirm with the system owner |
| DP03 | recovery_case | total_outstanding_at_entry | NUMBER | numeric(18,2) | Yes | Core bank (ALS) | COLLINS | TOTAL_BALANCE | Converted to numeric(18,2); amounts in THB | Daily, end of day | INT-01, INT-02 | To confirm with the system owner |
| DP02 | party | cif_no | TEXT | varchar(20) | Yes | SCBPDM | COLLINS | CIF | Copied; trimmed | Daily, end of day | INT-04 | To confirm with the system owner |
| DP02 | party | party_type | LOV | varchar(15) | Yes | SCBPDM | COLLINS | To confirm with the system owner | Source code mapped to LOV-PARTY-TYPE through the code map; an unmapped code is held in the exception list | Daily, end of day | INT-04 | To confirm with the system owner |
| DP02 | party | first_name | TEXT | varchar(100) | Yes | SCBPDM | COLLINS | To confirm with the system owner | Copied; trimmed | Daily, end of day | INT-04 | To confirm with the system owner |
| DP02 | party | last_name | TEXT | varchar(100) | No | SCBPDM | COLLINS | To confirm with the system owner | Copied; trimmed | Daily, end of day | INT-04 | To confirm with the system owner |
| DP02 | party | id_type | LOV | varchar(20) | Yes | SCBPDM | COLLINS | To confirm with the system owner | Source code mapped to LOV-ID-TYPE through the code map; an unmapped code is held in the exception list | Daily, end of day | INT-04 | To confirm with the system owner |
| DP02 | party | id_no_token | TEXT | varchar(64) | Yes | SCBPDM | COLLINS | To confirm with the system owner | Tokenized at load; the clear value is not stored | Daily, end of day | INT-04 | To confirm with the system owner |
| DP02 | party | date_of_birth | DATE | date | No | SCBPDM | COLLINS | To confirm with the system owner | Converted to a date; Buddhist Era years converted to Gregorian | Daily, end of day | INT-04 | To confirm with the system owner |
| DP02 | party | segment | LOV | varchar(20) | No | SCBPDM | COLLINS | Segment | Source code mapped to LOV-SEGMENT through the code map; an unmapped code is held in the exception list | Daily, end of day | INT-04 | To confirm with the system owner |
| DP02 | contact_point | value_token | TEXT | varchar(256) | Yes | SCBPDM | COLLINS | To confirm with the system owner | Masked at load | Daily, end of day | INT-04 | To confirm with the system owner |
| DP01 | loan_account | account_no | TEXT | varchar(20) | Yes | Core bank (ALS) | COLLINS | ACCOUNT_KEY / iacct / AccNo | Copied; trimmed | Daily, end of day | INT-01, INT-02 | To confirm with the system owner |
| DP01 | loan_account | contract_no | TEXT | varchar(20) | No | Core bank (ALS) | COLLINS | ContractNo | Copied; trimmed | Daily, end of day | INT-01, INT-02 | To confirm with the system owner |
| DP01 | loan_account | product_code | LOV | varchar(10) | Yes | Core bank (ALS) | COLLINS | acct_prd_cd | Source code mapped to LOV-PRODUCT-CODE through the code map; an unmapped code is held in the exception list | Daily, end of day | INT-01, INT-02 | To confirm with the system owner |
| DP01 | loan_account | product_category_efs | TEXT | varchar(60) | No | EFS | COLLINS | Product_Category_EFS | Copied; trimmed | Daily, end of day | INT-07 | To confirm with the system owner |
| DP01 | loan_account | business_unit | LOV | varchar(10) | No | Core bank (ALS) | COLLINS | BU | Source code mapped to LOV-BU through the code map; an unmapped code is held in the exception list | Daily, end of day | INT-01, INT-02 | To confirm with the system owner |
| DP01 | loan_account | contract_date | DATE | date | No | Core bank (ALS) | COLLINS | CONTRACT_DATE | Converted to a date; Buddhist Era years converted to Gregorian | Daily, end of day | INT-01, INT-02 | To confirm with the system owner |
| DP01 | loan_account | interest_rate | NUMBER | numeric(7,4) | No | Core bank (ALS) | COLLINS | INTEREST_RATE | Converted to numeric(7,4); amounts in THB | Daily, end of day | INT-01, INT-02 | To confirm with the system owner |
| DP01 | loan_account | principal_outstanding | NUMBER | numeric(18,2) | Yes | Core bank (ALS) | COLLINS | Principal | Converted to numeric(18,2); amounts in THB | Daily, end of day | INT-01, INT-02 | To confirm with the system owner |
| DP01 | loan_account | interest_outstanding | NUMBER | numeric(18,2) | Yes | Core bank (ALS) | COLLINS | AINT1 + AINT2 | AINT1 plus AINT2 | Daily, end of day | INT-01, INT-02 | To confirm with the system owner |
| DP01 | loan_account | fees_outstanding | NUMBER | numeric(18,2) | Yes | Core bank (ALS) | COLLINS | AFEE | Converted to numeric(18,2); amounts in THB | Daily, end of day | INT-01, INT-02 | To confirm with the system owner |
| DP01 | loan_account | total_balance | NUMBER | numeric(18,2) | Yes | Core bank (ALS) | COLLINS | TOTAL_BALANCE | Converted to numeric(18,2); amounts in THB | Daily, end of day | INT-01, INT-02 | To confirm with the system owner |
| DP01 | loan_account | accounting_balance | NUMBER | numeric(18,2) | No | Core bank (ALS) | COLLINS | ACCOUNTING_BALANCE | Converted to numeric(18,2); amounts in THB | Daily, end of day | INT-01, INT-02 | To confirm with the system owner |
| DP01 | loan_account | days_past_due | NUMBER | integer | Yes | Core bank (ALS) | COLLINS | DELAY_DAYS | Converted to integer; amounts in THB | Daily, end of day | INT-01, INT-02 | To confirm with the system owner |
| DP01 | loan_account | bucket | LOV | varchar(10) | No | Core bank (ALS) | COLLINS | Bucket | Source code mapped to LOV-BUCKET through the code map; an unmapped code is held in the exception list | Daily, end of day | INT-01, INT-02 | To confirm with the system owner |
| DP01 | loan_account | classification | LOV | varchar(10) | No | Core bank (ALS) | COLLINS | To confirm with the system owner | Source code mapped to LOV-CLASS through the code map; an unmapped code is held in the exception list | Daily, end of day | INT-01, INT-02 | To confirm with the system owner |
| DP01 | loan_account | last_payment_date | DATE | date | No | Core bank (ALS) | COLLINS | LAST_PAYMENT_DATE | Converted to a date; Buddhist Era years converted to Gregorian | Daily, end of day | INT-01, INT-02 | To confirm with the system owner |
| DP01 | loan_account | next_installment_date | DATE | date | No | Core bank (ALS) | COLLINS | NEXT_INSTALLMENT_DATE | Converted to a date; Buddhist Era years converted to Gregorian | Daily, end of day | INT-01, INT-02 | To confirm with the system owner |
| DP01 | loan_account | tdr_flag | BOOLEAN | boolean | Yes | Core bank (ALS) | COLLINS | TDR list | Y or N converted to true or false | Daily, end of day | INT-01, INT-02 | To confirm with the system owner |
| DP01 | loan_account | last_tdr_date | DATE | date | No | Core bank (ALS) | COLLINS | Last_TDR_Date | Converted to a date; Buddhist Era years converted to Gregorian | Daily, end of day | INT-01, INT-02 | To confirm with the system owner |
| DP01 | loan_account | data_as_of | DATE | date | Yes | Core bank (ALS) | COLLINS | ms_data_dt | Business date of the load | Daily, end of day | INT-01, INT-02 | To confirm with the system owner |
| DP01 | loan_account | settlement_booked_date | DATE | date | No | Core bank (ALS) | COLLINS | To confirm with the system owner | None | Daily, end of day | INT-01 | To confirm |
| DP01 | loan_account | settlement_booked_amount | NUMBER | numeric(18,2) | No | Core bank (ALS) | COLLINS | To confirm with the system owner | None | Daily, end of day | INT-01 | To confirm |
| DP01 | account_payment | payment_code | TEXT | varchar(20) | Yes | Core bank (ALS) | COLLINS | Payment_Code | Copied; trimmed | Daily, end of day | INT-01, INT-02 | To confirm with the system owner |
| DP01 | account_payment | payment_date | DATE | date | Yes | Core bank (ALS) | COLLINS | Payment_Date | Converted to a date; Buddhist Era years converted to Gregorian | Daily, end of day | INT-01, INT-02 | To confirm with the system owner |
| DP01 | account_payment | payment_amount | NUMBER | numeric(18,2) | Yes | Core bank (ALS) | COLLINS | Payment_Amount | Converted to numeric(18,2); amounts in THB | Daily, end of day | INT-01, INT-02 | To confirm with the system owner |
| DP01 | account_payment | payment_channel | LOV | varchar(15) | No | Core bank (ALS) | COLLINS | To confirm with the system owner | Source code mapped to LOV-PAY-CHANNEL through the code map; an unmapped code is held in the exception list | Daily, end of day | INT-01, INT-02 | To confirm with the system owner |
| DP01 | account_payment | data_as_of | DATE | date | Yes | Core bank (ALS) | COLLINS | ms_data_dt | Converted to a date; Buddhist Era years converted to Gregorian | Daily, end of day | INT-01, INT-02 | To confirm with the system owner |
| DP06 | collateral | collateral_no | TEXT | varchar(20) | Yes | CCMS | File load | To confirm with the system owner | Copied; trimmed | Weekly | INT-10 | To confirm with the system owner |
| DP06 | collateral | collateral_type | LOV | varchar(15) | Yes | CCMS | File load | To confirm with the system owner | Source code mapped to LOV-COLL-TYPE through the code map; an unmapped code is held in the exception list | Weekly | INT-10 | To confirm with the system owner |
| DP06 | collateral | title_doc_no | TEXT | varchar(40) | No | CCMS | File load | Title Deed / Ownership Doc | Copied; trimmed | Weekly | INT-10 | To confirm with the system owner |
| DP06 | collateral | plot_no | TEXT | varchar(20) | No | CCMS | File load | Plot No. | Copied; trimmed | Weekly | INT-10 | To confirm with the system owner |
| DP06 | collateral | area_text | TEXT | varchar(20) | No | CCMS | File load | Area | Copied; trimmed | Weekly | INT-10 | To confirm with the system owner |
| DP06 | collateral | province | LOV | varchar(40) | No | CCMS | File load | Province | Source code mapped to LOV-PROVINCE through the code map; an unmapped code is held in the exception list | Weekly | INT-10 | To confirm with the system owner |
| DP06 | collateral | district | TEXT | varchar(60) | No | CCMS | File load | District | Copied; trimmed | Weekly | INT-10 | To confirm with the system owner |
| DP06 | collateral | subdistrict | TEXT | varchar(60) | No | CCMS | File load | Subdistrict | Copied; trimmed | Weekly | INT-10 | To confirm with the system owner |
| DP06 | collateral | insured_value | NUMBER | numeric(18,2) | No | CCMS | File load | Insvalue | Converted to numeric(18,2); amounts in THB | Weekly | INT-10 | To confirm with the system owner |
| DP06 | collateral | insurance_expiry | DATE | date | No | CCMS | File load | To confirm with the system owner | Converted to a date; Buddhist Era years converted to Gregorian | Weekly | INT-10 | To confirm with the system owner |
| DP06 | account_collateral | lien_rank | NUMBER | integer | No | CCMS | File load | To confirm with the system owner | Converted to integer; amounts in THB | Weekly | INT-10 | To confirm with the system owner |
| DP06 | valuation | appraisal_no | TEXT | varchar(20) | Yes | SVAF | File load | Appraisal No. | Copied; trimmed | Weekly | INT-11 | To confirm with the system owner |
| DP06 | valuation | appraisal_type | LOV | varchar(15) | Yes | SVAF | File load | To confirm with the system owner | Source code mapped to LOV-APPRAISAL through the code map; an unmapped code is held in the exception list | Weekly | INT-11 | To confirm with the system owner |
| DP06 | valuation | appraised_value | NUMBER | numeric(18,2) | Yes | SVAF | File load | Appraised Value | Converted to numeric(18,2); amounts in THB | Weekly | INT-11 | To confirm with the system owner |
| DP06 | valuation | forced_sale_value | NUMBER | numeric(18,2) | No | SVAF | File load | Forced Sale Value | Converted to numeric(18,2); amounts in THB | Weekly | INT-11 | To confirm with the system owner |
| DP06 | valuation | appraisal_date | DATE | date | Yes | SVAF | File load | Appraisal Date | Converted to a date; Buddhist Era years converted to Gregorian | Weekly | INT-11 | To confirm with the system owner |
| DP06 | asset | asset_ref | TEXT | varchar(20) | Yes | AMIS | File load | Asset ID | Copied; trimmed | Monthly | INT-12 | To confirm with the system owner |
| DP06 | asset | asset_code | TEXT | varchar(20) | No | AMIS | File load | Asset Code | Copied; trimmed | Monthly | INT-12 | To confirm with the system owner |
| DP06 | asset | asset_type | LOV | varchar(20) | Yes | AMIS | File load | Asset Type | Source code mapped to LOV-ASSET-TYPE through the code map; an unmapped code is held in the exception list | Monthly | INT-12 | To confirm with the system owner |
| DP06 | asset | transfer_in_type | LOV | varchar(20) | Yes | AMIS | File load | Transfer-in Type | Source code mapped to LOV-TRANSFER-IN through the code map; an unmapped code is held in the exception list | Monthly | INT-12 | To confirm with the system owner |
| DP06 | asset | from_segment | LOV | varchar(20) | No | AMIS | File load | From Segment | Source code mapped to LOV-SEGMENT through the code map; an unmapped code is held in the exception list | Monthly | INT-12 | To confirm with the system owner |
| DP06 | asset | transfer_in_date | DATE | date | Yes | AMIS | File load | Ownership Transfer in Date | Converted to a date; Buddhist Era years converted to Gregorian | Monthly | INT-12 | To confirm with the system owner |
| DP06 | asset | book_value | NUMBER | numeric(18,2) | Yes | AMIS | File load | Book  Value | Converted to numeric(18,2); amounts in THB | Monthly | INT-12 | To confirm with the system owner |
| DP06 | asset | auction_purchase_price | NUMBER | numeric(18,2) | No | AMIS | File load | Auction Purchase Price | Converted to numeric(18,2); amounts in THB | Monthly | INT-12 | To confirm with the system owner |
| DP06 | asset | repossessed_date | DATE | date | No | RPS | File load | ReposessedCarDate | Thai year date YYMMDD converted to a Gregorian date | Weekly | INT-13 | To confirm with the system owner |
| DP06 | asset | stock_date | DATE | date | No | RPS | File load | STOCK_DATE | Converted to a date; Buddhist Era years converted to Gregorian | Weekly | INT-13 | To confirm with the system owner |
| DP04 | treatment | installments | NUMBER | integer | No | ACE | ACE | To confirm with the system owner | Converted to integer; amounts in THB | Per request | INT-34 | To confirm with the system owner |
| DP04 | treatment | booked_at | DATE | timestamptz | No | Core bank (ALS) | COLLINS | To confirm with the system owner | Converted to a date; Buddhist Era years converted to Gregorian | Daily, end of day | INT-01, INT-02 | To confirm with the system owner |
| DP07 | legal_action | lawsuit_no | TEXT | varchar(30) | No | LIT | LIT | LAWSUIT_NO / LAWSUIT_RUN | Copied; trimmed | Daily, end of day | INT-09 | To confirm with the system owner |
| DP07 | legal_action | black_case_no | TEXT | varchar(30) | No | LIT | LIT | เลขที่คดีดำ | Copied; trimmed | Daily, end of day | INT-09 | To confirm with the system owner |
| DP07 | legal_action | red_case_no | TEXT | varchar(30) | No | LIT | LIT | To confirm with the system owner | Copied; trimmed | Daily, end of day | INT-09 | To confirm with the system owner |
| DP07 | legal_action | court_name | TEXT | varchar(120) | No | LIT | LIT | NCOURT | Copied; trimmed | Daily, end of day | INT-09 | To confirm with the system owner |
| DP07 | legal_action | claim_amount | NUMBER | numeric(18,2) | No | LIT | LIT | AAMT_SUIT | Converted to numeric(18,2); amounts in THB | Daily, end of day | INT-09 | To confirm with the system owner |
| DP07 | legal_action | filed_date | DATE | date | No | LIT | LIT | To confirm with the system owner | Converted to a date; Buddhist Era years converted to Gregorian | Daily, end of day | INT-09 | To confirm with the system owner |
| DP07 | legal_action | judgment_date | DATE | date | No | LIT | LIT | Judgment date | Converted to a date; Buddhist Era years converted to Gregorian | Daily, end of day | INT-09 | To confirm with the system owner |
| DP07 | legal_action | judgment_amount | NUMBER | numeric(18,2) | No | LIT | LIT | To confirm with the system owner | Converted to numeric(18,2); amounts in THB | Daily, end of day | INT-09 | To confirm with the system owner |
| DP07 | legal_action | lit_status | TEXT | varchar(200) | No | LIT | COLLINS | STATE_RES_NAME | Copied; trimmed | Daily, end of day | INT-09 | To confirm with the system owner |
| DP07 | notice | sent_date | DATE | date | No | WIN | File load | DDMMYYYY | Converted to a date; Buddhist Era years converted to Gregorian | Weekly | INT-15 | To confirm with the system owner |
| DP07 | notice | barcode | TEXT | varchar(40) | No | WIN | File load | Barcode | Copied; trimmed | Weekly | INT-15 | To confirm with the system owner |
| DP07 | notice | callback_date | DATE | date | No | WIN | File load | DDMMYYYY_callBack | Converted to a date; Buddhist Era years converted to Gregorian | Weekly | INT-15 | To confirm with the system owner |
| DP07 | notice | delivery_status | LOV | varchar(15) | No | WIN | File load | To confirm with the system owner | Source code mapped to LOV-DELIVERY through the code map; an unmapped code is held in the exception list | Weekly | INT-15 | To confirm with the system owner |
| DP07 | notice | sent_type | LOV | varchar(10) | No | WIN | File load | Sent Type | Source code mapped to LOV-SENT-TYPE through the code map; an unmapped code is held in the exception list | Weekly | INT-15 | To confirm with the system owner |
| DP07 | hearing | hearing_date | DATE | timestamptz | Yes | LIT | LIT | To confirm with the system owner | Converted to a date; Buddhist Era years converted to Gregorian | Daily, end of day | INT-09 | To confirm with the system owner |
| DP07 | hearing | hearing_type | LOV | varchar(20) | No | LIT | LIT | To confirm with the system owner | Source code mapped to LOV-HEARING through the code map; an unmapped code is held in the exception list | Daily, end of day | INT-09 | To confirm with the system owner |
| DP07 | hearing | next_date | DATE | timestamptz | No | LIT | LIT | To confirm with the system owner | Converted to a date; Buddhist Era years converted to Gregorian | Daily, end of day | INT-09 | To confirm with the system owner |
| DP06 | asset_sale | contract_date | DATE | date | Yes | AMIS | File load | Contract Date | Converted to a date; Buddhist Era years converted to Gregorian | Monthly | INT-12 | To confirm with the system owner |
| DP06 | asset_sale | sale_date | DATE | date | Yes | AMIS | File load | Sale Date | Converted to a date; Buddhist Era years converted to Gregorian | Monthly | INT-12 | To confirm with the system owner |
| DP06 | asset_sale | sale_price | NUMBER | numeric(18,2) | Yes | AMIS | File load | Sale Price | Converted to numeric(18,2); amounts in THB | Monthly | INT-12 | To confirm with the system owner |
| DP06 | asset_sale | transfer_fee | NUMBER | numeric(18,2) | No | AMIS | File load | Sale Transfer Fee | Converted to numeric(18,2); amounts in THB | Monthly | INT-12 | To confirm with the system owner |
| DP06 | asset_sale | specific_business_tax | NUMBER | numeric(18,2) | No | AMIS | File load | Specific Business Tax | Converted to numeric(18,2); amounts in THB | Monthly | INT-12 | To confirm with the system owner |
| DP06 | asset_sale | corporate_income_tax | NUMBER | numeric(18,2) | No | AMIS | File load | Corporate Income Tax | Converted to numeric(18,2); amounts in THB | Monthly | INT-12 | To confirm with the system owner |
| DP06 | asset_sale | incentive_amount | NUMBER | numeric(18,2) | No | AMIS | File load | Incentive Amount | Converted to numeric(18,2); amounts in THB | Monthly | INT-12 | To confirm with the system owner |
| DP09 | debt_sale_account | outstanding | NUMBER | numeric(18,2) | Yes | Core bank (ALS) | COLLINS | OS By Acct | Converted to numeric(18,2); amounts in THB | Daily, end of day | INT-01, INT-02 | To confirm with the system owner |
| DP05 | interaction | action_code | LOV | varchar(10) | No | EFS | COLLINS | Actioncode ID | Source code mapped to LOV-ACTION-CODE through the code map; an unmapped code is held in the exception list | Daily, end of day | INT-07 | To confirm with the system owner |
| DP05 | interaction | contact_result | LOV | varchar(20) | No | EFS | COLLINS | Call Result | Source code mapped to LOV-CONTACT-RESULT through the code map; an unmapped code is held in the exception list | Daily, end of day | INT-07 | To confirm with the system owner |
| DP12 | decision_log_entry | model_version | TEXT | varchar(40) | No | COLLINS | COLLINS | To confirm with the system owner | Copied; trimmed | Daily; monthly for some models | INT-08 | To confirm with the system owner |
| DP11 | score | model_code | TEXT | varchar(30) | Yes | COLLINS | COLLINS | To confirm with the system owner | Copied; trimmed | Daily; monthly for some models | INT-08 | To confirm with the system owner |
| DP11 | score | model_version | TEXT | varchar(20) | Yes | COLLINS | COLLINS | To confirm with the system owner | Copied; trimmed | Daily; monthly for some models | INT-08 | To confirm with the system owner |
| DP11 | score | score_value | NUMBER | numeric(12,4) | No | COLLINS | COLLINS | To confirm with the system owner | Converted to numeric(12,4); amounts in THB | Daily; monthly for some models | INT-08 | To confirm with the system owner |
| DP11 | score | estimate_value | NUMBER | numeric(18,2) | No | COLLINS | COLLINS | To confirm with the system owner | Converted to numeric(18,2); amounts in THB | Daily; monthly for some models | INT-08 | To confirm with the system owner |
| DP11 | score | route_code | LOV | varchar(4) | No | COLLINS | COLLINS | To confirm with the system owner | Source code mapped to LOV-ROUTE through the code map; an unmapped code is held in the exception list | Daily; monthly for some models | INT-08 | To confirm with the system owner |
| DP11 | score | scored_at | DATE | date | Yes | COLLINS | COLLINS | To confirm with the system owner | Converted to a date; Buddhist Era years converted to Gregorian | Daily; monthly for some models | INT-08 | To confirm with the system owner |
| DP13 | proceeds | amount | NUMBER | numeric(18,2) | Yes | Core bank (ALS) | COLLINS | Payment_Amount | Converted to numeric(18,2); amounts in THB | Daily, end of day | INT-01, INT-02 | To confirm with the system owner |
| DP13 | proceeds | received_date | DATE | date | Yes | Core bank (ALS) | COLLINS | Payment_Date | Converted to a date; Buddhist Era years converted to Gregorian | Daily, end of day | INT-01, INT-02 | To confirm with the system owner |
| DP13 | proceeds | posting_ref | TEXT | varchar(40) | No | Core bank (ALS) | COLLINS | To confirm with the system owner | Copied; trimmed | Daily, end of day | INT-01, INT-02 | To confirm with the system owner |
| DP13 | write_off | amount | NUMBER | numeric(18,2) | Yes | GL | File load | AMT | Converted to numeric(18,2); amounts in THB | Monthly | INT-16 | To confirm with the system owner |
| DP13 | write_off | posted_date | DATE | date | No | GL | File load | DATE | Converted to a date; Buddhist Era years converted to Gregorian | Monthly | INT-16 | To confirm with the system owner |
| DP13 | write_off | responsibility_center | TEXT | varchar(10) | No | GL | File load | RC | Copied; trimmed | Monthly | INT-16 | To confirm with the system owner |
| DP13 | write_off | cost_center | TEXT | varchar(10) | No | GL | File load | OC | Copied; trimmed | Monthly | INT-16 | To confirm with the system owner |
| DP13 | write_off | gl_product | TEXT | varchar(10) | No | GL | File load | PRODUCT | Copied; trimmed | Monthly | INT-16 | To confirm with the system owner |
| DP14 | role | entra_group | TEXT | varchar(120) | No | Entra ID | Entra ID | To confirm with the system owner | Copied; trimmed | At each sign-in | INT-21 | To confirm with the system owner |

## Workbench fields

| Fields created in the Workbench |  |  |  |  |  |  |
|---|---|---|---|---|---|---|
| 303 fields entered by users or derived by the Workbench. They have no source system; the Workbench is their system of record. |  |  |  |  |  |  |
| Data product | Entity | Field | Data type | Physical type | Origin | Meaning |
| DP03 | recovery_case | id | TEXT | uuid | Entered or derived in the Workbench | Record identifier of the case |
| DP03 | recovery_case | case_no | TEXT | varchar(18) | Entered or derived in the Workbench | Case number RW-YYYY-NNNNNN, issued at creation and never reused |
| DP03 | recovery_case | primary_customer_id | CROSS_REF | uuid | Entered or derived in the Workbench | The borrower the case is opened for |
| DP03 | recovery_case | status | LOV | varchar(20) | Entered or derived in the Workbench | Case status: new, assigned, in progress, waiting customer, waiting partner, waiting approval, on hold, closed |
| DP03 | recovery_case | stage_code | LOV | varchar(20) | Entered or derived in the Workbench | The stage the case is on |
| DP03 | recovery_case | route_state | TEXT | varchar(60) | Entered or derived in the Workbench | The routing state from the rule set, for example FIRM_INSTRUCTED |
| DP03 | recovery_case | route_code | LOV | varchar(4) | Entered or derived in the Workbench | The approved route R1 to R8 |
| DP03 | recovery_case | owner_user_id | USER_REF | uuid | Entered or derived in the Workbench | The case owner |
| DP03 | recovery_case | queue_id | CROSS_REF | uuid | Entered or derived in the Workbench | The queue the case is in |
| DP03 | recovery_case | team_code | LOV | varchar(20) | Entered or derived in the Workbench | The owning team, used by scope rules |
| DP03 | recovery_case | region_code | LOV | varchar(10) | Entered or derived in the Workbench | The owning region, used by scope rules |
| DP03 | recovery_case | entry_date | DATE | date | Entered or derived in the Workbench | The date the case entered recovery |
| DP03 | recovery_case | exposure_band | LOV | varchar(10) | Entered or derived in the Workbench | Exposure band set from the outstanding balance at entry |
| DP03 | recovery_case | prescription_date | DATE | date | Entered or derived in the Workbench | The earliest date a legal claim on the case expires |
| DP03 | recovery_case | stage_clock_start | DATE | timestamptz | Entered or derived in the Workbench | When the current state started, for the service level |
| DP03 | recovery_case | deviation_open | BOOLEAN | boolean | Entered or derived in the Workbench | True while any deviation X1 to X7 is open |
| DP03 | recovery_case | legal_hold | BOOLEAN | boolean | Entered or derived in the Workbench | True while a legal hold stops normal routing |
| DP03 | recovery_case | rule_version | TEXT | varchar(20) | Entered or derived in the Workbench | The rule version the current state was entered under |
| DP03 | recovery_case | closed_date | DATE | date | Entered or derived in the Workbench | The date the case closed |
| DP03 | recovery_case | closure_reason | LOV | varchar(20) | Entered or derived in the Workbench | Cured, settled, realized, sold, written off, insurance settled, merged, canceled |
| DP03 | case_account | id | TEXT | uuid | Entered or derived in the Workbench | Record identifier of the case account link |
| DP03 | case_account | case_id | CROSS_REF | uuid | Entered or derived in the Workbench | The recovery_case this record belongs to |
| DP03 | case_account | account_id | CROSS_REF | uuid | Entered or derived in the Workbench | The loan_account this record belongs to |
| DP03 | case_account | is_primary | BOOLEAN | boolean | Entered or derived in the Workbench | True for the account the case was opened on |
| DP03 | case_account | linked_from | DATE | date | Entered or derived in the Workbench | Date the account joined the case |
| DP03 | case_account | linked_to | DATE | date | Entered or derived in the Workbench | Date the account left the case |
| DP03 | case_party | id | TEXT | uuid | Entered or derived in the Workbench | Record identifier of the case party link |
| DP03 | case_party | case_id | CROSS_REF | uuid | Entered or derived in the Workbench | The recovery_case this record belongs to |
| DP03 | case_party | party_id | CROSS_REF | uuid | Entered or derived in the Workbench | The party this record belongs to |
| DP03 | case_party | party_role | LOV | varchar(20) | Entered or derived in the Workbench | Borrower, co-borrower, guarantor, authorized signatory, heir |
| DP03 | case_party | role_from | DATE | date | Entered or derived in the Workbench | Date the role starts |
| DP03 | case_party | role_to | DATE | date | Entered or derived in the Workbench | Date the role ends |
| DP03 | deviation | id | TEXT | uuid | Entered or derived in the Workbench | Record identifier of the deviation |
| DP03 | deviation | case_id | CROSS_REF | uuid | Entered or derived in the Workbench | The recovery_case this record belongs to |
| DP03 | deviation | deviation_code | LOV | varchar(3) | Entered or derived in the Workbench | X1 to X7 |
| DP03 | deviation | raised_at | DATE | timestamptz | Entered or derived in the Workbench | When it was raised |
| DP03 | deviation | raised_by | LOV | varchar(20) | Entered or derived in the Workbench | Screening agent, rule, officer, customer contact |
| DP03 | deviation | paused_state | TEXT | varchar(60) | Entered or derived in the Workbench | The routing state the case was in when paused |
| DP03 | deviation | handler_user_id | USER_REF | uuid | Entered or derived in the Workbench | The named handler |
| DP03 | deviation | contact_stop | BOOLEAN | boolean | Entered or derived in the Workbench | True when customer contact is stopped |
| DP03 | deviation | cleared_at | DATE | timestamptz | Entered or derived in the Workbench | When it cleared |
| DP03 | deviation | outcome | LOV | varchar(20) | Entered or derived in the Workbench | Returned, re-routed, case ended |
| DP03 | queue | id | TEXT | uuid | Entered or derived in the Workbench | Record identifier of the queue |
| DP03 | queue | queue_code | TEXT | varchar(30) | Entered or derived in the Workbench | Queue code |
| DP03 | queue | queue_name | TEXT | varchar(100) | Entered or derived in the Workbench | Queue name |
| DP03 | queue | team_code | LOV | varchar(20) | Entered or derived in the Workbench | Team the queue belongs to |
| DP03 | queue | role_code | LOV | varchar(20) | Entered or derived in the Workbench | Role that works the queue |
| DP03 | queue | assignment_method | LOV | varchar(20) | Entered or derived in the Workbench | Round robin, lowest load, named owner, skill |
| DP03 | queue | capacity_cap | NUMBER | integer | Entered or derived in the Workbench | Most open cases one person may hold in the queue |
| DP03 | queue | overflow_queue_id | CROSS_REF | uuid | Entered or derived in the Workbench | Queue that receives overflow |
| DP03 | assignment | id | TEXT | uuid | Entered or derived in the Workbench | Record identifier of the assignment |
| DP03 | assignment | case_id | CROSS_REF | uuid | Entered or derived in the Workbench | The recovery_case this record belongs to |
| DP03 | assignment | task_id | CROSS_REF | uuid | Entered or derived in the Workbench | The task this record belongs to |
| DP03 | assignment | assignee_user_id | USER_REF | uuid | Entered or derived in the Workbench | The person or service identity assigned |
| DP03 | assignment | assigned_at | DATE | timestamptz | Entered or derived in the Workbench | When assigned |
| DP03 | assignment | ended_at | DATE | timestamptz | Entered or derived in the Workbench | When the assignment ended |
| DP03 | assignment | reason | LOV | varchar(20) | Entered or derived in the Workbench | Allocation, transfer, rebalance, manual, escalation |
| DP03 | assignment | rule_id | TEXT | varchar(20) | Entered or derived in the Workbench | The rule that made the assignment |
| DP03 | task | id | TEXT | uuid | Entered or derived in the Workbench | Record identifier of the task |
| DP03 | task | case_id | CROSS_REF | uuid | Entered or derived in the Workbench | The recovery_case this record belongs to |
| DP03 | task | task_code | TEXT | varchar(60) | Entered or derived in the Workbench | The task in the case model, for example VERIFY_PACK |
| DP03 | task | element_type | LOV | varchar(20) | Entered or derived in the Workbench | Human, customer, partner or decision task, milestone, event listener |
| DP03 | task | discretion | LOV | varchar(15) | Entered or derived in the Workbench | Automatic, discretionary, required |
| DP03 | task | status | LOV | varchar(15) | Entered or derived in the Workbench | Open, in progress, done, canceled |
| DP03 | task | owner_role | LOV | varchar(20) | Entered or derived in the Workbench | Role that owns the task |
| DP03 | task | due_at | DATE | timestamptz | Entered or derived in the Workbench | When the task is due |
| DP03 | task | completed_at | DATE | timestamptz | Entered or derived in the Workbench | When it completed |
| DP03 | task | outcome_code | TEXT | varchar(40) | Entered or derived in the Workbench | The event the task produced |
| DP03 | timer | id | TEXT | uuid | Entered or derived in the Workbench | Record identifier of the timer |
| DP03 | timer | case_id | CROSS_REF | uuid | Entered or derived in the Workbench | The recovery_case this record belongs to |
| DP03 | timer | task_id | CROSS_REF | uuid | Entered or derived in the Workbench | The task this record belongs to |
| DP03 | timer | timer_type | LOV | varchar(20) | Entered or derived in the Workbench | Service level, notice period, cure period, prescription, hearing deadline, offer validity, holding age, claim deadline |
| DP03 | timer | started_at | DATE | timestamptz | Entered or derived in the Workbench | When it started |
| DP03 | timer | expires_at | DATE | timestamptz | Entered or derived in the Workbench | When it expires |
| DP03 | timer | warn_at | DATE | timestamptz | Entered or derived in the Workbench | When the warning is raised |
| DP03 | timer | paused | BOOLEAN | boolean | Entered or derived in the Workbench | True while paused by a deviation. A prescription timer never pauses |
| DP03 | timer | status | LOV | varchar(15) | Entered or derived in the Workbench | Running, paused, expired, stopped |
| DP03 | timer | escalation_level | NUMBER | integer | Entered or derived in the Workbench | How many times it has escalated |
| DP02 | party | id | TEXT | uuid | Entered or derived in the Workbench | Record identifier of the party |
| DP02 | party | vulnerable_flag | BOOLEAN | boolean | Entered or derived in the Workbench | Vulnerable customer or hardship confirmed |
| DP02 | party | deceased_flag | BOOLEAN | boolean | Entered or derived in the Workbench | Death confirmed |
| DP02 | party | bankruptcy_flag | BOOLEAN | boolean | Entered or derived in the Workbench | Bankruptcy or receivership confirmed |
| DP02 | contact_point | id | TEXT | uuid | Entered or derived in the Workbench | Record identifier of the contact point |
| DP02 | contact_point | party_id | CROSS_REF | uuid | Entered or derived in the Workbench | The party this record belongs to |
| DP02 | contact_point | channel | LOV | varchar(15) | Entered or derived in the Workbench | Mobile, home phone, work phone, LINE, email, postal address |
| DP02 | contact_point | source | LOV | varchar(15) | Entered or derived in the Workbench | Bank record, field visit, agency, bureau trace, customer |
| DP02 | contact_point | consent_status | LOV | varchar(12) | Entered or derived in the Workbench | Given, withdrawn, unknown |
| DP02 | contact_point | verified_at | DATE | timestamptz | Entered or derived in the Workbench | When it last reached the right party |
| DP02 | contact_point | failed_count | NUMBER | integer | Entered or derived in the Workbench | Failed attempts since last success |
| DP01 | loan_account | id | TEXT | uuid | Entered or derived in the Workbench | Record identifier of the account |
| DP01 | loan_account | dispute_open | BOOLEAN | boolean | Entered or derived in the Workbench | True while the customer disputes the balance or the security on the account |
| DP01 | account_payment | id | TEXT | uuid | Entered or derived in the Workbench | Record identifier of the account payment |
| DP01 | account_payment | account_id | CROSS_REF | uuid | Entered or derived in the Workbench | The loan_account this record belongs to |
| DP06 | collateral | id | TEXT | uuid | Entered or derived in the Workbench | Record identifier of the collateral |
| DP06 | collateral | occupancy | LOV | varchar(15) | Entered or derived in the Workbench | Occupied by owner, tenant, vacant, unknown |
| DP06 | collateral | encumbrance_status | LOV | varchar(15) | Entered or derived in the Workbench | Clear, other creditor, seized, under dispute |
| DP06 | account_collateral | id | TEXT | uuid | Entered or derived in the Workbench | Record identifier of the account collateral link |
| DP06 | account_collateral | account_id | CROSS_REF | uuid | Entered or derived in the Workbench | The loan_account this record belongs to |
| DP06 | account_collateral | collateral_id | CROSS_REF | uuid | Entered or derived in the Workbench | The collateral this record belongs to |
| DP06 | valuation | id | TEXT | uuid | Entered or derived in the Workbench | Record identifier of the valuation |
| DP06 | valuation | collateral_id | CROSS_REF | uuid | Entered or derived in the Workbench | The collateral this record belongs to |
| DP06 | valuation | asset_id | CROSS_REF | uuid | Entered or derived in the Workbench | The asset this record belongs to |
| DP06 | valuation | valuer_partner_id | CROSS_REF | uuid | Entered or derived in the Workbench | The valuer |
| DP06 | valuation | accepted | BOOLEAN | boolean | Entered or derived in the Workbench | True once accepted for the route decision |
| DP06 | asset | id | TEXT | uuid | Entered or derived in the Workbench | Record identifier of the asset |
| DP06 | asset | case_id | CROSS_REF | uuid | Entered or derived in the Workbench | The recovery_case this record belongs to |
| DP06 | asset | collateral_id | CROSS_REF | uuid | Entered or derived in the Workbench | The collateral this record belongs to |
| DP06 | asset | holding_status | LOV | varchar(15) | Entered or derived in the Workbench | Held, listed, under offer, sold, transferred, rented |
| DP06 | asset | holding_cost_to_date | NUMBER | numeric(18,2) | Entered or derived in the Workbench | Holding cost to date, baht |
| DP04 | treatment | id | TEXT | uuid | Entered or derived in the Workbench | Record identifier of the treatment |
| DP04 | treatment | case_id | CROSS_REF | uuid | Entered or derived in the Workbench | The recovery_case this record belongs to |
| DP04 | treatment | decision_log_id | CROSS_REF | uuid | Entered or derived in the Workbench | The decision that approved it |
| DP04 | treatment | treatment_type | LOV | varchar(20) | Entered or derived in the Workbench | Restructure, settlement, deed in lieu, buy-back, guarantee claim, repossession, auction, debt sale, write-off, RAMC transfer, rental |
| DP04 | treatment | proposed_by | LOV | varchar(10) | Entered or derived in the Workbench | Agent, rule, person |
| DP04 | treatment | proposed_at | DATE | timestamptz | Entered or derived in the Workbench | When proposed |
| DP04 | treatment | offer_amount | NUMBER | numeric(18,2) | Entered or derived in the Workbench | Amount offered or agreed, baht |
| DP04 | treatment | haircut_amount | NUMBER | numeric(18,2) | Entered or derived in the Workbench | Amount forgiven, baht |
| DP04 | treatment | valid_until | DATE | date | Entered or derived in the Workbench | Offer validity |
| DP04 | treatment | approval_level | LOV | varchar(4) | Entered or derived in the Workbench | Approval level that approved it |
| DP04 | treatment | outcome | LOV | varchar(12) | Entered or derived in the Workbench | Kept, broken, completed, canceled, declined |
| DP04 | treatment | outcome_at | DATE | timestamptz | Entered or derived in the Workbench | When the outcome was recorded |
| DP04 | guarantee_claim | id | TEXT | uuid | Entered or derived in the Workbench | Record identifier of the guarantee claim |
| DP04 | guarantee_claim | case_id | CROSS_REF | uuid | Entered or derived in the Workbench | The recovery_case this record belongs to |
| DP04 | guarantee_claim | claim_type | LOV | varchar(25) | Entered or derived in the Workbench | TCG, credit life insurance, mortgage insurance, collateral insurance |
| DP04 | guarantee_claim | claim_deadline | DATE | date | Entered or derived in the Workbench | Last date the claim can be filed |
| DP04 | guarantee_claim | claimed_amount | NUMBER | numeric(18,2) | Entered or derived in the Workbench | Amount claimed, baht |
| DP04 | guarantee_claim | filed_at | DATE | date | Entered or derived in the Workbench | Date filed |
| DP04 | guarantee_claim | paid_amount | NUMBER | numeric(18,2) | Entered or derived in the Workbench | Amount paid, baht |
| DP04 | guarantee_claim | status | LOV | varchar(12) | Entered or derived in the Workbench | Preparing, filed, defect, paid, rejected |
| DP07 | legal_action | id | TEXT | uuid | Entered or derived in the Workbench | Record identifier of the legal action |
| DP07 | legal_action | case_id | CROSS_REF | uuid | Entered or derived in the Workbench | The recovery_case this record belongs to |
| DP07 | legal_action | law_firm_id | CROSS_REF | uuid | Entered or derived in the Workbench | The law firm instructed |
| DP07 | legal_action | action_type | LOV | varchar(20) | Entered or derived in the Workbench | Notice, civil case, appeal, enforcement, bankruptcy petition, LED auction |
| DP07 | legal_action | status | LOV | varchar(15) | Entered or derived in the Workbench | Open, filed, judgment, enforcing, closed, withdrawn |
| DP07 | notice | id | TEXT | uuid | Entered or derived in the Workbench | Record identifier of the notice |
| DP07 | notice | case_id | CROSS_REF | uuid | Entered or derived in the Workbench | The recovery_case this record belongs to |
| DP07 | notice | document_id | CROSS_REF | uuid | Entered or derived in the Workbench | The generated notice |
| DP07 | notice | notice_type | LOV | varchar(25) | Entered or derived in the Workbench | Demand, recall, statutory sale notice, guarantor notice |
| DP07 | hearing | id | TEXT | uuid | Entered or derived in the Workbench | Record identifier of the hearing |
| DP07 | hearing | legal_action_id | CROSS_REF | uuid | Entered or derived in the Workbench | The legal_action this record belongs to |
| DP07 | hearing | outcome | LOV | varchar(20) | Entered or derived in the Workbench | Held, adjourned, settled, judgment |
| DP08 | partner | id | TEXT | uuid | Entered or derived in the Workbench | Record identifier of the partner |
| DP08 | partner | partner_code | TEXT | varchar(20) | Entered or derived in the Workbench | Partner code |
| DP08 | partner | partner_name | TEXT | varchar(160) | Entered or derived in the Workbench | Registered name |
| DP08 | partner | partner_type | LOV | varchar(15) | Entered or derived in the Workbench | Agency, law firm, valuer, auction vendor, broker, debt buyer, AMC, RAMC |
| DP08 | partner | panel_status | LOV | varchar(12) | Entered or derived in the Workbench | Active, on notice, suspended, exited |
| DP08 | partner | contract_end | DATE | date | Entered or derived in the Workbench | Contract end date |
| DP08 | partner | score | NUMBER | numeric(5,2) | Entered or derived in the Workbench | Latest scorecard result |
| DP08 | partner_instruction | id | TEXT | uuid | Entered or derived in the Workbench | Record identifier of the partner instruction |
| DP08 | partner_instruction | case_id | CROSS_REF | uuid | Entered or derived in the Workbench | The recovery_case this record belongs to |
| DP08 | partner_instruction | partner_id | CROSS_REF | uuid | Entered or derived in the Workbench | The partner this record belongs to |
| DP08 | partner_instruction | instruction_type | LOV | varchar(20) | Entered or derived in the Workbench | Collect, file suit, enforce, appraise, repossess, list, sell |
| DP08 | partner_instruction | instructed_at | DATE | timestamptz | Entered or derived in the Workbench | When instructed |
| DP08 | partner_instruction | due_at | DATE | timestamptz | Entered or derived in the Workbench | When the result is due |
| DP08 | partner_instruction | status | LOV | varchar(12) | Entered or derived in the Workbench | Sent, accepted, declined, in progress, done, recalled |
| DP08 | partner_instruction | result_code | TEXT | varchar(40) | Entered or derived in the Workbench | Result reported by the partner |
| DP08 | partner_instruction | fee_amount | NUMBER | numeric(18,2) | Entered or derived in the Workbench | Fee payable, baht |
| DP06 | listing | id | TEXT | uuid | Entered or derived in the Workbench | Record identifier of the listing |
| DP06 | listing | asset_id | CROSS_REF | uuid | Entered or derived in the Workbench | The asset this record belongs to |
| DP06 | listing | sale_channel | LOV | varchar(15) | Entered or derived in the Workbench | Dutch auction, broker, direct, LED auction, RAMC |
| DP06 | listing | start_price | NUMBER | numeric(18,2) | Entered or derived in the Workbench | Start price, baht |
| DP06 | listing | floor_price | NUMBER | numeric(18,2) | Entered or derived in the Workbench | Floor price approved, baht |
| DP06 | listing | round_no | NUMBER | integer | Entered or derived in the Workbench | Current price round |
| DP06 | listing | listed_at | DATE | timestamptz | Entered or derived in the Workbench | When listed |
| DP06 | listing | status | LOV | varchar(12) | Entered or derived in the Workbench | Draft, live, under offer, sold, withdrawn |
| DP06 | asset_sale | id | TEXT | uuid | Entered or derived in the Workbench | Record identifier of the asset sale |
| DP06 | asset_sale | asset_id | CROSS_REF | uuid | Entered or derived in the Workbench | The asset this record belongs to |
| DP06 | asset_sale | listing_id | CROSS_REF | uuid | Entered or derived in the Workbench | The listing this record belongs to |
| DP06 | asset_sale | gain_loss | FORMULA | numeric(18,2) | Entered or derived in the Workbench | Sale price less book value and costs |
| DP09 | debt_sale_lot | id | TEXT | uuid | Entered or derived in the Workbench | Record identifier of the debt sale lot |
| DP09 | debt_sale_lot | lot_no | TEXT | varchar(15) | Entered or derived in the Workbench | Lot number, for example 1/2024 |
| DP09 | debt_sale_lot | cut_off_date | DATE | date | Entered or derived in the Workbench | Balance cut-off date |
| DP09 | debt_sale_lot | segment | LOV | varchar(20) | Entered or derived in the Workbench | Segment of the lot |
| DP09 | debt_sale_lot | reserve_price | NUMBER | numeric(18,2) | Entered or derived in the Workbench | Reserve price, baht |
| DP09 | debt_sale_lot | buyer_partner_id | CROSS_REF | uuid | Entered or derived in the Workbench | Winning buyer |
| DP09 | debt_sale_lot | buyer_class | LOV | varchar(10) | Entered or derived in the Workbench | AMC or non-AMC |
| DP09 | debt_sale_lot | signing_date | DATE | date | Entered or derived in the Workbench | Date the sale was signed |
| DP09 | debt_sale_lot | approval_authority | TEXT | varchar(60) | Entered or derived in the Workbench | Authority that approved the sale |
| DP09 | debt_sale_lot | payment_terms | TEXT | varchar(400) | Entered or derived in the Workbench | Deposit and payment terms |
| DP09 | debt_sale_lot | status | LOV | varchar(12) | Entered or derived in the Workbench | Building, offered, awarded, transferred, closed |
| DP09 | debt_sale_account | id | TEXT | uuid | Entered or derived in the Workbench | Record identifier of the debt sale account |
| DP09 | debt_sale_account | lot_id | CROSS_REF | uuid | Entered or derived in the Workbench | The debt_sale_lot this record belongs to |
| DP09 | debt_sale_account | account_id | CROSS_REF | uuid | Entered or derived in the Workbench | The loan_account this record belongs to |
| DP09 | debt_sale_account | borrower_code | TEXT | varchar(20) | Entered or derived in the Workbench | Borrower code |
| DP09 | debt_sale_account | selling_price | NUMBER | numeric(18,2) | Entered or derived in the Workbench | Price allocated to the account, baht |
| DP09 | debt_sale_account | put_back_status | LOV | varchar(12) | Entered or derived in the Workbench | None, claimed, accepted, rejected |
| DP05 | interaction | id | TEXT | uuid | Entered or derived in the Workbench | Record identifier of the interaction |
| DP05 | interaction | case_id | CROSS_REF | uuid | Entered or derived in the Workbench | The recovery_case this record belongs to |
| DP05 | interaction | party_id | CROSS_REF | uuid | Entered or derived in the Workbench | The party this record belongs to |
| DP05 | interaction | occurred_at | DATE | timestamptz | Entered or derived in the Workbench | When it happened |
| DP05 | interaction | channel | LOV | varchar(15) | Entered or derived in the Workbench | Call, visit, SMS, LINE, email, letter, portal, branch |
| DP05 | interaction | direction | LOV | varchar(8) | Entered or derived in the Workbench | Inbound or outbound |
| DP05 | interaction | promise_amount | NUMBER | numeric(18,2) | Entered or derived in the Workbench | Amount promised, baht |
| DP05 | interaction | promise_date | DATE | date | Entered or derived in the Workbench | Date promised |
| DP05 | interaction | summary | TEXT | varchar(2000) | Entered or derived in the Workbench | Summary of what was said |
| DP05 | interaction | conduct_check | LOV | varchar(15) | Entered or derived in the Workbench | Passed, blocked, not applicable |
| DP05 | interaction | source_system | LOV | varchar(10) | Entered or derived in the Workbench | EFS for collections history, or the Workbench |
| DP10 | document | id | TEXT | uuid | Entered or derived in the Workbench | Record identifier of the document |
| DP10 | document | case_id | CROSS_REF | uuid | Entered or derived in the Workbench | The recovery_case this record belongs to |
| DP10 | document | party_id | CROSS_REF | uuid | Entered or derived in the Workbench | The party this record belongs to |
| DP10 | document | document_type | LOV | varchar(30) | Entered or derived in the Workbench | Type from the document checklist |
| DP10 | document | source | LOV | varchar(12) | Entered or derived in the Workbench | Scan, upload, generated, partner, email |
| DP10 | document | storage_ref | ATTACHMENT | varchar(400) | Entered or derived in the Workbench | Reference to the stored file |
| DP10 | document | classification_confidence | NUMBER | numeric(5,4) | Entered or derived in the Workbench | OCR classification confidence |
| DP10 | document | review_status | LOV | varchar(12) | Entered or derived in the Workbench | Not needed, pending, confirmed, corrected |
| DP10 | document | retention_class | LOV | varchar(10) | Entered or derived in the Workbench | Retention class |
| DP10 | document | write_once | BOOLEAN | boolean | Entered or derived in the Workbench | True for legal documents held write-once |
| DP10 | document | doc_version | NUMBER | integer | Entered or derived in the Workbench | Document version |
| DP10 | document_field | id | TEXT | uuid | Entered or derived in the Workbench | Record identifier of the document field |
| DP10 | document_field | document_id | CROSS_REF | uuid | Entered or derived in the Workbench | The document this record belongs to |
| DP10 | document_field | field_name | TEXT | varchar(60) | Entered or derived in the Workbench | Field name from the document type |
| DP10 | document_field | field_value | TEXT | varchar(1000) | Entered or derived in the Workbench | Value read, masked where personal |
| DP10 | document_field | confidence | NUMBER | numeric(5,4) | Entered or derived in the Workbench | Extraction confidence |
| DP10 | document_field | confirmed_by | USER_REF | uuid | Entered or derived in the Workbench | Who confirmed a low confidence value |
| DP10 | document_custody | id | TEXT | uuid | Entered or derived in the Workbench | Record identifier of the custody movement |
| DP10 | document_custody | document_id | CROSS_REF | uuid | Entered or derived in the Workbench | The document this record belongs to |
| DP10 | document_custody | moved_at | DATE | timestamptz | Entered or derived in the Workbench | When it moved |
| DP10 | document_custody | from_location | LOV | varchar(20) | Entered or derived in the Workbench | Vault, branch, post, lawyer, court, land office |
| DP10 | document_custody | to_location | LOV | varchar(20) | Entered or derived in the Workbench | Where it went |
| DP10 | document_custody | held_by | TEXT | varchar(120) | Entered or derived in the Workbench | Person or firm holding it |
| DP10 | document_custody | due_back | DATE | date | Entered or derived in the Workbench | When it is due back |
| DP12 | decision_log_entry | id | TEXT | uuid | Entered or derived in the Workbench | Record identifier of the decision log entry |
| DP12 | decision_log_entry | case_id | CROSS_REF | uuid | Entered or derived in the Workbench | The recovery_case this record belongs to |
| DP12 | decision_log_entry | decision_code | LOV | varchar(8) | Entered or derived in the Workbench | D5.1 to D9.3, X1 to X7, or an access event |
| DP12 | decision_log_entry | rule_id | TEXT | varchar(20) | Entered or derived in the Workbench | Rule that fired |
| DP12 | decision_log_entry | rule_version | TEXT | varchar(20) | Entered or derived in the Workbench | Rule version |
| DP12 | decision_log_entry | agent_version | TEXT | varchar(40) | Entered or derived in the Workbench | Agent and prompt version used |
| DP12 | decision_log_entry | inputs_ref | TEXT | varchar(400) | Entered or derived in the Workbench | Reference to the inputs snapshot, with the freshness of each input |
| DP12 | decision_log_entry | recommendation | TEXT | jsonb | Entered or derived in the Workbench | Option, reasons, confidence and alternatives |
| DP12 | decision_log_entry | approver_user_id | USER_REF | uuid | Entered or derived in the Workbench | Who approved |
| DP12 | decision_log_entry | approval_level | LOV | varchar(4) | Entered or derived in the Workbench | Approval level applied |
| DP12 | decision_log_entry | final_call | TEXT | varchar(40) | Entered or derived in the Workbench | The option decided |
| DP12 | decision_log_entry | override_reason | TEXT | varchar(1000) | Entered or derived in the Workbench | Reason when the person did not follow the recommendation |
| DP12 | decision_log_entry | actions | TEXT | jsonb | Entered or derived in the Workbench | Target system, result and timestamps of each action |
| DP12 | decision_log_entry | outcome | TEXT | jsonb | Entered or derived in the Workbench | Cash, cure, loss and time, written when known |
| DP12 | decision_log_entry | decided_at | DATE | timestamptz | Entered or derived in the Workbench | When decided |
| DP12 | decision_log_entry | prev_hash | TEXT | char(64) | Entered or derived in the Workbench | Hash of the previous entry |
| DP12 | decision_log_entry | entry_hash | TEXT | char(64) | Entered or derived in the Workbench | Hash of this entry |
| DP11 | score | id | TEXT | uuid | Entered or derived in the Workbench | Record identifier of the score |
| DP11 | score | account_id | CROSS_REF | uuid | Entered or derived in the Workbench | The loan_account this record belongs to |
| DP11 | score | case_id | CROSS_REF | uuid | Entered or derived in the Workbench | The recovery_case this record belongs to |
| DP13 | proceeds | id | TEXT | uuid | Entered or derived in the Workbench | Record identifier of the proceeds |
| DP13 | proceeds | case_id | CROSS_REF | uuid | Entered or derived in the Workbench | The recovery_case this record belongs to |
| DP13 | proceeds | treatment_id | CROSS_REF | uuid | Entered or derived in the Workbench | The treatment this record belongs to |
| DP13 | proceeds | account_payment_id | CROSS_REF | uuid | Entered or derived in the Workbench | The account_payment this record belongs to |
| DP13 | proceeds | source | LOV | varchar(12) | Entered or derived in the Workbench | Customer, LED, auction, buyer, agency, insurer, guarantor |
| DP13 | proceeds | matched_to | LOV | varchar(15) | Entered or derived in the Workbench | Installment, settlement, fee, sale proceeds, unmatched |
| DP13 | write_off | id | TEXT | uuid | Entered or derived in the Workbench | Record identifier of the write-off |
| DP13 | write_off | case_id | CROSS_REF | uuid | Entered or derived in the Workbench | The recovery_case this record belongs to |
| DP13 | write_off | decision_log_id | CROSS_REF | uuid | Entered or derived in the Workbench | The decision_log_entry this record belongs to |
| DP13 | write_off | tax_criteria_met | BOOLEAN | boolean | Entered or derived in the Workbench | True when the tax criteria are met |
| DP13 | write_off | committee_date | DATE | date | Entered or derived in the Workbench | Committee approval date |
| DP13 | write_off | recovered_after | NUMBER | numeric(18,2) | Entered or derived in the Workbench | Recovered after charge-off to date, baht |
| DP14 | rule_row | id | TEXT | uuid | Entered or derived in the Workbench | Record identifier of the rule row |
| DP14 | rule_row | rule_id | TEXT | varchar(20) | Entered or derived in the Workbench | Rule ID, for example R-LIT-12 |
| DP14 | rule_row | rule_version | TEXT | varchar(20) | Entered or derived in the Workbench | Version |
| DP14 | rule_row | route_set | LOV | varchar(15) | Entered or derived in the Workbench | Route set |
| DP14 | rule_row | from_state | TEXT | varchar(60) | Entered or derived in the Workbench | From state |
| DP14 | rule_row | event_code | TEXT | varchar(60) | Entered or derived in the Workbench | Event |
| DP14 | rule_row | condition_expr | TEXT | varchar(1000) | Entered or derived in the Workbench | Condition |
| DP14 | rule_row | action_text | TEXT | varchar(1000) | Entered or derived in the Workbench | Action |
| DP14 | rule_row | to_state | TEXT | varchar(60) | Entered or derived in the Workbench | To state |
| DP14 | rule_row | owner_role | LOV | varchar(20) | Entered or derived in the Workbench | Owner of the next state |
| DP14 | rule_row | timer_spec | TEXT | varchar(60) | Entered or derived in the Workbench | Timer |
| DP14 | rule_row | valid_from | DATE | date | Entered or derived in the Workbench | Valid from |
| DP14 | rule_row | valid_to | DATE | date | Entered or derived in the Workbench | Valid to |
| DP14 | rule_row | approved_by | USER_REF | uuid | Entered or derived in the Workbench | Who approved the version |
| DP14 | rule_row | test_case_id | TEXT | varchar(20) | Entered or derived in the Workbench | Test case that proves the rule |
| DP14 | delegation_limit | id | TEXT | uuid | Entered or derived in the Workbench | Record identifier of the delegation limit |
| DP14 | delegation_limit | decision_code | LOV | varchar(8) | Entered or derived in the Workbench | Decision the limit applies to |
| DP14 | delegation_limit | approval_level | LOV | varchar(4) | Entered or derived in the Workbench | Level 1 to 6 under Regulation กกค.540031 |
| DP14 | delegation_limit | product_group | LOV | varchar(15) | Entered or derived in the Workbench | Product group |
| DP14 | delegation_limit | principal_limit | NUMBER | numeric(18,2) | Entered or derived in the Workbench | Principal limit, baht; empty means no limit |
| DP14 | delegation_limit | loss_pct_limit | NUMBER | numeric(5,2) | Entered or derived in the Workbench | Loss limit as a percentage |
| DP14 | delegation_limit | min_price_pct_fmv | NUMBER | numeric(5,2) | Entered or derived in the Workbench | Lowest sale price as a percentage of fair market value |
| DP14 | delegation_limit | holder_user_id | USER_REF | uuid | Entered or derived in the Workbench | Person holding the level |
| DP14 | delegation_limit | substitute_user_id | USER_REF | uuid | Entered or derived in the Workbench | Substitute when the holder is absent |
| DP14 | delegation_limit | valid_from | DATE | date | Entered or derived in the Workbench | Valid from |
| DP14 | delegation_limit | valid_to | DATE | date | Entered or derived in the Workbench | Valid to |
| DP14 | lov_value | id | TEXT | uuid | Entered or derived in the Workbench | Record identifier of the list value |
| DP14 | lov_value | lov_code | TEXT | varchar(30) | Entered or derived in the Workbench | List code, for example LOV-ROUTE |
| DP14 | lov_value | value_code | TEXT | varchar(30) | Entered or derived in the Workbench | Value code |
| DP14 | lov_value | label_en | TEXT | varchar(120) | Entered or derived in the Workbench | English label |
| DP14 | lov_value | label_th | TEXT | varchar(120) | Entered or derived in the Workbench | Thai label |
| DP14 | lov_value | sort_order | NUMBER | integer | Entered or derived in the Workbench | Display order |
| DP14 | lov_value | valid_from | DATE | date | Entered or derived in the Workbench | Valid from |
| DP14 | role | id | TEXT | uuid | Entered or derived in the Workbench | Record identifier of the role |
| DP14 | role | role_code | TEXT | varchar(20) | Entered or derived in the Workbench | Role code, for example RW-CASEOWN |
| DP14 | role | role_name | TEXT | varchar(80) | Entered or derived in the Workbench | Role name |
| DP14 | role | role_class | LOV | varchar(15) | Entered or derived in the Workbench | Bank user, partner user, non-human actor |
| DP14 | role | default_scope | LOV | varchar(8) | Entered or derived in the Workbench | Own, team, region, all |
| DP14 | permission | id | TEXT | uuid | Entered or derived in the Workbench | Record identifier of the permission |
| DP14 | permission | role_id | CROSS_REF | uuid | Entered or derived in the Workbench | The role this record belongs to |
| DP14 | permission | capability_area | LOV | varchar(30) | Entered or derived in the Workbench | One of the 14 capability areas |
| DP14 | permission | letters | TEXT | varchar(5) | Entered or derived in the Workbench | C, R, U, D and A, or a dash for none |
| DP14 | permission | matrix_version | TEXT | varchar(20) | Entered or derived in the Workbench | Permission matrix version |
| DP14 | template | id | TEXT | uuid | Entered or derived in the Workbench | Record identifier of the template |
| DP14 | template | template_code | TEXT | varchar(30) | Entered or derived in the Workbench | Template code |
| DP14 | template | template_version | NUMBER | integer | Entered or derived in the Workbench | Version |
| DP14 | template | language | LOV | varchar(2) | Entered or derived in the Workbench | Thai or English |
| DP14 | template | product_group | LOV | varchar(15) | Entered or derived in the Workbench | Product group it applies to |
| DP14 | template | body_ref | ATTACHMENT | varchar(400) | Entered or derived in the Workbench | Stored template body |
| DP14 | template | approved_by_legal | BOOLEAN | boolean | Entered or derived in the Workbench | True once Legal approves the wording |

## By source

| Fields by source system |  |  |  |
|---|---|---|---|
| Count of mapped fields per source system. |  |  |  |
| Source system | Fields | Refresh | Interface |
| Core bank (ALS) | 32 | Daily, end of day | INT-01, INT-02 |
| AMIS | 15 | Monthly | INT-12 |
| LIT | 12 | Daily, end of day | INT-09 |
| CCMS | 11 | Weekly | INT-10 |
| SCBPDM | 9 | Daily, end of day | INT-04 |
| COLLINS | 7 | Daily; monthly for some models | INT-08 |
| SVAF | 5 | Weekly | INT-11 |
| WIN | 5 | Weekly | INT-15 |
| GL | 5 | Monthly | INT-16 |
| EFS | 3 | Daily, end of day | INT-07 |
| RPS | 2 | Weekly | INT-13 |
| ACE | 1 | Per request | INT-34 |
| Entra ID | 1 | At each sign-in | INT-21 |

## Mapping rules

| Rules every mapping follows |  |
|---|---|
| Applied to every inbound field. |  |
| Rule | Detail |
| Business date | Every loaded row carries the business date of its load in data_as_of |
| Dates | Buddhist Era years are converted to Gregorian at load; the Workbench stores Gregorian dates |
| Amounts | Amounts are stored in THB as numeric with two decimals |
| Codes | Source codes map to Workbench lists through a versioned code map. An unmapped code holds the row in the exception list |
| Personal data | National ID and passport numbers are tokenized at load; contact values are masked by role |
| Keys | Source keys are kept on the record; Workbench identifiers are UUIDs |
| Customer facts | Customer facts come from SCBPDM and the core bank through COLLINS (DL20) |
| Contact history | Contact history before day 90 comes from EFS through COLLINS (DL29) |
