# TB0001-1282 [QA] Prepare testcase for [RWB-E1-001] Recovery tables for the 14 data products

| Field | Value |
|---|---|
| Jira | [TB0001-1282](https://scbjira.atlassian.net/browse/TB0001-1282) |
| Type | Sub-task |
| Status | To Do |
| Resolution | - |
| Parent | TB0001-1281 |
| Epic link | - |
| Assignee | - |
| Reporter | Piyawan Sanpanya |
| Priority | Medium |
| Labels | - |
| Components | E2E Workbench |
| Fix versions | - |
| Affects versions | - |
| Sprint | - |
| Team | - |
| Created | 2026-11-09T11:37:17.999+0700 |
| Updated | 2026-11-10T15:50:08.772+0700 |
| Due date | - |
| Resolved | - |
| Original estimate | - |
| Remaining estimate | - |
| Time spent | - |
| Votes | 0 |
| Watchers | 1 |
| Comments | 0 |

## Description

{code:sql}ตัวอย่าง Request/Response — POST /admin/reference-loads
โครงสร้างด้านล่างอิงจาก OpenAPI spec (recovery-workbench-api-specification-v2.yaml บรรทัด 2955-3001, 
schema ReferenceLoad บรรทัด 8812-8826,
schema Problem บรรทัด 8971-8989)
ส่วน ค่าตัวอย่าง (uuid, timestamp, ข้อความ) เป็นค่าที่ใส่ไว้เพื่อให้เห็นภาพเท่านั้น ไม่ได้มาจาก spec โดยตรง เพราะ spec ระบุแค่ชื่อฟิลด์กับ type ไม่ได้ให้ค่าตัวอย่างไว้

Request (201 success case — อ้างอิง test data ของ TC-002)

POST /admin/reference-loads HTTP/1.1
Authorization: Bearer <token>
Idempotency-Key: 3f29b1d2-7f44-4b1a-9e02-1f6a9c2d8e71
Content-Type: multipart/form-data; boundary=----WebKitBoundary

------WebKitBoundary
Content-Disposition: form-data; name="table"

data_product
------WebKitBoundary
Content-Disposition: form-data; name="validFrom"

2026-11-20
------WebKitBoundary
Content-Disposition: form-data; name="file"; filename="data_product_catalog_2026-11-20.csv"
Content-Type: text/csv

product_code,system_of_record,owner_user_id,refresh_cycle
DP01,...,...,...
...
DP06,CCMS,...,WEEKLY
...
DP14,...,...,...
------WebKitBoundary--
ฟิลด์ file / table / validFrom เป็นฟิลด์เดียวที่ schema ระบุไว้ชัดเจนสำหรับ endpoint นี้ (บรรทัด 2966-2979) — Idempotency-Key header เป็น mechanism ทั่วไปของระบบ (TSD P2) ไม่ได้ประกาศไว้ใน endpoint นี้โดยตรงแต่ปรากฏในตาราง TSD P4 สำหรับ API-P4-005

Response — 201 Created

{
  "id": "b6f0b9b0-6e2b-4a3a-8e93-9b2b7a0b7a10",
  "table": "data_product",
  "validFrom": "2026-11-20",
  "status": "LOADED",
  "rows": 14
}
หมายเหตุ: status schema ระบุแค่ type: string ไม่มี enum ค่าที่เป็นไปได้ระบุไว้ใน spec — "LOADED" เป็นค่าตัวอย่างที่ใส่ให้สมเหตุสมผลเท่านั้น ไม่ใช่ค่าที่ยืนยันจาก spec

Response — 403 Forbidden (ไม่มี Reference data C → TC-014)

{
  "type": "about:blank",
  "title": "Forbidden",
  "status": 403,
  "detail": "The role lacks the right in the capability area.",
  "messageCode": "MSG-P4-002",
  "field": null,
  "traceId": "a1b2c3d4-e5f6-4a3b-9c8d-1e2f3a4b5c6d"
}
Response — 422 Unprocessable Entity (ขาด DP09 → TC-004/AC8)

{
  "type": "about:blank",
  "title": "Unprocessable Entity",
  "status": 422,
  "detail": "Row missing for DP09",
  "messageCode": "MSG-P1-004",
  "field": "DP09",
  "traceId": "a1b2c3d4-e5f6-4a3b-9c8d-1e2f3a4b5c7e"
}
Response — 409 Conflict (โหลดไฟล์เดิมซ้ำ → TC-006/AC10)

{
  "type": "about:blank",
  "title": "Conflict",
  "status": 409,
  "detail": "The data product catalog load for 2026-11-20 is already complete or running. It was not run again.",
  "messageCode": "MSG-P1-011",
  "field": null,
  "traceId": "a1b2c3d4-e5f6-4a3b-9c8d-1e2f3a4b5c8f"
}
ข้อควรระวัง: legacy story (บรรทัด 123-127) ไม่ได้ระบุ HTTP status code ของเคสนี้ตรงๆ — ที่ใส่เป็น 409 เพราะ 409 คือโค้ดเดียวในชุด response ของ endpoint นี้ (401/403/409/422/503) ที่ความหมาย "Conflict. The state does not allow the action..." ตรงกับ "โหลดซ้ำแล้วปฏิเสธเพราะมีงานทำไปแล้ว" แต่นี่เป็น การอนุมานจากฉัน ไม่ใช่ข้อความยืนยันตรงจาก spec — ถ้าต้องการความแน่นอน ควรยืนยันกับทีม backend/ผู้ออกแบบ API อีกครั้งก่อนนำไปอ้างอิงใน test case

ทุก error response ใช้ schema Problem เดียวกัน (type, title, status, detail, messageCode, messageTh, field, traceId) ตาม OpenAPI บรรทัด 8971-8989 — ในตัวอย่างข้างต้นผมละ messageTh ไว้ เพราะไม่มีข้อความไทยที่ยืนยันแน่ชัดจาก spec ที่อ่านมา



ตัวอย่างการใช้งาน endpoint นี้
ได้ครับ — Postman ไม่ได้ต่อ raw HTTP แบบที่เขียนให้ดูก่อนหน้า มันแบ่งเป็น 
tab: Headers กับ 
Body → form-data และปล่อยให้ Postman set Content-Type/boundary ให้เองอัตโนมัติ 
(ห้ามพิมพ์ Content-Type: multipart/form-data เองใน Headers tab เดี๋ยว boundary จะเพี้ยน)

1. Method + URL

POST  {{base_url}}/admin/reference-loads
2. Headers tab
Key	Value
Authorization	Bearer <token>
Idempotency-Key	3f29b1d2-7f44-4b1a-9e02-1f6a9c2d8e71
อย่าใส่ Content-Type เอง — Postman จะใส่ multipart/form-data; boundary=... ให้อัตโนมัติตอนเลือก Body type = form-data

3. Body tab → เลือก form-data
KEY	TYPE	VALUE
table	Text	data_product
validFrom	Text	2026-11-20
file	File	เลือกไฟล์ (กดปุ่ม Select Files แล้วแนบ .csv)
(column "TYPE" ใน Postman ต้องกดสลับจาก Text → File เฉพาะแถว file เท่านั้น)

4. ไฟล์ CSV ที่จะแนบ (data_product_catalog_2026-11-20.csv)
ใช้ค่า system_of_record/refresh_cycle จริงจาก seed data ใน legacy story (section 13, บรรทัด 285-298) ส่วน owner_user_id เป็น uuid ตัวอย่าง (ไม่มีค่าจริงระบุใน spec — ต้องแทนด้วย user ID จริงจากระบบ):


product_code,system_of_record,owner_user_id,refresh_cycle
DP01,Core bank (ALS) via COLLINS,11111111-0000-0000-0000-000000000001,DAILY
DP02,SCBPDM via COLLINS,11111111-0000-0000-0000-000000000002,DAILY
DP03,Workbench,11111111-0000-0000-0000-000000000003,DAILY
DP04,Workbench,11111111-0000-0000-0000-000000000004,DAILY
DP05,Workbench,11111111-0000-0000-0000-000000000005,DAILY
DP06,CCMS,11111111-0000-0000-0000-000000000006,WEEKLY
DP07,LIT via COLLINS,11111111-0000-0000-0000-000000000007,DAILY
DP08,Workbench,11111111-0000-0000-0000-000000000008,DAILY
DP09,Workbench,11111111-0000-0000-0000-000000000009,DAILY
DP10,Workbench document hub,11111111-0000-0000-0000-000000000010,DAILY
DP11,COLLINS,11111111-0000-0000-0000-000000000011,DAILY
DP12,Workbench,11111111-0000-0000-0000-000000000012,DAILY
DP13,Workbench,11111111-0000-0000-0000-000000000013,DAILY
DP14,Workbench,11111111-0000-0000-0000-000000000014,DAILY
⚠️ หมายเหตุ: คอลัมน์ system_of_record สำหรับ DP06/DP07/DP13 เอกสารระบุว่าเป็น "(assumed, DL12)" — คือยังไม่ยืนยันจาก data steward ส่วน owner_user_id ทั้งหมดเป็น uuid ตัวอย่างที่ผมใส่เองเพื่อให้ format ถูกต้อง ไม่ใช่ user ID จริงของระบบ ต้องเปลี่ยนเป็นของจริงก่อนยิงจริงนะครับ

ขั้นตอนทำใน Postman
สร้าง request ใหม่ → Method = POST, URL ใส่ตามข้างบน
Tab Headers → ใส่ Authorization กับ Idempotency-Key 2 แถวตามตาราง
Tab Body → เลือก radio form-data
พิมพ์ key table → value data_product
พิมพ์ key validFrom → value 2026-11-20
พิมพ์ key file → กดสลับ dropdown ข้าง value จาก Text เป็น File → กด Select Files → เลือกไฟล์ csv ที่ save ไว้ตามเนื้อหาด้านบน
กด Send{code}

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
