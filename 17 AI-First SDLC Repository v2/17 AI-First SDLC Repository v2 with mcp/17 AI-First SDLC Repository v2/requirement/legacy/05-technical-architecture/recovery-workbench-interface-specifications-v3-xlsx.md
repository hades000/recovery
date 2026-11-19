<!-- source: 05 Technical architecture/Recovery Workbench Interface Specifications v3.xlsx -->
<!-- converted: 2026-11-16 from XLSX -->

> **Source:** `05 Technical architecture/Recovery Workbench Interface Specifications v3.xlsx`  
> **Converted from:** XLSX

## Interfaces

| Interface specifications |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 25 numbered interfaces the Workbench builds or reads, including INT-35 (NLEADS credit decision) and INT-36 (EasyApp e-signature), the two new ACE inbound interfaces raised in RWB-ACE-001. Inbound source interfaces are owned by the ACE team; this sheet and the Field mapping sheet are the ACE ingestion contract. No component calls a system of record directly. Supersedes v2. |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| ID | System | Purpose | Direction | Approach | Owner | Trigger | Payload | Frequency | Volume | Error handling | Retry | Owner of the fix | Standard | Decision |
| INT-01 | Core bank (ALS) | Loan accounts, balances, arrears, days past due, classification | In, into ACE | ACE ingestion, read through v_ace_account | ACE team | ACE batch complete for ALS (v_ace_batch_status) | ACCOUNT_KEY, CONTRACT_DATE, INTEREST_RATE, DELAY_DAYS, TOTAL_BALANCE, ACCOUNTING_BALANCE, Principal, AINT1, AINT2, AFEE, LAST_PAYMENT_DATE, NEXT_INSTALLMENT_DATE, Product_Category_Host, ms_data_dt | Daily, end of day | About 28,100 accounts in the active inventory and 156,400 further hire purchase accounts at 90 days past due or more, daily | ACE ingestion refuses the feed whole if the business date, structure, control totals or keys fail. The Workbench reads the last complete business date from v_ace_batch_status and marks the data product stale | ACE ingestion retries on its own schedule; the Workbench raises AceDataLate when the business date is not complete at its cut-off | ACE team | File specification | None |
| INT-02 | Core bank (ALS) | Payments posted to each account | In, into ACE | ACE ingestion, read through v_ace_payment | ACE team | ACE batch complete for ALS (v_ace_batch_status) | Payment_Code, hashed_account_key, Payment_Date, Payment_Amount, ms_data_dt | Daily, end of day | Payments on recovery accounts each day | ACE ingestion refuses the feed whole if the business date, structure, control totals or keys fail. The Workbench reads the last complete business date from v_ace_batch_status and marks the data product stale | ACE ingestion retries on its own schedule; the Workbench raises AceDataLate when the business date is not complete at its cut-off | ACE team | File specification | None |
| INT-04 | SCBPDM | Customer profile, identifiers and contact details | In, into ACE | ACE ingestion, read through v_ace_customer and v_ace_contact | ACE team | ACE batch complete for SCBPDM (v_ace_batch_status) | CIF, party type, name, identifier token, date of birth, segment, contact points with consent | Daily, end of day | Every party on an open case, about 23,600 cases at go-live | ACE ingestion refuses the feed whole if the business date, structure, control totals or keys fail. The Workbench reads the last complete business date from v_ace_batch_status and marks the data product stale | ACE ingestion retries on its own schedule; the Workbench raises AceDataLate when the business date is not complete at its cut-off | ACE team | File specification | DL20 |
| INT-07 | EFS | Collections history, action codes and promises before day 90 | In, into ACE | ACE ingestion, read through v_ace_efs_action | ACE team | ACE batch complete for EFS (v_ace_batch_status) | Actioncode ID, Description, Action Contact Status, Call Result, contact date, promise amount and date | Daily, end of day | History for about 3,110 new accounts a month at entry, then daily changes | ACE ingestion refuses the feed whole if the business date, structure, control totals or keys fail. The Workbench reads the last complete business date from v_ace_batch_status and marks the data product stale | ACE ingestion retries on its own schedule; the Workbench raises AceDataLate when the business date is not complete at its cut-off | ACE team | File specification | DL29 |
| INT-08 | COLLINS models | Scores, return by route, price and sale success estimates, scheme suggestions | In, into ACE | ACE ingestion, read through v_ace_score | ACE team | ACE batch complete for COLLINS (v_ace_batch_status) | model code, model version, account key, score, estimate, route, score date | Daily; monthly for some models | One row per account and model each day | ACE ingestion refuses the feed whole if the business date, structure, control totals or keys fail. The Workbench reads the last complete business date from v_ace_batch_status and marks the data product stale | ACE ingestion retries on its own schedule; the Workbench raises AceDataLate when the business date is not complete at its cut-off | ACE team | File specification | None |
| INT-09 | LIT | Litigation status and lawsuit numbers | In, into ACE | ACE ingestion, read through v_ace_lawsuit and v_ace_hearing | ACE team | ACE batch complete for LIT (v_ace_batch_status) | iacct, LAWSUIT_NO, AAMT_SUIT, black case number, NCOURT, STATE_RES_NAME, Total_Pay | Daily, end of day | About 670 lawsuits filed a month for Mortgage and SSME | ACE ingestion refuses the feed whole if the business date, structure, control totals or keys fail. The Workbench reads the last complete business date from v_ace_batch_status and marks the data product stale | ACE ingestion retries on its own schedule; the Workbench raises AceDataLate when the business date is not complete at its cut-off | ACE team | File specification | None |
| INT-10 | CCMS | Collateral records | In, into ACE | ACE ingestion, read through v_ace_collateral and v_ace_collateral_detail | ACE team | ACE batch complete for CCMS (v_ace_batch_status) | Collateral number, type, title deed, plot, area, province, district, subdistrict, insured value, account links | Weekly | Collateral on recovery accounts, weekly | ACE ingestion refuses the feed whole if a check fails. The Workbench reads the last complete business date from v_ace_batch_status and marks the data product stale | ACE ingestion retries on its own schedule; the Workbench raises AceDataLate when the business date is not complete at its cut-off | ACE team | File specification | DL06, DL12 |
| INT-11 | SVAF | Appraisals | In, into ACE | ACE ingestion, read through v_ace_valuation | ACE team | ACE batch complete for SVAF (v_ace_batch_status) | Appraisal No., Appraised Value, Forced Sale Value, Appraisal Date, collateral or asset reference, valuer | Weekly | New and changed appraisals, weekly | ACE ingestion refuses the feed whole if a check fails. The Workbench reads the last complete business date from v_ace_batch_status and marks the data product stale | ACE ingestion retries on its own schedule; the Workbench raises AceDataLate when the business date is not complete at its cut-off | ACE team | File specification | DL06, DL12 |
| INT-12 | AMIS | Assets held, book values and asset sales | In, into ACE | ACE ingestion, read through v_ace_asset, v_ace_npa_asset and v_ace_npa_sale | ACE team | ACE batch complete for AMIS (v_ace_batch_status) | Asset ID, Asset Code, Transfer-in Type, Asset Type, Ownership Transfer in Date, Book Value, Auction Purchase Price, Sale Date, Sale Price, taxes and fees | Monthly | About 4,700 properties held; about 30 sales a month | ACE ingestion refuses the feed whole if a check fails. The Workbench reads the last complete business date from v_ace_batch_status and marks the data product stale | ACE ingestion retries on its own schedule; the Workbench raises AceDataLate when the business date is not complete at its cut-off | ACE team | File specification | DL06, DL12 |
| INT-13 | RPS | Repossessed vehicles and stock | In, into ACE | ACE ingestion, read through v_ace_npa_asset | ACE team | ACE batch complete for RPS (v_ace_batch_status) | AccNo, ContractNo, RepoDT, ReposessedCarDate, VehicleStatus, STOCK_DATE, OutBal | Weekly | About 720 vehicles repossessed a month | ACE ingestion refuses the feed whole if a check fails. The Workbench reads the last complete business date from v_ace_batch_status and marks the data product stale | ACE ingestion retries on its own schedule; the Workbench raises AceDataLate when the business date is not complete at its cut-off | ACE team | File specification | DL06, DL12 |
| INT-14 | WIN | Demand, recall and sale notices for registered mail | Out | Batch: outbound file through the integration adapters | Workbench | Notice approved and generated | ContractNO, addressee, address, notice type, template version, document reference | Daily | About 1,900 registered letters a month | Hold the case step until the file is acknowledged | Send again; after the third failure raise a task to the owning team | Owning team, platform administrator | File specification | None |
| INT-15 | WIN | Proof of delivery for registered mail | In, into ACE | ACE ingestion, read through v_ace_pod | ACE team | ACE batch complete for WIN (v_ace_batch_status) | DDMMYYYY, ContractNO, Barcode, DDMMYYYY_callBack, Sent Type | Weekly | About 1,900 proofs of delivery a month | ACE ingestion refuses the feed whole if a check fails. The Workbench reads the last complete business date from v_ace_batch_status and marks the data product stale | ACE ingestion retries on its own schedule; the Workbench raises AceDataLate when the business date is not complete at its cut-off | ACE team | File specification | None |
| INT-16 | GL | Write-off postings | In, into ACE | ACE ingestion, read through v_ace_write_off | ACE team | ACE batch complete for GL (v_ace_batch_status) | DATE, RC, OC, ACCOUNT, PRODUCT, EVENT, AMT | Monthly | Write-off postings each month | ACE ingestion refuses the feed whole if a check fails. The Workbench reads the last complete business date from v_ace_batch_status and marks the data product stale | ACE ingestion retries on its own schedule; the Workbench raises AceDataLate when the business date is not complete at its cut-off | ACE team | File specification | DL12 |
| INT-17 | NSS | SMS to customers | Out | ACE notification path | ACE team | Message approved by the contact rules | contact point, template, language, case reference | As sent | Messages per day | Record the failure on the interaction ledger | As the ACE notification path retries | ACE team | Common module interface | DL30 |
| INT-18 | LINE OA | LINE messages to customers | Out | ACE notification path | ACE team | Message approved by the contact rules | LINE identifier, template, language, case reference | As sent | Messages per day | Record the failure on the interaction ledger | As the ACE notification path retries | ACE team | Common module interface | DL30 |
| INT-19 | Data lake and Power BI | Case, queue, decision and outcome data for reporting | Out | Daily batch | Workbench | Nightly | Case, queue, task, timer, decision log and outcome records changed that day | Daily | All changes in the day | Hold the publish and raise an alert | Run again in the next window | Platform administrator | File specification | None |
| INT-20 | COLLINS | Decisions and outcomes for model learning | Out | Daily batch to the data lake | Workbench | Nightly | Decision log entries and outcomes changed that day | Daily | All decisions in the day | Hold the publish and raise an alert | Run again in the next window | Platform administrator | File specification | None |
| INT-21 | Entra ID and the bank IAM | Sign-in and the roles each user holds | In | ACE sign-in; group-to-role mapping read through v_ace_iam_group | ACE team | Sign-in | User identity and Entra ID group membership; group-to-role mapping held in iam_group (new ACE table) and read through v_ace_iam_group.entra_group | At each sign-in | Every sign-in | Refuse the session and log it | None | Security administrator | OpenID Connect | DL40 |
| INT-22 | PII Kafka, audit and SOC logs | Personal data access, audit and security events | Out | ACE logging | ACE team | Each event | Who, what, when, which record, which fields | As they happen | Every read of personal data and every security event | As the ACE logging service | As the ACE logging service | ACE team | AsyncAPI 3.0 | None |
| INT-23 | Enterprise AI model endpoint | The model the agents call | Both | Private endpoint in the SCB tenant | Bank platform | An agent step | Prompt version, inputs with personal data removed or masked, the requested output schema | Per request | Per agent step | The rule result is used and the case still routes | None within the step; the agent is called again on the next event | Enterprise AI | OpenAPI 3.1 | DL33 |
| INT-24 | Partner portal | Instructions to partners and the results they report | Both | Workbench screens through the external gateway | Workbench | Instruction sent or result entered | Instruction type, case reference, documents, due date; result code, dates, amounts, fee | As entered | Per instruction | Show the error to the partner user and keep the entry | The user submits again | Partner and agency manager | OpenAPI 3.1 | DL03 |
| INT-25 | Debt buyers | Debt sale data tape for an awarded lot | Out | Batch: outbound file through the integration adapters | Workbench | Lot awarded | BorrCode, OS By Acct, SellingPriceByAcct, account data agreed in the sale terms, personal data as the sale terms allow | Per lot | About 3,800 accounts a year across the lots | Hold the case step until the file is acknowledged | Send again; after the third failure raise a task to the owning team | Owning team, platform administrator | File specification | None |
| INT-34 | ACE common module | Shared case view, entities, restructure calculator, notification path | Both | Published module interface | ACE team | Call or application event | As published by the common module | Per request | Per call | Return the error to the calling module | As the caller decides | ACE team | Module interface | DL14 |
| INT-35 | NLEADS | Credit approval result for a restructure plan, new to ACE and raised in RWB-ACE-001. The officer's submission in NLEADS stays INT-26 | In, into ACE | ACE ingestion, read through v_ace_credit_decision | ACE team | ACE batch complete for NLEADS (v_ace_batch_status) | nleads_ref, credit_result, credit_result_reason, decided_at | As decisions are made | One row per credit decision on a restructure plan | ACE ingestion refuses the feed whole if a check fails. The Workbench reads the last complete business date from v_ace_batch_status and marks the data product stale | ACE ingestion retries on its own schedule; the Workbench raises AceDataLate when the business date is not complete at its cut-off | ACE team | File specification | D-RCV-35 |
| INT-36 | EasyApp | E-signature reference and status for a restructure agreement, new to ACE and raised in RWB-ACE-001 | In, into ACE | ACE ingestion, read through v_ace_esign | ACE team | ACE batch complete for EasyApp (v_ace_batch_status) | external_ref | As signatures are requested | One row per signature request | ACE ingestion refuses the feed whole if a check fails. The Workbench reads the last complete business date from v_ace_batch_status and marks the data product stale | ACE ingestion retries on its own schedule; the Workbench raises AceDataLate when the business date is not complete at its cut-off | ACE team | File specification | D-RCV-35 |

## Field mapping

| Source field to Workbench field |  |  |  |  |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|---|---|---|
| 82 mappings from the source system and bank file fields to the ACE table.column that holds each value (Tier 1 exists in ACE today, Tier 2 is added by the ACE team in RWB-ACE-001) and the recovery.v_ace_* view column the Workbench reads, per the LDM v7 ACE mapping sheet. Outbound rows (INT-14, INT-25) name the Workbench (Tier 4) column the file is built from. The inbound rows are the ACE ingestion specification and are owned by the ACE team. |  |  |  |  |  |  |  |  |  |  |
| Interface | Source field | Table.column | Tier | Read path | LDM field | Data type | Physical type | Mandatory | Transformation | Owner |
| INT-01 | ACCOUNT_KEY / iacct / AccNo | account.account_key | Tier 1 | v_ace_account.account_no | DF-ACC-002 | TEXT | varchar(20) | Yes | Direct copy; ACE business key | ACE team |
| INT-01 | ContractNo | account.contract_number | Tier 1 | v_ace_account.contract_no | DF-ACC-003 | TEXT | varchar(20) | No | Direct copy | ACE team |
| INT-01 | acct_prd_cd | product.product_key | Tier 1 | v_ace_account.product_code | DF-ACC-004 | LOV | varchar(10) | Yes | Direct copy | ACE team |
| INT-01 | BU | account.business_unit | Tier 2 | v_ace_account.business_unit | DF-ACC-006 | LOV | varchar(10) | No | Direct copy | ACE team |
| INT-01 | CONTRACT_DATE | account.contract_date | Tier 1 | v_ace_account.contract_date | DF-ACC-007 | DATE | date | No | Direct copy | ACE team |
| INT-01 | INTEREST_RATE | account.interest_rate | Tier 1 | v_ace_account.interest_rate | DF-ACC-008 | NUMBER | numeric(7,4) | No | Direct copy; the view casts numeric(38,2) to numeric(7,4) | ACE team |
| INT-01 | Principal | account.principal_outstanding | Tier 2 | v_ace_account.principal_outstanding | DF-ACC-009 | NUMBER | numeric(18,2) | Yes | Direct copy | ACE team |
| INT-01 | AINT1 + AINT2 | account.interest_outstanding | Tier 2 | v_ace_account.interest_outstanding | DF-ACC-010 | NUMBER | numeric(18,2) | Yes | AINT1 plus AINT2 | ACE team |
| INT-01 | AFEE | account.fees_outstanding | Tier 2 | v_ace_account.fees_outstanding | DF-ACC-011 | NUMBER | numeric(18,2) | Yes | Direct copy | ACE team |
| INT-01 | TOTAL_BALANCE | account.total_balance | Tier 1 | v_ace_account.total_balance | DF-ACC-012 | NUMBER | numeric(18,2) | Yes | Direct copy | ACE team |
| INT-01 | ACCOUNTING_BALANCE | account.accounting_balance | Tier 1 | v_ace_account.accounting_balance | DF-ACC-013 | NUMBER | numeric(18,2) | No | Direct copy | ACE team |
| INT-01 | DELAY_DAYS | account.delay_days | Tier 1 | v_ace_account.days_past_due | DF-ACC-014 | NUMBER | integer | Yes | Direct copy; renamed days_past_due in the view | ACE team |
| INT-01 | Bucket | account.daily_bucket | Tier 2 | v_ace_account.bucket | DF-ACC-015 | LOV | varchar(10) | No | Direct copy; daily bucket (bucket_log_snapshot is monthly) | ACE team |
| INT-01 | LAST_PAYMENT_DATE | account.last_payment_date | Tier 1 | v_ace_account.last_payment_date | DF-ACC-017 | DATE | date | No | Direct copy | ACE team |
| INT-01 | NEXT_INSTALLMENT_DATE | account.next_installment_date | Tier 1 | v_ace_account.next_installment_date | DF-ACC-018 | DATE | date | No | Direct copy | ACE team |
| INT-01 | TDR list | account.is_restructured | Tier 1 | v_ace_account.tdr_flag | DF-ACC-019 | BOOLEAN | boolean | Yes | Y/N text cast to boolean by recovery.ace_to_boolean in the view | ACE team |
| INT-01 | Last_TDR_Date | account.last_tdr_date | Tier 1 | v_ace_account.last_tdr_date | DF-ACC-020 | DATE | date | No | Direct copy | ACE team |
| INT-01 | ms_data_dt | account.core_banking_system_date | Tier 1 | v_ace_account.data_as_of | DF-ACC-021 | DATE | date | Yes | Business date of the ACE batch | ACE team |
| INT-02 | Payment_Code | payment.pay_key | Tier 1 | v_ace_payment.payment_code | DF-ACC-024 | TEXT | varchar(20) | Yes | Direct copy; ACE business key | ACE team |
| INT-02 | Payment_Date | payment.pay_date | Tier 1 | v_ace_payment.payment_date | DF-ACC-025 | DATE | date | Yes | varchar cast to date by recovery.ace_to_date in the view | ACE team |
| INT-02 | Payment_Amount | payment.total_amount | Tier 1 | v_ace_payment.payment_amount | DF-ACC-026 | NUMBER | numeric(18,2) | Yes | Direct copy | ACE team |
| INT-02 | ms_data_dt | account.core_banking_system_date | Tier 1 | v_ace_payment.data_as_of | DF-ACC-028 | DATE | date | Yes | Read from the account batch date; no new payment column | ACE team |
| INT-02 | Payment_Amount | payment.total_amount | Tier 1 | v_ace_payment.payment_amount | DF-FIN-006 | NUMBER | numeric(18,2) | Yes | Direct copy | ACE team |
| INT-02 | Payment_Date | payment.pay_date | Tier 1 | v_ace_payment.payment_date | DF-FIN-007 | DATE | date | Yes | varchar cast to date by recovery.ace_to_date in the view | ACE team |
| INT-04 | CIF | customer.person_key | Tier 1 | v_ace_customer.cif_no | DF-PTY-002 | TEXT | varchar(20) | Yes | Direct copy; ACE business key | ACE team |
| INT-04 | Segment | customer.segment | Tier 2 | v_ace_customer.segment | DF-PTY-009 | LOV | varchar(20) | No | Direct copy | ACE team |
| INT-07 | Actioncode ID | efs_action.action_code | Tier 1 | v_ace_efs_action.action_code | DF-INT-007 | LOV | varchar(10) | No | Direct copy | ACE team |
| INT-07 | Call Result | efs_action.contact_result | Tier 2 | v_ace_efs_action.contact_result | DF-INT-008 | LOV | varchar(20) | No | Direct copy | ACE team |
| INT-09 | LAWSUIT_NO / LAWSUIT_RUN | lawsuit.lawsuit_no | Tier 2 | v_ace_lawsuit.lawsuit_no | DF-LEG-005 | TEXT | varchar(30) | No | Direct copy | ACE team |
| INT-09 | เลขที่คดีดำ | lawsuit.black_case_no | Tier 2 | v_ace_lawsuit.black_case_no | DF-LEG-006 | TEXT | varchar(30) | No | Direct copy | ACE team |
| INT-09 | NCOURT | lawsuit.court_name | Tier 2 | v_ace_lawsuit.court_name | DF-LEG-008 | TEXT | varchar(120) | No | Direct copy | ACE team |
| INT-09 | AAMT_SUIT | lawsuit.claim_amount | Tier 2 | v_ace_lawsuit.claim_amount | DF-LEG-009 | NUMBER | numeric(18,2) | No | Direct copy | ACE team |
| INT-09 | Judgment date | lawsuit.judgment_date | Tier 2 | v_ace_lawsuit.judgment_date | DF-LEG-011 | DATE | date | No | Direct copy | ACE team |
| INT-10 | Title Deed / Ownership Doc | collateral_detail.title_doc_no | Tier 2 | v_ace_collateral_detail.title_doc_no | DF-COL-004 | TEXT | varchar(40) | No | Direct copy | ACE team |
| INT-10 | Plot No. | collateral_detail.plot_no | Tier 2 | v_ace_collateral_detail.plot_no | DF-COL-005 | TEXT | varchar(20) | No | Direct copy | ACE team |
| INT-10 | Area | collateral_detail.area_text | Tier 2 | v_ace_collateral_detail.area_text | DF-COL-006 | TEXT | varchar(20) | No | Direct copy | ACE team |
| INT-10 | Province | collateral_detail.province | Tier 2 | v_ace_collateral_detail.province | DF-COL-007 | LOV | varchar(40) | No | Direct copy | ACE team |
| INT-10 | District | collateral_detail.district | Tier 2 | v_ace_collateral_detail.district | DF-COL-008 | TEXT | varchar(60) | No | Direct copy | ACE team |
| INT-10 | Subdistrict | collateral_detail.subdistrict | Tier 2 | v_ace_collateral_detail.subdistrict | DF-COL-009 | TEXT | varchar(60) | No | Direct copy | ACE team |
| INT-10 | Insvalue | collateral_detail.insured_value | Tier 2 | v_ace_collateral_detail.insured_value | DF-COL-012 | NUMBER | numeric(18,2) | No | Direct copy | ACE team |
| INT-11 | Appraisal No. | valuation.appraisal_no | Tier 2 | v_ace_valuation.appraisal_no | DF-COL-021 | TEXT | varchar(20) | Yes | Direct copy | ACE team |
| INT-11 | Appraised Value | valuation.appraised_value | Tier 2 | v_ace_valuation.appraised_value | DF-COL-023 | NUMBER | numeric(18,2) | Yes | Direct copy | ACE team |
| INT-11 | Forced Sale Value | valuation.forced_sale_value | Tier 2 | v_ace_valuation.forced_sale_value | DF-COL-024 | NUMBER | numeric(18,2) | No | Direct copy | ACE team |
| INT-11 | Appraisal Date | valuation.appraisal_date | Tier 2 | v_ace_valuation.appraisal_date | DF-COL-025 | DATE | date | Yes | Direct copy | ACE team |
| INT-12 | Asset ID | asset.asset_key | Tier 1 | v_ace_asset.asset_ref | DF-COL-031 | TEXT | varchar(20) | Yes | Direct copy; ACE business key | ACE team |
| INT-12 | Asset Code | npa_asset.asset_code | Tier 2 | v_ace_npa_asset.asset_code | DF-COL-032 | TEXT | varchar(20) | No | Direct copy | ACE team |
| INT-12 | Asset Type | asset.asset_type | Tier 1 | v_ace_asset.asset_type | DF-COL-033 | LOV | varchar(20) | Yes | Direct copy | ACE team |
| INT-12 | Transfer-in Type | npa_asset.transfer_in_type | Tier 2 | v_ace_npa_asset.transfer_in_type | DF-COL-034 | LOV | varchar(20) | Yes | Direct copy | ACE team |
| INT-12 | From Segment | npa_asset.from_segment | Tier 2 | v_ace_npa_asset.from_segment | DF-COL-035 | LOV | varchar(20) | No | Direct copy | ACE team |
| INT-12 | Ownership Transfer in Date | npa_asset.transfer_in_date | Tier 2 | v_ace_npa_asset.transfer_in_date | DF-COL-036 | DATE | date | Yes | Direct copy | ACE team |
| INT-12 | Book  Value | npa_asset.book_value | Tier 2 | v_ace_npa_asset.book_value | DF-COL-037 | NUMBER | numeric(18,2) | Yes | Direct copy | ACE team |
| INT-12 | Auction Purchase Price | npa_asset.auction_purchase_price | Tier 2 | v_ace_npa_asset.auction_purchase_price | DF-COL-038 | NUMBER | numeric(18,2) | No | Direct copy | ACE team |
| INT-12 | Contract Date | npa_sale.contract_date | Tier 2 | v_ace_npa_sale.contract_date | DF-SAL-012 | DATE | date | Yes | Direct copy | ACE team |
| INT-12 | Sale Date | npa_sale.sale_date | Tier 2 | v_ace_npa_sale.sale_date | DF-SAL-013 | DATE | date | Yes | Direct copy | ACE team |
| INT-12 | Sale Price | npa_sale.sale_price | Tier 2 | v_ace_npa_sale.sale_price | DF-SAL-014 | NUMBER | numeric(18,2) | Yes | Direct copy | ACE team |
| INT-12 | Sale Transfer Fee | npa_sale.transfer_fee | Tier 2 | v_ace_npa_sale.transfer_fee | DF-SAL-015 | NUMBER | numeric(18,2) | No | Direct copy | ACE team |
| INT-12 | Specific Business Tax | npa_sale.specific_business_tax | Tier 2 | v_ace_npa_sale.specific_business_tax | DF-SAL-016 | NUMBER | numeric(18,2) | No | Direct copy | ACE team |
| INT-12 | Corporate Income Tax | npa_sale.corporate_income_tax | Tier 2 | v_ace_npa_sale.corporate_income_tax | DF-SAL-017 | NUMBER | numeric(18,2) | No | Direct copy | ACE team |
| INT-12 | Incentive Amount | npa_sale.incentive_amount | Tier 2 | v_ace_npa_sale.incentive_amount | DF-SAL-019 | NUMBER | numeric(18,2) | No | Direct copy | ACE team |
| INT-13 | ReposessedCarDate | npa_asset.repossessed_date | Tier 2 | v_ace_npa_asset.repossessed_date | DF-COL-039 | DATE | date | No | Thai year date YYMMDD converted to a Gregorian date | ACE team |
| INT-13 | STOCK_DATE | npa_asset.stock_date | Tier 2 | v_ace_npa_asset.stock_date | DF-COL-040 | DATE | date | No | Converted to a date | ACE team |
| INT-14 | DDMMYYYY | notice.sent_date | Tier 4 | Workbench table | DF-LEG-019 | DATE | date | No | Direct copy | Workbench |
| INT-14 | Barcode | notice.barcode | Tier 4 | Workbench table | DF-LEG-020 | TEXT | varchar(40) | No | Direct copy | Workbench |
| INT-14 | DDMMYYYY_callBack | notice.callback_date | Tier 4 | Workbench table | DF-LEG-021 | DATE | date | No | Direct copy | Workbench |
| INT-14 | Sent Type | notice.sent_type | Tier 4 | Workbench table | DF-LEG-023 | LOV | varchar(10) | No | Direct copy | Workbench |
| INT-15 | DDMMYYYY | pod_receipt.sent_date | Tier 2 | v_ace_pod.sent_date | DF-LEG-019 | DATE | date | No | Direct copy | ACE team |
| INT-15 | Barcode | pod_receipt.barcode | Tier 2 | v_ace_pod.barcode | DF-LEG-020 | TEXT | varchar(40) | No | Direct copy | ACE team |
| INT-15 | DDMMYYYY_callBack | pod_receipt.callback_date | Tier 2 | v_ace_pod.callback_date | DF-LEG-021 | DATE | date | No | Direct copy | ACE team |
| INT-15 | Sent Type | pod_receipt.sent_type | Tier 2 | v_ace_pod.sent_type | DF-LEG-023 | LOV | varchar(10) | No | Direct copy | ACE team |
| INT-16 | AMT | gl_write_off.amount | Tier 2 | v_ace_write_off.amount | DF-FIN-013 | NUMBER | numeric(18,2) | Yes | Direct copy | ACE team |
| INT-16 | DATE | gl_write_off.posted_date | Tier 2 | v_ace_write_off.posted_date | DF-FIN-016 | DATE | date | No | Direct copy | ACE team |
| INT-16 | RC | gl_write_off.responsibility_center | Tier 2 | v_ace_write_off.responsibility_center | DF-FIN-017 | TEXT | varchar(10) | No | Direct copy | ACE team |
| INT-16 | OC | gl_write_off.cost_center | Tier 2 | v_ace_write_off.cost_center | DF-FIN-018 | TEXT | varchar(10) | No | Direct copy | ACE team |
| INT-16 | PRODUCT | gl_write_off.gl_product | Tier 2 | v_ace_write_off.gl_product | DF-FIN-019 | TEXT | varchar(10) | No | Direct copy | ACE team |
| INT-25 | BorrCode | debt_sale_account.borrower_code | Tier 4 | Workbench table | DF-SAL-034 | TEXT | varchar(20) | No | Direct copy | Workbench |
| INT-25 | OS By Acct | debt_sale_account.outstanding | Tier 4 | Snapshot of v_ace_account.total_balance at the cut-off date | DF-SAL-035 | NUMBER | numeric(18,2) | Yes | Direct copy | Workbench |
| INT-25 | SellingPriceByAcct | debt_sale_account.selling_price | Tier 4 | Workbench table | DF-SAL-036 | NUMBER | numeric(18,2) | No | Direct copy | Workbench |
| INT-35 | nleads_ref | credit_decision.nleads_ref | Tier 2 | v_ace_credit_decision.nleads_ref | DF-TRT-023 | TEXT | varchar(30) | No | Direct copy | ACE team |
| INT-35 | credit_result | credit_decision.credit_result | Tier 2 | v_ace_credit_decision.credit_result | DF-TRT-024 | LOV | varchar(10) | No | Direct copy | ACE team |
| INT-35 | credit_result_reason | credit_decision.credit_result_reason | Tier 2 | v_ace_credit_decision.credit_result_reason | DF-TRT-025 | TEXT | varchar(1000) | No | Direct copy | ACE team |
| INT-35 | decided_at | credit_decision.decided_at | Tier 2 | v_ace_credit_decision.decided_at | DF-TRT-026 | DATE | timestamptz(6) | No | Direct copy | ACE team |
| INT-36 | external_ref | esign_request.external_ref | Tier 2 | v_ace_esign.external_ref | DF-DOC-103 | TEXT | varchar(60) | No | Direct copy | ACE team |

## Outbound checks

| Checks every outbound file passes |  |  |
|---|---|---|
| Applied to every outbound file. The inbound checks are the ACE ingestion contract, owned by the ACE team in RWB-ACE-001; the Workbench reads completion from v_ace_batch_status and runs no inbound check. |  |  |
| Check | What it tests | If it fails |
| Layout | Every field matches the agreed file specification and template version | Do not send; raise to the platform administrator |
| Control totals | The header count and amount totals match the rows in the file | Do not send; raise to the platform administrator |
| Acknowledgement | The receiving system confirms the file | Hold the case step and send again |

## Key

| Key |  |  |
|---|---|---|
| What each term means. |  |  |
| Item | Term | Meaning |
| Approach | ACE ingestion | ACE receives the COLLINS feed or the file and lands it in its own tables; the Workbench loads nothing and reads the result through a v_ace_* view |
| Standard | OpenAPI 3.1 | Request and response interfaces |
| Standard | AsyncAPI 3.0 | Event interfaces |
| Standard | File specification | Layout, control totals, business date and checks |
| Column | Owner of the fix | Who is told and acts when the interface fails |
| Direction | In, into ACE | ACE ingests the source; the Workbench reads it through a read-only v_ace_* view |
| Trigger | ACE batch complete | The per-source record in v_ace_batch_status for the business date |
| Owner | ACE team | Owns the inbound source interface, the ACE tables behind it and the ingestion checks |
| Owner | Workbench | Owns the outbound interface and the case data it sends |
| Owner | Bank platform | Owns a shared bank service the Workbench calls |
| Owner of the fix | ACE team | Told and acts when an inbound interface fails |
| Column | Table.column | For an inbound interface, the ACE table and column that hold the value; for an outbound interface, the Workbench column the file is built from |
| Column | Read path | The recovery.v_ace_* view column the Workbench reads; the ACE column name appears only in the view definition |
| Column | LDM field | The field ID in the Logical Data Model and Data Dictionary v7 |
| Tier | Tier 1 | An ACE table or column that exists today, read through a view and never altered by the Workbench |
| Tier | Tier 2 | A new ACE table or column owned by the ACE team and raised in RWB-ACE-001 |
| Tier | Tier 4 | A Workbench-owned table; used only by the outbound interfaces |
