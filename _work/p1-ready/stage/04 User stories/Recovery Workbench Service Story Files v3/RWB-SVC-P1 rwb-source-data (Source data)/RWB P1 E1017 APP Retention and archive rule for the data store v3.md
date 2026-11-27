# RWB-P1-E1017-APP Retention and archive rule for the data store

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

### Version 3 changes

- RD-P1-047 (with X-04) and RD-P1-001: `POST /retention-runs` and `GET /retention-runs/{runId}` as published in `rwb-source-data.yaml` 5.1.0, workflow ID `retention-run-{runDate}`, UUID `Idempotency-Key`, 409 MSG-P2-006 for a second run of a date (findings #1, #2, #7, #8, #15).
- RD-P1-048 (with RD-P1-024, X-01): seven tables, ARCHIVE for `interaction` and REVIEW for six, age from rwb-case `closedAt`, holds by exact key, periods Pending with Compliance (findings #3 to #6, #9 to #11, #17).
- RD-P1-002, RD-P1-004, RD-P1-045: the eight catalogue activities, the shared message codes and the flag-off answer (findings #13, #16, #18, #21 to #24).
- Criteria rewritten with concrete synthetic values and AC17 to AC24 added; findings #12, #14, #19 and #20 are closed in part and the rest is listed in section 20.
- Finishing pass (requests W3-messages-0042, W5-runtime-0070; test case backfill): every criterion cites its Test Cases v9 row.

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
| Size | Not specified; pending refinement (DOR-RWB-P1-E1017-APP-16) |
| Legacy key | RWB-E1-017 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Contract version | rwb-source-data.yaml 5.1.0 (API Specification v7) |
| Patterns applied | DP01, DP03, DP07, DP10, DP11, DP13, DP15, DP19 |
| Readiness decisions | RD-P1-001; RD-P1-002; RD-P1-004; RD-P1-005; RD-P1-024; RD-P1-045; RD-P1-047; RD-P1-048 |
| Parallel lane | L-P1-A |
| Ready to start | After RWB-P1-E1001-APP, RWB-P1-E1064-APP |
| Depends on (build) | RWB-P1-E1017-CON, RWB-PLT-E1027-CON, RWB-PLT-E1043-CON, RWB-PLT-E1071-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON, RWB-P1-E1001-APP, RWB-P1-E1064-APP, RWB-P1-E1069-DB |
| Contract dependencies | RWB-P3-E1021-CON (rwb-case.yaml 5.1.0); rwb-source-data.yaml 5.1.0 (API Specification v7) |
| Integration dependencies | None |
| External dependencies | RWB-PLT-TE012-APP |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v1.md (FR-P1-028) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-017 for rwb-source-data. The rule table `retention_rule` and the retention action are rwb-document's in the target (Ownership Map ruling ASM-0076; Architecture v5 slides 16, 41 and 44), so this story holds no rule table and registers no Schedule: it delivers the retention action on rwb-source-data's own tables, started by P5's JOB-17 through `POST /retention-runs`, archived to the write-once container of RWB-PLT-TE012-APP and held back by the rwb-case legal-hold interface. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P1-E1017-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (22 resolved, 25 cross-document, 2 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: applied RD-P1-001; RD-P1-002; RD-P1-004; RD-P1-005; RD-P1-024; RD-P1-045; RD-P1-047; RD-P1-048.

### 1. Story

As a **Compliance and PDPA officer (RW-COMPLY)**, I want **a retention rule per data product and table, held as reference data, applied by a job that archives rows past their rule and logs the action**, so that **the store holds what the policy allows and nothing older**.

The legacy story built the whole of it inside the recovery module: a `retention_rule` table beside the recovery tables, a Quartz trigger for JOB-17, the selection, the archive writer, the legal-hold exclusion and the delete. D-RCV-60 keeps the behaviour and moves the ownership:

- **rwb-document (P5)** owns `retention_rule` and `retention_action`, loads, validates and approves the version, and owns the monthly Schedule JOB-17 (retention, first Sunday) on task queue `rwb-document` (Ownership Map ruling ASM-0076; Architecture v5 slides 16, 41 and 44).
- **rwb-source-data (P1), this story,** receives P5 rules and validates the table/action pairing. It archives `interaction` only; it lists `party_ext`, `account_ext`, `contact_point_ext`, `valuation_ext`, `dp_treatment` and `dp_guarantee_claim` for REVIEW only. Periods remain Pending, owner Compliance, tracked as GAP-1029. No destruction from the archive is built before Compliance approval (RD-P1-048).
- **rwb-case (P3)** publishes held/open exclusions and closure dates. P1 reads `GET /api/recovery/case/v1/cases/retention-exclusions?page=&size=` and `GET /api/recovery/case/v1/cases/closure-dates?closedBefore=&page=&size=`; it never reads case tables (RD-P1-047).
- **RWB-PLT-TE012-APP** owns the write-once container; the P1 container name, role grant and archive path remain Pending, owner solution architect, tracked as GAP-0490.

The seven tables in scope are `interaction`, `party_ext`, `account_ext`, `contact_point_ext`, `valuation_ext`, `dp_treatment` and `dp_guarantee_claim`. `interaction` permits ARCHIVE; the other six permit REVIEW only. `case_list_row` is excluded because it is not created in P1 (RD-P1-024, X-01). `reconciliation_result`, `data_product_load`, `efs_ledger_outcome`, `lake_copy_watermark`, platform tables and reference data are excluded under RD-P1-048 item 3. `decision_log_entry` is P7's and `retention_rule` is P5's. The run uses `POST /retention-runs` and `GET /retention-runs/{runId}`.

### 2. Business rationale

PDPA and the bank retention schedule limit how long recovery data is kept. The retention periods are Pending, owner Compliance, tracked as GAP-1029. Until Compliance supplies the schedule and approves disposal, this run supports ARCHIVE and REVIEW only: it archives `interaction`; it lists six other P1 tables for review without archiving or deleting them.

The target changes where each half lives, not who owns the policy. P5 owns retention rules and JOB-17; P1 receives the run date, rule version and rules. The P1 period values stay Pending with Compliance (GAP-1029). P1 validates seven tables, archives `interaction`, and lists the six REVIEW-only tables.

Three things are deliberately different from the legacy monolith. The archive goes to the write-once container and not to a data lake, because Arch v5 removes the lake and its Power BI feed (DP-17; ADR-018). The legal hold comes over an interface with a fake, so the run is testable on Day 1 and no case row is read by SQL (DP-01, DP-11). And the interaction ledger stays P1's under the default ruling and DP-18, so the ledger that the case timeline reads is retained by the service that owns it.

### 3. Preconditions

- RWB-P1-E1001-APP provides the base schema, `interaction`, `data_product`, `sys_objects`, `sys_fields` and the append-only trigger. RWB-P1-E1069-DB provides the extension tables used for REVIEW. `case_list_row` is not created in P1 under RD-P1-024 (X-01).
- RWB-P1-E1064-APP provides dictionary rows for the in-scope P1 tables; P1 validates the age basis against `sys_fields` where a rule requires it.
- The per-service Flyway sequence of rwb-source-data exists. The migration changes only the live-row ARCHIVE guard; the archive is never destroyed by this run (RD-P1-048).
- RWB-P1-E1017-CON publishes the API Specification v7 fragment and retention-run fake; CON Done and fake publication remain Pending in that story.
- RWB-PLT-E1071-CON is available: the workflow kit, the namespace `rwb-recovery` and the task queue `rwb-source-data`, so `RetentionRunWorkflow` starts on Day 1 against the kit.
- RWB-P3-E1021-CON publishes the held/open exclusion and closure-date operations with their fakes (RD-P1-047).
- RWB-PLT-TE012-APP has delivered a write-once container in each environment that the rwb-source-data login may write, and the run's read-back check passes on it.
- Retention periods are Pending, owner Compliance, tracked as GAP-1029 (DL26). P1 does not set or hard-code a regulatory period. Rules arrive from rwb-document as request data. For the interim build, rule version RET-2026.11 carries these P1 rows as data, each marked "proposed (RRA v4), pending DL26": `interaction` (DP05), ARCHIVE after 12 months closed; `dp_treatment` and `dp_guarantee_claim` (DP04), REVIEW only (RD-P1-048 item 1; ASM-5706). The `case_list_row` row of that list is withdrawn (X-01).
- Properties `rwb.source-data.retention.archive-container` and `rwb.source-data.retention.batch-size=5000` are present as configuration, not as constants.
- The run contract is fixed by RD-P1-047: `POST /retention-runs` carrying the rules and `GET /retention-runs/{runId}` (closes GAP-0489; ASM-0681 confirmed). The split of the legacy criteria stays recorded under GAP-0488 (ASM-0680).
- Pending: the table that stores a retention run record (status, counts per table, archive location, hold report and the stored answer) before the job log of RWB-P1-AD018-APP exists (wave 4), owner data architect, tracked as GAP-3457. `recordRun` and the GET operation cannot be built until this is settled.

### 4. Flow

1. rwb-document owns and supplies the retention rule version and rule rows. P1 does not assert that a period or version is approved or in force while GAP-1029 is open.
2. rwb-document: its Schedule JOB-17 fires on the first Sunday of the month (02:30 Asia/Bangkok in the legacy cron) and starts the owners' retention actions; the run date is the business date of that Sunday, for example 2026-12-06 (Architecture v5 slide 44, JOB-17; DP-10).
3. P5 calls `POST /retention-runs` with UUID `Idempotency-Key` and body `{ruleVersion, runDate, rules[]}`; each rule has `productCode`, `tableName`, `recordClass`, `retentionMonths`, `ageBasis` and `endAction`. A valid start answers `202 {runId, status: ACCEPTED}`. The same key with the same body replays the stored status and body; a reused key with a different body answers `409 MSG-PLT-N009-05`. A new key for a run date whose run is RUNNING or COMPLETED answers `409 MSG-P2-006` with the stored `runId` in `detail`; a new key after FAILED starts a new execution (RD-P1-001; RD-P1-047; X-04).
4. rwb-source-data validates the product, table, `recordClass`, `retentionMonths`, `ageBasis` and `endAction` against its own metadata. Only `interaction` may use ARCHIVE; the six REVIEW tables may use REVIEW only. `case_list_row` is excluded (RD-P1-024, X-01). One refused rule refuses the full set with 422: `MSG-GEN-002` when `retentionMonths` is outside 1 to 600, `MSG-GEN-001` when a required value is missing, `MSG-GEN-007` when `productCode` or `endAction` is not in its list, and `MSG-P1-002` when a table, table and action pairing or `ageBasis` check fails; `field` names the failing input, for example `/rules/0/retentionMonths` (RD-P1-004). P1 trusts rwb-document for the approval and validity of the version and reads neither (BR7).
5. At run start, rwb-source-data reads the P3 held/open exclusions and closure dates through the two RD-P1-047 operations, one hop with a 2 s budget. It reads exclusions again before each delete unit. An unreadable answer fails the run before selection or deletion (RD-P1-047; RD-P1-048). Pending: how the catalogue activity retry (1 s initial interval, back-off 2, 10 attempts) applies to this 2 s read and the breaker threshold, owner solution architect, tracked as GAP-3453; start-to-close and heartbeat values stay under GAP-0143.
6. For `interaction`, P1 measures age from case `closedAt`; it selects only closed, unheld rows whose runDate minus the supplied retentionMonths is after closedAt. A row exactly at the boundary is kept. Date values compare as dates and timestamptz values compare in Asia/Bangkok. The case-exclusion answer is joined by case_id and person_key. Period values remain Pending with Compliance under GAP-1029 (RD-P1-048). A `party_ext` key (by `person_key`) or an `account_ext` key (by `account_key`) is listed only when no case in the exclusion set carries it and its last linked case closed longer ago than the period. `dp_treatment` and `dp_guarantee_claim` join holds by `case_id`. `contact_point_ext` and `valuation_ext` have no case or person join. Pending: the age condition under which `contact_point_ext`, `valuation_ext`, `dp_treatment` and `dp_guarantee_claim` rows are listed, owner data architect with Compliance, tracked as GAP-3454. Pending: month-end clamping of the month subtraction and the answer to a `runDate` later than today, owner solution architect with Compliance, tracked as GAP-3455.
7. P1 archives selected `interaction` rows and verifies the manifest before deleting the corresponding live rows. The archive object path and manifest encoding remain Pending, owner storage architect, tracked as GAP-0490. REVIEW rows are counted as LISTED; they are not archived or deleted (RD-P1-048).
8. P1 deletes only the live `interaction` rows whose archive copy and manifest have been verified, after re-reading P3 exclusions before each unit. No archive object is destroyed. A unit failure leaves prior committed units recorded and the run FAILED (RD-P1-048).
9. `GET /retention-runs/{runId}` returns status RUNNING, COMPLETED or FAILED; `countsPerTable[]` with `selected`, `archived`, `deleted`, `listed` and `held`; `archiveLocation`; and `holdReport`. Compliance periods remain Pending under GAP-1029 (RD-P1-047; RD-P1-048).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A case is on legal hold or open | Its rows are kept, counted as held and shown in the hold report | MSG-P1-020 | AC4 |
| X2 | A rule set is refused in full | 422; the run does not start and no row is selected | MSG-GEN-001, MSG-GEN-002, MSG-GEN-007 or MSG-P1-002 (section 4 step 4) | AC6, AC7, AC18, AC19 |
| X3 | The archive write or the manifest check fails | No row of the unit is deleted; the run ends FAILED; the alert is raised | MSG-GEN-006 | AC9, AC24 |
| X4 | A run is started again after a FAILED run of the same run date | A new execution selects only the rows still present | None | AC10 |
| X5 | A row is exactly at its retention age | The row is kept | None | AC2 |
| X6 | A rule names `decision_log_entry`, `retention_rule`, a `v_ace_*` view or a `public` table | 422; the rules are refused in full | MSG-P1-002 | AC19 |
| X7 | A new key starts a run date whose run is RUNNING or COMPLETED | 409; no second run and no second archive | MSG-P2-006 | AC8 |
| X8 | The rwb-case exclusion or closure-date answer cannot be read inside the 2 s budget | The run ends FAILED before the affected selection or delete, because a hold that is unknown is treated as a hold | None on the wire; the POST has already answered 202 | AC14 |
| X9 | `Idempotency-Key` is reused with a different body | 409 with the Problem response; the stored answer is unchanged | MSG-PLT-N009-05 | AC8 |
| X10 | `Idempotency-Key` is missing, blank or not a UUID | 400; the handler is not invoked | MSG-PLT-N009-03 | AC15 |
| X11 | A role without the right calls the surface | 403; no run; the refusal is logged | MSG-P4-002 | AC17 |
| X12 | The flag `rwb.source-data.retention` is off | Both operations answer 404; no run and no archive (RD-P1-045) | Pending, GAP-3452 | AC21 |

X1 to X7 carry the exception paths of RWB-E1-017 onto the split. X8 to X12 are the paths the contract adds.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the published P1 contract, the workflow kit, the reference-data contract and the legal-hold interface with their fakes on Day 1; needs the P1 baseline and the dictionary for its own tables; the WORM container is an external dependency |
| Negotiable | The rule rows, periods, tables and age-basis fields are data handed in by P5; the story fixes the validation, the archive layout, the manifest and the purge behaviour |
| Valuable | P1 archives interaction only and lists six REVIEW-only tables; retention periods remain Pending with Compliance (GAP-1029) |
| Estimable | One contract surface, one workflow, eight activities, one manifest writer, one purge-setting migration and one message |
| Small | Fits one sprint with its tests, as the action slice of the legacy key |
| Testable | Every criterion runs on synthetic rows with a test clock, a stubbed container and a stubbed legal-hold answer |

### 7. Acceptance criteria

```gherkin
Feature: Retention run for rwb-source-data

  Background:
    Given synthetic rows only, rule version "RET-2026.11" and runDate "2026-12-06"
    And the fixture rule R1: productCode "DP05", tableName "interaction", recordClass "CLASS-A" (a fixture value), retentionMonths 12 (proposed, pending DL26, GAP-1029), ageBasis "case.closedAt", endAction "ARCHIVE"
    And the rwb-case retention-exclusions and closure-dates fakes and the write-once container stub are available

  Scenario: AC1 Start and read an archive run
    Given 1,250 CLASS-A interaction rows of unheld cases closed on 2025-11-30 and 4,800 rows of unheld cases closed on 2026-06-30
    When rwb-document posts rule R1 to POST /retention-runs with a UUID Idempotency-Key
    Then the response is 202 with a runId and status ACCEPTED
    And GET /retention-runs/{runId} returns status COMPLETED, and for interaction selected 1250, archived 1250, deleted 1250, listed 0 and held 0
    And the manifest was verified before the 1,250 live rows were deleted and 4,800 rows remain
    And archiveLocation is not empty
    And MSG-P1-020 is raised with count 1250, product "DP05" and held 0
    TC: TC-P1-E1017-APP-09

  Scenario: AC2 Measure age from case closure
    Given one row whose case closed at 2025-12-06T00:00+07:00 and one row whose case closed at 2025-12-05T23:59:59.999+07:00
    When the run evaluates retentionMonths 12 against runDate 2026-12-06
    Then the row of the case closed at 2025-12-06T00:00+07:00 is kept
    And the row of the case closed at 2025-12-05T23:59:59.999+07:00 is selected
    And occurred_at plays no part in the age of either row
    TC: TC-P1-E1017-APP-10

  Scenario: AC3 REVIEW lists rows without archiving or deleting them
    Given a REVIEW rule for party_ext and 5 party_ext keys that no excluded case carries and whose last linked case closed on 2020-01-31
    And REVIEW rules for account_ext, contact_point_ext, valuation_ext, dp_treatment and dp_guarantee_claim
    When the run completes
    Then countsPerTable for party_ext shows listed 5, archived 0 and deleted 0, and the 5 keys are in the run's list for Compliance
    And for each of the other five tables archived is 0 and deleted is 0
    And the row count of all six tables is unchanged and no archive object holds their rows
    TC: TC-P1-E1017-APP-11

  Scenario: AC4 Exclude held and open cases
    Given the exclusions fake returns case "RW-2026-000102" with reason LEGAL_HOLD, which has 40 interaction rows, and an unheld case closed on 2025-11-30 has 10 rows
    When the run completes
    Then the 40 rows stay in interaction and the 10 rows are archived and deleted
    And countsPerTable for interaction shows held 40 and deleted 10
    And holdReport is present (its fields are Pending, GAP-3450)
    And MSG-P1-020 is raised with held 1
    TC: TC-P1-E1017-APP-12

  Scenario: AC5 Recheck exclusions before each delete unit
    Given 100 selected interaction rows, 40 of them of one case that the exclusions fake reports as held only from the second read
    When rwb-source-data reads exclusions again before the delete unit
    Then 60 rows are deleted and the 40 rows of the held case are not deleted
    And archive files already written for the 40 rows stay and the hold report lists them
    TC: TC-P1-E1017-APP-13

  Scenario: AC6 Enforce the seven-table scope
    Given a request with rule R1 and a second rule for tableName "case_list_row"
    When POST /retention-runs validates the request
    Then it answers 422 with MSG-P1-002 and names case_list_row
    And no run is created and no row is selected, archived or deleted
    TC: TC-P1-E1017-APP-14

  Scenario: AC7 Enforce table-specific end actions
    Given a rule with endAction ARCHIVE for party_ext, and separately a rule with endAction REVIEW for interaction
    When each is posted to POST /retention-runs
    Then each answers 422 with MSG-P1-002
    And no run is created and no row is selected or changed
    TC: TC-P1-E1017-APP-15

  Scenario: AC8 Apply the retention-run conflict and replay rules
    Given an accepted run for runDate 2026-12-06 started with key K1
    When K1 is posted again with the same body
    Then the stored 202 and runId are returned and no second workflow or archive object exists
    When K1 is posted with a different body
    Then it answers 409 with MSG-PLT-N009-05
    When a new key K2 is posted while that run is RUNNING, and again after it is COMPLETED
    Then each answers 409 with MSG-P2-006 and the stored runId in detail
    When the run has instead ended FAILED and a new key K3 is posted
    Then it answers 202 and a new execution of workflow ID "retention-run-2026-12-06" starts
    TC: TC-P1-E1017-APP-16

  Scenario: AC9 Do not delete live interaction rows before archive verification
    Given the container stub returns a manifest whose count or hash differs, and separately a container that refuses writes
    When the run processes the unit
    Then no row of the unit is deleted and GET answers status FAILED
    And the alert MSG-GEN-006 is raised for the archive container
    TC: TC-P1-E1017-APP-17

  Scenario: AC10 Preserve completed units after a later failure
    Given 6,000 selected interaction rows, rwb.source-data.retention.batch-size 5000, and a container stub that refuses the second unit
    When the run ends
    Then 5,000 rows stay deleted with their verified manifest, 1,000 rows stay live and the run is FAILED with them recorded
    When a new key is posted for the same body after the container recovers
    Then only the 1,000 remaining rows are archived and deleted and no existing archive object is overwritten
    TC: TC-P1-E1017-APP-21

  Scenario: AC11 Do not hard-code a retention period
    Given the repository and the default configuration of a release
    When they are inspected and a rule without retentionMonths is posted
    Then no retention month value is present in code or default configuration
    And the post answers 422 with MSG-GEN-001 and field "/rules/0/retentionMonths"
    TC: TC-P1-E1017-APP-22

  Scenario: AC12 Keep archive objects until Compliance approves disposal
    Given an archive run completed and its objects in the container stub
    When any later run, rerun or configuration change executes
    Then no archive object is removed or rewritten
    And no operation, activity or setting of this service destroys one
    TC: TC-P1-E1017-APP-23

  Scenario: AC13 Return the ruled retention-run status and counts
    Given one run RUNNING, one COMPLETED and one FAILED
    When GET /retention-runs/{runId} is called for each
    Then status is RUNNING, COMPLETED and FAILED respectively
    And each countsPerTable item carries tableName, selected, archived, deleted, listed and held
    And each response carries archiveLocation and holdReport
    TC: TC-P1-E1017-APP-24

  Scenario: AC14 Fail before selection when rwb-case cannot be read
    Given the retention-exclusions or closure-dates fake does not answer within 2 seconds, and separately answers 500 and 401
    When rwb-source-data starts the run
    Then the run is FAILED with selected 0, archived 0 and deleted 0
    And no archive object is written
    TC: TC-P1-E1017-APP-25

  Scenario: AC15 Reject malformed or refused requests
    Given a request without an Idempotency-Key, one with a key that is not a UUID, and a well-formed body without runDate
    When each is posted to POST /retention-runs
    Then the first two answer 400 with MSG-PLT-N009-03
    And the third answers 422 with MSG-GEN-001 and field "/runDate"
    And no run is created and no row changes
    TC: TC-P1-E1017-APP-26

  Scenario: AC16 Apply recordClass and preserve correction chains
    Given rule R1 only, entry A of CLASS-A corrected by entry B of CLASS-B, and entries C and D of CLASS-A where D corrects C, all of one case closed on 2025-11-30
    When the run completes
    Then C and D are archived and deleted in one unit
    And A and B stay, because the correction of A is not past a supplied rule
    And a gap left in case_seq of the closed case is not reported as an error and no idempotency_key value is reused
    TC: TC-P1-E1017-APP-27

  Scenario: AC17 Access to the retention surface
    Given an RW-COMPLY user, a call with no valid token and an unknown runId
    When the RW-COMPLY user posts a run
    Then it answers 403 with MSG-P4-002, no run exists and the refusal is logged
    And the same user reads an existing run with 200
    And the call with no valid token answers 401 with MSG-P4-001
    And GET of the unknown runId answers 404 with MSG-P4-003
    TC: TC-P1-E1017-APP-01

  Scenario: AC18 Months boundaries
    Given rules that differ only in retentionMonths
    When retentionMonths is 1 and 600
    Then each request is accepted with 202
    When retentionMonths is 0 and 601
    Then each answers 422 with MSG-GEN-002 and field "/rules/0/retentionMonths", and no run is created
    TC: TC-P1-E1017-APP-02

  Scenario: AC19 Refused rule values
    Given in separate requests a rule for decision_log_entry, for retention_rule, for v_ace_efs_action, an ageBasis "occurred_at" for interaction, an endAction "DELETE" and an empty rules list
    When each is posted
    Then the first four answer 422 with MSG-P1-002, the fifth 422 with MSG-GEN-007 and the sixth 422 with MSG-GEN-001
    And no run is created and no row is read from a rule's table
    TC: TC-P1-E1017-APP-03

  Scenario: AC20 Hold current-state rows by their exact key
    Given a held case whose accountKeys hold "ACC-FX-1" and personKeys hold "PER-FX-1", with account_ext and party_ext rows for those keys older than the period
    When the REVIEW rules run
    Then neither key is listed and both rows are unchanged
    TC: TC-P1-E1017-APP-04

  Scenario: AC21 Flag off
    Given the flag rwb.source-data.retention is off
    When POST /retention-runs and GET /retention-runs/{runId} are called
    Then each answers 404, no workflow starts and no archive object is written
    TC: TC-P1-E1017-APP-05

  Scenario: AC22 The delete guard
    Given a database session without the setting rwb.retention.purge
    When DELETE and UPDATE are issued on interaction
    Then both are refused
    When the purge transaction sets rwb.retention.purge
    Then DELETE of verified rows succeeds and UPDATE is still refused
    And DELETE on decision_log_entry is refused in every case
    TC: TC-P1-E1017-APP-06

  Scenario: AC23 No personal data in logs or workflow history
    Given a run over interaction rows that hold summary text and contact references
    When the run completes
    Then no log line, metric, alert or workflow input, result or history entry holds a summary, a contact value or a name
    And activities pass page references, not row content
    TC: TC-P1-E1017-APP-07

  Scenario: AC24 An archive activity times out and is retried
    Given archiveTable times out once before its answer
    When the catalogue retry runs the activity again
    Then the same unit is repeated and no row is deleted before verifyManifest succeeds
    And when all 10 attempts fail the run is FAILED with deleted 0
    TC: TC-P1-E1017-APP-08
```

**Target reading.** P5 owns the rule set and starts the P1 action through `POST /retention-runs`; P1 returns the run through `GET /retention-runs/{runId}`. Retention periods remain Pending, owner Compliance, tracked as GAP-1029. RD-P1-048 permits ARCHIVE for `interaction` and REVIEW for the six extension and treatment tables; REVIEW counts rows as LISTED and does not archive or delete them. `case_list_row` is excluded under RD-P1-024 (X-01). P3 supplies held/open case exclusions and closure dates through RD-P1-047. The ARCHIVE object path and manifest schema remain Pending under GAP-0490. Pending: the decision record of a run and of a refused rule set, including what a failed record write does to a delete unit (MSG-P7-003), owner solution architect, GAP-2426; no criterion asserts it until it is ruled. AC1 to AC16 keep the IDs that Test Cases v9 maps; AC17 to AC24 need new rows.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Retention periods are Pending, owner Compliance, tracked as GAP-1029; P5 owns the rule rows and approval | RD-P1-048; DL26 |
| BR2 | ARCHIVE applies to `interaction` only; archive verification precedes deletion from the live table. REVIEW selects and counts as LISTED, with no archive or delete | RD-P1-048 |
| BR3 | Held and open cases are excluded using the P3 retention-exclusions answer; re-read exclusions before each delete unit | RD-P1-047; RD-P1-048 |
| BR4 | A live interaction row is deleted only after its archive copy is written and checked; archive objects are not destroyed by this run | RD-P1-048; NFR-074 |
| BR5 | The decision log is not archived by this run; its retention is set by Compliance and executed in rwb-decision | NFR-030; ADR-009; DL26 |
| BR6 | A refused rule makes the whole set fail before selection | RD-P1-047 |
| BR7 | P1 accepts rules from P5 and does not assert approval or valid-from status | RD-P1-047 |
| BR8 | P1 accepts only the seven ruled tables and table-specific actions; case_list_row is excluded as not created in P1 | RD-P1-024; RD-P1-048 |
| BR9 | `retentionMonths` is a whole number from 1 to 600 | RWB-E1-017 AC4; MSG-GEN-002 |

**Where each rule lives in the target.** P5 owns the retention rows, periods and approval. P1 receives rules in the request. ARCHIVE applies only to `interaction`; the other six in-scope tables are REVIEW only and their rows are counted as LISTED without archive or delete. P3 owns held/open exclusions and closure dates. P1 re-reads exclusions before each delete unit, deletes live interaction rows only after archive verification, and does not destroy archive objects. The periods remain Pending, owner Compliance, tracked as GAP-1029. `contact_point_ext` and `valuation_ext` have no case/person join key in Physical Schema v8 and stay REVIEW only; their join key is Pending, owner data architect, tracked as GAP-3279. `case_list_row` is not created in P1 (RD-P1-024, X-01).

### 9. State transitions

This story does not change a case status. Run states are RUNNING, COMPLETED and FAILED. Periods remain Pending with Compliance under GAP-1029.

| From | Event | Condition | To |
|---|---|---|---|
| no run for the run date | `POST /retention-runs` accepted | Rules validate and no run of the date is active or completed | RUNNING |
| RUNNING | Archive verified and interaction live rows deleted; REVIEW rows listed | Every unit completes | COMPLETED |
| RUNNING | A unit fails | Archive verification, exclusion read or delete fails | FAILED |
| FAILED | `POST /retention-runs` with a new UUID key | The prior execution is FAILED | RUNNING |
| RUNNING | A second start for the same runDate | A run is active | Unchanged; 409 MSG-P2-006 |
| any run | The next rule version | P5 supplies another ruleVersion | Period values remain Pending until Compliance supplies the schedule (GAP-1029) |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-COMPLY, Compliance and PDPA officer | Owns the retention periods; reads the run result and the hold report through `GET /retention-runs/{runId}` and the summary alert (Platform administration R) |
| RW-REFADM, reference data administrator | Submits the retention load to rwb-document (Reference data C); this service receives the rules in the run request |
| Holder of Reference data A | Approves the retention load in rwb-document |
| RW-DATASTEW, data steward | Reads the run result for their products |
| RW-PLATADM, platform administrator | Starts a rerun of the retention action and reads the run (Platform administration U) |
| SY-DATALOAD, data load | Is the service identity that runs the action, writes the archive and deletes the archived rows |
| SY-CASEWF, case workflow module | Supplies P3 held/open exclusions and closure dates through RWB-P3-E1021-CON |

P5 owns approval of the rule set. P1 authorizes POST and GET through rwb-access; the exact operation right remains Pending, owner security architect, tracked as GAP-2429. P1 does not make a compliance period decision.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-002 | P3 retention-exclusions response | caseId, caseNumber, reason, closedAt, accountKeys, personKeys | Read through RWB-P3-E1021-CON (RD-P1-047) |
| DF-CAS-020 | P3 retention-exclusions response | held/open case facts | Read through RWB-P3-E1021-CON (RD-P1-047) |
| DF-INT-001 to DF-INT-028 | `interaction` | all columns | Read, archive; delete live rows only after manifest verification |
| DF-REF-116 to DF-REF-126 | `retention_rule` (P5's table) | rule values | Supplied in request; P1 does not read the table |
| DF-RPT-001 onwards | `case_list_row` | all columns | Excluded: not created in P1 (RD-P1-024, X-01) |
| Dictionary of RWB-P1-E1064-APP | `data_product`, `sys_objects`, `sys_fields` | product code, table and column names | Read, to validate a rule |
| Pending, GAP-3457 | retention run record | runId, status, counts per table, archiveLocation, holdReport | Write and read |
| DF-OPS-118 onwards | `reconciliation_result` | all columns | Excluded under RD-P1-048 item 3 |
| DF-OPS-001 onwards | `data_product_load` | all columns | Excluded under RD-P1-048 item 3 |
| DF-EXT-001 to DF-EXT-012 | `party_ext` | all 12 fields | REVIEW only; joins by person_key |
| DF-EXT-013 to DF-EXT-026 | `contact_point_ext` | all 14 fields | REVIEW only; no exact join key, Pending GAP-3279 |
| DF-EXT-027 to DF-EXT-035 | `account_ext` | all 9 fields | REVIEW only; joins by account_key |
| DF-EXT-036 to DF-EXT-049 | `valuation_ext` | all 14 fields | REVIEW only; no exact join key, Pending GAP-3279 |
| RWB-P1-E1064-APP | `dp_treatment`, `dp_guarantee_claim` | all columns per P1 dictionary (RWB-P1-E1064-APP) | REVIEW only; no archive or delete |

The interaction fields are archived as a row and deleted from the live table only after manifest verification. The six REVIEW-only tables are listed without archive or delete. Dictionary field identifiers remain as published by RWB-P1-E1064-APP.

**Which side is this story's.** P1 archives `interaction` only. P1 lists `party_ext`, `account_ext`, `contact_point_ext`, `valuation_ext`, `dp_treatment` and `dp_guarantee_claim` for REVIEW only. `contact_point_ext` and `valuation_ext` stay REVIEW only while their join key is Pending under GAP-3279. `case_list_row` is excluded because P1 does not create it (RD-P1-024, X-01). `reconciliation_result`, `data_product_load` and operational/reference/platform tables are excluded under RD-P1-048. P1 neither reads nor writes P5's `retention_rule` table or P7's `decision_log_entry`. The retention periods remain Pending, owner Compliance, GAP-1029.

### 12. Contract

#### 12.1 REST operations provided

Two operations on base `/api/recovery/source-data/v1` (DP-13). The first is the start that P5's JOB-17 calls; the second is the run record that Compliance and P5 read.

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| POST | `/retention-runs` | Start one retention run for a run date and a rule version: validates the rules against this service's own tables, archives the selected rows, checks the manifest and deletes them per table and rule | Platform administration U, or the rwb-document service identity with the same right | `Idempotency-Key` required; the stored answer is returned for a replay with the same body, `422` for a different body |
| GET | `/retention-runs/{runId}` | Status, `countsPerTable[]`, archiveLocation and holdReport | Platform administration R or authorized Compliance role | Read only |

Request body: `{ruleVersion, runDate, rules[]}`; each rule has `productCode`, `tableName`, `recordClass`, `retentionMonths`, `ageBasis` and `endAction`. `Idempotency-Key` is a UUID. A start answers `202 {runId, status: ACCEPTED}`. A date already RUNNING or COMPLETED answers `409 MSG-P2-006`; a key reused with another body answers `409 MSG-PLT-N009-05`; a refused rule set answers 422 with the codes of section 4 step 4; a missing or non-UUID key answers `400 MSG-PLT-N009-03`; no valid token `401 MSG-P4-001`; a role without the right `403 MSG-P4-002`; an unknown `runId` `404 MSG-P4-003`; an unavailable dependency before the 202 `503`. GET answers RUNNING, COMPLETED or FAILED and `countsPerTable[] {tableName, selected, archived, deleted, listed, held}`, `archiveLocation` and `holdReport` (RD-P1-001; RD-P1-047; RD-P1-048).

The response fields are fixed by RD-P1-047. Pending: the fields of `holdReport`, owner solution architect, tracked as GAP-3450. P1 contract version is `rwb-source-data.yaml` 5.1.0 (API Specification v7). Problem details use the published P1 Problem schema; unresolved archive object path and manifest layout remain Pending under GAP-0490.

#### 12.2 REST operations consumed

| Interface | Operation | Owner | Use | Pattern |
|---|---|---|---|---|
| rwb-case retention-exclusions | `GET /api/recovery/case/v1/cases/retention-exclusions?page=&size=` | P3 rwb-case | Held/open case IDs, accountKeys and personKeys; page size up to 1,000 and cursor | RD-P1-047; 2 s one-hop budget |
| rwb-case closure-dates | `GET /api/recovery/case/v1/cases/closure-dates?closedBefore=&page=&size=` | P3 rwb-case | closedAt and account/person keys for closed unheld cases | RD-P1-047; 2 s one-hop budget |

Both reads are published in `rwb-case.yaml` 5.1.0: paged with `page`, `size` (1 to 1,000) and `cursor`; `closure-dates` requires `closedBefore` (date-time); an exclusion item holds `caseId`, `caseNumber`, `reason` (LEGAL_HOLD or OPEN), `closedAt`, `accountKeys`, `personKeys`. P1 reads every page. P1 reads held/open exclusions at run start and again before each interaction delete unit. It reads closure dates for the interaction age basis. An exclusion answer unreadable within 2 seconds fails the run before selection or deletion. P1 does not read rwb_case tables (RD-P1-047; RD-P1-048).

#### 12.3 Events published

None. The topic of the service is `rwb.source-data.events.v1` with event names `rwb.source-data.<Event>.v1` (DP-14), and its two events `AceDataReady` and `AceDataLate` belong to RWB-P1-E1013-APP (Architecture v5 slides 15 and 43). A retention run is started and read over REST. The decision-record mapping under DP-03 is separate and remains Pending under GAP-2426; this story does not define its event payload or outbox behavior.

#### 12.4 Events consumed

None. Architecture v5 slide 15 gives rwb-source-data no consumed event ("none: Airflow call; fallback polls ACE batch record"), and the retention run is started by the P5 Schedule and its contract call, not by an event.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `RetentionRunWorkflow` | Workflow, one run per runDate, workflow ID `retention-run-{runDate}`, conflict policy FAIL and reuse policy ALLOW_DUPLICATE_FAILED_ONLY | `rwb-source-data` in namespace `rwb-recovery` | Input `{ruleVersion, runDate, rules[]}`; output status, countsPerTable, archiveLocation and holdReport (RD-P1-047; RD-P1-001) |
| `validateRules` | Activity | `rwb-source-data` | Rules in; a refused rule set or the accepted set out; one transaction, no row read |
| `casesOnLegalHold` | Activity | `rwb-source-data` | Reads P3 held/open exclusions and closure dates, at start and before each delete unit; 2 s per call |
| `caseNumbers` | Activity | `rwb-source-data` | Reads the case numbers of the held cases for the hold report |
| `selectRows(page)` | Activity | `rwb-source-data` | Interaction only for ARCHIVE; age from case.closedAt, join hold exclusions by case_id/person_key, page size 5000 |
| `archiveTable` | Activity | `rwb-source-data` | Interaction page in; archive copy and manifest out; object path/layout Pending GAP-0490 |
| `verifyManifest` | Activity | `rwb-source-data` | Manifest location in; a count and hash comparison out; a mismatch fails the unit |
| `deleteArchivedRows` | Activity | `rwb-source-data` | Deletes only verified live interaction rows after exclusion re-read; no archive destruction |
| `recordRun` | Activity | `rwb-source-data` | Writes status, countsPerTable, archiveLocation and holdReport to run record |

The eight activities are those of the Temporal Workflow and Activity Catalog, each retried with 1 s initial interval, back-off 2 and 10 attempts; start-to-close and heartbeat values are Pending under GAP-0143. Inputs and results carry page references and counts, never row content. The workflow is started by the REST contract call, not by a Schedule. It uses ID `retention-run-{runDate}`, conflict policy FAIL and reuse policy ALLOW_DUPLICATE_FAILED_ONLY. A failed run may be started again with a new UUID key; a RUNNING or COMPLETED run for that date answers 409 MSG-P2-006 (RD-P1-047; RD-P1-001).

#### 12.6 Schedules

None. JOB-17 (retention, monthly, first Sunday) is the Schedule of rwb-document on task queue `rwb-document` (Architecture v5 slides 16 and 44; ASM-0076), and this service registers no Schedule of its own.

#### 12.7 Tables owned

| Table | Schema | Owner | This story |
|---|---|---|---|
| `interaction` | `rwb_source_data` | P1 | ARCHIVE; delete live rows only after manifest verification and exclusion re-read |
| `case_list_row` | Not created in P1 | P1 | Excluded by RD-P1-024 (X-01) |
| `reconciliation_result` | `rwb_source_data` | P1 | Excluded under RD-P1-048 item 3 |
| `data_product_load` | `rwb_source_data` | P1 | Excluded under RD-P1-048 item 3 |
| `party_ext`, `account_ext`, `contact_point_ext`, `valuation_ext`, `dp_treatment`, `dp_guarantee_claim` | `rwb_source_data` | P1 | REVIEW only; count as LISTED; no archive or delete. `contact_point_ext` and `valuation_ext` join key Pending GAP-3279 |
| `data_product`, `sys_objects`, `sys_fields` | `rwb_source_data` | P1 | Read only, to validate a rule set; no row is written |
| `retention_rule`, `retention_action` | `rwb_document` | P5 | **Not read and not written here**; the rules arrive in the request |
| `decision_log_entry` | `rwb_decision` | P7 | **Never named by a rule and never touched here** |

No table of another service is read (DP-01). P1 deletes live `interaction` rows only after archive verification; REVIEW-only tables are not archived or deleted. `case_list_row` is not created under RD-P1-024. No archive object is destroyed by this run.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-case retention-exclusions and closure-dates fakes (RWB-P3-E1021-CON) | `retention-exclusions`, `closure-dates` | No case excluded; held and open cases with account/person keys; timeout and 5xx |
| Write-once container stub (RWB-PLT-TE012-APP) | The archive and its manifest | A writable container, a container refusing writes, a manifest whose count or hash differs |
| Clock control | Run date and closure boundary | Synthetic closedAt and runDate values; the regulatory period remains Pending under GAP-1029 |
| rwb-source-data retention-run WireMock (published by RWB-P1-E1017-CON, for P5) | `POST /retention-runs`, `GET /retention-runs/{runId}` | A `202` with a `runId`, a `409` for an active run, a `422` for refused rules, a timeout, a 5xx, a completed run with counts |

The last fake is the one P5's JOB-17 tests call, so rwb-document can prove its Schedule and its start on Day 1 without this service being built.

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 2 operations on `/api/recovery/source-data/v1` | 2 P3 retention reads | OpenAPI 3.1, one hop, 2 s budget and breaker (DP-11) |
| Kafka | None | None | The topic `rwb.source-data.events.v1` and its two events belong to RWB-P1-E1013-APP |
| Temporal | 1 workflow, 8 activities (section 12.5) | None | Task queue `rwb-source-data` in namespace `rwb-recovery`; no Schedule in this service |
| File | One archive path for `interaction`; object path and manifest layout Pending, owner storage architect, GAP-0490 | The manifest read back for the check | Write-once container of RWB-PLT-TE012-APP |
| SQL | None | None | No view and no other schema is read; the hold comes over the interface |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.sourcedata`, modules `retention`, `archive` and `hold`, with the published types in `...sourcedata.api`. Service base `/api/recovery/source-data/v1`, schema `rwb_source_data`, task queue `rwb-source-data` in namespace `rwb-recovery`, topic `rwb.source-data.events.v1` (not published here).

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Decision-record payload, key, transaction timing and failure behavior Pending, owner solution architect, GAP-2426 | H RWB-PLT-E1027-CON |
| DP-07 | Reference data, LOV | rwb-source-data reference-data contract | H RWB-PLT-E1043-CON; C RWB-P3-E1021-CON for held/open exclusions and closure dates |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-10 is used, not owned: the Schedule is P5's and this story supplies the workflow that the Schedule starts. DP-03 decision-record payload, key, transaction timing and failure behavior remain Pending, owner solution architect, tracked as GAP-2426. DP-19 applies to the platform administration surface that reads a run and to the Compliance summary, neither of which this story builds.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `RetentionRunWorkflow` | Workflow | Run per date; validates, selects, archives `interaction`, verifies, deletes live rows and records status/counts; six REVIEW tables are listed only |
| `RuleSetValidator` | Service | Validates a rule set against `data_product`, `sys_objects`, `sys_fields`, the seven ruled tables, table/action pairing and the 1 to 600 month range; period values remain request data and Pending with Compliance under GAP-1029 |
| `RetentionSelector` | Repository | Reads interaction rows past the case `closedAt` boundary; filters `retention_class = recordClass`; applies P3 exclusions by case_id/person_key; preserves correction chains as one unit |
| `ArchiveWriter` | Service | Writes selected interaction rows and a manifest to the approved write-once target; object path and manifest format Pending under GAP-0490 |
| `ManifestVerifier` | Service | Reads the manifest and the files back and compares count and hashes before any delete |
| `RetentionPurger` | Repository | Deletes the archived rows in one transaction per table and rule, under `rwb.retention.purge` |
| `RetentionExclusionsClient` | Client | Reads P3 retention-exclusions and closure-dates, re-reads exclusions before each delete unit |
| `RetentionRunController` | Controller | The two operations on `/api/recovery/source-data/v1`; RFC 9457 problem details |
| `V<n>__rwb_e1_017_retention_purge.sql` | Migration | Replaces `refuse_change()` so that DELETE is allowed only inside the purge setting; UPDATE stays refused and `decision_log_entry` keeps its unconditional refusal |

**Database.** This story creates no table. It adds only the live `interaction` archive-delete guard migration. The seven in-scope tables are from RWB-P1-E1001-APP and RWB-P1-E1069-DB; dictionary rows are from RWB-P1-E1064-APP. `case_list_row` is not created in P1. REVIEW-only tables are not deleted. No archive object is destroyed.

**Configuration and reference data**

- `rwb.source-data.retention.batch-size=5000` bounds a page and a file set.
- `rwb.source-data.retention.archive-container` is an environment reference; its target container, authorized prefix and object path remain Pending, owner solution architect, under GAP-0490.
- `rwb.retention.purge` is the transaction setting the trigger requires for a DELETE; it is set by `RetentionPurger` inside its own transaction and by nothing else.
- The rule version, the run date and the rules come in the request; the service holds no rule row and no default period (ASM-0076).
- The P3 calls use a one-hop 2 s budget (RD-P1-047). Retry count and breaker thresholds are not specified here.

**Build steps**

1. The migration that replaces `refuse_change()` with the purge-setting rule, and a test that UPDATE and DELETE are still refused outside it and on `decision_log_entry` always.
2. `RuleSetValidator` validates the whole request against data_product, sys_objects and sys_fields; the seven ruled tables; and ARCHIVE/REVIEW pairing. It filters interaction by `retention_class = recordClass`; correction chains are handled as one unit under RD-P1-048 item 6.
3. `RetentionExclusionsClient` and the `casesOnLegalHold` and `caseNumbers` activities, with the fake answers of 12.8.
4. `RetentionSelector` with paging and the hold exclusion, and the boundary test that no other schema is named.
5. `ArchiveWriter` with the manifest write and `ManifestVerifier` with its read-back check.
6. `RetentionPurger` per table and rule, after the check, under the purge setting.
7. `recordRun`, the hold report and the MSG-P1-020 summary alert.
8. The two contract operations, the idempotency of a start and the `409` of an active run.
9. Tests for AC1 to AC24.

**Feature flag.** `rwb.source-data.retention`. While it is off both operations answer 404 and nothing starts (RD-P1-045 item 4). Pending: the message code of that answer and the order in which the flag is switched on relative to the registration of JOB-17, owner platform architect, tracked as GAP-3452.

**Done when.** AC1 to AC24 pass, covering acceptance, refusal, status/counts, ARCHIVE verification, REVIEW listing, hold exclusions and the re-read before deletion; the workflow records RUNNING, COMPLETED or FAILED. Test data in DEV and delivery sign-offs remain Pending in section 20.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-020 | Retention run summary to Compliance (new, see additions) | {count} rows of {product} were archived under rule {rule} version {version}. {held} cases on legal hold were kept. |
| MSG-GEN-002 | `retentionMonths` outside 1 to 600 (422) | {field} must be between {min} and {max}. |
| MSG-P1-002 | A retention rule set refused at a check | The {source} load for {date} was refused: {check}. The previous load is still in use. |
| MSG-GEN-006 | Archive container or rwb-case unavailable; run unit fails | {system} is not available. Try again in a few minutes. |
| MSG-P2-006 | A new key for a run date that is RUNNING or COMPLETED (409) | A retention run for {date} is already running or complete. It was not run again. |
| MSG-P4-002 | A role without the right on the run surface | You cannot {action} here. Your role does not include it. |
| MSG-GEN-001 | A required value is missing (422) | Enter {field}. |
| MSG-GEN-007 | `productCode` or `endAction` not in its list (422) | {value} is not a valid value for {field}. Choose a value from the list. |
| MSG-P4-001 | No valid token (401) | Your session is not valid or you have no Recovery Workbench role. Sign in again or ask your team manager to request one. |
| MSG-P4-003 | Unknown `runId` (404) | This case is not in your scope. |
| MSG-PLT-N009-05 | Key reused with another request or in flight (409) | The Idempotency-Key conflicts with another request to {operation}. |
| MSG-PLT-N009-03 | Idempotency-Key is missing, blank or not a UUID (400) | The Idempotency-Key header is required and must be valid for {operation}. |
| MSG-P7-003 | DP-03 decision record: payload, key, transaction timing and effect on the delete unit | Pending, owner solution architect, GAP-2426. |

Texts are those of Error and Message Standard v6. Thai text follows decision DL10, which is open; its assumptions are ASM-2250, ASM-2357, ASM-2377 and ASM-2863. Pending: the refused-check names of MSG-P1-002, and the channel, recipients and one-per-product or one-per-run rule of MSG-P1-020, owner product owner, tracked as GAP-3451.

### 15. Screens and states

No screen in this story. Compliance reads the run result, the counts and the hold report through `GET /retention-runs/{runId}` and the MSG-P1-020 summary alert, and the platform administrator reads the same run in the job monitor that another P1 story owns. Retention classes show on SCR-47 Personal data from Epic 8; until then they are loaded in rwb-document. States of SCR-47: loading as Screen Specifications v1 defines it; empty, error and no access: Not specified in the source documents (CG-ALL-2193). The gateway-bff composite route (DP-19) is not used by this story: the two operations are service-to-service and administration reads.

### 16. Test cases

- Test Cases v9 maps TC-P1-E1017-APP-09 to TC-P1-E1017-APP-17 to AC1 to AC9 and TC-P1-E1017-APP-21 to TC-P1-E1017-APP-27 to AC10 to AC16, with the values of section 7.
- TC-P1-E1017-APP-18 (access), TC-P1-E1017-APP-19 (section 12 surface) and TC-P1-E1017-APP-20 (section 12.7 tables) stay.
- TC-P1-E1017-APP-01 to -08 cover AC17 to AC24.

### 17. Guardrails

- No business value in code: the periods, the tables, the age-basis fields, the end action and the archive location are data in the request or properties of the service, never constants.
- No personal data in logs, dashboard series, alert payloads or workflow inputs, results and history. The archive holds Confidential personal data: its encryption and read roles are Pending, owner security architect, tracked as GAP-3456. The archive object path and manifest format remain Pending under GAP-0490; test rows are synthetic.
- ACE data only through the owner's contract or `recovery.v_ace_*` views: this story reads neither, and a rule naming a `v_ace_*` view or a `public` table is refused.
- No cross-schema read or key: P1 reads the seven in-scope tables in `rwb_source_data` and P3 retention answers through its contract. P5 `retention_rule` and P7 `decision_log_entry` are not touched.
- No row is deleted before its archive copy is checked, and no row of a held case is deleted at all.
- The decision log keeps its own retention in rwb-decision; this run refuses a rule that names it (BR5).
- The write-once container is written forward only: a wrong archive is a new object at a new run date, never an edit.
- Rules are data, not code: a new version changes a period without a release of this service.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-RDF-013 | Retention and archive rule by record class | Business Requirements Epic 1, sections 3.1 and 4 | FEAT-RDF-17 | All recovery processes | R-UNI-20; CTL-08; DL26 | TC-P1-E1017-APP-09 to TC-P1-E1017-APP-17, TC-P1-E1017-APP-21 to TC-P1-E1017-APP-27, TC-P1-E1017-APP-01 to TC-P1-E1017-APP-08 |
| RD-P1-047 / RD-P1-048 | P1 retention interface, P3 exclusions, ARCHIVE/REVIEW behavior | P1 run and P3 contract | Retention-run request and status/counts | - | - | TC-P1-E1017-APP-09, TC-P1-E1017-APP-11 to TC-P1-E1017-APP-15, TC-P1-E1017-APP-24, TC-P1-E1017-APP-25 |
| NFR-075 / DL26 | Ledger retention period | P1 interaction ARCHIVE | Compliance period remains Pending under GAP-1029 | - | - | TC-P1-E1017-APP-22 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-P1-E1017-CON | Contract | H build dependency: the two operations, the workflow contract, the schemas and the retention-run fake P5 calls |
| RWB-P1-E1017-OPS | DevOps | Follows this story: it deploys the retention worker, the archive identity, the alerts and the runbook |
| RWB-P5-E1017-APP | App development | Sibling of the same legacy key: the rule, the action table and the Schedule JOB-17 that starts this run |
| RWB-P1-E1001-APP | App development | H build dependency: base schema, interaction, data_product, sys_objects, sys_fields and append-only trigger |
| RWB-P1-E1064-APP | App development | H build dependency: the dictionary rows that prove an age-basis field |
| RWB-PLT-TE012-APP | App development | X external dependency: the write-once container and its credential |
| RWB-PLT-E1027-CON, RWB-PLT-E1043-CON, RWB-PLT-E1071-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON | Contract | H: the decision-record library, the reference-data library, the workflow kit, the per-service Flyway sequence and the composite route |
| RWB-P3-E1021-CON | Contract | C: publishes held/open exclusions and closure dates with fakes (RD-P1-047) |

Pending: decision-record contract mapping and failure behavior, owner solution architect, GAP-2426. Decision DL26 is open, owner Compliance.

### 19. Out of scope

- `retention_rule`, `retention_action`, the retention load and its approval, and the monthly Schedule JOB-17: RWB-P5-E1017-APP (ASM-0076; Architecture v5 slides 16, 41 and 44).
- Retention classes for documents and the document legal hold (RWB-E1-041 in the legacy set, RWB-P5-E1017-APP in the target).
- The retention class for ledger entries as its own reference row (FEAT-ILG-10, RWB-E2-034).
- The decision log retention period (NFR-030, DL26) and its execution (RWB-P7-E1017-APP); the lake copy is retired with the data lake (DP-17).
- Closing a case after its retention period (REQ-S7-008, Epic 6).
- The personal data screen SCR-47 (Epic 8).
- The held/open exclusions and closure dates are owned by rwb-case and read through RWB-P3-E1021-CON (RD-P1-047).
- The write-once container, its immutability policy and its credential: RWB-PLT-TE012-APP.
- The deployment, the KEDA scaling, the alerts and the runbook: RWB-P1-E1017-OPS.
- The cross-service proof of the rule, the hold and the archive across P1, P3, P5 and P7: RWB-ITG-E1017-ITG.

### 20. Remaining delivery steps

- Size: Not specified; pending refinement. Owner: squad.
- Epic design sign-off: Pending. Owner: solution architect.
- CON Done: Pending. Owner: contract owner.
- Fake published: Pending. Owner: contract owner.
- Test data in DEV: Pending. Owner: QA.
- Decision-record payload, key, transaction timing and failure behavior: Pending, GAP-2426. Owner: solution architect.
- Archive object path and manifest format: Pending, GAP-0490. Owner: storage architect.
- Archive encryption and read roles: Pending, GAP-3456. Owner: security architect.
- Retention run record table: Pending, GAP-3457 (blocks `recordRun` and the GET). Owner: data architect.
- `holdReport` fields: Pending, GAP-3450. Owner: solution architect.
- Refused-check names and the MSG-P1-020 channel and recipients: Pending, GAP-3451. Owner: product owner.
- Flag-off message code and flag switch-on order: Pending, GAP-3452. Owner: platform architect.
- Retry against the 2 s rwb-case read and breaker threshold: Pending, GAP-3453. Owner: solution architect.
- Listing age condition for `contact_point_ext`, `valuation_ext`, `dp_treatment`, `dp_guarantee_claim`: Pending, GAP-3454. Owner: data architect with Compliance.
- Month-end arithmetic and a future `runDate`: Pending, GAP-3455. Owner: solution architect with Compliance.
- `contact_point_ext` and `valuation_ext` hold-join key: Pending, GAP-3279. Owner: data architect.
