# TB0001-1393 RWB-E1-042: REVIEW-074 fix, write reference_load before staging rows

| Field | Value |
|---|---|
| Jira | [TB0001-1393](https://scbjira.atlassian.net/browse/TB0001-1393) |
| Type | Sub-task |
| Status | To Do |
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
| Created | 2026-11-12T18:10:45.465+0700 |
| Updated | 2026-11-16T18:00:56.797+0700 |
| Due date | - |
| Resolved | - |
| Original estimate | - |
| Remaining estimate | - |
| Time spent | - |
| Votes | 0 |
| Watchers | 1 |
| Comments | 0 |

## Description

Plan tasks: TASK-RWB-E1-042-056 to 061 and the merge milestone TASK-RWB-E1-042-063.

* Defect (REVIEW-074): the merged code on develop-recovery (ac921bf8) stages parameter_value rows before it inserts rwb_reference_load, so every PARAMETER load fails on PostgreSQL (fk_parameter_value_load is not deferrable).
* Fix (TASK-056): in ReferenceLoadService.load, save and flush rwb_reference_load (VALIDATED, row_count = data rows) first, then handler.stage(); a different returned count throws LoadRowCountMismatchException and the load rolls back (X14b). No migration, shared file or dependency change.
* Error advice (TASK-057): count mismatch gives 500 with type, title, status, traceId only and one ERROR log line; the unmapped integrity-violation log no longer carries the exception message (REVIEW-087).
* Tests (TASK-058): ordering, row count, mismatch rollback, race, advice and controller tests (T-042-46 unit). Container proof (TASK-059) waits for INC-001 and this fix being merged.
* Fix-branch regression, 80% coverage and footprint (TASK-060); evidence and MR into develop-recovery on request (TASK-061); MR merged and squash SHA recorded (TASK-063).

Branch: feature/TB0001-1203-reference-load-write-order from develop-recovery.
Plan: output/INC-003-epic-1-RWB-E1-042/plan/tasks.md (AISDLC workspace repository).

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
| Created Date | customfield_10249 | 2026-11-12 |
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
