# RWB-ITG-W2J01-ITG Wave 2 journey end to end

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-W2J01-ITG |
| Work type | ITG (Integration) |
| Suggested owner | QA team (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W2 |
| Wave | 2 |
| Business epic | NEW |
| Release | None (new story) |
| Legacy key | W2J01 |
| Legacy disposition | New |
| Build status | Not started |
| Patterns applied | None |
| Parallel lane | L-ITG-W2 |
| Ready to start | Day 1 |
| Size | Fits two weeks; set by the squad at refinement |
| Depends on (build) | None |
| Contract dependencies | RWB-ITG-W2J01-CON |
| Contract version | v1 (base path /api/recovery/<short>/v1) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: new integration harness story for the wave 2 release gate. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (17 resolved, 7 cross-document, 2 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **member of the QA team**, I want **one repeatable wave 2 end-to-end journey harness that chains the wave 2 business behaviour on one case for one business date across rwb-payment, rwb-treatment, rwb-asset, rwb-deviation and rwb-integration, asserting each hop through the owner's published contract and composing through gateway-bff where a screen would**, so that **the wave 2 release is accepted on evidence of the whole journey and not on four separate service test results, and a red hop stops the release instead of being found in production**.

This story builds the harness, its evidence and its gate. It builds no production screen, endpoint, event, workflow, Schedule or table, and it owns no table. The behaviour it proves is owned by the wave 2 service stories and by the platform stories of rwb-case, rwb-source-data, rwb-decision and rwb-access; the harness only drives the owners' published operations, reads the owners' published answers and records what happened.

The journey chains, in this order, only the wave 2 business behaviour of EP02 and EP03 (wave map §R5.6: EP02 and EP03 are wave 2): case entry and route with its decision record; a payment matched and its clearance confirmed in rwb-payment; the settlement or TDR treatment in rwb-treatment (R-SET-20, R-RES-33); the collateral release instruction to CCMS through rwb-integration with the case at COLLATERAL_RELEASE_REQUESTED (the journey the sibling harness story RWB-ITG-E3017-ITG also covers); an asset taken on and held in rwb-asset; the monthly re-appraisal cycle falling due and the order to SVAF raised through rwb-integration (R-DIS-15, JOB-19; the journey the sibling harness story RWB-ITG-E3026-ITG also covers); a deviation raised in rwb-deviation that pauses the stage clock while the prescription clock keeps running (R-DEV-01); and the case closed or sold, with the ledger read through rwb-source-data and every decision record reaching rwb-decision.

The five owners the journey drives are rwb-payment (P8), rwb-treatment (S2), rwb-asset (S5), rwb-deviation (S8) and rwb-integration (P2). rwb-case, rwb-source-data, rwb-decision and rwb-access are read as the platform owners of the case state, the ledger, the decision log and the authorisation answer. The harness adds no business rule of its own: every expectation it asserts is copied from a rule, a state or an operation that a source already gives.

The harness stories are what give the QA team its Day 1 work (Template and Rules §R5.7 rule 6). W1J01 is the wave 1 counterpart and W2J01 is this one; it is the wave 2 release gate of Architecture v5 slide 46, which lists contract tests per API, event and activity, Temporal replay tests and a daily journey smoke workflow and asks how the 19 services are tested as a set.

### 2. Business rationale

A service can be green on its own contract tests and still leave the wave broken, because what the wave sells is a journey: the money arrives, the treatment closes, the bank's security comes back, the asset the bank took on is re-appraised on its cycle, and the customer's circumstances pause one clock without pausing the legal one. Each of those outcomes is produced by a different owner, on a different task queue, through a different call type, and each one is only as good as the hop before it. A wrong clearance date moves a collateral release, a missed re-appraisal cycle holds an asset at a stale value against the provision steps (FEAT-AST-05), and a deviation that pauses the prescription clock instead of the stage clock is a legal exposure, not a test failure.

The wave 2 chain also crosses the platform on every hop: the case and its clocks in rwb-case, the ledger in rwb-source-data, the decision record in rwb-decision and the authorisation answer in rwb-access. So the defects this harness catches are the ones no single service test can see: an owner that answers a shape its contract does not allow, a hop that quietly grows a second call, a decision record that is written after the state change instead of in the same transaction (R-UNI-39, Principle 5), a stale ACE data product read as if it were today's, and a repeat of the same run that produces a second business effect.

The harness is also the cheapest place to hold the wave entry check. The alternative is a manual walk-through per wave, which proves the behaviour once for one person on one day and leaves no evidence the release can be judged on. The report this harness produces is keyed by story and business date, holds one trace per run, names the contract version of every hop and holds the pass or fail the gate reads.

It meets REQ-CHO-006, REQ-CHO-009, REQ-RDF-004, REQ-DVH-002, REQ-DRI-005 and REQ-ILG-005 at the integration level and leaves every business rule and every screen behaviour with the owning stories. The journey's business rules are R-SET-20, R-SET-21, R-RES-33, R-DIS-15, R-DIS-16, R-DIS-17, R-DIS-44 and R-DEV-01, all of which the owning services run and the harness only asserts.

### 3. Preconditions

- The harness environment: the stub set, contract harness and component tests run in the DEV sandbox, and the wave journey runs in SIT (Integration Test Plan v1; Test Strategy v3). The harness repository, deployment and namespace are Not specified in the source documents (GAP-0428).
- The seeded case, its route, its proceeds, its treatment, its asset and its identifiers: Not specified in the source documents (GAP-0428). Seeding uses only the owning services' published operations, never a schema write, and the case ID keeps the form RW-YYYY-NNNNNN of REQ-CWC-002.
- The published contracts of rwb-payment, rwb-treatment, rwb-asset, rwb-deviation, rwb-integration, rwb-case, rwb-source-data, rwb-decision and rwb-access are in the contract registry, and one stub set is generated from each of them, so the journey runs from Day 1 before the wave 2 app stories are live.
- The business date under test is fixed at 2026-12-15, the business date the case and payment examples of the source documents use, and every clock the journey asserts is read from the owner and not from the harness.
- The route the seeded case carries is the route that produces both a treatment leg and a held asset leg (a deed in lieu, FEAT-TRT-12 and FEAT-AST-02, or an asset taken on after enforcement, FEAT-AST-03). Which route the case carries is decided by rwb-valuation and rwb-treatment, not by this story; the harness takes the seeded route as given and asserts the owner's state on each leg.
- The re-appraisal interval that makes the cycle fall due, and its application as data rather than code, are held by rwb-asset per R-DIS-15; the harness reads the interval and does not set it.
- The deviation code the journey raises is one of X1 to X7 (R-DEV-01); which code the seeded case carries is Not specified in the source documents (GAP-0428).
- The wave gate is ITG-W2, with the entry and exit criteria of Integration Test Plan v1 (see Gate definition). The evidence format and the evidence retention are Not specified in the source documents (GAP-0428).
- No build dependency. Day 1, against the stub set, with each stub replaced by the real owner as its wave 2 story lands.

### 4. Flow

1. Harness: seeds the case and its route through the owning services' published operations only, and reads the case back with `GET /api/recovery/case/v1/cases/{caseId}` for the route, the stage, the status, the deviation flag, the prescription date and the stage clock; the route decision's record is read with `GET /api/recovery/decision/v1/decision-log`.
2. Harness: reads the proceeds of the case with `GET /api/recovery/payment/v1/proceeds` and asserts a payment matched to the plan or the settlement, its matched_to and its posting reference; it asserts `rwb.payment.ProceedsMatched.v1` (EV-25) on `rwb.payment.events.v1` for the case, and `rwb.payment.TreatmentBooked.v1` (EV-11) where the treatment is booked.
3. Harness: reads the treatment with `GET /api/recovery/treatment/v1/treatments/{treatmentId}` and asserts its type, its booked date, its outcome and its installments paid; it asserts `rwb.treatment.TreatmentApproved.v1` (EV-10) on `rwb.treatment.events.v1`, and the settlement close of R-SET-20 and the final-installment close of R-RES-33 as the state the owner returns.
4. Harness: asserts the collateral release instruction to CCMS as an outbound item read with `GET /api/recovery/integration/v1/admin/outbound-items`, and asserts the case answers at COLLATERAL_RELEASE_REQUESTED and then at COLLATERAL_RELEASED or CASE_CLOSED_SETTLED, as the owner returns it.
5. Harness: reads the asset with `GET /api/recovery/asset/v1/assets/{assetKey}` and asserts it is taken on and held, with its transfer-in or repossession date and its stock date; it asserts `rwb.asset.AssetTakenOn.v1` (EV-22) on `rwb.asset.events.v1`.
6. Harness: holds the business date at 2026-12-15 and drives the JOB-19 re-appraisal Schedule of rwb-asset on its monthly cycle, asserts the cycle falling due against R-DIS-15, and asserts the re-appraisal order to SVAF as a second outbound item read with `GET /api/recovery/integration/v1/admin/outbound-items`.
7. Harness: raises the deviation through `POST /api/recovery/deviation/v1/cases/{caseId}/deviations` (S8), asserts `rwb.deviation.DeviationRaised.v1` (EV-06) on `rwb.deviation.events.v1` within the run window, and asserts on `GET /api/recovery/case/v1/cases/{caseId}/timers` that the stage clock is paused and the prescription clock is still running with its date unchanged (R-DEV-01).
8. Harness: asserts the case at its close or sale, and reads the ledger through `GET /api/recovery/source-data/v1/data-products/{productCode}/records` with one entry per hop of the journey.
9. Harness: reads every decision record of the journey with `GET /api/recovery/decision/v1/decision-log` and asserts `rwb.decision.DecisionRecorded.v1` (EV-08) on `rwb.decision-record.v1` for each hop that took a decision.
10. Harness: authorises every call through `POST /api/recovery/access/v1/authorise` with the role and scope of the synthetic officer, and records the refusal path for a role without the right.
11. Harness: asserts the one-hop rule and the 2 s budget from the run trace, that no hop reads another owner's schema, and that a composition goes through the gateway-bff composite route where a screen would compose.
12. Harness: repeats the run from the same seeded state, compares the two reports assertion by assertion, and asserts that no second payment match, treatment, asset take-on, re-appraisal order or deviation was created and that the ledger and the decision log hold no duplicate entry.
13. Harness: publishes the per-run evidence report keyed by story and business date with the contract version of every hop, and holds the wave gate that reads every wave 2 harness result of the business date and fails the release when one is red.

### 5. Exception paths

| ID | Trigger | What the harness asserts | Message | ITG test case | Covered by |
|---|---|---|---|---|---|
| X1 | A hop answers a shape its published contract does not allow | The run fails at that hop before any assertion of the next hop; the report names the owner, the operation and both contract versions, and the earlier state is unchanged | None | TC-W2J01-06-ITG | AC3 |
| X2 | A hop does not answer inside the 2 s budget | The run fails at that hop and names it; the report holds the elapsed time and the contract version, and the state of the earlier hops is unchanged | MSG-GEN-006 | TC-W2J01-07-ITG | AC2 |
| X3 | The decision record of a hop cannot be written | Nothing moves: the state change, the record and the outbox row are one transaction, so the hop fails and the run is reported failed, not passed (Principle 5, R-UNI-39) | MSG-P7-003 | TC-W2J01-08-ITG | AC6 |
| X4 | A role without the right calls a hop | The hop is refused and the run fails; nothing is written and the refusal carries the message, not an empty answer | MSG-P4-002 | TC-W2J01-09-ITG | AC7 |
| X5 | An ACE data product behind a hop is stale for the business date | The hop does not treat the stale product as today's; the run fails and the report names the product and the date it carries | MSG-P1-001 | TC-W2J01-10-ITG | AC8 |

The report text of a failed run is for the wave entry check and is not part of the message standard. The business messages the journey produces are asserted as data on the owners' answers and are listed in section 14.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Runs against the published contracts and the stub set from Day 1; it waits for no wave 2 build, and each stub is replaced by its owner as the owner lands |
| Negotiable | The seed, the fixed business date, the evidence format and the gate thresholds are configuration agreed at the wave entry check, not business values in code |
| Valuable | The wave 2 journey is proven as a whole before the release is accepted, which is the outcome no per-service test can give |
| Estimable | One harness runner, one stub set, one event probe, one outbound-item probe, one evidence report and one gate |
| Small | Fits in one iteration with its tests |
| Testable | Each scenario of section 7 is one automated run with a machine-checkable result, and a repeated run must reproduce it |

### 7. Acceptance criteria

```gherkin
Feature: Wave 2 journey end to end - integration harness

  Background:
    Given the business date under test is 2026-12-15
    Given the seeded case and its proceeds, treatment, asset and deviation identifiers are Not specified in the source documents (GAP-0428)
    Given the published contracts of rwb-payment, rwb-treatment, rwb-asset, rwb-deviation, rwb-integration, rwb-case, rwb-source-data, rwb-decision and rwb-access are in the contract registry with a stub set generated from each

  Scenario: AC1 The journey runs green for one business date (new, D-RCV-60)
    Given the case has entered from the daily case list with a route and with its route decision record
    When the harness runs the journey for business date 2026-12-15 across the five owners
    Then a payment is matched and its clearance is confirmed in rwb-payment
    And the settlement or TDR treatment records its outcome in rwb-treatment
    And the collateral release instruction to CCMS is raised through rwb-integration and the case answers at COLLATERAL_RELEASE_REQUESTED
    And an asset is taken on and held in rwb-asset
    And the re-appraisal cycle falls due and the order to SVAF is raised through rwb-integration
    And the deviation pauses the stage clock and the prescription clock keeps running
    And the case closes or is sold
    And the ledger read through rwb-source-data holds one entry per hop
    And every decision record of the journey is read from rwb-decision
    And the run is green, recorded against one parent CaseWorkflow, with one trace

  Scenario: AC2 Each hop is one owner, one hop, a 2 s budget (new, D-RCV-60)
    Given the harness records the trace of the run
    When the harness reads every hop from the trace
    Then each hop calls exactly one owner and no owner calls a second owner inside the hop
    And each call answers inside the 2 s budget with a circuit breaker per downstream
    And no hop reads another owner's schema, and every read names a published operation
    And where a screen would compose several owners, the harness calls the gateway-bff composite route
    And no call uses the retired monolith base (DP-13)

  Scenario: AC3 A forced failure names the hop and leaves the earlier state unchanged (new, D-RCV-60)
    Given the treatment hop is forced to answer a shape its contract does not allow
    When the harness runs the journey for business date 2026-12-15
    Then the run stops at the treatment hop and names rwb-treatment, the operation and both contract versions
    And the payment, the case and the ledger carry the state they carried before the hop
    And the run is reported failed and is never reported passed
    And the evidence report names the hop that failed

  Scenario: AC4 A repeated run produces the same evidence and no duplicate business effect (new, D-RCV-60)
    Given the first run of the journey ended green for business date 2026-12-15
    When the harness returns to the same seeded state and runs the journey again for 2026-12-15
    Then the evidence report is the same as the first run on every assertion it holds
    And no second payment match, treatment, asset take-on, re-appraisal order or deviation is created
    And the ledger and the decision log hold no duplicate entry for the journey

  Scenario: AC5 The wave gate fails the release on one red harness result (new, D-RCV-60)
    Given the wave gate reads every wave 2 harness result recorded for business date 2026-12-15
    When one wave 2 harness result is red
    Then the gate reports the release as failed and names the red harness and the hop that failed
    And the gate reports the release as passed only when every wave 2 harness result is green

  Scenario: AC6 A decision record that cannot be written stops the hop and fails the run (new, D-RCV-60)
    Given the decision record of one hop is forced to fail to write
    When the harness runs the journey for business date 2026-12-15
    Then the state change, the record and the outbox row of that hop are not written
    And the run is reported failed and is never reported passed
    And MSG-P7-003 is asserted on the owner's answer

  Scenario: AC7 A role without the right is refused on a hop and the run fails (new, D-RCV-60)
    Given RW-AUDIT calls a hop that needs the officer's right
    When the harness authorises the call through POST /api/recovery/access/v1/authorise
    Then the hop is refused and the run fails
    And nothing is written and the refusal carries MSG-P4-002, not an empty answer

  Scenario: AC8 A stale ACE data product is never read as today's and fails the run (new, D-RCV-60)
    Given a data product behind a hop carries the previous business date
    When the harness runs the journey for business date 2026-12-15
    Then the hop does not treat the stale product as today's
    And the run fails and the report names the product and the date it carries
    And MSG-P1-001 is asserted on the owner's answer

  Scenario: AC9 BR2 to BR6 hold on the owners' answers and no rule is re-implemented (new, D-RCV-60)
    Given the journey has reached the close, the treatment, the re-appraisal, the valuer report and the no-bid round of the seeded case
    When the harness reads each owner's answer for BR2 to BR6
    Then BR2 holds: the case closes at CASE_CLOSED_SETTLED when CCMS confirms the release
    And BR3 holds: the treatment, the collateral release and the case close when the final installment is paid
    And BR4 holds: the re-appraisal order goes to SVAF only when the appraisal date is older than 12 months and the one-year rule is not applied
    And BR5 holds: a valuer report runs the outlier check and an accepted value resets the list and floor price inputs
    And BR6 holds: a round closing with no bid at the floor re-lists the asset and orders a re-appraisal where the cycle is due
    And the harness changes no rule and re-implements none of them

  Scenario: AC10 A consumed call that fails or does not answer stops the hop and fails the run (new, D-RCV-60)
    Given a consumed owner call on one hop is forced to fail or to give no answer within the 2 s budget
    When the harness runs the journey for business date 2026-12-15
    Then the run stops at that hop and names the owner, the operation and the contract version
    And nothing is written past that hop
    And the run is reported failed and is never reported passed

  Scenario: AC11 A status change the model does not allow is refused and the run fails (new, D-RCV-60)
    Given a hop attempts a status change that the case status model does not allow
    When the harness runs the journey for business date 2026-12-15
    Then the change is refused and the case keeps the status it carried before the hop
    And nothing is written for the refused change
    And the run is reported failed and is never reported passed
```

The eleven criteria are new for this harness and restate no app criterion. The criteria of the wave 2 services are owned by their own stories, and the two journey hops that also carry a sibling harness (the collateral release of RWB-ITG-E3017-ITG and the re-appraisal of RWB-ITG-E3026-ITG) are asserted here only as hops of the wave 2 chain.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | When funds are cleared, the account is closed in ALS and the collateral release is requested, and the case moves to COLLATERAL_RELEASE_REQUESTED | R-SET-20 |
| BR2 | When CCMS confirms the release, the title returns, the treatment closes and the case closes at CASE_CLOSED_SETTLED | R-SET-21 |
| BR3 | When the final installment is paid, the treatment closes, the collateral is released and the case closes | R-RES-33 |
| BR4 | The re-appraisal cycle falls due when the appraisal date is older than 12 months and the one-year rule is not applied, and the order goes to SVAF | R-DIS-15; JOB-19 |
| BR5 | A valuer report records the value and runs the outlier check, and an accepted value updates the appraised value and resets the list and floor price inputs | R-DIS-16; R-DIS-17 |
| BR6 | A round that closes with no bid at the floor re-lists the asset and orders a re-appraisal where the cycle is due | R-DIS-44 |
| BR7 | A deviation of code X1 to X7 pauses the stage clock, keeps the prescription clock running and routes the case to the named owner the same day | R-DEV-01 |
| BR8 | No action proceeds if its decision log entry cannot be written; the record, the state change and the outbox row are one transaction | REQ-DRI-005; R-UNI-39; Principle 5 |
| BR9 | Every action the Workbench takes on a case writes to the ledger as it happens | REQ-ILG-005; FEAT-ILG-01 |
| BR10 | A decision records the freshness of the data it used, and a stale data product is never read as today's | REQ-RDF-009; MSG-P1-001 |
| BR11 | No component calls a system of record directly; ACE data is read only through rwb-source-data's contract | REQ-DRI-006 |
| BR12 | An outbound instruction to an outside system is an item its owner can read back, with its own result and retry | REQ-DRI-007 |

The harness asserts these twelve rules against the owners and the published contracts; it re-implements none of them and changes no BR row.

### 9. State transitions

The harness changes no case, treatment, asset, deviation or decision state of its own. Every move below is made by the owner when the harness calls the owner's published operation, or when the owner's workflow reacts to an event the harness caused. A state the harness set by hand would prove nothing, so the report names the owner and the operation that made each move.

| Observed fact | Caused by | Asserted as |
|---|---|---|
| Payment matched and its clearance confirmed | rwb-payment, JOB-07 payment matching and the clearance step of R-SET-20 | The proceeds answer carries the match and the posting reference; ProceedsMatched is on the topic (TC-W2J01-01-ITG) |
| Treatment booked, approved and closed at PLAN_COMPLETED or CASE_CLOSED_SETTLED | rwb-treatment, TreatmentWorkflow | The treatment answer carries its type, its booked date, its outcome and its installments paid (TC-W2J01-01-ITG) |
| Collateral release requested, then released | rwb-treatment with CCMS through rwb-integration | The case answers at COLLATERAL_RELEASE_REQUESTED and then at COLLATERAL_RELEASED or CASE_CLOSED_SETTLED, and the outbound item is readable (TC-W2J01-01-ITG) |
| Asset taken on and held at ASSET_HELD | rwb-asset, AssetDisposalWorkflow | The asset answer carries its transfer-in or repossession date and its stock date; AssetTakenOn is on the topic (TC-W2J01-01-ITG) |
| Re-appraisal cycle due and the order to SVAF raised | rwb-asset, the JOB-19 monthly Schedule | The asset answers at REAPPRAISAL_CYCLE_DUE and then at REAPPRAISAL_ORDERED, and the SVAF outbound item is readable (TC-W2J01-01-ITG) |
| Deviation flagged at DEV_FLAGGED | rwb-deviation, DeviationWorkflow | DeviationRaised is on the topic, the case answers with the flag, the stage clock is paused and the prescription date is unchanged (TC-W2J01-01-ITG) |
| Case closed or sold | rwb-case on the owner's state, and rwb-asset where the case ends in a sale | The case answers at its close state and the asset answer carries its sale state where the leg is a sale (TC-W2J01-01-ITG) |
| A hop forced to answer a shape its contract does not allow | the harness, on the stub set | The run stops at the hop and the earlier state is unchanged (TC-W2J01-06-ITG) |
| A decision record that cannot be written | the owner of the hop, whose transaction rolls back | Nothing moved and the run is failed (TC-W2J01-08-ITG) |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-OFF, recovery officer | The synthetic user the harness drives: reads and drives the case through the owning contracts within the case scope of the seeded queue (R-ALLOC rules of the allocation table) |
| RW-CASEOWN, case owner | Reads the case, its timers, its deviation flag and the ledger of the same seeded case |
| RW-TEAMMGR, team manager | Reads the same evidence across the queue; changes nothing |
| RW-AUDIT, internal audit | Reads the decision log and the ledger of the journey; changes nothing |
| RW-PLATADM, platform administrator | Reads the outbound items and the data product freshness the run asserts; resends nothing |
| QA lead | Owns the seeded data, the fixed business date, the stub set, the evidence format and the wave gate |
| Integration lead | Owns the harness code, the trace assertions and the swap from a stub to the real owner |
| The owning services' identities | rwb-payment, rwb-treatment, rwb-asset, rwb-deviation, rwb-integration, rwb-case, rwb-source-data, rwb-decision and rwb-access make every state change the harness asserts |
| No delegation of authority level applies | The harness takes no business decision; approvals inside the journey are the approval stories' |

Authorisation is answered on every call by `POST /api/recovery/access/v1/authorise`, and the harness asserts both the allow path for RW-OFF in scope and the refusal path for a role without the right.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-005 | recovery_case | status | Read |
| DF-CAS-017 | recovery_case | prescription_date | Read |
| DF-CAS-018 | recovery_case | stage_clock_start | Read |
| DF-CAS-019 | recovery_case | deviation_open | Read |
| DF-FIN-001 | proceeds | id | Read |
| DF-FIN-002 | proceeds | case_id | Read |
| DF-FIN-005 | proceeds | source | Read |
| DF-FIN-008 | proceeds | matched_to | Read |
| DF-FIN-009 | proceeds | posting_ref | Read |
| DF-TRT-001 | treatment | id | Read |
| DF-TRT-004 | treatment | treatment_type | Read |
| DF-TRT-012 | treatment | booked_at | Read |
| DF-TRT-013 | treatment | outcome | Read |
| DF-TRT-032 | treatment | installments_paid | Read |
| DF-COL-031 | asset | asset_ref | Read |
| DF-COL-033 | asset | asset_type | Read |
| DF-COL-036 | asset | transfer_in_date | Read |
| DF-COL-039 | asset | repossessed_date | Read |
| DF-COL-040 | asset | stock_date | Read |
| DF-COL-023 | valuation | appraised_value | Read |
| DF-COL-025 | valuation | appraisal_date | Read |
| DF-CAS-038 | deviation | deviation_code | Written by rwb-deviation through `POST /cases/{caseId}/deviations`, read back |
| DF-CAS-039 | deviation | raised_at | Read |
| DF-CAS-041 | deviation | paused_state | Read |
| DF-CAS-043 | deviation | contact_stop | Read |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Read, through the rwb-decision contract |
| DF-INT-005 | interaction | channel | Read, through the rwb-source-data contract |
| DF-INT-011 | interaction | summary | Read, through the rwb-source-data contract |

Field IDs are those of the Logical Data Model and Data Dictionary. The harness owns no table and writes no row directly: it reads through the owner's contract and its only write is the deviation it raises through the rwb-deviation operation (DP-01). Test data is synthetic; no production case, party, payment or asset is copied, and no personal data is written to a report.

### 12. Contract

#### 12.1 REST operations provided

None. The harness is a test runner: it serves no operation, opens no port a service calls and publishes no endpoint.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| GET | `/api/recovery/payment/v1/proceeds` | P8 rwb-payment | The payment matched to the plan or the settlement, its matched_to and its posting reference (AC1) |
| GET | `/api/recovery/treatment/v1/treatments/{treatmentId}` | S2 rwb-treatment | The treatment type, its booked date, its outcome and its installments paid (AC1, AC3) |
| GET | `/api/recovery/asset/v1/assets/{assetKey}` | S5 rwb-asset | The asset taken on and held, its dates and its re-appraisal state (AC1) |
| POST | `/api/recovery/deviation/v1/cases/{caseId}/deviations` | S8 rwb-deviation | Raises the journey deviation through its owner (AC1) |
| GET | `/api/recovery/integration/v1/admin/outbound-items` | P2 rwb-integration | The CCMS collateral release instruction and the SVAF re-appraisal order (AC1) |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The route, the stage, the status, the deviation flag and the prescription date (AC1, AC3) |
| GET | `/api/recovery/case/v1/cases/{caseId}/timers` | P3 rwb-case | The paused stage clock and the running prescription clock after the deviation (AC1) |
| GET | `/api/recovery/source-data/v1/data-products/{productCode}/records` | P1 rwb-source-data | The ledger entries of the journey and the freshness of the data product (AC1, X5) |
| GET | `/api/recovery/decision/v1/decision-log` | P7 rwb-decision | The decision record of every hop that took a decision, including the route decision (AC1, X3) |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | The role, scope and right check on every call, including the refusal path (X4) |

Every operation is one hop on the owner's base `/api/recovery/<short>/v1` with a 2 s budget and a circuit breaker per downstream; where a screen would compose several owners, the harness calls the gateway-bff composite route. The composite route paths and their merge order are Not specified in the source documents (GAP-0428).

The deviation is read back through the rwb-case contract and not through a deviation GET path: the ownership map gives `POST /cases/{caseId}/deviations` and `PATCH /deviations/{deviationId}` for S8 and no GET deviations path, so the harness reads the flag from rwb-case and names the S8 read operation as the one RWB-S8-E2015-APP publishes rather than restating a path here. No operation is invented in this story.

#### 12.3 Events published

None. The harness publishes no Kafka event; it consumes the owners' events and writes its evidence report to the wave record.

#### 12.4 Events consumed

| Event | Topic | Producer | What the harness asserts |
|---|---|---|---|
| `rwb.payment.ProceedsMatched.v1` (EV-25) | `rwb.payment.events.v1` | P8 rwb-payment | The match fact for the case, keyed by caseId, present inside the run window |
| `rwb.payment.TreatmentBooked.v1` (EV-11) | `rwb.payment.events.v1` | P8 rwb-payment | The booking fact where the treatment leg books a plan |
| `rwb.treatment.TreatmentApproved.v1` (EV-10) | `rwb.treatment.events.v1` | S2 rwb-treatment | The approval of the treatment before its close |
| `rwb.asset.AssetTakenOn.v1` (EV-22) | `rwb.asset.events.v1` | S5 rwb-asset | The take-on fact for the asset of the case |
| `rwb.deviation.DeviationRaised.v1` (EV-06) | `rwb.deviation.events.v1` | S8 rwb-deviation | One fact per deviation raised on the case, with its code |
| `rwb.decision.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | all 19 services | One record per hop that took a decision, arriving before the record is read from the central ledger |

The events carry IDs and business facts only, keyed by caseId, and the harness asserts the absence of personal data in each one (DP-09). Order per case is guaranteed by the case key, and every state the harness asserts is read from the owner's contract and never reconstructed from a topic.

#### 12.5 Workflows and activities

None added. The harness starts no workflow, adds no activity and owns no task queue. It exercises the existing parent CaseWorkflow in rwb-case (one per case, entry to closure, with a child workflow per stage) and the stage children the journey needs: TreatmentWorkflow on the rwb-treatment queue, AssetDisposalWorkflow on the rwb-asset queue and DeviationWorkflow on the rwb-deviation queue, which can start at any time and pauses the stage clock. It exercises JOB-07 payment matching, the event-triggered workflow in rwb-payment, and JOB-19 Re-appraisal, the monthly Schedule in rwb-asset, and asserts their effects through the owners' contracts and topics. The route decision itself runs on the route owner and is asserted here as case state and as a decision record only. No workflow, activity or Schedule is created, changed or owned by this story (DP-10, DP-12).

#### 12.6 Schedules

None added. JOB-19 Re-appraisal (monthly, rwb-asset) is exercised on the cycle of business date 2026-12-15, and JOB-07 Payment matching (event-triggered, rwb-payment) is exercised on the AceDataReady of the business date. No cron, overlap policy or catch-up window is set, changed or owned by this story (DP-10).

#### 12.7 Tables owned

None. The harness owns no schema and no table (DP-01). It reads the case through rwb-case, the ledger through rwb-source-data (DP-18), the decision record through rwb-decision and the freshness of the data product through rwb-source-data; it never reads another owner's tables and never writes a row.

#### 12.8 Contract fakes

| Fake | Contract | Use in the run |
|---|---|---|
| WireMock stub for rwb-payment | `GET /proceeds`, `rwb.payment.events.v1` | Day-1 run of the match and clearance hop before the wave 2 app story is live |
| WireMock stub for rwb-treatment | `GET /treatments/{treatmentId}` | Day-1 run of the treatment hop, and the forced bad shape of AC3 |
| WireMock stub for rwb-asset | `GET /assets/{assetKey}` | Day-1 run of the take-on, the hold and the re-appraisal cycle |
| WireMock stub for rwb-deviation | `POST /cases/{caseId}/deviations` | Day-1 run of the deviation hop, and the forced decision-record failure of X3 |
| WireMock stub for rwb-integration | `GET /admin/outbound-items` | Day-1 assertions on the CCMS instruction and the SVAF order |
| WireMock stub for rwb-case | `GET /cases/{caseId}`, `GET /cases/{caseId}/timers` | Day-1 assertions on the route, the status, the deviation flag and the two clocks |
| WireMock stub for rwb-source-data | `GET /data-products/{productCode}/records` | Day-1 assertions on the ledger entries and the stale product of X5 |
| WireMock stub for rwb-decision | `GET /decision-log` | Day-1 assertions on the route decision record and the records of the journey |
| WireMock stub for rwb-access | `POST /authorise` | Day-1 authorisation and the refusal path of X4 |

Each stub is generated from the published contract and its version is pinned in the run report, so a contract change shows up as a run failure and not as a silent pass. The wave gate is ITG-W2 (see Gate definition). The evidence format, the evidence retention and the seeding set are Not specified in the source documents (GAP-0428).

#### 12.9 Call-type summary

| Call type | In this story |
|---|---|
| REST | 0 provided, 10 consumed, one hop each on `/api/recovery/<short>/v1` with a 2 s budget and a breaker per downstream, composed through gateway-bff where a screen would (AC1, AC2, X1, X2, X4) |
| Kafka | None published; `rwb.payment.ProceedsMatched.v1`, `rwb.payment.TreatmentBooked.v1`, `rwb.treatment.TreatmentApproved.v1`, `rwb.asset.AssetTakenOn.v1`, `rwb.deviation.DeviationRaised.v1` and `rwb.decision.DecisionRecorded.v1` consumed for assertion (AC1) |
| Temporal | None added; the parent CaseWorkflow, the treatment, asset and deviation stage children, JOB-07 payment matching and JOB-19 Re-appraisal exercised (AC1) |
| File | None. The harness reads and writes no file exchange; the CCMS instruction and the SVAF order are asserted as outbound items of rwb-integration, and the evidence report is a harness artefact and not a service file (AC1) |

### 13. Solution plan

**Pattern application**

None. This story applies no decoupling pattern of §R5.5; it reads each owner through that owner's published contract and records the result.

The harness holds the architecture as an assertion, not as a pattern it applies: it calls one owner per hop on that owner's base and fails a run whose trace shows a call chain deeper than the gateway and one owner (DP-11), it composes through the gateway-bff composite route where a screen would (DP-19), it reads the ledger from rwb-source-data and not from a table (DP-18), it reads the case, the decision record and the authorisation answer from their owners, and it fails a run that finds a cross-schema read. Because the patterns belong to the services, this story's metadata Patterns applied row is None and the tables above name only owners the ownership map gives.

The harness is the wave 2 release gate. The wave 2 business epics are EP02 and EP03 (§R5.6), the wave is delivered by four service epics plus the integration epic, and no release is accepted on four separate green service runs. The gate reads every wave 2 harness result recorded for the business date, the two sibling harness stories included, and it passes the release only when every one of them is green. It is part of the wave gate ITG-W2 (see Gate definition); its evidence format is Not specified in the source documents (GAP-0428).

**Harness components**

| Component | Type | Responsibility |
|---|---|---|
| JourneyRunner | Job | Runs the journey once per business date in hop order, holds the run lock and stops the run at the first failed hop |
| OwnerClient | Harness adapter | Calls the ten consumed operations of §12.2, one hop each, with the 2 s budget and the Idempotency-Key header where the operation requires one |
| StubSet | Fake | The nine WireMock stubs generated from the published contracts, each with its version pinned in the report |
| EventProbe | Service | Consumes the six events of §12.4 and asserts each fact for the case inside the run window, including the absence of personal data |
| OutboundItemProbe | Assertion | Asserts the CCMS release instruction and the SVAF re-appraisal order as readable outbound items of rwb-integration |
| TraceAssertion | Assertion | Fails the run on a call chain deeper than the gateway and one owner, on a call outside the 2 s budget, and on any cross-schema reference in the trace |
| ClockProbe | Assertion | Reads the two clocks of the case before and after the deviation and fails the run when the stage clock is not paused or the prescription date has moved |
| RepeatProbe | Assertion | Compares a repeated run from the same seed assertion by assertion, and fails on a second business effect or a duplicate ledger or decision entry |
| WaveGate | Reporter | Writes the per-run evidence report keyed by story and business date and holds the pass or fail the wave entry check reads |

**Environment and test data**

- Environment: the DEV sandbox for the stub set and SIT for the wave journey (Integration Test Plan v1). The harness repository is Not specified in the source documents (GAP-0428). The run is against the §12.8 stub set from Day 1 and against each real owner as its wave 2 story lands.
- Data: the seeded case, its route, its proceeds, its treatment, its asset and its identifiers: Not specified in the source documents (GAP-0428). The case ID keeps the form RW-YYYY-NNNNNN of REQ-CWC-002, the business date under test is fixed at 2026-12-15, and the deviation is one of X1 to X7 as R-DEV-01 gives them. No production record is copied.
- Reset: each run starts from the same seeded state and the same fixed business date, so a repeated run is deterministic and the two reports are comparable assertion by assertion.
- Seeding: through the owners' published operations only, never a schema write, so the seeded state is one the services themselves accept.

**Build steps**

1. Generate the nine stubs from the published contracts, pin each contract version in the report, and prove the journey runs green against the stub set from Day 1 (X1).
2. Build JourneyRunner and OwnerClient with the hop order of §4, the 2 s budget, the breaker per downstream and the run lock.
3. Add the payment, treatment and case hops of AC1 and assert the states of §9 as the owners return them.
4. Add the two outbound-item assertions through rwb-integration: the CCMS collateral release instruction and the SVAF re-appraisal order, with JOB-19 driven on the fixed business date.
5. Add the asset take-on and hold assertions, and the re-appraisal cycle assertion of R-DIS-15.
6. Add the deviation hop: raise it through the S8 operation, assert DeviationRaised, and assert with ClockProbe that the stage clock pauses and the prescription clock keeps its date (R-DEV-01).
7. Add the ledger and decision-record assertions, the access path through `POST /api/recovery/access/v1/authorise` and the refusal path of X4.
8. Add TraceAssertion, the forced bad shape of AC3 and the timeout case of X2, and prove a forced failure names the hop and leaves the earlier state unchanged.
9. Add RepeatProbe and prove the repeated run reproduces the report with no duplicate business effect.
10. Add WaveGate, read every wave 2 harness result of the business date, and prove the release fails when one of them is red.
11. Swap one stub for its real owner as each wave 2 story lands, rerunning the journey after each swap, and report a stub pass as a stub pass and never as a real-owner pass.

**Gate definition.** The gate reads the wave 2 harness results recorded for the business date and passes the release only when every one of them is green; one red harness fails the release and names the harness and the hop. This check is part of the wave gate ITG-W2. ITG-W2 entry: wave 1 exit met; P8, S2, S5 and S8 deployed; their contracts pinned; the harness extended to the wave 2 contracts. ITG-W2 exit: every wave 2 journey test case passes; no open severity 1 or 2 defect; the non-functional evidence of wave 2 green (Integration Test Plan v1). The evidence format and retention are Not specified in the source documents (GAP-0428), and the gate holds no threshold beyond every harness result green.

**Feature switch.** The harness has no production feature flag and runs in the test environment only. The wave 2 behaviour it exercises is switched on by the wave 2 stories' own flags; where a flag holds a behaviour off, the run reports the hop as skipped and the gate treats a skipped hop as not green.

**Done when.** The tests of section 16 pass; the journey runs green for business date 2026-12-15 against the stub set on Day 1 and again, hop by hop, against each real owner as its wave 2 story lands; the report holds one trace, the contract version of every hop and every assertion of section 7; and the wave gate fails the release on one red harness result and passes it on all green.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P7-003 | The decision record of a hop cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | A role without the right calls a hop | You cannot {action} here. Your role does not include it. |
| MSG-P1-001 | An ACE data product behind a hop is stale for the business date | {product} is from {date}. Today's load has not arrived. |
| MSG-P3-004 | The case answers as on hold for the deviation the harness raised | This case is on hold for {deviation}. The prescription date is still {date}. |
| MSG-GEN-006 | A system of record behind a hop does not answer inside the budget | {system} is not available. Your request is queued and will be retried. |

The harness produces none of these messages itself: it asserts the message the owning service returns and names the message ID in the report, so a failed run points at an owner, an operation and a message and not only at a date. MSG-P1-001 is the message a stale data product raises; MSG-P1-002 of the same family is the refusal of a reference load and is not the one a stale product produces, so it is not asserted here. Thai text for each message follows decision DL10, which is open; its assumptions are ASM-2250, ASM-2357, ASM-2377 and ASM-2863.

### 15. Screens and states

The harness renders no screen and opens no page. Where a screen would compose several owners, the harness calls the gateway-bff composite route and asserts the answer the screen consumes, so a green hop means the screen has the right data behind it:

| Screen | State | What the harness asserts |
|---|---|---|
| SCR-03 Case record | Settlement leg | The case answers with its route, its stage and its status, the treatment answer carries its outcome, and the collateral release instruction is readable as an outbound item |
| SCR-03 Case record | Asset on hold | The asset answer carries its type, its take-on date and its stock date, and the re-appraisal cycle state and the SVAF order |
| SCR-03 Case record | On hold for a deviation | The deviation flag with the code, the paused stage clock and the prescription date unchanged (MSG-P3-004 where the case answers as on hold) |
| SCR-03 Case record | Loading | Not specified in the source documents (CG-ALL-857) |
| SCR-03 Case record | Empty | Not specified in the source documents (CG-ALL-857) |
| SCR-03 Case record | Error | Not specified in the source documents (CG-ALL-857) |
| SCR-03 Case record | No access | Not specified in the source documents (CG-ALL-857) |

The screen behaviour of each state stays with the wave 2 app stories. What the wave entry check reads instead is the evidence report, whose format and retention are Not specified in the source documents (GAP-0428).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-W2J01-01-ITG | AC1, BR1 to BR7, BR9 | End to end | Business date 2026-12-15, seeded case through entry, route, payment, treatment, collateral release, asset take-on, re-appraisal, deviation and close |
| TC-W2J01-02-ITG | AC2, BR11 | Component | Run trace of the AC1 run; one owner per hop, 2 s budget, no cross-schema read, gateway-bff composition |
| TC-W2J01-03-ITG | AC3 | Integration | Treatment hop forced to answer a shape its contract does not allow |
| TC-W2J01-04-ITG | AC4 | Integration | The same seeded state run twice on 2026-12-15 |
| TC-W2J01-05-ITG | AC5 | End to end | Every wave 2 harness result recorded for the business date, one of them red |
| TC-W2J01-06-ITG | X1 | Component | Contract version mismatch and a shape outside the OpenAPI document on one hop |
| TC-W2J01-07-ITG | X2, BR12 | Integration | One hop delayed past the 2 s budget |
| TC-W2J01-08-ITG | X3, BR8 | NFR | Decision record write forced to fail on ten hops; no state changes |
| TC-W2J01-09-ITG | X4 | Component | RW-AUDIT calls a hop that needs the officer's right; refused with MSG-P4-002 |
| TC-W2J01-10-ITG | X5, BR10 | Integration | Data product behind a hop carries the previous business date; MSG-P1-001 |
| TC-W2J01-11-ITG | AC6 | Integration | Decision record write forced to fail on one hop; no state changes |
| TC-W2J01-12-ITG | AC7 | Component | RW-AUDIT calls a hop that needs the officer's right; refused with MSG-P4-002 |
| TC-W2J01-13-ITG | AC8 | Integration | Data product behind a hop carries the previous business date; the run fails naming the product |
| TC-W2J01-14-ITG | AC9, BR2 to BR6 | Component | Owner answers for the close, the treatment, the re-appraisal, the valuer report and the no-bid round, read against the published contracts |
| TC-W2J01-15-ITG | AC10 | Integration | A consumed owner call on one hop forced to fail or to give no answer within the 2 s budget |
| TC-W2J01-16-ITG | AC11 | Integration | A hop attempts a status change that the case status model does not allow |

The full test, with its Given, When and Then, is held under the same test case ID in the wave 2 harness pack; the wave journey runs in SIT, and the pack and its evidence format are Not specified in the source documents (GAP-0428).

### 17. Guardrails

- No business value in code: the re-appraisal interval, the deviation codes, the matched_to values, the state names and the message texts are the owners' data, read by the harness and never held as a copy.
- No personal data in logs, traces, tests or reports: the harness asserts IDs, codes and states only, the events are asserted for the absence of personal data, and no production case, party, payment or asset is copied.
- No read of another owner's tables: every read and every seed goes through the owner's contract (DP-01), the ledger is read from rwb-source-data (DP-18), and TraceAssertion fails a run that shows a cross-schema reference.
- One hop and a 2 s budget per call with a breaker per downstream, and a composition through gateway-bff where a screen would compose, so the harness fails where a screen would fail (DP-11, DP-19).
- A stub pass is never reported as a real-owner pass: the report names the contract version and whether the hop was a stub or the owner, and the gate treats a skipped hop as not green.
- A forced failure is an input to the run and never a waiver: a red hop is fixed in the owner that owns it or reported as a gap, and the run is reported failed.
- The harness never runs against UAT or production, never calls an outside system directly, and never sets a case, treatment, asset, deviation or decision state by hand.
- A repeated run must reproduce the report: a second business effect or a duplicate ledger or decision entry fails the run.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CHO-006 | A treatment record for every offer, holding its type, terms, approval and outcome | Business Requirements Epic 2, sections 3.3 and 4; Program, section 5.9 | FEAT-TRT-01 | 06 to 10 Recovery case processes | R-SET-20, R-RES-33 | TC-W2J01-01-ITG, TC-W2J01-03-ITG |
| REQ-CHO-009 | Payments received matched to the plan, the settlement or the fee; anything unmatched to the exception list | Business Requirements Epic 2, sections 3.8 and 4; Program, section 5.9 | FEAT-PAY-03, FEAT-PAY-10 | 06 to 10 Recovery case processes | R-SET-20, R-SET-21 | TC-W2J01-01-ITG, TC-W2J01-04-ITG |
| REQ-RDF-004 | Collateral records and appraisal values on the case, read through the ACE views | Business Requirements Program, section 5.1 | FEAT-VAL-01, FEAT-AST-09 | 06 to 10 Recovery case processes | R-DIS-15, R-DIS-16, R-DIS-17 | TC-W2J01-01-ITG, TC-W2J01-10-ITG |
| REQ-DVH-002 | A deviation pauses the stage clock, keeps the prescription clock running and does not replace the case state | Business Requirements Epic 2, section 4; Program, section 5.15 | FEAT-DVH-02, FEAT-DVF-03 | 11 Handle customer care and deviations | R-DEV-01, R-UNI-43 | TC-W2J01-01-ITG, TC-W2J01-09-ITG |
| REQ-DRI-005 | No action proceeds if its decision log entry cannot be written | Business Requirements Epic 1, section 4; Program, section 5.7 | FEAT-DRI-01 | All recovery processes | R-UNI-39 | TC-W2J01-08-ITG |
| REQ-ILG-005 | Every action the Workbench takes on a case writes to the ledger as it happens | Business Requirements Epic 1, section 4; Program, section 5.1 | FEAT-ILG-01 | 06 to 10 Recovery case processes | R-UNI-39 | TC-W2J01-01-ITG, TC-W2J01-04-ITG |

The features are the EP03 rows of the Epics 3 to 8 specification and the EP02 rows of the Epic 2 requirements; the requirements keep their Program and epic BRD text, and no requirement is tabulated here that a source does not give.

### 19. Out of scope

- Any production behaviour: the harness is test and evidence only. It builds no production screen, endpoint, event, workflow, Schedule or table, and it owns no table.
- The wave 2 behaviour itself, which belongs to the service stories: payment matching and clearance in rwb-payment (FEAT-PAY-03, FEAT-PAY-10), the settlement and TDR treatment and the collateral release in rwb-treatment (R-SET-20, R-SET-21, R-RES-33, FEAT-TRT-17), the asset take-on, holding and re-appraisal in rwb-asset (FEAT-AST-01 to FEAT-AST-03, FEAT-AST-05, FEAT-AST-09), the deviation handling in rwb-deviation (R-DEV-01, FEAT-DVF-03) and the outbound items in rwb-integration.
- The sibling harness stories and their own journeys: RWB-ITG-E3017-ITG for the collateral release and RWB-ITG-E3026-ITG for the re-appraisal. This story asserts those two hops only as hops of the wave 2 chain and does not restate their criteria or their test cases.
- The platform owners' behaviour: the case and its clocks (rwb-case), the ledger (rwb-source-data), the decision log (rwb-decision), the authorisation answer (rwb-access) and the composite route (the platform edge story RWB-PLT-N001-CON).
- The route decision itself, which runs on the route owner and is read here as case state and as a decision record only.
- The auction and sale legs beyond the close of the journey (FEAT-AST-10 to FEAT-AST-21), debt sale (S6), write-off (S7), guarantee (S3) and litigation (S4), all of which are later waves.
- The harness environment, the seeding set, the evidence format and retention, the gate name and its thresholds: carried as one gap and one assumption, not decided here.
