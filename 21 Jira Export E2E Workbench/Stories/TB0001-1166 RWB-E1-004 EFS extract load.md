# TB0001-1166 [RWB-E1-004] EFS extract load

| Field | Value |
|---|---|
| Jira | [TB0001-1166](https://scbjira.atlassian.net/browse/TB0001-1166) |
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
| Created | 2026-11-05T12:37:07.408+0700 |
| Updated | 2026-11-18T17:17:58.343+0700 |
| Due date | - |
| Resolved | - |
| Original estimate | - |
| Remaining estimate | - |
| Time spent | - |
| Votes | 0 |
| Watchers | 1 |
| Comments | 0 |

## Description

As a data steward and data product owner (RW-DATASTEW), I want the EFS contacts and promises for accounts at 90 days past due loaded each working day from the COLLINS daily batch, so that the contact history is on the case from its first day.

## Acceptance criteria

```gherkin
Feature: EFS extract load

  Background:
    Given the business date is 2026-11-30 and INT-01 is COMPLETED for 2026-11-30
    Given the INT-07 mapping version "EFS-MAP-1" is approved with sign-off reference "EFS-SIGN-2026-11-18" on 2026-11-18

  Scenario: AC1 Start-of-day file
    Given COLLINS completes the INT-07 staging records at 06:30 with 9,450 contact records for 2026-11-30 and a matching trailer
    When the JOB-01 attempt at 07:00 runs the INT-07 step
    Then collections_history holds 9,450 new rows with business date 2026-11-30, of which 1,320 carry a promise amount and date
    Then the INT-07 load_run shows 9,450 read, 9,450 loaded, status COMPLETED
    Then after the case list step, the row of case "RW-2026-000123" shows last contact 2026-11-30 15:42 and action code "PTP"

  Scenario: AC2 Mapping signed
    Given the INT-07 load for 2026-11-30 is COMPLETED
    When the data steward calls GET /admin/jobs with type "INT-07" and from 2026-11-30
    Then the Job shows mapping version "EFS-MAP-1"
    Then the mapping version in source_field_map carries approved_on 2026-11-18 and approval reference "EFS-SIGN-2026-11-18"

  Scenario: AC3 Late file
    Given COLLINS has not completed the INT-07 staging records for 2026-11-30 by 08:00
    When the INT-07 window check runs at 08:00
    Then the INT-07 load_run status is LATE
    Then one LoadRefused event is in the outbox with failedCheck "LATE"
    Then FreshnessQuery returns DP05 with business date 2026-11-27 and status STALE
    Then the data steward group receives MSG-P1-001 "DP05 Interaction is from 2026-11-27. Today's load has not arrived."
    Then collections_history keeps every row for 2026-11-27 unchanged

  Scenario: AC4 Mapping not approved
    Given the INT-07 mapping version in force is "EFS-MAP-2" with no approval
    When the INT-07 step runs
    Then the system refuses the load with MSG-P1-002 "The INT-07 load for 2026-11-30 was refused: mapping version EFS-MAP-2 not approved. The previous load is still in use."
    Then the system writes no collections_history row

  Scenario: AC5 Unknown account keys within the tolerance
    Given 40 of the 9,450 records name an account key not in loan_account, which is 0.42 percent
    When the INT-07 step runs
    Then the system writes 9,410 rows
    Then the system writes 40 dq_exception rows with check code "DQ-040"

  Scenario: AC6 Code missing from the code map
    Given 6 records carry call result "R99", which is not in the code map for LOV-CONTACT-RESULT
    When the INT-07 step runs
    Then the system holds the 6 records in dq_exception with check code "DQ-041"
    Then the system writes 9,444 rows

  Scenario: AC7 Action code outside the named list
    Given the named list efs.history.action.codes does not hold action code "SYS01"
    Given 120 records carry action code "SYS01"
    When the INT-07 step runs
    Then the system does not writ the 120 records and not held
    Then the load_run check results show "SKIPPED_ACTION_CODE" = 120

  Scenario: AC8 Same contact delivered again
    Given collections_history already holds EFS record key "EFS-77001234" from the load of 2026-11-27
    Given the 2026-11-30 delivery holds "EFS-77001234" again
    When the INT-07 step runs
    Then collections_history holds one row for "EFS-77001234"
    Then the load_run check results show "REPEATED" = 1

  Scenario: AC9 Blocking check fails
    Given the INT-07 staging records have no column "Call Result"
    When the INT-07 step runs
    Then the system refuses the load at DQ-037 with MSG-P1-002 naming "structure"
    Then one LoadRefused event is in the outbox with failedCheck "DQ-037"

  Scenario: AC10 Rerun of a completed load
    Given the INT-07 load for 2026-11-30 is COMPLETED
    When the platform administrator calls POST /admin/jobs/{jobId}/rerun for it
    Then the response is 409 with MSG-P1-011
    Then collections_history is unchanged
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
