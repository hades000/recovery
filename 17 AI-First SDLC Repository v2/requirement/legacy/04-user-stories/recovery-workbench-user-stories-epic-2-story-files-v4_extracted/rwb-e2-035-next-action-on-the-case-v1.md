<!-- source: 04 User stories/Recovery Workbench User Stories Epic 2 Story Files v4.zip!RWB E2 035 Next action on the case v1.md -->
<!-- converted: 2026-11-16 from Markdown (extracted) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 2 Story Files v4.zip!RWB E2 035 Next action on the case v1.md`  
> **Converted from:** Markdown (extracted)

# RWB-E2-035 Next action on the case

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E2-035 |
| Epic | E2, release 31 December 2026 |
| Module | P2 Integration |
| Feature | FEAT-CWC-27 Show the next action and its due date on a case; FEAT-CWC-28 Set the next action from the routing rules |
| Requirement IDs | REQ-WKM-012, REQ-WKM-013, REQ-WKM-016, REQ-WKM-014, REQ-WKM-015 |
| BRD section | Business Requirements Epic 2, section 3.2 |
| L3 process | 06 to 10 Recovery case processes |
| Decision | None |
| Priority | Must |
| Depends on | RWB-E1-018, RWB-E1-031, RWB-E2-033 |
| Status | Ready for build |

## 1. Story

As a **case owner (RW-CASEOWN)**, I want **every active case to show one next action, its owner and its due date, taken from the routing rule that moved the case into its current state**, so that **I never open a case and have to work out what it needs**.

## 2. Business rationale

A case owner today reads the case history to decide what is owed next, and a case can wait for weeks with nobody owing anything on it. The routing rules already hold the action, the owner of the next state and the timer for every move, so the Workbench copies these onto the case at each move and shows them on the case and in the case list. A case with no next action is raised to the team manager as an exception. It meets REQ-WKM-012, REQ-WKM-013 and REQ-WKM-016; the business measure is the count of active cases with no next action, with a target of zero.

## 3. Preconditions

- RWB-E1-018 (case record and transitions), RWB-E1-031 (case list) and RWB-E2-033 (case list with ageing) are done.
- The rule rows for the route sets in force are loaded with action_text, owner_role and timer_spec (RWB-E1-029; DL24).
- The service levels and timers reference table holds a time per state (DL22). Until the business values are loaded it is seeded with 5 working days for each state of the route sets in force (assumed); a state left out of the seed has no row.
- The bank holiday list is loaded in the configuration service under key rwb.calendar.bank-holidays (RWB-E1-042), by RW-REFADM.
- The reader holds a role with Case record R; the transition runs under SY-CASEWF.
- Feature flag `rwb.casewf.next-action` is on.

## 4. Flow

1. SY-RULES: evaluates the route set and returns the firing rule row for the case's state and event.
2. SY-CASEWF: moves the case to the rule's to_state and, in the same transaction, calls NextActionAssigner with the firing rule.
3. NextActionAssigner: copies the rule's action_text, owner_role and rule_id to the case.
4. TimerSpecResolver: turns the rule's timer_spec into a due date (BR3); when the spec has no fixed duration it reads the service levels and timers reference table for the to_state (BR4).
5. NextActionAssigner: sets next_action_waiting when the owner role belongs to a customer party or a partner user (BR5).
6. NextActionAssigner: when no due date can be found, leaves the due date empty and raises task NEXT_ACTION_MISSING on the exception queue for the team manager (BR7).
7. JOB-05 timer check: every 5 minutes finds active cases with no next action, resolves them from the latest state change in the decision log, or raises the same task once.
8. Case owner: opens the case record (SCR-03); the front end calls GET /api/recovery/v1/cases/{caseId}/next-action and shows the action, the owner and the due date, or the waiting text.
9. Team manager: opens the case list (SCR-02); the next action, its owner and due date are columns and an overdue action is marked (BR6).

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The rule's timer_spec is None or has no fixed duration | Due date taken from the service levels and timers table for the to_state | None | AC5 |
| X2 | No due date can be found from the rule or the table | Due date empty; task NEXT_ACTION_MISSING raised once for the team manager; warning on the case | MSG-P2-023 | AC6 |
| X3 | The due date falls on a weekend or a bank holiday | Working days skip Saturday, Sunday and the holiday list | None | AC7 |
| X4 | The case closes | Next action cleared; the case leaves the exception list | None | AC8 |
| X5 | The same transition is delivered twice | Next action unchanged; no second task | None | AC9 |
| X6 | Two transitions on one case commit at the same time | The optimistic lock refuses the second; it is retried and the next action is that of the last committed rule | MSG-GEN-004 | AC10 |
| X7 | An active case from before the flag was switched on has no next action | JOB-05 sets it from the latest state change in the decision log | None | AC11 |
| X8 | The reader's role does not hold Case record R | Refused with 403 | MSG-P4-002 | Access test TC-E2-035-13 |
| X9 | The rule's timer is "same day" | Due date is the business date of the move | None | AC12 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the transition, rule rows and case list that exist after RWB-E1-018 and RWB-E2-033 |
| Negotiable | Action text, owner and timer are rule data; durations for states without a timer are DL22 values |
| Valuable | Every active case states what is owed, by whom and by when |
| Estimable | One assigner, one timer resolver, one job step, one read endpoint, two screen elements |
| Small | Fits in one sprint with its tests |
| Testable | Each criterion below has one test with fixed rule rows and dates |

## 7. Acceptance criteria

```gherkin
Feature: Next action on the case

  Background:
    Given rule R-RES-04 version "RES-2026.12" moves IN_FCR_QUEUE on CASE_PICKED_UP to WITH_FCR_OFFICER with action "Assign the case to a restructuring officer and start the offer clock", owner role RW-RESTRUCT and timer "2 working days"
    Given rule R-SET-13 version "SET-2026.12" moves WITH_OPS_SETTLEMENT on SETTLEMENT_BOOKED to AWAITING_PAYMENT with action "Set the payment due date and wait for the money", owner role CU-BORROW and timer "payment due 30 days"
    Given the bank holiday list holds 31 December 2026 and 1 January 2027

  Scenario: AC1 Every active case carries a next action
    Given case "RW-2026-000401" with status IN_PROGRESS moved by R-RES-04 on 11 December 2026
    When the case is opened
    Then it shows action "Assign the case to a restructuring officer and start the offer clock", owner "Restructuring officer (FCR)" and due date 15 December 2026

  Scenario: AC2 The routing rules set it
    Given case "RW-2026-000402" in state IN_FCR_QUEUE
    When event CASE_PICKED_UP fires R-RES-04 on Friday 11 December 2026
    Then the case holds next action text from R-RES-04, owner role RW-RESTRUCT, rule ID R-RES-04 and due date Tuesday 15 December 2026
    Then the system writes the values in the same transaction as the move to WITH_FCR_OFFICER

  Scenario: AC3 Waiting is a valid next action
    Given case "RW-2026-000403" moved by R-SET-13 on 14 December 2026
    When the case is opened
    Then the next action reads "Waiting for Customer (borrower): Set the payment due date and wait for the money"
    Then the wait ends on 13 January 2027
    Then next action waiting is true

  Scenario: AC4 It is visible on the list
    Given case "RW-2026-000401" with due date 15 December 2026
    Given case "RW-2026-000403" with due date 13 January 2027
    When a manager reads the list on 16 December 2026
    Then next action, next action owner and due date are columns
    Then the system marks row "RW-2026-000401" Overdue
    Then the system does not mark row "RW-2026-000403" Overdue

  Scenario: AC5 A rule with no timer takes the state's service level
    Given rule R-RES-03 moves the case to BACK_TO_ROUTE_DECISION with owner role RW-CASEOWN and timer "None"
    Given the service levels and timers table holds 5 working days for BACK_TO_ROUTE_DECISION
    When R-RES-03 fires on Monday 14 December 2026
    Then the due date is Monday 21 December 2026
    Then the owner shown is the case owner named on the case

  Scenario: AC6 No due date can be found
    Given rule R-DEV-05 moves the case to DEV_WITH_OWNER with owner role RW-LEGAL and timer "deadline driven"
    Given the service levels and timers table holds no row for DEV_WITH_OWNER
    When the rule fires on case "RW-2026-000404" of team "MTG-BKK"
    Then the case holds the action and owner of R-DEV-05 with no due date
    Then the system raises one task NEXT_ACTION_MISSING on the exception queue for role RW-TEAMMGR of team "MTG-BKK"
    Then the case record shows warning MSG-P2-023

  Scenario: AC7 Working days skip weekends and bank holidays
    When R-RES-04 fires on Wednesday 30 December 2026
    Then the due date is Tuesday 5 January 2027

  Scenario: AC8 A closed case has no next action
    Given case "RW-2026-000404" with task NEXT_ACTION_MISSING open
    When the case closes with closure reason SETTLED
    Then the next action fields are empty
    Then the system cancels the task
    Then the case is not in the list of active cases with no next action

  Scenario: AC9 A repeated transition changes nothing
    Given case "RW-2026-000402" was moved by R-RES-04 on 11 December 2026 with decision log entry "DLE-SYN-0402"
    When the same transition with "DLE-SYN-0402" is processed again
    Then the next action and due date are unchanged
    Then the system raises no task

  Scenario: AC10 Two transitions at the same time
    Given case "RW-2026-000405" at version 7
    When two transitions commit against version 7 at the same time
    Then one commits and the other is refused with MSG-GEN-004 and retried against version 8
    Then the next action is that of the rule committed last

  Scenario: AC11 Cases open before the switch-on are filled
    Given 3 active cases with no next action, each with a state change in the decision log by R-RES-04 on 11 December 2026
    When JOB-05 runs on 14 December 2026
    Then each of the 3 cases holds the next action of R-RES-04 with due date 15 December 2026

  Scenario: AC12 A same day timer
    Given a rule with timer "same day" fires on 14 December 2026
    Then the due date is 14 December 2026
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | On every move, the next action text, the owner role and the rule ID come from the firing rule row: action_text, owner_role, rule_id | FEAT-CWC-28; REQ-WKM-013; rule_row |
| BR2 | The next action is never entered by a person | REQ-WKM-013 |
| BR3 | timer_spec "n working days" adds n working days; "n days" with any label before it adds n calendar days; "same day", "Same day" and "immediate" give the date of the move; "next working day" adds 1 working day | rule_row.timer_spec |
| BR4 | Any other timer_spec, including "None", takes the time for the to_state from the service levels and timers table | DL22 |
| BR5 | The next action is a wait when the owner role is of class Customer party or Partner user; the text starts "Waiting for {owner}:" | role.role_class |
| BR6 | A next action is overdue when its due date is earlier than today and the case is not closed | REQ-WKM-012 |
| BR7 | An active case with no due date or no next action raises one NEXT_ACTION_MISSING task to the team manager | REQ-WKM-016 |
| BR8 | Working days are Monday to Friday, excluding the dates in the bank holiday list | Configuration key rwb.calendar.bank-holidays |
| BR9 | When the owner role is the role of the case's queue, the owner shown is the case owner; otherwise the role name | queue.role_code |

## 9. State transitions

None. This story does not change a case status. It writes the next action fields on the case in the same transaction as each move made by RWB-E1-018 and RWB-E1-021, and creates or cancels NEXT_ACTION_MISSING tasks (task status OPEN to CANCELED).

## 10. Authority

| Who | What they may do in this story |
|---|---|
| SY-CASEWF, case workflow module | Writes the next action fields and the exception task (Case record U, Queue and allocation C) |
| SY-RULES, rules component | Returns the firing rule row |
| RW-CASEOWN, case owner | Reads the next action of cases in scope (Case record R) |
| RW-TEAMMGR, team manager | Reads the list and works NEXT_ACTION_MISSING tasks on the exception queue |
| RW-COE, center of excellence analyst | Owns the action, owner and timer columns of the rule rows (Rules and parameters CRUD) |
| RW-REFADM, reference data administrator | Loads the service levels and timers table and the bank holiday list |
| No approval applies | The story takes no decision |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-049 | recovery_case | next_action_text | Write |
| DF-CAS-050 | recovery_case | next_action_owner_role | Write |
| DF-CAS-051 | recovery_case | next_action_due_date | Write |
| DF-CAS-052 | recovery_case | next_action_rule_id | Write |
| DF-CAS-053 | recovery_case | next_action_waiting | Write |
| DF-CAS-005 | recovery_case | status | Read |
| DF-CAS-007 | recovery_case | route_state | Read |
| DF-CAS-009 | recovery_case | owner_user_id | Read |
| DF-CAS-010 | recovery_case | queue_id | Read |
| DF-CAS-011 | recovery_case | team_code | Read |
| DF-CAS-022 | recovery_case | closed_date | Read |
| DF-WRK-005 | queue | role_code | Read |
| DF-WRK-017 to DF-WRK-026 | task | all fields | Write |
| DF-REF-002 | rule_row | rule_id | Read |
| DF-REF-003 | rule_row | rule_version | Read |
| DF-REF-008 | rule_row | action_text | Read |
| DF-REF-009 | rule_row | to_state | Read |
| DF-REF-010 | rule_row | owner_role | Read |
| DF-REF-011 | rule_row | timer_spec | Read |
| DF-REF-036 | role | role_name | Read |
| DF-REF-037 | role | role_class | Read |
| DF-DEC-004 | decision_log_entry | rule_id | Read |
| DF-DEC-005 | decision_log_entry | rule_version | Read |

Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

**GET /api/recovery/v1/cases/{caseId}/next-action** (new; recorded in the additions file)

| Item | Value |
|---|---|
| Parameters | caseId (path, uuid) |
| Response 200 | NextAction: text, ownerRole, ownerName, ownerUserId (when BR9 names the case owner), dueDate, waiting, overdue, missing, ruleId, ruleVersion |
| 401 | No valid session (MSG-P4-001) |
| 403 | Role lacks Case record R (MSG-P4-002) |
| 404 | Case does not exist or is outside scope (MSG-P4-003) |
| Authorization | Case record, right R |
| Idempotency | Read only |

**GET /api/recovery/v1/cases** and **GET /api/recovery/v1/cases/export** (change recorded in the additions file): each Case item and each export row gains nextAction, nextActionOwner, nextActionDueDate and nextActionOverdue, read from the same fields. Authorization and errors are unchanged from RWB-E2-033.

**Interface inside P3** (called by the transition service of RWB-E1-018 in the same transaction)

```java
void NextActionAssigner.assign(UUID caseId, RuleRowRef firedRule, LocalDate businessDate);
Optional<LocalDate> TimerSpecResolver.dueDate(String timerSpec, String toState, LocalDate from);
```

**Published interfaces called**

```java
// P7 decision log, for cases with no next action
Optional<RuleRowRef> DecisionLogQuery.latestStateChange(UUID caseId);
// P4 reference data
RoleInfo ReferenceData.role(String roleCode);          // roleName, roleClass
Optional<Duration> ReferenceData.serviceLevel(String state);
```

**Job step**

| Item | Value |
|---|---|
| Trigger | JOB-05 Timer check, every 5 minutes |
| Step | Next action check: active cases with next_action_rule_id empty or next_action_due_date empty |
| Input | Case rows of P3; the latest state change from P7 |
| Output | Filled next action fields, or one NEXT_ACTION_MISSING task |
| Events published | None |
| Idempotency key | Case ID and task code NEXT_ACTION_MISSING: at most one open task per case |
| Restart | The next run picks up any case the last run missed |

## 13. Solution plan

**Package.** The story is in the P2 backlog. The fields, the rule rows and the transitions belong to P3, so the code is in folder `recovery/casewf/nextaction`, Java package `<ACE base package>.recovery.casewf.nextaction`. Front end folder `src/modules/recovery/caserecord/nextaction`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| NextActionAssigner | Service | BR1, BR5, BR7 and BR9, called inside the transition |
| TimerSpecResolver | Service | BR3, BR4 and BR8, pure functions with a holiday list input |
| NextActionCheckStep | Job | The JOB-05 step for cases with no next action (BR7, AC11) |
| NextActionController | Controller | GET /cases/{caseId}/next-action |
| NextActionRepository | Repository | Reads and writes the next action fields on recovery_case |
| NextActionPanel | React component | Next action on the SCR-03 header with the waiting text, the overdue marker and the MSG-P2-023 warning |

**Database.** Migration in the P3 migration folder adds to recovery_case: next_action_text varchar(1000), next_action_owner_role varchar(20), next_action_due_date date, next_action_rule_id varchar(20), next_action_waiting boolean NOT NULL DEFAULT false; and `CREATE INDEX ix_case_next_action_missing ON recovery_case (team_code) WHERE closed_date IS NULL AND next_action_due_date IS NULL`. Writes task rows (task_code NEXT_ACTION_MISSING, element_type HUMAN_TASK, discretion REQUIRED, owner_role RW-TEAMMGR). Reads rule_row and queue.

**Configuration and reference data.** Rule rows (RW-COE, RWB-E1-029); service levels and timers table (DL22; assumed 5 working days); bank holiday list rwb.calendar.bank-holidays (RW-REFADM); role names and classes (P4).

**Build steps**

1. Add the migration and extend the generated types with the NextAction schema and the new operation.
2. Write TimerSpecResolver with a table of timer_spec cases taken from the 448 rule rows, and unit tests for AC5, AC7 and AC12.
3. Write NextActionAssigner and call it from the transition service in the same transaction; test AC1, AC2, AC3, AC9 and AC10.
4. Add the exception task and its cancel on closure (AC6, AC8).
5. Add NextActionCheckStep to JOB-05 (AC11).
6. Write NextActionController and NextActionPanel; add the next action fields to the Case items of GET /cases and to the export columns (AC4).
7. Add the access test and the contract test for the new operation.

**Feature flag.** `rwb.casewf.next-action`. Off: the assigner is not called, the step does not run and the panel and columns are hidden.

**Done when.** The tests in section 16 pass and the report of active cases with no next action reads zero on the SIT data set after JOB-05 has run.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P2-023 | The case has no next action or no due date (new) | This case has no next action. It is on the exception list for {team}. |
| MSG-GEN-004 | A transition commits against a changed version | Someone else changed this record. Reload it to see their change. |
| MSG-P4-002 | Role lacks Case record R | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | Case outside the reader's scope | This case is not in your scope. |

Thai text for each message follows decision DL10.

## 15. Screens and states

SCR-03 Case record, states Read only, Editable and On hold: the header shows the next action, its owner and its due date; a wait shows "Waiting for {owner}" and the wait end date; an overdue action carries the text "Overdue"; a missing action shows MSG-P2-023. SCR-02 Case list: next action, next action owner and due date columns with the overdue marker. SCR-09 Exception queue: the team manager sees NEXT_ACTION_MISSING tasks.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-035-01 | AC1, BR1, BR9 | System | Case moved by R-RES-04 on 11 December 2026 |
| TC-E2-035-02 | AC2, BR1, BR2, BR3 | System | CASE_PICKED_UP on Friday 11 December 2026 |
| TC-E2-035-03 | AC3, BR5 | System | Case moved by R-SET-13 on 14 December 2026 |
| TC-E2-035-04 | AC4, BR6 | System | Two cases read on 16 December 2026 |
| TC-E2-035-05 | AC5, BR4, BR9 | System | R-RES-03 with timer None; table row of 5 working days |
| TC-E2-035-06 | AC6, BR7 | System | R-DEV-05 with timer "deadline driven" and no table row |
| TC-E2-035-07 | AC7, BR8 | System | Move on 30 December 2026 with two holidays |
| TC-E2-035-08 | AC8 | System | Case with an open NEXT_ACTION_MISSING task closes |
| TC-E2-035-09 | AC9 | System | Same transition processed twice |
| TC-E2-035-10 | AC10 | System | Two transitions against version 7 |
| TC-E2-035-11 | AC11 | System | Three cases with no next action before JOB-05 |
| TC-E2-035-12 | AC12, BR3 | System | Rule with timer "same day" |
| TC-E2-035-13 | Access | Access | RW-REFADM reads the next action; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: action text, owner, timer, service levels and holidays are data.
- No personal data in logs, tests or prompts; the next action holds rule text only.
- No read of another module's tables: the decision log and the role table are read through P7 and P4 interfaces.
- The parser recognizes timer patterns; it never holds a duration for a named state.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-WKM-012 | Every open case carries one next action with owner and due date | Business Requirements Epic 2, section 3.2 | FEAT-CWC-27 | 06 to 10 Recovery case processes | R-RES-04, R-SET-13 | TC-E2-035-01, TC-E2-035-03, TC-E2-035-04, TC-E2-035-08, TC-E2-035-13 |
| REQ-WKM-013 | The next action comes from the rule that moved the case | Business Requirements Epic 2, section 3.2 | FEAT-CWC-28 | 06 to 10 Recovery case processes | R-RES-03, R-RES-04, R-SET-13 | TC-E2-035-02, TC-E2-035-05, TC-E2-035-07, TC-E2-035-09, TC-E2-035-10, TC-E2-035-12 |
| REQ-WKM-016 | A case with no next action is reported as an exception | Business Requirements Epic 2, section 3.2 | FEAT-CWC-27 | 06 to 10 Recovery case processes | R-DEV-05 | TC-E2-035-06, TC-E2-035-11 |
| REQ-WKM-014 | Next action visible on the case record and every queue view | Business Requirements Epic 2, section 3.2 | FEAT-CWC-27, FEAT-CWC-28 | 06 to 10 Recovery case processes | None | TC-E2-035-01 |
| REQ-WKM-015 | An overdue next action escalates like a service level breach | Business Requirements Epic 2, section 3.2 | FEAT-CWC-27, FEAT-CWC-28 | 06 to 10 Recovery case processes | None | TC-E2-035-01 |

## 19. Out of scope

- Escalation when a next action passes its due date: RWB-E2-015 (REQ-WKM-015).
- The next action column in the queue view screens: RWB-E2-011.
- The values of the service levels per state: DL22.
- Loading the route set rule rows beyond allocation, assignment and transfer: DL24.
