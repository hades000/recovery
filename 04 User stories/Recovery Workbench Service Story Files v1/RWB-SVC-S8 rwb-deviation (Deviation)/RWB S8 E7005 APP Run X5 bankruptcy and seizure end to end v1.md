# RWB-S8-E7005-APP Run X5 bankruptcy and seizure end to end

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S8-E7005-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-deviation |
| Service epic | RWB-SVC-S8 |
| Wave | 4 |
| Business epic | EP07 |
| Release | 31 May 2027 (tentative) |
| Legacy key | RWB-E7-005 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | L-S8-P |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S8-E7005-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S8 rwb-deviation v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: app slice split from RWB-E7-005 for rwb-deviation (S8). The X5 bankruptcy and seizure deviation is one `deviation` row of schema `rwb_deviation` on base `/api/recovery/deviation/v1` (DP-13), routed to Legal by R-DEV-05 and re-routed by R-DEV-15, with one decision record written through the local decision-record library before the row changes (DP-03) and the two deviation screens read through the gateway-bff composite route (DP-19). The case, its stage clock, the filing with the receiver or the LED, the legal action and the documents stay with rwb-case, rwb-litigation, rwb-document and rwb-access, and are consumed and faked. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **Legal counsel (RW-LEGAL)**, I want **the X5 bankruptcy and seizure deviation routed to Legal the same day, its own claim deadline held as a durable clock, and the case re-routed to litigation and then to write-off after the receiver reports â€” with one decision record written before the deviation changes â€”**, so that **a bankruptcy or a seizure never runs on a case whose stage clock is still counting, and the case of record, the filing with the official receiver or the LED and the legal action stay with the services that own them**.

This story owns the deviation of code X5 and the evaluation of R-DEV-05 and R-DEV-15, and nothing else:

- the two deviation operations of TSD S8 T-A on base `/api/recovery/deviation/v1`: API-S8-001 create and API-S8-002 patch, keeping their legacy operation IDs (DP-13);
- the `deviation` row of schema `rwb_deviation` with its fields DF-CAS-036 to DF-CAS-045 and X5 as one value of `deviation_code`, `X5` of LOV-DEVIATION (TSD S8 T3.1 and T3.2);
- the states of the deviation in the standard `state` column: `DEV_FLAGGED`, `DEV_WITH_OWNER`, `DEV_REROUTE` and `RESUMED` as the 22 DEVIATION rules of TSD S8 T4 give them;
- the evaluation of R-DEV-05 from `DEV_FLAGGED` on `OWNER_ASSIGNED` (assign to Legal; file with the official receiver or the LED before the deadline) and of R-DEV-15 from `DEV_WITH_OWNER` on `BANKRUPTCY_FILED` (route to litigation, then to write-off after the receiver reports), each with one decision record written through the local decision-record library with the rule ID and the version in force, before the deviation changes (DP-03, legacy AC2, AC3 and AC4);
- the X5 deadline timer behind R-DEV-05's "before the deadline" and the SLA timer of R-DEV-20, both durable timers of `DeviationWorkflow` on queue `rwb-deviation`;
- the two catalogue events of the service, `DeviationRaised` (EV-06) and `DeviationCleared` (EV-07), which carry the pause, the resume and the contact stop to the timers and to communications.

It does not own the case, its stage clock, the work assignment, the filing, the legal action or the documents. `recovery_case` and the stage clock it pauses are the case of record's (rwb-case, P3): this service records the state the case paused in as `paused_state` and announces the pause, and the stage workflow that owns the clock consumes `DeviationRaised`. The stage timer, the work assignment and the case task are not in this service's one table. The act of filing with the official receiver or the LED, the court references and the `legal_action` row are rwb-litigation's (S4), reached through the case of record and never called from here: the connection matrix of Architecture v5 slide 13 gives rwb-deviation no REST call to S4. The evidence pack is rwb-document's (P5). The central `decision_log_entry` and the rule rows are rwb-decision's (P7). No component of this story writes a `recovery_case`, `assignment`, `timer`, `legal_action`, `document`, `decision_log_entry` or `rule_row` row, and none reads a `v_ace_*` view.

### 2. Business rationale

Bankruptcy and seizure are the two legal events that stop a recovery case dead: direct collection must stop, and a claim must be lodged with the official receiver or the Legal Execution Department before a deadline that does not move for the bank. The legacy story handled X5 inside one process that wrote the deviation, the assignment, the timer, the legal action and the decision log entry, all in the single `recovery` schema, and the deviation had no clock of its own: the module's own problem statement is that complaints, hardship, death, fraud, bankruptcy, lost contact and collateral events are handled case by case with no clock (FSD S8 v3 A1.3). In the target the same step is cut four ways: the deviation and its two rules are deviation's; the case and its stage clock are the case of record's; the filing, the receiver and the legal action are litigation's; and the record of the decision is the shared library's.

This story is the deviation slice. It raises the X5 deviation, evaluates R-DEV-05 â€” from `DEV_FLAGGED`, on `OWNER_ASSIGNED`, `deviation_code = X5`, "Assign to Legal; file with the official receiver or the LED before the deadline", to `DEV_WITH_OWNER`, owner "Legal", channel "LIT, Workbench", service level "deadline driven" (Business Rules and Routing Logic v4; TSD S8 T4) â€” and writes the decision record of that answer before the row changes. It then holds two clocks the legacy story did not have: the claim deadline of R-DEV-05 and the 10-working-day SLA of R-DEV-20, both durable timers of `DeviationWorkflow`. On `BANKRUPTCY_FILED` it evaluates R-DEV-15 and moves the deviation to `DEV_REROUTE`; R-DEV-19 then re-opens the route decision at D6, which is rwb-valuation's and rwb-case's, not this service's.

A failed record write changes nothing and the officer sees MSG-P7-003: that is legacy AC4, and it is DP-03 applied in the place the legacy `DecisionLogWriter` sat. AC2 and AC3 are the two rules, and they are copied word for word in section 7. AC1 of the legacy key is the end-to-end run of the whole deviation and is owned by `RWB-ITG-E7005-ITG`, which proves it across the services; it is not restated here.

Two vocabularies must not be confused, and the story is built so that they cannot be. `DEV_FLAGGED`, `DEV_WITH_OWNER` and `DEV_REROUTE` are states of the **deviation**, in the standard `state` column of `deviation` (TSD S8 T4). The case of record has states of its own, and it is the case that pauses. Legacy AC2 and AC3 say "the case moves to DEV_WITH_OWNER" and "the case moves to DEV_REROUTE"; in the target the deviation moves to those states and announces itself, and rwb-case moves the case. The two services agree on the announcement shape and on nothing else (BR3).

The naming baseline is fixed and is not a local choice: schema `rwb_deviation`, login `rwb_deviation`, base `/api/recovery/deviation/v1`, topic `rwb.deviation.events.v1` with retry and `.dlt` topics, event names `rwb.deviation.<Event>.v1`, task queue `rwb-deviation` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.deviation`. The two screens are read through the gateway-bff composite route and no screen calls the service directly (DP-19).

It serves FEAT-DVF-05 "Run X5 bankruptcy and seizure end to end" and the FSD S8 measure "deviations closed within the service level, set with DL22". The requirement identifiers of the key are absent from the legacy master, from the Epics 3 to 8 specification and from the TSD S8 trace table, so the story traces to the feature until the PRD adds them (GAP-3059; ASM-5170).

### 3. Preconditions

- `RWB-S8-E7005-CON` is published: API-S8-001 and API-S8-002 on `/api/recovery/deviation/v1`, the `DeviationRequest`, `Deviation` and `DeviationOutcome` schemas, the error envelope, the `Idempotency-Key` rule and the fake. This story builds against it on Day 1; it is the first build dependency.
- The `deviation` table exists in schema `rwb_deviation` with the fields DF-CAS-036 to DF-CAS-045 of TSD S8 T3.1 and the seven standard columns of T3.0. No new table and no new column is created by this story.
- The local decision-record library and the record format of DP-03 are live (`RWB-PLT-E1027-CON`) and the record is hash-linked on the shared topic `rwb.decision-record.v1`. The story builds against its stub until the platform contract story publishes.
- The gateway-bff composite route `RWB-PLT-N001-CON` serves SCR-08 Deviation queue and SCR-06 Raise deviation; it is in the build list (DP-19), so the two read surfaces are available from Day 1.
- The case contract of rwb-case that reads the case state, pauses and resumes the stage clock and accepts the route fact is published and faked. It is **not** in this story's dependency rows: the metadata carries no contract dependency and the absence is recorded as GAP-3059 with ASM-5170. No source read for this key names its operations.
- The values of LOV-DEVIATION (`X1`, `X2`, `X3`, `X4`, `X5`, `X6`, `X7`), LOV-RAISED-BY (`SCREENING_AGENT`, `RULE`, `OFFICER`, `CUSTOMER_CONTACT`) and LOV-DEV-OUTCOME (`RETURNED`, `RE_ROUTED`, `CASE_ENDED`) of TSD S8 T3.2 are read as values in force with their version, on the reference data of rwb-case. DP-07 is not in this story's pattern set and the read carries no dependency row either (GAP-3059; ASM-5170).
- The claim deadline of R-DEV-05 and the service levels of R-DEV-20 are versioned reference rows and not code. Their values are Not specified in the source documents (GAP-3059; ASM-5170).
- The service runs as its own login on schema `rwb_deviation` (DP-01, DP-02); it holds no grant on another `rwb_*` schema and no `v_ace_*` grant.
- The caller holds a Workbench role with the Case record right the legacy permission block of RWB-E7-005 gives, right U. TSD S8 T6.1 gives RW-LEGAL the right R only on the case record while FSD S8 A2.14.3.3 names Legal counsel as the primary actor of X5; the difference is carried as GAP-3059 with ASM-5170 and is rwb-access's to settle.
- The FSD S8 v3 and the TSD S8 v2 this story reads are In review with an empty sign-off table, and neither this story nor its contract half is signed off. The run of D-RCV-60 has no human approval step, so both stories carry Status Draft (realignment v1) and the missing approval is recorded rather than waited for (GAP-3059; ASM-5175).

### 4. Flow

1. The X5 deviation arrives on `POST /cases/{caseId}/deviations` (API-S8-001) with `deviationCode = X5`, `raisedBy` from LOV-RAISED-BY, `pausedState` set to the routing state the case was in and `contactStop` false; a flag raised by the screening agent arrives on the same operation with `raisedBy = SCREENING_AGENT`.
2. `DeviationValidator` checks the case reference against the caller's scope, the value of `deviationCode` against LOV-DEVIATION, `raisedBy` against LOV-RAISED-BY, the required fields of VR-S8-014-1 and the state the case is in. A failed check answers 422 or 404 and nothing is written.
3. `DeviationDecisionWriter` evaluates R-DEV-01 and then R-DEV-05 with the rule package in force â€” `deviation_code = X5`, event `OWNER_ASSIGNED`, the deadline and the Legal route as versioned reference rows â€” and writes **one** decision record through the local decision-record library before the deviation changes: rule ID `R-DEV-05`, the version in force, the inputs reference, the answer `DEV_WITH_OWNER` and the decision code read from LOV-DECISION.
4. `DeviationWriter` writes, in one `rwb_deviation` transaction, the `deviation` row with `state` `DEV_FLAGGED` moving to `DEV_WITH_OWNER`, `handler_user_id` set to the Legal handler the route names, `contact_stop` unchanged at false for X5 and `outcome` empty, plus the idempotency row of the request. No other owner's row is written.
5. `DeviationWorkflow` starts or continues on `rwb-deviation`: it opens the X5 claim deadline as its own durable timer and the 10-working-day SLA of R-DEV-20 as a second one, and it does not open a prescription timer, because the prescription clock never pauses (R-DEV-01).
6. `CaseAnnouncementClient` announces the pause to rwb-case with `caseId`, `deviationCode X5` and `raisedBy` â€” the three fields EV-06 carries â€” and rwb-case pauses the stage clock, keeps the prescription clock running and puts the case with the Legal handler. The stage timer and the assignment are the case's and this service writes neither.
7. The Legal counsel opens SCR-08 Deviation queue through the gateway-bff composite route (DP-19) and reads the X5 deviations of the case from this service and the case state from rwb-case; the queue shows code, handler, raised date, return point, contact stop and the deadline timer.
8. The counsel files the claim with the official receiver or the LED. That filing, its legal action, its court references and its lifecycle are rwb-litigation's (S4); this service holds the deadline and the handler, and records nothing of the filing except what the case event carries back.
9. The filing returns to this service as the `BANKRUPTCY_FILED` event of the case of record. `DeviationWorkflow` handles it and evaluates R-DEV-15: the deviation moves from `DEV_WITH_OWNER` to `DEV_REROUTE` with `outcome = RE_ROUTED`, and the decision record of that answer is written before the row changes.
10. R-DEV-19 follows on `ROUTE_REOPENED`: the deviation is announced to the route decision at D6, which is rwb-valuation's, with the rule ID and the version in force, and the case is re-decided against litigation and then write-off after the receiver reports. This service evaluates neither the route rule nor the write-off trigger.
11. The outcome of the deviation is recorded on `PATCH /deviations/{deviationId}` (API-S8-002) with `DeviationOutcome`: `outcome`, `clearedAt` and the state the case returns to. `DeviationCleared` (EV-07) then carries `caseId`, `deviationCode` and `outcome` to the timers and to communications, and contact resumes only when no other deviation holds a contact stop.
12. A repeated request with the same `Idempotency-Key`, or the same open deviation for the same case and code, writes nothing and publishes no second event; the repeat is counted under R-UNI-40.
13. SCR-08 and SCR-06 read the deviation and its states from this service through the composite route, read only, next to the case state of rwb-case.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The request carries no `deviationCode`, no `raisedBy`, no `pausedState` or no `contactStop` | The answer is 422 and nothing is read beyond the validator; no decision record and no row | MSG-GEN-001 | AC2 |
| X2 | The case ID names no case in the caller's scope, or the deviation ID names no row | The answer is 404 and nothing is written; an out-of-scope case cannot be told from a missing one | None | AC2 |
| X3 | A deviation of code X5 is already open on the case, or the row is not in the state the step needs | The answer is 409 and nothing changes; the repeat is counted under R-UNI-40 | None | AC2 |
| X4 | A role without the Case record right raises or patches the deviation | Refused before any read or write; nothing changes and no decision record is written | MSG-P4-002 | AC2 |
| X5 | The local decision-record write fails | The transaction writes nothing: the deviation keeps its previous state, no event leaves the service and the case clock is not paused | MSG-P7-003 | AC4 |
| X6 | The claim deadline of R-DEV-05 is reached before the filing is recorded | The deadline timer fires and R-DEV-20 escalates to the team manager and reports the breach; the deviation stays `DEV_WITH_OWNER` | MSG-S8-001 | AC2 |
| X7 | The case of record does not answer inside 2 s, or its breaker is open | The deviation keeps what it wrote, because that fact is true and this service's own; the answer is 503 with the platform envelope and the hand-off is re-run by repeating the same `Idempotency-Key` | None | AC2 |
| X8 | The case refuses the pause or the route fact | The deviation keeps its state, the refusal is recorded for the case owner and the caller reads the answer of the case contract unchanged; this service does not move the case itself | None | AC3 |
| X9 | `BANKRUPTCY_FILED` arrives for a deviation that is not in `DEV_WITH_OWNER`, or twice | R-DEV-15 does not fire, the second arrival is treated as a repeat and nothing changes; the deviation is not re-routed twice | None | AC3 |
| X10 | A component, a statement or a test reaches another `rwb_*` schema, a `v_ace_*` view or an ACE table | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | BR5 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against `RWB-S8-E7005-CON`, the decision-record library and the composite route; the case contract and the reference data are consumed and faked, and the missing dependency rows are recorded (GAP-3059) |
| Negotiable | The claim deadline, the SLA, the Legal handler route and the three list values are versioned reference data; the story fixes the behaviour and the shapes, not the values |
| Valuable | An X5 deviation gets a handler, a clock and a re-route, so a bankruptcy or a seizure no longer runs on a case whose stage clock is still counting |
| Estimable | Two operations, one validator, two rule evaluations, one library write, one repository write, one workflow with two timers, one client and one read-only screen fragment |
| Small | Fits two weeks with its tests, as the X5 slice of the legacy key; AC1 is the harness story's |
| Testable | Each owned criterion of section 7 is one test with the cross-service answers stubbed in the contract fakes; the contract half is tested in `RWB-S8-E7005-CON` and the whole run in `RWB-ITG-E7005-ITG` |

### 7. Acceptance criteria

```gherkin
Feature: Run X5 bankruptcy and seizure end to end, in rwb-deviation

  Background:
    Given the X5 deviation "DV-2026-000502" exists on case "RW-2026-000502"
    Given the rule package of R-DEV-05 and R-DEV-15 is in force at its version, and LOV-DEVIATION, LOV-RAISED-BY and LOV-DEV-OUTCOME are read with their version in force
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC2 Rule R-DEV-05 (legacy RWB-E7-005 AC2)
    Given a case in state DEV_FLAGGED
    Given the rwb-case contract mock returns the case in state DEV_FLAGGED
    When owner assigned
    Then assign to Legal; file with the official receiver or the LED before the deadline
    Then the case moves to DEV_WITH_OWNER

  Scenario: AC3 Rule R-DEV-15 (legacy RWB-E7-005 AC3)
    Given a case in state DEV_WITH_OWNER
    Given the rwb-case contract mock returns the event BANKRUPTCY_FILED
    When bankruptcy filed
    Then route to litigation, then to write-off after the receiver reports
    Then the case moves to DEV_REROUTE

  Scenario: AC4 Not recorded (legacy RWB-E7-005 AC4)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

These three criteria are the legacy criteria of RWB-E7-005, copied word for word: not one legacy line is reworded, shortened or renumbered, and every value of the source (`DEV_FLAGGED`, `DEV_WITH_OWNER`, `DEV_REROUTE`, `BANKRUPTCY_FILED`, MSG-P7-003, the official receiver, the LED) is kept character for character. The only additions are the origin tag on each `Scenario:` line and, inside AC2 and AC3, one `Given` line for the cross-service answer that a source does not give in process: the case state and the filing event are answered by the rwb-case contract fake, and every other line and value is unchanged. AC1 of the legacy key is not owned by this story; it is the end-to-end run of the whole deviation and is owned by `RWB-ITG-E7005-ITG`. In AC2 and AC3 the states named are the deviation's, and the case is announced to and moved by rwb-case (BR3, section 9). The contract half of these surfaces is tested in `RWB-S8-E7005-CON`.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| R-DEV-01 | Deviations Â· X1 to X7 Â· from `ANY_STATE` Â· event `DEVIATION_FLAGGED` Â· condition `deviation_code in (X1..X7)` Â· action "Pause the stage clock, keep the prescription clock running, route to the named owner" Â· to `DEV_FLAGGED` Â· owner "Workbench" Â· channel "Workbench, the Workbench document hub" Â· same day | Business Rules and Routing Logic v4 (R-DEV-01); TSD S8 T4 |
| R-DEV-05 | Deviations Â· X1 to X7 Â· from `DEV_FLAGGED` Â· event `OWNER_ASSIGNED` Â· condition `deviation_code = X5` Â· action "Assign to Legal; file with the official receiver or the LED before the deadline" Â· to `DEV_WITH_OWNER` Â· owner "Legal" Â· channel "LIT, Workbench" Â· service level "deadline driven" | Business Rules and Routing Logic v4 (R-DEV-05); TSD S8 T4 |
| R-DEV-15 | Deviations Â· X1 to X7 Â· from `DEV_WITH_OWNER` Â· event `BANKRUPTCY_FILED` Â· condition `deviation_code = X5` Â· action "Route to litigation, then to write-off after the receiver reports" Â· to `DEV_REROUTE` Â· owner "Legal, litigation officer" Â· channel "LIT" | Business Rules and Routing Logic v4 (R-DEV-15); TSD S8 T4 |
| R-DEV-19 | Deviations Â· X1 to X7 Â· from `DEV_REROUTE` Â· event `ROUTE_REOPENED` Â· condition "Any" Â· action "Recompute the segment and re-run the hard gates" Â· to `ROUTE_D6` Â· owner "Case owner" Â· channel "Workbench" | Business Rules and Routing Logic v4 (R-DEV-19); TSD S8 T4 |
| R-DEV-20 | Deviations Â· X1 to X7 Â· from `DEV_WITH_OWNER` Â· event `SLA_BREACHED` Â· condition "time in DEV_WITH_OWNER exceeds the deviation service level" Â· action "Escalate to the team manager and report the breach" Â· to `DEV_WITH_OWNER` Â· owner "Team manager" Â· 10 working days | Business Rules and Routing Logic v4 (R-DEV-20) |
| BR1 | The deviation is a `deviation` row of this service: `deviation_code` takes `X5` of LOV-DEVIATION, the state is the standard `state` column, and the handler, the paused state, the contact stop and the outcome are written on that row and nowhere else | TSD S8 T3.1, T3.2; Architecture v5 slide 41 (S8 owns deviations); legacy Data block |
| BR2 | The decision is written before the deviation changes: one record through the local decision-record library, with the rule ID and the version in force; a failed write changes nothing and the caller sees MSG-P7-003 | DP-03; TSD S8 T2 ("writes the decision log entry before any change"); Architecture v5 slide 28 (R-UNI-39); legacy AC4 |
| BR3 | The case is announced to, never written: the pause, the resume and the route fact go to rwb-case with the rule and its version, and the states `DEV_FLAGGED`, `DEV_WITH_OWNER` and `DEV_REROUTE` are the deviation's states while the case has states of its own | R-DEV-01, R-DEV-15, R-DEV-19; legacy AC2 and AC3; Ownership Map v1 (`recovery_case` is rwb-case's) |
| BR4 | The prescription clock is never paused by this service: R-DEV-01 pauses the stage clock only, and the prescription date and its warning belong to the case of record | R-DEV-01; FSD S8 A2.3.1; Architecture v5 slide 3 ("the legal deadline never pauses") |
| BR5 | No ACE read and no cross-schema read: this story reads no `v_ace_*` view, no ACE table and no other `rwb_*` schema, and its login holds no such grant | DP-01, DP-05 as a prohibition |
| BR6 | Closed vocabulary: `deviation_code`, `raised_by` and `outcome` take only the values of LOV-DEVIATION, LOV-RAISED-BY and LOV-DEV-OUTCOME in force, read with their version; the claim deadline, the service levels and the Legal route are versioned reference rows and are never written in code | TSD S8 T3.2; FSD S8 A2.14.3.1 (BR-S8-014); Template and Rules section R7.2 (s17) |
| BR7 | No personal data: the row, the decision record, the log and every call carry identifiers, list values, codes and dates only; no name, address, identity number or account number enters this service | TSD S8 T3.1; Architecture v5 slides 42 and 43 notes |
| R-UNI-39 | An action whose decision cannot be recorded does not proceed and nothing moves | Business Rules and Routing Logic v4 (R-UNI-39); legacy AC4 |
| R-UNI-40 | The same event or the same request twice produces one effect, and the repeat is counted | Business Rules and Routing Logic v4 (R-UNI-40) |

The claim deadline that R-DEV-05's action names and the deviation service level of R-DEV-20 have no value in any source read for this key, so both are versioned reference rows and never code: the placeholder Not specified in the source documents (GAP-3059; ASM-5171) stands in the configuration of section 13, in the rule row and on the timer.

### 9. State transitions

This story moves the state of its own deviation and announces a pause and a route fact to the case. The two are different objects and are never used one for the other.

**`deviation.state`** â€” the DEVIATION machine of TSD S8 T4, moved by this service:

| From | Event | Condition | To |
|---|---|---|---|
| (none) | The deviation is raised on API-S8-001 | `deviationCode` is a value of LOV-DEVIATION and the record is written | `DEV_FLAGGED` |
| `DEV_FLAGGED` | `OWNER_ASSIGNED` | `deviation_code = X5`, R-DEV-05 fires and the decision record is written | `DEV_WITH_OWNER`, handler Legal, deadline timer open |
| `DEV_WITH_OWNER` | `BANKRUPTCY_FILED` | `deviation_code = X5`, R-DEV-15 fires and the decision record is written | `DEV_REROUTE`, `outcome = RE_ROUTED` |
| `DEV_REROUTE` | `ROUTE_REOPENED` | R-DEV-19 fires; the route decision is re-run at D6 by its owners | `ROUTE_D6`, announced to rwb-case |
| `DEV_WITH_OWNER` | `SLA_BREACHED` | 10 working days in the state are exceeded; R-DEV-20 escalates | `DEV_WITH_OWNER`, with the breach reported |
| `DEV_REROUTE` | The outcome is recorded on API-S8-002 | `outcome = RETURNED` and the case returns to the paused state | `RESUMED` through R-DEV-18 |
| `DEV_REROUTE` | The case ends | `outcome = CASE_ENDED`; the close is rwb-case's | `CASE_ENDED` on the case, announced here |

**The case's own pause and re-route** are rwb-case's, and this story only announces them (BR3):

| From (rwb-case) | Announced by this service on | Effect on the case | Owner of the move |
|---|---|---|---|
| Any stage state | `DeviationRaised` (EV-06) after R-DEV-05 | Stage clock paused at `paused_state`, prescription clock still running, case with the Legal handler | rwb-case |
| Paused state | `DeviationCleared` (EV-07) with `outcome = RETURNED` | Stage clock resumed at the state it paused in, contact resumed | rwb-case |
| Paused state | `DeviationCleared` (EV-07) with `outcome = RE_ROUTED` | Case re-opened at the route decision D6 on R-DEV-19 | rwb-case with rwb-valuation; the litigation route, the receiver and the write-off are rwb-litigation's and rwb-writeoff's |

The value of `state` for a deviation whose outcome is not mapped by R-DEV-05, R-DEV-15, R-DEV-18 or R-DEV-19 is not given by any source read here, so it is left at `DEV_REROUTE` and carried as Not specified in the source documents (GAP-3059; ASM-5171). Neither the case row nor its state is read as a table or written here; the case read of 12.2 and the announcement are the only paths by which the case moves.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-LEGAL, legal counsel | The primary actor of FSD S8 A2.14. TSD S8 T6.1 gives the role the right R on the case record, so the write right on the two operations is carried as GAP-3059 with ASM-5172 and settled by rwb-access |
| RW-ENFORCE, enforcement owner | Case record RU of TSD S8 T6.1: raises, reads and patches the X5 deviation in scope, and records the receiver's answer |
| RW-LITOFF, litigation officer | Case record RU; the litigation owner of R-DEV-15's second half, reading the deviation and its deadline |
| RW-CASEOWN, RW-RESTRUCT, RW-SPECIAL, RW-COMPLAIN, RW-FRAUD, RW-SALEOFF and the remaining roles of the legacy permission block | Case record U, as the legacy block gives them; the full role list is rwb-access data |
| RW-CONDUCT, RW-RISK, RW-COE, RW-TEAMMGR, RW-HEADLIT and the read-only roles of TSD S8 T6.1 | Case record R: read the deviation and its states only |
| rwb-deviation service identity | Validates, evaluates R-DEV-05 and R-DEV-15, writes the decision record and the row, runs `DeviationWorkflow` and announces the case; it holds no grant on another schema and no `v_ace_*` grant |
| rwb-case (P3) service identity | Owns the case of record, its stage clock and its work assignment; consumes `DeviationRaised` and `DeviationCleared` and answers the route fact |
| rwb-access (P4) service identity | Owns the roles, the rights, the scope and the masking data the two operations declare |

The rights above are the rows of TSD S8 T6.1 and the legacy permission block, and nothing wider. The role code of the Legal handler that R-DEV-05 routes to is a value of the reference data and is Not specified in the source documents (GAP-3059; ASM-5172). DP-08 is not in this story's pattern set: the declared right of each operation is enforced at the edge for the screen path and by this service on the write paths. A refusal keeps MSG-P4-002 and changes nothing.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-CAS-036 | deviation (S8, `rwb_deviation`) | id | Write on create; read as the reference of every call and answer |
| DF-CAS-037 | deviation (S8, `rwb_deviation`) | case_id | Write on create; read and sent on the case announcement |
| DF-CAS-038 | deviation (S8, `rwb_deviation`) | deviation_code | Write, `X5` of LOV-DEVIATION; read by both rules |
| DF-CAS-039 | deviation (S8, `rwb_deviation`) | raised_at | Write on create |
| DF-CAS-040 | deviation (S8, `rwb_deviation`) | raised_by | Write on create, against LOV-RAISED-BY; sent on EV-06 |
| DF-CAS-041 | deviation (S8, `rwb_deviation`) | paused_state | Write on create; the state the case returns to on R-DEV-18 |
| DF-CAS-042 | deviation (S8, `rwb_deviation`) | handler_user_id | Write when R-DEV-05 assigns; read by the SLA rule and the queue |
| DF-CAS-043 | deviation (S8, `rwb_deviation`) | contact_stop | Write; false for X5, because the contact stop of FSD S8 A2.5 belongs to X1 to X3 |
| DF-CAS-044 | deviation (S8, `rwb_deviation`) | cleared_at | Write on API-S8-002 |
| DF-CAS-045 | deviation (S8, `rwb_deviation`) | outcome | Write, against LOV-DEV-OUTCOME; sent on EV-07 |
| Standard columns | deviation (S8, `rwb_deviation`) | state, version, created_at, created_by, updated_at, updated_by, is_active | Written by the service identity; `state` carries the DEVIATION machine of TSD S8 T4 (TSD S8 T3.0) |
| DF-DEC-003, DF-DEC-004, DF-DEC-005, DF-DEC-008, DF-DEC-012, DF-DEC-016, DF-DEC-017, DF-DEC-018 | decision record (PLT library, created in `rwb_deviation`) | decision code, rule ID, rule version, inputs reference, final call, decided at, the two hashes | Write through the local library, before the deviation changes |
| DF-CAS-001 to DF-CAS-023 | recovery_case (P3, `rwb_case`) | the case, its product group, its state and its prescription date | Read on the case contract only; never written here |
| DF-WRK-009 to DF-WRK-016, DF-WRK-027 to DF-WRK-036 | assignment and timer (case of record) | the case task and the stage clock R-DEV-01 pauses | Announced to; never read as a table and never written here |
| DF-LEG-001 to DF-LEG-014 | legal_action (S4, `rwb_litigation`) | the filing with the official receiver or the LED | Not touched: the filing and its court references are rwb-litigation's, and this service has no call to it |
| DF-DOC-001 to DF-DOC-011 | document (P5, `rwb_document`) | the evidence of the filing | Not touched: the pack is rwb-document's |
| DF-DEC-001 to DF-DEC-018, DF-REF-001 to DF-REF-015 | decision_log_entry and rule_row (P7, `rwb_decision`) | the central ledger and the rule rows of R-DEV-05 and R-DEV-15 | Read as values in force through the rule package; never written here |

Field identifiers are those of TSD S8 v2 T3.1, the data dictionary identifiers the legacy story's Data block carries, and the standard columns of TSD S8 T3.0. **No new table, no new column and no migration:** `deviation` arrives with the S8 schema of this service and its contract story `RWB-S8-E7005-CON` publishes the DDL template, which the service's own Flyway applies (DP-15); `decision_record` and `idempotency_key` are platform library objects created in `rwb_deviation` by the library's migration (DP-03). The legacy story's `recovery_case`, `assignment`, `timer`, `legal_action` and `document` rows are other owners' and appear here as consumed shapes only. The `deviation` object keeps the DF-CAS identifier range of the dictionary although this service owns it; the range is copied, not renumbered (GAP-3059; ASM-5181).

**No personal data.** The row this story writes carries identifiers, codes, dates and list values. The borrower, the guarantor, the address and the identity number never enter `rwb_deviation`: they are held by ACE and reached only through rwb-source-data by the services that need them, and they are not logged here and not put on any call or event.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-deviation (S8); base `/api/recovery/deviation/v1` (DP-13).

| ID | Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|---|
| API-S8-001 | POST | `/cases/{caseId}/deviations` | Raise the X5 deviation: the `deviation` row and the decision record of R-DEV-01 and R-DEV-05 (TSD S8 T-A.2) | Case record U, scope applied | `Idempotency-Key` header required; the answer is stored and a repeat returns it |
| API-S8-002 | PATCH | `/deviations/{deviationId}` | Record the outcome of the deviation and return or re-route the case (TSD S8 T-A.2) | Case record U, scope applied | Not applicable |

The two operations and their IDs, purposes and error sets are those of TSD S8 T-A.1 and T-A.2; they keep their legacy IDs and differ only in the base, which DP-13 renames. Errors: 401 no session; 403 no right (MSG-P4-002); 404 unknown or out-of-scope reference; 409 a state that refuses the step or an X5 deviation already open; 422 a missing or invalid field (MSG-GEN-001); 503 the decision-record library or a consumed contract unavailable. The request and answer shapes are declared by `RWB-S8-E7005-CON`, which this story consumes as its first build dependency.

#### 12.2 REST operations consumed

| Method and path | Owner | Use in this story |
|---|---|---|
| The case read and the pause, resume and route announcement of rwb-case, operation Not specified in the source documents (GAP-3059; ASM-5170) | P3 rwb-case | Reads the case state and the paused state, pauses the stage clock and keeps the prescription clock, and accepts the route fact of R-DEV-19. The stage timer and the assignment are the case's |
| The reference-data read of LOV-DEVIATION, LOV-RAISED-BY and LOV-DEV-OUTCOME, `RWB-P3-E1043-CON` | P3 rwb-case | The three list codes at their version in force (DP-07, declared here although the pattern is not in this story's set) |

Every row is one hop with a 2 s timeout and a breaker per downstream (ADR-020). Both rows are built against their fakes; the case row carries the missing dependency of GAP-3059. The filing with the official receiver or the LED is **not** a consumed call of this story: the connection matrix of Architecture v5 slide 13 gives rwb-deviation no REST edge to rwb-litigation, and the filing fact returns as the `BANKRUPTCY_FILED` case event of 12.4.

#### 12.3 Events published

| Event | Topic | Payload | Consumer |
|---|---|---|---|
| `rwb.deviation.DeviationRaised.v1` (EV-06) | `rwb.deviation.events.v1` | `caseId`, `deviationCode`, `raisedBy` | The timers that pause the stage clock, and communications for the contact stop (Event and Messaging Design v4) |
| `rwb.deviation.DeviationCleared.v1` (EV-07) | `rwb.deviation.events.v1` | `caseId`, `deviationCode`, `outcome` | The timers that resume the stage clock, and communications (Event and Messaging Design v4) |

The two events are the catalogue's, on the service topic of the naming rule with its retry and `.dlt` topics, in the CloudEvents envelope. DP-09 is not in this key's pattern set, so the outbox and the producer are not declared by the pattern table and the platform story `RWB-PLT-TE006-CON` is not in the metadata; the gap is carried as GAP-3059 with ASM-5173 and the events are still published, because the event catalogue assigns both to this service. The decision record is written through the local decision-record library of DP-03, which publishes `DecisionRecorded` on the shared `rwb.decision-record.v1`; that element is the library's and this story declares no payload of its own.

#### 12.4 Events consumed

| Event | Topic | Owner | Use |
|---|---|---|---|
| The case event that carries `BANKRUPTCY_FILED` for a case with an open X5 deviation | `rwb.case.events.v1` | P3 rwb-case | The trigger of R-DEV-15 and of the move to `DEV_REROUTE`; the event name is Not specified in the source documents (GAP-3059; ASM-5174) |
| The case event that reports the stage clock pause, the resume and the route re-open at D6 | `rwb.case.events.v1` | P3 rwb-case | The confirmation the `CaseAnnouncementClient` waits for; the event names are Not specified in the source documents (GAP-3059; ASM-5174) |

Once and not twice: each consumer holds an inbox row keyed on the CloudEvents id, so a repeated delivery writes one effect and the repeat is counted (R-UNI-40). The connection matrix of Architecture v5 slide 13 gives rwb-deviation no subscription to rwb-litigation, rwb-decision or rwb-comms, so the filing, the approval and the contact stop reach this service only through the case events above or not at all.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| DeviationWorkflow | Workflow, one run per open deviation, the S8 child of CaseWorkflow; can start at any time and pauses the stage clock | `rwb-deviation` | Started by CaseWorkflow on rwb-case, or by the create of API-S8-001; holds the deviation's two durable timers and its signals (Temporal design slides 8 and 13) |
| validateDeviation | Activity | `rwb-deviation` | The validator of step 2 |
| evaluateRules | Activity through the embedded Drools kit | `rwb-deviation` | R-DEV-01, R-DEV-05 and R-DEV-15 with the rule package and the version in force |
| recordDecision | Activity through the library | `rwb-deviation` | The local decision record and its outbox row, written before the change (DP-03) |
| applyDeviation | Activity | `rwb-deviation` | The `deviation` row and its state, in one `rwb_deviation` transaction (RecordAndApply) |
| raiseClockSignal | Activity or signal | `rwb-deviation` | The pause, the resume and the route fact announced to rwb-case, and the two timers opened on the workflow |
| publishDeviation | Activity | `rwb-deviation` | `DeviationRaised` and `DeviationCleared` on `rwb.deviation.events.v1` through the outbox |

The workflow name is fixed by the Temporal and Drools design (`DeviationWorkflow` on `rwb-deviation`, "DEV 22", "can start at any time and pauses the stage clock"). The claim deadline of R-DEV-05 and the 10 working days of R-DEV-20 are durable timers of that workflow and not Schedules. History: Continue-As-New at every clear and at least every 28 days, children with parent close policy ABANDON.

#### 12.6 Schedules

None. No Temporal Schedule and no Quartz job is declared. The deviation is raised by a person, by the screening agent or by a case event, and its two clocks are durable timers of `DeviationWorkflow`. The service owns no job (Ownership Map v1: jobs 0) and `rwb-deviation` registers no Schedule of Architecture v5 slide 44.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| deviation | S8 (rwb_deviation) | The X5 row, its state, its handler, its paused state and its outcome, DF-CAS-036 to DF-CAS-045 |
| decision_record | PLT library, created in `rwb_deviation` | The hash-linked record of the R-DEV-05 and R-DEV-15 answers, written before the change (DP-03) |
| idempotency_key | PLT library, created in `rwb_deviation` | The key of the create, with the stored answer |

Not owned and never written: `recovery_case` (P3), `assignment` and `timer` (the case of record), `legal_action` (S4), `document` (P5), `decision_log_entry` and `rule_row` (P7). No `v_ace_*` view and no ACE table is read (BR5).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case WireMock | Case `RW-2026-000502` at state `DEV_FLAGGED` and at `DEV_WITH_OWNER`, the pause accepted, the `BANKRUPTCY_FILED` event, the route fact accepted, the refusal of a route fact from another state, and a delayed answer | AC2, AC3, X7, X8 |
| decision-record library stub (RWB-PLT-E1027-CON) | A healthy chain with its outbox row, and a stopped chain for the fail-closed test | AC2, AC3, AC4 |
| reference-data WireMock | LOV-DEVIATION, LOV-RAISED-BY and LOV-DEV-OUTCOME at their version in force, and the claim-deadline and SLA rows at theirs | AC2, AC3, X6 |
| gateway-bff composite route fake (RWB-PLT-N001-CON) | The merged SCR-08 and SCR-06 answer for `RW-2026-000502`, with the deviation read once | AC2 |
| Event topic fake | The two `rwb.deviation.*` events with their CloudEvents envelope, and a repeated delivery for the inbox test | AC2, AC3 |

The fakes are test-only and are replaced by the real services in SIT; the drift between a fake and `RWB-S8-E7005-CON` or against the case document is a build failure.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 2 consumed | API-S8-001 and API-S8-002 provided; the case read and announcement and the reference data consumed; one hop, 2 s |
| Kafka | 2 published, 2 consumed | `DeviationRaised` and `DeviationCleared` published on `rwb.deviation.events.v1`; the case events of 12.4 consumed; outbox and inbox per DP-09, carried as GAP-3059 |
| Temporal | 1 workflow, 6 activities, no Schedule | `DeviationWorkflow` with its validator, its rule evaluation, its record, its apply, its signal and its publish, and its two durable timers |
| File | None | No file is read, built or delivered here; the pack and the filing documents are rwb-document's and rwb-litigation's |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.deviation`, module `deviation`, Java package `th.co.scb.ace.workbench.recovery.deviation.x5`; front end `src/modules/recovery/deviation/X5.tsx`, the fragment SCR-08 and SCR-06 embed, read only where the legacy screen block is read only.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/deviation/v1`; the two operations keep API-S8-001 and API-S8-002 | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 carries legacy AC4's fail-closed behaviour and the "writes the result to the decision log with the rule version" of the legacy feature. DP-13 renames the base and keeps the two operation IDs. DP-19 covers SCR-08 and SCR-06 only, and the screen model and the merge order stay with the edge contract. DP-01 and DP-02 stand behind the schema and the login and add no dependency; DP-15 applies the contract's DDL template through this service's own Flyway.

**Dependencies the table adds and the plan does not hold.** The pattern table adds the two H rows the metadata also carries, `RWB-PLT-E1027-CON` and `RWB-PLT-N001-CON`, and nothing else. Three consumed things have no row: the case contract of rwb-case, the reference-data read of the three lists (DP-07 is not in the pattern set) and the platform outbox behind the two published events (DP-09 is not in the pattern set either). They are recorded once as GAP-3059. The story builds against their fakes on Day 1 and no C dependency blocks the build (Template and Rules section R5.7 rule 2).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| DeviationController | Controller | API-S8-001 and API-S8-002 with the problem mapping for 401, 403, 404, 409, 422 and 503 |
| DeviationValidator | Service | The case and the caller's scope, `deviationCode` and `raisedBy` against their lists, the required fields of VR-S8-014-1 and the state the step needs |
| RuleEvaluation | Service through the embedded Drools kit | R-DEV-01, R-DEV-05 and R-DEV-15 with the rule package, the version in force and the reference rows; the version is pinned and recorded |
| DeviationDecisionWriter | Library adapter | One hash-linked record with the rule ID and the version in force, before any change; refuses the request when the write fails (DP-03) |
| DeviationWriter | Repository | The `deviation` row, its state, its handler and the idempotency row, in one `rwb_deviation` transaction |
| CaseAnnouncementClient | Client | The case read and the pause, resume and route announcement to rwb-case, one hop, 2 s, breaker, no retry of its own |
| DeviationEventPublisher | Outbox adapter | `DeviationRaised` and `DeviationCleared` in the CloudEvents envelope, written in the same transaction as the row |
| DeviationWorkflow | Workflow | The X5 slice on `rwb-deviation`, its two durable timers and its signals |
| X5 | React component | Shows the deviation, its code, handler, return point, contact stop and deadline on SCR-08 and SCR-06, with the refusal, not-recorded and failed states |

**Database and migrations.** No Flyway file of its own. `deviation` arrives with the S8 schema and the DDL template of `RWB-S8-E7005-CON`; the decision record and the idempotency key are library objects created in `rwb_deviation` by the library's migration (DP-03). The index set of `deviation` is Not specified in the source documents (GAP-3059; ASM-5170); this story needs a lookup by `case_id` for the queue and by `id` for the patch, and creates no index beyond what the contract template declares.

**Configuration and reference data.**

- The claim deadline behind R-DEV-05, as a versioned reference row. Its value is Not specified in the source documents (GAP-3059; ASM-5171).
- The deviation service level behind R-DEV-20 (10 working days), as a versioned reference row.
- The route of R-DEV-05 to the Legal handler, as a versioned reference row of code to handler role; the role code is Not specified in the source documents (GAP-3059; ASM-5172).
- LOV-DEVIATION, LOV-RAISED-BY and LOV-DEV-OUTCOME at their version in force (TSD S8 T3.2).
- The decision code of the R-DEV-05 and R-DEV-15 answers, read as a value of LOV-DECISION at its version in force.
- The 2 s budget and the single hop are the platform rule of ADR-020 and not a value of this story.

**Build steps**

1. Build `DeviationValidator` and `DeviationWriter` over the `deviation` row and the contract fake; test AC2 and X1 to X3.
2. Build `RuleEvaluation` and `DeviationDecisionWriter` against the library stub, with the stopped chain; test AC2, AC3 and AC4.
3. Build `DeviationWorkflow` with the claim-deadline timer and the SLA timer, and test the escalation of X6.
4. Build `CaseAnnouncementClient` against the case fake, with the pause, the route fact, the refusal and the delayed answer; test AC2, AC3, X7 and X8.
5. Build `DeviationEventPublisher` with the two events and the inbox repeat; test AC2 and X9.
6. Build `X5` and read the deviation through the composite route fake; test AC2.
7. Add the boundary test: no statement outside `rwb_deviation`, no `v_ace_*` read, no write to `rwb_case`, `rwb_litigation`, `rwb_document` or `rwb_decision`; test BR5.

**Feature flag.** `rwb.deviation.x5-v1`, read as a flag of the platform library; off means the X5 create answers 404 and SCR-08 shows no X5 row, while the read of an existing deviation and the other six codes are unaffected.

**Done when.** The tests of section 16 pass, the contract tests of `RWB-S8-E7005-CON` stay green, the boundary test runs in the pipeline, and a SIT week shows one deviation row per X5 flag, one decision record per rule answer, one pause per raise, one route fact per `BANKRUPTCY_FILED`, no write of a case, assignment, timer, legal-action or document row from this service, and no `v_ace_*` read in its logs.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S8-001 | The deviation is raised and routed (information), and the SLA or the deadline breach of X6 is reported with the same wording | {deviation} was raised. The case is with {handler}. |
| MSG-GEN-001 | A required field of the request is missing (X1) | Enter {field}. |
| MSG-P4-002 | The caller's role does not hold the right of the operation (X4) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the deviation changes (X5, AC4) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The four texts are the legacy wording of RWB-E7-005 section 14 and are copied unchanged; no message is reworded and no message identifier is added. `MSG-GEN-001` is displayed with the field it names and `MSG-S8-001` with the deviation and the handler. The 409 of X3, the 404 of X2 and the 503 of X7 carry the platform error envelope and no business message of this set, and the 409's message text is not stated in any source read for this key, so the story fixes only its status, its cause and its `messageId` slot.

### 15. Screens and states

No screen is built in this story. Two existing surfaces show what it writes, read through the gateway-bff composite route (DP-19):

| Screen | State | What the user sees or does |
|---|---|---|
| SCR-08 Deviation queue | Loading | The placeholder while the composite route answers |
| SCR-08 Deviation queue | List | The X5 deviations of the case with their code, handler, raised date, return point, contact stop, deadline and SLA state, and the case state from rwb-case |
| SCR-06 Raise deviation | Form | The raise form of API-S8-001: the code, `raisedBy`, the paused state and the contact stop |
| SCR-06 Raise deviation | Saved | The deviation raised with MSG-S8-001, the handler named and the deadline shown |
| SCR-08 Deviation queue | Not recorded | MSG-P7-003, and the deviation unchanged with the case clock not paused |
| SCR-08 Deviation queue | Refused | A role without the right reads MSG-P4-002 and nothing changes |
| SCR-08 Deviation queue | Failed | The answer of a refused pause or route fact, or a 503 when a consumed contract did not answer; the deviation keeps what it wrote |

The two screens and their `Loading; list` and `Form; saved` states are the ones the legacy screen block of RWB-E7-005 gives, copied unchanged; the refusal, not-recorded and failed states are the ones the exception paths of section 5 add. The route merges this service's answer with the case of rwb-case; the route path, the screen-model field list and the merge order belong to `RWB-PLT-N001-CON`, not here.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E7-005-02 | AC2 | Component | Deviation `DV-2026-000502` on case `RW-2026-000502`, code `X5`, `raisedBy` `OFFICER`, paused state `WITH_FCR_OFFICER`; the case fake at `DEV_FLAGGED`; the reference deadline row at its version; the handler set to the Legal route and the case announcement accepted |
| TC-E7-005-03 | AC3 | Component | The same deviation at `DEV_WITH_OWNER`; the case fake delivering `BANKRUPTCY_FILED`; R-DEV-15 firing; `DEV_REROUTE` with `outcome = RE_ROUTED` and the route fact accepted by the case fake |
| TC-E7-005-04 | AC4 | Component | The decision-record library stubbed to stop the chain; the deviation unchanged, no event published and MSG-P7-003 on the screen |
| TC-E7-005-05 | Access | Component | A role without the Case record right sends API-S8-001 and API-S8-002; refused with MSG-P4-002 and nothing written |
| TC-E7-005-06 | Principle 5 | NFR | A forced decision-record write failure on 10 deviations; no deviation changes, no event leaves the service and the incident is raised under R-UNI-39 |
| TC-S8-E7005-APP-01 | AC2 | Component | The claim-deadline timer and the 10-working-day SLA timer of `DeviationWorkflow`; the deadline reached before the filing, the escalation of R-DEV-20 and MSG-S8-001 |
| TC-S8-E7005-APP-02 | AC2, AC3 | Component | `DeviationRaised` and `DeviationCleared` with their three fields each in the CloudEvents envelope on `rwb.deviation.events.v1`, and a repeated delivery producing one effect and a counted repeat |
| TC-S8-E7005-APP-03 | BR5 | NFR | The boundary test: no statement outside `rwb_deviation`, no `v_ace_*` read, no write to `rwb_case`, `rwb_litigation`, `rwb_document` or `rwb_decision` |

The five legacy identifiers are the legacy identifiers of RWB-E7-005 in their legacy order, with their legacy covers and their legacy data; TC-E7-005-01 covers AC1, which this story does not own, and sits with `RWB-ITG-E7005-ITG`. The legacy `System` level of the first three maps to `Component` here, because the cross-service answers are the contract fakes and the whole run across the services is the harness story's; the access case keeps `Access` at `Component` and the forced-failure case keeps `Principle 5` at `NFR`. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the claim deadline, the SLA, the Legal route, the three list values and the decision code are data with a version; no role, list value, state name or code appears in Java.
- No personal data in logs, tests, workflow inputs or prompts: the row carries identifiers, codes and dates, and the customer's identity never enters this service or its history.
- ACE data only through the owner's contract or the owner's `v_ace_*` views: no component of this story reads an ACE view or an ACE table, and the service identity holds no `v_ace_*` grant (BR5).
- No read of another service's tables and no cross-schema join: the case, the filing, the pack and the ledger are reached only on their contracts, their events and their fakes (DP-01).
- One hop and a 2 s budget on each consumed call, with a breaker per downstream and no call chain; a hand-off is re-run by repeating the same `Idempotency-Key` and never by a silent resend.
- The decision is never recorded after the effect: the record is written first through the library, and a failed write stops the request with nothing changed (DP-03, R-UNI-39, MSG-P7-003).
- The prescription clock is never paused, and the case clock is paused only by the case of record on `DeviationRaised` (BR4).
- The two screens are read only except for the raise and the outcome patch; no screen calls an owner service directly (DP-19).
- Every example in the story is synthetic; no production payload and no production file is copied into a test or a fake.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Screens | Test cases |
|---|---|---|---|---|---|---|---|
| No requirement ID in the legacy master (GAP-3059; ASM-5170) | The X5 deviation is assigned to Legal, its deadline held and the case re-routed after the receiver reports, with the result recorded with its rule version | Epics 3 to 8 specification, E7 S8 row; FSD S8 v3 A2.14 | FEAT-DVF-05 | 04 Handle special situations | R-DEV-01, R-DEV-05, R-DEV-15, R-DEV-19, R-DEV-20, R-UNI-39, R-UNI-40, BR1 to BR7 | SCR-08, SCR-06 | TC-E7-005-02, TC-E7-005-03, TC-E7-005-04 |
| FEAT-DVF-05 | Run X5 bankruptcy and seizure end to end | Business Rules and Routing Logic v4 (R-DEV-05, R-DEV-15) | FEAT-DVF-05 | 04 Handle special situations | R-DEV-05, R-DEV-15 | SCR-08, SCR-06 | TC-E7-005-02 to TC-E7-005-06 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E7-005, disposition Split (rework) |
| Legacy criteria | AC2, AC3 and AC4, owned by this story and copied word for word in section 7; AC1 is owned by RWB-ITG-E7005-ITG |
| Legacy test cases | TC-E7-005-02 to TC-E7-005-06, kept in legacy order; TC-E7-005-01 sits with the harness story |
| Requirement | The legacy master, the Epics 3 to 8 specification and TSD S8 T8 carry no REQ identifier for this feature, so the story traces to FEAT-DVF-05 until the PRD adds the identifiers (GAP-3059) |
| Contract half | RWB-S8-E7005-CON: the two operations, the schemas, the `deviation` template, the `Idempotency-Key` rule and the fakes |
| Sibling slice | RWB-ITG-E7005-ITG and the other X1 to X7 stories of this service |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013 (19 services inside ACE), ADR-014 (schema and login per service), ADR-016 (reusable Temporal layer), ADR-020 (contract-first REST, one hop, 2 s timeout), ADR-022 (local decision record plus central ledger) |

### 19. Out of scope

- AC1 and the whole end-to-end run of X5 across the services: `RWB-ITG-E7005-ITG` and the wave 4 integration harness.
- The case of record, its stage clock, its prescription clock, its work assignment and its case task: rwb-case (P3) and the case-side story of this legacy family.
- The filing with the official receiver or the LED, the legal action, the court references and the enforcement steps: rwb-litigation (S4) and its own stories; this service holds the deadline and the handler only.
- The evidence pack, its documents and their custody: rwb-document (P5).
- The central ledger, the rule packages and the rule registry: rwb-decision (P7) and `RWB-PLT-E1027-CON`.
- The contact stop, the letters and the calls: rwb-comms (P6), which consumes `DeviationRaised` and `DeviationCleared`; the contact stop of FSD S8 A2.5 belongs to X1 to X3 and not to X5.
- The screening that may raise the flag: the screening agent of rwb-agent (P10) and the Epic 2 screening stories.
- The other six deviation codes and their route rules: the sibling X1, X2, X3, X4, X6 and X7 stories of this service.
- The contract document itself: `RWB-S8-E7005-CON`.
- The roles, rights, scope and masking data themselves, including the difference between the FSD primary role and TSD S8 T6.1: rwb-access (P4).
- The gateway-bff composite route, the screen field list and the layout of SCR-08 and SCR-06: `RWB-PLT-N001-CON` and the edge stories.
- The deployment of this build, its flag, its dashboards, its alerts and its runbook: its own OPS story.
