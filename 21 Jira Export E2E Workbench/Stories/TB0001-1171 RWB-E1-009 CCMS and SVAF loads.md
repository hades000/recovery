# TB0001-1171 [RWB-E1-009] CCMS and SVAF loads

| Field | Value |
|---|---|
| Jira | [TB0001-1171](https://scbjira.atlassian.net/browse/TB0001-1171) |
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
| Sprint | - |
| Team | - |
| Created | 2026-11-05T12:37:11.873+0700 |
| Updated | 2026-11-18T17:17:55.454+0700 |
| Due date | - |
| Resolved | - |
| Original estimate | - |
| Remaining estimate | - |
| Time spent | - |
| Votes | 0 |
| Watchers | 1 |
| Comments | 0 |

## Description

As a data steward and data product owner (RW-DATASTEW), I want collateral records from CCMS and appraisals from SVAF loaded from their weekly files and linked to the loan accounts, so that the collateral and asset data product DP06 is current without anyone looking the values up in CCMS or SVAF.

## Acceptance criteria

```gherkin
Feature: CCMS and SVAF loads

  Background:
    Given the CCMS and SVAF files for business date 2026-11-27 are due on Monday 2026-11-30 at 04:00
    Given the parameter appraisal.max.age = 365 is in force

  Scenario: AC1 Daily load of the weekly files
    Given the adapter has passed the CCMS file with 31,200 collateral records and 33,050 account links, and the SVAF file with 2,140 appraisals
    When JOB-09 calls the CCMS and SVAF loaders at 04:00
    Then collateral holds 31,200 rows from the file and account_collateral holds 33,050 links to loan_account rows
    Then valuation holds 2,140 appraisals written through ValuationRecordApi, each linked to its collateral
    Then the system stores an appraisal date "15/03/2569" in the file as 2026-03-15
    Then both load_runs show status COMPLETED and FreshnessQuery returns DP06 with business date 2026-11-27

  Scenario: AC2 Sample matches
    Given both loads for 2026-11-27 are complete
    When the sample check picks 50 cases at random that have collateral
    Then for all 50 the collateral type, the title deed number and the latest appraised value equal the CCMS and SVAF file values after mapping
    Then the INT-11 load_run check results show "SAMPLE" = "50 of 50"

  Scenario: AC3 Appraisal age
    Given appraisal "APR-0045521" has appraisal date 2025-11-26, which is 366 days before 2026-11-27
    Given appraisal "APR-0045522" has appraisal date 2025-11-27, which is 365 days before 2026-11-27
    When the SVAF loader runs
    Then the system stores "APR-0045521" with stale_flag true and age_days 366
    Then the system stores "APR-0045522" with stale_flag false and age_days 365

  Scenario: AC4 CCMS file refused by the adapter
    Given the adapter refuses the CCMS file for 2026-11-27 at DQ-059 control total
    When JOB-09 runs
    Then the system does not call the CCMS loader and no collateral or account_collateral row changes
    Then the SVAF loader is still called, and appraisals for collateral not yet in DP06 are held with check code "DQ-068"

  Scenario: AC5 Links to unknown accounts within the tolerance
    Given 120 of the 33,050 account links name an account key not in loan_account, which is 0.36 percent
    When the CCMS loader runs
    Then the system writes 32,930 links
    Then the system writes 120 dq_exception rows with check code "DQ-061" and the account key

  Scenario: AC6 Appraisal for an unknown collateral
    Given 4 appraisals name collateral numbers not in collateral
    When the SVAF loader runs
    Then the system holds the 4 appraisals in dq_exception with check code "DQ-068"
    Then the system writes 2,136 appraisals

  Scenario: AC7 Collateral type missing from the code map
    Given 2 CCMS records carry collateral type code "K7", which is not in the code map for LOV-COLL-TYPE
    When the CCMS loader runs
    Then the system holds the 2 records in dq_exception with check code "DQ-062"
    Then the system writes 31,198 collateral rows

  Scenario: AC8 Unknown references above the tolerance
    Given 180 of the 33,050 account links name an account key not in loan_account, which is 0.54 percent
    When the CCMS loader runs
    Then the system refuses the INT-10 load at DQ-061 and no collateral or account_collateral row changes
    Then one LoadRefused event is in the outbox with failedCheck "DQ-061"
    Then the data steward group receives MSG-P1-002 "The INT-10 load for 2026-11-27 was refused: references. The previous load is still in use."

  Scenario: AC9 SVAF file not received
    Given no SVAF file for 2026-11-27 has passed the adapter by Tuesday 2026-12-01 04:00
    When the data steward lists the jobs for INT-11
    Then there is no INT-11 load_run for 2026-11-27 and valuation keeps the appraisals of 2026-11-20
    Then FreshnessQuery returns DP06 with status STALE, and the data steward group has received MSG-P1-001 from the freshness check

  Scenario: AC10 Valuation write fails
    Given ValuationRecordApi raises an error after 1,000 of 2,140 appraisals
    When the SVAF loader runs
    Then the system stores no appraisal from the file
    Then the INT-11 load_run status is FAILED
    Then a rerun by the platform administrator stores 2,140 appraisals

  Scenario: AC11 Loader called twice for one file
    Given the INT-10 load for 2026-11-27 is COMPLETED for interface run "IR-0000451"
    When the adapter calls the CCMS loader again for "IR-0000451"
    Then no row changes and the loader returns the outcome of the completed load
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
