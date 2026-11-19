# TB0001-1297 [RWB-TE-003] Plan and task review — FDA plan approval, FDE task approval

| Field | Value |
|---|---|
| Jira | [TB0001-1297](https://scbjira.atlassian.net/browse/TB0001-1297) |
| Type | Sub-task |
| Status | Done |
| Resolution | Resolved |
| Parent | TB0001-1237 |
| Epic link | - |
| Assignee | Jesniphat Pukkham |
| Reporter | thanapat khumprom |
| Priority | Medium |
| Labels | - |
| Components | E2E Workbench |
| Fix versions | - |
| Affects versions | - |
| Sprint | Delivery Workbench Q4S1 Squad2; Delivery Workbench Q4S2 Squad2 |
| Team | RWB_SQ2 |
| Created | 2026-11-10T10:45:28.335+0700 |
| Updated | 2026-11-10T10:52:10.970+0700 |
| Due date | - |
| Resolved | 2026-11-10T10:52:10.938+0700 |
| Original estimate | 1m |
| Remaining estimate | 0m |
| Time spent | 1m |
| Votes | 0 |
| Watchers | 2 |
| Comments | 1 |

## Description

Please review the implementation plan for RWB-TE-003 (AISDLC stage 6) and reply in this ticket.

*Files* (repo {{AP2477-ACE/ace-aisdlc}}, branch {{spec/INC-005-te-003-attempt-02}}, commit {{37645a9}}):

* Plan: https://gitdop.se.scb.co.th/AP2477-ACE/ace-aisdlc/-/blob/spec/INC-005-te-003-attempt-02/recovery/output/INC-005-epic-1-RWB-TE-003/plan/plan.md
* Tasks (38): https://gitdop.se.scb.co.th/AP2477-ACE/ace-aisdlc/-/blob/spec/INC-005-te-003-attempt-02/recovery/output/INC-005-epic-1-RWB-TE-003/plan/tasks.md
* Plan-gate review (runs 1–3): https://gitdop.se.scb.co.th/AP2477-ACE/ace-aisdlc/-/blob/spec/INC-005-te-003-attempt-02/recovery/output/INC-005-epic-1-RWB-TE-003/review/plan-review.md

*Questions to answer first* (review run 3 is FAIL because of question 1):

# *REVIEW-P-13 (Medium).* The record says you acknowledged the new dependencies and the shared ACE file edits _as ACE tech lead_ (OPEN-026). Other records list the ACE tech lead as a separate person. Are you the ACE tech lead? If not, who is? The plan cannot be approved until this is settled.
# *REVIEW-P-18 (Low).* OPEN-024 was closed on RW-SECADM's confirmation relayed by you, without RW-SECADM's name. Do you, as FDA, accept that basis? Who is the RW-SECADM person to name before RWB-E1-037 switches the access test on?
# *REVIEW-P-14..17, -19 (Low).* Fix them in plan run 4, or accept them as they are?

*Then, if you agree:*

* Plan approval (FDA): accept the plan and planner decisions PD-01..PD-12 and PD-14 (AC-PLAN-05). This includes one generated interface per API operation, so an operation nobody has built has no route.
* Task approval (FDE): accept {{tasks.md}} (TASK-001..038).
* AC-PLAN-07: wait for BA Henka to reissue the story (OPEN-016), or allow work to continue on the approved decisions.

Implementation stays on hold until RWB-TE-001 is merged in ACE {{develop}}.

## Comments (1)

### Comment 1: Jesniphat Pukkham, 2026-11-10T10:48:24.380+0700

Comment ID 1782498

Approved


## Other Jira fields

| Field | ID | Value |
|---|---|---|
| [CHART] Time in Status | customfield_10025 | 10569_*:*_1_*:*_0_*\|*_3_*:*_1_*:*_2567_*\|*_10014_*:*_1_*:*_264400 |
| Actual End Date | customfield_14458 | 2026-11-10 |
| Actual Start Date | customfield_14457 | 2026-11-10 |
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
