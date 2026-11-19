# TB0001-1307 [RWB-TE-003] TASK-006 Reference-list file

| Field | Value |
|---|---|
| Jira | [TB0001-1307](https://scbjira.atlassian.net/browse/TB0001-1307) |
| Type | Sub-task |
| Status | Review |
| Resolution | - |
| Parent | TB0001-1237 |
| Epic link | - |
| Assignee | - |
| Reporter | thanapat khumprom |
| Priority | Medium |
| Labels | AISDLC, RWB-TE-003 |
| Components | E2E Workbench |
| Fix versions | - |
| Affects versions | - |
| Sprint | Delivery Workbench Q4S1 Squad2; Delivery Workbench Q4S2 Squad2 |
| Team | RWB_SQ2 |
| Created | 2026-11-10T11:49:46.372+0700 |
| Updated | 2026-11-11T11:00:17.253+0700 |
| Due date | - |
| Resolved | - |
| Original estimate | - |
| Remaining estimate | - |
| Time spent | - |
| Votes | 0 |
| Watchers | 1 |
| Comments | 0 |

## Description

*Story:* RWB-TE-003 — TB0001-1237 · *Plan task:* TASK-006 · *Surface:* Backend
*Blocked by:* TASK-005 (the sub-task with that TASK ID in its summary, under TB0001-1237)
*Approved plan:* commit {{fd93eb7}} — [tasks.md|https://gitdop.se.scb.co.th/AP2477-ACE/ace-aisdlc/-/blob/fd93eb7/recovery/output/INC-005-epic-1-RWB-TE-003/plan/tasks.md] · [plan.md|https://gitdop.se.scb.co.th/AP2477-ACE/ace-aisdlc/-/blob/fd93eb7/recovery/output/INC-005-epic-1-RWB-TE-003/plan/plan.md]

h3. What to do

*Reference-list file* {{backend/src/main/resources/recovery/api/recovery-api-reference.yaml}}:

* the 14 areas exactly as in Users, Roles and Permissions v3: Case record, Queue and allocation, Treatment and offer, Litigation, Asset and disposal, Debt sale, Write-off and posting, Documents, Rules and parameters, Reference data, Decision log, Partner portal, Reporting, Platform administration;
* rights {{C, R, U, D, A}};
* releases {{E1..E6}} in order;
* a source note.

{{None}} is not listed; the lint accepts it as the no-right area.

h3. Deliverable

{{recovery-api-reference.yaml}}

h3. Done when

Areas compared line by line with the v3 matrix header (AISDLC repo {{recovery/requirement/legacy/02-business-architecture-and-process/recovery-workbench-users-roles-and-permissions-v3-xlsx.md}}); every area and right used in the API file is in the lists.

h3. Trace

SPEC-RWB-TE-003-002; FR-RWB-003; Guard-1

h3. Rules

* ACE repo {{ace-monorepo}}, branch {{feature/TB0001-1237-api-contract-tests}} from {{develop}}; commits {{TB0001-1237: <summary>}}. Edit only the paths listed in plan §7.
* No business value hard-coded elsewhere; if _Done when_ cannot be met, stop and report.
* Evidence ({{implement/...}}) goes to {{recovery/output/INC-005-epic-1-RWB-TE-003/implement/}} in the AISDLC repo {{AP2477-ACE/ace-aisdlc}}.

## Comments (0)

(none)

## Other Jira fields

| Field | ID | Value |
|---|---|---|
| Actual Start Date | customfield_14457 | 2026-11-11 |
| App Owner | customfield_10188 | - |
| App Owner (migrated 3) | customfield_11031 | - |
| Approver2 | customfield_11586 | Nuttakorn Leeviravanich |
| AR: Atlassian-TemplateO | customfield_11656 | emaile,role |
| AR: Atlassian_Template | customfield_11654 | \|\|Full Name \|\| Email \|\| Role \|\| Company \|\| \|{Full Name}\|{Email}\|{Role}\|{Company}\| \|\|\|\| |
| BI Status | customfield_10169 | To be Confirmed |
| Build % | customfield_12531 | 0% |
| Bulk Backlog Detail Uploaded | customfield_11628 | No |
| CCB Status | customfield_10228 | New |
| Created Date | customfield_10249 | 2026-11-10 |
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
