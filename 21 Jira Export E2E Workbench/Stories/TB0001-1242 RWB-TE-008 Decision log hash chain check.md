# TB0001-1242 [RWB-TE-008] Decision log hash chain check

| Field | Value |
|---|---|
| Jira | [TB0001-1242](https://scbjira.atlassian.net/browse/TB0001-1242) |
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
| Created | 2026-11-05T16:11:15.834+0700 |
| Updated | 2026-11-17T21:36:02.358+0700 |
| Due date | - |
| Resolved | - |
| Original estimate | - |
| Remaining estimate | - |
| Time spent | - |
| Votes | 0 |
| Watchers | 1 |
| Comments | 0 |

## Description

As an internal auditor (RW-AUDIT), I want a nightly job that recomputes the whole decision log hash chain, records the result with the last hash, and reports a break to Compliance the same day, so that a changed entry is found the day it happens and the log can be relied on in audit.

## Acceptance criteria

```gherkin
Feature: Decision log hash chain check

  Background:
    Given the environment is SIT with the synthetic decision log
    Given JOB-13 for business date 2 December 2026 ended at 01:40 on 3 December 2026

  Scenario: AC1 Chain intact
    Given the decision log holds 48,210 entries and none has been changed
    When JOB-14 runs at 02:00 on 3 December 2026
    Then the job run record shows type "JOB-14", business date 2 December 2026, status "COMPLETED" and result "INTACT"
    Then its checks hold entries checked 48,210, last chain_seq 48,210 and that entry's entry_hash
    Then MSG-P7-007 with the count and the last hash is sent to the Compliance group

  Scenario: AC2 Break
    Given the actions of the entry with chain_seq 30,005 were changed in the SIT database with the trigger disabled
    When JOB-14 runs
    Then the run result is "BROKEN" with first break chain_seq 30,005 and its entry ID
    Then the system raises an incident and MSG-P7-008 with the entry ID is sent to the Compliance group before 08:00 on 3 December 2026

  Scenario: AC3 A run that stops is reported
    Given the database connection is closed in the test double after 20,000 entries
    When JOB-14 runs
    Then the run status is "FAILED" with entries checked 20,000
    Then the system alerts the platform administrator group
    Then the system sends MSG-P7-013 to the Compliance group with the date of the last complete check, 2 December 2026

  Scenario: AC4 A rerun gives a new record and no second scheduled run
    Given JOB-14 for business date 2 December 2026 failed at 02:20
    When test user "U-9301" holding RW-PLATADM reruns it from the job monitor at 08:30
    Then a second run record for business date 2 December 2026 is written with rerun true
    Then the system marks the report to Compliance as a rerun
    Then while the rerun is running a second start of JOB-14 is refused by the scheduler

  Scenario: AC5 An empty log is intact
    Given the decision log holds no entry
    When JOB-14 runs
    Then the result is "INTACT" with entries checked 0 and last hash of 64 zeros

  Scenario: AC6 The job waits for the decision log copy
    Given JOB-13 for business date 2 December 2026 is still running at 02:00 and ends at 02:25
    When JOB-14 fires at 02:00
    Then it starts the check at 02:25 and records the JOB-13 end time
    Then if JOB-13 has not ended by 04:00 the check starts at 04:00 with the note "JOB-13 not ended"

  Scenario: AC7 Several changed entries
    Given the entries with chain_seq 12,001 and 40,350 were changed in the SIT database
    When JOB-14 runs
    Then the first break is chain_seq 12,001 and the failing count is 2
    Then one incident and one MSG-P7-008 report name both entry IDs

  Scenario: AC8 Entries written during the run
    Given the log holds 48,210 entries when JOB-14 starts
    Given 37 entries are appended while it runs
    When the run ends
    Then entries checked is 48,210 and last chain_seq is 48,210
    Then the next night's run checks 48,247 entries
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
