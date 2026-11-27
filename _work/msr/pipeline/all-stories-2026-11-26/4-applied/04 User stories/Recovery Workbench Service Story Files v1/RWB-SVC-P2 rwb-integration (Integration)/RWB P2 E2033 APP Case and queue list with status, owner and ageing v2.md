# RWB-P2-E2033-APP Case and queue list with status, owner and ageing

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P2-E2033-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-integration |
| Service epic | RWB-SVC-P2 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-033 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP06, DP07, DP08, DP13, DP14, DP15, DP19 |
| Parallel lane | L-P2-H |
| Ready to start | Day 1 |
| Depends on (build) | RWB-P2-E2033-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1037-CON, RWB-PLT-E1047-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON |
| Contract dependencies | RWB-P3-E1042-CON, RWB-P3-E1043-CON, RWB-P4-E1037-CON, RWB-P3-E1018-CON, RWB-P3-E1031-CON, RWB-P3-E2011-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P2 rwb-integration v1.md (no FR mapped to REQ-WKM-002, REQ-DVH-006, REQ-ACA-006) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-033 for rwb-integration. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P2-E2033-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **team manager (RW-TEAMMGR)**, I want **every case in every queue in my scope on the case list with its identifier, product, queue, owner, status, age in state, stage and prescription clock states and service level breach flag, with a breach filter and an extract**, so that **I can see where work is waiting without asking anyone**.

The legacy story extended the case-list operation and the case export of the monolith, served by `CaseAndWorkflowController`, `CaseListQueryService`, `PrescriptionClockReader`, `AgeingCalculator` and `CaseExportService`, reading `recovery_case`, `queue` and `timer` in the shared recovery schema. Under D-RCV-60 the case, the queue, the timer and the task are rwb-case's (Arch v5 slide 41), the roles, the scope, the rights and the access log are rwb-access's, the parameters and the reference data are rwb-case's (R-PREC default ruling), and no service reads another service's table (DP-01). What stays with rwb-integration is the composition: a read-only case-list page and an Excel export on the integration base, `GET /api/recovery/integration/v1/case-list` and `GET /api/recovery/integration/v1/case-list/export`, composed per request from the P3 case-list and ageing contracts, the P4 authorise contract, the P3 parameter contract and the P3 reference-data contract, with the breach filter, the prescription clock, the deviation flag and the stable order of the legacy story applied to the composed page.

The Ownership Map keeps `GET /cases` and `GET /cases/export` with P3, and ADR-020 with DP-19 puts the screens directly on the owner services through gateway-bff. This story does not move that ownership: rwb-case keeps the system-of-record read of the case list and its own export, and the composed page and the file on the integration base are an additional, read-only composition for the integration slice of this legacy key. That the same page is now composed twice, once case-side and once integration-side, is recorded as a gap and an assumption and is not hidden (GAP-0660; ASM-1133). The precedent is the credit approval pack of RWB-P2-E2006-APP, which records the same deliberate double composition.

The slice writes no business row. It reads nothing from another schema, holds no copy of a case, a queue or a timer, publishes no event, starts no workflow and creates no Schedule, because the legacy story wrote nothing either. Its only write is the access-log entry of an export, which is the rwb-access owner's row and is asked for through the owner's contract; the file itself is produced on request and is never a data-lake file (DP-17).

### 2. Business rationale

A team manager today learns where cases wait by asking each owner or by building a spreadsheet. The legacy story completed the case list for every queue in the manager's scope: a breach filter, the prescription clock beside the stage clock so a paused case is not read as safe, and the same columns in the extract. It meets REQ-WKM-002 (every queue in the team, filtered by status, product and ageing, with an export), REQ-DVH-006 (the deviation flag is visible in every queue view) and REQ-ACA-006 (a read of the case store is written to the access log), and the business measure is the count of cases past their service level per queue, which the manager can read every morning.

In the target the facts are in the same place but the path changes. The case rows, the queue and the timer projection are case facts of rwb-case (DP-01), so they are read through the case-list and ageing contracts and never from `recovery_case`, `queue` or `timer`. The roles, the scope and the rights are data of rwb-access (Arch v5 slide 41), so the authorise check is one call of its contract (DP-08). The page size limits and the export row limit are parameters of rwb-case (DP-06), and the lists the filter values are checked against are reference data of rwb-case (DP-07), so neither is written in code. Every call is one hop with a 2 s timeout and a breaker, built on Day 1 against its fake (DP-11 as it applies to the consumed contracts, ADR-020).

The composition survives a boundary that the monolith did not have. Inside one service, a page and its extract read the same rows in the same transaction; across a contract there is no shared transaction, so the story fixes the two rules that keep the two answers consistent: the page and the export are read with the same filter set and the same stable order, and the export re-reads at the moment of the request rather than reusing a page from the browser. A case that changes between two page requests is therefore ordered by case number, never by a row number, which is what AC11 asserts.

The duplication is the one deliberate cost, and it is stated. The ageing and service-level rules (BR2 to BR5) are evaluated twice: by the P3 ageing contract for the case-side screen, and by `AgeingAndBreachCalculator` here for the composed page and the export, on the same timer and clock inputs. The two answers agree because both read the same owner's fields; where they could disagree, the case-side answer is the record and this page is the composition (GAP-0660; ASM-1145).

### 3. Preconditions

- RWB-P2-E2033-CON is published and baselined: the two provided operations, the page shape, the filter set, the breach and clock fields, the error envelope, the read-only idempotency statement and the contract fakes of this story.
- RWB-PLT-E1042-CON and RWB-P3-E1042-CON are published: the parameter contract of rwb-case and the client library. `caselist.export.maxrows` (assumed 10,000 in the legacy story, DL11) and the case-list page bounds are rows of that contract, not code (DP-06; ASM-1138).
- RWB-PLT-E1043-CON and RWB-P3-E1043-CON are published: the reference-data contract of rwb-case, which carries LOV-PRODUCT, LOV-CASE-STATUS and LOV-STAGE with the version in force (DP-07; ASM-1139).
- RWB-PLT-E1037-CON and RWB-P4-E1037-CON are published: the authorise contract, the guard library that caches the rights of a session, and the access-log operation of an export (DP-08).
- RWB-PLT-E1047-CON is published: the naming library, so the REST base, the topic name and the event names of this service follow the platform rule and not a local choice (DP-13, DP-14).
- RWB-PLT-E1044-CON is published: the per-service Flyway sequence and the migration conventions of `rwb_integration` (DP-15). This story adds no migration, because it stores nothing (ASM-1142).
- RWB-PLT-N001-CON is published: the gateway-bff composite route that serves SCR-02 Case list (DP-19).
- RWB-P3-E1031-CON is published: the case-list contract of rwb-case, which fixes the row of the composed page and the filter set this story passes through.
- RWB-P3-E2011-CON is published: the ageing and service-level contract of rwb-case, which publishes `ageDays`, `stageClockStart`, `serviceLevelDueAt`, `serviceLevelState`, `prescriptionDate` and `prescriptionClockStatus` for a case (DP-01; ASM-1137).
- RWB-P3-E1018-CON is published: the case record read of rwb-case, used when a list row does not carry a field the composition needs.
- The role to permission matrix gives RW-TEAMMGR the Case record right R with Team scope, and the caller is signed in through Entra ID with a role that holds Case record R.
- The queues of the teams are loaded in rwb-case, with their team and their role, and are read through the queue list of its contract, never from a table of this service.
- The feature switch `rwb.casewf.case-list-ageing` is carried to the platform flag library and is on; while it is off the breach filter and the clock columns are not served (ASM-1144).
- The login is the rwb-integration login (DP-02): Not specified in the source documents (GAP-0660; ASM-1135).

### 4. Flow

1. Team manager: opens SCR-02 Case list through gateway-bff and chooses the filters (DP-19).
2. gateway-bff: calls `GET /api/recovery/integration/v1/case-list` on rwb-integration, one hop, and merges the answer into the SCR-02 screen model.
3. rwb-integration: checks the Case record right and the caller's scope through the rwb-access authorise contract, cached per session by the guard library; a role without Case record R is a 403 and nothing is read (DP-08).
4. rwb-integration: validates each filter value against its list of values read through the rwb-case reference-data contract, the queue code against the queue list of the rwb-case contract, and the page size against the bounds read through the rwb-case parameter contract (DP-06, DP-07).
5. rwb-integration: reads the page of cases in the caller's scope through the rwb-case case-list contract, with the filters and the paging the legacy operation used; the contract is the only path to the rows (DP-01).
6. rwb-integration: reads the ageing and service-level fields of that page of case ids through the rwb-case ageing contract, batched so that one page is one hop: `ageDays`, `stageClockStart`, `serviceLevelDueAt`, `serviceLevelState`, `prescriptionDate` and `prescriptionClockStatus`.
7. rwb-integration: `AgeingAndBreachCalculator` applies BR2 to BR5 to those inputs, so the page carries the age in state, the service level state and the breach flag of the legacy story, and `PrescriptionClockReader` resolves the prescription clock state and its date beside the stage clock.
8. rwb-integration: applies the breach filter when `breached` is set and orders the rows by breach, then age in state descending, then case number, and returns one page with its paging envelope.
9. Front end: shows the columns of section 15 and marks each breached case with the text "Breached", never by colour alone.
10. Team manager: chooses Extract; the front end calls `GET /api/recovery/integration/v1/case-list/export` with the same filters and without page and size.
11. rwb-integration: reads the parameter `caselist.export.maxrows` and refuses the export with 422 when the matching rows exceed it, before any file is built.
12. rwb-integration: records one access-log entry through the rwb-access contract, with the user, the time, the filters and the row count; a refused entry stops the export and no file is produced.
13. rwb-integration: writes the matching rows with the ageing and clock columns to an Excel file and returns it as a download; the file is produced on request and is stored nowhere (DP-17).
14. rwb-integration: answers the export with the file and with `Cache-Control: no-store`; the read is idempotent, so the same request on unchanged data returns the same rows in the same order and the access log holds one entry per export.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A filter value is not in its list of values, for example product CAR | Request refused with 422 before any case is read | MSG-GEN-007 | AC6 |
| X2 | Page size below 1 or above 200 | Request refused with 422 | MSG-GEN-002 | AC7 |
| X3 | No case matches the filters | Empty state; the extract holds the header row only | MSG-P3-020 | AC8 |
| X4 | A queue filter names a queue outside the caller's scope | Only cases in scope are returned, so the result is empty | MSG-P3-020 | AC9 |
| X5 | A case has no SERVICE_LEVEL timer yet (status New) | `serviceLevelState` NONE; `breached` false | None | AC5 |
| X6 | The service level due time equals the current time | Not breached; breached from the next minute | None | AC4 |
| X7 | The extract would hold more than 10,000 rows | Extract refused before any file is built | MSG-P3-021 | AC10 |
| X8 | A case changes between two page requests | Order is stable by case number, so no case is skipped or repeated by the order | None | AC11 |
| X9 | The caller's role does not hold Case record R | Refused with 403 before any contract is called; nothing is read and nothing is logged as an export | MSG-P4-002 | Access test TC-E2-033-12 |
| X10 | A consumed contract (rwb-case case list, ageing, queues, parameters, reference data, or rwb-access) does not answer inside the 2 s budget | One hop, 2 s timeout and a breaker per downstream; no partial page and no file is returned, and a page is never answered from a stale cache | MSG-GEN-006 | AC1, AC3 |
| X11 | The access-log entry of an export cannot be recorded | No file is produced and nothing is written; the export is refused | MSG-P7-003 | AC3 |

X10 is the mechanism that replaces the legacy in-process calls: a page that cannot be composed has no answer to show, so the failure is a 503 and not a thinner page. X11 is a refusal and not a degradation: an export that cannot be recorded is not made (BR7 in the legacy story, kept here).

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds on Day 1 against the published contracts: this key's contract baseline, the parameter and reference-data contracts, the authorise contract, the naming library, the migration conventions and the edge route. The rwb-case and rwb-access answers come from their contract fakes |
| Negotiable | The export columns, the filter set and the page bounds are fixed by the legacy story; the list values, the limits and the queue codes are data rows of their owners |
| Valuable | Gives the manager the whole of the team's work in one list and one file, and keeps the case facts with rwb-case |
| Estimable | Two operations, one composition service, one calculator, one clock reader, one export writer, six consumed contracts and one page of screen support |
| Small | Fits one iteration with its tests, and writes no business row |
| Testable | Each owned criterion is one automated test against the contract fakes; the access case is a component test and the boundary case is an architecture test |

### 7. Acceptance criteria

```gherkin
Feature: Case and queue list with status, owner and ageing

  Background:
    Given today is 10 December 2026 at 09:00 Asia/Bangkok
    Given the team manager holds role RW-TEAMMGR with Team scope for team "MTG-BKK"
    Given queue "MTG-BKK-CO" belongs to team "MTG-BKK" and role RW-CASEOWN
    Given queue "MTG-BKK-LIT" belongs to team "MTG-BKK" and role RW-LITOFF
    Given the rwb-access contract mock returns role "RW-TEAMMGR" with the Case record right "R" and scope "Team" for team "MTG-BKK"
    Given the rwb-case contract mock returns queue "MTG-BKK-CO" for team "MTG-BKK" with role "RW-CASEOWN" and queue "MTG-BKK-LIT" for team "MTG-BKK" with role "RW-LITOFF"
    Given the rwb-case contract mock returns LOV-PRODUCT, LOV-CASE-STATUS and LOV-STAGE with the version in force
    Given the rwb-case contract mock returns case-list page size minimum 1, case-list page size maximum 200 and caselist.export.maxrows 10,000

  Scenario: AC1 Every case is visible (legacy RWB-E2-033 AC1)
    Given case "RW-2026-000101", product MORTGAGE, queue "MTG-BKK-CO", owner "U-1001", status ASSIGNED, stage clock start 1 December 2026, service level due 8 December 2026 17:00
    Given case "RW-2026-000102", product MORTGAGE, queue "MTG-BKK-LIT", owner "U-1002", status IN_PROGRESS, stage clock start 8 December 2026, service level due 15 December 2026 17:00
    Given case "RW-2026-000103", product MORTGAGE, queue "MTG-BKK-CO", no owner, status NEW, entry date 10 December 2026
    Given the rwb-case contract mock returns case "RW-2026-000101", product MORTGAGE, queue "MTG-BKK-CO", owner "U-1001", status ASSIGNED and stage clock start 1 December 2026
    Given the rwb-case contract mock returns case "RW-2026-000102", product MORTGAGE, queue "MTG-BKK-LIT", owner "U-1002", status IN_PROGRESS and stage clock start 8 December 2026
    Given the rwb-case contract mock returns case "RW-2026-000103", product MORTGAGE, queue "MTG-BKK-CO", no owner, status NEW and entry date 10 December 2026
    Given the rwb-case contract mock returns the SERVICE_LEVEL timer of case "RW-2026-000101" due 8 December 2026 17:00, of case "RW-2026-000102" due 15 December 2026 17:00, and no SERVICE_LEVEL timer for case "RW-2026-000103"
    When the manager opens the list
    Then 3 rows show
    Then row "RW-2026-000101" shows product MORTGAGE, queue "MTG-BKK-CO", owner "U-1001", status ASSIGNED, age in state 9 days and service level state BREACHED
    Then row "RW-2026-000102" shows queue "MTG-BKK-LIT", owner "U-1002", status IN_PROGRESS, age in state 2 days and service level state RUNNING
    Then row "RW-2026-000103" shows owner "Unassigned", status NEW, age in state 0 days and service level state NONE
    Then the rows are in the order "RW-2026-000101", "RW-2026-000102", "RW-2026-000103"

  Scenario: AC2 Ageing is correct when a clock is paused (legacy RWB-E2-033 AC2)
    Given case "RW-2026-000104" with deviation X1 raised on 9 December 2026
    Given its SERVICE_LEVEL timer has paused true and status PAUSED
    Given its PRESCRIPTION timer has status RUNNING and expires 30 June 2028
    Given the rwb-case contract mock returns case "RW-2026-000104" with deviation open Yes
    Given the rwb-case contract mock returns the SERVICE_LEVEL timer of case "RW-2026-000104" with paused true and status PAUSED, and its PRESCRIPTION timer with status RUNNING and expires 30 June 2028
    When the list is read
    Then row "RW-2026-000104" shows service level state PAUSED, prescription clock RUNNING with date 30 June 2028 and deviation open Yes
    Then the system does not count the case as breached

  Scenario: AC3 It can be filtered and extracted (legacy RWB-E2-033 AC3)
    Given the 4 cases above
    Given the rwb-case contract mock returns the 4 cases above with their queue, owner, status, stage clock start and entry date
    Given the rwb-case contract mock returns the SERVICE_LEVEL and PRESCRIPTION timers of the 4 cases above
    Given the rwb-access contract mock returns one access-log entry with the user, the time, the 3 filters and row count 1
    When the manager filters by queue "MTG-BKK-CO", product MORTGAGE and breached Yes and then chooses Extract with the same filters
    Then 1 row shows, "RW-2026-000101"
    Then an Excel file downloads with a header row and 1 data row for "RW-2026-000101" with columns age in state, service level state, service level due, prescription date, prescription clock and deviation open
    Then the access log holds one export entry with the user, the time, the 3 filters and row count 1

  Scenario: AC4 Breach at the boundary of the service level (legacy RWB-E2-033 AC4)
    Given case "RW-2026-000105" with a RUNNING SERVICE_LEVEL timer due 10 December 2026 09:00
    Given the rwb-case contract mock returns the RUNNING SERVICE_LEVEL timer of case "RW-2026-000105" due 10 December 2026 09:00
    When the list is read at 10 December 2026 09:00
    Then row "RW-2026-000105" shows service level state RUNNING
    Then when the list is read again at 10 December 2026 09:01, row "RW-2026-000105" shows service level state BREACHED

  Scenario: AC5 A case with no service level timer (legacy RWB-E2-033 AC5)
    Given case "RW-2026-000103" with status NEW and no SERVICE_LEVEL timer
    Given the rwb-case contract mock returns case "RW-2026-000103" with status NEW and no SERVICE_LEVEL timer
    When the list is read with breached No
    Then row "RW-2026-000103" shows service level state NONE and is in the result

  Scenario: AC6 A filter value outside its list is refused (legacy RWB-E2-033 AC6)
    Given the rwb-case contract mock returns LOV-PRODUCT without the value "CAR"
    When the manager requests the list with product "CAR"
    Then the response is 422 with message MSG-GEN-007 for field product
    Then the system reads no case

  Scenario: AC7 Page size outside its limits is refused (legacy RWB-E2-033 AC7)
    Given the rwb-case contract mock returns case-list page size minimum 1 and maximum 200
    When the manager requests the list with page size 500
    Then the response is 422 with message MSG-GEN-002 naming page size, minimum 1 and maximum 200

  Scenario: AC8 No case matches (legacy RWB-E2-033 AC8)
    Given the rwb-case contract mock returns no case for product SSME
    When the manager filters by product SSME and then chooses Extract with the same filter
    Then the list shows the empty state with message MSG-P3-020
    Then an Excel file downloads with the header row and no data row

  Scenario: AC9 Scope limits the list (legacy RWB-E2-033 AC9)
    Given case "RW-2026-000201" in queue "HP-NE-CO" of team "HP-NE"
    Given the rwb-access contract mock returns scope "Team" for team "MTG-BKK" and no scope over queue "HP-NE-CO"
    Given the rwb-case contract mock returns case "RW-2026-000201" in queue "HP-NE-CO" of team "HP-NE"
    When the manager of team "MTG-BKK" filters by queue "HP-NE-CO"
    Then the list shows the empty state with message MSG-P3-020
    Then case "RW-2026-000201" does not appear in any page of the unfiltered list

  Scenario: AC10 The extract limit (legacy RWB-E2-033 AC10)
    Given 10,001 cases in the manager's scope match breached No
    Given the rwb-case contract mock returns 10,001 cases in the manager's scope matching breached No
    Given the rwb-case contract mock returns caselist.export.maxrows 10,000
    When the manager chooses Extract with breached No
    Then the response is 422 with message MSG-P3-021 naming 10,000 rows
    Then the system produces no file

  Scenario: AC11 Order is stable across pages (legacy RWB-E2-033 AC11)
    Given 120 cases in scope with no breach and the same age in state
    Given the rwb-case contract mock returns 120 cases in scope with no breach and the same age in state
    When the manager reads page 1 and page 2 with page size 50
    Then page 1 holds the 50 lowest case numbers and page 2 the next 50
    Then no case appears on both pages
```

AC1 to AC11 are the criteria this story owns; every value is copied unchanged from the legacy story and the only additions are the `Given` lines that state what each contract mock returns. The rwb-case contracts answer the rows, the queues, the ageing and service-level fields, the prescription clock, the deviation flag, the list values and the two parameter limits. The rwb-access contract answers the Case record right, the scope and the access-log entry of an export. The breach decision at the boundary (AC4), the age in state (AC1, AC2), the paused clock (AC2), the absent timer (AC5) and the order (AC1, AC11) are this story's own computation on those inputs, which is why they are asserted here and not stubbed. X9 is proved by TC-E2-033-12 against this story's own operation.

The page is composed twice in the target. rwb-case keeps `GET /cases` and `GET /cases/export` and the case-side screen, and this story composes the same page on the integration base for the integration slice of this legacy key. The duplication is deliberate and recorded (GAP-0660; ASM-1133); the values the two answers share are read from the same P3 contracts, so they agree on the row, the queue, the owner, the age and the service level state.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The list holds only cases in the caller's scope: Own, Team or All, from the role's default scope, read through the rwb-access authorise contract | `role.default_scope` through the P4 contract; CTL-09; DP-08 |
| BR2 | Age in state is the whole number of calendar days from `stage_clock_start` (or `entry_date` when it is empty) to today in Asia/Bangkok | `recovery_case.stage_clock_start`, `entry_date` through the P3 ageing contract; legacy RWB-E2-011 `ageDays` |
| BR3 | A case is breached when its SERVICE_LEVEL timer has status EXPIRED, or has status RUNNING with `expires_at` earlier than now. A breach does not move the case | R-UNI-30; timer status through the P3 ageing contract |
| BR4 | A deviation pauses the stage clock and keeps the prescription clock running; the list shows both; a paused SERVICE_LEVEL timer is never breached | R-DEV-01; timer `paused` through the P3 ageing contract |
| BR5 | `prescriptionClockStatus` is RUNNING or EXPIRED from the PRESCRIPTION timer, and NONE when the case has no such timer | timer type; LOV-TIMER-STATUS; the P3 ageing contract |
| BR6 | Filter values are checked against LOV-PRODUCT, LOV-CASE-STATUS and LOV-STAGE and against the queue codes in force, all read through their owners' contracts | lists of values; the P3 queue list; DP-07 |
| BR7 | The extract holds at most `caselist.export.maxrows` rows, carries no customer personal field, and is written to the access log before the file is made | legacy RWB-E1-031; CTL-11; REQ-ACA-006; DP-06 |
| BR8 | The service reads no case, queue, timer, role, parameter or reference row of another service: every fact comes through the owner's contract, one hop, and `rwb_integration` holds no copy and no foreign key into another schema | Arch v5 slides 13, 41 and 45; DP-01; ADR-010; ADR-020 |
| BR9 | The page and the export are read-only: no business row is written, no event is published, no workflow is started and no Schedule is created; the only write is the access-log entry of an export, asked for through the rwb-access contract | legacy BR and section 9; DP-17; Template and Rules §R7.2 s17 |
| BR10 | The page size limits and the export row limit are parameter rows of rwb-case read with the version in force; no limit is written in code | DP-06; legacy guardrail 1 |
| BR11 | The file is produced on request for the officer and is never a data-lake file; the data lake is removed | DP-17; Arch v5 slide 37; ASM-1146 |
| BR12 | The switch is the platform feature flag `rwb.casewf.case-list-ageing`; while it is off, the breached parameter is ignored and the list and export keep the columns of the case-side read | legacy solution plan; platform flag library (ASM-1144) |
| BR13 | The ageing and service-level rules are evaluated on both sides: the P3 ageing contract for the case-side screen, and `AgeingAndBreachCalculator` here for the composed page and the export, on the same owner fields; the case-side answer is the record | GAP-0660; ASM-1145 |

### 9. State transitions

None. This story does not change a case status and does not move a case. It reads the case rows, the queue list and the timer projection through their owners' contracts and, for an export, writes one access-log entry through the rwb-access contract.

| Observed fact | Written by | Appears as |
|---|---|---|
| Case number, product, queue, owner, status, stage, entry date, stage clock start, deviation flag | rwb-case (P3) | The row of the page and of the file |
| Age in state, service level due, service level state, prescription date, prescription clock state | rwb-case (P3) ageing contract, re-applied here by BR2 to BR5 | The computed columns of the page and of the file |
| Queue code, team code and queue role | rwb-case (P3) | The queue filter values and their validation |
| Case record right, scope and default scope | rwb-access (P4) | Whether the caller sees a page, and which rows |
| Access-log entry of an export | rwb-access (P4) | One log row per export, with the user, the time, the filters and the row count |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-TEAMMGR, team manager | Reads and extracts the list for the team's queues (Case record R, Team scope) |
| RW-CASEOWN, case owner | Reads and extracts the list for the cases they own (Case record R, Own scope) |
| RW-PRODHEAD, RW-AUDIT, RW-CONDUCT and other roles with Case record R | Read and extract the list in their scope |
| RW-REFADM, reference data administrator | No Case record right; refused with MSG-P4-002 |
| rwb-integration service identity (the rwb-integration login, DP-02) | Applies the access check, calls the P3 and P4 contracts one hop away, composes the page, builds the file and writes nothing but the owner's access-log entry |
| rwb-case, through its contracts | Owns the case, the queue, the timer projection, the parameters and the reference data; is the record of the case-side list and of its own export |
| rwb-access, through its contracts | Owns the right, the scope, the masking policy and the access log; the export entry is its row |
| gateway-bff (the platform edge) | Calls the composed operation once and merges the answer into the SCR-02 screen model; holds no copy of a case |
| No approval applies | The story takes no decision |

The service runs as the rwb-integration login (DP-02). The login name is Not specified in the source documents (GAP-0660; ASM-1135).

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | recovery_case | id | Read through the rwb-case case-list contract |
| DF-CAS-002 | recovery_case | case_no | Read through the rwb-case case-list contract |
| DF-CAS-003 | recovery_case | product_group | Read through the rwb-case case-list contract |
| DF-CAS-005 | recovery_case | status | Read through the rwb-case case-list contract |
| DF-CAS-006 | recovery_case | stage_code | Read through the rwb-case case-list contract |
| DF-CAS-009 | recovery_case | owner_user_id | Read through the rwb-case case-list contract |
| DF-CAS-010 | recovery_case | queue_id | Read through the rwb-case case-list contract |
| DF-CAS-011 | recovery_case | team_code | Read through the rwb-case case-list contract |
| DF-CAS-013 | recovery_case | entry_date | Read through the rwb-case case-list contract |
| DF-CAS-017 | recovery_case | prescription_date | Read through the rwb-case ageing contract |
| DF-CAS-018 | recovery_case | stage_clock_start | Read through the rwb-case ageing contract |
| DF-CAS-019 | recovery_case | deviation_open | Read through the rwb-case case-list contract |
| DF-WRK-002 | queue | queue_code | Read through the rwb-case queue list |
| DF-WRK-004 | queue | team_code | Read through the rwb-case queue list |
| DF-WRK-028 | timer | case_id | Read through the rwb-case ageing contract |
| DF-WRK-030 | timer | timer_type | Read through the rwb-case ageing contract |
| DF-WRK-032 | timer | expires_at | Read through the rwb-case ageing contract |
| DF-WRK-034 | timer | paused | Read through the rwb-case ageing contract |
| DF-WRK-035 | timer | status | Read through the rwb-case ageing contract |
| DF-REF-038 | role | default_scope | Read through the rwb-access authorise contract |
| The parameter rows of the case list | parameter_value, through the rwb-case parameter contract | `caselist.export.maxrows` and the page bounds, with the version in force | Read; the field IDs of these rows are Not specified in the source documents (GAP-0660; ASM-1138) |
| The reference rows of the filter values | reference_row, through the rwb-case reference-data contract | LOV-PRODUCT, LOV-CASE-STATUS, LOV-STAGE with the version in force | Read; the field IDs of these rows are Not specified in the source documents (GAP-0660; ASM-1139) |
| The access-log entry of an export | the access log of rwb-access | user, time, the filters and the row count | Written by rwb-access, asked for through its contract; no column is held here |

Field IDs are those in the Logical Data Model and Data Dictionary v9. No row of `recovery_case`, `queue`, `timer`, `role`, `parameter_value` or `reference_row` is copied into `rwb_integration` (BR8), and the schema holds no foreign key into another schema. The JSON field names of the case-list and ageing answers are Not specified in the source documents (GAP-0660; ASM-1136; ASM-1137). The Excel column set is the legacy set: the case number, product, queue, owner, status, stage, age in state, service level state, service level due, prescription date, prescription clock and deviation open, and it carries no customer personal field.

### 12. Contract

#### 12.1 REST operations provided

Base `/api/recovery/integration/v1`; owner rwb-integration (P2).

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| GET | `/case-list` | The composed case and queue list page: the rows of the caller's scope with case number, product, queue, owner, status, stage, age in state, service level state, service level due, prescription date, prescription clock state and deviation open, the filter set, the breach filter, the stable order and the paging envelope | Case record R, scope applied, through the rwb-access authorise contract | Read only: the same request on unchanged data returns the same rows in the same order; no response is stored |
| GET | `/case-list/export` | The same filters without page and size, written as an Excel file with the legacy export columns, after the access-log entry is recorded | Case record R, scope applied | Read only on the data; each export records its own access-log entry |

The Ownership Map keeps `GET /cases` and `GET /cases/export` with P3 and ADR-020 with DP-19 puts SCR-02 on the owner service through gateway-bff, so the composed page and the export on the integration base are an additional read-only composition and not a move of the owner's operation (GAP-0660; ASM-1133; ASM-1134). The two paths are not rows of the Ownership Map and are fixed here under the service base of DP-13; their exact form and the JSON field names of the page, the filter set and the problem body are Not specified in the source documents (GAP-0660; ASM-1134; ASM-1136).

The query parameters are the legacy ones: `product`, `stage`, `status`, `owner`, `queue`, `page`, `size`, `sort` and `breached` (true or false), and the export takes the same set without `page` and `size`. Each row carries `caseNo`, `product`, `queue`, `owner` (with the text "Unassigned" when it is empty), `status`, `stage`, `ageDays`, `serviceLevelState` (BREACHED, RUNNING, PAUSED or NONE), `serviceLevelDueAt`, `prescriptionDate`, `prescriptionClockStatus` (RUNNING, EXPIRED or NONE) and `deviationOpen`. Errors: 401 no session or no Recovery role (MSG-P4-001); 403 no Case record right (MSG-P4-002); 422 a filter value outside its list (MSG-GEN-007), a page size outside 1 to 200 (MSG-GEN-002) or an export above its row limit (MSG-P3-021); 503 a consumed contract does not answer inside the budget (MSG-GEN-006) or a database is unavailable (E503); and 503 an access-log entry that cannot be recorded (MSG-P7-003), which produces no file.

#### 12.2 REST operations consumed

One hop per call, no chaining; 2 s timeout and a breaker per downstream (ADR-020). The Ownership Map and the P3, P4 contract stories name the owners; this story declares only the consumed side.

| Method | Path | Service | Used for | Timeout |
|---|---|---|---|---|
| GET | `/api/recovery/case/v1/cases` | rwb-case (P3) | The case rows of the caller's scope with the filters and the paging of the legacy operation; the case-list contract of RWB-P3-E1031-CON | One hop, 2 s, breaker |
| GET | The ageing and service-level read of the RWB-P3-E2011-CON contract, for a page of case ids | rwb-case (P3) | `ageDays`, `stageClockStart`, `serviceLevelDueAt`, `serviceLevelState`, `prescriptionDate` and `prescriptionClockStatus`, batched so that one page is one hop; the per-case projection the Ownership Map names is `GET /cases/{caseId}/timers` | One hop, 2 s, breaker |
| GET | `/api/recovery/case/v1/queues` | rwb-case (P3) | The queue codes in force with their team code and role, for the queue filter and its validation | One hop, 2 s, breaker |
| GET | `/api/recovery/case/v1/cases/{caseId}` | rwb-case (P3) | The case record read of RWB-P3-E1018-CON, used when a list row does not carry a field the composition needs | One hop, 2 s, breaker |
| GET | The reference-data read of the RWB-P3-E1043-CON contract | rwb-case (P3) | LOV-PRODUCT, LOV-CASE-STATUS and LOV-STAGE with the version in force (DP-07) | One hop, 2 s, cached |
| GET | `/api/recovery/case/v1/admin/parameters` | rwb-case (P3) | `caselist.export.maxrows` and the case-list page bounds, with the version in force (DP-06) | One hop, 2 s, cached |
| POST | `/api/recovery/access/v1/authorise` | rwb-access (P4) | The Case record right, the caller's scope and its default scope, cached per session by the guard library (DP-08) | One hop, 2 s, cached |
| POST | The access-log operation of the RWB-P4-E1037-CON contract | rwb-access (P4) | One access-log entry per export: the user, the time, the filters and the row count; a refusal fails the export | One hop, 2 s |

The path of the ageing read, the path of the reference-data read and the path and the row shape of the access-log operation are Not specified in the source documents (GAP-0660; ASM-1137; ASM-1139; ASM-1140). The case-list, queue and parameter paths are the Ownership Map rows of P3 under the service base of DP-13, and the queue codes come from that queue list and not from a queue table of this service (ASM-1147); the authorise path is the one Architecture v5 slide 14 gives rwb-access.

#### 12.3 Events published

None. The composed read and the export publish no event, write no outbox row and hold no decision record. The service's topic `rwb.integration.events.v1` carries only FileDelivered and FileFailed, which belong to the file stories of this service (Arch v5 slide 16 and slide 43), and this story declares no topic and no event name of its own (DP-14).

#### 12.4 Events consumed

None. The page is composed per request through the owners' contracts and subscribes to no topic: a case that changes is seen on the next read, not through a projection of `CaseStateChanged`, `DeviationRaised` or `TimerBreached`, and no inbox row is written by this story.

#### 12.5 Workflows and activities

None. The page and the export are served inside the request: no workflow, no activity, no signal and no timer. The stage clock and the prescription clock belong to the case workflow of rwb-case, which this story only reads through its contract.

#### 12.6 Schedules

None. The legacy story had no job and the target adds none: the page is read on request and the export is officer-driven, so no Schedule, no Temporal timer and no batch window is created by this story (Arch v5 slide 44).

#### 12.7 Tables owned

| Table | Schema | Owner | Use in this story |
|---|---|---|---|
| None | — | — | This story creates, reads and writes no table; nothing is copied into `rwb_integration` (DP-01, BR8) |
| `recovery_case`, `queue`, `timer`, `role`, `parameter_value`, `reference_row` | each owner's own schema | rwb-case (P3) and rwb-access (P4) | The facts behind the consumed contracts; this story never reads them |
| The access log | rwb_access | rwb-access (P4) | One entry per export, written by the owner through its contract |

The `rwb_integration` schema holds interface config, file runs and outbound items for the file stories of this service (Arch v5 slide 41), and the platform library objects `outbox_event`, `processed_event`, `outbox_delivery` and `idempotency_key` exist in it from the service baseline. This story adds no table, no column and no index to any of them, writes no row in any of them, and adds no migration in the service's Flyway sequence (DP-15, ASM-1142).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-case WireMock — case list and queues | The P3 contract of RWB-P3-E1031-CON | Case `RW-2026-000101`, `RW-2026-000102`, `RW-2026-000103`, `RW-2026-000104`, `RW-2026-000105` and `RW-2026-000201` with their product, queue, owner, status and stage clock start; queues `MTG-BKK-CO` and `MTG-BKK-LIT` with their team and role; no case for product SSME; 120 cases of equal age; 10,001 cases for AC10 |
| rwb-case WireMock — ageing | The P3 contract of RWB-P3-E2011-CON | The SERVICE_LEVEL and PRESCRIPTION timers of the cases above, including the paused timer of AC2, the boundary timer of AC4 and the absent timer of AC5 |
| rwb-case WireMock — reference data and parameters | The P3 contracts of RWB-P3-E1043-CON and RWB-P3-E1042-CON | LOV-PRODUCT, LOV-CASE-STATUS and LOV-STAGE with the version in force, LOV-PRODUCT without `CAR` for AC6; page size minimum 1, maximum 200 and `caselist.export.maxrows` 10,000 |
| rwb-access WireMock | The P4 contract of RWB-P4-E1037-CON | Allow RW-TEAMMGR with Case record R and Team scope for `MTG-BKK`; refuse RW-REFADM with MSG-P4-002; scope over `MTG-BKK` and none over `HP-NE-CO`; the access-log entry recorded, and refused for X11 |
| gateway-bff composite route stub | The edge route of RWB-PLT-N001-CON | The SCR-02 route and the merged screen model (DP-19) |
| A 2 s delay stub per downstream | X10 | One slow answer per consumed contract, so the breaker and the unavailable answer are exercised |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 5 named consumed plus the ageing, reference-data and access-log operations | The page and the export provided; the case list, the queues, the case record, the parameters, the ageing read, the reference-data read, the authorise check and the access-log entry consumed; one hop, 2 s timeout, breaker per downstream |
| Kafka | None | No event is published and none is consumed (12.3, 12.4) |
| Temporal | None | No workflow and no activity (12.5) |
| File | 1 written on request | The Excel export of the legacy column set, produced per request and stored nowhere (DP-17); no file is read |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.integration`, module `caselist`, Java package `th.co.scb.ace.workbench.recovery.integration.caselist`; front end support `src/modules/recovery/integration/caselist/CaseListPage.tsx`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables; here the case, the queue and the timer come from rwb-case's contracts | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-08 | RecoveryAccessGuard | Authorise contract of rwb-access and the guard library | H RWB-PLT-E1037-CON; C RWB-P4-E1037-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/integration/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library; no event and no topic is added here | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema; this story adds no migration | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-14 applies to the names of this service and not to a new event: the topic `rwb.integration.events.v1` and the events FileDelivered and FileFailed stay the file stories', and this slice publishes nothing (12.3). DP-15 applies to the service baseline and not to this read: the story adds no table and no migration, and the H dependency is on the conventions of the sequence (ASM-1142).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| CaseListController | Controller | `GET /case-list` and `GET /case-list/export`; the parameter binding, the error mapping and the `Cache-Control: no-store` header |
| CaseListCompositionService | Service | Composes the page: the access check, the filter validation, the case rows, the ageing fields, the breach filter, the order and the paging envelope |
| AgeingAndBreachCalculator | Service | Pure functions for BR2 to BR5, unit tested without a database: age in state, the service level state, the breach flag, the boundary rule and the paused rule |
| PrescriptionClockReader | Service | Resolves `prescriptionClockStatus` and `prescriptionDate` from the PRESCRIPTION timer of the ageing answer (BR5) |
| FilterValidator | Service | Checks each filter value against the reference-data lists and the queue codes in force, and the page size against the parameter bounds |
| CaseExportService | Service | Re-reads with the same filters, applies the row limit, asks for the access-log entry first, and writes the legacy columns |
| ExportWorkbookWriter | Component | Writes the Excel file of the legacy column set in the request; the file is streamed to the caller and stored nowhere |
| CaseListClient | Client | The case rows through the rwb-case case-list contract (DP-01) |
| AgeingClient | Client | The ageing and service-level fields of a page of case ids through the rwb-case contract, batched to one hop |
| QueueCatalog | Service | The queue codes, their teams and their roles through the rwb-case queue list |
| ParameterReader | Service | `caselist.export.maxrows` and the page bounds through the rwb-case parameter contract with the version in force (DP-06) |
| ReferenceCatalog | Service | LOV-PRODUCT, LOV-CASE-STATUS and LOV-STAGE through the reference-data contract with the version in force (DP-07) |
| AccessCheckClient | Client | The Case record right and the scope through the rwb-access authorise contract, cached per session by the guard library (DP-08) |
| AccessLogClient | Client | One access-log entry per export through the rwb-access contract; a refusal fails the export |
| SourceCallGuard | Component | Wraps each contract call with the 2 s timeout, a breaker and a bulkhead, and turns a failure into the unavailable answer (X10) |
| CaseListPage | React component | The SCR-02 columns, the breach filter, the breach marker, the paused marker and the empty state; the screen is served through gateway-bff (DP-19) |

**Database and migrations**

- No table, no column and no index: the read copies nothing and the schema `rwb_integration` is not touched by this story (BR8, BR9).
- No migration in the rwb-integration Flyway sequence. DP-15 is satisfied by the baseline of RWB-P2-E1007-APP and by the conventions of RWB-PLT-E1044-CON (ASM-1142).
- The service connects with its own login, `rwb_integration`, holding grants on its own schema only and no grant on `recovery` or on another `rwb_*` schema (DP-02, Arch v5 slide 29). The login name is Not specified in the source documents (GAP-0660; ASM-1135).

**Configuration and reference data**

- `caselist.export.maxrows` (assumed 10,000 in the legacy story, DL11) and the case-list page bounds are rows of the rwb-case parameter contract, read with the version in force; no limit is in code (DP-06; ASM-1138).
- LOV-PRODUCT, LOV-CASE-STATUS and LOV-STAGE are rows of the rwb-case reference-data contract with the version in force, and the queue codes are those of the rwb-case queue list; no code value is in code (DP-07; ASM-1139).
- The feature switch keeps the legacy name `rwb.casewf.case-list-ageing` as its reference. In the target it is a feature flag of the platform flag library (R-PREC default ruling; the Ownership Map gives `feature_flag` to PLT); off ignores the breached parameter and serves the case-side columns only (BR12; ASM-1144).

**Build steps**

1. `CaseListCompositionService` and `CaseListController` against the contract fakes, with the filter set, the paging envelope and one test per AC; AC1, AC8, AC9.
2. `CaseListClient` and `AgeingClient` over the rwb-case contracts, with the batched ageing read so that one page is one hop; AC1, AC2, AC5.
3. `AgeingAndBreachCalculator` and `PrescriptionClockReader` with unit tests for BR2 to BR5, including the boundary of AC4 and the paused clock of AC2; AC1, AC2, AC4, AC5.
4. `FilterValidator` with `ReferenceCatalog`, `QueueCatalog` and `ParameterReader`, so no list value and no limit is in code; AC6, AC7.
5. `AccessCheckClient` and the scope refusal with 403; the access case of section 16.
6. `CaseExportService` and `ExportWorkbookWriter` with the legacy column set, the row limit from the parameter contract, and the access-log entry recorded before the file is built; AC3, AC8, AC10.
7. The stable order by breach, age in state and case number, with the two-page test; AC11.
8. `SourceCallGuard` with the timeout, the breaker and the unavailable answer; X10 as a component test.
9. `CaseListPage` against the gateway-bff stub, with the list, filtered, paused, breached and empty states of section 15.
10. The contract-fake run of every consumed answer in isolation and the architecture test that no statement reaches another schema, so the story builds before rwb-case and rwb-access land.

**Feature switch.** The legacy flag name `rwb.casewf.case-list-ageing` is kept as the legacy reference for the switch. In the target the switch is a feature flag of the platform flag library (Template and Rules §R3 default ruling; Ownership Map `feature_flag` is PLT); off ignores the breached parameter and keeps the case-side columns (ASM-1144).

**Done when.** The tests in section 16 pass, page 1 of the list over 23,600 synthetic cases returns in under 2 seconds at the 95th percentile in SIT (NFR-008 as the legacy story states it), the export of 10,000 rows completes and one access-log entry is recorded per export, the contract tests of RWB-P3-E1031-CON, RWB-P3-E2011-CON, RWB-P3-E1042-CON, RWB-P3-E1043-CON and RWB-P4-E1037-CON stay green, and no query of this story reaches the `recovery` schema or another `rwb_*` schema.

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
| MSG-GEN-006 | A consumed contract does not answer inside the budget | Not specified in the source documents (GAP-0660; ASM-1136) |

MSG-GEN-007 to MSG-P7-003 are copied unchanged from the legacy story, and no identifier is renumbered by the realignment. MSG-GEN-006 is the platform unavailable message; its text is fixed by the Error and Message Standard and not by this story, so the placeholder stands here (ASM-1136). MSG-P1-001 does not arise in this story, because the composed page carries no ACE data product and no freshness stamp. Thai text for each message follows decision DL10.

### 15. Screens and states

| Screen | State | What the user does |
|---|---|---|
| SCR-02 Case list | Loading | Sees the list placeholder while the composed operation answers |
| SCR-02 Case list | List | Reads the columns case number, product, queue, owner, status, stage, age in state, service level state, service level due, prescription date, prescription clock and deviation |
| SCR-02 Case list | Filtered | Sets filters for queue, product, status, stage, owner and breached, and reads the filtered page |
| SCR-02 Case list | Empty | Reads the empty message MSG-P3-020 when no case matches |
| SCR-02 Case list | Breached marker | Reads the text "Breached" on a breached row, never colour alone |
| SCR-02 Case list | Paused marker | Reads "Paused" on a case whose stage clock is paused, with the prescription clock beside it |
| SCR-02 Case list | Extract | Chooses Extract with the same filters and receives the Excel file, or the row-limit message MSG-P3-021 |

The screen is SCR-02 Case list and is served by the gateway-bff composite route, which calls rwb-integration once and merges the answer into the case screen model, one hop (DP-19). The route path, the screen-model field list and the merge order are Not specified in the source documents (GAP-0660; ASM-1141) and belong to RWB-PLT-N001-CON; the case-side slice RWB-P3-E2033-APP carries the screen work of the owner's own list, and this story supplies the page model, the columns and the states above for the composed page.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-033-12 | Access | Component | RW-REFADM calls the list; refused with MSG-P4-002 |
| TC-E2-033-01 | AC1, BR1, BR2, BR3 | End to end | Three cases in team MTG-BKK as in AC1 |
| TC-E2-033-02 | AC2, BR4, BR5 | End to end | Case with X1 raised, paused SERVICE_LEVEL timer, running PRESCRIPTION timer |
| TC-E2-033-03 | AC3, BR7 | End to end | Four cases; filters queue, product and breached; extract file and access log |
| TC-E2-033-04 | AC4, BR3 | End to end | Timer due 10 December 2026 09:00, read at 09:00 and 09:01 |
| TC-E2-033-05 | AC5 | End to end | NEW case with no SERVICE_LEVEL timer |
| TC-E2-033-06 | AC6, BR6 | End to end | Product filter CAR |
| TC-E2-033-07 | AC7 | End to end | Page size 500 |
| TC-E2-033-08 | AC8 | End to end | Filter product SSME with no SSME case |
| TC-E2-033-09 | AC9, BR1 | End to end | Case in team HP-NE read by the MTG-BKK manager |
| TC-E2-033-10 | AC10, BR7 | End to end | 10,001 matching cases |
| TC-E2-033-11 | AC11 | End to end | 120 cases with equal age, pages of 50 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. Legacy levels map System to End to end, Access to Component and Resilience to NFR. TC-E2-033-01 to TC-E2-033-12 are the ones this story runs, against its own two operations and the contract fakes; the real cross-service journey of the key is proven by RWB-ITG-E2033-ITG, and this story holds no `-ITG` copy of a legacy test case.

### 17. Guardrails

- No business value in code: page size limits, the export limit, the lists and the service levels are read from the parameter catalog and the reference tables through their owners' contracts; the story fixes only the behaviour.
- No personal data in logs, tests, workflow history or prompts; the page and the extract carry the case number, the owner reference and no customer field, and test data is synthetic.
- No read of another service's tables and no ACE view: the case, the queue and the timer come only through the rwb-case contracts, the rights and the access log only through the rwb-access contract, and the service holds no grant on the `recovery` schema or on another `rwb_*` schema (DP-01, DP-08, ADR-010).
- The breach flag is computed at read time; the story never changes a timer or a case, and a refusal writes nothing.
- One hop, no chaining: the operation never calls a downstream of a downstream, and the breaker and bulkhead are per downstream (ADR-020).
- The export carries no customer personal field, is recorded in the access log before the file is made, and is never written to a data lake (DP-17).
- The page and the export are read-only: no business row, no decision record, no event and no workflow state (BR9).
- A role without the Case record right sees a refusal, never a partial list and never another role's rows (X9).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-WKM-002 | Team manager sees every team queue, filters by status, product and ageing, exports the view | Program 5.3; Epic 2 3.2 | None (legacy) | All recovery processes | R-UNI-30; BR1, BR2, BR3, BR6, BR7 | TC-E2-033-01, TC-E2-033-03 to TC-E2-033-12 |
| REQ-DVH-006 | Deviation flag visible on the case record view and in every queue view | Program 5.15; Epic 2 3.2 | None (legacy) | All recovery processes | R-DEV-01; BR4 | TC-E2-033-02 |
| REQ-ACA-006 | Every read of the case store is written to the access log | Program 5.4 | None (legacy) | All recovery processes | BR7, BR9 | TC-E2-033-03, TC-E2-033-10 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | — | — | — | BR8 | TC-E2-033-01, TC-E2-033-12 |

REQ-ACA-006 names a data-lake copy as well; the data lake is removed (Arch v5 slide 37, DP-17), so only the export entry of the case store is carried here (BR7) and the per-read coverage of the owner's own list belongs to the rwb-access and rwb-case stories.

### 19. Out of scope

- The case list of rwb-case itself, its own export and the SCR-02 screen work of the owner's list: RWB-P3-E2033-APP, and the `GET /cases` and `GET /cases/export` rows of the Ownership Map that stay with P3.
- The contract baseline of this composed read: RWB-P2-E2033-CON (the sibling story of this key).
- Next action columns and the overdue mark: RWB-E2-035.
- My queue and team queue screens with counts, oldest case and cap use: RWB-E2-011, carried by RWB-P3-E2011-CON and its page.
- Escalation when a service level is breached: RWB-E1-028 and RWB-E2-015.
- Manual transfer from the list: RWB-E2-012.
- The service level values per state: DL22, read as reference and parameter rows of rwb-case.
- The masking rule, the roles, the scope rows and the access log itself: the rwb-access stories; this story reads them through the P4 contract and holds no copy.
- The parameters and reference-data rows and their versions: the rwb-case stories; this story reads them through their contracts.
- The gateway-bff composite route, its path and its merge order: RWB-PLT-N001-CON.
- The service baseline, the adapter pattern, the problem mapping and the contract-test harness of rwb-integration: RWB-P2-E1007-APP.
- Any data-lake copy of the list or of the extract: removed with the data lake (DP-17).
- The real cross-service journey with all services live: RWB-ITG-E2033-ITG.
