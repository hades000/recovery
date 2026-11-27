# RWB-P3-E2033-APP Case and queue list with status, owner and ageing

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P3-E2033-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-case |
| Service epic | RWB-SVC-P3 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-033 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP06, DP07, DP08, DP13, DP14, DP15, DP19 |
| Parallel lane | L-P3-AK |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P2-E2033-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P3 rwb-case v1.md (FR-P3-014, FR-P3-016, FR-P3-019, FR-P3-021, FR-P3-022) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-033 for rwb-case. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P3-E2033-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **team manager (RW-TEAMMGR)**, I want **the case and queue list served by rwb-case from its own `rwb_case` rows, each row carrying the case number, the product group, the queue, the owner, the status, the stage, the age in state in days, the age since entry, the service level state and due time, the prescription date and the prescription clock, with the filters checked against the lists in force, the page bounds and the extract row limit read as parameter rows, a stable order, and a drill down from a queue**, so that **every case in every queue in my scope is on one list I can trust without asking anyone, and the age I read is the age of the owner's own row**.

This is the case-list slice of legacy RWB-E2-033. Inside `rwb-case` it is served on the service's own base `/api/recovery/case/v1`, from schema `rwb_case`, Java package `th.co.scb.ace.workbench.recovery.case`, topic `rwb.case.events.v1` and task queue `rwb-case` in namespace `rwb-recovery`.

- The legacy story extended the monolith's `GET monolith-base/cases`, its export and `CaseListQueryService`, `PrescriptionClockReader`, `AgeingCalculator` and `CaseExportService`, reading `recovery_case`, `queue` and `timer` in the shared recovery schema. Those tables are rwb-case's own (DP-01), so this slice is the owner's read of them with no contract between the service and its tables.
- The composed screen and the workbook on the integration base are RWB-P2-E2033-APP's and read this service through RWB-P2-E2033-CON; the rights, the scope rows and the access log are rwb-access's (DP-08); the deviation record behind the open flag is rwb-deviation's; the end-to-end journey is RWB-ITG-E2033-ITG. The list served here and the list composed there are the same facts twice, which is the stated cost of the split (GAP-2224; ASM-3661).
- The export itself — the workbook, its columns and the access-log entry that precedes it — is RWB-P3-E1031-APP, which owns that operation of this base. This slice owns the one invariant the legacy story added to it: at most `caselist.export.maxrows` rows, refused before anything is written (BR11). The queue summary counts, the cap use and the queue screens are RWB-P3-E2011-APP's, whose `ageDays` and page-size rows this slice re-uses and does not redefine.
- The rights are the legacy ones: `RW-TEAMMGR` with Team scope, `RW-CASEOWN` with Own scope, `RW-PRODHEAD`, `RW-AUDIT` and `RW-CONDUCT` in their scope, and a role with no Case record right refused with MSG-P4-002.

This secondary slice owns no legacy acceptance criterion: legacy AC1 to AC11 are carried by RWB-P2-E2033-APP, and the legacy test set TC-E2-033-01 to TC-E2-033-12 is kept here against this slice's own assertions, so the values the legacy story fixed are proved on the owner's rows as well as on the composed page.

The slice writes no business row: it reads `recovery_case`, `queue` and `timer` in `rwb_case`, computes the ages and the service level state at read time, publishes no event, starts no workflow, creates no Schedule and holds no foreign key to another service (DP-01).

### 2. Business rationale

A team manager today learns where cases wait by asking each owner or by building a spreadsheet. The legacy story completed the case list for every queue in the manager's scope — a breach filter, the prescription clock beside the stage clock so a paused case is not read as safe, and the same columns in the extract — and met REQ-WKM-002 (every queue in the team, filtered by status, product and ageing, with an export), REQ-DVH-006 (the deviation flag in every queue view) and REQ-ACA-006 (a read of the case store is written to the access log). The business measure is the count of cases past their service level per queue, read every morning.

In the target the facts stay where they are and the read moves with them. The case, the queue and the timer are rwb-case's, so the list is served by the owner of the rows: one query, one transaction, the same filter set and the same order for the page and for the limit check that guards the extract. A reader cannot be told a different age by a service that copied the case.

With about 23,600 open cases at go-live and 26,500 at the end of 2027 (NFR-001) and about 370 staff online in the busiest hour (NFR-002), this is the largest read in the Workbench and it has to stay inside the 2 s target of NFR-008. The mechanism is unchanged: one indexed query, the open timers joined once per page, the ages computed in the service, and the bounds read as parameter rows so a limit change is a data change.

Three rules do the visible work. The age in state is what the case has waited where it stands, not the age of the case (BR2), so a case that has just moved must not read as months old. A deviation pauses the stage clock and never the prescription clock (BR4), which is the failure the legacy story was written to prevent. The order ends on the case number (BR10), so pagination can neither repeat nor skip a case.

The scope is not a filter this service owns: it is the answer of the rwb-access authorise contract, cached per request, and a role without the right is refused rather than shown an empty page (BR1).

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-P2-E2033-CON is published and baselined | The contract baseline this slice is tested against: the page envelope, the row shape, the filter set, the problem bodies and the fakes. It is a contract dependency and never blocks the build |
| RWB-P3-E1019-APP is done | Queues carry their code, team and role, so a queue filter resolves against a row in force |
| RWB-P3-E1020-APP is done | New cases carry a queue and an owner by rule, so an unassigned case is the exception it should be |
| RWB-P3-E1028-APP is done | Each assigned case carries a SERVICE_LEVEL timer with `status`, `paused` and `expires_at` and, where the legal period applies, a PRESCRIPTION timer; this slice reads those rows and writes none |
| RWB-P3-E1031-APP and RWB-P3-E1031-CON are published | The export operation of this base exists, so the row-limit check has an operation to guard and the legacy extract columns keep one owner |
| RWB-P3-E2011-APP is done for the queue views | Its `ageDays`, its service level state and its page-size parameter rows are carried unchanged; this story adds the age in state beside them and declares no second pair of bounds |
| The parameters in force hold the bounds and the row limit | The case-list page-size minimum 1 and maximum 200 served by RWB-P3-E2011-APP and `caselist.export.maxrows` 10,000 (assumed in the legacy story, DL11), as rows of `parameter_value` with the version in force (DP-06; GAP-2224; ASM-3663) |
| The reference data in force holds the lists | LOV-PRODUCT, LOV-CASE-STATUS and LOV-STAGE as rows of `reference_row` with the version in force, read in process through the rwb-case reference-data contract (DP-07) |
| The role to permission matrix gives RW-TEAMMGR Case record R with Team scope | The caller signs in through Entra ID with a role holding Case record R; the right, the scope and its default are answered by rwb-access and cached per request by the guard library (DP-08) |
| The feature switch `rwb.casewf.case-list-ageing` is on | Off, the breach filter is ignored and the list keeps the columns of RWB-P3-E2011-APP and RWB-P3-E1031-APP; the switch's mechanism and owner are Not specified in the source documents (GAP-2224; ASM-3666) |
| The platform contracts the DP rows name are published | RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1037-CON, RWB-PLT-E1047-CON, RWB-PLT-E1044-CON and RWB-PLT-N001-CON. They are pulled by the rwb-case baseline stories, so this slice adds no build dependency and starts on Day 1 |
| The connection is the rwb-case login (DP-02) | Not specified in the source documents (GAP-2224; ASM-3666) |

### 4. Flow

1. Team manager: opens SCR-02 Case list through the gateway-bff composite route (DP-19) and chooses the filters queue, product, status, stage, owner and breached.
2. gateway-bff: calls `GET /api/recovery/case/v1/cases` on rwb-case, one hop, and merges the answer into the screen model.
3. rwb-case: `AccessCheckClient` asks the rwb-access authorise contract for Case record R and the caller's scope, cached for the request; a role without the right is a 403 and nothing is read (DP-08, BR1).
4. `FilterValidator` checks each filter value against the list in force for its field and a queue filter against the queue codes in force; a value outside its list is a 422 before any case is read (BR6).
5. `PageBoundsReader` reads the page-size minimum and maximum through the parameters contract with the version in force and refuses a size outside them with 422 (BR7).
6. `CaseListQueryService` builds one query over `rwb_case`: `recovery_case` filtered by the request and by the scope predicate, `queue` joined for the queue code and its team, and the open SERVICE_LEVEL and PRESCRIPTION `timer` rows of each case joined once for the page (BR8).
7. `AgeingCalculator` computes `ageInStateDays` from `stage_clock_start`, or from `entry_date` when it is empty, and `ageSinceEntryDays` from `entry_date`, both as whole calendar days to the reference day in Asia/Bangkok (BR2).
8. `ServiceLevelStateReader` resolves the service level state: EXPIRED, or RUNNING past `expires_at`, is BREACHED; a paused timer is PAUSED; a RUNNING timer inside its due time is RUNNING; no timer is NONE; a paused timer is never breached (BR3, BR4, BR5).
9. `PrescriptionClockReader` resolves `prescriptionDate` from the case row and `prescriptionClockStatus` from the PRESCRIPTION timer, NONE when there is none; `deviationOpen` is read from `recovery_case.deviation_open` and nothing else about the deviation is read (BR5, BR12).
10. `CaseListQueryService` orders the rows breach first, then age in state descending, then case number ascending, and returns one page with its envelope (BR10).
11. Team manager: selects a queue on the queue screen; the front end calls `GET /api/recovery/case/v1/queues/{queueId}/cases`, which applies the same scope, row shape, order and bounds to one queue and answers 404 for a queue outside the caller's teams.
12. Team manager: chooses Extract; the front end calls the export operation of this base with the same filters and without page and size; RWB-P3-E1031-APP re-reads with those filters, and this slice's limit check refuses with 422 when the matching rows exceed `caselist.export.maxrows`, before any file or access-log entry is built (BR11).
13. Nothing in steps 1 to 12 writes a case, a queue or a timer, publishes an event, adds an outbox row or starts a workflow: the operations are reads and the limit check is a refusal (BR9).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A filter value is not in its list of values, for example product CAR | Refused with 422; nothing is read | MSG-GEN-007 | AC3 |
| X2 | Page size below 1 or above 200 as the rows in force state them | Refused with 422 | MSG-GEN-002 | AC4 |
| X3 | No case matches the filters | Empty state on the list; the extract of RWB-P3-E1031-APP holds the header row only | MSG-P3-020 | AC6 |
| X4 | A queue filter names a queue outside the caller's scope | Only cases in scope are returned, so the result is empty | MSG-P3-020 | AC7 |
| X5 | A case has no SERVICE_LEVEL timer yet (status NEW) | Service level state NONE; breached false | None | AC1 |
| X6 | The service level due time equals the current time | Not breached; breached from the next minute | None | AC5 |
| X7 | The extract would hold more than `caselist.export.maxrows` rows | The extract is refused before anything is written and no file is produced | MSG-P3-021 | AC9 |
| X8 | A case changes between two page requests | The order ends on the case number, so no case is skipped or repeated by the order | None | AC10 |
| X9 | The caller's role does not hold the Case record right | Refused with 403 before any row is read; a refusal and never an empty page | MSG-P4-002 | AC7 |
| X10 | The rwb-access authorise contract does not answer inside the 2 s budget | One hop, 2 s timeout and a breaker; 503, and no page is served from a stale right cache | MSG-GEN-006 | AC7 |
| X11 | A queue id in the drill down is unknown or outside the caller's teams | Not found; nothing is read | MSG-P4-003 | AC8 |

X9 and X11 are the two refusals this slice must not turn into an empty answer: a consumer that reads an empty page as "no work" hides a permission problem, which is why the two are distinguished by status and not by body. X10 is the platform unavailable message.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Reads rows that RWB-P3-E1019-APP, RWB-P3-E1020-APP and RWB-P3-E1028-APP already write, and builds against RWB-P2-E2033-CON and its fake plus the rwb-access fake, so neither rwb-access nor the edge is needed in the development environment |
| Negotiable | The row fields are the legacy columns and the layout belongs to the designer (DL31); the order, the bounds, the row limit and the refusals are fixed |
| Valuable | Puts every case of every queue in the manager's scope on the owner's own list, with the age in state beside the age since entry and the prescription clock beside the service level state |
| Estimable | Two read operations, one query, one calculator, one state reader, one validator, one bounds reader and one page of screen support |
| Small | Reads only: no business row, no outbox row, no event, no workflow and no Schedule |
| Testable | Each criterion is one automated test; the access case and the drill down are component tests, and the boundary of the service level is a unit test on the calculator |

### 7. Acceptance criteria

```gherkin
Feature: Case and queue list with status, owner and ageing

  Background:
    Given today is 10 December 2026 at 09:00 Asia/Bangkok
    Given the team manager holds role RW-TEAMMGR with Team scope for team "MTG-BKK"
    Given queue "MTG-BKK-CO" belongs to team "MTG-BKK" and role RW-CASEOWN
    Given queue "MTG-BKK-LIT" belongs to team "MTG-BKK" and role RW-LITOFF
    Given the rwb-access contract mock returns role "RW-TEAMMGR" with the Case record right "R" and scope "Team" for team "MTG-BKK"
    Given the reference data in force holds LOV-PRODUCT, LOV-CASE-STATUS and LOV-STAGE
    Given the parameter rows in force hold the case-list page size minimum 1, the case-list page size maximum 200 and caselist.export.maxrows 10,000

  Scenario: AC1 The row carries the case, the queue, the owner, the status and the clocks (new, D-RCV-60)
    Given case "RW-2026-000101", product MORTGAGE, queue "MTG-BKK-CO", owner "U-1001", status ASSIGNED, stage clock start 1 December 2026, service level due 8 December 2026 17:00
    Given case "RW-2026-000102", product MORTGAGE, queue "MTG-BKK-LIT", owner "U-1002", status IN_PROGRESS, stage clock start 8 December 2026, service level due 15 December 2026 17:00
    Given case "RW-2026-000103", product MORTGAGE, queue "MTG-BKK-CO", no owner, status NEW, entry date 10 December 2026
    When the manager opens the list
    Then 3 rows show
    Then row "RW-2026-000101" shows product MORTGAGE, queue "MTG-BKK-CO", owner "U-1001", status ASSIGNED, age in state 9 days and service level state BREACHED
    Then row "RW-2026-000102" shows queue "MTG-BKK-LIT", owner "U-1002", status IN_PROGRESS, age in state 2 days and service level state RUNNING
    Then row "RW-2026-000103" shows owner "Unassigned", status NEW, age in state 0 days and service level state NONE
    Then the rows are in the order "RW-2026-000101", "RW-2026-000102", "RW-2026-000103"
    Then no row carries a customer name, an identity number or an account number

  Scenario: AC2 A paused clock is never breached and the prescription clock keeps running (new, D-RCV-60)
    Given case "RW-2026-000104" with deviation X1 raised on 9 December 2026
    Given its SERVICE_LEVEL timer has paused true and status PAUSED
    Given its PRESCRIPTION timer has status RUNNING and expires 30 June 2028
    Given case "RW-2026-000106", product MORTGAGE, queue "MTG-BKK-CO", owner "U-1003", status NEW, no stage clock start, entry date 2 December 2026
    When the list is read
    Then row "RW-2026-000104" shows service level state PAUSED, prescription clock RUNNING with date 30 June 2028 and deviation open Yes
    Then the system does not count case "RW-2026-000104" as breached, and the breached filter excludes it
    Then row "RW-2026-000106" shows age in state 8 days from its entry date, because its stage clock has not started

  Scenario: AC3 A filter value outside its list is refused (new, D-RCV-60)
    When the manager requests the list with product "CAR"
    Then the response is 422 with message MSG-GEN-007 naming the value "CAR" and the field product
    Then the system reads no case and writes no row
    Then a request with status "PENDING" is refused the same way, because that value is not in LOV-CASE-STATUS in force

  Scenario: AC4 The page-size bounds are parameter rows (new, D-RCV-60)
    When the manager requests the list with page size 500
    Then the response is 422 with message MSG-GEN-002 naming page size, minimum 1 and maximum 200
    Then when the case-list page size maximum row in force holds 100, a request with page size 500 is refused with those values and a request with page size 100 is served
    Then no bound is written in code: the same answer follows a restart with the new row in force

  Scenario: AC5 The breach boundary of the service level (new, D-RCV-60)
    Given case "RW-2026-000105" with a RUNNING SERVICE_LEVEL timer due 10 December 2026 09:00
    When the list is read at 10 December 2026 09:00
    Then row "RW-2026-000105" shows service level state RUNNING
    Then when the list is read again at 10 December 2026 09:01, row "RW-2026-000105" shows service level state BREACHED
    Then the case is not moved and no timer row is rewritten by either read

  Scenario: AC6 No case matches the filters (new, D-RCV-60)
    When the manager filters by product SSME and no SSME case is in scope
    Then the list shows the empty state with message MSG-P3-020
    Then the answer is an empty page and not a refusal
    Then the same filters on the export operation of this base produce the header row only

  Scenario: AC7 The scope comes from the authorise answer (new, D-RCV-60)
    Given case "RW-2026-000201" in queue "HP-NE-CO" of team "HP-NE"
    Given the rwb-access contract mock returns scope "Team" for team "MTG-BKK" and no scope over team "HP-NE"
    When the manager of team "MTG-BKK" filters by queue "HP-NE-CO"
    Then the list shows the empty state with message MSG-P3-020
    Then case "RW-2026-000201" does not appear in any page of the unfiltered list
    Then a caller whose role holds no Case record right is refused with 403 and MSG-P4-002 before any row is read

  Scenario: AC8 The queue drill down answers the same row (new, D-RCV-60)
    Given queue "MTG-BKK-CO" holds case "RW-2026-000101" and case "RW-2026-000103"
    Given queue "SME-NTH-CO" belongs to team "SME-NTH" and the rwb-access contract mock returns no scope over team "SME-NTH"
    When the manager requests GET /api/recovery/case/v1/queues/{queueId}/cases for queue "MTG-BKK-CO"
    Then 2 rows show with the row shape, the ages, the service level state and the order of the case list
    Then the page-size bounds and the filter checks of the case list apply unchanged
    Then a request for queue "SME-NTH-CO" answers 404 with MSG-P4-003 and reads no case

  Scenario: AC9 The extract limit (new, D-RCV-60)
    Given 10,001 cases in the manager's scope match breached No
    Given the parameter row caselist.export.maxrows in force holds 10,000
    When the manager chooses Extract with breached No
    Then the response is 422 with message MSG-P3-021 naming 10,000 rows
    Then the system produces no file and no access-log entry is written, because the refusal comes first
    Then when caselist.export.maxrows in force holds 20,000 the same request passes the check and the file is the export story's

  Scenario: AC10 Order is stable across pages (new, D-RCV-60)
    Given 120 cases in scope with no breach and the same age in state
    When the manager reads page 1 and page 2 with page size 50
    Then page 1 holds the 50 lowest case numbers and page 2 the next 50
    Then no case appears on both pages
    Then the order ends on the case number and never on a row number, so a case that changes between the two requests is not read twice
```

The ten criteria are this slice's own; legacy AC1 to AC11 are carried by RWB-P2-E2033-APP, and the legacy test set is kept in section 16. Every legacy value is kept character for character: the three cases of legacy AC1 with their owners, statuses, stage clock starts and service levels, their order, the paused timer and the running prescription clock of legacy AC2, the due time of legacy AC4, product CAR of legacy AC6, page size 500 and the bounds 1 and 200 of legacy AC7, product SSME of legacy AC8, the team HP-NE case of legacy AC9, the 10,000-row limit of legacy AC10 and the 120 cases with pages of 50 of legacy AC11.

Where a criterion needs another service the `Given` names the contract mock: the rwb-access authorise answer (AC7, AC8) is the only cross-service answer this slice takes. The reference and parameter rows are this service's own data and are seeded, not stubbed (DP-06, DP-07). Two readings had to be fixed and are recorded: the legacy `ageDays` is the legacy age in state, while RWB-P3-E2011-APP publishes `ageDays` as the age since entry, so this story keeps `ageDays` as the queue views publish it and adds `ageInStateDays` for the legacy column (GAP-2224; ASM-3664); an unassigned case is answered with no owner value and shown as the text "Unassigned", as the legacy criteria read the cell (GAP-2224; ASM-3664).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The list holds only cases in the caller's scope — Own, Team or All — taken from the rwb-access authorise contract; a role without the Case record right is refused and never given an empty page | CTL-09; `role.default_scope`; DP-08 |
| BR2 | Age in state is the whole number of calendar days from `stage_clock_start`, or from `entry_date` when it is empty, to the reference day in Asia/Bangkok; age since entry is the whole number of calendar days from `entry_date` to the same day | DF-CAS-018, DF-CAS-013; legacy BR2; GAP-2224; ASM-3664 |
| BR3 | A case is breached when its SERVICE_LEVEL timer has status EXPIRED, or status RUNNING with `expires_at` earlier than now; a breach does not move the case | R-UNI-30; DF-WRK-032, DF-WRK-035 |
| BR4 | A deviation pauses the stage clock and keeps the prescription clock running; the list shows both; a paused SERVICE_LEVEL timer is never breached | R-DEV-01; DF-WRK-034, DF-WRK-035 |
| BR5 | `serviceLevelState` is BREACHED, RUNNING, PAUSED or NONE from the SERVICE_LEVEL timer; `prescriptionClockStatus` is RUNNING or EXPIRED from the PRESCRIPTION timer and NONE when the case has no such timer; `prescriptionDate` is read from the case row | LOV-TIMER; LOV-TIMER-STATUS; DF-CAS-017; legacy BR5 |
| BR6 | Each filter value is checked against the list in force for its field — LOV-PRODUCT, LOV-CASE-STATUS, LOV-STAGE — and a queue filter against the queue codes in force; a value outside its list is refused before any case is read | DP-07; `queue.queue_code`; legacy BR6 |
| BR7 | No value is written in code: the page-size bounds are the parameter rows RWB-P3-E2011-APP fixes, the extract row limit is `caselist.export.maxrows` 10,000 (assumed, DL11), and every list is a reference row read with the version in force | DP-06; DP-07; GAP-2224; ASM-3663 |
| BR8 | The read holds only `rwb_case` rows — `recovery_case`, `queue` and `timer` — and no other service's table, view or row is read, joined or copied | DP-01; ADR-010 |
| BR9 | The operations are read-only: no business row, no outbox row, no event, no workflow and no Schedule; a refusal writes nothing | Template and Rules §R7.2 s17 |
| BR10 | The order is breach first, then age in state descending, then case number ascending, so the order is total and a case that changes between two requests is never skipped or repeated | Legacy flow step 7; legacy AC11 |
| BR11 | The extract holds at most `caselist.export.maxrows` rows, carries no customer personal field, and a request above the limit is refused with 422 before the access-log entry and before any file is built | REQ-ACA-006; legacy BR7; FSD P3 A2.19 AC-EXC-P3-019-02; RWB-P3-E1031-APP |
| BR12 | `deviationOpen` is read from `recovery_case.deviation_open` and names only that a deviation is open; the deviation record, its code, its owner and its clearance are rwb-deviation's | REQ-DVH-006; DF-CAS-019; R-DEV-01 |

How the rules hold in `rwb-case`: BR1 is one authorise call cached for the request, applied as a predicate and not as a filter over the answer, so no page can carry a row from outside the scope. BR2 is `AgeingCalculator`, a pure function over two dates and a reference day passed in, unit tested without a database. BR3 to BR5 are one read of the two timer types per page and one resolver per row, with the paused test ahead of the breach test so the order of the two tests cannot decide a breach. BR6 and BR7 are `FilterValidator` and `PageBoundsReader`; no list value and no limit is a constant, so removing a value from the reference data removes it from the accepted filters with no release. BR8 is the repository, and an architecture test fails a statement that names another schema. BR9 is the absence of a write path. BR10 is the SQL order clause with the tie break on `case_no`, whose uniqueness is fixed at creation. BR11 is a count with the page's own filters and scope, taken before the export writer starts, so the count and the file cannot disagree. BR12 is one boolean column; this service holds no deviation table.

### 9. State transitions

None. This story does not change a case status and does not move a case. It reads `recovery_case`, `queue` and `timer` in `rwb_case` and writes nothing: the export it guards is RWB-P3-E1031-APP's and the access-log entry is rwb-access's.

| Observed fact on the list | Written by | Appears as |
|---|---|---|
| Case number, product group, queue, owner, status, stage, entry date, prescription date and the open deviation flag | rwb-case (P3), the Epic 1 and Epic 2 stories of this service | The row of the page |
| Stage clock start and the SERVICE_LEVEL and PRESCRIPTION timers with their status, pause flag and due time | rwb-case (P3), RWB-P3-E1028-APP | `ageInStateDays`, `ageSinceEntryDays`, `serviceLevelState`, `serviceLevelDueAt`, `prescriptionClockStatus` |
| The Case record right and the caller's scope | rwb-access (P4) through the authorise contract | Whether a page is answered, and which rows |
| The queue code, its team and its role | rwb-case (P3), RWB-P3-E1019-APP | The queue filter values and the drill down |
| The page-size bounds and the extract row limit | rwb-case (P3), the parameter rows of DP-06 | Whether a request is served or refused |

A case that changes between two page requests changes the next answer and nothing else: no row is rewritten, no timer is recomputed, and the order is total by case number.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-TEAMMGR, team manager | Reads the list and the drill down for the team's queues (Case record R, Team scope); the extract file is RWB-P3-E1031-APP's |
| RW-CASEOWN, case owner | Reads the list for the cases they own (Case record R, Own scope) |
| RW-PRODHEAD, RW-AUDIT, RW-CONDUCT and other roles with Case record R | Read the list in their scope |
| RW-CAPACITY, capacity and workforce planner | Reads with scope All through the queue views of RWB-P3-E2011-APP; the scope is rwb-access's answer, not this story's |
| RW-REFADM, reference data administrator | No Case record right; refused with MSG-P4-002 |
| rwb-access, through its contract | Answers the right, the scope and its default; owns the role, permission and masking rows and the access log, none of which this story owns |
| No approval applies | The story takes no decision |

The service runs as the rwb-case login (DP-02); the name is Not specified in the source documents (GAP-2224; ASM-3666), and it holds grants on `rwb_case` only.

### 11. Data

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
| DF-WRK-001 | queue | id | Read |
| DF-WRK-002 | queue | queue_code | Read |
| DF-WRK-004 | queue | team_code | Read |
| DF-WRK-028 | timer | case_id | Read |
| DF-WRK-030 | timer | timer_type | Read |
| DF-WRK-032 | timer | expires_at | Read |
| DF-WRK-034 | timer | paused | Read |
| DF-WRK-035 | timer | status | Read |
| Not specified in the source documents (GAP-2224; ASM-3663) | parameter_catalog, parameter_value | the case-list page-size bounds and `caselist.export.maxrows`, with the version in force | Read, in process through the rwb-case parameters contract |
| Not specified in the source documents (GAP-2224; ASM-3663) | reference_row, reference_version | LOV-PRODUCT, LOV-CASE-STATUS and LOV-STAGE rows with the version in force | Read, in process through the rwb-case reference-data contract |

Field IDs are those of the Logical Data Model and Data Dictionary. Every row is a `rwb_case` row: the parameters and the reference rows are read through the contracts of this same service and never joined in SQL, and no other schema is named by any statement (BR8). No row is written, so no field is marked Write.

### 12. Contract

#### 12.1 REST operations provided

Base `/api/recovery/case/v1`; owner rwb-case (P3).

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| GET | `/cases` | One page of the cases in the caller's scope with the columns of the legacy list — case number, product group, queue, owner, status, stage, age in state, service level state, service level due, prescription date, prescription clock and deviation — with the age since entry beside the age in state, the filter set, the breach filter, the stable order and the paging envelope | Case record R, scope applied through the rwb-access authorise contract | Read only: the same request on unchanged data returns the same rows in the same order |
| GET | `/queues/{queueId}/cases` | The same row shape and order for one queue, as the drill down from a queue row; 404 for a queue outside the caller's teams | Queue and allocation R and Case record R, scope applied | Read only, as above |
| GET | `/cases/export` | The export operation of RWB-P3-E1031-APP re-read with the same filters without page and size; this story adds no column and no file, only the row-limit check refused with 422 MSG-P3-021 before the access-log entry and the file | Case record R, scope applied | Read only on the data; each export records its own access-log entry, which is rwb-access's row |

The query parameters are `product`, `stage`, `status`, `owner`, `queue`, `deviation`, `ageFrom`, `ageTo`, `page`, `size`, `sort`, with `breached` added by the legacy story. The route filter and the queue default sort are RWB-P3-E2011-APP's and are served unchanged; this story adds no filter and no sort token.

Each row carries `caseNo`, `productGroup`, `queueCode`, `ownerUserId` (absent when the case has no owner and shown as the text "Unassigned"), `status`, `stageCode`, `ageInStateDays`, `ageDays` (the age since entry, published by RWB-P3-E2011-APP), `entryDate`, `prescriptionDate`, `serviceLevelDueAt`, `serviceLevelState` (BREACHED, RUNNING, PAUSED or NONE), `prescriptionClockStatus` (RUNNING, EXPIRED or NONE) and `deviationOpen`. The names `ageDays`, `serviceLevelDueAt`, `serviceLevelState` and `prescriptionClockStatus` are the ones the legacy story and RWB-E2-011 fixed; the spelling of the other elements, of the envelope, of the filter set and of the problem body is Not specified in the source documents (GAP-2224; ASM-3662).

Errors: 401 no session or no Recovery role (MSG-P4-001); 403 no Case record right (MSG-P4-002); 404 queue unknown or outside the caller's teams (MSG-P4-003); 422 a filter value outside its list (MSG-GEN-007), a page size outside its bounds (MSG-GEN-002) or an extract above its row limit (MSG-P3-021); 503 the store is down or the authorise contract does not answer inside its budget (MSG-GEN-006).

#### 12.2 REST operations consumed

One hop, no chaining; 2 s timeout and a breaker (ADR-020).

| Method | Path | Service | Used for | Timeout |
|---|---|---|---|---|
| POST | `/api/recovery/access/v1/authorise` | rwb-access (P4) | The Case record right, the Queue and allocation right where the drill down needs it, and the caller's scope with its default, cached per request by the guard library (DP-08) | One hop, 2 s, cached per request |

The parameter and reference rows are read in process through RWB-P3-E1042-CON and RWB-P3-E1043-CON: library reads of this same service, not cross-service calls (DP-06, DP-07). The freshness header and the account columns of the legacy screen are RWB-P3-E2011-APP's and RWB-P2-E2033-APP's, so a page here carries no second downstream.

#### 12.3 Events published

None. The list and the drill down publish no event and write no outbox row. The topic `rwb.case.events.v1` with the names `rwb.case.CaseCreated.v1`, `rwb.case.CaseAllocated.v1`, `rwb.case.CaseTransferred.v1`, `rwb.case.CaseStateChanged.v1` and `rwb.case.TimerBreached.v1` belongs to the case, allocation, transfer, state and timer stories under DP-14; this slice subscribes to none of them and adds none.

#### 12.4 Events consumed

None. The list is read from the rows per request, so a change is seen on the next read rather than through a projection, and no inbox row is written. `rwb.deviation.DeviationRaised.v1` and `rwb.deviation.DeviationCleared.v1` are consumed by RWB-P3-E1028-APP to pause and resume the timer this slice renders; that is not this slice's subscription.

#### 12.5 Workflows and activities

None. The page and the drill down are served inside the request: no workflow, no activity, no signal and no timer. The durable service level and prescription timers live in `CaseWorkflow` on task queue `rwb-case`, owned by RWB-P3-E1028-APP; this slice reads their projection in `timer` and adds nothing to it.

#### 12.6 Schedules

None. The legacy story had no job and the target adds none: the list is read on request and the extract is officer-driven. The daily rebalancing Schedule and the queue measure snapshot belong to RWB-P3-E1030-APP.

#### 12.7 Tables owned

| Table | Schema | Owner | Use in this story |
|---|---|---|---|
| `recovery_case` | rwb_case | rwb-case (P3) | The case row behind every list row: number, product group, status, stage, owner, queue, team, entry date, prescription date, stage clock start and the open deviation flag |
| `queue` | rwb_case | rwb-case (P3) | The queue code and team of the queue column, of the queue filter values and of the drill down |
| `timer` | rwb_case | rwb-case (P3) | The open SERVICE_LEVEL and PRESCRIPTION timer of a case: type, due time, pause flag and status |
| `parameter_catalog`, `parameter_value`, `reference_row`, `reference_version` | rwb_case | rwb-case (P3) | The page-size bounds, the extract row limit and the filter lists, read through this service's contracts and never joined in SQL |
| `outbox_event`, `processed_event`, `idempotency_key` | PLT library, created in rwb_case | Platform library | Not written by this read path |

No other table is named. `case_list_row` is rwb-source-data's daily projection and is not read here: the API and the screen are P3's, which is the R-PREC default ruling read as the API and not as the row table. `case_account`, `case_party`, `assignment`, `queue_member` and `queue_measure` are this service's and are not read either.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-access WireMock | The P4 contract of DP-08 | `POST /authorise` granting Case record R with scope Team for `MTG-BKK`; refusing a role with no Case record right with MSG-P4-002; granting scope over `MTG-BKK` and none over `HP-NE` and `SME-NTH`; a delayed answer beyond 2 s for X10 |
| gateway-bff composite route stub | The edge route of RWB-PLT-N001-CON | The SCR-02 route and the merged screen model (DP-19), so the page's own calls can be asserted |
| Parameter and reference fixtures | This story's own test data | Page-size minimum 1, maximum 200 and `caselist.export.maxrows` 10,000 in force, a later maximum of 100 and a row limit of 20,000; LOV-PRODUCT without `CAR`; LOV-CASE-STATUS without `PENDING` |
| rwb-case seed set | This story's own test data | Cases `RW-2026-000101` to `RW-2026-000106`, `RW-2026-000201`, 120 cases of equal age and 10,001 cases for the limit |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 3 provided (2 own and the export the limit guards), 1 consumed | The case list, the queue drill down and the export of RWB-P3-E1031-APP provided; the rwb-access authorise check consumed; one hop, 2 s, breaker, cache per request |
| Kafka | None | No event published and none consumed (12.3, 12.4) |
| Temporal | None | No workflow and no activity (12.5); the timers read here are `CaseWorkflow`'s projection |
| File | None written | The workbook is RWB-P3-E1031-APP's; this story only refuses a request above the row limit |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.case`, module `caselist`; front end `src/modules/recovery/case/caselist/CaseListPage.tsx`.

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_case`; the page reads `recovery_case`, `queue` and `timer` of this service only | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and its client library: the page bounds and `caselist.export.maxrows` are parameter rows | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case: LOV-PRODUCT, LOV-CASE-STATUS and LOV-STAGE with the version in force | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-08 | RecoveryAccessGuard | Authorise contract of rwb-access and the guard library, cached per request, on both operations and on the limit check | H RWB-PLT-E1037-CON; C RWB-P4-E1037-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/case/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.case.events.v1` and `rwb.case.<Event>.v1` through the naming library; no event and no topic is added here | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in `rwb_case`: no new migration, because the timer index the legacy story asked for is the one RWB-P3-E2011-APP lands | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route for the case list and the queue drill down | H RWB-PLT-N001-CON |

DP-01 is the read of the three tables; DP-06 the two parameter reads of AC4 and AC9; DP-07 the three lists of AC3; DP-08 the authorise answer of AC7 and AC8; DP-13 the base path; DP-19 the composite route. DP-14 has an instance as a naming rule only, since the list publishes nothing. DP-15 has an instance as the sequence convention only: the legacy `ix_timer_case_type` index is landed by RWB-P3-E2011-APP as `ix_timer_case_type_status` on `timer (case_id, timer_type, status)`, and a second index on the same leading columns would add write cost and no read (GAP-2224; ASM-3665).

Metadata H is None: the platform contracts the DP rows name are pulled by the rwb-case baseline stories and by the queue-view story of this service, and RWB-P2-E2033-CON never blocks. The story is Day 1 and builds against the published contract and its fake.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| CaseListController | Controller | `GET /cases` and `GET /queues/{queueId}/cases`; parameter binding, problem responses with their message IDs, and the limit refusal on the export path |
| CaseListQueryService | Service | The scoped, filtered and ordered query for one page, the envelope, and the drill down with its queue predicate |
| CaseListRepository | Repository | One SQL query over `recovery_case`, `queue` and the open SERVICE_LEVEL and PRESCRIPTION `timer` rows, in `rwb_case` only |
| AgeingCalculator | Service | Pure functions for BR2 and BR4 on a reference day passed in |
| ServiceLevelStateReader | Service | BR3 and BR5, with the paused test ahead of the breach test |
| PrescriptionClockReader | Service | BR5: `prescriptionClockStatus` and `prescriptionDate` |
| FilterValidator | Service | BR6: each filter value against its list in force and the queue filter against the queue codes |
| PageBoundsReader | Service | BR7: the page-size bounds through the parameters contract |
| ExportLimitReader | Service | BR11: `caselist.export.maxrows` and the count with the page's own filters and scope |
| AccessCheckClient | Client | The Case record right and the scope through the authorise contract, cached per request (DP-08) |
| CaseRowMapper | Component | The row of 12.1, with the owner placeholder and the absent prescription date |
| CaseListPage | React component | The list in its List, Filtered, Empty, Breached and Paused states, the Extract refusal, and the queue drill down |

**Database and migrations.** Reads `recovery_case`, `queue` and `timer`; uses `ix_case_status_queue`, `ix_case_owner_status` and the `ix_timer_case_type_status` index RWB-P3-E2011-APP lands. No new table, column, index or migration for this story (GAP-2224; ASM-3665). The service connects with its own login (DP-02), holding grants on `rwb_case` only.

**Configuration and reference data.** The page bounds are the parameter rows RWB-P3-E2011-APP fixes, read with the version in force; this story declares no second pair, and the legacy limit of 1 to 200 is that maximum (GAP-2224; ASM-3663). `caselist.export.maxrows` is 10,000, the legacy value under DL11, read as a parameter row and never as a constant. LOV-PRODUCT, LOV-CASE-STATUS, LOV-STAGE and the queue codes are rows in force (DP-07). The feature switch keeps the legacy name `rwb.casewf.case-list-ageing`; off, the breach filter is ignored and the queue-view and export columns are served (GAP-2224; ASM-3666).

**Build steps**

1. `CaseListController` and `CaseRowMapper` against the contract fake and the rwb-access stub, with problem bodies and one test per refusal; AC1, AC3, AC4.
2. `CaseListRepository` and `CaseListQueryService` with the scope predicate, the filters, the timer join and the order of BR10; AC1, AC5, AC7.
3. `AgeingCalculator` with unit tests on the reference day, the empty stage clock, the paused clock and the 09:00 to 09:01 boundary; AC2, AC5.
4. `ServiceLevelStateReader` and `PrescriptionClockReader`, with the paused test ahead of the breach test and the absent timer; AC1, AC2.
5. `FilterValidator` with the three lists and the queue codes; AC3.
6. `PageBoundsReader` and `ExportLimitReader`, with the count taken before the export writer starts; AC4, AC9.
7. The drill down with the same row shape and the queue scope check that answers 404; AC8.
8. `AccessCheckClient` and the refusal of a role with no Case record right, as a refusal and not an empty page; AC7.
9. `CaseListPage` with the five states and the Extract refusal, asserted against the route stub; AC1, AC6, AC9.
10. The architecture test that no statement names a schema other than `rwb_case`, and the contract test of RWB-P2-E2033-CON, so the story builds before rwb-access and the edge land.

**Done when.** The tests in section 16 pass; page 1 over 23,600 synthetic cases returns in under 2 s at the 95th percentile in SIT (NFR-008); the 10,000-row limit is refused with 422 and no file; the RWB-P2-E2033-CON contract test is green; and no query of this story reaches a schema other than `rwb_case`.

### 14. Validation and messages

| ID | When | Message | Where it is produced |
|---|---|---|---|
| MSG-GEN-007 | A filter value is not in its list | {value} is not a valid value for {field}. | This story, in `FilterValidator` |
| MSG-GEN-002 | The page size is outside its bounds | {field} must be between {min} and {max}. | This story, in `PageBoundsReader` |
| MSG-P3-020 | No case matches the filters on the list | No cases match these filters. Change a filter to see more. | This story, on the empty state |
| MSG-P3-021 | The extract is above its row limit | The export holds at most {max} rows. Narrow the filters and try again. | This story, on the export path before the file |
| MSG-P4-001 | No valid session | You have no Recovery Workbench role. Ask your team manager to request one. | rwb-access, surfaced here |
| MSG-P4-002 | The role does not hold the Case record right | You cannot {action} here. Your role does not include it. | rwb-access through the authorise contract, surfaced here |
| MSG-P4-003 | The queue is unknown or outside the caller's teams | This case is not in your scope. | This story, on the drill down |
| MSG-GEN-006 | The authorise contract does not answer inside its budget | Not specified in the source documents (GAP-2224; ASM-3662) | This story, on the authorise guard |

The first six are copied unchanged from the legacy story and no identifier is renumbered by the realignment. MSG-P4-003 is the scope refusal of RWB-P3-E2011-APP, used here so both stories answer a queue outside scope the same way. Thai text for each message follows decision DL10. The refusal order is fixed: session, then right, then each filter value, then the page size, then the count for the limit, and only then is a row read or a file built.

### 15. Screens and states

| Screen | State | What this story supplies |
|---|---|---|
| SCR-02 Case list | Loading | The page placeholder while the operation answers |
| SCR-02 Case list | List | The twelve columns, the owner placeholder "Unassigned", the age in state, the age since entry, the prescription date and the service level state |
| SCR-02 Case list | Filtered | The answer for filters queue, product, status, stage, owner and breached, or the 422 of a value outside its list |
| SCR-02 Case list | Empty | The message MSG-P3-020 when no case matches |
| SCR-02 Case list | Breached marker | The text "Breached" on a breached row, never colour alone |
| SCR-02 Case list | Paused marker | The text "Paused" on a case whose stage clock is paused, with the prescription clock beside it |
| SCR-02 Case list | Extract refused | The message MSG-P3-021 naming 10,000 rows, and no file |
| Queue drill down | List | The cases of one queue with the same row shape and order, or the 404 of a queue outside the caller's teams |

The screen is served by the gateway-bff composite route, which calls rwb-case once and merges the answer into the screen model, one hop (DP-19). The route path, the screen-model field list and the visual layout are Not specified in the source documents (GAP-2224; ASM-3662) and belong to RWB-PLT-N001-CON and the designer (DL31); the queue summary rows above the drill down are RWB-P3-E2011-APP's.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-033-12 | AC7, BR1, BR8 | Component | RW-REFADM calls the list; refused with MSG-P4-002 and no row read |
| TC-E2-033-01 | AC1, BR1, BR2, BR3 | Component | Three cases in team MTG-BKK as in AC1, with the authorise fake granting Case record R and Team scope |
| TC-E2-033-02 | AC2, BR4, BR5, BR12 | Component | Case with deviation X1 open, a paused SERVICE_LEVEL timer and a running PRESCRIPTION timer |
| TC-E2-033-03 | AC9, AC3, BR6, BR11 | Contract | Four cases; filters queue, product and breached; 422 MSG-P3-021 above the limit and no file |
| TC-E2-033-04 | AC5, BR3, BR5 | Unit | Timer due 10 December 2026 09:00, read at 09:00 and 09:01 on the calculator, without a database |
| TC-E2-033-05 | AC1, BR5 | Component | NEW case with no SERVICE_LEVEL timer; state NONE and breached false |
| TC-E2-033-06 | AC3, BR6 | Contract | Product filter CAR and status PENDING; 422 MSG-GEN-007 and no case read |
| TC-E2-033-07 | AC4, BR7 | Contract | Page size 500; 422 MSG-GEN-002; the maximum changed to 100 and the request served at 100 |
| TC-E2-033-08 | AC6, BR10 | Component | Filter product SSME with no SSME case; empty state MSG-P3-020 |
| TC-E2-033-09 | AC7, BR1 | Component | Case in team HP-NE read by the MTG-BKK manager; empty answer and no row in any page |
| TC-E2-033-10 | AC9, BR11 | Contract | 10,001 matching cases and a row limit of 10,000; 422 MSG-P3-021 and no file |
| TC-E2-033-11 | AC10, BR10 | Component | 120 cases with equal age, pages of 50, page 1 and page 2 read in sequence |

The legacy level System maps to Component where the case is asserted on the owner's own operations against seeded `rwb_case` rows and the authorise fake, to Contract where the assertion is the request and answer of an operation, and to Unit where the calculator is proved without a database. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

The set is run here against this slice's assertions and by RWB-P2-E2033-APP against the composed page; the two are expected to agree on every shared value because both read the same owner fields. No identifier carries an `-ITG` suffix here: the integration copy is RWB-ITG-E2033-ITG.

### 17. Guardrails

- No business value in code: the page bounds, the extract row limit, the three lists and the queue codes are parameter and reference rows read with the version in force; the code holds behaviour and no value (BR7).
- No personal data in logs, tests, workflow history or prompts: a row carries the case number, codes, dates, whole days and a staff user reference, never a customer name, identity number, address, contact point or account number, and test data is synthetic.
- No read of another service's tables: the case, the queue and the timer are `rwb_case` rows, the rights come through the rwb-access contract, and no statement names a `recovery` or another `rwb_*` schema (DP-01, DP-08, ADR-010).
- No ACE view is read: this slice needs no account, customer, contact or collateral field, so it touches no `v_ace_*` view.
- The operations are reads: no case, queue, timer or assignment row is written, no outbox row is added and nothing is locked for the length of a page (BR9).
- One hop only: the service calls the authorise contract and returns, and never calls a service that calls another (ADR-020).
- The order is total and ends on the case number, so pagination cannot skip or repeat a case, and no page is served from a stored copy.
- A refusal is a refusal: no right, a queue outside the teams and a value outside its list are answers with a status and a message identifier, never an empty page and never a thinner row.
- The extract guards a file that is not this story's: the limit is checked before the access-log entry and before any workbook is built.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-WKM-002 | Team manager sees every team queue, filters by status, product and ageing, exports the view | Business Requirements Epic 2, section 3.2 | None in this module (the capability row is FEAT-CWC-19) | All recovery processes | R-UNI-30; BR1, BR2, BR3, BR6, BR7, BR10 | TC-E2-033-01, TC-E2-033-03, TC-E2-033-06 to TC-E2-033-11 |
| REQ-DVH-006 | Deviation flag visible in every queue view | Business Requirements Epic 2, section 3.2 | None | All recovery processes | R-DEV-01; BR4, BR5, BR12 | TC-E2-033-02 |
| REQ-ACA-006 | Every read of the case store is written to the access log | Business Requirements Epic 2, section 3.2 | None (the access log is rwb-access's) | All recovery processes | BR11; the entry is rwb-access's through RWB-P3-E1031-APP | TC-E2-033-03, TC-E2-033-10 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | Not applicable to a business requirement | None | Not applicable | BR8 | TC-E2-033-01, TC-E2-033-12 |

REQ-ACA-006 also named a data-lake copy; the data lake is removed (DP-17), so the requirement is carried here by the access-log ordering of the extract alone and no lake copy exists (GAP-2224; ASM-3662). The per-read entry of the case store belongs to rwb-access and RWB-P3-E1031-APP; this read path writes none.

| Legacy reference | Where it is kept |
|---|---|
| The legacy columns of AC1 with the owner placeholder and the absent prescription date | Metadata, sections 1, 7, 11, 12.1, 15 |
| The age in state of legacy BR2 beside the age from the entry date of RWB-P3-E2011-APP | Sections 7, 8 BR2, 13 |
| The breach rule R-UNI-30, the paused clock of R-DEV-01 and the two clocks of BR4 and BR5 | Sections 1, 8, 9, 11 |
| The lists of legacy BR6 and the queue codes | Sections 3, 8 BR6, 12.1, 13 |
| Page size 1 to 200 and the 10,000-row limit with MSG-GEN-002, MSG-GEN-007 and MSG-P3-021 | Sections 7, 8 BR7, 8 BR11, 12.1, 14 |
| The stable order and the case-number tie break | Sections 7 AC10, 8 BR10, 12.1 |
| The scope, the role matrix and MSG-P4-002 | Sections 7 AC7, 8 BR1, 10, 14 |
| Legacy test set TC-E2-033-01 to TC-E2-033-12 and its integration copy | Section 16 |
| Legacy key RWB-E2-033, story RWB-P3-E2033-APP, contract RWB-P2-E2033-CON | Metadata, sections 1, 3, 12 |

### 19. Out of scope

- The queue summary counts, the oldest case, the cap use and the queue screens of RWB-E2-011: RWB-P3-E2011-APP and RWB-P3-E2011-CON; this story serves the list they extend and re-uses their page-size rows.
- The extract file, its columns, its writer and the access-log entry before it: RWB-P3-E1031-APP and RWB-P3-E1031-CON. This story owns only the row limit and its refusal.
- The `case_list_row` projection, the case-list file load and the reconciliation rows: rwb-source-data and JOB-04. The case-list API and screen stay with P3 under the R-PREC default ruling.
- The composed page and the workbook on the integration base, and the duplicate serve of this legacy key: RWB-P2-E2033-APP and RWB-P2-E2033-CON.
- The roles, scope rows, permission matrix, masking policy and access log: rwb-access and RWB-P4-E1037-CON.
- The deviation record, its code, its owner and its clearance: rwb-deviation; this story reads the open flag only.
- The next action column and the overdue mark: RWB-E2-035, RWB-P3-E2035-APP.
- The escalation when a service level is breached and the notification that follows: RWB-E1-028 and RWB-E2-015; the timer state is read here and nothing is raised.
- Manual transfer and reassignment from the list: RWB-E2-012, RWB-P3-E2012-APP.
- The service level values per state and their parameter rows: DL22, set by RWB-P3-E1028-APP.
- The composite route path, its merge order and the screen field list: RWB-PLT-N001-CON; the layout belongs to the designer (DL31).
- The real cross-service journey with every service live and its `-ITG` copies: RWB-ITG-E2033-ITG.
