# TB0001-1200 [RWB-E1-039] Access log into the decision log and break-glass admin

| Field | Value |
|---|---|
| Jira | [TB0001-1200](https://scbjira.atlassian.net/browse/TB0001-1200) |
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
| Created | 2026-11-05T12:37:38.249+0700 |
| Updated | 2026-11-18T17:28:40.722+0700 |
| Due date | - |
| Resolved | - |
| Original estimate | - |
| Remaining estimate | - |
| Time spent | - |
| Votes | 0 |
| Watchers | 1 |
| Comments | 0 |

## Description

As a security administrator (RW-SECADM), I want every sign-in, refusal, read of a case record or document and export written to the decision log store, and emergency access taken only under a break-glass grant approved in the bank IAM against an open incident, for a limited time, with every action marked, so that every access can be audited from one log and emergency access is controlled and reviewed.

## Acceptance criteria

```gherkin
Feature: Access log into the decision log and break-glass admin

  Background:
    Given the environment is SIT
    Given the decision log store is available

  Scenario: AC1 Read logged
    Given test user "U-4101" holding RW-CASEOWN opens case "RW-2026-000123" at 10:15 on 3 December 2026
    When the case record view loads
    Then the system writes one decision log entry with decision code "AC-READ", actor "U-4101", the case ID and decided at 10:15
    Then its actions list the field IDs returned, with DF-PTY-007 and DF-PTY-016 marked "masked"

  Scenario: AC2 Break-glass granted
    Given incident "INC0004521" is open
    Given the security administrator approved IAM request "IAM-778812" and the IAM added test user "U-4102" holding RW-PLATADM to group "RWB-SIT-BREAKGLASS" until 18:00
    When "U-4102" calls POST /admin/break-glass at 10:30 with incident "INC0004521", request "IAM-778812", area "CASE_RECORD", right "U", scope "ALL" and a reason of 46 characters
    Then the grant is active until 14:30, the earlier of 4 hours and the group end
    Then the banner shows MSG-P4-004 with time "14:30"
    Then every entry written for "U-4102" until 14:30 carries the grant ID and incident "INC0004521"
    Then the system allows at 14:20 PATCH /tasks/{taskId} on case "RW-2026-000123" by "U-4102" and marked with the grant
    Then the system refuses at 14:31 the same call with MSG-P4-002, because RW-PLATADM holds only "R" in Case record, with no action by anyone

  Scenario: AC3 Export logged
    Given test user "U-4103" holding RW-TEAMMGR filters the case list by status "ASSIGNED" and product "MORTGAGE" and gets 37 rows
    When the user exports the list
    Then the system writes one decision log entry with decision code "AC-EXPT", actor "U-4103", the filter, row count 37 and no case ID

  Scenario: AC4 Document read logged
    Given test user "U-4101" holding RW-CASEOWN opens document "DOC-2026-0009981" on case "RW-2026-000123"
    When GET /documents/{documentId}/content returns the file
    Then one entry with decision code "AC-READ", the case ID and the document ID is written before the file is returned

  Scenario: AC5 Break-glass without an IAM grant is refused
    Given test user "U-4104" holds RW-PLATADM and is not in group "RWB-SIT-BREAKGLASS"
    When the user calls POST /admin/break-glass with incident "INC0004521"
    Then the system refuses the call with status 403 and message MSG-P4-007
    Then one entry with decision code "AC-DENY" and reason "NO_BREAKGLASS_GRANT" is written

  Scenario: AC6 Break-glass with a missing incident or a short reason is refused
    Given test user "U-4102" is in group "RWB-SIT-BREAKGLASS"
    When the user calls POST /admin/break-glass with no incident reference
    Then the system refuses the call with status 422 and message MSG-GEN-001 for field "incidentReference"
    Then when the user calls it with incident "INC0004521" and a reason of 12 characters
    Then the system refuses the call with status 422 and message MSG-GEN-002 for field "reason" with min 20 and max 1000

  Scenario: AC7 A read that cannot be logged returns nothing
    Given the decision log store is unavailable
    When test user "U-4101" opens case "RW-2026-000123"
    Then the call returns status 503 with message MSG-P7-003 and no case data
    Then the system raises an incident to the platform administrator queue

  Scenario: AC8 Access audit query
    Given case "RW-2026-000123" was read by "U-4101" at 10:15, by "U-4102" at 11:02 under break-glass, and by "U-4101" at 16:40 on 3 December 2026
    When test user "U-4105" holding RW-AUDIT calls GET /decision-log with that case ID, decision "AC-READ", from "2026-12-03" and to "2026-12-03"
    Then three entries return in time order with actor, time and fields shown
    Then the 11:02 entry carries incident "INC0004521"

  Scenario: AC9 Refusals are written to the decision log
    Given test user "U-4106" holds only RW-PHONECOL
    When the user calls GET /admin/roles
    Then the system refuses the call with MSG-P4-002
    Then one entry with decision code "AC-DENY", area "PLATFORM_ADMINISTRATION", right "R" and no case ID is written

  Scenario: AC10 A repeated activation does not open a second grant
    Given "U-4102" activated break-glass at 10:30 with Idempotency-Key "k-001"
    When the user sends the same request again with key "k-001" at 10:31
    Then the first response returns and no new entry is written
    Then when the user sends a request with key "k-002" at 10:32
    Then the call returns status 409 with message MSG-GEN-004
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
