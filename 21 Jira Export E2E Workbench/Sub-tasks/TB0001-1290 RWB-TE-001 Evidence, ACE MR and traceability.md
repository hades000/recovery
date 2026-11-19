# TB0001-1290 [RWB-TE-001] Evidence, ACE MR and traceability

| Field | Value |
|---|---|
| Jira | [TB0001-1290](https://scbjira.atlassian.net/browse/TB0001-1290) |
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
| Created | 2026-11-09T15:52:24.880+0700 |
| Updated | 2026-11-10T17:55:03.778+0700 |
| Due date | - |
| Resolved | 2026-11-10T17:55:03.757+0700 |
| Original estimate | 1h |
| Remaining estimate | 0m |
| Time spent | 1h |
| Votes | 0 |
| Watchers | 2 |
| Comments | 2 |

## Description

Covers *TASK-RWB-TE-001-18..20* of the approved plan.

Guardrails and shared-file footprint check, unit test evidence, ACE MR to develop (branch feature/TB0001-1235-recovery-module-boundary), traceability and release readiness in ace-aisdlc.

Task details (source of truth): [https://gitdop.se.scb.co.th/AP2477-ACE/ace-aisdlc/-/blob/main/recovery/output/INC-002-epic-1-RWB-TE-001/plan/tasks.md|https://gitdop.se.scb.co.th/AP2477-ACE/ace-aisdlc/-/blob/main/recovery/output/INC-002-epic-1-RWB-TE-001/plan/tasks.md]

Run with Claude Code in ace-aisdlc/recovery: /implement INC-002-epic-1-RWB-TE-001. Story points stay on the story.

## Comments (2)

### Comment 1: RACHATAPON PONGANANTAYOTIN, 2026-11-10T15:46:43.104+0700

Comment ID 1783560

h3. Acceptance evidence / MR gate clarification — RWB-TE-001

Parent: TB0001-1235.

*ไม่มี business AC ใน story ต้นฉบับ* โดย §7 ระบุ:
{quote}No business acceptance criteria. This story is an engineering enabler for module boundary tests; its development-process criteria were removed on 4 November 2026.{quote}
Source: repo {{AP2477-ACE/ace-aisdlc}}, {{recovery/requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB TE 001 Recovery module folder and boundary test v1.md}}, §7.

*เกณฑ์รับงาน*: D-RCV-16 กำหนด business rules BR1–BR6 + test cases ที่เหลือใน story แทน AC ที่ถูกนำออก. Evidence/traceability ต้องเชื่อม BR/test cases → SPEC → TASK → test results/MR ไม่ใช่สร้าง business AC ใหม่เอง. Access guard/TC-TE-001-08 อยู่นอก scope นี้ ย้ายไป RWB-E1-022 (D-RCV-36).

*MR pipeline evidence ที่ต้องแยกให้ชัด*
* Story §4 ข้อ 6–7 และ §13 ข้อ 7 ต้องการ backend boundary และ frontend dependency checks ที่ fail build เมื่อผิดกฎ.
* D-RCV-05 / SPEC-012/015/016 ใช้ build เดิม *ไม่เพิ่ม stage และไม่แก้ {{.gitlab-ci.yml}}*. Backend ผ่าน Gradle {{test}}; frontend ผ่าน ESLint/Vitest ใน Nx {{check}}.
* CI ที่ตรวจใน workspace จำกัด MR job ไว้ที่ target เป็น default branch โดย {{allow_failure: false}}; ยังไม่ใช่หลักฐานว่า MR ทุก target branch ถูกตรวจ.
* การห้าม merge จริงต้องยืนยัน project setting “Pipelines must succeed” และผล MR pipeline แยกต่างหาก; การตรวจ requirement ครั้งนี้ยังไม่ได้ยืนยันทั้งสองอย่าง.
* ข้อความ story ที่ยังขัดกับ decision ติดตาม BA ไว้ที่ OPEN-021.

หลักฐาน:
* [Decision log: D-RCV-05/16/36|https://gitdop.se.scb.co.th/AP2477-ACE/ace-aisdlc/-/blob/main/recovery/docs/decisions/INC-001-decisions.md]
* [Spec: coverage mapping และ SPEC-012/015/016/020|https://gitdop.se.scb.co.th/AP2477-ACE/ace-aisdlc/-/blob/main/recovery/output/INC-002-epic-1-RWB-TE-001/specify/spec.md]
* [Approved tasks: TASK-18..20|https://gitdop.se.scb.co.th/AP2477-ACE/ace-aisdlc/-/blob/main/recovery/output/INC-002-epic-1-RWB-TE-001/plan/tasks.md]
* [Parent comment 1780957: no business AC|https://scbjira.atlassian.net/browse/TB0001-1235?focusedCommentId=1780957]
* [Parent comment 1781003: TechX PO approval|https://scbjira.atlassian.net/browse/TB0001-1235?focusedCommentId=1781003]
* [OPEN-021|https://gitdop.se.scb.co.th/AP2477-ACE/ace-aisdlc/-/blob/main/recovery/docs/open-items.md]

คอมเมนต์นี้เป็นหลักฐาน requirement เท่านั้น ไม่ใช่ผลทดสอบผ่าน การยืนยัน merge protection หรือการอนุมัติปิดงาน.

### Comment 2: RACHATAPON PONGANANTAYOTIN, 2026-11-10T15:52:45.417+0700

Comment ID 1783621

h3. QA handoff evidence — BR1–BR6 and story cases, 10 Nov 2026

Fresh focused verification completed against ACE commit {{f144a1aa9b26ef30ff052ca4285850345ad9247c}}, branch {{feature/TB0001-1235-recovery-module-boundary}}.

* Backend: 23 passed, 0 failures/errors/skips; exit 0.
* Frontend: 2 passed, 0 failures/errors/skips; exit 0.
* BR1–BR6 / TC-TE-001-01..05 and 07: local fixture/actual-structure verification PASS against approved spec. Negative-fixture PASS means the expected violation was asserted.
* Frontend TC-TE-001-06 (Test Cases v5): approved allow-list behavior PASS (2 fixture tests).
* TC-TE-001-08: OUT OF SCOPE / NOT RUN; moved to RWB-E1-022 (D-RCV-36).
* Backend coverage: instructions 96.12%, branches 88.82%, lines 96.26%, methods 100%; all 80% gates pass. Frontend native 100% (0/0), not runtime UI coverage.

[Shareable QA summary with exact commands, test-method mapping, suite counts, fixture deviations and limitations|https://scbjira.atlassian.net/browse/TB0001-1235?focusedCommentId=1783617].

Persistent local evidence directory:
{{recovery/output/INC-002-epic-1-RWB-TE-001/implement/unit-tests/qa-br-verification-20261110T084952Z/}}
Includes report.md, backend/frontend logs and exit codes, JUnit XML, backend HTML report/JaCoCo XML, frontend coverage-summary.json and LCOV. These files are local, not yet committed/pushed or uploaded as Jira attachments. Do not treat a GitLab link to this new directory as published.

*Outstanding proof*: actual GitLab MR pipeline, failing-check merge blocking and project “Pipelines must succeed” setting were NOT tested. No new MR, commit, push, status change, fresh full ACE regression or QA acceptance is claimed. D-RCV-05 still requires reuse of existing CI with no new stage/CI YAML change.


## Other Jira fields

| Field | ID | Value |
|---|---|---|
| [CHART] Time in Status | customfield_10025 | 10569_*:*_1_*:*_0_*\|*_3_*:*_1_*:*_10388134_*\|*_10014_*:*_1_*:*_83303148 |
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
