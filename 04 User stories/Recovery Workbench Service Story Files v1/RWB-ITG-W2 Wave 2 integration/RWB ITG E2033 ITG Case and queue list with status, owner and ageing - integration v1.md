# RWB-ITG-E2033-ITG Case and queue list with status, owner and ageing

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-E2033-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W2 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-033 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP06, DP07, DP08, DP13, DP14, DP15, DP19 |
| Parallel lane | L-ITG-W2 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | RWB-P3-E1018-APP, RWB-P3-E1031-APP, RWB-P3-E2011-APP, RWB-P2-E2033-APP, RWB-P3-E2033-APP, RWB-P4-E2033-APP, RWB-S8-E2033-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-019, FR-PLT-026, FR-PLT-033) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-033 for the wave 2 integration harness. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **team manager (RW-TEAMMGR)**, I want **a repeatable cross-service journey harness that opens the case list over the team's queues and shows every case with its identifier, product, queue, owner, status, age in state, stage, prescription clock state and service level breach flag, filters it by status, product and ageing, and extracts the same columns to Excel — with the deviation flag that marks a paused case on the same rows**, so that **the manager's daily view is proven end to end across rwb-case, rwb-access, rwb-deviation and rwb-integration before RWB-P3-E2033-APP, RWB-P3-E1018-APP, RWB-P3-E1031-APP, RWB-P3-E2011-APP, RWB-P4-E2033-APP, RWB-S8-E2033-APP and RWB-P2-E2033-APP claim Done**.

This story builds the harness, its contract fakes, its seed pack, its evidence pack and its pass or fail gate. It builds no production endpoint, no screen, no table and no migration. Nothing it writes is deployed to a service.

No single app story can prove the journey. RWB-P3-E1018-APP proves the case record and its fields. RWB-P3-E1031-APP proves the queue and owner columns and the export. RWB-P3-E2011-APP proves the age in state and the service-level state. RWB-P3-E2033-APP proves the breached filter, the prescription clock and the export columns. RWB-P4-E2033-APP proves the scope and the Case record right. RWB-S8-E2033-APP proves the deviation flag and its pause of the stage clock. RWB-P2-E2033-APP proves the routed read the screen uses. Only their agreement proves that one row on the list, one export row and one access-log entry describe the same case at the same instant — and that agreement is this story.

### 2. Business rationale

RWB-E2-033 split into six app stories and this integration story. The app stories build the case record fields, the queue and owner columns with the export, the age in state and the service-level state, the breached filter and the prescription clock, the role scope and the access-log entry, and the deviation flag with its pause, each inside its own service. What no app story can prove on its own is the chain the manager actually relies on: a manager opens the list, the session and the role's default scope are read, the case query returns rows with queue, owner, age in state and service-level state, the prescription clock is added beside the stage clock, a breached case is marked and is never a paused one, the extract is written after its access-log entry, and the deviation flag makes the pause visible in every queue. That proof is this story.

The journey carries three requirements. The team manager sees every team queue, filters by status, product and ageing and exports the view (REQ-WKM-002): the harness asserts that one read holds all three queues' cases in scope in one order and that the export carries the same rows and columns. The deviation flag is visible in every queue view (REQ-DVH-006): the harness asserts that case "RW-2026-000104" reads PAUSED with the deviation open and is not counted as breached on any read or in the file. Every read of the case store is written to the access log (REQ-ACA-006): the harness asserts one entry per extract, written before the file, carrying the user, the time, the filters and the row count.

Architecture v5 changes the path, not the business. In the monolith the case query, the queue table, the timers and the export sat in one deployment and one schema. In the target:

- the case, the queue, the timer and the access log are read through their owners' contracts, and the harness never reads a table of any schema (DP-01);
- the export row limit, the page limits and the service level values are parameters of rwb-case, never values in the harness (DP-06);
- LOV-PRODUCT, LOV-CASE-STATUS, LOV-STAGE, LOV-TIMER-STATUS and the queue codes are reference data of rwb-case, loaded into the seed pack as files (DP-07);
- the authorise check is rwb-access's, driven through its session operation and its roles operation, with the refusal asserted rather than reproduced (DP-08);
- every path is on the owner's base `/api/recovery/<short>/v1` (DP-13);
- no legacy `rwb.p<n>.` or `rwb.casewf.` topic name survives: the harness subscribes to `rwb.case.events.v1` and `rwb.deviation.events.v1` and asserts the naming library's topic names (DP-14);
- each service migrates its own schema through its own Flyway sequence, and the harness runs no migration (DP-15);
- the journey runs through the gateway-bff composite route the case list screen uses, so the harness drives the same route the manager drives (DP-19).

The measure is the journey evidence: for each owned criterion, one pass or fail with the rows, the ages, the service-level states, the timers, the export cells, the access-log entry and the deviation flag captured in one report that can be re-run for any build and any business date.

### 3. Preconditions

- The wave 2 harness environment (SIT) is available with the gateway route for `/api/recovery/*`, the topics `rwb.case.events.v1` and `rwb.deviation.events.v1`, the Temporal namespace `rwb-recovery` with the task queues `rwb-case` and `rwb-deviation`, and a tool that compares an Excel file cell by cell. Not specified in the source documents (GAP-0415; ASM-0590): the harness environment, its seed pack and its evidence format.
- The seven integration dependencies have published their contracts, or their contract fakes stand in for them: RWB-P3-E1018-APP (the case record and its fields), RWB-P3-E1031-APP (the queue and owner columns and the export), RWB-P3-E2011-APP (the age in state and the service-level state), RWB-P3-E2033-APP (the breached filter, the prescription clock and the export columns), RWB-P4-E2033-APP (the session, the role's default scope, the access-log entry and the refusals), RWB-S8-E2033-APP (the deviation flag and its pause of the stage clock) and RWB-P2-E2033-APP (the routed read the screen uses).
- Team "MTG-BKK" holds queue "MTG-BKK-CO" with role RW-CASEOWN and queue "MTG-BKK-LIT" with role RW-LITOFF, and the caller holds RW-TEAMMGR with Case record R and Team scope for "MTG-BKK" (legacy sections 3 and 7).
- Today is 10 December 2026 at 09:00 Asia/Bangkok. Case "RW-2026-000101" is product MORTGAGE, queue "MTG-BKK-CO", owner "U-1001", status ASSIGNED, stage clock start 1 December 2026, service level due 8 December 2026 17:00. Case "RW-2026-000102" is product MORTGAGE, queue "MTG-BKK-LIT", owner "U-1002", status IN_PROGRESS, stage clock start 8 December 2026, service level due 15 December 2026 17:00. Case "RW-2026-000103" is product MORTGAGE, queue "MTG-BKK-CO", no owner, status NEW, entry date 10 December 2026. Case "RW-2026-000105" carries a RUNNING SERVICE_LEVEL timer due 10 December 2026 09:00 (legacy AC1, AC4, AC5).
- Case "RW-2026-000104" has deviation X1 raised on 9 December 2026, its SERVICE_LEVEL timer paused true with status PAUSED, and its PRESCRIPTION timer RUNNING to 30 June 2028 (legacy AC2).
- Case "RW-2026-000201" sits in queue "HP-NE-CO" of team "HP-NE", outside the manager's scope; a test user of role RW-REFADM holds no Case record right (legacy AC9, X9).
- The parameters carry caselist.export.maxrows = 10,000 (assumed; DL11) from the legacy parameter of RWB-E1-042, the page size range is 1 to 200, and the SIT data set holds 23,600 synthetic cases for the NFR-008 read (legacy sections 3 and 13).
- The feature switch `rwb.casewf.case-list-ageing` is on in the harness profile, and every case, owner and role in the seed pack is synthetic: no customer name, account number, national identifier or contact detail enters the harness, the seed pack, the export sample or the evidence pack (legacy sections 13 and 17).
- No build dependency. Day 1.

### 4. Flow

1. Harness: takes the run lock for the environment and records the build ID, the business date 10 December 2026, the fixed clock at 09:00 Asia/Bangkok and the versions of the seven contracts it is about to exercise.
2. Harness: seeds team "MTG-BKK", the two queues with their roles, cases "RW-2026-000101" to "RW-2026-000105" and case "RW-2026-000201", the SERVICE_LEVEL and PRESCRIPTION timers, deviation X1 for "RW-2026-000104", the export limit of 10,000 rows and the 23,600-case pack for the NFR read.
3. Harness: calls `GET /api/recovery/access/v1/me/session` against the rwb-access fake and records the role RW-TEAMMGR, the Team scope for "MTG-BKK" and Case record R, then reads `GET /api/recovery/access/v1/admin/roles` and records the role's default scope it asserts against.
4. Harness: subscribes to `rwb.case.events.v1` and `rwb.deviation.events.v1` with its own consumer group before the first read, so the pause of case "RW-2026-000104" is observed and not inferred.
5. Harness: reads page 1 of `GET /api/recovery/case/v1/cases` with no filter and asserts three rows with product, queue, owner, status, age in state 9, 2 and 0 days, service-level states BREACHED, RUNNING and NONE, and the order "RW-2026-000101", "RW-2026-000102", "RW-2026-000103".
6. Harness: reads the same operation with the breached filter set and asserts one row, "RW-2026-000101", and that "RW-2026-000104" is absent from it.
7. Harness: runs the two boundary reads at 09:00 and 09:01 for case "RW-2026-000105" and asserts RUNNING at 09:00 and BREACHED at 09:01 with no timer or case changed.
8. Harness: reads `GET /api/recovery/case/v1/cases/{caseId}` and `GET /api/recovery/case/v1/cases/{caseId}/timers` for "RW-2026-000104" and asserts PAUSED, the prescription clock RUNNING to 30 June 2028 and the deviation open Yes.
9. Harness: runs the filter refusals — product "CAR" answering 422 MSG-GEN-007 for field product with no case read, page size 500 answering 422 MSG-GEN-002 naming page size, minimum 1 and maximum 200, and product SSME answering the empty state MSG-P3-020.
10. Harness: runs `GET /api/recovery/case/v1/cases/export` with queue "MTG-BKK-CO", product MORTGAGE and breached Yes, compares the file cell by cell with the row the list returned, then reads `GET /api/recovery/access/v1/admin/access-log` and asserts one entry with the user, the time, the three filters and row count 1.
11. Harness: runs the scope case (queue "HP-NE-CO" answering the empty state, case "RW-2026-000201" absent from every page), the not-authorized case (RW-REFADM answering 403 MSG-P4-002), the extract limit (10,001 matching cases answering 422 MSG-P3-021 naming 10,000 rows with no file) and the stable paging read (two pages of 50 from 120 cases with the same age).
12. Harness: writes the per-scenario evidence into one run report keyed by story key and business date, measures the 23,600-case page-1 read at the 95th percentile, evaluates the gate, attaches the report to the wave 2 release record, releases the lock and restores the seed.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A filter value is not in its list of values, for example product CAR | Request refused with 422; nothing is read | MSG-GEN-007 | AC6 |
| X2 | Page size below 1 or above 200 | Request refused with 422 | MSG-GEN-002 | AC7 |
| X3 | No case matches the filters | Empty state; the extract holds the header row only | MSG-P3-020 | AC8 |
| X4 | A queue filter names a queue outside the caller's scope | Only cases in scope are returned, so the result is empty | MSG-P3-020 | AC9 |
| X5 | A case has no SERVICE_LEVEL timer yet (status NEW) | serviceLevelState NONE; breached false | None | AC5 |
| X6 | The service level due time equals the current time | Not breached; breached from the next minute | None | AC4 |
| X7 | The extract would hold more than 10,000 rows | Extract refused; no file is produced | MSG-P3-021 | AC10 |
| X8 | A case changes between two page requests | Order is stable by case number; no case appears twice | None | AC11 |
| X9 | The caller's role does not hold Case record R, or the session is no longer valid | Refused with 403 or 401; nothing is read | MSG-P4-002, MSG-P4-001 | TC-E2-033-12-ITG |
| X10 | The seed pack cannot be loaded or the evidence cannot be attached | The run refuses to start and names the missing seed item, or is marked failed; the local evidence file is kept for rerun | None to a user | All |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the seven published contracts or their fakes, the seed pack and the fixed clock; it builds no service feature and has no build dependency |
| Negotiable | The scenarios, the seeded values, the lists of values, the queue codes and the export limit are data files, never code |
| Valuable | The manager's list, its breach filter, its export and its access-log entry are proven once across four services, in the same evidence as the deviation flag |
| Estimable | One journey runner, one fake set, one fixture pack, three assertion helpers, one evidence collector, one gate |
| Small | Fits in one sprint with its tests |
| Testable | Each owned criterion has a fixed Given, When and Then and a recorded pass or fail in the report |

### 7. Acceptance criteria

```gherkin
Feature: Case and queue list with status, owner and ageing

  Background:
    Given today is 10 December 2026 at 09:00 Asia/Bangkok
    Given the rwb-access contract answers role RW-TEAMMGR with Team scope for team "MTG-BKK" and Case record R
    Given queue "MTG-BKK-CO" belongs to team "MTG-BKK" and role RW-CASEOWN
    Given queue "MTG-BKK-LIT" belongs to team "MTG-BKK" and role RW-LITOFF

  Scenario: AC1 Every case is visible in one list across the team's queues (new, D-RCV-60)
    Given case "RW-2026-000101", product MORTGAGE, queue "MTG-BKK-CO", owner "U-1001", status ASSIGNED, stage clock start 1 December 2026, service level due 8 December 2026 17:00
    Given case "RW-2026-000102", product MORTGAGE, queue "MTG-BKK-LIT", owner "U-1002", status IN_PROGRESS, stage clock start 8 December 2026, service level due 15 December 2026 17:00
    Given case "RW-2026-000103", product MORTGAGE, queue "MTG-BKK-CO", no owner, status NEW, entry date 10 December 2026
    When the harness reads page 1 of the list with no filter
    Then 3 rows show
    Then row "RW-2026-000101" shows product MORTGAGE, queue "MTG-BKK-CO", owner "U-1001", status ASSIGNED, age in state 9 days and service level state BREACHED
    Then row "RW-2026-000102" shows queue "MTG-BKK-LIT", owner "U-1002", status IN_PROGRESS, age in state 2 days and service level state RUNNING
    Then row "RW-2026-000103" shows owner "Unassigned", status NEW, age in state 0 days and service level state NONE
    Then the rows are in the order "RW-2026-000101", "RW-2026-000102", "RW-2026-000103"
    Then the read answers inside the 2 s timeout of one hop through the gateway route

  Scenario: AC2 Ageing is correct when a clock is paused (new, D-RCV-60)
    Given case "RW-2026-000104" with deviation X1 raised on 9 December 2026
    Given its SERVICE_LEVEL timer has paused true and status PAUSED
    Given its PRESCRIPTION timer has status RUNNING and expires 30 June 2028
    When the list is read and the case and its timers are read
    Then row "RW-2026-000104" shows service level state PAUSED, prescription clock RUNNING with date 30 June 2028 and deviation open Yes
    Then the system does not count the case as breached and the breached filter does not return it
    Then the deviation flag and the two timers read through the P3 operations carry the same pause the rwb-deviation events announced

  Scenario: AC3 It can be filtered and extracted (new, D-RCV-60)
    Given the 4 cases above
    When the manager filters by queue "MTG-BKK-CO", product MORTGAGE and breached Yes and then chooses Extract with the same filters
    Then 1 row shows, "RW-2026-000101"
    Then an Excel file downloads with a header row and 1 data row for "RW-2026-000101" with columns age in state, service level state, service level due, prescription date, prescription clock and deviation open
    Then the access log holds one export entry with the user, the time, the 3 filters and row count 1
    Then the ageing and clock cells of the file equal the row the list returned for the same filters

  Scenario: AC4 Breach at the boundary of the service level (new, D-RCV-60)
    Given case "RW-2026-000105" with a RUNNING SERVICE_LEVEL timer due 10 December 2026 09:00
    When the list is read at 10 December 2026 09:00
    Then row "RW-2026-000105" shows service level state RUNNING
    Then when the list is read again at 10 December 2026 09:01, row "RW-2026-000105" shows service level state BREACHED
    Then no read changed a timer or a case

  Scenario: AC5 A case with no service level timer (new, D-RCV-60)
    Given case "RW-2026-000103" with status NEW and no SERVICE_LEVEL timer
    When the list is read with breached No
    Then row "RW-2026-000103" shows service level state NONE and is in the result

  Scenario: AC6 A filter value outside its list is refused (new, D-RCV-60)
    When the manager requests the list with product "CAR"
    Then the response is 422 with message MSG-GEN-007 for field product
    Then the system reads no case

  Scenario: AC7 Page size outside its limits is refused (new, D-RCV-60)
    When the manager requests the list with page size 500
    Then the response is 422 with message MSG-GEN-002 naming page size, minimum 1 and maximum 200

  Scenario: AC8 No case matches (new, D-RCV-60)
    When the manager filters by product SSME and then chooses Extract with the same filter
    Then the list shows the empty state with message MSG-P3-020
    Then an Excel file downloads with the header row and no data row

  Scenario: AC9 Scope limits the list (new, D-RCV-60)
    Given case "RW-2026-000201" in queue "HP-NE-CO" of team "HP-NE"
    When the manager of team "MTG-BKK" filters by queue "HP-NE-CO"
    Then the list shows the empty state with message MSG-P3-020
    Then case "RW-2026-000201" does not appear in any page of the unfiltered list

  Scenario: AC10 The extract limit (new, D-RCV-60)
    Given 10,001 cases in the manager's scope match breached No
    When the manager chooses Extract with breached No
    Then the response is 422 with message MSG-P3-021 naming 10,000 rows
    Then the system produces no file

  Scenario: AC11 Order is stable across pages (new, D-RCV-60)
    Given 120 cases in scope with no breach and the same age in state
    When the manager reads page 1 and page 2 with page size 50
    Then page 1 holds the 50 lowest case numbers and page 2 the next 50
    Then no case appears on both pages
```

No legacy acceptance criterion is owned by this story: the eleven above are new and test only the integration deliverable, using the legacy values of RWB-E2-033 and no other. The refusal of a role without Case record R is carried by TC-E2-033-12-ITG, because a refusal is a component assertion with no list to read.

### 8. Business rules

| ID | Rule | Source | Proved by |
|---|---|---|---|
| BR1 | The list holds only cases in the caller's scope: Own, Team or All, from the role's default scope | role.default_scope; CTL-09 | AC1, AC9 |
| BR2 | Age in state is the whole number of calendar days from stage_clock_start (or entry_date when it is empty) to today in Asia/Bangkok | recovery_case.stage_clock_start, entry_date; RWB-E2-011 ageDays | AC1, AC5 |
| BR3 | A case is breached when its SERVICE_LEVEL timer has status EXPIRED, or has status RUNNING with expires_at earlier than now. A breach does not move the case | R-UNI-30; timer.status | AC1, AC4 |
| BR4 | A deviation pauses the stage clock and keeps the prescription clock running; the list shows both; a paused SERVICE_LEVEL timer is never breached | R-DEV-01; timer.paused | AC2 |
| BR5 | prescriptionClockStatus is RUNNING or EXPIRED from the PRESCRIPTION timer, and NONE when the case has no such timer | timer.timer_type; LOV-TIMER-STATUS | AC2 |
| BR6 | Filter values are checked against LOV-PRODUCT, LOV-CASE-STATUS, LOV-STAGE and the queue codes in force | The lists of values and the queue table | AC6, AC9 |
| BR7 | The extract holds at most caselist.export.maxrows rows, carries no customer personal field, and is written to the access log before the file is made | RWB-E1-031; CTL-11; REQ-ACA-006 | AC3, AC8, AC10 |

The rules are unchanged by the split. The harness asserts them across the service boundaries and restates none of them in code: the lists of values, the queue codes, the export limit and the service level values are seeded data.

### 9. State transitions

None for the case. This story changes no case status, no timer status and no deviation state; the harness asserts that no case, timer or deviation moves because of a list read or an extract.

The story reads case, queue and timer records through the P3 operations and writes exactly one access-log entry per extract through the P4 contract, which is the only write the journey causes. The harness asserts that the entry precedes the file and that a refused extract writes no entry.

The harness adds a run state of its own only: Not started, Running, Passed, Failed, with the latest run for a build deciding the gate.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-TEAMMGR, team manager | Reads and extracts the list for the team's queues (Case record R, Team scope); the role the journey runs under |
| RW-CASEOWN, case owner | Reads and extracts the list for the cases they own (Case record R, Own scope) |
| RW-PRODHEAD, RW-AUDIT, RW-CONDUCT and other roles with Case record R | Read and extract the list in their scope |
| RW-REFADM, reference data administrator | No Case record right; refused with MSG-P4-002 (TC-E2-033-12-ITG) |
| Integration lead | Agrees the fake set, the fixed clock and the run window with the four service owners |
| QA lead | Owns the seed pack, the evidence format and the pass or fail gate |
| No approval applies | The story takes no business decision and no delegation of authority level is used |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | recovery_case | id | Read through the P3 case operation |
| DF-CAS-002 | recovery_case | case_no | Read through the P3 case operation |
| DF-CAS-003 | recovery_case | product_group | Read through the P3 case operation |
| DF-CAS-005 | recovery_case | status | Read through the P3 case operation |
| DF-CAS-006 | recovery_case | stage_code | Read through the P3 case operation |
| DF-CAS-009 | recovery_case | owner_user_id | Read through the P3 case operation |
| DF-CAS-010 | recovery_case | queue_id | Read through the P3 case operation |
| DF-CAS-011 | recovery_case | team_code | Read through the P3 case operation (scope) |
| DF-CAS-013 | recovery_case | entry_date | Read through the P3 case operation (age fallback) |
| DF-CAS-017 | recovery_case | prescription_date | Read through the P3 case operation |
| DF-CAS-018 | recovery_case | stage_clock_start | Read through the P3 case operation (age) |
| DF-CAS-019 | recovery_case | deviation_open | Read through the P3 case operation (the deviation flag) |
| DF-WRK-002 | queue | queue_code | Read through the P3 queue and case operations |
| DF-WRK-004 | queue | team_code | Read through the P3 queue and case operations |
| DF-WRK-028 | timer | case_id | Read through the P3 timer operation |
| DF-WRK-030 | timer | timer_type | Read through the P3 timer operation |
| DF-WRK-032 | timer | expires_at | Read through the P3 timer operation |
| DF-WRK-034 | timer | paused | Read through the P3 timer operation |
| DF-WRK-035 | timer | status | Read through the P3 timer operation |
| DF-REF-038 | role | default_scope | Read through the P4 roles operation |

The harness owns no table in any schema and no schema at all: no table, no view, no migration and no seed table is created by this story. It reads through the operations of section 12, and its own evidence holds identifiers, states, message ids and timestamps only, never personal data. The case-list read is P3's under the R-PREC default ruling; `case_list_row` stays P1's daily published projection built for reconciliation, and the harness neither reads nor seeds it. Field IDs are those of the Logical Data Model and Data Dictionary.

### 12. Contract

#### 12.1 REST operations provided

None. The harness is a test asset in the integration pipeline and provides no REST operation.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| GET | `/api/recovery/case/v1/cases` | P3 rwb-case | The list with the filters, the page and the size, and the ageing, service-level and prescription columns (AC1, AC4, AC5, AC6, AC7, AC8, AC9, AC11) |
| GET | `/api/recovery/case/v1/cases/export` | P3 rwb-case | The Excel extract with the ageing and clock columns, and its row limit (AC3, AC8, AC10) |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The single case, its age in state and its deviation flag (AC2, AC4) |
| GET | `/api/recovery/case/v1/cases/{caseId}/timers` | P3 rwb-case | The SERVICE_LEVEL and PRESCRIPTION timer projection, their status and pause (AC2, AC4, AC5) |
| GET | `/api/recovery/access/v1/me/session` | P4 rwb-access | The role, the Team scope and Case record R the journey runs under (AC1, AC9, TC-E2-033-12-ITG) |
| GET | `/api/recovery/access/v1/admin/access-log` | P4 rwb-access | The export entry with the user, the time, the filters and the row count (AC3) |
| GET | `/api/recovery/access/v1/admin/roles` | P4 rwb-access | The role's default scope check behind the scope of every row (AC1, AC9, TC-E2-033-12-ITG) |

Every call is one hop on the owner's base `/api/recovery/<short>/v1` with the 2 s timeout, and every read is idempotent on unchanged data. The scope check that rwb-case makes inside its own process is not a path in the Ownership Map, so the harness seeds it through the role, the scope and the right of the rwb-access fake (12.8) and reads the resulting answer through the P3 operations instead of calling an access path of its own.

#### 12.3 Events published

None. The harness publishes no Kafka event on a production topic; the seed of section 4 is loaded as data, and the evidence goes to the release record through the pipeline.

#### 12.4 Events consumed

| Event | Topic | Owner | Use |
|---|---|---|---|
| `rwb.case.CaseStateChanged.v1` | `rwb.case.events.v1` | P3 rwb-case | Fixes the instant a status or stage change reached the topic, so the row the list returns after it describes the same case at the same instant (DP-14) |
| `rwb.deviation.DeviationRaised.v1` | `rwb.deviation.events.v1` | S8 rwb-deviation | The raise of X1 on 9 December 2026 that pauses the stage clock of case "RW-2026-000104" and makes its row PAUSED and not BREACHED (DP-14) |
| `rwb.deviation.DeviationCleared.v1` | `rwb.deviation.events.v1` | S8 rwb-deviation | Confirms that no clearance of the case happened inside the run window, so the pause the list shows is the open deviation and not a stale flag (DP-14) |

The harness consumes with its own consumer group and never reads a producer's outbox, inbox or schema.

#### 12.5 Workflows and activities

`CaseWorkflow` on task queue `rwb-case` is observed, not built: the durable timer inside it is the clock behind the SERVICE_LEVEL and PRESCRIPTION projection the list reads, and the harness asserts that the projection and the timer agree at 09:00 and 09:01 (AC2, AC4). `DeviationWorkflow`, the child on task queue `rwb-deviation`, is observed, not built: it is the pause of the stage clock that makes the row PAUSED (AC2).

The harness starts no workflow, adds no activity and writes no schedule. The case query, the timer projection, the export and the access-log entry belong to the app stories of the seven integration dependencies.

#### 12.6 Schedules

None. The harness adds no workflow and no schedule; the fixed clock at 09:00 and 09:01 is the harness's own, and the durable timer it reads belongs to `CaseWorkflow`.

#### 12.7 Tables owned

None. The harness owns no table in any schema and no schema of its own; it reads through the operations of 12.2 and writes one access-log entry through the P4 contract.

#### 12.8 Contract fakes

| Fake | Serves | Contract | What it answers |
|---|---|---|---|
| WireMock rwb-case | The four P3 operations of 12.2 | OpenAPI of P3 | The three rows of AC1 with their ages and service-level states and the order by breach, age and case number; the four cases of AC3; the boundary reads at 09:00 and 09:01; the PAUSED case with the prescription clock and the open deviation; the empty state and the single row of AC8 and AC9; the export bytes with the header and one data row and, for AC8, the header only; the 422 refusals with MSG-GEN-007, MSG-GEN-002 and MSG-P3-021; keeps the request journal for the filter, page and ordering assertions |
| WireMock rwb-access | The three P4 operations of 12.2 | OpenAPI of P4 | The session with role RW-TEAMMGR, Team scope for "MTG-BKK" and Case record R; the role's default scope from `GET /admin/roles`; the RW-REFADM user without the right, answering 403 MSG-P4-002; the export entry with the user, the time, the 3 filters and row count 1 after the export |
| WireMock rwb-deviation | The two S8 events of 12.4 | AsyncAPI of S8 | `DeviationRaised` for X1 on 9 December 2026 and no `DeviationCleared` inside the run window for case "RW-2026-000104" |
| WireMock rwb-integration | The routed read the screen uses | OpenAPI of P2 | The routed answer the case list screen receives, so the journey runs on the same route the manager drives and not on a direct call the screen never makes |
| Fixed clock | The harness itself | None | 10 December 2026 at 09:00 and 09:01 Asia/Bangkok, the two instants the boundary and the ageing are asserted at |

Each fake is replaced by the real service as its integration dependency lands, without a change to the scenarios. Not specified in the source documents (GAP-0415; ASM-0590): the fake set, the concrete fixture values, the harness environment, the OpenXML comparison method and the evidence format.

#### 12.9 Call-type summary

| Call type | In this story |
|---|---|
| REST | 0 provided, 7 consumed, one hop on the owner's base with the 2 s timeout |
| Kafka | 3 events consumed on `rwb.case.events.v1` and `rwb.deviation.events.v1`; none published on a production topic |
| Temporal | Observed only: `CaseWorkflow` on queue `rwb-case` and its `DeviationWorkflow` child on queue `rwb-deviation`; no workflow, activity or schedule added |
| File | One Excel export, compared cell by cell against the expected columns and the row the list returned |

### 13. Solution plan

**Package.** Folder `integration/recovery-case-list` in the ACE repository, package `<ACE base package>.recovery.integration.caselist`. Not part of any deployed service.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added | How this harness applies it |
|---|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none | The case, the queue and the timer are read through the P3 operations and the access log through the P4 operation; the harness opens no connection to any schema |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON | The export limit of 10,000 rows (assumed; DL11), the page range of 1 to 200 and the service level values are seeded from the parameter catalog, never values in the harness |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON | LOV-PRODUCT, LOV-CASE-STATUS, LOV-STAGE, LOV-TIMER-STATUS and the queue codes are loaded from files, so product "CAR" is refused by the data and not by a rule in the harness |
| DP-08 | RecoveryAccessGuard | Authorise contract of rwb-access and the guard library | H RWB-PLT-E1037-CON; C RWB-P4-E1037-CON | The session, the role's default scope and the refusal of RW-REFADM are read through the P4 operations; the harness reproduces no scope rule |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none | Every path of 12.2 uses the owner's base, so the harness never calls a monolith base |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON | No legacy `rwb.p<n>.` or `rwb.casewf.` topic name survives: the harness subscribes to `rwb.case.events.v1` and `rwb.deviation.events.v1` and asserts the naming library's topic names for every event it consumes |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON | Each service migrates its own schema; the harness runs no migration, creates no view and reads no schema |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON | The journey runs through the gateway route the case list screen uses, on the same bases, composed in parallel for the composite read |

The platform H dependencies in the table (H RWB-PLT-E1042-CON, H RWB-PLT-E1043-CON, H RWB-PLT-E1037-CON, H RWB-PLT-E1047-CON, H RWB-PLT-E1044-CON, H RWB-PLT-N001-CON) are delivered by the platform waves and are not repeated in the metadata: the harness converges on them and has no build dependency of its own. The blocking dependencies of this story are the seven I stories, which replace the fakes with real services one at a time.

**Harness components**

| Component | Type | Responsibility |
|---|---|---|
| JourneyRunner | Job | Runs the twelve flow steps for one scenario and one business date, holds the run lock and drives the fixed clock |
| FakeRegistry | Configuration | WireMock mappings for rwb-case, rwb-access, rwb-deviation and rwb-integration, one set per contract version, plus the fixed clock selection |
| CaseListFixturePack | Data | The team, the two queues, the five cases and the out-of-scope case, the timers, the deviation, the export limit, the 23,600-case pack and the role and scope fixtures, per scenario |
| RowAssertion | Service | Compares the rows, their order, the ages in state, the service-level states, the prescription clock and the deviation flag against the fixture, and the three refusals of AC6, AC7 and AC9 |
| ExtractAssertion | Service | Compares the Excel file cell by cell with the expected header and data row, and asserts the header-only file of AC8 and the no-file refusal of AC10 |
| AccessLogAssertion | Service | Reads the export entry through the P4 operation and asserts the user, the time, the three filters, the row count and the entry-before-file order |
| EvidenceCollector | Service | Writes one report keyed by story key and business date, with the rows, the timers, the export cells, the access-log entry, the messages and the NFR read |
| GateEvaluator | Service | Passes the run when every owned scenario passes and the evidence pack is attached |

**Environment and test data.** SIT, the wave 2 harness profile, one business date, the fixed clock at 09:00 and 09:01, synthetic cases and synthetic roles only. The seeded values are the legacy sections 3 and 7: team "MTG-BKK" with queues "MTG-BKK-CO" and "MTG-BKK-LIT", cases "RW-2026-000101" to "RW-2026-000105", case "RW-2026-000201", deviation X1 on 9 December 2026, the export limit of 10,000 rows, the page range of 1 to 200 and the 23,600-case pack; no other value is added. Not specified in the source documents (GAP-0415; ASM-0590): the environment, the seed pack, the comparison method and the evidence format.

**Build steps**

1. Write the CaseListFixturePack with the team, the two queues, the five cases, the out-of-scope case, the timers, the deviation, the export limit and the 23,600-case pack; test that a bad seed stops the run without reporting a scenario (X10).
2. Write the FakeRegistry with the four WireMock mapping sets and the fixed clock, with the lists of values and the queue codes loaded from files.
3. Write JourneyRunner steps 1 to 5 for AC1: the session, the subscription, page 1, the columns, the three ages, the three service-level states and the order.
4. Add AC2 and AC4 with the paused case, its two clocks and the two boundary reads at 09:00 and 09:01.
5. Add AC6, AC7, AC8, AC9 and AC10 with the three filter refusals, the empty state, the scope case and the extract limit.
6. Add AC3 with the export, the cell-by-cell comparison and the access-log entry, then AC5 and AC11 with the NEW case and the two pages of 50.
7. Add the not-authorized case of TC-E2-033-12-ITG and the 23,600-case read, write EvidenceCollector and GateEvaluator, attach the report to the wave 2 release record and rerun the eleven scenarios on the release build.

**Feature switch.** `rwb.casewf.case-list-ageing` is on in the harness profile, as the legacy story sets it. Off, the breached parameter is ignored and the list and export keep the earlier columns, so the harness reports the journey as not applicable rather than as passed. The harness itself is a pipeline stage selected by the run profile, not by a business flag.

**Done when.** The tests of section 16 pass, the run report is attached to the wave 2 release record with all eleven owned scenarios, and each fake has been replaced by the real service where its I story has landed in SIT. The NFR-008 check is a read the harness measures and does not build: page 1 of the list over 23,600 synthetic cases returns in under 2 seconds at the 95th percentile in SIT. The fixture pack and the evidence sign-off wait for the values of the gap and assumption rows cited above.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-007 | A filter value is not in its list | {value} is not a valid value for {field}. |
| MSG-GEN-002 | Page size outside 1 to 200 | {field} must be between {min} and {max}. |
| MSG-P3-020 | No case matches the filters | No cases match these filters. Change a filter to see more. |
| MSG-P3-021 | Extract above the row limit | The export holds at most {max} rows. Narrow the filters and try again. |
| MSG-P4-001 | No valid session | You have no Recovery Workbench role. Ask your team manager to request one. |
| MSG-P4-002 | Role lacks Case record R | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The export access event cannot be recorded | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The harness asserts these messages and never rewrites them. Thai text for each message follows decision DL10. Its own report text is for the release team and is not part of the message standard.

### 15. Screens and states

SCR-02 Case list, states Loading, Empty, List and Filtered. The team manager sets filters for queue, product, status, stage, owner and breached; reads the columns case number, product, queue, owner, status, stage, age in state, service level state, service level due, prescription date, prescription clock and deviation; and chooses Extract. A breached row carries the text "Breached", not colour alone; a paused stage clock shows "Paused". The Empty state shows MSG-P3-020.

No screen is built by this story. The harness drives the four states and the operations behind them and asserts the same facts through the contracts: the loading page holds the row count and the order, the list state the eleven columns, the filtered state the single row and the empty state the message. The visual layout belongs to RWB-P3-E2033-APP under DL31, and the accessibility acceptance of the "Breached" and "Paused" text is Not specified in the source documents (GAP-0415; ASM-0590).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-033-12-ITG | Access | Component | RW-REFADM calls the list; refused with MSG-P4-002 |
| TC-E2-033-01-ITG | AC1, BR1, BR2, BR3 | Integration | Three cases in team MTG-BKK as in AC1 |
| TC-E2-033-02-ITG | AC2, BR4, BR5 | Integration | Case with X1 raised, paused SERVICE_LEVEL timer, running PRESCRIPTION timer |
| TC-E2-033-03-ITG | AC3, BR7 | Integration | Four cases; filters queue, product and breached; extract file and access log |
| TC-E2-033-04-ITG | AC4, BR3 | Integration | Timer due 10 December 2026 09:00, read at 09:00 and 09:01 |
| TC-E2-033-05-ITG | AC5 | Integration | NEW case with no SERVICE_LEVEL timer |
| TC-E2-033-06-ITG | AC6, BR6 | Integration | Product filter CAR |
| TC-E2-033-07-ITG | AC7 | Integration | Page size 500 |
| TC-E2-033-08-ITG | AC8 | Integration | Filter product SSME with no SSME case |
| TC-E2-033-09-ITG | AC9, BR1 | Integration | Case in team HP-NE read by the MTG-BKK manager |
| TC-E2-033-10-ITG | AC10, BR7 | Integration | 10,001 matching cases |
| TC-E2-033-11-ITG | AC11 | Integration | 120 cases with equal age, pages of 50 |

Each `-ITG` case is the journey copy of the legacy case: the Given, When and Then are those of the legacy story's case, run across the four contracts and the gateway route. The app stories keep the unit and component copies of the same cases; TC-E2-033-12-ITG stays a component assertion because it tests the refusal and not a journey.

### 17. Guardrails

- No business value in code: the page limits, the export limit, the lists of values, the queue codes and the service level values are parameter or reference data in the seed pack, never values in the harness.
- No personal data in the export sample, the events, the workflow inputs, the logs or the evidence: the seed holds synthetic cases and synthetic roles only, and the extract carries no customer field.
- No read of another service's tables and no schema of the harness's own: the list is read through the P3 contract and the access log through the P4 contract, and the harness runs no migration.
- The breach flag is computed at read time by rwb-case; the harness never changes a timer, a case or a deviation, and asserts that neither the boundary read nor the extract moved one.
- Each fake is replaced by the real service as its I story lands; a fake that outlives its service is a defect, not a configuration.
- The harness never runs against UAT or production, and a value that must change changes in the seed pack through a reviewed change, never by an exception in a scenario.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-WKM-002 | Team manager sees every team queue, filters by status, product and ageing, exports the view | Business Requirements Epic 2 v2, section 3.2 | None | All recovery processes | R-UNI-30 | TC-E2-033-01-ITG, TC-E2-033-03-ITG to TC-E2-033-12-ITG |
| REQ-DVH-006 | Deviation flag visible in every queue view | Business Requirements Epic 2 v2, section 3.2 | None | All recovery processes | R-DEV-01 | TC-E2-033-02-ITG |
| REQ-ACA-006 | Every read of the case store is written to the access log | Business Requirements Program v4, section 5.4 | None | All recovery processes | None | TC-E2-033-03-ITG |

### 19. Out of scope

- Next action columns and the overdue mark: RWB-E2-035.
- My queue and team queue screens with counts, oldest case and cap use: RWB-E2-011.
- Escalation when a service level is breached: RWB-E1-028 and RWB-E2-015.
- Manual transfer from the list: RWB-E2-012.
- The service level values per state: DL22.
- Production code of any service in the journey: the operations of rwb-case, rwb-access, rwb-deviation and rwb-integration, their schemas and their screens belong to their own stories.

The harness, the fakes and the evidence pack cover the six items above only as a caller or a consumer would see them; building any of them is out of scope for this story.
