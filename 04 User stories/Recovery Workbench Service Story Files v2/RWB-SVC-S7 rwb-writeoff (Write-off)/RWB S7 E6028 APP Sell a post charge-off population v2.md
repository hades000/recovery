# RWB-S7-E6028-APP Sell a post charge-off population

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S7-E6028-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-writeoff |
| Service epic | RWB-SVC-S7 |
| Wave | 4 |
| Business epic | EP06 |
| Release | 30 April 2027 (tentative) |
| Legacy key | RWB-E6-028 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | L-S7-P |
| Ready to start | Day 1 |
| Size | Sized by the squad at refinement; no size value in the source documents (DOR-RWB-S7-E6028-APP-16) |
| Depends on (build) | RWB-S7-E6028-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Contract fake library version | Not specified in the source documents (DOR-RWB-S7-E6028-APP-22) |
| Contract version built against | /api/recovery/writeoff/v1 (path version /v1); contract version number Not specified in the source documents (DOR-RWB-S7-E6028-APP-23) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S7 rwb-writeoff v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: the sale-selection slice of RWB-E6-028 in rwb-writeoff. The four legacy criteria are kept word for word with their origin tag; the step evaluates R-WO-32 of the WO package from `PLACEMENT_DECIDED` on `SALE_SELECTED` where `placement_type = sale`, records the decision through the local decision-record library before any change (DP-03), writes the WRITEOFF state `SOLD_POST_CHARGEOFF` on `write_off.state` and answers rwb-case the same move so the parent `CaseWorkflow` hands the population to the debt sale stage in rwb-debtsale, and serves the sale-selection operation and the sold-population read on base `/api/recovery/writeoff/v1` (DP-13), reached from SCR-27 through the gateway-bff composite route (DP-19). No source publishes a sale-selection operation, `placement_type` and the sale reference have no column, no field ID and no list, the plan's C row is empty while the step consumes three contracts, the entry state `PLACEMENT_DECIDED` is produced by R-WO-29 which no S7 story claims, AC2's R-WO-12 is the branch RWB-S7-E6018-APP already builds, and the debt sale officer holds right R only in TSD S7 T6.1 (GAP-3049; ASM-5125 to ASM-5058). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-S7-E6028-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (28 resolved, 17 cross-document, 2 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **debt sale officer (RW-DEBTSALE)**, I want **to open the sale of charged-off accounts, with the approval the limit requires**, so that **write-offs follow the criteria and the committee's decision**.

This is the sale-selection slice of legacy RWB-E6-028. It owns:

- the four legacy criteria of the key (AC1 to AC4), copied verbatim with their origin tag, and the rules, messages, permission rows and screen they rest on;
- the sale-selection step of `WriteOffWorkflow` on task queue `rwb-writeoff`, as the stage child of `CaseWorkflow` (Temporal and Drools Design slides 5, 12 and 13);
- the evaluation of R-WO-32 against the WO package version in force, from `PLACEMENT_DECIDED` on `SALE_SELECTED` where `placement_type = sale`, and the assertion of the R-WO-12 escalation of AC2 on the pack-stage branch that exists in this service (FSD S7 A2.16.3.1; Business Rules and Routing Logic v4);
- the local decision record of the sale decision, written through RWB-PLT-E1027-CON before any change (DP-03), with the rule ID, the package version, the case and write-off references and the case move;
- the WRITEOFF state `SOLD_POST_CHARGEOFF` on the `write_off` row and the answer to rwb-case for the same move, so the case of record moves and the parent `CaseWorkflow` starts the debt sale stage on the owner's queue;
- the handed-over population for rwb-debtsale: the sold-population read of this service, from which S6 builds its lots (RWB-S6-E5024-APP);
- the sale-selection operation and the sold-population read on base `/api/recovery/writeoff/v1` (DP-13) and the post-charge-off state of SCR-27 Write-off proposal behind the gateway-bff composite route (DP-19).

It does not own: the published shape of the two operations, the elements, the placeholders, the consumed rows, the error set and the fakes, which are RWB-S7-E6028-CON; the scan (RWB-S7-E6013-APP), the tax criteria (RWB-S7-E6014-APP), the pack (RWB-S7-E6015-APP), the removal (RWB-S7-E6016-APP), the routing (RWB-S7-E6017-APP) and the three committee decisions (RWB-S7-E6018-APP to RWB-S7-E6020-APP); the posting and `WriteOffApproved` (RWB-S7-E6021-APP), the provision feed (RWB-S7-E6022-APP), the reconciliation (RWB-S7-E6023-APP), the exception loop (RWB-S7-E6024-APP), the retention close (RWB-S7-E6025-APP), the criteria change (RWB-S7-E6026-APP) and the post charge-off payment (RWB-S7-E6027-APP); the post charge-off decision of R-WO-29, which no S7 story claims and which the placement stories of S9 carry (ASM-5129); the lots, the reserve, the award, the buyer portal and the debt sale cap, which are rwb-debtsale's (RWB-S6-E5024-APP, RWB-S6-E6001-APP, RWB-S6-E6005-APP, RWB-S6-E6012-APP); the agency placement of R-WO-30 (RWB-S9-E6034-APP); the case of record and its route states (P3); the ACE data products (P1); the WO package and its 51 rules (P7); and the deployment of this build, which is the operations story of this legacy key.

### 2. Business rationale

The feature objective, the problem and the metric are unchanged from the legacy story and the module FSD: the sale of charged-off accounts is opened by a debt sale officer, with the approval the limit requires, because write-off populations are assembled by hand each month (FSD S7 A1.3, A2.16.1), and the packs accepted first time are measured on the decision log and the Workbench records against a target that rises each month, reviewed monthly (FSD S7 A2.16.1). What D-RCV-60 changes is who owns the case, the package, the decision, the population and the buyer side.

- **The sale selection is this service's step.** `write_off` is S7's only table in `rwb_writeoff` (context pack, ownership rows owned by S7; TSD S7 T3.1), and the WO route set of 51 rules over 27 states is the write-off stage's (TSD S7 T4); R-WO-32 is a transition of that stage and runs here.
- **The debt sale route is not.** Lots, reserve and tiered terms, the award, the buyer portal and the cap are rwb-debtsale's, and this story stops at the hand-off (FSD S6; RWB-S6-E5024-APP to RWB-S6-E6012-APP). Counting a sale here would be a business fact this service does not hold.
- **The hand-off is a case move.** The connection matrix carries no S7 to S6 edge (context pack, row S7), and the parent `CaseWorkflow` starts one child workflow per stage on the owner's queue, so "hand the charged-off population to the debt sale route" is answered to rwb-case as the move `SOLD_POST_CHARGEOFF`, and the population reaches S6 on this service's published read (DP-12; ASM-5127).
- **The approval by limit is asserted, not rebuilt.** AC1 asks for "the approval the limit requires"; that approval is R-WO-12 and R-WO-15 of the pack and committee stage, whose branch RWB-S7-E6018-APP already builds, and R-WO-12's from state is `PACK_PREPARED`, so the sale step never re-tests the limit: a case the committee or the credit committee rejected never reaches `PLACEMENT_DECIDED`, because that state lies behind posting (ASM-5128).
- **What is post charge-off.** The case is already written off when this step runs: `POSTED` and `PROVISION_RELEASED` are behind it and the provision feed has gone. A sale therefore releases no provision, posts no write-off and changes no approved amount; the money side of the sale is S6's and the ledger's (R-WO-50, R-WO-51).
- **The decision is recorded first**, which is what legacy AC1 asked for and legacy AC4 tested; a sale selection with no record is no selection.
- **The requirement is shared with the placement route.** REQ-S7-006 says post charge-off treatment is set by rule, including placement with an agency; the sale is the other placement the same rule run decides, and the requirement row is taken from the FSD over the empty plan row (ASM-5133).

No business value moves: `placement_type`, the sale reference, the from and to states, the rule ID, the package version and the limit are values of reference data and of the rule package, read with their version and never written in code.

### 3. Preconditions

- RWB-S7-E6028-CON is published: the sale-selection operation and the sold-population read with their placeholders, the elements, the consumed rows, the `Idempotency-Key` rule, the error set and the fakes are baselined and handed to this story (GAP-3049; ASM-5125).
- The rwb-case case read is published with its fake: the case reference, the case number, the product group, the stage and the state `PLACEMENT_DECIDED`. The operation name is Not specified in the source documents (GAP-3049; ASM-5127).
- The case-move answer of rwb-case is available for the fake: the move `SOLD_POST_CHARGEOFF`. No source publishes a REST operation that moves a case state on behalf of a stage; on the workflow boundary the answer is the stage outcome the parent `CaseWorkflow` applies (GAP-3049; ASM-5127).
- The rwb-decision rule-package read is published with its fake and answers the WO package at its version in force, with R-WO-12 and R-WO-32 among its 51 rules over 27 states (GAP-3049; ASM-5132).
- RWB-PLT-E1027-CON is published with its writer fake: the local decision-record library writes in the caller's transaction, and a failed write stops the action with MSG-P7-003 (DP-03).
- RWB-PLT-N001-CON is published: SCR-27 reaches this service through the gateway-bff composite route, one hop, and no screen calls a service directly (DP-19).
- `write_off` exists in schema `rwb_writeoff` from the DB story of this service, with the columns of DF-FIN-010 to DF-FIN-020 and the standard record columns of TSD S7 T3.0; this story adds no table, no column and no migration (ASM-5126).
- The case is at `PLACEMENT_DECIDED` with its post charge-off treatment decided under R-WO-29. That entry state is produced by a rule this key does not build and is read here as a state of the case and of the write-off row (GAP-3049; ASM-5129).
- The service runs as its own login on schema `rwb_writeoff`; it holds no grant on another `rwb_*` schema and no `v_ace_*` grant, so a statement on `rwb_case` or on an ACE view is refused by the database and fails the boundary test.
- No approval is needed to build against a Draft contract baseline; the contract is tagged by RWB-S7-E6028-CON when its tests pass.

### 4. Flow

1. RWB-S7-E6027-APP has posted the recovery and R-WO-29 has decided the post charge-off treatment, so the case and the write-off row sit at `PLACEMENT_DECIDED` with `placement_type = sale` (ASM-5129).
2. The debt sale officer opens SCR-27 Write-off proposal through the gateway-bff composite route and sees the charged-off population at that state, with the amount, the committee date and the posting date read from this service, one hop (DP-19).
3. The officer selects the account for sale. The screen sends the write-off reference, the selection, the sale reference and the officer's identity, with an `Idempotency-Key`.
4. The sale step of `WriteOffWorkflow` on queue `rwb-writeoff` receives the request as a signal to the running stage, with the write-off reference and the package version read from rwb-decision in force (DP-12; ASM-5132).
5. The step reads the case on the rwb-case contract and the `write_off` row on its own schema: the case reference, the state `PLACEMENT_DECIDED`, the amount and the approval facts. A case that is not at `PLACEMENT_DECIDED`, or a write-off with no approval behind it, is refused with 409 and nothing is written (ASM-5127, ASM-5128).
6. `SaleSelectionEvaluator` evaluates R-WO-32: from `PLACEMENT_DECIDED`, on `SALE_SELECTED`, where `placement_type = sale`, the action is "Hand the charged-off population to the debt sale route" and the state is `SOLD_POST_CHARGEOFF`. Where `placement_type` is another value, the rule does not fire and the account stays at `PLACEMENT_DECIDED` (FSD S7 A2.16.3.1; Business Rules and Routing Logic v4).
7. The evaluation answers the rule ID, the package version, the action of the rule, the selection and the case move the rule names.
8. `WriteOffDecisionRecordWriter` writes one decision record through the local decision-record library, **before any change**: the case and write-off references, the decision, the rule ID `R-WO-32` with its package version, the selection, the from state, the to state and the decided-at time, chained to the approval record it links to. A failed write stops the step with nothing changed (DP-03; legacy AC1 and AC4).
9. `WriteOffSaleWriter` updates the `write_off` row in the same `rwb_writeoff` transaction, with the optimistic lock of `version`: `state` becomes `SOLD_POST_CHARGEOFF` (ASM-5131).
10. `CaseMoveAnswer` answers rwb-case with the move `SOLD_POST_CHARGEOFF` and the rule version, and the parent `CaseWorkflow` starts the debt sale stage on `rwb-debtsale`; this service writes neither the `recovery_case` row nor a route state (ASM-5127).
11. rwb-debtsale reads the sold population on the published read of this service and builds its lots (RWB-S6-E5024-APP). The lot, the reserve, the award and the buyer are not this story's (ASM-5127).
12. The officer sees the account leave the population with its selection and its time recorded; a repeated request with the same `Idempotency-Key` answers the selection it created and writes nothing a second time.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The local decision record cannot be written | Nothing changes: no state is written, no move is answered and no record exists | MSG-P7-003 | AC4, TC-E6-028-04, TC-E6-028-06 |
| X2 | The role does not hold the Write-off and posting right the operation declares | 403 before any read or write; nothing changes | MSG-P4-002 | AC5, TC-E6-028-05 |
| X3 | The request lacks the write-off reference or the selection | 422 and nothing is recorded; the account stays at `PLACEMENT_DECIDED` | MSG-GEN-001 | AC1, X6 |
| X4 | The case is not at `PLACEMENT_DECIDED`, or the selection has already been taken | 409 and nothing is written; a selection is not taken twice | None | AC3, X6 |
| X5 | `placement_type` is not `sale` | R-WO-32 does not fire; the account stays at `PLACEMENT_DECIDED` and the sale is not opened | None | AC3 |
| X6 | The rwb-case or rwb-decision contract does not answer inside 2 s, or its breaker is open | The step retries on the workflow's own schedule; nothing is written and no move is answered; the caller sees 503 | None | AC1, X7 |
| X7 | The case is still held in the scan for an absent tax criteria version or an absent ALS extract | No pack reached the committee and no case is post charge-off, so nothing is at `PLACEMENT_DECIDED` to sell; the hold is raised by RWB-S7-E6013-APP | MSG-S7-001 | AC1 |
| X8 | A component, a statement or a test reaches a `v_ace_*` view, a `recovery_case` row or another service's schema | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | AC6, Section 17, BR6, BR7 |

X1 to X4 are the legacy exception paths carried onto the slice, X5 to X7 are the paths the rule condition and the post charge-off entry state add, and X8 is the ACE and schema boundary. The deviation codes X1 to X7 of R-WO-06 are codes of the rule package and are not the path identifiers of this table.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-S7-E6028-CON, the rwb-case and rwb-decision fakes and the decision-record stub, on its own schema, and needs no live P1, P3, P6 or S6 |
| Negotiable | The activity name, the element and path names, the decision code of the record and the shape of the stage outcome are this story's choice; the rule, the messages, the screen, the base and the two states are fixed |
| Valuable | A charged-off population reaches the debt sale route with its selection recorded, so the sale cycle starts from the write-off book of record and not from a hand-built list |
| Estimable | One workflow step, one evaluator, one record write, one row update, one case-move answer, two operations, three clients and one screen state |
| Small | Finished inside two weeks with its tests on the fakes |
| Testable | Each criterion runs on a synthetic post charge-off account through the contract fakes, plus the access, the wrong placement and the failed-record cases |

### 7. Acceptance criteria

```gherkin
Feature: Sell a post charge-off population

  Background:
    Given case "RC-2027-000184" is one of 25 charged-off accounts at state "PLACEMENT_DECIDED" with "placement_type" set to "sale"
    Given the WO rule package is in force at its version and carries R-WO-12 and R-WO-32
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 Sell a post charge-off population (legacy RWB-E6-028 AC1)
    Given the rwb-case contract mock returns the case of record at "PLACEMENT_DECIDED" and accepts the move "SOLD_POST_CHARGEOFF"
    Given the rwb-decision contract mock returns the WO package at its version in force with R-WO-32
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then opens the sale of charged-off accounts, with the approval the limit requires
    Then the system writes the result to the decision record with the rule version

  Scenario: AC2 Rule R-WO-12 (legacy RWB-E6-028 AC2)
    Given the rwb-decision contract mock returns the WO package in force with R-WO-12 and a write-off committee limit below the amount of "WO-2027-000184"
    Given the rwb-case contract mock returns the case of record at "PACK_PREPARED" and accepts the move "ESCALATED_TO_CREDIT_COMMITTEE"
    Given a case in state PACK_PREPARED
    When limit exceeded
    Then route the pack to the credit approval committee chaired by the product head with Risk
    Then the case moves to ESCALATED_TO_CREDIT_COMMITTEE

  Scenario: AC3 Rule R-WO-32 (legacy RWB-E6-028 AC3)
    Given the rwb-decision contract mock returns the WO package in force with R-WO-32
    Given the rwb-case contract mock returns the case of record at "PLACEMENT_DECIDED" and accepts the move "SOLD_POST_CHARGEOFF"
    Given a case in state PLACEMENT_DECIDED
    When sale selected
    Then hand the charged-off population to the debt sale route
    Then the case moves to SOLD_POST_CHARGEOFF

  Scenario: AC4 Not recorded (legacy RWB-E6-028 AC4)
    Given the decision record cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003

  Scenario: AC5 Role without the sale selection right (exception X2) (new, D-RCV-60)
    Given the caller holds no Write-off and posting right the sale selection declares
    When the caller requests the sale selection
    Then the system answers 403 before any read or write
    Then nothing changes and the user sees MSG-P4-002

  Scenario: AC6 Access to a view, a case row or another schema (exception X8) (new, D-RCV-60)
    Given a component, a statement or a test reads a v_ace_* view, a recovery_case row or another service's schema
    When the boundary test runs in the build
    Then the grant refuses the statement and the boundary test fails the build
    Then nothing is released

  Scenario: AC7 Rule values read with their package version (BR8) (new, D-RCV-60)
    Given the write-off package version in force carries rule R-WO-32
    When the sale selection runs
    Then R-WO-32 is read with its package version
    Then the rule ID with its version is recorded in the decision record

  Scenario: AC8 Error answers 401, 403 and 404 of the provided operations (new, D-RCV-60)
    Given the caller sends no valid credentials
    When the caller requests the sale selection
    Then the system answers 401 before any read or write
    Given the caller holds no Write-off and posting right the sale selection declares
    When the caller requests the sale selection
    Then the system answers 403 before any read or write
    Given the write-off reference matches no case of record
    When the caller requests the sale selection
    Then the system answers 404 and nothing is written

  Scenario: AC9 Replay of a write with the same idempotency key (new, D-RCV-60)
    Given the same write-off reference and the same Idempotency-Key are sent twice
    When the second request runs
    Then one decision record and one case move exist
    Then the answer is the answer of the first run

  Scenario: AC11 A consumed call fails or does not answer (exception X6) (new, D-RCV-60)
    Given the rwb-case or rwb-decision contract does not answer inside 2 s or its breaker is open
    When the sale selection runs
    Then nothing is written and no move is answered
    Then the caller sees 503

  Scenario: AC12 A status change the model does not allow is refused (exception X4) (new, D-RCV-60)
    Given the case is not at "PLACEMENT_DECIDED" or the selection has already been taken
    When the sale selection is requested
    Then the system answers 409 and nothing is written

  Scenario: AC10 Activity retry and timeout (new, D-RCV-60)
    Given the activity recordSaleSelection is retried after a failure or a timeout
    When the retry runs
    Then the decision record and the case move exist once for the write-off reference, as after a single run
    Then the answer is the answer of the first run
```

The four criteria are the legacy criteria of RWB-E6-028 with their origin tag added and the record term renamed (CG-ALL-11243): the repeated `Then`, the wording of `the user acts on the screen`, `limit exceeded`, `sale selected`, `the action is taken` and `the decision record cannot be written` all stand. The cross-service parts are mocked, so AC1 and AC3 carry two `Given the <service> contract mock returns <x>` lines each and AC2 carries one plus the accepted move, and those lines and the feature Background are the only additions. AC4 has no cross-service part and is copied with nothing added. AC5 and AC6 are not legacy criteria: they are written for this story to cover exceptions X2 and X8 of section 5. AC10 is not a legacy criterion either: it is written for this story for the retry and timeout of `recordSaleSelection` (section 12.5).

What the legacy lines describe now happens in three places: rwb-decision holds the package and the limit, rwb-case owns the case and its route states, and this story evaluates R-WO-32, evaluates the limit test of R-WO-12 on the branch that already exists, writes the record and the WRITEOFF state, and answers the move. Legacy AC2 and AC3 say "the case moves to .": the case route state is rwb-case's and is answered, while the named values are also the WRITEOFF states this service writes on `write_off.state` (ASM-5131). AC2's from state is `PACK_PREPARED`, the pack stage of RWB-S7-E6018-APP's branch and not `PLACEMENT_DECIDED`, so the criterion is proven on that shared branch and the sale step does not evaluate R-WO-12 a second time (ASM-5128). The `decision log` of the legacy text is the local decision record of DP-03 in `rwb_writeoff`, with the central `decision_log_entry` ledger of rwb-decision behind it.

### 8. Business rules

| Rule | Route set | Decision | From state | Event | Condition | Action | To state | Owner | Systems | Timer |
|---|---|---|---|---|---|---|---|---|---|---|
| R-WO-12 (BR4) | Write-off | D9 | PACK_PREPARED | LIMIT_EXCEEDED | amount above the write-off committee limit | Route the pack to the credit approval committee chaired by the product head with Risk | ESCALATED_TO_CREDIT_COMMITTEE | Credit approval committee | Committee View, Reference data | before the scheduled meeting |
| R-WO-32 (BR1, BR3) | Write-off | D9 | PLACEMENT_DECIDED | SALE_SELECTED | placement_type = sale | Hand the charged-off population to the debt sale route | SOLD_POST_CHARGEOFF | Debt sale officer | buyer portal, Workbench | per cycle |

The two rows are the rows of the Business Rules and Routing Logic v4, copied character for character except the BR ID added in the ID cell, and they are rows of the WRITEOFF machine of TSD S7 T4. Their owner and systems columns name a business role and systems, not services: "Credit approval committee" is the escalation RWB-S7-E6018-APP builds, "buyer portal" is the rwb-debtsale and partner side, "Workbench" is SCR-27 read through the composite route, and "per cycle" is the monthly sale cycle of RWB-S6-E6005-APP and not a timer of this service. R-WO-12's from state is `PACK_PREPARED`, so this step asserts the branch and does not re-run it (ASM-5128). R-WO-29, the post charge-off rule run that fills `PLACEMENT_DECIDED`, R-WO-30, the agency placement, and R-WO-50, the settled sale, are rows this step does not own (ASM-5127, ASM-5129).

| ID | Rule | Source | Covered by |
|---|---|---|---|
| BR1 | The sale selection is a transition of the write-off stage: R-WO-32 runs in `WriteOffWorkflow` on `rwb-writeoff`, writes `write_off.state` = `SOLD_POST_CHARGEOFF` and answers the case move | TSD S7 T3.1, T4; context pack ownership rows (table and workflow); FSD S7 A2.16.2 | AC1, AC3, TC-E6-028-01, TC-E6-028-03 |
| BR2 | The decision is recorded before the row changes and before the move is answered, with the rule ID, the package version, the selection and the two states; a failed write changes nothing and the caller sees MSG-P7-003 | DP-03; TSD S7 T2 ("writes the decision log entry before any change"); legacy AC1 and AC4 | AC1, AC4, TC-E6-028-04, TC-E6-028-06 |
| BR3 | Only a case at `PLACEMENT_DECIDED` with `placement_type = sale` is sold; another state or another placement type is refused, and the condition is the whole test of the rule | Business Rules and Routing Logic v4 row R-WO-32; FSD S7 A2.16.3.1 | AC3, X5, TC-E6-028-03 |
| BR4 | The limit approval is asserted, not re-run: R-WO-12 starts from `PACK_PREPARED` and its branch is RWB-S7-E6018-APP's; the sale step refuses a write-off with no approval behind it | ASM-5128; FSD S7 A2.16.3.1 | AC2, TC-E6-028-02 |
| BR5 | The hand-off is the case move plus the sold-population read: this service calls no rwb-debtsale operation, publishes no event for the hand-off and writes no lot, reserve or award | ASM-5127; context pack connection matrix row S7; DP-12 | AC1, TC-E6-028-01 |
| BR6 | No cross-schema join and no foreign key leaves `rwb_writeoff`; `case_id` and `decision_log_id` are identifiers of another service's fact | DP-01; TSD S7 T3.3 | AC6, TC-E6-028-08 |
| BR7 | ACE data only through the owner's contract: this service holds no `v_ace_*` grant and reads no ACE table; the balance, the provision and the tax result reach it on the write-off facts of its own schema and on the pack | DP-05 as a prohibition; FSD S7 A1.1; TSD S7 T1 | AC6, TC-E6-028-08 |
| BR8 | Every value a business person may change is a rule row or reference data read with its version: R-WO-32, its states, `placement_type`, the sale reference and the package version | FSD S7 BR-S7-016; legacy Guardrails | AC7, TC-E6-028-09 |
| BR9 | The same request twice, or the same `Idempotency-Key` twice, writes one record and sends one answer; a case that has left `PLACEMENT_DECIDED` is refused with 409 | TSD S7 T-A.2 | AC9, AC12, TC-E6-028-09 |
| BR10 | No person name, address, contact value or identity number enters `rwb_writeoff`, the decision record, a log or a workflow input; the case reference is a number and not an identity | Template and Rules §R7.2 (s17); TSD S7 T6.2 | TC-E6-028-10 |

### 9. State transitions

The case route state is rwb-case's; this story answers the move and the parent `CaseWorkflow` applies it (BR5). The WRITEOFF state on the write-off row is this service's and is the one written here.

| From (case state, rwb-case) | Event | Condition | To | Written by |
|---|---|---|---|---|
| `PLACEMENT_DECIDED` | `SALE_SELECTED` | `placement_type = sale` | `SOLD_POST_CHARGEOFF` | rwb-case, on this story's answer; `write_off.state` by this story |
| `PLACEMENT_DECIDED` | `SALE_SELECTED` | `placement_type` is another value, or the case is not at the state | Unchanged | none; R-WO-32 does not fire, 409 |
| `PACK_PREPARED` | `LIMIT_EXCEEDED` | amount above the write-off committee limit | `ESCALATED_TO_CREDIT_COMMITTEE` | rwb-case, on the answer of RWB-S7-E6018-APP (R-WO-12) |
| `PLACEMENT_DECIDED` | `SALE_SELECTED` | The rule fires but the record cannot be written | Unchanged | none; X1 and MSG-P7-003 |
| `SOLD_POST_CHARGEOFF` | `SALE_SETTLED` | buyer settles and the data transfer completes | `CASE_CLOSED` | rwb-case, on the answer of RWB-S6-E6005-APP and RWB-S6-E6010-APP (R-WO-50); not this story |
| `SOLD_POST_CHARGEOFF` | `PAYMENT_BELONGS_TO_BUYER` | the account was sold before the payment arrived | `REMITTED_TO_BUYER` | RWB-S7-E6027-APP (R-WO-40); not this story |

| Step execution | Event | Condition | To |
|---|---|---|---|
| Waiting | A sale selection for a case of the population | The package in force is read | Evaluating |
| Evaluating | R-WO-32 fires | `placement_type = sale` and the case is at `PLACEMENT_DECIDED` | Applying |
| Evaluating | R-WO-32 does not fire | Another placement type, another state, or no package | Waiting, nothing changed |
| Applying | The record is written, the row updated and the answer sent | The transaction commits | Waiting for the next request |
| Applying | The record write or the row update fails | X1 | Waiting, nothing changed |

The states `PLACEMENT_DECIDED` and `SOLD_POST_CHARGEOFF` are those of the WO machine of TSD S7 T4 and live on the case of record and on `write_off.state`; this step writes the row and answers the case. The entry state is filled by R-WO-29, which this key does not build (ASM-5129).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-DEBTSALE, debt sale officer | Write-off and posting R in TSD S7 T6.1 and the primary role of FSD S7 A2.16.3.3; it selects a charged-off account for sale and reads the population. The capability right of the selection is the C of a population change and its confirmation is recorded (GAP-3049; ASM-5130) |
| RW-WRITEOFF, write-off team member | Write-off and posting CRU: reads the sold population and its selection; it does not hold the committee approval right A |
| RW-CREDITAD, Credit Administration officer | Write-off and posting CRUA: selects and reads, and holds the posting and the closing steps of the later stories |
| RW-PRODHEAD, product head; RW-WOCOMM, write-off committee member; RW-FINANCE, Finance and CFO delegate | Write-off and posting RA: they take the limit decision of R-WO-12 and R-WO-15 in RWB-S7-E6018-APP, and read the sold population here |
| RW-FRAUD, RW-CONDUCT, RW-RISK, RW-COE, RW-AUDIT, RW-BIANAL, RW-TRIBE | Write-off and posting R: read only, in scope |
| SY-CASEWF, SY-RULES, SY-AGENT, SY-DATALOAD | Write-off and posting R or U as the matrix gives it: the service identities run the step and are subject to the same checks |
| rwb-writeoff service identity | Evaluates the rule, writes the record and the row, answers the move and serves the two operations; it holds no grant on another schema and no `v_ace_*` grant |

The rights are the rows of TSD S7 T6.1 and nothing wider. The FSD names the debt sale officer as the primary role and the Head of Asset Liquidity as also using the step, and TSD S7 T6.1 gives RW-DEBTSALE right R and carries no Head of Asset Liquidity row, so the operation is declared at right C of Write-off and posting and the role wording is recorded rather than resolved (GAP-3049; ASM-5130). DP-08 is not in this story's pattern set: the capability area and the right are declared per operation and the access guard is a service-template capability: each operation calls the rwb-access authorise check for its capability area and right before any read or write, and that check is stated here and not built here.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-FIN-010 | write_off (S7, `rwb_writeoff`) | id | Read, the write-off reference the operation takes as `writeOffId` |
| DF-FIN-011 | write_off (S7, `rwb_writeoff`) | case_id | Read, the case the sale is selected for |
| DF-FIN-012 | write_off (S7, `rwb_writeoff`) | decision_log_id | Read, the record reference the committee step set; the new record of this step chains to it and the column is not overwritten |
| DF-FIN-013 | write_off (S7, `rwb_writeoff`) | amount | Read, the charged-off amount; a sale changes no amount |
| DF-FIN-014 | write_off (S7, `rwb_writeoff`) | tax_criteria_met | Read, the result RWB-S7-E6014-APP wrote |
| DF-FIN-015 | write_off (S7, `rwb_writeoff`) | committee_date | Read, the approval date the sale depends on; not written here |
| DF-FIN-016 | write_off (S7, `rwb_writeoff`) | posted_date | Read, the posting date RWB-S7-E6021-APP set; not written here |
| DF-FIN-017 to DF-FIN-019 | write_off (S7, `rwb_writeoff`) | responsibility_center, cost_center, gl_product | Read only: the ledger side of the posting, not this step's |
| DF-FIN-020 | write_off (S7, `rwb_writeoff`) | recovered_after | Not written here: the recovery stories (RWB-S7-E6027-APP) |
| Standard columns | write_off (S7, `rwb_writeoff`) | `state`, `version`, `updated_at`, `updated_by` | Write: `state` = `SOLD_POST_CHARGEOFF`, `version` as the optimistic lock, the time and the service identity; `is_active`, `created_at` and `created_by` are read |
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library, created in `rwb_writeoff`) | rule id, rule version, decision code, selection, from and to state, decided at | Write through the local library, before the row changes |
| DF-CAS-001 to DF-CAS-023 | recovery_case (P3) | id, case_no, product_group, primary_person_key, status, stage_code and 17 more | Not read as a table and not written: the state arrives on the rwb-case contract and the move returns on its answer |
| DF-REF-001 to DF-REF-015 | rule_row (P7) | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | Not read as a table: the rule arrives on the package read |
| `placement_type` | the condition of R-WO-32 | Read as a request input and recorded in the decision record; it has no column in `write_off`, no field ID and no list of values, so its value set is Not specified in the source documents (GAP-3049; ASM-5126) |
| The sale reference | the identifier of the sale or lot the selection opens | Read as a request input and recorded in the decision record; it has no column, no field ID and no format, so it is Not specified in the source documents (GAP-3049; ASM-5126) |

Field IDs are those of TSD S7 T3.1 and the Logical Data Model and Data Dictionary, and the case, ledger and rule rows are the rows the legacy Data table lists, with their owners changed to P3 and P7 by the target. **No new table, no new column and no migration**: the table arrives with the DB story of this service, and `decision_record`, `idempotency_key` and `outbox_event` are library objects created in `rwb_writeoff` by the library's own migration (DP-03). This step writes no row to `outbox_event` because it publishes no event (§12.3).

**No personal data.** The rows carry identifiers, amounts, dates, list values, a state, a rule version and a sale reference. No name, address, contact value or identity number enters `rwb_writeoff`, the record, a log or a workflow input, and the fixtures are synthetic. `primary_person_key` is P3's and is never copied here; the buyer and the buyer's data are S6's and the partner gateway's.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-writeoff (S7); base `/api/recovery/writeoff/v1` (DP-13). No source publishes either operation of this step, so both are declared by RWB-S7-E6028-CON with placeholders (GAP-3049; ASM-5125).

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| POST | `/write-offs/{writeOffId}/sale-selection` (operation ID and path Not specified in the source documents (GAP-3049; ASM-5125)) | The sale selection in, with the write-off reference, the selection and the sale reference; the write-off answer out with the rule `R-WO-32` and its version, the state `SOLD_POST_CHARGEOFF` and the record reference | Write-off and posting, right C, scope applied | `Idempotency-Key` header |
| GET | `/write-offs?sale=SOLD_POST_CHARGEOFF` (path and filter Not specified in the source documents (GAP-3049; ASM-5125)) | The sold population: write-off reference, case reference, amount, committee date, posted date and the selection time, paged | Write-off and posting, right R, scope applied | none (a GET) |

The errors are 400, 401, 403 with MSG-P4-002, 404 for a write-off that is not in the population, 409 for a case that has left `PLACEMENT_DECIDED`, 422 with MSG-GEN-001 for an incomplete request and 503 when the library or a consumed contract does not answer. TSD S7 T-A.1 publishes only API-S7-001 and API-S7-002, so neither row is copied from a source document; the rights are the C and R of the capability area and the confirmation of the role right is recorded (ASM-5130). The scan (API-S7-001, right C) is RWB-S7-E6013-APP's and the committee decision (API-S7-002, right A) is RWB-S7-E6018-APP to RWB-S7-E6020-APP's; neither is declared, built or extended here.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| The case read (operation name Not specified in the source documents (GAP-3049; ASM-5127)) | `/api/recovery/case/v1` | P3 rwb-case | The case reference, case number, product group, stage and state of the case at `PLACEMENT_DECIDED`; read only, faked |
| The case-move answer (operation name Not specified in the source documents (GAP-3049; ASM-5127)) | rwb-case (P3) | P3 rwb-case | The move `SOLD_POST_CHARGEOFF` with the rule version; on the workflow boundary it is the stage outcome the parent `CaseWorkflow` applies; faked |
| The rule-package read in force (operation name Not specified in the source documents (GAP-3049; ASM-5132)) | `/api/recovery/decision/v1` | P7 rwb-decision | The WO package at its version, with R-WO-12 and R-WO-32 among its 51 rules over 27 states; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The three rows are contract dependencies of class C that the plan does not carry, because this story's C row is None; the absence is recorded (GAP-3049; ASM-5127, ASM-5132).

#### 12.3 Events published

None. The service publishes on `rwb.writeoff.events.v1` and its event set carries `WriteOffApproved` (`EV-24`, with `writeOffId`, `caseId` and `amount`, consumed by Posting), which belongs to the posting step of R-WO-20 and R-WO-21 and is RWB-S7-E6021-APP's. A sale selection publishes no event of its own: no source names one, S7 has no edge to S6 in the connection matrix, and the hand-off is the case move (ASM-5127). This story therefore declares no event, no producer group and no outbox row, and a build that publishes one fails the absence test. The topic carries the retry and `.dlt` topics of the platform (DP-14), and the outbox and inbox library that relays it is the DP-09 dependency the plan does not carry for this key (ASM-5132).

#### 12.4 Events consumed

None. The service listens to the rwb-source-data and rwb-payment events in its scan and recovery steps (context pack connection matrix, row S7: REST and events to P1, Temporal and events to P8), and neither belongs to the sale selection: the selection reads no ACE extract and moves no money. This story therefore holds no consumer group, no subscription and no inbox row, and a build that adds one fails the absence test. The trigger of the step is the officer's selection on SCR-27 through the composite route, and the FSD declares no background event for the feature beyond the monthly scan of R-WO-01 (FSD S7 A2.16.4.4).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `WriteOffWorkflow` | Workflow, one execution per case at the write-off stage, the child of `CaseWorkflow`, continues-as-new at each stage end | `rwb-writeoff` | Input: the case and write-off references, the cut-off date and the package in force; signals: the sale selection and the case answered by rwb-case; outcome for the parent: the case move |
| `recordSaleSelection` | Activity, the one sale step, with R-WO-32 and the limit assertion of BR4 | `rwb-writeoff` | The write-off reference, the selection, the sale reference and the package version in; the rule ID with its version, the selection recorded, the row state and the case move out, with the record written before the change |

WriteOffWorkflow ID form: Not specified in the source documents (CG-ALL-11239). Start rule: JOB-16 after AceDataReady per Temporal Catalog v1; start or signalWithStart and the duplicate-start policy: Not specified in the source documents (CG-ALL-11239).

No child workflow for the case and none for the money exists in this service. The activity name is a target design choice fixed by no source document; the step runs from the officer's selection, and the monthly scan is the Schedule of RWB-S7-E6013-APP (§12.6). The write-off states are this service's own record inside `WriteOffWorkflow`, and rwb-case moves the case state on the published outcome; the split of the state between this service and rwb-case is an open question with the P3 owner, so that no state has two writers (GAP-1800). Payment matching after charge-off is not run here: the match is the `ProceedsMatched` event (EV-25) published by rwb-payment, the recovery, the income and the agency fee are recorded in this service, a payment that matches nothing is held in the exception list shown here, and the ownership of the initial match is an open question with the P8 owner (GAP-1812). The hand-over of a charged-off population to the debt sale route is carried here as product behaviour, with the population, the route and the approval recorded here; the call type and its direction are an open question with the S6 owner before wave 4 system test (GAP-1799).

#### 12.6 Schedules

None. The sale selection is an officer-driven step and owns no Temporal Schedule. The "per cycle" timer of R-WO-32 is the monthly sale cycle of rwb-debtsale (RWB-S6-E6005-APP), `JOB-16` becomes the Temporal Schedule of R-WO-01 in RWB-S7-E6013-APP, and the placement review timer of R-WO-17 is RWB-S7-E6020-APP's; nothing of them is built or declared here.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| write_off | S7 (`rwb_writeoff`) | The write-off of the balance on a case; this story reads the row and writes `state`, `version`, `updated_at` and `updated_by` |
| Other entity groups of `rwb_writeoff` (eligibility, committee, posting, recovery after charge-off) | S7 (`rwb_writeoff`) | Tables, fields and keys Not specified in the source documents (GAP-1794); written with the S7 DB story, not by this story |
| decision_record | PLT library, created in `rwb_writeoff` | The local hash-linked decision record of the selection (DP-03) |
| idempotency_key | PLT library, created in `rwb_writeoff` | The key of the repeated request and the answer it holds |
| outbox_event | PLT library, created in `rwb_writeoff` | Present as a library object; this step writes no row to it (§12.3) |

Not owned and never read as a table: `recovery_case` and `timer` (P3), every `v_ace_*` view (P1), `decision_log_entry` and `rule_row` (P7), `document` (P5), `notice` (P6), `payment` (P8), `lot` and every debt sale table (S6). No foreign key leaves the schema and `case_id` is an identifier, not a foreign key across schemas (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case case fake | The case of record at `PLACEMENT_DECIDED` with `placement_type` set to sale, `RC-2027-000184` among 25 accounts; a case at another state; a case whose amount is above the write-off committee limit with no escalation | AC1, AC2, AC3, X4 |
| rwb-case case-move fake | The move `SOLD_POST_CHARGEOFF` accepted for `RC-2027-000184` with the rule version; a move refused because the case is not in the expected state | AC1, AC3, X4 |
| rwb-decision rule-package fake | The WO package at its version in force with R-WO-12 and R-WO-32 among its 51 rules over 27 states, and the write-off committee limit | AC1, AC2, AC3 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and outbox, and a stopped chain | AC4, X1 |
| gateway-bff composite route fake | The merged SCR-27 answer for the sold population, before and after a selection | AC1 |

The fakes are test-only and are replaced by the real services in SIT. The operation names and paths of the two provided rows and the three consumed rows carry the placeholder until their owners confirm them (GAP-3049; ASM-5125, ASM-5127, ASM-5132).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 3 consumed | The sale selection and the sold-population read on `/api/recovery/writeoff/v1`; the case read, the case-move answer and the package read; one hop, 2 s |
| Kafka | 0 published, 0 consumed | `WriteOffApproved` (`EV-24`) is RWB-S7-E6021-APP's; no event is published or consumed here (§12.3, §12.4) |
| Temporal | 1 workflow and 1 activity | `WriteOffWorkflow` and its sale step on `rwb-writeoff`; no Schedule |
| File | None | No file is read, built or delivered here; the buyer files are S6's and rwb-integration's |

### 13. Solution plan

**Package.** Java package `th.co.scb.ace.workbench.recovery.writeoff`, module `sale`; front end `src/modules/recovery/writeoff/WriteOffSale.tsx`, the fragment SCR-27 embeds.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the transaction rule of the step: the record, the row update and the answer commit together or not at all. DP-13 moves the base of the legacy `/api/recovery/v1` paths and gives the sale selection and the population read their home. DP-19 is how SCR-27 reaches this service, one hop through the gateway. These three are the whole pattern set of the key and the story adds no fourth: DP-04 (the embedded Drools kit), DP-09 (the outbox and inbox library) and DP-11 (the REST contract from the legacy in-process call to rwb-debtsale) are real dependencies of the step that the plan does not hold, and they are recorded in the registers instead of the metadata table (GAP-3049; ASM-5132).

**Dependencies the tables add and the plan does not hold.** The three consumed rows are class C dependencies in fact and the plan's C row is None, so the story builds against their documents and fakes on Day 1. The Drools kit of DP-04 would add `RWB-PLT-E1072-CON`; the package is read as data and evaluated by this service's own evaluator, so no kit is declared. The outbox library of DP-09 would add `RWB-PLT-TE006-CON` and is needed only by the stories that publish. The hand-off to rwb-debtsale adds no H, C or I row because no edge exists and no operation is called. The plan's H row stands unchanged.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `WriteOffWorkflow` sale branch | Workflow | Receives the selection as a signal on the running stage, reads the package in force and reports the outcome to the parent |
| `recordSaleSelection` | Activity | Reads the case and the row, evaluates R-WO-32, asserts the limit of BR4, writes the record, updates the row and sends the answer |
| `SaleSelectionEvaluator` | Service | The rule evaluation over the package in force, with the placement-type test, the state test and the no-fire path |
| `WriteOffDecisionRecordWriter` | Library adapter | Writes the record with the rule ID and the version before any change, hash-linked; refuses the step when the write fails |
| `WriteOffSaleWriter` | Repository | Updates `state`, `version`, `updated_at` and `updated_by` on the write-off row in the caller's transaction |
| `SaleSelectionController` | Controller | The sale-selection operation with the capability area and its right, the `Idempotency-Key` and the problem mapping |
| `SoldPopulationController` | Controller | The sold-population read, paged and scoped, for rwb-debtsale and for the screen |
| `CaseClient` | Client | The case read of rwb-case, one hop, 2 s, breaker, no retry of its own |
| `RulePackageClient` | Client | The WO package read of rwb-decision at its version in force |
| `CaseMoveAnswer` | Client | The `SOLD_POST_CHARGEOFF` answer with the rule version |
| `WriteOffSale` | React component | Shows the post charge-off population and the selection on SCR-27, read only |

**Database and migrations.** No Flyway file. The `write_off` table arrives with the DB story of this service, and the record and the idempotency key are library objects created in `rwb_writeoff` by the library's migration (DP-03). No column is added for `placement_type`, the sale reference or the selection time: they are request inputs and decision-record facts with placeholders, and the state is the standard record column (ASM-5126).

**Configuration and reference data.**

- R-WO-32 and R-WO-12, their from and to states and the `placement_type` condition: rule rows of the WO package with their version, never written in code (ASM-5132).
- The values of `placement_type`, the format of the sale reference and the decision code the record carries: values with no list in any source, validated as present and stored with the record (ASM-5126).
- The parameters this step reads are R-WO-32 and R-WO-12 with their from and to states, `placement_type` and the write-off committee limit; the reference-data contract is the WO package read of rwb-decision (`RulePackageClient`) at its version in force, and no other list is read (DP-06 and DP-07 are not in this story's pattern set).
- The capability area "Write-off and posting" and its rights: access rows of rwb-access, read through the guard (ASM-5130).
- The 2 s budget, the single hop and the breaker are the platform rule of ADR-020; the sale selection sets no timer, because the cycle is S6's.

**Build steps**

1. The sale branch of `WriteOffWorkflow` and its input record, registered on `rwb-writeoff` as the stage child of `CaseWorkflow`, with the officer's selection as its signal.
2. `CaseClient` against its fake, with the 2 s budget, the breaker, the not-in-population path and the moved-case path (AC1, X4, X6).
3. `RulePackageClient` against its fake, with the version in force recorded with the outcome (AC1).
4. `SaleSelectionEvaluator` over the package, with R-WO-32, the placement-type test, the state test and the no-fire path (AC3, X5).
5. `WriteOffDecisionRecordWriter` against the stub, with the failed-write path (AC1, AC4, X1).
6. `WriteOffSaleWriter` with the optimistic lock and the single transaction of BR2 (AC3).
7. `CaseMoveAnswer` with the `SOLD_POST_CHARGEOFF` move (AC3, X4).
8. `SaleSelectionController` and `SoldPopulationController` with the rights, the `Idempotency-Key`, the problem mapping and the paging, and `WriteOffSale` on SCR-27 through the composite route fake (AC1, X2).
9. The assertion of the shared R-WO-12 branch: the escalation case is run against the branch of RWB-S7-E6018-APP and asserts the limit, the committee and the state; no second implementation is added (AC2, ASM-5128).
10. The boundary test: no statement outside `rwb_writeoff`, no `v_ace_*` read, no write to any schema but `rwb_writeoff`, and no publish (X8, BR5, BR6, BR7).

**Feature flag.** `rwb.writeoff.sale-selection-v1`, a flag of the platform library; off means the two operations answer 503 with no write and SCR-27 hides the sale actions, and the scan, the pack, the committee and the posting stories are unaffected.

**Done when.** The tests of section 16 pass, the step runs from a synthetic post charge-off account in SIT, R-WO-32 moves the account to `SOLD_POST_CHARGEOFF` with its selection recorded, the shared R-WO-12 branch still escalates above the limit, a case at another state or with another placement type is refused, a repeated key writes once, a forced record failure changes nothing, rwb-debtsale reads the sold population through the published read, and no `recovery_case` row, no other schema's write and no `v_ace_*` read exists in the build.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S7-001 | Carried from the legacy message set of RWB-E6-028: the scan is held for an absent tax criteria version (R-WO-03), so no case reaches the write-off population this step sells. Raised by RWB-S7-E6013-APP, not by this step | The scan is on hold until Finance publishes the tax criteria. |
| MSG-GEN-001 | The write-off reference, the selection or another required element of the request is absent or invalid (X3) | Enter {field}. |
| MSG-P4-002 | A role without the right of the operation calls it (X2) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the row changes (X1) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The four IDs are those of the legacy message set; the text is the legacy and FSD wording, copied unchanged, and no message is reworded and no new one is added. MSG-S7-001 is kept because the legacy table of RWB-E6-028 lists it; it is not raised by this step, whose own validation is the presence of the selection.

### 15. Screens and states

SCR-27 Write-off proposal is served through the gateway-bff composite route (DP-19). The route calls rwb-writeoff for the population, the write-off facts, the sale selection and its record, and rwb-case for the case and its route state; this story fixes the rwb-writeoff answers only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON.

The legacy screen table gives the states "Scan; proposed; in committee; approved", and the post charge-off state this step needs is not among them: the population it sells sits at `PLACEMENT_DECIDED`, downstream of posting and of the provision release, so the screen gains a post-charge-off state and a sold state that no source describes (GAP-3049; ASM-5129). The scan state is RWB-S7-E6013-APP's, the proposed state RWB-S7-E6015-APP's, the committee states RWB-S7-E6017-APP's to RWB-S7-E6020-APP's and the posted state RWB-S7-E6021-APP's. The refusal, missing-field, wrong-state and not-recorded states read the messages of section 14. The empty, loading, error and no access states are not in Screen Specifications v1 for SCR-27 and are Not specified in the source documents (CG-ALL-11244).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E6-028-01 | AC1 | Component | The 25-account post charge-off population on the fakes with `RC-2027-000184`; the record, the row state, the answer and the population read asserted |
| TC-E6-028-02 | AC2 | Component | The shared R-WO-12 branch: an amount above the write-off committee limit, the escalation and the state `ESCALATED_TO_CREDIT_COMMITTEE` (ASM-5128) |
| TC-E6-028-03 | AC3 | Component | `placement_type = sale` at `PLACEMENT_DECIDED`; the state `SOLD_POST_CHARGEOFF`, the row update and the move asserted; another placement type does not fire |
| TC-E6-028-04 | AC4 | Component | The decision-record stub stopped; nothing written, no answer sent and MSG-P7-003 shown |
| TC-E6-028-05 | AC5, Access | Component | A role without the right of the sale selection; 403 with MSG-P4-002 and no read |
| TC-E6-028-06 | Principle 5 | Component | A forced decision-record write failure inside the transaction; the row stays at `PLACEMENT_DECIDED` and no record exists |
| TC-E6-028-07 | Section 12 operations, events and activities | Contract | The published contract of every operation, event and activity of section 12 on the fakes; request, answer and event shape asserted |
| TC-E6-028-08 | AC6, BR6, BR7, section 12.7 tables (ASM-3438) | Component | A statement or test that reads a table outside section 12.7 or another schema; the grant refuses it and the boundary test fails the build |
| TC-E6-028-09 | AC7, BR8, BR9 | Component | The same request and the same Idempotency-Key twice: one record, one answer, and the package version read asserted |
| TC-E6-028-10 | BR10 | Component | Synthetic fixtures only: no name, address, contact value or identity number in the write-off row, the record, a log or a workflow input |
| TC-E6-028-11 | AC10 | Component | Not specified in the source documents (NEWAC-RWB-S7-E6028-APP-AC10) |
| TC-E6-028-12 | AC11 | Component | The rwb-case or rwb-decision fake not answering inside 2 s, and the breaker open; nothing written, no move answered and 503 seen |
| TC-E6-028-13 | AC12 | Component | A case not at `PLACEMENT_DECIDED` and a selection already taken; 409 answered and nothing written |
| TC-E6-028-14 | AC8 | Component | A call with no valid credentials, a caller without the right, and an unknown write-off reference; 401, 403 and 404 answered with no read or write |
| TC-E6-028-15 | AC9 | Component | The same write-off reference and the same Idempotency-Key sent twice; one record, one move and the first answer returned |

The six legacy cases are those of RWB-E6-028 in their legacy order, with the Level column added: every case is tested on the fakes, so every case is `Component`. TC-E6-028-02 runs against the branch RWB-S7-E6018-APP builds, because R-WO-12's from state is `PACK_PREPARED` and the two stories share the same rule and the same service (ASM-5128). The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same ID; no `-ITG` copy is written by this story, and the cross-service journey belongs to the wave 4 harness (RWB-ITG-E6028-ITG). The harness pack is not specified in the source documents: the fixture layout, the synthetic keys, the amounts, the write-off committee limit, the business date, the evidence format and retention, and the gate are agreed at the wave 4 entry check and held as configuration (GAP-0458). The write-off read and the write-off sale operation are not published, so the population is asserted through the case read, the decision record and DP09, and the handover is driven by the lot operation that S6 publishes.

### 17. Guardrails

- No business value in code: R-WO-12 and R-WO-32, their states, `placement_type`, the sale reference, the decision code, the package version and the capability rights stay rule rows and reference data, never a constant, a default or a branch.
- No personal data in `rwb_writeoff`, in a workflow input or in a log: identifiers, amounts, dates, states and a rule version only, and every fixture is synthetic.
- ACE data only through the owner's contract: this service holds no `v_ace_*` grant and reads no ACE table, and a build that adds one fails the boundary test (BR7).
- The case stays with rwb-case: no `recovery_case` row, no case state column and no case write here (BR5).
- The buyer side stays with rwb-debtsale: no lot, reserve, award, cap or buyer record is written or called here, and no event is published for the hand-off (BR5, §12.3).
- One base, one topic, one queue, one schema and one login per service; no document names another service's base or topic as its own (DP-13, DP-14).
- No retired element is reintroduced: no shared job table, no Quartz row, no monolith base, no event published by this step and no write to a retired log table.
- The decision is recorded before the change; a build that updates the row or answers the move outside the record's transaction fails the review (DP-03).
- The approval is never re-decided here: a sale on a write-off with no approval behind it is refused (BR4).

### 18. Traceability

| Requirement ID | Requirement (short) | Story element | Test cases | Feature | L3 process |
|---|---|---|---|---|---|
| REQ-S7-006 | Post charge-off treatment is set by rule, including placement with an agency (FSD S7 Requirements served); the sale is the other placement of the same rule run and the row is taken over the empty plan row (ASM-5133) | The sale selection of R-WO-32: the record, the row state, the case-move answer and the two operations | TC-E6-028-01, TC-E6-028-02, TC-E6-028-03, TC-E6-028-05 | FEAT-WOF-16 | Not specified in the source documents (DOR-RWB-S7-E6028-APP-2) |
| ADR-013 | 19 services inside ACE | rwb-writeoff as the owner of the write-off stage and of its post charge-off population | TC-E6-028-01 | FEAT-WOF-16 | Not specified in the source documents (DOR-RWB-S7-E6028-APP-2) |
| ADR-014 | Schema and login per service | `rwb_writeoff` and its own login | TC-E6-028-01 | FEAT-WOF-16 | Not specified in the source documents (DOR-RWB-S7-E6028-APP-2) |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The three consumed rows with their budget and breaker | TC-E6-028-01 | FEAT-WOF-16 | Not specified in the source documents (DOR-RWB-S7-E6028-APP-2) |
| ADR-022 | Local decision record plus central ledger | The record written before the row changes | TC-E6-028-04, TC-E6-028-06 | FEAT-WOF-16 | Not specified in the source documents (DOR-RWB-S7-E6028-APP-2) |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E6-028, disposition Split (rework); feature FEAT-WOF-16 |
| Legacy criteria | AC1, AC2, AC3 and AC4, owned word for word by this story |
| Wave and release | Wave 4 and release 30 April 2027 (tentative), copied unchanged from the plan; EP06 and the service wave agree at 4, so no W-MAP conflict is raised (ASM-5058) |
| Source text | Legacy RWB-E6-028; FSD S7 Write-off and recovery v3 A1.1 to A1.4, A2.16, Requirements served and Screens; TSD S7 Write-off and recovery v2 T2, T3.1, T3.2, T3.3, T4, T5.3, T6.1, T8 and T-A; Business Rules and Routing Logic v4 rows R-WO-12 and R-WO-32; Recovery Workbench Epics 3 to 8 Specification v3 row FEAT-WOF-16 and integration INT-16 |
| Test cases | TC-E6-028-01 to TC-E6-028-06 |
| Feature and screens | FEAT-WOF-16, SCR-27 Write-off proposal |
| Rules | R-WO-32, with R-WO-12 asserted on the branch of RWB-S7-E6018-APP, governed in rwb-decision |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-020, ADR-022 |

### 19. Out of scope

- The published shape of the two operations, the elements, the placeholders, the consumed rows, the error set and the fakes: RWB-S7-E6028-CON.
- The monthly scan, the tax criteria, the pack, the removal, the routing and the three committee decisions: RWB-S7-E6013-APP to RWB-S7-E6020-APP.
- The approval by limit itself: R-WO-12 and R-WO-15 are RWB-S7-E6018-APP's branch, asserted here only (ASM-5128).
- The post charge-off decision of R-WO-29 and the agency placement of R-WO-30: no S7 story claims R-WO-29, and RWB-S9-E6034-APP carries the agency route (ASM-5129).
- Lots, reserve and tiered terms, bids, the award, the buyer portal, the sale agreement, the data transfer, the cap and the settled sale (R-WO-50, R-WO-51): rwb-debtsale, RWB-S6-E5024-APP to RWB-S6-E6012-APP and rwb-integration for the buyer files.
- The post charge-off payment and its remittance to the buyer (R-WO-40): RWB-S7-E6027-APP.
- The posting, `WriteOffApproved` (`EV-24`), the provision feed and the reconciliation: RWB-S7-E6021-APP to RWB-S7-E6023-APP.
- The case of record, its route states and the parent `CaseWorkflow`: rwb-case (P3); the ACE data products: rwb-source-data (P1); the WO package and its rule rows: rwb-decision (P7).
- The gateway-bff composite route and the screen field list of SCR-27, including the post-charge-off state no source describes: RWB-PLT-N001-CON and the edge stories (ASM-5129).
- The cross-service journey of the legacy key and its evidence: the wave 4 harness, which copies none of these criteria.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
