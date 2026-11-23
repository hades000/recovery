# RWB-ITG-E7001-ITG Run X1 dispute and complaint end to end

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-E7001-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W4 |
| Wave | 4 |
| Business epic | EP07 |
| Release | 31 May 2027 (tentative) |
| Legacy key | RWB-E7-001 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | L-ITG-W4 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | RWB-S8-E7001-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E7-001 as the wave 4 integration proof of the X1 dispute and complaint deviation, from the complaint and the flag through the contact stop, the complaint officer's handling, the evidence pack and the resolution to the resumed case and the return point, observed across rwb-deviation, rwb-case, rwb-document and rwb-decision; the build of the X1 flow is RWB-S8-E7001-APP. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **complaint officer**, I want **the X1 dispute and complaint deviation to stop contact and pause the stage clock while the prescription clock keeps running, pass to me as the named handler, carry the evidence pack, and resolve back to the exact decision the case paused in with its timers resumed, proved end to end against the real services**, so that **a complaint is always answered inside its service level and the customer's case is never left suspended, delayed or worked as if the complaint had not been made**.

This story builds the harness and the evidence, and nothing else. The flag, the contact stop, the X1 route, the two clocks, the resolution and the resume are built by S8 in RWB-S8-E7001-APP and its CON story; the case state and the timers are P3's, the evidence pack and its documents are P5's, and the decision record is written through P7's library. The harness raises and drives the deviation through S8's published operations, observes every hop through the owners' published contracts, and writes a run report per case. It builds no production endpoint, no table, no workflow, no activity, no schedule and no screen, and it writes no code in any service.

### 2. Business rationale

A customer disputes the balance or the security, or complains about how the case has been worked, and the case can carry on being chased through the same phone numbers while the complaint sits in a queue. That is the failure this story is written against, and R-UNI-04 and R-UNI-09 name it: a complaint logged against the case raises X1, pauses the stage clock and applies the contact stop the same day, and a disputed balance or security raises X1 and pauses recovery action on the disputed amount. The contact stop is the part that cannot be repaired afterwards — a dunning call made after a complaint is a conduct finding, not a late task.

The second half of the story is the return path, and it is where R-DEV-09 and R-DEV-18 meet the requirement. The resolution records the outcome and the same decision resumes; the clock resume returns the case to the exact state it paused in. REQ-S8-003 states the outcome from the business side: a complaint is resolved inside its service level and the case returns to the same decision with its timers resumed. A deviation that resumed into a new decision would re-run the route on a case whose facts have not changed, and a deviation that never resumed would leave a live case with no owner and a prescription running down against a bank that has stopped asking for its money. The Temporal design puts the two clocks on slide 24 as one line, "Stage clock paused; prescription never", and slide 24 also carries the undo rule, "Resume returns to the exact paused state". R-DEV-20 adds the limit on the handler's side: ten working days in DEV_WITH_OWNER and the deviation escalates to the team manager with the breach reported.

The harness is decoupled the way the services are. Every call is one hop on `/api/recovery/<short>/v1` with a 2 s budget (DP-11, DP-13). The decision record is written by S8 through the local decision-record library on `rwb.decision-record.v1` (DP-03) and read back through rwb-decision's contract; where a screen would compose these calls the path is the gateway-bff composite route (DP-19). No service's table is read and no view is opened: the case and the timers come from P3, the evidence pack from P5, the decisions and the rule rows from P7, and, where ACE data sits behind any of them, it is read only through rwb-source-data's contract (DP-01, DP-05). It carries REQ-S8-003 and the X1 rules R-DEV-01, R-DEV-02, R-DEV-09, R-DEV-18 and R-DEV-20 into evidence rather than restating them.

Two limits are stated here because they shape the whole run. The first is that the Ownership Map publishes two rwb-deviation operations for this flow, the raise and the patch, and no `GET /deviations`: the harness therefore never reads a deviation record, and asserts the deviation through the case read, the timers read, the decision log and the two deviation events. The second is that the contact stop has no published read of its own in this story — no contact plan operation and no notice operation — so the run asserts it through the case read that carries the deviation and its paused stage, and through the one `rwb.deviation.DeviationRaised.v1` consumption by rwb-comms, which is the event row that suppresses the notices. A notice count is not claimed anywhere in this file, because the map publishes no notice read to count.

### 3. Preconditions

- The published contracts of S8 rwb-deviation (the deviation raise and the patch), P3 rwb-case (the case and its timers), P5 rwb-document (the documents of a case), P7 rwb-decision (the decision log) and P4 rwb-access (the session) are in the contract registry, and a stub set is generated from each one.
- RWB-S8-E7001-APP owns the X1 flow, the contact stop, the two clocks and the resume; until it lands, the fixture of §12.8 stands in for its effect and the story is reported as a stub pass.
- FEAT-DVF-01 is the S8 feature and FEAT-DVH-04 is its screening dependency: the fixture holds an X1 code that screening has already produced, so this story never asserts a screening score, a confidence band or a human review threshold (R-DEV-01).
- The X1 rules are R-DEV-01 (pause the stage clock, keep the prescription clock, route to the named owner), R-DEV-02 (assign to the complaint officer), R-DEV-09 (record the outcome, the same decision resumes), R-DEV-18 (resume the stage clock and return the case) and R-DEV-20 (ten working days, then escalate to the team manager); the universal triggers are R-UNI-04 and R-UNI-09. The harness asserts those rules and changes none of them.
- The complaint service level of REQ-S8-003 and the outcome and reason codes of the resolution are business values held in the fixture, never in code.
- The harness environment and base hosts, the fixture layout, the synthetic case, deviation and complaint keys, the complaint outcome and reason codes, the evidence-pack answer shape, the evidence format and retention, and the pass or fail gate: Not specified in the source documents (GAP-0464; ASM-0656).
- The synthetic case, its deviation, its complaint reference, its documents, its timers and the business date are held in the fixture as data, not written in code.
- No build dependency. Day 1, with the stubs in place from the first run; the one wait is RWB-S8-E7001-APP, which replaces its stub and never blocks the lane.

### 4. Flow

1. Harness: loads the fixture: case `RW-2027-000701` in an active stage with the stage clock and the prescription clock running, deviation code `X1`, deviation `DEV-SYN-000701`, complaint `CMP-SYN-000701`, business date `2027-05-31`, and an evidence pack of three documents `DOC-SYN-000701-1` to `DOC-SYN-000701-3`. It takes a snapshot of the state, the stage and the remaining time of both clocks before it writes anything. On Day 1 the stubs of §12.8 return the same records.
2. Harness: raises the X1 deviation through `POST /api/recovery/deviation/v1/cases/{caseId}/deviations` with one Idempotency-Key, which starts DeviationWorkflow on the task queue `rwb-deviation`, and asserts the answer carries MSG-S8-001 with the deviation and the complaint officer as the handler, and that a repeat of the same key returns the same answer without a second deviation.
3. Harness: reads `GET /api/recovery/case/v1/cases/{caseId}` and asserts the case is in DEV_FLAGGED with deviation code X1, and reads `GET /api/recovery/case/v1/cases/{caseId}/timers` and asserts the stage clock is paused and the prescription clock is still running (R-DEV-01, R-UNI-04, Temporal design slide 24).
4. Harness: asserts the contact stop through the case read, which carries the deviation and the paused stage, and through the one `rwb.deviation.DeviationRaised.v1` consumption by rwb-comms that suppresses the notices; no contact plan is read, because the map publishes no contact operation for this story, and no notice count is claimed.
5. Harness: reads `GET /api/recovery/document/v1/cases/{caseId}/documents` and asserts the evidence pack of the complaint is on the case with its document count and its metadata only — never the content, and never a field that carries personal data (FEAT-DVF-01).
6. Harness: assigns the deviation to the complaint officer through `PATCH /api/recovery/deviation/v1/deviations/{deviationId}` with one Idempotency-Key, and asserts the case read answers DEV_WITH_OWNER with the complaint officer named as the handler (R-DEV-02). The deviation record itself is not read: the map publishes no `GET /deviations`.
7. Harness: counts one `rwb.deviation.DeviationRaised.v1` on `rwb.deviation.events.v1`, asserts its consumption is visible in the case read and in the contact stop, and replays it once and asserts the case, the timers and the decision log are unchanged, because the inbox holds one processed row per consumer.
8. Harness: reads `GET /api/recovery/decision/v1/decision-log?caseId={caseId}` and asserts one entry for the flag and one for the assignment, each with its rule id and rule version, and that `rwb.decision-record.DecisionRecorded.v1` was published on `rwb.decision-record.v1` and confirmed by the central ledger in rwb-decision (DP-03).
9. Harness: resolves the deviation through `PATCH /api/recovery/deviation/v1/deviations/{deviationId}` with the resolution step, the outcome held in the fixture and one Idempotency-Key, and asserts the case read answers DEV_RESOLVED with that outcome recorded (R-DEV-09).
10. Harness: asserts the service level of the resolution: the time in DEV_WITH_OWNER is inside the complaint service level of REQ-S8-003, and a variant held in the fixture runs past the deviation service level of R-DEV-20 and is asserted to escalate to the team manager with the breach reported while the state stays DEV_WITH_OWNER.
11. Harness: counts one `rwb.deviation.DeviationCleared.v1` on `rwb.deviation.events.v1` and asserts its consumption through the case read, then reads `GET /api/recovery/case/v1/cases/{caseId}` and asserts the case is back in the snapshot state, at the same stage and on the same decision, and reads `GET /api/recovery/case/v1/cases/{caseId}/timers` and asserts the stage clock is resumed with the time it had left and the prescription clock is still running (R-DEV-18, REQ-S8-003).
12. Harness: reads the decision log again and asserts one entry for the resolution and one for the resume, each with its rule id and rule version, so the four actions of the run carry four records and no action carries two.
13. Harness: replays the resolution with a forced failure of the decision-record write, and asserts the answer carries MSG-P7-003 and the case, the handler and both clocks are unchanged, with no entry and no `rwb.decision-record.DecisionRecorded.v1` for that action (AC6).
14. Harness: calls `GET /api/recovery/access/v1/me/session` as a synthetic caller with no Case record U, then raises a deviation on the case through `POST /api/recovery/deviation/v1/cases/{caseId}/deviations` and asserts 403 with MSG-P4-002 and no state change; then raises a deviation without its code and asserts MSG-GEN-001 naming the missing field (AC7).
15. Harness: writes one run report per case, keyed by story and case_no, naming the contract version of each hop, whether the hop was a stub or the owner, the deviation and complaint keys, the four states observed, the timer names and their remaining time, and the criteria verdicts.

### 5. Exception paths

| ID | Trigger | What the harness asserts | Message | ITG test case |
|---|---|---|---|---|
| X1 | A stub answers a shape the published contract does not allow | The run fails at that hop and the report names the service, the operation and the contract version; no criterion is marked passed | None | TC-E7-001-01-ITG (ITG AC1) |
| X2 | The flag is raised and the stage clock is not paused, or the prescription clock is paused with it | The run fails on AC2 and the report names the timer, the clock type and the state read; a paused prescription is a failure as serious as an unpaused stage | None | TC-E7-001-01-ITG (ITG AC2) |
| X3 | The case reaches DEV_WITH_OWNER but no handler is named, or the handler is a queue and not a role | The run fails on AC3 and the report names the case, the state and the handler it read, because a complaint without a named handler is the failure this story is written against | None | TC-E7-001-01-ITG (ITG AC3) |
| X4 | The resolution lands in DEV_RESOLVED but the case resumes into a different state, a different stage or a different decision | The run fails on AC4 and the report names the snapshot, the state read after the clear and, for each timer, the time it had left before and after | None | TC-E7-001-01-ITG (ITG AC4) |
| X5 | The decision record is written twice for one action, written without its rule version, or not confirmed by the central ledger | The run fails on AC5 and the report names the entries, their rule versions and the missing confirmation | None | TC-E7-001-04-ITG (ITG AC5) |
| X6 | A forced decision-record failure leaves the case changed, or answers without MSG-P7-003 | The run fails on AC6 and the report names the state before and after, the handler, both clocks and the answer | MSG-P7-003 (expected, and missing) | TC-E7-001-04-ITG (ITG AC6) |
| X7 | A caller without Case record U is allowed to raise a deviation, or a raise short of a required parameter is accepted | The run fails on AC7 and the report names the caller, the operation and the answer; a 201 is a failure even when no data changed | MSG-P4-002, MSG-GEN-001 (expected, and missing) | TC-E7-001-03-ITG (ITG AC7) |

The report text is for the wave entry check and is not part of the message standard. The business messages the run touches are in section 14 and are asserted by ID and by their substituted values.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Runs against the published contracts and the stubs from Day 1; the only wait is RWB-S8-E7001-APP, and its fixture answers until it lands |
| Negotiable | The fixture layout, the synthetic keys, the complaint outcome and reason codes, the timer names, the report shape and the gate are configuration agreed at the wave entry check, not business values in code |
| Valuable | The contact stop is proved to be same day, the two clocks are proved to pause and to keep running independently, the evidence pack is proved to be on the case, and the resume to the same decision with its timers is proved rather than assumed |
| Estimable | One runner, one stub set, one case fixture, one clock probe, one evidence-pack probe, one decision probe, one event observer and one report |
| Small | Fits in one sprint with its four tests |
| Testable | Each criterion runs against the stubs and again against RWB-S8-E7001-APP as it lands |

### 7. Acceptance criteria

```gherkin
Feature: Run X1 dispute and complaint end to end - wave 4 integration harness

  Background:
    Given the synthetic case "RW-2027-000701" carries deviation "DEV-SYN-000701" with deviation code "X1" and complaint reference "CMP-SYN-000701"
    Given the complaint was logged against the case on business date "2027-05-31" and the case is in an active stage with both clocks running
    Given the evidence pack of the complaint is held as three documents for the case and the rule package in force holds R-DEV-01, R-DEV-02, R-DEV-09 and R-DEV-18

  Scenario: AC1 Run X1 dispute and complaint end to end (legacy RWB-E7-001 AC1)
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then takes the dispute from detection through the evidence pack to resolution and the return point
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 The X1 flag pauses the stage clock, stops contact and keeps the prescription clock (new, D-RCV-60)
    Given the case "RW-2027-000701" is in an active stage with the stage clock and the prescription clock running
    When the complaint "CMP-SYN-000701" is raised against the case under R-UNI-04 and the deviation is raised through POST /api/recovery/deviation/v1/cases/{caseId}/deviations
    Then GET /api/recovery/case/v1/cases/{caseId} answers DEV_FLAGGED with deviation code "X1"
    And GET /api/recovery/case/v1/cases/{caseId}/timers shows the stage clock paused and the prescription clock still running
    And contact is stopped for the case and the one "rwb.deviation.DeviationRaised.v1" is consumed by rwb-case and rwb-comms

  Scenario: AC3 The complaint officer becomes the named handler (new, D-RCV-60)
    Given the case "RW-2027-000701" is in DEV_FLAGGED with deviation code "X1"
    When the deviation "DEV-SYN-000701" is patched with the owner-assigned step under R-DEV-02
    Then GET /api/recovery/case/v1/cases/{caseId} answers DEV_WITH_OWNER with the complaint officer named as the handler
    And the handler read is one named role for the case and not a queue or a team
    And the stage clock is still paused and the prescription clock is still running

  Scenario: AC4 The complaint resolves and the case resumes exactly where it paused (new, D-RCV-60)
    Given the case "RW-2027-000701" is in DEV_WITH_OWNER with the complaint officer as the handler
    When the deviation is resolved through PATCH /api/recovery/deviation/v1/deviations/{deviationId} under R-DEV-09 with the outcome held in the fixture
    Then GET /api/recovery/case/v1/cases/{caseId} answers DEV_RESOLVED with that outcome recorded
    And after the clear the case is read back in the state and at the stage the fixture recorded before the flag, with the same decision
    And GET /api/recovery/case/v1/cases/{caseId}/timers shows the stage clock resumed with the time it had left and the prescription clock still running

  Scenario: AC5 The decision record is written once per action with its rule version (new, D-RCV-60)
    Given the case carries deviation "DEV-SYN-000701" and the rule package in force holds R-DEV-01, R-DEV-02, R-DEV-09 and R-DEV-18
    When the flag, the assignment, the resolution and the resume have run
    Then GET /api/recovery/decision/v1/decision-log?caseId={caseId} holds one entry per action with its rule id and rule version
    And "rwb.decision-record.DecisionRecorded.v1" is published once per action on "rwb.decision-record.v1" and confirmed by the central ledger in rwb-decision
    And a replay of "rwb.deviation.DeviationRaised.v1" leaves the case, the timers and the decision log unchanged, because the inbox holds one processed row per consumer

  Scenario: AC6 A forced decision-record failure stops the action (new, D-RCV-60)
    Given the decision record for the case cannot be written
    When the deviation is resolved through PATCH /api/recovery/deviation/v1/deviations/{deviationId}
    Then the answer carries "MSG-P7-003"
    And the case is still read in DEV_WITH_OWNER with the same handler and the same paused stage clock
    And no decision log entry and no "rwb.decision-record.DecisionRecorded.v1" exist for that action

  Scenario: AC7 A caller without the Case record U right is refused (new, D-RCV-60)
    Given a synthetic caller with role "RW-OFF" and no Case record U
    When the caller raises a deviation through POST /api/recovery/deviation/v1/cases/{caseId}/deviations
    Then the answer is 403 with "MSG-P4-002"
    And no deviation is read on the case and no state changes
    And the stage clock and the prescription clock are unchanged
```

Legacy AC2 (the decision log cannot be written, and the action leaves nothing behind) is asserted here in AC6; the build of the X1 flow, the contact stop and the resume stays with RWB-S8-E7001-APP, and AC1 is the business outcome that whole flow has to reach.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A deviation in any state pauses the stage clock, keeps the prescription clock running and routes the case to the named owner | R-DEV-01, Business Rules and Routing Logic v4 line 383; Temporal and Drools design slide 24 |
| BR2 | An X1 deviation is assigned to the complaint officer | R-DEV-02, the same, line 384 |
| BR3 | On resolution the outcome is recorded and the same decision resumes | R-DEV-09, the same, line 391 |
| BR4 | The clock resume returns the case to the state it paused in, with the stage clock resumed and the case returned | R-DEV-18, the same, line 400 |
| BR5 | Time in DEV_WITH_OWNER beyond the deviation service level escalates to the team manager and the breach is reported; the service level is 10 working days | R-DEV-20, the same, line 402 |
| BR6 | A complaint logged against the case raises X1, pauses the stage clock and applies the contact stop, the same day | R-UNI-04, the same, line 408 |
| BR7 | A disputed balance or a disputed security raises X1 and pauses recovery action on the disputed amount, the same day | R-UNI-09, the same, line 413 |
| BR8 | A complaint is resolved inside its service level and the case returns to the same decision with its timers resumed | REQ-S8-003, Business Requirements Program v4 line 419 |
| BR9 | Every hop in the run is one REST call on the owner's base `/api/recovery/<short>/v1` with a 2 s timeout, never an in-process call and never a second hop | DP-11, DP-13 |
| BR10 | The decision record is written by the owning service through the local decision-record library on `rwb.decision-record.v1`, and the central ledger in rwb-decision confirms it | DP-03; ADR-022 |
| BR11 | No service's table and no recovery view is read: the case, the timers, the documents and the decisions come through their owners' contracts, and any ACE data behind them through rwb-source-data's data-product contract | DP-01, DP-05 |

The harness asserts these rules and changes none of them; the rules themselves are evaluated in RWB-S8-E7001-APP, the states and the timers are held by P3 rwb-case, the evidence pack is P5's, and the record is P7's.

### 9. State transitions

| From | Event | Condition | To | Owner of the change |
|---|---|---|---|---|
| ANY_STATE | DEVIATION_FLAGGED | a complaint or a dispute is logged, so deviation_code = X1 | DEV_FLAGGED | S8 rwb-deviation, DeviationWorkflow, R-DEV-01 and R-UNI-04; `rwb.deviation.DeviationRaised.v1` |
| DEV_FLAGGED | OWNER_ASSIGNED | deviation_code = X1 | DEV_WITH_OWNER | S8 rwb-deviation, R-DEV-02, assigning the complaint officer |
| DEV_WITH_OWNER | DEVIATION_RESOLVED | deviation_code = X1 and the outcome is recorded | DEV_RESOLVED | S8 rwb-deviation, R-DEV-09 |
| DEV_RESOLVED | CLOCK_RESUMED | any | RESUMED, in the state the case paused in | S8 rwb-deviation for the deviation state, P3 rwb-case for the case state and the timers, R-DEV-18 |

The four states are the deviation states of R-DEV-01, R-DEV-02, R-DEV-09 and R-DEV-18, and the case state is read through the P3 contract after every step. Both clocks are read through `GET /api/recovery/case/v1/cases/{caseId}/timers`: the stage clock is paused from DEV_FLAGGED and resumed at R-DEV-18 with the time it had left, and the prescription clock is never paused at any point in the run. The harness changes no state. Every change in the table is made by the owner: S8 holds the deviation and drives DeviationWorkflow, P3 holds the case state and the timers, P5 holds the documents, P7 holds the ledger. A state the harness had set by hand would prove nothing, so the report names the owner and the operation behind every value it asserts, and it carries the pre-flag snapshot beside the post-clear read.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-COMPLAIN, complaint officer | Is the handler of X1 under R-DEV-02; holds Case record U on the case; is the role the journey is written for and the role that resolves the complaint |
| RW-CASEOWN, case owner | Holds Case record U and owns the case again after the resume; RW-TEAMMGR is the escalation point of R-DEV-20 when the deviation sits past its service level |
| RW-OFF, RW-TRIBE, RW-PLATADM | Read only where their rights allow; RW-OFF is the refused caller of AC7 |
| RW-CONDUCT, conduct and QA officer | Reads the same evidence where their rights allow; the complaint and the contact stop are the material a conduct review asks for, and no conduct finding is produced here |
| QA lead | Owns the harness configuration, the fixtures, the report shape and the pass or fail gate |
| Integration lead | Owns the harness code, the stub set and the swap from a stub to the real service |
| The owning services' identities | S8 runs DeviationWorkflow and writes the decision record, P3 holds the case and the timers, P5 holds the evidence pack, P7 holds the ledger and P4 answers the session; they make every change the harness asserts |
| No delegation of authority level applies | The harness takes no business decision; authorisation is answered by rwb-access and the DoA is P4's |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-036 to DF-CAS-045 | deviation | deviation_code, raised_at, raised_by, paused_state, owner, outcome | Written through the rwb-deviation raise and patch, read back through the case and the timers |
| DF-CAS-001 to DF-CAS-023 | recovery_case | case_no, status, stage_code, primary_person_key | Read through the rwb-case contract |
| DF-WRK-027 to DF-WRK-036 | timer | timer_type, started_at, expires_at, paused_at | Read through the rwb-case timers contract |
| DF-WRK-009 to DF-WRK-016 | assignment | assignee_user_id, assigned_at, ended_at | Read through the rwb-case contract |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | decision_code, rule_id, rule_version | Read through the rwb-decision contract |
| DF-REF-001 to DF-REF-015 | rule_row | rule_id, rule_version, from_state, event_code | Read through the rwb-decision contract |
| DF-DOC-001 to DF-DOC-011 | document | document_type, case_id, doc_version, retention_class | Read through the rwb-document contract, as metadata only |

Field IDs are those in the Logical Data Model and Data Dictionary v8. The deviation is S8's, the case, the assignment and the timers are P3's, the decision log and the rule rows are P7's, and the document is P5's; the harness reads them only through those contracts and never from a schema. The harness owns no table and writes no row. The two deviation writes are S8's own published operations of §12.2, taken with one Idempotency-Key each; everything else in the table is read through the owner. The evidence pack is read as document metadata — type, version and retention class — and its content is never fetched, so no personal data enters the run record.

### 12. Contract

#### 12.1 REST operations provided

None. The harness is a test runner and provides no REST operation.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| POST | `/api/recovery/deviation/v1/cases/{caseId}/deviations` | S8 rwb-deviation | Raises the X1 deviation and starts DeviationWorkflow, with one Idempotency-Key (AC1, AC2, AC5, AC7) |
| PATCH | `/api/recovery/deviation/v1/deviations/{deviationId}` | S8 rwb-deviation | The owner-assigned step, the resolution and the resume step, with one Idempotency-Key (AC3, AC4, AC5, AC6) |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The case state and the handler after the flag, the assignment, the resolution and the resume (AC1 to AC7) |
| GET | `/api/recovery/case/v1/cases/{caseId}/timers` | P3 rwb-case | The stage clock and the prescription clock, and the time each had left (AC2, AC3, AC4, AC6, AC7) |
| GET | `/api/recovery/document/v1/cases/{caseId}/documents` | P5 rwb-document | The evidence pack of the complaint, as document metadata (AC1) |
| GET | `/api/recovery/decision/v1/decision-log?caseId={caseId}` | P7 rwb-decision | The decision record of the flag, the assignment, the resolution and the resume, with the rule version and the ledger confirmation (AC1, AC5, AC6) |
| GET | `/api/recovery/access/v1/me/session` | P4 rwb-access | The caller's roles and rights before a write (AC3, AC7) |

Every call is one hop on the owner's base `/api/recovery/<short>/v1` with a 2 s budget (DP-11, DP-13). No operation is invented in this story: each path is the owner's published operation in the Ownership Map, and where a screen would compose them the path would be the gateway-bff composite route (DP-19).

The map publishes no `GET /deviations` for S8, and this story does not pretend otherwise. The deviation is therefore asserted through three published reads — the case read for the state and the handler, the timers read for the two clocks and their remaining time, and the decision log for the record — plus the `rwb.deviation.DeviationRaised.v1` and `rwb.deviation.DeviationCleared.v1` publications. The two writes above are the only deviation operations the run uses, and both are the map's own. The contact stop is asserted through the case read and the rwb-comms consumption of the raised event, because the map publishes no contact-plan or notice operation for this flow.

#### 12.3 Events published

None. The harness publishes no Kafka event; it writes its report to the wave record.

#### 12.4 Events consumed

| Event | Topic | Producer | Use in the run |
|---|---|---|---|
| `rwb.deviation.DeviationRaised.v1` | `rwb.deviation.events.v1` | S8 rwb-deviation | Counts one publication after the X1 flag, names rwb-case, rwb-comms and rwb-treatment as the consumers of event row 06, and with the replay proves one processed row per consumer (AC2, AC5) |
| `rwb.deviation.DeviationCleared.v1` | `rwb.deviation.events.v1` | S8 rwb-deviation | Counts one publication when the deviation clears and the case leaves DEV_RESOLVED for its paused state (AC4) |
| `rwb.case.CaseStateChanged.v1` | `rwb.case.events.v1` | P3 rwb-case | Proves the four observed states are the four published for the case (AC2, AC3, AC4) |
| `rwb.decision-record.DecisionRecorded.v1` | `rwb.decision-record.v1` | S8 rwb-deviation through the local decision-record library (DP-03) | Proves the record was published once per action with its rule version and confirmed by the central ledger (AC5, AC6) |

The harness subscribes to the two topics under one consumer group of its own, counts publications and replays each event once. The consumer effect it reads is the case through the rwb-case operation of §12.2 and the contact stop through the rwb-comms consumption; the inbox row counts of rwb-treatment come from the consumer evidence in the run fixture, because that consumer exposes no operation in this story. `rwb.deviation.DeviationCleared.v1` is asserted by count and by the case state that follows it, since the map publishes no clear operation of its own to drive — the resume step of the patch is what produces it.

#### 12.5 Workflows and activities

None added. The harness exercises DeviationWorkflow, S8's child workflow on the task queue `rwb-deviation` in the `rwb-recovery` namespace, started through the deviation raise and continued through the patch: it is the workflow that carries the X1 route, the contact stop, the pause of the stage clock and the resume. It observes CaseWorkflow on `rwb-case`, the parent that receives the deviation through the case router as a signal and pauses and resumes the stage clock for the case, and whose child-per-stage shape is slide 25 of Arch v5 and slide 13 of the Temporal design. Both are stated here as observed and not built here; no workflow, activity or Schedule is created, changed or owned by this story.

#### 12.6 Schedules

None added. The X1 flag arrives as an event and the complaint arrives as a complaint, so nothing in the journey is on a cron: the harness starts the run with the raise operation and holds the service-level breach of the R-DEV-20 variant in its own fixture instead of waiting on a schedule. The timer check of JOB-05 is retired in favour of durable timers inside the workflows (Arch v5 slide 44), which is why the two clocks and the ten working days are read through the timers operation and not through a job.

#### 12.7 Tables owned

None. The harness owns no schema and no table (DP-01); deviation is S8's, recovery_case, assignment and timer are P3's, document is P5's, and decision_log_entry and rule_row are P7's.

#### 12.8 Contract fakes

| Fake | Contract | Stubbed answer in the run |
|---|---|---|
| Stub for rwb-deviation | `POST /cases/{caseId}/deviations`, `PATCH /deviations/{deviationId}` | Accepts the raise once per Idempotency-Key and answers MSG-S8-001 with deviation `DEV-SYN-000701` and the complaint officer as the handler; the patch accepts the owner-assigned step, the resolution and the resume step and keeps the same deviationId; a raise without its code answers MSG-GEN-001 naming the field |
| Stub for rwb-case | `GET /cases/{caseId}`, `GET /cases/{caseId}/timers` | Case `RW-2027-000701` in DEV_FLAGGED, then DEV_WITH_OWNER with the complaint officer, then DEV_RESOLVED, then the snapshot state again; the stage clock paused and then resumed with the time it had left, the prescription clock running throughout |
| Stub for rwb-document | `GET /cases/{caseId}/documents` | Three documents for the case, `DOC-SYN-000701-1` to `DOC-SYN-000701-3`, with type, version and retention class and no content |
| Stub for rwb-decision | `GET /decision-log?caseId={caseId}` | One entry per action with its rule id and rule version, and the central ledger confirmation |
| Stub for rwb-access | `GET /me/session` | Allows RW-COMPLAIN with Case record U; refuses RW-OFF with 403 and MSG-P4-002 |
| Complaint evidence fixture | The complaint, its outcome and the reason codes, and the service-level clock | Complaint `CMP-SYN-000701` with its outcome and reason codes held as data, its service level, and a breach variant that runs past the ten working days of R-DEV-20, at the point where the real handling would answer |

Each stub is generated from the published contract and its version is pinned in the run report, so a contract change shows up as a run failure and not as a silent pass. The harness environment and base hosts, the fixture layout, the synthetic case, deviation and complaint keys, the complaint outcome and reason codes, the evidence-pack answer shape, the evidence format and retention, and the pass or fail gate are Not specified in the source documents (GAP-0464; ASM-0656).

#### 12.9 Call-type summary

| Call type | In this story |
|---|---|
| REST | 0 provided, 7 consumed, one hop each on `/api/recovery/<short>/v1` with a 2 s budget (DP-11, DP-13) |
| Kafka | None published; four consumed, `rwb.deviation.DeviationRaised.v1`, `rwb.deviation.DeviationCleared.v1`, `rwb.case.CaseStateChanged.v1` and `rwb.decision-record.DecisionRecorded.v1`, counted and replayed once |
| Temporal | None added; DeviationWorkflow on `rwb-deviation` exercised from the raise and the patch, with CaseWorkflow on `rwb-case` observed as the parent that pauses and resumes the stage clock |
| File | None. The evidence pack is read as document metadata through the P5 contract; no file or claim-check is transferred by this story |

### 13. Solution plan

**Package.** Folder `itg/recovery`, package `th.co.scb.ace.workbench.recovery.itg`, test scope only; not part of any deployed service.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The H dependencies DP-03 and DP-19 add, RWB-PLT-E1027-CON and RWB-PLT-N001-CON, are platform stories delivered by the platform wave and are not repeated in the metadata H field of this story, which stays None; DP-13 adds nothing. The one blocking dependency is the I story RWB-S8-E7001-APP, which replaces its stub; until it is live the run uses the stub, and a stub pass is reported as a stub pass.

**Harness components**

| Component | Type | Responsibility |
|---|---|---|
| JourneyRunner | Job | Runs the seven owned criteria in order for a case and holds the run lock |
| DeviationDriver | Service | Raises the X1 deviation and patches the owner-assigned step, the resolution and the resume step, once per Idempotency-Key |
| ClockProbe | Service | Reads the timers and asserts the stage clock paused, the prescription clock running, the time left before and after the pause, and the resume |
| EvidencePackProbe | Service | Reads the documents of the case and asserts the pack is present with its type, version and retention class, and no content |
| DecisionProbe | Service | Reads the decision log and asserts one record per action, with its rule version and the ledger confirmation |
| EventObserver | Service | Subscribes to `rwb.deviation.events.v1`, `rwb.case.events.v1` and `rwb.decision-record.v1`, counts publications and replays each event once |
| StubSet | Fake | The five stubs and the complaint evidence fixture of §12.8, generated from the published contracts with the version pinned |
| EvidenceReport | Service | Writes one report per case keyed by story and case_no, with the pre-flag snapshot and the post-clear read, and holds the pass or fail gate |

**Environment and test data.** SIT, against the stubs from Day 1 and the real services as RWB-S8-E7001-APP lands, on synthetic case `RW-2027-000701`, deviation `DEV-SYN-000701`, complaint `CMP-SYN-000701`, documents `DOC-SYN-000701-1` to `DOC-SYN-000701-3` and business date `2027-05-31`. The harness seeds nothing by hand and never writes a schema row. The environment and base hosts, the fixture layout, the synthetic keys, the complaint outcome and reason codes, the evidence-pack answer shape, the evidence format and retention, and the pass or fail gate are Not specified in the source documents (GAP-0464; ASM-0656).

**Build steps**

1. Generate the five stubs and the complaint evidence fixture from the published contracts and pin each contract version in the run report; fail the run on a mismatch (X1).
2. Build the DeviationDriver for the raise and prove it is accepted once per Idempotency-Key and answers MSG-S8-001 with the deviation and the complaint officer as the handler (AC1).
3. Add AC2 on the case read and the timers read: DEV_FLAGGED with X1, the stage clock paused and the prescription clock still running, and the contact stop held through the case read and the rwb-comms consumption (X2).
4. Add the EvidencePackProbe for AC1: the three documents of the pack are read as metadata through the P5 contract and no content is fetched.
5. Add AC3 on the owner-assigned patch: DEV_WITH_OWNER with the complaint officer named, one named role and not a queue, with both clocks unchanged (X3).
6. Add AC4 on the resolution and the resume: DEV_RESOLVED with the outcome recorded, then the snapshot state and stage with the same decision and the stage clock resumed with the time it had left (X4).
7. Add the EventObserver for AC2 and AC4: one DeviationRaised publication with its consumers, one DeviationCleared publication, one CaseStateChanged per state, and a replay that changes nothing because the inbox holds one row per consumer.
8. Add the DecisionProbe for AC5 and AC6: one entry per action with its rule version, the ledger confirmation, then a forced write failure that leaves the case, the handler and both clocks untouched and answers MSG-P7-003 (X5, X6).
9. Add the access path for AC7 through the session read and the raise operation, and assert 403 with MSG-P4-002 and no state change, and MSG-GEN-001 for a raise short of its code (X7).
10. Add the R-DEV-20 service-level variant and the EvidenceReport gate, and swap a stub for the real owner as RWB-S8-E7001-APP lands.

**Feature switch.** None. The harness has no production flag and runs in the test environment only.

**Done when.** The tests of section 16 pass against the fakes and again against RWB-S8-E7001-APP when it lands, and the wave entry check holds a run report keyed by story and case_no with the pre-flag snapshot beside the post-clear read.

### 14. Validation and messages

| ID | Type | Message |
|---|---|---|
| MSG-S8-001 | Information | {deviation} was raised. The case is with {handler}. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The harness asserts the message ID and the substituted values on the answer it reads, and owns no message text. MSG-S8-001 is asserted with the deviation and the complaint officer as the handler when the X1 flag is raised (step 2, AC2). MSG-GEN-001 is asserted with the missing field name when a raise is made without its deviation code (step 14, AC7). MSG-P4-002 is asserted with the refused raise for a caller without Case record U (step 14, AC7). MSG-P7-003 is asserted when the decision record cannot be written and nothing changes (step 13, AC6).

### 15. Screens and states

The legacy story's screens are SCR-06 Raise deviation and SCR-08 Deviation queue, and neither is built or rendered here: the harness calls the two operations behind them and reads the states through the owners. What the wave entry check looks at instead is the run report, whose environment, layout and retention are Not specified in the source documents (GAP-0464; ASM-0656).

| State | Read through | What the run asserts |
|---|---|---|
| DEV_FLAGGED | rwb-case case read and timers read | The X1 flag is raised by the complaint, the case is flagged, contact is stopped and the stage clock is paused while the prescription clock runs |
| DEV_WITH_OWNER | rwb-case case read and timers read | The complaint officer is the named handler, the evidence pack is on the case, and the decision record exists with its rule version |
| DEV_RESOLVED | rwb-case case read | The complaint is resolved with its outcome recorded inside its service level, and the deviation clears |
| RESUMED | rwb-case case read and timers read | The case is back in the state and stage of the pre-flag snapshot, on the same decision, with the stage clock resumed and the prescription clock still running |
| A refused raise | rwb-access session read and the raise answer | 403 with MSG-P4-002 and no state change |

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E7-001-01-ITG | AC1 (legacy); ITG AC1, AC2, AC3 and AC4 | End to end | One case with an X1 complaint, the raise, the contact stop, the evidence pack, the assignment, the resolution and the resume live |
| TC-E7-001-02-ITG | AC2 (legacy, the not-recorded case); ITG AC6 | Integration | A forced decision-record failure on the resolution |
| TC-E7-001-03-ITG | Access; ITG AC7 | Component | A synthetic caller without Case record U, and a raise short of its code |
| TC-E7-001-04-ITG | Principle 5; ITG AC5 and AC6 | Integration | A forced decision-record failure at the point of the state change, with the state, handler and clocks read before and after, and the record read with its rule version and ledger confirmation |

The AC column names the legacy AC the copy derives from and the ITG AC it asserts, and the full legacy test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx under the same legacy test case ID. Legacy AC1 stays the business outcome of RWB-S8-E7001-APP, and legacy AC2 is the build criterion of that story; the -ITG copies here assert the same behaviour across the service boundary. AC2, AC3 and AC4 have no legacy test case of their own in this key, so they are asserted as the ordered steps of the one end-to-end journey in TC-E7-001-01-ITG, and AC5 is asserted with the decision-record checks of TC-E7-001-04-ITG.

### 17. Guardrails

- No business value in code: the synthetic case, deviation and complaint keys, the business date, the outcome and reason codes, the service level, the timer names and the report layout are data.
- No personal data in logs, events or reports: every key is synthetic, the events carry IDs and facts only, and the evidence pack is read as metadata and never as content.
- ACE data only through the owner's contract: the case, the timers, the documents and the decisions come from their owners, and ACE data behind them only through the P1 data-product contract, never a direct view read and never another service's schema (DP-01, DP-05).
- One hop and a 2 s budget per call, with a circuit breaker per downstream, so the harness fails where a screen would (DP-11, DP-13).
- No invented operation: only the two deviation writes and the five reads of §12.2, and the deviation and the contact stop are never asserted through a read the map does not publish.
- A stub pass is never reported as a real pass: the report names the contract version and whether the hop was a stub or the owner.
- The harness never runs against UAT or production, and it never writes a row by hand or sets a state it then asserts.
- A failing criterion is fixed in the owning service or raised as a gap; it is never waived in the script.

### 18. Traceability

| Item | Source | Where it lands |
|---|---|---|
| Legacy story RWB-E7-001 Run X1 dispute and complaint end to end | Recovery Workbench User Stories Epics 3 to 8 v3, lines 10941 to 11019 | Sections 1, 3, 11, 14 and 19 of this file |
| Legacy AC1, verbatim | The same, lines 10960 to 10964 | Section 7, AC1, marked (legacy RWB-E7-001 AC1) |
| Legacy AC2, the not-recorded case | The same, lines 10966 to 10970 | AC6 here; the legacy criterion also stays with RWB-S8-E7001-APP (section 19) |
| Legacy test cases TC-E7-001-01 to TC-E7-001-04 | The same, lines 11014 to 11017 | Copied as -ITG in section 16 |
| Legacy endpoints, screens, permission check and messages | The same, lines 10981 to 11008 | Sections 12.2, 15 and 14 |
| FEAT-DVF-01 Run X1 dispute and complaint end to end | Epics 3 to 8 Specification v3, line 124 | Sections 1 and 2 |
| REQ-S8-003, the complaint inside its service level and the same decision with its timers resumed | Business Requirements Program v4, line 419 | Section 8, BR8 |
| R-DEV-01, R-DEV-02, R-DEV-09, R-DEV-18 and R-DEV-20 | Business Rules and Routing Logic v4, lines 383, 384, 391, 400 and 402 | Sections 8 and 9 |
| R-UNI-04 and R-UNI-09, the complaint and the dispute raise X1 | The same, lines 408 and 413 | Section 8, BR6 and BR7 |
| The S8 deviation contract and its two events | Architecture v5 slides 15, 25 and 41 to 44; the S8 contract at lines 1049 to 1069 and the event rows 06 and 07 at lines 2918 and 2919 of the text extract | Sections 2, 12.2, 12.4 and 12.5 |
| DeviationWorkflow, the pause of the stage clock, the parent CaseWorkflow and "Resume returns to the exact paused state" | Temporal and Drools design slides 13 and 24, lines 1566 to 1661 | Sections 2, 8, 12.5 and 13 |
| DF-CAS-036 to DF-CAS-045, DF-CAS-001 to DF-CAS-023, DF-WRK-027 to DF-WRK-036, DF-WRK-009 to DF-WRK-016, DF-DEC-001 to DF-DEC-018, DF-REF-001 to DF-REF-015 and DF-DOC-001 to DF-DOC-011 | Logical Data Model and Data Dictionary v8 | Section 11 |
| DP-03, DP-13 and DP-19 | Template and Rules v1 §R5.5 | Section 13, pattern application |
| ADR-015, ADR-020 and ADR-022 | Architecture Decision Records v3, with ADR-015, ADR-020 and ADR-022 as added by Template and Rules v1 §R8.4 | Sections 12.4, 12.2 and 8: outbox and inbox on Kafka, contract-first REST with one hop and 2 s, local decision record plus central ledger |

### 19. Out of scope

- RWB-S8-E7001-CON and RWB-S8-E7001-APP: the build of the X1 route, the contact stop, the two clocks, the evidence-pack link, the resolution and the resume, and the decision record.
- The complaint evidence pack build in P5 and the document checklist: the pack is read as metadata through the contract, and no document is created, classified or retained here.
- The S8 deviation screening and the other six deviation codes (RWB-S8-E7002-* to RWB-S8-E7007-*), and the screening dependency FEAT-DVH-04.
- SCR-06 Raise deviation and SCR-08 Deviation queue, and every gateway-bff composite route.
- The platform stories and their H dependencies named in section 13, including RWB-PLT-E1027-CON and RWB-PLT-N001-CON.
- The conduct review of the complaint and the breach path of a contact sent while a block is on (FEAT-DVF-10): the same evidence serves it, and none of it is built or asserted here.
- Any production change: no endpoint, table, workflow, activity, schedule, screen, feature flag or configuration in any service.
