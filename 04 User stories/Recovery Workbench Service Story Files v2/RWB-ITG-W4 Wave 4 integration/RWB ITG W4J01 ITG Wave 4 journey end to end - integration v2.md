# RWB-ITG-W4J01-ITG Wave 4 journey end to end

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-W4J01-ITG |
| Work type | ITG (Integration) |
| Suggested owner | QA team (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W4 |
| Wave | 4 |
| Business epic | NEW |
| Release | None (new story) |
| Legacy key | W4J01 |
| Legacy disposition | New |
| Build status | Not started |
| Patterns applied | None |
| Parallel lane | L-ITG-W4 |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-ITG-W4J01-ITG-16); the squad sizes the story at refinement |
| Depends on (build) | None |
| Contract dependencies | Not specified in the source documents (DOR-RWB-ITG-W4J01-ITG-21) |
| Contract version | v1 (the /v1 path base in section 12.2) |
| Integration dependencies | None |
| External dependencies | None |
| Epic design sign-off | Not specified in the source documents (DOR-RWB-ITG-W4J01-ITG-14) |
| Contract fake library version | Not specified in the source documents (DOR-RWB-ITG-W4J01-ITG-22) |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: new integration harness story for the wave 4 release gate. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (24 resolved, 11 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **member of the QA team**, I want **one repeatable wave 4 end-to-end journey harness that chains the wave 4 business behaviour on one synthetic portfolio for one business date across rwb-debtsale, rwb-writeoff, rwb-partner, rwb-deviation and rwb-integration, asserting each hop through the owner's published contract and composing through gateway-bff where a screen would**, so that **the wave 4 release is accepted on evidence of the whole journey and not on five separate service test results, and a red hop stops the release instead of being found in production**.

This story builds the harness, its evidence and its gate. It builds no production screen, endpoint, event, workflow, Schedule or table, and it owns no table. The behaviour it proves is owned by the wave 4 service stories and by the platform stories of rwb-case, rwb-source-data, rwb-decision and rwb-access; the harness only drives the owners' published operations, reads the owners' published answers and records what happened.

The journey chains, in this order, the wave 4 business behaviour of EP06, EP07 and EP08 (wave map §R5.6: EP06, EP07 and EP08 are wave 4) and the two services Arch v5 slide 38 adds in this wave, S7 rwb-writeoff and S9 rwb-partner: a debt-sale lot awarded and its accounts transferred, derecognised and posted to the general ledger (R-DS-23, R-DS-30, R-DS-32, R-DS-34; the journey the sibling harness story RWB-ITG-E6008-ITG also covers); the monthly write-off scan, the committee route and decision, the posting with its provision release and the completeness check (R-WO-01, R-WO-06, R-WO-11, R-WO-21, R-WO-42; the journeys RWB-ITG-E6017-ITG and RWB-ITG-E6021-ITG also cover); a partner instruction, its recorded result, the fee claim and the partner review (REQ-S9-001, REQ-S9-004; the journeys RWB-ITG-E7012-ITG and RWB-ITG-E7013-ITG also cover); a deviation of code X5 raised mid-journey that holds the case out of the population, pauses the stage clock while the prescription clock keeps running and returns the case (R-DEV-01, R-DEV-05, R-DEV-18, R-DEV-19; the journey RWB-ITG-E7005-ITG also covers); the case closed after its retention period (REQ-S7-008, R-WO-36; the journey RWB-ITG-E6025-ITG also covers); and the EP08 hardening controls that only a whole journey can prove, the rule version in force stamped on every decision record and the hash chain of those records verified (JOB-20, JOB-14).

The journey runs on two cases of one synthetic portfolio, because a sold account and a written-off account are mutually exclusive outcomes of the same case: the account awarded in the lot stops every other open action and closes the case as sold (R-UNI-47), and the account that is written off is posted, retained and closed (R-WO-21, R-WO-36).

The five owners the journey drives are rwb-debtsale (S6), rwb-writeoff (S7), rwb-partner (S9), rwb-deviation (S8) and rwb-integration (P2). The rwb-partner hop is proved against the real owner in this wave: the instruction, its recorded result and the partner review are asserted here, because the wave map places S9 rwb-partner in wave 4; the wave 3 journey (RWB-ITG-W3J01-ITG) proves its instruction hop only against the published contract of S9 served by its fake. rwb-case, rwb-source-data, rwb-decision and rwb-access are read as the platform owners of the case state, the ledger, the decision log and the authorisation answer. The harness adds no business rule of its own: every expectation it asserts is copied from a rule, a state or an operation that a source already gives.

The harness stories are what give the QA team its Day 1 work (Template and Rules §R5.7 rule 6). W1J01 built the contract-test harness and the synthetic test data, and W2J01 is the wave 2 counterpart; this story is the wave 4 release gate of Architecture v5 slide 46, which lists contract tests per API, event and activity, Temporal replay tests and a daily journey smoke workflow and asks how the 19 services are tested as a set.

### 2. Business rationale

A service can be green on its own contract tests and still leave the wave broken, because what the final wave sells is a set of outcomes that only exist end to end. An approved write-off must leave the book once, against a general ledger reference, with the provision released and the approved population equal to the posted population (REQ-S7-005, R-WO-21, R-WO-42). A lot award must stop every open action on the case the same day, transfer the data and post the result without re-keying (REQ-S6-007, REQ-S6-008, R-UNI-47, R-DS-30). A partner fee may only be paid against a recorded result and the contracted schedule (REQ-S9-004). A bankruptcy must stop direct collection and start a claim deadline clock while the prescription clock keeps running (REQ-DVH-009, R-DEV-01, R-DEV-05). Each outcome is produced by a different owner, on a different task queue, through a different call type, and each one is only as good as the hop before it.

The wave 4 chain also crosses the platform on every hop: the case and its clocks in rwb-case, the ledger in rwb-source-data, the decision record in rwb-decision and the authorisation answer in rwb-access. So the defects this harness catches are the ones no single service test can see: an owner that answers a shape its contract does not allow, a hop that quietly grows a second call, a decision record written after the state change instead of in the same transaction (R-UNI-39, Principle 5), a point of no return taken before the central ledger confirmed the record (Arch v5 slide 28; Temporal design slide 26), a posting counted twice, a case reported posted on a partial answer, a stale ACE data product read as if it were today's, and a repeat of the same run that produces a second business effect.

The wave 4 write-off and debt-sale legs are also the two places where the design deliberately slows down: the posting and the transfer wait for the central ledger in strict mode. A harness that stubbed the ledger would never see that gate at all, which is why this story asserts it as its own criterion and not as an implementation detail.

The harness is the cheapest place to hold the wave entry check. The alternative is a manual walk-through per wave, which proves the behaviour once for one person on one day and leaves no evidence the release can be judged on. The report this harness produces is keyed by story and business date, holds one trace per run, names the contract version of every hop and holds the pass or fail the gate reads.

It meets REQ-S6-007, REQ-S6-008, REQ-S7-005, REQ-S7-008, REQ-S9-001, REQ-S9-004, REQ-S8-001, REQ-DVH-009, REQ-DRI-005 and REQ-ILG-005 at the integration level and leaves every business rule and every screen behaviour with the owning stories. The journey's business rules are R-DS-23, R-DS-30, R-DS-32, R-DS-34, R-UNI-47, R-WO-01, R-WO-06, R-WO-11, R-WO-21, R-WO-42, R-WO-43, R-WO-36, R-DEV-01, R-DEV-05, R-DEV-18, R-DEV-19, R-DEV-20, R-UNI-25, R-UNI-26, R-UNI-45 and R-UNI-39, all of which the owning services run and the harness only asserts.

### 3. Preconditions

- The harness environment, its repository, its deployment and its namespace: Not specified in the source documents (GAP-0480; ASM-0672).
- The seeded portfolio, its two cases, the lot, the accounts, the write-off, the partner and the instruction, and their identifiers: Not specified in the source documents (GAP-0480; ASM-0672). Seeding uses only the owning services' published operations, never a schema write, and the case ID keeps the form RW-YYYY-NNNNNN of REQ-CWC-002.
- The published contracts of rwb-debtsale, rwb-writeoff, rwb-partner, rwb-deviation, rwb-integration, rwb-case, rwb-source-data, rwb-decision and rwb-access are in the contract registry, and one stub set is generated from each of them, so the journey runs from Day 1 before the wave 4 app stories are live.
- The business date under test is fixed at 2027-04-30, the E6 release date of the Program release plan (Program, section 8), and the write-off cut-off month is 2027-04. Every clock the journey asserts is read from the owner and not from the harness.
- rwb-writeoff runs `WriteOffWorkflow` on task queue `rwb-writeoff` and holds the JOB-16 write-off scan Schedule on the 3rd working day of the month (Arch v5 slides 20 and 44; Temporal design slide 23); rwb-debtsale runs `DebtSaleWorkflow` on its queue, rwb-partner runs `InstructionWorkflow` and rwb-deviation runs `DeviationWorkflow`. This story observes all four and changes none.
- The topics `rwb.debtsale.events.v1`, `rwb.writeoff.events.v1`, `rwb.partner.events.v1`, `rwb.deviation.events.v1`, `rwb.payment.events.v1`, `rwb.integration.events.v1`, `rwb.decision-record.v1` and `rwb.decision.events.v1` exist with their retry and `.dlt` topics, and the consumers' inbox tables are in place (Arch v5 slides 42 and 43).
- The data products DP01 Account and arrears and DP13 Money and closure are published by rwb-source-data, with `v_ace_account` and `v_ace_write_off` as their sources and a freshness stamp, so the account position and the posting can be read back from ACE (INT-16 GL).
- The deviation code the journey raises is X5, the bankruptcy and seizure code that stops direct collection and starts the claim deadline clock (R-DEV-05, REQ-DVH-009); the handler, the SLA and the claim deadline are read from the owners and not set here.
- The retention period, the write-off eligibility and tax criteria, the partner fee schedule and the committee limit are data of their owners (FEAT-WOF-01, FEAT-WOF-02, FEAT-PRM-02, R-WO-11); the harness reads them and never holds a value.
- The evidence format, the evidence retention and the wave gate definition, including its thresholds: Not specified in the source documents (GAP-0480; ASM-0672).
- No build dependency. Day 1, against the stub set, with each stub replaced by the real owner as its wave 4 story lands.

### 4. Flow

1. Harness: loads the seeded portfolio through the owning services' published operations only: case `RW-2027-000401` on the write-off leg and case `RW-2027-000402` on the debt-sale leg, lot `LOT-SYN-2027-0401` holding the account of case `RW-2027-000402`, partner `PTR-SYN-000401`, instruction `INS-SYN-2027-0401` and deviation `DEV-SYN-000401`. It reads both cases with `GET /api/recovery/case/v1/cases/{caseId}` and the caller's rights with `GET /api/recovery/access/v1/me/session`.
2. Harness: awards the lot through `POST /api/recovery/debtsale/v1/debt-sale-lots/{lotId}/award` with one Idempotency-Key, which starts `DebtSaleWorkflow` on task queue `rwb-debtsale`, and asserts the lot answers at LOT_AWARDED under R-DS-23 with its price against the reserve as the owner returns them; it asserts `rwb.debtsale.LotAwarded.v1` (EV-23) once on `rwb.debtsale.events.v1`.
3. Harness: asserts the derecognition and the posting on the sold account: the lot answers at DERECOGNISED under R-DS-30, the general ledger posting is a readable outbound item of rwb-integration with its file run, and the posting reference is recorded once; the sold account is read through DP01 and DP13, and the transfer is asserted with `rwb.debtsale.AccountsTransferred.v1` and the buyer's money with `rwb.payment.ProceedsMatched.v1` (EV-25) on `rwb.payment.events.v1`.
4. Harness: asserts the case effect of the award on case `RW-2027-000402`: the case answers at CASE_CLOSED_SOLD under R-UNI-47, every open action on it has stopped the same day, and the lot closes at LOT_CLOSED under R-DS-34 once its claim window is closed as the owner reports it.
5. Harness: raises the X5 deviation on case `RW-2027-000401` through `POST /api/recovery/deviation/v1/cases/{caseId}/deviations` with one Idempotency-Key, which starts `DeviationWorkflow` on task queue `rwb-deviation`; it asserts `rwb.deviation.DeviationRaised.v1` (EV-06) once, the case at DEV_FLAGGED, the stage clock paused and the prescription clock still running with its date unchanged (R-DEV-01).
6. Harness: assigns the deviation through `PATCH /api/recovery/deviation/v1/deviations/{deviationId}` and asserts the case at DEV_WITH_OWNER with Legal as the handler under R-DEV-05, the claim deadline timer running for the receiver or the LED filing, and one decision record per step with its rule id and rule version.
7. Harness: runs the JOB-16 write-off scan for cut-off month 2027-04 through `POST /api/recovery/writeoff/v1/write-off-scans` with one Idempotency-Key, and asserts R-WO-01 on the population and that case `RW-2027-000401`, which carries the open X5 deviation, is held out of it and routed to the deviation handler at CASE_REMOVED_BY_TEAM under R-WO-06, while the case without a deviation is proposed in the population.
8. Harness: resolves the deviation and asserts the case returns: either RESUMED under R-DEV-18 with the stage clock resumed from the state it paused in, or ROUTE_D6 under R-DEV-19 where the outcome changes the route; it asserts `rwb.deviation.DeviationCleared.v1` (EV-07) once and that no second DeviationRaised was published for the same code.
9. Harness: re-runs the scan for the same cut-off month with the same Idempotency-Key and asserts that case `RW-2027-000401` is now in the population at POPULATION_PROPOSED, that no second population row and no second decision entry is written for any case of the month, and that the committee route of R-WO-11 puts the pack at WITH_COMMITTEE with one committee meeting timer whose expiry is the date the owner booked.
10. Harness: records the committee decision through `POST /api/recovery/writeoff/v1/write-offs/{writeOffId}/committee-decision` with one Idempotency-Key and asserts the case at POSTING_PENDING; it asserts that the point of no return is held until the central ledger in rwb-decision confirms the decision record, and that the posting then answers POSTED under R-WO-21 with one posting reference, one DP13 entry and one `rwb.writeoff.WriteOffApproved.v1` (EV-24) on `rwb.writeoff.events.v1` consumed once by rwb-case, once by rwb-payment and once by rwb-reporting.
11. Harness: asserts the completeness check of R-WO-42 on the cut-off month: the approved count and amount equal the posted count and amount, completeness is published, and the retention timer starts at RETENTION_RUNNING; where the two populations differ, R-WO-43 fires the exception at WRITEOFF_EXCEPTION and the run says so (X6).
12. Harness: drives the partner leg: it issues the instruction through `POST /api/recovery/partner/v1/cases/{caseId}/instructions` with one Idempotency-Key, reads it back with `GET /api/recovery/partner/v1/partner/instructions`, and asserts `rwb.partner.InstructionIssued.v1` (EV-20) once; it submits the result through `POST /api/recovery/partner/v1/partner/instructions/{instructionId}/results` and asserts `rwb.partner.PartnerResultSubmitted.v1` (EV-21) once and its consumption by rwb-litigation, rwb-asset and rwb-case; it submits the fee invoice through `POST /api/recovery/partner/v1/partner/instructions/{instructionId}/invoices` and reads the approval of REQ-S9-004 in the decision log, with the proceeds the fee is checked against read from `GET /api/recovery/payment/v1/proceeds`.
13. Harness: drives the partner service level path of R-UNI-25 and R-UNI-45 on the fixture clock: the missed service level is chased once and the work recalled, the re-selection re-issues one instruction for the case and restarts the partner clock, and the first partner holds no open instruction afterwards; `rwb.partner.InstructionIssued.v1` counts one publication per issue and no second publication for the recalled one.
14. Harness: asserts the partner review of the six points of REQ-S9-001 against the partner read and the instruction read, and records the action of each instruction through `POST /api/recovery/partner/v1/partner/instructions/{instructionId}/results` once per instruction.
15. Harness: asserts the close of the written-off case after its retention period: the placement term expiry starts the retention timer (R-WO-36), the case answers RETENTION_RUNNING and then CASE_CLOSED with its closed date and closure reason after the timer's expiry as the owner reports it, and no timer is left running on the case.
16. Harness: asserts the EP08 hardening controls on the same run: `rwb.decision.RulePackageInForce.v1` (EV-30) on `rwb.decision.events.v1` carried the version the run used, every decision record of the journey names the rule id and the rule version in force at its point, the hash chain of the records of both cases verifies under the JOB-14 check, and `rwb.decision.DecisionRecorded.v1` (EV-08) is on `rwb.decision-record.v1` for each hop that took a decision, confirmed by the central ledger.
17. Harness: authorises every call through the owner's answer (`GET /api/recovery/access/v1/me/session` for the caller, `POST /api/recovery/access/v1/authorise` for the check) and records the refusal path for a role without the right.
18. Harness: asserts the one-hop rule and the 2 s budget from the run trace, that no hop reads another owner's schema, and that a composition goes through the gateway-bff composite route where a screen would compose.
19. Harness: repeats the run from the same seeded state, compares the two reports assertion by assertion, and asserts that no second lot award, transfer, write-off posting, instruction, deviation, queue placement or timer was created and that the ledger and the decision log hold no duplicate entry.
20. Harness: publishes the per-run evidence report keyed by story and business date with the contract version of every hop, and holds the wave gate that reads every wave 4 harness result of the business date and fails the release when one is red.

### 5. Exception paths

| ID | Trigger | What the harness asserts | Message | ITG test case | Covered by |
|---|---|---|---|---|---|
| X1 | A hop answers a shape its published contract does not allow | The run fails at that hop before any assertion of the next hop; the report names the owner, the operation and both contract versions, and the earlier state is unchanged | None | TC-W4J01-09-ITG | AC3 |
| X2 | A hop does not answer inside the 2 s budget | The run fails at that hop and names it; the report holds the elapsed time and the contract version, and the state of the earlier hops is unchanged | MSG-GEN-006 | TC-W4J01-10-ITG | AC2 |
| X3 | The decision record of a hop cannot be written | Nothing moves: the state change, the record and the outbox row are one transaction, so the hop fails and the run is reported failed, not passed (Principle 5, R-UNI-39) | MSG-P7-003 | TC-W4J01-11-ITG | AC8 |
| X4 | A role without the right calls a hop | The hop is refused and the run fails; nothing is written and the refusal carries the message, not an empty answer | MSG-P4-002 | TC-W4J01-12-ITG | AC9 |
| X5 | An ACE data product behind a hop is stale for the business date | The hop does not treat the stale product as today's; the run fails and the report names the product and the date it carries | MSG-P1-001 | TC-W4J01-13-ITG | AC10 |
| X6 | The write-off scan is held because the tax criteria are not published, or the approved and posted populations differ | The scan or the posting does not proceed, the exception is named, and no case of the month is reported as posted | MSG-S7-001 | TC-W4J01-14-ITG | AC11 |

The report text of a failed run is for the wave entry check and is not part of the message standard. The business messages the journey produces are asserted as data on the owners' answers and are listed in section 14.

Screen states: the harness builds no screen, so it owns no empty, loading, error or no access state. The states of any screen the journey reads are the owning stories' and are not asserted here.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Runs against the published contracts and the stub set from Day 1; it waits for no wave 4 build, and each stub is replaced by its owner as the owner lands |
| Negotiable | The seed, the fixed business date, the cut-off month, the evidence format and the gate thresholds are configuration agreed at the wave entry check, not business values in code |
| Valuable | The wave 4 journey is proven as a whole before the release is accepted, which is the outcome no per-service test can give |
| Estimable | One harness runner, one stub set, one event probe, one outbound-item probe, one evidence report and one gate |
| Small | Fits in one iteration with its tests |
| Testable | Each scenario of section 7 is one automated run with a machine-checkable result, and a repeated run must reproduce it |

### 7. Acceptance criteria

```gherkin
Feature: Wave 4 journey end to end - integration harness

  Background:
    Given the business date under test is 2027-04-30 and the write-off cut-off month is 2027-04
    Given the seeded portfolio and the identifiers of its two cases, its lot, its write-off, its partner and its instruction are Not specified in the source documents (GAP-0480; ASM-0672)
    Given the published contracts of rwb-debtsale, rwb-writeoff, rwb-partner, rwb-deviation, rwb-integration, rwb-case, rwb-source-data, rwb-decision and rwb-access are in the contract registry with a stub set generated from each

  Scenario: AC1 The wave 4 journey runs green for one business date (new, D-RCV-60)
    Given the two cases have entered from the daily case list with their route and with their decision records
    When the harness runs the journey for business date 2027-04-30 across the five owners
    Then the lot is awarded and its accounts are transferred, derecognised and posted to the general ledger with one posting reference
    And the case of the sold account answers at CASE_CLOSED_SOLD and every open action on it has stopped the same day
    And the X5 deviation pauses the stage clock while the prescription clock keeps running
    And the case carrying the open deviation is held out of the write-off population and routed to its handler
    And the deviation is resolved and the case returns to the state it paused in or to the route decision
    And the write-off scan proposes the population, the pack is routed to the committee, the committee decision is recorded and the posting answers POSTED with the provision released
    And the approved and posted populations are equal and the retention timer starts
    And the written-off case closes after its retention period
    And the instruction is issued, its result recorded, the fee approved and the partner review held on the six points
    And a partner that misses its service level is chased once and recalled, and the work is re-issued once
    And the ledger read through rwb-source-data holds one entry per hop
    And every decision record of the journey names its rule id and rule version, read from rwb-decision
    And the run is green, recorded against one parent CaseWorkflow per case, with one trace

  Scenario: AC2 Each hop is one owner, one hop, a 2 s budget (new, D-RCV-60)
    Given the harness records the trace of the run
    When the harness reads every hop from the trace
    Then each hop calls exactly one owner and no owner calls a second owner inside the hop
    And each call answers inside the 2 s budget with a circuit breaker per downstream
    And no hop reads another owner's schema, and every read names a published operation
    And where a screen would compose several owners, the harness calls the gateway-bff composite route
    And no call uses the retired monolith base (DP-13)

  Scenario: AC3 A forced failure names the hop and leaves the earlier state unchanged (new, D-RCV-60)
    Given the write-off posting hop is forced to answer a shape its contract does not allow
    When the harness runs the journey for business date 2027-04-30
    Then the run stops at that hop and names rwb-writeoff, the operation and both contract versions
    And the scan, the committee route and the case carry the state they carried before the hop
    And no posting reference and no ledger entry is written
    And the run is reported failed and is never reported passed
    And the evidence report names the hop that failed

  Scenario: AC4 A repeated run produces the same evidence and no duplicate business effect (new, D-RCV-60)
    Given the first run of the journey ended green for business date 2027-04-30
    When the harness returns to the same seeded state and runs the journey again for 2027-04-30
    Then the evidence report is the same as the first run on every assertion it holds
    And no second lot award, transfer, write-off posting, instruction, deviation, queue placement or timer is created
    And the ledger and the decision log hold no duplicate entry for the journey

  Scenario: AC5 The point of no return waits for the ledger (new, D-RCV-60)
    Given the write-off posting and the debt transfer are the two points of no return of the journey
    When the central ledger in rwb-decision has not yet confirmed the decision record of the step
    Then the step does not execute and no posting reference and no transfer is written
    And the step proceeds only after the ledger confirms the record
    And where the ledger is late after confirmation, the later steps are retried and not undone

  Scenario: AC6 The EP08 hardening controls hold on the same run (new, D-RCV-60)
    Given the rule package in force for the business date was published as RulePackageInForce on rwb.decision.events.v1
    When the harness reads the decision records of both cases
    Then every record names the rule id and the rule version in force at its point
    And the hash chain of the records verifies under the JOB-14 check
    And one record edited out of the chain fails the run and names the case and the record

  Scenario: AC7 The wave gate fails the release on one red harness result (new, D-RCV-60)
    Given the wave gate reads every wave 4 harness result recorded for the business date
    When one wave 4 harness result is red
    Then the gate reports the release as failed and names the red harness and the hop that failed
    And the gate reports the release as passed only when every wave 4 harness result is green

  Scenario: AC8 A hop whose decision record cannot be written changes nothing (new, D-RCV-60)
    Given the decision record of the write-off posting hop cannot be written
    When the harness runs the journey for business date 2027-04-30
    Then the state change, the decision record and the outbox row are not written and the hop fails
    And the run is reported failed with MSG-P7-003 named in the report
    And the case carries the state it carried before the hop

  Scenario: AC9 A role without the right is refused and writes nothing (new, D-RCV-60)
    Given RW-AUDIT calls a hop that needs the officer's right
    When the access contract answers the call with no right for the role
    Then the hop is refused with MSG-P4-002 and the run fails
    And nothing is written and the refusal carries the message, not an empty answer

  Scenario: AC10 A stale ACE data product is not treated as today's (new, D-RCV-60)
    Given a data product behind a hop carries the previous business date
    When the harness runs the journey for business date 2027-04-30
    Then the hop does not treat the stale product as today's and the run fails
    And the report names the product and the date it carries with MSG-P1-001

  Scenario: AC11 A held write-off scan or differing populations proceed no case (new, D-RCV-60)
    Given the tax criteria of the cut-off month are not published or the approved and posted populations differ
    When the harness runs the write-off scan and the posting for the cut-off month
    Then the held scan or posting does not proceed and no case of the month is reported as posted
    And the exception is named, with MSG-S7-001 where the tax criteria are missing

  Scenario: AC12 A status change the model does not allow is refused (new, D-RCV-60)
    Given a case is in a state from which the state model does not allow the requested status change
    When the harness requests that status change for business date 2027-04-30
    Then the change is refused and the case keeps the state it carried before the request
    And the refusal names the message Not specified in the source documents (NEWAC-RWB-ITG-W4J01-ITG-AC10)
    And the run is reported failed and is never reported passed

  Scenario: AC13 A consumed call that fails or does not answer stops the hop (new, D-RCV-60)
    Given a hop of the journey calls a consumed owner
    When the consumed owner fails or does not answer inside the 2 s budget
    Then the hop stops, the circuit breaker for that downstream applies, and the run names the owner and the operation
    And no state change, decision record or outbox row is written for the hop and the run is reported failed
    And a call that does not answer inside the budget carries MSG-GEN-006, and the message of any other failure is Not specified in the source documents (NEWAC-RWB-ITG-W4J01-ITG-AC9)
```

The thirteen criteria are new for this harness and restate no app criterion. The criteria of the wave 4 services are owned by their own stories, and the hops that also carry a sibling harness (the derecognition of RWB-ITG-E6008-ITG, the committee route of RWB-ITG-E6017-ITG, the posting of RWB-ITG-E6021-ITG, the retention close of RWB-ITG-E6025-ITG, the X5 flow of RWB-ITG-E7005-ITG, the fee approval of RWB-ITG-E7012-ITG and the partner review of RWB-ITG-E7013-ITG) are asserted here only as hops of the wave 4 chain.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | When the best bid is at or above the reserve, the price is tested against the reserve and the 54 percent cap, the award is recorded, and the lot is awarded at LOT_AWARDED with the sale agreement and the customer notices generated | R-DS-23 |
| BR2 | When an account is awarded in a debt sale lot while on another route, every open action stops, the case closes as sold and the data is transferred the same day | R-UNI-47 |
| BR3 | When the data is transferred, the balance is derecognised at DERECOGNISED, and a rejected posting is held at POSTING_REJECTED_DS with an exception task for two working days | R-DS-30; R-DS-32 |
| BR4 | When no put-back claim is made inside the claim window, the lot closes at LOT_CLOSED and the realised recovery is recorded by lot and by buyer | R-DS-34 |
| BR5 | When the cut-off date is reached and the ALS load is complete, every open case is tested against the eligibility rule on both tracks and the tax criteria, and the population is proposed at POPULATION_PROPOSED | R-WO-01 |
| BR6 | A case with an open deviation of X1 to X7 is held out of the population and routed to the deviation handler at CASE_REMOVED_BY_TEAM | R-WO-06 |
| BR7 | When the amount is inside the write-off committee limit, the pack is routed to the committee and the meeting is scheduled at WITH_COMMITTEE | R-WO-11 |
| BR8 | When ALS and the general ledger return a reference, the posting reference is recorded and the case answers POSTED | R-WO-21 |
| BR9 | When the approved count and amount equal the posted count and amount, completeness is published and the retention timer starts at RETENTION_RUNNING; when they differ, the exception fires at WRITEOFF_EXCEPTION and the list owner is named | R-WO-42; R-WO-43 |
| BR10 | When the placement term is expired and nothing was recovered, the placement closes and the retention timer starts | R-WO-36 |
| BR11 | A deviation of code X1 to X7 pauses the stage clock, keeps the prescription clock running and routes the case to the named owner the same day | R-DEV-01 |
| BR12 | An X5 bankruptcy is assigned to Legal and filed with the official receiver or the LED before the deadline, and a breach of the deviation service level is escalated to the team manager | R-DEV-05; R-DEV-20 |
| BR13 | A resolved deviation resumes the stage clock and returns the case to the state it paused in, or reopens the route decision where the outcome changes the route | R-DEV-18; R-DEV-19 |
| BR14 | A partner that misses its service level is chased once and then has the work recalled, a panel exit recalls every open case held by that partner, and the next partner is selected on the scorecard and re-instructed inside two working days | R-UNI-25; R-UNI-26; R-UNI-45 |
| BR15 | No action proceeds if its decision log entry cannot be written; the record, the state change and the outbox row are one transaction, and a point of no return waits for the central ledger to confirm the record | REQ-DRI-005; R-UNI-39; Arch v5 slide 28; Temporal design slide 26 |

The harness asserts these fifteen rules against the owners and the published contracts; it re-implements none of them and changes no BR row.

Rule coverage: AC1 and TC-01 assert BR1 to BR10 and BR14 on the one run; BR11 to BR13 are also asserted by TC-08; BR9 is also asserted by AC11 and TC-14; BR15 is asserted by AC5 and AC8, with TC-05 and TC-11.

### 9. State transitions

The harness changes no case, lot, write-off, partner, deviation or decision state of its own. Every move below is made by the owner when the harness calls the owner's published operation, or when the owner's workflow reacts to an event the harness caused. A state the harness set by hand would prove nothing, so the report names the owner and the operation that made each move.

| Observed fact | Caused by | Asserted as |
|---|---|---|
| Lot awarded at LOT_AWARDED | rwb-debtsale, the award step of DebtSaleWorkflow | The lot answer carries the award and the price against the reserve; LotAwarded is on the topic (TC-W4J01-01-ITG) |
| Accounts transferred, derecognised and posted at DERECOGNISED then GL_POSTED | rwb-debtsale, the transfer and derecognition steps, with the posting through rwb-integration | The lot answer and DP01 and DP13 carry the transfer, the derecognition and one posting reference (TC-W4J01-01-ITG) |
| Case closed as sold at CASE_CLOSED_SOLD | rwb-case on the award event, under R-UNI-47 | The case answer carries the sold state and no open action (TC-W4J01-01-ITG) |
| Population proposed, pack routed, posting recorded at POPULATION_PROPOSED, WITH_COMMITTEE and POSTED | rwb-writeoff, WriteOffWorkflow and the JOB-16 Schedule | The case answer carries each state and the posting reference; WriteOffApproved is on the topic (TC-W4J01-01-ITG) |
| Completeness published and the retention running at RETENTION_RUNNING, then CASE_CLOSED | rwb-writeoff and rwb-case, under R-WO-42 and R-WO-36 | The case answer carries the reconciliation and the closure after the retention timer (TC-W4J01-01-ITG) |
| Deviation flagged at DEV_FLAGGED and assigned at DEV_WITH_OWNER | rwb-deviation, DeviationWorkflow | DeviationRaised is on the topic, the case answers with the flag and the handler, the stage clock is paused and the prescription date is unchanged (TC-W4J01-01-ITG) |
| Deviation resolved or rerouted at RESUMED or ROUTE_D6 | rwb-deviation and rwb-case, under R-DEV-18 and R-DEV-19 | DeviationCleared is on the topic and the stage clock resumes from the paused state (TC-W4J01-01-ITG) |
| Instruction issued, result recorded, work recalled and re-issued | rwb-partner, InstructionWorkflow | The instruction answer carries its status and its result, InstructionIssued counts one publication per issue, and the recalled partner holds no open instruction (TC-W4J01-01-ITG) |
| A hop forced to answer a shape its contract does not allow | the harness, on the stub set | The run stops at the hop and the earlier state is unchanged (TC-W4J01-09-ITG) |
| A decision record that cannot be written | the owner of the hop, whose transaction rolls back | Nothing moved and the run is failed (TC-W4J01-11-ITG) |
| A point of no return held before the ledger confirms | rwb-writeoff and rwb-debtsale, in strict mode | No posting reference and no transfer is written before the confirmation (TC-W4J01-05-ITG) |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-OFF, recovery officer | The synthetic user the harness drives: reads and drives the case through the owning contracts within the case scope of the seeded queue |
| RW-CASEOWN, case owner | Reads the case, its timers, its deviation flag and the ledger of the same seeded cases |
| RW-CREDITAD, Credit Administration officer | The role the posting and the transfer are asserted under; changes nothing itself |
| RW-WRITEOFF, write-off team member | Reads the population, the committee route and the posting of the cut-off month; changes nothing |
| RW-WOCOMM, write-off committee member | The role the committee decision is asserted under |
| RW-DEBTSALE, debt sale officer | The role the award and the lot read are asserted under |
| RW-AGENCYMG, partner and agency manager | The role the instruction, the fee claim and the partner review are asserted under |
| RW-TEAMMGR, team manager | Reads the same evidence across the queue and receives the deviation escalation; changes nothing |
| RW-AUDIT, internal audit | Reads the decision log, the hash chain and the ledger of the journey; changes nothing |
| RW-PLATADM, platform administrator | Reads the outbound items and the data product freshness the run asserts; resends nothing |
| QA lead | Owns the seeded portfolio, the fixed business date, the stub set, the evidence format and the wave gate |
| Integration lead | Owns the harness code, the trace assertions and the swap from a stub to the real owner |
| The owning services' identities | rwb-debtsale, rwb-writeoff, rwb-partner, rwb-deviation, rwb-integration, rwb-case, rwb-source-data, rwb-decision and rwb-access make every state change the harness asserts |
| No delegation of authority level applies | The harness takes no business decision; the committee decision and the fee approval inside the journey are the owning stories' |

Authorisation is answered on every call by the access contract (`POST /api/recovery/access/v1/authorise`), and the harness asserts both the allow path for RW-OFF in scope and the refusal path for a role without the right.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 to DF-CAS-023 | `recovery_case` | case_no, status, stage_code, prescription_date, deviation_open, closed_date, closure_reason | Read through the rwb-case contract |
| DF-CAS-036 to DF-CAS-045 | `deviation` | deviation_code, raised_at, paused_state, handler | Written through the rwb-deviation raise and patch, read back through the case and the timers |
| DF-WRK-027 to DF-WRK-036 | `timer` | timer_type, started_at, expires_at, paused_at | Read through the rwb-case timers contract |
| DF-SAL-020 to DF-SAL-030 | `debt_sale_lot` | lot_no, cut_off_date, buyer_partner_id, status | Read through the rwb-debtsale contract |
| DF-SAL-031 to DF-SAL-035 | `debt_sale_account` | account_key, borrower_code, outstanding | Read through the rwb-debtsale contract and DP09 |
| DF-FIN-010 to DF-FIN-020 | `write_off` | id, case_id, decision_log_id, amount, tax_criteria_met, committee_date, posted_date, responsibility_center, cost_center, gl_product, recovered_after | Read as the posting result through the case, DP13 and the decision log; written by S7 |
| DF-PRT-001 to DF-PRT-007 | `partner` | partner_code, partner_type, panel_status, contract_end | Read through the rwb-partner contract |
| DF-PRT-008 to DF-PRT-016 | `partner_instruction` | id, case_id, partner_id, instruction_type, instructed_at, due_at, status, result_code, fee_amount | Read through the rwb-partner contract |
| DF-DEC-001 to DF-DEC-018 | `decision_log_entry` | id, case_id, decision_code, rule_id, rule_version, final_call, actions, outcome, decided_at, entry_hash | Read through the rwb-decision decision-log contract |
| DF-REF-001 to DF-REF-015 | `rule_row` | rule_id, rule_version, route_set, from_state, event_code, to_state | Asserted from the decision entry (DF-DEC-004, DF-DEC-005); the rule catalogue is P7's and is not read directly here |
| DF-ACE-001 to DF-ACE-042 | `v_ace_account` | account_key, account_code, account_status, total_balance | Read through DP01 of the rwb-source-data contract only |
| DF-ACE-261 to DF-ACE-269 | `v_ace_write_off` | write_off_key, account_key, amount, posted_date, responsibility_center, cost_center, gl_product, source_system, data_as_of | Read through the P1 DP13 contract only |
| DF-INT-001 to DF-INT-013 | `interaction` | occurred_at, channel, direction, summary | Read through the rwb-source-data contract, where the run records the journey on the case timeline |

Field IDs are those of the Logical Data Model and Data Dictionary. The harness owns no table and writes no row directly: it reads through the owner's contract and its writes are the owner's published operations of §12.2, taken with one Idempotency-Key each (DP-01). Test data is synthetic; no production case, party, payment, partner or asset is copied, and no personal data is written to a report.

### 12. Contract

#### 12.1 REST operations provided

None. The harness is a test runner: it serves no operation, opens no port a service calls and publishes no endpoint.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| POST | `/api/recovery/debtsale/v1/debt-sale-lots/{lotId}/award` | S6 rwb-debtsale | Awards the seeded lot and starts DebtSaleWorkflow (AC1) |
| GET | `/api/recovery/debtsale/v1/debt-sale-lots/{lotId}` | S6 rwb-debtsale | The lot, its award, its transfer and its close (AC1) |
| POST | `/api/recovery/writeoff/v1/write-off-scans` | S7 rwb-writeoff | Runs the JOB-16 scan for cut-off month 2027-04 and its re-run (AC1, AC4) |
| POST | `/api/recovery/writeoff/v1/write-offs/{writeOffId}/committee-decision` | S7 rwb-writeoff | Records the committee decision and starts the posting (AC1, AC5) |
| POST | `/api/recovery/partner/v1/cases/{caseId}/instructions` | S9 rwb-partner | Issues the instruction to the selected partner (AC1) |
| GET | `/api/recovery/partner/v1/partner/instructions` | S9 rwb-partner | The instruction, its due date, its status and its result (AC1, AC4) |
| POST | `/api/recovery/partner/v1/partner/instructions/{instructionId}/results` | S9 rwb-partner | Records the partner result and the review action (AC1) |
| POST | `/api/recovery/partner/v1/partner/instructions/{instructionId}/invoices` | S9 rwb-partner | Submits the fee claim for approval (AC1) |
| GET | `/api/recovery/partner/v1/partners` | S9 rwb-partner | The partner, its panel status and its contract, for the six-point review (AC1) |
| POST | `/api/recovery/deviation/v1/cases/{caseId}/deviations` | S8 rwb-deviation | Raises the X5 deviation through its owner (AC1) |
| PATCH | `/api/recovery/deviation/v1/deviations/{deviationId}` | S8 rwb-deviation | Assigns, escalates and resolves the deviation (AC1) |
| GET | `/api/recovery/integration/v1/admin/outbound-items` | P2 rwb-integration | The general ledger posting, the data transfer and the buyer file (AC1, X1) |
| POST | `/api/recovery/integration/v1/admin/outbound-items/{itemId}/resend` | P2 rwb-integration | The single re-post of a rejected posting (AC5, X6) |
| GET | `/api/recovery/payment/v1/proceeds` | P8 rwb-payment | The proceeds the lot, the fee and the recovery are checked against (AC1) |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The state of both cases at every hop (AC1, AC3) |
| GET | `/api/recovery/case/v1/cases/{caseId}/timers` | P3 rwb-case | The two clocks, the committee timer and the retention timer (AC1) |
| GET | `/api/recovery/case/v1/queues` | P3 rwb-case | The committee queue and the case queue the population moves between (AC1) |
| GET | `/api/recovery/case/v1/queues/{queueId}/cases` | P3 rwb-case | The case is in the committee queue and no longer in its source queue (AC1) |
| GET | `/api/recovery/source-data/v1/data-products/DP13/records?caseId={caseId}` | P1 rwb-source-data | The ledger entries and the posting of the journey (AC1, X5) |
| GET | `/api/recovery/source-data/v1/data-products/DP01/records?caseId={caseId}` | P1 rwb-source-data | The account position and the derecognised status (AC1) |
| GET | `/api/recovery/source-data/v1/data-products/freshness?product=DP13` | P1 rwb-source-data | The business date and the load time behind the read (X5) |
| GET | `/api/recovery/decision/v1/decision-log?caseId={caseId}` | P7 rwb-decision | The decision record of every hop, its rule id and its rule version (AC1, AC3, AC6) |
| GET | `/api/recovery/access/v1/me/session` | P4 rwb-access | The caller's rights for the run (X4) |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | The role, scope and right check on every call, including the refusal path (X4) |

Every operation is one hop on the owner's base `/api/recovery/<short>/v1` with a 2 s budget and a circuit breaker per downstream; where a screen would compose several owners, the harness calls the gateway-bff composite route. The composite route paths and their merge order are Not specified in the source documents (GAP-0480; ASM-0672).

No operation is invented in this story: each path and each owner is the row the Ownership Map gives. Where an owner publishes no read for its own record (the write-off record and the deviation record), the harness identifies the record through the case, DP13, the instruction read and the decision log, and names the owning app story's own read rather than restating a path here.

#### 12.3 Events published

None. The harness publishes no Kafka event; it consumes the owners' events and writes its evidence report to the wave record.

#### 12.4 Events consumed

| Event | Topic | Producer | What the harness asserts |
|---|---|---|---|
| `rwb.debtsale.LotAwarded.v1` (EV-23) | `rwb.debtsale.events.v1` | S6 rwb-debtsale | The award fact for the lot of the case, keyed by caseId, present once inside the run window |
| `rwb.debtsale.AccountsTransferred.v1` (event catalogue A3, row "+") | `rwb.debtsale.events.v1` | S6 rwb-debtsale | The transfer fact for the sold accounts before the derecognition is asserted |
| `rwb.payment.ProceedsMatched.v1` (EV-25) | `rwb.payment.events.v1` | P8 rwb-payment | The buyer's money matched to the lot and to the case |
| `rwb.writeoff.WriteOffApproved.v1` (EV-24) | `rwb.writeoff.events.v1` | S7 rwb-writeoff | The approval fact of the posting, consumed once by rwb-case, rwb-payment and rwb-reporting |
| `rwb.partner.InstructionIssued.v1` (EV-20) | `rwb.partner.events.v1` | S9 rwb-partner | One fact per issue, including the re-issue after the recall |
| `rwb.partner.PartnerResultSubmitted.v1` (EV-21) | `rwb.partner.events.v1` | S9 rwb-partner | The result fact, consumed once by rwb-litigation, rwb-asset and rwb-case |
| `rwb.deviation.DeviationRaised.v1` (EV-06) | `rwb.deviation.events.v1` | S8 rwb-deviation | One fact for the X5 flag, with its code |
| `rwb.deviation.DeviationCleared.v1` (EV-07) | `rwb.deviation.events.v1` | S8 rwb-deviation | One fact for the return of the case, consumed once by rwb-case and rwb-comms |
| `rwb.decision.RulePackageInForce.v1` (EV-30) | `rwb.decision.events.v1` | P7 rwb-decision | The rule version the run used, and the cache refresh it started (AC6) |
| `rwb.decision.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | all 19 services | One record per hop that took a decision, arriving before the record is read from the central ledger |
| `rwb.integration.FileDelivered.v1` (event catalogue A3, row "+") | `rwb.integration.events.v1` | P2 rwb-integration | The buyer file of the sold lot and the posting file of the write-off, delivered once |

The events carry IDs and business facts only, keyed by caseId, and the harness asserts the absence of personal data in each one (DP-09). Order per case is guaranteed by the case key, and every state the harness asserts is read from the owner's contract and never reconstructed from a topic.

#### 12.5 Workflows and activities

None added. The harness starts no workflow, adds no activity and owns no task queue. It exercises the existing parent CaseWorkflow in rwb-case (one per case, entry to closure, with a child workflow per stage) and the stage children the journey needs: DebtSaleWorkflow on the rwb-debtsale queue, WriteOffWorkflow on the rwb-writeoff queue, InstructionWorkflow on the rwb-partner queue and DeviationWorkflow on the rwb-deviation queue, which can start at any time and pauses the stage clock. It exercises the delivery steps that run as activities on rwb-integration's queue and asserts their effect as outbound items. No workflow, activity or Schedule is created, changed or owned by this story (DP-10, DP-12).

#### 12.6 Schedules

None added. JOB-16 Write-off scan (monthly, 3rd working day, rwb-writeoff) is exercised for cut-off month 2027-04, JOB-20 Rule promote (00:01, rwb-decision) is exercised for the rule version in force on the business date, and JOB-14 Hash-chain check (02:00, rwb-decision) is exercised for the chain of both cases. No cron, overlap policy or catch-up window is set, changed or owned by this story (DP-10).

#### 12.7 Tables owned

None. The harness owns no schema and no table (DP-01). It reads the cases through rwb-case, the ledger and both data products through rwb-source-data (DP-05, DP-18), the decision record and the rule versions through rwb-decision, the sold accounts and the lot through rwb-debtsale, the posting result through DP13, the partner and the instruction through rwb-partner and the deviation through its two published operations; it never reads another owner's tables and never writes a row.

#### 12.8 Contract fakes

| Fake | Contract | Use in the run |
|---|---|---|
| WireMock stub for rwb-debtsale | `POST /debt-sale-lots/{lotId}/award`, `GET /debt-sale-lots/{lotId}`, `rwb.debtsale.events.v1` | Day-1 run of the award, the transfer, the derecognition and the lot close before the wave 4 app story is live |
| WireMock stub for rwb-writeoff | `POST /write-off-scans`, `POST /write-offs/{writeOffId}/committee-decision`, `rwb.writeoff.events.v1` | Day-1 run of the scan, the committee route and the posting, and the held scan of X6 |
| WireMock stub for rwb-partner | `GET /partners`, `POST /cases/{caseId}/instructions`, `GET /partner/instructions`, `POST /partner/instructions/{instructionId}/results`, `POST /partner/instructions/{instructionId}/invoices` | Day-1 run of the instruction, the result, the fee claim, the recall and the review |
| WireMock stub for rwb-deviation | `POST /cases/{caseId}/deviations`, `PATCH /deviations/{deviationId}` | Day-1 run of the X5 raise, the assignment, the escalation and the return |
| WireMock stub for rwb-integration | `GET /admin/outbound-items`, `POST /admin/outbound-items/{itemId}/resend` | Day-1 assertions on the posting, the transfer, the buyer file and the single re-post |
| WireMock stub for rwb-payment | `GET /proceeds` | Day-1 assertions on the buyer's money and the recovery the fee is checked against |
| WireMock stub for rwb-case | `GET /cases/{caseId}`, `GET /cases/{caseId}/timers`, `GET /queues`, `GET /queues/{queueId}/cases` | Day-1 assertions on the states, the two clocks, the committee timer and the queue placement |
| WireMock stub for rwb-source-data | `GET /data-products/{productCode}/records`, `GET /data-products/freshness` | Day-1 assertions on the ledger entries, the account position and the stale product of X5 |
| WireMock stub for rwb-decision | `GET /decision-log` | Day-1 assertions on the records, the rule versions and the hash chain, and the forced failure of X3 |
| WireMock stub for rwb-access | `GET /me/session`, `POST /authorise` | Day-1 authorisation and the refusal path of X4 |

Each stub is generated from the published contract and its version is pinned in the run report, so a contract change shows up as a run failure and not as a silent pass. The evidence format, the evidence retention, the wave gate definition and its thresholds, and the seeding set are Not specified in the source documents (GAP-0480; ASM-0672).

#### 12.9 Call-type summary

| Call type | In this story |
|---|---|
| REST | 0 provided, 24 consumed, one hop each on `/api/recovery/<short>/v1` with a 2 s budget and a breaker per downstream, composed through gateway-bff where a screen would (AC1, AC2, X1, X2, X4) |
| Kafka | None published; eleven events consumed for assertion, `rwb.debtsale.LotAwarded.v1`, `rwb.debtsale.AccountsTransferred.v1`, `rwb.payment.ProceedsMatched.v1`, `rwb.writeoff.WriteOffApproved.v1`, `rwb.partner.InstructionIssued.v1`, `rwb.partner.PartnerResultSubmitted.v1`, `rwb.deviation.DeviationRaised.v1`, `rwb.deviation.DeviationCleared.v1`, `rwb.decision.RulePackageInForce.v1`, `rwb.decision.DecisionRecorded.v1` and `rwb.integration.FileDelivered.v1` (AC1, AC6) |
| Temporal | None added; the parent CaseWorkflow of each case and the debt sale, write-off, partner and deviation stage children exercised, with JOB-16, JOB-20 and JOB-14 (AC1, AC6) |
| File | None written. The buyer file and the posting file are asserted as outbound items and as delivery events of rwb-integration, and the evidence report is a harness artefact and not a service file (AC1) |

### 13. Solution plan

**Pattern application**

None. This story applies no decoupling pattern of §R5.5; it reads each owner through that owner's published contract and records the result.

The harness holds the architecture as an assertion, not as a pattern it applies: it calls one owner per hop on that owner's base and fails a run whose trace shows a call chain deeper than the gateway and one owner (DP-11), it composes through the gateway-bff composite route where a screen would (DP-19), it reads the ledger from rwb-source-data and not from a table (DP-18), it reads the decision record and the rule version from rwb-decision (DP-03) and the authorisation answer from rwb-access, and it fails a run that finds a cross-schema read (DP-01). Because the patterns belong to the services, this story's metadata Patterns applied row is None and the tables above name only owners the ownership map gives.

The harness is the wave 4 release gate. The wave 4 business epics are EP06, EP07 and EP08 (§R5.6), the wave is delivered by the S7 and S9 service epics and the integration epic, and no release is accepted on five separate green service runs. The gate reads every wave 4 harness result recorded for the business date, the sibling harness stories included, and it passes the release only when every one of them is green. Its thresholds, its name and its evidence format are Not specified in the source documents (GAP-0480; ASM-0672).

**Harness components**

| Component | Type | Responsibility |
|---|---|---|
| JourneyRunner | Job | Runs the journey once per business date in hop order across the two cases, holds the run lock and stops the run at the first failed hop |
| OwnerClient | Harness adapter | Calls the twenty-four consumed operations of §12.2, one hop each, with the 2 s budget and the Idempotency-Key header where the operation requires one |
| StubSet | Fake | The ten WireMock stubs generated from the published contracts, each with its version pinned in the report |
| EventProbe | Service | Consumes the eleven events of §12.4 and asserts each fact for its case inside the run window, including the absence of personal data |
| OutboundItemProbe | Assertion | Asserts the general ledger posting, the data transfer and the buyer file as readable outbound items of rwb-integration, each with its file run |
| QueueAndTimerProbe | Assertion | Reads the queues, the committee timer, the retention timer, the stage clock and the prescription clock, and fails the run when a placement or a clock is missing or moved |
| LedgerGateProbe | Assertion | Fails a point of no return that executes before the central ledger confirmed the decision record, and passes it only after the confirmation |
| TraceAssertion | Assertion | Fails the run on a call chain deeper than the gateway and one owner, on a call outside the 2 s budget, and on any cross-schema reference in the trace |
| HardeningProbe | Assertion | Reads every decision record of both cases, asserts the rule version in force at each point and verifies the hash chain under the JOB-14 check (AC6) |
| RepeatProbe | Assertion | Compares a repeated run from the same seed assertion by assertion, and fails on a second business effect or a duplicate ledger or decision entry |
| WaveGate | Reporter | Writes the per-run evidence report keyed by story and business date and holds the pass or fail the wave entry check reads |

**Environment and test data**

- Environment: the harness environment and its repository are Not specified in the source documents (GAP-0480; ASM-0672). The run is against the §12.8 stub set from Day 1 and against each real owner as its wave 4 story lands.
- Data: the seeded portfolio, its two cases, its lot, its write-off, its partner and its instruction are Not specified in the source documents (GAP-0480; ASM-0672). The case IDs keep the form RW-YYYY-NNNNNN of REQ-CWC-002, the business date under test is fixed at 2027-04-30 and the cut-off month at 2027-04, and the deviation is X5 as R-DEV-05 gives it. No production record is copied.
- Reset: each run starts from the same seeded state and the same fixed business date, so a repeated run is deterministic and the two reports are comparable assertion by assertion.
- Seeding: through the owners' published operations only, never a schema write, so the seeded state is one the services themselves accept.

**Build steps**

1. Generate the ten stubs from the published contracts, pin each contract version in the report, and prove the journey runs green against the stub set from Day 1 (X1).
2. Build JourneyRunner and OwnerClient with the hop order of §4, the 2 s budget, the breaker per downstream and the run lock.
3. Add the debt-sale leg: the award, the transfer, the derecognition, the posting reference and the lot close, and assert the CASE_CLOSED_SOLD effect of R-UNI-47.
4. Add the write-off leg: the JOB-16 scan for cut-off month 2027-04, the R-WO-06 hold of the case with the open deviation, the committee route of R-WO-11 and the single re-run of the same key.
5. Add the committee decision and the posting with LedgerGateProbe, and assert POSTED, the provision release, the single posting reference and the single WriteOffApproved per consumer (AC5).
6. Add the completeness check of R-WO-42 and the exception of R-WO-43, and the close after the retention period of R-WO-36.
7. Add the partner leg: the instruction, the result, the fee claim and the review, then the recall and re-issue path of R-UNI-25 and R-UNI-45 with the fixture clock.
8. Add the deviation leg: the X5 raise, the assignment to Legal, the claim deadline timer, the escalation of R-DEV-20 and the return of R-DEV-18 or R-DEV-19.
9. Add the ledger and decision-record assertions and the access path, with the refusal path of X4.
10. Add HardeningProbe: the rule version in force on every record, the RulePackageInForce publication and the hash-chain verification of both cases (AC6).
11. Add TraceAssertion, the forced bad shape of AC3, the timeout of X2 and the stale product of X5, and prove a forced failure names the hop and leaves the earlier state unchanged.
12. Add RepeatProbe and prove the repeated run reproduces the report with no duplicate business effect.
13. Add WaveGate, read every wave 4 harness result of the business date, and prove the release fails when one of them is red.
14. Swap one stub for its real owner as each wave 4 story lands, rerunning the journey after each swap, and report a stub pass as a stub pass and never as a real-owner pass.

**Gate definition.** The gate reads the wave 4 harness results recorded for the business date and passes the release only when every one of them is green; one red harness fails the release and names the harness and the hop. The gate's name, its evidence format and retention, and any threshold beyond all-green are Not specified in the source documents (GAP-0480; ASM-0672).

**Feature switch.** The harness has no production feature flag and runs in the test environment only. The wave 4 behaviour it exercises is switched on by the wave 4 stories' own flags; where a flag holds a behaviour off, the run reports the hop as skipped and the gate treats a skipped hop as not green.

**Done when.** The tests of section 16 pass; the journey runs green for business date 2027-04-30 against the stub set on Day 1 and again, hop by hop, against each real owner as its wave 4 story lands; the report holds one trace, the contract version of every hop and every assertion of section 7; and the wave gate fails the release on one red harness result and passes it on all green.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S7-001 | The write-off scan is held because the tax criteria are not published | The scan is on hold until Finance publishes the tax criteria. |
| MSG-S8-001 | The X5 deviation is raised and the case is with its handler | {deviation} was raised. The case is with {handler}. |
| MSG-P7-003 | The decision record of a hop cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | A role without the right calls a hop | You cannot {action} here. Your role does not include it. |
| MSG-P1-001 | An ACE data product behind a hop is stale for the business date | {product} is from {date}. Today's load has not arrived. |
| MSG-GEN-006 | A system of record behind a hop does not answer inside the budget | {system} is not available. Your request is queued and will be retried. |

The harness produces none of these messages itself: it asserts the message the owning service returns and names the message ID in the report, so a failed run points at an owner, an operation and a message and not only at a date. MSG-S8-001 is asserted with the deviation and Legal as the handler when the X5 flag is raised, and MSG-S7-001 with the transcription the scan answers when the tax criteria are missing (X6). Thai text for each message follows decision DL10, which is still open; its assumptions ASM-2250, ASM-2357, ASM-2377 and ASM-2863 are confirmed by the programme directive.

### 15. Screens and states

The harness renders no screen and opens no page. Where a screen would compose several owners, the harness calls the gateway-bff composite route and asserts the answer the screen consumes, so a green hop means the screen has the right data behind it:

| Screen | State | What the harness asserts |
|---|---|---|
| SCR-25 Lot builder and SCR-26 Award | Lot awarded and transferred | The lot answer carries its award, the transfer and the posting reference, and the case of the sold account answers at CASE_CLOSED_SOLD |
| SCR-25 Lot builder | Empty, loading, error, no access | Not specified in the source documents (CG-ALL-1262) |
| SCR-26 Award | Empty, loading, error, no access | Not specified in the source documents (CG-ALL-1263) |
| SCR-27 Write-off proposal | Population, committee and posting | The case answers at POPULATION_PROPOSED, WITH_COMMITTEE, POSTING_PENDING, POSTED and RETENTION_RUNNING, and the posting and the completeness read from DP13 and the decision log |
| SCR-27 Write-off proposal | Empty, loading, error, no access | Not specified in the source documents (CG-ALL-1264) |
| SCR-06 Raise deviation and SCR-08 Deviation queue | On hold for X5 | The X5 flag with the code, the handler, the paused stage clock, the running prescription clock and the claim deadline timer (MSG-S8-001) |
| SCR-06 Raise deviation | Empty, loading, error, no access | Not specified in the source documents (CG-ALL-1260) |
| SCR-08 Deviation queue | Empty, loading, error, no access | Loading as Screen Specifications v1 SCR-08 gives it; empty, error and no access: Not specified in the source documents (CG-ALL-1261) |
| SCR-34 Partner list and SCR-35 Placement and allocation | Instruction issued, recalled and reviewed | The instruction answer carries its due date, its status and its result, the recalled partner holds no open instruction, and the review records one action per instruction |
| SCR-34 Partner list | Empty, loading, error, no access | Loading as Screen Specifications v1 SCR-34 gives it; empty, error and no access: Not specified in the source documents (CG-ALL-1265) |
| SCR-35 Placement and allocation | Empty, loading, error, no access | Loading as Screen Specifications v1 SCR-35 gives it; empty, error and no access: Not specified in the source documents (CG-ALL-1266) |

The screen behaviour of each state stays with the wave 4 app stories. What the wave entry check reads instead is the evidence report. The harness environment, seed, evidence format, retention and gate are agreed with QA and the integration lead at the wave entry check and are Not specified in the source documents (GAP-0480) until then; the harness builds against the stub set until each owner lands (ASM-0672).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-W4J01-01-ITG | AC1, BR1 to BR14 | End to end | Business date 2027-04-30, seeded portfolio through award, transfer, derecognition, posting, scan, committee, write-off posting, completeness, instruction, result, fee, deviation, recall and close |
| TC-W4J01-02-ITG | AC2 | Component | Run trace of the AC1 run; one owner per hop, 2 s budget, no cross-schema read, gateway-bff composition |
| TC-W4J01-03-ITG | AC3 | Integration | Write-off posting hop forced to answer a shape its contract does not allow |
| TC-W4J01-04-ITG | AC4 | Integration | The same seeded state run twice on 2027-04-30 |
| TC-W4J01-05-ITG | AC5, BR15 | Integration | Central ledger delayed for the posting and for the transfer; no reference and no transfer written before the confirmation |
| TC-W4J01-06-ITG | AC6 | Component | Decision records of both cases read against the rule version in force, and one record edited out of the chain |
| TC-W4J01-07-ITG | AC7 | End to end | Every wave 4 harness result recorded for the business date, one of them red |
| TC-W4J01-08-ITG | BR11 to BR13 | Integration | X5 raise, assignment, SLA breach, resolution and reroute on the fixture clock |
| TC-W4J01-09-ITG | AC3, X1 | Component | Contract version mismatch and a shape outside the OpenAPI document on one hop |
| TC-W4J01-10-ITG | AC2, X2 | Integration | One hop delayed past the 2 s budget |
| TC-W4J01-11-ITG | AC8, X3, BR15 | NFR | Decision record write forced to fail on ten hops; no state changes |
| TC-W4J01-12-ITG | AC9, X4 | Component | RW-AUDIT calls a hop that needs the officer's right; refused with MSG-P4-002 |
| TC-W4J01-13-ITG | AC10, X5 | Integration | Data product behind a hop carries the previous business date; MSG-P1-001 |
| TC-W4J01-14-ITG | AC11, X6 | Integration | Scan held for the unpublished tax criteria, and a month whose approved and posted populations differ |
| TC-W4J01-15-ITG | AC12 | Integration | Status change the state model does not allow, requested by the harness; test detail Not specified in the source documents (NEWAC-RWB-ITG-W4J01-ITG-AC10) |
| TC-W4J01-16-ITG | AC13 | Integration | Consumed owner fails or does not answer inside the 2 s budget; test detail Not specified in the source documents (NEWAC-RWB-ITG-W4J01-ITG-AC9) |

The full test, with its Given, When and Then, is held under the same test case ID in the wave 4 harness pack; its pack, environment and evidence format are Not specified in the source documents (GAP-0480; ASM-0672).

### 17. Guardrails

- No business value in code: the eligibility and tax criteria, the committee limit, the retention period, the fee schedule, the deviation codes, the state names and the message texts are the owners' data, read by the harness and never held as a copy.
- No personal data in logs, traces, tests or reports: the harness asserts IDs, codes and states only, the events are asserted for the absence of personal data, and no production case, party, payment, partner or asset is copied.
- No read of another owner's tables: every read and every seed goes through the owner's contract (DP-01), the ledger and both data products are read from rwb-source-data (DP-05, DP-18), and TraceAssertion fails a run that shows a cross-schema reference.
- Nothing irreversible is proven by a shortcut: the point of no return is asserted only through the owners' operations and only after the central ledger confirms the record, so the harness never fabricates a posting or a transfer (R-UNI-39, Arch v5 slide 28).
- One hop and a 2 s budget per call with a breaker per downstream, and a composition through gateway-bff where a screen would compose, so the harness fails where a screen would fail (DP-11, DP-19).
- A stub pass is never reported as a real-owner pass: the report names the contract version and whether the hop was a stub or the owner, and the gate treats a skipped hop as not green.
- A forced failure is an input to the run and never a waiver: a red hop is fixed in the owner that owns it or reported as a gap, and the run is reported failed.
- The harness never runs against UAT or production, never calls an outside system directly, and never sets a case, lot, write-off, instruction or deviation state by hand.
- A repeated run must reproduce the report: a second business effect or a duplicate ledger or decision entry fails the run.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-S6-007 | An account awarded in a lot stops every other open action on its case the same day | Business Requirements Program, section 5.13 | FEAT-DBS-09, FEAT-DBS-14 | 4 Work the route; 6 Close | R-DS-23, R-UNI-47 | TC-W4J01-01-ITG, TC-W4J01-04-ITG |
| REQ-S6-008 | Data transfer, derecognition and the general ledger posting follow the award without re-keying | Business Requirements Program, section 5.13 | FEAT-DBS-11, FEAT-DBS-12 | 4 Work the route; 5 Collect | R-DS-30, R-DS-32, R-DS-34 | TC-W4J01-01-ITG, TC-W4J01-05-ITG |
| REQ-S7-005 | Approved write-offs post to the core system and the general ledger, the provision is released, and completeness is published | Business Requirements Program, section 5.14 | FEAT-WOF-09, FEAT-WOF-11 | 4 Work the route; 5 Collect | R-WO-21, R-WO-42, R-WO-43 | TC-W4J01-01-ITG, TC-W4J01-03-ITG, TC-W4J01-14-ITG |
| REQ-S7-008 | A case closes after its retention period | Business Requirements Program, section 5.14 | FEAT-WOF-13 | 6 Close | R-WO-36 | TC-W4J01-01-ITG |
| REQ-S9-001 | Every partner type is managed on the same six points | Business Requirements Program, section 5.16 | FEAT-PRM-01, FEAT-PRM-10 | 4 Work the route | R-UNI-25, R-UNI-26 | TC-W4J01-01-ITG, TC-W4J01-08-ITG |
| REQ-S9-004 | Fees are calculated from the contracted schedule and paid against recorded results | Business Requirements Program, section 5.16 | FEAT-PRM-07, FEAT-PRM-09 | 5 Collect | R-DS-34, R-UNI-45 | TC-W4J01-01-ITG |
| REQ-S8-001 | Each of X1 to X7 runs end to end with its own flow, approver, contact rules and return point | Business Requirements Program, section 5.15 | FEAT-DVF-05 | 4 Work the route | R-DEV-01, R-DEV-05, R-DEV-18, R-DEV-19, R-DEV-20 | TC-W4J01-01-ITG, TC-W4J01-08-ITG |
| REQ-DVH-009 | A bankruptcy or external seizure stops direct collection and starts the claim deadline clock | Business Requirements Program, section 5.15 | FEAT-DVF-05 | 4 Work the route | R-DEV-01, R-DEV-05 | TC-W4J01-01-ITG, TC-W4J01-08-ITG |
| REQ-DRI-005 | No action proceeds if its decision log entry cannot be written | Business Requirements Program, section 5.7 | FEAT-DRI-01 | All recovery processes | R-UNI-39 | TC-W4J01-03-ITG, TC-W4J01-11-ITG |
| REQ-ILG-005 | Every action the Workbench takes on a case writes to the ledger as it happens | Business Requirements Program, section 5.1 | FEAT-ILG-01 | All recovery processes | R-UNI-39 | TC-W4J01-01-ITG, TC-W4J01-04-ITG |

The features are the EP06 and EP07 rows of the Epics 3 to 8 specification and the EP01 and EP07 rows of the Program requirements; the requirements keep their Program BRD text, and no requirement is tabulated here that a source does not give. The L3 process names are the six journey steps of Architecture v5 slide 3, and "All recovery processes" is used where a rule applies at every step.

### 19. Out of scope

- Any production behaviour: the harness is test and evidence only. It builds no production screen, endpoint, event, workflow, Schedule or table, and it owns no table.
- The wave 4 behaviour itself, which belongs to the service stories: the lot award, the transfer, the derecognition and the general ledger posting in rwb-debtsale (R-DS-23, R-DS-30, R-DS-32, R-DS-34), the scan, the committee route, the posting and the completeness check in rwb-writeoff (R-WO-01, R-WO-11, R-WO-21, R-WO-42), the instruction, the result, the fee and the review in rwb-partner (REQ-S9-001, REQ-S9-004), the deviation handling in rwb-deviation (R-DEV-01, R-DEV-05, R-DEV-18 to R-DEV-20) and the outbound items in rwb-integration.
- The sibling harness stories and their own journeys: RWB-ITG-E6008-ITG for the derecognition and the posting, RWB-ITG-E6017-ITG and RWB-ITG-E6021-ITG for the committee route and the posting, RWB-ITG-E6025-ITG for the retention close, RWB-ITG-E7005-ITG for the X5 flow, RWB-ITG-E7012-ITG for the fee approval and RWB-ITG-E7013-ITG for the partner review. This story asserts those hops only as hops of the wave 4 chain and does not restate their criteria or their test cases.
- The platform owners' behaviour: the case and its clocks (rwb-case), the ledger, both data products and their freshness (rwb-source-data), the decision log, the central ledger, the rule versions and the hash chain (rwb-decision), the authorisation answer (rwb-access) and the composite route (the platform edge story RWB-PLT-N001-CON).
- The other deviations X1 to X4, X6 and X7, which have their own harness stories of the wave 4 folder; this journey asserts X5 only.
- The EP08 administration and hardening stories themselves (the rule change, the QA sample, the broken-chain detection, the regulatory returns and the autonomy step-ups): this story evidences the version stamping and the hash chain of its own run and leaves the controls to those stories.
- The cutover and migration harnesses of the wave 4 folder (RWB-ITG-DM003-ITG to RWB-ITG-DM013-ITG) and the non-functional harnesses of RWB-ITG-NFR.
- The harness environment, the seeding set, the evidence format and retention, the gate name and its thresholds: carried as one gap and one assumption, not decided here.

