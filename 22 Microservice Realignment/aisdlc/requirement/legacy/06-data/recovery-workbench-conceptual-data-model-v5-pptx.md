<!-- source: 06 Data/Recovery Workbench Conceptual Data Model v5.pptx -->
<!-- converted: 2026-11-16 from PPTX -->

> **Source:** `06 Data/Recovery Workbench Conceptual Data Model v5.pptx`  
> **Converted from:** PPTX

## Slide 1

SCB

COLLECTIONS AND RECOVERY TRANSFORMATION Recovery Workbench: conceptual data model

Henka Group, 28 October 2026 (C) Siam Commercial Bank and Henka Pte Ltd

## Slide 2

The data model on one page

2

Case 5 entities Recovery case, Case account, Case party, Deviation, and more

Work management 5 entities Queue, Assignment, Task, Timer, and more

Party 3 entities Party, Contact point, Party product

Account and arrears 2 entities Loan account, Account payment

Collateral and asset 4 entities Collateral, Account collateral, Valuation, Asset

Treatment 4 entities Treatment, Guarantee claim, Dp treatment, Dp guarantee claim

Legal 3 entities Legal action, Notice, Hearing

Partner 2 entities Partner, Partner instruction

Disposal and debt sale 4 entities Listing, Asset sale, Debt sale lot, Debt sale account

Interaction 2 entities Interaction, Collections history

Document 8 entities Document, Document field, Document custody, Case document check, and more

Decision and control 3 entities Decision log entry, Score, Approval

Money and closure 2 entities Proceeds, Write-off

Reference and access 26 entities Rule, Delegation limit, List value, Role, and more

108 entities in 14 subject areas and 14 data products, with 1256 fields

The recovery case is at the center. Every other entity is linked to a case, an account, a party or a reference list.

## Slide 3

Subject areas and what each holds

3

| Subject area | What it holds | Entities | Data products |
|---|---|---|---|
| Case | The recovery case, its owner, its status and route, and the accounts and parties linked to it. | 5 | DP03 |
| Work management | Queues, assignments, tasks and timers that move the case and hold it to service levels. | 5 | DP03 |
| Party | Customers, guarantors, co-borrowers and heirs, their role on the case and how to reach them. | 3 | DP02 |
| Account and arrears | Loan accounts with balances, arrears, days past due, classification and payments. | 2 | DP01 |
| Collateral and asset | Collateral securing the accounts, its valuation, and assets the bank holds after repossession or transfer. | 4 | DP06 |
| Treatment | Restructures, settlements, deeds in lieu, guarantee claims and their terms, approvals and outcomes. | 4 | DP04 |
| Legal | Notices, lawsuits, hearings, judgments and enforcement. | 3 | DP07 |
| Partner | Law firms, agencies, valuers, auction vendors and buyers, and the work placed with them. | 2 | DP08 |
| Disposal and debt sale | Asset listings and bids, debt sale lots, buyers and awards. | 4 | DP06, DP09 |
| Interaction | Every contact, letter, promise and hand-over on the case, in order. | 2 | DP05 |
| Document | Documents held against the case, the fields extracted from them, and custody of originals. | 8 | DP10 |
| Decision and control | One log entry per decision, with versions, inputs, recommendation, approval, actions and outcome. | 3 | DP12, DP11 |
| Money and closure | Payments and proceeds matched to the case, write-offs and recovery after charge-off. | 2 | DP13 |
| Reference and access | Rules, limits, lists of values, roles, permissions and templates, all versioned. | 26 | DP14 |

## Slide 4

Data products and where each comes from

4

| ID | Data product | System of record | How it reaches the Workbench | Freshness |
|---|---|---|---|---|
| DP01 | Account and arrears | Core bank (ALS) | COLLINS daily batch into the ACE database | End of day; in the Workbench the next morning |
| DP02 | Customer and party | SCBPDM and core bank | COLLINS daily batch into the ACE database | End of day; in the Workbench the next morning |
| DP03 | Case and ownership | Recovery Workbench | Held in the Workbench | As it changes |
| DP04 | Treatment and offers | Recovery Workbench; restructure plans in ACE | Held in the Workbench | As it changes |
| DP05 | Contact and promises | EFS before day 90; the Workbench after | COLLINS daily batch from EFS; held in the Workbench | End of day for EFS history; as it changes after |
| DP06 | Collateral and assets | CCMS, SVAF, AMIS, RPS | File load until a batch feed exists | Weekly or monthly today |
| DP07 | Legal events and cases | LIT for court records; the Workbench for instructions | COLLINS daily batch for litigation status; held in the Workbench | End of day for LIT status |
| DP08 | Partner performance | Recovery Workbench | Held in the Workbench; partner results through the partner portal | As it changes |
| DP09 | Debt sale | Recovery Workbench | Held in the Workbench | As it changes |
| DP10 | Documents and extracted fields | Recovery Workbench document hub | Held in the Workbench | As it changes |
| DP11 | Scores and route economics | COLLINS | COLLINS daily batch into the ACE database | End of day; monthly for some models |
| DP12 | Decision log | Recovery Workbench | Held in the Workbench | As it changes |
| DP13 | Money and closure | Core bank (ALS) and GL | COLLINS daily batch for payments; file load for GL | End of day for payments; monthly for GL |
| DP14 | Reference data | Recovery Workbench | Held in the Workbench | By versioned load |

## Slide 5

What ACE already holds

5

In ACE today: 3 DP01 Account and arrears Loan information DP02 Customer and party Customer profile and customer information DP11 Scores and route economics COLLINS scores

Partly in ACE today: 5 DP04 Treatment and offers Restructure calculation in ACE DP05 Contact and promises Collection activity log DP06 Collateral and assets SVAF by manual file; NPA not available DP07 Legal events and cases Litigation status DP13 Money and closure Payments in loan information

New in the Workbench: 5 DP03 Case and ownership Written by the Workbench DP08 Partner performance Written by the Workbench DP10 Documents and extracted fields Written by the Workbench DP12 Decision log Written by the Workbench DP14 Reference data Written by the Workbench

Not available: 1 DP09 Debt sale Debt sale data not available

ACE holds end of day data loaded through COLLINS. There is no real-time feed today.

## Slide 6

How the core entities connect

6

Recovery case

Document

Task

Decision log entry

Partner instruction

Deviation

Interaction

Treatment

Legal action

Asset

Collateral

Party

Case party

Case account

Loan account

A case has many parties, accounts, tasks, documents, decisions, contacts, treatments and legal actions. An account is secured by collateral, and an asset comes from collateral.

## Slide 7

What the Workbench takes from ACE

7

Reuse: 4 entities Used as ACE holds them Assignment Loan account Account payment Score

Extend: 9 entities ACE entity with recovery fields and states added Recovery case Queue Party Collateral Asset Interaction Document Role Permission

New: 95 entities Added in the recovery module Case account, Case party, Deviation, Task, Timer, Contact point, Account collateral, Valuation, Treatment, Guarantee claim, Legal action, Notice, Hearing, Partner, Partner instruction, Listing, Asset sale, Debt sale lot, Debt sale account, Document field, Document custody, Decision log entry, Proceeds, Write-off, Rule, Delegation limit, List value, Template, Data product, Data product access, Data product load, Data contract, Sys objects, Sys fields, Sys field version, Load run, Dq exception, Dq rule, Source field map, Source code map, Tracker inventory, Tracker row, Case list row, Collections history, Reconciliation result, Lake copy watermark, Retention rule, Dp treatment, Dp guarantee claim, Interface config, Interface run, Interface signoff, Outbound item, Processed event, Idempotency key, Outbox event, Outbox delivery, Feature flag, Feature flag change, Job catalog, Party product, Efs ledger outcome, Case entry exclusion, Queue member, Queue measure, Parameter catalog, Parameter value, Reference version, Reference row, Rule test case, Masking rule, Role conflict, Partner user, Document type, Document checklist item, Case document check, Document hub parameter, Document intake, Document text, Retention action, Merge field, Signature request, Approval, Payment match rule, Measure definition, Measure snapshot, Measure publish, Agent policy, Agent prompt, Agent run, Agent sample, Agent evaluation run, Agent evaluation, Agent feedback, Agent alert

## Slide 8

Rules every entity follows

8

| Rule | What it means |
|---|---|
| Held as metadata | Each entity is an object and each field a field definition, as in the bank TSD section T3. A field or a list value is added by a versioned load |
| Standard columns | Every record carries is_active, state, version, created_at, created_by, updated_at and updated_by |
| One system of record | Each entity names the system whose value is correct. Loaded data is read only in the Workbench |
| Reference data is versioned | Rules, limits, lists of values, roles and templates carry a version, a valid from date and the approver |
| Personal data is protected | Identity numbers are tokenized. Every field marked as personal data is masked unless the role is allowed to see it |
| The decision log is append only | Entries are never changed. Each entry carries the hash of the one before it |
| Every value has its age | Each loaded record carries the business date of the load, so a screen and a decision can show how old an input is |
| The account number is the join | The case identifier stays in the Workbench. Other systems are matched on the account number |

## Slide 9

Gaps and the assumptions taken

9

| Gap | What is missing | Assumption the model takes | Decision |
|---|---|---|---|
| G1 | Collateral records and appraisals reach ACE weekly or monthly by manual file. Daily appraisal data is not available. | A file load from CCMS and SVAF each week. An appraisal past its age limit is flagged on the case and blocks the route decision until replaced. | DL06, DL12 |
| G2 | Assets held after repossession or transfer (AMIS, RPS) are not in COLLINS. | A monthly file load from AMIS and a weekly file load from RPS until a batch feed exists. | DL06, DL12 |
| G3 | Debt sale data is not available in ACE. | Debt sale lots are built and held in the Workbench. Past lots are loaded once from the bank's debt sale files. | None |
| G4 | The Thai Credit Guarantee quota is not available in ACE. | The guarantee officer records the quota and the claim deadline on the case. The deadline drives a timer. | DL06 |
| G5 | The full loan history since the account opened is not available. | The model holds what COLLINS carries. Routing does not need history before collections started. | DL12 |
| G6 | How much EFS contact history comes into the interaction ledger. | The contact outcomes the business lead names, for the period the account was in collections, loaded at case entry and daily while the case is open. | DL29 |
| G7 | Where customer facts come from. | The customer profile ACE already receives through COLLINS from UDP, SCBPDM and the core bank batch. | DL20 |
| G8 | What counts as one case. | One case per customer per product, with the accounts linked through case account. | DL17 |

## Slide 10

Gaps and the assumptions taken, continued

10

| Gap | What is missing | Assumption the model takes | Decision |
|---|---|---|---|
| G9 | Systems that carry the case identifier. | The Workbench only. The account number joins the case to other systems. | DL21 |
| G10 | Thai names for fields, labels and list values. | Each list value carries an English and a Thai label. Thai labels are filled as they are approved. | DL10 |
| G11 | Retention and masking per data product. | Every field marked as personal data is masked for every role except those the masking rules name. Retention follows the bank schedule once received. | DL26 |
| G12 | Difference accepted between a load and its source. | Zero. A load that does not reconcile to its control totals is refused whole and the previous load stays in use. | DL25 |
| G13 | Write-off postings in the general ledger are not in COLLINS. | A monthly file from the GL is matched to the write-off record. | DL12 |
| G14 | Work orders and operational status held in Salesforce are not available. | Not modeled. NPA work orders are raised as tasks on the case. | DL12 |
