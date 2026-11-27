# RWB-P2-E2035-APP Next action on the case

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P2-E2035-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-integration |
| Service epic | RWB-SVC-P2 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Size | Set by the squad at refinement |
| Contract version | v1 (the /v1 path of /api/recovery/integration) |
| Legacy key | RWB-E2-035 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP04, DP05, DP06, DP07, DP10, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | L-P2-H |
| Ready to start | After RWB-P2-E2033-APP |
| Depends on (build) | RWB-P2-E2035-CON, RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1071-CON, RWB-PLT-E1047-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON, RWB-P2-E2033-APP |
| Contract dependencies | RWB-P3-E1042-CON, RWB-P3-E1043-CON, RWB-P3-E1018-CON, RWB-P3-E1031-CON, RWB-P3-E2042-CON |
| Integration dependencies | None |
| External dependencies | RWB-P2-E2035-OPS |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P2 rwb-integration v1.md (no FR mapped to REQ-WKM-012, REQ-WKM-013, REQ-WKM-016, REQ-WKM-014, REQ-WKM-015) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-035 for rwb-integration. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P2-E2035-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (16 resolved, 40 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **case owner (RW-CASEOWN)**, I want **every active case to show one next action, its owner and its due date, resolved from the rule package that moved the case into its current state and served by one operation of the integration service**, so that **I never open a case and have to work out what it needs**.

The legacy story put the assigner, the field writes, the read endpoint and the JOB-05 check in one module. Under D-RCV-60 the work splits by owner. rwb-case owns the case record, the CMMN state, the queues, the tasks and the timers (Arch v5 slide 41), so rwb-case writes `recovery_case.next_action_*` in the same transaction as the move, cancels the exception task and holds the optimistic lock; that side is `RWB-P3-E2035-APP`, which consumes the resolve operation published here. rwb-integration owns the resolution itself: `POST /api/recovery/integration/v1/next-actions:resolve` is the side-effect-free operation that turns the rule that fired into the action text, the owner, the due date, the waiting flag and the missing flag; `GET /api/recovery/integration/v1/cases/{caseId}/next-action` is the read the case record screen consumes; `POST /api/recovery/integration/v1/cases/{caseId}/next-action` is the JOB-05 fill, which resolves and then writes through the rwb-case contract; and the `next-action-check` Schedule finds active cases with no next action and fills them or raises one `NEXT_ACTION_MISSING` task.

The Ownership Map keeps `GET /cases/{caseId}/next-action` with P3 (API Specification v4, x-module P3; Arch v5 slide 41), while this work package assigns the story to rwb-integration. The two are reconciled explicitly: rwb-integration serves the path under its own base `/api/recovery/integration/v1` (DP-13), and rwb-case keeps the case row, the four columns and the write. The operation is therefore served here and owned there, and the conflict is carried in GAP-0667 and ASM-1178 rather than left implicit.

What this story does not do is decide. The evaluation of the RESTRUCTURE package stays with the case workflow's `EvaluateRules` activity, which returns `RuleResult(packageCode, packageVersion, ruleId, outputs)` and raises `NoPackageInForce`; this service receives the fired rule ID and package version, reads the catalog row through `RuleCatalog.row(ruleId, packageVersion)` as published in `RWB-P3-E2042-CON`, and holds no second rule engine. It reads no workbook, no generated DRL and no rule table (D-RCV-36 T3, T5, T6; DP-04).

### 2. Business rationale

A case owner today reads the case history to decide what is owed next, and a case can wait for weeks with nobody owing anything on it. The route-set rules already hold the action, the owner of the next state and the timer for every move, as rows of the RESTRUCTURE rule package. The Workbench copies these onto the case at each move and shows them on the case and in the case list. A case with no next action is raised to the team manager as an exception. The measure is the count of active cases with no next action, with a target of zero, and it meets REQ-WKM-012, REQ-WKM-013 and REQ-WKM-016.

In the target the data stays where it is and the calls change. The rule rows are registry rows of rwb-decision (Ownership Map: `rule_row`, `rule_package_version` are P7; ASM-0069), and the catalog operation that answers action_text, owner_role and timer_spec is the one published in `RWB-P3-E2042-CON`, which reads rwb-decision. The role name and the role class, the service levels and timers rows and the calendar rows are reference data of rwb-case (Ownership Map: `reference_row`, `reference_version` are P3; DP-07). The case facts are case facts of rwb-case (DP-01). The decision log is the central ledger of rwb-decision (DP-03). The authorise check is the contract of rwb-access (DP-08 is not in the pattern list of this legacy key, and the check is therefore carried as the `RWB-P4-E1037-CON` contract dependency of the resolve read).

Two legacy components move for good reason. `RuleEvaluator` was called from the same transaction as the write; in the target the evaluation is the case workflow's activity and the resolution is a separate, side-effect-free call, so the case transaction stays short and the same resolve answer can serve the case screen, the fill step and the case list columns. `NextActionCheckStep` was a step inside JOB-05 Timer check; in the target JOB-05 is retired (Arch v5 slide 44 lists it as durable timers, and the Ownership Map ruling on `timer` retires `TimerDue`), so the fill becomes the Temporal Schedule `next-action-check` on the queue of this service, every five minutes. The legacy flag `rwb.casewf.next-action` is kept as the reference of the switch, and the switch itself is a feature flag of the platform flag library (R-PREC default ruling).

The authorise check is the contract of rwb-access. DP-08 is not among the patterns applied to this legacy key and the contract-dependency row of the work package does not list `RWB-P4-E1037-CON`, so the check is named in section 12.2 and the omission is carried in the gap row rather than hidden.

### 3. Preconditions

- `RWB-P2-E2035-CON` is published: the three operations, the consumed shapes, the schedule, the error mapping and the contract fakes of this key. It is a same-service contract story and therefore a build dependency (Template and Rules §R5.7 rule 3).
- `RWB-P2-E2033-APP` is done: the case list and the case export of this service exist, and their responses are the ones the four next-action columns are added to.
- RWB-PLT-E1027-CON is published: the local decision-record library and the shared topic `rwb.decision-record.v1` (DP-03).
- RWB-PLT-E1072-CON is published: the embedded Drools kit, with the `RuleResult` and `NoPackageInForce` types and the version-in-force check (DP-04).
- RWB-PLT-E1042-CON and RWB-P3-E1042-CON are published: the parameters contract of rwb-case, which carries the calendar key `rwb.calendar.bank-holidays` (DP-06).
- RWB-PLT-E1043-CON and RWB-P3-E1043-CON are published: the reference-data contract of rwb-case, which carries the role name and role class, the service levels and timers rows and the route-state list with the version in force (DP-07).
- RWB-PLT-E1071-CON is published: the Temporal workflow kit, the `rwb-recovery` namespace and the Schedule conventions of the platform (DP-10).
- RWB-PLT-E1047-CON is published: the naming library, so the Schedule, the task queue and the topic names follow the platform rule (DP-14).
- RWB-PLT-E1044-CON is published: the per-service Flyway sequence of `rwb_integration`, which carries the `job_catalog` row of the new Schedule and the `decision_record` library table (DP-15).
- RWB-PLT-N001-CON is published: the gateway-bff composite route that serves the SCR-03 Case record next action header (DP-19).
- At the wave 2 entry check, the platform edge story and the integration lead agree the composite route path, merge order, call list and the answer when one source is slow, and agree with QA the harness repository, SIT environment, seeded data, per-run evidence format and retention, and pass/fail gate; until then these values are Not specified in the source documents (GAP-0418).
- `RWB-P3-E2042-CON` is published with the `RuleCatalog.row(ruleId, packageVersion)` operation, and package version "RES-2026.12" of code RESTRUCTURE is in force from 2026-12-01 with rule R-RES-04 and rule R-SET-13 (RWB-E2-042; RWB-E1-073).
- `RWB-P3-E1018-CON` and `RWB-P3-E1031-CON` are published: the case facts read and the case list row read that the composition and the four columns use.
- `RWB-P3-E1043-CON` carries the service levels and timers rows (seeded with 5 working days for each state of the route sets in force until the DL22 values are loaded) and the calendar key `rwb.calendar.bank-holidays` with 31 December 2026 and 1 January 2027.
- `RWB-P4-E1037-CON` is published: the authorise contract the read and the fill check the Case record right and the case scope with.
- `RWB-P3-E2035-APP` is the case-side story of this key: it writes the four columns, cancels the exception task on closure and holds the optimistic lock. This story builds against the published rwb-case contract and its fake, so that story does not block (class C).
- The login is the rwb-integration login (DP-02): Not specified in the source documents (GAP-0667; ASM-1177).

### 4. Flow

1. rwb-case: event CASE_PICKED_UP arrives on the case workflow, `EvaluateRules` returns `RuleResult` with rule ID R-RES-04 and package version "RES-2026.12", and the transition calls `POST /api/recovery/integration/v1/next-actions:resolve` with caseId, ruleId, packageVersion and businessDate.
2. rwb-integration: checks that the case exists and is in scope through the rwb-case contract, reads the case facts (state, status, owner, queue, team, closed date), and reads `RuleCatalog.row("R-RES-04", "RES-2026.12")` through the rwb-case catalog contract (DP-04, C dependency).
3. rwb-integration: `TimerSpecResolver` turns the catalog row's `timer_spec` into a due date (BR3); when the spec is "None" or has no fixed duration, it reads the service levels and timers row of the to_state through the reference-data contract (BR4), and skips Saturday, Sunday and the calendar rows (BR8).
4. rwb-integration: `OwnerResolver` sets the owner role from the catalog row, sets `ownerName` and `ownerUserId` when the owner role is the role of the case's queue (BR9), and sets `waiting` when the role class is Customer party or Partner user (BR5).
5. rwb-integration: returns the resolve answer — text, ownerRole, ownerName, ownerUserId, dueDate, waiting, missing, ruleId, ruleVersion — and writes nothing. A missing due date sets `missing` true and leaves the due date empty (BR7).
6. rwb-case: writes `recovery_case.next_action_text`, `next_action_owner_role`, `next_action_due_date`, `next_action_rule_id` and `next_action_waiting` in the same transaction as the move and raises one `NEXT_ACTION_MISSING` task when `missing` is true (`RWB-P3-E2035-APP`).
7. rwb-integration: the `next-action-check` Schedule fires every five minutes and starts `NextActionCheckWorkflow`, which reads the active cases with no next action through the rwb-case contract, reads the latest state change of each case through the decision-log contract of rwb-decision, resolves each case, and calls `POST /api/recovery/integration/v1/cases/{caseId}/next-action` to fill it or raise the same task once.
8. Case owner: opens the case record (SCR-03); the front end calls `GET /api/recovery/integration/v1/cases/{caseId}/next-action` through gateway-bff and shows the action, the owner and the due date, or the waiting text, or the missing message.
9. Team manager: opens the case list (SCR-02) and the case export; the four next-action columns are on each row and an overdue action is marked (BR6).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The rule's timer_spec is None or has no fixed duration | Due date taken from the service levels and timers row of the to_state through the reference-data contract | None | AC5 |
| X2 | No due date can be found from the rule or the table | The resolve answer sets `missing` true with no due date; rwb-case writes the action and raises one task for the team manager | MSG-P2-023 | AC6 |
| X3 | The due date falls on a weekend or a bank holiday | Working days skip Saturday, Sunday and the calendar rows of `rwb.calendar.bank-holidays` | None | AC7 |
| X4 | The case closes | The resolve answer carries no action and no due date; the cancel of the task is rwb-case's (`RWB-P3-E2035-APP`) | None | AC8 |
| X5 | The same transition is resolved twice | The resolve answer is identical and the fill writes once; no second task | None | AC9 |
| X6 | Two transitions on one case commit at the same time | The optimistic lock is the case row's (`RWB-P3-E2035-APP`); the resolve of the committed rule is the one that stays | MSG-GEN-004 | AC10 |
| X7 | An active case from before the flag was switched on has no next action | The `next-action-check` Schedule fills it from the latest state change in the decision log | None | AC11 |
| X8 | The rule's timer is "same day" | Due date is the business date of the move | None | AC12 |
| X9 | The reader's role does not hold Case record R | Refused with 403 before any contract call | MSG-P4-002 | AC13 |
| X10 | No RESTRUCTURE package version is in force on the business date, or the case is outside the reader's scope | The resolve answers `NoPackageInForce` and the fill writes nothing; an out-of-scope case is a 404 | MSG-P3-027, MSG-P4-003 | AC14 |
| X11 | The rwb-case, rwb-access, rwb-decision or reference-data contract does not answer inside the budget | One hop, 2 s timeout and a breaker per downstream; the resolve fails and nothing is written, the read answers 503 and the fill skips the case until the next run | MSG-GEN-006 | AC1, AC11 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds after RWB-P2-E2033-APP against the published contracts of this service and the rwb-case, rwb-access and rwb-decision fakes; the case-side write is another story's and does not block |
| Negotiable | Action text, owner, timer, role class, service level and calendar are data rows; the story fixes only the behaviour and the answer shape |
| Valuable | Every active case states what is owed, by whom and by when, and the measure of cases with no next action is driven to zero |
| Estimable | Three operations, one resolver, one timer resolver, one owner resolver, one read composition, one workflow with three activities and one Schedule |
| Small | Fits one sprint with its tests |
| Testable | Each criterion below has one test with fixed catalog rows, roles and dates, run against the contract fakes |

### 7. Acceptance criteria

```gherkin
Feature: Next action on the case

  Background:
    Given the RESTRUCTURE package version "RES-2026.12" is in force and holds rule R-RES-04, which moves IN_FCR_QUEUE on CASE_PICKED_UP to WITH_FCR_OFFICER with action "Assign the case to a restructuring officer and start the offer clock", owner role RW-RESTRUCT and timer "2 working days"
    Given the same version holds rule R-SET-13, which moves WITH_OPS_SETTLEMENT on SETTLEMENT_BOOKED to AWAITING_PAYMENT with action "Set the payment due date and wait for the money", owner role CU-BORROW and timer "payment due 30 days"
    Given the bank holiday list holds 31 December 2026 and 1 January 2027
    Given the rule catalog mock returns the row of R-RES-04 of version "RES-2026.12" with action "Assign the case to a restructuring officer and start the offer clock", owner role RW-RESTRUCT and timer "2 working days"
    Given the rule catalog mock returns the row of R-SET-13 of version "RES-2026.12" with action "Set the payment due date and wait for the money", owner role CU-BORROW and timer "payment due 30 days"

  Scenario: AC1 Every active case carries a next action (legacy RWB-E2-035 AC1)
    Given case "RW-2026-000401" with status IN_PROGRESS moved by R-RES-04 on 11 December 2026
    Given the rwb-case contract mock returns case "RW-2026-000401" in state WITH_FCR_OFFICER with rule ID R-RES-04, package version "RES-2026.12" and due date 15 December 2026
    When the case is opened
    Then it shows action "Assign the case to a restructuring officer and start the offer clock", owner "Restructuring officer (FCR)" and due date 15 December 2026
    Then the next action names rule R-RES-04 of version "RES-2026.12"

  Scenario: AC2 The routing rules set it (legacy RWB-E2-035 AC2)
    Given case "RW-2026-000402" in state IN_FCR_QUEUE
    Given the rwb-case contract mock returns case "RW-2026-000402" in state IN_FCR_QUEUE with owner role RW-RESTRUCT and queue role RW-RESTRUCT
    When event CASE_PICKED_UP fires R-RES-04 on Friday 11 December 2026
    Then RuleEvaluator.evaluate("RESTRUCTURE", facts, 2026-12-11) returns ruleId "R-RES-04" and packageVersion "RES-2026.12"
    Then POST /api/recovery/integration/v1/next-actions:resolve returns ruleId "R-RES-04", packageVersion "RES-2026.12", ownerRole "RW-RESTRUCT", dueDate 2026-12-15 and waiting false
    Then the case holds next action text from R-RES-04, owner role RW-RESTRUCT, rule ID R-RES-04, rule version "RES-2026.12" and due date Tuesday 15 December 2026
    Then the system writes the values in the same transaction as the move to WITH_FCR_OFFICER

  Scenario: AC3 Waiting is a valid next action (legacy RWB-E2-035 AC3)
    Given case "RW-2026-000403" moved by R-SET-13 on 14 December 2026
    Given the rwb-case contract mock returns case "RW-2026-000403" in state AWAITING_PAYMENT with owner role CU-BORROW
    When the case is opened
    Then the next action reads "Waiting for Customer (borrower): Set the payment due date and wait for the money"
    Then the wait ends on 13 January 2027
    Then next action waiting is true

  Scenario: AC4 It is visible on the list (legacy RWB-E2-035 AC4)
    Given case "RW-2026-000401" with due date 15 December 2026
    Given case "RW-2026-000403" with due date 13 January 2027
    Given the rwb-case contract mock returns the case list rows of "RW-2026-000401" with due date 15 December 2026 and of "RW-2026-000403" with due date 13 January 2027
    When a manager reads the list on 16 December 2026
    Then next action, next action owner and due date are columns
    Then the system marks row "RW-2026-000401" Overdue
    Then the system does not mark row "RW-2026-000403" Overdue

  Scenario: AC5 A rule with no timer takes the state's service level (legacy RWB-E2-035 AC5)
    Given RESTRUCTURE rule R-RES-03 moves the case to BACK_TO_ROUTE_DECISION with owner role RW-CASEOWN and timer "None"
    Given the service levels and timers table holds 5 working days for BACK_TO_ROUTE_DECISION
    Given the reference-data contract mock returns timerSpec "None" for R-RES-03 and a service level of 5 working days for BACK_TO_ROUTE_DECISION
    When R-RES-03 fires on Monday 14 December 2026
    Then its catalog row returns timerSpec "None" through RuleCatalog.row("R-RES-03", "RES-2026.12")
    Then the due date is Monday 21 December 2026
    Then the owner shown is the case owner named on the case

  Scenario: AC6 No due date can be found (legacy RWB-E2-035 AC6)
    Given RESTRUCTURE rule R-DEV-05 moves the case to DEV_WITH_OWNER with owner role RW-LEGAL and timer "deadline driven"
    Given the service levels and timers table holds no row for DEV_WITH_OWNER
    Given the rule catalog mock returns the row of R-DEV-05 with timer "deadline driven" and the reference-data contract mock returns no service level for DEV_WITH_OWNER
    When the rule fires on case "RW-2026-000404" of team "MTG-BKK"
    Then the case holds the action and owner of R-DEV-05 with no due date
    Then the system raises one task NEXT_ACTION_MISSING on the exception queue for role RW-TEAMMGR of team "MTG-BKK"
    Then the case record shows warning MSG-P2-023

  Scenario: AC7 Working days skip weekends and bank holidays (legacy RWB-E2-035 AC7)
    Given the calendar rows of rwb.calendar.bank-holidays hold 31 December 2026 and 1 January 2027
    When R-RES-04 fires on Wednesday 30 December 2026
    Then the due date is Tuesday 5 January 2027

  Scenario: AC8 A closed case has no next action (legacy RWB-E2-035 AC8)
    Given case "RW-2026-000404" with task NEXT_ACTION_MISSING open
    Given the rwb-case contract mock returns case "RW-2026-000404" with closed date 2026-12-18 and closure reason SETTLED
    When the case closes with closure reason SETTLED
    Then the next action fields are empty
    Then the system cancels the task
    Then the case is not in the list of active cases with no next action

  Scenario: AC9 A repeated transition changes nothing (legacy RWB-E2-035 AC9)
    Given case "RW-2026-000402" was moved by R-RES-04 on 11 December 2026 with decision record "DLE-SYN-0402"
    Given the decision-record contract mock returns decision record "DLE-SYN-0402" with rule ID R-RES-04 and version "RES-2026.12" as the latest state change
    When the same transition with "DLE-SYN-0402" is processed again
    Then the next action and due date are unchanged
    Then the system raises no task

  Scenario: AC10 Two transitions at the same time (legacy RWB-E2-035 AC10)
    Given case "RW-2026-000405" at version 7
    Given the rwb-case contract mock holds case "RW-2026-000405" at version 7
    When two transitions commit against version 7 at the same time
    Then one commits and the other is refused with MSG-GEN-004 and retried against version 8
    Then the next action is that of the rule committed last

  Scenario: AC11 Cases open before the switch-on are filled (legacy RWB-E2-035 AC11)
    Given 3 active cases with no next action, each with a state change in the decision record by R-RES-04 on 11 December 2026
    Given the rwb-case contract mock returns those 3 active cases with no next action, and the decision-record contract mock returns R-RES-04 of version "RES-2026.12" as their latest state change
    When JOB-05 runs on 14 December 2026
    Then each of the 3 cases holds the next action of R-RES-04 with due date 15 December 2026
    Then each reads the text from RuleCatalog.row("R-RES-04", "RES-2026.12")

  Scenario: AC12 A same day timer (legacy RWB-E2-035 AC12)
    Given RESTRUCTURE rule R-RES-07 with timer "same day" moves case "RW-2026-000406" on 14 December 2026
    Given the rule catalog mock returns the row of R-RES-07 with timer "same day"
    When the next action is set from that rule
    Then the due date is 14 December 2026

  Scenario: AC13 A role without Case record R (legacy RWB-E2-035 AC13)
    Given user "U-REF-01" holds RW-REFADM and no role with Case record R
    Given the rwb-access contract mock refuses Case record R for RW-REFADM
    When they call GET /api/recovery/integration/v1/cases/{caseId}/next-action
    Then the response is 403 with MSG-P4-002
    Then no next action data is returned

  Scenario: AC14 No RESTRUCTURE version in force (legacy RWB-E2-035 AC14)
    Given no RESTRUCTURE package version is in force on 2027-01-04
    When event CASE_PICKED_UP fires for case "RW-2026-000407" on 2027-01-04
    Then RuleEvaluator.evaluate("RESTRUCTURE", facts, 2027-01-04) throws NoPackageInForce
    Then the move is refused with MSG-P3-027 for the package in force check
    Then the case keeps its state and holds no next action from this move
    Then POST /api/recovery/integration/v1/next-actions:resolve answers 409 with MSG-P3-027 for the same package in force check

  Scenario: AC15 The resolve writes nothing and reads only the catalog row (readiness, BR12 and BR13) (new, D-RCV-60)
    Given case "RW-2026-000402" in state IN_FCR_QUEUE
    When the resolve is called for case "RW-2026-000402" on Friday 11 December 2026 with event CASE_PICKED_UP
    Then the answer carries ruleId "R-RES-04" and packageVersion "RES-2026.12"
    Then no column of recovery_case is written
    Then RuleCatalog.row("R-RES-04", "RES-2026.12") is the only rule read; no workbook, generated DRL or rule table is read

  Scenario: AC16 A replay with the same idempotency key changes nothing (readiness) (new, D-RCV-60)
    Given case "RW-2026-000402" was resolved on 11 December 2026 with rule R-RES-04 and version "RES-2026.12"
    When the same resolve call with the same idempotency key is sent again
    Then the answer is the same as the first answer
    Then no column of recovery_case is written and no task is raised

  Scenario: AC17 A consumed call fails or does not answer (readiness) (new, D-RCV-60)
    Given the rule catalog mock does not answer the RuleCatalog.row call for R-RES-04 of version "RES-2026.12"
    When the resolve is called for case "RW-2026-000402" on Friday 11 December 2026
    Then no ruleId, owner or due date is returned from a partial result
    Then the answer is the failure of the consumed call with MSG-GEN-006
```

The fourteen criteria AC1 to AC14 are the legacy criteria of RWB-E2-035, copied with their values and their dates. AC15 to AC17 are added at readiness and have no legacy source. The legacy path of AC13 becomes `GET /api/recovery/integration/v1/cases/{caseId}/next-action` under DP-13: the monolith base of the legacy story is replaced by the base of this service, and no other value of the criterion changes. The mock Givens name the contract that answers where a legacy statement crossed a module boundary: the case facts come from the rwb-case fake, the catalog row from the catalog fake, the role class, service level and calendar rows from the reference-data fake, the state change from the decision-record fake and the role check from the rwb-access fake.

Four statements of the legacy criteria are the case side's, not this story's, and they are proved in `RWB-P3-E2035-APP`: the write of the four fields in the same transaction as the move (AC2), the cancel of the `NEXT_ACTION_MISSING` task on closure (AC8), the optimistic lock and its retry (AC10) and the refusal of the move when no version is in force (AC14). What this story proves is the resolve answer and the same rwb-case contract call in each of those four: the answer carries the rule, the version, the owner and the due date; the answer of a closed case carries no action; the resolve of the committed rule is the one that stays; and the resolve refuses with `NoPackageInForce` and MSG-P3-027. AC11 is named by its legacy job name JOB-05; in the target the fill is the `next-action-check` Schedule of section 12.6, which runs every five minutes and does the same work (see ASM-1180).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | On every move, the next action text, the owner role and the rule ID come from the catalog row of the firing rule: `RuleCatalog.row(ruleId, packageVersion)` returns action_text, owner_role and timer_spec, and the row is read through the operation published in RWB-P3-E2042-CON | FEAT-CWC-28; REQ-WKM-013; D-RCV-36 T6 |
| BR2 | The next action is never entered by a person | REQ-WKM-013 |
| BR3 | timer_spec "n working days" adds n working days; "n days" with any label before it adds n calendar days, so "payment due 30 days" adds 30 calendar days; "same day", "Same day" and "immediate" give the date of the move; "next working day" adds 1 working day | rule_row.timer_spec through RuleCatalog |
| BR4 | Any other timer_spec, including "None" and "deadline driven", takes the time for the to_state from the service levels and timers rows through the reference-data contract | DL22; DP-07 |
| BR5 | The next action is a wait when the owner role is of class Customer party or Partner user; the text starts "Waiting for {owner}:" | role.role_class through the reference-data contract |
| BR6 | A next action is overdue when its due date is earlier than today and the case is not closed | REQ-WKM-012 |
| BR7 | An active case with no due date or no next action raises one NEXT_ACTION_MISSING task to the team manager; the fill raises it once, and the task is written through the rwb-case contract | REQ-WKM-016 |
| BR8 | Working days are Monday to Friday, excluding the dates of the calendar key rwb.calendar.bank-holidays, read through the parameters contract | Configuration key rwb.calendar.bank-holidays; DP-06 |
| BR9 | When the owner role is the role of the case's queue, the owner shown is the case owner; otherwise the role name | queue.role_code of the case, through the rwb-case contract |
| BR10 | The rule version is the package version label of the `RuleResult`, and the next action records the version of the move that set it; a later version does not rewrite an action already set | D-RCV-36 T5, T7; R-UNI-38 |
| BR11 | No RESTRUCTURE version in force is a refusal (`NoPackageInForce` from the embedded kit), never a default move and never an empty next action | D-RCV-36 T3; R-UNI-41 |
| BR12 | rwb-case is the only writer of `recovery_case`; this service resolves and serves and never writes a case column, and the resolve operation is side-effect free | Arch v5 slide 41; DP-01; RWB-P3-E2035-APP |
| BR13 | The rule catalog is read only through `RuleCatalog.row(ruleId, packageVersion)`; no workbook, no generated DRL and no rule table is read, and no second rule engine runs | D-RCV-36 T3, T5, T6; DP-04 |
| BR14 | The latest state change of a case is its newest decision record that carries a rule ID and a rule version; no decision code or final call is tested until LOV-DECISION marks the state-change codes | DF-DEC-003; DF-DEC-012; FSD P7 A2.3 |

### 9. State transitions

None. This story changes no case status and writes no case row: it resolves the next action, serves it and fills it through the rwb-case contract. The case status, the four next-action columns and the `NEXT_ACTION_MISSING` task status (OPEN to CANCELED) are rwb-case's writes in `RWB-P3-E2035-APP`, in the same transaction as the move.

The only record lifecycles this story holds are its own: the `next-action-check` Schedule run (IDLE to RUNNING to COMPLETE or FAILED), and the resolve answer, which is stateless and stored nowhere.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| SY-RULES, the rule evaluation activity of rwb-case | Returns the `RuleResult` (rule ID and package version) that this service resolves; it never resolves the action itself |
| SY-CASEWF, case workflow module | Writes the next action fields and the exception task through the rwb-case contract (Case record U, Queue and allocation C) and owns the transaction |
| RW-CASEOWN, case owner | Reads the next action of cases in scope (Case record R) |
| RW-TEAMMGR, team manager | Reads the list and works NEXT_ACTION_MISSING tasks on the exception queue |
| RW-COE, center of excellence analyst | Owns the action, owner and timer columns of the rule rows (Rules and parameters CRUD) |
| RW-REFADM, reference data administrator | Loads the service levels and timers rows and the calendar rows of `rwb.calendar.bank-holidays` |
| No approval applies | The story takes no decision |

The service runs as the rwb-integration login (DP-02). The login name is Not specified in the source documents (GAP-0667; ASM-1177).

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-049 | recovery_case | next_action_text | Read here through the rwb-case contract; written by rwb-case (`RWB-P3-E2035-APP`) |
| DF-CAS-050 | recovery_case | next_action_owner_role | Read here; written by rwb-case |
| DF-CAS-051 | recovery_case | next_action_due_date | Read here; written by rwb-case |
| DF-CAS-052 | recovery_case | next_action_rule_id | Read here; written by rwb-case |
| DF-CAS-053 | recovery_case | next_action_waiting | Read here; written by rwb-case |
| DF-CAS-005 | recovery_case | status | Read through the rwb-case contract |
| DF-CAS-007 | recovery_case | route_state | Read through the rwb-case contract |
| DF-CAS-009 | recovery_case | owner_user_id | Read through the rwb-case contract |
| DF-CAS-010 | recovery_case | queue_id | Read through the rwb-case contract |
| DF-CAS-011 | recovery_case | team_code | Read through the rwb-case contract |
| DF-CAS-022 | recovery_case | closed_date | Read through the rwb-case contract |
| DF-WRK-005 | queue | role_code | Read through the rwb-case contract |
| DF-WRK-017 to DF-WRK-026 | task | all fields | Read here through the rwb-case contract; written by rwb-case on the fill |
| DF-REF-002, DF-REF-003, DF-REF-008, DF-REF-010, DF-REF-011, DF-REF-296, DF-REF-297, DF-REF-298 | rule_row | rule_id, rule_version, action_text, owner_role, timer_spec, package_version_id, drools_rule_name, outputs | Read through `RuleCatalog.row(ruleId, packageVersion)` only |
| DF-REF-036 | role | role_name | Read through the reference-data contract |
| DF-REF-037 | role | role_class | Read through the reference-data contract |
| DF-DEC-004 | decision_log_entry | rule_id | Read through the decision-log contract of rwb-decision |
| DF-DEC-005 | decision_log_entry | rule_version | Read through the decision-log contract of rwb-decision |
| DF-OPS-225, DF-OPS-226, DF-OPS-227, DF-OPS-228 | job_catalog (rwb_integration) | job_id, job_name, owner_role, schedule_text | Write: the row of the `next-action-check` Schedule |
| DF-DEC-001 to DF-DEC-018 | decision_record (library table in rwb_integration) | all fields | Write by the local decision-record library on a fill (`NextActionCheckWorkflow`) |

The rule row is read only through `RuleCatalog.row(ruleId, packageVersion)`; this story reads no workbook and no drl_source. Field IDs are those in the Logical Data Model and Data Dictionary. No case row, no task row, no role row and no rule row is copied into `rwb_integration` (DP-01, BR12), and the JSON field names of the consumed contracts are Not specified in the source documents (GAP-0667; ASM-1179).

### 12. Contract

#### 12.1 REST operations provided

Base `/api/recovery/integration/v1`; owner rwb-integration (P2).

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| POST | `/next-actions:resolve` | Side-effect-free resolution: input caseId, ruleId, packageVersion, businessDate; answer text, ownerRole, ownerName, ownerUserId (when BR9 names the case owner), dueDate, waiting, missing, ruleId, ruleVersion. Consumed by the case transition of `RWB-P3-E2035-APP` | Case record R, scope applied, through the rwb-access authorise contract | Not applicable: the call writes nothing, and the same input answers the same output |
| GET | `/cases/{caseId}/next-action` | The next action of a case for SCR-03: text, ownerRole, ownerName, ownerUserId, dueDate, waiting, overdue, missing, ruleId, ruleVersion. Composed from the case facts, the latest state change, the catalog row, the role class, the service level and the calendar rows | Case record R, scope applied | Not applicable: read only |
| POST | `/cases/{caseId}/next-action` | The fill of the `next-action-check` Schedule: resolves the case and writes the four values through the rwb-case contract, or raises one `NEXT_ACTION_MISSING` task; records its own decision record first | Case record U for the service identity, scope applied | `Idempotency-Key` on the POST; a case that already holds a next action is left unchanged and answers 200 with what it holds |

The Ownership Map keeps `GET /cases/{caseId}/next-action` with P3, and this story serves it from rwb-integration under its own base (DP-13); the reconciliation and the conflict are carried in GAP-0667 and ASM-1178.

Two responses of `RWB-P2-E2033-APP` change: each Case item of `GET /cases` and each row of `GET /cases/export` gains `nextAction`, `nextActionOwner`, `nextActionDueDate` and `nextActionOverdue`, resolved by this story from the same four fields, with the authorization and the errors left as that story set them. The response field names of the three operations and of the two changed responses are Not specified in the source documents (GAP-0667; ASM-1182).

Errors: 401 no session (MSG-P4-001); 403 no Case record R (MSG-P4-002); 404 unknown case or case outside the scope (MSG-P4-003); 409 no package version in force (MSG-P3-027) or a case changed by someone else (MSG-GEN-004); 422 a missing required input (MSG-GEN-001); 503 a consumed contract does not answer inside the budget (MSG-GEN-006).

#### 12.2 REST operations consumed

One hop per call, no chaining; 2 s timeout and a breaker per downstream (DP-11).

| Method | Path | Service | Used for | Timeout |
|---|---|---|---|---|
| GET | `/api/recovery/case/v1/cases/{caseId}` | rwb-case (P3) | The case facts: state, status, owner, queue, queue role, team, closed date | One hop, 2 s, breaker |
| GET | `/api/recovery/case/v1/cases` | rwb-case (P3) | The active cases with no next action and the case list rows that carry the four columns | One hop, 2 s, breaker |
| GET | `/api/recovery/decision/v1/rule-catalog/{ruleId}?packageVersion=` | rwb-decision (P7), through the `RuleCatalog.row` operation published in RWB-P3-E2042-CON | action_text, owner_role, timer_spec and outputs of one rule row | One hop, 2 s, cached |
| GET | `/api/recovery/case/v1/reference-data/role-classes/{roleCode}` | rwb-case (P3) | role_name and role_class of the owner role (BR5, BR9) | One hop, 2 s, cached |
| GET | `/api/recovery/case/v1/reference-data/service-levels/{toState}` | rwb-case (P3) | The service levels and timers row of the to_state (BR4) | One hop, 2 s, cached |
| GET | `/api/recovery/case/v1/parameters/rwb.calendar.bank-holidays` | rwb-case (P3) | The bank holiday list (BR8) | One hop, 2 s, cached |
| GET | `/api/recovery/decision/v1/decision-log?caseId=&latestStateChange=true` | rwb-decision (P7) | The latest state change of a case: rule ID and rule version, for the fill (AC9, AC11) | One hop, 2 s |
| POST | `/api/recovery/access/v1/authorise` | rwb-access (P4) | Case record R or U and the scope of the case, cached per session by the guard library | One hop, 2 s, cached |
| POST | Not specified in the source documents (GAP-0667; ASM-1179) | rwb-case (P3) | The write of the four next-action fields and the raise or cancel of the `NEXT_ACTION_MISSING` task, called by the fill | One hop, 2 s |

The catalog path is the one the rwb-decision contract publishes and the operation name is `RuleCatalog.row(ruleId, packageVersion)` as published in RWB-P3-E2042-CON. The reference-data and parameter paths are named by the reference tables and the configuration key of the legacy story, not by a path in a source: the operation shapes are the P3 contract's to fix, and the paths above are the ones this story builds against until that baseline is published. The write path of the fill is the rwb-case case-record contract of `RWB-P3-E2035-APP`, and its exact path and payload are Not specified in the source documents (GAP-0667; ASM-1179).

#### 12.3 Events published

None of its own. This story declares no event type and publishes on no topic of its own: `rwb.integration.events.v1` carries FileDelivered and FileFailed, which belong to the file stories of this service. The fill writes its own decision record through the local decision-record library (DP-03), and the library publishes `rwb.decision-record.DecisionRecorded.v1` on `rwb.decision-record.v1` from the same transaction; the record of the move itself is rwb-case's, written by its own library call in `RWB-P3-E2035-APP`.

#### 12.4 Events consumed

None. The resolve is call-driven: the case transition calls it inside its own request, the read is called by the case record screen through gateway-bff, and the fill is started by the Schedule. The latest state change is read from the decision-log contract at the time of the fill, so the service subscribes to no topic and holds no inbox.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| NextActionCheckWorkflow | Workflow, started by the `next-action-check` Schedule | `rwb-integration` | Input: business date, run window. Output: counts of filled, unchanged, missing and failed cases |
| findCasesWithoutNextAction | Activity | `rwb-integration` | Input: business date. Output: the active cases with no next action, read through the rwb-case contract |
| resolveNextAction | Activity | `rwb-integration` | Input: caseId, ruleId, packageVersion, business date. Output: the resolve answer; the workflow-kit types `RuleResult` and `NoPackageInForce` are used and no rule engine is run |
| fillNextAction | Activity | `rwb-integration` | Input: caseId and the resolve answer. Output: filled, unchanged or missing; calls the rwb-case contract in one call and raises at most one task per case |

The three activities carry the retry policy of the workflow kit, and `NoPackageInForce` is a non-retryable outcome of `resolveNextAction`.

#### 12.6 Schedules

| Schedule | Cadence | Documented fields | Legacy reference |
|---|---|---|---|
| `next-action-check` | Every 5 minutes | Schedule ID `next-action-check`, overlap policy SKIP, catch-up window, business date and run window input, the workflow `NextActionCheckWorkflow` | JOB-05 Timer check, the next action step |

The cadence of 5 minutes is the legacy cadence; the catch-up window and the overlap window are Not specified in the source documents (GAP-0667; ASM-1184) and are values of the deployment (`RWB-P2-E2035-OPS`).

#### 12.7 Tables owned

| Table | Schema | Owner | Use in this story |
|---|---|---|---|
| job_catalog | rwb_integration | P2 (Ownership Map; TSD P2 v3 T3.1) | One row for the `next-action-check` Schedule: job_id, job_name, owner_role, schedule_text, runbook_path, expected_minutes, alert_after_minutes |
| decision_record | rwb_integration | PLT library, created in rwb_integration (DP-03) | The local decision record of a fill, written by the library in the same transaction as the record |

No case table, no task table, no role table and no rule table is owned or read directly: the case facts, the task write, the role rows and the rule row come through their owners' contracts (DP-01, BR12). The service holds no ACE view and no copy of a case field.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-case WireMock | The P3 contract | Case `RW-2026-000401` in WITH_FCR_OFFICER with due date 2026-12-15; `RW-2026-000402` in IN_FCR_QUEUE at version 7 and 8; `RW-2026-000403` in AWAITING_PAYMENT with a wait to 2027-01-13; `RW-2026-000404` closed with reason SETTLED; `RW-2026-000405` at version 7 with a 409 version refusal; three active cases with no next action; the case list rows of AC4; the task write accepted and refused once |
| Rule catalog WireMock (published shapes of RWB-P3-E2042-CON) | The `RuleCatalog.row` operation | R-RES-04, R-SET-13, R-RES-03 with timer "None", R-DEV-05 with timer "deadline driven" and R-RES-07 with timer "same day", all of version "RES-2026.12"; one 404 for an unknown rule ID; one `NoPackageInForce` answer for 2027-01-04 |
| rwb-case reference-data stub | The P3 reference-data and parameter contract | role_class PARTNER_USER for CU-BORROW and INTERNAL for RW-RESTRUCT and RW-CASEOWN; 5 working days for BACK_TO_ROUTE_DECISION; no row for DEV_WITH_OWNER; the calendar rows 2026-12-31 and 2027-01-01 |
| rwb-decision WireMock | The P7 decision-log contract | Latest state change R-RES-04 of version "RES-2026.12" for `RW-2026-000402` with entry DLE-SYN-0402 and for the three cases of AC11; an empty answer for a case with no state change |
| rwb-access WireMock | The P4 contract | Case record R granted to RW-CASEOWN and RW-TEAMMGR in scope; refused for RW-REFADM with MSG-P4-002; a case out of scope answered 404 with MSG-P4-003 |
| gateway-bff composite route stub | The edge route of RWB-PLT-N001-CON | The SCR-03 next action header route and the merged screen model (DP-19) |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 3 provided, 8 named paths consumed | Resolve, read and fill provided; the case facts, the case list, the catalog row, the role class, the service level, the calendar, the latest state change, the authorise check and the case write consumed; one hop, 2 s timeout, breaker per downstream |
| Kafka | None declared; 1 published by the decision-record library | `rwb.decision-record.v1` carries DecisionRecorded on the service's behalf on a fill (DP-03) |
| Temporal | 1 workflow, 3 activities, 1 Schedule | NextActionCheckWorkflow, findCasesWithoutNextAction, resolveNextAction, fillNextAction; `next-action-check` every 5 minutes |
| File | None | This story reads and writes no file |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.integration`, module `nextaction`, Java package `th.co.scb.ace.workbench.recovery.integration.nextaction`; front end `src/modules/recovery/caserecord/NextActionPanel.tsx`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables; the case facts and the task write come through the rwb-case contract | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1`; here the record of a fill is the service's own and the record of a move is rwb-case's | H RWB-PLT-E1027-CON |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit types and the catalog read through rwb-decision's registry; the evaluation itself stays with the case workflow, so no second rule engine runs | H RWB-PLT-E1072-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | No ACE read in this story: the case facts come from rwb-case and no view is read | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case for the calendar key | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case for the role class, the service level and the calendar rows | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule `next-action-check` and the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/integration/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.integration.events.v1`; the naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in `rwb_integration`: the `job_catalog` row and the library table | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route for the SCR-03 header | H RWB-PLT-N001-CON |

DP-04 applies as a prohibition as well as a rule: the kit's `RuleResult` and `NoPackageInForce` types and the version-in-force check are used, and the package is never evaluated a second time in this service (ASM-1185). DP-03 applies on both sides of the seam: this service writes the record of its fill, and rwb-case writes the record of the move.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| NextActionController | Controller | The three operations; input validation; the problem mapping of section 14 |
| NextActionResolveService | Service | BR1, BR5, BR7, BR9 and BR10: reads the catalog row, resolves the owner and the waiting flag, and assembles the resolve answer without writing |
| TimerSpecResolver | Service | BR3, BR4 and BR8: pure functions over the timer spec, the service level and the calendar rows |
| OwnerResolver | Service | BR5 and BR9: the owner role, the owner name and the owner user from the case queue role and the role class |
| NextActionReadService | Service | The read of SCR-03: case facts, latest state change, catalog row, role rows and the overdue marker |
| NextActionFillService | Service | The fill: finds the cases, resolves each one, records the decision, calls the rwb-case write, raises at most one task |
| RuleCatalogClient | Client | Calls `RuleCatalog.row(ruleId, packageVersion)` and caches a row per rule and version (DP-04) |
| CaseClient | Client | Calls the rwb-case contract for the case facts, the case list and the next-action write |
| ReferenceDataClient | Client | Calls the reference-data and parameter contract for the role class, the service level and the calendar rows (DP-07, DP-06) |
| DecisionLogClient | Client | Calls the decision-log contract for the latest state change of a case (DP-03) |
| AccessCheckClient | Client | Calls the rwb-access authorise contract for Case record R or U and the scope, cached by the guard library |
| DecisionRecordWriter | Library client | Writes the local decision record of a fill and lets the library publish DecisionRecorded; a failure fails the fill and nothing is written |
| ScheduleRunRepository | Repository | Reads and writes the `job_catalog` row and the run outcome of the Schedule |
| NextActionPanel | React component | SCR-03's header: the action, the owner, the due date, the rule and version, the waiting text, the overdue marker and the missing message |

**Database and migrations**

- One migration in the `rwb_integration` sequence adds the `job_catalog` row of `next-action-check` and the library table `decision_record` (DP-15).
- No case column, no case table and no copy of a case, role or rule row lives in `rwb_integration` (DP-01, BR12).
- The service connects with its own login holding grants on `rwb_integration` only, and no grant on `recovery` or on another `rwb_*` schema (DP-02). The login name is Not specified in the source documents (GAP-0667; ASM-1177).

**Configuration and reference data**

- Package version "RES-2026.12" and the rows R-RES-04, R-SET-13, R-RES-03, R-DEV-05 and R-RES-07 are the legacy values of this story and are carried unchanged; they are rows of the RESTRUCTURE registry in rwb-decision and are loaded by RWB-E2-042 and RWB-P7-E2035-APP (ASM-1181).
- The service levels and timers rows are seeded with 5 working days per state until the DL22 values are loaded, and the calendar rows 2026-12-31 and 2027-01-01 are loaded under `rwb.calendar.bank-holidays` (RW-REFADM).
- The role names and classes are rwb-access and rwb-case reference rows; the role class is read through the reference-data contract (BR5), and the name of its answer field is Not specified in the source documents (GAP-0734); no role code and no class value is written in code (DP-07).
- The legacy flag `rwb.casewf.next-action` is kept as the legacy reference of the switch; the switch itself is a feature flag of the platform flag library (ASM-1186).

**Build steps**

1. Publish the resolve operation with the timer resolver and the owner resolver, against the catalog, reference-data and case fakes; AC1, AC2, AC3, AC5, AC7, AC12.
2. Add the missing path: the flag, the task raise and the answer that carries no due date; AC6.
3. Add the read operation and its composition, with the overdue marker and the closed-case answer; AC1, AC4, AC8.
4. Add the four columns to the case list and the export responses of RWB-P2-E2033-APP; AC4.
5. Write NextActionCheckWorkflow and its three activities, with the idempotent fill and the one-task rule; AC9, AC11.
6. Register the `next-action-check` Schedule with its `job_catalog` row and its overlap and catch-up values.
7. Add the access test, the no-version test and the contract test of the three operations; AC13, AC14.
8. Run the contract-fake suite of section 12.8 so the story builds before rwb-case, rwb-access and rwb-decision land.

**Feature switch.** `rwb.casewf.next-action`. Off: the resolve answers 404 with MSG-GEN-006 for a caller outside the release, the fill does not run, the four columns are hidden and the panel is not served. The flag value comes from the platform flag library and is never a value of this service.

**Done when.** The tests in section 16 pass and the report of active cases with no next action reads zero on the SIT data set after the `next-action-check` Schedule has run.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P2-023 | The case has no next action or no due date | This case has no next action. It is on the exception list for {team}. |
| MSG-P3-027 | No RESTRUCTURE version is in force | The rule version was refused at the {check} check: {detail}. |
| MSG-GEN-004 | A case changed between the read and the write, or a fill repeats a case already filled | Someone else changed this record. Reload it to see their change. |
| MSG-P4-002 | Role lacks Case record R | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | Case outside the reader's scope | This case is not in your scope. |
| MSG-GEN-001 | A required input of an operation is missing | Enter {field}. |
| MSG-GEN-006 | A consumed contract does not answer inside the budget, or the flag is off | The service is not available. Try again in a few minutes. |
| MSG-P4-001 | Not specified in the source documents (DOR-RWB-P2-E2035-APP-9) | Not specified in the source documents (DOR-RWB-P2-E2035-APP-9) |

For MSG-P3-027 in this story {check} is "package in force" and {detail} names the package code RESTRUCTURE and the business date only. The texts of MSG-P2-023, MSG-P3-027, MSG-GEN-004, MSG-P4-002 and MSG-P4-003 are the legacy texts of RWB-E2-035 and are copied unchanged; MSG-GEN-001 and MSG-GEN-006 are the platform texts and are not restated here. Thai text for each message follows decision DL10.

### 15. Screens and states

SCR-03 Case record, states Read only, Editable and On hold: the header shows the next action, its owner, its due date and the rule ID with its version; a wait shows "Waiting for {owner}" and the wait end date; an overdue action carries the text "Overdue"; a missing action shows MSG-P2-023. The header is served by the gateway-bff composite route, which calls this service once and merges the answer into the case screen model (DP-19). States: loading as in Screen Specifications v1, section SCR-03; empty: a case with no next action shows MSG-P2-023; error: a consumed contract that does not answer inside the budget shows MSG-GEN-006; no access: MSG-P4-002 for a role without Case record R and MSG-P4-003 for a case outside the reader's scope.

SCR-02 Case list: the next action, next action owner and due date columns with the overdue marker, on the rows of the case list of RWB-P2-E2033-APP. States: empty and loading as in Screen Specifications v1, section SCR-02; error: a consumed contract that does not answer inside the budget shows MSG-GEN-006; no access: MSG-P4-002 for a role without Case record R, and a case outside the reader's scope is answered with MSG-P4-003. SCR-09 Exception queue: the team manager sees the `NEXT_ACTION_MISSING` tasks rwb-case raised. States: loading as in Screen Specifications v1, section SCR-09; no access: MSG-P4-002, as in the message table of that section; empty and error: Not specified in the source documents (CG-ALL-3272). The field-level layout, the masking and the composite route of the header are Not specified in the source documents (GAP-0667; ASM-1182).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-035-01 | AC1, BR1, BR9, BR10 | End to end | Case moved by R-RES-04 on 11 December 2026 |
| TC-E2-035-02 | AC2, BR1, BR2, BR3, BR10 | End to end | CASE_PICKED_UP on Friday 11 December 2026 |
| TC-E2-035-03 | AC3, BR5 | End to end | Case moved by R-SET-13 on 14 December 2026 |
| TC-E2-035-04 | AC4, BR6 | End to end | Two cases read on 16 December 2026 |
| TC-E2-035-05 | AC5, BR4, BR9 | End to end | R-RES-03 with timer None; row of 5 working days |
| TC-E2-035-06 | AC6, BR7 | End to end | R-DEV-05 with timer "deadline driven" and no row |
| TC-E2-035-07 | AC7, BR8 | End to end | Move on 30 December 2026 with two holidays |
| TC-E2-035-08 | AC8 | End to end | Case with an open NEXT_ACTION_MISSING task closes |
| TC-E2-035-09 | AC9 | End to end | Same transition processed twice |
| TC-E2-035-10 | AC10 | End to end | Two transitions against version 7 |
| TC-E2-035-11 | AC11 | End to end | Three cases with no next action before the fill run |
| TC-E2-035-12 | AC12, BR3 | End to end | Rule with timer "same day" |
| TC-E2-035-13 | AC13, Access | Component | RW-REFADM reads the next action; refused with MSG-P4-002 |
| TC-E2-035-14 | AC14, BR11 | End to end | No RESTRUCTURE version in force on 2027-01-04; NoPackageInForce and MSG-P3-027 |
| TC-E2-035-15 | §12 operations, events and activities | Component | Each operation, event and activity of section 12 against its published contract |
| TC-E2-035-16 | §12.7 tables | Component | Boundary values of each table of section 12.7; values Not specified in the source documents (DOR-RWB-P2-E2035-APP-12) |
| TC-E2-035-17 | AC15, BR12, BR13 | Component | Resolve call on RW-2026-000402 with a write counter and a rule read counter |
| TC-E2-035-18 | AC16, BR12 | Component | Same resolve call sent twice with the same idempotency key |
| TC-E2-035-19 | AC17 | Component | Rule catalog does not answer for R-RES-04 of RES-2026.12 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. Legacy levels map System to End to end and Access to Component. The case-side statements of TC-E2-035-02, -08, -10 and -14 are proved in RWB-P3-E2035-APP; here the same test cases run against the three operations of this story.

### 17. Guardrails

- No business value in code: action text, owner role, timer, role class, service levels, calendar and route states are data rows of the catalog, the reference tables and the parameters.
- No personal data in logs, tests, workflow history or prompts: the next action holds rule text and role codes only, and the case is carried by its case ID.
- No read of another service's tables and no ACE view: the case facts, the task write and the catalog row come only through the rwb-case contract, the role and service level rows only through the reference-data contract, the calendar only through the parameters contract and the state change only through the decision-log contract (DP-01, DP-05).
- The parser recognizes timer patterns; it never holds a duration for a named state.
- The rule row is read only through `RuleCatalog.row(ruleId, packageVersion)`; no workbook, no drl_source and no rule table is read by this story (BR13).
- One evaluator: the move is evaluated by the case workflow's `EvaluateRules` activity, and this service resolves the fired rule without running a second rule engine.
- rwb-case is the only writer of the case row and of the exception task; the resolve operation writes nothing (BR12).
- The Schedule carries the overlap policy SKIP and raises at most one open `NEXT_ACTION_MISSING` task per case.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-WKM-012 | Every open case carries one next action with owner and due date | Business Requirements Epic 2, section 3.2 | FEAT-CWC-27 | 06 to 10 Recovery case processes | R-RES-04, R-SET-13 | TC-E2-035-01, TC-E2-035-03, TC-E2-035-04, TC-E2-035-08, TC-E2-035-13 |
| REQ-WKM-013 | The next action comes from the rule that moved the case | Business Requirements Epic 2, section 3.2 | FEAT-CWC-28 | 06 to 10 Recovery case processes | R-RES-03, R-RES-04, R-SET-13 | TC-E2-035-02, TC-E2-035-05, TC-E2-035-07, TC-E2-035-09, TC-E2-035-10, TC-E2-035-12, TC-E2-035-14 |
| REQ-WKM-016 | A case with no next action is reported as an exception | Business Requirements Epic 2, section 3.2 | FEAT-CWC-27 | 06 to 10 Recovery case processes | R-DEV-05 | TC-E2-035-06, TC-E2-035-11 |
| REQ-WKM-014 | Next action visible on the case record and every queue view | Business Requirements Epic 2, section 3.2 | FEAT-CWC-27, FEAT-CWC-28 | 06 to 10 Recovery case processes | None | TC-E2-035-01 |
| REQ-WKM-015 | An overdue next action escalates like a service level breach | Business Requirements Epic 2, section 3.2 | FEAT-CWC-27, FEAT-CWC-28 | 06 to 10 Recovery case processes | None | TC-E2-035-01 |

### 19. Out of scope

- The write of the four case columns, the `NEXT_ACTION_MISSING` task lifecycle and the optimistic lock: rwb-case's, in RWB-P3-E2035-APP.
- The registry rows of the RESTRUCTURE package, the rule catalog and the central decision ledger: rwb-decision's (RWB-P7-E2035-APP; ASM-0069).
- The role rows, the role classes and the authorise check: rwb-access's (RWB-P4-E2035-APP).
- The service levels and timers rows, the calendar rows and the reference versions: rwb-case's reference-data stories (RWB-P3-E1043-CON, RWB-P3-E1042-CON).
- The deployment of the operations and of the Schedule, the dashboards, the alerts and the runbook (RWB-P2-E2035-OPS).
- The escalation when a next action passes its due date: RWB-E2-015 (REQ-WKM-015).
- The next action column in the queue view screens: RWB-E2-011.
- The values of the service levels per state: DL22.
- Loading the route-set rule rows beyond allocation, assignment and transfer: DL24; the RESTRUCTURE rows are RWB-E2-042.
- The RESTRUCTURE package checks, scenarios and approval (RWB-E1-073).
- Temporal durable timers inside the case workflow that would replace the fill Schedule (ADR-011, Epic 3).
- The real cross-service proof of the journey (RWB-ITG-E2035-ITG).
