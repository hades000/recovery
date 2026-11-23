<!-- source: 06 Data/Recovery Workbench Conceptual Data Model v6.xlsx -->
<!-- converted: 2026-11-16 from XLSX -->

> **Source:** `06 Data/Recovery Workbench Conceptual Data Model v6.xlsx`  
> **Converted from:** XLSX

## Subject areas

| Subject areas |  |  |  |  |
|---|---|---|---|---|
| 17 subject areas. Each entity belongs to one subject area, including the 30 read-only ACE source views and the 4 extension tables. The entity count is counted from the Entities tab. |  |  |  |  |
| Subject area | What it holds | Entities | Entities in it | Data products |
| Case | The recovery case, its owner, its status and route, and the accounts and parties linked to it. | 5 | Recovery case, Case account, Case party, Deviation, Case entry exclusion | DP03 |
| Work management | Queues, assignments, tasks and timers that move the case and hold it to service levels. | 5 | Queue, Assignment, Task, Timer, Queue member | DP03 |
| Party | Customers, guarantors, co-borrowers and heirs, their role on the case and how to reach them. | 6 | Party extension, Contact point extension, v_ace_customer, v_ace_contact, v_ace_ca_relation, v_ace_party_product | DP02 |
| Account and arrears | Loan accounts with balances, arrears, days past due, classification and payments. | 5 | Account extension, v_ace_account, v_ace_payment, v_ace_aa_relation, v_ace_bucket_log | DP01 |
| Collateral and asset | Collateral securing the accounts, its valuation, and assets the bank holds after repossession or transfer. | 6 | Valuation extension, v_ace_collateral, v_ace_asset, v_ace_valuation, v_ace_collateral_detail, v_ace_npa_asset | DP06 |
| Treatment | Restructures, settlements, deeds in lieu, guarantee claims and their terms, approvals and outcomes. | 6 | Treatment, Guarantee claim, Dp treatment, Dp guarantee claim, v_ace_plan, v_ace_credit_decision | DP04 |
| Legal | Notices, lawsuits, hearings, judgments and enforcement. | 6 | Legal action, Notice, Hearing, v_ace_lawsuit, v_ace_hearing, v_ace_pod | DP07 |
| Partner | Law firms, agencies, valuers, auction vendors and buyers, and the work placed with them. | 2 | Partner, Partner instruction | DP08 |
| Disposal and debt sale | Asset listings and bids, debt sale lots, buyers and awards. | 5 | Listing, Asset sale, Debt sale lot, Debt sale account, v_ace_npa_sale | DP06, DP09 |
| Interaction | Every contact, letter, promise and hand-over on the case, in order. | 3 | Interaction, v_ace_efs_action, v_ace_efs_assignment | DP05 |
| Document | Documents held against the case, the fields extracted from them, and custody of originals. | 9 | Document, Document field, Document custody, Case document check, Document intake, Document text, Retention action, Signature request, v_ace_esign | DP10 |
| Decision and control | One log entry per decision, with versions, inputs, recommendation, approval, actions and outcome. | 3 | Decision log entry, Approval, v_ace_score | DP12, DP11 |
| Money and closure | Payments and proceeds matched to the case, write-offs and recovery after charge-off. | 3 | Proceeds, Write-off, v_ace_write_off | DP13 |
| Reference and access | Rules, limits, lists of values, roles, permissions and templates, all versioned. | 31 | Rule, Delegation limit, List value, Role, Permission, Template, Data product, Data product access, Sys objects, Sys fields, Sys field version, Retention rule, Efs ledger outcome, Parameter catalog, Parameter value, Reference version, Reference row, Rule test case, Masking rule, Role conflict, Partner user, Document type, Document checklist item, Document hub parameter, Merge field, Payment match rule, v_ace_efs_action_code, v_ace_product, v_ace_branch, v_ace_holiday, v_ace_iam_group | DP14 |
| Loads and operations | Interfaces, reconciliation, jobs, feature flags, the outbox and idempotency records that run the Workbench. Source batches are read through v_ace_batch_status, not loaded. | 14 | Data product load, Data contract, Reconciliation result, Lake copy watermark, Interface config, Outbound item, Processed event, Idempotency key, Outbox event, Outbox delivery, Feature flag, Feature flag change, Job catalog, v_ace_batch_status | OPS |
| Agent runtime | Agent policies, prompts, runs, labeled samples, evaluations, feedback and alerts. | 8 | Agent policy, Agent prompt, Agent run, Agent sample, Agent evaluation run, Agent evaluation, Agent feedback, Agent alert | AGT |
| Reporting | Measure definitions, the daily case list and the measure snapshots published to Power BI. | 5 | Case list row, Queue measure, Measure definition, Measure snapshot, Measure publish | DP03, RPT |
| Total |  | 122 |  |  |

## Data products

| Data products |  |  |  |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|---|---|
| 14 data products. ACE is the system of record for seven, ingested from the source named; the Workbench is the system of record for the other seven. Each has one way in and one freshness. The 14 hold 97 of the 122 entities; OPS, AGT and RPT hold the other 25. |  |  |  |  |  |  |  |  |  |
| ID | Data product | What it holds | System of record | How it reaches the Workbench | Freshness | In ACE | Decisions it serves | Main users | Entities |
| DP01 | Account and arrears | Loan accounts with balances, interest, fees, days past due, bucket, classification, restructure flag and payments | ACE (ingested from ALS) | Read through recovery.v_ace_account, v_ace_payment, v_ace_aa_relation and v_ace_bucket_log. ACE ingests ALS daily; the Workbench loads nothing. | ACE end of day; the views carry the ACE business date | Yes: loan information and payments | D6 entry, D6 to D9 | Case owner, restructuring officer, write-off team member |  |
| DP02 | Customer and party | Customers, guarantors, co-borrowers and heirs, identity masked to the last four, contact points, consent and flags for vulnerability, death and bankruptcy | ACE (ingested from SCBPDM and the core bank) | Read through recovery.v_ace_customer, v_ace_contact, v_ace_ca_relation and v_ace_party_product. The Workbench holds only its own flags and consent in party_ext and contact_point_ext. | ACE end of day; consent and flags as they change in the Workbench | Yes: customer profile; party_product added by RWB-ACE-001 | All decisions | Case owner, hardship and vulnerability specialist, Compliance and PDPA officer |  |
| DP03 | Case and ownership | The case, its accounts and parties, status, stage, route, owner, queue, tasks, timers and deviations | Recovery Workbench | Held in the Workbench. Accounts and parties are linked by ACE business key to v_ace_account and v_ace_customer; no foreign key. | As it changes | New in the Workbench | All decisions | Case owner, team manager, capacity and workforce planner |  |
| DP04 | Treatment and offers | Restructures, settlements, deeds in lieu, buy-backs and guarantee claims, with terms, approval level and outcome | Recovery Workbench for the treatment; ACE (ingested from the core bank) for the restructure plan | Held in the Workbench; the plan reference, status and published calculation are read through recovery.v_ace_plan, and the credit result through v_ace_credit_decision. | As it changes in the Workbench; plan status from the ACE batch | Partly: restructure calculation; credit_decision added by RWB-ACE-001 | D5, D6 | Restructuring officer, guarantee officer, approvers |  |
| DP05 | Contact and promises | Every contact, letter, promise and hand-over on the case, in order, including the collections history from EFS | ACE (ingested from EFS) | Read through recovery.v_ace_efs_action and v_ace_efs_assignment. The Workbench writes its own contact, letter and promise entries to interaction. | ACE end of day; Workbench entries as they change | Yes: collection activity log | D6 entry, X6 | Case owner, phone and field collector, Conduct and QA officer |  |
| DP06 | Collateral and assets | Collateral, appraisals, assets held after repossession or transfer, listings and sale results | ACE (ingested from CCMS, SVAF, AMIS and RPS) | Read through recovery.v_ace_collateral, v_ace_collateral_detail, v_ace_asset, v_ace_npa_asset, v_ace_npa_sale and v_ace_valuation. Listings and sale results stay in the Workbench. | ACE weekly or monthly per source; listings as they change | Yes after RWB-ACE-001: collateral_detail, valuation, npa_asset and npa_sale are Tier 2 | D6, D8 | NPA and asset manager, sale officer, Head of NPA |  |
| DP07 | Legal events and cases | Notices and proof of delivery, lawsuits, court case numbers, hearings, judgments and enforcement | ACE (ingested from LIT and WIN) for the court record and the proof of delivery; Workbench for notices and enforcement | Read through recovery.v_ace_lawsuit, v_ace_hearing and v_ace_pod. Notices and enforcement actions are written to the Workbench and dispatched through WIN. | ACE end of day; Workbench entries as they change | Partly: litigation status; lawsuit, hearing and pod_receipt added by RWB-ACE-001 | D7 | Litigation officer, enforcement owner, law firm user |  |
| DP08 | Partner performance | Partners on the panel, work placed with each, results, fees and scorecards | Recovery Workbench | Held in the Workbench; partner results arrive through the partner portal. | As it changes | New in the Workbench | D7, D8 | Partner and agency manager, Head of Litigation |  |
| DP09 | Debt sale | Debt sale lots, the accounts in each lot, buyers, prices, approval and put-backs | Recovery Workbench | Held in the Workbench. Past lots are migrated once from the bank's debt sale files; nothing is loaded at run time. | As it changes | No: debt sale data not in ACE | D8.4 | Debt sale officer, Head of Asset Liquidity |  |
| DP10 | Documents and extracted fields | Documents against the case, the fields read from them, retention class and custody of originals | Recovery Workbench document hub | Held in the Workbench. The signature request and its status are read through recovery.v_ace_esign. | As it changes | New in the Workbench; esign_request added by RWB-ACE-001 | All decisions | Case owner, Credit Administration officer, Legal counsel |  |
| DP11 | Scores and route economics | Risk scores, expected return by route, estimated sale price and sale success rate, restructure scheme suggestions | ACE (ingested from COLLINS) | Read through recovery.v_ace_score. The Workbench loads nothing. | ACE end of day; monthly for some models | Yes: COLLINS scores; collins_score added by RWB-ACE-001 if ACE does not hold the model | D5, D6, D8, D9 | Case owner, Risk and model risk officer, center of excellence analyst |  |
| DP12 | Decision log | One entry per decision with the rule, model and agent versions, inputs, recommendation, approval, actions and outcome | Recovery Workbench | Held in the Workbench. | As it changes | New in the Workbench | Audit, testing, learning | Internal audit, Risk and model risk officer, center of excellence analyst |  |
| DP13 | Money and closure | Payments and proceeds matched to the case, write-off postings and recovery after charge-off | ACE (ingested from ALS and GL) | Read through recovery.v_ace_payment and v_ace_write_off; proceeds matching and the write-off decision stay in the Workbench. | ACE end of day for payments; monthly for GL | Partly: payments; gl_write_off added by RWB-ACE-001 | D6 to D9 | Write-off team member, Finance and CFO delegate |  |
| DP14 | Reference data | Rules, approval limits, lists of values, roles, permissions and letter templates, each versioned | Recovery Workbench | Held in the Workbench and versioned. Source codes and descriptions are read through v_ace_product, v_ace_branch, v_ace_efs_action_code, v_ace_holiday and v_ace_iam_group rather than loaded. | By versioned load | New in the Workbench; lists confirmed against ACE views | All decisions | Reference data administrator, data steward and data product owner |  |
| Total |  |  |  |  |  |  |  |  |  |

## Entities

| Entities |  |  |  |  |  |  |
|---|---|---|---|---|---|---|
| 122 entities: 88 Workbench tables, then the 4 extension tables, then the 30 ACE source views. Each names its subject area, data product, system of record and what it reads from ACE or holds itself. |  |  |  |  |  |  |
| Entity | Subject area | Data product | What it is | System of record | ACE | Fields |
| Recovery case | Case | DP03 Case and ownership | One recovery case per customer per product, from 90 days past due to close. | Workbench | Extend ACE Case | 33 |
| Case account | Case | DP03 Case and ownership | Links each loan account to the case it is recovered under. | Workbench | New | 6 |
| Case party | Case | DP03 Case and ownership | The role each party plays on a case. | Workbench | New | 6 |
| Deviation | Case | DP03 Case and ownership | A deviation X1 to X7 raised on a case. | Workbench | New | 10 |
| Queue | Work management | DP03 Case and ownership | A queue of work belonging to one team and one role. | Workbench | Extend ACE work queue | 10 |
| Assignment | Work management | DP03 Case and ownership | Who holds a case or a task and from when. | Workbench | Reuse ACE Assignee | 10 |
| Task | Work management | DP03 Case and ownership | A unit of work on a case: a CMMN human, customer, partner or decision task. | Workbench | New | 10 |
| Timer | Work management | DP03 Case and ownership | A running clock on a case: a service level, a legal period or an offer validity. | Workbench | New | 14 |
| Treatment | Treatment | DP04 Treatment and offers | A resolution put to the customer or carried out on the case, with its terms and outcome. | Workbench | New; restructure plans reuse ACE TDRCalculation | 21 |
| Guarantee claim | Treatment | DP04 Treatment and offers | A claim against a Thai Credit Guarantee Corporation guarantee or an insurer. | Workbench | New | 8 |
| Legal action | Legal | DP07 Legal events and cases | A notice, lawsuit, appeal, enforcement or bankruptcy action on a case. | ACE (ingested from LIT) for the court record; Workbench for the instruction | New | 14 |
| Notice | Legal | DP07 Legal events and cases | A demand, recall or statutory notice and its proof of delivery. | Workbench for the notice; ACE (ingested from WIN) for the proof of delivery | New | 14 |
| Hearing | Legal | DP07 Legal events and cases | A court hearing on a legal action. | Workbench | New | 6 |
| Partner | Partner | DP08 Partner performance | An outside firm the bank places work with. | Workbench | New | 7 |
| Partner instruction | Partner | DP08 Partner performance | Work placed with a partner on a case. | Workbench | New | 9 |
| Listing | Disposal and debt sale | DP06 Collateral and assets | An asset offered for sale, with its prices and rounds. | Workbench | New | 8 |
| Asset sale | Disposal and debt sale | DP06 Collateral and assets | The sale of an asset. | Workbench | New | 11 |
| Debt sale lot | Disposal and debt sale | DP09 Debt sale | A lot of accounts offered to debt buyers. | Workbench | New | 11 |
| Debt sale account | Disposal and debt sale | DP09 Debt sale | An account in a debt sale lot. | Workbench | New | 7 |
| Interaction | Interaction | DP05 Contact and promises | One entry in the interaction ledger: a contact, letter, promise, payment or hand-over. | Workbench | Extend ACE activity log | 29 |
| Document | Document | DP10 Documents and extracted fields | A document held against a case. | Workbench document hub | Extend ACE Attachment | 20 |
| Document field | Document | DP10 Documents and extracted fields | A field read from a document. | Workbench document hub | New | 8 |
| Document custody | Document | DP10 Documents and extracted fields | Each movement of an original document. | Workbench | New | 7 |
| Decision log entry | Decision and control | DP12 Decision log | One record per decision. Append only and hash chained. | Workbench | New | 22 |
| Proceeds | Money and closure | DP13 Money and closure | Money received on a case and what it was matched to. | Workbench | New | 9 |
| Write-off | Money and closure | DP13 Money and closure | A write-off of the balance on a case. | ACE (ingested from GL) for the posting; Workbench for the decision | New | 11 |
| Rule | Reference and access | DP14 Reference data | One versioned routing rule or sentry. | Workbench | New | 18 |
| Delegation limit | Reference and access | DP14 Reference data | An approval limit by decision, level, product and amount. | Workbench | New | 19 |
| List value | Reference and access | DP14 Reference data | A value in a list of values. | Workbench | New | 7 |
| Role | Reference and access | DP14 Reference data | A Workbench role, held as data. | Workbench | Extend ACE RBAC | 5 |
| Permission | Reference and access | DP14 Reference data | What a role may do in one capability area. | Workbench | Extend ACE RBAC | 5 |
| Template | Reference and access | DP14 Reference data | A letter or notice template. | Workbench | New | 14 |
| Data product | Reference and access | DP14 Reference data | One of the 14 data products, with its single system of record, owner and refresh cycle. | Workbench | New | 10 |
| Data product access | Reference and access | DP14 Reference data | Which role may read which data product, by version. | Workbench | New | 7 |
| Data product load | Loads and operations | OPS Loads and operations | The freshness stamp of a data product for one business date, written from v_ace_batch_status. | Workbench | Reads ACE batch status | 9 |
| Data contract | Loads and operations | OPS Loads and operations | A versioned data contract with one ACE source view or one outbound interface, confirmed by its system owner. | Workbench | New | 11 |
| Sys objects | Reference and access | DP14 Reference data | The metadata registry of entities: one row per object in the data dictionary. | Workbench | New | 7 |
| Sys fields | Reference and access | DP14 Reference data | The metadata registry of fields: the data dictionary held as data. | Workbench | New | 17 |
| Sys field version | Reference and access | DP14 Reference data | Each version of a field definition, kept when the definition changes. | Workbench | New | 5 |
| Case list row | Reporting | DP03 Case and ownership | One row of the daily case list per case account and business date, published to Power BI. | Workbench | New | 19 |
| Reconciliation result | Loads and operations | OPS Loads and operations | The daily reconciliation of the case list to v_ace_account by product group. | Workbench | New | 12 |
| Lake copy watermark | Loads and operations | OPS Loads and operations | How far a copy to the data lake has reached, for example the decision log copy. | Workbench | New | 6 |
| Retention rule | Reference and access | DP14 Reference data | How long rows of a table or a retention class are kept and what happens at the end, by version. | Workbench | New | 12 |
| Dp treatment | Treatment | DP04 Treatment and offers | The snapshot of each treatment for a business date in the DP04 data product. | Workbench | New | 18 |
| Dp guarantee claim | Treatment | DP04 Treatment and offers | The snapshot of each guarantee claim for a business date in the DP04 data product. | Workbench | New | 10 |
| Interface config | Loads and operations | OPS Loads and operations | The settings of one outbound file interface, by version. | Workbench | New | 13 |
| Outbound item | Loads and operations | OPS Loads and operations | One outbound file waiting to be sent, sent or in the exception queue. | Workbench | New | 10 |
| Processed event | Loads and operations | OPS Loads and operations | An event or work key a consumer has already processed, so a repeat is ignored and counted. | Workbench | New | 6 |
| Idempotency key | Loads and operations | OPS Loads and operations | The stored response of an API request sent with an Idempotency-Key header, kept 24 hours. | Workbench | New | 5 |
| Outbox event | Loads and operations | OPS Loads and operations | An application event or outbound work request written in the same transaction as the change. | Workbench | New | 9 |
| Outbox delivery | Loads and operations | OPS Loads and operations | The delivery of one outbox event to one consumer, with its retries. | Workbench | New | 9 |
| Feature flag | Loads and operations | OPS Loads and operations | A feature flag with its value per environment, owner and removal date. | Workbench | New | 11 |
| Feature flag change | Loads and operations | OPS Loads and operations | One change of a feature flag value in one environment. | Workbench | New | 6 |
| Job catalog | Loads and operations | OPS Loads and operations | A scheduled job with its owner, run book and expected duration. | Workbench | New | 9 |
| Efs ledger outcome | Reference and access | DP14 Reference data | Which EFS action codes enter the interaction ledger and on which channel. | Workbench | New | 4 |
| Case entry exclusion | Case | DP03 Case and ownership | An account at 90 days past due that an exclusion rule kept out of recovery on a business date. | Workbench | New | 6 |
| Queue member | Work management | DP03 Case and ownership | A person who works a queue, with personal capacity and skills, by version. | Workbench | New | 8 |
| Queue measure | Reporting | DP03 Case and ownership | One snapshot of a queue's counts, ageing and breaches, published when it reconciles to the case list. | Workbench | New | 11 |
| Parameter catalog | Reference and access | DP14 Reference data | The definition of every parameter and environment setting, with its owner and default. | Workbench | New | 15 |
| Parameter value | Reference and access | DP14 Reference data | An approved, dated value version of a parameter per environment and product group. | Workbench | New | 12 |
| Reference version | Reference and access | DP14 Reference data | One version of a reference or rule table, with its author, approver, checks and change checklist. | Workbench | New | 22 |
| Reference row | Reference and access | DP14 Reference data | One row of a reference table version held as data. | Workbench | New | 4 |
| Rule test case | Reference and access | DP14 Reference data | A test case of the rule table test harness, with its expected and actual result. | Workbench | New | 13 |
| Masking rule | Reference and access | DP14 Reference data | Which role sees which personal data field unmasked, by version. | Workbench | New | 7 |
| Role conflict | Reference and access | DP14 Reference data | A pair of roles one person may not hold together, by version. | Workbench | New | 7 |
| Partner user | Reference and access | DP14 Reference data | A partner user's identity bound to one partner firm and one partner role. | Workbench | New | 6 |
| Document type | Reference and access | DP14 Reference data | A document type, the fields extracted from it and its Legal and NPA sign-off, by version. | Workbench | New | 16 |
| Document checklist item | Reference and access | DP14 Reference data | A document type required or expected for a case stage and route, by checklist version. | Workbench | New | 10 |
| Case document check | Document | DP10 Documents and extracted fields | The latest document completeness check of a case against its checklist. | Workbench | New | 9 |
| Document hub parameter | Reference and access | DP14 Reference data | A document hub parameter value, by version. | Workbench | New | 8 |
| Document intake | Document | DP10 Documents and extracted fields | A file received by the document hub, from scan to OCR, classification, extraction, matching and review. | Workbench | New | 40 |
| Document text | Document | DP10 Documents and extracted fields | The OCR text of one page of an intake item. | Workbench | New | 6 |
| Retention action | Document | DP10 Documents and extracted fields | What the monthly retention job did with one document. | Workbench | New | 5 |
| Merge field | Reference and access | DP14 Reference data | A merge code a template may use and the field that supplies its value, by catalog version. | Workbench | New | 9 |
| Signature request | Document | DP10 Documents and extracted fields | A request for a party to sign a generated document, and its result. | Workbench | New | 11 |
| Approval | Decision and control | DP12 Decision log | An item waiting for approval, routed to the level the delegation of authority requires. | Workbench | New | 22 |
| Payment match rule | Reference and access | DP14 Reference data | A rule for matching a payment to a plan installment, by version. | Workbench | New | 13 |
| Measure definition | Reporting | RPT Reporting | The agreed definition of a reported measure, by version. | Workbench | New | 10 |
| Measure snapshot | Reporting | RPT Reporting | The value of one measure for a business date, product and dimension value. | Workbench | New | 12 |
| Measure publish | Reporting | RPT Reporting | Whether the day's dashboard data set was published or held after reconciling to the case list. | Workbench | New | 6 |
| Agent policy | Agent runtime | AGT Agent runtime | A version of an agent's policy: model, tools, autonomy, limits and fallback. | Workbench | New | 25 |
| Agent prompt | Agent runtime | AGT Agent runtime | A version of an agent's prompt text. | Workbench | New | 10 |
| Agent run | Agent runtime | AGT Agent runtime | One call of an agent or model, with its versions, checks, answer, cost and fallback. | Workbench | New | 25 |
| Agent sample | Agent runtime | AGT Agent runtime | One labeled subject in a versioned evaluation sample. | Workbench | New | 9 |
| Agent evaluation run | Agent runtime | AGT Agent runtime | One evaluation of an agent version against a sample. | Workbench | New | 16 |
| Agent evaluation | Agent runtime | AGT Agent runtime | The score of one approach on one label key in an evaluation run. | Workbench | New | 11 |
| Agent feedback | Agent runtime | AGT Agent runtime | A person's verdict on an agent answer. | Workbench | New | 6 |
| Agent alert | Agent runtime | AGT Agent runtime | A cost cap or drift alert raised for an agent. | Workbench | New | 9 |
| Party extension | Party | DP02 Customer and party | Workbench flags about an ACE customer: vulnerability, death override, bankruptcy and fraud. One row per person_key; no copy of the customer record. | Workbench | Extension table; keyed by ACE person_key | 12 |
| Contact point extension | Party | DP02 Customer and party | Consent and contact quality for an ACE phone, email or address. One row per contact_key and contact_type. | Workbench | Extension table; keyed by ACE phone_key, email_key or address_key | 14 |
| Account extension | Account and arrears | DP01 Account and arrears | Workbench state about an ACE account, such as an open dispute. One row per account_key. | Workbench | Extension table; keyed by ACE account_key | 9 |
| Valuation extension | Collateral and asset | DP06 Collateral and assets | The Workbench decision about an ACE appraisal: accepted, valuer, stale and age. One row per valuation_key. | Workbench | Extension table; keyed by ACE valuation_key | 14 |
| v_ace_account | Account and arrears | DP01 Account and arrears | Read-only view over the ACE account: balances, arrears, days past due, classification, restructure flag and the ACE business date. Replaces the former loan account copy. | ACE (ingested from ALS) | Read-only view | 42 |
| v_ace_payment | Account and arrears | DP01 Account and arrears | Read-only view over the ACE payment: amount, capital, interest and expense split, channel and payment date. Replaces the former account payment copy. | ACE (ingested from ALS) | Read-only view | 12 |
| v_ace_customer | Party | DP02 Customer and party | Read-only view over the ACE customer: name, identity masked to the last four, date of birth, status and profile. Replaces the former customer copy. | ACE (ingested from SCBPDM and the core bank) | Read-only view | 20 |
| v_ace_contact | Party | DP02 Customer and party | Read-only view over ACE phone, email and address, unioned behind a contact_type discriminator. Replaces the former contact point copy; values in full because notices need them. | ACE (ingested from SCBPDM) | Read-only view | 9 |
| v_ace_ca_relation | Party | DP02 Customer and party | Read-only view over the ACE borrower, guarantor and co-borrower relation, with the guarantee amount. | ACE (ingested from SCBPDM) | Read-only view | 5 |
| v_ace_aa_relation | Account and arrears | DP01 Account and arrears | Read-only view over the ACE parent and child account link. | ACE (ingested from ALS) | Read-only view | 2 |
| v_ace_collateral | Collateral and asset | DP06 Collateral and assets | Read-only view over the ACE collateral link: collateral number, asset, account, value and type. Replaces the former collateral copy. | ACE (ingested from CCMS) | Read-only view | 8 |
| v_ace_asset | Collateral and asset | DP06 Collateral and assets | Read-only view over the ACE asset: the collateral asset, its type and its address. Replaces the former asset copy. | ACE (ingested from AMIS and RPS) | Read-only view | 9 |
| v_ace_efs_action | Interaction | DP05 Contact and promises | Read-only view over the ACE collections action: action code, contact result, promise and outcome. Replaces the former collections history copy. | ACE (ingested from EFS) | Read-only view | 20 |
| v_ace_efs_action_code | Reference and access | DP14 Reference data | Read-only view over the ACE action code list: 1,106 values, with the English name and category. | ACE (ingested from EFS) | Read-only view | 3 |
| v_ace_efs_assignment | Interaction | DP05 Contact and promises | Read-only view over the ACE assignment and hand-over history, with the balance at each hand-over. | ACE (ingested from EFS) | Read-only view | 9 |
| v_ace_bucket_log | Account and arrears | DP01 Account and arrears | Read-only view over the ACE monthly bucket snapshot: bucket, past due amount and month start. | ACE (ingested from ALS) | Read-only view | 6 |
| v_ace_product | Reference and access | DP14 Reference data | Read-only view over the ACE product list: code, name, type and category. Source of the product and product code lists. | ACE (ingested from the core bank) | Read-only view | 5 |
| v_ace_branch | Reference and access | DP14 Reference data | Read-only view over the ACE branch list: code, name, address and phone. Source of the branch, business unit and region values. | ACE (ingested from the core bank) | Read-only view | 4 |
| v_ace_holiday | Reference and access | DP14 Reference data | Read-only view over the ACE holiday calendar, used for service levels and legal days. | ACE | Read-only view | 5 |
| v_ace_plan | Treatment | DP04 Treatment and offers | Read-only view over the ACE restructure plan: reference, status, booking, approval and the published calculation. | ACE (ingested from the core bank) | Read-only view | 18 |
| v_ace_batch_status | Loads and operations | OPS Loads and operations | Read-only view over the ACE batch record: source, business date, completion, row count and checksum. Drives the Workbench freshness stamp. | ACE | Read-only view | 9 |
| v_ace_valuation | Collateral and asset | DP06 Collateral and assets | Read-only view over the ACE appraisal: number, type, appraised and forced sale value, date. Replaces the former valuation copy. | ACE (ingested from SVAF) | Read-only view | 9 |
| v_ace_collateral_detail | Collateral and asset | DP06 Collateral and assets | Read-only view over the ACE collateral detail: title deed, plot, area, province, district, insurance and lien rank. Replaces the former collateral link copy. | ACE (ingested from CCMS) | Read-only view | 12 |
| v_ace_npa_asset | Collateral and asset | DP06 Collateral and assets | Read-only view over the ACE NPA asset: transfer in, book value, auction price and repossession dates. | ACE (ingested from AMIS and RPS) | Read-only view | 12 |
| v_ace_npa_sale | Disposal and debt sale | DP06 Collateral and assets | Read-only view over the ACE NPA sale: contract, sale price, taxes, fees and incentive. | ACE (ingested from AMIS) | Read-only view | 11 |
| v_ace_lawsuit | Legal | DP07 Legal events and cases | Read-only view over the ACE lawsuit: court case numbers, claim, filing, judgment and status. | ACE (ingested from LIT) | Read-only view | 13 |
| v_ace_hearing | Legal | DP07 Legal events and cases | Read-only view over the ACE hearing: date, type and next date. | ACE (ingested from LIT) | Read-only view | 7 |
| v_ace_pod | Legal | DP07 Legal events and cases | Read-only view over the ACE proof of delivery: notice reference, barcode, sent date and delivery status. | ACE (ingested from WIN) | Read-only view | 10 |
| v_ace_write_off | Money and closure | DP13 Money and closure | Read-only view over the ACE write-off posting: amount, posted date, responsibility and cost centre. | ACE (ingested from GL) | Read-only view | 9 |
| v_ace_score | Decision and control | DP11 Scores and route economics | Read-only view over the ACE score: model, version, score, estimate and route. Replaces the former score copy. | ACE (ingested from COLLINS) | Read-only view | 10 |
| v_ace_party_product | Party | DP02 Customer and party | Read-only view over the ACE customer product holding: product type and status. Replaces the former product holding copy. | ACE (ingested from SCBPDM) | Read-only view | 6 |
| v_ace_credit_decision | Treatment | DP04 Treatment and offers | Read-only view over the ACE credit decision: NLEADS reference, result, reason and decision date. | ACE (ingested from NLEADS) | Read-only view | 8 |
| v_ace_esign | Document | DP10 Documents and extracted fields | Read-only view over the ACE e-signature request: external reference, requested date and status. The signed file stays in the Workbench document hub. | ACE (ingested from EasyApp) | Read-only view | 7 |
| v_ace_iam_group | Reference and access | DP14 Reference data | Read-only view over the ACE group-to-role mapping, used at sign-in by the ACE common module. | ACE (ingested from Entra ID) | Read-only view | 4 |

## Relationships

| Relationships |  |  |  |  |
|---|---|---|---|---|
| 104 relationships. Each reads from the entity that holds the reference to the entity it refers to. A reference to a v_ace_* view is a business key with no foreign key. |  |  |  |  |
| Entity | Refers to | Cardinality | What the reference means | Subject area |
| Recovery case | v_ace_customer | Many to one | The borrower the case is opened for | Case |
| Recovery case | Queue | Many to zero or one | The queue the case is in | Case |
| Case account | Recovery case | Many to one | The recovery_case this record belongs to | Case |
| Case account | v_ace_account | Many to one | The ACE account this record belongs to, matched on the ACE business key with no foreign key | Case |
| Case party | Recovery case | Many to one | The recovery_case this record belongs to | Case |
| Case party | v_ace_customer | Many to one | The ACE customer this record belongs to, matched on the ACE business key with no foreign key | Case |
| Deviation | Recovery case | Many to one | The recovery_case this record belongs to | Case |
| Queue | Queue | Many to zero or one | Queue that receives overflow | Work management |
| Assignment | Recovery case | Many to one | The recovery_case this record belongs to | Work management |
| Assignment | Task | Many to zero or one | The task this record belongs to | Work management |
| Assignment | Queue | Many to zero or one | The queue the assignment placed the case in | Work management |
| Task | Recovery case | Many to one | The recovery_case this record belongs to | Work management |
| Timer | Recovery case | Many to one | The recovery_case this record belongs to | Work management |
| Timer | Task | Many to zero or one | The task this record belongs to | Work management |
| Timer | Treatment | Many to zero or one | The treatment a plan timer belongs to | Work management |
| Treatment | Recovery case | Many to one | The recovery_case this record belongs to | Treatment |
| Treatment | Decision log entry | Many to zero or one | The decision that approved it | Treatment |
| Guarantee claim | Recovery case | Many to one | The recovery_case this record belongs to | Treatment |
| Legal action | Recovery case | Many to one | The recovery_case this record belongs to | Legal |
| Legal action | Partner | Many to zero or one | The law firm instructed | Legal |
| Notice | Recovery case | Many to one | The recovery_case this record belongs to | Legal |
| Notice | Document | Many to zero or one | The generated notice | Legal |
| Notice | v_ace_customer | Many to zero or one | The ACE customer the notice is addressed to | Legal |
| Notice | Template | Many to zero or one | Template version the notice was generated from | Legal |
| Notice | Outbound item | Many to zero or one | WIN file the notice was last written to | Legal |
| Hearing | Legal action | Many to one | The legal_action this record belongs to | Legal |
| Partner instruction | Recovery case | Many to one | The recovery_case this record belongs to | Partner |
| Partner instruction | Partner | Many to one | The partner this record belongs to | Partner |
| Listing | v_ace_asset | Many to one | The asset this record belongs to, matched on the ACE business key with no foreign key | Disposal and debt sale |
| Asset sale | v_ace_asset | Many to one | The asset this record belongs to, matched on the ACE business key with no foreign key | Disposal and debt sale |
| Asset sale | Listing | Many to zero or one | The listing this record belongs to | Disposal and debt sale |
| Debt sale lot | Partner | Many to zero or one | Winning buyer | Disposal and debt sale |
| Debt sale account | Debt sale lot | Many to one | The debt_sale_lot this record belongs to | Disposal and debt sale |
| Debt sale account | v_ace_account | Many to one | The ACE account this record belongs to, matched on the ACE business key with no foreign key | Disposal and debt sale |
| Interaction | Recovery case | Many to one | The recovery_case this record belongs to | Interaction |
| Interaction | v_ace_customer | Many to zero or one | The ACE customer this record belongs to, matched on the ACE business key with no foreign key | Interaction |
| Interaction | Decision log entry | Many to zero or one | Decision log entry the entry records, for DECISION_TAKEN | Interaction |
| Interaction | Interaction | Many to zero or one | Entry this entry corrects | Interaction |
| Interaction | v_ace_contact | Many to zero or one | The contact point reached; the number or address is read in full from v_ace_contact and masked for display at E1-037 | Interaction |
| Interaction | Treatment | Many to zero or one | The treatment offered, for an OFFER entry | Interaction |
| Interaction | Proceeds | Many to zero or one | The proceeds matched, for a PAYMENT entry | Interaction |
| Document | Recovery case | Many to one | The recovery_case this record belongs to | Document |
| Document | v_ace_customer | Many to zero or one | The ACE customer this record belongs to, matched on the ACE business key with no foreign key | Document |
| Document | Document | Many to zero or one | The document row this version supersedes; empty for version 1 | Document |
| Document | Template | Many to zero or one | Template version a generated document was made from | Document |
| Document | Treatment | Many to zero or one | Treatment a generated document belongs to | Document |
| Document field | Document | Many to one | The document this record belongs to | Document |
| Document custody | Document | Many to one | The document this record belongs to | Document |
| Decision log entry | Recovery case | Many to zero or one | The recovery_case this record belongs to; empty only for access events (decision code AC-...) with no case | Decision and control |
| Decision log entry | Decision log entry | Many to zero or one | The entry this entry corrects | Decision and control |
| Proceeds | Recovery case | Many to one | The recovery_case this record belongs to | Money and closure |
| Proceeds | Treatment | Many to zero or one | The treatment this record belongs to | Money and closure |
| Proceeds | v_ace_payment | Many to zero or one | The ACE payment this record belongs to, matched on the ACE business key with no foreign key | Money and closure |
| Write-off | Recovery case | Many to one | The recovery_case this record belongs to | Money and closure |
| Write-off | Decision log entry | Many to zero or one | The decision_log_entry this record belongs to | Money and closure |
| Permission | Role | Many to one | The role this record belongs to | Reference and access |
| Case list row | Recovery case | Many to one | Case | Reporting |
| Case list row | v_ace_account | Many to one | The ACE account; unique with business_date | Reporting |
| Retention rule | Reference version | Many to zero or one | Reference version that brought the row | Reference and access |
| Dp treatment | Treatment | Many to one | The treatment copied; unique with business_date | Treatment |
| Dp treatment | Recovery case | Many to one | The case of the treatment | Treatment |
| Dp treatment | Decision log entry | Many to zero or one | The decision that approved the treatment | Treatment |
| Dp guarantee claim | Guarantee claim | Many to one | The guarantee claim copied; unique with business_date | Treatment |
| Dp guarantee claim | Recovery case | Many to one | The case of the claim | Treatment |
| Processed event | Outbox event | Many to zero or one | Outbox event of the first delivery, where the key came from an event | Loads and operations |
| Outbox event | Recovery case | Many to zero or one | The case the event belongs to; empty for events with no case; unique with case_seq | Loads and operations |
| Outbox delivery | Outbox event | Many to one | The outbox event delivered | Loads and operations |
| Outbox delivery | Task | Many to zero or one | The RESOLVE_OUTBOX_DELIVERY task raised when the delivery entered the exception queue | Loads and operations |
| Case entry exclusion | v_ace_account | Many to one | The account excluded; unique with business_date | Case |
| Queue member | Queue | Many to one | The queue | Work management |
| Queue measure | Queue | Many to one | The queue measured; unique with as_of | Reporting |
| Reference row | Reference version | Many to one | The reference version the row belongs to; unique with row_key | Reference and access |
| Partner user | Partner | Many to one | The firm the partner user works for | Reference and access |
| Document type | Reference version | Many to zero or one | Reference version that brought the row | Reference and access |
| Document checklist item | Reference version | Many to zero or one | Reference version that brought the row | Reference and access |
| Case document check | Recovery case | Many to one | Case checked; one row per case; unique | Document |
| Case document check | Outbox event | Many to zero or one | Event that triggered the last check, for repeat detection | Document |
| Document hub parameter | Reference version | Many to zero or one | Reference version that brought the row | Reference and access |
| Document intake | Partner | Many to zero or one | Partner that sent the file by SFTP | Document |
| Document intake | Recovery case | Many to zero or one | Case the item belongs to once known | Document |
| Document intake | Document | Many to zero or one | Document created from the item, or the uploaded document | Document |
| Document text | Document intake | Many to one | Intake item the page belongs to; unique with page_no | Document |
| Document text | Document | Many to zero or one | Document the page belongs to once attached | Document |
| Retention action | Document | Many to one | Document acted on; unique with run_month | Document |
| Retention action | Decision log entry | Many to zero or one | DOCRET decision log entry for an archive | Document |
| Signature request | Recovery case | Many to one | Case | Document |
| Signature request | Treatment | Many to zero or one | Treatment the agreement belongs to | Document |
| Signature request | Document | Many to one | Generated document sent for signature | Document |
| Signature request | v_ace_customer | Many to one | Signing party | Document |
| Signature request | Document | Many to zero or one | Signed copy or branch scan | Document |
| Approval | Recovery case | Many to one | The case | Decision and control |
| Approval | Delegation limit | Many to zero or one | Delegation row that covers the item | Decision and control |
| Approval | Decision log entry | Many to zero or one | Decision log entry of the outcome | Decision and control |
| Agent policy | Agent evaluation run | Many to zero or one | Evaluation run an autonomy step is based on | Agent runtime |
| Agent run | Recovery case | Many to zero or one | The case the run is for | Agent runtime |
| Agent run | Agent evaluation run | Many to zero or one | Evaluation run the run belongs to, if any | Agent runtime |
| Agent run | Decision log entry | Many to zero or one | Decision log entry written for the step that used the run | Agent runtime |
| Agent evaluation | Agent evaluation run | Many to one | Evaluation run the score belongs to | Agent runtime |
| Agent feedback | Agent run | Many to one | Agent run the feedback is on | Agent runtime |
| Agent feedback | Decision log entry | Many to zero or one | Decision log entry written for the feedback | Agent runtime |
| Party extension | v_ace_customer | Many to one | The ACE customer the flags belong to, matched on person_key; no foreign key | Party |
| Contact point extension | v_ace_contact | Many to one | The ACE phone, email or address the consent belongs to, matched on contact_key and contact_type; no foreign key | Party |
| Account extension | v_ace_account | Many to one | The ACE account the dispute state belongs to, matched on account_key; no foreign key | Account and arrears |
| Valuation extension | v_ace_valuation | Many to one | The ACE appraisal the decision belongs to, matched on valuation_key; no foreign key | Collateral and asset |

## Gaps

| Gaps and the assumptions taken |  |  |  |  |
|---|---|---|---|---|
| Where the data needed is not available today or waits on a bank decision. The model is built on the assumption shown. The ACE gaps section lists what the ACE team adds under RWB-ACE-001. |  |  |  |  |
| Gap | What is missing | Assumption the model takes | What it affects | Decision |
| G1 | ACE holds no appraisal and no title deed detail today. | ACE ingests SVAF and CCMS; valuation and collateral_detail are Tier 2 in RWB-ACE-001. Until they land, DP06 stays behind its feature flag. An appraisal past its age limit is flagged on the case and blocks the route decision until it is replaced. | DP06; D6 route, D8 floor price | DL43, DL06, DL12 |
| G2 | ACE holds the collateral asset, not the repossessed or purchased asset. | ACE ingests AMIS and RPS; npa_asset and npa_sale are Tier 2 in RWB-ACE-001. Until they land, the NPA screens stay behind their feature flag. | DP06; D8 disposal | DL43, DL06, DL12 |
| G3 | Debt sale data is not available in ACE. | Debt sale lots are built and held in the Workbench. Past lots are migrated once from the bank's debt sale files. | DP09; D8.4 debt sale | None |
| G4 | The Thai Credit Guarantee quota is not available in ACE. | The guarantee officer records the quota and the claim deadline on the case. The deadline drives a timer. | DP04; D6.5 guarantee claim | DL06 |
| G5 | The full loan history since the account opened is not available. | The model holds the ACE account at its current state and the monthly bucket snapshot. Routing does not need history before collections started. | DP01 | DL12 |
| G6 | How much EFS contact history ACE keeps, and for how long. | The contact outcomes the business lead names, for the period the account was in collections, are read through v_ace_efs_action. Nothing is copied into the Workbench. | DP05; D6 entry, X6 | DL29 |
| G7 | Where customer facts come from. | ACE ingests them from SCBPDM and the core bank batch; the Workbench reads v_ace_customer. DL20 is amended by D-RCV-35. | DP02 | DL20, D-RCV-35 |
| G8 | What counts as one case. | One case per customer per product, with the accounts linked through case account. | DP03; every entity linked to the case | DL17 |
| G9 | Systems that carry the case identifier. | The Workbench only. The ACE account_key joins the case to ACE and to other systems. | DP03; all inbound and outbound flows | DL21 |
| G10 | Thai names for fields, labels and list values. | Each list value carries an English and a Thai label. Thai labels are filled as they are approved. | DP14 lists of values; every screen | DL10 |
| G11 | Retention and masking per data product. | Every field marked as personal data is masked for every role except those the masking rules name. Identification numbers never leave ACE in clear; contact values are full in v_ace_contact because notices need them, and display masking is E1-037. Retention follows the bank schedule once received. | All data products | DL26 |
| G12 | Difference accepted between a view and its ACE source. | Zero. ACE ingestion refuses a batch that does not reconcile to its control totals, and the Workbench reconciles the case list to v_ace_account and the money movements to v_ace_payment and v_ace_write_off every day (REC-01 to REC-05). | All data products read from ACE views | DL25 |
| G13 | GL write-off postings are not in ACE today. | ACE ingests the GL file; gl_write_off is Tier 2 in RWB-ACE-001, read through v_ace_write_off and matched to the write-off decision. | DP13; D9 | DL43, DL12 |
| G14 | Work orders and operational status held in Salesforce are not available. | Not modeled. NPA work orders are raised as tasks on the case. | DP06; D8 | DL12 |
| ACE gaps |  |  |  |  |
| 14 ACE tables and 12 ACE columns are not in ACE today. They are raised once in RWB-ACE-001 and read through the 14 Section B views. |  |  |  |  |
| # | ACE object | Kind and columns | Source | Fields read |
| 1 | ace_batch_run | New table, 9 columns. The per-source business date, completion record, row count and checksum. | All sources | 0 |
| 2 | valuation | New table, 11 columns. Appraisal number, type, appraised and forced sale value, appraisal date. | SVAF | 5 |
| 3 | collateral_detail | New table, 15 columns. Title deed, plot, area, province, district, insured value, insurance expiry, lien rank. | CCMS | 9 |
| 4 | npa_asset | New table, 14 columns. Transfer in, book value, auction purchase price, repossession and stock dates. | AMIS, RPS | 8 |
| 5 | npa_sale | New table, 13 columns. Sale contract, sale price, transfer fee, taxes and incentive. | AMIS | 7 |
| 6 | lawsuit | New table, 15 columns. Court case numbers, claim, filing, judgment and litigation status. | LIT | 9 |
| 7 | hearing | New table, 9 columns. Hearing date, type and next date. | LIT | 3 |
| 8 | pod_receipt | New table, 12 columns. Notice reference, sent date, barcode, callback date, delivery status and sent type. | WIN | 5 |
| 9 | gl_write_off | New table, 11 columns. Write-off amount, posted date, responsibility centre, cost centre and GL product. | GL | 5 |
| 10 | collins_score | New table, 12 columns. Model, version, score, estimate, route and scored date. | COLLINS | 6 |
| 11 | party_product | New table, 7 columns. Customer product type and status. | SCBPDM | 4 |
| 12 | credit_decision | New table, 10 columns. NLEADS reference, credit result, reason and decision date. | NLEADS | 4 |
| 13 | esign_request | New table, 9 columns. Signature external reference, requested date and status. | EasyApp | 1 |
| 14 | iam_group | New table, 7 columns. Group-to-role mapping used at sign-in. | Entra ID | 1 |
| 15 | account | 7 new columns on an existing ACE table: business_unit, principal_outstanding, interest_outstanding, fees_outstanding, daily_bucket, settlement_booked_date, settlement_booked_amount. | ALS | 7 |
| 16 | customer | 3 new columns on an existing ACE table: party_type, id_type, segment. | SCBPDM | 3 |
| 17 | efs_action | 2 new columns on an existing ACE table: contact_result, action_contact_status. | EFS | 3 |
|  | Total: 14 new tables, 12 new columns | 154 columns in the 14 new tables, 12 on existing tables |  | 80 |
| Raised once in RWB-ACE-001. DL43 stays open until the ACE team lead accepts the scope and the 21 November date. |  |  |  |  |

## Key

| Key |  |  |
|---|---|---|
| What each term and value means. |  |  |
| Item | Term | Meaning |
| Term | Subject area | A group of entities about one business subject |
| Term | Data product | A set of entities with one system of record, one way into the Workbench and one freshness, published for use by decisions, screens and reports |
| Term | Entity | A thing the model holds a record of: a Workbench table, an extension table or an ACE source view |
| Term | System of record | The system whose value is correct when two systems differ |
| Value | Held in the Workbench | The Workbench is the system of record and writes the data itself |
| Value | ACE end of day | ACE ingests the source at the end of the business day; the Workbench reads the result through a v_ace_* view the next morning |
| Value | Reuse ACE | The entity exists in ACE and is read through a v_ace_* view as it is |
| Value | Extend ACE | The entity exists in ACE and the Workbench adds fields or states in its own table or extension table |
| Value | New | The entity is added in the recovery module |
| Value | Many to one | Every record refers to exactly one record of the other entity |
| Value | Many to zero or one | A record may refer to one record of the other entity or to none |
| Standard | ISO/IEC/IEEE 29148 | Requirements for data and information |
| Standard | Bank TSD section T3 | Metadata-driven data model: objects, fields and records, standard columns, lists of values and relationships |
| Term | ACE source view | A SELECT-only recovery.v_ace_* view over ACE source tables. The only read path from the recovery module into ACE |
| Term | Extension table | A Workbench 1:1 table keyed by an ACE business key. Holds Workbench flags and decisions about an ACE record, never a copy of it |
| Term | Business key | The ACE key a Workbench table stores to link to a view, for example account_key or person_key. No foreign key is created |
| Value | ACE (ingested from X) | ACE is the system of record; the named source lands in ACE through ACE ingestion, not through a Workbench load |
