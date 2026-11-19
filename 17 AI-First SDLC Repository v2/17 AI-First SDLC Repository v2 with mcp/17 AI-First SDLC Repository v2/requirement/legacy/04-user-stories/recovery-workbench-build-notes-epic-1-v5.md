<!-- source: 04 User stories/Recovery Workbench Build Notes Epic 1 v5.md -->
<!-- converted: 2026-11-16 from Markdown (copied) -->

> **Source:** `04 User stories/Recovery Workbench Build Notes Epic 1 v5.md`  
> **Converted from:** Markdown (copied)

# Recovery Workbench build notes, Epic 1

SCB Collections and Recovery. Henka Group, 15 November 2026.

(C) Siam Commercial Bank and Henka Pte Ltd

These notes follow the 71 stories of Recovery Workbench User Stories Epic 1 v8. Version 4 walked every flow step, and most of those steps were load or job steps. The ACE re-base of 15 November 2026 (D-RCV-35, ADR-010) removed that estate: the Workbench takes no inbound source data, ACE ingests every source, and the recovery module reads ACE only through the 30 SELECT-only `recovery.v_ace_*` views. In this version each story carries four notes in place of the old steps.

| Note | What it answers |
|---|---|
| View | Which views or Workbench tables the story reads, and what it takes from each |
| Grant | Which role holds which privilege, and what the story may not do |
| Freshness | Which data product the read belongs to, how its business date and stamp are set, and what a stale product does |
| Boundary | Where the module boundary falls and which rule fails the build when a class crosses it |

The story remains the specification. Where these notes and the story differ, the story governs. Section 13 of each story is its solution plan and section 16 its tests; where version 4 described a Workbench step that the re-base did not change, that section still carries it, and where it described a load or a job, the four notes replace it. RWB-E1-069 owns the view list, the grants and the view conformance test. RWB-ACE-001 owns the 14 Tier 2 tables and the 12 columns that Section B needs, and nothing in the Workbench creates or alters them.

## The 30 views and their sources

The 16 Section A views ship in V0002 and read the 21 ACE tables that exist today. The 14 Section B views ship in V0003 and read the tables that RWB-ACE-001 adds. Together they hold 304 columns, each with a dictionary row in the 122-object, 1,366-field dictionary of V0001.

| View | ACE source | Fields | Section |
|---|---|---:|---|
| `v_ace_account` | account | 42 | A |
| `v_ace_payment` | payment | 12 | A |
| `v_ace_customer` | customer | 20 | A |
| `v_ace_contact` | phone, email, address | 9 | A |
| `v_ace_ca_relation` | ca_relation | 5 | A |
| `v_ace_aa_relation` | aa_relation | 2 | A |
| `v_ace_collateral` | collateral | 8 | A |
| `v_ace_asset` | asset | 9 | A |
| `v_ace_efs_action` | efs_action | 20 | A |
| `v_ace_efs_action_code` | efs_action_code | 3 | A |
| `v_ace_efs_assignment` | efs_assignment | 9 | A |
| `v_ace_bucket_log` | bucket_log_snapshot | 6 | A |
| `v_ace_product` | product | 5 | A |
| `v_ace_branch` | branch | 4 | A |
| `v_ace_holiday` | bot_holiday | 5 | A |
| `v_ace_plan` | ace_case, cfsc_mg_ssme_tdr_case, tdr_calculation, ai_recommended_plan | 18 | A |
| `v_ace_batch_status` | ace_batch_run | 9 | B |
| `v_ace_valuation` | valuation | 9 | B |
| `v_ace_collateral_detail` | collateral_detail | 12 | B |
| `v_ace_npa_asset` | npa_asset | 12 | B |
| `v_ace_npa_sale` | npa_sale | 11 | B |
| `v_ace_lawsuit` | lawsuit | 13 | B |
| `v_ace_hearing` | hearing | 7 | B |
| `v_ace_pod` | pod_receipt | 10 | B |
| `v_ace_write_off` | gl_write_off | 9 | B |
| `v_ace_score` | collins_score | 10 | B |
| `v_ace_party_product` | party_product | 6 | B |
| `v_ace_credit_decision` | credit_decision | 8 | B |
| `v_ace_esign` | esign_request | 7 | B |
| `v_ace_iam_group` | iam_group | 4 | B |

## The grants

Two database roles carry the read path. Their names are fixed in the Environment and Deployment Design, and no story invents a third.

| Role | Holds | On what | Set by |
|---|---|---|---|
| `ace_view_owner` | USAGE and SELECT | The 21 Section A tables and the 14 Section B tables in `public`; owner of the 30 views | V0002 and V0003 (RWB-E1-069), with the SELECT on the Tier 2 tables granted to it by RWB-ACE-001 |
| `recovery_svc` | USAGE on `recovery` and SELECT on each view | The 30 views only; no privilege of any kind in `public` | V0002 for Section A, V0003 for Section B |
| `recovery_svc` | DML on the Workbench tables | The 92 tables of schema `recovery` | V0001 (RWB-E1-001) |
| `PUBLIC` | Nothing | Nothing | `REVOKE ALL ON ALL TABLES IN SCHEMA recovery FROM PUBLIC` in V0002 |

No view takes an INSERT, UPDATE, DELETE or TRUNCATE. A story that changes a Workbench decision writes its own table; a story that appears to change an ACE record writes an extension table keyed by the ACE business key.

## Freshness

A product is fresh when ACE reports its batch for the business date COMPLETE. RWB-E1-015 writes one `data_product_load` row per product per business date from `v_ace_batch_status`, and the `ace_batch_run` record that RWB-ACE-001 adds carries the business date, the status and the record count. A read that finds no COMPLETE batch keeps the last good business date, marks the product stale and raises MSG-P1-001. The Workbench products (DP03, DP04, DP08, DP09, DP10, DP12 and DP14) are stamped from their own last committed write, because no ACE batch produces them.

| Product | Data | Cycle | Expected by |
|---|---|---|---|
| DP01 | Account and arrears | DAILY | 08:00 |
| DP02 | Customer and party | DAILY | 08:00 |
| DP03 | Case and ownership | ON_CHANGE | As it changes |
| DP04 | Treatment and offers | ON_CHANGE | As it changes |
| DP05 | Contact and promises | DAILY | 08:00 |
| DP06 | Collateral and assets | WEEKLY | MON 08:00 |
| DP07 | Legal events and cases | DAILY | 08:00 |
| DP08 | Partner performance | ON_CHANGE | As it changes |
| DP09 | Debt sale | ON_CHANGE | As it changes |
| DP10 | Documents and extracted fields | ON_CHANGE | As it changes |
| DP11 | Scores and route economics | DAILY | 08:00 |
| DP12 | Decision log | ON_CHANGE | As it changes |
| DP13 | Money and closure | DAILY | 08:00 |
| DP14 | Reference data | ON_CHANGE | As it changes |

## The boundary

The boundary has four parts, and each one fails loudly.

- **No copy.** The recovery schema holds no ACE source table. The 88 Workbench tables hold Workbench records; the four extension tables hold a Workbench decision about an ACE record; the 30 views are the only read of ACE data.
- **No constraint into `public`.** No foreign key, check or unique constraint in `recovery` names a table or type outside it, because ACE cascades deletes on `account`. A link is a varchar(255) business key with no foreign key.
- **No direct read.** Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table. The allowed objects are the 30 view names in `recovery-modules.yaml`, not a literal list in the test.
- **No write to a view.** `recovery_svc` holds SELECT only; the view conformance test of RWB-E1-069 fails if it finds a write privilege or a privilege in `public`.

## What this version removes from version 4

| Removed | Why | Where it went |
|---|---|---|
| RWB-E1-003 ALS daily extract load | ACE ingests ALS | ACE ingestion; the Workbench reads `v_ace_account` and `v_ace_payment` |
| RWB-E1-004 EFS extract load | ACE ingests EFS | ACE ingestion; the Workbench reads `v_ace_efs_action` |
| RWB-E1-005 Excel and SharePoint inventory | No tracker estate to inventory | Cutover plan |
| RWB-E1-006 Data quality rules v1 | ACE runs the ingestion checks | ACE ingestion; the daily gate is in RWB-E1-015 |
| RWB-E1-009 CCMS and SVAF loads | ACE ingests CCMS and SVAF | ACE ingestion; `v_ace_collateral`, `v_ace_valuation` and Section B |
| RWB-E1-010 Excel and SharePoint loads | No tracker estate to load | Cutover plan |
| RWB-E1-012 Retire local copies | No local copy to retire | Cutover plan |
| RWB-E1-051 Legacy feed jobs on ADF and Control-M | No ADF job remains | ACE ingestion |

The job steps that remain are Workbench jobs: allocation, rebalancing, the letter and notice runs, OCR and the agent runs. Every one of them reads its source through a view and writes only a Workbench table. The pipeline steps that remain are migrations, the dictionary conformance test, the view conformance test, the boundary test and the PDPA lint.

## RWB-E1-001 Recovery tables for the 14 data products

Module: P1 Recovery data engine

**View.** No view. The story creates the 92 tables of Physical Schema v5, `data_product`, `sys_objects` and `sys_fields`; the 30 views arrive next in V0002 and V0003 (RWB-E1-069).

**Grant.** V0001 gives the recovery service role DML on the Workbench tables and nothing on a view; no `GRANT` on `public` and no `GRANT SELECT ON ALL TABLES`.

**Freshness.** All 14 products: DP01, DP02, DP05, DP07, DP11 and DP13 DAILY by 08:00, DP06 WEEKLY by Monday 08:00, and the Workbench products DP03, DP04, DP08, DP09, DP10, DP12 and DP14 ON_CHANGE as they change. RWB-E1-015 stamps `data_product_load` from `v_ace_batch_status`; a product with no COMPLETE batch keeps its last good business date, is marked stale and raises MSG-P1-001.

**Boundary.** v4 created a 43-table copy schema and seeded 108 objects and 1,256 fields. v5 creates the 92 tables, the four extension tables and the 122-object, 1,366-field dictionary, and leaves every source read to RWB-E1-069. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

## RWB-E1-002 Case list v1 with case ID, owner and queue

Module: P1 Recovery data engine

**View.** `v_ace_account` for balance and days past due, `v_ace_efs_action` for the last contact, `v_ace_batch_status` for the business date of the ACE batch; `case_account`, `case_list_row` and `recovery_case` come through `CaseQueryApi`.

**Grant.** No change. `recovery_svc` holds SELECT on the views named above from V0002 (RWB-E1-069) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP01 Account and arrears, DAILY, expected 08:00. RWB-E1-015 stamps `data_product_load` from `v_ace_batch_status`; a product with no COMPLETE batch keeps its last good business date, is marked stale and raises MSG-P1-001.

**Boundary.** v4 steps 2, 3 and 5 built a `load_run` row, called `LoadRunQuery.completedLoad` and joined `loan_account`. The table is gone: the completeness check is a read of `v_ace_batch_status`, and the join is to `v_ace_account`. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 enforces the view-only read, and the Section B read stays behind its flag until RWB-ACE-001 is deployed and V0003 applies (DL43).

## RWB-E1-007 Integration adapters for outbound files

Module: P2 Integration

**View.** `v_ace_account` for the account key, `v_ace_contact` for the contact key and channel, `v_ace_batch_status` for the date; writes `interface_config`, `outbound_item`, `outbox_event`, `outbox_delivery`, `processed_event`, `debt_sale_account` and `recovery_case`.

**Grant.** No change. `recovery_svc` holds SELECT on the views named above from V0002 (RWB-E1-069) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP01 Account and arrears, DAILY, expected 08:00; DP05 Contact and promises, DAILY, expected 08:00. RWB-E1-015 stamps `data_product_load` from `v_ace_batch_status`; a product with no COMPLETE batch keeps its last good business date, is marked stale and raises MSG-P1-001.

**Boundary.** v4 built the inbound file loads INT-10, INT-11 and INT-15 and the outbound interface INT-14. v5 keeps the outbound adapter, the outbox and the contract tests; the inbound loads are gone, and the adapter writes Workbench outbound files only. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 enforces the view-only read, and the Section B read stays behind its flag until RWB-ACE-001 is deployed and V0003 applies (DL43).

## RWB-E1-008 Decision log store v1, append only and hash chained

Module: P7 Decision center and log

**View.** No view. The story owns `decision_log_entry` and reads no ACE source.

**Grant.** No view in this story. `recovery_svc` holds DML on the Workbench tables it uses (V0001) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP12 Decision log, ON_CHANGE as it changes. A Workbench product is stamped from its last committed write, not from an ACE batch, so no ACE clock makes it stale.

**Boundary.** No change of substance. The entry carries the business keys of the ACE records it names, never a copy of an ACE column. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

## RWB-E1-011 Reconciliation and data quality report

Module: P1 Recovery data engine

**View.** `v_ace_account`, `v_ace_payment`, `v_ace_plan`, `v_ace_customer`, `v_ace_contact`, `v_ace_asset` and `v_ace_batch_status` for the reconciliation; writes `reconciliation_result`, `case_list_row` and the case exceptions.

**Grant.** No change. `recovery_svc` holds SELECT on the views named above from V0002 (RWB-E1-069) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP01 Account and arrears, DAILY, expected 08:00; DP05 Contact and promises, DAILY, expected 08:00; DP06 Collateral and assets, WEEKLY, expected MON 08:00; DP13 Money and closure, DAILY, expected 08:00. RWB-E1-015 stamps `data_product_load` from `v_ace_batch_status`; a product with no COMPLETE batch keeps its last good business date, is marked stale and raises MSG-P1-001.

**Boundary.** v4 reconciled the load runs and the copy tables after JOB-04. v5 reconciles the Workbench case data against the ACE views and the ACE batch record; there is no load run to reconcile. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 enforces the view-only read, and the Section B read stays behind its flag until RWB-ACE-001 is deployed and V0003 applies (DL43).

## RWB-E1-013 Baseline measures

Module: P9 Reporting

**View.** `v_ace_payment` for money collected and `case_account` for the case stock; writes `measure_definition` and `measure_snapshot`.

**Grant.** No change. `recovery_svc` holds SELECT on the views named above from V0002 (RWB-E1-069) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP03 Case and ownership, ON_CHANGE as it changes; DP13 Money and closure, DAILY, expected 08:00. RWB-E1-015 stamps `data_product_load` from `v_ace_batch_status`; a product with no COMPLETE batch keeps its last good business date, is marked stale and raises MSG-P1-001.

**Boundary.** v4 read the money measures from the copy tables. v5 reads `v_ace_payment`; the case stock comes from `case_account`. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

## RWB-E1-014 Decision log copy to the data lake

Module: P1 Recovery data engine

**View.** No view. The story copies `decision_log_entry` to the lake and owns `lake_copy_watermark`.

**Grant.** No view in this story. `recovery_svc` holds DML on the Workbench tables it uses (V0001) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP12 Decision log, ON_CHANGE as it changes. A Workbench product is stamped from its last committed write, not from an ACE batch, so no ACE clock makes it stale.

**Boundary.** The copy is unchanged; it now stamps the ACE business date it copies alongside the Workbench sequence. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

## RWB-E1-015 Freshness stamp per data product

Module: P1 Recovery data engine

**View.** `v_ace_batch_status` is the freshness source: one row per ACE batch with its business date, status and record count; reads `data_product` and writes `data_product_load`.

**Grant.** No change. `recovery_svc` holds SELECT on the views named above from V0002 (RWB-E1-069) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** All 14 products: DP01, DP02, DP05, DP07, DP11 and DP13 DAILY by 08:00, DP06 WEEKLY by Monday 08:00, and the Workbench products DP03, DP04, DP08, DP09, DP10, DP12 and DP14 ON_CHANGE as they change. RWB-E1-015 stamps `data_product_load` from `v_ace_batch_status`; a product with no COMPLETE batch keeps its last good business date, is marked stale and raises MSG-P1-001.

**Boundary.** v4 stamped each product from its `load_run`. v5 stamps it from `v_ace_batch_status` and the `ace_batch_run` record that RWB-ACE-001 populates; a Workbench product is stamped from its own last committed write. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 enforces the view-only read, and the Section B read stays behind its flag until RWB-ACE-001 is deployed and V0003 applies (DL43).

## RWB-E1-016 Access control per data product and catalog entries

Module: P1 Recovery data engine

**View.** `v_ace_account`, `v_ace_customer` and `v_ace_contact` for the field level checks; writes `data_product_access` and `masking_rule` and reads the four extension tables.

**Grant.** No change beyond the DML V0001 already gives `recovery_svc` on the Workbench tables, including the extension table it writes; SELECT on the views comes from V0002 (RWB-E1-069). The story grants no privilege in `public` and no write on a view.

**Freshness.** DP01 Account and arrears, DAILY, expected 08:00; DP02 Customer and party, DAILY, expected 08:00; DP05 Contact and promises, DAILY, expected 08:00; DP06 Collateral and assets, WEEKLY, expected MON 08:00; DP14 Reference data, ON_CHANGE as it changes. RWB-E1-015 stamps `data_product_load` from `v_ace_batch_status`; a product with no COMPLETE batch keeps its last good business date, is marked stale and raises MSG-P1-001.

**Boundary.** v4 answered a data product record request from the copy tables. v5 answers it from the views named for each product, so access is decided on the view and the product, and the customer view still returns only the masked identity. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

## RWB-E1-017 Retention and archive rule for the data store

Module: P1 Recovery data engine

**View.** No view. The story owns `retention_rule` and `retention_action` over `recovery_case`.

**Grant.** No view in this story. `recovery_svc` holds DML on the Workbench tables it uses (V0001) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP03 Case and ownership, ON_CHANGE as it changes; DP10 Documents and extracted fields, ON_CHANGE as it changes; DP12 Decision log, ON_CHANGE as it changes; DP14 Reference data, ON_CHANGE as it changes. A Workbench product is stamped from its last committed write, not from an ACE batch, so no ACE clock makes it stale.

**Boundary.** No change of substance. The retention classes cover the 92 Workbench tables; the ACE source is retained by ACE under its own schedule. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

## RWB-E1-018 Case ID issuance and case record v1

Module: P3 Case and workflow

**View.** `v_ace_account`, `v_ace_customer`, `v_ace_ca_relation` and `v_ace_batch_status` for the entry gate; writes `recovery_case`, `case_account`, `case_party`, `case_entry_exclusion`, `party_ext` and `account_ext`.

**Grant.** No change beyond the DML V0001 already gives `recovery_svc` on the Workbench tables, including `party_ext` and `account_ext`; SELECT on the views comes from V0002 (RWB-E1-069). The story grants no privilege in `public` and no write on a view.

**Freshness.** DP01 Account and arrears, DAILY, expected 08:00; DP02 Customer and party, DAILY, expected 08:00; DP03 Case and ownership, ON_CHANGE as it changes. RWB-E1-015 stamps `data_product_load` from `v_ace_batch_status`; a product with no COMPLETE batch keeps its last good business date, is marked stale and raises MSG-P1-001.

**Boundary.** v4 created cases when JOB-01 published LoadCompleted for COLLINS. v5 creates them when the ACE batch for the business date is COMPLETE; the entry gate reads `v_ace_batch_status`. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 enforces the view-only read, and the Section B read stays behind its flag until RWB-ACE-001 is deployed and V0003 applies (DL43).

## RWB-E1-019 Roles, teams and queues as data

Module: P3 Case and workflow

**View.** No view. The story loads `role`, `queue`, `queue_member`, `reference_row` and `reference_version` as reference data.

**Grant.** No view in this story. `recovery_svc` holds DML on the Workbench tables it uses (V0001) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP14 Reference data, ON_CHANGE as it changes. A Workbench product is stamped from its last committed write, not from an ACE batch, so no ACE clock makes it stale.

**Boundary.** v4 loaded the queue files through the reference data service; v5 does the same, so only the table names and the version rules moved. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

## RWB-E1-020 Allocation and assignment engine v1

Module: P3 Case and workflow

**View.** No view. The story reads `recovery_case`, `queue_member` and `rule_row` and writes `assignment` and `decision_log_entry`.

**Grant.** No view in this story. `recovery_svc` holds DML on the Workbench tables it uses (V0001) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP03 Case and ownership, ON_CHANGE as it changes; DP14 Reference data, ON_CHANGE as it changes. A Workbench product is stamped from its last committed write, not from an ACE batch, so no ACE clock makes it stale.

**Boundary.** No change of substance. Allocation no longer waits on a load: it waits on the entry gate of RWB-E1-018, which reads the ACE batch record. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

## RWB-E1-021 Transfer rules and engine v1

Module: P3 Case and workflow

**View.** No view. The story reads `recovery_case`, `queue` and `rule_row` and writes `assignment` and `decision_log_entry`.

**Grant.** No view in this story. `recovery_svc` holds DML on the Workbench tables it uses (V0001) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP03 Case and ownership, ON_CHANGE as it changes; DP14 Reference data, ON_CHANGE as it changes. A Workbench product is stamped from its last committed write, not from an ACE batch, so no ACE clock makes it stale.

**Boundary.** No change of substance. A transfer names an ACE business key where it names an account; it never copies one. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

## RWB-E1-022 Sign-on with SSO, MFA and the first roles

Module: P4 Access and administration

**View.** No view. The story owns `role`, `permission` and `role_conflict`.

**Grant.** No view in this story. `recovery_svc` holds DML on the Workbench tables it uses (V0001) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP14 Reference data, ON_CHANGE as it changes. A Workbench product is stamped from its last committed write, not from an ACE batch, so no ACE clock makes it stale.

**Boundary.** No change of substance. The first roles are seeded as reference data, not as a copy of an ACE identity table. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

## RWB-E1-023 Case record view v1, read only

Module: P3 Case and workflow

**View.** `v_ace_account`, `v_ace_customer`, `v_ace_contact`, `v_ace_efs_action` and `v_ace_batch_status` for the read-only case record; reads `recovery_case`, `case_account`, `case_party`, `document` and `interaction`.

**Grant.** No change. `recovery_svc` holds SELECT on the views named above from V0002 (RWB-E1-069) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP01 Account and arrears, DAILY, expected 08:00; DP02 Customer and party, DAILY, expected 08:00; DP05 Contact and promises, DAILY, expected 08:00. RWB-E1-015 stamps `data_product_load` from `v_ace_batch_status`; a product with no COMPLETE batch keeps its last good business date, is marked stale and raises MSG-P1-001.

**Boundary.** v4 read the case, party and contact data from the copy tables. v5 reads the five views for the account and customer side and shows the freshness line from the batch record; that line stays behind its flag until RWB-ACE-001 lands. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 enforces the view-only read, and the Section B read stays behind its flag until RWB-ACE-001 is deployed and V0003 applies (DL43).

## RWB-E1-024 Document store and index

Module: P5 Document hub

**View.** No view. The story owns `document`, `document_field`, `document_type` and `document_hub_parameter`.

**Grant.** No view in this story. `recovery_svc` holds DML on the Workbench tables it uses (V0001) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP10 Documents and extracted fields, ON_CHANGE as it changes. A Workbench product is stamped from its last committed write, not from an ACE batch, so no ACE clock makes it stale.

**Boundary.** No change of substance. A document carries the case and ACE business keys; the document itself is a Workbench record. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

## RWB-E1-025 Document types and fields agreed

Module: P5 Document hub

**View.** No view. The story loads `document_type` as reference data.

**Grant.** No view in this story. `recovery_svc` holds DML on the Workbench tables it uses (V0001) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP10 Documents and extracted fields, ON_CHANGE as it changes; DP14 Reference data, ON_CHANGE as it changes. A Workbench product is stamped from its last committed write, not from an ACE batch, so no ACE clock makes it stale.

**Boundary.** v4 took the type list from the trackers of RWB-E1-012. v5 takes it from the fields the ACE views can supply and the types legal counsel signs off. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

## RWB-E1-026 Attach and search screen

Module: P5 Document hub

**View.** No view. The attach screen reads `recovery_case`, `document`, `document_type` and `document_hub_parameter`.

**Grant.** No view in this story. `recovery_svc` holds DML on the Workbench tables it uses (V0001) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP03 Case and ownership, ON_CHANGE as it changes; DP10 Documents and extracted fields, ON_CHANGE as it changes. A Workbench product is stamped from its last committed write, not from an ACE batch, so no ACE clock makes it stale.

**Boundary.** v4 listed the document types and fields from the copy tables. v5 lists the same types and the view fields the caller may see; no copy table is read. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

## RWB-E1-027 Decision log writer v1

Module: P7 Decision center and log

**View.** No view. The story writes `decision_log_entry` and reads `lov_value`.

**Grant.** No view in this story. `recovery_svc` holds DML on the Workbench tables it uses (V0001) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP12 Decision log, ON_CHANGE as it changes. A Workbench product is stamped from its last committed write, not from an ACE batch, so no ACE clock makes it stale.

**Boundary.** No change of substance. The writer takes the ACE business keys and the rule, model and agent versions it is given. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

## RWB-E1-028 Service levels, timers, escalation and prescription dates

Module: P3 Case and workflow

**View.** `v_ace_account` for days past due and the prescription basis; reads `recovery_case`, `case_account`, `reference_row` and writes `timer` and `decision_log_entry`.

**Grant.** No change. `recovery_svc` holds SELECT on the views named above from V0002 (RWB-E1-069) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP01 Account and arrears, DAILY, expected 08:00; DP03 Case and ownership, ON_CHANGE as it changes. RWB-E1-015 stamps `data_product_load` from `v_ace_batch_status`; a product with no COMPLETE batch keeps its last good business date, is marked stale and raises MSG-P1-001.

**Boundary.** v4 read `loan_account.days_past_due` and `last_payment_date`. v5 reads the same two values from `v_ace_account`; the calendar comes from `v_ace_holiday`. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

## RWB-E1-029 Rule load, validation and rollback

Module: P3 Case and workflow

**View.** No view. The story owns `rule_row`, `rule_test_case`, `reference_row` and `reference_version`.

**Grant.** No view in this story. `recovery_svc` holds DML on the Workbench tables it uses (V0001) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP14 Reference data, ON_CHANGE as it changes. A Workbench product is stamped from its last committed write, not from an ACE batch, so no ACE clock makes it stale.

**Boundary.** No change of substance. A rule that names an ACE field names its BR Field ID from the dictionary, not a copy column. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

## RWB-E1-030 Daily rebalancing and queue measures

Module: P3 Case and workflow

**View.** No view. The story reads `recovery_case`, `queue`, `queue_member` and `timer` and writes `queue_measure` and `decision_log_entry`.

**Grant.** No view in this story. `recovery_svc` holds DML on the Workbench tables it uses (V0001) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP03 Case and ownership, ON_CHANGE as it changes. A Workbench product is stamped from its last committed write, not from an ACE batch, so no ACE clock makes it stale.

**Boundary.** v4 started JOB-06 at 06:30 or when JOB-03 completed. v5 keeps that chain; the one load shaped wait behind it, the case list, now reads `v_ace_batch_status` through RWB-E1-002. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

## RWB-E1-031 Queue and owner on the case list with filters

Module: P3 Case and workflow

**View.** No view. The case list filters read `recovery_case` and `queue` through the P3 interface.

**Grant.** No view in this story. `recovery_svc` holds DML on the Workbench tables it uses (V0001) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP03 Case and ownership, ON_CHANGE as it changes. A Workbench product is stamped from its last committed write, not from an ACE batch, so no ACE clock makes it stale.

**Boundary.** v4 showed the product from the case record. v5 keeps that column and takes the product category from `v_ace_account` when the caller may see it. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

## RWB-E1-032 Automatic attach from the OCR intake

Module: P5 Document hub

**View.** `v_ace_account` for the account key that the intake matches; reads `document_intake`, `document_text` and `document` and writes `decision_log_entry`.

**Grant.** No change. `recovery_svc` holds SELECT on the views named above from V0002 (RWB-E1-069) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP01 Account and arrears, DAILY, expected 08:00; DP10 Documents and extracted fields, ON_CHANGE as it changes. RWB-E1-015 stamps `data_product_load` from `v_ace_batch_status`; a product with no COMPLETE batch keeps its last good business date, is marked stale and raises MSG-P1-001.

**Boundary.** v4 ran the match step in JOB-12 against the case and account rows. v5 matches to the account key and product on `v_ace_account`; the job step stays, the copy read does not. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

## RWB-E1-033 Search across cases

Module: P5 Document hub

**View.** No view. Search reads `document_text`, `document_field` and `document`; an ACE field is shown by its dictionary entry.

**Grant.** No view in this story. `recovery_svc` holds DML on the Workbench tables it uses (V0001) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP10 Documents and extracted fields, ON_CHANGE as it changes. A Workbench product is stamped from its last committed write, not from an ACE batch, so no ACE clock makes it stale.

**Boundary.** v4 searched the stored document text and fields. v5 searches the same Workbench index; an ACE field is reached through the views only when a document links to one. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

## RWB-E1-034 Letter template management

Module: P6 Communications

**View.** No view. The story owns `template` and reads `merge_field` and `lov_value`.

**Grant.** No view in this story. `recovery_svc` holds DML on the Workbench tables it uses (V0001) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP14 Reference data, ON_CHANGE as it changes. A Workbench product is stamped from its last committed write, not from an ACE batch, so no ACE clock makes it stale.

**Boundary.** No change of substance. A merge field names a BR Field ID; the value is read from the owning interface at generation. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

## RWB-E1-035 Case record view v1.1 with documents and history timeline

Module: P3 Case and workflow

**View.** No view. The timeline reads `interaction`, `document`, `assignment` and `decision_log_entry`.

**Grant.** No view in this story. `recovery_svc` holds DML on the Workbench tables it uses (V0001) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP03 Case and ownership, ON_CHANGE as it changes; DP05 Contact and promises, DAILY, expected 08:00; DP10 Documents and extracted fields, ON_CHANGE as it changes; DP12 Decision log, ON_CHANGE as it changes. RWB-E1-015 stamps `data_product_load` from `v_ace_batch_status`; a product with no COMPLETE batch keeps its last good business date, is marked stale and raises MSG-P1-001.

**Boundary.** v4 built each timeline entry from the ledger and the document store. v5 keeps that and adds the source reference the ledger already carries for an ACE-sourced event. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

## RWB-E1-037 Role to permission matrix as data and PDPA field masking by role

Module: P4 Access and administration

**View.** `v_ace_customer` and `v_ace_contact` for the masking rules and the two masked identity fields; owns `role`, `permission`, `masking_rule` and writes `decision_log_entry`.

**Grant.** No change. `recovery_svc` holds SELECT on the views named above from V0002 (RWB-E1-069) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP02 Customer and party, DAILY, expected 08:00; DP14 Reference data, ON_CHANGE as it changes. RWB-E1-015 stamps `data_product_load` from `v_ace_batch_status`; a product with no COMPLETE batch keeps its last good business date, is marked stale and raises MSG-P1-001.

**Boundary.** v4 masked the personal fields of the copy tables through FieldMasker. v5 masks the view columns and never sees a clear identity number, because `v_ace_customer` exposes only `id_no_masked` and `id_no_last4`. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

## RWB-E1-038 Delegation of authority table as reference data

Module: P4 Access and administration

**View.** No view. The story loads `delegation_limit` and reads `lov_value`.

**Grant.** No view in this story. `recovery_svc` holds DML on the Workbench tables it uses (V0001) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP14 Reference data, ON_CHANGE as it changes. A Workbench product is stamped from its last committed write, not from an ACE batch, so no ACE clock makes it stale.

**Boundary.** No change of substance. Limit 0 to 95 are loaded as reference data; no approval level reads an ACE table. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

## RWB-E1-039 Access log into the decision log and break-glass admin

Module: P4 Access and administration, with P7 Decision center and log

**View.** No view. The story writes `decision_log_entry` and reads `role` and `permission`.

**Grant.** No view in this story. `recovery_svc` holds DML on the Workbench tables it uses (V0001) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP12 Decision log, ON_CHANGE as it changes; DP14 Reference data, ON_CHANGE as it changes. A Workbench product is stamped from its last committed write, not from an ACE batch, so no ACE clock makes it stale.

**Boundary.** No change of substance. A break-glass action is a decision log entry with its reason and its expiry. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

## RWB-E1-040 Document checklist per case type as reference data

Module: P5 Document hub

**View.** No view. The story loads `document_checklist_item` and reads `document_type`, `document`, `case_document_check` and `recovery_case`.

**Grant.** No view in this story. `recovery_svc` holds DML on the Workbench tables it uses (V0001) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP10 Documents and extracted fields, ON_CHANGE as it changes; DP14 Reference data, ON_CHANGE as it changes. A Workbench product is stamped from its last committed write, not from an ACE batch, so no ACE clock makes it stale.

**Boundary.** No change of substance. The checklist names document types, not source tables. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

## RWB-E1-041 Retention classes and virus scan on intake

Module: P5 Document hub

**View.** No view. The story owns `retention_rule`, `retention_action` and the scan state on `document_intake`; reads `document`.

**Grant.** No view in this story. `recovery_svc` holds DML on the Workbench tables it uses (V0001) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP10 Documents and extracted fields, ON_CHANGE as it changes. A Workbench product is stamped from its last committed write, not from an ACE batch, so no ACE clock makes it stale.

**Boundary.** No change of substance. Retention classes apply to Workbench documents; ACE source documents stay in ACE. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

## RWB-E1-042 Central configuration service and parameter catalog

Module: P3 Case and workflow

**View.** No view. The story owns `parameter_catalog` and `parameter_value`.

**Grant.** No view in this story. `recovery_svc` holds DML on the Workbench tables it uses (V0001) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP14 Reference data, ON_CHANGE as it changes. A Workbench product is stamped from its last committed write, not from an ACE batch, so no ACE clock makes it stale.

**Boundary.** No change of substance. Parameters are data; no environment name or source table is written in code. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

## RWB-E1-043 Reference data service with versioned tables

Module: P3 Case and workflow

**View.** No view. The story owns `reference_version`, `reference_row` and `lov_value`.

**Grant.** No view in this story. `recovery_svc` holds DML on the Workbench tables it uses (V0001) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP14 Reference data, ON_CHANGE as it changes. A Workbench product is stamped from its last committed write, not from an ACE batch, so no ACE clock makes it stale.

**Boundary.** No change of substance. The reference load service is the only path that changes a versioned table. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

## RWB-E1-044 Database migrations versioned with parameterized schema names

Module: P3 Case and workflow

**View.** No view. The story owns the migration path and the schema name parameter; it creates no table of its own.

**Grant.** No view in this story. `recovery_svc` holds DML on the Workbench tables it uses (V0001) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** No ACE freshness. The only clock is the Workbench `created_at` and `updated_at`; nothing in this story waits on an ACE batch.

**Boundary.** v4 shipped a baseline migration file. v5 rules that RWB-E1-044 ships no production migration file; RWB-E1-001 owns V0001 and RWB-E1-069 owns V0002 and V0003. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

## RWB-E1-045 Multi-product parameters for Mortgage, HP and SSME

Module: P3 Case and workflow

**View.** No view. The story reads `recovery_case`, `reference_row` and `timer` and writes `parameter_value` rows for the three products.

**Grant.** No view in this story. `recovery_svc` holds DML on the Workbench tables it uses (V0001) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP03 Case and ownership, ON_CHANGE as it changes; DP14 Reference data, ON_CHANGE as it changes. A Workbench product is stamped from its last committed write, not from an ACE batch, so no ACE clock makes it stale.

**Boundary.** v4 already held the three products as reference data. v5 keeps that and adds the product category from `v_ace_account` as the key the parameters are read by. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

## RWB-E1-046 Template and merge field catalog as data

Module: P6 Communications

**View.** No view. The story loads `merge_field` and reads `lov_value` and `template`.

**Grant.** No view in this story. `recovery_svc` holds DML on the Workbench tables it uses (V0001) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP14 Reference data, ON_CHANGE as it changes. A Workbench product is stamped from its last committed write, not from an ACE batch, so no ACE clock makes it stale.

**Boundary.** v4 checked each merge field against the copy tables. v5 checks it against the dictionary, where the 30 views and the Workbench tables both have rows. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

## RWB-E1-047 Feature flags for module release with a removal date

Module: P2 Integration

**View.** No view. The story owns `feature_flag` and `feature_flag_change`.

**Grant.** No view in this story. `recovery_svc` holds DML on the Workbench tables it uses (V0001) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP14 Reference data, ON_CHANGE as it changes. A Workbench product is stamped from its last committed write, not from an ACE batch, so no ACE clock makes it stale.

**Boundary.** No change of substance. Section B features keep a flag until RWB-ACE-001 is deployed and V0003 applies. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

## RWB-E1-048 Rule change audit report

Module: P3 Case and workflow

**View.** No view. The story reads `reference_row` and `reference_version`.

**Grant.** No view in this story. `recovery_svc` holds DML on the Workbench tables it uses (V0001) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP14 Reference data, ON_CHANGE as it changes. A Workbench product is stamped from its last committed write, not from an ACE batch, so no ACE clock makes it stale.

**Boundary.** No change of substance. The audit report reads the version history, not the source data. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

## RWB-E1-049 OCR pipeline on the Workbench document hub

Module: P5 Document hub

**View.** No view. The OCR pipeline reads `document_intake` and writes `document_text` and `document_hub_parameter`.

**Grant.** No view in this story. `recovery_svc` holds DML on the Workbench tables it uses (V0001) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP10 Documents and extracted fields, ON_CHANGE as it changes. A Workbench product is stamped from its last committed write, not from an ACE batch, so no ACE clock makes it stale.

**Boundary.** No change of substance. OCR reads the Workbench document copy; no ACE table is read. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

## RWB-E1-050 Document classification

Module: P5 Document hub

**View.** No view. Classification reads `document_text` and `document_type` and writes the type on `document_intake`.

**Grant.** No view in this story. `recovery_svc` holds DML on the Workbench tables it uses (V0001) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP10 Documents and extracted fields, ON_CHANGE as it changes. A Workbench product is stamped from its last committed write, not from an ACE batch, so no ACE clock makes it stale.

**Boundary.** No change of substance. The classifier reads the document text only. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

## RWB-E1-052 Notice generation v1

Module: P6 Communications

**View.** `v_ace_account`, `v_ace_customer`, `v_ace_contact` and `v_ace_pod` for the merge values and the proof of delivery; reads `template`, `merge_field`, `case_party` and `recovery_case`.

**Grant.** No change. `recovery_svc` holds SELECT on the views named above from V0002 (RWB-E1-069) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP01 Account and arrears, DAILY, expected 08:00; DP02 Customer and party, DAILY, expected 08:00; DP07 Legal events and cases, DAILY, expected 08:00. RWB-E1-015 stamps `data_product_load` from `v_ace_batch_status`; a product with no COMPLETE batch keeps its last good business date, is marked stale and raises MSG-P1-001.

**Boundary.** v4 merged values from the party, account and contact copy tables. v5 reads them from the views; the proof of delivery comes from `v_ace_pod` and stays behind its flag until RWB-ACE-001 lands. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 enforces the view-only read, and the Section B read stays behind its flag until RWB-ACE-001 is deployed and V0003 applies (DL43).

## RWB-E1-053 Field extraction for the six types into the index

Module: P5 Document hub

**View.** No view. Extraction reads `document_text` and `document_type` and writes `document_field`.

**Grant.** No view in this story. `recovery_svc` holds DML on the Workbench tables it uses (V0001) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP10 Documents and extracted fields, ON_CHANGE as it changes. A Workbench product is stamped from its last committed write, not from an ACE batch, so no ACE clock makes it stale.

**Boundary.** No change of substance. Extracted values stay Workbench records; an ACE field is compared through its dictionary entry, never written back. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

## RWB-E1-054 Review queue for low-confidence documents

Module: P5 Document hub

**View.** No view. The review queue reads `document_intake`, `document_text`, `document_field` and `recovery_case` and writes `decision_log_entry`.

**Grant.** No view in this story. `recovery_svc` holds DML on the Workbench tables it uses (V0001) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP10 Documents and extracted fields, ON_CHANGE as it changes. A Workbench product is stamped from its last committed write, not from an ACE batch, so no ACE clock makes it stale.

**Boundary.** No change of substance. A reviewer confirms a Workbench field; no ACE object is updated. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

## RWB-E1-055 Proof of delivery capture design with WIN

Module: P6 Communications

**View.** `v_ace_account`, `v_ace_contact` and `v_ace_pod` for the delivery evidence; reads `case_account`, `notice` and `template`.

**Grant.** No change. `recovery_svc` holds SELECT on the views named above from V0002 (RWB-E1-069) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP01 Account and arrears, DAILY, expected 08:00; DP07 Legal events and cases, DAILY, expected 08:00. RWB-E1-015 stamps `data_product_load` from `v_ace_batch_status`; a product with no COMPLETE batch keeps its last good business date, is marked stale and raises MSG-P1-001.

**Boundary.** v4 waited on the INT-15 load. v5 reads `v_ace_pod` after ACE ingests the WIN result; the proof path stays behind its flag until RWB-ACE-001 lands. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 enforces the view-only read, and the Section B read stays behind its flag until RWB-ACE-001 is deployed and V0003 applies (DL43).

## RWB-E1-056 Run books and monitoring for every Epic 1 Workbench job

Module: P2 Integration

**View.** `v_ace_batch_status` for the ACE batch state; reads `job_catalog`, `data_product_load`, `case_list_row` and `reconciliation_result`.

**Grant.** No change. `recovery_svc` holds SELECT on the views named above from V0002 (RWB-E1-069) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** All 14 products: DP01, DP02, DP05, DP07, DP11 and DP13 DAILY by 08:00, DP06 WEEKLY by Monday 08:00, and the Workbench products DP03, DP04, DP08, DP09, DP10, DP12 and DP14 ON_CHANGE as they change. RWB-E1-015 stamps `data_product_load` from `v_ace_batch_status`; a product with no COMPLETE batch keeps its last good business date, is marked stale and raises MSG-P1-001.

**Boundary.** v4 gave every Epic 1 job a run book, most of them load jobs. v5 gives a run book to every Workbench job and to the ACE batch record the Workbench depends on; the load jobs no longer exist. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 enforces the view-only read, and the Section B read stays behind its flag until RWB-ACE-001 is deployed and V0003 applies (DL43).

## RWB-E1-057 Intake from branches, mailroom, partner SFTP and email

Module: P5 Document hub

**View.** No view. Intake reads `document_intake` and `document_hub_parameter` and writes the received file record.

**Grant.** No view in this story. `recovery_svc` holds DML on the Workbench tables it uses (V0001) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP10 Documents and extracted fields, ON_CHANGE as it changes. A Workbench product is stamped from its last committed write, not from an ACE batch, so no ACE clock makes it stale.

**Boundary.** v4 ran intake as JOB-12 and stored each file in the document hub. v5 keeps that path and the source reference; ACE ingests no document from it. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

## RWB-E1-058 Agent platform set-up [E1a]

Module: P10 Agent runtime

**View.** No view. The agent platform reads `recovery_case`, `rule_row` and `agent_policy` and writes the agent tables.

**Grant.** No view in this story. `recovery_svc` holds DML on the Workbench tables it uses (V0001) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP03 Case and ownership, ON_CHANGE as it changes; DP14 Reference data, ON_CHANGE as it changes. A Workbench product is stamped from its last committed write, not from an ACE batch, so no ACE clock makes it stale.

**Boundary.** v4 depended on the ALS load before an agent test could see cases. v5 seeds cases in the sandbox and reads ACE data through the views, so no load gate remains. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

## RWB-E1-059 Case intake agent in shadow [E1b]

Module: P10 Agent runtime

**View.** `v_ace_valuation` and `v_ace_contact` for the shadow comparison; writes `agent_run`, `agent_sample` and `agent_evaluation_run`.

**Grant.** No change. `recovery_svc` holds SELECT on the views named above from V0002 (RWB-E1-069) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP02 Customer and party, DAILY, expected 08:00; DP06 Collateral and assets, WEEKLY, expected MON 08:00. RWB-E1-015 stamps `data_product_load` from `v_ace_batch_status`; a product with no COMPLETE batch keeps its last good business date, is marked stale and raises MSG-P1-001.

**Boundary.** v4 compared the agent against the contact and appraisal rows it held. v5 compares it against `v_ace_contact` and `v_ace_valuation`; the story stays behind its flag until RWB-ACE-001 lands. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 enforces the view-only read, and the Section B read stays behind its flag until RWB-ACE-001 is deployed and V0003 applies (DL43).

## RWB-E1-060 Extraction evaluation [E1c]

Module: P10 Agent runtime

**View.** No view. The evaluation reads `document_field` and the agent tables.

**Grant.** No view in this story. `recovery_svc` holds DML on the Workbench tables it uses (V0001) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP10 Documents and extracted fields, ON_CHANGE as it changes. A Workbench product is stamped from its last committed write, not from an ACE batch, so no ACE clock makes it stale.

**Boundary.** No change of substance. The evaluation compares extracted fields with the reviewed Workbench field. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

## RWB-E1-061 Intake agent evaluation and L1 proposal [E2a]

Module: P10 Agent runtime

**View.** No view. The proposal reads `agent_evaluation_run`, `agent_evaluation`, `agent_run` and `agent_policy`.

**Grant.** No view in this story. `recovery_svc` holds DML on the Workbench tables it uses (V0001) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP03 Case and ownership, ON_CHANGE as it changes. A Workbench product is stamped from its last committed write, not from an ACE batch, so no ACE clock makes it stale.

**Boundary.** No change of substance. The L1 proposal is a decision log entry, not an automatic change. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

## RWB-E1-062 Deviation screening agent in shadow [E2b]

Module: P10 Agent runtime

**View.** No view. The screening reads `recovery_case`, `rule_row`, `document_field` and the agent tables; writes `deviation`.

**Grant.** No view in this story. `recovery_svc` holds DML on the Workbench tables it uses (V0001) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP03 Case and ownership, ON_CHANGE as it changes; DP10 Documents and extracted fields, ON_CHANGE as it changes. A Workbench product is stamped from its last committed write, not from an ACE batch, so no ACE clock makes it stale.

**Boundary.** No change of substance. The screening agent reads Workbench records and proposes; a person decides. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

## RWB-E1-063 Agent monitoring dashboard v1 [E2c]

Module: P10 Agent runtime

**View.** No view. The dashboard reads `agent_run`, `agent_policy`, `agent_evaluation` and `agent_alert`.

**Grant.** No view in this story. `recovery_svc` holds DML on the Workbench tables it uses (V0001) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP03 Case and ownership, ON_CHANGE as it changes. A Workbench product is stamped from its last committed write, not from an ACE batch, so no ACE clock makes it stale.

**Boundary.** No change of substance. The dashboard reports the agent tables and the freshness line of the products the agents read. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

## RWB-E1-064 Data dictionary for the 14 data products

Module: P1 Recovery data engine

**View.** No view. The dictionary reads `sys_objects`, `sys_fields`, `sys_field_version`, `data_contract` and `data_product`.

**Grant.** No view in this story. `recovery_svc` holds DML on the Workbench tables it uses (V0001) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP01 Account and arrears, DAILY, expected 08:00; DP06 Collateral and assets, WEEKLY, expected MON 08:00; DP14 Reference data, ON_CHANGE as it changes. RWB-E1-015 stamps `data_product_load` from `v_ace_batch_status`; a product with no COMPLETE batch keeps its last good business date, is marked stale and raises MSG-P1-001.

**Boundary.** v4 described the copy tables. v5 describes the 92 tables and the 30 views, so the dictionary is the one place a view column and its ACE source field are defined. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

## RWB-E1-065 Sandbox database with synthetic recovery data

Module: P1 Recovery data engine

**View.** All 30 views: the sandbox seeds the ACE schema, applies V0001 to V0003 so the 30 views exist, and fills the 88 Workbench tables and the four extension tables `party_ext`, `contact_point_ext`, `account_ext` and `valuation_ext` from their dictionary rows.

**Grant.** No change beyond the DML V0001 already gives `recovery_svc` on the Workbench tables, including `party_ext`, `contact_point_ext`, `account_ext` and `valuation_ext`; SELECT on the views comes from V0002 (RWB-E1-069). The story grants no privilege in `public` and no write on a view.

**Freshness.** All 14 products: DP01, DP02, DP05, DP07, DP11 and DP13 DAILY by 08:00, DP06 WEEKLY by Monday 08:00, and the Workbench products DP03, DP04, DP08, DP09, DP10, DP12 and DP14 ON_CHANGE as they change. RWB-E1-015 stamps `data_product_load` from `v_ace_batch_status`; a product with no COMPLETE batch keeps its last good business date, is marked stale and raises MSG-P1-001.

**Boundary.** v4 built a sandbox from the copy schema. v5 builds it from the ACE schema, the RWB-ACE-001 Tier 2 DDL and the 30 views, so DEV and SIT test the same read path as PROD. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

## RWB-E1-066 Interaction ledger store and writer

Module: P1 Recovery data engine

**View.** No view. The story owns `interaction` and reads `recovery_case` through `CaseQueryApi`.

**Grant.** No view in this story. `recovery_svc` holds DML on the Workbench tables it uses (V0001) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP05 Contact and promises, DAILY, expected 08:00; DP12 Decision log, ON_CHANGE as it changes. RWB-E1-015 stamps `data_product_load` from `v_ace_batch_status`; a product with no COMPLETE batch keeps its last good business date, is marked stale and raises MSG-P1-001.

**Boundary.** No change of substance. An ACE-sourced contact is a ledger entry with its source reference, not a copy of the contact. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

## RWB-E1-067 Every Workbench action into the interaction ledger

Module: P1 Recovery data engine

**View.** No view. The story intercepts Workbench actions and writes `interaction` and `processed_event`.

**Grant.** No view in this story. `recovery_svc` holds DML on the Workbench tables it uses (V0001) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP05 Contact and promises, DAILY, expected 08:00; DP12 Decision log, ON_CHANGE as it changes. RWB-E1-015 stamps `data_product_load` from `v_ace_batch_status`; a product with no COMPLETE batch keeps its last good business date, is marked stale and raises MSG-P1-001.

**Boundary.** No change of substance. The interception covers Workbench actions; an ACE change reaches the ledger as an event reference. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

## RWB-E1-068 Interaction ledger read interface

Module: P1 Recovery data engine

**View.** No view. The read interface reads `interaction` and `recovery_case`.

**Grant.** No view in this story. `recovery_svc` holds DML on the Workbench tables it uses (V0001) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP05 Contact and promises, DAILY, expected 08:00; DP12 Decision log, ON_CHANGE as it changes. RWB-E1-015 stamps `data_product_load` from `v_ace_batch_status`; a product with no COMPLETE batch keeps its last good business date, is marked stale and raises MSG-P1-001.

**Boundary.** No change of substance. The ledger read is a Workbench read; masking of `summary` follows RWB-E1-037. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

## RWB-E1-069 Read-only ACE source views, grants and boundary rule

Module: P1 Recovery data engine

**View.** All 30 views: 16 Section A views over the 21 ACE tables that exist today and 14 Section B views over the 14 tables and 12 columns RWB-ACE-001 adds; writes the four extension tables.

**Grant.** V0002 grants `USAGE` on `public` and `SELECT` on the 21 Tier 1 tables to `ace_view_owner`, sets that role as owner of each view, grants `USAGE` on `recovery` and `SELECT` on each view to `recovery_svc`, and revokes all from `PUBLIC`. V0003 repeats the SELECT grant for the 14 Section B views. No `GRANT SELECT ON ALL TABLES` and no write on a view.

**Freshness.** All 14 products: DP01, DP02, DP05, DP07, DP11 and DP13 DAILY by 08:00, DP06 WEEKLY by Monday 08:00, and the Workbench products DP03, DP04, DP08, DP09, DP10, DP12 and DP14 ON_CHANGE as they change. RWB-E1-015 stamps `data_product_load` from `v_ace_batch_status`; a product with no COMPLETE batch keeps its last good business date, is marked stale and raises MSG-P1-001.

**Boundary.** This is the story that replaces the load estate: V0002 ships the 16 Section A views, the four extension tables and the grant block; V0003 ships the 14 Section B views and waits for RWB-ACE-001. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 enforces the view-only read, and the Section B read stays behind its flag until RWB-ACE-001 is deployed and V0003 applies (DL43).

## RWB-TE-001 Recovery module folder and boundary test

Module: P2 Integration

**View.** No view. The story owns the module map `recovery-modules.yaml` and the boundary test that reads it.

**Grant.** No database grant. The module map is the contract; the build fails when a class names an object outside it.

**Freshness.** No ACE freshness. The only clock is the Workbench `created_at` and `updated_at`; nothing in this story waits on an ACE batch.

**Boundary.** Rule BND-6 lives in this story: no recovery class names a `public` table, and the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`. No constraint in `recovery` references `public`; a link to an ACE record is a varchar(255) business key with no foreign key.

## RWB-TE-002 Code owners for the recovery module

Module: P2 Integration

**View.** No view. The story owns `CODEOWNERS` and the review rules.

**Grant.** No view in this story. `recovery_svc` holds DML on the Workbench tables it uses (V0001) and no privilege in `public`; the check grants nothing and writes no ACE object.

**Freshness.** No ACE freshness. The only clock is the Workbench `created_at` and `updated_at`; nothing in this story waits on an ACE batch.

**Boundary.** No change of substance. The owners cover the view migrations as well as the module folders. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

## RWB-TE-003 Types and contract tests from the API specification

Module: P2 Integration

**View.** No view. The story owns the generated types and the contract tests.

**Grant.** No view in this story. `recovery_svc` holds DML on the Workbench tables it uses (V0001) and no privilege in `public`; the check grants nothing and writes no ACE object.

**Freshness.** No ACE freshness. The only clock is the Workbench `created_at` and `updated_at`; nothing in this story waits on an ACE batch.

**Boundary.** No change of substance. An ACE-sourced field keeps its dictionary type; the view type and the API type are compared. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

## RWB-TE-004 Masked data in SIT and UAT

Module: P1 Recovery data engine

**View.** No view. The masked copy loads the Workbench tables `recovery_case`, `case_account`, `case_party`, `interaction`, `document_field`, `party_ext` and `contact_point_ext` in SIT and UAT.

**Grant.** No change beyond the DML V0001 already gives `recovery_svc` on the Workbench tables, including `party_ext` and `contact_point_ext`; SELECT on the views comes from V0002 (RWB-E1-069). The story grants no privilege in `public` and no write on a view.

**Freshness.** DP03 Case and ownership, ON_CHANGE as it changes; DP05 Contact and promises, DAILY, expected 08:00; DP10 Documents and extracted fields, ON_CHANGE as it changes. RWB-E1-015 stamps `data_product_load` from `v_ace_batch_status`; a product with no COMPLETE batch keeps its last good business date, is marked stale and raises MSG-P1-001.

**Boundary.** The earlier story loaded a masked copy of the ACE source tables. v5 loads a masked copy of the Workbench tables only; ACE supplies its own SIT and UAT data through ACE, so no ACE source is copied. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

## RWB-TE-005 Rule table test harness

Module: P3 Case and workflow

**View.** No view. The harness reads `rule_row` and `rule_test_case`.

**Grant.** No view in this story. `recovery_svc` holds DML on the Workbench tables it uses (V0001) and no privilege in `public`; the check grants nothing and writes no ACE object.

**Freshness.** DP14 Reference data, ON_CHANGE as it changes. A Workbench product is stamped from its last committed write, not from an ACE batch, so no ACE clock makes it stale.

**Boundary.** No change of substance. A rule test case names a BR Field ID and a synthetic value. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

## RWB-TE-006 Outbox and retry for outbound work

Module: P2 Integration

**View.** No view. The story owns `outbox_event`, `outbox_delivery` and `task` and reads `decision_log_entry` and `recovery_case`.

**Grant.** No view in this story. `recovery_svc` holds DML on the Workbench tables it uses (V0001) and no privilege in `public`; the check grants nothing and writes no ACE object.

**Freshness.** DP03 Case and ownership, ON_CHANGE as it changes; DP12 Decision log, ON_CHANGE as it changes. A Workbench product is stamped from its last committed write, not from an ACE batch, so no ACE clock makes it stale.

**Boundary.** The outbox is unchanged. v5 retries Workbench outbound work only; a failed ACE ingest is the ACE team's retry and shows as a stale product. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

## RWB-TE-007 Scheduled jobs on Quartz

Module: P3 Case and workflow

**View.** No view. The story owns the Quartz schedule and `job_catalog`.

**Grant.** No view in this story. `recovery_svc` holds DML on the Workbench tables it uses (V0001) and no privilege in `public`; the check grants nothing and writes no ACE object.

**Freshness.** No ACE freshness. The only clock is the Workbench `created_at` and `updated_at`; nothing in this story waits on an ACE batch.

**Boundary.** The Quartz schedule is unchanged. v5 schedules Workbench jobs only; the ACE batch schedule belongs to ACE. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

## RWB-TE-008 Decision log hash chain check

Module: P7 Decision center and log

**View.** No view. The check reads `decision_log_entry`.

**Grant.** No view in this story. `recovery_svc` holds DML on the Workbench tables it uses (V0001) and no privilege in `public`; the check grants nothing and writes no ACE object.

**Freshness.** DP12 Decision log, ON_CHANGE as it changes. A Workbench product is stamped from its last committed write, not from an ACE batch, so no ACE clock makes it stale.

**Boundary.** No change of substance. The hash chain covers the ledger, including entries that name ACE business keys. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

## RWB-TE-011 PDPA lint for code, tests and logs

Module: P2 Integration

**View.** The dictionary entries of `v_ace_customer` and `v_ace_contact` and the Workbench fields `interaction.summary` and `document_field.field_value`.

**Grant.** No change. `recovery_svc` holds SELECT on the views named above from V0002 (RWB-E1-069) and no privilege in `public`; the check grants nothing and writes no ACE object.

**Freshness.** DP02 Customer and party, DAILY, expected 08:00; DP05 Contact and promises, DAILY, expected 08:00; DP10 Documents and extracted fields, ON_CHANGE as it changes. RWB-E1-015 stamps `data_product_load` from `v_ace_batch_status`; a product with no COMPLETE batch keeps its last good business date, is marked stale and raises MSG-P1-001.

**Boundary.** The earlier lint read the copy table columns. v5 reads the field list from the dictionary, so the view columns and the Workbench fields are covered by one rule set. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

## RWB-TE-012 Document storage containers

Module: P5 Document hub

**View.** No view. The story owns the document storage containers.

**Grant.** No view in this story. `recovery_svc` holds DML on the Workbench tables it uses (V0001) and no privilege in `public`; the check grants nothing and writes no ACE object.

**Freshness.** DP10 Documents and extracted fields, ON_CHANGE as it changes. A Workbench product is stamped from its last committed write, not from an ACE batch, so no ACE clock makes it stale.

**Boundary.** No change of substance. An ACE source document stays in ACE; the container holds Workbench documents only. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

## RWB-TE-013 Agent runtime client with fallback

Module: P10 Agent runtime

**View.** No view. The client reads `agent_policy` and `agent_run` and writes `decision_log_entry` and `recovery_case`.

**Grant.** No view in this story. `recovery_svc` holds DML on the Workbench tables it uses (V0001) and no privilege in `public`; the check grants nothing and writes no ACE object.

**Freshness.** DP03 Case and ownership, ON_CHANGE as it changes; DP12 Decision log, ON_CHANGE as it changes. A Workbench product is stamped from its last committed write, not from an ACE batch, so no ACE clock makes it stale.

**Boundary.** No change of substance. The fallback keeps a person in the path when the agent runtime is unavailable. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.
