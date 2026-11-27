# RWB-ITG-E7003-ITG Run X3 deceased customer end to end

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-E7003-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W4 |
| Wave | 4 |
| Business epic | EP07 |
| Release | 31 May 2027 (tentative) |
| Legacy key | RWB-E7-003 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | L-ITG-W4 |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-ITG-E7003-ITG-16) |
| Contract version | v1 (the /v1 path major version of each operation in section 12.2; minor version not specified in the source documents (DOR-RWB-ITG-E7003-ITG-23)) |
| Contract fake library version | Not specified in the source documents (DOR-RWB-ITG-E7003-ITG-22) |
| Depends on (build) | RWB-S8-E7003-APP (not done yet) |
| Contract dependencies | RWB-S8-E7003-CON |
| Integration dependencies | RWB-S8-E7003-APP |
| External dependencies | None |
| Reference data | Reference-data contract DP-06 and DP-07; parameters: Not specified in the source documents (DOR-RWB-ITG-E7003-ITG-20) |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E7-003 as the wave 4 integration proof of the X3 deceased customer deviation, from the confirmed death through the contact stop and the assignment to the specialist and Legal to the insurance answer and the close or the return to the route decision, observed across rwb-deviation, rwb-case, rwb-source-data, rwb-document and rwb-decision; the build of the X3 flow is RWB-S8-E7003-APP. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-ITG-E7003-ITG). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (17 resolved, 7 cross-document, 2 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **hardship and vulnerability specialist**, I want **the X3 deceased customer deviation to stop all contact the same day, hold the case for the specialist and Legal with the stage clock paused and the prescription clock still running, and carry the insurance answer and the estate position through to a close or back to the route decision, proved end to end against the real services**, so that **every deviation has a handler and a clock, and a customer who has died is never chased, never written to and never left in a state that nobody revisits**.

This story builds the harness and the evidence, and nothing else. The X3 screening, the deviation, the contact stop, the branch on the insurance answer and the return point are built by S8 in RWB-S8-E7003-APP and its CON story; the case state and the timers are P3's, the death certificate and the claim evidence are P5's, the party data and the freshness stamp are P1's, and the decision record is written through P7's library. The harness raises and drives the deviation through S8's published operations, observes every hop through the owners' published contracts, and writes a run report per case and branch. It builds no production endpoint, no table, no workflow, no activity, no schedule and no screen, and it writes no code in any service.

### 2. Business rationale

A customer dies and the case carries on being chased. That is the failure this story is written against, and it is the one the published universal rule names in its first clause: R-UNI-05 requires that a death confirmed from the registry or from a document raises X3, stops all contact and holds the case for the specialist and Legal, on the same day. A demand letter or a call to a bereaved family is not a poor outcome, it is a conduct breach and a legal exposure, and it cannot be undone by an apology. The same rule puts a person on the case, because an estate claim is not an agent decision: R-DEV-03 assigns X3 to the specialist and joins Legal for the estate claim.

The second half of the story is the branch, and it is where the legacy story is weakest. Under R-DEV-11 a X3 case whose insurance clears the balance closes on CASE_ENDED with its timers stopped; under R-DEV-12 a X3 case whose insurance does not clear returns to the route decision against the estate, and R-DEV-19 reopens that decision with the segment recomputed and the hard gates re-run, which is where ROUTE_D6 comes from. Both ends are legitimate and both must be proved, because a harness that only proved the happy close would never see the case that has to come back to the route decision with an estate in front of it. The Temporal design shows the shape of the first hours on slide 8: X3 raised on 10 December against case RW-2026-000502, contact stopped, the stage clock paused while the prescription clock keeps running, and the case routed to the specialist and Legal. The prescription clock is a legal deadline and the design is explicit that it is never paused, even during a deviation.

One correction is made here and it is recorded rather than smoothed over. Legacy AC3 is an X3 scenario but cites R-DEV-06, and R-DEV-06 is the X6 and X7 rule ("Agent handles within policy; a person approves an insurance claim"). No approval step is invented in this story: the published X3 branch has none, the assignment is R-DEV-03 and the two outcomes are R-DEV-11 and R-DEV-12. The conflict is carried as GAP-0467, the legacy criterion stays with RWB-S8-E7003-APP as its build criterion, and the harness asserts the published rules of section 8 instead of the legacy wording.

The harness is decoupled the way the services are. Every call is one hop on `/api/recovery/<short>/v1` with a 2 s budget (DP-11, DP-13). The legacy story reads `v_ace_customer`; in the target the deceased flag and the party data are read only through rwb-source-data's DP02 Customer and party contract with its freshness stamp, never from a view and never from another service's schema (DP-05, DP-01), and the screening itself consumes `rwb.source-data.AceDataReady.v1`, which carries the deceased and bankrupt flags (Arch v5 slide 15 S8 IN, slide 42 row 26). The decision record is written by S8 through the local decision-record library on `rwb.decision-record.v1` (DP-03) and read back through rwb-decision's contract, and the death certificate and the claim evidence are read through P5's document contract as DP10 Documents and extracted fields. Where a screen would compose these calls the path is the gateway-bff composite route (DP-19). The story carries REQ-S8-001 and the X3 rules into evidence rather than restating them.

### 3. Preconditions

- The published contracts of S8 rwb-deviation (the deviation raise and the patch), P3 rwb-case (the case and its timers), P1 rwb-source-data (DP02 Customer and party, and the freshness read), P5 rwb-document (the case document list and the document read), P7 rwb-decision (the decision log) and P4 rwb-access (the session) are in the contract registry, and a stub set is generated from each one.
- The data product catalog holds DP02 Customer and party and DP10 Documents and extracted fields, each with one system of record, so the deceased flag and the death certificate have one named owner before a value is asserted (FSD P1 v3, A2.2).
- RWB-S8-E7003-APP owns the X3 flow, the contact stop and the branch on the insurance answer; until it lands, the fixture of §12.8 stands in for its effect and the story is reported as a stub pass.
- FEAT-DVF-03 is the S8 feature and FEAT-DVH-04 is its screening dependency: the fixture holds an X3 code that screening has already produced, so this story never asserts a screening score, a confidence band or a human review threshold (R-DEV-01).
- The X3 assignment is R-DEV-03, the close is R-DEV-11, the return is R-DEV-12 and the reopen of the route decision is R-DEV-19; the harness asserts those rules and changes none of them.
- The harness environment and base hosts, the fixture layout, the synthetic case, deviation, document and claim keys, the stub answer shapes, the insurer and estate answer shapes, the heir-notification content, the evidence format and retention, and the pass or fail gate: Not specified in the source documents (GAP-0468; ASM-0660).
- The synthetic case, its deviation, its documents, its two branch outcomes and the business date are held in the fixture as data, not written in code.
- No build dependency. Day 1, with the stubs in place from the first run; the one wait is RWB-S8-E7003-APP, which replaces its stub and never blocks the lane.

### 4. Flow

1. Harness: loads the fixture: case `RW-2027-001203` in state ANY_STATE with deviation code `X3`, deviation `DEV-SYN-000203`, death certificate `DOC-SYN-000203`, claim evidence `DOC-SYN-000204`, insurance claim `CLM-SYN-000203`, business date `2027-05-14` and one estate position held for branch B. On Day 1 the stubs of §12.8 return the same records.
2. Harness: reads `GET /api/recovery/source-data/v1/data-products/DP02/records?caseId={caseId}` and asserts the deceased flag and the party of the case, then reads `GET /api/recovery/source-data/v1/data-products/freshness?product=DP02` and asserts the business date and the load time behind that read, so a stale product is never reported as a clean contact stop (R-UNI-05, DP-05).
3. Harness: counts one `rwb.source-data.AceDataReady.v1` on `rwb.source-data.events.v1` and asserts its consumption by rwb-deviation, which is the screening trigger that turns the deceased flag into an X3 code (Arch v5 slide 15 S8 IN, slide 42 row 26).
4. Harness: raises the X3 deviation through `POST /api/recovery/deviation/v1/cases/{caseId}/deviations` with one Idempotency-Key, which starts DeviationWorkflow on the task queue `rwb-deviation`, and asserts the answer carries MSG-S8-001 with the deviation and the handler.
5. Harness: reads `GET /api/recovery/case/v1/cases/{caseId}` and asserts DEV_FLAGGED on the same business date, and reads `GET /api/recovery/case/v1/cases/{caseId}/timers` and asserts the stage clock is paused while the prescription clock is still running (R-UNI-05, R-DEV-01; Temporal design slide 8).
6. Harness: asserts no outbound contact is read for the case on the DP02 contact points, so the contact stop is proved on data and not only on the state (R-UNI-05).
7. Harness: assigns the deviation through `PATCH /api/recovery/deviation/v1/deviations/{deviationId}` with one Idempotency-Key, and asserts the case read answers DEV_WITH_OWNER with the specialist named as the handler and Legal named for the estate claim (R-DEV-03). The deviation record itself is not read: the map publishes no `GET /deviations`.
8. Harness: reads `GET /api/recovery/document/v1/cases/{caseId}/documents` and asserts the death certificate and the claim evidence are listed with their types and sources, then reads `GET /api/recovery/document/v1/documents/{documentId}` for each and asserts the metadata and the extracted fields behind the estate claim (DP10).
9. Branch A, insurance clears: harness records the settlement through `PATCH /api/recovery/deviation/v1/deviations/{deviationId}` with the resolved step and one Idempotency-Key, and asserts the case read answers CASE_ENDED and the timers read shows the stage clock and the prescription clock stopped (R-DEV-11).
10. Branch B, insurance does not clear: harness records the estate position through the same patch with the return step and one Idempotency-Key, and asserts the case read answers DEV_REROUTE (R-DEV-12).
11. Branch B, continue: harness reads `GET /api/recovery/case/v1/cases/{caseId}` until it answers ROUTE_D6 under R-DEV-19, and asserts the route decision is S1's product and that no route operation is called by this run.
12. Harness: reads `GET /api/recovery/decision/v1/decision-log?caseId={caseId}` and asserts one entry per action with its rule id and rule version, that `rwb.decision.DecisionRecorded.v1` was published once on `rwb.decision-record.v1` and confirmed by the central ledger in rwb-decision (DP-03), and that `rwb.document.DocumentStored.v1` was published once per stored document.
13. Harness: replays the `AceDataReady` and `DeviationRaised` events once each and asserts the case, the timers, the document list and the decision log are unchanged, because the inbox holds one processed row per consumer.
14. Harness: writes one run report per case and branch, keyed by story, case_no and branch, naming the contract version of each hop, whether the hop was a stub or the owner, the deviation and document keys, the states observed, the timer names, the branch outcome and the criteria verdicts.

### 5. Exception paths

| ID | Trigger | What the harness asserts | Message | ITG test case | Covered by |
|---|---|---|---|---|---|
| X1 | A stub answers a shape the published contract does not allow | The run fails at that hop and the report names the service, the operation and the contract version; no criterion is marked passed | None | TC-E7-003-01-ITG (ITG AC1) | AC1 |
| X2 | The death is confirmed and the case is not in DEV_FLAGGED on the same business date | The run fails on AC2 and the report names the DP02 read, the freshness stamp and the state read, because a late flag is the conduct breach this story exists to catch | None | TC-E7-003-02-ITG (ITG AC2) | AC2 |
| X3 | The case is flagged and contact is still read for the case, or the prescription clock is paused with the stage clock | The run fails on AC2 and the report names the contact point, the timer, the clock type and the state read; a paused prescription is a failure as serious as a live contact plan | None | TC-E7-003-02-ITG (ITG AC2) | AC2 |
| X4 | The case reaches DEV_WITH_OWNER but the specialist and Legal are not the named handlers | The run fails on AC3 and the report names the case, the state and the handler read, because a deviation without the named owner is the failure this story is written against | None | TC-E7-003-02-ITG (ITG AC3) | AC3 |
| X5 | The insurance answer clears the balance and the case does not reach CASE_ENDED, or a timer still runs | The run fails on AC4 and the report names the state read and the timer names | None | TC-E7-003-03-ITG (ITG AC4) | AC4 |
| X6 | The insurance answer does not clear and the case does not reach DEV_REROUTE, or never reaches ROUTE_D6 | The run fails on AC5 and the report names the state read and the branch fixture | None | TC-E7-003-03-ITG (ITG AC5) | AC5 |
| X7 | The decision record is written twice, or without its rule version, or a document event is published twice, or the ledger has not confirmed it | The run fails on AC6 and the report names the entries, their rule versions, the publication counts and the missing confirmation | None | TC-E7-003-01-ITG (ITG AC6) | AC6 |
| X8 | A forced decision-record failure leaves the case changed, or answers without MSG-P7-003 | The run fails on AC7 and the report names the state before and after, the handler and the answer | MSG-P7-003 (expected, and missing) | TC-E7-003-04-ITG (ITG AC7) | AC7 |
| X9 | A caller without the Case record U is allowed to raise a deviation | The run fails on AC8 and the report names the caller role, the operation and the answer; a 201 is a failure even when no data changed | MSG-P4-002 (expected, and missing) | TC-E7-003-05-ITG (ITG AC8) | AC8 |

The report text is for the wave entry check and is not part of the message standard. The business messages the run touches are in section 14 and are asserted by ID and by their substituted values.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Runs against the published contracts and the stubs from Day 1; the only wait is RWB-S8-E7003-APP, and its fixture answers until it lands |
| Negotiable | The fixture layout, the synthetic keys, the two branch answers, the timer names, the report shape and the gate are configuration agreed at the wave entry check, not business values in code |
| Valuable | The contact stop is proved to be same-day, the two clocks are proved to pause and to keep running independently, both the close and the return to the route decision are proved, and the ACE read is proved to go through the contract and not a view |
| Estimable | One runner, one stub set, one case fixture, one screening probe, one clock probe, one document probe, two branch answers, one event observer and one report |
| Small | Fits in one sprint with its six tests |
| Testable | Each criterion runs against the stubs and again against RWB-S8-E7003-APP as it lands |

### 7. Acceptance criteria

```gherkin
Feature: Run X3 deceased customer end to end - wave 4 integration harness

  Background:
    Given the synthetic case "RW-2027-001203" carries deviation "DEV-SYN-000203" with deviation code "X3" and death certificate "DOC-SYN-000203"
    Given the deceased flag arrives through the DP02 Customer and party contract of rwb-source-data on business date "2027-05-14" and the screening consumes "rwb.source-data.AceDataReady.v1"
    Given the rule package in force holds R-DEV-03, R-DEV-11, R-DEV-12 and R-DEV-19 and the insurance claim "CLM-SYN-000203" answers for the case

  Scenario: AC1 Run X3 deceased customer end to end (legacy RWB-E7-003 AC1)
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then stops contact, notifies heirs, files the insurance claim and settles the estate position
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 A confirmed death raises X3 the same day, stops all contact and pauses only the stage clock (new, D-RCV-60)
    Given a case in any active state with a confirmed death from the registry or a document
    When the X3 screening consumes "rwb.source-data.AceDataReady.v1" under R-UNI-05 and the deviation is raised through POST /api/recovery/deviation/v1/cases/{caseId}/deviations under R-DEV-01
    Then GET /api/recovery/case/v1/cases/{caseId} answers DEV_FLAGGED on the same business date
    And no outbound contact is read for the case on the DP02 contact points and the case is held for the specialist and Legal
    And GET /api/recovery/case/v1/cases/{caseId}/timers shows the stage clock paused and the prescription clock still running

  Scenario: AC3 The specialist and Legal are the named handlers (new, D-RCV-60)
    Given the case "RW-2027-001203" is in state DEV_FLAGGED with deviation code "X3"
    When the deviation is assigned through PATCH /api/recovery/deviation/v1/deviations/{deviationId} under R-DEV-03
    Then GET /api/recovery/case/v1/cases/{caseId} answers DEV_WITH_OWNER with the specialist named as the handler and Legal named for the estate claim
    And the assignment read on the case names the specialist and Legal and no other handler
    And no approval step is asserted, because R-DEV-03 names none

  Scenario: AC4 Insurance clears the balance and the case closes with its timers stopped (new, D-RCV-60)
    Given the case "RW-2027-001203" is in state DEV_WITH_OWNER with deviation code "X3"
    When the insurance answer in the fixture clears the balance and the settlement is recorded under R-DEV-11
    Then GET /api/recovery/case/v1/cases/{caseId} answers CASE_ENDED
    And GET /api/recovery/case/v1/cases/{caseId}/timers shows the stage clock and the prescription clock stopped
    And GET /api/recovery/document/v1/documents/{documentId} answers the death certificate "DOC-SYN-000203" and the claim evidence "DOC-SYN-000204" with their types and sources
    And "rwb.deviation.DeviationCleared.v1" is published once on "rwb.deviation.events.v1"

  Scenario: AC5 Insurance does not clear and the case returns to the route decision (new, D-RCV-60)
    Given the case "RW-2027-001203" is in state DEV_WITH_OWNER with deviation code "X3"
    When the insurance answer in the fixture does not clear the balance and the estate position is recorded under R-DEV-12
    Then GET /api/recovery/case/v1/cases/{caseId} answers DEV_REROUTE
    And GET /api/recovery/case/v1/cases/{caseId} answers ROUTE_D6 under R-DEV-19
    And the route decision is read as the product of S1 and no route operation is called by this run

  Scenario: AC6 The decision record and the document evidence are published once (new, D-RCV-60)
    Given the X3 raise, the assignment and the branch outcome have run for the case
    When the decision log and the events are read
    Then GET /api/recovery/decision/v1/decision-log?caseId={caseId} holds one entry per action with its rule id and rule version
    And "rwb.decision.DecisionRecorded.v1" is published once on "rwb.decision-record.v1" and confirmed by the central ledger in rwb-decision
    And "rwb.document.DocumentStored.v1" is published once for the death certificate and once for the claim evidence
    And "rwb.source-data.AceDataReady.v1" is published once on "rwb.source-data.events.v1" and consumed once by rwb-deviation
    And a replay of the "AceDataReady" event leaves the case, the timers and the decision log unchanged, because the inbox holds one processed row per consumer

  Scenario: AC7 A forced decision-record failure stops the action (new, D-RCV-60)
    Given the decision record for the case cannot be written
    When the deviation is assigned through PATCH /api/recovery/deviation/v1/deviations/{deviationId}
    Then the answer carries "MSG-P7-003"
    And the case is still read in DEV_FLAGGED with the same handler and the same timers
    And no decision log entry and no "rwb.decision.DecisionRecorded.v1" exist for that action

  Scenario: AC8 A caller without the right is refused (new, D-RCV-60)
    Given a synthetic caller with role "RW-OFF" and no Case record U
    When the caller raises a deviation through POST /api/recovery/deviation/v1/cases/{caseId}/deviations
    Then the answer is 403 with "MSG-P4-002"
    And no deviation is read on the case and no state changes

  Scenario: AC9 Every business rule in section 8 is covered or marked as evaluated elsewhere (new, D-RCV-60)
    Given the rule table of section 8 holds the rules BR1 to BR11
    When the harness run report is read
    Then each rule names an AC of section 7 in its Covered by column or is marked as evaluated in RWB-S8-E7003-APP
    And the harness changes no rule

  Scenario: AC10 A consumed call that fails or does not answer changes no state (new, D-RCV-60)
    Given a case in state DEV_FLAGGED with deviation code "X3"
    When a consumed REST call on the owner's base /api/recovery/<short>/v1 does not answer within 2 s or fails
    Then the answer carries the error condition of the contract and the case is still read in DEV_FLAGGED with the same timers
    And no decision log entry and no "rwb.decision.DecisionRecorded.v1" exists for that action
```

Legacy AC2 (the R-DEV-03 assignment and the DEV_WITH_OWNER move) is asserted here in AC3, and legacy AC4 (the decision log cannot be written) in AC7; the build of those steps stays with RWB-S8-E7003-APP. Legacy AC3 is not asserted as written: it is an X3 scenario tagged with R-DEV-06, and R-DEV-06 belongs to X6 and X7, so the published X3 branch is asserted instead, R-DEV-11 in AC4 and R-DEV-12 in AC5, with no approval step invented (GAP-0467; ASM-0659). The legacy criterion stays with RWB-S8-E7003-APP as a build criterion and is not copied here.

### 8. Business rules

| ID | Rule | Source | Covered by |
|---|---|---|---|
| BR1 | A death confirmed from the registry or a document raises X3, stops all contact and holds the case for the specialist and Legal, on the same day | R-UNI-05, line 409 | AC2; TC-E7-003-02-ITG |
| BR2 | A deviation in any state pauses the stage clock, keeps the prescription clock running and routes the case to the named owner | R-DEV-01, line 383; Temporal design slide 8 | AC2; TC-E7-003-02-ITG |
| BR3 | An X3 deviation is assigned to the specialist, and Legal joins X3 for the estate claim | R-DEV-03, line 385 | AC3; TC-E7-003-02-ITG |
| BR4 | An X3 case whose insurance clears the balance closes on CASE_ENDED | R-DEV-11, line 393 | AC4; TC-E7-003-03-ITG |
| BR5 | An X3 case whose insurance does not clear returns to the route decision against the estate, DEV_REROUTE | R-DEV-12, line 394 | AC5; TC-E7-003-03-ITG |
| BR6 | After the reroute the case reopens the route decision with the segment recomputed and the hard gates re-run, ending in ROUTE_D6 | R-DEV-19, line 401 | AC5; TC-E7-003-03-ITG |
| BR7 | A deviation that sits with its owner past the deviation service level escalates to the team manager and the breach is reported | R-DEV-20, line 402 | None in this harness; evaluated in RWB-S8-E7003-APP |
| BR8 | Every X1 to X7 deviation runs end to end with its own flow, approver, contact rules and return point | REQ-S8-001, BRD Program v4 line 417 | AC1 (X3 only); X1 to X7 flows are built in RWB-S8-E7003-APP |
| BR9 | ACE data is read only through rwb-source-data's data-product contract with its freshness stamp, never from a view and never from another service's schema; the screening consumes `rwb.source-data.AceDataReady.v1` with the deceased and bankrupt flags | DP-01, DP-05; Arch v5 slide 15 S8 IN and slide 42 row 26 | AC2 and AC6; TC-E7-003-02-ITG, TC-E7-003-07-ITG |
| BR10 | The decision record is written by the owning service through the local decision-record library on `rwb.decision-record.v1`, and the central ledger in rwb-decision confirms it | DP-03; ADR-022 | AC6 and AC7; TC-E7-003-07-ITG, TC-E7-003-04-ITG |
| BR11 | Every hop in the run is one REST call on the owner's base `/api/recovery/<short>/v1` with a 2 s timeout | DP-11, DP-13 | AC10; TC-E7-003-09-ITG |

The harness asserts these rules to the extent the Covered by column states and changes none of them; the rules themselves are evaluated in RWB-S8-E7003-APP and the states are held by P3 rwb-case. R-DEV-06 is deliberately absent: the rule table applies it to X6 and X7, and no approval step is asserted for X3 (GAP-0467). Approval and decision record (GAP-1820): an approval that the FSD names on a deviation is a step inside DeviationWorkflow, taken by the role the deviation code assigns (for X3 under R-DEV-03, the specialist, with Legal joining for the estate claim), and the decision-record library writes the entry. No P7 ApprovalWorkflow call is added; that stays an open question. Which assigned role approves, and the operation and payload that submit the approval, are Not specified in the source documents (GAP-1820), so this harness asserts no approval step.

### 9. State transitions

| From | Event | Condition | To | Owner of the change |
|---|---|---|---|---|
| ANY_STATE | CUSTOMER_DECEASED | a death is confirmed from the registry or a document; deviation_code = X3 | DEV_FLAGGED | S8 rwb-deviation, DeviationWorkflow, R-UNI-05 and R-DEV-01; `rwb.deviation.DeviationRaised.v1` |
| DEV_FLAGGED | OWNER_ASSIGNED | deviation_code = X3 | DEV_WITH_OWNER | S8 rwb-deviation, R-DEV-03, the specialist with Legal for the estate claim |
| DEV_WITH_OWNER | INSURANCE_SETTLED | deviation_code = X3 and insurance clears the balance | CASE_ENDED | S8 rwb-deviation, R-DEV-11; P3 stops the stage clock and the prescription clock |
| DEV_WITH_OWNER | ESTATE_CONFIRMED | deviation_code = X3 and insurance does not clear | DEV_REROUTE | S8 rwb-deviation, R-DEV-12 |
| DEV_REROUTE | ROUTE_REOPENED | any | ROUTE_D6 | P3 rwb-case for the case state and S1 rwb-valuation for the D6 route decision, R-DEV-19 |

The states are the deviation states of R-DEV-01, R-DEV-03, R-DEV-11, R-DEV-12 and R-DEV-19, and the case state is read through the P3 contract after every step. The two clocks are read through `GET /api/recovery/case/v1/cases/{caseId}/timers`: the stage clock is paused from DEV_FLAGGED and the prescription clock is never paused, and both stop only when the case closes on CASE_ENDED. The documents that carry the evidence are P5's and are read through its contract. The harness changes no state. Every change in the table is made by the owner: S8 holds the deviation and drives DeviationWorkflow, P3 holds the case state and the timers, P5 holds the documents, S1 produces the D6 route decision and P7 holds the central ledger. A state the harness had set by hand would prove nothing, so the report names the owner and the operation behind every value it asserts.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-SPECIAL, hardship and vulnerability specialist | Is the named handler of X3 under R-DEV-03; holds Case record U; is the role the journey is written for |
| RW-LITOFF, litigation officer | Is the Legal handler who joins X3 for the estate claim under R-DEV-03; holds Case record U |
| RW-CASEOWN, case owner | Owns the case after the reroute and holds Case record U; the team manager is the escalation point of R-DEV-20 |
| RW-OFF, RW-TRIBE, RW-PLATADM | Read only where their rights allow; RW-OFF is the refused caller of AC8 |
| QA lead | Owns the harness configuration, the fixtures, the branch answers, the report shape and the pass or fail gate |
| Integration lead | Owns the harness code, the stub set and the swap from a stub to the real service |
| The owning services' identities | S8 runs DeviationWorkflow and writes the decision record, P3 holds the case and the timers, P1 answers DP02 and the freshness read, P5 holds the documents, P7 holds the ledger and P4 answers the session; they make every change the harness asserts |
| No delegation of authority level applies | The harness takes no business decision and asserts no approval, because the published X3 branch names none; authorisation is answered by rwb-access and the DoA is P4's |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 to DF-CAS-023 | recovery_case | case_no, status, stage_code, primary_person_key | Read through the rwb-case contract |
| DF-CAS-036 to DF-CAS-045 | deviation | deviation_code, raised_at, raised_by, paused_state, handler | Written through the rwb-deviation raise and patch, read back through the case and the timers |
| DF-WRK-009 to DF-WRK-016 | assignment | assignee_user_id, assigned_at, ended_at | Read through the rwb-case contract |
| DF-WRK-027 to DF-WRK-036 | timer | timer_type, started_at, expires_at, paused_at | Read through the rwb-case timers contract |
| DF-ACE-055 to DF-ACE-074 | v_ace_customer, DP02 Customer and party | person_key, cif_no, date_of_birth, customer_status, deceased flag | Read through the rwb-source-data DP02 contract with its freshness stamp, never the view |
| DF-DOC-001 to DF-DOC-011 | document, DP10 Documents and extracted fields | document_type, source, storage_ref, person_key | Read through the rwb-document contract |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | decision_code, rule_id, rule_version | Read through the rwb-decision contract |

Field IDs are those in the Logical Data Model and Data Dictionary v9. The ACE side is DP02 Customer and party behind P1's contract: the legacy `v_ace_customer` is not read by the harness, and no schema is named in it. The document side is DP10 Documents and extracted fields behind P5's contract. The case, the deviation, the assignment and the timers belong to P3 and S8, and the decision log belongs to P7; the harness reads them only through those contracts and never from a schema. The harness owns no table and writes no row. The two writes it makes are the owner's published operations of §12.2, taken with one Idempotency-Key each.

### 12. Contract

#### 12.1 REST operations provided

None. The harness is a test runner and provides no REST operation.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| POST | `/api/recovery/deviation/v1/cases/{caseId}/deviations` | S8 rwb-deviation | Raises the X3 deviation and starts DeviationWorkflow, with one Idempotency-Key (AC1, AC2, AC6, AC8) |
| PATCH | `/api/recovery/deviation/v1/deviations/{deviationId}` | S8 rwb-deviation | The assignment to the specialist and Legal, the branch outcome and the forced failure, with one Idempotency-Key (AC3, AC4, AC5, AC7) |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The case state after the flag, the assignment, the close and the reroute, and the handler (AC1 to AC5, AC7) |
| GET | `/api/recovery/case/v1/cases/{caseId}/timers` | P3 rwb-case | The stage clock, the prescription clock and their stop on the close (AC2, AC4, AC5, AC7) |
| GET | `/api/recovery/source-data/v1/data-products/DP02/records?caseId={caseId}` | P1 rwb-source-data | The deceased flag, the party and the contact points of the case, through the contract and not the view (AC2) |
| GET | `/api/recovery/source-data/v1/data-products/freshness?product=DP02` | P1 rwb-source-data | The business date and the load time behind the DP02 read (AC2) |
| GET | `/api/recovery/document/v1/cases/{caseId}/documents` | P5 rwb-document | The death certificate and the claim evidence on the case (AC1, AC4) |
| GET | `/api/recovery/document/v1/documents/{documentId}` | P5 rwb-document | The metadata and extracted fields of the death certificate and the claim evidence (AC1, AC4) |
| GET | `/api/recovery/decision/v1/decision-log?caseId={caseId}` | P7 rwb-decision | The decision record of the flag, the assignment and the branch outcome, with the rule version and the ledger confirmation (AC1, AC6, AC7) |
| GET | `/api/recovery/access/v1/me/session` | P4 rwb-access | The caller's roles and rights before a write (AC8) |

Every call is one hop on the owner's base `/api/recovery/<short>/v1` with a 2 s budget (DP-11, DP-13). No operation is invented in this story: each path is the owner's published operation in the Ownership Map, and where a screen would compose them the path would be the gateway-bff composite route (DP-19).

The map publishes no `GET /deviations` and no `POST /deviations/{id}/clear` for S8, and this story does not pretend otherwise. The deviation is therefore asserted through three published reads — the case read for the state and the handler, the timers read for the two clocks, and the decision log for the record — plus the `rwb.deviation.DeviationRaised.v1` and `rwb.deviation.DeviationCleared.v1` publications. The two writes above are the only deviation operations the run uses, and both are the map's own.

#### 12.3 Events published

None. The harness publishes no Kafka event; it writes its report to the wave record.

#### 12.4 Events consumed

| Event | Topic | Producer | Use in the run |
|---|---|---|---|
| `rwb.source-data.AceDataReady.v1` | `rwb.source-data.events.v1` | P1 rwb-source-data | Starts the X3 screening with the deceased flag, counted once and consumed once by rwb-deviation (AC2, AC6) |
| `rwb.deviation.DeviationRaised.v1` | `rwb.deviation.events.v1` | S8 rwb-deviation | Counts one publication after the X3 flag and, with the replay, proves one processed row per consumer (AC2, AC6) |
| `rwb.deviation.DeviationCleared.v1` | `rwb.deviation.events.v1` | S8 rwb-deviation | Counts one publication when the deviation clears on the close or on the reroute (AC4, AC5) |
| `rwb.case.CaseStateChanged.v1` | `rwb.case.events.v1` | P3 rwb-case | Proves the states observed are the states published for the case (AC2 to AC5) |
| `rwb.document.DocumentStored.v1` | `rwb.document.events.v1` | P5 rwb-document | Counts one publication for the death certificate and one for the claim evidence (AC4, AC6) |
| `rwb.decision.DecisionRecorded.v1` | `rwb.decision-record.v1` | S8 rwb-deviation through the local decision-record library (DP-03) | Proves the record was published once with its rule version and confirmed by the central ledger (AC6, AC7) |

The harness subscribes to the four topics under one consumer group of its own, counts publications and replays `AceDataReady` and `DeviationRaised` once each. The consumer effect it reads is the case through the rwb-case operation of §12.2; the inbox row counts of the other consumers are read from the consumer evidence in the run fixture, because they expose no operation in this story.

#### 12.5 Workflows and activities

None added. The harness exercises DeviationWorkflow, S8's child workflow on the task queue `rwb-deviation` in the `rwb-recovery` namespace, started through the deviation raise and continued through the patch: it is the workflow that carries the X3 route, the pause of the stage clock, the contact stop and the branch on the insurance answer. It observes CaseWorkflow on `rwb-case`, the parent that receives the deviation through the case router as a signal and pauses and resumes the stage clock for the case. Both are stated here as observed and not built here; no workflow, activity or Schedule is created, changed or owned by this story. The D6 route decision is S1's product and is only read as the case state ROUTE_D6.

#### 12.6 Schedules

None added. The deceased flag arrives on the overnight `AceDataReady` event and the branch arrives with the insurance answer, so nothing in the journey is on a cron: the harness starts the run from the screening event and holds the insurance and estate answers in its own fixture instead of waiting on a schedule. The timer check of JOB-05 is retired in favour of durable timers inside the workflows (Arch v5 slide 44), which is why the two clocks are read through the timers operation and not through a job.

#### 12.7 Tables owned

None. The harness owns no schema and no table (DP-01); deviation is S8's, recovery_case, assignment and timer are P3's, document is P5's, decision_log_entry is P7's, and the party side belongs to DP02 behind P1's contract.

#### 12.8 Contract fakes

| Fake | Contract | Stubbed answer in the run |
|---|---|---|
| Stub for rwb-deviation | `POST /cases/{caseId}/deviations`, `PATCH /deviations/{deviationId}` | Accepts the raise once per Idempotency-Key and answers MSG-S8-001 with deviation `DEV-SYN-000203` and the specialist as the handler; the patch accepts the assignment and the branch outcome and keeps the same deviationId |
| Stub for rwb-case | `GET /cases/{caseId}`, `GET /cases/{caseId}/timers` | Case `RW-2027-001203` in DEV_FLAGGED, then DEV_WITH_OWNER with the specialist and Legal, then CASE_ENDED in branch A or DEV_REROUTE and ROUTE_D6 in branch B; the stage clock paused, the prescription clock running and both stopped on the close |
| Stub for rwb-source-data | DP02 records, freshness | The deceased flag and the party of the case, no live outbound contact point, and business date `2027-05-14` with a load time |
| Stub for rwb-document | `GET /cases/{caseId}/documents`, `GET /documents/{documentId}` | The death certificate `DOC-SYN-000203` and the claim evidence `DOC-SYN-000204`, each with its type, source and extracted fields |
| Stub for rwb-decision | `GET /decision-log?caseId={caseId}` | One entry per action with its rule id and rule version, and the central ledger confirmation |
| Stub for rwb-access | `GET /me/session` | Allows RW-SPECIAL with Case record U; refuses RW-OFF with 403 and MSG-P4-002 |
| Insurer and estate fixture | The insurance answer and the estate position | The claim `CLM-SYN-000203` clears the balance in branch A and does not clear it in branch B, with the estate position and the heirs to notify held at the point where the real insurer answer would arrive |

Each stub is generated from the published contract and its version is pinned in the run report, so a contract change shows up as a run failure and not as a silent pass. The harness environment and base hosts, the fixture layout, the synthetic keys, the stub answer shapes, the insurer and estate answer shapes, the heir-notification content, the evidence format and retention, and the pass or fail gate are Not specified in the source documents (GAP-0468; ASM-0660).

#### 12.9 Call-type summary

| Call type | In this story |
|---|---|
| REST | 0 provided, 10 consumed, one hop each on `/api/recovery/<short>/v1` with a 2 s budget (DP-11, DP-13) |
| Kafka | None published; six consumed, `rwb.source-data.AceDataReady.v1`, `rwb.deviation.DeviationRaised.v1`, `rwb.deviation.DeviationCleared.v1`, `rwb.case.CaseStateChanged.v1`, `rwb.document.DocumentStored.v1` and `rwb.decision.DecisionRecorded.v1`, counted and two of them replayed once |
| Temporal | None added; DeviationWorkflow on `rwb-deviation` exercised from the raise, with CaseWorkflow on `rwb-case` observed as the parent that pauses and resumes the stage clock |
| File | None. The insurer and estate answers are held in the run fixture; no file or claim-check is transferred by this story |

### 13. Solution plan

**Package.** Folder `itg/recovery`, package `th.co.scb.ace.workbench.recovery.itg`, test scope only; not part of any deployed service.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The H dependencies DP-03 and DP-19 add, RWB-PLT-E1027-CON and RWB-PLT-N001-CON, are platform stories delivered by the platform wave and are not repeated in the metadata H field of this story, which stays None; DP-05 adds none in the pattern table, but this story takes the stricter reading of it and reads the ACE side only through P1's DP02 contract, never through a `v_ace_*` view; DP-13 adds nothing. The one blocking dependency is the I story RWB-S8-E7003-APP, which replaces its stub; until it is live the run uses the stub, and a stub pass is reported as a stub pass.

**Harness components**

| Component | Type | Responsibility |
|---|---|---|
| JourneyRunner | Job | Runs the eight owned criteria in order for a case and a branch, and holds the run lock |
| DeviationDriver | Service | Raises the X3 deviation and patches the assignment and the branch outcome, once per Idempotency-Key |
| ScreeningProbe | Service | Reads DP02 with the freshness stamp, asserts the deceased flag, the party and the absent outbound contact, and watches `AceDataReady` reach rwb-deviation |
| OwnerProbe | Service | Reads the case after the assignment and asserts the specialist and Legal are the named handlers |
| ClockProbe | Service | Reads the timers and asserts the stage clock paused, the prescription clock running and both stopped on the close |
| DocumentProbe | Service | Reads the case document list and each document, and asserts the death certificate and the claim evidence with their types and extracted fields |
| BranchDriver | Service | Holds the insurance answer and the estate position, and drives the close or the return without inventing an approval |
| DecisionProbe | Service | Reads the decision log and asserts one record per action, with its rule version and the ledger confirmation |
| EventObserver | Service | Subscribes to the four topics of §12.4, counts publications and replays `AceDataReady` and `DeviationRaised` once |
| StubSet | Fake | The six stubs and the insurer and estate fixture of §12.8, generated from the published contracts with the version pinned |
| EvidenceReport | Service | Writes one report per case and branch keyed by story, case_no and branch, and holds the pass or fail gate |

**Environment and test data.** SIT, against the stubs from Day 1 and the real services as RWB-S8-E7003-APP lands, on synthetic case `RW-2027-001203`, deviation `DEV-SYN-000203`, documents `DOC-SYN-000203` and `DOC-SYN-000204`, claim `CLM-SYN-000203` and business date `2027-05-14`. The harness seeds nothing by hand and never writes a schema row. The environment and base hosts, the fixture layout, the synthetic keys, the insurer and estate answer shapes, the heir-notification content, the evidence format and retention, and the pass or fail gate are Not specified in the source documents (GAP-0468; ASM-0660).

**Build steps**

1. Generate the six stubs and the insurer and estate fixture from the published contracts and pin each contract version in the run report; fail the run on a mismatch (X1).
2. Build the ScreeningProbe for AC2: DP02 through the contract with its freshness stamp, the deceased flag, no live outbound contact, and one `AceDataReady` consumed by rwb-deviation (X2, X3).
3. Build the DeviationDriver for the raise and prove it is accepted once per Idempotency-Key and answers MSG-S8-001 with the deviation and the handler (AC1, AC2).
4. Add AC2 on the case read and the timers read: DEV_FLAGGED on the same business date, the stage clock paused and the prescription clock still running.
5. Add AC3 on the assignment patch and the case read: DEV_WITH_OWNER with the specialist and Legal named, and no approval step (X4).
6. Add AC4 on branch A: the close on CASE_ENDED with both clocks stopped, and the death certificate and claim evidence read through the P5 contract (X5).
7. Add AC5 on branch B: DEV_REROUTE under R-DEV-12 and the case read in ROUTE_D6 under R-DEV-19, with no route operation called (X6).
8. Add the EventObserver for AC6: one `AceDataReady`, one `DeviationRaised`, one `DeviationCleared` per branch, one `CaseStateChanged` per state and one `DocumentStored` per document, with a replay that changes nothing (X7).
9. Add the DecisionProbe for AC6 and AC7: one entry per action with its rule version, the ledger confirmation, then a forced write failure that leaves the case and the timers untouched and answers MSG-P7-003 (X8).
10. Add the access path for AC8 through the session read and the raise operation, and assert 403 with MSG-P4-002 and no state change (X9).
11. Add the EvidenceReport and the gate, and swap a stub for the real owner as RWB-S8-E7003-APP lands.

**Feature switch.** None. The harness has no production flag and runs in the test environment only.

**Done when.** The tests of section 16 pass against the fakes and again against RWB-S8-E7003-APP when it lands, and the wave entry check holds a run report keyed by story, case_no and branch.

### 14. Validation and messages

| ID | Type | Message |
|---|---|---|
| MSG-S8-001 | Information | {deviation} was raised. The case is with {handler}. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The harness asserts the message ID and the substituted values on the answer it reads, and owns no message text. MSG-S8-001 is asserted with the deviation code and the specialist and Legal as the handler when the X3 flag is raised, MSG-GEN-001 with the missing field when a write is made short of a required parameter, MSG-P4-002 with the refused raise for a caller without Case record U, and MSG-P7-003 when the decision record cannot be written and nothing changes.

### 15. Screens and states

The legacy story's screens are SCR-08 Deviation queue and SCR-06 Raise deviation, and neither is built or rendered here: the harness calls the two operations behind them and reads the states through the owners. Both screens carry all four states in the table below, Empty, Loading, Error and No access, and a state the specification does not publish is recorded as Not specified in the source documents (CG-ALL-1161, CG-ALL-1162) so the wave entry check reads a recorded state and not a blank. What the wave entry check looks at instead is the run report, whose environment, layout and retention are Not specified in the source documents (GAP-0468; ASM-0660).

| State | Read through | What the run asserts |
|---|---|---|
| DEV_FLAGGED | rwb-case case read, timers read and DP02 read | The X3 flag is raised on the same business date, no outbound contact is read, and the stage clock is paused while the prescription clock runs |
| DEV_WITH_OWNER | rwb-case case read and timers read | The specialist is the handler and Legal joins for the estate claim, the clocks hold, and the decision record exists with its rule version |
| CASE_ENDED | rwb-case case read, timers read and rwb-document reads | Branch A: the insurance cleared the balance, the case closed, both clocks stopped, and the death certificate and claim evidence are on the case |
| DEV_REROUTE | rwb-case case read | Branch B: the insurance did not clear and the case returns to the route decision against the estate |
| ROUTE_D6 | rwb-case case read | Branch B: the route decision reopened under R-DEV-19, and the deviation cleared |
| A refused raise | rwb-access session read and the raise answer | 403 with MSG-P4-002 and no state change |
| Empty (SCR-06 Raise deviation) | Not specified in the source documents (CG-ALL-1161) | Not specified in the source documents (CG-ALL-1161) |
| Loading (SCR-06 Raise deviation) | Not specified in the source documents (CG-ALL-1161) | Not specified in the source documents (CG-ALL-1161) |
| Error (SCR-06 Raise deviation) | Not specified in the source documents (CG-ALL-1161) | Not specified in the source documents (CG-ALL-1161) |
| No access (SCR-06 Raise deviation) | Screen Specifications v1, SCR-06: access Case record, checked on every request | MSG-P4-002 "You cannot {action} here. Your role does not include it."; the screen is not rendered by this harness |
| Empty (SCR-08 Deviation queue) | Not specified in the source documents (CG-ALL-1162) | Not specified in the source documents (CG-ALL-1162) |
| Loading (SCR-08 Deviation queue) | Screen Specifications v1, SCR-08: states Loading and list | The Loading state is named there and its content is Not specified in the source documents (CG-ALL-1162); the screen is not rendered by this harness |
| Error (SCR-08 Deviation queue) | Not specified in the source documents (CG-ALL-1162) | Not specified in the source documents (CG-ALL-1162) |
| No access (SCR-08 Deviation queue) | Screen Specifications v1, SCR-08: access Case record, checked on every request | MSG-P4-002 "You cannot {action} here. Your role does not include it."; the screen is not rendered by this harness |

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E7-003-01-ITG | AC1 (legacy); ITG AC1 | End to end | One case with an X3 flag, the raise, the assignment and one branch live |
| TC-E7-003-02-ITG | AC2 (legacy, rule R-DEV-03); ITG AC3 | Integration | A case in DEV_FLAGGED with deviation code X3 and the specialist and Legal as the handlers |
| TC-E7-003-03-ITG | AC3 (legacy, rule R-DEV-06 — mis-cited, see GAP-0467); ITG AC4 and AC5 assert R-DEV-11 and R-DEV-12 instead | Integration | A case in DEV_WITH_OWNER with the insurance answer clearing in one run and not clearing in the other |
| TC-E7-003-04-ITG | AC4 (legacy); ITG AC7 | Integration | A forced decision-record failure on the assignment |
| TC-E7-003-05-ITG | Access; ITG AC8 | Component | RW-OFF caller without Case record U |
| TC-E7-003-06-ITG | Principle 5; ITG AC7 | Integration | A forced decision-record failure at the point of the state change |
| TC-E7-003-07-ITG | ITG AC6 (no legacy test of its own) | End to end | The X3 run of TC-E7-003-01-ITG, counting the publications and replaying AceDataReady and DeviationRaised once each |
| TC-E7-003-08-ITG | ITG AC9 (new, D-RCV-60) | Component | The section 8 rule table and the harness run report |
| TC-E7-003-09-ITG | ITG AC10 (new, D-RCV-60) | Integration | A case in DEV_FLAGGED with a consumed call on the stub held beyond 2 s |

The Covers column names the legacy AC the copy derives from and the ITG AC it asserts, and the full legacy test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx under the same legacy test case ID. Legacy AC2 and AC4 stay with RWB-S8-E7003-APP as build criteria; the -ITG copies here assert the same behaviour across the service boundary. Legacy AC3 is copied as the -03 run but its rule is not asserted as cited: that run proves R-DEV-11 and R-DEV-12, and no approval step is invented. ITG AC2 is asserted at the raise step of TC-E7-003-02-ITG and ITG AC6 in the end-to-end run of TC-E7-003-01-ITG and in TC-E7-003-07-ITG, because the legacy test set has no test of its own for either.

Harness environment, fixtures, insurer and estate answer shapes, heir-notification content, evidence format and the wave entry gate are not published in the source documents (GAP-0468); they are agreed at the wave entry check, and a stub pass is never recorded as a real pass.

### 17. Guardrails

- No business value in code: the synthetic case, deviation, document and claim keys, the business date, the timer names, the two branch answers and the report layout are data.
- No personal data in logs, events or reports: every party key is synthetic, the death certificate is a fixture, and the events carry IDs and facts only.
- ACE data only through the P1 contract: DP02 with its freshness stamp, never a direct `v_ace_*` view read and never another service's schema (DP-01, DP-05).
- One hop and a 2 s budget per call, with a circuit breaker per downstream, so the harness fails where a screen would (DP-11, DP-13).
- No invented operation and no invented approval: only the two deviation writes and the eight reads of §12.2, and the X3 branch is asserted as R-DEV-11 and R-DEV-12 name it.
- A stub pass is never reported as a real pass: the report names the contract version and whether the hop was a stub or the owner.
- The harness never runs against UAT or production, and it never writes a row by hand or sets a state it then asserts.
- A failing criterion is fixed in the owning service or raised as a gap; it is never waived in the script.

### 18. Traceability

| Item | Source | Where it lands |
|---|---|---|
| Legacy story RWB-E7-003 Run X3 deceased customer end to end | Recovery Workbench User Stories Epics 3 to 8 v4, lines 11114 to 11208 | Sections 1, 3, 11, 14 and 19 of this file |
| Legacy AC1, verbatim | The same, lines 11133 to 11137 | Section 7, AC1, marked (legacy RWB-E7-003 AC1) |
| Legacy AC2 and AC4, rule R-DEV-03 and the not-recorded case | The same, lines 11139 to 11143 and 11151 to 11155 | AC3 and AC7 here; the legacy criteria stay with RWB-S8-E7003-APP (section 19) |
| Legacy AC3, an X3 scenario citing R-DEV-06 | The same, lines 11145 to 11149 | The conflict GAP-0467; AC4 and AC5 here assert R-DEV-11 and R-DEV-12 instead, and the legacy criterion stays with RWB-S8-E7003-APP |
| Legacy test cases TC-E7-003-01 to TC-E7-003-06 | The same, lines 11201 to 11206 | Copied as -ITG in section 16 |
| Legacy endpoints, screens, permission check and messages | The same, lines 11168 to 11195 | Sections 12.2, 15 and 14 |
| FEAT-DVF-03 Run X3 deceased customer end to end | Epics 3 to 8 Specification v3, line 126 | Sections 1 and 2 |
| REQ-S8-001, with REQ-S8-004 and REQ-S8-005 as the X6 and X7 siblings | Business Requirements Program v5, lines 417, 420 and 421 | Section 8, BR8 |
| R-DEV-01, R-DEV-03, R-DEV-11, R-DEV-12, R-DEV-19 and R-DEV-20 | Business Rules and Routing Logic v4, lines 383, 385, 393, 394, 401 and 402 | Sections 8 and 9 |
| R-UNI-05 | The same, line 409 | Section 8, BR1; section 9; AC2 |
| R-DEV-06, the rule the legacy AC3 cites and the X3 branch does not use | The same, line 388 | Sections 7, 8 and 16; GAP-0467 |
| The X3 worked example, the contact stop and the two clocks | Temporal and Drools design slide 8, lines 375 to 414; slide 24, lines 1566 to 1661 | Sections 2, 8, 9 and 13 |
| The S8 contract, the deceased and bankrupt flags on `AceDataReady`, and the event rows 06, 07 and 26 | Architecture v5 slides 15 and 25, lines 1049 to 1069, and slides 41 to 44, lines 2906, 2911, 2912 and 2945 | Sections 2, 8, 12.4 and 12.5 |
| DF-CAS-001 to DF-CAS-023, DF-CAS-036 to DF-CAS-045, DF-WRK-009 to DF-WRK-016, DF-WRK-027 to DF-WRK-036, DF-ACE-055 to DF-ACE-074, DF-DOC-001 to DF-DOC-011, DF-DEC-001 to DF-DEC-018 | Logical Data Model and Data Dictionary v9 | Section 11 |
| DP-03, DP-05, DP-13 and DP-19 | Template and Rules v1 §R5.5 | Section 13, pattern application |
| ADR-015, ADR-020 and ADR-022 | Architecture Decision Records v4 | Sections 12.4, 12.2 and 8: outbox and inbox on Kafka, contract-first REST with one hop and 2 s, local decision record plus central ledger |
| DeviationWorkflow, the pause of the stage clock and the parent CaseWorkflow | Architecture v5 slide 25, line 1858; slide 41 and the service catalogue | Sections 2, 9, 12.5 and 13 |

### 19. Out of scope

- RWB-S8-E7003-CON and RWB-S8-E7003-APP: the build of the X3 screening, the contact stop, the assignment, the branch on the insurance answer, the return point and the decision record.
- The insurer and estate handling: the claim filing, the heir notification and the estate position are S8's flow and the insurer's answer; this story holds their answers in a fixture and asserts the state that follows.
- The S8 screening and the other six deviation codes (RWB-S8-E7001-*, RWB-S8-E7002-*, RWB-S8-E7004-* to RWB-S8-E7007-*), and the screening dependency FEAT-DVH-04.
- The document hub build: the death certificate and the claim evidence are read through P5's contract, and no document is uploaded, extracted, versioned or retained by this story.
- The route decision of S1 and its approval on P7: ROUTE_D6 is read through the case, and the route operation is not called by this story.
- SCR-08 Deviation queue and SCR-06 Raise deviation, and every gateway-bff composite route.
- The platform stories and their H dependencies named in section 13, including RWB-PLT-E1027-CON and RWB-PLT-N001-CON.
- The other X codes and their harness stories, and the legacy AC3 rule R-DEV-06, which is not asserted on an X3 case.
- Any production change: no endpoint, table, workflow, activity, schedule, screen, feature flag or configuration in any service.
