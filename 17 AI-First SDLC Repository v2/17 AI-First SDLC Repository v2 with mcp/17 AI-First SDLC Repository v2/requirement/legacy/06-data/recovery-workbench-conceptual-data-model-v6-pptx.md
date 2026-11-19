<!-- source: 06 Data/Recovery Workbench Conceptual Data Model v6.pptx -->
<!-- converted: 2026-11-16 from PPTX -->

> **Source:** `06 Data/Recovery Workbench Conceptual Data Model v6.pptx`  
> **Converted from:** PPTX

## Slide 1

SCB

COLLECTIONS AND RECOVERY TRANSFORMATION Recovery Workbench: conceptual data model

Henka Group, 15 November 2026 (C) Siam Commercial Bank and Henka Pte Ltd

## Slide 2

The data model on one page

2

Case 5 entities Recovery case, Case account, Case party, Deviation, Case entry exclusion

Work management 5 entities Queue, Assignment, Task, Timer, Queue member

Party 6 entities v_ace_customer, v_ace_contact, party_ext, and more

Account and arrears 5 entities v_ace_account, v_ace_payment, account_ext, and more

Collateral and asset 6 entities v_ace_collateral, v_ace_valuation, valuation_ext, and more

Treatment 6 entities Treatment, Guarantee claim, v_ace_plan, and more

Legal 6 entities Legal action, Notice, v_ace_lawsuit, v_ace_pod

Partner 2 entities Partner, Partner instruction

Disposal and debt sale 5 entities Listing, Asset sale, Debt sale lot, v_ace_npa_sale

Interaction 3 entities Interaction, v_ace_efs_action, v_ace_efs_assignment

Document 9 entities Document, Document intake, Signature request, v_ace_esign, and more

Decision and control 3 entities Decision log entry, Approval, v_ace_score

Money and closure 3 entities Proceeds, Write-off, v_ace_write_off

Reference and access 31 entities Rule, Delegation limit, List value, Role, and more

122 entities: 88 tables, 4 extension tables, 30 ACE views, 1366 fields

The recovery case is at the center. Every other entity is linked to a case, an account, a party or a reference list.

## Slide 3

Subject areas and what each holds

3

| Subject area | What it holds | Entities | Data products |
|---|---|---|---|
| Case | The recovery case, its owner, its status and route, and the accounts and parties linked to it. | 5 | DP03 |
| Work management | Queues, assignments, tasks and timers that move the case and hold it to service levels. | 5 | DP03 |
| Party | Customers, guarantors, co-borrowers and heirs, read from ACE with their contact points and flags. | 6 | DP02 |
| Account and arrears | Loan accounts and payments with balances, arrears, days past due and classification, read from ACE. | 5 | DP01 |
| Collateral and asset | Collateral, appraisals and assets, read from ACE, with the Workbench decision on each appraisal. | 6 | DP06 |
| Treatment | Restructures, settlements, deeds in lieu, guarantee claims and their terms, approvals and outcomes. | 6 | DP04 |
| Legal | Notices, lawsuits, hearings, judgments and enforcement. | 6 | DP07 |
| Partner | Law firms, agencies, valuers, auction vendors and buyers, and the work placed with them. | 2 | DP08 |
| Disposal and debt sale | Asset listings and bids, debt sale lots, buyers and awards. | 5 | DP06, DP09 |
| Interaction | Contacts, letters, promises and hand-overs: the ACE collections action plus the Workbench interaction ledger. | 3 | DP05 |
| Document | Documents held against the case, the fields extracted from them, and custody of originals. | 9 | DP10 |
| Decision and control | One log entry per decision, with versions, inputs, recommendation, approval, actions and outcome. | 3 | DP12, DP11 |
| Money and closure | Payments and proceeds matched to the case, write-offs and recovery after charge-off. | 3 | DP13 |
| Reference and access | Rules, limits, lists of values, roles and templates, with the ACE code lists read through views. | 31 | DP14 |

## Slide 4

Data products and where each comes from

4

| ID | Data product | System of record | How it reaches the Workbench | Freshness |
|---|---|---|---|---|
| DP01 | Account and arrears | ACE (ingested from ALS) | Read through v_ace_account and v_ace_payment | ACE end of day; views carry the business date |
| DP02 | Customer and party | ACE (ingested from SCBPDM and the core bank) | Read through v_ace_customer, v_ace_contact and v_ace_ca_relation | ACE end of day; consent as it changes |
| DP03 | Case and ownership | Recovery Workbench | Held in the Workbench; links by ACE business key | As it changes |
| DP04 | Treatment and offers | Workbench; ACE (ingested from the core bank) for the plan | Held in the Workbench; plan read through v_ace_plan | As it changes; plan status from ACE |
| DP05 | Contact and promises | ACE (ingested from EFS) | Read through v_ace_efs_action and v_ace_efs_assignment | ACE end of day; new entries as they change |
| DP06 | Collateral and assets | ACE (ingested from CCMS, SVAF, AMIS, RPS) | Read through six v_ace_* views; no file load | Weekly or monthly per source |
| DP07 | Legal events and cases | ACE (ingested from LIT, WIN); Workbench for notices | Read through v_ace_lawsuit, v_ace_hearing and v_ace_pod | ACE end of day; notices as they change |
| DP08 | Partner performance | Recovery Workbench | Held in the Workbench; partner portal results | As it changes |
| DP09 | Debt sale | Recovery Workbench | Held in the Workbench | As it changes |
| DP10 | Documents and extracted fields | Recovery Workbench document hub | Held in the Workbench; signature status through v_ace_esign | As it changes |
| DP11 | Scores and route economics | ACE (ingested from COLLINS) | Read through v_ace_score | ACE end of day; monthly for some models |
| DP12 | Decision log | Recovery Workbench | Held in the Workbench | As it changes |
| DP13 | Money and closure | ACE (ingested from ALS and GL) | Read through v_ace_payment and v_ace_write_off | End of day for payments; monthly for GL |
| DP14 | Reference data | Recovery Workbench | Held in the Workbench; codes read through v_ace_* lists | By versioned load |

## Slide 5

The four tiers and the read path

5

Tier 1: 22 ACE tables Read only, through 16 views Account and payment Customer, contact and relation Collateral and asset Collections action and assignment Product, branch and holiday Restructure plan and parent account

Tier 2: 14 tables, 12 columns The ACE team adds them, with 14 views valuation, collateral_detail npa_asset, npa_sale lawsuit, hearing, pod_receipt gl_write_off, collins_score party_product, credit_decision esign_request, iam_group, ace_batch_run

Tier 3: 4 extension tables Workbench flags, keyed by ACE key party_ext contact_point_ext account_ext valuation_ext One row per ACE record

Tier 4: 88 Workbench tables The case and what the Workbench writes Case, work management, treatment Legal, partner, debt sale Documents, decision log, agents Reference, outbox, flags No copy of source data

ACE holds the data, the Workbench holds the case, and a read-only recovery.v_ace_* view joins them. There is no load and no foreign key into ACE.

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

v_ace_asset

v_ace_collateral

v_ace_customer

Case party

Case account

v_ace_account

A case has many parties, accounts, tasks, documents, decisions, contacts, treatments and legal actions. Accounts, parties, collateral and assets are read from ACE views and linked by business key.

## Slide 7

What the Workbench reads and what it owns

7

ACE read: 30 views SELECT only, no foreign key v_ace_account, v_ace_payment, v_ace_customer, v_ace_contact, v_ace_ca_relation, v_ace_aa_relation, v_ace_collateral, v_ace_asset, v_ace_efs_action, v_ace_efs_action_code, v_ace_efs_assignment, v_ace_bucket_log, v_ace_product, v_ace_branch, v_ace_holiday, v_ace_plan, v_ace_batch_status, v_ace_valuation, v_ace_collateral_detail, v_ace_npa_asset, v_ace_npa_sale, v_ace_lawsuit, v_ace_hearing, v_ace_pod, v_ace_write_off, v_ace_score, v_ace_party_product, v_ace_credit_decision, v_ace_esign, v_ace_iam_group

Extension: 4 tables Workbench flags about an ACE record party_ext: person_key contact_point_ext: contact_key and type account_ext: account_key valuation_ext: valuation_key No copy of the ACE row

Workbench: 88 tables The case and everything the Workbench writes Case, work management, party and account state, treatment, legal, partner, disposal, interaction, document, decision log, money, reference, outbox, flags and agents

## Slide 8

Rules every entity follows

8

| Rule | What it means |
|---|---|
| Held as metadata | Each entity is an object and each field a field definition, as in the bank TSD section T3. A field or a list value is added by a versioned load |
| Standard columns | Every record carries is_active, state, version, created_at, created_by, updated_at and updated_by |
| One system of record | Each entity names the system whose value is correct. Source data is read from ACE through a view and never written by the Workbench |
| Reference data is versioned | Rules, limits, lists of values, roles and templates carry a version, a valid from date and the approver |
| Personal data is protected | Identification numbers never leave ACE in clear. Every field marked as personal data is masked unless the role is allowed to see it, and every read is audited |
| The decision log is append only | Entries are never changed. Each entry carries the hash of the one before it |
| Every value has its age | Each ACE row carries the business date of its batch, so a screen and a decision can show how old an input is |
| The account number is the join | The case identifier stays in the Workbench. Other systems are matched on the ACE account_key |

## Slide 9

Gaps and the assumptions taken

9

| Gap | What is missing | Assumption the model takes | Decision |
|---|---|---|---|
| G1 | ACE holds no appraisal or title deed detail today. | ACE ingests SVAF and CCMS; valuation and collateral_detail are Tier 2 in RWB-ACE-001. Until they land, DP06 stays behind its flag. A stale appraisal blocks the route decision. | DL43, DL06, DL12 |
| G2 | ACE holds the collateral asset, not the repossessed one. | ACE ingests AMIS and RPS; npa_asset and npa_sale are Tier 2 in RWB-ACE-001. Until they land, the NPA screens stay behind their flag. | DL43, DL06, DL12 |
| G3 | Debt sale data is not available in ACE. | Debt sale lots are built and held in the Workbench. Past lots are migrated once from the bank's debt sale files. | None |
| G4 | The Thai Credit Guarantee quota is not available in ACE. | The guarantee officer records the quota and the claim deadline on the case. The deadline drives a timer. | DL06 |
| G5 | The full loan history since the account opened is not available. | The model holds the ACE account at its current state and the monthly bucket snapshot. Routing does not need history before collections started. | DL12 |
| G6 | How much EFS contact history ACE keeps. | The outcomes the business lead names, for the period in collections, are read through v_ace_efs_action. Nothing is copied. | DL29 |
| G7 | Where customer facts come from. | ACE ingests them from SCBPDM and the core bank; the Workbench reads v_ace_customer. DL20 is amended. | DL20, D-RCV-35 |
| G8 | What counts as one case. | One case per customer per product, with the accounts linked through case account. | DL17 |

## Slide 10

Gaps and the assumptions taken, continued

10

| Gap | What is missing | Assumption the model takes | Decision |
|---|---|---|---|
| G9 | Systems that carry the case identifier. | The Workbench only. The ACE account_key joins the case to other systems. | DL21 |
| G10 | Thai names for fields, labels and list values. | Each list value of a closed list carries an English and a Thai label. Thai labels are filled as they are approved. | DL10 |
| G11 | Retention and masking per data product. | Every field marked as personal data is masked for every role except those the masking rules name. Identification numbers never leave ACE in clear. Retention follows the bank schedule once received. | DL26 |
| G12 | Difference accepted between a view and its source. | Zero. ACE ingestion refuses a batch that does not reconcile to its control totals; the Workbench runs REC-01 to REC-05 daily. | DL25 |
| G13 | GL write-off postings are not in ACE today. | ACE ingests the GL file; gl_write_off is Tier 2 in RWB-ACE-001, read through v_ace_write_off and matched to the write-off decision. | DL43, DL12 |
| G14 | Work orders and operational status held in Salesforce are not available. | Not modeled. NPA work orders are raised as tasks on the case. | DL12 |
