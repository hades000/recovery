# TB0001-1288 [RWB-TE-001] BE - JaCoCo coverage and backend check

| Field | Value |
|---|---|
| Jira | [TB0001-1288](https://scbjira.atlassian.net/browse/TB0001-1288) |
| Type | Sub-task |
| Status | Done |
| Resolution | Resolved |
| Parent | TB0001-1235 |
| Epic link | - |
| Assignee | RACHATAPON PONGANANTAYOTIN |
| Reporter | Jesniphat Pukkham |
| Priority | Medium |
| Labels | - |
| Components | E2E Workbench |
| Fix versions | - |
| Affects versions | - |
| Sprint | Delivery Workbench Q4S1 Squad2 |
| Team | RWB_SQ1 |
| Created | 2026-11-09T15:52:23.087+0700 |
| Updated | 2026-11-10T17:55:53.837+0700 |
| Due date | - |
| Resolved | 2026-11-10T17:55:53.812+0700 |
| Original estimate | 1h |
| Remaining estimate | 0m |
| Time spent | 1h |
| Votes | 0 |
| Watchers | 2 |
| Comments | 2 |

## Description

Covers *TASK-RWB-TE-001-11..12* of the approved plan.

JaCoCo 0.8.14 recovery-only coverage tasks in backend/build.gradle.kts (OPEN-023 approved), checkstyleMain/checkstyleTest and the backend regression and 80% coverage gate.

Task details (source of truth): [https://gitdop.se.scb.co.th/AP2477-ACE/ace-aisdlc/-/blob/main/recovery/output/INC-002-epic-1-RWB-TE-001/plan/tasks.md|https://gitdop.se.scb.co.th/AP2477-ACE/ace-aisdlc/-/blob/main/recovery/output/INC-002-epic-1-RWB-TE-001/plan/tasks.md]

Run with Claude Code in ace-aisdlc/recovery: /implement INC-002-epic-1-RWB-TE-001. Story points stay on the story.

## Comments (2)

### Comment 1: RACHATAPON PONGANANTAYOTIN, 2026-11-10T15:46:41.947+0700

Comment ID 1783558

h3. Acceptance evidence / MR gate clarification — RWB-TE-001

Parent: TB0001-1235.

*ไม่มี business AC ใน story ต้นฉบับ* โดย §7 ระบุ:
{quote}No business acceptance criteria. This story is an engineering enabler for module boundary tests; its development-process criteria were removed on 4 November 2026.{quote}
Source: repo {{AP2477-ACE/ace-aisdlc}}, {{recovery/requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB TE 001 Recovery module folder and boundary test v1.md}}, §7.

*ไม่ได้ยกเว้น acceptance/testing*: D-RCV-16 ให้รับงานตาม BR1–BR6 และ test cases ที่เหลือใน story; subtask นี้ยังต้องมี JaCoCo recovery-only coverage, backend regression/checkstyle และหลักฐาน coverage 80% ตาม approved plan TASK-11..12 และ SPEC-020. การไม่มี business AC ไม่ได้ยกเว้น coverage gate.

*Pipeline scope*: D-RCV-05 และ SPEC-012/016 ระบุใช้ unit tests ใน build เดิม *ไม่แก้ {{.gitlab-ci.yml}} และไม่เพิ่ม pipeline stage*. อย่าสรุปว่า task coverage ถูกผูกกับ MR pipeline โดยอัตโนมัติเพียงเพราะเพิ่ม JaCoCo task; ต้องแยกหลักฐานการรัน coverage task ออกจากหลักฐาน backend {{test/check}} และ MR pipeline.

หลักฐาน:
* [D-RCV-05 / D-RCV-06 / D-RCV-16 / D-RCV-40|https://gitdop.se.scb.co.th/AP2477-ACE/ace-aisdlc/-/blob/main/recovery/docs/decisions/INC-001-decisions.md]
* [Spec: SPEC-012/016/018/020|https://gitdop.se.scb.co.th/AP2477-ACE/ace-aisdlc/-/blob/main/recovery/output/INC-002-epic-1-RWB-TE-001/specify/spec.md]
* [Approved task details|https://gitdop.se.scb.co.th/AP2477-ACE/ace-aisdlc/-/blob/main/recovery/output/INC-002-epic-1-RWB-TE-001/plan/tasks.md]
* [Parent comment 1780957: no business AC|https://scbjira.atlassian.net/browse/TB0001-1235?focusedCommentId=1780957]

การ block merge จริงต้องยืนยัน GitLab “Pipelines must succeed” แยกต่างหาก; คอมเมนต์นี้เป็นหลักฐาน requirement ไม่ใช่ผลทดสอบผ่านหรือการอนุมัติปิดงาน.

### Comment 2: RACHATAPON PONGANANTAYOTIN, 2026-11-10T15:52:43.486+0700

Comment ID 1783618

h3. QA result — backend verification and coverage, 10 Nov 2026

*PASS for focused local verification.* ACE commit {{f144a1aa9b26ef30ff052ca4285850345ad9247c}}; branch {{feature/TB0001-1235-recovery-module-boundary}}. No source changes.

Fresh Java 21 Gradle run executed recovery architecture tests plus existing ModulithTest, recoveryCoverageReport and recoveryCoverageVerification with --rerun-tasks: *23 passed / 0 failed / 0 errors / 0 skipped*, exit 0, BUILD SUCCESSFUL in 23s.

||JaCoCo metric||Covered / total||Percent||80% gate||
|Instructions (statement proxy)|1488/1548|96.12%|PASS|
|Branches|151/170|88.82%|PASS|
|Lines|309/321|96.26%|PASS|
|Methods (function proxy)|63/63|100.00%|PASS|

Scope is recovery production classes plus approved test-scope architecture tooling, not all ACE modules. This focused run did not rerun checkstyle/full ACE regression and does not claim their fresh completion. Recovery coverage tasks were explicitly requested; this is not evidence that CI automatically invokes them or that GitLab blocks merge.

[Full command, BR1–BR6/story-case mapping, suite counts and limitations|https://scbjira.atlassian.net/browse/TB0001-1235?focusedCommentId=1783617].
Local native evidence: {{recovery/output/INC-002-epic-1-RWB-TE-001/implement/unit-tests/qa-br-verification-20261110T084952Z/backend/}}. Contains JaCoCo XML, JUnit XML, HTML report, log and exit-code.txt; not yet published/attached. No QA sign-off/status change implied.


## Other Jira fields

| Field | ID | Value |
|---|---|---|
| [CHART] Time in Status | customfield_10025 | 3_*:*_1_*:*_0_*\|*_10014_*:*_1_*:*_83297905 |
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
| Created Date | customfield_10249 | 2026-11-09 |
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
