# RWB-P1-E1002-APP Case list v1 with case ID, owner and queue

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P1-E1002-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-source-data |
| Service epic | RWB-SVC-P1 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-002 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP02, DP05, DP06, DP07, DP10, DP11, DP14, DP15, DP17, DP19 |
| Parallel lane | L-P1-A |
| Ready to start | After RWB-P1-E1069-APP, RWB-P1-E1015-APP |
| Depends on (build) | RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1071-CON, RWB-PLT-E1047-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON, RWB-P1-E1069-APP, RWB-P1-E1015-APP |
| Contract dependencies | RWB-P3-E1042-CON, RWB-P3-E1043-CON, RWB-P3-E1018-CON, RWB-P3-E1020-CON, RWB-P2-E1007-CON |
| Integration dependencies | None |
| External dependencies | RWB-P1-E1002-OPS |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v1.md (FR-P1-014, FR-P1-015, FR-P1-016, FR-P1-017, FR-P1-018, FR-P1-019, FR-P1-020, FR-P1-021, FR-P1-022) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-002 for rwb-source-data. The story keeps the case-list build behaviour of the legacy story and moves the builder from the JOB-04 Spring Batch step and its Quartz chain into the Temporal workflow `CaseListBuildWorkflow` on task queue `rwb-source-data`, reads the case through the rwb-case case query contract and ACE data through P1's own views, writes `case_list_row` in schema `rwb_source_data`, and drops the extract file, the outbound file adapter and the Power BI data set under DP-17. Gaps GAP-0485 to GAP-0487 and their assumptions are carried in §12, §13 and §16. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **team manager (RW-TEAMMGR)**, I want **one case list with case number, account, product, stage, status, owner, queue, route, total balance and days past due for every account at 90 days past due or more, built from the open cases and the ACE account view on each ACE business date and available in Power BI**, so that **every recovery team works from one list that is dated to the ACE batch it was built from**.

The legacy story built the list as one Spring Batch step of JOB-04, chained by Quartz after JOB-03, joined in process to `CaseQueryApi` and the `recovery.v_ace_*` views, and published it as a CSV extract through the outbound file adapter to the data lake for a Power BI data set. D-RCV-60 keeps the behaviour and moves the ownership:

- **The builder becomes a workflow.** One `CaseListBuildWorkflow` per business date on task queue `rwb-source-data` in namespace `rwb-recovery`, started by `rwb.source-data.AceDataReady.v1` (published by RWB-P1-E1015-APP) and started again, only when no run for that date is open, by the `DailyCaseList` Schedule at 07:15 Asia/Bangkok (DP-10; Arch v5 slides 44 and 12). The two activities are `listEligibleAccounts`, which reads the case through the rwb-case case query contract, and `snapshot(page)`, which reads P1's own released rows and serves them in pages (Arch v5 slide 15).
- **Case data arrives by contract, not in process.** The `CaseQueryApi` java interface of RWB-E1-018 becomes the rwb-case case query and allocation contracts, called one hop with a 2 s timeout and faked from Day 1 (DP-11; C RWB-P3-E1018-CON, C RWB-P3-E1020-CON).
- **ACE data stays read-only through P1's own views.** `v_ace_account`, `v_ace_efs_action` and `v_ace_batch_status` are read by P1 only, in schema `recovery`, with no copy and no foreign key (DP-01, DP-05, DP-02).
- **The rows live in P1's own schema.** `case_list_row` is created in `rwb_source_data` by RWB-P1-E1001-APP and written here on the service's own Flyway sequence (DP-01, DP-15). The row is the daily published projection; the case list API and screen stay with rwb-case.
- **DP-17 removes the publish path.** There is no data lake, no extract file, no outbound file adapter and no Power BI data set. The released rows are read by rwb-case for the SCR-02 case list screen and by rwb-reporting for its measures, both through P1's case-list contract: `GET /case-list/dates/{businessDate}` for the released status and row count, `GET /case-list/rows` for paged rows in the section 11 column order, and `snapshot(page)` for a caller inside the namespace.
- **Names.** REST base `/api/recovery/source-data/v1`, topic `rwb.source-data.events.v1`, task queue `rwb-source-data`, namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.sourcedata` (DP-13, DP-14).

### 2. Business rationale

Each recovery team keeps its own list of accounts today, and the lists do not agree with each other or with the source. This story builds one case list each business date from the open cases and `v_ace_account`, with the account number, balance and days past due read live from ACE rather than copied. The count is checked daily against ACE by REC-01 in RWB-P1-E1011-APP, and a business key with no ACE row is listed by REC-05. It meets REQ-RDF-007 and serves the measure "case list built and released by 07:30 on 99 percent of days" (FSD P1 v3 A2.18).

**What D-RCV-60 changes.** The list, its columns, its date and its 07:15 wait are unchanged. What changes is where the list is built, who owns the row and how a reader reaches it. Built in an event-started workflow it starts the moment the ACE batch is stamped ready instead of waiting for a Quartz chain, and it can be replayed for a business date by the platform administrator through the rerun operation (DP-10, DP-11). Owned by `rwb-source-data` it sits with the only login that may read ACE, so the balance, days past due and last contact stay read-only view reads (DP-05, ADR-010). Read by contract instead of by a lake file, the released rows reach rwb-case and rwb-reporting without a second copy and without a nightly file window (DP-17).

**Why the released status survives the lake.** Publishing was never only a file transfer: it was the point at which a reconciled list became readable by a team. That gate stays. `publish_status` still moves from PENDING to HELD or RELEASED under RWB-P1-E1011-APP, the case-list date operation still answers the released status and the row count, and a date that is HELD is not served to rwb-case or rwb-reporting. What disappears is the transfer, the retry, the exception queue task and the 07:30 data set refresh, because there is no lake to transfer to (GAP-0485).

### 3. Preconditions

- RWB-P1-E1001-APP is done: `case_list_row` exists in `rwb_source_data` with the columns of section 11 and the unique key on `(business_date, case_id, account_key)`.
- RWB-P1-E1069-APP is done: the Section A views exist, including `v_ace_account`, `v_ace_efs_action` and `v_ace_batch_status`, on P1's own Flyway sequence (DP-05). `v_ace_batch_status` is a Section B view, so the freshness line and the gate stay behind their flags until RWB-ACE-001 lands (DL43).
- RWB-P1-E1015-APP is done: it stamps `data_product_load` and publishes `rwb.source-data.AceDataReady.v1`; the daily completeness gate holds the build until the ALS batch for the business date is COMPLETED.
- RWB-PLT-E1071-CON is in place: the Temporal workflow kit and the Schedule registration, on namespace `rwb-recovery` (DP-10).
- RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1047-CON, RWB-PLT-E1044-CON and RWB-PLT-N001-CON are in place: the parameters and reference-data client libraries, the topic naming library, the per-service Flyway sequence and the gateway-bff composite route (DP-06, DP-07, DP-14, DP-15, DP-19).
- The rwb-case case query, allocation, parameter and reference-data contracts are published and faked (C RWB-P3-E1018-CON, C RWB-P3-E1020-CON, C RWB-P3-E1042-CON, C RWB-P3-E1043-CON).
- Parameters are loaded through the rwb-case parameter contract: `case.entry.dpd` 90 (DL16), `recon.caselist.tolerance.pct` 0.00 (assumed, DL25), `caselist.allocation.wait.until` 07:15.
- The service login `rwb_source_data` holds SELECT on the 30 `recovery.v_ace_*` views and no privilege on `public` or on any other `rwb_*` schema (DP-02).

### 4. Flow

1. `rwb.source-data.AceDataReady.v1` arrives on `rwb.source-data.events.v1` for the business date, or the `DailyCaseList` Schedule fires at 07:15 Asia/Bangkok when the event has not arrived.
2. `CaseListBuildWorkflow` starts with workflow ID = business date; a second start for a date whose run is RUNNING returns MSG-P1-011 and starts nothing.
3. System: reads the business date and completion time of the ALS batch from `v_ace_batch_status` (source_system ALS, is_complete true) and asks the freshness stamp of DP01.
4. Activity `listEligibleAccounts`: reads the open case accounts for the business date from the rwb-case case query contract, each with its `case_id`, `case_no`, product group, stage, status, owner, queue, team, route and `account_key` (DP-11).
5. System: joins each `account_key` to `v_ace_account` for the account number (`account_code`), total balance and days past due, for the business date in `data_as_of` (DP-05).
6. System: reads the latest contact and action code per `account_key` from `v_ace_efs_action`.
7. System: reads the allocation state for the date from the rwb-case allocation contract and sets the check ALLOCATION_COMPLETE YES or NO.
8. System: replaces the `case_list_row` rows for the business date in one transaction, each with the refresh time and publish status PENDING, and counts the rows below the entry threshold.
9. RWB-P1-E1011-APP: the reconciliation compares the list with `v_ace_account` and sets the publish status of the date to HELD or RELEASED.
10. Reader: rwb-case for SCR-02 and rwb-reporting for its measures read the released date through `GET /case-list/dates/{businessDate}` and `GET /case-list/rows`, or call `snapshot(page)` inside the namespace; a HELD date answers its status and no rows.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A source the case list reads is not COMPLETED at the cut-off | The daily completeness gate of RWB-P1-E1015-APP holds the workflow; no `case_list_row` is written; the last released date stays the one that is served; the data steward and team managers are alerted | MSG-P1-001 | AC5 (RWB-ITG-E1002-ITG) |
| X2 | The allocation step has not completed by 07:15 | The list is built with the owner and queue as they are; the check ALLOCATION_COMPLETE is NO on the run | None (shown on the run record) | AC6 |
| X3 | The workflow runs again for the same business date | The rows for that date are replaced; no duplicate rows; the refresh time is the time of the rerun | None | AC7 |
| X4 | The rwb-case case query contract raises an error | The transaction rolls back; the run status is FAILED; the previous rows stay; the platform administrator restarts through the rerun operation | None (alert to the platform administrator) | AC8 |
| X5 | The publish step's transfer to the lake fails after the adapter retries | No longer reachable: there is no lake, no adapter and no transfer (DP-17). The check PUBLISHED is retained as history and answers YES when the date is RELEASED; see the Target reading of AC9 | None | AC9 |
| X6 | A case account has no `v_ace_account` row for the business date | The row is written with empty balance and days past due; REC-05 lists the key for the data steward and the ACE team; the case and the link are unchanged | None (REC-05) | AC10 (RWB-ITG-E1002-ITG) |
| X7 | A role without Platform administration R lists the case-list runs | 403 with the problem envelope and the guard-library refusal | MSG-P4-002 | AC11 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Reads cases only through the rwb-case contracts and ACE only through P1's own views; the readers of the list are other services that call this contract |
| Negotiable | The entry threshold, the tolerance and the wait time are parameters read by contract; the workflow and schedule names are fixed here under GAP-0487 |
| Valuable | One list for every team, with owner and queue, dated to the ACE batch, replacing the team files |
| Estimable | One workflow, two activities, one table, one contract, four fakes |
| Small | Can be finished in two weeks or less with its tests, once RWB-P1-E1069-APP and RWB-P1-E1015-APP are in |
| Testable | Each criterion below is one automated test on synthetic cases and a contract fake |

### 7. Acceptance criteria

```gherkin
Feature: Case list v1 with case ID, owner and queue

  Background:
    Given the business date is 2026-11-30 and v_ace_batch_status shows ALS COMPLETED for 2026-11-30
    Given the parameters case.entry.dpd = 90 and recon.caselist.tolerance.pct = 0.00 are in force

  Scenario: AC2 Columns present (legacy RWB-E1-002 AC2)
    Given the case list for 2026-11-30 is built
    When the extract file for 2026-11-30 is written
    Then each row holds case number, account number, product, stage, status, owner, queue, route, total balance and days past due, in that order
    Then each row also holds team, business date and refresh time
    Then the Power BI data set "Case list v1" offers filters on team, queue and product
    Then the row for case "RW-2026-000123" shows account "ACC0000123", product "MORTGAGE", status "ASSIGNED", queue "MTG-BKK-CO", total balance 1,250,000.00 and days past due 96, the values of v_ace_account for that account_key

  Scenario: AC6 Allocation not finished (legacy RWB-E1-002 AC6)
    Given JOB-03 for 2026-11-30 has not completed at 07:15
    Given the rwb-case allocation contract mock returns ALLOCATION_COMPLETE NO for 2026-11-30
    When the case list step starts at 07:15
    Then the system builds the list with the owner and queue as they are at 07:15
    Then the run record shows check ALLOCATION_COMPLETE NO
    Then the report shows "Owners and queues may be incomplete for 30 Nov 2026"

  Scenario: AC7 Run repeated for the same date (legacy RWB-E1-002 AC7)
    Given the case list for 2026-11-30 holds 28,156 rows
    When the platform administrator restarts the step for 2026-11-30
    Then case_list_row still holds 28,156 rows for 2026-11-30 and no case account appears twice
    Then the refresh time is the time of the rerun

  Scenario: AC8 Case interface error (legacy RWB-E1-002 AC8)
    Given CaseQueryApi raises an error after 12,000 accounts are read
    Given the rwb-case case query contract mock raises an error after 12,000 accounts
    When the case list step runs
    Then the system writes no case_list_row for 2026-11-30
    Then the run status is FAILED
    Then the rows for 2026-11-27 are unchanged

  Scenario: AC9 Transfer to the lake fails (legacy RWB-E1-002 AC9)
    Given the outbound file adapter fails all its retries for the 2026-11-30 extract file
    When the publish step runs with publish_status "RELEASED"
    Then the run shows COMPLETED with check PUBLISHED NO
    Then the transfer is in the exception queue with a task for the platform administrator

  Scenario: AC11 Case list access refused (legacy RWB-E1-002 AC11)
    Given user "u-owner-01" holds RW-CASEOWN and not Platform administration R
    When the user calls GET /admin/jobs?type=JOB-04
    Then the system refuses the call with status 403 and MSG-P4-002
```

**Target reading.** Every Given, When and Then above is the legacy line, value for value, with its origin tag. The only additions are the two mock `Given` lines, on AC6 for the rwb-case allocation contract and on AC8 for the rwb-case case query contract; no legacy line is changed or dropped. What changes is where each assertion runs:

- **AC2.** The ten columns, the three extra fields and the row values are the `case_list_row` columns DF-RPT-001 to DF-RPT-019 in `rwb_source_data`, in the order the operation `GET /case-list/rows` returns them. The legacy extract file and the Power BI data set are removed by DP-17 (GAP-0485, ASM-0677): the filters on team, queue and product are query parameters of `GET /case-list/rows`, and the data set refresh line is read as the refresh time and business date the date operation answers. Case "RW-2026-000123" is the P3 case query fake fixture and account "ACC0000123" the `v_ace_account` fixture, so every legacy value is asserted unchanged.
- **AC6.** The 07:15 wait is the `DailyCaseList` Schedule time in Asia/Bangkok; the allocation mock answers ALLOCATION_COMPLETE NO for 2026-11-30, so the workflow still builds the list and still records the check.
- **AC7.** The restart is `POST /admin/jobs/{jobId}/rerun` (API-P1-002) with an Idempotency-Key, which starts `CaseListBuildWorkflow` again for the same business date; the rows are replaced in one transaction and the count 28,156 is unchanged.
- **AC8.** The failing call is the rwb-case case query contract, which is one hop from the workflow activity; the rollback, the FAILED status and the unchanged 2026-11-27 rows are unchanged in substance.
- **AC9.** Kept as history. There is no outbound file adapter and no lake in the target (DP-17), so the transfer cannot fail: PUBLISHED answers YES when the date is RELEASED and NO when it is HELD, and the exception queue task for a failed transfer has no target. The criterion is not deleted because the check it names was a real control; it is explained in GAP-0485 and ASM-0677 and is not re-implemented.
- **AC11.** The legacy call keeps its path and parameter as written; the target operation is API-P1-001 `GET /admin/jobs` with the filter parameter `jobCode`, and the 403 with MSG-P4-002 now comes from the guard library of rwb-access, so the refusal is identical in every service.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The case list holds one row per open case and linked account for the business date | REQ-RDF-007; DL17 |
| BR2 | Account number, total balance and days past due come from `v_ace_account` by `account_key` for the ACE business date in `data_as_of`; the Workbench holds no copy | D-RCV-35 U4; ADR-010 |
| BR3 | The list is built only when the daily completeness gate of RWB-P1-E1015-APP reports the sources the case list reads COMPLETE for the business date | BR-P1-014-4; MSG-P1-001 |
| BR4 | The count of accounts at or above the entry threshold is compared with `v_ace_account` by REC-01 of RWB-P1-E1011-APP; this story builds the list and records the rows below the threshold, it does not pass or fail a count | CTL-01; REC-01; `case.entry.dpd` (DL16) |
| BR5 | The list carries the business date and the refresh time on every row | REQ-RDF-009; FEAT-RDF-18 |
| BR6 | A repeated run for the same business date replaces that date's rows | R-UNI-40 |
| BR7 | A transfer that fails after the retry limit goes to the exception queue with a task for the owner | R-UNI-34; REQ-DRI-007; no transfer exists in the target (DP-17) |
| BR8 | Case data is read only through the rwb-case contracts. ACE data is read only through `recovery.v_ace_*` views | ADR-002; DT08; ADR-010 |
| BR9 | Last contact and action code come from `v_ace_efs_action` by `account_key`, taking the row with the latest `contact_at` | RWB-E1-069; Data Tier Map |
| BR10 | A case account with no ACE row is written with empty amounts and listed by REC-05; it is never deleted and the case is never changed by this story | BR-P1-011-3 |

Where each rule lives in the target: BR1, BR5 and BR6 are answered by the table `case_list_row` in `rwb_source_data` and its unique key. BR2, BR8 and BR9 are answered by the SELECT-only login on the three views and by the boundary rule of RWB-P1-E1069-DB. BR3 and BR4 are answered by the freshness gate of RWB-P1-E1015-APP and the reconciliation of RWB-P1-E1011-APP, both unchanged. BR7 keeps its text as history: with DP-17 there is no file to fail, and the exception queue task of the legacy publish step has no target. BR10 is answered by the empty-amount row and the REC-05 break list.

### 9. State transitions

The story does not change a case status. It writes the `case_list_row` rows of the business date and moves the run state of `CaseListBuildWorkflow`, and it writes `publish_status` as PENDING only; RWB-P1-E1011-APP moves it to HELD or RELEASED.

| From | To | Trigger |
|---|---|---|
| Date absent | Rows written, publish_status PENDING | `CaseListBuildWorkflow` completes for the business date |
| Rows written, PENDING | Rows written, PENDING (replaced) | The workflow is started again for the same date; the rows are replaced and the bucket count is unchanged |
| Run RUNNING | Run COMPLETED | Both activities complete and the transaction commits |
| Run RUNNING | Run FAILED | The case query contract fails; the transaction rolls back and no row of that date changes |
| publish_status PENDING | publish_status HELD or RELEASED | REC-01 and REC-02 of RWB-P1-E1011-APP, outside this story |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| `rwb_source_data` login, the service identity | Runs the workflow and both activities; writes `case_list_row`; reads the three views |
| rwb-case, the case service | Serves the case query, allocation, parameter and reference-data contracts |
| RW-PLATADM, platform administrator | Lists the runs (Platform administration R) and restarts a run (Platform administration U) |
| RW-DATASTEW, RW-COE, RW-AUDIT, RW-COMPLY, RW-SECADM | List the runs (Platform administration R) |
| RW-BIANAL, reporting and BI analyst | Reads the released dates and rows through the case-list contract (Reporting R); the data set is no longer built from a lake file |
| RW-TEAMMGR, RW-CASEOWN, RW-PHONECOL | Read the case list on SCR-02 and on the reporting screens; row-level security by team follows RWB-P1-E1016-APP |

No approval level from the delegation of authority applies. Every "who" is a role code held as data in rwb-access and reached through its authorise contract (DP-08 is not in this story's pattern set; the guard library is used by the platform, not built here).

### 11. Data

| Field group | Entity | Fields | Read or write |
|---|---|---|---|
| Case (read through the rwb-case case query contract) | case | DF-CAS-001 id, DF-CAS-002 case_no, DF-CAS-003 product_group, DF-CAS-005 status, DF-CAS-006 stage_code, DF-CAS-008 route_code, DF-CAS-009 owner_user_id, DF-CAS-011 team_code | Read (fake) |
| Case account (read through the contract) | case_account | DF-CAS-026 account_key | Read (fake) |
| Queue (read through the contract) | queue | DF-WRK-002 queue_code | Read (fake) |
| Account and arrears | v_ace_account | DF-ACE-001 account_key, DF-ACE-002 account_code, DF-ACE-018 days_past_due, DF-ACE-020 total_balance, DF-ACE-036 data_as_of | Read (DP-05) |
| Contact | v_ace_efs_action | DF-ACE-109 account_key, DF-ACE-111 action_code, DF-ACE-114 contact_at | Read (DP-05) |
| Batch record | v_ace_batch_status | DF-ACE-178 source_system, DF-ACE-179 business_date, DF-ACE-181 completed_at, DF-ACE-186 is_complete | Read (DP-05) |
| Freshness | data_product_load | DF-OPS-001 to DF-OPS-009 | Read (written by RWB-P1-E1015-APP) |
| Case list | case_list_row | DF-RPT-001 id, DF-RPT-002 business_date, DF-RPT-003 case_id, DF-RPT-004 case_no, DF-RPT-005 account_key, DF-RPT-006 account_no, DF-RPT-007 product_group, DF-RPT-008 stage_code, DF-RPT-009 status, DF-RPT-010 owner_user_id, DF-RPT-011 queue_code, DF-RPT-012 team_code, DF-RPT-013 route_code, DF-RPT-014 total_balance, DF-RPT-015 days_past_due, DF-RPT-016 refreshed_at, DF-RPT-017 last_contact_at, DF-RPT-018 last_action_code, DF-RPT-019 publish_status | Write (PENDING only) |

Field IDs are those in the Logical Data Model and the Data Dictionary. `case_list_row` is P1's table in `rwb_source_data`; the cross-reference `case_id` is an identifier held without a foreign key, and `account_key` stays a varchar(255) business key with no foreign key to ACE (DP-01, TSD P1 v3 T3.9). The exact column widths of the paged row answer and the maximum page size are Not specified in the source documents (GAP-0486; ASM-0678).

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-source-data (P1); base `/api/recovery/source-data/v1`. The four operations and their answer shapes are fixed here (GAP-0486; ASM-0678) because no source document gives them.

| ID | Method | Path | Shape | Access |
|---|---|---|---|---|
| API-P1-001 | GET | `/admin/jobs` | `Job[]` filtered by `jobCode`, `status`, `from`, `to`; each `Job` carries the business date, the status and the checks ROWS_BELOW_ENTRY, ALLOCATION_COMPLETE and PUBLISHED | Platform administration R |
| API-P1-002 | POST | `/admin/jobs/{jobId}/rerun` | `Job`; requires the Idempotency-Key header; 409 when the date is not complete in `v_ace_batch_status` or a run for it is open | Platform administration U |
| — | GET | `/case-list/dates/{businessDate}` | The business date, the `publish_status`, the row count and `refreshed_at` | Reporting R |
| — | GET | `/case-list/rows` | Paged rows in the section 11 column order, filtered by `businessDate`, `team`, `queue` and `product`; a HELD date answers its status and no rows | Reporting R |

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| GET | `/api/recovery/case/v1/cases?businessDate=2026-11-30` | P3 rwb-case | The open case accounts with case number, product group, stage, status, owner, queue, team, route and `account_key`; faked (RWB-P3-E1018-CON) |
| GET | `/api/recovery/case/v1/queues/{queueId}/cases?businessDate=2026-11-30` | P3 rwb-case | The owner and queue as they stand and the allocation state for the date; faked (RWB-P3-E1020-CON) |
| GET | `/api/recovery/case/v1/parameters/{key}` | P3 rwb-case | `case.entry.dpd`, `recon.caselist.tolerance.pct` and `caselist.allocation.wait.until` with the version in force; faked (RWB-P3-E1042-CON) |
| GET | `/api/recovery/case/v1/reference-data/{lovCode}` | P3 rwb-case | LOV-PUBLISH-STATUS, LOV-PRODUCT and LOV-CASE-STATUS; faked (RWB-P3-E1043-CON) |

Every call is one hop with a 2 s timeout, a circuit breaker and a bulkhead (DP-11). No call is made to rwb-integration: the outbound file adapter of RWB-P2-E1007-CON is a contract dependency only, retained because the legacy publish step named it and because its removal is the DP-17 gap (GAP-0485).

#### 12.3 Events published

None. This story publishes no business event. `publish_status` becoming RELEASED is a state of the row, not an event; the readers ask the date operation. `rwb.source-data.AceDataReady.v1` and `rwb.source-data.AceDataLate.v1` on `rwb.source-data.events.v1` belong to RWB-P1-E1015-APP (DP-14).

#### 12.4 Events consumed

| Event | Topic | Owner | Starts |
|---|---|---|---|
| `rwb.source-data.AceDataReady.v1` | `rwb.source-data.events.v1` | P1 (RWB-P1-E1015-APP) | `CaseListBuildWorkflow` for the business date; the payload is IDs, codes, dates and counts only |

The consumer dedupes through `processed_event` in `rwb_source_data` (DP-09 library, created by this service's DB story).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| CaseListBuildWorkflow | Workflow, one per business date, workflow ID = business date | `rwb-source-data` | Input schema (business date, source, trigger), run record shape, search attributes BusinessDate and PublishStatus; no case data and no personal data in the payload |
| listEligibleAccounts | Activity | `rwb-source-data` | Business date in; `CaseAccountRow[]` out, one per open case account, from the rwb-case case query contract and the allocation contract |
| snapshot(page) | Activity | `rwb-source-data` | Business date and page in; the page of released `case_list_row` rows in the §11 column order out; idempotent, read only, served to rwb-case for SCR-02 and to rwb-reporting for its measures |

The activity and workflow interfaces are published in the contract jar of `rwb-source-data`; a caller imports the interface and calls the owner's task queue (Arch v5 slide 11).

#### 12.6 Schedules

| Schedule | Cadence | Documented fields | Legacy reference |
|---|---|---|---|
| DailyCaseList | Daily at 07:15 Asia/Bangkok, with `rwb.source-data.AceDataReady.v1` as the primary trigger | Schedule ID `DailyCaseList`, cadence `0 15 7 * * *` in `Asia/Bangkok`, overlap policy SKIP, catch-up window one business date, business date input | JOB-04 case list step and the `caselist.allocation.wait.until` wait of 07:15 |

The Schedule name, its 07:15 fallback and the workflow name are not given by Arch v5 or by TSD P1 (GAP-0487; ASM-0679); the 07:15 value is the legacy wait kept unchanged.

#### 12.7 Tables owned

| Table | Schema | Owner (Ownership Map) | This story |
|---|---|---|---|
| case_list_row | rwb_source_data | P1 | Read, replace the rows of one business date, write `publish_status` PENDING |
| data_product_load | rwb_source_data | P1 | Read only; the stamp is written by RWB-P1-E1015-APP |
| outbox_event, processed_event, idempotency_key | rwb_source_data | PLT library | Created in this schema; the inbox dedupes AceDataReady and the idempotency table stores the rerun response |

No other table is named and no table of another service is read (DP-01).

#### 12.8 Contract fakes

| Fake | Serves | Used for |
|---|---|---|
| rwb-case case query fake (RWB-P3-E1018-CON) | `GET /cases` | Every run and the AC8 error; the fixture carries case "RW-2026-000123" and account "ACC0000123" |
| rwb-case allocation fake (RWB-P3-E1020-CON) | `GET /queues/{queueId}/cases` | AC6: ALLOCATION_COMPLETE NO for 2026-11-30 |
| rwb-case parameters fake (RWB-P3-E1042-CON) | `GET /parameters/{key}` | `case.entry.dpd` 90, `recon.caselist.tolerance.pct` 0.00, `caselist.allocation.wait.until` 07:15 |
| rwb-case reference-data fake (RWB-P3-E1043-CON) | `GET /reference-data/{lovCode}` | LOV-PUBLISH-STATUS, LOV-PRODUCT and LOV-CASE-STATUS |

The four fakes are the only contract partners of this story; the rwb-integration outbound adapter of RWB-P2-E1007-CON is declared as a dependency but never called, because the file path it served is removed (DP-17).

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 4 operations | 4 operations | Platform administration reads and rerun; released dates and paged rows; case, allocation, parameters and reference data, one hop, 2 s |
| Kafka | None | 1 event | AceDataReady on `rwb.source-data.events.v1`; nothing published |
| Temporal | 1 workflow, 2 activities, 1 Schedule | — | CaseListBuildWorkflow, listEligibleAccounts, snapshot(page), DailyCaseList on `rwb-source-data` |
| File | None | None | **No file.** The legacy extract file, the outbound adapter and the Power BI data set are removed by DP-17 (GAP-0485) |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.sourcedata.caselist`, with the published workflow and activity types in `...sourcedata.caselist.api`. REST base `/api/recovery/source-data/v1`, schema and login `rwb_source_data`, topic `rwb.source-data.events.v1`, task queue `rwb-source-data` in namespace `rwb-recovery`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `CaseListBuildWorkflow` | Workflow (Temporal) | One run per business date: gate, `listEligibleAccounts`, join the views, replace the rows, record the checks; replay safe and idempotent on the business date |
| `ListEligibleAccountsActivity` | Activity | Calls the rwb-case case query and allocation contracts; returns one row per open case account; writes nothing |
| `SnapshotActivity` | Activity | Reads `case_list_row` of the released date and returns the page in the §11 column order for rwb-case and rwb-reporting |
| `CaseListRowRepository` | Repository | Deletes and inserts the rows of one business date in one transaction; no statement names another schema |
| `LastContactReader` | Service | Reads the latest `v_ace_efs_action` row per `account_key` |
| `CaseListContract` | Controller | API-P1-001, API-P1-002, the date operation and the paged-rows operation |
| `DailyCaseListRegistrar` | Component (workflow kit) | Registers or updates the Schedule; fails the release if the namespace rejects it |

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-02 | `recovery_svc` login | One login per service | none |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-17 | Data lake, INT-19, INT-20 | Removed (no data lake); reporting from events into rwb-reporting | none; gap if the story needs lake data |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

**Build steps**

1. Write `CaseListRowRepository` against a container database in `rwb_source_data`; test the replace of one date's rows and the unchanged 2026-11-27 rows when the transaction fails (AC7, AC8).
2. Write `ListEligibleAccountsActivity` against the four contract fakes; prove that a contract error after 12,000 accounts fails the run and writes nothing (AC8).
3. Write the join to `v_ace_account` and `v_ace_efs_action` and the empty-amount row for a case account with no ACE row (AC10 fixture, proven in RWB-ITG-E1002-ITG).
4. Write the ALLOCATION_COMPLETE check from the allocation fake and the 07:15 wait from `caselist.allocation.wait.until` (AC6).
5. Write `SnapshotActivity` and the two read operations; prove the column order, the filters and that a HELD date answers no rows (AC2).
6. Write the workflow and its dedupe on the business date, and the rerun operation with the Idempotency-Key rule (AC7).
7. Register `DailyCaseList` at 07:15 Asia/Bangkok with overlap policy SKIP and prove the event trigger and the Schedule start the same workflow once (GAP-0487).
8. Add MSG-P1-001, MSG-P1-011 and MSG-P4-002 to the message table; the texts are the legacy ones.

**Feature flag.** `rwb.p1.case-list`, from the platform flag library. Off: the workflow is not started and the date operation answers the last released date.

**Done when.** The tests in section 16 pass in DEV and SIT, `CaseListBuildWorkflow` builds 28,156 rows for a synthetic business date through the four fakes, the date and rows operations serve the released date to rwb-case and rwb-reporting, and no file, adapter or lake path exists in the deployment.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-001 | The ACE batch for the business date is not complete, list not built | {product} is from {date}. Today's ACE batch has not arrived. |
| MSG-P1-011 | A second start while a run for the date is running or complete | The {source} load for {date} is already complete or running. It was not run again. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |

The IDs and texts are the legacy ones, character for character. MSG-P4-002 is now raised by the guard library of rwb-access, so the refusal is identical in every service.

### 15. Screens and states

No Workbench screen is built in this story. The team manager reads the case list on SCR-02 Case list (Loading; empty; list; filtered), which rwb-case builds through the gateway-bff composite route (DP-19), and the reporting screens of rwb-reporting read the same released rows. The composite route and the screen field list belong to the edge and rwb-case stories; this story serves the two read operations and the `snapshot(page)` activity behind them. The filters are team, queue and product, and the header line shows the business date and the refresh time of the released date.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-002-01 | AC1, BR1, BR2, BR4 | Integration | 28,140 synthetic accounts in `v_ace_account` at 90 days past due or more; 21 exclusions; 37 case accounts below 90 (run in RWB-ITG-E1002-ITG) |
| TC-E1-002-02 | AC2, BR1 | End to end | Built list; case RW-2026-000123; the case query fake and the account fixture |
| TC-E1-002-03 | AC3, BR5 | End to end | ALS batch complete at 05:40; allocation complete at 06:52; run complete at 07:12 (run in RWB-ITG-E1002-ITG) |
| TC-E1-002-04 | AC4, BR9 | End to end | `v_ace_efs_action` PTP action with contact_at 2026-11-30 15:42 (run in RWB-ITG-E1002-ITG) |
| TC-E1-002-05 | AC5, BR3 | End to end | No COMPLETED ALS row for 2026-11-30 (run in RWB-ITG-E1002-ITG) |
| TC-E1-002-06 | AC6 | End to end | Allocation fake answers ALLOCATION_COMPLETE NO for 2026-11-30 at 07:15 |
| TC-E1-002-07 | AC7, BR6 | End to end | Rerun of a built date through API-P1-002 with an Idempotency-Key |
| TC-E1-002-08 | AC8 | Component | Case query fake raises an error after 12,000 accounts |
| TC-E1-002-09 | AC9, BR7 | End to end | Publish status RELEASED; no adapter exists, so the check answers YES and the legacy failure path is asserted as removed |
| TC-E1-002-10 | AC10, BR10 | Integration | Case account ACC0000456 with no `v_ace_account` row (run in RWB-ITG-E1002-ITG) |
| TC-E1-002-11 | AC11, Access | Component | RW-CASEOWN calls `GET /admin/jobs?type=JOB-04`; refused with MSG-P4-002 |

The 11 legacy TC IDs, their Covers and their Data are kept in legacy order and character for character, so a row still names AC1, AC3, AC4, AC5 or AC10 where the legacy named it: those five criteria sit with RWB-ITG-E1002-ITG, which runs them end to end against the real contracts. The legacy Level "System" maps to "End to end" and "Access" maps to "Component", because the access test now exercises the guard library in one component. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the entry threshold, the tolerance and the wait time are parameters read through the rwb-case parameter contract, never constants (DP-06).
- No personal data in events, workflow inputs or logs: the workflow payload holds the business date and the source; the run record holds counts; `case_list_row` holds no customer name, identity number or contact value.
- ACE data only through the owner's contract or `recovery.v_ace_*` views: the three views are read by the `rwb_source_data` login and by no other login (DP-02, DP-05).
- No cross-schema read and no cross-schema key: every statement names `rwb_source_data`; `case_id` is an identifier and `account_key` a varchar(255) business key, both without a foreign key (DP-01).
- One hop and a 2 s timeout on every call to rwb-case, with a circuit breaker and a bulkhead per downstream (DP-11).
- The workflow is idempotent on the business date: a second start for an open or complete date starts nothing and answers MSG-P1-011.
- No file, no lake path, no adapter and no data set is created or referenced at run time (DP-17).
- No production payload is copied into a fixture; every fixture is synthetic.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-RDF-007 | Case list reconciles daily to the count of accounts at 90 days past due or more in `v_ace_account`, and every business key resolves to an ACE row | Epic 1, 3.1; Program, 5.1 | FEAT-RDF-18 | 06 Take over and own the case | CTL-01; REC-01; REC-05; R-UNI-34; R-UNI-40 | TC-E1-002-01 to TC-E1-002-11 |
| REQ-RDF-009 | Every screen and API that shows source data shows its business date and freshness status | Epic 1, 3.1 | FEAT-RDF-18 | 06 Take over and own the case | BR5; T3.7 | TC-E1-002-03 |
| REQ-DRI-007 | A delivery that fails after its retry limit is parked with a task for its owner | Program, 5.1 | FEAT-RDF-18 | 06 Take over and own the case | R-UNI-34 | TC-E1-002-09 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-P1-E1069-APP | App development | H: the three views the build reads |
| RWB-P1-E1015-APP | App development | H: the freshness stamp, the gate and `AceDataReady` |
| RWB-PLT-E1071-CON | Contract | H: the workflow kit, the task queue and the Schedule registration (DP-10) |
| RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1047-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON | Contract | H: parameters, reference data, topic naming, Flyway and the composite route |
| RWB-P3-E1018-CON, RWB-P3-E1020-CON, RWB-P3-E1042-CON, RWB-P3-E1043-CON | Contract | C: the case query, allocation, parameter and reference-data contracts, faked |
| RWB-P2-E1007-CON | Contract | C: the outbound adapter the legacy publish step used; declared only, never called (DP-17) |
| RWB-P1-E1002-CON | Contract | Sibling: the contract baseline of this story, Day 1 |
| RWB-P1-E1002-OPS | DevOps | X: the deployment, the worker scaling, the Schedule registration and the alerts |
| RWB-P1-E1011-APP | App development | Writes `reconciliation_result` and moves `publish_status` to HELD or RELEASED |
| RWB-ITG-E1002-ITG | Integration | I: runs AC1, AC3, AC4, AC5 and AC10 end to end |
| RWB-P3-E1002-APP | App development | The case list API and screen side of the same legacy key |

### 19. Out of scope

- The contract baseline, its documents and its fakes (RWB-P1-E1002-CON).
- The deployment, the chart, the worker scaling, the Schedule registration and the alerts (RWB-P1-E1002-OPS).
- The reconciliation, `reconciliation_result` and the hold of the publish (RWB-P1-E1011-APP).
- The ACE batch gate, the freshness stamp and `data_product_load` writes (RWB-P1-E1015-APP).
- The case list API and the SCR-02 screen with its queue and owner filters (RWB-P3-E1002-APP).
- The Section B view `v_ace_batch_status` until RWB-ACE-001 lands (DL43).
- Row-level security by team on the reporting screens (RWB-P1-E1016-APP).
- The data lake, the extract file, the outbound file adapter, the Power BI data set and their 07:30 refresh (DP-17, GAP-0485).
- AC1, AC3, AC4, AC5 and AC10 of the legacy story, which are carried by RWB-ITG-E1002-ITG.
