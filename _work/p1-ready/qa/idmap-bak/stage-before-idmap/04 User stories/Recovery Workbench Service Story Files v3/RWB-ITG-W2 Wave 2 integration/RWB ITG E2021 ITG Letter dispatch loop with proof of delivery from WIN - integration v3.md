# RWB-ITG-E2021-ITG Letter dispatch loop with proof of delivery from WIN

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Version 3 changes** (D-RCV-60 P1 developer readiness, RD-P1 register)

- The ledger is read on the case-scoped path with the case UUID, and each entry is asserted by `eventCode`, `conductCheck`, `deliveryStatus`, `externalRef` and business key (RD-P1-007; findings 1 and 3).
- The proof entry is appended by rwb-comms from the rwb-source-data proof-of-delivery read; the Workbench ingests no INT-15 file (finding 2).
- The contact point and consent read is named as the DP02 record read; contract version and dependencies added (RD-P1-005; findings 5 and 6).
- A ledger append writes no decision record; the one record is the acting service's (finding 4). Remaining delivery steps are in section 20.
- Finishing pass: test case IDs of Test Cases v9 cited in place of the placeholders.
- The delivery entry pairs with the dispatch entry on the barcode (externalRef) with a UUID version 5 business key; NEW-GAP-S10-16 is closed (RD-P1-064 rules 4 and 6).

| Item | Value |
|---|---|
| Story key | RWB-ITG-E2021-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W2 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-021 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP05, DP07, DP09, DP10, DP11, DP13, DP18, DP19 |
| Parallel lane | L-ITG-W2 |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-ITG-E2021-ITG-16) |
| Depends on (build) | RWB-P1-E2021-APP, RWB-P3-E2021-APP, RWB-P4-E2021-APP, RWB-P6-E2021-APP, RWB-P7-E2014-APP, RWB-P7-E2021-APP |
| Contract dependencies | rwb-access provider contract for POST /api/recovery/access/v1/authorise (contract story: Not specified in the source documents (DOR-RWB-ITG-E2021-ITG-21)); contract version /v1; RWB-P1-E1066-CON (interaction ledger) and the DP02 record read and proof-of-delivery read of rwb-source-data, built against rwb-source-data.yaml 5.1.0 (API Specification v7) |
| Integration dependencies | RWB-P7-E2014-APP, RWB-P6-E2021-APP, RWB-P1-E2021-APP, RWB-P4-E2021-APP, RWB-P3-E2021-APP, RWB-P7-E2021-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to REQ-OCC-003, REQ-OCC-005, REQ-OCC-006, REQ-ILG-010) |
| Conduct and consent rule package | Not specified in the source documents (GAP-1610); governed in rwb-decision |
| Status | Draft (directive resolutions) |
| Readiness decisions | RD-P1-005, RD-P1-007, RD-P1-064 |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-021 for the wave 2 integration harness. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-ITG-E2021-ITG). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (18 resolved, 31 cross-document, 3 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3, as listed under Version 3 changes.

### 1. Story

As a **litigation officer (RW-LITOFF)**, I want **one repeatable cross-service journey harness that runs a letter from the conduct check through the WIN file, the acknowledgment and the INT-15 proof of delivery to the notice-period timer, against the owning services' published contracts and their fakes**, so that **the notice period is proven to start from proof of delivery and not from printing, and no letter is proven to reach the WIN file while a contact stop or a legal hold is on**.

### 2. Business rationale

A notice period counted from the print date can be challenged, and a letter sent while a contact stop is on is a conduct breach. Those two outcomes are only as good as the loop that produces them: the conduct check in rwb-comms, the WIN letters file (INT-14) sent through rwb-integration on the 16:00 window (JOB-10), the WIN acknowledgment, the INT-15 proof file that ACE ingests, the ledger entry in rwb-source-data, the decision record in rwb-decision and the NOTICE_PERIOD timer in rwb-case. That loop crosses six services and four call types, so a defect at any hop shows up as a wrong notice state or a timer that starts on the wrong date.

This story owns the harness that proves the loop, and the four legacy criteria that describe it end to end: AC1 dispatch, AC2 proof back, AC4 contact stop blocks the letter and AC5 consent withdrawn does not stop a statutory notice. It serves REQ-OCC-003, REQ-OCC-005, REQ-OCC-006 and REQ-ILG-010, and it carries CTL-15 and CTL-16 and the FSD P6 measure "notices with proof of delivery, 100 percent" into evidence.

The harness is decoupled the same way the services are. It calls each owner's base `/api/recovery/<short>/v1` and never a monolith base (DP-13, DP-01), it calls through the gateway-bff composite route where a screen would (DP-19), every call is one hop with a 2 s budget (DP-11), the ledger is read from rwb-source-data and never from a table (DP-05, DP-18), reference data such as the statutory notice type list is read from rwb-case (DP-07), the decision record is read from rwb-decision and its library and topic (DP-03), the dispatch and delivery facts are consumed as Kafka events from the owner's topic (DP-09), and the 16:00 run of JOB-10 is exercised on the Schedule in rwb-comms rather than a Quartz row (DP-10).

### 3. Preconditions

- The harness runs in SIT, with the WIN file-drop fixture and the INT-15 proof-file fixture on the JOB-10 16:00 window: Not specified in the source documents (GAP-0404; ASM-0579).
- Proof-of-delivery capture stays behind its feature flag until RWB-ACE-001 lands and the `v_ace_pod` view is available (DL43; GAP-1608). The fallback is proof entered by hand against the barcode, to be agreed with the litigation business owner before wave 2.
- The ledger path takes the case UUID: the seed of case `RC-2026-000321` uses `c0000000-0000-4000-8000-000000000321`. The proof result reaches rwb-comms as rows of `GET /api/recovery/source-data/v1/proof-of-delivery?businessDate=` over `v_ace_pod`; ACE ingests the WIN proof file and the Workbench ingests no INT-15 file, so the INT-15 proof-file fixture of this story stands for the fake answer of that read, or in SIT for ACE test rows.
- The published contracts of rwb-comms, rwb-case, rwb-source-data, rwb-access and rwb-decision are in the contract registry, and a WireMock stub set is generated from each one.
- The dispatch-eligible notice states are set to Approved (`rwb.comms.dispatch.eligible-states` = APPROVED), and the proof window is the 7 days of R-LIT-08, both present as data, not code.
- The statutory notice type list is readable as reference data through the rwb-case reference-data contract (DP-07); the list of statutory types is data owned by the business, and this story reads it and does not set it.
- An approver path exists so that a notice reaches state Approved before the run; notice approval itself is RWB-P7-E2014-APP.
- A SIT case, notice, deviation, contact point and consent status can be seeded through the owning services' published operations only; the seeding set and the harness environment specification are not specified in the source documents (GAP-0404; ASM-0579).
- The feature switch `rwb.comms.win-dispatch-loop` is on for the environment under test.
- No build dependency. Day 1, with the fakes in place from the first run, and each fake replaced by the real service as its I story lands.

### 4. Flow

1. Harness: seeds the SIT case `RC-2026-000321`, its notice `N-0101` (type DEMAND, template DEMAND-SSME, language TH, version 1 Approved), its contact point, its consent status and, for the blocked run, the open deviation, through the owning services' published operations only.
2. Harness: requests the notice with `POST /api/recovery/comms/v1/cases/{caseId}/notices` and reads it back with `GET /api/recovery/comms/v1/notices/{noticeId}`, proving the notice is built and returned by its owner (DP-11, DP-13).
3. Harness: reads the case with `GET /api/recovery/case/v1/cases/{caseId}` for legal hold and queue state, and `GET /api/recovery/case/v1/cases/{caseId}/timers` for a NOTICE_PERIOD timer, before and after the run.
4. Harness: holds the JOB-10 window at 16:00 on the business date under test on the rwb-comms Schedule and triggers the file window; the window control and its fixture are not specified in the source documents (GAP-0404; ASM-0579).
5. Harness: drops the INT-14 WIN letters fixture, then reads the WIN acknowledgment fixture and asserts the barcode RR223344556TH and the sent date reach the notice as Sent.
6. Harness: subscribes to `rwb.comms.events.v1` and asserts `rwb.comms.NoticeDispatched.v1` (EV-14) carries the notice for the case and no personal data.
7. Harness: drops the INT-15 proof-file fixture for the barcode with result DELIVERED and the call-back date, asserts `rwb.comms.NoticeDelivered.v1` (EV-15), and asserts the notice becomes Delivered with the call-back date. The fixture is the answer of the proof-of-delivery read that rwb-comms calls (or ACE test rows in SIT), and rwb-comms alone appends the proof entry.
8. Harness: asserts the ledger entries through `GET /api/recovery/source-data/v1/cases/{caseId}/interactions` with `{caseId}` the case UUID: the dispatch entry with `eventCode` LETTER, `conductCheck` PASSED, `deliveryStatus` SENT, `externalRef` RR223344556TH and the barcode summary, and the proof entry with `eventCode` LETTER and `deliveryStatus` DELIVERED, and the decision record through `GET /api/recovery/decision/v1/decision-log`.
9. Harness: asserts the NOTICE_PERIOD timer on `GET /api/recovery/case/v1/cases/{caseId}/timers` is running from the delivery date and not from the sent date.
10. Harness: repeats the run with the open X1 deviation and the contact stop on, and asserts the notice is Held with hold reason CONTACT_STOP_X1, the conduct check is BLOCKED, one decision entry names R-LIT-05 (written by the acting service; the ledger append writes none), and the WIN file fixture does not contain the notice.
11. Harness: repeats the run with the postal consent status WITHDRAWN on a statutory notice type, and asserts the notice is written to the WIN file and the conduct check is PASSED with the summary "Statutory notice, consent withdrawn".
12. Harness: authorises each call through `POST /api/recovery/access/v1/authorise` and records the refusal path for a caller outside the case scope.
13. Harness: publishes the per-run evidence report keyed by story and business date, with the four criteria and their assertions, and gates the wave on the result.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A fake answers a shape the published contract does not allow | The run fails at that hop; the report names the service, the operation and the contract version | None | AC1 |
| X2 | The WIN window fixture is not picked up inside the run window | The run fails and the report names the window and the fixture; the run is not marked passed | None | AC1 |
| X3 | The INT-15 proof fixture is not read back | The run fails and the report names the fixture; a notice that stays Sent is reported as an unproven delivery, not as a pass | None | AC2 |
| X4 | `rwb.comms.NoticeDispatched.v1` or `rwb.comms.NoticeDelivered.v1` is not consumed inside the run window | The run fails and the report names the event and the topic | None | AC1, AC2 |
| X5 | The notice is written to the WIN file while the contact stop is on | The run fails on AC4 regardless of the notice state | None | AC4 |
| X6 | A statutory notice is held because consent was withdrawn | The run fails on AC5 | None | AC5 |
| X7 | The NOTICE_PERIOD timer starts from the sent date | The run fails on AC2 and the report names the two dates | None | AC2 |
| X8 | A caller outside the case scope is authorised | The run fails on the access check and the report names the operation | None | AC4 |
| X9 | A real service is reachable but its contract version differs from the registry | The run fails before any assertion and the report names the service and both versions | None | AC1 |

The report text is for the wave entry check and is not part of the message standard. The business messages the journey produces are in section 14 and are asserted as data on the notice, the case and the ledger.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Runs against published contracts and fakes from Day 1; the only waits are the six I stories, one at a time |
| Negotiable | The fixtures, the window control and the report shape are configuration and agreed at the wave entry check, not business values in code |
| Valuable | The dispatch loop and the proof-based notice period are proven end to end before the wave opens |
| Estimable | One harness runner, one stub set, two file fixtures, one event probe, one report |
| Small | Fits in one sprint with its tests |
| Testable | Each criterion runs against its fake and again against the real owner as the I story lands |

### 7. Acceptance criteria

```gherkin
Feature: Letter dispatch loop with proof of delivery from WIN

  Background:
    Given the dispatch-eligible notice states are "APPROVED"
    Given the proof window is 7 days
    Given notice "N-0101" for case "RC-2026-000321" is "Approved" with notice type "DEMAND" and template "DEMAND-SSME" "TH" version 1 Approved
    Given case "RC-2026-000321" has no legal hold and no open deviation

  Scenario: AC1 Dispatch (legacy RWB-E2-021 AC1)
    Given JOB-10 runs at 16:00 on 2026-12-14
    When the conduct check passes and WIN acknowledges contract "CT-88001" with barcode "RR223344556TH" and sent date 15122026
    Then notice "N-0101" is "Sent" with barcode "RR223344556TH" and sent date 2026-12-15
    Then the ledger entry for the letter, read with caseId "c0000000-0000-4000-8000-000000000321", has eventCode "LETTER", deliveryStatus "SENT", externalRef "RR223344556TH", conduct check "PASSED" and summary naming barcode "RR223344556TH"
    Then its idempotencyKey starts "EV-14-RC-2026-000321-" and ends with the UUID of the dispatch action
    Then GET /notices/N-0101 returns sentDate 2026-12-15 and barcode "RR223344556TH"

  Scenario: AC2 Proof back (legacy RWB-E2-021 AC2)
    Given notice "N-0101" is "Sent" on 2026-12-15
    When the INT-15 file of 2026-12-21 returns barcode "RR223344556TH" with result "DELIVERED" and call-back date 18122026
    Then notice "N-0101" is "Delivered" with callback date 2026-12-18
    Then the ledger has an entry "Delivered" for case "RC-2026-000321" on 2026-12-18, that is eventCode "LETTER" and deliveryStatus "DELIVERED" appended by rwb-comms with idempotencyKey "LETTER-RC-2026-000321-20261218-{u}", where {u} is the UUID version 5 of the proof row's podKey in the RFC 9562 URL namespace, and externalRef "RR223344556TH", the barcode of the dispatch entry
    Then no entry is updated and the dispatch entry is unchanged
    Then case "RC-2026-000321" has a running "NOTICE_PERIOD" timer started on 2026-12-18 by rwb-case on the INT-15 DELIVERED result

  Scenario: AC4 Contact stop blocks the letter (legacy RWB-E2-021 AC4)
    Given case "RC-2026-000321" has an open deviation "X1" with contact stop on
    When JOB-10 runs on 2026-12-14
    Then the system does not writ notice "N-0101" to the WIN file
    Then notice "N-0101" is "Held" with hold reason "CONTACT_STOP_X1"
    Then the ledger entry has eventCode "LETTER", conduct check "BLOCKED", no deliveryStatus and no externalRef
    Then one decision log entry exists with rule "R-LIT-05"
    Then rwb-source-data writes no decision record for the ledger append
    Then the system routes the case to the complaint officer with MSG-P6-001 naming "X1 Dispute or complaint"

  Scenario: AC5 Consent withdrawn does not stop a statutory notice (legacy RWB-E2-021 AC5)
    Given the borrower's postal address contact point has consent status "WITHDRAWN"
    Given notice type "DEMAND" is a statutory notice
    When JOB-10 runs on 2026-12-14
    Then the system writes notice "N-0101" to the WIN file
    Then the ledger entry has eventCode "LETTER", conduct check "PASSED" and summary "Statutory notice, consent withdrawn"

  Scenario: AC13 Duplicate delivery of a consumed event (new, D-RCV-60)
    Given notice "N-0101" for case "RC-2026-000321" is "Delivered" with callback date 2026-12-18
    Given the ledger has one entry "Delivered" for case "RC-2026-000321" on 2026-12-18
    When the INT-15 file of 2026-12-21 returns barcode "RR223344556TH" with result "DELIVERED" and call-back date 18122026 a second time
    Then the ledger still has exactly one entry "Delivered" for case "RC-2026-000321" on 2026-12-18, with the same id and caseSeq (a repeat of the business key answers 200 with the existing entry)
    Then case "RC-2026-000321" has one running "NOTICE_PERIOD" timer and no second timer is started

  Scenario: AC14 Consumed call fails or does not answer (RWB-ITG-E2021-ITG) (new, D-RCV-60)
    Given notice "N-0101" for case "RC-2026-000321" is "Sent" on 2026-12-15
    When the consumed call fails or does not answer
    Then notice "N-0101" keeps its state "Sent" with no change recorded
    Then the record kept of the failure is "Not specified in the source documents (NEWAC-RWB-ITG-E2021-ITG-AC14)"

  Scenario: AC15 Disallowed status change is refused (RWB-ITG-E2021-ITG) (new, D-RCV-60)
    Given notice "N-0101" for case "RC-2026-000321" is "Delivered" with callback date 2026-12-18
    When a status change from "Delivered" to "Approved" is requested for notice "N-0101"
    Then the change is refused and notice "N-0101" stays "Delivered"
    Then the ledger has no new entry for case "RC-2026-000321"
```

AC3 and AC6 to AC12 are cited in the flow and exception table but are owned by the app stories of this legacy key (RWB-P6-E2021-APP, RWB-P1-E2021-APP, RWB-P3-E2021-APP, RWB-P4-E2021-APP and RWB-P7-E2021-APP); the seven criteria above are the ones this ITG story owns.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every letter is checked before it is written to the WIN file, and the result is on the ledger entry | REQ-OCC-005; FEAT-OCC-05 |
| BR2 | A contact stop from X1 or X2 holds the notice and routes the case to the deviation owner | R-LIT-05; CTL-16 |
| BR3 | A legal hold stops every outbound action | R-UNI-20 |
| BR4 | Withdrawn consent removes the channel from the contact plan, and statutory notices continue | R-UNI-10; REQ-OCC-006; CTL-16 |
| BR5 | The notice period starts from the delivery date on the proof | R-LIT-07; CTL-15 |
| BR6 | A refused, returned or undeliverable letter records the result and queues an alternate service method | R-LIT-09 |
| BR7 | No proof inside the proof window marks the notice unserved, and the notice period does not start | R-LIT-08 |
| BR8 | A withdrawn template holds the notice | R-LIT-04 |
| BR9 | A held or unserved result that cannot be written to the decision log does not proceed | Principle 5; R-UNI-39 |
| BR10 | Which notice types are statutory is a list held as reference data | Principle 1; LOV-NOTICE |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| In progress | Offer or notice sent to the customer | WIN acknowledges the notice | Waiting customer |
| In progress | Deviation flagged or legal hold placed | Contact stop or legal hold found at the check | ON_HOLD |

The case status moves are made by P3 on the events the dispatch loop raises. The owning services change the notice state: Approved to Sent, Approved to Held, Sent to Delivered, Sent to Unserved (DELIVERY_FAILED, PROOF_WINDOW_EXPIRED).

The harness changes no state itself. It seeds through the owning services' published operations, drives the 16:00 window and the two file fixtures, and then asserts the states the owners reached: notice Approved, Sent, Held, Delivered and Unserved, and the case status Waiting customer or On hold. A state the harness set by hand would prove nothing, so the report names the owner and the operation that made each move.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-LITOFF, litigation officer | Reads the notice, its dispatch and its proof through the rwb-comms contract; owns the journey case for the run |
| RW-CONDUCT, Conduct and QA officer | Reads the blocked contacts on the ledger for AC4 |
| RW-HEADLIT and roles with Litigation R | Read the same journey evidence |
| QA lead | Owns the harness configuration, the fixtures, the report shape and the pass or fail gate |
| Integration lead | Owns the harness code, the stub set and the swap from a fake to the real service |
| The owning services' identities | rwb-comms, rwb-case, rwb-source-data, rwb-access and rwb-decision make every state change the harness asserts; rwb-integration and rwb-comms run the 16:00 window |
| No approval level from the delegation of authority applies | The harness takes no business decision; notice approval is RWB-P7-E2014-APP |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-LEG-015 | notice | id | Read |
| DF-LEG-016 | notice | case_id | Read |
| DF-LEG-018 | notice | notice_type | Read |
| DF-LEG-019 | notice | sent_date | Read |
| DF-LEG-020 | notice | barcode | Read |
| DF-LEG-021 | notice | callback_date | Read |
| DF-LEG-022 | notice | delivery_status | Read |
| Standard column | notice | state | Read |
| DF-LEG-032 | notice | hold_reason | Read |
| DF-CAS-020 | recovery_case | legal_hold | Read |
| DF-CAS-038 | deviation | deviation_code | Read |
| DF-CAS-043 | deviation | contact_stop | Read |
| DF-CAS-044 | deviation | cleared_at | Read |
| DF-ACE-075 | v_ace_contact | contact_type | Read through the rwb-source-data contract |
| DF-EXT-015 | contact_point_ext | consent_given | Read through the rwb-source-data contact point and consent operation named in RWB-P1-E2021-APP |
| DF-INT-005 | interaction | channel | Read, through the rwb-source-data contract |
| DF-INT-011 | interaction | summary | Read, through the rwb-source-data contract |
| DF-INT-012 | interaction | conduct_check | Read, through the rwb-source-data contract |
| DF-WRK-030 | timer | timer_type | Read, through the rwb-case contract |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Read, through the rwb-decision contract |

Field IDs are those in the Logical Data Model and Data Dictionary. The harness owns no table and writes no row directly: it reads and writes through the API of the owning service only (DP-01, DP-18). The seeding set and the environment are not specified in the source documents (GAP-0404; ASM-0579).

### 12. Contract

#### 12.1 REST operations provided

None. The harness is a test runner and provides no REST operation.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| POST | `/api/recovery/comms/v1/cases/{caseId}/notices` | P6 rwb-comms | Request the journey notice and read back its state (AC1, AC4, AC5) |
| GET | `/api/recovery/comms/v1/notices/{noticeId}` | P6 rwb-comms | Read the notice, its barcode, its sent date, its call-back date and its delivery status (AC1, AC2) |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | Case status and legal hold before and after the run (AC1, AC4) |
| GET | `/api/recovery/case/v1/cases/{caseId}/timers` | P3 rwb-case | The NOTICE_PERIOD timer and its start date (AC2) |
| GET | `/api/recovery/source-data/v1/cases/{caseId}/interactions` | P1 rwb-source-data | The ledger entries (`eventCode`, `conductCheck`, `deliveryStatus`, `externalRef`, `idempotencyKey`, `caseSeq`, `summary`); `{caseId}` is the case UUID; 404 MSG-P4-003 for an unknown case (AC1, AC2, AC4, AC5, AC13) |
| GET | `/api/recovery/source-data/v1/data-products/DP02/records` | P1 rwb-source-data | The postal contact point and its consent as `fields` entries (`contactKey`, `contactType`, `consentStatus`), `?caseId=` the case UUID (AC5) |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | Role, scope and authority check for each call, including the refusal path (AC4) |
| GET | `/api/recovery/decision/v1/decision-log` | P7 rwb-decision | The decision entry for a held notice and the rule that produced it (AC4) |

The contact point and consent read is the DP02 record read of RWB-P1-E2021-APP; it carries no address. The harness appends nothing to the ledger: rwb-comms is the only writer-caller of the letter and proof entries, over `POST /api/recovery/source-data/v1/cases/{caseId}/interactions`. Every operation is one hop on the owner's base `/api/recovery/<short>/v1` with a 2 s budget and a circuit breaker per downstream (DP-11, DP-13); where a screen would compose them, the harness calls the gateway-bff composite route (DP-19). No operation is invented in this story.

#### 12.3 Events published

None. The harness publishes no Kafka event; it consumes the owner's events and writes its report to the wave record.

#### 12.4 Events consumed

| Event | Topic | Producer | Use |
|---|---|---|---|
| `rwb.comms.NoticeDispatched.v1` (EV-14) | `rwb.comms.events.v1` | P6 rwb-comms | Assert the dispatch fact for AC1 |
| `rwb.comms.NoticeDelivered.v1` (EV-15) | `rwb.comms.events.v1` | P6 rwb-comms | Assert the delivery fact and the status DELIVERED for AC2 |

Both events carry IDs and business facts only, keyed by caseId, and the harness asserts that no personal data is present (DP-09).

#### 12.5 Workflows and activities

None added. The harness exercises the existing JOB-10 WIN notices run, a Temporal Schedule in rwb-comms that opens the Airflow file window at 16:00, and the JOB-11 Outbox sender run, the outbox relay in every service, and asserts their effects through the services' contracts and the owner's topic (DP-10). No workflow, activity or Schedule is created, changed or owned by this story.

#### 12.6 Schedules

None added. JOB-10 WIN notices at 16:00, the Schedule in rwb-comms with the Airflow file window, is exercised on the business date under test only, and no cron, overlap policy or catch-up window is set by this story (DP-10).

#### 12.7 Tables owned

None. The harness owns no schema and no table (DP-01); it reads and writes through the owning services' contracts, and the ledger is rwb-source-data's (DP-18).

#### 12.8 Contract fakes

| Fake | Contract | Use in the run |
|---|---|---|
| WireMock stub for rwb-comms | `POST /cases/{caseId}/notices`, `GET /notices/{noticeId}`, `rwb.comms.events.v1` | Day-1 run of AC1, AC2, AC4 and AC5 before RWB-P6-E2021-APP is live |
| WireMock stub for rwb-case | `GET /cases/{caseId}`, `GET /cases/{caseId}/timers` | Day-1 assertions on case status, legal hold and the NOTICE_PERIOD timer |
| WireMock stub for rwb-source-data | `GET` and `POST /cases/{caseId}/interactions` (InteractionRequest 5.1.0: 201, 200 on a repeated business key), `GET /data-products/DP02/records`, `GET /proof-of-delivery?businessDate=` | Day-1 assertions on the ledger entry and on the consent status |
| WireMock stub for rwb-access | `POST /authorise` | Day-1 authorisation and refusal path |
| WireMock stub for rwb-decision | `GET /decision-log` | Day-1 assertion of the R-LIT-05 and R-LIT-07 entries |
| WIN file-drop fixture | INT-14 WIN letters and the WIN acknowledgment | The 16:00 window drop and the acknowledgment that sets Sent |
| Proof-file fixture | INT-15 proof file | The delivery and undelivered rows keyed by barcode |

Each stub is generated from the published contract and its version is pinned in the run report, so a contract change shows up as a run failure and not as a silent pass. The fixture contents, the result codes of the proof file, the 16:00 window control, the harness environment, the data seeding set and the evidence format and retention are not specified in the source documents (GAP-0404; ASM-0579).

#### 12.9 Call-type summary

| Call type | In this story |
|---|---|
| REST | 0 provided, 8 consumed, one hop each on `/api/recovery/<short>/v1` with a 2 s budget (DP-11, DP-13), composed through gateway-bff where a screen would (DP-19) |
| Kafka | None published; `rwb.comms.NoticeDispatched.v1` and `rwb.comms.NoticeDelivered.v1` consumed from `rwb.comms.events.v1` (EV-14, EV-15) |
| Temporal | None added; JOB-10 WIN notices at 16:00 and JOB-11 Outbox sender exercised (DP-10) |
| File | INT-14 WIN letters drop with the WIN acknowledgment, and the INT-15 proof file drop, both as fixtures |

### 13. Solution plan

**Package.** Folder `itg/recovery`, package `th.co.scb.ace.workbench.recovery.itg`, test scope only; not part of any deployed service.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-18 | Interaction ledger | Ledger owned by rwb-source-data (default ruling) | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The platform H dependencies in the table above (RWB-PLT-E1027-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON and RWB-PLT-N001-CON) are delivered by the platform waves and are not repeated in the metadata H field of this story, which stays empty. The blocking dependencies are the six I stories: RWB-P7-E2014-APP, RWB-P6-E2021-APP, RWB-P1-E2021-APP, RWB-P4-E2021-APP, RWB-P3-E2021-APP and RWB-P7-E2021-APP. Each one replaces its fake; until it is live the run uses the stub, and a stub pass is reported as a stub pass.

**Harness components**

| Component | Type | Responsibility |
|---|---|---|
| JourneyRunner | Job | Runs the four owned criteria in order for a business date and holds the run lock |
| StubSet | Fake | The five WireMock stubs generated from the published contracts, with the contract version pinned |
| WinFileFixture | Fixture | The INT-14 WIN letters drop and the WIN acknowledgment, keyed by barcode and business date |
| ProofFileFixture | Fixture | The INT-15 proof rows, keyed by barcode, with result DELIVERED, REFUSED or UNDELIVERABLE |
| WindowControl | Service | Moves the JOB-10 16:00 window in the environment under test and triggers the Airflow file window |
| EventProbe | Service | Consumes `rwb.comms.events.v1` and asserts EV-14 and EV-15 for the case |
| EvidenceReport | Service | Writes the per-run report keyed by story and business date, and holds the pass or fail gate |

**Environment and test data.** SIT, against the fakes from Day 1 and the real services as the I stories land, on the case `RC-2026-000321` and the notice `N-0101` of the legacy criteria plus the deviation, contact point and consent rows those criteria need. The environment, the seeding set and the evidence retention are not specified in the source documents (GAP-0404; ASM-0579). Seeding uses only the owning services' published operations, never a schema write.

**Build steps**

1. Generate the five stubs from the published contracts and pin each contract version in the run report; fail the run on a version mismatch (X1, X9).
2. Build the two file fixtures and the window control, and prove the drop and the read-back for one business date (X2, X3).
3. Build the JourneyRunner for AC1: request the notice, hold the 16:00 window, drop the WIN fixture, read the acknowledgment, assert Sent with the barcode and the ledger entry with conduct check PASSED.
4. Add the EventProbe for EV-14 and EV-15 and assert the key and the absence of personal data (X4).
5. Add AC2: drop the INT-15 DELIVERED row, assert Delivered with the call-back date, the ledger entry and the NOTICE_PERIOD timer started on the delivery date and not on the sent date (X7).
6. Add AC4: seed the open X1 deviation with the contact stop, assert Held with CONTACT_STOP_X1, BLOCKED on the ledger, one R-LIT-05 decision entry, the MSG-P6-001 route and the notice absent from the WIN fixture (X5).
7. Add AC5: seed the WITHDRAWN postal consent on the statutory type, assert the notice in the WIN file and PASSED with the statutory summary (X6).
8. Add the access path through `POST /api/recovery/access/v1/authorise`, including the refusal for a caller outside the case scope (X8).
9. Add the EvidenceReport and the gate, then swap one stub for its real service as each I story lands and rerun the four criteria.

**Feature switch.** `rwb.comms.win-dispatch-loop`, the legacy flag of this behaviour, is on for the environment under test so the dispatch loop runs as the release will.

**Done when.** The tests of section 16 pass for the four owned criteria; the four criteria pass against the five fakes on Day 1 and again, one at a time, against each real service as its I story lands; and the wave entry check holds a run report keyed by story and business date with the contract and fixture versions named.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P6-008 | A notice is refused, undeliverable or has no proof in the window | {notice} for case {case} was not served: {reason}. The case is in your queue to choose another service method. |
| MSG-P6-001 | A contact stop blocks the letter | Contact with this customer is stopped for {reason}. |
| MSG-P3-004 | A legal hold or deviation blocks the letter | This case is on hold for {deviation}. The prescription date is still {date}. |
| MSG-P6-003 | The template was withdrawn before dispatch | The {template} template has been withdrawn. The notice is on hold until Legal approves a new version. |
| MSG-P7-003 | The decision log write failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-003 | The notice is outside the caller's scope | This case is not in your scope. |
| MSG-GEN-001 | Notice type missing | Enter {field}. |
| MSG-P6-004 | WIN acknowledged the notice | {notice} was sent for registered mail on {date}. |

The harness produces none of these messages itself; it asserts the message the owning service returns and names the message ID in the report, so a run failure points at a service and a message and not only at a date.

### 15. Screens and states

SCR-18 Notice approval (built in RWB-P7-E2014-APP) shows the states this journey sets:

| State | What the user sees and does |
|---|---|
| Sent | Sent date and barcode; the litigation officer waits for proof |
| Delivered | Callback date and the notice period end date from the timer |
| Unserved | The result and MSG-P6-008; the litigation officer chooses an alternate service method on the case (R-LIT-10, Epic 5) |
| Empty | Not specified in the source documents (CG-ALL-695) |
| Loading | Not specified in the source documents (CG-ALL-695) |
| Error | Not specified in the source documents (CG-ALL-695) |
| No access | Not specified in the source documents (CG-ALL-695) |

SCR-04 Case timeline shows each ledger entry with its conduct check result.

SCR-04 states: Empty: Not specified in the source documents (CG-ALL-694). Loading: as in Screen Specifications v1, section SCR-04. Error: Not specified in the source documents (CG-ALL-694). No access: Not specified in the source documents (CG-ALL-694).

The harness renders no screen. It reads these states through the rwb-comms, rwb-case and rwb-source-data contracts, and it asserts the same three SCR-18 states (not the Empty, Loading, Error and No access rows) and the SCR-04 timeline entry that a litigation officer would see, so a passed run means the screen has the right data behind it. What the wave entry check looks at instead is the evidence report, whose format and retention are not specified in the source documents (GAP-0404; ASM-0579).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-021-01-ITG | AC1, BR1 | Integration | N-0101 Approved; acknowledgment RR223344556TH |
| TC-E2-021-02-ITG | AC2, BR5 | Integration | INT-15 DELIVERED, call-back 18122026 |
| TC-E2-021-03-ITG | AC3, BR6 (run by Not specified in the source documents (CG-ALL-692)) | Integration | INT-15 UNDELIVERABLE |
| TC-E2-021-04-ITG | AC4, BR2 | Integration | Open X1 with contact stop |
| TC-E2-021-05-ITG | AC5, BR4, BR10 | Integration | Postal consent WITHDRAWN, DEMAND notice |
| TC-E2-021-06-ITG | AC6, BR7 (run by Not specified in the source documents (CG-ALL-692)) | Integration | N-0102 sent 2026-12-15 and N-0103 sent 2026-12-16; JOB-10 on 2026-12-22 |
| TC-E2-021-07-ITG | AC7, BR3 (run by Not specified in the source documents (CG-ALL-692)) | Integration | Legal hold true |
| TC-E2-021-08-ITG | AC8, BR8 (run by Not specified in the source documents (CG-ALL-692)) | Integration | DEMAND-SSME TH v1 withdrawn 2026-12-13 |
| TC-E2-021-09-ITG | AC9, BR9 (run by Not specified in the source documents (CG-ALL-692)) | Integration | Open X2 with stop; decision log stubbed unavailable |
| TC-E2-021-10-ITG | AC10 (run by Not specified in the source documents (CG-ALL-692)) | Integration | POST repeated with one Idempotency-Key |
| TC-E2-021-11-ITG | AC11 (run by Not specified in the source documents (CG-ALL-692)) | Integration | N-0200 outside scope |
| TC-E2-021-12-ITG | AC12 (run by Not specified in the source documents (CG-ALL-692)) | Integration | POST with no notice type |
| TC-E2-021-13-ITG | Access | Component | RW-CASEOWN sends POST /cases/{caseId}/notices; refused with MSG-P4-002 |

The ledger assertions added to AC1, AC2, AC4, AC5 and AC13 in version 3 (TC-E2-021-01, 02, 04, 05-ITG and the AC13 case): Test Cases v9: TC-E2-021-01-ITG, TC-E2-021-02-ITG, TC-E2-021-04-ITG, TC-E2-021-05-ITG, TC-E2-021-15-ITG.
| TC-E2-021-14-ITG | Principle 5 | NFR | Decision log write forced to fail on 10 unserved results; no notice changes |
| TC-E2-021-15-ITG | AC13 | Integration | INT-15 DELIVERED for N-0101 received a second time, call-back 18122026 |
| TC-E2-021-16-ITG | AC14 | Integration | Consumed call forced to fail or not answer; notice N-0101 Sent |
| TC-E2-021-17-ITG | AC15 | Integration | Notice N-0101 Delivered; status change to Approved requested |

The integration cases above are the ITG copies of the legacy cases of the same number and carry the legacy data unchanged; the component and NFR copies keep the legacy levels. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the proof window, the statutory notice types, the eligible states, the fixture contents and the result code mappings are data.
- No personal data in logs, fixtures, reports, tests or prompts: the ledger summaries carry codes and barcodes, and the events are asserted for the absence of personal data.
- No read of another service's tables: every read and every seed goes through the owning contract (DP-01), and the ledger is rwb-source-data's (DP-18).
- One hop and a 2 s budget per call, with a circuit breaker per downstream, so the harness fails where a screen would (DP-11).
- A stub pass is never reported as a real-service pass: the report names the contract version and whether the hop was a stub or the owner.
- The harness never runs against UAT or production, and it never sets a notice, case, timer or decision state by hand.
- A failing criterion is fixed in the service that owns it or reported as a gap; it is never waived in the script.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-OCC-003 | Letters dispatched for print and post, proof of delivery returns | Business Requirements Epic 2, sections 3.6 and 4 | FEAT-OCC-02 | 13 Manage documents and correspondence | R-LIT-07, R-LIT-08, R-LIT-09 | TC-E2-021-01-ITG, TC-E2-021-02-ITG, TC-E2-021-03-ITG, TC-E2-021-06-ITG, TC-E2-021-10-ITG, TC-E2-021-11-ITG, TC-E2-021-12-ITG |
| REQ-OCC-005 | Every outbound contact carries a conduct check result | Business Requirements Epic 2, sections 3.6 and 4 | FEAT-OCC-05, FEAT-OCC-06 | 16 Manage risk, control and compliance | R-LIT-05, R-UNI-20, R-LIT-04, R-UNI-39 | TC-E2-021-01-ITG, TC-E2-021-04-ITG, TC-E2-021-05-ITG, TC-E2-021-07-ITG, TC-E2-021-08-ITG, TC-E2-021-09-ITG, TC-E2-021-14-ITG |
| REQ-OCC-006 | Withdrawn consent stops the channel; statutory notices continue | Business Requirements Epic 2, sections 3.6 and 4 | FEAT-OCC-05 | 16 Manage risk, control and compliance | R-UNI-10 | TC-E2-021-01-ITG, TC-E2-021-05-ITG, TC-E2-021-07-ITG |
| REQ-ILG-010 | Dispatch results, including proof of delivery, written to the ledger | Business Requirements Epic 2, sections 3.6 and 4 | FEAT-ILG-07 | 06 to 10 Recovery case processes | R-LIT-07, R-LIT-09 | TC-E2-021-01-ITG, TC-E2-021-02-ITG, TC-E2-021-03-ITG, TC-E2-021-13-ITG |

### 19. Out of scope

- Alternate service methods and substituted service (R-LIT-10, R-LIT-11, Epic 5).
- SMS and LINE dispatch (RWB-ITG-E2022-ITG, from the legacy RWB-E2-022).
- The breach path for a contact sent while a block is on (FEAT-DVF-10, Epic 7).
- Notice approval (RWB-P7-E2014-APP).
- Any production screen, endpoint, event, workflow, Schedule or table: this story builds a test harness and its evidence only, and the behaviour it proves is built by the six I stories.
- The rwb-comms dispatch behaviour itself and the rwb-integration file runs, which are the service stories of P6, P2 and P3 (DP-01, DP-10).
- The fixture contents, the WIN window control, the harness environment and the evidence format and retention: carried as a gap and an assumption, not decided here.

### 20. Remaining delivery steps

- Size the story at refinement (owner: squad).
- Publish the rwb-source-data 5.1.0 fake with the ledger, DP02 and proof-of-delivery answers (owner: rwb-source-data contract owner).
- Add the proof-of-delivery read to rwb-source-data.yaml or confirm where its contract is published (owner: solution architect).
- Provide ACE test rows for `v_ace_pod` in SIT and seed the case UUID (owner: bank platform team with the integration and QA team).
- Pending: harness environment, fixtures, window control and evidence format, owner integration and QA team, tracked as GAP-0404.
- Have the "Case record C on rwb-source-data" service row of rwb-comms in place before the ledger assertions run against the real services (owner: rwb-access owner; RD-P1-064 rule 2).
