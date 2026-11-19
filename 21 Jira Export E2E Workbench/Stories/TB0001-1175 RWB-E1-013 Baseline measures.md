# TB0001-1175 [RWB-E1-013] Baseline measures

| Field | Value |
|---|---|
| Jira | [TB0001-1175](https://scbjira.atlassian.net/browse/TB0001-1175) |
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
| Team | RWB_SQ1 |
| Created | 2026-11-05T12:37:15.513+0700 |
| Updated | 2026-11-17T21:34:28.874+0700 |
| Due date | - |
| Resolved | - |
| Original estimate | - |
| Remaining estimate | - |
| Time spent | - |
| Votes | 0 |
| Watchers | 1 |
| Comments | 0 |

## Description

As the Tribe lead (RW-TRIBE), I want cases by route, age and queue, realized recovery, time in stage and turnaround per route published as the baseline, with definitions agreed by the Tribe, so that every later epic is measured against the same baseline.

## Acceptance criteria

```gherkin
Feature: Baseline measures

Background:
Given the synthetic case set for business date 2026-11-27 holds 120 open cases: 60 Mortgage, 45 Hire purchase and 15 SSME
Given age bands are "0-90", "91-180", "181-365", "366-730" and "over 730" days since entry

Scenario: AC1 Definitions agreed
Given a definition file of 6 rows for "CASES_BY_ROUTE", "CASES_BY_AGE", "CASES_BY_QUEUE", "REALIZED_RECOVERY", "TIME_IN_STAGE" and "TAT_BY_ROUTE"
Given each row names its data product, formula, unit and approver "TRB-0001" with approval date 2026-11-20
When it is loaded with valid from 2026-11-21
Then definition version "MD-2026.11" is in force with 6 measures
Then each measure returns its data product and formula through MeasureCatalog

Scenario: AC2 Baseline published
Given the loads of business date 2026-11-27 passed their checks
When JOB-15 runs at 01:30 on 2026-11-28
Then measure_snapshot holds rows for business date 2026-11-27 marked baseline and frozen with definition version "MD-2026.11"
Then "CASES_BY_ROUTE" totals 120 cases, of which 60 are Mortgage
Then "REALIZED_RECOVERY" equals the sum of synthetic payments since entry, 4,350,000.00 THB

Scenario: AC3 Power BI data set
Given the baseline measures are published
When JOB-15 runs at 01:30 on 2026-12-02
Then the INT-19 extract for business date 2026-12-01 is in the data lake with freshness stamp 2026-12-01 and the record count in its trailer
Then the extract holds the baseline rows of 2026-11-27 unchanged
Then the job monitor records the JOB-15 run with its row count, start and end time

Scenario: AC4 Definition without a formula refused
Given a definition file where row "TIME_IN_STAGE" has no formula
When it is loaded
Then the system refuses the load in full with MSG-GEN-001 naming "formula"
Then the system puts no definition version in force

Scenario: AC5 Baseline published twice
Given the baseline for 2026-11-27 is frozen
When JOB-15 is rerun for business date 2026-11-27 from SCR-44
Then the frozen rows are unchanged
Then the run record shows MSG-P9-001 naming 2026-11-27

Scenario: AC6 Loads of the baseline date failed
Given the COLLINS load for 2026-11-27 was refused at check "control total"
When JOB-15 runs at 01:30 on 2026-11-28
Then the system writes no baseline rows for 2026-11-27
Then the run record shows MSG-P1-001 naming "DP03 Case" and 2026-11-26
Then the system publishes the baseline by the first JOB-15 run after the 2026-11-27 load passes

Scenario: AC7 Data lake unavailable
Given the data lake load area does not answer
When JOB-15 runs at 01:30 on 2026-12-01
Then the system writes measure_snapshot rows for 2026-11-30 in the Workbench
Then the system holds the extract and an alert goes to the operations channel with MSG-GEN-006 naming "Data lake"
Then the system sends the extract by the next JOB-15 run

Scenario: AC8 Measure with no definition in force
Given the extract configuration lists measure "COST_PER_CASE" with no definition in force
When JOB-15 runs at 01:30 on 2026-11-30
Then the system writes no value for "COST_PER_CASE"
Then the run record shows MSG-P9-003 naming "COST_PER_CASE"
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
