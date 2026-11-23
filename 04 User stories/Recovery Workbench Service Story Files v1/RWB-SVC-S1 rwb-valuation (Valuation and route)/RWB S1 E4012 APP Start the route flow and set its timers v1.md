# RWB-S1-E4012-APP Start the route flow and set its timers

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S1-E4012-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-valuation |
| Service epic | RWB-SVC-S1 |
| Wave | 3 |
| Business epic | EP04 |
| Release | 28 February 2027 (tentative) |
| Legacy key | RWB-E4-012 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | L-S1-L |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S1-E4012-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S1 rwb-valuation v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the application slice of RWB-E4-012 split out for rwb-valuation. Both legacy criteria of the key (AC1 and AC2) are copied word for word with their origin tags, and the cross-service parts they touch are mocked. The route flow becomes the `startRouteFlow` step of `RouteDecisionWorkflow` on task queue `rwb-valuation`: after the approval of FEAT-VAL-08 it reads the rule row in force for the approved route on rwb-decision, composes the route start with the task set and the timer set that row names, answers the route start to rwb-case on the case answer of `POST /cases/{caseId}/route` at base `/api/recovery/valuation/v1` (DP-13), writes the decision record through the local library before anything is answered (DP-03) and shows the submitted state of SCR-13 through the gateway-bff composite route (DP-19). The task set, the timer set, their codes and their values are not published (GAP-2648; ASM-4356); the four consumed rows publish no operation name and the plan carries no C row (GAP-2649; ASM-4357); no S1 rule package is in force for the step (GAP-2650; ASM-4358). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **case owner**, I want **the Workbench to open the chosen route, create its tasks and start its clocks**, so that **the route is chosen on expected return with reasons**.

This is the application slice of legacy RWB-E4-012. It owns:

- the two legacy criteria of the key, AC1 and AC2, copied verbatim with their origin tags, and the rules, messages and screen they name;
- the step `startRouteFlow` of `RouteDecisionWorkflow` on `rwb-valuation`, run in the same step as the approval of FEAT-VAL-08 and not later (REQ-S1-007);
- the read of the rule row in force for the approved route, from its `ROUTE_APPROVED_<route>` state on event `ROUTE_APPROVED`, which names the action, the to state and the timer of the first step of the route (routing logic R-RES-01, R-SET-01, R-DIL-01 and R-LIT-01);
- the composition of the route start: the route code, the rule id and rule version, the task set and the timer set of the route, as governed data and never as a constant;
- the answer of the route start to rwb-case on the case answer of `POST /cases/{caseId}/route` on `/api/recovery/valuation/v1`, its right and its `Idempotency-Key` (API-S1-001; DP-13);
- the read of the case state, the right, and the rule with its version, one hop and 2 s each, against their contract mocks;
- the decision record of the route start, written through RWB-PLT-E1027-CON in the caller's transaction before the answer, with the route, the rule id, the rule version, the task set and the timer set applied (DP-03);
- the check that the data product the rule and the case read is not stale, with VR-S1-012-1 and MSG-P1-001;
- the submitted state of SCR-13 Route decision, reached through the gateway-bff composite route (DP-19).

It does not own: the published shape of the route operation, the route-start element set, the four consumed rows, the workflow elements, the rights, the error set and the fakes, which are RWB-S1-E4012-CON; the recommendation and the approval of FEAT-VAL-05 to FEAT-VAL-08, which are the sibling route stories; the `task` and `timer` rows, the case of record, its route states and the parent `CaseWorkflow`, which are rwb-case's (P3); the rule rows, their versions and the central ledger, which are rwb-decision's (P7); the roles and scopes behind the right, which are rwb-access's (P4); the composite route and the field list of SCR-13, which are RWB-PLT-N001-CON; and the deployment, the flag and the alerts of this capability, which are the operations story of this legacy key.

### 2. Business rationale

The route decision is one act in two halves: a person approves a route, and the chosen route must then be open, staffed and timed before the first officer opens the case. FEAT-VAL-12 is that second half. REQ-S1-007 of FSD S1 states it in one line: a route decision starts the route flow and sets its timers in the same step. The legacy key makes that a system feature, run unattended, with the result written to the decision log with the rule version.

Under D-RCV-60 the ownership of the facts around that act changes, and that is what this story carries.

- **the start is rule-driven, not hard-coded.** The route sets of the routing logic already name, per route and per approved state, the action, the to state and the timer: R-RES-01 opens the treatment record on R1, R-SET-01 sets the payoff and range on R2, R-DIL-01 starts the early readiness checks on R3 with 2 working days, R-LIT-01 opens the litigation task and sets the notice and prescription timers on R4 same day. The step applies the row in force and asserts no route, no task and no duration of its own (BR-S1-012).
- **the tasks and the clocks are rwb-case's rows.** The legacy Data table names `task` and `timer` with DF-WRK-017 to DF-WRK-036, and neither table is S1's: the ownership rows give S1 no table at all. This service therefore composes the route start with the task set and the timer set that the rule row names and answers it; rwb-case creates the `task` and `timer` rows and starts the clocks. A build that writes either row fails the boundary test.
- **the clocks are no longer Quartz.** The legacy integration point is the Quartz scheduler, which the target retires (TE-007). A clock in the target is a timer row of the case, driven by the workflow platform of RWB-PLT-E1071; S1 owns no job and no schedule, so this story carries no Temporal Schedule and no Quartz row, and the platform replacement sits with RWB-PLT-E1071 and with rwb-case.
- **same step, one answer.** The route start does not wait for a second call or a second event: it rides on the case answer that the approval already produces, which is why this service publishes no event. The ownership rows give S1 no event, so a route-approved notice on `rwb.valuation.events.v1` would be invented (BR9).
- **the decision is recorded first.** Legacy AC2 makes the step trustworthy: when the record cannot be written nothing changes and the user sees MSG-P7-003. Under DP-03 the record is local, hash-linked and written in the same transaction as the answer, and R-UNI-39 forbids any action that is not logged.
- **stale data stops the start.** VR-S1-012-1 refuses a start on a data product whose ACE batch has not arrived, with MSG-P1-001 naming the product and its date; the route is not opened on yesterday's facts.
- **the case is not reopened.** A route that is already open, or a case that is not in an approved state, does not start a second flow: the answer says so and nothing is created, which is what makes the step idempotent on a repeated command.

The measure of the module is unchanged: recommendations accepted, read monthly from the decision log and the Workbench records. The requirement the step serves is REQ-S1-007.

### 3. Preconditions

- RWB-S1-E4012-CON is published: the route operation with its route-start elements, the four consumed rows, the decision-record element, the workflow elements, the rights, the error set and the fakes are baselined and tagged for this story.
- RWB-PLT-E1027-CON is published with its writer stub: the local decision-record library writes in the caller's transaction, and a failed write stops the step with MSG-P7-003 (DP-03).
- RWB-PLT-N001-CON is published: SCR-13 Route decision reaches this service through the gateway-bff composite route, one hop, and no screen calls a service directly (DP-19).
- The approval of FEAT-VAL-08 has answered in the same workflow execution with the approved route: R1 to R8 of `LOV-ROUTE` (TSD S1 T3.2), its expected return and the rule version under which it was approved.
- The rule row in force for the approved route is available for its mock, read on rwb-decision as `ROUTE_APPROVED_<route>` on event `ROUTE_APPROVED`, and it names the action, the to state and the timer. Its operation name is Not specified in the source documents (GAP-2649; ASM-4357) and is not in this story's contract-dependency list, which is None.
- The task set and the timer set of each route, their codes and their values are Not specified in the source documents beyond the row-level examples of the routing logic (GAP-2648; ASM-4356). They are read as governed rows with their version and are never written in code.
- No S1 rule package is in force and no rule id or parameter is named for the route-start step (GAP-2650; ASM-4358); the rule id and version are read from the answer in force and recorded.
- rwb-case owns `task`, `timer` and the case of record: this service writes neither row, and the route start is answered and not applied (ASM-4357).
- The service runs as its own login on schema `rwb_valuation`, holds the library objects `decision_record` and `idempotency_key`, holds no grant on another `rwb_*` schema and no `v_ace_*` grant, so a statement on `rwb_case`, `rwb_decision` or `rwb_access` is refused by the database (DP-01).
- The legacy story, the FSD S1 v3 and the TSD S1 v2 carry status "In review" and no approval of them is recorded for this run; they are treated as a Draft baseline and this story stays at Draft (realignment v1) (ASM-4336).
- No approval is needed to build against a Draft contract baseline; the contract is tagged by RWB-S1-E4012-CON when its tests pass.

### 4. Flow

1. The approval of FEAT-VAL-08 answers inside `RouteDecisionWorkflow` on `rwb-valuation` with the approved route, its expected return and the rule version; the same execution continues into `startRouteFlow` and no second trigger is awaited (REQ-S1-007).
2. The step reads the case on rwb-case, one hop with a 2 s budget and a breaker: the case reference, its state, the asset link and whether the route is already open; a case not in the `ROUTE_APPROVED_<route>` state or a route already open is answered as "nothing to start" and no second flow begins.
3. The step reads the rule row in force on rwb-decision, one hop with a 2 s budget: the rule id, the rule version, the route set, the action, the to state and the timer for `ROUTE_APPROVED_<route>` on `ROUTE_APPROVED`. A missing answer leaves the step held and nothing is written (GAP-2650).
4. The step checks VR-S1-012-1: where a data product the rule and the case read is stale after a late or failed ACE batch, the start is refused with MSG-P1-001 naming the product and its date, and nothing is created.
5. The step composes the route start from the rule row and the governed data: the route code of `LOV-ROUTE`, the rule id and rule version, the to state, the task set of the route with its task codes, and the timer set with its timer types and their values, all read with their version (BR-S1-012; GAP-2648).
6. The step checks the caller and the case scope: the route command carries the capability area Treatment and offer with right U, checked against the caller's scope, and a caller without it is refused with MSG-P4-002 before any read or write (AC-EXC-S1-012-01).
7. Before the answer is returned, `RouteStartDecisionRecordWriter` writes one decision record through the library of DP-03: the case, the approved route, the expected return, the rule id, the rule version, the to state, the task set and the timer set applied. A failed write stops the step with nothing changed and nothing answered (AC2; R-UNI-39).
8. The step answers the route start to rwb-case on the case answer, and rwb-case opens the route, creates the `task` rows of the task set and the `timer` rows of the timer set and applies the move from `ROUTE_APPROVED_<route>` to the to state the row names (R-RES-01, R-SET-01, R-DIL-01, R-LIT-01). This service writes no case, task or timer row.
9. The workflow commits the step, and the route operation answers `Approval` with the approved route, the route start reference and the rule version applied; a repeat of the same `Idempotency-Key` returns the stored answer and starts no second flow (R-UNI-40).
10. SCR-13 Route decision shows the submitted state with the approved route and the route start, read only through the composite route; a later change of value, payment or deviation reopens the decision as a fresh one (REQ-S1-008, FEAT-VAL-11).
11. Where a clock is recomputed after a legal hold or a resume, the timer set is read again from the rule row in force and answered to rwb-case, which recomputes the `timer` rows (R-UNI-21). No clock is recomputed in this service.
12. Every step of the flow emits no Kafka event: the route start travels on the case answer and the decision record on `rwb.decision-record.v1` through the library (BR9).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The local decision record cannot be written | The transaction writes nothing, no route start is answered and no task or timer is created | MSG-P7-003 | AC2, TC-E4-012-02, TC-E4-012-04 |
| X2 | The caller does not hold the Treatment and offer right of the operation | 403 before any read or write, and no record is written | MSG-P4-002 | TC-E4-012-03 |
| X3 | The data product the rule or the case reads is stale after a late or failed ACE batch | The start is refused, the product and its date are named and nothing is created | MSG-P1-001 | TC-S1-E4012-APP-01 |
| X4 | The rule row in force for the approved route does not answer, or names no to state | The step is held, the parent is told and nothing is written | None (reason on the record) | TC-S1-E4012-APP-01 |
| X5 | The case is not in an approved state, or the route is already open | The answer says "nothing to start", no second flow begins and the repeat is counted | None | TC-E4-012-01 |
| X6 | rwb-case, rwb-decision or rwb-access does not answer inside 2 s, or its breaker is open | The step waits and retries on the workflow's own schedule; nothing is written and the caller sees 503 in the platform envelope | None | TC-E4-012-01 |
| X7 | The same command is submitted twice with the same `Idempotency-Key`, or the same case answer arrives twice | One record, one answer and one route start; the repeat is counted | None | TC-S1-E4012-APP-02 |
| X8 | A component, a statement or a test reaches a `recovery_case`, `task` or `timer` row, a `v_ace_*` view or another service's schema | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | s17, BR8, TC-S1-E4012-APP-01 |
| X9 | The route start is composed with a task code, a timer type or a duration that is not a governed row | The step refuses the start and names the missing row; no value is defaulted | None (reason on the record) | BR1, BR2 |

X1 and X2 are the exception paths the legacy key and the FSD name (MSG-P7-003 and MSG-P4-002), X3 is VR-S1-012-1 of the FSD, X4 to X9 are the paths the target call types, the governed data and the split add. No duration, task code or route is a constant of this story.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-S1-E4012-CON, the rwb-case, rwb-decision and rwb-access fakes and the decision-record stub, on its own schema, and needs no live P3, P6 or P7 |
| Negotiable | The activity names and the shape of the route-start element are this story's choice; the operation, the rules, the messages, the screen and the rights are fixed by the baseline |
| Valuable | The approved route is open, staffed and timed in the same step as the approval, so no case waits overnight for a task or loses a clock |
| Estimable | One workflow step, two activities, three clients, one record write, one case answer and one screen fragment |
| Small | Finished inside two weeks with its tests on the fakes |
| Testable | Each path runs on synthetic cases through the contract fakes, plus the stale product, the missing rule row, the already-open route, the stopped record write and the repeated command |

### 7. Acceptance criteria

```gherkin
Feature: Start the route flow and set its timers

  Scenario: AC1 Start the route flow and set its timers (legacy RWB-E4-012 AC1)
    Given the data and the rule version this feature needs are in place
    Given the rwb-case contract mock returns the case state "ROUTE_APPROVED_LITIGATION" for "RC-2026-000412"
    Given the rwb-decision contract mock returns the rule row in force for route "R4" with its rule id and rule version
    Given the rwb-access contract mock returns the Treatment and offer right U accepted for "RW-CASEOWN"
    When its trigger arrives
    Then opens the chosen route, creates its tasks and starts its clocks
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded (legacy RWB-E4-012 AC2)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

The two criteria are the legacy criteria of RWB-E4-012 word for word, with their origin tag added and nothing else changed: the repetition of `Then`, the wording `opens the chosen route, creates its tasks and starts its clocks` without an added subject, `its trigger arrives`, `the action is taken` and `the decision log cannot be written` all stand. The cross-service parts are mocked, so AC1 carries three `Given the <service> contract mock returns <x>` lines and those lines are the only additions to the legacy text. AC1 says the result is written "to the decision log with the rule version", which is the local decision record of DP-03 on its way to `rwb.decision-record.v1`. The criterion carries no task code, no timer type and no duration: those are governed rows in force (GAP-2648; ASM-4356).

### 8. Business rules

| ID | Rule | Message |
|---|---|---|
| VR-S1-012-1 | Data product stale after a late or failed ACE batch for its source (`v_ace_batch_status`) | MSG-P1-001 {product} is from {date}. Today's ACE batch has not arrived. |
| BR-S1-012 | No value a business person may change is written in code; it is read from reference data with its version | None |
| R-UNI-21 | The hold is lifted: resume the case in the state it paused in, recompute the timers | None |
| R-UNI-38 | A new rule version reaches its effective date: apply it to decisions taken from that date; open cases keep the version they were decided under | None |
| R-UNI-39 | The decision log entry cannot be written: block the action and raise an incident; no action proceeds unlogged | MSG-P7-003 |
| R-UNI-40 | The same event arrives twice with the same key: ignore the second, record the idempotency hit | None |

The two VR and BR rows are the rows of FSD S1 A2.12.3.1, copied character for character. The four universal rules are the rows of the Business Rules and Routing Logic v4 that this step depends on.

| ID | Rule | Source |
|---|---|---|
| BR1 | The route start is the rule row in force for `ROUTE_APPROVED_<route>` on `ROUTE_APPROVED`: its action, its to state and its timer are applied as read, and no route, to state or duration is a constant of the build | FSD S1 A2.12.3.1 BR-S1-012; R-RES-01, R-SET-01, R-DIL-01, R-LIT-01 |
| BR2 | The task set and the timer set of a route are governed rows with a version; a missing row refuses the start and no default is applied | GAP-2648; VR-S1-012-1 |
| BR3 | The route start happens in the same step as the approval and rides on the case answer; it waits for no second call, no second event and no batch | FSD S1 REQ-S1-007; legacy AC1 |
| BR4 | `task` and `timer` are rwb-case's rows: this service composes the sets and answers them, and writes neither row and no case row | Ownership Map (S1 declares no table); TSD S1 T3.1 |
| BR5 | No clock is a Quartz job: S1 owns no job and no schedule, and a clock is a timer row of the case, driven by the workflow platform | TE-007 retirement; context pack S1 ownership rows (no job) |
| BR6 | The route start is recorded before anything is answered, with the case, the route, the expected return, the rule id, the rule version, the to state, the task set and the timer set applied; a failed write changes nothing and shows MSG-P7-003 | DP-03; R-UNI-39; legacy AC2 |
| BR7 | A case not in an approved state and a route already open start nothing; the answer says so and no second flow begins | R-UNI-40; legacy X5 |
| BR8 | No foreign key leaves `rwb_valuation` and no statement reaches another schema or a `v_ace_*` view: the case, the rule, the task and the timer are identifiers of other owners' facts | DP-01; TSD S1 T3.3 |
| BR9 | No event is published: the ownership rows give S1 no event, and the route start adds no name to `rwb.valuation.events.v1` | context pack S1 ownership rows |
| BR10 | A clock is recomputed only from the rule row in force, on a resume or a lifted hold, and by rwb-case on the answered timer set; the recomputation keeps the timer types and changes no route | R-UNI-21; BR1 |
| BR11 | No person name, address, contact value or identity number enters `rwb_valuation`, the decision record, a log or a workflow input; the route start carries identifiers, codes, amounts, dates and a rule version only | Template and Rules v1 §R7.2 (s17) |

### 9. State transitions

The case state is rwb-case's and is not changed by this story: the step answers the route start and rwb-case applies the move to the case of record (BR4). What this story owns is the state of the start step.

| From (case, on rwb-case) | Event | Condition | To |
|---|---|---|---|
| ROUTE_APPROVED_RESTRUCTURE | ROUTE_APPROVED | The approval answered on R1 | PROPOSED_IN_COLLINS (R-RES-01) |
| ROUTE_APPROVED_SETTLEMENT | ROUTE_APPROVED | The approval answered on R2 | PAYOFF_AND_RANGE_SET (R-SET-01) |
| ROUTE_APPROVED_DIL | ROUTE_APPROVED | The approval answered on R3 | EARLY_READINESS_CHECK, timer 2 working days (R-DIL-01) |
| ROUTE_APPROVED_LITIGATION | ROUTE_APPROVED | The approval answered on R4 | NOTICE_GENERATED, timer same day (R-LIT-01) |
| Any approved route state | The record cannot be written | X1 | Unchanged, nothing answered and no task or timer created (AC2) |
| Any approved route state | The rule row or a governed set is missing | X4, X9 | Unchanged, the step held and the parent told |

| Step execution | Event | Condition | To |
|---|---|---|---|
| Waiting | The approval of FEAT-VAL-08 answers | The workflow runs on `rwb-valuation` | Reading the case and the rule |
| Reading the case and the rule | Both answer with their versions | The case is in its approved state and the route is not open | Checking the data product |
| Checking the data product | The product is current | The record is written and the transaction commits | Waiting, with the route start answered |
| Any | The record write, the transaction or a consumed row fails | X1, X6 | Waiting, nothing changed |

The state names are the rows of the D6 route sets and live on the case of record; the timers named against R-DIL-01 and R-LIT-01 are the timer column of those rows. No S1 rule row is in force for this step (GAP-2650; ASM-4358).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-CASEOWN, RW-RESTRUCT, RW-SPECIAL, RW-GUARANT | Treatment and offer U in the legacy permission table of the key: submit the route command that starts the flow and read the route start and the record |
| RW-CASEOWN (CRU), RW-RESTRUCT (CRUA), RW-SPECIAL (CRU), RW-GUARANT (CRU) | TSD S1 T6.1 rows for the capability area; FSD S1 A2.12.3.3 gives the primary use to "None; runs unattended" and the case owner as also using it |
| RW-TEAMMGR, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-LEGAL, RW-CONDUCT, RW-RISK, RW-COE, RW-AUDIT, RW-BIANAL, RW-TRIBE | Treatment and offer R: read only, in scope |
| RW-PRODHEAD, RW-CREDCOMM | Treatment and offer RA: they approve above the limit and at committee, which is FEAT-VAL-09 and not this step |
| SY-CASEWF, SY-RULES, SY-AGENT | Treatment and offer R: the service identities read the step and are subject to the same checks |
| rwb-valuation service identity | Runs the step unattended, reads the case, the rule, the governed sets and the right, answers the route start, writes the decision record and answers the route operation; it holds no grant on another schema and no `v_ace_*` grant |

The rights above are the rows of TSD S1 T6.1 and of the legacy permission table of this key, and nothing wider. The step is an unattended system feature, so the right is checked on the caller of the route command and not on the clock.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-WRK-017 to DF-WRK-026 | `task` (P3) | id, case_id, task_code, element_type, discretion, status and 4 more | Not written: the task set is composed from the rule row and answered to rwb-case |
| DF-WRK-027 to DF-WRK-036 | `timer` (P3) | id, case_id, task_id, timer_type, started_at, expires_at and 4 more | Not written: the timer set is composed from the rule row and answered to rwb-case |
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library, created in `rwb_valuation`) | decision_code, rule_id, rule_version, model_version, inputs reference, outcome, decided at and 12 more | Write, one record per route start, before anything is answered |
| DF-REF-001 to DF-REF-015 | `rule_row` (P7) | rule_id, rule_version, route_set, from_state, event_code, action, to_state and 9 more | Not read as a table: the rule row in force arrives on the rwb-decision row |
| DF-CAS-001 to DF-CAS-023 | `recovery_case` (P3) | id, case_no, product_group, status, stage_code | Not read or written as a table: the case state arrives on the rwb-case row and the route start is answered |
| The task set and the timer set of a route (no Field ID published) | Governed rows read with their version; the row, its owner and its codes are Not specified in the source documents (GAP-2648; ASM-4356) | The task codes of the route and the timer types and values of the route | Consumed as data, recorded in the decision record, never stored as a column |

Field IDs are those of the Logical Data Model and Data Dictionary v8, of TSD S1 T3.1 and of the legacy Data table, with the owners changed by the target. **No new table, no new column and no migration**: the schema `rwb_valuation` and its login arrive with the DB story of this service, and `decision_record` and `idempotency_key` are library objects created in it by the library's migration (DP-03). The ownership rows give S1 no table, so the task set and the timer set applied live in the decision record and in the answer to the case.

**No personal data.** The rows this story reads and writes carry identifiers, codes, amounts, dates and a rule version. No name, address, contact value or identity number enters `rwb_valuation`, the decision record, a log or a workflow input, and every fixture is synthetic.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-valuation (S1); base `/api/recovery/valuation/v1` (DP-13). This story supplies the behaviour behind the one operation the legacy Endpoints table names, and its shape is baselined by RWB-S1-E4012-CON.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| POST | `/cases/{caseId}/route` | `RouteRequest` in and `Approval` out; the answer carries the approved route, the route start reference, the to state and the rule version applied (API-S1-001) | Treatment and offer, right U, scope applied | `Idempotency-Key` header; the stored answer is returned on a repeat, and no second flow starts |

The element list of `RouteRequest` and `Approval` is not published: TSD S1 T-A.2 names the two types and no field table (GAP-2648; ASM-4356). The route start adds no operation of its own. The errors are 409 on a second submission under a new key, 422 with MSG-GEN-001 for an invalid element, and 503 when the decision library or a consumed row does not answer, in one problem envelope. The two valuation operations of the map belong to the appraisal-intake slice of RWB-S1-E4002-CON and are not touched here.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| `GET /cases/{caseId}` family (read) | `/api/recovery/case/v1` | P3 rwb-case | The case state, the asset link and whether the route is open; read only; faked |
| The case-answer of the route start (operation name Not specified in the source documents (GAP-2649; ASM-4357)) | `/api/recovery/case/v1` | P3 rwb-case | The route start with its to state, task set and timer set; applied by the case of record, which creates the `task` and `timer` rows; faked |
| The rule-row read in force (operation name Not specified in the source documents (GAP-2649; ASM-4357)) | `/api/recovery/decision/v1` | P7 rwb-decision | The rule id, the version, the action, the to state and the timer for `ROUTE_APPROVED_<route>` on `ROUTE_APPROVED`, and the governed sets with their version; faked |
| `POST /authorise` | `/api/recovery/access/v1` | P4 rwb-access | The capability area, the right and the scope of the caller; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). These rows are class C dependencies of the plan, whose C row for this slice is empty, so the story builds against their documents and fakes on Day 1 and the absence is recorded as GAP-2649 (ASM-4357).

#### 12.3 Events published

None. The ownership rows give rwb-valuation no event, so this story adds no name, no outbox row and no payload to `rwb.valuation.events.v1`, and a build that publishes one here fails the absence test (BR9). The one publication of the step is the decision record, which the library of DP-03 sends to `rwb.decision-record.v1` in the transaction of the step.

#### 12.4 Events consumed

None. The step is started by the approval of FEAT-VAL-08 inside the same workflow execution, and by nothing else; the ownership rows give S1 no event and no job, and FSD S1 A2.12.4.4 declares no background event for the feature, although A2.12.2 names "a completed ACE batch, an event or a timer" as the generic trigger of the module. No source publishes a name for a route-approved notice, so no subscription is declared. A duplicate of the command is caught by the idempotency row (X7).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `RouteDecisionWorkflow` | Workflow, one execution per case per assessment, continues-as-new | `rwb-valuation` in namespace `rwb-recovery` | Input: the case, the asset key, the route set and the rule package in force; signals: the recommendation ready, the approval answered and the case-answer |
| `startRouteFlow` | Activity, the route start of this story | `rwb-valuation` | The case, the approved route, the expected return and the rule in force in; the to state, the task set, the timer set and the step outcome out |
| `recordRouteStart` | Activity, the record of this story | `rwb-valuation` | The decision record, the idempotency row and the case-answer out, in one transaction |

`RouteDecisionWorkflow` is the one workflow the ownership rows give S1, and the two activities are this story's; the scoring, intake and approval activities belong to the sibling stories. The activity names are a target design choice and are fixed by the baseline so that the workflow history is stable.

#### 12.6 Schedules

None. The ownership rows give S1 no job and the legacy Quartz scheduler is retired (TE-007), so this story declares no Temporal Schedule and no Quartz row. The clocks of the route are timer rows of the case, created by rwb-case on the answered timer set and driven by the workflow platform of RWB-PLT-E1071; S1 schedules nothing.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| None | S1 declares no table | The Ownership Map gives S1 no table; the task set and the timer set applied are elements of the decision record and of the case answer |
| decision_record | PLT library, created in `rwb_valuation` | The local hash-linked decision record, one per route start (DP-03) |
| idempotency_key | PLT library, created in `rwb_valuation` | The key of the repeated command and the answer it holds |

Not owned and never read as a table: `recovery_case`, `assignment`, `task` and `timer` (P3), `decision_log_entry`, `rule_row` and the task and timer reference rows (P7), and every `v_ace_*` view (P1). No foreign key leaves `rwb_valuation` (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case case-state fake | Case `RC-2026-000412` at `ROUTE_APPROVED_LITIGATION` with its asset link and no open route; a case in another state; a case with the route already open | AC1, X5 |
| rwb-case route-start answer fake | The route start accepted with its reference and its created task and timer count; refused with its reason | TC-E4-012-01 |
| rwb-decision rule-row fake | The row in force for `ROUTE_APPROVED_LITIGATION` on `ROUTE_APPROVED` with its rule id and version; the task set and the timer set with their version; a route with no row | AC1, X4 |
| rwb-access authorise fake | Treatment and offer, right U accepted and refused | TC-E4-012-03, X2 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and a stopped chain | AC2, X1 |
| gateway-bff composite route fake | The merged SCR-13 answer for case `RC-2026-000412`, with the approved route and the submitted state read once | AC1, TC-E4-012-01 |

The fakes are test-only and are replaced by the real services in SIT. The rows whose names are not published are stubbed from the documents and carry the placeholder until their owners confirm them (GAP-2649; ASM-4357). The task and timer sets are served by the fake as governed rows with a version and never as constants of the test (GAP-2648; ASM-4356).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 4 consumed | `POST /cases/{caseId}/route` on `/api/recovery/valuation/v1`; the rwb-case case-state and route-start rows, the rwb-decision rule-row and governed-set row and the rwb-access row; one hop, 2 s |
| Kafka | 0 published, 0 consumed | No event of this service and no subscription; the decision record reaches `rwb.decision-record.v1` through the library of DP-03 |
| Temporal | 1 workflow and 2 activities | `RouteDecisionWorkflow`, `startRouteFlow` and `recordRouteStart` on `rwb-valuation`; no Schedule |
| File | None of this service | The route start is composed from governed rows and no file is read or written here |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.valuation`, module `routestart`, Java package `th.co.scb.ace.workbench.recovery.valuation.routestart`; front end `src/modules/recovery/valuation/RouteStart.tsx`, the fragment SCR-13 embeds.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the transaction rule of the step: the record, the idempotency row and the case answer commit together or not at all. DP-13 moves the base of the one operation. DP-19 is how SCR-13 reaches this service, one hop through the gateway. Quartz is not a pattern of this story: the timing platform belongs to RWB-PLT-E1071 and the timer rows to rwb-case, and S1 owns no job.

**Dependencies the tables add and the plan does not hold.** The four consumed rows are class C dependencies of this story and the plan's C row is None, so the story builds against their documents and fakes on Day 1 and the absence is recorded as GAP-2649 (ASM-4357). The three H rows of the metadata are the contract of this key and the two platform contracts of DP-03 and DP-19, and no other H row is added.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `RouteDecisionWorkflow` route-start branch | Workflow | Continues from the approval, runs the start, answers the case and reports the outcome to the parent |
| `startRouteFlow` | Activity | Reads the case and the rule row, checks the data product, composes the to state, the task set and the timer set, validates the command |
| `recordRouteStart` | Activity | Writes the decision record and the idempotency row, answers the case and returns the route start reference and the outcome |
| `CaseStateClient` | Client | The case state, the open-route flag and the route-start answer of rwb-case, one hop, 2 s |
| `RuleRowClient` | Client | The rule row in force and the governed task and timer sets with their version, from rwb-decision, one hop, 2 s |
| `AccessClient` | Client | The capability area, the right and the scope of the caller, one hop, 2 s |
| `DataProductGuard` | Component | VR-S1-012-1: refuses the start on a stale product with MSG-P1-001 naming the product and its date |
| `RouteStartDecisionRecordWriter` | Library adapter | Writes one record per start before anything else changes, hash-linked, and refuses the step when the write fails (DP-03) |
| `RouteController` | Controller | The route operation, its capability area and right, the `Idempotency-Key`, and the problem mapping of 400, 401, 403, 404, 409, 422 and 503 |
| `RouteStart` | React component | Shows the submitted route, its to state and the route start on SCR-13, read only |

**Database and migrations.** No Flyway file. `rwb_valuation` and its login arrive with the DB story of this service, and the decision record and the idempotency key are library objects created in it by the library's migration (DP-03). No column is added for the task set, the timer set or the to state: they are recorded in the decision record and answered to the case.

**Configuration and reference data.**

- The route codes of `LOV-ROUTE` at their version in force (TSD S1 T3.2), read as data and never as constants.
- The task set and the timer set of each route are governed rows with their version; their codes, their owner and their values are not published (GAP-2648; ASM-4356).
- The capability area Treatment and offer and its rights are access rows of rwb-access, read through the guard.
- No parameter is named in the sources for the step and no S1 rule package is in force (GAP-2650; ASM-4358).

**Build steps**

1. The route-start branch of `RouteDecisionWorkflow` and its input record, registered on `rwb-valuation`, with the approval answer as its trigger (REQ-S1-007).
2. `CaseStateClient` against its fake, with the 2 s budget, the breaker and the approved-state and open-route guard (X5, X6).
3. `AccessClient` and the right check, with the refused path (X2).
4. `RuleRowClient` and the governed task and timer sets, with the missing-row and missing-to-state paths (X4, X9).
5. `DataProductGuard` and VR-S1-012-1 with MSG-P1-001 (X3).
6. `startRouteFlow` composing the to state, the task set and the timer set, with the already-open route and the repeated command (X5, X7).
7. `recordRouteStart` and `RouteStartDecisionRecordWriter` against the library stub, with the failed-write path (AC2, X1).
8. `RouteController` with the right, the `Idempotency-Key` and the problem mapping (TC-E4-012-03).
9. `RouteStart` and SCR-13 through the composite route fake (TC-E4-012-01).
10. The boundary test: no statement outside `rwb_valuation`, no `v_ace_*` read, no write to `rwb_case`, `rwb_decision` or `rwb_access`, no `task` or `timer` row and no outbox row (X8, BR8, BR9).

**Feature flag.** `rwb.valuation.route-start-v1`, read as a flag of the platform library; off means the route is not opened from this step, the case keeps its approved state and the manual fallback is the operations runbook of this legacy key.

**Done when.** The tests of section 16 pass, an approved route opens one route, creates its tasks and starts its clocks in SIT, a stale product or a missing rule row refuses the start, a forced record failure changes nothing and shows MSG-P7-003, no `task`, `timer` or `recovery_case` row exists in the build, and SCR-13 answers through the gateway-bff composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required element of the command is absent or invalid (X9) | Enter {field}. |
| MSG-P4-002 | A role without the Treatment and offer right calls the route operation (X2) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the route start changes anything (X1, AC2) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | The data product is stale after a late or failed ACE batch (X3) | {product} is from {date}. Today's ACE batch has not arrived. |

The three messages of the legacy key are copied unchanged from its message set, and MSG-P1-001 is copied from VR-S1-012-1 of FSD S1. No message is reworded and no new one is added; a refused or held start carries its reason on the decision record and in the screen state, and no source publishes a message text for it.

### 15. Screens and states

SCR-13 Route decision is served through the gateway-bff composite route (DP-19), and this story fixes the route-start part of its answer and the states it can show.

| Screen | States | What this story sets |
|---|---|---|
| SCR-13 Route decision | Loading; recommendation; overridden; submitted | Submitted with the approved route, its to state and the route start; plus refused with MSG-P4-002, not recorded with MSG-P7-003, stale with MSG-P1-001, invalid with MSG-GEN-001, and held where the rule row is missing. Loading, recommendation and overridden are the sibling stories' |

The screen's route elements, its merge order and its field list belong to RWB-PLT-N001-CON and the sibling route stories of this service; the route-start element and the states above are this story's.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E4-012-01 | AC1: the approved route is opened, its tasks created and its clocks started, and the result is recorded with the rule version; a case not in an approved state and an already-open route start nothing | Component | Case `RC-2026-000412`, approved route `R4`, the rule row in force, one route already open and one case in another state |
| TC-E4-012-02 | AC2: the decision log cannot be written | Component | The decision-record stub stopped; nothing written, no route start and MSG-P7-003 shown |
| TC-E4-012-03 | Access: a role without the right | Component | A role without Treatment and offer U; 403 with MSG-P4-002 and no read |
| TC-E4-012-04 | Principle 5: a forced decision log write failure | NFR | A forced failure at the moment of the route start; no record, no case answer and no event |
| TC-S1-E4012-APP-01 | The stale product and the missing rule row: the start is refused and named, and nothing is created | Component | A product with a yesterday date and `v_ace_batch_status` naming its source; a route with no rule row and a row with no to state |
| TC-S1-E4012-APP-02 | Idempotency and the boundary: one start per case, and no `task`, `timer`, `v_ace_*` or foreign-schema write | Component | The same command twice under one key; the build scan of step 10, plus an outbox that must stay empty |

The four legacy case IDs are the legacy cases of RWB-E4-012 in their legacy order, with the Level column added. TC-E4-012-01 is Component because the step is tested on its fakes; the legacy wording of the case is kept in the Test Cases workbook, where the full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases. The `-ITG` copies belong to the wave 3 harness.

### 17. Guardrails

- No business value in code: the route codes, the to states, the task codes, the timer types and their durations stay governed rows or a rule row read with their version, never a constant, a default or a branch of the build.
- No personal data in `rwb_valuation`, in a workflow input or in a log: identifiers, codes, amounts, dates and a rule version only, and every fixture is synthetic.
- ACE data only through the owner's contract: this service holds no `v_ace_*` grant and reads no ACE table, and a build that adds one fails the boundary test.
- The case, the tasks and the timers stay with rwb-case: no `recovery_case`, `assignment`, `task` or `timer` row is written here, and the route start is answered and not applied (BR4).
- The decision is recorded before the answer and the command is idempotent; a build that answers a start before its record fails the review (DP-03, BR6, BR7).
- No clock is a Quartz job or a local scheduler row: a build that adds a job, a Schedule or a `timer` write fails the review (BR5, BR10).
- One base, one topic, one queue and one login per service; no document, module or test names another service's base or topic as its own (DP-13, DP-14).
- No retired element is reintroduced: no shared job table, no Quartz row, no monolith base `/api/recovery/v1`, no event published by this step, no `v_ace_*` read.

### 18. Traceability

| Source | Reference | Used in |
|---|---|---|
| Legacy story | RWB-E4-012, disposition Split (rework); AC1 and AC2 owned word for word by this story | 1, 7, 16 |
| Feature | FEAT-VAL-12 Start the route flow and set its timers, module S1, epic E4, system, depends on FEAT-VAL-08 | 1, 2, 3, 8 |
| FSD S1 v3 | A1.4 preconditions; A2.12.1 to A2.12.3.3, including VR-S1-012-1 and BR-S1-012; A2.12.4.1 to A2.12.4.4; REQ-S1-007; SCR-13 | 2, 3, 4, 5, 8, 11, 14, 15 |
| TSD S1 v2 | T2 components; T3.0 standard columns; T3.1 `valuation` and `score`; T3.2 `LOV-ROUTE`; T3.3 relationships; T4 no state machine; T5.2 and T5.3; T6.1 rights; T-A.1 and T-A.2 API-S1-001 | 3, 10, 11, 12, 13, 16 |
| Logical data model | DF-WRK-017 to DF-WRK-036, DF-DEC-001 to DF-DEC-018, DF-REF-001 to DF-REF-015, DF-CAS-001 to DF-CAS-023 | 11 |
| Routing logic | R-RES-01, R-SET-01, R-DIL-01 and R-LIT-01 (route start, to state and timer); R-UNI-21, R-UNI-38, R-UNI-39, R-UNI-40; no S1 route rule is in force, because the S1 package is Phase 2 | 2, 4, 8, 9, 14 |
| Patterns | DP-03, DP-13, DP-19 (Template and Rules v1 §R5.5) | 13 |
| Gaps and assumptions | GAP-2648 to -3; ASM-4356 to -4 | 1, 3, 4, 11, 12, 13, 14 |
| Decisions | ADR-013, ADR-014, ADR-015, ADR-016, ADR-020, ADR-022; D-RCV-60 | all |

### 19. Out of scope

- The published shape of the route operation, the route-start element set, the four consumed rows, the decision-record element, the workflow elements, the error set and the fakes: RWB-S1-E4012-CON.
- The recommendation, the expected return by route and the approval of FEAT-VAL-05 to FEAT-VAL-08: the sibling route stories of this service.
- The above-limit committee approval of FEAT-VAL-09, the hold of FEAT-VAL-10 and the reconsideration of FEAT-VAL-11: sibling stories of this service.
- The case of record, its route states, the `task` and `timer` rows and the parent `CaseWorkflow`: rwb-case (P3).
- The route's own flow after its first step, for example the treatment record of R-RES-01 and the litigation task of R-LIT-01: the route services S2 to S7.
- The rule rows, the governed task and timer sets, their versions and the central ledger: rwb-decision (P7) and their business owners.
- The roles, scopes and masking behind the right: rwb-access (P4).
- The composite route, the merge order and the field list of SCR-13: RWB-PLT-N001-CON and the edge stories.
- The decision-record library's own schema, the timing platform and the Schedule replacement: RWB-PLT-E1027-CON and RWB-PLT-E1071-CON.
- The cross-service journey of the legacy key and its evidence: the wave 3 harness.
- The deployment, the flag, the dashboards, the alerts and the runbook of this capability: the operations story of this legacy key.
