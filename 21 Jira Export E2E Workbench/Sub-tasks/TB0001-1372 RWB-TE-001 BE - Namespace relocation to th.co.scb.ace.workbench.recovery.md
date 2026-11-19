# TB0001-1372 [RWB-TE-001] BE - Namespace relocation to th.co.scb.ace.workbench.recovery

| Field | Value |
|---|---|
| Jira | [TB0001-1372](https://scbjira.atlassian.net/browse/TB0001-1372) |
| Type | Sub-task |
| Status | Done |
| Resolution | Resolved |
| Parent | TB0001-1235 |
| Epic link | - |
| Assignee | RACHATAPON PONGANANTAYOTIN |
| Reporter | RACHATAPON PONGANANTAYOTIN |
| Priority | Medium |
| Labels | - |
| Components | E2E Workbench |
| Fix versions | - |
| Affects versions | - |
| Sprint | Delivery Workbench Q4S1 Squad2 |
| Team | RWB_SQ1 |
| Created | 2026-11-11T17:11:01.236+0700 |
| Updated | 2026-11-12T10:08:44.476+0700 |
| Due date | - |
| Resolved | 2026-11-12T10:08:44.456+0700 |
| Original estimate | 2h |
| Remaining estimate | 0m |
| Time spent | 2h |
| Votes | 0 |
| Watchers | 1 |
| Comments | 0 |

## Description

h2. Scope
2026-11-11 namespace amendment (D-RCV-51): relocate the completed recovery package subtree from {{th.co.scb.ace.demo.recovery}} to {{th.co.scb.ace.workbench.recovery}}. Backend-only; no UI/API change. Does not reopen TB0001-1287..1290 (Done, baseline).

h2. Trace
* Spec: SPEC-RWB-TE-001-021..024 ({{output/INC-002-epic-1-RWB-TE-001/specify/spec.md}} "Active amendment")
* Plan/Tasks: TASK-RWB-TE-001-21..31 ({{output/INC-002-epic-1-RWB-TE-001/plan/plan.md}}, {{plan/tasks.md}} "Active amendment" / "Amendment task table")
* Plan gate: {{review/plan-gate-review-4.md}} (FAIL, remediated) → {{review/plan-gate-review-5.md}} (PASS)

h2. Work
* Relocate 58 main {{package-info.java}} + 8 test-scope architecture tooling files to the new root
* Update module map {{rootPackage}} in {{recovery-modules.yaml}}
* Add {{RecoveryModuleDiscoveryTest}} (actual-host discovery assertion, 19 modules)
* Reconcile {{backend/build.gradle.kts}}: add {{jacoco}} + {{recoveryCoverageReport}}/{{recoveryCoverageVerification}} over the new paths
* Re-run fixture/rule/loader suites; regression + 80% coverage gate; update traceability matrix

h2. Approvals
PRE-DELTA-1 (D-RCV-51 technical scope) and PRE-DELTA-2 (PO spec approval) were approved 2026-11-11 via Jira comments 1785735/1785826/1785987 on the parent TB0001-1235.

PRE-DELTA-3 (FDA plan approval) and PRE-DELTA-4 (FDE task approval) are *APPROVED*, 2026-11-11, after plan gate 5 PASS ({{review/plan-gate-review-5.md}}). Recorded in {{docs/increments/INC-002-epic-1-RWB-TE-001.md}} "Owners and approvals". Note: relayed by the assignee (Rachatapon Ponganantayotin) in the AISDLC Claude Code session, not a direct Jesniphat Pukkham statement in-session or a Jira comment — no exact time/channel given.

Status: unblocked for {{/implement}}.

## Comments (0)

(none)

## Other Jira fields

| Field | ID | Value |
|---|---|---|
| [CHART] Time in Status | customfield_10025 | 3_*:*_1_*:*_0_*\|*_10014_*:*_1_*:*_1866738 |
| Actual End Date | customfield_14458 | 2026-11-12 |
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
| Story Point | customfield_17479 | 1 |
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
