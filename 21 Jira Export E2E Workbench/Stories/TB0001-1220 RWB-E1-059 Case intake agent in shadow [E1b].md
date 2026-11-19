# TB0001-1220 [RWB-E1-059] Case intake agent in shadow [E1b]

| Field | Value |
|---|---|
| Jira | [TB0001-1220](https://scbjira.atlassian.net/browse/TB0001-1220) |
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
| Team | RWB_SQ2 |
| Created | 2026-11-05T12:37:54.209+0700 |
| Updated | 2026-11-17T10:09:56.714+0700 |
| Due date | - |
| Resolved | - |
| Original estimate | - |
| Remaining estimate | - |
| Time spent | - |
| Votes | 0 |
| Watchers | 1 |
| Comments | 0 |

## Description

As a center of excellence analyst (RW-COE), I want the case intake agent to build a case file summary and flag gaps for every new Epic 1 case in shadow mode, so that the agent is scored against the business analysts' review before any case owner sees its output.

## Acceptance criteria

```gherkin
Feature: Case intake agent in shadow [E1b]

  Background:
    Given agent "INTAKE" has approved policy "P1" with mode "SHADOW" and prompt "PR1"
    Given the gap types in output schema "intake-summary-v1" are MISSING_DOCUMENT, NO_VALID_APPRAISAL, NO_CONTACT_POINT and STALE_INPUT

  Scenario: AC1 Shadow run
    Given 200 Epic 1 cases created between 2026-11-30 and 2026-12-04
    When the agent runs on each CaseCreated event
    Then 200 agent runs with mode "SHADOW" store a summary and gap flags
    Then no case field, task, queue or decision log entry changes
    Then GET /cases/{caseId} and GET /cases/{caseId}/timeline return no agent output
    Then GET /admin/agent-runs returns the 200 runs without the summary or the gap flags

  Scenario: AC2 Agreement rate
    Given the business analysts' review of the same 200 cases in sample "INTAKE-S1" version 1
    When the comparison runs
    Then one score row per gap type holds the agreement rate, precision, recall and sample size 200
    Then for MISSING_DOCUMENT with 182 agreeing cases the agreement rate is 0.9100
    Then each score row holds policy "P1", prompt "PR1" and the model version

  Scenario: AC3 A new case starts one shadow run
    Given case "RW-2026-000301" is created on 2026-11-30
    When EV-01 CaseCreated is processed
    Then one agent run exists with key "INTAKE:<caseId>:2026-11-30", trigger "CaseCreated" and mode "SHADOW"

  Scenario: AC4 A failed run is counted and not retried
    Given the model stub does not answer for case "RW-2026-000302"
    When the agent runs
    Then the run holds status "TIMED_OUT" and fallback true
    Then the system makes no second run for that event
    Then the failure count for type "TIMED_OUT" on 2026-11-30 is 1

  Scenario: AC5 Stale input is flagged
    Given the latest COLLINS load is for 2026-11-28 and the business date is 2026-11-30
    When the agent runs for case "RW-2026-000303"
    Then the run holds data_as_of 2026-11-28
    Then the stored gap flags include STALE_INPUT
    Then an answer without STALE_INPUT fails check "SCHEMA_RULE" with fallback true

  Scenario: AC6 A repeated event has no further effect
    Given EV-01 CaseCreated for case "RW-2026-000301" was processed on 2026-11-30
    When the same event arrives again with the same event ID
    Then one agent run exists for the case and date and the repeat is counted (R-UNI-40)

  Scenario: AC7 Partly labeled sample
    Given sample "INTAKE-S1" version 2 has labels for 180 of 200 cases
    When the comparison runs
    Then each score row holds sample size 180
    Then the system lists the 20 unlabeled cases as unlabeled on the evaluation run

  Scenario: AC8 Empty sample
    Given sample "INTAKE-S3" has no labeled rows for "INTAKE"
    When RW-COE starts the evaluation
    Then the system refuses the request with 422 and MSG-P10-002
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
