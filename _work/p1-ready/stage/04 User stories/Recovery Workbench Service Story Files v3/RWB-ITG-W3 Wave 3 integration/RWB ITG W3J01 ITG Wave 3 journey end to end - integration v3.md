# RWB-ITG-W3J01-ITG Wave 3 journey end to end

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Version 3 changes** (D-RCV-60 P1 developer readiness, RD-P1 register)

- Reconciliation is a child workflow of `AceIngestCheck`, not started by consuming `AceDataReady` (RD-P1-040).
- `AceDataReady` grain, key and payload stated.
- Finishing pass: message English aligned to Error and Message Standard v6 (RD-P1-004).

| Item | Value |
|---|---|
| Story key | RWB-ITG-W3J01-ITG |
| Work type | ITG (Integration) |
| Suggested owner | QA team (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W3 |
| Wave | 3 |
| Business epic | NEW |
| Release | None (new story) |
| Legacy key | W3J01 |
| Legacy disposition | New |
| Build status | Not started |
| Patterns applied | None |
| Parallel lane | L-ITG-W3 |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-ITG-W3J01-ITG-16); the squad sizes it at refinement |
| Depends on (build) | None |
| Contract dependencies | RWB-ITG-W3J01-CON |
| Contract version | v1 (path version of every consumed operation; contract number Not specified in the source documents (DOR-RWB-ITG-W3J01-ITG-23)) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |
| Readiness decisions | RD-P1-003, RD-P1-040, RD-P1-004 |

**Change log.** D-RCV-60, 22 November 2026: new integration harness story for the wave 3 release gate. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-ITG-W3J01-ITG). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (22 resolved, 7 cross-document, 2 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **member of the QA team**, I want **one repeatable wave 3 end-to-end journey harness that chains the wave 3 business behaviour on one case for one business date across rwb-valuation with SVAF, rwb-payment, rwb-source-data, rwb-integration, rwb-guarantee, rwb-comms, rwb-litigation and rwb-partner, asserting each hop through the owner's published contract and composing through gateway-bff where a screen would**, so that **the wave 3 release is accepted on evidence of the whole journey and not on five separate service test results, and a red hop stops the release instead of being found in production**.

This story builds the harness, its evidence and its gate. It builds no production screen, endpoint, event, workflow, Schedule or table, and it owns no table. The behaviour it proves is owned by the wave 3 service stories and by the platform stories of rwb-case, rwb-source-data, rwb-decision and rwb-access; the harness only drives the owners' published operations, reads the owners' published answers and records what happened.

W3J01 is a new story with no legacy counterpart. Its criteria are new under D-RCV-60 and its chain is built from the wave 3 legacy keys: RWB-E4-001 and RWB-E4-002 for the appraisal order and the appraisal value, RWB-E4-045 for the fees and charges, RWB-E4-050 for the daily reconciliation, RWB-E4-046 for the settlement booking, RWB-E4-047 for the general ledger posting, the guarantee claim of the wave 3 guarantee key, RWB-E5-002 for the proof of delivery and RWB-E5-009 for the instruction to the firm. No legacy story owns a wave 3 journey, so no legacy acceptance criterion is carried into this story.

The journey chains, in this order, only the wave 3 business behaviour of EP04 and EP05 (wave map §R5.6: EP04 and EP05 are wave 3): an appraisal is ordered when the last one is older than the limit and the order leaves through rwb-integration to SVAF; the appraisal value is received from SVAF into ACE and accepted by the case owner through rwb-valuation; fees and charges are worked out by rwb-payment from the fee tables held as data; the money movements of the business date are reconciled against the ACE payment and write-off rows with the outcome by rec_code and business date (legacy RWB-E4-050, REC-04, REC-05 and REC-06); a settlement is booked to ALS through rwb-integration and the booked position is read back from ACE; the settlement and sale entries are posted to the general ledger through rwb-integration with the posting reference recorded on the proceeds; a guarantee claim is filed in rwb-guarantee inside its deadline; the proof of delivery is recorded on a notice and the case moves with the notice period started (legacy RWB-E5-002, R-LIT-07); and the instruction and the pack are sent to the firm with the partner clock started (legacy RWB-E5-009, R-LIT-24 and R-LIT-26).

The owners the journey drives are S1 rwb-valuation, P8 rwb-payment, P1 rwb-source-data, P2 rwb-integration, S3 rwb-guarantee, P6 rwb-comms, S4 rwb-litigation and S9 rwb-partner, with S2 rwb-treatment and S7 rwb-writeoff read on the two legs the chain touches. rwb-case, rwb-decision and rwb-access are read as the platform owners of the case state and its clocks, the decision log and the authorisation answer. The harness computes no business rule of its own: every expectation it asserts is copied from a rule, a state or an operation that a source already gives.

The harness stories are what give the QA team its Day 1 work (Template and Rules §R5.7 rule 6). W1J01 and W2J01 are the earlier counterparts and W3J01 is this one; it is the wave 3 release gate of Architecture v5 slide 46, which lists contract tests per API, event and activity, Temporal replay tests and a daily journey smoke workflow and asks how the 19 services are tested as a set.

### 2. Business rationale

A service can be green on its own contract tests and still leave the wave broken, because what the wave sells is a journey: the security is valued on an appraisal the bank ordered and a person accepted, the fee on the payment follows the schedule the partner signed, the money that moved on the business date is reconciled to the case before the day closes, the settlement the customer signed is booked and posted, the guarantee claim is filed before its deadline, the notice the court will read is proven served, and the firm that will file has the pack and a clock. Each of those outcomes is produced by a different owner, on a different task queue, through a different call type, and each one is only as good as the hop before it. A fee held in code cannot follow a renegotiated schedule, a settlement accepted and never booked leaves the agreement unenforceable and the payment due date unset, a guarantee claim filed a day late is a claim lost, a notice recorded served with no proof behind it is a case that fails at filing, and an instruction issued with half a pack reaches the firm with the clock already running.

The wave 3 chain also crosses the platform on every hop: the case and its clocks in rwb-case, the ACE rows and the reconciliation outcome in rwb-source-data, the decision record in rwb-decision and the authorisation answer in rwb-access. So the defects this harness catches are the ones no single service test can see: an owner that answers a shape its contract does not allow, a hop that quietly grows a second call, a decision record written after the state change instead of in the same transaction (R-UNI-39, Principle 5), a stale ACE data product read as if it were today's, a duplicate event that produces a second claim or a second instruction instead of one idempotency hit (R-UNI-40), and a repeat of the same run that produces a second business effect.

The harness is also the cheapest place to hold the wave entry check. The alternative is a manual walk-through per wave, which proves the behaviour once for one person on one day and leaves no evidence the release can be judged on. The report this harness produces is keyed by story and business date, holds one trace per run, names the contract version of every hop and holds the pass or fail the gate reads.

It meets REQ-S1-001, REQ-RDF-004, REQ-CHO-009, REQ-RDF-007, REQ-RDF-008, REQ-S2-008, REQ-S3-001, REQ-OCC-003, REQ-S4-004, REQ-DRI-001, REQ-DRI-005 and REQ-ILG-010 at the integration level and leaves every business rule and every screen behaviour with the owning stories. The journey's business rules are R-DIS-15, R-DIS-54, R-LIT-07, R-LIT-08, R-LIT-24, R-LIT-26, R-UNI-39 and R-UNI-40 with REC-04, REC-05 and REC-06, all of which the owning services run and the harness only asserts.

### 3. Preconditions

- The harness environment, its repository, its deployment and its namespace: Not specified in the source documents (GAP-0436; ASM-0618).
- The seeded case, its route, its accounts, its asset and appraisal, its payment and proceeds, its treatment, its guarantee, its notice and its partner, with every identifier: Not specified in the source documents (GAP-0436; ASM-0618). Seeding uses only the owning services' published operations, never a schema write, and the case ID keeps the form RW-YYYY-NNNNNN of REQ-CWC-002.
- The published contracts of rwb-valuation, rwb-payment, rwb-source-data, rwb-integration, rwb-guarantee, rwb-comms, rwb-litigation, rwb-partner, rwb-treatment, rwb-writeoff, rwb-case, rwb-decision and rwb-access are in the contract registry, and one stub set is generated from each of them, so the journey runs from Day 1 before the wave 3 app stories are live.
- The business date under test is fixed at 2026-12-14, the ACE batch date the legacy reconciliation key RWB-E4-050 names for its example, and every clock and every freshness stamp the journey asserts is read from the owner and not from the harness (GAP-0436; ASM-0619).
- The appraisal of the seeded asset carries appraisal date 2026-11-02 and appraised value 4250000 for asset `AST-0001` under appraisal `AP-0001`, as the legacy keys RWB-E4-002 and RWB-E4-001 state them, so that the appraisal is older than the 12-month limit at the business date under test.
- The settlement the run books carries treatment `T-0001` at a settlement amount of 820000 for account `A-0001`, as the legacy key RWB-E4-046 states it, and the fee assertions are made against the partner's contracted fee terms read from rwb-partner for that business date, never against a figure in the script.
- The data product code that serves the `v_ace_valuation`, `v_ace_payment`, `v_ace_write_off`, `v_ace_batch_status` and `v_ace_account` records, and the reconciliation outcome of the business date: Not specified in the source documents (GAP-0436; ASM-0618).
- The wave 3 harness pack, its fixed seeding set, its evidence format, its evidence retention and the wave gate definition with its thresholds: Not specified in the source documents (GAP-0436; ASM-0620).
- The proof window that makes a notice unserved (R-LIT-08) and the notice period by product and type (R-LIT-07) are held as data by their owners; the harness reads them and does not set them.
- S7 rwb-writeoff is a wave 4 service and S9 rwb-partner a wave 4 service (Architecture v5 slide 41), so the write-off side of REC-06 and the partner-side instruction are asserted through those owners' published contracts and their stubs, and each is rerun against the real service when it lands.
- No build dependency and no contract dependency. Day 1, against the stub set, with each stub replaced by the real owner as its wave 3 story lands.

### 4. Flow

1. Harness: seeds the case and its asset through the owning services' published operations only, with one appraisal older than the 12-month limit at the business date, and reads the case back with `GET /api/recovery/case/v1/cases/{caseId}` for the route, the stage, the status and the two clocks. The seeding set and the environment are Not specified in the source documents (GAP-0436; ASM-0618).
2. Harness: triggers the route assessment with `POST /api/recovery/valuation/v1/cases/{caseId}/route` on the rwb-valuation base, which starts RouteDecisionWorkflow on task queue rwb-valuation; the request carries no person's identity, because the order is raised by the rule and not by a person (R-DIS-15 by way of the S1 step; REQ-S1-001).
3. Harness: asserts the appraisal order as an outbound item through `GET /api/recovery/integration/v1/admin/outbound-items`, naming the case and the appraisal it replaces, and asserts that exactly one order exists for the case and the Idempotency-Key of the request.
4. Harness: asserts that ACE has ingested the SVAF result for the business date by consuming `rwb.source-data.AceDataReady.v1` on `rwb.source-data.events.v1`, and reads the appraisal number, type, value and date with the acceptance fields `accepted`, `stale_flag` and `age_days` through `GET /api/recovery/source-data/v1/data-products/{productCode}/records` (DP-05, REQ-RDF-004, REQ-RDF-009). The product code is Not specified in the source documents (GAP-0436; ASM-0618).
5. Harness: drives the fee step with `POST /api/recovery/payment/v1/proceeds/{proceedsId}/match` on the rwb-payment base, so the partner fees, court fees and charges are worked out by the service that owns the fee tables and not by the harness, and reads the matched proceeds and the fees on the case back through `GET /api/recovery/payment/v1/proceeds` and `GET /api/recovery/payment/v1/cases/{caseId}/payments`.
6. Harness: asserts the partner fee against the contracted fee terms read from `GET /api/recovery/partner/v1/partners` and against the recorded result the fee is paid on, so the fee follows the schedule and the result and is not a percentage in the script (REQ-S9-004, R-DIS-11, R-WO-37).
7. Harness: holds the business date at 2026-12-14 on the rwb-source-data contract fake (§12.8) and reads the outcome of JOB-04 reconciliation, which rwb-source-data runs as an event-triggered workflow started by the ACE data ready signal, through `GET /api/recovery/source-data/v1/data-products/{productCode}/records`: one row per rec_code and business date, REC-04 matching the payments in `v_ace_payment` to the proceeds matched to the case, REC-06 matching the posting in `v_ace_write_off` to the approved write-off, and REC-05 listing every account_key and payment_code that does not resolve (DP-05, legacy RWB-E4-050). The approved write-off side is read through rwb-writeoff's published contract, which is a wave 4 owner and runs on its stub.
8. Harness: reads the accepted settlement terms through `GET /api/recovery/treatment/v1/treatments/{treatmentId}` and posts the accepted treatment with `POST /api/recovery/treatment/v1/treatments/{treatmentId}/submit`, so the booking is raised by rwb-treatment and not by the harness; it then asserts the ALS booking as an outbound item through `GET /api/recovery/integration/v1/admin/outbound-items` and its delivery through `GET /api/recovery/integration/v1/admin/outbox/deliveries`.
9. Harness: reads the booked position and the settlement payment back through the same rwb-source-data products operation, on the rwb-source-data contract fake (§12.8), after the next ACE batch, and asserts the case state after the booking through the rwb-case contract (REQ-CHO-008, DP-05).
10. Harness: drives the posting for the settlement proceeds with `POST /api/recovery/payment/v1/proceeds/{proceedsId}/match` and reads the proceeds and the posting reference recorded against them with `GET /api/recovery/payment/v1/proceeds`, then asserts the general ledger posting item and its delivery as outbound items of rwb-integration, so the entries reach the ledger through the outbound interface and never through a direct write (REQ-DRI-006, REQ-DRI-007).
11. Harness: files a guarantee claim with `POST /api/recovery/guarantee/v1/cases/{caseId}/guarantee-claims` on the rwb-guarantee base, takes the claim and its deadline from the answer of that operation and asserts `rwb.guarantee.GuaranteeClaimFiled.v1` on `rwb.guarantee.events.v1` inside the run window, with the claim deadline the owner holds.
12. Harness: asserts the proof of delivery on the notice: it reads the notice and its dispatch and proof of delivery with `GET /api/recovery/comms/v1/notices/{noticeId}`, asserts `rwb.comms.NoticeDelivered.v1` on `rwb.comms.events.v1` for the case, and asserts on `GET /api/recovery/case/v1/cases/{caseId}` and `GET /api/recovery/case/v1/cases/{caseId}/timers` that the case has moved to WITH_CUSTOMER_NOTICE_PERIOD with the notice period started from `delivered_at` (R-LIT-07), and that a notice whose proof window expired reads NOTICE_UNSERVED with no notice period started (R-LIT-08, legacy RWB-E5-002).
13. Harness: issues the instruction and the pack with `POST /api/recovery/litigation/v1/cases/{caseId}/legal-actions` on the rwb-litigation base, reads the legal action back through `GET /api/recovery/litigation/v1/legal-actions/{legalActionId}`, and asserts the case at FIRM_INSTRUCTED through the rwb-case contract with the partner clock started on `GET /api/recovery/case/v1/cases/{caseId}/timers` (R-LIT-24, R-LIT-26, legacy RWB-E5-009).
14. Harness: reads the instruction as rwb-partner publishes it through `GET /api/recovery/partner/v1/partner/instructions` and asserts `rwb.partner.InstructionIssued.v1` on `rwb.partner.events.v1` for the case, naming the partner, the instruction type and its due date; rwb-partner is a wave 4 owner, so this hop proves the instruction against the published contract of S9 served by its fake, and the real-owner instruction, result and review are proved in RWB-ITG-W4J01-ITG (EV-20).
15. Harness: reads `GET /api/recovery/decision/v1/decision-log` once per hop and asserts exactly one record for each hop that took a decision, carrying the rule ID and the rule version the owner recorded, and asserts `rwb.decision.DecisionRecorded.v1` (EV-08) on `rwb.decision-record.v1` for each of them within the 5-minute window (DP-03, REQ-DRI-001).
16. Harness: authorises every call through `POST /api/recovery/access/v1/authorise` with the role and scope of the synthetic officer, and records the refusal path for a role without the right.
17. Harness: asserts the one-hop rule and the 2 s budget from the run trace, that no hop reads another owner's schema, and that a composition goes through the gateway-bff composite route where a screen would compose.
18. Harness: repeats the run from the same seeded state, compares the two reports assertion by assertion, and asserts that no second appraisal order, fee, reconciliation row, booking item, posting item, guarantee claim, notice delivery or instruction was created, and that the ledger and the decision log hold no duplicate entry (R-UNI-40).
19. Harness: publishes the per-run evidence report keyed by story and business date with the contract version of every hop, and holds the wave gate that reads every wave 3 harness result of the business date and fails the release when one is red.

The wave 3 gate signs against this list of steps 1 to 19 and the TC-W3J01 test case IDs traced in section 18.

### 5. Exception paths

| ID | Trigger | What the harness asserts | Message | ITG test case | Covered by |
|---|---|---|---|---|---|
| X1 | A hop answers a shape its published contract does not allow | The run fails at that hop before any assertion of the next hop; the report names the owner, the operation and both contract versions, and the earlier state is unchanged | None | TC-W3J01-07-ITG | AC3 |
| X2 | A hop does not answer inside the 2 s budget | The run fails at that hop and names it; the report holds the elapsed time and the contract version, and the state of the earlier hops is unchanged | MSG-GEN-006 | TC-W3J01-08-ITG | AC2, AC9 |
| X3 | The decision record of a hop cannot be written | Nothing moves: the state change, the record and the outbox row are one transaction, so the hop fails and the run is reported failed, not passed (R-UNI-39, Principle 5) | MSG-P7-003 | TC-W3J01-09-ITG | AC7 |
| X4 | An ACE data product behind the appraisal, the reconciliation or the read-back is stale for the business date | The hop does not treat the stale product as today's; the run fails and the report names the product and the date it carries | MSG-P1-001 | TC-W3J01-10-ITG | AC8 |
| X5 | A role without the right calls a hop | The hop is refused and the run fails; nothing is written and the refusal carries the message, not an empty answer | MSG-P4-002 | TC-W3J01-04-ITG | AC4 |
| X6 | The same event or the same command arrives twice with the same key | One fact, one idempotency hit recorded by the owner, and no second claim, order, instruction or booking item; a second business effect fails the run (R-UNI-40) | None | TC-W3J01-05-ITG | AC5 |

The report text of a failed run is for the wave entry check and is not part of the message standard. The business messages the journey produces are asserted as data on the owners' answers and are listed in section 14.

Screen states: SCR-13, SCR-18, SCR-19 and SCR-28 carry empty, loading, error and no-access states that this harness does not build. Where the gateway-bff composite route answers one of those states, the harness asserts the answer as data; the state texts are Not specified in the source documents (DOR-RWB-ITG-W3J01-ITG-10).

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Runs against the published contracts and the stub set from Day 1; it waits for no wave 3 build, and each stub is replaced by its owner as the owner lands |
| Negotiable | The seed, the fixed business date, the product codes, the evidence format and the gate thresholds are configuration agreed at the wave entry check, not business values in code |
| Valuable | The wave 3 journey is proven as a whole before the release is accepted, which is the outcome no per-service test can give |
| Estimable | One harness runner, one stub set, one event probe, one outbound-item probe, one evidence report and one gate |
| Small | Fits in one iteration with its tests |
| Testable | Each scenario of section 7 is one automated run with a machine-checkable result, and a repeated run must reproduce it |

### 7. Acceptance criteria

```gherkin
Feature: Wave 3 journey end to end - integration harness

  Background:
    Given the business date under test is 2026-12-14
    Given the seeded case, its asset, its treatment, its notice and its partner identifiers are Not specified in the source documents (GAP-0436; ASM-0618)
    Given the published contracts of rwb-valuation, rwb-payment, rwb-source-data, rwb-integration, rwb-guarantee, rwb-comms, rwb-litigation, rwb-partner, rwb-treatment, rwb-writeoff, rwb-case, rwb-decision and rwb-access are in the contract registry with a stub set generated from each

  Scenario: AC1 The journey runs green for one business date (new, D-RCV-60)
    Given the case has entered from the daily case list with a route and a decision record
    When the harness runs the journey for business date 2026-12-14 across the wave 3 owners
    Then an appraisal is ordered through rwb-valuation and the order leaves through rwb-integration to SVAF
    And the appraisal value is received from SVAF and accepted by the case owner
    And partner fees, court fees and charges are worked out by rwb-payment from the fee tables held as data
    And the money movements of the business date are reconciled by rwb-source-data by rec_code and business date
    And the settlement is booked to ALS through rwb-integration and read back from ACE
    And the settlement and sale entries are posted to the general ledger through rwb-integration with the posting reference recorded
    And a guarantee claim is filed in rwb-guarantee inside its deadline
    And the proof of delivery is recorded on the notice and the case moves with the notice period started
    And the instruction and the pack are issued to the firm and the partner clock is started
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
    Given the guarantee claim hop is forced to answer a shape its contract does not allow
    When the harness runs the journey for business date 2026-12-14
    Then the run stops at the guarantee hop and names rwb-guarantee, the operation and both contract versions
    And the appraisal, the fees, the reconciliation, the booking and the posting carry the state they carried before the hop
    And the run is reported failed and is never reported passed
    And the evidence report names the hop that failed

  Scenario: AC4 A role without the right is refused (new, D-RCV-60)
    Given a role that does not hold the right calls the guarantee claim hop
    When the harness runs the journey for business date 2026-12-14
    Then the hop is refused by rwb-access and the refusal carries MSG-P4-002
    And no claim is filed, no decision record is written for the hop and the earlier state is unchanged
    And the run is reported failed and names the operation and the role that was refused

  Scenario: AC5 A repeated run produces the same evidence and no second effect (new, D-RCV-60)
    Given the first run of the journey ended green for business date 2026-12-14
    When the harness returns to the same seeded state and runs the journey again for 2026-12-14
    Then the evidence report is the same as the first run on every assertion it holds
    And no second appraisal order, fee, reconciliation row, booking item, posting item, guarantee claim, notice delivery or instruction is created
    And a duplicate event is answered with one idempotency hit and one fact (R-UNI-40)
    And the ledger and the decision log hold no duplicate entry for the journey

  Scenario: AC6 The evidence report and the wave gate hold the release (new, D-RCV-60)
    Given the run holds one trace, the contract version of every hop and the pass or fail of every criterion
    When the wave gate reads every wave 3 harness result recorded for business date 2026-12-14
    Then the gate reports the release as passed only when every wave 3 harness result is green
    And the gate reports the release as failed when one wave 3 harness result is red, and names the harness and the hop that failed
    And the report is keyed by story and business date and its format and retention are Not specified in the source documents (GAP-0436; ASM-0618)

  Scenario: AC7 A hop whose decision record cannot be written moves nothing and the run fails (new, D-RCV-60)
    Given the decision record of one hop of the journey is forced to fail to write
    When the harness runs the journey for business date 2026-12-14
    Then the state change, the decision record and the outbox row of that hop are not written
    And MSG-P7-003 is returned by the owning service
    And the run stops at that hop and is reported failed

  Scenario: AC8 A stale ACE data product behind a hop does not pass as today's data (new, D-RCV-60)
    Given the data product behind the appraisal, the reconciliation or the read-back carries the previous business date
    When the harness runs the journey for business date 2026-12-14
    Then the hop does not treat the stale product as today's data
    And the run fails and the report names the product and the date it carries
    And MSG-P1-001 is returned by the owning service

  Scenario: AC9 A consumed call that fails or does not answer stops the run at that hop (new, D-RCV-60)
    Given a consumed call on one hop of the journey fails or does not answer inside the 2 s budget
    When the harness runs the journey for business date 2026-12-14
    Then the hop's circuit breaker records the failure and the run stops at that hop without a second effect
    And the state of every earlier hop is unchanged and no outbox row is written for the failed hop
    And the run is reported failed, names the hop, the operation and the owner, and is never reported passed

  Scenario: AC10 The proceeds, notice, instruction and reconciliation rules hold across the owners (new, D-RCV-60)
    Given the seeded state holds posted asset proceeds, a dispatched notice with proof of delivery, a notice whose proof window expires with no proof, and the payment and write-off rows of the business date
    And it holds a case for a panel firm that covers the court region and the case type and passes the conflict check, and a case for a firm nominated by the Head of Litigation or a widened panel
    When the harness runs the journey for business date 2026-12-14
    Then the posted proceeds are applied to the case and the loan account and the vendor fee is matched (BR2)
    And the proof of delivery is attached, the notice period starts from `delivered_at` and the case moves to WITH_CUSTOMER_NOTICE_PERIOD (BR3)
    And the notice with the expired proof window is marked unserved and its notice period does not start (BR4)
    And the panel firm is instructed with the pack through the portal and its case moves to FIRM_INSTRUCTED (BR5)
    And the nominated firm or widened panel is instructed with the pack through the portal and its case moves to FIRM_INSTRUCTED (BR6)
    And REC-04 matches the payments in `v_ace_payment` to the proceeds matched to the case (BR9)
    And REC-06 matches the posting in `v_ace_write_off` to the approved write-off (BR10)
    And REC-05 lists every account_key and payment_code that does not resolve, with the outcome in `reconciliation_result` by rec_code and business date (BR11)
```

The six criteria are new for this harness and restate no app criterion, because W3J01 is a new story with no legacy counterpart. The criteria of the wave 3 services are owned by their own stories, and the hops that also carry a sibling harness (the appraisal order of RWB-ITG-E4001-ITG, the appraisal value of RWB-ITG-E4002-ITG, the fees of RWB-ITG-E4045-ITG, the booking of RWB-ITG-E4046-ITG, the posting of RWB-ITG-E4047-ITG, the reconciliation of RWB-ITG-E4050-ITG, the proof of delivery of RWB-ITG-E5002-ITG and the instruction of RWB-ITG-E5009-ITG) are asserted here only as hops of the wave 3 chain.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | An appraisal older than the 12-month policy limit raises a valuation order to SVAF with no person asking, and the asset waits at AWAITING_VALUER | R-DIS-15; REQ-S1-001 |
| BR2 | When asset proceeds are posted, the proceeds are applied to the case and the loan account and the vendor fee is matched | R-DIS-54 |
| BR3 | Proof of delivery received on a dispatched notice attaches the proof, starts the notice period from `delivered_at` and moves the case to WITH_CUSTOMER_NOTICE_PERIOD | R-LIT-07 |
| BR4 | A proof window that expires with no proof returned marks the notice unserved, and the notice period does not start | R-LIT-08 |
| BR5 | A panel firm that covers the court region and the case type and passes the conflict check is instructed with the pack through the portal, and the case moves to FIRM_INSTRUCTED | R-LIT-24 |
| BR6 | A firm nominated by the Head of Litigation, or a widened panel, is instructed with the pack through the portal, and the case moves to FIRM_INSTRUCTED | R-LIT-26 |
| BR7 | No action proceeds if its decision log entry cannot be written; the record, the state change and the outbox row are one transaction | R-UNI-39; REQ-DRI-005 |
| BR8 | The same event arriving twice with the same key is ignored and the idempotency hit is recorded, so one fact produces one business effect | R-UNI-40 |
| BR9 | REC-04 matches the payments in `v_ace_payment` to the proceeds matched to the case for the business date | REC-04; legacy RWB-E4-050 |
| BR10 | REC-06 matches the posting in `v_ace_write_off` to the approved write-off for the business date | REC-06; legacy RWB-E4-050 |
| BR11 | REC-05 lists every account_key and payment_code that does not resolve in the view, and the outcome is written to `reconciliation_result` by rec_code and business date | REC-05; legacy RWB-E4-050 |
| BR12 | An outbound instruction to an outside system is an item its owner can read back, with its own result, retry and exception queue | REQ-DRI-007 |

The harness asserts these twelve rules against the owners and the published contracts; it re-implements none of them and changes no BR row. REC-04, REC-05 and REC-06 carry no rule ID in the Business Rules and Routing Logic extract read here and are taken as the legacy key RWB-E4-050 names them.

### 9. State transitions

The harness changes no case, appraisal, fee, reconciliation, booking, posting, claim, notice or instruction state of its own. Every move below is made by the owner when the harness calls the owner's published operation, or when the owner's workflow reacts to an event the harness caused. A state the harness set by hand would prove nothing, so the report names the owner and the operation that made each move.

| Observed fact | Caused by | Asserted as |
|---|---|---|
| Appraisal ordered and the case waiting on the valuer | S1 rwb-valuation, RouteDecisionWorkflow on task queue rwb-valuation | The outbound item to SVAF is readable and the case answers at the state the owner reached (TC-W3J01-01-ITG) |
| Appraisal received and accepted | S1 rwb-valuation on the ACE appraisal read through P1 rwb-source-data | The acceptance fields `accepted`, `stale_flag` and `age_days` are set against the `valuation_key` (TC-W3J01-01-ITG) |
| Payment matched and fees recorded | P8 rwb-payment, the match step and the fee step of the proceeds | The proceeds answer carries the match and the fee amounts, and ProceedsMatched is on the topic (TC-W3J01-01-ITG) |
| Reconciliation outcome written by rec_code and business date | P1 rwb-source-data, JOB-04 reconciliation, `ReconciliationWorkflow` (`recon-{businessDate}`), started as a child of `AceIngestCheck` after the ALS stamp | One row per rec_code and business date through the P1 products operation (TC-W3J01-01-ITG) |
| Settlement booked to ALS and confirmed from the next ACE batch | S2 rwb-treatment through P2 rwb-integration | The outbound item is readable and delivered, and the booked position and the payment are read from `v_ace_account` and `v_ace_payment` (TC-W3J01-01-ITG) |
| Entries posted to the general ledger with the posting reference recorded | P8 rwb-payment through P2 rwb-integration | The posting item and its delivery are readable, and the posting reference is on the proceeds (TC-W3J01-01-ITG) |
| Guarantee claim filed inside its deadline | S3 rwb-guarantee, GuaranteeClaimWorkflow | The claim answer carries the deadline, and GuaranteeClaimFiled is on the topic (TC-W3J01-01-ITG) |
| Notice served and the notice period started, or the notice unserved | P6 rwb-comms for the notice and the proof of delivery, S4 rwb-litigation for R-LIT-07 and R-LIT-08, P3 rwb-case for the state and the timer | The notice answer carries its proof, the case answers at WITH_CUSTOMER_NOTICE_PERIOD or NOTICE_UNSERVED, and the timer answer shows the notice period (TC-W3J01-01-ITG) |
| Firm instructed and the partner clock started | S4 rwb-litigation, LitigationWorkflow, with the instruction on S9 rwb-partner | The legal action answer carries the pack and the firm, the case answers at FIRM_INSTRUCTED, the partner clock is on the case timers, and InstructionIssued is on the topic (TC-W3J01-01-ITG) |
| A hop forced to answer a shape its contract does not allow | the harness, on the stub set | The run stops at the hop and the earlier state is unchanged (TC-W3J01-07-ITG) |
| A decision record that cannot be written | the owner of the hop, whose transaction rolls back | Nothing moved and the run is failed (TC-W3J01-09-ITG) |
| A duplicate event or a repeated command | the owner of the hop, through its inbox and Idempotency-Key | One fact and one idempotency hit, and no second business effect (TC-W3J01-05-ITG) |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-CASEOWN, case owner | The synthetic user the harness drives on the appraisal acceptance and the case reads, within the case scope of the seeded queue |
| RW-LITOFF, litigation officer | Drives the notice and the instruction hops and reads the pack, the notice and the firm |
| RW-CREDITAD, credit administration | Drives the booking, the posting and the reconciliation reads |
| RW-GUARANT, guarantee officer | Files the guarantee claim and reads it back |
| RW-CASEOWN, RW-TEAMMGR, RW-COMPLAIN, RW-FRAUD and the further roles that hold the case record R | Read the same journey evidence; change nothing |
| RW-AUDIT, internal audit | Reads the decision log and the ledger of the journey; changes nothing |
| RW-PLATADM, platform administrator | Reads the outbound items, the deliveries and the data product freshness the run asserts; resends nothing |
| QA lead | Owns the seeded data, the fixed business date, the stub set, the evidence format and the wave gate |
| Integration lead | Owns the harness code, the trace assertions and the swap from a stub to the real owner |
| The owning services' identities | rwb-valuation, rwb-payment, rwb-source-data, rwb-integration, rwb-guarantee, rwb-comms, rwb-litigation, rwb-partner, rwb-treatment, rwb-writeoff, rwb-case, rwb-decision and rwb-access make every state change the harness asserts |
| No delegation of authority level applies | The harness takes no business decision; the approvals inside the journey are the approval stories' |

Authorisation is answered on every call by `POST /api/recovery/access/v1/authorise`, and the harness asserts both the allow path for RW-CASEOWN in scope and the refusal path for a role without the right.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 to DF-CAS-023 | recovery_case | status, stage_code, prescription_date, stage_clock_start | Read, through the rwb-case contract |
| DF-ACE-187 to DF-ACE-195 | v_ace_valuation | valuation_key, asset_key, appraisal_no, appraisal_type, appraised_value, appraisal_date | Read, through the rwb-source-data data product (DP-05) |
| DF-EXT-036 to DF-EXT-049 | valuation_ext | valuation_key, accepted, accepted_at, stale_flag, age_days | Read, through the rwb-source-data data product (DP-05) |
| DF-ACE-043 to DF-ACE-054 | v_ace_payment | payment_code, account_key, payment_date, payment_amount, payment_channel, capital_amount | Read, through the rwb-source-data data product (DP-05) |
| DF-ACE-261 to DF-ACE-269 | v_ace_write_off | write_off_key, account_key, amount, posted_date, responsibility_center, gl_product | Read, through the rwb-source-data data product (DP-05) |
| DF-ACE-178 to DF-ACE-186 | v_ace_batch_status | source_system, business_date, status, record_count, checksum, is_complete | Read, through the rwb-source-data data product (DP-05) |
| DF-ACE-001 to DF-ACE-042 | v_ace_account | account_key, account_code, account_status, contract_no, total_balance | Read, through the rwb-source-data data product (DP-05) |
| DF-FIN-001 to DF-FIN-009 | proceeds | id, case_id, payment_code, source, amount, matched_to, posting_ref | Read, through the rwb-payment contract |
| DF-FIN-010 to DF-FIN-020 | write_off | id, case_id, decision_log_id, amount, committee_date | Read, through the rwb-writeoff contract |
| DF-OPS-118 to DF-OPS-129 | reconciliation_result | id, rec_code, business_date, product_group, source_count, workbench_count | Read, through the rwb-source-data data product (DP-05) |
| DF-OPS-168 to DF-OPS-177 | outbound_item | id, interface_id, idempotency_key, payload_ref, case_ids, attempt_count | Read, through the rwb-integration admin operation |
| DF-TRT-001 to DF-TRT-014 | treatment | id, case_id, treatment_type, state, and the accepted settlement terms | Read and driven, through the rwb-treatment contract |
| DF-TRT-015 to DF-TRT-022 | guarantee_claim | id, case_id, claim_type, claim_deadline, claimed_amount, filed_at | Written by rwb-guarantee through `POST /cases/{caseId}/guarantee-claims`, read back |
| DF-LEG-015 to DF-LEG-023 | notice | id, case_id, document_id, notice_type, sent_date, barcode, and the proof of delivery | Read, through the rwb-comms contract |
| DF-PRT-001 to DF-PRT-007 | partner | id, partner_code, partner_name, partner_type, panel_status, contract_end | Read, through the rwb-partner contract |
| DF-PRT-008 to DF-PRT-016 | partner_instruction | id, case_id, partner_id, instruction_type, instructed_at, due_at | Read, through the rwb-partner contract |
| DF-WRK-027 to DF-WRK-036 | timer | id, case_id, timer_type, started_at, expires_at | Read, through the rwb-case contract |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | case_id, decision_code, rule_id, rule_version, model_version | Read, through the rwb-decision contract |
| DF-REF-001 to DF-REF-015 | rule_row | rule_id, rule_version, route_set, from_state, event_code | Read, through the rwb-decision contract |

Field IDs are those of the Logical Data Model and Data Dictionary, taken from the legacy keys RWB-E4-001, RWB-E4-002, RWB-E4-045, RWB-E4-046, RWB-E4-047, RWB-E4-050, RWB-E5-002 and RWB-E5-009. The harness owns no table and writes no row directly: it reads through the owner's contract and its only writes are the guarantee claim it files through the rwb-guarantee operation and the commands it posts to the owners that own them (DP-01). Which field of `reconciliation_result` carries each count the run reads, and the product code behind each data product read, are Not specified in the source documents (GAP-0436; ASM-0618). Test data is synthetic; no production case, party, payment, guarantee, notice or partner record is copied, and no personal data is written to a report. Criteria and test data read the ACE views only through the rwb-source-data data product (DP-05); no criterion or test case names a view as a direct read. Reference data is read only through the reference-data contract (DP-06, DP-07): the fee tables that rwb-payment reads and the rule rows that rwb-decision reads take their parameters from those products, and the parameter names are Not specified in the source documents (DOR-RWB-ITG-W3J01-ITG-20).

### 12. Contract

#### 12.1 REST operations provided

None. The harness is a test runner: it serves no operation, opens no port a service calls and publishes no endpoint.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| POST | `/api/recovery/valuation/v1/cases/{caseId}/route` | S1 rwb-valuation | The route assessment that checks the appraisal age and raises the SVAF order (AC1) |
| GET | `/api/recovery/source-data/v1/data-products/{productCode}/records` | P1 rwb-source-data | The appraisal and its acceptance, the ACE payment and write-off rows, the reconciliation outcome, the booked position and the batch status (AC1, X4, DP-05) |
| GET | `/api/recovery/integration/v1/admin/outbound-items` | P2 rwb-integration | The SVAF order, the ALS booking item and the general ledger posting item (AC1) |
| GET | `/api/recovery/integration/v1/admin/outbox/deliveries` | P2 rwb-integration | The delivery, the attempt count and the retry record of each item (AC1, BR12) |
| POST | `/api/recovery/payment/v1/proceeds/{proceedsId}/match` | P8 rwb-payment | Drives the fee step and the posting step as part of the proceeds match (AC1) |
| GET | `/api/recovery/payment/v1/proceeds` | P8 rwb-payment | The matched proceeds, the fee amounts and the posting reference (AC1) |
| GET | `/api/recovery/payment/v1/cases/{caseId}/payments` | P8 rwb-payment | The payments and the fees on the case (AC1) |
| GET | `/api/recovery/partner/v1/partners` | S9 rwb-partner | The partner and its contracted fee terms (AC1); run on the stub until S9 lands |
| GET | `/api/recovery/treatment/v1/treatments/{treatmentId}` | S2 rwb-treatment | The accepted settlement terms to be booked (AC1) |
| POST | `/api/recovery/treatment/v1/treatments/{treatmentId}/submit` | S2 rwb-treatment | Posts the accepted treatment so the booking is raised (AC1) |
| POST | `/api/recovery/guarantee/v1/cases/{caseId}/guarantee-claims` | S3 rwb-guarantee | Files the guarantee claim inside its deadline and answers with the claim and its deadline (AC1, AC3) |
| GET | `/api/recovery/comms/v1/notices/{noticeId}` | P6 rwb-comms | The notice with its dispatch and its proof of delivery (AC1) |
| POST | `/api/recovery/litigation/v1/cases/{caseId}/legal-actions` | S4 rwb-litigation | Issues the instruction and the pack to the firm (AC1) |
| GET | `/api/recovery/litigation/v1/legal-actions/{legalActionId}` | S4 rwb-litigation | The legal action, the firm and the pack read back (AC1) |
| GET | `/api/recovery/partner/v1/partner/instructions` | S9 rwb-partner | The instruction as the partner service publishes it (AC1); run on the stub until S9 lands |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The status, the stage, the prescription date and the stage clock (AC1, AC3, AC4) |
| GET | `/api/recovery/case/v1/cases/{caseId}/timers` | P3 rwb-case | The notice period and the partner clock (AC1) |
| GET | `/api/recovery/decision/v1/decision-log` | P7 rwb-decision | The decision record of every hop that took a decision (AC1, X3) |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | The role, scope and right check on every call, including the refusal path (AC4, X5) |

Every operation is one hop on the owner's base `/api/recovery/<short>/v1` with a 2 s budget and a circuit breaker per downstream; where a screen would compose several owners, the harness calls the gateway-bff composite route, whose paths and merge order are Not specified in the source documents (GAP-0436; ASM-0618). The `{productCode}` behind each data product read is Not specified in the source documents (GAP-0436; ASM-0618). No operation is invented in this story.

The write that records the proof of delivery is not named by any source read: the ownership map gives `GET /notices/{noticeId}` to P6 with the proof of delivery on the answer and no delivery-confirmation path, so the harness names the P6 operation that RWB-P6-E5002-APP publishes for the delivery confirmation and asserts the result through the P6 notice read, the P3 case and the P3 timers rather than restating a path here. The guarantee claim is read from the answer of the S3 create operation and the event, because the ownership map gives S3 `POST /cases/{caseId}/guarantee-claims` and `PATCH /guarantee-claims/{claimId}` and no claim read path; no path is invented for it. The same holds for the reconciliation outcome of JOB-04, which has no published read path in the ownership map and is read as records of the rwb-source-data data product (GAP-0436; ASM-0621).

#### 12.3 Events published

None. The harness publishes no Kafka event; it consumes the owners' events and writes its evidence report to the wave record.

#### 12.4 Events consumed

| Event | Topic | Producer | What the harness asserts |
|---|---|---|---|
| `rwb.valuation.RouteDecided.v1` | `rwb.valuation.events.v1` | S1 rwb-valuation | The route decision that follows the appraisal acceptance (AC1) |
| `rwb.source-data.AceDataReady.v1` (EV-26) | `rwb.source-data.events.v1` | P1 rwb-source-data | The ACE batch of the source system and business date is ready (one event per source system and business date, record key `{sourceSystem}:{businessDate}`, payload `sourceSystem`, `businessDate`, `status`, `completedAt`), so the appraisal and the read-back run; the reconciliation of the date is started inside rwb-source-data after the ALS stamp (AC1, X4) |
| `rwb.payment.ProceedsMatched.v1` (EV-25) | `rwb.payment.events.v1` | P8 rwb-payment | The fee step and the posting fact for the case, once for the run (AC1, AC5) |
| `rwb.treatment.TreatmentApproved.v1` (EV-10) | `rwb.treatment.events.v1` | S2 rwb-treatment | The approval that precedes the ALS booking (AC1) |
| `rwb.integration.FileDelivered.v1` | `rwb.integration.events.v1` | P2 rwb-integration | The ALS booking and the general ledger posting delivered, where the interface is a file (AC1) |
| `rwb.integration.FileFailed.v1` | `rwb.integration.events.v1` | P2 rwb-integration | A failed item, which the run must not pass over (AC1) |
| `rwb.guarantee.GuaranteeClaimFiled.v1` | `rwb.guarantee.events.v1` | S3 rwb-guarantee | One claim filed for the case, with its deadline (AC1, AC5) |
| `rwb.comms.NoticeDelivered.v1` (EV-15) | `rwb.comms.events.v1` | P6 rwb-comms | The delivery fact that starts the notice period (AC1) |
| `rwb.partner.InstructionIssued.v1` (EV-20) | `rwb.partner.events.v1` | S9 rwb-partner | The instruction and its due date for the case (AC1); run on the stub until S9 lands |
| `rwb.decision.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | all 19 services | One record per hop that took a decision, arriving before the record is read from the central ledger (AC1, X3) |

The events carry IDs and business facts only, keyed by caseId, and the harness asserts the absence of personal data in each one (DP-09). Order per case is guaranteed by the case key, a duplicate is answered with one idempotency hit (R-UNI-40), and every state the harness asserts is read from the owner's contract and never reconstructed from a topic.

#### 12.5 Workflows and activities

None added. The harness starts no workflow, adds no activity and owns no task queue. It exercises the existing parent CaseWorkflow in rwb-case (one per case, entry to closure, with a child workflow per stage), RouteDecisionWorkflow on task queue rwb-valuation, TreatmentWorkflow on task queue rwb-treatment, GuaranteeClaimWorkflow on task queue rwb-guarantee, LitigationWorkflow on task queue rwb-litigation, and the JOB-04 reconciliation workflow of rwb-source-data, which starts on the ACE data ready signal. It exercises the `deliverFile` activity on task queue rwb-integration, which carries the SVAF order, the ALS booking and the general ledger posting, and the `issueInstruction` activity of S4 rwb-litigation. No workflow, activity or Schedule is created, changed or owned by this story (DP-10, DP-12).

#### 12.6 Schedules

None added. JOB-04 Reconciliation (Airflow: ACE data ready, rwb-source-data) is exercised on business date 2026-12-14, JOB-10 WIN notices (16:00, rwb-comms with rwb-integration) is exercised as the dispatch fact that precedes the notice hop, and JOB-07 Payment matching and JOB-08 Booking confirmation (Airflow: ACE data ready, rwb-payment) are exercised as the facts that raise the fee and booking steps. No cron, overlap policy or catch-up window is set, changed or owned by this story (DP-10).

#### 12.7 Tables owned

None. The harness owns no schema and no table (DP-01). It reads the case and its timers through rwb-case, the ACE rows, the reconciliation outcome and the freshness through rwb-source-data (DP-05), the decision record through rwb-decision, the outbound items through rwb-integration, the fees and proceeds through rwb-payment, the claim through rwb-guarantee, the notice through rwb-comms, the legal action through rwb-litigation and the instruction through rwb-partner; it never reads another owner's tables and never writes a row.

#### 12.8 Contract fakes

| Fake | Contract | Use in the run |
|---|---|---|
| WireMock stub for rwb-valuation | `POST /cases/{caseId}/route`, `rwb.valuation.events.v1` | Day-1 run of the appraisal order and the acceptance before RWB-S1-E4001-APP and RWB-S1-E4002-APP are live |
| WireMock stub for rwb-source-data | `GET /data-products/{productCode}/records`, `rwb.source-data.events.v1` | Day-1 assertions on the appraisal, the ACE payment and write-off rows, the reconciliation outcome and the freshness |
| WireMock stub for rwb-integration | `GET /admin/outbound-items`, `GET /admin/outbox/deliveries`, `rwb.integration.events.v1` | Day-1 assertions on the SVAF order, the ALS booking and the general ledger posting |
| WireMock stub for rwb-payment | `POST /proceeds/{proceedsId}/match`, `GET /proceeds`, `GET /cases/{caseId}/payments`, `rwb.payment.events.v1` | Day-1 run of the fee step and the posting step |
| WireMock stub for rwb-partner | `GET /partners`, `GET /partner/instructions`, `rwb.partner.events.v1` | Day-1 assertion of the contracted fee terms and the instruction, until S9 lands in wave 4 |
| WireMock stub for rwb-writeoff | `write_off` read through the published contract | Day-1 assertion of the approved write-off side of REC-06, until S7 lands in wave 4 |
| WireMock stub for rwb-treatment | `GET /treatments/{treatmentId}`, `POST /treatments/{treatmentId}/submit`, `rwb.treatment.events.v1` | Day-1 run of the booking hop |
| WireMock stub for rwb-guarantee | `POST /cases/{caseId}/guarantee-claims`, `rwb.guarantee.events.v1` | Day-1 run of the claim hop, and the forced bad shape of AC3 |
| WireMock stub for rwb-comms | `GET /notices/{noticeId}`, `rwb.comms.events.v1` | Day-1 assertion of the notice, the dispatch and the proof of delivery |
| WireMock stub for rwb-litigation | `POST /cases/{caseId}/legal-actions`, `GET /legal-actions/{legalActionId}` | Day-1 run of the instruction hop |
| WireMock stub for rwb-case | `GET /cases/{caseId}`, `GET /cases/{caseId}/timers` | Day-1 assertions on the status, the notice period and the partner clock |
| WireMock stub for rwb-decision | `GET /decision-log` | Day-1 assertions of one record per hop and the forced failure of X3 |
| WireMock stub for rwb-access | `POST /authorise` | Day-1 authorisation and the refusal path of AC4 and X5 |

Each stub is generated from the published contract and its version is pinned in the run report, so a contract change shows up as a run failure and not as a silent pass. The evidence format, the evidence retention, the wave gate definition and its thresholds, the seeding set, the product codes and the wave 3 harness pack are Not specified in the source documents (GAP-0436; ASM-0618). The S7 and S9 stubs are reported as stub passes and never as a wave 3 service result (GAP-0436; ASM-0622).

#### 12.9 Call-type summary

| Call type | In this story |
|---|---|
| REST | 0 provided, 19 consumed, one hop each on `/api/recovery/<short>/v1` with a 2 s budget and a breaker per downstream, composed through gateway-bff where a screen would (AC1, AC2, X1, X2, X5) |
| Kafka | None published; `rwb.valuation.RouteDecided.v1`, `rwb.source-data.AceDataReady.v1`, `rwb.payment.ProceedsMatched.v1`, `rwb.treatment.TreatmentApproved.v1`, `rwb.integration.FileDelivered.v1`, `rwb.integration.FileFailed.v1`, `rwb.guarantee.GuaranteeClaimFiled.v1`, `rwb.comms.NoticeDelivered.v1`, `rwb.partner.InstructionIssued.v1` and `rwb.decision.DecisionRecorded.v1` consumed for assertion (AC1, X6) |
| Temporal | None added; the parent CaseWorkflow, RouteDecisionWorkflow, TreatmentWorkflow, GuaranteeClaimWorkflow, LitigationWorkflow, the JOB-04 reconciliation workflow and the `deliverFile` and `issueInstruction` activities exercised (AC1) |
| File | None. The harness reads and writes no file exchange; the SVAF order, the ALS booking and the general ledger posting are asserted as outbound items of rwb-integration, and the evidence report is a harness artefact and not a service file (AC1) |

### 13. Solution plan

The harness holds the architecture as an assertion, not as a pattern it applies. This story has no pattern table of its own because Patterns applied is None: the decoupling is a property of the owners it calls and it obeys it as follows.

- No schema of its own. The harness owns no schema and no table (DP-01), and it fails a run whose trace references another owner's schema or a view of its own. Every ACE row it needs is read through the rwb-source-data data product over the ACE view contract (DP-05), never through `v_ace_*` directly.
- Every read through the owner's contract. The case and its clocks are rwb-case's, the record is rwb-decision's, the authority is rwb-access's, the fees and proceeds are rwb-payment's, the notice is rwb-comms', the legal action is rwb-litigation's, the claim is rwb-guarantee's and the instruction is rwb-partner's.
- One hop and 2 s per call. Each call is one hop on the owner's base `/api/recovery/<short>/v1` with a 2 s budget and a circuit breaker per downstream, and never the retired monolith base (DP-11, DP-13).
- Composed through the gateway-bff composite route where a screen would, so a composition the screens make is exercised the way the screens make it (DP-19).
- No monolith base, no shared table and no local copy of a business value: the fee terms, the notice period, the proof window, the rec_codes, the rule versions and the message texts are the owners' data, read by the harness.

The package is the test scope `itg/recovery`, package `th.co.scb.ace.workbench.recovery.itg`, test scope only and not part of any deployed service, as the sibling harness stories name it.

The harness is the wave 3 release gate. The wave 3 business epics are EP04 and EP05 (§R5.6), the wave is delivered by the service epics of rwb-valuation, rwb-guarantee, rwb-litigation and rwb-debtsale with rwb-payment from the earlier wave, plus the integration epic, and no release is accepted on five separate green service runs. The gate reads every wave 3 harness result recorded for the business date, the eight sibling harness stories included, and it passes the release only when every one of them is green. Its thresholds, its name, its evidence format and the wave 3 harness pack are Not specified in the source documents (GAP-0436; ASM-0618).

**Harness components**

| Component | Type | Responsibility |
|---|---|---|
| Wave3JourneyRunner | Job | Runs the journey once per business date in hop order, holds the run lock and stops the run at the first failed hop |
| OwnerClient | Harness adapter | Calls the nineteen consumed operations of §12.2, one hop each, with the 2 s budget and the Idempotency-Key header where the operation requires one |
| StubSet | Fake | The thirteen WireMock stubs generated from the published contracts, each with its version pinned in the report |
| EventProbe | Service | Consumes the ten events of §12.4 and asserts each fact for the case inside the run window, including the absence of personal data and the idempotency hit of a duplicate |
| OutboundItemProbe | Assertion | Asserts the SVAF order, the ALS booking and the general ledger posting as readable outbound items and deliveries of rwb-integration |
| ReconciliationProbe | Assertion | Reads the JOB-04 outcome by rec_code and business date through the rwb-source-data product and asserts REC-04, REC-05 and REC-06 against the ACE rows and the Workbench-side rows |
| ClockProbe | Assertion | Reads the notice period and the partner clock before and after the two hops and fails the run when the clock did not start from `delivered_at` or from the instruction |
| TraceAssertion | Assertion | Fails the run on a call chain deeper than the gateway and one owner, on a call outside the 2 s budget, and on any cross-schema reference in the trace |
| RepeatProbe | Assertion | Compares a repeated run from the same seed assertion by assertion, and fails on a second business effect or a duplicate ledger or decision entry |
| WaveGate | Reporter | Writes the per-run evidence report keyed by story and business date and holds the pass or fail the wave entry check reads |

**Environment and test data**

- Environment: the harness environment and its repository are Not specified in the source documents (GAP-0436; ASM-0618). The run is against the §12.8 stub set from Day 1 and against each real owner as its wave 3 story lands.
- Data: the seeded case, its asset, its treatment, its notice and its partner are Not specified in the source documents (GAP-0436; ASM-0618). The case ID keeps the form RW-YYYY-NNNNNN of REQ-CWC-002, the business date under test is fixed at 2026-12-14, the appraisal is `AP-0001` for asset `AST-0001` at appraisal date 2026-11-02 with appraised value 4250000, and the settlement is treatment `T-0001` at 820000 for account `A-0001`, each as the legacy keys state them. No production record is copied.
- Reset: each run starts from the same seeded state and the same fixed business date, so a repeated run is deterministic and the two reports are comparable assertion by assertion.
- Seeding: through the owners' published operations only, never a schema write, so the seeded state is one the services themselves accept.

**Build steps**

1. Generate the thirteen stubs from the published contracts, pin each contract version in the report, and prove the journey runs green against the stub set from Day 1 (X1).
2. Build Wave3JourneyRunner and OwnerClient with the hop order of §4, the 2 s budget, the breaker per downstream, the run lock and the Idempotency-Key on every command.
3. Add the appraisal hops: trigger the route assessment, assert the SVAF order as an outbound item, consume AceDataReady, and assert the appraisal, the acceptance and the stale flag through the P1 product (X4).
4. Add the fee step and the partner terms assertion, so every fee is asserted against the schedule the owner holds and never against a figure in the script.
5. Add the reconciliation hop: hold the business date, read the JOB-04 outcome by rec_code and business date, and assert REC-04, REC-05 and REC-06 against the ACE rows and the Workbench-side rows, with the write-off side on the S7 stub.
6. Add the booking hop and the read-back from `v_ace_account` and `v_ace_payment` after the next ACE batch, and assert the case state after the booking.
7. Add the posting hop and assert the general ledger item, its delivery and the posting reference on the proceeds.
8. Add the guarantee hop, assert GuaranteeClaimFiled with its deadline, and add the forced bad shape of AC3.
9. Add the notice hop: assert the proof of delivery, the case at WITH_CUSTOMER_NOTICE_PERIOD with the notice period started from `delivered_at`, and the NOTICE_UNSERVED path of R-LIT-08.
10. Add the instruction hop: assert the legal action, the firm, the pack, the case at FIRM_INSTRUCTED, the partner clock and InstructionIssued, with the partner side on the S9 stub.
11. Add the ledger and decision-record assertions, the access path through `POST /api/recovery/access/v1/authorise` and the refusal path of AC4.
12. Add TraceAssertion and the timeout case of X2, and prove a forced failure names the hop and leaves the earlier state unchanged.
13. Add RepeatProbe and the duplicate-event case of X6, and prove the repeated run reproduces the report with one idempotency hit and no duplicate business effect.
14. Add WaveGate, read every wave 3 harness result of the business date, and prove the release fails when one of them is red.
15. Swap one stub for its real owner as each wave 3 story lands, rerunning the journey after each swap, and report a stub pass as a stub pass and never as a real-owner pass.

**Gate definition.** The gate reads the wave 3 harness results recorded for the business date and passes the release only when every one of them is green; one red harness fails the release and names the harness and the hop. The gate's name, its evidence format and retention, and any threshold beyond all-green are Not specified in the source documents (GAP-0436; ASM-0620).

**Feature switch.** The harness has no production feature flag and runs in the test environment only. The wave 3 behaviour it exercises is switched on by the wave 3 stories' own flags; where a flag holds a behaviour off, the run reports the hop as skipped and the gate treats a skipped hop as not green. The flag keys for this harness are Not specified in the source documents (GAP-0436; ASM-0618).

**Done when.** The tests of section 16 pass; the journey runs green for business date 2026-12-14 against the stub set on Day 1 and again, hop by hop, against each real owner as its wave 3 story lands; the report holds one trace, the contract version of every hop and every assertion of section 7; and the wave gate fails the release on one red harness result and passes it on all green.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P7-003 | The decision record of a hop cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | A role without the right calls a hop | You cannot {action} here. Your role does not include it. |
| MSG-P1-001 | An ACE data product behind a hop is stale for the business date | {product} is from {date}. Today's load has not arrived. |
| MSG-GEN-006 | A system of record behind a hop does not answer inside the budget | {system} is not available. Try again in a few minutes. |
| MSG-S4-001 | The pack the instruction carries is missing a document | The pack is missing {item}. Add it before filing. |
| MSG-S4-002 | The claim on the case is close to its prescription date | The claim on this case expires on {date}. File before then. |

The harness produces none of these messages itself: it asserts the message the owning service returns and names the message ID in the report, so a failed run points at an owner, an operation and a message and not only at a date. R-DIS-15, R-DIS-54, R-LIT-07, R-LIT-08, R-LIT-24, R-LIT-26, R-UNI-39 and R-UNI-40 and the three rec_codes carry no message ID of their own in the rule set read here, so the harness asserts the state, the data, the outbound item and the decision record and names a message ID only where an owning service returns one of those above. Thai text for each message follows decision DL10, which is still open and rests on assumptions ASM-2250, ASM-2357, ASM-2377 and ASM-2863. The English text follows Error and Message Standard v4, and the standard governs it.

### 15. Screens and states

The harness renders no screen and opens no page. Where a screen would compose several owners, the harness calls the gateway-bff composite route and asserts the answer the screen consumes, so a green hop means the screen has the right data behind it:

| Screen | State | What the harness asserts |
|---|---|---|
| SCR-13 Route decision | recommendation | The appraisal, the acceptance and the route state the owner returns, and the SVAF order as an outbound item |
| SCR-13 Route decision | loading | Not specified in the source documents (CG-ALL-935) |
| SCR-13 Route decision | empty | Not specified in the source documents (CG-ALL-935) |
| SCR-13 Route decision | error | Not specified in the source documents (CG-ALL-935) |
| SCR-13 Route decision | no access | Not specified in the source documents (CG-ALL-935) |
| SCR-28 Proceeds matching | matched | The payment, the proceeds, the fee and the posting reference aligned to the case and to the partner's schedule |
| SCR-28 Proceeds matching | unmatched | The reconciliation outcome that lists the account_key and payment_code that do not resolve (REC-05) |
| SCR-28 Proceeds matching | empty | Not specified in the source documents (CG-ALL-938) |
| SCR-28 Proceeds matching | loading | Not specified in the source documents (CG-ALL-938) |
| SCR-28 Proceeds matching | error | Not specified in the source documents (CG-ALL-938) |
| SCR-28 Proceeds matching | no access | Not specified in the source documents (CG-ALL-938) |
| SCR-18 Notice approval | delivered | The notice answer with its proof of delivery, the case at WITH_CUSTOMER_NOTICE_PERIOD and the notice period timer |
| SCR-18 Notice approval | unserved | The notice answer marked unserved, no notice period started, and the case at NOTICE_UNSERVED |
| SCR-18 Notice approval | empty | Not specified in the source documents (CG-ALL-936) |
| SCR-18 Notice approval | loading | Not specified in the source documents (CG-ALL-936) |
| SCR-18 Notice approval | error | Not specified in the source documents (CG-ALL-936) |
| SCR-18 Notice approval | no access | Not specified in the source documents (CG-ALL-936) |
| SCR-19 Litigation workspace | instructed | The legal action with the firm and the pack, the case at FIRM_INSTRUCTED and the partner clock |
| SCR-19 Litigation workspace | empty | Not specified in the source documents (CG-ALL-937) |
| SCR-19 Litigation workspace | loading | Not specified in the source documents (CG-ALL-937) |
| SCR-19 Litigation workspace | error | Not specified in the source documents (CG-ALL-937) |
| SCR-19 Litigation workspace | no access | Not specified in the source documents (CG-ALL-937) |

The screen behaviour of each state stays with the wave 3 app stories. What the wave entry check reads instead is the evidence report, whose format and retention are Not specified in the source documents (GAP-0436; ASM-0618). The wave 3 entry check, with the integration and QA leads, settles the harness environment and pipeline, the seeding set and fixtures, the business date and ACE batch, the product codes, the evidence report format and retention, and the gate name and thresholds (GAP-0436).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-W3J01-01-ITG | AC1, BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10, BR11, BR12 | End to end | Business date 2026-12-14, seeded case through appraisal order, appraisal value, fees, reconciliation, booking, posting, claim, notice and instruction |
| TC-W3J01-02-ITG | AC2 | Component | Run trace of the AC1 run; one owner per hop, 2 s budget, no cross-schema read, gateway-bff composition |
| TC-W3J01-03-ITG | AC3 | Integration | Guarantee hop forced to answer a shape its contract does not allow |
| TC-W3J01-04-ITG | AC4, X5 | Component | A role without the right calls the claim hop; refused with MSG-P4-002 |
| TC-W3J01-05-ITG | AC5, X6, BR8 | Integration | The same seeded state run twice on 2026-12-14, with a duplicate event on the claim topic |
| TC-W3J01-06-ITG | AC6 | End to end | Every wave 3 harness result recorded for the business date, one of them red |
| TC-W3J01-07-ITG | X1 | Component | Contract version mismatch and a shape outside the OpenAPI document on one hop |
| TC-W3J01-08-ITG | X2, BR12 | Integration | One hop delayed past the 2 s budget; MSG-GEN-006 |
| TC-W3J01-09-ITG | AC7, X3, BR7 | NFR | Decision record write forced to fail on every hop of the journey; no state changes |
| TC-W3J01-10-ITG | AC8, X4 | Integration | The data product behind the appraisal or the reconciliation carries the previous business date; MSG-P1-001 |
| TC-W3J01-11-ITG | AC9 | Integration | A consumed call on one hop fails or does not answer inside the 2 s budget; the run stops at that hop and is reported failed |
| TC-W3J01-12-ITG | AC10, BR2, BR3, BR4, BR5, BR6, BR9, BR10, BR11 | End to end | Business date 2026-12-14; posted asset proceeds, a notice with proof of delivery, a notice with an expired proof window, a panel firm case, a nominated or widened panel case, payment and write-off rows with an unresolved account_key and payment_code; identifiers Not specified in the source documents (GAP-0436; ASM-0618) |

These are new test cases under D-RCV-60 and carry no legacy copy, because W3J01 is a new story: the wave 3 legacy test cases stay with their own ITG stories and are not restated here. The full test, with its Given, When and Then, is held under the same test case ID in the wave 3 harness pack; its pack, environment and evidence format are Not specified in the source documents (GAP-0436; ASM-0618).

### 17. Guardrails

- No business value in code: the 12-month appraisal limit, the fee schedules and the partner's contracted terms, the proof window, the notice periods, the rec_codes, the rule versions, the state names and the message texts are the owners' data, read by the harness and never held as a copy.
- No personal data in logs, traces, tests or reports: the harness asserts IDs, codes and states only, the events are asserted for the absence of personal data, and no production case, party, payment, guarantee, notice or partner record is copied.
- No read of another owner's tables: every read and every seed goes through the owner's contract (DP-01), every ACE row is read from rwb-source-data (DP-05), and TraceAssertion fails a run that shows a cross-schema reference.
- The Workbench writes nothing to SVAF, ALS or the general ledger directly: the order, the booking and the posting leave as outbound items of rwb-integration, logged, retried and placed in an exception queue after the retry limit (REQ-DRI-006, REQ-DRI-007).
- One hop and a 2 s budget per call with a breaker per downstream, and a composition through gateway-bff where a screen would compose, so the harness fails where a screen would fail (DP-11, DP-19).
- A stub pass is never reported as a real-owner pass: the report names the contract version and whether the hop was a stub or the owner, and the gate treats a skipped hop as not green.
- S7 rwb-writeoff and S9 rwb-partner are wave 4 owners: their hops and their rows are reported as stub passes, and neither is reported as a wave 3 service result.
- A forced failure is an input to the run and never a waiver: a red hop is fixed in the owner that owns it or reported as a gap, and the run is reported failed.
- The harness never runs against UAT or production, never calls an outside system directly, and never sets a case, appraisal, fee, reconciliation, booking, posting, claim, notice or instruction state by hand.
- A repeated run must reproduce the report: a second business effect, a duplicate ledger or decision entry, or a duplicate fact on the same key fails the run (R-UNI-40).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-S1-001 | An appraisal older than the policy limit triggers a new valuation order without a person asking for it | Business Requirements Program v5, section 5.8 | FEAT-VAL-01 | D6 route decision (S1 valuation) | R-DIS-15 | TC-W3J01-01-ITG |
| REQ-RDF-004 | Collateral records and appraisal values are available on the case through `v_ace_valuation`, and the Workbench's acceptance is held in `valuation_ext` | Business Requirements Program v5, section 5.1 | FEAT-VAL-01, FEAT-VAL-02 | D6 route decision (S1 valuation) | R-DIS-15 | TC-W3J01-01-ITG, TC-W3J01-10-ITG |
| REQ-RDF-009 | Every data product carries a freshness stamp and every decision records the freshness of the data it used | Business Requirements Program v5, section 5.1 | FEAT-VAL-01, FEAT-VAL-02 | D6 route decision (S1 valuation) | None in force (S1 package Phase 2) | TC-W3J01-01-ITG, TC-W3J01-10-ITG |
| REQ-CHO-009 | Payments received, read from ACE through `v_ace_payment`, are matched to the plan, the settlement or the fee by the ACE `payment_code`, and anything unmatched goes to an exception list | Business Requirements Program v5, section 5.3 | FEAT-PAY-05, FEAT-PAY-11 | D6.4 settlement | REC-04, REC-05 | TC-W3J01-01-ITG |
| REQ-RDF-007 | The case list reconciles daily to the ACE count with no variance, and every business key resolves to an ACE row | Business Requirements Program v5, section 5.1 | FEAT-PAY-11, FEAT-RDF-11 | D6.4 settlement | REC-04, REC-05, REC-06 | TC-W3J01-01-ITG |
| REQ-RDF-008 | The Workbench reports reconciliation breaks and referential completeness, each break with a reason | Business Requirements Program v5, section 5.1 | FEAT-PAY-11 | D6.4 settlement | REC-05 | TC-W3J01-01-ITG |
| REQ-S2-008 | Booked terms, settled accounts and released collateral are posted to their systems of record without re-keying | Business Requirements Program v5, section 5.9 | FEAT-PAY-06, FEAT-PAY-07 | D6.4 settlement | R-DIS-54 | TC-W3J01-01-ITG |
| REQ-CHO-008 | Terms booked in the core system are recorded on the case, and the booking is confirmed from the next business date's ACE account data in `v_ace_account` | Business Requirements Program v5, section 5.3 | FEAT-PAY-06, FEAT-CHO-08 | D6.4 settlement | R-DIS-54 | TC-W3J01-01-ITG |
| REQ-S3-001 | A guarantee claim is prepared from case data and submitted inside the guarantor's deadline | Business Requirements Program v5, section 5.10 | FEAT-GUA-01 | D6.5 guarantee claim | R-GUA-01, R-GUA-12 | TC-W3J01-01-ITG, TC-W3J01-03-ITG |
| REQ-OCC-003 | Letters are dispatched for print and post, and proof of delivery returns to the case | Business Requirements Program v5, section 5.6 | FEAT-LIT-02, FEAT-OCC-03 | D7 litigation | R-LIT-07, R-LIT-08 | TC-W3J01-01-ITG |
| REQ-S4-004 | A law firm is selected from the panel by rule using panel performance, and instructed through the partner portal | Business Requirements Program v5, section 5.11 | FEAT-LIT-09 | D7 litigation | R-LIT-24, R-LIT-26 | TC-W3J01-01-ITG |
| REQ-ILG-010 | Letters, messages and calls dispatched by the Workbench write their result to the ledger, including proof of delivery where it returns | Business Requirements Program v5, section 5.4 | FEAT-ILG-01, FEAT-LIT-02 | D7 litigation | R-LIT-07 | TC-W3J01-01-ITG, TC-W3J01-05-ITG |
| REQ-DRI-001 | Every decision writes one record holding the case, the decision, the rule and its version | Business Requirements Program v5, section 5.7 | All features of the journey | All wave 3 processes | R-UNI-39 | TC-W3J01-01-ITG, TC-W3J01-09-ITG |
| REQ-DRI-005 | No action proceeds if its decision log entry cannot be written | Business Requirements Program v5, section 5.7 | All features of the journey | All wave 3 processes | R-UNI-39 | TC-W3J01-09-ITG |
| REQ-DRI-007 | The integration adapters log every outbound file, retry on a defined schedule and place failures in an exception queue | Business Requirements Program v5, section 5.2 | FEAT-PAY-06, FEAT-PAY-07, FEAT-LIT-09 | D6.4 settlement; D7 litigation | R-UNI-40 | TC-W3J01-01-ITG, TC-W3J01-08-ITG |

The features are the EP04 and EP05 rows of the Epics 3 to 8 specification and the Program requirements they draw on; the requirements keep their Program BRD text, and no requirement is tabulated here that a source does not give.

### 19. Out of scope

- Any production behaviour: the harness is test and evidence only. It builds no production screen, endpoint, event, workflow, Schedule or table, and it owns no table.
- The wave 3 behaviour itself, which belongs to the service stories: the appraisal order and the appraisal value in rwb-valuation (RWB-S1-E4001-APP, RWB-S1-E4002-APP), the fee step in rwb-payment (RWB-P8-E4045-APP), the reconciliation in rwb-source-data and its payment side RWB-P8-E4050-APP, the booking in RWB-P8-E4046-APP and RWB-P2-E4046-APP, the posting in RWB-P8-E4047-APP, the guarantee claim in rwb-guarantee, the proof of delivery in RWB-P6-E5002-APP, RWB-S4-E5002-APP and RWB-P3-E5002-APP, and the instruction in RWB-S4-E5009-APP.
- The individual wave 3 harness stories and their own journeys: RWB-ITG-E4001-ITG for the appraisal order, RWB-ITG-E4002-ITG for the appraisal value, RWB-ITG-E4045-ITG for the fees, RWB-ITG-E4046-ITG for the booking, RWB-ITG-E4047-ITG for the posting, RWB-ITG-E4050-ITG for the reconciliation, RWB-ITG-E5002-ITG for the proof of delivery and RWB-ITG-E5009-ITG for the instruction. This story asserts those hops only as hops of the wave 3 chain and does not restate their criteria or their test cases.
- The debt sale legs of the wave: the lot award, the derecognition and the posting run of S6 rwb-debtsale (R-DS-31, R-DS-32, R-DS-33), which the posting harness story and the debt sale service stories cover. This journey asserts no lot.
- The platform owners' behaviour: the case and its clocks (rwb-case), the ACE view contract, the reconciliation and the freshness (rwb-source-data), the decision log (rwb-decision), the authorisation answer (rwb-access) and the composite route (the platform edge story RWB-PLT-N001-CON), which the platform wave delivers.
- The deployment work: the harness environment, its pipeline, its Helm chart and its namespace are the platform and DevOps stories', and none of them is decided here.
- The SVAF feed, the ALS interface, the general ledger interface and the WIN dispatch: their IDs, transport, file layouts, result codes and test endpoints, none of which a source read gives.
- S7 rwb-writeoff and S9 rwb-partner, which are wave 4 owners: the write-off side of REC-06 and the partner side of the instruction are asserted through their published contracts and their stubs, and their behaviour is theirs.
- The approvals inside the journey and the delegation of authority behind them, which belong to the approval and access stories.
- The harness environment, the seeding set, the product codes, the evidence format and retention, the gate name and its thresholds, and the wave 3 harness pack: carried as one gap and its assumptions, not decided here.
