<!-- source: 15 ACE DB Alignment/Recovery Workbench ACE DB Alignment Change Register v1.md -->
<!-- converted: 2026-11-16 from Markdown (copied) -->

> **Source:** `15 ACE DB Alignment/Recovery Workbench ACE DB Alignment Change Register v1.md`  
> **Converted from:** Markdown (copied)

# Recovery Workbench ACE DB alignment change register

SCB Collections and Recovery. Henka Group, 15 November 2026.

(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Document | Recovery Workbench ACE DB Alignment Change Register v1 |
| Purpose | The decision record and the edit plan for re-basing the Workbench on the ACE database: no inbound source loads, read-only views, ACE-owned additions, Workbench-owned extension tables |
| Status | Signed off on 15 November 2026 (U1 to U5, 30 views, all 133 fields through ACE). Wave 1 delivered: STTM v4, LDM v7, Physical Schema v5, RWB-ACE-001 |
| Decisions | U1 to U5, recorded as D-RCV-35 |
| Decision owner | Recovery tech lead with the data architect; ACE team lead for RWB-ACE-001 and DL43 |
| Scope | 82 files, 332 existing stories, 2 new stories, 133 source fields |
| Frozen inputs produced with this register | ACE Data Tier Map v1.md, ACE Field Gap List v1.xlsx, ACE Source Views v1.sql, ACE Schema PostgreSQL v1.sql, ACE Schema Extract v1.csv, ACE DB Alignment Tracker v1.xlsx |
| Sources examined | ACE-data-schema_20261104.xlsx (62 tables, 547 columns); Physical Schema v4.sql (108 tables, 1,256 fields); LDM and Data Dictionary v6.xlsx (133 external fields); STTM v3.xlsx; Conceptual Data Model v5.xlsx; Decision Log v8.xlsx; ADR v1.md; all six story workbooks; TSD P1 v2 |

## 1. Why this change

The Workbench design today builds a separate recovery schema inside the ACE database and fills it with copies of source data. Eleven copy tables hold 121 fields of loan, payment, party, contact, collateral, valuation, asset, collections, product and score data. Nine more tables run the load: `load_run`, `dq_exception`, `dq_rule`, `source_field_map`, `source_code_map`, `interface_run`, `interface_signoff`, `tracker_inventory` and `tracker_row`, 116 fields. JOB-01 and JOB-09 move the data from the COLLINS staging feeds and the file loads.

The bank already runs ACE. ACE ingests account, payment, customer, address, phone, email, ca_relation, collateral, asset, efs_action, efs_assignment, bucket_log_snapshot, product and branch today, and it has case, SLA, holiday, audit, Quartz and Spring Batch tables. The Workbench is a module of ACE (ADR-001). Two copies of the same account row, one in ACE and one in the recovery schema, is a defect in waiting: they disagree, and the Workbench owns the one nobody else maintains.

The documents half-anticipate the change. The LDM has an ACE column, the Conceptual Data Model has an In ACE today column, CDM slide 7 and the TSD P1 model mark `loan_account` and `account_payment` as Reuse ACE and `party` and `collateral` as Extend. The physical schema, the STTM, the interface specifications, the jobs and the stories still build the copies.

This register finishes the move. The Workbench stops handling source data. It reads ACE through views, and it adds only new tables and columns.

## 2. The five decisions

| # | Decision | What it changes |
|---|---|---|
| U1 | No inbound source loads in the Workbench. All source data lands in the ACE DB through ACE's ingestion, including SVAF and CCMS, which ACE does not hold today. The Workbench only reads the ACE DB. | Deletes the load machinery and the inbound half of the interface estate. 20 tables leave the schema. |
| U2 | The ACE team owns the new ACE tables and columns for source data. One new story, RWB-ACE-001, lists every new table and column the Workbench needs. | Adds 14 tables and 12 columns to the ACE team's backlog, with an 80-row field appendix. |
| U3 | Workbench-owned fields that ACE lacks go into extension tables in the recovery schema. They are 1:1 tables keyed by ACE business keys. Existing ACE tables are never altered by the Workbench. | Adds 4 extension tables. Keeps the Workbench out of ACE's DDL. |
| U4 | Read path is read-only views. `recovery.v_ace_*` SELECT-only views sit over ACE tables and map names and types. There are no FK constraints into ACE tables, because ACE uses ON DELETE CASCADE on account. Boundary rule: the recovery module may read ACE only through these views. | Adds 30 views and the grant they need. Re-keys 14 foreign keys to business keys. |
| U5 | Excel and SharePoint trackers are removed from system scope. Retirement is handled in the Cutover plan. | Removes 2 tables and 3 stories from scope; adds a retirement procedure to Cutover. |

### 2.1 Assumption to confirm at the gate

AMIS and RPS (NPA assets), LIT (legal), WIN proof-of-delivery inbound, GL write-off inbound and COLLINS scores follow the same route as SVAF and CCMS: ACE ingests them, and they appear in RWB-ACE-001. That is the assumption this register is built on. If any one of them is not ingested by ACE, its fields leave the ACE story and become a Workbench staging problem again, which reopens U1 for that source.

At sign-off the bank also routed the last three sources through ACE rather than recording them by hand:

| Field | Source | ACE object added |
|---|---|---|
| `treatment.nleads_ref`, `credit_result`, `credit_result_reason`, `credit_result_at` | NLEADS | `credit_decision` (4 fields) |
| `signature_request.external_ref` | EasyApp | `esign_request` (1 field) |
| `role.entra_group` | Entra ID | `iam_group` (1 field) |

That takes the ACE story to 80 fields and leaves no external field entered by hand. The ACE team lead confirms the whole list at the gate, together with DL43.

## 3. Target data architecture

One line: **ACE holds the data, the Workbench holds the case, and a view joins them.**

| Tier | Owner | What it holds | Count |
|---|---|---|---:|
| 1 | ACE team, read only | ACE tables that exist today, read through a view and never altered | 22 tables, 16 views |
| 2 | ACE team | New ACE tables and columns for source data that ACE does not hold | 14 tables, 12 columns, 14 views |
| 3 | Workbench | 1:1 extension tables keyed by ACE business keys | 4 tables |
| 4 | Workbench | Case, workflow, treatment, legal, partner, debt sale, documents, decision log, reference, outbox, flags, agents | 88 tables |
| Removed | - | Source copies, load machinery and the 6 columns the ACE story absorbs | 20 tables, 243 fields |

The full table-and-column map is **Recovery Workbench ACE Data Tier Map v1.md**. The field-level list is **Recovery Workbench ACE Field Gap List v1.xlsx**. The view definitions that compile are **Recovery Workbench ACE Source Views v1.sql**.

### 3.1 Tier 2 - what the ACE team is asked to add

| Object | Kind | Columns | Source | Fields the Workbench reads |
|---|---|---:|---|---:|
| `ace_batch_run` | new table | 9 | all | 0 (drives freshness) |
| `valuation` | new table | 11 | SVAF | 5 |
| `collateral_detail` | new table | 15 | CCMS | 9 |
| `npa_asset` | new table | 14 | AMIS, RPS | 8 |
| `npa_sale` | new table | 13 | AMIS | 7 |
| `lawsuit` | new table | 15 | LIT | 9 |
| `hearing` | new table | 9 | LIT | 3 |
| `pod_receipt` | new table | 12 | WIN | 5 |
| `gl_write_off` | new table | 11 | GL | 5 |
| `collins_score` | new table | 12 | COLLINS | 6 |
| `party_product` | new table | 7 | SCBPDM | 4 |
| `credit_decision` | new table | 10 | NLEADS | 4 |
| `esign_request` | new table | 9 | EasyApp | 1 |
| `iam_group` | new table | 7 | Entra ID | 1 |
| `account` | 7 new columns | 7 | ALS | 7 |
| `customer` | 3 new columns | 3 | SCBPDM | 3 |
| `efs_action` | 2 new columns | 2 | EFS | 2 |
| **Total** | 14 tables, 12 columns | **166** | | **80** |

Every new table carries `source_system`, `business_date` and `loaded_at`, a business key with a unique constraint, and a primary key. The Workbench links to the business key only.

### 3.2 The read path and the two-migration rule

A view cannot be created over a table that does not exist. The views therefore ship in two parts:

- **Section A**, 16 views, 177 fields, over ACE tables that exist today. Ships with RWB-E1-069 as the next free sequence after the V0001 baseline.
- **Section B**, 14 views, 127 fields, over the Tier 2 additions. Ships the week RWB-ACE-001 lands. Until then the features that need them stay behind their flags.

This is the one place where the plan's estimate and the design differ: the plan said about 10 views, and the frozen list is 30. The reason is the boundary rule itself: one view per ACE object family, so a developer can be told which view to read and cannot wander into `public`. Merging them would save 15 objects and make the grant and the conformance test coarser. The recommendation is 26.

### 3.3 Personal data

| Field | Treatment |
|---|---|
| `customer.identification_number` | Never exposed in clear. `v_ace_customer` returns `id_no_masked` (last four) and `id_no_last4`. |
| `phone.phone_number`, `email.email`, `address.address` | Full value in `v_ace_contact`, because notices and calls need it. Display masking is E1-037 at the API. Every read is audited. |
| Tokenization at load | Removed. There is no load. E1-037 role masking replaces `id_no_token`. |

## 4. Field disposition

The LDM v6 holds 133 fields with an external source. Every one is resolved:

| Disposition | Fields | Meaning |
|---|---:|---|
| ACE reuse | 52 | Already in an ACE table. Named in the view; no new column. |
| ACE new | 80 | Not in ACE. RWB-ACE-001 asks the ACE team. |
| Recovery extension | 1 | `party.fraud_flag` becomes `recovery.party_ext.fraud_flag`. |
| Workbench | 0 | No external field is entered by hand. |
| **Total** | **133** | |

Distinct ACE columns for the 80 ACE-new fields: 79, because `efs_action.contact_result` serves both `interaction.contact_result` and `collections_history.contact_result`.

The carried examples, repeated in the LDM v7 and STTM v4:

| LDM field | Source | Read path v5 |
|---|---|---|
| `loan_account.days_past_due` | ALS `DELAY_DAYS` | `v_ace_account.days_past_due` from `public.account.delay_days` |
| `account_payment.payment_date` | ALS `Payment_Date` | `v_ace_payment.payment_date` from `recovery.ace_to_date(public.payment.pay_date)`; `pay_date` is varchar |
| `party.cif_no` | SCBPDM `CIF` | `v_ace_customer.cif_no` from `public.customer.person_key` |
| `collections_history.contact_at` | EFS | `v_ace_efs_action.contact_at` from `public.efs_action.action_timestamp` |

## 5. What leaves the physical schema

| Group | Tables | Fields |
|---|---|---:|
| Source copies | `loan_account`, `account_payment`, `party`, `contact_point`, `collateral`, `account_collateral`, `collections_history`, `party_product`, `valuation`, `score`, `asset` | 121 |
| Load machinery | `load_run`, `dq_exception`, `dq_rule`, `source_field_map`, `source_code_map`, `interface_run`, `interface_signoff`, `tracker_inventory`, `tracker_row` | 116 |
| Columns on retained tables | `treatment` 4, `signature_request` 1, `role` 1 - read from ACE now | 6 |
| **Total** | **20 tables** | **243** |

Kept and re-pointed:

- `interface_config` stays for outbound interfaces only.
- `data_product_load` stays as the freshness stamp and is sourced from `ace_batch_run`.
- `reconciliation_result` stays and reconciles the case list to `v_ace_account`.

### 5.1 The foreign keys, corrected

The plan says 23 foreign keys across 14 tables are re-pointed. The schema says something slightly different, and the difference matters to the edit:

- 23 foreign key constraints reference the 11 source-copy tables.
- They span 20 tables, not 14.
- 9 of them are on tables that leave with the copy (`account_payment`, `account_collateral` twice, `valuation` twice, `asset`, `score`, `party_product`, `contact_point`).
- The other 14 sit on 13 retained tables and are re-keyed to business keys with no foreign key.

The 14 are listed in the Tier Map section 5. One of them, `interaction.contact_point_id`, becomes `contact_key` holding a composite `contact_type:key`, because a contact point is now one of three ACE objects and the key must be unambiguous on its own.

## 6. What the governance documents record

### 6.1 D-RCV-35 (Decision Log v8 to v9)

> D-RCV-35 ruled: the Recovery Workbench takes no inbound source data. All source data lands in the ACE database through ACE's ingestion (U1); the ACE team owns the new ACE tables and columns, raised once in RWB-ACE-001 (U2); Workbench-only fields go into 1:1 extension tables keyed by ACE business keys and no existing ACE table is altered by the Workbench (U3); the recovery module reads ACE only through SELECT-only `recovery.v_ace_*` views, with no foreign key into ACE because ACE cascades deletes on `account` (U4); Excel and SharePoint trackers leave system scope and are retired through the Cutover plan (U5). This supersedes DT12, DL06 option A and DL12 option A, amends DL20 to name ACE as the route for customer facts, and amends D-RCV-29 because the sys_objects and sys_fields counts change.

- **Supersedes** DT12 (data through COLLINS), DL06 option A (daily batch through COLLINS for all Epic 1 and Epic 2 data), DL12 option A (read and write through ACE and COLLINS only).
- **Amends** DL20 (source of customer facts) to say the facts come from ACE, which ingests them from SCBPDM and the core bank.
- **Amends** D-RCV-29: the baseline dictionary becomes 122 `sys_objects` rows and 1,366 `sys_fields` rows instead of 108 and 1,256.

### 6.2 ADR-010 (ADR v1 to v2)

> **ADR-010 Read source data from the ACE database through read-only views.** Status: accepted. Supersedes ADR-005. The recovery module reads source data from the ACE database through `recovery.v_ace_*` views. It does not load, copy or transform source data. The ACE team owns every table and column the views read; the Workbench owns only its extension tables. Consequences: one copy of source data; the Workbench cannot start before the ACE additions land (DL43); no tokenization at load, so masking moves to the views and to E1-037; the load, DQ and tracker estate leaves scope. ADR-001 consequence updated: recovery takes ACE's data position, which is now an asset rather than a constraint.

### 6.3 ACE Architecture Decision v2 to v3

| Section | Edit |
|---|---|
| 1 How does data arrive | SVAF, CCMS, AMIS, RPS, LIT, WIN, GL, COLLINS scores and SCBPDM party product arrive through ACE ingestion, not through a Workbench load. |
| 4 A module reads only its own tables | Exception: the recovery module reads `recovery.v_ace_*` views, which read public ACE tables. No direct public read, no write. |
| 5 Data | The recovery module owns the case and the extension tables; ACE owns source data. |
| 7 Data | The entity list loses the copy tables and gains the views and extension tables. |

### 6.4 Open point and rulings

- **DL43** (new, open): does the ACE team accept the RWB-ACE-001 scope and its dates? Owner: ACE team lead. Needed by: 2026-11-21 for a 30 November release. Blocks: E1-069, E1-002, E1-016, E1-018, the whole recovery data engine.
- **Rulings v2**: mark the copy-table counts (44 tables, 533 fields, 108/1,256) superseded by D-RCV-35. Ruling R4 (definitions) holds; the systems of record are re-worded "ACE (ingested from X)".
- **Admin and Access Model v5**: remove the SY-DATALOAD actor; add the read-only ACE service identity.

## 7. The document edit list

82 file rows: 80 new versions and 2 new files. The plan said about 70; the difference is that a document published as both md and xlsx (or docx and pptx) is two files here, because a writer edits one artefact at a time.

| Folder | Files | L | M | S | Wave |
|---|---:|---:|---:|---:|---|
| 01 Decisions and governance | 4 | 0 | 1 | 3 | W2 |
| 02 Business architecture and process | 3 | 0 | 1 | 2 | W2 |
| 03 Requirements and specifications | 7 | 2 | 3 | 2 | W2 |
| 04 User stories | 19 | 2 | 10 | 7 | W1, W3, W4 |
| 05 Technical architecture | 17 | 8 | 5 | 4 | W2 |
| 06 Data | 17 | 6 | 5 | 6 | W1, W2 |
| 09 Testing and quality | 4 | 1 | 2 | 1 | W4 |
| 10 Policy, controls and compliance | 1 | 0 | 0 | 1 | W4 |
| 11 Delivery and operations | 7 | 2 | 3 | 2 | W4 |
| 12 Project communication | 3 | 1 | 2 | 0 | W5 |
| **Total** | **82** | **22** | **32** | **28** | |

Each row, with its size, wave, owner and status column, is in **Recovery Workbench ACE DB Alignment Tracker v1.xlsx**, sheet `Documents`. The register keeps the summary; the tracker is the working list.

The rule for every row: a new version in the home folder, the old version stays until sign-off, one writer per file, and an edit log returned to this register.

## 8. The story disposition

332 existing stories, plus 2 new.

| Family | Stories | Remove | Rewrite | Minor | No impact | New |
|---|---:|---:|---:|---:|---:|---:|
| Epic 1 | 67 | 8 | 13 | 21 | 25 | 1 |
| Technical enablers | 13 | 0 | 3 | 3 | 7 | 0 |
| Epic 2 | 35 | 1 | 6 | 16 | 12 | 0 |
| Epics 3 to 8 | 181 | 0 | 6 | 65 | 110 | 0 |
| Administration | 22 | 0 | 2 | 1 | 19 | 0 |
| Data migration | 14 | 2 | 4 | 8 | 0 | 0 |
| ACE team | - | - | - | - | - | 1 |
| **Total** | **332** | **11** | **34** | **114** | **173** | **2** |

159 stories are touched. The per-story list with entities today, the ACE action and a status column is the tracker's `Stories` sheet.

### 8.1 Count reconciliation against the plan

The named lists and the automated scan do not agree in every family. The scan is the list of record, because it reads the Entities column and the Gherkin of all 332 stories rather than a sample. The differences:

| Item | Plan | Reconciled | Why |
|---|---:|---:|---|
| Epic 1 removals | 9 | 8 | The plan's own list names eight: E1-003, 004, 005, 006, 009, 010, 012, 051. |
| Epic 1 and TE rewrites | 17 | 16 | The list names 16 (13 E1 plus 3 TE); the seventeenth is the new E1-069. |
| Epic 1 and TE minor | 12 | 24 | Eleven are named. The scan finds 13 more that mention JOB-0x, INT-0x or a tracker in Gherkin and need the same text edit. |
| Epic 2 minor | 17 | 16 | The plan names no individual rows; the scan finds 16 with a removed entity or load wording. |
| Epics 3 to 8 minor | ~74 | 65 | The scan counts stories that name a removed entity or a load job; 6 rewrites are separate. |
| Files | ~70 | 82 | Paired formats counted separately. |
| Views | ~10 | 30 | One view per ACE object family, for the boundary rule. |
| Re-pointed FKs | 23 across 14 tables | 23 across 20 tables; 14 survive in 13 | 9 sit on tables that leave with the copy. |

None of these changes the intent. Each is a bookkeeping correction so the Wave 3 agents edit the right files.

### 8.2 The two new stories

**RWB-ACE-001 - ACE DB additions for the Recovery Workbench** (owner: ACE team). It carries:

- The 14 new tables and 12 new columns, per source, with type, nullability, key and reference.
- The field appendix: 80 rows from the gap list, each with field ID, source field, type, frequency and the Workbench view that reads it.
- The batch business-date record `ace_batch_run` and its population rules.
- The SELECT grant for the recovery role on the listed tables.
- Acceptance criteria on population, on freshness, on not breaking the existing ACE reads, and on the migration being reversible.
- The date the Workbench needs it: 2026-11-21 for a 30 November release.

**RWB-E1-069 - Read-only ACE source views, grants and boundary rule** (owner: recovery squad). It carries:

- The 16 Section A views (over ACE tables that exist today), and the 14 Section B views (over the RWB-ACE-001 additions) as a second migration: 30 in all, per section 3.2.
- The 4 extension tables.
- The grant to the recovery service identity and the revoke from PUBLIC.
- TE-001 extended so the boundary test allows only `recovery.v_ace_*`.
- A view conformance test that fails the build if a recovery constraint references `public`, if a view does not compile, or if the recovery role can write.

## 9. Execution

| Wave | What | Work | Gate |
|---|---|---|---|
| 0 | This register, the Tier Map, the gap list, the views, the schema dump | Coordinator | **Sign-off on this register** |
| 1 | STTM v4 and gap sheet, LDM v7, Physical Schema v5, RWB-ACE-001, then verify | 4 agents plus 1 verify agent | Schema and LDM counts agree; views compile |
| 2 | Governance, architecture, requirements, data documents | 45 files, one owner each | Each returns an edit log |
| 3 | Stories: removals, rewrites, minor; build notes | 16 file owners, about 80 story fragments | One writer per file; assembly merges fragments |
| 4 | Test and delivery | 13 files | Traceability complete |
| 5 | Three verification agents, then index, control sheet, hub | 5 agents | No open defect in a live document |

One writer per output file. Every agent reads the same frozen inputs and never edits a file another agent owns. Each returns a short edit log: sections changed, IDs removed or added, open questions. The log is appended to this register.

## 10. Verification

### 10.1 What was run for this register

The ACE schema was generated from the workbook into PostgreSQL 17 and the views were compiled against it:

| Check | Result |
|---|---|
| ACE schema loads | 62 tables, 547 columns, 58 composite foreign keys, 60 primary keys, 22 unique constraints, 31 indexes |
| Section A views compile against the ACE schema on their own | 16 of 16 |
| Section B views compile after the Tier 2 probe | 14 of 14 |
| `v_ace_account.days_past_due` reads `account.delay_days` | 95 on the smoke row |
| `v_ace_payment.payment_date` casts `20261130` | 2026-11-30 |
| `v_ace_customer.id_no_masked` | `*********0123` from `1234567890123` |
| `v_ace_contact.contact_value_masked` | `******5678` from `0812345678` |
| Physical Schema v4 loads as written | **No** - see DEF-01 to DEF-03 |

### 10.2 What Wave 1 must run

- Physical Schema v5 in a PostgreSQL 17 container that first runs the ACE schema, then V0001, then the Section A views.
- Every `v_ace_*` view compiles; no constraint in `recovery` references `public.*`; `v_data_dictionary` returns `days_past_due` sourced from `public.account.delay_days`.
- `sys_objects` and `sys_fields` counts match LDM v7 exactly.
- The recovery role cannot select a public table directly, and cannot INSERT, UPDATE or DELETE on any table.

### 10.3 What Wave 5 must run

- Cross-document grep: no remaining `loan_account`, `account_payment`, `collections_history`, `party` as a table, `load_run`, `tracker_`, `JOB-01` or inbound `INT-0x` load wording, except in superseded text and this register.
- Every story's Entities column resolves to a Physical Schema v5 table or a `v_ace_*` view.
- Every removed story or test case has a row in this register's appendix.
- Every REQ-RDF in the RTM points at a live story or test.
- RWB-ACE-001 rows equal STTM v4 gap-sheet rows, 1:1.

## 11. Defects found while writing this register

| ID | Where | Defect | Fix |
|---|---|---|---|
| DEF-01 | Physical Schema v4.sql | No `data_product` seed rows, although D-RCV-29 and rulings R1 and R4 require 14. The file does not load: the first `sys_objects` insert fails the foreign key. | v5 seeds 14 rows before `sys_objects`, definitions from CDM v6. |
| DEF-02 | Physical Schema v4.sql | `data_product.refresh_cycle` is `varchar(10)`, but its comment and the LDM use "On change" and "By versioned load". | Widen to `varchar(30)` in v5. |
| DEF-03 | Physical Schema v4.sql | 33 `sys_objects` rows carry OPS, AGT or RPT and `data_product` is NOT NULL. Ruling R1 is not applied to v4. | Apply R1 in v5: nullable, 33 rows NULL, FK created. |
| DEF-04 | ACE workbook | `ace_case_accounts` and `batch_job_execution_params` carry no primary key. | No Workbench change; recorded so the conformance test does not assume one. |
| DEF-05 | Physical Schema v5 | 42 fields on retained tables still carry a source system and source field from the copy design (hearing, legal_action, notice, write_off, asset_sale, proceeds, dp_treatment, interaction, decision_log_entry, debt_sale_account, treatment, recovery_case). They mirror a Tier 1 or Tier 2 column and should either be dropped and read from the view, or declared a Workbench snapshot. | Wave 2 cleanup, one story at a time: the owning story drops the column and reads the view, or states why the snapshot is kept. Recorded, not blocking: the schema, the views and the dictionary counts are consistent. |
| DEF-06 | Physical Schema v5 | `case_list_row` was UNIQUE (business_date) and `case_entry_exclusion` was UNIQUE (business_date), which allow one row per day in the whole table rather than one per case account. | Fixed in v5: `case_list_row` is UNIQUE (business_date, case_id, account_no) and `case_entry_exclusion` is UNIQUE (business_date, account_key). Found by RWB-E1-002 and RWB-E1-018 while they were re-based. |
| DEF-07 | Physical Schema v5 | `dp_treatment` was UNIQUE (business_date) and `dp_guarantee_claim` was UNIQUE (business_date), which allow one stage-2 snapshot row per day in the whole table rather than one per treatment or claim. | Fixed in v5: `dp_treatment` is UNIQUE (business_date, treatment_id) and `dp_guarantee_claim` is UNIQUE (business_date, guarantee_claim_id). Found while RWB-E2-006 was checked against `v_ace_credit_decision`. |

DEF-01 to DEF-03 are pre-existing and would have blocked the build at V0001. They are fixed in Physical Schema v5 as part of Wave 1, not by a separate change.

## 12. Risks

| # | Risk | Likelihood | Effect | Mitigation |
|---|---|---|---|---|
| R1 | The ACE team does not accept RWB-ACE-001 or cannot deliver by 21 November | Medium | The 30 November release moves; E1-002, E1-016, E1-018 and the data engine cannot start | DL43 raised on the day of sign-off; a fallback scope of Tier 1 views plus the case list is costed but not recommended |
| R2 | A source is not ingested by ACE after all (AMIS, RPS, LIT, WIN, GL, COLLINS, NLEADS, EasyApp, Entra ID) | Medium | That source reopens U1 and needs a staging table and load in the Workbench | Confirm each source in DL43; the gap list names them one by one |
| R3 | ACE changes a column the views read | Low | A view breaks at deploy | The conformance test runs in the pipeline; the ACE team treats the view list as a contract |
| R4 | The dictionary count changes again after LDM v7 | Medium | D-RCV-29 and E1-001 AC1 disagree | The Wave 1 verify agent re-derives both counts from the same pair before either is signed |
| R5 | Masking in the view is read as a PDPA control on its own | Low | Audit finding | The register states the control is the grant plus E1-037 plus the audit log; Data Classification v4 repeats it |

## 13. Sign-off

| Role | Name | Decision | Date |
|---|---|---|---|
| Data architect | | Approves U1 to U5, the Tier Map, the 30-view list and the count re-base | 15 Nov 2026 |
| Recovery tech lead | | Approves D-RCV-35, ADR-010 and the edit plan | 15 Nov 2026 |
| ACE team lead | | Accepts the RWB-ACE-001 scope and dates (DL43) - pending gate meeting | |
| Product owner | | Approves the story removals and the scope change | 15 Nov 2026 |

Signed at the 15 November gate with three answers recorded: approve and start Wave 1; keep 30 views, one per ACE object family; route NLEADS, EasyApp and Entra ID through ACE rather than recording them by hand.

## Appendix A - the 11 stories that leave

| Story | Title | Later home |
|---|---|---|
| RWB-E1-003 | ALS daily extract load | ACE ingestion; content parked in Data Load Story Removals v1 |
| RWB-E1-004 | EFS extract load | ACE ingestion |
| RWB-E1-005 | Excel and SharePoint inventory | Cutover plan |
| RWB-E1-006 | Data quality rules v1 | ACE ingestion checks; the daily gate moves into E1-015 |
| RWB-E1-009 | CCMS and SVAF loads | ACE ingestion |
| RWB-E1-010 | Excel and SharePoint loads | Cutover plan |
| RWB-E1-012 | Retire local copies | Cutover plan |
| RWB-E1-051 | Legacy feed jobs on ADF and Control-M | ACE ingestion; no ADF job remains |
| RWB-E2-023 | Automated EFS file load | ACE ingestion |
| RWB-DM-001 | Migrate account and arrears | Not needed: the data is in ACE |
| RWB-DM-002 | Migrate customer and party | Not needed: the data is in ACE |

The parked content stays in `14 Story Updates/Recovery Workbench Data Load Story Removals v1.md`, marked obsolete with its new home. The Wave 3 removal agent updates that file.

## Appendix B - the 14 re-pointed foreign keys

| Table | Old column | New column | Old target |
|---|---|---|---|
| `recovery_case` | `primary_customer_id` | `primary_person_key` | `party` |
| `case_account` | `account_id` | `account_key` | `loan_account` |
| `case_party` | `party_id` | `person_key` | `party` |
| `notice` | `party_id` | `person_key` | `party` |
| `listing` | `asset_id` | `asset_key` | `asset` |
| `asset_sale` | `asset_id` | `asset_key` | `asset` |
| `debt_sale_account` | `account_id` | `account_key` | `loan_account` |
| `interaction` | `party_id` | `person_key` | `party` |
| `interaction` | `contact_point_id` | `contact_key` (composite: contact_type:key) | `contact_point` |
| `document` | `party_id` | `person_key` | `party` |
| `proceeds` | `account_payment_id` | `payment_code` | `account_payment` |
| `case_list_row` | `account_id` | `account_key` | `loan_account` |
| `case_entry_exclusion` | `account_id` | `account_key` | `loan_account` |
| `signature_request` | `party_id` | `person_key` | `party` |

## Appendix C - what this pack contains

| File | What it is |
|---|---|
| `Recovery Workbench ACE DB Alignment Change Register v1.md` | This document |
| `Recovery Workbench ACE Data Tier Map v1.md` | The frozen table and column map, tiers 1 to 4 and the removals |
| `Recovery Workbench ACE Field Gap List v1.xlsx` | 133 fields with disposition; 140 new ACE columns; the counts |
| `Recovery Workbench ACE Source Views v1.sql` | 30 view definitions, the helper functions, the grants and the conformance test |
| `ACE Schema PostgreSQL v1.sql` | The 62 ACE tables as runnable PostgreSQL DDL, generated from the workbook |
| `ACE Schema Extract v1.csv` | 547 rows, one per ACE column, for grep and agent use |
| `Recovery Workbench ACE DB Alignment Tracker v1.xlsx` | 82 documents, 334 stories, 9 decisions and 4 defects, with status columns |
| `ACE-data-schema_20261104.xlsx` | Copy of the ACE workbook this pack is built from |

## Appendix D - edit log

Filled by each agent as it returns. One row per file: agent, date, sections changed, IDs added or removed, open questions.

| Date | File | Agent | Sections | IDs | Open questions |
|---|---|---|---|---|---|
| 15 Nov 2026 | Wave 0 pack | Coordinator | All | U1 to U5, D-RCV-35, ADR-010, DL43, RWB-ACE-001, RWB-E1-069 | DL43; the AMIS, RPS, LIT, WIN, GL and COLLINS assumption |
| 15 Nov 2026 | Source to Target Mapping v4 | W1 agent | All tabs rebuilt; new ACE gaps tab | 133 rows, 80 gaps | none |
| 15 Nov 2026 | Logical Data Model v7 | W1 agent | Entities, Fields, Relationships, Sources, new ACE mapping tab | 122 entities, 1,366 fields | DEF-05 |
| 15 Nov 2026 | Physical Schema v5 | W1 agent | 20 tables removed, 4 extension tables, 30 views, dictionary reseeded | 92 tables, 122 objects, 1,366 fields | DEF-05 |
| 15 Nov 2026 | RWB-ACE-001 | W1 agent | New | 14 tables, 12 columns, 80 fields | ACE team estimate (DL43) |
