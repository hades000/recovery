# RWB-S8-E7006-APP Run X6 lost contact and skip trace end to end

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S8-E7006-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-deviation |
| Service epic | RWB-SVC-S8 |
| Wave | 4 |
| Business epic | EP07 |
| Release | 31 May 2027 (tentative) |
| Legacy key | RWB-E7-006 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | L-S8-Q |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S8-E7006-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S8 rwb-deviation v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the application slice of RWB-E7-006 is realigned onto rwb-deviation (S8, service wave 2, business wave 4). The one legacy criterion the plan assigns to this slice (AC2) is kept word for word with its origin tag and only the `Given the <service> contract mock returns <x>` lines are added; AC1 belongs to the wave 4 harness. X6 is built as the always-on child of `CaseWorkflow` on task queue `rwb-deviation`: it evaluates R-DEV-01, R-DEV-06, R-DEV-16, R-DEV-17, R-DEV-18, R-DEV-19 and R-DEV-20 with the DEV package in force, dispatches the skip trace to rwb-agent, reads the internal contact data through rwb-source-data, writes the `deviation` row in `rwb_deviation`, records the decision through the local decision-record library before the row changes (DP-03), publishes `DeviationRaised` and `DeviationCleared` from the outbox, and answers the case move and the clock change to the parent. The two operations move onto `/api/recovery/deviation/v1` (DP-13) and the two screens are reached through the gateway-bff composite route (DP-19). TSD S8 T5.1 publishes no external interface for the bureau, the internal data or the agency, the plan's C row is empty although the skip trace crosses to rwb-agent, and the 30-day clock of R-DEV-17 is a durable timer (GAP-3061; ASM-5182 to ASM-5189). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-S8-E7006-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **case owner** — and as the step the FSD gives no primary person, because it runs unattended and the agent works the trace under policy — I want **the Workbench to run the skip trace through the bureau, internal data and agency sources and route on the result**, so that **every deviation has a handler and a clock**, and no case waits on a lost contact that nobody is working.

This story owns:

- the one legacy criterion of RWB-E7-006 that the plan assigns to this slice (AC2, verbatim with its origin tag), and the messages, the rule rows and the two screens it depends on;
- the X6 branch of `DeviationWorkflow` on task queue `rwb-deviation` in namespace `rwb-recovery`, started by the case router at any time as the child of `CaseWorkflow` (context pack slides 3 and 13; Temporal and Drools Design slide 13);
- the evaluation of R-DEV-01, R-DEV-06, R-DEV-16, R-DEV-17, R-DEV-18, R-DEV-19 and R-DEV-20 on an X6 of a case, plus R-UNI-12 when a new verified contact point arrives, against the DEV package version in force;
- the skip trace itself: the request dispatched to rwb-agent on its own queue, the internal contact data read from rwb-source-data, the answer that names the source of every contact point, and the 30-day clock of R-DEV-17;
- the `deviation` row in schema `rwb_deviation` with the columns of DF-CAS-036 to DF-CAS-045, its `state`, its `contact_stop` and its `outcome`;
- the decision record of the flag, the routing, the verified contact point and the exhausted trace, written through the local decision-record library **before** the row changes (DP-03);
- the publication of `DeviationRaised` and `DeviationCleared` on `rwb.deviation.events.v1` from the outbox;
- the stage outcome returned to rwb-case, carrying the rule ID, its version and the return point, on which the parent pauses the stage clock and resumes it, and the script never pauses the prescription clock;
- the two operations on base `/api/recovery/deviation/v1` (DP-13) and the read-only slices of SCR-08 and SCR-06 behind the gateway-bff composite route (DP-19).

It does not own: the published shapes, the `deviation` element, the skip-trace answer element, the error set and the fakes (RWB-S8-E7006-CON); the end-to-end journey of AC1 across the services and the wave 4 harness (the split plan assigns AC1 outside this slice, ASM-5188); the case of record, its route state, its assignment and its timers (rwb-case, P3); the agent runtime, its policy and its model (rwb-agent, P10); the internal contact data product and its freshness (rwb-source-data, P1); the bureau, the agency and the partner record (S9 rwb-partner and the outside systems); the DEV rule rows and their versions (rwb-decision, P7); the rights and the reference data (rwb-access, P4); and the schema, migration and deployment of this service (the DB, INF and OPS stories of this key).

### 2. Business rationale

The objective and the metric do not move: deviations closed within the service level, measured on the decision log and the Workbench records, reviewed monthly (FSD S8 A2.15.1). The FSD row that carries this feature is REQ-S8-004, "A lost contact case runs skip tracing and returns to a decision whether or not contact is restored", with REQ-DVH-011 for the flow end to end (FSD S8 Requirements served). The feature is FEAT-DVF-06, kind system, primary actor none, systems NCB, EFS and the Partner portal (FSD S8 A1.2, A2.15.2; Epics 3 to 8 Specification v3).

A borrower who cannot be reached is the quiet failure of a recovery case: the letters go to an address nobody reads, the clock runs down and the account arrives at the next decision untouched (FSD S8 A1.3). X6 is the code that stops that silence becoming a written-off account, and D-RCV-60 changes who owns each fact, not what the case owner gets.

- **The deviation record is this service's.** `deviation` is the one table the Ownership Map gives S8 and it lives in `rwb_deviation` (context pack ownership rows; TSD S8 T3.1). The X6 row is written here, and its status is the `state` column of the 9 DEVIATION states of TSD S8 T4.
- **The case stays with rwb-case (P3).** `recovery_case`, `assignment`, `queue` and `timer` are P3's, and the S8 row of the connection matrix gives S8 **events** from P3 and no REST row, so the stage clock pauses and resumes on the stage outcome the parent applies and this story writes no case and no timer row (context pack slide 13; ASM-5182).
- **The skip trace is the agent's work.** R-DEV-06 says "Agent handles within policy; a person approves an insurance claim", the connection matrix gives S8 a Temporal and event edge to rwb-agent and no other, so the trace is an activity dispatched to rwb-agent's queue and its answer is consumed on that owner's contract (ASM-5183). DP-20 would add `C RWB-P10-TE013-CON`; the plan's C row is empty, so the row is recorded as absent rather than invented.
- **The internal data is not this service's.** R-UNI-12 names EFS, Workbench and NCB and R-DEV-16 names Workbench and NCB; the contact data product is P1's, read on its REST contract, the one REST edge the matrix gives S8 (ASM-5184).
- **The bureau and the agency have no published interface.** FSD S8 A2.15.2 lists NCB, EFS and the Partner portal as integration points, while TSD S8 T5.1 publishes **None**, the `partner` row of DF-PRT-001 to DF-PRT-007 belongs to S9 and the matrix gives S8 no row to S9 or to P2. Their answers therefore arrive inside the skip-trace answer with the placeholder, and no partner row is read here (GAP-3061; ASM-5184).
- **The decision is recorded first**, in the same transaction as the deviation change: that is what TSD S8 T2 states and what legacy AC2 tests (DP-03).
- **The clocks are two.** R-DEV-01 pauses the stage clock and never the prescription clock, R-DEV-18 resumes it at the return point, and R-DEV-17's 30 days is a durable timer of the workflow, not a Schedule (context pack slide 8; ASM-5186).
- **The event leaves from the outbox**, on the one topic of the service, with rwb-case and rwb-reporting among its listeners (context pack topic and connection matrix column S8; ASM-5185).

No business value moves: the deviation codes, the raised-by codes, the outcome codes, the 30-day clock, the 10-working-day escalation and the deviation service level that DL22 sets stay reference data or rule rows read with their version, never a constant of the code (ASM-5189).

### 3. Preconditions

- RWB-S8-E7006-CON is published and tagged: the X6 element use of `deviation`, the three state values it writes, the skip-trace answer element, the consumed rows, the error set and the fakes are baselined and handed to this story (H).
- RWB-PLT-E1027-CON is published with its writer stub: the local decision-record library joins the caller's transaction and a failed write stops the action with MSG-P7-003 (DP-03; H).
- RWB-PLT-N001-CON is published: SCR-08 Deviation queue and SCR-06 Raise deviation reach this service through the gateway-bff composite route, one hop each, and no screen calls a service directly (DP-19; H).
- `deviation` exists in `rwb_deviation` from the DB story of this service with the columns of DF-CAS-036 to DF-CAS-045 and the standard record columns of TSD S8 T3.0; this story adds no table, no column and no migration.
- The DEV rule package is in force at its version with R-DEV-01, R-DEV-06, R-DEV-16, R-DEV-17, R-DEV-18, R-DEV-19, R-DEV-20 and R-UNI-12; it is authored, tested and approved in rwb-decision (P7) and only loaded and evaluated here.
- The rwb-case workflow boundary is available for the fake: the case reference, its route state and its `paused_state` arrive as child-workflow input, and the outcome is the child result the parent applies. No source publishes a REST operation that moves a case state or pauses a timer on behalf of a stage (ASM-5182).
- The rwb-agent skip-trace contract is published with its fake: the request and the answer that names the source of each contact point, the exhausted answer, and the 2 s activity budget; its operation name and its element are Not specified in the source documents (GAP-3061; ASM-5183).
- The rwb-source-data internal-contact-data read is published with its fake, on the data-product contract with its freshness stamp; the bureau (NCB) and agency (Partner portal) answers carry the placeholder, because TSD S8 T5.1 publishes no interface and the matrix gives S8 no row to P2 or S9 (GAP-3061; ASM-5184).
- The data product the module reads carries today's business date, or shows its date as stale and holds the action (VR-S8-015-1; MSG-P1-001).
- The service runs as its own login on `rwb_deviation` and holds no grant on another `rwb_*` schema and no `v_ace_*` grant, so a statement on `rwb_case`, on `rwb_agent`, on `partner` or on a `recovery.v_ace_*` view is refused by the database and fails the boundary test (DP-01, DP-05).
- No approval is needed to build against a Draft contract baseline; the contract is tagged by RWB-S8-E7006-CON when its tests pass.

### 4. Flow

1. X6 is raised on a case from the screening agent of E2, from an officer on SCR-06, or by R-UNI-12 when a new verified contact point arrives on an open X6. The caller sends `POST /cases/{caseId}/deviations` on `/api/recovery/deviation/v1` with `deviation_code` X6, `raised_by`, `paused_state` and the reason, one `Idempotency-Key` per raise (API-S8-001).
2. The handler signals the case's `DeviationWorkflow` on queue `rwb-deviation`; it never writes a table or a case row on the request thread.
3. `evaluateDeviationRules` loads the DEV package version in force and evaluates R-DEV-01: the deviation is flagged, the stage clock is paused, the prescription clock keeps running and the deviation routes to its named owner. R-DEV-06 then moves X6 to `DEV_WITH_OWNER`, where the agent handles within policy and the case owner stays accountable.
4. `recordAndApplyDeviation` writes one decision record through the local library **before any change**: case reference, deviation reference, rule ID with the package version, inputs reference, the outcome and the decided-at time (DP-03; TSD S8 T2).
5. In the same `rwb_deviation` transaction the activity inserts the `deviation` row: `id`, `case_id`, `deviation_code` X6 of `LOV-DEVIATION`, `raised_at`, `raised_by` of `LOV-RAISED-BY`, `paused_state`, `handler_user_id` the case owner, `contact_stop`, `cleared_at` and `outcome` empty, and `state` = `DEV_WITH_OWNER`.
6. The outbox publishes `DeviationRaised` in that transaction, with identifiers, the code, the raised-at instant, the contact-stop flag and the rule version, and no personal data.
7. The step returns the stage outcome to the parent: the deviation reference, the return point, the rule IDs with their versions and `CLOCK_PAUSE`. rwb-case pauses the stage timer and moves the case; the prescription timer is not touched (context pack slide 8).
8. `runSkipTrace` dispatches the trace to rwb-agent's queue with the case reference, the deviation reference and the trace window, and waits on the activity's durable timer. rwb-agent works the bureau, the internal data and the agency; this service reads none of them directly (ASM-5183, ASM-5184).
9. `readContactData` reads the internal contact data product of the case from rwb-source-data on its contract, one hop and 2 s, and records the freshness stamp with the answer; a stale product holds the step (VR-S8-015-1).
10. **A contact point is verified.** R-DEV-16 closes X6 and returns the case to the `paused_state`; R-DEV-18 resumes the stage clock. `PATCH /deviations/{deviationId}` is answered with the `Deviation` in `DEV_RESOLVED`, `cleared_at`, `outcome` and the source of the contact point, and `DeviationCleared` is published from the same transaction.
11. **The trace is exhausted.** R-DEV-17 routes to escalation or to the route decision inside its 30-day clock, `state` becomes `DEV_REROUTE`, and R-DEV-19 reopens the route decision D6 in rwb-valuation with the segment recomputed and the hard gates re-run; where the trace produced nothing at all, the case goes to escalation with the breach recorded. `DeviationCleared` is published with the same envelope (ASM-5186).
12. Beyond the deviation service level in `DEV_WITH_OWNER`, R-DEV-20 escalates to the team manager and reports the breach at 10 working days; the deviation service level itself is set with DL22 and no source publishes its value (ASM-5189).
13. A repeated raise or a repeated advance with the same case and `Idempotency-Key` answers the record it already wrote, writes nothing, publishes no second event and counts the repeat (R-UNI-40).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The local decision record cannot be written | Nothing changes: no `deviation` row, no event, no stage outcome and no clock change, and the case does not pause | MSG-P7-003 | AC2, TC-E7-006-02, TC-E7-006-04 |
| X2 | The role lacks the Case record right of the raise or of the advance | 403 before any change and before any decision record; the unattended step runs under the service identity with the same check | MSG-P4-002 | AC2, TC-E7-006-03 |
| X3 | A required value is absent or invalid: the code, the raised-by, the paused state or the outcome | The request is refused with the field named and nothing is written | MSG-GEN-001 | AC2 |
| X4 | The data product behind the contact data is stale after a late or failed ACE batch | The step holds, writes nothing and shows the product and its date | MSG-P1-001 | AC2 |
| X5 | The skip-trace answer does not arrive inside its budget, or its breaker is open | The deviation stays open at `DEV_WITH_OWNER`, the 30-day clock keeps running, the trace is shown as unavailable and the step does not retry inside itself | None (platform 503 envelope) | AC2 |
| X6 | An X6 is already open on the case | One open X6 per case: the repeat is counted, no second row and no second event | None | AC2 |
| X7 | The advance names no next step, or the trace answer names a source with no verified contact point | Nothing closes: the deviation stays at `DEV_WITH_OWNER` and the unmapped outcome is recorded for the case owner | None | AC2 |
| X8 | A component, a statement or a test reaches a `v_ace_*` view, a `rwb_case` row, a `partner` row or another service's schema | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | Section 17, BR3, BR5 |

X1 to X3 are the paths RWB-E7-006 and its FSD exception rows carry; X4 to X7 are the paths the target call types, the agent dispatch, the 30-day clock and the container add; X8 is the DP-01 and DP-05 boundary.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-S8-E7006-CON, the decision-record stub, the gateway-bff fake, the rwb-case workflow fake and the agent and data-product fakes, on its own schema, and needs no live P1, P3 or P10 |
| Negotiable | The activity names, the decision code per rule and the shape of the stage outcome are this story's choice; the rules, the messages, the screens, the two operations and the `deviation` columns are fixed |
| Valuable | A lost contact stops the stage clock the day it is found, is worked through every source the bank has, and ends in a verified contact point or in a route decision, with the legal clock intact |
| Estimable | One workflow branch, four activities, one agent dispatch, two event publications, two operations, two screen fragments and the access and failure tests |
| Small | Finished inside two weeks with its tests on the fakes |
| Testable | Every path runs on synthetic cases through the contract fakes, plus the verified, the exhausted, the access and the forced record-write failure cases |

### 7. Acceptance criteria

```gherkin
Feature: Run X6 lost contact and skip trace end to end

  Background:
    Given the DEV rule package is in force at its version and carries R-DEV-01, R-DEV-06, R-DEV-16 and R-DEV-17
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC2 Not recorded (legacy RWB-E7-006 AC2)
    Given the rwb-deviation contract mock returns deviation "DEV-2027-001206" of code "X6" on case "RW-2027-001206" in state "DEV_WITH_OWNER" with the case owner as handler
    Given the rwb-decision contract mock returns the decision log store unavailable for the entry of "DEV-2027-001206"
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

AC2 is the criterion of RWB-E7-006 word for word: `the decision log cannot be written`, `the action is taken`, `nothing changes` and `the user sees MSG-P7-003` all stand, and the only additions are the two mock lines that stand in for the contract this service publishes and for the decision log it does not own. On this story "the action" is either the raise through `POST /cases/{caseId}/deviations`, the advance through `PATCH /deviations/{deviationId}`, or the answer the agent's trace produces: all three write the decision record first, so all three change nothing when the record cannot be written, and none leaves a deviation row, a contact stop, an event or a paused clock behind (DP-03).

AC1 of RWB-E7-006 is not copied here: the split plan gives this slice AC2 only, so the happy path of X6 across the services is proved by RWB-ITG-E7006-ITG and its harness (ASM-5188). The case number and the deviation reference in the mock lines are synthetic test data and no source value (section 16).

### 8. Business rules

| Rule | Route set | Codes | From state | Event | Condition | Action | To state | Owner | Systems | Timer |
|---|---|---|---|---|---|---|---|---|---|---|
| R-DEV-01 | Deviations | X1 to X7 | ANY_STATE | DEVIATION_FLAGGED | deviation_code in (X1..X7) | Pause the stage clock, keep the prescription clock running, route to the named owner | DEV_FLAGGED | Workbench | Workbench, the Workbench document hub | same day |
| R-DEV-06 | Deviations | X1 to X7 | DEV_FLAGGED | OWNER_ASSIGNED | deviation_code in (X6,X7) | Agent handles within policy; a person approves an insurance claim | DEV_WITH_OWNER | Agent, case owner | Workbench | None |
| R-DEV-16 | Deviations | X1 to X7 | DEV_WITH_OWNER | CONTACT_RESTORED | deviation_code = X6 and a contact point is verified | Close X6 and return to the paused state | DEV_RESOLVED | Case owner | Workbench, NCB | None |
| R-DEV-17 | Deviations | X1 to X7 | DEV_WITH_OWNER | CONTACT_NOT_FOUND | deviation_code = X6 and skip trace exhausted | Route to escalation or to the route decision | DEV_REROUTE | Case owner | Workbench | 30 days |
| R-DEV-18 | Deviations | X1 to X7 | DEV_RESOLVED | CLOCK_RESUMED | Any | Resume the stage clock and return the case | RESUMED | Previous owner | Workbench | None |
| R-DEV-19 | Deviations | X1 to X7 | DEV_REROUTE | ROUTE_REOPENED | Any | Recompute the segment and re-run the hard gates | ROUTE_D6 | Case owner | Workbench | None |
| R-DEV-20 | Deviations | X1 to X7 | DEV_WITH_OWNER | SLA_BREACHED | time in DEV_WITH_OWNER exceeds the deviation service level | Escalate to the team manager and report the breach | DEV_WITH_OWNER | Team manager | Workbench | 10 working days |
| R-UNI-12 | Universal rules | All | ANY_ACTIVE | CONTACT_DETAIL_CHANGED | a new verified contact point arrives | Update the contact data product, close X6 if it is open | RESUME_STATE | Workbench | EFS, Workbench, NCB | same day |

The eight rows are the rows of the Business Rules and Routing Logic v4, copied character for character. The owner column is a business role, not a service: the states are the `deviation.state` of this service, the route states of the case are rwb-case's, the DEV package and its versions are rwb-decision's, "NCB" and "EFS" are outside systems and the internal data product, and "the Workbench document hub" is rwb-document (P5) for the documents R-DEV-01 needs. R-DEV-02 to R-DEV-05, R-DEV-07 to R-DEV-15 and R-DEV-21 to R-DEV-22 belong to the other codes of this service and are not built here; FSD S8 A2.15.3.1 prints VR-S8-015-1 and BR-S8-015 for this feature and prints no rule row, so the rules are taken from the rule workbook (GAP-3061).

| ID | Rule | Source |
|---|---|---|
| BR1 | `deviation` is this service's: its code, raise facts, paused state, handler, contact stop, outcome and state are columns of `deviation` in `rwb_deviation`, and no other service writes them | Context pack ownership rows; TSD S8 T3.1 |
| BR2 | The decision is recorded before the deviation row changes, with the rule ID and the package version in force; a failed write changes nothing and the caller sees MSG-P7-003 | DP-03; TSD S8 T2; legacy AC2 |
| BR3 | The case, its assignment, its queue and its timers stay with rwb-case: the stage clock is paused and resumed by the parent on this story's outcome, and no `recovery_case` or `timer` row is written here | Context pack connection matrix row S8; slide 13; ASM-5182 |
| BR4 | One clock rule: R-DEV-01 pauses the stage clock and never the prescription clock, and the case returns to the state it paused in | Context pack slide 8; R-DEV-01, R-DEV-16, R-DEV-18 |
| BR5 | The bureau, the internal data and the agency are never read directly: no `v_ace_*` view, no ACE table, no `partner` row and no agency file is read here, and every answer arrives on the owner's contract | DP-05, DP-11; TSD S8 T5.1; ASM-5183, ASM-5184 |
| BR6 | The skip trace is one dispatch per open X6 and one answer: the agent works it under policy and this service never re-runs a trace whose answer is in hand | R-DEV-06; ASM-5183 |
| BR7 | Two outcomes close the code: a verified contact point under R-DEV-16 inside the 30-day clock of R-DEV-17, or the exhausted trace that routes to escalation or to D6; no third path exists and no outcome is invented | R-DEV-16, R-DEV-17, R-DEV-19; FSD S8 A2.15 |
| BR8 | One event per raise and one per clear, published from the outbox in the transaction of the row, with identifiers, codes, the contact-stop flag and the rule version only | Context pack topic; connection matrix; ASM-5185 |
| BR9 | The same raise twice, or the same `Idempotency-Key` twice, writes once, publishes once and answers one record | R-UNI-40; TSD S8 T-A.2 |
| BR10 | No person name, contact value, address, account number or identity number enters `rwb_deviation`, the decision record, a log, a workflow input or an event; a contact point is carried as a reference and a source code, never as a value | Template and Rules v1 §R7.2 s17 |

### 9. State transitions

The case route state is rwb-case's and this story does not change it: the step returns the outcome and the parent applies it (BR3). What this story owns is the `deviation.state` of the X6 record it writes, over the 9 DEVIATION states of TSD S8 T4.

| From (`deviation.state`) | Event | Condition | To |
|---|---|---|---|
| No row | DEVIATION_FLAGGED | `deviation_code` = X6 and the record is written | DEV_FLAGGED, then DEV_WITH_OWNER on OWNER_ASSIGNED (R-DEV-01, R-DEV-06) |
| DEV_WITH_OWNER | CONTACT_RESTORED | A contact point is verified inside the trace window | DEV_RESOLVED, then RESUMED on CLOCK_RESUMED (R-DEV-16, R-DEV-18) |
| DEV_WITH_OWNER | CONTACT_NOT_FOUND | The skip trace is exhausted inside the 30-day clock | DEV_REROUTE, then ROUTE_D6 on ROUTE_REOPENED (R-DEV-17, R-DEV-19) |
| DEV_WITH_OWNER | CONTACT_NOT_FOUND | The trace produced nothing and the case goes to escalation | DEV_REROUTE with the escalation recorded (R-DEV-17) |
| DEV_WITH_OWNER | SLA_BREACHED | Time in DEV_WITH_OWNER exceeds the deviation service level | Unchanged, escalated to the team manager with the breach reported (R-DEV-20) |
| Any active | CONTACT_DETAIL_CHANGED | A new verified contact point arrives on an open X6 | DEV_RESOLVED, then RESUMED (R-UNI-12, R-DEV-16) |
| Any | The same raise again | The case and the code already hold an open X6 | Unchanged; the repeat is counted and no event leaves (R-UNI-40) |

| Step execution | Event | Condition | To |
|---|---|---|---|
| Waiting | A raise arrives for a case | The package in force is loaded | Evaluating |
| Evaluating | R-DEV-01 and R-DEV-06 fire | The decision record is written | Applying |
| Applying | The row and the outbox row are written and the outcome returned | The transaction commits | Tracing |
| Applying | The record write or the transaction fails | X1 | Waiting, nothing changed, MSG-P7-003 |
| Tracing | `runSkipTrace` is dispatched and `readContactData` answers | The answer names a source and a verified contact point, or the trace is exhausted | Resolving |
| Tracing | The answer is late, or the clock of R-DEV-17 runs out | X5, or the 30-day timer fires | Resolving on the outcome that exists |
| Resolving | R-DEV-16, R-DEV-17, R-DEV-18 or R-DEV-19 fire and `DeviationCleared` is relayed | The transaction commits | Closed |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| None; runs unattended | The primary actor of FSD S8 A2.15.3.3: the raise, the trace dispatch and the clock are started by the system |
| Case owner (RW-CASEOWN) | Holds CRU on the case record (TSD S8 T6.1), holds the case through the pause and closes or reroutes it under R-DEV-16 and R-DEV-17 |
| Team manager (RW-TEAMMGR) | Holds R and receives the escalation and the breach report of R-DEV-20 |
| Conduct and QA officer (RW-CONDUCT) | Holds R and reads the deviation and its decision record |
| rwb-case (P3) | Owns the case of record, its assignment, its queues and its timers, and applies the stage outcome this story returns |
| rwb-agent (P10) | Owns the skip trace, its policy and its model, and works the bureau, the internal data and the agency under R-DEV-06 |
| rwb-source-data (P1) | Owns the internal contact data product and its freshness stamp |
| rwb-decision (P7) | Owns the DEV package, its rule rows and their version; this story only evaluates them and records the outcome |
| rwb-access (P4) | Owns the roles and the capability rights this story checks through the guard |

The FSD records no primary role and the case owner as a secondary user (FSD S8 A2.15.3.3), and the legacy permission table gives Case record right U to RW-CASEOWN, RW-RESTRUCT, RW-SPECIAL, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-ENFORCE, RW-SALEOFF and 4 more. No delegated authority limit applies: X6 takes no credit decision, and the one approval in the module that touches X6 is the insurance claim of X7, which is not this story's.

### 11. Data

| BR Field ID | Table | Owner | Use in this story |
|---|---|---|---|
| DF-CAS-036 to DF-CAS-045 | `deviation` | S8, `rwb_deviation` | **Write**, one row per X6: `id`, `case_id`, `deviation_code`, `raised_at`, `raised_by`, `paused_state`, `handler_user_id`, `contact_stop`, `cleared_at`, `outcome`, plus `state` and the standard columns of TSD S8 T3.0 |
| None: library table | `decision_record` | Platform library in `rwb_deviation` | The hash-linked record written before the row (DP-03) |
| None: library table | `idempotency_key`, `outbox_event` | Platform library in `rwb_deviation` | The raise and advance keys with their answers, and the two event rows relayed to the topic |
| DF-CAS-001 to DF-CAS-023 | `recovery_case` | P3 rwb-case | The case reference, its route state and its `paused_state`; consumed on the workflow boundary and its events, never written |
| DF-WRK-009 to DF-WRK-016, DF-WRK-027 to DF-WRK-036 | `assignment`, `timer` | P3 rwb-case | The handler assignment, the stage clock and the prescription clock; named, never written (ASM-5182) |
| DF-DEC-001 to DF-DEC-018 | `decision_log_entry` | P7 rwb-decision | The central ledger; the record of DP-03 is copied to it by rwb-decision, not written here |
| DF-REF-001 to DF-REF-015 | `rule_row` | P7 rwb-decision | The DEV package rows and their versions; read through the package, never written |
| DF-PRT-001 to DF-PRT-007 | `partner` | S9 rwb-partner | The agency record the trace may use; **not read as a table** here, and its read carries the placeholder (GAP-3061; ASM-5184) |
| No field IDs published | the skip-trace answer of rwb-agent | P10 rwb-agent | The source of each contact point, the verified flag and the trace window; the element is Not specified in the source documents (GAP-3061; ASM-5183) |

The owned row writes the ten fields of DF-CAS-036 to DF-CAS-045 and no personal data: `case_id` and `handler_user_id` are identifiers of other services' facts, and no customer name, contact value or address is copied into `rwb_deviation` (BR10). The three lists are those of TSD S8 T3.2 — `LOV-DEVIATION` with X1 to X7, `LOV-RAISED-BY` with SCREENING_AGENT, RULE, OFFICER and CUSTOMER_CONTACT, and `LOV-DEV-OUTCOME` with RETURNED, RE_ROUTED and CASE_ENDED — and every one of them is reference data read at its version, never a constant.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-deviation (S8); base `/api/recovery/deviation/v1` (DP-13). Both rows are the operations the Ownership Map gives this service, and X6 uses both; the queue read is not published by this service.

| Method | Path | Shape | Access | Idempotency |
|---|---|---|---|---|
| POST | `/cases/{caseId}/deviations` | `DeviationRequest` in, `Deviation` out (API-S8-001) | Case record, right U, scope applied | `Idempotency-Key` header |
| PATCH | `/deviations/{deviationId}` | `DeviationOutcome` in, `Deviation` out (API-S8-002) | Case record, right U, scope applied | Not applicable |

Both answer 400, 401, 403 with MSG-P4-002, 404, 409, 422 with MSG-GEN-001 and 503, each in the platform error envelope; the exact status list and the shapes are RWB-S8-E7006-CON's. The POST is the raise and the PATCH is the advance that carries the verified contact point or the exhausted trace.

#### 12.2 REST operations consumed

| Operation | Owner | Use |
|---|---|---|
| The internal contact data read of the case; operation name Not specified in the source documents (GAP-3061; ASM-5184) | P1 rwb-source-data | The internal data of the trace: the contact data product of the case with its source and its freshness stamp; faked on Day 1 |
| The case state, the return point and the clock change; operation name Not specified in the source documents (GAP-3061; ASM-5182) | P3 rwb-case | Consumed on the child-workflow input and the stage outcome, not on a REST row, because the matrix gives S8 events from P3 and no REST edge; faked |
| The skip trace of the case; element and operation Not specified in the source documents (GAP-3061; ASM-5183) | P10 rwb-agent | An activity dispatched to rwb-agent's queue `rwb-agent` under the rwb-agent contract of DP-20; the bureau, the internal data and the agency are worked inside it; faked |
| The agency record of the trace; operation and owner Not specified in the source documents (GAP-3061; ASM-5184) | S9 rwb-partner, or the agency's own interface | Not reachable: TSD S8 T5.1 publishes no external interface and the matrix gives S8 no row to S9 or to P2; the placeholder stands and the answer is read inside the trace answer only |

Each row is one hop with a 2 s budget and a breaker, and none retries inside the step (DP-11, ADR-020). Only the first row is a REST edge of the connection matrix; the others are the workflow boundary, the agent activity and a read no source publishes (ASM-5182, ASM-5183, ASM-5184).

#### 12.3 Events published

| Event | Topic | Data | Consumers |
|---|---|---|---|
| `DeviationRaised` (EV-06, `rwb.deviation.DeviationRaised.v1`) | `rwb.deviation.events.v1`, with `.retry` and `.dlt` | Case reference, deviation reference, code X6, raised-at, paused state, contact-stop flag, rule ID and version; CloudEvents envelope; no personal data | rwb-case and rwb-reporting (connection matrix column S8) |
| `DeviationCleared` (EV-07, `rwb.deviation.DeviationCleared.v1`) | `rwb.deviation.events.v1`, with `.retry` and `.dlt` | Case reference, deviation reference, outcome (`CONTACT_RESTORED` or `CONTACT_NOT_FOUND`), the source code of the contact point, cleared-at, rule ID and version; CloudEvents envelope; no personal data | rwb-case and rwb-reporting (connection matrix column S8) |

The ids are the two events the Ownership Map gives S8 and their names are the two TSD S8 T5.3 publishes; the pairing of id to name is recorded as ASM-5185. The topic is the one naming rule of the context pack and DP-14 applies, although the plan's pattern set for this key does not carry it (ASM-5185).

#### 12.4 Events consumed

| Event | Owner | Use |
|---|---|---|
| The case events of rwb-case; event names Not specified in the source documents (GAP-3061; ASM-5182) | P3 rwb-case | Keeps an open X6 aligned with the case it belongs to: the case router forwards a case move to the running child, a case that leaves its stage ends the open X6 with the outcome it holds, and a contact change raises R-UNI-12 |

The S8 row of the connection matrix names an event subscription to P3 and none of its event names is published, so the consumer group is declared against the placeholder and faked (ASM-5182). No other event is consumed; the case router itself is rwb-case's.

#### 12.5 Workflows and activities

| Name | Type | Queue | Element |
|---|---|---|---|
| `DeviationWorkflow` | Workflow, one execution per case, started at any time, child of `CaseWorkflow`, parent close policy ABANDON, continues-as-new | `rwb-deviation` in namespace `rwb-recovery` | Hosts the X6 branch; its input, its signals and its stage outcome to the parent |
| `evaluateDeviationRules` | Activity, the EvaluateRules step | `rwb-deviation` | The case reference, the code and the paused state in; rule ID, package version and decision out |
| `recordAndApplyDeviation` | Activity, the RecordAndApply step | `rwb-deviation` | The decision in; the `deviation` row, the outbox rows and the stage outcome out, one transaction |
| `runSkipTrace` | Activity dispatched to rwb-agent's queue | `rwb-agent` | The case reference, the deviation reference and the trace window in; the source of each contact point, the verified flag and the answer's reference out (ASM-5183) |
| `readContactData` | Activity, the internal-data read | `rwb-deviation` | The case reference in; the contact data product of the case with its freshness stamp out (ASM-5184) |
| `resolveDeviation` | Activity, the outcome step | `rwb-deviation` | The verified point or the exhausted answer in; the row update, `DeviationCleared`, the return point and the clock change out |
| `traceClock` | Durable timer of the workflow, the 30 days of R-DEV-17, not an activity and not a Schedule | `rwb-deviation` | The window of the reference data with its version; the expiry is the event `CONTACT_NOT_FOUND` |

The stage outcome carries the case reference, the deviation reference, the return point, the rule IDs with their versions and one of `CLOCK_PAUSE`, `CLOCK_RESUME` or `ROUTE_D6`; the parent applies it to the case and its timers (ASM-5182). The activity names are a target design choice fixed by no source document.

#### 12.6 Schedules

None. The Ownership Map gives S8 no job and X6 is started by an event, a signal or a contact change, never by a clock of its own; the 30 days of R-DEV-17 and the 10 working days of R-DEV-20 are durable Temporal timers inside `DeviationWorkflow`, not Schedules, and this story declares no Quartz row, no shared job table and no batch table (ASM-5186).

#### 12.7 Tables owned

| Table | Owner | Use |
|---|---|---|
| `deviation` | S8, `rwb_deviation` | The X6 record: its code, raise facts, paused state, handler, contact stop, outcome and state |
| `decision_record` | Platform library in `rwb_deviation` | The local record written before the row (DP-03) |
| `idempotency_key` | Platform library in `rwb_deviation` | The raise and advance keys and the answers they hold |
| `outbox_event` | Platform library in `rwb_deviation` | The `DeviationRaised` and `DeviationCleared` rows relayed to the topic |

`recovery_case`, `assignment`, `timer`, `decision_log_entry`, `rule_row`, `partner` and every `v_ace_*` view are other owners' and are named only; no foreign key leaves `rwb_deviation` (DP-01).

#### 12.8 Contract fakes

| Fake | Answer | Used by |
|---|---|---|
| rwb-case workflow fake | The case in `WITH_FCR_OFFICER` with its prescription date; an accepted `CLOCK_PAUSE`, `CLOCK_RESUME` and `ROUTE_D6`; a refused outcome; a case-closed event | AC2, X6, X7 |
| rwb-agent trace fake | A verified contact point from each of the three sources, an exhausted trace, and an answer that does not arrive inside its budget; the element carries the placeholder (GAP-3061; ASM-5183) | AC2, X5 |
| rwb-source-data data-product fake | The contact data product with a fresh stamp and with a stale stamp | AC2, X4 |
| rwb-decision package fake | The DEV package at its version with the eight rules of section 8 | AC2 |
| Local decision-record stub (`RWB-PLT-E1027-CON`) | A healthy chain and outbox; a stopped chain | AC2 |
| Outbox relay stub (`RWB-PLT-TE006-CON`) | A relayed `DeviationRaised` and `DeviationCleared`; a relay that fails and retries | AC2 |
| gateway-bff composite route fake | The merged SCR-08 and SCR-06 answer for a synthetic case | AC2 |

The fakes are test-only and are replaced by the real services in SIT. The trace element, the consumed operation names and the agency read carry the placeholder until their owners confirm them (GAP-3061; ASM-5183, ASM-5184).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 1 consumed | `POST /cases/{caseId}/deviations` and `PATCH /deviations/{deviationId}` on `/api/recovery/deviation/v1`; the rwb-source-data internal-data read; one hop, 2 s |
| Kafka | 2 published, 1 consumed | `DeviationRaised` and `DeviationCleared` on `rwb.deviation.events.v1`; the rwb-case case events; the decision record rides the library's `rwb.decision-record.v1` and is not this service's event |
| Temporal | 1 workflow, 5 activities, 1 dispatched activity and 1 durable timer | `DeviationWorkflow` with `evaluateDeviationRules`, `recordAndApplyDeviation`, `runSkipTrace` (on `rwb-agent`), `readContactData` and `resolveDeviation`, and the 30-day `traceClock`; no Schedule |
| File | None | No file is read, built or delivered by this story |

### 13. Solution plan

**Deliverables.** The X6 branch of `DeviationWorkflow` with its activities and its durable timer, the evaluator against the DEV package version, the decision-record writer, the `deviation` insert and update with their outbox and idempotency rows, the two publishers, the stage outcome with the clock change, the two write handlers on the target base and the two read-only screen fragments.

**Pattern application** (§R5.5)

| DP | Legacy marker | Pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H `RWB-PLT-E1027-CON` |
| DP-13 | `/api/recovery/v1` | `/api/recovery/deviation/v1` | None |
| DP-19 | Screen, ace-web | gateway-bff composite route | H `RWB-PLT-N001-CON` |

DP-03 is the transaction rule of the step: the record and the row commit together or not at all, and legacy AC2 is its proof. DP-13 moves the base of the two operations and nothing else. DP-19 puts SCR-08 and SCR-06 behind the composite route. DP-09, DP-14 and DP-20 are not in the pattern set of this key although the two published events need the outbox library, the topic naming rule applies and the trace crosses to rwb-agent; all three are recorded as absent rather than added to the metadata (ASM-5183, ASM-5185).

**Build steps.** (1) Wire the `DeviationWorkflow` branch and its activities on `rwb-deviation`. (2) Load the DEV package version and evaluate R-DEV-01 and R-DEV-06. (3) Write the decision record first and insert the `deviation` row with its outbox rows and its idempotency row in one transaction. (4) Publish `DeviationRaised` and return the clock-pause outcome. (5) Dispatch `runSkipTrace` to `rwb-agent` and `readContactData` to rwb-source-data, with their budgets and breakers. (6) Implement the two outcomes: R-DEV-16 with R-DEV-18, and R-DEV-17 with R-DEV-19, publishing `DeviationCleared`. (7) Add the 30-day `traceClock`, the R-DEV-20 escalation and the R-UNI-12 contact change. (8) Add the two write handlers on the target base and the two screen fragments. (9) Prove AC2 and the eight exception paths on the fakes.

**Feature flag.** `rwb.deviation.x6-skip-trace-v1`, a flag of the platform library; off means X6 is raised and paused as before but no trace is dispatched, the case stays at `DEV_WITH_OWNER` with its 30-day clock, and no other code is affected.

**Done when.** AC2 passes at component level on the fakes, a verified contact point closes X6 and resumes the stage clock, an exhausted trace reroutes the case, a repeated raise writes once and publishes once, a forced record failure changes nothing, the boundary test shows no `v_ace_*` read, no `rwb_case` statement, no `partner` row and no second topic, and the two screens answer through the gateway-bff route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S8-001 | The raise succeeds and the case moves to its handler (SCR-06 saved) | {deviation} was raised. The case is with {handler}. |
| MSG-GEN-001 | A required value of the raise or of the advance is absent or invalid (X3) | Enter {field}. |
| MSG-P4-002 | The role lacks the Case record right of the operation (X2) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the change (X1) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | The data product behind the trace is stale (X4, VR-S8-015-1) | {product} is from {date}. Today's ACE batch has not arrived. |

The text is the legacy and FSD S8 wording, copied unchanged; no message is reworded and none is added. The deviation service level that R-DEV-20 escalates against is set with DL22 and not published (ASM-5189).

### 15. Screens and states

| Screen | States | What this story answers |
|---|---|---|
| SCR-06 Raise deviation | Form; saved | The raise of X6 with its reason, its raised-by and the saved confirmation of MSG-S8-001 on `POST /cases/{caseId}/deviations` |
| SCR-08 Deviation queue | Loading; list | The open deviations by type, handler and age, the X6 trace status with its sources, and the advance that sends `PATCH /deviations/{deviationId}` |

Both screens are the edge contract's (DP-19) and the composite route also calls rwb-case for the case, its owner and its timers and rwb-agent for the trace status; this story fixes only its own answers (ASM-5182). The saved, refused, not-recorded, exhausted and stale-data states read the messages of section 14 on the same route.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E7-006-01 | AC1 (as the legacy id of this key: the trace, the handler and the decision-log entry of an X6) | Component | Synthetic case `RW-2027-001206`; one `deviation` row in DEV_WITH_OWNER, one decision record, one `DeviationRaised`; the end-to-end half is the harness that owns AC1 |
| TC-E7-006-02 | AC2 | Component | The decision-record stub stopped on the raise and on the advance; no row, no event, no outcome and no pause, MSG-P7-003 |
| TC-E7-006-03 | Access | Component | A role without the Case record right; 403 with MSG-P4-002 and no decision record |
| TC-E7-006-04 | Principle 5 | Component | A forced decision-record write failure stops the action with MSG-P7-003 and leaves the case at its paused state |

The four ids are the legacy cases of RWB-E7-006 in their legacy order, carried as the application proof of this slice, with the Level column added: every case is tested on the fakes, so every case is `Component`. TC-E7-006-01 exercises the record this story writes and its cross-service half is proved by RWB-ITG-E7006-ITG (ASM-5188). The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same id; the `-ITG` copies belong to the wave 4 harness and are not written here.

### 17. Guardrails

- No business value in code: the deviation codes, the raised-by and outcome lists, the 30-day trace window, the 10-working-day escalation and the deviation service level stay reference data or rule rows read with their version.
- No personal data in the deviation row, the decision record, an event, a workflow input, a log or a prompt: identifiers, codes, source codes, instants and a rule version only, and a contact point is a reference, never a value (BR10).
- ACE data and the trace sources only through the owner's contract: no `v_ace_*` view, no ACE table, no `partner` row, no agency file and no other service's schema (DP-01, DP-05, DP-11).
- One base, one topic, one queue and one login per service; this story adds no second topic and no Schedule (DP-13, DP-14).
- The decision record is written before the change and in its transaction; a failure rolls the row back (DP-03).
- One clock rule: the stage clock is paused and resumed by rwb-case on this story's outcome, and the prescription clock is never paused (BR4).
- No retired element is reintroduced: no Quartz row, no shared job table, no monolith base, no data-lake path and no read of the partner table.

### 18. Traceability

| Legacy | Story | Test |
|---|---|---|
| RWB-E7-006 AC1 | Not copied here; owned by RWB-ITG-E7006-ITG, which proves the X6 journey (ASM-5188) | TC-E7-006-01 (the application half) |
| RWB-E7-006 AC2 | AC2 (verbatim, with the mock lines) | TC-E7-006-02, TC-E7-006-04 |
| RWB-E7-006 TC-03 Access | AC2, X2 (the right on the two operations) | TC-E7-006-03 |
| RWB-E7-006 TC-04 Principle 5 | AC2, X1 (the forced failure of the decision record) | TC-E7-006-04 |

| Source | What it supplies |
|---|---|
| REQ-S8-004, REQ-DVH-011 (FSD S8 Requirements served) | A lost contact case runs skip tracing and returns to a decision whether or not contact is restored |
| FSD S8 A2.15, A1.2, A1.4, Screens | FEAT-DVF-06, its prerequisites, VR-S8-015-1 and BR-S8-015, the roles and SCR-06 and SCR-08 |
| TSD S8 T2, T3.1, T3.2, T4, T5.1, T5.3, T6.1 and T-A.1 | The decision-first rule, the `deviation` columns and lists, the DEVIATION machine, the absent external interfaces, the two events, the rights and the two operations |
| Business Rules and Routing Logic v4, DEV and UNIVERSAL sets | R-DEV-01, R-DEV-06, R-DEV-16 to R-DEV-20 and R-UNI-12 |
| Context pack S8 and the connection matrix | The schema, base, topic, queue, the two events, the one owned table, the P1 REST edge, the P10 Temporal edge and the P3 event edge |
| Split plan, slice RWB-S8-E7006-APP | H, C, I, X, the lane, the wave and the release (GAP-3061) |

### 19. Out of scope

- The contract surface: the OpenAPI document, the X6 element use, the skip-trace answer element, the consumed rows, the error set and the fakes (RWB-S8-E7006-CON).
- The end-to-end X6 journey across the services and the wave 4 harness: RWB-ITG-E7006-ITG, which owns AC1 and writes the run report.
- The other six codes and their flows (X1 to X5, X7), the screening agent and its L1 policy, the low-confidence review, two deviations on one case, the contact-breach path, the override review and the complaint-to-contact matching: each is its own story of this service.
- The case of record, its route state, its assignment, its queues and its timers: rwb-case (P3), whose answers this story consumes and fakes.
- The skip trace itself, its policy and its model, and the bureau, internal data and agency connections: rwb-agent (P10); the internal contact data product: rwb-source-data (P1).
- The agency and partner record, its panel and its contract: S9 rwb-partner, which no interface of this story reaches.
- The DEV package and the ledger: rwb-decision (P7); the roles and reference data: rwb-access (P4).
- The schema and migration of `rwb_deviation`, the login, the deployment, the observability, the alerts and the runbook: the DB, INF and OPS stories of this legacy key.
- Any change to a legacy file, to a master or to built Epic 1 and Epic 2 code.
