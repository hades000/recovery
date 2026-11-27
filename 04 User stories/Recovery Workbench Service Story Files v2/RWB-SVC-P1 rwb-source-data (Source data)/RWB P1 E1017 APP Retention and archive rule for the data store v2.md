# RWB-P1-E1017-APP Retention and archive rule for the data store

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P1-E1017-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-source-data |
| Service epic | RWB-SVC-P1 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Size | To be sized by the squad at refinement (DOR-RWB-P1-E1017-APP-16) |
| Legacy key | RWB-E1-017 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP07, DP10, DP11, DP13, DP15, DP19 |
| Parallel lane | L-P1-A |
| Ready to start | After RWB-P1-E1001-APP, RWB-P1-E1064-APP |
| Depends on (build) | RWB-P1-E1017-CON, RWB-PLT-E1027-CON, RWB-PLT-E1043-CON, RWB-PLT-E1071-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON, RWB-P1-E1001-APP, RWB-P1-E1064-APP |
| Contract dependencies | RWB-P3-E1043-CON |
| Integration dependencies | None |
| External dependencies | RWB-P1-E1017-OPS, RWB-PLT-TE012-APP |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v1.md (FR-P1-028) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-017 for rwb-source-data. The rule table `retention_rule` and the retention action are rwb-document's in the target (Ownership Map ruling ASM-0076; Architecture v5 slides 16, 41 and 44), so this story holds no rule table and registers no Schedule: it delivers the retention action on rwb-source-data's own tables, started by P5's JOB-17 through `POST /retention-runs`, archived to the write-once container of RWB-PLT-TE012-APP and held back by the rwb-case legal-hold interface. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P1-E1017-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (22 resolved, 25 cross-document, 2 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **Compliance and PDPA officer (RW-COMPLY)**, I want **a retention rule per data product and table, held as reference data, applied by a job that archives rows past their rule and logs the action**, so that **the store holds what the policy allows and nothing older**.

The legacy story built the whole of it inside the recovery module: a `retention_rule` table beside the recovery tables, a Quartz trigger for JOB-17, the selection, the archive writer, the legal-hold exclusion and the delete. D-RCV-60 keeps the behaviour and moves the ownership:

- **rwb-document (P5)** owns `retention_rule` and `retention_action`, loads, validates and approves the version, and owns the monthly Schedule JOB-17 (retention, first Sunday) on task queue `rwb-document` (Ownership Map ruling ASM-0076; Architecture v5 slides 16, 41 and 44).
- **rwb-source-data (P1), this story,** owns the action on its own tables: it validates the rules it is handed against its own metadata, selects the rows past their age-basis date, archives them with a manifest, checks the manifest and then deletes them in one transaction per table and rule.
- **rwb-case (P3)** owns the legal hold. P1 reads it once per run through the published `CaseHoldQuery` interface, never by SQL (DP-01, DP-11).
- **RWB-PLT-TE012-APP** owns the write-once container; P1 writes `retention/YYYY-MM-DD/<table>/` into it and reads the manifest back.

The tables in scope are `interaction`, `case_list_row`, `reconciliation_result`, `data_product_load`, `party_ext`, `contact_point_ext`, `account_ext` and `valuation_ext`. `decision_log_entry` is P7's table and `retention_rule` is P5's: this story neither reads nor writes either, and it keeps no copy of a rule. The run is started by `POST /retention-runs` on base `/api/recovery/source-data/v1` and read back through `GET /retention-runs/{runId}`.

### 2. Business rationale

PDPA and the bank retention schedule limit how long personal data is kept, and today recovery records stay in spreadsheets and systems with no end date. A retention rule per data product and table, loaded as versioned data, lets Compliance set and change periods without a release. A monthly run archives rows past their period to a write-once archive container and removes them from the live store, keeps every row of a case under legal hold, and records what it did. That is REQ-RDF-013, with NFR-031 and NFR-072 behind it, and the measure of FSD P1 A2.17: 100 percent of the Workbench records past their retention archived or on legal hold each month, measured on the JOB-17 run record.

The target changes where each half lives, not what the officer gets. The rule stays data, but it is P5's data: one versioned, approved row set beside the documents that carry the same retention classes, so Compliance changes a period once and not once per service (Architecture v5 slides 16 and 41; ASM-0076). The monthly Schedule is P5's too (slide 44, JOB-17, first Sunday), and it starts each owner's action through that owner's contract. rwb-source-data therefore runs an action and not a rule engine: it receives the rule version, the run date and the rules, proves them against its own tables and dictionary, and applies them to the eight tables it owns.

Three things are deliberately different from the legacy monolith. The archive goes to the write-once container and not to a data lake, because Arch v5 removes the lake and its Power BI feed (DP-17; ADR-018). The legal hold comes over an interface with a fake, so the run is testable on Day 1 and no case row is read by SQL (DP-01, DP-11). And the interaction ledger stays P1's under the default ruling and DP-18, so the ledger that the case timeline reads is retained by the service that owns it.

### 3. Preconditions

- RWB-P1-E1001-APP is done: schema `rwb_source_data` holds the eight tables in scope, the standard record columns, `data_product` with DP01 to DP14, `sys_objects` and `sys_fields`, and the append-only trigger with its `refuse_change()` function (legacy RWB-E1-001 in the target).
- RWB-P1-E1064-APP is done: the dictionary rows name every column of every table in scope, so an age-basis field can be proved against `sys_fields` for its table (legacy RWB-E1-064 in the target).
- The per-service Flyway sequence of rwb-source-data exists with its own history table, and the purge-setting change of this story is a later version on that sequence (DP-15; RWB-PLT-E1044-CON).
- RWB-P1-E1017-CON is published: the OpenAPI document, the `RetentionRunWorkflow` contract, the request and response schemas, the `409` rule and the retention-run fake that P5's JOB-17 tests call.
- RWB-PLT-E1071-CON is available: the workflow kit, the namespace `rwb-recovery` and the task queue `rwb-source-data`, so `RetentionRunWorkflow` starts on Day 1 against the kit.
- RWB-P3-E1043-CON is published, and rwb-case publishes `CaseHoldQuery` with its fake: `casesOnLegalHold()` and `caseNumbers(...)` answer from the contract and not from a table of P1 (legacy section 12; DP-11).
- RWB-PLT-TE012-APP has delivered a write-once container in each environment that the rwb-source-data login may write, and the run's read-back check passes on it.
- Retention rule version "RET-2026.11" is in force with DP05 `interaction` at 24 months on `occurred_at` (assumed until Compliance supplies the bank schedule; DL26), and the rwb-document load and approval of that version is P5's story.
- Properties `rwb.source-data.retention.archive-container` and `rwb.source-data.retention.batch-size=5000` are present as configuration, not as constants.
- The split of the legacy ACs and the shape of the P1 retention-run contract are Not specified in the source documents (GAP-0488; ASM-0680) and (GAP-0489; ASM-0681); the run contract fixed by this story is `POST /retention-runs` carrying the rules and `GET /retention-runs/{runId}`.

### 4. Flow

1. rwb-document: loads retention rule version "RET-2026.11" through its own load path, validates it in full and approves it; the rows, the validation and the version in force are P5's (ASM-0076; RWB-P5-E1017-APP).
2. rwb-document: its Schedule JOB-17 fires on the first Sunday of the month (02:30 Asia/Bangkok in the legacy cron) and starts the owners' retention actions; the run date is the business date of that Sunday, for example 2026-12-06 (Architecture v5 slide 44, JOB-17; DP-10).
3. P5: calls `POST /retention-runs` on `/api/recovery/source-data/v1` with an `Idempotency-Key` built from the run date and the rule version, and a body carrying the rule version, the run date and the rules, one per product, table, record class, retention months, age-basis field and end action; the answer is `202 Accepted` with the `runId`.
4. rwb-source-data: `validateRules` proves the request against its own metadata before any row is touched: the product exists in `data_product`, the table is one of the eight tables this story owns, the table is not `decision_log_entry` and not a `v_ace_*` view or a `public` table, the age-basis field exists in `sys_fields` for that table, the months sit between 1 and 600, and the end action is ARCHIVE or REVIEW; one bad rule refuses the run in full (BR6; MSG-GEN-002, MSG-P1-002).
5. rwb-source-data: `casesOnLegalHold()` and `caseNumbers(...)` of the published `CaseHoldQuery` interface of rwb-case are called once, one hop with a 2 s budget, through the contract fake on Day 1; no case table is read by SQL and the transport detail is settled in RWB-P1-E1017-CON; the case IDs and case numbers of the held cases are held for the exclusion and the hold report (DP-11).
6. rwb-source-data: `selectRows(page)` reads, per rule, the rows whose age-basis field is older than the run date minus the retention months, in pages of the batch size 5000, and leaves out every row of a held case; a row exactly at its retention age is kept (AC7).
7. rwb-source-data: `archiveTable` writes the selected rows of one table as JSON lines under `retention/YYYY-MM-DD/<table>/` in the write-once container, with a manifest carrying the row count and the SHA-256 of every file; `verifyManifest` reads the manifest and the files back and compares count and hashes before anything is deleted (BR4).
8. rwb-source-data: `deleteArchivedRows` deletes the archived rows in one transaction per table and rule, under the transaction setting `rwb.retention.purge` that the append-only trigger allows; an UPDATE is refused as before and `decision_log_entry` keeps its unconditional refusal (BR5).
9. rwb-source-data: `recordRun` writes on the run the counts per product and table, the rule version, the archive location and the hold report, and `GET /retention-runs/{runId}` answers them; the summary alert to Compliance carries MSG-P1-020, and the same run is visible in the job monitor that another P1 story owns.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A case is on legal hold | Its rows are kept and listed in the hold report | MSG-P1-020 | AC3 |
| X2 | A rule row has months outside 1 to 600 | The rules are refused in full before any selection; the previous version stays in force for the next run | MSG-GEN-002 | AC4 |
| X3 | The archive write or the manifest check fails | No row deleted; the run ends Failed; the alert is raised; the rerun repeats the unit | MSG-GEN-006 | AC5 |
| X4 | A run is started again for the same run date and rule version | Rows already archived are gone, so the rerun archives only rows still past their rule | None | AC6 |
| X5 | A row is exactly at its retention age | The row is kept | None | AC7 |
| X6 | A rule names `decision_log_entry` | The rules are refused in full; the decision log is never archived by this run | MSG-P1-002 | AC8 |
| X7 | A second start is posted while a run for that run date is active | `409`; the active run continues and no second archive is opened | MSG-P2-006 | AC9 |
| X8 | The legal-hold answer does not arrive inside the 2 s budget | The run fails before any selection; nothing is archived and nothing is deleted, because a hold that is unknown is treated as a hold | None from this service; the breaker opens | AC10 |
| X9 | The `Idempotency-Key` is replayed with a different body | `422` with the error envelope; the stored answer is not overwritten | MSG-GEN-001 | AC11 |
| X10 | A rule names a table this story does not own | The rules are refused in full and the table is named | MSG-P1-002 | AC12 |

X1 to X7 are the exception paths of RWB-E1-017 carried onto the split. X8 to X10 are the paths the contract adds: a called interface, a stored answer and a table list that is now a set of eight names rather than "every table in the schema".

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the published P1 contract, the workflow kit, the reference-data contract and the legal-hold interface with their fakes on Day 1; needs the P1 baseline and the dictionary for its own tables; the WORM container is an external dependency |
| Negotiable | The rule rows, periods, tables and age-basis fields are data handed in by P5; the story fixes the validation, the archive layout, the manifest and the purge behaviour |
| Valuable | The eight tables keep no row longer than their rule, every removal is recorded, and a held case is never touched |
| Estimable | One contract surface, one workflow, six activities, one manifest writer, one purge-setting migration and one message |
| Small | Fits one sprint with its tests, as the action slice of the legacy key |
| Testable | Every criterion runs on synthetic rows with a test clock, a stubbed container and a stubbed legal-hold answer |

### 7. Acceptance criteria

```gherkin
Feature: Retention and archive rule for the data store

  Background:
    Given retention rule version "RET-2026.11" holds product "DP05", table "interaction", age basis "occurred_at", 24 months
    Given the run date is Sunday 2026-12-06
    Given the rwb-document JOB-17 Schedule starts the rwb-source-data retention run through the /retention-runs contract with that rule version, that run date and those rules

  Scenario: AC1 Retention rule applied (legacy RWB-E1-017 AC1)
    Given 1,250 interaction rows with occurred_at before 2024-12-06 and 4,800 rows from 2024-12-06 onward
    When JOB-17 runs
    Then 1,250 rows move to the archive container under "retention/2026-12-06/interaction/"
    Then the 1,250 rows are no longer in the live interaction table
    Then the job run logs count 1,250 for DP05 interaction under rule version "RET-2026.11"

  Scenario: AC2 Rule changed as data (legacy RWB-E1-017 AC2)
    Given retention rule version "RET-2027.01" changes DP05 interaction to 36 months, approved and valid from 2027-01-01
    Given interaction rows with occurred_at on 2024-01-15 and on 2023-12-20
    When JOB-17 runs on Sunday 2027-01-03
    Then the row from 2024-01-15 stays in the live table
    Then the row from 2023-12-20 moves to the archive container
    Then the job run logs rule version "RET-2027.01"

  Scenario: AC3 Legal hold (legacy RWB-E1-017 AC3)
    Given the rwb-case legal-hold contract mock returns case "RW-2024-000311" on legal hold with 40 older interaction rows
    Given case "RW-2024-000311" is marked legal hold and has 40 interaction rows older than 24 months
    When JOB-17 runs
    Then the system keeps its 40 rows in the live table
    Then the hold report lists case "RW-2024-000311" with 40 rows kept
    Then the summary alert to Compliance reads MSG-P1-020 with 1 case on legal hold kept

  Scenario: AC4 A rule with months outside the allowed range (legacy RWB-E1-017 AC4)
    Given a retention load version "RET-2026.12" with a row for DP05 interaction at 0 months
    When the load is validated
    Then the system refuses the load in full with MSG-GEN-002 for field "retention_months" between 1 and 600
    Then version "RET-2026.11" stays in force

  Scenario: AC5 The archive write fails (legacy RWB-E1-017 AC5)
    Given the archive container refuses writes
    When JOB-17 runs
    Then the system deletes no interaction row
    Then the job run ends "FAILED" with MSG-GEN-006 for system "Archive container"

  Scenario: AC6 A repeat run in the same month (legacy RWB-E1-017 AC6)
    Given JOB-17 archived 1,250 rows on 2026-12-06
    When JOB-17 is rerun on 2026-12-06
    Then the system archives 0 rows
    Then the archive container still holds one set of the 1,250 rows

  Scenario: AC7 A row exactly at its retention age (legacy RWB-E1-017 AC7)
    Given an interaction row with occurred_at 2024-12-06T00:00+07:00
    When JOB-17 runs on 2026-12-06
    Then the row stays in the live table

  Scenario: AC8 A rule for the decision log is refused (legacy RWB-E1-017 AC8)
    Given a retention load version "RET-2026.12" with a row for product "DP12", table "decision_log_entry"
    When the load is validated
    Then the system refuses the load in full with MSG-P1-002 and check "decision_log_entry is not archived by the retention job"

  Scenario: AC9 A rerun while the job is running (legacy RWB-E1-017 AC9)
    Given JOB-17 is running
    When a platform administrator posts a rerun of JOB-17
    Then the system refuses the rerun with status 409 and MSG-P2-006

  Scenario: AC10 The legal-hold answer does not arrive in time (new, D-RCV-60)
    Given the rwb-case legal-hold answer for the run does not arrive inside the 2 s budget
    When JOB-17 runs
    Then the run ends "FAILED" before any selection
    Then the system archives no row and deletes no row
    Then the circuit breaker to the rwb-case legal-hold interface opens

  Scenario: AC11 An Idempotency-Key is replayed with a different body (new, D-RCV-60)
    Given a retention run was started with an Idempotency-Key and a body with rule version "RET-2026.11"
    When the same Idempotency-Key is posted with a body that differs
    Then the system answers 422 with the error envelope and MSG-GEN-001
    Then the stored answer of the first start is not overwritten

  Scenario: AC12 A rule names a table this story does not own (new, D-RCV-60)
    Given a retention load version "RET-2026.12" with a row for product "DP05" and a table this story does not own
    When the load is validated
    Then the system refuses the load in full with MSG-P1-002 and names the table in the {check} value

  Scenario: AC13 A rule names an ACE view (new, D-RCV-60)
    Given a retention load version "RET-2026.12" with a row for product "DP05" and table "v_ace_efs_action"
    When the load is validated
    Then the system refuses the load in full with MSG-P1-002 and check "v_ace_efs_action is ACE data; ACE applies its own retention"

  Scenario: AC14 An error answer of a provided operation carries its status (new, D-RCV-60)
    Given a caller presents no credential to POST /retention-runs
    When the caller posts a retention run
    Then the system answers 401
    Given a caller without the right to start a run
    When the caller posts a retention run
    Then the system answers 403
    Given a runId that does not exist
    When the caller gets GET /retention-runs/{runId}
    Then the system answers 404

  Scenario: AC15 An activity of the run is retried or times out (new, D-RCV-60)
    Given an archive activity of RetentionRunWorkflow times out before its answer
    When the activity is retried
    Then the retry repeats the unit
    Then no row is deleted before the archive copy is checked

  Scenario: AC16 A consumed call fails or does not answer (new, D-RCV-60)
    Given the rwb-case legal-hold contract mock returns an error for the run
    When JOB-17 runs
    Then the run ends "FAILED" before any selection
    Then the system archives no row and deletes no row
```

**Target reading.** Every assertion keeps its legacy wording; what changes is who runs it and where the rule comes from. "When JOB-17 runs" is now "when the P5 Schedule JOB-17 starts the rwb-source-data run through `POST /retention-runs`", and the run date, the rule version and the rules arrive in that request rather than from a `retention_rule` table, which this service no longer holds (ASM-0076; Architecture v5 slides 16 and 44). "The load is validated" in AC4 and AC8 is the same validation performed twice in the target: rwb-document refuses the version at its own load, and rwb-source-data refuses the same rules in full when a run presents them, so the criteria run against the P1 validation with the messages unchanged and version "RET-2026.11" still in force for the next run. The two operations are `POST /retention-runs` and `GET /retention-runs/{runId}` on `/api/recovery/source-data/v1`, with the rule version, the run date and the rules in the request, and the status, counts per table, rule version, archive location and held cases in the answer; the field-level detail is settled in RWB-P1-E1017-CON. The legal-hold part of AC3 is stubbed with the rwb-case contract mock named in its Given, so the 40 rows and the case number "RW-2024-000311" are the fixture's and no case table is read by SQL. The archive of AC1, AC2, AC5 and AC6 is the write-once container of RWB-PLT-TE012-APP under `retention/2026-12-06/interaction/`, read back through its manifest, and the container's own contract is Not specified in the source documents (GAP-0490; ASM-0682). The count of 1,250, the 4,800 recent rows, the 24 and 36 months, the dates 2024-01-15, 2023-12-20 and 2024-12-06T00:00+07:00, the run dates and the message IDs are the legacy values, unchanged, and AC10 to AC16 are added: AC10 to AC12 for exceptions X8 to X10, AC13 for BR8, AC14 for the error answers, AC15 for a retried or timed-out activity and AC16 for a failed consumed call.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Each data product and table has one retention rule in force, held as a versioned data row | Retention classes reference table (refdata.txt); DL26; Principle 1 |
| BR2 | A row older than its retention period on its age-basis field is archived and removed from the live store | `retention_months`; REQ-RDF-013 |
| BR3 | A legal hold keeps every row of the case, overriding the retention rule | R-UNI-20; NFR-072 |
| BR4 | A row is removed only after its archive copy is written and checked | Archive container (RWB-PLT-TE012-APP); NFR-074 |
| BR5 | The decision log is not archived by this run; its retention is set by Compliance and executed in rwb-decision | NFR-030; ADR-009; DL26 |
| BR6 | A rule set with an exception is refused in full | Reference data change process, step 3; CTL-08 |
| BR7 | A new version applies from its valid-from date; earlier runs keep their recorded version | R-UNI-38 |
| BR8 | A rule names a table of this service that this story owns and a column of that table; a `v_ace_*` view, a `public` table and `decision_log_entry` are refused, because ACE and rwb-decision apply their own retention | BR-P1-017-2; FSD P1 A2.17 |

**Where each rule lives in the target.** BR1, BR6 and BR7 are rules about the rule set, and the rows and the approval are rwb-document's (ASM-0076); this story keeps the validation of a rule set it is handed and nothing else. BR2, BR3, BR4 and BR8 are this story's own behaviour: the selection, the hold exclusion through the rwb-case interface, the archive-then-delete order of the manifest check, and the table-and-column test against `data_product`, `sys_objects` and `sys_fields`. BR5 is a refusal in this service and the retention itself in rwb-decision (P7), whose decision log is never named in a rule. No rule here fixes a business value: the months, the tables, the age-basis fields and the end action are all data in the request. P5 rwb-document owns both retention tables, `retention_rule` and `retention_action`, the load and the retention Schedule JOB-17 (ASM-0076); this service holds no rule table and no Schedule, keeps only a contract read, receives the rule version, the run date and the rules in the run request, validates them against its own tables and applies them to its own eight tables. Each owner applies the rule to its own schema, and the suite asserts the rule version, legal holds and the decision-log exclusion through the owners' APIs and Temporal visibility. Each archive or purge action writes a decision record whose decision code and final call come from LOV-DECISION and the final-call list through the rwb-case reference-data contract, with ruleId empty, the run reference in inputsRef, and the product, table, counts, hold report reference and archive location in actions and outcome; the value names are settled with the reference-data owner before the first joint environment.

### 9. State transitions

None. This story does not change a case status. It changes the run status of the retention action (Running, Complete, Failed) and, through P5, the retention rule version in force.

| From | Event | Condition | To |
|---|---|---|---|
| no run for the run date | `POST /retention-runs` accepted | The rule set validates and no run for that date is active | Running |
| Running | Manifest checked and rows deleted for every table and rule | Every unit completed | Complete |
| Running | A unit fails | The archive write, the manifest check or the delete failed | Failed |
| Failed | A rerun for the same run date | The previous run is not active | Running |
| Running | A second start for the same run date | A run is active | Unchanged, with `409` on the second call |
| any run | The next rule version | P5 loads and approves a later version | The next run reads the new version; earlier runs keep their recorded version |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-COMPLY, Compliance and PDPA officer | Owns the retention periods; reads the run result and the hold report through `GET /retention-runs/{runId}` and the summary alert (Platform administration R) |
| RW-REFADM, reference data administrator | Submits the retention load to rwb-document (Reference data C); this service receives the rules in the run request |
| Holder of Reference data A | Approves the retention load in rwb-document |
| RW-DATASTEW, data steward | Reads the run result for their products |
| RW-PLATADM, platform administrator | Starts a rerun of the retention action and reads the run (Platform administration U) |
| SY-DATALOAD, data load | Is the service identity that runs the action, writes the archive and deletes the archived rows |
| SY-CASEWF, case workflow module | Answers `CaseHoldQuery` from rwb-case |

The approval of the rule set is P5's authority in the target, and the legacy approval row is kept here to show where it moved. Each operation of this service (`POST /retention-runs` and `GET /retention-runs/{runId}`) is authorised through rwb-access before it runs; the authorise check name is Not specified in the source documents (DOR-RWB-P1-E1017-APP-6). This story takes no business decision of its own, and no approval level from the delegation of authority applies to it: a run either satisfies its rules or is refused.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-002 | `recovery_case` (P3, over the contract) | case_no | Read through `CaseHoldQuery` |
| DF-CAS-020 | `recovery_case` (P3, over the contract) | legal_hold | Read through `CaseHoldQuery` |
| DF-INT-001 | `interaction` | id | Write (deleted once archived) |
| DF-INT-002 | `interaction` | case_id | Read |
| DF-INT-003 | `interaction` | person_key | Read |
| DF-INT-004 | `interaction` | occurred_at | Read |
| DF-INT-005 | `interaction` | channel | Read |
| DF-INT-006 | `interaction` | direction | Read |
| DF-INT-007 | `interaction` | action_code | Read |
| DF-INT-008 | `interaction` | contact_result | Read |
| DF-INT-009 | `interaction` | promise_amount | Read |
| DF-INT-010 | `interaction` | promise_date | Read |
| DF-INT-011 | `interaction` | summary | Read |
| DF-INT-012 | `interaction` | conduct_check | Read |
| DF-INT-013 | `interaction` | source_system | Read |
| DF-REF-116 to DF-REF-126 | `retention_rule` (P5's table) | id, product_code, table_name, record_class, retention_months, age_basis_field, end_action, rule_version, valid_from, valid_to, approved_by | Read in the request only; never read from or written to the table |
| DF-RPT-001 onwards | `case_list_row` | all columns | Write (archive and delete) |
| DF-OPS-118 onwards | `reconciliation_result` | all columns | Write (archive and delete) |
| DF-OPS-001 onwards | `data_product_load` | all columns | Write (archive and delete) |
| DF-EXT-001 to DF-EXT-012 | `party_ext` | all 12 fields | Write (archive and delete) |
| DF-EXT-013 to DF-EXT-026 | `contact_point_ext` | all 14 fields | Write (archive and delete) |
| DF-EXT-027 to DF-EXT-035 | `account_ext` | all 9 fields | Write (archive and delete) |
| DF-EXT-036 to DF-EXT-049 | `valuation_ext` | all 14 fields | Write (archive and delete) |

The interaction id row is written in the sense that archived rows are deleted from the live table, and the same holds for the other seven tables. Field IDs are those in the Logical Data Model and Data Dictionary.

**Which side is this story's.** The `interaction`, `case_list_row`, `reconciliation_result`, `data_product_load` and four extension rows are this story's: their rows are selected, archived and deleted here. The `retention_rule` rows are P5's: the field IDs are kept so the request schema is expressed in the bank's own field names, and no row of that table is read or written by rwb-source-data (ASM-0076). `decision_log_entry` is P7's and appears in no rule. The age-basis column of each table is read from `sys_fields`, so a rule naming a column that the table does not have is refused before a row is read.

### 12. Contract

#### 12.1 REST operations provided

Two operations on base `/api/recovery/source-data/v1` (DP-13). The first is the start that P5's JOB-17 calls; the second is the run record that Compliance and P5 read.

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| POST | `/retention-runs` | Start one retention run for a run date and a rule version: validates the rules against this service's own tables, archives the selected rows, checks the manifest and deletes them per table and rule | Platform administration U, or the rwb-document service identity with the same right | `Idempotency-Key` required; the stored answer is returned for a replay with the same body, `422` for a different body |
| GET | `/retention-runs/{runId}` | Status, the counts per table, the rule version, the archive location and the held cases of one run | Platform administration R | Read only |

Request body: the rule version, the run date and the rules, each with `productCode`, `tableName`, `recordClass`, `retentionMonths`, `ageBasisField` and `endAction`. Answer to a start: `202 Accepted` with the `runId`. Errors: `400` for a malformed body, `401`, `403`, `409` for an active run for the same run date, `422` for a refused rule set, `503` when the legal-hold answer or the container does not answer.

The response field names of the two operations, the page shape of the counts and the problem body are Not specified in the source documents (GAP-0489; ASM-0681); this story fixes the two paths, the request fields and the answer to a start, and RWB-P1-E1017-CON fixes the schemas.

The legacy job monitor of `GET /admin/jobs` and its rerun operation are other P1 stories; this story adds neither and changes no path of theirs. A run is visible in the monitor through that story's record, and the retention-run operations above are the surface P5 and Compliance use.

#### 12.2 REST operations consumed

| Interface | Operation | Owner | Use | Pattern |
|---|---|---|---|---|
| `CaseHoldQuery` (published interface) | `casesOnLegalHold()` | P3 rwb-case | Once per run: the case IDs whose every row is kept | DP-11; one hop, 2 s timeout, no stale cache |
| `CaseHoldQuery` (published interface) | `caseNumbers(Set<UUID> caseIds)` | P3 rwb-case | Once per run: the case numbers of the held cases for the hold report | DP-11; same hop, same budget |

The interface is the legacy `CaseHoldQuery` of the story's section 12, published by rwb-case and consumed here with the fake named in 12.8; the C dependency recorded for this story is RWB-P3-E1043-CON, the rwb-case contract it is scheduled against, and the legal-hold interface lands with the rwb-case contracts of wave 1. No REST path exists for it in the sources, so the pair of operations is fixed as named above and recorded as (GAP-0491; ASM-0683). When the answer does not arrive inside 2 s the run fails before a selection and nothing is archived or deleted (X8). No other service is called at run time: the lists of values that the request may carry reach this service through the reference-data client library (DP-07), and the rules themselves arrive in the request.

#### 12.3 Events published

None. The topic of the service is `rwb.source-data.events.v1` with event names `rwb.source-data.<Event>.v1` (DP-14), and its two events `AceDataReady` and `AceDataLate` belong to RWB-P1-E1013-APP (Architecture v5 slides 15 and 43). A retention run is a step that P5 starts and reads, so this story publishes no event, writes no outbox row and adds nothing to the shared ledger beyond the decision record of DP-03.

#### 12.4 Events consumed

None. Architecture v5 slide 15 gives rwb-source-data no consumed event ("none: Airflow call; fallback polls ACE batch record"), and the retention run is started by the P5 Schedule and its contract call, not by an event.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `RetentionRunWorkflow` | Workflow, one run per run date and rule version, workflow ID = `retention-<runDate>-<ruleVersion>` | `rwb-source-data` in namespace `rwb-recovery` | Input: rule version, run date, rules; output: status, counts per table, rule version, archive location, held cases |
| `validateRules` | Activity | `rwb-source-data` | Rules in; a refused rule set or the accepted set out; one transaction, no row read |
| `casesOnLegalHold`, `caseNumbers` | Activities wrapping the interface | `rwb-source-data` | Called once per run, 2 s each, retried once with jitter |
| `selectRows(page)` | Activity | `rwb-source-data` | Table, age-basis field and month count in; one page of ids out, batch size 5000 |
| `archiveTable` | Activity | `rwb-source-data` | Page in; the JSON lines files and the manifest with the row count and the SHA-256 per file out |
| `verifyManifest` | Activity | `rwb-source-data` | Manifest location in; a count and hash comparison out; a mismatch fails the unit |
| `deleteArchivedRows` | Activity | `rwb-source-data` | The archived ids and the purge setting in; the delete in one transaction per table and rule |
| `recordRun` | Activity | `rwb-source-data` | The counts, the rule version, the archive location and the hold report in; the run record out |

The workflow is started by the contract call and not by a Schedule, and its `Retry` policy is the kit default with the archive write and the manifest check non-retryable inside a unit: the unit is repeated by a rerun, not by a silent retry.

#### 12.6 Schedules

None. JOB-17 (retention, monthly, first Sunday) is the Schedule of rwb-document on task queue `rwb-document` (Architecture v5 slides 16 and 44; ASM-0076), and this service registers no Schedule of its own.

#### 12.7 Tables owned

| Table | Schema | Owner | This story |
|---|---|---|---|
| `interaction` | `rwb_source_data` | P1 | Read for selection; rows deleted after the manifest check |
| `case_list_row` | `rwb_source_data` | P1 | Read for selection; rows deleted after the manifest check |
| `reconciliation_result` | `rwb_source_data` | P1 | Read for selection; rows deleted after the manifest check |
| `data_product_load` | `rwb_source_data` | P1 | Read for selection; rows deleted after the manifest check |
| `party_ext`, `contact_point_ext`, `account_ext`, `valuation_ext` | `rwb_source_data` | P1 | Read for selection; rows deleted after the manifest check |
| `data_product`, `sys_objects`, `sys_fields` | `rwb_source_data` | P1 | Read only, to validate a rule set; no row is written |
| `retention_rule`, `retention_action` | `rwb_document` | P5 | **Not read and not written here**; the rules arrive in the request |
| `decision_log_entry` | `rwb_decision` | P7 | **Never named by a rule and never touched here** |

No table of another service is read and no foreign key crosses a schema (DP-01). The append-only trigger and its `refuse_change()` function are in P1's schema and are changed by this story's migration so that a DELETE is allowed only inside the purge setting.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-case `CaseHoldQuery` fake (RWB-P3-E1043-CON) | `casesOnLegalHold()`, `caseNumbers(...)` | No case on hold; one case on hold with 40 rows; a timeout; a case number list |
| Write-once container stub (RWB-PLT-TE012-APP) | The archive and its manifest | A writable container, a container refusing writes, a manifest whose count or hash differs |
| Clock control | The run date | 2026-12-06, 2027-01-03 and a row at exactly 24 months |
| rwb-source-data retention-run WireMock (this story, for P5) | `POST /retention-runs`, `GET /retention-runs/{runId}` | A `202` with a `runId`, a `409` for an active run, a `422` for refused rules, a completed run with counts |

The last fake is the one P5's JOB-17 tests call, so rwb-document can prove its Schedule and its start on Day 1 without this service being built.

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 2 operations on `/api/recovery/source-data/v1` | 1 published interface (`CaseHoldQuery`, no REST path in the sources) | OpenAPI 3.1, one hop, 2 s timeout, breaker per downstream (DP-11) |
| Kafka | None | None | The topic `rwb.source-data.events.v1` and its two events belong to RWB-P1-E1013-APP |
| Temporal | 1 workflow, 8 activities | None | Task queue `rwb-source-data` in namespace `rwb-recovery`; no Schedule in this service |
| File | 1 archive path `retention/YYYY-MM-DD/<table>/` with a manifest | The manifest read back for the check | Write-once container of RWB-PLT-TE012-APP; row count and SHA-256 per file |
| SQL | None | None | No view and no other schema is read; the hold comes over the interface |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.sourcedata`, modules `retention`, `archive` and `hold`, with the published types in `...sourcedata.api`. Service base `/api/recovery/source-data/v1`, schema `rwb_source_data`, task queue `rwb-source-data` in namespace `rwb-recovery`, topic `rwb.source-data.events.v1` (not published here).

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

DP-10 is used, not owned: the Schedule is P5's and this story supplies the workflow that the Schedule starts. DP-03 applies as one decision record per run and per refused rule set through the library, with no event of its own. DP-19 applies to the platform administration surface that reads a run and to the Compliance summary, neither of which this story builds.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `RetentionRunWorkflow` | Workflow | One run per run date and rule version; orders validate, select, archive, check, delete and record |
| `RuleSetValidator` | Service | Validates a rule set against `data_product`, `sys_objects` and `sys_fields`, the eight owned tables and the 1 to 600 range |
| `RetentionSelector` | Repository | Reads, per rule and page, the ids past the age-basis date, excluding the held cases; reads no other schema |
| `ArchiveWriter` | Service | Writes the JSON lines files and the manifest with the row count and the SHA-256 per file to the write-once container |
| `ManifestVerifier` | Service | Reads the manifest and the files back and compares count and hashes before any delete |
| `RetentionPurger` | Repository | Deletes the archived rows in one transaction per table and rule, under `rwb.retention.purge` |
| `CaseHoldClient` | Client | The `CaseHoldQuery` interface through the rwb-case contract, one hop, 2 s, breaker (DP-11) |
| `RetentionRunController` | Controller | The two operations on `/api/recovery/source-data/v1`; RFC 9457 problem details |
| `V<n>__rwb_e1_017_retention_purge.sql` | Migration | Replaces `refuse_change()` so that DELETE is allowed only inside the purge setting; UPDATE stays refused and `decision_log_entry` keeps its unconditional refusal |

**Database.** This story creates no table. It adds one migration on rwb-source-data's own Flyway sequence (DP-15) that replaces `refuse_change()` with the purge-setting rule and adds the index that serves the selection where the table has none; the eight tables and their columns come from RWB-P1-E1001-APP and their dictionary rows from RWB-P1-E1064-APP. The run record is the workflow's own state, answered through `GET /retention-runs/{runId}`, and the durable proof of what was archived is the manifest in the container; a job-monitor row is the monitor story's record and is not defined here.

**Configuration and reference data**

- `rwb.source-data.retention.batch-size=5000` bounds a page and a file set.
- `rwb.source-data.retention.archive-container` names the container of RWB-PLT-TE012-APP; the path under it is `retention/YYYY-MM-DD/<table>/`.
- `rwb.retention.purge` is the transaction setting the trigger requires for a DELETE; it is set by `RetentionPurger` inside its own transaction and by nothing else.
- The rule version, the run date and the rules come in the request; the service holds no rule row and no default period (ASM-0076).
- The legal-hold interface, its 2 s budget and its retry are configuration of the client, not constants.

**Build steps**

1. The migration that replaces `refuse_change()` with the purge-setting rule, and a test that UPDATE and DELETE are still refused outside it and on `decision_log_entry` always.
2. `RuleSetValidator` with whole-set validation: product in `data_product`, table in the eight owned names, not `decision_log_entry`, not a `v_ace_*` view or a `public` table, months 1 to 600, age-basis field in `sys_fields` for that table, end action ARCHIVE or REVIEW.
3. `CaseHoldClient` and the two activities, with the fake answers of 12.8.
4. `RetentionSelector` with paging and the hold exclusion, and the boundary test that no other schema is named.
5. `ArchiveWriter` with the manifest write and `ManifestVerifier` with its read-back check.
6. `RetentionPurger` per table and rule, after the check, under the purge setting.
7. `recordRun`, the hold report and the MSG-P1-020 summary alert.
8. The two contract operations, the idempotency of a start and the `409` of an active run.
9. Tests for AC1 to AC9 and the access test.

**Feature flag.** `rwb.source-data.retention`, off until P5's JOB-17 is registered in the environment; a run started while the flag is off is refused with `503` and no archive is opened.

**Done when.** The tests in section 16 pass, SIT holds a completed run for 2026-12-06 with 1,250 rows archived under `retention/2026-12-06/interaction/`, the manifest verifies, the live table holds 4,800 rows, the held case is reported with its 40 rows, and the runbook entry of RWB-P1-E1017-OPS covers a failed run.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-020 | Retention run summary to Compliance (new, see additions) | {count} rows of {product} were archived under rule {rule} version {version}. {held} cases on legal hold were kept. |
| MSG-GEN-002 | `retention_months` outside 1 to 600 | {field} must be between {min} and {max}. |
| MSG-P1-002 | A retention rule set refused at a check | The {source} load for {date} was refused: {check}. The previous load is still in use. |
| MSG-GEN-006 | Archive container unavailable | {system} is not available. Your request is queued and will be retried. |
| MSG-P2-006 | A rerun while the run is active | {job} is already running. Wait for it to finish before you run it again. |
| MSG-P4-002 | A role without the right on the run surface | You cannot {action} here. Your role does not include it. |
| MSG-GEN-001 | A start whose body fails validation | The request is not valid: {detail}. |
| MSG-P7-003 | The decision record of the run cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

Thai text for each message follows decision DL10, which is open; its assumptions are ASM-2250, ASM-2357, ASM-2377 and ASM-2863. The texts are the legacy ones, unchanged, except MSG-P2-006, which carries the Error and Message Standard v4 wording; the run adds the check names of the rule-set validation ("decision_log_entry is not archived by the retention job", "v_ace_efs_action is ACE data; ACE applies its own retention", "interaction.occurred_at is not a column of the table") as the `{check}` value of MSG-P1-002.

### 15. Screens and states

No screen in this story. Compliance reads the run result, the counts and the hold report through `GET /retention-runs/{runId}` and the MSG-P1-020 summary alert, and the platform administrator reads the same run in the job monitor that another P1 story owns. Retention classes show on SCR-47 Personal data from Epic 8; until then they are loaded in rwb-document. States of SCR-47: loading as Screen Specifications v1 defines it; empty, error and no access: Not specified in the source documents (CG-ALL-2193). The gateway-bff composite route (DP-19) is not used by this story: the two operations are service-to-service and administration reads.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-017-01 | AC1, BR1, BR2, BR4 | End to end | 1,250 old and 4,800 recent synthetic interaction rows, rule version "RET-2026.11", run date 2026-12-06 |
| TC-E1-017-02 | AC2, BR7 | End to end | Version "RET-2027.01" at 36 months; rows from 2024-01-15 and 2023-12-20; run date 2027-01-03 |
| TC-E1-017-03 | AC3, BR3 | End to end | Case "RW-2024-000311" on legal hold with 40 old rows, answered by the contract fake |
| TC-E1-017-04 | AC4, BR6 | Component | A rule with 0 months; version "RET-2026.11" still in force |
| TC-E1-017-05 | AC5, BR4 | End to end | Container stub refusing writes; no row deleted; run Failed with MSG-GEN-006 |
| TC-E1-017-06 | AC6 | End to end | The run twice on 2026-12-06; 0 rows archived the second time; one archive set |
| TC-E1-017-07 | AC7 | Component | A row at exactly 24 months on 2026-12-06 |
| TC-E1-017-08 | AC8, BR5 | Component | A rule for `decision_log_entry`; refused in full |
| TC-E1-017-09 | AC9 | End to end | A second start during an active run; `409` with MSG-P2-006 |
| TC-E1-017-10 | Access | Component | RW-COMPLY posts a start and a rerun; refused with MSG-P4-002 |
| TC-E1-017-11 | Section 12 operations, events and activities | Contract | Contract fake of POST /retention-runs, RetentionRunWorkflow and the activities of 12.5 |
| TC-E1-017-12 | 12.7 tables, ASM-3438 | Component | One row per table of 12.7 at the age-basis boundary of the rule |
| TC-E1-017-13 | AC10 | End to end | Legal-hold contract fake answering after the 2 s budget; run date 2026-12-06 |
| TC-E1-017-14 | AC11 | Contract | Same Idempotency-Key posted with a body that differs from rule version "RET-2026.11" |
| TC-E1-017-15 | AC12, BR8 | Component | Rule for product "DP05" naming a table this story does not own; load refused in full |
| TC-E1-017-16 | AC13, BR8 | Component | Rule for product "DP05" with table "v_ace_efs_action"; load refused in full |
| TC-E1-017-17 | AC14 | Contract | No credential, a caller without the right to start a run, and an unknown runId; answers 401, 403 and 404 |
| TC-E1-017-18 | AC15 | Component | An archive activity of RetentionRunWorkflow that times out and is retried |
| TC-E1-017-19 | AC16 | End to end | Legal-hold contract fake returns an error; run date 2026-12-06 |

The legacy test case IDs, Covers and Data are kept in order and character for character; the legacy level "System" maps to "End to end" and "Access" to "Component", as in the other stories of this run. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. The four cases that assert the container and the legal hold run against the stubs of 12.8.

### 17. Guardrails

- No business value in code: the periods, the tables, the age-basis fields, the end action and the archive location are data in the request or properties of the service, never constants.
- No personal data in events, workflow inputs or logs: the run carries counts, table names, case numbers and hashes; the archived files are written to the container and never logged; test rows are synthetic.
- ACE data only through the owner's contract or `recovery.v_ace_*` views: this story reads neither, and a rule naming a `v_ace_*` view or a `public` table is refused.
- No cross-schema read and no cross-schema key: the eight tables are in `rwb_source_data`, the legal hold comes over the rwb-case interface, and `retention_rule` and `decision_log_entry` are never touched.
- No row is deleted before its archive copy is checked, and no row of a held case is deleted at all.
- The decision log keeps its own retention in rwb-decision; this run refuses a rule that names it (BR5).
- The write-once container is written forward only: a wrong archive is a new object at a new run date, never an edit.
- Rules are data, not code: a new version changes a period without a release of this service.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-RDF-013 | Retention and archive rule by record class | Business Requirements Epic 1, sections 3.1 and 4 | FEAT-RDF-17 | All recovery processes | R-UNI-20, R-UNI-38; CTL-08; DL26; BR-P1-017-2 | TC-E1-017-01, TC-E1-017-02, TC-E1-017-03, TC-E1-017-04, TC-E1-017-05, TC-E1-017-06, TC-E1-017-07, TC-E1-017-08, TC-E1-017-09, TC-E1-017-10, TC-E1-017-11, TC-E1-017-12, TC-E1-017-13, TC-E1-017-14, TC-E1-017-15, TC-E1-017-16, TC-E1-017-17, TC-E1-017-18, TC-E1-017-19 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-P1-E1017-CON | Contract | H build dependency: the two operations, the workflow contract, the schemas and the retention-run fake P5 calls |
| RWB-P1-E1017-OPS | DevOps | X external dependency: the deployment, the container mount, the alerts and the runbook of this action |
| RWB-P5-E1017-APP | App development | Sibling of the same legacy key: the rule, the action table and the Schedule JOB-17 that starts this run |
| RWB-P1-E1001-APP | App development | H build dependency: the eight tables, `data_product`, `sys_objects`, `sys_fields` and the append-only trigger |
| RWB-P1-E1064-APP | App development | H build dependency: the dictionary rows that prove an age-basis field |
| RWB-PLT-TE012-APP | App development | X external dependency: the write-once container and its credential |
| RWB-PLT-E1027-CON, RWB-PLT-E1043-CON, RWB-PLT-E1071-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON | Contract | H: the decision-record library, the reference-data library, the workflow kit, the per-service Flyway sequence and the composite route |
| RWB-P3-E1043-CON | Contract | C: the rwb-case contract this story is scheduled against and the fake of the legal-hold interface |

Decision DL26 is open; its assumptions are ASM-0247, ASM-0264, ASM-0275 and ASM-0355.

### 19. Out of scope

- `retention_rule`, `retention_action`, the retention load and its approval, and the monthly Schedule JOB-17: RWB-P5-E1017-APP (ASM-0076; Architecture v5 slides 16, 41 and 44).
- Retention classes for documents and the document legal hold (RWB-E1-041 in the legacy set, RWB-P5-E1017-APP in the target).
- The retention class for ledger entries as its own reference row (FEAT-ILG-10, RWB-E2-034).
- The decision log retention period (NFR-030, DL26) and its execution (RWB-P7-E1017-APP); the lake copy is retired with the data lake (DP-17).
- Closing a case after its retention period (REQ-S7-008, Epic 6).
- The personal data screen SCR-47 (Epic 8).
- The legal hold and the case number themselves: rwb-case owns them and answers `CaseHoldQuery`.
- The write-once container, its immutability policy and its credential: RWB-PLT-TE012-APP.
- The deployment, the KEDA scaling, the alerts and the runbook: RWB-P1-E1017-OPS.
- The cross-service proof of the rule, the hold and the archive across P1, P3, P5 and P7: RWB-ITG-E1017-ITG.
