# RWB-P3-E1002-APP Case list v1 with case ID, owner and queue

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P3-E1002-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-case |
| Service epic | RWB-SVC-P3 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-002 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP02, DP05, DP06, DP07, DP10, DP11, DP14, DP15, DP17, DP19 |
| Parallel lane | L-P3-B |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P3 rwb-case v1.md (FR-P3-019, FR-P3-021) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-002 and reworked for rwb-case. The case list keeps its rows, its columns, its freshness line and its orphan handling; the nightly file build, the data-lake transfer and the Power BI data set are removed under DP-17, and the request-time list is served by `GET /cases` on the owner's own rows. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P3-E1002-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **team manager (RW-TEAMMGR)**, I want **one case list served by rwb-case with the case ID, the owner and the queue on every row, for every open case and its linked accounts, dated to the ACE business date it was built from**, so that **every recovery team works from one list that carries the same owner, the same queue and the same account position as ACE**.

Service facts: schema `rwb_case`, REST base `/api/recovery/case/v1`, topic `rwb.case.events.v1` with event names `rwb.case.<Event>.v1`, Temporal task queue `rwb-case` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.case`, epic `RWB-SVC-P3` (DP-14 naming rule).

- The legacy story was a nightly batch step of the P1 data engine: it joined the open cases to `v_ace_account`, wrote `case_list_row`, reconciled the count and pushed an extract file to the data lake for a Power BI data set. This story is that list as a read of its owner: `GET /api/recovery/case/v1/cases` (API-P3-001), page by page, with the scope, the filters and the header `X-Data-As-Of`.
- Three owners replace the one module: the case, its account link and the queue are `rwb_case` rows of this service (DP-01); the account number, balance, days past due, last contact, action code and data as of are `rwb-source-data`'s, read through its contract one hop with a mock (DP-05, DP-11); the composite route and the screen-model merge are `gateway-bff`'s (DP-19).
- The list is no longer a file: `case_list_row`, its unique key, the lake path, the outbound adapter and the "Case list v1" data set are removed (DP-17), the daily trigger becomes the Schedule `rwb-case-caselist-daily` (DP-10), and reporting reads the events of this service in `rwb-reporting`.
- It is a Day-1 story in lane L-P3-B with no build dependency, built against the `rwb_case` baseline schema and the fakes; the eleven legacy criteria are reworked into eleven new ones (ASM-3676) and the eleven legacy test cases are kept.

### 2. Business rationale

Each recovery team keeps its own list of accounts today, and the lists do not agree with each other or with the source. This story makes one list, served by the service that owns the case row, with the owner and the queue on every row and the account position read from the owner of ACE data rather than copied, so a manager who filters by queue sees the same owner and the same balance as the officer who opens the case.

The ownership split is the point: the case row has one owner (`rwb_case`) and the account has another (`rwb-source-data`), and neither keeps a copy of the other's value (DP-01, DP-05) — a nightly copy is what made the legacy list disagree with ACE. The freshness line is not decoration either: the list states the business date it was built from and the time it answered, so a late ALS batch shows as a stale date (AC5) rather than as a plausible but wrong list (BR3, BR5). Three rules carry the rest: a case with no owner or queue is listed with blank cells and never guessed (AC6, BR7); an account key the source answer does not hold is listed with empty amounts and goes to REC-05 (AC10, BR7); and a read stays a read — no case row, no assignment, no event and no file (BR10).

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| The `rwb_case` baseline schema exists with its login | `recovery_case`, `case_account`, `queue` and the standard record columns in schema `rwb_case`, one login for the service (DP-01, DP-02); the seed and fixtures of section 12.8 stand in for production rows until RWB-P3-E1018-APP fills them |
| The parameters are in force | `case.entry.dpd` 90 (DL16), `recon.caselist.tolerance.pct` 0.00 (assumed, DL25) and `caselist.allocation.wait.until` 07:15, read as parameter rows with their version through the rwb-case parameters contract (DP-06) |
| The reference data is in force | LOV-PRODUCT, LOV-STAGE, LOV-CASE-STATUS and LOV-ROUTE as reference rows with their version, through the rwb-case reference-data contract (DP-07) |
| The rwb-source-data contract answers the freshness and the account reads | `RWB-P1-E1015-CON` publishes the freshness resource and the account read this story consumes; it is built against its fake and never blocks (DP-05, DP-11; GAP-2228) |
| The workflow kit is installed | The Schedule and the workflow of 12.5 and 12.6 run through `RWB-PLT-E1071-CON` (DP-10) |
| The composite route exists | gateway-bff serves SCR-02 and merges the answer of this service and of rwb-source-data into the screen model (DP-19; `RWB-PLT-N001-CON`) |
| The caller holds a role with the Case record right R | The right, the scope and its default are declared on the operation and answered by the guard library, which holds no permission row of its own |
| The feature flag `rwb.p1.case-list` is on | Off, `GET /cases` answers 404 and the Schedule is paused (ASM-3682) |

The platform contracts the DP rows name are baselines pulled by the rwb-case platform stories; this story declares no build, contract, integration or external dependency of its own (ASM-3681).

### 4. Flow

1. Team manager: opens SCR-02 Case list through the gateway-bff composite route (DP-19); the screen shows the Loading state.
2. gateway-bff: calls `GET /api/recovery/case/v1/cases` with page 0 and size 50, one hop, no chaining.
3. rwb-case: the guard checks the declared Case record right R and the caller's scope, per object and per request; a role without the right is a 403 and nothing is read.
4. `CaseListQueryService`: applies the scope and the filters and reads `recovery_case`, `case_account` and `queue` in `rwb_case` only (DP-01); the page is ordered by team, queue, then case number.
5. rwb-case: asks the rwb-source-data contract twice for one page — the ALS freshness answer, and the account keys of the page — each one hop with a 2 s timeout and a breaker (DP-05, DP-11).
6. `CaseListRowMapper`: builds one row per open case with case ID, case number, product group, stage, status, owner, queue, team, route, entry date and its account keys, then the account number, total balance, days past due, last contact, action code and data as of from the source answer; an account key the answer does not hold leaves blank cells and is listed for REC-05, never guessed (AC10).
7. `CaseListRowMapper`: stamps the row's refresh time and the page's `X-Data-As-Of` from the freshness answer, and flags the page stale when the ALS batch for the date is not complete (AC3, AC5).
8. rwb-case: answers `CasePage` with `page`, `size`, `total` and the header; the read holds no lock beyond its statement and writes nothing.
9. Screen: the ten columns, the filters on team, queue and product and the refresh line; a row opens the case record of RWB-P3-E1023-APP, which is a separate route.
10. 07:15, or the configured wait time: the Schedule `rwb-case-caselist-daily` starts `CaseListDayOpen` for the business date; it reads the freshness answer once and raises MSG-P1-001 to the team manager group when the batch is late (AC5). It writes no row and changes no page content.
11. No extract file is written, no lake path is called and no report data set is refreshed by this service (DP-17; AC9).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The ALS batch for the business date is not complete | Rows carry the last complete ACE date and are marked stale; no row claims the missing date; the day-open run alerts the team manager group | MSG-P1-001 | AC5 |
| X2 | A case has no owner or no queue at the wait time | Blank owner and blank queue cells, the case is still listed, the page shows the incomplete line | None (shown on the page) | AC6 |
| X3 | A linked account key is absent from the source answer | Empty account number, balance and days past due for that row; the key is listed for REC-05; the case and the link are unchanged | None (REC-05) | AC10 |
| X4 | The rwb-source-data contract answers an error or passes 2 s | 503 with no partial page; the read is retried once with jitter; no row carries a half-filled account column | MSG-GEN-006 | AC8 |
| X5 | The same page is read twice for the same business date | The same rows in the same order, no duplicate case, the refresh time of the second read | None | AC7 |
| X6 | A caller holds no Case record right | 403, no row and no column read | MSG-P4-002 | AC11 |
| X7 | A filter value is outside its list | 422 before any case is read; the list stays as it is | MSG-GEN-007 | AC11 |
| X8 | The page size is outside 1 to 200 | 422 before any case is read | MSG-GEN-002 | AC1 |

X6 and X7 answer with a status on purpose: a value outside its list is a caller error, and a missing right is a refusal with a status — neither returns an empty page, because an empty page reads as "no work" and hides a permission problem.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Reads only `rwb_case` rows and builds against the fakes of the source-data, access and workflow contracts, so neither rwb-source-data nor rwb-access needs to exist in the development environment |
| Negotiable | Page bounds, the wait time and the list values are parameter and reference rows; the row shape and the freshness rule are fixed |
| Valuable | One list per team with owner, queue and account position, dated to the ACE batch it came from, replacing the team files and one nightly extract |
| Estimable | One query operation, one row mapper, two downstream reads, one Schedule and one workflow |
| Small | Fits in two weeks: query, mapper, page, two fakes, one Schedule |
| Testable | Every criterion has a test case in section 16; the refusals and the stale page are contract tests and the columns are component tests |

### 7. Acceptance criteria

```gherkin
Feature: Case list v1 with case ID, owner and queue

  Background:
    Given the rwb-source-data contract mock returns 28,140 accounts at 90 days past due or more with dataAsOf 2026-11-30
    Given the parameters case.entry.dpd = 90 and recon.caselist.tolerance.pct = 0.00 are in force
    Given the rwb_case seed holds open cases with their linked account keys

  Scenario: AC1 One row per open case with its case ID, owner and queue (new, D-RCV-60)
    Given rwb_case holds 28,119 open cases and 28,156 linked account keys
    Given 37 of the linked accounts are below 90 days past due
    When a caller reads GET /api/recovery/case/v1/cases with page 0 and size 200
    Then the page holds total 28,119 and each case appears once
    Then every row carries its case ID, case number, owner user ID, queue code and team code
    Then the 37 accounts below 90 days past due appear on the account list of their case and add no case row

  Scenario: AC2 Columns present (new, D-RCV-60)
    Given case "RW-2026-000123" links account "ACC0000123"
    Given the rwb-source-data contract mock returns account "ACC0000123" with account number "ACC0000123", product "MORTGAGE", total balance 1,250,000.00 and days past due 96 for 2026-11-30
    When the case list is read
    Then the row shows case number "RW-2026-000123", account number "ACC0000123", product "MORTGAGE", status "ASSIGNED", queue "MTG-BKK-CO", total balance 1,250,000.00 and days past due 96
    Then each row also holds team, business date and refresh time
    Then the page offers filters on team, queue and product
    Then the account values are the source answer for that account key and rwb-case holds no copy of them

  Scenario: AC3 Daily refresh (new, D-RCV-60)
    Given the ALS batch for 2026-11-30 completed at 05:40 and the allocation for 2026-11-30 completed at 06:52
    When the case list is read and answers at 07:12 on 2026-12-01
    Then every row carries refresh time 2026-12-01 07:12
    Then the header X-Data-As-Of is 2026-11-30
    Then the refresh line reads "Refreshed 1 Dec 2026 07:12, data as of 30 Nov 2026"

  Scenario: AC4 Last contact from the EFS history through the owner (new, D-RCV-60)
    Given the rwb-source-data contract mock returns for account "ACC0000123" last contact 2026-11-30 15:42 with action code "PTP"
    When the row of case "RW-2026-000123" is read
    Then the row shows last contact 2026-11-30 15:42 and action code "PTP"
    Then rwb-case holds neither the contact time nor the action code

  Scenario: AC5 ACE batch not complete (new, D-RCV-60)
    Given the rwb-source-data contract mock returns freshness for ALS with no COMPLETED row for 2026-11-30
    When the case list is read at 08:00
    Then the rows carry the last complete business date 2026-11-27 in X-Data-As-Of and are marked stale
    Then no row claims business date 2026-11-30
    Then the team manager group receives MSG-P1-001 "DP01 Account and arrears is from 2026-11-27. Today's ACE batch has not arrived."

  Scenario: AC6 Allocation not finished (new, D-RCV-60)
    Given case "RW-2026-000456" has no owner and no queue at 07:15
    When the case list is read
    Then the row of "RW-2026-000456" shows a blank owner and a blank queue and is still listed
    Then the page shows "Owners and queues may be incomplete for 30 Nov 2026"

  Scenario: AC7 Same page read twice (new, D-RCV-60)
    Given the list for 2026-11-30 returned 28,119 rows on the first read
    When the same read is made again for 2026-11-30
    Then the page holds total 28,119 again and no case appears twice
    Then the refresh time is the time of the second read

  Scenario: AC8 Source contract error (new, D-RCV-60)
    Given the rwb-source-data contract mock answers an error after the accounts of 40 rows are read
    When the case list is read
    Then the response is 503 with no partial page and no row carries a half-filled account column
    Then the read is retried once with jitter and the second answer is served

  Scenario: AC9 No extract file and no data lake (new, D-RCV-60)
    Given the case list for 2026-11-30 is served
    When the read completes
    Then no extract file is written and no lake path or lake credential is called
    Then the reporting read model is built by rwb-reporting from the events of rwb.case.events.v1

  Scenario: AC10 Case account without an ACE account row (new, D-RCV-60)
    Given case "RW-2026-000456" links account key "ACC0000456", which the rwb-source-data contract does not return for 2026-11-30
    When the case list is read
    Then the row for "ACC0000456" has an empty account number, total balance and days past due
    Then REC-05 of RWB-P1-E1011 lists "case_account.account_key ACC0000456" as an orphan for the data steward and the ACE team
    Then the case and its case_account link are unchanged

  Scenario: AC11 Case list access refused (new, D-RCV-60)
    Given user "u-owner-01" holds the Case record right R with scope Own and case "RW-2026-000123" is owned by "u-owner-02"
    When "u-owner-01" reads GET /api/recovery/case/v1/cases
    Then the row of "RW-2026-000123" is not returned and none of its columns is read
    Then a caller with no Case record right is refused with status 403 and MSG-P4-002
```

Every scenario is tagged `(new, D-RCV-60)`: this story owns no legacy criterion identifier, and the eleven legacy criteria AC1 to AC11 of RWB-E1-002 are reworked into these eleven, keeping the legacy values, the legacy columns and the legacy test cases (ASM-3676). Each cross-service Given carries the rwb-source-data mock and every value the legacy story attributes to ACE.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The list holds one row per open case for the business date, with its linked account keys; a linked account below the entry threshold adds no case row | REQ-RDF-007; DL17 (one case per customer per product, accounts linked) |
| BR2 | Account number, total balance, days past due, last contact, action code and data as of come from rwb-source-data by account key for the ACE business date; the Workbench holds no copy | D-RCV-35 U4; ADR-010; DP-05 |
| BR3 | The list is served only with the freshness answer of the owner of ACE data; a date that is not complete is marked stale and never presented as complete | BR-P1-014-4; MSG-P1-001 |
| BR4 | The count of accounts at or above the entry threshold is compared with the ACE count by REC-01 of RWB-P1-E1011; this story serves the rows and passes or fails no count | CTL-01; REC-01; parameter case.entry.dpd (DL16) |
| BR5 | Every row carries the business date and the refresh time, and the page carries the same date in `X-Data-As-Of` | REQ-RDF-009 (freshness); FEAT-RDF-18 |
| BR6 | The same request on unchanged data returns the same rows in the same order; no read writes or replaces a row, so a repeated read is safe | R-UNI-40 read as idempotence of a read |
| BR7 | An account key the source answer does not hold is listed with empty amounts and goes to REC-05; it is never deleted and the case is never changed by this story | BR-P1-011-3; REQ-DRI-007 |
| BR8 | Case data is read only from the rows of this service, and ACE data only through the rwb-source-data contract; no other schema is named | ADR-002; DT08; ADR-010 |
| BR9 | Last contact and action code come from the source answer for the account key, taking the row with the latest `contact_at` | RWB-E1-069; OpenAPI `GET /cases` |
| BR10 | No extract file, no data-lake transfer, no Power BI data set and no event from this service; reporting reads the case events of the owner topic | DP-17; AC9 |

### 9. State transitions

None. This story changes no case status and writes no row: it reads `recovery_case`, `case_account` and `queue`, and it changes the run state of nothing. The only states it exposes are the case statuses of LOV-CASE-STATUS and the stage codes of LOV-STAGE as rows in force; a filter value outside its list is refused before a case is read (AC11). The Schedule run of 12.5 has Temporal execution states only — RUNNING, COMPLETED, FAILED — and no case state.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-TEAMMGR, team manager | Reads the list for every queue of the team (Case record R, Team scope) |
| RW-CASEOWN, case owner | Reads the list for the cases they own (Case record R, Own scope) |
| RW-PHONECOL, RW-FIELDCOL, RW-RESTRUCT and every role with Case record R | Read the list in their scope |
| RW-BIANAL, reporting and BI analyst | Reads the list; the reporting read model itself is rwb-reporting's, fed by events (BR10) |
| RW-PLATADM, platform administrator | Pauses, resumes and triggers the Schedule (Platform administration U) |
| SY-CASEWF, case workflow identity | Runs the Schedule's workflow and its activities |
| No approval applies | The story takes no decision and records none |

The role names are read from rwb-access by the guard; no name of a person appears anywhere and the owner is a staff user reference only.

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
| DF-CAS-026 | case_account | account_key | Read |
| DF-CAS-027 | case_account | is_primary | Read |
| DF-WRK-001 | queue | id | Read |
| DF-WRK-002 | queue | queue_code | Read |
| DF-WRK-004 | queue | team_code | Read |
| DF-ACE-001 | v_ace_account (through the owner) | account_key | Read |
| DF-ACE-002 | v_ace_account (through the owner) | account_code | Read |
| DF-ACE-018 | v_ace_account (through the owner) | days_past_due | Read |
| DF-ACE-020 | v_ace_account (through the owner) | total_balance | Read |
| DF-ACE-036 | v_ace_account (through the owner) | data_as_of | Read |
| DF-ACE-109 | v_ace_efs_action (through the owner) | account_key | Read |
| DF-ACE-111 | v_ace_efs_action (through the owner) | action_code | Read |
| DF-ACE-114 | v_ace_efs_action (through the owner) | contact_at | Read |
| DF-ACE-178 | v_ace_batch_status (through the owner) | source_system | Read |
| DF-ACE-179 | v_ace_batch_status (through the owner) | business_date | Read |
| DF-ACE-186 | v_ace_batch_status (through the owner) | is_complete | Read |
| Not specified in the source documents (GAP-2228; ASM-3679) | parameter_catalog, parameter_value | `case.entry.dpd`, `recon.caselist.tolerance.pct`, `caselist.allocation.wait.until`, the page bounds | Read in process |
| Not specified in the source documents (GAP-2228; ASM-3679) | reference_row, reference_version, lov_value | LOV-PRODUCT, LOV-STAGE, LOV-CASE-STATUS, LOV-ROUTE | Read in process |

Field IDs are those in the Logical Data Model and Data Dictionary, copied from the legacy story. Every `recovery_case`, `case_account` and `queue` row is a `rwb_case` table of this service (DP-01); no view is read by this service — the ACE fields are the answer of the rwb-source-data contract (DP-05). The parameter and reference rows are read through the contracts of this same service and never joined in SQL (DP-06, DP-07). No row is written, so no field is marked Write, and `case_list_row` is not a table of this story (DP-17).

### 12. Contract

#### 12.1 REST operations provided

Base `/api/recovery/case/v1`; owner rwb-case (P3).

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| GET | `/cases` | One page of the open cases in the caller's scope, each row carrying case ID, case number, product group, stage, status, owner, queue, team, route, entry date, its account keys and the account columns of the legacy list, with `X-Data-As-Of` | Case record R, scope applied per object | Read only: the same request on unchanged data returns the same rows in the same order (BR6) |

Query: `product`, `stage`, `status`, `owner`, `queue`, `caseNo`, `ageFrom`, `ageTo`, `route`, `page`, `size` (1 to 200), `sort`. The response is `CasePage`: `items` of `CaseListRow`, `page`, `size`, `total`. `CaseListRow` adds to the `Case` schema of API-P3-001 the elements `caseId`, `accountKeys`, `accountNumber`, `totalBalance`, `daysPastDue`, `lastContactAt`, `lastActionCode`, `dataAsOf`, `refreshedAt` and `stale`, all of which are the legacy columns of the case list. `refreshedAt` is the time the read answered and `dataAsOf` the ACE business date of the freshness answer, also carried in `X-Data-As-Of` with the stale flag (ASM-3678). The schema names and the problem body are Not specified in the source documents (GAP-2228; ASM-3677).

Errors: 401 no session (MSG-P4-001); 403 no Case record right (MSG-P4-002); 422 a filter value outside its list (MSG-GEN-007) or a page size outside its bounds (MSG-GEN-002); 503 the store is down or the source-data contract does not answer inside its budget (MSG-GEN-006).

#### 12.2 REST operations consumed

One hop, no chaining; 2 s timeout and a breaker per downstream (ADR-020). Both rows are the rwb-source-data contract of RWB-P1-E1015-CON.

| Method | Path | Service | Used for | Timeout |
|---|---|---|---|---|
| GET | `/accounts/{accountKey}` | rwb-source-data (P1) | Account number, total balance, days past due, data as of and the latest contact and action code of one account key; called for the keys of the page, or with the key list where the contract publishes its batch form | One hop, 2 s, breaker, retry once with jitter |
| GET | `/data-products/freshness` | rwb-source-data (P1) | The ALS business date, its completion time and the stale flag behind `X-Data-As-Of` and the refresh line | One hop, 2 s, breaker |

The account path is the one Architecture v5 slide 10 names for the case screen, and the freshness resource is RWB-P1-E1015-CON's; whether one call carries the page's key list or one call is made per key is a contract fact of that baseline (GAP-2228; ASM-3677). The parameters and the reference rows are in-process library reads of this same service and are not rows of this table (DP-06, DP-07).

#### 12.3 Events published

None. The read writes no outbox row and publishes no event. The topic `rwb.case.events.v1` with the names `rwb.case.CaseCreated.v1`, `rwb.case.CaseAllocated.v1`, `rwb.case.CaseAllocationFailed.v1`, `rwb.case.CaseTransferred.v1`, `rwb.case.CaseStateChanged.v1`, `rwb.case.TimerBreached.v1` and the signal `rwb.case.CaseEvent.v1` belongs to the stories that own the case, allocation, transfer, state and timer behaviour under DP-14; this story adds none and the owner topic is named only as the service baseline (BR10).

#### 12.4 Events consumed

None. The page is read from the rows per request, so a case that moves is seen on the next read; no inbox row is written and no subscription is added. `rwb.source-data.AceDataReady.v1` and `rwb.source-data.AceDataLate.v1` are the trigger of the case creation and the freshness of this list, and the freshness answer of 12.2 carries the date this page states rather than a stored event.

#### 12.5 Workflows and activities

| Item | Type | Name | Queue | Purpose |
|---|---|---|---|---|
| `rwb-case-caselist-daily` → `CaseListDayOpen`, workflow ID `case-list-{businessDate}` | Workflow | `CaseListDayOpen` | `rwb-case` | Opens the list day for one business date: reads the freshness answer once, and raises the stale alert when the ALS batch is late (AC5) |
| Freshness read | Activity | `readFreshness` | `rwb-case` | The one call of 12.2 to the freshness resource, logged by id and business date only |
| Stale alert | Activity | `raiseStaleListAlert` | `rwb-case` | MSG-P1-001 to the team manager group when the date is stale |

The workflow is deterministic and holds no clock read and no I/O; the fixed workflow ID makes a repeated start of the same business date a no-op (TSD T2.4 convention, read for `rwb-case`).

#### 12.6 Schedules

| Schedule | Workflow | Cron | Zone | Note |
|---|---|---|---|---|
| `rwb-case-caselist-daily` | `CaseListDayOpen` | `0 15 7 * * ?` from the parameter `caselist.allocation.wait.until` | Asia/Bangkok | Overlap policy SKIP; a manual trigger is Platform administration U; the list itself stays a read, so the Schedule changes no row |

#### 12.7 Tables owned

| Table | Schema | Owner | Use in this story |
|---|---|---|---|
| `recovery_case` | rwb_case | rwb-case (P3) | The case row behind every list row: case number, product group, status, stage, route, owner, queue, team and entry date |
| `case_account` | rwb_case | rwb-case (P3) | The account keys of the case and the primary flag that orders the account columns |
| `queue` | rwb_case | rwb-case (P3) | The queue code and team of the owner and queue columns and of the filter values |
| `parameter_catalog`, `parameter_value` | rwb_case | rwb-case (P3) | The threshold, the tolerance, the wait time and the page bounds, read in process (DP-06) |
| `reference_row`, `reference_version`, `lov_value` | rwb_case | rwb-case (P3) | The four lists of values in force (DP-07) |

No other table is named. `case_list_row` is removed with the data lake (DP-17) and is not read here; `assignment` and `queue_member` are this service's and are not read, because the list needs the current owner on the case row; no `rwb_access` or `rwb_source_data` table is read (DP-01).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-source-data account fake | The account read of 12.2 | 28,140 accounts at 90 days past due or more for 2026-11-30; account `ACC0000123` with `MORTGAGE`, 1,250,000.00, 96 days and contact 2026-11-30 15:42 with `PTP`; no row for `ACC0000456` (AC10); an error after 40 rows (AC8) |
| rwb-source-data freshness fake | The freshness read of 12.2 | ALS complete at 05:40 for 2026-11-30; ALS with no COMPLETED row for 2026-11-30 and the last complete date 2026-11-27 (AC5) |
| rwb-access guard fake | The right and the scope of the operation | Case record R with scope Team and All; scope Own for `u-owner-01` with `RW-2026-000123` owned by `u-owner-02`; a role with no Case record right refused with MSG-P4-002 |
| RWB-PLT-E1071-CON test kit | The Schedule and the workflow of 12.5 | A test server that fires `rwb-case-caselist-daily` once for 2026-11-30 and once for a stale date |
| rwb-case seed set | This story's own test data | 28,119 open cases with 28,156 account keys, 37 accounts below 90 days, case `RW-2026-000123`, case `RW-2026-000456` with no owner and with `ACC0000456`, and the parameter and list rows in force |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 2 consumed | `GET /cases` provided; the account read and the freshness read of rwb-source-data consumed; one hop, 2 s, breaker, one retry with jitter |
| Kafka | None | No event published and none consumed (12.3, 12.4) |
| Temporal | 1 workflow, 2 activities, 1 Schedule | `CaseListDayOpen`, `readFreshness`, `raiseStaleListAlert`, `rwb-case-caselist-daily` |
| File | None | No file is written or read; the lake and the extract are removed (DP-17) |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.case`, module `caselist`, Java package `th.co.scb.ace.workbench.recovery.case.caselist`; front end `src/modules/recovery/case/caselist`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_case`; the list reads `recovery_case`, `case_account` and `queue` of this service only | none |
| DP-02 | `recovery_svc` login | One login per service; the `rwb_case` login holds grants on `rwb_case` only | none |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | The account, contact and batch columns are read through the rwb-source-data contract, not from a view | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library: threshold, tolerance, wait time, page bounds | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case: the four lists in force | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-10 | Quartz, JOB-nn | The Quartz chain step becomes the Schedule `rwb-case-caselist-daily` through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | The legacy `CaseQueryApi` and the ACE-view join become REST calls of the rwb-source-data contract with a mock, one hop, 2 s | none (C from the legacy dependency RWB-E1-069) |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.case.events.v1` and `rwb.case.<Event>.v1` from the naming library; this story publishes nothing | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in `rwb_case`: the list indexes land here | H RWB-PLT-E1044-CON |
| DP-17 | Data lake, INT-19, INT-20 | Removed: no data lake; `case_list_row`, the extract file and the Power BI data set go, and reporting reads events | none; gap GAP-2228 |
| DP-19 | Screen, ace-web | gateway-bff composite route for SCR-02 | H RWB-PLT-N001-CON |

DP-09 is not applied: the read publishes nothing. The platform CON rows above are library baselines of the service, and the four dependency rows of the metadata table stay None as the story's WP fixes them (ASM-3681).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| CaseListController | Controller | `GET /cases`; the filter and page validation; the problem responses with their message ids |
| CaseListQueryService | Service | Scope and filter predicate over `recovery_case`, `case_account` and `queue`; the stable order; the page envelope |
| CaseListRowMapper | Component | One row per case with the legacy columns, the account keys, the blanks of AC10 and the stale flag of AC5 |
| SourceDataClient | Client | The two reads of 12.2, one hop, 2 s, breaker, one retry with jitter (DP-05, DP-11) |
| AccessCheckClient | Client | The declared Case record right and the caller's scope, cached per request |
| CaseAndWorkflowRepository | Repository | Paged query on the three tables of 12.7 in `rwb_case` |
| CaseListDayOpen | Workflow | The day-open workflow of 12.5, with its two activities |
| CaseListPage | React component | SCR-02: columns, filters, refresh line, Loading, list, stale and refused states |

**Database and migrations**

- Reads `recovery_case`, `case_account` and `queue`; no row is written and no foreign key points out of `rwb_case`.
- `V012_1__case_list_index.sql` in the rwb-case Flyway sequence after the V0001 baseline (DP-15; RWB-PLT-E1044-CON): `ix_case_list_team_queue` on `recovery_case (team_code, queue_id, status)` and `ix_case_account_key` on `case_account (account_key)`. If RWB-P3-E2033-APP already lands an index on the same columns, that one is used and this migration is not created.
- The legacy key `uk_case_list_row UNIQUE (business_date)` and its replacement `UNIQUE (business_date, case_id, account_key)` are dropped with the table, which now belongs to nobody (GAP-2228; ASM-3680).

**Configuration and reference data**

- `case.entry.dpd` 90, `recon.caselist.tolerance.pct` 0.00, `caselist.allocation.wait.until` 07:15 and the page bounds 1 to 200 are parameter rows with the version in force (DL16, DL25; ASM-3679); no value is a constant.
- The lists come through the reference-data contract (DP-07); the labels follow the label standard (DL10).
- The feature flag keeps the legacy name `rwb.p1.case-list` (ASM-3682). Off: `GET /cases` answers 404 and the Schedule is paused.

**Build steps**

1. `CaseListController` and `CaseListRowMapper` against the fakes, with the 401, 403, 422 and 503 bodies; AC1, AC2.
2. `CaseListQueryService` and `CaseAndWorkflowRepository` with the scope predicate, the filters and the stable order; AC1, AC7, AC11.
3. `SourceDataClient` with the two reads, the blanks of AC10 and the stale flag of AC5; AC3, AC4, AC5, AC8, AC10.
4. `CaseListPage` with the ten columns, the filters and the five states; AC2, AC6.
5. `CaseListDayOpen`, its two activities and the Schedule wiring in the workflow kit test environment; AC5.
6. The removal check of AC9 and the 2 s check on 26,500 cases at the 95th percentile.

**Feature flag.** `rwb.p1.case-list`. Off: no list and no Schedule.

**Done when.** The tests in section 16 pass; the list answers in under 2 s at the 95th percentile on 26,500 cases in SIT; no query of this story names a schema other than `rwb_case`; no extract file, lake call or report refresh exists in the build; and AC5 is seen in the test server of the workflow kit.

### 14. Validation and messages

| ID | When | Message | Where it is produced |
|---|---|---|---|
| MSG-P1-001 | The ACE batch for the business date is not complete | DP01 Account and arrears is from 2026-11-27. Today's ACE batch has not arrived. | rwb-source-data freshness answer, surfaced here and by `raiseStaleListAlert` |
| MSG-P4-001 | No valid session | Not specified in the source documents (GAP-2228; ASM-3677) | The guard, surfaced here |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. | The guard, surfaced here |
| MSG-GEN-007 | A filter value is outside its list | Not specified in the source documents (GAP-2228; ASM-3677) | This story, before a case is read |
| MSG-GEN-002 | A page size is outside its bounds | Not specified in the source documents (GAP-2228; ASM-3677) | This story, before a case is read |
| MSG-GEN-006 | The source-data contract does not answer | Not specified in the source documents (GAP-2228; ASM-3677) | This story, on the 503 of X4 |

The texts of MSG-P1-001, MSG-P4-002 and the two owner lines are copied from the legacy story character for character and no identifier is renumbered. The refusal order is fixed: the session, the right, the filter values, the page bounds, then the cases, then the source reads; a request refused at any of the first four steps reads nothing.

### 15. Screens and states

| Screen | State | What this story supplies |
|---|---|---|
| SCR-02 Case list | Loading | Skeleton rows while the page answers |
| SCR-02 Case list | List | The ten columns with case ID, owner, queue and team, the refresh line and the page controls |
| SCR-02 Case list | Filtered | The chosen team, queue and product above the list, with a clear control |
| SCR-02 Case list | Stale | The business date of the last complete ACE data and MSG-P1-001, in place of the refresh line |
| SCR-02 Case list | Incomplete allocation | "Owners and queues may be incomplete for 30 Nov 2026" with blank owner and queue cells |
| SCR-02 Case list | Empty | A plain sentence when no case meets the filters |
| SCR-02 Case list | Refused | MSG-P4-002 on a role without the Case record right |

The route is the gateway-bff composite route of RWB-PLT-N001-CON and the layout belongs to the designer (DL31); the columns, the filter set and the states are this story's. The owner cell shows the owner user reference as the case row holds it, and the display name is not this service's to resolve.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-002-11 | AC11, BR1, access | Component | `u-owner-01` with scope Own and `RW-2026-000123` owned by `u-owner-02`; a role with no Case record right refused with 403 and MSG-P4-002 |
| TC-E1-002-01 | AC1, BR1, BR2, BR4 | Component | 28,119 open cases and 28,156 linked account keys; 37 accounts below 90 days; page 0 size 200 |
| TC-E1-002-02 | AC2, BR1 | Component | Case `RW-2026-000123`; source answer with `MORTGAGE`, 1,250,000.00 and 96 days |
| TC-E1-002-03 | AC3, BR5 | Component | ALS complete at 05:40; allocation complete at 06:52; answer at 07:12 on 2026-12-01 |
| TC-E1-002-04 | AC4, BR9 | Component | Contact 2026-11-30 15:42 with action code `PTP` for `ACC0000123` |
| TC-E1-002-05 | AC5, BR3 | Component | Freshness with no COMPLETED ALS row for 2026-11-30 and 2026-11-27 as the last complete date; the Schedule run sees the stale answer |
| TC-E1-002-06 | AC6, BR7 | Component | `RW-2026-000456` with no owner and no queue at 07:15 |
| TC-E1-002-07 | AC7, BR6 | Contract | Two identical reads of 2026-11-30; the same 28,119 rows in the same order |
| TC-E1-002-08 | AC8 | Contract | Source fake answering an error after 40 rows; 503 with no partial page, then the retried answer |
| TC-E1-002-09 | AC9, BR10 | Component | A served page; no file written, no lake path called, no report refresh |
| TC-E1-002-10 | AC10, BR7, BR2 | Component | `ACC0000456` absent from the source answer for 2026-11-30; blank cells and the REC-05 line |

The legacy level System maps to Component where the assertion is on the seeded `rwb_case` rows and the fakes, and to Contract where it is the request, the answer or the refusal of an operation. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. No identifier carries an `-ITG` suffix here: the cross-service proof with every service live is RWB-ITG-E1002-ITG.

### 17. Guardrails

- No business value in code: the threshold, the tolerance, the wait time, the page bounds and the lists are parameter and reference rows with the version in force (BR5; DP-06, DP-07).
- No personal data in logs, tests or prompts: a row carries the case number, codes, dates, amounts and a staff user reference, never a customer name, identity number, address or contact value; the test data is synthetic.
- ACE data only through the owner's contract: no view, no `v_ace_*` name and no foreign key into ACE in this service (DP-05).
- No read of another service's tables, and no other schema named by a query or a view of this story (DP-01).
- One hop at a time: rwb-case calls rwb-source-data and returns; it never calls a service that calls another (ADR-020).
- A refusal is a refusal: a role without the right is a 403 and never a thinner row or an empty page.
- No event, no workflow payload with personal data, and no file: the Schedule's history carries the business date and case identifiers only (BR10).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-RDF-007 | Case list reconciles daily to the count of accounts at 90 days past due or more, and every business key resolves to an ACE row | Epic 1, 3.1; Program, 5.1 | FEAT-RDF-18 | 06 Take over and own the case | CTL-01; REC-01; REC-05; R-UNI-34; R-UNI-40 | TC-E1-002-01, TC-E1-002-02, TC-E1-002-10 |
| REQ-RDF-009 | The list carries the business date and the refresh time (freshness) | Epic 1, 3.1; Program, 5.1 | FEAT-RDF-18 | 06 Take over and own the case | BR5; MSG-P1-001 | TC-E1-002-03, TC-E1-002-05 |
| REQ-DRI-007 | An orphan or a failed read goes to the exception queue with a task for the owner | Epic 1, 3.5; Program, 5.5 | FEAT-RDF-18 | 06 Take over and own the case | R-UNI-34; REC-05 | TC-E1-002-08, TC-E1-002-10 |

| Legacy reference | Where it is kept |
|---|---|
| The story statement, the rationale and the eight preconditions | Sections 1, 2, 3 |
| The eleven legacy criteria AC1 to AC11 and the seven exception paths X1 to X7 | Sections 5, 7, 14 |
| Business rules BR1 to BR10, the authority table and the field list | Sections 8, 10, 11 |
| The job step and the `CaseQueryApi` interface | Section 12.2 and 12.5 |
| The `case_list_row` key, the extract file, the lake path and the Power BI data set | Sections 12.7, 13, 19 (removed, DP-17) |
| Messages MSG-P1-001, MSG-P4-002 and screen SCR-02 | Sections 14, 15 |
| Legacy test set TC-E1-002-01 to TC-E1-002-11, and its integration copy RWB-ITG-E1002-ITG | Section 16 |

### 19. Out of scope

- The reconciliation itself, its checks and the results table: REC-01 and REC-05 move to rwb-source-data with JOB-04 (RWB-P1-E1011). This story serves the rows and lists the orphans; it passes or fails no count.
- The ACE batch gate, the freshness stamp and the two batch events: RWB-P1-E1015-CON and RWB-P1-E1015-APP. They are consumed through the freshness answer and never re-implemented here.
- The data lake, the outbound file adapter, the extract file, the Power BI data set "Case list v1" and its 07:30 refresh: removed under DP-17; the reporting read model is rwb-reporting's.
- The queue and owner columns with their filters and the export: RWB-P3-E1031-APP. The list with status, owner and ageing, and the queue views: RWB-P3-E2033-APP and RWB-P3-E2011-APP.
- The case record view, the account tab and the timeline: RWB-P3-E1018-APP, RWB-P3-E1023-APP and RWB-P3-E1035-APP.
- Case creation, allocation and transfer, which fill the owner, the queue and the linked accounts this list shows: RWB-P3-E1018-APP, RWB-P3-E1020-APP and RWB-P3-E1021-APP.
- The right, the scope, the permission matrix and row-level security: rwb-access through the guard, and RWB-E1-016 read as scope rather than as a Power BI filter.
- Queue measures, ageing and the daily rebalance: RWB-P3-E1030-APP.
