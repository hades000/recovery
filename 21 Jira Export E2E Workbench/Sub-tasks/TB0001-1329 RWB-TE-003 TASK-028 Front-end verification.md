# TB0001-1329 [RWB-TE-003] TASK-028 Front-end verification

| Field | Value |
|---|---|
| Jira | [TB0001-1329](https://scbjira.atlassian.net/browse/TB0001-1329) |
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
| Created | 2026-11-10T11:53:41.254+0700 |
| Updated | 2026-11-11T11:16:07.337+0700 |
| Due date | - |
| Resolved | - |
| Original estimate | - |
| Remaining estimate | - |
| Time spent | - |
| Votes | 0 |
| Watchers | 1 |
| Comments | 0 |

## Description

*Story:* RWB-TE-003 — TB0001-1237 · *Plan task:* TASK-028 · *Surface:* Frontend (configuration)
*Blocked by:* TASK-027
*Held:* stage 7 waits for the plan-gate re-check of plan run 7, the approver's confirmation of the final commit (AC-PLAN-11) and OPEN-044. RWB-TE-001 is merged in ACE {{develop-recovery}} (2026-11-10).
*Plan text:* plan run 7 (2026-11-11; runs 5–6 approved by Jesniphat Pukkham 2026-11-10, final commit to be confirmed) — [tasks.md|https://gitdop.se.scb.co.th/AP2477-ACE/ace-aisdlc/-/blob/spec/INC-005-te-003-attempt-02/recovery/output/INC-005-epic-1-RWB-TE-003/plan/tasks.md] · [plan.md|https://gitdop.se.scb.co.th/AP2477-ACE/ace-aisdlc/-/blob/spec/INC-005-te-003-attempt-02/recovery/output/INC-005-epic-1-RWB-TE-003/plan/plan.md] on branch {{spec/INC-005-te-003-attempt-02}} (MR !21). Last approved version: {{fd93eb7}}.

h3. What to do

*Front-end verification* (unit tests NOT_APPLICABLE): BV-06 {{npx nx run frontend:typecheck}} runs {{generate-recovery-api}} first and passes; BV-07 from a clean state {{npm run build}} in {{frontend/}} creates no generated folder (CLAR-015); BV-08 {{npx nx run frontend:check}} passes with the generated folder present, including RWB-TE-001's Vitest {{test}} target (80% gate), whose coverage report does not list the generated folder; BV-05 {{git status --porcelain}} clean. Record the {{skipLibCheck}} limitation (R-10).

h3. Deliverable

{{implement/build-verification.md}} (front-end rows)

h3. Done when

Each BV row PASS with output

h3. Trace

SPEC-RWB-TE-003-004, SPEC-RWB-TE-003-005, SPEC-RWB-TE-003-016; FR-RWB-003

h3. Rules

* ACE repo {{ace-monorepo}}, branch {{feature/TB0001-1237-api-contract-tests}} from {{develop-recovery}}; merge request into {{develop-recovery}} (D-RCV-56); commits {{TB0001-1237: <summary>}}. Edit only the paths listed in plan §7.
* If _Done when_ cannot be met, stop and report.
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
