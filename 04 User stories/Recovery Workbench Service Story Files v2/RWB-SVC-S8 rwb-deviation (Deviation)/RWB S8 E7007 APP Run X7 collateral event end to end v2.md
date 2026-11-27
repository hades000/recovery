# RWB-S8-E7007-APP Run X7 collateral event end to end

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S8-E7007-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-deviation |
| Service epic | RWB-SVC-S8 |
| Wave | 4 |
| Business epic | EP07 |
| Release | 31 May 2027 (tentative) |
| Legacy key | RWB-E7-007 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | L-S8-R |
| Ready to start | Day 1 |
| Size | Sized by the squad at refinement; not specified in the source documents (DOR-RWB-S8-E7007-APP-16) |
| Depends on (build) | RWB-S8-E7007-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Contract version | Not specified in the source documents (DOR-RWB-S8-E7007-APP-23); the only version in the story is the /v1 segment of the base path /api/recovery/deviation/v1 |
| Integration dependencies | rwb-integration, as the carrier of the outside effects of Aric, NCB, EFS, LIT, SVAF and the partner portal; interface identities confirmed with P2 before the wave 4 test (GAP-1821) |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S8 rwb-deviation v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: the X7 collateral-event slice of RWB-E7-007 in rwb-deviation. The three legacy criteria this story owns are kept word for word with their origin tag; the step evaluates R-DEV-06 from `DEV_FLAGGED` on `OWNER_ASSIGNED` for `deviation_code` in (X6, X7) and answers `DEV_WITH_OWNER`, evaluates R-DEV-12 from `DEV_WITH_OWNER` on `ESTATE_CONFIRMED` and answers `DEV_REROUTE`, hands the re-route to the route decision under R-DEV-19, records every outcome through the local decision-record library before any change (DP-03), reads collateral and appraisal data through rwb-source-data's contract (DP-05), serves the outcome branch of the deviation operation on base `/api/recovery/deviation/v1` (DP-13) and reaches SCR-06 and SCR-08 through the gateway-bff composite route (DP-19). No source publishes the consumed operation names, the insurance-claim and re-appraisal answer shapes, or the outbox row this step needs (GAP-3063; ASM-5190 to ASM-5199). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-S8-E7007-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (30 resolved, 17 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **case owner (RW-CASEOWN)**, I want **the X7 collateral event to be handled end to end — the insurance claim approved by a person, the collateral re-appraised and the case returned to the route decision**, so that **every deviation has a handler and a clock** (legacy RWB-E7-007; FSD S8 A2.16.1).

This is the X7 slice of legacy RWB-E7-007 and of FEAT-DVF-07. It owns:

- the three legacy criteria (AC2, AC3 and AC4), copied verbatim with their origin tag, and the rules, messages and screen states they depend on;
- the X7 branch of `DeviationWorkflow` on task queue `rwb-deviation` in namespace `rwb-recovery`, the child of `CaseWorkflow` that can start at any time and pauses the stage clock (context pack workflow row; Temporal and Drools Design slide 13);
- the evaluation of R-DEV-06 and R-DEV-12 against the DEV package at its version in force, with the two moves `DEV_WITH_OWNER` and `DEV_REROUTE` (FSD S8 A2.16.3.1; Business Rules and Routing Logic v4);
- the hand-over of the re-routed case to the route decision at D6 under R-DEV-19, `DEV_REROUTE` on `ROUTE_REOPENED` to `ROUTE_D6`;
- the record of the outcome on the deviation row it owns — `handler_user_id`, `outcome`, `cleared_at` and `contact_stop` — with `outcome` from LOV-DEV-OUTCOME (TSD S8 T3.1, T3.2);
- the local decision record of each outcome, written through RWB-PLT-E1027-CON before any change, with the rule ID, the package version and the case move (DP-03);
- the read of collateral and appraisal data through rwb-source-data's contract, because this service owns no `v_ace_*` view (DP-05);
- the outcome branch of the deviation operation on base `/api/recovery/deviation/v1` (DP-13) and the X7 states of SCR-06 and SCR-08 behind the gateway-bff composite route (DP-19).

It does not own: the published shape of the operation, the deviation elements, the consumed rows, the error set and the fakes, which are RWB-S8-E7007-CON; the raise of the deviation and the clock pause (the deviation-raise and timer slices of this service, and rwb-case's timer row); the X1 to X6 handler stories RWB-S8-E7001-APP to RWB-S8-E7006-APP; the insurance claim itself, which is rwb-guarantee's FEAT-GUA-08; the appraisal order and the accepted value, which are rwb-valuation's FEAT-VAL-01 and FEAT-VAL-02; the case of record, its route states and its timers, which are rwb-case's (P3); the DEV package and its 22 rules, which are rwb-decision's (P7); and the deployment of this build, which is the operations story of this legacy key.

### 2. Business rationale

The objective, the problem and the metric are unchanged from the legacy story and the module FSD: "Files the insurance claim, re-appraises the collateral and returns the case to the route decision" (FSD S8 A2.16.1), because "complaints, hardship, death, fraud, bankruptcy, lost contact and collateral events are handled case by case with no clock" (FSD S8 A1.3), and the measure is "Deviations closed within the service level | Set with DL22 | Decision log and Workbench records | Monthly" (FSD S8 A2.16.1). What D-RCV-60 changes is who owns the case, the clock, the claim and the package.

- **The deviation is this service's row.** `deviation` is S8's only table in `rwb_deviation` (context pack, ownership rows owned by S8; TSD S8 T3.1), and the DEV route set of 22 rules over 9 states is the deviation stage's (TSD S8 T4); R-DEV-06 and R-DEV-12 are transitions of that stage and run here.
- **The case and the clock are not this service's.** `recovery_case`, every route state — `DEV_FLAGGED`, `DEV_WITH_OWNER`, `DEV_REROUTE`, `ROUTE_D6` — and the `timer` row are rwb-case's; this step evaluates the rules, records the decision and **answers** the move (ASM-5191, ASM-5192).
- **The claim and the appraisal are other services'.** FEAT-GUA-08 files and approves the insurance claim on a collateral event in rwb-guarantee (S3), and FEAT-VAL-01 and FEAT-VAL-02 order and receive the appraisal in rwb-valuation (S1); this story is the deviation decision those facts feed and the return point they move (legacy "Depends on FEAT-GUA-08"; ASM-5194).
- **ACE data arrives through its owner.** The legacy Data table names `v_ace_collateral` and `v_ace_valuation`; S8 owns no such view, so the collateral record and the appraised value arrive on rwb-source-data's contract (DP-05; ASM-5195).
- **The package is read, not embedded.** The DEV route set is governed in rwb-decision, and DP-04 is not in this key's pattern set, so the package arrives on its read with the version in force and the version is recorded with the outcome (ASM-5193).
- **The decision is recorded first**, before the deviation row changes and before the move is answered, which is what legacy AC4 tests.
- **A person still approves the claim.** R-DEV-06 lets the agent handle within policy and requires a person to approve an insurance claim, so the step never approves a claim by rule; that is what legacy AC2's state move is built on.
- **REQ-S8-005 is served.** "A collateral event triggers an insurance claim and a re-appraisal before the next decision" (FSD S8 Requirements served) is this story's requirement, and the next decision is the route decision R-DEV-12 and R-DEV-19 hand the case to.

No business value moves: the two states, the codes, the outcome list, the rule IDs and the package version are rule rows and reference data read with their version, never constants of the code.

### 3. Preconditions

- RWB-S8-E7007-CON is published: the outcome branch of the deviation operation, the deviation elements, the consumed rows, the `Idempotency-Key` rule, the error set and the fakes are baselined and handed to this story.
- The rwb-case case read is published with its fake: the case reference, the case number, the product group, the stage and the deviation state `DEV_FLAGGED`. The operation name is Not specified in the source documents (GAP-3063; ASM-5191).
- The case-move answer of rwb-case is available for the fake: the moves `DEV_WITH_OWNER`, `DEV_REROUTE` and `ROUTE_D6`, each with the rule ID and its version. No source names a published operation that moves a case state on behalf of a stage; on the workflow boundary the answer is the stage outcome the parent `CaseWorkflow` applies (GAP-3063; ASM-5191).
- The rwb-decision rule-package read is published with its fake and answers the DEV package at its version in force, with R-DEV-06, R-DEV-12 and R-DEV-19 among its 22 rules over 9 states (GAP-3063; ASM-5193).
- The rwb-guarantee claim answer is published with its fake: the insurance claim of the collateral event, its status and the person who approved it. The operation name is Not specified in the source documents (GAP-3063; ASM-5194).
- The rwb-valuation re-appraisal answer is published with its fake: the re-appraisal order of the collateral and the accepted value. The operation name is Not specified in the source documents (GAP-3063; ASM-5194).
- The rwb-source-data read is published with its fake and answers the collateral record and the appraised value of the collateral key, read only (DP-05; GAP-3063; ASM-5195).
- RWB-PLT-E1027-CON is published with its writer fake: the local decision-record library writes in the caller's transaction, and a failed write stops the action with MSG-P7-003, so no move is answered and no row changes (DP-03).
- RWB-PLT-N001-CON is published: SCR-06 and SCR-08 reach this service through the gateway-bff composite route, one hop, and no screen calls a service directly (DP-19).
- `deviation` exists in schema `rwb_deviation` from the DB story of this service, with the columns of DF-CAS-036 to DF-CAS-045 and the standard record columns of TSD S8 T3.0; this story adds no table, no column and no migration.
- The Temporal namespace `rwb-recovery` and the queue `rwb-deviation` exist; the X7 step runs inside the running deviation stage workflow and needs no Schedule, because the service owns no job (context pack jobs row; ASM-5192).
- The service runs as its own login on schema `rwb_deviation`; it holds no grant on another `rwb_*` schema and no `v_ace_*` grant, so a statement on `rwb_case` or on an ACE view is refused by the database and fails the boundary test.
- No approval is needed to build against a Draft contract baseline; the contract is tagged by RWB-S8-E7007-CON when its tests pass (ASM-5197).

### 4. Flow

1. The X7 deviation of the case is open: rwb-case holds the case at `DEV_FLAGGED` with the stage clock paused and the prescription clock running (R-DEV-01, raised by the deviation-raise slice); this story reads that state only.
2. The case owner opens SCR-08 Deviation queue, or SCR-06 Raise deviation for the same case, through the gateway-bff composite route and reads the deviation, its code, the handler and the paused state, one hop (DP-19).
3. The owner works the collateral event: the claim is with rwb-guarantee and the re-appraisal with rwb-valuation, and the owner reads both answers on the screen. The claim approval is never taken by rule (FSD S8 A2.16.2; R-DEV-06).
4. rwb-valuation has ordered and received the appraisal; the collateral record and the appraised value are read on the rwb-source-data contract, one hop, read only (DP-05; FEAT-VAL-01, FEAT-VAL-02).
5. The owner assigns the handler and confirms the claim. The screen sends the deviation reference, the assignment, the claim reference and the owner's identity with an `Idempotency-Key` (FSD S8 A2.16.2 step 2).
6. The X7 step of `DeviationWorkflow` on queue `rwb-deviation` receives the request as a signal to the running stage, with the package version read from rwb-decision in force (ASM-5193).
7. The step reads the deviation row it owns and the case state on the rwb-case contract: a case not at `DEV_FLAGGED` is refused with 409 and nothing is written (ASM-5191).
8. `CollateralDeviationEvaluator` applies R-DEV-06: from `DEV_FLAGGED`, on `OWNER_ASSIGNED`, where `deviation_code` is in (X6, X7), the action is "Agent handles within policy; a person approves an insurance claim" and the state is `DEV_WITH_OWNER`. The evaluation answers the rule ID, the package version, the handler and the move.
9. `DeviationRecordWriter` writes one decision record through the local decision-record library, **before any change**: the case reference, the deviation, the code X7, the rule ID `R-DEV-06` with its package version, the handler, the outcome, the from state and the to state. A failed write stops the step with nothing changed (DP-03; legacy AC4).
10. `deviation` is updated in one transaction with `handler_user_id`, `outcome` (`RETURNED` or `RE_ROUTED`) and the standard columns, and `CaseMoveAnswer` answers rwb-case with `DEV_WITH_OWNER`; rwb-case writes the `recovery_case` row and the `assignment` row it owns (ASM-5191, ASM-5192).
11. When the estate position is confirmed and the insurance does not clear, R-DEV-12 fires: from `DEV_WITH_OWNER`, on `ESTATE_CONFIRMED`, action "Return to the route decision against the estate", state `DEV_REROUTE`. A second record is written under R-DEV-12 with its own version, and `DEV_REROUTE` is answered to rwb-case (FSD S8 A2.16.3.1).
12. The re-routed case leaves the deviation stage for the route decision: R-DEV-19 recomputes the segment and re-runs the hard gates on `ROUTE_REOPENED`, the step answers `ROUTE_D6`, and rwb-valuation's route decision takes the case from there (R-DEV-19; ASM-5199).
13. `DeviationCleared` (`EV-07`, `caseId`, `deviationCode`, `outcome`) is relayed on `rwb.deviation.events.v1` through the outbox in the same transaction, so timers and communications see the outcome; the raise event EV-06 belongs to the raise step (ASM-5196).
14. A repeated request with the same `Idempotency-Key` answers the outcome it created and writes no second record, no second row and no second event; a decision on a case that has left `DEV_FLAGGED` answers 409 with no change.
15. The owner sees the deviation in its handled or re-routed state with the outcome, the handler, the claim approval and the return point, read back from this service and from the case state of rwb-case, read only (DP-19).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The local decision record cannot be written | Nothing changes: no row is updated, no move is answered and no event is written | MSG-P7-003 | AC4, TC-E7-007-04, TC-E7-007-06 |
| X2 | The role does not hold the Case record right U | 403 before any read or write; nothing changes and no record is written | MSG-P4-002 | AC5, TC-E7-007-05 |
| X3 | A required element of the request is absent or invalid | 422 and nothing is recorded; the deviation stays in its state | MSG-GEN-001 | AC2 |
| X4 | The case is not at `DEV_FLAGGED`, or the outcome has already been taken | 409 and nothing is written for that case; a decision is not taken twice | None | AC2, AC3 |
| X5 | The rwb-case, rwb-decision, rwb-guarantee, rwb-valuation or rwb-source-data contract does not answer inside 2 s, or its breaker is open | The step retries on the workflow's own schedule; nothing is written, no move is answered and no event is relayed; the caller sees 503 with the platform error envelope | None | AC2, AC3 |
| X6 | The insurance claim is not yet approved by a person | R-DEV-06 does not fire; the deviation stays at `DEV_FLAGGED` and the screen shows the claim state; no state is advanced by rule | None | AC2 |
| X7 | The same request arrives twice, or the outcome is confirmed twice | One record, one row update, one event and one answer; the repeat answers the outcome that exists and is counted | None | AC2 |
| X8 | The appraisal answer arrives after the case has left the deviation stage | No record is written, no row changes and the late answer is not applied to a closed deviation | None | AC3 |
| X9 | A component, a statement or a test reaches a `v_ace_*` view, a `recovery_case` row, a `timer` row or another service's schema | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | AC6, BR5, BR6 |

X1 to X4 are the legacy exception paths carried onto the slice, X2 and X4 to X9 are the paths the target call types, the claim gate and the boundary add, and X3 is the required-field rule of the module FSD (VR-S8-016-1). No source publishes a message for an appraisal that arrives after the stage has closed; the step discards it silently and the case is recorded as a gap rather than invented (GAP-3063; ASM-5194).

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-S8-E7007-CON, the rwb-case, rwb-decision, rwb-guarantee, rwb-valuation and rwb-source-data fakes and the decision-record stub, on its own schema, and needs no live P1, P3, P7, S1 or S3 |
| Negotiable | The activity and component names, the decision code of the record and the shape of the stage outcome are this story's choice; the rules, messages, screen states, operation and two moves are fixed |
| Valuable | An X7 collateral event leaves the deviation stage with a person-approved claim, a recorded outcome and a case returned to the route decision, so no case sits paused without a handler |
| Estimable | One workflow branch, one evaluator, one record write, one row update, three case-move answers, one event and five clients |
| Small | Finished inside two weeks with its tests on the fakes |
| Testable | Each criterion runs on a synthetic flagged case through the contract fakes, plus the access, invalid-request, moved-case, unapproved-claim and failed-record cases |

### 7. Acceptance criteria

```gherkin
Feature: Run X7 collateral event end to end

  Background:
    Given case "RW-2026-000702" carries the open deviation X7 at "DEV_FLAGGED" with the stage clock paused and the prescription clock running
    Given the DEV rule package is in force at its version and carries R-DEV-06, R-DEV-12 and R-DEV-19
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC2 Rule R-DEV-06 (legacy RWB-E7-007 AC2)
    Given the rwb-case contract mock returns the case state "DEV_FLAGGED" for "RW-2026-000702" and accepts the move "DEV_WITH_OWNER"
    Given the rwb-decision contract mock returns the DEV package at its version in force with R-DEV-06
    Given the rwb-guarantee contract mock returns the insurance claim of the collateral event approved by a person
    Given a case in state DEV_FLAGGED
    When owner assigned
    Then agent handles within policy; a person approves an insurance claim
    Then the case moves to DEV_WITH_OWNER

  Scenario: AC3 Rule R-DEV-12 (legacy RWB-E7-007 AC3)
    Given the rwb-case contract mock returns the case state "DEV_WITH_OWNER" for "RW-2026-000702" and accepts the move "DEV_REROUTE"
    Given the rwb-decision contract mock returns the DEV package at its version in force with R-DEV-12 and R-DEV-19
    Given the rwb-valuation contract mock returns the accepted re-appraised value of the collateral
    Given a case in state DEV_WITH_OWNER
    When estate confirmed
    Then return to the route decision against the estate
    Then the case moves to DEV_REROUTE

  Scenario: AC4 Not recorded (legacy RWB-E7-007 AC4)
    Given the decision record cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003

  Scenario: AC5 Access (exception X2; added by this story) (new, D-RCV-60)
    Given the role does not hold the Case record right U
    When the outcome is requested for the case
    Then the request is refused with 403 and MSG-P4-002, and nothing is read or written

  Scenario: AC6 Boundary (exception X9; added by this story) (new, D-RCV-60)
    Given a component, a statement or a test reaches a v_ace_* view, a recovery_case row, a timer row or another service's schema
    When the build runs the boundary test
    Then the grant refuses the statement, the boundary test fails the build and nothing is released

  Scenario: AC7 Timeout (exception X5; added by this story) (new, D-RCV-60)
    Given the rwb-case contract mock does not answer inside 2 s for "RW-2026-000702"
    When the outcome is requested for the case
    Then the step retries on the workflow's own schedule, nothing is written, no move is answered and no event is relayed, and the caller sees 503 with the platform error envelope

  Scenario: AC8 Failed call or open breaker (exception X5; added by this story) (new, D-RCV-60)
    Given the breaker of the rwb-decision contract is open
    When the outcome is requested for the case
    Then nothing is written, no move is answered and no event is relayed, and the caller sees 503 with the platform error envelope

  Scenario: AC9 Disallowed transition (exception X4; added by this story) (new, D-RCV-60)
    Given the case is not at "DEV_FLAGGED" or its outcome has already been taken
    When the outcome is requested for the case
    Then the request is refused with 409, nothing is written for that case and a decision is not taken twice

  Scenario: AC10 Error answers (exceptions X2, X3, X4, X5; added by this story) (new, D-RCV-60)
    Given a request reaches the outcome operation of the deviation service
    When the request is refused or a consumed contract is unavailable
    Then the answer is 403 for a role without the Case record right U, 422 for an absent or invalid required element, 409 for a case not at DEV_FLAGGED, or 503 with the platform error envelope; the 401 and 404 answers are Not specified in the source documents (NEWAC-RWB-S8-E7007-APP-AC8)

  Scenario: AC11 Replay (exception X7; added by this story) (new, D-RCV-60)
    Given the same request arrives twice, or the outcome is confirmed twice
    When the repeat is received
    Then one decision record, one row update, one event and one answer exist, and the repeat answers the outcome that exists and is counted
```

The three criteria are the legacy criteria of RWB-E7-007 word for word, with their origin tag added and nothing else changed: the repeated `Then`, the wording of `owner assigned`, `estate confirmed` and `the action is taken`, and `the decision record cannot be written` all stand. The cross-service parts are mocked, so AC2 carries three `Given the <service> contract mock returns <x>` lines and AC3 three, and those are the only additions. Legacy AC1 — the end-to-end journey — is owned by RWB-ITG-E7007-ITG by the split plan, so it is not repeated here (ASM-5190). What the legacy lines describe now happens in four places: rwb-case holds the case and its states and writes the moves, rwb-decision holds the package with R-DEV-06 to R-DEV-19 at its version, rwb-guarantee approves the claim and rwb-valuation re-appraises the collateral, and this story applies the rules, writes the record, updates the deviation row, relays the event and answers the moves. The `decision log` of the legacy text is the local decision record of DP-03 in `rwb_deviation`, with the central `decision_log_entry` ledger of rwb-decision behind it. AC3 names R-DEV-12 as the legacy story wrote it; the rule's own condition is `deviation_code = X3 and insurance does not clear`, and the return-to-route-decision path is also carried by R-DEV-19 on `ROUTE_REOPENED`, so the step applies both and records the legacy condition as it stands (GAP-3063; ASM-5199).

### 8. Business rules

| Rule | Route set | Decision | From state | Event | Condition | Action | To state | Owner | Systems | Timer |
|---|---|---|---|---|---|---|---|---|---|---|
| R-DEV-06 | Deviations | X1 to X7 | DEV_FLAGGED | OWNER_ASSIGNED | deviation_code in (X6,X7) | Agent handles within policy; a person approves an insurance claim | DEV_WITH_OWNER | Agent, case owner | Workbench | None |
| R-DEV-12 | Deviations | X1 to X7 | DEV_WITH_OWNER | ESTATE_CONFIRMED | deviation_code = X3 and insurance does not clear | Return to the route decision against the estate | DEV_REROUTE | Case owner | Workbench | None |
| R-DEV-19 | Deviations | X1 to X7 | DEV_REROUTE | ROUTE_REOPENED | Any | Recompute the segment and re-run the hard gates | ROUTE_D6 | Case owner | Workbench | None |

The three rows are the rows of the Business Rules and Routing Logic v4, copied character for character. Their owner and systems columns name business roles and systems, not services: in the target "Workbench" is SCR-06 and SCR-08 for this service and the case of rwb-case read through the composite route, "Agent" is the rwb-agent output the handler acts on, and "case owner" is the role set of the permission table below (ASM-5191). R-DEV-09 and R-DEV-18, the resume path of an X7 outcome that changes nothing, and R-DEV-01, the raise, are named and not owned here.

| ID | Rule | Source |
|---|---|---|
| BR1 | The X7 handling is a transition of the deviation stage: it runs in `DeviationWorkflow` on `rwb-deviation`, and only `deviation` of `rwb_deviation` records its outcome | TSD S8 T3.1, T4; context pack ownership rows (table and workflow); FSD S8 A2.16.2 |
| BR2 | The decision is recorded before the row changes and before the move is answered, with the rule ID, the package version, the outcome and the two states; a failed write changes nothing and the caller sees MSG-P7-003 | DP-03; TSD S8 T2 ("writes the decision log entry before any change"); legacy AC4 |
| BR3 | R-DEV-06 never approves a claim: the agent handles within policy and a person approves the insurance claim, and the approval arrives on the rwb-guarantee contract | Business Rules and Routing Logic v4 row R-DEV-06; legacy AC2; ASM-5194 |
| BR4 | The moves are answered, not written: `recovery_case`, every route state, the `assignment` row and the `timer` row are rwb-case's | ASM-5191, ASM-5192; TSD S8 T4 |
| BR5 | No cross-schema join and no foreign key leaves `rwb_deviation`; `case_id` and `handler_user_id` are identifiers of another service's fact | DP-01; TSD S8 T3.3 |
| BR6 | ACE data only through the owner's contract: the collateral record and the appraised value arrive on rwb-source-data's contract, and this service holds no `v_ace_*` grant | DP-05; FSD S8 A1.1; TSD S8 T1; ASM-5195 |
| BR7 | The package is read at its version in force and the version is recorded with the outcome; no rule threshold is a constant | ASM-5193; FSD S8 BR-S8-016 |
| BR8 | `outcome` takes its value from LOV-DEV-OUTCOME — RETURNED, RE_ROUTED, CASE_ENDED — and no literal is written in code | TSD S8 T3.2; ASM-5199 |
| BR9 | No person name, address, contact value or identity number enters `rwb_deviation`, the decision record, an event, a log or a workflow input | Template and Rules §R7.2 (s17); TSD S8 T6.2 |
| BR10 | R-DEV-06: the claim gate and the move to `DEV_WITH_OWNER`, as the §8 rule row | Business Rules and Routing Logic v4 row R-DEV-06; legacy AC2 |
| BR11 | R-DEV-12: the return to the route decision and the move to `DEV_REROUTE`, as the §8 rule row | Business Rules and Routing Logic v4 row R-DEV-12; legacy AC3 |
| BR12 | R-DEV-19: the hand-over of the re-route to the route decision and the move to `ROUTE_D6`, as the §8 rule row | Business Rules and Routing Logic v4 row R-DEV-19; legacy AC3 |

**Coverage of BR1 to BR12.** BR1 by AC2 and AC3; BR2 by AC4, TC-E7-007-04 and TC-E7-007-06; BR3 by AC2 and TC-E7-007-02; BR4 by AC2, AC3, TC-E7-007-02 and TC-E7-007-03; BR5 and BR6 by AC6 and TC-E7-007-08; BR7 by AC2, AC3, TC-E7-007-02 and TC-E7-007-03; BR8 by AC3 and TC-E7-007-03; BR9 by AC6 and TC-E7-007-08; BR10 by AC2 and TC-E7-007-02; BR11 and BR12 by AC3 and TC-E7-007-03.

### 9. State transitions

The case route state is rwb-case's and is not changed by this story: the step answers the move and the parent `CaseWorkflow` applies it (BR4). The deviation record's own lifecycle column `state` moves here.

| From (case state, rwb-case) | Event | Condition | To | Written by |
|---|---|---|---|---|
| `DEV_FLAGGED` | `OWNER_ASSIGNED` | `deviation_code` in (X6, X7) and the claim approved by a person | `DEV_WITH_OWNER` | rwb-case, on this story's answer (R-DEV-06) |
| `DEV_FLAGGED` | `OWNER_ASSIGNED` | The claim is not approved by a person | Unchanged | none; R-DEV-06 does not fire (X6) |
| `DEV_FLAGGED` | Any decision | The case is not at `DEV_FLAGGED` | Unchanged | none; 409 (X4) |
| `DEV_WITH_OWNER` | `ESTATE_CONFIRMED` | The estate position is confirmed and the insurance does not clear | `DEV_REROUTE` | rwb-case, on this story's answer (R-DEV-12) |
| `DEV_WITH_OWNER` | `DEVIATION_RESOLVED` | `deviation_code` in (X1, X7) and the outcome changes nothing | `DEV_RESOLVED` | rwb-case, under R-DEV-09, outside this story's criteria |
| `DEV_REROUTE` | `ROUTE_REOPENED` | Any | `ROUTE_D6` | rwb-case, on this story's answer (R-DEV-19) |

| Step execution | Event | Condition | To |
|---|---|---|---|
| Waiting | The owner's assignment and claim confirmation for a flagged X7 case | The package in force is read | Evaluating |
| Evaluating | R-DEV-06 fires | The claim is approved by a person and the case is at `DEV_FLAGGED` | Recording |
| Evaluating | R-DEV-06 does not fire | The claim is unapproved, or the state is not the rule's | Waiting, nothing changed |
| Recording | The record is written, the row updated, the event relayed and the answer sent | The transaction commits | Handled, waiting for the estate position |
| Handled | R-DEV-12 fires | The estate is confirmed and the insurance does not clear | Re-routed, `DEV_REROUTE` answered and a second record written |
| Re-routed | R-DEV-19 fires | Any | Waiting, `ROUTE_D6` answered; the case leaves for rwb-valuation |
| Recording or Re-routed | The record write fails | X1 | Waiting, nothing changed |

The states `DEV_FLAGGED`, `DEV_WITH_OWNER`, `DEV_REROUTE` and `ROUTE_D6` are those of the DEV machine of TSD S8 T4 and live on the case of record; this step writes none of them. `ROUTE_D6` is where the route decision of rwb-valuation picks the case up again.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-CASEOWN, case owner | Case record CRU in TSD S8 T6.1: the primary role of FSD S8 A2.16.3.3, deciding X7, confirming the claim and reading the outcome back |
| RW-SPECIAL, hardship and vulnerability specialist | Case record RU: the second role the legacy permission table gives right U on the case record, handling the collateral event with the owner |
| RW-GUARANT, guarantee officer | Case record RU: reads the claim state the rwb-guarantee record carries and never approves by rule |
| RW-RESTRUCT, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-ENFORCE, RW-SALEOFF, RW-DEBTSALE | Case record RU or R as the matrix gives it: the other roles of the legacy permission table's right U |
| RW-LEGAL, RW-NPAMGR, RW-WRITEOFF, RW-CREDITAD, RW-CONDUCT, RW-RISK, RW-AUDIT, RW-BIANAL, RW-TRIBE | Case record R: read only, in scope |
| SY-CASEWF, SY-RULES, SY-AGENT, SY-DATALOAD | Case record R or U as the matrix gives it: the service identities run the step and are subject to the same checks |
| rwb-deviation service identity | Evaluates R-DEV-06, R-DEV-12 and R-DEV-19, writes the record and the row, relays the event, answers the moves and serves the operation; it holds no grant on another schema and no `v_ace_*` grant |

The rights are the rows of TSD S8 T6.1 and nothing wider, and the right the outcome needs is U — the right the legacy permission table gives on the case record and the right TSD S8 T-A.2 declares on API-S8-002. DP-08 is not in this story's pattern set: the capability area and the right are declared per operation and the guard is a service-template capability, so the check is stated here and not built here. The rwb-access authorise check that guards the operation is Not specified in the source documents (DOR-RWB-S8-E7007-APP-6).

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-CAS-036 | deviation (S8, `rwb_deviation`) | id | Read, the deviation reference the operation takes as `deviationId` |
| DF-CAS-037 | deviation (S8, `rwb_deviation`) | case_id | Read, the case of the deviation |
| DF-CAS-038 | deviation (S8, `rwb_deviation`) | deviation_code | Read, the code X7 the slice handles |
| DF-CAS-039 | deviation (S8, `rwb_deviation`) | raised_at | Read |
| DF-CAS-040 | deviation (S8, `rwb_deviation`) | raised_by | Read, from LOV-RAISED-BY |
| DF-CAS-041 | deviation (S8, `rwb_deviation`) | paused_state | Read, the return point R-DEV-12 and R-DEV-19 leave |
| DF-CAS-042 | deviation (S8, `rwb_deviation`) | handler_user_id | Write, the owner assigned under R-DEV-06 |
| DF-CAS-043 | deviation (S8, `rwb_deviation`) | contact_stop | Write on clear only, where the stop is lifted by the outcome |
| DF-CAS-044 | deviation (S8, `rwb_deviation`) | cleared_at | Write when the outcome leaves the stage |
| DF-CAS-045 | deviation (S8, `rwb_deviation`) | outcome | Write, from LOV-DEV-OUTCOME |
| Standard columns | deviation (S8, `rwb_deviation`) | `is_active`, `state`, `version`, `created_at`, `created_by`, `updated_at`, `updated_by` | Write `state`, `version`, `updated_at` and `updated_by`; the others read |
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library, created in `rwb_deviation`) | rule id, rule version, decision code, inputs reference, from and to state, decided at | Write through the local library, before the row changes |
| DF-WRK-009 to DF-WRK-016 | assignment (P3) | id, case_id, task_id, assignee_user_id, assigned_at, ended_at and 2 more | Not read as a table and not written: the assignment row is created by rwb-case on this story's answer (ASM-5192) |
| DF-WRK-027 to DF-WRK-036 | timer (P3) | id, case_id, task_id, timer_type, started_at, expires_at and 4 more | Not read as a table and not written: the stage clock is paused and resumed by rwb-case (ASM-5192) |
| DF-CAS-001 to DF-CAS-023 | recovery_case (P3) | id, case_no, product_group, primary_person_key, status, stage_code and 17 more | Not read as a table: the state arrives on the rwb-case contract |
| DF-REF-001 to DF-REF-015 | rule_row (P7) | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | Not read as a table: the rules arrive on the package read |
| DF-ACE-091 to DF-ACE-098 | v_ace_collateral (P1) | collateral_no, asset_key, account_key, collateral_value, collateral_type, register_date and 2 more | Not read as a view: the collateral record arrives on the rwb-source-data contract (DP-05) |
| DF-ACE-187 to DF-ACE-195 | v_ace_valuation (P1) | valuation_key, asset_key, appraisal_no, appraisal_type, appraised_value, appraisal_date and 3 more | Not read as a view: the appraised value arrives on the rwb-source-data contract and the accepted value on the rwb-valuation answer (DP-05) |
| The claim and its approver | rwb-guarantee (S3) | The insurance claim of the collateral event, its status and the approving person's identity | Read on the rwb-guarantee contract; the property names are Not specified in the source documents (GAP-3063; ASM-5194) |

Field IDs are those of TSD S8 T3.1 and the Logical Data Model and Data Dictionary, and the case, assignment, timer, ledger, rule and ACE rows are the rows the legacy Data table lists, with their owners changed to P3 and P1 by the target. **No new table, no new column and no migration**: the table arrives with the DB story of this service, and `decision_record`, `idempotency_key` and `outbox_event` are library objects created in `rwb_deviation` by their own migrations (DP-03).

**No personal data.** The rows carry identifiers, codes, dates, an outcome, a state and a rule version. No name, address, contact value or identity number enters `rwb_deviation`, the record, the event, a log or a workflow input, and the fixtures are synthetic. `primary_person_key` is P3's and is never copied here; the approving person is carried as an identity reference and never as a name.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-deviation (S8); base `/api/recovery/deviation/v1` (DP-13). This story supplies the outcome branch of the deviation operation, whose shape RWB-S8-E7007-CON declares.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| PATCH | `/deviations/{deviationId}` (API-S8-002) | `DeviationOutcome` in with the assignment, the claim reference and the outcome, `Deviation` out with the rule `R-DEV-06` or `R-DEV-12` and its version, the handler, the outcome and the state | Case record, right U, scope applied | `Idempotency-Key` header; TSD S8 T-A.2 publishes it as "Not applicable" and the story keeps the rule for the repeat (ASM-5198) |

The errors are 400, 401, 403 with MSG-P4-002, 404 for a deviation that is not this service's, 409 for a case that has left `DEV_FLAGGED`, 422 with MSG-GEN-001 for an absent or invalid element and 503 when the library or a consumed contract does not answer (TSD S8 T-A.2). The raise operation `POST /cases/{caseId}/deviations` (API-S8-001) belongs to the deviation-raise slice and is not declared here (ASM-5198).

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| The case read (operation name Not specified in the source documents (GAP-3063; ASM-5191)) | `/api/recovery/case/v1` | P3 rwb-case | The case reference, case number, product group, stage and state of the case at `DEV_FLAGGED` and `DEV_WITH_OWNER`; read only, faked |
| The case-move answer (operation name Not specified in the source documents (GAP-3063; ASM-5191)) | rwb-case (P3) | P3 rwb-case | The moves `DEV_WITH_OWNER`, `DEV_REROUTE` and `ROUTE_D6` with the rule version; on the workflow boundary it is the stage outcome the parent `CaseWorkflow` applies; faked |
| The DEV rule-package read in force (operation name Not specified in the source documents (GAP-3063; ASM-5193)) | `/api/recovery/decision/v1` | P7 rwb-decision | The DEV package at its version, with R-DEV-06, R-DEV-12 and R-DEV-19 among its 22 rules over 9 states; faked |
| The insurance-claim read (operation name Not specified in the source documents (GAP-3063; ASM-5194)) | `/api/recovery/guarantee/v1` | S3 rwb-guarantee | The claim of the collateral event on FEAT-GUA-08, its status and the approving person's identity; faked |
| The re-appraisal read (operation name Not specified in the source documents (GAP-3063; ASM-5194)) | `/api/recovery/valuation/v1` | S1 rwb-valuation | The re-appraisal order of the collateral and the accepted value of FEAT-VAL-01 and FEAT-VAL-02; faked |
| The collateral and appraisal read (operation name Not specified in the source documents (GAP-3063; ASM-5195)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | The collateral record of DF-ACE-091 to DF-ACE-098 and the appraised value of DF-ACE-187 to DF-ACE-195, read only; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The six rows are contract dependencies of class C that the plan does not carry, because this story's C row is None; the absence is recorded (GAP-3063; ASM-5191, ASM-5193, ASM-5194, ASM-5195).

#### 12.3 Events published

| Event | Name | Payload | Producer group | Consumer |
|---|---|---|---|---|
| EV-07 | `rwb.deviation.DeviationCleared.v1` on `rwb.deviation.events.v1` | `caseId`, `deviationCode`, `outcome` | rwb-deviation X7 outcome | Timers and communications, per the event set of the Event and Messaging Design v5 |

One row, relayed through the outbox in the transaction that writes the deviation row, with a CloudEvents envelope and the retry and `.dlt` topics of the platform (DP-14). EV-06 `DeviationRaised` belongs to the raise step. The outbox and inbox library is the DP-09 dependency the plan does not carry for this key, and the absence is recorded (GAP-3063; ASM-5196).

#### 12.4 Events consumed

None. The trigger of the step is the owner's decision on SCR-06 or SCR-08 through the composite route, because the FSD declares no background event for the feature (FSD S8 A2.16.4.4: "No background event"). The claim state and the accepted appraisal are read on their owners' contracts and not from their topics; the service listens to the rwb-source-data and rwb-case events in its screening and timer slices, and none belongs to this step. This story therefore holds no consumer group, no subscription and no inbox row, and a build that adds one fails the absence test.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `DeviationWorkflow` | Workflow, starts at any time for a case, the child of `CaseWorkflow`, continues-as-new at each stage end | `rwb-deviation` in namespace `rwb-recovery` (CG-ALL-11600) | Input: the case reference and the package in force; signals: the owner's outcome and the case answered by rwb-case; outcome for the parent: the case move |
| `recordCollateralOutcome` | Activity, the X7 step, with R-DEV-06, the R-DEV-12 re-route and the R-DEV-19 hand-over | `rwb-deviation` | The deviation reference, the assignment, the claim reference and the packaging version in; the rule ID with its version, the record written, the row updated and the case move out |

No child workflow for the case, the claim or the appraisal exists in this service, and no timer is armed by this story: R-DEV-06 and R-DEV-12 carry no timer and the stage clock is rwb-case's (ASM-5192). The activity name is a target design choice fixed by no source document.

Workflow ID form: Not specified in the source documents (CG-ALL-11601). Start: an agent or officer flags the deviation (EV-06 starts screening), or universal rules R-UNI-04 to 09 fire. Duplicate-start policy: Not specified in the source documents (CG-ALL-11601).

The approval the FSD names (AC-ALT-S8-002-01) is a step inside `DeviationWorkflow`, taken by the approver role the code assigns (role not specified in the source documents, GAP-1820); the local decision-record library writes the entry and its hash. No P7 `ApprovalWorkflow` edge is set for this service; that question stays open (GAP-1820).

#### 12.6 Schedules

None. The service owns no job (context pack jobs row: 0), the step is member-driven, and the only clock involved — the stage clock that pauses — is the `timer` row of rwb-case resumed under R-DEV-18. No Temporal Schedule, no Quartz row, no shared job table and no batch table is declared, built or re-registered here.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| deviation | S8 (`rwb_deviation`) | The deviation X1 to X7 raised on a case; this story reads the row and writes its state, handler, outcome and cleared-at columns |
| decision_record | PLT library, created in `rwb_deviation` | The local hash-linked decision record of each X7 outcome (DP-03) |
| idempotency_key | PLT library, created in `rwb_deviation` | The key of the repeated request and the answer it holds |
| outbox_event | PLT library, created in `rwb_deviation` | The row that relays EV-07 in the same transaction (§12.3) |

Not owned and never read as a table: `recovery_case`, `assignment` and `timer` (P3), every `v_ace_*` view (P1), `decision_log_entry` and `rule_row` (P7), `document` (P5), `notice` (P6), `payment` (P8), the claim of rwb-guarantee (S3) and the appraisal of rwb-valuation (S1). No foreign key leaves the schema and `case_id` is an identifier, not a foreign key across schemas (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case case fake | The case of record at `DEV_FLAGGED` and at `DEV_WITH_OWNER` for `RW-2026-000702`; a case that has moved; a case that is not in scope | AC2, AC3, X4 |
| rwb-case case-move fake | The moves `DEV_WITH_OWNER`, `DEV_REROUTE` and `ROUTE_D6` accepted, and a move refused | AC2, AC3 |
| rwb-decision rule-package fake | The DEV package at its version in force with R-DEV-06, R-DEV-12 and R-DEV-19 among its 22 rules over 9 states | AC2, AC3 |
| rwb-guarantee claim fake | The insurance claim of the collateral event approved by a person, and one not yet approved | AC2, X6 |
| rwb-valuation re-appraisal fake | The re-appraisal order and the accepted value of `COL-2026-000702`; an appraisal still open | AC3, X8 |
| rwb-source-data collateral fake | The collateral record and the appraised value of `COL-2026-000702`, read only | AC2, AC3 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and outbox, and a stopped chain | AC4, X1 |
| gateway-bff composite route fake | The merged SCR-08 and SCR-06 answers for `RW-2026-000702`, in their flagged and handled states | AC2, AC3 |

The fakes are test-only and are replaced by the real services in SIT. The operation names of the case read, the two claims, the package read and the source-data read carry the placeholder until their owners confirm them (GAP-3063; ASM-5191, ASM-5193, ASM-5194, ASM-5195).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 6 consumed | The deviation outcome operation on `/api/recovery/deviation/v1`; the case read, the case-move answers, the package read, the claim read, the re-appraisal read and the source-data read; one hop, 2 s |
| Kafka | 1 published, 0 consumed | `DeviationCleared` (`EV-07`) on `rwb.deviation.events.v1` with its retry and `.dlt` topics; EV-06 belongs to the raise step (§12.3, §12.4) |
| Temporal | 1 workflow and 1 activity | `DeviationWorkflow` and `recordCollateralOutcome` on `rwb-deviation`; no Schedule and no timer of this story |
| File | None | No file is read, built or delivered here |

### 13. Solution plan

**Package.** Java package `th.co.scb.ace.workbench.recovery.deviation`, module `collateral`; front end `src/modules/recovery/deviation/DeviationQueue.tsx` and `RaiseDeviation.tsx`, the fragments SCR-08 and SCR-06 embed.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the transaction rule of the step: the record, the row update, the event and the answer commit together or not at all. DP-05 is applied as the contract form, because S8 owns no `v_ace_*` view in the Ownership Map. DP-13 moves the base of the legacy path and gives the outcome operation its home. DP-19 is how SCR-06 and SCR-08 reach this service, one hop through the gateway. These four are the whole pattern set of the key; DP-09 (the outbox and inbox library) is a real dependency of the event and is recorded in the registers instead of the metadata table (GAP-3063; ASM-5196).

**Dependencies the tables add and the plan does not hold.** The six consumed rows are class C dependencies in fact and the plan's C row is None, so the story builds against their documents and fakes on Day 1. The outbox library of DP-09 would add `RWB-PLT-TE006-CON`. The mechanism of DP-04 is absent: the package is read as data and evaluated by this service's own evaluator. The lists LOV-DEV-OUTCOME, LOV-DEVIATION and LOV-RAISED-BY are closed lists per Reference Data v5, so the enums in rwb-deviation.yaml stand. The plan's H row stands unchanged.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `DeviationWorkflow` X7 branch | Workflow | Receives the owner's outcome as a signal, reads the package in force and reports the move to the parent |
| `recordCollateralOutcome` | Activity | Reads the deviation and the case, applies R-DEV-06 with the claim gate, R-DEV-12 and R-DEV-19, writes the record, updates the row and sends the answers |
| `CollateralDeviationEvaluator` | Service | The rule evaluation over the package in force, with the two branches, the claim-approved test and the no-fire paths |
| `DeviationRecordWriter` | Library adapter | Writes the record with the rule ID and the version before any change, hash-linked; refuses the step when the write fails |
| `DeviationController` | Controller | The outcome branch of the operation with the capability area, right U, the `Idempotency-Key` and the problem mapping |
| `CaseClient` | Client | The case read of rwb-case, one hop, 2 s, breaker, no retry of its own |
| `RulePackageClient` | Client | The DEV package read of rwb-decision at its version in force |
| `CaseMoveAnswer` | Client | The `DEV_WITH_OWNER`, `DEV_REROUTE` and `ROUTE_D6` answers |
| `ClaimClient` | Client | The claim and its approving person from rwb-guarantee |
| `ReappraisalClient` | Client | The order and the accepted value from rwb-valuation |
| `SourceDataClient` | Client | The collateral record and the appraised value from rwb-source-data (DP-05) |
| `DeviationOutcomeEvent` | Outbox producer | Relays `DeviationCleared` (`EV-07`) in the record's transaction |
| `DeviationQueue`, `RaiseDeviation` | React components | Show the flagged, handled and re-routed states, read only |

**Database and migrations.** Schema ownership: `rwb_deviation` is the only schema this story owns; `rwb_case`, `rwb_decision`, `rwb_guarantee`, `rwb_valuation` and `rwb_source_data` belong to rwb-case, rwb-decision, rwb-guarantee, rwb-valuation and rwb-source-data and are only read or answered through their contracts, never written. No Flyway file. `deviation` arrives with the DB story of this service, and the record, the key and the outbox are library objects created in `rwb_deviation` by their migrations (DP-03). No column is added for the claim, the appraisal or the return point: the claim and the appraisal are other services' facts and the return point is `paused_state`.

**Configuration and reference data.** Reference data is read under DP-06 and DP-07: the parameters are the rule rows and the LOV lists named below, and their reference-data contract is Not specified in the source documents (DOR-RWB-S8-E7007-APP-20).

- R-DEV-06, R-DEV-12 and R-DEV-19, their from and to states and the `deviation_code` conditions: rule rows of the DEV package with their version, never written in code (ASM-5193).
- LOV-DEV-OUTCOME, LOV-DEVIATION and LOV-RAISED-BY: reference lists read with their version (TSD S8 T3.2).
- The capability area "Case record" and its right U: access rows of rwb-access, read through the guard.
- The 2 s budget, the single hop and the breaker are the platform rule of ADR-020; no timer duration is a constant, because this step arms no timer.

**Screen states.** Screen states for SCR-08 Deviation queue and SCR-06 Raise deviation beyond those section 15 gives are Not specified in the source documents (DOR-RWB-S8-E7007-APP-10). The no-access refusal reads MSG-P4-002 when the Case record right U is not held (X2).

**Open decisions.** Open decision DL22 is still open and is carried with its assumptions ASM-1162, ASM-1304, ASM-2217 and ASM-2569, each carried as a confirmed assumption; the build proceeds on those assumptions until DL22 closes.

**Build steps**

1. The X7 branch of `DeviationWorkflow` and its input record, registered on `rwb-deviation` as the stage child of `CaseWorkflow`, with the owner's outcome as its signal.
2. `CaseClient` and `RulePackageClient` against their fakes, with the 2 s budget, the breaker, the moved-case path and the version recorded (AC2, AC3, X4).
3. `ClaimClient`, `ReappraisalClient` and `SourceDataClient` against their fakes, with the unapproved-claim and late-appraisal paths (AC2, AC3, X6, X8).
4. `CollateralDeviationEvaluator` over the package, with R-DEV-06, R-DEV-12, R-DEV-19 and the no-fire paths (AC2, AC3, X6).
5. `DeviationRecordWriter` against the stub, with the failed-write path (AC4, X1).
6. The row update and `CaseMoveAnswer`, with the three moves and the idempotent repeat (AC2, AC3, X7).
7. `DeviationController` with the outcome branch, the rights, the `Idempotency-Key` and the problem mapping of the declared errors, plus the two screen states through the composite route fake (AC2, AC3, X2, X3).
8. `DeviationOutcomeEvent` on the outbox with `DeviationCleared` in the same transaction (AC3, §12.3).
9. The boundary test: no statement outside `rwb_deviation`, no `v_ace_*` read, no write to `rwb_case`, `rwb_decision`, `rwb_guarantee`, `rwb_valuation` or `rwb_source_data` (X9, BR5, BR6).

**Feature flag.** `rwb.deviation.collateral-outcome-v1`, a flag of the platform library; off means the operation answers 503 with no write and no answer, the screen hides the outcome actions, and the raise, timer and screening slices are unaffected.

**Done when.** The tests of section 16 pass, the step runs from a synthetic flagged X7 case in SIT, R-DEV-06 moves the case to `DEV_WITH_OWNER` with the record and the claim gate, R-DEV-12 moves it to `DEV_REROUTE` and R-DEV-19 answers `ROUTE_D6`, an unapproved claim and a moved case are refused, a repeated key writes once, a forced record failure changes nothing, one `DeviationCleared` event is relayed, and no `recovery_case`, `assignment` or `timer` row and no `v_ace_*` read exists in the build.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S8-001 | Carried from the legacy message set of RWB-E7-007: the deviation and its handler are shown once the step succeeds; the information the screen shows after the action | {deviation} was raised. The case is with {handler}. |
| MSG-GEN-001 | A required element of the request is absent or invalid — the assignment, the claim reference or the outcome (X3) | Enter {field}. |
| MSG-P4-002 | A role without the Case record right U calls the outcome (X2) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the row changes (X1) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The four IDs are those of the legacy message set of RWB-E7-007 and of FSD S8 A2.16, and the text is the legacy and FSD wording, copied unchanged; no message is reworded and no new one is added. The required-field rule is VR-S8-016-1 of the module FSD.

### 15. Screens and states

SCR-08 Deviation queue and SCR-06 Raise deviation are served through the gateway-bff composite route (DP-19). The route calls rwb-deviation for the deviation, its code, its handler and its outcome, rwb-case for the case and its route state, and rwb-guarantee for the claim; this story fixes the rwb-deviation answers only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON.

The legacy screen table gives the states "Loading; list" for SCR-08 and "Form; saved" for SCR-06. This story adds no screen and no state: it fills two of the states with the X7 facts — the queue row shows code X7, the handler, the claim state and the return point, and the raise form shows the saved deviation with its outcome. The flagged, handled and re-routed case states are rwb-case's and are shown read only; the refusal, invalid-request and not-recorded states read the messages of section 14. SCR-06 empty, loading, error and no access states: Not specified in the source documents (CG-ALL-11607). SCR-08 empty, error and no access states: Not specified in the source documents (CG-ALL-11608).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E7-007-01 | AC1 (run by RWB-ITG-E7007-ITG; component proof only, not owned by this story) | Component | `RW-2026-000702` with the open X7 deviation; the record, the row update, the outcome and the answer asserted on the fakes |
| TC-E7-007-02 | AC2 | Component | `RW-2026-000702` at `DEV_FLAGGED` with the claim approved by a person; R-DEV-06 applied and the `DEV_WITH_OWNER` move asserted on the fake |
| TC-E7-007-03 | AC3 | Component | `RW-2026-000702` at `DEV_WITH_OWNER` with the estate confirmed; R-DEV-12 applied, `DEV_REROUTE` and then `ROUTE_D6` asserted |
| TC-E7-007-04 | AC4 | Component | The decision-record stub stopped; nothing written, no row updated, no answer sent and MSG-P7-003 shown |
| TC-E7-007-05 | AC5 (access; exception X2) | Component | A role without the Case record right U; 403 with MSG-P4-002 and no read |
| TC-E7-007-06 | Principle 5 | Component | A forced decision record write failure inside the transaction; the deviation stays in its state and no event is relayed |
| TC-E7-007-07 | Contract of the operations, events and activities of section 12 | Contract | Each operation, event and activity of section 12 checked against the published contract in RWB-S8-E7007-CON |
| TC-E7-007-08 | AC6 (exception X9); boundary of the section 12.7 tables (ASM-3438) | Component | Each table of section 12.7 and every statement of the build checked: no statement outside `rwb_deviation`, no `v_ace_*` read, no write to another service's schema |
| TC-E7-007-09 | AC7 (exception X5) | Component | `RW-2026-000702` with the rwb-case contract not answering inside 2 s; the retry on the workflow's schedule, nothing written, no move, no event and 503 with the platform error envelope asserted |
| TC-E7-007-10 | AC8 (exception X5) | Component | The rwb-decision contract fake with its breaker open; nothing written, no move, no event and 503 with the platform error envelope asserted |
| TC-E7-007-11 | AC9 (exception X4) | Component | `RW-2026-000702` not at `DEV_FLAGGED`, and a second outcome for a taken decision; 409 asserted and nothing written |
| TC-E7-007-12 | AC10 (exceptions X2, X3, X4, X5) | Component | One request per refusal path; 403, 422, 409 and 503 asserted with their envelopes; the 401 and 404 cases are Not specified in the source documents (NEWAC-RWB-S8-E7007-APP-AC8) |
| TC-E7-007-13 | AC11 (exception X7) | Component | The same request sent twice and the outcome confirmed twice; one record, one row update, one event and one answer asserted |

The six legacy cases are those of RWB-E7-007 in their legacy order, with the Level column added: every legacy case is tested on the fakes, so every legacy case is `Component`. TC-E7-007-07 is the contract test of section 12 and TC-E7-007-08 the boundary test of section 12.7 and of AC6, both added by this story. TC-E7-007-01 covers legacy AC1, which the split plan gives to RWB-ITG-E7007-ITG; it is carried here as the component-level proof of the same data and flow, and the cross-service journey and its `-ITG` copy belong to the wave 4 harness (ASM-5190). The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same ID.

The harness environment, base hosts, fixture layout, synthetic keys, insurance-claim answer shape, evidence format and retention, and pass or fail gate are Not specified in the source documents (GAP-0472).

### 17. Guardrails

- No business value in code: R-DEV-06, R-DEV-12 and R-DEV-19, the states, the codes, the outcome list, the claim gate and the package version stay rule rows and reference data, never a constant, a default or a branch.
- No personal data in `rwb_deviation`, in an event, in a workflow input or in a log: identifiers, codes, dates, an outcome and a rule version only, and every fixture is synthetic.
- ACE data only through the owner's contract: this service holds no `v_ace_*` grant and reads no ACE table, and a build that adds one fails the boundary test (BR6).
- The case stays with rwb-case: no `recovery_case` row, no case state column, no `assignment` row, no `timer` row and no case write here (BR4).
- A claim is never approved by rule: R-DEV-06 stops at a person's approval, and a build that advances the state without it fails the review (BR3).
- One base, one topic, one queue, one schema and one login per service; no document names another service's base or topic as its own (DP-13, DP-14).
- No retired element is reintroduced: no monolith base, no shared `recovery` schema read, no Quartz row and no shared job table.
- The decision is recorded before the change; a build that answers a move outside the record's transaction fails the review (DP-03).
- The event carries no personal data and no free text beyond the code and the outcome, and it is relayed only in the record's transaction (ASM-5196).

### 18. Traceability

| Requirement ID | Requirement (short) | Story element | Test cases | Feature | L3 process |
|---|---|---|---|---|---|
| REQ-S8-005 | A collateral event triggers an insurance claim and a re-appraisal before the next decision | The claim gate of R-DEV-06, the re-appraisal read, the R-DEV-12 re-route and the R-DEV-19 hand-over | TC-E7-007-02, TC-E7-007-03 | FEAT-DVF-07 | Not specified in the source documents (DOR-RWB-S8-E7007-APP-2) |
| REQ-DVH-005 | A resolved deviation returns the case to the state it paused in, or to the route decision where the outcome changes the route | `paused_state`, `DEV_REROUTE` and `ROUTE_D6` | TC-E7-007-03 | FEAT-DVF-07 | Not specified in the source documents (DOR-RWB-S8-E7007-APP-2) |
| REQ-DVH-011 | The full deviation flows with their approvers, contact stops and return points run end to end | The X7 flow as this story's slice of it | TC-E7-007-01 | FEAT-DVF-07 | Not specified in the source documents (DOR-RWB-S8-E7007-APP-2) |
| ADR-013, ADR-014 | 19 services inside ACE, schema and login per service | `rwb_deviation` and its own login | TC-E7-007-06 | FEAT-DVF-07 | Not specified in the source documents (DOR-RWB-S8-E7007-APP-2) |
| ADR-015, ADR-022 | Kafka with outbox and inbox; local decision record plus central ledger | `DeviationCleared` on the outbox and the record of DP-03 | TC-E7-007-04, TC-E7-007-06 | FEAT-DVF-07 | Not specified in the source documents (DOR-RWB-S8-E7007-APP-2) |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The six consumed rows with their budget and breaker | TC-E7-007-02, TC-E7-007-03 | FEAT-DVF-07 | Not specified in the source documents (DOR-RWB-S8-E7007-APP-2) |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E7-007, disposition Split (rework); feature FEAT-DVF-07 |
| Legacy criteria | AC2, AC3 and AC4 owned word for word; AC1 owned by RWB-ITG-E7007-ITG (ASM-5190) |
| Legacy cases | TC-E7-007-01 to TC-E7-007-06, all six carried |
| Source text | Legacy RWB-E7-007; FSD S8 Deviation handling v3 A2.16, A2.16.2, A2.16.3 and A2.16.4; TSD S8 Deviation handling v2 T2, T3.1, T3.2, T3.3, T4, T5.3, T6.1 and T-A; Business Rules and Routing Logic v4 rows R-DEV-06, R-DEV-12 and R-DEV-19; Event and Messaging Design v5 rows EV-06 and EV-07 |
| Feature and screens | FEAT-DVF-07, SCR-08 Deviation queue, SCR-06 Raise deviation |
| Rules | R-DEV-06 and R-DEV-12 owned; R-DEV-19 and R-DEV-01 named |
| Decoupling patterns | DP03, DP05, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-015, ADR-020, ADR-022 |
| Contract baseline | RWB-S8-E7007-CON |

### 19. Out of scope

- The published shape of the outcome operation, the deviation elements, the consumed rows, the error set and the fakes: RWB-S8-E7007-CON.
- The raise of the deviation, the pause of the stage clock, the contact stop and the prescription clock: the raise and timer slices of this service, FSD S8 A2.1 to A2.6, and rwb-case for the timer row.
- The other handler stories: X1 to X6 are RWB-S8-E7001-APP to RWB-S8-E7006-APP.
- The insurance claim itself, its evidence and its approval screen: rwb-guarantee (S3), FEAT-GUA-08.
- The appraisal order, the valuer and the accepted value: rwb-valuation (S1), FEAT-VAL-01 and FEAT-VAL-02.
- The case of record, its route states, the `assignment` and `timer` rows and the parent `CaseWorkflow`: rwb-case (P3).
- The authoring, testing, approval and versioning of the DEV package and its rule rows: rwb-decision (P7).
- The collateral and appraisal data of ACE and their ingestion: rwb-source-data (P1) and ACE ingestion, never a direct read here.
- The route decision at D6 that receives the re-routed case: rwb-valuation (S1).
- The gateway-bff composite route and the screen field list of SCR-06 and SCR-08: RWB-PLT-N001-CON and the edge stories.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
- The end-to-end cross-service journey and its `-ITG` test copies: RWB-ITG-E7007-ITG and the wave 4 harness.
