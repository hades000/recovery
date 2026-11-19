<!-- source: 06 Data/Recovery Workbench Data Ownership and Stewardship v3.xlsx -->
<!-- converted: 2026-11-16 from XLSX -->

> **Source:** `06 Data/Recovery Workbench Data Ownership and Stewardship v3.xlsx`  
> **Converted from:** XLSX

## Ownership

| Who owns each data product |  |  |  |  |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|---|---|---|
| 14 data products, each with one business owner, one steward and one system of record. ACE owns the source data; the Workbench owns the case. The tier column says which, and RWB-ACE-001 is the only route to a new field in Tier 1 or Tier 2. |  |  |  |  |  |  |  |  |  |  |
| ID | Data product | What it holds | Business owner | Data steward | System of record | System of record owner | Who may change it | How a change is requested | Freshness | Tier |
| DP01 | Account and arrears | Loan accounts with balances, interest, fees, days past due, bucket, classification, restructure flag and payments | Product heads | Data steward and data product owner | ACE (account and payment, ingested from ALS) | ACE team lead | The ACE team only; the Workbench reads the view | Raise it with the ACE team; a new field is a change to RWB-ACE-001 | End of day in ACE; read as of the ACE business date | 1 and 2 |
| DP02 | Customer and party | Customers, guarantors, co-borrowers and heirs, identity numbers masked in the view, contact points, consent and flags for vulnerability, death and bankruptcy | Compliance and PDPA officer | Data steward and data product owner | ACE (customer, ca_relation and contact views) | ACE team lead for Tier 1 and 2; application owner for Tier 3 (party_ext, contact_point_ext) | The ACE team only; Workbench flags live in the extension tables | Raise it with the ACE team; a new field is a change to RWB-ACE-001 | End of day in ACE; read as of the ACE business date | 1, 2 and 3 |
| DP03 | Case and ownership | The case, its accounts and parties, status, stage, route, owner, queue, tasks, timers and deviations | Business lead | Data steward and data product owner | Recovery Workbench | Application owner (DL02) | Users with the right in the permission matrix, through Workbench screens | Raise the change with the business owner; the product owner adds it to the backlog or the reference data administrator loads it | As it changes | 4 |
| DP04 | Treatment and offers | Restructures, settlements, deeds in lieu, buy-backs and guarantee claims, with terms, approval level and outcome | Product heads | Data steward and data product owner | Recovery Workbench; restructure plans read from v_ace_plan | Application owner with the ACE team | Users with the right in the permission matrix for the Workbench record; the ACE team for the plan | Raise the change with the business owner; the product owner adds it to the backlog or the reference data administrator loads it | As it changes | 1 and 4 |
| DP05 | Contact and promises | Every contact, letter, promise and hand-over on the case, in order, including the collections history from EFS | Business lead | Data steward and data product owner | ACE (efs_action) and the Workbench for its own interactions | Collections system owner; application owner | The ACE team for EFS history; users for Workbench interactions | Raise it with the ACE team for EFS history; Workbench fields go to the product owner | End of day in ACE for EFS history; as it changes here | 1, 2 and 4 |
| DP06 | Collateral and assets | Collateral, appraisals, assets held after repossession or transfer, listings and sale results | Head of NPA | Data steward and data product owner | ACE (collateral, asset, valuation, npa_asset and npa_sale) | ACE team lead for Tier 1 and 2; application owner for Tier 3 and 4 | The ACE team only; the Workbench decides in valuation_ext | Raise it with the ACE team; a new field is a change to RWB-ACE-001 | Weekly or monthly in ACE, as each source ingests | 1, 2, 3 and 4 |
| DP07 | Legal events and cases | Notices and proof of delivery, lawsuits, court case numbers, hearings, judgments and enforcement | Head of Litigation | Data steward and data product owner | ACE (lawsuit, hearing and pod_receipt) and the Workbench for notices and instructions | Legal systems owner; application owner | The ACE team for court records; users for instructions | Raise it with the ACE team for court records; Workbench fields go to the product owner | End of day in ACE for LIT status | 2 and 4 |
| DP08 | Partner performance | Partners on the panel, work placed with each, results, fees and scorecards | Partner and agency manager | Data steward and data product owner | Recovery Workbench | Application owner (DL02) | Users with the right in the permission matrix, through Workbench screens | Raise the change with the business owner; the product owner adds it to the backlog or the reference data administrator loads it | As it changes | 4 |
| DP09 | Debt sale | Debt sale lots, the accounts in each lot, buyers, prices, approval and put-backs | Head of Asset Liquidity | Data steward and data product owner | Recovery Workbench | Application owner (DL02) | Users with the right in the permission matrix, through Workbench screens | Raise the change with the business owner; the product owner adds it to the backlog or the reference data administrator loads it | As it changes | 4 |
| DP10 | Documents and extracted fields | Documents against the case, the fields read from them, retention class and custody of originals | Legal counsel | Data steward and data product owner | Recovery Workbench document hub | Application owner (DL02) | The document hub; legal documents are write-once | Raise the change with the business owner; the product owner adds it to the backlog or the reference data administrator loads it | As it changes | 4 |
| DP11 | Scores and route economics | Risk scores, expected return by route, estimated sale price and sale success rate, restructure scheme suggestions | Risk and model risk officer | Data steward and data product owner | ACE (collins_score) and the Workbench for route economics | ACE team lead for Tier 2; application owner for Tier 4 | The ACE team for scores; the product owner for route economics | Raise it with the ACE team for scores; Workbench changes go to the product owner | End of day in ACE for scores; monthly for some models | 2 and 4 |
| DP12 | Decision log | One entry per decision with the rule, model and agent versions, inputs, recommendation, approval, actions and outcome | Risk and model risk officer | Data steward and data product owner | Recovery Workbench | Application owner (DL02) | No one; append only. Corrections are new entries | Raise the change with the business owner; the product owner adds it to the backlog or the reference data administrator loads it | As it changes | 4 |
| DP13 | Money and closure | Payments and proceeds matched to the case, write-off postings and recovery after charge-off | Finance and CFO delegate | Data steward and data product owner | ACE (payment and gl_write_off) and the Workbench for matching | ACE team lead for Tier 1 and 2; application owner for Tier 4 | The ACE team only; the Workbench matches proceeds to the case | Raise it with the ACE team; a new field is a change to RWB-ACE-001 | End of day in ACE for payments; monthly for GL | 1, 2 and 4 |
| DP14 | Reference data | Rules, approval limits, lists of values, roles, permissions and letter templates, each versioned | Center of excellence | Data steward and data product owner | Recovery Workbench | Application owner (DL02) | Reference data administrator, after approval by the list owner; Risk where a limit moves | Raise the change with the business owner; the product owner adds it to the backlog or the reference data administrator loads it | By versioned load | 4 |

## Ownership split

_Merged ranges: A10:F10_

| Who owns which tier |  |  |  |  |  |
|---|---|---|---|---|---|
| ACE owns the source data, the Workbench owns the case. RWB-ACE-001 is the only route to a new field in Tier 1 or Tier 2; a Workbench request never alters an ACE table. |  |  |  |  |  |
| Tier | What it holds | Owner | Who may add a field | Route for a new field | Workbench access |
| 1 | 22 ACE tables that exist today, read through 16 views | ACE team | The ACE team, under ACE change control | No new ACE object: the view maps a column ACE already holds. If ACE holds nothing, the field is Tier 2 | SELECT through recovery.v_ace_* only |
| 2 | 14 new tables and 12 new columns for source data that ACE does not hold, read through 14 views | ACE team | The ACE team, under ACE change control | RWB-ACE-001, with a field row in the ACE Field Gap List. The views ship the week it lands | SELECT once the view exists; the feature stays behind its flag until then |
| 3 | 4 extension tables keyed by ACE business keys: party_ext, contact_point_ext, account_ext, valuation_ext | Workbench data steward | The Workbench data steward, with the business owner | Workbench backlog. The table holds a decision about an ACE record and never a copy of one | Read and write by the recovery module |
| 4 | 88 Workbench tables: case, workflow, treatment, legal, partner, debt sale, documents, decision log, reference, outbox, flags and agents | Workbench data steward | The Workbench data steward, with the business owner | Workbench backlog; the product owner approves, and the change is versioned in the data dictionary | Read and write by the recovery module |
| A screen that needs a new source field follows the Tier 2 route even when the screen is a Workbench screen. The Workbench never alters an ACE table and never adds a column to one. |  |  |  |  |  |

## Roles

| Data roles |  |
|---|---|
| What each data role does. |  |
| Role | Accountable for |
| Business owner | Decides what the data means, who may use it and the quality it must meet. Approves definition changes in the Workbench and sponsors an RWB-ACE-001 change for a source field |
| Data steward | Keeps definitions, read mappings, quality checks and the exception list. The Workbench data steward owns Tier 3 and Tier 4; the ACE data steward owns the ingestion checks for Tier 1 and Tier 2 |
| System of record owner | Owns the source system and its fields. The ACE team lead holds this for Tier 1 and Tier 2; the Workbench application owner holds it for Tier 3 and Tier 4. Confirms the read mapping |
| Application owner | Owns the Workbench as the system of record for the data it creates |
| Reference data administrator | Loads lists, rules and limits after the owner approves, in the Workbench only |
| Compliance and PDPA officer | Sets the classification, masking and retention for personal data |
| ACE team lead | Owns the Tier 1 and Tier 2 tables, the RWB-ACE-001 scope and dates, and the SELECT grant the views need. Approves every change to an ACE table or column the views read |
| ACE data steward | Keeps the identity match M1 to M5, the ingestion checks and the per-source business date that v_ace_batch_status reports |

## Change process

| How a data change is requested |  |  |
|---|---|---|
| Every change to a data product follows these steps. |  |  |
| Step | Stage | What happens |
| 1 | Request | The requester raises the change with the business owner, with the reason and the date it is needed |
| 2 | Assess | The data steward assesses the effect on the read mapping, the checks, the reports and the models; the ACE team assesses it too where a Tier 1 or Tier 2 field moves |
| 3 | Approve | The business owner approves. Compliance approves where personal data changes; Risk where a limit or a model input changes |
| 4 | Make | A Tier 1 or Tier 2 change is made by the ACE team, through RWB-ACE-001 for a new field; a Tier 3 or Tier 4 change goes to the Workbench backlog; a list or limit change is a validated load |
| 5 | Test | The change runs through the ACE ingestion checks and the view conformance test in SIT |
| 6 | Release | In the monthly release, or as a validated reference load with a valid from date |
| 7 | Record | The data dictionary and the mapping are updated with the version |

## Quality measures

| What the steward measures |  |  |
|---|---|---|
| Measured for every data product each day. |  |  |
| Measure | Meaning | Where it is checked |
| Completeness | Every mandatory field is filled | ACE ingestion checks for Tier 1 and 2; Workbench data quality rules for Tier 3 and 4 |
| Accuracy | Balances reconcile to the core bank within the tolerance (DL25) | Daily reconciliation |
| Timeliness | The data product carries the expected business date | v_ace_batch_status |
| Validity | Every coded value is in its list | ACE ingestion checks for Tier 1 and 2; Workbench data quality rules and lov_value for Tier 3 and 4 |
| Uniqueness | One case per customer per product (DL17) | Workbench case entry rule (DL17), on the person_key that the ACE identity match M1 to M5 gives |
| View conformance | Every v_ace_* view compiles and no recovery table reads public.* | Build pipeline |
| Freshness stamp | The ACE business date is visible on the case screen | Screen check |
