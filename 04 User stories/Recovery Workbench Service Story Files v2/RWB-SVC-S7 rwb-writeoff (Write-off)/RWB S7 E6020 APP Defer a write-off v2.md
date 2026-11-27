# RWB-S7-E6020-APP Defer a write-off

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S7-E6020-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-writeoff |
| Service epic | RWB-SVC-S7 |
| Wave | 4 |
| Business epic | EP06 |
| Release | 30 April 2027 (tentative) |
| Legacy key | RWB-E6-020 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | L-S7-H |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-S7-E6020-APP-16) |
| Depends on (build) | RWB-S7-E6020-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S7 rwb-writeoff v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: the deferral slice of RWB-E6-020 in rwb-writeoff. The three legacy criteria are kept word for word with their origin tag; the step evaluates R-WO-17 from `WITH_COMMITTEE` on `COMMITTEE_DEFERRED` with `review_date` present and answers the move `DEFERRED`, refuses a defer with no review date under R-WO-18, sets the review timer and answers `SCAN_DUE` under R-WO-19 when the review date is reached, records every outcome through the local decision-record library before any change (DP-03), and serves the defer branch of the published `POST /write-offs/{writeOffId}/committee-decision` on base `/api/recovery/writeoff/v1` (DP-13) behind the gateway-bff composite route (DP-19). No source publishes a review-date property, field ID, column or list, the legacy `timer` table is rwb-case's in the target, and DP-04, DP-09 and DP-10 are absent from the plan's pattern set (GAP-3031; ASM-5059 to ASM-5058). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-S7-E6020-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (22 resolved, 14 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **write-off committee member (RW-WOCOMM)**, I want **the Workbench to let the committee defer with a review date, and hold the case until then**, so that **write-offs follow the criteria and the committee's decision**.

This is the deferral slice of legacy RWB-E6-020. It owns:

- the three legacy criteria (AC1, AC2, AC3), copied verbatim with their origin tag, and the rules, messages and screen state they depend on;
- one branch of `WriteOffWorkflow` on task queue `rwb-writeoff`, the stage child of `CaseWorkflow`, as one of the three decisions the committee takes on a case routed to it (context pack workflow row; Temporal and Drools Design slides 5, 12 and 13);
- the evaluation of R-WO-17 against the WO package version in force — from `WITH_COMMITTEE`, on `COMMITTEE_DEFERRED`, where `review_date` is present, the action is "Set the review timer and hold the case for the next scan" and the state is `DEFERRED` — and the refusal of R-WO-18 when the review date is absent (FSD S7 A2.8.3.1; Business Rules and Routing Logic v4);
- the review timer of R-WO-17 and its firing under R-WO-19, `DEFERRED` on `REVIEW_DATE_REACHED` to `SCAN_DUE`, which returns the case to the next monthly scan;
- the local decision record of the deferral and of the review-date return, written through RWB-PLT-E1027-CON before any change (DP-03), with the rule ID, the package version, the review date and the case move;
- the answer to rwb-case for `DEFERRED` and for `SCAN_DUE`, with the review date, the rule and its version, so that the case of record and its timer row are written by the service that owns them;
- the defer branch of the committee-decision operation of the module on base `/api/recovery/writeoff/v1` and the deferred state of SCR-27 Write-off proposal behind the gateway-bff composite route (DP-13, DP-19).

It does not own: the published shape of the operation, the `CommitteeDecision` and `DecisionLogEntry` elements, the review-date placeholder, the consumed rows, the error set and the fakes, which are RWB-S7-E6020-CON; the scan (RWB-S7-E6013-APP), the tax criteria (RWB-S7-E6014-APP), the pack (RWB-S7-E6015-APP), the removal (RWB-S7-E6016-APP) and the routing into committee (RWB-S7-E6017-APP); the approval inside the limit and the credit-committee escalation and rejection of R-WO-12 to R-WO-15 (RWB-S7-E6018-APP); the rejection of R-WO-16 (RWB-S7-E6019-APP); the posting and `WriteOffApproved` (RWB-S7-E6021-APP); the case of record, its route states and its timer row, which are rwb-case's (P3); the WO package and its 51 rules, which are rwb-decision's (P7); and the deployment of this build, which is the operations story of this legacy key.

### 2. Business rationale

The objective, the problem and the metric are unchanged from the legacy story and the module FSD: "Lets the committee defer with a review date, and holds the case until then" (FSD S7 A2.8.1), because write-off populations are assembled by hand each month (FSD S7 A1.3), and the measure is "Write-off packs accepted first time | Rising each month | Decision log and Workbench records | Monthly" (FSD S7 A2.8.1). What D-RCV-60 changes is who owns the case, the timer, the package and the decision.

- **The deferral is this service's step.** `write_off` is S7's only table in `rwb_writeoff` (context pack, ownership rows owned by S7; TSD S7 T3.1) and the WO route set of 51 rules over 27 states is the write-off stage's (TSD S7 T4); R-WO-17 and R-WO-19 are transitions of that stage and run here.
- **The case is not this service's.** `recovery_case` and every route state — `WITH_COMMITTEE`, `DEFERRED`, `SCAN_DUE` — are rwb-case's; this step evaluates the rules, records the decision and **answers** the move (ASM-5063).
- **The timer is not this service's row either.** The legacy Data table names `timer` with DF-WRK-027 to DF-WRK-036, and S7 owns one table only, so the timer row and JOB-05 TimerScheduler are rwb-case's; the review timer itself is a durable Temporal timer inside this service's stage workflow (ASM-5062).
- **The package is read, not embedded.** The WO route set is governed in rwb-decision, and DP-04 is not in this key's pattern set, so the package arrives on its read with the version in force and the version is recorded with the outcome (ASM-5064).
- **The decision is recorded first**, before the case leaves the committee state, which is what legacy AC1 asked for and legacy AC3 tested.
- **The review date is the condition.** R-WO-17 fires only where `review_date` is present and R-WO-18 sends an incomplete decision back to the committee; no source gives the review date a property, a field ID, a column or a list, and it is carried as an additive request property and recorded with the decision (ASM-5060).
- **A deferral approves nothing and writes nothing to `write_off`.** The deferral sets no `committee_date`, no `posted_date` and no GL column, so no column of the table is written and the hold lives in the record and in the timer (ASM-5065).
- **The requirement is shared.** REQ-S7-003 says the committee decision to approve, reject or defer is recorded against each account, so this slice carries the same requirement as the approve and reject stories and proves it here on its own (FSD S7 Requirements served; ASM-5066).

No business value moves: the review date rule, the two states, the timer durations, the rule ID and the package version are rule rows and reference data read with their version, never constants of the code.

### 3. Preconditions

- RWB-S7-E6020-CON is published: the defer branch of the committee-decision operation, the `CommitteeDecision` and `DecisionLogEntry` elements, the review-date placeholder, the consumed rows, the `Idempotency-Key` rule, the error set and the fakes are baselined and handed to this story.
- The rwb-case case read is published with its fake: the case reference, the case number, the product group, the stage and the state `WITH_COMMITTEE`. The operation name is Not specified in the source documents (GAP-3031; ASM-5063).
- The case-move answer of rwb-case is available for the fake: the move `DEFERRED` with the review date, and the move `SCAN_DUE` when the review date is reached. No source names a published operation that moves a case state on behalf of a stage; on the workflow boundary the answer is the stage outcome the parent `CaseWorkflow` applies (GAP-3031; ASM-5063).
- The rwb-case timer answer is available for the fake: the creation, or the cancellation, of the review timer row of DF-WRK-027 to DF-WRK-036. The operation name is Not specified in the source documents (GAP-3031; ASM-5062).
- The rwb-decision rule-package read is published with its fake and answers the WO package at its version in force, with R-WO-17, R-WO-18 and R-WO-19 among its 51 rules over 27 states (GAP-3031; ASM-5064).
- RWB-PLT-E1027-CON is published with its writer fake: the local decision-record library writes in the caller's transaction, and a failed write stops the action with MSG-P7-003, so no move is answered and nothing changes (DP-03).
- RWB-PLT-N001-CON is published: SCR-27 reaches this service through the gateway-bff composite route, one hop, and no screen calls a service directly (DP-19).
- `write_off` exists in schema `rwb_writeoff` from the DB story of this service, with the columns of DF-FIN-010 to DF-FIN-020 and the standard record columns of TSD S7 T3.0; this story adds no table, no column and no migration, and writes no column of it.
- The Temporal namespace `rwb-recovery` and the queue `rwb-writeoff` exist; a durable timer of the review date is a workflow timer, and the Scheduled job kit of DP-10 is not held by the plan for this key (GAP-3031; ASM-5062).
- The service runs as its own login on schema `rwb_writeoff`; it holds no grant on another `rwb_*` schema and no `v_ace_*` grant, so a statement on `rwb_case` or on an ACE view is refused by the database and fails the boundary test.
- No approval is needed to build against a Draft contract baseline; the contract is tagged by RWB-S7-E6020-CON when its tests pass.

### 4. Flow

1. RWB-S7-E6017-APP has routed the pack to the committee and the case sits at `WITH_COMMITTEE` (R-WO-11, R-WO-10); this story reads that outcome only (FSD S7 A2.5; TSD S7 T4).
2. The committee member opens SCR-27 Write-off proposal through the gateway-bff composite route and reads the case, its pack and the limit applied, one hop (DP-19).
3. The member defers the write-off and gives the review date. The review date is the one input R-WO-17 requires; the screen sends the write-off reference, the decision `defer` — the published member of the request's decision set (ASM-5061) — the review date, the member's identity and an `Idempotency-Key` (FSD S7 A2.8.2 step 2).
4. The deferral step of `WriteOffWorkflow` on queue `rwb-writeoff` receives the request as a signal to the running stage, with the package version read from rwb-decision in force (DP-12; ASM-5064).
5. The step reads the case on the rwb-case contract: the case reference, its product group, its stage and its state. A case that is not at `WITH_COMMITTEE` is refused with 409 and nothing is written (ASM-5063).
6. `CommitteeDecisionEvaluator` applies R-WO-17: from `WITH_COMMITTEE`, on `COMMITTEE_DEFERRED`, where `review_date` is present, the action is "Set the review timer and hold the case for the next scan" and the state is `DEFERRED`. Where the review date is absent, R-WO-18 refuses the decision and the case stays at `WITH_COMMITTEE` (FSD S7 A2.8.3.1; Business Rules and Routing Logic v4).
7. The evaluation answers the rule ID, the package version, the action of the rule, the review date and the case move the rule names.
8. `WriteOffDecisionRecordWriter` writes one decision record through the local decision-record library, **before any change**: the case reference, the write-off reference, the decision `defer`, the rule ID `R-WO-17` with its package version, the review date, the from state, the to state and the decided-at time. A failed write stops the step with nothing changed (DP-03; legacy AC1 and AC3).
9. `ReviewTimer` sets a durable Temporal timer for the review date inside the running `WriteOffWorkflow`; `CaseMoveAnswer` answers rwb-case with the move `DEFERRED`, the review date, the rule and its version, and rwb-case writes the `recovery_case` row and the `timer` row it owns. This service writes neither (ASM-5062, ASM-5063).
10. When the review date arrives, the timer fires in the same workflow execution, `CommitteeDecisionEvaluator` applies R-WO-19 — `DEFERRED` on `REVIEW_DATE_REACHED`, action "Return the case to the next monthly scan", state `SCAN_DUE` — a second record is written under R-WO-19 with its own version, and `CaseMoveAnswer` answers `SCAN_DUE` so the case re-enters the next cut-off of RWB-S7-E6013-APP.
11. A repeated request with the same `Idempotency-Key` answers the deferral it created and writes no second record, no second timer and no second answer; a decision on a case that has left `WITH_COMMITTEE` answers 409 with no change.
12. The member sees the deferral recorded with its review date, and the deferred case with its review date, read back from this service and from the case state of rwb-case, read only (DP-19).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The local decision record cannot be written | Nothing changes: no move is answered, no timer is set and the case stays at `WITH_COMMITTEE` | MSG-P7-003 | AC3, TC-E6-020-03, TC-E6-020-05 |
| X2 | The role does not hold the Write-off and posting right A | 403 before any read or write; nothing changes and no record is written | MSG-P4-002 | AC4, TC-E6-020-04, TC-E6-020-08 |
| X3 | The review date is absent on a defer | 422 and nothing is recorded; R-WO-18 refuses the decision and the case stays at `WITH_COMMITTEE` | MSG-GEN-001 | AC2, X4 |
| X4 | The case is not at `WITH_COMMITTEE`, or a decision has already been taken | 409 and nothing is written for that case; a decision is not taken twice | None | AC1, AC2 |
| X5 | The rwb-case or rwb-decision contract does not answer inside 2 s, or its breaker is open | The step retries on the workflow's own schedule; nothing is written, no timer is set and no move is answered; the caller sees 503 with the platform error envelope | None | AC1, AC2 |
| X6 | The case is still held in the scan for an absent tax criteria version or an absent ALS extract | No pack reached the committee, so no case is at `WITH_COMMITTEE` to decide; the hold is raised by RWB-S7-E6013-APP | MSG-S7-001 | AC1 |
| X7 | A repeated `Idempotency-Key`, or the same deferral taken twice | One record, one timer and one answer; the repeat answers the deferral that exists and is counted | None | AC1 |
| X8 | The review timer fires but the workflow has already left the deferral, or the case has moved off `DEFERRED` by another path | R-WO-19 does not fire, no record is written and the timer is not re-armed | None | AC2 |
| X9 | A component, a statement or a test reaches a `v_ace_*` view, a `recovery_case` row, a `timer` row or another service's schema | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | AC5, TC-E6-020-09, Section 17, BR5, BR6 |

X1 to X4 are the legacy exception paths carried onto the slice, X5 and X7 to X9 are the paths the target call types, the timer and the boundary add, and X6 is the held scan the legacy table carries. No source publishes a validation rule for a review date that is in the past or earlier than the next cut-off; the step refuses only an absent value, and the former is recorded as a gap rather than invented (GAP-3031; ASM-5060).

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-S7-E6020-CON, the rwb-case and rwb-decision fakes and the decision-record stub, on its own schema, and needs no live P1, P3 or P7 |
| Negotiable | The activity and component names, the decision code of the record and the shape of the stage outcome are this story's choice; the rules, messages, screen state, operation and two states are fixed |
| Valuable | A deferred case leaves the committee with its review date recorded and returns to the next scan by itself, so no case is written off against the committee's decision |
| Estimable | One workflow branch and one durable timer, one evaluator, one record write, two case-move answers, one timer answer, three clients and one read-only screen state |
| Small | Finished inside two weeks with its tests on the fakes |
| Testable | Each criterion runs on a synthetic in-committee case through the contract fakes, plus the access, missing-review-date, moved-case and failed-record cases |

### 7. Acceptance criteria

```gherkin
Feature: Defer a write-off

  Background:
    Given case "RC-2026-000732" is one of 40 cases in state "WITH_COMMITTEE" on the pack of the monthly write-off scan
    Given the WO rule package is in force at its version and carries R-WO-17, R-WO-18 and R-WO-19
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 Defer a write-off (legacy RWB-E6-020 AC1)
    Given the rwb-case contract mock returns the case of record at "WITH_COMMITTEE" and accepts the move "DEFERRED"
    Given the rwb-decision contract mock returns the WO package at its version in force with R-WO-17 and R-WO-19
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then lets the committee defer with a review date, and holds the case until then
    Then the system writes the result to the decision record with the rule version

  Scenario: AC2 Rule R-WO-17 (legacy RWB-E6-020 AC2)
    Given the rwb-case contract mock returns the case state "WITH_COMMITTEE" for "RC-2026-000732" and accepts the move "DEFERRED"
    Given a case in state WITH_COMMITTEE
    When committee deferred
    Then set the review timer and hold the case for the next scan
    Then the case moves to DEFERRED

  Scenario: AC3 Not recorded (legacy RWB-E6-020 AC3)
    Given the decision record cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003

  Scenario: AC4 A role without the Write-off and posting right A is refused before any read or write (new, D-RCV-60)
    Given a user whose role does not hold the Write-off and posting right A
    When the user submits a committee decision on case "RC-2026-000732"
    Then the system answers 403 with MSG-P4-002 and writes no record

  Scenario: AC5 A component reaching a v_ace view, a recovery_case row, a timer row or another service's schema is refused (new, D-RCV-60)
    Given a component, a statement or a test that reads a `v_ace_*` view, a `recovery_case` row, a `timer` row or another service's schema
    When the boundary test runs
    Then the grant refuses the statement, the boundary test fails the build and nothing is released

  Scenario: AC6 Each business rule of the deferral is held where section 8 places it (new, D-RCV-60)
    Given the rules BR1 to BR9 of section 8 are in force for the deferral
    When the deferral is run on the fakes
    Then the deferral runs in WriteOffWorkflow on rwb-writeoff, the decision record is written before the move, the moves are answered and not written, and no name, address, contact value or identity number enters the record

  Scenario: AC7 An error answer of the committee decision operation carries its contract status code (401, 403 or 404) (new, D-RCV-60)
    Given the committee decision operation is called with a request the contract does not accept
    When the operation answers
    Then the answer carries the status code of the contract (401, 403 or 404) and the platform error envelope

  Scenario: AC8 A timed-out consumed activity is retried on the workflow's schedule and writes nothing (new, D-RCV-60)
    Given the rwb-case contract does not answer inside 2 s
    When the activity runs
    Then the step retries on the workflow's own schedule, nothing is written, no timer is set and no move is answered

  Scenario: AC9 A consumed call that fails or does not answer leaves nothing changed (new, D-RCV-60)
    Given a consumed contract fails, does not answer inside 2 s or its breaker is open
    When the committee decision for the deferral is submitted
    Then nothing is written, no timer is set and no move is answered, and the caller sees the answer that section 5 X5 states

  Scenario: AC10 A status change the model does not allow is refused (new, D-RCV-60)
    Given case "RC-2026-000732" is at a state from which the model does not allow the move "DEFERRED"
    When the committee decision for the deferral is submitted
    Then the system refuses the move and the case stays in its state
```

The three criteria are the legacy criteria of RWB-E6-020 word for word, with their origin tag added and one wording change, `decision log` to `decision record` (CG-ALL-11037): the repeated `Then`, the wording of `the user acts on the screen`, `committee deferred` and `the action is taken` all stand, and `the decision record cannot be written` replaces `the decision log cannot be written`. The cross-service parts are mocked, so AC1 carries two `Given the <service> contract mock returns <x>` lines and AC2 one, and those are the only additions. What the legacy lines describe now happens in three places: rwb-case answers the case, writes the move and owns the timer row; rwb-decision holds the package with R-WO-17 to R-WO-19 at its version; and this story evaluates the rule, writes the record, sets the review timer and answers the move. The `decision log` of the legacy text is the local decision record of DP-03 in `rwb_writeoff`, with the central `decision_log_entry` ledger of rwb-decision behind it. The review timer is stated twice on purpose: R-WO-17 sets it and R-WO-19 fires it at the review date, and the second firing is the same story's (ASM-5062).

### 8. Business rules

| Rule | Route set | Decision | From state | Event | Condition | Action | To state | Owner | Systems | Timer |
|---|---|---|---|---|---|---|---|---|---|---|
| R-WO-17 | Write-off | D9 | WITH_COMMITTEE | COMMITTEE_DEFERRED | review_date present | Set the review timer and hold the case for the next scan | DEFERRED | Write-off team | Workbench scheduler, Committee View | to the review date |
| R-WO-19 | Write-off | D9 | DEFERRED | REVIEW_DATE_REACHED | Any | Return the case to the next monthly scan | SCAN_DUE | Write-off team | Workbench scheduler, Workbench | next cut-off |

The two rows are the rows of the Business Rules and Routing Logic v4, copied character for character; their rule IDs in the table below are BR10 (R-WO-17) and BR11 (R-WO-19). Their owner and systems columns name business roles and systems, not services: in the target "Workbench scheduler" is the durable Temporal timer of this stage workflow and the timer row of rwb-case, "Committee View" is the case of rwb-case and its route state read through the composite route, "Workbench" is SCR-27 and the scan of RWB-S7-E6013-APP, and "Write-off team" is the role set of the permission table below (ASM-5062, ASM-5065). R-WO-18, the refusal of a defer with no review date, is the refusal path of X3 and is named, not owned, here.

| ID | Rule | Source |
|---|---|---|
| BR1 | The deferral is a transition of the write-off stage: it runs in `WriteOffWorkflow` on `rwb-writeoff`, and no column of `write_off` records it | TSD S7 T3.1, T4; context pack ownership rows (table and workflow); FSD S7 A2.8.2 |
| BR2 | The decision is recorded before the case moves, with the rule ID, the package version, the decision, the review date and the two states; a failed write changes nothing and the caller sees MSG-P7-003 | DP-03; TSD S7 T2 ("writes the decision log entry before any change"); legacy AC1 and AC3 |
| BR3 | Only a case at `WITH_COMMITTEE` is decided, and a defer carries a review date: another state is refused with 409, and an absent review date is refused under R-WO-18 | Business Rules and Routing Logic v4 rows R-WO-17 and R-WO-18; FSD S7 A2.8.3.1 |
| BR4 | The moves are answered, not written: `recovery_case`, every route state and the `timer` row are rwb-case's, and this service answers `DEFERRED` with the review date and later `SCAN_DUE` | ASM-5063; TSD S7 T4 |
| BR5 | No cross-schema join and no foreign key leaves `rwb_writeoff`; `case_id` and `decision_log_id` are identifiers of another service's fact | DP-01; TSD S7 T3.3 |
| BR6 | ACE data only through the owner's contract: this service holds no `v_ace_*` grant and reads no ACE table, and the balance and the tax result reach it on the pack of RWB-S7-E6015-APP | DP-05 as a prohibition; FSD S7 A1.1; TSD S7 T1 |
| BR7 | Every value a business person may change is a rule row or reference data read with its version: R-WO-17 to R-WO-19, the two states, the review date and the package version | FSD S7 BR-S7-008; legacy Guardrails |
| BR8 | The review timer is durable and one per deferral: a repeated key re-arms nothing, and a firing after the case has left `DEFERRED` writes nothing | TSD S7 T-A.2; ASM-5062 |
| BR9 | No person name, address, contact value or identity number enters `rwb_writeoff`, the decision record, a log or a workflow input; `membersPresent` and the member's identity stay identifiers in the ledger | Template and Rules §R7.2 (s17); TSD S7 T6.2 |
| BR10 | R-WO-17: from `WITH_COMMITTEE` on `COMMITTEE_DEFERRED` with `review_date` present, set the review timer and hold the case for the next scan, moving it to `DEFERRED` | Business Rules and Routing Logic v4 row R-WO-17 |
| BR11 | R-WO-19: from `DEFERRED` on `REVIEW_DATE_REACHED`, return the case to the next monthly scan, moving it to `SCAN_DUE` | Business Rules and Routing Logic v4 row R-WO-19 |

### 9. State transitions

The case route state is rwb-case's and is not changed by this story: the step answers the move and the parent `CaseWorkflow` applies it (BR4). What this story owns is the step, the record and the timer.

| From (case state, rwb-case) | Event | Condition | To | Written by |
|---|---|---|---|---|
| `WITH_COMMITTEE` | `COMMITTEE_DEFERRED` | `review_date` present | `DEFERRED` | rwb-case, on this story's answer |
| `WITH_COMMITTEE` | `COMMITTEE_DEFERRED` | `review_date` absent | Unchanged | none; R-WO-18 refuses the decision and MSG-GEN-001 |
| `WITH_COMMITTEE` | `COMMITTEE_DEFERRED` | The case is not at `WITH_COMMITTEE` | Unchanged | none; 409 |
| `DEFERRED` | `REVIEW_DATE_REACHED` | Any, at the review date | `SCAN_DUE` | rwb-case, on this story's second answer (R-WO-19) |
| `DEFERRED` | A committee decision taken again | Not published | Unchanged | No row of TSD S7 T4 decides a case at `DEFERRED`; the deferral is closed by R-WO-19 (GAP-3031) |

| Step execution | Event | Condition | To |
|---|---|---|---|
| Waiting | A committee decision for a case of the pack | The package in force is read | Evaluating |
| Evaluating | R-WO-17 fires | The review date is present and the case is at `WITH_COMMITTEE` | Recording |
| Evaluating | R-WO-17 does not fire | The review date is absent, or the state is not the rule's | Waiting, nothing changed |
| Recording | The record is written, the timer set and the answer sent | The transaction commits | Deferred, waiting for the review date |
| Deferred | The durable timer fires at the review date | R-WO-19 applies and the case is at `DEFERRED` | Waiting, `SCAN_DUE` answered and a second record written |
| Recording or Deferred | The record write fails | X1 | Waiting, nothing changed |

The states `WITH_COMMITTEE`, `DEFERRED` and `SCAN_DUE` are those of the WO machine of TSD S7 T4 and live on the case of record; this step writes none of them. `SCAN_DUE` is where the scan story RWB-S7-E6013-APP picks the case up again at the next cut-off.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-WOCOMM, write-off committee member | Write-off and posting RA in TSD S7 T6.1: the primary role of FSD S7 A2.8.3.3, deferring a case inside the committee and reading the deferral back |
| RW-CREDITAD, Credit Administration officer | Write-off and posting CRUA: defers a case, sets a review date and reads the record |
| RW-PRODHEAD, product head; RW-FINANCE, Finance and CFO delegate | Write-off and posting RA: the other two roles the legacy permission table gives right A on the committee decision |
| RW-WRITEOFF, write-off team member | Write-off and posting CRU: the owner R-WO-17 and R-WO-19 name in the rule rows; reads the deferred population and its review dates, and does not hold right A |
| RW-FRAUD, RW-DEBTSALE, RW-CONDUCT, RW-RISK, RW-COE, RW-AUDIT, RW-BIANAL, RW-TRIBE | Write-off and posting R: read only, in scope |
| SY-CASEWF, SY-RULES, SY-AGENT, SY-DATALOAD | Write-off and posting R or U as the matrix gives it: the service identities run the step and are subject to the same checks |
| rwb-writeoff service identity | Evaluates R-WO-17 to R-WO-19, writes the records, sets the durable timer, answers both moves and serves the operation; it holds no grant on another schema and no `v_ace_*` grant |

The rights are the rows of TSD S7 T6.1 and nothing wider, and the right the deferral needs is A — the right the legacy permission table gives to RW-CREDITAD, RW-PRODHEAD, RW-WOCOMM and RW-FINANCE and the right TSD S7 T-A.2 declares on API-S7-002. The rule rows name "Write-off team" as the owner of the deferral and of the return ticket; that is the business owner of the stage, and the role that may act is the one holding right A (ASM-5065). DP-08 is not in this story's pattern set: the capability area and the right are declared per operation and the guard is a service-template capability, so the check is stated here and not built here: the rwb-access authorise check on `POST /write-offs/{writeOffId}/committee-decision` tests the capability area "Write-off and posting" and right A before any read or write, and its request contract is Not specified in the source documents (DOR-RWB-S7-E6020-APP-6).

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-FIN-010 | write_off (S7, `rwb_writeoff`) | id | Read, the write-off reference the operation takes as `writeOffId` |
| DF-FIN-011 | write_off (S7, `rwb_writeoff`) | case_id | Read, the case of the decision |
| DF-FIN-012 | write_off (S7, `rwb_writeoff`) | decision_log_id | Read, the record reference the pack and routing steps set; the new record links to it |
| DF-FIN-013 | write_off (S7, `rwb_writeoff`) | amount | Read, the amount the committee has in front of it; a deferral changes no amount |
| DF-FIN-014 | write_off (S7, `rwb_writeoff`) | tax_criteria_met | Read, the result RWB-S7-E6014-APP wrote |
| DF-FIN-015 | write_off (S7, `rwb_writeoff`) | committee_date | Not written here: no committee date is set by a deferral; RWB-S7-E6018-APP sets it on approval |
| DF-FIN-016 to DF-FIN-019 | write_off (S7, `rwb_writeoff`) | posted_date, responsibility_center, cost_center, gl_product | Not written here: RWB-S7-E6021-APP |
| DF-FIN-020 | write_off (S7, `rwb_writeoff`) | recovered_after | Not written here: the recovery stories |
| Standard columns | write_off (S7, `rwb_writeoff`) | `is_active`, `state`, `version`, `created_at`, `created_by`, `updated_at`, `updated_by` | Not written: this step reads the row and writes no column of it |
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library, created in `rwb_writeoff`) | rule id, rule version, decision code, inputs reference, review date, from and to state, decided at | Write through the local library, before the case moves |
| DF-WRK-027 to DF-WRK-036 | timer (P3) | id, case_id, task_id, timer_type, started_at, expires_at and 4 more | Not read as a table and not written: the timer row is created and cancelled by rwb-case on this story's answer (ASM-5062) |
| DF-CAS-001 to DF-CAS-023 | recovery_case (P3) | id, case_no, product_group, primary_person_key, status, stage_code and 17 more | Not read as a table and not written: the state arrives on the rwb-case contract |
| DF-REF-001 to DF-REF-015 | rule_row (P7) | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | Not read as a table: the rules arrive on the package read |
| `review_date` | the condition of R-WO-17 and R-WO-18 | Read as a request input and recorded in the decision record and in the case-move answer; the property, the field ID, the column and the list are Not specified in the source documents (GAP-3031; ASM-5060) |

Field IDs are those of TSD S7 T3.1 and the Logical Data Model and Data Dictionary, and the case, timer, ledger and rule rows are the rows the legacy Data table lists, with their owners changed to P3 and P7 by the target. **No new table, no new column and no migration**: the table arrives with the DB story of this service, this story writes none of its columns, and `decision_record` and `idempotency_key` are library objects created in `rwb_writeoff` by the library's own migration (DP-03). `outbox_event` sits in the schema as a library object and this step writes no row to it because it publishes no event (§12.3).

**No personal data.** The rows carry identifiers, amounts, dates, a rule version, a review date and a state. No name, address, contact value or identity number enters `rwb_writeoff`, the record, a log or a workflow input, and the fixtures are synthetic. `membersPresent` is a list of member identifiers in the ledger and is not copied here; `primary_person_key` is P3's and is never copied here.

### 12. Contract

Contract version: v1, base `/api/recovery/writeoff/v1`, fixed for this story (DOR-RWB-S7-E6020-APP-23).

#### 12.1 REST operations provided

Owner rwb-writeoff (S7); base `/api/recovery/writeoff/v1` (DP-13). This story supplies the defer branch of the committee-decision operation, whose shape RWB-S7-E6020-CON declares.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| POST | `/write-offs/{writeOffId}/committee-decision` (API-S7-002) | `CommitteeDecision` in with the decision `defer` and the review date, `DecisionLogEntry` out with the rule `R-WO-17` and its version, the review date and the state `DEFERRED` | Write-off and posting, right A, scope applied | `Idempotency-Key` header |

The errors are 400, 401, 403 with MSG-P4-002, 404 for a write-off that is not in the pack, 409 for a case that has left `WITH_COMMITTEE`, 422 with MSG-GEN-001 for an absent review date under R-WO-18 and 503 when the library or a consumed contract does not answer. TSD S7 T-A.1 publishes the operation as API-S7-002 with the request `CommitteeDecision`, the answer `DecisionLogEntry`, the right A and the error set 401, 403, 404, 409, 422 and 503, so the operation needs no placeholder; the review date has no property in the published request and is the declared placeholder (§11; GAP-3031; ASM-5059, ASM-5060). The same operation serves the approval and the rejection, which are RWB-S7-E6018-APP's and RWB-S7-E6019-APP's, and the scan is RWB-S7-E6013-APP's; none of the three is built or declared here.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| The case read (operation name Not specified in the source documents (GAP-3031; ASM-5063)) | `/api/recovery/case/v1` | P3 rwb-case | The case reference, case number, product group, stage and state of the case at `WITH_COMMITTEE`; read only, faked |
| The case-move answer (operation name Not specified in the source documents (GAP-3031; ASM-5063)) | rwb-case (P3) | P3 rwb-case | The move `DEFERRED` with the review date and the rule version, and later `SCAN_DUE` under R-WO-19; on the workflow boundary it is the stage outcome the parent `CaseWorkflow` applies; faked |
| The review-timer answer (operation name Not specified in the source documents (GAP-3031; ASM-5062)) | rwb-case (P3) | P3 rwb-case | The creation and the cancellation of the `timer` row of the review date, which rwb-case owns; faked |
| The WO rule-package read in force (operation name Not specified in the source documents (GAP-3031; ASM-5064)) | `/api/recovery/decision/v1` | P7 rwb-decision | The WO package at its version, with R-WO-17, R-WO-18 and R-WO-19 among its 51 rules over 27 states; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The four rows are contract dependencies of class C that the plan does not carry, because this story's C row is None; the absence is recorded (GAP-3031; ASM-5062, ASM-5063, ASM-5064).

#### 12.3 Events published

None. The service publishes on `rwb.writeoff.events.v1` and its event set carries `WriteOffApproved` (`EV-24`, with `writeOffId`, `caseId` and `amount`, consumed by Posting), which belongs to the posting step of R-WO-20 and R-WO-21, declared by RWB-S7-E6021-APP. A deferral approves nothing, posts nothing and changes no amount, so this story declares no event, no producer group and no outbox row, and a build that publishes one fails the absence test. The topic carries the retry and `.dlt` topics of the platform (DP-14), and the outbox and inbox library that relays it is the DP-09 dependency the plan does not carry for this key (ASM-5065).

#### 12.4 Events consumed

None. The service listens to the rwb-source-data and rwb-payment events in its scan and recovery steps (context pack connection matrix, row S7), and none belongs to the deferral: a deferral reads no ACE extract and moves no money. The review date is a workflow timer and not an event, so this story holds no consumer group, no subscription and no inbox row, and a build that adds one fails the absence test. The trigger of the step is the committee member's decision on SCR-27 through the composite route; the FSD declares no background event for the feature (FSD S7 A2.8.4.4).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `WriteOffWorkflow` | Workflow, one execution per case at the write-off stage, the child of `CaseWorkflow`, continues-as-new at each stage end | `rwb-writeoff` | Input: the case reference, the cut-off date and the package in force; signals: the committee decision and the case answered by rwb-case; the durable review timer of R-WO-17; outcome for the parent: the case move |
| `recordCommitteeDeferral` | Activity, the deferral step, with R-WO-17, the R-WO-18 refusal and the R-WO-19 firing | `rwb-writeoff` | The case reference, the decision `defer`, the review date and the package version in; the rule ID with its version, the decision recorded, the timer set and the case move out, with the record written before the answer |
| `ReviewTimer` | Durable workflow timer | `rwb-writeoff` | Armed with the review date of R-WO-17 and fired once; it wakes the same execution for R-WO-19 and is cancelled if the case leaves `DEFERRED` by another path |

No child workflow for the case and none for the money exists in this service. The activity name and the timer component are target design choices fixed by no source document, and the review timer is not a Temporal Schedule (ASM-5062).

Workflow ID form: Not specified in the source documents (CG-ALL-11033). Start rule: on the third working day after AceDataReady (R-WO-01), JOB-16 in Temporal Catalog v1. Duplicate-start policy: Not specified in the source documents (CG-ALL-11033).

#### 12.6 Schedules

None. The deferral is a member-driven step, and the review timer is a durable timer inside the workflow execution, not a Schedule. `JOB-16`, the write-off scan, becomes the Temporal Schedule of R-WO-01 in RWB-S7-E6013-APP, and `JOB-05` Timer check, which implements TimerScheduler for every caller (Batch and Scheduling Design v5, JOB-05), is rwb-case's and creates and cancels the timer rows that this story's answers name (ASM-5062). No Quartz row, no shared job table and no batch table is declared, built or re-registered here.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| write_off | S7 (`rwb_writeoff`) | The write-off of the balance on a case; this story reads the row of the decision and writes none of its columns |
| decision_record | PLT library, created in `rwb_writeoff` | The local hash-linked decision record of the deferral and of the review-date return (DP-03) |
| idempotency_key | PLT library, created in `rwb_writeoff` | The key of the repeated request and the answer it holds |
| outbox_event | PLT library, created in `rwb_writeoff` | Present as a library object; this step writes no row to it (§12.3) |

Not owned and never read as a table: `recovery_case` and `timer` (P3), every `v_ace_*` view (P1), `decision_log_entry` and `rule_row` (P7), `document` (P5), `notice` (P6), `payment` (P8). No foreign key leaves the schema and `case_id` is an identifier, not a foreign key across schemas (DP-01). The review date has no column in `write_off` and is held by the record and by the timer (GAP-3031; ASM-5060).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case case fake | The case of record at `WITH_COMMITTEE` with its pack and limit, `RC-2026-000732` among 40 cases; a case that has moved; a case that is not in the pack | AC1, X4 |
| rwb-case case-move fake | The move `DEFERRED` accepted with the review date and the rule version, the move `SCAN_DUE` accepted at the review date, and a move refused | AC1, AC2, X4, X8 |
| rwb-case review-timer fake | A `timer` row created for the review date and cancelled on R-WO-19; a case that is no longer at `DEFERRED` | AC2, X8 |
| rwb-decision rule-package fake | The WO package at its version in force with R-WO-17, R-WO-18 and R-WO-19 among its 51 rules over 27 states | AC1, AC2 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and outbox, and a stopped chain | AC3, X1 |
| gateway-bff composite route fake | The merged SCR-27 answer for `RC-2026-000732`, in its in-committee and deferred states | AC1 |

The fakes are test-only and are replaced by the real services in SIT. The operation names of the case read, the two case-move answers, the review-timer answer and the package read carry the placeholder until their owners confirm them (GAP-3031; ASM-5062, ASM-5063, ASM-5064).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 4 consumed | The committee-decision operation on `/api/recovery/writeoff/v1` (defer branch); the case read, the case-move answers, the review-timer answer and the package read; one hop, 2 s |
| Kafka | 0 published, 0 consumed | `WriteOffApproved` (`EV-24`) belongs to RWB-S7-E6021-APP, and no event is consumed here (§12.3, §12.4) |
| Temporal | 1 workflow, 1 activity and 1 durable timer | `WriteOffWorkflow`, `recordCommitteeDeferral` and `ReviewTimer` on `rwb-writeoff`; no Schedule |
| File | None | No file is read, built or delivered here |

### 13. Solution plan

**Package.** Java package `th.co.scb.ace.workbench.recovery.writeoff`, module `committee`; front end `src/modules/recovery/writeoff/WriteOffProposal.tsx`, the fragment SCR-27 embeds, read only for this story's state.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the transaction rule of the step: the record and the answer commit together or not at all. DP-13 moves the base of the legacy paths and gives the defer branch its home. DP-19 is how SCR-27 reaches this service, one hop through the gateway. These three are the whole pattern set of the key and the story adds no fourth: DP-04 (the embedded Drools kit), DP-05 (the ACE read), DP-09 (the outbox and inbox library) and DP-10 (the scheduler kit) are real dependencies of the stage that the plan does not hold, and they are recorded in the registers instead of the metadata table (GAP-3031; ASM-5062, ASM-5064, ASM-5065).

**Dependencies the tables add and the plan does not hold.** The four consumed rows are class C dependencies in fact and the plan's C row is None, so the story builds against their documents and fakes on Day 1. The Drools kit of DP-04 would add `RWB-PLT-E1072-CON`; the package is read as data and evaluated by this service's own evaluator, so no kit is declared. The outbox library of DP-09 would add `RWB-PLT-TE006-CON` and is needed only by the stories that publish. The scheduler kit of DP-10 would add `RWB-PLT-E1071-CON`; a durable workflow timer needs no Schedule, so it is not declared. The plan's H row stands unchanged.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `WriteOffWorkflow` deferral branch | Workflow | Receives the committee decision as a signal, reads the package in force, arms the review timer and reports each outcome to the parent |
| `recordCommitteeDeferral` | Activity | Reads the case, applies R-WO-17 with the R-WO-18 refusal and R-WO-19 at the review date, writes the record and sends the answers |
| `CommitteeDecisionEvaluator` | Service | The rule evaluation over the package in force, with the defer branch, the review-date test, the state test and the no-fire path |
| `ReviewTimer` | Workflow timer | Holds the review date durably and wakes the execution once for R-WO-19; cancelled when the case leaves `DEFERRED` |
| `WriteOffDecisionRecordWriter` | Library adapter | Writes the record with the rule ID and the version before any change, hash-linked; refuses the step when the write fails |
| `CommitteeDecisionController` | Controller | The committee-decision operation with its defer branch, the capability area and right A, the `Idempotency-Key` and the problem mapping |
| `CaseClient` | Client | The case read of rwb-case, one hop, 2 s, breaker, no retry of its own |
| `RulePackageClient` | Client | The WO package read of rwb-decision at its version in force |
| `CaseMoveAnswer` | Client | The `DEFERRED` answer with the review date and the `SCAN_DUE` answer at the review date |
| `ReviewTimerClient` | Client | The timer creation and cancellation answer to rwb-case, which owns the `timer` row |
| `WriteOffProposal` | React component | Shows the deferred case and its review date on SCR-27, read only |

**Database and migrations.** No Flyway file. `write_off` arrives with the DB story of this service, and the record and idempotency key are library objects created in `rwb_writeoff` by the library's migration (DP-03). No column is added for the review date, the decision or the case state: the review date is a record input, the state and the timer row are facts and rows of rwb-case (ASM-5060, ASM-5063).

**Configuration and reference data.**

- R-WO-17, R-WO-18 and R-WO-19, their from and to states and the review-date condition: rule rows of the WO package with their version, never written in code (ASM-5064).
- The review date itself: a date the committee chooses, validated as present and recorded with the decision; no source publishes a list, a range or a rule for a past date (ASM-5060).
- The capability area "Write-off and posting" and its rights: access rows of rwb-access, read through the guard.
- The 2 s budget, the single hop and the breaker are the platform rule of ADR-020; the timer duration is the review date and not a constant.
- Parameters read: the rule rows R-WO-17 to R-WO-19 and the package version in force, read through `RulePackageClient` from the WO package of rwb-decision; that package read is the reference-data contract. DP-06 and DP-07 are not in this story's pattern set, and the read's contract element is Not specified in the source documents (DOR-RWB-S7-E6020-APP-20).

**Build steps**

1. The deferral branch of `WriteOffWorkflow` and its input record, registered on `rwb-writeoff` as the stage child of `CaseWorkflow`, with the member's decision as its signal.
2. `CaseClient` against its fake, with the 2 s budget, the breaker, the not-in-pack path and the moved-case path (AC1, X4, X5).
3. `RulePackageClient` against its fake, with the version in force recorded with each outcome (AC1, AC2).
4. `CommitteeDecisionEvaluator` over the package, with R-WO-17, the R-WO-18 refusal, the R-WO-19 firing and the no-fire path (AC1, AC2, X3).
5. `WriteOffDecisionRecordWriter` against the stub, with the failed-write path (AC1, AC3, X1).
6. `CaseMoveAnswer` with the `DEFERRED` and `SCAN_DUE` moves, and `ReviewTimerClient` with the timer creation and cancellation (AC2, X8).
7. `ReviewTimer` armed from the review date, fired once, cancelled on a case that leaves `DEFERRED` (AC2, X8).
8. `CommitteeDecisionController` with the defer branch, the rights, the `Idempotency-Key` and the problem mapping of the declared errors, and `WriteOffProposal` on SCR-27 through the composite route fake (AC1, X2, X7).
9. The boundary test: no statement outside `rwb_writeoff`, no `v_ace_*` read, no write to any other service's schema, and no write to a column of `write_off` (X9, BR1, BR5, BR6).

**Feature flag.** `rwb.writeoff.committee-decision-v1`, a flag of the platform library; off means the operation answers 503 with no write and no timer, SCR-27 hides the decision actions, and the scan, the pack and the routing stories are unaffected.

**Done when.** The tests of section 16 pass, the step runs from a synthetic in-committee case in SIT, R-WO-17 defers the case with its review date recorded and its timer armed, an absent review date and a moved case are refused, R-WO-19 returns the case to `SCAN_DUE` at the review date, a repeated key writes once, a forced record failure changes nothing, no `recovery_case` or `timer` row, no `write_off` column write and no `v_ace_*` read exists in the build, and SCR-27 answers through the composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S7-001 | Carried from the legacy message set of RWB-E6-020: the scan is held for an absent tax criteria version (R-WO-03), so no pack reaches the committee. Raised by RWB-S7-E6013-APP, not by this step | The scan is on hold until Finance publishes the tax criteria. |
| MSG-GEN-001 | The review date is absent on a defer, or a required element of the request is invalid (X3) | Enter {field}. |
| MSG-P4-002 | A role without the Write-off and posting right A calls the decision (X2) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the case moves (X1) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The four IDs are those of the legacy message set of RWB-E6-020 and of FSD S7 A2.8, and the text is the legacy and FSD wording, copied unchanged; no message is reworded and no new one is added. No source publishes a message for a review date in the past or earlier than the next cut-off, so the step validates only the absent value and the former is recorded as a gap (GAP-3031; ASM-5060).

### 15. Screens and states

Screen states of SCR-27 Write-off proposal for this story: the error state shows MSG-P7-003 when the local decision record cannot be written, and the no-access state shows MSG-P4-002 for a role without the Write-off and posting right A. The empty state and the loading state of SCR-27 are Not specified in the source documents (DOR-RWB-S7-E6020-APP-10).

SCR-27 Write-off proposal, in its in-committee and deferred states, is served through the gateway-bff composite route (DP-19). The route calls rwb-writeoff for the pack, the decision and the review date, and rwb-case for the case and its route state; this story fixes the rwb-writeoff answers only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON.

The legacy screen table gives the states "Scan; proposed; in committee; approved". This story produces the deferred state: a case shows its deferral, the review date and the time it was taken, and stays in the population for the next scan until the review date arrives. The scan state is RWB-S7-E6013-APP's, the proposed state RWB-S7-E6015-APP's, the routing into committee RWB-S7-E6017-APP's, the approved state RWB-S7-E6018-APP's and the rejected state RWB-S7-E6019-APP's. The refusal, missing-review-date and not-recorded states read the messages of section 14.

The states empty, loading, error and no access of SCR-27 are not in Screen Specifications v1: empty is Not specified in the source documents (CG-ALL-11038), loading is Not specified in the source documents (CG-ALL-11038), error is Not specified in the source documents (CG-ALL-11038) and no access is Not specified in the source documents (CG-ALL-11038).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E6-020-01 | AC1 | Component | The 40-case in-committee population on the fake with `RC-2026-000732`; the record, the `DEFERRED` answer and the review date asserted |
| TC-E6-020-02 | AC2 | Component | `RC-2026-000732` at `WITH_COMMITTEE` with a review date; R-WO-17 applied, the timer armed and the `DEFERRED` move asserted on the fake |
| TC-E6-020-03 | AC3 | Component | The decision-record stub stopped; nothing written, no timer set, no answer sent and MSG-P7-003 shown |
| TC-E6-020-04 | Access | Component | A role without the Write-off and posting right A; 403 with MSG-P4-002 and no read |
| TC-E6-020-05 | Principle 5 | Component | A forced decision record write failure inside the transaction; the case stays at `WITH_COMMITTEE` and no timer is armed |
| TC-E6-020-06 | Contract (§12) | Component | The defer branch of `POST /write-offs/{writeOffId}/committee-decision` and the activities and signals of §12.5 checked against the contract on the fake; the defer answer and rule IDs asserted |
| TC-E6-020-07 | Boundary (§12.7) | Component | Each table of §12.7 checked at its boundary: `write_off` read only; `decision_record`, `idempotency_key` and `outbox_event` written only by this step; no read of tables not owned |
| TC-E6-020-08 | AC4 | Component | A role without the Write-off and posting right A; 403 with MSG-P4-002 and no read or write |
| TC-E6-020-09 | AC5, BR5, BR6 | Component | A component, statement or test reading a `v_ace_*` view, a `recovery_case` row, a `timer` row or another service's schema; the grant refuses it and the boundary test fails the build |
| TC-E6-020-10 | AC10 | Component | Not specified in the source documents (NEWAC-RWB-S7-E6020-APP-AC10) |
| TC-E6-020-11 | BR1, BR4, BR10, BR11 | Component | The deferral run in `WriteOffWorkflow` on `rwb-writeoff` with R-WO-17 and R-WO-19 applied from the package; the `DEFERRED` and `SCAN_DUE` answers asserted and no `write_off` column written |
| TC-E6-020-12 | BR2, BR7, BR8 | Component | The record written with the rule ID, package version, decision, review date and both states before the move; a repeated key arms no second timer; a firing after the case has left `DEFERRED` writes nothing |
| TC-E6-020-13 | BR3, BR9 | Component | A case not at `WITH_COMMITTEE` refused with 409; an absent review date refused under R-WO-18; no name, address, contact value or identity number in the record, the log or a workflow input |
| TC-E6-020-14 | AC6, BR1 to BR9 | Component | The deferral run on the fakes with BR1 to BR9 in force; each rule checked as section 8 states it |
| TC-E6-020-15 | AC7 | Component | Each error answer of `POST /write-offs/{writeOffId}/committee-decision` on the fake checked at its contract status code (401, 403 or 404) with the platform error envelope |
| TC-E6-020-16 | AC8 | Component | The rwb-case fake does not answer inside 2 s; the retry on the workflow's schedule asserted, with nothing written, no timer set and no move answered |
| TC-E6-020-17 | AC9 | Component | The rwb-decision fake fails, or its breaker is forced open; nothing written, no timer set, no move answered and the answer of section 5 X5 asserted |

The five legacy cases are those of RWB-E6-020 in their legacy order, with the Level column added: every case is tested on the fakes, so every case is `Component`. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same ID; no `-ITG` copy is written by this story, and the cross-service journey belongs to the wave 4 harness.

### 17. Guardrails

- No business value in code: R-WO-17 to R-WO-19, the two states, the review-date condition, the decision code, the package version and the capability rights stay rule rows and reference data, never a constant, a default or a branch.
- No personal data in `rwb_writeoff`, in a workflow input or in a log: identifiers, amounts, dates, a state and a rule version only, and every fixture is synthetic.
- ACE data only through the owner's contract: this service holds no `v_ace_*` grant and reads no ACE table, and a build that adds one fails the boundary test (BR6).
- The case stays with rwb-case: no `recovery_case` row, no case state column, no `timer` row and no case write here (BR4).
- The write-off row is read, not written: no column of `write_off` is set by a deferral, not even `committee_date` (BR1).
- One base, one topic, one queue, one schema and one login per service; no document names another service's base or topic as its own (DP-13, DP-14).
- The timer is durable and single: no Quartz row, no shared job table, no re-arming on a repeat and no firing after the case has left `DEFERRED` (BR8).
- No retired element is reintroduced: no monolith base, no shared `recovery` schema read and no event published by this step.
- The decision is recorded before the change; a build that answers a move outside the record's transaction fails the review (DP-03).

### 18. Traceability

| Requirement ID | Requirement (short) | Story element | Test cases | Feature | L3 process |
|---|---|---|---|---|---|---|---|
| REQ-S7-003 | The committee decision to approve, reject or defer is recorded against each account (FSD S7 Requirements served); the deferral shares the row with the approval and the rejection stories (ASM-5066) | The defer branch of the committee decision: R-WO-17 and R-WO-19, the record, the timer and the two case-move answers | TC-E6-020-01, TC-E6-020-02, TC-E6-020-03, TC-E6-020-05 | FEAT-WOF-08 | Not specified in the source documents (DOR-RWB-S7-E6020-APP-2) |
| ADR-013 | 19 services inside ACE | rwb-writeoff as the owner of the write-off stage | TC-E6-020-01 | FEAT-WOF-08 | Not specified in the source documents (DOR-RWB-S7-E6020-APP-2) |
| ADR-014 | Schema and login per service | `rwb_writeoff` and its own login | TC-E6-020-01 | FEAT-WOF-08 | Not specified in the source documents (DOR-RWB-S7-E6020-APP-2) |
| ADR-016 | Reusable Temporal layer; Schedules replace Quartz | The durable review timer inside the stage workflow | TC-E6-020-02 | FEAT-WOF-08 | Not specified in the source documents (DOR-RWB-S7-E6020-APP-2) |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The four consumed rows with their budget and breaker | TC-E6-020-01 | FEAT-WOF-08 | Not specified in the source documents (DOR-RWB-S7-E6020-APP-2) |
| ADR-022 | Local decision record plus central ledger | The records written before each change | TC-E6-020-03, TC-E6-020-05 | FEAT-WOF-08 | Not specified in the source documents (DOR-RWB-S7-E6020-APP-2) |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E6-020, disposition Split (rework); feature FEAT-WOF-08 |
| Legacy criteria | AC1, AC2 and AC3, owned word for word by this story |
| Wave and release | Wave 4 and release 30 April 2027 (tentative), copied unchanged from the plan; EP06 and the service wave agree at 4, so no W-MAP conflict is raised (ASM-5058) |
| Source text | Legacy RWB-E6-020; FSD S7 Write-off and recovery v3 A2.8, Requirements served and Screens; TSD S7 Write-off and recovery v2 T2, T3.1, T3.2, T4, T5.3, T6.1 and T-A; Business Rules and Routing Logic v4 rows R-WO-17, R-WO-18 and R-WO-19; Batch and Scheduling Design v5, JOB-05 and JOB-16 |
| Test cases | TC-E6-020-01 to TC-E6-020-05 |
| Feature and screens | FEAT-WOF-08, SCR-27 Write-off proposal |
| Rules | R-WO-17 and R-WO-19, with R-WO-18 as the refusal of a defer with no review date, governed in rwb-decision |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-016, ADR-020, ADR-022 |

### 19. Out of scope

- The published shape of the committee decision, the `CommitteeDecision` and `DecisionLogEntry` elements, the review-date placeholder, the consumed rows, the error set and the fakes: RWB-S7-E6020-CON.
- The monthly scan, the tax criteria, the pack, the removal and the routing into committee: RWB-S7-E6013-APP to RWB-S7-E6017-APP.
- The approval inside the limit, the credit-committee escalation and the rejection of R-WO-12 to R-WO-15: RWB-S7-E6018-APP. The rejection of R-WO-16: RWB-S7-E6019-APP.
- The posting, `WriteOffApproved` (`EV-24`), the provision release, the Finance feed, the reconciliation, the exception loop and the retention close: RWB-S7-E6021-APP to RWB-S7-E6025-APP.
- The case of record, its route states and the `timer` row: rwb-case (P3), which writes them on this story's answers (ASM-5062, ASM-5063).
- The authoring, testing, approval and versioning of the WO package and of R-WO-17 to R-WO-19: rwb-decision (P7) (ASM-5064).
- A validation rule, a message or a list of values for a review date in the past or earlier than the next cut-off: no source gives one (GAP-3031; ASM-5060).
- The decision of a case that is already `DEFERRED`: no row of TSD S7 T4 publishes it, and the deferral is closed by R-WO-19 (GAP-3031).
- The gateway-bff composite route and the screen field list of SCR-27: RWB-PLT-N001-CON and the edge stories.
- The cross-service journey of the legacy key and its evidence: the wave 4 harness, which copies none of these criteria.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
