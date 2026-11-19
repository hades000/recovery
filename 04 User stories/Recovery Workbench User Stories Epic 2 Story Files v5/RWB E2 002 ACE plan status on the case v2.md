# RWB-E2-002 ACE plan status on the case

SCB Collections and Recovery. Henka Group, 16 November 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E2-002 |
| Epic | E2, release 31 December 2026 |
| Module | P2 Integration |
| Feature | FEAT-CHO-02 Read the ACE plan status |
| Requirement IDs | REQ-DRI-013, REQ-CHO-002 |
| BRD section | Business Requirements Epic 2, section 3.2; Business Requirements Program, sections 5.2 and 5.3 |
| L3 process | 7.3 Negotiate settlement or deed in lieu |
| Decision | D-RCV-36; ADR-012 |
| Priority | Must |
| Depends on | RWB-E2-001, RWB-E1-072, RWB-E2-042 |
| Status | Ready for build |

## 1. Story

As a **case owner (RW-CASEOWN)**, I want **the restructure plan status from the ACE common module (created, approved, booked, broken) on the case**, so that **a case with a live plan is never treated as if it had none, and a broken plan returns the case to me the next morning**.

## 2. Business rationale

Restructure plans are calculated and held in ACE (DL14). Without the plan status on the case, a recovery officer can start litigation on a customer who is paying a plan, or miss a plan that broke. This story reads the status from the ACE common module each morning and on each case view, keeps the last known status with its date when ACE returns none, and raises the broken plan to the restructure rules. It meets REQ-CHO-002 and REQ-DRI-013.

The restructure rules R-RES-29, R-RES-30, R-RES-31 and R-LIT-02 are rows of package RESTRUCTURE under ADR-012, fixed by D-RCV-36 on 16 November 2026. SY-RULES evaluates them through RuleEvaluator, the result names the rule and the package version, and the decision log records both. The action text, the owner role and the timer spec of the row are read from RuleCatalog. The measure is that a broken plan is back with the case owner the next morning and no case with a live plan is treated as if it had none.

## 3. Preconditions

- RWB-E2-001 (case creation from the ACE data) is done.
- RWB-E1-072 is done: RuleEvaluator, RuleCatalog and the rule package store exist, and DecisionLogWriter records the rule ID and the package version.
- RWB-E2-042 is done: package RESTRUCTURE is in force with rows R-RES-29, R-RES-30, R-RES-31 and R-LIT-02, and each row carries action_text, owner_role and timer_spec.
- The ACE common module publishes RestructurePlanQuery in SIT and UAT (INT-34; DL14).
- The account number is the join key between the case and the ACE plan (DL21).
- The plan event map rows are loaded: ACE status BROKEN with route state PLAN_CURE_PERIOD maps to event CURE_PERIOD_EXPIRED; BROKEN with any other route state maps to TREATMENT_BROKEN.
- Parameter `restructure.max_breaks` = 2 is in force (Restructure route set: a second break bars a further restructure).

## 4. Flow

1. Scheduler: the plan status step runs in JOB-02 after the case creation step, once a day.
2. The recovery service identity: the PlanStatusService lists every open case with its account numbers through the P3 CaseQuery.
3. The recovery service identity: calls RestructurePlanQuery.statusFor with the account numbers in batches of 500 (assumed; DL11).
4. The recovery service identity: for each plan returned, compares status and status date with the stored values; an unchanged plan is skipped.
5. SY-CASEWF: writes plan_ref, plan_status and plan_status_as_of on the case through CasePlanStatus.update.
6. The recovery service identity: on a change to BROKEN, looks up the event in the plan event map and calls CaseEvents.raise with plan_status = broken and the break count.
7. SY-RULES and SY-CASEWF: SY-RULES builds RestructureFacts for the case (route state, plan_status, break_count, prior_route) and calls RuleEvaluator.evaluate("RESTRUCTURE", facts, businessDate); the result names the rule, the package version and the outputs. SY-CASEWF writes the decision log entry with that rule ID and package version, then reads action_text, owner_role and timer_spec from RuleCatalog.row(ruleId, packageVersion), moves the route state and places the case in the case owner's queue with a task due by the timer spec.
8. Case owner: opens the case record view; the front end calls GET /cases/{caseId}/plan-status, which reads ACE live with a 2-second timeout and falls back to the stored status.
9. The recovery service identity: for a case with a stored plan that ACE no longer returns, keeps the stored status and date and writes a break for the data steward and the ACE team.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | ACE returns no status for a plan the case holds | The case keeps its last known status and date; a break on the data quality console lists the plan for the ACE team | MSG-P2-008 | AC3 |
| X2 | The ACE common module is unavailable or does not answer in 2 seconds | The daily step keeps every stored status and retries in the next run; the view shows the stored status | MSG-GEN-006, MSG-P2-008 | AC4 |
| X3 | ACE returns a status code not in the plan status list | The status is not stored; a break with check "Lists of values" is written | None | AC5 |
| X4 | The daily step runs twice for the same day | No status is written twice and no event is raised twice | None | AC6 |
| X5 | The decision log write fails during the broken plan move | The route state does not move; an incident is raised; the event is raised again in the next run | MSG-P7-003 | AC7 |
| X6 | A user reads the plan status of a case outside their scope | Refused | MSG-P4-003 | AC8 |
| X7 | A role without the Case record right reads the plan status | Refused; nothing changes | MSG-P4-002 | TC-E2-002-10 |
| X8 | No RESTRUCTURE version is IN_FORCE on the business date | NoPackageInForce; no decision log entry is written and the route state does not move; the case goes to the exception queue for a person | MSG-P3-027 | AC9 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the cases from RWB-E2-001, the ACE interface, the evaluator of RWB-E1-072 and the RESTRUCTURE package of RWB-E2-042 |
| Negotiable | The event map, batch size, timeout, maximum breaks and package version are data rows or properties |
| Valuable | No action is taken on a case with a live plan without the plan in view |
| Estimable | One service, one job step, one endpoint, one map table, one rule package |
| Small | Within two weeks with its tests |
| Testable | Each criterion below is one automated test |

## 7. Acceptance criteria

```gherkin
Feature: ACE plan status on the case

  Background:
    Given case "RW-2026-000310" is open with synthetic account "A-0310"
    Given the ACE common module stub holds plan "TDR-SYN-0310" for "A-0310"
    Given package "RESTRUCTURE" version "RES-2026.12" is in force with rows R-RES-29, R-RES-30, R-RES-31 and R-LIT-02

  Scenario: AC1 Plan status on the case
    Given plan "TDR-SYN-0310" has status "APPROVED" in ACE with status date 2026-12-10
    When the case record view loads on 2026-12-11
    Then the case shows plan "TDR-SYN-0310" with status "Approved" and date 2026-12-10
    Then RuleEvaluator.evaluate("RESTRUCTURE", facts, 2026-12-11) reads plan_status "APPROVED" for the case
    Then rule R-LIT-02 does not fire for the case because plan_status is not broken

  Scenario: AC2 Broken plan
    Given the case is in route state "PLAN_CURE_PERIOD" with break count 0
    Given plan "TDR-SYN-0310" has status "BROKEN" in ACE with status date 2026-12-14
    When the daily case update runs on 2026-12-15
    Then the case plan status is "BROKEN" with date 2026-12-14
    Then the route state moves to "PLAN_BROKEN" by R-RES-29 and then to "BACK_TO_ROUTE_DECISION" by R-RES-30
    Then the case is in the case owner's queue with a task due in 5 working days, from timer_spec "5 working days" of row R-RES-30 of version "RES-2026.12"
    Then the system writes a decision log entry for each move with the rule ID and the package version "RES-2026.12"

  Scenario: AC3 Status not available
    Given the case holds plan "TDR-SYN-0310" with status "BOOKED" and date 2026-12-01
    Given ACE returns no status for "TDR-SYN-0310"
    When the daily case update runs on 2026-12-15
    Then the case keeps status "BOOKED" with date 2026-12-01
    Then the case record view shows message MSG-P2-008 with the date 2026-12-01
    Then a break with product "DP04" lists plan "TDR-SYN-0310" for the ACE team

  Scenario: AC4 ACE unavailable
    Given the ACE common module does not answer within 2 seconds
    When the daily case update runs on 2026-12-16
    Then the system changes no plan status
    Then the run summary carries message MSG-GEN-006 with system "ACE common module"
    Then the next run retries every case

  Scenario: AC5 Unknown status code
    Given ACE returns status "SUSPENDED" for plan "TDR-SYN-0310"
    When the daily case update runs
    Then the stored status does not change
    Then a break with check "Lists of values" names the code "SUSPENDED"

  Scenario: AC6 Daily step run twice
    Given the daily case update on 2026-12-15 stored status "BROKEN" for plan "TDR-SYN-0310"
    When the step is rerun on 2026-12-15
    Then the system writes no status row
    Then the system raises no second CURE_PERIOD_EXPIRED event for the case

  Scenario: AC7 Decision log write fails on a broken plan
    Given the decision log store is unavailable
    When the daily case update finds plan "TDR-SYN-0310" broken
    Then the route state stays "PLAN_CURE_PERIOD"
    Then the system raises an incident with message MSG-P7-003
    Then the system raises the event again in the next run

  Scenario: AC8 Case outside the scope
    Given a case owner whose scope is "Own" and case "RW-2026-000310" is owned by another person
    When the case owner calls GET /cases/{caseId}/plan-status for it
    Then the response is 404 with message MSG-P4-003

  Scenario: AC9 No RESTRUCTURE version in force
    Given no RESTRUCTURE version is IN_FORCE on 2026-12-15
    When the daily case update finds plan "TDR-SYN-0310" broken on that date
    Then NoPackageInForce is thrown with MSG-P3-027 for package "RESTRUCTURE"
    Then no decision log entry is written and the route state stays "PLAN_CURE_PERIOD"
    Then the case goes to the exception queue for role "RW-TEAMMGR" with the gap
```

## 8. Business rules

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

## 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| PLAN_CURE_PERIOD | CURE_PERIOD_EXPIRED | ACE plan status BROKEN | PLAN_BROKEN |
| PLAN_BROKEN | BREAK_RECORDED | break_count < max_breaks | BACK_TO_ROUTE_DECISION |
| PLAN_BROKEN | BREAK_RECORDED | break_count >= max_breaks | RESTRUCTURE_BARRED |
| LIT_ROUTE_APPROVED | TREATMENT_BROKEN | plan_status = broken and prior_route in (R1, R2) | NOTICE_GENERATED |

These are route states (recovery_case.route_state); the case status stays "In progress". The story also writes the stored plan status.

## 10. Authority

| Who | What they may do in this story |
|---|---|
| The recovery service identity | Calls the ACE interface and writes the stored plan status through P3 |
| SY-RULES, Drools evaluator | Evaluates package RESTRUCTURE (R-RES-29, R-RES-30, R-RES-31 and R-LIT-02) and reads the catalog row |
| SY-CASEWF, case workflow module | Writes the decision log entry, moves the route state, places the case in the queue, raises the task |
| SY-DECLOG, decision log writer | Writes each entry (Decision log, C) |
| RW-CASEOWN, case owner | Reads the plan status on cases in scope (Case record, R) |
| RW-RESTRUCT, restructuring officer | Reads the plan status on cases in scope (Case record, R) |
| RW-DATASTEW, RW-PLATADM | Read the breaks for the ACE team (Platform administration, R) |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | recovery_case | id | Read |
| DF-CAS-007 | recovery_case | route_state | Write, through the P3 interface |
| DF-CAS-009 | recovery_case | owner_user_id | Read |
| DF-CAS-010 | recovery_case | queue_id | Write, through the P3 interface |
| DF-CAS-046 | recovery_case | plan_ref | Write |
| DF-CAS-047 | recovery_case | plan_status | Write |
| DF-CAS-048 | recovery_case | plan_status_as_of | Write |
| DF-CAS-026 | case_account | account_key | Read |
| DF-ACE-002 | v_ace_account | account_code | Read |
| DF-WRK-018 | task | case_id | Write, through the P3 interface |
| DF-WRK-019 | task | task_code | Write, through the P3 interface |
| DF-WRK-024 | task | due_at | Write, through the P3 interface |
| DF-REF-002 | rule_row | rule_id | Read |
| DF-REF-003 | rule_row | rule_version | Read |
| DF-REF-008 | rule_row | action_text | Read |
| DF-REF-010 | rule_row | owner_role | Read |
| DF-REF-011 | rule_row | timer_spec | Read |
| DF-REF-296 | rule_row | package_version_id | Read |
| DF-REF-298 | rule_row | outputs | Read |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Write |

Field IDs are those in the Logical Data Model and Data Dictionary. The rule_row fields are read by rule ID and package version through RuleCatalog.row and the evaluation result; the story reads no drl_source and no workbook, and it holds no rule table of its own.

## 12. Contract

**Job step: plan status in JOB-02 Case creation.** Trigger: after the case creation step of JOB-02, daily. Input: open cases and their account numbers; ACE plan statuses. Output: stored plan status per case; rule events for broken plans; breaks for the data steward. Rule evaluation: RuleEvaluator.evaluate("RESTRUCTURE", facts, businessDate) for each case whose status changed, with the rule ID and the package version written to the decision log. The package is loaded, approved and rolled back through RWB-E1-073 and RWB-E2-042; this story only evaluates it. Events published: CaseStateChanged (EV-05) by P3 for each route move. Idempotency key: case ID + plan reference + status + status date. Restart: a rerun skips every case whose stored status and date equal the ACE values.

**Endpoint (new, recorded in additions).**

| Method and path | Request | Response | Errors | Authorization | Idempotency |
|---|---|---|---|---|---|
| GET /api/recovery/v1/cases/{caseId}/plan-status | Path: caseId | PlanStatus: planRef, status, statusDate, live (true when read from ACE now), messageCode | 401 (MSG-P4-001); 403 no Case record right (MSG-P4-002); 404 not found or out of scope (MSG-P4-003) | Case record, R | Read only; writes nothing |

**Published interfaces called.**

```java
// P3 recovery.casewf.rules (published, RWB-E1-072)
RuleResult RuleEvaluator.evaluate(String packageCode, Object facts, LocalDate onDate); // throws NoPackageInForce
RuleRow RuleCatalog.row(String ruleId, String packageVersion);
// ACE common module
List<PlanStatusView> RestructurePlanQuery.statusFor(List<String> accountNos); // planRef, accountNo, status, statusDate
// P3 recovery.casewf.api
void CasePlanStatus.update(UUID caseId, String planRef, String status, LocalDate statusDate);
void CaseEvents.raise(UUID caseId, String eventCode, Map<String, Object> facts); // throws DecisionLogUnavailableException
```

## 13. Solution plan

- **Package.** folder `src/main/java/recovery/integration/aceplan`, Java package `recovery.integration.aceplan`; front end `src/modules/recovery/case/PlanStatusPanel.tsx`.

| Component | Type | Responsibility |
|---|---|---|
| PlanStatusController | Controller | GET /cases/{caseId}/plan-status with the scope check |
| PlanStatusService | Service | Daily compare and write; event lookup; exceptions; live read with timeout and fallback |
| AcePlanClient | Service | Wraps RestructurePlanQuery with batching and the 2-second timeout |
| PlanEventMap | Reference table | Rows: ACE status, route state, rule event; versioned reference data, not a rule table |
| PlanStatusStep | Job | Step of JOB-02 |
| RestructureFacts | Fact builder | Builds the facts for one case: route state, plan_status, break_count and prior_route |
| PlanStatusPanel | React component | Shows plan, status, date and MSG-P2-008 when not live |

- **Database:** the three new recovery_case columns plan_ref varchar(30), plan_status varchar(10), plan_status_as_of date are added by P3 in its migration for this story; no P2 table.
- **Configuration and reference data:** plan event map rows (RW-COE); new list LOV-PLAN-STATUS with CREATED, APPROVED, BOOKED, BROKEN (RW-COE); parameter restructure.max_breaks = 2; package RESTRUCTURE rows R-RES-29, R-RES-30, R-RES-31 and R-LIT-02 (RW-COE, RWB-E2-042); properties `rwb.ace.plan.batch-size` = 500 and `rwb.ace.plan.timeout-ms` = 2000 (assumed; DL11). The package version in force per environment is recorded in `config/rule-packages.lock`; the values in this story are as at 16 November 2026.
- **Build steps:**
  1. Build AcePlanClient against a stub of RestructurePlanQuery with batching and the timeout.
  2. Build PlanStatusService compare and write with the idempotency key.
  3. Build RestructureFacts and the RuleEvaluator call with the catalog read for action text, owner role and timer spec.
  4. Build the event lookup with PlanEventMap and the CaseEvents.raise call; handle DecisionLogUnavailableException and NoPackageInForce.
  5. Build the exception writes for no status, unknown codes and the no-package path.
  6. Build PlanStatusStep in JOB-02.
  7. Build the endpoint with live read and fallback, and PlanStatusPanel.
- **Feature flag:** `rwb.integration.ace-plan-status`.
- **Done when:** the tests in section 16 pass and the SIT run against the ACE stub moves a broken plan case to the case owner's queue, with the rule ID and the package version on every decision log entry.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P2-008 | Plan status shown from the stored value | The ACE plan status is from {date}. Today's status was not returned. |
| MSG-GEN-006 | ACE common module unavailable | {system} is not available. Your request is queued and will be retried. |
| MSG-P7-003 | Decision log write failed on a broken plan | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P3-027 | No RESTRUCTURE version is in force | The rule version was refused at the {check} check: {detail}. |
| MSG-P4-003 | Case outside the caller's scope | This case is not in your scope. |
| MSG-P4-002 | A role without the Case record right | You cannot {action} here. Your role does not include it. |

For MSG-P3-027 in this story, {check} is "no package in force" and {detail} names the package code "RESTRUCTURE" and the business date only, never a case fact.

## 15. Screens and states

SCR-03 Case record, states loading and read only: the plan status panel shows the plan reference, status, date and, when not live, MSG-P2-008. SCR-14 Treatment record, state broken, shows the broken plan once the case returns to the route decision.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-002-01 | AC1, BR1, BR2, BR6, BR10 | System | ACE stub plan TDR-SYN-0310 APPROVED |
| TC-E2-002-02 | AC2, BR4, BR5, BR10 | System | Case in PLAN_CURE_PERIOD; ACE plan BROKEN |
| TC-E2-002-03 | AC3, BR7 | System | ACE stub returns no plan |
| TC-E2-002-04 | AC4 | Resilience | ACE stub delayed 3 seconds |
| TC-E2-002-05 | AC5, BR3 | System | ACE stub returns SUSPENDED |
| TC-E2-002-06 | AC6, BR9 | System | Step run twice on 2026-12-15 |
| TC-E2-002-07 | AC7, BR8 | System | Decision log store stopped |
| TC-E2-002-08 | AC8 | System | Case owner with scope Own and a case of another owner |
| TC-E2-002-09 | AC9, BR11 | System | No RESTRUCTURE version in force on 2026-12-15 |
| TC-E2-002-10 | Access | Access | RW-REFADM (no Case record right) calls GET /cases/{caseId}/plan-status; refused with MSG-P4-002 |
| TC-E2-002-11 | Principle 5 | Resilience | Decision log write forced to fail on the R-RES-29 move; route state unchanged |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: status codes, the event map, maximum breaks, batch size, timeout, rule rows and package versions are rows or properties.
- No personal data in logs, tests, workflow history or prompts: logs hold case IDs and plan references, never account numbers.
- No read of another module's tables; ACE data only through recovery.v_ace_* views: the plan comes from RestructurePlanQuery and no ACE table is read.
- A read of the plan status writes nothing.
- The rule package is loaded and approved through RWB-E1-073; this story evaluates it and never reads drl_source or the workbook.
- The decision log entry is written before the route state moves.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-013 | Plan status read from the ACE common module | Program 5.2; Epic 2 3.2 | FEAT-CHO-02 | 7.3 Negotiate settlement or deed in lieu | R-UNI-39, R-UNI-40 | TC-E2-002-01, TC-E2-002-04, TC-E2-002-06, TC-E2-002-07 |
| REQ-CHO-002 | Plan status change visible on the case | Program 5.3; Epic 2 3.2 | FEAT-CHO-02 | 7.3 Negotiate settlement or deed in lieu | R-RES-29, R-RES-30, R-RES-31, R-LIT-02 | TC-E2-002-02, TC-E2-002-03, TC-E2-002-05, TC-E2-002-08, TC-E2-002-09 |

## 19. Out of scope

- Creating or changing a plan: ACE, under DL14.
- The treatment record and plan timers: RWB-E2-004.
- Booking confirmation of the plan: RWB-E2-007.
- Authoring, approval and rollback of package RESTRUCTURE: RWB-E2-042 and RWB-E1-073.
- The full restructure route in the Workbench: Epic 3.
