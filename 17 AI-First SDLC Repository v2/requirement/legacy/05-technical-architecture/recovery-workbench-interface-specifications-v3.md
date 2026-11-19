<!-- source: 05 Technical architecture/Recovery Workbench Interface Specifications v3.md -->
<!-- converted: 2026-11-16 from Markdown (copied) -->

> **Source:** `05 Technical architecture/Recovery Workbench Interface Specifications v3.md`  
> **Converted from:** Markdown (copied)

# Recovery Workbench interface specifications

SCB Collections and Recovery. Henka Group, 15 November 2026.

(C) Siam Commercial Bank and Henka Pte Ltd

## Document control

| Attribute | Value |
|---|---|
| Document title | Recovery Workbench interface specifications |
| Version | 3 |
| Status | In review |
| Date | 15 November 2026 |
| Owner | Solution architect |
| Decision | D-RCV-35 |
| Supersedes | Recovery Workbench Interface Specifications v2 |

The Workbench loads no source data. ACE ingests every inbound source named here, and the recovery module reads the result through the read-only `recovery.v_ace_*` views. The inbound field maps below are the ACE ingestion specification: they say what ACE must deliver for the Workbench read path, not what the Workbench copies. The ACE team owns the inbound interfaces and the tables behind them, raised once in RWB-ACE-001. The Workbench owns the outbound interfaces and the case.

No component calls a system of record directly. Data arrives in ACE through ACE's own ingestion, the Workbench reads it through 30 `recovery.v_ace_*` views, and outbound data leaves through the paths ACE already has. There is no inbound run, sign-off or data quality gate inside the Workbench; those move to the ACE ingestion story.

| ID | System | Direction | Owner | Approach | Frequency |
|---|---|---|---|---|---|
| INT-01 | Core bank (ALS) | In, into ACE | ACE team | ACE ingestion, read through `v_ace_account` | Daily, end of day |
| INT-02 | Core bank (ALS) | In, into ACE | ACE team | ACE ingestion, read through `v_ace_payment` | Daily, end of day |
| INT-04 | SCBPDM | In, into ACE | ACE team | ACE ingestion, read through `v_ace_customer` and `v_ace_contact` | Daily, end of day |
| INT-07 | EFS | In, into ACE | ACE team | ACE ingestion, read through `v_ace_efs_action` | Daily, end of day |
| INT-08 | COLLINS models | In, into ACE | ACE team | ACE ingestion, read through `v_ace_score` | Daily; monthly for some models |
| INT-09 | LIT | In, into ACE | ACE team | ACE ingestion, read through `v_ace_lawsuit` and `v_ace_hearing` | Daily, end of day |
| INT-10 | CCMS | In, into ACE | ACE team | ACE ingestion, read through `v_ace_collateral` and `v_ace_collateral_detail` | Weekly |
| INT-11 | SVAF | In, into ACE | ACE team | ACE ingestion, read through `v_ace_valuation` | Weekly |
| INT-12 | AMIS | In, into ACE | ACE team | ACE ingestion, read through `v_ace_asset`, `v_ace_npa_asset` and `v_ace_npa_sale` | Monthly |
| INT-13 | RPS | In, into ACE | ACE team | ACE ingestion, read through `v_ace_npa_asset` | Weekly |
| INT-14 | WIN | Out | Workbench | Batch: outbound file through the integration adapters | Daily |
| INT-15 | WIN | In, into ACE | ACE team | ACE ingestion, read through `v_ace_pod` | Weekly |
| INT-16 | GL | In, into ACE | ACE team | ACE ingestion, read through `v_ace_write_off` | Monthly |
| INT-17 | NSS | Out | ACE team | ACE notification path | As sent |
| INT-18 | LINE OA | Out | ACE team | ACE notification path | As sent |
| INT-19 | Data lake and Power BI | Out | Workbench | Daily batch | Daily |
| INT-20 | COLLINS | Out | Workbench | Daily batch to the data lake | Daily |
| INT-21 | Entra ID and the bank IAM | In | ACE team | ACE sign-in; group-to-role mapping read through `v_ace_iam_group` | At each sign-in |
| INT-22 | PII Kafka, audit and SOC logs | Out | ACE team | ACE logging | As they happen |
| INT-23 | Enterprise AI model endpoint | Both | Bank platform | Private endpoint in the SCB tenant | Per request |
| INT-24 | Partner portal | Both | Workbench | Workbench screens through the external gateway | As entered |
| INT-25 | Debt buyers | Out | Workbench | Batch: outbound file through the integration adapters | Per lot |
| INT-34 | ACE common module | Both | ACE team | Published module interface | Per request |
| INT-35 | NLEADS | In, into ACE | ACE team | ACE ingestion, read through `v_ace_credit_decision` | As decisions are made |
| INT-36 | EasyApp | In, into ACE | ACE team | ACE ingestion, read through `v_ace_esign` | As signatures are requested |

---

## INT-01 Core bank (ALS)

| Item | Specification |
|---|---|
| Purpose | Loan accounts, balances, arrears, days past due, classification |
| Direction | In, into ACE |
| Approach | ACE ingestion, read through `v_ace_account` |
| ACE object | `account`, plus 7 new columns (RWB-ACE-001) |
| Trigger | ACE batch complete for ALS (`v_ace_batch_status`) |
| Frequency | Daily, end of day |
| Volume | About 28,100 accounts in the active inventory and 156,400 further hire purchase accounts at 90 days past due or more, daily |
| Error handling | ACE ingestion refuses the feed whole if the business date, structure, control totals or keys fail. The Workbench reads the last complete business date from `v_ace_batch_status` and marks the data product stale |
| Retry | ACE ingestion retries on its own schedule; the Workbench raises AceDataLate when the business date is not complete at its cut-off |
| Owner of the fix | ACE team |
| Standard | File specification |
| Decision | None |

**Payload**

ACCOUNT_KEY, CONTRACT_DATE, INTEREST_RATE, DELAY_DAYS, TOTAL_BALANCE, ACCOUNTING_BALANCE, Principal, AINT1, AINT2, AFEE, LAST_PAYMENT_DATE, NEXT_INSTALLMENT_DATE, Product_Category_Host, ms_data_dt.

**Field mapping**

Table.column is the ACE column that holds the value: Tier 1 exists in ACE today, Tier 2 is added by the ACE team in RWB-ACE-001. Read path is the `recovery.v_ace_*` view column the Workbench reads. LDM field is the LDM v7 field ID; the mapping follows the LDM v7 ACE mapping sheet.

| Source field | Table.column | Tier | Read path | LDM field | Type | Mandatory | Transformation |
|---|---|---|---|---|---|---|---|
| ACCOUNT_KEY / iacct / AccNo | `account.account_key` | Tier 1 | `v_ace_account.account_no` | DF-ACC-002 | varchar(20) | Yes | Direct copy; ACE business key |
| ContractNo | `account.contract_number` | Tier 1 | `v_ace_account.contract_no` | DF-ACC-003 | varchar(20) | No | Direct copy |
| acct_prd_cd | `product.product_key` | Tier 1 | `v_ace_account.product_code` | DF-ACC-004 | varchar(10) | Yes | Direct copy |
| BU | `account.business_unit` | Tier 2 | `v_ace_account.business_unit` | DF-ACC-006 | varchar(10) | No | Direct copy |
| CONTRACT_DATE | `account.contract_date` | Tier 1 | `v_ace_account.contract_date` | DF-ACC-007 | date | No | Direct copy |
| INTEREST_RATE | `account.interest_rate` | Tier 1 | `v_ace_account.interest_rate` | DF-ACC-008 | numeric(7,4) | No | Direct copy; the view casts numeric(38,2) to numeric(7,4) |
| Principal | `account.principal_outstanding` | Tier 2 | `v_ace_account.principal_outstanding` | DF-ACC-009 | numeric(18,2) | Yes | Direct copy |
| AINT1 + AINT2 | `account.interest_outstanding` | Tier 2 | `v_ace_account.interest_outstanding` | DF-ACC-010 | numeric(18,2) | Yes | AINT1 plus AINT2 |
| AFEE | `account.fees_outstanding` | Tier 2 | `v_ace_account.fees_outstanding` | DF-ACC-011 | numeric(18,2) | Yes | Direct copy |
| TOTAL_BALANCE | `account.total_balance` | Tier 1 | `v_ace_account.total_balance` | DF-ACC-012 | numeric(18,2) | Yes | Direct copy |
| ACCOUNTING_BALANCE | `account.accounting_balance` | Tier 1 | `v_ace_account.accounting_balance` | DF-ACC-013 | numeric(18,2) | No | Direct copy |
| DELAY_DAYS | `account.delay_days` | Tier 1 | `v_ace_account.days_past_due` | DF-ACC-014 | integer | Yes | Direct copy; renamed days_past_due in the view |
| Bucket | `account.daily_bucket` | Tier 2 | `v_ace_account.bucket` | DF-ACC-015 | varchar(10) | No | Direct copy; daily bucket (bucket_log_snapshot is monthly) |
| LAST_PAYMENT_DATE | `account.last_payment_date` | Tier 1 | `v_ace_account.last_payment_date` | DF-ACC-017 | date | No | Direct copy |
| NEXT_INSTALLMENT_DATE | `account.next_installment_date` | Tier 1 | `v_ace_account.next_installment_date` | DF-ACC-018 | date | No | Direct copy |
| TDR list | `account.is_restructured` | Tier 1 | `v_ace_account.tdr_flag` | DF-ACC-019 | boolean | Yes | Y/N text cast to boolean by recovery.ace_to_boolean in the view |
| Last_TDR_Date | `account.last_tdr_date` | Tier 1 | `v_ace_account.last_tdr_date` | DF-ACC-020 | date | No | Direct copy |
| ms_data_dt | `account.core_banking_system_date` | Tier 1 | `v_ace_account.data_as_of` | DF-ACC-021 | date | Yes | Business date of the ACE batch |

---

## INT-02 Core bank (ALS)

| Item | Specification |
|---|---|
| Purpose | Payments posted to each account |
| Direction | In, into ACE |
| Approach | ACE ingestion, read through `v_ace_payment` |
| ACE object | `payment` |
| Trigger | ACE batch complete for ALS (`v_ace_batch_status`) |
| Frequency | Daily, end of day |
| Volume | Payments on recovery accounts each day |
| Error handling | ACE ingestion refuses the feed whole if the business date, structure, control totals or keys fail. The Workbench reads the last complete business date from `v_ace_batch_status` and marks the data product stale |
| Retry | ACE ingestion retries on its own schedule; the Workbench raises AceDataLate when the business date is not complete at its cut-off |
| Owner of the fix | ACE team |
| Standard | File specification |
| Decision | None |

**Payload**

Payment_Code, hashed_account_key, Payment_Date, Payment_Amount, ms_data_dt.

**Field mapping**

Table.column is the ACE column that holds the value: Tier 1 exists in ACE today, Tier 2 is added by the ACE team in RWB-ACE-001. Read path is the `recovery.v_ace_*` view column the Workbench reads. LDM field is the LDM v7 field ID; the mapping follows the LDM v7 ACE mapping sheet.

| Source field | Table.column | Tier | Read path | LDM field | Type | Mandatory | Transformation |
|---|---|---|---|---|---|---|---|
| Payment_Code | `payment.pay_key` | Tier 1 | `v_ace_payment.payment_code` | DF-ACC-024 | varchar(20) | Yes | Direct copy; ACE business key |
| Payment_Date | `payment.pay_date` | Tier 1 | `v_ace_payment.payment_date` | DF-ACC-025 | date | Yes | varchar cast to date by recovery.ace_to_date in the view |
| Payment_Amount | `payment.total_amount` | Tier 1 | `v_ace_payment.payment_amount` | DF-ACC-026 | numeric(18,2) | Yes | Direct copy |
| ms_data_dt | `account.core_banking_system_date` | Tier 1 | `v_ace_payment.data_as_of` | DF-ACC-028 | date | Yes | Read from the account batch date; no new payment column |
| Payment_Amount | `payment.total_amount` | Tier 1 | `v_ace_payment.payment_amount` | DF-FIN-006 | numeric(18,2) | Yes | Direct copy |
| Payment_Date | `payment.pay_date` | Tier 1 | `v_ace_payment.payment_date` | DF-FIN-007 | date | Yes | varchar cast to date by recovery.ace_to_date in the view |

---

## INT-04 SCBPDM

| Item | Specification |
|---|---|
| Purpose | Customer profile, identifiers and contact details |
| Direction | In, into ACE |
| Approach | ACE ingestion, read through `v_ace_customer` and `v_ace_contact` |
| ACE object | `customer`, plus 3 new columns (RWB-ACE-001); `phone`, `email` and `address` |
| Trigger | ACE batch complete for SCBPDM (`v_ace_batch_status`) |
| Frequency | Daily, end of day |
| Volume | Every party on an open case, about 23,600 cases at go-live |
| Error handling | ACE ingestion refuses the feed whole if the business date, structure, control totals or keys fail. The Workbench reads the last complete business date from `v_ace_batch_status` and marks the data product stale |
| Retry | ACE ingestion retries on its own schedule; the Workbench raises AceDataLate when the business date is not complete at its cut-off |
| Owner of the fix | ACE team |
| Standard | File specification |
| Decision | DL20 |

**Payload**

CIF, party type, name, identifier token, date of birth, segment, contact points with consent.

**Field mapping**

Table.column is the ACE column that holds the value: Tier 1 exists in ACE today, Tier 2 is added by the ACE team in RWB-ACE-001. Read path is the `recovery.v_ace_*` view column the Workbench reads. LDM field is the LDM v7 field ID; the mapping follows the LDM v7 ACE mapping sheet.

| Source field | Table.column | Tier | Read path | LDM field | Type | Mandatory | Transformation |
|---|---|---|---|---|---|---|---|
| CIF | `customer.person_key` | Tier 1 | `v_ace_customer.cif_no` | DF-PTY-002 | varchar(20) | Yes | Direct copy; ACE business key |
| Segment | `customer.segment` | Tier 2 | `v_ace_customer.segment` | DF-PTY-009 | varchar(20) | No | Direct copy |

---

## INT-07 EFS

| Item | Specification |
|---|---|
| Purpose | Collections history, action codes and promises before day 90 |
| Direction | In, into ACE |
| Approach | ACE ingestion, read through `v_ace_efs_action` |
| ACE object | `efs_action`, plus 2 new columns (RWB-ACE-001) |
| Trigger | ACE batch complete for EFS (`v_ace_batch_status`) |
| Frequency | Daily, end of day |
| Volume | History for about 3,110 new accounts a month at entry, then daily changes |
| Error handling | ACE ingestion refuses the feed whole if the business date, structure, control totals or keys fail. The Workbench reads the last complete business date from `v_ace_batch_status` and marks the data product stale |
| Retry | ACE ingestion retries on its own schedule; the Workbench raises AceDataLate when the business date is not complete at its cut-off |
| Owner of the fix | ACE team |
| Standard | File specification |
| Decision | DL29 |

**Payload**

Actioncode ID, Description, Action Contact Status, Call Result, contact date, promise amount and date.

**Field mapping**

Table.column is the ACE column that holds the value: Tier 1 exists in ACE today, Tier 2 is added by the ACE team in RWB-ACE-001. Read path is the `recovery.v_ace_*` view column the Workbench reads. LDM field is the LDM v7 field ID; the mapping follows the LDM v7 ACE mapping sheet.

| Source field | Table.column | Tier | Read path | LDM field | Type | Mandatory | Transformation |
|---|---|---|---|---|---|---|---|
| Actioncode ID | `efs_action.action_code` | Tier 1 | `v_ace_efs_action.action_code` | DF-INT-007 | varchar(10) | No | Direct copy |
| Call Result | `efs_action.contact_result` | Tier 2 | `v_ace_efs_action.contact_result` | DF-INT-008 | varchar(20) | No | Direct copy |

---

## INT-08 COLLINS models

| Item | Specification |
|---|---|
| Purpose | Scores, return by route, price and sale success estimates, scheme suggestions |
| Direction | In, into ACE |
| Approach | ACE ingestion, read through `v_ace_score` |
| ACE object | `collins_score` (new table) |
| Trigger | ACE batch complete for COLLINS (`v_ace_batch_status`) |
| Frequency | Daily; monthly for some models |
| Volume | One row per account and model each day |
| Error handling | ACE ingestion refuses the feed whole if the business date, structure, control totals or keys fail. The Workbench reads the last complete business date from `v_ace_batch_status` and marks the data product stale |
| Retry | ACE ingestion retries on its own schedule; the Workbench raises AceDataLate when the business date is not complete at its cut-off |
| Owner of the fix | ACE team |
| Standard | File specification |
| Decision | None |

**Payload**

model code, model version, account key, score, estimate, route, score date.

---

## INT-09 LIT

| Item | Specification |
|---|---|
| Purpose | Litigation status and lawsuit numbers |
| Direction | In, into ACE |
| Approach | ACE ingestion, read through `v_ace_lawsuit` and `v_ace_hearing` |
| ACE object | `lawsuit` and `hearing` (new tables) |
| Trigger | ACE batch complete for LIT (`v_ace_batch_status`) |
| Frequency | Daily, end of day |
| Volume | About 670 lawsuits filed a month for Mortgage and SSME |
| Error handling | ACE ingestion refuses the feed whole if the business date, structure, control totals or keys fail. The Workbench reads the last complete business date from `v_ace_batch_status` and marks the data product stale |
| Retry | ACE ingestion retries on its own schedule; the Workbench raises AceDataLate when the business date is not complete at its cut-off |
| Owner of the fix | ACE team |
| Standard | File specification |
| Decision | None |

**Payload**

iacct, LAWSUIT_NO, AAMT_SUIT, black case number, NCOURT, STATE_RES_NAME, Total_Pay.

**Field mapping**

Table.column is the ACE column that holds the value: Tier 1 exists in ACE today, Tier 2 is added by the ACE team in RWB-ACE-001. Read path is the `recovery.v_ace_*` view column the Workbench reads. LDM field is the LDM v7 field ID; the mapping follows the LDM v7 ACE mapping sheet.

| Source field | Table.column | Tier | Read path | LDM field | Type | Mandatory | Transformation |
|---|---|---|---|---|---|---|---|
| LAWSUIT_NO / LAWSUIT_RUN | `lawsuit.lawsuit_no` | Tier 2 | `v_ace_lawsuit.lawsuit_no` | DF-LEG-005 | varchar(30) | No | Direct copy |
| เลขที่คดีดำ | `lawsuit.black_case_no` | Tier 2 | `v_ace_lawsuit.black_case_no` | DF-LEG-006 | varchar(30) | No | Direct copy |
| NCOURT | `lawsuit.court_name` | Tier 2 | `v_ace_lawsuit.court_name` | DF-LEG-008 | varchar(120) | No | Direct copy |
| AAMT_SUIT | `lawsuit.claim_amount` | Tier 2 | `v_ace_lawsuit.claim_amount` | DF-LEG-009 | numeric(18,2) | No | Direct copy |
| Judgment date | `lawsuit.judgment_date` | Tier 2 | `v_ace_lawsuit.judgment_date` | DF-LEG-011 | date | No | Direct copy |

---

## INT-10 CCMS

| Item | Specification |
|---|---|
| Purpose | Collateral records |
| Direction | In, into ACE |
| Approach | ACE ingestion, read through `v_ace_collateral` and `v_ace_collateral_detail` |
| ACE object | `collateral` and `collateral_detail` (new table) |
| Trigger | ACE batch complete for CCMS (`v_ace_batch_status`) |
| Frequency | Weekly |
| Volume | Collateral on recovery accounts, weekly |
| Error handling | ACE ingestion refuses the feed whole if a check fails. The Workbench reads the last complete business date from `v_ace_batch_status` and marks the data product stale |
| Retry | ACE ingestion retries on its own schedule; the Workbench raises AceDataLate when the business date is not complete at its cut-off |
| Owner of the fix | ACE team |
| Standard | File specification |
| Decision | DL06, DL12 |

**Payload**

Collateral number, type, title deed, plot, area, province, district, subdistrict, insured value, account links.

**Field mapping**

Table.column is the ACE column that holds the value: Tier 1 exists in ACE today, Tier 2 is added by the ACE team in RWB-ACE-001. Read path is the `recovery.v_ace_*` view column the Workbench reads. LDM field is the LDM v7 field ID; the mapping follows the LDM v7 ACE mapping sheet.

| Source field | Table.column | Tier | Read path | LDM field | Type | Mandatory | Transformation |
|---|---|---|---|---|---|---|---|
| Title Deed / Ownership Doc | `collateral_detail.title_doc_no` | Tier 2 | `v_ace_collateral_detail.title_doc_no` | DF-COL-004 | varchar(40) | No | Direct copy |
| Plot No. | `collateral_detail.plot_no` | Tier 2 | `v_ace_collateral_detail.plot_no` | DF-COL-005 | varchar(20) | No | Direct copy |
| Area | `collateral_detail.area_text` | Tier 2 | `v_ace_collateral_detail.area_text` | DF-COL-006 | varchar(20) | No | Direct copy |
| Province | `collateral_detail.province` | Tier 2 | `v_ace_collateral_detail.province` | DF-COL-007 | varchar(40) | No | Direct copy |
| District | `collateral_detail.district` | Tier 2 | `v_ace_collateral_detail.district` | DF-COL-008 | varchar(60) | No | Direct copy |
| Subdistrict | `collateral_detail.subdistrict` | Tier 2 | `v_ace_collateral_detail.subdistrict` | DF-COL-009 | varchar(60) | No | Direct copy |
| Insvalue | `collateral_detail.insured_value` | Tier 2 | `v_ace_collateral_detail.insured_value` | DF-COL-012 | numeric(18,2) | No | Direct copy |

---

## INT-11 SVAF

| Item | Specification |
|---|---|
| Purpose | Appraisals |
| Direction | In, into ACE |
| Approach | ACE ingestion, read through `v_ace_valuation` |
| ACE object | `valuation` (new table) |
| Trigger | ACE batch complete for SVAF (`v_ace_batch_status`) |
| Frequency | Weekly |
| Volume | New and changed appraisals, weekly |
| Error handling | ACE ingestion refuses the feed whole if a check fails. The Workbench reads the last complete business date from `v_ace_batch_status` and marks the data product stale |
| Retry | ACE ingestion retries on its own schedule; the Workbench raises AceDataLate when the business date is not complete at its cut-off |
| Owner of the fix | ACE team |
| Standard | File specification |
| Decision | DL06, DL12 |

**Payload**

Appraisal No., Appraised Value, Forced Sale Value, Appraisal Date, collateral or asset reference, valuer.

**Field mapping**

Table.column is the ACE column that holds the value: Tier 1 exists in ACE today, Tier 2 is added by the ACE team in RWB-ACE-001. Read path is the `recovery.v_ace_*` view column the Workbench reads. LDM field is the LDM v7 field ID; the mapping follows the LDM v7 ACE mapping sheet.

| Source field | Table.column | Tier | Read path | LDM field | Type | Mandatory | Transformation |
|---|---|---|---|---|---|---|---|
| Appraisal No. | `valuation.appraisal_no` | Tier 2 | `v_ace_valuation.appraisal_no` | DF-COL-021 | varchar(20) | Yes | Direct copy |
| Appraised Value | `valuation.appraised_value` | Tier 2 | `v_ace_valuation.appraised_value` | DF-COL-023 | numeric(18,2) | Yes | Direct copy |
| Forced Sale Value | `valuation.forced_sale_value` | Tier 2 | `v_ace_valuation.forced_sale_value` | DF-COL-024 | numeric(18,2) | No | Direct copy |
| Appraisal Date | `valuation.appraisal_date` | Tier 2 | `v_ace_valuation.appraisal_date` | DF-COL-025 | date | Yes | Direct copy |

---

## INT-12 AMIS

| Item | Specification |
|---|---|
| Purpose | Assets held, book values and asset sales |
| Direction | In, into ACE |
| Approach | ACE ingestion, read through `v_ace_asset`, `v_ace_npa_asset` and `v_ace_npa_sale` |
| ACE object | `asset` for the asset key and type; `npa_asset` and `npa_sale` (new tables) |
| Trigger | ACE batch complete for AMIS (`v_ace_batch_status`) |
| Frequency | Monthly |
| Volume | About 4,700 properties held; about 30 sales a month |
| Error handling | ACE ingestion refuses the feed whole if a check fails. The Workbench reads the last complete business date from `v_ace_batch_status` and marks the data product stale |
| Retry | ACE ingestion retries on its own schedule; the Workbench raises AceDataLate when the business date is not complete at its cut-off |
| Owner of the fix | ACE team |
| Standard | File specification |
| Decision | DL06, DL12 |

**Payload**

Asset ID, Asset Code, Transfer-in Type, Asset Type, Ownership Transfer in Date, Book Value, Auction Purchase Price, Sale Date, Sale Price, taxes and fees.

**Field mapping**

Table.column is the ACE column that holds the value: Tier 1 exists in ACE today, Tier 2 is added by the ACE team in RWB-ACE-001. Read path is the `recovery.v_ace_*` view column the Workbench reads. LDM field is the LDM v7 field ID; the mapping follows the LDM v7 ACE mapping sheet.

| Source field | Table.column | Tier | Read path | LDM field | Type | Mandatory | Transformation |
|---|---|---|---|---|---|---|---|
| Asset ID | `asset.asset_key` | Tier 1 | `v_ace_asset.asset_ref` | DF-COL-031 | varchar(20) | Yes | Direct copy; ACE business key |
| Asset Code | `npa_asset.asset_code` | Tier 2 | `v_ace_npa_asset.asset_code` | DF-COL-032 | varchar(20) | No | Direct copy |
| Asset Type | `asset.asset_type` | Tier 1 | `v_ace_asset.asset_type` | DF-COL-033 | varchar(20) | Yes | Direct copy |
| Transfer-in Type | `npa_asset.transfer_in_type` | Tier 2 | `v_ace_npa_asset.transfer_in_type` | DF-COL-034 | varchar(20) | Yes | Direct copy |
| From Segment | `npa_asset.from_segment` | Tier 2 | `v_ace_npa_asset.from_segment` | DF-COL-035 | varchar(20) | No | Direct copy |
| Ownership Transfer in Date | `npa_asset.transfer_in_date` | Tier 2 | `v_ace_npa_asset.transfer_in_date` | DF-COL-036 | date | Yes | Direct copy |
| Book  Value | `npa_asset.book_value` | Tier 2 | `v_ace_npa_asset.book_value` | DF-COL-037 | numeric(18,2) | Yes | Direct copy |
| Auction Purchase Price | `npa_asset.auction_purchase_price` | Tier 2 | `v_ace_npa_asset.auction_purchase_price` | DF-COL-038 | numeric(18,2) | No | Direct copy |
| Contract Date | `npa_sale.contract_date` | Tier 2 | `v_ace_npa_sale.contract_date` | DF-SAL-012 | date | Yes | Direct copy |
| Sale Date | `npa_sale.sale_date` | Tier 2 | `v_ace_npa_sale.sale_date` | DF-SAL-013 | date | Yes | Direct copy |
| Sale Price | `npa_sale.sale_price` | Tier 2 | `v_ace_npa_sale.sale_price` | DF-SAL-014 | numeric(18,2) | Yes | Direct copy |
| Sale Transfer Fee | `npa_sale.transfer_fee` | Tier 2 | `v_ace_npa_sale.transfer_fee` | DF-SAL-015 | numeric(18,2) | No | Direct copy |
| Specific Business Tax | `npa_sale.specific_business_tax` | Tier 2 | `v_ace_npa_sale.specific_business_tax` | DF-SAL-016 | numeric(18,2) | No | Direct copy |
| Corporate Income Tax | `npa_sale.corporate_income_tax` | Tier 2 | `v_ace_npa_sale.corporate_income_tax` | DF-SAL-017 | numeric(18,2) | No | Direct copy |
| Incentive Amount | `npa_sale.incentive_amount` | Tier 2 | `v_ace_npa_sale.incentive_amount` | DF-SAL-019 | numeric(18,2) | No | Direct copy |

---

## INT-13 RPS

| Item | Specification |
|---|---|
| Purpose | Repossessed vehicles and stock |
| Direction | In, into ACE |
| Approach | ACE ingestion, read through `v_ace_npa_asset` |
| ACE object | `npa_asset` (new table) |
| Trigger | ACE batch complete for RPS (`v_ace_batch_status`) |
| Frequency | Weekly |
| Volume | About 720 vehicles repossessed a month |
| Error handling | ACE ingestion refuses the feed whole if a check fails. The Workbench reads the last complete business date from `v_ace_batch_status` and marks the data product stale |
| Retry | ACE ingestion retries on its own schedule; the Workbench raises AceDataLate when the business date is not complete at its cut-off |
| Owner of the fix | ACE team |
| Standard | File specification |
| Decision | DL06, DL12 |

**Payload**

AccNo, ContractNo, RepoDT, ReposessedCarDate, VehicleStatus, STOCK_DATE, OutBal.

**Field mapping**

Table.column is the ACE column that holds the value: Tier 1 exists in ACE today, Tier 2 is added by the ACE team in RWB-ACE-001. Read path is the `recovery.v_ace_*` view column the Workbench reads. LDM field is the LDM v7 field ID; the mapping follows the LDM v7 ACE mapping sheet.

| Source field | Table.column | Tier | Read path | LDM field | Type | Mandatory | Transformation |
|---|---|---|---|---|---|---|---|
| ReposessedCarDate | `npa_asset.repossessed_date` | Tier 2 | `v_ace_npa_asset.repossessed_date` | DF-COL-039 | date | No | Thai year date YYMMDD converted to a Gregorian date |
| STOCK_DATE | `npa_asset.stock_date` | Tier 2 | `v_ace_npa_asset.stock_date` | DF-COL-040 | date | No | Converted to a date |

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

Outbound. Table.column is the Workbench (Tier 4) column the file is built from.

| Source field | Table.column | Tier | Read path | LDM field | Type | Mandatory | Transformation |
|---|---|---|---|---|---|---|---|
| DDMMYYYY | `notice.sent_date` | Tier 4 | Workbench table | DF-LEG-019 | date | No | Direct copy |
| Barcode | `notice.barcode` | Tier 4 | Workbench table | DF-LEG-020 | varchar(40) | No | Direct copy |
| DDMMYYYY_callBack | `notice.callback_date` | Tier 4 | Workbench table | DF-LEG-021 | date | No | Direct copy |
| Sent Type | `notice.sent_type` | Tier 4 | Workbench table | DF-LEG-023 | varchar(10) | No | Direct copy |

---

## INT-15 WIN

| Item | Specification |
|---|---|
| Purpose | Proof of delivery for registered mail |
| Direction | In, into ACE |
| Approach | ACE ingestion, read through `v_ace_pod` |
| ACE object | `pod_receipt` (new table) |
| Trigger | ACE batch complete for WIN (`v_ace_batch_status`) |
| Frequency | Weekly |
| Volume | About 1,900 proofs of delivery a month |
| Error handling | ACE ingestion refuses the feed whole if a check fails. The Workbench reads the last complete business date from `v_ace_batch_status` and marks the data product stale |
| Retry | ACE ingestion retries on its own schedule; the Workbench raises AceDataLate when the business date is not complete at its cut-off |
| Owner of the fix | ACE team |
| Standard | File specification |
| Decision | None |

**Payload**

DDMMYYYY, ContractNO, Barcode, DDMMYYYY_callBack, Sent Type.

**Field mapping**

Table.column is the ACE column that holds the value: Tier 1 exists in ACE today, Tier 2 is added by the ACE team in RWB-ACE-001. Read path is the `recovery.v_ace_*` view column the Workbench reads. LDM field is the LDM v7 field ID; the mapping follows the LDM v7 ACE mapping sheet. The notice itself stays in the Workbench; the proof of delivery is held in `pod_receipt`.

| Source field | Table.column | Tier | Read path | LDM field | Type | Mandatory | Transformation |
|---|---|---|---|---|---|---|---|
| DDMMYYYY | `pod_receipt.sent_date` | Tier 2 | `v_ace_pod.sent_date` | DF-LEG-019 | date | No | Direct copy |
| Barcode | `pod_receipt.barcode` | Tier 2 | `v_ace_pod.barcode` | DF-LEG-020 | varchar(40) | No | Direct copy |
| DDMMYYYY_callBack | `pod_receipt.callback_date` | Tier 2 | `v_ace_pod.callback_date` | DF-LEG-021 | date | No | Direct copy |
| Sent Type | `pod_receipt.sent_type` | Tier 2 | `v_ace_pod.sent_type` | DF-LEG-023 | varchar(10) | No | Direct copy |

---

## INT-16 GL

| Item | Specification |
|---|---|
| Purpose | Write-off postings |
| Direction | In, into ACE |
| Approach | ACE ingestion, read through `v_ace_write_off` |
| ACE object | `gl_write_off` (new table) |
| Trigger | ACE batch complete for GL (`v_ace_batch_status`) |
| Frequency | Monthly |
| Volume | Write-off postings each month |
| Error handling | ACE ingestion refuses the feed whole if a check fails. The Workbench reads the last complete business date from `v_ace_batch_status` and marks the data product stale |
| Retry | ACE ingestion retries on its own schedule; the Workbench raises AceDataLate when the business date is not complete at its cut-off |
| Owner of the fix | ACE team |
| Standard | File specification |
| Decision | DL12 |

**Payload**

DATE, RC, OC, ACCOUNT, PRODUCT, EVENT, AMT.

**Field mapping**

Table.column is the ACE column that holds the value: Tier 1 exists in ACE today, Tier 2 is added by the ACE team in RWB-ACE-001. Read path is the `recovery.v_ace_*` view column the Workbench reads. LDM field is the LDM v7 field ID; the mapping follows the LDM v7 ACE mapping sheet. The write-off decision stays in the Workbench; the posting is held in `gl_write_off`.

| Source field | Table.column | Tier | Read path | LDM field | Type | Mandatory | Transformation |
|---|---|---|---|---|---|---|---|
| AMT | `gl_write_off.amount` | Tier 2 | `v_ace_write_off.amount` | DF-FIN-013 | numeric(18,2) | Yes | Direct copy |
| DATE | `gl_write_off.posted_date` | Tier 2 | `v_ace_write_off.posted_date` | DF-FIN-016 | date | No | Direct copy |
| RC | `gl_write_off.responsibility_center` | Tier 2 | `v_ace_write_off.responsibility_center` | DF-FIN-017 | varchar(10) | No | Direct copy |
| OC | `gl_write_off.cost_center` | Tier 2 | `v_ace_write_off.cost_center` | DF-FIN-018 | varchar(10) | No | Direct copy |
| PRODUCT | `gl_write_off.gl_product` | Tier 2 | `v_ace_write_off.gl_product` | DF-FIN-019 | varchar(10) | No | Direct copy |

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
| Approach | ACE sign-in; group-to-role mapping read through `v_ace_iam_group` |
| ACE object | `iam_user`; `iam_group` (new table, RWB-ACE-001) |
| Trigger | Sign-in |
| Frequency | At each sign-in |
| Volume | Every sign-in |
| Error handling | Refuse the session and log it |
| Retry | None |
| Owner of the fix | Security administrator |
| Standard | OpenID Connect |
| Decision | DL40 |

**Payload**

User identity and Entra ID group membership. ACE holds the group-to-role mapping in `iam_group` (`entra_group`, `role_code`) and the Workbench reads it through `v_ace_iam_group.entra_group`.

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

Outbound. Table.column is the Workbench (Tier 4) column the file is built from; the outstanding balance is the snapshot of `v_ace_account.total_balance` at the cut-off date.

| Source field | Table.column | Tier | Read path | LDM field | Type | Mandatory | Transformation |
|---|---|---|---|---|---|---|---|
| BorrCode | `debt_sale_account.borrower_code` | Tier 4 | Workbench table | DF-SAL-034 | varchar(20) | No | Direct copy |
| OS By Acct | `debt_sale_account.outstanding` | Tier 4 | Snapshot of v_ace_account.total_balance at the cut-off date | DF-SAL-035 | numeric(18,2) | Yes | Direct copy |
| SellingPriceByAcct | `debt_sale_account.selling_price` | Tier 4 | Workbench table | DF-SAL-036 | numeric(18,2) | No | Direct copy |

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

## INT-35 NLEADS

| Item | Specification |
|---|---|
| Purpose | Credit approval result for a restructure plan, new to ACE and raised in RWB-ACE-001. The officer's submission in NLEADS stays INT-26 |
| Direction | In, into ACE |
| Approach | ACE ingestion, read through `v_ace_credit_decision` |
| ACE object | `credit_decision` (new table), 4 Workbench fields read |
| Trigger | ACE batch complete for NLEADS (`v_ace_batch_status`) |
| Frequency | As decisions are made |
| Volume | One row per credit decision on a restructure plan |
| Error handling | ACE ingestion refuses the feed whole if a check fails. The Workbench reads the last complete business date from `v_ace_batch_status` and marks the data product stale |
| Retry | ACE ingestion retries on its own schedule; the Workbench raises AceDataLate when the business date is not complete at its cut-off |
| Owner of the fix | ACE team |
| Standard | File specification |
| Decision | D-RCV-35 |

**Payload**

nleads_ref, credit_result, credit_result_reason, decided_at.

**Field mapping**

Table.column is the ACE column that holds the value: Tier 1 exists in ACE today, Tier 2 is added by the ACE team in RWB-ACE-001. Read path is the `recovery.v_ace_*` view column the Workbench reads. LDM field is the LDM v7 field ID; the mapping follows the LDM v7 ACE mapping sheet.

| Source field | Table.column | Tier | Read path | LDM field | Type | Mandatory | Transformation |
|---|---|---|---|---|---|---|---|
| nleads_ref | `credit_decision.nleads_ref` | Tier 2 | `v_ace_credit_decision.nleads_ref` | DF-TRT-023 | varchar(30) | No | Direct copy |
| credit_result | `credit_decision.credit_result` | Tier 2 | `v_ace_credit_decision.credit_result` | DF-TRT-024 | varchar(10) | No | Direct copy |
| credit_result_reason | `credit_decision.credit_result_reason` | Tier 2 | `v_ace_credit_decision.credit_result_reason` | DF-TRT-025 | varchar(1000) | No | Direct copy |
| decided_at | `credit_decision.decided_at` | Tier 2 | `v_ace_credit_decision.decided_at` | DF-TRT-026 | timestamptz(6) | No | Direct copy |

---

## INT-36 EasyApp

| Item | Specification |
|---|---|
| Purpose | E-signature reference and status for a restructure agreement, new to ACE and raised in RWB-ACE-001 |
| Direction | In, into ACE |
| Approach | ACE ingestion, read through `v_ace_esign` |
| ACE object | `esign_request` (new table), 1 Workbench field read |
| Trigger | ACE batch complete for EasyApp (`v_ace_batch_status`) |
| Frequency | As signatures are requested |
| Volume | One row per signature request |
| Error handling | ACE ingestion refuses the feed whole if a check fails. The Workbench reads the last complete business date from `v_ace_batch_status` and marks the data product stale |
| Retry | ACE ingestion retries on its own schedule; the Workbench raises AceDataLate when the business date is not complete at its cut-off |
| Owner of the fix | ACE team |
| Standard | File specification |
| Decision | D-RCV-35 |

**Payload**

external_ref.

**Field mapping**

Table.column is the ACE column that holds the value: Tier 1 exists in ACE today, Tier 2 is added by the ACE team in RWB-ACE-001. Read path is the `recovery.v_ace_*` view column the Workbench reads. LDM field is the LDM v7 field ID; the mapping follows the LDM v7 ACE mapping sheet.

| Source field | Table.column | Tier | Read path | LDM field | Type | Mandatory | Transformation |
|---|---|---|---|---|---|---|---|
| external_ref | `esign_request.external_ref` | Tier 2 | `v_ace_esign.external_ref` | DF-DOC-103 | varchar(60) | No | Direct copy |

ACE receives the signature call-back, so the reference belongs with the ingestion and not on the Workbench document. The signed file stays in the Workbench document hub.

---

## Checks ACE ingestion passes

These checks run in ACE, not in the Workbench. They are the ingestion contract for every inbound interface above and are owned by the ACE team in RWB-ACE-001. The Workbench runs none of them: it reads the result from `v_ace_batch_status` and never sees a refused feed.

| Check | What it tests | If it fails |
|---|---|---|
| Business date | The feed is for the expected business date and is not a repeat | ACE refuses the feed |
| Structure | Every expected field is present with the expected type and length | ACE refuses the feed |
| Control totals | Record count and balance totals match the totals the source sends | ACE refuses the feed |
| Keys | Every record has its key, and no key appears twice | ACE refuses the feed |
| References | Each account, customer or asset matches a record ACE holds | ACE holds the row and reports it in its exception list |
| Lists of values | Each coded value is in its list of values | ACE holds the row and reports it in its exception list |
| Movement | Changes against the previous business date are within the expected range | ACE loads and alerts the data steward |

## Checks every outbound file passes

| Check | What it tests | If it fails |
|---|---|---|
| Layout | Every field matches the agreed file specification and template version | Do not send; raise to the platform administrator |
| Control totals | The header count and amount totals match the rows in the file | Do not send; raise to the platform administrator |
| Acknowledgement | The receiving system confirms the file | Hold the case step and send again |
