<!-- source: 05 Technical architecture/Recovery Workbench Interface Specifications v2.xlsx -->
<!-- converted: 2026-11-16 from XLSX -->

> **Source:** `05 Technical architecture/Recovery Workbench Interface Specifications v2.xlsx`  
> **Converted from:** XLSX

## Interfaces

| Interface specifications |  |  |  |  |  |  |  |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 23 interfaces the Workbench builds or reads. No component calls a system of record directly. Interfaces that need same-day data are named under DL06. |  |  |  |  |  |  |  |  |  |  |  |  |  |
| ID | System | Purpose | Direction | Approach | Trigger | Payload | Frequency | Volume | Error handling | Retry | Owner of the fix | Standard | Decision |
| INT-01 | Core bank (ALS) | Loan accounts, balances, arrears, days past due, classification | In | Batch: COLLINS daily load into the ACE database | COLLINS load complete | ACCOUNT_KEY, CONTRACT_DATE, INTEREST_RATE, DELAY_DAYS, TOTAL_BALANCE, ACCOUNTING_BALANCE, Principal, AINT1, AINT2, AFEE, LAST_PAYMENT_DATE, NEXT_INSTALLMENT_DATE, Product_Category_Host, ms_data_dt | Daily, end of day | About 28,100 accounts in the active inventory and 156,400 further hire purchase accounts at 90 days past due or more, daily | Refuse the load whole if the business date, structure, control totals or keys fail. Keep the previous load in use and mark the data product stale | Check each hour until the load window closes | Data steward, platform administrator | File specification | None |
| INT-02 | Core bank (ALS) | Payments posted to each account | In | Batch: COLLINS daily load into the ACE database | COLLINS load complete | Payment_Code, hashed_account_key, Payment_Date, Payment_Amount, ms_data_dt | Daily, end of day | Payments on recovery accounts each day | Refuse the load whole if the business date, structure, control totals or keys fail. Keep the previous load in use and mark the data product stale | Check each hour until the load window closes | Data steward, platform administrator | File specification | None |
| INT-04 | SCBPDM | Customer profile, identifiers and contact details | In | Batch: COLLINS daily load into the ACE database | COLLINS load complete | CIF, party type, name, identifier token, date of birth, segment, contact points with consent | Daily, end of day | Every party on an open case, about 23,600 cases at go-live | Refuse the load whole if the business date, structure, control totals or keys fail. Keep the previous load in use and mark the data product stale | Check each hour until the load window closes | Data steward, platform administrator | File specification | DL20 |
| INT-07 | EFS | Collections history, action codes and promises before day 90 | In | Batch: COLLINS daily load into the ACE database | COLLINS load complete | Actioncode ID, Description, Action Contact Status, Call Result, contact date, promise amount and date | Daily, end of day | History for about 3,110 new accounts a month at entry, then daily changes | Refuse the load whole if the business date, structure, control totals or keys fail. Keep the previous load in use and mark the data product stale | Check each hour until the load window closes | Data steward, platform administrator | File specification | DL29 |
| INT-08 | COLLINS models | Scores, return by route, price and sale success estimates, scheme suggestions | In | Batch: COLLINS daily load into the ACE database | COLLINS load complete | model code, model version, account key, score, estimate, route, score date | Daily; monthly for some models | One row per account and model each day | Refuse the load whole if the business date, structure, control totals or keys fail. Keep the previous load in use and mark the data product stale | Check each hour until the load window closes | Data steward, platform administrator | File specification | None |
| INT-09 | LIT | Litigation status and lawsuit numbers | In | Batch: COLLINS daily load into the ACE database | COLLINS load complete | iacct, LAWSUIT_NO, AAMT_SUIT, black case number, NCOURT, STATE_RES_NAME, Total_Pay | Daily, end of day | About 670 lawsuits filed a month for Mortgage and SSME | Refuse the load whole if the business date, structure, control totals or keys fail. Keep the previous load in use and mark the data product stale | Check each hour until the load window closes | Data steward, platform administrator | File specification | None |
| INT-10 | CCMS | Collateral records | In | Batch: file load through the integration adapters | File received by the weekly cut-off | Collateral number, type, title deed, plot, area, province, district, subdistrict, insured value, account links | Weekly | Collateral on recovery accounts, weekly | Refuse the file whole if a check fails. Hold records with an unknown reference in the exception list | Mark the data product stale one business day after the file was due; ask the sending team | Data steward, the sending team | File specification | DL06, DL12 |
| INT-11 | SVAF | Appraisals | In | Batch: file load through the integration adapters | File received by the weekly cut-off | Appraisal No., Appraised Value, Forced Sale Value, Appraisal Date, collateral or asset reference, valuer | Weekly | New and changed appraisals, weekly | Refuse the file whole if a check fails. Hold records with an unknown reference in the exception list | Mark the data product stale one business day after the file was due; ask the sending team | Data steward, the sending team | File specification | DL06, DL12 |
| INT-12 | AMIS | Assets held, book values and asset sales | In | Batch: file load through the integration adapters | File received by the monthly cut-off | Asset ID, Asset Code, Transfer-in Type, Asset Type, Ownership Transfer in Date, Book Value, Auction Purchase Price, Sale Date, Sale Price, taxes and fees | Monthly | About 4,700 properties held; about 30 sales a month | Refuse the file whole if a check fails. Hold records with an unknown reference in the exception list | Mark the data product stale one business day after the file was due; ask the sending team | Data steward, the sending team | File specification | DL06, DL12 |
| INT-13 | RPS | Repossessed vehicles and stock | In | Batch: file load through the integration adapters | File received by the weekly cut-off | AccNo, ContractNo, RepoDT, ReposessedCarDate, VehicleStatus, STOCK_DATE, OutBal | Weekly | About 720 vehicles repossessed a month | Refuse the file whole if a check fails. Hold records with an unknown reference in the exception list | Mark the data product stale one business day after the file was due; ask the sending team | Data steward, the sending team | File specification | DL06, DL12 |
| INT-14 | WIN | Demand, recall and sale notices for registered mail | Out | Batch: outbound file through the integration adapters | Notice approved and generated | ContractNO, addressee, address, notice type, template version, document reference | Daily | About 1,900 registered letters a month | Hold the case step until the file is acknowledged | Send again; after the third failure raise a task to the owning team | Owning team, platform administrator | File specification | None |
| INT-15 | WIN | Proof of delivery for registered mail | In | Batch: file load through the integration adapters | File received by the weekly cut-off | DDMMYYYY, ContractNO, Barcode, DDMMYYYY_callBack, Sent Type | Weekly | About 1,900 proofs of delivery a month | Refuse the file whole if a check fails. Hold records with an unknown reference in the exception list | Mark the data product stale one business day after the file was due; ask the sending team | Data steward, the sending team | File specification | None |
| INT-16 | GL | Write-off postings | In | Batch: file load through the integration adapters | File received by the monthly cut-off | DATE, RC, OC, ACCOUNT, PRODUCT, EVENT, AMT | Monthly | Write-off postings each month | Refuse the file whole if a check fails. Hold records with an unknown reference in the exception list | Mark the data product stale one business day after the file was due; ask the sending team | Data steward, the sending team | File specification | DL12 |
| INT-17 | NSS | SMS to customers | Out | ACE notification path | Message approved by the contact rules | contact point, template, language, case reference | As sent | Messages per day | Record the failure on the interaction ledger | As the ACE notification path retries | ACE team | Common module interface | DL30 |
| INT-18 | LINE OA | LINE messages to customers | Out | ACE notification path | Message approved by the contact rules | LINE identifier, template, language, case reference | As sent | Messages per day | Record the failure on the interaction ledger | As the ACE notification path retries | ACE team | Common module interface | DL30 |
| INT-19 | Data lake and Power BI | Case, queue, decision and outcome data for reporting | Out | Daily batch | Nightly | Case, queue, task, timer, decision log and outcome records changed that day | Daily | All changes in the day | Hold the publish and raise an alert | Run again in the next window | Platform administrator | File specification | None |
| INT-20 | COLLINS | Decisions and outcomes for model learning | Out | Daily batch to the data lake | Nightly | Decision log entries and outcomes changed that day | Daily | All decisions in the day | Hold the publish and raise an alert | Run again in the next window | Platform administrator | File specification | None |
| INT-21 | Entra ID and the bank IAM | Sign-in and the roles each user holds | In | ACE sign-in | Sign-in | User identity and Entra ID group membership | At each sign-in | Every sign-in | Refuse the session and log it | None | Security administrator | OpenID Connect | DL40 |
| INT-22 | PII Kafka, audit and SOC logs | Personal data access, audit and security events | Out | ACE logging | Each event | Who, what, when, which record, which fields | As they happen | Every read of personal data and every security event | As the ACE logging service | As the ACE logging service | ACE team | AsyncAPI 3.0 | None |
| INT-23 | Enterprise AI model endpoint | The model the agents call | Both | Private endpoint in the SCB tenant | An agent step | Prompt version, inputs with personal data removed or masked, the requested output schema | Per request | Per agent step | The rule result is used and the case still routes | None within the step; the agent is called again on the next event | Enterprise AI | OpenAPI 3.1 | DL33 |
| INT-24 | Partner portal | Instructions to partners and the results they report | Both | Workbench screens through the external gateway | Instruction sent or result entered | Instruction type, case reference, documents, due date; result code, dates, amounts, fee | As entered | Per instruction | Show the error to the partner user and keep the entry | The user submits again | Partner and agency manager | OpenAPI 3.1 | DL03 |
| INT-25 | Debt buyers | Debt sale data tape for an awarded lot | Out | Batch: outbound file through the integration adapters | Lot awarded | BorrCode, OS By Acct, SellingPriceByAcct, account data agreed in the sale terms, personal data as the sale terms allow | Per lot | About 3,800 accounts a year across the lots | Hold the case step until the file is acknowledged | Send again; after the third failure raise a task to the owning team | Owning team, platform administrator | File specification | None |
| INT-34 | ACE common module | Shared case view, entities, restructure calculator, notification path | Both | Published module interface | Call or application event | As published by the common module | Per request | Per call | Return the error to the calling module | As the caller decides | ACE team | Module interface | DL14 |

## Field mapping

| Source field to Workbench field |  |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|
| 77 mappings from the field names in the source systems and bank files to the logical data model. |  |  |  |  |  |  |  |
| Interface | Source field | Entity | Field | Data type | Physical type | Mandatory | Transformation |
| INT-01 | ACCOUNT_KEY / iacct / AccNo | loan_account | account_no | TEXT | varchar(20) | Yes | Direct copy |
| INT-01 | ContractNo | loan_account | contract_no | TEXT | varchar(20) | No | Direct copy |
| INT-01 | acct_prd_cd | loan_account | product_code | LOV | varchar(10) | Yes | Direct copy |
| INT-01 | BU | loan_account | business_unit | LOV | varchar(10) | No | Direct copy |
| INT-01 | CONTRACT_DATE | loan_account | contract_date | DATE | date | No | Direct copy |
| INT-01 | INTEREST_RATE | loan_account | interest_rate | NUMBER | numeric(7,4) | No | Direct copy |
| INT-01 | Principal | loan_account | principal_outstanding | NUMBER | numeric(18,2) | Yes | Direct copy |
| INT-01 | AINT1 + AINT2 | loan_account | interest_outstanding | NUMBER | numeric(18,2) | Yes | AINT1 plus AINT2 |
| INT-01 | AFEE | loan_account | fees_outstanding | NUMBER | numeric(18,2) | Yes | Direct copy |
| INT-01 | TOTAL_BALANCE | loan_account | total_balance | NUMBER | numeric(18,2) | Yes | Direct copy |
| INT-01 | ACCOUNTING_BALANCE | loan_account | accounting_balance | NUMBER | numeric(18,2) | No | Direct copy |
| INT-01 | DELAY_DAYS | loan_account | days_past_due | NUMBER | integer | Yes | Direct copy |
| INT-01 | Bucket | loan_account | bucket | LOV | varchar(10) | No | Direct copy |
| INT-01 | LAST_PAYMENT_DATE | loan_account | last_payment_date | DATE | date | No | Direct copy |
| INT-01 | NEXT_INSTALLMENT_DATE | loan_account | next_installment_date | DATE | date | No | Direct copy |
| INT-01 | TDR list | loan_account | tdr_flag | BOOLEAN | boolean | Yes | Direct copy |
| INT-01 | Last_TDR_Date | loan_account | last_tdr_date | DATE | date | No | Direct copy |
| INT-01 | ms_data_dt | loan_account | data_as_of | DATE | date | Yes | Business date of the load |
| INT-02 | Payment_Code | account_payment | payment_code | TEXT | varchar(20) | Yes | Direct copy |
| INT-02 | Payment_Date | account_payment | payment_date | DATE | date | Yes | Direct copy |
| INT-02 | Payment_Amount | account_payment | payment_amount | NUMBER | numeric(18,2) | Yes | Direct copy |
| INT-02 | ms_data_dt | account_payment | data_as_of | DATE | date | Yes | Direct copy |
| INT-02 | Payment_Amount | proceeds | amount | NUMBER | numeric(18,2) | Yes | Direct copy |
| INT-02 | Payment_Date | proceeds | received_date | DATE | date | Yes | Direct copy |
| INT-04 | CIF | party | cif_no | TEXT | varchar(20) | Yes | Direct copy |
| INT-04 | Segment | party | segment | LOV | varchar(20) | No | Direct copy |
| INT-07 | Actioncode ID | interaction | action_code | LOV | varchar(10) | No | Direct copy |
| INT-07 | Call Result | interaction | contact_result | LOV | varchar(20) | No | Direct copy |
| INT-09 | LAWSUIT_NO / LAWSUIT_RUN | legal_action | lawsuit_no | TEXT | varchar(30) | No | Direct copy |
| INT-09 | เลขที่คดีดำ | legal_action | black_case_no | TEXT | varchar(30) | No | Direct copy |
| INT-09 | NCOURT | legal_action | court_name | TEXT | varchar(120) | No | Direct copy |
| INT-09 | AAMT_SUIT | legal_action | claim_amount | NUMBER | numeric(18,2) | No | Direct copy |
| INT-09 | Judgment date | legal_action | judgment_date | DATE | date | No | Direct copy |
| INT-10 | Title Deed / Ownership Doc | collateral | title_doc_no | TEXT | varchar(40) | No | Direct copy |
| INT-10 | Plot No. | collateral | plot_no | TEXT | varchar(20) | No | Direct copy |
| INT-10 | Area | collateral | area_text | TEXT | varchar(20) | No | Direct copy |
| INT-10 | Province | collateral | province | LOV | varchar(40) | No | Direct copy |
| INT-10 | District | collateral | district | TEXT | varchar(60) | No | Direct copy |
| INT-10 | Subdistrict | collateral | subdistrict | TEXT | varchar(60) | No | Direct copy |
| INT-10 | Insvalue | collateral | insured_value | NUMBER | numeric(18,2) | No | Direct copy |
| INT-11 | Appraisal No. | valuation | appraisal_no | TEXT | varchar(20) | Yes | Direct copy |
| INT-11 | Appraised Value | valuation | appraised_value | NUMBER | numeric(18,2) | Yes | Direct copy |
| INT-11 | Forced Sale Value | valuation | forced_sale_value | NUMBER | numeric(18,2) | No | Direct copy |
| INT-11 | Appraisal Date | valuation | appraisal_date | DATE | date | Yes | Direct copy |
| INT-12 | Asset ID | asset | asset_ref | TEXT | varchar(20) | Yes | Direct copy |
| INT-12 | Asset Code | asset | asset_code | TEXT | varchar(20) | No | Direct copy |
| INT-12 | Asset Type | asset | asset_type | LOV | varchar(20) | Yes | Direct copy |
| INT-12 | Transfer-in Type | asset | transfer_in_type | LOV | varchar(20) | Yes | Direct copy |
| INT-12 | From Segment | asset | from_segment | LOV | varchar(20) | No | Direct copy |
| INT-12 | Ownership Transfer in Date | asset | transfer_in_date | DATE | date | Yes | Direct copy |
| INT-12 | Book  Value | asset | book_value | NUMBER | numeric(18,2) | Yes | Direct copy |
| INT-12 | Auction Purchase Price | asset | auction_purchase_price | NUMBER | numeric(18,2) | No | Direct copy |
| INT-12 | Contract Date | asset_sale | contract_date | DATE | date | Yes | Direct copy |
| INT-12 | Sale Date | asset_sale | sale_date | DATE | date | Yes | Direct copy |
| INT-12 | Sale Price | asset_sale | sale_price | NUMBER | numeric(18,2) | Yes | Direct copy |
| INT-12 | Sale Transfer Fee | asset_sale | transfer_fee | NUMBER | numeric(18,2) | No | Direct copy |
| INT-12 | Specific Business Tax | asset_sale | specific_business_tax | NUMBER | numeric(18,2) | No | Direct copy |
| INT-12 | Corporate Income Tax | asset_sale | corporate_income_tax | NUMBER | numeric(18,2) | No | Direct copy |
| INT-12 | Incentive Amount | asset_sale | incentive_amount | NUMBER | numeric(18,2) | No | Direct copy |
| INT-13 | ReposessedCarDate | asset | repossessed_date | DATE | date | No | Thai year date YYMMDD converted to a Gregorian date |
| INT-13 | STOCK_DATE | asset | stock_date | DATE | date | No | Converted to a date |
| INT-14 | DDMMYYYY | notice | sent_date | DATE | date | No | Direct copy |
| INT-14 | Barcode | notice | barcode | TEXT | varchar(40) | No | Direct copy |
| INT-14 | DDMMYYYY_callBack | notice | callback_date | DATE | date | No | Direct copy |
| INT-14 | Sent Type | notice | sent_type | LOV | varchar(10) | No | Direct copy |
| INT-15 | DDMMYYYY | notice | sent_date | DATE | date | No | Direct copy |
| INT-15 | Barcode | notice | barcode | TEXT | varchar(40) | No | Direct copy |
| INT-15 | DDMMYYYY_callBack | notice | callback_date | DATE | date | No | Direct copy |
| INT-15 | Sent Type | notice | sent_type | LOV | varchar(10) | No | Direct copy |
| INT-16 | AMT | write_off | amount | NUMBER | numeric(18,2) | Yes | Direct copy |
| INT-16 | DATE | write_off | posted_date | DATE | date | No | Direct copy |
| INT-16 | RC | write_off | responsibility_center | TEXT | varchar(10) | No | Direct copy |
| INT-16 | OC | write_off | cost_center | TEXT | varchar(10) | No | Direct copy |
| INT-16 | PRODUCT | write_off | gl_product | TEXT | varchar(10) | No | Direct copy |
| INT-25 | BorrCode | debt_sale_account | borrower_code | TEXT | varchar(20) | No | Direct copy |
| INT-25 | OS By Acct | debt_sale_account | outstanding | NUMBER | numeric(18,2) | Yes | Direct copy |
| INT-25 | SellingPriceByAcct | debt_sale_account | selling_price | NUMBER | numeric(18,2) | No | Direct copy |

## Load checks

| Checks every inbound load passes |  |  |
|---|---|---|
| Applied to every COLLINS load and file load. |  |  |
| Check | What it tests | If it fails |
| Business date | The load is for the expected business date and is not a repeat | Refuse the load |
| Structure | Every expected field is present with the expected type and length | Refuse the load |
| Control totals | Record count and balance totals match the totals the source sends | Refuse the load |
| Keys | Every record has its key, and no key appears twice | Refuse the load |
| References | Each account, customer or asset is one the Workbench can match | Hold the record in the exception list and try it with the next load |
| Lists of values | Each coded value is in its list of values | Hold the record in the exception list |
| Movement | Changes against the previous load are within the expected range | Load, and alert the data steward |

## Key

| Key |  |  |
|---|---|---|
| What each term means. |  |  |
| Item | Term | Meaning |
| Approach | Batch | The COLLINS daily load or a file through the integration adapters |
| Standard | OpenAPI 3.1 | Request and response interfaces |
| Standard | AsyncAPI 3.0 | Event interfaces |
| Standard | File specification | Layout, control totals, business date and checks |
| Column | Owner of the fix | Who is told and acts when the interface fails |
