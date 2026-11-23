# RWB-S8-E2036-APP Queue write interface for models and agents

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S8-E2036-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-deviation |
| Service epic | RWB-SVC-S8 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-036 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP07, DP08, DP09, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | L-S8-K |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P2-E2036-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S8 rwb-deviation v1.md (no FR mapped to REQ-CWC-017, REQ-CWC-018, REQ-CWC-019, REQ-CWC-020, REQ-ACA-010) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the deviation slice of RWB-E2-036 is realigned onto rwb-deviation (S8, service wave 2, business wave 2). The placement command itself stays with rwb-case (RWB-P3-E2036-APP) and the caller-facing admission with rwb-integration; this story owns the one fact of the deviation service that the queue-write interface obeys — the hold that an open deviation puts on a case, carried on `DeviationRaised` (EV-06) and `DeviationCleared` (EV-07) on `rwb.deviation.events.v1` with the exact open-deviation count, the handler and the return point, so that a model or an agent never moves a case out of a deviation handler's queue and a hold is not lifted while a second deviation is still open. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **center of excellence analyst (RW-COE)** and the **deviation handler of a case**, I want **an open deviation on a case to publish one exact hold — the case, the code, the open count, the handler and the state the case paused in — on the two events of rwb-deviation, and to keep that hold until the last deviation clears**, so that **a model or an agent never moves a case out of a deviation handler's queue and a case is never released early**.

This is the deviation slice of legacy RWB-E2-036. It owns:

- the **hold facts on the two published events** — `DeviationRaised` and `DeviationCleared` on `rwb.deviation.events.v1`, with the case, the code, the exact open-deviation count, the handler and the return point, written to the outbox in the transaction of the `deviation` row (DP-09, DP-14);
- the **count and the lift rule**, read from the `deviation` rows of the case that are not cleared, so the hold is exact when a second deviation is open and lifts only at the last clear (FEAT-DVH-09; FSD S8 A2.9; R-DEV-08, R-DEV-18);
- the **decision record** of the hold, written before the row and the event commit (DP-03), the **lists** read at their version (DP-07) and the **right** of the act (DP-08);
- one migration in `rwb_deviation` for the count read, and the service's own base, topic and queue (DP-01, DP-13, DP-14, DP-15);
- the **hold banner** that SCR-02 and SCR-07 merge through the gateway-bff composite route (DP-19).

It owns **no legacy acceptance criterion**: the split plan gives this slice none, and section 7 carries eight criteria written for the service change.

It does not own: the placement command, the queue, the caseload cap, the overflow queue, the assignment and the refusal itself (rwb-case, RWB-P3-E2036-APP); the caller-facing admission, its replay and the approved callers list (rwb-integration); the Queue and allocation C answer (rwb-access); the central ledger and the DEV rule rows (rwb-decision); the raise and the clear of a deviation as the X1 dispute journey (RWB-S8-E7001-APP); and the schema, the deployment and the observability of the service (the DB, INF and OPS stories of this key).

### 2. Business rationale

Model scores and agent findings reach the queues today through a weekly file that a person loads by hand, so a case flagged on Monday is worked the following week. The interface lets an approved caller place a case on a queue the day the decision is made, and it carries one safeguard: **a case with an open deviation stays with the deviation handler** (legacy §8 BR4; R-DEV-01). That safeguard is the only part of the interface this service supplies, and it is the part that cannot be checked anywhere else.

In the monolith the safeguard was a read of the deviation table inside the placement handler. In the target the placement handler is rwb-case's and the deviation record is this service's, so the fact has to travel. The target design gives it no synchronous call: the S8 row of the connection matrix is Temporal and events to P3, the Ownership Map gives S8 exactly two operations and neither is a queue or hold read, and the case record already carries `deviation_open` (DF-CAS-019), which rwb-case reads for its refusal without asking this service (RWB-P3-E2036-APP). The hand-over is therefore the two events this service already publishes, and this story makes them sufficient: the hold, the exact open count, the handler and the return point.

The count is the second reason this slice exists. A case may carry more than one open deviation and resumes only when all are cleared (FSD S8 A2.9; FEAT-DVH-09). If the hold were a flag toggled per deviation, the first clear would release a case that is still disputed, and the interface would place it — a wrong business answer caused by a lost count. Publishing the count on every raise and every clear lets the consumer hold the case while the count is above zero and lift the hold exactly at zero, whatever order the deviations are cleared in.

It meets REQ-CWC-017 (the write carries the case and the reason), REQ-CWC-019 (the interface is not opened to a consumer until its safeguards hold) and REQ-ACA-010 (a non-human caller is subject to the same checks), and it serves control CTL-06 and rule R-UNI-39 through the record-first rule. The business measure does not move: the time from a model decision to the case reaching a queue, from up to 7 days to the same day (legacy §2).

### 3. Preconditions

- RWB-P2-E2036-CON is published: the placement contract with its refusals, including the open-deviation refusal and its message, its error envelope and its fake. This story builds against that contract and never resolves the refusal from an rwb-integration table (DP-11).
- The two events of the service are baselined at their shape — `DeviationRaised` (EV-06) and `DeviationCleared` (EV-07) on `rwb.deviation.events.v1` — and the hold facts this story adds are authored inside major version 1 by the event catalogue and the service contract story. The payload element names are Not specified in the source documents (GAP-3102; ASM-5317).
- `deviation` exists in `rwb_deviation` from the DB story of this service with the columns of DF-CAS-036 to DF-CAS-045 and the standard record columns of TSD S8 T3.0; the migration of section 13 is the only change this story makes to the schema (DP-15).
- The local decision-record library and the shared topic `rwb.decision-record.v1` are published with the writer stub: the record is written in the caller's transaction and a failed write stops the act with MSG-P7-003 (DP-03).
- The outbox, inbox and idempotency libraries are published with their stubs, and the naming library fixes the topic name `rwb.deviation.events.v1` with its retry and `.dlt` topics (DP-09, DP-14).
- The reference-data contract of rwb-case is published with its fake: `LOV-DEVIATION` (X1 to X7), `LOV-RAISED-BY` (SCREENING_AGENT, RULE, OFFICER, CUSTOMER_CONTACT) and `LOV-DEV-OUTCOME` (RETURNED, RE_ROUTED, CASE_ENDED) are read at the version in force and never written in code (DP-07; TSD S8 T3.2).
- The authorise contract of rwb-access and the guard library are published with their fake: the act holds the Case record right of the matrix in force (DP-08; TSD S8 T6.1).
- The DEV rule package is in force at its version with R-DEV-01, R-DEV-02, R-DEV-03, R-DEV-08, R-DEV-09 and R-DEV-18; the rows are authored and approved in rwb-decision and loaded here (FSD S8 A2.2.3.1, A2.4.3.1, A2.6.3.1).
- The rwb-case side of the hold is available as a fake: the case router applies the hold it is given and answers with the case state; no source publishes an operation of rwb-case that sets `deviation_open`, so the fake stands in for the consumer (GAP-3102; ASM-5316).
- The gateway-bff composite route is published: SCR-02 and SCR-07 merge the hold banner and the on-hold state from this service and the case, one hop each (DP-19).
- The service runs as its own login on `rwb_deviation` and holds no grant on another `rwb_*` schema and no `v_ace_*` grant, so a statement on `rwb_case` fails the database and the boundary test (DP-01).
- No approval is needed to build against a Draft contract baseline; the contract is tagged by RWB-P2-E2036-CON and the event catalogue when their tests pass.

### 4. Flow

1. A deviation is raised on a case from one of three places: the screening agent of E2, an officer on SCR-06, or a customer contact; the raise reaches `DeviationWorkflow` on task queue `rwb-deviation` as a signal, never as a table write on the request thread (FEAT-DVH-01; Architecture v5 slide 13).
2. `evaluateDeviationRules` loads the DEV package version in force and evaluates R-DEV-01 — the stage clock pauses, the prescription clock keeps running — then R-DEV-02 for X1 and R-DEV-03 for X2 and X3, with Legal joining X3 (FSD S8 A2.4).
3. `recordAndApplyDeviation` writes one decision record through the local library **before any change**: case reference, deviation reference, rule ID with the package version, the outcome and the decided-at time (DP-03; TSD S8 T2).
4. In the same `rwb_deviation` transaction the activity inserts the `deviation` row — `case_id`, `deviation_code` of `LOV-DEVIATION`, `raised_at`, `raised_by` of `LOV-RAISED-BY`, `paused_state`, `handler_user_id`, `contact_stop` and `state` after the move (TSD S8 T3.1).
5. In the same transaction the activity reads the **open-deviation count** of the case: the rows of `deviation` for that case whose `cleared_at` is empty, counted after the insert (ASM-5318).
6. The outbox row of `DeviationRaised` is written in that transaction with the case, the deviation, the code, the **open count**, the handler and the return point, and no personal data; the relay publishes it on `rwb.deviation.events.v1` with the CloudEvents envelope (DP-09, DP-14).
7. rwb-case consumes the event on its case router and holds the case: `deviation_open` becomes true while the count is above zero, and the case stays in the deviation handler's queue and keeps its owner; a placement that arrives for that case is refused there (RWB-P3-E2036-APP; ASM-5316).
8. The handler works the deviation; `clearDeviation` records the outcome with R-DEV-09 on `PATCH /deviations/{deviationId}` — RETURNED, RE_ROUTED or CASE_ENDED of `LOV-DEV-OUTCOME` — and writes `cleared_at` and `outcome`.
9. In that transaction the count is read again, and the outbox row of `DeviationCleared` carries the case, the deviation, the outcome, the cleared-at instant, the remaining **open count** and, when that count is zero, the **return point** so the case returns to the state it paused in (R-DEV-08, R-DEV-18).
10. While the count is above zero the consumer keeps the hold; at zero the hold lifts, the case returns to `paused_state` and, where the outcome re-routes it, the route decision D6 is reopened in rwb-valuation (R-DEV-19).
11. A repeat of the same raise or the same clear for the same deviation is deduplicated by the inbox, answers the answer already stored, writes no second `deviation` row, no second outbox row and no second event, and leaves the count where it was (DP-09).
12. The hold banner on SCR-02 and SCR-07 and the on-hold state read the hold through the gateway-bff composite route; this story adds no screen and no new operation (DP-19; legacy §15).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The decision record cannot be written | Nothing changes: no `deviation` row, no outbox row and no event, so the hold the placement interface obeys does not move | MSG-P7-003 | AC6 |
| X2 | The role lacks the Case record right of the raise or of the clear | 403 before any change and before any record; no event and no count movement | MSG-P4-002 | AC7 |
| X3 | A required value is absent or outside its list: the code, the raised-by, the outcome or the paused state | The request is refused with the field named; nothing is written and no hold is published | MSG-GEN-001 | AC1, AC4 |
| X4 | The reference-data list cannot be read | The act holds, nothing is written and no event leaves; the list id is named | None (platform envelope) | AC5 |
| X5 | A repeated raise or clear of the same deviation arrives twice | One row, one outbox row, one event; the count is unchanged and the consumer sees one hold | None | AC5 |
| X6 | A second deviation is open on the case when the first clears | The count stays above zero and the event carries that count, so the hold is not lifted and a placement is still refused | None | AC2, AC3 |
| X7 | The case closes while a deviation is open | The case event ends the open deviation with `CASE_ENDED`; the count falls to zero and the hold lifts with the case, not before | None | AC3 |
| X8 | A statement, a component or a test reaches `rwb_case`, `rwb_queue` or another service's schema | The grant refuses the statement and the boundary test fails the build | None (pipeline log) | Section 17, BR2, BR7 |

X1 to X3 are the paths the legacy key carries; X4 to X7 are the paths the target call types and the second-deviation rule add; X8 is the DP-01 boundary.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-P2-E2036-CON's fake, the decision-record and outbox stubs, the reference-data and guard fakes and the case-router fake, on its own schema; needs no live P1, P2, P3 or P4 |
| Negotiable | The activity names, the shape of the hold element and the count query are this story's choice; the events, the codes, the lists, the states and the messages are fixed |
| Valuable | A case in a deviation handler's queue cannot be moved by a model or an agent, and a hold is never lifted while another deviation is open |
| Estimable | One workflow branch, two activities, two event publications, one count read, one index and the access and failure tests |
| Small | Finished inside two weeks with its tests on the fakes |
| Testable | Every path runs on synthetic cases through the contract fakes, plus the access refusal, the forced record failure and the duplicate delivery |

### 7. Acceptance criteria

```gherkin
Feature: Queue write interface for models and agents — the deviation hold

  Background:
    Given the DEV rule package is in force at its version and carries R-DEV-01, R-DEV-02, R-DEV-03, R-DEV-08, R-DEV-09 and R-DEV-18
    Given the lists LOV-DEVIATION, LOV-RAISED-BY and LOV-DEV-OUTCOME are read at the version in force
    Given the rwb-case reference-data contract mock returns LOV-DEVIATION with X1 to X7, LOV-RAISED-BY with SCREENING_AGENT, RULE, OFFICER and CUSTOMER_CONTACT, and LOV-DEV-OUTCOME with RETURNED, RE_ROUTED and CASE_ENDED
    Given the rwb-case contract mock returns case "RW-2026-000504" with no open deviation and the deviation handler queue, and applies every hold it is given
    Given the rwb-integration contract mock returns the refusal with message MSG-P2-021 for a case with an open deviation

  Scenario: AC1 The first deviation publishes one hold with its handler and its return point (new, D-RCV-60)
    Given case "RW-2026-000504" has no open deviation
    When deviation "X2" is raised on it with raised_by "SCREENING_AGENT" and paused state "WITH_FCR_OFFICER"
    Then one "deviation" row is written with code "X2", handler "U-SP-01", contact stop true and state "DEV_WITH_OWNER"
    Then one "DeviationRaised" is written to the outbox with case "RW-2026-000504", code "X2", open count 1, the handler and the return point "WITH_FCR_OFFICER"
    Then the case mock is given the hold and holds the case in the deviation handler queue
    Then the payload carries no customer name, contact value or identity number

  Scenario: AC2 A second deviation keeps the hold and counts (new, D-RCV-60)
    Given deviation "X2" on case "RW-2026-000504" is open with open count 1
    When deviation "X3" is raised on the same case
    Then one "DeviationRaised" is published with code "X3" and open count 2
    Then the case mock still holds the case and no hold is lifted
    Then a placement of that case is refused with message MSG-P2-021

  Scenario: AC3 The hold lifts only at the last clear (new, D-RCV-60)
    Given deviations "X2" and "X3" on case "RW-2026-000504" are open with open count 2
    When "X2" is cleared with outcome "RETURNED"
    Then one "DeviationCleared" is published for "X2" with open count 1 and no return point
    Then the case mock still holds the case
    When "X3" is then cleared with outcome "RETURNED"
    Then one "DeviationCleared" is published for "X3" with open count 0 and return point "WITH_FCR_OFFICER"
    Then the case mock lifts the hold and returns the case to "WITH_FCR_OFFICER"

  Scenario: AC4 The clear records the outcome and the act never moves the case (new, D-RCV-60)
    Given deviation "X1" on case "RW-2026-000504" is open and the handler "U-SP-01" is recorded
    When the handler records outcome "RE_ROUTED"
    Then the "deviation" row carries cleared_at, outcome "RE_ROUTED" and state "DEV_REROUTE"
    Then the handler "U-SP-01" and the paused state are unchanged
    Then this service writes no queue, assignment or case row

  Scenario: AC5 The lists and the count come from their owners and a repeat writes once (new, D-RCV-60)
    Given the rwb-case reference-data contract mock returns LOV-DEVIATION as unavailable
    When a deviation is raised
    Then no "deviation" row and no outbox row is written and no event leaves
    Given the contract mock answers again and the raise is delivered twice with the same deviation reference
    Then one "deviation" row, one outbox row and one "DeviationRaised" exist with open count 1

  Scenario: AC6 The record and the event commit together (new, D-RCV-60)
    Given the decision-record stub is forced to fail
    When a deviation is raised on case "RW-2026-000504"
    Then the act is refused with message MSG-P7-003
    Then no "deviation" row, no outbox row and no event exist
    Then the case mock is given no hold and the placement interface still sees the case as free of deviation

  Scenario: AC7 The act is guarded and no hold leaves without a right (new, D-RCV-60)
    Given a role without the Case record right
    When it raises or clears a deviation on case "RW-2026-000504"
    Then the act is refused with message MSG-P4-002
    Then no "deviation" row is written and no event leaves
    Then no decision record is written

  Scenario: AC8 The queue-write path needs no operation of this service (new, D-RCV-60)
    Given case "RW-2026-000504" carries an open deviation and the hold it published
    When the placement path asks whether the case may move
    Then no operation of the deviation base "/api/recovery/deviation/v1" is called
    Then the refusal is answered from the case flag the hold set
    Then the service exposes exactly the two operations it exposed before this story
```

The eight criteria are new for the service change and each tests one deliverable of the title: the hold, its count, its lift, its return point, its lists and count, its transaction, its right and its boundary. The values they use — case "RW-2026-000504", codes X1 to X7, handler "U-SP-01", paused state "WITH_FCR_OFFICER", messages MSG-P2-021, MSG-P7-003, MSG-P4-002 and MSG-GEN-001 — are the legacy story's and the FSD's, copied unchanged; no business value is chosen here.

### 8. Business rules

| Rule | Route set | Codes | From state | Event | Condition | Action | To state | Owner | Timer |
|---|---|---|---|---|---|---|---|---|---|
| R-DEV-01 | Deviations | X1 to X7 | ANY_STATE | DEVIATION_FLAGGED | deviation_code in (X1..X7) | Pause the stage clock, keep the prescription clock running, route to the named owner | DEV_FLAGGED | Workbench | same day |
| R-DEV-02 | Deviations | X1 | DEV_FLAGGED | OWNER_ASSIGNED | deviation_code = X1 | Assign to the complaint officer | DEV_WITH_OWNER | Complaint officer | None |
| R-DEV-03 | Deviations | X2, X3 | DEV_FLAGGED | OWNER_ASSIGNED | deviation_code in (X2,X3) | Assign to the specialist; Legal joins X3 for the estate claim | DEV_WITH_OWNER | Hardship and vulnerability specialist | None |
| R-DEV-08 | Deviations | X1 to X7 | DEV_REJECTED | CLOCK_RESUMED | Any | Return the case to the state it paused in | RESUMED | Previous owner | None |
| R-DEV-09 | Deviations | X1, X7 | DEV_WITH_OWNER | DEVIATION_RESOLVED | deviation_code in (X1,X7) | Record the outcome; the same decision resumes | DEV_RESOLVED | Case owner | None |
| R-DEV-18 | Deviations | X1 to X7 | DEV_RESOLVED | CLOCK_RESUMED | Any | Resume the stage clock and return the case | RESUMED | Previous owner | None |

The six rows are the rows of Business Rules and Routing Logic v4, copied character for character; R-DEV-04 to R-DEV-06 move the other codes from DEV_FLAGGED to DEV_WITH_OWNER (TSD S8 T4) and their conditions are set in the workbook, so they are not restated here. The owner column is a business role, not a service: the states are `deviation.state` of this service, the route states of the case are rwb-case's, the DEV package and its versions are rwb-decision's.

| ID | Rule | Source |
|---|---|---|
| BR1 | A case with an open deviation stays with the deviation handler: the hold this story publishes is what the queue-write interface obeys, and no placement moves such a case | Legacy §8 BR4; R-DEV-01 |
| BR2 | `deviation` is this service's: its code, raise facts, paused state, handler, contact stop, outcome and state are columns of `deviation` in `rwb_deviation`, and no other service writes them | Context pack ownership rows; TSD S8 T3.1 |
| BR3 | The hold is true while at least one deviation of the case is open, and lifts only when the last one clears; the count on the event is the authority for that decision | FSD S8 A2.9; FEAT-DVH-09; ASM-5318 |
| BR4 | The decision is recorded before the deviation row changes, with the rule ID and the package version in force; a failed write changes nothing and the caller sees MSG-P7-003 | DP-03; TSD S8 T2 |
| BR5 | The case, its queue, its assignment, its timers and its `deviation_open` flag stay with rwb-case: the flag is set and cleared by the case from this story's events, and no case or queue row is written here | Architecture v5 slide 13; RWB-P3-E2036-APP; ASM-5316 |
| BR6 | One event per raise and one per clear, published from the outbox in the transaction of the row, with identifiers, codes, the count, the handler, the return point and the rule version only | Context pack topic; connection matrix; ASM-5317 |
| BR7 | No person name, contact value, address or identity number enters `rwb_deviation`, the decision record, a log, a workflow input or an event | Template and Rules v1 §R7.2 s17 |
| BR8 | Every code, raised-by value, outcome and state is reference data or a rule row read at its version, and an unreadable list holds the act | TSD S8 T3.2; FSD S8 A2.8.3.1 (BR-S8-008) |

### 9. State transitions

The case route state is rwb-case's and this story does not change it: the hold it publishes is applied by the case (BR5). This story owns `deviation.state` over the 9 DEVIATION states of TSD S8 T4, and the hold marker that the two events carry.

| From (`deviation.state`) | Event | Condition | To |
|---|---|---|---|
| No row | DEVIATION_FLAGGED | `deviation_code` in X1 to X7 and the record is written | DEV_FLAGGED, then DEV_WITH_OWNER on OWNER_ASSIGNED (R-DEV-01, R-DEV-02, R-DEV-03) |
| DEV_WITH_OWNER | DEVIATION_RESOLVED | `outcome` = RETURNED | DEV_RESOLVED, then RESUMED on CLOCK_RESUMED (R-DEV-09, R-DEV-18) |
| DEV_WITH_OWNER | DEVIATION_RESOLVED | `outcome` = RE_ROUTED or CASE_ENDED | DEV_REROUTE, then the route decision D6 or the case end (R-DEV-19) |
| DEV_FLAGGED | FLAG_REJECTED | The owner marks the flag as not a deviation | DEV_REJECTED, then RESUMED (R-DEV-07, R-DEV-08) |
| Any | The case closes while the flag is open | A case event names the case closed | The open deviation ends with `CASE_ENDED`; the count falls and the hold lifts with the case |

| Hold marker (carried on the events) | Event | Condition | To |
|---|---|---|---|
| Off | A deviation is raised | Count after the insert is 1 | On, count 1, handler and return point carried |
| On, count n | A deviation is raised | Count after the insert is n+1 | On, count n+1 |
| On, count n | A deviation is cleared | Count after the clear is above zero | On, count n-1, no return point |
| On, count 1 | A deviation is cleared | Count after the clear is zero | Off, count 0, return point carried |
| Any | The same raise or clear again | The deviation reference and the key are already stored | Unchanged; no second row and no second event |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Complaint officer (RW-COMPLAIN) | Holds RU and raises X1, works it and records its outcome (TSD S8 T6.1; FSD S8 A2.10.3.3) |
| Hardship and vulnerability specialist (RW-SPECIAL) | Holds RU and raises and works X2 and X3 (FSD S8 A2.11, A2.12) |
| Fraud investigator (RW-FRAUD) | Holds RU and works X4 (FSD S8 A2.13) |
| Legal counsel (RW-LEGAL) | Holds R, joins X3 on the estate claim and reads the hold and its decision record (R-DEV-03) |
| Case owner (RW-CASEOWN) | Holds CRU and is the role the resolution rules name where the case is returned (R-DEV-09, R-DEV-18) |
| Conduct and QA officer (RW-CONDUCT) | Holds R and reads the deviations, their holds and their records |
| rwb-case (P3) | Owns the case of record, its queue, its assignment, its timers and its `deviation_open` flag, and applies the hold this story publishes |
| rwb-integration (P2) | Owns the caller-facing placement contract whose refusal message this story's hold reason agrees with |
| rwb-decision (P7) | Owns the DEV package, its rule rows and the central ledger |
| rwb-access (P4) | Owns the roles and the capability rights this story checks through the guard |
| Solution architect | Confirms the hold element, the count rule and the case boundary reading (GAP-3102) |

No level of the delegated authority applies: a deviation takes no credit decision, and no approval level from the delegation of authority is used by the placement (legacy §10).

### 11. Data

| BR Field ID | Table | Owner | Use in this story |
|---|---|---|---|
| DF-CAS-036 to DF-CAS-045 | `deviation` | S8, `rwb_deviation` | **Write and read**: `id`, `case_id`, `deviation_code`, `raised_at`, `raised_by`, `paused_state`, `handler_user_id`, `contact_stop`, `cleared_at`, `outcome`, plus `state` and the standard columns of TSD S8 T3.0 |
| None: derived | `deviation` open count | S8, `rwb_deviation` | **Read**: the rows of the case whose `cleared_at` is empty, counted in the transaction of the raise and of the clear; no counter column is added |
| None: library table | `decision_record` | Platform library in `rwb_deviation` | The hash-linked record written before the row (DP-03) |
| None: library table | `outbox_event`, `processed_event`, `idempotency_key` | Platform library in `rwb_deviation` | The two event rows, the inbox mark of a repeat and the stored answer (DP-09) |
| DF-CAS-001 to DF-CAS-023, DF-CAS-019 | `recovery_case` | P3 rwb-case | The case reference and its `deviation_open` flag; named on the event, never written |
| DF-WRK-001 to DF-WRK-016 | `queue`, `assignment` | P3 rwb-case | The deviation handler's queue and the assignment that a refused placement leaves alone; named, never written |
| DF-DEC-001 to DF-DEC-018 | `decision_log_entry` | P7 rwb-decision | The central ledger; the record of DP-03 is copied to it by rwb-decision, not written here |
| DF-REF-001 to DF-REF-015 | `rule_row` | P7 rwb-decision | The DEV package rows and their versions; read through the package, never written |

The owned row writes the ten fields of DF-CAS-036 to DF-CAS-045 and no personal data: `case_id` and `handler_user_id` are identifiers of other services' facts, and no customer name, contact value or address is copied into `rwb_deviation`. The three lists are TSD S8 T3.2's and every one of them is reference data read at its version, never a constant (BR8).

### 12. Contract

#### 12.1 REST operations provided

None added. The service keeps the two operations the Ownership Map gives it on base `/api/recovery/deviation/v1` (DP-13), unchanged and owned by RWB-S8-E7001-APP: `POST /cases/{caseId}/deviations` (API-S8-001) and `PATCH /deviations/{deviationId}` (API-S8-002). No operation is added for a queue, a hold or a placement read, because the hold travels on the events (ASM-5316).

#### 12.2 REST operations consumed

None at run time. The rwb-integration placement contract RWB-P2-E2036-CON is a **build-against** dependency: its refusal for a case with an open deviation, its message and its envelope fix the wording this story's hold reason agrees with, and its fake stands in for the answered refusal (DP-11). This story calls no service on a request thread: the raise and the clear arrive as signals and workflow inputs, and the case is answered by the events. The element names of that refusal are Not specified in the source documents (GAP-3102; ASM-5317).

#### 12.3 Events published

| Event | Topic | Data | Consumers |
|---|---|---|---|
| `DeviationRaised` (EV-06, `rwb.deviation.DeviationRaised.v1`) | `rwb.deviation.events.v1`, with `.retry` and `.dlt` | Case reference, deviation reference, code, raised-at, paused state, handler, contact-stop flag, **open count**, rule ID and version; CloudEvents envelope; no personal data | rwb-case, rwb-comms and rwb-reporting (connection matrix column S8) |
| `DeviationCleared` (EV-07, `rwb.deviation.DeviationCleared.v1`) | `rwb.deviation.events.v1`, with `.retry` and `.dlt` | Case reference, deviation reference, outcome, cleared-at, **open count**, the **return point** when the count is zero, rule ID and version; CloudEvents envelope; no personal data | rwb-case, rwb-comms and rwb-reporting (connection matrix column S8) |

The ids, the names and the topic are the Ownership Map and TSD S8 T5.3's; the hold properties are additive inside major version 1 and their element names are Not specified in the source documents (GAP-3102; ASM-5317). The record of the hold also rides `rwb.decision-record.v1` through the library (DP-03) and is not a business event of this service.

#### 12.4 Events consumed

| Event | Owner | Use |
|---|---|---|
| The case events of rwb-case; event names Not specified in the source documents (GAP-3102; ASM-5316) | P3 rwb-case | Keeps an open deviation aligned with the case it belongs to: a case that closes ends the open deviation with `CASE_ENDED`, and the count falls with it |

The S8 row of the connection matrix names an event subscription to P3 and none of its event names is published, so the consumer group is declared against the placeholder and faked. No other event is consumed.

#### 12.5 Workflows and activities

| Name | Type | Queue | Element |
|---|---|---|---|
| `DeviationWorkflow` | Workflow, one execution per case, started at any time, child of `CaseWorkflow`, parent close policy ABANDON, continues-as-new | `rwb-deviation` in namespace `rwb-recovery` | Unchanged; hosts the hold steps of the raise and the clear |
| `recordAndApplyDeviation` | Activity, the RecordAndApply step | `rwb-deviation` | The decision and the row in; the `deviation` row, the open count, the outbox row and the `DeviationRaised` payload out, one transaction |
| `releaseDeviationHold` | Activity, the clear step | `rwb-deviation` | The outcome in; the row update, the open count and the `DeviationCleared` payload with its return point out, one transaction |

The count is read inside each activity, so a raise and a clear that commit together still produce one exact number; no counter is kept outside the table (ASM-5318).

#### 12.6 Schedules

None. The Ownership Map gives S8 no job, and the holds are event-driven: no Temporal Schedule, no Quartz row and no batch table is created by this story.

#### 12.7 Tables owned

| Table | Owner | Use |
|---|---|---|
| `deviation` | S8, `rwb_deviation` | The record whose raise and clear move the hold, and the open count read from its `cleared_at` |
| `decision_record` | Platform library in `rwb_deviation` | The local record written before the row (DP-03) |
| `outbox_event` | Platform library in `rwb_deviation` | The two event rows relayed to the topic |
| `processed_event`, `idempotency_key` | Platform library in `rwb_deviation` | The inbox mark of a repeat and the stored answer |

`recovery_case`, `queue`, `assignment`, `decision_log_entry` and `rule_row` are other owners' and are named only; no foreign key leaves `rwb_deviation` (DP-01).

#### 12.8 Contract fakes

| Fake | Answer | Used by |
|---|---|---|
| rwb-integration placement fake (`RWB-P2-E2036-CON`) | A refused placement for a case with an open deviation, with MSG-P2-021 and its envelope; an accepted placement | AC2, AC8 |
| rwb-case case-router fake | Applies every hold it is given, holds while the count is above zero, lifts at zero and returns the case to its paused state; a case that closes | AC1 to AC3, X7 |
| rwb-case reference-data fake | The three lists at their version; an unavailable list | AC5 |
| rwb-access authorise fake | Case record right U held; refused | AC7 |
| Local decision-record stub | A healthy chain; a stopped chain | AC6 |
| Outbox relay stub | A relayed `DeviationRaised` and `DeviationCleared`; a duplicate delivery | AC5 |
| gateway-bff composite route fake | The merged hold banner and on-hold state of SCR-02 and SCR-07 for a synthetic case | Section 15 |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | None provided, none consumed | The two operations of the service are unchanged and owned by RWB-S8-E7001-APP; the placement contract is a build-against edge, not a call |
| Kafka | 2 published, 1 consumed | `DeviationRaised` and `DeviationCleared` on `rwb.deviation.events.v1`; the rwb-case case events; the record rides `rwb.decision-record.v1` through the library |
| Temporal | 1 workflow, 2 activities in this story | `DeviationWorkflow` with `recordAndApplyDeviation` and `releaseDeviationHold` on `rwb-deviation`; no Schedule |
| File | None | No file is read, built or delivered by this story |

### 13. Solution plan

**Deliverables.** The hold facts on the two published events, the open-count read, the handler and return point on the record, the record-first transaction, the inbox mark of a repeat, the one migration, the guard and list reads, and the hold banner answered through the composite route.

**Pattern application** (§R5.5)

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_deviation`; never read another service's tables | None |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H `RWB-PLT-E1027-CON` |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H `RWB-PLT-E1043-CON`; C `RWB-P3-E1043-CON` |
| DP-08 | RecoveryAccessGuard | Authorise contract of rwb-access and the guard library | H `RWB-PLT-E1037-CON`; C `RWB-P4-E1037-CON` |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H `RWB-PLT-TE006-CON` |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | None (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/deviation/v1` | None |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.deviation.events.v1`; naming library | H `RWB-PLT-E1047-CON` |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H `RWB-PLT-E1044-CON` |
| DP-19 | Screen, ace-web | gateway-bff composite route | H `RWB-PLT-N001-CON` |

The seven H rows and the two C rows the patterns add are held by the platform and service contract stories and are not repeated in the metadata rows, which carry only the legacy build-against contract as the plan gives it (GAP-3102; ASM-5321).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| DeviationHoldService | Service | The hold facts, the count and the return point of a raise and of a clear (BR3, BR5, BR6) |
| OpenDeviationCounter | Repository | The count of `deviation` rows of the case whose `cleared_at` is empty, inside the transaction |
| DeviationRepository | Repository | Reads and writes `deviation` with the optimistic lock version and the standard columns |
| EventOutboxWriter | Library use | Writes the two event rows with the hold element and the CloudEvents envelope (DP-09) |
| DecisionRecordWriter | Library use | Writes the record before the row, propagation MANDATORY (DP-03) |
| ReferenceDataClient | Client | Reads the three lists at their version; holds the act when a list cannot be read (DP-07) |
| AccessGuard | Library use | The Case record right of the raise and of the clear (DP-08) |

**Database.** One Flyway step in `rwb_deviation`: `CREATE INDEX ix_deviation_open_case ON deviation (case_id) WHERE cleared_at IS NULL`, so the count of a case's open deviations is cheap. It is not unique, because a case may hold more than one open deviation (FEAT-DVH-09; ASM-5327). No table, no column and no second migration.

**Build steps.** (1) Add the hold element and the count read to `recordAndApplyDeviation`. (2) Add `releaseDeviationHold` with the outcome and the return point. (3) Write the migration and the count query. (4) Wire the record-first transaction and the inbox dedupe. (5) Add the list and guard reads. (6) Prove the eight criteria and the eight exception paths on the fakes.

**Done when.** AC1 to AC8 pass at component level on the fakes, a second open deviation never lifts the hold, a repeat writes and publishes once, the boundary test shows no `rwb_case` statement, and the hold banner answers through the gateway-bff route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P2-021 | A placement is refused because the case has an open deviation (X6) | This case has an open deviation and stays with the deviation handler. |
| MSG-P7-003 | The decision record cannot be written before the change (X1) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | The role lacks the Case record right (X2) | You cannot {action} here. Your role does not include it. |
| MSG-GEN-001 | A required value is absent or outside its list (X3) | Enter {field}. |
| MSG-GEN-006 | A list cannot be read, when the platform answers with its envelope (X4) | Not specified in the source documents (GAP-3102; ASM-5317) |

The text is the legacy and FSD S8 wording, copied unchanged; MSG-P2-021 is the refusal the caller sees at the placement and it is the same sentence this story's hold reasons about, which is why RWB-P2-E2036-CON is the contract dependency. Thai text follows decision DL10.

### 15. Screens and states

No screen in this story (legacy §15). A case on hold appears in its queue on SCR-07 Team queues and in SCR-02 Case list with the on-hold banner of MSG-P3-004, and the decision log query SCR-38 shows the entry with the caller and the version; the banner and the state read this service's hold through the gateway-bff composite route, and the placement refusal carries MSG-P2-021 on the same route (DP-19; FSD S8 A2.2.4.2).

| State | What the user sees | Served by |
|---|---|---|
| On hold, count 1 or more | The banner naming the deviation code and the prescription date, the handler and "Contact stopped" where the code stops contact | The case, merged with this service's hold facts |
| Cleared at count zero, RETURNED | The case back in the state it paused in, no banner | The case on the return point this story publishes |
| Cleared at count zero, RE_ROUTED | The case in the route decision D6 with the re-decision pending | The case and rwb-valuation |
| Hold refused at the placement | The caller sees MSG-P2-021 and nothing moves | rwb-case, on the flag this story's hold set |

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-036-09 | AC1, AC2, AC3, AC8 (legacy AC9: a case with an open deviation stays with its handler) | Component | Case with X2 open in the deviation handler's queue; the hold, its count and the refusal |
| TC-E2-036-13 | AC7 (legacy access case) | Component | A role without the Case record right; 403 MSG-P4-002 |
| TC-E2-036-14 | AC6 (legacy Principle 5 case) | NFR | Decision-record write forced to fail; 503 MSG-P7-003; row, outbox and hold unchanged |
| TC-E2-036-01 | Legacy AC1, the placement half; proved by RWB-P3-E2036-APP and RWB-ITG-E2036-ITG | Component | Approved caller MDL-SYN-PRIORITY under SY-AGENT; NEW case |
| TC-E2-036-02 | Legacy AC2, the cap and the overflow; not this slice | Component | Owners at 150 and 149; then both at 150 |
| TC-E2-036-03 | AC6 (one decision record per act) | Component | One raise; record fields checked |
| TC-E2-036-04 | Legacy AC4, the flag; rwb-integration's | Component | Flag off |
| TC-E2-036-05 | Legacy AC5, the caller list; rwb-integration's | Component | Caller MDL-SYN-UNLISTED |
| TC-E2-036-06 | Legacy AC6, field validation; the placement's | Component | Request with no reason |
| TC-E2-036-07 | AC5 (a repeat writes once) | Component | Same raise and same clear delivered twice |
| TC-E2-036-08 | Legacy AC8, a closed case; rwb-case's | Component | CLOSED case |
| TC-E2-036-10 | Legacy AC10, an unknown queue or case; rwb-case's | Component | Queue ID that does not exist |
| TC-E2-036-11 | Legacy AC11, two placements at once; rwb-case's | Component | Two placements against one case version |
| TC-E2-036-12 | Legacy AC12, a case with an owner; rwb-case's | Component | IN_PROGRESS case with owner U-5100 |

The fourteen ids are the legacy cases of RWB-E2-036, carried in their legacy order: the deviation cases are re-pointed to this slice's criteria and the placement cases keep their legacy reference and name the slice that proves them, because the split gives this service the hold half of the key and gives the placement half to rwb-case and the end-to-end journey to RWB-ITG-E2036-ITG, which holds the `-ITG` copy of every case. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same id.

### 17. Guardrails

- No business value in code: the codes, the raised-by and outcome lists, the handler routing, the states and the messages stay reference data or rule rows read at their version.
- No personal data in the `deviation` row, the decision record, an event, a workflow input, a log or a prompt: identifiers, codes, instants, a count and a rule version only.
- ACE data and other services' facts only through their owners' contracts: no `v_ace_*` view, no ACE table and no other service's schema (DP-01, DP-11).
- One base, one topic, one queue and one login per service; this story adds no second topic, no Schedule and no operation (DP-13, DP-14).
- The decision record is written before the change and in its transaction; a failure rolls the row and the outbox back (DP-03).
- The count is read inside the transaction that changes the row, and a counter kept anywhere else is a defect.
- No hold leaves the service without a right, and no case, queue or assignment row is written here.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CWC-017 | A queue accepts a write from a model or an agent with the case and the reason | Business Requirements Epic 2, section 3.2 | FEAT-CWC-29 | All recovery processes | R-DEV-01 | TC-E2-036-09 |
| REQ-CWC-018 | A model or agent passes the same permission checks and its write is logged with its version | Business Requirements Epic 2, section 3.2 | FEAT-CWC-29 | All recovery processes | R-UNI-39 | TC-E2-036-13, TC-E2-036-14 |
| REQ-CWC-019 | The interface ships behind a feature flag | Business Requirements Epic 2, section 3.2 | FEAT-CWC-29 | All recovery processes | None | TC-E2-036-04 |
| REQ-CWC-020 | Model and rule work in the same queue, in one priority order | Business Requirements Epic 2, section 3.2 | FEAT-CWC-29 | All recovery processes | None | TC-E2-036-01 |
| REQ-ACA-010 | Agents run under service identities and are subject to the same role checks as people | Business Requirements Epic 2, section 3.2 | FEAT-CWC-29 | All recovery processes | CTL-09 | TC-E2-036-13 |

Legacy trace: story RWB-E2-036, module P2 Integration, feature FEAT-CWC-29, rules R-DEV-01 and R-UNI-39, control CTL-09. No legacy criterion is allocated to this slice; the twelve legacy criteria are proved by RWB-ITG-E2036-ITG and by the primary slices of the key, and the eight criteria of section 7 are new for the service change (GAP-3102; ASM-5326). The open items are the hold element names and the case-event names (GAP-3102).

| Source | What it supplies |
|---|---|
| FSD S8 Deviation handling v3 A2.1, A2.2, A2.4, A2.6, A2.9 and A1.4 | The flag, the pause, the routing to the named owner, the clear and the two-deviation rule |
| TSD S8 Deviation handling v2 T2, T3.0 to T3.3, T4, T5.3, T6.1 and T-A.1 | The record-first rule, the `deviation` columns and lists, the DEVIATION states, the two events and the rights |
| Business Rules and Routing Logic v4, DEV route set | R-DEV-01 to R-DEV-03, R-DEV-08, R-DEV-09 and R-DEV-18 |
| Context pack S8 and the connection matrix | The schema, base, topic, queue, the two events, the one owned table and the S8 row to P3 |
| RWB-P3-E2036-APP and RWB-P2-E2036-CON | The refuse-on-flag reading of the case and the refusal message the hold agrees with |
| Split plan, slice RWB-S8-E2036-APP | H, C, I, X, the lane, the wave, the release and the carried test ids (GAP-3102) |

### 19. Out of scope

- The placement command, the queue, the method, the cap, the overflow queue, the assignment, the decision entry of the placement and the refusal itself (rwb-case, RWB-P3-E2036-APP).
- The caller-facing admission, its replay, the approved callers list and the feature flag (rwb-integration, RWB-P2-E2036-CON and RWB-P2-E2036-APP).
- The Queue and allocation C answer and the matrix version (rwb-access, RWB-P4-E2036-APP); granting SY-AGENT the right in the production matrix is a matrix change under RWB-E1-037.
- The raise and the clear of a deviation as the X1 dispute journey, its evidence pack and its outcome screens (RWB-S8-E7001-APP).
- The other flows of the module: the X1 to X7 end-to-end journeys, the screening agent and its policy, the low-confidence review, the contact-breach path, the override review and the complaint-to-contact matching.
- The DEV package, its rule rows and their versions, and the central ledger (rwb-decision, P7).
- The schema and migration of `rwb_deviation` beyond the one index, the login, the deployment, the observability and the pipeline (the DB, INF and OPS stories of this legacy key).
- Any change to a legacy file, to a master or to built Epic 1 and Epic 2 code.
