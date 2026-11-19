<!-- source: 04 User stories/Recovery Workbench User Stories Epic 2 Story Files v5.zip!RWB E2 015 Timers escalation and the deviation flag on the case record view v1.md -->
<!-- converted: 2026-11-16 from Markdown (extracted) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 2 Story Files v5.zip!RWB E2 015 Timers escalation and the deviation flag on the case record view v1.md`  
> **Converted from:** Markdown (extracted)

# RWB-E2-015 Timers, escalation and the deviation flag on the case record view

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E2-015 |
| Epic | E2, release 31 December 2026 |
| Module | P3 Case and workflow |
| Feature | FEAT-WKM-05 Show timers and the service level on the case; FEAT-WKM-06 Show the deviation flag on the case; FEAT-WKM-07 Show escalation state on the case; FEAT-DVH-02 Pause the stage clock on a deviation; FEAT-DVH-03 Keep the prescription clock running during a deviation; FEAT-DVH-05 Apply a contact stop for X1 to X3; FEAT-DVH-06 Clear a deviation and resume the timers; FEAT-DVH-09 Handle two deviations on one case |
| Requirement IDs | REQ-WKM-004, REQ-WKM-005, REQ-DVH-002 |
| BRD section | Business Requirements Epic 2, sections 3.3 and 4; Business Requirements Program, sections 5.3 and 5.15 |
| L3 process | All recovery processes; 11 Handle customer care and deviations |
| Decision | X1 to X7 |
| Priority | Must |
| Depends on | RWB-E1-028, RWB-E1-035 |
| Status | Ready for build |

## 1. Story

As a **case owner (RW-CASEOWN)**, I want **the case record view to show every timer with its due date, the escalation path, the prescription date and any deviation flag with its approver**, so that **the next deadline and the reason a case left its path are visible on the case**.

## 2. Business rationale

Deadlines are agreed by email today, and litigation was not filed for debtors who met the criteria because nobody saw the prescription date in time (CTL-18). A deviation pauses the stage clock but never the prescription clock (REQ-DVH-002), so the case owner must see both, with who holds the deviation and where the case returns. This story puts every timer, escalation and deviation on the case record view. It meets REQ-WKM-004, REQ-WKM-005 and REQ-DVH-002. The measure is that every open case's record view shows its next due date and its prescription date.

## 3. Preconditions

- RWB-E1-028 is done: timers, warnings, escalations and prescription dates are written for each case, and JOB-05 Timer check runs every 5 minutes.
- RWB-E1-035 is done: the case record view SCR-03 exists with its timeline.
- The deviation handling module (S8) publishes `DeviationQuery` with the open and cleared deviations of a case.
- The decision log query interface (P7) returns the approver of a deviation decision (decision codes X1 to X7).
- SERVICE_LEVEL rows carry the escalation role for each status (RWB-E1-045; values DL22).
- `prescription.warning-days` is in force (assumed 90; DL22).
- The person holds a role with Case record R and the case is in scope.

## 4. Flow

1. Case owner: opens SCR-03 Case record for a case.
2. Front end: calls `GET /cases/{caseId}` and `GET /cases/{caseId}/timers`.
3. Case service: reads the case, its timers and, for each timer with a task, the owner role of the task.
4. Case service: reads the open deviations from `DeviationQuery` and the approver of each from the P7 decision log query.
5. Case service: reads the escalation role for the case's product and status from `ProductParameterService.serviceLevel(...)`.
6. Front end: shows the timers ordered by due date, each with status, due date, warning state, escalation level, escalated to and the next escalation point.
7. Front end: shows the prescription date with the warning when the business date is on or after the prescription timer's warn at.
8. Front end: when a deviation is open, shows state On hold with MSG-P3-004, each deviation's code, handler, approver, raised date, contact stop and return point.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The case has no running timer | The timers section shows the empty sentence | MSG-P3-018 | AC8 |
| X2 | The case is outside the person's scope | Not found | MSG-P4-003 | AC9 |
| X3 | The deviation module does not answer inside the timeout | The timers show; the deviation section shows that it could not be read and the on hold banner still shows from the case flag | MSG-GEN-006 | AC10 |
| X4 | Two deviations are open | Both show; the case stays on hold until both clear | MSG-P3-004 | AC5 |
| X5 | Prescription date is 91 days away with a 90 day warning | No warning | None | AC3 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Reads what the timer engine and the deviation module already write |
| Negotiable | The layout and the warning days are negotiable; the content is fixed by REQ-WKM-005 |
| Valuable | The next deadline, the escalation and the deviation are on one screen |
| Estimable | Two read endpoints extended, two published interfaces read, one screen section |
| Small | Fits in one sprint with its tests |
| Testable | API tests on seeded timers and deviations and a browser test of SCR-03 |

## 7. Acceptance criteria

```gherkin
Feature: Timers, escalation and the deviation flag on the case record view

  Background:
    Given the business date is 2026-12-15
    Given user "U-CO-01" holds RW-CASEOWN and owns case "RW-2026-000501" with product group "HIRE_PURCHASE" and status "IN_PROGRESS"
    Given prescription.warning-days is 90

  Scenario: AC1 Timers shown
    Given case "RW-2026-000501" has a "NOTICE_PERIOD" timer started on 2026-12-01 expiring on 2027-01-30, on a task owned by role "RW-LITOFF"
    When "U-CO-01" opens the case record
    Then the timer shows type "Notice period", due date 2027-01-30, status "Running" and owner of the next step "Litigation officer"

  Scenario: AC2 Deviation flag
    Given case "RW-2026-000502" has deviation "X3" raised on 2026-12-10, handler "U-SP-01", approved in decision log entry "DLE-9101" by "U-LG-01", paused state "WITH_FCR_OFFICER" and contact stop true
    When "U-CO-01" opens the case record
    Then the screen is in state "On hold" with MSG-P3-004 naming "Deceased customer" and the prescription date
    Then the deviation shows code "X3", handler "U-SP-01", approver "U-LG-01", raised on 2026-12-10, return point "WITH_FCR_OFFICER" and "Contact stopped"

  Scenario: AC3 Prescription
    Given case "RW-2026-000501" has prescription date 2027-02-13, 60 days after the business date
    When "U-CO-01" opens the case record
    Then the prescription date 2027-02-13 shows with the warning MSG-P3-003
    Then for case "RW-2026-000503" with prescription date 2027-03-16, 91 days after the business date, no warning shows

  Scenario: AC4 Escalation state
    Given case "RW-2026-000501" has a "SERVICE_LEVEL" timer that expired on 2026-12-12 with escalation level 1, escalated to "RW-TEAMMGR" at 2026-12-12 09:05
    Given the SERVICE_LEVEL row for "HIRE_PURCHASE" status "IN_PROGRESS" names the next escalation role "RW-PRODHEAD"
    When "U-CO-01" opens the case record
    Then the timer shows status "Expired", escalated to "Team manager" at 2026-12-12 09:05 and next escalation point "Product head"
    Then the case stays in queue and status as before

  Scenario: AC5 Two deviations
    Given case "RW-2026-000504" has deviations "X1" raised on 2026-12-05 and "X3" raised on 2026-12-08, both open
    When "U-CO-01" opens the case record
    Then both deviations show with their own handler and approver
    Then the screen stays in state "On hold"
    Then when "X1" is cleared on 2026-12-14, the screen stays in state "On hold" with only "X3" open and "X1" shown as cleared on 2026-12-14

  Scenario: AC6 Stage clock paused and prescription running
    Given case "RW-2026-000502" with deviation "X3" open since 2026-12-10
    Given its "SERVICE_LEVEL" timer paused on 2026-12-10 and its "PRESCRIPTION" timer running
    When "U-CO-01" opens the case record
    Then the service level timer shows "Paused since 2026-12-10"
    Then the prescription timer shows "Running" with its date

  Scenario: AC7 Deviation cleared and timers resumed
    Given case "RW-2026-000505" had deviation "X1" cleared on 2026-12-14 and its "SERVICE_LEVEL" timer resumed with a new expiry of 2026-12-22
    When "U-CO-01" opens the case record
    Then the screen is not on hold
    Then the service level timer shows "Running" with due date 2026-12-22
    Then the deviation shows as cleared on 2026-12-14 with outcome "Returned"

  Scenario: AC8 No running timer
    Given case "RW-2026-000506" has no timer with status "RUNNING", "PAUSED" or "EXPIRED"
    When "U-CO-01" opens the case record
    Then the timers section shows MSG-P3-018

  Scenario: AC9 Case outside scope
    Given case "RW-2026-000507" belongs to team "SME-NTH" and "U-CO-01" has scope Own in team "MTG-BKK"
    When "U-CO-01" opens it
    Then the system does not find the response with MSG-P4-003

  Scenario: AC10 Deviation module does not answer
    Given the deviation query does not answer within 2 seconds for case "RW-2026-000502"
    When "U-CO-01" opens the case record
    Then the timers and the prescription date show
    Then the deviation section shows MSG-GEN-006 naming "Deviation handling"
    Then the on hold banner shows from the case's deviation flag
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every timer of the case with status Running, Paused or Expired shows with type, due date, status and the owner role of its task | REQ-WKM-005; LOV-TIMER |
| BR2 | A breached service level shows the role it was escalated to, when, and the next escalation point. The case does not move | R-UNI-30; REQ-WKM-004 |
| BR3 | A deviation pauses the stage clock and keeps the prescription clock running | R-DEV-01; REQ-DVH-002 |
| BR4 | A case with a deviation open shows as on hold with the deviation and the prescription date | casemodel.txt Case status (On hold); R-UNI-04; R-UNI-05 |
| BR5 | X1, X2 and X3 show the contact stop | R-UNI-04; R-UNI-05; R-UNI-06; CTL-16 |
| BR6 | The case leaves on hold only when every open deviation is cleared | R-UNI-43; FEAT-DVH-09 |
| BR7 | The prescription date shows a warning from `prescription.warning-days` before it (assumed 90; DL22) | R-UNI-31; CTL-18 |
| BR8 | The return point of a deviation is the routing state the case was in when it paused | DF-CAS-041; R-DEV-08 |
| BR9 | The approver of a deviation is the approver on its decision log entry | REQ-DRI-001 |

## 9. State transitions

None. This story does not change a case status. It shows the timer statuses (Running, Paused, Expired) and the On hold status that other stories set. It adds two fields that the escalation step of JOB-05 Timer check behind TimerScheduler (RWB-E1-028) writes when a timer escalates.

## 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-CASEOWN, case owner | Reads the case record view (Case record R, scope Own) |
| RW-TEAMMGR, team manager | Reads (Case record R, scope Team) |
| RW-SPECIAL, RW-COMPLAIN, RW-FRAUD, RW-LEGAL | Read the case and its deviations (Case record R) |
| RW-AUDIT, internal audit | Reads (Case record R, scope All) |
| SY-CASEWF, case workflow module | Writes the escalation fields in JOB-05 |

Reading the approver needs no Decision log right: the case service returns the approver's user ID only, not the decision log entry.

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | recovery_case | id | Read |
| DF-CAS-003 | recovery_case | product_group | Read |
| DF-CAS-005 | recovery_case | status | Read |
| DF-CAS-017 | recovery_case | prescription_date | Read |
| DF-CAS-018 | recovery_case | stage_clock_start | Read |
| DF-CAS-019 | recovery_case | deviation_open | Read |
| DF-CAS-020 | recovery_case | legal_hold | Read |
| DF-WRK-027 | timer | id | Read |
| DF-WRK-029 | timer | task_id | Read |
| DF-WRK-030 | timer | timer_type | Read |
| DF-WRK-031 | timer | started_at | Read |
| DF-WRK-032 | timer | expires_at | Read |
| DF-WRK-033 | timer | warn_at | Read |
| DF-WRK-034 | timer | paused | Read |
| DF-WRK-035 | timer | status | Read |
| DF-WRK-036 | timer | escalation_level | Read |
| DF-WRK-043 | timer | escalated_to_role | Write (JOB-05 escalation step), Read |
| DF-WRK-044 | timer | escalated_at | Write (JOB-05 escalation step), Read |
| DF-WRK-023 | task | owner_role | Read |
| DF-CAS-038 | deviation | deviation_code | Read, through the S8 interface |
| DF-CAS-039 | deviation | raised_at | Read, through the S8 interface |
| DF-CAS-041 | deviation | paused_state | Read, through the S8 interface |
| DF-CAS-042 | deviation | handler_user_id | Read, through the S8 interface |
| DF-CAS-043 | deviation | contact_stop | Read, through the S8 interface |
| DF-CAS-044 | deviation | cleared_at | Read, through the S8 interface |
| DF-CAS-045 | deviation | outcome | Read, through the S8 interface |
| DF-DEC-010 | decision_log_entry | approver_user_id | Read, through the P7 interface |

Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

**GET /api/recovery/v1/cases/{caseId}** (P3)

| Item | Value |
|---|---|
| Request | Path `caseId` (uuid) |
| Response | 200 `Case` with `prescriptionDate`, `stageClockStart`, `deviationOpen`, `legalHold`, and the new `deviations[]` (`deviationCode`, `raisedAt`, `handlerUserId`, `approverUserId`, `pausedState`, `contactStop`, `clearedAt`, `outcome`) and `deviationsAvailable` (boolean) |
| Errors | 401 (MSG-P4-001); 403 no Case record R (MSG-P4-002); 404 unknown or out of scope (MSG-P4-003); 503 |
| Authorization | Case record, right R, scope applied |
| Idempotency | Not applicable |

**GET /api/recovery/v1/cases/{caseId}/timers** (P3)

| Item | Value |
|---|---|
| Request | Path `caseId` (uuid) |
| Response | 200 `Timer[]` with `timerType`, `startedAt`, `expiresAt`, `warnAt`, `paused`, `status`, `escalationLevel`, and the new `nextStepOwnerRole`, `escalatedToRole`, `escalatedAt`, `nextEscalationRole`, `inWarning` |
| Errors | 401; 403 (MSG-P4-002); 404 (MSG-P4-003); 503 |
| Authorization | Case record, right R, scope applied |
| Idempotency | Not applicable |

**Published interfaces used**

```java
// S8
List<DeviationView> DeviationQuery.forCase(UUID caseId);
// P7
Optional<UUID> DecisionLogQuery.approverOf(UUID caseId, String decisionCode, Instant raisedAt);
// P3, RWB-E1-045
ServiceLevel ProductParameterService.serviceLevel(String productGroup, String caseStatus, LocalDate businessDate);
```

`DeviationQuery.forCase` is called with a 2 second timeout (NFR-008). No events are published.

## 13. Solution plan

**Package.** `recovery.casewf.caseview` in the recovery module; front end folder `src/modules/recovery/casewf/caserecord`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| CaseViewService | Service | Builds the case with deviations, approvers and the availability flag |
| TimerViewService | Service | Builds the timers with the task owner role, escalation fields, next escalation point and warning state |
| TimerRepository | Repository | Reads the case's timers and their tasks |
| EscalationRecorder | Service | Change to the RWB-E1-028 escalation step: writes `escalated_to_role` and `escalated_at` |
| CaseAndWorkflowController | Controller | The two endpoints with the new fields |
| CaseClocksPanel | React component | Timers, prescription date and warnings on SCR-03 |
| DeviationPanel | React component | Deviations, handler, approver, contact stop, return point; on hold banner |

**Database.** Migration `V<next>__rwb_e2_015_timer_escalation.sql` adds `timer.escalated_to_role varchar(20)` and `timer.escalated_at timestamptz`. Reads use `ix_timer_case_id` and `ix_task_case_id`.

**Configuration and reference data.** `prescription.warning-days` = 90 (assumed; DL22), `caseview.deviation-timeout-ms` = 2000, both in the configuration service. SERVICE_LEVEL escalation roles (business lead; DL22). Timer and deviation labels from LOV-TIMER and LOV-DEVIATION through the P4 list interface.

**Build steps**

1. Write the migration; change the escalation step of JOB-05 to write the two fields.
2. Build `TimerViewService` with the owner role, escalation and warning fields; test each timer status.
3. Build `CaseViewService` with the S8 and P7 calls, the timeout and the availability flag.
4. Extend the two endpoints and the generated types.
5. Build `CaseClocksPanel` and `DeviationPanel` with the On hold state and the warnings.
6. Write the tests in section 16 with seeded timers and stubbed S8 and P7 interfaces in system tests, and real ones in SIT.

**Feature flag.** `rwb.p3.case-clocks`. Off: SCR-03 shows the Epic 1 read only fields.

**Done when.** The tests in section 16 pass, and SCR-03 for a case with 50 documents and 6 timers loads within 2 seconds (NFR-009).

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-003 | A timer or the prescription date is inside its warning period | {timer} ends on {date}. |
| MSG-P3-004 | The case is on hold for a deviation | This case is on hold for {deviation}. The prescription date is still {date}. |
| MSG-P3-018 | The case has no running, paused or expired timer | There are no running timers on this case. |
| MSG-GEN-006 | The deviation module does not answer in time | {system} is not available. Your request is queued and will be retried. |
| MSG-P4-003 | The case is outside the person's scope | This case is not in your scope. |
| MSG-P4-002 | A role without Case record R opens the view | You cannot {action} here. Your role does not include it. |

MSG-P3-018 is new (see Additions). Thai text follows DL10.

## 15. Screens and states

| Screen | State | What the user does |
|---|---|---|
| SCR-03 Case record | Loading | Sees skeleton rows in the clocks and deviation panels |
| SCR-03 Case record | Read only | Reads timers, due dates, escalation, prescription date and warnings |
| SCR-03 Case record | Editable | Same panels; edits elsewhere on the record are not part of this story |
| SCR-03 Case record | On hold | Reads the banner with MSG-P3-004 and each open deviation with handler, approver, contact stop and return point |

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-015-01 | AC1, BR1 | System | NOTICE_PERIOD timer on a task owned by RW-LITOFF |
| TC-E2-015-02 | AC2, BR4, BR5, BR8, BR9 | System | X3 with handler, approver, paused state and contact stop |
| TC-E2-015-03 | AC3, BR7 | System | Prescription 60 and 91 days ahead |
| TC-E2-015-04 | AC4, BR2 | System | SERVICE_LEVEL expired, level 1, escalated to RW-TEAMMGR |
| TC-E2-015-05 | AC5, BR6 | System | X1 and X3 open, then X1 cleared |
| TC-E2-015-06 | AC6, BR3 | System | Paused service level and running prescription |
| TC-E2-015-07 | AC7, BR6 | System | X1 cleared and timer resumed |
| TC-E2-015-08 | AC8 | System | Case with only stopped timers |
| TC-E2-015-09 | AC9 | System | Case of team SME-NTH opened by an MTG-BKK owner |
| TC-E2-015-10 | AC10 | System | Stubbed deviation query delayed 3 seconds |
| TC-E2-015-11 | Access | Access | RW-REFADM (no Case record right) calls `GET /cases/{caseId}/timers`; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code. Warning days, escalation roles, timeouts and labels are data.
- No personal data in logs, tests or prompts. The panels show staff user IDs resolved to display names by the ACE common module, and no customer data. Test data is synthetic.
- No read of another module's tables. Deviations come from `DeviationQuery` (S8) and approvers from `DecisionLogQuery` (P7).
- The view never changes a timer, a deviation or the case.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-WKM-004 | A breached service level visible to the escalation role without the case moving | Business Requirements Epic 2, section 3.3; Program, section 5.3 | FEAT-WKM-07 | All recovery processes | R-UNI-30 | TC-E2-015-04, TC-E2-015-11 |
| REQ-WKM-005 | Timers, escalation state and the deviation flag on the case record view | Business Requirements Epic 2, section 3.3; Program, section 5.3 | FEAT-WKM-05, FEAT-WKM-06 | All recovery processes | R-UNI-31, R-UNI-04, R-UNI-05 | TC-E2-015-01 to TC-E2-015-03, TC-E2-015-08 to TC-E2-015-10 |
| REQ-DVH-002 | A deviation pauses the stage clock and keeps the prescription clock running | Business Requirements Epic 2, section 4; Program, section 5.15 | FEAT-DVH-02, FEAT-DVH-03, FEAT-DVH-05, FEAT-DVH-06, FEAT-DVH-09 | 11 Handle customer care and deviations | R-DEV-01, R-UNI-43 | TC-E2-015-02, TC-E2-015-05 to TC-E2-015-07 |

## 19. Out of scope

- Raising, handling and clearing deviations (S8, SCR-06 and SCR-08).
- Starting, pausing and resuming timers, and the escalation itself (RWB-E1-028).
- The history timeline on the case (RWB-E2-016).
- The next action panel (RWB-E2-035).
