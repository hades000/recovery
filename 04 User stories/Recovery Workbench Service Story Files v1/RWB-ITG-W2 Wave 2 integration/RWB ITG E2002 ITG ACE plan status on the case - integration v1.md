# RWB-ITG-E2002-ITG ACE plan status on the case

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-E2002-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W2 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-002 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP04, DP05, DP06, DP07, DP09, DP10, DP11, DP13, DP15, DP19 |
| Parallel lane | L-ITG-W2 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | RWB-P3-E2042-APP, RWB-P2-E2002-APP, RWB-P3-E2002-APP, RWB-P4-E2002-APP, RWB-P7-E2002-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to REQ-DRI-013, REQ-CHO-002) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-002 for the wave 2 integration harness. The harness proves, across services, that the ACE plan status lands on the case through the P2 contract, that a broken plan moves the route state by R-RES-29 and R-RES-30 with its task, its durable timer and one decision record per move carrying the rule ID and the package version, that a status ACE cannot give leaves the stored status with its date, that an unknown code, a timeout, a repeated run, a failed decision record and a missing package version each stop where the legacy story said they stop, and that the refusals and the schema, hop, timeout and registry boundaries hold. It builds no production code. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **member of the integration and test team (QA)**, I want **a repeatable cross-service harness that drives the ACE plan status onto the case through rwb-integration, rwb-case, rwb-access, rwb-decision and the RESTRUCTURE package registry and writes one evidence report per run**, so that **an approved plan is proved to reach the case, a broken plan is proved to return the case to its owner with a task and a timer, and every exception and refusal the legacy story defined is proved across services before the wave is accepted and after every change**.

This story builds the harness, the fakes, the seeds and the evidence only. It builds no production screen, endpoint, table, workflow or schedule, and it owns no table. It owns no legacy acceptance criterion: the nine criteria of RWB-E2-002 stay with the app stories and the nine criteria of section 7 are new. The behaviour it exercises is owned by the five I stories: RWB-P2-E2002-APP (the ACE plan-status read and the `/api/recovery/integration/v1/cases/{caseId}/plan-status` answer), RWB-P3-E2002-APP (the plan status on the case, the route state, the task and the timer), RWB-P4-E2002-APP (the rights and the scope check), RWB-P7-E2002-APP (the embedded Drools evaluation of package RESTRUCTURE and the local decision record) and RWB-P3-E2042-APP (the rule packages and their versions, authored, approved and put in force).

The realignment facts the harness proves on every run: the embedded Drools kit runs in the owning service and takes the package and the version from rwb-decision (DP-04); the Quartz timer of JOB-05 becomes a durable timer of the workflow kit on `rwb-case`, and the daily step becomes an event-started run, not a Quartz row (DP-10); the plan-status operation sits on `/api/recovery/integration/v1` (DP-13); and the case record plan section is read as one gateway answer through the gateway-bff composite route, never by the browser calling each service (DP-19).

### 2. Business rationale

Restructure plans are calculated and held in ACE (DL14). A case owner who cannot see the plan status will start litigation on a customer who is paying a plan, or miss a plan that broke; a broken plan that does not return to the case owner the next morning is a payment plan that quietly dies. The legacy story read the status from the ACE common module each morning and on each case view, kept the last known status with its date when ACE returned none, and raised the broken plan to the restructure rules R-RES-29, R-RES-30, R-RES-31 and R-LIT-02 of package RESTRUCTURE.

In the target that one journey is served by five services: rwb-integration calls the ACE common module and answers the plan-status operation; rwb-case stores the status and its date on the case, moves the route state, places the task and holds the timer; rwb-access answers the rights and the scope check; rwb-decision holds the rule-package registry and the central decision ledger, and its embedded Drools kit evaluates RESTRUCTURE with the package version in force on the business date; rwb-payment is untouched. A defect at any seam — a status stored without its date, a route move without its decision record, a task without the timer spec of the row, a stored status overwritten by an unknown code, a second event raised on a rerun, a package version taken from anywhere but the registry — would only appear with a live case, unless the journey is exercised across the services as one flow.

This story is that exercise. It runs the plan-status journey from the ACE common module stub through rwb-integration and rwb-case, then through the real services as their app stories land, reproduces every exception and refusal the legacy story defined in the same run, and attaches one evidence report per run keyed by story and business date. It meets REQ-DRI-013 and REQ-CHO-002 at the integration level, and it leaves every business rule, every screen behaviour and every table with the owning stories.

### 3. Preconditions

- The five I stories are published and deployed in the SIT environment as they land: RWB-P3-E2042-APP (the rule packages and their versions), RWB-P2-E2002-APP (the ACE plan-status read and the P2 operation), RWB-P3-E2002-APP (the plan status, the route state, the task and the timer on the case), RWB-P4-E2002-APP (the rights and the scope check) and RWB-P7-E2002-APP (the embedded Drools evaluation and the local decision record).
- gateway-bff is deployed with the composite case-record route of DP-19 available, so the plan section is read as one gateway answer. The composite route path and its merge order, the harness repository, its SIT and UAT environments, its seeding, its per-run evidence format and retention and its pass or fail gate are Not specified in the source documents (GAP-0386; ASM-0561).
- The contract fakes of §12.8 are published from the owning services' OpenAPI documents, so the harness runs green from Day 1 before any I story lands.
- The synthetic seeds of the legacy story exist: open case "RW-2026-000310" with account "A-0310"; the ACE common module stub holds plan "TDR-SYN-0310" for "A-0310"; package "RESTRUCTURE" version "RES-2026.12" is in force with rows R-RES-29, R-RES-30, R-RES-31 and R-LIT-02, each row carrying action_text, owner_role and timer_spec; the plan event map rows are loaded (ACE status BROKEN with route state PLAN_CURE_PERIOD maps to event CURE_PERIOD_EXPIRED; BROKEN with any other route state maps to TREATMENT_BROKEN); parameter `restructure.max_breaks` = 2 is in force; the plan status list LOV-PLAN-STATUS holds CREATED, APPROVED, BOOKED and BROKEN, and "SUSPENDED" is the unknown code the harness drives as the negative case.
- The reference rows and the parameter are read by their owners through their contracts: LOV-PLAN-STATUS and the plan event map rows through rwb-case's reference-data contract (DP-07), `restructure.max_breaks` through its parameters contract (DP-06), the package and the version through rwb-decision's registry. The harness holds no copy of any of them.
- The ACE read is bounded by the timeout the legacy story fixes: 2 seconds per call, with the batching of `rwb.ace.plan.batch-size` = 500 and `rwb.ace.plan.timeout-ms` = 2000 as properties, not code (DP-11).
- Feature `rwb.integration.ace-plan-status` is on in the harness environments, so the step writes and the operation answers; the harness asserts the off state through the platform library.
- No build dependency: the harness starts on Day 1 against the fakes, and each fake is replaced by the real service as its I story lands.

### 4. Flow

1. Harness: starts a run for the story and the business date, takes the run lock, and records the build under test, the harness pack version, the version of each contract it will exercise and the fake or real mode of each of the five services.
2. Harness: seeds through the owning contracts, or through the fake in fake mode — the case "RW-2026-000310" with account "A-0310"; the package RESTRUCTURE version "RES-2026.12" in force with rows R-RES-29, R-RES-30, R-RES-31 and R-LIT-02 through the rwb-decision registry; the plan event map rows and LOV-PLAN-STATUS through the rwb-case reference-data contract; the parameter `restructure.max_breaks` = 2; the ACE common module stub with plan "TDR-SYN-0310".
3. Harness: reads the session through `GET /api/recovery/access/v1/me/session` for the user with RW-CASEOWN and records the role and the scope it will exercise, and for RW-REFADM without the Case record right.
4. Harness: sets plan "TDR-SYN-0310" to "APPROVED" with status date 2026-12-10 in the ACE stub, runs the step for 2026-12-11, reads the P2 plan-status operation and the P3 case operation, and asserts the stored status and date, the label "Approved" with date 2026-12-10, the package "RESTRUCTURE" version "RES-2026.12" on the evaluation, and that rule R-LIT-02 did not fire (AC1).
5. Harness: sets the case to route state "PLAN_CURE_PERIOD" with break count 0, sets "BROKEN" with status date 2026-12-14 in the stub, runs the daily case update for 2026-12-15, and asserts the stored status and date, the route state "PLAN_BROKEN" by R-RES-29 and then "BACK_TO_ROUTE_DECISION" by R-RES-30, the case owner's queue, the task due in 5 working days from timer_spec "5 working days" of row R-RES-30 of version "RES-2026.12", the durable timer through the P3 timers read, and one decision log entry per move naming its rule ID and version "RES-2026.12" (AC2).
6. Harness: holds plan "TDR-SYN-0310" with status "BOOKED" and date 2026-12-01, makes the stub return no status, runs the update for 2026-12-15, and asserts the stored status and date, MSG-P2-008 with the date 2026-12-01 on the case record answer, and the break with product "DP04" listing the plan for the ACE team (AC3).
7. Harness: delays the ACE stub beyond 2 seconds, runs the update for 2026-12-16, and asserts that no plan status changed, that the run summary carries MSG-GEN-006 with system "ACE common module", and that the next run retries every case (AC4).
8. Harness: makes the stub return status "SUSPENDED", runs the update, and asserts that the stored status is unchanged and that a break with check "Lists of values" names the code "SUSPENDED", read through rwb-case's reference-data contract (AC5).
9. Harness: reruns the step for 2026-12-15 after the stored "BROKEN" write and asserts that no second status row is written and that no second CURE_PERIOD_EXPIRED event is raised for the case, and that the repeat is counted as a hit through the inbox (AC6).
10. Harness: makes the decision record store unavailable, runs the update on the broken plan, and asserts that the route state stays "PLAN_CURE_PERIOD", that an incident is raised with MSG-P7-003, and that the move is retried in the next run and then recorded once (AC7).
11. Harness: makes no RESTRUCTURE version IN_FORCE on 2026-12-15, runs the update, and asserts NoPackageInForce with MSG-P3-027 for package "RESTRUCTURE", no decision log entry, no route move, and the case in the exception queue for role RW-TEAMMGR (AC8).
12. Harness: reads the plan-status operation as RW-REFADM without the Case record right and as a caller whose scope excludes the case, and asserts the refusal with MSG-P4-002 and the 404 with MSG-P4-003; it then runs the boundary checks over the trace (AC9).
13. Harness: publishes the evidence report keyed by story id and business date with one row per criterion, the seam each row exercised, the service or the fake that answered, the value observed and the pass or fail result; the format and the retention are Not specified in the source documents (GAP-0386; ASM-0561).
14. Harness: releases the run lock and, on any failed criterion, fails the run and names the criterion, the seam and the observed value.

### 5. Exception paths

| ID | Trigger | What the harness asserts | Message | Covered by |
|---|---|---|---|---|
| X1 | ACE returns no status for a plan the case holds | The stored status and date are unchanged; the case record answer carries MSG-P2-008 with the date; a break with product "DP04" lists the plan for the ACE team | MSG-P2-008 | AC3 |
| X2 | The ACE common module is unavailable or does not answer in 2 seconds | No status changes; the run summary carries MSG-GEN-006 with system "ACE common module"; the next run retries every case | MSG-GEN-006, MSG-P2-008 | AC4 |
| X3 | ACE returns a status code not in the plan status list | The stored status is unchanged; a break with check "Lists of values" names the code | None | AC5 |
| X4 | The daily step runs twice for the same day | No second status row and no second CURE_PERIOD_EXPIRED event; the repeat is counted as an inbox hit | None | AC6 |
| X5 | The decision record write fails during the broken plan move | The route state stays "PLAN_CURE_PERIOD"; an incident is raised; the move is retried in the next run | MSG-P7-003 | AC7; TC-E2-002-11-ITG |
| X6 | The case is outside the caller's scope | 404 with MSG-P4-003; nothing is returned and nothing is written | MSG-P4-003 | AC9 |
| X7 | The caller's role holds no Case record R | Refused with MSG-P4-002; nothing is returned and nothing is written | MSG-P4-002 | AC9; TC-E2-002-10-ITG |
| X8 | No RESTRUCTURE version is IN_FORCE on the business date | NoPackageInForce with MSG-P3-027; no decision log entry; the route state does not move; the case is in the exception queue for RW-TEAMMGR | MSG-P3-027 | AC8 |
| X9 | The seed pack cannot be loaded, another run holds the environment lock, or the evidence report cannot be attached | The run refuses to start and names the missing seed item or the lock holder, or is marked failed with the local evidence file kept for the rerun; no criterion is reported as passed | None | All |
| X10 | The trace shows a cross-schema read, a call chain deeper than one hop, a call above 2 seconds, or a rule evaluation whose package or version does not come from rwb-decision | The run fails and names the seam and the boundary broken | None | AC9 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Runs on its own once the five I stories are deployed; until then it runs against the §12.8 fakes and the ACE common module stub, with no work order inside another team's lane |
| Negotiable | The seeds, the fakes and the assertions are configuration and data; the legacy values and the message codes are the ones the legacy story gives |
| Valuable | The plan status, the broken plan move, the task, the timer and the decision record are proved to belong to one journey across five services, with the exclusions and refusals the business asked for |
| Estimable | One runner, one fake pack, one seed set, one evidence publisher and one gate |
| Small | Fits in one iteration with the owning stories' contract tests |
| Testable | Each of the eleven `-ITG` test cases of section 16 is one run of the harness and one row of the evidence report |

### 7. Acceptance criteria

```gherkin
Feature: ACE plan status on the case - wave 2 integration harness

  Background:
    Given open case "RW-2026-000310" with synthetic account "A-0310"
    Given the ACE common module stub holds plan "TDR-SYN-0310" for "A-0310"
    Given package "RESTRUCTURE" version "RES-2026.12" is in force with rows R-RES-29, R-RES-30, R-RES-31 and R-LIT-02

  Scenario: AC1 The plan status is read through the P2 contract and lands on the case (new, D-RCV-60)
    Given plan "TDR-SYN-0310" has status "APPROVED" in ACE with status date 2026-12-10
    When the plan-status step runs on 2026-12-11 and the harness reads GET /api/recovery/integration/v1/cases/{caseId}/plan-status for "RW-2026-000310"
    Then ACE answers "APPROVED" with status date 2026-12-10 and the answer reaches the case record
    Then GET /api/recovery/case/v1/cases/{caseId} holds plan "TDR-SYN-0310", plan status "APPROVED" and status date 2026-12-10, and the case shows "Approved" with date 2026-12-10
    Then RuleEvaluator.evaluate("RESTRUCTURE", facts, 2026-12-11) reads plan_status "APPROVED" for the case, with package "RESTRUCTURE" and version "RES-2026.12"
    Then rule R-LIT-02 does not fire for the case because plan_status is not broken

  Scenario: AC2 A broken plan moves the route state across two services and one package (new, D-RCV-60)
    Given the case is in route state "PLAN_CURE_PERIOD" with break count 0
    Given plan "TDR-SYN-0310" has status "BROKEN" in ACE with status date 2026-12-14
    When the daily case update runs on 2026-12-15
    Then the case plan status is "BROKEN" with date 2026-12-14, read back through the P2 plan-status operation and the P3 case operation
    Then the route state moves to "PLAN_BROKEN" by R-RES-29 and then to "BACK_TO_ROUTE_DECISION" by R-RES-30
    Then the case is in the case owner's queue with a task due in 5 working days, from timer_spec "5 working days" of row R-RES-30 of version "RES-2026.12"
    Then the task and the timer are read through GET /api/recovery/case/v1/cases/{caseId}/timers, and the timer is a durable timer of the workflow kit on rwb-case and not a Quartz row
    Then the system writes a decision log entry for each move with the rule ID and the package version "RES-2026.12", read through GET /api/recovery/decision/v1/decision-log

  Scenario: AC3 A status ACE cannot give keeps the stored status (new, D-RCV-60)
    Given the case holds plan "TDR-SYN-0310" with status "BOOKED" and date 2026-12-01
    Given ACE returns no status for "TDR-SYN-0310"
    When the daily case update runs on 2026-12-15
    Then the case keeps status "BOOKED" with date 2026-12-01
    Then the case record answer shows message MSG-P2-008 with the date 2026-12-01
    Then a break with product "DP04" lists plan "TDR-SYN-0310" for the ACE team

  Scenario: AC4 ACE does not answer in time (new, D-RCV-60)
    Given the ACE common module does not answer within 2 seconds
    When the daily case update runs on 2026-12-16
    Then the system changes no plan status
    Then the run summary carries message MSG-GEN-006 with system "ACE common module"
    Then the next run retries every case

  Scenario: AC5 An unknown status code (new, D-RCV-60)
    Given ACE returns status "SUSPENDED" for plan "TDR-SYN-0310"
    When the daily case update runs
    Then the stored status does not change
    Then a break with check "Lists of values" names the code "SUSPENDED", and the plan status list it is checked against is read from rwb-case's reference-data contract

  Scenario: AC6 The daily step run twice (new, D-RCV-60)
    Given the daily case update on 2026-12-15 stored status "BROKEN" for plan "TDR-SYN-0310"
    When the step is rerun on 2026-12-15
    Then the system writes no second status row
    Then the system raises no second CURE_PERIOD_EXPIRED event for the case
    Then the repeat is counted as an idempotency hit through the inbox

  Scenario: AC7 A failed decision record on a broken plan (new, D-RCV-60)
    Given the decision record store is unavailable
    When the daily case update finds plan "TDR-SYN-0310" broken
    Then the route state stays "PLAN_CURE_PERIOD"
    Then the system raises an incident with message MSG-P7-003
    Then the move is retried in the next run and writes its decision log entry once

  Scenario: AC8 No RESTRUCTURE version in force (new, D-RCV-60)
    Given no RESTRUCTURE version is IN_FORCE on 2026-12-15
    When the daily case update finds plan "TDR-SYN-0310" broken on that date
    Then NoPackageInForce is thrown with MSG-P3-027 for package "RESTRUCTURE"
    Then no decision log entry is written and the route state stays "PLAN_CURE_PERIOD"
    Then the case goes to the exception queue for role "RW-TEAMMGR" with the gap
    Then the registry answer is read through GET /api/recovery/decision/v1/admin/rule-packages, and no other source is used for the package or the version

  Scenario: AC9 Access and boundary (new, D-RCV-60)
    Given the role RW-REFADM, which holds no Case record right, calls GET /api/recovery/integration/v1/cases/{caseId}/plan-status for "RW-2026-000310"
    Then the answer is refused with MSG-P4-002, and the rights are read through GET /api/recovery/access/v1/me/session
    Given a case outside the caller's scope
    When the caller calls the same operation for it
    Then the response is 404 with message MSG-P4-003
    And the run fails on any cross-schema read in the trace
    And the run fails on any call that is not one hop with a 2 s timeout
    And the run fails on any rule evaluation that does not take its package and its version from rwb-decision
```

These nine criteria are new for the ITG harness. They do not restate the nine criteria owned by RWB-E2-002 and they build on no legacy acceptance criterion of this key.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The plan status is read from the ACE common module through its published interface, never from ACE tables | INT-34; DL14; ADR-002 |
| BR2 | The account number is the join between the case and the ACE plan | DL21 |
| BR3 | Plan status values: CREATED, APPROVED, BOOKED, BROKEN; any other code is held as an exception | Story intent; ifspec Load checks, Lists of values |
| BR4 | A plan marked broken while the case is in the cure period marks the plan broken and records the break | R-RES-29, R-RES-30 |
| BR5 | A second break bars a further restructure | R-RES-31; parameter restructure.max_breaks |
| BR6 | A case on the litigation route with a broken plan returns to the legal route | R-LIT-02 |
| BR7 | When ACE returns no status, the last known status and its date stay on the case | FEAT-CHO-02; VR-P2-001-1 |
| BR8 | A decision that cannot be written to the decision log does not proceed | Principle 5; R-UNI-39 |
| BR9 | A repeat of the same status and date raises no event | R-UNI-40 |
| BR10 | R-RES-29, R-RES-30, R-RES-31 and R-LIT-02 are rows of package RESTRUCTURE, evaluated by RuleEvaluator; the result names the rule and the package version, and the action text, owner role and timer spec come from RuleCatalog | D-RCV-36 T5, T6, T7; ADR-012 |
| BR11 | No RESTRUCTURE version in force is a refusal (NoPackageInForce), never a default move | R-UNI-41; D-RCV-36 T7 |

The harness asserts these eleven rules against the owning services and the published contracts; it does not re-implement them and it changes no BR row. Three realignment rules sit on top of them and are proved by the same run:

- The package and the version on every evaluation and every decision record come from rwb-decision's registry (DP-04, BR10); no service carries a rule table, a package version or a fallback default of its own.
- The timer that holds the task due in 5 working days is a durable timer of the workflow kit on `rwb-case`, started by the route move (DP-10); there is no Quartz row, no five-minute timer check and no JOB-05 step to read.
- The status and its date are stored by rwb-case and read by the plan-status operation of rwb-integration and by the case record route of gateway-bff (DP-13, DP-19); the status list and the parameter are read through rwb-case's reference-data and parameters contracts (DP-06, DP-07), never from a copy in the harness.

### 9. State transitions

None caused by this story. The harness changes no case status and no route state; it drives the step and reads the result. The facts below are caused by the owning services and are observed and asserted by the harness. The case status stays "In progress" throughout, as the legacy story states; only the route state and the stored plan status move.

| Observed fact | Caused by | Asserted as |
|---|---|---|
| Plan status and its date stored on the case | rwb-case, written through the P3 contract after the P2 read | Plan status "APPROVED" with 2026-12-10 and then "BROKEN" with 2026-12-14, read back through the P3 case operation (TC-E2-002-01-ITG, TC-E2-002-02-ITG) |
| Route state moved twice | rwb-case, by R-RES-29 then R-RES-30 with package version "RES-2026.12" | "PLAN_CURE_PERIOD" to "PLAN_BROKEN" to "BACK_TO_ROUTE_DECISION" (TC-E2-002-02-ITG) |
| Case placed in the case owner's queue with a task | rwb-case placement and task | The queue, the task code and the due date 5 working days after 2026-12-15 (TC-E2-002-02-ITG) |
| Timer started | rwb-case, a durable timer of the workflow kit (DP-10) | The timer read through the P3 timers operation, with no Quartz row behind it (TC-E2-002-02-ITG, TC-E2-002-06-ITG) |
| Decision record written per move | rwb-decision, the local record sealed in the central ledger | One entry per move naming R-RES-29 or R-RES-30 and version "RES-2026.12" (TC-E2-002-02-ITG, TC-E2-002-07-ITG) |
| Break raised | rwb-case and the data quality path | A break with product "DP04" for the missing status and a break with check "Lists of values" for the unknown code (TC-E2-002-03-ITG, TC-E2-002-05-ITG) |
| Case in the exception queue | rwb-case, on NoPackageInForce | The case in the exception queue for RW-TEAMMGR, with no decision record and no route move (TC-E2-002-09-ITG) |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-CASEOWN, case owner | The synthetic user the harness drives: reads the plan status and the route state of cases in scope (Case record R); receives the task of the broken plan move |
| RW-REFADM, reference data administrator | Holds no Case record right; the harness drives the refusal with MSG-P4-002 (Reference data C, Case record none) |
| RW-TEAMMGR, team manager | Receives the case in the exception queue on the no-package path (Case record R) |
| RW-COE, rule owner | Authors and approves the RESTRUCTURE rows and their versions through the registry story; the harness reads the version in force and never changes it (Rules and parameters C) |
| RW-PLATADM, platform administrator | Owns the harness environments, the topics, the namespace and the run lock; reads the evidence report |
| QA lead | Owns the harness pack, the seeds, the evidence format and the gate |
| Integration lead | Owns the fake pack, the run of record and the replacement of each fake by its I story |
| Platform workflow owner | Owns the Temporal namespace, the durable timers and the task queue `rwb-case` in SIT and UAT |
| No approval applies | The story takes no decision; the harness asserts the decisions and the refusals of the owning stories |

### 11. Data

The harness owns no table and no schema (DP-01, DP-15). It seeds and reads the fields below through the owning services' contracts and asserts them; the field IDs are those of the Logical Data Model and Data Dictionary.

| BR Field ID | Entity | Schema | Field | Read or write |
|---|---|---|---|---|
| DF-CAS-001 | recovery_case | rwb_case | id | Read through the P3 contract |
| DF-CAS-007 | recovery_case | rwb_case | route_state | Read through the P3 contract |
| DF-CAS-009 | recovery_case | rwb_case | owner_user_id | Read through the P3 contract |
| DF-CAS-010 | recovery_case | rwb_case | queue_id | Read through the P3 contract |
| DF-CAS-026 | case_account | rwb_case | account_key | Read through the P3 contract |
| DF-CAS-046 | recovery_case | rwb_case | plan_ref | Read through the P3 contract |
| DF-CAS-047 | recovery_case | rwb_case | plan_status | Read through the P3 contract |
| DF-CAS-048 | recovery_case | rwb_case | plan_status_as_of | Read through the P3 contract |
| DF-WRK-002 | queue | rwb_case | queue_code | Read through the P3 contract |
| DF-WRK-018 | task | rwb_case | case_id | Read through the P3 contract |
| DF-WRK-019 | task | rwb_case | task_code | Read through the P3 contract |
| DF-WRK-024 | task | rwb_case | due_at | Read through the P3 contract |
| DF-WRK-030 | timer | rwb_case | timer_type | Read through the P3 timers operation |
| DF-WRK-031 | timer | rwb_case | started_at | Read through the P3 timers operation |
| DF-WRK-035 | timer | rwb_case | status | Read through the P3 timers operation |
| DF-REF-274 to DF-REF-278 | rule_package | rwb_decision | all fields | Read through the P7 rule-package registry |
| DF-REF-279, DF-REF-281, DF-REF-282 | rule_package_version | rwb_decision | id, version_label, status | Read through the P7 rule-package registry |
| DF-REF-286, DF-REF-287 | rule_package_version | rwb_decision | valid_from, valid_to | Read through the P7 rule-package registry |
| DF-REF-002 | rule_row | rwb_decision | rule_id | Read through the P7 registry, by rule ID and package version |
| DF-REF-003 | rule_row | rwb_decision | rule_version | Read through the P7 registry, by rule ID and package version |
| DF-REF-008 | rule_row | rwb_decision | action_text | Read through the P7 registry, by rule ID and package version |
| DF-REF-010 | rule_row | rwb_decision | owner_role | Read through the P7 registry, by rule ID and package version |
| DF-REF-011 | rule_row | rwb_decision | timer_spec | Read through the P7 registry, by rule ID and package version |
| DF-REF-296 | rule_row | rwb_decision | package_version_id | Read through the P7 registry, by rule ID and package version |
| DF-REF-298 | rule_row | rwb_decision | outputs | Read through the P7 registry, by rule ID and package version |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | rwb_decision | all fields | Read through the P7 decision-log operation |

Three notes on ownership, each checked against the Ownership Map:

- `rwb_case` holds recovery_case, case_account, queue, task and timer and is owned by P3 rwb-case; the timer row is the screen projection behind the P3 timers operation, while the clock itself is the durable timer of the workflow (DP-10).
- `rwb_decision` holds rule_package, rule_package_version, rule_row, rule_test_case and decision_log_entry and is owned by P7 rwb-decision; the registry and the central ledger are the only source of the package, the version and the record.
- `rwb_integration` holds interface_config, job_catalog and outbound_item and is owned by P2 rwb-integration; the harness reads none of them directly and calls only the plan-status operation. `rwb_access` holds the roles, the scope and the rights, read through the session operation only; the harness reads no table of either schema.

The plan-status answer itself — planRef, status, statusDate, live and messageCode — is read as the contract payload of §12.2 and not from a table. Test data is synthetic: no production case, party, account or plan is used, and no personal data is written to a run report.

### 12. Contract

#### 12.1 REST operations provided

None. The harness provides no REST operation and serves no path.

#### 12.2 REST operations consumed

One hop per call, no chaining; the 2 s timeout and the breaker per downstream of DP-11 apply to every row. Every path is on the owner's `/api/recovery/<short>/v1` base (DP-13).

| Method | Path | Owner | Use |
|---|---|---|---|
| GET | `/api/recovery/integration/v1/cases/{caseId}/plan-status` | P2 rwb-integration | The plan status of the case: planRef, status, statusDate, live and messageCode, read from the ACE common module within 2 seconds with the stored value as fallback (AC1, AC3, AC4, AC9) |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The case facts the assertions rest on: the plan reference, the stored plan status and its date, the route state, the owner and the queue (AC1, AC2, AC3, AC9) |
| GET | `/api/recovery/case/v1/cases/{caseId}/timers` | P3 rwb-case | The timer the broken plan move started, its type, its start and its status (AC2, AC6) |
| GET | `/api/recovery/access/v1/me/session` | P4 rwb-access | The role, the scope and the Case record right the caller holds, asserted on both refusals (AC9; TC-E2-002-10-ITG) |
| GET | `/api/recovery/decision/v1/decision-log` | P7 rwb-decision | The decision log entries of the case, each with its rule ID and its package version (AC1, AC2, AC7, AC8) |
| GET | `/api/recovery/decision/v1/admin/rule-packages` | P7 rwb-decision | The RESTRUCTURE package and the version in force on the business date, and the empty answer of the no-package path (AC1, AC2, AC8) |

The case record plan section is read through the gateway-bff composite case-record route (DP-19), owned by the platform edge story RWB-PLT-N001-CON. Its path and its merge order are Not specified in the source documents (GAP-0386; ASM-0561).

#### 12.3 Events published

None. The harness publishes no Kafka event; it consumes as a test consumer with its own group.

#### 12.4 Events consumed

| Event | Topic | Owner | What the harness asserts |
|---|---|---|---|
| rwb.source-data.AceDataReady.v1 | rwb.source-data.events.v1 | P1 rwb-source-data | The business date is ready and the daily case update has run for 2026-12-15, so the status write and the route move of AC2 exist and the AC4 run of 2026-12-16 has a first date to retry from (AC1, AC2, AC4, AC6) |
| rwb.case.CaseStateChanged.v1 | rwb.case.events.v1 | P3 rwb-case | The route move is published once per move with its from and to route state. The event design gives no plan-status case event and the Ownership Map lists none, so the move is observed on this case event and no new event is invented (AC2, AC6) |
| CURE_PERIOD_EXPIRED | rwb.case.events.v1 | P3 rwb-case | The legacy event code of the plan event map (ACE status BROKEN with route state PLAN_CURE_PERIOD) is raised once for the case and not again on the rerun of 2026-12-15 (AC6) |
| rwb.decision-record.DecisionRecorded.v1 | rwb.decision-record.v1 | All 19 services; P7 rwb-decision seals the central ledger | One record per route move, carrying rule ID R-RES-29 or R-RES-30 and package version "RES-2026.12", and no record on the no-package and failed-record paths (AC2, AC7, AC8) |
| rwb.decision.RulePackageInForce.v1 | rwb.decision.events.v1 | P7 rwb-decision | The version in force on 2026-12-15 is "RES-2026.12" and no RESTRUCTURE version is in force on the AC8 business date, so the registry read and the event agree (AC1, AC2, AC8) |

The harness consumes these topics for assertion only, holds no inbox table of its own and publishes nothing.

#### 12.5 Workflows and activities

None added and none started. The harness starts no Temporal workflow, calls no activity and uses no task queue. The workflows and queues it observes are owned and started by the owning services:

| Workflow or step | Queue | Owner | What the harness observes |
|---|---|---|---|
| CaseWorkflow | rwb-case | P3 rwb-case | The route state moves, the task and the durable timer of the broken plan move (DP-10) |
| Plan-status step | rwb-integration | P2 rwb-integration | The ACE read and the plan-status answer of the case, with the 2 s budget (DP-11) |
| EvaluateRules activity | rwb-decision | P7 rwb-decision | The evaluation of package RESTRUCTURE with the version "RES-2026.12" and the record written with it (DP-03, DP-04) |

#### 12.6 Schedules

None. The schedule the step replaces is the legacy daily case update: the plan-status step of JOB-02, once a day after the case creation step. In the target it is an event-started run of DailyCaseRun in rwb-case from AceDataReady, with the plan-status step on `rwb-integration` and the timer held as a durable timer (DP-10), and JOB-05's five-minute timer check is retired. The harness starts neither the Schedule nor the workflow and creates no Schedule; a run is started by the test pipeline.

#### 12.7 Tables owned

None. The harness owns no table and no schema (DP-01, DP-15). It seeds and reads through the owning services' contracts only; the case, queue, task and timer tables in `rwb_case` are owned by P3 rwb-case, the registry and the decision log in `rwb_decision` by P7 rwb-decision, and the integration tables in `rwb_integration` by P2 rwb-integration.

#### 12.8 Contract fakes

| Fake | Serves | Stubbed answers |
|---|---|---|
| rwb-integration (WireMock, from its OpenAPI) | `GET /api/recovery/integration/v1/cases/{caseId}/plan-status` | "APPROVED" with status date 2026-12-10; "BROKEN" with 2026-12-14; no status for "TDR-SYN-0310"; an answer beyond 2 seconds; "SUSPENDED"; the stored "BOOKED" with 2026-12-01 as the fallback; the refusals of AC9 |
| rwb-case (WireMock, from its OpenAPI) | `GET /api/recovery/case/v1/cases/{caseId}` and `GET /api/recovery/case/v1/cases/{caseId}/timers` | The case "RW-2026-000310" with "A-0310", the stored plan status and date, route state "PLAN_CURE_PERIOD" and then "PLAN_BROKEN" and "BACK_TO_ROUTE_DECISION", the case owner's queue, the task due 5 working days after 2026-12-15, and the timer of the move |
| rwb-access (WireMock, from its OpenAPI) | `GET /api/recovery/access/v1/me/session` | RW-CASEOWN in scope; RW-REFADM without the Case record right; a caller whose scope excludes the case; the exception-queue role RW-TEAMMGR |
| rwb-decision (WireMock, from its OpenAPI) | `GET /api/recovery/decision/v1/decision-log` and `GET /api/recovery/decision/v1/admin/rule-packages` | The two entries of the broken plan move naming R-RES-29 and R-RES-30 with "RES-2026.12"; the empty decision log of the no-package path; "RES-2026.12" in force with rows R-RES-29, R-RES-30, R-RES-31 and R-LIT-02 and their timer_spec; the no-version-in-force answer of AC8 |
| rwb-source-data (WireMock, from its OpenAPI) | The business-date readiness the daily update follows | AceDataReady for 2026-12-15 and for 2026-12-16, so the AC4 retry has its own run |
| ACE common module stub (RestructurePlanQuery), served behind rwb-integration | The plan read of the P2 operation | Plan "TDR-SYN-0310" for "A-0310" with "APPROVED" 2026-12-10, "BROKEN" 2026-12-14, no plan, a 3-second delay and "SUSPENDED" |
| gateway-bff composite case-record route (WireMock) | One gateway answer composing the case facts, the plan status and its message code | The plan section of AC1 and the stored-value answer of AC3; the path and the merge order are Not specified in the source documents (GAP-0386; ASM-0561) |

The fakes are published from the owning services' OpenAPI documents and are versioned with the harness pack; the ACE common module stub is the only outside-system stand-in, and it is served behind rwb-integration so that no service and no test calls an outside system directly.

#### 12.9 Call-type summary

| Call type | In this story |
|---|---|
| REST | 0 provided, 6 consumed, each one hop on the owner's `/api/recovery/<short>/v1` base with a 2 s timeout (DP-11, DP-13) |
| Kafka | 0 published, 5 consumed over five rows and four topics: `rwb.source-data.AceDataReady.v1` on `rwb.source-data.events.v1`, `rwb.case.CaseStateChanged.v1` and the legacy event code CURE_PERIOD_EXPIRED on `rwb.case.events.v1`, `rwb.decision.RulePackageInForce.v1` on `rwb.decision.events.v1`, and `rwb.decision-record.DecisionRecorded.v1` on `rwb.decision-record.v1` |
| Temporal | None started: no workflow, no activity, no queue `rwb-case`, `rwb-integration` or `rwb-decision`; the run is started by the test pipeline |
| File | None |

### 13. Solution plan

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

The H and C dependencies the table adds — RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, C RWB-P7-E1073-CON, RWB-PLT-E1042-CON, C RWB-P3-E1042-CON, RWB-PLT-E1043-CON, C RWB-P3-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-E1044-CON and RWB-PLT-N001-CON — are held by the service and platform stories and are not repeated in the metadata columns, which stay "None". The real gate of this story is its five I stories: they replace the fakes with the real plan-status read, the case write, the rights check, the embedded Drools evaluation and the registry. DP-15 resolves to no migration because the harness owns no schema, and DP-05 resolves to no ACE view: the plan comes from the ACE common module's published interface (INT-34) behind rwb-integration's operation, and no service and no test reads a `v_ace_*` view for it.

**Harness components**

| Component | Type | Responsibility |
|---|---|---|
| PlanStatusJourneyRunner | Test harness | Runs the eleven `-ITG` cases of §16 as one run per business date, in fake or real mode per service, and stops at the first failed assertion with the trace |
| PlanStatusClient | Harness adapter | Calls the six consumed operations of §12.2 through one hop with the 2 s timeout, and records each answer |
| AcePlanStatusStub | Stub | Serves the ACE common module RestructurePlanQuery answers behind rwb-integration: "APPROVED" 2026-12-10, "BROKEN" 2026-12-14, no plan, a 3-second delay and "SUSPENDED" |
| RulePackageFixtureLoader | Service | Puts version "RES-2026.12" of package "RESTRUCTURE" in force with rows R-RES-29, R-RES-30, R-RES-31 and R-LIT-02 through the P7 registry, and withdraws it for the AC8 run; it never writes a rule row |
| FakePack | WireMock project | Serves rwb-integration, rwb-case, rwb-access, rwb-decision, rwb-source-data and the gateway-bff route of §12.8 from the published OpenAPI documents |
| StateChangeAsserter | Assertion | Asserts the stored plan status and its date, the route state change, the queue, the task due date from the timer_spec and the durable timer of the move |
| DecisionRecordAsserter | Assertion | Asserts one entry per move, its rule ID and package version "RES-2026.12", its absence on the no-package path and its single write after the AC7 retry |
| BreakAsserter | Assertion | Asserts the product "DP04" break of the missing status and the "Lists of values" break of the unknown code, with the plan reference and the code |
| BoundaryCheck | Assertion | Fails the run on a cross-schema read in the trace, on a call chain deeper than one hop, on a call above 2 seconds, and on a package or version that does not come from the rwb-decision registry (AC9) |
| RunLock | Service | One run at a time in the harness environment |
| EvidenceReportPublisher | Reporter | Writes the per-run evidence report keyed by story id and business date; the format and the retention are Not specified in the source documents (GAP-0386; ASM-0561) |
| JourneyGate | Assertion | Passes the run only when every owned criterion passes, and fails it naming the criterion, the seam and the observed value |

**Environment and test data.** SIT for the run of record and UAT for the acceptance run, with `rwb.integration.ace-plan-status` on in both. The data are the synthetic seeds of the legacy story: case "RW-2026-000310" with account "A-0310" and plan "TDR-SYN-0310"; package "RESTRUCTURE" version "RES-2026.12" with rows R-RES-29, R-RES-30, R-RES-31 and R-LIT-02; the plan event map rows and LOV-PLAN-STATUS; the parameter `restructure.max_breaks` = 2; the ACE stub statuses "APPROVED" 2026-12-10, "BROKEN" 2026-12-14, no plan, a 3-second delay and "SUSPENDED"; the business dates 2026-12-10, 2026-12-11, 2026-12-14, 2026-12-15 and 2026-12-16; the roles RW-CASEOWN in scope, RW-REFADM without the Case record right and RW-TEAMMGR for the exception queue. Each run starts from the seeded state, so a repeated run is deterministic. The harness repository, the environments, the seeding mechanism, the evidence format and its retention and the gate are Not specified in the source documents (GAP-0386; ASM-0561).

**Build steps**

1. Build PlanStatusJourneyRunner and PlanStatusClient against the published OpenAPI documents of the five services and the gateway-bff route, with the run lock, the build under test and the fake or real mode recorded per run.
2. Publish FakePack for the five services and the composite route from the same documents, with the ACE common module stub behind rwb-integration, and prove the harness runs green from Day 1 on the fakes.
3. Write the seed pack and RulePackageFixtureLoader: the case, the account, the plan, the version "RES-2026.12" with its four rows, the plan event map rows, LOV-PLAN-STATUS and the parameter, all through the owning contracts.
4. Write StateChangeAsserter for AC1, AC2 and AC3, with a unit test on fixtures for the stored status and date, the route state change, the queue, the due date from the timer_spec and the timer read.
5. Write DecisionRecordAsserter for AC2, AC7 and AC8, including the failed-record run, the single write after the retry and the empty answer of the no-package path.
6. Write BreakAsserter for AC3 and AC5 and the timeout, retry and inbox-hit assertions of AC4 and AC6.
7. Write BoundaryCheck and the refusal assertions of AC9, and make the run fail on the first boundary broken.
8. Replace each fake with the real service as its I story lands, in the order rwb-integration, rwb-case, rwb-access, rwb-decision and the rwb-decision registry, rerun in UAT, and attach the evidence report to the release record.

**Feature switch.** `rwb.integration.ace-plan-status`, the legacy switch of this story: on in SIT and UAT. The harness asserts the off state on the fakes — the step writes no status, the operation answers from the stored value and the route state does not move — and asserts that the case record section shows the stored status and date only.

**Done when.** The eleven `-ITG` test cases of section 16 pass in SIT and UAT with the five I stories in place and not only against the fakes; the evidence report for the run is attached to the release record with the nine owned criteria green; the access and Principle 5 cases are green with MSG-P4-002 and MSG-P7-003; and the boundary checks of AC9 are green, so no cross-schema read, no second hop, no call above 2 seconds and no package or version from outside the registry appears in the trace.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P2-008 | Plan status shown from the stored value | The ACE plan status is from {date}. Today's status was not returned. |
| MSG-GEN-006 | ACE common module unavailable | {system} is not available. Your request is queued and will be retried. |
| MSG-P7-003 | Decision log write failed on a broken plan | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P3-027 | No RESTRUCTURE version is in force | The rule version was refused at the {check} check: {detail}. |
| MSG-P4-002 | A role without the Case record right | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | Case outside the caller's scope | This case is not in your scope. |

The harness asserts the message ID and the substituted values: the date 2026-12-01 in MSG-P2-008, "ACE common module" in MSG-GEN-006, the check "no package in force" with the package code "RESTRUCTURE" and the business date in MSG-P3-027, and the refused action in MSG-P4-002. It never rewrites the text, and Thai text for each message follows decision DL10.

### 15. Screens and states

| Screen | State | What the harness asserts |
|---|---|---|
| SCR-03 Case record | Read only | The plan section is read through the composite route and shows plan "TDR-SYN-0310" with "Approved" and date 2026-12-10 (AC1), and then "BROKEN" with date 2026-12-14 after the 2026-12-15 update (AC2) |
| SCR-03 Case record | Loading, stored value | The answer carries MSG-P2-008 with date 2026-12-01 and the stored "BOOKED", and no status changes (AC3, AC4) |
| SCR-14 Treatment record | Broken | The broken plan is shown once the case returns to the route decision, so the route state "BACK_TO_ROUTE_DECISION" is the state the harness asserts (AC2) |
| SCR-38 Decision log query | Read only | The decision log entries of the case are read as one ordered answer through the P7 contract, each naming its rule ID and version "RES-2026.12" (AC2, AC7, AC8) |

The harness builds no screen and renders no page: it asserts the composite route answer and the contract answers the screens consume. The case record plan section and the plan status panel remain with RWB-P3-E2002-APP, the refusals with RWB-P4-E2002-APP, and the decision log query screen with P7. The composite route path and merge order are Not specified in the source documents (GAP-0386; ASM-0561).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-002-10-ITG | Access; ITG AC9 | Component | RW-REFADM (no Case record right) calls GET /cases/{caseId}/plan-status; refused with MSG-P4-002 |
| TC-E2-002-01-ITG | AC1, BR1, BR2, BR6, BR10; ITG AC1 | Integration | ACE stub plan TDR-SYN-0310 APPROVED |
| TC-E2-002-02-ITG | AC2, BR4, BR5, BR10; ITG AC2 | Integration | Case in PLAN_CURE_PERIOD; ACE plan BROKEN |
| TC-E2-002-03-ITG | AC3, BR7; ITG AC3 | Integration | ACE stub returns no plan |
| TC-E2-002-04-ITG | AC4; ITG AC4 | Integration | ACE stub delayed 3 seconds |
| TC-E2-002-05-ITG | AC5, BR3; ITG AC5 | Integration | ACE stub returns SUSPENDED |
| TC-E2-002-06-ITG | AC6, BR9; ITG AC6 | Integration | Step run twice on 2026-12-15 |
| TC-E2-002-07-ITG | AC7, BR8; ITG AC7 | Integration | Decision log store stopped |
| TC-E2-002-08-ITG | AC8; ITG AC9 | Integration | Case owner with scope Own and a case of another owner |
| TC-E2-002-09-ITG | AC9, BR11; ITG AC8 | Integration | No RESTRUCTURE version in force on 2026-12-15 |
| TC-E2-002-11-ITG | Principle 5; ITG AC7 | NFR | Decision log write forced to fail on the R-RES-29 move; route state unchanged |

The legacy criteria of this key stay with the app stories: AC1 to AC9 of RWB-E2-002 are owned by RWB-P2-E2002-APP, RWB-P3-E2002-APP, RWB-P4-E2002-APP, RWB-P7-E2002-APP and RWB-P3-E2042-APP, and this story owns none of them. The eleven `-ITG` cases assert the same behaviour as the legacy test cases under the same base id and add the seam each one exercises across services; the legacy AC column in Covers is the legacy criterion the copy derives from and the ITG AC is the criterion of §7 the copy proves at integration level. The access case and the Principle 5 case keep their legacy Level of the app stories as Component and NFR. The full legacy test, with its Given, When and Then, is in the Test Cases workbook, tab Story test cases, under the legacy test case ID.

### 17. Guardrails

- No business value in code: the status list, the plan event map, the maximum breaks, the batch size, the timeout, the rule rows and the package versions are rows, parameters or properties held by the owning services; the harness reads them through the contracts and never holds a copy.
- No personal data in logs, tests, workflow inputs, traces or reports: the harness uses synthetic identifiers only — the case, the plan reference, the rule IDs, the statuses, the dates and the counts — and writes no account number to a run report.
- ACE data only through the owner's contract: the plan comes from the ACE common module through rwb-integration's operation, the harness reads no ACE table and no `v_ace_*` view, and no service reads another service's schema (DP-01, DP-05). The BoundaryCheck fails the run on a cross-schema reference.
- Rules only from the registry: the package and the version of every evaluation come from rwb-decision, the harness never loads a rule row or a package version of its own, and it reads no DRL and no workbook (DP-04).
- One hop only: the harness fails a run when the trace shows a call chain deeper than the gateway and one owner, or a call above the 2 s budget (DP-11).
- The harness owns nothing: no table, no schema, no endpoint, no screen, no workflow, no Schedule and no production feature flag (DP-01, DP-10, DP-15); it is test and evidence only.
- The read path writes nothing: the harness asserts that a read of the plan status, a refusal and a repeated run leave every stored value unchanged.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-013 | Plan status read from the ACE common module | Program 5.2; Epic 2 3.2 | FEAT-CHO-02 | 7.3 Negotiate settlement or deed in lieu | R-UNI-39, R-UNI-40 | TC-E2-002-01-ITG, TC-E2-002-04-ITG, TC-E2-002-06-ITG, TC-E2-002-07-ITG |
| REQ-CHO-002 | Plan status change visible on the case | Program 5.3; Epic 2 3.2 | FEAT-CHO-02 | 7.3 Negotiate settlement or deed in lieu | R-RES-29, R-RES-30, R-RES-31, R-LIT-02 | TC-E2-002-02-ITG, TC-E2-002-03-ITG, TC-E2-002-05-ITG, TC-E2-002-08-ITG, TC-E2-002-09-ITG |

The two requirements keep the legacy BRD section, the feature, the L3 process and the rule text of RWB-E2-002. The access case and the Principle 5 case (TC-E2-002-10-ITG and TC-E2-002-11-ITG) are the copies of the legacy Access and Principle 5 cases and trace to the same two requirements through MSG-P4-002 and MSG-P7-003 at integration level.

### 19. Out of scope

- The five owning I stories and everything they build: RWB-P2-E2002-APP (the ACE plan-status read and the plan-status operation), RWB-P3-E2002-APP (the plan status on the case, the route state, the task and the timer), RWB-P4-E2002-APP (the rights and the scope check), RWB-P7-E2002-APP (the embedded Drools evaluation and the local decision record) and RWB-P3-E2042-APP (the rule packages and their versions).
- The nine acceptance criteria of RWB-E2-002, which stay with those app stories; this story owns no legacy criterion and its `-ITG` cases add only the seam.
- Production code in any service: the harness is test and evidence only.
- The contract baselines of rwb-integration, rwb-case, rwb-access, rwb-decision and rwb-source-data, which their CON stories own.
- Platform deployment, the gateway-bff composite route implementation (RWB-PLT-N001-CON) and the platform configuration of Kafka, Temporal and the observability stack.
- Creating or changing a plan: ACE, under DL14.
- Authoring, approval, rollback and promotion of package RESTRUCTURE: RWB-E2-042 and RWB-E1-073.
- The neighbouring integration stories of the same wave: RWB-E2-001 (EFS hand-over with full history from the COLLINS load), RWB-E2-004 (treatment entity and plan timers data model) and RWB-E2-003.
- The booking confirmation of the plan (RWB-E2-007), the full restructure route in the Workbench (Epic 3) and the treatment record and plan timers of RWB-E2-004.
