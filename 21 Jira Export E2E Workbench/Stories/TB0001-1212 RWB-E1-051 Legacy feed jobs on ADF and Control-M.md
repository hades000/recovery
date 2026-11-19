# TB0001-1212 [RWB-E1-051] Legacy feed jobs on ADF and Control-M

| Field | Value |
|---|---|
| Jira | [TB0001-1212](https://scbjira.atlassian.net/browse/TB0001-1212) |
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
| Created | 2026-11-05T12:37:47.577+0700 |
| Updated | 2026-11-17T21:45:16.573+0700 |
| Due date | - |
| Resolved | - |
| Original estimate | - |
| Remaining estimate | - |
| Time spent | - |
| Votes | 0 |
| Watchers | 1 |
| Comments | 0 |

## Description

As a data steward and data product owner (RW-DATASTEW), I want the ALS, EFS, CCMS and SVAF feed jobs scheduled on Control-M and ADF, each writing a run record and alerting on failure, so that the squad loads run every day or week without a manual step.

## Acceptance criteria

```gherkin
Feature: Legacy feed jobs on ADF and Control-M

  Background:
    Given the interface configuration rows for "INT-01", "INT-07", "INT-10" and "INT-11" are in force

  Scenario: AC1 Four jobs scheduled
    Given the Control-M definitions for the ALS and EFS extracts and the ADF pipelines for CCMS and SVAF are deployed in SIT
    When business date 2026-11-15 runs, with the CCMS and SVAF files moved on Sunday 2026-11-15
    Then JOB-01 writes run rows for "INT-01" and "INT-07" with status "LOADED" and start times from 05:00
    Then JOB-09 writes run rows for "INT-10" and "INT-11" on Monday 2026-11-16 with status "LOADED" and start times from 04:00
    Then each run row holds the business date, the record count and the start and end time

  Scenario: AC2 Run book
    Given the four feed jobs
    When the run book check runs in the pipeline
    Then a run book exists for each of JOB-01 and JOB-09 with the sections purpose, schedule, owner, failure signs, restart steps and escalation
    Then the restart steps name the Control-M or ADF job for each of the four feeds

  Scenario: AC3 Contract tests
    Given the layout file for "INT-11" SVAF declares "Appraised Value" as a number of 18 digits with 2 decimals
    Given the sample file carries "Appraised Value" as text
    When the contract tests run in the pipeline
    Then the "INT-11" test fails with message MSG-P2-002 naming field "Appraised Value"
    Then the system blocks the merge

  Scenario: AC4 Alert on failure
    Given the ADF pipeline for CCMS fails on Sunday 2026-11-22
    When JOB-09 runs on Monday 2026-11-23 at 04:00
    Then the "INT-10" run row shows status "MISSING"
    Then the data steward and the platform administrator receive message MSG-P2-004 within 15 minutes (assumed; DL11)

  Scenario: AC5 COLLINS load late
    Given no COLLINS load for business date 2026-11-24 has arrived
    When JOB-01 retries at 06:00, 07:00, 08:00 and 09:00
    Then after the 09:00 attempt the run rows for "INT-01" and "INT-07" show status "MISSING"
    Then the account and arrears data product shows MSG-P1-001 with the date 2026-11-23

  Scenario: AC6 Feed started twice
    Given the "INT-07" load for business date 2026-11-25 is LOADED at 05:10
    When Control-M starts the EFS load again and JOB-01 is rerun at 05:40
    Then the system writes a run row with status "DUPLICATE"
    Then the system loads no EFS record a second time
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
