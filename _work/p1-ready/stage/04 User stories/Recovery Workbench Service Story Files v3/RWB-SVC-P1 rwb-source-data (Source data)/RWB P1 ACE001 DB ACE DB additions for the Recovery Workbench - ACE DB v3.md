# RWB-P1-ACE001-DB ACE DB additions for the Recovery Workbench

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P1-ACE001-DB |
| Work type | DB (ACE DB) |
| Document version | v3 |
| Suggested owner | ACE team (suggested; any team may pick up this story) |
| Service | rwb-source-data |
| Service epic | RWB-SVC-P1 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-ACE-001 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP05, DP15, DP19 |
| Parallel lane | L-P1-A |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-P1-ACE001-DB-16); the squad sizes this story at refinement |
| Depends on (build) | None; the AC4 check on account, customer and efs_action waits for the Tier 1 grant of RWB-P1-E1069-DB (section 3) |
| Contract dependencies | None: this DB story publishes no API contract, so no contract or CON dependency applies |
| Contract fake library version | None published: this DB story publishes no contract fake (DOR-RWB-P1-ACE001-DB-22) |
| Contract version | Not applicable: this DB story builds against no API contract version; it publishes no contract, has no contract dependency and does not use the `/v1` base path of the service |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v1.md (FR-P1-001, FR-P1-002, FR-P1-005, FR-P1-007, FR-P1-008, FR-P1-010, FR-P1-012, FR-P1-013, FR-P1-029) |
| Status | Draft (directive resolutions) |
| Readiness decisions | RD-P1-025, RD-P1-027, RD-P1-041, RD-P1-043, RD-P1-045 |

**Version 3 changes.**

- ACE Field Gap List v2 is the normative column and field definition (81 field rows, 79 distinct columns), with the two metadata exceptions in BR1 (RWB-P1-ACE001-DB#1, #2, #6 and #8; RD-P1-025, RD-P1-027).
- Batch record states, redelivery, forward-only correction, grants, Section B access and test data follow the rulings (RWB-P1-ACE001-DB#3, #4, #5, #12, #13, #15, #19, #20 and #22; RD-P1-041, RD-P1-043, RD-P1-045).
- AC1, AC2, AC8 restated and AC15 to AC18 added; application rules BR9 to BR11 and their test case leave this story (RWB-P1-ACE001-DB#16, #17, #18, #23 and #24).
- Pending: source codes and job map, foreign-key rules, the 12 columns no view selects, grant owner, iam_group_key, classification, volumes (RWB-P1-ACE001-DB#7, #9, #10, #11, #14, #18 and #21).
- Readiness decisions: as in the header.
- Cited the Test Cases v9 IDs of AC15 to AC18.

**Change log.** D-RCV-60, 22 November 2026: the database slice of legacy RWB-ACE-001, restated for the target. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 27 November 2026: version 3 applies the listed RD-P1 rulings and review corrections.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P1-ACE001-DB). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (22 resolved, 38 cross-document, 2 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As an **ACE database engineer** (a role of the ACE team for which the roles table holds no code, CDC-02350), I want **the 14 tables and the 12 columns that the Workbench reads and ACE does not hold added to schema `public` with their business keys, one `ace_batch_run` row per source and business date written even for a zero-row delivery, one ingestion job per source that is idempotent on the business key, and SELECT on those 14 tables and 12 columns granted to `ace_view_owner` and to no one else**, so that **the Workbench reads one copy of ACE source data through the Section B views, holds no load or staging table of its own, and cannot write into ACE data at any point**.

This is the database half of legacy RWB-ACE-001. It delivers the 14 new ACE tables of section 11 (154 columns, as defined in ACE Field Gap List v2, sheet `ACE additions`, including the `ace_batch_run` and `party_product` metadata exceptions); the 12 new columns on `account` (7), `customer` (3) and `efs_action` (2), additive only; `ace_batch_run` with 9 columns, a primary key and the unique key `(source_system, business_date)`, written once per source and business date even for a zero-row delivery; one ACE ingestion job per source, idempotent on the business key, on ACE's own schedule; the ACE Field Gap List v2 fixture (81 field rows over 79 distinct ACE columns) and its conformance test; and the SELECT grant to `ace_view_owner`, the ACE regression proof and forward-only correction.

It creates no `recovery.v_ace_*` view, no view SQL and no view conformance test: those are RWB-P1-E1069-APP, and the 14 Section B views deploy after this story is reported done. It creates no table in `rwb_source_data` and issues no grant on a view.

### 2. Business rationale

ACE holds account, payment, customer, contact, collateral, the collateral asset, collections activity, assignment, bucket history, product, branch and holiday. It does not hold the appraisal, the CCMS collateral detail, the NPA asset and sale, the lawsuit and hearing, the proof of delivery, the GL write-off, the COLLINS score, the SCBPDM product holding, the NLEADS credit decision, the EasyApp signature reference or the Entra group mapping, it has no per-source business date record, and three tables ACE already holds are missing 12 columns the Workbench reads.

Without them the Workbench must own a load estate and a second copy of source data (DP-05, DP-17) or read the systems of record directly (REQ-DRI-006), and the target refuses both. This story is the third path and the one the legacy story chose: ACE ingests and owns the data and the Workbench reads it through SELECT-only views over ACE's own objects (ADR-010). The measure is the legacy one: all 81 field rows over 79 distinct columns populated to a value or an explicit null for one full file per source, and every ACE Field Gap List v2 field row resolving to its deployed column and type. It serves REQ-RDF-001 and REQ-RDF-002, and it is the precondition of DP01 to DP07 and DP11 as FSD P1 A2.14 reads them.

### 3. Preconditions

- The ACE schema in DEV and SIT is at the common migration head (V026 at the time of writing, legacy RWB-ACE-001 section 3). The ACE DBA allocates this story's migration version on the ACE schema's own Flyway sequence at build time, and the file keeps the legacy name form V<version>__rwb_ace_001_recovery_source_additions.sql. Until then the version number is Not specified in the source documents (GAP-2165; GAP-0517; CG-ALL-1839; ASM-3469).
- The ACE ingestion framework accepts a new source: a file or API contract, a staging-to-target mapper, a batch record writer and a unique business key per target table (legacy section 3).
- Each of the 14 ACE ingestion jobs keeps the interface number recorded from Interface Specifications v3; ACE keeps its own job names and cadence. Until they are recorded at build time, the numbers and cadence are Not specified in the source documents (GAP-0517; GAP-2165).
- The ACE DBA role that owns schema `public` is available for the migration window (RWB-E1-044 in the legacy set).
- The NOLOGIN role `ace_view_owner` exists, or is created once for the read path, and no credential appears in a migration, a script or a runbook (TSD P1 T6.3; DP-02). The grantee is `ace_view_owner` only: SELECT on the 14 tables goes to that role and the 12 columns are covered by the table SELECT. The service logins keep SELECT on the views and hold no public grant (GAP-2165; GAP-0518; ASM-3470).
- Each source owner has confirmed the field list: SVAF, CCMS, AMIS, RPS, LIT, WIN, GL, COLLINS, SCBPDM, NLEADS, EasyApp and the Entra ID administrator (legacy section 3).
- The conformance fixture is ACE Field Gap List v2, sheet `Fields` (81 ACE-new field rows over 79 distinct columns), held in the repository as a fixture; the table definitions are its sheet `ACE additions`. Both are copied, never re-derived.
- No approval is required to run a Draft migration on a development database; the migration reaches SIT once the tests in section 16 pass. DL43 is open (owner ACE team lead); this story is planned to its recommended answer A (RD-P1-043; ASM-5703).
- Until the Section B view migration is applied, the read flag rwb.dataengine.booking-facts stays off. The three Tier 2 fields principal_outstanding, settlement_booked_date and settlement_booked_amount answer fieldState NOT_AVAILABLE with no value, never a zero amount and never a default date (GAP-0596).
- Before the Section B additions land in an environment, freshness is read from v_ace_batch_status populated with synthetic batch rows in system test only. An environment without the view shows the data product as not stamped and never infers freshness from a row count, a file or a data date (GAP-1507).
- P1 writes no other service's schema. The cut-over package layout and the cut-over record are agreed at the cut-over rehearsal, and the extract carries legacy keys only (GAP-0532).
- No other service writes rwb_source_data. The command operations for the party flags and for contact consent and verification are to be defined in the P1 rwb-source-data contract (GAP-0245).
- While DL43 is open, the P3 features that read the Tier 2 additions (batch status, party product, credit decision) stay behind their feature flags until the additions land. The fallback date per flag is Not specified in the source documents (GAP-1557).
- For the AC4 check of the 12 columns: `ace_view_owner` holds USAGE on schema `public` and SELECT on `account`, `customer` and `efs_action` from RWB-P1-E1069-DB; the check queries these privileges first. Pending: ACE Source Views v2 gives the view-owner SELECT grants to RWB-P1-E1069-DB while this story also grants SELECT on the 14 new tables; one owner is to be named, owner solution architect, tracked as GAP-3534.
- The platform dependencies of the applied patterns DP-15 and DP-19 are recorded as notes and not in the metadata table; the build dependency stays None as the Work Package fixes it. Their names are Not specified in the source documents (GAP-2165).

### 4. Flow

1. ACE team: applies the ACE migration in DEV. The legacy file `V027__rwb_ace_001_recovery_source_additions.sql` is kept as the name and the source of the object list; the version on the ACE sequence is Not specified in the source documents (GAP-2165; ASM-3469). It creates the 14 tables and adds the 12 columns in one transaction.
2. ACE team: adds one ingestion job per source. Each writes its target table and one `ace_batch_run` row per source and business date, including a run that delivers no row. Job numbers, interface numbers and cadence are ACE's own (GAP-2165; ASM-3471).
3. ACE team: runs the population check (AC2) against one synthetic file per source with known expected values, then the conformance test (AC8) against `information_schema.columns`.
4. ACE team: runs the ACE regression suite (AC6) and confirms that no existing screen, batch job or report changes.
5. ACE DBA: grants SELECT on the 14 tables to `ace_view_owner` and revokes the same privileges from PUBLIC (AC4).
6. rwb-source-data, on its own Flyway sequence: creates the 14 Section B views and grants SELECT on each to the `rwb_source_data` login. That work is RWB-P1-E1069-APP and RWB-P1-E1069-DB, not this story.
7. ACE team: repeats steps 1 to 5 in SIT, then in the PROD window, and records the version and the checksum of the migration in the ACE release notes.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A source file fails its trailer or checksum | No target row of the file is kept; the one `ace_batch_run` row of the source and date reads FAILED; the latest COMPLETED row of an earlier date is unchanged | Pipeline log: trailer 41,200 does not match 41,197 rows for SVAF 2026-11-30 | AC3, AC11 |
| X2 | A field row of ACE Field Gap List v2 has no column after the migration | The conformance test fails and names the field ID and the column it expected | DF-COL-013 resolves to no column collateral_detail.insurance_expiry | AC8 |
| X3 | A source re-sends a business date already loaded | Target rows are upserted on their business keys and the single batch row of the source and date is updated; SQLSTATE 23505 applies only to a plain INSERT of an existing key | None | AC7, AC17 |
| X4 | A new column would rename, retype or drop an existing ACE column | The migration is rejected at review before it runs; the 12 columns are additive only | Review finding, no message id | AC1, AC6 |
| X5 | The grant reaches more than SELECT, or PUBLIC keeps a privilege | The grant check fails the security review and names the role, the privilege and the object | ace_view_owner holds INSERT on public.valuation; the view owner reads the 14 tables only | AC4 |
| X6 | A migration defect is found | P1 switches the Section B flags off; ACE corrects the schema only with a forward migration and records the migration history | Pipeline shows the corrective forward version and the old version retained | AC5 |

X1 to X6 are the legacy exception paths with the role and the schema named; a partial load is repaired by a re-run that upserts on the business key (AC7).

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs nothing from the recovery module; it is first on the recovery critical path and the source of the 14 tables every Section B view reads |
| Negotiable | The field list is fixed by ACE Field Gap List v2 and the 12 columns by section 11; the ingestion design, the constraint and index names and the job numbers are the ACE team's choice |
| Valuable | Removes 14 tables and a load estate from the Workbench and gives ACE one more complete source set, read through one grant on its own objects |
| Estimable | 14 tables, 12 columns, 14 ingestion jobs, one batch record, one grant, one conformance test, no down script; corrections use ACE-team forward migrations only (RD-P1-045) |
| Small | One migration plus the jobs; one slice of the legacy key, with the view SQL and the read path in RWB-P1-E1069 |
| Testable | Every criterion in section 7 is one catalogue query, one refused statement with its SQLSTATE, one ingestion run or one regression run |

### 7. Acceptance criteria

```gherkin
Feature: ACE DB additions for the Recovery Workbench

  Background:
    Given the ACE schema in DEV and SIT at the common migration head of section 3
    Given the role "ace_view_owner" exists in both environments

  Scenario: AC1 Tables and columns deployed (new, D-RCV-60)
    When the ACE team applies the ACE migration of section 11 in DEV and then in SIT
    Then schema public holds the 14 new tables of section 11.1
    Then account holds 7 new columns, customer 3 and efs_action 2, and the 12 columns of section 11.2 are the only columns added
    Then `ace_batch_run` matches its nine-column definition in ACE Field Gap List v2, sheet `ACE additions`, with a primary key and unique key `(source_system, business_date)`
    Then the columns of each of the 14 tables equal sheet "ACE additions" of ACE Field Gap List v2 in name, type, length and nullability
    Then the primary keys, unique business keys and foreign keys equal the Key column of that sheet
    Then ace_batch_run has no loaded_at column and party_product has no source_system column
    Then no existing ACE column is renamed, retyped or dropped
    Then no table outside the 14 is created and no column outside the 12 is added

  Scenario: AC2 Every Workbench field is populated (new, D-RCV-60)
    Given one synthetic file per source, with a known expected value for every field row of ACE Field Gap List v2, sheet "Fields", that the source feeds
    When ACE ingests each file for business date 2026-11-30 in a test container
    Then each target column of the 81 field rows equals its expected value, and is null only where the file omits it
    Then the row count per target table equals the file trailer count and is greater than 0
    # Pending: source_system codes and the source-to-job map, owner ACE ingestion owner, ASM-5695

  Scenario: AC3 Business date and completion recorded (new, D-RCV-60)
    Given the ALS file for business date 2026-11-30 completes at `2026-12-01T04:40:00+07:00` with record_count 184500
    When `public.ace_batch_run` is queried for ALS and 2026-11-30
    Then one `public.ace_batch_run` row contains ALS, 2026-11-30, `COMPLETED`, record_count 184500 and that completion time
    Then a failed run for 2026-12-01 writes one `FAILED` row and leaves 2026-11-30 as the latest successful `COMPLETED` row for ALS
    Then a successful rerun for 2026-12-01 updates that one row to `COMPLETED` with its record_count and completion time
    Then a delivery of zero rows still writes one ace_batch_run row for that source and business date

  Scenario: AC4 Read grant only (new, D-RCV-60)
    Given the role "ace_view_owner" and a test role "rwb_no_grant" that holds no grant anywhere
    When the ACE DBA applies the grant block of section 13
    Then ace_view_owner holds SELECT on each of the 14 new tables, and this story grants it nothing else
    Then the 12 new columns on account, customer and efs_action are readable by ace_view_owner through the SELECT on those tables
    Then an insert, update, delete or truncate by ace_view_owner on any table is refused with SQLSTATE 42501
    Then PUBLIC and `rwb_no_grant` hold no privilege on the 14 new tables; this story adds no privilege to existing account, customer or efs_action grants
    Then a select by rwb_no_grant is refused with SQLSTATE 42501

  Scenario: AC5 ACE-owned forward correction (RD-P1-045)
    Given a migration defect after Section B has been enabled
    When the ACE team disables its ingestion jobs and P1 switches the Section B feature flags off
    Then the defect is corrected only by an ACE-team forward migration; no down script or P1 script drops ACE objects (RD-P1-043, RD-P1-045)
    Then the ACE migration history lists the faulty version and the corrective version

  Scenario: AC6 Existing ACE reads unaffected (new, D-RCV-60)
    Given the ACE regression suite at a recorded version, run before the migration
    When it runs again after the migration
    Then no test that passed before fails after
    Then the row counts of account, payment, customer and efs_action are unchanged

  Scenario: AC7 Idempotent reload (new, D-RCV-60)
    Given a source file already ingested for 2026-11-30
    When a corrected redelivery with one changed value is ingested
    Then target rows are upserted on their business keys and the value is updated without duplicate keys
    Then the single `ace_batch_run` row for the source/date is updated
    Then deletion of target keys absent from the redelivery is Pending, owner ACE ingestion owner, tracked as GAP-3535

  Scenario: AC8 Field appendix matches the migration (new, D-RCV-60)
    Given the 81 ACE-new field rows of ACE Field Gap List v2, sheet "Fields", held as a repository fixture
    When the conformance test compares the fixture with information_schema.columns
    Then every row resolves to its named ACE table, column, type and length; the rows cover 79 distinct ACE columns (RD-P1-025, RD-P1-027)
    Then a fixture that drops one mapped column fails the build and names its field ID
    Then an extra mapped column, one present in a new ACE table and absent from the mapping sheet, fails the build; key and load metadata columns of sheet "ACE additions" are checked by AC1

  Scenario: AC9 Business rules BR1 to BR8 hold (new, D-RCV-60)
    Given the ACE schema with the migration of section 11 applied in DEV
    When the ACE team runs the constraint, grant and conformance checks of section 13 and the appendix test of AC8
    Then the 14 tables match ACE Field Gap List v2; `ace_batch_run` and `party_product` retain their defined column exceptions, and each present `business_date` is the source date (BR1)
    Then each of the 14 new tables has a unique constraint on its business key, and the Workbench links on that key (BR2)
    Then no existing ACE column is renamed, retyped or dropped (BR3)
    Then ace_batch_run holds one row per source and business date, including a zero-row delivery (BR4)
    Then ace_view_owner holds SELECT only, PUBLIC holds no grant and no service login holds a direct grant on the new tables; Section B access is through the rwb-source-data contract (RD-P1-043) (BR5)
    Then added columns are listed in ACE Field Gap List v2, sheet `ACE additions`; all 81 field rows in sheet `Fields` map to 79 distinct ACE columns (BR6)
    Then a repeat ingestion on (source_system, business_date) writes the same rows once and one batch record row (BR7)
    Then a column change without the matching ACE Field Gap List v2 fixture change fails the build (BR8)

  Scenario: AC10 No service login reads the new tables (TC-P1-ACE001-DB-01)
    Given every rwb_<name> service login, including rwb_source_data, and the rwb_no_grant role
    When each attempts SELECT on each of the 14 new tables
    Then each is refused with SQLSTATE 42501

  Scenario: AC11 A failed file leaves no partial target load (TC-P1-ACE001-DB-02)
    Given a SVAF file for 2026-11-30 whose trailer says 41,200 and which holds 41,197 rows
    When ACE ingests the file
    Then public.valuation is unchanged and ace_batch_run holds one FAILED row for SVAF and 2026-11-30

  Scenario: AC12 Partial load retry is idempotent (TC-P1-ACE001-DB-03)
    Given an ingestion job stops after writing part of a file
    When the same file is retried
    Then each business key is held once and one batch row exists for the source and date

  Scenario: AC13 Zero-row delivery is recorded (TC-P1-ACE001-DB-04)
    Given an ACE source file with trailer count 0
    When the ingestion job completes
    Then ace_batch_run has one row for the source and date with record_count 0 and status COMPLETED

  Scenario: AC14 Orphan business key (TC-P1-ACE001-DB-05)
    Given a lawsuit row whose account_key is not in public.account
    When the LIT file is ingested
    Then the row is not stored with a broken foreign key
    # Pending: reject the row or the whole file, and the job load order, owner ACE team lead, GAP-3576

  Scenario: AC15 An account delete takes its child rows with it (TC-P1-ACE001-DB-06)
    Given an account with rows in lawsuit, pod_receipt, gl_write_off, collins_score, credit_decision and esign_request
    When the existing ACE delete of that account runs
    Then it succeeds as it did before the migration and those child rows are deleted (D-RCV-35 cascade)
    # Pending: ON DELETE of the other foreign keys, owner ACE team lead, GAP-3576

  Scenario: AC16 The migration is atomic and runs once (TC-P1-ACE001-DB-07)
    Given a copy of the ACE head on which one statement of the migration fails
    When the migration runs
    Then none of the 14 tables and none of the 12 columns exists
    When the migration is run twice on a good copy
    Then the second run changes nothing

  Scenario: AC17 A duplicate business key is refused (TC-P1-ACE001-DB-08)
    Given one row in each of the 14 tables
    When a plain INSERT repeats its business key
    Then each insert is refused with SQLSTATE 23505

  Scenario: AC18 Job logs hold no personal value (TC-P1-ACE001-DB-09)
    Given synthetic files with marked person values in title_doc_no, plot_no and barcode
    When an ingestion succeeds and when it fails
    Then no log line holds a marked value
```

These criteria prove the database deliverable in the story title: the 14 tables, 12 columns, batch record, ingestion, grant, field fixture conformance and ACE regression behavior. No down script is used. No legacy criterion text is repeated. They answer the intent of legacy AC1 to AC8 of RWB-ACE-001 and leave the view SQL, the read contract and the freshness stamp to RWB-P1-E1069-APP and RWB-P1-E1015-APP.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every new table carries `source_system`, `business_date` and `loaded_at`, except that `ace_batch_run` has no `loaded_at` and `party_product` has no `source_system`; the business date is the source business date, not the ingest date | D-RCV-35 U2; legacy BR1; ACE Field Gap List v2 |
| BR2 | Every new table has a business key with a unique constraint; the Workbench links by that key and never by a generated id | D-RCV-35 U4; legacy BR2 |
| BR3 | New columns on existing ACE tables are additive only; no existing column is renamed, retyped or dropped | D-RCV-35 U3; legacy BR3 |
| BR4 | The batch record is one row per source and business date, written even when the source delivers zero rows | legacy BR4; TSD P1 T3.7 |
| BR5 | Selective grant: `ace_view_owner` reads the 14 new tables and the 12 new columns and writes nothing; PUBLIC holds nothing; no service login holds a grant in `public` | D-RCV-35 U4; TSD P1 T6.3; CTL-02 |
| BR6 | A field is in this story only if the Workbench reads it; a field the Workbench does not read is not added | legacy BR6; ACE Field Gap List v2 |
| BR7 | An ingestion job is idempotent on `(source_system, business_date)`: a repeat run writes the same rows once and one batch record row | legacy X3, AC7 |
| BR8 | The field appendix is the contract: a column change and the appendix change ship in the same pull request, and the conformance test fails the build on a mismatch | legacy section 15; AC8 |

**Where each rule lives.** BR1 to BR4 and BR7 are this story's objects and statements: the tables, the constraints, the batch record and the jobs. BR5 is the grant block of section 13, applied to `ace_view_owner` (ASM-3470); the login and the view grants that complete the read path are RWB-P1-E1069-DB's. BR6 and BR8 are the field fixture and its conformance test. The application rules the legacy set numbered BR9 to BR11 (batch gate, proof-of-delivery flag, wave plan) belong to the application stories of the gate (RWB-P1-E1018-APP), of proof of delivery and of delivery planning, and are not this story's. Decision DL43 is open (recommended answer A, RD-P1-043); its assumptions are ASM-0193, ASM-0737, ASM-0748 and ASM-0816.

### 9. State transitions

None on a case: this story changes the ACE schema version (the head to the next version on the ACE sequence) and the ingestion job set (14 jobs added).

| From | Event | Condition | To |
|---|---|---|---|
| the ACE schema at the common migration head | the ACE migration of section 13 | Every statement compiles against the head | 14 tables and 12 columns present, no existing column changed |
| no batch row for a source and business date | an ingestion run | The file passes its trailer and checksum | One `ace_batch_run` row for that source and date, status COMPLETED, with record_count, checksum and completed_at |
| no batch row for a source and business date | an ingestion run | The file fails its trailer or checksum | One row, status FAILED; the earlier COMPLETED rows are unchanged |
| a FAILED batch row | a successful rerun of the same date | The file passes | The same row reads COMPLETED. Pending: whether a RUNNING row is inserted at job start and who sets checksum and feed_version, owner ACE ingestion owner (GAP-3536) |
| a COMPLETED batch row | a corrected redelivery of the same business date | The business key already holds the row | Rows are upserted by the business key and the single batch row is updated; deletion of keys absent from the redelivery is Pending, owner ACE ingestion owner, tracked as GAP-3535 |
| migration applied | defect identified | Section B flags are off and ACE disables its ingestion jobs | Corrective ACE-team forward migration is applied; migration history is retained |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| ACE team lead | Owns the story, the estimate and the field appendix |
| ACE DBA | Applies the ACE-owned migration and grants; applies corrective forward versions when needed, after the Section B flags are off |
| ACE ingestion owner | Adds the 14 jobs and owns their interface numbers, schedule and re-run |
| `ace_view_owner` | Selects the 14 new tables and the 12 columns; writes nothing; owns the 30 views on the service sequence, not here |
| Recovery squad, data steward and data product owner | Read batch status and freshness through the rwb-source-data contract and SCR-44 only; no database grant to Section B views or `public` tables (RD-P1-043) |
| No approval level from the delegation of authority applies | A schema change is not a credit decision |

The owner of the 14 tables is the ACE team (legacy section 10). No personal name and no credential appears in a migration, a script or a runbook.

### 11. Data

**11.1 New tables.** 14 tables in schema `public`, 154 columns in all. Column names, types, lengths, nullability and constraints are normative in ACE Field Gap List v2, sheet `ACE additions` (166 definition rows); `source_system` values of `ace_batch_run` and the status values RUNNING, COMPLETED and FAILED are those the P1 readers use (RD-P1-041).

| Table | Columns | Source | Business key | Fields read by the Workbench |
|---|---:|---|---|---:|
| `ace_batch_run` | 9 | All sources | `(source_system, business_date)` | 0 |
| `valuation` | 11 | SVAF | `valuation_key` | 5 |
| `collateral_detail` | 15 | CCMS | `collateral_detail_key` | 9 |
| `npa_asset` | 14 | AMIS, RPS | `npa_asset_key` | 8 |
| `npa_sale` | 13 | AMIS | `npa_sale_key` | 7 |
| `lawsuit` | 15 | LIT | `lawsuit_key` | 9 |
| `hearing` | 9 | LIT | `hearing_key` | 3 |
| `pod_receipt` | 12 | WIN | `pod_key` | 5 |
| `gl_write_off` | 11 | GL | `write_off_key` | 5 |
| `collins_score` | 12 | COLLINS | `score_key` | 7 |
| `party_product` | 7 | SCBPDM | `(person_key, account_key, product_type, business_date)` | 4 |
| `credit_decision` | 10 | NLEADS | `credit_decision_key` | 4 |
| `esign_request` | 9 | EasyApp | `esign_key` | 1 |
| `iam_group` | 7 | Entra ID | `(entra_group, role_code)` | 1 |

Pending: `iam_group.iam_group_key` is NOT NULL in sheet `ACE additions` with no key, source or generation rule; how it is filled and whether it is unique, owner ACE team lead with the data architect, tracked as GAP-3537.

**11.2 New columns on existing tables.** 12 columns, additive only.

| Table | Column | Type | Source | Field ID |
|---|---|---|---|---|
| `account` | `business_unit` | varchar(10) | ALS | DF-ACC-006 |
| `account` | `principal_outstanding` | numeric(18,2) | ALS | DF-ACC-009 |
| `account` | `interest_outstanding` | numeric(18,2) | ALS | DF-ACC-010 |
| `account` | `fees_outstanding` | numeric(18,2) | ALS | DF-ACC-011 |
| `account` | `daily_bucket` | varchar(10) | ALS | DF-ACC-015 |
| `account` | `settlement_booked_date` | date | ALS | DF-ACC-030 |
| `account` | `settlement_booked_amount` | numeric(18,2) | ALS | DF-ACC-031 |
| `customer` | `party_type` | varchar(15) | SCBPDM | DF-PTY-003 |
| `customer` | `id_type` | varchar(20) | SCBPDM | DF-PTY-006 |
| `customer` | `segment` | varchar(20) | SCBPDM | DF-PTY-009 |
| `efs_action` | `contact_result` | varchar(20) | EFS | DF-INT-008, DF-INT-036 |
| `efs_action` | `action_contact_status` | varchar(20) | EFS | DF-INT-035 |

These 12 columns serve 13 field rows. No Section B view and no Section A view of ACE Source Views v2 selects them. Pending: the story that appends them to `v_ace_account`, `v_ace_customer` and `v_ace_efs_action`, owner data architect with the ACE team lead, tracked as GAP-3570.

**11.3 Field conformance.** The normative field set is the repository fixture copied from ACE Field Gap List v2, sheet `Fields`: 81 ACE-new field rows over 79 distinct ACE columns (RD-P1-025 item 7; RD-P1-027 item 4). `collins_score.model_version` serves DF-DEC-006 and DF-DEC-023, and `efs_action.contact_result` serves DF-INT-008 and DF-INT-036. The legacy appendix A (80 rows) is stale. A mapped column is an ACE column named in that sheet.

| Table | Fields | Source |
|---|---:|---|
| `customer` | 3 | SCBPDM |
| `account` | 7 | ALS |
| `collateral_detail` | 9 | CCMS |
| `valuation` | 5 | SVAF |
| `npa_asset` | 8 | AMIS, RPS |
| `credit_decision` | 4 | NLEADS |
| `lawsuit` | 9 | LIT |
| `pod_receipt` | 5 | WIN |
| `hearing` | 3 | LIT |
| `npa_sale` | 7 | AMIS |
| `efs_action` | 3 | EFS |
| `collins_score` | 7 | COLLINS |
| `gl_write_off` | 5 | GL |
| `iam_group` | 1 | Entra ID |
| `party_product` | 4 | SCBPDM |
| `esign_request` | 1 | EasyApp |
| **Total** | **81 field rows** | source codes and job map pending (ASM-5695) |

**Sources and jobs.** The tables above name 14 sources (ALS, SCBPDM, SVAF, CCMS, AMIS, RPS, LIT, WIN, GL, COLLINS, NLEADS, EasyApp, EFS and Entra ID). Pending: their `source_system` codes (the P1 seed proposes ALS, SCBPDM, SVAF, CCMS, AMIS, RPS, LIT, WIN, COLLINS, GL and EFS; ASM-5695), which job loads each table and the 12 columns (ALS and EFS included), and which jobs write `ace_batch_run`; owner ACE ingestion owner, tracked as ASM-5695 and GAP-2165.

**Ownership and grant.** The 14 tables are ACE-owned objects in schema `public`; only ACE creates, alters or drops them. This story grants SELECT on the 14 new tables to `ace_view_owner`. The service login `rwb_source_data` receives no grant here; RWB-P1-E1069-DB owns Section B view grants. No person or other service reads Section B views directly; batch status and freshness are exposed through the rwb-source-data contract only (RD-P1-043).

**Sequence note.** This story adds no object to schema `rwb_source_data`. The ACE migration runs on the ACE schema's own sequence and the ACE DBA allocates its version at build time (GAP-2165; ASM-3469). The rwb-source-data contract test consumes the versioned ACE Field Gap List v2 fixture; this story creates no P1 Flyway migration.

### 12. Contract

**12.1 REST operations provided**

None. This is a database story and publishes no operation.

**12.2 REST operations consumed**

None.

**12.3 Events published**

None. The topic of the service is `rwb.source-data.events.v1` with event names `rwb.source-data.<Event>.v1` (DP-14). `AceDataReady` and `AceDataLate` are RWB-P1-E1015-APP's, raised from `v_ace_batch_status`; a batch completion is a row, not an event this story publishes.

**12.4 Events consumed**

None.

**12.5 Workflows and activities**

None. The migration, the ingestion jobs and the conformance test are not Temporal workflows or activities, and the task queue `rwb-source-data` in namespace `rwb-recovery` is not used here.

**12.6 Schedules**

None in this story. The ingestion jobs are ACE's own jobs and keep ACE's own schedule: no cadence, cut-off or time is written here (GAP-2165; ASM-3471).

**12.7 Tables owned**

| Object | Schema | Owner | Created or altered here |
|---|---|---|---|
| `ace_batch_run` | `public` | ACE team | Created: 9 columns, primary key, unique key `(source_system, business_date)` |
| `valuation` | `public` | ACE team | Created: 11 columns, business key `valuation_key` |
| `collateral_detail` | `public` | ACE team | Created: 15 columns, business key `collateral_detail_key` |
| `npa_asset` | `public` | ACE team | Created: 14 columns, business key `npa_asset_key` |
| `npa_sale` | `public` | ACE team | Created: 13 columns, business key `npa_sale_key` |
| `lawsuit` | `public` | ACE team | Created: 15 columns, business key `lawsuit_key` |
| `hearing` | `public` | ACE team | Created: 9 columns, business key `hearing_key` |
| `pod_receipt` | `public` | ACE team | Created: 12 columns, business key `pod_key` |
| `gl_write_off` | `public` | ACE team | Created: 11 columns, business key `write_off_key` |
| `collins_score` | `public` | ACE team | Created: 12 columns, business key `score_key` |
| `party_product` | `public` | ACE team | Created: 7 columns, business key `(person_key, account_key, product_type, business_date)` |
| `credit_decision` | `public` | ACE team | Created: 10 columns, business key `credit_decision_key` |
| `esign_request` | `public` | ACE team | Created: 9 columns, business key `esign_key` |
| `iam_group` | `public` | ACE team | Created: 7 columns, business key `(entra_group, role_code)` |
| `account`, `customer`, `efs_action` | `public` | ACE team | Altered: the 12 columns of section 11.2 added, 7 + 3 + 2; no existing column changed |

No table in a `rwb_*` schema is created, altered or dropped here, and no `v_ace_*` view is created: the views are RWB-P1-E1069-APP's and the login and view grants are RWB-P1-E1069-DB's.

**12.8 Contract fakes**

| Fixture | Serves | Used by |
|---|---|---|
| ACE head fixture | `ACE Schema PostgreSQL v1.sql`, the head of section 3, with synthetic rows only | The migration and the regression suite run against it |
| One synthetic file per source | The sources of section 11.3, with known expected values; codes pending under ASM-5695 | AC2, AC7 and the conformance test; no production data in any file |
| Field fixture | ACE Field Gap List v2 sheet `Fields` (81 rows over 79 distinct columns) and sheet `ACE additions` (table definitions) | AC1, AC8 |
| No-grant role | The test role `rwb_no_grant`, holding no grant anywhere | AC4, the refusal with SQLSTATE 42501 |

A database story uses no service contract fake; these four fixtures stand in for the ACE head and the neighbouring stories.

**12.9 Call-type summary**

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | None | None | The base of the service is `/api/recovery/source-data/v1` and is not used in this story |
| Kafka | None | None | The topic `rwb.source-data.events.v1` belongs to RWB-P1-E1015-APP |
| Temporal | None | None | No workflow, activity or Schedule |
| File | None | None | The source files belong to ACE and are read by ACE's own ingestion jobs, not by this story |
| SQL | `SELECT` on the 14 tables and the 12 columns, granted to `ace_view_owner` | The source files, read by ACE's own ingestion | SQL only: SELECT for the view owner, no DML for that role, and no statement of this story reads a `rwb_*` schema |

### 13. Solution plan

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 is the reason the story exists: the 14 tables are the objects behind 14 Section B views and the Workbench reads them through the views, never directly. DP-15 is the sequence rule: the ACE migration runs on the ACE schema's own sequence (GAP-2165; ASM-3469) and the versioned ACE Field Gap List v2 fixture is the conformance contract; this story creates no P1 Flyway migration. DP-19 is named for completeness: the batch status these tables feed is shown on SCR-44, a gateway-bff composite route, and this story builds no screen. The empty, loading, error and no-access states of SCR-44 are owned by RWB-P1-AD018-APP, the SCR-44 interface story, and this story does not specify them. The dependencies of DP-15 and DP-19 are recorded here as notes and not in the metadata table, which the Work Package fixes as None (ASM-3473).

**Sequencing**

| Sequence | Version and file | Contents |
|---|---|---|
| ACE schema sequence | the version allocated at build time for `V027__rwb_ace_001_recovery_source_additions.sql`; the number is Not specified in the source documents (GAP-2165; ASM-3469) | 14 `CREATE TABLE`, 12 `ALTER TABLE ... ADD COLUMN`, the primary keys, the business-key unique constraints and the foreign keys to `account`, `asset`, `customer`, `npa_asset` and `lawsuit` |
| ACE schema sequence | the grant block of the same migration, applied by the ACE DBA | `GRANT SELECT` on the 14 tables to `ace_view_owner`, `REVOKE ALL` on the same 14 from PUBLIC |
| rwb-source-data sequence | None | This story creates no P1 Flyway version |
| ACE schema sequence | the corrective forward migration | Applies the next ACE-owned version; no down script is authored or run (RD-P1-045) |

**Table definitions.** The 14 tables and the 12 columns are those of sheet `ACE additions` of ACE Field Gap List v2, with the metadata columns and exceptions of BR1, the business keys of BR2, a primary key and the unique key `(source_system, business_date)` on `ace_batch_run` (BR4), and no existing ACE column renamed, retyped or dropped (BR3). Foreign keys: to `account`, `asset`, `customer`, `npa_asset` and `lawsuit` as the sheet lists them; ON DELETE beyond the account cascade of D-RCV-35 is Pending (GAP-3576). No row volume, lock-duration limit, foreign-key index or job completion time is set by any source: Pending, owner ACE DBA, tracked as GAP-3538.

**Grant block** (the legacy block, with the role named):

```sql
GRANT SELECT ON public.ace_batch_run, public.valuation, public.collateral_detail, public.npa_asset,
     public.npa_sale, public.lawsuit, public.hearing, public.pod_receipt, public.gl_write_off,
     public.collins_score, public.party_product, public.credit_decision, public.esign_request,
     public.iam_group TO ace_view_owner;

REVOKE ALL ON public.ace_batch_run, public.valuation, public.collateral_detail, public.npa_asset,
     public.npa_sale, public.lawsuit, public.hearing, public.pod_receipt, public.gl_write_off,
     public.collins_score, public.party_product, public.credit_decision, public.esign_request,
     public.iam_group FROM PUBLIC;
```

The 12 columns come with the SELECT the view owner already holds on `account`, `customer` and `efs_action`; no column-level grant and no `GRANT ... ON ALL TABLES` is written. No INSERT, UPDATE, DELETE or TRUNCATE is granted on any table.

**Correction and Section B gate.** If a migration defect is found, the P1 Section B flags are switched off first. The ACE team owns and applies a corrective forward migration; P1 does not reverse or drop ACE objects; the ACE team disables its own ingestion jobs (RD-P1-043, RD-P1-045).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `V027__rwb_ace_001_recovery_source_additions.sql` (legacy name; the version allocated on the ACE sequence) | Migration | The 14 tables, the 12 columns, the primary keys, the unique constraints and the foreign keys |
| 14 ingestion jobs and the `ace_batch_run` writer | ACE Spring Batch | One batch record row per source and business date, and one mapper per source writing its target table idempotently on the business key |
| `FieldAppendixConformanceTest` | Pipeline test | Compares the 81 field rows with `information_schema.columns` and names the field ID of any failure |
| `AceGrantCheck` | Pipeline check | `ace_view_owner` holds SELECT on the 14 tables and no DML, PUBLIC holds nothing, and the no-grant test role is refused |
| Corrective forward migration | ACE migration | The only correction of an applied migration (RD-P1-045) |

**Build steps**

1. The migration with the 14 tables and the 12 columns, with a fixture asserting the column counts of section 11 (AC1).
2. The batch record and its unique key, with a zero-row delivery fixture and a re-sent-date fixture (AC3, AC7).
3. The 14 jobs with one full synthetic file per source, and the comparison of each target row count with the file trailer (AC2).
4. `FieldAppendixConformanceTest`, with failing fixtures for a missing column, a wrong type and an extra mapped column (AC8).
5. The grant block and `AceGrantCheck` (AC4, AC10); the forward-only correction plan (AC5); row counts of `account`, `payment`, `customer` and `efs_action` before and after, then the ACE regression suite as the closing gate (AC6).

**Done when.** The migration applies, a correction would be an ACE-owned forward migration, the 14 tables and the 12 columns hold their counts and business keys, all ACE Field Gap List v2 field rows are populated from one full file per source, `ace_batch_run` holds one row per source and business date, `ace_view_owner` holds SELECT on the 14 tables and nothing else, the conformance test and the ACE regression suite pass, and the tests in section 16 are green.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| Conformance check 1 | A field row resolves to no column | DF-COL-013 resolves to no column collateral_detail.insurance_expiry |
| Conformance check 2 | A field row resolves to a column of the wrong type | DF-PTY-009 resolves to customer.segment of type text; varchar(20) expected |
| Conformance check 3 | A deployed mapped column has no appendix row | account.settlement_booked_amount is deployed and has no appendix row |
| Grant check | The view owner holds more than SELECT, or PUBLIC holds a privilege | ace_view_owner holds INSERT on public.valuation; the view owner reads the 14 tables only |
| SQLSTATE 42501 | A role without the grant selects a table | Tests assert the SQLSTATE only; the text depends on the schema privilege of the role |
| SQLSTATE 23505 | A second row for one business key | duplicate key value violates unique constraint ace_batch_run_source_system_business_date_key |

These are pipeline and build log texts in the style of RWB-E1-069, for developers; they are not part of the message standard. No `MSG-` ID applies: this story raises no user-facing message, and the messages of the read path are raised by RWB-P1-E1069-APP and by the guard library.

### 15. Screens and states

No screen in this story. The result is visible in the ACE release pipeline and in the ACE Flyway history, and the platform administrator reads the ACE batch status per source and business date on SCR-44 Interface and job monitor under Platform administration R; the data steward reads the same batch status for freshness and changes nothing. The 14 tables are never shown directly to a user: they are read through the 14 Section B views and the service contract, never through SQL on a screen.

The SCR-44 empty, loading, error and no-access states belong to RWB-P1-AD018-APP. Their content is Not specified in the source documents (CG-ALL-1840), because Screen Specifications v1 also lacks them.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-ACE-001-01 | AC1; BR1, BR2; legacy AC1 tables and columns deployed | End to end | Clean PostgreSQL container at the ACE head, then the migration; column and constraint query against sheet `ACE additions` |
| TC-ACE-001-02 | AC2; legacy AC2 every field populated | End to end | One synthetic file per source for 2026-11-30 with expected values; row count per table against the trailer |
| TC-ACE-001-03 | AC3; BR4; legacy AC3 business date and completion | End to end | ALS file for 2026-11-30 completing at 2026-12-01T04:40:00+07:00 with record_count 184500; a failed and then successful run for 2026-12-01; read of public.ace_batch_run |
| TC-ACE-001-04 | AC4; BR5; legacy AC4 read grant only | End to end | Sessions as `ace_view_owner` and `rwb_no_grant`; privilege query for PUBLIC, `rwb_no_grant` and `ace_view_owner` over the 14 tables and the 3 altered tables |
| TC-ACE-001-05 | AC5; legacy AC5, restated as forward correction | End to end | Synthetic copy of the SIT schema, a faulty and a corrective migration version; migration history |
| TC-ACE-001-06 | AC6; BR3; legacy AC6 existing ACE reads unaffected | End to end | The ACE regression suite over every existing screen, batch job and report |
| TC-ACE-001-07 | AC7; BR7; legacy AC7 idempotent reload | End to end | A corrected 2026-11-30 redelivery with one changed value; row counts per business key and one row in `ace_batch_run` |
| TC-ACE-001-08 | AC8; BR6; BR8; legacy AC8 field appendix matches | End to end | The 81 field rows against `information_schema.columns`; a missing column, a wrong type and an extra mapped column |
| TC-P1-ACE001-DB-01 to TC-P1-ACE001-DB-05 | AC10 to AC14 | Component | As the scenarios of section 7 |
| TC-P1-ACE001-DB-06 to TC-P1-ACE001-DB-09 | AC15 to AC18 | Component | Account delete, atomic migration, duplicate key, job logs |
| TC-ACE-001-10 | AC9; BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8 | End to end | The ACE schema in DEV with the migration of section 11 applied; the constraint, grant and conformance checks of section 13; a repeat ingestion and a zero-row delivery; a column change without the matching appendix change |

The legacy TC IDs are kept character for character and the legacy level "System" maps to "End to end". TC-ACE-001-10 proves AC9. TC-ACE-001-09 tests application behaviour (the batch gate) and is to move to the story of the gate; TC-P1-E1069-APP-11 does not exercise this grant and is not evidence for this story. The full test of each case, with its Given, When and Then, is in Recovery Workbench Test Cases v9.xlsx, tab Story test cases; it holds AC1 to AC18 as worded in this version.

### 17. Guardrails

- No business value in a migration: the field list and the 12 columns are copied from the appendix and section 11.2, and every list of values comes from the source or from reference data, never from a constant written here.
- Personal data columns of the new base tables include `collateral_detail.title_doc_no` and `plot_no`, `lawsuit.black_case_no`, `red_case_no` and `court_name`, `pod_receipt.barcode`, `party_product.person_key` and `customer` identifiers, classified Confidential in Data Classification v6 and masked in UAT; a full column-level list and the non-production retention rule are Pending, owner compliance with the data owner (GAP-3539). No personal data in a migration, a script, a job log, a test fixture or a runbook: the fixtures are synthetic, `person_key` and `account_key` are business keys, and no file carries production data.
- No write path into ACE data: `ace_view_owner` holds SELECT on the 14 tables and nothing else, and PUBLIC holds nothing.
- No copy of an ACE column into a `rwb_*` schema and no foreign key from a Workbench table into `public` (DP-01, DP-05).
- No business date written by the Workbench: the business date is the source business date from the batch record (BR1; FSD P1 A2.14), and no cadence or interface number is invented for the 14 jobs (ASM-3471).
- An applied migration is never edited: a correction is a new version on the ACE sequence, a forward migration is the only correction; applied migrations are never reversed, and the 14 tables stay ACE's, so no service story creates, alters or drops one of them.

### 18. Traceability

| Requirement ID | Requirement (quoted) | Source | Rules | Test cases |
|---|---|---|---|---|
| REQ-RDF-001 | Recovery data is held in 14 data products, each with exactly one named system of record, "ACE (ingested from X)" or the Workbench, and one named owner. | FSD P1 v3, Requirements served | BR1, BR2, BR6; D-RCV-35 U2 | TC-ACE-001-01, TC-ACE-001-02, TC-ACE-001-08, TC-ACE-001-10 |
| REQ-RDF-002 | Account balance, arrears, payments and classification for every account at 90 or more days past due are read from ACE through v_ace_account and v_ace_payment, current to the previous working day. | FSD P1 v3, Requirements served | BR3, BR4, BR6; D-RCV-35 U3 | TC-ACE-001-02, TC-ACE-001-03, TC-ACE-001-07, TC-ACE-001-10 |
| D-RCV-35 U2 | The ACE team owns the new ACE tables and columns; the Workbench reads them and adds only its own records. | Decision Log, D-RCV-35 | BR1 to BR8 | all |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-P1-E1069-APP | App development | Consumer: the 14 Section B views and the read contract over the 14 tables; its Section B migration runs after this story is reported done |
| RWB-P1-E1069-DB | ACE DB | Sibling: the `rwb_source_data` login, the view grants and the ownership of the 30 views by `ace_view_owner`; it creates none of these 14 tables |
| RWB-P1-E1015-APP | App development | Consumer: the freshness stamp per data product, read from `v_ace_batch_status` over `ace_batch_run` |
| RWB-P1-AD018-APP | App development | Consumer: the SCR-44 interface and job monitor, which shows the ACE batch status per source and business date |

The field appendix is the contract: if a column changes, ACE Field Gap List v2 and the gap sheet of Source to Target Mapping v7 change in the same pull request, and the conformance test fails the build on a mismatch.

### 19. Out of scope

- The 30 `recovery.v_ace_*` views, the view SQL, the three helper functions and the view conformance test: RWB-P1-E1069-APP.
- The `rwb_source_data` login, the query on the views, the view grants and the four extension tables: RWB-P1-E1069-DB.
- The freshness stamp and the events `AceDataReady` and `AceDataLate`: RWB-P1-E1015-APP.
- Adding the 12 columns to the three views (GAP-3570), and the application rules for the batch gate and the flags.
- The file specifications, the interface numbers and the schedule of the 14 ingestion jobs: ACE's own, named by reference and not restated here (ASM-3471).
- The masking of a personal field on the read path and the authorise check: rwb-access, RWB-P4-E1069-APP.
- Any change to the field appendix or to the 12 columns without a new version of the appendix, and performance tuning beyond the primary keys and the business-key unique constraints named here.

### 20. Remaining delivery steps

- Size: Not specified; owner ACE team lead.
- Epic design sign-off and DL43 acceptance: Pending; owner ACE team lead (RD-P1-043 is a planning basis only).
- ACE sequence version: Not specified; owner ACE DBA (GAP-2165).
- Source codes and job map: Pending; owner ACE ingestion owner (ASM-5695).
- Foreign-key delete rules, orphan handling and load order: Pending; owner ACE team lead (GAP-3576).
- The 12 columns in the views: Pending; owner data architect with the ACE team lead (GAP-3570).
- Tier 2 grant owner, redelivery deletions, batch row at job start, iam_group_key, volumes and window, classification list: Pending (GAP-3534 to GAP-3539).
- Section B migration and feature flags: deploy after the ACE dependency gate passes; owner release owner with ACE team lead (RD-P1-043).
- Test data in DEV: Pending; owner ACE ingestion owner.
- Down script: Not applicable; corrections use ACE-team forward migrations only (RD-P1-045).
