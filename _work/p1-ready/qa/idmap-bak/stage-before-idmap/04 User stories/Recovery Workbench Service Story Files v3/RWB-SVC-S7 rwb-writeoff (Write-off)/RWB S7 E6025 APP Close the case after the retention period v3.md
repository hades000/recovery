# RWB-S7-E6025-APP Close the case after the retention period

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Version 3 changes** (D-RCV-60 P1 developer readiness, RD-P1 register)

- Start rule of `WriteOffWorkflow` / JOB-16: only the `AceDataReady` event with `sourceSystem` ALS and `status` COMPLETED counts; the event is published once per source system and business date (RD-P1-003, RD-P1-040).

| Item | Value |
|---|---|
| Story key | RWB-S7-E6025-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-writeoff |
| Service epic | RWB-SVC-S7 |
| Wave | 4 |
| Business epic | EP06 |
| Release | 30 April 2027 (tentative) |
| Legacy key | RWB-E6-025 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | L-S7-M |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-S7-E6025-APP-16) |
| Depends on (build) | RWB-S7-E6025-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | rwb-case and rwb-decision (class C, placeholders, GAP-3041) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S7 rwb-writeoff v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |
| Readiness decisions | RD-P1-003, RD-P1-040 |

**Change log.** D-RCV-60, 22 November 2026: the closure slice of RWB-E6-025 in rwb-writeoff. The four legacy criteria are kept word for word with their origin tag; the step evaluates R-WO-36 and R-WO-47 on the WO package in force, records the outcome through the local decision-record library before any change (DP-03), writes `write_off.state`, answers rwb-case with the moves `RETENTION_RUNNING` and `CASE_CLOSED` and stops the case timers, and its read on SCR-27 arrives through the gateway-bff composite route (DP-19) because the service keeps base `/api/recovery/writeoff/v1` (DP-13) and provides no operation of its own. The retention period length is not set in any source (DL26), the placement record has no column and no published owner operation, the closing entry names a loss no field carries, the plan's C and I rows are empty while the step consumes two services, and TSD S7 T4 does not print either rule (GAP-3041; ASM-5098, ASM-5100, ASM-5101, ASM-5102). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-S7-E6025-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (24 resolved, 20 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **Credit Administration officer** — and as the step the FSD gives no primary person, because it runs unattended — I want **the Workbench to close the case once the retention period has run and no action is open**, so that **write-offs follow the criteria and the committee's decision**.

This is the closure slice of legacy RWB-E6-025 (feature FEAT-WOF-13). It owns:

- the four legacy criteria (AC1 to AC4), copied verbatim with their origin tag, and the rules R-WO-36 and R-WO-47, the messages and the screen state they depend on;
- the retention branch of `WriteOffWorkflow` on task queue `rwb-writeoff` in namespace `rwb-recovery`, as the stage child of `CaseWorkflow` and as the last step of the write-off stage (context pack Temporal slides 5, 12 and 13);
- the evaluation of R-WO-36 and R-WO-47 against the WO package version in force, the retention timer they start and stop, and the hold of R-WO-48 when a document carries no retention class;
- the closing entry: one decision record per closure with the rule ID, the package version, cash recovered, loss and the two states, written **before** the case moves (DP-03);
- the write of `write_off.state` and the answer to rwb-case with the moves `RETENTION_RUNNING` and `CASE_CLOSED` and the stop of every case timer, so that the service that owns the case writes the case;
- the read-only closure state of SCR-27 Write-off proposal behind the gateway-bff composite route (DP-19), on the service base `/api/recovery/writeoff/v1` (DP-13); its no-access state is a 403 with MSG-P4-002 and no read (TC-E6-025-05), and its empty, loading and error states are Not specified in the source documents (DOR-RWB-S7-E6025-APP-10).

It does not own: the published shapes, the consumed rows, the state vocabulary this step adds, the error set and the fakes, which are RWB-S7-E6025-CON; the scan and the tax criteria (RWB-S7-E6013-APP, RWB-S7-E6014-APP); the pack, the removal and the routing (RWB-S7-E6015-APP to RWB-S7-E6017-APP); the committee decision and the posting (RWB-S7-E6018-APP to RWB-S7-E6021-APP); the reconciliation that also starts a retention timer under R-WO-42 (RWB-S7-E6023-APP); the payment on a closed case under R-WO-49 (RWB-S7-E6027-APP); the case of record, its route states, the `timer` rows and the parent `CaseWorkflow`, which are rwb-case (P3); the WO package and its 51 rules, which are rwb-decision (P7); and the deployment of this build, which is the operations story of this legacy key.

### 2. Business rationale

The feature objective, the problem and the metric are unchanged from the legacy story and the module FSD: the case closes once the retention period has run and no action is open, because write-off populations were assembled by hand each month (FSD S7 A1.3, A2.13.1), and the packs accepted first time are measured on the decision log and the Workbench records against a target that rises each month, reviewed monthly (FSD S7 A2.13.1). The requirement is REQ-S7-008, a case closes after its retention period and reopening it needs a written rule, a reason and an approver (Program BRD v4; FSD S7 Requirements served). What D-RCV-60 changes is who owns the case, the timer, the record and the screen.

- **The closure is this service's step.** `write_off` is S7's only table in `rwb_writeoff` (context pack ownership rows; TSD S7 T3.1), the WO route set of 51 rules over 27 states is the write-off stage's (TSD S7 T4), and R-WO-36 and R-WO-47 are the two transitions that end that stage.
- **The case stays with rwb-case.** `recovery_case`, the route states and the `timer` rows are P3's (legacy Data table lists both tables; context pack ownership rows), so this step evaluates the rules, writes its own row, records the entry and **answers** the two moves and the timer stop.
- **The retention period is not a constant.** No source sets its length: NFR-028, NFR-030 and NFR-031 are open under DL26, and REQ-S7-008 names the period without a value, so the period is reference data read with its version and the value stays a placeholder here (GAP-3041; ASM-5102).
- **The timer is a durable timer, not a scheduler row.** The two rules name the "Workbench scheduler", and in the target the stage waits on a Temporal durable timer inside `WriteOffWorkflow`; no Quartz row, no shared job table and no Schedule is created, and the only job of the service, JOB-16, is the monthly scan of R-WO-01 (ASM-5100).
- **Two ways in.** A case reaches `RETENTION_RUNNING` from `PLACED_WITH_AGENCY` on a placement whose term expired with nothing recovered (R-WO-36), or from `POSTED` when the approved and posted populations reconcile (R-WO-42, RWB-S7-E6023-APP). This step owns the first and the timer from both, and reads the second as an outcome it did not produce (ASM-5100).
- **Closure is a decision, so it is recorded.** Legacy AC1 asks for the result in the decision log with the rule version and legacy AC4 stops the action when the log cannot be written; the record is written through the local library in the same transaction as the move, so no case closes without its entry (DP-03).
- **The closing entry is the record, not a new table.** R-WO-47 asks for "cash recovered and loss"; no column of `write_off` carries a loss and `recovered_after` is the only recovered amount field, so the two amounts are attributes of the closing entry and their binding to a column is left open (GAP-3041; ASM-5103).
- **The hold is a document fact.** R-WO-48 holds the closure when a document on the case has no retention class and raises a Document Hub task; the class is rwb-document's and the task is P5's, so this step refuses the closure and changes nothing (GAP-3041).
- **Nothing leaves the service.** The connection matrix gives S7 REST and events to P1 and Temporal and events to P8, and no row to P9 or to a data lake; a closure is a case fact, so no event is published here (ASM-5099).

No business value moves: the period, the retention class, the states, the rule IDs and the package version are reference data and rule rows, read with their version and never written in code.

### 3. Preconditions

- RWB-S7-E6025-CON is published: the `write_off` element, the state values this step writes, the consumed rows, the closing-entry element, the rights, the error set and the fakes are baselined and handed to this story.
- The rwb-case case read is published with its fake: the case reference, the case number, the product group, the stage and the state `PLACED_WITH_AGENCY`, `RETENTION_RUNNING` or `CASE_CLOSED`. The operation name is Not specified in the source documents (GAP-3041; ASM-5098).
- The case-move answer of rwb-case is available for the fake: the moves `RETENTION_RUNNING` and `CASE_CLOSED` with the rule version. No source publishes an operation that moves a case state on behalf of a stage; on the workflow boundary the answer is the stage outcome the parent `CaseWorkflow` applies (GAP-3041; ASM-5098).
- The timer read and stop of rwb-case is available for the fake: the open timers of the case and their close. The `timer` rows are P3's, and the operation name is Not specified in the source documents (GAP-3041; ASM-5098).
- The rwb-decision rule-package read is published with its fake and answers the WO package at its version in force, with R-WO-36, R-WO-47 and R-WO-48 among its 51 rules over 27 states (GAP-3041; ASM-5005).
- The retention period and the retention classes are reference data with their version; no source sets a period, so the value is a placeholder at build time (GAP-3041; ASM-5102).
- RWB-PLT-E1027-CON is published with its writer fake: the local decision-record library writes in the caller's transaction, and a failed write stops the action with MSG-P7-003, so no move is answered and nothing changes (DP-03).
- RWB-PLT-N001-CON is published: SCR-27 reaches this service through the gateway-bff composite route, one hop, and no screen calls a service directly (DP-19).
- `write_off` exists in schema `rwb_writeoff` from the DB story of this service, with the columns of DF-FIN-010 to DF-FIN-020 and the standard record columns of TSD S7 T3.0; this story adds no table, no column and no migration.
- The service runs as its own login on schema `rwb_writeoff`; it holds no grant on another `rwb_*` schema and no `v_ace_*` grant, so a statement on `rwb_case`, on `recovery_case` or on an ACE view is refused by the database and fails the boundary test.
- No approval is needed to build against a Draft contract baseline; the contract is tagged by RWB-S7-E6025-CON when its tests pass.

### 4. Flow

1. A case reaches `RETENTION_RUNNING`: R-WO-36 fires from `PLACED_WITH_AGENCY` when the placement term has expired with `recovered_amount = 0`, or R-WO-42 has already published the reconciliation completeness of RWB-S7-E6023-APP (Business Rules and Routing Logic v4).
2. The retention branch of `WriteOffWorkflow` on queue `rwb-writeoff` starts on that signal and reads the package in force, the case and the open timers (DP-12; ASM-5100).
3. R-WO-36 closes the placement and starts the retention timer for the period of the reference data (placeholder). The timer is a durable timer of the workflow, not a job (ASM-5100, ASM-5102).
4. The step writes `write_off.state = RETENTION_RUNNING` and answers rwb-case with the same move; rwb-case writes the `recovery_case` row and parks the stage (ASM-5035).
5. The retention timer expires. `RetentionClosureEvaluator` tests R-WO-47: no open placement, no open sale, no open exception, and a retention class on every document.
6. Where a document carries no retention class, R-WO-48 holds the closure, the state stays `RETENTION_RUNNING`, the Document Hub task of P5 is raised by the document owner and this step changes nothing (X4).
7. Where every condition holds, the evaluator answers the rule ID, the package version, the action, the closing amounts and the move `CASE_CLOSED` (AC3).
8. `WriteOffDecisionRecordWriter` writes the closing entry **before any change**: the case reference, the write-off reference, the rule ID `R-WO-47` with its package version, cash recovered, loss, the from state, the to state and the closed-at time. A failed write stops the step with nothing changed (DP-03; legacy AC1 and AC4).
9. `CaseMoveAnswer` answers rwb-case with the move `CASE_CLOSED`; `TimerStopClient` closes every timer the case still holds. rwb-case writes its row, its state and its timers; this service writes none of them (ASM-5098, ASM-5035).
10. The step writes `write_off.state = CASE_CLOSED` in the same transaction as the entry, and publishes nothing (ASM-5099).
11. The officer reads the closed case and its closing entry on SCR-27 through the composite route, read only (DP-19).
12. A repeated timer expiry, or a resume after a worker restart, is idempotent: one entry, one move answer and one timer close per case, and a case that has left `RETENTION_RUNNING` answers 409 with no change.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The local decision record cannot be written | Nothing changes: no move is answered, `write_off.state` is unchanged and no timer is stopped | MSG-P7-003 | AC4, TC-E6-025-04, TC-E6-025-06 |
| X2 | The role does not hold the Write-off and posting right | 403 before any read or write; the unattended step runs under the service identity with the same check | MSG-P4-002 | AC5, TC-E6-025-05 |
| X3 | The retention period or the retention class reference data has no version in force | The step waits, the state is unchanged and the case stays at `RETENTION_RUNNING`; the closure is never taken on an unversioned period | None | AC1, AC3 |
| X4 | A document on the case carries no retention class | R-WO-48 holds the closure, the state stays `RETENTION_RUNNING`, the task to the document owner is raised and nothing is written | None | AC3 |
| X5 | An open placement, an open sale or an open exception exists at expiry | R-WO-47 does not fire, the case stays at `RETENTION_RUNNING` with a fresh timer and nothing is written | None | AC3 |
| X6 | The rwb-case or rwb-decision contract does not answer inside 2 s, or its breaker is open | The step retries on the workflow's own schedule; nothing is written and no move is answered; the caller sees 503 with the platform error envelope | None | AC1, AC3 |
| X7 | A repeated timer expiry, or a case that has left `RETENTION_RUNNING` | One entry and one answer; the repeat answers the outcome that exists, and a moved case is refused with 409 | None | AC1, AC3 |
| X8 | A component, a statement or a test reaches a `v_ace_*` view, a `recovery_case` row, a `timer` row or another service's schema | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | AC6, TC-E6-025-08 |

X1 is the legacy not-recorded path and X2 the legacy access path carried onto the slice; X3 to X7 are the paths the timer, the document class and the target call types add, and X8 is the ACE and schema boundary. X4 is the hold of R-WO-48, which no legacy criterion of this key covers.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-S7-E6025-CON, the rwb-case and rwb-decision fakes and the decision-record stub, on its own schema, and needs no live P1, P3 or P7 |
| Negotiable | The activity names and the closing-entry attribute names are this story's choice; the rules, the messages, the states, the period source and the screen are fixed |
| Valuable | A closed case is a closed case with its closing entry, its stopped timers and its recorded amounts, so no retention period runs on the books untracked |
| Estimable | One workflow branch, two rule evaluations, one record write, one row write, one case-move answer, one timer stop, three clients and one read-only screen state |
| Small | Finished inside two weeks with its tests on the fakes |
| Testable | Each criterion runs on a synthetic retained case through the contract fakes, plus the hold, the not-recorded, the access and the repeat cases |

### 7. Acceptance criteria

```gherkin
Feature: Close the case after the retention period

  Background:
    Given case "RC-2026-000884" is at the write-off stage with write-off "WO-2027-000402" in state "RETENTION_RUNNING"
    Given the WO rule package is in force at its version and carries R-WO-36, R-WO-47 and R-WO-48
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 Close the case after the retention period (legacy RWB-E6-025 AC1)
    Given the rwb-decision contract mock returns the WO package at its version in force with R-WO-47
    Given the rwb-case contract mock returns the case of record at "RETENTION_RUNNING" and accepts the move "CASE_CLOSED"
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then closes the case once the retention period has run and no action is open
    Then the system writes the result to the decision record with the rule version

  Scenario: AC2 Rule R-WO-36 (legacy RWB-E6-025 AC2)
    Given the rwb-case contract mock returns the case of record at "PLACED_WITH_AGENCY" and accepts the move "RETENTION_RUNNING"
    Given the rwb-decision contract mock returns the WO package at its version in force with R-WO-36
    Given a case in state PLACED_WITH_AGENCY
    When placement term expired
    Then close the placement and start the retention timer
    Then the case moves to RETENTION_RUNNING

  Scenario: AC3 Rule R-WO-47 (legacy RWB-E6-025 AC3)
    Given the rwb-case contract mock returns the case of record at "RETENTION_RUNNING" with no open placement, no open sale and no open exception, and accepts the move "CASE_CLOSED"
    Given the rwb-decision contract mock returns the WO package at its version in force with R-WO-47
    Given a case in state RETENTION_RUNNING
    When retention timer expired
    Then close the case, stop every timer and write the closing entry with cash recovered and loss
    Then the case moves to CASE_CLOSED

  Scenario: AC4 Not recorded (legacy RWB-E6-025 AC4)
    Given the decision record cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003

  Scenario: AC5 Access without the Write-off and posting right (X2) (new, D-RCV-60)
    Given the caller does not hold the Write-off and posting right
    When the closure is requested by that caller
    Then the caller sees 403 with MSG-P4-002 before any read or write

  Scenario: AC6 Schema and ACE boundary (X8) (new, D-RCV-60)
    Given a component, a statement or a test reaches a v_ace_* view, a recovery_case row, a timer row or another service's schema
    When the boundary test runs
    Then the grant refuses the statement, the build fails and nothing is released

  Scenario: AC7 Disallowed status transition (no legacy criterion) (new, D-RCV-60)
    Given the write-off is in state "RETENTION_RUNNING"
    When a move the state model does not allow is requested
    Then the move is refused and nothing is written

  Scenario: AC8 Rules BR1 to BR9 hold (no legacy criterion) (new, D-RCV-60)
    Given the rule rows BR1 to BR9 of section 8 are in force
    When the closure, the placement expiry and the retention expiry are evaluated
    Then each rule BR1 to BR9 holds as its row in section 8 states

  Scenario: AC9 Consumed contract does not answer inside 2 s (X6) (new, D-RCV-60)
    Given the rwb-case contract mock does not answer within 2 s
    When the retention expiry arrives
    Then the step retries on the workflow schedule, nothing is written and no move is answered
    Then the caller sees 503 with the platform error envelope

  Scenario: AC10 Consumed call fails or its breaker is open (X6) (new, D-RCV-60)
    Given the rwb-decision contract mock fails or its breaker is open
    When the retention expiry arrives
    Then nothing is written, no move is answered and the caller sees 503 with the platform error envelope
```

The four criteria AC1 to AC4 are the legacy criteria of RWB-E6-025 word for word, with their origin tag added and nothing else changed except the decision record wording (CG-ALL-11169) (AC5 to AC10 are this story's own, covering X2, X8, the disallowed status change, the BR1 to BR9 rules and the X6 timeout and failed call): the repeated `Then`, the wording of `its trigger arrives`, `placement term expired`, `retention timer expired` and `the decision record cannot be written` all stand. The cross-service parts are mocked, so AC1, AC2 and AC3 carry `Given the <service> contract mock returns <x>` lines, and those are the only additions; AC4 has no cross-service part and is copied with nothing added. What the legacy lines describe now happens in three places: rwb-case holds the case, its states and its timers, rwb-decision holds the package at its version, and this story evaluates the rules, writes `write_off.state`, writes the closing entry and answers the moves. The `decision log` of the legacy text is the local decision record of DP-03 in `rwb_writeoff`, with the central `decision_log_entry` ledger of rwb-decision behind it.

### 8. Business rules

| Rule | BR ID | Route set | Decision | From state | Event | Condition | Action | To state | Owner | Systems | Timer |
|---|---|---|---|---|---|---|---|---|---|---|---|
| R-WO-36 | BR10 | Write-off | D9 | PLACED_WITH_AGENCY | PLACEMENT_TERM_EXPIRED | ends_at passed and recovered_amount = 0 | Close the placement and start the retention timer | RETENTION_RUNNING | Workbench | Partner Portal, Workbench scheduler | None |
| R-WO-47 | BR11 | Write-off | D9 | RETENTION_RUNNING | RETENTION_TIMER_EXPIRED | no open placement, no open sale, no open exception, and a retention class on every document | Close the case, stop every timer and write the closing entry with cash recovered and loss | CASE_CLOSED | Workbench | Workbench scheduler, Document Hub, Decision Log | on expiry |

The two rows are the rows of the Business Rules and Routing Logic v4, copied character for character. Their owner and systems columns name a business role and systems, not services: "Workbench" is this service and its stage, the "Workbench scheduler" is the durable timer of `WriteOffWorkflow` and not a Quartz job, the "Partner Portal" is the agency placement fact that reaches the case, the "Document Hub" is rwb-document (P5) for the retention class and its task, and the "Decision Log" is the local record of DP-03 with the rwb-decision ledger behind it (ASM-5098, ASM-5100, ASM-5101). R-WO-48, the hold when a document carries no retention class, is the refusal of X4 and is evaluated here; R-WO-42, the reconciliation that also reaches `RETENTION_RUNNING`, is RWB-S7-E6023-APP's and is read, not written; R-WO-49, a payment on a closed case, is RWB-S7-E6027-APP's.

| ID | Rule | Source | Covered by |
|---|---|---|---|
| BR1 | The closure is the last transition of the write-off stage: it runs in `WriteOffWorkflow` on `rwb-writeoff` and writes `write_off.state` only | TSD S7 T3.1, T4; context pack ownership rows (table and workflow); FSD S7 A2.13.2 | AC3, TC-E6-025-03 |
| BR2 | The closing entry is recorded before the case moves, with the rule ID, the package version, cash recovered, loss and the two states; a failed write changes nothing and the caller sees MSG-P7-003 | DP-03; TSD S7 T2 ("writes the decision log entry before any change"); legacy AC1 and AC4 | AC1, AC4, TC-E6-025-01, TC-E6-025-04, TC-E6-025-06 |
| BR3 | Two rules close a stage and one holds it: R-WO-36 from `PLACED_WITH_AGENCY` on an expired placement term with nothing recovered, R-WO-47 from `RETENTION_RUNNING` on the expiry where nothing is open and every document has a retention class, R-WO-48 as the hold | Business Rules and Routing Logic v4 rows R-WO-36, R-WO-47 and R-WO-48; FSD S7 A2.13.3.1 | AC2, AC3, TC-E6-025-02, TC-E6-025-03 |
| BR4 | The move is answered, not written: `recovery_case`, its route states and the `timer` rows are rwb-case's, and this service answers `RETENTION_RUNNING` and `CASE_CLOSED` with the rule and its version and asks for the timer stop | ASM-5098, ASM-5035; TSD S7 T3.3 | AC2, AC3, TC-E6-025-02, TC-E6-025-03 |
| BR5 | No cross-schema join and no foreign key leaves `rwb_writeoff`; `case_id` and `decision_log_id` are identifiers of another service's fact | DP-01; TSD S7 T3.3 | AC6, TC-E6-025-08 |
| BR6 | ACE data only through the owner's contract: this service holds no `v_ace_*` grant and reads no ACE table, and the balance and the recovered amounts reach it on the case and the write-off of their owners | DP-05 as a prohibition; FSD S7 A1.1; TSD S7 T1 | AC6, TC-E6-025-08 |
| BR7 | Every value a business person may change is a rule row or reference data read with its version: the two rules, the states, the retention period, the retention classes and the package version | FSD S7 BR-S7-013; legacy Guardrails | AC1, AC3, TC-E6-025-01, TC-E6-025-03 |
| BR8 | The expiry is idempotent: one entry, one move answer and one timer close per case, and a case that has left `RETENTION_RUNNING` is refused with 409 | TSD S7 T-A.2; platform delivery rule (at least once, consumers idempotent) | AC1, AC3, TC-E6-025-01, TC-E6-025-03 |
| BR9 | No person name, address, contact value or identity number enters `rwb_writeoff`, the closing entry, a log or a workflow input; the case reference is a number and not an identity | Template and Rules §R7.2 (s17); TSD S7 T6.2 | AC6, TC-E6-025-08 |
| BR10 | R-WO-36 from `PLACED_WITH_AGENCY`: the placement is closed and the retention timer starts, as the rule row of the WO package says | Business Rules and Routing Logic v4 row R-WO-36; FSD S7 A2.13.3.1 | AC2, TC-E6-025-02 |
| BR11 | R-WO-47 from `RETENTION_RUNNING`: the case is closed, its timers stopped and its entry written, with R-WO-48 as the hold | Business Rules and Routing Logic v4 row R-WO-47; FSD S7 A2.13.3.1 | AC3, TC-E6-025-03 |

### 9. State transitions

The case route state is rwb-case's and is not changed by this story: the step answers the move and the parent `CaseWorkflow` applies it (BR4). What this story owns is the step, the row and the entry; the states it writes are the ones of the WO machine.

| From (case state, rwb-case) | Event | Condition | To | Written by |
|---|---|---|---|---|
| `PLACED_WITH_AGENCY` | `PLACEMENT_TERM_EXPIRED` | `ends_at` passed and `recovered_amount = 0` | `RETENTION_RUNNING` | rwb-case, on this story's answer (R-WO-36) |
| `PLACED_WITH_AGENCY` | `PLACEMENT_TERM_EXPIRED` | The term has not passed, or an amount was recovered | Unchanged | none; the placement keeps running |
| `POSTED` | `POPULATION_RECONCILED` | Approved and posted populations equal | `RETENTION_RUNNING` | rwb-case, on the answer of RWB-S7-E6023-APP (R-WO-42) |
| `RETENTION_RUNNING` | `RETENTION_TIMER_EXPIRED` | Nothing open and a retention class on every document | `CASE_CLOSED` | rwb-case, on this story's answer (R-WO-47) |
| `RETENTION_RUNNING` | `RETENTION_CLASS_MISSING` | A document on the case has no retention class | Unchanged | none; R-WO-48 holds the closure and P5 raises the task |
| `RETENTION_RUNNING` | `RETENTION_TIMER_EXPIRED` | An open placement, an open sale or an open exception exists | Unchanged | none; R-WO-47 does not fire and the timer restarts |
| `CASE_CLOSED` | `PAYMENT_RECEIVED_AFTER_CHARGEOFF` | A payment matches the closed case with no placement | `PAYMENT_MATCHED` | rwb-case, on the answer of RWB-S7-E6027-APP (R-WO-49) |

| Step execution | Event | Condition | To |
|---|---|---|---|
| Waiting | The stage enters `RETENTION_RUNNING` | The package in force is read and the period has a version | Timing |
| Timing | The durable timer fires | The period has run | Evaluating |
| Evaluating | R-WO-47 fires | Nothing open and every document has a retention class | Recording |
| Evaluating | R-WO-48 holds | A document has no retention class | Waiting, nothing changed |
| Recording | The entry is written and the answer sent | The transaction commits | Closed |
| Recording | The entry write fails | X1 | Waiting, nothing changed |

The states `PLACED_WITH_AGENCY`, `RETENTION_RUNNING` and `CASE_CLOSED` are those of the WO machine of the Business Rules and Routing Logic v4 and live on the case of record; this step writes `write_off.state` and none of the case columns.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| None; runs unattended | The primary actor of FSD S7 A2.13.3.3: the placement expiry and the retention expiry start the step |
| RW-CREDITAD, Credit Administration officer | Write-off and posting CRUA in TSD S7 T6.1: the role of the legacy story, reading the closure and its entry |
| RW-WOCOMM, write-off committee member; RW-PRODHEAD, product head; RW-FINANCE, Finance and CFO delegate | Write-off and posting RA: the other holders of right A on the write-off and posting area |
| RW-WRITEOFF, write-off team member | Write-off and posting CRU: holds right C and reads the closure |
| RW-FRAUD, RW-DEBTSALE, RW-CONDUCT, RW-RISK, RW-COE, RW-AUDIT, RW-BIANAL, RW-TRIBE | Write-off and posting R: read only, in scope |
| SY-CASEWF, SY-RULES, SY-AGENT, SY-DATALOAD | Write-off and posting R or U as the matrix gives it: the service identities run the step and are subject to the same checks |
| rwb-writeoff service identity | Evaluates the rules, writes the row and the entry, answers the moves and asks for the timer stop; it holds no grant on another schema and no `v_ace_*` grant |

The rights are the rows of TSD S7 T6.1 and nothing wider. The legacy permission table gives right A to RW-CREDITAD, RW-PRODHEAD, RW-WOCOMM and RW-FINANCE and right C to RW-WRITEOFF and RW-CREDITAD; the closure itself is unattended, so no operation of this story declares a user right. DP-08 is not in this story's pattern set: the capability area and the right are declared per operation of the service and the access guard is a service-template capability, so the check is stated here and not built here.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-FIN-010 | write_off (S7, `rwb_writeoff`) | id | Read, the write-off reference of the closing case |
| DF-FIN-011 | write_off (S7, `rwb_writeoff`) | case_id | Read, the case of the closure |
| DF-FIN-012 | write_off (S7, `rwb_writeoff`) | decision_log_id | Read, the record reference of the posting step; the closing entry is linked to it |
| DF-FIN-013 | write_off (S7, `rwb_writeoff`) | amount | Read, the balance written off; the loss is not bound to it by any source (ASM-5103) |
| DF-FIN-014 | write_off (S7, `rwb_writeoff`) | tax_criteria_met | Read, the result RWB-S7-E6014-APP wrote |
| DF-FIN-015, DF-FIN-016 | write_off (S7, `rwb_writeoff`) | committee_date, posted_date | Read only: set by the approval and the posting steps |
| DF-FIN-017 to DF-FIN-019 | write_off (S7, `rwb_writeoff`) | responsibility_center, cost_center, gl_product | Read only: GL values of the posting step |
| DF-FIN-020 | write_off (S7, `rwb_writeoff`) | recovered_after | Read, the recovered amount of the case; its use in the closing entry is Not specified in the source documents (GAP-3041; ASM-5103) |
| `state` (standard column) | write_off (S7, `rwb_writeoff`) | `state` | **Write**: `RETENTION_RUNNING` on R-WO-36 and `CASE_CLOSED` on R-WO-47 |
| Standard columns | write_off (S7, `rwb_writeoff`) | `version`, `updated_at`, `updated_by` | Write with the state, under the optimistic lock |
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library, created in `rwb_writeoff`) | rule id, rule version, decision code, cash recovered, loss, from and to state, closed at | Write through the local library, before the case moves |
| DF-WRK-027 to DF-WRK-036 | timer (P3) | id, case_id, task_id, timer_type, started_at, expires_at and 4 more | Not read as a table and not written: the timers are read and stopped on the rwb-case contract |
| DF-CAS-001 to DF-CAS-023 | recovery_case (P3) | id, case_no, product_group, status, stage_code, one personal-data field not carried, and 17 more | Not read as a table and not written: the state arrives on the contract and the move returns on its answer |
| DF-PRT-001 to DF-PRT-007 | partner (S9 / agency record) | id, partner_code, partner_name, partner_type, panel_status, contract_end and 1 more | Not read as a table: the placement facts arrive with the case and the placement read is unpublished (GAP-3041; ASM-5101) |
| DF-REF-001 to DF-REF-015 | rule_row (P7) | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | Not read as a table: the rule arrives on the package read |
| Retention period, retention class | reference data and parameters | The period of the retention timer and the class on a document | Read with their version; the period value is Not specified in the source documents (GAP-3041; ASM-5102) |

Field IDs are those of TSD S7 T3.1 and the Logical Data Model and Data Dictionary, and the case, timer, partner, ledger and rule rows are the rows the legacy Data table lists, with their owners changed to P3, S9 and P7 by the target. **No new table, no new column and no migration**: the table arrives with the DB story of this service, and `decision_record`, `idempotency_key` and `outbox_event` are library objects created in `rwb_writeoff` by the library's own migration (DP-03).

**No personal data.** The rows carry identifiers, amounts, dates, list values, a rule version and a state. No name, address, contact value or identity number enters `rwb_writeoff`, the entry, a log or a workflow input, and the fixtures are synthetic; the case's personal-data field is P3's and is never copied here, and the partner row's name is the agency's commercial name and is never copied either.

### 12. Contract

#### 12.1 REST operations provided

None. Owner rwb-writeoff (S7); base `/api/recovery/writeoff/v1` (DP-13). The closure is unattended and this story provides no operation. The two operations of this legacy key are other stories' of the same service: `POST /write-off-scans` (API-S7-001, right C) is RWB-S7-E6013-APP's and `POST /write-offs/{writeOffId}/committee-decision` (API-S7-002, right A) carries the committee outcomes at RWB-S7-E6018-APP to RWB-S7-E6020-APP. The read of the closure state behind SCR-27 is Not specified in the source documents and carries the placeholder (GAP-3041; ASM-5098).

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| The case read (operation name Not specified in the source documents (GAP-3041; ASM-5098)) | `/api/recovery/case/v1` | P3 rwb-case | The case reference, case number, product group, stage and state at `PLACED_WITH_AGENCY`, `RETENTION_RUNNING` or `CASE_CLOSED`; read only, faked |
| The case-move answer (operation name Not specified in the source documents (GAP-3041; ASM-5098)) | rwb-case (P3) | P3 rwb-case | The moves `RETENTION_RUNNING` and `CASE_CLOSED` with the rule ID, its version and the closing amounts; on the workflow boundary it is the stage outcome the parent `CaseWorkflow` applies; faked |
| The timer read and stop (operation name Not specified in the source documents (GAP-3041; ASM-5098)) | rwb-case (P3) | P3 rwb-case | The open timers of the case and their close, the `timer` rows of DF-WRK-027 to DF-WRK-036; faked |
| The rule-package read in force (operation name Not specified in the source documents (GAP-3041; ASM-5005)) | `/api/recovery/decision/v1` | P7 rwb-decision | The WO package at its version, with R-WO-36, R-WO-47 and R-WO-48 among its 51 rules over 27 states; faked |
| The placement read (operation name and owner Not specified in the source documents (GAP-3041; ASM-5101)) | rwb-case (P3) or the agency record's owner | The placement of `PLACED_WITH_AGENCY` with `ends_at` and `recovered_amount`; no source publishes the operation and the connection matrix gives S7 no row to rwb-partner (S9); faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The five rows are contract dependencies of class C that the plan does not carry, because this story's C row is None; the absence is recorded (GAP-3041; ASM-5098, ASM-5005, ASM-5101). Each row builds against the `/v1` of its path; no other contract version is specified in the source documents (DOR-RWB-S7-E6025-APP-23).

#### 12.3 Events published

None. The service publishes on `rwb.writeoff.events.v1` and its event set carries `WriteOffApproved` (`rwb.writeoff.WriteOffApproved.v1`, `EV-24`, with `writeOffId`, `caseId` and `amount`, consumed by Posting), and that event belongs to the approval and posting steps, which are RWB-S7-E6018-APP's and RWB-S7-E6021-APP's. A closure approves nothing, posts nothing and changes no amount, so this story declares no event, no producer group and no outbox row, and a build that publishes one fails the absence test. The topic carries the retry and `.dlt` topics of the platform (DP-14), and the outbox library of DP-09 is the dependency the plan does not carry for this key (ASM-5099).

#### 12.4 Events consumed

None. The service listens to the rwb-source-data and rwb-payment events in its scan and recovery steps (context pack connection matrix, row S7: REST and events to P1, Temporal and events to P8), and none belongs to the closure: the two triggers are the placement expiry and the retention expiry, which are timers of the stage. This story therefore holds no consumer group, no subscription and no inbox row, and a build that adds one fails the absence test (ASM-5099, ASM-5100).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `WriteOffWorkflow` | Workflow, one execution per case at the write-off stage, the child of `CaseWorkflow`, continues-as-new at each stage end | `rwb-writeoff` | Input: the case reference, the write-off reference and the package in force; signals: the placement expiry, the retention expiry and the case answered by rwb-case; outcome for the parent: the case move |
| `closeAfterRetention` | Activity, the one closure step, with R-WO-36, R-WO-47 and the R-WO-48 hold | `rwb-writeoff` | The case reference, the write-off reference, the package version and the period in; the rule ID with its version, the state, the record reference and the case move out, with the entry written before the answer |
| `retentionTimer` | Durable timer of the workflow, the wait of R-WO-36 and R-WO-47, not an activity and not a Schedule | `rwb-writeoff` | The period of the reference data with its version; the expiry is the event `RETENTION_TIMER_EXPIRED` |

No child workflow for the case and none for the money exists in this service, and the activity names are a target design choice fixed by no source document. The stage waits on the durable timer of the platform kit (L3 Scheduled job and the workflow timers of the kit), not on a scheduler row.

The start of `WriteOffWorkflow` is JOB-16 on the third working day after AceDataReady (R-WO-01) (counted only for the event with `sourceSystem` = `ALS` and `status` = `COMPLETED`, RD-P1-040), as the Temporal Catalog v1 Workflows row gives it. Its workflow ID form is Not specified in the source documents (CG-ALL-11165), and so is its duplicate-start policy (CG-ALL-11165).

#### 12.6 Schedules

None. The retention wait is a durable timer inside the workflow, not a Temporal Schedule, not a Quartz row and not a shared job table; the FSD declares the monthly scan as the module's only background event (FSD S7 A2.13.4.4) and JOB-16 is RWB-S7-E6013-APP's. DP-10 is not in this key's pattern set, and the "Workbench scheduler" of the two rules is read as the durable timer (ASM-5100).

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| write_off | S7 (`rwb_writeoff`) | The write-off of the balance on a case; this story writes its `state`, its lock version and its audit columns and reads the rest |
| decision_record | PLT library, created in `rwb_writeoff` | The local hash-linked closing entry (DP-03) |
| idempotency_key | PLT library, created in `rwb_writeoff` | The key of the repeated expiry and the outcome it holds |
| outbox_event | PLT library, created in `rwb_writeoff` | Present as a library object; this step writes no row to it (§12.3) |

Not owned and never read as a table: `recovery_case` and `timer` (P3), every `v_ace_*` view (P1), `decision_log_entry` and `rule_row` (P7), `partner` (S9), `document` (P5), `notice` (P6), `payment` (P8). No foreign key leaves the schema and `case_id` is an identifier, not a foreign key across schemas (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case case fake | `RC-2026-000884` at `PLACED_WITH_AGENCY`, at `RETENTION_RUNNING` with nothing open, at `RETENTION_RUNNING` with an open placement or sale or exception, and at `CASE_CLOSED` | AC1, AC2, AC3, X5 |
| rwb-case case-move fake | The moves `RETENTION_RUNNING` and `CASE_CLOSED` accepted with the rule and its version; a move refused because the case is not in the expected state | AC2, AC3, X7 |
| rwb-case timer fake | Two open timers of the case closed in one answer; a timer that is already closed; no answer beyond 2 s | AC3, X6 |
| rwb-decision rule-package fake | The WO package at its version in force with R-WO-36, R-WO-47 and R-WO-48 among its 51 rules over 27 states | AC1, AC2, AC3 |
| Placement fake | A placement with `ends_at` passed and `recovered_amount = 0`, and one with an amount recovered; the placement read carries the placeholder (GAP-3041; ASM-5101) | AC2, X5 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain, and a stopped chain | AC1, AC4, X1 |
| gateway-bff composite route fake | The merged SCR-27 answer for `RC-2026-000884` in its retention and its closed state | AC1 |

The fakes are test-only and are replaced by the real services in SIT. The operation names of the case read, the case-move answer, the timer read and stop, the package read and the placement read carry the placeholder until their owners confirm them (GAP-3041; ASM-5098, ASM-5005, ASM-5101).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 0 provided, 5 consumed | The case read, the case-move answer, the timer read and stop, the package read and the placement read; one hop, 2 s |
| Kafka | 0 published, 0 consumed | `WriteOffApproved` (`EV-24`) belongs to the approval and posting stories and no event is consumed here (§12.3, §12.4) |
| Temporal | 1 workflow, 1 activity and 1 durable timer | `WriteOffWorkflow`, its `closeAfterRetention` activity and the retention timer on `rwb-writeoff`; no Schedule |
| File | None | No file is read, built or delivered here |

### 13. Solution plan

**Package.** Java package `th.co.scb.ace.workbench.recovery.writeoff`, module `closure`; front end `src/modules/recovery/writeoff/WriteOffProposal.tsx`, the fragment SCR-27 embeds, read only for this story's state.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the transaction rule of the step: the entry and the move answer commit together or not at all. DP-13 fixes the base of the service and gives the closure no element of its own. DP-19 is how SCR-27 reaches the closure state, one hop through the gateway. These three are the whole pattern set of the key and the story adds no fourth: DP-04 (the embedded Drools kit), DP-09 (the outbox and inbox library), DP-10 (the scheduler row) and DP-05 (the ACE read) are real dependencies or markers of the stage that the plan does not hold, and they are recorded in the registers instead of the metadata table (GAP-3041; ASM-5005, ASM-5099, ASM-5100).

**Dependencies the tables add and the plan does not hold.** The five consumed rows are class C dependencies in fact and the plan's C row is None, so the story builds against their documents and fakes on Day 1. The Drools kit of DP-04 would add `RWB-PLT-E1072-CON`; the package is read as data and evaluated by this service's own evaluator, so no kit is declared. The outbox library of DP-09 would add `RWB-PLT-TE006-CON` and is needed only by the stories that publish. The plan's H row stands unchanged.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `WriteOffWorkflow` retention branch | Workflow | Receives the placement and retention expiries as signals, reads the package and the period in force, waits on the durable timer and reports the outcome to the parent |
| `closeAfterRetention` | Activity | Reads the case and its timers, evaluates R-WO-36 and R-WO-47 with the R-WO-48 hold, writes the row and the entry, sends the answer |
| `RetentionClosureEvaluator` | Service | The rule evaluation over the package in force: the two rules, the four closure conditions, the hold and the no-fire path |
| `WriteOffDecisionRecordWriter` | Library adapter | Writes the closing entry with the rule ID, the version and the two amounts before any change, hash-linked; refuses the step when the write fails |
| `CaseClient` | Client | The case read of rwb-case, one hop, 2 s, breaker, no retry of its own |
| `RulePackageClient` | Client | The WO package read of rwb-decision at its version in force |
| `CaseMoveAnswer` | Client | The `RETENTION_RUNNING` and `CASE_CLOSED` answers with the rule, its version and the amounts |
| `TimerStopClient` | Client | The timer read and stop of rwb-case, one hop, idempotent per timer |
| `PlacementClient` | Client | The placement facts of the case at `PLACED_WITH_AGENCY`; the read is a placeholder |
| `WriteOffProposal` | React component | Shows the case, its write-off and its closure entry on SCR-27, read only |

**Database and migrations.** No Flyway file. The `write_off` table arrives with the DB story of this service, and the record and idempotency key are library objects created in `rwb_writeoff` by the library's migration (DP-03). No column is added for the retention period, the loss or the placement: the period and the class are reference data, the loss is an attribute of the entry and the placement is another owner's fact (ASM-5101, ASM-5102, ASM-5103).

**Configuration and reference data.**

- R-WO-36, R-WO-47 and R-WO-48, their from and to states and the closure conditions: rule rows of the WO package with their version, never written in code (ASM-5005).
- The retention period of the timer and the retention classes of the documents: reference data with their version; no source sets a period (ASM-5102). Open decision DL26 holds the period; its assumptions are ASM-0247, ASM-0264, ASM-0275 and ASM-0355.
- The capability area "Write-off and posting" and its rights: access rows of rwb-access, read through the guard.
- The 2 s budget, the single hop and the breaker are the platform rule of ADR-020.
- Parameters and reference data: the retention period and the retention classes are read through the reference-data contract as parameters (DP-06, DP-07); the parameter key is Not specified in the source documents (DOR-RWB-S7-E6025-APP-20).

**Build steps**

1. The retention branch of `WriteOffWorkflow` and its input record, registered on `rwb-writeoff` as the stage child of `CaseWorkflow`, with the two expiries as signals and the durable timer between them.
2. `CaseClient` and `TimerStopClient` against their fakes, with the 2 s budget, the breaker, the open-timer path and the closed-timer path (AC1, AC3, X6).
3. `RulePackageClient` and `PlacementClient` against their fakes, with the version in force recorded with the outcome and the placement placeholder (AC1, AC2).
4. `RetentionClosureEvaluator` over the package, with R-WO-36, R-WO-47, the R-WO-48 hold, the four conditions and the no-fire path (AC2, AC3, X4, X5).
5. `WriteOffDecisionRecordWriter` against the stub, with the failed-write path (AC1, AC4, X1).
6. `CaseMoveAnswer` with the two moves and the amounts, and the write of `write_off.state` in the same transaction (AC2, AC3).
7. The read-only closure state of `WriteOffProposal` on SCR-27 through the composite route fake (AC1).
8. The boundary test: no statement outside `rwb_writeoff`, no `v_ace_*` read, no write to the case or timer tables of rwb-case or to any other service's schema (X8, BR4, BR5, BR6).

**Feature flag.** `rwb.writeoff.retention-closure-v1`, a flag of the platform library; off means the step takes no closure, the case stays at `RETENTION_RUNNING` and SCR-27 hides the closing entry, and the scan, the pack and the posting stories are unaffected.

**Done when.** The tests of section 16 pass, the step runs from a synthetic retained case in SIT, R-WO-36 moves a case to `RETENTION_RUNNING`, R-WO-47 closes it with its entry and its stopped timers, the R-WO-48 hold and an open dependency are refused, a repeated expiry writes once, a forced entry failure changes nothing, no `recovery_case` row, no `timer` row and no `v_ace_*` read exists in the build, and SCR-27 answers through the composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S7-001 | Carried from the legacy message set of RWB-E6-025: the scan is held for an absent tax criteria version (R-WO-03), so no case reaches the retention stage. Raised by RWB-S7-E6013-APP, not by this step | The scan is on hold until Finance publishes the tax criteria. |
| MSG-GEN-001 | A required value of the step is absent or invalid, for example a period with no version in force or a case with no reference (X3) | Enter {field}. |
| MSG-P4-002 | A role without the Write-off and posting right calls the service surface (X2) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The closing entry cannot be written before the case moves (X1, X6) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The four IDs are those of the legacy message set; the text is the legacy and FSD wording, copied unchanged, and no message is reworded and no new one is added. MSG-S7-001 is kept because the legacy table of RWB-E6-025 lists it. The hold of R-WO-48 raises no message of this service: it raises the Document Hub task of its owner (X4).

### 15. Screens and states

SCR-27 Write-off proposal, in its retention and its closed state, is served through the gateway-bff composite route (DP-19). The route calls rwb-writeoff for the write-off, its state and its closing entry, and rwb-case for the case and its route state; this story fixes the rwb-writeoff answers only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON.

The legacy screen table gives the states "Scan; proposed; in committee; approved". Those four are the earlier stories' of this key set; this story produces the two states after them: a retained case shows the retention timer running, its period and its class status, and a closed case shows the closure, its entry, cash recovered and loss and the closed-at time, read only. The scan state is RWB-S7-E6013-APP's, the proposed state RWB-S7-E6015-APP's, the committee states RWB-S7-E6017-APP to RWB-S7-E6020-APP's and the posted state RWB-S7-E6021-APP's. The hold, refused, not-recorded and unavailable states read the messages of section 14. The empty, loading and error states of SCR-27 are Not specified in the source documents (CG-ALL-11170); Screen Specifications v1 gives none of them.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E6-025-01 | AC1 | Component | A retained case at its expiry on the fakes; the entry, the state, the move answer and the closed case asserted |
| TC-E6-025-02 | AC2 | Component | A placement with `ends_at` passed and `recovered_amount = 0`; the placement closed, the timer started and `RETENTION_RUNNING` answered |
| TC-E6-025-03 | AC3 | Component | A retained case with nothing open and every document classed; the closure, the two stopped timers, the entry with cash recovered and loss and `CASE_CLOSED` |
| TC-E6-025-04 | AC4 | Component | The decision-record stub stopped; nothing written, no move answered and MSG-P7-003 shown |
| TC-E6-025-05 | AC5 | Component | A role without the Write-off and posting right; 403 with MSG-P4-002 and no read |
| TC-E6-025-06 | Principle 5 | Component | A forced decision record write failure inside the transaction; the case stays at `RETENTION_RUNNING` and no entry exists |
| TC-E6-025-07 | Contract (§12 operations, events and activities) | Component | The rwb-case, rwb-decision and rwb-writeoff operations, events and activities of section 12 on their published contracts, each answered by its fake; every status and field asserted |
| TC-E6-025-08 | AC6, BR5, BR6, BR9, X8 (§12.7 tables) | Component | The boundary test over the tables of section 12.7 and the build: no statement outside `rwb_writeoff`, no `v_ace_*` read, no write to `recovery_case` or `timer`, no personal data field; any hit fails the build |
| TC-E6-025-09 | AC7 | Component | Not specified in the source documents (NEWAC-RWB-S7-E6025-APP-AC10) |
| TC-E6-025-10 | AC8 | Component | The rule rows BR1 to BR9 of section 8 on the fakes; each rule's outcome asserted against its row |
| TC-E6-025-11 | AC9 | Component | The rwb-case fake not answering inside 2 s; the retry on the workflow schedule, no entry, no move answered, the state unchanged and 503 with the platform error envelope asserted |
| TC-E6-025-12 | AC10 | Component | The rwb-case or rwb-decision fake failing or its breaker open; nothing written, no move answered and 503 with the platform error envelope asserted |

The six legacy cases are those of RWB-E6-025 in their legacy order, with the Level column added: every case is tested on the fakes, so every case is `Component`, and the legacy level `System` maps to `Component` because the artefact under test is the step against its contract fakes. The hold of R-WO-48, the open-dependency path and the repeat are paths no legacy case names; they are asserted inside TC-E6-025-01 and TC-E6-025-03 with the fixtures of section 12.8; TC-E6-025-07 and TC-E6-025-08 are added for the contract and the boundary tests, and AC5 and AC6 cover X2 and X8, and AC7 covers the disallowed status change. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same ID; no `-ITG` copy is written by this story, and the cross-service journey belongs to the wave 4 harness.

### 17. Guardrails

- No business value in code: the two rules, R-WO-48, the states, the retention period, the retention classes, the closure conditions and the package version stay rule rows and reference data, never a constant, a default or a branch.
- No personal data in `rwb_writeoff`, in a workflow input or in a log: identifiers, amounts, dates, states and a rule version only, and every fixture is synthetic.
- ACE data only through the owner's contract: this service holds no `v_ace_*` grant and reads no ACE table, and a build that adds one fails the boundary test (BR6).
- The case and its timers stay with rwb-case: no `recovery_case` row, no `timer` row and no case state write here (BR4).
- The write-off row is written in one column only: `state` with its lock version and audit columns; no amount, no date and no GL value is set by a closure (BR1).
- The period is never hard-coded and never defaulted: a period with no version in force holds the step (X3, ASM-5102).
- One base, one topic, one queue, one schema and one login per service; no document names another service's base or topic as its own (DP-13, DP-14).
- No retired element is reintroduced: no shared job table, no Quartz row, no monolith base, no event published by this step, no `recovery_log` write and no data-lake path.
- The entry is written before the change; a build that answers the move outside the entry's transaction fails the review (DP-03).

### 18. Traceability

| Requirement ID | Requirement (short) | Story element | Test cases | Feature | L3 process |
|---|---|---|---|---|---|
| REQ-S7-008 | A case closes after its retention period, and reopening a closed case needs a written rule, a reason and an approver (Must, E6; FSD S7 Requirements served) | The closure of R-WO-36 and R-WO-47, the closing entry, the state and the two moves | TC-E6-025-01, TC-E6-025-02, TC-E6-025-03 | FEAT-WOF-13 | Not specified in the source documents (DOR-RWB-S7-E6025-APP-2) |
| NFR-031 | Case records carry a retention and archive rule by record class, and a case closes after its retention period (Open, DL26) | The retention class condition of R-WO-47 and the period of the timer | TC-E6-025-03 | FEAT-WOF-13 | Not specified in the source documents (DOR-RWB-S7-E6025-APP-2) |
| ADR-013 | 19 services inside ACE | rwb-writeoff as the owner of the write-off stage | TC-E6-025-01 | FEAT-WOF-13 | Not specified in the source documents (DOR-RWB-S7-E6025-APP-2) |
| ADR-014 | Schema and login per service | `rwb_writeoff` and its own login | TC-E6-025-01 | FEAT-WOF-13 | Not specified in the source documents (DOR-RWB-S7-E6025-APP-2) |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The five consumed rows with their budget and breaker | TC-E6-025-01 | FEAT-WOF-13 | Not specified in the source documents (DOR-RWB-S7-E6025-APP-2) |
| ADR-022 | Local decision record plus central ledger | The closing entry written before the case moves | TC-E6-025-04, TC-E6-025-06 | FEAT-WOF-13 | Not specified in the source documents (DOR-RWB-S7-E6025-APP-2) |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E6-025, disposition Split (rework); feature FEAT-WOF-13 |
| Legacy criteria | AC1 to AC4, owned word for word by this story |
| Source text | Legacy RWB-E6-025; FSD S7 Write-off and recovery v3 A1.3, A2.13, Requirements served and Screens; TSD S7 Write-off and recovery v2 T2, T3.1, T3.2, T4, T5.3, T6.1 and T-A; Business Rules and Routing Logic v4 rows R-WO-36, R-WO-47 and R-WO-48; Program BRD v4 REQ-S7-008, NFR-031 |
| Test cases | TC-E6-025-01 to TC-E6-025-06 |
| Feature and screens | FEAT-WOF-13, SCR-27 Write-off proposal |
| Rules | R-WO-36 and R-WO-47, with R-WO-48 as the hold, governed in rwb-decision |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-020, ADR-022 |

### 19. Out of scope

- The published shapes, the state values this step adds, the consumed rows, the closing-entry element, the error set and the fakes: RWB-S7-E6025-CON.
- The monthly scan and the tax criteria: RWB-S7-E6013-APP and RWB-S7-E6014-APP; the pack, the removal and the routing: RWB-S7-E6015-APP to RWB-S7-E6017-APP.
- The committee decision, the posting, the provision release and the Finance feed: RWB-S7-E6018-APP to RWB-S7-E6022-APP.
- The reconciliation that also reaches `RETENTION_RUNNING` under R-WO-42: RWB-S7-E6023-APP.
- The post charge-off placement, the agency recall and the sale of the population: RWB-S7-E6026-APP to RWB-S7-E6028-APP; the payment on a closed case under R-WO-49: RWB-S7-E6027-APP.
- The retention class of a document, its application to stored documents and the Document Hub task of R-WO-48: rwb-document (P5) and FEAT-DCM-17, the dependency the legacy header names; the retention applied on closure by FEAT-COM-08: rwb-comms (P6), which the connection matrix reaches from the case and not from this service.
- The case of record, its route states and the `timer` rows: rwb-case (P3); the WO package and its rule rows: rwb-decision (P7); the placement and the agency record: S9 rwb-partner, whose read no source publishes (GAP-3041; ASM-5101).
- The ACE data products: rwb-source-data (P1); the gateway-bff composite route and the screen field list of SCR-27: RWB-PLT-N001-CON and the edge stories.
- The cross-service journey of the legacy key and its evidence: the wave 4 harness, which copies none of these criteria.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
