<!-- source: 04 User stories/Recovery Workbench User Stories Epic 2 Story Files v4.zip!RWB E2 033 Case and queue list with status owner and ageing v1.md -->
<!-- converted: 2026-11-04 from Markdown (extracted) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 2 Story Files v4.zip!RWB E2 033 Case and queue list with status owner and ageing v1.md`  
> **Converted from:** Markdown (extracted)

# RWB-E2-033 Case and queue list with status, owner and ageing

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E2-033 |
| Epic | E2, release 31 December 2026 |
| Module | P2 Integration |
| Feature | None |
| Requirement IDs | REQ-WKM-002, REQ-DVH-006 |
| BRD section | Business Requirements Epic 2, section 3.2 |
| L3 process | All recovery processes |
| Decision | D6 entry |
| Priority | Must |
| Depends on | RWB-E1-018, RWB-E1-031, RWB-E2-011 |
| Status | Ready for build |

## 1. Story

As a **team manager (RW-TEAMMGR)**, I want **every case in every queue in my scope on the case list with its identifier, product, queue, owner, status, age in state, stage and prescription clock states and service level breach flag, with a breach filter and an extract**, so that **I can see where work is waiting without asking anyone**.

## 2. Business rationale

Today a team manager learns where cases wait by asking each owner or by building a spreadsheet. RWB-E1-031 puts the queue and owner on the case list with an export, and RWB-E2-011 adds the age and the service level state for the queue screens. This story completes the case list for every queue in the manager's scope: a breach filter, the prescription clock beside the stage clock so a paused case is not read as safe, and the same columns in the extract. It meets REQ-WKM-002 (every queue in the team, filtered by status, product and ageing, with an export) and REQ-DVH-006 (the deviation flag is visible in every queue view). The business measure is the count of cases past their service level per queue, which the manager can read every morning.

## 3. Preconditions

- RWB-E1-018 (case record), RWB-E1-031 (queue and owner on the case list, GET /cases/export) and RWB-E2-011 (ageDays, serviceLevelDueAt and serviceLevelState on GET /cases) are done. RWB-E1-028 writes the SERVICE_LEVEL and PRESCRIPTION timer rows.
- The queues table (RWB-E1-019) and the service levels and timers reference table (DL22) are loaded.
- Parameter caselist.export.maxrows = 10,000 (assumed; DL11) from RWB-E1-042.
- The role to permission matrix (RWB-E1-037) gives RW-TEAMMGR the Case record right R with Team scope.
- The caller is signed in through Entra ID and holds a role with Case record R.
- Feature flag `rwb.casewf.case-list-ageing` is on.

## 4. Flow

1. Team manager: opens the case list (SCR-02).
2. Front end: calls GET /api/recovery/v1/cases with the filters chosen, including breached when set.
3. CaseAndWorkflowController: checks Case record R through the common module access check and applies the caller's scope (CTL-09).
4. CaseAndWorkflowController: validates each filter value against its list of values and the page size against 1 to 200.
5. CaseListQueryService (RWB-E2-011): reads the cases in scope with their queue, owner and SERVICE_LEVEL timer, and computes ageDays and serviceLevelState.
6. PrescriptionClockReader (this story): adds prescriptionClockStatus from the PRESCRIPTION timer and applies the breached filter (BR3, BR4).
7. CaseListQueryService: orders the rows by breach, then age in state descending, then case number, and returns one page.
8. Front end: shows the columns in section 15 and marks each breached case.
9. Team manager: chooses Extract; the front end calls GET /api/recovery/v1/cases/export with the same filters.
10. CaseExportService (RWB-E1-031): writes the matching rows with the ageing and clock columns to an Excel file, after the export is written to the access log.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A filter value is not in its list of values, for example product CAR | Request refused with 422; nothing is read | MSG-GEN-007 | AC6 |
| X2 | Page size below 1 or above 200 | Request refused with 422 | MSG-GEN-002 | AC7 |
| X3 | No case matches the filters | Empty state; the extract holds the header row only | MSG-P3-020 | AC8 |
| X4 | A queue filter names a queue outside the caller's scope | Only cases in scope are returned, so the result is empty | MSG-P3-020 | AC9 |
| X5 | A case has no SERVICE_LEVEL timer yet (status New) | serviceLevelState NONE; breached false | None | AC5 |
| X6 | The service level due time equals the current time | Not breached; breached from the next minute | None | AC4 |
| X7 | The extract would hold more than 10,000 rows | Extract refused | MSG-P3-021 | AC10 |
| X8 | A case changes between two page requests | Order is stable by case number | None | AC11 |
| X9 | The caller's role does not hold Case record R | Refused with 403; nothing is read | MSG-P4-002 | Access test TC-E2-033-12 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds on the case list and export of RWB-E1-031 and the ageing of RWB-E2-011; no new endpoint |
| Negotiable | Columns and filters are listed; their values are data. The layout belongs to the designer (DL31) |
| Valuable | Replaces the manager's daily round of questions and spreadsheets with one list |
| Estimable | One filter, one computed field, extract columns, one list change |
| Small | No write to any business table |
| Testable | Each criterion below has one test case with fixed synthetic data |

## 7. Acceptance criteria

```gherkin
Feature: Case and queue list with status, owner and ageing

  Background:
    Given today is 10 December 2026 at 09:00 Asia/Bangkok
    Given the team manager holds role RW-TEAMMGR with Team scope for team "MTG-BKK"
    Given queue "MTG-BKK-CO" belongs to team "MTG-BKK" and role RW-CASEOWN
    Given queue "MTG-BKK-LIT" belongs to team "MTG-BKK" and role RW-LITOFF

  Scenario: AC1 Every case is visible
    Given case "RW-2026-000101", product MORTGAGE, queue "MTG-BKK-CO", owner "U-1001", status ASSIGNED, stage clock start 1 December 2026, service level due 8 December 2026 17:00
    Given case "RW-2026-000102", product MORTGAGE, queue "MTG-BKK-LIT", owner "U-1002", status IN_PROGRESS, stage clock start 8 December 2026, service level due 15 December 2026 17:00
    Given case "RW-2026-000103", product MORTGAGE, queue "MTG-BKK-CO", no owner, status NEW, entry date 10 December 2026
    When the manager opens the list
    Then 3 rows show
    Then row "RW-2026-000101" shows product MORTGAGE, queue "MTG-BKK-CO", owner "U-1001", status ASSIGNED, age in state 9 days and service level state BREACHED
    Then row "RW-2026-000102" shows queue "MTG-BKK-LIT", owner "U-1002", status IN_PROGRESS, age in state 2 days and service level state RUNNING
    Then row "RW-2026-000103" shows owner "Unassigned", status NEW, age in state 0 days and service level state NONE
    Then the rows are in the order "RW-2026-000101", "RW-2026-000102", "RW-2026-000103"

  Scenario: AC2 Ageing is correct when a clock is paused
    Given case "RW-2026-000104" with deviation X1 raised on 9 December 2026
    Given its SERVICE_LEVEL timer has paused true and status PAUSED
    Given its PRESCRIPTION timer has status RUNNING and expires 30 June 2028
    When the list is read
    Then row "RW-2026-000104" shows service level state PAUSED, prescription clock RUNNING with date 30 June 2028 and deviation open Yes
    Then the system does not count the case as breached

  Scenario: AC3 It can be filtered and extracted
    Given the 4 cases above
    When the manager filters by queue "MTG-BKK-CO", product MORTGAGE and breached Yes
    Then 1 row shows, "RW-2026-000101"
    When the manager chooses Extract with the same filters
    Then an Excel file downloads with a header row and 1 data row for "RW-2026-000101" with columns age in state, service level state, service level due, prescription date, prescription clock and deviation open
    Then the access log holds one export entry with the user, the time, the 3 filters and row count 1

  Scenario: AC4 Breach at the boundary of the service level
    Given case "RW-2026-000105" with a RUNNING SERVICE_LEVEL timer due 10 December 2026 09:00
    When the list is read at 10 December 2026 09:00
    Then row "RW-2026-000105" shows service level state RUNNING
    When the list is read at 10 December 2026 09:01
    Then row "RW-2026-000105" shows service level state BREACHED

  Scenario: AC5 A case with no service level timer
    Given case "RW-2026-000103" with status NEW and no SERVICE_LEVEL timer
    When the list is read with breached No
    Then row "RW-2026-000103" shows service level state NONE and is in the result

  Scenario: AC6 A filter value outside its list is refused
    When the manager requests the list with product "CAR"
    Then the response is 422 with message MSG-GEN-007 for field product
    Then the system reads no case

  Scenario: AC7 Page size outside its limits is refused
    When the manager requests the list with page size 500
    Then the response is 422 with message MSG-GEN-002 naming page size, minimum 1 and maximum 200

  Scenario: AC8 No case matches
    When the manager filters by product SSME
    Then the list shows the empty state with message MSG-P3-020
    When the manager chooses Extract with the same filter
    Then an Excel file downloads with the header row and no data row

  Scenario: AC9 Scope limits the list
    Given case "RW-2026-000201" in queue "HP-NE-CO" of team "HP-NE"
    When the manager of team "MTG-BKK" filters by queue "HP-NE-CO"
    Then the list shows the empty state with message MSG-P3-020
    Then case "RW-2026-000201" does not appear in any page of the unfiltered list

  Scenario: AC10 The extract limit
    Given 10,001 cases in the manager's scope match breached No
    When the manager chooses Extract with breached No
    Then the response is 422 with message MSG-P3-021 naming 10,000 rows
    Then the system produces no file

  Scenario: AC11 Order is stable across pages
    Given 120 cases in scope with no breach and the same age in state
    When the manager reads page 1 and page 2 with page size 50
    Then page 1 holds the 50 lowest case numbers and page 2 the next 50
    Then no case appears on both pages
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The list holds only cases in the caller's scope: Own, Team or All, from the role's default scope | role.default_scope; CTL-09 |
| BR2 | Age in state is the whole number of calendar days from stage_clock_start (or entry_date when it is empty) to today in Asia/Bangkok | recovery_case.stage_clock_start, entry_date; RWB-E2-011 ageDays |
| BR3 | A case is breached when its SERVICE_LEVEL timer has status EXPIRED, or has status RUNNING with expires_at earlier than now. A breach does not move the case | R-UNI-30; timer.status |
| BR4 | A deviation pauses the stage clock and keeps the prescription clock running; the list shows both; a paused SERVICE_LEVEL timer is never breached | R-DEV-01; timer.paused |
| BR5 | prescriptionClockStatus is RUNNING or EXPIRED from the PRESCRIPTION timer, and NONE when the case has no such timer | timer.timer_type; LOV-TIMER-STATUS |
| BR6 | Filter values are checked against LOV-PRODUCT, LOV-CASE-STATUS, LOV-STAGE and the queue codes in force | Lists of values; queue table |
| BR7 | The extract holds at most caselist.export.maxrows rows, carries no customer personal field, and is written to the access log before the file is made | RWB-E1-031; CTL-11; REQ-ACA-006 |

## 9. State transitions

None. This story does not change a case status. It reads case, queue and timer records and, through RWB-E1-031, writes one access log entry per extract.

## 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-TEAMMGR, team manager | Reads and extracts the list for the team's queues (Case record R, Team scope) |
| RW-CASEOWN, case owner | Reads and extracts the list for the cases they own (Case record R, Own scope) |
| RW-PRODHEAD, RW-AUDIT, RW-CONDUCT and other roles with Case record R | Read and extract the list in their scope |
| RW-REFADM, reference data administrator | No Case record right; refused with MSG-P4-002 |
| No approval applies | The story takes no decision |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | recovery_case | id | Read |
| DF-CAS-002 | recovery_case | case_no | Read |
| DF-CAS-003 | recovery_case | product_group | Read |
| DF-CAS-005 | recovery_case | status | Read |
| DF-CAS-006 | recovery_case | stage_code | Read |
| DF-CAS-009 | recovery_case | owner_user_id | Read |
| DF-CAS-010 | recovery_case | queue_id | Read |
| DF-CAS-011 | recovery_case | team_code | Read |
| DF-CAS-013 | recovery_case | entry_date | Read |
| DF-CAS-017 | recovery_case | prescription_date | Read |
| DF-CAS-018 | recovery_case | stage_clock_start | Read |
| DF-CAS-019 | recovery_case | deviation_open | Read |
| DF-WRK-002 | queue | queue_code | Read |
| DF-WRK-004 | queue | team_code | Read |
| DF-WRK-028 | timer | case_id | Read |
| DF-WRK-030 | timer | timer_type | Read |
| DF-WRK-032 | timer | expires_at | Read |
| DF-WRK-034 | timer | paused | Read |
| DF-WRK-035 | timer | status | Read |
| DF-REF-038 | role | default_scope | Read |

Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

**GET /api/recovery/v1/cases** (operationId getCases; extended by RWB-E1-031 and RWB-E2-011; this story's change recorded in the additions file)

| Item | Value |
|---|---|
| Query parameters used | product, stage, status, owner, queue, page, size, sort; and the new parameter breached (true or false) |
| Response 200 | CasePage of Case. Each item carries ageDays, serviceLevelDueAt and serviceLevelState (BREACHED, RUNNING, PAUSED, NONE) from RWB-E2-011, and the new field prescriptionClockStatus (RUNNING, EXPIRED, NONE) |
| 401 | No valid session (MSG-P4-001) |
| 403 | Role lacks Case record R (MSG-P4-002) |
| 422 | Filter value outside its list (MSG-GEN-007) or page size outside 1 to 200 (MSG-GEN-002) |
| 503 | Database unavailable (E503) |
| Authorization | Case record, right R; scope filters every row |
| Idempotency | Read only. The same request on unchanged data returns the same rows in the same order |

**GET /api/recovery/v1/cases/export** (from RWB-E1-031; this story's change recorded in the additions file)

| Item | Value |
|---|---|
| Query parameters | The same as GET /cases, including breached, without page and size |
| Response 200 | Excel file with the RWB-E1-031 columns plus age in state, service level state, service level due, prescription date, prescription clock and deviation open |
| 422 | Above caselist.export.maxrows (MSG-P3-021) |
| 503 | Access event not recorded (MSG-P7-003) |
| Authorization | Case record, right R; scope applies |
| Idempotency | Each export writes its own access log entry |

No event is published. The access log entry is written through the RWB-E1-039 interface that RWB-E1-031 already calls.

## 13. Solution plan

**Package.** The story is in the P2 backlog. The endpoints belong to P3 in the API specification and the tables to P3, so under the boundary rule the code is in the P3 package: folder `recovery/casewf/caselist`, Java package `<ACE base package>.recovery.casewf.caselist`, extending the classes of RWB-E1-031 and RWB-E2-011. Front end folder `src/modules/recovery/caselist`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| CaseAndWorkflowController | Controller | Adds the breached parameter and the filter value check to getCases and the export |
| CaseListQueryService | Service | From RWB-E2-011; adds the breached predicate and the order of step 7 |
| PrescriptionClockReader | Service | Computes prescriptionClockStatus from the PRESCRIPTION timer (BR5) |
| AgeingCalculator | Service | Pure functions for BR2 to BR4, unit tested without a database |
| CaseExportService | Service | From RWB-E1-031; adds the ageing and clock columns |
| CaseListPage | React component | SCR-02 columns, breach filter, breach marker and empty state |

**Database.** Reads recovery_case (id, case_no, product_group, status, stage_code, owner_user_id, queue_id, team_code, entry_date, prescription_date, stage_clock_start, deviation_open), queue (queue_code, team_code) and timer (case_id, timer_type, expires_at, paused, status). Writes nothing. Index needed: `CREATE INDEX ix_timer_case_type ON timer (case_id, timer_type) WHERE status IN ('RUNNING','PAUSED','EXPIRED')`, added by a Flyway migration in the P3 migration folder. ix_case_status_queue and ix_case_owner_status serve the other filters.

**Configuration and reference data.** LOV-PRODUCT, LOV-CASE-STATUS, LOV-STAGE through the P4 reference data interface; the queues table (RWB-E1-019); caselist.export.maxrows (RWB-E1-042, assumed 10,000; DL11), loaded by RW-REFADM.

**Build steps**

1. Add the breached parameter and prescriptionClockStatus to the API specification; regenerate types (RWB-TE-003).
2. Write AgeingCalculator and PrescriptionClockReader with unit tests for BR2 to BR5, including AC2 and AC4.
3. Add the breached predicate, the filter value check and the stable order to CaseListQueryService; add the index migration; test AC1, AC5, AC6, AC7, AC9 and AC11.
4. Add the ageing and clock columns to CaseExportService; test AC3, AC8 and AC10.
5. Add the columns, the breach filter and the breach marker to CaseListPage.
6. Add the contract test for the changed operations and the access test for a role without Case record R.

**Feature flag.** `rwb.casewf.case-list-ageing`. Off: the breached parameter is ignored and the list and export keep the RWB-E2-011 and RWB-E1-031 columns.

**Done when.** The tests in section 16 pass; page 1 of the list over 23,600 synthetic cases returns in under 2 seconds at the 95th percentile in SIT (NFR-008).

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-007 | A filter value is not in its list (new) | {value} is not a valid value for {field}. |
| MSG-GEN-002 | Page size outside 1 to 200 | {field} must be between {min} and {max}. |
| MSG-P3-020 | No case matches the filters | No cases match these filters. Change a filter to see more. |
| MSG-P3-021 | Extract above the row limit | The export holds at most {max} rows. Narrow the filters and try again. |
| MSG-P4-001 | No valid session | You have no Recovery Workbench role. Ask your team manager to request one. |
| MSG-P4-002 | Role lacks Case record R | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The export access event cannot be recorded | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

Thai text for each message follows decision DL10.

## 15. Screens and states

SCR-02 Case list, states Loading, Empty, List and Filtered. The team manager sets filters for queue, product, status, stage, owner and breached; reads the columns case number, product, queue, owner, status, stage, age in state, service level state, service level due, prescription date, prescription clock and deviation; and chooses Extract. A breached row carries the text "Breached", not color alone; a paused stage clock shows "Paused". The Empty state shows MSG-P3-020.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-033-01 | AC1, BR1, BR2, BR3 | System | Three cases in team MTG-BKK as in AC1 |
| TC-E2-033-02 | AC2, BR4, BR5 | System | Case with X1 raised, paused SERVICE_LEVEL timer, running PRESCRIPTION timer |
| TC-E2-033-03 | AC3, BR7 | System | Four cases; filters queue, product and breached; extract file and access log |
| TC-E2-033-04 | AC4, BR3 | System | Timer due 10 December 2026 09:00, read at 09:00 and 09:01 |
| TC-E2-033-05 | AC5 | System | NEW case with no SERVICE_LEVEL timer |
| TC-E2-033-06 | AC6, BR6 | System | Product filter CAR |
| TC-E2-033-07 | AC7 | System | Page size 500 |
| TC-E2-033-08 | AC8 | System | Filter product SSME with no SSME case |
| TC-E2-033-09 | AC9, BR1 | System | Case in team HP-NE read by the MTG-BKK manager |
| TC-E2-033-10 | AC10, BR7 | System | 10,001 matching cases |
| TC-E2-033-11 | AC11 | System | 120 cases with equal age, pages of 50 |
| TC-E2-033-12 | Access | Access | RW-REFADM calls the list; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: page size limits, the export limit, lists and service levels are read from the parameter catalog and reference tables.
- No personal data in logs, tests or prompts; the extract carries no customer field.
- No read of another module's tables: the query reads P3 tables only; owner names come from the common module interface.
- The breach flag is computed at read time; the story never changes a timer or a case.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-WKM-002 | Team manager sees every team queue, filters by status, product and ageing, exports the view | Business Requirements Epic 2, section 3.2 | None | All recovery processes | R-UNI-30 | TC-E2-033-01, TC-E2-033-03 to TC-E2-033-12 |
| REQ-DVH-006 | Deviation flag visible in every queue view | Business Requirements Epic 2, section 3.2 | None | All recovery processes | R-DEV-01 | TC-E2-033-02 |

## 19. Out of scope

- Next action columns and the overdue mark: RWB-E2-035.
- My queue and team queue screens with counts, oldest case and cap use: RWB-E2-011.
- Escalation when a service level is breached: RWB-E1-028 and RWB-E2-015.
- Manual transfer from the list: RWB-E2-012.
- The service level values per state: DL22.
