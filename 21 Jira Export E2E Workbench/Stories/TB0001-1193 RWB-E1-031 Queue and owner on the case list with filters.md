# TB0001-1193 [RWB-E1-031] Queue and owner on the case list with filters

| Field | Value |
|---|---|
| Jira | [TB0001-1193](https://scbjira.atlassian.net/browse/TB0001-1193) |
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
| Sprint | Design - Pre-analyze |
| Team | RWB_SQ2 |
| Created | 2026-11-05T12:37:32.793+0700 |
| Updated | 2026-11-18T17:22:58.939+0700 |
| Due date | - |
| Resolved | - |
| Original estimate | - |
| Remaining estimate | - |
| Time spent | - |
| Votes | 0 |
| Watchers | 1 |
| Comments | 0 |

## Description

As a team manager (RW-TEAMMGR), I want the queue and owner columns on the case list, with filters by queue, team and status and an export to Excel, so that I see my queues and who owns each case without a new screen.

## Acceptance criteria

```gherkin
Feature: Queue and owner on the case list with filters

  Background:
    Given team manager U-71 of team "DIL-BKK" with scope Team
    Given team "DIL-BKK" has 64 cases in queue "DIL-BKK-CO" and 20 in "DIL-BKK-OVF"

  Scenario: AC1 Filter by queue
    Given the case list
    When U-71 filters by queue "DIL-BKK-CO"
    Then 64 cases show, each with its owner and status
    Then no case from another queue shows

  Scenario: AC2 Export
    Given the list filtered by queue "DIL-BKK-CO" and status "ASSIGNED" with 51 cases
    When U-71 chooses Export
    Then an Excel file with 51 rows downloads
    Then the access log holds the export with user U-71, the time, the filters and 51 rows

  Scenario: AC3 No case meets the filters
    When U-71 filters by queue "DIL-BKK-CO" and status "WAITING_PARTNER" and no case matches
    Then the list shows the empty state with MSG-P3-020

  Scenario: AC4 Export above the limit
    Given parameter "caselist.export.maxrows" is 10000
    Given a filtered list of 10,001 cases for a user with scope All
    When the user chooses Export
    Then the system makes no file
    Then MSG-P3-021 shows with maximum 10000

  Scenario: AC5 Access log unavailable
    Given the access log store is unavailable
    When U-71 chooses Export on a list of 51 cases
    Then the system makes no file
    Then MSG-P7-003 shows

  Scenario: AC6 Queue outside the scope
    When U-71 filters by queue "LIT-BKK-OFF" of team "LIT-BKK"
    Then no case shows
    Then the list shows the empty state with MSG-P3-020

  Scenario: AC7 A case with no owner
    Given case RW-2026-000601 is in queue "DIL-BKK-OVF" with no owner
    When U-71 filters by queue "DIL-BKK-OVF"
    Then case RW-2026-000601 shows with a blank owner cell

  Scenario: AC8 Export at the limit
    Given a filtered list of exactly 10,000 cases for a user with scope All
    When the user chooses Export
    Then a file with 10,000 rows downloads
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
