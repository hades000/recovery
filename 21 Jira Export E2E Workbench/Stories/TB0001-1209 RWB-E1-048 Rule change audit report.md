# TB0001-1209 [RWB-E1-048] Rule change audit report

| Field | Value |
|---|---|
| Jira | [TB0001-1209](https://scbjira.atlassian.net/browse/TB0001-1209) |
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
| Created | 2026-11-05T12:37:45.314+0700 |
| Updated | 2026-11-17T21:45:36.442+0700 |
| Due date | - |
| Resolved | - |
| Original estimate | - |
| Remaining estimate | - |
| Time spent | - |
| Votes | 0 |
| Watchers | 1 |
| Comments | 0 |

## Description

As a center of excellence analyst (RW-COE), I want the parameter change and rule change checklist (request, impact, test result, approver, load, verify, rollback plan) recorded on every change and reported for audit, so that a configuration change is as controlled as a code change.

## Acceptance criteria

```gherkin
Feature: Rule change audit report

  Background:
    Given the business date is 2026-12-01
    Given SERVICE_LEVEL version 3 is in force with 10 working days for "MORTGAGE" status "IN_PROGRESS"
    Given user "U-REF-01" holds RW-REFADM, "U-RSK-01" holds the approve right and "U-AUD-01" holds RW-AUDIT

  Scenario: AC1 Change by checklist
    Given a request "CR-2026-0042" to change "MORTGAGE" status "IN_PROGRESS" to 8 working days from 2026-12-10
    Given "U-REF-01" loads SERVICE_LEVEL version 4 with impact summary "412 open Mortgage cases in IN_PROGRESS" and rollback plan "Reload version 3"
    Given the load checks pass
    Given "U-RSK-01" approves version 4 on 2026-12-02
    When "U-AUD-01" reads the change log for 2026-12-01 to 2026-12-31
    Then one entry shows table "SERVICE_LEVEL", version 4, request "CR-2026-0042", test result "PASSED", author "U-REF-01", approver "U-RSK-01", approved on 2026-12-02 and valid from 2026-12-10
    Then the entry shows 1 row changed, 0 added and 0 removed against version 3
    Then the approval time is before the valid from date

  Scenario: AC2 Checklist skipped
    Given SERVICE_LEVEL version 5 loaded by "U-REF-01" with valid from 2026-12-15 and never approved
    When the business date reaches 2026-12-15
    Then the reference data service still serves version 4
    Then the change log shows version 5 with status "VALIDATED" and approver empty

  Scenario: AC3 Checklist item missing at approval
    Given HOLIDAY version 2 loaded with no rollback plan
    When "U-RSK-01" approves it
    Then the system refuses the approval with MSG-P3-022 naming "rollback plan"
    Then version 2 stays "VALIDATED"

  Scenario: AC4 Failed test result
    Given rule version "RULE_UNIVERSAL_RULES" version 3 whose harness result is "FAILED" with 2 of 50 tests failing
    When "U-RSK-01" approves it
    Then the system refuses the approval with MSG-P3-022 naming "test result"

  Scenario: AC5 Verification after the change takes effect
    Given SERVICE_LEVEL version 4 in force from 2026-12-10
    When "U-REF-01" records the verification on 2026-12-10 with the note "Timer on RW-2026-000101 shows 8 working days"
    Then the change log entry for version 4 shows verified by "U-REF-01" on 2026-12-10

  Scenario: AC6 Period with no changes
    When "U-AUD-01" reads the change log for 2026-11-01 to 2026-11-15
    Then the response is an empty list with total 0

  Scenario: AC7 Verification too early
    Given SERVICE_LEVEL version 4 with valid from 2026-12-10
    When "U-REF-01" records the verification on 2026-12-09
    Then the system refuses the call with MSG-GEN-003 naming "verified at" and "valid from"

  Scenario: AC8 Period in the wrong order
    When "U-AUD-01" reads the change log from 2026-12-31 to 2026-12-01
    Then the system refuses the call with MSG-GEN-003 naming "to" and "from"

  Scenario: AC9 Report as CSV
    When "U-AUD-01" reads the change log for 2026-12-01 to 2026-12-31 with format "csv"
    Then the response is a CSV file with one header row and one row per version
    Then it carries no party identifier and no case data
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
