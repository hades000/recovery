# TB0001-1247 [RWB-TE-013] Agent runtime client with fallback

| Field | Value |
|---|---|
| Jira | [TB0001-1247](https://scbjira.atlassian.net/browse/TB0001-1247) |
| Type | Story |
| Status | To Do |
| Resolution | - |
| Parent | TB0001-1234 |
| Epic link | TB0001-1234 |
| Assignee | - |
| Reporter | KRISSADA RONGRAT |
| Priority | Medium |
| Labels | - |
| Components | E2E Workbench |
| Fix versions | - |
| Affects versions | - |
| Sprint | - |
| Team | RWB_SQ2 |
| Created | 2026-11-05T16:11:20.087+0700 |
| Updated | 2026-11-17T10:09:37.611+0700 |
| Due date | - |
| Resolved | - |
| Original estimate | - |
| Remaining estimate | - |
| Time spent | - |
| Votes | 0 |
| Watchers | 1 |
| Comments | 0 |

## Description

As a platform administrator (RW-PLATADM), I want one client in the recovery module that calls the agent orchestrator, applies the autonomy mode, runs shadow mode and falls back to the rule result, so that agents are added to a case step without changing the case flow, and every step records what the agent did.

## Acceptance criteria

```gherkin
Feature: Agent runtime client with fallback

  Background:
    Given agent "INTAKE" has approved policy "P1" with timeout 60 seconds and prompt "PR1"
    Given case "RW-2026-000201" is in route state "NEW" and status "New"
    Given the calling step has rule result rule "R-UNI-32" version "2026.11" with next state "RESUME_STATE"

  Scenario: AC1 Shadow
    Given the policy of "INTAKE" has autonomy mode "SHADOW"
    When the agent answers in 2,000 ms with a valid output
    Then the system stores the agent answer on the agent run and the rule result is the applied result
    Then one decision log entry holds agent version "INTAKE@P1/PR1", the rule ID and version, recommendation null and fallback false in actions
    Then the calling step receives the rule result and no agent output

  Scenario: AC2 No answer
    Given the agent does not answer in 60 seconds
    When the step runs
    Then the system uses the rule result and the step continues to "RESUME_STATE"
    Then the decision log entry holds actions fallback true with reason "TIMED_OUT" and the agent run ID (R-UNI-32)
    Then the agent run holds status "TIMED_OUT" and fallback true

  Scenario: AC3 Assisted mode returns the answer as a recommendation
    Given the policy of "INTAKE" has autonomy mode "L1"
    When the agent answers with confidence 0.91
    Then the rule result is the applied result
    Then the outcome returns the agent answer as the recommendation for the person who decides
    Then the decision log entry holds the agent answer in recommendation with confidence 0.91

  Scenario: AC4 A guardrail failure falls back
    Given the agent answer fails check "SCHEMA"
    When the step runs
    Then the system applies the rule result
    Then the decision log entry holds actions fallback true with reason "SCHEMA"

  Scenario: AC5 No approved policy
    Given agent "INTAKE" has no approved policy on 2026-11-30
    When the step runs on 2026-11-30
    Then the system makes no orchestrator call
    Then the system applies the rule result with fallback true and reason "NO_POLICY" in the decision log entry

  Scenario: AC6 The decision log write fails
    Given the decision log writer throws on write
    When the step runs
    Then the calling step does not act and case "RW-2026-000201" stays in "NEW"
    Then the client raises DecisionNotRecordedException carrying MSG-P7-003 and an incident is raised (R-UNI-39)
    Then the agent run stays with decision_log_id empty

  Scenario: AC7 A repeated step key
    Given the step with key "CASEWF:RW-2026-000201:ENTRY:2026-11-30" ran once
    When it runs again with the same key
    Then one agent run and one decision log entry exist for the key
    Then the second call returns the first outcome (R-UNI-40)

  Scenario: AC8 Agent switched off
    Given the policy of "INTAKE" has autonomy mode "OFF"
    When the step runs
    Then no orchestrator call and no agent run row are made
    Then the decision log entry holds agent version null and fallback false
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
