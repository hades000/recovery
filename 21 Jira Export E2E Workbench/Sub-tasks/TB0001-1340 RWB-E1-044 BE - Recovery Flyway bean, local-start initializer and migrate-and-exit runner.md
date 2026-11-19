# TB0001-1340 [RWB-E1-044] BE - Recovery Flyway bean, local-start initializer and migrate-and-exit runner

| Field | Value |
|---|---|
| Jira | [TB0001-1340](https://scbjira.atlassian.net/browse/TB0001-1340) |
| Type | Sub-task |
| Status | To Do |
| Resolution | - |
| Parent | TB0001-1205 |
| Epic link | - |
| Assignee | - |
| Reporter | Jesniphat Pukkham |
| Priority | Medium |
| Labels | - |
| Components | E2E Workbench |
| Fix versions | - |
| Affects versions | - |
| Sprint | Delivery Workbench Q4S1 Squad2; Delivery Workbench Q4S2 Squad2 |
| Team | RWB_SQ2 |
| Created | 2026-11-10T13:43:49.874+0700 |
| Updated | 2026-11-10T15:29:46.903+0700 |
| Due date | - |
| Resolved | - |
| Original estimate | - |
| Remaining estimate | - |
| Time spent | - |
| Votes | 0 |
| Watchers | 1 |
| Comments | 0 |

## Description

Covers TASK-RWB-E1-044-00..05 of the approved plan.

Precondition check, branch from develop, Testcontainers PostgreSQL test dependency and test tasks in backend/build.gradle.kts (D-RCV-49), RecoveryFlywayConfig (schema ace, rwb_ prefix, baseline 0, createSchemas(false)), profile db-migrate-recovery activation, initializer with failure reporting, RecoveryMigrationExit runner and application-db-migrate-recovery.yaml.

Task details (source of truth): [https://gitdop.se.scb.co.th/AP2477-ACE/ace-aisdlc/-/blob/main/recovery/output/INC-001-epic-1-RWB-E1-044/plan/tasks.md|https://gitdop.se.scb.co.th/AP2477-ACE/ace-aisdlc/-/blob/main/recovery/output/INC-001-epic-1-RWB-E1-044/plan/tasks.md]

Run with Claude Code in ace-aisdlc/recovery: /implement INC-001-epic-1-RWB-E1-044. ACE develop must be at or after 9f450bbd. Story points stay on the story.

Update 2026-11-10 (D-RCV-50): cut the branch from develop-recovery (it holds RWB-TE-001, 7050e771; bring it up to date with develop first) and open the ACE MR into develop-recovery, not develop. ACE reviews shared files at the develop-recovery to develop batch MR.

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
