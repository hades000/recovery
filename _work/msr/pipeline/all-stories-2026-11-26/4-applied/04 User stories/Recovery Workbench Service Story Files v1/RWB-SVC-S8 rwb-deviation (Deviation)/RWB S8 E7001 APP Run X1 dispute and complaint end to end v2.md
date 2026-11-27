# RWB-S8-E7001-APP Run X1 dispute and complaint end to end

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S8-E7001-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-deviation |
| Service epic | RWB-SVC-S8 |
| Wave | 4 |
| Business epic | EP07 |
| Release | 31 May 2027 (tentative) |
| Legacy key | RWB-E7-001 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | L-S8-L |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S8-E7001-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S8 rwb-deviation v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the application slice of RWB-E7-001 is realigned onto rwb-deviation (S8, service wave 2, business wave 4). The legacy criterion this slice owns is kept word for word with its origin tag and only the `Given the <service> contract mock returns <x>` lines are added. X1 is built as the always-on child of `CaseWorkflow` on task queue `rwb-deviation`: it evaluates R-DEV-01, R-DEV-02, R-DEV-09, R-DEV-18, R-DEV-19, R-DEV-20 and R-DEV-22 with the DEV package in force, writes the `deviation` row in `rwb_deviation`, records the decision through the local decision-record library before the row changes (DP-03), publishes `DeviationRaised` and `DeviationCleared` from the outbox, and answers the case move to the parent. The two operations move onto `/api/recovery/deviation/v1` (DP-13) and the two screens are reached through the gateway-bff composite route (DP-19). The event ids are published as EV-06 and EV-07 with no names, the plan's C row is empty although the evidence pack is P5's, and the X1 complaint service level is set with DL22 (GAP-3051; ASM-5134 to ASM-5141). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-S8-E7001-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **complaint officer (RW-COMPLAIN)**, I want **to take the dispute from detection through the evidence pack to resolution and the return point, with the decision recorded and the stage clock paused, so that every deviation has a handler and a clock**.

This story owns:

- the one legacy criterion of RWB-E7-001 that the plan assigns to this slice (AC2, verbatim with its origin tag), and the rules, messages and screens it depends on;
- the X1 branch of `DeviationWorkflow` on task queue `rwb-deviation` in namespace `rwb-recovery`, started by the case router at any time as the child of `CaseWorkflow` (Architecture v5 slides 3 and 13; Temporal and Drools Design slide 13);
- the evaluation of R-DEV-01, R-DEV-02, R-DEV-07, R-DEV-08, R-DEV-09, R-DEV-18, R-DEV-19 and R-DEV-20 on an X1 of a case, with the DEV package version in force;
- the `deviation` row in schema `rwb_deviation` with the columns of DF-CAS-036 to DF-CAS-045, its `state` and its `contact_stop`;
- the decision record of the flag, the assignment and the outcome, written through the local decision-record library **before** the row changes (DP-03);
- the publication of `DeviationRaised` and `DeviationCleared` on `rwb.deviation.events.v1` from the outbox;
- the stage outcome returned to rwb-case, carrying the rule ID, its version and the return point, on which the parent pauses and resumes the stage clock;
- the two operations on base `/api/recovery/deviation/v1` (DP-13) and the read-only slices of SCR-06 and SCR-08 behind the gateway-bff composite route (DP-19).

It does not own: the published shapes, the `deviation` element, the two envelopes, the error set and the fakes (RWB-S8-E7001-CON); the end-to-end journey of AC1 across the services and the wave 4 harness, which RWB-ITG-E7001-ITG owns (ASM-5141); the case of record, its route state, its assignment and its timers (rwb-case, P3); the evidence pack documents, their retention and the notices (rwb-document P5, rwb-comms P6); the DEV rule rows and their versions (rwb-decision, P7); the rights and the reference data (rwb-access P4); and the schema, migration and deployment of this service (the DB, INF and OPS stories of this key).

### 2. Business rationale

The objective and the metric do not move: deviations closed within the service level, measured on the decision log and the Workbench records, reviewed monthly (FSD S8 A2.10.1). The requirements are REQ-DVH-011, "The full deviation flows with their approvers, contact stops and return points run end to end", and REQ-S8-003, "A complaint is resolved inside its service level and the case returns to the same decision with its timers resumed" (FSD S8 Requirements served).

A complaint is the one deviation the bank cannot let drift: the stage clock must stop so the case is not counted late, the legal clock must keep running because the law does not pause, contact must stop, and the case must come back to the exact state it paused in (FSD S8 A2.1.1, A2.2.1, A2.3.1; Architecture v5 slide 3).

D-RCV-60 changes who owns each fact, not what the officer gets:

- **The deviation record is this service's.** `deviation` is written in `rwb_deviation` and is the one table the Ownership Map gives S8 (context pack, Ownership rows; TSD S8 T3.1). Its status is the `state` column, so the 9 DEVIATION states of TSD S8 T4 live here and not on the case.
- **The case stays with rwb-case (P3).** `recovery_case`, `queue`, `assignment` and `timer` are P3's; the S8 row of the connection matrix names Temporal and events to P3, so the stage clock is paused and resumed by the parent on the stage outcome and this story writes no case or timer row (Architecture v5 slide 13; ASM-5139).
- **The decision is recorded first**, in the same transaction as the deviation change: that is what TSD S8 T2 states and what legacy AC2 tests (DP-03).
- **The evidence pack stays with rwb-document (P5)** and the contact and customer facts with rwb-source-data (P1): the plan's C row is empty and the FSD names the Document hub as an integration point, so both reads are taken on the owner's contract with a fake and the gap is recorded (GAP-3051; ASM-5137, ASM-5138).
- **The event leaves from the outbox**, on the one topic of the service, with rwb-case, rwb-comms and rwb-reporting as its only listeners (context pack topic and connection matrix; ASM-5135, ASM-5136).

No business value moves: the deviation codes, the raised-by codes, the outcome codes, the escalation at 10 working days and the X1 complaint service level stay reference data or rule rows read with their version, never a constant of the code.

### 3. Preconditions

- RWB-S8-E7001-CON is published and tagged: the two operations on `/api/recovery/deviation/v1`, the `deviation` element, the three closed lists, the two envelopes, the consumed rows, the error set and the fakes are baselined and handed to this story.
- RWB-PLT-E1027-CON is published with its writer stub: the local decision-record library writes in the caller's transaction and a failed write stops the action with MSG-P7-003 (DP-03).
- RWB-PLT-N001-CON is published: SCR-06 and SCR-08 reach this service through the gateway-bff composite route, one hop each, and no screen calls a service directly (DP-19).
- `deviation` exists in `rwb_deviation` from the DB story of this service with the columns of DF-CAS-036 to DF-CAS-045 and the standard record columns of TSD S8 T3.0; this story adds no table, no column and no migration.
- The DEV rule package is in force at its version with R-DEV-01, R-DEV-02, R-DEV-07, R-DEV-08, R-DEV-09, R-DEV-18, R-DEV-19 and R-DEV-20; it is authored, tested and approved in rwb-decision (P7) and loaded here (FSD S8 A2.10.3.1; Business Rules and Routing Logic v4).
- The rwb-case workflow boundary is available for the fake: the case reference, its route state and its `paused_state` arrive as child-workflow input, and the outcome is the child result the parent applies. No source publishes a REST operation that moves a case state or pauses a timer on behalf of a stage (Architecture v5 slide 13; ASM-5139).
- The rwb-document contract of the evidence pack is published with its fake; its operation name is Not specified in the source documents (GAP-3051; ASM-5137). The rwb-source-data customer and contact facts are consumed the same way (ASM-5138).
- The data product the module reads carries today's business date, or shows its date as stale and holds the action (VR-S8-010-1; MSG-P1-001).
- The service runs as its own login on `rwb_deviation` and holds no grant on another `rwb_*` schema and no `v_ace_*` grant, so a statement on `rwb_case` or on a `recovery.v_ace_*` view is refused by the database and fails the boundary test (DP-01, DP-05).
- No approval is needed to build against a Draft contract baseline; the contract is tagged by RWB-S8-E7001-CON when its tests pass.

### 4. Flow

1. X1 arrives on a case from one of three places: the screening agent of E2, an officer on SCR-06 Raise deviation, or a self-service dispute the customer raises through rwb-comms (FEAT-COM-04). The caller sends `POST /cases/{caseId}/deviations` on `/api/recovery/deviation/v1` with `deviation_code` X1, `raised_by`, `paused_state` and the reason, one `Idempotency-Key` per raise (API-S8-001).
2. The handler signals the case's `DeviationWorkflow` on queue `rwb-deviation`; it never writes a table or a case row on the request thread.
3. `evaluateDeviationRules` loads the DEV package version in force and evaluates R-DEV-01 on the case: `deviation_code in (X1..X7)`, so the deviation is flagged, the stage clock is paused, the prescription clock keeps running and the deviation routes to its named owner. R-DEV-02 then assigns X1 to the complaint officer.
4. `recordAndApplyDeviation` writes one decision record through the local library **before any change**: case reference, deviation reference, rule ID with the package version, inputs reference, the outcome and the decided-at time (DP-03; TSD S8 T2).
5. In the same `rwb_deviation` transaction the activity inserts the `deviation` row: `id`, `case_id`, `deviation_code` X1 of `LOV-DEVIATION`, `raised_at`, `raised_by` of `LOV-RAISED-BY`, `paused_state` (the routing state the case was in), `handler_user_id` the complaint officer, `contact_stop` true because X1 is one of X1 to X3 (REQ-DVH-004), `cleared_at` and `outcome` empty, and `state` = DEV_WITH_OWNER after the R-DEV-02 move.
6. The outbox publishes `DeviationRaised` on `rwb.deviation.events.v1` in that transaction, with identifiers, the code, the raised-at instant, the contact-stop flag and the rule version, and no personal data.
7. The step returns the stage outcome to the parent: the deviation reference, the return point, the rule IDs with their versions and `CLOCK_PAUSE`. rwb-case pauses the stage timer and moves the case; the prescription timer is not touched, which is the one-clock rule of R-DEV-01 (Architecture v5 slide 8).
8. The complaint officer works the dispute on SCR-08 Deviation queue and the case record: the complaint facts, the preceding contact and the evidence pack, which is read from rwb-document on its contract, one hop and 2 s (ASM-5137).
9. The officer records the outcome with `PATCH /deviations/{deviationId}` and a `DeviationOutcome` of `LOV-DEV-OUTCOME`: RETURNED, RE_ROUTED or CASE_ENDED (API-S8-002).
10. R-DEV-09 records the outcome and resumes the same decision; R-DEV-18 resumes the stage clock and returns the case to `paused_state`; the contact stop is lifted, `cleared_at` and `outcome` are written, `state` becomes RESUMED, and `DeviationCleared` is published from the same transaction.
11. Where the outcome changes the route, R-DEV-19 reopens the route decision D6 in rwb-valuation with the segment recomputed and the hard gates re-run; where the officer marks the flag as not a deviation, R-DEV-07 clears it with the reason and R-DEV-08 returns the case, and the same `DeviationCleared` is published.
12. Beyond the deviation service level in DEV_WITH_OWNER, R-DEV-20 escalates to the team manager and reports the breach at 10 working days; the X1 complaint service level itself is the value set with DL22, which no source publishes (GAP-3051; ASM-5140).
13. A repeated raise with the same case, code and `Idempotency-Key` answers the record it already wrote, writes nothing, publishes no second event and counts the repeat.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The local decision record cannot be written | Nothing changes: no `deviation` row, no event and no stage outcome leaves the service, and the case does not pause | MSG-P7-003 | AC2, TC-E7-001-02, TC-E7-001-04 |
| X2 | The role lacks the Case record right of the raise or of the outcome | 403 before any change and before any decision record | MSG-P4-002 | AC2, TC-E7-001-03 |
| X3 | A required value is absent or invalid: the code, the raised-by, the paused state or the outcome | The request is refused with the field named and nothing is written | MSG-GEN-001 | AC2 |
| X4 | The data product behind the case facts is stale after a late or failed ACE batch | The step holds, writes nothing and shows the product and its date | MSG-P1-001 | AC2 |
| X5 | The rwb-document evidence-pack read does not answer inside 2 s or its breaker is open | The dispute stays open, the evidence pack shows as unavailable, no outcome is recorded and no second attempt is made inside the step | None (platform 503 envelope) | AC2 |
| X6 | An X1 is already open on the case | One open deviation per code and case: the repeat is counted, no second row and no second event | None | AC2 |
| X7 | The outcome names no next step | R-DEV-22 returns the case to the route decision within 2 working days and records that the outcome was not mapped | None | AC2 |
| X8 | A component, a statement or a test reaches a `v_ace_*` view, a `rwb_case` row or another service's schema | The grant refuses the statement and the boundary test fails the build | None (pipeline log) | Section 17, BR3, BR4 |

X1 to X3 are the paths RWB-E7-001 carries; X4 to X7 are the paths the target call types and the container adds; X8 is the DP-01 and DP-05 boundary.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-S8-E7001-CON, the decision-record stub, the gateway-bff fake, the rwb-case workflow fake and the document and data-product fakes, on its own schema, and needs no live P1, P3, P5 or P7 |
| Negotiable | The activity names, the decision code per rule and the shape of the stage outcome are this story's choice; the rules, the messages, the screens, the two operations and the `deviation` columns are fixed |
| Valuable | A dispute pauses the stage clock the day it is raised, has one named handler and one recorded decision, and returns the case to the state it paused in with the legal clock intact |
| Estimable | One workflow branch, three activities, two event publications, two operations, two screen fragments and the access and failure tests |
| Small | Finished inside two weeks with its tests on the fakes |
| Testable | Every path runs on synthetic cases through the contract fakes, plus the access refusal and the forced record-write failure |

### 7. Acceptance criteria

```gherkin
Feature: Run X1 dispute and complaint end to end

  Background:
    Given the DEV rule package is in force at its version and carries R-DEV-01, R-DEV-02, R-DEV-09 and R-DEV-18
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC2 Not recorded (legacy RWB-E7-001 AC2)
    Given the rwb-deviation contract mock returns deviation "DEV-2026-000701" of code "X1" on case "RW-2026-000701" in state "DEV_WITH_OWNER" with the complaint officer as handler
    Given the rwb-decision contract mock returns the decision log store unavailable for the entry of "DEV-2026-000701"
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

AC2 is the criterion of RWB-E7-001 word for word: `the decision log cannot be written`, `the action is taken`, `nothing changes` and `the user sees MSG-P7-003` all stand, and the only additions are the two mock lines that stand in for the contract this service publishes and for the decision log it does not own. On this story "the action" is either the raise through `POST /cases/{caseId}/deviations` or the outcome through `PATCH /deviations/{deviationId}`: both write the decision record first, so both change nothing when the record cannot be written, and neither leaves a deviation row, a contact stop, an event or a paused clock behind (DP-03).

AC1 of RWB-E7-001 is not copied here: the split plan gives this slice AC2 only and gives the happy path of X1 across the services to RWB-ITG-E7001-ITG, which carries it word for word with its `-ITG` test copies (ASM-5141). The case number and the deviation reference in the mock lines are synthetic test data and no source value (section 16).

### 8. Business rules

| Rule | Route set | Codes | From state | Event | Condition | Action | To state | Owner | Systems | Timer |
|---|---|---|---|---|---|---|---|---|---|---|
| R-DEV-01 | Deviations | X1 to X7 | ANY_STATE | DEVIATION_FLAGGED | deviation_code in (X1..X7) | Pause the stage clock, keep the prescription clock running, route to the named owner | DEV_FLAGGED | Workbench | Workbench, the Workbench document hub | same day |
| R-DEV-02 | Deviations | X1 to X7 | DEV_FLAGGED | OWNER_ASSIGNED | deviation_code = X1 | Assign to the complaint officer | DEV_WITH_OWNER | Complaint officer | Workbench | None |
| R-DEV-07 | Deviations | X1 to X7 | DEV_FLAGGED | FLAG_REJECTED | owner marks the flag as not a deviation | Clear the flag, record the reason, resume the clock | DEV_REJECTED | Workbench | Workbench | None |
| R-DEV-08 | Deviations | X1 to X7 | DEV_REJECTED | CLOCK_RESUMED | Any | Return the case to the state it paused in | RESUMED | Previous owner | Workbench | None |
| R-DEV-09 | Deviations | X1 to X7 | DEV_WITH_OWNER | DEVIATION_RESOLVED | deviation_code in (X1,X7) | Record the outcome; the same decision resumes | DEV_RESOLVED | Case owner | Workbench | None |
| R-DEV-18 | Deviations | X1 to X7 | DEV_RESOLVED | CLOCK_RESUMED | Any | Resume the stage clock and return the case | RESUMED | Previous owner | Workbench | None |
| R-DEV-19 | Deviations | X1 to X7 | DEV_REROUTE | ROUTE_REOPENED | Any | Recompute the segment and re-run the hard gates | ROUTE_D6 | Case owner | Workbench | None |
| R-DEV-20 | Deviations | X1 to X7 | DEV_WITH_OWNER | SLA_BREACHED | time in DEV_WITH_OWNER exceeds the deviation service level | Escalate to the team manager and report the breach | DEV_WITH_OWNER | Team manager | Workbench | 10 working days |
| R-DEV-22 | Deviations | X1 to X7 | DEV_WITH_OWNER | DEVIATION_RESOLVED | otherwise, the outcome does not name a next step | Return the case to the route decision and record that the outcome was not mapped | DEV_REROUTE | Case owner | Workbench | 2 working days |

The nine rows are the rows of Business Rules and Routing Logic v4, copied character for character. The owner column is a business role, not a service: the states are the `deviation.state` of this service, the route states of the case are rwb-case's, the DEV package and its versions are rwb-decision's and the documents behind R-DEV-01 are rwb-document's. R-DEV-03 to R-DEV-06 and R-DEV-10 to R-DEV-17 and R-DEV-21 belong to the other codes of this service and are not built here.

| ID | Rule | Source |
|---|---|---|
| BR1 | `deviation` is this service's: its code, raise facts, paused state, handler, contact stop, outcome and state are columns of `deviation` in `rwb_deviation`, and no other service writes them | Context pack ownership rows; TSD S8 T3.1 |
| BR2 | The decision is recorded before the deviation row changes, with the rule ID and the package version in force; a failed write changes nothing and the caller sees MSG-P7-003 | DP-03; TSD S8 T2; legacy AC2 |
| BR3 | The case, its assignment, its queue and its timers stay with rwb-case: the stage clock is paused and resumed by the parent on this story's outcome, and no `recovery_case` or `timer` row is written here | Architecture v5 slides 8 and 13; ASM-5139 |
| BR4 | One clock rule: R-DEV-01 pauses the stage clock and never the prescription clock, and the case returns to the state it paused in | Architecture v5 slide 8 notes; R-DEV-01, R-DEV-08, R-DEV-18 |
| BR5 | The evidence pack and the customer facts stay with their owners: no `v_ace_*` view, no ACE table and no document blob is read here, and both arrive on the owner's contract | DP-05, DP-11; GAP-3051; ASM-5137, ASM-5138 |
| BR6 | A deviation code outside X1 to X7, or one with no owner, never lands here: R-DEV-21 routes it to the team manager of the case owner and logs it as unmapped | R-DEV-21; FSD S8 REQ-DVH-003 |
| BR7 | One event per raise and one per clear, published from the outbox in the transaction of the row, with identifiers, codes, the contact-stop flag and the rule version only | Context pack topic; connection matrix; ASM-5135, ASM-5136 |
| BR8 | The same raise twice, or the same `Idempotency-Key` twice, writes once, publishes once and answers one record | TSD S8 T-A.2; Architecture v5 slide 11 |
| BR9 | No person name, contact value, address or identity number enters `rwb_deviation`, the decision record, a log, a workflow input or an event | Template and Rules v1 §R7.2 s17 |

### 9. State transitions

The case route state is rwb-case's and this story does not change it: the step returns the outcome and the parent applies it (BR3). This story owns the `deviation.state` of the record it writes, over the 9 DEVIATION states of TSD S8 T4.

| From (`deviation.state`) | Event | Condition | To |
|---|---|---|---|
| No row | DEVIATION_FLAGGED | `deviation_code` = X1 and the record is written | DEV_FLAGGED, then DEV_WITH_OWNER on OWNER_ASSIGNED (R-DEV-01, R-DEV-02) |
| DEV_WITH_OWNER | DEVIATION_RESOLVED | `outcome` = RETURNED | DEV_RESOLVED, then RESUMED on CLOCK_RESUMED (R-DEV-09, R-DEV-18) |
| DEV_WITH_OWNER | DEVIATION_RESOLVED | `outcome` = RE_ROUTED | DEV_REROUTE, then ROUTE_D6 on ROUTE_REOPENED (R-DEV-19) |
| DEV_WITH_OWNER | DEVIATION_RESOLVED | `outcome` = CASE_ENDED, or no next step named | DEV_REROUTE with the outcome recorded as not mapped (R-DEV-22) |
| DEV_FLAGGED | FLAG_REJECTED | The officer marks the flag as not a deviation | DEV_REJECTED, then RESUMED (R-DEV-07, R-DEV-08) |
| DEV_WITH_OWNER | SLA_BREACHED | Time in DEV_WITH_OWNER exceeds the service level | Unchanged, escalated to the team manager with the breach reported (R-DEV-20) |
| Any | The same raise again | X6 | Unchanged; the repeat is counted and no event leaves |

| Step execution | Event | Condition | To |
|---|---|---|---|
| Waiting | A raise arrives for a case | The package in force is loaded | Evaluating |
| Evaluating | R-DEV-01 and R-DEV-02 fire | The decision record is written | Applying |
| Applying | The row and the outbox row are written and the outcome returned | The transaction commits | Waiting for the outcome |
| Applying | The record write or the transaction fails | X1 | Waiting, nothing changed, MSG-P7-003 |
| Waiting for the outcome | `PATCH /deviations/{deviationId}` arrives | The outcome is one of LOV-DEV-OUTCOME | Resolving |
| Resolving | R-DEV-09, R-DEV-18 or R-DEV-19 fire and `DeviationCleared` is relayed | The transaction commits | Closed |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Complaint officer (RW-COMPLAIN) | Holds RU on the case record (TSD S8 T6.1) and raises X1 on SCR-06, works SCR-08 and records the outcome on the case record |
| Case owner (RW-CASEOWN) | Holds CRU and is the "Case owner" the outcome rules name where the case is re-routed (R-DEV-09, R-DEV-19) |
| Team manager (RW-TEAMMGR) | Holds R and receives the escalation and the breach report of R-DEV-20 |
| Conduct and QA officer (RW-CONDUCT) | Holds R and reads the deviation and its decision record; the complaint-to-contact matching is another story's |
| rwb-case (P3) | Owns the case of record, its assignment, its queues and its timers, and applies the stage outcome this story returns |
| rwb-decision (P7) | Owns the DEV package, its rule rows and their version; this story only evaluates them and records the outcome |
| rwb-access (P4) | Owns the roles and the capability rights this story checks through the guard |
| Solution architect | Confirms the event names, the evidence-pack operation and the case boundary reading (GAP-3051) |

The FSD records the complaint officer as the primary role and the Conduct and QA officer as a secondary user (FSD S8 A2.10.3.3). No delegated authority limit applies: a deviation takes no credit decision, and the only approval in the module is the insurance claim of X3, which is not this story's.

### 11. Data

| BR Field ID | Table | Owner | Use in this story |
|---|---|---|---|
| DF-CAS-036 to DF-CAS-045 | `deviation` | S8, `rwb_deviation` | **Write**, one row per X1: `id`, `case_id`, `deviation_code`, `raised_at`, `raised_by`, `paused_state`, `handler_user_id`, `contact_stop`, `cleared_at`, `outcome`, plus `state` and the standard columns of TSD S8 T3.0 |
| None: library table | `decision_record` | Platform library in `rwb_deviation` | The hash-linked record written before the row (DP-03) |
| None: library table | `idempotency_key`, `outbox_event` | Platform library in `rwb_deviation` | The raise key with its answer and the two event rows relayed to the topic |
| DF-CAS-001 to DF-CAS-023 | `recovery_case` | P3 rwb-case | The case reference, its route state and its `paused_state`; consumed on the workflow boundary, never written |
| DF-WRK-001 to DF-WRK-016, DF-WRK-027 to DF-WRK-036 | `queue`, `assignment`, `timer` | P3 rwb-case | The complaint queue, the handler assignment and the two clocks; named, never written |
| DF-DEC-001 to DF-DEC-018 | `decision_log_entry` | P7 rwb-decision | The central ledger; the record of DP-03 is copied to it by rwb-decision, not written here |
| DF-REF-001 to DF-REF-015 | `rule_row` | P7 rwb-decision | The DEV package rows and their versions; read through the package, never written |
| DF-DOC-001 to DF-DOC-011 | `document` | P5 rwb-document | The evidence pack of the dispute; read on the owner's contract (GAP-3051; ASM-5137) |

The owned row writes the ten fields of DF-CAS-036 to DF-CAS-045 and no personal data: `case_id` and `handler_user_id` are identifiers of other services' facts, and no customer name, contact value or address is copied into `rwb_deviation` (BR9). The three lists are those of TSD S8 T3.2 - `LOV-DEVIATION` with X1 to X7, `LOV-RAISED-BY` with SCREENING_AGENT, RULE, OFFICER and CUSTOMER_CONTACT, and `LOV-DEV-OUTCOME` with RETURNED, RE_ROUTED and CASE_ENDED - and every one of them is reference data read at its version, never a constant (BR6, section 17).

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-deviation (S8); base `/api/recovery/deviation/v1` (DP-13). Both rows are the operations of the Ownership Map for this service and both are writes; the queue read is not published by this service (GAP-3051; ASM-5142).

| Method | Path | Shape | Access | Idempotency |
|---|---|---|---|---|
| POST | `/cases/{caseId}/deviations` | `DeviationRequest` in, `Deviation` out (API-S8-001) | Case record, right U, scope applied | `Idempotency-Key` header |
| PATCH | `/deviations/{deviationId}` | `DeviationOutcome` in, `Deviation` out (API-S8-002) | Case record, right U, scope applied | Not applicable |

Both answer 400, 401, 403 with MSG-P4-002, 404, 409, 422 with MSG-GEN-001 and 503, each in the platform error envelope; the exact status list and the shapes are RWB-S8-E7001-CON's. The POST is the one the self-service dispute of rwb-comms calls, and the PATCH is the one the officer's screen calls.

#### 12.2 REST operations consumed

| Operation | Owner | Use |
|---|---|---|
| The read of the case documents and their evidence pack; operation name Not specified in the source documents (GAP-3051; ASM-5137) | P5 rwb-document | The complaint evidence pack of the case: document type, source, storage reference and index entries (DF-DOC-001 to DF-DOC-011); faked on Day 1 |
| The read of the customer and contact facts of the case; operation name Not specified in the source documents (GAP-3051; ASM-5138) | P1 rwb-source-data | The facts the dispute is checked against, on the data-product contract with its freshness stamp; faked on Day 1 |

Both are one hop with a 2 s budget and a breaker, and neither retries inside the step (DP-11, ADR-020). Neither is a row of the plan's C list, which is empty (GAP-3051); the metadata rows stay as the plan gives them.

#### 12.3 Events published

| Event | Topic | Data | Consumers |
|---|---|---|---|
| `DeviationRaised` (EV-06, `rwb.deviation.DeviationRaised.v1`) | `rwb.deviation.events.v1`, with `.retry` and `.dlt` | Case reference, deviation reference, code X1, raised-at, paused state, contact-stop flag, rule ID and version; CloudEvents envelope; no personal data | rwb-case, rwb-comms and rwb-reporting (connection matrix column S8) |
| `DeviationCleared` (EV-07, `rwb.deviation.DeviationCleared.v1`) | `rwb.deviation.events.v1`, with `.retry` and `.dlt` | Case reference, deviation reference, outcome, cleared-at, rule ID and version; CloudEvents envelope; no personal data | rwb-case, rwb-comms and rwb-reporting (connection matrix column S8) |

The ids are the two events the Ownership Map gives S8 and their names are the two TSD S8 T5.3 publishes; the pairing of id to name is recorded as ASM-5134. The topic is the one naming rule of the context pack and DP-14 applies, although the plan's pattern set for this key does not carry it (ASM-5136).

#### 12.4 Events consumed

| Event | Owner | Use |
|---|---|---|
| The case events of rwb-case; event names Not specified in the source documents (GAP-3051; ASM-5139) | P3 rwb-case | Keeps an open deviation aligned with the case it belongs to: the case router forwards a case move to the running child, and a case that closes ends its open X1 with `CASE_ENDED` |

The S8 row of the connection matrix names an event subscription to P3 and none of its event names is published, so the consumer group is declared against the placeholder and faked (ASM-5139). No other event is consumed; the case router itself is rwb-case's.

#### 12.5 Workflows and activities

| Name | Type | Queue | Element |
|---|---|---|---|
| `DeviationWorkflow` | Workflow, one execution per case, started at any time, child of `CaseWorkflow`, parent close policy ABANDON, continues-as-new | `rwb-deviation` in namespace `rwb-recovery` | Hosts the X1 branch; its input, its signals and its stage outcome to the parent |
| `evaluateDeviationRules` | Activity, the EvaluateRules step | `rwb-deviation` | The case reference, the code and the paused state in; rule ID, package version and decision out |
| `recordAndApplyDeviation` | Activity, the RecordAndApply step | `rwb-deviation` | The decision in; the `deviation` row, the outbox rows and the stage outcome out, one transaction |
| `resolveDeviation` | Activity, the outcome step | `rwb-deviation` | The outcome in; the row update, `DeviationCleared` and the return point out |

The stage outcome carries the case reference, the deviation reference, the return point, the rule IDs with their versions and one of `CLOCK_PAUSE`, `CLOCK_RESUME` or `ROUTE_D6`; the parent applies it to the case and its timers (ASM-5139).

#### 12.6 Schedules

None. The Ownership Map gives S8 no job and the deviation is started by an event, a signal or the self-service raise, never by a clock of its own; R-DEV-20's escalation is a durable Temporal timer inside the workflow, not a Schedule. This story declares no Quartz row, no shared job table and no batch table.

#### 12.7 Tables owned

| Table | Owner | Use |
|---|---|---|
| `deviation` | S8, `rwb_deviation` | The X1 record: its code, raise facts, paused state, handler, contact stop, outcome and state |
| `decision_record` | Platform library in `rwb_deviation` | The local record written before the row (DP-03) |
| `idempotency_key` | Platform library in `rwb_deviation` | The raise key and the answer it holds |
| `outbox_event` | Platform library in `rwb_deviation` | The `DeviationRaised` and `DeviationCleared` rows relayed to the topic |

`recovery_case`, `queue`, `assignment`, `timer`, `decision_log_entry`, `rule_row`, `document` and every `v_ace_*` view are other owners' and are named only; no foreign key leaves `rwb_deviation` (DP-01).

#### 12.8 Contract fakes

| Fake | Answer | Used by |
|---|---|---|
| rwb-case workflow fake | The case in `WITH_FCR_OFFICER` with its prescription date; an accepted `CLOCK_PAUSE` and `CLOCK_RESUME`; a refused outcome; a case-closed event | AC2, X6, X7 |
| rwb-document evidence-pack fake | The complaint evidence pack of a synthetic case; an empty pack; no answer inside 2 s | AC2, X5 |
| rwb-source-data data-product fake | The customer and contact facts of the case with a fresh stamp; a stale stamp | AC2, X4 |
| rwb-decision package fake | The DEV package at its version with the nine rules of section 8 | AC2 |
| Local decision-record stub (`RWB-PLT-E1027-CON`) | A healthy chain and outbox; a stopped chain | AC2 |
| Outbox relay stub (`RWB-PLT-TE006-CON`) | A relayed `DeviationRaised` and `DeviationCleared`; a relay that fails and retries | AC2 |
| gateway-bff composite route fake | The merged SCR-06 and SCR-08 answer for a synthetic case | AC2 |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 2 consumed | `POST /cases/{caseId}/deviations` and `PATCH /deviations/{deviationId}` on `/api/recovery/deviation/v1`; the rwb-document and rwb-source-data reads; one hop, 2 s |
| Kafka | 2 published, 1 consumed | `DeviationRaised` and `DeviationCleared` on `rwb.deviation.events.v1`; the rwb-case case events; the decision record rides the library's `rwb.decision-record.v1` and is not this service's event |
| Temporal | 1 workflow and 3 activities | `DeviationWorkflow` with `evaluateDeviationRules`, `recordAndApplyDeviation` and `resolveDeviation` on `rwb-deviation`; no Schedule |
| File | None | No file is read, built or delivered by this story |

### 13. Solution plan

**Deliverables.** The X1 branch of `DeviationWorkflow` with its three activities, the evaluator against the DEV package version, the decision-record writer, the `deviation` insert and update with their outbox and idempotency rows, the two publishers, the stage outcome with the clock signal, the two write handlers on the target base and the two read-only screen fragments.

**Pattern application** (§R5.5)

| DP | Legacy marker | Pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H `RWB-PLT-E1027-CON` |
| DP-13 | `/api/recovery/v1` | `/api/recovery/deviation/v1` | None |
| DP-19 | Screen, ace-web | gateway-bff composite route | H `RWB-PLT-N001-CON` |

DP-13 moves the base of the two operations and nothing else. DP-19 puts SCR-06 and SCR-08 behind the composite route. DP-09 and DP-14 are not in the pattern set of this key although the two published events need the outbox library and the topic naming rule (ASM-5135, ASM-5136).

**Build steps.** (1) Wire the `DeviationWorkflow` branch and its activities on `rwb-deviation`. (2) Load the DEV package version and evaluate R-DEV-01 and R-DEV-02. (3) Write the decision record first and insert the `deviation` row with its contact stop, its outbox rows and its idempotency row in one transaction. (4) Publish `DeviationRaised` and return the clock-pause outcome. (5) Implement the outcome path with R-DEV-09, R-DEV-18, R-DEV-19, R-DEV-22 and the `DeviationCleared` publication. (6) Add the R-DEV-20 timer and the escalation. (7) Add the two write handlers on the target base and the two screen fragments. (8) Prove AC2 and the eight exception paths on the fakes.

**Done when.** AC2 passes at component level on the fakes, the raise and the outcome each write once and publish once under a repeat, the boundary test shows no `v_ace_*` read and no `rwb_case` statement, and the two screens answer through the gateway-bff route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S8-001 | The raise succeeds and the case moves to its handler (SCR-06 saved) | {deviation} was raised. The case is with {handler}. |
| MSG-GEN-001 | A required value of the raise or of the outcome is absent or invalid (X3) | Enter {field}. |
| MSG-P4-002 | The role lacks the Case record right of the operation (X2) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the change (X1) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | The data product behind the case facts is stale (X4, VR-S8-010-1) | {product} is from {date}. Today's ACE batch has not arrived. |

The text is the legacy and FSD S8 wording, copied unchanged; no message is reworded and none is added. The X1 complaint service level that R-DEV-20 escalates against is set with DL22 and not published (GAP-3051; ASM-5140).

### 15. Screens and states

| Screen | States | What this story answers |
|---|---|---|
| SCR-06 Raise deviation | Form; saved | The raise of X1 with its reason, its raised-by and the saved confirmation of MSG-S8-001 on `POST /cases/{caseId}/deviations` |
| SCR-08 Deviation queue | Loading; list | The officer's open deviations by type, handler and age, and the outcome entry that sends `PATCH /deviations/{deviationId}` |

Both screens are the edge contract's (DP-19) and the composite route also calls rwb-case for the case, its owner and its timers; this story fixes only its own answers (ASM-5142). The saved, refused, not-recorded and stale-data states read the messages of section 14 on the same route.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E7-001-01 | AC1 (as the legacy id of this key: the record, the handler and the decision-log entry of an X1) | Component | Synthetic case `RW-2026-000701`; one `deviation` row in DEV_WITH_OWNER, one decision record, one `DeviationRaised`; the end-to-end half is RWB-ITG-E7001-ITG |
| TC-E7-001-02 | AC2 | Component | The decision-record stub stopped on the raise and on the outcome; no row, no event, no outcome and no pause, MSG-P7-003 |
| TC-E7-001-03 | AC2, X2 | Component | A role without the Case record right; 403 with MSG-P4-002 and no decision record |
| TC-E7-001-04 | AC2, X1 | Component | A forced decision-record write failure stops the action with MSG-P7-003 |

The four ids are the legacy cases of RWB-E7-001 in their legacy order, carried as the application proof of this slice; TC-E7-001-01 exercises the record this story writes and its cross-service half is proved by RWB-ITG-E7001-ITG under the same id with the `-ITG` suffix (ASM-5141). The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same id; the `-ITG` copies belong to the wave 4 harness.

### 17. Guardrails

- No business value in code: the deviation codes, the raised-by and outcome lists, the 10-working-day escalation and the complaint service level stay reference data or rule rows read with their version.
- No personal data in the deviation row, the decision record, an event, a workflow input, a log or a prompt: identifiers, codes, instants and a rule version only.
- ACE data and documents only through the owner's contract: no `v_ace_*` view, no ACE table, no document blob and no other service's schema (DP-01, DP-05, DP-11).
- One base, one topic, one queue and one login per service; this story adds no second topic and no Schedule (DP-13, DP-14).
- The decision record is written before the change and in its transaction; a failure rolls the row back (DP-03).
- One clock rule: the stage clock is paused and resumed by rwb-case on this story's outcome, and the prescription clock is never paused (BR4).

### 18. Traceability

| Legacy | Story | Test |
|---|---|---|
| RWB-E7-001 AC1 | Not copied here; owned by RWB-ITG-E7001-ITG (ASM-5141) | TC-E7-001-01 (the application half), TC-E7-001-01-ITG |
| RWB-E7-001 AC2 | AC2 (verbatim, with the mock lines) | TC-E7-001-02, TC-E7-001-04 |
| RWB-E7-001 TC-03 Access | AC2, X2 (the right on the two operations) | TC-E7-001-03 |
| RWB-E7-001 TC-04 Principle 5 | AC2, X1 (the forced failure of the decision record) | TC-E7-001-04 |

| Source | What it supplies |
|---|---|
| REQ-DVH-011, REQ-S8-003 (FSD S8 Requirements served) | The end-to-end deviation flow and the complaint resolved inside its service level with the timers resumed |
| FSD S8 A2.10, A1.4, Screens | The X1 feature, its prerequisites, VR-S8-010-1, the roles and SCR-06 and SCR-08 |
| TSD S8 T2, T3.1, T3.2, T4, T5.3, T6.1 and T-A.1 | The decision-first rule, the `deviation` columns and lists, the DEVIATION state machine, the two events, the rights and the two operations |
| Business Rules and Routing Logic v4, DEV route set | R-DEV-01, R-DEV-02, R-DEV-07 to R-DEV-09, R-DEV-18 to R-DEV-20 and R-DEV-22 |
| Context pack S8 and the connection matrix | The schema, base, topic, queue, the two events, the one owned table and the listeners of P3, P6 and P9 |
| Split plan, slice RWB-S8-E7001-APP | H, C, I, X, the lane, the wave and the release (GAP-3051) |

### 19. Out of scope

- The contract surface: the OpenAPI and AsyncAPI documents, the `deviation` element, the lists, the two envelopes, the error set and the fakes (RWB-S8-E7001-CON).
- The end-to-end X1 journey across the services and the wave 4 harness (RWB-ITG-E7001-ITG, which owns AC1); the X1 happy-path acceptance criteria are not restated here.
- The other six codes and their flows (X2 to X7), the screening agent and its L1 policy, the low-confidence review, two deviations on one case, the contact-breach path, the override review and the complaint-to-contact matching - each is its own story of this service.
- The case of record, its route state, its assignment, its queues and its timers (rwb-case, P3); the evidence pack and its retention (rwb-document, P5); the notices and the self-service dispute (rwb-comms, P6); the DEV package and the ledger (rwb-decision, P7); the roles and reference data (rwb-access, P4).
- The schema and migration of `rwb_deviation`, the login, the deployment, the observability and the pipeline (the DB, INF and OPS stories of this legacy key).
- Any change to a legacy file, to a master or to built Epic 1 and Epic 2 code.
