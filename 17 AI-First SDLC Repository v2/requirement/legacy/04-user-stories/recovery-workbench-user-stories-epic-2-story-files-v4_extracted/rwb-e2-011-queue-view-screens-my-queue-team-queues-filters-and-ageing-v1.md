<!-- source: 04 User stories/Recovery Workbench User Stories Epic 2 Story Files v4.zip!RWB E2 011 Queue view screens my queue team queues filters and ageing v1.md -->
<!-- converted: 2026-11-16 from Markdown (extracted) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 2 Story Files v4.zip!RWB E2 011 Queue view screens my queue team queues filters and ageing v1.md`  
> **Converted from:** Markdown (extracted)

# RWB-E2-011 Queue view screens: my queue, team queues, filters and ageing

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E2-011 |
| Epic | E2, release 31 December 2026 |
| Module | P3 Case and workflow |
| Feature | FEAT-WKM-01 Show my queue with filters and ageing; FEAT-WKM-02 Show team queues |
| Requirement IDs | REQ-WKM-001, REQ-WKM-002, REQ-WKM-006 |
| BRD section | Business Requirements Epic 2, sections 3.3 and 4; Business Requirements Program, section 5.3 |
| L3 process | 06 Take over and own the case |
| Decision | None |
| Priority | Must |
| Depends on | RWB-E1-020, RWB-E1-031 |
| Status | Ready for build |

## 1. Story

As a **team manager (RW-TEAMMGR)**, I want **screens for my queue and my team's queues with filters by stage, route, status and age, sorted by service level**, so that **every person sees their work in one place and the team manager sees the team's load**.

## 2. Business rationale

Cases are run from team spreadsheets and the team manager learns of a late case from email. With about 23,600 open cases at go-live (NFR-001), a case owner needs their own list ordered by the next service level date, and the team manager needs each queue's depth, oldest case and breaches without a report request. This story gives both views on the case list and the team queues screen. It meets REQ-WKM-001, REQ-WKM-002 and REQ-WKM-006. The measure is that the team queue counts equal the case list counts for the same team every day.

## 3. Preconditions

- RWB-E1-020 is done: every case has a queue and an owner by rule.
- RWB-E1-031 is done: the case list (SCR-02) shows queue and owner with filters by queue, team and status, and the export.
- RWB-E1-028 is done: each assigned case has a SERVICE_LEVEL timer.
- Queues are loaded with their team, role and caseload cap (RWB-E1-019; cap values DL23, assumed 150).
- The signed-in person holds RW-CASEOWN (scope Own) or RW-TEAMMGR (scope Team) with the scope set by RWB-E1-037.
- The COLLINS load for the business date has passed its checks, or the case list shows its date as stale.

## 4. Flow

1. Case owner: opens My queue from the menu.
2. Front end: calls `GET /cases` with `owner=me`, `sort=serviceLevelDueAt` and the filters kept for the session.
3. Case service: applies the scope, the filters and the sort; returns one page of cases with age, status and service level state.
4. Front end: shows the list in state List, or Empty with MSG-P3-017.
5. Case owner: sets the stage filter to Litigation; the front end keeps the filter in session storage and reloads the list in state Filtered.
6. Team manager: opens Team queues from the menu.
7. Front end: calls `GET /queues`.
8. Queue service: returns each queue in the manager's teams with the open case count, the oldest entry date, the breach count and the open cases per owner against the cap.
9. Team manager: selects a queue; the front end calls `GET /queues/{queueId}/cases` and shows the cases sorted by service level.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The person has no case in scope for the filters | Empty state | MSG-P3-017 | AC4 |
| X2 | Age from is greater than age to | The request is refused; the list is not reloaded | MSG-GEN-003 | AC5 |
| X3 | Page size above 200 | The request is refused | MSG-GEN-002 | AC6 |
| X4 | A team manager opens a queue of another team | Not found | MSG-P4-003 | AC7 |
| X5 | Today's COLLINS load has not arrived | The list shows with the stale banner and the date of the data | MSG-P1-001 | AC8 |
| X6 | A case's service level timer is paused by a deviation | The case shows "Paused" and sorts after running timers | MSG-P3-004 | AC9 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Reads the case, queue and timer rows that Epic 1 already writes |
| Negotiable | Columns and filter order can change; the sort and the counts are fixed |
| Valuable | Each person works one ordered list; the team manager sees load and breaches |
| Estimable | Two endpoints extended, one endpoint used, two screens |
| Small | Fits in one sprint with its tests |
| Testable | API tests on a seeded database and browser tests on both screens |

## 7. Acceptance criteria

```gherkin
Feature: Queue view screens: my queue, team queues, filters and ageing

  Background:
    Given the business date is 2026-12-15
    Given team "MTG-BKK" has queues "MTG-BKK-CO" and "MTG-BKK-LIT" with a caseload cap of 150
    Given user "U-CO-01" holds RW-CASEOWN in team "MTG-BKK" and user "U-TM-01" holds RW-TEAMMGR for team "MTG-BKK"

  Scenario: AC1 My queue
    Given "U-CO-01" owns 40 open cases, 3 with an expired service level timer and 37 with running timers
    When "U-CO-01" opens My queue
    Then 40 cases list in one page
    Then the 3 breached cases come first, then the 37 by service level due date, earliest first
    Then each row shows the case number, product group, stage, status, age in days from the entry date and the service level due date

  Scenario: AC2 Team view
    Given "MTG-BKK-CO" holds 412 open cases with the oldest entered on 2026-09-02 and 9 breaches
    Given "MTG-BKK-LIT" holds 38 open cases with the oldest entered on 2026-10-20 and 0 breaches
    When "U-TM-01" opens Team queues
    Then "MTG-BKK-CO" shows count 412, oldest case age 104 days and 9 breaches
    Then "MTG-BKK-LIT" shows count 38, oldest case age 56 days and 0 breaches
    Then each owner in "MTG-BKK-CO" shows their open case count against the cap of 150

  Scenario: AC3 Filter
    Given "U-CO-01" owns 12 open cases on stage "LITIGATION" and 28 on other stages
    When the stage filter is set to "LITIGATION" and the list refreshes
    Then only the 12 litigation cases show
    Then after "U-CO-01" opens a case and returns to My queue the filter is still "LITIGATION"
    Then after sign-out and sign-in the filter is cleared

  Scenario: AC4 Empty queue
    Given "U-CO-02" owns no open case
    When "U-CO-02" opens My queue
    Then the screen shows the empty state with MSG-P3-017

  Scenario: AC5 Age range in the wrong order
    When "U-CO-01" sets age from 120 and age to 90
    Then the system refuses the request with MSG-GEN-003 naming "age to" and "age from"
    Then the list keeps its previous rows

  Scenario: AC6 Page size above the limit
    When the front end requests My queue with page size 500
    Then the system refuses the request with MSG-GEN-002 naming "size", 1 and 200

  Scenario: AC7 Queue of another team
    Given queue "SME-NTH-CO" belongs to team "SME-NTH"
    When "U-TM-01" requests the cases of "SME-NTH-CO"
    Then the system does not find the response with MSG-P4-003

  Scenario: AC8 Stale data
    Given the COLLINS load of 2026-12-15 has not arrived and the case data is from 2026-12-14
    When "U-CO-01" opens My queue
    Then the 40 cases show with the stale banner MSG-P1-001 naming the date 2026-12-14

  Scenario: AC9 Paused service level
    Given 2 of the 40 cases have a deviation "X1" open and their service level timers paused
    When "U-CO-01" opens My queue
    Then the 2 cases show "Paused" with MSG-P3-004 on hover and sort after the 37 running timers

  Scenario: AC10 Age boundary
    Given case "RW-2026-000301" entered on 2026-09-16 and case "RW-2026-000302" entered on 2026-09-17
    When "U-CO-01" sets age from 90 and age to 90
    Then only "RW-2026-000301" shows, with age 90 days

  Scenario: AC11 Counts reconcile to the case list
    When "U-TM-01" reads the count of "MTG-BKK-CO" on Team queues and the case list filtered by queue "MTG-BKK-CO" and status not "CLOSED"
    Then both show 412

  Scenario: AC12 Load time
    Given "U-CO-01" owns 500 open cases
    When "U-CO-01" opens My queue with page size 200
    Then the first page shows within 2 seconds at the 95th percentile over 20 runs
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | My queue shows the open cases whose owner is the signed-in person; Team queues shows only the queues of the manager's teams | roles.txt default scope (Own, Team); CTL-09 |
| BR2 | Sort order: breached service level first, then running by due date earliest first, then paused, then no service level timer | REQ-WKM-001; R-UNI-30 |
| BR3 | Age is the number of calendar days from the case entry date to the business date | DF-CAS-013; labels.txt Stage clock |
| BR4 | A breach is an open case whose SERVICE_LEVEL timer has status EXPIRED | R-UNI-30; REQ-CWC-011 |
| BR5 | The open case count of a queue is its cases with status not Closed, and equals the case list count for the same queue | REQ-WKM-006; NFR-018 |
| BR6 | An owner at or above the queue's caseload cap is shown at cap | Queue field capacity_cap; DL23 |
| BR7 | A timer paused by a deviation shows as paused; the prescription date keeps running | R-DEV-01; R-UNI-43 |
| BR8 | Filters are kept for the browser session only and are not stored on the server | Principle 1 (no business value stored per user) |

## 9. State transitions

None. This story does not change a case status. It reads cases, queues and timers only.

## 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-CASEOWN, case owner | Opens My queue (Case record R, scope Own); reads queue rows of own queue (Queue and allocation R) |
| RW-TEAMMGR, team manager | Opens Team queues and My queue (Queue and allocation R, Case record R, scope Team) |
| RW-CAPACITY, capacity and workforce planner | Opens Team queues (Queue and allocation R, scope All) |
| RW-RESTRUCT, RW-LITOFF | Open My queue for the cases they own (Case record R) |
| RW-AUDIT, internal audit | Reads both views (R, scope All); changes nothing |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | recovery_case | id | Read |
| DF-CAS-002 | recovery_case | case_no | Read |
| DF-CAS-003 | recovery_case | product_group | Read |
| DF-CAS-005 | recovery_case | status | Read |
| DF-CAS-006 | recovery_case | stage_code | Read |
| DF-CAS-008 | recovery_case | route_code | Read |
| DF-CAS-009 | recovery_case | owner_user_id | Read |
| DF-CAS-010 | recovery_case | queue_id | Read |
| DF-CAS-011 | recovery_case | team_code | Read |
| DF-CAS-013 | recovery_case | entry_date | Read |
| DF-CAS-019 | recovery_case | deviation_open | Read |
| DF-WRK-001 | queue | id | Read |
| DF-WRK-002 | queue | queue_code | Read |
| DF-WRK-003 | queue | queue_name | Read |
| DF-WRK-004 | queue | team_code | Read |
| DF-WRK-007 | queue | capacity_cap | Read |
| DF-WRK-028 | timer | case_id | Read |
| DF-WRK-030 | timer | timer_type | Read |
| DF-WRK-032 | timer | expires_at | Read |
| DF-WRK-034 | timer | paused | Read |
| DF-WRK-035 | timer | status | Read |

Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

**GET /cases** (P3)

| Item | Value |
|---|---|
| Request | Query: `owner` (`me` or a user ID), `stage`, `route` (new), `status`, `ageFrom`, `ageTo`, `queue`, `page` (default 0), `size` (default 50, 1 to 200), `sort` (`serviceLevelDueAt` new; default for My queue) |
| Response | 200 `CasePage`: `items[]` of `Case` with the new computed fields `ageDays`, `serviceLevelDueAt`, `serviceLevelState` (BREACHED, RUNNING, PAUSED, NONE); `page`, `size`, `total`; header `X-Data-As-Of` with the business date of the case data |
| Errors | 401 (MSG-P4-001); 403 no Case record R (MSG-P4-002); 422 age range in the wrong order (MSG-GEN-003) or size outside 1 to 200 (MSG-GEN-002); 503 |
| Authorization | Case record, right R, scope applied |
| Idempotency | Not applicable |

**GET /queues** (P3)

| Item | Value |
|---|---|
| Request | None |
| Response | 200 `Queue[]` with the new computed fields `openCaseCount`, `oldestEntryDate`, `oldestAgeDays`, `breachCount`, `owners[]` (`ownerUserId`, `openCaseCount`, `atCap`) |
| Errors | 401; 403 no Queue and allocation R (MSG-P4-002); 503 |
| Authorization | Queue and allocation, right R, scope applied (queues of the caller's teams) |
| Idempotency | Not applicable |

**GET /api/recovery/v1/queues/{queueId}/cases** (P3)

| Item | Value |
|---|---|
| Request | Path `queueId`; query `page`, `size` (1 to 200), `sort` (`serviceLevelDueAt`) |
| Response | 200 `CasePage` as above |
| Errors | 401; 403 (MSG-P4-002); 404 queue unknown or outside scope (MSG-P4-003); 422 size (MSG-GEN-002); 503 |
| Authorization | Queue and allocation, right R, scope applied |
| Idempotency | Not applicable |

## 13. Solution plan

**Package.** `recovery.casewf.queueview` in the recovery module; front end folder `src/modules/recovery/casewf/queues`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| CaseListQueryService | Service | Builds the scoped case query with filters, age and the service level sort; computes `ageDays` and `serviceLevelState` |
| QueueSummaryService | Service | Counts open cases, oldest entry date, breaches and open cases per owner for each queue in scope |
| CaseListRepository | Repository | One SQL query joining `recovery_case` with the SERVICE_LEVEL `timer` of each case |
| QueueSummaryRepository | Repository | Grouped counts by `queue_id` and `owner_user_id` |
| CaseAndWorkflowController | Controller | The three endpoints; parameter checks; problem responses |
| MyQueuePage | React component | SCR-02 in the My queue view with filters, sort and states |
| TeamQueuesPage | React component | SCR-07 with the queue rows, owner spread and drill down |
| useSessionFilters | React component | Hook that keeps filters in session storage, wrapped in try and catch, cleared at sign-out |

**Database.** Reads `recovery_case`, `queue` and `timer`. Uses `ix_case_owner_status`, `ix_case_status_queue` and `ix_timer_case_id`. Adds index `ix_timer_case_type_status` on `timer (case_id, timer_type, status)` in migration `V<next>__rwb_e2_011_queue_view_index.sql`.

**Configuration and reference data.** Page size limits (`queueview.page-size.default` 50, `queueview.page-size.max` 200) in the configuration service, loaded by the platform administrator. Stage, route and status labels from LOV-STAGE, LOV-ROUTE and LOV-CASE-STATUS through the P4 list interface. Caseload caps from the queue table (DL23).

**Build steps**

1. Add the index migration and `CaseListRepository` with the service level join; test the four sort groups.
2. Build `CaseListQueryService` with scope, filters, age and the new computed fields; add `route` and the sort to `GET /cases`.
3. Build `QueueSummaryService` and the computed fields on `GET /queues`; test the counts against `GET /cases` for the same queue.
4. Add the scope check to `GET /queues/{queueId}/cases`.
5. Build `MyQueuePage` with Loading, Empty, List and Filtered states and `useSessionFilters`.
6. Build `TeamQueuesPage` with Loading and List states and the drill down.
7. Add the stale banner from `X-Data-As-Of` and the paused marker.
8. Write the API, browser and load tests in section 16.

**Feature flag.** `rwb.p3.queue-views`. Off: the menu items My queue and Team queues are hidden and the endpoints return the Epic 1 fields only.

**Done when.** The tests in section 16 pass, and the browser accessibility check (RWB-TE-010) passes on both screens.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-017 | The list has no case for the person and filters | There are no cases in this queue. |
| MSG-GEN-003 | Age to is less than age from | {field} cannot be before {other}. |
| MSG-GEN-002 | Page size outside 1 to 200 | {field} must be between {min} and {max}. |
| MSG-P4-003 | A queue outside the caller's scope | This case is not in your scope. |
| MSG-P1-001 | The case data is from an earlier business date | {product} is from {date}. Today's load has not arrived. |
| MSG-P3-004 | A case on hold for a deviation | This case is on hold for {deviation}. The prescription date is still {date}. |
| MSG-P4-002 | A role without the right opens a view | You cannot {action} here. Your role does not include it. |

MSG-P3-017 is new (see Additions). Thai text follows DL10.

## 15. Screens and states

| Screen | State | What the user does |
|---|---|---|
| SCR-02 Case list, My queue view | Loading | Sees skeleton rows |
| SCR-02 Case list, My queue view | Empty | Reads MSG-P3-017 |
| SCR-02 Case list, My queue view | List | Reads cases sorted by service level; opens a case on SCR-03 |
| SCR-02 Case list, My queue view | Filtered | Sets stage, route, status and age filters; clears them |
| SCR-07 Team queues | Loading | Sees skeleton rows |
| SCR-07 Team queues | List | Reads count, oldest age, breaches and owners against the cap; opens a queue's cases; goes to SCR-05 Transfer case (RWB-E2-012) |

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-011-01 | AC1, BR1, BR2, BR3 | System | 40 cases for U-CO-01: 3 breached, 37 running |
| TC-E2-011-02 | AC2, BR4, BR6 | System | Queues MTG-BKK-CO (412 cases) and MTG-BKK-LIT (38 cases) |
| TC-E2-011-03 | AC3, BR8 | System | 12 litigation and 28 other cases; browser session kept and ended |
| TC-E2-011-04 | AC4 | System | U-CO-02 with no case |
| TC-E2-011-05 | AC5 | System | Age from 120, age to 90 |
| TC-E2-011-06 | AC6 | System | Page size 500 |
| TC-E2-011-07 | AC7, BR1 | System | Queue SME-NTH-CO requested by a MTG-BKK manager |
| TC-E2-011-08 | AC8 | System | Data as of 2026-12-14 on business date 2026-12-15 |
| TC-E2-011-09 | AC9, BR7 | System | Two cases with X1 open and paused timers |
| TC-E2-011-10 | AC10, BR3 | System | Entry dates 2026-09-16 and 2026-09-17 |
| TC-E2-011-11 | AC11, BR5 | System | Queue count against the case list count |
| TC-E2-011-12 | AC12 | System | 500 cases, 20 timed runs |
| TC-E2-011-13 | Access | Access | RW-WRITEOFF (no Queue and allocation right) calls `GET /queues`; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code. Caps, page sizes, labels and list values are read from the queue table, the configuration service and the lists.
- No personal data in logs, tests or prompts. Rows show case numbers and codes; party names follow the masking rules of RWB-E1-037. Test data is synthetic.
- No read of another module's tables. List labels come through the P4 interface; deviation details come through the S8 interface.
- Browser storage holds only the filter values and is wrapped in try and catch; the page works without it.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-WKM-001 | A case owner sees their own queue with ageing and service level state | Business Requirements Epic 2, section 3.3; Program, section 5.3 | FEAT-WKM-01 | 06 Take over and own the case | R-UNI-30 | TC-E2-011-01, TC-E2-011-03 to TC-E2-011-06, TC-E2-011-08 to TC-E2-011-10, TC-E2-011-12 |
| REQ-WKM-002 | A team manager sees every queue in the team with filters | Business Requirements Epic 2, section 3.3; Program, section 5.3 | FEAT-WKM-02 | 06 Take over and own the case | R-UNI-30 | TC-E2-011-02, TC-E2-011-07, TC-E2-011-13 |
| REQ-WKM-006 | Queue counts, ageing and breaches reconcile to the case list | Business Requirements Epic 2, section 4; Program, section 5.3 | FEAT-WKM-02 | 06 Take over and own the case | R-UNI-30 | TC-E2-011-02, TC-E2-011-11 |

## 19. Out of scope

- The export of the case list (RWB-E1-031).
- Transfer and reassignment from the team queues screen (RWB-E2-012).
- Partner work in the same queue view (REQ-WKM-011, partner placements in Epic 6).
- The daily queue measures in Power BI (RWB-E1-030).
- The next action column (RWB-E2-035).
