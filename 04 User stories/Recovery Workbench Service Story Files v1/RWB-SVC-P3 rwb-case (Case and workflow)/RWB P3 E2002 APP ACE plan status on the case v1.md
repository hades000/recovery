# RWB-P3-E2002-APP ACE plan status on the case v1

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P3-E2002-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-case |
| Service epic | RWB-SVC-P3 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-002 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP04, DP05, DP06, DP07, DP09, DP10, DP11, DP13, DP15, DP19 |
| Parallel lane | L-P3-Y |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P2-E2002-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P3 rwb-case v1.md (FR-P3-032) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-002 for rwb-case. The ACE read and its live answer stay with rwb-integration (RWB-P2-E2002-APP); this story keeps the stored plan status on the case in `rwb_case`, the RESTRUCTURE evaluation through the embedded Drools kit, the route move, the task, the durable timer, the local decision record and the plan status panel. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **case owner (RW-CASEOWN)**, I want **the restructure plan status of the ACE common module (created, approved, booked, broken) stored on my case with the date it was read, the route state of the case moved by the RESTRUCTURE rules when a plan breaks, the case returned to me with a task and a durable timer, and the status on the case record even when ACE cannot answer**, so that **a case with a live plan is never treated as if it had none, and a broken plan returns the case to me the next morning without anyone re-keying it**.

### 2. Business rationale

Restructure plans are calculated and held in ACE (DL14). Without the plan status on the case, a recovery officer can start litigation on a customer who is paying a plan, or miss a plan that broke. The legacy story read the status from the ACE common module each morning and on each case view, kept the last known status with its date when ACE returned none, and raised a broken plan to the restructure rules.

In the target the same journey is cut across services. rwb-integration owns the call to the ACE common module and answers the live status on its own base `/api/recovery/integration/v1` (RWB-P2-E2002-APP), because only that service speaks to outside systems. rwb-case owns the case of record: it stores `plan_ref`, `plan_status` and `plan_status_as_of` on `recovery_case` in `rwb_case` (DP-01), joins the plan to the case on the account number (DL21), evaluates package RESTRUCTURE with the version in force through the embedded Drools kit inside an activity (DP-04), moves the route state, places the case in the case owner's queue with a task and a durable timer (DP-10), and writes the local decision record with the rule ID and the package version in the same transaction as the move (DP-03). Because the plan is a fact of the case and not of the reader, rwb-case also serves the stored status, with `live` false and the message code that says the value is from an earlier date, so a screen or a caller keeps working when the ACE read fails or is not routable from the edge.

Retiring the in-process call is the realignment work: the legacy `RestructurePlanQuery.statusFor` call and the legacy `CasePlanStatus.update` and `CaseEvents.raise` published interfaces are replaced by the rwb-integration contract on one side (DP-11, one hop, 2 s timeout, built against its contract fake) and by one `rwb_case` transaction with its outbox rows on the other (DP-09). The legacy plan-status operation of the monolith (`GET` on base `/api/recovery/v1` with path `/cases/{caseId}/plan-status`) becomes a stored-status read on `/api/recovery/case/v1` (DP-13), and the plan section of the case record is composed at the edge by gateway-bff from the live answer of rwb-integration and the stored answer of rwb-case in parallel (DP-19).

It meets REQ-DRI-013 (plan status read from the ACE common module) and REQ-CHO-002 (a change to a restructure plan status in ACE is visible on the case through the ACE common module) for the case side, and it carries the legacy measure: a broken plan is back with the case owner the next morning and no case with a live plan is treated as if it had none. It owns no legacy acceptance criterion; the nine criteria of RWB-E2-002 are exercised across services by RWB-ITG-E2002-ITG, and the eleven criteria in section 7 are new for this service change.

### 3. Preconditions

- RWB-P2-E2002-CON is published: the plan-status resource shape (`planRef`, `accountNo`, `status`, `statusDate`, `live`), the `GET /api/recovery/integration/v1/cases/{caseId}/plan-status` operation, its error envelope and its contract fake. This story builds against that contract and its fake and never against the ACE common module.
- The `rwb_case` schema baseline and the case of record exist from the Epic 1 case story (RWB-P3-E1018-APP): `recovery_case`, `case_account`, `queue`, `task`, `timer` and the outbox table.
- The workflow kit and the embedded Drools kit are published by the platform contract stories (DP-04, DP-10) and the local decision-record library and the shared topic `rwb.decision-record.v1` by the platform contract story of DP-03. These platform dependencies are held by the platform stories and are not repeated in the metadata rows.
- RWB-P3-E2042-APP has put package RESTRUCTURE version "RES-2026.12" in force for the business date, with rows R-RES-29, R-RES-30, R-RES-31 and R-LIT-02, each row carrying `action_text`, `owner_role` and `timer_spec`, and the version has at least 50 passing scenarios and an approver who is not the author.
- Parameter `restructure.max_breaks` = 2 is in force in `parameter_value`, owner RW-COE (DL23).
- The plan status list LOV-PLAN-STATUS holds CREATED, APPROVED, BOOKED and BROKEN in the rwb-case reference data, and the plan event map rows are loaded: ACE status BROKEN with route state PLAN_CURE_PERIOD maps to event code CURE_PERIOD_EXPIRED; BROKEN with any other route state maps to TREATMENT_BROKEN.
- The properties `rwb.ace.plan.batch-size` = 500 and `rwb.ace.plan.timeout-ms` = 2000 are in force as parameter rows (assumed; DL11), not as code.
- The plan-status step runs after the case creation step of the daily case update, so a case exists before its plan is read.
- The login is the rwb-case login (DP-02): Not specified in the source documents (GAP-0774; ASM-1397).

### 4. Flow

1. rwb-source-data publishes AceDataReady (EV-26) for the business date; the rwb-case case router consumes it through its inbox and starts DailyCaseRun on task queue `rwb-case`.
2. DailyCaseRun runs the case creation step first, then the plan-status step of this story; the order is the legacy order of JOB-02.
3. The plan-status step pages the open cases with an account from `recovery_case` and `case_account` and, for each case, calls the rwb-integration operation `GET /api/recovery/integration/v1/cases/{caseId}/plan-status` inside the `readPlanStatus` activity: one hop, 2 s timeout, breaker per downstream (DP-11), with the page size and the concurrency taken from `rwb.ace.plan.batch-size` and the timeout from `rwb.ace.plan.timeout-ms`. The direction of this hand-over and its batching are Not specified in the source documents (GAP-0769; ASM-1392): the connection matrix has neither a P3 to P2 call nor a P2 to P3 call, so the step reads one case per call and the page size bounds the concurrency.
4. `readPlanStatus` returns the plan reference, the account number, the status, the status date and the `live` flag for the case, or no plan, or a timeout.
5. The step compares the answer with the stored `plan_ref`, `plan_status` and `plan_status_as_of`; a case whose status and date are unchanged is skipped and costs no write and no event.
6. An answer whose status is not in LOV-PLAN-STATUS is not stored: the step records the rejection with the check "Lists of values" and the rejected code, and the case keeps its stored value.
7. An answer with no plan for a case that holds one keeps the stored status and its date, records an exception with product "DP04" naming the plan, and leaves the case unchanged.
8. EvaluateRules activity: for a case whose status changed, the embedded Drools kit evaluates package RESTRUCTURE on the facts `route_state`, `plan_status`, `break_count` and `prior_route` with the business date; the package model and its checksum are fetched from rwb-decision (`GET /api/recovery/decision/v1/rule-models/{packageCode}/{versionLabel}`) and the KieBase is swapped only after the checksum is verified (DP-04). The result names the rule ID, the package version and the outputs; `NoPackageInForce` is a refusal, never a default.
9. For each rule that fires, the step reads the catalog row of the rule by rule ID and package version for `action_text`, `owner_role` and `timer_spec`; the catalog is owned by rwb-decision and its read operation is Not specified in the source documents (GAP-0770; ASM-1393).
10. RecordAndApply activity: in one `rwb_case` transaction the service writes the new `route_state` and `plan_status`/`plan_status_as_of`, the task row with its `task_code` and `due_at` from the `timer_spec`, the queue placement, and the local decision record with the rule ID and the package version, and inserts CaseStateChanged (EV-05) and DecisionRecorded in the outbox (DP-03, DP-09). A failed write rolls the whole transaction back, so nothing moves.
11. The workflow signals CaseWorkflow with the route move; CaseWorkflow holds the due date of the task as a durable timer of the workflow kit (DP-10) and raises TimerBreached through its own state when the timer passes, so no Quartz row and no five-minute timer check is involved.
12. On a status that is not BROKEN, or a plan that is live and unchanged, the case keeps its route state and only the stored status and its date are written; the RESTRUCTURE rules decide, and this story never invents a route move.
13. Case owner: the case record is served by the gateway-bff composite route, which calls rwb-case `GET /api/recovery/case/v1/cases/{caseId}` and rwb-integration `GET /api/recovery/integration/v1/cases/{caseId}/plan-status` in parallel, one hop each, and merges the two answers (DP-19). When the live answer is missing, the stored answer of rwb-case is shown with MSG-P2-008 and its date.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The rwb-integration operation returns no plan for a case that holds one | The case keeps its stored status and date; the exception with product "DP04" lists the plan for the ACE team; the next run reads it again | MSG-P2-008 | AC5 |
| X2 | The rwb-integration operation does not answer within 2 seconds or is unavailable | The step keeps every stored status and retries the case in the next run; the read answer of the case carries the stored value with its date | MSG-GEN-006, MSG-P2-008 | AC5 |
| X3 | The status returned is not in LOV-PLAN-STATUS | The status is not stored; the exception with check "Lists of values" names the code and the plan reference; no decision record and no route move | None | AC4 |
| X4 | The plan-status step runs twice for the same business date | No status row is written twice, no route move is repeated and no event is raised twice | None | AC3 |
| X5 | The local decision-record write fails during the broken plan move | The transaction rolls back: the status and the route state do not move, the step fails, and the move is retried in the next run | MSG-P7-003 | AC7 |
| X6 | No RESTRUCTURE version is IN_FORCE on the business date | `NoPackageInForce`; no decision record is written and the route state does not move; the case goes to the exception queue for role RW-TEAMMGR | MSG-P3-027 | AC6 |
| X7 | A user reads the plan status of a case outside their scope | Refused; nothing is returned and nothing is written | MSG-P4-003 | AC8 |
| X8 | A role without the Case record right reads the plan status | Refused; nothing changes | MSG-P4-002 | AC8 |
| X9 | A plan breaks on a case whose route state is not the cure period | The rules of package RESTRUCTURE decide the move, including R-LIT-02 on the litigation route; no second route is invented by code | None | AC10 |
| X10 | The break count is at `restructure.max_breaks` | The rules bar a further restructure; the case stays with the case owner and no restructure task is raised | None | AC9 |

The break of X1 and X3 is the data-quality exception with product "DP04" and with check "Lists of values" that the legacy story raises; the table that holds a break is `reconciliation_result`, owned by rwb-source-data, and the operation by which rwb-case hands it over is Not specified in the source documents (GAP-0772; ASM-1395).

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds on Day 1 against the rwb-integration contract fake of RWB-P2-E2002-CON and the platform kits; no work order sits inside another team's lane |
| Negotiable | The status list, the plan event map, the maximum breaks, the batch size, the timeout, the rule rows and the package version are rows and parameters; the story fixes the behaviour |
| Valuable | A case with a live plan is never treated as if it had none, and a broken plan is back with the case owner the next morning with a task and a timer |
| Estimable | One step of the daily workflow, one client, one facts builder, one rule evaluation, one transaction, one read operation, one panel |
| Small | Fits two weeks with its tests |
| Testable | Each of the eleven criteria of section 7 is one automated test; the cross-service answer is stubbed in the rwb-integration contract fake |

### 7. Acceptance criteria

```gherkin
Feature: ACE plan status on the case

  Background:
    Given case "RW-2026-000310" is open with synthetic account "A-0310"
    Given package "RESTRUCTURE" version "RES-2026.12" is in force with rows R-RES-29, R-RES-30, R-RES-31 and R-LIT-02
    Given parameter "restructure.max_breaks" is 2

  Scenario: AC1 The plan status is stored on the case (new, D-RCV-60)
    Given the rwb-integration contract mock returns plan "TDR-SYN-0310" for "A-0310" with status "APPROVED" and status date 2026-12-10
    When the plan-status step of the daily case update runs for case "RW-2026-000310"
    Then the case holds plan_ref "TDR-SYN-0310", plan_status "APPROVED" and plan_status_as_of 2026-12-10
    Then GET /cases/{caseId}/plan-status returns planRef "TDR-SYN-0310", status "APPROVED", statusDate 2026-12-10 and live false
    Then the status write, the decision record and the outbox row commit in one rwb_case transaction
    Then the case status is unchanged and no route state moves

  Scenario: AC2 A broken plan moves the route state (new, D-RCV-60)
    Given the case is in route state "PLAN_CURE_PERIOD" with break count 0
    Given the rwb-integration contract mock returns plan "TDR-SYN-0310" with status "BROKEN" and status date 2026-12-14
    When the daily case update runs on 2026-12-15
    Then the case plan status is "BROKEN" with plan_status_as_of 2026-12-14
    Then the route state moves to "PLAN_BROKEN" by R-RES-29 and then to "BACK_TO_ROUTE_DECISION" by R-RES-30
    Then the case is in the case owner's queue with a task due in 5 working days, from timer_spec "5 working days" of row R-RES-30 of version "RES-2026.12"
    Then CaseWorkflow holds the due date as a durable timer and no Quartz row is written
    Then one decision record per move names R-RES-29 or R-RES-30 and the package version "RES-2026.12"
    Then rwb.case.CaseStateChanged.v1 is published with event code CURE_PERIOD_EXPIRED for the first move and BREAK_RECORDED for the second

  Scenario: AC3 A repeat of the same status and date changes nothing (new, D-RCV-60)
    Given the step on 2026-12-15 stored status "BROKEN" with date 2026-12-14 for plan "TDR-SYN-0310"
    When the step runs again for 2026-12-15 with the same answer
    Then no status row is written a second time
    Then no second CURE_PERIOD_EXPIRED event is raised for the case
    Then the route state stays "BACK_TO_ROUTE_DECISION" and the repeat is counted once in the run summary

  Scenario: AC4 An unknown status code is not stored (new, D-RCV-60)
    Given the case holds plan "TDR-SYN-0310" with status "BOOKED" and date 2026-12-01
    Given the rwb-integration contract mock returns status "SUSPENDED" for "TDR-SYN-0310"
    When the daily case update runs
    Then plan_status and plan_status_as_of are unchanged
    Then the exception with check "Lists of values" names the code "SUSPENDED" and plan "TDR-SYN-0310"
    Then no decision record is written and no route state moves

  Scenario: AC5 A status ACE cannot give keeps the stored status (new, D-RCV-60)
    Given the case holds plan "TDR-SYN-0310" with status "BOOKED" and date 2026-12-01
    Given the rwb-integration contract mock returns no plan for "A-0310"
    When the daily case update runs on 2026-12-15
    Then the case keeps status "BOOKED" with date 2026-12-01
    Then GET /cases/{caseId}/plan-status returns live false and message MSG-P2-008 with the date 2026-12-01
    Then the exception with product "DP04" lists plan "TDR-SYN-0310" for the ACE team

  Scenario: AC6 No RESTRUCTURE version is in force (new, D-RCV-60)
    Given no RESTRUCTURE version is IN_FORCE on 2026-12-15
    When the daily case update finds plan "TDR-SYN-0310" broken on that date
    Then NoPackageInForce is raised with MSG-P3-027 for package "RESTRUCTURE"
    Then no decision record is written and the route state stays "PLAN_CURE_PERIOD"
    Then the stored plan status is not changed
    Then the case is placed in the exception queue for role "RW-TEAMMGR"

  Scenario: AC7 A failed decision record write on a broken plan (new, D-RCV-60)
    Given the local decision-record store is unavailable
    When the daily case update finds plan "TDR-SYN-0310" broken
    Then plan_status and the route state do not change
    Then the step fails with message MSG-P7-003 and the move is retried in the next run
    Then the retried move writes one decision record and one state change

  Scenario: AC8 The plan status read is refused without the right or outside the scope (new, D-RCV-60)
    Given user "U-5001" holds RW-REFADM, which has no Case record right
    Given the rwb-access contract mock returns no Case record right for role "RW-REFADM"
    When "U-5001" calls GET /cases/{caseId}/plan-status for case RW-2026-000310
    Then the call is refused with status 403 and MSG-P4-002
    Given a case owner whose scope is "Own" and a case owned by another person
    When the case owner calls the same operation for it
    Then the response is 404 with message MSG-P4-003
    Then the read writes nothing

  Scenario: AC9 A second break bars a further restructure (new, D-RCV-60)
    Given the case is in route state "PLAN_BROKEN" with break count 1
    Given the rwb-integration contract mock returns status "BROKEN" with a new status date
    When the daily case update runs
    Then the break count is 2 and the route state moves to "RESTRUCTURE_BARRED" by R-RES-31
    Then no restructure task is raised and the case stays with the case owner

  Scenario: AC10 A broken plan on the litigation route returns the case to the legal route (new, D-RCV-60)
    Given the case is in route state "LIT_ROUTE_APPROVED" with prior_route "R2"
    Given the rwb-integration contract mock returns plan "TDR-SYN-0310" with status "BROKEN" and status date 2026-12-14
    When the daily case update runs on 2026-12-15
    Then R-LIT-02 fires and the route state moves to "NOTICE_GENERATED"
    Then the plan event map row for status BROKEN with route state "LIT_ROUTE_APPROVED" raises TREATMENT_BROKEN
    Then the legal route task is due the same day and the decision record names R-LIT-02 and version "RES-2026.12"

  Scenario: AC11 The case record shows the plan status through the composite route (new, D-RCV-60)
    Given the gateway-bff composite route serves the case record of case "RW-2026-000310"
    Given the case holds plan "TDR-SYN-0310" with status "APPROVED" and date 2026-12-10
    When the case owner opens the case record
    Then the plan panel shows plan "TDR-SYN-0310", status "Approved" and date 2026-12-10
    And the browser calls one composite route and no owner service directly
    When the live answer of rwb-integration is not available
    Then the panel shows the stored status with message MSG-P2-008 and its date
```

AC1 to AC11 are new for the rwb-case slice: the nine legacy criteria of RWB-E2-002 are exercised across services by RWB-ITG-E2002-ITG and the app slice of rwb-integration by RWB-P2-E2002-APP, so this story owns no legacy acceptance criterion and copies none.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The plan status is read from the ACE common module through its published interface, never from ACE tables, and in the target the read is the rwb-integration contract on `/api/recovery/integration/v1` | INT-34; DL14; ADR-002; DP-11 |
| BR2 | The account number is the join between the case and the ACE plan | DL21 |
| BR3 | Plan status values: CREATED, APPROVED, BOOKED, BROKEN; any other code is held as an exception and never stored | LOV-PLAN-STATUS (TSD P3 v3 T3.2); story intent |
| BR4 | A plan marked broken while the case is in the cure period marks the plan broken and records the break | R-RES-29, R-RES-30 |
| BR5 | A second break bars a further restructure | R-RES-31; parameter restructure.max_breaks |
| BR6 | A case on the litigation route with a broken plan returns to the legal route | R-LIT-02 |
| BR7 | When ACE returns no status, the last known status and its date stay on the case | FEAT-CHO-02; VR-P2-001-1 |
| BR8 | A decision that cannot be written to the decision record does not proceed: the record, the state change and the outbox row are one transaction | Principle 5; R-UNI-39; DP-03 |
| BR9 | A repeat of the same status and date raises no event and writes no row | R-UNI-40 |
| BR10 | R-RES-29, R-RES-30, R-RES-31 and R-LIT-02 are rows of package RESTRUCTURE, evaluated by the embedded Drools kit; the result names the rule and the package version, and the action text, the owner role and the timer spec come from the rule catalog of rwb-decision | D-RCV-36 T5, T6, T7; DP-04 |
| BR11 | No RESTRUCTURE version in force is a refusal (`NoPackageInForce`), never a default move | R-UNI-41; D-RCV-36 T7 |
| BR12 | The stored status is `plan_status` with `plan_status_as_of`; both are written together or not at all, and a status without its date is never written | DF-CAS-047, DF-CAS-048 |
| BR13 | The plan event map (ACE status and route state to event code) is data, not code, and a case whose pair has no row is held as an exception | Legacy PlanEventMap; DP-07 |
| BR14 | The plan-status step writes nothing outside `rwb_case` and calls no ACE view; the plan comes from the rwb-integration contract and the rule catalog from rwb-decision | DP-01, DP-05; ADR-010 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| PLAN_CURE_PERIOD | CURE_PERIOD_EXPIRED | ACE plan status BROKEN | PLAN_BROKEN |
| PLAN_BROKEN | BREAK_RECORDED | break_count < max_breaks | BACK_TO_ROUTE_DECISION |
| PLAN_BROKEN | BREAK_RECORDED | break_count >= max_breaks | RESTRUCTURE_BARRED |
| LIT_ROUTE_APPROVED | TREATMENT_BROKEN | plan_status = broken and prior_route in (R1, R2) | NOTICE_GENERATED |

These are route states (`recovery_case.route_state`, DF-CAS-007); the case status stays "In progress". The story also writes the stored plan status and its date (`plan_status`, `plan_status_as_of`), which are facts of the case and not route states.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| rwb-case service identity (the rwb-case login, DP-02) | Runs the plan-status step; reads the plan status through the rwb-integration contract; writes the stored status, the route state, the task, the placement, the timer and the decision record |
| Drools evaluator (SY-RULES identity) | Evaluates package RESTRUCTURE through the embedded kit and returns the rule ID, the package version and the outputs (Rules and parameters R) |
| CaseWorkflow | Holds the durable timer of the task due date and raises TimerBreached through its own state; moves no route state by itself |
| Decision-record library identity | Writes the local decision record and its outbox row (Decision log C) |
| RW-CASEOWN, case owner | Reads the plan status on cases in scope and receives the task of a broken plan (Case record R) |
| RW-RESTRUCT, restructuring officer | Reads the plan status on cases in scope (Case record R) |
| RW-TEAMMGR, team manager | Receives the case in the exception queue on the no-package path (Case record R) |
| RW-DATASTEW, RW-PLATADM | Read the data-quality exception for the ACE team (Platform administration R) |
| RW-COE | Owns the RESTRUCTURE rows, the plan event map rows, the status list and the parameters |
| RW-RISK | Approves a package version; the author cannot approve |
| RW-REFADM | Holds no Case record right; refused on the read operation with MSG-P4-002 |

The per-service login name is Not specified in the source documents (GAP-0774; ASM-1397); the story names it "the rwb-case login (DP-02)" until it is agreed.

### 11. Data

| BR Field ID | Entity in rwb_case | Field | Read or write |
|---|---|---|---|
| DF-CAS-046 | recovery_case | plan_ref | Write |
| DF-CAS-047 | recovery_case | plan_status | Write |
| DF-CAS-048 | recovery_case | plan_status_as_of | Write |
| DF-CAS-007 | recovery_case | route_state | Write |
| DF-CAS-021 | recovery_case | rule_version (the package version of the move) | Write |
| DF-CAS-001, DF-CAS-005, DF-CAS-009, DF-CAS-010 | recovery_case | id, status, owner_user_id, queue_id | Read, and owner and queue written with the placement |
| DF-CAS-026 | case_account | account_key | Read, for the join to the plan |
| DF-WRK-018, DF-WRK-019, DF-WRK-024 | task | case_id, task_code, due_at | Write |
| DF-WRK-030, DF-WRK-031, DF-WRK-035 | timer | timer_type, started_at, status | Write |
| DF-REF-132 to DF-REF-158 | parameter_catalog, parameter_value | `restructure.max_breaks`, `rwb.ace.plan.batch-size`, `rwb.ace.plan.timeout-ms` and their versions in force | Read |
| DF-REF-159 to DF-REF-184 | reference_version, reference_row | LOV-PLAN-STATUS version and the plan event map version with its rows | Read |
| DF-REF-002, DF-REF-003, DF-REF-008, DF-REF-010, DF-REF-011, DF-REF-296, DF-REF-298 | rule_row (rwb_decision, owner P7) | rule_id, rule_version, action_text, owner_role, timer_spec, package_version_id, outputs | Read, by rule ID and package version through the rwb-decision registry |
| DF-DEC-001 to DF-DEC-018 | decision record (local library) and decision_log_entry (rwb_decision) | all fields | Write locally; the central entry is sealed by rwb-decision |

The plan fields `planRef`, `status`, `statusDate` and `live` are read from the rwb-integration contract and are not read from any table; the account number used for the join is `case_account.account_key`. No copy of an ACE plan row is written into `rwb_case`, and no foreign key crosses a schema (DP-01).

Field IDs are those in the Logical Data Model and Data Dictionary v8. `rule_row` is owned by rwb-decision (P7) under the Ownership Map, so this story reads the catalog row through the P7 contract and holds no rule table, no DRL source and no workbook of its own.

### 12. Contract

#### 12.1 REST operations provided

Base `/api/recovery/case/v1`; owner rwb-case (P3).

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| GET | `/cases/{caseId}/plan-status` | The stored plan status of the case: `planRef`, `status`, `statusDate`, `live` (false) and `messageCode`; the legacy plan-status answer with the live read removed | Case record R, scope applied | Not applicable: the call writes nothing |
| GET | `/cases/{caseId}` | The case read, extended with the optional fields `planRef`, `planStatus` and `planStatusAsOf` (a backward-compatible addition, no field removed) | Case record R, scope applied | Not applicable |

Errors: 401 no session (MSG-P4-001), 403 no Case record R (MSG-P4-002), 404 not found or out of scope (MSG-P4-003), 503 store down. The timer started by a route move is read with the existing `GET /cases/{caseId}/timers` operation of rwb-case; this story writes the timer row and the durable timer, and owns neither read operation.

The live read of the same resource is served by rwb-integration on `/api/recovery/integration/v1/cases/{caseId}/plan-status` (RWB-P2-E2002-APP); this story serves the stored answer only, so a caller that cannot reach the ACE read still sees what the case holds. The gateway-bff composite route that merges the two is DP-19.

#### 12.2 REST operations consumed

| Method | Path | Service | Used for | Timeout |
|---|---|---|---|---|
| GET | `/api/recovery/integration/v1/cases/{caseId}/plan-status` | rwb-integration (P2) | The ACE plan status of the case: `planRef`, `accountNo`, `status`, `statusDate`, `live` (DP-11, built against RWB-P2-E2002-CON and its fake) | One hop, 2 s |
| GET | `/api/recovery/decision/v1/rule-models/{packageCode}/{versionLabel}` | rwb-decision (P7) | The RESTRUCTURE model, its version label and its checksum before the KieBase is used (DP-04) | One hop, 2 s |
| GET | Not specified in the source documents (GAP-0770; ASM-1393) | rwb-decision (P7) | The catalog row of a fired rule by rule ID and package version: `action_text`, `owner_role`, `timer_spec` | One hop, 2 s |
| POST | `/api/recovery/access/v1/authorise` | rwb-access (P4) | The Case record right and the scope before a read, cached by the guard library | One hop, 2 s |

#### 12.3 Events published

| Event | Topic | Owner of the type | Key | Payload (IDs and facts only) |
|---|---|---|---|---|
| `rwb.case.CaseStateChanged.v1` (EV-05) | `rwb.case.events.v1` | P3 | caseId | caseId, fromRouteState, toRouteState, eventCode (CURE_PERIOD_EXPIRED, BREAK_RECORDED or TREATMENT_BROKEN), ruleId, packageVersion, breakCount |
| `rwb.decision-record.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | P7 owns the type and the central ledger; every service writes its own record | caseId | decision record reference, rule ID R-RES-29, R-RES-30, R-RES-31 or R-LIT-02, package version, business date |

Both are written to the outbox in the same transaction as the state change and relayed with the CloudEvents envelope; no personal data is carried and the account number is not in any payload (DP-09).

#### 12.4 Events consumed

| Event | Topic | Owner of the type | Handler |
|---|---|---|---|
| `rwb.source-data.AceDataReady.v1` (EV-26) | `rwb.source-data.events.v1` | P1 | Case router, inbox dedupe, `signalWithStart` of DailyCaseRun, which runs this story's step after case creation |
| `rwb.decision.RulePackageInForce.v1` (EV-30) | `rwb.decision.events.v1` | P7 | Drops the cached KieBase of package RESTRUCTURE so the next evaluation fetches the version in force |

#### 12.5 Workflows and activities

| Name | Type | Task queue | Purpose |
|---|---|---|---|
| DailyCaseRun | Workflow (event-started from AceDataReady, owned with the case creation step) | `rwb-case` | Runs the plan-status step after the case creation step |
| PlanStatusStep | Step of DailyCaseRun | `rwb-case` | Pages the open cases, compares, evaluates, records and applies |
| readPlanStatus | Activity | `rwb-case` | Calls the rwb-integration operation with the 2 s timeout, the breaker and the bounded concurrency |
| EvaluateRules | Activity (workflow kit) | `rwb-case` | Calls the embedded Drools kit for package RESTRUCTURE with the facts and the business date |
| RecordAndApply | Activity (workflow kit) | `rwb-case` | Writes the decision record, the status, the route state, the task, the placement, the timer and the outbox rows in one transaction |
| CaseWorkflow | Workflow (parent, one per case, workflow ID = case ID) | `rwb-case` | Receives the route move and holds the durable timer of the task due date (DP-10) |

#### 12.6 Schedules

None new. The legacy plan-status step of JOB-02 runs inside the event-started DailyCaseRun workflow after case creation; no Quartz row, no five-minute timer check and no separate Schedule is created by this story. The Schedule fallback of DailyCaseRun, if an environment needs one, belongs to the story that owns DailyCaseRun.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| recovery_case | P3 (rwb_case) | The story adds `plan_ref` varchar(30), `plan_status` varchar(10) and `plan_status_as_of` date, and writes `route_state`, `rule_version` and the owner and queue on a move |
| task | P3 (rwb_case) | The task of a broken plan with its `task_code` and `due_at` from the timer spec |
| timer | P3 (rwb_case) | The screen projection of the due date behind the timers read; the clock itself is the durable timer of CaseWorkflow |
| queue, assignment | P3 (rwb_case) | The placement of the case in the case owner's queue |
| parameter_catalog, parameter_value | P3 (rwb_case) | `restructure.max_breaks`, `rwb.ace.plan.batch-size`, `rwb.ace.plan.timeout-ms` |
| reference_version, reference_row | P3 (rwb_case) | LOV-PLAN-STATUS version and the plan event map rows |
| outbox_event, processed_event, idempotency_key | PLT library, created in rwb_case | Outbox, inbox and idempotency objects (DP-09) |

rwb-case reads no table of another service and holds no foreign key across services (DP-01). `rule_row`, `rule_package_version` and `decision_log_entry` are rwb-decision tables and are read or written only through its contract.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-integration WireMock | The P2 contract of RWB-P2-E2002-CON | "APPROVED" with 2026-12-10; "BROKEN" with 2026-12-14; no plan for "A-0310"; a delay beyond 2 s; "SUSPENDED"; and the `live` flag |
| rwb-decision WireMock | The P7 contract | `GET /rule-models/RESTRUCTURE/RES-2026.12` with its checksum and rows R-RES-29, R-RES-30, R-RES-31 and R-LIT-02 with their timer specs; the empty answer of the no-package path; the catalog row of a fired rule |
| rwb-access WireMock | The P4 contract | `POST /authorise` granting Case record R, refusing it for RW-REFADM and excluding a case from an Own scope |
| gateway-bff composite route (WireMock) | The DP-19 route of the case record | The merged plan section of AC11 and the stored-value answer with MSG-P2-008 |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 4 consumed | The stored plan-status read and the extended case read provided; the P2 plan status, the P7 rule model, the P7 catalog row and the P4 authorise consumed; one hop, 2 s |
| Kafka | 2 published, 2 consumed | `rwb.case.events.v1` and `rwb.decision-record.v1` published; `rwb.source-data.events.v1` and `rwb.decision.events.v1` consumed |
| Temporal | 2 workflows, 3 activities | DailyCaseRun and CaseWorkflow; readPlanStatus, EvaluateRules and RecordAndApply |
| File | None | This story reads and writes no file |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.case`, module `planstatus`, Java package `th.co.scb.ace.workbench.recovery.case.planstatus`; front end `src/modules/recovery/case/PlanStatusPanel.tsx`.

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
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The H and C dependencies this table adds are held by the platform and service contract stories and are not repeated in the metadata rows, which carry only the contract dependency of the legacy read: RWB-P2-E2002-CON. DP-05 resolves to no ACE view and no rwb-source-data call for the plan: the plan comes from the rwb-integration contract, so rwb-case reads no `v_ace_*` view (ADR-010). DP-15 resolves to one migration in `rwb_case`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| PlanStatusStep | Step of DailyCaseRun | Pages the open cases, calls the read, compares, drives the evaluation and the apply, and records the run counts |
| PlanStatusClient | Client | Calls the rwb-integration operation with one hop, the 2 s timeout, a breaker and the bounded concurrency from `rwb.ace.plan.batch-size` |
| PlanStatusComparator | Service | Compares status and status date with the stored values and skips an unchanged plan; builds the idempotency key from case ID, plan reference, status and status date |
| PlanEventMapCatalog | Service | Reads the plan event map rows of rwb-case reference data and returns the event code of an ACE status and route state pair; holds no map in code |
| RestructureFacts | Fact builder | Builds the facts of one case: route state, plan_status, break_count and prior_route |
| RulePackageClient | Client | Fetches the RESTRUCTURE model and its checksum from rwb-decision, verifies it and hands it to the KieBase registry (DP-04) |
| RuleCatalogClient | Client | Reads `action_text`, `owner_role` and `timer_spec` of the fired rule by rule ID and package version |
| RouteMoveService | Service | Applies the rule outputs: route state, placement in the case owner's queue, task with its due date, timer row, and the signal to CaseWorkflow |
| CasePlanStatusRepository | Repository | Writes `plan_ref`, `plan_status`, `plan_status_as_of`, `route_state` and `rule_version` in schema rwb_case only |
| DecisionRecordWriter | Library adapter | Writes the local decision record with the rule ID and the package version, hash-linked, in the same transaction (DP-03) |
| PlanStatusController | Controller | `GET /cases/{caseId}/plan-status` and the plan fields of `GET /cases/{caseId}`, with the access check and the scope |
| PlanStatusPanel | React component | Shows plan, status, date, and MSG-P2-008 with the stored date when the answer is not live |

**Database and migrations**

- Migration `V2002_1__plan_status.sql` adds `plan_ref` varchar(30), `plan_status` varchar(10) and `plan_status_as_of` date to `recovery_case`, with `plan_status` validated against LOV-PLAN-STATUS by the service, no database check constraint on the list value.
- No new table: the task, the timer, the queue, the assignment, the parameter and the reference tables already exist in `rwb_case`.
- One index for the step: `ix_recovery_case_open_plan ON recovery_case (status) WHERE closed_date IS NULL AND plan_ref IS NOT NULL`, so the page of cases with a plan is read without a scan.
- The migration runs in the rwb-case Flyway sequence of the service's own schema (DP-15); no other schema is touched.

**Configuration and reference data**

- Plan event map rows (RW-COE), versioned reference data of rwb-case: ACE status BROKEN with route state PLAN_CURE_PERIOD maps to event code CURE_PERIOD_EXPIRED; BROKEN with any other route state maps to TREATMENT_BROKEN. The table code under which the map is loaded in `reference_version` is Not specified in the source documents (GAP-0771; ASM-1394), because LOV-REF-TABLE lists no code for this map.
- LOV-PLAN-STATUS with CREATED, APPROVED, BOOKED and BROKEN (RW-COE).
- Parameter `restructure.max_breaks` = 2 (RW-COE); `rwb.ace.plan.batch-size` = 500 and `rwb.ace.plan.timeout-ms` = 2000 (assumed; DL11).
- Package RESTRUCTURE rows R-RES-29, R-RES-30, R-RES-31 and R-LIT-02 with their action text, owner role and timer spec (RW-COE, through RWB-P3-E2042-APP). The version in force per environment is read from the rwb-decision registry on every evaluation; there is no lock file.

**Build steps**

1. PlanStatusClient against the rwb-integration contract fake, with the 2 s timeout, the breaker and the bounded concurrency; tests for AC1 and AC5.
2. PlanStatusComparator and the idempotency key; test for AC3.
3. PlanEventMapCatalog and the status list read through the reference-data contract; tests for AC4 and the event codes of AC2 and AC10.
4. RestructureFacts, RulePackageClient with the checksum check, and the EvaluateRules call; tests for AC2, AC6, AC9 and AC10.
5. RouteMoveService and CasePlanStatusRepository with the task, the placement, the timer and the signal, all in one transaction with the decision record; tests for AC2 and AC7.
6. PlanStatusController with the access check, the scope and the stored fallback answer; tests for AC5 and AC8.
7. PlanStatusPanel and the composite-route contract test; test for AC11.
8. Register the step into DailyCaseRun after the case creation step and run the step over a page of synthetic cases to confirm no second write and no second event; test for AC3.
9. Contract-fake run of every cross-service answer in isolation, so the story builds before rwb-integration lands.

**Feature switch.** The legacy flag `rwb.integration.ace-plan-status` is kept as the legacy reference. In the target the switch is a parameter read through the parameters contract: off means the step writes no status and the read answers from the stored value only.

**Done when.** The tests in section 16 pass, the rwb-integration contract tests stay green, every decision record of a route move names its rule ID and the package version, and no case in the SIT run with a live plan has been moved by a rule.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P2-008 | Plan status shown from the stored value | The ACE plan status is from {date}. Today's status was not returned. |
| MSG-GEN-006 | rwb-integration or the ACE common module unavailable | {system} is not available. Your request is queued and will be retried. |
| MSG-P7-003 | Decision record write failed on a broken plan | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P3-027 | No RESTRUCTURE version is in force | The rule version was refused at the {check} check: {detail}. |
| MSG-P4-003 | Case outside the caller's scope | This case is not in your scope. |
| MSG-P4-002 | A role without the Case record right | You cannot {action} here. Your role does not include it. |

For MSG-P3-027 in this story, {check} is "no package in force" and {detail} names the package code "RESTRUCTURE" and the business date only, never a case fact. For MSG-GEN-006, {system} is "rwb-integration" when the service does not answer and "ACE common module" when it reports the ACE side.

### 15. Screens and states

SCR-03 Case record, states loading and read only: the plan status panel shows the plan reference, the status, the date and, when the answer is not live, MSG-P2-008. SCR-14 Treatment record, state broken, shows the broken plan once the case returns to the route decision.

Both screens are served by the gateway-bff composite route, which calls rwb-case and rwb-integration in parallel, one hop each, and merges the two answers into the screen model: the live answer of rwb-integration when it answers, the stored answer of rwb-case with its message code when it does not (DP-19). The screen fields, the field-level masking and the merge order are Not specified in the source documents (GAP-0773; ASM-1396); the full read-only case view and the timer and deviation sections remain with RWB-P3-E1023-APP.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-002-01 | AC1, AC11, BR1, BR2, BR6, BR10 | Component | rwb-integration stub plan TDR-SYN-0310 APPROVED |
| TC-E2-002-02 | AC2, BR4, BR5, BR10, BR13 | Component | Case in PLAN_CURE_PERIOD; plan BROKEN with 2026-12-14 |
| TC-E2-002-03 | AC5, BR7 | Component | rwb-integration stub returns no plan |
| TC-E2-002-04 | AC5, BR7 | Component | rwb-integration stub delayed 3 seconds |
| TC-E2-002-05 | AC4, BR3 | Component | rwb-integration stub returns SUSPENDED |
| TC-E2-002-06 | AC3, BR9 | Component | Step run twice on 2026-12-15 |
| TC-E2-002-07 | AC7, BR8 | Component | Decision record store stopped |
| TC-E2-002-08 | AC8 | Component | Case owner with scope Own and a case of another owner |
| TC-E2-002-09 | AC6, BR11 | Component | No RESTRUCTURE version in force on 2026-12-15 |
| TC-E2-002-10 | AC8, BR14 | Component | RW-REFADM (no Case record right) calls GET /cases/{caseId}/plan-status; refused with MSG-P4-002 |
| TC-E2-002-11 | AC7, BR8 | NFR | Decision record write forced to fail on the R-RES-29 move; route state unchanged |

The legacy levels map System to Component, Access to Component and Resilience to NFR, because the cross-service behaviour of this key is proved by the integration story. The `-ITG` copy of each case is held by RWB-ITG-E2002-ITG. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: status codes, the plan event map, the maximum breaks, the batch size, the timeout, the rule rows and the package version are rows or parameters.
- No personal data in logs, tests, workflow history or prompts: logs hold case IDs and plan references, never account numbers, names or identity numbers; the workflow payloads pass the payload codec.
- No read of another service's tables and no ACE view: the plan comes from the rwb-integration contract, the rule model and catalog from rwb-decision, the rights from rwb-access; `rwb_case` holds no foreign key into another schema (DP-01, DP-05).
- One evaluator: RESTRUCTURE is evaluated only through the embedded Drools kit on the version fetched from rwb-decision; no code reads a workbook, a DRL source or a rule row directly (D-RCV-36 T3, T6; DP-04).
- A read of the plan status writes nothing and raises no event.
- The decision record is written before the route state moves, in one transaction with it; a failed write rolls the whole move back (R-UNI-39).
- NoPackageInForce is never caught and turned into a default move; the case goes to the exception queue.
- Every outbound event is written to the outbox in the same transaction as the state change and carries IDs and facts only (DP-09).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-013 | Plan status read from the ACE common module | Program 5.2; Epic 2 3.2 | FEAT-CHO-02 | 7.3 Negotiate settlement or deed in lieu | R-UNI-39, R-UNI-40 | TC-E2-002-01, TC-E2-002-04, TC-E2-002-06, TC-E2-002-07 |
| REQ-CHO-002 | Plan status change visible on the case | Program 5.3; Epic 2 3.2 | FEAT-CHO-02 | 7.3 Negotiate settlement or deed in lieu | R-RES-29, R-RES-30, R-RES-31, R-LIT-02 | TC-E2-002-02, TC-E2-002-03, TC-E2-002-05, TC-E2-002-08, TC-E2-002-09 |
| D-RCV-60 DP-04 | The rule package and its version come from the rwb-decision registry on every evaluation and are named on every decision record | Decision log, D-RCV-60; Template and Rules §R5.5 | FEAT-CHO-02 | 7.3 | R-UNI-41; D-RCV-36 T4 to T7 | TC-E2-002-09, TC-E2-002-11 |
| D-RCV-60 DP-10 | The task due date is a durable timer of the workflow, not a Quartz row or a five-minute timer check | Template and Rules §R5.5; Architecture v5 slide 44 | FEAT-CHO-02 | 7.3 | R-RES-30 | TC-E2-002-02, TC-E2-002-06 |

### 19. Out of scope

- The call to the ACE common module and the live plan-status answer on `/api/recovery/integration/v1` (RWB-P2-E2002-APP).
- Creating or changing a plan: ACE, under DL14.
- The authoring, approval and rollback of package RESTRUCTURE and its rows (RWB-P3-E2042-APP).
- The treatment record and the plan timers owned by rwb-treatment (RWB-E2-004).
- Booking confirmation of the plan from the ALS load (RWB-E2-007).
- The rights, the roles and the scope data themselves (P4 access stories).
- The break on the data-quality console and the `reconciliation_result` table (rwb-source-data).
- The full read-only case record view, the timer section and the deviation flag (RWB-P3-E1023-APP).
- The full restructure route in the Workbench: Epic 3.
- The deployment of this capability: chart values, topic and queue provisioning, dashboards and the runbook.
