# TB0001-1241 [RWB-TE-007] Scheduled jobs on Quartz

| Field | Value |
|---|---|
| Jira | [TB0001-1241](https://scbjira.atlassian.net/browse/TB0001-1241) |
| Type | Story |
| Status | To Do |
| Resolution | - |
| Parent | TB0001-1234 |
| Epic link | TB0001-1234 |
| Assignee | - |
| Reporter | KRISSADA RONGRAT |
| Priority | Medium |
| Labels | - |
| Components | E2E Workbench |
| Fix versions | - |
| Affects versions | - |
| Sprint | - |
| Team | RWB_SQ1 |
| Created | 2026-11-05T16:11:15.000+0700 |
| Updated | 2026-11-17T21:35:58.338+0700 |
| Due date | - |
| Resolved | - |
| Original estimate | - |
| Remaining estimate | - |
| Time spent | - |
| Votes | 0 |
| Watchers | 1 |
| Comments | 0 |

## Description

As a platform administrator (RW-PLATADM), I want the timer check, the morning allocation run and the daily reconciliation run as Quartz jobs with a run book each, so that scheduled work runs once, on time and visibly, and a missed run is caught up for its business date.

## Acceptance criteria

```gherkin
Feature: Scheduled jobs on Quartz

  Background:
    Given two service instances "ACE-1" and "ACE-2" share the clustered Quartz job store
    Given the COLLINS load for business date 2026-12-02 passed its checks at 05:20 and JOB-02 succeeded at 05:50

  Scenario: AC1 Runs once
    When the morning allocation is due for business date 2026-12-02
    Then JOB-03 runs once, on one of the two instances
    Then the system logs its run with job "JOB-03", business date 2026-12-02, instance, start, end, status "SUCCEEDED" and the case counts

  Scenario: AC2 Missed run
    Given both instances were down from 04:30 to 09:40 on 2026-12-02
    When the service restarts at 09:40
    Then JOB-03 and JOB-04 run for business date 2026-12-02 after JOB-02 succeeds for that date
    Then the system logs each run with MSG-P3-030 naming the job and 2026-12-02

  Scenario: AC3 Repeated run for the same date
    Given JOB-03 succeeded for business date 2026-12-02
    When JOB-03 is fired again for 2026-12-02
    Then the system allocates no case again
    Then the run log records a skip for JOB-03 and 2026-12-02

  Scenario: AC4 Timer check does not overlap
    Given a JOB-05 run that started at 10:00 takes 7 minutes
    When the 10:05 fire is due
    Then the 10:05 run starts only after the 10:00 run ends
    Then no two JOB-05 runs are in progress at the same time

  Scenario: AC5 Several missed dates
    Given COLLINS loads passed for business dates 2026-12-02, 2026-12-03 and 2026-12-04 while both instances were down
    When the service restarts on 2026-12-04 at 11:00
    Then JOB-03 runs for 2026-12-02, then 2026-12-03, then 2026-12-04
    Then the system logs each run with its business date

  Scenario: AC6 More missed dates than the limit
    Given 7 business dates with passed COLLINS loads and no JOB-03 run
    When the service restarts
    Then no automatic catch-up run starts
    Then an alert with MSG-P3-031 names JOB-03 and the 7 dates

  Scenario: AC7 Dependency not met
    Given JOB-02 failed for business date 2026-12-03
    When JOB-03 is due for 2026-12-03
    Then JOB-03 does not run and its run is recorded "WAITING" with MSG-P3-031 naming "JOB-02"
    Then when JOB-02 succeeds for 2026-12-03 at 08:10 JOB-03 runs for 2026-12-03

  Scenario: AC8 Instance stops part way
    Given JOB-04 is running for 2026-12-02 on "ACE-1"
    When "ACE-1" stops
    Then "ACE-2" runs JOB-04 again for 2026-12-02 within the cluster check-in interval of 20 seconds
    Then the run log shows one "FAILED" run on "ACE-1" and one "SUCCEEDED" run on "ACE-2"

  Scenario: AC9 Allocation late
    Given JOB-03 for 2026-12-02 has not succeeded at 07:00
    When the deadline check runs at 07:00
    Then an alert with MSG-P3-031 naming JOB-03, 2026-12-02 and 07:00 reaches the operations channel by 07:15

  Scenario: AC10 Run book for every job
    Given the run book folder holds run books for JOB-03 and JOB-05 only
    When the build runs
    Then the build fails naming JOB-04
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
