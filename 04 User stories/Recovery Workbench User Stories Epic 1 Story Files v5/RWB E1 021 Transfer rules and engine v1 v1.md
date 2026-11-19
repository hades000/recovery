# RWB-E1-021 Transfer rules and engine v1

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E1-021 |
| Epic | E1, release 30 November 2026 |
| Module | P3 Case and workflow |
| Feature | FEAT-CWC-10 Run the transfer rule table and engine |
| Requirement IDs | REQ-CWC-010, REQ-CWC-016 |
| BRD section | Business Requirements Epic 1, section 3.3; Business Requirements Program, section 5.3 |
| L3 process | All recovery processes |
| Decision | None |
| Priority | Must |
| Depends on | RWB-E1-028, RWB-E1-020, RWB-E1-027 |
| Status | Ready for build |

## 1. Story

As a **team manager (RW-TEAMMGR)**, I want **cases moved between queues and roles by the transfer rule table on stage change, route decided, timer expired, deviation raised or cleared, approval needed, document received, payment missed, or a manual request with a reason**, so that **hand-offs between teams run without email**.

## 2. Business rationale

A case changes hands between the TDR, litigation, NPA and debt sale teams by email today, and the case can wait between teams with nobody holding it. This story moves the case by rule when one of eight triggers fires, picks the owner in the receiving queue, ends the old assignment and records the rule and version, and gives the team manager a programmatic transfer with a coded reason before the Epic 2 screens. It meets REQ-CWC-010 and REQ-CWC-016.

## 3. Preconditions

- RWB-E1-020 is done: AssignmentEngine and the queue structure are in use.
- RWB-E1-028 is done: timers publish TimerDue when a timer other than a service level expires. A service level breach (TimerBreached) never moves the case (R-UNI-30).
- RWB-E1-027 is done: the decision log writer is available.
- The transfer rows version "TRF-2026.11" (rule table TRANSFER) are loaded through RWB-E1-029. Each row holds trigger event, condition, target queue code and row order.
- The transfer reason list LOV-TRANSFER-REASON holds R01 Capacity, R02 Customer deceased, R03 Skill, R04 Owner absent, R05 Legal referral and R06 Wrong queue (DL23).
- Manual transfer callers hold Queue and allocation U (RW-TEAMMGR, RW-CAPACITY). Hold and release callers hold Case record U (for example RW-LITOFF acting on a Legal instruction).

## 4. Flow

1. Event source: writes a trigger event to the outbox: CaseStateChanged for a stage change or a route decided (rule event ROUTE_APPROVED), TimerDue, DeviationRaised, DeviationCleared, ApprovalRequested, DocumentStored or PaymentMissed.
2. TransferListener: receives the event once per event ID; a repeated event ID is ignored (R-UNI-40).
3. TransferRuleEvaluator (SY-RULES): reads the transfer rows in force and returns the first row, in row order, whose trigger and condition match the case.
4. TransferService: skips an automated transfer when legal_hold is true (R-UNI-20) and logs the skip.
5. TransferService: locks the case by its version, picks the owner in the target queue with AssignmentEngine, and checks the move is allowed from the case status.
6. TransferService: in one transaction ends the open assignment, writes the new assignment (reason TRANSFER), updates queue, team and owner, and writes CaseTransferred (EV-04).
7. TransferService: as the last step before commit, writes the decision log entry with the row ID, version, from and to queue and owner, and the trigger.
8. Team manager: calls POST /cases/{caseId}/transfer with reason code MANUAL, transfer reason R03 and a target owner or queue; steps 5 to 7 run with reason MANUAL.
9. Litigation officer: calls POST /cases/{caseId}/legal-hold with action place or lift; the case goes to On hold or back to the status it paused in.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | Two transfers reach the same case in the same second | First commits; second refused on the version check and logged as rejected | MSG-GEN-004 | AC3 |
| X2 | Manual transfer without a transfer reason | Refused with 422; nothing changes | MSG-P3-001 | AC6 |
| X3 | Named target owner at the caseload cap | Refused with 422; nothing changes | MSG-P3-002 | AC7 |
| X4 | Transfer of a closed case | Refused with 409 | MSG-P3-005 | AC8 |
| X5 | Decision log write fails | Refused with 503 for a manual call; event retried for a rule transfer; nothing changes | MSG-P7-003 | AC9 |
| X6 | Rule trigger arrives while legal_hold is true | No automated transfer; skip logged | None | AC10 |
| X7 | The same event arrives twice | Second ignored; one transfer | None | AC11 |
| X8 | No owner below the cap in the target queue | Case placed in the target queue's overflow queue with no owner; team manager told | MSG-P3-011 | AC12 |
| X9 | Hold placed on a case already on hold | Refused with 409 | MSG-P3-005 | AC13 |
| X10 | No transfer row matches the event | No transfer; nothing logged as a decision | None | AC14 |
| X11 | A role without Queue and allocation U calls the transfer | Refused with 403 | MSG-P4-002 | Access test TC-E1-021-15 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds on the assignment engine (RWB-E1-020) and the timer events (RWB-E1-028); no screen |
| Negotiable | Trigger rows, target queues and the reason list are data |
| Valuable | Removes email hand-offs between the six recovery teams |
| Estimable | One listener, one service, one rule table, two endpoints |
| Small | Fits two weeks with its tests |
| Testable | Every criterion has a test case in section 16 |

## 7. Acceptance criteria

```gherkin
Feature: Transfer rules and engine v1

  Background:
    Given the transfer rows version "TRF-2026.11" are in force
    Given queue "LIT-BKK-OFF" belongs to team "LIT-BKK" and role RW-LITOFF with method "LOWEST_LOAD" and cap 150

  Scenario: AC1 Rule-driven transfer
    Given case RW-2026-000301 is "IN_PROGRESS" in queue "TDR-BKK-CO" with owner U-21
    Given transfer row "TRF-007" moves a case to queue "LIT-BKK-OFF" when ROUTE_APPROVED carries route "R4"
    When the route decision approves route "R4" for the case
    Then the case is in queue "LIT-BKK-OFF" with owner U-31, the member with the lowest load
    Then the assignment of U-21 has an end time and a new assignment has reason "TRANSFER" and rule ID "TRF-007"
    Then the decision log entry carries rule ID "TRF-007" and rule version "TRF-2026.11"

  Scenario: AC2 Manual transfer
    Given a team manager of team "TDR-BKK"
    When they call the transfer endpoint for case RW-2026-000302 with reason code "MANUAL", transfer reason "R03" and target owner U-22
    Then the case owner is U-22
    Then the assignment and the decision log entry carry transfer reason "R03"

  Scenario: AC3 One queue only
    Given case RW-2026-000303 is in queue "TDR-BKK-CO" with record version 7
    When a rule transfer to "LIT-BKK-OFF" and a manual transfer to "DIL-BKK-CO" arrive in the same second
    Then the case ends in exactly one queue
    Then the system refuses the second transfer with MSG-GEN-004
    Then a decision log entry records the second transfer with final call "TRANSFER_REJECTED"

  Scenario Outline: AC4 Eight triggers
    Given transfer row "<row>" moves a case to queue "<queue>" on trigger "<event>"
    Given case RW-2026-000304 meets the row's condition
    When "<event>" arrives for the case
    Then the case is in queue "<queue>"
    Then the decision log entry carries rule ID "<row>"

    Examples:
      | row     | event              | queue        |
      | TRF-001 | CaseStateChanged   | NPA-BKK-CO   |
      | TRF-002 | ROUTE_APPROVED     | LIT-BKK-OFF  |
      | TRF-003 | TimerDue           | LIT-BKK-OFF  |
      | TRF-004 | DeviationRaised    | DEV-HANDLER  |
      | TRF-005 | DeviationCleared   | TDR-BKK-CO   |
      | TRF-006 | ApprovalRequested  | TDR-BKK-APR  |
      | TRF-008 | DocumentStored     | DIL-BKK-CO   |
      | TRF-009 | PaymentMissed      | TDR-BKK-CO   |

  Scenario: AC5 Admin API
    Given a team manager with Queue and allocation U and a litigation officer with Case record U
    When the team manager reassigns case RW-2026-000305 to U-23 with transfer reason "R04"
    When the litigation officer places a legal hold with reason "Court order" and reference "ORD-2026-0412", then lifts it
    Then the case owner is U-23
    Then the case went to "ON_HOLD" and back to "IN_PROGRESS"
    Then each of the three calls has a decision log entry with its reason

  Scenario: AC6 Manual transfer without a reason
    When a team manager calls the transfer endpoint for case RW-2026-000306 with no transfer reason
    Then the system refuses the call with 422 and MSG-P3-001
    Then the case keeps its queue and owner

  Scenario: AC7 Target owner at the cap
    Given U-24 holds 150 open cases in queue "TDR-BKK-CO"
    When a team manager transfers case RW-2026-000307 to U-24 with transfer reason "R01"
    Then the system refuses the call with 422 and MSG-P3-002 naming U-24

  Scenario: AC8 Closed case
    Given case RW-2026-000308 has status "CLOSED"
    When a team manager transfers it to queue "TDR-BKK-CO"
    Then the system refuses the call with 409 and MSG-P3-005

  Scenario: AC9 Decision log unavailable
    Given the decision log store is unavailable
    When a team manager transfers case RW-2026-000309 with transfer reason "R03"
    Then the system refuses the call with 503 and MSG-P7-003
    Then the case keeps its queue and owner

  Scenario: AC10 Legal hold stops automated transfers
    Given case RW-2026-000310 has legal_hold = true
    When TimerDue arrives and matches row "TRF-003"
    Then the case keeps its queue and owner
    Then the system records the skip on the job log with rule R-UNI-20

  Scenario: AC11 A repeated event
    Given PaymentMissed with event ID "EVT-88120" moved case RW-2026-000311 to "TDR-BKK-CO"
    When PaymentMissed with event ID "EVT-88120" arrives again
    Then the case has one transfer for the event
    Then the system counts the repeat as an idempotency hit

  Scenario: AC12 No owner below the cap in the target queue
    Given every member of "LIT-BKK-OFF" holds 150 open cases
    When row "TRF-007" fires for case RW-2026-000312
    Then the case is in the overflow queue "LIT-BKK-OVF" with no owner
    Then the system tells the team manager of "LIT-BKK" with MSG-P3-011 and count 1

  Scenario: AC13 Hold on a case already on hold
    Given case RW-2026-000313 has status "ON_HOLD" with a legal hold
    When a litigation officer places a legal hold again
    Then the system refuses the call with 409 and MSG-P3-005

  Scenario: AC14 No row matches
    Given no transfer row matches DocumentStored for case RW-2026-000314
    When DocumentStored arrives for the case
    Then the case keeps its queue and owner
    Then the system writes no decision log entry
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A case moves by the first transfer row, in row order, whose trigger and condition match | Transfer rows (rule table TRANSFER); REQ-CWC-010 |
| BR2 | The eight triggers are stage change, route decided, timer expired, deviation raised, deviation cleared, approval needed, document received and payment missed, plus manual request | REQ-CWC-010; events EV-05, EV-06, EV-07, EV-09, EV-12, EV-16, EV-18 |
| BR3 | A manual transfer needs a transfer reason from the list | LOV-TRANSFER-REASON (assumed); REQ-WKM-003; VR-P3-010-1 |
| BR4 | A transfer to an owner at the cap is refused | queue.capacity_cap; VR-P3-010-2 |
| BR5 | A case is in exactly one queue with one open assignment | REQ-CWC-005 |
| BR6 | No automated transfer while a legal hold is in force | R-UNI-20 |
| BR7 | Lifting a hold returns the case to the status it paused in | R-UNI-21; casemodel.txt status transitions |
| BR8 | An event with the same ID is processed once | R-UNI-40 |
| BR9 | Every transfer is logged with rule ID and version before it takes effect | Principle 5; R-UNI-39; REQ-CWC-016 |
| BR10 | A transfer keeps the case status and the clocks | R-UNI-18 (same principle for reallocation) |

## 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| New, Assigned, In progress, any Waiting | LEGAL_HOLD_PLACED (R-UNI-20) | Placed through the legal-hold endpoint | On hold |
| On hold | LEGAL_HOLD_LIFTED (R-UNI-21) | Lifted through the legal-hold endpoint | The status it paused in |

A rule or manual transfer changes the queue, the team and the owner, not the status.

## 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-TEAMMGR | Transfers and reassigns cases in team scope (Queue and allocation U) |
| RW-CAPACITY | Transfers cases (Queue and allocation U) |
| RW-LITOFF and other roles with Case record U | Place and lift a legal hold on a Legal or court instruction (Case record U) |
| RW-CASEOWN | Reads the case; may not transfer (Queue and allocation R) |
| SY-RULES | Evaluates the transfer rows |
| SY-CASEWF | Carries out rule transfers (Queue and allocation CRU) |
| SY-DECLOG | Writes the entries |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | recovery_case | id | Read |
| DF-CAS-005 | recovery_case | status | Write |
| DF-CAS-006 | recovery_case | stage_code | Read |
| DF-CAS-008 | recovery_case | route_code | Read |
| DF-CAS-009 | recovery_case | owner_user_id | Write |
| DF-CAS-010 | recovery_case | queue_id | Write |
| DF-CAS-011 | recovery_case | team_code | Write |
| DF-CAS-019 | recovery_case | deviation_open | Read |
| DF-CAS-020 | recovery_case | legal_hold | Write |
| DF-CAS-021 | recovery_case | rule_version | Write |
| DF-CAS-055 | recovery_case | status_before_hold | Write |
| DF-WRK-001 | queue | id | Read |
| DF-WRK-002 | queue | queue_code | Read |
| DF-WRK-004 | queue | team_code | Read |
| DF-WRK-007 | queue | capacity_cap | Read |
| DF-WRK-008 | queue | overflow_queue_id | Read |
| DF-WRK-009 to DF-WRK-016 | assignment | all fields | Write |
| DF-WRK-040 | assignment | transfer_reason_code | Write |
| DF-REF-002 | rule_row | rule_id | Read |
| DF-REF-003 | rule_row | rule_version | Read |
| DF-REF-006 | rule_row | event_code | Read |
| DF-REF-007 | rule_row | condition_expr | Read |
| DF-REF-052 | rule_row | rule_table | Read |
| DF-REF-053 | rule_row | row_order | Read |
| DF-REF-054 | rule_row | target_queue_code | Read |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Write |

Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

**POST /api/recovery/v1/cases/{caseId}/transfer**

| Item | Value |
|---|---|
| Request | TransferRequest: toOwnerId (uuid) or toQueueId (uuid), reasonCode = "MANUAL", note, and transferReasonCode (new field, LOV-TRANSFER-REASON) |
| Response | 200 Assignment: id, caseId, assigneeUserId, assignedAt, reason, ruleId |
| Errors | 401 (MSG-P4-001); 403 no Queue and allocation U (MSG-P4-002); 404 not found or out of scope (MSG-P4-003); 409 status does not allow the move (MSG-P3-005) or version changed (MSG-GEN-004); 422 no reason (MSG-P3-001), owner at cap (MSG-P3-002); 503 decision not recorded (MSG-P7-003) |
| Authorization | Queue and allocation, right U, scope Team |
| Idempotency | Idempotency-Key header; a repeat with the same key returns the first response |

**POST /api/recovery/v1/cases/{caseId}/legal-hold**

| Item | Value |
|---|---|
| Request | LegalHoldRequest: action (place, lift), reason (required), reference |
| Response | 200 Case with status and legalHold |
| Errors | 401; 403 no Case record U (MSG-P4-002); 404; 409 already on hold or not on hold (MSG-P3-005); 503 (MSG-P7-003) |
| Authorization | Case record, right U, scope applied |
| Idempotency | Idempotency-Key header |

**Events.** Consumes CaseStateChanged (EV-05), DeviationRaised (EV-06), DeviationCleared (EV-07), ApprovalRequested (EV-09), PaymentMissed (EV-12), DocumentStored (EV-16), TimerDue (EV-18). Publishes CaseTransferred (EV-04: caseId, fromOwner, toOwner, reasonCode) and CaseStateChanged (EV-05) for hold and release.

**Published interface**

```java
// P3, package recovery.casewf.transfer (published)
public interface TransferService {
    TransferResult transferByRule(UUID caseId, String triggerEvent, UUID eventId);
    TransferResult transferManual(UUID caseId, ManualTransfer request, UUID callerId, String idempotencyKey);
    CaseView placeLegalHold(UUID caseId, String reason, String reference, UUID callerId);
    CaseView liftLegalHold(UUID caseId, String reason, UUID callerId);
}
```

## 13. Solution plan

**Package.** `recovery/casewf/transfer`, Java package `recovery.casewf.transfer`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| TransferListener | Listener | Reads the eight trigger events from the outbox, deduplicates by event ID, calls transferByRule |
| TransferRuleEvaluator | Service | First matching transfer row in row order for an event and a case snapshot |
| TransferService | Published interface | Lock, hold check, owner choice, decision log, assignment swap, event |
| LegalHoldService | Service | Place and lift with status_before_hold |
| CaseAndWorkflowController | Controller | POST /cases/{caseId}/transfer and POST /cases/{caseId}/legal-hold |
| CaseAndWorkflowRepository | Repository | recovery_case, assignment, queue, processed event IDs |
| TransferRuleTable | Rule table | Rule rows with rule table TRANSFER through RuleTableReader (P4) |

**Database**

- Writes recovery_case (queue_id, team_code, owner_user_id, status, legal_hold, status_before_hold, rule_version, version), assignment (end the open row, insert the new row), processed_event (event_id unique), outbox.
- Update with `WHERE id = ? AND version = ?`; zero rows updated means the version changed (MSG-GEN-004).
- Constraint: partial unique index `ux_assignment_open_case ON assignment (case_id) WHERE ended_at IS NULL AND task_id IS NULL`.
- Migration in this story: `V021_1__transfer.sql` adds recovery_case.status_before_hold, assignment.transfer_reason_code, the partial unique index and table processed_event (event_id uuid primary key, consumer varchar(60), processed_at).

**Configuration and reference data**

- Transfer rows "TRF-2026.11" loaded by RW-COE through RWB-E1-029.
- LOV-TRANSFER-REASON (R01 to R06; DL23) loaded by RW-REFADM through RWB-E1-043.
- Queues from RWB-E1-019.

**Build steps**

1. TransferRuleEvaluator with unit tests for each trigger (AC4) and no match (AC14).
2. TransferService.transferByRule with version lock, hold check and assignment swap; tests AC1, AC3, AC10, AC12.
3. TransferListener with processed_event deduplication; test AC11.
4. transferManual with reason and cap validation; tests AC2, AC6, AC7, AC8.
5. LegalHoldService place and lift; tests AC5, AC13.
6. Decision log write as the last step of each transaction, including the rejected transfer; test AC9.
7. Controller endpoints with access checks and Idempotency-Key; access test.

**Feature flag.** `rwb.p3.transfer`. Off: no rule transfers and the two endpoints return 404.

**Done when.** The tests in section 16 pass and each of the eight triggers moves a case in SIT.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-001 | Manual transfer without a reason | Choose a reason for the transfer. |
| MSG-P3-002 | Target owner at the cap | {owner} is at the caseload cap. Choose another owner or the team queue. |
| MSG-P3-005 | Move not allowed from the status | This case cannot move to {state} from {current}. |
| MSG-P3-011 | Target queue full, case in overflow | {count} new cases are waiting in the overflow queue for {team}. Every owner is at the caseload cap. |
| MSG-GEN-004 | Second transfer on a changed record | Someone else changed this record. Reload it to see their change. |
| MSG-P7-003 | Decision log write failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |

## 15. Screens and states

No screen in this story. SCR-02 Case list (list; filtered) and SCR-03 Case record (read only; on hold) show the new queue, owner and the hold banner. The transfer screen SCR-05 comes in Epic 2 (RWB-E2-012).

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-021-01 | AC1, BR1 | System | Case in TDR-BKK-CO, route R4 approved |
| TC-E1-021-02 | AC2, BR3 | System | Manual transfer with R03 |
| TC-E1-021-03 | AC3, BR5 | System | Two transfers on record version 7 |
| TC-E1-021-04 | AC4, BR2 | System | Eight trigger rows |
| TC-E1-021-05 | AC5, BR7 | System | Reassign, place hold, lift hold |
| TC-E1-021-06 | AC6, BR3 | System | No transfer reason |
| TC-E1-021-07 | AC7, BR4 | System | Owner U-24 at 150 |
| TC-E1-021-08 | AC8 | System | Closed case |
| TC-E1-021-09 | AC9, BR9 | System | Decision log store down for a manual call |
| TC-E1-021-10 | AC10, BR6 | System | legal_hold = true and TimerDue |
| TC-E1-021-11 | AC11, BR8 | System | Event EVT-88120 twice |
| TC-E1-021-12 | AC12 | System | Every member of LIT-BKK-OFF at 150 |
| TC-E1-021-13 | AC13 | System | Hold on a case on hold |
| TC-E1-021-14 | AC14, BR1 | System | DocumentStored with no row |
| TC-E1-021-15 | Access | Access | RW-CASEOWN calls POST /cases/{caseId}/transfer and is refused with MSG-P4-002 |
| TC-E1-021-16 | Principle 5 | Resilience | Decision log write forced to fail for a rule transfer; event retried, case unchanged |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: triggers, target queues and the reason list are data.
- No personal data in logs, events, tests or prompts.
- No read of another module's tables: trigger events arrive through the outbox; rule rows through RuleTableReader (P4).
- A transfer never resets the stage clock or the prescription date.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CWC-010 | Transfer by rule on eight triggers and manual request with a reason | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-10 | All recovery processes | R-UNI-20, R-UNI-21, R-UNI-40 | TC-E1-021-01 to TC-E1-021-14 |
| REQ-CWC-016 | Every transfer logged with rule ID and version | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-10 | All recovery processes | R-UNI-39 | TC-E1-021-01, TC-E1-021-03, TC-E1-021-09, TC-E1-021-16 |

## 19. Out of scope

- The transfer screen and queue history on the case (RWB-E2-012, RWB-E2-016).
- Reallocation when an owner leaves or passes the cap (Epic 2, R-UNI-18, R-UNI-19).
- Escalation of a breached timer without moving the case (RWB-E1-028).
- The route decision itself (Epic 4).

