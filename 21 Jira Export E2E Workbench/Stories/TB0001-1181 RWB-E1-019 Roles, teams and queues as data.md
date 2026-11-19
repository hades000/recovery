# TB0001-1181 [RWB-E1-019] Roles, teams and queues as data

| Field | Value |
|---|---|
| Jira | [TB0001-1181](https://scbjira.atlassian.net/browse/TB0001-1181) |
| Type | Story |
| Status | To Do |
| Resolution | - |
| Parent | TB0001-1162 |
| Epic link | TB0001-1162 |
| Assignee | Chitchaya Muanchonchana |
| Reporter | KRISSADA RONGRAT |
| Priority | Medium |
| Labels | - |
| Components | E2E Workbench |
| Fix versions | - |
| Affects versions | - |
| Sprint | Design - Pre-analyze |
| Team | RWB_SQ1 |
| Created | 2026-11-05T12:37:20.550+0700 |
| Updated | 2026-11-18T17:28:19.989+0700 |
| Due date | - |
| Resolved | - |
| Original estimate | - |
| Remaining estimate | - |
| Time spent | - |
| Votes | 0 |
| Watchers | 1 |
| Comments | 0 |

## Description

As a reference data administrator (RW-REFADM), I want queues, queue membership and capacity, each tied to a team code and a role code, held as versioned reference data loaded from the Excel template, so that the organization changes without a code release.

## Acceptance criteria

```gherkin
Feature: Roles, teams and queues as data

  Background:
    Given TEAM holds "TDR-BKK", "DIL-BKK", "LIT-BKK", "NPA-BKK", "DS-BKK" and "WO-BKK"
    Given the loader holds RW-REFADM and the approver holds RW-TEAMMGR

  Scenario: AC1 Tables loaded
    Given the Queues template with 12 queues for the TDR, DIL, litigation, NPA, debt sale and write-off teams and 48 member rows
    When the QUEUE and QUEUE_MEMBER sheets are loaded as version 1 with valid from 2026-11-30 and approved
    Then 12 queue rows are in force with table version 1
    Then each queue holds its team code and the role that works it, for example "LIT-BKK-OFF" with "LIT-BKK" and RW-LITOFF
    Then 48 member rows are in force
    Then the reference version holds the author, the approver and the approval time

  Scenario: AC2 Rollback
    Given QUEUE version 3 is in force with an error in queue "DIL-BKK-CO"
    Given QUEUE version 2 was in force before it
    When rollback is called once for version 3
    Then QUEUE version 2 is in force for every queue row
    Then each queue keeps its record ID, so cases in the queue keep their queue
    Then the system records the rollback with the caller, the time and the reason

  Scenario: AC3 Capacity
    Given member U-11 of queue "TDR-BKK-CO" has capacity 40 and holds 40 open cases
    When a 41st case is offered for U-11
    Then the capacity service answers "AT_CAP" for U-11
    Then names the overflow queue "TDR-BKK-OVF" for the case

  Scenario: AC4 Unknown team code
    Given the QUEUE sheet has queue "XYZ-CO" on row 7 with team code "XYZ"
    When it is loaded
    Then the system refuses the load in full with MSG-P1-002 naming row 7 and check "team code not in TEAM"
    Then no queue or member row changes

  Scenario: AC5 Cap outside its range
    Given queue "NPA-BKK-CO" has capacity cap 0
    When the QUEUE sheet is loaded
    Then the system refuses the load with MSG-GEN-002 for capacity cap with minimum 1 and maximum 500

  Scenario: AC6 Author cannot approve
    Given QUEUE version 4 was loaded by user U-90
    When U-90 approves it
    Then the system refuses the approval with MSG-P7-002
    Then version 4 stays VALIDATED and is not in force

  Scenario: AC7 Rollback with no earlier version
    Given QUEUE version 1 is the only version
    When rollback is called for version 1
    Then the system refuses the call with MSG-P3-015
    Then version 1 stays in force

  Scenario: AC8 The same file loaded twice
    Given the QUEUE sheet for valid from 2026-12-15 was loaded as version 5
    When the same file is loaded again for valid from 2026-12-15
    Then the response returns version 5
    Then the system writes no new version

  Scenario: AC9 A version with a future valid from
    Given QUEUE version 2 is in force and version 3 is approved with valid from 2026-12-15
    When the capacity service is asked on 2026-12-14
    Then it answers from version 2
    Then on 2026-12-15 it answers from version 3

  Scenario: AC10 Member without the queue role
    Given member U-12 on row 22 of the QUEUE_MEMBER sheet is listed on queue "LIT-BKK-OFF" and does not hold RW-LITOFF
    When the sheet is loaded
    Then the system refuses the load with MSG-P1-002 naming row 22 and check "member does not hold the queue role"

  Scenario: AC11 Overflow loop
    Given queue "DS-BKK-CO" overflows to "DS-BKK-OVF" and "DS-BKK-OVF" overflows to "DS-BKK-CO"
    When the QUEUE sheet is loaded
    Then the system refuses the load with MSG-P1-002 and check "overflow queues form a loop"

  Scenario: AC12 Required column empty
    Given queue row 3 has no assignment method
    When the QUEUE sheet is loaded
    Then the system refuses the load with MSG-GEN-001 for assignment method on row 3
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
