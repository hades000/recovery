# TB0001-1359 [RWB-E1-001] BE - Authorisation and release readiness (TASK-15, 17)

| Field | Value |
|---|---|
| Jira | [TB0001-1359](https://scbjira.atlassian.net/browse/TB0001-1359) |
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
| Created | 2026-11-11T16:11:43.634+0700 |
| Updated | 2026-11-18T09:17:03.943+0700 |
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

Implementation Builder work for RWB-E1-001, parent [TB0001-1163|https://scbjira.atlassian.net/browse/TB0001-1163]. This sub-task carries TASK-RWB-E1-001-15 and -17, the last two of the approved plan.

Canonical plan: {{output/INC-010-epic-1-RWB-E1-001/plan/plan.md}}, {{tasks.md}}, {{tests/scenarios.md}}.

h2. Readiness — NOT READY, last in the dependency graph

Blocked by every other precondition, and by the three sibling sub-tasks.

||Precondition||Card||
|*PRE-6* RWB-E1-044 recovery Flyway configuration|[TB0001-1205|https://scbjira.atlassian.net/browse/TB0001-1205]|
|*PRE-7* RWB-E1-043 reference load endpoints, which TASK-15 tests against|[TB0001-1344|https://scbjira.atlassian.net/browse/TB0001-1344]|
|Sibling work|[TB0001-1356|https://scbjira.atlassian.net/browse/TB0001-1356], [TB0001-1357|https://scbjira.atlassian.net/browse/TB0001-1357] and the handler sub-task|

*PRE-9 is not linked here and has no card at all.* The Jenkins recovery deploy step must run as {{ACEDbFlywayRole_<ENV>}} (OPEN-019, held by K. Tee). It blocks deployment, not the build, so TASK-17 records it rather than waiting for it. Someone still has to raise it.

h2. Tasks

||Task||Work||
|TASK-15|Authorisation. TC-E1-001-11: RW-DATASTEW calling {{POST /admin/reference-loads}} with {{table = data_product}} is refused 403 with MSG-P4-002 *before* {{validate}} runs, and the refusal is in the access log with caller, capability and table code. TC-E1-001-18: RW-REFADM cannot confirm its own load as owner — that needs Reference data U. Both run against RWB-E1-043's endpoints; if those are not yet deployed, cover the handler side at unit level and *record the endpoint half as owed* rather than claiming it passed.|
|TASK-17|Consolidation and release readiness. Confirm every scope bullet in {{plan.md}} has a green task, all 16 deltas in {{data-model.md}} §3 are verified by TASK-03, the migration sequence was taken at merge and the merge-order map updated in the same MR, and {{implement/report.md}} records the ACE branch, commit SHAs and MR link so the traceability matrix can link story → spec → code. Record what could not be exercised from the repository: the deploy-job behaviour in DEV and SIT (OPEN-019).|

h2. Completion rules

* No unsecured endpoint, permissive fallback or bypass. Isolated test mocks do not prove integrated authorisation.
* Required tests must not be disabled or skipped to claim completion.
* The story cannot be declared complete while the endpoint half of TASK-15 is owed.

h2. Branch policy

D-RCV-50 as on the parent story.

## Linked issues

- is blocked by TB0001-1205: [RWB-E1-044] Database migrations versioned with parameterized schema names (Hold)
- is blocked by TB0001-1344: RWB-E1-043: Implementation Builder — reference data service with versioned tables (TASK-00..21) (To Do)

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
