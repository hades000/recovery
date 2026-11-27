# RWB-ITG-E7006-ITG Run X6 lost contact and skip trace end to end

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-E7006-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W4 |
| Wave | 4 |
| Business epic | EP07 |
| Release | 31 May 2027 (tentative) |
| Legacy key | RWB-E7-006 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | L-ITG-W4 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | RWB-S8-E7006-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E7-006 as the wave 4 integration proof of the X6 lost contact and skip trace flow, driven from the deviation raise and observed across rwb-deviation, rwb-case and the decision log; the build of the flow is RWB-S8-E7006-APP and its CON story. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-ITG-E7006-ITG). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **case owner**, I want **the X6 lost contact flow to be proved end to end from the raise of the flag through the skip trace, the pause of the stage clock, the named owner and the return or the route, with the bureau, internal data and agency answers read through the owners' published contracts**, so that **every deviation has a handler and a clock, and no case waits on a lost contact that nobody is working**.

This story builds the wave 4 integration harness and the evidence it leaves, and nothing else. The X6 flow itself — the screening, the pause, the routing to the owner, the skip trace and the return — is built by S8 in RWB-S8-E7006-APP and its CON story. The harness raises the deviation through S8's published operation, observes every hop through the owners' published contracts, and writes a run report per case. It builds no production endpoint, no table, no workflow, no activity, no schedule and no screen, and it writes no code in any service.

### 2. Business rationale

A borrower who cannot be reached is the quiet failure of a recovery case. The case sits with an owner, the letters go out to an address nobody reads, the clock runs down, and the account arrives at the next decision untouched. The rule set already says what should happen: a lost contact raises X6, the stage clock pauses while the prescription clock keeps running, the agent works the skip trace through the bureau, the internal data and the agency, and the case either comes back to the state it paused in with a verified contact point or goes on to escalation or the route decision (R-DEV-06, R-DEV-16, R-DEV-17). What no document proves is that those steps actually join up across services: that the flag reaches the case, that the timer in rwb-case really pauses and resumes, that the agency instruction really leaves, that a verified contact point really closes X6, and that the decision is recorded once with the rule version that produced it.

That join is the whole point of an integration story. Each service is proved on its own by its own tests; nothing in the monolith's single transaction model survives the split, so the seams have to be proved where they are. A raise that leaves rwb-deviation and never reaches the case, a pause that stops the stage clock but also stops the legal clock, a close that cannot be told apart from a reroute, or a decision record written twice — each of those is invisible to a unit test and plain on the case record, the timer list and the decision log. This story reads exactly those three places.

The harness is decoupled the way the services are. Every call is one hop on `/api/recovery/<short>/v1` with a 2 s budget (DP-11, DP-13). ACE data and the partner answers are read only through the owners' contracts: DP01 Account and arrears and DP13 Money and closure through rwb-source-data (DP-05), the agency instruction through rwb-partner, the case and its timers through rwb-case. The decision record is written by S8 through the local decision-record library on `rwb.decision-record.v1` (DP-03) and read back through rwb-decision's contract; where a screen would compose these calls the path is the gateway-bff composite route (DP-19). It carries REQ-S8-004 and REQ-S8-001 into evidence rather than restating them.

### 3. Preconditions

- The published contracts of S8 rwb-deviation (raise and advance), P3 rwb-case (the case and its timers), P1 rwb-source-data (DP01, DP13 and freshness), S9 rwb-partner (partner instructions), P7 rwb-decision (the decision log) and P4 rwb-access (the session) are in the contract registry, and a stub set is generated from each one.
- The data product catalog holds DP01 Account and arrears and DP13 Money and closure, each with one system of record, so the contact data and the closure position of a case have one named owner before a value is asserted (FSD P1 v3, A2.2).
- S8 rwb-deviation runs DeviationWorkflow on the task queue `rwb-deviation`, and the case router in rwb-case delivers DeviationRaised and DeviationCleared to the CaseWorkflow, which pauses and resumes the stage clock (Temporal and Drools design slide 24).
- RWB-S8-E7006-APP owns the X6 screening, the pause, the routing, the skip trace and the return; until it lands, the stub of §12.8 stands in for its effect and the story is reported as a stub pass.
- The X1 to X7 route set is FEAT-DVF-01 to FEAT-DVF-07 and is not asserted here; the fixture holds one case with X6 raised, so this story never asserts another deviation code.
- The harness environment and base hosts, the fixture layout, the synthetic case and deviation keys, the skip-trace source answer shapes for the bureau, the internal data and the agency, the evidence format and retention, and the pass or fail gate: Not specified in the source documents (GAP-0471; ASM-0663).
- The synthetic case, its deviation, its two runs (a verified contact point and an exhausted trace) and the business date are held in the fixture as data, not written in code.
- No build dependency. Day 1, with the stubs in place from the first run; the one wait is RWB-S8-E7006-APP, which replaces its stub and never blocks the lane.

### 4. Flow

1. Harness: loads the fixture — case `RW-2027-001206` on business date 2027-04-30, deviation `DEV-SYN-001206` with deviation_code X6, and a second run of the same case whose skip trace is exhausted. On Day 1 the stubs of §12.8 return the same records.
2. Harness: reads `GET /api/recovery/access/v1/me/session` as a synthetic case owner and asserts Case record U before anything is raised.
3. Harness: raises X6 through `POST /api/recovery/deviation/v1/cases/{caseId}/deviations` with one Idempotency-Key, which starts DeviationWorkflow on the task queue `rwb-deviation`.
4. Harness: reads `GET /api/recovery/case/v1/cases/{caseId}` and asserts the X6 flag is on the case record, and reads `GET /api/recovery/case/v1/cases/{caseId}/timers` and asserts the stage clock is paused while the prescription clock keeps running.
5. Harness: advances the deviation through `PATCH /api/recovery/deviation/v1/deviations/{deviationId}` with the owner assignment, and asserts the case reaches DEV_WITH_OWNER with its handler named. There is no `GET /deviations` and no clear operation on the published contract, so every later state is asserted through the case, the timers and the decision log, never through a deviation read.
6. Harness: reads `GET /api/recovery/source-data/v1/data-products/DP01/records?caseId={caseId}` for the internal contact data behind the trace, then `GET /api/recovery/source-data/v1/data-products/freshness?product=DP01` and asserts the business date and the load time behind that read, so a stale product is never reported as a clean trace.
7. Harness: reads `GET /api/recovery/source-data/v1/data-products/DP13/records?caseId={caseId}` and records the closure position of the case beside the deviation. The run asserts the read answers with its own freshness; no rule in this story evaluates money.
8. Harness: reads `GET /api/recovery/partner/v1/partner/instructions` and asserts the agency instruction placed for the case, its status and, where it has returned, its result.
9. Harness: reads `GET /api/recovery/decision/v1/decision-log?caseId={caseId}` and asserts one entry for the raise and one for the routing, each with its rule id and rule version, and that `rwb.decision-record.DecisionRecorded.v1` was published on `rwb.decision-record.v1` and confirmed by the central ledger in rwb-decision.
10. Harness: counts `rwb.deviation.DeviationRaised.v1` on `rwb.deviation.events.v1`, asserts one publication and the case effect once, then replays it and asserts the case is unchanged, because the inbox holds one processed row per consumer.
11. Harness: advances the same deviation with a verified contact point through `PATCH /api/recovery/deviation/v1/deviations/{deviationId}` and asserts X6 is closed, the case returns to the state it paused in and the stage clock resumes, with `rwb.deviation.DeviationCleared.v1` published once on the same topic.
12. Harness: runs the second fixture, where the trace is exhausted, reads the timers to assert the 30-day clock, then advances the deviation and asserts the case routes to escalation or to the route decision with DEV_REROUTE.
13. Harness: forces the decision-record failure on the raise, asserts the case and its timers are unchanged and the answer carries MSG-P7-003.
14. Harness: calls `GET /api/recovery/access/v1/me/session` as a synthetic caller whose role holds no Case record U, then raises the deviation through the same POST path and asserts 403 with MSG-P4-002 and no state change.
15. Harness: writes one run report per case, keyed by story and case_no, naming the contract version of each hop, whether the hop was a stub or the owner, the deviation id, the two route outcomes, the timer evidence and the decision-record confirmation.

### 5. Exception paths

| ID | Trigger | What the harness asserts | Message | ITG test case |
|---|---|---|---|---|
| X1 | A stub answers a shape the published contract does not allow | The run fails at that hop and the report names the service, the operation and the contract version; no criterion is marked passed | None | TC-E7-006-01-ITG (ITG AC1) |
| X2 | The raise answers 200 and no X6 flag is on the case record | The run fails on AC2 and the report names the case, the deviation id and the case read | None | TC-E7-006-01-ITG (ITG AC2) |
| X3 | The stage clock keeps running after the flag, or the prescription clock pauses with it | The run fails on AC2 and the report names the two timers and their status, because pausing the legal clock is a failure even when the case looks right | None | TC-E7-006-01-ITG (ITG AC2) |
| X4 | The skip trace returns a verified contact point and X6 stays open, or the case does not return to the state it paused in | The run fails on AC3 and the report names the case, the deviation id and the timer evidence | None | TC-E7-006-01-ITG (ITG AC3) |
| X5 | The skip trace is exhausted and the case neither escalates nor reaches the route decision | The run fails on AC3 and the report names the case, the 30-day clock and the route the case is left in | None | TC-E7-006-01-ITG (ITG AC3) |
| X6 | The decision record exists zero times or twice, or the ledger has not confirmed it | The run fails on AC4 and the report names the decision entries, their rule versions and the missing or duplicate confirmation; strict mode is never assumed | MSG-P7-003 (expected when the record cannot be written) | TC-E7-006-04-ITG (ITG AC5) |
| X7 | The decision record cannot be written and the case still changes | The run fails on AC5 and the report names the case, the timers and the state that moved; a change without a record is a failure whatever the answer says | MSG-P7-003 | TC-E7-006-04-ITG (ITG AC5) |
| X8 | A caller without Case record U is allowed to raise the deviation | The run fails on AC6 and the report names the caller role, the operation and the answer; a 200 is a failure even when no data changed | MSG-P4-002 (expected, and missing) | TC-E7-006-03-ITG (ITG AC6) |

The report text is for the wave entry check and is not part of the message standard. The business messages the run touches are in section 14 and are asserted by ID and by their substituted values.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Runs against the published contracts and the stubs from Day 1; the only wait is RWB-S8-E7006-APP, and its fixture answers until it lands |
| Negotiable | The fixture layout, the skip-trace answer shapes, the report shape and the gate are configuration agreed at the wave entry check, not business values in code |
| Valuable | The pause is proved to stop the stage clock and not the legal clock, the skip trace is proved to route on its result both ways, and the decision record is proved to be written once |
| Estimable | One runner, one stub set, two fixture runs, one timer probe, one instruction probe, one event observer and one report |
| Small | Fits in one sprint with its four tests |
| Testable | Each criterion runs against the stubs and again against RWB-S8-E7006-APP as it lands |

### 7. Acceptance criteria

```gherkin
Feature: Run X6 lost contact and skip trace end to end - wave 4 integration harness

  Background:
    Given the synthetic case "RW-2027-001206" holds the deviation "DEV-SYN-001206" with deviation_code X6 on business date "2027-04-30"
    Given the case is in a stage state whose stage clock is paused and whose prescription clock is running
    Given the bureau, the internal data and the agency answer through the stubs of section 12.8

  Scenario: AC1 Run X6 lost contact and skip trace end to end (legacy RWB-E7-006 AC1)
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then runs the skip trace through the bureau, internal data and agency sources and routes on the result
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 The X6 flag pauses the stage clock and names its owner (new, D-RCV-60)
    Given the case "RW-2027-001206" carries no X6 flag
    When the case owner raises X6 through POST /api/recovery/deviation/v1/cases/{caseId}/deviations
    Then the X6 flag is on the case record read through GET /api/recovery/case/v1/cases/{caseId}
    And the stage clock is paused while the prescription clock keeps running, read through GET /api/recovery/case/v1/cases/{caseId}/timers
    And the deviation is with its named owner, "Agent, case owner", and the case reaches DEV_WITH_OWNER

  Scenario: AC3 The skip trace routes on its result (new, D-RCV-60)
    Given the X6 deviation "DEV-SYN-001206" is with its owner and the skip trace has run through the bureau, the internal data and the agency
    When a contact point is verified for the case
    Then X6 is closed and the case returns to the state it paused in, and the stage clock resumes
    When the skip trace is exhausted instead
    Then the case routes to escalation or to the route decision after the 30-day clock, read through GET /api/recovery/case/v1/cases/{caseId}/timers

  Scenario: AC4 The decision record is written once and the deviation event is published once (new, D-RCV-60)
    Given X6 "DEV-SYN-001206" is raised, routed and closed on case "RW-2027-001206"
    When the run reads GET /api/recovery/decision/v1/decision-log?caseId={caseId}
    Then one entry exists for the raise and one for the routing, each with its rule id and rule version
    And "rwb.decision-record.DecisionRecorded.v1" is published on "rwb.decision-record.v1" and confirmed by the central ledger in rwb-decision
    And "rwb.deviation.DeviationRaised.v1" is published once on "rwb.deviation.events.v1" and consumed once by rwb-case
    And "rwb.deviation.DeviationCleared.v1" is published once on the same topic when the contact point is verified, and a replay of either event leaves the case and its timers unchanged

  Scenario: AC5 A forced decision-record failure stops the action (new, D-RCV-60)
    Given the decision record cannot be written for case "RW-2027-001206"
    When the case owner raises X6 through POST /api/recovery/deviation/v1/cases/{caseId}/deviations
    Then nothing changes on the case and on its timers
    And the answer carries "MSG-P7-003"

  Scenario: AC6 A caller without the Case record U right is refused (new, D-RCV-60)
    Given a synthetic caller whose role holds no Case record U
    When the caller raises X6 through POST /api/recovery/deviation/v1/cases/{caseId}/deviations
    Then the answer is 403 with "MSG-P4-002"
    And no state changes
```

Legacy AC2 (the decision log cannot be written, "Not recorded") belongs to RWB-S8-E7006-APP; this harness asserts the same failure through AC5.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A deviation X1 to X7 pauses the stage clock, keeps the prescription clock running and routes to the named owner on the same day | R-DEV-01 |
| BR2 | For X6 and X7 the agent handles within policy and the case owner stays accountable; the flag moves from DEV_FLAGGED to DEV_WITH_OWNER | R-DEV-06 |
| BR3 | When X6 is with its owner and a contact point is verified, X6 closes and the case returns to the state it paused in | R-DEV-16 |
| BR4 | When X6 is with its owner and the skip trace is exhausted, the case routes to escalation or to the route decision within 30 days | R-DEV-17 |
| BR5 | When a new verified contact point arrives, the contact data product is updated and X6 is closed if it is open, the same day | R-UNI-12 |
| BR6 | Every call the harness makes is one hop on the owner's base `/api/recovery/<short>/v1` with a 2 s budget, never an in-process call | DP-11, DP-13 |
| BR7 | ACE data and the partner answers are read only through the owners' contracts — DP01 and DP13 of rwb-source-data and the partner instructions of rwb-partner — never from a view or another service's schema | DP-01, DP-05, DP-13 |
| BR8 | The result of every decision is written as a decision record with its rule id and rule version, and confirmed in the central ledger | DP-03; ADR-022 |

The harness asserts these rules and changes none of them; the rules themselves are evaluated in RWB-S8-E7006-APP.

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| ANY_STATE | DEVIATION_FLAGGED | deviation_code = X6 raised on the case | DEV_FLAGGED |
| DEV_FLAGGED | OWNER_ASSIGNED | deviation_code in (X6, X7) | DEV_WITH_OWNER |
| DEV_WITH_OWNER | CONTACT_RESTORED | a contact point is verified | DEV_RESOLVED |
| DEV_WITH_OWNER | CONTACT_NOT_FOUND | the skip trace is exhausted inside the 30-day clock | DEV_REROUTE |

DEVIATION_FLAGGED, OWNER_ASSIGNED, CONTACT_RESTORED and CONTACT_NOT_FOUND are the event codes of R-DEV-01, R-DEV-06, R-DEV-16 and R-DEV-17. The flag is raised and owned in S8 rwb-deviation, which runs DeviationWorkflow; the owner named at DEV_WITH_OWNER is the Agent with the case owner accountable (R-DEV-06); the close at DEV_RESOLVED and the route at DEV_REROUTE are the case owner's (R-DEV-16, R-DEV-17); and P3 rwb-case holds the case state and its timers while P7 rwb-decision holds the central ledger. The harness changes no state. Every change in the table is made by the owner. A state the harness had set by hand would prove nothing, so the report names the owner and the operation behind every value it asserts.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-CASEOWN, case owner | Raises X6, holds the case through the pause and closes or reroutes it; holds Case record U and is the role the journey is written for |
| RW-RESTRUCT, RW-SPECIAL, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-ENFORCE, RW-SALEOFF | Hold Case record U on the same capability area and may raise and work a deviation where their rights allow |
| A synthetic caller with no Case record U | The refused caller of AC6; the fixture names its role, and the run asserts the refusal, not the identity |
| QA lead | Owns the harness configuration, the fixtures, the report shape and the pass or fail gate |
| Integration lead | Owns the harness code, the stub set and the swap from a stub to the real service |
| The owning services' identities | S8 runs DeviationWorkflow and writes the decision record, P3 holds the case and its timers, P1 answers the data products, S9 holds the agency instruction, P7 holds the ledger and P4 answers the session; they make every change the harness asserts |
| No delegation of authority level applies | The harness takes no business decision; authorisation is answered by rwb-access and the DoA is P4's |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-036 to DF-CAS-045 | deviation | deviation_code, case_id, raised_at, raised_by, paused_state | Read through the rwb-deviation contract and the case record |
| DF-CAS-001 to DF-CAS-023 | recovery_case | case_no, status, stage_code | Read through the rwb-case contract |
| DF-WRK-009 to DF-WRK-016 | assignment | case_id, holder, assigned_at | Read through the rwb-case contract |
| DF-WRK-027 to DF-WRK-036 | timer | case_id, task_id, timer_type, started_at, expires_at, status | Read through the rwb-case contract |
| DF-PRT-001 to DF-PRT-007 | partner | partner_code, partner_type, panel_status, contract_end | Read through the rwb-partner contract, for the agency instruction |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | decision_code, rule_id, rule_version, model_version | Read through the rwb-decision contract |
| DF-REF-001 to DF-REF-015 | rule_row | rule_id, rule_version, route_set, from_state, event_code | Read through the rwb-decision contract |

Field IDs are those in the Logical Data Model and Data Dictionary v9. The deviation is S8's, the case, the assignment and the timers are P3's, the partner and its instruction are S9's, the decision log and the rule rows are P7's, and the ACE side is DP01 and DP13 of P1's contract. The harness reads them only through those contracts and never from a schema. The harness owns no table and writes no row.

### 12. Contract

#### 12.1 REST operations provided

None. The harness is a test runner and provides no REST operation.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| POST | `/api/recovery/deviation/v1/cases/{caseId}/deviations` | S8 rwb-deviation | Raises X6 on the case; the trigger of every criterion, with one Idempotency-Key (AC1, AC2, AC5, AC6) |
| PATCH | `/api/recovery/deviation/v1/deviations/{deviationId}` | S8 rwb-deviation | Advances the deviation to its owner, records the verified contact point and records the exhausted trace (AC2, AC3, AC4) |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The X6 flag on the case record, the case state and the handler (AC2, AC3, AC4, AC5) |
| GET | `/api/recovery/case/v1/cases/{caseId}/timers` | P3 rwb-case | The paused stage clock, the running prescription clock and the 30-day clock (AC2, AC3, AC5) |
| GET | `/api/recovery/source-data/v1/data-products/DP01/records?caseId={caseId}` | P1 rwb-source-data | The internal contact data behind the trace (AC1, AC3) |
| GET | `/api/recovery/source-data/v1/data-products/DP13/records?caseId={caseId}` | P1 rwb-source-data | The closure position of the case, recorded in the report (AC1) |
| GET | `/api/recovery/source-data/v1/data-products/freshness?product=DP01` | P1 rwb-source-data | The business date and the load time behind the DP01 read (AC1, AC3) |
| GET | `/api/recovery/partner/v1/partner/instructions` | S9 rwb-partner | The agency instruction placed for the case, its status and its result (AC1, AC3) |
| GET | `/api/recovery/decision/v1/decision-log?caseId={caseId}` | P7 rwb-decision | The decision record of the raise and the routing, with the rule version, and the ledger confirmation (AC1, AC4, AC5) |
| GET | `/api/recovery/access/v1/me/session` | P4 rwb-access | The caller's roles and rights before the raise (AC6) |

Every call is one hop on the owner's base `/api/recovery/<short>/v1` with a 2 s budget (DP-11, DP-13). No operation is invented in this story: each path is the owner's published operation, and where a screen would compose them the path would be the gateway-bff composite route (DP-19). S8 publishes the raise and the advance only — there is no `GET` on the deviations resource and no clear operation — so the harness never reads or clears a deviation directly: it asserts every deviation state through the case, the timers and the decision log. The X1 to X7 route set and the other six flows are FEAT-DVF-01 to FEAT-DVF-07 and are not asserted here.

#### 12.3 Events published

None. The harness publishes no Kafka event; it writes its report to the wave record.

#### 12.4 Events consumed

| Event | Topic | Producer | Use in the run |
|---|---|---|---|
| `rwb.deviation.DeviationRaised.v1` | `rwb.deviation.events.v1` | S8 rwb-deviation | Counts one publication after the raise and, with the replay, proves one processed row per consumer (AC4) |
| `rwb.deviation.DeviationCleared.v1` | `rwb.deviation.events.v1` | S8 rwb-deviation | Counts one publication when the contact point is verified, and proves the clear reached the case once (AC4) |
| `rwb.case.CaseStateChanged.v1` | `rwb.case.events.v1` | P3 rwb-case | Shows the case reaching DEV_WITH_OWNER and returning to the paused state, once each (AC2, AC3, AC4) |
| `rwb.source-data.AceDataReady.v1` | `rwb.source-data.events.v1` | P1 rwb-source-data | Anchors the business date the run is worked on, so the deviation screening is never asserted against a date that has not loaded (AC1) |
| `rwb.decision-record.DecisionRecorded.v1` | `rwb.decision-record.v1` | S8 rwb-deviation through the local decision-record library (DP-03) | Proves the raise and the routing were recorded and confirmed by the central ledger before the case moved on (AC4, AC5) |

The harness subscribes to the four topics under one consumer group of its own, counts publications and replays each event once. The consumer effect it reads is the case through the rwb-case operation of §12.2; the inbox row counts of rwb-comms and rwb-treatment come from the consumer evidence in the run fixture, because neither consumer exposes an operation in this story.

#### 12.5 Workflows and activities

None added. The harness exercises DeviationWorkflow, S8's child workflow on the task queue `rwb-deviation` in the `rwb-recovery` namespace, which can start at any time and pauses the stage clock; and it observes CaseWorkflow, P3's parent on the task queue `rwb-case`, which receives the deviation through the case router and pauses and resumes its stage timer. Both are stated here as observed and not built here; no workflow, activity or Schedule is created, changed or owned by this story.

#### 12.6 Schedules

None added. X6 is raised on a case at any time, not on a clock, and the harness starts the journey with the raise operation; it sets no cron, overlap policy or catch-up window. The morning deviation screening that runs after AceDataReady is S8's and is not asserted here.

#### 12.7 Tables owned

None. The harness owns no schema and no table (DP-01); deviation is S8's, recovery_case, assignment and timer are P3's, partner and its instruction are S9's, decision_log_entry and rule_row are P7's, and the ACE side belongs to the data products behind P1's contract.

#### 12.8 Contract fakes

| Fake | Contract | Stubbed answer in the run |
|---|---|---|
| Stub for rwb-deviation | `POST /cases/{caseId}/deviations`, `PATCH /deviations/{deviationId}` | Accepts the raise once per Idempotency-Key on case `RW-2027-001206`, then answers the advance to DEV_WITH_OWNER, the verified contact point and the exhausted trace, and refuses to answer a deviation read because no such operation is published |
| Stub for rwb-case | `GET /cases/{caseId}`, `GET /cases/{caseId}/timers` | Case `RW-2027-001206` with the X6 flag, its state after each advance, a paused stage clock, a running prescription clock and the 30-day clock on the exhausted run |
| Stub for rwb-source-data | DP01 records, DP13 records, freshness | The internal contact data of the case, the closure position with no rule applied, and business date 2027-04-30 with a load time for DP01 |
| Stub for rwb-partner | `GET /partner/instructions` | One agency instruction for the case with its status, and its result once the trace returns |
| Stub for rwb-decision | `GET /decision-log?caseId={caseId}` | One entry for the raise and one for the routing, each with its rule id and rule version, and the ledger confirmation |
| Stub for rwb-access | `GET /me/session` | Allows RW-CASEOWN with Case record U; refuses the synthetic caller that holds none with 403 and MSG-P4-002 |
| Skip-trace fixture (bureau, internal data and agency side) | The NCB, EFS and agency answers of the trace | A verified contact point on the first run and an exhausted trace on the second, at the point where the real adapters would answer |

Each stub is generated from the published contract and its version is pinned in the run report, so a contract change shows up as a run failure and not as a silent pass. The harness environment and base hosts, the fixture layout, the synthetic case and deviation keys, the skip-trace source answer shapes for the bureau, the internal data and the agency, the evidence format and retention, and the pass or fail gate are Not specified in the source documents (GAP-0471; ASM-0663).

#### 12.9 Call-type summary

| Call type | In this story |
|---|---|
| REST | 0 provided, 10 consumed, one hop each on `/api/recovery/<short>/v1` with a 2 s budget (DP-11, DP-13) |
| Kafka | None published; five consumed, `rwb.deviation.DeviationRaised.v1`, `rwb.deviation.DeviationCleared.v1`, `rwb.case.CaseStateChanged.v1`, `rwb.source-data.AceDataReady.v1` and `rwb.decision-record.DecisionRecorded.v1`, counted and replayed once |
| Temporal | None added; DeviationWorkflow on `rwb-deviation` exercised from the raise, and CaseWorkflow on `rwb-case` observed as it pauses and resumes its stage timer |
| File | None. No file run is asserted; the trace answer reaches the run through the partner instruction and the case read |

### 13. Solution plan

**Package.** Folder `itg/recovery`, package `th.co.scb.ace.workbench.recovery.itg`, test scope only; not part of any deployed service.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The H dependencies DP-03 and DP-19 add, RWB-PLT-E1027-CON and RWB-PLT-N001-CON, are platform stories delivered by the platform wave and are not repeated in the metadata H field of this story, which stays None; DP-13 adds none. The one blocking dependency is the I story RWB-S8-E7006-APP, which replaces its stub; until it is live the run uses the stub, and a stub pass is reported as a stub pass.

**Harness components**

| Component | Type | Responsibility |
|---|---|---|
| JourneyRunner | Job | Runs the four owned criteria in order for a case and holds the run lock |
| CaseOwnerDriver | Service | Reads the session, raises X6 once per case with one Idempotency-Key and advances the deviation through each step |
| ClockProbe | Service | Reads the case timers and asserts the stage clock paused, the prescription clock running and the 30-day clock on the exhausted run |
| SourceReadBack | Service | Reads DP01 and DP13 with the freshness stamp, and names the business date behind the contact data |
| AgencyInstructionProbe | Service | Reads the partner instruction of the case, its status and its result |
| EventObserver | Service | Subscribes to `rwb.deviation.events.v1`, `rwb.case.events.v1`, `rwb.source-data.events.v1` and `rwb.decision-record.v1`, counts publications and replays each event once |
| LedgerConfirm | Service | Reads the decision log and asserts one entry per decision with its rule version and the central ledger confirmation |
| StubSet | Fake | The six stubs and the skip-trace fixture of §12.8, generated from the published contracts with the version pinned |
| EvidenceReport | Service | Writes one report per case keyed by story and case_no, and holds the pass or fail gate |

**Environment and test data.** SIT, against the stubs from Day 1 and the real services as RWB-S8-E7006-APP lands, on the synthetic case `RW-2027-001206`, deviation `DEV-SYN-001206` and business date 2027-04-30, in two runs: a verified contact point and an exhausted trace. The harness seeds nothing by hand and never writes a schema row. The environment and base hosts, the fixture layout, the synthetic case and deviation keys, the skip-trace source answer shapes for the bureau, the internal data and the agency, the evidence format and retention, and the pass or fail gate are Not specified in the source documents (GAP-0471; ASM-0663).

**Build steps**

1. Generate the six stubs and the skip-trace fixture from the published contracts and pin each contract version in the run report; fail the run on a mismatch (X1).
2. Build the CaseOwnerDriver and prove the raise is accepted once per Idempotency-Key and the X6 flag appears on the case record (AC2, X2).
3. Add the ClockProbe for AC2: the stage clock paused, the prescription clock still running, and the deviation with its named owner (X3).
4. Add the SourceReadBack and the AgencyInstructionProbe for AC1 and AC3: DP01 with its freshness, DP13 recorded without a rule, and the agency instruction with its result.
5. Prove the verified contact point path for AC3: X6 closes, the case returns to the state it paused in and the stage clock resumes (X4).
6. Prove the exhausted path for AC3: the 30-day clock is read and the case reaches escalation or the route decision (X5).
7. Add the LedgerConfirm for AC4: one entry for the raise and one for the routing with their rule versions, and the ledger confirmation before the case moved on (X6).
8. Add the EventObserver for AC4: one DeviationRaised, one DeviationCleared and the case effect once, with a replay that changes nothing because the inbox holds one row per consumer.
9. Add the forced decision-record failure for AC5 and assert nothing moves and MSG-P7-003 is carried (X7).
10. Add the access path for AC6 through the session read and the raise, then the EvidenceReport and the gate, and swap a stub for the real owner as RWB-S8-E7006-APP lands (X8).

**Feature switch.** None. The harness has no production flag and runs in the test environment only.

**Done when.** The tests of section 16 pass against the fakes and again against RWB-S8-E7006-APP when it lands, and the wave entry check holds a run report keyed by story and case_no.

### 14. Validation and messages

| ID | Type | Message |
|---|---|---|
| MSG-S8-001 | Information | {deviation} was raised. The case is with {handler}. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The harness asserts the message ID and the substituted values on the answer it reads, and owns no message text. MSG-S8-001 is asserted on the raise answer with the deviation id and the handler, where the screen would show it; MSG-GEN-001 with the missing field when a read is made short of a required parameter; MSG-P4-002 with the refused action on the raise; and MSG-P7-003 when the decision record cannot be written and nothing changes.

### 15. Screens and states

The legacy story has no screen of its own for this journey beyond the queue and the raise form, and neither does this harness: it observes the owners' operations and writes a report. The states are read through those operations, not rendered.

| State | Read through | What the run asserts |
|---|---|---|
| DEV_FLAGGED | rwb-case case read and the timers | The X6 flag is on the case and the stage clock has paused while the prescription clock runs |
| DEV_WITH_OWNER | rwb-case case read, the timers and the decision log | The deviation is with its named owner and the case has not moved on |
| DEV_RESOLVED | rwb-case case read and the timers | X6 is closed and the case is back in the state it paused in, with the stage clock resumed |
| DEV_REROUTE | rwb-case case read and the 30-day timer | The trace is exhausted and the case is on its way to escalation or the route decision |

The harness renders no screen. SCR-08 Deviation queue and SCR-06 Raise deviation belong to the S8 stories of EP07 and are neither built nor read here. What the wave entry check looks at instead is the run report, whose environment, layout and retention are Not specified in the source documents (GAP-0471; ASM-0663).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E7-006-01-ITG | AC1 (legacy); ITG AC1, ITG AC3 | End to end | One case with X6 raised, the trace through the bureau, the internal data and the agency, once verified and once exhausted |
| TC-E7-006-02-ITG | Legacy AC2 is not recorded and stays with RWB-S8-E7006-APP; ITG AC5 | Integration | The decision record forced to fail on the raise |
| TC-E7-006-03-ITG | Access; ITG AC6 | Component | A synthetic caller with no Case record U |
| TC-E7-006-04-ITG | Principle 5; ITG AC5 | Integration | A forced decision-record failure with the case and the timers watched for movement |

The AC column names what the copy derives from and the ITG AC it asserts, and the full legacy test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx under the same legacy test case ID.

### 17. Guardrails

- No business value in code: the synthetic case, its deviation, the business date, the skip-trace answers, the report layout and the gate are data.
- No personal data in logs, events or reports: every key is synthetic, the events carry IDs and facts only, and no contact detail is copied into a report.
- ACE data and partner answers only through the owners' contracts: DP01 and DP13 with their freshness stamp and the partner instruction of rwb-partner, never a direct view read and never another service's schema (DP-01, DP-05).
- One hop and a 2 s budget per call, with a circuit breaker per downstream, so the harness fails where a screen would (DP-11, DP-13).
- No invented operation: the raise and the advance are S8's published operations, and every deviation state is asserted through the case, the timers and the decision log.
- A stub pass is never reported as a real pass: the report names the contract version and whether the hop was a stub or the owner.
- The harness never runs against UAT or production, and it never writes a row by hand or sets a state it then asserts.
- A failing criterion is fixed in the owning service or raised as a gap; it is never waived in the script.

### 18. Traceability

| Item | Source | Where it lands |
|---|---|---|
| Legacy story RWB-E7-006 Run X6 lost contact and skip trace end to end | Recovery Workbench User Stories Epics 3 to 8 v4, lines 11393 to 11474 | Sections 1, 3, 11, 14 and 19 of this file |
| Legacy AC1, verbatim | The same, lines 11412 to 11416 | Section 7, AC1, marked (legacy RWB-E7-006 AC1) |
| Legacy AC2, Not recorded, and its test case TC-E7-006-02 | The same, lines 11418 to 11422 and 11468 | AC5 asserts the same failure here; the legacy AC stays with RWB-S8-E7006-APP (section 19) |
| Legacy test cases TC-E7-006-01 to TC-E7-006-04 | The same, lines 11463 to 11470 | Copied as -ITG in section 16 |
| Legacy endpoints and the Case record U right | The same, lines 11434 to 11452 | Section 12.2 and section 10 |
| Legacy messages MSG-S8-001, MSG-GEN-001, MSG-P4-002, MSG-P7-003 | The same, lines 11454 to 11461 | Section 14 |
| FEAT-DVF-06 Run X6 lost contact and skip trace end to end | Epics 3 to 8 Specification v3, line 129 | Sections 1 and 2 |
| INT-30 NCB, contact tracing for lost contact | Epics 3 to 8 Specification v3, line 239 | Sections 2, 12.8 and 13 |
| REQ-S8-004 and REQ-S8-001 | Business Requirements Program v5, lines 420 and 417 | Section 2 |
| R-DEV-06, R-DEV-16, R-DEV-17, R-UNI-12 | Business Rules and Routing Logic v4, lines 388, 398, 399 and 416 | Sections 8 and 9 |
| DF-CAS-036 to DF-CAS-045, DF-CAS-001 to DF-CAS-023, DF-WRK-009 to DF-WRK-016, DF-WRK-027 to DF-WRK-036, DF-PRT-001 to DF-PRT-007, DF-DEC-001 to DF-DEC-018, DF-REF-001 to DF-REF-015 | Logical Data Model and Data Dictionary v9 | Section 11 |
| DP-03, DP-13 and DP-19 | Template and Rules v1 §R5.5 | Section 13, pattern application |
| ADR-015, ADR-020 and ADR-022 | Architecture Decision Records v4 | Sections 12.4, 12.2 and 8: outbox and inbox on Kafka, contract-first REST with one hop and 2 s, local decision record plus central ledger |
| DeviationWorkflow and the paused stage clock | Architecture v5 slides 15, 25 and 41; Temporal and Drools design slides 13 and 24 | Sections 2, 8, 12.5 and 13 |

### 19. Out of scope

- RWB-S8-E7006-CON and RWB-S8-E7006-APP: the build of the X6 screening, the pause, the routing, the skip trace and the return, and the decision record that goes with them.
- The S8 service build itself: its schema, its endpoints, its workflow, its rule package and its screens, including SCR-06 Raise deviation and SCR-08 Deviation queue.
- The bureau, EFS and agency adapters as products: NCB contact tracing (INT-30) and the partner portal path are the adapters' own stories, and this story only reads their answers through the partner instruction and the case.
- The other six deviation flows X1 to X5 and X7 (FEAT-DVF-01 to FEAT-DVF-05, FEAT-DVF-07) and the override review (FEAT-DVF-08).
- The platform H dependencies named in section 13, and platform deployment and configuration.
- Any production change: this story runs in the test environment only and ships no code to a service.
