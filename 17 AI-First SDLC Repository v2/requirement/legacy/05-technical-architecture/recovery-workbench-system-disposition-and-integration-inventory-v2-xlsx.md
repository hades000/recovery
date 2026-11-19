<!-- source: 05 Technical architecture/Recovery Workbench System Disposition and Integration Inventory v2.xlsx -->
<!-- converted: 2026-11-16 from XLSX -->

> **Source:** `05 Technical architecture/Recovery Workbench System Disposition and Integration Inventory v2.xlsx`  
> **Converted from:** XLSX

## Disposition

| System disposition |  |  |  |  |  |  |
|---|---|---|---|---|---|---|
| 24 systems and tools that recovery uses today, what happens to each and when. |  |  |  |  |  |  |
| System | Role in recovery today | Disposition | What the Workbench does with it | From | Interfaces | Decision |
| Core bank (ALS) | System of record for loan accounts, balances, payments and bookings | Keep | Reads accounts and payments through COLLINS daily; bookings stay in the core bank, made by the officer and confirmed on the next load | E1 | INT-01, INT-02, INT-03 | DL12 |
| SCBPDM | Customer profile, identifiers and contact details | Keep | Reads the customer profile ACE already receives through COLLINS | E1 | INT-04 | DL20 |
| UDP | Customer and account attributes in the data platform | Keep | Reads attributes through COLLINS | E1 | INT-05 | DL20 |
| AAL | Data ACE already receives | Keep | Reads through COLLINS | E1 | INT-06 | DL12 |
| EFS | Collections case handling to day 90; recovery teams also look up history in it | Keep for collections | Takes over each case at day 90 with its contact history, action codes and promises; recovery case handling moves to the Workbench | E1 | INT-07 | DL29 |
| COLLINS | Collection engine data platform and models | Keep and feed | Data route for every daily load; receives decisions and outcomes back for model learning | E1 | INT-08, INT-20 | DT12 |
| ACE | Collection workbench in production: sign-in, access, audit, case view, restructure calculator | Extend | The Workbench is built inside ACE as its recovery module; common parts are reused | E1 | INT-21, INT-22, INT-34 | DT07, DT08 |
| LIT | Litigation tracking and lawsuit numbers | Keep | Reads litigation status through COLLINS; law firms report through the partner portal from Epic 5 | E1 | INT-09, INT-33 | DL12 |
| CCMS | Collateral records | Keep | Weekly file load | E1 | INT-10 | DL06, DL12 |
| SVAF | Appraisals | Keep | Weekly file load; replaces the manual appraisal file | E1 | INT-11 | DL06, DL12 |
| AMIS | Assets held, book values and asset sales | Keep | Monthly file load | E3 | INT-12 | DL06, DL12 |
| RPS | Repossessed vehicles and stock | Keep | Weekly file load | E3 | INT-13 | DL06, DL12 |
| WIN | Registered mail for notices | Keep | Sends notices out by daily file and loads proof of delivery weekly | E1 | INT-14, INT-15 | None |
| GL | General ledger | Keep | Monthly load of write-off postings | E6 | INT-16 | DL12 |
| NSS and LINE OA | SMS and LINE messages to customers | Keep | Sends through the ACE notification path | E2 | INT-17, INT-18 | DL30 |
| Data lake and Power BI | Bank reporting | Keep and feed | Receives case, queue, decision and outcome data daily; recovery reports move here from spreadsheets | E1 | INT-19 | None |
| Enterprise AI model endpoint | Bank model hosting in the SCB tenant | Reuse | The agents call it through a private endpoint | E1 | INT-23 | DL33 |
| Partner portal | Does not exist | New | Workbench screens for law firms, auction houses and buyers through the external gateway; needs the architecture change with one to three months of lead time | E5 | INT-24, INT-25 | DL03 |
| NLEADS | Credit approval for restructure plans | Keep | No interface; the officer submits in NLEADS and records the result on the case | E3 | INT-26 | DL12 |
| HOME.SCB | Public listing of assets for sale | Keep | No interface; the sales team publishes the listing and records it on the asset | E4 | INT-27 | DL12 |
| SCIS, TCG, NCB, Aric, Salesforce | Vehicle transfer, guarantee claims, contact tracing, fraud referral, NPA work orders | Keep | No interface; the officer works in the system and records the result on the case | E3 | INT-28 to INT-32 | DL12 |
| Recovery team spreadsheets and SharePoint lists | Open recovery work, trackers and approvals | Retire | Open items load into the Workbench; each spreadsheet runs side by side for two weeks, then retires with a read-only archive after ten clean days | E1 | File load (RWB-E1-010, RWB-E1-012) | None |
| Email approvals in Outlook | Approval of recovery decisions | Replace | Approvals move to the Workbench approval queue with the decision log | E2 | None | None |
| Shared folders of scanned documents | Recovery documents and originals custody | Replace | The document hub becomes the system of record for recovery documents | E1 | None | DT06 |

## Interfaces

| Integration inventory |  |  |  |  |  |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 34 interfaces with 31 systems. No component calls a system of record directly: data comes in through COLLINS or a file load and leaves through paths ACE already has. |  |  |  |  |  |  |  |  |  |  |  |
| ID | System | What the Workbench uses it for | Direction | Route | Path | Frequency | Data product | In ACE today | First needed | Standard | Decision |
| INT-01 | Core bank (ALS) | Loan accounts, balances, arrears, days past due, classification | In | COLLINS | COLLINS batch | Daily, end of day | DP01 | Yes | E1 | File specification | None |
| INT-02 | Core bank (ALS) | Payments posted to each account | In | COLLINS | COLLINS batch | Daily, end of day | DP01, DP13 | Yes | E1 | File specification | None |
| INT-03 | Core bank (ALS) | Restructure, settlement and write-off bookings | Out | Not at all today | Booked by the officer; confirmed on the next day's load | As approved | DP04, DP13 | Not applicable | E3 | None | DL12 |
| INT-04 | SCBPDM | Customer profile, identifiers and contact details | In | COLLINS | COLLINS batch | Daily, end of day | DP02 | Yes | E1 | File specification | DL20 |
| INT-05 | UDP | Customer and account attributes held in the data platform | In | COLLINS | COLLINS batch | Daily, end of day | DP01, DP02 | Yes | E1 | File specification | DL20 |
| INT-06 | AAL | Data ACE already receives through COLLINS | In | COLLINS | COLLINS batch | Daily, end of day | To confirm | Yes | E1 | File specification | DL12 |
| INT-07 | EFS | Collections history, action codes and promises before day 90 | In | COLLINS | COLLINS batch | Daily, end of day | DP05 | Partly | E1 | File specification | DL29 |
| INT-08 | COLLINS models | Scores, return by route, price and sale success estimates, scheme suggestions | In | COLLINS | COLLINS batch | Daily; monthly for some models | DP11 | Yes | E1 | File specification | None |
| INT-09 | LIT | Litigation status and lawsuit numbers | In | COLLINS | COLLINS batch | Daily, end of day | DP07 | Partly | E1 | File specification | None |
| INT-10 | CCMS | Collateral records | In | File | File load | Weekly | DP06 | No | E1 | File specification | DL06, DL12 |
| INT-11 | SVAF | Appraisals | In | File | File load | Weekly | DP06 | Manual file, weekly or monthly | E1 | File specification | DL06, DL12 |
| INT-12 | AMIS | Assets held, book values and asset sales | In | File | File load | Monthly | DP06 | No | E3 | File specification | DL06, DL12 |
| INT-13 | RPS | Repossessed vehicles and stock | In | File | File load | Weekly | DP06 | No | E3 | File specification | DL06, DL12 |
| INT-14 | WIN | Demand, recall and sale notices for registered mail | Out | File | File | Daily | DP07 | No | E1 | File specification | None |
| INT-15 | WIN | Proof of delivery for registered mail | In | File | File load | Weekly | DP07 | No | E2 | File specification | None |
| INT-16 | GL | Write-off postings | In | File | File load | Monthly | DP13 | No | E6 | File specification | DL12 |
| INT-17 | NSS | SMS to customers | Out | Direct through ACE | ACE notification path | As sent | DP05 | Yes | E2 | Common module interface | DL30 |
| INT-18 | LINE OA | LINE messages to customers | Out | Direct through ACE | ACE notification path | As sent | DP05 | Yes | E2 | Common module interface | DL30 |
| INT-19 | Data lake and Power BI | Case, queue, decision and outcome data for reporting | Out | File | Daily batch | Daily | DP03, DP12 | Not applicable | E1 | File specification | None |
| INT-20 | COLLINS | Decisions and outcomes for model learning | Out | File | Daily batch to the data lake | Daily | DP12 | Not applicable | E2 | File specification | None |
| INT-21 | Entra ID and the bank IAM | Sign-in and the roles each user holds | In | Direct through ACE | ACE sign-in | At each sign-in | DP14 | Yes | E1 | OpenID Connect | DL40 |
| INT-22 | PII Kafka, audit and SOC logs | Personal data access, audit and security events | Out | Direct through ACE | ACE logging | As they happen | None | Yes | E1 | AsyncAPI 3.0 | None |
| INT-23 | Enterprise AI model endpoint | The model the agents call | Both | Direct through ACE | Private endpoint in the SCB tenant | Per request | None | No | E1 | OpenAPI 3.1 | DL33 |
| INT-24 | Partner portal | Instructions to partners and the results they report | Both | Direct through ACE | Workbench screens through the external gateway | As entered | DP06, DP07, DP08 | No | E2 | OpenAPI 3.1 | DL03 |
| INT-25 | Debt buyers | Debt sale data tape for an awarded lot | Out | File | File through the data room | Per lot | DP09 | No | E5 | File specification | None |
| INT-26 | NLEADS | Credit approval for restructure plans | Out | Not at all today | Submitted by the officer in NLEADS | As needed | DP04 | Not applicable | E3 | None | DL12 |
| INT-27 | HOME.SCB | Listings of assets for sale | Out | Not at all today | Not available today; published by the sale officer | As listed | DP06 | No | E3 | None | DL12 |
| INT-28 | SCIS | Vehicle registration transfer | Out | Not at all today | Not available today; prepared by the officer | As needed | DP06 | No | E4 | None | DL12 |
| INT-29 | Thai Credit Guarantee Corporation | Quota and claim submission | Both | Not at all today | Not available today; entered and filed by the guarantee officer | As needed | DP04 | No | E4 | None | DL12 |
| INT-30 | NCB | Contact tracing for lost contact | In | Not at all today | Not available today; by the officer | As needed | DP02 | No | E7 | None | DL12 |
| INT-31 | Aric | Fraud referral | Out | Not at all today | Not available today; by the fraud investigator | As needed | None | No | E8 | None | DL12 |
| INT-32 | Salesforce | Work orders and operational status for NPA | In | Not at all today | Not available today | None | DP06 | No | Not planned | None | DL12 |
| INT-33 | Legal Execution Department and courts | Enforcement and court records | In | Through partners | Through the law firms in the partner portal | As entered | DP07 | Not applicable | E5 | None | None |
| INT-34 | ACE common module | Shared case view, entities, restructure calculator, notification path | Both | Direct through ACE | Published module interface | Per request | DP03, DP04 | Yes | E1 | Module interface | DL14 |

## By route

| Interfaces by route and direction |  |  |  |  |
|---|---|---|---|---|
| Calculated from the Interfaces tab. |  |  |  |  |
| Route | In | Out | Both | Total |
| COLLINS |  |  |  |  |
| File |  |  |  |  |
| Direct through ACE |  |  |  |  |
| Through partners |  |  |  |  |
| Not at all today |  |  |  |  |
| Total |  |  |  |  |

## Key

| Key |  |  |
|---|---|---|
| What each disposition, route and standard means. |  |  |
| Item | Term | Meaning |
| Disposition | Keep | The system stays as it is; the Workbench reads from it or the officer works in it |
| Disposition | Keep for collections | The system stays for collections; recovery work moves to the Workbench |
| Disposition | Keep and feed | The system stays and the Workbench sends data back to it |
| Disposition | Extend | The Workbench is built inside it |
| Disposition | Reuse | The Workbench uses the bank service as it is |
| Disposition | New | Built for the Workbench |
| Disposition | Replace | The Workbench takes over the work; the old way stops |
| Disposition | Retire | Switched off after the content moves to the Workbench |
| Route | COLLINS | The COLLINS daily batch into the ACE database |
| Route | File | A file load or an outbound file through the integration adapters |
| Route | Direct through ACE | A path ACE already runs: sign-in, logging, the notification path, the common module, the model endpoint, the partner portal |
| Route | Through partners | Entered by a partner in the partner portal |
| Route | Not at all today | No interface. A person does the step in the other system and records it on the case |
| Standard | OpenAPI 3.1 | Request and response interfaces |
| Standard | AsyncAPI 3.0 | Event interfaces |
| Standard | File specification | Batch files: layout, control totals, business date and checks, in the interface specifications |
