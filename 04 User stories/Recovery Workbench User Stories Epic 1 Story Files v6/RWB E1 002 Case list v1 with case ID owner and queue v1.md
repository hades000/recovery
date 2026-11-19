# RWB-E1-002 Case list v1 with case ID, owner and queue

SCB Collections and Recovery. Henka Group, 15 November 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E1-002 |
| Epic | E1, release 30 November 2026 |
| Module | P1 Recovery data engine |
| Feature | FEAT-RDF-18 Show the case list with case ID, owner and queue |
| Requirement IDs | REQ-RDF-007 |
| BRD section | Business Requirements Epic 1, section 3.1; Business Requirements Program, section 5.1 |
| L3 process | 06 Take over and own the case |
| Decision | D6 entry; D-RCV-35 (U1, U4); ADR-010 |
| Priority | Must |
| Depends on | RWB-E1-018, RWB-E1-020, RWB-E1-069, RWB-E1-007, RWB-E1-015 |
| Status | Ready for build |

## 1. Story

As a **team manager (RW-TEAMMGR)**, I want **one case list with case number, account, product, stage, status, owner, queue, route, total balance and days past due for every account at 90 days past due or more, built from the open cases and the ACE account view on each ACE business date and available in Power BI**, so that **every recovery team works from one list that is dated to the ACE batch it was built from**.

## 2. Business rationale

Each recovery team keeps its own list of accounts today, and the lists do not agree with each other or with the source. This story builds one case list each business date from the open cases and `v_ace_account`, with the account number, balance and days past due read live from ACE rather than copied, and publishes it to Power BI. The count is checked daily against ACE by REC-01 in RWB-E1-011, and a business key with no ACE row is listed by REC-05. It meets REQ-RDF-007 and serves the measure "case list built and released by 07:30 on 99 percent of days".

## 3. Preconditions

- RWB-E1-018 is done: open cases exist with their linked accounts, and P3 publishes `CaseQueryApi` with `account_key` as the account link.
- RWB-E1-020 is done: JOB-03 morning allocation sets the owner and the queue.
- RWB-E1-069 is done: the Section A views exist, including `v_ace_account`, `v_ace_efs_action` and `v_ace_batch_status`. `v_ace_batch_status` is a Section B view, so the freshness line and the gate stay behind their flags until RWB-ACE-001 lands (DL43).
- RWB-E1-015 is done: the daily completeness gate holds JOB-04 until the ALS batch for the business date is COMPLETED.
- RWB-E1-007 is done: the outbound file adapter writes files to the data lake (INT-19).
- Parameters are loaded: `case.entry.dpd` 90 (DL16), `recon.caselist.tolerance.pct` 0.00 (assumed, DL25), `caselist.allocation.wait.until` 07:15.
- The reporting and BI analyst (RW-BIANAL) has built the Power BI data set "Case list v1" on the lake file and scheduled its refresh at 07:30.
- JOB-04 runs as the recovery service identity (recovery_svc), which holds SELECT on `recovery.v_ace_*` and no privilege on `public`.

## 4. Flow

1. Quartz: JOB-04 Daily reconciliation reaches its case list step after JOB-03 completes for the business date, and only when the daily completeness gate of RWB-E1-015 reports COMPLETE for the sources the case list reads.
2. System: reads the business date and completion time of the ALS batch from `v_ace_batch_status` (source_system ALS, is_complete true).
3. System: reads the open case accounts from `CaseQueryApi.openCaseAccounts(businessDate)`, each with its `account_key`.
4. System: joins each account_key to `v_ace_account` for the account number (`account_code`), total balance and days past due, for the business date in `data_as_of`.
5. System: reads the latest contact and action code per account_key from `v_ace_efs_action`.
6. System: replaces the case_list_row rows for the business date in one transaction, each with the refresh time and publish status PENDING.
7. System: counts the rows below the entry threshold and records the count on the run for information; the reconciliation itself is REC-01 of RWB-E1-011.
8. RWB-E1-011: the reconciliation step compares the list with `v_ace_account` and sets the publish status of the date to HELD or RELEASED.
9. System: the publish step sends the extract file for the business date to the data lake through the outbound file adapter only when the publish status is RELEASED.
10. Power BI: refreshes the data set at 07:30; the report shows the ten columns, the filters, the refresh time and the ACE business date.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A source the case list reads is not COMPLETED at the cut-off | The daily completeness gate of RWB-E1-015 holds the step; no case_list_row is written; the lake keeps the last released list; the data steward and team managers are alerted | MSG-P1-001 | AC5 |
| X2 | JOB-03 has not completed by 07:15 | The list is built with the owner and queue as they are; the check ALLOCATION_COMPLETE is NO on the run | None (shown on the report) | AC6 |
| X3 | The step runs again for the same business date | The rows for that date are replaced; no duplicate rows | None | AC7 |
| X4 | `CaseQueryApi` raises an error | The transaction rolls back; the run status is FAILED; the previous rows stay; the platform administrator restarts the step | None (alert to the platform administrator) | AC8 |
| X5 | The publish step's transfer to the lake fails after the adapter retries | The run is COMPLETED with check PUBLISHED NO; the transfer goes to the exception queue with a task for the platform administrator | None (R-UNI-34) | AC9 |
| X6 | A case account has no `v_ace_account` row for the business date | The row is written with empty balance and days past due; REC-05 lists the key for the data steward and the ACE team; the case and the link are unchanged | None (REC-05) | AC10 |
| X7 | A role without Platform administration R lists the case list runs | 403 | MSG-P4-002 | TC-E1-002-11 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Reads cases only through the P3 published interface and accounts only through `v_ace_account`; the Power BI report is built by the BI analyst |
| Negotiable | The entry threshold, the tolerance and the wait time are parameters |
| Valuable | One list for every team, with owner and queue, dated to the ACE batch, replacing the team files |
| Estimable | One batch step, one table, one extract file, one join to the ACE view |
| Small | Can be finished in two weeks or less with its tests |
| Testable | Each criterion below is one automated test on synthetic cases |

## 7. Acceptance criteria

```gherkin
Feature: Case list v1 with case ID, owner and queue

  Background:
    Given the business date is 2026-11-30 and v_ace_batch_status shows ALS COMPLETED for 2026-11-30
    Given the parameters case.entry.dpd = 90 and recon.caselist.tolerance.pct = 0.00 are in force

  Scenario: AC1 List built and reconciled
    Given v_ace_account holds 28,140 accounts at 90 days past due or more with data_as_of 2026-11-30
    Given P3 excluded 21 of them at entry, so the ACE count to match is 28,119
    Given the open cases link 28,119 accounts at 90 days past due or more and 37 accounts below 90 days past due
    When the case list step of JOB-04 runs
    Then case_list_row holds 28,156 rows for 2026-11-30
    Then REC-01 of RWB-E1-011 compares 28,119 with 28,119 and is PASS
    Then the run record shows 37 rows below 90 days past due

  Scenario: AC2 Columns present
    Given the case list for 2026-11-30 is built
    When the extract file for 2026-11-30 is written
    Then each row holds case number, account number, product, stage, status, owner, queue, route, total balance and days past due, in that order
    Then each row also holds team, business date and refresh time
    Then the Power BI data set "Case list v1" offers filters on team, queue and product
    Then the row for case "RW-2026-000123" shows account "ACC0000123", product "MORTGAGE", status "ASSIGNED", queue "MTG-BKK-CO", total balance 1,250,000.00 and days past due 96, the values of v_ace_account for that account_key

  Scenario: AC3 Daily refresh
    Given the ALS batch for 2026-11-30 completed at 05:40 and JOB-03 completed at 06:52
    When the case list step runs and completes at 07:12
    Then every row for 2026-11-30 carries refresh time 2026-12-01 07:12
    Then the report after the 07:30 data set refresh shows "Refreshed 1 Dec 2026 07:12, data as of 30 Nov 2026"

  Scenario: AC4 Last contact from EFS through ACE
    Given v_ace_efs_action holds an action "PTP" for an account of case "RW-2026-000123" with contact_at 2026-11-30 15:42
    When the case list step runs
    Then the row of case "RW-2026-000123" shows last contact 2026-11-30 15:42 and action code "PTP"

  Scenario: AC5 ACE batch not complete
    Given v_ace_batch_status shows no COMPLETED ALS row for 2026-11-30 at 08:00
    When the DP01 cut-off passes and JOB-04 is triggered
    Then the daily completeness gate holds the step and no case_list_row for 2026-11-30 is written
    Then the lake keeps the extract file for 2026-11-27
    Then the team manager group receives MSG-P1-001 "DP01 Account and arrears is from 2026-11-27. Today's ACE batch has not arrived."

  Scenario: AC6 Allocation not finished
    Given JOB-03 for 2026-11-30 has not completed at 07:15
    When the case list step starts at 07:15
    Then the system builds the list with the owner and queue as they are at 07:15
    Then the run record shows check ALLOCATION_COMPLETE NO
    Then the report shows "Owners and queues may be incomplete for 30 Nov 2026"

  Scenario: AC7 Run repeated for the same date
    Given the case list for 2026-11-30 holds 28,156 rows
    When the platform administrator restarts the step for 2026-11-30
    Then case_list_row still holds 28,156 rows for 2026-11-30 and no case account appears twice
    Then the refresh time is the time of the rerun

  Scenario: AC8 Case interface error
    Given CaseQueryApi raises an error after 12,000 accounts are read
    When the case list step runs
    Then the system writes no case_list_row for 2026-11-30
    Then the run status is FAILED
    Then the rows for 2026-11-27 are unchanged

  Scenario: AC9 Transfer to the lake fails
    Given the outbound file adapter fails all its retries for the 2026-11-30 extract file
    When the publish step runs with publish_status "RELEASED"
    Then the run shows COMPLETED with check PUBLISHED NO
    Then the transfer is in the exception queue with a task for the platform administrator

  Scenario: AC10 Case account without an ACE account row
    Given case "RW-2026-000456" links account_key "ACC0000456", which has no v_ace_account row for 2026-11-30
    When the case list step runs
    Then the row for "ACC0000456" has an empty account number, total balance and days past due
    Then REC-05 of RWB-E1-011 lists "case_account.account_key ACC0000456" as an orphan for the data steward and the ACE team
    Then the case and its case_account link are unchanged

  Scenario: AC11 Case list access refused
    Given user "u-owner-01" holds RW-CASEOWN and not Platform administration R
    When the user calls GET /admin/jobs?type=JOB-04
    Then the system refuses the call with status 403 and MSG-P4-002
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The case list holds one row per open case and linked account for the business date | REQ-RDF-007; DL17 (one case per customer per product, accounts linked) |
| BR2 | Account number, total balance and days past due come from `v_ace_account` by `account_key` for the ACE business date in `data_as_of`; the Workbench holds no copy | D-RCV-35 U4; ADR-010 |
| BR3 | The list is built only when the daily completeness gate of RWB-E1-015 reports the sources the case list reads COMPLETE for the business date | BR-P1-014-4; MSG-P1-001 |
| BR4 | The count of accounts at or above the entry threshold is compared with `v_ace_account` by REC-01 of RWB-E1-011; this step builds the list and records the rows below the threshold, it does not pass or fail a count | CTL-01; REC-01; parameter case.entry.dpd (DL16) |
| BR5 | The list carries the business date and the refresh time on every row | REQ-RDF-009 (freshness); FEAT-RDF-18 |
| BR6 | A repeated step for the same business date replaces that date's rows | R-UNI-40 |
| BR7 | A file that fails after the retry limit goes to the exception queue with a task for the owner | R-UNI-34; REQ-DRI-007 |
| BR8 | Case data is read only through the P3 published interface. ACE data is read only through `recovery.v_ace_*` views | ADR-002; DT08; ADR-010 |
| BR9 | Last contact and action code come from `v_ace_efs_action` by `account_key`, taking the row with the latest `contact_at` | RWB-E1-069; Data Tier Map |
| BR10 | A case account with no ACE row is written with empty amounts and listed by REC-05; it is never deleted and the case is never changed by this story | BR-P1-011-3 |

## 9. State transitions

None. This story does not change a case status. It writes the case_list_row rows of the business date and the run state of the JOB-04 case list step (RUNNING to COMPLETED or FAILED); it does not write a publish status beyond PENDING, which RWB-E1-011 sets to HELD or RELEASED.

## 10. Authority

| Who | What they may do in this story |
|---|---|
| recovery_svc, recovery service identity | Runs the case list step; writes case_list_row and reads the ACE views |
| SY-CASEWF, case workflow module | Serves `CaseQueryApi` |
| RW-PLATADM, platform administrator | Lists the runs (Platform administration R) and restarts the step (Platform administration U) |
| RW-DATASTEW, RW-COE, RW-AUDIT, RW-COMPLY, RW-SECADM | List the runs (Platform administration R) |
| RW-BIANAL, reporting and BI analyst | Builds and schedules the Power BI data set (Reporting CRUD) |
| RW-TEAMMGR, RW-CASEOWN, RW-PHONECOL | Read the case list report in Power BI (Reporting R); row-level security by team follows RWB-E1-016 |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | recovery_case | id | Read (through CaseQueryApi) |
| DF-CAS-002 | recovery_case | case_no | Read (through CaseQueryApi) |
| DF-CAS-003 | recovery_case | product_group | Read (through CaseQueryApi) |
| DF-CAS-005 | recovery_case | status | Read (through CaseQueryApi) |
| DF-CAS-006 | recovery_case | stage_code | Read (through CaseQueryApi) |
| DF-CAS-008 | recovery_case | route_code | Read (through CaseQueryApi) |
| DF-CAS-009 | recovery_case | owner_user_id | Read (through CaseQueryApi) |
| DF-CAS-011 | recovery_case | team_code | Read (through CaseQueryApi) |
| DF-CAS-026 | case_account | account_key | Read (through CaseQueryApi) |
| DF-WRK-002 | queue | queue_code | Read (through CaseQueryApi) |
| DF-ACE-001 | v_ace_account | account_key | Read |
| DF-ACE-002 | v_ace_account | account_code | Read |
| DF-ACE-018 | v_ace_account | days_past_due | Read |
| DF-ACE-020 | v_ace_account | total_balance | Read |
| DF-ACE-036 | v_ace_account | data_as_of | Read |
| DF-ACE-109 | v_ace_efs_action | account_key | Read |
| DF-ACE-111 | v_ace_efs_action | action_code | Read |
| DF-ACE-114 | v_ace_efs_action | contact_at | Read |
| DF-ACE-178 | v_ace_batch_status | source_system | Read |
| DF-ACE-179 | v_ace_batch_status | business_date | Read |
| DF-ACE-181 | v_ace_batch_status | completed_at | Read |
| DF-ACE-186 | v_ace_batch_status | is_complete | Read |
| DF-RPT-001 | case_list_row | id | Write |
| DF-RPT-002 | case_list_row | business_date | Write |
| DF-RPT-003 | case_list_row | case_id | Write |
| DF-RPT-004 | case_list_row | case_no | Write |
| DF-RPT-005 | case_list_row | account_key | Write |
| DF-RPT-006 | case_list_row | account_no | Write |
| DF-RPT-007 | case_list_row | product_group | Write |
| DF-RPT-008 | case_list_row | stage_code | Write |
| DF-RPT-009 | case_list_row | status | Write |
| DF-RPT-010 | case_list_row | owner_user_id | Write |
| DF-RPT-011 | case_list_row | queue_code | Write |
| DF-RPT-012 | case_list_row | team_code | Write |
| DF-RPT-013 | case_list_row | route_code | Write |
| DF-RPT-014 | case_list_row | total_balance | Write |
| DF-RPT-015 | case_list_row | days_past_due | Write |
| DF-RPT-016 | case_list_row | refreshed_at | Write |
| DF-RPT-017 | case_list_row | last_contact_at | Write |
| DF-RPT-018 | case_list_row | last_action_code | Write |
| DF-RPT-019 | case_list_row | publish_status | Write (PENDING) |

Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

**Job step**

| Item | Value |
|---|---|
| Trigger | JOB-04 Daily reconciliation, case list step, chained after JOB-03 completes, or at 07:15 if JOB-03 has not completed; only when the daily completeness gate of RWB-E1-015 returns COMPLETE for the sources it reads |
| Job name | JOB-04 Daily reconciliation |
| Input | `CaseQueryApi.openCaseAccounts(businessDate)`; `v_ace_account`; `v_ace_efs_action`; `v_ace_batch_status`; parameters |
| Output | case_list_row for the business date; check results ROWS_BELOW_ENTRY (count), ALLOCATION_COMPLETE (YES or NO), PUBLISHED (YES or NO); extract file `case-list/<businessDate>.csv` held for the publish step and sent to the data lake through the outbound adapter (INT-19) when publish_status is RELEASED |
| Events published | None |
| Idempotency key | business_date; the step deletes and inserts the rows of that date in one transaction |
| Restart | A FAILED step is restarted by the platform administrator from the scheduler console with the business date; it runs in full again and replaces the date's rows |

**Published interface used** (P3, from RWB-E1-018)

```java
public interface CaseQueryApi {
    Stream<OpenCaseAccountView> openCaseAccounts(LocalDate businessDate);
    long excludedAccountCount(LocalDate businessDate);
}

public record OpenCaseAccountView(UUID caseId, String caseNo, String accountKey, String productGroup,
        String stageCode, String status, UUID ownerUserId, String queueCode, String teamCode, String routeCode) {}
```

**GET /admin/jobs** (API-P1-001), with `type=JOB-04`

| Item | Value |
|---|---|
| Response 200 | `Job[]` with checks ROWS_BELOW_ENTRY (count), ALLOCATION_COMPLETE (YES or NO), PUBLISHED (YES or NO) |
| 401, 403, 503 | MSG-P4-001; MSG-P4-002; database unavailable |
| Authorization | Platform administration R |
| Idempotency | Read only |

The step start is guarded by the `business_date` key: a second trigger for a date whose run is RUNNING returns MSG-P1-011 and starts nothing.

## 13. Solution plan

**Package.** Folder `recovery/dataengine/caselist`, Java package `recovery.dataengine.caselist`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| CaseListStepConfig | Job (Spring Batch step in JOB-04) | Reads open case accounts, joins the ACE views, writes rows, records the below-threshold count |
| CaseListChainListener | Listener (Quartz job listener) | Starts the step when JOB-03 completes for the business date, or at the wait time, and only on a COMPLETE gate result |
| CaseListRow | Entity | Maps case_list_row |
| CaseListRowRepository | Repository | Deletes and inserts the rows of one business date |
| CaseListExtractWriter | Service | Writes the CSV extract and hands it to the outbound file adapter |
| LastContactReader | Service | Reads the latest `v_ace_efs_action` row per account_key |
| DailyCompletenessGate (from RWB-E1-015) | Published interface | Returns COMPLETE or HOLD for the business date |
| LoadAlertNotifier | Service | Sends MSG-P1-001 through the ACE notification path |
| RecoveryDataEngineController | Controller (job listing) | Lists the run through GET /admin/jobs |

**Database.** No new table: V0001 (RWB-E1-001) creates case_list_row with the columns in section 11. Physical Schema v5 declares `uk_case_list_row UNIQUE (business_date)`, which would allow one row per date and contradicts BR1; the next free migration replaces it with `UNIQUE (business_date, case_id, account_key)` and adds index `(business_date, team_code, queue_code)`. Reads `v_ace_account` and `v_ace_efs_action` by `account_key`; no foreign key into ACE.

**Configuration and reference data.** Parameters `case.entry.dpd`, `recon.caselist.tolerance.pct` and `caselist.allocation.wait.until` from the parameter catalog, loaded by the center of excellence analyst. Lake path and alert recipient groups as configuration, set by the platform administrator. The Power BI data set and its 07:30 schedule are owned by the reporting and BI analyst.

**Build steps**

1. Write the key migration, CaseListRow and CaseListRowRepository; test the replace of one date's rows.
2. Write a contract test against `CaseQueryApi` with a stub of synthetic cases and their `account_key`.
3. Write CaseListStepConfig: read, join `v_ace_account` and `v_ace_efs_action`, write in one transaction; write the orphan row with empty amounts.
4. Write the below-threshold count and the ALLOCATION_COMPLETE check.
5. Write the gate call and the HOLD path.
6. Write CaseListChainListener with the wait time.
7. Write CaseListExtractWriter with the column order and the adapter hand-off; test the PUBLISHED check when the adapter fails.
8. Add the JOB-04 step to the job listing.

**Feature flag.** `rwb.p1.case-list`. Off: JOB-04 skips the case list step.

**Done when.** The tests in section 16 pass, and the Power BI data set "Case list v1" refreshes in SIT from the extract file.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-001 | The ACE batch for the business date is not complete, list not built | {product} is from {date}. Today's ACE batch has not arrived. |
| MSG-P1-011 | A second trigger while a run for the date is running | The {source} load for {date} is already complete or running. It was not run again. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |

## 15. Screens and states

No Workbench screen in this story. The team manager reads the Power BI report "Case list v1" with the ten columns, the filters on team, queue and product, and the refresh line. The Workbench case list screen SCR-02 is built by P3 (RWB-E1-031).

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-002-01 | AC1, BR1, BR2, BR4 | System | 28,140 synthetic accounts in v_ace_account at 90 days past due or more; 21 exclusions; 37 case accounts below 90 |
| TC-E1-002-02 | AC2, BR1 | System | Built list; case RW-2026-000123 |
| TC-E1-002-03 | AC3, BR5 | System | ALS batch complete at 05:40; JOB-03 complete at 06:52; step complete at 07:12 |
| TC-E1-002-04 | AC4, BR9 | System | v_ace_efs_action PTP action with contact_at 2026-11-30 15:42 |
| TC-E1-002-05 | AC5, BR3 | System | No COMPLETED ALS row for 2026-11-30 |
| TC-E1-002-06 | AC6 | System | JOB-03 not complete at 07:15 |
| TC-E1-002-07 | AC7, BR6 | System | Restart of a built date |
| TC-E1-002-08 | AC8 | System | Stub interface error after 12,000 accounts |
| TC-E1-002-09 | AC9, BR7 | System | Outbound adapter forced to fail |
| TC-E1-002-10 | AC10, BR10 | System | Case account ACC0000456 with no v_ace_account row |
| TC-E1-002-11 | AC11, Access | Access | RW-CASEOWN calls GET /admin/jobs?type=JOB-04; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: the threshold, the tolerance and the wait time are parameters.
- No personal data in logs, tests or prompts. The list holds no customer name, ID number or contact value.
- No read of another module's tables. recovery_case, case_account and queue are read only through `CaseQueryApi`.
- ACE data only through `recovery.v_ace_*` views; the step holds no copy of an account and no foreign key into ACE.
- The extract file goes to the data lake only through the outbound file adapter.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-RDF-007 | Case list reconciles daily to the count of accounts at 90 days past due or more in v_ace_account, and every business key resolves to an ACE row | Epic 1, 3.1; Program, 5.1 | FEAT-RDF-18 | 06 Take over and own the case | CTL-01; REC-01; REC-05; R-UNI-34; R-UNI-40 | TC-E1-002-01 to TC-E1-002-11 |

## 19. Out of scope

- The reconciliation by product, the balance reconciliation, the break list and the hold of the publish (RWB-E1-011).
- The ACE batch gate and the freshness stamp (RWB-E1-015).
- The Workbench case list screen with queue and owner filters and export (RWB-E1-031).
- Row-level security by team in Power BI (RWB-E1-016).
- Queue measures and ageing (RWB-E1-030).
