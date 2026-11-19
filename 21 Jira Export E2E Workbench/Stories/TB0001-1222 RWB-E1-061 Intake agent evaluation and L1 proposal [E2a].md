# TB0001-1222 [RWB-E1-061] Intake agent evaluation and L1 proposal [E2a]

| Field | Value |
|---|---|
| Jira | [TB0001-1222](https://scbjira.atlassian.net/browse/TB0001-1222) |
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
| Created | 2026-11-05T12:37:55.871+0700 |
| Updated | 2026-11-17T10:10:44.594+0700 |
| Due date | - |
| Resolved | - |
| Original estimate | - |
| Remaining estimate | - |
| Time spent | - |
| Votes | 0 |
| Watchers | 1 |
| Comments | 0 |

## Description

As a center of excellence analyst (RW-COE), I want the evaluation report of the case intake agent and the proposal to run it at autonomy level 1, built from the stored shadow results, so that the risk and model risk officer approves the step to L1 on measured results.

## Acceptance criteria

```gherkin
Feature: Intake agent evaluation and L1 proposal [E2a]

  Background:
    Given evaluation run "EV-INTAKE-001" of "INTAKE" on sample "INTAKE-S1" version 1 has status "DONE"
    Given it holds 200 shadow runs: 188 ANSWERED, 7 TIMED_OUT, 3 GUARDRAIL_FAILED and 2 BELOW_FLOOR
    Given the 200 runs cost 412.6000 baht in total with median latency 4,100 ms and 95th percentile 9,800 ms

  Scenario: AC1 Report
    Given the shadow results
    When the report is written
    Then it holds sample size 200, the agreement rate per gap type, failure counts 7 TIMED_OUT, 3 GUARDRAIL_FAILED and 2 BELOW_FLOOR
    Then it holds total cost 412.6000 baht, cost per case 2.0630 baht, median latency 4,100 ms and 95th percentile 9,800 ms
    Then it holds policy "P1", prompt "PR1" and the model version, and no personal field

  Scenario: AC2 Proposal
    Given the report
    When RW-COE loads policy "INTAKE" version "P2" with mode "L1", evaluation run "EV-INTAKE-001", conditions "agreement at least 0.85 for every gap type", fallback "rule result per R-UNI-32" and measures "acceptance, correction rate, fallback rate below 0.10"
    Then the system stores version "P2" with status "LOADED" and holds the conditions, the fallback and the measures to watch
    Then "P1" stays in force until RW-RISK approves "P2"

  Scenario: AC3 Report on an unfinished evaluation
    Given evaluation run "EV-INTAKE-002" has status "RUNNING"
    When RW-COE requests its report
    Then the system refuses the request with 409 and MSG-P10-008

  Scenario: AC4 A proposal without its measures
    Given a policy file with mode "L1" and no measures to watch
    When RW-COE loads it
    Then the system refuses the load with 422 and MSG-P10-001 naming check "measures to watch present"

  Scenario: AC5 Scores below a stated condition
    Given gap type NO_CONTACT_POINT has agreement 0.8150 in "EV-INTAKE-001"
    When RW-COE loads a proposal with condition "agreement at least 0.85 for every gap type"
    Then the system refuses the load with 422 and MSG-P10-001 naming "NO_CONTACT_POINT 0.8150 below 0.85"

  Scenario: AC6 Sample below the minimum
    Given evaluation run "EV-INTAKE-003" has sample size 150
    When RW-COE loads a proposal that names it
    Then the system refuses the load with 422 and MSG-P10-001 naming check "sample size at least 200"

  Scenario: AC7 The loader cannot approve the proposal
    Given user "coe.user01" loaded version "P2"
    When user "coe.user01" approves "P2"
    Then the system refuses the approval with 409 and MSG-P7-002
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
