# Recovery Workbench interface specifications

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd

Each interface the Workbench builds or reads, with its approach, trigger, payload, frequency, volume, error handling, retry and owner. No component calls a system of record directly: data comes in through COLLINS or a file load, and leaves through paths ACE already has.

| ID | System | Direction | Approach | Frequency |
|---|---|---|---|---|
| INT-01 | Core bank (ALS) | In | Batch: COLLINS daily load into the ACE database | Daily, end of day |
| INT-02 | Core bank (ALS) | In | Batch: COLLINS daily load into the ACE database | Daily, end of day |
| INT-04 | SCBPDM | In | Batch: COLLINS daily load into the ACE database | Daily, end of day |
| INT-07 | EFS | In | Batch: COLLINS daily load into the ACE database | Daily, end of day |
| INT-08 | COLLINS models | In | Batch: COLLINS daily load into the ACE database | Daily; monthly for some models |
| INT-09 | LIT | In | Batch: COLLINS daily load into the ACE database | Daily, end of day |
| INT-10 | CCMS | In | Batch: file load through the integration adapters | Weekly |
| INT-11 | SVAF | In | Batch: file load through the integration adapters | Weekly |
| INT-12 | AMIS | In | Batch: file load through the integration adapters | Monthly |
| INT-13 | RPS | In | Batch: file load through the integration adapters | Weekly |
| INT-14 | WIN | Out | Batch: outbound file through the integration adapters | Daily |
| INT-15 | WIN | In | Batch: file load through the integration adapters | Weekly |
| INT-16 | GL | In | Batch: file load through the integration adapters | Monthly |
| INT-17 | NSS | Out | ACE notification path | As sent |
| INT-18 | LINE OA | Out | ACE notification path | As sent |
| INT-19 | Data lake and Power BI | Out | Daily batch | Daily |
| INT-20 | COLLINS | Out | Daily batch to the data lake | Daily |
| INT-21 | Entra ID and the bank IAM | In | ACE sign-in | At each sign-in |
| INT-22 | PII Kafka, audit and SOC logs | Out | ACE logging | As they happen |
| INT-23 | Enterprise AI model endpoint | Both | Private endpoint in the SCB tenant | Per request |
| INT-24 | Partner portal | Both | Workbench screens through the external gateway | As entered |
| INT-25 | Debt buyers | Out | Batch: outbound file through the integration adapters | Per lot |
| INT-34 | ACE common module | Both | Published module interface | Per request |

---

## INT-01 Core bank (ALS)

| Item | Specification |
|---|---|
| Purpose | Loan accounts, balances, arrears, days past due, classification |
| Direction | In |
| Approach | Batch: COLLINS daily load into the ACE database |
| Trigger | COLLINS load complete |
| Frequency | Daily, end of day |
| Volume | About 28,100 accounts in the active inventory and 156,400 further hire purchase accounts at 90 days past due or more, daily |
| Error handling | Refuse the load whole if the business date, structure, control totals or keys fail. Keep the previous load in use and mark the data product stale |
| Retry | Check each hour until the load window closes |
| Owner of the fix | Data steward, platform administrator |
| Standard | File specification |
| Decision | None |

**Payload**

ACCOUNT_KEY, CONTRACT_DATE, INTEREST_RATE, DELAY_DAYS, TOTAL_BALANCE, ACCOUNTING_BALANCE, Principal, AINT1, AINT2, AFEE, LAST_PAYMENT_DATE, NEXT_INSTALLMENT_DATE, Product_Category_Host, ms_data_dt.

**Field mapping**

| Source field | Entity | Field | Type | Mandatory | Transformation |
|---|---|---|---|---|---|
| ACCOUNT_KEY / iacct / AccNo | loan_account | account_no | varchar(20) | Yes | Direct copy |
| ContractNo | loan_account | contract_no | varchar(20) | No | Direct copy |
| acct_prd_cd | loan_account | product_code | varchar(10) | Yes | Direct copy |
| BU | loan_account | business_unit | varchar(10) | No | Direct copy |
| CONTRACT_DATE | loan_account | contract_date | date | No | Direct copy |
| INTEREST_RATE | loan_account | interest_rate | numeric(7,4) | No | Direct copy |
| Principal | loan_account | principal_outstanding | numeric(18,2) | Yes | Direct copy |
| AINT1 + AINT2 | loan_account | interest_outstanding | numeric(18,2) | Yes | AINT1 plus AINT2 |
| AFEE | loan_account | fees_outstanding | numeric(18,2) | Yes | Direct copy |
| TOTAL_BALANCE | loan_account | total_balance | numeric(18,2) | Yes | Direct copy |
| ACCOUNTING_BALANCE | loan_account | accounting_balance | numeric(18,2) | No | Direct copy |
| DELAY_DAYS | loan_account | days_past_due | integer | Yes | Direct copy |
| Bucket | loan_account | bucket | varchar(10) | No | Direct copy |
| LAST_PAYMENT_DATE | loan_account | last_payment_date | date | No | Direct copy |
| NEXT_INSTALLMENT_DATE | loan_account | next_installment_date | date | No | Direct copy |
| TDR list | loan_account | tdr_flag | boolean | Yes | Direct copy |
| Last_TDR_Date | loan_account | last_tdr_date | date | No | Direct copy |
| ms_data_dt | loan_account | data_as_of | date | Yes | Business date of the load |

---

## INT-02 Core bank (ALS)

| Item | Specification |
|---|---|
| Purpose | Payments posted to each account |
| Direction | In |
| Approach | Batch: COLLINS daily load into the ACE database |
| Trigger | COLLINS load complete |
| Frequency | Daily, end of day |
| Volume | Payments on recovery accounts each day |
| Error handling | Refuse the load whole if the business date, structure, control totals or keys fail. Keep the previous load in use and mark the data product stale |
| Retry | Check each hour until the load window closes |
| Owner of the fix | Data steward, platform administrator |
| Standard | File specification |
| Decision | None |

**Payload**

Payment_Code, hashed_account_key, Payment_Date, Payment_Amount, ms_data_dt.

**Field mapping**

| Source field | Entity | Field | Type | Mandatory | Transformation |
|---|---|---|---|---|---|
| Payment_Code | account_payment | payment_code | varchar(20) | Yes | Direct copy |
| Payment_Date | account_payment | payment_date | date | Yes | Direct copy |
| Payment_Amount | account_payment | payment_amount | numeric(18,2) | Yes | Direct copy |
| ms_data_dt | account_payment | data_as_of | date | Yes | Direct copy |
| Payment_Amount | proceeds | amount | numeric(18,2) | Yes | Direct copy |
| Payment_Date | proceeds | received_date | date | Yes | Direct copy |

---

## INT-04 SCBPDM

| Item | Specification |
|---|---|
| Purpose | Customer profile, identifiers and contact details |
| Direction | In |
| Approach | Batch: COLLINS daily load into the ACE database |
| Trigger | COLLINS load complete |
| Frequency | Daily, end of day |
| Volume | Every party on an open case, about 23,600 cases at go-live |
| Error handling | Refuse the load whole if the business date, structure, control totals or keys fail. Keep the previous load in use and mark the data product stale |
| Retry | Check each hour until the load window closes |
| Owner of the fix | Data steward, platform administrator |
| Standard | File specification |
| Decision | DL20 |

**Payload**

CIF, party type, name, identifier token, date of birth, segment, contact points with consent.

**Field mapping**

| Source field | Entity | Field | Type | Mandatory | Transformation |
|---|---|---|---|---|---|
| CIF | party | cif_no | varchar(20) | Yes | Direct copy |
| Segment | party | segment | varchar(20) | No | Direct copy |

---

## INT-07 EFS

| Item | Specification |
|---|---|
| Purpose | Collections history, action codes and promises before day 90 |
| Direction | In |
| Approach | Batch: COLLINS daily load into the ACE database |
| Trigger | COLLINS load complete |
| Frequency | Daily, end of day |
| Volume | History for about 3,110 new accounts a month at entry, then daily changes |
| Error handling | Refuse the load whole if the business date, structure, control totals or keys fail. Keep the previous load in use and mark the data product stale |
| Retry | Check each hour until the load window closes |
| Owner of the fix | Data steward, platform administrator |
| Standard | File specification |
| Decision | DL29 |

**Payload**

Actioncode ID, Description, Action Contact Status, Call Result, contact date, promise amount and date.

**Field mapping**

| Source field | Entity | Field | Type | Mandatory | Transformation |
|---|---|---|---|---|---|
| Actioncode ID | interaction | action_code | varchar(10) | No | Direct copy |
| Call Result | interaction | contact_result | varchar(20) | No | Direct copy |

---

## INT-08 COLLINS models

| Item | Specification |
|---|---|
| Purpose | Scores, return by route, price and sale success estimates, scheme suggestions |
| Direction | In |
| Approach | Batch: COLLINS daily load into the ACE database |
| Trigger | COLLINS load complete |
| Frequency | Daily; monthly for some models |
| Volume | One row per account and model each day |
| Error handling | Refuse the load whole if the business date, structure, control totals or keys fail. Keep the previous load in use and mark the data product stale |
| Retry | Check each hour until the load window closes |
| Owner of the fix | Data steward, platform administrator |
| Standard | File specification |
| Decision | None |

**Payload**

model code, model version, account key, score, estimate, route, score date.

---

## INT-09 LIT

| Item | Specification |
|---|---|
| Purpose | Litigation status and lawsuit numbers |
| Direction | In |
| Approach | Batch: COLLINS daily load into the ACE database |
| Trigger | COLLINS load complete |
| Frequency | Daily, end of day |
| Volume | About 670 lawsuits filed a month for Mortgage and SSME |
| Error handling | Refuse the load whole if the business date, structure, control totals or keys fail. Keep the previous load in use and mark the data product stale |
| Retry | Check each hour until the load window closes |
| Owner of the fix | Data steward, platform administrator |
| Standard | File specification |
| Decision | None |

**Payload**

iacct, LAWSUIT_NO, AAMT_SUIT, black case number, NCOURT, STATE_RES_NAME, Total_Pay.

**Field mapping**

| Source field | Entity | Field | Type | Mandatory | Transformation |
|---|---|---|---|---|---|
| LAWSUIT_NO / LAWSUIT_RUN | legal_action | lawsuit_no | varchar(30) | No | Direct copy |
| เลขที่คดีดำ | legal_action | black_case_no | varchar(30) | No | Direct copy |
| NCOURT | legal_action | court_name | varchar(120) | No | Direct copy |
| AAMT_SUIT | legal_action | claim_amount | numeric(18,2) | No | Direct copy |
| Judgment date | legal_action | judgment_date | date | No | Direct copy |

---

## INT-10 CCMS

| Item | Specification |
|---|---|
| Purpose | Collateral records |
| Direction | In |
| Approach | Batch: file load through the integration adapters |
| Trigger | File received by the weekly cut-off |
| Frequency | Weekly |
| Volume | Collateral on recovery accounts, weekly |
| Error handling | Refuse the file whole if a check fails. Hold records with an unknown reference in the exception list |
| Retry | Mark the data product stale one business day after the file was due; ask the sending team |
| Owner of the fix | Data steward, the sending team |
| Standard | File specification |
| Decision | DL06, DL12 |

**Payload**

Collateral number, type, title deed, plot, area, province, district, subdistrict, insured value, account links.

**Field mapping**

| Source field | Entity | Field | Type | Mandatory | Transformation |
|---|---|---|---|---|---|
| Title Deed / Ownership Doc | collateral | title_doc_no | varchar(40) | No | Direct copy |
| Plot No. | collateral | plot_no | varchar(20) | No | Direct copy |
| Area | collateral | area_text | varchar(20) | No | Direct copy |
| Province | collateral | province | varchar(40) | No | Direct copy |
| District | collateral | district | varchar(60) | No | Direct copy |
| Subdistrict | collateral | subdistrict | varchar(60) | No | Direct copy |
| Insvalue | collateral | insured_value | numeric(18,2) | No | Direct copy |

---

## INT-11 SVAF

| Item | Specification |
|---|---|
| Purpose | Appraisals |
| Direction | In |
| Approach | Batch: file load through the integration adapters |
| Trigger | File received by the weekly cut-off |
| Frequency | Weekly |
| Volume | New and changed appraisals, weekly |
| Error handling | Refuse the file whole if a check fails. Hold records with an unknown reference in the exception list |
| Retry | Mark the data product stale one business day after the file was due; ask the sending team |
| Owner of the fix | Data steward, the sending team |
| Standard | File specification |
| Decision | DL06, DL12 |

**Payload**

Appraisal No., Appraised Value, Forced Sale Value, Appraisal Date, collateral or asset reference, valuer.

**Field mapping**

| Source field | Entity | Field | Type | Mandatory | Transformation |
|---|---|---|---|---|---|
| Appraisal No. | valuation | appraisal_no | varchar(20) | Yes | Direct copy |
| Appraised Value | valuation | appraised_value | numeric(18,2) | Yes | Direct copy |
| Forced Sale Value | valuation | forced_sale_value | numeric(18,2) | No | Direct copy |
| Appraisal Date | valuation | appraisal_date | date | Yes | Direct copy |

---

## INT-12 AMIS

| Item | Specification |
|---|---|
| Purpose | Assets held, book values and asset sales |
| Direction | In |
| Approach | Batch: file load through the integration adapters |
| Trigger | File received by the monthly cut-off |
| Frequency | Monthly |
| Volume | About 4,700 properties held; about 30 sales a month |
| Error handling | Refuse the file whole if a check fails. Hold records with an unknown reference in the exception list |
| Retry | Mark the data product stale one business day after the file was due; ask the sending team |
| Owner of the fix | Data steward, the sending team |
| Standard | File specification |
| Decision | DL06, DL12 |

**Payload**

Asset ID, Asset Code, Transfer-in Type, Asset Type, Ownership Transfer in Date, Book Value, Auction Purchase Price, Sale Date, Sale Price, taxes and fees.

**Field mapping**

| Source field | Entity | Field | Type | Mandatory | Transformation |
|---|---|---|---|---|---|
| Asset ID | asset | asset_ref | varchar(20) | Yes | Direct copy |
| Asset Code | asset | asset_code | varchar(20) | No | Direct copy |
| Asset Type | asset | asset_type | varchar(20) | Yes | Direct copy |
| Transfer-in Type | asset | transfer_in_type | varchar(20) | Yes | Direct copy |
| From Segment | asset | from_segment | varchar(20) | No | Direct copy |
| Ownership Transfer in Date | asset | transfer_in_date | date | Yes | Direct copy |
| Book  Value | asset | book_value | numeric(18,2) | Yes | Direct copy |
| Auction Purchase Price | asset | auction_purchase_price | numeric(18,2) | No | Direct copy |
| Contract Date | asset_sale | contract_date | date | Yes | Direct copy |
| Sale Date | asset_sale | sale_date | date | Yes | Direct copy |
| Sale Price | asset_sale | sale_price | numeric(18,2) | Yes | Direct copy |
| Sale Transfer Fee | asset_sale | transfer_fee | numeric(18,2) | No | Direct copy |
| Specific Business Tax | asset_sale | specific_business_tax | numeric(18,2) | No | Direct copy |
| Corporate Income Tax | asset_sale | corporate_income_tax | numeric(18,2) | No | Direct copy |
| Incentive Amount | asset_sale | incentive_amount | numeric(18,2) | No | Direct copy |

---

## INT-13 RPS

| Item | Specification |
|---|---|
| Purpose | Repossessed vehicles and stock |
| Direction | In |
| Approach | Batch: file load through the integration adapters |
| Trigger | File received by the weekly cut-off |
| Frequency | Weekly |
| Volume | About 720 vehicles repossessed a month |
| Error handling | Refuse the file whole if a check fails. Hold records with an unknown reference in the exception list |
| Retry | Mark the data product stale one business day after the file was due; ask the sending team |
| Owner of the fix | Data steward, the sending team |
| Standard | File specification |
| Decision | DL06, DL12 |

**Payload**

AccNo, ContractNo, RepoDT, ReposessedCarDate, VehicleStatus, STOCK_DATE, OutBal.

**Field mapping**

| Source field | Entity | Field | Type | Mandatory | Transformation |
|---|---|---|---|---|---|
| ReposessedCarDate | asset | repossessed_date | date | No | Thai year date YYMMDD converted to a Gregorian date |
| STOCK_DATE | asset | stock_date | date | No | Converted to a date |

---

## INT-14 WIN

| Item | Specification |
|---|---|
| Purpose | Demand, recall and sale notices for registered mail |
| Direction | Out |
| Approach | Batch: outbound file through the integration adapters |
| Trigger | Notice approved and generated |
| Frequency | Daily |
| Volume | About 1,900 registered letters a month |
| Error handling | Hold the case step until the file is acknowledged |
| Retry | Send again; after the third failure raise a task to the owning team |
| Owner of the fix | Owning team, platform administrator |
| Standard | File specification |
| Decision | None |

**Payload**

ContractNO, addressee, address, notice type, template version, document reference.

**Field mapping**

| Source field | Entity | Field | Type | Mandatory | Transformation |
|---|---|---|---|---|---|
| DDMMYYYY | notice | sent_date | date | No | Direct copy |
| Barcode | notice | barcode | varchar(40) | No | Direct copy |
| DDMMYYYY_callBack | notice | callback_date | date | No | Direct copy |
| Sent Type | notice | sent_type | varchar(10) | No | Direct copy |

---

## INT-15 WIN

| Item | Specification |
|---|---|
| Purpose | Proof of delivery for registered mail |
| Direction | In |
| Approach | Batch: file load through the integration adapters |
| Trigger | File received by the weekly cut-off |
| Frequency | Weekly |
| Volume | About 1,900 proofs of delivery a month |
| Error handling | Refuse the file whole if a check fails. Hold records with an unknown reference in the exception list |
| Retry | Mark the data product stale one business day after the file was due; ask the sending team |
| Owner of the fix | Data steward, the sending team |
| Standard | File specification |
| Decision | None |

**Payload**

DDMMYYYY, ContractNO, Barcode, DDMMYYYY_callBack, Sent Type.

**Field mapping**

| Source field | Entity | Field | Type | Mandatory | Transformation |
|---|---|---|---|---|---|
| DDMMYYYY | notice | sent_date | date | No | Direct copy |
| Barcode | notice | barcode | varchar(40) | No | Direct copy |
| DDMMYYYY_callBack | notice | callback_date | date | No | Direct copy |
| Sent Type | notice | sent_type | varchar(10) | No | Direct copy |

---

## INT-16 GL

| Item | Specification |
|---|---|
| Purpose | Write-off postings |
| Direction | In |
| Approach | Batch: file load through the integration adapters |
| Trigger | File received by the monthly cut-off |
| Frequency | Monthly |
| Volume | Write-off postings each month |
| Error handling | Refuse the file whole if a check fails. Hold records with an unknown reference in the exception list |
| Retry | Mark the data product stale one business day after the file was due; ask the sending team |
| Owner of the fix | Data steward, the sending team |
| Standard | File specification |
| Decision | DL12 |

**Payload**

DATE, RC, OC, ACCOUNT, PRODUCT, EVENT, AMT.

**Field mapping**

| Source field | Entity | Field | Type | Mandatory | Transformation |
|---|---|---|---|---|---|
| AMT | write_off | amount | numeric(18,2) | Yes | Direct copy |
| DATE | write_off | posted_date | date | No | Direct copy |
| RC | write_off | responsibility_center | varchar(10) | No | Direct copy |
| OC | write_off | cost_center | varchar(10) | No | Direct copy |
| PRODUCT | write_off | gl_product | varchar(10) | No | Direct copy |

---

## INT-17 NSS

| Item | Specification |
|---|---|
| Purpose | SMS to customers |
| Direction | Out |
| Approach | ACE notification path |
| Trigger | Message approved by the contact rules |
| Frequency | As sent |
| Volume | Messages per day |
| Error handling | Record the failure on the interaction ledger |
| Retry | As the ACE notification path retries |
| Owner of the fix | ACE team |
| Standard | Common module interface |
| Decision | DL30 |

**Payload**

contact point, template, language, case reference.

---

## INT-18 LINE OA

| Item | Specification |
|---|---|
| Purpose | LINE messages to customers |
| Direction | Out |
| Approach | ACE notification path |
| Trigger | Message approved by the contact rules |
| Frequency | As sent |
| Volume | Messages per day |
| Error handling | Record the failure on the interaction ledger |
| Retry | As the ACE notification path retries |
| Owner of the fix | ACE team |
| Standard | Common module interface |
| Decision | DL30 |

**Payload**

LINE identifier, template, language, case reference.

---

## INT-19 Data lake and Power BI

| Item | Specification |
|---|---|
| Purpose | Case, queue, decision and outcome data for reporting |
| Direction | Out |
| Approach | Daily batch |
| Trigger | Nightly |
| Frequency | Daily |
| Volume | All changes in the day |
| Error handling | Hold the publish and raise an alert |
| Retry | Run again in the next window |
| Owner of the fix | Platform administrator |
| Standard | File specification |
| Decision | None |

**Payload**

Case, queue, task, timer, decision log and outcome records changed that day.

---

## INT-20 COLLINS

| Item | Specification |
|---|---|
| Purpose | Decisions and outcomes for model learning |
| Direction | Out |
| Approach | Daily batch to the data lake |
| Trigger | Nightly |
| Frequency | Daily |
| Volume | All decisions in the day |
| Error handling | Hold the publish and raise an alert |
| Retry | Run again in the next window |
| Owner of the fix | Platform administrator |
| Standard | File specification |
| Decision | None |

**Payload**

Decision log entries and outcomes changed that day.

---

## INT-21 Entra ID and the bank IAM

| Item | Specification |
|---|---|
| Purpose | Sign-in and the roles each user holds |
| Direction | In |
| Approach | ACE sign-in |
| Trigger | Sign-in |
| Frequency | At each sign-in |
| Volume | Every sign-in |
| Error handling | Refuse the session and log it |
| Retry | None |
| Owner of the fix | Security administrator |
| Standard | OpenID Connect |
| Decision | DL40 |

**Payload**

User identity and Entra ID group membership.

---

## INT-22 PII Kafka, audit and SOC logs

| Item | Specification |
|---|---|
| Purpose | Personal data access, audit and security events |
| Direction | Out |
| Approach | ACE logging |
| Trigger | Each event |
| Frequency | As they happen |
| Volume | Every read of personal data and every security event |
| Error handling | As the ACE logging service |
| Retry | As the ACE logging service |
| Owner of the fix | ACE team |
| Standard | AsyncAPI 3.0 |
| Decision | None |

**Payload**

Who, what, when, which record, which fields.

---

## INT-23 Enterprise AI model endpoint

| Item | Specification |
|---|---|
| Purpose | The model the agents call |
| Direction | Both |
| Approach | Private endpoint in the SCB tenant |
| Trigger | An agent step |
| Frequency | Per request |
| Volume | Per agent step |
| Error handling | The rule result is used and the case still routes |
| Retry | None within the step; the agent is called again on the next event |
| Owner of the fix | Enterprise AI |
| Standard | OpenAPI 3.1 |
| Decision | DL33 |

**Payload**

Prompt version, inputs with personal data removed or masked, the requested output schema.

---

## INT-24 Partner portal

| Item | Specification |
|---|---|
| Purpose | Instructions to partners and the results they report |
| Direction | Both |
| Approach | Workbench screens through the external gateway |
| Trigger | Instruction sent or result entered |
| Frequency | As entered |
| Volume | Per instruction |
| Error handling | Show the error to the partner user and keep the entry |
| Retry | The user submits again |
| Owner of the fix | Partner and agency manager |
| Standard | OpenAPI 3.1 |
| Decision | DL03 |

**Payload**

Instruction type, case reference, documents, due date; result code, dates, amounts, fee.

---

## INT-25 Debt buyers

| Item | Specification |
|---|---|
| Purpose | Debt sale data tape for an awarded lot |
| Direction | Out |
| Approach | Batch: outbound file through the integration adapters |
| Trigger | Lot awarded |
| Frequency | Per lot |
| Volume | About 3,800 accounts a year across the lots |
| Error handling | Hold the case step until the file is acknowledged |
| Retry | Send again; after the third failure raise a task to the owning team |
| Owner of the fix | Owning team, platform administrator |
| Standard | File specification |
| Decision | None |

**Payload**

BorrCode, OS By Acct, SellingPriceByAcct, account data agreed in the sale terms, personal data as the sale terms allow.

**Field mapping**

| Source field | Entity | Field | Type | Mandatory | Transformation |
|---|---|---|---|---|---|
| BorrCode | debt_sale_account | borrower_code | varchar(20) | No | Direct copy |
| OS By Acct | debt_sale_account | outstanding | numeric(18,2) | Yes | Direct copy |
| SellingPriceByAcct | debt_sale_account | selling_price | numeric(18,2) | No | Direct copy |

---

## INT-34 ACE common module

| Item | Specification |
|---|---|
| Purpose | Shared case view, entities, restructure calculator, notification path |
| Direction | Both |
| Approach | Published module interface |
| Trigger | Call or application event |
| Frequency | Per request |
| Volume | Per call |
| Error handling | Return the error to the calling module |
| Retry | As the caller decides |
| Owner of the fix | ACE team |
| Standard | Module interface |
| Decision | DL14 |

**Payload**

As published by the common module.

---

## Checks every inbound load passes

| Check | What it tests | If it fails |
|---|---|---|
| Business date | The load is for the expected business date and is not a repeat | Refuse the load |
| Structure | Every expected field is present with the expected type and length | Refuse the load |
| Control totals | Record count and balance totals match the totals the source sends | Refuse the load |
| Keys | Every record has its key, and no key appears twice | Refuse the load |
| References | Each account, customer or asset is one the Workbench can match | Hold the record in the exception list and try it with the next load |
| Lists of values | Each coded value is in its list of values | Hold the record in the exception list |
| Movement | Changes against the previous load are within the expected range | Load, and alert the data steward |
