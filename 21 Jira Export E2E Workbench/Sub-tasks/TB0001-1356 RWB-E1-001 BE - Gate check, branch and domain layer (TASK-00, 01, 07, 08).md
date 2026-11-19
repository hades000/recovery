# TB0001-1356 [RWB-E1-001] BE - Gate check, branch and domain layer (TASK-00, 01, 07, 08)

| Field | Value |
|---|---|
| Jira | [TB0001-1356](https://scbjira.atlassian.net/browse/TB0001-1356) |
| Type | Sub-task |
| Status | To Do |
| Resolution | - |
| Parent | TB0001-1163 |
| Epic link | - |
| Assignee | - |
| Reporter | PREMMAST SUWANNIKOM |
| Priority | Medium |
| Labels | - |
| Components | E2E Workbench |
| Fix versions | - |
| Affects versions | - |
| Sprint | Delivery Workbench Q4S1 Squad1; Delivery Workbench Q4S2 Squad1 |
| Team | RWB_SQ1 |
| Created | 2026-11-11T16:11:02.240+0700 |
| Updated | 2026-11-18T09:17:02.915+0700 |
| Due date | - |
| Resolved | - |
| Original estimate | - |
| Remaining estimate | - |
| Time spent | - |
| Votes | 0 |
| Watchers | 1 |
| Comments | 0 |

## Description

h2. Scope

Implementation Builder work for RWB-E1-001, parent [TB0001-1163|https://scbjira.atlassian.net/browse/TB0001-1163]. This sub-task carries TASK-RWB-E1-001-00, -01, -07 and -08 of the approved plan.

Canonical plan: {{output/INC-010-epic-1-RWB-E1-001/plan/}} — {{plan.md}}, {{tasks.md}}, {{data-model.md}}, {{contracts/backend-apis.json}}, {{tests/scenarios.md}}, {{review/plan-gate-review.md}}. These are workspace paths, not a claim that they are merged or published.

h2. Readiness — READY TO START

This is the only one of the four RWB-E1-001 Builder sub-tasks that can start today. It carries no blocking link.

||Task||Work||Can start||
|TASK-00|Plan-approval precondition check: confirm PRE-4 and PRE-5 each carry a name and a date.|Yes — both recorded, see below|
|TASK-01|Cut {{feature/TB0001-1163-recovery-tables}} from {{develop-recovery}}, record the SHA, and verify PRE-6, PRE-7, the {{dataengine}} package and the deploy role directly against that branch.|Yes — this task is the precondition check itself; it is meant to be run and to report what is missing|
|TASK-07|Entity {{DataProduct}} over {{rwb_data_product}} in {{th.co.scb.ace.demo.recovery.dataengine.internal.catalog}}, not exposed outside the module (BND-4).|Yes — needs only the module package; {{TB0001-1287}} is Done|
|TASK-08|{{DataProductRepository}}: read the active row by {{productCode}}, read every active row, and the write {{apply}} uses.|Yes|

Honest caveat: TASK-01 as written stops with {{BLOCKED}} if the RWB-E1-044 recovery Flyway bean or the {{ReferenceTableHandler}} interface is absent. Both are absent today. So this sub-task is expected to end in a recorded {{BLOCKED}} report for TASK-01 plus a completed entity and repository — not a green precondition run. Do not stub the missing bean or interface to make TASK-01 pass.

h2. Verification

TASK-01 must also record whether the recovery deploy step is configured to run as {{ACEDbFlywayRole_<ENV>}} (OPEN-019) and whether the RWB-E1-043 plan still carries the three unprefixed {{uq_*}} names (OPEN-039). Neither stops the build; both are recorded in {{implement/report.md}}.

h2. Branch policy

D-RCV-50: {{feature/TB0001-1163-recovery-tables}} from refreshed {{develop-recovery}}; story MR targets {{develop-recovery}}. Work stays inside {{th.co.scb.ace.demo.recovery.dataengine}} and the approved recovery migration and test paths. Never run against a shared database.

h2. Next

The remaining 14 tasks sit in three sibling sub-tasks, each linked to the card it waits on.

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
| Created Date | customfield_10249 | 2026-11-11 |
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
