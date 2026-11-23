# RWB-P3-E1031-APP Queue and owner on the case list with filters

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P3-E1031-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-case |
| Service epic | RWB-SVC-P3 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-031 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP06, DP07, DP08, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | L-P3-F |
| Ready to start | After RWB-P3-E1020-APP |
| Depends on (build) | RWB-P3-E1031-CON, RWB-PLT-E1042-CON, RWB-P3-E1042-CON, RWB-PLT-E1043-CON, RWB-P3-E1043-CON, RWB-PLT-E1037-CON, RWB-PLT-E1047-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON, RWB-P3-E1020-APP |
| Contract dependencies | RWB-P4-E1037-CON, RWB-P4-E1039-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P3 rwb-case v1.md (FR-P3-009, FR-P3-011) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-031 and reworked for rwb-case. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **team manager (RW-TEAMMGR)**, I want **the queue and owner columns on the case list, with filters by queue, team and status and an export to Excel**, so that **I see my queues and who owns each case without a new screen**.

Inside `rwb-case` this is the case-list and export slice of legacy RWB-E1-031. Service facts: schema `rwb_case`, REST base `/api/recovery/case/v1`, topic `rwb.case.events.v1` with event names `rwb.case.<Event>.v1`, Temporal task queue `rwb-case` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.case`, epic `RWB-SVC-P3` (DP-13, DP-14).

- The slice delivers two operations on the owner's own rows: `GET /api/recovery/case/v1/cases` with the queue, team and status filters and the queue and owner columns on every row, and `GET /api/recovery/case/v1/cases/export` with the row limit, the access-log entry that precedes the file and the workbook masked by role.
- What the legacy story called the module's own code is now three owners. The right, the scope and the access log are `rwb-access`'s (DP-08, DP-11); the display name of an owner is resolved at the edge; the composite route is `gateway-bff`'s (DP-19). The case, the queue and their columns are this service's and are read from `rwb_case` only (DP-01).
- The wider case list with ageing and the queue views are RWB-P3-E2033-APP and RWB-P3-E2011-APP; this story adds the queue and owner columns, the three filters and the export those two stories re-use. The journey with every service live is RWB-ITG-E1031-ITG.
- All eight legacy criteria are this story's (AC1 to AC8), with legacy test cases TC-E1-031-01 to TC-E1-031-09. The contract form of the two operations is RWB-P3-E1031-CON, which is a build dependency because the row shape it fixes is what the screen binds to.

The story writes no case, queue or assignment row and changes no case status. It reads `recovery_case` and `queue` in `rwb_case`, and it writes exactly one row that is not its own: the access-log entry in `rwb-access`, made through that service's contract before any file is built.

### 2. Business rationale

Today a team manager asks each collector for their list to know who holds which case. With allocation by rule (RWB-P3-E1020-APP), every case has a queue and an owner; this story shows both on the case list, filters by queue, team and status inside the manager's scope, and exports the filtered list with the export written to the access log for PDPA. It meets REQ-CWC-007 (the result of allocation is visible) and REQ-ACA-009 (a user sees only the cases their scope allows).

The facts the screen shows are the owner's: the case row, its queue and its owner are `rwb_case` rows, so the list is served by the service that holds them and no copy can show a manager a different queue or owner (DP-01). The scope is not a filter this service owns; it is the answer of the rwb-access authorise contract, cached for the request (DP-08), and a role without the Case record right is refused rather than shown an empty page, because an empty page reads as "no work" and hides a permission problem.

Three rules do the visible work: filters combine with AND, so a queue filter and a team filter narrow and never widen (BR2); an export is written to the access log before the file is made, and no file is made when the entry cannot be written (BR3), which is the PDPA control the legacy story fixed; and the export holds at most `caselist.export.maxrows` rows with the columns masked for the caller's role (BR4, BR5), so an export can never be a wider read than a screen.

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-P3-E1020-APP is done | Cases carry `queue_id`, `team_code` and `owner_user_id`, so the queue column and the owner column are populated and an unassigned case is the exception it should be (it waits for this story in lane L-P3-F) |
| RWB-P3-E1031-CON is published and baselined | The two operations, the row and page shape, the filter set, the paging order and the problem body this story is tested against. It is an H dependency of the same service and the first thing this story builds against |
| RWB-P4-E1039-CON is published | The access-log write operation and its error answer, used by AC2 and AC5 (contract dependency; the build uses its fake and never blocks) |
| RWB-P4-E1037-CON is published | The authorise answer with the Case record right R, the caller's scope and the masking rules of the role, cached per request (contract dependency) |
| The platform contracts the DP rows name are published | RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1037-CON, RWB-PLT-E1047-CON, RWB-PLT-E1044-CON and RWB-PLT-N001-CON; they are pulled by the rwb-case baseline stories and add no work of their own here |
| The parameters in force hold the export limit | `caselist.export.maxrows` = 10,000, the legacy value under DL11, read as a parameter row with the version in force through the rwb-case parameters contract (DP-06; ASM-3628) |
| The reference data in force holds the lists | LOV-CASE-STATUS and LOV-TEAM as reference rows with the version in force, and the queues as `queue` rows of this service (DP-07) |
| The user holds a role with the Case record right R | The team manager's default scope is Team; the right and the scope are answered by rwb-access and cached per request by the guard library |
| The feature flag `rwb.p3.caselistqueue` is on | Off, the list hides the queue and owner columns and the export (ASM-3629) |

### 4. Flow

1. Team manager: opens SCR-02 Case list through the gateway-bff composite route (DP-19); the screen shows the Loading state.
2. gateway-bff: calls `GET /api/recovery/case/v1/cases` on rwb-case with page 0 and size 50, one hop.
3. rwb-case: `AccessCheckClient` asks the rwb-access authorise contract for the Case record right R and the caller's scope, cached for the request; a role without the right is a 403 and nothing is read (DP-08).
4. `CaseQueryService` applies the caller's scope and returns one page; `CaseListPage` shows each row with case number, product, status, stage, queue, owner and entry date (list state).
5. Team manager: picks queue "DIL-BKK-CO", team "DIL-BKK" and status "ASSIGNED"; the page calls `GET /cases` with the three filters (filtered state).
6. `CaseQueryService` combines the filters with AND inside the scope and returns only the cases that meet every filter, with the total.
7. Team manager: chooses Export; `ExportButton` calls `GET /cases/export` with the filters shown and without page and size.
8. `CaseExportService`: counts the matching rows against `caselist.export.maxrows`; above the limit it refuses with MSG-P3-021 and builds nothing (AC4).
9. `AccessEventClient`: writes the access event AC-EXPT through the rwb-access contract with the user, the time, the filters and the row count, before the workbook is built; if the entry cannot be written, no file is made (AC5, MSG-P7-003).
10. `CaseExportService`: builds the xlsx with the columns masked for the caller's role; the browser downloads "Case list 20261202 1.xlsx" (AC2, AC8).

Nothing in steps 1 to 10 writes a case, a queue or an assignment, publishes an event, starts a workflow or takes a lock for the length of a page.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | No case meets the filters | Empty state with a plain sentence | MSG-P3-020 | AC3 |
| X2 | The filtered list holds more rows than the export limit | Export refused; the user narrows the filter | MSG-P3-021 | AC4 |
| X3 | The access log cannot be written | Export not made | MSG-P7-003 | AC5 |
| X4 | A filter names a queue outside the caller's scope | Only in-scope cases return; an out-of-scope queue returns none | MSG-P3-020 | AC6 |
| X5 | A case has no owner | Owner cell is blank; the case is still listed | None | AC7 |
| X6 | Exactly 10,000 rows | Export allowed | None | AC8 |
| X7 | A role without Case record R opens the list | Refused with 403 | MSG-P4-002 | TC-E1-031-09 |

X4 and X7 answer differently on purpose: a queue outside the scope is an empty page inside a permitted read, and a role without the right is a refusal with a status. A consumer that reads the second as the first hides a permission problem.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Reads the queue, team and owner fields RWB-P3-E1020-APP fills; builds against RWB-P3-E1031-CON and the rwb-access fakes, so neither rwb-access nor the edge needs to exist in the development environment |
| Negotiable | Column order and the export row limit are configurable; the three filters, the AND rule and the access-log ordering are fixed |
| Valuable | Team managers see ownership on one screen and take a masked extract of exactly what they see |
| Estimable | Two query parameters, one export operation, two clients, one screen change |
| Small | Fits under one week: two operations, one query, one export writer, one page of screen support |
| Testable | Every criterion has a test case in section 16; the refusals are contract tests and the screen states are component tests |

### 7. Acceptance criteria

```gherkin
Feature: Queue and owner on the case list with filters

  Background:
    Given team manager U-71 of team "DIL-BKK" with scope Team
    Given team "DIL-BKK" has 64 cases in queue "DIL-BKK-CO" and 20 in "DIL-BKK-OVF"
    Given the rwb-access contract mock returns the Case record right R with scope Team for team "DIL-BKK"

  Scenario: AC1 Filter by queue (legacy RWB-E1-031 AC1)
    Given the case list
    When U-71 filters by queue "DIL-BKK-CO"
    Then 64 cases show, each with its owner and status
    Then no case from another queue shows

  Scenario: AC2 Export (legacy RWB-E1-031 AC2)
    Given the list filtered by queue "DIL-BKK-CO" and status "ASSIGNED" with 51 cases
    Given the rwb-access contract mock returns the access-log entry AC-EXPT recorded with user U-71, the time, the filters and 51 rows
    When U-71 chooses Export
    Then an Excel file with 51 rows downloads
    Then the access log holds the export with user U-71, the time, the filters and 51 rows

  Scenario: AC3 No case meets the filters (legacy RWB-E1-031 AC3)
    When U-71 filters by queue "DIL-BKK-CO" and status "WAITING_PARTNER" and no case matches
    Then the list shows the empty state with MSG-P3-020

  Scenario: AC4 Export above the limit (legacy RWB-E1-031 AC4)
    Given parameter "caselist.export.maxrows" is 10000
    Given a filtered list of 10,001 cases for a user with scope All
    When the user chooses Export
    Then the system makes no file
    Then MSG-P3-021 shows with maximum 10000

  Scenario: AC5 Access log unavailable (legacy RWB-E1-031 AC5)
    Given the access log store is unavailable
    Given the rwb-access contract mock returns the access-log store unavailable
    When U-71 chooses Export on a list of 51 cases
    Then the system makes no file
    Then MSG-P7-003 shows

  Scenario: AC6 Queue outside the scope (legacy RWB-E1-031 AC6)
    When U-71 filters by queue "LIT-BKK-OFF" of team "LIT-BKK"
    Then no case shows
    Then the list shows the empty state with MSG-P3-020

  Scenario: AC7 A case with no owner (legacy RWB-E1-031 AC7)
    Given case RW-2026-000601 is in queue "DIL-BKK-OVF" with no owner
    When U-71 filters by queue "DIL-BKK-OVF"
    Then case RW-2026-000601 shows with a blank owner cell

  Scenario: AC8 Export at the limit (legacy RWB-E1-031 AC8)
    Given a filtered list of exactly 10,000 cases for a user with scope All
    When the user chooses Export
    Then a file with 10,000 rows downloads
```

Every criterion is the legacy text, copied unchanged; the only added line is the rwb-access mock Given of AC2 and AC5, which carries the values the legacy story attributes to the access log. The team filter of the flow is an additive filter on the same operation and is stated in BR2 and in RWB-P3-E1031-CON (GAP-2208; ASM-3624).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The list holds only cases inside the caller's scope (Own, Team, Region, All) | REQ-ACA-009; CTL-09; LOV-SCOPE |
| BR2 | Filters combine with AND, and the queue, team and status filters narrow inside the scope | FSD A2.19; legacy section 4 step 4 |
| BR3 | Every export is written to the access log before the file is made | REQ-ACA-006; CTL-11 |
| BR4 | Export columns follow the masking rules for the caller's role | REQ-ACA-005; DL26 |
| BR5 | An export holds at most the configured number of rows | Parameter caselist.export.maxrows = 10,000 (assumed; DL11) |
| BR6 | A screen responds in under 2 seconds | NFR-008 |
| BR7 | A case with no owner is listed with a blank owner cell, never hidden and never filled by guess | Legacy AC7 |
| BR8 | Nothing is published and no case row is written: the two operations are reads, and the only row written is the access-log entry of rwb-access | DP-09 not applied; legacy section 9 |

### 9. State transitions

None. This story does not change a case status. It reads queue, owner and status only. The states the screen exposes are the case statuses of LOV-CASE-STATUS (NEW, ASSIGNED, IN_PROGRESS, WAITING_CUSTOMER, WAITING_PARTNER, WAITING_APPROVAL, ON_HOLD, CLOSED) as rows in force, and a filter value outside that list is refused before a case is read (RWB-P3-E1031-CON AC6).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-TEAMMGR | Lists, filters and exports cases in team scope (Case record R) |
| RW-CASEOWN | Lists and exports their own cases (Case record R, scope Own) |
| Every role with Case record R | Lists cases in its scope |
| RW-REFADM, RW-SECADM | No Case record right; refused |
| RW-COMPLY | Reads the access log entries for exports |

The right, the scope and its default are answered by rwb-access and held nowhere in rwb-case (DP-08). Role names appear as role codes only; no personal name, address or credential appears in this story, and the owner is a staff user reference (U-71 style) with no name beside it (GAP-2208; ASM-3625).

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
| DF-CAS-012 | recovery_case | region_code | Read |
| DF-CAS-013 | recovery_case | entry_date | Read |
| DF-WRK-001 | queue | id | Read |
| DF-WRK-002 | queue | queue_code | Read |
| DF-WRK-003 | queue | queue_name | Read |
| DF-WRK-004 | queue | team_code | Read |

Field IDs are those in the Logical Data Model and Data Dictionary. Every entity above is a `rwb_case` table of this service (DP-01). `caselist.export.maxrows` and the LOV-CASE-STATUS and LOV-TEAM rows are read with the version in force through the rwb-case parameter and reference contracts and are never joined in SQL (DP-06, DP-07); their field identifiers are not in the legacy table and are not fixed by any source read for this story (GAP-2208; ASM-3628). No row is written, so no field is marked Write.

### 12. Contract

#### 12.1 REST operations provided

Base `/api/recovery/case/v1`; owner rwb-case (P3).

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| GET | `/cases` | One page of the cases in the caller's scope with the filters queue, team, status, owner, product and stage; each row carries case number, product group, status, stage code, queue, owner, team and entry date | Case record R, scope applied through the rwb-access authorise contract | Read only: the same request on unchanged data returns the same rows in the same order |
| GET | `/cases/export` | The same filters without page and size, answered as an xlsx masked by role, after the access-log entry AC-EXPT and after the row-limit check | Case record R, scope applied | Not applicable on the data; each export is a new access-log entry, and the entry is written before the file |

The request carries the legacy query parameters `queue` (uuid), `status`, `owner`, `product`, `stage`, `page`, `size` and `sort`, with `team` added by this story (BR2; GAP-2208; ASM-3624). The response is the legacy `CasePage`: `items` with `caseNo`, `productGroup`, `status`, `stageCode`, `queueId`, `ownerUserId`, `teamCode`, `regionCode` and `entryDate`, plus `page`, `size` and `total`; `queueCode` and `queueName` are joined from `queue` for the column and the filter labels, and `regionCode` is the field the region scope of BR1 is decided on. The exact spelling of the row, the envelope and the problem body is the one RWB-P3-E1031-CON freezes (GAP-2209; ASM-3630).

Errors: 401 no session or no Recovery role (MSG-P4-001); 403 no Case record right (MSG-P4-002); 422 a filter value outside its list or an export above the row limit (MSG-P3-021); 503 the store is down or the access log cannot be written (MSG-P7-003).

#### 12.2 REST operations consumed

One hop, no chaining; 2 s timeout and a breaker per downstream (ADR-020).

| Method | Path | Service | Used for | Timeout |
|---|---|---|---|---|
| POST | `/api/recovery/access/v1/authorise` | rwb-access (P4) | The Case record right R, the caller's scope with its default, and the masking rules of the role, cached per request by the guard library (DP-08; RWB-P4-E1037-CON) | One hop, 2 s, cached per request |
| POST | `/api/recovery/access/v1/access-events` | rwb-access (P4) | The access-log entry AC-EXPT with the user, the time, the filters and the row count, written before the workbook is built (DP-11; RWB-P4-E1039-CON) | One hop, 2 s, no retry on the export path |

The masking rules travel in the authorise answer and are applied by this service when it builds the columns; rwb-case holds no copy of a masking row (GAP-2208; ASM-3627). The parameter and reference reads of DP-06 and DP-07 are in-process library reads of this same service and not cross-service calls, so they are not rows of this table.

#### 12.3 Events published

None. The two operations are reads: no outbox row is written and no event is published. `rwb.case.events.v1` and the names `rwb.case.CaseCreated.v1`, `rwb.case.CaseAllocated.v1`, `rwb.case.CaseTransferred.v1`, `rwb.case.CaseStateChanged.v1` and `rwb.case.TimerBreached.v1` belong to the stories that own the case, allocation, transfer, state and timer behaviour under DP-14, and this story adds none to them. The access event AC-EXPT is not a Kafka event: it is the rwb-access contract call of 12.2.

#### 12.4 Events consumed

None. The list is read from the rows per request, so a case that moves is seen on the next read rather than through a projection, and no inbox row is written. `rwb.case.CaseAllocated.v1` and `rwb.case.CaseTransferred.v1` are the events that change the queue and the owner this screen shows; the screen does not subscribe to them and needs no cache.

#### 12.5 Workflows and activities

None. Both operations answer inside the request: no workflow, no activity, no signal and no timer. `CaseWorkflow` on task queue `rwb-case` is the case lifecycle and is not started, signalled or read by this story.

#### 12.6 Schedules

None. The legacy story had no job and the target adds none: the list is read on request and the export is officer-driven, so no Temporal Schedule, no timer and no batch window belongs to this story.

#### 12.7 Tables owned

| Table | Schema | Owner | Use in this story |
|---|---|---|---|
| `recovery_case` | rwb_case | rwb-case (P3) | The case row behind every list row: number, product group, status, stage, owner, queue, team, region and entry date |
| `queue` | rwb_case | rwb-case (P3) | The queue code and name of the column and of the queue filter values |
| `parameter_catalog`, `parameter_value` | rwb_case | rwb-case (P3) | `caselist.export.maxrows` with the version in force, read through the contracts of this service and never joined in SQL |
| `reference_row`, `reference_version` | rwb_case | rwb-case (P3) | LOV-CASE-STATUS and LOV-TEAM with the version in force |
| `lov_value` | rwb_case | rwb-case (P3) | The list values served by the reference-data contract to the filter pickers |

No other table is named. `assignment` and `queue_member` are this service's and are not read here: the list needs the current owner on the case row, not the assignment history. No table of `rwb_access` is read and no `recovery` or other `rwb_*` schema is named (DP-01, DP-08).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-access authorise fake | The P4 contract of DP-08 | Granting Case record R with scope Team for `DIL-BKK` and scope All for AC4 and AC8; refusing a role with no Case record right with MSG-P4-002; returning the masking rules of the role |
| rwb-access access-log fake | RWB-P4-E1039-CON through DP-11 | Accepting the AC-EXPT entry of AC2 and AC8; answering unavailable for AC5, so no file is made |
| RWB-P3-E1031-CON fake | The two operations of 12.1 | The row, the page envelope, the 403, 422 and 503 problem bodies, for the contract test of this story |
| gateway-bff route stub | The edge route of RWB-PLT-N001-CON | The SCR-02 route and the merged screen model (DP-19) |
| rwb-case seed set and fixtures | This story's own test data | 64 cases in `DIL-BKK-CO`, 20 in `DIL-BKK-OVF`, 51 filtered cases, 10,000 and 10,001 case sets, case `RW-2026-000601` with no owner, one queue of another team, and the parameter row `caselist.export.maxrows` 10,000 |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 2 consumed | `GET /cases` and `GET /cases/export` provided; the rwb-access authorise and access-log operations consumed; one hop, 2 s, breaker, cache per request |
| Kafka | None | No event published and none consumed (12.3, 12.4) |
| Temporal | None | No workflow and no activity (12.5) |
| File | 1 | The xlsx of the export, returned in the response; nothing is written to Blob and no claim-check store is used |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.case`, module `caselist`, Java package `th.co.scb.ace.workbench.recovery.case.caselist`; front end `src/modules/recovery/case/caselist`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_case`; the list and the export read `recovery_case` and `queue` of this service only and never another service's tables | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and its client library: the export row limit is a parameter row | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case: LOV-CASE-STATUS and LOV-TEAM with the version in force | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-08 | RecoveryAccessGuard | Authorise contract of rwb-access and the guard library, cached per request, on both operations | H RWB-PLT-E1037-CON; C RWB-P4-E1037-CON |
| DP-11 | In-process call, published interface | The legacy `AccessEventPublisher` becomes the access-log operation of rwb-access, called with a mock one hop and a 2 s timeout | none (C from the legacy dependency RWB-P4-E1039-CON) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/case/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.case.events.v1` and `rwb.case.<Event>.v1`; naming library; this story publishes nothing | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in schema `rwb_case`: the team index the legacy story asked for arrives here | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route for SCR-02 | H RWB-PLT-N001-CON |

**Components**

| Component | Type | Responsibility |
|---|---|---|
| CaseListController | Controller | `GET /cases` with the team filter; `GET /cases/export`; problem responses with their message ids |
| CaseQueryService | Service | Builds the scoped query with the AND filters; joins `queue` for the code and the name |
| CaseExportService | Service | Row count against the limit, the access-log entry first, then the xlsx with masked columns |
| AccessEventClient | Client | The AC-EXPT entry through the rwb-access access-log contract (DP-11) |
| AccessCheckClient | Client | The Case record right R, the scope and the masking rules through the authorise contract (DP-08) |
| CaseAndWorkflowRepository | Repository | Paged query on `recovery_case` and `queue` in `rwb_case` |
| CaseRowMapper | Component | The row of 12.1, with the blank owner of AC7 |
| CaseListPage | React component | SCR-02 with the queue and owner columns and the states Loading, empty, list, filtered |
| CaseListFilters | React component | Queue, team and status pickers from the queues and the lists in force |
| ExportButton | React component | Calls the export and shows MSG-P3-021 or MSG-P7-003 |

**Database and migrations**

- Reads `recovery_case` and `queue` only; uses `ix_case_status_queue` (status, queue_id) and `ix_case_owner_status` where they already exist.
- Adds `ix_case_team_status` on `recovery_case (team_code, status)` as `V031_1__case_team_index.sql` in the rwb-case Flyway sequence after the V0001 baseline (DP-15; RWB-PLT-E1044-CON). If the case-list story RWB-P3-E2033-APP already lands an index on the same two columns, that index is used and this migration is not created.
- The service connects with its own login (DP-02), holding grants on `rwb_case` only and no grant on a `recovery` or another `rwb_*` schema. The login name is not fixed by any source read here (GAP-2208; ASM-3628).

**Configuration and reference data**

- `caselist.export.maxrows` = 10,000 as a parameter row with the version in force, never a constant (DL11; ASM-3628). The page size default 50 and maximum 200 are the parameter rows RWB-P3-E2011-APP declares and are re-used, not re-declared.
- Queues come from `queue`; LOV-CASE-STATUS, LOV-TEAM and the filter labels come through the rwb-case reference-data contract (DP-07); the labels "Export" and "Owner user ID" follow the label standard (DL10).
- The feature flag keeps the legacy name `rwb.p3.caselistqueue` (ASM-3629).

**Build steps**

1. `CaseListController` and `CaseRowMapper` against the fake of RWB-P3-E1031-CON and the rwb-access stub, with the problem bodies; AC1, AC3.
2. `CaseQueryService` and `CaseAndWorkflowRepository` with the scope predicate and the AND filters, team included; AC1, AC6, AC7.
3. `CaseListPage` and `CaseListFilters` with the Loading, list, filtered and empty states; AC1, AC3, AC7.
4. `AccessEventClient` and `CaseExportService` with the limit check and the access-log entry ahead of the workbook; AC2, AC4, AC5, AC8.
5. The export response, the masked columns and the file name "Case list YYYYMMDD 1.xlsx"; AC2, AC8.
6. The access test, the 2 second check on 26,500 cases, and the contract test of RWB-P3-E1031-CON.

**Feature flag.** `rwb.p3.caselistqueue`. Off: the list hides the queue and owner columns and the export.

**Done when.** The tests in section 16 pass; the list answers in under 2 seconds on 26,500 cases at the 95th percentile in SIT (NFR-008); the export is refused with 422 and no file above 10,000 rows; no file is made when the access-log entry fails; the contract test of RWB-P3-E1031-CON is green; and no query of this story names a schema other than `rwb_case`.

### 14. Validation and messages

| ID | When | Message | Where it is produced |
|---|---|---|---|
| MSG-P3-020 | No case meets the filters | No cases match these filters. Change a filter to see more. | This story, on the list empty state |
| MSG-P3-021 | Export above the row limit | The export holds at most {max} rows. Narrow the filters and try again. | This story, on the export path, before the file |
| MSG-P7-003 | Access log unavailable at export | The action was not taken because the decision could not be recorded. Try again in a few minutes. | rwb-access through the access-log contract, surfaced here |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. | rwb-access through the authorise contract, surfaced here |
| MSG-P4-001 | No valid session | Not specified in the source documents (GAP-2208; ASM-3626) | rwb-access, surfaced here |

The four identified texts are copied from the legacy story character for character and no identifier is renumbered. The refusal order is fixed: the session, then the right, then the filter values, then the row count, then the access-log entry, and only then a row is read or a file is built; a request refused at any of those steps reads nothing and writes nothing.

### 15. Screens and states

| Screen | State | What this story supplies |
|---|---|---|
| SCR-02 Case list | Loading | Skeleton rows while the operation answers |
| SCR-02 Case list | List | Columns case number, product, status, stage, queue, owner, entry date; a blank owner cell for AC7 |
| SCR-02 Case list | Filtered | The chosen queue, team and status shown above the list with a clear control; Export uses the filters shown |
| SCR-02 Case list | Empty | MSG-P3-020 when no case matches |
| SCR-02 Case list | Export refused | MSG-P3-021 naming the maximum of 10,000 rows, and no file |
| SCR-02 Case list | Export failed | MSG-P7-003 when the access-log entry cannot be written, and no file |
| SCR-02 Case list | Refused | MSG-P4-002 on a role without the Case record right |

The screen is SCR-02 and is served by the gateway-bff composite route, which calls rwb-case once and merges the answer into the case screen model, one hop (DP-19). The owner cell shows the owner user reference as the case row holds it; the display name is not this service's to resolve (GAP-2208; ASM-3625). The route path, the screen-model field list and the visual layout belong to RWB-PLT-N001-CON and the designer (DL31).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-031-01 | AC1, BR1, BR2 | Component | 64 cases in DIL-BKK-CO and 20 in DIL-BKK-OVF, authorise fake granting Case record R with Team scope |
| TC-E1-031-02 | AC2, BR3, BR4 | Component | 51 cases filtered by queue and status; the access-log fake accepts the AC-EXPT entry |
| TC-E1-031-03 | AC3 | Component | Filter queue DIL-BKK-CO with status WAITING_PARTNER and no match |
| TC-E1-031-04 | AC4, BR5 | Contract | 10,001 cases, scope All, parameter row 10000; 422 MSG-P3-021 and no file |
| TC-E1-031-05 | AC5, BR3 | Component | Access-log fake answering unavailable; no file and MSG-P7-003 |
| TC-E1-031-06 | AC6, BR1 | Component | Queue LIT-BKK-OFF of team LIT-BKK read by U-71; empty state |
| TC-E1-031-07 | AC7, BR7 | Component | Case RW-2026-000601 in DIL-BKK-OVF with no owner; blank owner cell |
| TC-E1-031-08 | AC8, BR5 | Contract | Exactly 10,000 cases, scope All; file with 10,000 rows |
| TC-E1-031-09 | Access, BR1 | Component | A role without Case record R calls GET /cases and is refused with 403 and MSG-P4-002 |

The legacy level System maps to Component where the assertion is made on the seeded `rwb_case` rows and the rwb-access fakes, and to Contract where it is the request, the answer or the refusal of an operation. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID. No identifier carries an `-ITG` suffix here: the integration copy of the set is RWB-ITG-E1031-ITG.

### 17. Guardrails

- No business value in code: the export row limit, the lists and the queues are parameter and reference rows read with the version in force (BR5; DP-06, DP-07).
- No personal data in logs, tests or prompts: a row carries the case number, codes, dates and a staff user reference, never a customer name, identity number, address or account number; test data is synthetic.
- No read of another service's tables: the case and the queue are `rwb_case` rows, and the right, the scope, the masking rules and the access log come through the rwb-access contracts (DP-01, DP-08, DP-11).
- The export is never made when its access-log entry cannot be written, and the entry is written before the file is built (BR3).
- One hop only: the service calls rwb-access and returns, and never calls a service that calls another (ADR-020).
- A refusal is a refusal: a role without the right is a 403 with MSG-P4-002 and never a thinner row or an empty page.
- No event, no workflow and no lock: both operations are reads and the only row written is rwb-access's.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CWC-007 | Every case has a queue and an owner by rule, visible on the case list | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-19 | 06 Take over and own the case | None | TC-E1-031-01, TC-E1-031-03, TC-E1-031-07 |
| REQ-ACA-009 | A user sees only the cases their scope allows | Epic 1, 3.4; Program, 5.4 | FEAT-CWC-19 | 06 Take over and own the case | None | TC-E1-031-02, TC-E1-031-04, TC-E1-031-05, TC-E1-031-06, TC-E1-031-08 |
| REQ-ACA-006 | Every read of the case store is written to the access log | Epic 1, 3.4; Program, 5.4 | FEAT-CWC-19 | 06 Take over and own the case | BR3 | TC-E1-031-02, TC-E1-031-05 |
| REQ-ACA-005 | An export carries only the columns the caller's role may see | Epic 1, 3.4; Program, 5.4 | FEAT-CWC-19 | 06 Take over and own the case | BR4 | TC-E1-031-02 |

| Legacy reference | Where it is kept |
|---|---|
| The story statement, the rationale and the five preconditions | Sections 1, 2, 3 |
| The eight criteria AC1 to AC8 and the seven exception paths X1 to X7 | Sections 5, 7, 14 |
| Business rules BR1 to BR6, the authority table and the fourteen fields | Sections 8, 10, 11 |
| The two operations, the query parameters and the access event AC-EXPT | Section 12 |
| The components, the team index and the feature flag `rwb.p3.caselistqueue` | Section 13 |
| Messages MSG-P3-020, MSG-P3-021, MSG-P7-003, MSG-P4-002 and screen SCR-02 | Sections 14, 15 |
| Legacy test set TC-E1-031-01 to TC-E1-031-09, and its integration copy RWB-ITG-E1031-ITG | Section 16 |

### 19. Out of scope

- The right, the scope, the permission matrix, the masking policy and the access log itself: rwb-access, RWB-P4-E1037-CON and RWB-P4-E1039-CON. This story reads them through the two contracts and holds no copy.
- The gateway-bff composite route, its path and the screen-model merge: RWB-PLT-N001-CON. The owner display name is resolved at the edge, not here (ASM-3625).
- The wider case list with status, owner and ageing, and the queue views: RWB-P3-E2033-APP, RWB-P3-E2011-APP. This story adds the queue and owner columns, the three filters and the export they re-use.
- My queue and team queue screens (SCR-07) and the queue summary counts: RWB-E2-011, RWB-P3-E2011-APP.
- The base case list with filters by product, stage, age and deviation: RWB-E1-002, FEAT-RDF-18 and RWB-P3-E2033-APP.
- The masking rules themselves: RWB-E1-037, DL26, read from the authorise answer.
- Manual transfer and reassignment from the list: RWB-E2-012, RWB-P3-E2012-APP.
- The next action column and the deviation flag on the list: RWB-E2-035 and RWB-E2-033, RWB-P3-E2035-APP and RWB-P3-E2033-APP.
