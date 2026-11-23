# RWB-ITG-E7007-ITG Run X7 collateral event end to end

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-E7007-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W4 |
| Wave | 4 |
| Business epic | EP07 |
| Release | 31 May 2027 (tentative) |
| Legacy key | RWB-E7-007 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | L-ITG-W4 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | RWB-S8-E7007-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E7-007 as the wave 4 integration proof of the X7 collateral event, driven from the deviation operations on rwb-deviation and observed across rwb-guarantee, rwb-valuation, rwb-asset, rwb-case and rwb-decision; the build of the flow is RWB-S8-E7007-APP and its CON story. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **case owner**, I want **an insurance claim filed and the collateral re-appraised through the owners' own operations, and the case returned to the route decision before the next decision is taken, proved end to end against the real services and observed at every hop**, so that **a collateral event is handled by a named owner with a clock on it, and the case never takes its next decision on an unfiled claim or a stale appraisal**.

This story builds the harness and the evidence, and nothing else. The X7 flow itself — the flag, the routing by code, the return point and the decision record — is built by S8 in RWB-S8-E7007-APP and its CON story. The insurance claim is S3 rwb-guarantee's, the re-appraisal is S1 rwb-valuation's, the asset and its collateral link are S5 rwb-asset's, the case state and its timers are P3 rwb-case's, and the decision log and the central ledger are P7 rwb-decision's. The harness starts the journey on the deviation operations, observes every hop through the owners' published contracts, and writes a run report per case. It builds no production endpoint, no table, no workflow, no activity, no schedule and no screen, and it writes no code in any service.

### 2. Business rationale

A collateral event — collateral stolen, damaged or written off, or the insurance on it lapsed — is the one deviation whose handler cannot settle it alone. The case needs money from an insurer and a fresh value on the security before it may be routed again. That is the failure this story is written against: the deviation is flagged, the case is held with a named owner, and then the next decision runs anyway, on the value the collateral carried before the event and on a claim that was never filed. The route then re-decides against a security that no longer exists in the shape the decision assumed, the treatment it picks is under-secured from the day it is agreed, and the loss that the insurance would have covered is discovered a year later with the claim deadline passed.

The flow has a fixed order and the harness asserts that order. The flag pauses the stage clock and keeps the prescription clock running (R-DEV-01); the case is routed to the named owner by code, the agent works within policy and a person approves the insurance claim (R-DEV-06); the claim is filed in S3 and the collateral is re-appraised through S1; the case then returns to the route decision (R-DEV-12) and the route decision is re-opened at D6 (R-DEV-19). REQ-S8-005 puts the obligation in one line: a collateral event triggers an insurance claim and a re-appraisal before the next decision. REQ-S8-001 puts the second: X7 runs end to end with its own flow, approver, contact rules and return point. This story carries both into evidence rather than restating them.

The money and the security live with three owners, and the harness touches each of them only through its published contract. S3 holds the TCG and insurance claims, S1 holds the valuations and the D6 route decision, S5 holds the asset. A claim is filed and a claim is paid at different times, and the harness proves the difference on the money product rather than assuming it: before a person approves, DP13 shows no money moved for the claim. The decision record is written by S8 through the local decision-record library on `rwb.decision-record.v1` (DP-03) and confirmed by the central ledger in rwb-decision, and the harness reads it back through rwb-decision's contract.

The harness is decoupled the way the services are. Every call is one hop on `/api/recovery/<short>/v1` with a 2 s budget (DP-11, DP-13). ACE collateral and appraisal data is read only through rwb-source-data's data-product contract (DP-05) with its freshness stamp, never from a view and never from another service's schema (DP-01). Where a screen would compose these calls the path is the gateway-bff composite route (DP-19).

### 3. Preconditions

- The published contracts of S8 rwb-deviation (the raise and the transition), S3 rwb-guarantee (the claim and its update), S1 rwb-valuation (the re-appraisal), S5 rwb-asset (the asset read), P3 rwb-case (the case and its timers), P1 rwb-source-data (DP01, DP13 and freshness), P7 rwb-decision (the decision log) and P4 rwb-access (the session) are in the contract registry, and a stub set is generated from each one.
- The data product catalog holds DP01 Account and arrears and DP13 Money and closure, each with one system of record, so the account behind the collateral and the money that the claim would move each have one named owner before a value is asserted (FSD P1 v3, A2.2).
- RWB-S8-E7007-APP owns the X7 flag, the routing by code, the return point and the decision record; until it lands, the deviation fixture of §12.8 stands in for its effect and the story is reported as a stub pass.
- The insurance claim is S3's build and the re-appraisal is S1's build; the harness reads both through their contracts and asserts neither of their internal steps.
- The case, its deviation, its timer and its assignment are P3's and S8's; the fixture holds a case already in DEV_FLAGGED with an open X7 deviation, so this story never asserts how the flag was raised.
- The harness seeds nothing by hand: the case, the collateral, the asset and the business date are held in the fixture as data.
- The harness environment and base hosts, the fixture layout, the synthetic case, asset and collateral keys, the insurance-claim answer shape, the evidence format and retention, and the pass or fail gate: Not specified in the source documents (GAP-0472; ASM-0664).
- No build dependency. Day 1, with the stubs in place from the first run; the one wait is RWB-S8-E7007-APP, which replaces its stub and never blocks the lane.

### 4. Flow

1. Harness: loads the fixture: case `RW-2027-000701` with case_no `RW-2027-000701` in state `DEV_FLAGGED`, holding an open deviation of code `X7` and its assignment, with collateral `COL-SYN-000701` on asset `AST-SYN-000701` and one stage timer. On Day 1 the stub of §12.8 returns the same records.
2. Harness: reads `GET /api/recovery/case/v1/cases/{caseId}` and asserts the case is in `DEV_FLAGGED`, and reads `GET /api/recovery/case/v1/cases/{caseId}/timers` to assert the stage clock is paused while the prescription clock still runs (R-DEV-01).
3. Harness: assigns the owner through `PATCH /api/recovery/deviation/v1/deviations/{deviationId}` with the `OWNER_ASSIGNED` event and one Idempotency-Key, which S8 evaluates as R-DEV-06, and asserts the case moves to `DEV_WITH_OWNER` and stays there.
4. Harness: asserts the person's approval of the insurance claim is recorded, by reading `GET /api/recovery/decision/v1/decision-log?caseId={caseId}` for the R-DEV-06 entry with its rule version, and asserts `MSG-S8-001` on the transition answer names the deviation and the handler the case is with.
5. Harness: files the insurance claim through `POST /api/recovery/guarantee/v1/cases/{caseId}/guarantee-claims` with one Idempotency-Key, then moves it through `PATCH /api/recovery/guarantee/v1/guarantee-claims/{claimId}`, and asserts the claim is filed once with one claim id.
6. Harness: re-appraises the collateral through `POST /api/recovery/valuation/v1/assets/{assetKey}/valuations` with one Idempotency-Key, and asserts S1 records one valuation for the asset and answers with its appraisal reference.
7. Harness: reads `GET /api/recovery/asset/v1/assets/{assetKey}` and asserts the asset still carries the collateral key of the event and now points at the re-appraisal, so the claim and the new value belong to the same security.
8. Harness: reads `GET /api/recovery/source-data/v1/data-products/DP01/records?caseId={caseId}` for the account behind the collateral and its arrears position, then `GET /api/recovery/source-data/v1/data-products/freshness?product=DP01` for the business date and the load time behind that read, so a stale product is never reported as a clean event.
9. Harness: reads `GET /api/recovery/source-data/v1/data-products/DP13/records?caseId={caseId}` before and after the approval and asserts no money moved for the claim until a person approved it.
10. Harness: drives `ESTATE_CONFIRMED`, which S8 evaluates as R-DEV-12, and asserts the case moves to `DEV_REROUTE`; then drives `ROUTE_REOPENED`, which S8 evaluates as R-DEV-19, and asserts the case reaches `ROUTE_D6` before the next decision record exists.
11. Harness: counts one `rwb.deviation.DeviationRaised.v1` on `rwb.deviation.events.v1`, then replays it and asserts the case and the deviation are unchanged, because the inbox holds one processed row per consumer; it counts `rwb.case.CaseStateChanged.v1` against the transitions and reads the consumer effect through the case.
12. Harness: reads the decision log for the whole run and asserts one entry per transition, each with its rule id and rule version, that `rwb.decision-record.DecisionRecorded.v1` was published once per entry on `rwb.decision-record.v1`, and that the central ledger confirmed each record.
13. Harness: holds the decision-record write back and asserts the action is refused with `MSG-P7-003` and nothing changes; then calls `GET /api/recovery/access/v1/me/session` as a synthetic `RW-OFF` caller and asserts the deviation transition answers 403 with `MSG-P4-002` and no state change.
14. Harness: writes one run report per case, keyed by story and case_no, naming the contract version of each hop, whether the hop was a stub or the owner, the claim id, the valuation reference, the state after each transition and the criteria verdicts.

### 5. Exception paths

| ID | Trigger | What the harness asserts | Message | ITG test case |
|---|---|---|---|---|
| X1 | A stub answers a shape the published contract does not allow | The run fails at that hop and the report names the service, the operation and the contract version; no criterion is marked passed | None | TC-E7-007-01-ITG (ITG AC1) |
| X2 | The claim is filed twice, or a second claim id appears for the same event | The run fails on AC3 and the report names both claim ids and the Idempotency-Key; a duplicate claim is a duplicate demand on the insurer | None | TC-E7-007-03-ITG (ITG AC3) |
| X3 | The re-appraisal is recorded but the asset still points at the old value | The run fails on AC3 and the report names the asset, the old appraisal and the new one | None | TC-E7-007-03-ITG (ITG AC3) |
| X4 | The case reaches the route decision before the claim is filed or the re-appraisal is recorded | The run fails on AC3 and the report names the state, the transition and the missing step, against REQ-S8-005 | None | TC-E7-007-03-ITG (ITG AC3) |
| X5 | The decision record is written twice for one transition, or the ledger never confirmed it | The run fails on AC4 and the report names the transition, the two entries and the missing confirmation | MSG-P7-003 | TC-E7-007-04-ITG (ITG AC5) |
| X6 | A forced decision-record failure changes the case anyway | The run fails on AC5 and the report names the attempted transition, the state before it and the state after it | MSG-P7-003 (expected) | TC-E7-007-04-ITG (ITG AC5); TC-E7-007-06-ITG (ITG AC5) |
| X7 | A caller without the Case record U right is allowed the transition | The run fails on AC6 and the report names the caller role, the operation and the answer; a 200 is a failure even when no data changed | MSG-P4-002 (expected, and missing) | TC-E7-007-05-ITG (ITG AC6) |
| X8 | The case sits in a state the flow does not allow, or the timer read disagrees with the state | The run fails at that hop and the report names the state pair and the two reads it compared | None | TC-E7-007-02-ITG (ITG AC2) |

The report text is for the wave entry check and is not part of the message standard. The business messages the run touches are in section 14 and are asserted by ID and by their substituted values.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Runs against the published contracts and the stubs from Day 1; the only wait is RWB-S8-E7007-APP, and its fixture answers until it lands |
| Negotiable | The fixture layout, the synthetic keys, the claim answer shape, the report shape and the gate are configuration agreed at the wave entry check, not business values in code |
| Valuable | The claim is proved filed once, the collateral is proved re-appraised, and the case is proved to reach the route decision after both and not before them |
| Estimable | One runner, one stub set, one claim and valuation fixture, one state probe, one timer read, one event observer and one report |
| Small | Fits in one sprint with its six tests |
| Testable | Each criterion runs against the stubs and again against RWB-S8-E7007-APP as it lands |

### 7. Acceptance criteria

```gherkin
Feature: Run X7 collateral event end to end - wave 4 integration harness

  Background:
    Given the synthetic case "RW-2027-000701" holds an open deviation of code "X7" on collateral "COL-SYN-000701" of asset "AST-SYN-000701"
    Given the case is in state "DEV_FLAGGED" and its stage clock is paused while the prescription clock runs
    Given DP01 and DP13 answer for the case with their freshness stamp and no money has moved for the claim

  Scenario: AC1 Run X7 collateral event end to end (legacy RWB-E7-007 AC1)
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then files the insurance claim, re-appraises the collateral and returns the case to the route decision
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 The X7 flag is raised and a person approves the insurance claim (new, D-RCV-60)
    Given the case "RW-2027-000701" is in state "DEV_FLAGGED" with deviation code "X7"
    When the owner is assigned through PATCH /api/recovery/deviation/v1/deviations/{deviationId} with event "OWNER_ASSIGNED"
    Then the agent handles within policy and a person approves the insurance claim under R-DEV-06
    And the case moves to "DEV_WITH_OWNER" and stays there
    And "MSG-S8-001" names the deviation and the handler the case is with

  Scenario: AC3 The claim is filed and the collateral re-appraised before the next decision (new, D-RCV-60)
    Given the case "RW-2027-000701" is in state "DEV_WITH_OWNER"
    When the insurance claim is filed through POST /api/recovery/guarantee/v1/cases/{caseId}/guarantee-claims and PATCH /api/recovery/guarantee/v1/guarantee-claims/{claimId}
    And the collateral "COL-SYN-000701" is re-appraised through POST /api/recovery/valuation/v1/assets/{assetKey}/valuations
    Then the case returns to the route decision with event "ESTATE_CONFIRMED" under R-DEV-12 and moves to "DEV_REROUTE"
    And "ROUTE_REOPENED" under R-DEV-19 moves it to "ROUTE_D6" before the next decision is recorded
    And the asset still carries the collateral key of the event and points at the one new valuation

  Scenario: AC4 The decision record is written once and confirmed by the ledger (new, D-RCV-60)
    Given the case "RW-2027-000701" completes the X7 flow from "DEV_FLAGGED" to "ROUTE_D6"
    When the flow is replayed from the event "rwb.deviation.DeviationRaised.v1"
    Then one decision record per transition is read through GET /api/recovery/decision/v1/decision-log?caseId={caseId}, each with its rule id and rule version
    And the central ledger in rwb-decision confirms each record
    And "rwb.deviation.DeviationRaised.v1" is published once on "rwb.deviation.events.v1" and consumed once by rwb-case, rwb-comms and rwb-treatment
    And a replay changes nothing, because the inbox holds one processed row per consumer

  Scenario: AC5 A forced decision-record failure stops the action (new, D-RCV-60)
    Given the decision record for case "RW-2027-000701" cannot be written
    When the owner is assigned through PATCH /api/recovery/deviation/v1/deviations/{deviationId}
    Then nothing changes: the case stays in "DEV_FLAGGED" and no entry appears in the decision log
    And the caller sees "MSG-P7-003"

  Scenario: AC6 A caller without the right is refused (new, D-RCV-60)
    Given a synthetic caller with role "RW-OFF" and no Case record U
    When the caller reads the case through GET /api/recovery/case/v1/cases/{caseId}
    Then the answer is 403 with "MSG-P4-002"
    And no state changes
```

Legacy AC2 (rule R-DEV-06) and legacy AC3 (rule R-DEV-12) are copied by RWB-S8-E7007-APP, which owns the build of the flow; the harness asserts the same two transitions as AC2 and AC3. Legacy AC4, the decision log cannot be written, also belongs to RWB-S8-E7007-APP, and this story asserts the same failure at the harness boundary through AC5.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A deviation flag pauses the stage clock, keeps the prescription clock running, and routes the case to the named owner | R-DEV-01 |
| BR2 | The agent handles within policy and a person approves the insurance claim, for deviation codes X6 and X7, and the case moves to DEV_WITH_OWNER | R-DEV-06 |
| BR3 | The outcome is recorded and the same decision resumes, for deviation codes X1 and X7, and the case moves to DEV_RESOLVED | R-DEV-09 |
| BR4 | When the estate is confirmed the case returns to the route decision against the estate, and moves to DEV_REROUTE | R-DEV-12 |
| BR5 | From DEV_REROUTE the segment is recomputed and the hard gates re-run, and the case moves to ROUTE_D6 | R-DEV-19 |
| BR6 | A collateral event triggers an insurance claim and a re-appraisal before the next decision | REQ-S8-005 |
| BR7 | Every call is one hop on the owner's `/api/recovery/<short>/v1` with a 2 s budget, and the harness never chains two calls to answer one assertion | DP-11, DP-13 |
| BR8 | ACE collateral and appraisal data is read only through rwb-source-data's data-product contract with its freshness stamp, never from a view and never from another service's schema | DP-01, DP-05 |
| BR9 | The decision record is written by the owning service through the local decision-record library on `rwb.decision-record.v1` and confirmed by the central ledger before the case moves on | DP-03 |

The harness asserts these rules and changes none of them; the rules themselves are evaluated in RWB-S8-E7007-APP and in the owners of the claim, the valuation and the case.

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| DEV_FLAGGED | OWNER_ASSIGNED | deviation_code in (X6, X7) and a person approves the insurance claim | DEV_WITH_OWNER |
| DEV_WITH_OWNER | ESTATE_CONFIRMED | the claim is filed and the collateral re-appraised, and the estate is confirmed | DEV_REROUTE |
| DEV_REROUTE | ROUTE_REOPENED | the segment is recomputed and the hard gates are re-run | ROUTE_D6 |

The case states are `DEV_FLAGGED`, `DEV_WITH_OWNER`, `DEV_REROUTE` and `ROUTE_D6`, and the event codes `OWNER_ASSIGNED`, `ESTATE_CONFIRMED` and `ROUTE_REOPENED` are the R-DEV-06, R-DEV-12 and R-DEV-19 codes. S8 rwb-deviation holds the deviation and drives DeviationWorkflow, which writes the state change; P3 rwb-case holds the case state and its timers and publishes `rwb.case.CaseStateChanged.v1`; S1 rwb-valuation owns the route decision through RouteDecisionWorkflow, and P3 holds the resulting `ROUTE_D6` case state; P7 rwb-decision holds the central ledger that confirms every decision record on the way. The harness changes no state: every change in the table is made by the owner through the operation of §12.2, and the report names the owner and the operation behind every value it asserts. A state the harness had set by hand would prove nothing.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-CASEOWN, case owner | Owns the deviation and the claim; holds Case record U; is the role the journey is written for |
| RW-RESTRUCT, RW-SPECIAL, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-ENFORCE, RW-SALEOFF | Hold Case record U and may act on the same deviation where the code routes to them; they are the other holders of the right the run asserts |
| RW-OFF, RW-TRIBE, RW-PLATADM | Read only where their rights allow; RW-OFF is the refused caller of AC6 |
| QA lead | Owns the harness configuration, the fixtures, the report shape and the pass or fail gate |
| Integration lead | Owns the harness code, the stub set and the swap from a stub to the real service |
| The owning services' identities | S8 runs DeviationWorkflow and writes the deviation and the decision record, S3 files the claim, S1 records the re-appraisal and owns ROUTE_D6, S5 answers the asset, P3 holds the case state and its timers, P1 answers the data products, P7 holds the ledger and P4 answers the session; they make every change the harness asserts |
| No delegation of authority level applies | The harness takes no business decision; the approval is a person's and its DoA routing is P7's, behind ApprovalWorkflow |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-036 to DF-CAS-045 | deviation | deviation_code, raised_at, raised_by, paused_state, handler_user_id, contact_stop, cleared_at | Read through the rwb-deviation contract |
| DF-CAS-001 to DF-CAS-023 | recovery_case | case_no, status, stage_code | Read through the rwb-case contract |
| DF-WRK-009 to DF-WRK-016 | assignment | assignee_user_id, assigned_at, ended_at | Read through the rwb-case contract |
| DF-WRK-027 to DF-WRK-036 | timer | timer_type, started_at, expires_at, status | Read through the rwb-case contract |
| DF-ACE-091 to DF-ACE-098 | v_ace_collateral | collateral_no, asset_key, account_key, collateral_value, collateral_type, register_date | Read through the S5 asset read, never from the view |
| DF-ACE-187 to DF-ACE-195 | v_ace_valuation | valuation_key, asset_key, appraisal_no, appraisal_type, appraised_value, appraisal_date | Read through the S1 re-appraisal answer, never from the view |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | decision_code, rule_id, rule_version | Read through the rwb-decision contract |
| DF-REF-001 to DF-REF-015 | rule_row | rule_id, rule_version, from_state, event_code | Read through the rwb-decision contract |

Field IDs are those in the Logical Data Model and Data Dictionary v8. The deviation is S8's, the case, the assignment and the timer are P3's, the decision log and the rule rows are P7's, and the ACE side sits behind P1's contract: collateral and appraisal values reach the harness through the S5 asset read and the S1 re-appraisal answer, and the account and money figures through DP01 and DP13 with their freshness stamp. The DP06 product that carries those views is read by S1 and S5, not by the harness. The claim's own fields — claim type, deadline, claimed amount and status — are S3's and are read back through the guarantee-claim answer; they are not a data dependency of this harness and are not restated here. The harness owns no table and writes no row.

### 12. Contract

#### 12.1 REST operations provided

None. The harness is a test runner and provides no REST operation.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| POST | `/api/recovery/deviation/v1/cases/{caseId}/deviations` | S8 rwb-deviation | Raises or re-raises the X7 deviation on the case in the fixture setup (AC1) |
| PATCH | `/api/recovery/deviation/v1/deviations/{deviationId}` | S8 rwb-deviation | The transition: OWNER_ASSIGNED, then ESTATE_CONFIRMED and ROUTE_REOPENED, one Idempotency-Key each (AC2, AC3, AC5) |
| POST | `/api/recovery/guarantee/v1/cases/{caseId}/guarantee-claims` | S3 rwb-guarantee | Files the insurance claim on the collateral event (AC3) |
| PATCH | `/api/recovery/guarantee/v1/guarantee-claims/{claimId}` | S3 rwb-guarantee | Moves the claim to filed and carries its answer and one claim id (AC3) |
| POST | `/api/recovery/valuation/v1/assets/{assetKey}/valuations` | S1 rwb-valuation | Records the re-appraisal of the collateral (AC3) |
| GET | `/api/recovery/asset/v1/assets/{assetKey}` | S5 rwb-asset | The asset, its collateral key and the valuation it now points at (AC3) |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The case state after each transition and the refusal of AC5 and AC6 (AC2, AC3, AC5, AC6) |
| GET | `/api/recovery/case/v1/cases/{caseId}/timers` | P3 rwb-case | The stage clock paused and the prescription clock running (AC2) |
| GET | `/api/recovery/source-data/v1/data-products/DP01/records?caseId={caseId}` | P1 rwb-source-data | The account behind the collateral and its arrears position (AC1, AC3) |
| GET | `/api/recovery/source-data/v1/data-products/DP13/records?caseId={caseId}` | P1 rwb-source-data | No money moves for the claim until a person approves it (AC2, AC3) |
| GET | `/api/recovery/source-data/v1/data-products/freshness?product=DP01` | P1 rwb-source-data | The business date and the load time behind the ACE read (AC3) |
| GET | `/api/recovery/decision/v1/decision-log?caseId={caseId}` | P7 rwb-decision | One entry per transition, with its rule id and rule version, and the ledger confirmation (AC1, AC2, AC4, AC5) |
| GET | `/api/recovery/access/v1/me/session` | P4 rwb-access | The caller's roles and rights before a read (AC6) |

Every call is one hop on the owner's base `/api/recovery/<short>/v1` with a 2 s budget (DP-11, DP-13). No operation is invented in this story: each path is the owner's published operation, and where a screen would compose them the path would be the gateway-bff composite route (DP-19). S8's contract carries the raise and the transition only; Arch v5 slide 15 also shows `GET /deviations` and `POST /deviations/{id}/clear`, and neither is a published operation in the Ownership Map, so there is no read of a single deviation and no clear operation here. The harness therefore asserts the effect of every transition through the case, its timers and the decision log, never by reading the deviation back. The claim, the valuation and the asset each have their own owner, and this story calls each one directly rather than composing them.

#### 12.3 Events published

None. The harness publishes no Kafka event; it writes its report to the wave record.

#### 12.4 Events consumed

| Event | Topic | Producer | Use in the run |
|---|---|---|---|
| `rwb.deviation.DeviationRaised.v1` | `rwb.deviation.events.v1` | S8 rwb-deviation | Counts one publication for the X7 event and, with the replay, proves one processed row per consumer (AC4) |
| `rwb.deviation.DeviationCleared.v1` | `rwb.deviation.events.v1` | S8 rwb-deviation | Counts the publication where the case leaves the deviation and asserts no second one arrives for the same event (AC4) |
| `rwb.case.CaseStateChanged.v1` | `rwb.case.events.v1` | P3 rwb-case | Counts one publication per transition of §9 and names the state pair the harness then reads on the case (AC2, AC3, AC4) |
| `rwb.decision-record.DecisionRecorded.v1` | `rwb.decision-record.v1` | S8 rwb-deviation through the local decision-record library (DP-03) | Proves the record of each transition was published once and confirmed by the central ledger (AC4, AC5) |

The harness subscribes to the three topics under one consumer group of its own, counts publications and replays each event once. The consumer effect it reads is the case through the rwb-case operation of §12.2; the inbox row counts of rwb-comms and rwb-treatment come from the consumer evidence in the run fixture, because neither consumer exposes an operation in this story.

#### 12.5 Workflows and activities

None added. The harness exercises DeviationWorkflow, S8's child workflow on the task queue `rwb-deviation` in the `rwb-recovery` namespace, which can start at any time and pauses the stage clock; it observes GuaranteeClaimWorkflow on `rwb-guarantee`, which files the claim; and it observes CaseWorkflow on `rwb-case`, which is the parent from entry to closure and receives the deviation events through the case router as signals. They are stated here as observed and not built here; no workflow, activity or Schedule is created, changed or owned by this story.

#### 12.6 Schedules

None added. The collateral event starts from the deviation flag and never from a clock, and the monthly re-appraisal schedule belongs to S5 rwb-asset (JOB-19), so the harness sets no cron, overlap policy or catch-up window.

#### 12.7 Tables owned

None. The harness owns no schema and no table (DP-01); deviation is S8's, recovery_case, assignment and timer are P3's, decision_log_entry and rule_row are P7's, the guarantee claim is S3's, the valuation is S1's, the asset is S5's, and the ACE side belongs to the views behind P1's contract.

#### 12.8 Contract fakes

| Fake | Contract | Stubbed answer in the run |
|---|---|---|
| Stub for rwb-deviation | `POST /cases/{caseId}/deviations`, `PATCH /deviations/{deviationId}` | Accepts the raise once per Idempotency-Key, answers the transition with `MSG-S8-001` and the handler, and returns the same transition once when the same key is replayed |
| Stub for rwb-guarantee | `POST /cases/{caseId}/guarantee-claims`, `PATCH /guarantee-claims/{claimId}` | One claim for the case with one claim id, moving from preparing to filed, and the same claim on a replay |
| Stub for rwb-valuation | `POST /assets/{assetKey}/valuations` | One valuation for `AST-SYN-000701` with its appraisal reference and date, and no second valuation on a replay |
| Stub for rwb-asset | `GET /assets/{assetKey}` | Asset `AST-SYN-000701` with collateral `COL-SYN-000701` and the new valuation reference |
| Stub for rwb-case | `GET /cases/{caseId}`, `GET /cases/{caseId}/timers` | Case `RW-2027-000701` with one state per transition, and a stage timer paused with a prescription timer running |
| Stub for rwb-source-data | DP01 records, DP13 records, freshness | The account behind the collateral with its arrears position, no money moved for the claim until the approval, and business date with a load time |
| Stub for rwb-decision | `GET /decision-log?caseId={caseId}` | One entry per transition, each with its rule id and rule version, and the ledger confirmation |
| Stub for rwb-access | `GET /me/session` | Allows RW-CASEOWN with Case record U; refuses RW-OFF with 403 and MSG-P4-002 |

Each stub is generated from the published contract and its version is pinned in the run report, so a contract change shows up as a run failure and not as a silent pass. The harness environment and base hosts, the fixture layout, the synthetic case, asset and collateral keys, the insurance-claim answer shape, the evidence format and retention, and the pass or fail gate are Not specified in the source documents (GAP-0472; ASM-0664).

#### 12.9 Call-type summary

| Call type | In this story |
|---|---|
| REST | 0 provided, 13 consumed, one hop each on `/api/recovery/<short>/v1` with a 2 s budget (DP-11, DP-13) |
| Kafka | None published; four consumed, `rwb.deviation.DeviationRaised.v1`, `rwb.deviation.DeviationCleared.v1`, `rwb.case.CaseStateChanged.v1` and `rwb.decision-record.DecisionRecorded.v1`, counted and replayed once |
| Temporal | None added; DeviationWorkflow on `rwb-deviation` driven from the deviation operations, GuaranteeClaimWorkflow on `rwb-guarantee` and CaseWorkflow on `rwb-case` observed |
| File | None |

### 13. Solution plan

**Package.** Folder `itg/recovery`, package `th.co.scb.ace.workbench.recovery.itg`, test scope only; not part of any deployed service.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The H dependencies DP-03 and DP-19 add, RWB-PLT-E1027-CON and RWB-PLT-N001-CON, are platform stories delivered by the platform wave and are not repeated in the metadata H field of this story, which stays None. The only blocking dependency is the I story RWB-S8-E7007-APP, which replaces its stub; until it is live the run uses the stub, and a stub pass is reported as a stub pass. DP-05 and DP-13 add no dependency: the data products and the per-service base are already in the owners' contracts.

**Harness components**

| Component | Type | Responsibility |
|---|---|---|
| JourneyRunner | Job | Runs the six owned criteria in order for a case and holds the run lock |
| DeviationDriver | Service | Raises and transitions the deviation once per Idempotency-Key and reads the case and its timers before and after each step |
| ClaimDriver | Service | Files the insurance claim and moves it to filed, and asserts one claim id for the event |
| ReappraisalDriver | Service | Records the re-appraisal through S1 and reads the asset through S5, so the claim and the new value belong to the same security |
| AceReadBack | Service | Reads DP01 and DP13 with the freshness stamp, and names any figure that is stale or any money that moved early |
| EventObserver | Service | Subscribes to `rwb.deviation.events.v1`, `rwb.case.events.v1` and `rwb.decision-record.v1`, counts publications and replays each event once |
| LedgerConfirm | Service | Reads the decision log and asserts one entry per transition with its rule version, and the ledger confirmation |
| StubSet | Fake | The eight stubs of §12.8, generated from the published contracts with the version pinned |
| EvidenceReport | Service | Writes one report per case keyed by story and case_no, and holds the pass or fail gate |

**Environment and test data.** SIT, against the stubs from Day 1 and the real services as RWB-S8-E7007-APP lands, on the synthetic case `RW-2027-000701`, collateral `COL-SYN-000701`, asset `AST-SYN-000701` and one business date. The harness seeds nothing by hand and never writes a schema row. The harness environment and base hosts, the fixture layout, the synthetic case, asset and collateral keys, the insurance-claim answer shape, the evidence format and retention, and the pass or fail gate are Not specified in the source documents (GAP-0472; ASM-0664).

**Build steps**

1. Generate the eight stubs from the published contracts and pin each contract version in the run report; fail the run on a mismatch (X1).
2. Build the DeviationDriver and prove the transition is accepted once per Idempotency-Key and the case state moves from DEV_FLAGGED to DEV_WITH_OWNER (AC2).
3. Add the timer read to AC2 and prove the stage clock is paused while the prescription clock runs, and that the two reads agree with the state (X8).
4. Build the ClaimDriver for AC3: one claim for the event, one claim id, and a replay that returns the same claim (X2).
5. Build the ReappraisalDriver for AC3: one valuation for the asset and an asset read that carries the collateral key and the new valuation (X3).
6. Add the AceReadBack for AC3: DP01 and DP13 with the freshness stamp, and no money moved for the claim before the approval.
7. Drive ESTATE_CONFIRMED and ROUTE_REOPENED and assert DEV_REROUTE and then ROUTE_D6, and that no next decision record exists when the case reaches ROUTE_D6 (AC3, X4).
8. Add the EventObserver for AC4: one DeviationRaised, one CaseStateChanged per transition, one DecisionRecorded per entry, and a replay that changes nothing because the inbox holds one row per consumer.
9. Add the forced decision-record failure for AC5 and the session and case path for AC6, then the EvidenceReport and the gate, and swap a stub for the real owner as RWB-S8-E7007-APP lands (X5, X6, X7).

**Feature switch.** None. The harness has no production flag and runs in the test environment only.

**Done when.** The tests of section 16 pass against the fakes and again against RWB-S8-E7007-APP when it lands, and the wave entry check holds a run report keyed by story and case_no.

### 14. Validation and messages

| ID | Type | Message |
|---|---|---|
| MSG-S8-001 | Information | {deviation} was raised. The case is with {handler}. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The harness asserts the message ID and the substituted values on the answer it reads, and owns no message text. MSG-S8-001 is asserted with the deviation code and the handler on the assignment of AC2, MSG-GEN-001 with the missing field when a read is made short of a required parameter, MSG-P4-002 with the refused action on the case read of AC6, and MSG-P7-003 when the decision record cannot be written and nothing changes.

### 15. Screens and states

The legacy story names SCR-08 Deviation queue and SCR-06 Raise deviation, and the harness renders neither: it observes the owners' operations and writes a report. The states are read through those operations, not rendered.

| State | Read through | What the run asserts |
|---|---|---|
| DEV_FLAGGED | rwb-case case read and rwb-case timers | The X7 deviation is open, the stage clock is paused and the prescription clock runs |
| DEV_WITH_OWNER | rwb-case case read and the decision log | A person approved the insurance claim and the case is with the named handler |
| DEV_REROUTE | rwb-case case read | The claim is filed and the collateral re-appraised, and the case has returned to the route decision |
| ROUTE_D6 | rwb-case case read and the decision log | The segment is recomputed and the hard gates re-run, and no next decision record exists yet |

SCR-08 and SCR-06 belong to the S8 stories and neither is built or read here. What the wave entry check looks at instead is the run report, whose environment, layout and retention are Not specified in the source documents (GAP-0472; ASM-0664).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E7-007-01-ITG | AC1 (legacy); ITG AC1 | End to end | One case in DEV_FLAGGED with an X7 deviation, the claim and the re-appraisal steps live |
| TC-E7-007-02-ITG | AC2 (legacy rule R-DEV-06); ITG AC2 | Integration | A case in DEV_FLAGGED with a named owner, the approval recorded and the timer pair |
| TC-E7-007-03-ITG | AC3 (legacy rule R-DEV-12); ITG AC3 | Integration | A case in DEV_WITH_OWNER, one claim, one valuation and the return to ROUTE_D6 |
| TC-E7-007-04-ITG | AC4 (legacy, not recorded); ITG AC5 | Integration | A forced decision-record failure on the assignment transition |
| TC-E7-007-05-ITG | Access; ITG AC6 | Component | RW-OFF caller without Case record U |
| TC-E7-007-06-ITG | Principle 5; ITG AC5 | Integration | A forced decision-record failure at the point where the case would move |

The AC column names the legacy AC the copy derives from and the ITG AC it asserts, and the full legacy test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx under the same legacy test case ID. Legacy AC2, AC3 and AC4 are the build's, in RWB-S8-E7007-APP; the -ITG copies assert the same behaviour across the services the flow crosses.

### 17. Guardrails

- No business value in code: the synthetic case, asset, collateral and claim keys, the business date, the transition event codes, the report layout and the gate are data.
- No personal data in logs, events or reports: every key is synthetic, and the events carry IDs and facts only.
- ACE data only through the P1 contract: DP01 and DP13 with their freshness stamp, never a direct view read and never another service's schema (DP-01, DP-05).
- One hop and a 2 s budget per call, with a circuit breaker per downstream, so the harness fails where a screen would (DP-11, DP-13).
- The deviation is never read back to prove a transition: its contract publishes the raise and the transition only, so the effect is asserted through the case, the timers and the decision log.
- A stub pass is never reported as a real pass: the report names the contract version and whether the hop was a stub or the owner.
- The harness never runs against UAT or production, and it never writes a row by hand or sets a state it then asserts.
- A failing criterion is fixed in the owning service or raised as a gap; it is never waived in the script.

### 18. Traceability

| Item | Source | Where it lands |
|---|---|---|
| Legacy story RWB-E7-007 Run X7 collateral event end to end | Recovery Workbench User Stories Epics 3 to 8 v3, lines 11476 to 11571 | Sections 1, 3, 11, 14 and 19 of this file |
| Legacy AC1, verbatim | The same, lines 11493 to 11499 | Section 7, AC1, marked (legacy RWB-E7-007 AC1) |
| Legacy AC2, AC3 and AC4 | The same, lines 11501 to 11517 | AC2 and AC5 assert the same behaviour here; the legacy criteria stay with RWB-S8-E7007-APP (sections 7 and 19) |
| Legacy test cases TC-E7-007-01 to TC-E7-007-06 | The same, lines 11561 to 11568 | Copied as -ITG in section 16 |
| FEAT-DVF-07 Run X7 collateral event end to end | Epics 3 to 8 Specification v3, line 130; FSD S8 Deviation handling v3, A2.16 | Sections 1 and 2 |
| FEAT-GUA-08 File an insurance claim on a collateral event | Epics 3 to 8 Specification v3, line 44; FSD S3 Guarantees and guarantors v3, A2.8 | Sections 4, 12.2 and 12.8 |
| INT-29 Thai Credit Guarantee Corporation | Epics 3 to 8 Specification v3, line 238 | Sections 2 and 12.8: the guarantee claim path is entered and filed by the officer, and the harness reads only the S3 answer |
| REQ-S8-005 and REQ-S8-001 | Business Requirements Program v4, lines 421 and 417 | Section 8, BR6, and section 7, AC3 |
| R-DEV-06 and R-DEV-12 | Business Rules and Routing Logic v4, lines 388 and 394 | Sections 8 and 9 |
| R-DEV-09 and R-DEV-19 | Business Rules and Routing Logic v4, lines 391 and 401 | Sections 8 and 9 |
| R-DEV-17 | Business Rules and Routing Logic v4, line 399 | Section 9: the X6 path shares DEV_REROUTE and is not asserted here |
| DF-CAS-036 to DF-CAS-045, DF-CAS-001 to DF-CAS-023, DF-WRK-009 to DF-WRK-016, DF-WRK-027 to DF-WRK-036, DF-ACE-091 to DF-ACE-098, DF-ACE-187 to DF-ACE-195, DF-DEC-001 to DF-DEC-018, DF-REF-001 to DF-REF-015 | Logical Data Model and Data Dictionary v8 | Section 11 |
| DP-03, DP-05, DP-13 and DP-19 | Template and Rules v1 §R5.5 | Section 13, pattern application |
| ADR-015, ADR-020 and ADR-022 | Architecture Decision Records v3 | Sections 12.4, 12.2 and 8: outbox and inbox on Kafka, contract-first REST with one hop and 2 s, local decision record plus central ledger |
| DeviationWorkflow, GuaranteeClaimWorkflow and CaseWorkflow | Architecture v5 slides 15, 18, 25 and 41; Temporal and Drools design slides 13 and 24 | Sections 2, 9, 12.5 and 13 |

### 19. Out of scope

- RWB-S8-E7007-CON and RWB-S8-E7007-APP: the build of the X7 flag, the routing by code, the return point and the decision record.
- The S8 build itself, and the SCR-08 Deviation queue and SCR-06 Raise deviation screens with it.
- The S3 guarantee build: the insurance claim, its types, its deadlines and its payment are S3's stories, and this story only files it and reads the answer.
- The SVAF and asset valuation adapters as products: the re-appraisal order and the appraisal intake are S1's and ACE's, and this story only records the re-appraisal and reads it back.
- The asset and auction stories of S5, and the monthly re-appraisal schedule (JOB-19).
- The platform stories named in section 13, and platform deployment and configuration.
- Every production change: this story adds no endpoint, no table, no workflow, no activity, no schedule and no screen.
