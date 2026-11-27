# RWB-P3-E2035-APP Next action on the case

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P3-E2035-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-case |
| Service epic | RWB-SVC-P3 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-035 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP04, DP05, DP06, DP07, DP10, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | L-P3-AM |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P2-E2035-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P3 rwb-case v1.md (FR-P3-021, FR-P3-023) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-035 for rwb-case. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P3-E2035-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **case owner (RW-CASEOWN)**, I want **every active case in rwb-case to carry one next action, its owner and its due date, written in the same transaction as the rule move that put the case into its current state and read from the rule catalogue row that fired**, so that **I never open a case and have to work out what it needs, and a case never waits for weeks with nobody owing anything on it**.

### 2. Business rationale

A case owner today reads the case history to decide what is owed next, and a case can wait for weeks with nobody owing anything on it. The route-set rules already hold the action, the owner of the next state and the timer for every move, as rows of the RESTRUCTURE rule package. The legacy story copied these onto the case at each move, showed them on the case record and in the case list, and raised a case with no next action to the team manager as an exception.

In the target the case of record and its rule move live in rwb-case. Every move is made by CaseWorkflow: EvaluateRules asks the embedded Drools kit for package RESTRUCTURE on the facts and the business date, the answer names the fired rule and the package version, and RecordAndApply writes the state change, the task, the queue placement, the local decision record and the outbox row in one `rwb_case` transaction. This story adds the next action to that same transaction: NextActionAssigner reads the catalogue row of the firing rule inside the embedded kit by rule ID and package version (DP-04), copies `action_text`, `owner_role` and the rule ID onto `recovery_case`, and TimerSpecResolver turns `timer_spec` into a due date on the working-day calendar with the bank holiday list (DP-06). Because the values are written with the move and never recomputed by a reader, the next action always names the rule and the version that set it, and a later package version never rewrites an action already set.

The split is the realignment work. The legacy `RuleCatalog.row(ruleId, packageVersion)` read of the monolith, the legacy `RuleEvaluator` call and the legacy `JOB-05` five-minute Quartz check are replaced by the catalogue of the embedded Drools kit with packages from rwb-decision (DP-04), by the platform workflow kit (DP-10) and by the decision-record library and shared topic `rwb.decision-record.v1` (DP-03). The legacy operation on the monolith base with path `/cases/{caseId}/next-action` becomes `GET /cases/{caseId}/next-action` on `/api/recovery/case/v1` (DP-13), the four `nextAction` columns of the case list and the export are served from the same five fields, and the panel is composed at the edge by gateway-bff (DP-19). JOB-05 is retired: the fill for cases opened before the switch-on runs as a step of DailyCaseRun under a Temporal Schedule, so no Quartz row and no five-minute timer check survives.

It meets REQ-WKM-012, REQ-WKM-013 and REQ-WKM-016 for the case side and it carries the legacy measure: the count of active cases with no next action, with a target of zero. It owns no legacy acceptance criterion; the fourteen criteria of RWB-E2-035 are exercised across services by RWB-ITG-E2035-ITG and by the other slices of the key, and the fifteen criteria in section 7 are new for this service change.

### 3. Preconditions

- RWB-P2-E2035-CON is published: the `NextAction` resource shape (`text`, `ownerRole`, `ownerName`, `ownerUserId`, `dueDate`, `waiting`, `overdue`, `missing`, `ruleId`, `ruleVersion`) and the consumer stub of the contract. This story builds against that contract and its fake; there is no run-time call to rwb-integration.
- The `rwb_case` schema baseline and the case of record exist from the Epic 1 case story (RWB-P3-E1018-APP): `recovery_case`, `task`, `queue`, `timer` and the outbox table.
- Package RESTRUCTURE version "RES-2026.12" is in force for the business date, with rows R-RES-04, R-RES-03, R-SET-13, R-DEV-05 and R-RES-07, each carrying `action_text`, `owner_role` and `timer_spec`; the rows are loaded through RWB-P3-E2042-APP and read only through the catalogue of the embedded Drools kit.
- The embedded Drools kit is published by RWB-PLT-E1072-CON with the rule packages of RWB-P7-E1073-CON, the workflow kit by RWB-PLT-E1071-CON, the decision-record library and shared topic by RWB-PLT-E1027-CON, and the platform guard library by RWB-PLT-E1037-CON. These platform dependencies are held by the platform stories and are not repeated in the metadata rows (GAP-0734; ASM-1301).
- The service levels and timers rows hold a time per state (DL22). Until the business values are loaded the table is seeded with 5 working days for each state of the route sets in force, as the legacy story assumed; a state left out of the seed has no row (GAP-0734; ASM-1304).
- The bank holiday list is loaded as the parameter `rwb.calendar.bank-holidays` (RW-REFADM) and read through the parameters contract of rwb-case, never from code.
- Roles, role names and role classes are data in rwb-access; the role name and the role class of an owner role are read through the rwb-access contract.
- The reader holds a role with Case record R; the move runs under the rwb-case service identity (DP-02) with the Case record write right.
- The feature switch `rwb.casewf.next-action` is a parameter row and is on.

### 4. Flow

1. An event for the case, for example CASE_PICKED_UP, reaches rwb-case through the case router; the router dedupes it on `processed_event` and signals or starts CaseWorkflow (workflow ID = case ID) on task queue `rwb-case`.
2. CaseWorkflow passes the event to the running stage child, which asks the rules: the EvaluateRules activity calls the embedded Drools kit for package RESTRUCTURE on the facts of the case (route state, status, owner, queue, team) and the business date. The package model and its checksum are fetched from rwb-decision and the KieBase is swapped only after the checksum is verified (DP-04); `NoPackageInForce` is a refusal, never a default.
3. The answer names the package version, the fired rule ID and the outputs, including `to_state`.
4. RecordAndApply, in the same activity and in one `rwb_case` transaction, moves the case, writes the task row and the queue placement, writes the local decision record through the decision-record library and inserts its outbox row, and calls NextActionAssigner with the rule ID and the package version. A failed write rolls the whole move back, so nothing moves and no next action is set.
5. NextActionAssigner reads the catalogue row of that rule by rule ID and package version from the catalogue of the embedded kit — `action_text`, `owner_role`, `timer_spec` — and copies `action_text`, `owner_role` and the rule ID onto the case as `next_action_text`, `next_action_owner_role` and `next_action_rule_id`. The workbook, the generated DRL source and the `rwb_decision` rule tables are never read.
6. TimerSpecResolver turns `timer_spec` into `next_action_due_date`: "n working days" adds n working days, "n days" with any label before it adds n calendar days, "same day", "Same day" and "immediate" give the business date of the move, "next working day" adds one working day. Working days are Monday to Friday, excluding the dates of the bank holiday list.
7. Any other `timer_spec`, including "None", takes the time of `to_state` from the service levels and timers rows; a rule with no timer never leaves the due date empty by accident.
8. NextActionAssigner sets `next_action_waiting` when the owner role is of class Customer party or Partner user, and the rendered text starts "Waiting for {owner}: ". The role name and the role class are read through the rwb-access contract.
9. When the owner role is the role of the case's queue, the owner shown is the case owner named on the case; otherwise the owner shown is the role name.
10. When no due date can be found from the rule or the table, `next_action_due_date` stays empty and one task NEXT_ACTION_MISSING is raised on the exception queue for RW-TEAMMGR of the case's team, with the warning MSG-P2-023 on the case. The task is raised once: the idempotency key is the case ID and the task code, so at most one open task exists per case.
11. CaseWorkflow holds the due date of the task as a durable timer of the workflow kit (DP-10); no Quartz row and no five-minute timer check is involved.
12. On a case that closes, the next action fields are cleared and an open NEXT_ACTION_MISSING task is canceled in the same transaction as the closure.
13. A case opened before the switch-on is filled by the next-action check step of DailyCaseRun, fired by the DailyCaseRun Temporal Schedule (DP-10). The step finds active cases with `next_action_rule_id` empty or `next_action_due_date` empty, resolves the rule ID and the rule version from the latest state change in the local decision record, fills the action from the catalogue row, or raises the same task once. JOB-05 is retired and no Quartz job is scheduled.
14. Case owner: the case record is served by the gateway-bff composite route, which calls rwb-case `GET /api/recovery/case/v1/cases/{caseId}` and `GET /api/recovery/case/v1/cases/{caseId}/next-action` and merges the two answers (DP-19); the panel shows the action, the owner, the due date, the rule with its version, the waiting text and the overdue marker.
15. Team manager: the case list and the export carry `nextAction`, `nextActionOwner`, `nextActionDueDate` and `nextActionOverdue`, read from the same fields; `overdue` is computed at read time from `next_action_due_date`, the business date and the closure of the case, and is never stored.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The rule's `timer_spec` is None or has no fixed duration | The due date is taken from the service levels and timers rows for `to_state` | None | AC4 |
| X2 | No due date can be found from the rule or the table | The due date stays empty; one task NEXT_ACTION_MISSING is raised for the team manager and the warning shows on the case | MSG-P2-023 | AC5 |
| X3 | The due date falls on a weekend or a bank holiday | Working days skip Saturday, Sunday and the bank holiday list | None | AC6 |
| X4 | The case closes | The next action fields are cleared and the open task is canceled in the same transaction | None | AC7 |
| X5 | The same transition is delivered twice | The inbox drops it on `processed_event`; the next action and the due date are unchanged; no second task and no second decision record | None | AC8 |
| X6 | Two transitions on one case commit at the same time | The optimistic lock refuses the second; it is retried against the next version and the next action is that of the rule committed last | MSG-GEN-004 | AC9 |
| X7 | An active case from before the switch-on has no next action | The next-action check step of DailyCaseRun sets it from the latest state change in the local decision record | None | AC10 |
| X8 | The rule's timer is "same day" | The due date is the business date of the move | None | AC11 |
| X9 | The read is called by a role without Case record R, or for a case outside the caller's scope | Refused with 403 for the right and 404 for the scope; nothing is returned and nothing is written | MSG-P4-002, MSG-P4-003 | AC13 |
| X10 | No RESTRUCTURE package version is in force on the business date | `NoPackageInForce`; the move is refused and no next action is written; the case keeps its state and queue | MSG-P3-027 | AC12 |
| X11 | The local decision-record write fails during the move | The transaction rolls back: the state and the next action do not move, the step fails and the move is retried | MSG-P7-003 | AC1 |

The exception of X5 is the inbox of the platform event library, recorded in `processed_event` with the idempotency key of the event; X6 is the optimistic lock on the case version, so a retried move always reads the version it commits against.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds on Day 1 against the RWB-P2-E2035-CON fake and the platform kits of DP-03, DP-04, DP-10, DP-11 and DP-19; no work order sits inside another team's lane |
| Negotiable | The action text, the owner role, the timer spec, the service levels and the holiday list are rows and parameters; the story fixes the behaviour |
| Valuable | Every active case states what is owed, by whom and by when, and the answer names the rule and the version that set it |
| Estimable | One assigner, one timer resolver, one step of the daily workflow, one read operation, two extended read operations, one cancel, one panel |
| Small | Fits one sprint with its tests |
| Testable | Each of the fifteen criteria of section 7 is one automated test with fixed catalogue rows and dates |

### 7. Acceptance criteria

```gherkin
Feature: Next action on the case

  Background:
    Given the RESTRUCTURE package version "RES-2026.12" is in force and holds rule R-RES-04, which moves IN_FCR_QUEUE on CASE_PICKED_UP to WITH_FCR_OFFICER with action "Assign the case to a restructuring officer and start the offer clock", owner role RW-RESTRUCT and timer "2 working days"
    Given the same version holds rule R-SET-13, which moves WITH_OPS_SETTLEMENT on SETTLEMENT_BOOKED to AWAITING_PAYMENT with action "Set the payment due date and wait for the money", owner role CU-BORROW and timer "payment due 30 days"
    Given the bank holiday list holds 31 December 2026 and 1 January 2027

  Scenario: AC1 The move writes the next action in the same transaction (new, D-RCV-60)
    Given case "RW-2026-000401" is open in state "IN_FCR_QUEUE" with no next action
    When event CASE_PICKED_UP moves the case to "WITH_FCR_OFFICER" on Friday 11 December 2026
    Then the case holds next_action_text "Assign the case to a restructuring officer and start the offer clock", next_action_owner_role "RW-RESTRUCT", next_action_rule_id "R-RES-04" and next_action_due_date 15 December 2026
    Then EvaluateRules returns ruleId "R-RES-04" and packageVersion "RES-2026.12" and no other rule engine decides the move
    Then the decision record, the state, the task and the outbox row commit in one rwb_case transaction
    Then a failed decision-record write rolls the state and the next action back together

  Scenario: AC2 The catalogue row is the only source of the action (new, D-RCV-60)
    Given the catalogue of the embedded kit holds row R-RES-04 of version "RES-2026.12" with action_text "Assign the case to a restructuring officer and start the offer clock", owner_role "RW-RESTRUCT" and timer_spec "2 working days"
    Given the test fixture holds no workbook and no drl_source
    When R-RES-04 fires on case "RW-2026-000401" on Friday 11 December 2026
    Then the next action text, owner role and timer spec equal the catalogue row character for character
    Then the assigner reads the row by rule ID and package version
    Then the run records zero reads of a workbook and zero reads of a drl_source

  Scenario: AC3 Waiting is a valid next action (new, D-RCV-60)
    When R-SET-13 fires on case "RW-2026-000403" on Monday 14 December 2026
    Then the next action text is "Waiting for Customer (borrower): Set the payment due date and wait for the money"
    Then the case holds next_action_owner_role "CU-BORROW" and next_action_rule_id "R-SET-13"
    Then the wait ends on 13 January 2027 and next_action_waiting is true

  Scenario: AC4 A rule with no timer takes the state's service level (new, D-RCV-60)
    Given RESTRUCTURE rule R-RES-03 moves the case to "BACK_TO_ROUTE_DECISION" with owner role "RW-CASEOWN" and timer "None"
    Given the service levels and timers table holds 5 working days for "BACK_TO_ROUTE_DECISION"
    When R-RES-03 fires on Monday 14 December 2026
    Then its catalogue row returns timer_spec "None" by rule ID and package version
    Then the due date is Monday 21 December 2026
    Then the owner shown is the case owner named on the case

  Scenario: AC5 No due date can be found (new, D-RCV-60)
    Given RESTRUCTURE rule R-DEV-05 moves the case to "DEV_WITH_OWNER" with owner role "RW-LEGAL" and timer "deadline driven"
    Given the service levels and timers table holds no row for "DEV_WITH_OWNER"
    When the rule fires on case "RW-2026-000404" of team "MTG-BKK"
    Then the case holds the action and owner of R-DEV-05 with no due date
    Then one task NEXT_ACTION_MISSING is raised for role RW-TEAMMGR of team "MTG-BKK"
    Then a second move on the same case raises no second open task
    Then the case record shows warning MSG-P2-023

  Scenario: AC6 Working days skip weekends and bank holidays (new, D-RCV-60)
    When R-RES-04 fires on Wednesday 30 December 2026
    Then the due date is Tuesday 5 January 2027

  Scenario: AC7 A closed case clears the action and cancels the task (new, D-RCV-60)
    Given case "RW-2026-000404" holds the next action of R-DEV-05 and an open task NEXT_ACTION_MISSING
    When the case closes with closure reason SETTLED
    Then the next action fields are empty and next_action_waiting is false
    Then the system cancels the task NEXT_ACTION_MISSING
    Then the case is not in the list of active cases with no next action

  Scenario: AC8 A repeated transition changes nothing (new, D-RCV-60)
    Given case "RW-2026-000402" was moved by R-RES-04 on 11 December 2026 with decision log entry "DLE-SYN-0402"
    When the same transition with "DLE-SYN-0402" is delivered again
    Then the inbox drops the duplicate on processed_event
    Then the next action and due date are unchanged
    Then the system writes no second decision record and raises no task

  Scenario: AC9 Two transitions at the same time (new, D-RCV-60)
    Given case "RW-2026-000405" is at version 7
    When two transitions commit against version 7 at the same time
    Then one commits and the other is refused with MSG-GEN-004 and retried against version 8
    Then the next action is that of the rule committed last

  Scenario: AC10 Cases open before the switch-on are filled (new, D-RCV-60)
    Given 3 active cases with no next action, each with a state change in the decision record by R-RES-04 on 11 December 2026
    When the next-action check step of DailyCaseRun runs on 14 December 2026 under the DailyCaseRun Temporal Schedule
    Then each of the 3 cases holds the next action of R-RES-04 with due date 15 December 2026
    Then each reads the text from the catalogue row of "R-RES-04" and "RES-2026.12"
    Then no Quartz row and no JOB-05 timer check is scheduled

  Scenario: AC11 A same day timer (new, D-RCV-60)
    Given RESTRUCTURE rule R-RES-07 carries timer "same day"
    When R-RES-07 moves case "RW-2026-000406" on 14 December 2026
    Then the due date is 14 December 2026

  Scenario: AC12 No RESTRUCTURE version is in force (new, D-RCV-60)
    Given no RESTRUCTURE package version is in force on 2027-01-04
    When event CASE_PICKED_UP fires for case "RW-2026-000407" on 2027-01-04
    Then the evaluation returns NoPackageInForce
    Then the move is refused with MSG-P3-027 for the package in force check
    Then the case keeps its state and its queue and writes no next action

  Scenario: AC13 The read operation and its access (new, D-RCV-60)
    Given case "RW-2026-000401" holds the next action of R-RES-04
    When the case owner calls GET /cases/{caseId}/next-action on /api/recovery/case/v1
    Then the answer carries text, ownerRole, ownerUserId, dueDate, waiting, overdue, ruleId "R-RES-04" and ruleVersion "RES-2026.12"
    Given user "U-REF-01" holds RW-REFADM and no role with Case record R
    When "U-REF-01" calls the same operation
    Then the response is 403 with MSG-P4-002 and no next action data is returned
    Given a case owner whose scope is "Own" and a case owned by another person
    When the case owner calls the same operation for it
    Then the response is 404 with MSG-P4-003
    Then the call writes nothing

  Scenario: AC14 The case list and the export carry the next action (new, D-RCV-60)
    Given case "RW-2026-000401" has due date 15 December 2026
    Given case "RW-2026-000403" has due date 13 January 2027
    When a manager reads GET /cases and GET /cases/export on 16 December 2026
    Then each case item and each export row carries nextAction, nextActionOwner, nextActionDueDate and nextActionOverdue
    Then the system marks row "RW-2026-000401" Overdue
    Then the system does not mark row "RW-2026-000403" Overdue

  Scenario: AC15 The composed screen shows the next action (new, D-RCV-60)
    Given the gateway-bff composite route serves the case record of case "RW-2026-000401"
    When the case owner opens the case record
    Then the SCR-03 panel shows the action, the owner, the due date and rule "R-RES-04" with version "RES-2026.12"
    And the browser calls one composite route and no owner service directly
    When the next action is a wait
    Then the panel shows the waiting text with its end date and the Overdue marker when the due date has passed
```

AC1 to AC15 are new for the rwb-case slice: the legacy criteria AC1 to AC14 of RWB-E2-035 are exercised across services by RWB-ITG-E2035-ITG and by the other slices of the key, and no slice of RWB-E2-035 was allocated the legacy ACs (GAP-0734; ASM-1305).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | On every move, the next action text, the owner role and the rule ID come from the catalogue row of the firing rule, read by rule ID and package version inside the embedded Drools kit: `action_text`, `owner_role`, `timer_spec` | FEAT-CWC-28; REQ-WKM-013; D-RCV-36 T6; DP-04 |
| BR2 | The next action is never entered by a person | REQ-WKM-013 |
| BR3 | `timer_spec` "n working days" adds n working days; "n days" with any label before it adds n calendar days; "same day", "Same day" and "immediate" give the date of the move; "next working day" adds 1 working day | catalogue row `timer_spec` |
| BR4 | Any other `timer_spec`, including "None", takes the time of the target state from the service levels and timers rows | DL22 |
| BR5 | The next action is a wait when the owner role is of class Customer party or Partner user; the text starts "Waiting for {owner}:"; the role name and the role class are read through the rwb-access contract | role class; rwb-access contract |
| BR6 | A next action is overdue when its due date is earlier than today and the case is not closed; the flag is computed at read time and never stored | REQ-WKM-012; DF-CAS-051 |
| BR7 | An active case with no due date or no next action raises one NEXT_ACTION_MISSING task to the team manager; at most one open task per case, keyed on the case ID and the task code | REQ-WKM-016 |
| BR8 | Working days are Monday to Friday, excluding the dates of the bank holiday list held under the parameter `rwb.calendar.bank-holidays` | parameters contract (DP-06) |
| BR9 | When the owner role is the role of the case's queue, the owner shown is the case owner; otherwise the role name | `queue.role_code`; rwb-access contract |
| BR10 | The rule version is the package version label of the evaluation, and the next action records the version of the move that set it; a later version does not rewrite an action already set | D-RCV-36 T5, T7; R-UNI-38 |
| BR11 | No RESTRUCTURE version in force is a refusal (`NoPackageInForce`), never a default move and never an empty next action | D-RCV-36 T3; R-UNI-41 |
| BR12 | `next_action_text`, `next_action_owner_role`, `next_action_due_date`, `next_action_rule_id` and `next_action_waiting` are written together with the move or not at all: the state change, the next action, the task, the decision record and the outbox row are one `rwb_case` transaction | DF-CAS-049 to DF-CAS-053; Principle 5; DP-03 |
| BR13 | The catalogue row and the timer spec come from the embedded Drools kit's catalogue with the packages of rwb-decision; the workbook, the generated DRL source and the `rwb_decision` rule tables are never read | D-RCV-36 T3, T6; DP-04; DP-01 |
| BR14 | The next-action check for cases opened before the switch-on is a step of DailyCaseRun under a Temporal Schedule; JOB-05 is retired and no Quartz job, trigger or five-minute check remains | DP-10; D-RCV-36 T2 |
| BR15 | The read operations write nothing and raise no event | REQ-WKM-014 |

### 9. State transitions

None for the case status: this story does not change a case status. It writes the five next-action fields on `recovery_case` in the same transaction as each move made by CaseWorkflow, clears them on closure, and creates or cancels the NEXT_ACTION_MISSING task.

| Object | From | Trigger | To |
|---|---|---|---|
| task (NEXT_ACTION_MISSING) | OPEN | The case closes with closure reason SETTLED | CANCELED |
| recovery_case (version) | n | A move commits with its next action | n+1 |
| next_action text, owner role, rule ID, due date and waiting flag | Any value | A move commits | The values of the firing catalogue row, or empty when no due date is found |

The case version is the optimistic lock of `recovery_case`; a refused commit is retried against the current version and never writes a second next action from the same event.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| rwb-case service identity (the rwb-case login, DP-02) | Runs the move and the next-action check step; writes the next-action fields, the task, the placement, the timer and the decision record |
| Drools evaluator (SY-RULES identity) | Evaluates package RESTRUCTURE through the embedded kit and returns the rule ID, the package version and the outputs (Rules and parameters R) |
| NextActionAssigner | Reads the catalogue row by rule ID and package version and writes the five fields inside the move's transaction |
| TimerSpecResolver | Turns `timer_spec` into a due date on the working-day calendar; holds no duration for a named state |
| CaseWorkflow | Holds the due date of the task as a durable timer and drives the RecordAndApply transaction; moves no state by itself |
| Decision-record library identity | Writes the local decision record and its outbox row in the same transaction (Decision log C) |
| RW-CASEOWN, case owner | Reads the next action of cases in scope and receives the task of the move (Case record R) |
| RW-RESTRUCT, restructuring officer | Reads the next action of cases in scope (Case record R) |
| RW-LEGAL, legal officer | Reads the next action of cases in scope and works the DEV_WITH_OWNER task (Case record R) |
| CU-BORROW, customer party | Is a wait owner; holds no Workbench right and never reads the case (no Case record right) |
| RW-TEAMMGR, team manager | Reads the list and works NEXT_ACTION_MISSING tasks on the exception queue |
| RW-COE, center of excellence analyst | Owns the action text, owner role and timer spec columns of the rule rows (Rules and parameters CRUD) |
| RW-REFADM, reference data administrator | Loads the service levels and timers rows and the bank holiday list; holds no Case record right and is refused on the read with MSG-P4-002 |
| No approval applies | The story takes no decision |

### 11. Data

| BR Field ID | Entity in rwb_case | Field | Read or write |
|---|---|---|---|
| DF-CAS-049 | recovery_case | next_action_text | Write, and cleared on closure |
| DF-CAS-050 | recovery_case | next_action_owner_role | Write, and cleared on closure |
| DF-CAS-051 | recovery_case | next_action_due_date | Write, and cleared on closure |
| DF-CAS-052 | recovery_case | next_action_rule_id | Write, and cleared on closure |
| DF-CAS-053 | recovery_case | next_action_waiting | Write, and set false on closure |
| DF-CAS-005 | recovery_case | status | Read |
| DF-CAS-007 | recovery_case | route_state | Read |
| DF-CAS-009 | recovery_case | owner_user_id | Read, for the owner shown in BR9 and for the scope |
| DF-CAS-010 | recovery_case | queue_id | Read |
| DF-CAS-011 | recovery_case | team_code | Read, for the NEXT_ACTION_MISSING task |
| DF-CAS-022 | recovery_case | closed_date | Read, for the closure and the overdue flag |
| DF-WRK-005 | queue | role_code | Read, for BR9 |
| DF-WRK-017 to DF-WRK-026 | task | the task fields, `task_code` NEXT_ACTION_MISSING, `due_at`, status | Write, and status on cancel |
| DF-REF-002, DF-REF-003, DF-REF-008, DF-REF-009, DF-REF-010, DF-REF-011, DF-REF-296, DF-REF-297, DF-REF-298 | catalogue row of the embedded Drools kit (owner P7, packages of rwb-decision) | rule_id, rule_version, action_text, to_state, owner_role, timer_spec, package_version_id, drools_rule_name, outputs | Read, by rule ID and package version |
| DF-REF-036, DF-REF-037 | role (owner P4, through the rwb-access contract) | role_name, role_class | Read, for BR5 and BR9 |
| DF-DEC-004, DF-DEC-005 | decision record (local library) | rule_id, rule_version | Write locally in the move's transaction |
| Not a field: the service levels and timers rows and the bank holiday list | reference rows and parameter of rwb-case | the time per state and the holiday dates | Read |

The catalogue row is read only inside the embedded kit by rule ID and package version; this story reads no workbook, no `drl_source` and no `rwb_decision` table (DP-04, DP-01). The field of the rwb-access answer that carries the role class is Not specified in the source documents (GAP-0734; ASM-1303); until the field is agreed the story reads the role name and the role class through the platform guard library and its response model. Field IDs are those in the Logical Data Model and Data Dictionary v9.

### 12. Contract

#### 12.1 REST operations provided

Base `/api/recovery/case/v1`; owner rwb-case (P3).

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| GET | `/cases/{caseId}/next-action` | The next action of the case: `text`, `ownerRole`, `ownerUserId`, `dueDate`, `waiting`, `overdue`, `missing`, `ruleId`, `ruleVersion` (the `NextAction` resource shape of RWB-P2-E2035-CON); a new operation recorded in the additions file of the contract story | Case record R, scope applied | Not applicable: the call writes nothing |
| GET | `/cases` | The case list, extended with `nextAction`, `nextActionOwner`, `nextActionDueDate` and `nextActionOverdue` on each case item (a backward-compatible addition, no field removed) | Case record R, scope applied | Not applicable |
| GET | `/cases/export` | The case export, extended with the same four columns (a backward-compatible addition, no column removed) | Case record R, scope applied | Not applicable |

Errors: 401 no session (MSG-P4-001), 403 no Case record R (MSG-P4-002), 404 not found or out of scope (MSG-P4-003), 503 store down. `overdue` and `missing` are computed on the read: `overdue` is true when `next_action_due_date` is earlier than the business date and the case is not closed; `missing` is true when `next_action_rule_id` is empty.

#### 12.2 REST operations consumed

| Method | Path | Service | Used for | Timeout |
|---|---|---|---|---|
| POST | `/api/recovery/access/v1/authorise` | rwb-access (P4), through the platform guard library RWB-PLT-E1037-CON (DP-11) | The Case record right and the scope before a read, and the role name and role class for BR5 and BR9; cached per request | One hop, 2 s |

This story calls no other service at run time. The `NextAction` resource shape and the consumer stub come from RWB-P2-E2035-CON, which is built against and tested with its fake; there is no run-time call to rwb-integration in this story.

#### 12.3 Events published

| Event | Topic | Owner of the type | Key | Payload (IDs and facts only) |
|---|---|---|---|---|
| `rwb.decision-record.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | P7 owns the type and the central ledger; every service writes its own record (DP-03) | caseId | decision record reference, rule ID (for example R-RES-04), package version, business date |

The record and its outbox row are written in the same `rwb_case` transaction as the state change and the next action, and relayed with the CloudEvents envelope; no personal data and no account number is carried. This story adds no `rwb.case` event: the case events of the move belong to the stories that own each move.

#### 12.4 Events consumed

None. The next action is set inside the transaction of a move that another story triggers; this story adds no consumer and no handler.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Purpose |
|---|---|---|---|
| CaseWorkflow | Workflow (parent, one per case, workflow ID = case ID) | `rwb-case` | Drives the move; the assigner runs inside the RecordAndApply transaction it starts, and the task due date is a durable timer |
| RecordAndApply | Activity (workflow kit) | `rwb-case` | Moves the case, writes the task, the placement and the local decision record, and calls NextActionAssigner to write the five fields in the same transaction |
| DailyCaseRun | Workflow (Schedule and event-started from AceDataReady) | `rwb-case` | Runs the next-action check step, replacing JOB-05 |
| NextActionCheckStep | Step of DailyCaseRun | `rwb-case` | Fills the next action of active cases that have none, or raises one NEXT_ACTION_MISSING task |

No new activity beyond RecordAndApply and the step of DailyCaseRun: the evaluate, the record and the apply are the ones the case workflow already has.

#### 12.6 Schedules

| Schedule | Workflow | Purpose |
|---|---|---|
| DailyCaseRun Temporal Schedule (DP-10) | DailyCaseRun | Fires the daily case run whose next-action check step fills the cases opened before the switch-on |

Nothing else is scheduled: JOB-05 is retired, no Quartz job, trigger or five-minute timer check is created, and the story adds no second Schedule. The time of day of the DailyCaseRun Schedule is Not specified in the source documents (GAP-0734; ASM-1302).

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| recovery_case | P3 (rwb_case) | The story adds `next_action_text` varchar(1000), `next_action_owner_role` varchar(20), `next_action_due_date` date, `next_action_rule_id` varchar(20) and `next_action_waiting` boolean NOT NULL DEFAULT false (DF-CAS-049 to DF-CAS-053), and writes and clears them |
| task | P3 (rwb_case) | The NEXT_ACTION_MISSING task with its `due_at` and its CANCELED status |
| queue | P3 (rwb_case) | `role_code`, read for BR9 |
| timer | P3 (rwb_case) | The screen projection of the due date; the clock itself is the durable timer of CaseWorkflow |
| outbox_event, processed_event, idempotency_key | PLT library, created in rwb_case | Outbox, inbox and idempotency objects of the move and of the decision-record event |
| decision_record | Local table of the RWB-PLT-E1027-CON library, created in rwb_case | The local decision record of the move, with its rule ID and package version (DP-03) |

rwb-case reads no table of another service and holds no foreign key across services (DP-01). The catalogue row of the rule is read inside the embedded kit and no `rwb_decision` table is read or written by this story.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| RWB-P2-E2035-CON consumer stub | The `NextAction` resource shape and the consumer side of the contract story | The `NextAction` objects of AC1, AC3, AC13 and AC14, and the error envelope of 403 and 404 |
| rwb-access WireMock | The P4 contract through the platform guard library RWB-PLT-E1037-CON | `POST /authorise` granting Case record R, refusing it for RW-REFADM, excluding a case from an Own scope, and returning the role name and role class |
| Temporal test server | The workflow kit of RWB-PLT-E1071-CON | CaseWorkflow with the RecordAndApply transaction, the DailyCaseRun workflow and its Schedule |
| Drools test kit | The embedded kit of RWB-PLT-E1072-CON with the packages of RWB-P7-E1073-CON | Version "RES-2026.12" with rows R-RES-04, R-RES-03, R-SET-13, R-DEV-05 and R-RES-07 and their catalogue rows; the empty answer of the no-package path |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided (2 extended), 1 consumed | The next-action read provided, and the case list and the export extended; the P4 authorise consumed through the platform guard library; one hop, 2 s |
| Kafka | 1 published, 0 consumed | `rwb.decision-record.v1` published through the outbox; nothing consumed |
| Temporal | 1 workflow plus 1 Schedule | CaseWorkflow with the assigner inside RecordAndApply, and the DailyCaseRun Schedule with its next-action check step |
| File | None | This story reads and writes no file |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.case`, module `nextaction`, Java package `th.co.scb.ace.workbench.recovery.case.nextaction`; front end `src/modules/recovery/case/NextActionPanel.tsx`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision | H RWB-PLT-E1072-CON; C RWB-P7-E1073-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The H and C dependencies this table adds are held by the platform and service contract stories and are not repeated in the metadata rows, which carry only the contract dependency of the legacy key: RWB-P2-E2035-CON (GAP-0734; ASM-1301). DP-05 resolves to no ACE view and no rwb-source-data call: the next action needs the rule row and the case row only, so rwb-case reads no `v_ace_*` view. DP-14 resolves to no new topic of its own, because this story publishes only on the shared `rwb.decision-record.v1` and adds no case event; the naming library still supplies the envelope. DP-15 resolves to one migration in `rwb_case`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| NextActionAssigner | Service | BR1, BR5, BR7, BR9, BR10 and BR12; reads the catalogue row by rule ID and package version and writes the five fields inside the move's transaction |
| TimerSpecResolver | Service | BR3, BR4 and BR8; pure functions with the service levels and the holiday list as inputs, with no duration for a named state |
| NextActionCheckStep | Step of DailyCaseRun | The retired JOB-05 step: fills active cases that have no next action or no due date, or raises the task once (BR7, BR14) |
| NextActionRepository | Repository | Reads and writes the five fields on `recovery_case` in `rwb_case` only |
| NextActionController | Controller | `GET /cases/{caseId}/next-action` and the four fields of the case list and the export |
| ClosureListener | Service adapter | Clears the fields and cancels the open task in the closure transaction |
| NextActionPanel | React component | The next action on the SCR-03 header with the waiting text, the rule and its version, the overdue marker and the MSG-P2-023 warning |

**Database and migrations**

- Migration `V2035_1__next_action.sql` adds to `recovery_case`: `next_action_text` varchar(1000), `next_action_owner_role` varchar(20), `next_action_due_date` date, `next_action_rule_id` varchar(20) and `next_action_waiting` boolean NOT NULL DEFAULT false (DF-CAS-049 to DF-CAS-053).
- `next_action_owner_role` is validated against the role list by the service, with no database check constraint on the list value.
- One index for the check step: `ix_case_next_action_missing ON recovery_case (team_code) WHERE closed_date IS NULL AND next_action_due_date IS NULL`, so the page of active cases with no due date is read without a scan.
- No new table: the task, the queue, the timer, the outbox and the local decision record already exist in `rwb_case` from the Epic 1 story and the platform libraries.
- The migration runs in the rwb-case Flyway sequence of the service's own schema (DP-15); no other schema is touched.

**Configuration and reference data**

- Package RESTRUCTURE version "RES-2026.12" with rows R-RES-04, R-RES-03, R-SET-13, R-DEV-05 and R-RES-07, each with its action text, owner role and timer spec (RW-COE, through RWB-P3-E2042-APP). The version in force per environment is read from the rwb-decision registry on every evaluation; there is no lock file.
- The service levels and timers rows (DL22, RW-REFADM): until the business values are loaded the table is seeded with 5 working days for each state of the route sets in force, as the legacy story assumed, so a state left out of the seed has no row (GAP-0734; ASM-1304).
- Parameter `rwb.calendar.bank-holidays` with the holiday dates (RW-REFADM), read through the parameters contract of rwb-case (DP-06).
- Roles, role names and role classes in rwb-access; the role name and the role class are read through the contract (GAP-0734; ASM-1303).
- Feature switch `rwb.casewf.next-action` as a parameter row: off means the assigner is not called, the check step does not run, and the panel and the four columns are hidden.

**Build steps**

1. Add the migration and the five fields to `recovery_case`, and extend the generated types with the `NextAction` schema of RWB-P2-E2035-CON.
2. Write TimerSpecResolver with a table of `timer_spec` cases taken from the route-set rows and the service level lookup, and unit tests for AC4, AC6 and AC11.
3. Write NextActionAssigner against the catalogue of the embedded kit and call it from RecordAndApply in the same transaction; tests for AC1, AC2 and AC3.
4. Add the NEXT_ACTION_MISSING task, its idempotency key and its cancel on closure; tests for AC5 and AC7.
5. Add the inbox dedupe and the optimistic lock paths around the assigner; tests for AC8 and AC9.
6. Add NextActionCheckStep to DailyCaseRun under its Schedule and retire JOB-05; test for AC10.
7. Write NextActionController with the access check, the scope, the overdue flag and the four fields of the list and the export; tests for AC13 and AC14, and the contract test for AC12.
8. Write NextActionPanel and the composite-route contract test; test for AC15.
9. Contract-fake run of every consumed answer in isolation, so the story builds before rwb-integration and rwb-access land.

**Done when.** The tests in section 16 pass, the report of active cases with no next action reads zero on the SIT data set after the DailyCaseRun step has run, and every next action names its rule ID and package version.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P2-023 | The case has no next action or no due date (new) | This case has no next action. It is on the exception list for {team}. |
| MSG-P3-027 | No RESTRUCTURE version is in force | The rule version was refused at the {check} check: {detail}. |
| MSG-GEN-004 | A transition commits against a changed version | Someone else changed this record. Reload it to see their change. |
| MSG-P7-003 | The local decision-record write fails during the move | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | The role lacks Case record R | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | The case is outside the reader's scope | This case is not in your scope. |

For MSG-P3-027 in this story {check} is "package in force" and {detail} names the package code RESTRUCTURE and the business date only, never a case fact. For MSG-P2-023 {team} is the team code of the case and nothing else. Thai text for each message follows decision DL10.

### 15. Screens and states

SCR-03 Case record, states read only, editable and on hold: the header shows the next action, its owner, its due date and the rule ID with its version; a wait shows "Waiting for {owner}" and the wait end date; an overdue action carries the text "Overdue"; a missing action shows MSG-P2-023. SCR-02 Case list: the next action, next action owner and due date columns with the overdue marker. SCR-09 Exception queue: the team manager sees the NEXT_ACTION_MISSING tasks.

All three are served by the gateway-bff composite route (DP-19), which calls rwb-case, one hop, and merges the answers into the screen model: the browser calls one composite route and no owner service directly. The full read-only case record view, the timer section and the deviation flag remain with RWB-P3-E1023-APP; the queue-view next action column remains with RWB-E2-011.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-035-01 | AC1, AC15, BR1, BR9, BR10, BR12 | Component | Case moved by R-RES-04 on 11 December 2026 |
| TC-E2-035-02 | AC1, AC2, BR1, BR2, BR3, BR10, BR13 | Component | CASE_PICKED_UP on Friday 11 December 2026 |
| TC-E2-035-03 | AC3, BR5 | Component | Case moved by R-SET-13 on 14 December 2026 |
| TC-E2-035-04 | AC14, BR6 | Component | Two cases read on 16 December 2026 |
| TC-E2-035-05 | AC4, BR4, BR9 | Component | R-RES-03 with timer None; table row of 5 working days |
| TC-E2-035-06 | AC5, BR7 | Component | R-DEV-05 with timer "deadline driven" and no table row |
| TC-E2-035-07 | AC6, BR8 | Component | Move on 30 December 2026 with two holidays |
| TC-E2-035-08 | AC7 | Component | Case with an open NEXT_ACTION_MISSING task closes |
| TC-E2-035-09 | AC8 | Component | Same transition processed twice |
| TC-E2-035-10 | AC9 | Component | Two transitions against version 7 |
| TC-E2-035-11 | AC10, BR14 | Component | Three cases with no next action before the daily case run |
| TC-E2-035-12 | AC11, BR3 | Component | Rule with timer "same day" |
| TC-E2-035-13 | AC13 | Component | RW-REFADM reads the next action; refused with MSG-P4-002 |
| TC-E2-035-14 | AC12, BR11 | Component | No RESTRUCTURE version in force on 2027-01-04; NoPackageInForce and MSG-P3-027 |

The legacy levels map System to Component and Access to Component, because the cross-service journey of this key is proved by RWB-ITG-E2035-ITG. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the action text, the owner role, the timer spec, the service levels and the holiday dates are rows or parameters.
- No personal data in logs, tests, workflow history or prompts: the next action holds rule text only, and logs carry case IDs and rule IDs, never account numbers, names or identity numbers; the workflow payloads pass the payload codec.
- No read of another service's tables: the catalogue row is read inside the embedded kit, the role name and role class through the rwb-access contract; `rwb_case` holds no foreign key into another schema (DP-01).
- One evaluator: the move calls the embedded Drools kit on the package version of rwb-decision, and no second rule engine decides the target state (DP-04).
- The workbook, the generated DRL source and the `rwb_decision` rule tables are never read by this story; the catalogue is the only source of an action text, an owner role and a timer spec.
- The parser recognises timer patterns; it never holds a duration for a named state.
- A read of the next action writes nothing and raises no event.
- The next action is written before the transaction commits and in the same transaction as the state change, the task and the decision record; a failed write rolls the whole move back (R-UNI-39, DP-03).
- NoPackageInForce is never caught and turned into a default move or an empty next action.
- The decision-record event is written to the outbox in the same transaction and carries IDs and facts only.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-WKM-012 | Every open case carries one next action with owner and due date | Business Requirements Epic 2, section 3.2 | FEAT-CWC-27 | 06 to 10 Recovery case processes | R-RES-04, R-SET-13 | TC-E2-035-01, TC-E2-035-03, TC-E2-035-04, TC-E2-035-08, TC-E2-035-13 |
| REQ-WKM-013 | The next action comes from the rule that moved the case | Business Requirements Epic 2, section 3.2 | FEAT-CWC-28 | 06 to 10 Recovery case processes | R-RES-03, R-RES-04, R-SET-13 | TC-E2-035-02, TC-E2-035-05, TC-E2-035-07, TC-E2-035-09, TC-E2-035-10, TC-E2-035-12, TC-E2-035-14 |
| REQ-WKM-016 | A case with no next action is reported as an exception | Business Requirements Epic 2, section 3.2 | FEAT-CWC-27 | 06 to 10 Recovery case processes | R-DEV-05 | TC-E2-035-06, TC-E2-035-11 |
| REQ-WKM-014 | Next action visible on the case record and every queue view | Business Requirements Epic 2, section 3.2 | FEAT-CWC-27, FEAT-CWC-28 | 06 to 10 Recovery case processes | None | TC-E2-035-01 |
| REQ-WKM-015 | An overdue next action escalates like a service level breach | Business Requirements Epic 2, section 3.2 | FEAT-CWC-27, FEAT-CWC-28 | 06 to 10 Recovery case processes | None | TC-E2-035-01 |
| D-RCV-60 DP-04 | The catalogue row and the package version come from the embedded kit with the packages of rwb-decision, and every next action names its rule and version | Decision log, D-RCV-60; Template and Rules §R5.5 | FEAT-CWC-28 | 06 to 10 Recovery case processes | R-RES-04; D-RCV-36 T4 to T7 | TC-E2-035-02, TC-E2-035-05, TC-E2-035-14 |
| D-RCV-60 DP-10 | JOB-05 is retired and its check runs as a step of DailyCaseRun under a Temporal Schedule, with no Quartz row | Decision log, D-RCV-60; Template and Rules §R5.5; Architecture v5 slide 44 | FEAT-CWC-27 | 06 to 10 Recovery case processes | R-RES-04 | TC-E2-035-11 |

### 19. Out of scope

- Escalation when a next action passes its due date: RWB-E2-015 (REQ-WKM-015).
- The next action column in the queue view screens: RWB-E2-011.
- The values of the service levels per state: DL22.
- Loading the route set rule rows beyond allocation, assignment and transfer: DL24; the RESTRUCTURE rows are RWB-E2-042 and RWB-P3-E2042-APP.
- The RESTRUCTURE package checks, its scenarios and its approval (RWB-E1-073).
- The rule catalogue, the rule registry and the central decision ledger: rwb-decision (RWB-P7-E1073-CON, RWB-PLT-E1027-CON).
- The `NextAction` resource shape and the consumer stub themselves: RWB-P2-E2035-CON; there is no run-time call to rwb-integration in this story.
- The `POST /authorise` operation, the roles, the role classes and the scope data: rwb-access (RWB-PLT-E1037-CON and the P4 access stories).
- The gateway-bff composite route itself (RWB-PLT-N001-CON) and the full read-only case record view (RWB-P3-E1023-APP).
- The deployment of this capability: chart values, topic and queue provisioning, dashboards and the runbook.
