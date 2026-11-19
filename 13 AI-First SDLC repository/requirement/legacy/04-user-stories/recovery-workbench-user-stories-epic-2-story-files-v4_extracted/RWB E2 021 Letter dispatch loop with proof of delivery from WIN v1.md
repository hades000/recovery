<!-- source: 04 User stories/Recovery Workbench User Stories Epic 2 Story Files v4.zip!RWB E2 021 Letter dispatch loop with proof of delivery from WIN v1.md -->
<!-- converted: 2026-11-04 from Markdown (extracted) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 2 Story Files v4.zip!RWB E2 021 Letter dispatch loop with proof of delivery from WIN v1.md`  
> **Converted from:** Markdown (extracted)

# RWB-E2-021 Letter dispatch loop with proof of delivery from WIN

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E2-021 |
| Epic | E2, release 31 December 2026 |
| Module | P6 Communications |
| Feature | FEAT-OCC-01 Generate a letter from an approved template; FEAT-OCC-02 Dispatch a letter through WIN and capture proof of delivery; FEAT-OCC-05 Run the conduct check before every outbound contact; FEAT-OCC-06 Block an outbound contact when a contact stop is in force; FEAT-ILG-07 Bring dispatch outcomes into the ledger |
| Requirement IDs | REQ-OCC-003, REQ-OCC-005, REQ-OCC-006, REQ-ILG-010 |
| BRD section | Business Requirements Epic 2, sections 3.6 and 4 |
| L3 process | 13 Manage documents and correspondence; 16 Manage risk, control and compliance; 06 to 10 Recovery case processes |
| Decision | D7.1 |
| Priority | Must |
| Depends on | RWB-E1-052, RWB-E1-055, RWB-E2-014 |
| Status | Ready for build |

## 1. Story

As a **litigation officer (RW-LITOFF)**, I want **every approved letter sent to WIN after the conduct check, with the dispatch and the proof of delivery returned to the case and the notice period started from delivery**, so that **the notice period is counted from proof of delivery and not from printing**.

## 2. Business rationale

A notice period counted from the print date can be challenged, and a letter sent to a customer under a contact stop is a conduct breach. This story adds the conduct check before every letter, handles refused, undeliverable and unproven letters, writes every outcome to the interaction ledger and gives the litigation officer an endpoint to request and read a notice. It serves REQ-OCC-003, REQ-OCC-005, REQ-OCC-006 and REQ-ILG-010, controls CTL-15 and CTL-16, and the FSD P6 measure "notices with proof of delivery, 100 percent".

## 3. Preconditions

- RWB-E1-052 and RWB-E1-055 are done: generation, the WIN file, the acknowledgment and the INT-15 load run.
- RWB-E2-014 is done: notices are approved on SCR-18 and reach state Approved.
- The dispatch-eligible notice states are set to Approved (`rwb.comms.dispatch.eligible-states` = APPROVED).
- Open deviations and their contact stop flags are readable through the S8 interface (RWB-E2-015).
- The proof window is loaded as reference data: 7 days from sending (R-LIT-08).
- The requester holds RW-LITOFF or RW-ENFORCE (Litigation C) for POST and any role with Litigation R for GET.

## 4. Flow

1. Litigation officer: requests a notice through POST /cases/{caseId}/notices; the system calls NoticeApi.generate (RWB-E1-052) and returns the notice in state Generated.
2. Approver: approves the notice on SCR-18 (RWB-E2-014); state Approved.
3. JOB-10, daily 16:00: for each Approved notice runs the conduct check: legal hold on the case, open deviation with contact stop, current template still Approved, statutory status of the notice type.
4. System: a notice that fails the check is held, the reason is written to the decision log and to the ledger with conduct check Blocked, and the case goes to the deviation owner (R-LIT-05) or the hold owner; it is not written to the file.
5. System: a notice that passes is written to the INT-14 file with conduct check Passed; the WIN acknowledgment sets Sent with the barcode (RWB-E1-055) and the ledger entry carries the barcode.
6. JOB-09: loads the INT-15 file; a Delivered record sets Delivered and publishes NoticeDelivered; P3 starts the notice period from the delivery date (R-LIT-07).
7. System: a Refused or Undeliverable record sets Unserved, writes the decision log entry under R-LIT-09, writes the ledger entry and raises DELIVERY_FAILED to P3, which transfers the case to the owner's queue with reason NOTICE_UNSERVED.
8. JOB-10, at the start of each run: a Sent notice with no proof 7 days after its sent date becomes Unserved under R-LIT-08; the notice period does not start.
9. Litigation officer: reads the notice, its dispatch and its proof through GET /notices/{noticeId} and on SCR-18.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | WIN returns Refused or Undeliverable | Notice Unserved; case to the owner's queue with the reason | MSG-P6-008 | AC3 |
| X2 | An open X1 or X2 deviation has the contact stop on | Notice held; case to the deviation owner | MSG-P6-001 | AC4 |
| X3 | Consent for the postal channel is withdrawn | A statutory notice is still sent | None | AC5 |
| X4 | No proof 7 days after sending | Notice Unserved; notice period not started | MSG-P6-008 | AC6 |
| X5 | A legal hold is on the case | Notice held; nothing sent | MSG-P3-004 | AC7 |
| X6 | The template of an approved notice is withdrawn before dispatch | Notice held | MSG-P6-003 | AC8 |
| X7 | The decision log write fails for a held or unserved notice | Notice unchanged; retried on the next run; incident raised | MSG-P7-003 | AC9 |
| X8 | POST repeated with the same Idempotency-Key | The first notice is returned | None | AC10 |
| X9 | GET for a notice outside the caller's scope | Refused | MSG-P4-003 | AC11 |
| X10 | POST with no notice type | Refused | MSG-GEN-001 | AC12 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds on the v1 dispatch and generation; approval (RWB-E2-014) is a prior story |
| Negotiable | The proof window, statutory notice types and eligible states are data |
| Valuable | Every letter carries a conduct result and the notice period starts only from proof |
| Estimable | Two endpoints, one check service, two result handlers, one daily window check |
| Small | Fits in two weeks with its tests |
| Testable | Each criterion runs with synthetic notices and WIN files |

## 7. Acceptance criteria

```gherkin
Feature: Letter dispatch loop with proof of delivery from WIN

  Background:
    Given the dispatch-eligible notice states are "APPROVED"
    Given the proof window is 7 days
    Given notice "N-0101" for case "RC-2026-000321" is "Approved" with notice type "DEMAND" and template "DEMAND-SSME" "TH" version 1 Approved
    Given case "RC-2026-000321" has no legal hold and no open deviation

  Scenario: AC1 Dispatch
    Given JOB-10 runs at 16:00 on 2026-12-14
    When the conduct check passes and WIN acknowledges contract "CT-88001" with barcode "RR223344556TH" and sent date 15122026
    Then notice "N-0101" is "Sent" with barcode "RR223344556TH" and sent date 2026-12-15
    Then the ledger entry for the letter has conduct check "PASSED" and summary naming barcode "RR223344556TH"
    Then GET /notices/N-0101 returns sentDate 2026-12-15 and barcode "RR223344556TH"

  Scenario: AC2 Proof back
    Given notice "N-0101" is "Sent" on 2026-12-15
    When the INT-15 file of 2026-12-21 returns barcode "RR223344556TH" with result "DELIVERED" and call-back date 18122026
    Then notice "N-0101" is "Delivered" with callback date 2026-12-18
    Then the ledger has an entry "Delivered" for case "RC-2026-000321" on 2026-12-18
    Then case "RC-2026-000321" has a running "NOTICE_PERIOD" timer started on 2026-12-18

  Scenario: AC3 Undelivered
    Given notice "N-0101" is "Sent" on 2026-12-15
    When the INT-15 file of 2026-12-21 returns barcode "RR223344556TH" with result "UNDELIVERABLE"
    Then notice "N-0101" is "Unserved" with delivery status "UNDELIVERABLE"
    Then one decision log entry exists with decision code "D7.1" and rule "R-LIT-09"
    Then the system transfers case "RC-2026-000321" to its owner's queue with reason "NOTICE_UNSERVED"
    Then the owner sees MSG-P6-008 naming "DEMAND" and "UNDELIVERABLE"
    Then the system starts no notice period timer

  Scenario: AC4 Contact stop blocks the letter
    Given case "RC-2026-000321" has an open deviation "X1" with contact stop on
    When JOB-10 runs on 2026-12-14
    Then the system does not writ notice "N-0101" to the WIN file
    Then notice "N-0101" is "Held" with hold reason "CONTACT_STOP_X1"
    Then the ledger entry has conduct check "BLOCKED"
    Then one decision log entry exists with rule "R-LIT-05"
    Then the system routes the case to the complaint officer with MSG-P6-001 naming "X1 Dispute or complaint"

  Scenario: AC5 Consent withdrawn does not stop a statutory notice
    Given the borrower's postal address contact point has consent status "WITHDRAWN"
    Given notice type "DEMAND" is a statutory notice
    When JOB-10 runs on 2026-12-14
    Then the system writes notice "N-0101" to the WIN file
    Then the ledger entry has conduct check "PASSED" and summary "Statutory notice, consent withdrawn"

  Scenario: AC6 Proof window expires
    Given notice "N-0102" for case "RC-2026-000654" is "Sent" with sent date 2026-12-15 and no proof returned
    Given notice "N-0103" for case "RC-2026-000655" is "Sent" with sent date 2026-12-16 and no proof returned
    When JOB-10 runs on 2026-12-22
    Then notice "N-0102" is "Unserved" with delivery status "PENDING"
    Then one decision log entry exists for "N-0102" with rule "R-LIT-08"
    Then the system starts no notice period timer for case "RC-2026-000654"
    Then notice "N-0103" stays "Sent"

  Scenario: AC7 Legal hold stops dispatch
    Given case "RC-2026-000321" has legal hold true
    When JOB-10 runs on 2026-12-14
    Then notice "N-0101" is "Held" with hold reason "LEGAL_HOLD" and is not in the WIN file
    Then the case record shows MSG-P3-004

  Scenario: AC8 Template withdrawn after approval
    Given template "DEMAND-SSME" "TH" version 1 was withdrawn on 2026-12-13
    When JOB-10 runs on 2026-12-14
    Then notice "N-0101" is "Held" with hold reason "TEMPLATE_WITHDRAWN" and is not in the WIN file
    Then the system raises a task to the litigation officer team with MSG-P6-003

  Scenario: AC9 Decision log write fails on a held notice
    Given case "RC-2026-000321" has an open deviation "X2" with contact stop on
    Given the decision log store is unavailable
    When JOB-10 runs on 2026-12-14
    Then notice "N-0101" stays "Approved" and is not in the WIN file
    Then the job record shows MSG-P7-003 for "N-0101"
    Then the system raises an incident under rule R-UNI-39

  Scenario: AC10 Repeated request
    Given "LIT-0101" sent POST /cases/RC-2026-000321/notices with notice type "RECALL" and Idempotency-Key "a1b2c3d4-0001"
    When the same request is sent again with Idempotency-Key "a1b2c3d4-0001"
    Then the response is the first notice with status 201
    Then case "RC-2026-000321" has one RECALL notice

  Scenario: AC11 Notice outside the caller's scope
    Given notice "N-0200" belongs to a case outside the scope of "LIT-0101"
    When "LIT-0101" sends GET /notices/N-0200
    Then the response is status 404 with MSG-P4-003

  Scenario: AC12 Notice type missing
    Given "LIT-0101" holds RW-LITOFF and case "RC-2026-000321" is in scope
    When "LIT-0101" sends POST /cases/RC-2026-000321/notices with no notice type
    Then the response is status 422 with MSG-GEN-001 naming "notice type"
```

## 8. Business rules

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

## 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| In progress | Offer or notice sent to the customer | WIN acknowledges the notice | Waiting customer |
| In progress | Deviation flagged or legal hold placed | Contact stop or legal hold found at the check | On hold (set by P3 under R-DEV-01 or R-UNI-20; this story holds the notice only) |

The case status moves are made by P3 on the events this story raises. This story changes the notice state: Approved to Sent, Approved to Held, Sent to Delivered, Sent to Unserved (DELIVERY_FAILED, PROOF_WINDOW_EXPIRED).

## 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-LITOFF, litigation officer | Requests a notice (Litigation C); reads it (Litigation R) |
| RW-ENFORCE, enforcement owner | Requests and reads a notice (Litigation CRU) |
| RW-CASEOWN, RW-LEGAL, RW-HEADLIT and other roles with Litigation R | Read the notice, its dispatch and proof |
| RW-CONDUCT, Conduct and QA officer | Reads blocked contacts on the ledger (Case record R) |
| SY-DATALOAD, data load from COLLINS | Runs JOB-10 and the INT-15 step |
| SY-CASEWF, case workflow module | Applies DELIVERY_FAILED and the transfer; starts the timer |
| SY-DECLOG, decision log writer | Writes the D7.1 entries |

No approval level from the delegation of authority applies in this story; notice approval is RWB-E2-014.

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-LEG-015 | notice | id | Read |
| DF-LEG-016 | notice | case_id | Read |
| DF-LEG-018 | notice | notice_type | Read |
| DF-LEG-019 | notice | sent_date | Read |
| DF-LEG-020 | notice | barcode | Read |
| DF-LEG-021 | notice | callback_date | Write |
| DF-LEG-022 | notice | delivery_status | Write |
| Standard column | notice | state | Write |
| DF-LEG-032 | notice | hold_reason | Write |
| DF-CAS-020 | recovery_case | legal_hold | Read |
| DF-CAS-038 | deviation | deviation_code | Read |
| DF-CAS-043 | deviation | contact_stop | Read |
| DF-CAS-044 | deviation | cleared_at | Read |
| DF-PTY-015 | contact_point | channel | Read |
| DF-PTY-018 | contact_point | consent_status | Read |
| DF-INT-005 | interaction | channel | Write, through the ledger writer |
| DF-INT-011 | interaction | summary | Write, through the ledger writer |
| DF-INT-012 | interaction | conduct_check | Write, through the ledger writer |
| DF-WRK-030 | timer | timer_type | Read |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Write |

Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

**POST /api/recovery/v1/cases/{caseId}/notices** (api.yaml, x-module P6)

| Item | Value |
|---|---|
| Request | NoticeRequest: noticeType (required), partyId (defaults to the borrower), language (defaults to TH) |
| Response | 201 Notice: id, caseId, documentId, noticeType, sentDate, barcode, callbackDate, deliveryStatus, sentType |
| Errors | 401 no session; 403 role lacks Litigation C (MSG-P4-002); 404 case not found or out of scope (MSG-P4-003); 409 template not approved (MSG-P6-005) or a notice of this type already in progress (MSG-P3-005); 422 field fails (MSG-GEN-001); 503 decision not recorded (MSG-P7-003) |
| Authorization | Litigation, right C, scope applied |
| Idempotency | Idempotency-Key header, kept 24 hours |

**GET /api/recovery/v1/notices/{noticeId}** (api.yaml, x-module P6)

| Item | Value |
|---|---|
| Response | 200 Notice |
| Errors | 401; 403 (MSG-P4-002); 404 not found or out of scope (MSG-P4-003); 503 |
| Authorization | Litigation, right R, scope applied |
| Idempotency | Not applicable |

**Jobs.** JOB-10 WIN outbound notices (daily 16:00) gets two steps: the proof window step first, then the conduct check before each file record. JOB-09 File loads adds the Refused and Undeliverable results to the INT-15 step. Idempotency for each: notice ID and business date; a rerun from SCR-44 skips notices already Unserved, Held or in a file of that date.

**Events published.** NoticeDispatched (EV-14), NoticeDelivered (EV-15) with status DELIVERED, REFUSED or UNDELIVERABLE.

**Published interfaces called**

```java
List<ContactStopView> DeviationApi.activeContactStops(UUID caseId);            // S8
CaseSummary CaseWorkflowApi.getCaseSummary(UUID caseId);                        // P3, carries legalHold
void CaseWorkflowApi.applyEvent(UUID caseId, String eventCode, Map<String,String> facts); // P3, DELIVERY_FAILED, PROOF_WINDOW_EXPIRED, CONTACT_STOP_APPLIED
UUID InteractionLedgerApi.record(InteractionRecord record);                     // ledger writer
DecisionLogRef DecisionLogApi.write(DecisionLogRequest request) throws DecisionLogWriteException; // P7
```

## 13. Solution plan

- Package: folders `recovery/comms/dispatch` and `recovery/comms/notices`, Java packages `recovery.comms.dispatch` and `recovery.comms.notices`.

| Component | Type | Responsibility |
|---|---|---|
| NoticeController | Controller | POST /cases/{caseId}/notices and GET /notices/{noticeId} |
| ConductCheckService | Service | Legal hold, contact stop, template state and statutory rule for one outbound contact; returns Passed or Blocked with the reason and rule ID |
| WinNoticeFileJob | Job | From RWB-E1-055; calls ConductCheckService before writing each record |
| DeliveryResultHandler | Service | Applies Delivered, Refused and Undeliverable from INT-15; writes the decision log, ledger and P3 event |
| ProofWindowStep | Job | First step of JOB-10: Sent notices past the proof window become Unserved under R-LIT-08 |
| StatutoryNoticeTypes | Rule table | Reads the statutory notice type list from reference data |

- Database: table notice (columns from RWB-E1-052 and RWB-E1-055). Index ix_notice_state_sent supports the window check. No new table.
- Configuration and reference data: `rwb.comms.dispatch.eligible-states` = APPROVED; proof window 7 days as a timer row (R-LIT-08, business lead, DL22); statutory notice types DEMAND, RECALL, STATUTORY_SALE_NOTICE, GUARANTOR_NOTICE, assumed, owner Legal counsel; INT-15 result codes mapped to LOV-DELIVERY in the code map (data steward).
- Build steps:
  1. Add the INT-15 result column to the file reader and the code map to LOV-DELIVERY; test the mapping.
  2. Build ConductCheckService with the four checks in order: legal hold, contact stop, template, consent with the statutory rule; unit test each branch.
  3. Wire ConductCheckService into WinNoticeFileJob with the decision log and ledger writes; test AC1, AC4, AC5, AC7, AC8, AC9.
  4. Build DeliveryResultHandler for the three results; test AC2 and AC3.
  5. Build ProofWindowStep in JOB-10; test AC6 with the 6-day and 7-day boundary.
  6. Build NoticeController on NoticeApi with Idempotency-Key and scope; test AC10, AC11, AC12.
- Feature flag: `rwb.comms.win-dispatch-loop`.
- Done when: the tests in section 16 pass, and REC-05 shows no break for the synthetic month of notices.

## 14. Validation and messages

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

## 15. Screens and states

SCR-18 Notice approval (built in RWB-E2-014) shows the states this story sets:

| State | What the user sees and does |
|---|---|
| Sent | Sent date and barcode; the litigation officer waits for proof |
| Delivered | Callback date and the notice period end date from the timer |
| Unserved | The result and MSG-P6-008; the litigation officer chooses an alternate service method on the case (R-LIT-10, Epic 5) |

SCR-04 Case timeline shows each ledger entry with its conduct check result.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-021-01 | AC1, BR1 | System | N-0101 Approved; acknowledgment RR223344556TH |
| TC-E2-021-02 | AC2, BR5 | System | INT-15 DELIVERED, call-back 18122026 |
| TC-E2-021-03 | AC3, BR6 | System | INT-15 UNDELIVERABLE |
| TC-E2-021-04 | AC4, BR2 | System | Open X1 with contact stop |
| TC-E2-021-05 | AC5, BR4, BR10 | System | Postal consent WITHDRAWN, DEMAND notice |
| TC-E2-021-06 | AC6, BR7 | System | N-0102 sent 2026-12-15 and N-0103 sent 2026-12-16; JOB-10 on 2026-12-22 |
| TC-E2-021-07 | AC7, BR3 | System | Legal hold true |
| TC-E2-021-08 | AC8, BR8 | System | DEMAND-SSME TH v1 withdrawn 2026-12-13 |
| TC-E2-021-09 | AC9, BR9 | System | Open X2 with stop; decision log stubbed unavailable |
| TC-E2-021-10 | AC10 | System | POST repeated with one Idempotency-Key |
| TC-E2-021-11 | AC11 | System | N-0200 outside scope |
| TC-E2-021-12 | AC12 | System | POST with no notice type |
| TC-E2-021-13 | Access | Access | RW-CASEOWN sends POST /cases/{caseId}/notices; refused with MSG-P4-002 |
| TC-E2-021-14 | Principle 5 | Resilience | Decision log write forced to fail on 10 unserved results; no notice changes |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: proof window, statutory notice types, eligible states and result code mappings are data.
- No personal data in logs, tests or prompts. Ledger summaries carry codes and barcodes, never names or addresses.
- No read of another module's tables. Deviations, case hold, contact points, timers and the transfer go through the owning interfaces.
- The conduct check runs inside the same transaction that selects the notice for the file, so a stop raised after the check reaches the next run.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-OCC-003 | Letters dispatched for print and post, proof of delivery returns | Business Requirements Epic 2, sections 3.6 and 4 | FEAT-OCC-02 | 13 Manage documents and correspondence | R-LIT-07, R-LIT-08, R-LIT-09 | TC-E2-021-01, TC-E2-021-02, TC-E2-021-03, TC-E2-021-06, TC-E2-021-10, TC-E2-021-11, TC-E2-021-12 |
| REQ-OCC-005 | Every outbound contact carries a conduct check result | Business Requirements Epic 2, sections 3.6 and 4 | FEAT-OCC-05, FEAT-OCC-06 | 16 Manage risk, control and compliance | R-LIT-05, R-UNI-20, R-LIT-04, R-UNI-39 | TC-E2-021-04, TC-E2-021-07, TC-E2-021-08, TC-E2-021-09, TC-E2-021-14 |
| REQ-OCC-006 | Withdrawn consent stops the channel; statutory notices continue | Business Requirements Epic 2, sections 3.6 and 4 | FEAT-OCC-05 | 16 Manage risk, control and compliance | R-UNI-10 | TC-E2-021-05 |
| REQ-ILG-010 | Dispatch results, including proof of delivery, written to the ledger | Business Requirements Epic 2, section 4 | FEAT-ILG-07 | 06 to 10 Recovery case processes | R-LIT-07, R-LIT-09 | TC-E2-021-01, TC-E2-021-02, TC-E2-021-03, TC-E2-021-13 |

## 19. Out of scope

- Alternate service methods and substituted service (R-LIT-10, R-LIT-11, Epic 5).
- SMS and LINE dispatch (RWB-E2-022).
- The breach path for a contact sent while a block is on (FEAT-DVF-10, Epic 7).
- Notice approval (RWB-E2-014).
