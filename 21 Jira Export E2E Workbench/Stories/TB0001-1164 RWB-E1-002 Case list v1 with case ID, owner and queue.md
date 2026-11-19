# TB0001-1164 [RWB-E1-002] Case list v1 with case ID, owner and queue

| Field | Value |
|---|---|
| Jira | [TB0001-1164](https://scbjira.atlassian.net/browse/TB0001-1164) |
| Type | Story |
| Status | To Do |
| Resolution | - |
| Parent | TB0001-1162 |
| Epic link | TB0001-1162 |
| Assignee | - |
| Reporter | KRISSADA RONGRAT |
| Priority | Medium |
| Labels | - |
| Components | E2E Workbench |
| Fix versions | - |
| Affects versions | - |
| Sprint | Design - Pre-analyze |
| Team | RWB_SQ2 |
| Created | 2026-11-05T12:37:05.590+0700 |
| Updated | 2026-11-18T17:22:59.715+0700 |
| Due date | - |
| Resolved | - |
| Original estimate | - |
| Remaining estimate | - |
| Time spent | - |
| Votes | 0 |
| Watchers | 1 |
| Comments | 0 |

## Description

As a team manager (RW-TEAMMGR), I want one case list with case number, account, product, stage, status, owner, queue, route, total balance and days past due for every account at 90 days past due or more, refreshed each working day and available in Power BI, so that every recovery team works from one list.

## Acceptance criteria

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

## Comments (0)

(none)

## Other Jira fields

| Field | ID | Value |
|---|---|---|
| App Owner | customfield_10188 | - |
| App Owner (migrated 3) | customfield_11031 | - |
| Approver2 | customfield_11586 | Nuttakorn Leeviravanich |
| AR: Atlassian-TemplateO | customfield_11656 | emaile,role |
| AR: Atlassian_Template | customfield_11654 | \|\|Full Name \|\| Email \|\| Role \|\| Company \|\| \|{Full Name}\|{Email}\|{Role}\|{Company}\| \|\|\|\| |
| BI Status | customfield_10169 | To be Confirmed |
| Build % | customfield_12531 | 0% |
| Bulk Backlog Detail Uploaded | customfield_11628 | No |
| CCB Status | customfield_10228 | New |
| Created Date | customfield_10249 | 2026-11-05 |
| Customer Impact | customfield_10246 | No |
| CX Status | customfield_10217 | To be Confirmed |
| Defect Re-Opened? | customfield_10619 | No |
| Defect Re-Opened? (Checkbox) | customfield_10174 | No |
| Demand type | customfield_10244 | Project |
| Demand types(Migrated on 29 Mar 2024) | customfield_11926 | Incident |
| Deploy Status | customfield_10170 | Initial |
| DGO Approval | customfield_10113 | Pending |
| DPO Approval | customfield_10122 | Pending |
| Epic Type | customfield_10275 | Project |
| Epic Type OLD | customfield_10052 | Project |
| Execution Method | customfield_10240 | Manual |
| Grooming Status | customfield_10212 | Not Started |
| Grooming Status (migrated) | customfield_10649 | Not Started |
| Has been Approved | customfield_10232 | No |
| Independent Story | customfield_10101 | No |
| Is Required Downtime | customfield_10245 | N |
| Is Required Downtime | customfield_11847 | N |
| Issue Priority | customfield_10102 | Medium |
| IT Risk Approval | customfield_10133 | Pending |
| Logs / Description | customfield_11491 | Log: xxxx URL: xxxx |
| Penetration Test Status | customfield_10183 | Not Started |
| Penetration Test Status (migrated) | customfield_10654 | Not Started |
| Priority | customfield_10610 | Medium |
| QbD Status OLD | customfield_10050 | Not Required |
| Regulatory Related | customfield_10260 | No |
| Regulatory Status | customfield_10201 | No Issues |
| Regulatory Status (migrated) | customfield_10647 | No Issues |
| Release Confirmation | customfield_10637 | Not Confirmed Internal |
| Release Confirmation (API) | customfield_10200 | Not Confirmed Internal |
| Requirement Status | customfield_10207 | Not Completed |
| Root Cause | customfield_12535 | Unknown |
| SAT Process | customfield_10274 | PENDING |
| SAT Status(Migrated) | customfield_12360 | Not Start |
| SD Required | customfield_10257 | no |
| Segment | customfield_10193 | Retail |
| Severity | customfield_10168 | 3 - Medium |
| Severity (migrated) | customfield_10597 | 3 - Medium |
| SIT retest failure tracking | customfield_15014 | 0.0 |
| SIT Shakedown Status | customfield_10189 | Not Started |
| Solution Remark (Nonstd) | customfield_10216 | To be Confirmed |
| Solution Status | customfield_10640 | To be Confirmed |
| Squad Estimation Status | customfield_10229 | Estimation In Progress |
| Target Fix Date Adjustment Flag | customfield_15017 | No |
| Test Cases Review | customfield_10150 | In-progress |
| Testing environment | customfield_15163 | Non-Aging |
| Toggle Flag | customfield_11588 | No Toggle Flag |
| Training Material Status | customfield_10176 | Not Started |
| UAT Estimation Status | customfield_10234 | Estimation In Progress |
| UAT Execution By | customfield_13554 | UAT Team |
| UAT Execution By | customfield_10237 | Squad Team |
| UAT Owner | customfield_10184 | KANRUTHAI ASAVAROONGPAISAL |
| UAT retest failure tracking | customfield_15015 | 0.0 |
| UAT Shakedown Status | customfield_10194 | Not Started |
