<!-- source: 04 User stories/Recovery Workbench User Stories Epic 1 Story Files v5.zip!RWB E1 030 Daily rebalancing and queue measures v1.md -->
<!-- converted: 2026-11-04 from Markdown (extracted) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 1 Story Files v5.zip!RWB E1 030 Daily rebalancing and queue measures v1.md`  
> **Converted from:** Markdown (extracted)

# RWB-E1-030 Daily rebalancing and queue measures

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E1-030 |
| Epic | E1, release 30 November 2026 |
| Module | P3 Case and workflow |
| Feature | FEAT-CWC-17 Rebalance queues daily; FEAT-CWC-18 Publish queue measures; FEAT-WKM-11 Reallocate when the caseload cap is breached; FEAT-RPT-02 Publish queue and ageing measures |
| Requirement IDs | REQ-CWC-015, REQ-RDF-012 |
| BRD section | Business Requirements Epic 1, section 3.3; Business Requirements Program, sections 5.1 and 5.3 |
| L3 process | All recovery processes; 15 Manage performance, data and AI |
| Decision | None |
| Priority | Must |
| Depends on | RWB-E1-020, RWB-E1-027, RWB-E1-028 |
| Status | Ready for build |

## 1. Story

As a **team manager (RW-TEAMMGR)**, I want **a daily job that assigns unassigned cases and moves the newest cases off owners above the cap by the assignment rules, and queue counts, ageing and service level breaches published to Power BI**, so that **queues stay balanced and every team manager sees the same numbers as the case list**.

## 2. Business rationale

Team managers rebalance work by hand today and count queues from spreadsheets that do not match. This story moves cases left in overflow or without an owner each morning, takes owners above the cap back inside it (R-UNI-19), and publishes depth, ageing, owner spread and breaches as one snapshot that reconciles to the case list. It meets REQ-CWC-015 and REQ-RDF-012.

## 3. Preconditions

- RWB-E1-020 is done: AssignmentEngine and CapacityService answer for the queue version in force.
- RWB-E1-028 is done: timers are EXPIRED on a service level breach.
- RWB-E1-027 is done: the decision log writer is available.
- Caseload caps are loaded (DL23). If DL23 is late, rebalancing reports and moves nothing.
- JOB-03 has completed for the business date; JOB-06 runs as SY-CASEWF.
- JOB-15 Reporting extract copies the snapshot to the data lake for Power BI nightly (owner RW-BIANAL).

## 4. Flow

1. Quartz: starts JOB-06 at 06:30, or when JOB-03 completes for the business date if that is later.
2. RebalanceJob: lists cases in each queue with no owner and status NEW or ASSIGNED, and owners whose open cases exceed their capacity.
3. RebalanceService: for each owner above the cap, selects the newest cases by assignment time until the owner is inside the cap (R-UNI-19).
4. RebalanceService: skips cases with deviation_open or legal_hold true.
5. AssignmentEngine: picks an owner below the cap in the same queue for each selected or unassigned case.
6. RebalanceService: writes the decision log entry, ends the old assignment, writes the new one with reason REBALANCE and publishes CaseTransferred, case by case.
7. QueueMeasureService: at the end of the run, takes one snapshot per queue at one time: depth, unassigned, age in days from the entry date, owner spread and SERVICE_LEVEL timers EXPIRED.
8. QueueMeasureService: checks each queue depth against the case count for the same queue and time, and publishes the snapshot only when every queue matches.
9. JOB-15: copies the snapshot to the data lake; Power BI shows it from the next morning.
10. TimerBreachNotifier: on TimerBreached from JOB-05, sends the team manager MSG-P3-028 with the queue's breach count.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | No member of the queue has capacity | Cases stay where they are; counted in the summary | MSG-P3-011 | AC4 |
| X2 | No caseload cap is loaded for the queue | The queue is reported and nothing is moved | None | AC5 |
| X3 | Decision log write fails for a case | That case is not moved; the run continues | MSG-P7-003 | AC6 |
| X4 | JOB-06 runs again the same day | Already balanced queues give no further moves | None | AC7 |
| X5 | A case has an open deviation or a legal hold | Not moved | None | AC8 |
| X6 | The snapshot depth differs from the case count | Snapshot not published; break listed for the data steward | MSG-P3-029 | AC9 |
| X7 | An owner holds exactly the cap | No case is moved off them | None | AC10 |
| X8 | A role without Platform administration U reruns JOB-06 | Refused with 403 | MSG-P4-002 | Access test TC-E1-030-11 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Reuses the assignment engine (RWB-E1-020) and the timers (RWB-E1-028) |
| Negotiable | Caps and the ordering of moves are data (DL23) |
| Valuable | Removes daily hand rebalancing and gives one set of queue numbers |
| Estimable | One job, one measure snapshot, one notifier |
| Small | Fits two weeks with its tests |
| Testable | Every criterion has a test case in section 16 |

## 7. Acceptance criteria

```gherkin
Feature: Daily rebalancing and queue measures

  Background:
    Given queue "TDR-BKK-CO" uses "LOWEST_LOAD" with cap 150
    Given the business date is 2026-12-02

  Scenario: AC1 Rebalance
    Given queue "TDR-BKK-CO" has 12 cases with no owner
    Given members U-61 and U-62 hold 140 and 144 open cases
    When JOB-06 runs
    Then the system assigns the 12 cases , 8 to U-61 and 4 to U-62, by lowest load with ties going to the member first in the queue list
    Then each assignment has reason "REBALANCE" and a decision log entry

  Scenario: AC2 Measures reconcile
    Given the snapshot taken at 2026-12-02 06:52
    When the queue report refreshes
    Then the depth of each queue equals the case list count for that queue at 06:52
    Then queue "TDR-BKK-CO" shows depth 296, unassigned 0 and an average age of 41 days

  Scenario: AC3 Breach alert
    Given case RW-2026-000501 in queue "TDR-BKK-CO" passes its service level
    When the timer check raises the breach
    Then the team manager of "TDR-BKK" receives MSG-P3-028 with count 1 and queue "TDR-BKK-CO"
    Then the next snapshot shows 1 breach for "TDR-BKK-CO" in Power BI

  Scenario: AC4 No member has capacity
    Given every member of "TDR-BKK-CO" holds 150 open cases and 5 cases have no owner
    When JOB-06 runs
    Then the 5 cases keep no owner
    Then the team manager receives MSG-P3-011 with count 5

  Scenario: AC5 No cap loaded
    Given queue "WO-BKK-CO" has no capacity cap
    When JOB-06 runs
    Then the system moves no case in "WO-BKK-CO"
    Then the snapshot still reports "WO-BKK-CO"

  Scenario: AC6 Decision log unavailable for one case
    Given owner U-63 holds 153 open cases and the decision log write fails for the second of the 3 newest cases
    When JOB-06 runs
    Then the system moves 2 cases off U-63 and 1 stays
    Then the job record lists the case that stayed with MSG-P7-003

  Scenario: AC7 A repeated run
    Given JOB-06 has balanced "TDR-BKK-CO" on 2026-12-02
    When JOB-06 runs again on 2026-12-02
    Then the system moves no case
    Then the system writes no decision log entry

  Scenario: AC8 Held cases are not moved
    Given owner U-64 holds 152 open cases and the 2 newest have deviation_open = true
    When JOB-06 runs
    Then those 2 cases stay with U-64 and the next 2 newest are moved

  Scenario: AC9 A count difference holds the snapshot
    Given the snapshot depth for "DIL-BKK-CO" is 88 and the case count at the same time is 87
    When the snapshot is checked
    Then the system does not publish it
    Then the data steward receives MSG-P3-029 with check "queue depth against case list"

  Scenario: AC10 Owner exactly at the cap
    Given owner U-65 holds 150 open cases
    When JOB-06 runs
    Then the system moves no case off U-65
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Cases with no owner are assigned by the queue's method within the cap | queue.assignment_method, queue.capacity_cap; FEAT-CWC-17 |
| BR2 | An owner above the cap loses the newest cases until inside the cap | R-UNI-19 |
| BR3 | Cases with an open deviation or a legal hold are not moved | R-UNI-20; R-DEV-01 |
| BR4 | A queue with no cap is reported and not rebalanced | DL23 |
| BR5 | A move keeps the case status and the clocks | R-UNI-18 |
| BR6 | Measures publish only when queue depths reconcile to the case list with zero difference | DL25; REC-01 |
| BR7 | Every move is logged before it takes effect | Principle 5; R-UNI-39 |
| BR8 | A breach raises an alert to the escalation role; the case does not move | R-UNI-30 |

## 9. State transitions

None. This story does not change a case status. It changes the owner and the assignment of a case (reason REBALANCE), and the status of a measure snapshot (TAKEN, PUBLISHED, HELD).

## 10. Authority

| Who | What they may do in this story |
|---|---|
| SY-CASEWF | Moves cases and takes the snapshot |
| SY-DECLOG | Writes the entries |
| RW-TEAMMGR | Receives the summaries and alerts; reads queues in team scope |
| RW-BIANAL | Builds the Power BI report on the snapshot (Reporting CRUD) |
| RW-DATASTEW | Receives the reconciliation break |
| RW-PLATADM | Reruns JOB-06 (Platform administration U) |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | recovery_case | id | Read |
| DF-CAS-005 | recovery_case | status | Read |
| DF-CAS-009 | recovery_case | owner_user_id | Write |
| DF-CAS-010 | recovery_case | queue_id | Read |
| DF-CAS-013 | recovery_case | entry_date | Read |
| DF-CAS-019 | recovery_case | deviation_open | Read |
| DF-CAS-020 | recovery_case | legal_hold | Read |
| DF-WRK-001 | queue | id | Read |
| DF-WRK-002 | queue | queue_code | Read |
| DF-WRK-004 | queue | team_code | Read |
| DF-WRK-006 | queue | assignment_method | Read |
| DF-WRK-007 | queue | capacity_cap | Read |
| DF-WRK-048 | queue_member | capacity | Read |
| DF-WRK-009 to DF-WRK-016 | assignment | all fields | Write |
| DF-WRK-028 | timer | case_id | Read |
| DF-WRK-030 | timer | timer_type | Read |
| DF-WRK-035 | timer | status | Read |
| DF-RPT-020 to DF-RPT-030 | queue_measure | all fields | Write |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Write |

Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

**Job**

| Item | Value |
|---|---|
| Trigger | Quartz at 06:30, after JOB-03 completes for the business date |
| Job name | JOB-06 Daily rebalancing |
| Schedule | Daily 06:30 |
| Input | Queues in force, members and capacity, open cases per owner, cases with no owner, EXPIRED service level timers |
| Output | Assignments with reason REBALANCE, decision log entries, one queue_measure snapshot per queue |
| Events published | CaseTransferred (EV-04) per move |
| Idempotency key | caseId and businessDate for a move; queueId and snapshot time for a snapshot |
| Restart | Rerun from the job monitor; balanced queues give no moves; managers rebalance by hand if the rerun fails (batch.txt) |

**GET /api/recovery/v1/cases** (used for the reconciliation test)

| Item | Value |
|---|---|
| Request | Query queue (uuid), status, page, size |
| Response | CasePage: items, page, size, total |
| Errors | 401; 403 no Case record R (MSG-P4-002); 503 |
| Authorization | Case record, right R, scope applied |

**POST /api/recovery/v1/admin/jobs/{jobId}/rerun** (P1) for JOB-06: Platform administration U; 409 when the job is running.

**Published interface**

```java
// P3, package recovery.casewf.rebalance (published), read by P9 for Power BI
public interface QueueMeasureService {
    List<QueueMeasureView> latestPublished(LocalDate businessDate);
}
public record QueueMeasureView(String queueCode, String teamCode, OffsetDateTime asOf,
        int depth, int unassigned, BigDecimal avgAgeDays, int maxAgeDays,
        int ownerMin, int ownerMax, int breached) {}
```

## 13. Solution plan

**Package.** `recovery/casewf/rebalance`, Java package `recovery.casewf.rebalance`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| RebalanceJob | Job | JOB-06; selects cases and owners, calls RebalanceService, writes counts |
| RebalanceService | Service | R-UNI-19 selection, hold checks, owner choice, decision log, assignment swap |
| QueueMeasureService | Published interface | Takes, reconciles and publishes the snapshot |
| TimerBreachNotifier | Listener | Sends MSG-P3-028 to the team manager on TimerBreached |
| CaseAndWorkflowRepository | Repository | recovery_case, assignment, queue, queue_member, timer, queue_measure |

**Database**

- Writes assignment, recovery_case.owner_user_id, queue_measure, outbox.
- Snapshot query in one REPEATABLE READ transaction so depth and the case count are read at the same time.
- Migration in this story: `V030_1__queue_measure.sql` creates queue_measure (id, queue_id, as_of, depth, unassigned, avg_age_days, max_age_days, owner_min, owner_max, breached, status, standard columns; unique (queue_id, as_of)).

**Configuration and reference data**

- Caps and member capacity from RWB-E1-019 (DL23).
- Measure definitions agreed with the Tribe (REQ-RDF-012), owned by RW-COE.

**Build steps**

1. Owner over cap selection by newest assignment; unit tests AC8, AC10.
2. RebalanceService with AssignmentEngine and hold checks; tests AC1, AC4, AC5.
3. One transaction per case with the decision log write as its last step; continue on failure; test AC6.
4. Idempotent rerun; test AC7.
5. QueueMeasureService snapshot and reconciliation; tests AC2, AC9.
6. TimerBreachNotifier; test AC3.
7. P9 hand-off through QueueMeasureService for JOB-15.

**Feature flag.** `rwb.p3.rebalance`. Off: JOB-06 does not move cases; the snapshot still runs.

**Done when.** The tests in section 16 pass and the Power BI queue page shows the 2026-12-02 snapshot on 2026-12-03 in SIT.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-011 | Cases left without an owner | {count} new cases are waiting in the overflow queue for {team}. Every owner is at the caseload cap. |
| MSG-P3-028 | Service level breach alert | {count} cases in {queue} are past their service level. |
| MSG-P3-029 | Snapshot does not reconcile | The queue measures for {date} were not published: {check}. |
| MSG-P7-003 | Decision log write failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |

## 15. Screens and states

No new screen. SCR-02 Case list (filtered) shows the new owner; SCR-09 Exception queue (list) shows cases left without an owner. The team view SCR-07 comes in Epic 2; queue measures appear on the Power BI queue page built by RW-BIANAL.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-030-01 | AC1, BR1, BR7 | System | 12 unassigned cases, owners at 140 and 144 |
| TC-E1-030-02 | AC2, BR6 | System | Snapshot at 06:52 |
| TC-E1-030-03 | AC3, BR8 | System | One breach in TDR-BKK-CO |
| TC-E1-030-04 | AC4 | System | Every member at 150, 5 unassigned |
| TC-E1-030-05 | AC5, BR4 | System | Queue WO-BKK-CO with no cap |
| TC-E1-030-06 | AC6, BR7 | System | Owner at 153, log fails for one case |
| TC-E1-030-07 | AC7 | System | JOB-06 twice on 2026-12-02 |
| TC-E1-030-08 | AC8, BR3 | System | Owner at 152 with 2 held cases |
| TC-E1-030-09 | AC9, BR6 | System | Depth 88 against count 87 |
| TC-E1-030-10 | AC10, BR2 | System | Owner at exactly 150 |
| TC-E1-030-11 | Access | Access | RW-CASEOWN reruns JOB-06 and is refused with MSG-P4-002 |
| TC-E1-030-12 | Principle 5 | Resilience | Decision log write forced to fail for every move in the run |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: caps, methods and measure definitions are data.
- No personal data in the snapshot, the alerts, the logs or the tests; the snapshot holds counts only.
- No read of another module's tables: P9 reads the snapshot through QueueMeasureService.
- A move never resets the stage clock or the prescription date.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CWC-015 | Daily rebalancing; queue counts, ageing and breaches reported | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-17, FEAT-CWC-18, FEAT-WKM-11 | All recovery processes | R-UNI-19, R-UNI-30 | TC-E1-030-01, TC-E1-030-03 to TC-E1-030-10, TC-E1-030-12 |
| REQ-RDF-012 | Baseline measures for cases by queue and age published | Epic 1, 3.3; Program, 5.1 | FEAT-RPT-02 | 15 Manage performance, data and AI | None | TC-E1-030-02, TC-E1-030-09 |

## 19. Out of scope

- Reallocation when an owner leaves or is absent (R-UNI-18, Epic 2).
- The team queues screen (SCR-07, Epic 2) and the steering dashboard (Epic 2).
- The Power BI report layout (P9, RW-BIANAL).
