# RWB-P1-ACE001-DB ACE DB additions for the Recovery Workbench

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P1-ACE001-DB |
| Work type | DB (ACE DB) |
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
| Depends on (build) | None |
| Contract dependencies | None: this DB story publishes no API contract, so no contract or CON dependency applies |
| Contract fake library version | None published: this DB story publishes no contract fake (DOR-RWB-P1-ACE001-DB-22) |
| Contract version | Not applicable: this DB story builds against no API contract version; it publishes no contract, has no contract dependency and does not use the `/v1` base path of the service |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v1.md (FR-P1-001, FR-P1-002, FR-P1-005, FR-P1-007, FR-P1-008, FR-P1-010, FR-P1-012, FR-P1-013, FR-P1-029) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: the database slice of legacy RWB-ACE-001, restated for the target. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P1-ACE001-DB). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (22 resolved, 38 cross-document, 2 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As an **ACE database engineer**, I want **the 14 tables and the 12 columns that the Workbench reads and ACE does not hold added to schema `public` with their business keys, one `ace_batch_run` row per source and business date written even for a zero-row delivery, one idempotent ingestion job per source keyed on `(source_system, business_date)`, and SELECT on those 14 tables and 12 columns granted to `ace_view_owner` and to no one else**, so that **the Workbench reads one copy of ACE source data through the Section B views, holds no load or staging table of its own, and cannot write into ACE data at any point**.

This is the database half of legacy RWB-ACE-001. It delivers the 14 new ACE tables of section 11 (154 columns, each with `source_system`, `business_date`, `loaded_at` and a unique business key); the 12 new columns on `account` (7), `customer` (3) and `efs_action` (2), additive only; `ace_batch_run` with 9 columns, a primary key and the unique key `(source_system, business_date)`, written once per source and business date even for a zero-row delivery; one ACE ingestion job per source, idempotent on the business key, on ACE's own schedule; the 80-row field appendix and its conformance test; and the selective grant to `ace_view_owner` with the PUBLIC revoke, the down script and the ACE regression proof.

It creates no `recovery.v_ace_*` view, no view SQL and no view conformance test: those are RWB-P1-E1069-APP, and the 14 Section B views deploy after this story is reported done. It creates no table in `rwb_source_data` and issues no grant on a view.

### 2. Business rationale

ACE holds account, payment, customer, contact, collateral, the collateral asset, collections activity, assignment, bucket history, product, branch and holiday. It does not hold the appraisal, the CCMS collateral detail, the NPA asset and sale, the lawsuit and hearing, the proof of delivery, the GL write-off, the COLLINS score, the SCBPDM product holding, the NLEADS credit decision, the EasyApp signature reference or the Entra group mapping, it has no per-source business date record, and three tables ACE already holds are missing 12 columns the Workbench reads.

Without them the Workbench must own a load estate and a second copy of source data (DP-05, DP-17) or read the systems of record directly (REQ-DRI-006), and the target refuses both. This story is the third path and the one the legacy story chose: ACE ingests and owns the data and the Workbench reads it through SELECT-only views over ACE's own objects (ADR-010). The measure is the legacy one: 80 of 80 appendix fields populated to a value or an explicit null for one full file per source, and 80 of 80 field rows resolving to a deployed column of the right type. It serves REQ-RDF-001 and REQ-RDF-002, and it is the precondition of DP01 to DP07 and DP11 as FSD P1 A2.14 reads them.

### 3. Preconditions

- The ACE schema in DEV and SIT is at the common migration head (V026 at the time of writing, legacy RWB-ACE-001 section 3). The ACE DBA allocates this story's migration version on the ACE schema's own Flyway sequence at build time, and the file keeps the legacy name form V<version>__rwb_ace_001_recovery_source_additions.sql. Until then the version number is Not specified in the source documents (GAP-2165; GAP-0517; CG-ALL-1839; ASM-3469).
- The ACE ingestion framework accepts a new source: a file or API contract, a staging-to-target mapper, a batch record writer and a unique business key per target table (legacy section 3).
- Each of the 14 ACE ingestion jobs keeps the interface number recorded from Interface Specifications v3; ACE keeps its own job names and cadence. Until they are recorded at build time, the numbers and cadence are Not specified in the source documents (GAP-0517; GAP-2165).
- The ACE DBA role that owns schema `public` is available for the migration window (RWB-E1-044 in the legacy set).
- The NOLOGIN role `ace_view_owner` exists, or is created once for the read path, and no credential appears in a migration, a script or a runbook (TSD P1 T6.3; DP-02). The grantee is `ace_view_owner` only: SELECT on the 14 tables goes to that role and the 12 columns are covered by the table SELECT. The service logins keep SELECT on the views and hold no public grant (GAP-2165; GAP-0518; ASM-3470).
- Each source owner has confirmed the field list: SVAF, CCMS, AMIS, RPS, LIT, WIN, GL, COLLINS, SCBPDM, NLEADS, EasyApp and the Entra ID administrator (legacy section 3).
- The 80-row field appendix is taken from legacy RWB-ACE-001 appendix A and sheet `Fields` of the accompanying workbook; it is copied, never re-derived.
- No approval is required to run a Draft migration on a development database; the migration reaches SIT once the tests in section 16 pass. DL43 is treated as accepted for this run and recorded as an assumption (ASM-3472).
- Until the Section B view migration is applied, the read flag rwb.dataengine.booking-facts stays off. The three Tier 2 fields principal_outstanding, settlement_booked_date and settlement_booked_amount answer fieldState NOT_AVAILABLE with no value, never a zero amount and never a default date (GAP-0596).
- Before the Section B additions land in an environment, freshness is read from v_ace_batch_status populated with synthetic batch rows in system test only. An environment without the view shows the data product as not stamped and never infers freshness from a row count, a file or a data date (GAP-1507).
- P1 writes no other service's schema. The cut-over package layout and the cut-over record are agreed at the cut-over rehearsal, and the extract carries legacy keys only (GAP-0532).
- No other service writes rwb_source_data. The command operations for the party flags and for contact consent and verification are to be defined in the P1 rwb-source-data contract (GAP-0245).
- DL43 is open: the P3 features that read the Tier 2 additions (batch status, party product, credit decision) stay behind their feature flags until the additions land. The fallback date per flag is Not specified in the source documents (GAP-1557).
- The platform dependencies of the applied patterns DP-15 and DP-19 are recorded as notes and not in the metadata table; the build dependency stays None as the Work Package fixes it. Their names are Not specified in the source documents (GAP-2165).

### 4. Flow

1. ACE team: applies the ACE migration in DEV. The legacy file `V027__rwb_ace_001_recovery_source_additions.sql` is kept as the name and the source of the object list; the version on the ACE sequence is Not specified in the source documents (GAP-2165; ASM-3469). It creates the 14 tables and adds the 12 columns in one transaction.
2. ACE team: adds one ingestion job per source. Each writes its target table and one `ace_batch_run` row per source and business date, including a run that delivers no row. Job numbers, interface numbers and cadence are ACE's own (GAP-2165; ASM-3471).
3. ACE team: runs the population check (AC2) against one full synthetic file per source, then the field-appendix conformance test (AC8) against `information_schema.columns`.
4. ACE team: runs the ACE regression suite (AC6) and confirms that no existing screen, batch job or report changes.
5. ACE DBA: grants SELECT on the 14 tables to `ace_view_owner` and revokes the same privileges from PUBLIC (AC4).
6. rwb-source-data, on its own Flyway sequence: creates the 14 Section B views and grants SELECT on each to the `rwb_source_data` login. That work is RWB-P1-E1069-APP and RWB-P1-E1069-DB, not this story.
7. ACE team: repeats steps 1 to 5 in SIT, then in the PROD window, and records the version and the checksum of the migration in the ACE release notes.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A source file fails its trailer or checksum | The ingestion writes no row for that source and business date; `ace_batch_run` keeps the previous COMPLETED row as the latest | Pipeline log: trailer 41,200 does not match 41,197 rows for SVAF 2026-11-30 | AC3 |
| X2 | A field row of appendix A has no column after the migration | The conformance test fails and names the field ID and the column it expected | DF-COL-013 resolves to no column collateral_detail.insurance_expiry | AC8 |
| X3 | A source re-sends a business date already loaded | The unique business key rejects the duplicate and the batch record keeps one row for that source and date | SQLSTATE 23505 duplicate key value violates unique constraint ace_batch_run_source_system_business_date_key | AC7 |
| X4 | A new column would rename, retype or drop an existing ACE column | The migration is rejected at review before it runs; the 12 columns are additive only | Review finding, no message id | AC1, AC6 |
| X5 | The grant reaches more than SELECT, or PUBLIC keeps a privilege | The grant check fails the security review and names the role, the privilege and the object | ace_view_owner holds INSERT on public.valuation; the view owner reads the 14 tables only | AC4 |
| X6 | The migration must be backed out | The down script drops the 14 tables and the 12 columns in reverse dependency order; no ACE row is touched | Pipeline log: 14 tables dropped, 12 columns dropped | AC5 |

X1 to X6 are the legacy exception paths with the role and the schema named; a partial load is repaired by a re-run that upserts on the business key (AC7).

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs nothing from the recovery module; it is first on the recovery critical path and the source of the 14 tables every Section B view reads |
| Negotiable | The field list is fixed by appendix A and the 12 columns by section 11; the ingestion design, the constraint and index names and the job numbers are the ACE team's choice |
| Valuable | Removes 14 tables and a load estate from the Workbench and gives ACE one more complete source set, read through one grant on its own objects |
| Estimable | 14 tables, 12 columns, 14 ingestion jobs, one batch record, one grant, one conformance test, one down script |
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
    Then ace_batch_run holds 9 columns, a primary key and the unique key (source_system, business_date)
    Then each of the 14 tables carries source_system, business_date and loaded_at
    Then no existing ACE column is renamed, retyped or dropped
    Then no table outside the 14 is created and no column outside the 12 is added

  Scenario: AC2 Every Workbench field is populated (new, D-RCV-60)
    Given one full synthetic file for each of the 12 sources in the field appendix of section 11.3
    When ACE ingests each file for business date 2026-11-30 in a test container
    Then all 80 appendix A fields hold a value or an explicit null
    Then the row count per target table equals the file trailer count

  Scenario: AC3 Business date and completion recorded (new, D-RCV-60)
    Given the ALS file for 2026-11-30 is ingested and completes at 04:40
    When the view owner reads v_ace_batch_status for ALS and 2026-11-30
    Then it returns ALS, 2026-11-30, COMPLETED, the record count and the completion time
    Then a failed run for 2026-12-01 leaves 2026-11-30 as the latest COMPLETED row for ALS
    Then a delivery of zero rows still writes one ace_batch_run row for that source and business date

  Scenario: AC4 Read grant only (new, D-RCV-60)
    Given the role "ace_view_owner" and a test role "rwb_no_grant" that holds no grant anywhere
    When the ACE DBA applies the grant block of section 13
    Then ace_view_owner holds SELECT on each of the 14 new tables and on no other table added by this story
    Then the 12 new columns on account, customer and efs_action are readable by ace_view_owner through the SELECT on those tables
    Then an insert, update, delete or truncate by ace_view_owner on any table is refused with SQLSTATE 42501
    Then PUBLIC holds no privilege on any of the 14 tables or the 12 columns
    Then a select by rwb_no_grant is refused with SQLSTATE 42501

  Scenario: AC5 Reversible (new, D-RCV-60)
    Given a copy of the ACE schema with the migration applied
    When the down script of section 13 runs
    Then the 14 tables and the 12 columns are gone
    Then the account, payment, customer and efs_action row counts are unchanged
    Then the 14 ingestion jobs write no row after the down script

  Scenario: AC6 Existing ACE reads unaffected (new, D-RCV-60)
    Given the ACE regression suite
    When it runs after the migration
    Then every existing screen, batch job and report passes
    Then the row counts of account, payment, customer and efs_action are unchanged

  Scenario: AC7 Idempotent reload (new, D-RCV-60)
    Given a source file already ingested for 2026-11-30
    When the same file is ingested again
    Then no duplicate row is created
    Then ace_batch_run holds one row for that source and business date
    Then the reload is keyed on (source_system, business_date) and writes no second row

  Scenario: AC8 Field appendix matches the migration (new, D-RCV-60)
    Given the 80 rows of appendix A of legacy RWB-ACE-001
    When the conformance test compares them with information_schema.columns
    Then 80 of 80 resolve to a column of the right type
    Then no appendix row is missing and no extra mapped column exists
    Then the test names the field ID of any row that fails

  Scenario: AC9 Business rules BR1 to BR8 hold (new, D-RCV-60)
    Given the ACE schema with the migration of section 11 applied in DEV
    When the ACE team runs the constraint, grant and conformance checks of section 13 and the appendix test of AC8
    Then each of the 14 new tables holds source_system, business_date and loaded_at, and business_date is the source business date (BR1)
    Then each of the 14 new tables has a unique constraint on its business key, and the Workbench links on that key (BR2)
    Then no existing ACE column is renamed, retyped or dropped (BR3)
    Then ace_batch_run holds one row per source and business date, including a zero-row delivery (BR4)
    Then ace_view_owner holds SELECT only, PUBLIC holds no grant and no service login holds a grant in public (BR5)
    Then every added column is listed in appendix A and every appendix A field is read by the Workbench (BR6)
    Then a repeat ingestion on (source_system, business_date) writes the same rows once and one batch record row (BR7)
    Then a column change without the matching appendix change fails the build (BR8)
```

These nine criteria are new and prove only the database deliverable in the story title: the 14 tables, the 12 columns, the batch record, the ingestion, the grant, the down script and the appendix conformance. No legacy criterion text is repeated. They answer the intent of legacy AC1 to AC8 of RWB-ACE-001 and leave the view SQL, the read contract and the freshness stamp to RWB-P1-E1069-APP and RWB-P1-E1015-APP.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every new table carries `source_system`, `business_date` and `loaded_at`; the business date is the source business date, not the ingest date | D-RCV-35 U2; legacy BR1 |
| BR2 | Every new table has a business key with a unique constraint; the Workbench links by that key and never by a generated id | D-RCV-35 U4; legacy BR2 |
| BR3 | New columns on existing ACE tables are additive only; no existing column is renamed, retyped or dropped | D-RCV-35 U3; legacy BR3 |
| BR4 | The batch record is one row per source and business date, written even when the source delivers zero rows | legacy BR4; TSD P1 T3.7 |
| BR5 | Selective grant: `ace_view_owner` reads the 14 new tables and the 12 new columns and writes nothing; PUBLIC holds nothing; no service login holds a grant in `public` | D-RCV-35 U4; TSD P1 T6.3; CTL-02 |
| BR9 | While `v_ace_batch_status` does not exist, the batch gate answers as for an incomplete batch: 409 with MSG-P1-001, no candidate and no break row; DP01 is never stamped LOADED for the date, so no case is created for it. The gate reads the view only and is never inferred from data_as_of, a row count or a file | FSD P1 OQ-P1-01; ASM-B-P1-07-E1018-4 |
| BR10 | Proof-of-delivery capture stays behind its feature flag until RWB-ACE-001 lands and `v_ace_pod` is available; the fallback (proof entered by hand against the barcode) is agreed with the litigation business owner before wave 2 | FSD P6 AC-ALT-P6-001-01 to -02; DL43 |
| BR11 | Wave 1 delivers the 16 Section A views, the four extension tables, the dictionary, the reconciliation, the case list and the ledger; the 14 Section B views, the batch-status freshness source and every Tier 2 feature stay behind their flags until RWB-ACE-001 lands; the fallback freshness source (CG-9) is confirmed before system test; the asset_key proof runs from Day 1 against v_ace_asset and v_ace_collateral; the valuation_key proof runs against v_ace_valuation from the week RWB-ACE-001 lands and against its contract fake before that week; the appraisal acceptance rows load in both cases, as they are Workbench decisions keyed by an ACE business key with no foreign key; the cutover stays behind its feature switch until the Section B views answer, so no day is counted clean on a STALE DP06 stamp | FSD P1 OQ-P1-01, A2.1; Arch v5 slide 41; DL43 |
| BR6 | A field is in this story only if the Workbench reads it; a field the Workbench does not read is not added | legacy BR6; appendix A |
| BR7 | An ingestion job is idempotent on `(source_system, business_date)`: a repeat run writes the same rows once and one batch record row | legacy X3, AC7 |
| BR8 | The field appendix is the contract: a column change and the appendix change ship in the same pull request, and the conformance test fails the build on a mismatch | legacy section 15; AC8 |

**Where each rule lives.** BR1 to BR4 and BR7 are this story's objects and statements: the tables, the constraints, the batch record and the jobs. BR5 is the grant block of section 13, applied to `ace_view_owner` (ASM-3470); the login and the view grants that complete the read path are RWB-P1-E1069-DB's. BR6 and BR8 are the appendix and its conformance test, copied from the legacy story and never re-derived. Open decision DL43 (cited by BR10 and BR11) is still open; its assumptions are ASM-0193, ASM-0737, ASM-0748 and ASM-0816.

### 9. State transitions

None on a case: this story changes the ACE schema version (the head to the next version on the ACE sequence) and the ingestion job set (14 jobs added).

| From | Event | Condition | To |
|---|---|---|---|
| the ACE schema at the common migration head | the ACE migration of section 13 | Every statement compiles against the head | 14 tables and 12 columns present, no existing column changed |
| no batch row for a source and business date | an ingestion run | The file passes its trailer and checksum | One `ace_batch_run` row for that source and date, with `is_complete`, the record count and the completion time |
| no batch row for a source and business date | an ingestion run | The file fails its trailer or checksum | No row written for that date; the previous COMPLETED row stays the latest |
| a COMPLETED batch row | a repeat delivery of the same business date | The business key already holds the row | The row is refreshed once; no duplicate row and no second batch record row |
| the migration applied | the down script | The reversal is authorised | 14 tables and 12 columns gone, no ACE row touched |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| ACE team lead | Owns the story, the estimate and the field appendix |
| ACE DBA | Applies the migration, the grant and the down script in DEV, SIT and the release window |
| ACE ingestion owner | Adds the 14 jobs and owns their interface numbers, schedule and re-run |
| `ace_view_owner` | Selects the 14 new tables and the 12 columns; writes nothing; owns the 30 views on the service sequence, not here |
| Recovery squad, data steward and data product owner | Read the 14 Section B views and the batch status per source and business date; hold no grant on a `public` table and change nothing |
| No approval level from the delegation of authority applies | A schema change is not a credit decision |

The owner of the 14 tables is the ACE team (legacy section 10). No personal name and no credential appears in a migration, a script or a runbook.

### 11. Data

**11.1 New tables.** 14 tables in schema `public`, 154 columns in all.

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
| `collins_score` | 12 | COLLINS | `score_key` | 6 |
| `party_product` | 7 | SCBPDM | `(person_key, account_key, product_type, business_date)` | 4 |
| `credit_decision` | 10 | NLEADS | `credit_decision_key` | 4 |
| `esign_request` | 9 | EasyApp | `esign_key` | 1 |
| `iam_group` | 7 | Entra ID | `(entra_group, role_code)` | 1 |

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

**11.3 The 80 fields.** The full table, with source field and frequency, is appendix A of legacy RWB-ACE-001 and sheet `Fields` of the workbook; this is the summary that AC2 and the conformance test count.

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
| `collins_score` | 6 | COLLINS |
| `gl_write_off` | 5 | GL |
| `iam_group` | 1 | Entra ID |
| `party_product` | 4 | SCBPDM |
| `esign_request` | 1 | EasyApp |
| **Total** | **80** | 12 sources |

**Ownership and grant.** The 14 tables are ACE's own objects in schema `public` and are **not** rows of the Ownership Map, which covers the `rwb_*` schemas only; the owner is the ACE team (legacy section 10) and no story of the 19 services creates, alters or drops them. The 12 columns belong to tables ACE already owns, on the same terms. `ace_view_owner` already reads the Tier 1 tables behind the 16 Section A views (TSD P1 T6.3); this story adds SELECT on the 14 new tables and with them the 12 new columns, and nothing else.

**Sequence note.** This story adds no object to schema `rwb_source_data`. The ACE migration runs on the ACE schema's own sequence and the ACE DBA allocates its version at build time (GAP-2165; ASM-3469). The one P1 Flyway version that this story needs records the field-appendix conformance contract in `flyway_schema_history` in schema `rwb_source_data` and creates no table.

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

None in this story. The 14 ingestion jobs are ACE's own Spring Batch jobs and keep ACE's own schedule: no cadence, cut-off or time is written here (GAP-2165; ASM-3471).

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
| ACE head fixture | `ACE Schema PostgreSQL v1.sql`, the head of section 3 | The migration and the regression suite run against it |
| One full synthetic file per source | The 12 sources of section 11.3 | AC2, AC7 and the conformance test; no production data in any file |
| Field-appendix fixture | The 80 rows of appendix A of legacy RWB-ACE-001 | AC8, the row-by-row comparison with `information_schema.columns` |
| No-grant role | The test role `rwb_no_grant`, holding no grant anywhere | AC4, the refusal with SQLSTATE 42501 |

A database story uses no service contract fake; these four fixtures stand in for the ACE head and the neighbouring stories.

**12.9 Call-type summary**

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | None | None | The base of the service is `/api/recovery/source-data/v1` and is not used in this story |
| Kafka | None | None | The topic `rwb.source-data.events.v1` belongs to RWB-P1-E1015-APP |
| Temporal | None | None | No workflow, activity or Schedule |
| File | None | None | The 12 source files belong to ACE and are read by ACE's own ingestion jobs, not by this story |
| SQL | `SELECT` on the 14 tables and the 12 columns, granted to `ace_view_owner` | The 12 source files, read by ACE's own ingestion | SQL only: SELECT for the view owner, no DML for that role, and no statement of this story reads a `rwb_*` schema |

### 13. Solution plan

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 is the reason the story exists: the 14 tables are the objects behind 14 Section B views and the Workbench reads them through the views, never directly. DP-15 is the sequence rule: the ACE migration runs on the ACE schema's own sequence (GAP-2165; ASM-3469) and the one P1 version records the conformance contract. DP-19 is named for completeness: the batch status these tables feed is shown on SCR-44, a gateway-bff composite route, and this story builds no screen. The empty, loading, error and no-access states of SCR-44 are owned by RWB-P1-AD018-APP, the SCR-44 interface story, and this story does not specify them. The dependencies of DP-15 and DP-19 are recorded here as notes and not in the metadata table, which the Work Package fixes as None (ASM-3473).

**Sequencing**

| Sequence | Version and file | Contents |
|---|---|---|
| ACE schema sequence | the version allocated at build time for `V027__rwb_ace_001_recovery_source_additions.sql`; the number is Not specified in the source documents (GAP-2165; ASM-3469) | 14 `CREATE TABLE`, 12 `ALTER TABLE ... ADD COLUMN`, the primary keys, the business-key unique constraints and the foreign keys to `account`, `asset`, `customer`, `npa_asset` and `lawsuit` |
| ACE schema sequence | the grant block of the same migration, applied by the ACE DBA | `GRANT SELECT` on the 14 tables to `ace_view_owner`, `REVOKE ALL` on the same 14 from PUBLIC |
| rwb-source-data sequence | one P1 Flyway version that creates no table | The field-appendix conformance contract, recorded in `flyway_schema_history` in schema `rwb_source_data` |
| ACE schema sequence | the down script, outside Flyway | Drops the 14 tables and the 12 columns in reverse dependency order |

**Table definitions.** The 14 tables and the 12 columns are taken verbatim from section 11, with `source_system`, `business_date` and `loaded_at` and a unique business key on each table (BR1, BR2), a primary key and the unique key `(source_system, business_date)` on `ace_batch_run` (BR4), and no existing ACE column renamed, retyped or dropped (BR3).

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

**Down script.** Drops the 14 tables in reverse dependency order (`hearing` before `lawsuit`, `npa_sale` before `npa_asset`, `collateral_detail` and `valuation` after the tables they reference), then drops the 12 columns from `account`, `customer` and `efs_action`. It touches no ACE row and no view: the Section B views are dropped by the service sequence that created them (AC5).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `V027__rwb_ace_001_recovery_source_additions.sql` (legacy name; the version allocated on the ACE sequence) | Migration | The 14 tables, the 12 columns, the primary keys, the unique constraints and the foreign keys |
| 14 ingestion jobs and the `ace_batch_run` writer | ACE Spring Batch | One batch record row per source and business date, and one mapper per source writing its target table idempotently on the business key |
| `FieldAppendixConformanceTest` | Pipeline test | Compares the 80 appendix rows with `information_schema.columns` and names the field ID of any failure |
| `AceGrantCheck` | Pipeline check | `ace_view_owner` holds SELECT on the 14 tables and no DML, PUBLIC holds nothing, and the no-grant test role is refused |
| `down_ace_001.sql` | Script | Drops the 14 tables and the 12 columns in reverse dependency order |

**Build steps**

1. The migration with the 14 tables and the 12 columns, with a fixture asserting the column counts of section 11 (AC1).
2. The batch record and its unique key, with a zero-row delivery fixture and a re-sent-date fixture (AC3, AC7).
3. The 14 jobs with one full synthetic file per source, and the comparison of each target row count with the file trailer (AC2).
4. `FieldAppendixConformanceTest`, with failing fixtures for a missing column, a wrong type and an extra mapped column (AC8).
5. The grant block and `AceGrantCheck`; the down script on a copy of the SIT schema with row counts of `account`, `payment`, `customer` and `efs_action` before and after (AC4, AC5); then the ACE regression suite as the closing gate (AC6).

**Done when.** The migration applies and the down script reverses it, the 14 tables and the 12 columns hold their counts and business keys, all 80 appendix fields are populated from one full file per source, `ace_batch_run` holds one row per source and business date, `ace_view_owner` holds SELECT on the 14 tables and nothing else, the conformance test and the ACE regression suite pass, and the tests in section 16 are green.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| Conformance check 1 | A field row resolves to no column | DF-COL-013 resolves to no column collateral_detail.insurance_expiry |
| Conformance check 2 | A field row resolves to a column of the wrong type | DF-PTY-009 resolves to customer.segment of type text; varchar(20) expected |
| Conformance check 3 | A deployed mapped column has no appendix row | account.settlement_booked_amount is deployed and has no appendix row |
| Grant check | The view owner holds more than SELECT, or PUBLIC holds a privilege | ace_view_owner holds INSERT on public.valuation; the view owner reads the 14 tables only |
| SQLSTATE 42501 | A role without the grant selects a table | permission denied for schema public |
| SQLSTATE 23505 | A second row for one business key | duplicate key value violates unique constraint ace_batch_run_source_system_business_date_key |

These are pipeline and build log texts in the style of RWB-E1-069, for developers; they are not part of the message standard. No `MSG-` ID applies: this story raises no user-facing message, and the messages of the read path are raised by RWB-P1-E1069-APP and by the guard library.

### 15. Screens and states

No screen in this story. The result is visible in the ACE release pipeline and in the ACE Flyway history, and the platform administrator reads the ACE batch status per source and business date on SCR-44 Interface and job monitor under Platform administration R; the data steward reads the same batch status for freshness and changes nothing. The 14 tables are never shown directly to a user: they are read through the 14 Section B views and the service contract, never through SQL on a screen.

The SCR-44 empty, loading, error and no-access states belong to RWB-P1-AD018-APP. Their content is Not specified in the source documents (CG-ALL-1840), because Screen Specifications v1 also lacks them.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-ACE-001-01 | AC1; BR1, BR2; legacy AC1 tables and columns deployed | End to end | Clean PostgreSQL container at the ACE head, then the migration; catalogue query over the 14 tables and the 12 columns |
| TC-ACE-001-02 | AC2; legacy AC2 every field populated | End to end | One full synthetic file per source for 2026-11-30; row count per table against the trailer |
| TC-ACE-001-03 | AC3; BR4; legacy AC3 business date and completion | End to end | ALS file for 2026-11-30 completing at 04:40; a failed run for 2026-12-01; read of the batch record |
| TC-ACE-001-04 | AC4; BR5; legacy AC4 read grant only | End to end | Sessions as `ace_view_owner` and `rwb_no_grant`; privilege query over the 14 tables and the 12 columns |
| TC-ACE-001-05 | AC5; legacy AC5 reversible | End to end | Copy of the SIT schema, the migration, the down script, the row counts of `account`, `payment`, `customer` and `efs_action` |
| TC-ACE-001-06 | AC6; BR3; legacy AC6 existing ACE reads unaffected | End to end | The ACE regression suite over every existing screen, batch job and report |
| TC-ACE-001-07 | AC7; BR7; legacy AC7 idempotent reload | End to end | The 2026-11-30 file ingested twice; row counts per target table and one row in `ace_batch_run` |
| TC-ACE-001-08 | AC8; BR6; BR8; legacy AC8 field appendix matches | End to end | The 80 appendix rows against `information_schema.columns`; a missing column, a wrong type and an extra mapped column |
| TC-ACE-001-09 | BR9; GAP-0574 | Component | With v_ace_batch_status absent in SIT, the batch gate answers 409 with MSG-P1-001, no candidate and no break row; DP01 is not stamped LOADED and no case is created |
| TC-ACE-001-10 | AC9; BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8 | End to end | The ACE schema in DEV with the migration of section 11 applied; the constraint, grant and conformance checks of section 13; a repeat ingestion and a zero-row delivery; a column change without the matching appendix change |
| TC-E1-069-02 | Regression evidence: the read grant on the views is unchanged by this story | Component | Sessions as `rwb_source_data`, `ace_view_owner` and a role with no grant in SIT |

The legacy TC IDs are kept character for character and the legacy level "System" maps to "End to end". TC-ACE-001-09 is new and proves BR9, and TC-ACE-001-10 is new and proves AC9. TC-E1-069-02 stays from the RWB-E1-069 test set as evidence that the grant this story adds leaves the read path as it was. The full test of each carried-over test case, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in a migration: the field list and the 12 columns are copied from the appendix and section 11.2, and every list of values comes from the source or from reference data, never from a constant written here.
- No personal data in a migration, a script, a test fixture or a runbook: the fixtures are synthetic, `person_key` and `account_key` are business keys, and no file carries production data.
- No write path into ACE data: `ace_view_owner` holds SELECT on the 14 tables and nothing else, and PUBLIC holds nothing.
- No copy of an ACE column into a `rwb_*` schema and no foreign key from a Workbench table into `public` (DP-01, DP-05).
- No business date written by the Workbench: the business date is the source business date from the batch record (BR1; FSD P1 A2.14), and no cadence or interface number is invented for the 14 jobs (ASM-3471).
- An applied migration is never edited: a correction is a new version on the ACE sequence, the down script is the only reversal, and the 14 tables stay ACE's, so no service story creates, alters or drops one of them.

### 18. Traceability

| Requirement ID | Requirement (quoted) | Source | Rules | Test cases |
|---|---|---|---|---|
| REQ-RDF-001 | Recovery data is held in 14 data products, each with exactly one named system of record, "ACE (ingested from X)" or the Workbench, and one named owner. | FSD P1 v3, Requirements served | BR1, BR2, BR6; D-RCV-35 U2 | TC-ACE-001-01, TC-ACE-001-02, TC-ACE-001-08, TC-ACE-001-10 |
| REQ-RDF-002 | Account balance, arrears, payments and classification for every account at 90 or more days past due are read from ACE through v_ace_account and v_ace_payment, current to the previous working day. | FSD P1 v3, Requirements served | BR3, BR4, BR6; D-RCV-35 U3 | TC-ACE-001-02, TC-ACE-001-03, TC-ACE-001-07, TC-ACE-001-10, TC-E1-069-02 |
| D-RCV-35 U2 | The ACE team owns the new ACE tables and columns; the Workbench reads them and adds only its own records. | Decision Log, D-RCV-35 | BR1 to BR8 | all |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-P1-E1069-APP | App development | Consumer: the 14 Section B views and the read contract over the 14 tables; its Section B migration runs after this story is reported done |
| RWB-P1-E1069-DB | ACE DB | Sibling: the `rwb_source_data` login, the view grants and the ownership of the 30 views by `ace_view_owner`; it creates none of these 14 tables |
| RWB-P1-E1015-APP | App development | Consumer: the freshness stamp per data product, read from `v_ace_batch_status` over `ace_batch_run` |
| RWB-P1-AD018-APP | App development | Consumer: the SCR-44 interface and job monitor, which shows the ACE batch status per source and business date |

The field appendix is the contract: if a column changes, appendix A and the STTM v4 gap sheet change in the same pull request, and the conformance test fails the build on a mismatch.

### 19. Out of scope

- The 30 `recovery.v_ace_*` views, the view SQL, the three helper functions and the view conformance test: RWB-P1-E1069-APP.
- The `rwb_source_data` login, the query on the views, the view grants and the four extension tables: RWB-P1-E1069-DB.
- The freshness stamp and the events `AceDataReady` and `AceDataLate`: RWB-P1-E1015-APP.
- The file specifications, the interface numbers and the schedule of the 14 ingestion jobs: ACE's own, named by reference and not restated here (ASM-3471).
- The masking of a personal field on the read path and the authorise check: rwb-access, RWB-P4-E1069-APP.
- Any change to the field appendix or to the 12 columns without a new version of the appendix, and performance tuning beyond the primary keys and the business-key unique constraints named here.
