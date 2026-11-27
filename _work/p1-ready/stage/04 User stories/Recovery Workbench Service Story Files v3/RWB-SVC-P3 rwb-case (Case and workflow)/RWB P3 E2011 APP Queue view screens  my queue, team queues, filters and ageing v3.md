# RWB-P3-E2011-APP Queue view screens: my queue, team queues, filters and ageing

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P3-E2011-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-case |
| Service epic | RWB-SVC-P3 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-011 |
| Legacy disposition | Moved (no impact) |
| Build status | Not started |
| Epic design sign-off | Not specified in the source documents (DOR-RWB-P3-E2011-APP-14); the story stays Draft until a signed epic design record exists |
| Size | Not specified in the source documents (DOR-RWB-P3-E2011-APP-16); the squad sizes it at refinement |
| Patterns applied | DP01, DP06, DP07, DP08, DP13, DP14, DP15, DP19 |
| Parallel lane | L-P3-F |
| Ready to start | After RWB-P3-E1020-APP |
| Depends on (build) | RWB-P3-E2011-CON, RWB-PLT-E1042-CON, RWB-P3-E1042-CON, RWB-PLT-E1043-CON, RWB-P3-E1043-CON, RWB-PLT-E1037-CON, RWB-PLT-E1047-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON, RWB-P3-E1020-APP, RWB-P3-E1031-CON |
| Contract dependencies | RWB-P4-E1037-CON |
| Contract version | Not specified in the source documents (DOR-RWB-P3-E2011-APP-23); the contract is addressed by path /v1 |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P3 rwb-case v1.md (FR-P3-014, FR-P3-015, FR-P3-016, FR-P3-017, FR-P3-018, FR-P3-019, FR-P3-021, FR-P3-022, FR-P3-025, FR-P3-040) |
| Status | Draft (directive resolutions) |
| Readiness decisions | RD-P1-003, RD-P1-005, RD-P1-040, RD-P1-041, RD-P1-062 |

**Version 3 changes.**

- Test case rows TC-P3-E2011-APP-01 added to section 16 (Test Cases v9 mappings, tc-backfill).
- D-RCV-60 finishing pass: RD-P1-062.

- RD-P1-005 and RD-P1-041: BR12 states the freshness status values, the stamp in use and the never-stamped answer.
- RD-P1-062 fixes the no-date behaviour and fixture dates. Omit X-Data-As-Of and show the stale banner. MSG-P1-001 wording for an empty date remains Pending (GAP-3284).
- RD-P1-003 and RD-P1-040: no text change; this view subscribes to no event.

**Change log.** D-RCV-60, 22 November 2026: moved from RWB-E2-011 for rwb-case. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P3-E2011-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (22 resolved, 10 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3 aligns the story with RD-P1-003, RD-P1-005, RD-P1-040, RD-P1-041. Tool: Claude Code / Claude Sonnet 5.5.

### 1. Story

As a **team manager (RW-TEAMMGR)**, I want **screens for my queue and my team's queues with filters by stage, route, status and age, sorted by service level, served by rwb-case from its own `rwb_case` rows over `/api/recovery/case/v1` and through the gateway-bff composite route**, so that **every person sees their work in one place and the team manager sees the team's load**.

The three read operations behind the two screens are `GET /api/recovery/case/v1/cases` for My queue with its filters, sort and age, `GET /api/recovery/case/v1/queues` for the team queue summary with its count, oldest age, breach count and per-owner spread against the cap, and `GET /api/recovery/case/v1/queues/{queueId}/cases` for the drill down from a queue row. The legacy story is moved with no business change: the behaviour, the values, the sort, the counts, the page limits and the message texts are the ones RWB-E2-011 fixed, and this story only re-homes them on the target naming of rwb-case.

In the target the monolith screen is not a screen model held by the case service: it is a composite route at the edge (DP-19). gateway-bff calls rwb-case once per answer and merges the answers into the screen model, so rwb-case returns the list and the queue rows and never composes a second service's panel. rwb-case authorises every call through the rwb-access authorise contract and its guard library (DP-08), reads its list labels and its page-size limits as data through the reference-data and parameters contracts of rwb-case (DP-07, DP-06), reads the business date of the case data from the rwb-source-data freshness answer, and reads nothing else outside schema `rwb_case` (DP-01). The read path writes no row and publishes no event; the counts it shows move only when their own stories publish CaseCreated, CaseAllocated, CaseTransferred, CaseStateChanged and TimerBreached on `rwb.case.events.v1` (DP-14).

### 2. Business rationale

Cases are run from team spreadsheets and the team manager learns of a late case from email. With about 23,600 open cases at go-live (NFR-001), a case owner needs their own list ordered by the next service level date, and the team manager needs each queue's depth, oldest case and breaches without a report request. This story gives both views on the case list and the team queues screen. It meets REQ-WKM-001, REQ-WKM-002 and REQ-WKM-006. The measure is that the team queue counts equal the case list counts for the same team every day.

Nothing in that rationale changes in the target, which is why the legacy key is moved and not reworked. What changes is where the answers come from: the list and the queue rows are two operations of one owning service instead of two screens of one monolith, and the screen is composed at the edge inside one 2 s budget (DP-19, ADR-020). The queue view is now the only place a team manager can see load, ageing and breaches without a report request, because the reporting copy is read from events by rwb-reporting and arrives later than the working list.

### 3. Preconditions

- RWB-P3-E1020-APP is done: every case has a queue and an owner by rule, so a queue row and an owner row are both populated.
- RWB-P3-E1031-CON is published: the case list contract (SCR-02) shows queue and owner with filters by queue, team and status, and the export; this story extends that page and does not redefine it.
- RWB-P3-E1028-APP is done: each assigned case has a SERVICE_LEVEL timer, and that story writes `timer.status`, `timer.paused` and the escalation fields this view reads.
- RWB-P3-E2011-CON is published: the OpenAPI 3.1 document of the three read operations, the page and queue resources, the error envelope, the paging and sort rules and the contract fakes, so the build starts on Day 1 against the fake (DP-11).
- RWB-P3-E1019-APP is done: queues are loaded with their team, role and caseload cap (RWB-E1-019; cap values DL23, assumed 150).
- RWB-PLT-E1042-CON and RWB-P3-E1042-CON are published: the parameters contract of rwb-case with its client library, so the page-size default and maximum are read as data and never written in code (DP-06).
- RWB-PLT-E1043-CON and RWB-P3-E1043-CON are published: the reference-data contract of rwb-case with its client library, so LOV-STAGE, LOV-ROUTE and LOV-CASE-STATUS come as data with their version (DP-07).
- RWB-PLT-E1037-CON is published: the access guard library, and rwb-access answers the authorise check over its contract, cached per request (DP-08).
- The signed-in person holds RW-CASEOWN (scope Own) or RW-TEAMMGR (scope Team) with the scope set by rwb-access (RWB-E1-037 in the legacy numbering).
- The ACE batch for the business date is COMPLETE, or the freshness answer of rwb-source-data reports an earlier business date and the list shows its date as stale with MSG-P1-001 (GAP-0709; ASM-1256).
- RWB-PLT-N001-CON is published: the gateway-bff composite route for SCR-02 and SCR-07 (DP-19). Its path, its merge order and the screen field list belong to that contract; this story fixes only the three answers rwb-case returns.
- RWB-PLT-E1047-CON is published: the topic and event naming library (DP-14). RWB-PLT-E1044-CON is published: the per-service Flyway sequence in schema `rwb_case` (DP-15).
- The login is the rwb-case login (DP-02): one login and one connection pool for the service, with grants on schema `rwb_case` only (Architecture v5 slide 29).

### 4. Flow

1. Case owner: opens My queue from the menu, reached through the App Gateway at `/recovery/*` and the gateway-bff session (DP-19).
2. Front end: calls `GET /api/recovery/case/v1/cases` with `owner=me`, `sort=serviceLevelDueAt` and the filters kept for the session, one hop through the composite route.
3. rwb-case: authorises the read through the rwb-access contract, `POST /api/recovery/access/v1/authorise`, right R on Case record and on Queue and allocation, scope applied, cached per request (DP-08).
4. rwb-case: applies the scope, the filters and the sort and returns one page of cases with age, status and service level state, plus the `X-Data-As-Of` header carrying the business date of the case data that the freshness answer of rwb-source-data reports (GAP-0709; ASM-1256).
5. Front end: shows the list in state List, or Empty with MSG-P3-017.
6. Case owner: sets the stage filter to Litigation; the front end keeps the filter in session storage and reloads the list in state Filtered.
7. Team manager: opens Team queues from the menu; the front end calls `GET /api/recovery/case/v1/queues`, one hop.
8. rwb-case: returns each queue in the manager's teams with the open case count, the oldest entry date, the breach count and the open cases per owner against the cap.
9. Team manager: selects a queue; the front end calls `GET /api/recovery/case/v1/queues/{queueId}/cases` and shows the cases sorted by service level.
10. gateway-bff: merges the answers into the screen model and, for a paused row, takes the deviation code that the hover of MSG-P3-004 names from the rwb-deviation answer of the screen; rwb-case returns the paused state and the open flag only.
11. Nothing in this flow writes: the three operations are reads, no case, no queue and no timer changes, and the read path publishes no event and writes no outbox row.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The person has no case in scope for the filters | Empty state | MSG-P3-017 | AC4 |
| X2 | Age from is greater than age to | The request is refused; the list is not reloaded | MSG-GEN-003 | AC5 |
| X3 | Page size above 200 | The request is refused | MSG-GEN-002 | AC6 |
| X4 | A team manager opens a queue of another team | Not found | MSG-P4-003 | AC7 |
| X5 | Today's ACE batch has not arrived | The list shows with the stale banner and the date of the data | MSG-P1-001 | AC8 |
| X6 | A case's service level timer is paused by a deviation | The case shows "Paused" and sorts after running timers | MSG-P3-004 | AC9 |
| X7 | A role without Case record R or without Queue and allocation R opens either view | Refused with 403 by the rwb-access check behind the endpoint; the answer carries the refusal and not an empty list | MSG-P4-002 | AC13; TC-E2-011-13 |

The refusal of X7 is a refusal and never an empty page: a consumer that reads an empty page as "no work" would hide a permission problem, which is why the two answers are distinguished by status and not by body.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Reads the case, queue and timer rows that RWB-P3-E1020-APP, RWB-P3-E1019-APP and RWB-P3-E1028-APP already write; builds against the published contracts and their fakes, so neither rwb-access nor rwb-source-data needs to exist in the development environment |
| Negotiable | Columns and filter order can change; the sort, the counts and the page limits are fixed |
| Valuable | Each person works one ordered list; the team manager sees load and breaches |
| Estimable | Three endpoints extended, one consumed freshness answer, one reference-data and one parameters read, two screens |
| Small | Fits in one sprint with its tests |
| Testable | API tests on a seeded database and browser tests on both screens; the scope refusal and the stale banner are stubbed in the contract fakes and real in SIT |

### 7. Acceptance criteria

```gherkin
Feature: Queue view screens: my queue, team queues, filters and ageing

  Background:
    Given the business date is 2026-12-15
    Given team "MTG-BKK" has queues "MTG-BKK-CO" and "MTG-BKK-LIT" with a caseload cap of 150
    Given user "U-CO-01" holds RW-CASEOWN in team "MTG-BKK" and user "U-TM-01" holds RW-TEAMMGR for team "MTG-BKK"

  Scenario: AC1 My queue (legacy RWB-E2-011 AC1)
    Given "U-CO-01" owns 40 open cases, 3 with an expired service level timer and 37 with running timers
    When "U-CO-01" opens My queue
    Then 40 cases list in one page
    Then the 3 breached cases come first, then the 37 by service level due date, earliest first
    Then each row shows the case number, product group, stage, status, age in days from the entry date and the service level due date

  Scenario: AC2 Team view (legacy RWB-E2-011 AC2)
    Given "MTG-BKK-CO" holds 412 open cases with the oldest entered on 2026-09-02 and 9 breaches
    Given "MTG-BKK-LIT" holds 38 open cases with the oldest entered on 2026-10-20 and 0 breaches
    When "U-TM-01" opens Team queues
    Then "MTG-BKK-CO" shows count 412, oldest case age 104 days and 9 breaches
    Then "MTG-BKK-LIT" shows count 38, oldest case age 56 days and 0 breaches
    Then each owner in "MTG-BKK-CO" shows their open case count against the cap of 150

  Scenario: AC3 Filter (legacy RWB-E2-011 AC3)
    Given "U-CO-01" owns 12 open cases on stage "LITIGATION" and 28 on other stages
    When the stage filter is set to "LITIGATION" and the list refreshes
    Then only the 12 litigation cases show
    Then after "U-CO-01" opens a case and returns to My queue the filter is still "LITIGATION"
    Then after sign-out and sign-in the filter is cleared

  Scenario: AC4 Empty queue (legacy RWB-E2-011 AC4)
    Given "U-CO-02" owns no open case
    When "U-CO-02" opens My queue
    Then the screen shows the empty state with MSG-P3-017

  Scenario: AC5 Age range in the wrong order (legacy RWB-E2-011 AC5)
    When "U-CO-01" sets age from 120 and age to 90
    Then the system refuses the request with MSG-GEN-003 naming "age to" and "age from"
    Then the list keeps its previous rows

  Scenario: AC6 Page size above the limit (legacy RWB-E2-011 AC6)
    When the front end requests My queue with page size 500
    Then the system refuses the request with MSG-GEN-002 naming "size", 1 and 200

  Scenario: AC7 Queue of another team (legacy RWB-E2-011 AC7)
    Given the rwb-access contract mock returns scope Team for "U-TM-01" over team "MTG-BKK" and no scope over team "SME-NTH"
    Given queue "SME-NTH-CO" belongs to team "SME-NTH"
    When "U-TM-01" requests the cases of "SME-NTH-CO"
    Then the system does not find the response with MSG-P4-003

  Scenario: AC8 Stale data (legacy RWB-E2-011 AC8)
    Given the rwb-source-data contract mock returns the latest complete ACE business date 2026-12-11
    Given the expected ACE business-date batch of 2026-12-14 has not arrived and the case data is from 2026-12-11
    When "U-CO-01" opens My queue
    Then the 40 cases show with the stale banner MSG-P1-001 naming the date 2026-12-11

  Scenario: AC9 Paused service level (legacy RWB-E2-011 AC9)
    Given the rwb-deviation contract mock returns deviation "X1" open on 2 of the 40 cases
    Given 2 of the 40 cases have a deviation "X1" open and their service level timers paused
    When "U-CO-01" opens My queue
    Then the 2 cases show "Paused" with MSG-P3-004 on hover and sort after the 37 running timers

  Scenario: AC10 Age boundary (legacy RWB-E2-011 AC10)
    Given case "RW-2026-000301" entered on 2026-09-16 and case "RW-2026-000302" entered on 2026-09-17
    When "U-CO-01" sets age from 90 and age to 90
    Then only "RW-2026-000301" shows, with age 90 days

  Scenario: AC11 Counts reconcile to the case list (legacy RWB-E2-011 AC11)
    When "U-TM-01" reads the count of "MTG-BKK-CO" on Team queues and the case list filtered by queue "MTG-BKK-CO" and status not "CLOSED"
    Then both show 412

  Scenario: AC12 Load time (legacy RWB-E2-011 AC12)
    Given "U-CO-01" owns 500 open cases
    When "U-CO-01" opens My queue with page size 200
    Then the first page shows within 2 seconds at the 95th percentile over 20 runs

  Scenario: AC13 A role without the right is refused with 403, never with an empty list (new, D-RCV-60)
    Given a user holds RW-WRITEOFF and no Queue and allocation right
    When the user opens My queue
    Then the system refuses the request with 403 and MSG-P4-002
    Then the answer carries the refusal and not an empty list

  Scenario: AC14 The queue read writes nothing and publishes no event (new, D-RCV-60)
    Given "MTG-BKK-CO" holds Not specified in the source documents (NEWAC-RWB-P3-E2011-APP-AC14) open cases
    When "U-TM-01" reads the count of "MTG-BKK-CO" on Team queues
    Then the count stays unchanged after the read and no event is published

  Scenario: AC15 The page size limit is read from the parameters contract, not from code (new, D-RCV-60)
    Given the parameters contract mock returns the page size maximum Not specified in the source documents (NEWAC-RWB-P3-E2011-APP-AC15)
    When the front end requests My queue with a page size above that maximum
    Then the system refuses the request with MSG-GEN-002 naming "size" and the maximum Not specified in the source documents (NEWAC-RWB-P3-E2011-APP-AC15)

  Scenario: AC16 The provided operations answer 401, 403 and 404 as the contract states (new, D-RCV-60)
    Then the system answers 401 for a request without a valid session
    Then the system answers 403 for a user without the right, as in AC13
    Then the system answers 404 for a queue outside the user's scope, as in AC7

  Scenario: AC17 A queue activity that is retried or times out ends in a stated result (new, D-RCV-60)
    Given "U-CO-01" opens My queue and the read activity is retried
    When the read activity exceeds its timeout
    Then the system ends the request with the timeout result of the contract
    Then the screen shows no partial list

  Scenario: AC18 A consumed call that fails or does not answer shows no false count (new, D-RCV-60)
    Given "MTG-BKK-CO" count is read from a consumed contract
    When the consumed call fails or does not answer
    Then the screen shows no count for the failed call and does not show zero

  Scenario: AC19 A status change the model does not allow is refused (new, D-RCV-60)
    Given case "RW-2026-000301" is owned by "U-CO-01"
    When "U-CO-01" requests a status change the model does not allow
    Then the system refuses the change and keeps the status
    Then no event is published
```

**Note.** The twelve criteria are the legacy ones word for word with their origin tag; AC13 to AC19 are new (D-RCV-60): AC13 to AC15 cover exception X7 and rules BR9 and BR10, and AC16 to AC19 cover the error answers and the failure cases; no value, no message and no count is changed by the move. The three mock Givens stand in for the answers rwb-case and the composite route take from other services: the rwb-access scope answer of AC7, the rwb-source-data freshness answer of AC8 and the rwb-deviation answer that names the deviation of a paused row in AC9. AC12 is a response-time criterion and is levelled NFR in section 16.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | My queue shows the open cases whose owner is the signed-in person; Team queues shows only the queues of the manager's teams | roles.txt default scope (Own, Team); CTL-09 |
| BR2 | Sort order: breached service level first, then running by due date earliest first, then paused, then no service level timer | REQ-WKM-001; R-UNI-30 |
| BR3 | Age is the number of calendar days from the case entry date to the business date | DF-CAS-013; labels.txt Stage clock |
| BR4 | A breach is an open case whose SERVICE_LEVEL timer has status EXPIRED | R-UNI-30; REQ-CWC-011 |
| BR5 | The open case count of a queue is its cases with status not Closed, and equals the case list count for the same queue | REQ-WKM-006; NFR-018 |
| BR6 | An owner at or above the queue's caseload cap is shown at cap | Queue field capacity_cap; DL23 (GAP-0707; ASM-1254; ASM-1232, ASM-1237, ASM-1259, ASM-1560) |
| BR7 | A timer paused by a deviation shows as paused; the prescription date keeps running | R-DEV-01; R-UNI-43 |
| BR8 | Filters are kept for the browser session only and are not stored on the server | Principle 1 (no business value stored per user) |
| BR9 | The three operations are reads of `rwb_case` rows: they write nothing, take no lock and publish no event, so a queue count never changes because a person looked at it | DP-01; Architecture v5 slide 11 |
| BR10 | The page-size default and maximum, the caps and every label are data read through the parameters and reference-data contracts or from the queue row, never values in code | DP-06; DP-07; REQ-WKM-006 |
| BR11 | The queue summary fields are computed live from `rwb_case` and the open timer of each case: openCaseCount and breachCount are integers, oldestAgeDays an integer, oldestEntryDate a date, owners[] holds ownerUserId, openCaseCount (integer) and atCap (boolean); queue_measure is read only as a reconciliation check | GAP-0708 |
| BR12 | The business date of the case data is read from GET /api/recovery/source-data/v1/data-products/freshness and cached for the request; rwb-case sets X-Data-As-Of on the two case answers and omits the header when the answer does not arrive inside the budget; the composite route fills {product} with the data product name the screen shows. The answer is `DataProductFreshness` of rwb-source-data.yaml 5.1.0: `status` is `LOADED` or `STALE` and the row is the stamp in use (the latest stamped business date); a product never stamped answers `STALE` with `businessDate` null (RD-P1-005, RD-P1-041). When businessDate is null omit X-Data-As-Of and show the stale banner. MSG-P1-001 supplies product only (no-date wording Pending, GAP-3284) | GAP-0709 |

### 9. State transitions

None. This story does not change a case status. It reads cases, queues and timers only.

| What moves the counts this view shows | Cause | What this view then shows | Owner story |
|---|---|---|---|
| The open count of a queue | CaseCreated, CaseAllocated, CaseTransferred or CaseStateChanged on `rwb.case.events.v1` | The new count, the new oldest entry date and the new per-owner spread on the next read | RWB-P3-E1018-APP; RWB-P3-E1020-APP; RWB-P3-E1021-APP |
| The breach count of a queue | The durable service level timer expires and escalates | The case moves to the first sort group and the queue counts one more breach | RWB-P3-E1028-APP |
| The service level state of a row | A deviation pauses or resumes the timer | PAUSED with the position after the running timers, then RUNNING again | RWB-P3-E1028-APP; S8 |
| The business date of the data | The ACE batch completes for a later business date | The stale banner disappears and every age is computed from the new date | rwb-source-data; RWB-P3-E1030-APP |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-CASEOWN, case owner | Opens My queue (Case record R, scope Own); reads queue rows of own queue (Queue and allocation R) |
| RW-TEAMMGR, team manager | Opens Team queues and My queue (Queue and allocation R, Case record R, scope Team) |
| RW-CAPACITY, capacity and workforce planner | Opens Team queues (Queue and allocation R, scope All) |
| RW-RESTRUCT, RW-LITOFF | Open My queue for the cases they own (Case record R) |
| RW-AUDIT, internal audit | Reads both views (R, scope All); changes nothing |
| rwb-access | Answers the role, scope and right check through its authorise contract, cached per request; it owns the role, scope and masking policy and this story owns none of them |

Reading a queue row needs no reference-data administration right: the labels arrive already resolved through the reference-data contract, and a person who may read the list may read its labels.

### 11. Data

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
| DF-WRK-045 to DF-WRK-048 | queue_member | id, queue_id, user_id, capacity | Read, for the per-owner cap when the personal capacity is the one in force (GAP-0707; ASM-1254) |
| DF-WRK-028 | timer | case_id | Read |
| DF-WRK-030 | timer | timer_type | Read |
| DF-WRK-032 | timer | expires_at | Read |
| DF-WRK-034 | timer | paused | Read |
| DF-WRK-035 | timer | status | Read |
| DF-RPT-021 to DF-RPT-030 | queue_measure | queue_id, as_of, depth, unassigned, avg_age_days, max_age_days, owner_min, owner_max, breached, status | Read only through the snapshot the queue-measure story of RWB-SVC-P3 publishes, when that snapshot reconciles to the case list (GAP-0708; ASM-1255) |
| DF-REF-132 to DF-REF-158 | parameter_catalog, parameter_value | The page-size default and maximum in force | Read, through the parameters contract |
| DF-REF-159 to DF-REF-184 | reference_version, reference_row | LOV-STAGE, LOV-ROUTE and LOV-CASE-STATUS labels and versions | Read, through the reference-data contract |

Field IDs are those in the Logical Data Model and Data Dictionary v9. Every row is a `rwb_case` row or a row read through the published contract of its owner; no foreign key and no join crosses a schema (DP-01).

### 12. Contract

#### 12.1 REST operations provided

Base `/api/recovery/case/v1`; owner rwb-case (P3). The three operations exist in the target map; this story adds to them the fields and the checks the two screens need.

| Method | Path | Purpose | Added in this story | Access |
|---|---|---|---|---|
| GET | `/cases` | List the cases in the caller's scope with filters, paging, age and service level state | The `route` filter, `sort=serviceLevelDueAt` as the default order for My queue, the computed `ageDays`, `serviceLevelDueAt` and `serviceLevelState` (BREACHED, RUNNING, PAUSED, NONE), and the `X-Data-As-Of` response header carrying the business date of the case data | Case record R, scope applied |
| GET | `/queues` | List the queues of the caller's teams with their load | The computed `openCaseCount`, `oldestEntryDate`, `oldestAgeDays`, `breachCount` and `owners[]` with `ownerUserId`, `openCaseCount` and `atCap` (GAP-0707; GAP-0708; ASM-1254; ASM-1255) | Queue and allocation R, scope applied |
| GET | `/queues/{queueId}/cases` | List the cases of one queue, sorted by service level | The scope check that answers 404 for a queue outside the caller's teams, and the same computed fields and header as `/cases` | Queue and allocation R, scope applied |

Errors for the three: 401 no session (MSG-P4-001), 403 no right (MSG-P4-002), 404 queue unknown or outside scope (MSG-P4-003), 422 age range inverted (MSG-GEN-003) or page size outside its range (MSG-GEN-002), 503 store down. Idempotency is not applicable to a read.

#### 12.2 REST operations consumed

| Method | Path | Service | Used for | Timeout |
|---|---|---|---|---|
| GET | `/api/recovery/source-data/v1/data-products/freshness` | P1 rwb-source-data | The business date of the case data, for the `X-Data-As-Of` header and the stale banner (GAP-0709; ASM-1256) | One hop, 2 s (DP-11) |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | The role, scope and right check on each of the three operations, cached per request (DP-08) | One hop, 2 s (DP-11) |

Two calls, no chain. The freshness answer is cached for the request and for the business date, so a page of rows does not ask again per row. The stage, route and status labels are read through the rwb-case reference-data contract (RWB-P3-E1043-CON, DP-07) and the page-size limits through the rwb-case parameters contract (RWB-P3-E1042-CON, DP-06) as in-process library reads of the same service, so neither is a cross-service row. The deviation code the hover of MSG-P3-004 names is composed at the edge from the rwb-deviation answer of the screen, so this story adds no deviation read to rwb-case and returns the paused state and the open flag only.

#### 12.3 Events published

None. The read path publishes nothing and writes no outbox row. The counts and the sort move only when CaseCreated, CaseAllocated, CaseTransferred, CaseStateChanged and TimerBreached are published on `rwb.case.events.v1` by their own stories, and this story subscribes to none of them.

#### 12.4 Events consumed

None. `rwb.source-data.AceDataReady.v1` moves the business date the freshness answer reports, and it is consumed by the case workflow stories on task queue `rwb-case`; this view reads the answer and subscribes to nothing. `rwb.deviation.DeviationRaised.v1` and `rwb.deviation.DeviationCleared.v1` are consumed by RWB-P3-E1028-APP to pause and resume the timer this view renders.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| CaseWorkflow | Workflow, parent, one per case, workflow ID = case ID | `rwb-case` | Holds the durable service level timer that writes the status, the pause flag and the escalation this view reads; owned by RWB-P3-E1028-APP, and this story adds no workflow and no activity to it |
| Queue summary read | Query inside the service | `rwb-case` | Groups `recovery_case` by `queue_id` and `owner_user_id`, joins the open SERVICE_LEVEL timer of each case, and orders the rows by the caller's teams |

#### 12.6 Schedules

None registered by this story. The 06:30 rebalancing Schedule (JOB-06) and the daily queue measure snapshot belong to RWB-P3-E1030-APP, and the nightly reporting copy belongs to rwb-reporting; this view registers no Schedule and reads no scheduler state.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| recovery_case | P3 (rwb_case) | The case row behind every list row: number, product group, status, stage, route, owner, queue, team, entry date and the open flag |
| queue | P3 (rwb_case) | The queue row of Team queues: code, name, team, role and cap |
| queue_member | P3 (rwb_case) | The personal capacity of an owner, when the per-owner cap in force is the personal one (GAP-0707; ASM-1254) |
| timer | P3 (rwb_case) | The open SERVICE_LEVEL timer of a case: type, due date, pause flag and status, for the sort and the breach count |
| queue_measure | P3 (rwb_case) | The reconciled snapshot of a queue, read only and only when it is in force (GAP-0708; ASM-1255) |
| outbox_event, processed_event, idempotency_key | PLT library, created in rwb_case | Not written by this read path |

No other table is named. `lov_value`, `reference_row` and `parameter_value` are read through the rwb-case contracts and never joined in SQL, and no schema other than `rwb_case` is read (DP-01, DP-06, DP-07).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-access WireMock | The P4 contract | `POST /authorise` granting Case record R and Queue and allocation R, refusing a role without the right, and refusing scope over SME-NTH for a scope Team in MTG-BKK |
| rwb-source-data WireMock | rwb-source-data.yaml 5.1.0 | On test day 2026-12-15, expected D is 2026-12-14. Offer LOADED for D, STALE for the preceding sandbox bank business day with staleSince D, and never stamped (STALE, businessDate and staleSince null). Also offer a timeout. For never stamped, omit X-Data-As-Of and show the stale banner. Assert MSG-P1-001 and product only while no-date wording is Pending (GAP-3284). |
| rwb-deviation WireMock | The S8 contract, used by the composite route and the browser test | An open X1 on the two paused cases of AC9, and an empty answer |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 3 provided, 2 consumed | Cases, queues and queue cases provided; freshness and authorise consumed; one hop, 2 s timeout, breaker per downstream |
| Kafka | None published, none consumed | The five case events that move the counts are published by their own stories; this read path carries no Kafka traffic |
| Temporal | None added | The timer that writes the status read here lives in CaseWorkflow and belongs to RWB-P3-E1028-APP |
| File | None | No file is read or written |

### 13. Solution plan

**Package.** Java package `th.co.scb.ace.workbench.recovery.case.queueview`, module `queueview`; front end folder `src/modules/recovery/case/queues`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_case`; the three answers read `recovery_case`, `queue`, `queue_member`, `timer` and `queue_measure` of this service only and never another service's tables | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and its client library: the page-size default 50 and maximum 200 are parameter rows, not constants | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case: LOV-STAGE, LOV-ROUTE and LOV-CASE-STATUS labels and versions | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-08 | RecoveryAccessGuard | Authorise contract of rwb-access and the guard library, cached per request, on each of the three operations | H RWB-PLT-E1037-CON; C RWB-P4-E1037-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/case/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.case.events.v1` and `rwb.case.<Event>.v1` through the naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in schema `rwb_case`: one index migration in this story | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route for SCR-02 and SCR-07 | H RWB-PLT-N001-CON |

DP-14 is claimed although this story publishes nothing: the topic and event names the counts depend on are resolved through the naming library, and a local topic name would leave the two screens reading a stream nobody writes. The same-service CON baselines RWB-P3-E2011-CON and RWB-P3-E1031-CON are class H dependencies and are not DP rows.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| CaseQueueController | Controller | The three read operations; parameter checks; problem responses and status codes |
| CaseListQueryService | Service | Builds the scoped case query with filters, age and the service level sort; computes `ageDays` and `serviceLevelState` |
| QueueSummaryService | Service | Counts open cases, the oldest entry date, the breaches and the open cases per owner for each queue in scope |
| CaseListRepository | Repository | One SQL query joining `recovery_case` with the open SERVICE_LEVEL `timer` of each case, in `rwb_case` only |
| QueueSummaryRepository | Repository | Grouped counts by `queue_id` and `owner_user_id`, and the cap lookup |
| CapReader | Service | Resolves the cap in force for an owner from `queue.capacity_cap` or `queue_member.capacity` (GAP-0707; ASM-1254) |
| FreshnessClient | Client | Calls the rwb-source-data freshness answer once per request and for the business date; supplies `X-Data-As-Of` |
| AccessCheckClient | Client | Calls the rwb-access authorise contract, cached per request (DP-08) |
| MyQueuePage | React component | SCR-02 in the My queue view with filters, sort and states |
| TeamQueuesPage | React component | SCR-07 with the queue rows, owner spread and drill down |
| useSessionFilters | React component | Hook that keeps filters in session storage, wrapped in try and catch, cleared at sign-out |

**Database.** Reads `recovery_case`, `queue`, `queue_member`, `timer` and `queue_measure` in schema `rwb_case`, and uses `ix_case_owner_status`, `ix_case_status_queue` and `ix_timer_case_id` where they already exist. Adds one index, `ix_timer_case_type_status` on `timer (case_id, timer_type, status)`, in its own Flyway step `V<next>__rwb_e2_011_queue_view_index.sql` (DP-15). No column is added to any table.

**Configuration and reference data.** `queueview.page-size.default` = 50 and `queueview.page-size.max` = 200 are parameter rows of `parameter_catalog` read through the parameters contract (DP-06); stage, route and status labels come from LOV-STAGE, LOV-ROUTE and LOV-CASE-STATUS through the reference-data contract (DP-07); caseload caps come from the queue row, or from the member's personal capacity when that is the cap in force (DL23; GAP-0707; ASM-1254).

**Build steps**

1. Extend the OpenAPI document and the generated types for the three operations with the added fields, the header and the paging and sort rules; contract test against RWB-P3-E2011-CON.
2. Add the index migration and `CaseListRepository` with the service level join; test the four sort groups.
3. Build `CaseListQueryService` with scope, filters, age and the computed fields; add `route` and the sort to `GET /cases`.
4. Build `QueueSummaryService`, `CapReader` and the computed fields on `GET /queues`; test the counts against `GET /cases` for the same queue.
5. Add the scope check to `GET /queues/{queueId}/cases`.
6. Build `FreshnessClient` and the `X-Data-As-Of` header with its stale state; tests for AC8.
7. Build `MyQueuePage` with Loading, Empty, List and Filtered states and `useSessionFilters`; build `TeamQueuesPage` with Loading and List states and the drill down; add the paused marker and the hover of MSG-P3-004.
8. Authorisation through the rwb-access contract on the three operations; test the refusal of AC7 and the refusal of section 16.
9. Write the API, browser and load tests of section 16.

**Feature switch.** `rwb.p3.queue-views`, a service configuration value. Off: the menu items My queue and Team queues are hidden and the three operations return the Epic 1 fields only; on: the age, the service level state, the queue counts and the owner spread.

**Done when.** Every test in section 16 passes, the three contract fakes drive every cross-service answer, a page of 200 cases for an owner with 500 open cases loads inside 2 s at the 95th percentile through the composite route (NFR-009), and the contract tests of RWB-P3-E2011-CON stay green.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-017 | The list has no case for the person and filters | There are no cases in this queue. |
| MSG-GEN-003 | Age to is less than age from | {field} cannot be before {other}. |
| MSG-GEN-002 | Page size outside 1 to 200 | {field} must be between {min} and {max}. |
| MSG-P4-003 | A queue outside the caller's scope | This case is not in your scope. |
| MSG-P1-001 | The case data is from an earlier business date | {product} is from {date}. Today's load has not arrived. |
| MSG-P3-004 | A case on hold for a deviation | This case is on hold for {deviation}. The prescription date is still {date}. |
| MSG-P4-002 | A role without the right opens a view | You cannot {action} here. Your role does not include it. |
| MSG-P4-001 | Not specified in the source documents (DOR-RWB-P3-E2011-APP-9) | Not specified in the source documents (DOR-RWB-P3-E2011-APP-9) |

MSG-P3-017 is new (see Additions). Thai text follows DL10 (open; assumptions ASM-2250, ASM-2357, ASM-2377, ASM-2863). The seven texts are the legacy texts unchanged; the move changes no wording. MSG-P4-001 is used but has no text in the sources (DOR-RWB-P3-E2011-APP-9). The `{product}` of MSG-P1-001 is filled by the composite route with the data product name the screen shows (BR12; GAP-0709).

### 15. Screens and states

| Screen | State | What the user does |
|---|---|---|
| SCR-02 Case list, My queue view | Loading | Sees skeleton rows |
| SCR-02 Case list, My queue view | Empty | Reads MSG-P3-017 |
| SCR-02 Case list, My queue view | List | Reads cases sorted by service level; opens a case on SCR-03 |
| SCR-02 Case list, My queue view | Filtered | Sets stage, route, status and age filters; clears them |
| SCR-02 Case list, My queue view | Error | Not specified in the source documents (CG-ALL-4098) |
| SCR-02 Case list, My queue view | No access | Not specified in the source documents (CG-ALL-4098) |
| SCR-03 | Loading | Not specified in the source documents (CG-ALL-4099) |
| SCR-03 | Empty | Not specified in the source documents (CG-ALL-4099) |
| SCR-03 | Error | Not specified in the source documents (CG-ALL-4099) |
| SCR-03 | No access | Not specified in the source documents (CG-ALL-4099) |
| SCR-05 Transfer case | Loading | Not specified in the source documents (CG-ALL-4100) |
| SCR-05 Transfer case | Empty | Not specified in the source documents (CG-ALL-4100) |
| SCR-05 Transfer case | Error | Not specified in the source documents (CG-ALL-4100) |
| SCR-05 Transfer case | No access | Not specified in the source documents (CG-ALL-4100) |
| SCR-07 Team queues | Loading | Sees skeleton rows |
| SCR-07 Team queues | List | Reads count, oldest age, breaches and owners against the cap; opens a queue's cases; goes to SCR-05 Transfer case (RWB-E2-012) |
| SCR-07 Team queues | Empty | Not specified in the source documents (CG-ALL-4101) |
| SCR-07 Team queues | Error | Not specified in the source documents (CG-ALL-4101) |
| SCR-07 Team queues | No access | Not specified in the source documents (CG-ALL-4101) |

The composite route that serves these states is owned by RWB-PLT-N001-CON; its path, its merge order and the screen field list are not fixed here, and this story fixes only the three answers it contributes. A stale business date shows as a banner on both screens and never blocks the list.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-011-01 | AC1, BR1, BR2, BR3 | End to end | 40 cases for U-CO-01: 3 breached, 37 running |
| TC-E2-011-02 | AC2, BR4, BR6 | End to end | Queues MTG-BKK-CO (412 cases) and MTG-BKK-LIT (38 cases) |
| TC-E2-011-03 | AC3, BR8 | End to end | 12 litigation and 28 other cases; browser session kept and ended |
| TC-E2-011-04 | AC4 | End to end | U-CO-02 with no case |
| TC-E2-011-05 | AC5 | End to end | Age from 120, age to 90 |
| TC-E2-011-06 | AC6 | End to end | Page size 500 |
| TC-E2-011-07 | AC7, BR1 | End to end | Queue SME-NTH-CO requested by a MTG-BKK manager |
| TC-E2-011-08 | AC8 | End to end | Data as of 2026-12-11 on business date 2026-12-15 |
| TC-E2-011-09 | AC9, BR7 | End to end | Two cases with X1 open and paused timers |
| TC-E2-011-10 | AC10, BR3 | End to end | Entry dates 2026-09-16 and 2026-09-17 |
| TC-E2-011-11 | AC11, BR5 | End to end | Queue count against the case list count |
| TC-E2-011-12 | AC12 | NFR | 500 cases, 20 timed runs |
| TC-E2-011-13 | AC13, Access | Component | RW-WRITEOFF (no Queue and allocation right) calls `GET /queues`; refused with MSG-P4-002 |
| TC-E2-011-14 | AC14, BR9, section 12 operations | Contract | Queue summary read and the rwb_case reads of section 12.5; count taken before and after a person opens the queue |
| TC-E2-011-15 | Section 12.7 tables; bounds Not specified in the source documents (DOR-RWB-P3-E2011-APP-12) | Boundary | Rows at the bounds of each table named in section 12.7 |
| TC-E2-011-16 | AC15, BR10 | Component | Parameters contract mock returns page size maximum Not specified in the source documents (NEWAC-RWB-P3-E2011-APP-AC15); no limit taken from code |
| TC-E2-011-17 | AC13, X7 | Contract | Role with no Case record R and no Queue and allocation R opens My queue or Team queues; refused with 403 and MSG-P4-002 |
| TC-E2-011-18 | AC16 | Contract | Request without a valid session, user without the right, queue outside scope; answers 401, 403 and 404 |
| TC-E2-011-19 | AC17 | Contract | Queue read retried and then timed out; no partial list shown |
| TC-E2-011-20 | AC18 | Contract | Consumed call fails and does not answer; no count shown |
| TC-E2-011-21 | AC19 | Component | Status change the model does not allow; status kept and no event published |
| TC-P3-E2011-APP-01 | AC8 | End to end | Fixtures of AC8 |

The legacy levels map System to End to end, Access to Component and Resilience to NFR. TC-E2-011-12 is levelled NFR here because AC12 proves the 2 s response budget at the 95th percentile rather than a business outcome. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v9.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code. Caps, page sizes, labels and list values are read from the queue table, the parameters contract and the reference-data contract, and the feature switch from service configuration.
- No personal data in logs, tests or prompts. Rows show case numbers, codes and staff user IDs; no customer name, address, identity number or contact point appears in an answer or a log line, and test data is synthetic.
- No read of another service's table. List labels come through the rwb-case reference-data contract, the business date through the rwb-source-data freshness answer, the authorisation through the rwb-access contract, and no join crosses into another schema (DP-01, DP-06, DP-07, DP-08).
- ACE data is read only through the owner's contract or the `v_ace_*` views of rwb-source-data; this story reads no ACE view at all.
- The three operations are reads: no case, queue, timer or assignment row is written, no outbox row is added and nothing is locked for the length of a page.
- One hop only: rwb-case calls the freshness answer and the authorise contract and returns; it never calls a service that calls another (ADR-020).
- Browser storage holds only the filter values and is wrapped in try and catch; the page works without it, and a cleared session clears the filters.
- Every answer carries IDs, codes, dates, counts and amounts only; the owner column is a staff user ID and not a display name.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-WKM-001 | A case owner sees their own queue with ageing and service level state | Business Requirements Epic 2, section 3.3; Program, section 5.3 | FEAT-WKM-01 | 06 Take over and own the case | R-UNI-30 | TC-E2-011-01, TC-E2-011-03 to TC-E2-011-06, TC-E2-011-08 to TC-E2-011-10, TC-E2-011-12 |
| REQ-WKM-002 | A team manager sees every queue in the team with filters | Business Requirements Epic 2, section 3.3; Program, section 5.3 | FEAT-WKM-02 | 06 Take over and own the case | R-UNI-30 | TC-E2-011-02, TC-E2-011-07, TC-E2-011-13 |
| REQ-WKM-006 | Queue counts, ageing and breaches reconcile to the case list | Business Requirements Epic 2, section 4; Program, section 5.3 | FEAT-WKM-02, FEAT-CWC-18 | 06 Take over and own the case | R-UNI-30 | TC-E2-011-02, TC-E2-011-11 |
| REQ-CWC-011 | Service levels per queue and status are held as data and a breach raises an event without moving the case; the breach count and the paused marker of this view come from that timer state | Business Requirements Epic 1, section 4; Program, section 5.3 | FEAT-WKM-01, FEAT-WKM-02 | 06 Take over and own the case | R-UNI-30 | TC-E2-011-02, TC-E2-011-09 |
| REQ-WKM-011 | Work allocated to a partner is visible in the same queue view as internal work; not served by this story, because partner placements arrive with the partner panel in Epic 6 | Business Requirements Epic 2, section 4; Program, section 5.3 | None in this story | 06 Take over and own the case | None | None |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | Not applicable to a business requirement | None | Not applicable | ADR-020 | TC-E2-011-12 |

### 19. Out of scope

- The contract baseline of the three read operations, the paging and sort rules and the fakes (RWB-P3-E2011-CON).
- The export of the case list (RWB-E1-031, RWB-P3-E1031-APP).
- Transfer and reassignment from the team queues screen (RWB-E2-012).
- Partner work in the same queue view (REQ-WKM-011, partner placements in Epic 6).
- The daily queue measures and their snapshot in Power BI (RWB-E1-030, RWB-P3-E1030-APP).
- The next action column (RWB-E2-035).
- The gateway-bff composite route and the screen field list (RWB-PLT-N001-CON).
- The deployment, the consumer groups, the dashboards and the runbook of this capability, which belong to the operations story of this legacy key.
- The cross-service journey harness and its evidence, when a journey story is raised for this legacy key.
