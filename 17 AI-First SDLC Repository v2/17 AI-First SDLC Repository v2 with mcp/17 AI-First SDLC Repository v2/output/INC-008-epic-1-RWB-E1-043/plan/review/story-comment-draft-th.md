# ร่างคอมเมนต์สำหรับสตอรี่ RWB-E1-043 (Plan Gate)

```
ผลการตรวจสอบ Plan Gate: FAIL (พบเฉพาะระดับ Low เท่านั้น — ไม่บล็อกการส่งต่องาน ตาม REVIEW_GATE_WARNING)

Compliance Reviewer ได้ทำการตรวจสอบ plan-gate review สำหรับ RUN_ID
INC-009-epic-1-RWB-E1-043 แล้ว
ผลลัพธ์: [CRITICAL:0] [HIGH:0] [MEDIUM:0] [LOW:1]

ประเด็นที่พบ REVIEW-RWB-E1-043-PLAN-001 (ระดับ Low):
Endpoint สำหรับ rollback (POST /api/recovery/v1/admin/reference-loads/{loadId}/rollback)
มีการระบุทั้ง error code 404 (MSG-P4-003) และ 422 (MSG-P3-027) สำหรับเงื่อนไขเดียวกัน
("loadId ไม่สามารถ resolve ไปยัง version ที่สถานะ APPROVED ได้") โดยไม่มีกติกาชัดเจนว่า
กรณีใดควรใช้ error code ใด
ได้บันทึกประเด็นนี้ไว้ใน plan.md หัวข้อ §Risks แล้ว และผูกเงื่อนไขไว้กับ TASK-09/TASK-13
ก่อนที่ Builder จะเริ่มเขียนโค้ดส่วนนี้

ตามนโยบายความรุนแรง (.github/rules/pdlc.md) ประเด็นระดับ Low เพียงอย่างเดียวจะไม่บล็อก
การส่งต่องานโดยอัตโนมัติ แต่สถานะ FAIL จะยังคงถูกเก็บรักษาไว้ (ไม่เปลี่ยนเป็น PASS) และ
ประเด็นนี้ต้องแสดงให้เห็นต่อไปจนกว่าจะมีมนุษย์บันทึกการแก้ไขหรือการยอมรับอย่างชัดเจน

สิ่งที่ต้องทำก่อนเริ่ม Implementation Builder:
1. ตรวจสอบและอนุมัติ plan.md + tasks.md
2. จัดการประเด็น REVIEW-RWB-E1-043-PLAN-001 (เลือกกติกาว่าจะใช้ 404 อย่างเดียว หรือ 422
   อย่างเดียวสำหรับ rollback endpoint แล้วอัปเดต contracts/backend-apis.json และ
   คำอธิบายของ TASK-09 พร้อมเพิ่ม test scenario สำหรับกรณี negative path)
3. ดำเนินการให้ PRE-1 ถึง PRE-8 ผ่านครบทุกข้อ (ปัจจุบันยังอยู่ในสถานะ pending ทั้งหมด —
   ดูรายละเอียดที่ plan.md §Plan approval preconditions)

เอกสารตรวจสอบฉบับเต็ม: output/INC-009-epic-1-RWB-E1-043/plan/review/plan-gate-review.md
```
