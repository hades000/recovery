# RWB-ITG-E2007-ITG Booking confirmation from the ALS load

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-E2007-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W2 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-007 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP04, DP05, DP06, DP07, DP09, DP10, DP11, DP13, DP19 |
| Parallel lane | L-ITG-W2 |
| Ready to start | Day 1 |
| Sprint fit | Fits within one two-week sprint |
| Depends on (build) | None |
| Contract dependencies | RWB-P2-E2007-CON |
| Integration dependencies | RWB-P3-E2004-APP, RWB-P1-E1069-APP, RWB-P3-E2042-APP, RWB-P2-E2007-APP, RWB-P3-E2007-APP, RWB-P4-E2007-APP, RWB-S2-E2007-APP, RWB-P1-E2007-APP, RWB-P7-E2007-APP |
| External dependencies | None |
| Open decisions | DL12 (ASM-0189, ASM-2559, ASM-2608) and DL25 (ASM-0728, ASM-0735, ASM-0743, ASM-2602) proceed on their confirmed assumptions per the directive of 26 November 2026 |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to REQ-CHO-008) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-007 for the wave 2 integration harness. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (29 resolved, 31 cross-document, 3 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **member of the integration and QA team**, I want **a repeatable cross-service journey harness for booking confirmation from the ALS load that runs the BOOKING_MATCH journey across rwb-payment, rwb-source-data, rwb-decision, rwb-treatment, rwb-case and rwb-access on one business date, capturing the fired rule row, the package version, the treatment event, the case route move and the task outcomes as evidence**, so that **the BOOKING_MATCH journey is proven end to end before the wave 2 release is accepted**.

This story builds the harness and the evidence only. It builds no production endpoint, no screen, no table, no migration, no workflow and no schedule; it serves no operation, it owns no table and it starts no workflow of its own. The screens SCR-01, SCR-14 and SCR-29 are not built here, so their empty, loading, error and no-access states are not specified in this story. The real behaviour is owned by the nine I stories, and those nine stories block the ITG run:

- RWB-P3-E2004-APP: the treatment entity, the booking command and the booking difference.
- RWB-P1-E1069-APP: the read-only ACE source views and the grant the match reads them under.
- RWB-P3-E2042-APP: the rule-package authoring operation that loads, approves and rolls back the BOOKING_MATCH rows.
- RWB-P2-E2007-APP: rwb-integration, the JOB-08 trigger and the admin job catalogue the harness drives.
- RWB-P3-E2007-APP: rwb-case, the route move on BOOKING_CONFIRMED and SETTLEMENT_BOOKED, the tasks and the case timeline.
- RWB-P4-E2007-APP: rwb-access, the role, scope and right check behind the rerun refusal.
- RWB-S2-E2007-APP: rwb-treatment, the treatment state, booked at and the booking difference on the contract.
- RWB-P1-E2007-APP: rwb-source-data, the ACE account and batch-status reads, the freshness product and the reconciliation answer.
- RWB-P7-E2007-APP: rwb-decision, the decision record and the package version in force.

### 2. Business rationale

The legacy RWB-E2-007 journey is the check that every approved restructure and settlement is actually booked in the core bank. The officer books by hand in ALS (INT-03), ACE ingests the ALS batch, the booked terms appear on the account, and the Workbench compares each approved treatment with the account as ACE holds it for the business date. The legacy story carries that journey, its rule package and its task paths in one module; under the target architecture the journey crosses six services and the module no longer exists. RWB-E2-007 therefore splits into nine app stories and this integration story, and only the integration story can show the whole route.

What the harness proves, on one business date and with synthetic data:

- The composite booking and treatment route the screens consume is one hop per call and composes from rwb-case, rwb-treatment, rwb-payment and rwb-access without any service reading another service's schema.
- JOB-08 starts on `AceDataReady` for ALS with business date 2026-12-16 and takes its batch gate from rwb-source-data: a batch that is not COMPLETE starts nothing.
- BOOKING_MATCH fires with its row and its package version on the evidence: the SETTLEMENT row confirming a booking, the RESTRUCTURE row returning NO_BOOKING and TERMS_DIFFER, and version BKG-2026.12 named on the result and on the decision record.
- TreatmentBooked leaves rwb-payment exactly once per confirmed treatment with business date 2026-12-16, and the case route moves from WITH_OPS_SETTLEMENT to AWAITING_PAYMENT on SETTLEMENT_BOOKED.
- A missing booking raises one task the officer can see, a differing term raises one task for Credit Administration, and a partly booked case names the accounts without a booking.
- The decision record is written before the treatment change, so a booking that cannot be logged does not proceed and no TreatmentBooked is published.
- The ALS batch COMPLETE gate holds: no run and no missing-booking task for a business date whose batch ended FAILED.
- REC-03 is visible at the integration level: an approved treatment still missing after two batches appears on the break list for the data steward.
- REQ-CHO-008 is met at the integration level, with every business rule, message and screen behaviour left where the owning stories put them.

The measure is the legacy one: REC-03, approved treatments against bookings, zero after two days. The harness is the place where the six service boundaries are exercised together, so a broken boundary is found in SIT and not by a settlement that is silently never confirmed.

### 3. Preconditions

- The nine I stories are published and deployed in the SIT environment, or their published contracts and the §12.8 fakes stand in for them from Day 1: RWB-P3-E2004-APP (treatment entity, booking command, booking difference), RWB-P1-E1069-APP (read-only ACE source views and the grant), RWB-P3-E2042-APP (rule-package authoring and the BOOKING_MATCH rows), RWB-P2-E2007-APP (rwb-integration job catalogue and the JOB-08 trigger), RWB-P3-E2007-APP (rwb-case route move, tasks, timeline), RWB-P4-E2007-APP (rwb-access authorise), RWB-S2-E2007-APP (rwb-treatment), RWB-P1-E2007-APP (rwb-source-data freshness and reconciliation) and RWB-P7-E2007-APP (rwb-decision record and registry).
- Package BOOKING_MATCH version "BKG-2026.12" is in force for the business date, with a RESTRUCTURE row comparing tdr_flag, last_tdr_date and principal_outstanding against offer_amount and interest_rate against the approved rate, a SETTLEMENT row comparing settlement_booked_date and settlement_booked_amount against offer_amount, and tolerance 0.00 baht (DL25). The rows are loaded, approved and promoted by the owning stories; the harness only seeds and reads them.
- The ACE batch for ALS with business date 2026-12-16 is COMPLETE, and the batch for 2026-12-17 ended FAILED so the gate case can be asserted.
- Synthetic data only: settlement treatment TRT-SYN-0701 on case RW-2026-000701 with offer amount 650,000.00 baht and synthetic account A-0701; restructure treatment TRT-SYN-0702 on synthetic account A-0702 with tdr_flag false; restructure treatment TRT-SYN-0703 on A-0703 with rate 4.5000 booked against 4.2500 approved; treatment TRT-SYN-0704 covering A-0704 and A-0705 with only A-0704 booked. No production case, account, party or payment is used.
- The test users hold the roles the journey asserts: RW-RESTRUCT for the missing-booking task, RW-CREDITAD for the differing-terms task, RW-DATASTEW for the REC-03 break list, RW-PLATADM for the rerun, and RW-CASEOWN for the refusal case.
- The harness environment, its repository, its test-data seeding, its evidence format and retention, and its pass/fail gate: Not specified in the source documents (GAP-0395; ASM-0570).
- No build dependency. Day 1.

### 4. Flow

1. Harness: takes the run lock for the environment, records the build ID, the business date and the versions of the six service contracts it is about to exercise, and reseeds the state so the run is deterministic.
2. Harness: seeds the approved treatments TRT-SYN-0701, TRT-SYN-0702, TRT-SYN-0703 and TRT-SYN-0704, their cases and accounts, the approval dates, the BOOKING_MATCH version "BKG-2026.12" with its RESTRUCTURE and SETTLEMENT rows, and the ACE facts for business date 2026-12-16 through the owning contracts or the §12.8 fakes; reads each item back and asserts the seeded state.
3. Harness: asserts the batch gate through the rwb-source-data freshness answer — the batch for 2026-12-16 is COMPLETE and the batch for 2026-12-17 ended FAILED — and records the product, the business date and the completeness flag on the evidence.
4. Harness: opens the JOB-08 window by publishing `AceDataReady` for 2026-12-16 on `rwb.source-data.events.v1`, confirms the JOB-08 entry and its owner on the rwb-integration job catalogue, and records the workflow ID of the event-started run on queue `rwb-integration`. The JOB-08 owner conflict is recorded: Architecture v5 slide 44 names rwb-payment the owner of JOB-08 while the workflow is registered on rwb-integration (GAP-0659).
5. Harness: asserts the fired row and the package version — the SETTLEMENT row of "BKG-2026.12" decides TRT-SYN-0701 as booked, and the RESTRUCTURE row returns NO_BOOKING for TRT-SYN-0702 and TERMS_DIFFER with approved rate 4.2500 and booked rate 4.5000 for TRT-SYN-0703 — on the decision record read through rwb-decision. Harness also asserts one `rwb.decision.BookingDecisionMade.v1` event per treatment and business date on `rwb.decision.events.v1`, keyed by treatmentId, carrying the outcome, the row, the package code and version, the business date and the difference terms.
6. Harness: asserts the decision record precedes the treatment change, then asserts TreatmentBooked with business date 2026-12-16 on `rwb.payment.events.v1`, the treatment state BOOKED with booked at 2026-12-16 through rwb-treatment, and the case route move from WITH_OPS_SETTLEMENT to AWAITING_PAYMENT with the CaseStateChanged event and the timeline entry.
7. Harness: asserts the task outcomes through rwb-case — one open task WITH_OPS_BOOKING for RW-RESTRUCT carrying MSG-P2-011, one open task UNMATCHED_EXCEPTION for RW-CREDITAD carrying MSG-P2-012 with the term, the booked value and the approved value, and the accounts without a booking named on the partly booked case.
8. Harness: asserts the incomplete-batch no-run — no JOB-08 run for 2026-12-17, no missing-booking task for that date and MSG-P1-001 on the freshness answer — and asserts the no-package case, where a run with no BOOKING_MATCH version in force ends failed with MSG-P3-027 and no treatment marked booked, no difference written and no task raised.
9. Harness: reruns JOB-08 for 2026-12-16 through the rerun operation and asserts no second TreatmentBooked, no second decision record and no task; then asserts the next batch for 2026-12-17 with the booking still missing raises no second task, that the open task stays, and that the REC-03 break list shows TRT-SYN-0702 as missing for 2 days.
10. Harness: forces the decision-log failure, asserts the treatment stays APPROVED, no TreatmentBooked is published, MSG-P7-003 is raised and the match runs again with the next batch; asserts the access refusal for RW-CASEOWN with MSG-P4-002; then returns every fake to its healthy answer.
11. Harness: writes one run report per business date keyed by story and business date, evaluates the pass/fail gate, attaches the report to the wave 2 release record and releases the run lock. The report format, the retention and the gate definition: Not specified in the source documents (GAP-0395; ASM-0570).

### 5. Exception paths

| ID | Trigger | What the harness asserts | Message | ITG test case | Covered by |
|---|---|---|---|---|---|
| X1 | AC2: no booking appears in the next batch for TRT-SYN-0702 | The RESTRUCTURE row returns NO_BOOKING; one task WITH_OPS_BOOKING for RW-RESTRUCT; the treatment stays APPROVED | MSG-P2-011 | TC-E2-007-02-ITG | AC2 |
| X2 | AC3: a booked term differs from the approved term | TERMS_DIFFER with approved rate 4.2500 and booked rate 4.5000; the difference on the treatment; one task UNMATCHED_EXCEPTION for RW-CREDITAD; the treatment stays APPROVED | MSG-P2-012 | TC-E2-007-03-ITG | AC3 |
| X3 | AC4: only some accounts of the case are booked | The treatment stays APPROVED and the task for RW-RESTRUCT names A-0705 as not booked | MSG-P2-011 | TC-E2-007-04-ITG | AC4 |
| X4 | AC5: the ACE batch for ALS with business date 2026-12-17 ended FAILED | No JOB-08 run for 2026-12-17, no missing-booking task for that date, MSG-P1-001 on the freshness answer | MSG-P1-001 | TC-E2-007-05-ITG | AC5 |
| X5 | AC6: JOB-08 is rerun for 2026-12-16 after it marked TRT-SYN-0701 booked | No second TreatmentBooked, no second decision record, no task, and one outbox delivery on the integration catalogue | None | TC-E2-007-06-ITG | AC6 |
| X6 | AC7: the batch of 2026-12-17 still shows no booking for TRT-SYN-0702 | No second task; the open task stays; the REC-03 break list shows TRT-SYN-0702 as missing for 2 days | None | TC-E2-007-07-ITG | AC7 |
| X7 | AC8: the decision log store is unavailable when the match finds TRT-SYN-0701 booked | The treatment stays APPROVED and no TreatmentBooked is published; an incident is raised; the match runs again with the next batch | MSG-P7-003 | TC-E2-007-08-ITG | AC8 |
| X8 | AC9: no BOOKING_MATCH version is IN_FORCE on the business date | The run ends failed with NoPackageInForce; no treatment marked booked, no difference written, no task raised; the alert names RW-PLATADM | MSG-P3-027 | TC-E2-007-09-ITG | AC9 |
| X9 | A role without the right reruns JOB-08 (RW-CASEOWN) | The rerun is refused through rwb-access; no run, no event and no task; the job state is unchanged | MSG-P4-002 | TC-E2-007-10-ITG | Not specified in the source documents (DOR-RWB-ITG-E2007-ITG-3) |
| X10 | Principle 5: the decision record cannot be written for a confirmed booking | The markBooked path does not proceed; the treatment stays APPROVED, no TreatmentBooked and no outbox delivery exist, and the run reports the failure as a defect rather than a pass | MSG-P7-003 | TC-E2-007-11-ITG | Not specified in the source documents (DOR-RWB-ITG-E2007-ITG-3) |
| X11 | The seed pack cannot be loaded, another run holds the environment lock, or the evidence cannot be attached to the release record | The run refuses to start and names the missing seed item or the lock holder, or is marked failed with the local evidence kept for rerun; no scenario is reported as passed | None | All | Not specified in the source documents (DOR-RWB-ITG-E2007-ITG-3) |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Runs on its own once the nine published contracts or the §12.8 fakes exist; it builds no service feature and has no build dependency |
| Negotiable | The seeded treatments, the batch fixtures, the expected rows and the evidence layout are data files, never code |
| Valuable | The booking journey is proven once across six services, with the fired row and the package version on the evidence |
| Estimable | One journey runner, one fake pack, one fixture set, one assertion set, one report writer |
| Small | Fits in one iteration with the owning stories' contract tests |
| Testable | Each owned criterion is one automated journey with synthetic data and a machine-checkable result |

### 7. Acceptance criteria

```gherkin
Feature: Booking confirmation from the ALS load - wave 2 integration harness

  Background:
    Given package "BOOKING_MATCH" version "BKG-2026.12" is in force with the RESTRUCTURE and SETTLEMENT rows and tolerance 0.00 baht
    Given the ACE batch for ALS with business date 2026-12-16 is COMPLETED

  Scenario: AC1 Booking confirmed (legacy RWB-E2-007 AC1)
    Given settlement treatment "TRT-SYN-0701" on case "RW-2026-000701" was approved on 2026-12-15 with offer amount 650,000.00 baht
    Given the officer booked the settlement in ALS on 2026-12-16
    Given the rwb-source-data contract returns settlement booked date 2026-12-16 and settlement booked amount 650,000.00 baht for synthetic account "A-0701" at business date 2026-12-16
    When the next day's ALS batch is complete and JOB-08 runs on 2026-12-17
    Then the SETTLEMENT row of package "BOOKING_MATCH" version "BKG-2026.12" decides that the account is booked
    Then the booked terms match the approved treatment and the treatment state is "BOOKED" with booked at 2026-12-16
    Then the system publishes treatmentBooked with business date 2026-12-16
    Then the route state moves from "WITH_OPS_SETTLEMENT" to "AWAITING_PAYMENT" by R-SET-13 with a decision log entry

  Scenario: AC5 ACE batch not complete (legacy RWB-E2-007 AC5)
    Given the ACE batch for ALS with business date 2026-12-17 ended "FAILED"
    When JOB-08 is due on 2026-12-18
    Then JOB-08 does not run for 2026-12-17
    Then the system raises no missing booking task for 2026-12-17

  Scenario: AC7 Booking still missing on the next batch (legacy RWB-E2-007 AC7)
    Given task "WITH_OPS_BOOKING" is open for "TRT-SYN-0702" from the batch of 2026-12-16
    When the batch of 2026-12-17 still shows no booking
    Then the system raises no second task
    Then the REC-03 break list for the data steward shows "TRT-SYN-0702" as missing for 2 days

  Scenario: AC10 Duplicate delivery of a consumed event (new, D-RCV-60)
    When the same consumed event is delivered a second time
    Then the system applies the event once and creates no second booking effect

  Scenario: AC11 Consumed call fails or does not answer (new, D-RCV-60)
    Given the rwb-source-data contract call fails or gets no answer for synthetic account "A-0701" at business date 2026-12-16
    When JOB-08 runs on 2026-12-17
    Then treatment "TRT-SYN-0701" stays in state "APPROVED" and no TreatmentBooked event is published

  Scenario: AC12 Status change the model does not allow is refused (new, D-RCV-60)
    Given treatment "TRT-SYN-0701" is in state "APPROVED"
    When a status change is requested that the state model does not allow
    Then the change is refused and the treatment state stays unchanged
```

AC1, AC5 and AC7 above are the legacy criteria of RWB-E2-007, run across the six service contracts; AC5 and AC7 are copied unchanged, and the AC1 Given reads through the rwb-source-data contract. They are ITG criteria, not APP criteria: each Given is a seeded fact of the environment and none of them is a contract mock. AC2, AC3, AC4, AC6, AC8 and AC9 are owned by the app stories of this legacy key and are cited only through their test cases TC-E2-007-02, -03, -04, -06, -08 and -09.

Legacy levels map as System to Component, Access to Contract and Resilience to NFR (GAP-2490).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Bookings are made by the officer in ALS and confirmed only from the next ACE batch | INT-03; DL12; D-RCV-35 U1 |
| BR2 | A restructure is booked when every account matches the RESTRUCTURE rows of package BOOKING_MATCH: tdr_flag true with a last TDR date on or after the approval date and the terms equal | DF-ACE-031; DF-ACE-030; CTL-26; D-RCV-36 T5 |
| BR3 | A settlement is booked when the account matches the SETTLEMENT rows of package BOOKING_MATCH: a settlement booked date on or after the approval date and a booked amount equal to the offer amount | R-SET-13; D-RCV-36 T5 |
| BR4 | The tolerance on amounts and rates is zero in the row of package BOOKING_MATCH in force | DL25 |
| BR5 | A missing booking after the grace batches raises one task to the officer | REC-03; parameter booking.missing.grace_loads |
| BR6 | A difference in terms raises one task to Credit Administration | REC-03; FEAT-CHO-08 |
| BR7 | A confirmed booking moves the case | R-RES-22, R-SET-13 |
| BR8 | No missing booking is raised for a business date whose ACE batch for ALS is not COMPLETE | JOB-08; CTL-02 |
| BR9 | A decision that cannot be written to the decision log does not proceed | Principle 5; R-UNI-39 |
| BR10 | The match is decided by package BOOKING_MATCH through RuleEvaluator; the result names the row and the package version, and the story holds no comparison code and no rule table | D-RCV-36 T3, T5; ADR-012 |
| BR11 | No BOOKING_MATCH version in force is a refusal (NoPackageInForce), never a default match | R-UNI-41; D-RCV-36 T7 |

The rules are unchanged by the split. The harness asserts these eleven rules against the owning services and re-implements none of them: the tolerance, the grace and the compared terms are read from the row the package fired, never restated in the harness.

### 9. State transitions

None for the case. The harness changes no case, treatment, task or event itself; it observes the owning services and asserts the result.

| From | Event | Condition | To |
|---|---|---|---|
| WITH_OPS_BOOKING | BOOKING_CONFIRMED | NLEADS result APPROVED recorded and every account matched | BOOKED_IN_ALS_NLEADS |
| WITH_OPS_SETTLEMENT | SETTLEMENT_BOOKED | Agreement signed and terms booked in ALS | AWAITING_PAYMENT |

The treatment state moves from APPROVED to BOOKED on a confirmed booking. A missing or differing booking leaves both the route state and the treatment state unchanged. The harness asserts each row after the call and asserts that the row is unchanged after a missing booking, a differing term, a refused rerun and a failed decision-log write.

The harness adds a run state of its own only: Not started, Seeding, Running, Passed, Failed, with the latest run for a build deciding the gate.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| SY-RULES, Drools evaluator | Supplies the fired row, the outcome and the package version the harness asserts; it evaluates nothing for the harness |
| SY-CASEWF, case workflow module | Writes the route move and the tasks the harness asserts (Queue and allocation CRU) |
| SY-DECLOG, decision log writer | Writes the entry the harness reads back, and the entry whose failure stops the booking (Decision log C) |
| RW-RESTRUCT, restructuring officer | The role the missing-booking task is raised for; the harness seeds the role, never a person |
| RW-CREDITAD, Credit Administration officer | The role the differing-terms task is raised for |
| RW-DATASTEW, data steward | Reads the REC-03 break list the harness asserts |
| RW-PLATADM, platform administrator | The role that may rerun JOB-08; the harness seeds it for the rerun case and asserts the refusal for RW-CASEOWN (Platform administration, U) |
| Integration and QA team (RW-TRIBE squad members and the QA lead) | Runs the harness, keeps the fake mappings, the seed pack and the evidence, and owns the run report and the gate |

No approval level from the delegation of authority applies: the journey takes no business decision of its own. Authorisation is answered by rwb-access through the authorise operation of §12.2.

### 11. Data

The harness owns no table. It reads the fields below through the owning services' contracts and asserts them; the field IDs are those of the Logical Data Model and Data Dictionary.

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-TRT-001 | treatment | id | Read through the rwb-treatment contract |
| DF-TRT-002 | treatment | case_id | Read through the rwb-treatment contract |
| DF-TRT-004 | treatment | treatment_type | Read through the rwb-treatment contract |
| DF-TRT-007 | treatment | offer_amount | Read through the rwb-treatment contract |
| DF-TRT-012 | treatment | booked_at | Read through the rwb-treatment contract; written by rwb-treatment, never by the harness |
| DF-TRT-027 | treatment | interest_rate | Read through the rwb-treatment contract |
| DF-TRT-028 | treatment | booking_difference | Read through the rwb-treatment contract |
| Standard column | treatment | state | Read through the rwb-treatment contract |
| DF-CAS-026 | case_account | account_key | Read through the rwb-case contract |
| DF-ACE-001 | v_ace_account | account_key | Read through the rwb-source-data contract |
| DF-ACE-025 | v_ace_account | interest_rate | Read through the rwb-source-data contract |
| DF-ACC-009 | loan_account | principal_outstanding | Read through the rwb-source-data contract (Section B, RWB-ACE-001); ACE view column v_ace_account.principal_outstanding |
| DF-ACE-031 | v_ace_account | tdr_flag | Read through the rwb-source-data contract |
| DF-ACE-030 | v_ace_account | last_tdr_date | Read through the rwb-source-data contract |
| DF-ACE-036 | v_ace_account | data_as_of | Read through the rwb-source-data contract |
| DF-ACC-030 | loan_account | settlement_booked_date | Read through the rwb-source-data contract (Section B, RWB-ACE-001); ACE view column v_ace_account.settlement_booked_date |
| DF-ACC-031 | loan_account | settlement_booked_amount | Read through the rwb-source-data contract (Section B, RWB-ACE-001); ACE view column v_ace_account.settlement_booked_amount |
| DF-ACE-178 | v_ace_batch_status | source_system | Read through the rwb-source-data freshness answer |
| DF-ACE-179 | v_ace_batch_status | business_date | Read through the rwb-source-data freshness answer |
| DF-ACE-182 | v_ace_batch_status | status | Read through the rwb-source-data freshness answer |
| DF-ACE-186 | v_ace_batch_status | is_complete | Read through the rwb-source-data freshness answer |
| DF-REF-002 | rule_row | rule_id | Read through the rwb-decision contract |
| DF-REF-003 | rule_row | rule_version | Read through the rwb-decision contract |
| DF-WRK-018 | task | case_id | Read through the rwb-case contract |
| DF-WRK-019 | task | task_code | Read through the rwb-case contract |
| DF-WRK-022 | task | status | Read through the rwb-case contract |
| DF-WRK-023 | task | owner_role | Read through the rwb-case contract |
| DF-OPS-118 to DF-OPS-129 | reconciliation_result | all fields | Read through the rwb-source-data reconciliation answer (REC-03) |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Read through the rwb-decision contract |

The matching row and its version are read only through the rwb-decision contract; the harness reads no rule_row row directly, no drl_source and no workbook. Test data is synthetic: the treatments, cases, accounts and business dates of §3 and §7 only. No production case, party or account is used, and no personal data is written to a run report.

### 12. Contract

#### 12.1 REST operations provided

None. The harness is a test asset in the integration pipeline; it serves no operation.

#### 12.2 REST operations consumed

One hop per call, no chaining; the 2 s timeout and the circuit breaker per downstream of DP-11 apply to every row.

Contract version: every row is pinned to the /v1 path of its owner's contract, and every event in §12.4 is a v1 event type; no other version is named.

| Method | Path | Owner | Use |
|---|---|---|---|
| GET | `/api/recovery/integration/v1/admin/scheduled-jobs` | P2 rwb-integration | The JOB-08 entry, its owning service rwb-payment, its trigger and its last run status, so a run for 2026-12-16 and the absence of a run for 2026-12-17 are on the evidence |
| POST | `/api/recovery/source-data/v1/admin/jobs/{jobId}/rerun` | P1 rwb-source-data | Drives the AC6 rerun of JOB-08 for 2026-12-16 and the access refusal of X9; Idempotency-Key per job and business date |
| GET | `/api/recovery/source-data/v1/data-products/freshness` | P1 rwb-source-data | The ALS batch status, business date and completeness behind AC5 and X4, and the REC-03 reconciliation answer for the business date |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The route state before and after a confirmed booking, and the unchanged route state after a missing or differing booking |
| GET | `/api/recovery/case/v1/cases/{caseId}/timeline` | P3 rwb-case | The route move, the task and the REC-03 evidence as the case shows them |
| GET | `/api/recovery/case/v1/me/tasks` | P3 rwb-case | The one open task WITH_OPS_BOOKING for RW-RESTRUCT, the differing-terms task for RW-CREDITAD, and the absence of a second task |
| GET | `/api/recovery/treatment/v1/treatments/{treatmentId}` | S2 rwb-treatment | The treatment state APPROVED or BOOKED, booked at 2026-12-16 and the booking difference of the differing case |
| GET | `/api/recovery/decision/v1/decision-log` | P7 rwb-decision | The fired row and package version BKG-2026.12 on the record of the confirmed booking, its precedence over the treatment change, and the absence of a record on a refused run |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | The role, scope and right check behind the rerun refusal of X9 |
| GET | `/api/recovery/integration/v1/admin/outbox/deliveries` | P2 rwb-integration | One TreatmentBooked delivery per confirmed treatment, and no second delivery on the rerun or on the failed decision-log write |

The composite booking and treatment route that the screens consume is gateway-bff (DP-19), owned by the platform edge story RWB-PLT-N001-CON. Its path and its merge order: Not specified in the source documents (GAP-0395; ASM-0570).

#### 12.3 Events published

None. The harness publishes no Kafka event of its own; its fixture publishes `AceDataReady` through the rwb-source-data test profile only, and the evidence leaves through the pipeline.

#### 12.4 Events consumed

| Event | Topic | Owner | What the harness asserts |
|---|---|---|---|
| `rwb.source-data.AceDataReady.v1` | `rwb.source-data.events.v1` | P1 rwb-source-data | Opens the JOB-08 window for business date 2026-12-16 and starts the event-started workflow on queue `rwb-payment`; no window opens for the FAILED batch of 2026-12-17 |
| `rwb.treatment.TreatmentApproved.v1` | `rwb.treatment.events.v1` | S2 rwb-treatment | The approval date (2026-12-15) that the match uses against the booked date |
| `rwb.payment.TreatmentBooked.v1` | `rwb.payment.events.v1` | P8 rwb-payment | Exactly one event per confirmed treatment with treatmentId, bookingRef (account_key + business date) and businessDate 2026-12-16; none on the rerun, none on the failed decision-log write and none for a treatment left APPROVED |
| `rwb.case.CaseStateChanged.v1` | `rwb.case.events.v1` | P3 rwb-case | The route move WITH_OPS_SETTLEMENT to AWAITING_PAYMENT on SETTLEMENT_BOOKED, and no move on a missing or differing booking |
| `rwb.decision.DecisionRecorded.v1` | `rwb.decision-record.v1` | P7 rwb-decision (ledger); every service publishes its own record | The record of the confirmed booking reaches the ledger and names the fired row and package version BKG-2026.12, in the order recorded by §12.2 |
| `rwb.decision.RulePackageInForce.v1` | `rwb.decision.events.v1` | P7 rwb-decision | The seeded version BKG-2026.12 is the version in force that the owning service swapped in |

Consumers dedupe through their own inbox table; the harness consumes with its own group and never asserts a producer's outbox row directly.

#### 12.5 Workflows and activities

JOB-08 Booking confirmation is exercised, not built: an event-started workflow on queue `rwb-payment`, started by `AceDataReady` for the business date. The harness records the workflow ID, the business date and the outcome of the run, and asserts the booking, the event and the route move afterwards. JOB-11 Outbox sender is observed: the harness waits for the relay window and reads the deliveries off the integration catalogue and the topics.

No workflow is built, no activity is added and no schedule is created by this story. JOB-08 and its activities belong to RWB-P2-E2007-APP.

#### 12.6 Schedules

None. The harness starts no Schedule. JOB-20 Rule promote (00:01 in rwb-decision) is the mechanism that puts a package version in force; where the seeded version has to be promoted inside the run, the harness waits for that window and asserts `RulePackageInForce`, and adds no Schedule of its own.

#### 12.7 Tables owned

None. The harness owns no table in any schema (DP-01); it seeds and reads through the operations of §12.2 only.

#### 12.8 Contract fakes

| Fake | Serves | Stubbed answers |
|---|---|---|
| WireMock rwb-payment | `rwb.payment.events.v1`, the booking side of JOB-08 | One TreatmentBooked for TRT-SYN-0701 with bookingRef A-0701 and businessDate 2026-12-16; no event on the rerun, on the failed decision-log write or for a treatment left APPROVED |
| WireMock rwb-source-data | `/api/recovery/source-data/v1/data-products/freshness`, `/api/recovery/source-data/v1/admin/jobs/{jobId}/rerun` | ALS batch 2026-12-16 COMPLETED and 2026-12-17 FAILED with MSG-P1-001 on the freshness answer; the REC-03 answer with TRT-SYN-0702 missing for 2 days; 202 on a rerun, 409 with MSG-P2-006 while the run is open |
| WireMock rwb-decision | `/api/recovery/decision/v1/decision-log` | The records of the confirmed booking with the fired SETTLEMENT or RESTRUCTURE row and version BKG-2026.12; no record when the write is forced to fail; the absence of a record on a refused run |
| WireMock rwb-treatment | `/api/recovery/treatment/v1/treatments/{treatmentId}` | TRT-SYN-0701 BOOKED with booked at 2026-12-16; TRT-SYN-0702 and TRT-SYN-0703 APPROVED; the booking difference with approved rate 4.2500 and booked rate 4.5000 on TRT-SYN-0703 |
| WireMock rwb-case | `/api/recovery/case/v1/cases/{caseId}`, `/cases/{caseId}/timeline`, `/me/tasks` | RW-2026-000701 route state WITH_OPS_SETTLEMENT before and AWAITING_PAYMENT after the move; the one open task WITH_OPS_BOOKING for RW-RESTRUCT with MSG-P2-011; the differing-terms task for RW-CREDITAD with MSG-P2-012; no second task on the rerun or the second batch |
| WireMock rwb-access | `/api/recovery/access/v1/authorise` | Allow RW-PLATADM the Platform administration U right for JOB-08; refuse RW-CASEOWN with MSG-P4-002 |
| Integration job catalogue fake | `/api/recovery/integration/v1/admin/scheduled-jobs`, `/admin/outbox/deliveries` | The JOB-08 entry owned by rwb-payment with its trigger and last run status; one outbox delivery per confirmed treatment and no second delivery |
| Environment and evidence stand-in | The run lock, the seed pack and the report target | Placeholder pair only: the harness repository, its environment, its seeding, its evidence format and retention and its gate are Not specified in the source documents (GAP-0395; ASM-0570) |

Each fake is replaced by the real service as its I story lands, contract by contract, without a change to the scenarios.

The Integration lead and the QA lead agree the following at the wave 2 entry check (GAP-0395): the composite booking and treatment route path and its merge order, agreed with the platform edge story; the harness environment; the ALS booking fixture format; the seed pack; the evidence format and retention; and the pass or fail gate. The result is recorded in the booking confirmation harness pack before the first real-service run.

#### 12.9 Call-type summary

| Call type | Used | Detail |
|---|---|---|
| REST | Yes | Ten consumed operations of §12.2 through gateway-bff and the owning services; one hop, 2 s timeout, breaker per downstream |
| Kafka | Yes | Consumes six events across `rwb.source-data.events.v1`, `rwb.treatment.events.v1`, `rwb.payment.events.v1`, `rwb.case.events.v1`, `rwb.decision-record.v1` and `rwb.decision.events.v1`; publishes none |
| Temporal | Observed only | Observes JOB-08 Booking confirmation on queue `rwb-payment` and JOB-11 Outbox sender; starts no workflow, adds no activity and creates no Schedule |
| File | No | Reads and writes no business file; the evidence report is a pipeline artefact of the run, not an interface |

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
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The platform H dependencies named by this table are delivered by the platform wave and are not repeated in the metadata H list. The blocking dependencies of this story are the nine I stories, which replace the fakes with real services one at a time.

**Placement of package BOOKING_MATCH (GAP-2485):** the booking-confirmation slice under test evaluates BOOKING_MATCH in rwb-decision on the version it holds, through the embedded kit, and publishes the outcome; the treatment state, the task, the route move and the posting stay with their owners.

**Harness components**

| Component | Type | Responsibility |
|---|---|---|
| JourneyRunner | Test harness | Runs steps 1 to 11 for one scenario and one business date, with the run lock and the build ID, and stops at the first failed assertion with the trace |
| FakePack | WireMock project | Serves rwb-payment, rwb-source-data, rwb-decision, rwb-treatment, rwb-case, rwb-access and the integration job catalogue from the published OpenAPI documents of §12.8 |
| BookingFixture | Data | The seeded treatments, cases, accounts, approval dates, the BOOKING_MATCH version and rows, and the ALS batch status per business date |
| TreatmentBookedAssertion | Assertion | Asserts exactly one TreatmentBooked per confirmed treatment with the business date and booking reference, and none on the rerun or the failed write |
| DecisionOrderCheck | Assertion | Fails the run when the decision record does not precede the treatment change, when there is more than one record for one treatment and business date, or when the record names no fired row or no package version |
| TaskAssertion | Assertion | Asserts the task code, the owner role, the message ID, the named accounts and the absence of a second task |
| RejectedRunCheck | Assertion | Asserts the gate cases: no run on a batch that is not COMPLETE, a failed run with NoPackageInForce when no version is in force, and a refused rerun with the job state unchanged |
| RunReportWriter | Reporter | Writes one run report per business date with the trace and the per-assertion result; format and retention Not specified in the source documents (GAP-0395; ASM-0570) |

**Environment and test data**

- Environment: SIT, one namespace, the wave 2 harness profile, the six owning services deployed from their wave 2 builds or replaced by the §12.8 fakes. Harness repository, environment, seeding and gate: Not specified in the source documents (GAP-0395; ASM-0570).
- Data: synthetic treatments TRT-SYN-0701 (settlement, 650,000.00 baht), TRT-SYN-0702 (restructure, no booking), TRT-SYN-0703 (restructure, rate 4.5000 booked against 4.2500 approved) and TRT-SYN-0704 (two accounts, one booked); case RW-2026-000701; accounts A-0701 to A-0705; BOOKING_MATCH version BKG-2026.12 with the RESTRUCTURE and SETTLEMENT rows and tolerance 0.00 baht; ALS batches 2026-12-16 COMPLETED and 2026-12-17 FAILED.
- Reset: each run starts from the seeded state, so a repeated run is deterministic and the same report is produced; the run lock keeps two runs of the environment apart.

**Build steps**

1. Build JourneyRunner and FakePack against the published OpenAPI documents of the six services and the integration job catalogue, and prove the harness runs green from Day 1 on the fakes.
2. Write BookingFixture for treatments, cases, accounts, approval dates, the BOOKING_MATCH version and rows and the two ALS batch dates, and a test that a bad seed stops the run (X11).
3. Add the AC1 journey with DecisionOrderCheck and TreatmentBookedAssertion: fired SETTLEMENT row, version BKG-2026.12, treatment BOOKED at 2026-12-16, one TreatmentBooked, route move to AWAITING_PAYMENT and the timeline entry.
4. Add the missing and differing set of X1, X2 and X3 through TaskAssertion, asserting the task code, the owner role, the message ID, the named accounts and the unchanged treatment and route state.
5. Add the gate cases of X4 and X8 through RejectedRunCheck: no run for a batch that ended FAILED, and a failed run with MSG-P3-027 when no BOOKING_MATCH version is in force.
6. Add the rerun and the second batch of X5 and X6: no second TreatmentBooked, no second decision record, no second outbox delivery and no second task, with the REC-03 break list showing 2 days.
7. Add the failure and refusal cases of X7, X9 and X10: the forced decision-log failure, the RW-CASEOWN refusal with MSG-P4-002 and the Principle 5 forced failure.
8. Write RunReportWriter and the gate, replace each fake with the real service as its I story lands, and rerun the whole journey on the release build.

**Feature switch:** the production switch this journey exercises is `rwb.integration.booking-confirmation` from the legacy solution plan; with it off, no booking confirmation runs for the business date, so the run is expected to fail and the gate reports it rather than hiding it. The harness has no production feature flag of its own and runs in the test environment only.

**Done when:** the journey runs green against the nine deployed I stories in SIT, the run report for the business date holds every assertion of §5, §7 and §16 with its trace, every confirmed booking names the fired row and the package version in force, and each fake has been replaced by the real service where its I story has landed.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P2-011 | Task text, booking missing | No booking for treatment {treatment} was found in the ALS load for {date}. Book it in ALS. Accounts not booked: {accounts}. |
| MSG-P2-012 | Task text and treatment note, term differs | The booked {term} is {booked}. The approved {term} is {approved}. |
| MSG-P1-001 | ACE batch late or not complete | {product} is from {date}. Today's load has not arrived. |
| MSG-P7-003 | Decision log write failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P3-027 | No BOOKING_MATCH version is in force | The {table} load was refused: {check}. The version in force is unchanged. |
| MSG-P2-006 | Rerun while JOB-08 runs | {job} is already running. Wait for it to finish before you run it again. |
| MSG-P4-002 | A role without the right reruns JOB-08 | You cannot {action} here. Your role does not include it. |

For MSG-P3-027 in this journey {check} is "no package in force" and {table} names the package code "BOOKING_MATCH" only, never a case or an account fact; the business date is not part of this message. The harness asserts the message ID and the substituted values; it does not own the message text. Where the text above differs from the Error and Message Standard v4 for MSG-P2-006, MSG-P2-011 or MSG-P3-027, the standard's wording governs.

### 15. Screens and states

| Screen | State | What the harness asserts |
|---|---|---|
| SCR-14 Treatment record | Approved | The treatment state, the approval date and the approved terms the match reads |
| SCR-14 Treatment record | Booked | Booked at 2026-12-16, or the booking difference with each term approved and booked |
| SCR-14 Treatment record | Empty | Not specified in the source documents (CG-ALL-594) |
| SCR-14 Treatment record | Loading | Not specified in the source documents (CG-ALL-594) |
| SCR-14 Treatment record | Error | Not specified in the source documents (CG-ALL-594) |
| SCR-14 Treatment record | No access | Not specified in the source documents (CG-ALL-594) |
| SCR-01 My work | Task list | One open task WITH_OPS_BOOKING for RW-RESTRUCT with MSG-P2-011 naming the accounts not booked; one UNMATCHED_EXCEPTION task for RW-CREDITAD with MSG-P2-012; no second task on the rerun or the second batch |
| SCR-01 My work | Empty | Not specified in the source documents (CG-ALL-593) |
| SCR-01 My work | Loading | Not specified in the source documents (CG-ALL-593) |
| SCR-01 My work | Error | Not specified in the source documents (CG-ALL-593) |
| SCR-01 My work | No access | Not specified in the source documents (CG-ALL-593) |
| SCR-29 Posting | Out of scope | The posting screen comes in Epic 4; the harness asserts no posting behaviour of this journey |
| SCR-29 Posting | Empty | Not specified in the source documents (CG-ALL-595) |
| SCR-29 Posting | Loading | Not specified in the source documents (CG-ALL-595) |
| SCR-29 Posting | Error | Not specified in the source documents (CG-ALL-595) |
| SCR-29 Posting | No access | Not specified in the source documents (CG-ALL-595) |

The harness opens no screen and renders no page; it asserts the answers of the operations those screens consume. Screen-level behaviour remains with the owning APP stories. Legacy section 15 names SCR-29 Posting as Epic 4 and the harness keeps that boundary.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-007-01-ITG | AC1, BR1, BR3, BR7, BR10 | Integration | Synthetic settlement booked 2026-12-16 at 650,000.00 baht |
| TC-E2-007-02-ITG | AC2, BR5 (run by Not specified in the source documents (CG-ALL-590)) | Integration | Restructure with tdr_flag false, read through the rwb-source-data contract |
| TC-E2-007-03-ITG | AC3, BR2, BR4, BR6 (run by Not specified in the source documents (CG-ALL-590)) | Integration | Rate 4.5000 booked against 4.2500 approved |
| TC-E2-007-04-ITG | AC4, BR2 (run by Not specified in the source documents (CG-ALL-590)) | Integration | Two accounts, one booked |
| TC-E2-007-05-ITG | AC5, BR8 | Integration | ACE batch failed for 2026-12-17 |
| TC-E2-007-06-ITG | AC6 (run by Not specified in the source documents (CG-ALL-590)) | Integration | JOB-08 rerun for 2026-12-16 |
| TC-E2-007-07-ITG | AC7, BR5 | Integration | Booking missing on two batches |
| TC-E2-007-08-ITG | AC8, BR9 (run by Not specified in the source documents (CG-ALL-590)) | Integration | Decision log store stopped |
| TC-E2-007-09-ITG | AC9, BR11 (run by Not specified in the source documents (CG-ALL-590)) | Integration | No BOOKING_MATCH version in force on 2026-12-17 |
| TC-E2-007-10-ITG | Access | Component | RW-CASEOWN calls POST /admin/jobs/{jobId}/rerun for JOB-08; refused with MSG-P4-002 |
| TC-E2-007-11-ITG | Principle 5 | NFR | Decision log write forced to fail on markBooked; treatment stays APPROVED, no event |
| TC-E2-007-12-ITG | AC10 | Integration | Consumed event delivered a second time |
| TC-E2-007-13-ITG | AC11 | Integration | Rwb-source-data contract call fails or gets no answer for 2026-12-16 |
| TC-E2-007-14-ITG | AC12 | Integration | Status change the state model does not allow, from APPROVED |

The full legacy test, with its Given, When and Then, is in the legacy test case workbook, tab Story test cases, under the legacy test case ID. The Covers column names the legacy AC of RWB-E2-007 that the ITG copy is derived from; the Level column maps the legacy System level to Integration, the legacy Access level to Component and the legacy Resilience level to NFR.

### 17. Guardrails

- No business value in code: the compared terms, the tolerance and the grace are rows of package BOOKING_MATCH or parameters of rwb-case; the harness reads them and never holds a copy.
- No personal data in logs, events, workflow inputs, evidence or prompts: the booking reference holds the account_key, not the account number, and the fixture is synthetic.
- No read of another service's schema and no direct ACE read: the account and batch data go through rwb-source-data's contract or the owning service's own views (DP-05), and the harness fails the run on any cross-schema reference found in the trace.
- No call to ALS: the harness reads only what ACE holds for the completed batch, and it never calls an outside system or a production endpoint.
- No comparison code and no rule table: package BOOKING_MATCH decides, through the evaluator of the owning service; the harness reads the fired row and the package version through the rwb-decision contract and reads no workbook and no drl_source.
- The decision record comes first: a booking that cannot be recorded does not proceed, and the harness fails the run when a treatment change appears without its record.
- One hop only: the harness fails a run when the trace shows a call chain deeper than the gateway and one owner.
- Each fake is replaced by the real service as its I story lands; a fake that outlives its service is a defect, not a configuration.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CHO-008 | Booking confirmed from the next day's ALS batch | Business Requirements Epic 2, section 3.2; Program, section 5.3 | FEAT-CHO-08 | 7.3 Negotiate settlement or deed in lieu | R-RES-22, R-SET-13, R-UNI-39 | TC-E2-007-01-ITG to TC-E2-007-14-ITG |

The rule ID and the package version on the decision record carry REQ-CHO-008 at the integration level; this story adds no requirement ID of its own.

### 19. Out of scope

- The nine owning app stories RWB-P3-E2004-APP, RWB-P1-E1069-APP, RWB-P3-E2042-APP, RWB-P2-E2007-APP, RWB-P3-E2007-APP, RWB-P4-E2007-APP, RWB-S2-E2007-APP, RWB-P1-E2007-APP and RWB-P7-E2007-APP, and every screen, endpoint, table, migration, rule and workflow they build.
- Production code, production data and any deployed artefact of any service: the harness is test and evidence only.
- The contract baselines of the six services, which their CON stories own.
- Platform deployment, the gateway-bff composite route implementation (RWB-PLT-N001-CON) and the platform configuration of Kafka, Temporal and the observability stack.
- The CON and OPS stories of RWB-E2-007, including the integration job catalogue provisioning and the environment operations.
- ALS itself and the ACE ingestion: the harness reads the results of the completed batch only.
- Posting a settlement booking to ALS from the Workbench (FEAT-PAY-06, Epic 4) and the SCR-29 Posting screen.
- Payment matching to the plan or the settlement (JOB-07, FEAT-OCC-10, Epic 2).
- Authoring, approval and rollback of package BOOKING_MATCH (RWB-E2-042 and RWB-E1-073).
- The other legacy journeys of the wave 2 harness set: RWB-E2-006, RWB-E2-008, RWB-E2-009 and RWB-E2-010.
