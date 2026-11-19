# TB0001-1355 [RWB-TE-005] Evidence, ACE MR and traceability

| Field | Value |
|---|---|
| Jira | [TB0001-1355](https://scbjira.atlassian.net/browse/TB0001-1355) |
| Type | Sub-task |
| Status | To Do |
| Resolution | - |
| Parent | TB0001-1239 |
| Epic link | - |
| Assignee | - |
| Reporter | Chayaporn Kaewin |
| Priority | Medium |
| Labels | - |
| Components | E2E Workbench |
| Fix versions | - |
| Affects versions | - |
| Sprint | Delivery Workbench Q4S1 Squad1 |
| Team | - |
| Created | 2026-11-11T15:00:35.613+0700 |
| Updated | 2026-11-16T09:13:21.906+0700 |
| Due date | - |
| Resolved | - |
| Original estimate | - |
| Remaining estimate | - |
| Time spent | - |
| Votes | 0 |
| Watchers | 1 |
| Comments | 0 |

## Description

Source: output/INC-006-epic-1-RWB-TE-005/plan/tasks.md (section "Verification, gates and evidence", part 2).

h4. TASK-RWB-TE-005-16 — Evidence, handoff and traceability
{{output/INC-006-epic-1-RWB-TE-005/implement/unit-tests/report.md}} with the Unit Test Evidence table per {{.github/rules/implementation-execution-gates.md}} (Backend rows for the unit gate and the combined gate, Frontend NOT_APPLICABLE with the plan rationale; no average). Record ACE branch, commit SHAs, MR link (only when the user asks), the {{recoveryIntegrationTest}} run SHA. Handoff note {{implement/handoff-e1-029.md}} with HC-1..HC-8 as written in plan.md for the RWB-E1-029 Builder and Planner, and the open points: the VALIDATED/FAILED status values (HC-2, {{HV-TE005-03}}); no evaluator owner ({{GAP-TE005-01}}); Unique/FIRST conflict (PD-01) for Context Updater; the proposed row for {{docs/architecture/migration-merge-order-map.md}} (PD-07: story RWB-TE-005, name {{V<seq>__rwb_te_005_rule_test_case.sql}}); {{rwb.environment}} and {{rwb.p3.rule-harness}} for K. Tee (HC-8). List {{HV-TE005-01..07}}. Record the E1-029 conflict (E1-029 refuses a load whole on a failing test and stores LOADED; TE-005 retains a FAILED version, HC-3/HC-4) and the three additive contract fields (PD-04) in the handoff note. In the Unit Test Evidence table, "statements" is the JaCoCo INSTRUCTION counter. Update {{requirement/Traceability_Matrix.md}} (TASK and CODE refs for RWB-TE-005). Effective-screen coverage consolidation: NOT_APPLICABLE (UI NO, 0 screens). State that fixtures are hand-built synthetic codes because the synthetic generator (RWB-E1-065) is not built.
*Trace:* SPEC-001..-011 (trace); REQ-CWC-013, -014; FR-RWB-008
*Blocked by:* TASK-RWB-TE-005-15
*Verification:* Files present; matrix row carries TASK and CODE refs; HV list and handoff note in implement/

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
