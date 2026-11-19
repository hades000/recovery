# TB0001-1192 [RWB-E1-030] Daily rebalancing and queue measures

| Field | Value |
|---|---|
| Jira | [TB0001-1192](https://scbjira.atlassian.net/browse/TB0001-1192) |
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
| Team | RWB_SQ1 |
| Created | 2026-11-05T12:37:29.312+0700 |
| Updated | 2026-11-17T21:35:39.150+0700 |
| Due date | - |
| Resolved | - |
| Original estimate | - |
| Remaining estimate | - |
| Time spent | - |
| Votes | 0 |
| Watchers | 1 |
| Comments | 0 |

## Description

As a team manager (RW-TEAMMGR), I want a daily job that assigns unassigned cases and moves the newest cases off owners above the cap by the assignment rules, and queue counts, ageing and service level breaches published to Power BI, so that queues stay balanced and every team manager sees the same numbers as the case list.

## Acceptance criteria

```gherkin
Feature: Daily rebalancing and queue measures

  Background:
    Given queue "TDR-BKK-CO" uses "LOWEST_LOAD" with cap 150
    Given the business date is 2026-12-02

  Scenario: AC1 Rebalance
    Given queue "TDR-BKK-CO" has 12 cases with no owner
    Given members U-61 and U-62 hold 140 and 144 open cases
    When JOB-06 runs
    Then the system assigns the 12 cases , 8 to U-61 and 4 to U-62, by lowest load with ties going to the member first in the queue list
    Then each assignment has reason "REBALANCE" and a decision log entry

  Scenario: AC2 Measures reconcile
    Given the snapshot taken at 2026-12-02 06:52
    When the queue report refreshes
    Then the depth of each queue equals the case list count for that queue at 06:52
    Then queue "TDR-BKK-CO" shows depth 296, unassigned 0 and an average age of 41 days

  Scenario: AC3 Breach alert
    Given case RW-2026-000501 in queue "TDR-BKK-CO" passes its service level
    When the timer check raises the breach
    Then the team manager of "TDR-BKK" receives MSG-P3-028 with count 1 and queue "TDR-BKK-CO"
    Then the next snapshot shows 1 breach for "TDR-BKK-CO" in Power BI

  Scenario: AC4 No member has capacity
    Given every member of "TDR-BKK-CO" holds 150 open cases and 5 cases have no owner
    When JOB-06 runs
    Then the 5 cases keep no owner
    Then the team manager receives MSG-P3-011 with count 5

  Scenario: AC5 No cap loaded
    Given queue "WO-BKK-CO" has no capacity cap
    When JOB-06 runs
    Then the system moves no case in "WO-BKK-CO"
    Then the snapshot still reports "WO-BKK-CO"

  Scenario: AC6 Decision log unavailable for one case
    Given owner U-63 holds 153 open cases and the decision log write fails for the second of the 3 newest cases
    When JOB-06 runs
    Then the system moves 2 cases off U-63 and 1 stays
    Then the job record lists the case that stayed with MSG-P7-003

  Scenario: AC7 A repeated run
    Given JOB-06 has balanced "TDR-BKK-CO" on 2026-12-02
    When JOB-06 runs again on 2026-12-02
    Then the system moves no case
    Then the system writes no decision log entry

  Scenario: AC8 Held cases are not moved
    Given owner U-64 holds 152 open cases and the 2 newest have deviation_open = true
    When JOB-06 runs
    Then those 2 cases stay with U-64 and the next 2 newest are moved

  Scenario: AC9 A count difference holds the snapshot
    Given the snapshot depth for "DIL-BKK-CO" is 88 and the case count at the same time is 87
    When the snapshot is checked
    Then the system does not publish it
    Then the data steward receives MSG-P3-029 with check "queue depth against case list"

  Scenario: AC10 Owner exactly at the cap
    Given owner U-65 holds 150 open cases
    When JOB-06 runs
    Then the system moves no case off U-65
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
