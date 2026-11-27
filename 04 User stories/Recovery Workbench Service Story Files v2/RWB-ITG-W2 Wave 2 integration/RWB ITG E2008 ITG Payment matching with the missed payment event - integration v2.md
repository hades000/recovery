# RWB-ITG-E2008-ITG Payment matching with the missed payment event

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-E2008-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W2 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-008 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP04, DP05, DP06, DP07, DP09, DP10, DP11, DP13, DP15, DP19 |
| Parallel lane | L-ITG-W2 |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-ITG-E2008-ITG-16); the squad sizes the story at refinement |
| Depends on (build) | None |
| Contract dependencies | RWB-P3-E1043-CON (reference data for the data product list and the source-system list; added at the wave 2 contract freeze; until published, the client library and the fixture of §12.8) |
| Contract version | v1, major version 1 with BACKWARD acceptance (every operation of §12.2 is on the /v1 path; MatchRequest carries the proceeds identifier, the case, the treatment, the account payment and a reason code; every non-2xx body is application/problem+json) |
| Integration dependencies | RWB-P3-E2004-APP, RWB-P1-E1069-APP, RWB-P3-E2042-APP, RWB-P8-E2008-APP, RWB-S2-E2008-APP, RWB-P1-E2008-APP, RWB-P7-E2008-APP, RWB-P4-E2008-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to REQ-CHO-007, REQ-CHO-009) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-008 for the wave 2 integration harness. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (41 resolved, 38 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **member of the integration and QA team**, I want **a repeatable cross-service journey harness for payment matching and the missed payment event across rwb-payment, rwb-source-data, rwb-decision, rwb-treatment, rwb-case and rwb-access**, so that **the PAYMENT_MATCH journey is proven end to end, with evidence, before the wave 2 release is accepted**.

This story builds the harness and the evidence only. It builds no production endpoint, no screen, no table, no migration, no workflow and no schedule. It serves no operation, it owns no table and it starts no workflow of its own. The real behaviour is owned by the eight I stories RWB-P8-E2008-APP (JOB-07 as an event-started workflow in rwb-payment, the proceeds match, the missed payment event and the REC-04 result), RWB-P1-E2008-APP (the ACE payment, account and batch-status reads and the data-quality exception list), RWB-S2-E2008-APP (the treatment plan position and the installment update), RWB-P3-E2042-APP (the PAYMENT_MATCH package in force), RWB-P7-E2008-APP (the decision record and the central ledger), RWB-P4-E2008-APP (the role, scope and right check), RWB-P3-E2004-APP (the case, the account and the running plans of the case) and RWB-P1-E1069-APP (the ACE view grants behind the reads), and those eight stories block the ITG run.

### 2. Business rationale

The legacy RWB-E2-008 journey is one business day of the payments module: the ALS payments posted in ACE for business date D are matched to the installments of the running plans, an installment that is still unpaid when the ACE batch completes raises a missed payment, and anything that matches no plan is held for a person. Today the match is done by hand and a missed installment is found weeks later, after the cure period has gone. The split gives each service its own app story and leaves one integration story — this one — that proves the whole journey across the service boundaries on synthetic data, on one business date, with a report that can be re-run for any build.

The harness proves, in one run and one evidence pack: that JOB-07 starts on `AceDataReady` and runs for the business date the ACE batch actually completed; that package PAYMENT_MATCH fires row EXACT under rule R-RES-26 with package version PM-2026.12 on every match; that the D5 decision record is written before the proceeds row and names the rule and the version; that the proceeds row and `ProceedsMatched` leave the service together; that `recordInstallmentPaid` moves the plan to installments paid 4 with next due date 2027-01-15; that an unpaid due date raises `PaymentMissed` and P3 moves the plan PLAN_RUNNING to PLAN_CURE_PERIOD under R-RES-27; that an unmatched receipt sits on the exception list with MSG-P8-001 and is readable unmatched; that a payment on an account with no open case leaves no proceeds row and lands on the REC-05 business-key break; that an incomplete ALS batch stops the run with MSG-P1-001 instead of raising a missed payment from stale data; that the rerun of one business date adds no second row and no second event; and that the ledger, the proceeds and the plan all agree on one business date.

It evidences REQ-CHO-007 and REQ-CHO-009 at the integration level, with the match measure REC-04 and the REC-05 break, and it leaves every business rule, every message and every screen behaviour where the owning stories put them.

### 3. Preconditions

- The eight I stories are published and deployed in the SIT environment, or the contract fakes of §12.8 stand in for each of them: RWB-P3-E2004-APP (case, account and running plans), RWB-P1-E1069-APP (ACE view grants and the payment, next-installment and batch-status reads), RWB-P3-E2042-APP (PAYMENT_MATCH package in force), RWB-P8-E2008-APP (JOB-07, the proceeds match and the missed payment event), RWB-S2-E2008-APP (treatment plan position and the installment update), RWB-P1-E2008-APP (freshness, the data-quality exception list and the job rerun), RWB-P7-E2008-APP (decision record and ledger) and RWB-P4-E2008-APP (authorise).
- Package PAYMENT_MATCH version "PM-2026.12" is in force, with exactly one EXACT row: amount tolerance 0 percent, window 10 days before the due date and 0 days after, grace 0 days. The version is loaded and approved through the rwb-decision rule-package operations by RWB-P3-E2042-APP; the harness only reads it and asserts it.
- The ACE batch for ALS with business date 2026-12-14 is COMPLETE, so JOB-07 has a batch to run on. The batch is read through the P1 contract, never from the ACE view.
- The ALS payment fixture for business date 2026-12-14 is loaded through the P1 test profile, and `AceDataReady` for that business date opens the JOB-07 window.
- Case "RC-2026-000555" has account "A-0555" and running restructure plan "T-0701" with installment amount 12,500.00 THB, installments 24 and installments paid 3, account "A-0555" has next installment date 2026-12-15, and plan "T-0702" on account "A-0666" of case "RC-2026-000566" has installment amount 12,500.00 THB with next installment date 2026-12-16 (legacy section 7 Background).
- gateway-bff is deployed with the composite proceeds and exception route available to the screens that consume it. The composite route path and its merge order: Not specified in the source documents (GAP-0393; ASM-0568).
- The harness environment, its repository, its test-data seeding (including the ALS payment fixture format), its evidence format and retention and its pass or fail gate: Not specified in the source documents (GAP-0393; ASM-0568).

### 4. Flow

1. Harness: takes the run lock for the environment, records the build ID, the business date and the versions of the six contracts it is about to exercise, then seeds the case, the account, the plan, the payments and the PAYMENT_MATCH version through the owning contracts or the published fakes and reads each item back to assert the seeded state.
2. Harness: publishes or replays `AceDataReady` for business date 2026-12-14 on `rwb.source-data.events.v1`, then starts JOB-07 through the event-started workflow `matchPayments` on queue `rwb-payment` and records its workflow ID, the business date and the run outcome.
3. Harness: asserts the EXACT row of PAYMENT_MATCH (tolerance 0 percent, window 10 days before and 0 days after, grace 0 days), the R-RES-26 decision record with decision code D5, and package version PM-2026.12 on the entry, and fails the run when any of the three disagrees.
4. Harness: reads the proceeds of the business date through the P8 contract and asserts, for "PAY-90001", treatment "T-0701", source "CUSTOMER", amount 12,500.00 and matched to "INSTALLMENT", one `ProceedsMatched` event and one outbox row; then asserts `recordInstallmentPaid` for "T-0701" with due date 2026-12-15 and, after the ALS batch of 2026-12-15, installments paid 4 and next due date 2027-01-15 through the S2 and P3 contracts.
5. Harness: for the plan with no matched payment for its due date, asserts `PaymentMissed` on `rwb.payment.events.v1` with treatment "T-0701", due date 2026-12-15 and amount due 12,500.00, and asserts on the case timeline and the plan position that the plan moved PLAN_RUNNING to PLAN_CURE_PERIOD under R-RES-27.
6. Harness: reads the unmatched side of the P8 proceeds operation and asserts the "PAY-90002" row with matched to "UNMATCHED", no treatment, and the run summary carrying MSG-P8-001 with one unmatched payment for 2026-12-14.
7. Harness: asserts the REC-05 business-key break: no proceeds row exists for "PAY-90003" on account "A-0999", and "PAY-90003" is a break row on the reconciliation break list of rwb-source-data with check name "References" for the data steward; no exception table is written in `rwb_payment`.
8. Harness: withholds the COMPLETE batch for business date 2026-12-15, lets the scheduled JOB-07 time of 2026-12-16 pass, and asserts that no run happens for that business date, that no `PaymentMissed` exists for due date 2026-12-15, and that the freshness read carries MSG-P1-001 naming "DP01 Account and arrears" and 2026-12-14.
9. Harness: reruns JOB-07 for business date 2026-12-14 through the P1 rerun operation and asserts that the proceeds still hold two rows for that business date and that no second `ProceedsMatched` and no second `PaymentMissed` exist, so the idempotency keys of payment_code and of treatment plus due date hold. The composite proceeds and exception route path and merge order, the harness environment, the ALS payment fixture format, the seed pack, the evidence format and retention, and the pass or fail gate are agreed at the wave 2 entry check and recorded in the payment matching harness pack before the first real-service run (GAP-0393).
10. Harness: forces the decision-log write to fail through the P7 fake or the service's fault profile, runs the match again, and asserts that no proceeds row is written, that the run summary carries MSG-P7-003, and that the run is reported failed at that assertion rather than green.
11. Harness: writes one run report per business date, keyed by story key and business date, with the request, the response, the proceeds row, the decision entry, the plan position, the events and each assertion result; the report format and retention are Not specified in the source documents (GAP-0393; ASM-0568).

### 5. Exception paths

| ID | Trigger | What the harness asserts | Message | ITG test case | Covered by |
|---|---|---|---|---|---|
| X1 | A payment matches no plan installment ("PAY-90002" of 3,000.00) | One proceeds row with matched to "UNMATCHED" and no treatment; the read of unmatched proceeds returns "PAY-90002"; the run summary carries the count | MSG-P8-001 | TC-E2-008-03-ITG | AC3 |
| X2 | A payment sits on an account with no open case ("PAY-90003" on "A-0999") | No proceeds row for "PAY-90003"; the REC-05 business-key break carries "PAY-90003" for the data steward | None | TC-E2-008-04-ITG | AC4 |
| X3 | The ACE batch for ALS is not COMPLETE for the business date (2026-12-15 ended "FAILED") | JOB-07 does not run for 2026-12-15; no `PaymentMissed` for due date 2026-12-15; the freshness answer names "DP01 Account and arrears" and 2026-12-14 | MSG-P1-001 | TC-E2-008-05-ITG | AC5 |
| X4 | JOB-07 is rerun for business date 2026-12-14 | Still two proceeds rows for that date; no second `ProceedsMatched`; no second `PaymentMissed` | None | TC-E2-008-06-ITG | AC6 (cited; owned by app story) |
| X5 | A payment lands on the last day of the window and another one day before it opens ("PAY-90004" at 10 days, "PAY-90005" at 11 days) | "PAY-90004" matched to "INSTALLMENT" for "T-0701"; "PAY-90005" matched to "UNMATCHED" and held | MSG-P8-001 | TC-E2-008-07-ITG | AC7 (cited; owned by app story) |
| X6 | No PAYMENT_MATCH version is in force on the business date | The run stops before matching with NoPackageInForce and MSG-P3-027 naming package "PAYMENT_MATCH", then MSG-P8-002; no proceeds row and no event; the job monitor shows JOB-07 failed | MSG-P3-027, MSG-P8-002 | TC-E2-008-08-ITG | AC8 (cited; owned by app story) |
| X7 | The decision log write fails for a match that would otherwise succeed | No proceeds row for the payment; the run summary carries MSG-P7-003; the record is absent while the state change is absent too, so the pair never disagrees | MSG-P7-003 | TC-E2-008-09-ITG | AC9 (cited; owned by app story) |
| X8 | The caller holds RW-CASEOWN (Write-off and posting R absent) and calls the proceeds read | 403 with MSG-P4-002 on the direct call; the composite answer hides the unmatched action; no data is returned | MSG-P4-002 | TC-E2-008-10-ITG | None (Access, no §7 criterion) |
| X9 | The seed pack cannot be loaded | The run refuses to start and names the missing seed item; no scenario is reported as passed | None | All | None (run control) |
| X10 | Another run holds the environment lock | The run refuses to start and names the lock holder; the lock is never taken over | None | All | None (run control) |
| X11 | The evidence pack cannot be written or attached to the run record | The run is marked failed and the local evidence file is kept for rerun; no scenario is reported as passed | None | All | None (run control) |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Runs on its own once the eight I stories or their contracts are available; the fixture, the package version and the batch status are preconditions, not build dependencies |
| Negotiable | The seeded payments, the expected rule ID and the expected package version are data files, never code; the harness fixes no threshold of its own |
| Valuable | The journey is proven once across six services, and the match, the record, the proceeds and the plan position are shown to agree on one business date |
| Estimable | One harness project, one journey specification, one fake pack, one payment fixture per business date, one evidence collector and one gate |
| Small | Fits in two weeks, in one iteration with the owning stories' contract tests |
| Testable | Each criterion and each exception row has a fixed Given, When and Then and a machine-checked result in the run report |

### 7. Acceptance criteria

```gherkin
Feature: Payment matching with the missed payment event

  Background:
    Given package "PAYMENT_MATCH" version "PM-2026.12" is in force with row "EXACT": amount tolerance 0 percent, window 10 days before the due date and 0 days after, grace 0 days
    Given case "RC-2026-000555" has account "A-0555" and running restructure plan "T-0701" with installment amount 12,500.00 THB, installments 24 and installments paid 3
    Given account "A-0555" has next installment date 2026-12-15

  Scenario: AC1 Payment matched (legacy RWB-E2-008 AC1)
    Given the rwb-source-data contract answers that the ACE batch for ALS with business date 2026-12-14 is COMPLETED
    Given the rwb-source-data contract fake (ALS payment fixture, §12.8) holds payment "PAY-90001" of 12,500.00 THB on account "A-0555" dated 2026-12-14
    When JOB-07 runs on 2026-12-15
    Then the EXACT row of package "PAYMENT_MATCH" version "PM-2026.12" matches "PAY-90001" to the installment
    Then the decision log entry names rule "R-RES-26" and rule version "PM-2026.12"
    Then a proceeds row exists for case "RC-2026-000555" with treatment "T-0701", payment code "PAY-90001", source "CUSTOMER", amount 12,500.00 and matched to "INSTALLMENT"
    Then the system calls treatmentApi.recordInstallmentPaid for "T-0701" with due date 2026-12-15
    Then the system writes proceedsMatched to the outbox
    Then after the ALS batch of 2026-12-15 the plan shows installments paid 4 and next due date 2027-01-15

  Scenario: AC3 Exception (legacy RWB-E2-008 AC3)
    Given the rwb-source-data contract answers that the ACE batch for ALS with business date 2026-12-14 is COMPLETED
    Given the rwb-source-data contract fake (ALS payment fixture, §12.8) holds payment "PAY-90002" of 3,000.00 THB on account "A-0555"
    When JOB-07 runs on 2026-12-15
    Then a proceeds row exists for "PAY-90002" with matched to "UNMATCHED" and no treatment
    Then GET /proceeds?matched=false returns "PAY-90002" for the Credit Administration officer
    Then the run summary shows MSG-P8-001 with 1 unmatched payment for 2026-12-14

  Scenario: AC4 Payment on an account with no open case (legacy RWB-E2-008 AC4)
    Given the rwb-source-data contract fake (ALS payment fixture, §12.8) holds payment "PAY-90003" on account "A-0999" that is on no open case
    When JOB-07 runs on 2026-12-15
    Then the system writes no proceeds row for "PAY-90003"
    Then the REC-05 business-key break lists "PAY-90003" for the data steward

  Scenario: AC5 ACE batch not complete (legacy RWB-E2-008 AC5)
    Given the ACE batch for ALS with business date 2026-12-15 ended "FAILED"
    When the scheduled time for JOB-07 on 2026-12-16 passes
    Then JOB-07 does not run for business date 2026-12-15
    Then the system writes no PaymentMissed for due date 2026-12-15
    Then the plan view shows MSG-P1-001 naming "DP01 Account and arrears" and 2026-12-14

  Scenario: AC10 Daily reconciliation of payments to proceeds (BR8, REC-04) (new, D-RCV-60)
    Given the rwb-source-data contract answers that the ACE batch for ALS with business date 2026-12-14 is COMPLETED
    Given the rwb-source-data contract fake (ALS payment fixture, §12.8) holds for business date 2026-12-14 only payment "PAY-90001" of 12,500.00 THB and payment "PAY-90002" of 3,000.00 THB, both on account "A-0555"
    When JOB-07 runs on 2026-12-15
    Then the REC-04 result for business date 2026-12-14 shows 2 payments and 2 proceeds rows
    Then the REC-04 result shows 15,500.00 THB for the payments and 15,500.00 THB for the proceeds rows

  Scenario: AC11 Duplicate delivery of a consumed event (BR6) (new, D-RCV-60)
    Given the rwb-source-data AceDataReady fake delivered the ALS business date 2026-12-14 and JOB-07 consumed it
    When the same AceDataReady event is delivered again
    Then no second matching run is started for 2026-12-14
    Then no second proceeds row, ProceedsMatched or PaymentMissed is written

  Scenario: AC12 A consumed call does not answer (new, D-RCV-60)
    Given the rwb-case open-case fake does not answer within 2 s
    When JOB-07 runs for business date 2026-12-14
    Then the activity retries on the workflow policy with 1 s initial, back-off 2 and 10 attempts
    Then no proceeds row and no ProceedsMatched is written while no answer arrives

  Scenario: AC13 A status change the model does not allow is refused (new, D-RCV-60)
    Given plan "T-0701" is in state "PLAN_CURE_PERIOD"
    When a movement of plan "T-0701" is requested that the status model of rwb-case does not allow
    Then the movement is refused with a problem+json answer
    Then no case movement is recorded
```

AC1, AC3, AC4 and AC5 are the legacy criteria of RWB-E2-008 run across the six contracts, the ALS payment fixture and the JOB-07 window; the Givens of AC1, AC3, AC4 and AC10 that read ACE data are written against the rwb-source-data contract (DP-01, DP-05). AC10 is the journey criterion for BR8 (REC-04). AC11, AC12 and AC13 are the journey criteria for a redelivered event, an unanswered consumed call and a refused status movement; the operation that requests the movement of AC13: Not specified in the source documents (NEWAC-RWB-ITG-E2008-ITG-AC13). AC2, AC6, AC7, AC8 and AC9 are owned by the app stories of this legacy key and are cited only through their test cases TC-E2-008-02, TC-E2-008-06, TC-E2-008-07, TC-E2-008-08 and TC-E2-008-09.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A payment on the plan account for the installment amount, dated inside the window before the next due date, matches that installment | R-RES-26; row EXACT of package PAYMENT_MATCH |
| BR2 | A due date that passes, plus the grace days, with no matched payment raises PaymentMissed once | R-RES-27; REQ-CHO-007 |
| BR3 | A payment that matches no plan, sale or lot is held on the exception list for the reconciliation agent | R-UNI-03; CTL-41 |
| BR4 | A payment on an account with no open case is listed on the REC-05 business-key break and gets no proceeds row | REC-05; DQ-012 |
| BR5 | Matching runs only on a COMPLETE ACE batch; no missed payment is raised from stale data | JOB-07; CTL-02 |
| BR6 | One proceeds row per payment_code, ordered by paymentCode ascending; duplicate payment_code rows in v_ace_payment are not folded here and go to the REC-05 break list of RWB-P1-E1011-APP if the data-quality owner confirms a break; one PaymentMissed per plan and due date | R-UNI-40; ux_proceeds_payment_code |
| BR7 | Window, tolerance, grace days, partial floor and match types are columns of the package rows with a version | Principle 1; D-RCV-36 T10 |
| BR8 | Payments in v_ace_payment reconcile to proceeds by count and amount daily | REC-04 |
| BR9 | The match is decided by package PAYMENT_MATCH through RuleEvaluator; the result names rule R-RES-26 and the package version, and the decision log records both | D-RCV-36 T5, T7; ADR-012 |
| BR10 | No PAYMENT_MATCH version in force is a refusal (NoPackageInForce), never a default match | R-UNI-41; D-RCV-36 T7 |

The ten rules are unchanged by the split. The harness asserts them across the service boundaries and re-implements none of them: it reads the fired row and the version from the decision entry and never restates a window, a tolerance or a grace day in its own code.

### 9. State transitions

None for the case. This story changes no case status. The harness writes no state; the table is what it observes on the plan after a call to the owning service.

| From | Event | Condition | To |
|---|---|---|---|
| PLAN_RUNNING | PAYMENT_RECEIVED | payment matched to the installment | PLAN_RUNNING (next due date advanced, R-RES-26) |
| PLAN_RUNNING | PAYMENT_MISSED | due_date passed and no payment matched | PLAN_CURE_PERIOD (R-RES-27) |

The proceeds row carries its own match state, which the harness reads and asserts: matched_to "INSTALLMENT" on a match, matched_to "UNMATCHED" with no treatment on a held receipt.

The harness adds a run state of its own only: Not started, Seeding, Running, Passed, Failed, with the latest run for a build deciding the gate. A failed run never overwrites a passed report for the same build and business date.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| SY-RULES, Drools evaluator | Supplies the fired rule R-RES-26 and package version PM-2026.12 that the harness asserts; it is asked by rwb-payment, never by the harness |
| SY-CASEWF, case workflow module | Consumes `ProceedsMatched` and `PaymentMissed` and moves the plan route state; the harness asserts the result on the case and treatment contracts |
| SY-DECLOG, decision log writer | Writes the D5 entry the harness reads back through rwb-decision (Decision log C) |
| SY-AGENT, agent platform | Reads the exception list as the reconciliation agent would; the harness reads the same list, not the agent run |
| RW-CREDITAD, Credit Administration officer | Reads matched and unmatched receipts on SCR-28 (Write-off and posting CRUA); the synthetic user the access case refuses and allows |
| RW-CASEOWN, case owner | Reads the plan position on SCR-14 (Treatment and offer R); the role of the access refusal of TC-E2-008-10-ITG |
| RW-COE, center of excellence analyst | Owns package PAYMENT_MATCH and loads a new version (Rules and parameters CRUD); the harness seeds none of it in production and reads the version in force |
| Integration and QA team | Runs the harness, keeps the fake mappings, the payment fixture and the evidence, and owns the pass or fail gate |

No approval level from the delegation of authority applies: a match moves money inside the plan, and the harness takes no business decision. Authorisation is answered by rwb-access through the authorise operation of §12.2.

### 11. Data

The harness owns no table. It reads and asserts the fields below through the owning services' contracts; the field IDs are those of the Logical Data Model and Data Dictionary.

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-ACE-043 | v_ace_payment | payment_code | Read through the P8 proceeds operation |
| DF-ACE-044 | v_ace_payment | account_key | Read through the P8 proceeds operation |
| DF-ACE-045 | v_ace_payment | payment_date | Read through the P8 proceeds operation |
| DF-ACE-046 | v_ace_payment | payment_amount | Read through the P8 proceeds operation |
| DF-ACE-054 | v_ace_payment | data_as_of | Read through the P1 freshness operation |
| DF-ACE-028 | v_ace_account | next_installment_date | Read through the installment-facts read of rwb-source-data (RWB-P1-E2008-APP §12.1); the account resource of Architecture v5 slide 15 is unowned and unpublished (GAP-0602) |
| DF-ACE-178 | v_ace_batch_status | source_system | Read through the P1 freshness and job operations |
| DF-ACE-179 | v_ace_batch_status | business_date | Read through the P1 freshness and job operations |
| DF-ACE-182 | v_ace_batch_status | status | Read through the P1 freshness and job operations |
| DF-CAS-025 | case_account | case_id | Read through the P3 case operation |
| DF-CAS-026 | case_account | account_key | Read through the P3 case operation |
| DF-TRT-001 | treatment | id | Read through the S2 treatment operation |
| DF-TRT-004 | treatment | treatment_type | Read through the S2 treatment operation |
| DF-TRT-009 | treatment | installments | Read through the S2 treatment operation |
| DF-TRT-031 | treatment | installment_amount | Read through the S2 treatment operation |
| DF-TRT-032 | treatment | installments_paid | Read through the S2 treatment operation; written by rwb-payment through the same contract, never by the harness |
| DF-FIN-001 to DF-FIN-009 | proceeds | all fields | Read through the P8 proceeds operation; written by rwb-payment, never by the harness |
| DF-FIN-004 | proceeds | payment_code: one business-key column, varchar(255), holding the ACE payment_code, with no foreign key and no uuid cross-reference to account_payment | Read through the P8 proceeds operation |
| DF-REF-002 | rule_row | rule_id | Read through the P7 decision-log operation |
| DF-REF-003 | rule_row | rule_version | Read through the P7 decision-log operation |
| DF-REF-296 | rule_row | package_version_id | Read through the P7 decision-log operation |
| DF-REF-297 | rule_row | drools_rule_name | Read through the P7 decision-log operation |
| DF-REF-298 | rule_row | outputs | Read through the P7 decision-log operation |
| DF-DEC-004 | decision_log_entry | rule_id | Read through the P7 decision-log operation |
| DF-DEC-005 | decision_log_entry | rule_version | Read through the P7 decision-log operation |
| DF-OPS-118 to DF-OPS-129 | reconciliation_result | all fields | Read through the P1 job and data-quality operations (REC-04) |

The payment rows are read through the P1 contract over `v_ace_payment` and the proceeds through P8; the harness reads no ACE view directly and reads no `drl_source` and no workbook. This story writes no booking into ALS (the officer books the payment), ledger postings leave through rwb-integration, and the auto-debit and LED routes stay outside the 19 services until an interface is named (GAP-1631). Criteria and test data follow the same rule: every field of this section is read through its operation, never through an ACE view. DF-REF-261 to DF-REF-273 were the retired `payment_match_rule` fields and are read by no story (D-RCV-36 T10). Test data is synthetic: no production case, party, account or payment is used, and no personal data enters a run report.

### 12. Contract

#### 12.1 REST operations provided

None. The harness is a test asset in the integration pipeline and serves no operation.

#### 12.2 REST operations consumed

One hop per call, no chaining; the 2 s timeout and the circuit breaker per downstream of DP-11 apply to every row.

| Method | Path | Owner | Use |
|---|---|---|---|
| GET | `/api/recovery/payment/v1/proceeds` | P8 rwb-payment | Reads the matched and unmatched proceeds of the business date with payment code, treatment, source, amount and matched-to value (AC1, AC3, AC5) |
| POST | `/api/recovery/payment/v1/proceeds/{proceedsId}/match` | P8 rwb-payment | Drives the manual match path as a negative access control only; the automatic journey never calls it (TC-E2-008-10-ITG) |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | Reads the case, the account and the running plan position after the events |
| GET | `/api/recovery/case/v1/cases/{caseId}/timeline` | P3 rwb-case | Reads the timeline entry of the plan movement and the missed payment |
| GET | `/api/recovery/treatment/v1/treatments/{treatmentId}` | S2 rwb-treatment | Reads installment amount, installments, installments paid, treatment type and the next due date of the plan |
| GET | `/api/recovery/decision/v1/decision-log` | P7 rwb-decision | Asserts the D5 entry with rule R-RES-26 and package version PM-2026.12, and its order before the proceeds row (AC1) |
| GET | `/api/recovery/source-data/v1/data-products/freshness` | P1 rwb-source-data | Reads the freshness and batch state of "DP01 Account and arrears" and the MSG-P1-001 answer (AC5) |
| GET | `/api/recovery/source-data/v1/admin/data-quality/exceptions` | P1 rwb-source-data | Reads the REC-05 business-key break of "PAY-90003" for the data steward (AC4) |
| POST | `/api/recovery/source-data/v1/admin/jobs/{jobId}/rerun` | P1 rwb-source-data | Reruns the job of one business date for the idempotency case (AC6, cited through TC-E2-008-06-ITG) |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | Role, scope and Write-off and posting right used by the proceeds read and by the access refusal (Architecture v5: rwb-access IN POST /authorise) |

The composite screen route itself is gateway-bff (DP-19), owned by the platform edge story RWB-PLT-N001-CON. Its path and merge order are Not specified in the source documents (GAP-0393; ASM-0568).

The journey also exercises seven calls that rwb-payment consumes; the harness does not call them and they are not rows of the table above. Each is a one-hop REST contract of its owner (DP-11), except that rule evaluation runs on the embedded kit (DP-04):

- `RecoveryDataApi.paymentsLoaded`: `GET /api/recovery/source-data/v1/payments?businessDate=D`, answering `PaymentsAnswer` (RWB-P1-E2008-APP §12.1).
- `RecoveryDataApi.nextInstallmentDate`: `GET /api/recovery/source-data/v1/accounts/{accountKey}/installment-facts?businessDate=D` (RWB-P1-E2008-APP §12.1).
- `BatchStatusQuery.forSource`: the batch status is carried in `PaymentsAnswer`; a separate operation name and payload: Not specified in the source documents (GAP-1346).
- `RuleEvaluator.evaluate`, `CaseWorkflowApi.openCaseForAccount`, `TreatmentApi.runningPlans` and `TreatmentApi.recordInstallmentPaid`: published operation name and payload Not specified in the source documents (GAP-1346); the build uses their fakes on Day 1 until each owner publishes.

The two source-data reads take their element names and error answers from RWB-P1-E2008-APP, including 409 with MSG-P1-001 and MSG-P2-007 for a held run. The contract dependency and integration dependency rows of this story stay as given; the solution architect confirms the scope of RWB-P3-E2004-CON, RWB-P3-E2042-CON and RWB-P7-E1073-CON.

#### 12.3 Events published

None. The harness publishes no Kafka event of its own; the ALS payment fixture is replayed through the rwb-source-data test profile so `AceDataReady` opens the JOB-07 window.

#### 12.4 Events consumed

| Event | Topic | Owner | What the harness asserts |
|---|---|---|---|
| rwb.source-data.AceDataReady.v1 | rwb.source-data.events.v1 | P1 rwb-source-data | Opens the JOB-07 window for business date 2026-12-14 and starts the event-started workflow on queue rwb-payment (DP-10) |
| rwb.payment.ProceedsMatched.v1 | rwb.payment.events.v1 | P8 rwb-payment | One event per match with case, proceeds and amount, and one outbox row written in the same transaction as the proceeds row and the decision record (AC1) |
| rwb.payment.PaymentMissed.v1 | rwb.payment.events.v1 | P8 rwb-payment | One event per plan and due date that passed unpaid, with treatment "T-0701", due date 2026-12-15 and amount due 12,500.00; exactly one on a rerun (AC2, cited through TC-E2-008-02-ITG) |
| rwb.case.CaseStateChanged.v1 | rwb.case.events.v1 | P3 rwb-case | The plan moved PLAN_RUNNING to PLAN_CURE_PERIOD under R-RES-27 on the missed payment, and the state is visible on the case timeline |
| rwb.decision.DecisionRecorded.v1 | rwb.decision-record.v1 | P7 rwb-decision (ledger); every service publishes its own record | The D5 record of each match reaches the ledger inside the run window and names rule R-RES-26 and package version PM-2026.12 (DP-03) |
| rwb.decision.RulePackageInForce.v1 | rwb.decision.events.v1 | P7 rwb-decision | The seeded version PM-2026.12 is the version in force on the business date, and the one rwb-payment swapped in |

The harness consumes with its own consumer group and never asserts a producer's outbox row directly; consumers dedupe through their own inbox.

The harness asserts one `DecisionRecorded` shape, read by one ledger consumer group. Decision codes come from LOV-DECISION, with D5 for a match, and `inputs_ref` is read as an opaque reference to the payment facts of the business date. The input age limit is a parameter read through DP-06, and the decision-log read publishes its page default, so the harness never guesses it. The payload element names, the consumer group name, the dedupe key, the decision code of a missed payment, the parameter key and the page default value: Not specified in the source documents (GAP-2494).

#### 12.5 Workflows and activities

Observed, not built. JOB-07 Payment matching is an event-started workflow on queue `rwb-payment` in namespace `rwb-recovery`, started by `AceDataReady` for the business date, with activity `matchPayments` in rwb-payment (Architecture v5 job map; DP-10). The harness records its workflow ID, its business date and its outcome, and asserts the proceeds, the decision entry and the plan afterwards.

JOB-11 Outbox sender is observed: the harness waits for the relay window and reads the events of §12.4 off the topics; it asserts neither the relay schedule nor its state.

No workflow is built, no activity is added and no schedule is created by this story. JOB-07 belongs to RWB-P8-E2008-APP.

#### 12.6 Schedules

None. The harness adds no Schedule and no cron; it starts a run from the test pipeline and, where a version must be promoted, waits for the JOB-20 Rule promote window at 00:01 in rwb-decision and asserts `RulePackageInForce`.

#### 12.7 Tables owned

None. The harness owns no table in any schema (DP-01); it reads and writes through the operations of §12.2 only.

#### 12.8 Contract fakes

| Fake | Serves | Contract | What it answers |
|---|---|---|---|
| WireMock rwb-payment | `GET /api/recovery/payment/v1/proceeds`, `POST /api/recovery/payment/v1/proceeds/{proceedsId}/match` | OpenAPI of P8 | The matched and unmatched proceeds of business date 2026-12-14: "PAY-90001" 12,500.00 matched to INSTALLMENT for "T-0701"; "PAY-90002" 3,000.00 UNMATCHED with no treatment; "PAY-90004" matched and "PAY-90005" unmatched on 2026-12-05; 403 with MSG-P4-002 for the access refusal; a forced decision-store failure for X7 |
| WireMock rwb-source-data | `GET /api/recovery/source-data/v1/data-products/freshness`, `GET /api/recovery/source-data/v1/admin/data-quality/exceptions`, `POST /api/recovery/source-data/v1/admin/jobs/{jobId}/rerun` | OpenAPI of P1 | ALS batch of 2026-12-14 COMPLETE and of 2026-12-15 FAILED; the freshness answer with MSG-P1-001 naming "DP01 Account and arrears" and 2026-12-14; the REC-05 break of "PAY-90003" with check "References"; the rerun answer for business date 2026-12-14 |
| WireMock rwb-decision | `GET /api/recovery/decision/v1/decision-log` | OpenAPI of P7 | The D5 entry for "PAY-90001" with rule R-RES-26 and version PM-2026.12 and its timestamp before the proceeds row; no entry for the refused version case; 503 for the forced write failure |
| WireMock rwb-treatment | `GET /api/recovery/treatment/v1/treatments/{treatmentId}` | OpenAPI of S2 | "T-0701" with installment amount 12,500.00, installments 24 and installments paid 3 before the run and 4 with next due date 2027-01-15 after it |
| WireMock rwb-case | `GET /api/recovery/case/v1/cases/{caseId}`, `GET /api/recovery/case/v1/cases/{caseId}/timeline` | OpenAPI of P3 | "RC-2026-000555" with account "A-0555" and plan "T-0701"; "RC-2026-000566" with account "A-0666" and plan "T-0702"; no open case for "A-0999"; the timeline entry of the plan movement under R-RES-27 |
| WireMock rwb-access | `POST /api/recovery/access/v1/authorise` | OpenAPI of P4 | Allow RW-CREDITAD with Write-off and posting R; refuse RW-CASEOWN for Write-off and posting U with MSG-P4-002 |
| ALS payment fixture | The payment side of the journey | The rwb-source-data payments contract: `GET /api/recovery/source-data/v1/payments?businessDate=D` of RWB-P1-E2008-APP §12.1 | One file per business date holding "PAY-90001" 12,500.00 on "A-0555" dated 2026-12-14, "PAY-90002" 3,000.00, "PAY-90003" on "A-0999", "PAY-90004" and "PAY-90005" dated 2026-12-05, replayed through the rwb-source-data test profile so `AceDataReady` opens the window |

Each fake is replaced by the real service as its I story lands, without a change to the scenarios. The consumed contracts that the patterns of §13 add (RWB-P7-E1073-CON, RWB-P3-E1042-CON, RWB-P3-E1043-CON and RWB-P4-E1037-CON) are built against from Day 1 through their fakes or client libraries, and through each contract once it is published. The harness repository, its environment, the fixture file format and the evidence format: Not specified in the source documents (GAP-0393; ASM-0568).

#### 12.9 Call-type summary

| Call type | Used | Detail |
|---|---|---|
| REST | Yes | 0 provided and 10 consumed, one hop on the owner's base `/api/recovery/<short>/v1` with the 2 s timeout and the breaker of DP-11 |
| Kafka | Yes | Consumes `rwb.source-data.AceDataReady.v1`, `rwb.payment.ProceedsMatched.v1`, `rwb.payment.PaymentMissed.v1`, `rwb.case.CaseStateChanged.v1`, `rwb.decision.DecisionRecorded.v1` and `rwb.decision.RulePackageInForce.v1`; publishes nothing |
| Temporal | No | Observed only: JOB-07 Payment matching on queue `rwb-payment` and JOB-11 Outbox sender; no workflow, activity or schedule added |
| File | Yes | One ALS payment fixture per business date; no other file |

### 13. Solution plan

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision | H RWB-PLT-E1072-CON; C RWB-P7-E1073-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

How the harness applies each pattern: DP-01, it owns no table and reads no schema, every read is an operation of §12.2; DP-03, it reads the D5 entry through rwb-decision and the record on the shared topic; DP-04, it reads the fired row R-RES-26 and version PM-2026.12, never the workbook or the DRL; DP-05, it asserts payments, next installment date and batch state only through the P1 and P8 contracts; DP-06 and DP-07, any parameter or LOV the journey needs is seeded through the P3 contract as data; DP-09, it subscribes to the owner's topics and the shared topic and publishes nothing; DP-10, JOB-07 is started by `AceDataReady` and observed on queue `rwb-payment`; DP-11, every call is one hop with the 2 s timeout; DP-13, every path uses the owner's base; DP-15, it runs no migration and seeds through operations; DP-19, the journey runs through the gateway route the screens use.

The platform H dependencies named by this table (RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-E1044-CON and RWB-PLT-N001-CON) are delivered by the platform wave and are not repeated in the metadata H list. The consumed contracts the patterns add are RWB-P7-E1073-CON, RWB-P3-E1042-CON, RWB-P3-E1043-CON and RWB-P4-E1037-CON. The blocking dependencies of this story are the eight I stories, which replace the fakes one at a time.

The match record has two halves, and the harness asserts both. rwb-payment evaluates package PAYMENT_MATCH in its own worker, writes the local decision record of each match and each missed payment in its own transaction through the local library, and publishes it. rwb-decision holds the package, its rows and its test cases, collects the records, appends them to the central hash-chained ledger and runs JOB-14; it evaluates no payment, writes no proceeds row and moves no plan state.

**Harness components**

| Component | Type | Responsibility |
|---|---|---|
| JourneyRunner | Test harness | Runs one journey per business date with the run lock, the build ID and the contract versions, and stops at the first failed assertion with the trace |
| FakePack | WireMock project | Serves rwb-payment, rwb-source-data, rwb-decision, rwb-treatment, rwb-case and rwb-access from the published OpenAPI documents of §12.8 |
| PaymentFixturePack | Data | The ALS payment fixture per business date, with the payment codes, dates and amounts of the legacy section 7 scenarios, replayed through the P1 test profile |
| PackageFixture | Data | The PAYMENT_MATCH EXACT row of version PM-2026.12 as read through rwb-decision, and the empty-version state of AC8; it holds values, never a threshold in code |
| MatchAssertion | Assertion | Reads the proceeds through P8 and compares payment code, amount, source, treatment and matched-to value against the expected row |
| DecisionOrderCheck | Assertion | Reads the D5 entry and the proceeds row and fails the run when the entry does not precede the row, when the rule ID is not R-RES-26, or when the version is not PM-2026.12 |
| MissedPaymentAssertion | Assertion | Reads `PaymentMissed`, the case timeline and the plan position and fails the run when the event, the state movement under R-RES-27 or the amounts disagree |
| RunReportWriter | Reporter | Writes one run report keyed by story key and business date with the trace and the per-assertion result; format and retention Not specified in the source documents (GAP-0393; ASM-0568) |

**Environment and test data**

- Environment: SIT, one namespace, the six services deployed from their wave 2 builds or replaced by the §12.8 fakes, with the Kafka topics of the six services, the shared topic `rwb.decision-record.v1` and the Temporal namespace `rwb-recovery`. Harness repository, environment and seeding: Not specified in the source documents (GAP-0393; ASM-0568).
- Data: synthetic case "RC-2026-000555", account "A-0555", plan "T-0701" (12,500.00 THB, 24 installments, 3 paid, next due 2026-12-15), case "RC-2026-000566", account "A-0666", plan "T-0702" (12,500.00 THB, next due 2026-12-16), account "A-0999" with no open case, payments "PAY-90001" to "PAY-90005", business dates 2026-12-05, 2026-12-14 and 2026-12-15, and PAYMENT_MATCH version PM-2026.12. No production record is copied.
- Reset: each run starts from the seeded state and the fixture of one business date, so a repeated run is deterministic and produces the same report.
- Volume: the volume test of the matching run, the receipt list and the posting run takes its population as an assumption until the receipt-to-installment ratio is observed on the ACE data for a busy month and stated in the next NFR version. The assumed population is the draft estimate EST-10 of Recovery Workbench Service Volume, Calls and Temporal Sizing v1: base 13,000 and high 187,000 receipts a month (about 8,500 a business day, high), to be confirmed by the Payments and posting owner.
- Business dates: the run uses 2026-12-14 as the matched and unmatched day, 2026-12-15 as the missed payment day and the boundary day of AC7, and 2026-12-16 for the withheld batch.

**Build steps**

1. Build JourneyRunner and the contract clients against the published OpenAPI documents of the six services, with the run lock and the build ID.
2. Publish FakePack for the six services from the same documents and prove the run green from Day 1 on the fakes.
3. Write PaymentFixturePack and PackageFixture and assert that `AceDataReady` starts the workflow on queue `rwb-payment` and that the EXACT row and version PM-2026.12 are the ones in force.
4. Add AC1 with MatchAssertion and DecisionOrderCheck: the record, then the proceeds row, then `ProceedsMatched`, then the plan at installments paid 4 with next due date 2027-01-15.
5. Add the missed payment of AC2 through MissedPaymentAssertion, including the plan state under R-RES-27, and the exception path of AC3 with the unmatched read and MSG-P8-001.
6. Add AC4 with the REC-05 break read and AC5 with the withheld batch, the freshness answer and MSG-P1-001.
7. Add the rerun of AC6, the window boundary of AC7, the no-version refusal of AC8 and the access refusal, then the forced decision-log failure of X7.
8. Write RunReportWriter, attach the report to the wave 2 run record, replace each fake with the real service as its I story lands, and apply the pass or fail gate; the gate definition: Not specified in the source documents (GAP-0393; ASM-0568).

**Feature switch:** the harness has no production feature flag and runs in the test environment only. The production switch it exercises is `rwb.payments.matching` from the legacy solution plan: with the flag off, JOB-07 does not match and the harness asserts the disabled state before it asserts the enabled one. The flag is read and set through the platform feature-flag operation, never held in the harness.

**Done when:** the journey runs green against the eight deployed I stories in SIT, the run report for the business date holds every assertion of §7 and §16 with its trace, every match decision entry names R-RES-26 and PM-2026.12 before its proceeds row, every payment of the fixture is either a proceeds row or a held exception, and the pass or fail gate agreed with QA is met for one full business date.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P8-001 | Run summary with unmatched payments | {count} payments for {date} matched no plan and are on the exception list. |
| MSG-P8-002 | No PAYMENT_MATCH version in force | Payment matching for {date} did not run: no matching rule is in force. |
| MSG-P3-027 | No PAYMENT_MATCH version is in force | The {table} load was refused: {check}. The version in force is unchanged. |
| MSG-P1-001 | The ACE batch is late or not complete | {product} is from {date}. Today's load has not arrived. |
| MSG-P4-002 | The role lacks Write-off and posting R | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Decision log write failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The harness asserts the message ID and the substituted values and owns no message text. For MSG-P3-027 in this journey {table} names the package code "PAYMENT_MATCH" and {check} is "no package in force", never a payment or an account fact. Thai text for each message follows decision DL10, which is open with assumptions ASM-2250, ASM-2357, ASM-2377 and ASM-2863. For the two run messages MSG-P8-001 and MSG-P8-002, Thai wording, channel and blocking: Not specified in the source documents (GAP-1637).

### 15. Screens and states

| Screen | State | What the harness asserts |
|---|---|---|
| SCR-28 Proceeds matching | Loading | The proceeds read answers while the match of the business date is still running, and the run report records the pending day |
| SCR-28 Proceeds matching | Matched | The matched read returns "PAY-90001" of 12,500.00 for "T-0701" with the rule R-RES-26 and version PM-2026.12 from its decision entry |
| SCR-28 Proceeds matching | Unmatched | The unmatched read returns "PAY-90002" with MSG-P8-001 in the run summary; "PAY-90005" is held and "PAY-90003" is absent from the proceeds |
| SCR-28 Proceeds matching | Empty | Not specified in the source documents (CG-ALL-606) |
| SCR-28 Proceeds matching | Loading | Not specified in the source documents (CG-ALL-606) |
| SCR-28 Proceeds matching | Error | Not specified in the source documents (CG-ALL-606) |
| SCR-28 Proceeds matching | No access | A caller without the Write-off and posting right, such as RW-CASEOWN on the proceeds read, is answered with MSG-P4-002 and no data |
| SCR-14 Treatment record | Plan position | "T-0701" shows installments paid 4 and next due date 2027-01-15 after the match, and PLAN_CURE_PERIOD after the missed payment |
| SCR-14 Treatment record | Empty | Not specified in the source documents (CG-ALL-605) |
| SCR-14 Treatment record | Loading | Not specified in the source documents (CG-ALL-605) |
| SCR-14 Treatment record | Error | Not specified in the source documents (CG-ALL-605) |
| SCR-14 Treatment record | No access | A caller without the Treatment and offer right is answered with MSG-P4-002 |
| SCR-44 Run summary | Run state | The JOB-07 run of the business date shows payments read, matched, unmatched and missed, and the failed state of the no-version and decision-log cases |
| SCR-44 Run summary | Empty | Not specified in the source documents (CG-ALL-607) |
| SCR-44 Run summary | Loading | Not specified in the source documents (CG-ALL-607) |
| SCR-44 Run summary | Error | Not specified in the source documents (CG-ALL-607) |
| SCR-44 Run summary | No access | A caller without the Platform administration right is answered with MSG-P4-002 |

The harness opens no screen and renders no page; it asserts the route answers and the contracts that the screens consume. Screen-level behaviour remains with the owning APP stories. The harness environment, the composite route and the evidence detail: Not specified in the source documents (GAP-0393; ASM-0568).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-008-01-ITG | AC1, BR1, BR9 | Integration | PAY-90001 12,500.00 on A-0555 dated 2026-12-14 in the rwb-source-data contract fake; T-0701 due 2026-12-15 |
| TC-E2-008-02-ITG | AC2, BR2 (cited; owned by app story) | Integration | No payment 2026-12-05 to 2026-12-15 |
| TC-E2-008-03-ITG | AC3, BR3 | Integration | PAY-90002 3,000.00 |
| TC-E2-008-04-ITG | AC4, BR4 | Integration | PAY-90003 on A-0999 with no open case |
| TC-E2-008-05-ITG | AC5, BR5 | Integration | ACE batch for ALS of 2026-12-15 failed |
| TC-E2-008-06-ITG | AC6, BR6 (cited; owned by app story) | Integration | JOB-07 rerun for 2026-12-14 |
| TC-E2-008-07-ITG | AC7, BR1, BR7 (cited; owned by app story) | Integration | PAY-90004 10 days and PAY-90005 11 days before their due dates |
| TC-E2-008-08-ITG | AC8, BR10 (cited; owned by app story) | Integration | No PAYMENT_MATCH version in force on 2026-12-15 |
| TC-E2-008-09-ITG | AC9, BR9 (cited; owned by app story) | Integration | PAY-90001 matched under version PM-2026.12 |
| TC-E2-008-10-ITG | Access | Component | RW-CASEOWN calls GET /proceeds; refused with MSG-P4-002 |
| TC-E2-008-11-ITG | AC10, BR8 | Integration | PAY-90001 12,500.00 and PAY-90002 3,000.00 for business date 2026-12-14; REC-04 result of that date |
| TC-E2-008-12-ITG | AC11, BR6 | Integration | `AceDataReady` for business date 2026-12-14 delivered twice |
| TC-E2-008-13-ITG | AC12 | Integration | rwb-case open-case fake does not answer within 2 s |
| TC-E2-008-14-ITG | AC13 | Integration | Movement of plan T-0701 in PLAN_CURE_PERIOD that the status model of rwb-case does not allow |

The full legacy test, with its Given, When and Then, is in the legacy test case workbook, tab Story test cases, under the legacy test case ID. The Covers column names the legacy AC of RWB-E2-008 that the ITG copy is derived from; the Level column maps the legacy System level to Integration and the legacy Access level to Component. Each `-ITG` case is the journey copy of the legacy case run across the six contracts, the ALS payment fixture and the JOB-07 window, except TC-E2-008-11-ITG to TC-E2-008-14-ITG, which have no legacy case and cover AC10 to AC13 of this story.

### 17. Guardrails

- No business value in code: the tolerance 0 percent, the window of 10 days before and 0 days after, the grace of 0 days and the match types are columns of the PAYMENT_MATCH rows; the harness reads them from the fired row and holds no copy.
- No personal data in logs, events, tests, traces or reports: payments are identified by payment_code and account_key, account numbers are never logged, and the fixture and every seeded case are synthetic.
- No read of another service's schema and no direct ACE read: ACE payment, account and batch data come only through the rwb-source-data contract or the owning service's own views (DP-05), and every read of §12.2 goes through the owner's contract.
- The decision record is written before the proceeds row; DecisionOrderCheck fails the run when a proceeds row exists without its D5 entry, or when the entry names a rule or a version the package did not fire.
- One hop only: the harness fails a run when the trace shows a call chain deeper than the gateway and one owner, and it holds the 2 s budget per call.
- No second rule engine: the harness reads the rule ID and the package version through the rwb-decision contract, and no caller reads the workbook, the `drl_source` or a `rule_row` row.
- Each fake is replaced by the real service as its I story lands; a fake that outlives its service is a defect, not a configuration. The harness never runs against UAT or production, and an exception is never added to a scenario.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CHO-007 | Plan timers run from the treatment; a missed payment raises an event | Business Requirements Epic 2, sections 3.8 and 4 | FEAT-OCC-11 | 7.3 Negotiate settlement or deed in lieu | R-RES-27 | TC-E2-008-01-ITG, TC-E2-008-02-ITG, TC-E2-008-03-ITG, TC-E2-008-05-ITG, TC-E2-008-06-ITG |
| REQ-CHO-009 | Payments matched to the plan; unmatched to an exception list | Business Requirements Epic 2, sections 3.8 and 4 | FEAT-OCC-10, FEAT-PAY-01, FEAT-PAY-02 | 7.3 Negotiate settlement or deed in lieu | R-RES-26, R-UNI-03, R-UNI-40 | TC-E2-008-01-ITG, TC-E2-008-03-ITG, TC-E2-008-04-ITG, TC-E2-008-06-ITG, TC-E2-008-07-ITG, TC-E2-008-08-ITG, TC-E2-008-09-ITG, TC-E2-008-10-ITG, TC-E2-008-11-ITG |

The rule R-RES-26 and the package version on the D5 entry carry REQ-CHO-009 at the integration level, and the `PaymentMissed` event with the plan movement under R-RES-27 carries REQ-CHO-007. This story adds no requirement ID of its own and cites the legacy TCs of both requirements, including the ones owned by the app stories.

### 19. Out of scope

- The eight owning I stories RWB-P8-E2008-APP, RWB-P1-E2008-APP, RWB-S2-E2008-APP, RWB-P3-E2042-APP, RWB-P7-E2008-APP, RWB-P4-E2008-APP, RWB-P3-E2004-APP and RWB-P1-E1069-APP, and every screen, endpoint, table, migration, rule and workflow they build.
- Production code in any service: the harness is test and evidence only.
- The CON stories of rwb-payment, rwb-source-data, rwb-decision, rwb-treatment, rwb-case and rwb-access, and the OPS and INF stories of the wave.
- Platform deployment, the gateway-bff composite proceeds and exception route (RWB-PLT-N001-CON), and the platform configuration of Kafka, Temporal and the observability stack.
- The ALS system itself, its ingestion DAG and its batch record: the harness consumes what rwb-source-data publishes.
- Partial payments, late payments inside a window after the due date and the settlement, auction and enforcement proceeds (RWB-E2-027, FEAT-PAY-03, FEAT-PAY-04, Epic 4).
- Manual matching of an unmatched receipt and the reconciliation agent that works the exception list (Epic 4).
- A same-day or intraday matching run on payment received (DL06): wave 2 keeps one run per business date. Open question for the solution architect: the same-day trigger; an intraday run is added only when an interface that carries a payment during the day is named.
- The cure period and the broken plan rule (R-RES-28 to R-RES-31, FEAT-TRT-11, Epic 3), and the authoring, approval and rollback of package PAYMENT_MATCH (RWB-E2-042 and RWB-E1-073).
- The other legacy journeys of Epic 2 and their harness stories.
