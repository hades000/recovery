# RWB-S7-E6019-APP Reject a write-off

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Version 3 changes** (D-RCV-60 P1 developer readiness, RD-P1 register)

- Start rule of `WriteOffWorkflow` / JOB-16: only the `AceDataReady` event with `sourceSystem` ALS and `status` COMPLETED counts; the event is published once per source system and business date (RD-P1-003, RD-P1-040).

| Item | Value |
|---|---|
| Story key | RWB-S7-E6019-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-writeoff |
| Service epic | RWB-SVC-S7 |
| Wave | 4 |
| Business epic | EP06 |
| Release | 30 April 2027 (tentative) |
| Legacy key | RWB-E6-019 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | L-S7-G |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-S7-E6019-APP-16) |
| Depends on (build) | RWB-S7-E6019-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Contract version | v1, base `/api/recovery/writeoff/v1` (API-S7-002) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S7 rwb-writeoff v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |
| Readiness decisions | RD-P1-003, RD-P1-040 |

**Change log.** D-RCV-60, 22 November 2026: the reject slice of RWB-E6-019 in rwb-writeoff. The two legacy criteria are kept word for word with their origin tag; the step evaluates R-WO-16 (with R-WO-18 as the refusal of an incomplete decision), records the decision through the local decision-record library before any change (DP-03), answers rwb-case for the move `RETURNED_TO_PURSUE` with the reason, and serves the reject branch of the published `POST /write-offs/{writeOffId}/committee-decision` on base `/api/recovery/writeoff/v1` (DP-13), reached from SCR-27 through the gateway-bff composite route (DP-19). Every source publishes that operation (TSD S7 T-A.1, API-S7-002, right A) but no source gives the reject reason a column, a field ID or a list of values, the plan's C row is empty while the step consumes three contracts, and R-WO-16's owner conflicts with the FSD role and the permission table (GAP-3029; ASM-5052, ASM-5053, ASM-5054, ASM-5056). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-S7-E6019-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (23 resolved, 15 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **write-off committee member (RW-WOCOMM)**, I want **the Workbench to let the committee reject, with a reason that returns the case to recovery**, so that **write-offs follow the criteria and the committee's decision**.

This is the reject slice of legacy RWB-E6-019. It owns:

- the two legacy criteria this story owns (AC1, AC2), copied verbatim with their origin tag, and the rule, message and screen they depend on;
- one step of `WriteOffWorkflow` on task queue `rwb-writeoff`, as the stage child of `CaseWorkflow` and as one of the three decisions the committee takes on a case routed to it (Temporal and Drools Design slides 5, 12 and 13);
- the evaluation of R-WO-16 against the WO package version in force, from `WITH_COMMITTEE` on `COMMITTEE_REJECTED` with `decision_reason` present, and the refusal of R-WO-18 when the reason is absent (FSD S7 A2.7.3.1; Business Rules and Routing Logic v4);
- the local decision record of the rejection, written through RWB-PLT-E1027-CON before any change (DP-03), with the rule ID, the package version, the case reference, the reason and the case move;
- the answer to rwb-case for `RETURNED_TO_PURSUE`, with the reason the rule records, so that the case of record returns to the pursue track and the service that owns the case writes it;
- the reject branch of the committee-decision operation of the module on base `/api/recovery/writeoff/v1` and the in-committee state of SCR-27 Write-off proposal behind the gateway-bff composite route (DP-13, DP-19).

It does not own: the published shape of the committee decision, the `CommitteeDecision` and `DecisionLogEntry` elements, the reason field, the consumed rows, the error set and the fakes, which are RWB-S7-E6019-CON; the routing of the pack to the committee and the schedule of the meeting (RWB-S7-E6017-APP); the approval inside the limit and the credit-committee escalation of R-WO-12, R-WO-13 and R-WO-15 and the rejection of R-WO-14 (RWB-S7-E6018-APP); the deferral of R-WO-17 and R-WO-19 (RWB-S7-E6020-APP); the scan (RWB-S7-E6013-APP), the tax criteria (RWB-S7-E6014-APP) and the pack of R-WO-05 (RWB-S7-E6015-APP); the posting with `WriteOffApproved` (RWB-S7-E6021-APP); the case of record, its route states and the parent `CaseWorkflow`, which are rwb-case (P3); the ACE data products, which are rwb-source-data's (P1); the WO package and its 51 rules, which are rwb-decision's (P7); and the deployment of this build, which is the operations story of this legacy key.

### 2. Business rationale

The feature objective, the problem and the metric are unchanged from the legacy story and the module FSD: the committee rejects with a reason that returns the case to recovery, because write-off populations are assembled by hand each month (FSD S7 A1.3, A2.7.1), and the packs accepted first time are measured on the decision log and the Workbench records against a target that rises each month, reviewed monthly (FSD S7 A2.7.1). What D-RCV-60 changes is who owns the case, the package, the decision and the screen.

- **The rejection is this service's step.** `write_off` is S7's only table in `rwb_writeoff` (context pack, ownership rows owned by S7; TSD S7 T3.1), and the WO route set of 51 rules over 27 states is the write-off stage's (TSD S7 T4); R-WO-16 is a transition of that stage and runs here.
- **The case stays with rwb-case.** `recovery_case`, the committee state `WITH_COMMITTEE` and the state the rejection writes, `RETURNED_TO_PURSUE`, are P3's; this step evaluates the rule, records the decision and **answers** the case move (ASM-5054).
- **The package is read, not embedded.** The WO route set is governed in rwb-decision, and DP-04 is not in this key's pattern set, so the package arrives on its read with the version in force and the version is recorded with the outcome (ASM-5005).
- **The decision is recorded first**, before the case leaves the committee state, which is what legacy AC1 asked for and legacy AC2 tested; a rejection with no record is no rejection.
- **The reason is the condition.** R-WO-16 fires only where `decision_reason` is present and R-WO-18 sends an incomplete decision back to the committee, so the reason is the one input this step validates; no source gives it a column, a field ID, a length or a list of values (ASM-5053).
- **A rejection writes nothing to `write_off`.** The legacy Data table lists `recovery_case`, `decision_log_entry` and `rule_row` and no column of the write-off row, `committee_date` is the approval's fact and `posted_date` the posting's, so the reject slice writes no column of the table (GAP-3029; ASM-5055).
- **The rejection is not the credit-committee rejection.** R-WO-14 returns a case from `ESCALATED_TO_CREDIT_COMMITTEE` to the pursue track after the credit committee rejects it above the write-off committee limit; that row belongs to the approval slice of RWB-S7-E6018-APP and this step neither tests nor writes it (ASM-5055).
- **The requirement is shared.** REQ-S7-003 says the committee decision to approve, reject or defer is recorded against each account, so the reject carries the same requirement as the approve and defer stories and is proven here on its own (FSD S7 Requirements served; ASM-5057).

No business value moves: the reason, the from and to states, the rule ID, the package version and the decision code of the record are values of reference data and of the rule package, read with their version and never written in code.

### 3. Preconditions

- RWB-S7-E6019-CON is published: the committee-decision operation with its reject branch, the `CommitteeDecision` and `DecisionLogEntry` elements, the reason field with its placeholder, the consumed rows, the case-move answer, the `Idempotency-Key` rule, the error set and the fakes are baselined and handed to this story.
- The rwb-case case read is published with its fake: the case reference, the case number, the product group, the stage and the state `WITH_COMMITTEE`. The operation name is Not specified in the source documents (GAP-3029; ASM-5054).
- The case-move answer of rwb-case is available for the fake: the move `RETURNED_TO_PURSUE` with the reason and the rule version. No source names a published operation that moves a case state on behalf of a stage; on the workflow boundary the answer is the stage outcome the parent `CaseWorkflow` applies (GAP-3029; ASM-5054).
- The rwb-decision rule-package read is published with its fake and answers the WO package at its version in force, with R-WO-16 and R-WO-18 among its 51 rules over 27 states (GAP-3029; ASM-5005).
- RWB-PLT-E1027-CON is published with its writer fake: the local decision-record library writes in the caller's transaction, and a failed write stops the action with MSG-P7-003, so no move is answered and nothing changes (DP-03).
- RWB-PLT-N001-CON is published: SCR-27 reaches this service through the gateway-bff composite route, one hop, and no screen calls a service directly (DP-19).
- `write_off` exists in schema `rwb_writeoff` from the DB story of this service, with the columns of DF-FIN-010 to DF-FIN-020 and the standard record columns of TSD S7 T3.0; this story adds no table, no column and no migration, and writes no column of it.
- The WO package is in force at its version and is read on its package read; the rule rows, the decision reason and the states are governed in rwb-decision and are not a build item of this story.
- The service runs as its own login on schema `rwb_writeoff`; it holds no grant on another `rwb_*` schema and no `v_ace_*` grant, so a statement on `rwb_case` or on an ACE view is refused by the database and fails the boundary test.
- No approval is needed to build against a Draft contract baseline; the contract is tagged by RWB-S7-E6019-CON when its tests pass.

### 4. Flow

1. RWB-S7-E6017-APP has routed the pack to the committee and the case sits at `WITH_COMMITTEE` (R-WO-11, R-WO-10); this story reads that outcome only (FSD S7 A2.5; TSD S7 T4).
2. The committee member opens SCR-27 Write-off proposal through the gateway-bff composite route and reads the case, its pack and the limit applied, one hop (DP-19).
3. The member records the rejection and gives the reason. The reason is the only input this step requires on a reject; the screen sends the write-off reference, the decision, the reason, the member's identity and an `Idempotency-Key`.
4. The decision step of `WriteOffWorkflow` on queue `rwb-writeoff` receives the request as a signal to the running stage, with the write-off reference, the decision, the reason and the package version read from rwb-decision in force (DP-12; ASM-5005).
5. The step reads the case on the rwb-case contract: the case reference, its product group, its stage and its state. A case that is not at `WITH_COMMITTEE` is refused with 409 and nothing is written (ASM-5054).
6. `CommitteeDecisionEvaluator` evaluates R-WO-16: from `WITH_COMMITTEE`, on `COMMITTEE_REJECTED`, where `decision_reason` is present, the action is "Return the case to the pursue track" and the state is `RETURNED_TO_PURSUE`. Where the reason is absent, R-WO-18 refuses the decision and the case stays at `WITH_COMMITTEE` (FSD S7 A2.7.3.1; Business Rules and Routing Logic v4).
7. The evaluation answers the rule ID, the package version, the action of the rule, the recorded reason and the case move the rule names.
8. `WriteOffDecisionRecordWriter` writes one decision record through the local decision-record library, **before any change**: the case reference, the decision, the rule ID `R-WO-16` with its package version, the reason, the from state, the to state and the decided-at time. A failed write stops the step with nothing changed (DP-03; legacy AC1 and AC2).
9. `CaseMoveAnswer` answers rwb-case with the move `RETURNED_TO_PURSUE`, the reason and the rule version. rwb-case writes the `recovery_case` row and the state; this service writes neither the row nor the state (ASM-5054).
10. The member sees the rejection recorded and the case returned to the pursue track, read back from this service and from the case state of rwb-case, read only (DP-19).
11. A repeated request with the same `Idempotency-Key` answers the decision it created, writes no second record and sends no second answer; a decision on a case that has left `WITH_COMMITTEE` answers 409 with no change.
12. The reason is screened for personal data before it is stored: no identity value and no contact value is copied into the record or the answer.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The local decision record cannot be written | Nothing changes: no move is answered, the case stays at `WITH_COMMITTEE` and no record exists | MSG-P7-003 | AC2, TC-E6-019-02, TC-E6-019-04 |
| X2 | The role does not hold the Write-off and posting right A | 403 before any read or write; nothing changes and no record is written | MSG-P4-002 | AC3, TC-E6-019-03, TC-E6-019-09 |
| X3 | The reason is absent on a reject | 422 and nothing is recorded; the decision is refused and the case stays at `WITH_COMMITTEE` | MSG-GEN-001 | AC1, X5 |
| X4 | The case is not at `WITH_COMMITTEE`, or the decision has already been taken | 409 and nothing is written for that case; a decision is not taken twice | None | AC1, X3, AC7, TC-E6-019-11 |
| X5 | The rwb-case or rwb-decision contract does not answer inside 2 s, or its breaker is open | The step retries on the workflow's own schedule; nothing is written and no move is answered; the caller sees 503 with the platform error envelope | None | AC1, X2, AC10, AC11, TC-E6-019-14, TC-E6-019-15 |
| X6 | The case is still held in the scan for an absent tax criteria version or an absent ALS extract | No pack reached the committee, so no case is at `WITH_COMMITTEE` to decide; the hold is raised by RWB-S7-E6013-APP | MSG-S7-001 | AC1 |
| X7 | A repeated `Idempotency-Key`, or the same decision taken twice | One record and one answer; the repeat answers the decision that exists and is counted | None | AC1, AC9, TC-E6-019-13 |
| X8 | A component, a statement or a test reaches a `v_ace_*` view, a `recovery_case` row or another service's schema | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | AC4, TC-E6-019-06, TC-E6-019-10, Section 17, BR5, BR6 |

X1 to X3 are the legacy exception paths carried onto the slice, X4 to X7 are the paths the target call types and the interactive trigger add, and X8 is the ACE and schema boundary. The deviation codes X1 to X7 of R-WO-06 are codes of the rule package and are not the path identifiers of this table.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-S7-E6019-CON, the rwb-case and rwb-decision fakes and the decision-record stub, on its own schema, and needs no live P1, P3 or P7 |
| Negotiable | The activity name, the decision code of the record and the shape of the stage outcome are this story's choice; the rule, the messages, the screen, the operation and the two states are fixed |
| Valuable | A rejected case leaves the committee with its reason recorded and returns to the pursue track in the service that owns it, so no case is written off against the committee's decision |
| Estimable | One workflow step, one evaluator, one record write, one case-move answer, one operation branch, three clients and one read-only screen state |
| Small | Finished inside two weeks with its tests on the fakes |
| Testable | Each criterion runs on a synthetic in-committee case through the contract fakes, plus the access, missing-reason and failed-record cases |

### 7. Acceptance criteria

```gherkin
Feature: Reject a write-off

  Background:
    Given case "RC-2026-000731" is one of 40 cases in state "WITH_COMMITTEE" on the pack of the monthly write-off scan
    Given the WO rule package is in force at its version and carries R-WO-16 and R-WO-18
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 Reject a write-off (legacy RWB-E6-019 AC1)
    Given the rwb-case contract mock returns the case of record at "WITH_COMMITTEE" and accepts the move "RETURNED_TO_PURSUE"
    Given the rwb-decision contract mock returns the WO package at its version in force with R-WO-16
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then lets the committee reject, with a reason that returns the case to recovery
    Then WriteOffWorkflow writes the result to the decision record with the rule version

  Scenario: AC2 Not recorded (legacy RWB-E6-019 AC2)
    Given the decision record cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003

  Scenario: AC3 A role without the Write-off and posting right A is refused (new, D-RCV-60)
    Given a role that does not hold the Write-off and posting right A
    When the committee decision is taken
    Then the system answers 403 before any read or write, nothing is written and the user sees MSG-P4-002

  Scenario: AC4 A component reaching a v_ace_* view, a recovery_case row or another service's schema fails the build (new, D-RCV-60)
    Given a component, a statement or a test reaches a v_ace_* view, a recovery_case row or another service's schema
    When the boundary test runs
    Then the grant refuses the statement, the build fails and nothing is released

  Scenario: AC5 A repeated request is answered once (new, D-RCV-60)
    Given the same request or the same Idempotency-Key is sent twice
    When the second request arrives
    Then one record is written and one answer is sent, and a case that has left WITH_COMMITTEE is refused with 409 and nothing is written

  Scenario: AC6 A decision reason with personal data is screened before it is stored (new, D-RCV-60)
    Given a decision reason carries a name, an address, a contact value or an identity number
    When the reason is screened
    Then no such value reaches rwb_writeoff, the decision record, a log or a workflow input, and the reason is screened before it is stored

  Scenario: AC7 A status change the model does not allow is refused with 409 (new, D-RCV-60)
    Given the case is in a state other than WITH_COMMITTEE, or the decision event is not COMMITTEE_REJECTED
    When the committee decision is taken
    Then the system answers 409, nothing is written and the case keeps its state

  Scenario: AC8 A request with no valid identity, with no right or for an unknown write-off is answered 401, 403 or 404 (new, D-RCV-60)
    Given a request to the provided operations without a valid identity, from a role without the right, or for a writeOffId that does not exist
    When the request reaches POST /write-offs/{writeOffId}/committee-decision
    Then the system answers 401 with no valid identity, 403 with no right and 404 for an unknown writeOffId, with the platform error envelope, and nothing is written

  Scenario: AC9 A replay of a write with the same Idempotency-Key is answered from the first answer (new, D-RCV-60)
    Given a committee decision was written with an Idempotency-Key
    When the same write is replayed with the same Idempotency-Key
    Then no second record is written and the first answer is returned

  Scenario: AC10 A retried or timed-out activity writes once (new, D-RCV-60)
    Given the recordCommitteeDecision activity is retried or times out
    When the workflow retries on its own schedule
    Then nothing is written twice and no move is answered before the decision record is written

  Scenario: AC11 A consumed call that fails or does not answer changes nothing (new, D-RCV-60)
    Given the rwb-case or rwb-decision contract fails or does not answer inside 2 s
    When the committee decision is taken
    Then nothing is written, no move is answered and the caller sees 503 with the platform error envelope
```

The two criteria are the legacy criteria of RWB-E6-019 with their origin tag added; the wording changes are that the legacy `decision log` is named `decision record` and the AC1 actor is `WriteOffWorkflow` (CG-ALL-11012); the repeated `Then`, the wording of `the user acts on the screen` and `the action is taken` all stand. The cross-service parts are mocked, so AC1 carries `Given the <service> contract mock returns <x>` lines, and those are the only additions. AC2 has no cross-service part and gains no line. What the legacy lines describe happens in three places now: rwb-case answers the case and writes the move, rwb-decision holds the package at its version, and this story evaluates R-WO-16, writes the record and answers the move. The `decision log` of the legacy text is the local decision record of DP-03 in `rwb_writeoff`, with the central `decision_log_entry` ledger of rwb-decision behind it.

### 8. Business rules

| Rule | Route set | Decision | From state | Event | Condition | Action | To state | Owner | Systems | Timer |
|---|---|---|---|---|---|---|---|---|---|---|
| R-WO-16 | Write-off | D9 | WITH_COMMITTEE | COMMITTEE_REJECTED | decision_reason present | Return the case to the pursue track | RETURNED_TO_PURSUE | Case owner | Committee View, Decision Log | None |

The row is the row of the Business Rules and Routing Logic v4, copied character for character. Its BR ID is BR10, listed in the rule table below; the row itself stays as copied. Its owner and systems columns name a business role and systems, not services: in the target the "Committee View" is the case of rwb-case and its route state read through the composite route, the "Decision Log" is the local record of DP-03 in `rwb_writeoff` with the rwb-decision ledger behind it, and "Case owner" is read as the committee decision owner the permission table gives right A (GAP-3029; ASM-5056). R-WO-18, the refusal of a decision with no reason, and R-WO-14, the rejection after the credit committee has rejected a case above the write-off committee limit, are the rows this step does not own: R-WO-18 is the refusal path of X3 and R-WO-14 belongs to RWB-S7-E6018-APP (ASM-5055).

| ID | Rule | Source | Covered by |
|---|---|---|---|
| BR1 | The rejection is a transition of the write-off stage: it runs in `WriteOffWorkflow` on `rwb-writeoff` and writes no column of `write_off` | TSD S7 T3.1, T4; context pack ownership rows (table and workflow); FSD S7 A2.7.2 | AC1, TC-E6-019-06 |
| BR2 | The decision is recorded before the case moves, with the rule ID, the package version, the decision, the reason and the two states; a failed write changes nothing and the caller sees MSG-P7-003 | DP-03; TSD S7 T2 ("writes the decision log entry before any change"); legacy AC1 and AC2 | AC2, TC-E6-019-02, TC-E6-019-04 |
| BR3 | Only a case at `WITH_COMMITTEE` is decided, and a reject carries a reason: another state is refused, and a reason that is present is the whole condition of the rule | Business Rules and Routing Logic v4 rows R-WO-16 and R-WO-18; FSD S7 A2.7.3.1 | AC1, TC-E6-019-01 |
| BR4 | The move is answered, not written: `recovery_case` and every route state are rwb-case's, and this service answers `RETURNED_TO_PURSUE` with the rule and its version | ASM-5054; TSD S7 T4 | AC1, TC-E6-019-01 |
| BR5 | No cross-schema join and no foreign key leaves `rwb_writeoff`; `case_id` and `decision_log_id` are identifiers of another service's fact | DP-01; TSD S7 T3.3 | AC4, TC-E6-019-06 |
| BR6 | ACE data only through the owner's contract: this service holds no `v_ace_*` grant and reads no ACE table, and the balance and the tax result reach it on the pack of RWB-S7-E6015-APP | DP-05 as a prohibition; FSD S7 A1.1; TSD S7 T1 | AC4, TC-E6-019-06 |
| BR7 | Every value a business person may change is a rule row or reference data read with its version: R-WO-16, its states, the reason and the package version | FSD S7 BR-S7-007; legacy Guardrails | AC1, TC-E6-019-01 |
| BR8 | The same request twice, or the same `Idempotency-Key` twice, writes one record and sends one answer; a case that has left `WITH_COMMITTEE` is refused with 409 | TSD S7 T-A.2 | AC5, TC-E6-019-07 |
| BR9 | No person name, address, contact value or identity number enters `rwb_writeoff`, the decision record, a log or a workflow input; the case reference is a number and not an identity, and the reason is screened before it is stored | Template and Rules §R7.2 (s17); TSD S7 T6.2 | AC6, TC-E6-019-08 |
| BR10 | R-WO-16, the rule row of this step: from `WITH_COMMITTEE` on `COMMITTEE_REJECTED`, where `decision_reason` is present, the action returns the case to the pursue track and the state is `RETURNED_TO_PURSUE` | Business Rules and Routing Logic v4 row R-WO-16; FSD S7 A2.7.3.1 | AC1, TC-E6-019-01 |

### 9. State transitions

The case route state is rwb-case's and is not changed by this story: the step answers the move and the parent `CaseWorkflow` applies it (BR4). What this story owns is the step and the record; the states it writes are the ones of the WO machine.

| From (case state, rwb-case) | Event | Condition | To | Written by |
|---|---|---|---|---|
| `WITH_COMMITTEE` | `COMMITTEE_REJECTED` | `decision_reason` present | `RETURNED_TO_PURSUE` | rwb-case, on this story's answer |
| `WITH_COMMITTEE` | `COMMITTEE_REJECTED` | `decision_reason` absent | Unchanged | none; R-WO-18 refuses the decision and MSG-GEN-001 |
| `WITH_COMMITTEE` | `COMMITTEE_REJECTED` | The case is not at `WITH_COMMITTEE` | Unchanged | none; 409 |
| `RETURNED_TO_PURSUE` | The onward path | The case is pursued again | Not published | No row of TSD S7 T4 moves a case out of `RETURNED_TO_PURSUE`; the onward path stays with the case owner (GAP-3029; ASM-5054) |
| `ESCALATED_TO_CREDIT_COMMITTEE` | `CREDIT_COMMITTEE_REJECTED` | `decision_reason` present | `RETURNED_TO_PURSUE` | rwb-case, on the answer of RWB-S7-E6018-APP (R-WO-14) |

| Step execution | Event | Condition | To |
|---|---|---|---|
| Waiting | A committee decision for a case of the pack | The package in force is read | Evaluating |
| Evaluating | R-WO-16 fires | The reason is present and the case is at `WITH_COMMITTEE` | Recording |
| Evaluating | R-WO-16 does not fire | The reason is absent, or the state is not the rule's | Waiting, nothing changed |
| Recording | The record is written and the answer sent | The transaction commits | Waiting for the next request |
| Recording | The record write fails | X1 | Waiting, nothing changed |

The states `WITH_COMMITTEE`, `RETURNED_TO_PURSUE` and `ESCALATED_TO_CREDIT_COMMITTEE` are those of the WO machine of TSD S7 T4 and live on the case of record; this step writes none of them.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-WOCOMM, write-off committee member | Write-off and posting RA in TSD S7 T6.1: the primary role of FSD S7 A2.7.3.3, rejecting a case inside the committee and reading the decision back |
| RW-CREDITAD, Credit Administration officer | Write-off and posting CRUA: rejects a case and reads the record |
| RW-PRODHEAD, product head; RW-FINANCE, Finance and CFO delegate | Write-off and posting RA: the other two roles the legacy permission table gives right A on the committee decision |
| RW-WRITEOFF, write-off team member | Write-off and posting CRU: reads the rejection and its reason, and prepares the next population; it does not hold right A |
| RW-FRAUD, RW-DEBTSALE, RW-CONDUCT, RW-RISK, RW-COE, RW-AUDIT, RW-BIANAL, RW-TRIBE | Write-off and posting R: read only, in scope |
| SY-CASEWF, SY-RULES, SY-AGENT, SY-DATALOAD | Write-off and posting R or U as the matrix gives it: the service identities run the step and are subject to the same checks |
| rwb-writeoff service identity | Evaluates the rule, writes the record, answers the move and serves the operation; it holds no grant on another schema and no `v_ace_*` grant |

The rights are the rows of TSD S7 T6.1 and nothing wider, and the right this story needs is A — the right the legacy permission table gives to RW-CREDITAD, RW-PRODHEAD, RW-WOCOMM and RW-FINANCE for the committee decision, and the right TSD S7 T-A.2 declares on API-S7-002. DP-08 is not in this story's pattern set: the capability area and the right are declared per operation and the access guard is a service-template capability, so the check is stated here and not built here. The authorise check is the rwb-access check of the capability area Write-off and posting for right A, made before any read or write; its operation name is Not specified in the source documents (DOR-RWB-S7-E6019-APP-6).

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-FIN-010 | write_off (S7, `rwb_writeoff`) | id | Read, the write-off reference the operation takes as `writeOffId` |
| DF-FIN-011 | write_off (S7, `rwb_writeoff`) | case_id | Read, the case of the decision |
| DF-FIN-012 | write_off (S7, `rwb_writeoff`) | decision_log_id | Read, the record reference the pack step set; the new record of this step links to it |
| DF-FIN-013 | write_off (S7, `rwb_writeoff`) | amount | Read, the amount the committee has in front of it; a rejection changes no amount |
| DF-FIN-014 | write_off (S7, `rwb_writeoff`) | tax_criteria_met | Read, the result RWB-S7-E6014-APP wrote |
| DF-FIN-015 | write_off (S7, `rwb_writeoff`) | committee_date | Not written here: no committee date is set on a rejection; RWB-S7-E6018-APP sets it on approval |
| DF-FIN-016 to DF-FIN-019 | write_off (S7, `rwb_writeoff`) | posted_date, responsibility_center, cost_center, gl_product | Not written here: RWB-S7-E6021-APP |
| DF-FIN-020 | write_off (S7, `rwb_writeoff`) | recovered_after | Not written here: the recovery stories |
| Standard columns | write_off (S7, `rwb_writeoff`) | `is_active`, `state`, `version`, `created_at`, `created_by`, `updated_at`, `updated_by` | Not written: this step reads the row and writes no column of it |
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library, created in `rwb_writeoff`) | rule id, rule version, decision code, inputs reference, reason, from and to state, decided at | Write through the local library, before the case moves |
| DF-CAS-001 to DF-CAS-023 | recovery_case (P3) | id, case_no, product_group, primary_person_key, status, stage_code and 17 more | Not read as a table and not written: the state arrives on the rwb-case contract and the move returns on its answer |
| DF-REF-001 to DF-REF-015 | rule_row (P7) | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | Not read as a table: the rule arrives on the package read |
| `decision_reason` | the reason of R-WO-16 and R-WO-18 (request input) | Not specified in the source documents (DOR-RWB-S7-E6019-APP-7) | Read as a request input and recorded in the decision record; its field, column, length and list are Not specified in the source documents (GAP-3029; ASM-5053) |
| `decision_code` | the code of the decision record | Not specified in the source documents (DOR-RWB-S7-E6019-APP-7) | Write, the code the decision carries; its value set is Not specified in the source documents (GAP-3029; ASM-5053) |

Field IDs are those of TSD S7 T3.1 and the Logical Data Model and Data Dictionary, and the case, ledger and rule rows are the rows the legacy Data table lists, with their owners changed to P3 and P7 by the target. **No new table, no new column and no migration**: the table arrives with the DB story of this service, this story writes none of its columns, and `decision_record` and `idempotency_key` are library objects created in `rwb_writeoff` by the library's own migration (DP-03). `outbox_event` also sits in the schema as a library object, and this step writes no row to it because it publishes no event (§12.3).

**Personal data classing.** The rows carry identifiers, amounts, dates, list values, a reason, a rule version and a state. The personal-data classing of these fields is Not specified in the source documents (DOR-RWB-S7-E6019-APP-11). No name, address, contact value or identity number enters `rwb_writeoff`, the record, a log or a workflow input, and the fixtures are synthetic. The reason is free text a staff member writes; it is reviewed for personal data before it is stored, and `primary_person_key` is P3's and is never copied here.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-writeoff (S7); base `/api/recovery/writeoff/v1` (DP-13). This story supplies the reject branch of the committee-decision operation, whose shape RWB-S7-E6019-CON declares.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| POST | `/write-offs/{writeOffId}/committee-decision` (API-S7-002) | `CommitteeDecision` in with the decision and the reason, `DecisionLogEntry` out with the rule `R-WO-16` and its version, the reason and the state `RETURNED_TO_PURSUE` | Write-off and posting, right A, scope applied | `Idempotency-Key` header |

The errors are 400, 401, 403 with MSG-P4-002, 404 for a write-off that is not in the pack, 409 for a case that has left `WITH_COMMITTEE`, 422 with MSG-GEN-001 for a missing reason and 503 when the library or a consumed contract does not answer; the reason for a 422 on an incomplete decision is R-WO-18. TSD S7 T-A.1 publishes the operation as API-S7-002 with the request `CommitteeDecision`, the response `DecisionLogEntry` and the error set 401, 403, 404, 409, 422, 503, so the operation itself is published and needs no placeholder; the decision code values and the reason field are what no source gives (§11; GAP-3029; ASM-5052, ASM-5053). The same operation serves the approval and the deferral, which are RWB-S7-E6018-APP's and RWB-S7-E6020-APP's, and the scan is RWB-S7-E6013-APP's; none of the three is built or declared here.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| The case read (operation name Not specified in the source documents (GAP-3029; ASM-5054)) | `/api/recovery/case/v1` | P3 rwb-case | The case reference, case number, product group, stage and state of the case at `WITH_COMMITTEE`; read only, faked |
| The case-move answer (operation name Not specified in the source documents (GAP-3029; ASM-5054)) | rwb-case (P3) | P3 rwb-case | The move `RETURNED_TO_PURSUE` with the reason and the rule version; on the workflow boundary it is the stage outcome the parent `CaseWorkflow` applies; faked |
| The rule-package read in force (operation name Not specified in the source documents (GAP-3029; ASM-5005)) | `/api/recovery/decision/v1` | P7 rwb-decision | The WO package at its version, with R-WO-16 and R-WO-18 among its 51 rules over 27 states; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The three rows are contract dependencies of class C that the plan does not carry, because this story's C row is None; the absence is recorded (GAP-3029; ASM-5054, ASM-5005).

#### 12.3 Events published

None. The service publishes on `rwb.writeoff.events.v1` and its event set carries `WriteOffApproved` (`EV-24`, with `writeOffId`, `caseId` and `amount`, consumed by Posting), and that event belongs to the posting step of R-WO-20 and R-WO-21, which is RWB-S7-E6021-APP's. A rejection approves nothing, posts nothing and changes no amount, so this story declares no event, no producer group and no outbox row, and a build that publishes one fails the absence test. The topic carries the retry and `.dlt` topics of the platform (DP-14), and the outbox and inbox library that relays it is the DP-09 dependency the plan does not carry for this key (ASM-5055).

#### 12.4 Events consumed

None. The service listens to the rwb-source-data and rwb-payment events in its scan and recovery steps (context pack connection matrix, row S7: REST and events to P1, Temporal and events to P8), and none belongs to the rejection: a rejection reads no ACE extract and moves no money. This story therefore holds no consumer group, no subscription and no inbox row, and a build that adds one fails the absence test. The trigger of the step is the committee member's decision on SCR-27 through the composite route, and the FSD declares no background event for the feature beyond the monthly scan of R-WO-01 (FSD S7 A2.7.4.4).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `WriteOffWorkflow` | Workflow, one execution per case at the write-off stage, the child of `CaseWorkflow`, continues-as-new at each stage end; started by JOB-16 on the third working day after AceDataReady (R-WO-01) (counted only for the event with `sourceSystem` = `ALS` and `status` = `COMPLETED`, RD-P1-040); workflow ID form: Not specified in the source documents (CG-ALL-11008); duplicate-start policy: Not specified in the source documents (CG-ALL-11008) | `rwb-writeoff` | Input: the case reference, the cut-off date and the package in force; signals: the committee decision and the case answered by rwb-case; outcome for the parent: the case move |
| `recordCommitteeDecision` | Activity, the one decision step, with the reject branch of R-WO-16 and the refusal of R-WO-18 | `rwb-writeoff` | The case reference, the decision, the reason and the package version in; the rule ID with its version, the decision recorded and the case move out, with the record written before the answer |

No child workflow for the case and none for the money exists in this service. The activity name is a target design choice fixed by no source document; the step runs from the committee member's decision, and the monthly scan is the Schedule of RWB-S7-E6013-APP (§12.6).

#### 12.6 Schedules

None. The rejection is a member-driven step and owns no Temporal Schedule. `JOB-16`, the write-off scan job of the context pack and TSD S7, becomes the Temporal Schedule of R-WO-01 in RWB-S7-E6013-APP, and the meeting booking of R-WO-11 is RWB-S7-E6017-APP's; nothing of either is built or declared here.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| write_off | S7 (`rwb_writeoff`) | The write-off of the balance on a case; this story reads the row of the decision and writes none of its columns |
| decision_record | PLT library, created in `rwb_writeoff` | The local hash-linked decision record of the rejection (DP-03) |
| idempotency_key | PLT library, created in `rwb_writeoff` | The key of the repeated request and the answer it holds |
| outbox_event | PLT library, created in `rwb_writeoff` | Present as a library object; this step writes no row to it (§12.3) |

Not owned and never read as a table: `recovery_case` and `timer` (P3), every `v_ace_*` view (P1), `decision_log_entry` and `rule_row` (P7), `document` (P5), `notice` (P6), `payment` (P8). No foreign key leaves the schema and `case_id` is an identifier, not a foreign key across schemas (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case case fake | The case of record at `WITH_COMMITTEE` with its pack and limit, `RC-2026-000731` among 40 cases; a case that has moved; a case that is not in the pack | AC1, X3, X4 |
| rwb-case case-move fake | The move `RETURNED_TO_PURSUE` accepted for `RC-2026-000731` with the reason and the rule version; a move refused because the case is not in the expected state | AC1, X4 |
| rwb-decision rule-package fake | The WO package at its version in force with R-WO-16 and R-WO-18 among its 51 rules over 27 states | AC1 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and outbox, and a stopped chain | AC2, X1 |
| gateway-bff composite route fake | The merged SCR-27 answer for `RC-2026-000731`, in its in-committee state and after the decision | AC1 |

The fakes are test-only and are replaced by the real services in SIT. The operation names of the case read, the case-move answer and the package read carry the placeholder until their owners confirm them (GAP-3029; ASM-5054, ASM-5005).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 3 consumed | The committee-decision operation on `/api/recovery/writeoff/v1` (reject branch); the case read, the case-move answer and the package read; one hop, 2 s |
| Kafka | 0 published, 0 consumed | `WriteOffApproved` (`EV-24`) belongs to RWB-S7-E6021-APP and no event is consumed here (§12.3, §12.4) |
| Temporal | 1 workflow and 1 activity | `WriteOffWorkflow` and its decision step on `rwb-writeoff`; no Schedule |
| File | None | No file is read, built or delivered here |

### 13. Solution plan

**Package.** Java package `th.co.scb.ace.workbench.recovery.writeoff`, module `committee`; front end `src/modules/recovery/writeoff/WriteOffProposal.tsx`, the fragment SCR-27 embeds, read only for this story's state.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the transaction rule of the step: the record and the answer commit together or not at all. DP-13 moves the base of the legacy `/api/recovery/v1` paths and gives the committee-decision operation its home. DP-19 is how SCR-27 reaches this service, one hop through the gateway. These three are the whole pattern set of the key and the story adds no fourth: DP-04 (the embedded Drools kit), DP-09 (the outbox and inbox library) and DP-05 (the ACE read) are real dependencies of the stage that the plan does not hold, and they are recorded in the registers instead of the metadata table (GAP-3029; ASM-5005, ASM-5055).

**Dependencies the tables add and the plan does not hold.** The three consumed rows are class C dependencies in fact and the plan's C row is None, so the story builds against their documents and fakes on Day 1. The Drools kit of DP-04 would add `RWB-PLT-E1072-CON`; the package is read as data and evaluated by this service's own evaluator, so no kit is declared. The outbox library of DP-09 would add `RWB-PLT-TE006-CON` and is needed only by the stories that publish. The plan's H row stands unchanged.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `WriteOffWorkflow` decision branch | Workflow | Receives the committee decision as a signal on the running stage, reads the package in force and reports the outcome to the parent |
| `recordCommitteeDecision` | Activity | Reads the case, evaluates R-WO-16 with the R-WO-18 refusal, writes the record, sends the answer |
| `CommitteeDecisionEvaluator` | Service | The rule evaluation over the package in force, with the reject branch, the reason test, the state test and the no-fire path |
| `WriteOffDecisionRecordWriter` | Library adapter | Writes the record with the rule ID and the version before any change, hash-linked; refuses the step when the write fails |
| `CommitteeDecisionController` | Controller | The committee-decision operation with its reject branch, the capability area and right A, the `Idempotency-Key` and the problem mapping |
| `CaseClient` | Client | The case read of rwb-case, one hop, 2 s, breaker, no retry of its own |
| `RulePackageClient` | Client | The WO package read of rwb-decision at its version in force |
| `CaseMoveAnswer` | Client | The `RETURNED_TO_PURSUE` answer with the reason and the rule version |
| `WriteOffProposal` | React component | Shows the case, its pack and the recorded decision with its reason on SCR-27, read only |

**Database and migrations.** No Flyway file. The `write_off` table arrives with the DB story of this service, and the record and idempotency key are library objects created in `rwb_writeoff` by the library's migration (DP-03). No column is added for the reason, the decision code or the case state: the reason and the code are decision-record inputs with placeholders, and the state and the rule row are facts and rows of their owners (ASM-5053, ASM-5054).

**Configuration and reference data.**

- R-WO-16 and R-WO-18, their from and to states and the reason condition: rule rows of the WO package with their version, never written in code (ASM-5005).
- The reason itself, and the decision code the record carries: free-text and coded values with no list in any source, validated as present and stored with the record (ASM-5053).
- The capability area "Write-off and posting" and its rights: access rows of rwb-access, read through the guard.
- The 2 s budget, the single hop and the breaker are the platform rule of ADR-020; the rejection has no timer.
- Reference data read: the parameters are the WO rule package version in force, the R-WO-16 and R-WO-18 rows with their from and to states and reason condition, and the reason and decision code values; they are read through the reference-data contract of `RulePackageClient`, whose operation is Not specified in the source documents (DOR-RWB-S7-E6019-APP-20; DP-06 and DP-07 are not in this story's pattern set).

**Build steps**

1. The decision branch of `WriteOffWorkflow` and its input record, registered on `rwb-writeoff` as the stage child of `CaseWorkflow`, with the member's decision as its signal.
2. `CaseClient` against its fake, with the 2 s budget, the breaker, the not-in-pack path and the moved-case path (AC1, X4, X5).
3. `RulePackageClient` against its fake, with the version in force recorded with the outcome (AC1).
4. `CommitteeDecisionEvaluator` over the package, with R-WO-16, the R-WO-18 refusal and the no-fire path (AC1, X3).
5. `WriteOffDecisionRecordWriter` against the stub, with the failed-write path (AC1, AC2, X1).
6. `CaseMoveAnswer` with the `RETURNED_TO_PURSUE` move and the reason (AC1, X4).
7. `CommitteeDecisionController` with the reject branch, the rights, the `Idempotency-Key` and the problem mapping of the declared errors, and `WriteOffProposal` on SCR-27 through the composite route fake (AC1, X2, X7).
8. The boundary test: no statement outside `rwb_writeoff`, no `v_ace_*` read, no write to `rwb_case`, `rwb_decision` or any other schema, and no write to a column of `write_off` (X8, BR1, BR5, BR6).

**Feature flag.** `rwb.writeoff.committee-decision-v1`, a flag of the platform library; off means the operation answers 503 with no write and SCR-27 hides the decision actions, and the scan, the pack and the routing stories are unaffected.

**Done when.** The tests of section 16 pass, the step runs from a synthetic in-committee case in SIT, R-WO-16 returns a case to the pursue track with its reason recorded, a missing reason and a moved case are refused, a repeated key writes once, a forced record failure changes nothing, no `recovery_case` row, no `write_off` column write and no `v_ace_*` read exists in the build, and SCR-27 answers through the composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S7-001 | Carried from the legacy message set of RWB-E6-019: the scan is held for an absent tax criteria version (R-WO-03), so no pack reaches the committee. Raised by RWB-S7-E6013-APP, not by this step | The scan is on hold until Finance publishes the tax criteria. |
| MSG-GEN-001 | The reason is absent on a reject, or a required element of the request is invalid (X3) | Enter {field}. |
| MSG-P4-002 | A role without the Write-off and posting right A calls the decision (X2) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the case moves (X1) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The four IDs are those of the legacy message set; the text is the legacy and FSD wording, copied unchanged, and no message is reworded and no new one is added. MSG-S7-001 is kept because the legacy table of RWB-E6-019 lists it and because the hold is the only reason a pack is not in committee; it is not raised by this step, whose own validation is the presence of the reason.

### 15. Screens and states

SCR-27 Write-off proposal, in its in-committee state and its post-decision state, is served through the gateway-bff composite route (DP-19). The route calls rwb-writeoff for the pack, the decision and the reason, and rwb-case for the case and its route state; this story fixes the rwb-writeoff answers only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON.

The legacy screen table gives the states "Scan; proposed; in committee; approved". This story produces the decision read from the in-committee state: a rejected case shows the rejection, its reason and its time, and leaves the committee population for the pursue track. The scan state is RWB-S7-E6013-APP's, the proposed state RWB-S7-E6015-APP's, the routing into committee RWB-S7-E6017-APP's, the approved state RWB-S7-E6018-APP's and the deferred state RWB-S7-E6020-APP's. The refusal, missing-reason and not-recorded states read the messages of section 14.

The further states of SCR-27 are these. The empty state, shown when no write-off is in the in-committee state, has its wording Not specified in the source documents (DOR-RWB-S7-E6019-APP-10). The loading state, shown while the composite route answers, has its wording Not specified in the source documents (DOR-RWB-S7-E6019-APP-10). The error state, shown when the pack or the decision cannot be read, has its wording Not specified in the source documents (DOR-RWB-S7-E6019-APP-10); a decision that cannot be recorded shows MSG-P7-003. The no-access state, shown to a role without the Write-off and posting right A, shows MSG-P4-002 and no decision action, with no read (TC-E6-019-03). The empty, loading, error and no access states of SCR-27 are not in Screen Specifications v1, so each is Not specified in the source documents (CG-ALL-11013).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E6-019-01 | AC1 | Component | The 40-case in-committee population on the fake with `RC-2026-000731`; the record, the answer and the decision state asserted |
| TC-E6-019-02 | AC2 | Component | The decision-record stub stopped; nothing written, no answer sent and MSG-P7-003 shown |
| TC-E6-019-03 | AC3, Access | Component | A role without the Write-off and posting right A; 403 with MSG-P4-002 and no read |
| TC-E6-019-04 | Principle 5 | Component | A forced decision record write failure inside the transaction; the case stays at `WITH_COMMITTEE` and no record exists |
| TC-E6-019-05 | §12 operations, events and activities (contract) | Component | The published `POST /write-offs/{writeOffId}/committee-decision` operation on `/api/recovery/writeoff/v1` (API-S7-002), the `recordCommitteeDecision` activity and the `WriteOffWorkflow` signals of §12.5 checked against it; no event published (§12.3) |
| TC-E6-019-06 | AC4, BR1, BR5, BR6, §12.7 tables (ASM-3438) | Component | Boundary test of the grant and the build statements against the tables of §12.7: `write_off` read only, no write to its columns, no `v_ace_*` view, no `recovery_case` row, no other service's schema; a forced breach fails the build |
| TC-E6-019-07 | AC5, BR8 | Component | The same request and the same `Idempotency-Key` sent twice; one record and one answer; a case that has left `WITH_COMMITTEE` refused with 409 |
| TC-E6-019-08 | AC6, BR9 | Component | A decision reason carrying a name, an address, a contact value or an identity number; the reason is screened before it is stored and nothing of it reaches `rwb_writeoff`, the record, a log or a workflow input |
| TC-E6-019-09 | AC3, X2, Access | Component | A role without the Write-off and posting right A; 403 with MSG-P4-002, no read and no write |
| TC-E6-019-10 | AC4, X8 | Component | A statement, a test and a component reaching a `v_ace_*` view, a `recovery_case` row and another service's schema; the grant refuses it and the build fails |
| TC-E6-019-11 | AC7, X4 | Component | A case not at `WITH_COMMITTEE`, and a decision already taken; 409 and nothing written |
| TC-E6-019-12 | AC8 | Component | A request with no valid identity, a role without the right and an unknown `writeOffId`; 401, 403 and 404 with the platform error envelope and nothing written |
| TC-E6-019-13 | AC9, X7 | Component | The same `Idempotency-Key` replayed after a decision is written; no second record and the first answer returned |
| TC-E6-019-14 | AC10, X5 | Component | The `recordCommitteeDecision` activity retried and timed out on the fake; one write and no move answered before the record |
| TC-E6-019-15 | AC11, X5 | Component | The rwb-case or rwb-decision fake fails or does not answer inside 2 s; nothing written and 503 with the platform error envelope |

The four legacy cases are those of RWB-E6-019 in their legacy order, with the Level column added: every case is tested on the fakes, so every case is `Component`. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same ID; no `-ITG` copy is written by this story, and the cross-service journey belongs to the wave 4 harness.

### 17. Guardrails

- No business value in code: R-WO-16, R-WO-18, its states, the reason condition, the decision code, the package version and the capability rights stay rule rows and reference data, never a constant, a default or a branch.
- No personal data in `rwb_writeoff`, in a workflow input or in a log: identifiers, amounts, dates, states, a reason and a rule version only, and every fixture is synthetic.
- ACE data only through the owner's contract: this service holds no `v_ace_*` grant and reads no ACE table, and a build that adds one fails the boundary test (BR6).
- The case stays with rwb-case: no `recovery_case` row, no case state column and no case write here (BR4).
- The write-off row is read, not written: no column of `write_off` is set by a rejection (BR1).
- One base, one topic, one queue, one schema and one login per service; no document names another service's base or topic as its own (DP-13, DP-14).
- No retired element is reintroduced: no shared job table, no Quartz row, no monolith base, no event published by this step and no write to the retired legacy log.
- The decision is recorded before the change; a build that answers the move outside the record's transaction fails the review (DP-03).
- The reason is stored as staff-entered text: it is screened for personal data before it is written, and no identity value is ever copied into the record.

### 18. Traceability

| Requirement ID | Requirement (short) | Feature | L3 process | Story element | Test cases |
|---|---|---|---|---|---|
| REQ-S7-003 | The committee decision to approve, reject or defer is recorded against each account (FSD S7 Requirements served) | FEAT-WOF-07 | Not specified in the source documents (DOR-RWB-S7-E6019-APP-2) | The reject branch of the committee decision: R-WO-16, the record, the case-move answer and the operation | TC-E6-019-01, TC-E6-019-02, TC-E6-019-03, TC-E6-019-04 |
| ADR-013 | 19 services inside ACE | FEAT-WOF-07 | Not specified in the source documents (DOR-RWB-S7-E6019-APP-2) | rwb-writeoff as the owner of the write-off stage | TC-E6-019-01 |
| ADR-014 | Schema and login per service | FEAT-WOF-07 | Not specified in the source documents (DOR-RWB-S7-E6019-APP-2) | `rwb_writeoff` and its own login | TC-E6-019-01 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | FEAT-WOF-07 | Not specified in the source documents (DOR-RWB-S7-E6019-APP-2) | The three consumed rows with their budget and breaker | TC-E6-019-01 |
| ADR-022 | Local decision record plus central ledger | FEAT-WOF-07 | Not specified in the source documents (DOR-RWB-S7-E6019-APP-2) | The record written before the case moves | TC-E6-019-02, TC-E6-019-04 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E6-019, disposition Split (rework); feature FEAT-WOF-07 |
| Legacy criteria | AC1 and AC2, owned word for word by this story |
| Wave and release | Wave 4 and release 30 April 2027 (tentative), copied unchanged from the plan; EP06 and the service wave agree at 4, so no W-MAP conflict is raised (ASM-5058) |
| Source text | Legacy RWB-E6-019; FSD S7 Write-off and recovery v3 A2.7, Requirements served and Screens; TSD S7 Write-off and recovery v2 T2, T3.1, T3.2, T4, T5.3, T6.1 and T-A; Business Rules and Routing Logic v4 rows R-WO-16 and R-WO-18 |
| Test cases | TC-E6-019-01 to TC-E6-019-04 |
| Feature and screens | FEAT-WOF-07, SCR-27 Write-off proposal |
| Rules | R-WO-16, with R-WO-18 as the refusal of an incomplete decision, governed in rwb-decision |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-020, ADR-022 |

### 19. Out of scope

- The published shape of the committee decision, the `CommitteeDecision` and `DecisionLogEntry` elements, the reason field, the consumed rows, the error set and the fakes: RWB-S7-E6019-CON.
- The monthly scan, the tax criteria, the pack and the routing into committee: RWB-S7-E6013-APP to RWB-S7-E6017-APP.
- The approval inside the limit and the credit-committee escalation of R-WO-12, R-WO-13 and R-WO-15, and the credit-committee rejection of R-WO-14: RWB-S7-E6018-APP.
- The deferral of R-WO-17 and the review timer of R-WO-19: RWB-S7-E6020-APP.
- The posting, `WriteOffApproved` (`EV-24`), the provision release and the reconciliation: RWB-S7-E6021-APP to RWB-S7-E6023-APP.
- The `committee_date` of an approved write-off and every other column of `write_off`: none is written by a rejection (BR1).
- The onward path of a case from `RETURNED_TO_PURSUE`: no row of TSD S7 T4 publishes it and no story of this split claims it (GAP-3029; ASM-5054).
- The case of record, its route states and the parent `CaseWorkflow`: rwb-case (P3); the ACE data products: rwb-source-data (P1); the WO package and its rule rows: rwb-decision (P7).
- The gateway-bff composite route and the screen field list of SCR-27: RWB-PLT-N001-CON and the edge stories.
- The cross-service journey of the legacy key and its evidence: the wave 4 harness, which copies none of these criteria.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
