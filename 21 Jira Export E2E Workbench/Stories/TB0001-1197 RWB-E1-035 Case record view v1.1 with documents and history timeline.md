# TB0001-1197 [RWB-E1-035] Case record view v1.1 with documents and history timeline

| Field | Value |
|---|---|
| Jira | [TB0001-1197](https://scbjira.atlassian.net/browse/TB0001-1197) |
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
| Created | 2026-11-05T12:37:35.841+0700 |
| Updated | 2026-11-18T17:22:59.228+0700 |
| Due date | - |
| Resolved | - |
| Original estimate | - |
| Remaining estimate | - |
| Time spent | - |
| Votes | 0 |
| Watchers | 1 |
| Comments | 0 |

## Description

As a case owner (RW-CASEOWN), I want a timeline on the case record view with contacts, documents, assignments, transfers and status changes in time order, each with who or which rule caused it, so that I see what happened to the case without asking anyone.

## Acceptance criteria

```gherkin
Feature: Case record view v1.1 with documents and history timeline

  Background:
    Given case owner U-81 owns case RW-2026-000801

  Scenario: AC1 Timeline order
    Given case RW-2026-000801 has a rule transfer at 2026-12-02 08:10 by row "TRF-007" version "TRF-2026.11"
    Given documents "Demand letter" stored at 2026-12-02 10:30 and "Title deed" at 2026-12-03 09:00
    Given a status change from "ASSIGNED" to "IN_PROGRESS" at 2026-12-03 11:15 by U-81
    When the timeline opens
    Then the four events show in the order transfer, demand letter, title deed, status change
    Then the transfer shows "TRF-007" with version "TRF-2026.11" and the status change shows U-81

  Scenario: AC2 Transfer reason
    Given a manual transfer at 2026-12-04 14:00 by team manager U-71 with transfer reason "R04"
    When the event is opened
    Then the reason "R04 Owner absent", the from owner, the to owner and the rule version "TRF-2026.11" are shown

  Scenario: AC3 Decision log unavailable
    Given the decision log query does not answer within 3 seconds
    When the timeline opens
    Then the interactions, documents and assignments show in time order
    Then the panel shows MSG-P3-023 for "Decisions"

  Scenario: AC4 A new case shows only its creation
    Given case RW-2026-000802 was created on 2026-12-02 and its only record is the creation entry in the decision log
    When the timeline opens
    Then one item shows with type "Case created", time 2026-12-02 and the entry rule version

  Scenario: AC5 Events at the same time
    Given an assignment and a decision log entry both at 2026-12-02 07:00:00
    When the timeline opens
    Then the decision log entry shows before the assignment, by the fixed type order
    Then the order is the same on every opening

  Scenario: AC6 More than 50 events
    Given case RW-2026-000803 has 132 events
    When the timeline opens
    Then the first page shows the 50 most recent events and total 132
    Then the third page shows 32 events

  Scenario: AC7 Case outside the scope
    Given case RW-2026-000804 belongs to team "LIT-BKK" and U-81 has scope Own
    When U-81 calls the timeline for RW-2026-000804
    Then the response is 404 with MSG-P4-003
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
