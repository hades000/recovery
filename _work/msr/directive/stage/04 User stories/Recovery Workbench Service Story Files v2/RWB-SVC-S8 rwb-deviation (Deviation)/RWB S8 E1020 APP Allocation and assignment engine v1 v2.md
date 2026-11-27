# RWB-S8-E1020-APP Allocation and assignment engine v1

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S8-E1020-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-deviation |
| Service epic | RWB-SVC-S8 |
| Wave | 1 |
| Service wave | 2 (rwb-deviation, Architecture v5); this story is delivered in business wave 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-020 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP04, DP05, DP06, DP07, DP09, DP10, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | L-S8-A |
| Ready to start | Day 1 |
| Size | Not set; the squad sizes it at refinement (DOR-RWB-S8-E1020-APP-16) |
| Depends on (build) | None |
| Contract dependencies | RWB-P3-E1020-CON |
| Contract version | /v1 for this story's own operations on /api/recovery/deviation/v1 (DP-13); version of RWB-P3-E1020-CON not specified in the source documents (DOR-RWB-S8-E1020-APP-23) |
| Integration dependencies | None |
| External dependencies | None |
| Platform preconditions | Wave 0 until the plan carries them: the platform contracts of the DP rows (GAP-3073) |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S8 rwb-deviation v1.md (no FR mapped to REQ-CWC-007, REQ-CWC-008, REQ-CWC-009, REQ-CWC-016) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: the deviation slice of RWB-E1-020 is realigned onto rwb-deviation (S8, service wave 2, business wave 1). The legacy key allocates every new case by rule; its exception X4 sends a case with an open deviation to the deviation handler queue with no case owner. In the target the deviation, its handler queue and its named owner are this service's, while the case, the queue, the assignment and the timers stay with rwb-case, so this slice builds the placement answer the morning allocation needs: the handler queue code from the parameter `allocation.deviation.queue.code`, the handler by code from the DEV package (R-DEV-01, R-DEV-03 to R-DEV-06, R-DEV-21), the decision record before the row (DP-03), `DeviationRaised` from the outbox (DP-09, DP-14) and the stage outcome the parent applies. The two operations stay on `/api/recovery/deviation/v1` (DP-13) and the two screens behind the gateway-bff composite route (DP-19). The case owns no queue column, so no migration adds one; the plan gives this key no CON story of its own, and the boundary shape, the handler roster and the assignment method are not published (GAP-3072, GAP-3073; ASM-5230 to ASM-5234). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-S8-E1020-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (32 resolved, 27 cross-document, 2 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **team manager (RW-TEAMMGR)**, I want **a new case that carries an open deviation to be sent to the deviation handler queue with one named handler instead of being given a case owner by the morning allocation**, so that **every case at 90 days past due that no case owner may work has one handler, one queue and one recorded reason from its first day**.

This story owns:

- the deviation half of the legacy exception X4: the handler queue code of a case with an open deviation, and the named handler of that deviation by code (R-DEV-01, R-DEV-03 to R-DEV-06, R-DEV-21);
- the handler choice for the codes X2 to X7 and for an unmapped code, which RWB-S8-E7001-APP does not build;
- the `deviation` row's `handler_user_id` and `state` in `rwb_deviation`, its decision record written before the change (DP-03), and its `DeviationRaised` row in the outbox (EV-06);
- the placement answer returned to rwb-case as the stage outcome of `DeviationWorkflow`, the child of the case, on task queue `rwb-deviation` in namespace `rwb-recovery`;
- the read-only deviation queue slice of SCR-08 and the queue and owner columns of SCR-02 behind the gateway-bff composite route (DP-19);
- the idempotency of the placement per case and business date, and the one migration that indexes the two reads it needs.

It does not own: the case of record, its queue, its assignment, its timers and the morning run JOB-03 (rwb-case, P3); the X1 raise and outcome journey (RWB-S8-E7001-APP); the DEV rule rows, their versions and the central ledger (rwb-decision, P7); the roles, the rights and the reference values (rwb-access P4, rwb-case P3); the contact stop, the evidence pack and the notices (X1 to X3 flows, P5 and P6); and the schema, deployment and observability of this service (the DB, INF and OPS stories of this legacy key).

### 2. Business rationale

The objective and the measure do not move: deviations closed within the service level, measured on the decision record and the Workbench records and reviewed monthly (FSD S8 A2.4.1). The service-side requirement is REQ-DVH-003, "Each deviation code routes to its named owner, and a code with no owner routes to the team manager and is recorded as unmapped" (FSD S8 Requirements served).

The legacy problem is that a case can be owned by nobody: the allocation engine of RWB-E1-020 places every new case in a queue and gives it an owner by rule before 07:00, but a case that already carries a deviation cannot be worked by a case owner, and the legacy path is one monolith method that reads `deviation_open`, reads the queue table and writes both the case and the deviation (RWB-E1-020 sections 3, 4 and 5 X4).

D-RCV-60 changes who owns each fact, not what the team manager gets:

- **The deviation and its handler are this service's.** `deviation` is the one table the Ownership Map gives S8, its `handler_user_id` and its `state` are its columns, and the DEV package is evaluated inside this service by its own embedded kit (context pack ownership rows; TSD S8 T0.2, T3.1; DP-01, DP-04).
- **The case, the queue and the owner are rwb-case's.** `recovery_case`, `queue`, `queue_member` and `assignment` are P3's, and the S8 row of the connection matrix names Temporal and events to P3 and never REST, so the diversion is answered as a child-workflow outcome and this story writes no case, queue or assignment row (Architecture v5 slides 8 and 13; ASM-5230).
- **The handler queue code is a parameter, not a constant.** "DEV-HANDLER" is the value the legacy section 3 says is assumed under DL23, and in the target the code is read from `allocation.deviation.queue.code` through the parameters contract of rwb-case (DP-06; ASM-5232).
- **The decision is recorded first**, in the same transaction as the deviation change and before the event leaves: that is what TSD S8 T2 states and what the legacy decision-log rules require (DP-03).
- **The event leaves from the outbox** on `rwb.deviation.events.v1`, with rwb-case, rwb-comms and rwb-treatment as its listeners (TSD S8 T5.2.1; ASM-5234).

No business value moves: the deviation codes, the raised-by values, the handler roles, the state names and the queue code stay rule rows or reference data read with their version, never a constant of the code.

### 3. Preconditions

- The service baseline is in place: `rwb-deviation`, schema `rwb_deviation`, base `/api/recovery/deviation/v1`, topic `rwb.deviation.events.v1` with `.retry` and `.dlt`, task queue `rwb-deviation` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.deviation`, gateway-bff for its screens (context pack service row; TSD S8 T0.1).
- The plan gives this key H = None, C = `RWB-P3-E1020-CON` only, so the two published operations of the service and the platform contracts behind the DP rows are preconditions already in place rather than in-lane build dependencies (GAP-3073; ASM-5233).
- `RWB-P3-E1020-CON` is published with its fake: the case element the parent presents (case reference, product group, region, exposure band, business date, the open deviation reference and code) and the stage outcome it accepts. The element names of both shapes are Not specified in the source documents (GAP-3072; ASM-5230).
- rwb-case starts `DeviationWorkflow` on `rwb-deviation` as the child of `CaseWorkflow`, with parent close policy ABANDON and continue-as-new; the case router of P3 forwards the case and never calls this service over REST (TSD S8 T5.2.1; Architecture v5 slide 13).
- `deviation` exists in `rwb_deviation` from the DB story of this service with the fields DF-CAS-036 to DF-CAS-045 and the standard record columns of TSD S8 T3.0; this story adds no column (DP-15).
- The DEV rule package is in force at its version with R-DEV-01, R-DEV-03, R-DEV-04, R-DEV-05, R-DEV-06 and R-DEV-21; it is authored, tested and approved in rwb-decision and loaded here, and this service evaluates it with its embedded kit (DP-04; TSD S8 T2).
- The parameter `allocation.deviation.queue.code` holds "DEV-HANDLER", the value DL23 assumes, read through the parameters contract of rwb-case (DP-06; RWB-E1-020 sections 3 and 4; ASM-5232).
- The lists LOV-DEVIATION (X1 to X7), LOV-RAISED-BY (SCREENING_AGENT, RULE, OFFICER, CUSTOMER_CONTACT) and LOV-DEV-OUTCOME (RETURNED, RE_ROUTED, CASE_ENDED) are read through the reference-data contract of rwb-case (DP-07; TSD S8 T3.2).
- The queue and its members are P3's rows: the handler candidates of a queue arrive on the P3 contract, and this service keeps no copy of a queue, a member or a cap (GAP-3072; ASM-5231).
- The service runs as its own login on `rwb_deviation` and holds no grant on another `rwb_*` schema and no `v_ace_*` grant, so a statement on `rwb_case` fails the boundary test (DP-01, DP-02).
- No approval is needed to build against a Draft contract baseline; the contract is tagged when its tests pass.

### 4. Flow

1. The morning allocation of rwb-case reaches a NEW case for business date 2026-12-01 and starts `DeviationWorkflow` on queue `rwb-deviation` as the child of `CaseWorkflow`, with the case element of `RWB-P3-E1020-CON`; the run itself stays JOB-03 of P3 (RWB-E1-020 sections 3 and 4; ASM-5230).
2. The workflow reads the case's open deviation from its own rows: a row whose `cleared_at` is empty and whose `state` is not RESUMED, DEV_REJECTED or CASE_ENDED. With no open deviation it answers NO_DEVIATION and ends, and nothing is written (AC4).
3. `evaluateHandlerRules` loads the DEV package version in force and evaluates R-DEV-01 for the open code: the deviation is flagged, the stage clock pauses and the prescription clock keeps running. It then evaluates the code rule: R-DEV-03 for X2 and X3, R-DEV-04 for X4, R-DEV-05 for X5, R-DEV-06 for X6 and X7, and R-DEV-21 where the code is outside X1 to X7 or the code has no owner (Business Rules and Routing Logic v4).
4. The handler queue code is read from the parameter `allocation.deviation.queue.code` through the parameters contract of rwb-case; "DEV-HANDLER" is the value in force and no queue code is written in code (DP-06; ASM-5232).
5. `assignHandler` picks the handler the fired rule names from the members the P3 contract lists for that queue, taking the handler with the fewest open deviations in this service's own rows; no cap is applied, because no source publishes a handler cap (GAP-3072; ASM-5231).
6. `recordAndApplyPlacement` writes one decision record through the local library before any change: case reference, business date, deviation reference, code, rule ID with the package version, the queue code, the handler reference, the inputs reference and the decided-at time; the queue code and the handler reference are named members of the actions payload (DP-03; TSD S8 T2).
7. In the same `rwb_deviation` transaction the activity updates the row: `handler_user_id`, `state` = DEV_WITH_OWNER, `version`, `updated_at` and `updated_by`, and writes the outbox row for `DeviationRaised` with identifiers, the code, the queue code, the rule ID and version and no personal data (DP-09).
8. The workflow returns the stage outcome to the parent: the deviation reference, the queue code, the handler reference, the rule IDs with their versions and PLACE_DEVIATION_QUEUE. The parent places the case in the queue, keeps status NEW, sets no case owner and pauses the stage clock (R-DEV-01; ASM-5230).
9. A repeat presentation for the same case and business date answers the placement already recorded, writes nothing, publishes no second event and counts the repeat (R-UNI-40).
10. SCR-08 Deviation queue shows the open deviation with its type, its handler and its age, and SCR-02 Case list shows the case in the handler queue with no owner; both are composed by gateway-bff and neither writes anything (DP-19). SCR-08 empty, error and no-access states and SCR-02 error and no-access states are Not specified in the source documents (DOR-RWB-S8-E1020-APP-10).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The decision record cannot be written | Nothing changes: no handler, no state move and no event, the case is not diverted, and the step answers a failure | MSG-P7-003 | AC5 |
| X2 | No DEV package version is in force at the run | The step holds before any case is placed, the run of that case is reported and the case keeps status NEW | MSG-P3-027 | AC5 |
| X3 | The parameter `allocation.deviation.queue.code` has no value, or names a queue the P3 contract does not list | The placement holds, the handler is not assigned and the case is not diverted; the parameter and the missing queue are named | None (platform 503 envelope) | AC3 |
| X4 | The P3 contract does not answer inside 2 s or its breaker is open | The placement holds, the handler is not assigned and the case stays NEW with no queue and no owner | None (platform 503 envelope) | AC1 |
| X5 | The case's open deviation is already in DEV_WITH_OWNER with a handler | The existing handler is answered and nothing is rewritten; the placement is not repeated | None | AC7 |
| X6 | The code is outside X1 to X7, or the code has no owner | R-DEV-21 assigns the case owner's team manager and records the code as unmapped | None | AC6 |
| X7 | A repeat presentation for the same case and business date | The recorded placement is answered, the repeat is counted and no second row, record or event leaves | None | AC7 |
| X8 | A component, a statement or a test reaches a `v_ace_*` view, a `rwb_case` row or another service's schema | The grant refuses the statement and the boundary test fails the build | None (pipeline log) | AC8, Section 17, BR5, BR6 |

X1 to X4 are the paths the target call types and the container add; X6 is the unmapped-code path the FSD requires; X5 and X7 are the idempotency of the placement; X8 is the DP-01 and DP-05 boundary. The legacy per-case paths of the allocation itself — overflow, exception queue, repeated run, a case that is not NEW — are RWB-P3-E1020-APP's.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against `RWB-P3-E1020-CON`, the DEV package fixture, the decision-record stub, the outbox relay stub and the parameters and reference-data fakes, on its own schema, and needs no live P1, P3 or P7 |
| Negotiable | The activity names, the shape of the placement answer and the tie-break of two handlers with the same load are this story's choice; the rules, the state names, the queue code source and the `deviation` fields are fixed |
| Valuable | A case that already carries a deviation is diverted on the morning it arrives, with one handler, one queue, one recorded decision and no case owner |
| Estimable | One workflow branch, two activities, one event publication, two reads, one migration and the boundary and failure tests |
| Small | Finished inside two weeks with its tests on the fakes |
| Testable | Every path runs on synthetic cases through the contract fakes, plus the forced record failure and the missing-parameter path |

### 7. Acceptance criteria

```gherkin
Feature: Allocation and assignment engine v1 - the deviation handler slice

  Background:
    Given the DEV rule package is in force at its version and carries R-DEV-01, R-DEV-03, R-DEV-04, R-DEV-05, R-DEV-06 and R-DEV-21
    Given the parameter "allocation.deviation.queue.code" holds "DEV-HANDLER" through the rwb-case parameters contract
    Given the business date is 2026-12-01
    Given the rwb-case contract mock returns case "RW-2026-000206" with status "NEW", product group "MORTGAGE", region "BKK", exposure band "B2" and an open deviation of code "X3"

  Scenario: AC1 A case with an open deviation is diverted to the handler queue (new, D-RCV-60)
    Given the rwb-case contract mock returns case "RW-2026-000206" in status "NEW" with an open deviation of code "X3"
    When the morning allocation presents case "RW-2026-000206" to rwb-deviation for business date 2026-12-01
    Then the answer names the handler queue "DEV-HANDLER" and rule "R-DEV-01" with the package version in force
    Then the answer carries no case owner and the case keeps status "NEW"
    Then the deviation row is in state "DEV_WITH_OWNER" with the specialist as handler
    Then one decision record carries rule "R-DEV-03" and the package version in force
    Then rwb.deviation.DeviationRaised.v1 is published on topic rwb.deviation.events.v1 with the case reference and code "X3"

  Scenario: AC2 The code decides the named owner (new, D-RCV-60)
    Given the rwb-case contract mock returns four new cases with an open deviation of code "X2", "X4", "X5" and "X6"
    When the morning allocation presents each case for business date 2026-12-01
    Then the X2 case is assigned to the specialist by rule "R-DEV-03"
    Then the X4 case is assigned to the fraud team by rule "R-DEV-04"
    Then the X5 case is assigned to Legal by rule "R-DEV-05"
    Then the X6 case is assigned to the agent with the case owner approving by rule "R-DEV-06"
    Then each decision record names its own rule ID and the package version in force

  Scenario: AC3 The handler queue is a parameter, not a constant (new, D-RCV-60)
    Given the rwb-case parameters contract returns "DEV-HANDLER-2" for the parameter "allocation.deviation.queue.code"
    When the morning allocation presents a new case with an open deviation of code "X2"
    Then the answer names the handler queue "DEV-HANDLER-2" with no deployment
    Then the decision record carries the queue code it used
    Then when the parameter holds no value the placement holds, writes nothing and the case is not diverted

  Scenario: AC4 A case with no open deviation is left to the allocation (new, D-RCV-60)
    Given the rwb-case contract mock returns case "RW-2026-000210" with status "NEW" and no open deviation
    When the morning allocation presents the case for business date 2026-12-01
    Then the answer carries no handler queue, no handler and no rule ID
    Then this service writes no deviation row, no decision record and no event
    Then the case is allocated by the rules of rwb-case as if this service had not been called

  Scenario: AC5 A placement that cannot be recorded changes nothing (new, D-RCV-60)
    Given the decision record write is forced to fail for case "RW-2026-000206"
    When the morning allocation presents the case
    Then no handler is written and the deviation keeps the state it had
    Then no DeviationRaised is published and the answer names the failure
    Then the case is not diverted and keeps status "NEW" with no queue and no owner
    Then the caller sees MSG-P7-003

  Scenario: AC6 An unmapped code goes to the team manager and is recorded (new, D-RCV-60)
    Given the rwb-case contract mock returns a new case with an open deviation whose code is outside "X1" to "X7"
    When the morning allocation presents the case
    Then the deviation is assigned to the case owner's team manager by rule "R-DEV-21"
    Then the decision record names rule "R-DEV-21" and the code it could not map
    Then the case is diverted to the handler queue "DEV-HANDLER" with no case owner

  Scenario: AC7 The same case on the same business date has one placement (new, D-RCV-60)
    Given case "RW-2026-000206" was presented and diverted for business date 2026-12-01
    When the morning allocation presents the same case again for 2026-12-01
    Then no second deviation row, no second decision record and no second event are written
    Then the answer is the placement already recorded and the repeat is counted

  Scenario: AC8 A statement against another service's schema is refused by the boundary test (new, D-RCV-60)
    Given the boundary test runs on the build of this service
    When a component, a statement or a test reads a `v_ace_*` view, reads or writes a `rwb_case` row or touches another service's schema
    Then the grant refuses the statement
    Then the boundary test fails the build

  Scenario: AC9 A provided operation answers 401, 403 and 404 for its error cases (new, D-RCV-60)
    Given a caller presents no credential to an operation on "/api/recovery/deviation/v1"
    When the caller calls the operation
    Then the answer is 401
    Then a caller without Case record U gets 403 with MSG-P4-002
    Then an operation that names a case that does not exist answers 404

  Scenario: AC10 A replay of a write with the same idempotency key writes nothing new (new, D-RCV-60)
    Given the placement for case "RW-2026-000206" was recorded for business date 2026-12-01
    When the same write is replayed with the same idempotency key
    Then the recorded answer is returned
    Then no second deviation row, no second decision record and no second event are written

  Scenario: AC11 A retried or timed-out activity holds the placement and changes nothing (new, D-RCV-60)
    Given the rwb-case contract mock does not answer inside the time Not specified in the source documents (NEWAC-RWB-S8-E1020-APP-AC12) for case "RW-2026-000206"
    When the morning allocation presents the case and the activity is retried or times out
    Then the placement holds, the handler is not assigned and the case stays "NEW" with no queue and no owner
    Then no deviation row, decision record or event is written

  Scenario: AC12 A status change the model does not allow is refused (new, D-RCV-60)
    Given the deviation for case "RW-2026-000206" is in state "DEV_WITH_OWNER"
    When a status change the deviation model does not allow is requested
    Then the change is refused and the deviation keeps its state
    Then no DeviationRaised is published
```

AC1 to AC12 are the criteria this story owns, and every one of them is new under D-RCV-60 because this slice owns no legacy acceptance criterion: the plan gives the one criterion of the legacy key that covers the diversion, AC7 of RWB-E1-020, to RWB-P3-E1020-APP, and this story proves the deviation half of it. The case number, the zone suffix of AC3 and the codes X2 to X7 are synthetic test data except the codes, which are the LOV-DEVIATION values of TSD S8 T3.2; no business value is invented, because the queue code comes from the parameter, the handler from the rule and the state from the DEV package.

### 8. Business rules

| Rule | Route set | Codes | From state | Event | Condition | Action | To state | Owner | Systems | Timer |
|---|---|---|---|---|---|---|---|---|---|---|
| R-DEV-01 (BR1) | Deviations | X1 to X7 | ANY_STATE | DEVIATION_FLAGGED | deviation_code in (X1..X7) | Pause the stage clock, keep the prescription clock running, route to the named owner | DEV_FLAGGED | Workbench | Workbench, the Workbench document hub | same day |
| R-DEV-03 (BR4) | Deviations | X1 to X7 | DEV_FLAGGED | OWNER_ASSIGNED | deviation_code in (X2,X3) | Assign to the specialist; Legal joins X3 for the estate claim | DEV_WITH_OWNER | Specialist, Legal | Workbench | None |
| R-DEV-04 (BR4) | Deviations | X1 to X7 | DEV_FLAGGED | OWNER_ASSIGNED | deviation_code = X4 | Assign to the fraud team and refer to Aric | DEV_WITH_OWNER | Fraud team | Aric, Workbench | None |
| R-DEV-05 (BR4) | Deviations | X1 to X7 | DEV_FLAGGED | OWNER_ASSIGNED | deviation_code = X5 | Assign to Legal; file with the official receiver or the LED before the deadline | DEV_WITH_OWNER | Legal | LIT, Workbench | deadline driven |
| R-DEV-06 (BR4) | Deviations | X1 to X7 | DEV_FLAGGED | OWNER_ASSIGNED | deviation_code in (X6,X7) | Agent handles within policy; a person approves an insurance claim | DEV_WITH_OWNER | Agent, case owner | Workbench | None |
| R-DEV-21 (BR4) | Deviations | X1 to X7 | DEV_FLAGGED | OWNER_ASSIGNED | deviation_code is not one of X1 to X7, or no owner is set for the code | Assign to the case owner's team manager and log the unmapped code | DEV_WITH_OWNER | Team manager | Workbench | same day |

The six rows are the rows of Business Rules and Routing Logic v4, copied character for character apart from the BR tags in the rule ID column; their states are the DEVIATION states of TSD S8 T4 and their rule IDs are the ones the DEV package carries, never a constant of the code. R-DEV-02 is RWB-S8-E7001-APP's (the X1 complaint officer) and R-DEV-07 to R-DEV-20 and R-DEV-22 are the outcome and escalation rules of the other stories of this service; this story places a deviation, it does not resolve one.

Wave: this story is wave 1 as W-MAP gives it for EP01, and rwb-deviation starts in wave 2 in Architecture v5. W-MAP is kept (GAP-0064, GAP-1456): the business-epic wave is kept, and the build wave per story is Not specified in the source documents (GAP-1456).

| ID | Rule | Source |
|---|---|---|
| BR1 | A case that carries an open deviation is never given a case owner by the morning allocation: it is answered with the handler queue code and one handler, and the case keeps status NEW | RWB-E1-020 AC7, section 5 X4; R-DEV-01; REQ-DVH-003 |
| BR2 | The decision is recorded before the deviation row changes, with the rule ID and the package version in force; a failed write changes nothing, diverts nothing and answers MSG-P7-003 | DP-03; TSD S8 T2; legacy BR7 |
| BR3 | The handler queue code is read from the parameter `allocation.deviation.queue.code` at every placement; no queue code, no handler role and no state name is written in code | DP-06; RWB-E1-020 section 3; TSD S8 T3.2; BR-S8-004 |
| BR4 | The handler is the owner the fired rule names for the code, and a code outside X1 to X7 or a code with no owner follows R-DEV-21 and is recorded as unmapped | R-DEV-03 to R-DEV-06, R-DEV-21; FSD S8 A2.4.3.1; REQ-DVH-003 |
| BR5 | `deviation` is this service's: no `recovery_case`, `queue`, `queue_member`, `assignment` or `timer` row is read or written, and the case facts arrive on the P3 contract | Context pack ownership rows; TSD S8 T0.2; DP-01 |
| BR6 | ACE data is never read here: the party facts a screening needs are rwb-source-data's, and this slice reads no `v_ace_*` view and no ACE table | DP-05; TSD S8 T0.4 |
| BR7 | The placement is answered once per case and business date; a second presentation answers the recorded placement and counts the repeat | R-UNI-40; legacy BR8 |
| BR8 | One `DeviationRaised` per placement, published from the outbox in the transaction of the row, with identifiers, the code, the queue code and the rule version and no personal data | DP-09, DP-14; TSD S8 T5.2.1, T5.3 |
| BR9 | The service identity that runs the placement holds the Case record letters of TSD S8 T6.1 and a person needs Case record right U for the raise; a caller without it is refused 403 | TSD S8 T6.1, T6.2; legacy section 10 |

### 9. State transitions

The case state, its queue, its assignment and its two clocks are rwb-case's and this story does not change them: the step returns the placement and the parent applies it (BR5). This story owns the `deviation.state` of the record it writes, over the 9 DEVIATION states of TSD S8 T4.

| From (`deviation.state`) | Event | Condition | To |
|---|---|---|---|
| No row | - | The case has no open deviation | Unchanged; the answer is NO_DEVIATION and nothing is written (AC4) |
| DEV_FLAGGED | DEVIATION_FLAGGED | The open code is X1 to X7 | DEV_FLAGGED on R-DEV-01 |
| DEV_FLAGGED | OWNER_ASSIGNED | The code rule names an owner: X2 or X3 (R-DEV-03), X4 (R-DEV-04), X5 (R-DEV-05), X6 or X7 (R-DEV-06) | DEV_WITH_OWNER |
| DEV_FLAGGED | OWNER_ASSIGNED | The code is outside X1 to X7, or no owner is set for it | DEV_WITH_OWNER with the team manager and the code recorded as unmapped (R-DEV-21) |
| DEV_WITH_OWNER | OWNER_ASSIGNED | A handler is already set | Unchanged; the existing handler is answered and nothing is rewritten (X5) |

| Step execution | Event | Condition | To |
|---|---|---|---|
| Waiting | The parent presents a case for a business date | The DEV package version in force is loaded | Evaluating |
| Evaluating | R-DEV-01 and one code rule fire | The parameter and the handler candidates are available | Applying |
| Applying | The decision record, the row update and the outbox row commit | The transaction commits | Answered, placement returned to the parent |
| Applying | The record write or the transaction fails | X1, X2 | Waiting, nothing changed, MSG-P7-003 or MSG-P3-027 |
| Answered | The same case and business date arrive again | X7 | Unchanged, the recorded placement is answered and the repeat is counted |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Hardship and vulnerability specialist (RW-SPECIAL) | Holds RU on the case record (TSD S8 T6.1) and is the handler R-DEV-03 names for X2 and X3 |
| Fraud investigator (RW-FRAUD) | Holds RU and is the handler R-DEV-04 names for X4 |
| Legal counsel (RW-LEGAL) | Holds R, joins X3 for the estate claim on R-DEV-03 and is the handler R-DEV-05 names for X5 |
| Complaint officer (RW-COMPLAIN) | Holds RU and is the X1 handler of R-DEV-02, which stays with RWB-S8-E7001-APP |
| Case owner (RW-CASEOWN) | Holds CRU and is the "case owner" whose team manager R-DEV-21 names, and the owner the agent works with on R-DEV-06 |
| Team manager (RW-TEAMMGR) | Holds R, receives the X3, X4, X5, X6, X7 and unmapped placements as the named owner where the rule names a team, and reads SCR-08 |
| SY-CASEWF, case workflow module | Presents the case as the parent workflow and applies the placement; it writes no deviation row |
| SY-RULES, rules component | Evaluates the DEV package version in force and returns the rule ID with its output (R-DEV-01, R-DEV-03 to R-DEV-06, R-DEV-21) |
| rwb-access (P4) | Owns the roles and the rights of TSD S8 T6.1 that the guard checks; the rwb-access authorise check is Not specified in the source documents (DOR-RWB-S8-E1020-APP-6) |
| rwb-decision (P7) | Owns the DEV package, its rows and their versions, and the central ledger; this service only evaluates and records |

No delegated authority limit applies: a placement takes no credit decision and approves nothing, and the only approval in the module is the insurance claim of X3, which is not this story's. The database login is per service (DP-02) and its name is Not specified in the source documents (GAP-3073; ASM-5233).

### 11. Data

| BR Field ID | Table | Owner | Use in this story |
|---|---|---|---|
| DF-CAS-036 to DF-CAS-045 | `deviation` | S8, `rwb_deviation` | **Write**: `handler_user_id` and the standard `state` and `version` columns on a placement; the row itself is created by the raise stories |
| DF-CAS-038, DF-CAS-041, DF-CAS-043 | `deviation` | S8, `rwb_deviation` | **Read**: the code, the paused state and the contact stop of the open deviation the placement is about |
| None: library table | Not specified in the source documents (DOR-RWB-S8-E1020-APP-7) | Platform library in `rwb_deviation` | The hash-linked record written before the row (DP-03) |
| None: library table | `outbox_event`, `idempotency_key`, `processed_event` | Platform library in `rwb_deviation` | The `DeviationRaised` row, the placement key with its answer and the inbox of the parent's presentation |
| DF-CAS-001 to DF-CAS-023 | `recovery_case` | P3 rwb-case | The case reference, product group, region, exposure band and status; consumed on the workflow boundary, never written |
| DF-WRK-001 to DF-WRK-016 | `queue`, `queue_member`, `assignment` | P3 rwb-case | The handler queue, its members and the case owner whose team manager R-DEV-21 names; read on the owner's contract, never written |
| DF-REF-001 to DF-REF-015 | `rule_row` | P7 rwb-decision | The DEV package rows and their versions; read through the package, never written |
| DF-DEC-001 to DF-DEC-018 | `decision_log_entry` | P7 rwb-decision | The central ledger; the record of DP-03 is copied to it by rwb-decision, not written here |

The placement writes no new column: the handler queue is not a column of `deviation` (TSD S8 T3.1), because the queue belongs to the case and to the parameter, and the row carries only the handler and the state (`handler_user_id`, `state`). The codes and the lists are the LOV-DEVIATION, LOV-RAISED-BY and LOV-DEV-OUTCOME values of TSD S8 T3.2, read at their version through DP-07. No personal value enters `rwb_deviation`, the record, the event or a log: `case_id` and `handler_user_id` are references to other services' facts, and no customer name, contact value or address is copied.

### 12. Contract

#### 12.1 REST operations provided

None new in this story. The two operations the Ownership Map gives rwb-deviation stay exactly as the service baseline publishes them on base `/api/recovery/deviation/v1` (DP-13), and this story adds no path, no element and no status:

| ID | Method | Path | What this story decides behind it |
|---|---|---|---|
| API-S8-001 | POST | `/cases/{caseId}/deviations` | The handler queue code and the handler of a raise for the codes X2 to X7 and for an unmapped code, through the same engine the parent calls; the X1 raise stays RWB-S8-E7001-APP's. Case record U, `Idempotency-Key` |
| API-S8-002 | PATCH | `/deviations/{deviationId}` | Nothing: the outcome path is RWB-S8-E7001-APP's and the other code stories'. Case record U |

Both keep the error set 401, 403 with MSG-P4-002, 404, 409, 422 and 503 of TSD S8 T-A.2, each in the platform problem envelope. The morning entry of the allocation is not a REST call: rwb-case starts the child workflow (12.5), because the S8 row of the connection matrix names Temporal and events to P3 and never REST (ASM-5230).

#### 12.2 REST operations consumed

None for this slice. The case and its open deviation arrive on the Temporal boundary defined by `RWB-P3-E1020-CON`, and the queue and its members travel in the same element, so no hop is added and the one-hop 2 s rule of DP-11 is untouched. The element names of the case input and of the stage outcome are Not specified in the source documents (GAP-3072; ASM-5230). The P1 party-flag read and the P10 agent run of TSD S8 T5.2.2 are the screening stories' and are not consumed here.

#### 12.3 Events published

| Event | Topic | Data | Consumers |
|---|---|---|---|
| `DeviationRaised` (EV-06, `rwb.deviation.DeviationRaised.v1`) | `rwb.deviation.events.v1` | Case reference, deviation reference, code, raised-at, the queue code, the rule ID and version; CloudEvents 1.0, key `caseId`; no personal data | rwb-case, rwb-comms, rwb-treatment (TSD S8 T5.2.1) |
| `DecisionRecorded` (EV-08, `rwb.decision.DecisionRecorded.v1`) | `rwb.decision-record.v1` | The placement record of DP-03, relayed by the library | rwb-decision, for the central ledger (DP-03) |

`DeviationCleared` (EV-07) is not published by this story: nothing is cleared at a placement, and the clear path is RWB-S8-E7001-APP's. The pairing of the id EV-06 with the name `DeviationRaised` is taken from TSD S8 T0.2 and T5.2.1 (ASM-5234).

#### 12.4 Events consumed

None. The case is presented by its parent as a child workflow, not as an event, so this slice subscribes to nothing; the `CaseCreated` (EV-01), `AceDataReady` (EV-26) and `AgentRunCompleted` (EV-28) subscriptions of TSD S8 T5.2.2 belong to the screening and agent-run stories of this service.

#### 12.5 Workflows and activities

| Name | Type | Queue | Element |
|---|---|---|---|
| `DeviationWorkflow` | Workflow, one execution per case, started by rwb-case as the child of `CaseWorkflow`, parent close policy ABANDON, continues-as-new; workflow ID form and duplicate-start policy are Not specified in the source documents (CG-ALL-11264) | `rwb-deviation` in namespace `rwb-recovery` | Hosts the handler-placement branch; its input carries the case element of `RWB-P3-E1020-CON` and its result is the stage outcome the parent applies |
| `evaluateHandlerRules` | Activity, the EvaluateRules step | `rwb-deviation` | The case, the open deviation and the business date in; the rule ID, the package version, the queue code and the handler out |
| `recordAndApplyPlacement` | Activity, the RecordAndApply step | `rwb-deviation` | The decision in; the decision record, the row update, the outbox row and the stage outcome out, one transaction |

The stage outcome carries the case reference, the deviation reference, the queue code, the handler reference, the rule IDs with their versions and PLACE_DEVIATION_QUEUE or NO_DEVIATION; the parent places the case and pauses its own clock (ASM-5230). The names of the outcome element and of its fields are Not specified in the source documents (GAP-3072; ASM-5230).

#### 12.6 Schedules

None. The Ownership Map gives S8 no job, and the morning allocation stays JOB-03 of rwb-case: this story starts no Schedule, reads no Quartz row and declares no batch table (context pack ownership rows; DP-10).

#### 12.7 Tables owned

| Table | Owner | Use |
|---|---|---|
| `deviation` | S8, `rwb_deviation` | The open deviation the placement is about, its handler and its state |
| `decision_record` | Platform library in `rwb_deviation` | The record written before the row (DP-03) |
| `idempotency_key` | Platform library in `rwb_deviation` | The placement key of the case and the business date, with its answer |
| `outbox_event` | Platform library in `rwb_deviation` | The `DeviationRaised` and `DecisionRecorded` rows relayed to their topics |
| `processed_event` | Platform library in `rwb_deviation` | The inbox of the parent's presentation |

`recovery_case`, `queue`, `queue_member`, `assignment`, `timer`, `rule_row`, `decision_log_entry` and every `v_ace_*` view are other owners' and are named only; no foreign key leaves `rwb_deviation` (DP-01).

#### 12.8 Contract fakes

| Fake | Answer | Used by |
|---|---|---|
| rwb-case allocation fake (`RWB-P3-E1020-CON`) | A NEW case with an open deviation of code X3; the same case with no open deviation; four cases of codes X2, X4, X5 and X6; an unmapped code; a case already in DEV_WITH_OWNER; no answer inside 2 s | AC1 to AC7 |
| rwb-case queue and members fake | The queue "DEV-HANDLER" with its members and their role codes; a queue the contract does not list | AC1, AC3 |
| rwb-case parameters fake (`RWB-P3-E1042-CON`, DP-06) | `allocation.deviation.queue.code` = "DEV-HANDLER"; the value "DEV-HANDLER-2"; no value | AC1, AC3 |
| rwb-case reference-data fake (`RWB-P3-E1043-CON`, DP-07) | LOV-DEVIATION, LOV-RAISED-BY and LOV-DEV-OUTCOME at their version | AC1, AC2 |
| rwb-decision package fake (`RWB-P7-E1073-CON`) | The DEV package at its version with the six rules of section 8; no version in force | AC1, AC5 |
| Local decision-record stub (`RWB-PLT-E1027-CON`) | A healthy chain and a stopped chain | AC5 |
| Outbox relay stub (`RWB-PLT-TE006-CON`) | A relayed `DeviationRaised`; a relay that fails and retries | AC1, AC7 |
| gateway-bff composite route fake (`RWB-PLT-N001-CON`) | The merged SCR-08 and SCR-02 answer for a synthetic case | AC1, AC4 |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | None | No operation is provided new and none is consumed by this slice; the two published operations keep their contract and the placement is answered on the workflow boundary |
| Kafka | 1 published service event and 1 decision record; 0 consumed | `DeviationRaised` on `rwb.deviation.events.v1`; `DecisionRecorded` on `rwb.decision-record.v1` from the library |
| Temporal | 1 workflow and 2 activities | `DeviationWorkflow` with `evaluateHandlerRules` and `recordAndApplyPlacement` on `rwb-deviation`; no Schedule |
| File | None | No file is read, built or delivered by this story |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.deviation`, module `deviation/handler-placement`, Java package `th.co.scb.ace.workbench.recovery.deviation.placement`.

**Pattern application** (R5.5)

| DP | Legacy marker | Pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_deviation`; never read another service's tables | None |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision | H RWB-PLT-E1072-CON; C RWB-P7-E1073-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | None |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | None |
| DP-13 | `/api/recovery/v1` | `/api/recovery/deviation/v1` | None |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.deviation.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in `rwb_deviation` | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

What each DP means for this slice:

- DP-01 is the reason the queue, the members and the case facts arrive on the P3 contract: `recovery_case`, `queue`, `queue_member` and `assignment` are P3's and no statement of this story names them.
- DP-03 is the placement record: the deviation's decision is written before the row and before the event, in the same transaction.
- DP-04 is the DEV package: the rule rows and their version are governed in rwb-decision and evaluated here by the service's own kit, which is why the kit row and the P7 registry row appear here and not in the metadata, whose C row carries `RWB-P3-E1020-CON` alone (GAP-3073; ASM-5233).
- DP-05 is recorded because the legacy key reads ACE data (`v_ace_batch_status`) for its batch gate: the gate is P1's in the target and the case arrives from a run that has already passed it, so this service reads no view.
- DP-06 is the handler queue code and DP-07 the three lists; both are read on the P3 contracts with their version, and a new value moves the case with no deployment.
- DP-09 and DP-14 are the single event of the placement on the one topic of the service, with the retry and `.dlt` topics of the naming rule.
- DP-10 is the workflow kit behind the child and DP-11 the one-hop rule that keeps the boundary a Temporal call rather than a second REST hop.
- DP-13 moves the base of the two operations, DP-15 puts the one migration in the `rwb_deviation` sequence, and DP-19 puts SCR-08 and SCR-02 behind the composite route.
- DP-02 and DP-08 are the service's own patterns in TSD S8 T0.3 and are already in place at the baseline; the plan's pattern set for this key does not carry them (ASM-5233).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| DeviationWorkflow (placement branch) | Workflow | Receives the case from the parent, runs the two activities and returns the stage outcome |
| HandlerQueueRule | Service | Reads `allocation.deviation.queue.code` and answers the queue code of a placement, with no value in code |
| HandlerAssignmentEngine | Service | Applies the fired code rule, reads the queue members on the P3 contract and picks the handler with the fewest open deviations |
| OpenDeviationQuery | Service | Reads the case's open deviation from `deviation` and answers NONE, OPEN or ALREADY_ASSIGNED |
| PlacementRecordWriter | Service | Writes the decision record, the row update and the two outbox rows in one transaction (DP-03, DP-09) |
| HandlerPlacementRepository | Repository | `deviation`, the decision record, the outbox, the inbox and the idempotency key in `rwb_deviation`; no foreign table |
| PlacementController | Controller | The placement element of the two published operations, behind the service's DeviationHandlingController; validation and problem responses |

**Database and migrations.** One migration in the per-service Flyway sequence of DP-15: `V1020_1__placement_indexes.sql` adds `ix_deviation_case_state` on `deviation (case_id, state)` and `ix_deviation_handler_state` on `deviation (handler_user_id, state)`, so the open-deviation read and the handler load are index reads. No column is added: the queue code is not a column of `deviation`, and no business value is written in the migration.

**Configuration and reference data.** The parameter `allocation.deviation.queue.code` through DP-06 and the three lists through DP-07; the queues and their members from P3; the DEV package version from P7. The value "DEV-HANDLER" is the DL23 assumed value and lives in the parameter row, never in the code (ASM-5232).

**Build steps.** (1) Wire the placement branch of `DeviationWorkflow` and the two activities on `rwb-deviation`. (2) `OpenDeviationQuery` against `deviation`, with the four answers. (3) `HandlerQueueRule` over the parameters contract and `HandlerAssignmentEngine` over the members of the P3 contract and the open-deviation count. (4) `PlacementRecordWriter` with the record first, the row update, the two outbox rows and the idempotency key in one transaction. (5) The stage outcome and its PLACE_DEVIATION_QUEUE and NO_DEVIATION values. (6) The placement element of the two published operations. (7) The migration and its index tests. (8) Prove AC1 to AC7 on the fakes.

**Feature flag.** `rwb.s8.handler-placement`. Off: a presentation answers NO_DEVIATION and the case is allocated by the rules of rwb-case as if this service had not been called; no row, no record and no event are written. It needs no schema rollback and blocks no raise.

**Done when.** AC1 to AC12 pass at component level on the fakes; a placement writes one record, one row update and one event; a forced record failure leaves nothing changed; a repeat writes nothing; the boundary test shows no `v_ace_*` read and no statement against another service's schema; and SCR-08 answers through the gateway-bff route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P7-003 | The decision record cannot be written before the change (X1) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P3-027 | No DEV package version is in force at the presentation (X2) | The {table} load was refused: {check}. The version in force is unchanged. |
| MSG-P4-002 | A caller without Case record right U raises a deviation (BR9) | You cannot {action} here. Your role does not include it. |
| MSG-P1-001 | The data product behind the case facts is stale (VR-S8-004-1) | {product} is from {date}. Today's load has not arrived. |

The four messages are copied from the legacy, FSD S8 or Error and Message Standard v4 wording; the placement itself adds no new message, and the overflow, exception and deviation counts of the morning summary stay with the allocation's own MSG-P3-011 and MSG-P3-012 in rwb-case. The Thai text follows DL10, which is still open and carries assumptions ASM-2250, ASM-2357, ASM-2377 and ASM-2863. Open decision DL23 is still open and carries assumptions ASM-1232, ASM-1237, ASM-1259 and ASM-1560.

### 15. Screens and states

| Screen | States | What this story answers |
|---|---|---|
| SCR-08 Deviation queue | Loading; list; Empty: Not specified in the source documents (CG-ALL-11276); Error: Not specified in the source documents (CG-ALL-11276); No access: Not specified in the source documents (CG-ALL-11276) | The open deviations by type, handler and age, with the handler this story assigned and the code the DEV package names |
| SCR-02 Case list | Empty; Loading; list; Error: Not specified in the source documents (CG-ALL-11275); No access: Not specified in the source documents (CG-ALL-11275) | The queue and the owner column of a diverted case: the queue "DEV-HANDLER" and no owner, which is the placement answer rendered |

Both screens are the edge contract's (DP-19) and the composite route also calls rwb-case for the case, its owner and its timers; this story fixes only its own answers and builds no screen of its own. The saved, refused, not-recorded and stale-data states read the messages of section 14 on the same route.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-020-14 | BR9: the right on the two operations is unchanged, and the morning placement runs as the service identity, so a role without Case record U is refused and nothing runs | Component | RW-CASEOWN asks for the raise of a deviation; the automated placement runs as the service identity; 403 MSG-P4-002 for the caller |
| TC-E1-020-01 | owned by RWB-P3-E1020-APP (the queue a new case is placed in) | Component | One case per product group and region; the case side's data |
| TC-E1-020-15 | AC5, BR2: the decision record failure leaves no handler, no state move, no event and no diversion | NFR | The record write forced to fail for the placement and for the raise of a deviation; MSG-P7-003; nothing changed |
| TC-E1-020-08 | owned by RWB-P3-E1020-APP (a repeated run for the same business date) | Component | The same run repeated for 2026-12-01; the case side's data |
| TC-E1-020-02 | owned by RWB-P3-E1020-APP (the owner chosen by the assignment rule) | Component | Three owners with 120, 95 and 140 open cases; the case side's data |
| TC-E1-020-03 | owned by RWB-P3-E1020-APP (an owner at the cap is skipped) | Component | The next owner at 150 open cases; the case side's data |
| TC-E1-020-04 | owned by RWB-P3-E1020-APP (every owner at the cap, overflow) | Component | Every owner at 150 open cases; the case side's data |
| TC-E1-020-05 | owned by RWB-P3-E1020-APP (no allocation rule matched) | Component | Product group SSME and region NE3 with no rule; the case side's data |
| TC-E1-020-06 | AC1, AC2, BR2: one decision record per placement, naming the rule and the package version, and one `DeviationRaised` | Component | Case `RW-2026-000206` with code X3; the row in DEV_WITH_OWNER; one record with `R-DEV-03` and the version; one event |
| TC-E1-020-07 | AC1, AC2, AC3, AC6: a case with an open deviation goes to the handler queue with its handler and no case owner; the case-side half is RWB-P3-E1020-APP's | Component | Cases with `deviation_open` true for X2, X3, X4, X5, X6 and an unmapped code; the queue "DEV-HANDLER"; the parameter at "DEV-HANDLER" and at "DEV-HANDLER-2" |
| TC-E1-020-09 | owned by RWB-P3-E1020-APP (a run with no new cases) | Component | No case with status NEW on 2026-12-01; the case side's data |
| TC-E1-020-10 | owned by RWB-P3-E1020-APP (the run waits for case creation) | Component | JOB-02 not complete for the business date; the case side's data |
| TC-E1-020-11 | owned by RWB-P3-E1020-APP (two runs at once allocate each case once) | Component | Two workers on the same case; the case side's data |
| TC-E1-020-12 | owned by RWB-P3-E1020-APP (an owner one case below the cap) | Component | The next owner at 149 open cases; the case side's data |
| TC-E1-020-13 | owned by RWB-P3-E1020-APP (a queue with no overflow queue) | Component | Queue HP-CEN-CO with no overflow queue and every owner at 150; the case side's data |
| TC-E1-020-16 | AC4 (section 7) | Component | Case `RW-2026-000210` with status NEW and no open deviation; business date 2026-12-01 |
| TC-E1-020-17 | AC7 (section 7) | Component | Case `RW-2026-000206` presented and diverted for 2026-12-01, then presented again for the same date |
| TC-E1-020-18 | Contract test of the operations, events and activities of section 12 | Contract | Not specified in the source documents (DOR-RWB-S8-E1020-APP-12) |
| TC-E1-020-19 | AC8 (section 7): boundary test of the tables of section 12.7; no read of `v_ace_*` or `rwb_case` | Component | Not specified in the source documents (DOR-RWB-S8-E1020-APP-12) |
| TC-E1-020-20 | AC9 (section 7): error answers 401, 403 and 404 of the two operations | Component | Not specified in the source documents (NEWAC-RWB-S8-E1020-APP-AC10) |
| TC-E1-020-21 | AC10 (section 7): replay of a write with the same idempotency key | Component | Not specified in the source documents (NEWAC-RWB-S8-E1020-APP-AC11) |
| TC-E1-020-22 | AC11 (section 7): retried or timed-out activity | Component | Not specified in the source documents (NEWAC-RWB-S8-E1020-APP-AC12) |
| TC-E1-020-23 | AC12 (section 7): status change the model does not allow is refused | Component | Not specified in the source documents (NEWAC-RWB-S8-E1020-APP-AC13) |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. Every legacy test case of the key is listed so that the key's test set is not lost: the four this slice answers are re-pointed to the criteria it owns — TC-E1-020-07 to the diversion and the handler of AC1, AC2, AC3 and AC6, TC-E1-020-06 to the record and the event of AC1 and AC2, TC-E1-020-14 to the right of BR9, and TC-E1-020-15 to the record failure of AC5 — and the eleven that test the allocation, its caps and its queues stay with RWB-P3-E1020-APP. The legacy levels map as the Template and Rules require: System to Component because the case side is stubbed by `RWB-P3-E1020-CON`, Access to Component, Resilience to NFR. The `-ITG` copy of the diversion is TC-E1-020-07-ITG in RWB-ITG-E1020-ITG; no `-ITG` copy sits in this story.

### 17. Guardrails

- No business value in code: the deviation codes, the handler roles, the state names and the handler queue code are rule rows, list values or parameter rows read at their version (BR3, BR4).
- No personal data in the row, the decision record, an event, a workflow input, a log or a prompt: case and handler references, codes, instants and a rule version only (NFR-039, NFR-040).
- ACE data only through the owner's contract: no `v_ace_*` view, no ACE table, no other service's schema and no copy of a party flag (DP-01, DP-05).
- One base, one topic, one queue and one login per service; this story adds no second topic and no Schedule (DP-13, DP-14, DP-10).
- The decision record is written before the change and in its transaction; a failure rolls the row back and diverts nothing (DP-03).
- The placement is idempotent per case and business date, and the repeat counter is the only effect of a second presentation (BR7).
- The queue, the members and the caps stay with rwb-case: this story answers a queue code and a handler and never moves a case, assigns a case owner or pauses a clock itself (BR5).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CWC-007 | Every new case placed in a queue and assigned by rule | Business Requirements Epic 1, section 3.3; Program, section 5.3 | FEAT-CWC-07 | 18.3.2 Allocate work to teams, people and partners by rule | BR1, BR4 | TC-E1-020-07, and the allocation side in RWB-P3-E1020-APP |
| REQ-CWC-008 | Allocation rules apply first match and always have a default | Business Requirements Epic 1, section 3.3; Program, section 5.3 | FEAT-CWC-07, FEAT-CWC-09 | 18.3.2 | BR3, BR4 | TC-E1-020-06, TC-E1-020-07 |
| REQ-CWC-009 | Round robin, lowest load, named owner, cap and overflow | Business Requirements Epic 1, section 3.3; Program, section 5.3 | FEAT-CWC-08 | 18.3.2 | BR4 | TC-E1-020-07, and the caps in RWB-P3-E1020-APP |
| REQ-CWC-016 | Every allocation logged with rule ID and version | Business Requirements Epic 1, section 3.3; Program, section 5.3 | FEAT-CWC-07 | 6.1 Take over the case at 90 days past due | BR2, BR8 | TC-E1-020-06, TC-E1-020-15 |

| Legacy | Story | Test |
|---|---|---|
| RWB-E1-020 AC7 (a case with an open deviation goes to the deviation handler queue with no case owner) | Not copied here; owned by RWB-P3-E1020-APP. This story builds the deviation half: AC1, AC2, AC3 and AC6 | TC-E1-020-07, TC-E1-020-06 |
| RWB-E1-020 section 5 X4 | AC1, X4 | TC-E1-020-07 |
| RWB-E1-020 BR7 and TC-E1-020-15 (a decision that cannot be recorded does not proceed) | AC5 | TC-E1-020-15 |
| RWB-E1-020 section 10 (the rights of the run and of the handlers) | BR9, section 10 | TC-E1-020-14 |

| Source | What it supplies |
|---|---|
| REQ-DVH-003 and FSD S8 A2.4 (route the deviation to the named owner), A1.4, Screens | The handler routing of each code, the unmapped-code path, the roles and SCR-06 and SCR-08 |
| TSD S8 T0.1, T0.2, T0.3, T0.4, T2, T3.1, T3.2, T4, T5.2.1, T5.2.2, T5.3, T6.1, T-A.1 | The service identity, the one owned table and its columns, the DEV decision-first rule, the 9 states, the two events, the consumed rows, the rights and the two operations |
| Business Rules and Routing Logic v4, DEV route set | R-DEV-01, R-DEV-03 to R-DEV-06 and R-DEV-21 |
| Context pack S8 and the connection matrix | The schema, base, topic, queue, the two operations, the one table, the one workflow and the Temporal and event rows to P3 |
| Split plan, slice RWB-S8-E1020-APP | H, C, I, X, the lane, the wave and the release (GAP-3072, GAP-3073) |

### 19. Out of scope

- The allocation and assignment engine itself: package ALLOCATION and package ASSIGNMENT, JOB-03, the round-robin cursor, the caseload caps, the overflow queue, the exception queue, the allocation summary, the allocation's decision-log entry and the `CaseAllocated` and `CaseAllocationFailed` events (RWB-P3-E1020-APP).
- The rule registry, the version lifecycle, the dry run, the approval and the Drools evaluation of the packages as a governed artefact (RWB-P7-E1020-APP); this story only evaluates the DEV package it is given.
- The X1 raise and outcome journey and the other code flows: the complaint evidence pack, the hardship decision, the deceased estate and insurance claim, the fraud referral, the bankruptcy claim, the skip trace, the collateral event, the contact stop and the outcome entry (RWB-S8-E7001-APP and the X2 to X7 stories of this service).
- The case of record, its route state, its queue, its assignment, its caps and its two clocks (rwb-case, P3); the roles and the rights (rwb-access, P4); the party flags and the customer facts (rwb-source-data, P1); the evidence pack (rwb-document, P5); the notices (rwb-comms, P6).
- The screening agent at L1 and its low-confidence review (FEAT-DVH-07, FEAT-DVH-08), two deviations on one case (FEAT-DVH-09) and the override review (FEAT-DVF-08).
- The integration harness copy of the key, RWB-ITG-E1020-ITG, which proves the diversion end to end across the four services.
- The schema and migration of `rwb_deviation`, the login, the deployment, the observability and the pipeline (the DB, INF and OPS stories of this legacy key).
- Any change to a legacy file, to a master or to built Epic 1 and Epic 2 code.
