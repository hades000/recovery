# RWB-ITG-E7005-ITG Run X5 bankruptcy and seizure end to end

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-E7005-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W4 |
| Wave | 4 |
| Business epic | EP07 |
| Release | 31 May 2027 (tentative) |
| Legacy key | RWB-E7-005 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | L-ITG-W4 |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-ITG-E7005-ITG-16); the squad sizes it at refinement |
| Contract version | Path major /v1 on every consumed operation; exact contract version Not specified in the source documents (DOR-RWB-ITG-E7005-ITG-23); rwb-source-data.yaml 5.1.0 for the rwb-source-data reads (RD-P1-005) |
| Depends on (build) | RWB-S8-E7005-APP |
| Contract dependencies | rwb-integration or the owning service's contract for each outside effect (credit bureau, fraud, external flow, litigation, appraisal, partner portal); interface identities confirmed with P2 before the wave 4 test |
| Integration dependencies | RWB-S8-E7005-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |
| Readiness decisions | RD-P1-005, RD-P1-041 |

**Version 3 changes.**

- Aligned the freshness read to the LOADED and STALE states.
- Readiness decisions: RD-P1-005, RD-P1-041.

**Change log.** D-RCV-60, 27 November 2026: D-RCV-60 P1 developer readiness (RD-P1 register).

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E7-005 as the wave 4 integration proof of the X5 bankruptcy and seizure deviation, from the flag through the assignment to Legal and the bankruptcy filing to the route decision, observed across rwb-deviation, rwb-litigation, rwb-case and rwb-decision; the build of the X5 flow is RWB-S8-E7005-APP. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-ITG-E7005-ITG). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (13 resolved, 9 cross-document, 3 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **Legal counsel**, I want **the X5 bankruptcy and seizure deviation to stop direct collection, pass to Legal with the stage clock paused and the prescription clock still running, and carry the filing with the official receiver or the LED and the bankruptcy to litigation and back to the route decision, proved end to end against the real services**, so that **every deviation has a handler and a clock, and a case that is bankrupt or seized is never worked as if nothing had happened**.

This story builds the harness and the evidence, and nothing else. The deviation flag, the X5 route, the clocks, the bankruptcy step and the re-route are built by S8 in RWB-S8-E7005-APP and its CON story; the case state and the timers are P3's, the legal action is S4's, and the decision record is written through P7's library. The harness raises and drives the deviation through S8's published operations, observes every hop through the owners' published contracts, and writes a run report per case. It builds no production endpoint, no table, no workflow, no activity, no schedule and no screen, and it writes no code in any service.

### 2. Business rationale

A borrower files for bankruptcy, or a creditor seizes an asset, and the case can carry on being chased. That is the failure this story is written against. The X5 flag has to stop direct collection the same day, because a demand letter or a call after the filing is a legal exposure and not just a poor outcome. It has to reach Legal, because the claim has to be filed with the official receiver or the Legal Execution Department before a deadline that the bank does not set. And it has to keep the legal clock running while the working clock stops: the Temporal design puts it plainly on slide 24, "Stage clock paused; prescription never" — a deviation that paused everything would let a prescription lapse while the case sat with a handler, and a deviation that paused nothing would keep breaching the stay.

The second half of the story is the return path. Under R-DEV-15 a bankruptcy filing routes the case to litigation, and a write-off follows only after the receiver reports; under R-DEV-19 the case then reopens the route decision with the segment recomputed and the hard gates re-run, which is where ROUTE_D6 comes from. If the case never comes back to the route decision, a bankrupt borrower stays in a legal stage that nobody revisits, and if a write-off is booked before the receiver reports, the bank writes off a balance that may still be recoverable from an estate. R-UNI-07 states the same trigger from the universal side: a filing or an external seizure raises X5, stops enforcement and starts the claim deadline clock.

The harness is decoupled the way the services are. Every call is one hop on `/api/recovery/<short>/v1` with a 2 s budget (DP-11, DP-13). ACE data is read only through rwb-source-data's data-product contract (DP-05), with its freshness stamp, never from a view and never from another service's schema (DP-01). The decision record is written by S8 through the local decision-record library on `rwb.decision-record.v1` (DP-03) and read back through rwb-decision's contract; where a screen would compose these calls the path is the gateway-bff composite route (DP-19). It carries REQ-S8-001 and the X5 rules R-DEV-05, R-DEV-15 and R-DEV-19 into evidence rather than restating them.

One limit is stated here because it shapes the whole run: the Ownership Map publishes only two rwb-deviation operations, the raise and the patch. There is no `GET /deviations` and no `POST /deviations/{id}/clear` in the map, so the harness never reads a deviation record directly. It asserts the deviation through the case read, the timers read and the decision log, and it proves the clear through the `rwb.deviation.DeviationCleared.v1` publication and the case state that follows it.

### 3. Preconditions

- The published contracts of S8 rwb-deviation (the deviation raise and the patch), P3 rwb-case (the case and its timers), S4 rwb-litigation (the legal action), P7 rwb-decision (the decision log), P1 rwb-source-data (DP01, DP13 and freshness) and P4 rwb-access (the session) are in the contract registry, and a stub set is generated from each one.
- The data product catalog holds DP01 Account and arrears and DP13 Money and closure, each with one system of record, so the account side of the contact stop and the money side of the write-off have one named owner before a value is asserted (FSD P1 v3, A2.2).
- RWB-S8-E7005-APP owns the X5 flow, the two clocks and the bankruptcy step; until it lands, the fixture of §12.8 stands in for its effect and the story is reported as a stub pass.
- FEAT-DVF-05 is the S8 feature and FEAT-DVH-04 is its screening dependency: the fixture holds an X5 code that screening has already produced, so this story never asserts a screening score, a confidence band or a human review threshold (R-DEV-01).
- The X5 route to Legal is R-DEV-05, the bankruptcy route to litigation is R-DEV-15 and the reopen of the route decision is R-DEV-19; the harness asserts those rules and changes none of them.
- The harness environment and base hosts, the fixture layout, the synthetic case, deviation and legal-action keys, the stub answer shapes, the evidence format and retention, and the pass or fail gate: Not specified in the source documents (GAP-0470; ASM-0662).
- The synthetic case, its deviation, its legal action, its timers and the business date are held in the fixture as data, not written in code.
- No build dependency. Day 1, with the stubs in place from the first run; the one wait is RWB-S8-E7005-APP, which replaces its stub and never blocks the lane.

### 4. Flow

1. Harness: loads the fixture: case `RW-2027-001105` in state ANY_STATE with deviation code `X5`, deviation `DEV-SYN-000105`, legal action `LA-SYN-000105`, business date `2027-04-30` and a claim deadline held as a timer. On Day 1 the stubs of §12.8 return the same records.
2. Harness: raises the X5 deviation through `POST /api/recovery/deviation/v1/cases/{caseId}/deviations` with one Idempotency-Key, which starts DeviationWorkflow on the task queue `rwb-deviation`, and asserts the answer carries MSG-S8-001 with the deviation and Legal as the handler.
3. Harness: reads `GET /api/recovery/case/v1/cases/{caseId}` and asserts the case is in DEV_FLAGGED, and reads `GET /api/recovery/case/v1/cases/{caseId}/timers` and asserts the stage clock is paused, the prescription clock is still running and a claim deadline timer is running for the receiver or the LED filing (R-DEV-01, R-DEV-05, Temporal design slide 24).
4. Harness: assigns the deviation to Legal through `PATCH /api/recovery/deviation/v1/deviations/{deviationId}` with one Idempotency-Key, and asserts the case read answers DEV_WITH_OWNER with Legal as the handler (R-DEV-05). The deviation record itself is not read: the map publishes no `GET /deviations`.
5. Harness: reads `GET /api/recovery/source-data/v1/data-products/DP01/records?caseId={caseId}` and asserts the account of the case carries the direct-collection stop that the X5 flag implies, then reads `GET /api/recovery/source-data/v1/data-products/freshness?product=DP01` and asserts the business date and the load time behind that read, so a stale product is never reported as a clean stop.
6. Harness: counts one `rwb.deviation.DeviationRaised.v1` on `rwb.deviation.events.v1`, asserts its consumption through the case read and the case router signal, and replays it once and asserts the case, the timers and the decision log are unchanged, because the inbox holds one processed row per consumer.
7. Harness: reads `GET /api/recovery/decision/v1/decision-log?caseId={caseId}` and asserts one entry for the flag and one for the assignment, each with its rule id and rule version, and that `rwb.decision.DecisionRecorded.v1` was published on `rwb.decision-record.v1` and confirmed by the central ledger in rwb-decision (DP-03).
8. Harness: files the bankruptcy through `PATCH /api/recovery/deviation/v1/deviations/{deviationId}` with the bankruptcy-filed step and one Idempotency-Key, and asserts the case read answers DEV_REROUTE and that R-DEV-15 has routed the case to litigation.
9. Harness: reads `GET /api/recovery/litigation/v1/legal-actions/{legalActionId}` and asserts the legal action for the case, its action type and its status, as the evidence that the litigation route is one legal action and not a second one.
10. Harness: reads `GET /api/recovery/source-data/v1/data-products/DP13/records?caseId={caseId}` and asserts no write-off is read for the case while the receiver report is withheld; then holds the receiver report in the fixture and asserts the case leaves DEV_REROUTE for the route decision, still with no write-off posting from this run (R-DEV-15, R-DEV-19).
11. Harness: reads `GET /api/recovery/case/v1/cases/{caseId}` until it answers ROUTE_D6, and counts one `rwb.deviation.DeviationCleared.v1` on `rwb.deviation.events.v1` with its consumption through the case read; the route operation itself belongs to S1 and is not called here.
12. Harness: counts one `rwb.case.CaseStateChanged.v1` per state change on `rwb.case.events.v1` for the case, and asserts the three states it observed are the three published (AC2, AC3).
13. Harness: calls `GET /api/recovery/access/v1/me/session` as a synthetic RW-OFF caller, then raises a deviation on the case through `POST /api/recovery/deviation/v1/cases/{caseId}/deviations` and asserts 403 with MSG-P4-002 and no state change.
14. Harness: writes one run report per case, keyed by story and case_no, naming the contract version of each hop, whether the hop was a stub or the owner, the deviation and legal-action keys, the three states observed, the timer names and the criteria verdicts.

### 5. Exception paths

| ID | Trigger | What the harness asserts | Message | ITG test case | Covered by |
|---|---|---|---|---|---|
| X1 | A stub answers a shape the published contract does not allow | The run fails at that hop and the report names the service, the operation and the contract version; no criterion is marked passed | None | TC-E7-005-01-ITG (ITG AC1) | AC1 |
| X2 | The flag is raised and the stage clock is not paused, or the prescription clock is paused with it | The run fails on AC2 and the report names the timer, the clock type and the state read; a paused prescription is a failure as serious as an unpaused stage | None | TC-E7-005-02-ITG (ITG AC2) | AC2 |
| X3 | The case reaches DEV_WITH_OWNER but no handler is named in the case read | The run fails on AC2 and the report names the case, the state and the missing handler, because a deviation without an owner is the failure this story is written against | None | TC-E7-005-02-ITG (ITG AC2) | AC2 |
| X4 | The bankruptcy is filed and the case does not reach DEV_REROUTE, or the legal action is not one action | The run fails on AC3 and the report names the state read and the legal action count | None | TC-E7-005-03-ITG (ITG AC3) | AC3 |
| X5 | A write-off is read for the case in DP13 while the receiver report is withheld | The run fails on AC3 and the report names the DP13 row and the freshness stamp; a write-off before the report is a loss, not a timing difference | None | TC-E7-005-03-ITG (ITG AC3) | AC3 |
| X6 | The decision record is written twice, or written without its rule version, or the ledger has not confirmed it | The run fails on AC4 and the report names the entries, their rule versions and the missing confirmation | None | TC-E7-005-04-ITG (ITG AC5) | AC4 |
| X7 | A forced decision-record failure leaves the case changed, or answers without MSG-P7-003 | The run fails on AC5 and the report names the state before and after, the handler and the answer | MSG-P7-003 (expected, and missing) | TC-E7-005-06-ITG (ITG AC5) | AC5 |
| X8 | A caller without the Case record U is allowed to raise a deviation | The run fails on AC6 and the report names the caller role, the operation and the answer; a 201 is a failure even when no data changed | MSG-P4-002 (expected, and missing) | TC-E7-005-05-ITG (ITG AC6) | AC6 |

The report text is for the wave entry check and is not part of the message standard. The harness environment, fixture layout, stub answer shapes, evidence format and retention, and the pass or fail gate are agreed at the wave 4 entry check and recorded in the harness README; fixture values stay data. The business messages the run touches are in section 14 and are asserted by ID and by their substituted values.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Runs against the published contracts and the stubs from Day 1; the only wait is RWB-S8-E7005-APP, and its fixture answers until it lands |
| Negotiable | The fixture layout, the synthetic keys, the timer names, the report shape and the gate are configuration agreed at the wave entry check, not business values in code |
| Valuable | The contact stop is proved to be immediate, the two clocks are proved to pause and to keep running independently, the return path to the route decision is proved, and a write-off before the receiver reports is proved to be absent |
| Estimable | One runner, one stub set, one case fixture, one timer probe, one legal-action probe, one money read-back, one event observer and one report |
| Small | Fits in one sprint with its six tests |
| Testable | Each criterion runs against the stubs and again against RWB-S8-E7005-APP as it lands |

### 7. Acceptance criteria

```gherkin
Feature: Run X5 bankruptcy and seizure end to end - wave 4 integration harness

  Background:
    Given the synthetic case "RW-2027-001105" carries deviation "DEV-SYN-000105" with deviation code "X5" and legal action "LA-SYN-000105"
    Given the deviation screening has produced the X5 code for the case on business date "2027-04-30"
    Given the rule package in force holds R-DEV-05, R-DEV-15 and R-DEV-19 and DP01 and DP13 answer for the case

  Scenario: AC1 Run X5 bankruptcy and seizure end to end (legacy RWB-E7-005 AC1)
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then stops direct collection and files the claim with the receiver or the LED before the deadline
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 The X5 flag goes to Legal with one clock paused and the legal clock running (new, D-RCV-60)
    Given the case "RW-2027-001105" is in state DEV_FLAGGED with deviation code "X5"
    When the deviation is raised through POST /api/recovery/deviation/v1/cases/{caseId}/deviations and assigned through PATCH /api/recovery/deviation/v1/deviations/{deviationId} under R-DEV-05
    Then GET /api/recovery/case/v1/cases/{caseId} answers DEV_WITH_OWNER with Legal named as the handler
    And GET /api/recovery/case/v1/cases/{caseId}/timers shows the stage clock paused and the prescription clock still running
    And a claim deadline timer runs for the filing with the official receiver or the LED

  Scenario: AC3 Bankruptcy filed routes to litigation and back to the route decision (new, D-RCV-60)
    Given the case "RW-2027-001105" is in state DEV_WITH_OWNER with deviation code "X5"
    When bankruptcy is filed under R-DEV-15
    Then GET /api/recovery/litigation/v1/legal-actions/{legalActionId} answers one legal action for the case
    And GET /api/recovery/case/v1/cases/{caseId} answers DEV_REROUTE
    And no write-off is read for the case in DP13 while the receiver report is withheld
    When the receiver report is held in the fixture
    Then the case is read in ROUTE_D6 under R-DEV-19
    And no write-off posting is made by this run

  Scenario: AC4 The decision record is written once and confirmed by the central ledger (new, D-RCV-60)
    Given the case carries deviation "DEV-SYN-000105" and the rule package in force holds R-DEV-05 and R-DEV-15
    When the flag, the assignment and the bankruptcy filing have run
    Then GET /api/recovery/decision/v1/decision-log?caseId={caseId} holds one entry per action with its rule id and rule version
    And "rwb.decision.DecisionRecorded.v1" is published once on "rwb.decision-record.v1" and confirmed by the central ledger in rwb-decision
    And "rwb.deviation.DeviationRaised.v1" is published once on "rwb.deviation.events.v1" and consumed once by rwb-case, rwb-comms and rwb-treatment
    And a replay of either event leaves the case, the timers and the decision log unchanged, because the inbox holds one processed row per consumer

  Scenario: AC5 A forced decision-record failure stops the action (new, D-RCV-60)
    Given the decision record for the case cannot be written
    When the deviation is assigned through PATCH /api/recovery/deviation/v1/deviations/{deviationId}
    Then the answer carries "MSG-P7-003"
    And the case is still read in DEV_FLAGGED with the same handler and the same timers
    And no decision log entry and no "rwb.decision.DecisionRecorded.v1" exist for that action

  Scenario: AC6 A caller without the right is refused (new, D-RCV-60)
    Given a synthetic caller with role "RW-OFF" and no Case record U
    When the caller raises a deviation through POST /api/recovery/deviation/v1/cases/{caseId}/deviations
    Then the answer is 403 with "MSG-P4-002"
    And no deviation is read on the case and no state changes

  Scenario: AC7 Every hop is one REST call on the owner base with a 2 s timeout (new, D-RCV-60)
    Given the synthetic case "RW-2027-001105" is in the run
    When each hop of the run is called
    Then each hop is one REST call on the owner base "/api/recovery/<short>/v1"
    And no hop answers later than 2 s

  Scenario: AC8 ACE data is read only through the rwb-source-data data-product contract (new, D-RCV-60)
    Given the run needs ACE data for the case "RW-2027-001105"
    When the ACE data is read
    Then it is read through the rwb-source-data data-product contract with its freshness stamp
    And no view and no other service schema is read

  Scenario: AC9 A deviation past its service level escalates to the team manager and the breach is reported (new, D-RCV-60)
    Given deviation "DEV-SYN-000105" sits with its owner past the deviation service level
    When the escalation runs under R-DEV-20
    Then the deviation escalates to the team manager
    And the breach is reported

  Scenario: AC10 Only deviation code X5 is raised in the run (new, D-RCV-60)
    Given the synthetic case RW-2027-001105 is in the run
    When the run raises deviations for the case
    Then the only deviation code raised is X5

  Scenario: AC11 A consumed call that fails or does not answer fails the run (new, D-RCV-60)
    Given one consumed call of the run is stubbed to fail or to answer after 2 s
    When the run reaches that call
    Then the run fails on that hop and the run report names the hop and the answer
    And no later state is read as passed
```

Legacy AC2 (the R-DEV-05 assignment and the DEV_WITH_OWNER move) is asserted here in AC2 together with the two clocks, legacy AC3 (R-DEV-15 and DEV_REROUTE) in AC3, and legacy AC4 (the decision log cannot be written) in AC5; the build of those steps stays with RWB-S8-E7005-APP.

### 8. Business rules

| ID | Rule | Source | Covered by |
|---|---|---|---|
| BR1 | A deviation in any state pauses the stage clock and keeps the prescription clock running, and routes the case to the named owner | R-DEV-01; Temporal and Drools design slide 24 | AC2 |
| BR2 | An X5 bankruptcy or seizure is assigned to Legal, and the claim is filed with the official receiver or the LED before the deadline | R-DEV-05 | AC1, AC2 |
| BR3 | When bankruptcy is filed on X5 the case routes to litigation, and to write-off only after the receiver reports | R-DEV-15 | AC3 |
| BR4 | Every X1 to X7 deviation runs end to end with its own flow, approver, contact rules and return point | REQ-S8-001 | AC10 (X5 only) |
| BR5 | A filing or an external seizure raises X5, stops enforcement and starts the claim deadline clock | R-UNI-07 | AC2 |
| BR6 | After the reroute the case reopens the route decision with the segment recomputed and the hard gates re-run, ending in ROUTE_D6 | R-DEV-19 | AC3 |
| BR7 | A deviation that sits with its owner past the deviation service level escalates to the team manager and the breach is reported | R-DEV-20 | AC9 |
| BR8 | Every hop in the run is one REST call on the owner's base `/api/recovery/<short>/v1` with a 2 s timeout | DP-11, DP-13 | AC7 |
| BR9 | ACE data is read only through rwb-source-data's data-product contract with its freshness stamp, never from a view and never from another service's schema | DP-01, DP-05 | AC8 |
| BR10 | The decision record is written by the owning service through the local decision-record library on `rwb.decision-record.v1`, and the central ledger in rwb-decision confirms it | DP-03; ADR-022 | AC4 |

The harness asserts these rules and changes none of them; the rules themselves are evaluated in RWB-S8-E7005-APP and the states are held by P3 rwb-case. Reference data is read through the reference-data contract under DP-06 and DP-07, and no parameter value is hard-coded; the rule package in force is the parameter set the run reads. The claim deadline, the service level and the Legal route of R-DEV-05 are versioned reference rows held as placeholders until a source gives their values. Both X5 slices trace to FEAT-DVF-05 until the Epic 3 to 8 PRD adds identifiers. Case record U is declared on both operations and the widening of RW-LEGAL is left to rwb-access. The two catalogue events are published through the platform outbox, and step D1 decides whether RWB-PLT-TE006-CON and a rwb-case contract story become dependencies of this key.

### 9. State transitions

| From | Event | Condition | To | Owner of the change |
|---|---|---|---|---|
| ANY_STATE | DEVIATION_FLAGGED | deviation_code in (X1..X7) | DEV_FLAGGED | S8 rwb-deviation, DeviationWorkflow, R-DEV-01; `rwb.deviation.DeviationRaised.v1` |
| DEV_FLAGGED | OWNER_ASSIGNED | deviation_code = X5 | DEV_WITH_OWNER | S8 rwb-deviation, R-DEV-05, assigning Legal |
| DEV_WITH_OWNER | BANKRUPTCY_FILED | deviation_code = X5 | DEV_REROUTE | S8 rwb-deviation, R-DEV-15, routing to S4 rwb-litigation |
| DEV_REROUTE | ROUTE_REOPENED | any | ROUTE_D6 | P3 rwb-case for the case state and S1 rwb-valuation for the D6 route decision, R-DEV-19 |

The states are the deviation states of R-DEV-01, R-DEV-05, R-DEV-15 and R-DEV-19, and the case state is read through the P3 contract after every step. The two clocks are read through `GET /api/recovery/case/v1/cases/{caseId}/timers`: the stage clock is paused from DEV_FLAGGED, the prescription clock is never paused, and the claim deadline timer of R-DEV-05 runs from DEV_WITH_OWNER. The harness changes no state. Every change in the table is made by the owner: S8 holds the deviation and drives DeviationWorkflow, P3 holds the case state and the timers, S4 holds the legal action, P7 holds the central ledger. A state the harness had set by hand would prove nothing, so the report names the owner and the operation behind every value it asserts.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-LITOFF, litigation officer | Is the Legal handler of X5 under R-DEV-05; holds Case record U; is the role the journey is written for |
| RW-CASEOWN, case owner | Owns the case after the reroute and holds Case record U; the team manager is the escalation point of R-DEV-20 |
| RW-ENFORCE, RW-SALEOFF | Read the same evidence where their rights allow; their enforcement work is what X5 stops |
| RW-OFF, RW-TRIBE, RW-PLATADM | Read only where their rights allow; RW-OFF is the refused caller of AC6 |
| QA lead | Owns the harness configuration, the fixtures, the report shape and the pass or fail gate |
| Integration lead | Owns the harness code, the stub set and the swap from a stub to the real service |
| The owning services' identities | S8 runs DeviationWorkflow and writes the decision record, P3 holds the case and the timers, S4 holds the legal action, P7 holds the ledger, P1 answers the data products and P4 answers the session; they make every change the harness asserts |
| No delegation of authority level applies | The harness takes no business decision; authorisation is answered by rwb-access and the DoA is P4's |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-036 to DF-CAS-045 | deviation | deviation_code, raised_at, raised_by, paused_state, handler | Written through the rwb-deviation raise and patch, read back through the case and the timers |
| DF-CAS-001 to DF-CAS-023 | recovery_case | case_no, status, stage_code, primary_person_key | Read through the rwb-case contract |
| DF-WRK-009 to DF-WRK-016 | assignment | assignee_user_id, assigned_at, ended_at | Read through the rwb-case contract |
| DF-WRK-027 to DF-WRK-036 | timer | timer_type, started_at, expires_at, paused_at | Read through the rwb-case timers contract |
| DF-LEG-001 to DF-LEG-014 | legal_action | action_type, lawsuit_no, black_case_no, status | Read through the rwb-litigation contract |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | decision_code, rule_id, rule_version | Read through the rwb-decision contract |
| DF-REF-001 to DF-REF-015 | rule_row | rule_id, rule_version, from_state, event_code | Read through the rwb-decision contract |

Field IDs are those in the Logical Data Model and Data Dictionary v9. The deviation and the assignment belong to S8 and P3's case contract, the case and the timers are P3's, the legal action is S4's, the decision log and the rule rows are P7's, and the account and the money side are DP01 and DP13 of P1's contract; the harness reads them only through those contracts and never from a schema. The harness owns no table and writes no row. The two writes it makes are the owner's published operations of §12.2, taken with one Idempotency-Key each.

### 12. Contract

#### 12.1 REST operations provided

None. The harness is a test runner and provides no REST operation.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| POST | `/api/recovery/deviation/v1/cases/{caseId}/deviations` | S8 rwb-deviation | Raises the X5 deviation and starts DeviationWorkflow, with one Idempotency-Key (AC1, AC2, AC4, AC6) |
| PATCH | `/api/recovery/deviation/v1/deviations/{deviationId}` | S8 rwb-deviation | The assignment to Legal and the bankruptcy-filed step, with one Idempotency-Key (AC2, AC3, AC5) |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The case state after the flag, the assignment, the filing and the reroute, and the handler (AC1 to AC6) |
| GET | `/api/recovery/case/v1/cases/{caseId}/timers` | P3 rwb-case | The stage clock, the prescription clock and the claim deadline timer (AC2, AC4, AC5) |
| GET | `/api/recovery/litigation/v1/legal-actions/{legalActionId}` | S4 rwb-litigation | The one legal action of the bankruptcy route, its action type and its status (AC3) |
| GET | `/api/recovery/decision/v1/decision-log?caseId={caseId}` | P7 rwb-decision | The decision record of the flag, the assignment and the filing, with the rule version and the ledger confirmation (AC1, AC4, AC5) |
| GET | `/api/recovery/source-data/v1/data-products/DP01/records?caseId={caseId}` | P1 rwb-source-data | The account of the case and the contact stop behind it (AC1, AC2) |
| GET | `/api/recovery/source-data/v1/data-products/DP13/records?caseId={caseId}` | P1 rwb-source-data | The money and closure rows of the case, to prove no write-off before the receiver reports (AC3) |
| GET | `/api/recovery/source-data/v1/data-products/freshness?product=DP01` | P1 rwb-source-data | The business date and the load time behind the ACE read (AC1). The answer's `status` is LOADED or STALE, and a never-stamped product answers STALE with `businessDate` null (RD-P1-005, RD-P1-041) |
| GET | `/api/recovery/access/v1/me/session` | P4 rwb-access | The caller's roles and rights before a write (AC6) |

Every call is one hop on the owner's base `/api/recovery/<short>/v1` with a 2 s budget (DP-11, DP-13). No operation is invented in this story: each path is the owner's published operation in the Ownership Map, and where a screen would compose them the path would be the gateway-bff composite route (DP-19).

The map publishes no `GET /deviations` and no `POST /deviations/{id}/clear` for S8, and this story does not pretend otherwise. The deviation is therefore asserted through three published reads — the case read for the state and the handler, the timers read for the two clocks and the claim deadline, and the decision log for the record — plus the `rwb.deviation.DeviationRaised.v1` and `rwb.deviation.DeviationCleared.v1` publications. The two writes above are the only deviation operations the run uses, and both are the map's own.

#### 12.3 Events published

None. The harness publishes no Kafka event; it writes its report to the wave record.

#### 12.4 Events consumed

| Event | Topic | Producer | Use in the run |
|---|---|---|---|
| `rwb.deviation.DeviationRaised.v1` | `rwb.deviation.events.v1` | S8 rwb-deviation | Counts one publication after the X5 flag and, with the replay, proves one processed row per consumer (AC4) |
| `rwb.deviation.DeviationCleared.v1` | `rwb.deviation.events.v1` | S8 rwb-deviation | Counts one publication when the deviation clears and the case leaves DEV_REROUTE (AC3) |
| `rwb.case.CaseStateChanged.v1` | `rwb.case.events.v1` | P3 rwb-case | Proves the three observed states are the three published for the case (AC2, AC3) |
| `rwb.decision.DecisionRecorded.v1` | `rwb.decision-record.v1` | S8 rwb-deviation through the local decision-record library (DP-03) | Proves the record was published once with its rule version and confirmed by the central ledger (AC4, AC5) |

The harness subscribes to the three topics under one consumer group of its own, counts publications and replays each event once. The consumer effect it reads is the case through the rwb-case operation of §12.2; the inbox row counts of rwb-comms and rwb-treatment come from the consumer evidence in the run fixture, because neither consumer exposes an operation in this story. `rwb.deviation.DeviationCleared.v1` is asserted by count and by the case state that follows it, since the map publishes no clear operation to drive.

#### 12.5 Workflows and activities

None added. The harness exercises DeviationWorkflow, S8's child workflow on the task queue `rwb-deviation` in the `rwb-recovery` namespace, started through the deviation raise and continued through the patch: it is the workflow that carries the X5 route, the pause of the stage clock, the claim deadline timer and the bankruptcy step. It observes CaseWorkflow on `rwb-case`, the parent that receives the deviation through the case router as a signal and pauses and resumes the stage clock for the case. Both are stated here as observed and not built here; no workflow, activity or Schedule is created, changed or owned by this story, and LitigationWorkflow on `rwb-litigation` is only seen through the legal-action read of §12.2.

#### 12.6 Schedules

None added. The X5 flag arrives as an event and the confusion it stops arrives as a filing, so nothing in the journey is on a cron: the harness starts the run with the raise operation and holds the receiver report in its own fixture instead of waiting on a schedule. The timer check of JOB-05 is retired in favour of durable timers inside the workflows (Arch v5 slide 44), which is why the two clocks are read through the timers operation and not through a job.

#### 12.7 Tables owned

None. The harness owns no schema and no table (DP-01); deviation is S8's, recovery_case, assignment and timer are P3's, legal_action is S4's, decision_log_entry and rule_row are P7's, and the account and the money side belong to the products behind P1's contract.

#### 12.8 Contract fakes

| Fake | Contract | Stubbed answer in the run |
|---|---|---|
| Stub for rwb-deviation | `POST /cases/{caseId}/deviations`, `PATCH /deviations/{deviationId}` | Accepts the raise once per Idempotency-Key and answers MSG-S8-001 with deviation `DEV-SYN-000105` and Legal as the handler; the patch accepts the assignment and the bankruptcy step and keeps the same deviationId |
| Stub for rwb-case | `GET /cases/{caseId}`, `GET /cases/{caseId}/timers` | Case `RW-2027-001105` in DEV_FLAGGED, then DEV_WITH_OWNER with Legal, then DEV_REROUTE, then ROUTE_D6; the stage clock paused, the prescription clock running and one claim deadline timer |
| Stub for rwb-litigation | `GET /legal-actions/{legalActionId}` | One legal action `LA-SYN-000105` for the case, its action type and its status after the bankruptcy route |
| Stub for rwb-decision | `GET /decision-log?caseId={caseId}` | One entry per action with its rule id and rule version, and the central ledger confirmation |
| Stub for rwb-source-data | DP01 records, DP13 records, freshness | The account of the case with the contact stop, no write-off row for the case, and business date `2027-04-30` with a load time |
| Stub for rwb-access | `GET /me/session` | Allows RW-LITOFF with Case record U; refuses RW-OFF with 403 and MSG-P4-002 |
| Receiver and LED filing fixture | The claim deadline and the receiver report | A claim deadline timer with its expiry, and a receiver report withheld until the fixture holds it, at the point where the real filing would answer |

Each stub is generated from the published contract and its version is pinned in the run report, so a contract change shows up as a run failure and not as a silent pass. The harness environment and base hosts, the fixture layout, the synthetic case, deviation and legal-action keys, the stub answer shapes, the evidence format and retention, and the pass or fail gate are Not specified in the source documents (GAP-0470; ASM-0662).

#### 12.9 Call-type summary

| Call type | In this story |
|---|---|
| REST | 0 provided, 10 consumed, one hop each on `/api/recovery/<short>/v1` with a 2 s budget (DP-11, DP-13) |
| Kafka | None published; four consumed, `rwb.deviation.DeviationRaised.v1`, `rwb.deviation.DeviationCleared.v1`, `rwb.case.CaseStateChanged.v1` and `rwb.decision.DecisionRecorded.v1`, counted and replayed once |
| Temporal | None added; DeviationWorkflow on `rwb-deviation` exercised from the raise, with CaseWorkflow on `rwb-case` observed as the parent that pauses and resumes the stage clock |
| File | None. The receiver report is held in the run fixture; no file or claim-check is transferred by this story |

### 13. Solution plan

**Package.** Folder `itg/recovery`, package `th.co.scb.ace.workbench.recovery.itg`, test scope only; not part of any deployed service.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The H dependencies DP-03 and DP-19 add, RWB-PLT-E1027-CON and RWB-PLT-N001-CON, are platform stories delivered by the platform wave and are not repeated in the metadata H field of this story, which stays None; DP-13 adds nothing. The one blocking dependency is the I story RWB-S8-E7005-APP, which replaces its stub; until it is live the run uses the stub, and a stub pass is reported as a stub pass.

**Harness components**

| Component | Type | Responsibility |
|---|---|---|
| JourneyRunner | Job | Runs the six owned criteria in order for a case and holds the run lock |
| DeviationDriver | Service | Raises the X5 deviation and patches the assignment and the bankruptcy step, once per Idempotency-Key |
| ClockProbe | Service | Reads the timers and asserts the stage clock paused, the prescription clock running and the claim deadline timer present |
| LitigationProbe | Service | Reads the legal action and asserts one action for the case, with its type and status |
| MoneyReadBack | Service | Reads DP13 with the freshness stamp and names any write-off row seen before the receiver report |
| DecisionProbe | Service | Reads the decision log and asserts one record per action, with its rule version and the ledger confirmation |
| EventObserver | Service | Subscribes to `rwb.deviation.events.v1`, `rwb.case.events.v1` and `rwb.decision-record.v1`, counts publications and replays each event once |
| StubSet | Fake | The six stubs and the receiver fixture of §12.8, generated from the published contracts with the version pinned |
| EvidenceReport | Service | Writes one report per case keyed by story and case_no, and holds the pass or fail gate |

**Environment and test data.** SIT, against the stubs from Day 1 and the real services as RWB-S8-E7005-APP lands, on synthetic case `RW-2027-001105`, deviation `DEV-SYN-000105`, legal action `LA-SYN-000105` and business date `2027-04-30`. The harness seeds nothing by hand and never writes a schema row. The environment and base hosts, the fixture layout, the synthetic keys, the stub answer shapes, the evidence format and retention, and the pass or fail gate are Not specified in the source documents (GAP-0470; ASM-0662).

**Build steps**

1. Generate the six stubs and the receiver fixture from the published contracts and pin each contract version in the run report; fail the run on a mismatch (X1).
2. Build the DeviationDriver for the raise and prove it is accepted once per Idempotency-Key and answers MSG-S8-001 with the deviation and the handler (AC1).
3. Add AC2 on the case read and the timers read: DEV_WITH_OWNER with Legal, the stage clock paused and the prescription clock still running, and the claim deadline timer present (X2, X3).
4. Add AC3 on the bankruptcy patch and the legal-action read, asserting DEV_REROUTE and one legal action for the case (X4).
5. Add the MoneyReadBack for AC3: no write-off row in DP13 while the receiver report is withheld, then the receiver report held and the case read in ROUTE_D6 under R-DEV-19 (X5).
6. Add the EventObserver for AC4: one DeviationRaised publication with its consumption, one CaseStateChanged per state, and a replay that changes nothing because the inbox holds one row per consumer.
7. Add the DecisionProbe for AC4 and AC5: one entry per action with its rule version, the ledger confirmation, then a forced write failure that leaves the case and the timers untouched and answers MSG-P7-003 (X6, X7).
8. Add the access path for AC6 through the session read and the raise operation, and assert 403 with MSG-P4-002 and no state change (X8).
9. Add the EvidenceReport and the gate, and swap a stub for the real owner as RWB-S8-E7005-APP lands.

**Feature switch.** None. The harness has no production flag and runs in the test environment only.

**Done when.** The tests of section 16 pass against the fakes and again against RWB-S8-E7005-APP when it lands, and the wave entry check holds a run report keyed by story and case_no.

### 14. Validation and messages

| ID | Type | Message |
|---|---|---|
| MSG-S8-001 | Information | {deviation} was raised. The case is with {handler}. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The harness asserts the message ID and the substituted values on the answer it reads, and owns no message text. MSG-S8-001 is asserted with the deviation code and Legal as the handler when the X5 flag is raised, MSG-GEN-001 with the missing field when a write is made short of a required parameter, MSG-P4-002 with the refused raise for a caller without Case record U, and MSG-P7-003 when the decision record cannot be written and nothing changes.

### 15. Screens and states

The legacy story's screens are SCR-08 Deviation queue and SCR-06 Raise deviation, and neither is built or rendered here: the harness calls the two operations behind them and reads the states through the owners. What the wave entry check looks at instead is the run report, whose environment, layout and retention are Not specified in the source documents (GAP-0470; ASM-0662).

| State | Read through | What the run asserts |
|---|---|---|
| DEV_FLAGGED | rwb-case case read and timers read | The X5 flag is raised, the case is flagged and the stage clock is paused while the prescription clock runs |
| DEV_WITH_OWNER | rwb-case case read and timers read | Legal is the handler, the claim deadline timer runs, and the decision record exists with its rule version |
| DEV_REROUTE | rwb-case case read and rwb-litigation legal-action read | The bankruptcy is filed, one legal action exists for the case, and no write-off is read in DP13 |
| ROUTE_D6 | rwb-case case read | The case reopens the route decision under R-DEV-19 and the deviation clears |
| A refused raise | rwb-access session read and the raise answer | 403 with MSG-P4-002 and no state change |

The screen states of SCR-06 and SCR-08 are recorded below for the owners that render them; this run builds and asserts none of them. Screen Specifications v1 gives SCR-06 as form and saved and SCR-08 as loading and list. The empty, loading and error behaviour follows the front-end design system rules, and the no access message is the one Screen Specifications v1 lists for both screens.

| Screen | Empty | Loading | Error | No access |
|---|---|---|---|---|
| SCR-06 Raise deviation | Explains what the screen is for (raise X1 to X7 on a case with the reason and the evidence) and what to do next; no blank page | Skeleton or progress indicator; no layout shift | Safe message with its message ID, retry where safe, and a support reference | MSG-P4-002 and nothing changes |
| SCR-08 Deviation queue | Explains what the screen is for (open deviations by type, handler and age) and what to do next; no blank page | Skeleton or progress indicator; no layout shift | Safe message with its message ID, retry where safe, and a support reference | MSG-P4-002 and nothing changes |

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E7-005-01-ITG | AC1 (legacy); ITG AC1 | End to end | One case with an X5 flag, the raise, the assignment and the filing live |
| TC-E7-005-02-ITG | AC2 (legacy, rule R-DEV-05); ITG AC2 | Integration | A case in DEV_FLAGGED with deviation code X5 |
| TC-E7-005-03-ITG | AC3 (legacy, rule R-DEV-15); ITG AC3 | Integration | A case in DEV_WITH_OWNER with the bankruptcy filed and the receiver report withheld |
| TC-E7-005-04-ITG | ITG AC5 (legacy AC4 is RWB-S8-E7005-APP's) | Integration | A forced decision-record failure on the assignment |
| TC-E7-005-05-ITG | Access; ITG AC6 | Component | RW-OFF caller without Case record U |
| TC-E7-005-06-ITG | Principle 5; ITG AC5 | Integration | A forced decision-record failure at the point of the state change |
| TC-E7-005-07-ITG | AC7; BR8 | Component | Each hop of the run on its owner base with the 2 s timeout |
| TC-E7-005-08-ITG | AC8; BR9 | Integration | ACE data read through the rwb-source-data contract with its freshness stamp |
| TC-E7-005-09-ITG | AC9; BR7 | Integration | A deviation past its service level with its owner |
| TC-E7-005-10-ITG | AC10; BR4 | Component | A run that raises deviation code X5 only |
| TC-E7-005-11-ITG | AC11 | Integration | One consumed hop stubbed to fail or to answer after 2 s |

The AC column names the legacy AC the copy derives from and the ITG AC it asserts, and the full legacy test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx under the same legacy test case ID. Legacy AC2, AC3 and AC4 stay with RWB-S8-E7005-APP as build criteria; the -ITG copies here assert the same behaviour across the service boundary.

### 17. Guardrails

- No business value in code: the synthetic case, deviation and legal-action keys, the business date, the timer names, the claim deadline and the report layout are data.
- No personal data in logs, events or reports: every key is synthetic, and the events carry IDs and facts only.
- ACE data only through the P1 contract: DP01 and DP13 with their freshness stamp, never a direct view read and never another service's schema (DP-01, DP-05).
- One hop and a 2 s budget per call, with a circuit breaker per downstream, so the harness fails where a screen would (DP-11, DP-13).
- No invented operation: only the two deviation writes and the eight reads of §12.2, and the deviation is never asserted through a read the map does not publish.
- A stub pass is never reported as a real pass: the report names the contract version and whether the hop was a stub or the owner.
- The harness never runs against UAT or production, and it never writes a row by hand or sets a state it then asserts.
- A failing criterion is fixed in the owning service or raised as a gap; it is never waived in the script.

### 18. Traceability

| Item | Source | Where it lands |
|---|---|---|
| Legacy story RWB-E7-005 Run X5 bankruptcy and seizure end to end | Recovery Workbench User Stories Epics 3 to 8 v4, lines 11295 to 11391 | Sections 1, 3, 11, 14 and 19 of this file |
| Legacy AC1, verbatim | The same, lines 11314 to 11318 | Section 7, AC1, marked (legacy RWB-E7-005 AC1) |
| Legacy AC2, AC3 and AC4, rules R-DEV-05 and R-DEV-15 and the not-recorded case | The same, lines 11320 to 11335 | AC2, AC3 and AC5 here; the legacy criteria stay with RWB-S8-E7005-APP (section 19) |
| Legacy test cases TC-E7-005-01 to TC-E7-005-06 | The same, lines 11382 to 11387 | Copied as -ITG in section 16 |
| Legacy endpoints, screens, permission check and messages | The same, lines 11349 to 11376 | Sections 12.2, 15 and 14 |
| FEAT-DVF-05 Run X5 bankruptcy and seizure end to end | Epics 3 to 8 Specification v3, line 128 | Sections 1 and 2 |
| REQ-S8-001, with REQ-S8-004 and REQ-S8-005 as the X6 and X7 siblings | Business Requirements Program v5, lines 417, 420 and 421 | Section 8, BR4; the X6 and X7 harness stories are RWB-ITG-E7006-ITG and RWB-ITG-E7007-ITG |
| R-DEV-01, R-DEV-05, R-DEV-15, R-DEV-19 and R-DEV-20 | Business Rules and Routing Logic v4, lines 383, 387, 397, 401 and 402 | Sections 8 and 9 |
| R-UNI-07 | The same, line 411 | Section 8, BR5 |
| INT-30 contact tracing and INT-33 the Legal Execution Department and courts | Epics 3 to 8 Specification v3, lines 239 and 241 | Sections 2, 11 and 12.8 |
| DF-CAS-036 to DF-CAS-045, DF-CAS-001 to DF-CAS-023, DF-WRK-009 to DF-WRK-016, DF-WRK-027 to DF-WRK-036, DF-LEG-001 to DF-LEG-014, DF-DEC-001 to DF-DEC-018, DF-REF-001 to DF-REF-015 | Logical Data Model and Data Dictionary v9 | Section 11 |
| DP-03, DP-13 and DP-19 | Template and Rules v1 §R5.5 | Section 13, pattern application |
| ADR-015, ADR-020 and ADR-022 | Architecture Decision Records v4 | Sections 12.4, 12.2 and 8: outbox and inbox on Kafka, contract-first REST with one hop and 2 s, local decision record plus central ledger |
| DeviationWorkflow, the pause of the stage clock and the parent CaseWorkflow | Architecture v5 slides 15, 17, 25 and 41; Temporal and Drools design slides 13 and 24 | Sections 2, 8, 12.5 and 13 |
| Points of no return and strict mode | Temporal and Drools design slide 26 | Sections 2 and 8: the write-off is a later posting and is never booked by this run |

### 19. Out of scope

- RWB-S8-E7005-CON and RWB-S8-E7005-APP: the build of the X5 route, the two clocks, the bankruptcy step, the re-route and the decision record.
- The S8 deviation screening and the other six deviation codes (RWB-S8-E7006-*, RWB-S8-E7007-*), and the screening dependency FEAT-DVH-04.
- The LIT adapter and the litigation build: `LitigationWorkflow`, the hearings, the judgment and the enforcement ladder are S4's own stories, and this story only reads one legal action through the contract.
- The write-off build (RWB-S7-*): DP13 is read to prove a write-off is absent before the receiver reports, and no write-off is created or posted here.
- The route decision of S1 and its approval on P7: ROUTE_D6 is read through the case, and the route operation is not called by this story.
- The platform stories and their H dependencies named in section 13, including RWB-PLT-E1027-CON and RWB-PLT-N001-CON.
- SCR-08 Deviation queue and SCR-06 Raise deviation, and every gateway-bff composite route.
- Any production change: no endpoint, table, workflow, activity, schedule, screen, feature flag or configuration in any service.
