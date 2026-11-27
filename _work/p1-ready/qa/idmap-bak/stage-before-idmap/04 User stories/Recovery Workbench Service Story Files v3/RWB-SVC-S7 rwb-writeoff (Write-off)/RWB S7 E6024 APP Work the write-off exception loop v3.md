# RWB-S7-E6024-APP Work the write-off exception loop

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Version 3 changes** (D-RCV-60 P1 developer readiness, RD-P1 register)

- Start rule of `WriteOffWorkflow` / JOB-16: only the `AceDataReady` event with `sourceSystem` ALS and `status` COMPLETED counts; the event is published once per source system and business date (RD-P1-003, RD-P1-040).

| Item | Value |
|---|---|
| Story key | RWB-S7-E6024-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-writeoff |
| Service epic | RWB-SVC-S7 |
| Wave | 4 |
| Business epic | EP06 |
| Release | 30 April 2027 (tentative) |
| Legacy key | RWB-E6-024 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | L-S7-L |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S7-E6024-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | rwb-case and rwb-decision contracts (case read, case moves, task raise, package read), built on their fakes |
| Integration dependencies | None |
| External dependencies | None |
| Size | Not specified in the source documents (DOR-RWB-S7-E6024-APP-16) |
| Contract fake version | Not specified in the source documents (DOR-RWB-S7-E6024-APP-22) |
| Contract version | Not specified in the source documents (DOR-RWB-S7-E6024-APP-23); the only version stated is the /v1 path |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S7 rwb-writeoff v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |
| Readiness decisions | RD-P1-003, RD-P1-040 |

**Change log.** D-RCV-60, 22 November 2026: the exception loop of RWB-E6-024 in rwb-writeoff. The three legacy criteria are kept word for word with their origin tag; the exception step of `WriteOffWorkflow` raises the exception under R-WO-24 when the posting step reports the retry count at or above the retry limit, moves the `write_off` row to `WRITEOFF_EXCEPTION`, raises the correction task to the loop's owner, records the correction decision for R-WO-44, R-WO-45 and R-WO-46 through the local decision-record library before any change (DP-03), answers rwb-case for the case move and serves the correction decision on base `/api/recovery/writeoff/v1` (DP-13), reached from SCR-27 through the gateway-bff composite route (DP-19). No source names the loop's owner or its time limit, which REQ-S7-004 requires, and no source publishes the correction operation, its elements or a list of values. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-S7-E6024-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (22 resolved, 13 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **write-off committee member**, I want **to open the exception path for a case the rules cannot clear**, so that **write-offs follow the criteria and the committee's decision**.

This is the exception loop of legacy RWB-E6-024. It owns:

- the three legacy criteria (AC1, AC2, AC3), copied verbatim with their origin tag, and the rules, messages and screen state they depend on;
- the exception step of `WriteOffWorkflow` on task queue `rwb-writeoff`, the stage child of `CaseWorkflow`, and the raise of R-WO-24 out of `POSTING_REJECTED` when the retry count reaches the retry limit (context pack ownership rows; Temporal and Drools Design slides 5, 12 and 13);
- the working of the loop: the correction decision of the owner and its three outcomes, the exits R-WO-44, R-WO-45 and R-WO-46 of `WRITEOFF_EXCEPTION` (Business Rules and Routing Logic v4, rows R-WO-44 to R-WO-46; States sheet, three rules out);
- the correction task raised to the loop's owner as a human task with a service level, and the `assignment` record the case workspace keeps for it, which stay rwb-case's;
- one `write_off` row moved to `WRITEOFF_EXCEPTION` in `rwb_writeoff`, with the columns of DF-FIN-010 to DF-FIN-020 that this step fills (§11);
- the decision record of the raise and of the correction, written before the row changes (DP-03), with the rule ID, its package version and the correction;
- the answer to rwb-case for the moves `WRITEOFF_EXCEPTION`, `POSTING_PENDING`, `SCAN_DUE` and `WITH_COMMITTEE`, with the rule and its version;
- the correction operation on base `/api/recovery/writeoff/v1` and the exception state of SCR-27 Write-off proposal behind the gateway-bff composite route (DP-13, DP-19).

It does not own: the published shape of the correction operation, the `CorrectionRequest` and `WriteOffCorrection` elements, the field IDs, the consumed rows, the rights, the error set and the fakes, which are RWB-S7-E6024-CON; the posting to ALS and the general ledger, its retries, R-WO-21, R-WO-22, R-WO-23 and the re-post action of R-WO-44 (RWB-S7-E6021-APP); the committee routing of R-WO-11 (RWB-S7-E6017-APP); the committee decision API-S7-002 and R-WO-15 to R-WO-17 (RWB-S7-E6018-APP to RWB-S7-E6020-APP); the other two entries to `WRITEOFF_EXCEPTION`, R-WO-41 and R-WO-43 (RWB-S7-E6027-APP and RWB-S7-E6023-APP by their subject); the case of record, its route states, the task and the assignment, which are rwb-case (P3); the WO package and its rule rows, which are rwb-decision (P7); and the deployment of this build, which is the operations story of this legacy key.

### 2. Business rationale

The feature objective, the problem and the metric are unchanged from the legacy story and the module FSD: the loop "opens the exception path for a case the rules cannot clear", because write-off populations are assembled by hand each month, and the measure is "Write-off packs accepted first time | Rising each month | Decision log and Workbench records | Monthly" (FSD S7 A2.12.1; FSD S7 A1.3). The requirement is REQ-S7-004, "The write-off exception loop has one named owner and a time limit." What D-RCV-60 changes is who holds the case, the task, the rule and the decision.

- **The requirement names two facts no source supplies.** The rule row gives the owner as "Owner to confirm with C&R" and the timer as "to confirm with Credit Administration", and the FSD says of the loop "This loop has no owner today" (Business Rules and Routing Logic v4, R-WO-24; FSD S7 A2.12.1). The story builds the loop with the owner and the service level as rule and reference rows and records both values as unconfirmed (ASM-5093).
- **The state has three entries and three exits.** `WRITEOFF_EXCEPTION` is an exception state of the Write-off route set with three rules in (R-WO-24, R-WO-41, R-WO-43) and three out (R-WO-44, R-WO-45, R-WO-46). Only R-WO-24 is this feature's; the other two entries belong to the payment and reconciliation slices and appear in no FSD feature rule table (ASM-5097).
- **The case, the task and the assignment stay with rwb-case.** `recovery_case`, `task` and `assignment` (DF-WRK-009 to DF-WRK-016) are P3's, so the raise and every correction **answer** the move, and the assignment is written by the workspace, not here (ASM-5096).
- **The rule is read, not embedded.** R-WO-24 and its retry limit are rows of the WO package, 51 rules over 27 states, authored and approved in rwb-decision; DP-04 is not in this key's pattern set (ASM-5095).
- **The count is the posting step's.** `retry_count` is no column of `write_off` and appears in no field list, so the count arrives from the posting step of the same workflow and no column is added for it (ASM-5095).
- **The decision is recorded first**, in the same transaction as the row, which is what legacy AC1 asked for and legacy AC3 tested.
- **The correction is a ledger fact elsewhere.** The interaction ledger names a `CORRECTION` event code and is owned by rwb-source-data by default ruling, so the correction is recorded in the decision record and, where the ledger is written, by its owner; DP-18 is absent from this key's pattern set.

No business value moves: the retry limit, the owner, the service level and the three correction outcomes are rule rows and reference data read with their version, never constants of the code.

### 3. Preconditions

- RWB-S7-E6024-CON is published: the correction operation, the `CorrectionRequest` and `WriteOffCorrection` elements, the field IDs, the consumed rows, the rights, the `Idempotency-Key` rule, the error set and the fakes are baselined and handed to this story.
- The rwb-case read of a write-off case is published with its fake: the case reference, the case number, the product group, the write-off reference, the stage and the state `POSTING_REJECTED`. Its operation name is Not specified in the source documents (GAP-3039; ASM-5096).
- The rwb-case case-move answer is available for the fake: the four moves of this story with the rule and its version. No source names a published operation that moves a case state on behalf of a stage; on the workflow boundary it is the stage outcome the parent `CaseWorkflow` applies (GAP-3039; ASM-5096).
- The rwb-case task raise is available for the fake: the correction task, its queue, the loop's owner and its service level. Its operation name and the queue code are Not specified in the source documents (GAP-3039; ASM-5096).
- The rwb-decision rule-package read is published with its fake and answers the WO package at its version in force, with R-WO-24, R-WO-44, R-WO-45 and R-WO-46 among its 51 rules over 27 states and the retry limit among its facts; its operation name is Not specified in the source documents (GAP-3039; ASM-5095).
- RWB-PLT-E1027-CON is published with its writer fake: the local decision-record library writes in the caller's transaction, and a failed write stops the action with MSG-P7-003, so the row and its record commit together or not at all (DP-03).
- RWB-PLT-N001-CON is published: SCR-27 reaches this service through the gateway-bff composite route, one hop, and no screen calls a service directly (DP-19).
- `write_off` exists in schema `rwb_writeoff` from the DB story of this service, with the columns of DF-FIN-010 to DF-FIN-020 and the standard record columns of TSD S7 T3.0; this story adds no table, no column and no migration.
- The WO package is in force at its version and the retry limit is a row of it; the correction task's service level is a reference row and its value is Not specified in the source documents (GAP-3039; ASM-5093).
- The service runs as its own login on schema `rwb_writeoff`; it holds no grant on another `rwb_*` schema and no `v_ace_*` grant, so a statement on `recovery_case`, `assignment` or another service's table is refused by the database and fails the boundary test.
- No approval is needed to build against a Draft contract baseline; the contract is tagged by RWB-S7-E6024-CON when its tests pass.

### 4. Flow

1. The posting step of `WriteOffWorkflow` answers a rejected posting with its retry count; the exception step of the same workflow on queue `rwb-writeoff` reads the count and the WO package at its version in force from rwb-decision, one hop with a 2 s budget and a breaker (FSD S7 A2.9, A2.12; ASM-5095).
2. The step reads the case on the rwb-case contract: the case reference, the case number, the product group, the write-off reference, the stage and the state `POSTING_REJECTED`, read only; it never reads `recovery_case` (ASM-5096).
3. `ExceptionEvaluator` evaluates R-WO-24: where the retry count is at or above the retry limit, the exception is raised; where it is below, the case stays with the posting step and no exception opens (FSD S7 A2.12.3.1; BRRL R-WO-24).
4. `WriteOffDecisionRecordWriter` writes the decision record of the raise **before any change**: the case reference, the write-off reference, the rule ID `R-WO-24` with its package version, the retry count and the limit in force as inputs, the outcome and the move. A failed write stops the step with nothing changed (DP-03; AC1, AC3).
5. `ExceptionRowWriter` moves the `write_off` row to `WRITEOFF_EXCEPTION` in one `rwb_writeoff` transaction with the record and the idempotency row (§11).
6. `CaseMoveAnswer` answers rwb-case for the move `WRITEOFF_EXCEPTION` with the rule ID, the version and the decided-at time; rwb-case writes the `recovery_case` row (ASM-5096).
7. `CorrectionTaskClient` raises the correction task to the loop's owner through the human-task template of the workflow kit, with the case, the write-off, the state, the rule and the service level as parameters. The owner and the service level are read as rule and reference rows and no value is written in code (ASM-5093).
8. The owner decides on the correction task or on the correction operation: `CORRECTION_REPOST`, `CORRECTION_RETURN_TO_SCAN` or `CORRECTION_REFER_TO_COMMITTEE`, the three rule events of R-WO-44, R-WO-45 and R-WO-46 (BRRL rows; ASM-5094).
9. The decision record of the correction is written before the row changes, with the correction, the rule ID of the chosen exit and its version, the actor by identity and role, and the decided-at time.
10. `ExceptionRowWriter` writes the row state the correction names and `CaseMoveAnswer` answers the move: `POSTING_PENDING` on R-WO-44, `SCAN_DUE` on R-WO-45, `WITH_COMMITTEE` on R-WO-46. The re-post itself, the next scan and the pack are the owning stories' (RWB-S7-E6021-APP, RWB-S7-E6013-APP, RWB-S7-E6015-APP).
11. The task closes on the workspace and the failed-candidate count of the day is reported; a repeated decision with the same `Idempotency-Key` answers the decision it created and writes no second record.
12. SCR-27 Write-off proposal shows the case in its exception state — the write-off, the retry count, the limit in force, the rule and version and the three corrections offered — from this service through the composite route, read only, next to the case state of rwb-case (DP-19).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The local decision record cannot be written | The transaction writes nothing: no row state change and no case-move answer leaves the service | MSG-P7-003 | AC3, TC-E6-024-03, TC-E6-024-05 |
| X2 | The role does not hold the Write-off and posting right A of the correction | 403 before any read or write; nothing changes and no record is written | MSG-P4-002 | AC4, TC-E6-024-04, TC-E6-024-06 |
| X3 | The retry count is below the retry limit | R-WO-24 does not fire; no exception, no row change and no task, and the case stays with the posting step | None | AC2 |
| X4 | The correction is not one of the three outcomes, or the task is submitted with no correction | The request is refused with MSG-GEN-001 and the task stays open; nothing changes | MSG-GEN-001 | AC1 |
| X5 | The rwb-case, rwb-decision or rwb-case task contract does not answer inside 2 s, or its breaker is open | The step retries on the workflow's own schedule; nothing is written and no move is answered; the caller sees 503 with the platform error envelope | None | AC1, AC10, X6 |
| X6 | The correction task is not raised because the workspace refuses the assignment | The record and the row are rolled back with the answer, and the raise is retried; the loop is never opened without its task | None | AC1 |
| X7 | A repeated decision for the same write-off, or the same `Idempotency-Key` twice | One record, one row state and one answer; the repeat is counted and the key answers the decision it created | None | AC1 |
| X8 | A component, a statement or a test reaches a `recovery_case`, `task` or `assignment` row or another service's schema | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | AC5, TC-E6-024-07, Section 17, BR3, BR4 |

X1 and X2 are the legacy exception paths carried onto the slice, X3 to X6 are the raise and the task of the loop, and X7 to X8 are the once-per-decision rule and the schema boundary.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-S7-E6024-CON, the rwb-case, rwb-decision and rwb-case task fakes and the decision-record stub, on its own schema, and needs no live P3, P7 or posting step |
| Negotiable | The activity names, the decision code per rule and the shape of the stage outcome are this story's choice; the rule, the messages, the screen state, the operation and the table columns are fixed |
| Valuable | A write-off that the posting cannot clear leaves the open retry loop and reaches one named person with one decision, so the exception is corrected, returned or referred instead of looping |
| Estimable | One workflow step, one evaluator, one record write, one row writer, one task raise, one case-move answer, four clients, one operation and one read-only screen fragment |
| Small | Finished inside two weeks with its tests on the fakes |
| Testable | Each criterion runs on a synthetic case and write-off through the contract fakes, plus the below-limit, refused, failed-record and repeated-decision cases |

### 7. Acceptance criteria

```gherkin
Feature: Work the write-off exception loop

  Background:
    Given case "RC-2026-000701" carries write-off "WO-2026-000311" at the write-off stage of rwb-writeoff
    Given the WO rule package is in force at its version and carries R-WO-24, R-WO-44, R-WO-45 and R-WO-46
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 Work the write-off exception loop (legacy RWB-E6-024 AC1)
    Given the rwb-case contract mock returns the case "RC-2026-000701" in state "POSTING_REJECTED" with the correction task open on the case workspace
    Given the rwb-decision contract mock returns the WO package at its version in force with R-WO-24 and the retry limit as a rule fact
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then opens the exception path for a case the rules cannot clear. This loop has no owner today
    Then the system writes the result to the decision record with the rule version

  Scenario: AC2 Rule R-WO-24 (legacy RWB-E6-024 AC2)
    Given the rwb-case contract mock returns the case "RC-2026-000701" in state "POSTING_REJECTED" and accepts the move "WRITEOFF_EXCEPTION"
    Given a case in state POSTING_REJECTED
    When retry limit reached
    Then raise the write-off exception for correction
    Then the case moves to WRITEOFF_EXCEPTION

  Scenario: AC3 Not recorded (legacy RWB-E6-024 AC3)
    Given the decision record cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003

  Scenario: AC4 A role without the correction right is refused (new, D-RCV-60)
    Given the user holds the write-off and posting right C and does not hold right A
    When the user submits a correction for the write-off
    Then the request is refused with 403 and MSG-P4-002 before any read or write
    Then nothing changes and no record is written

  Scenario: AC5 A statement outside the service boundary fails the build (new, D-RCV-60)
    Given a component of rwb-writeoff issues a statement against a recovery_case, task or assignment row or another service schema
    When the boundary test runs
    Then the grant refuses the statement and the build fails
    Then nothing is released

  Scenario: AC6 No person data enters the decision record (new, D-RCV-60)
    Given a correction is recorded for the write-off
    When the decision record is written
    Then the record and the answer carry identifiers, a role code and an identity only
    Then no name, address, contact value or identity number is written

  Scenario: AC7 A correction exit writes its state and its move (new, D-RCV-60)
    Given the write-off is in state WRITEOFF_EXCEPTION and the owner decides R-WO-44, R-WO-45 or R-WO-46
    When the correction is recorded
    Then the write-off row takes the state of the chosen exit and the case move is answered
    Then the decision record carries the chosen rule ID and its version

  Scenario: AC8 A provided operation answers 401, 403 or 404 with the platform error envelope (new, D-RCV-60)
    Given a caller presents no valid credential, a role without the right, or a write-off outside the route of the correction
    When the caller calls the correction operation
    Then the answer is 401, 403 or 404 with the platform error envelope
    Then nothing changes and no record is written

  Scenario: AC9 A replay of a write with the same Idempotency-Key answers the first decision (new, D-RCV-60)
    Given a correction for the write-off was recorded under an Idempotency-Key
    When the same request is sent again with the same Idempotency-Key
    Then one decision record, one row state and one answer exist
    Then the repeat is counted and the key answers the decision it created

  Scenario: AC10 A consumed call that fails or does not answer leaves nothing written (new, D-RCV-60)
    Given the rwb-case contract does not answer inside 2 s, or its breaker is open
    When the correction is submitted
    Then the step retries on the workflow's own schedule and the caller sees 503 with the platform error envelope
    Then nothing is written and no case move is answered
```

The three criteria are the legacy criteria of RWB-E6-024 word for word, with their origin tag added and nothing else changed: the repeated `Then`, the wording of `the user acts on the screen`, `retry limit reached` and `the action is taken`, and the one legacy Given of AC2 all stand. The cross-service parts are mocked, so AC1 carries two `Given the <service> contract mock returns <x>` lines and AC2 one, and those are the only additions. What the legacy lines describe now happens in three places: rwb-case holds the case, its state and the task; rwb-decision holds the package with the retry limit; and this story evaluates the rule, raises the task, writes the record and the row and answers the move. `the decision log` of the legacy text is the local decision record of DP-03 in `rwb_writeoff`, with the central `decision_log_entry` ledger of rwb-decision behind it. Two points are recorded rather than smoothed over: the legacy sentence "This loop has no owner today" is kept word for word and the loop's owner and service level are the unconfirmed values of AC1, which REQ-S7-004 requires and no source supplies (ASM-5093); and the legacy AC2 tests the raise only, while the working of the loop that the title names rests on the three exits of the state, which are built here and covered by the contract cases (ASM-5094, ASM-5097).

### 8. Business rules

| Rule | Route set | Decision | From state | Event | Condition | Action | To state | Owner | Systems | Timer |
|---|---|---|---|---|---|---|---|---|---|---|
| R-WO-24 | Write-off | D9 | POSTING_REJECTED | RETRY_LIMIT_REACHED | retry_count at or above the retry limit | Raise the write-off exception for correction | WRITEOFF_EXCEPTION | Owner to confirm with C&R | Rules component, Case Workspace | to confirm with Credit Administration |

The row is the row of the Business Rules and Routing Logic v4, copied character for character. Its owner and systems columns name a business role and systems, not services: in the target the "Rules component" is the WO package read from rwb-decision (P7) and evaluated here, and "Case Workspace" is SCR-27 and the case workspace of rwb-case (P3), which holds the task. The two unconfirmed cells are the loop's owner and its time limit, which REQ-S7-004 requires and no source supplies (ASM-5093).

The three exits the loop is worked by are the third table, copied the same way, because the state is worked by this story and the phrase "for correction" has no meaning without them.

| Rule | Route set | Decision | From state | Event | Condition | Action | To state | Owner | Systems | Timer |
|---|---|---|---|---|---|---|---|---|---|---|
| R-WO-44 | Write-off | D9 | WRITEOFF_EXCEPTION | CORRECTION_REPOST | the owner decides to re-post | Re-post to ALS and the general ledger | POSTING_PENDING | Credit Administration | ALS core and GL | to confirm with Credit Administration |
| R-WO-45 | Write-off | D9 | WRITEOFF_EXCEPTION | CORRECTION_RETURN_TO_SCAN | the owner decides to return the case | Return the case to the next monthly scan | SCAN_DUE | Write-off team | Workbench, Decision Log | next cut-off |
| R-WO-46 | Write-off | D9 | WRITEOFF_EXCEPTION | CORRECTION_REFER_TO_COMMITTEE | the owner refers the case back | Return the pack to the committee | WITH_COMMITTEE | Write-off committee | Committee View | None |

| ID | Rule | Source |
|---|---|---|
| BR1 | The exception state of the write-off is this service's: `write_off` is the one table of `rwb_writeoff`, and no other service writes it | Context pack ownership rows (table `write_off`); TSD S7 T3.1; FSD S7 A2.12.2 |
| BR2 | The decision is recorded before the row and the answer change, with the rule ID, its package version and the correction; a failed write changes nothing and the caller sees MSG-P7-003 | DP-03; TSD S7 T2 ("writes the decision log entry before any change"); legacy AC1 and AC3 |
| BR3 | The ACE data stays with rwb-source-data: this story reads no `v_ace_*` view and no ACE table, and the ALS posting and its reference are the posting story's | DP-05 as a prohibition; FSD S7 A2.12.2; ASM-5095 |
| BR4 | The case, its route states, the task and the assignment are rwb-case's: the moves are answered and never written, and no `assignment` row is written here | ASM-5096; TSD S7 T4; LDM v8 `assignment` (work management) |
| BR5 | No cross-schema join and no foreign key leaves `rwb_writeoff`; `case_id` and `decision_log_id` are identifiers of other services' facts | DP-01; TSD S7 T3.3 |
| BR6 | Every value a business person may change is a rule row or reference data read with its version: the retry limit, the loop's owner, the correction task's service level and the three correction outcomes | FSD S7 A2.12.3.1, BR-S7-012; legacy Guardrails; ASM-5093, ASM-5094 |
| BR7 | The three entries of `WRITEOFF_EXCEPTION` are not one story: this story raises the state under R-WO-24 only, and R-WO-41 and R-WO-43 are the payment and reconciliation slices' | BRRL v4, States sheet (`WRITEOFF_EXCEPTION`, 3 rules in); ASM-5097 |
| BR8 | The same decision twice, or the same `Idempotency-Key` twice, writes one record, one row state and one answer | Platform API rule (ADR-020); TSD S7 T-A.2 |
| BR9 | No person name, address, contact value or identity number enters `rwb_writeoff`, the record, a log or a workflow input; the actor is an identity and a role code | Template and Rules §R7.2 (s17); TSD S7 T6.2 |
| BR10 | The write-off row carries the route state the rule names, because no list of values publishes a write-off state vocabulary | TSD S7 T3.2 (empty); ASM-5094 |

| Rule | Covered by |
|---|---|
| BR1 | AC5, TC-E6-024-07 |
| BR2 | AC1, AC3, TC-E6-024-03 |
| BR3 | AC5, TC-E6-024-07 |
| BR4 | AC2, AC5, TC-E6-024-07 |
| BR5 | AC5, TC-E6-024-07 |
| BR6 | AC1, AC2, TC-E6-024-01, TC-E6-024-02 |
| BR7 | AC2, TC-E6-024-02 |
| BR8 | AC1, AC9, TC-E6-024-11 |
| BR9 | AC6, TC-E6-024-08 |
| BR10 | AC2, TC-E6-024-02 |
| R-WO-24 | AC2 |
| R-WO-44 | AC7, TC-E6-024-09 |
| R-WO-45 | AC7, TC-E6-024-09 |
| R-WO-46 | AC7, TC-E6-024-09 |

### 9. State transitions

The case route state is rwb-case's and is not changed by this story: the step answers the move and the parent `CaseWorkflow` applies it (BR4). What this story owns is the state of the step and the row it writes.

| From (step) | Event | Condition | To |
|---|---|---|---|
| Waiting | The posting step answers a rejection with its retry count | The package in force is read | Evaluating |
| Evaluating | R-WO-24 fires | The count is at or above the limit | Recording |
| Evaluating | No rule fires | The count is below the limit | Waiting, `POSTING_REJECTED` unchanged (X3) |
| Recording | The record is written | The transaction commits | Awaiting the correction |
| Recording | The record write or the transaction fails | X1 | Waiting, nothing changed |
| Awaiting the correction | The owner decides | One of the three rule events | Applying the correction |
| Applying the correction | The row state and the answer are written | The transaction commits | Closed for this exception |

| From (`write_off.state`) | Event | Condition | To |
|---|---|---|---|
| `POSTING_REJECTED` | R-WO-24 | retry_count at or above the retry limit | `WRITEOFF_EXCEPTION`, written by this step |
| `WRITEOFF_EXCEPTION` | R-WO-44 | the owner decides to re-post | `POSTING_PENDING`, written here; the re-post is RWB-S7-E6021-APP's |
| `WRITEOFF_EXCEPTION` | R-WO-45 | the owner returns the case | `SCAN_DUE`, written here |
| `WRITEOFF_EXCEPTION` | R-WO-46 | the owner refers the case back | `WITH_COMMITTEE`, written here |
| `WRITEOFF_EXCEPTION` | R-WO-41 | a payment reopens a question | Not this story: RWB-S7-E6027-APP |
| `WRITEOFF_EXCEPTION` | R-WO-43 | the approved and posted populations differ | Not this story: RWB-S7-E6023-APP |

The route states are those of the WRITEOFF machine of TSD S7 T4 and live on the case of record; the row state mirrors the route state because no list of values publishes a write-off row state (BR10). `WRITEOFF_EXCEPTION` is an exception state with 3 rules in and 3 out (BRRL v4, States sheet), and the state label in the source reads "Write-off exception, owner to confirm", which is the second unconfirmed fact of REQ-S7-004.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-WOCOMM, write-off committee member | Write-off and posting RA in TSD S7 T6.1 and right A of the legacy permission table: the primary role, working the loop and deciding a correction |
| RW-CREDITAD, Credit Administration officer | Write-off and posting CRUA: works the loop, raises and re-runs a correction, reads the post-charge-off history |
| RW-PRODHEAD, RW-FINANCE | Write-off and posting RA: work the loop and decide a correction inside their delegation |
| RW-WRITEOFF, write-off team member | Write-off and posting CRU: reads the exception, raises the task again and does not decide a correction, because right A is not in the legacy table for this role |
| RW-RISK, RW-COE, RW-CONDUCT, RW-AUDIT, RW-BIANAL, RW-TRIBE, RW-FRAUD, RW-DEBTSALE | Write-off and posting R: read only, in scope |
| SY-CASEWF, SY-RULES, SY-AGENT, SY-DATALOAD | Write-off and posting R as the matrix gives them: the service identities run the step and are subject to the same checks |
| rwb-writeoff service identity | Runs the step, reads the case, the package and the task answer, writes the record and the row, raises the task and answers the moves; it holds no grant on another schema and no `v_ace_*` grant |

The rights are the rows of TSD S7 T6.1 and nothing wider. The legacy permission table gives the module right A to RW-CREDITAD, RW-PRODHEAD, RW-WOCOMM and RW-FINANCE and right C to RW-WRITEOFF and RW-CREDITAD; the correction is a decision on the write-off and takes right A, while the read of the loop and the raise take C (ASM-5092). The FSD gives the loop the write-off committee member as primary role with the write-off team member and the Finance delegate as also-users (FSD S7 A2.12.3.3), which matches the persona of the legacy story. DP-08 is not in this story's pattern set: the capability area and the right are declared per operation and the guard is a service-template capability, so the check is stated here and not built here. Each operation's authorise check is the rwb-access check of the capability area and the right in this section, read through the guard.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-FIN-010 | write_off (S7, `rwb_writeoff`) | id | Read, the write-off reference of the record, the task and the answer |
| DF-FIN-011 | write_off (S7, `rwb_writeoff`) | case_id | Read, and carried in the record and the answer |
| DF-FIN-012 | write_off (S7, `rwb_writeoff`) | decision_log_id | Write, the identifier the local decision record returns for the raise and for the correction |
| DF-FIN-013 | write_off (S7, `rwb_writeoff`) | amount | Read, the amount the exception and the re-post carry; not changed by this step |
| DF-FIN-014 to DF-FIN-019 | write_off (S7, `rwb_writeoff`) | tax_criteria_met, committee_date, posted_date, responsibility_center, cost_center, gl_product | Read only: written by RWB-S7-E6014-APP, RWB-S7-E6018-APP and RWB-S7-E6021-APP |
| DF-FIN-020 | write_off (S7, `rwb_writeoff`) | recovered_after | Read only: unchanged by this step |
| Standard columns | write_off (S7, `rwb_writeoff`) | `is_active`, `state`, `version`, `created_at`, `created_by`, `updated_at`, `updated_by` | Write, `state` = `WRITEOFF_EXCEPTION` and then the state the correction names, with the optimistic lock of `version` |
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library, created in `rwb_writeoff`) | rule id, rule version, inputs reference, outcome, correction, decided at | Write through the local library, before the row and the answer change |
| `retry_count` | the posting step (RWB-S7-E6021-APP) | the retry count at the limit | Not a column of `write_off` and in no field list: read as the step's fact (GAP-3039; ASM-5095) |
| DF-CAS-001 to DF-CAS-023 | recovery_case (P3) | id, case_no, product_group, primary_person_key, status, stage_code and 17 more | Not read as a table and not written: the case arrives on the rwb-case contract |
| DF-WRK-009 to DF-WRK-016 | assignment (P3, work management) | id, case_id, task_id, assignee_user_id, assigned_at, ended_at and 2 more | Not written: the workspace writes the assignment when the task is raised (ASM-5096) |
| DF-REF-001 to DF-REF-015 | rule_row (P7) | rule_id, rule_version, route_set, from_state, event_code and 9 more | Not read as a table: the rule rows arrive on the package read |

Field IDs are those of TSD S7 T3.1, the Logical Data Model and Data Dictionary and the legacy Data table, with their owners changed to P3, P7 and the posting step by the target. **No new table, no new column and no migration**: `write_off` arrives with the DB story of this service, this story writes its `state`, `decision_log_id` and standard columns, and `decision_record` and `idempotency_key` are library objects created in `rwb_writeoff` by the library's own migration (DP-03).

**No personal data.** The rows carry identifiers, an amount, dates, a state, a retry count and a rule version. No name, address, contact value or identity number enters `rwb_writeoff`, the record, a task parameter, a log or a workflow input, and the fixtures are synthetic. `primary_person_key` is P3's and is never copied here.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-writeoff (S7); base `/api/recovery/writeoff/v1` (DP-13). This story supplies the behaviour behind the correction, whose shape RWB-S7-E6024-CON declares.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| POST | `/write-offs/{writeOffId}/correction-decision` (proposed path; no source names this operation - GAP-3039; ASM-5092) | `CorrectionRequest` in with `correction` (one of `CORRECTION_REPOST`, `CORRECTION_RETURN_TO_SCAN`, `CORRECTION_REFER_TO_COMMITTEE`) and `correctionReason`, `WriteOffCorrection` out with the write-off, the case, the correction, the rule ID with its version, the from state `WRITEOFF_EXCEPTION`, the to state and the decided-at time | Write-off and posting, right A, scope applied | `Idempotency-Key` header |

The errors are 400, 401, 403 with MSG-P4-002, 404 for an unknown write-off, 409 for a write-off that is not in `WRITEOFF_EXCEPTION` or a repeated key with another body, 422 with MSG-GEN-001 for a missing or unknown correction and 503 when the library or a consumed contract does not answer. TSD S7 T-A.1 publishes two operations for the module — `POST /write-off-scans` (API-S7-001, right C) and `POST /write-offs/{writeOffId}/committee-decision` (API-S7-002, right A) — and no correction operation, and the legacy Endpoints table of RWB-E6-024 repeats those same two rows, so the correction is the one operation this baseline adds (GAP-3039; ASM-5092). The scan is RWB-S7-E6013-APP's and the committee decision is RWB-S7-E6018-APP's; neither is built or declared here.

#### 12.2 REST operations consumed

| Operation | Path | Owner | Use |
|---|---|---|---|
| The read of a write-off case (operation name Not specified in the source documents (GAP-3039; ASM-5096)) | `/api/recovery/case/v1` | P3 rwb-case | The case reference, case number, product group, write-off reference, stage and state `POSTING_REJECTED`; read only, faked |
| The case-move answer (operation name Not specified in the source documents (GAP-3039; ASM-5096)) | rwb-case (P3) | P3 rwb-case | The moves `WRITEOFF_EXCEPTION`, `POSTING_PENDING`, `SCAN_DUE` and `WITH_COMMITTEE` with the rule and its version; on the workflow boundary it is the stage outcome the parent `CaseWorkflow` applies; faked |
| The correction task raise and its answer (operation names and queue code Not specified in the source documents (GAP-3039; ASM-5093, ASM-5096)) | `/api/recovery/case/v1` | P3 rwb-case | The human task with its owner, its queue, its service level and its outcome; faked |
| The WO rule-package read in force (operation name Not specified in the source documents (GAP-3039; ASM-5095)) | `/api/recovery/decision/v1` | P7 rwb-decision | The WO package at its version, with R-WO-24 and R-WO-44 to R-WO-46 among its 51 rules over 27 states and the retry limit among its facts; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The four rows are contract dependencies of class C that the plan does not carry, because this story's C row is None; the absence is recorded (GAP-3039).

#### 12.3 Events published

None. The service publishes on `rwb.writeoff.events.v1` and its event set carries `WriteOffApproved` (event `EV-24`), which the approval story RWB-S7-E6018-APP publishes when the committee approves. The exception raises no domain event: the case state change is rwb-case's `CaseStateChanged` (`EV-05`), and the raise is a command answered across the workflow boundary. A build that publishes one fails the absence test. The topic carries the retry and `.dlt` topics of the platform (DP-14), and the outbox and inbox library that relays it is the DP-09 dependency the plan does not carry for this key.

#### 12.4 Events consumed

None of this story's own. The raise is started by the posting step of the same `WriteOffWorkflow` and not by an event: the connection matrix gives row S7 a subscription to rwb-payment and one to rwb-source-data, and both belong to the post-charge-off recovery story RWB-S7-E6027-APP (`ProceedsMatched`, `EV-25`, and the ACE data-ready fact, `EV-26`). The retry count therefore arrives from the workflow's own posting step and no subscription is declared here. Where the retry count is later published as an event by its owner, the inbox of DP-09 receives it and that library is the recorded missing H row.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `WriteOffWorkflow` | Workflow, one execution per case in the write-off stage, the child of `CaseWorkflow`, continues-as-new at each stage end | `rwb-writeoff` | Input: the case, the route state and the package in force; signals: the posting outcome with its retry count and the correction decision. This step sits after the posting step of the same stage |
| `raiseWriteOffException` | Activity, the raise | `rwb-writeoff` | The case, the write-off, the retry count and the package version in; the rule ID with its version, the row state and the case move out, with the record and the row written in one transaction |
| `recordCorrection` | Activity, the working of the loop | `rwb-writeoff` | The correction, the rule ID of the chosen exit with its version and the actor in; the record, the row state and the case move out |

No child workflow for the case and none for the money exists in this service, and the correction task is the workflow kit's human-task template with its own timer. The activity names are a target design choice fixed by no source document. Start rule of `WriteOffWorkflow`: JOB-16 on the third working day after AceDataReady (R-WO-01) (counted only for the event with `sourceSystem` = `ALS` and `status` = `COMPLETED`, RD-P1-040), per Temporal Catalog v1. Workflow ID form and duplicate-start policy: Not specified in the source documents (CG-ALL-11139). `raiseWriteOffException` is not in Temporal Catalog v1; the name is a target design choice (DOR-RWB-S7-E6024-APP-8).

#### 12.6 Schedules

None new. The loop is started by the posting step and worked by a person, so this story registers no Schedule, and the legacy JOB-16 scan and its Temporal Schedule stay RWB-S7-E6013-APP's. The correction task's service level is the timer of the human-task template of the workflow kit, and its value is Not specified in the source documents (GAP-3039; ASM-5093): it is a reference row read at run time, never a constant, and where the template's timer kit is a platform dependency the plan's H row does not carry it is recorded rather than added.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| write_off | S7 (`rwb_writeoff`) | The write-off of a case; this story moves its `state` to `WRITEOFF_EXCEPTION` and then to the state the correction names |
| decision_record | PLT library, created in `rwb_writeoff` | The local hash-linked decision record of the raise and of the correction (DP-03) |
| idempotency_key | PLT library, created in `rwb_writeoff` | The key of the repeated decision and the answer it holds |
| outbox_event | PLT library, created in `rwb_writeoff` | Present as a library object; this step writes no row to it (§12.3) |

Not owned and never read as a table: `recovery_case`, `task` and `assignment` (P3), every `v_ace_*` view (P1), `decision_log_entry` and `rule_row` (P7), `document` (P5), `proceeds` (P8) and the later stories' data. `retry_count` is no column of `write_off` (§11) and the posting record that holds it is RWB-S7-E6021-APP's. No foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case case fake | Case `RC-2026-000701` with write-off `WO-2026-000311` in `POSTING_REJECTED`, a case in `WRITEOFF_EXCEPTION`, and a case that has left the stage | AC1, AC2, X3 |
| rwb-case case-move fake | The four moves accepted for the write-off, and a move refused because the case is not in the expected state | AC2, X7 |
| rwb-case task fake | The correction task accepted with its owner, queue and service level; a refused assignment; an unreadable answer | AC1, X5, X6 |
| rwb-decision rule-package fake | The WO package at its version in force with R-WO-24, R-WO-44 to R-WO-46 and the retry limit | AC1, AC2, X3 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and outbox, and a stopped chain | AC3, X1 |
| gateway-bff composite route fake | The merged SCR-27 answer for the write-off, in its exception state | AC1 |

The fakes are test-only and are replaced by the real services in SIT. The operation names of the four consumed rows carry the placeholder until their owners confirm them (GAP-3039; ASM-5093, ASM-5095, ASM-5096).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 4 consumed | `POST /write-offs/{writeOffId}/correction-decision` on `/api/recovery/writeoff/v1`; the case read, the case-move answer, the task raise and the package read; one hop, 2 s |
| Kafka | 0 published, 0 consumed | No event of this step; `WriteOffApproved` (EV-24) is the approval story's and the payment and ACE subscriptions are RWB-S7-E6027-APP's |
| Temporal | 1 workflow, 2 activities, 0 Schedules | `WriteOffWorkflow`, `raiseWriteOffException` and `recordCorrection` on `rwb-writeoff` |
| File | None | No file is read, built or delivered here |

### 13. Solution plan

**Package.** Java package `th.co.scb.ace.workbench.recovery.writeoff`, module `exception`; front end `src/modules/recovery/writeoff/WriteOffException.tsx`, the fragment SCR-27 embeds, read only.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the transaction rule of both activities: the record and the row commit together or not at all. DP-13 moves the base of the one added operation and nothing else. DP-19 is how SCR-27 reaches this service, one hop through the gateway. These three are the whole pattern set of the key and the story adds no fourth: DP-04 (the embedded Drools kit), DP-09 (the outbox and inbox library), DP-10 (the Scheduled job kit) and DP-18 (the interaction ledger) are real dependencies of the stage that the plan does not hold, and they are recorded in the registers instead of the metadata table (GAP-3039).

**Dependencies the tables add and the plan does not hold.** The four consumed rows are class C dependencies in fact and the plan's C row is None (GAP-3040), so the story builds against their documents and fakes on Day 1. The Drools kit of DP-04 would add `RWB-PLT-E1072-CON` and a second kit story that is not specified in the source documents (CG-ALL-11137); the package is read as data and evaluated by this service's own evaluator, so no kit is declared. The human-task template and its timer are the workflow kit's, and no row for it is in the plan. The plan's H row stands unchanged.

**Correction operation.** The correction operation is the one operation added on the base `/api/recovery/writeoff/v1` (DP-13). Its path, request element, answer element and error set are Not specified in the source documents (GAP-3039). Its vocabulary is the three rule events of the exit (R-WO-44, R-WO-45, R-WO-46), because no list of values exists (TSD S7 T3.2, BR10).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `WriteOffWorkflow` exception head | Workflow | Takes the posting outcome and the correction signal, reads the package and reports the outcome to the parent |
| `raiseWriteOffException` | Activity | Reads the case and the package, evaluates R-WO-24, writes the record and the row, answers the move and raises the task |
| `recordCorrection` | Activity | Records the correction of R-WO-44, R-WO-45 or R-WO-46, writes the row state and answers the move |
| `ExceptionEvaluator` | Service | The rule evaluation over the package in force, with the retry limit and the below-limit path |
| `WriteOffDecisionRecordWriter` | Library adapter | Writes the record of the raise and of the correction before any change, hash-linked; refuses the step when the write fails |
| `ExceptionRowWriter` | Repository | Moves the `write_off` row in one `rwb_writeoff` transaction with the idempotency row and the optimistic lock |
| `CaseClient` | Client | The case read, the case-move answer and the task raise of rwb-case, one hop, 2 s, breaker |
| `RulePackageClient` | Client | The package read of rwb-decision at its version in force |
| `CorrectionController` | Controller | The correction operation, the capability area and right, the `Idempotency-Key` and the problem mapping |
| `WriteOffException` | React component | Shows the exception and the three corrections on SCR-27, read only, with the refusal and not-recorded states |

**Database and migrations.** No Flyway file. `write_off` arrives with the DB story of this service, and the record and idempotency key are library objects created in `rwb_writeoff` by the library's migration (DP-03). No column is added for the retry count, the limit, the owner, the service level or the correction: the first two are rule and workflow facts, the next two are reference rows and the last is a decision recorded in the record.

**Configuration and reference data.**

- The retry limit, the loop's owner and the correction task's service level: rule rows of the package and reference rows with their version, never written in code (ASM-5093, ASM-5095).
- Parameters read: the retry limit (rule row of the package), the loop's owner and the correction task's service level (reference rows), and the three correction outcomes (reference values). Reference-data contract: Not specified in the source documents (DOR-RWB-S7-E6024-APP-20).
- The capability area "Write-off and posting" and its rights: access rows of rwb-access, read through the guard.
- The 2 s budget, the single hop and the breaker are the platform rule of ADR-020.

**Build steps**

1. The exception head of `WriteOffWorkflow` and its input record, registered on `rwb-writeoff` as the stage child of `CaseWorkflow`, after the posting step.
2. `CaseClient` and `RulePackageClient` against their fakes, with the 2 s budget, the breaker and the no-answer path (AC1, X5).
3. `ExceptionEvaluator` over the package, with R-WO-24 and the below-limit path (AC2, X3).
4. `WriteOffDecisionRecordWriter` against the stub, with the failed-write path (AC1, AC3, X1).
5. `ExceptionRowWriter` with the one transaction, the row state and the idempotency row (AC1, X7).
6. `CaseMoveAnswer` and the task raise with the four moves and the owner and service level as parameters (AC1, AC2, X4, X6).
7. `recordCorrection` with R-WO-44, R-WO-45 and R-WO-46, the three row states and the three moves (AC1).
8. `CorrectionController` with the rights, the `Idempotency-Key` and the problem mapping, and `WriteOffException` on SCR-27 through the composite route fake (AC1).
9. The boundary test: no statement outside `rwb_writeoff`, no `v_ace_*` read, no write to the data of rwb-case or rwb-decision or to the workspace tables (X8, BR3, BR4, BR5).

**Feature flag.** `rwb.writeoff.exception-v1`, a flag of the platform library; off means the raise holds the case at `POSTING_REJECTED`, writes nothing and raises no task, and the scan, pack, committee and posting stories are unaffected.

**Done when.** The tests of section 16 pass, R-WO-24 raises the exception and R-WO-44, R-WO-45 and R-WO-46 each write their state and their move on the fakes, a count below the limit raises nothing, a repeated decision writes once, a forced record failure changes nothing, the owner and the service level are read and not coded, no `recovery_case`, `task` or `assignment` write exists in the build, and SCR-27 answers through the composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required field of the correction request is absent, or the correction is not one of the three outcomes (X4) | Enter {field}. |
| MSG-P4-002 | A role without the Write-off and posting right calls the operation (X2) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the row and the answer change (X1) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-S7-001 | Not raised by this story: it is the message of the R-WO-03 scan hold, carried in the legacy message set of the key | The scan is on hold until Finance publishes the tax criteria. |

The four IDs are those of the legacy message set and of FSD S7 A2.12.3.1, and the text is the legacy and FSD wording, copied unchanged; no message is reworded and no new one is added. MSG-S7-001 stands in the set because the legacy table lists it for every S7 story, and no path of this story reaches it. VR-S7-012-2, "An action outside the role's permission", is the validation rule behind MSG-P4-002.

### 15. Screens and states

SCR-27 Write-off proposal, in its exception state, is served through the gateway-bff composite route (DP-19). The route calls rwb-writeoff for the write-off, its retry count, the limit in force, the rule and version and the three corrections, and rwb-case for the case, its route state and the open task; this story fixes the rwb-writeoff answers only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON.

The legacy screen table gives the states "Scan; proposed; in committee; approved" and names no exception state, while the routing logic gives the case `WRITEOFF_EXCEPTION` and the FSD rule table `A2.12` a correction path. The exception state is therefore this story's read-only addition to the screen, taken from the route state and not from a screen list, and the missing screen-state vocabulary is part of the gap recorded for the key (GAP-3039; ASM-5094). The scan state belongs to RWB-S7-E6013-APP, the proposed state to RWB-S7-E6015-APP, the in-committee state to RWB-S7-E6017-APP and the approved state to RWB-S7-E6018-APP. The refusal, not-recorded and refused-correction states read the messages of section 14. The empty, loading, error and no-access states of SCR-27 are not in Screen Specifications v1: Not specified in the source documents (CG-ALL-11145).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E6-024-01 | AC1 | Component | Case `RC-2026-000701` and write-off `WO-2026-000311` at `POSTING_REJECTED`; the raise, the record, the row state, the task and each of the three corrections asserted with the package version |
| TC-E6-024-02 | AC2 | Component | A retry count at the limit on the posting step's answer and a count below it; R-WO-24 asserted to raise once only, and the `WRITEOFF_EXCEPTION` move asserted on the fake |
| TC-E6-024-03 | AC3 | Component | The decision-record stub stopped; nothing written, no task raised and MSG-P7-003 shown |
| TC-E6-024-04 | Access | Component | A role without the Write-off and posting right A; 403 with MSG-P4-002 and no read; RW-WRITEOFF holding C and refused the decision |
| TC-E6-024-06 | Access | Component | A role without right A of the correction is refused with 403 and MSG-P4-002 before any read or write (AC4) |
| TC-E6-024-07 | Access | Component | A statement against recovery_case, task, assignment or another service schema is refused and fails the build (AC5) |
| TC-E6-024-08 | Data | Component | The decision record and the answer carry identifiers, a role code and an identity only (AC6) |
| TC-E6-024-09 | Flow | Component | Each of R-WO-44, R-WO-45 and R-WO-46 writes its state and its move on the fakes (AC7) |
| TC-E6-024-05 | Principle 5 | Component | A forced decision record write failure inside the transaction; no row state change and no case-move answer |
| TC-E6-024-13 | Contract §12 | Component | Each operation, event and activity of §12 checked against its contract element at the /v1 path; the names of §12.5 asserted on the fakes |
| TC-E6-024-14 | Boundary §12.7 (ASM-3438) | Component | Each table of §12.7 at its owner and its read boundary; nothing outside the owner read or written |
| TC-E6-024-10 | AC8 | Access | A caller without a valid credential, a role without the right and a write-off outside the route; 401, 403 and 404 with the platform error envelope and nothing written |
| TC-E6-024-11 | AC9 | Flow | The same Idempotency-Key sent twice; one record, one row state and one answer, with the repeat counted |
| TC-E6-024-12 | AC10 | Flow | The rwb-case fake not answering inside 2 s and its breaker open; 503 with the platform error envelope; nothing written and no case move answered |

The five legacy cases are those of RWB-E6-024 in their legacy order, with the Level column added: every case is tested on the fakes, so every case is `Component`. TC-E6-024-02 carries the raise that the legacy AC2 tests and the below-limit path that keeps the state from being opened; TC-E6-024-01 carries the working of the loop through the three corrections. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same ID; no `-ITG` copy is written by this story, and the cross-service journey belongs to the wave 4 harness.

### 17. Guardrails

- No business value in code: the retry limit, the loop's owner, the service level, the three correction outcomes and the row states stay data, reference data or the rule package, never a constant, a default or a branch.
- No personal data in `rwb_writeoff`, in a task parameter, a workflow input or a log: identifiers, an amount, dates, a state, a retry count and a rule version only, and every fixture is synthetic.
- ACE data only through the owner's contract: this service holds no `v_ace_*` grant and reads no ACE table, and a build that adds one fails the boundary test (BR3).
- The case, the task and the assignment stay with rwb-case: no `recovery_case`, `task` or `assignment` row and no case route-state column here (BR4).
- The money stays with rwb-payment and the posting with the posting step: this story records the decision to re-post and writes no posting, no reference and no ledger row.
- One base, one topic, one queue, one schema and one login per service; no document names another service's base or topic as its own (DP-13, DP-14).
- No retired element is reintroduced: no Quartz job row, no shared job table, no monolith base, no data-lake extract and no event published by this step.
- The decision is recorded before the change; a build that writes a row outside the record's transaction fails the review (DP-03).

### 18. Traceability

| Requirement ID | Requirement (short) | Story element | Test cases | Feature | L3 process |
|---|---|---|---|---|---|
| REQ-S7-004 | The write-off exception loop has one named owner and a time limit (FSD S7 Requirements served; Business Requirements Program v5 REQ-S7-004). The owner and the time limit are the two values no source supplies and this story carries as unconfirmed (GAP-3039; ASM-5093) | The raise, the task, the three corrections and the record | TC-E6-024-01, TC-E6-024-02, TC-E6-024-05 | FEAT-WOF-12 | Not specified in the source documents (DOR-RWB-S7-E6024-APP-2) |
| ADR-013 | 19 services inside ACE | rwb-writeoff as the owner of the exception state | TC-E6-024-01 | FEAT-WOF-12 | Not specified in the source documents (DOR-RWB-S7-E6024-APP-2) |
| ADR-014 | Schema and login per service | `rwb_writeoff` and its own login | TC-E6-024-01 | FEAT-WOF-12 | Not specified in the source documents (DOR-RWB-S7-E6024-APP-2) |
| ADR-016 | Reusable Temporal layer; Schedules replace Quartz | The exception step and the correction task inside `WriteOffWorkflow` | TC-E6-024-01 | FEAT-WOF-12 | Not specified in the source documents (DOR-RWB-S7-E6024-APP-2) |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The four consumed rows and the correction operation | TC-E6-024-01, TC-E6-024-04 | FEAT-WOF-12 | Not specified in the source documents (DOR-RWB-S7-E6024-APP-2) |
| ADR-022 | Local decision record plus central ledger | The record written before the change, twice in the loop | TC-E6-024-03, TC-E6-024-05 | FEAT-WOF-12 | Not specified in the source documents (DOR-RWB-S7-E6024-APP-2) |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E6-024, disposition Split (rework); feature FEAT-WOF-12 |
| Legacy criteria | AC1, AC2 and AC3, owned word for word by this story |
| Source text | Legacy RWB-E6-024; FSD S7 Write-off and recovery v3 A2.9, A2.12 and Requirements served; TSD S7 Write-off and recovery v2 T3, T4, T6 and T-A; Business Rules and Routing Logic v4 rows R-WO-24 and R-WO-44 to R-WO-46 and the States sheet; Epics 3 to 8 Specification v3 row FEAT-WOF-12 |
| Test cases | TC-E6-024-01 to TC-E6-024-05 |
| Feature and screens | FEAT-WOF-12, SCR-27 Write-off proposal and the case workspace task |
| Rules | R-WO-24, R-WO-44, R-WO-45 and R-WO-46, governed in rwb-decision |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-016, ADR-020, ADR-022 |

### 19. Out of scope

- The published shape of the correction operation, the `CorrectionRequest` and `WriteOffCorrection` elements, the field IDs, the consumed rows, the error set and the fakes: RWB-S7-E6024-CON.
- The posting to ALS and the general ledger, its retries, R-WO-21, R-WO-22, R-WO-23 and the re-post action of R-WO-44: RWB-S7-E6021-APP, with the money in rwb-payment (P8).
- The scan, the pack, the removal and the committee routing: RWB-S7-E6013-APP to RWB-S7-E6017-APP. The committee decision API-S7-002 and R-WO-15 to R-WO-17: RWB-S7-E6018-APP to RWB-S7-E6020-APP.
- The other two entries to `WRITEOFF_EXCEPTION`: R-WO-41 with RWB-S7-E6027-APP and R-WO-43 with RWB-S7-E6023-APP (ASM-5097).
- The case of record, its route states, the task, the assignment and the parent `CaseWorkflow`: rwb-case (P3); the WO package and its rule rows: rwb-decision (P7); the interaction ledger and its `CORRECTION` code: rwb-source-data (P1) by default ruling.
- The owner of the loop and its time limit, which REQ-S7-004 requires and no source names: carried as unconfirmed (ASM-5093).
- The gateway-bff composite route, the screen field list and the screen-state vocabulary of SCR-27: RWB-PLT-N001-CON and the edge stories.
- The cross-service journey of the legacy key and its evidence: the wave 4 harness, which copies none of these criteria.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
