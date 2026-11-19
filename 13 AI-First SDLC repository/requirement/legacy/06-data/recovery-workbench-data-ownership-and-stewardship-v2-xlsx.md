<!-- source: 06 Data/Recovery Workbench Data Ownership and Stewardship v2.xlsx -->
<!-- converted: 2026-11-04 from XLSX -->

> **Source:** `06 Data/Recovery Workbench Data Ownership and Stewardship v2.xlsx`  
> **Converted from:** XLSX

## Ownership

| Who owns each data product |  |  |  |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|---|---|
| 14 data products, each with one business owner, one steward and one system of record. The business owner decides what the data means; the steward keeps it right. |  |  |  |  |  |  |  |  |  |
| ID | Data product | What it holds | Business owner | Data steward | System of record | System of record owner | Who may change it | How a change is requested | Freshness |
| DP01 | Account and arrears | Loan accounts with balances, interest, fees, days past due, bucket, classification, restructure flag and payments | Product heads | Data steward and data product owner | Core bank (ALS) | Core banking owner | The source system only; the Workbench reads it | Raise the change with the system owner; the data steward updates the mapping | End of day; in the Workbench the next morning |
| DP02 | Customer and party | Customers, guarantors, co-borrowers and heirs, tokenized identifiers, contact points, consent and flags for vulnerability, death and bankruptcy | Compliance and PDPA officer | Data steward and data product owner | SCBPDM and core bank | Data and analytics owner | The source system only; the Workbench reads it | Raise the change with the system owner; the data steward updates the mapping | End of day; in the Workbench the next morning |
| DP03 | Case and ownership | The case, its accounts and parties, status, stage, route, owner, queue, tasks, timers and deviations | Business lead | Data steward and data product owner | Recovery Workbench | Application owner (DL02) | Users with the right in the permission matrix, through Workbench screens | Raise the change with the business owner; the product owner adds it to the backlog or the reference data administrator loads it | As it changes |
| DP04 | Treatment and offers | Restructures, settlements, deeds in lieu, buy-backs and guarantee claims, with terms, approval level and outcome | Product heads | Data steward and data product owner | Recovery Workbench; restructure plans in ACE | Application owner with the ACE team | Users with the right in the permission matrix, through Workbench screens | Raise the change with the business owner; the product owner adds it to the backlog or the reference data administrator loads it | As it changes |
| DP05 | Contact and promises | Every contact, letter, promise and hand-over on the case, in order, including the collections history from EFS | Business lead | Data steward and data product owner | EFS before day 90; the Workbench after | Collections system owner; application owner | Users with the right in the permission matrix, through Workbench screens | Raise the change with the business owner; the product owner adds it to the backlog or the reference data administrator loads it | End of day for EFS history; as it changes after |
| DP06 | Collateral and assets | Collateral, appraisals, assets held after repossession or transfer, listings and sale results | Head of NPA | Data steward and data product owner | CCMS, SVAF, AMIS, RPS | Collateral, valuation, NPA and repossession system owners | The source system only; the Workbench reads it | Raise the change with the system owner; the data steward updates the mapping | Weekly or monthly today |
| DP07 | Legal events and cases | Notices and proof of delivery, lawsuits, court case numbers, hearings, judgments and enforcement | Head of Litigation | Data steward and data product owner | LIT for court records; the Workbench for instructions | Legal systems owner; application owner | Users with the right in the permission matrix, through Workbench screens | Raise the change with the business owner; the product owner adds it to the backlog or the reference data administrator loads it | End of day for LIT status |
| DP08 | Partner performance | Partners on the panel, work placed with each, results, fees and scorecards | Partner and agency manager | Data steward and data product owner | Recovery Workbench | Application owner (DL02) | Users with the right in the permission matrix, through Workbench screens | Raise the change with the business owner; the product owner adds it to the backlog or the reference data administrator loads it | As it changes |
| DP09 | Debt sale | Debt sale lots, the accounts in each lot, buyers, prices, approval and put-backs | Head of Asset Liquidity | Data steward and data product owner | Recovery Workbench | Application owner (DL02) | Users with the right in the permission matrix, through Workbench screens | Raise the change with the business owner; the product owner adds it to the backlog or the reference data administrator loads it | As it changes |
| DP10 | Documents and extracted fields | Documents against the case, the fields read from them, retention class and custody of originals | Legal counsel | Data steward and data product owner | Recovery Workbench document hub | Application owner (DL02) | The document hub; legal documents are write-once | Raise the change with the business owner; the product owner adds it to the backlog or the reference data administrator loads it | As it changes |
| DP11 | Scores and route economics | Risk scores, expected return by route, estimated sale price and sale success rate, restructure scheme suggestions | Risk and model risk officer | Data steward and data product owner | COLLINS | Data and analytics owner | Data and analytics through COLLINS; Model Risk approves model changes | Raise the change with the system owner; the data steward updates the mapping | End of day; monthly for some models |
| DP12 | Decision log | One entry per decision with the rule, model and agent versions, inputs, recommendation, approval, actions and outcome | Risk and model risk officer | Data steward and data product owner | Recovery Workbench | Application owner (DL02) | No one; append only. Corrections are new entries | Raise the change with the business owner; the product owner adds it to the backlog or the reference data administrator loads it | As it changes |
| DP13 | Money and closure | Payments and proceeds matched to the case, write-off postings and recovery after charge-off | Finance and CFO delegate | Data steward and data product owner | Core bank (ALS) and GL | Core banking and finance systems owners | The source system only; the Workbench reads it | Raise the change with the system owner; the data steward updates the mapping | End of day for payments; monthly for GL |
| DP14 | Reference data | Rules, approval limits, lists of values, roles, permissions and letter templates, each versioned | Center of excellence | Data steward and data product owner | Recovery Workbench | Application owner (DL02) | Reference data administrator, after approval by the list owner; Risk where a limit moves | Raise the change with the business owner; the product owner adds it to the backlog or the reference data administrator loads it | By versioned load |

## Roles

| Data roles |  |
|---|---|
| What each data role does. |  |
| Role | Accountable for |
| Business owner | Decides what the data means, who may use it and the quality it must meet. Approves definition changes |
| Data steward | Keeps definitions, mappings, quality checks and the exception list. Reviews load breaks every day |
| System of record owner | Owns the source system, its fields and its file or batch layout. Confirms the source to target mapping |
| Application owner | Owns the Workbench as the system of record for the data it creates |
| Reference data administrator | Loads lists, rules and limits after the owner approves |
| Compliance and PDPA officer | Sets the classification, masking and retention for personal data |

## Change process

| How a data change is requested |  |  |
|---|---|---|
| Every change to a data product follows these steps. |  |  |
| Step | Stage | What happens |
| 1 | Request | The requester raises the change with the business owner, with the reason and the date it is needed |
| 2 | Assess | The data steward assesses the effect on mappings, checks, reports and models |
| 3 | Approve | The business owner approves. Compliance approves where personal data changes; Risk where a limit or a model input changes |
| 4 | Make | A source change is made by the system owner; a Workbench field change goes to the backlog; a list or limit change is a validated load |
| 5 | Test | The change runs through the load checks in SIT |
| 6 | Release | In the monthly release, or as a data load with a valid from date |
| 7 | Record | The data dictionary and the mapping are updated with the version |

## Quality measures

| What the steward measures |  |  |
|---|---|---|
| Measured for every data product each day. |  |  |
| Measure | Meaning | Where it is checked |
| Completeness | Every mandatory field is filled | Load checks |
| Accuracy | Balances reconcile to the core bank within the tolerance (DL25) | Daily reconciliation |
| Timeliness | The data product carries the expected business date | Freshness check |
| Validity | Every coded value is in its list | Load checks |
| Uniqueness | One case per customer per product (DL17) | Duplicate check |
