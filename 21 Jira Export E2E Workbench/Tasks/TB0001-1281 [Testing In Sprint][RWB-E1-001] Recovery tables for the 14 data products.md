# TB0001-1281 [Testing In Sprint][RWB-E1-001] Recovery tables for the 14 data products 

| Field | Value |
|---|---|
| Jira | [TB0001-1281](https://scbjira.atlassian.net/browse/TB0001-1281) |
| Type | Task |
| Status | To Do |
| Resolution | - |
| Parent | - |
| Epic link | - |
| Assignee | Piyawan Sanpanya |
| Reporter | Piyawan Sanpanya |
| Priority | Medium |
| Labels | TestInSprint |
| Components | E2E Workbench |
| Fix versions | - |
| Affects versions | - |
| Sprint | - |
| Team | - |
| Created | 2026-11-09T11:33:04.014+0700 |
| Updated | 2026-11-10T12:03:38.411+0700 |
| Due date | - |
| Resolved | - |
| Original estimate | - |
| Remaining estimate | - |
| Time spent | - |
| Votes | 0 |
| Watchers | 1 |
| Comments | 2 |

## Description

*Artifact*

*Test case :* 

      API testing: [^api-tests.zip] 

      Functional testing : [^functional-tests.zip] 

      QA Test Case Generator :  

Test Result : 

## Linked issues

- tests TB0001-1163: [RWB-E1-001] Recovery tables for the 14 data products (Dev In Progress)

## Sub-tasks

- TB0001-1282 [To Do] [QA] Prepare testcase for [RWB-E1-001] Recovery tables for the 14 data products
- TB0001-1283 [To Do] [QA] Review test case for [RWB-E1-001] Recovery tables for the 14 data products

## Attachments

- [api-tests.zip](../../Attachments/TB0001-1281/api-tests.zip) (2917 bytes, Piyawan Sanpanya, 2026-11-09T11:48:04.356+0700)
- [functional-tests.zip](../../Attachments/TB0001-1281/functional-tests.zip) (3020 bytes, Piyawan Sanpanya, 2026-11-09T11:49:44.246+0700)

## Comments (2)

### Comment 1: Piyawan Sanpanya, 2026-11-10T10:20:06.327+0700

Comment ID 1782345

h2. QA Test Case Generation — Validation Summary (TB0001-1163)

สร้าง test case ทั้งหมด 15 รายการสำหรับ TB0001-1163 (RWB-E1-001: Recovery tables for the 14 data products) โดยอ้างอิง story เดิมและ spec.md ที่ผ่านการ cross-check กับ decision-log D-RCV-28/D-RCV-29 (AC1 ถูกตัดออกตั้งแต่ 4 พ.ย. 2026)

h3. Coverage Summary

||ประเภท||พบทั้งหมด||Dedicated TC||Covered-by-AC||
|Acceptance Criteria (AC)|6 (AC2,3,7,8,9,10)|6|0|
|Business Rules (BL)|7 (BR1-7)|4 (BR1,5,6,7)|3 (BR2→AC3, BR3→AC3/7, BR4→AC7/8/9/10)|
|Exception/Error Handling (EH)|8 (X1-8)|4 (X1,2,3,8)|4 (X4→AC7, X5→AC8, X6→AC9, X7→AC10)|
|General (GEN)|1|1 (feature flag off)|-|

h3. รายการที่พิจารณาแล้วไม่สร้าง TC แยก

* {{DataProductCatalogHandler.tableCode()}} contract — internal mechanism ที่ทุก catalog-load TC ทดสอบผ่านอยู่แล้วโดยอ้อม ไม่ใช่สิ่งที่สังเกตได้อิสระ
* ขั้นตอน "RW-DATASTEW confirms the load as owner" — นอกขอบเขตของ story นี้ (ของ dependency RWB-E1-043)

h3. Validation Table

||TC ID||Source||Reference||Status||Notes||
|TC-001|AC|AC2|✅ Covered|v_data_dictionary field mapping|
|TC-002|AC|AC3|✅ Covered|Smoke — ตรงกับ "Done when"|
|TC-003|AC|AC7/X4|✅ Covered|Dual coverage|
|TC-004|AC|AC8/X5|✅ Covered|Dual coverage|
|TC-005|AC|AC9/X6|✅ Covered|Dual coverage|
|TC-006|AC|AC10/X7|✅ Covered|Dual coverage|
|TC-007|BL|BR1|✅ Covered|Smoke — migration+dictionary conformance|
|TC-008|BL|BR5|✅ Covered|DP07/DP13 ไม่ซ้ำกับ AC3(DP06)|
|TC-009|BL|BR6|✅ Covered|Overlap กับ X3 โดยเจตนา|
|TC-010|BL|BR7|✅ Covered|is_personal flag|
|TC-011|EH|X1|✅ Covered|Migration rollback|
|TC-012|EH|X2|✅ Covered|Conformance test fail|
|TC-013|EH|X3|✅ Covered|Idempotent re-run|
|TC-014|EH|X8|✅ Covered|403 authority refusal|
|TC-015|GEN|Feature flag|✅ Covered|rwb.p1.data-catalog off|

*รวมทั้งหมด: 15 test cases*

Test case files อยู่ที่ repo path: {{recovery/output/test-cases/TB0001-1163/}} (พร้อม index.md)

หมายเหตุ: ยังไม่ได้สร้าง Jira issue ย่อยสำหรับแต่ละ test case รอ QA/ผู้เกี่ยวข้องรีวิวและยืนยันก่อนตามกฎของ QA Test Case Generator agent

### Comment 2: Piyawan Sanpanya, 2026-11-10T10:33:11.689+0700

Comment ID 1782420

h3. เพิ่มเติม (Addendum) — ยืนยันความครบถ้วนของ Acceptance Criteria Coverage

อ้างอิงจาก comment สรุปผลการตรวจสอบก่อนหน้านี้ ขอแจ้งข้อมูลเพิ่มเติมเพื่อเป็นหลักฐานยืนยันว่าการ generate test case ได้ครอบคลุม Acceptance Criteria ครบถ้วนตามเนื้อหา story ฉบับปัจจุบันแล้ว ดังนี้

h4. 1. Acceptance Criteria ที่มีผลบังคับใช้ในปัจจุบัน (Active ACs)

Story มี Acceptance Criteria ที่ยังมีผลบังคับใช้ทั้งหมด 6 รายการ ได้แก่ AC2, AC3, AC7, AC8, AC9, AC10 โดยแต่ละรายการมี test case รองรับแบบ 1 ต่อ 1 ครบถ้วนดังนี้

||Acceptance Criteria||Test Case||
|AC2|TC-001|
|AC3|TC-002|
|AC7|TC-003|
|AC8|TC-004|
|AC9|TC-005|
|AC10|TC-006|

สรุป: ครอบคลุม 6/6 (100%) ของ Acceptance Criteria ที่มีผลบังคับใช้ในปัจจุบัน

h4. 2. AC1 (ถูกถอดออกจาก story แล้ว)

AC1 ถูกถอดออกจาก story ตามการปรับปรุงเมื่อวันที่ 4 พฤศจิกายน 2026 ซึ่งมีการยืนยันไว้ทั้งใน increment card และ spec.md (decision log D-RCV-28, D-RCV-29) เนื้อหาเดิมของ AC1 ถูกย้ายไปกำหนดไว้ภายใต้ BR1 และ exception path X1/X2/X3 แทน ซึ่งได้มี test case รองรับครบถ้วนแล้วเช่นกัน ได้แก่ TC-007 (BR1), TC-011 (X1), TC-012 (X2), TC-013 (X3)

h4. 3. AC4, AC5, AC6

ไม่มีเนื้อหา AC4, AC5, AC6 ปรากฏอยู่ใน story ทั้งฉบับ legacy และฉบับ spec.md ปัจจุบัน (ลำดับ Acceptance Criteria ในเอกสารต้นทางระบุต่อเนื่องจาก AC3 ไปยัง AC7 โดยตรง) จึงไม่มีข้อมูลตั้งต้นสำหรับสร้าง test case ในส่วนนี้

h4. สรุป

การ generate test case ทั้ง 15 รายการครอบคลุม Acceptance Criteria ที่มีผลบังคับใช้ในปัจจุบันครบถ้วน 100% (6/6) รวมถึงครอบคลุมเนื้อหาของ AC1 เดิมผ่าน Business Rule และ Exception path ที่เกี่ยวข้องแล้ว ไม่มี Acceptance Criteria รายการใดถูกข้ามหรือละเว้นโดยไม่มีเหตุผลรองรับ


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
