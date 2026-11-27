# RWB-ITG-E3010-ITG Book the plan and set the schedule

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-E3010-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W2 |
| Wave | 2 |
| Business epic | EP03 |
| Release | 31 January 2027 (tentative) |
| Legacy key | RWB-E3-010 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | L-ITG-W2 |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S2-E3010-APP (not done; WireMock fakes in §12.8 until it is live) |
| Contract dependencies | RWB-S2-E3010-CON |
| Integration dependencies | RWB-S2-E3010-APP |
| External dependencies | None |
| Size | Not specified in the source documents (DOR-RWB-ITG-E3010-ITG-16); squad sizes at refinement |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E3-010 for the wave 2 integration harness. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-ITG-E3010-ITG). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (23 resolved, 9 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **QA and integration harness**, I want **one repeatable cross-service proof that booking an approved plan sends the agreed terms to NLEADS and ALS, reads the booking facts from the ACE views, sets the payment schedule, starts the plan timers and writes the decision record with the rule version, against the owning services' published contracts and their fakes**, so that **a plan that has been agreed reaches the two core systems once, the schedule and the clocks come from what ACE holds rather than from a re-keyed copy, and the booking is on the record with the rule and the version that made it before the case is allowed to run**.

The treatment is owned by rwb-treatment, the outbound item by rwb-integration, the booking facts by ACE and read through rwb-source-data, the case state and the plan timers by rwb-case, and the record by rwb-decision. The harness provides no operation, table, workflow, schedule or screen. It proves the behaviour the owning services publish, and RWB-S2-E3010-APP owns the real behaviour and builds it.

### 2. Business rationale

A restructure reaches booking in days only if three things hold at once: the plan leaves to NLEADS and ALS once and is acknowledged, the payment schedule and the plan timers come from the facts ACE holds rather than from a copy the Workbench re-keyed, and the decision record names the rule and the version that booked it. The monolith did all three in the P3 module against one recovery schema, in one transaction, where a schedule nobody set and a record nobody wrote could not hide behind a case that had moved. In v5 the same loop crosses five owners and three call types. rwb-treatment holds the approved treatment and raises the booking, rwb-integration owns the outbound item and its delivery to NLEADS and ALS, rwb-source-data owns the contract over `v_ace_account`, `v_ace_payment` and `v_ace_plan`, rwb-case moves the case state and shows the timers, and rwb-decision holds the record. A defect at any hop now looks exactly like a successful booking, until the customer's first installment falls due against a schedule nothing set.

This story owns the harness that proves the loop as the legacy key describes it. It carries AC1 of RWB-E3-010 into evidence: the approved treatment `T-0001` for account `A-0001`, the plan at plan status APPROVED in `v_ace_plan`, the booking instruction for the agreed terms through the Temporal Nexus operation into the ACE Common namespace ace-collection, the booking facts read from the three ACE views, the payment schedule and the plan timers, and the result on the decision log with the rule version. The same loop is asserted on its two later facts, which the owning services drive and the harness observes: the R-RES-22 confirmation when ALS and NLEADS both acknowledge, which records the booking reference from the TreatmentBooked event on rwb.payment.events.v1, sets the payment schedule and moves the case to BOOKED_IN_ALS_NLEADS, and the R-RES-25 move when the schedule is set, which starts the plan timers, moves the plan to running and puts the case at PLAN_RUNNING. It serves REQ-S2-008, REQ-CHO-007 and REQ-CHO-008, and it carries FEAT-TRT-10 and its FEAT-CHO-07 and FEAT-CHO-08 dependencies into evidence.

The harness is decoupled the same way the services are. It never reads another service's table (DP-01): the treatment comes from rwb-treatment, the outbound item and its delivery from rwb-integration, the case state and the timers from rwb-case, the record from rwb-decision, and the account, payment and plan rows from rwb-source-data, which owns the ACE view contract (DP-05). It calls each owner's base `/api/recovery/<short>/v1` and never a monolith base (DP-13), and it calls through the gateway-bff composite route where a screen would (DP-19). Every call is one hop with a 2 s budget. The record is read from rwb-decision and its shared topic rather than from a log table of the harness's own (DP-03).

### 3. Preconditions

- The published contracts of rwb-treatment, rwb-integration, rwb-source-data, rwb-case, rwb-decision and rwb-access are in the contract registry, and a WireMock stub set is generated from each one and its version pinned.
- Contract version: the harness builds against the rwb-treatment booking and schedule contract at major version 1 (v1) and pins that version; a breaking change is major version 2. The contract versions of rwb-integration, rwb-source-data, rwb-case, rwb-decision and rwb-access for this story are not specified in the source documents (DOR-RWB-ITG-E3010-ITG-23).
- The case holds the approved treatment `T-0001` for account `A-0001`, and `v_ace_plan` holds the plan at plan status APPROVED, as the legacy key states them.
- The rule package in force carries R-RES-22 and R-RES-25, and the version of each is readable on the decision record that cites it.
- The NLEADS interface config and the ALS interface config exist in rwb-integration as outbound items. The interface codes, the transports, the message or file layouts and the test endpoints are not specified in the source documents (GAP-0424; ASM-0600).
- An authorisation path exists through `POST /api/recovery/access/v1/authorise` for the role that holds the booking right and for a caller outside it.
- A journey case, its treatment and its plan are seeded through the owning services' published operations only. The seeding set, the harness environment specification and the evidence format are not specified in the source documents (GAP-0424; ASM-0599).
- No build dependency and no contract dependency. Day 1, with the fakes in place from the first run, and the rwb-treatment fake replaced by the real service when RWB-S2-E3010-APP lands.

### 4. Flow

1. Harness: seeds the case, its approved treatment `T-0001` for account `A-0001` and its plan through the owning services' published operations only, and reads the plan back at plan status APPROVED. The seeding set and its environment are not specified in the source documents (GAP-0424; ASM-0599).
2. Harness: reads the treatment through `GET /api/recovery/treatment/v1/treatments/{treatmentId}` and asserts it is approved, that it is `T-0001`, and that it belongs to `A-0001`.
3. Harness: reads the plan status through `GET /api/recovery/integration/v1/cases/{caseId}/plan-status` and asserts APPROVED before the booking, proving the booking fact is ACE's and not the harness's.
4. Harness: asserts the outbound item for NLEADS and the outbound item for ALS through `GET /api/recovery/integration/v1/admin/outbound-items`, each naming the case and the treatment, and their delivery through `GET /api/recovery/integration/v1/admin/outbox/deliveries`. The interface detail and the fixtures behind them are not specified in the source documents (GAP-0424; ASM-0600).
5. Harness: asserts the delivery and, where the configured interface is a file, `rwb.integration.FileDelivered.v1` for the delivery and `rwb.integration.FileFailed.v1` for a failure the run must not pass over.
6. Harness: asserts the booking facts through `GET /api/recovery/source-data/v1/data-products/{productCode}/records`: the account row from `v_ace_account`, the payment row from `v_ace_payment`, the plan row from `v_ace_plan` and the plan status through the rwb-integration plan-status read again, as the owner drove it and never as a value the harness wrote (DP-05). The data product code that carries each row is not named for this story in the source documents (GAP-0424; ASM-0599).
7. Harness: asserts the payment schedule and the plan timers through `GET /api/recovery/case/v1/cases/{caseId}/timers`, reading the timer rows the owner created for the plan and not a schedule of its own.
8. Harness: asserts the case at BOOKED_IN_ALS_NLEADS and then at PLAN_RUNNING through `GET /api/recovery/case/v1/cases/{caseId}`, and `rwb.case.CaseStateChanged.v1` for each move on `rwb.case.events.v1`.
9. Harness: asserts exactly one decision record for each move through `GET /api/recovery/decision/v1/decision-log`, naming R-RES-22 and R-RES-25 with their versions, and `rwb.decision.DecisionRecorded.v1` on `rwb.decision-record.v1` for each.
10. Harness: subscribes to `rwb.treatment.events.v1` and `rwb.payment.events.v1` and asserts `rwb.treatment.TreatmentApproved.v1` as the earlier fact and `rwb.payment.TreatmentBooked.v1` as the booking ACE took, once for the path, with no personal data on either.
11. Harness: asserts that every outbound item was logged, retried on its configured schedule where it did not deliver first time, and placed in the exception queue after the retry limit, as REQ-DRI-007 states it.
12. Harness: authorises each call through `POST /api/recovery/access/v1/authorise` and records the refusal path for a caller that does not hold the booking right.
13. Harness: asserts that each call sat on the owner's base as a single hop with a 2 s budget and a breaker per downstream, and that no call was retried into a second state change.
14. Harness: publishes one evidence report per business date, keyed by story and business date, with the criterion and its assertions, and gates the wave on the result. The evidence format and its retention are not specified in the source documents (GAP-0424; ASM-0599).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A fake answers a shape the published contract does not allow | The run fails at that hop; the report names the service, the operation and the contract version | None | AC1 |
| X2 | No outbound item is created for NLEADS, or none for ALS, on the case and the treatment | The run fails on AC1 and the report names the interface config, the case and the treatment | None | AC1 |
| X3 | The outbound item stays undelivered, or `rwb.integration.FileFailed.v1` arrives | The run fails and the report names the outbound item and the failure the owner recorded | None | AC1 |
| X4 | The booking facts are not reflected from `v_ace_account`, `v_ace_payment` and `v_ace_plan` inside the run window | The run fails and the report names the view, the account and the business date | None | AC1 |
| X5 | The case does not reach BOOKED_IN_ALS_NLEADS, or does not reach PLAN_RUNNING after it | The run fails on AC1 and the report names the two states it saw | None | AC1 |
| X6 | Zero decision records or two exist for a move, or the record carries no rule version | The run fails on AC1 and the report names the records it found | None | AC1 |
| X7 | The record cannot be written for a move | Nothing changes: the case state, the schedule, the plan timers and the outbound item stay as they were, and the owning service returns MSG-P7-003 | MSG-P7-003 | AC1; BR8 |
| X8 | A caller without the booking right attempts the booking | The call is refused with MSG-P4-002 and the refusal is recorded | MSG-P4-002 | AC1 |
| X9 | A real service is reachable but its contract version differs from the registry | The run fails before any assertion and the report names the service and both versions | None | AC1 |
| X10 | The schedule is set but a plan timer the treatment carries is missing | The run fails on the R-RES-25 fact and the report names the timer type and the treatment | None | AC1; BR3 |

The report text is for the wave entry check and is not part of the message standard. The rule set carries no message ID for R-RES-22 or R-RES-25, so the harness asserts state, data and the decision record and not a message; the business messages this journey can produce are in section 14 and belong to the owning services.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Runs against published contracts and fakes from Day 1; the only wait is one I story, RWB-S2-E3010-APP |
| Negotiable | The NLEADS and ALS interface fixtures, the seeding set and the report shape are configuration and agreed at the wave entry check, not business values in code |
| Valuable | The booking of an approved plan, its schedule, its clocks and its record are proven end to end before the wave opens |
| Estimable | One harness runner, one stub set, two interface fixtures, one event probe, one report |
| Small | Fits in one sprint with its tests |
| Testable | The criterion runs against its fakes and again against the real owner as RWB-S2-E3010-APP lands |

### 7. Acceptance criteria

```gherkin
Feature: Book the plan and set the schedule

  Scenario: AC1 Book the plan and set the schedule (legacy RWB-E3-010 AC1)
    Given the case holds an approved treatment "T-0001" for account "A-0001" and the rwb-source-data contract fake serves the plan at plan status APPROVED
    When the Workbench books the plan
    Then it sends the booking instruction through the Temporal Nexus operation into the ACE Common namespace ace-collection (operation name Not specified in the source documents (GAP-2667)), and NLEADS and ALS act on it through operations
    Then it reads the booking facts through the rwb-source-data contract fake from v_ace_account, v_ace_payment and v_ace_plan, sets the payment schedule and starts the plan timers
    Then the system writes the result to the decision log with the rule version

  Scenario: AC5 Every outbound item is logged, retried and queued for a named owner after the retry limit (new, D-RCV-60)
    Given an outbound booking instruction has been sent
    When the instruction is not acknowledged by ALS or NLEADS
    Then the item is logged and retried on the defined schedule, and after the retry limit it is placed in the exception queue with a task for a named owner
    Then every read behind it goes through an owner's contract and no account or payment copy is held

  Scenario: AC6 A redelivered TreatmentBooked event does not book the plan twice (new, D-RCV-60)
    Given the TreatmentBooked event has been consumed once
    When the same TreatmentBooked event is delivered again
    Then the plan is not booked twice and no second schedule or decision record is written

  Scenario: AC7 A consumed call that fails or does not answer is handled, not silently dropped (new, D-RCV-60)
    Given a consumed call to a dependency has been made
    When the call fails or no answer is returned
    Then the failure is handled as the owning contract specifies and no booking result is written for it

  Scenario: AC8 A status change the model does not allow is refused (new, D-RCV-60)
    Given the case holds a status from which the requested status change is not allowed by the model
    When a status change to the requested status is made
    Then the change is refused and the case status is not changed
```

AC2, AC3 and AC4 are owned by the app story of this legacy key, RWB-S2-E3010-APP, and are not restated here. AC1 is the cross-service criterion this ITG copy owns: the harness asserts it through the owners' contracts, and it asserts the R-RES-22 and R-RES-25 facts of the same loop as observed facts in section 4 and section 16 rather than as new criteria.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The agreed terms of an approved plan leave the Workbench as one booking instruction keyed by the case and the treatment, sent through the one outbound path, a Temporal Nexus operation into the ACE Common namespace ace-collection (operation name Not specified in the source documents (GAP-2667)); the booking act stays with operations in ALS and NLEADS | Legacy RWB-E3-010 AC1; FEAT-TRT-10; R-RES-21 |
| BR2 | At booking confirmed, the Workbench consumes the TreatmentBooked event (EV-11) on rwb.payment.events.v1 through its inbox, records the booking reference and the booking date read from `v_ace_plan`, and writes the schedule columns on rwb-treatment from the schedule basis in `v_ace_payment`; the booking is one PlanBooking body with nleadsRef, alsBookingRef, bookedAt, firstDueDate, installmentCount, installmentAmount and installmentsPaid required and bookingDifference optional, and alsBookingRef is carried on the booking record and the decision record; rwb-payment owns the booking | R-RES-22 |
| BR3 | At BOOKED_IN_ALS_NLEADS with the schedule set, the plan timers start, the plan moves to running and the case reaches PLAN_RUNNING | R-RES-25 |
| BR4 | The booking facts are read from `v_ace_account`, `v_ace_payment` and `v_ace_plan` and are never re-keyed into a Workbench copy | REQ-CHO-008; legacy RWB-E3-010; D-RCV-35 U1 and U4 |
| BR5 | The plan timers run as durable timers inside TreatmentWorkflow on rwb-treatment through the workflow kit, with no Quartz table or job, and a breach is reported on the rwb-case timer path; a missed payment raises a PaymentMissed event from rwb-payment on rwb.payment.events.v1 rather than moving the case | REQ-CHO-007 |
| BR6 | Every outbound item is logged, retried on a defined schedule and placed in an exception queue with a task for a named owner after the retry limit | REQ-DRI-007 |
| BR7 | The decision record carries the rule and its version, and the package and its version from RESTRUCTURE, PAYMENT_MATCH or BOOKING_MATCH that applied it (package code not specified in the source documents (GAP-1707)), and it is written with the state change in one transaction | REQ-DRI-001 |
| BR8 | No move proceeds if its decision record cannot be written | REQ-DRI-005 |
| BR9 | The Workbench holds no account or payment copy; the account, payment and plan rows stay ACE's and are read through the owner's contract | REQ-RDF-001; legacy RWB-E3-010; D-RCV-35 U1 and U4 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| WITH_OPS_BOOKING | BOOKING_CONFIRMED | ALS and NLEADS both acknowledge | BOOKED_IN_ALS_NLEADS (R-RES-22) |
| BOOKED_IN_ALS_NLEADS | SCHEDULE_SET | first_due_date set | PLAN_RUNNING (R-RES-25) |

The treatment and the case are the owners' state: rwb-treatment holds the treatment and its plan timers, and P3 moves the case status on the facts the loop raises. The treatment approval is published as `rwb.treatment.TreatmentApproved.v1`, the booking ACE took as `rwb.payment.TreatmentBooked.v1`, and the case move is read back through the rwb-case contract.

The harness changes no state itself. It seeds through the owning services' published operations, reads the plan status the owner holds, and then asserts the states the owners reached: WITH_OPS_BOOKING to BOOKED_IN_ALS_NLEADS, and BOOKED_IN_ALS_NLEADS to PLAN_RUNNING. The harness sets nothing by hand: a state it set would prove nothing, so the report names the owner and the operation that made each move.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-RESTRUCT and the roles with Treatment and offer R | Read the treatment, the case state, the schedule, the timers and the decision record through the owners' contracts |
| The roles the legacy names for the booking right (Operations (booking), per R-RES-21) | Place the booking fact and read it back; the harness calls under the same right and fails where it is refused |
| QA lead | Owns the harness configuration, the NLEADS and ALS fixtures, the report shape and the pass or fail gate |
| Integration lead | Owns the harness code, the stub set and the swap from a fake to the real service |
| The owning services' identities | rwb-treatment, rwb-integration, rwb-source-data, rwb-case, rwb-decision, rwb-access and rwb-payment make every state change the harness asserts |
| No approval level from the delegation of authority applies | The harness takes no business decision; the treatment approval and any booking approval belong to the treatment story |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 to DF-CAS-023 | recovery_case | status (WITH_OPS_BOOKING, BOOKED_IN_ALS_NLEADS, PLAN_RUNNING) | Read, through the rwb-case contract |
| DF-WRK-027 to DF-WRK-036 | timer | id, case_id, task_id, timer_type, started_at, expires_at and 4 more | Read, through the rwb-case timers contract |
| DF-ACE-001 to DF-ACE-042 | v_ace_account | account_key, account_code, account_status, contract_no, product_category_efs, total_balance and 36 more | Read, through the rwb-source-data products contract |
| DF-ACE-043 to DF-ACE-054 | v_ace_payment | payment_code, account_key, payment_date, payment_amount, payment_channel, capital_amount and 6 more | Read, through the rwb-source-data products contract |
| DF-ACE-160 to DF-ACE-177 | v_ace_plan | plan_ref, account_key, plan_status, booked_at, approved_at, closed_at and 12 more | Read, through the rwb-source-data products contract |
| DF-TRT-001 to DF-TRT-014 | treatment | id, case_id, decision_log_id, treatment_type, plan installment counters, state | Read and write, through the rwb-treatment contract |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | decision_code, rule_id, rule_version, model_version | Read, through the rwb-decision contract |

Field IDs are those in the Logical Data Model and Data Dictionary, taken from the legacy key. The harness owns no table and writes no row directly: it reads and writes through the API of the owning service only (DP-01, DP-05), and the Workbench holds no account or payment copy, because the account, payment and plan rows are ACE's (legacy RWB-E3-010; D-RCV-35 U1 and U4). In the run, those rows are read only through the rwb-source-data contract fake (§12.8). Any list or parameter the harness asserts, including the NLEADS and ALS result codes, is not named in the parameter catalogue or the reference-data contract (DP-06, DP-07); these are not specified in the source documents (DOR-RWB-ITG-E3010-ITG-20; GAP-0424; ASM-0600).

### 12. Contract

#### 12.1 REST operations provided

None. The harness is a test runner and provides no REST operation.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| POST | `/api/recovery/treatment/v1/cases/{caseId}/treatments` | S2 rwb-treatment | Seed the treatment, only where the run must (AC1) |
| GET | `/api/recovery/treatment/v1/treatments/{treatmentId}` | S2 rwb-treatment | Read the approved treatment `T-0001` and its plan counters (AC1) |
| GET | `/api/recovery/integration/v1/admin/outbound-items` | P2 rwb-integration | The outbound item for NLEADS and the outbound item for ALS, each naming the case and the treatment (AC1) |
| GET | `/api/recovery/integration/v1/admin/outbox/deliveries` | P2 rwb-integration | The delivery of each outbound item (AC1) |
| GET | `/api/recovery/integration/v1/cases/{caseId}/plan-status` | P2 rwb-integration | The plan status at APPROVED before booking and at running after it (AC1) |
| GET | `/api/recovery/source-data/v1/data-products/{productCode}/records` | P1 rwb-source-data | The booking facts from `v_ace_account`, `v_ace_payment` and `v_ace_plan` (AC1) |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The case at BOOKED_IN_ALS_NLEADS and at PLAN_RUNNING (AC1) |
| GET | `/api/recovery/case/v1/cases/{caseId}/timers` | P3 rwb-case | The payment schedule and the plan timers the owner created (AC1) |
| GET | `/api/recovery/decision/v1/decision-log` | P7 rwb-decision | One record for each move, naming R-RES-22 or R-RES-25 and its version (AC1) |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | Role, scope and authority check for each call, including the refusal path (AC1) |

The data product code that carries the account, payment and plan rows is not named for this story in the source documents (GAP-0424; ASM-0599). Every operation is one hop on the owner's base `/api/recovery/<short>/v1` with a 2 s budget and a circuit breaker per downstream (DP-13); where a screen would compose them, the harness calls the gateway-bff composite route (DP-19). No operation is invented in this story.

#### 12.3 Events published

None. The harness publishes no Kafka event; it seeds through the owning services' contracts and consumes the owners' events.

#### 12.4 Events consumed

| Event | Topic | Producer | Use |
|---|---|---|---|
| `rwb.treatment.TreatmentApproved.v1` | `rwb.treatment.events.v1` | S2 rwb-treatment | The plan treatment was approved before the run (AC1) |
| `rwb.payment.TreatmentBooked.v1` | `rwb.payment.events.v1` | P8 rwb-payment | The booking ACE took, read back before the schedule is set (AC1) |
| `rwb.case.CaseStateChanged.v1` | `rwb.case.events.v1` | P3 rwb-case | The case reached BOOKED_IN_ALS_NLEADS and then PLAN_RUNNING (AC1) |
| `rwb.decision.DecisionRecorded.v1` | `rwb.decision-record.v1` | every service, through the local decision-record library | Each record written with the state change (AC1) |
| `rwb.integration.FileDelivered.v1` | `rwb.integration.events.v1` | P2 rwb-integration | The plan delivered, where the configured NLEADS or ALS interface is a file (AC1) |
| `rwb.integration.FileFailed.v1` | `rwb.integration.events.v1` | P2 rwb-integration | The plan failed, where the configured interface is a file (AC1) |

All six carry IDs and business facts only, keyed by caseId and treatmentId, and the harness asserts that no personal data is present (DP-03, DP-09).

#### 12.5 Workflows and activities

None added. The harness exercises the existing TreatmentWorkflow in rwb-treatment, which holds the treatment and its plan timers across the booking, and the CaseWorkflow in rwb-case, which routes the stage facts and moves the case status, and asserts their effects through the services' contracts and the owners' topics. No workflow, activity or Schedule is created, changed or owned by this story.

#### 12.6 Schedules

None added. The plan timers are the treatment's and rwb-case's, set from the treatment record as R-RES-25 states it; this story sets no cron, overlap policy, catch-up window or Schedule of its own.

#### 12.7 Tables owned

None. The harness owns no schema and no table (DP-01): the treatment and its plan timers are rwb-treatment's, the interface config and outbound items are rwb-integration's, the case and its timer rows are rwb-case's, and the account, payment and plan rows are ACE's, read through rwb-source-data's contract (DP-05).

#### 12.8 Contract fakes

| Fake | Contract | Use in the run |
|---|---|---|
| WireMock stub for rwb-treatment | `POST /cases/{caseId}/treatments`, `GET /treatments/{treatmentId}`, `rwb.treatment.events.v1` | Day-1 runs of AC1 and of the R-RES-22 and R-RES-25 paths before RWB-S2-E3010-APP is live |
| WireMock stub for rwb-integration | `GET /admin/outbound-items`, `GET /admin/outbox/deliveries`, `GET /cases/{caseId}/plan-status`, `rwb.integration.events.v1` | Day-1 assertions on the NLEADS and ALS outbound items, their delivery and the plan status |
| WireMock stub for rwb-source-data | `GET /data-products/{productCode}/records` | Day-1 assertions on the account, payment and plan rows |
| WireMock stub for rwb-case | `GET /cases/{caseId}`, `GET /cases/{caseId}/timers`, `rwb.case.events.v1` | Day-1 assertions on BOOKED_IN_ALS_NLEADS, PLAN_RUNNING, the schedule and the plan timers |
| WireMock stub for rwb-decision | `GET /decision-log`, `rwb.decision-record.v1` | Day-1 assertion of one record per move with its rule version |
| WireMock stub for rwb-access | `POST /authorise` | Day-1 authorisation and refusal path |
| NLEADS outbound fixture | The outbound item on the configured NLEADS interface | The plan as it leaves and the acknowledgement, where the interface is a file |
| ALS outbound fixture | The outbound item on the configured ALS interface | The plan as it leaves and the acknowledgement, where the interface is a file |

Each stub is generated from the published contract and its version is pinned in the run report, so a contract change shows up as a run failure and not as a silent pass. The NLEADS and ALS interface codes and transports, the message or file layouts and result codes, the fixture contents, the data seeding set, the harness environment and the evidence format and retention are not specified in the source documents (GAP-0424; ASM-0600).

#### 12.9 Call-type summary

| Call type | In this story |
|---|---|
| REST | 0 provided, 10 consumed, one hop each on `/api/recovery/<short>/v1` with a 2 s budget (DP-13), composed through gateway-bff where a screen would (DP-19) |
| Kafka | None published; `rwb.treatment.TreatmentApproved.v1`, `rwb.payment.TreatmentBooked.v1`, `rwb.case.CaseStateChanged.v1`, `rwb.decision.DecisionRecorded.v1`, `rwb.integration.FileDelivered.v1` and `rwb.integration.FileFailed.v1` consumed (DP-03, DP-09) |
| Temporal | None added; the TreatmentWorkflow and the CaseWorkflow exercised |
| File | The NLEADS and ALS outbound interfaces as fixtures, where the configured interface is a file |

### 13. Solution plan

**Package.** Folder `itg/recovery`, package `th.co.scb.ace.workbench.recovery.itg`, test scope only; not part of any deployed service.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The platform H dependencies in the table above (RWB-PLT-E1027-CON and RWB-PLT-N001-CON) are delivered by the platform waves and are not repeated in the metadata H field of this story, which stays None. The blocking dependency is the one I story, RWB-S2-E3010-APP: until it is live the run uses the rwb-treatment stub, and a stub pass is reported as a stub pass.

The microservice move is the story's own reading of the legacy behaviour. The booking leaves through P2 rwb-integration's outbound interface instead of the monolith adapter (the DP-16 lineage, carried here in prose because this harness builds no adapter). The ACE facts are read through the P1 products contract and never from a local copy (DP-05). Every call is one hop on the per-service base (DP-13). The record goes through the local decision-record library (DP-03). The composed read a screen would make goes through the gateway-bff composite route (DP-19). Per-service schemas mean the Workbench holds no account or payment copy (DP-01): the account, payment and plan rows stay ACE's, and the harness sees them only as the owner returns them.

**Harness components**

| Component | Type | Responsibility |
|---|---|---|
| JourneyRunner | Job | Runs the owned criterion and its two later facts in order for a business date and holds the run lock |
| StubSet | Fake | The six WireMock stubs, each generated from the published contract with the version pinned |
| NleadsAlsFixture | Fixture | The outbound items on the configured NLEADS and ALS interfaces and their acknowledgements, keyed by case and treatment |
| EventProbe | Service | Consumes `rwb.treatment.events.v1`, `rwb.payment.events.v1`, `rwb.case.events.v1`, `rwb.integration.events.v1` and `rwb.decision-record.v1` and asserts the facts for the case |
| EvidenceReport | Service | Writes the per-run report keyed by story and business date, and holds the pass or fail gate |

**Environment and test data.** SIT, against the fakes from Day 1 and the real services as they land, on account `A-0001` with the approved treatment `T-0001` and a plan at plan status APPROVED in `v_ace_plan`. The environment, the seeding set, the NLEADS and ALS fixtures and the evidence retention are not specified in the source documents (GAP-0424; ASM-0599). Seeding uses only the owning services' published operations, never a schema write.

**Build steps**

1. Generate the six stubs from the published contracts, pin each contract version in the run report and fail the run on a version mismatch (X1, X9).
2. Build the NleadsAlsFixture and prove the one booking instruction through the Nexus operation from sending to acknowledgement by ALS and NLEADS for a business date (X2, X3).
3. Build the JourneyRunner for AC1: read the treatment, the plan status and the booking facts, assert the one booking instruction sent through the Nexus operation, the schedule and the plan timers, and one record naming R-RES-22 with its version (X4, X5, X6).
4. Add the EventProbe for `rwb.treatment.TreatmentApproved.v1`, `rwb.payment.TreatmentBooked.v1`, `rwb.case.CaseStateChanged.v1` and `rwb.decision.DecisionRecorded.v1` and assert the key and the absence of personal data.
5. Add the R-RES-25 fact: with the schedule set, the plan timers exist, the plan reads running and the case reaches PLAN_RUNNING, with one record naming R-RES-25 and its version (X5, X10).
6. Add the file events `rwb.integration.FileDelivered.v1` and `rwb.integration.FileFailed.v1` for each configured interface and assert that a failure fails the run (X3).
7. Add the record failure path: with the decision log write forced to fail, the case state, the schedule, the plan timers and the outbound item stay untouched and the owner returns MSG-P7-003 (X7).
8. Add the access path through `POST /api/recovery/access/v1/authorise`, including the refusal for a caller without the booking right (X8).
9. Add the EvidenceReport and the gate, then swap the rwb-treatment stub for the real service when RWB-S2-E3010-APP lands and rerun the criterion and its two later facts.

**Feature switch.** The legacy key names no feature switch for this behaviour. The journey runs behind the platform feature-flag library as the wave releases it; the flag key for this harness is not specified in the source documents (GAP-0424; ASM-0599).

**Done when.** The tests of section 16 pass for AC1 and for the two later facts of the loop; the criterion passes against the fakes on Day 1 and again against rwb-treatment when RWB-S2-E3010-APP lands; and the wave entry check holds a run report keyed by story and business date with the contract and fixture versions named.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P7-003 | The decision record for a move cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | The caller's role does not include the right, or the case is outside their scope | You cannot {action} here. Your role does not include it. |
| MSG-GEN-001 | A required value is missing from the request | Enter {field}. |

R-RES-22 and R-RES-25 carry no message ID in the rule set, so the harness asserts the state, the data and the decision record and names a message ID only where the owning service returns one of the three above. The harness produces none of these messages itself.

### 15. Screens and states

SCR-14 Treatment record (built in RWB-S2-E3010-APP) shows the states this journey sets:

| State | What the user sees and does |
|---|---|
| Draft | The plan treatment is being prepared; no booking fact exists |
| Submitted | The plan is with its approver; no booking fact exists |
| Approved | The plan treatment is approved and ready to leave to NLEADS and ALS |
| Booked | The plan has left, the schedule is set, the plan timers run and the case is at PLAN_RUNNING |
| Broken | A later missed payment takes the plan out of running and into the cure path, which is RWB-E3-011 |
| Empty | Not specified in the source documents (CG-ALL-826) |
| Loading | Not specified in the source documents (CG-ALL-826) |
| Error | Not specified in the source documents (CG-ALL-826) |
| No access | The refusal with MSG-P4-002, tested in TC-E3-010-05-ITG |

The case states BOOKED_IN_ALS_NLEADS and PLAN_RUNNING are read through the rwb-case contract and shown on the case record view, whose screen ID is not named for this feature in the source documents (GAP-0424; ASM-0599).

The harness renders no screen. It reads these states through the rwb-treatment, rwb-integration, rwb-source-data, rwb-case and rwb-decision contracts, so a passed run means the screens have the right data behind them. What the wave entry check looks at instead is the evidence report, whose format and retention are not specified in the source documents (GAP-0424; ASM-0599).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E3-010-01-ITG | Legacy AC1 of RWB-E3-010: book the plan and set the schedule — the booking instruction through the Nexus operation into ACE Common, the booking facts, the schedule, the plan timers and the record with its rule version (BR1, BR2, BR4, BR7) | Integration | Treatment `T-0001` approved for account `A-0001`; `v_ace_plan` at plan status APPROVED, served by the rwb-source-data contract fake; one booking instruction through the Nexus operation |
| TC-E3-010-02-ITG | Run by RWB-S2-E3010-APP: legacy AC2 of RWB-E3-010, asserted as the R-RES-22 fact of the same loop: booking confirmed, the booking date from `v_ace_plan`, the schedule from `v_ace_payment` and the case at BOOKED_IN_ALS_NLEADS (BR2) | Integration | WITH_OPS_BOOKING; ALS and NLEADS both acknowledging |
| TC-E3-010-03-ITG | Run by RWB-S2-E3010-APP: legacy AC3 of RWB-E3-010, asserted as the R-RES-25 fact of the same loop: the schedule set, the plan timers started, the plan running and the case at PLAN_RUNNING (BR3, BR5) | Integration | BOOKED_IN_ALS_NLEADS; first_due_date set |
| TC-E3-010-04-ITG | Run by RWB-S2-E3010-APP: legacy AC4 of RWB-E3-010: the decision log write forced to fail, nothing changes and MSG-P7-003 is returned (BR8) | Integration | Decision log stubbed unavailable; MSG-P7-003 |
| TC-E3-010-05-ITG | Access: a role without the booking right is refused with MSG-P4-002 | Component | A role without the right; refused with MSG-P4-002 |
| TC-E3-010-06-ITG | Principle 5: no business value in code, no personal data in events or logs, no read of another service's tables (BR9) | NFR | Events and reports scanned for personal data; every read through an owner's contract |
| TC-E3-010-07-ITG | AC5 (new, D-RCV-60): every outbound item is logged, retried on the defined schedule and placed in an exception queue with a task for a named owner after the retry limit (BR6); every read goes through an owner's contract (BR9) | Integration | Outbound item not acknowledged by ALS or NLEADS; retry schedule and limit not specified in the source documents (DOR-RWB-ITG-E3010-ITG-4) |
| TC-E3-010-08-ITG | AC6 (new, D-RCV-60): a redelivered TreatmentBooked event does not book the plan twice (BR2) | Integration | TreatmentBooked event delivered twice on rwb.payment.events.v1; the second delivery is a duplicate |
| TC-E3-010-09-ITG | AC7 (new, D-RCV-60): a consumed call that fails or does not answer is handled, not silently dropped | Integration | Not specified in the source documents (NEWAC-RWB-ITG-E3010-ITG-AC7) |
| TC-E3-010-10-ITG | AC8 (new, D-RCV-60): a status change the model does not allow is refused and the case status is unchanged | Component | Not specified in the source documents (NEWAC-RWB-ITG-E3010-ITG-AC8) |

TC-E3-010-01-ITG to TC-E3-010-06-ITG are the ITG copies of the legacy cases TC-E3-010-01 to TC-E3-010-06; among them, the integration cases cover AC1 and the two later facts of the same loop, and the component and NFR copies keep the legacy levels. TC-E3-010-01-ITG is the copy that covers AC1. TC-E3-010-07-ITG to TC-E3-010-10-ITG cover AC5 to AC8; TC-E3-010-07-ITG also covers BR6 and BR9. The full test, with its Given, When and Then, is in `Recovery Workbench Test Cases v8.xlsx`, tab Story test cases, under the legacy test case IDs TC-E3-010-01 to TC-E3-010-06.

SCR-14 states: this story owns no screen. No empty, loading or error state is specified in the source documents (DOR-RWB-ITG-E3010-ITG-10). The no-access state is the refusal with MSG-P4-002 in TC-E3-010-05-ITG.

### 17. Guardrails

- No business value in code: the rule versions, the NLEADS and ALS interface fixtures, the seeding set, the eligible states and the result code mappings are data.
- No personal data in logs, fixtures, reports, tests or prompts: the events carry IDs and business facts only, and the harness asserts the absence of personal data.
- No read of another service's tables: every read and every seed goes through the owning contract (DP-01), and the account, payment and plan rows are ACE's, read through rwb-source-data's products contract (DP-05).
- The Workbench holds no account or payment copy (legacy RWB-E3-010; D-RCV-35 U1 and U4), so the harness fails a run that finds a re-keyed row behind a state it asserts.
- One hop and a 2 s budget per call, with a circuit breaker per downstream, so the harness fails where a screen would.
- A stub pass is never reported as a real-service pass: the report names the contract version and whether the hop was a stub or the owner.
- The harness never runs against UAT or production, and it never sets a treatment, plan, case or decision state by hand.
- A failing assertion is fixed in the service that owns it or reported as a gap; it is never waived in the script.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-S2-008 | Booked terms, settled accounts and released collateral are posted to their systems of record without re-keying | Business Requirements Program v5, section 5.9 | FEAT-TRT-10 | D6, treatment and settlement | R-RES-22, R-RES-25 | TC-E3-010-01-ITG, TC-E3-010-02-ITG |
| REQ-CHO-007 | Plan timers run from the treatment record, and a missed payment raises an event | Business Requirements Program v5, section 5.3 | FEAT-TRT-10 | D6, treatment and settlement | R-RES-25 | TC-E3-010-03-ITG |
| REQ-CHO-008 | The plan and the booked terms are recorded on the case, and the booking is confirmed from the next business date's ACE account data in `v_ace_account` | Business Requirements Program v5, section 5.3 | FEAT-TRT-10; FEAT-CHO-07; FEAT-CHO-08 | D6, treatment and settlement | R-RES-22 | TC-E3-010-01-ITG, TC-E3-010-02-ITG |
| REQ-DRI-001 | Every decision writes one record holding the case, the decision, the rule and its version | Business Requirements Program v5, section 5.7 | FEAT-TRT-10 | D6, treatment and settlement | R-RES-22, R-RES-25 | TC-E3-010-01-ITG, TC-E3-010-03-ITG |
| REQ-DRI-007 | The integration adapters log every outbound file, retry on a defined schedule and place failures in an exception queue | Business Requirements Program v5, section 5.2 | FEAT-TRT-10 | D6, treatment and settlement | R-RES-21, R-RES-22 | TC-E3-010-01-ITG, TC-E3-010-03-ITG, TC-E3-010-07-ITG |

### 19. Out of scope

- AC2, AC3 and AC4 of the legacy key, and the whole rwb-treatment behaviour, which are owned by RWB-S2-E3010-APP.
- The rwb-treatment contract baseline, which is RWB-S2-E3010-CON.
- The rwb-integration interface build, the outbound item lifecycle and the retry and exception queue, and the NLEADS and ALS interface codes, transports and layouts, none of which a source read gives.
- The rwb-payment booking match (RWB-E2-007 and RWB-E2-008).
- The plan break detection and its cure path (RWB-E3-011).
- Any production screen, endpoint, event, workflow, schedule or table: this story builds a test harness and its evidence only.
