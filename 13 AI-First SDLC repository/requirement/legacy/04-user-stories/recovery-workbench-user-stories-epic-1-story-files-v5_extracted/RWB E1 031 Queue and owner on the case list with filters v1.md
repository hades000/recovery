<!-- source: 04 User stories/Recovery Workbench User Stories Epic 1 Story Files v5.zip!RWB E1 031 Queue and owner on the case list with filters v1.md -->
<!-- converted: 2026-11-04 from Markdown (extracted) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 1 Story Files v5.zip!RWB E1 031 Queue and owner on the case list with filters v1.md`  
> **Converted from:** Markdown (extracted)

# RWB-E1-031 Queue and owner on the case list with filters

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E1-031 |
| Epic | E1, release 30 November 2026 |
| Module | P3 Case and workflow |
| Feature | FEAT-CWC-19 Show queue and owner on the case list |
| Requirement IDs | REQ-CWC-007, REQ-ACA-009 |
| BRD section | Business Requirements Epic 1, sections 3.3 and 3.4; Business Requirements Program, sections 5.3 and 5.4 |
| L3 process | 06 Take over and own the case |
| Decision | None |
| Priority | Must |
| Depends on | RWB-E1-020, RWB-E1-039 |
| Status | Ready for build |

## 1. Story

As a **team manager (RW-TEAMMGR)**, I want **the queue and owner columns on the case list, with filters by queue, team and status and an export to Excel**, so that **I see my queues and who owns each case without a new screen**.

## 2. Business rationale

Today a team manager asks each collector for their list to know who holds which case. With allocation by rule (RWB-E1-020), every case has a queue and an owner; this story shows both on the case list, filters by queue, team and status inside the manager's scope, and exports the filtered list with the export written to the access log for PDPA. It meets REQ-CWC-007 (the result of allocation is visible) and REQ-ACA-009 (a user sees only the cases their scope allows).

## 3. Preconditions

- RWB-E1-020 is done: cases carry queue_id, team_code and owner_user_id.
- RWB-E1-039 is done: the access log interface records exports.
- The user holds a role with Case record R; the team manager's default scope is Team (roles.txt).
- Parameter `caselist.export.maxrows` = 10,000 (assumed; DL11) from RWB-E1-042.
- Owner display names come from the ACE user directory in the common module.

## 4. Flow

1. Team manager: opens SCR-02 Case list; the screen shows the Loading state.
2. CaseListPage: calls GET /cases with page 0 and size 50; the service applies the caller's scope.
3. CaseListPage: shows each row with case number, product, status, stage, queue, owner and entry date (list state).
4. Team manager: picks queue "DIL-BKK-CO", team "DIL-BKK" and status "ASSIGNED"; the page calls GET /cases with the filters (filtered state).
5. CaseQueryService: returns only cases inside the caller's scope that meet every filter, with the total.
6. Team manager: chooses Export.
7. CaseExportService: checks the row count against the limit, publishes the access event AC-EXPT with user, time, filters and row count, then builds the xlsx with masking by role (FieldMasker, RWB-E1-037).
8. Browser: downloads "Case list 20261202 1.xlsx".

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | No case meets the filters | Empty state with a plain sentence | MSG-P3-020 | AC3 |
| X2 | The filtered list holds more rows than the export limit | Export refused; the user narrows the filter | MSG-P3-021 | AC4 |
| X3 | The access log cannot be written | Export not made | MSG-P7-003 | AC5 |
| X4 | A filter names a queue outside the caller's scope | Only in-scope cases return; an out-of-scope queue returns none | MSG-P3-020 | AC6 |
| X5 | A case has no owner | Owner cell is blank; the case is still listed | None | AC7 |
| X6 | Exactly 10,000 rows | Export allowed | None | AC8 |
| X7 | A role without Case record R opens the list | Refused with 403 | MSG-P4-002 | Access test TC-E1-031-09 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Reads fields RWB-E1-020 fills; adds columns and filters to an existing screen |
| Negotiable | Column order and the export limit are configurable |
| Valuable | Team managers see ownership on one screen |
| Estimable | Two query parameters, one export endpoint, one screen change |
| Small | Fits under one week |
| Testable | Every criterion has a test case in section 16 |

## 7. Acceptance criteria

```gherkin
Feature: Queue and owner on the case list with filters

  Background:
    Given team manager U-71 of team "DIL-BKK" with scope Team
    Given team "DIL-BKK" has 64 cases in queue "DIL-BKK-CO" and 20 in "DIL-BKK-OVF"

  Scenario: AC1 Filter by queue
    Given the case list
    When U-71 filters by queue "DIL-BKK-CO"
    Then 64 cases show, each with its owner and status
    Then no case from another queue shows

  Scenario: AC2 Export
    Given the list filtered by queue "DIL-BKK-CO" and status "ASSIGNED" with 51 cases
    When U-71 chooses Export
    Then an Excel file with 51 rows downloads
    Then the access log holds the export with user U-71, the time, the filters and 51 rows

  Scenario: AC3 No case meets the filters
    When U-71 filters by queue "DIL-BKK-CO" and status "WAITING_PARTNER" and no case matches
    Then the list shows the empty state with MSG-P3-020

  Scenario: AC4 Export above the limit
    Given parameter "caselist.export.maxrows" is 10000
    Given a filtered list of 10,001 cases for a user with scope All
    When the user chooses Export
    Then the system makes no file
    Then MSG-P3-021 shows with maximum 10000

  Scenario: AC5 Access log unavailable
    Given the access log store is unavailable
    When U-71 chooses Export on a list of 51 cases
    Then the system makes no file
    Then MSG-P7-003 shows

  Scenario: AC6 Queue outside the scope
    When U-71 filters by queue "LIT-BKK-OFF" of team "LIT-BKK"
    Then no case shows
    Then the list shows the empty state with MSG-P3-020

  Scenario: AC7 A case with no owner
    Given case RW-2026-000601 is in queue "DIL-BKK-OVF" with no owner
    When U-71 filters by queue "DIL-BKK-OVF"
    Then case RW-2026-000601 shows with a blank owner cell

  Scenario: AC8 Export at the limit
    Given a filtered list of exactly 10,000 cases for a user with scope All
    When the user chooses Export
    Then a file with 10,000 rows downloads
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The list holds only cases inside the caller's scope (Own, Team, Region, All) | REQ-ACA-009; CTL-09; LOV-SCOPE |
| BR2 | Filters combine with AND | FSD A2.19 |
| BR3 | Every export is written to the access log before the file is made | REQ-ACA-006; CTL-11 |
| BR4 | Export columns follow the masking rules for the caller's role | REQ-ACA-005; DL26 |
| BR5 | An export holds at most the configured number of rows | Parameter caselist.export.maxrows = 10,000 (assumed; DL11) |
| BR6 | A screen responds in under 2 seconds | NFR-008 |

## 9. State transitions

None. This story does not change a case status. It reads queue, owner and status only.

## 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-TEAMMGR | Lists, filters and exports cases in team scope (Case record R) |
| RW-CASEOWN | Lists and exports their own cases (Case record R, scope Own) |
| Every role with Case record R | Lists cases in its scope |
| RW-REFADM, RW-SECADM | No Case record right; refused |
| RW-COMPLY | Reads the access log entries for exports |

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
| DF-CAS-012 | recovery_case | region_code | Read |
| DF-CAS-013 | recovery_case | entry_date | Read |
| DF-WRK-001 | queue | id | Read |
| DF-WRK-002 | queue | queue_code | Read |
| DF-WRK-003 | queue | queue_name | Read |
| DF-WRK-004 | queue | team_code | Read |

Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

**GET /api/recovery/v1/cases**

| Item | Value |
|---|---|
| Request | Query queue (uuid), status, owner, product, stage, page, size, sort; new query parameter team (see additions) |
| Response | CasePage: items (Case with caseNo, productGroup, status, stageCode, queueId, ownerUserId, teamCode, entryDate), page, size, total |
| Errors | 401 (MSG-P4-001); 403 no Case record R (MSG-P4-002); 503 |
| Authorization | Case record, right R, scope applied |
| Idempotency | Not applicable |

**GET /cases/export** (new endpoint, see additions)

| Item | Value |
|---|---|
| Request | The same query parameters as GET /cases, without page and size |
| Response | 200 application/vnd.openxmlformats-officedocument.spreadsheetml.sheet |
| Errors | 401; 403 no Case record R (MSG-P4-002); 422 above the row limit (MSG-P3-021); 503 access log unavailable (MSG-P7-003) |
| Authorization | Case record, right R, scope applied |
| Idempotency | Not applicable; each export is a new access log entry |

**Published interface used (P4, RWB-E1-039)**

```java
// package recovery.access.accesslog
public interface AccessEventPublisher {
    void publish(AccessEvent event) throws DecisionLogUnavailableException;
}
// this story sends eventCode AC-EXPT with actorUserRef, area "Case record", right R, filter, rowCount
```

## 13. Solution plan

**Package.** Back end `recovery/casewf/caselist` (Java package `recovery.casewf.caselist`); front end `src/modules/recovery/casewf/caselist`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| CaseAndWorkflowController | Controller | GET /cases with the team filter; GET /cases/export |
| CaseQueryService | Service | Builds the scoped query with the filters; joins queue for code and name |
| CaseExportService | Service | Row limit, access log entry, xlsx with masked columns |
| CaseAndWorkflowRepository | Repository | Paged query on recovery_case and queue |
| CaseListPage | React component | SCR-02 with queue and owner columns and the states Loading, empty, list, filtered |
| CaseListFilters | React component | Queue, team and status pickers from the queues and lists in force |
| ExportButton | React component | Calls the export and shows MSG-P3-021 or MSG-P7-003 |

**Database**

- Reads recovery_case and queue only; uses ix_case_status_queue (status, queue_id) and ix_case_owner_status.
- Add `ix_case_team_status ON recovery_case (team_code, status)` in migration `V031_1__case_team_index.sql`.

**Configuration and reference data**

- Parameter caselist.export.maxrows (RWB-E1-042).
- Queues from RWB-E1-019; LOV-CASE-STATUS and LOV-TEAM through the P4 list interface.
- Labels "Export" and "Owner user ID" from the label standard (DL10).

**Build steps**

1. Team filter on GET /cases and the scoped query; tests AC1, AC6.
2. CaseListPage columns and states with Radix table; tests AC3, AC7.
3. CaseExportService with the limit and the access log first; tests AC2, AC4, AC5, AC8.
4. Export endpoint and ExportButton; file name "Case list YYYYMMDD 1.xlsx".
5. Access test and the 2 second check on 26,500 cases.

**Feature flag.** `rwb.p3.caselistqueue`. Off: the list hides the queue and owner columns and the export.

**Done when.** The tests in section 16 pass and the list answers in under 2 seconds on 26,500 cases in SIT (NFR-008).

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-020 | No case meets the filters | No cases match these filters. Change a filter to see more. |
| MSG-P3-021 | Export above the row limit | The export holds at most {max} rows. Narrow the filters and try again. |
| MSG-P7-003 | Access log unavailable at export | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |

## 15. Screens and states

SCR-02 Case list. Loading: skeleton rows. Empty: MSG-P3-020. List: columns case number, product, status, stage, queue, owner, entry date. Filtered: the chosen queue, team and status show above the list with a clear control; Export uses the filters shown.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-031-01 | AC1, BR1, BR2 | System | 64 cases in DIL-BKK-CO |
| TC-E1-031-02 | AC2, BR3, BR4 | System | 51 cases filtered by queue and status |
| TC-E1-031-03 | AC3 | System | Filter with no match |
| TC-E1-031-04 | AC4, BR5 | System | 10,001 cases, scope All |
| TC-E1-031-05 | AC5, BR3 | System | Access log store down |
| TC-E1-031-06 | AC6, BR1 | System | Queue of another team |
| TC-E1-031-07 | AC7 | System | Case with no owner |
| TC-E1-031-08 | AC8, BR5 | System | Exactly 10,000 cases |
| TC-E1-031-09 | Access | Access | RW-REFADM calls GET /cases and is refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: the export limit and the lists come from data.
- No personal data in logs, tests or prompts; the export applies masking by role and holds no customer name or ID number.
- No read of another module's tables: the access log is written through AccessEventPublisher (P4); owner names come from the ACE user directory interface.
- The export is never made when its access log entry cannot be written.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CWC-007 | Every case has a queue and an owner by rule, visible on the case list | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-19 | 06 Take over and own the case | None | TC-E1-031-01, TC-E1-031-03, TC-E1-031-07 |
| REQ-ACA-009 | A user sees only the cases their scope allows | Epic 1, 3.4; Program, 5.4 | FEAT-CWC-19 | 06 Take over and own the case | None | TC-E1-031-02, TC-E1-031-04, TC-E1-031-05, TC-E1-031-06, TC-E1-031-08 |

## 19. Out of scope

- My queue and team queue screens (RWB-E2-011, SCR-07 in Epic 2).
- The base case list with filters by product, stage, age and deviation (RWB-E1-002, FEAT-RDF-18).
- The masking rules themselves (RWB-E1-037, DL26).
