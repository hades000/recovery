# TB0001-1367 RWB-E1-042: P4 access - port types, clock, caller identity, capability policy, error advice, load/approve/rollback endpoints

| Field | Value |
|---|---|
| Jira | [TB0001-1367](https://scbjira.atlassian.net/browse/TB0001-1367) |
| Type | Sub-task |
| Status | In Progress |
| Resolution | - |
| Parent | TB0001-1203 |
| Epic link | - |
| Assignee | - |
| Reporter | Nuttapon Jittachotisak |
| Priority | Medium |
| Labels | INC-003, RWB-E1-042 |
| Components | E2E Workbench |
| Fix versions | - |
| Affects versions | - |
| Sprint | Delivery Workbench Q4S1 Squad1; Delivery Workbench Q4S2 Squad2 |
| Team | RWB_SQ2 |
| Created | 2026-11-11T17:07:41.092+0700 |
| Updated | 2026-11-16T18:00:54.957+0700 |
| Due date | - |
| Resolved | - |
| Original estimate | - |
| Remaining estimate | 0m |
| Time spent | 1d |
| Votes | 0 |
| Watchers | 1 |
| Comments | 0 |

## Description

Plan tasks: TASK-RWB-E1-042-006, 008, 009, 017 (P4 part), 027, 028, 029, 034, 035, 051, 052.

* access.api published types (ReferenceTableHandler port, RecoverySchema, MessageResolver, RecoveryClock, RecoveryCaller).
* SystemRecoveryClock (Asia/Bangkok), OidcRecoveryCaller (non-UUID oid gives 403), deny-all capability policy, RecoveryProblemAdvice.
* ReferenceLoadController: POST reference-loads, approve, rollback, with the planned check order.
* Kept as its own ACE commit so the AGENTS.md section 7 exception can be reviewed or dropped (OPEN-027).

Waits for: package move sub-task.
Plan: output/INC-003-epic-1-RWB-E1-042/plan/tasks.md (AISDLC workspace repository).

## Comments (0)

(none)

## Other Jira fields

| Field | ID | Value |
|---|---|---|
| Actual End Date | customfield_14458 | 2026-11-13 |
| Actual Start Date | customfield_14457 | 2026-11-12 |
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
| Story Point | customfield_17479 | 0 |
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
