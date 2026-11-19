<!-- source: 04 User stories/Recovery Workbench User Stories Epic 2 Story Files v4.zip!RWB E2 002 ACE plan status on the case v1.md -->
<!-- converted: 2026-11-16 from Markdown (extracted) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 2 Story Files v4.zip!RWB E2 002 ACE plan status on the case v1.md`  
> **Converted from:** Markdown (extracted)

# RWB-E2-002 ACE plan status on the case

SCB Collections and Recovery. Henka Group, 28 October 2026.

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
| Decision | D5 |
| Priority | Must |
| Depends on | RWB-E2-001 |
| Status | Ready for build |

## 1. Story

As a **case owner (RW-CASEOWN)**, I want **the restructure plan status from the ACE common module (created, approved, booked, broken) on the case**, so that **a case with a live plan is never treated as if it had none, and a broken plan returns the case to me the next morning**.

## 2. Business rationale

Restructure plans are calculated and held in ACE (DL14). Without the plan status on the case, a recovery officer can start litigation on a customer who is paying a plan, or miss a plan that broke. This story reads the status from the ACE common module each morning and on each case view, keeps the last known status with its date when ACE returns none, and raises the broken plan to the restructure rules. It meets REQ-CHO-002 and REQ-DRI-013.

## 3. Preconditions

- RWB-E2-001 (case creation from the COLLINS load) is done.
- The ACE common module publishes RestructurePlanQuery in SIT and UAT (INT-34; DL14).
- The account number is the join key between the case and the ACE plan (DL21).
- The plan event map rows are loaded: ACE status BROKEN with route state PLAN_CURE_PERIOD maps to event CURE_PERIOD_EXPIRED; BROKEN with any other route state maps to TREATMENT_BROKEN.
- Parameter `restructure.max_breaks` = 2 is in force (Restructure route set: a second break bars a further restructure).
- The restructure rules R-RES-29, R-RES-30, R-RES-31 and R-LIT-02 are in force.

## 4. Flow

1. Scheduler: the plan status step runs in JOB-02 after the case creation step, once a day.
2. SY-DATALOAD: the PlanStatusService lists every open case with its account numbers through the P3 CaseQuery.
3. SY-DATALOAD: calls RestructurePlanQuery.statusFor with the account numbers in batches of 500 (assumed; DL11).
4. SY-DATALOAD: for each plan returned, compares status and status date with the stored values; an unchanged plan is skipped.
5. SY-CASEWF: writes plan_ref, plan_status and plan_status_as_of on the case through CasePlanStatus.update.
6. SY-DATALOAD: on a change to BROKEN, looks up the event in the plan event map and calls CaseEvents.raise with plan_status = broken and the break count.
7. SY-RULES and SY-CASEWF: evaluate the rule for the case's route state, write the decision log entry, move the route state and place the case in the case owner's queue with a task.
8. Case owner: opens the case record view; the front end calls GET /cases/{caseId}/plan-status, which reads ACE live with a 2-second timeout and falls back to the stored status.
9. SY-DATALOAD: for a case with a stored plan that ACE no longer returns, keeps the stored status and date and writes a data quality exception for the ACE team.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | ACE returns no status for a plan the case holds | The case keeps its last known status and date; a data quality exception lists the plan for the ACE team | MSG-P2-008 | AC3 |
| X2 | The ACE common module is unavailable or does not answer in 2 seconds | The daily step keeps every stored status and retries in the next run; the view shows the stored status | MSG-GEN-006, MSG-P2-008 | AC4 |
| X3 | ACE returns a status code not in the plan status list | The status is not stored; a data quality exception with check "Lists of values" is written | None | AC5 |
| X4 | The daily step runs twice for the same day | No status is written twice and no event is raised twice | None | AC6 |
| X5 | The decision log write fails during the broken plan move | The route state does not move; an incident is raised; the event is raised again in the next run | MSG-P7-003 | AC7 |
| X6 | A user reads the plan status of a case outside their scope | Refused | MSG-P4-003 | AC8 |
| X7 | A role without the Case record right reads the plan status | Refused; nothing changes | MSG-P4-002 | TC-E2-002-09 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the cases from RWB-E2-001 and the ACE interface |
| Negotiable | The event map, batch size, timeout and maximum breaks are data rows or properties |
| Valuable | No action is taken on a case with a live plan without the plan in view |
| Estimable | One service, one job step, one endpoint, one map table |
| Small | Within two weeks with its tests |
| Testable | Each criterion below is one automated test |

## 7. Acceptance criteria

```gherkin
Feature: ACE plan status on the case

  Background:
    Given case "RW-2026-000310" is open with synthetic account "A-0310"
    Given the ACE common module stub holds plan "TDR-SYN-0310" for "A-0310"

  Scenario: AC1 Plan status on the case
    Given plan "TDR-SYN-0310" has status "APPROVED" in ACE with status date 2026-12-10
    When the case record view loads on 2026-12-11
    Then the case shows plan "TDR-SYN-0310" with status "Approved" and date 2026-12-10
    Then the rules component reads plan_status "APPROVED" for the case
    Then rule R-LIT-02 does not fire for the case because plan_status is not broken

  Scenario: AC2 Broken plan
    Given the case is in route state "PLAN_CURE_PERIOD" with break count 0
    Given plan "TDR-SYN-0310" has status "BROKEN" in ACE with status date 2026-12-14
    When the daily case update runs on 2026-12-15
    Then the case plan status is "BROKEN" with date 2026-12-14
    Then the route state moves to "PLAN_BROKEN" by R-RES-29 and then to "BACK_TO_ROUTE_DECISION" by R-RES-30
    Then the case is in the case owner's queue with a task due in 5 working days
    Then the system writes a decision log entry for each move with the rule ID and version

  Scenario: AC3 Status not available
    Given the case holds plan "TDR-SYN-0310" with status "BOOKED" and date 2026-12-01
    Given ACE returns no status for "TDR-SYN-0310"
    When the daily case update runs on 2026-12-15
    Then the case keeps status "BOOKED" with date 2026-12-01
    Then the case record view shows message MSG-P2-008 with the date 2026-12-01
    Then a data quality exception with product "DP04" lists plan "TDR-SYN-0310" for the ACE team

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
    Then a data quality exception with check "Lists of values" names the code "SUSPENDED"

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
| SY-DATALOAD, data load | Calls the ACE interface and writes the stored plan status through P3 |
| SY-RULES, rules component | Evaluates R-RES-29, R-RES-30, R-RES-31 and R-LIT-02 |
| SY-CASEWF, case workflow module | Moves the route state, places the case in the queue, raises the task |
| SY-DECLOG, decision log writer | Writes each entry (Decision log, C) |
| RW-CASEOWN, case owner | Reads the plan status on cases in scope (Case record, R) |
| RW-RESTRUCT, restructuring officer | Reads the plan status on cases in scope (Case record, R) |
| RW-DATASTEW, RW-PLATADM | Read the data quality exceptions for the ACE team (Platform administration, R) |

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
| DF-CAS-026 | case_account | account_id | Read |
| DF-ACC-002 | loan_account | account_no | Read |
| DF-WRK-018 | task | case_id | Write, through the P3 interface |
| DF-WRK-019 | task | task_code | Write, through the P3 interface |
| DF-WRK-024 | task | due_at | Write, through the P3 interface |
| DF-REF-002 | rule_row | rule_id | Read |
| DF-REF-003 | rule_row | rule_version | Read |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Write |

Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

**Job step: plan status in JOB-02 Case creation.** Trigger: after the case creation step of JOB-02, daily. Input: open cases and their account numbers; ACE plan statuses. Output: stored plan status per case; rule events for broken plans; data quality exceptions. Events published: CaseStateChanged (EV-05) by P3 for each route move. Idempotency key: case ID + plan reference + status + status date. Restart: a rerun skips every case whose stored status and date equal the ACE values.

**Endpoint (new, recorded in additions).**

| Method and path | Request | Response | Errors | Authorization | Idempotency |
|---|---|---|---|---|---|
| GET /cases/{caseId}/plan-status | Path: caseId | PlanStatus: planRef, status, statusDate, live (true when read from ACE now), messageCode | 401 (MSG-P4-001); 403 no Case record right (MSG-P4-002); 404 not found or out of scope (MSG-P4-003) | Case record, R | Read only; writes nothing |

**Published interfaces called.**

```java
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
| PlanEventMap | Rule table | Rows: ACE status, route state, rule event; versioned reference data |
| PlanStatusStep | Job | Step of JOB-02 |
| PlanStatusPanel | React component | Shows plan, status, date and MSG-P2-008 when not live |

- **Database:** the three new recovery_case columns plan_ref varchar(30), plan_status varchar(10), plan_status_as_of date are added by P3 in its migration for this story; no P2 table.
- **Configuration and reference data:** plan event map rows (RW-COE); new list LOV-PLAN-STATUS with CREATED, APPROVED, BOOKED, BROKEN (RW-COE); parameter restructure.max_breaks = 2; properties `rwb.ace.plan.batch-size` = 500 and `rwb.ace.plan.timeout-ms` = 2000 (assumed; DL11).
- **Build steps:**
  1. Build AcePlanClient against a stub of RestructurePlanQuery with batching and the timeout.
  2. Build PlanStatusService compare and write with the idempotency key.
  3. Build the event lookup with PlanEventMap and the CaseEvents.raise call; handle DecisionLogUnavailableException.
  4. Build the exception writes for no status and unknown codes.
  5. Build PlanStatusStep in JOB-02.
  6. Build the endpoint with live read and fallback, and PlanStatusPanel.
- **Feature flag:** `rwb.integration.ace-plan-status`.
- **Done when:** the tests in section 16 pass and the SIT run against the ACE stub moves a broken plan case to the case owner's queue.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P2-008 | Plan status shown from the stored value | The ACE plan status is from {date}. Today's status was not returned. |
| MSG-GEN-006 | ACE common module unavailable | {system} is not available. Your request is queued and will be retried. |
| MSG-P7-003 | Decision log write failed on a broken plan | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-003 | Case outside the caller's scope | This case is not in your scope. |
| MSG-P4-002 | A role without the Case record right | You cannot {action} here. Your role does not include it. |

## 15. Screens and states

SCR-03 Case record, states loading and read only: the plan status panel shows the plan reference, status, date and, when not live, MSG-P2-008. SCR-14 Treatment record, state broken, shows the broken plan once the case returns to the route decision.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-002-01 | AC1, BR1, BR2, BR6 | System | ACE stub plan TDR-SYN-0310 APPROVED |
| TC-E2-002-02 | AC2, BR4, BR5 | System | Case in PLAN_CURE_PERIOD; ACE plan BROKEN |
| TC-E2-002-03 | AC3, BR7 | System | ACE stub returns no plan |
| TC-E2-002-04 | AC4 | Resilience | ACE stub delayed 3 seconds |
| TC-E2-002-05 | AC5, BR3 | System | ACE stub returns SUSPENDED |
| TC-E2-002-06 | AC6, BR9 | System | Step run twice on 2026-12-15 |
| TC-E2-002-07 | AC7, BR8 | System | Decision log store stopped |
| TC-E2-002-08 | AC8 | System | Case owner with scope Own and a case of another owner |
| TC-E2-002-09 | Access | Access | RW-REFADM (no Case record right) calls GET /cases/{caseId}/plan-status; refused with MSG-P4-002 |
| TC-E2-002-10 | Principle 5 | Resilience | Decision log write forced to fail on the R-RES-29 move; route state unchanged |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: status codes, the event map, maximum breaks, batch size and timeout are rows or properties.
- No personal data in logs, tests or prompts; logs hold case IDs and plan references, never account numbers.
- No read of another module's tables or of ACE tables; ACE is reached only through RestructurePlanQuery.
- A read of the plan status writes nothing.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-013 | Plan status read from the ACE common module | Program 5.2; Epic 2 3.2 | FEAT-CHO-02 | 7.3 Negotiate settlement or deed in lieu | R-UNI-39, R-UNI-40 | TC-E2-002-01, TC-E2-002-04, TC-E2-002-06, TC-E2-002-07 |
| REQ-CHO-002 | Plan status change visible on the case | Program 5.3; Epic 2 3.2 | FEAT-CHO-02 | 7.3 Negotiate settlement or deed in lieu | R-RES-29, R-RES-30, R-RES-31, R-LIT-02 | TC-E2-002-02, TC-E2-002-03, TC-E2-002-05, TC-E2-002-08 |

## 19. Out of scope

- Creating or changing a plan: ACE, under DL14.
- The treatment record and plan timers: RWB-E2-004.
- Booking confirmation of the plan: RWB-E2-007.
- The full restructure route in the Workbench: Epic 3.
