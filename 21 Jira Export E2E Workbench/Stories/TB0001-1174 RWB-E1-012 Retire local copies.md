# TB0001-1174 [RWB-E1-012] Retire local copies

| Field | Value |
|---|---|
| Jira | [TB0001-1174](https://scbjira.atlassian.net/browse/TB0001-1174) |
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
| Created | 2026-11-05T12:37:14.434+0700 |
| Updated | 2026-11-18T17:18:09.757+0700 |
| Due date | - |
| Resolved | - |
| Original estimate | - |
| Remaining estimate | - |
| Time spent | - |
| Votes | 0 |
| Watchers | 1 |
| Comments | 0 |

## Description

As a team manager (RW-TEAMMGR), I want to confirm in the Workbench that my team's Excel or SharePoint tracker is replaced by the case list, with the location of the read-only archive recorded, so that there is one list and no shadow copy.

## Acceptance criteria

```gherkin
Feature: Retire local copies

  Background:
    Given the parameter tracker.retire.parallel.days = 2
    Given tracker "LIT-07 Litigation case tracker" of team LIT has decision LOAD, status SIGNED_OFF and signed off on Friday 2026-11-20

  Scenario: AC1 Team confirmation
    Given the LIT team has worked from the case list on Monday 2026-11-23 and Tuesday 2026-11-24
    When the LIT team manager calls POST /admin/trackers/{trackerId}/retire on 2026-11-25 with archive location "https://sharepoint.example/sites/lit/archive/LIT-07"
    Then the system retires the tracker status with retired_at 2026-11-25, the team manager's user ID and the archive location
    Then the system keeps the stored tracker file in the write-once store unchanged

  Scenario: AC2 Archive location
    Given LIT-07 was retired on 2026-11-25
    When the data steward calls GET /admin/trackers with status RETIRED
    Then the row for LIT-07 shows archive location "https://sharepoint.example/sites/lit/archive/LIT-07", retired on 2026-11-25, the confirming user and the stored file reference
    Then it lists the 3 fields "Hearing note", "Firm contact" and "Court room" as fields no feed carries

  Scenario: AC3 Business sign-off
    Given the six teams TDR, DIL, LIT, NPA, DEBT_SALE and WRITE_OFF have retired all their LOAD and RETIRE trackers by 2026-11-26
    When the Tribe lead calls GET /admin/trackers/retirement-report on 2026-11-26
    Then the report holds six team rows, each with the number of trackers, the number retired, the team manager who confirmed each retirement and the date
    Then every team row shows outstanding 0
    Then the system files the report with the release checklist of 30 November 2026

  Scenario: AC4 Tracker not signed off
    Given tracker "NPA-02 Asset holding list" has decision LOAD and status LOADED
    When the NPA team manager calls the retirement for NPA-02
    Then the system refuses the retirement with MSG-P1-013 "NPA-02 cannot be retired: its decision is LOAD and its status is LOADED."

  Scenario: AC5 Parallel period not yet complete
    Given LIT-07 was signed off on 2026-11-20
    When the LIT team manager calls the retirement on Monday 2026-11-23
    Then the system refuses the retirement with MSG-P1-014 "LIT-07 can be retired from 2026-11-25, after 2 working days of use of the case list."
    Then the status stays SIGNED_OFF

  Scenario: AC6 No archive location
    Given LIT-07 can be retired
    When the LIT team manager calls the retirement with no archive location
    Then the response is 400 with MSG-GEN-001 "Enter archive location."

  Scenario: AC7 Team manager of another team
    Given LIT-07 can be retired
    When the NPA team manager calls the retirement for LIT-07
    Then the response is 403 with MSG-P4-002
    Then the status stays SIGNED_OFF

  Scenario: AC8 Retirement repeated
    Given LIT-07 was retired on 2026-11-25
    When the LIT team manager calls the retirement again on 2026-11-26
    Then the response is 200 with retired_at 2026-11-25 and no field changes

  Scenario: AC9 Two retirements at the same time
    Given two sessions of the LIT team manager read LIT-07 at version 4
    When both call the retirement
    Then one succeeds and the other is refused with 409 and MSG-GEN-004

  Scenario: AC10 A team with an outstanding tracker
    Given team NPA has retired 3 of its 4 LOAD and RETIRE trackers and NPA-02 is still LOADED on 2026-11-26
    When the Tribe lead calls GET /admin/trackers/retirement-report on 2026-11-26
    Then the NPA row shows outstanding 1 with tracker code "NPA-02" and status LOADED
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
