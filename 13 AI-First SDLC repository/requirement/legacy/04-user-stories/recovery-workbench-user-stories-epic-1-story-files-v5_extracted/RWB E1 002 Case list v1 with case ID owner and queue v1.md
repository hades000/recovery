<!-- source: 04 User stories/Recovery Workbench User Stories Epic 1 Story Files v5.zip!RWB E1 002 Case list v1 with case ID owner and queue v1.md -->
<!-- converted: 2026-11-04 from Markdown (extracted) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 1 Story Files v5.zip!RWB E1 002 Case list v1 with case ID owner and queue v1.md`  
> **Converted from:** Markdown (extracted)

# RWB-E1-002 Case list v1 with case ID, owner and queue

SCB Collections and Recovery. Henka Group, 28 October 2026.

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
| Decision | D6 entry |
| Priority | Must |
| Depends on | RWB-E1-018, RWB-E1-003, RWB-E1-007, RWB-E1-020 |
| Status | Ready for build |

## 1. Story

As a **team manager (RW-TEAMMGR)**, I want **one case list with case number, account, product, stage, status, owner, queue, route, total balance and days past due for every account at 90 days past due or more, refreshed each working day and available in Power BI**, so that **every recovery team works from one list**.

## 2. Business rationale

Each recovery team keeps its own list of accounts today, and the lists do not agree with each other or with ALS. This story builds one case list each working day from the open cases and the account and arrears data product, checks its count against the ALS count of accounts at 90 days past due or more, and publishes it to Power BI. It meets REQ-RDF-007 (the case list reconciles daily to the ALS count, DL25) and serves the measure "loads on time and complete on 99 percent of days".

## 3. Preconditions

- RWB-E1-018 is done: open cases exist with their linked accounts, and P3 publishes `CaseQueryApi`.
- RWB-E1-020 is done: JOB-03 morning allocation sets the owner and the queue.
- RWB-E1-003 is done: the INT-01 load for the business date is COMPLETED, as `LoadRunQuery` reports.
- RWB-E1-007 is done: the outbound file adapter writes files to the data lake (INT-19).
- Parameters are loaded: `case.entry.dpd` 90 (DL16), `recon.caselist.tolerance.pct` 0.00 (assumed, DL25), `caselist.allocation.wait.until` 07:15.
- The reporting and BI analyst (RW-BIANAL) has built the Power BI data set "Case list v1" on the lake file and scheduled its refresh at 07:30.
- JOB-04 runs as service identity SY-DATALOAD.

## 4. Flow

1. Quartz: JOB-04 Daily reconciliation reaches its case list step after JOB-03 completes for the business date.
2. System: checks through `LoadRunQuery.completedLoad("INT-01", businessDate)` that the account load for the business date is COMPLETED.
3. System: opens a load_run row with job code JOB-04 and product DP03.
4. System: reads the open case accounts from `CaseQueryApi.openCaseAccounts(businessDate)`.
5. System: joins each account to loan_account for account number, total balance and days past due.
6. System: replaces the case_list_row rows for the business date in one transaction, each with the refresh time.
7. System: counts the case list rows at or above 90 days past due and compares the count with the ALS count of accounts at or above 90 days past due, less the accounts P3 excluded at entry.
8. System: writes the count check result to the load_run and alerts the data steward and the team managers if the difference is above the tolerance.
9. System: writes the extract file for the business date to the data lake through the outbound file adapter.
10. Power BI: refreshes the data set at 07:30; the report shows the ten columns, the filters and the refresh time.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The count of rows differs from the ALS count by more than the tolerance | The list is built and published; the load_run check COUNT is FAIL; the data steward and team managers are alerted | MSG-P1-012 | AC4 |
| X2 | The INT-01 load for the business date is not COMPLETED | The step does not run; the previous list stays in the lake | MSG-P1-001 | AC5 |
| X3 | JOB-03 has not completed by 07:15 | The list is built with the owner and queue as they are; the check ALLOCATION_COMPLETE is NO on the run | None (shown on the report) | AC6 |
| X4 | The step runs again for the same business date | The rows for that date are replaced; no duplicate rows | None | AC7 |
| X5 | `CaseQueryApi` raises an error | The transaction rolls back; status FAILED; the previous rows stay; the platform administrator reruns | None (alert to the platform administrator) | AC8 |
| X6 | The file transfer to the lake fails after the adapter retries | The run is COMPLETED in the Workbench; the transfer goes to the exception queue with a task for the platform administrator | None (R-UNI-34) | AC9 |
| X7 | A case account has no loan_account row | The row is written with empty balance and days past due and counted as an exception | None (dq_exception, check CL-01) | AC10 |
| X8 | A role without Platform administration R lists the case list runs | 403 | MSG-P4-002 | TC-E1-002-11 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Reads cases only through the P3 published interface and accounts from its own table; the Power BI report is built by the BI analyst |
| Negotiable | The entry threshold, the tolerance and the wait time are parameters |
| Valuable | One list for every team, with owner and queue, replacing the team files |
| Estimable | One batch step, one table, one extract file, one count check |
| Small | Can be finished in two weeks or less with its tests |
| Testable | Each criterion below is one automated test on synthetic cases |

## 7. Acceptance criteria

```gherkin
Feature: Case list v1 with case ID, owner and queue

  Background:
    Given the business date is 2026-11-30 and DP01 is loaded for 2026-11-30
    Given the parameters case.entry.dpd = 90 and recon.caselist.tolerance.pct = 0.00 are in force

  Scenario: AC1 List reconciles
    Given loan_account holds 28,140 accounts at 90 days past due or more for 2026-11-30
    Given P3 excluded 21 of them at entry, so the ALS count to match is 28,119
    Given the open cases link 28,119 accounts at 90 days past due or more and 37 accounts below 90 days past due
    When the case list step of JOB-04 runs
    Then case_list_row holds 28,156 rows for 2026-11-30
    Then the count check compares 28,119 with 28,119 and the load_run check COUNT is PASS
    Then the check results show 37 rows below 90 days past due

  Scenario: AC2 Columns present
    Given the case list for 2026-11-30 is built
    When the extract file for 2026-11-30 is written
    Then each row holds case number, account number, product, stage, status, owner, queue, route, total balance and days past due, in that order
    Then each row also holds team, business date and refresh time
    Then the Power BI data set "Case list v1" offers filters on team, queue and product
    Then the row for case "RW-2026-000123" shows account "ACC0000123", product "MORTGAGE", status "ASSIGNED", queue "MTG-BKK-CO", total balance 1,250,000.00 and days past due 96

  Scenario: AC3 Daily refresh
    Given the 07:00 loads are complete and JOB-03 completed at 06:52
    When the case list step runs and completes at 07:12
    Then every row for 2026-11-30 carries refresh time 2026-12-01 07:12
    Then the report after the 07:30 data set refresh shows "Refreshed 1 Dec 2026 07:12, data as of 30 Nov 2026"

  Scenario: AC4 Count outside the tolerance
    Given the ALS count to match is 28,119 and the open cases link 28,094 accounts at 90 days past due or more
    When the case list step runs
    Then the system builds the list and published with 28,094 rows at or above 90 days past due
    Then the load_run check COUNT is FAIL with a difference of 25 accounts, 0.09 percent
    Then the data steward and team manager groups receive MSG-P1-012 "The case list for 2026-11-30 does not reconcile to ALS for all products: a difference of 25 accounts, 0.09 percent."

  Scenario: AC5 Account data not loaded
    Given the INT-01 load for 2026-11-30 was refused and is not COMPLETED
    When JOB-04 reaches the case list step
    Then the step does not run and no case_list_row for 2026-11-30 is written
    Then the lake keeps the extract file for 2026-11-27
    Then the load_run for the step shows status REFUSED with failed check "INT-01 not complete"
    Then the team manager group receives MSG-P1-001 "DP01 Account and arrears is from 2026-11-27. Today's load has not arrived."

  Scenario: AC6 Allocation not finished
    Given JOB-03 for 2026-11-30 has not completed at 07:15
    When the case list step starts at 07:15
    Then the system builds the list with the owner and queue as they are at 07:15
    Then the load_run check ALLOCATION_COMPLETE is NO
    Then the report shows "Owners and queues may be incomplete for 30 Nov 2026"

  Scenario: AC7 Run repeated for the same date
    Given the case list for 2026-11-30 holds 28,156 rows
    When the platform administrator reruns the step for 2026-11-30
    Then case_list_row still holds 28,156 rows for 2026-11-30 and no case account appears twice
    Then the refresh time is the time of the rerun

  Scenario: AC8 Case interface error
    Given CaseQueryApi raises an error after 12,000 accounts are read
    When the case list step runs
    Then the system writes no case_list_row for 2026-11-30
    Then the load_run status is FAILED
    Then the rows for 2026-11-27 are unchanged

  Scenario: AC9 Transfer to the lake fails
    Given the outbound file adapter fails all its retries for the 2026-11-30 extract file
    When the case list step completes
    Then the system completes the load_run status with check PUBLISHED = NO
    Then the transfer is in the exception queue with a task for the platform administrator

  Scenario: AC10 Case account without account data
    Given case "RW-2026-000456" links account "ACC0000456", which has no loan_account row
    When the case list step runs
    Then the row for "ACC0000456" has an empty total balance and days past due
    Then the system writes one dq_exception row with check code "CL-01" and record key "ACC0000456"
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The case list holds one row per open case and linked account for the business date | REQ-RDF-007; DL17 (one case per customer per product, accounts linked) |
| BR2 | The ALS count to match is the accounts at or above the entry threshold in loan_account, less the accounts excluded at entry | CTL-01; REC-01; parameter case.entry.dpd (DL16) |
| BR3 | The count check passes when the difference is within the tolerance | Parameter recon.caselist.tolerance.pct, 0.00 assumed (DL25) |
| BR4 | The list is built only when the INT-01 load for the business date is COMPLETED | BR1 of RWB-E1-003; MSG-P1-001 |
| BR5 | The list carries the business date and the refresh time on every row | REQ-RDF-009 (freshness); FEAT-RDF-18 |
| BR6 | A repeated step for the same business date replaces that date's rows | R-UNI-40 |
| BR7 | A file that fails after the retry limit goes to the exception queue with a task for the owner | R-UNI-34; REQ-DRI-007 |
| BR8 | Case data is read only through the P3 published interface | ADR-002; DT08 |

## 9. State transitions

None. This story does not change a case status. It writes the load_run status for the case list step (RUNNING to COMPLETED, REFUSED or FAILED) and the case_list_row rows of the business date.

## 10. Authority

| Who | What they may do in this story |
|---|---|
| SY-DATALOAD, data load from COLLINS | Runs the case list step; writes case_list_row, load_run and dq_exception |
| SY-CASEWF, case workflow module | Serves `CaseQueryApi` |
| RW-PLATADM, platform administrator | Lists the runs (Platform administration R) and reruns the step (Platform administration U) |
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
| DF-CAS-026 | case_account | account_id | Read (through CaseQueryApi) |
| DF-WRK-002 | queue | queue_code | Read (through CaseQueryApi) |
| DF-ACC-001 | loan_account | id | Read |
| DF-ACC-002 | loan_account | account_no | Read |
| DF-ACC-012 | loan_account | total_balance | Read |
| DF-ACC-014 | loan_account | days_past_due | Read |
| DF-ACC-021 | loan_account | data_as_of | Read |
| DF-RPT-001 | case_list_row | id | Write |
| DF-RPT-002 | case_list_row | business_date | Write |
| DF-RPT-003 | case_list_row | case_id | Write |
| DF-RPT-004 | case_list_row | case_no | Write |
| DF-RPT-005 | case_list_row | account_id | Write |
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
| DF-OPS-023 | load_run | job_code | Write |
| DF-OPS-024 | load_run | product_code | Write |
| DF-OPS-025 | load_run | business_date | Write |
| DF-OPS-026 | load_run | status | Write |
| DF-OPS-034 | load_run | check_results | Write |
| DF-OPS-044 | dq_exception | check_code | Write |
| DF-OPS-045 | dq_exception | record_key | Write |
| DF-OPS-048 | dq_exception | raised_on | Write |
| DF-OPS-022 | load_run | interface_id | Read through LoadRunQuery (INT-01) |
| DF-OPS-025 | load_run | business_date | Read through LoadRunQuery (INT-01) |
| DF-OPS-026 | load_run | status | Read through LoadRunQuery (INT-01) |

Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

**Job step**

| Item | Value |
|---|---|
| Trigger | JOB-04 Daily reconciliation, case list step; chained after JOB-03 completes, or at 07:15 if JOB-03 has not completed |
| Job name | JOB-04 Daily reconciliation |
| Input | `CaseQueryApi.openCaseAccounts(businessDate)`, `CaseQueryApi.excludedAccountCount(businessDate)`, loan_account, `LoadRunQuery` (INT-01) |
| Output | case_list_row for the business date; load_run with checks COUNT, BELOW_ENTRY, ALLOCATION_COMPLETE, PUBLISHED; extract file `case-list/<businessDate>.csv` to the data lake through the outbound adapter (INT-19) |
| Events published | None |
| Idempotency key | business_date; the step deletes and inserts the rows of that date in one transaction |
| Restart | A FAILED step is rerun by POST /admin/jobs/{jobId}/rerun; it runs in full again |

**Published interface used** (P3, from RWB-E1-018)

```java
public interface CaseQueryApi {
    Stream<OpenCaseAccountView> openCaseAccounts(LocalDate businessDate);
    long excludedAccountCount(LocalDate businessDate);
}

public record OpenCaseAccountView(UUID caseId, String caseNo, UUID accountId, String productGroup,
        String stageCode, String status, UUID ownerUserId, String queueCode, String teamCode, String routeCode) {}
```

**GET /admin/jobs** (API-P1-001), with `type=JOB-04`

| Item | Value |
|---|---|
| Response 200 | `Job[]` with checks COUNT (PASS or FAIL with the difference), BELOW_ENTRY (count), ALLOCATION_COMPLETE (YES or NO), PUBLISHED (YES or NO) |
| 401, 403, 503 | MSG-P4-001; MSG-P4-002; database unavailable |
| Authorization | Platform administration R |
| Idempotency | Read only |

**POST /admin/jobs/{jobId}/rerun** (API-P1-002) reruns the step for the run's business date; Platform administration U; Idempotency-Key header; 409 with MSG-P1-011 while a run for that date is RUNNING.

## 13. Solution plan

**Package.** Folder `recovery/dataengine/caselist`, Java package `recovery.dataengine.caselist`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| CaseListStepConfig | Job (Spring Batch step in JOB-04) | Reads open case accounts, joins accounts, writes rows, runs the count check |
| CaseListChainListener | Listener (Quartz job listener) | Starts the step when JOB-03 completes for the business date, or at the wait time |
| CaseListRow | Entity | Maps case_list_row |
| CaseListRowRepository | Repository | Deletes and inserts the rows of one business date |
| CaseListCountCheck | Service | Computes the ALS count to match and compares it within the tolerance |
| CaseListExtractWriter | Service | Writes the CSV extract and hands it to the outbound file adapter |
| LoadAlertNotifier | Service (from RWB-E1-003) | Sends MSG-P1-012 |
| RecoveryDataEngineController | Controller (from RWB-E1-003) | Lists and reruns the step through the job endpoints |

**Database.** Migration `V1_002__case_list_row.sql` creates case_list_row with the columns in section 11 (case_no varchar(18), account_no varchar(20), product_group varchar(15), stage_code varchar(20), status varchar(20), queue_code varchar(30), team_code varchar(20), route_code varchar(4), total_balance numeric(18,2), days_past_due integer, refreshed_at timestamptz) and the standard columns, with `uk_case_list_row UNIQUE (business_date, case_id, account_id)` and an index on (business_date, team_code, queue_code). Reads loan_account by id.

**Configuration and reference data.** Parameters `case.entry.dpd`, `recon.caselist.tolerance.pct` and `caselist.allocation.wait.until` from the parameter catalog, loaded by the center of excellence analyst. Lake path and alert recipient groups as configuration, set by the platform administrator. The Power BI data set and its 07:30 schedule are owned by the reporting and BI analyst.

**Build steps**

1. Write migration V1_002, CaseListRow and CaseListRowRepository; test the replace of one date's rows.
2. Write a contract test against `CaseQueryApi` with a stub of synthetic cases.
3. Write CaseListStepConfig: read, join to loan_account, write in one transaction; write CL-01 exceptions for accounts with no loan_account row.
4. Write CaseListCountCheck with the exclusion count and the tolerance; unit test the boundary at the tolerance.
5. Write the INT-01 completion check and the REFUSED run record.
6. Write CaseListChainListener with the wait time and the ALLOCATION_COMPLETE check.
7. Write CaseListExtractWriter with the column order and the adapter hand-off; test the PUBLISHED check when the adapter fails.
8. Add the JOB-04 step to the job listing and the rerun endpoint.

**Feature flag.** `rwb.p1.case-list`. Off: JOB-04 skips the case list step.

**Done when.** The tests in section 16 pass, and the Power BI data set "Case list v1" refreshes in SIT from the extract file.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-012 | Count difference above the tolerance | The case list for {date} does not reconcile to ALS for {product}: a difference of {variance} accounts, {pct} percent. |
| MSG-P1-001 | INT-01 not complete, list not refreshed | {product} is from {date}. Today's load has not arrived. |
| MSG-P1-011 | Rerun while a run for the date is running | The {source} load for {date} is already complete or running. It was not run again. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |

## 15. Screens and states

No Workbench screen in this story. The team manager reads the Power BI report "Case list v1" with the ten columns, the filters on team, queue and product, and the refresh line. The Workbench case list screen SCR-02 is built by P3 (RWB-E1-031).

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-002-01 | AC1, BR1, BR2, BR3 | System | 28,140 synthetic accounts at 90 days past due or more; 21 exclusions; 37 case accounts below 90 |
| TC-E1-002-02 | AC2, BR1 | System | Built list; case RW-2026-000123 |
| TC-E1-002-03 | AC3, BR5 | System | JOB-03 complete at 06:52; step complete at 07:12 |
| TC-E1-002-04 | AC4, BR3 | System | 28,094 against 28,119 |
| TC-E1-002-05 | AC5, BR4 | System | INT-01 load for 2026-11-30 refused |
| TC-E1-002-06 | AC6 | System | JOB-03 not complete at 07:15 |
| TC-E1-002-07 | AC7, BR6 | System | Rerun of a built date |
| TC-E1-002-08 | AC8 | System | Stub interface error after 12,000 accounts |
| TC-E1-002-09 | AC9, BR7 | System | Outbound adapter forced to fail |
| TC-E1-002-10 | AC10 | System | Case account ACC0000456 with no loan_account row |
| TC-E1-002-11 | Access | Access | RW-CASEOWN calls GET /admin/jobs?type=JOB-04; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: the threshold, the tolerance and the wait time are parameters.
- No personal data in logs, tests or prompts. The list holds no customer name, ID number or contact value.
- No read of another module's tables. recovery_case, case_account and queue are read only through `CaseQueryApi`.
- The extract file goes to the data lake only through the outbound file adapter.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-RDF-007 | Case list reconciles daily to the ALS count at 90 days past due or more | Epic 1, 3.1; Program, 5.1 | FEAT-RDF-18 | 06 Take over and own the case | CTL-01; REC-01; R-UNI-34; R-UNI-40 | TC-E1-002-01 to TC-E1-002-11 |

## 19. Out of scope

- The reconciliation by product, the balance reconciliation, the red and green report and the hold of the publish (RWB-E1-011).
- The latest contact per case on the list (RWB-E1-004).
- The Workbench case list screen with queue and owner filters and export (RWB-E1-031).
- Row-level security by team in Power BI (RWB-E1-016).
- Queue measures and ageing (RWB-E1-030).
