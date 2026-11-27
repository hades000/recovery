# RWB-ITG-E7004-ITG Run X4 fraud end to end

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-E7004-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W4 |
| Wave | 4 |
| Business epic | EP07 |
| Release | 31 May 2027 (tentative) |
| Legacy key | RWB-E7-004 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | L-ITG-W4 |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-ITG-E7004-ITG-16); the squad sizes it at refinement |
| Depends on (build) | RWB-S8-E7004-APP |
| Contract dependencies | Not specified in the source documents (DOR-RWB-ITG-E7004-ITG-21) |
| Contract version | v1 (the /v1 base of every operation in section 12.2); rwb-source-data.yaml 5.1.0 for the rwb-source-data reads (RD-P1-005) |
| Integration dependencies | RWB-S8-E7004-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |
| Readiness decisions | RD-P1-005, RD-P1-041 |

**Version 3 changes.**

- Aligned the freshness read to the LOADED and STALE states.
- Readiness decisions: RD-P1-005, RD-P1-041.

**Change log.** D-RCV-60, 27 November 2026: D-RCV-60 P1 developer readiness (RD-P1 register).

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E7-004 as the wave 4 integration proof of the X4 fraud deviation, from the flag through the referral to the fraud team and the named handler to the confirmed or cleared outcome and the reopened route decision, observed across rwb-deviation, rwb-case, rwb-source-data and rwb-decision; the build of the X4 flow is RWB-S8-E7004-APP. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-ITG-E7004-ITG). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (19 resolved, 9 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **fraud investigator**, I want **the X4 fraud deviation to hold the case the same day, refer it once to the fraud team with the stage clock paused and the prescription clock still running, and route it on the confirmed or cleared outcome to the write-off route or back to the collections decision and the route decision, proved end to end against the real services**, so that **every deviation has a handler and a clock, and a case with a fraud flag is never worked as if nothing had happened**.

This story builds the harness and the evidence, and nothing else. The fraud flag, the X4 route, the referral, the confirmed and cleared outcomes and the re-route are built by S8 in RWB-S8-E7004-APP and its CON story; the case state and the timers are P3's, the write-off route is S7's and the route decision is S1's, and the decision record is written through P7's library. The harness raises and drives the deviation through S8's published operations, observes every hop through the owners' published contracts, and writes a run report per case and branch. It builds no production endpoint, no table, no workflow, no activity, no schedule and no screen, and it writes no code in any service.

### 2. Business rationale

A case is flagged for fraud and carries on being worked as an ordinary collection case. That is the failure this story is written against, and both published rules name it. R-UNI-08 fires when Aric or an officer flags fraud: it raises X4, holds the case and refers it to the fraud team, the same day. R-DEV-04 then assigns X4 to the fraud team and refers the case to Aric. A demand letter, a settlement offer or a write-off decision taken after a fraud signal is not a poor outcome, it is a loss the bank creates itself, and it can compromise an investigation that other parties are running. The same two rules put a named handler on the case, because a fraud flag that nobody owns is the deviation failure the whole of S8 exists to remove.

The second half of the story is the return path, and it has two legitimate ends. Under R-DEV-13 confirmed fraud routes the case to write-off, with recovery continuing under the fraud case; under R-DEV-14 fraud that is not confirmed returns the case to the collections decision. In both cases R-DEV-19 reopens the route decision with the segment recomputed and the hard gates re-run, which is where ROUTE_D6 comes from. A harness that proved only the write-off end would never see the case that has to go back to collections with its name cleared, and a harness that proved only the return would never see that a confirmed fraud case is not left in a treatment stage. R-LIT-77 states the litigation side of the same event: fraud confirmed in Aric stops the litigation and routes the case to write-off at D9. The litigation build is out of scope here and this story reads no legal action, but the rule is cited because it is the same confirmation driving the same route.

Aric itself is stated here plainly, because the honest boundary matters more than a tidy diagram. INT-31 Aric (Epics 3 to 8 Specification v3, line 240) is the fraud referral, outbound, and its delivery note is "Not available today; by the fraud investigator". No Aric operation exists in the Ownership Map, the referral feature is FEAT-ADM-13 in the administration module and not this story, and the WP sets External dependencies to None. Aric is therefore a contract fake and a run fixture in §12.8, it is not an X dependency, and this story invents no Aric API, no endpoint, no topic and no status vocabulary of its own. The harness asserts that the case produces exactly one referral with one reference, that the reference is carried through both outcomes, and that a repeat of the raise produces no second referral. The referral answer shape and its status words are configuration held in the fixture and are recorded as a gap, not guessed into a contract.

The harness is decoupled the way the services are. Every call is one hop on `/api/recovery/<short>/v1` with a 2 s budget (DP-11, DP-13). The money and closure side of the case is read only through rwb-source-data's DP13 data-product contract with its freshness stamp, never from a view and never from another service's schema (DP-05, DP-01), which is how the run proves that no write-off was posted. The decision record is written by S8 through the local decision-record library on `rwb.decision-record.v1` (DP-03) and read back through rwb-decision's contract; where a screen would compose these calls the path is the gateway-bff composite route (DP-19). The story carries REQ-S8-001 and the X4 rules into evidence rather than restating them.

One limit is stated here because it shapes the run. The Ownership Map publishes only two rwb-deviation operations, the raise and the patch. There is no `GET /deviations` and no clear operation, so the harness never reads a deviation record directly: it asserts the deviation through the case read, the timers read and the decision log, and it proves the clear through the `rwb.deviation.DeviationCleared.v1` publication and the case state that follows it.

### 3. Preconditions

- The published contracts of S8 rwb-deviation (the deviation raise and the patch), P3 rwb-case (the case and its timers), P1 rwb-source-data (DP13 records and the freshness read), P7 rwb-decision (the decision log) and P4 rwb-access (the session) are in the contract registry, and a stub set is generated from each one.
- The data product catalog holds DP13 Money and closure with one system of record, so the write-off and closure side of the case has one named owner before the absence of a posting is asserted (FSD P1 v3, A2.2).
- RWB-S8-E7004-APP owns the X4 flow, the referral and both outcomes; until it lands, the fixture of §12.8 stands in for its effect and the story is reported as a stub pass.
- FEAT-DVF-04 is the S8 feature and FEAT-DVH-04 is its screening dependency: the fixture holds an X4 code that screening has already produced, so this story never asserts a screening score, a confidence band or a human review threshold (R-DEV-01).
- The X4 assignment is R-DEV-04, the confirmed outcome is R-DEV-13, the cleared outcome is R-DEV-14 and the reopen of the route decision is R-DEV-19; the harness asserts those rules and changes none of them.
- The Aric referral is a fixture of §12.8 and not an X dependency: INT-31 is not available today, no Aric operation is published, and FEAT-ADM-13 is outside this story.
- The harness environment and base hosts, the fixture layout, the synthetic case, deviation and referral keys, the Aric referral answer shape and status vocabulary, the investigation tracking evidence, the evidence format and retention, and the pass or fail gate: Not specified in the source documents (GAP-0469; ASM-0661).
- The synthetic case, its deviation, its referral and investigation references, its two branch outcomes and the business date are held in the fixture as data, not written in code.
- No build dependency. Day 1, with the stubs in place from the first run; the one wait is RWB-S8-E7004-APP, which replaces its stub and never blocks the lane.

### 4. Flow

1. Harness: loads the fixture: case `RW-2027-001204` in state ANY_STATE with deviation code `X4`, deviation `DEV-SYN-001204`, Aric referral `ARIC-SYN-001204`, investigation `INV-SYN-001204`, business date `2027-04-30` and both outcome branches held; before anything is raised it reads `GET /api/recovery/access/v1/me/session` as a synthetic RW-FRAUD caller, asserts Case record U and reads the case in ANY_STATE. On Day 1 the stubs of §12.8 return the same records.
2. Harness: raises the X4 deviation through `POST /api/recovery/deviation/v1/cases/{caseId}/deviations` with one Idempotency-Key, which starts DeviationWorkflow on the task queue `rwb-deviation`, and asserts the answer carries MSG-S8-001 with the deviation and the fraud team as the handler (R-UNI-08, R-DEV-04).
3. Harness: asserts exactly one Aric referral `ARIC-SYN-001204` is recorded in the run fixture, that it carries the investigation reference `INV-SYN-001204`, and that a repeat of the same raise with the same Idempotency-Key records no second referral and no second investigation.
4. Harness: reads `GET /api/recovery/case/v1/cases/{caseId}` and asserts DEV_FLAGGED, and reads `GET /api/recovery/case/v1/cases/{caseId}/timers` and asserts the stage clock is paused, the prescription clock is still running and the deviation service level timer runs for the case (R-DEV-01, R-DEV-20; Temporal design slide 24).
5. Harness: counts one `rwb.deviation.DeviationRaised.v1` on `rwb.deviation.events.v1`, asserts its consumption through the case read, and replays it once and asserts the case, the timers and the decision log are unchanged, because the inbox holds one processed row per consumer.
6. Harness: assigns the deviation to the fraud team through `PATCH /api/recovery/deviation/v1/deviations/{deviationId}` with one Idempotency-Key, and asserts the case read answers DEV_WITH_OWNER with the fraud team named as the handler (R-DEV-04). The deviation record itself is not read: the map publishes no `GET /deviations`.
7. Harness: reads `GET /api/recovery/decision/v1/decision-log?caseId={caseId}` and asserts one entry for the flag and one for the assignment, each with its rule id and rule version, and that `rwb.decision.DecisionRecorded.v1` was published for each action on `rwb.decision-record.v1` and confirmed by the central ledger in rwb-decision (DP-03).
8. Branch A, fraud confirmed: harness records the confirmation through the patch with the confirmed step and one Idempotency-Key, and asserts the case read answers DEV_REROUTE with the write-off route named for the case (R-DEV-13). The write-off route belongs to S7 and no write-off operation is called.
9. Branch A: harness reads `GET /api/recovery/source-data/v1/data-products/DP13/records?caseId={caseId}` and asserts no write-off row and no posting exists for the case, then reads `GET /api/recovery/source-data/v1/data-products/freshness?product=DP13` and asserts the business date and the load time behind that read, so a stale product is never reported as a clean absence (DP-05).
10. Branch A: harness reads `GET /api/recovery/case/v1/cases/{caseId}` until it answers ROUTE_D6 under R-DEV-19, and counts one `rwb.deviation.DeviationCleared.v1` on `rwb.deviation.events.v1` with its consumption through the case read; the route operation itself belongs to S1 and is not called here.
11. Branch B, fraud not confirmed: harness records the cleared outcome through the patch with the cleared step and one Idempotency-Key on a second run of the fixture, and asserts the case read answers DEV_REROUTE with the collections decision named for the case (R-DEV-14), the decision record naming R-DEV-14, no write-off row in DP13, and the case read in ROUTE_D6 under R-DEV-19.
12. Harness: counts one `rwb.case.CaseStateChanged.v1` per state change on `rwb.case.events.v1` for the case, and asserts the states it observed on each branch are the states published.
13. Harness: forces a decision-record failure and assigns the deviation through the patch, and asserts the answer carries MSG-P7-003 with the case still in DEV_FLAGGED, the same handler, the same timers, no decision log entry and no `DecisionRecorded` publication for that action.
14. Harness: calls `GET /api/recovery/access/v1/me/session` as a synthetic RW-OFF caller with no Case record U, then raises a deviation on the case through `POST /api/recovery/deviation/v1/cases/{caseId}/deviations` and asserts 403 with MSG-P4-002 and no state change.
15. Harness: writes one run report per case and branch, keyed by story, case_no and branch, naming the contract version of each hop, whether the hop was a stub or the owner, the deviation, referral and investigation keys, the states observed, the timer names, the branch outcome and the criteria verdicts.

### 5. Exception paths

| ID | Trigger | What the harness asserts | Message | Covered by |
|---|---|---|---|---|
| X1 | A stub answers a shape the published contract does not allow | The run fails at that hop and the report names the service, the operation and the contract version; no criterion is marked passed | None | TC-E7-004-01-ITG (ITG AC1) |
| X2 | The flag is raised and the case is not in DEV_FLAGGED, the stage clock is not paused, the prescription clock is paused with it, or the referral is not exactly one | The run fails on AC2 and the report names the referral record, the timer, the clock type and the state read; a paused prescription is a failure as serious as an unpaused stage | None | TC-E7-004-01-ITG (ITG AC2) |
| X3 | The case reaches DEV_WITH_OWNER but the fraud team is not the named handler | The run fails on AC3 and the report names the case, the state and the handler read, because a deviation without its named owner is the failure this story is written against | None | TC-E7-004-01-ITG (ITG AC3) |
| X4 | Fraud is confirmed and the case does not reach DEV_REROUTE with the write-off route, or a write-off row or posting is read in DP13 | The run fails on AC4 and the report names the state read, the DP13 row and the freshness stamp; a write-off booked by this run is a loss, not a timing difference | None | TC-E7-004-01-ITG (ITG AC4) |
| X5 | Fraud is not confirmed and the case does not reach DEV_REROUTE with the collections decision, or never reaches ROUTE_D6 | The run fails on AC5 and the report names the state read and the branch fixture | None | TC-E7-004-01-ITG (ITG AC5) |
| X6 | The decision record is written twice, or written without its rule version, or the ledger has not confirmed it, or a deviation event is published twice | The run fails on AC6 and the report names the entries, their rule versions, the publication counts and the missing confirmation | None | TC-E7-004-01-ITG (ITG AC6) |
| X7 | A forced decision-record failure leaves the case changed, or answers without MSG-P7-003 | The run fails on AC7 and the report names the state before and after, the handler and the answer | MSG-P7-003 (expected, and missing) | TC-E7-004-02-ITG and TC-E7-004-04-ITG (ITG AC7) |
| X8 | A caller without Case record U is allowed to raise a deviation | The run fails on AC8 and the report names the caller role, the operation and the answer; a 201 is a failure even when no data changed | MSG-P4-002 (expected, and missing) | TC-E7-004-03-ITG (ITG AC8) |

The report text is for the wave entry check and is not part of the message standard. The business messages the run touches are in section 14 and are asserted by ID and by their substituted values.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Runs against the published contracts and the stubs from Day 1; the only wait is RWB-S8-E7004-APP, and its fixture answers until it lands |
| Negotiable | The fixture layout, the synthetic keys, the referral answer shape, the timer names, the report shape and the gate are configuration agreed at the wave entry check, not business values in code |
| Valuable | The hold and the referral are proved to be same-day and exactly once, the two clocks are proved to pause and to keep running independently, both outcomes are proved to reach the route decision, and a write-off by this run is proved to be absent |
| Estimable | One runner, one stub set, one case fixture, one referral probe, one clock probe, two outcome branches, one money read-back, one event observer and one report |
| Small | Fits in one sprint with its four tests |
| Testable | Each criterion runs against the stubs and again against RWB-S8-E7004-APP as it lands |

### 7. Acceptance criteria

```gherkin
Feature: Run X4 fraud end to end - wave 4 integration harness

  Background:
    Given the synthetic case "RW-2027-001204" carries deviation "DEV-SYN-001204" with deviation code "X4" and the Aric referral "ARIC-SYN-001204" with investigation "INV-SYN-001204"
    Given the fraud flag arrives from Aric or an officer on business date "2027-04-30" and the screening has produced the X4 code for the case
    Given the rule package in force holds R-DEV-04, R-DEV-13, R-DEV-14 and R-DEV-19 and DP13 answers for the case

  Scenario: AC1 Run X4 fraud end to end (legacy RWB-E7-004 AC1)
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then refers to the fraud team, tracks the investigation and routes the case on the outcome
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 The X4 flag holds the case, pauses only the stage clock and refers once to the fraud team (new, D-RCV-60)
    Given the case "RW-2027-001204" is in state ANY_STATE and Aric or an officer has flagged fraud
    When the X4 deviation is raised through POST /api/recovery/deviation/v1/cases/{caseId}/deviations under R-UNI-08 and R-DEV-01
    Then GET /api/recovery/case/v1/cases/{caseId} answers DEV_FLAGGED
    And GET /api/recovery/case/v1/cases/{caseId}/timers shows the stage clock paused and the prescription clock still running
    And exactly one Aric referral "ARIC-SYN-001204" is recorded for the case with the investigation reference "INV-SYN-001204"
    And a repeat of the raise with the same Idempotency-Key records no second referral

  Scenario: AC3 The fraud team is the named handler (new, D-RCV-60)
    Given the case "RW-2027-001204" is in state DEV_FLAGGED with deviation code "X4"
    When the deviation is assigned through PATCH /api/recovery/deviation/v1/deviations/{deviationId} under R-DEV-04
    Then GET /api/recovery/case/v1/cases/{caseId} answers DEV_WITH_OWNER with the fraud team named as the handler
    And the answer carries the same deviation "DEV-SYN-001204", so the assignment moves one deviation and creates none
    And GET /api/recovery/decision/v1/decision-log?caseId={caseId} holds one entry for the assignment with its rule id and rule version

  Scenario: AC4 Fraud confirmed routes to write-off and reopens the route decision (new, D-RCV-60)
    Given the case "RW-2027-001204" is in state DEV_WITH_OWNER with deviation code "X4"
    When the fraud team records fraud confirmed under R-DEV-13
    Then GET /api/recovery/case/v1/cases/{caseId} answers DEV_REROUTE with the write-off route named for the case
    And GET /api/recovery/source-data/v1/data-products/DP13/records?caseId={caseId} holds no write-off row and no posting for the case
    When the case is read again
    Then the case is read in ROUTE_D6 with the segment recomputed and the hard gates re-run under R-DEV-19
    And no write-off is created or posted by this run

  Scenario: AC5 Fraud not confirmed returns the case to the collections decision (new, D-RCV-60)
    Given the case "RW-2027-001204" is in state DEV_WITH_OWNER with deviation code "X4"
    When the fraud team records fraud not confirmed under R-DEV-14
    Then GET /api/recovery/case/v1/cases/{caseId} answers DEV_REROUTE with the collections decision named for the case
    And GET /api/recovery/source-data/v1/data-products/DP13/records?caseId={caseId} holds no write-off row and no posting for the case
    When the case is read again
    Then the case is read in ROUTE_D6 under R-DEV-19

  Scenario: AC6 The decision record is written once per action and confirmed by the central ledger (new, D-RCV-60)
    Given the case carries deviation "DEV-SYN-001204" and the rule package in force holds R-DEV-04, R-DEV-13 and R-DEV-14
    When the flag, the assignment and the outcome have run
    Then GET /api/recovery/decision/v1/decision-log?caseId={caseId} holds one entry per action with its rule id and rule version
    And "rwb.decision.DecisionRecorded.v1" is published once per action on "rwb.decision-record.v1" and confirmed by the central ledger in rwb-decision
    And "rwb.deviation.DeviationRaised.v1" is published once on "rwb.deviation.events.v1" and consumed once by rwb-case, rwb-comms and rwb-treatment
    And a replay of either event leaves the case, the timers and the decision log unchanged, because the inbox holds one processed row per consumer

  Scenario: AC7 A forced decision-record failure stops the action (new, D-RCV-60)
    Given the decision record for the case cannot be written
    When the deviation is assigned through PATCH /api/recovery/deviation/v1/deviations/{deviationId}
    Then the answer carries "MSG-P7-003"
    And the case is still read in DEV_FLAGGED with the same handler and the same timers
    And no decision log entry and no "rwb.decision.DecisionRecorded.v1" exist for that action

  Scenario: AC8 A caller without Case record U is refused (new, D-RCV-60)
    Given a synthetic caller with role "RW-OFF" and no Case record U
    When the caller raises a deviation through POST /api/recovery/deviation/v1/cases/{caseId}/deviations
    Then the answer is 403 with "MSG-P4-002"
    And no deviation is read on the case and no state changes

  Scenario: AC9 A deviation past its service level escalates to the team manager and the breach is reported (new, D-RCV-60)
    Given the case "RW-2027-001204" is in state DEV_WITH_OWNER with deviation code "X4"
    When the deviation service level passes with the deviation still with its owner
    Then GET /api/recovery/case/v1/cases/{caseId} answers with the escalation to the team manager and the breach reported under R-DEV-20
    And the X4 flow runs with its own flow, approver, contact rules and return point under BR8
    And every hop of the run is one REST call on /api/recovery/<short>/v1 with a 2 s timeout

  Scenario: AC10 A consumed call that fails or does not answer is not recorded as complete (new, D-RCV-60)
    Given the case "RW-2027-001204" is in state DEV_FLAGGED with deviation code "X4"
    When a consumed call of the X4 flow fails or does not answer within the 2 s timeout of BR10
    Then the action is not recorded as complete and the case keeps its state and timers
    And the failure answers with a message ID Not specified in the source documents (NEWAC-RWB-ITG-E7004-ITG-AC10)
```

Legacy AC2 (the case in which the decision log cannot be written) is asserted here in AC7; the legacy AC1 wording is kept word for word, and the build of the flow it describes stays with RWB-S8-E7004-APP.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Aric or an officer flags fraud, and the case raises X4, is held and is referred to the fraud team the same day | R-UNI-08 |
| BR2 | X4 is assigned to the fraud team and the case is referred to Aric | R-DEV-04 |
| BR3 | A deviation in any state pauses the stage clock and keeps the prescription clock running, and routes the case to the named owner | R-DEV-01; Temporal and Drools design slide 24 |
| BR4 | Fraud confirmed on X4 routes the case to write-off, and recovery continues under the fraud case | R-DEV-13 |
| BR5 | Fraud not confirmed on X4 returns the case to the collections decision | R-DEV-14 |
| BR6 | After the reroute the case reopens the route decision with the segment recomputed and the hard gates re-run, ending in ROUTE_D6 | R-DEV-19 |
| BR7 | A deviation that sits with its owner past the deviation service level escalates to the team manager and the breach is reported | R-DEV-20 |
| BR8 | Every X1 to X7 deviation runs end to end with its own flow, approver, contact rules and return point | REQ-S8-001 |
| BR9 | Fraud confirmed in Aric stops the litigation and routes the case to write-off at D9; the litigation build is out of scope here and this run reads no legal action | R-LIT-77 |
| BR10 | Every hop in the run is one REST call on the owner's base `/api/recovery/<short>/v1` with a 2 s timeout | DP-11, DP-13 |
| BR11 | ACE data is read only through rwb-source-data's data-product contract with its freshness stamp, never from a view and never from another service's schema | DP-01, DP-05 |
| BR12 | The decision record is written by the owning service through the local decision-record library on `rwb.decision-record.v1`, and the central ledger in rwb-decision confirms it | DP-03; ADR-022 |

The harness asserts these rules and changes none of them; the rules themselves are evaluated in RWB-S8-E7004-APP and the states are held by P3 rwb-case. The referral of BR2 is asserted against the fixture of §12.8, because no Aric operation is published.

Coverage: BR1 by AC2; BR2 and BR3 by AC2 and AC3; BR4 by AC4; BR5 by AC5; BR6 by AC4 and AC5; BR9 (write-off route only) by AC4; BR11 by AC4 and AC5; BR12 by AC6. BR7, BR8 and BR10 are covered by AC9; their test case is TC-E7-004-08-ITG.

Reference data: the run reads lists and parameters only through the reference-data contracts DP-06 and DP-07; the parameter keys read are Not specified in the source documents (DOR-RWB-ITG-E7004-ITG-20).

Outside effects: this run makes no direct call to an outside system. The Aric, NCB, EFS, LIT and SVAF effects and the partner portal are carried as contract dependencies on rwb-integration and built against their published fakes; the interface identity of each is confirmed with P2 before the wave 4 test.

### 9. State transitions

| From | Event | Condition | To | Owner of the change |
|---|---|---|---|---|
| ANY_STATE | DEVIATION_FLAGGED | deviation_code = X4, flagged by Aric or an officer | DEV_FLAGGED | S8 rwb-deviation, DeviationWorkflow, R-UNI-08 and R-DEV-01; `rwb.deviation.DeviationRaised.v1` |
| DEV_FLAGGED | OWNER_ASSIGNED | deviation_code = X4 | DEV_WITH_OWNER | S8 rwb-deviation, R-DEV-04, assigning the fraud team and referring to Aric |
| DEV_WITH_OWNER | FRAUD_CONFIRMED or FRAUD_NOT_CONFIRMED | deviation_code = X4 | DEV_REROUTE | S8 rwb-deviation, R-DEV-13 to the write-off route owned by S7, or R-DEV-14 to the collections decision |
| DEV_REROUTE | ROUTE_REOPENED | any | ROUTE_D6 | P3 rwb-case for the case state and S1 rwb-valuation for the D6 route decision, R-DEV-19 |

The states are the deviation states of R-UNI-08, R-DEV-04, R-DEV-13, R-DEV-14 and R-DEV-19, and the case state is read through the P3 contract after every step. The timers are read through `GET /api/recovery/case/v1/cases/{caseId}/timers`: the stage clock is paused from DEV_FLAGGED, the prescription clock is never paused, and the deviation service level timer of R-DEV-20 runs from DEV_WITH_OWNER. The harness changes no state. Every change in the table is made by the owner: S8 holds the deviation and drives DeviationWorkflow, P3 holds the case state and the timers, S7 holds the write-off route, S1 holds the route decision, and P7 holds the central ledger. A state the harness had set by hand would prove nothing, so the report names the owner and the operation behind every value it asserts.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-FRAUD, fraud investigator | Is the named handler of X4 under R-DEV-04, holds Case record U, and is the role the journey is written for |
| RW-CASEOWN, case owner | Owns the case after the reroute and holds Case record U; the team manager is the escalation point of R-DEV-20 |
| RW-WRITEOFF, write-off team member | Receives the case on the confirmed branch through S7's route under R-DEV-13; no write-off is posted by this run |
| RW-LITOFF, RW-ENFORCE | Read the same evidence where their rights allow; R-LIT-77 is the litigation side of the confirmed branch and is not exercised here |
| RW-OFF, RW-TRIBE, RW-PLATADM | Read only where their rights allow; RW-OFF holds no Case record U and is the refused caller of AC8 |
| QA lead | Owns the harness configuration, the fixtures, the report shape and the pass or fail gate |
| Integration lead | Owns the harness code, the stub set and the swap from a stub to the real service |
| The owning services' identities | S8 runs DeviationWorkflow, writes the decision record and raises the referral, P3 holds the case and the timers, S7 holds the write-off route, S1 holds the route decision, P7 holds the ledger, P1 answers DP13 and P4 answers the session; they make every change the harness asserts |
| No delegation of authority level applies | The harness takes no business decision; authorisation is answered by rwb-access and the DoA is P4's |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 to DF-CAS-023 | recovery_case | case_no, status, stage_code, primary_person_key | Read through the rwb-case contract |
| DF-CAS-036 to DF-CAS-045 | deviation | deviation_code, raised_at, raised_by, paused_state, handler | Written through the rwb-deviation raise and patch, read back through the case and the timers |
| DF-WRK-027 to DF-WRK-036 | timer | timer_type, started_at, expires_at, paused_at | Read through the rwb-case timers contract |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | decision_code, rule_id, rule_version | Read through the rwb-decision contract |
| DF-REF-001 to DF-REF-015 | rule_row | rule_id, rule_version, from_state, event_code | Read through the rwb-decision contract |
| DP13 Money and closure | money and closure data product | write-off and closure rows of the case | Read through the rwb-source-data data-product contract, to prove no write-off is posted |

Field IDs are those in the Logical Data Model and Data Dictionary v9. The case and the timers are P3's, the deviation is S8's, the decision log and the rule rows are P7's, and the money and closure side is DP13 behind P1's contract; the harness reads them only through those contracts and never from a schema. The harness owns no table and writes no row. The two writes it makes are the owner's published operations of §12.2, taken with one Idempotency-Key each. The referral and investigation keys of the fixture are run data and are not a field of any table this story owns.

### 12. Contract

#### 12.1 REST operations provided

None. The harness is a test runner and provides no REST operation.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| POST | `/api/recovery/deviation/v1/cases/{caseId}/deviations` | S8 rwb-deviation | Raises the X4 deviation and starts DeviationWorkflow, with one Idempotency-Key (AC1, AC2, AC6, AC8) |
| PATCH | `/api/recovery/deviation/v1/deviations/{deviationId}` | S8 rwb-deviation | The assignment to the fraud team and the confirmed or cleared outcome, with one Idempotency-Key (AC3, AC4, AC5, AC7) |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The case state after the flag, the assignment and each outcome, and the handler (AC1 to AC8) |
| GET | `/api/recovery/case/v1/cases/{caseId}/timers` | P3 rwb-case | The stage clock, the prescription clock and the deviation service level timer (AC2, AC6, AC7) |
| GET | `/api/recovery/decision/v1/decision-log?caseId={caseId}` | P7 rwb-decision | The decision record of the flag, the assignment and the outcome, with the rule version and the ledger confirmation (AC1, AC3, AC6, AC7) |
| GET | `/api/recovery/source-data/v1/data-products/DP13/records?caseId={caseId}` | P1 rwb-source-data | The money and closure rows of the case, to prove no write-off and no posting exist (AC4, AC5) |
| GET | `/api/recovery/source-data/v1/data-products/freshness?product=DP13` | P1 rwb-source-data | The business date and the load time behind the DP13 read (AC4, AC5). The answer's `status` is LOADED or STALE, and a never-stamped product answers STALE with `businessDate` null (RD-P1-005, RD-P1-041) |
| GET | `/api/recovery/access/v1/me/session` | P4 rwb-access | The caller's roles and rights before a write (AC2, AC8) |

Every call is one hop on the owner's base `/api/recovery/<short>/v1` with a 2 s budget (DP-11, DP-13). No operation is invented in this story: each path is the owner's published operation in the Ownership Map, and where a screen would compose them the path would be the gateway-bff composite route (DP-19). The map publishes no `GET /deviations` and no clear operation for S8, and this story does not pretend otherwise: the deviation is asserted through three published reads — the case read for the state and the handler, the timers read for the clocks and the service level, and the decision log for the record — plus the `rwb.deviation.DeviationRaised.v1` and `rwb.deviation.DeviationCleared.v1` publications, and the two writes above are the only deviation operations the run uses.

#### 12.3 Events published

None. The harness publishes no Kafka event; it writes its report to the wave record.

#### 12.4 Events consumed

| Event | Topic | Producer | Use in the run |
|---|---|---|---|
| `rwb.deviation.DeviationRaised.v1` | `rwb.deviation.events.v1` | S8 rwb-deviation | Counts one publication after the X4 flag and, with the replay, proves one processed row per consumer (AC6) |
| `rwb.deviation.DeviationCleared.v1` | `rwb.deviation.events.v1` | S8 rwb-deviation | Counts one publication when the deviation clears and the case leaves DEV_REROUTE (AC4, AC5) |
| `rwb.case.CaseStateChanged.v1` | `rwb.case.events.v1` | P3 rwb-case | Proves the observed states are the states published for the case on both branches (AC2 to AC5) |
| `rwb.decision.DecisionRecorded.v1` | `rwb.decision-record.v1` | S8 rwb-deviation through the local decision-record library (DP-03) | Proves the record was published once per action with its rule version and confirmed by the central ledger (AC1, AC3, AC6, AC7) |

The harness subscribes to the three topics under one consumer group of its own, counts publications and replays each event once. The consumer effect it reads is the case through the rwb-case operation of §12.2; the inbox row counts of rwb-comms and rwb-treatment come from the consumer evidence in the run fixture, because neither consumer exposes an operation in this story. `rwb.deviation.DeviationCleared.v1` is asserted by count and by the case state that follows it, since the map publishes no clear operation to drive.

#### 12.5 Workflows and activities

None added. The harness exercises DeviationWorkflow, S8's child workflow on the task queue `rwb-deviation` in the `rwb-recovery` namespace, started through the deviation raise and continued through the patch: it is the workflow that carries the X4 route, the referral, the pause of the stage clock, the service level timer and the confirmed or cleared outcome. It observes CaseWorkflow on `rwb-case`, the parent that receives the deviation through the case router as a signal and pauses and resumes the stage clock for the case (Arch v5 slide 25). Both are stated here as observed and not built here; no workflow, activity or Schedule is created, changed or owned by this story, and the write-off workflow on `rwb-writeoff` is never started by this run.

#### 12.6 Schedules

None added. The X4 flag arrives as a flag and a referral, and neither outcome is on a cron: the harness starts the run with the raise operation and holds both branch answers in its own fixture instead of waiting on a schedule. The deviation service level of R-DEV-20 is a durable timer inside the workflow and not a job, which is why the clocks and the service level are read through the timers operation and never through a scheduler.

#### 12.7 Tables owned

None. The harness owns no schema and no table (DP-01); deviation is S8's, recovery_case and timer are P3's, decision_log_entry and rule_row are P7's, and the money and closure side belongs to DP13 behind P1's contract.

#### 12.8 Contract fakes

| Fake | Contract | Stubbed answer in the run |
|---|---|---|
| Stub for rwb-deviation | `POST /cases/{caseId}/deviations`, `PATCH /deviations/{deviationId}` | Accepts the raise once per Idempotency-Key on case `RW-2027-001204` and answers MSG-S8-001 with deviation `DEV-SYN-001204` and the fraud team as the handler; the patch accepts the assignment and either outcome and keeps the same deviationId |
| Stub for rwb-case | `GET /cases/{caseId}`, `GET /cases/{caseId}/timers` | Case `RW-2027-001204` in DEV_FLAGGED, then DEV_WITH_OWNER with the fraud team, then DEV_REROUTE on either branch, then ROUTE_D6; the stage clock paused, the prescription clock running and the service level timer |
| Stub for rwb-source-data | DP13 records and freshness | The money and closure rows of the case with no write-off and no posting, and business date `2027-04-30` with a load time |
| Stub for rwb-decision | `GET /decision-log?caseId={caseId}` | One entry per action with its rule id and rule version, and the central ledger confirmation |
| Stub for rwb-access | `GET /me/session` | Allows RW-FRAUD with Case record U; refuses RW-OFF, which holds no Case record U, with 403 and MSG-P4-002 |
| Aric referral fixture | The referral of INT-31 and the investigation evidence | Exactly one referral `ARIC-SYN-001204` with investigation `INV-SYN-001204`, one answer per branch, and no second referral on a repeated raise; it stands at the point where the real Aric referral would answer |

Each stub is generated from the published contract and its version is pinned in the run report, so a contract change shows up as a run failure and not as a silent pass. The Aric referral fixture is not a contract: no Aric operation is published, so the harness asserts the referral record it holds and never calls Aric. The harness environment and base hosts, the fixture layout, the synthetic case, deviation and referral keys, the Aric referral answer shape and status vocabulary, the investigation tracking evidence, the evidence format and retention, and the pass or fail gate are Not specified in the source documents (GAP-0469; ASM-0661).

#### 12.9 Call-type summary

| Call type | In this story |
|---|---|
| REST | 0 provided, 8 consumed, one hop each on `/api/recovery/<short>/v1` with a 2 s budget (DP-11, DP-13) |
| Kafka | None published; four consumed, `rwb.deviation.DeviationRaised.v1`, `rwb.deviation.DeviationCleared.v1`, `rwb.case.CaseStateChanged.v1` and `rwb.decision.DecisionRecorded.v1`, counted and replayed once |
| Temporal | None added; DeviationWorkflow on `rwb-deviation` exercised from the raise, with CaseWorkflow on `rwb-case` observed as the parent that pauses and resumes the stage clock |
| File | None. Both branch answers and the Aric referral are held in the run fixture; no file or claim-check is transferred by this story |

### 13. Solution plan

**Package.** Folder `itg/recovery`, package `th.co.scb.ace.workbench.recovery.itg`, test scope only; not part of any deployed service.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The H dependencies DP-03 and DP-19 add, RWB-PLT-E1027-CON and RWB-PLT-N001-CON, are platform stories delivered by the platform wave and are not repeated in the metadata H field of this story, which stays None; DP-13 adds nothing. The one blocking dependency is the I story RWB-S8-E7004-APP, which replaces its stub; until it is live the run uses the stub, and a stub pass is reported as a stub pass. Aric adds no dependency: INT-31 is not available today and the referral is a fixture.

**Harness components**

| Component | Type | Responsibility |
|---|---|---|
| JourneyRunner | Job | Runs the criteria in order for a case and branch and holds the run lock |
| DeviationDriver | Service | Raises the X4 deviation and patches the assignment and the outcome, once per Idempotency-Key |
| ReferralProbe | Service | Asserts exactly one Aric referral with its investigation reference, and no second referral on a repeated raise |
| ClockProbe | Service | Reads the timers and asserts the stage clock paused, the prescription clock running and the service level timer present |
| OutcomeProbe | Service | Reads the case on both branches and asserts DEV_REROUTE and then ROUTE_D6, with the route each branch names |
| MoneyReadBack | Service | Reads DP13 with the freshness stamp and names any write-off row or posting seen for the case |
| DecisionProbe | Service | Reads the decision log and asserts one record per action, with its rule version and the ledger confirmation |
| EventObserver | Service | Subscribes to `rwb.deviation.events.v1`, `rwb.case.events.v1` and `rwb.decision-record.v1`, counts publications and replays each event once |
| StubSet | Fake | The five stubs and the Aric referral fixture of §12.8, generated from the published contracts with the version pinned |
| EvidenceReport | Service | Writes one report per case and branch, keyed by story, case_no and branch, and holds the pass or fail gate |

**Environment and test data.** SIT, against the stubs from Day 1 and the real services as RWB-S8-E7004-APP lands, on synthetic case `RW-2027-001204`, deviation `DEV-SYN-001204`, Aric referral `ARIC-SYN-001204`, investigation `INV-SYN-001204` and business date `2027-04-30`, in two runs: fraud confirmed and fraud not confirmed. The harness seeds nothing by hand and never writes a schema row. The environment and base hosts, the fixture layout, the synthetic keys, the referral answer shape and status vocabulary, the evidence format and retention, and the pass or fail gate are Not specified in the source documents (GAP-0469; ASM-0661).

**Build steps**

1. Generate the five stubs and the Aric referral fixture from the published contracts and pin each contract version in the run report; fail the run on a mismatch (X1).
2. Build the DeviationDriver for the raise and prove it is accepted once per Idempotency-Key and answers MSG-S8-001 with the deviation and the fraud team (AC1).
3. Add AC2 on the case read, the timers read and the ReferralProbe: DEV_FLAGGED, the stage clock paused and the prescription clock still running, and exactly one referral with no second on a repeated raise (X2).
4. Add AC3 on the assignment patch and the case read, asserting DEV_WITH_OWNER with the fraud team as the handler (X3).
5. Add AC4 on the confirmed branch: DEV_REROUTE with the write-off route, then ROUTE_D6, and the MoneyReadBack proving no write-off row and no posting in DP13 (X4).
6. Add AC5 on the cleared branch in a second run: DEV_REROUTE with the collections decision, then ROUTE_D6, and the same money read (X5).
7. Add the EventObserver for AC6: one DeviationRaised publication with its consumption, one CaseStateChanged per state, and a replay that changes nothing because the inbox holds one row per consumer (X6).
8. Add the DecisionProbe for AC6 and AC7: one entry per action with its rule version and the ledger confirmation, then a forced write failure that leaves the case and the timers untouched and answers MSG-P7-003 (X7).
9. Add the access path for AC8 through the session read and the raise operation, assert 403 with MSG-P4-002 and no state change, then add the EvidenceReport and the gate, and swap a stub for the real owner as RWB-S8-E7004-APP lands (X8).

**Feature switch.** None. The harness has no production flag and runs in the test environment only.

**Done when.** The tests of section 16 pass against the fakes and again against RWB-S8-E7004-APP when it lands, and the wave entry check holds a run report keyed by story, case_no and branch.

### 14. Validation and messages

| ID | Type | Message |
|---|---|---|
| MSG-S8-001 | Information | {deviation} was raised. The case is with {handler}. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The harness asserts the message ID and the substituted values on the answer it reads, and owns no message text. MSG-S8-001 is asserted with the deviation and the fraud team as the handler when the X4 flag is raised, MSG-GEN-001 with the missing field when a write is made short of a required parameter, MSG-P4-002 with the refused raise for a caller that holds Case record R and not U, and MSG-P7-003 when the decision record cannot be written and nothing changes.

### 15. Screens and states

The legacy story's screens are SCR-08 Deviation queue and SCR-06 Raise deviation, and neither is built or rendered here: the harness calls the two operations behind them and reads the states through the owners. What the wave entry check looks at instead is the run report, whose environment, layout and retention are Not specified in the source documents (GAP-0469; ASM-0661).

| State | Read through | What the run asserts |
|---|---|---|
| DEV_FLAGGED | rwb-case case read and timers read | The X4 flag is raised, the case is held, the stage clock is paused, the prescription clock runs, and one referral exists |
| DEV_WITH_OWNER | rwb-case case read and timers read | The fraud team is the handler, the service level timer runs, and the decision record exists with its rule version |
| DEV_REROUTE, write-off route | rwb-case case read and the DP13 read | Fraud is confirmed, the case names the write-off route, and no write-off row or posting exists in DP13 |
| DEV_REROUTE, collections route | rwb-case case read and the DP13 read | Fraud is not confirmed, the case names the collections decision, and no write-off row or posting exists in DP13 |
| ROUTE_D6 | rwb-case case read | The case reopens the route decision under R-DEV-19 and the deviation clears on either branch |
| A refused raise | rwb-access session read and the raise answer | 403 with MSG-P4-002 and no state change |
| SCR-06 Raise deviation: empty, loading, error, no access | Not specified in the source documents (CG-ALL-1168) | Not specified in the source documents (CG-ALL-1168) |
| SCR-08 Deviation queue: empty, error, no access | Not specified in the source documents (CG-ALL-1169) | Not specified in the source documents (CG-ALL-1169) |
| SCR-08 Deviation queue: loading | Screen Specifications v1 section SCR-08 | Taken from Screen Specifications v1 section SCR-08 |

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E7-004-01-ITG | AC1 (legacy); ITG AC1 to AC6 | End to end | One case with an X4 flag, the referral, the assignment and both outcome branches live |
| TC-E7-004-02-ITG | AC2 (legacy, the not-recorded case); ITG AC7 | Integration | A forced decision-record failure on the assignment |
| TC-E7-004-03-ITG | Access; ITG AC8 | Component | An RW-OFF caller with no Case record U |
| TC-E7-004-04-ITG | Principle 5; ITG AC7 | Integration | A forced decision-record failure at the point of the state change |
| TC-E7-004-05-ITG | ITG AC3 | Integration | Case RW-2027-001204 in DEV_WITH_OWNER with deviation code X4; the fraud team is read as the named handler |
| TC-E7-004-06-ITG | ITG AC4 | Integration | Case RW-2027-001204 in DEV_WITH_OWNER with deviation code X4; fraud confirmed under R-DEV-13 |
| TC-E7-004-07-ITG | ITG AC5 | Integration | Case RW-2027-001204 in DEV_WITH_OWNER with deviation code X4; fraud not confirmed under R-DEV-14 |
| TC-E7-004-08-ITG | ITG AC9; BR7, BR8, BR10 | Integration | Case RW-2027-001204 in DEV_WITH_OWNER with deviation code X4; the deviation service level has passed |
| TC-E7-004-09-ITG | ITG AC10 | Integration | Case RW-2027-001204 in DEV_FLAGGED with deviation code X4; a consumed call forced to fail or not answer within the 2 s timeout |

The AC column names the legacy test the copy derives from and the ITG criteria it asserts, and the full legacy test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx under the same legacy test case ID. Legacy AC2 stays with RWB-S8-E7004-APP as a build criterion; the -ITG copies here assert the same behaviour across the service boundary.

The X4 harness environment, base hosts, fixture layout, synthetic deviation and referral keys, referral answer shape, status vocabulary, investigation tracking evidence, evidence format and retention, and the pass or fail gate are Not specified in the source documents (GAP-0469). They are agreed at the wave 4 entry check and held as harness configuration, not as business values in code.

### 17. Guardrails

- No business value in code: the synthetic case, deviation, referral and investigation keys, the business date, the timer names, the service level and the report layout are data.
- No personal data in logs, events or reports: every key is synthetic, and the events carry IDs and facts only.
- ACE data only through the P1 contract: DP13 with its freshness stamp, never a direct view read and never another service's schema (DP-01, DP-05).
- One hop and a 2 s budget per call, with a circuit breaker per downstream, so the harness fails where a screen would (DP-11, DP-13).
- No invented Aric operation: the referral is asserted against the fixture of §12.8, and no endpoint, topic or status word for Aric is created here.
- No write-off created by this run: DP13 is read to prove the posting is absent, and S7's write-off route is named by the case and never called.
- A stub pass is never reported as a real pass: the report names the contract version and whether the hop was a stub or the owner.
- The harness never runs against UAT or production, and it never writes a row by hand or sets a state it then asserts.
- A failing criterion is fixed in the owning service or raised as a gap; it is never waived in the script.

### 18. Traceability

| Item | Source | Where it lands |
|---|---|---|
| Legacy story RWB-E7-004 Run X4 fraud end to end | Recovery Workbench User Stories Epics 3 to 8 v4, lines 11212 to 11291 | Sections 1, 3, 11, 14 and 19 of this file |
| Legacy AC1, verbatim | The same, lines 11231 to 11235 | Section 7, AC1, marked (legacy RWB-E7-004 AC1) |
| Legacy AC2, the case in which the decision log cannot be written | The same, lines 11237 to 11241 | Section 7, AC7; the legacy criterion stays with RWB-S8-E7004-APP (section 19) |
| Legacy test cases TC-E7-004-01 to TC-E7-004-04 | The same, lines 11286 to 11289 | Copied as -ITG in section 16 |
| Legacy endpoints, screens, permission check and messages | The same, lines 11253 to 11280 | Sections 12.2, 15 and 14 |
| FEAT-DVF-04 Run X4 fraud end to end | Epics 3 to 8 Specification v3, line 127 | Sections 1 and 2 |
| INT-31 Aric, the fraud referral | The same, line 240 | Sections 2, 3, 12.8 and 19: a fixture, not an external dependency |
| REQ-S8-001 | Business Requirements Program v5, line 417 | Section 8, BR8 |
| R-DEV-01, R-DEV-04, R-DEV-13, R-DEV-14, R-DEV-19 and R-DEV-20 | Business Rules and Routing Logic v4, lines 383, 386, 395, 396, 401 and 402 | Sections 8 and 9 |
| R-UNI-08 | The same, line 412 | Section 8, BR1 |
| R-LIT-77, fraud confirmed in Aric stops the litigation and routes to write-off | The same, line 216 | Section 8, BR9; the litigation build is out of scope (section 19) |
| DF-CAS-001 to DF-CAS-023, DF-CAS-036 to DF-CAS-045, DF-WRK-027 to DF-WRK-036, DF-DEC-001 to DF-DEC-018, DF-REF-001 to DF-REF-015 | Logical Data Model and Data Dictionary v9 | Section 11 |
| DP-03, DP-13 and DP-19 | Template and Rules v1 §R5.5 | Section 13, pattern application |
| ADR-015, ADR-020 and ADR-022 | Architecture Decision Records v4 | Sections 12.4, 12.2 and 8: outbox and inbox on Kafka, contract-first REST with one hop and 2 s, local decision record plus central ledger |
| The S8 contract and the deviation events | Architecture v5 slides 15 and 41 to 44 (S8 contract, lines 1049 to 1069; event rows 06 and 07) | Sections 2, 8, 12.4, 12.5 and 13 |
| One case workflow with a child per stage, including deviation, route decision and write-off | Architecture v5 slide 25 | Sections 2, 9 and 12.5 |
| DeviationWorkflow, the pause of the stage clock and the parent CaseWorkflow | Temporal and Drools design slides 13 and 24, extract lines 1566 to 1661 | Sections 2, 8, 12.5 and 13 |

### 19. Out of scope

- RWB-S8-E7004-CON and RWB-S8-E7004-APP: the build of the X4 route, the referral, the confirmed and cleared outcomes and the re-route.
- The Aric integration (INT-31) and FEAT-ADM-13: no Aric operation is built, called or contracted here; the referral is a fixture.
- The write-off build (RWB-S7-*): DP13 is read to prove a write-off is absent, and no write-off is created or posted here.
- The route decision of S1 and its approval on P7: ROUTE_D6 is read through the case, and the route operation is not called by this story.
- The litigation build of S4 and the litigation side of R-LIT-77: no legal action is read or changed by this run.
- The S8 screening and the other six deviation codes (RWB-S8-E7001-*, RWB-S8-E7002-*, RWB-S8-E7003-*, RWB-S8-E7005-* to RWB-S8-E7007-*), and the screening dependency FEAT-DVH-04.
- SCR-08 Deviation queue and SCR-06 Raise deviation, and every gateway-bff composite route.
- The platform stories and their H dependencies named in section 13, including RWB-PLT-E1027-CON and RWB-PLT-N001-CON.
- Any production change: no endpoint, table, workflow, activity, schedule, screen, feature flag or configuration in any service.
