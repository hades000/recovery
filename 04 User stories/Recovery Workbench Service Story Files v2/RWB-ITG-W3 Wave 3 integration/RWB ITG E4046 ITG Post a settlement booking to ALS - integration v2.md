# RWB-ITG-E4046-ITG Post a settlement booking to ALS

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-E4046-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W3 |
| Wave | 3 |
| Business epic | EP04 |
| Release | 28 February 2027 (tentative) |
| Legacy key | RWB-E4-046 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP19 |
| Parallel lane | L-ITG-W3 |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-ITG-E4046-ITG-16) |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | RWB-P8-E4046-APP, RWB-P2-E4046-APP (not done yet; day-1 stubs in section 12.8) |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E4-046 for the wave 3 integration harness. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-ITG-E4046-ITG). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (17 resolved, 20 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a member of the integration and QA team, I want **one repeatable cross-service harness that takes an accepted settlement for an account, posts the booking through the outbound interface to ALS, reads the booked position and the settlement payment back from the ACE views, and proves that the decision record carrying the rule version was written with the change, against the owning services' published contracts and their fakes**, so that **the booking of a settlement is shown to leave the Workbench through rwb-integration and to be confirmed from ACE data before the case moves, and a settlement never sits accepted with no booking behind it**.

### 2. Business rationale

A settlement that is signed and accepted but never booked in ALS leaves the agreement unenforceable and the payment due date unset, so the customer's money arrives against a case that has nothing to receive it. The reverse failure is worse to defend: a booking that reaches ALS with no decision record behind it is a state the bank cannot evidence at audit. The booking is also the point of no return of the settlement (Temporal and Drools Design slide 18, "Point of no return / undo: ALS/NLEADS booking"), so the fact that it happened, and what it was based on, has to be provable.

The chain that produces that proof crosses six services and three call types. The accepted settlement terms are S2 rwb-treatment's, in `rwb_treatment`. The booking leaves as an outbound item of P2 rwb-integration, where the interface config, the outbound item and its delivery sit, and every outbound is logged, retried on a defined schedule and placed in an exception queue after the retry limit (REQ-DRI-007). The booked position and the settlement payment are ACE's, read back through P1 rwb-source-data's data product over `v_ace_account` and `v_ace_payment`, because the Workbench holds no account or payment copy (REQ-CHO-008; REQ-S2-008; D-RCV-35 U1 and U4). The case state after the booking is P3 rwb-case's. The record that cites the rule and its version is written with the change in one transaction and reaches the ledger through `rwb.decision-record.v1` (REQ-DRI-001; R-UNI-39). The posting operation itself is P8 rwb-payment's, which owns bookings and posting files.

This story owns the harness that proves that chain as the legacy key describes it, carrying AC1 of RWB-E4-046 into evidence, the legacy values included: treatment `T-0001` accepted at a settlement amount of 820000 for account `A-0001`. It serves REQ-S2-008, REQ-CHO-008, REQ-DRI-007 and REQ-DRI-001, and it carries FEAT-PAY-06 and its FEAT-CHO-08 dependency into evidence. It also holds the two restructure neighbours of the same booking step in view, R-RES-22 and R-RES-23, because the same outbound path carries the ALS acknowledgement or the ALS rejection, and the settlement path is where a rejection has to be visible on the officer queue rather than lost.

The harness is decoupled the same way the services are. It owns no schema and reads no other service's table (DP-01): the accepted terms come from rwb-treatment, the outbound item and its delivery from rwb-integration, the booked position and the payment from rwb-source-data's product, the case state from rwb-case and the record from rwb-decision. It reads the ACE rows through rwb-source-data's contract and never through a view of its own (DP-05). The record is read from rwb-decision's contract and the shared `rwb.decision-record.v1` topic rather than from a local log table (DP-03). It calls each owner's base `/api/recovery/<short>/v1`, one hop per call with a 2 s timeout and a circuit breaker per downstream, and it calls the gateway-bff composite route where a screen would (DP-19).

### 3. Preconditions

- The published contracts of rwb-treatment, rwb-integration, rwb-source-data, rwb-case, rwb-decision and rwb-access are in the contract registry, and a stub set is generated from each published OpenAPI or AsyncAPI document with its version pinned.
- The settlement treatment `T-0001` is accepted at a settlement amount of 820000 for account `A-0001`, as the legacy key states it, and the acceptance is read from rwb-treatment's contract and not from a copy of the harness's own.
- Account `A-0001` and its next ACE batch are seeded, so that the booked position can be read from `v_ace_account` and the settlement payment from `v_ace_payment` after the batch has been ingested.
- The seeding set, the harness environment specification and the fixture contents are not specified in the source documents (GAP-0432; ASM-0608).
- The ALS booking is modelled by the outbound item on the interface config in rwb-integration and, where the configured interface is a file, by an outbound fixture. The ALS interface ID, its transport, the message or file layout and the test endpoint are not specified in the source documents (GAP-0432; ASM-0608).
- The operation in rwb-payment that posts the booking, and the data product code that carries `v_ace_account` and `v_ace_payment` records, are not specified in the source documents (GAP-0432; ASM-0608).
- The rule package in force carries R-SET-10, R-SET-13, R-RES-22 and R-RES-23, and the version of the rule that each step records is readable on the decision record that cites it.
- An authorisation path exists through `POST /api/recovery/access/v1/authorise` for the case owner's role and for a caller whose role does not include the right.
- No build dependency and no contract dependency. Day 1, with the fakes of section 12.8 in place from the first run, and each fake replaced by the real service as RWB-P8-E4046-APP and RWB-P2-E4046-APP land.

### 4. Flow

1. Harness: seeds account `A-0001`, its next ACE batch and the accepted settlement treatment `T-0001` at 820000 through the owning services' published operations only; the seeding set and the environment are not specified in the source documents (GAP-0432; ASM-0608).
2. Harness: reads the accepted settlement terms through `GET /api/recovery/treatment/v1/treatments/{treatmentId}` and asserts the treatment state, the settlement amount 820000 and account `A-0001` as the legacy key states them.
3. Harness: posts the accepted treatment with `POST /api/recovery/treatment/v1/treatments/{treatmentId}/submit`, so the booking is raised by the service that owns the treatment and not by the harness. Where the environment runs the stage child, the same fact arrives as the settlement step of TreatmentWorkflow on queue rwb-treatment after `rwb.treatment.TreatmentApproved.v1`.
4. Harness: asserts the ALS booking as an outbound item on the ALS interface config through `GET /api/recovery/integration/v1/admin/outbound-items`, naming the case and the treatment, and asserts that exactly one item exists for the treatment and one Idempotency-Key, because every POST carries an Idempotency-Key and a repeat of the same command creates no second item (Architecture v5 slide 11). The interface ID and its transport are not specified in the source documents (GAP-0432; ASM-0608).
5. Harness: asserts the delivery of that item through `GET /api/recovery/integration/v1/admin/outbox/deliveries`, and asserts the attempt count, the logged attempt and the retry record the owner kept (REQ-DRI-007).
6. Harness: reads the booked position and the settlement payment through the rwb-source-data contract fake of section 12.8 (`GET /api/recovery/source-data/v1/data-products/{productCode}/records`), and asserts both after the next ACE batch has been ingested (DP-05). The product code is not specified in the source documents (GAP-0432; ASM-0608).
7. Harness: asserts the case state after the booking through `GET /api/recovery/case/v1/cases/{caseId}`, and that the state is the owner's and not the harness's.
8. Harness: reads `GET /api/recovery/decision/v1/decision-log` and asserts one record for the booking, carrying the rule ID and the rule version the owner recorded, and asserts `rwb.decision.DecisionRecorded.v1` on `rwb.decision-record.v1` for it within 5 minutes (DP-03).
9. Harness: subscribes to `rwb.treatment.events.v1` and asserts `rwb.treatment.TreatmentApproved.v1` for the treatment, the fact that precedes the booking, with no personal data on it.
10. Harness: subscribes to `rwb.integration.events.v1` and asserts `rwb.integration.FileDelivered.v1` where the configured ALS interface is a file, and `rwb.integration.FileFailed.v1` where the booking fails, which fails the run and is reported as the exception the officer queue would carry (REQ-DRI-007).
11. Harness: repeats the run with the decision record forced to fail and asserts that nothing moves: no outbound item, no booked position, no case state change, and the message the owner returns. This is the negative path of AC2, whose criterion belongs to RWB-P8-E4046-APP.
12. Harness: authorises each call through `POST /api/recovery/access/v1/authorise` and records the refusal path for a role that does not include the right.
13. Harness: publishes one evidence report per story and business date, naming the criterion, the assertions, the contract versions, the ACE batch used and whether each hop was a stub or the owner. The evidence format and its retention are not specified in the source documents (GAP-0432; ASM-0608).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A fake answers a shape the published contract does not allow | The run fails at that hop; the report names the service, the operation and the contract version | None | AC1 |
| X2 | The accepted terms read from rwb-treatment do not carry the settlement amount 820000 or account `A-0001` | The run fails and the report names the treatment and the values it found | None | AC1 |
| X3 | No outbound item is created for the treatment on the ALS interface config | The run fails on AC1 and the report names the interface config and the treatment | None | AC1 |
| X4 | More than one outbound item exists for one treatment and one Idempotency-Key, or the repeat of the same command raises a second booking | The run fails on AC1 and the report names the outbound items it found | None | AC1 |
| X5 | The outbound item stays undelivered, or `rwb.integration.FileFailed.v1` arrives | The run fails on AC1 and the report names the outbound item and the failure the owner recorded | MSG-P7-003 where the owner returns it | AC1 |
| X6 | The booked position is not readable from `v_ace_account` for `A-0001`, or the settlement payment is missing from `v_ace_payment` after the next ACE batch | The run fails on AC1 and the report names the account, the batch and the rows it read | None | AC1 |
| X7 | The case state after the booking is not the one the owner recorded, or more than one record exists for the booking, or its rule version is missing | The run fails on AC1 and the report names the states and the records it found | None | AC1 |
| X8 | The record does not reach `rwb.decision-record.v1` inside 5 minutes | The run fails on AC1 and the report names the record and its arrival time | None | AC1 |
| X9 | The decision record is forced to fail but the outbound item, the booked position or the case state still moves | The run fails on the negative path and the report names what moved | MSG-P7-003 | AC2 path, BR7 |
| X10 | A role that does not include the right is authorised, or a caller outside the case scope passes | The run fails on the access check and the report names the operation | MSG-P4-002 | AC3, TC-E4-046-03-ITG |
| X11 | A real service is reachable but its contract version differs from the registry | The run fails before any assertion and the report names the service and both versions | None | AC1 |

The report text is for the wave entry check and is not part of the message standard. R-SET-10, R-SET-13, R-RES-22 and R-RES-23 carry no message ID in the rule set, so the harness asserts the state, the data, the outbound item and the decision record, and names a message ID only where an owning service returns one of the three in section 14.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Runs against published contracts and fakes from Day 1; the only waits are the two I stories, RWB-P8-E4046-APP and RWB-P2-E4046-APP, and the already-published rwb-treatment contract of wave 2 |
| Negotiable | The ALS interface fixture, the data product code, the seeding set and the report shape are configuration agreed at the wave entry check, not business values in code |
| Valuable | The booking of a settlement to ALS, the read-back from ACE and the record behind it are proven end to end before wave 3 opens |
| Estimable | One harness runner, one stub set, one interface fixture, one event probe, one report |
| Small | Fits in one sprint with its tests |
| Testable | The criterion runs against its fakes and again against the real owners as RWB-P8-E4046-APP and RWB-P2-E4046-APP land |

### 7. Acceptance criteria

```gherkin
Feature: Post a settlement booking to ALS

  Background:
    Given treatment "T-0001" is accepted as a settlement for account "A-0001"
    And account "A-0001" and its next ACE batch are seeded
    And the contract fakes of section 12.8 are published with their versions pinned

  Scenario: AC1 Post a settlement booking to ALS (legacy RWB-E4-046 AC1)
    Given treatment "T-0001" is accepted at a settlement amount of 820000 for account "A-0001"
    When the case owner posts the booking
    Then the Workbench sends the agreed terms to ALS through the outbound interface and tracks the item in outbound_item
    Then the booked position and the settlement payment are read through the rwb-source-data contract fake of section 12.8
    Then the system writes the result to the decision log with the rule version

  Scenario: AC3 A role without the right, or a caller outside the case scope, is refused at the access check (new, D-RCV-60)
    Given a caller whose role does not include the right to post the booking, or who is outside the scope of the case
    When the caller posts the booking
    Then the access check refuses the call and the report names the operation
    And the message MSG-P4-002 is returned

  Scenario: AC4 ALS and NLEADS acknowledge the booking and its reference is recorded, or an ALS rejection keeps the case with operations (new, D-RCV-60)
    Given treatment "T-0001" has been posted as the booking for account "A-0001"
    When ALS and NLEADS return their result for the booking
    Then on acknowledgement the booking reference is recorded on the case
    And on an ALS rejection the error is placed on the officer queue and the case stays with operations

  Scenario: AC5 A consumed event delivered a second time does not raise a second booking (new, D-RCV-60)
    Given treatment "T-0001" is accepted as a settlement for account "A-0001"
    And its TreatmentApproved event has been consumed once
    When the same TreatmentApproved event is delivered again
    Then exactly one outbound item and one booking exist for the treatment
    And the report names the outbound items it found

  Scenario: AC6 A consumed call that fails or does not answer leaves no booking reference recorded (new, D-RCV-60)
    Given treatment "T-0001" is accepted as a settlement for account "A-0001"
    When a call the service consumes fails or does not answer
    Then no booking reference is recorded on the case
    And the report names the call and the service

  Scenario: AC7 A status change the model does not allow is refused and nothing moves (new, D-RCV-60)
    Given treatment "T-0001" is in a case state from which the booking is not allowed
    When the booking is posted
    Then the status change is refused
    And the decision record is not written and the report names the states
```

AC2 of the legacy key ("Not recorded") is owned by RWB-P8-E4046-APP and is not restated here; the harness exercises it only as the negative path of the same loop, in step 11 of section 4 and in TC-E4-046-02-ITG.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The signed settlement is routed to operations and the payment instruction is raised | R-SET-10 |
| BR2 | The agreed terms are booked in ALS and the payment due date is set | R-SET-13 |
| BR3 | ALS and NLEADS both acknowledge the booking, and the booking reference is recorded | R-RES-22 |
| BR4 | An ALS rejection puts the error on the officer queue and keeps the case with operations | R-RES-23 |
| BR5 | The Workbench writes nothing to ALS directly: the agreed terms leave through the outbound interface and the item is tracked in `outbound_item`, and every outbound is logged, retried on a defined schedule and placed in an exception queue after the retry limit | REQ-DRI-006; REQ-DRI-007 |
| BR6 | Once ACE has ingested the result, the booked position and the settlement payment are read through the rwb-source-data data product (DP-05), and the Workbench holds no account or payment copy | REQ-CHO-008; REQ-S2-008; D-RCV-35 U1 and U4; DP-05 |
| BR7 | The decision record carries the rule and its version and is written with the change in one transaction, and no action proceeds without it | REQ-DRI-001; REQ-DRI-005; R-UNI-39 |

The four rule rows behind the booking are the settlement pair and the restructure pair: R-SET-10 raises the instruction and routes the case to operations, R-SET-13 sets the due date once the terms are booked, R-RES-22 records the reference when ALS and NLEADS acknowledge, and R-RES-23 keeps the case with operations and puts the error on the officer queue when ALS rejects. R-RES-16 is the neighbouring step that routes a signed restructure offer to operations for the same booking action, and it is cited here only because the harness runs the settlement path beside it.

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| WITH_OPS_SETTLEMENT | SETTLEMENT_BOOKED | agreement signed and terms booked in ALS | AWAITING_PAYMENT (R-SET-13) |
| WITH_OPS_BOOKING | BOOKING_CONFIRMED | ALS and NLEADS both acknowledge | BOOKED_IN_ALS_NLEADS (R-RES-22) |
| WITH_OPS_BOOKING | BOOKING_REJECTED | ALS rejects the booking | WITH_OPS_BOOKING, with the error on the officer queue (R-RES-23) |
| AWAITING_PAYMENT | PAYMENT_RECEIVED | `amount_received` = `settlement_amount` | PAYMENT_CLEARED (R-SET-14) |

These are the owner's states: rwb-treatment holds the treatment state, rwb-case holds the case state, and P3 moves the case on the facts the loop raises. The harness changes none of them itself. It seeds through the owning services' published operations, posts the accepted treatment through the rwb-treatment contract, and then asserts the state the owner reached, naming the owner and the operation behind each move in the report. A state the harness set by hand would prove nothing.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-CASEOWN, RW-RESTRUCT, RW-SPECIAL, and the operations roles that hold Treatment and offer C | Post the accepted treatment so the booking is raised, and read the treatment through the rwb-treatment contract |
| RW-CASEOWN, RW-TEAMMGR, RW-PHONECOL, RW-FIELDCOL and roles that hold the case record R | Read the same journey evidence, including the outbound item, the case state and the decision record |
| QA lead | Owns the harness configuration, the ALS interface fixture, the report shape and the pass or fail gate |
| Integration lead | Owns the harness code, the stub set and the swap from a fake to the real service |
| The owning services' identities | rwb-treatment, rwb-integration, rwb-source-data, rwb-case, rwb-decision and rwb-access make every change the harness asserts |
| No approval level from the delegation of authority applies | The harness takes no business decision; the settlement approval belongs to the treatment story and the booking authority to operations |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 to DF-CAS-023 | recovery_case | status, and the case identity the booking is keyed by | Read, through the rwb-case contract |
| DF-ACE-001 to DF-ACE-042 | v_ace_account | account_key, account_code, account_status, contract_no, product_category_efs, total_balance, and the booked position | Read, through the rwb-source-data data product (DP-05) |
| DF-ACE-043 to DF-ACE-054 | v_ace_payment | payment_code, account_key, payment_date, payment_amount, payment_channel, capital_amount, and the settlement payment | Read, through the rwb-source-data data product (DP-05) |
| DF-OPS-168 to DF-OPS-177 | outbound_item | id, interface_id, idempotency_key, payload_ref, case_ids, attempt_count | Read, through the rwb-integration admin operation |
| DF-TRT-001 to DF-TRT-014 | treatment | id, case_id, decision_log_id, treatment_type, proposed_by, proposed_at, state, and the accepted settlement terms | Read and write, through the rwb-treatment contract |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | case_id, decision_code, rule_id, rule_version, model_version | Read, through the rwb-decision contract |
| DF-REF-001 to DF-REF-015 | rule_row | rule_id, rule_version, route_set, from_state, event_code | Read, through the rwb-decision contract |

Field IDs are those in the Logical Data Model and Data Dictionary, taken from the legacy key. Reference data read by this story: the rule rows of DF-REF-001 to DF-REF-015 through the rwb-decision contract; the reference-data contracts DP-06 and DP-07 apply to these reads, and the parameter keys read are not specified in the source documents (DOR-RWB-ITG-E4046-ITG-20). Which of the ten `outbound_item` field IDs carries each field the harness reads, and the `interface_config` field IDs that sit behind the ALS booking, are not specified in the source documents (GAP-0432; ASM-0608). The harness owns no table and writes no row directly: every read and every seed goes through the API of the owning service (DP-01, DP-05), and the account and payment rows are ACE's, so the Workbench holds no account or payment copy (legacy RWB-E4-046; D-RCV-35 U1 and U4).

### 12. Contract

#### 12.1 REST operations provided

None. The harness is a test runner and provides no REST operation.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| GET | `/api/recovery/treatment/v1/treatments/{treatmentId}` | S2 rwb-treatment | The accepted settlement terms to be booked (AC1) |
| POST | `/api/recovery/treatment/v1/treatments/{treatmentId}/submit` | S2 rwb-treatment | Post the accepted treatment so the booking is raised (AC1) |
| GET | `/api/recovery/integration/v1/admin/outbound-items` | P2 rwb-integration | The ALS booking item and its interface config (AC1) |
| GET | `/api/recovery/integration/v1/admin/outbox/deliveries` | P2 rwb-integration | The delivery of that item (AC1) |
| GET | `/api/recovery/source-data/v1/data-products/{productCode}/records` | P1 rwb-source-data | The booked position from `v_ace_account` and the settlement payment from `v_ace_payment` (AC1, DP-05) |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The case state after the booking (AC1) |
| GET | `/api/recovery/decision/v1/decision-log` | P7 rwb-decision | The record with the rule ID and version (AC1) |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | Role and scope, including the refusal path |

Every operation is one hop on the owner's base `/api/recovery/<short>/v1`, with a 2 s timeout and a circuit breaker per downstream. Where a screen would compose them, the harness calls the gateway-bff composite route (DP-19). The `{productCode}` that carries `v_ace_account` and `v_ace_payment` records, the ALS interface ID and transport, and the operation in rwb-payment that posts the booking are not specified in the source documents (GAP-0432; ASM-0608). No operation is invented in this story.

#### 12.3 Events published

None. The harness publishes no Kafka event; it posts the accepted treatment through the rwb-treatment contract and consumes the owners' events.

#### 12.4 Events consumed

| Event | Topic | Producer | Use |
|---|---|---|---|
| `rwb.treatment.TreatmentApproved.v1` | `rwb.treatment.events.v1` | S2 rwb-treatment | The settlement was approved before the run (AC1) |
| `rwb.integration.FileDelivered.v1` | `rwb.integration.events.v1` | P2 rwb-integration | The ALS booking delivered, where the configured interface is a file (AC1) |
| `rwb.integration.FileFailed.v1` | `rwb.integration.events.v1` | P2 rwb-integration | The ALS booking failed, where the configured interface is a file (AC1) |
| `rwb.decision.DecisionRecorded.v1` | `rwb.decision-record.v1` | every service, through its own local decision-record library | The record reaches the ledger within 5 minutes (AC1, DP-03) |

All four carry IDs and business facts only, keyed by caseId with the treatment ID on the treatment event, and the harness asserts that no personal data is present.

#### 12.5 Workflows and activities

None added. The harness exercises TreatmentWorkflow on queue rwb-treatment, which carries the settlement step and raises the booking, and CaseWorkflow on queue rwb-case, which holds the case while the booking is outstanding, and the `deliverFile` activity on queue rwb-integration, which is the outbound leg to ALS. It asserts their effects through the services' contracts and the owners' topics. No workflow, activity or Schedule is created, changed or owned by this story.

#### 12.6 Schedules

None added. The booking is triggered by the accepted treatment and not by a Schedule, and this story sets no cron, overlap policy or catch-up window. The read-back from `v_ace_account` and `v_ace_payment` follows the next ACE batch, which the bank's Airflow signals as ready; the harness waits for that signal and sets no timer of its own.

#### 12.7 Tables owned

None. The harness owns no schema and no table (DP-01); the treatment is rwb-treatment's, the interface config and outbound items are rwb-integration's, the booking and posting are rwb-payment's, the case is rwb-case's, the record is rwb-decision's, and the account and payment rows are ACE's, read through rwb-source-data's contract (DP-05).

#### 12.8 Contract fakes

| Fake | Contract | Use in the run |
|---|---|---|
| Stub for rwb-treatment | `GET /treatments/{treatmentId}`, `POST /treatments/{treatmentId}/submit`, `rwb.treatment.events.v1` | Day-1 run of AC1 and of the negative path before RWB-P8-E4046-APP and RWB-P2-E4046-APP are live |
| Stub for rwb-integration | `GET /admin/outbound-items`, `GET /admin/outbox/deliveries`, `rwb.integration.events.v1` | Day-1 assertions on the ALS booking item, its interface config and its delivery |
| Stub for rwb-source-data | `GET /data-products/{productCode}/records` | Day-1 assertions on the booked position and the settlement payment |
| Stub for rwb-case | `GET /cases/{caseId}` | Day-1 assertions on the case state after the booking |
| Stub for rwb-decision | `GET /decision-log` | Day-1 assertion of one record for the booking with its rule version |
| Stub for rwb-access | `POST /authorise` | Day-1 authorisation and refusal path |
| Treatment event stub | `rwb.treatment.TreatmentApproved.v1` | The approval that precedes the booking, where the environment does not run the treatment stage |
| File event stub | `rwb.integration.FileDelivered.v1`, `rwb.integration.FileFailed.v1` | The delivered and failed ALS booking, where the interface is a file |

Each fake is generated from the published OpenAPI or AsyncAPI document of its service, and its version is pinned in the run report, so a contract change shows up as a run failure and not as a silent pass. The version of each published contract fake library the stub set is generated from is read from the contract registry at the start of the run and recorded in the report, and a run whose fake library version differs from the registry fails before any assertion; the version itself is not specified in the source documents (DOR-RWB-ITG-E4046-ITG-22). The contract version this story builds against is the version the registry pins for each service, and each run records it beside the fake library version; the version numbers are not specified in the source documents (DOR-RWB-ITG-E4046-ITG-23). The ALS interface ID and transport, the booking operation in rwb-payment, the data product code, the `outbound_item` field IDs, the harness environment, the seeding set and the evidence format are not specified in the source documents (GAP-0432; ASM-0608).

#### 12.9 Call-type summary

| Call type | In this story |
|---|---|
| REST | 0 provided, 8 consumed, one hop each on `/api/recovery/<short>/v1` with a 2 s timeout and a circuit breaker per downstream, composed through gateway-bff where a screen would (DP-19) |
| Kafka | None published; `rwb.treatment.TreatmentApproved.v1`, `rwb.integration.FileDelivered.v1`, `rwb.integration.FileFailed.v1` and `rwb.decision.DecisionRecorded.v1` consumed (DP-03) |
| Temporal | Exercised only: TreatmentWorkflow on queue rwb-treatment, CaseWorkflow on queue rwb-case and the `deliverFile` activity on queue rwb-integration; none added |
| File | Only where the configured ALS interface is a file, modelled by the outbound fixture |

### 13. Solution plan

**Package.** Folder `itg/recovery`, package `th.co.scb.ace.workbench.recovery.itg`, test scope only; not part of any deployed service.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The platform H dependencies in the table above (RWB-PLT-E1027-CON and RWB-PLT-N001-CON) are delivered by the platform wave and are not repeated in the metadata H row of this story, which stays None. The blocking dependencies are the two I stories, RWB-P8-E4046-APP and RWB-P2-E4046-APP: until they are live the run uses the rwb-treatment and rwb-integration stubs, and a stub pass is reported as a stub pass.

The decoupling is also the story's reading of the legacy behaviour. The harness owns no schema (DP-01) and reads the treatment, the outbound item, the case, the record and the ACE rows from their owners only. The account and payment rows are read through rwb-source-data's data product, which owns the ACE view contract, and not through a view of the harness's own (DP-05). The record is read from rwb-decision's contract and the shared `rwb.decision-record.v1` topic rather than from a local log table (DP-03). The composed reads a screen would make are exercised through the gateway-bff composite route (DP-19).

**Harness components**

| Component | Type | Responsibility |
|---|---|---|
| SettlementBookingRunner | Job | Runs the owned criterion and the negative path in order for a business date and holds the run lock |
| StubSet | Fake | The six service stubs and the two event stubs of section 12.8, each generated from the published contract with the version pinned |
| AlsBookingFixture | Fixture | The outbound item on the configured ALS interface, its delivery or failure, and the interface config it is keyed by |
| AceReadbackProbe | Service | Reads the booked position from `v_ace_account` and the settlement payment from `v_ace_payment` through the data product after the next ACE batch, and asserts them for `A-0001` |
| EventProbe | Service | Consumes `rwb.treatment.events.v1`, `rwb.integration.events.v1` and `rwb.decision-record.v1` and asserts the facts for the case |
| EvidenceReport | Service | Writes the report keyed by story and business date and holds the pass or fail gate |

**Environment and test data.** SIT, against the fakes from Day 1 and the real services as they land, on account `A-0001` with its next ACE batch seeded, one case with the accepted settlement treatment `T-0001` at 820000, and one case at `WITH_OPS_BOOKING` for the acknowledgement and rejection paths. The environment, the seeding set, the data product code, the ALS interface fixture and the evidence retention are not specified in the source documents (GAP-0432; ASM-0608). Seeding uses only the owning services' published operations, never a schema write. The wave 3 entry check, with the integration and QA leads, settles these values and the ALS interface values with the integration lead (GAP-0436; GAP-0432).

**Build steps**

1. Generate the six service stubs and the two event stubs from the published contracts, pin each version in the report and fail the run on a version mismatch (X1, X11).
2. Build the AlsBookingFixture and prove one outbound item from creation to delivery for a business date (X3, X5).
3. Build the SettlementBookingRunner for AC1: read the accepted terms, post the treatment, assert the ALS booking item and its delivery, read the booked position and the payment through the data product, and assert the case state after the booking (X2, X4, X6, X7).
4. Assert one record for the booking through the rwb-decision contract, naming the rule ID and version, and fail where either is absent (X7).
5. Add the EventProbe for `rwb.treatment.TreatmentApproved.v1`, `rwb.integration.FileDelivered.v1`, `rwb.integration.FileFailed.v1` and `rwb.decision.DecisionRecorded.v1`, and assert the key, the 5-minute arrival and the absence of personal data (X5, X8).
6. Add the acknowledgement and rejection paths of R-RES-22 and R-RES-23 as observed facts: the reference recorded when both systems acknowledge, and the error on the officer queue when ALS rejects, with the case kept with operations.
7. Add the negative path: force the decision record to fail, assert that nothing moves and record the message the owner returns (X9).
8. Add the access path through `POST /api/recovery/access/v1/authorise`, including the refusal for a role that does not include the right (X10).
9. Add the EvidenceReport and the gate, then swap the rwb-treatment and rwb-integration stubs for the real services as RWB-P8-E4046-APP and RWB-P2-E4046-APP land and rerun the criterion.

**Feature switch.** The legacy key names no feature switch for this behaviour. The harness runs behind the platform feature-flag library as the wave releases it; the flag key is not specified in the source documents (GAP-0432; ASM-0608).

**Done when.** The tests of section 16 pass; the criterion passes against the fakes on Day 1 and again against rwb-treatment, rwb-payment and rwb-integration when RWB-P8-E4046-APP and RWB-P2-E4046-APP land; and the wave entry check holds a report keyed by story and business date with the contract, fixture and ACE batch versions named.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P7-003 | The decision record for the booking cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | The caller's role does not include the right, or the case is outside their scope | You cannot {action} here. Your role does not include it. |
| MSG-GEN-001 | A required value is missing from the request | Enter {field}. |

R-SET-10, R-SET-13, R-RES-22 and R-RES-23 carry no message ID in the rule set, so the harness asserts the state, the data, the outbound item and the decision record, and names a message ID only where an owning service returns one of the three above. The harness produces none of these messages itself.

### 15. Screens and states

SCR-28 Proceeds matching is the screen the legacy key names for this behaviour:

| State | What the user sees and does |
|---|---|
| Loading | The booking and the payment read-back are running for the business date |
| matched | The booked position and the settlement payment, read through the rwb-source-data data product, are aligned to the case |
| unmatched | The booking or the payment does not align to the case, and an officer has to resolve it |
| Empty | Not specified in the source documents (CG-ALL-892) |
| Error | Not specified in the source documents (CG-ALL-892) |
| No access | Not specified in the source documents (CG-ALL-892) |

The harness renders no screen. It reads these states through the rwb-treatment, rwb-integration, rwb-source-data, rwb-case and rwb-decision contracts, so a passed run means the screen has the right data behind it. What the wave entry check looks at instead is the evidence report, whose format and retention are not specified in the source documents (GAP-0432; ASM-0608).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E4-046-01-ITG | AC1, AC4, BR1, BR2, BR3, BR4, BR5, BR6, BR7 | Integration | Settlement `T-0001` at 820000 for account `A-0001`; ALS booking item |
| TC-E4-046-02-ITG | Negative path of AC2, run by RWB-P8-E4046-APP; BR7 | Integration | Decision log forced to fail; MSG-P7-003 |
| TC-E4-046-03-ITG | AC3, Access | Component | A role without the right; MSG-P4-002 |
| TC-E4-046-04-ITG | Principle 5 | NFR | Forced decision-log write failure; nothing moves |
| TC-E4-046-05-ITG | AC5 | Integration | Settlement `T-0001` at 820000 for account `A-0001`; TreatmentApproved delivered twice |
| TC-E4-046-06-ITG | AC6 | Integration | Settlement `T-0001` at 820000 for account `A-0001`; a consumed call that fails or does not answer |
| TC-E4-046-07-ITG | AC7 | Integration | Settlement `T-0001` in a case state the booking does not allow |

These are the ITG copies of TC-E4-046-01 to TC-E4-046-04 and carry the legacy data unchanged, with the component and NFR copies keeping the legacy levels. The full legacy tests, with their Given, When and Then, are in `Recovery Workbench Test Cases v8.xlsx`, tab Story test cases, under those IDs.

### 17. Guardrails

- No business value in code: the rule versions, the ALS interface fixture, the settlement amount and account of the run, the seeding set and the result mappings are data.
- No personal data in logs, fixtures, reports, tests or prompts: the events carry IDs and business facts only, and the harness asserts the absence of personal data.
- No read of another service's tables: every read and every seed goes through the owning contract (DP-01), and the account and payment rows are ACE's, read through rwb-source-data's data product (DP-05).
- The Workbench writes nothing to ALS directly and holds no account or payment copy; the agreed terms leave as an outbound item and the position is read back from `v_ace_account` and `v_ace_payment` (REQ-CHO-008; REQ-S2-008; D-RCV-35 U1 and U4).
- One hop and a 2 s timeout per call, with a circuit breaker per downstream, so the harness fails where a screen would.
- A stub pass is never reported as a real-service pass: the report names the contract version and whether the hop was a stub or the owner.
- The harness never runs against UAT or production, and it never sets a treatment, booking, case or decision state by hand.
- A failing assertion is fixed in the service that owns it or reported as a gap; it is never waived in the script.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-S2-008 | Booked terms, settled accounts and released collateral are posted to their systems of record without re-keying | Business Requirements Program v5, section 5.9 | FEAT-PAY-06 | D6.4 settlement | R-SET-10, R-SET-13, R-RES-22 | TC-E4-046-01-ITG |
| REQ-CHO-008 | Terms booked in the core system are recorded on the case, and the booking is confirmed from the next business date's ACE account data in `v_ace_account` | Business Requirements Program v5, section 5.3 | FEAT-PAY-06; FEAT-CHO-08 | D6.4 settlement | R-SET-13, R-SET-20 | TC-E4-046-01-ITG |
| REQ-DRI-007 | The integration adapters log every outbound file, retry on a defined schedule and place failures in an exception queue | Business Requirements Program v5, section 5.2 | FEAT-PAY-06 | D6.4 settlement | R-SET-10, R-RES-22, R-RES-23 | TC-E4-046-01-ITG |
| REQ-DRI-001 | Every decision writes one record holding the case, the decision, the rule and its version | Business Requirements Program v5, section 5.7 | FEAT-PAY-06 | D6.4 settlement | R-SET-13, R-RES-22 | TC-E4-046-01-ITG, TC-E4-046-02-ITG, TC-E4-046-04-ITG |

### 19. Out of scope

- AC2 of the legacy key, the refusal when the decision log cannot be written, which is owned by RWB-P8-E4046-APP; this story exercises it only as a negative path.
- The rwb-payment behaviour itself: the booking, the posting file and the payment matching are RWB-P8-E4046-APP.
- The rwb-integration interface build, the outbound item lifecycle, the retry and the exception queue, which are RWB-P2-E4046-APP.
- The ALS interface itself: its ID, transport, message or file layout, result codes and test endpoint, none of which a source read gives.
- The production treatment and payment endpoints, TreatmentWorkflow on the rwb-treatment queue, the payment and posting activities on the rwb-payment queue, and the `rwb_treatment` and `rwb_payment` tables.
- The contract baselines of the six services, which are their CON stories and are consumed here through the published documents and their fakes.
- The platform configuration: the decision-record library, the gateway-bff composite route, the feature-flag library and the observability set.
- The next ACE batch itself, its Airflow DAG and its readiness signal, which belong to ACE and to rwb-source-data; the harness only waits for the batch and reads its result.
- Any production screen, event, workflow, Schedule or table: this story builds a test harness and its evidence only.
- The fixture contents, the harness environment, the evidence format and its retention, and the feature flag key: carried as a gap and an assumption, not decided here.
