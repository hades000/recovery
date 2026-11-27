# RWB-P5-E1017-APP Retention and archive rule for the data store

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P5-E1017-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-document |
| Service epic | RWB-SVC-P5 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-017 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP07, DP10, DP11, DP13, DP15, DP19 |
| Parallel lane | L-P5-D |
| Ready to start | Day 1 |
| Size | To be sized by the squad at refinement (DOR-RWB-P5-E1017-APP-16) |
| Depends on (build) | None |
| Contract dependencies | RWB-P1-E1017-CON |
| Contract version | v1 (path /api/recovery/document/v1) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P5 rwb-document v1.md (no FR mapped to REQ-RDF-013) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: the P5 slice of RWB-E1-017 moved into `rwb-document` with the schema `rwb_document`, the retention tables, the JOB-17 Temporal Schedule, the write-once archive and the `RetentionRunWorkflow` of the target service; the interaction-ledger side is carried by the `rwb-source-data` contract RWB-P1-E1017-CON. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P5-E1017-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (23 resolved, 19 cross-document, 2 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **Compliance and PDPA officer (RW-COMPLY)**, I want **a retention rule per data product and table, held as reference data, applied by a Schedule-started run that archives what is past its rule, keeps what is held and logs what it did**, so that **the store holds what the policy allows and nothing older**.

Inside `rwb-document` this is the retention and archive capability of the document service, and it is the P5 slice of the legacy key RWB-E1-017:

- Service `rwb-document`, schema `rwb_document`, REST base `/api/recovery/document/v1`, topic `rwb.document.events.v1` with event names `rwb.document.<Event>.v1`, Temporal task queue `rwb-document` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.document`.
- P5 owns the retention rule and the retention action: `retention_rule` and `retention_action` in `rwb_document`, under the Ownership Map ruling of ASM-0076 (Architecture v5 slides 16, 41 and 44). This service drops no copy of a rule and reads no table of another service (DP-01). The current P5 documents are read and archived and then deleted from `document`; the document type table is read in the version in force.
- JOB-17 "Retention, monthly 1st Sunday" is a **Temporal Schedule on queue `rwb-document`** that starts `RetentionRunWorkflow` at 02:30 Asia/Bangkok (DP-10, Architecture v5 slide 44). It is not a Quartz job and it writes no shared job table.
- The run archives the P5 documents past their rule to the write-once archive container `rwb-docs-archive` with a manifest (row count and SHA-256 per file), records `retention_action` and the `DOCRET` decision record, and deletes the live document only after the archive is written and read back and checked. Every document of a case under legal hold is kept.
- The **interaction ledger and its archive rows are P1's, not P5's**. The run calls the `rwb-source-data` contract **RWB-P1-E1017-CON**, which is this story's only contract dependency, so that `rwb-source-data` applies the same rule version to its own schema. The legacy values about `interaction` rows are carried as the P1 side of the same run: they are named here and are neither read nor written by P5.
- The decision log (`decision_log_entry`, P7) is never archived and never deleted by this run. A retention load that names it is refused in full (BR5, AC4).
- The legal hold is `recovery_case.legal_hold` (DF-CAS-020) in P3 `rwb-case`. The run reads the held cases through the P3 case contract (consumed at run time; the P3 and P7 contracts are named in 12.2 and 12.8 and are not in the contract-dependency list, see GAP-1029 and ASM-1971).
- No data lake (DP-17). The archive is Blob WORM with a manifest, held in containers of the platform storage product RWB-PLT-TE012-APP, and this service holds the reference, the hash and the manifest, never a second copy in its own store.
- The database login is one per service (DP-02). Its name is Not specified in the source documents (GAP-1029; ASM-1976); this story uses the phrase "the rwb-document login (DP-02)" and never a shared login.

This story owns **no legacy acceptance criterion** and no legacy criterion text is copied into it. The legacy AC1 to AC9 of RWB-E1-017 are owned by the P1 APP slice that applies the same rule to the interaction ledger (RWB-P1-E1017-APP) and are proved end to end by RWB-ITG-E1017-ITG; the CON story of that slice is RWB-P1-E1017-CON (GAP-1029; ASM-1969). What this story owns is the P5 deliverable: the rule as data, the Schedule-started run, the document archive, the retirement of the archived document rows, the hold report and the `DOCRET` record. Its eight criteria are new, they are tagged `(new, D-RCV-60)`, and each one tests only that deliverable.

### 2. Business rationale

PDPA and the bank retention schedule limit how long personal data is kept, and recovery documents today sit in folders, shared drives and with couriers with no end date (FSD P5 A1.3). A retention rule per data product and table, loaded as versioned data, lets Compliance set and change periods without a release. A monthly run archives what is past its period to a write-once archive with a manifest and a checked read-back, removes it from the live store, keeps every document of a case under legal hold, and records what it did in `retention_action` and in the decision log. It meets REQ-RDF-013 and REQ-DCM-019, and it supports NFR-031 (a retention and archive rule by record class), NFR-072 (a legal hold stops deletion and expiry for as long as it is in place, overriding the retention class) and NFR-074 (a document reaching the end of its period is disposed of or extended by a recorded decision, never silently).

The legacy story ran one job inside P1 over the interaction ledger and a `retention_rule` copy in the recovery schema. The Ownership Map moves retention to P5 (ASM-0076; Architecture v5 slides 16, 41 and 44 JOB-17) while the ledger stays with P1 (default ruling, DP-18). The realignment changes the mechanics, not the business rule:

1. **One schema, one API base, one topic.** `rwb_document` and `/api/recovery/document/v1` (DP-01, DP-13); the `rwb_document` schema holds `retention_rule`, `retention_action`, `document` and `document_type`, and no monolith table name survives.
2. **`retention_rule` is P5's.** The rule rows move to `rwb_document` and P1 drops its copy (ASM-0076). P1 keeps the interaction ledger and applies the same rule version to its own schema; P5 never reads `interaction`, which is a P1 table.
3. **JOB-17 becomes a Temporal Schedule.** The Quartz cron `0 30 2 ? * SUN#1` and the `@DisallowConcurrentExecution` annotation become a Schedule on queue `rwb-document` with an overlap policy, started `RetentionRunWorkflow` through the workflow kit (DP-10, Architecture v5 slide 44).
4. **The archive is Blob WORM with a manifest.** Not a database copy and not a file share: the write-once container `rwb-docs-archive` of RWB-PLT-TE012-APP, one file per rule and table per run date, with row count and SHA-256 per file, and a read-back before any delete (BR2, BR4).
5. **The legal hold arrives through the P3 contract.** `recovery_case.legal_hold` is P3's, so the held cases and their case numbers are read through the `rwb-case` contract with a fake and a 2 s timeout, never from a `rwb_case` copy and never from a cross-schema join (DP-01, DP-11).
6. **The interaction-ledger archive is a contract call.** The P1 side of the same run is `POST /api/recovery/source-data/v1/admin/retention-archive` of RWB-P1-E1017-CON, one hop and 2 s timeout; P1 records its own `retention_action` and its own counts, and P5 records only that the call succeeded and how many rows P1 reported.
7. **The decision log is excluded, not copied.** P7 owns `decision_log_entry`; the run refuses a load that names it, in full, and never touches a decision entry (BR5, AC4).
8. **No data lake.** The lake copy of legacy RWB-E1-014 and its Power BI feed are removed (DP-17, ADR-018); the archive is the write-once Blob container and reporting reads events.

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-P1-E1017-CON | The `rwb-source-data` contract `POST /api/recovery/source-data/v1/admin/retention-archive`: the P1 side of the same run, with its published request and answer and its fake. This is the story's only contract dependency (C) |
| RWB-PLT-E1027-CON | The decision-record library of DP-03: the `DOCRET` record is written inside the run-record transaction and published on the shared `rwb.decision-record.v1` topic |
| RWB-PLT-E1043-CON | The reference-data client library of DP-07, so LOV-RETENTION, LOV-RETENTION-END, LOV-RETENTION-ACTION and LOV-DOC-TYPE are read in the version in force and no list value is written in code |
| RWB-PLT-E1071-CON | The workflow kit with the L3 "Scheduled job" template, activity registration, retry policy and the Schedule with its overlap policy (DP-10) |
| RWB-PLT-E1044-CON | The per-service Flyway sequence that carries the retention migration as one step in `rwb_document` (DP-15) |
| RWB-PLT-N001-CON | The gateway-bff composite route that publishes the retention reads and the run read to the administration screen (DP-19) |
| RWB-PLT-TE012-APP | The platform storage product: the write-once container `rwb-docs-archive`, the managed identity, the manifest write and the read-back |
| The P3 `rwb-case` case and legal-hold contract | The held cases and their `case_no` (DF-CAS-002 and DF-CAS-020). Consumed at run time and not in the contract-dependency list (GAP-1029; ASM-1971) |
| The P3 reference-data contract | LOV-RETENTION and the other lists, through the cached client library of DP-07 (RWB-P3-E1043-CON; not in the contract-dependency list, ASM-1971) |
| The P7 decision ledger | The central ledger that collects the `DOCRET` record from `rwb.decision-record.v1`. Consumed, not in the contract-dependency list (ASM-1971) |
| RWB-P5-E1024-APP | The `document` rows, their `retention_class` and `created_at`, the `rwb_document` baseline and the storage containers `rwb-docs`, `rwb-docs-legal` and `rwb-quarantine` |
| RWB-P5-AD021-CON | The retention-class contract this story serves and reuses: `RetentionClass`, `DocumentRetention` and `RetentionActionPage` (12.1) |

Business preconditions carried from RWB-E1-017:

- Retention rule version "RET-2026.11" is loaded and approved: 24 months for the documents of product DP10, end action ARCHIVE (assumed until Compliance supplies the bank schedule; DL26 — GAP-1029; ASM-1972). The legacy version carries the same label, the same 24 months and the same product/table structure; only the table the rule names is the target one.
- A write-once archive container exists in each environment, writable by the rwb-document service identity (the legacy SY-DATALOAD data-load role). Its name `rwb-docs-archive` is assumed (GAP-1029; ASM-1974).
- The P3 case contract answers the held cases and their case numbers; P3 owns `legal_hold` and the hold is placed and cleared by `rwb-case`, never by this service.
- The reference-data contract answers LOV-RETENTION, LOV-RETENTION-END, LOV-RETENTION-ACTION and LOV-DOC-TYPE with their versions in force (DP-07).
- The login is the rwb-document login (DP-02). Its name is Not specified in the source documents (GAP-1029; ASM-1976).
- The release date 30 November 2026 is tentative and is copied unchanged.

The retention periods and the age-basis field of a document are Not specified in the source documents (GAP-1029; ASM-1972). The retention load and run-read paths are Not specified in the source documents (GAP-1029; ASM-1973). The decision code `DOCRET` and the LOV-RETENTION-ACTION values are carried from the sources as stated in ASM-1975.

### 4. Flow

1. Reference data administrator (RW-REFADM): calls `POST /api/recovery/document/v1/admin/retention-loads` with the rule version, its valid-from date and the rows, and an `Idempotency-Key`. `RetentionRuleLoader` validates the load **in full** before a row is stored: product code in force, table in the P5 owned list, `retention_months` between 1 and 600, table not `decision_log_entry`, age-basis field a field of that table, rule version and valid-from present (BR6, AC1).
2. Holder of Reference data A: approves the version with `POST /api/recovery/document/v1/admin/retention-loads/{loadId}/approve`. An exception anywhere in the load leaves the previous version in force with no partial store; an approved version applies from its valid-from date (BR7; R-UNI-38).
3. JOB-17 Retention Schedule on queue `rwb-document`: fires on the first Sunday of the month at 02:30 Asia/Bangkok and starts `RetentionRunWorkflow` with the run date (DP-10, 12.5 and 12.6).
4. `RetentionService`: reads the rules in force on the run date from `retention_rule` in `rwb_document` (BR1).
5. `CaseHoldClient`: reads the cases under legal hold through the P3 case contract (12.2) and builds the held-case set with the case number of each, so every document of such a case is excluded from the selection (BR3, AC3). It calls the published CaseHoldQuery interface of rwb-case, casesOnLegalHold and caseNumbers, one hop with a 2 s budget, through its contract fake on Day 1; no case table is read by SQL, and the transport detail is settled with rwb-case in RWB-P1-E1017-CON.
6. `RetentionService`: selects, per rule, the `document` rows whose age-basis field is older than the run date minus the retention months, excluding every document of a held case and counting the remainder per product and table (BR2).
7. `archiveDocuments` activity: `ArchiveWriter` writes the selected documents per rule and table to the write-once container `rwb-docs-archive` under `retention/YYYY-MM-DD/<table>/`, writes the manifest (row count and SHA-256 per file) and reads it back (BR2, BR4). The write runs under the rwb-document service identity; the container's account, credential scope, immutability policy and manifest schema are owned by RWB-PLT-TE012-APP.
8. `deleteArchived` activity: only after the manifest matches, deletes the archived rows from `document` in one transaction per rule and table, under the purge setting `rwb.document.retention_purge` (BR4, AC2). A failure before the delete leaves the live rows; a failure after the delete leaves a complete archive.
9. `callP1Archive` activity: calls the `rwb-source-data` contract RWB-P1-E1017-CON `POST /api/recovery/source-data/v1/admin/retention-archive` with the same rule version and run date, so P1 applies the rule to its own `interaction` rows and answers its own counts (12.2). P5 stores the call result and P1's reported counts; it reads no `interaction` row.
10. `writeRunRecord` activity: records on the run the counts per product and table, the rule version, the archive location and the hold report (case numbers and counts kept), and writes the `DOCRET` decision record through the decision-record library of DP-03 in the run-record transaction (BR5, BR8). The record keeps ruleId empty, carries the run reference in inputsRef, and carries the product, table, counts, hold report reference and archive location in actions and outcome; the decision code and final call values: Not specified in the source documents (GAP-2426).
11. RW-COMPLY: reads the run result through `GET /api/recovery/document/v1/admin/retention-runs` and the summary alert MSG-P1-020 (12.1, section 14). A failed run is rerun from the same read with `POST /admin/retention-runs/{runId}/rerun`, refused with 409 while a run is active (AC7).

The run is the owner's: one service selects, archives, deletes and records the P5 side, and calls the P1 side once. Nothing is deleted before the archive copy is checked, no case status changes, and no row of another service's schema is read at any step (DP-01, BR9, BR10).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A case is on legal hold | Every document of the case is kept and listed in the hold report with its count; the summary alert names the number of cases kept | MSG-P1-020 | AC3 |
| X2 | A rule row has `retention_months` outside 1 to 600 | The load is refused in full; the previous version stays in force | MSG-GEN-002 | AC1 |
| X3 | The archive write or the manifest read-back fails | No document is deleted; the run ends FAILED; the alert is raised; the rerun is taken from the run read | MSG-GEN-006 | AC5 |
| X4 | JOB-17 runs again for the same month | The rows already archived are gone; the rerun archives only the documents still past their rule; the archive keeps one copy of the set | None | AC6 |
| X5 | A document is exactly at its retention age | The document is kept; the boundary is the run date minus the retention months, and an age equal to that instant is not older than it | None | AC9 |
| X6 | A rule names the table `decision_log_entry` | The load is refused in full; the decision log is never archived or deleted by this run | MSG-P1-002 | AC4 |
| X7 | A rerun is posted while the run is active | Status 409; the active run continues unchanged and no second run starts | MSG-P2-006 | AC7 |
| X8 | The P3 case contract does not answer within 2 s, or its breaker is open | The run ends FAILED before any archive and before any delete; the alert is raised and the rerun repeats the whole run | MSG-GEN-006 | AC3 |
| X9 | The caller's role lacks the Platform administration `U` right | Status 403; no run starts | MSG-P4-002 | AC8 |

Target-service notes:

- The legacy X6 wording "table decision_log_entry" is kept as the check name that MSG-P1-002 carries; the table is P7's, is listed as forbidden in the load, and is never opened by this service (BR5, BR9).
- X8 is new to this slice and replaces the legacy in-process call `CaseHoldQuery`; the run fails whole rather than archive a partial selection, because a held case that was not seen would lose its documents (BR3, BR4).
- The `callP1Archive` activity (step 9) is retried under the run policy; a final failure of that call ends the run FAILED after the P5 side is recorded, and the P1 rows are left untouched for the rerun. The legacy values of that side are P1's and are recorded on the run as P1 reported them.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the `rwb_document` baseline and the `document` rows (RWB-P5-E1024-APP), the write-once container (RWB-PLT-TE012-APP) and the published `rwb-source-data` contract (RWB-P1-E1017-CON); the P3 and P7 reads sit behind fakes |
| Negotiable | Periods, tables, age-basis fields, the end action and the archive location are rule rows, properties or list values; the story fixes the archive, purge, hold and record behaviour |
| Valuable | The service keeps no document longer than its rule, every removal is recorded, and a held case keeps everything it holds |
| Estimable | Two owned tables, one migration, one Schedule-started workflow with four activities, one archive writer, one P1 client, one hold client |
| Small | Fits inside two weeks with its tests, as the P5 slice of a legacy key already split across P1, P5, P7 and the wave 1 integration story |
| Testable | Each criterion in section 7 runs on synthetic rows with a fixed run date and a stubbed container; no ACE data and no production data is needed |

### 7. Acceptance criteria

```gherkin
Feature: Retention and archive rule for the data store, P5 side

  Background:
    Given retention rule version "RET-2026.11" holds product "DP10", table "document", age basis "created_at", 24 months, end action "ARCHIVE"
    Given the run date is Sunday 2026-12-06
    Given the P3 case contract mock answers the held cases and their case numbers
    Given the archive container "rwb-docs-archive" accepts writes unless the scenario says otherwise

  Scenario: AC1 A rule load is validated in full (new, D-RCV-60)
    Given a retention load version "RET-2026.12" with a row for DP10 document at 0 months
    And the same load carries a row for product "DP12", table "decision_log_entry"
    When the load is validated
    Then the system refuses the load in full with MSG-GEN-002 for field "retention_months" between 1 and 600
    And the system refuses the load in full with MSG-P1-002 and check "decision_log_entry is not archived by the retention run"
    And no row of "RET-2026.12" is stored and version "RET-2026.11" stays in force

  Scenario: AC2 The run archives and records the documents past their rule (new, D-RCV-60)
    Given 1,250 synthetic document rows with created_at before 2024-12-06 and 4,800 rows from 2024-12-06 onward
    When JOB-17 runs
    Then 1,250 document rows are written to the archive container under "retention/2026-12-06/document/" with a manifest of the row count and the SHA-256 per file
    And the manifest is read back and matches before any delete
    Then the 1,250 rows are no longer in the live document table
    Then the run logs count 1,250 for DP10 document under rule version "RET-2026.11"
    And each archived document has a "retention_action" row with action "ARCHIVED" for run_month "2026-12"
    And one "DOCRET" decision record names the run, the rule version "RET-2026.11", the table "document" and the count 1,250

  Scenario: AC3 Legal hold keeps every document of the case (new, D-RCV-60)
    Given case "RW-2024-000311" is marked legal hold and has 40 documents older than 24 months
    When JOB-17 runs
    Then the system keeps its 40 documents in the live table
    Then the hold report lists case "RW-2024-000311" with 40 documents kept
    Then the summary alert to Compliance reads MSG-P1-020 with 1 case on legal hold kept
    And each kept document has a "retention_action" row with action "HELD" for run_month "2026-12"

  Scenario: AC4 The decision log is never archived (new, D-RCV-60)
    Given a retention load version "RET-2026.12" with a row for product "DP12", table "decision_log_entry"
    When the load is validated
    Then the system refuses the load in full with MSG-P1-002 and check "decision_log_entry is not archived by the retention job"
    And the P7 decision log is unchanged, because this service reads no "decision_log_entry" row and deletes none

  Scenario: AC5 The archive write fails (new, D-RCV-60)
    Given the archive container refuses writes
    When JOB-17 runs
    Then the system deletes no document
    Then the run ends "FAILED" with MSG-GEN-006 for system "Archive container"
    And no "retention_action" row with action "ARCHIVED" is written for the run

  Scenario: AC6 A repeat run in the same month (new, D-RCV-60)
    Given JOB-17 archived 1,250 documents on 2026-12-06
    When JOB-17 is rerun on 2026-12-06
    Then the system archives 0 documents
    Then the archive container still holds one set of the 1,250 documents

  Scenario: AC7 A rerun while the run is running (new, D-RCV-60)
    Given JOB-17 is running
    When a platform administrator posts a rerun of JOB-17
    Then the system refuses the rerun with status 409 and MSG-P2-006
    And one run continues and no second run starts

  Scenario: AC8 A role without the right is refused (new, D-RCV-60)
    Given a role without Platform administration "U"
    When the caller posts a rerun of JOB-17
    Then the system refuses the call with status 403 and MSG-P4-002
    And no run starts

  Scenario: AC9 A document exactly at its retention age is kept (new, D-RCV-60)
    Given a document with captured_at 2024-12-06T00:00+07:00 is in the live table
    When JOB-17 runs on the run date 2026-12-06
    Then the system keeps the document in the live table
    And the run neither archives nor deletes the document

  Scenario: AC10 The rule and the archive location are data (new, D-RCV-60)
    Given retention rule version "RET-2026.11" names the archive container "rwb-docs-archive"
    When the rule row names another archive container
    Then the run writes the archive to the container named by the rule row
    And no code change is needed

  Scenario: AC11 The run reads and writes only rwb_document (new, D-RCV-60)
    Given the run for product "DP10" and table "document"
    When JOB-17 runs
    Then the run reads and writes no table outside rwb_document
    And the interaction ledger, the legal hold and the decision log are reached only through their owners' contracts

  Scenario: AC12 JOB-17 is a Schedule of this service (new, D-RCV-60)
    Given JOB-17 is a Schedule of rwb-document
    When JOB-17 runs
    Then the run calls the P1 archive contract once for P1's own rows
    And no other service starts JOB-17

  Scenario Outline: AC13 A call that is not authenticated or names a job that does not exist is answered (new, D-RCV-60)
    Given <condition>
    When the caller <call>
    Then the system answers status <status> and no run starts

    Examples:
      | condition | call | status |
      | the caller presents no valid credential | posts a rerun of JOB-17 | 401 |
      | the job id named in the call does not exist | posts a rerun of that job id | 404 |

  Scenario: AC14 A contract call that does not answer within 2 s fails the run (new, D-RCV-60)
    Given the P3 case contract mock does not answer within 2 s
    When JOB-17 runs
    Then the run ends "FAILED" and no document is archived or deleted
    And the retry count of the activity is Not specified in the source documents (NEWAC-RWB-P5-E1017-APP-AC13)

  Scenario: AC15 A consumed call that fails ends the run (new, D-RCV-60)
    Given the P1 archive contract fails
    When JOB-17 runs
    Then the run ends "FAILED" with MSG-GEN-006 for system "P1 archive contract"
    And no document is deleted before the archive copy is checked
```

The fifteen criteria are new and test only the P5 deliverable: the rule as data, the Schedule-started run, the document archive and the recorded action. They reuse the legacy values that belong to the same run: the rule version "RET-2026.11", 24 months, the run date Sunday 2026-12-06, 1,250 old and 4,800 recent rows, case "RW-2024-000311" with 40 old rows, the archive path `retention/2026-12-06/document/`, the six message IDs and the decision code `DOCRET`.

The legacy `interaction` rows and their archive are **P1's side of the same run**, reached through RWB-P1-E1017-CON: P5 owns the `document` side and the rule, and P1 owns the ledger rows, its own `retention_action` and its own counts (GAP-1029; ASM-1970). No legacy criterion text is copied into this story, and the legacy AC1 to AC9 stay with RWB-P1-E1017-APP and RWB-ITG-E1017-ITG.

P5 owns the rule and the document archive; each owner applies the rule to its own schema; the suite asserts the rule version, the legal holds and the decision-log exclusion through the owners' APIs and Temporal visibility. The cross-service trigger and API for the P1 interaction rows: Not specified in the source documents (GAP-0342).

The age basis field `created_at` and the 24 months for documents are Not specified in the source documents (GAP-1029; ASM-1972); the legacy story set `occurred_at` for the interaction ledger and 24 months for DP05.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Each data product and table has one retention rule in force, held as a versioned data row in `retention_rule` | Retention classes reference table; DL26; RWB-E1-017 BR1; ASM-0076 |
| BR2 | A document older than its retention period on its age-basis field is archived and removed from the live store | `retention_rule.retention_months`; REQ-RDF-013; REQ-DCM-019 |
| BR3 | A legal hold keeps every document of the case, overriding the retention rule | R-UNI-20; `recovery_case.legal_hold`; NFR-072 |
| BR4 | A document is removed only after its archive copy is written and checked | Archive container; NFR-074; RWB-E1-017 BR4 |
| BR5 | The decision log is not archived by this run and never deleted; its retention is set by Compliance and it is P7's | NFR-030; DL26; RWB-E1-017 BR5 |
| BR6 | A retention load with an exception is refused in full | Reference data change process; CTL-08; RWB-E1-017 BR6 |
| BR7 | A new version applies from its valid-from date; earlier runs keep their recorded version | R-UNI-38; RWB-E1-017 BR7 |
| BR8 | The rule and the archive location are data, not code: a period, a table, an age-basis field, an end action and the container are rows or properties | Principle 1; BR-P5-017 of FSD P5 A2.17.3.1 |
| BR9 | The run reads and writes only `rwb_document`; no other service's table is read, and the interaction ledger, the legal hold and the decision log are reached through their owners' contracts or not at all | DP-01; DP-11; ASM-0076 |
| BR10 | The run is the owner's: this service selects, archives, deletes and records its own rows, and calls P1 once for P1's own rows | Architecture v5 slide 44 (JOB-17 owned by rwb-document); RWB-E1-017 section 12 |

Open decision DL26 applies to BR1 and BR5 and is still open; its assumptions: Not specified in the source documents (DOR-RWB-P5-E1017-APP-18).

Target-service statements that make the rules hold in `rwb-document`:

- BR1 is executed by the unique key on (`product_code`, `table_name`, `record_class`, `rule_version`) and by the in-force selection on `valid_from` and `valid_to`; the rule rows are `rwb_document` rows, and P1 holds no copy (ASM-0076).
- BR2 is executed by the selection on the age-basis column named by the rule, by the manifest write of `ArchiveWriter`, and by the delete under the purge setting `rwb.document.retention_purge`, which is set inside `deleteArchived`'s own transaction.
- BR3 is executed by the held-case set of `CaseHoldClient` applied before the selection; a case the P3 contract does not answer fails the run instead of being archived.
- BR4 is executed by the order of the four activities: `archiveDocuments` writes and reads back the manifest, `deleteArchived` runs only after it returns a match, and a mismatch raises MSG-GEN-006 and ends the run FAILED.
- BR5 is executed by the forbidden-table check on the retention load and by the absence of any read or delete on a P7 table.
- BR6 is executed by `RetentionRuleLoader` validating every row before the first store, so a refused load leaves the version in force and stores no row.
- BR7 is executed by the valid-from date on the row and by the version recorded on the run; a run is never re-valued in hindsight.
- BR8 keeps the container name, the batch size, the rule version and the purge setting as properties or rows; no period appears in Java.
- BR9 is executed by the schema boundary test on the module and by the contract calls of 12.2 with a 2 s timeout and a breaker per downstream (DP-11).
- BR10 is executed by JOB-17 being a Schedule of this service (12.6) and by the `callP1Archive` activity being the only cross-service write of the run.

### 9. State transitions

None. This story does not change a case status. It changes the JOB-17 run status and the retention rule version in force:

| From | Event | To |
|---|---|---|
| (none) | the JOB-17 Schedule fires on the first Sunday at 02:30 Asia/Bangkok | run Running |
| Running | the archive is written and the manifest read back matches; the live rows are deleted; the P1 call returns; the run record and the `DOCRET` record are written | run Complete |
| Running | the archive write, the manifest check, the P3 hold read or the P1 call fails | run Failed; no document is deleted, the alert is raised, the rerun repeats the run |
| Running | a rerun is posted | refused with 409 (MSG-P2-006); the run continues unchanged |
| A rule version in force | an approved version reaches its valid-from date | the new version is in force from that date; earlier runs keep the version they recorded |
| A rule version in force | a load is refused in full | the version in force is unchanged |

The rule version lifecycle (LOADED, APPROVED, IN_FORCE, SUPERSEDED, REFUSED) is the load path's; this story reads the version in force and writes its own rows.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-COMPLY, Compliance and PDPA officer | Owns the retention periods; reads the run result and the hold report (Platform administration R) |
| RW-REFADM, reference data administrator | Submits the retention load (Reference data C) |
| Holder of Reference data A | Approves the retention load |
| RW-DATASTEW, data steward | Reads the run result for their products through the same run read |
| RW-PLATADM, platform administrator | Reruns the failed run (Platform administration U) and reads the run read |
| The rwb-document service identity (the legacy SY-DATALOAD data-load role) | Runs JOB-17, writes the archive, deletes the archived rows, writes `retention_action` and the `DOCRET` record |
| P3 `rwb-case` | Owns `legal_hold` and the case number; answers the hold read; places and clears the hold itself |
| P1 `rwb-source-data` | Owns the interaction ledger; applies the same rule version to its own schema through RWB-P1-E1017-CON |
| P7 `rwb-decision` | Owns `decision_log_entry`; collects the `DOCRET` record from the shared decision-record topic |
| Nobody | Archives or deletes a `decision_log_entry` row from this story |

The refusal shape is 403 with an RFC 9457 problem response and `messageId` MSG-P4-002 (AC8). The database login is the rwb-document login (DP-02) and this story names no credential (GAP-1029; ASM-1976).

The rwb-access authorise check that guards each REST operation of this story: Not specified in the source documents (DOR-RWB-P5-E1017-APP-6).

### 11. Data

| BR Field ID | Table in `rwb_document` | Field | Read or write |
|---|---|---|---|
| DF-REF-116 | `retention_rule` | id | Write |
| DF-REF-117 | `retention_rule` | product_code | Write |
| DF-REF-118 | `retention_rule` | table_name | Write |
| DF-REF-119 | `retention_rule` | record_class | Write |
| DF-REF-120 | `retention_rule` | retention_months | Write |
| DF-REF-121 | `retention_rule` | age_basis_field | Write |
| DF-REF-122 | `retention_rule` | end_action | Write |
| DF-REF-123 | `retention_rule` | rule_version | Write |
| DF-REF-124 | `retention_rule` | valid_from | Write |
| DF-REF-125 | `retention_rule` | valid_to | Write |
| DF-REF-126 | `retention_rule` | approved_by | Write |
| DF-DOC-091 | `retention_action` | id | Write |
| DF-DOC-092 | `retention_action` | document_id | Write |
| DF-DOC-093 | `retention_action` | run_month | Write |
| DF-DOC-094 | `retention_action` | action | Write |
| DF-DOC-095 | `retention_action` | decision_log_id | Write |
| DF-DOC-001 to DF-DOC-011 | `document` | id, case_id, party_id, document_type, source, storage_ref, classification_confidence, review_status, retention_class, write_once, doc_version | Read; the archived rows are deleted after the manifest check |
| DF-DOC-025 | `document` | previous_version_id | Read |
| DF-DOC-026 | `document` | content_sha256 | Read; copied into the manifest per file |
| Standard columns | `document` | `state`, `captured_at`, `version` | Read; `captured_at` is the age-basis field of the assumed rule (ASM-1972) |
| DF-REF-219 | `document_type` | doc_type_code | Read |
| DF-REF-223 | `document_type` | retention_class | Read |
| DF-REF-229 | `document_type` | table_version | Read |
| DF-CAS-002 | `rwb-case` case, through the P3 contract | case_no | Read, as the hold report's identifier |
| DF-CAS-020 | `rwb-case` case, through the P3 contract | legal_hold | Read |
| DF-INT-001 to DF-INT-013 | `interaction` (P1 `rwb-source-data`) | the ledger row, its case and its age basis | Not read and not written by P5: P1 applies the rule to its own rows through RWB-P1-E1017-CON |

The `document` row is deleted in the sense that archived rows leave the live table (legacy section 11); the archive copy stays in the write-once container and the `retention_action` row stays in `rwb_document`. Field IDs are those in the Logical Data Model and Data Dictionary and the TSD P5 T3.1 table. No `rwb_case` row is copied and no `interaction` row is read: DF-CAS-002 and DF-CAS-020 arrive inside the P3 contract answer, and the ledger rows are P1's. Personal data never enters the run record, the hold report, the archive manifest, the decision record or the log: counts and case numbers only.

### 12. Contract

#### 12.1 REST operations provided

All paths sit on base `/api/recovery/document/v1` (DP-13); the retention-class reads and the three read operations are the shared retention contract shape that RWB-P5-AD021-CON defines and that RWB-P5-E1016-APP reuses.

| Operation | Path | Owner | Notes |
|---|---|---|---|
| GET | `/api/recovery/document/v1/retention-classes` | P5 | Query `productCode`, `docTypeCode`, `page`, `size`; answers `RetentionClassPage`. Read with the Documents right R inside scope |
| GET | `/api/recovery/document/v1/retention-classes/{classCode}` | P5 | Answers `RetentionClass`: classCode, labelEn, labelTh, productCode, docTypeCode, retentionMonths, ageBasisField, endAction, ruleVersion, validFrom, validTo |
| GET | `/api/recovery/document/v1/documents/{documentId}/retention` | P5 | Answers `DocumentRetention`: documentId, retentionClass, expiryDate, state, legalHold, legalHoldRef, lastAction |
| GET | `/api/recovery/document/v1/documents/{documentId}/retention-actions` | P5 | Answers `RetentionActionPage`: documentId, runMonth, action, decisionLogId, recordedAt |
| POST | `/api/recovery/document/v1/admin/retention-loads` | P5 | The `RetentionLoad` (ruleVersion, validFrom, rows[]) validated in full; `Idempotency-Key` required; Reference data C |
| POST | `/api/recovery/document/v1/admin/retention-loads/{loadId}/approve` | P5 | Approves the version; Reference data A; 404 unknown load, 409 a load already decided |
| GET | `/api/recovery/document/v1/admin/retention-runs` | P5 | `RetentionRunPage`: runId, runDate, ruleVersion, state, counts per product and table, archive location, hold report, P1 answer; Platform administration R |
| POST | `/api/recovery/document/v1/admin/retention-runs/{runId}/rerun` | P5 | Reruns a failed or completed run; `Idempotency-Key` required; 409 with MSG-P2-006 while a run is active; Platform administration U |

The request and answer field names of the eight operations, the paging shape and the run-read element names are Not specified in the source documents (GAP-1029; ASM-1973); the story fixes them as stated here. The example values are the legacy ones: rule version `RET-2026.11`, classes `LEGAL10Y` and `GENERAL05Y`, product `DP10`. Errors are RFC 9457 problem responses with `messageId` (section 14).

#### 12.2 REST operations consumed

| Operation | Path | Owner | Story | Note |
|---|---|---|---|---|
| POST | `/api/recovery/source-data/v1/admin/retention-archive` | P1 | RWB-P1-E1017-CON | The P1 side of the same run: the same rule version and run date, so P1 applies the rule to its own `interaction` rows and answers its own counts. One hop, 2 s timeout, breaker per downstream (DP-11). The path is fixed in that contract |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 | the case contract | The hold flag and the case number of a held case; one hop, 2 s timeout |
| POST | `/api/recovery/case/v1/cases/{caseId}/legal-hold` | P3 | the case contract | The hold is placed and cleared by `rwb-case`, never here; this story reads the effect and writes no hold |
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 | RWB-P3-E1043-CON | LOV-RETENTION and LOV-RETENTION-END, through the cached reference-data client library of DP-07; no list value in code |
| (decision-record library) | `rwb.decision-record.v1` | P7 | RWB-P7-E1027-CON | The `DOCRET` record is written through the library of DP-03 and collected by `rwb-decision`; no REST call is made by this story |

The P3 and P7 contracts are consumed at run time and are **not** in this story's contract-dependency list, whose only row is RWB-P1-E1017-CON (GAP-1029; ASM-1971). They are named here, in section 3 and in 12.8 so that no reader assumes a local read of `rwb_case`, `lov_value` or `decision_log_entry`.

#### 12.3 Events published

None. This slice adds no event to the two events the architecture gives `rwb-document` (`DocumentStored` and `DocumentFieldsExtracted`, Architecture v5 slides 16 and 41); the archive run publishes no event of its own and holds no outbox row for one.

The `DOCRET` decision record is written through the local decision-record library of DP-03 inside the run-record transaction and is published on the shared `rwb.decision-record.v1` topic by that library, not by this story. It is a decision record, not an event of `rwb.document.events.v1`.

#### 12.4 Events consumed

None. The run is started by the JOB-17 Schedule and the reference lists are read through the client library; no Kafka topic is consumed by this slice.

#### 12.5 Workflows and activities

| Name | Kind | Queue | Note |
|---|---|---|---|
| `RetentionRunWorkflow` | Workflow, from the L3 workflow kit template "Scheduled job", Schedule-started | `rwb-document` | The run of JOB-17: reads the rules, reads the holds, selects, archives, deletes, calls P1 and writes the run record |
| `archiveDocuments` | Activity | `rwb-document` | Writes the selected documents per rule and table to `rwb-docs-archive` with the manifest and reads it back |
| `callP1Archive` | Activity | `rwb-document` | Calls RWB-P1-E1017-CON for the P1 side of the same run and records P1's answer |
| `deleteArchived` | Activity | `rwb-document` | Deletes the archived rows in one transaction per rule and table, after the manifest check, under `rwb.document.retention_purge` |
| `writeRunRecord` | Activity | `rwb-document` | Writes the run record, the counts, the hold report, `retention_action` and the `DOCRET` record |

#### 12.6 Schedules

| Job | Name | When | Owner | Mechanism |
|---|---|---|---|---|
| JOB-17 | Retention | Monthly, first Sunday, 02:30 Asia/Bangkok | rwb-document | Temporal Schedule on queue `rwb-document`, overlap policy so one run at a time, with a catch-up window (DP-10; Architecture v5 slide 44) |

The legacy cron `0 30 2 ? * SUN#1` and the `@DisallowConcurrentExecution` annotation are replaced by the Schedule and its overlap policy; no shared Quartz table and no job row of another service is written (Architecture v5 slide 44).

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `retention_rule` | P5 (`rwb_document`) | Write: the version, its rows, the valid-from and valid-to dates and the approver; read: the rules in force on the run date |
| `retention_action` | P5 (`rwb_document`) | Write: one row per document per run month with the action (ARCHIVED, LISTED, HELD, EXCEPTION) and the decision-log reference |
| `document` | P5 (`rwb_document`) | Read and delete: the archived rows leave the live table after the manifest check |
| `document_type` | P5 (`rwb_document`) | Read only: the type row in force, for the retention class and the type code |
| decision-record library table | PLT library, created in `rwb_document` | The `DOCRET` record, in the run-record transaction |

No table, no view and no foreign key of another schema is used (DP-01). P1 holds no `retention_rule` table and no retention Schedule; the run request to P1 carries the rule version, the run date and the rules, and P1 validates them against its own tables (GAP-0488). `interaction` is P1's, `recovery_case` and `lov_value` are P3's and `decision_log_entry` is P7's; none of them is read, written or defined here.

#### 12.8 Contract fakes

| Fake | Story | Used for |
|---|---|---|
| rwb-source-data retention-archive fake | RWB-P1-E1017-CON | The P1 side of the run: a successful answer with counts, a timeout and a server error, each with its published shape |
| rwb-case case and legal-hold fake | the P3 case contract | The held cases and their case numbers, the empty hold set, and the 2 s timeout path of X8 |
| rwb-case reference-data fake | RWB-P3-E1043-CON (through RWB-PLT-E1043-CON) | LOV-RETENTION, LOV-RETENTION-END, LOV-RETENTION-ACTION and LOV-DOC-TYPE with their versions in force |
| P7 decision-record fake | RWB-P7-E1027-CON | The local `DOCRET` record, its publish on `rwb.decision-record.v1` and the collection by the central ledger |
| archive-container stub | RWB-PLT-TE012-APP | The manifest write and read-back, the SHA-256 comparison and the write refusal of AC5 |
| Drools kit | not used | No rule package is evaluated in this story: the retention rule is a data row, not a Drools rule |

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 8, consumed 4 | The two retention-class reads, the two document retention reads, the four admin operations; the P1 archive call, the two P3 case reads and the P3 list read |
| Kafka | Published 0 events; consumed 0 | The `DOCRET` record goes on `rwb.decision-record.v1` through the library of DP-03 |
| Temporal | 1 workflow, 4 activities, 1 Schedule | `RetentionRunWorkflow` on queue `rwb-document` with `archiveDocuments`, `callP1Archive`, `deleteArchived` and `writeRunRecord`, started by the JOB-17 Schedule |
| File | Blob WORM | The archive files and the manifest in `rwb-docs-archive` under `retention/YYYY-MM-DD/<table>/`, through RWB-PLT-TE012-APP |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.document`, module `document/retention`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| RetentionRunWorkflow | Temporal workflow | The Schedule-started run: rules in force, held cases, selection, archive, delete, P1 call, run record; fails whole on any failed step |
| RetentionService | Service | Reads the rules in force, selects the `document` rows past their rule, excludes the held cases, orders the four activities and decides the run state |
| RetentionRuleLoader | Service | Validates a retention load in full and stores an approved version; the forbidden-table and the 1-to-600 checks |
| ArchiveWriter | Service | Writes one file per rule and table with the manifest (row count and SHA-256 per file) to `rwb-docs-archive` and reads it back |
| P1ArchiveClient | Client | The `rwb-source-data` contract RWB-P1-E1017-CON: one hop, 2 s timeout, breaker, retry under the run policy |
| CaseHoldClient | Client | The `rwb-case` case and legal-hold contract: the held cases and their case numbers, one hop, 2 s timeout |
| RetentionRunRepository | Repository | The run record and the reads behind `GET /admin/retention-runs` |
| RetentionRuleRepository | Repository | Reads and writes `retention_rule` in `rwb_document`; the version in force by `valid_from` and `valid_to` |
| RetentionActionRepository | Repository | Writes and reads `retention_action` in `rwb_document` |
| RetentionController | Controller | The eight operations of 12.1, the access check and scope, and the RFC 9457 error mapping with `messageId` |

**Database.**

- Writes `retention_rule` with the TSD P5 T3.1 fields (DF-REF-116 to DF-REF-126 plus the standard columns) and `retention_action` with DF-DOC-091 to DF-DOC-095 plus the standard columns; reads `document` and `document_type`.
- One migration in the per-service Flyway sequence (DP-15): `V1017_1__document_retention.sql` creates `retention_rule` (id uuid, product_code varchar(25), table_name varchar(60), record_class varchar(20), retention_months integer check between 1 and 600, age_basis_field varchar(60), end_action varchar(12), rule_version varchar(20), valid_from date, valid_to date, approved_by uuid, standard columns) and `retention_action` (id uuid, document_id uuid, run_month char(7), action varchar(12), decision_log_id uuid null, standard columns).
- Keys and indexes: unique (`product_code`, `table_name`, `record_class`, `rule_version`) on `retention_rule`; `ix_document_retention_created ON document (retention_class, captured_at)` for the selection; `ix_retention_action_document ON retention_action (document_id, run_month)`; `ix_retention_action_decision ON retention_action (decision_log_id)`.
- A purge setting `rwb.document.retention_purge` guards the delete, in the same shape the legacy append-only trigger used: the delete is allowed only inside the `deleteArchived` transaction where the setting is on, and an update stays refused. No unconditional refusal remains on `document`, because a document is archivable; `decision_log_entry` is not in this schema and is never touched.

**Configuration and reference data.**

- Rule version `RET-2026.11` with 24 months for DP10 `document`, age basis `created_at`, end action `ARCHIVE`, prepared by Compliance and loaded by RW-REFADM and approved by the holder of Reference data A. The period and the age basis are assumed until the bank schedule arrives (DL26; GAP-1029; ASM-1972).
- Properties: `rwb.document.retention.archive-container=rwb-docs-archive` (name assumed; GAP-1029; ASM-1974), `rwb.document.retention.batch-size=5000`, `rwb.document.retention.run-time=02:30`, `rwb.document.retention.timezone=Asia/Bangkok`.
- Decision code `DOCRET` and the list LOV-RETENTION-ACTION (`ARCHIVED, LISTED, HELD, EXCEPTION`) are data values loaded by the data steward (TSD P5 T3.2; GAP-1029; ASM-1975).
- Feature flag `rwb.document.retention`. Off: the Schedule is paused, the four admin operations answer 404 and the four reads answer as of the last recorded run (GAP-1029; ASM-1977).

**Build steps**

1. Write the migration for `retention_rule` and `retention_action`, the keys and the three indexes; test the unique rule key and the months check at 0, 1, 600 and 601.
2. Build `RetentionRuleLoader` with whole-load validation (product in force, table in the P5 owned list, not `decision_log_entry`, months 1 to 600, age-basis field a field of the table); unit test AC1 and a refused load that leaves RET-2026.11 in force.
3. Build `RetentionRuleRepository` and the in-force selection on `valid_from` and `valid_to`; test the boundary date of RET-2027.01 of TC-E1-017-02.
4. Build `CaseHoldClient` against the P3 fake, including the 2 s timeout and the empty hold set; test the held-case exclusion of AC3.
5. Build the selection and the batching on `document (retention_class, created_at)` with the exactly-at-age boundary of TC-E1-017-07.
6. Build `ArchiveWriter` with the manifest write, the SHA-256 per file and the read-back; test the write refusal of AC5 against the container stub.
7. Build `deleteArchived` under `rwb.document.retention_purge`, one transaction per rule and table, and record `retention_action`; test that a manifest mismatch deletes nothing.
8. Build `P1ArchiveClient` and the `callP1Archive` step against the RWB-P1-E1017-CON fake; test the success, the timeout and the retry.
9. Register `RetentionRunWorkflow` on queue `rwb-document` and the JOB-17 Schedule with the overlap policy; test AC6 and AC7 with the test clock.
10. Build the eight operations of 12.1 with the access check and scope; API tests for AC1, AC2, AC3, AC8 and the run read.
11. Write the `DOCRET` record through the decision-record library in the run-record transaction; test that a record failure leaves the run Failed and no `ARCHIVED` action row.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-01 moves the rule and the action into `rwb_document` and removes every cross-module read: the hold and the case number come from the P3 contract and the ledger rows stay with P1. DP-03 replaces the in-process decision-log writer with the local library, so the run record and the `DOCRET` record share one transaction. DP-07 keeps the four lists out of the code. DP-10 replaces JOB-17 on Quartz with a Schedule and four activities of the workflow kit. DP-11 is the one-hop shape of the P3 and P1 calls. DP-13 and DP-15 give the service its own base and its own migration step. DP-19 puts the run read behind the gateway-bff composite route.

This is a **secondary slice** and it creates no H dependency of its own: the metadata rows `Depends on (build)`, `Contract dependencies`, `Integration dependencies` and `External dependencies` stay exactly as the Work Package fixes them, and the five H rows of the pattern table are the platform stories that the P5 service's own stories already depend on. The story builds against their published contracts and the fakes of 12.8 until they publish (GAP-1029; ASM-1969).

**Done when.** The tests in section 16 pass, the boundary test on the module tables passes, a synthetic run on 2026-12-06 archives 1,250 document rows under `retention/2026-12-06/document/` and deletes them after the manifest check, the held case RW-2024-000311 keeps its 40 documents, and one `DOCRET` record is on `rwb.decision-record.v1` for the run with no personal data.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-020 | Retention run summary to Compliance (new, see additions) | {count} rows of {product} were archived under rule {rule} version {version}. {held} cases on legal hold were kept. |
| MSG-GEN-002 | `retention_months` outside 1 to 600 | {field} must be between {min} and {max}. |
| MSG-P1-002 | Retention load refused at a check | The {source} load for {date} was refused: {check}. The previous load is still in use. |
| MSG-GEN-006 | Archive container unavailable, the manifest check failed, or the P3 case contract did not answer | {system} is not available. Your request is queued and will be retried. |
| MSG-P2-006 | Rerun while the run is active | {job} is already running. Wait for it to finish before you run it again. |
| MSG-P4-002 | Role without the right on the run read or the rerun | You cannot {action} here. Your role does not include it. |

The six message IDs are copied from RWB-E1-017; the MSG-P2-006 wording follows the Error and Message Standard v4, and the other wording is copied from RWB-E1-017 unchanged; MSG-P1-020 keeps its legacy P1 prefix because the ID is the one the legacy sources and the integration story already use, and no new ID is invented for it. Thai text for each message follows decision DL10, which is still open; its assumptions: Not specified in the source documents (DOR-RWB-P5-E1017-APP-18).

HTTP mapping: 422 for MSG-GEN-002 (a load row outside the range), 422 for MSG-P1-002 (a refused load, with the check named), 409 for MSG-P2-006, 403 for MSG-P4-002, 503 for MSG-GEN-006 on a failed run read or a failed step. Every error is an RFC 9457 problem response with `messageId` set to the ID above, `detail` carrying the text with its placeholders filled, and `instance` naming the request.

The MSG-GEN-006 `{system}` values used by this story are "Archive container" for a write or a manifest mismatch (AC5) and "Case service" for the P3 timeout (X8). The MSG-P1-002 `{check}` values are "decision_log_entry is not archived by the retention job" (AC4) and the field and range check for a refused months row. The MSG-P1-020 `{count}`, `{product}`, `{rule}`, `{version}` and `{held}` values come from the run record only.

### 15. Screens and states

No screen in this story. Compliance reads the run, the counts, the archive location and the hold report through `GET /api/recovery/document/v1/admin/retention-runs` and the summary alert MSG-P1-020. Retention classes show on SCR-47 Personal data from Epic 8; until then they are loaded by file. The document retention panel is RWB-P5-AD021-APP and its screen is not built here.

The run read shows one row per run with these states:

| State | What the reader sees |
|---|---|
| Running | The run date, the rule version in force and the step in progress; the rerun action is disabled |
| Complete | The counts per product and table, the archive location, the hold report with case numbers and counts, and the P1 answer with its counts |
| Failed | The failed step and its message (MSG-GEN-006 or the specific check), with the rerun action enabled for a role holding Platform administration `U` |
| Empty | Not specified in the source documents (CG-ALL-5772) |
| Loading | Not specified in the source documents (CG-ALL-5772) |
| Error | Not specified in the source documents (CG-ALL-5772) |
| No access | Not specified in the source documents (CG-ALL-5772) |

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-017-01 | AC1, BR1, BR2, BR4 | End to end | 1,250 old and 4,800 recent synthetic document rows; run date 2026-12-06 |
| TC-E1-017-02 | AC2, BR7 | End to end | Version RET-2027.01 at 36 months; document rows from 2024-01-15 and 2023-12-20 |
| TC-E1-017-03 | AC3, BR3 | End to end | Case RW-2024-000311 on legal hold with 40 old documents |
| TC-E1-017-04 | AC4, BR6 | End to end | A load row with 0 months |
| TC-E1-017-05 | AC5, BR4 | End to end | Archive-container stub refusing writes |
| TC-E1-017-06 | AC6 | End to end | JOB-17 run twice on 2026-12-06 |
| TC-E1-017-07 | AC2, BR2 | End to end | A document at exactly 24 months, captured_at 2024-12-06T00:00+07:00 |
| TC-E1-017-08 | AC4, BR5 | End to end | A load row for product DP12, table decision_log_entry |
| TC-E1-017-09 | AC7 | End to end | A rerun posted during a running JOB-17 |
| TC-E1-017-10 | AC8 | Component | A role without Platform administration U posts a rerun of JOB-17; refused with MSG-P4-002 |
| TC-E1-017-11 | BR9, BR10 | Contract | Each operation, event and activity of section 12 against the RWB-P1-E1017-CON and P3 contract mocks |
| TC-E1-017-12 | BR1, BR9 | Boundary | Each table of section 12.7 in `rwb_document`, and a query on any other schema |
| TC-E1-017-13 | AC9, BR2 | End to end | A document at exactly 24 months, captured_at 2024-12-06T00:00+07:00 |
| TC-E1-017-14 | AC10, BR8 | Component | A rule row naming another archive container |
| TC-E1-017-15 | AC11, BR9 | Boundary | A run for a DP10 document; schema boundary check on the module |
| TC-E1-017-16 | AC12, BR10 | End to end | A JOB-17 Schedule run that calls the P1 archive contract |
| TC-E1-017-17 | AC13 | Component | Not specified in the source documents (NEWAC-RWB-P5-E1017-APP-AC12) |
| TC-E1-017-18 | AC14 | End to end | Not specified in the source documents (NEWAC-RWB-P5-E1017-APP-AC13) |
| TC-E1-017-19 | AC15 | Contract | Not specified in the source documents (NEWAC-RWB-P5-E1017-APP-AC14) |

The ten legacy test case IDs are kept in their legacy order; TC-E1-017-11 to TC-E1-017-19 are added by this story for the contract and boundary tests and for criteria AC9 to AC15. The legacy Level System maps to End to end, and Access maps to Component. The Covers column names this slice's own criteria because the legacy AC1 to AC9 are owned by RWB-P1-E1017-APP and proved end to end by RWB-ITG-E1017-ITG (GAP-1029; ASM-1969); the legacy criteria that name `interaction` rows are the P1 side of the same run and are exercised through RWB-P1-E1017-CON, not through a P5 table. The `-ITG` copies of these cases belong to RWB-ITG-E1017-ITG. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: periods, tables, age-basis fields, the end action, the archive location, the run time and the batch size are data rows or properties.
- No personal data in the run record, the hold report, the archive manifest, the decision record, the logs or the tests: counts and case numbers only, and every test row is synthetic.
- No read of another service's table (DP-01): the legal hold and the case number come from the P3 case contract, the ledger rows are P1's through RWB-P1-E1017-CON, and the decision log is P7's and is never opened.
- The decision log is never archived and never deleted by this run, and no document is deleted before its archive copy is written and read back (BR4, BR5).
- One hop and a 2 s timeout on every consumed call, with a breaker per downstream (DP-11, ADR-020).
- The archive is write-once and is never overwritten: one file per rule and table per run date, with the manifest that makes the copy checkable.
- The run is idempotent by the run date and the rule version, and the Schedule holds one run at a time, so a rerun finds only the documents still past their rule.
- No data lake (DP-17): no lake copy, no Power BI feed from a lake and no ad-hoc extract is written by this story.
- One evaluator if any: this story evaluates no rule package, so no Drools kit is loaded and no rule row is read.
- The feature flag `rwb.document.retention` pauses the Schedule and the admin operations without a rollback of the schema.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-RDF-013 | Retention and archive rule by record class | Business Requirements Epic 1, sections 3.1 and 4 | FEAT-RDF-17 | All recovery processes | R-UNI-20, R-UNI-38; CTL-08; DL26 | TC-E1-017-01 to TC-E1-017-19 |

| Legacy reference | Where it is kept |
|---|---|
| Rule version RET-2026.11 and 24 months | Background, sections 3, 4, 8, 13, 14, 16 |
| JOB-17 Retention job, monthly first Sunday, 02:30 Asia/Bangkok | Sections 4, 9, 12.5, 12.6, 13 |
| Archive path `retention/YYYY-MM-DD/<table>/` and the manifest | Sections 4, 7, 8, 12.5, 13 |
| Decision code DOCRET and the DOCRET record | Sections 1, 4, 7, 8, 12.3, 12.7, 13 |
| LOV-RETENTION-ACTION (ARCHIVED, LISTED, HELD, EXCEPTION) and LOV-RETENTION-END (ARCHIVE, REVIEW) | Sections 3, 8, 11, 12.1, 13 |
| MSG-P1-020, MSG-GEN-002, MSG-P1-002, MSG-GEN-006, MSG-P2-006, MSG-P4-002 | Section 14, exception paths |
| Rules R-UNI-20, R-UNI-38; CTL-08; DL26 | Sections 2, 3, 8, 18 |

The legacy key is RWB-E1-017 and its disposition is Split (rework). The other slices are RWB-P1-E1017-CON and RWB-P1-E1017-APP (the interaction ledger and the P1 side of the run), RWB-P7-E1017-APP (the decision log and its exclusion) and RWB-ITG-E1017-ITG (the end-to-end proof). This story owns none of their criteria.

### 19. Out of scope

- The retention classes and the virus scan on intake (RWB-P5-E1041-APP and RWB-P5-E1016-APP).
- The document-retention screen and the retention-class administration panel (RWB-P5-AD021-APP).
- The interaction-ledger archive and its own `retention_action` rows (RWB-P1-E1017-APP and RWB-P1-E1017-CON).
- The decision log retention period and the decision log itself (NFR-030, DL26, RWB-P7-E1017-APP).
- Case closure after the retention period (REQ-S7-008, Epic 6).
- The personal data screen SCR-47 (Epic 8).
- The provisioning of the archive container, its immutability policy and its backup (RWB-PLT-TE012-APP).
- The Helm chart, the alerts and the runbook of a failed run (the deployment stories).
