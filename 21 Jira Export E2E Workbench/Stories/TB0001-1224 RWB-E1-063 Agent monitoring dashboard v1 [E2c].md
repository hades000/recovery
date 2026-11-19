# TB0001-1224 [RWB-E1-063] Agent monitoring dashboard v1 [E2c]

| Field | Value |
|---|---|
| Jira | [TB0001-1224](https://scbjira.atlassian.net/browse/TB0001-1224) |
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
| Created | 2026-11-05T12:37:57.364+0700 |
| Updated | 2026-11-17T10:10:56.819+0700 |
| Due date | - |
| Resolved | - |
| Original estimate | - |
| Remaining estimate | - |
| Time spent | - |
| Votes | 0 |
| Watchers | 1 |
| Comments | 0 |

## Description

As a risk and model risk officer (RW-RISK), I want a dashboard with runs, acceptance, override, fallback, latency, cost and evaluation score per agent and version, and an alert when an agent's daily cost passes its limit, so that every agent is watched from its first shadow run.

## Acceptance criteria

```gherkin
Feature: Agent monitoring dashboard v1 [E2c]

  Background:
    Given agents "INTAKE" (policy "P1", prompt "PR1") and "SCREENING" (policy "P1", prompt "PR1") run in shadow
    Given on business date 2026-12-01 "INTAKE" has 120 runs, 9 with fallback, cost 1,840.0000 baht
    Given on 2026-12-01 "SCREENING" has 150 runs, 21 with fallback, cost 2,310.5000 baht
    Given both policies have daily_cost_cap_thb 2,000 and alert_role "RW-COE"

  Scenario: AC1 Per agent
    Given two agents in shadow
    When the dashboard opens for 2026-12-01
    Then each agent shows runs, fallback rate, median and 95th percentile latency, cost and the latest evaluation score by policy and prompt version
    Then "INTAKE" shows 120 runs and fallback rate 0.0750
    Then acceptance and override show "no L1 runs" for both agents, because no agent runs at L1 in Epic 1

  Scenario: AC2 Alert
    Given cost above the daily parameter for "SCREENING"
    When JOB-15 completes for 2026-12-01
    Then one agent alert row exists for "SCREENING", type "COST_CAP", date 2026-12-01, measured 2,310.5000 and threshold 2,000
    Then the system sends MSG-P10-004 to the holders of RW-COE and RW-RISK through the notification path
    Then no alert exists for "INTAKE"

  Scenario: AC3 A copy that does not match is held
    Given the data lake write for 2026-12-01 stores 1 row for 2 agent and version groups
    When the count check runs
    Then the system holds the publish for 2026-12-01 and the report shows 2026-11-30
    Then the step reports failed in GET /admin/jobs and the data steward is alerted

  Scenario: AC4 A rerun for the same date
    Given JOB-15 completed for 2026-12-01 and sent the "SCREENING" alert
    When RW-PLATADM reruns JOB-15 for 2026-12-01
    Then agent_run_daily holds the same 2 rows for 2026-12-01
    Then no second alert row or notification exists

  Scenario: AC5 An agent with no runs
    Given agent "EXTRACT" has an approved policy and no runs on 2026-12-01
    When JOB-15 completes for 2026-12-01
    Then "EXTRACT" shows runs 0 and cost 0.0000 for 2026-12-01 and no alert

  Scenario: AC6 Cost equal to the cap
    Given "INTAKE" cost is 2,000.0000 baht on 2026-12-02
    When JOB-15 completes for 2026-12-02
    Then no cost alert exists for "INTAKE" on 2026-12-02

  Scenario: AC7 The notification path is down
    Given the P6 notification interface is unavailable at 01:40
    When the "SCREENING" alert is raised
    Then the system keeps the alert row with sent_at empty
    Then the system sends it when the outbox sender succeeds (R-UNI-33, R-UNI-35)
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
