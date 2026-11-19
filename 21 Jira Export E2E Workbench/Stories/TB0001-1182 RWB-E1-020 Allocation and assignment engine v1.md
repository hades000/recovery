# TB0001-1182 [RWB-E1-020] Allocation and assignment engine v1

| Field | Value |
|---|---|
| Jira | [TB0001-1182](https://scbjira.atlassian.net/browse/TB0001-1182) |
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
| Created | 2026-11-05T12:37:21.629+0700 |
| Updated | 2026-11-17T21:35:02.987+0700 |
| Due date | - |
| Resolved | - |
| Original estimate | - |
| Remaining estimate | - |
| Time spent | - |
| Votes | 0 |
| Watchers | 1 |
| Comments | 0 |

## Description

As a team manager (RW-TEAMMGR), I want every new recovery case placed in a queue and given an owner by the allocation and assignment rule tables on the morning it arrives, so that each case at 90 days past due has one owner from its first day and nobody allocates cases by hand.

## Acceptance criteria

```gherkin
Feature: Allocate a new recovery case to a queue and an owner

  Background:
    Given the allocation table version "ALLOC-2026.11" is in force from 2026-11-30
    Given the queue "MTG-BKK-CO" belongs to team "MTG-BKK" and role RW-CASEOWN
    Given the queue uses the method "ROUND_ROBIN" with a caseload cap of 150
    Given the queue "MTG-BKK-CO" has the overflow queue "MTG-BKK-OVF"
    Given the business date is 2026-12-01

  Scenario: AC1 A new case is placed in the queue its row names
    Given a new case RW-2026-000201 with status "NEW", product group "MORTGAGE", region "BKK" and exposure band "B2"
    Given allocation row "ALLOC-014" matches product group "MORTGAGE", region "BKK" and any exposure band, with target queue "MTG-BKK-CO"
    When the morning allocation run starts
    Then the system places the case in queue "MTG-BKK-CO"
    Then the case team is "MTG-BKK" and the region is "BKK"

  Scenario: AC2 The owner is chosen by the queue's method
    Given queue "MTG-BKK-CO" holds three case owners U-01, U-02 and U-03 with 120, 95 and 140 open cases
    Given the last owner given a case in the queue was U-02
    When case RW-2026-000201 is placed in the queue
    Then the system gives the case to U-03
    Then the case status becomes "ASSIGNED"
    Then the system writes an assignment record with reason "ALLOCATION" and rule ID "ALLOC-014"

  Scenario: AC3 An owner at the caseload cap is skipped
    Given the last owner given a case was U-02
    Given U-03, the next owner in turn, holds 150 open cases
    Given U-01 holds 120 open cases
    When case RW-2026-000202 is placed in the queue
    Then the system gives the case to U-01, the following owner below the cap

  Scenario: AC4 Every owner is at the cap
    Given U-01, U-02 and U-03 each hold 150 open cases
    When case RW-2026-000203 is placed in queue "MTG-BKK-CO"
    Then the system places the case in the overflow queue "MTG-BKK-OVF"
    Then the case status stays "NEW" and no owner is set
    Then the team manager of "MTG-BKK" receives the allocation summary with MSG-P3-011 and count 1

  Scenario: AC5 No allocation row matches
    Given a new case RW-2026-000204 with product group "SSME" and region "NE3" that matches no allocation row
    When the morning allocation run starts
    Then the system places the case in the exception queue "RWB-EXC"
    Then the case status stays "NEW"
    Then the system writes a decision log entry with final call "RULE_GAP", product group "SSME" and region "NE3"
    Then the system publishes caseAllocationFailed with reason "NO_ROW_MATCHED"
    Then the allocation summary carries MSG-P3-012 with count 1

  Scenario: AC6 Every allocation is logged
    Given case RW-2026-000205 matches row "ALLOC-014" and owner U-02 is below the cap
    When the case is placed in the queue and given an owner
    Then the system writes one decision log entry with rule ID "ALLOC-014", rule version "ALLOC-2026.11", queue "MTG-BKK-CO", owner U-02 and the inputs used
    Then if the decision log write fails, the allocation is not made, the case stays "NEW" with no queue and the job record carries MSG-P3-013 for the case

  Scenario: AC7 A case with an open deviation is not allocated to a case owner
    Given a new case RW-2026-000206 with deviation_open = true
    When the morning allocation run starts
    Then the system places the case in the deviation handler queue "DEV-HANDLER" named by rule R-DEV-01
    Then the system sets no case owner and the status stays "NEW"

  Scenario: AC8 A repeated run for the same date has no further effect
    Given the morning allocation run for 2026-12-01 has assigned case RW-2026-000201 to U-03
    When the run for 2026-12-01 is started again from the job monitor
    Then case RW-2026-000201 keeps owner U-03 and its one assignment record
    Then the system writes no second decision log entry for the case
    Then the job record shows 1 case skipped as already allocated

  Scenario: AC9 A run with no new cases
    Given no case has status "NEW" on 2026-12-01
    When the morning allocation run starts
    Then the run completes with 0 cases read
    Then the allocation summary for each team shows 0 in overflow and 0 in the exception queue

  Scenario: AC10 The run waits for case creation
    Given JOB-02 has not completed for 2026-12-01 because the COLLINS load was refused
    When 07:00 passes
    Then JOB-03 has not started for 2026-12-01
    Then the job monitor shows JOB-03 waiting on JOB-02 with MSG-P1-001
    Then every NEW case keeps no queue and no owner

  Scenario: AC11 Two runs at the same time allocate each case once
    Given a first run is allocating case RW-2026-000207
    When a rerun for 2026-12-01 reaches the same case at the same time
    Then the rerun skips the locked case
    Then the case has exactly one assignment record and one decision log entry for 2026-12-01

  Scenario: AC12 An owner one case below the cap gets the case
    Given U-03 is next in turn and holds 149 open cases
    When case RW-2026-000208 is placed in queue "MTG-BKK-CO"
    Then the system gives the case to U-03
    Then U-03 now holds 150 open cases

  Scenario: AC13 A queue with no overflow queue sends the case to the exception queue
    Given queue "HP-CEN-CO" has no overflow queue
    Given every owner in queue "HP-CEN-CO" holds 150 open cases
    When case RW-2026-000209 is placed in queue "HP-CEN-CO"
    Then the system places the case in the exception queue "RWB-EXC" with reason "NO_OVERFLOW_QUEUE"
    Then the case status stays "NEW"
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
