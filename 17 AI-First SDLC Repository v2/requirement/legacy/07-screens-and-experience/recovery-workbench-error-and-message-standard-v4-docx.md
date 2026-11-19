<!-- source: 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx -->
<!-- converted: 2026-11-16 from DOCX -->

> **Source:** `07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx`  
> **Converted from:** DOCX

Recovery Workbench

Error and message standard

SCB Collections and Recovery. Henka Group, 16 November 2026

| Item | Detail |
|---|---|
| Document | Recovery Workbench error and message standard |
| Version | 4 |
| Date | 16 November 2026 |
| Prepared by | Henka Group |
| Thai text | Proposed. The business lead drafts per module one epic ahead; Legal and Compliance approve (DL10) |
| Change history | v4, 16 November 2026, D-RCV-36: added MSG-P3-036, MSG-P3-037 and MSG-P3-038 for the Temporal workflow service, the workflow alert and the replay gate; MSG-P3-022 now cites RWB-E2-041 and MSG-P3-027 now cites RWB-E1-073 |

# 1. The pattern

Every message says what happened and what to do next, in that order, in the fewest words that are clear. A message names the thing on the screen and never the code behind it.

| Type | When it is used | Pattern | Example |
|---|---|---|---|
| Error | The action did not happen | What is wrong. What to do. | Enter the reason for the transfer. |
| Warning | The action can happen, but something needs attention | What is at risk. By when. | The claim on this case expires on 4 March 2027. File before then. |
| Confirmation | The action happened | What happened. What follows. | Approved. The case moves to Offer with customer. |
| Information | A state the user should know | The state, and the date or owner it depends on | This case is on hold for a complaint. |

# 2. Wording rules

- Write to the user as you. Write the system as the case, the record or the Workbench, never as I or we.

- Use the names in the business glossary. A field is called what the screen calls it.

- No codes, stack traces, table names or rule IDs on screen. The message ID and the rule ID go to the log.

- No blame and no apology. State the fact.

- Put a date, an amount or a name in the message when the user needs it to act.

- One message per problem. Field errors show next to the field; a summary at the top lists them when there is more than one.

- English and Thai carry the same meaning and the same placeholders. The Thai text uses กรุณา for a request and no ending particle.

- Dates show as 4 March 2027 in English and 4 มีนาคม 2570 in Thai. Amounts show in baht with thousands separators.

# 3. How a message is held

| Item | Rule |
|---|---|
| ID | MSG, the module code and a number, for example MSG-P3-011. GEN for messages every module uses |
| Where it is held | In the message table as reference data, with the English and Thai text and a version. A wording change is a data load, not a code release |
| Placeholders | Names in braces, for example {date}. Each placeholder is filled from the record, formatted for the language |
| Rule link | Each message names the rule or validation that raises it, so a test can check both |
| Language | The user's language setting picks the text. Customer-facing letters and messages follow the customer's language |
| Approval | Legal and Compliance approve customer-facing wording. The product owner approves screen wording |

# 4. The core messages

166 messages that the platform and stage modules and the Epic 1 and Epic 2 stories use. A new story adds its messages to this table in the same form.

| ID | Type | Raised when | English | Thai, proposed |
|---|---|---|---|---|
| MSG-GEN-001 | Error | Required field empty | Enter {field}. | กรุณากรอก {field} |
| MSG-GEN-002 | Error | Value outside its allowed range | {field} must be between {min} and {max}. | {field} ต้องอยู่ระหว่าง {min} ถึง {max} |
| MSG-GEN-003 | Error | Date in the wrong order | {field} cannot be before {other}. | {field} ต้องไม่ก่อน {other} |
| MSG-GEN-004 | Error | Record changed by someone else | Someone else changed this record. Reload it to see their change. | มีผู้อื่นแก้ไขรายการนี้แล้ว กรุณาโหลดใหม่เพื่อดูการเปลี่ยนแปลง |
| MSG-GEN-005 | Confirmation | Saved | Saved. | บันทึกแล้ว |
| MSG-GEN-006 | Error | System of record unavailable (R-UNI-33) | {system} is not available. Your request is queued and will be retried. | ระบบ {system} ไม่พร้อมใช้งาน ระบบได้จัดคิวคำขอของคุณไว้และจะดำเนินการใหม่ |
| MSG-GEN-007 | Error | A filter or field value is not in its list of values (RWB-E2-033) | {value} is not a valid value for {field}. Choose a value from the list. | {value} ไม่ใช่ค่าที่ถูกต้องสำหรับ {field} กรุณาเลือกค่าจากรายการ |
| MSG-P1-001 | Warning | Data product stale after a late or failed load | {product} is from {date}. Today's load has not arrived. | ข้อมูล {product} เป็นข้อมูล ณ วันที่ {date} ยังไม่ได้รับข้อมูลของวันนี้ |
| MSG-P1-002 | Error | Load refused at a check | The {source} load for {date} was refused: {check}. The previous load is still in use. | ระบบไม่รับข้อมูล {source} ของวันที่ {date} เนื่องจาก {check} ยังคงใช้ข้อมูลชุดก่อนหน้า |
| MSG-P1-003 | Error | Catalog row with no system of record, more than one, or no owner (RWB-E1-001) | {product} must have exactly one system of record and one named owner. | {product} ต้องมีระบบต้นทางหลักเพียงหนึ่งระบบและมีผู้รับผิดชอบที่ระบุชื่อหนึ่งคน |
| MSG-P1-004 | Error | Catalog file without exactly DP01 to DP14 (RWB-E1-001) | The catalog must hold the 14 data products DP01 to DP14. Missing: {products}. | แค็ตตาล็อกต้องมีผลิตภัณฑ์ข้อมูลครบ 14 รายการ ตั้งแต่ DP01 ถึง DP14 รายการที่ขาด: {products} |
| MSG-P1-005 | Error | A rule version names a field not in the data dictionary (RWB-E1-006) | {entity}.{field} is not in the data dictionary. Correct the rule or add the field to the dictionary. | ไม่พบ {entity}.{field} ในพจนานุกรมข้อมูล กรุณาแก้ไขเกณฑ์หรือเพิ่มฟิลด์ในพจนานุกรมข้อมูล |
| MSG-P1-006 | Warning | Load count or balance moves outside the expected range (DQ-007 and equivalents) (RWB-E1-003) | The {source} load for {date} changed by {pct} percent against the previous load, outside the expected {limit} percent. Check it before use. | ข้อมูล {source} ของวันที่ {date} เปลี่ยนแปลง {pct} เปอร์เซ็นต์จากการโหลดครั้งก่อน เกินกว่าที่คาดไว้ {limit} เปอร์เซ็นต์ กรุณาตรวจสอบก่อนใช้งาน |
| MSG-P1-007 | Error | A value in a loaded row is outside its list (RWB-E1-005) | Row {row}: {field} must be one of {values}. | แถวที่ {row}: {field} ต้องเป็นค่าใดค่าหนึ่งต่อไปนี้ {values} |
| MSG-P1-008 | Information | Tracker load complete (RWB-E1-010) | {loaded} rows loaded from {file}. {rejected} rows rejected; the reject list is on the load. | โหลดข้อมูล {loaded} แถวจาก {file} แล้ว ปฏิเสธ {rejected} แถว ดูรายการที่ถูกปฏิเสธได้ในรายการโหลด |
| MSG-P1-009 | Error | Counts do not match at tracker sign-off (RWB-E1-010) | The counts do not match: {confirmed} rows confirmed, {fileRows} rows in the file, {loaded} loaded, {rejected} rejected. Sign-off is not allowed. | จำนวนไม่ตรงกัน: ยืนยัน {confirmed} แถว ในไฟล์มี {fileRows} แถว โหลดแล้ว {loaded} แถว ปฏิเสธ {rejected} แถว ไม่สามารถลงนามรับรองได้ |
| MSG-P1-010 | Error | Tracker cannot be loaded or signed off in its decision and status (RWB-E1-010) | {tracker} cannot be loaded: its decision is {decision} and its status is {status}. | ไม่สามารถโหลด {tracker} ได้ เนื่องจากการตัดสินใจคือ {decision} และสถานะคือ {status} |
| MSG-P1-011 | Error | Rerun or repeat of a load that is already complete or running, or the same file again (RWB-E1-003) | The {source} load for {date} is already complete or running. It was not run again. | การโหลดข้อมูล {source} ของวันที่ {date} เสร็จสิ้นแล้วหรือกำลังดำเนินการอยู่ ระบบไม่ได้ดำเนินการซ้ำ |
| MSG-P1-012 | Warning | Case list count or balance outside the reconciliation tolerance (RWB-E1-002) | The case list for {date} does not reconcile to ALS for {product}: a difference of {variance} accounts, {pct} percent. | รายการกรณีของวันที่ {date} ไม่ตรงกับ ALS สำหรับ {product}: ต่างกัน {variance} บัญชี คิดเป็น {pct} เปอร์เซ็นต์ |
| MSG-P1-013 | Error | Tracker cannot be retired in its decision and status (RWB-E1-012) | {tracker} cannot be retired: its decision is {decision} and its status is {status}. | ไม่สามารถยกเลิกการใช้ {tracker} ได้ เนื่องจากการตัดสินใจคือ {decision} และสถานะคือ {status} |
| MSG-P1-014 | Error | Tracker retirement before the parallel period has passed (RWB-E1-012) | {tracker} can be retired from {date}, after {days} working days of use of the case list. | สามารถยกเลิกการใช้ {tracker} ได้ตั้งแต่วันที่ {date} หลังจากใช้รายการกรณีครบ {days} วันทำการ |
| MSG-P1-015 | Warning | A data quality rule fails at run time (RWB-E1-006) | Rule {rule} did not run for {date}: {reason}. The other rules ran. | เกณฑ์ {rule} ไม่ได้ทำงานสำหรับวันที่ {date} เนื่องจาก {reason} เกณฑ์อื่นทำงานตามปกติ |
| MSG-P1-016 | Error | Tracker inventory has no row for a team in the team list (RWB-E1-005) | The inventory has no row for team {team}. List its trackers, or add one row with location type NONE. | รายการสำรวจไม่มีแถวของทีม {team} กรุณาระบุไฟล์ติดตามงานของทีม หรือเพิ่มหนึ่งแถวที่มีประเภทที่จัดเก็บเป็น NONE |
| MSG-P1-017 | Error | A key value appears twice in a loaded file (RWB-E1-005) | Row {row}: tracker code {value} appears more than once. | แถวที่ {row}: รหัสไฟล์ติดตามงาน {value} ปรากฏมากกว่าหนึ่งครั้ง |
| MSG-P1-018 | Error | Tracker file of a type or size not allowed (RWB-E1-010) | Use an .xlsx or .csv file of at most {size} MB for a tracker load. | กรุณาใช้ไฟล์ .xlsx หรือ .csv ขนาดไม่เกิน {size} MB สำหรับการโหลดไฟล์ติดตามงาน |
| MSG-P1-019 | Error | The decision log lake copy does not match the live log on count or last hash (REC-08) (RWB-E1-014) | The decision log copy for {date} does not match the live log: {check}. The copy was not published. | สำเนาบันทึกการตัดสินใจของวันที่ {date} ไม่ตรงกับบันทึกจริง: {check} ระบบยังไม่เผยแพร่สำเนานี้ |
| MSG-P1-020 | Information | Retention job summary to Compliance after JOB-17 (RWB-E1-017) | {count} rows of {product} were archived under rule {rule} version {version}. {held} cases on legal hold were kept. | ระบบได้ย้ายข้อมูล {product} จำนวน {count} รายการไปเก็บถาวรตามเกณฑ์ {rule} ฉบับ {version} และคงข้อมูลของกรณีที่ถูกระงับทางกฎหมายไว้ {held} กรณี |
| MSG-P1-021 | Error | Publish of a data contract with no recorded system owner confirmation (RWB-E1-064) | The data contract for {system} cannot be published until its system owner confirms it. | ไม่สามารถเผยแพร่ข้อตกลงข้อมูลของ {system} ได้ จนกว่าเจ้าของระบบจะยืนยัน |
| MSG-P1-022 | Error | The interaction ledger write failed; the action is not saved and an incident is raised (RWB-E1-066) | The entry was not saved because the interaction ledger could not be written. Try again in a few minutes. | ระบบยังไม่บันทึกรายการนี้ เนื่องจากบันทึกประวัติการติดต่อไม่สำเร็จ กรุณาลองใหม่อีกครั้งในอีกสักครู่ |
| MSG-P10-001 | Error | A prompt, policy or sample file fails a load check (RWB-E1-058) | The {kind} file for {agent} was refused: {check}. The version in force is unchanged. | ระบบไม่รับไฟล์ {kind} ของ {agent} เนื่องจาก {check} ยังคงใช้ฉบับที่มีผลอยู่เดิม |
| MSG-P10-002 | Error | Evaluation started on a sample with no labeled rows (RWB-E1-058) | Sample {sample} has no labeled rows for {agent}. Load the labels before you run the evaluation. | ชุดตัวอย่าง {sample} ยังไม่มีข้อมูลที่ระบุผลสำหรับ {agent} กรุณาโหลดข้อมูลก่อนเริ่มการประเมิน |
| MSG-P10-003 | Error | Evaluation started while the same evaluation is running (RWB-E1-058) | An evaluation of {agent} on sample {sample} is already running. Wait for it to finish. | การประเมิน {agent} ด้วยชุดตัวอย่าง {sample} กำลังดำเนินการอยู่ กรุณารอจนเสร็จ |
| MSG-P10-004 | Warning | Agent cost on a business date above its daily limit (RWB-E1-063) | {agent} used {amount} baht of model calls on {date}, above the daily limit of {limit} baht. | {agent} ใช้ค่าเรียกใช้แบบจำลอง {amount} บาท ในวันที่ {date} เกินวงเงินรายวัน {limit} บาท |
| MSG-P10-005 | Information | No L1 intake summary for the case because the agent run failed (RWB-E2-028) | The agent summary is not available for this case. Work from the case record. | ยังไม่มีสรุปจากเอเจนต์สำหรับกรณีนี้ กรุณาใช้ข้อมูลในรายละเอียดกรณี |
| MSG-P10-006 | Warning | Weekly acceptance of an L1 agent falls by 10 points or more (RWB-E2-031) | {agent} acceptance for {segment} fell from {from} to {to} percent in the week to {date}. | อัตราการยอมรับของ {agent} สำหรับ {segment} ลดลงจาก {from} เป็น {to} เปอร์เซ็นต์ ในสัปดาห์ที่สิ้นสุดวันที่ {date} |
| MSG-P10-007 | Information | No TDR offer suggestion: model not in service, timeout or failed check (RWB-E2-032) | No offer suggestion is available for this treatment. The TDR model is not in service. | ไม่มีข้อเสนอแนะเงื่อนไขสำหรับแนวทางแก้ไขหนี้นี้ เนื่องจากแบบจำลอง TDR ยังไม่พร้อมใช้งาน |
| MSG-P10-008 | Error | Evaluation report requested before the evaluation is done (RWB-E1-061) | The evaluation of {agent} on sample {sample} is still running. Open the report when it has finished. | การประเมิน {agent} ด้วยชุดตัวอย่าง {sample} ยังไม่เสร็จ กรุณาเปิดรายงานอีกครั้งเมื่อการประเมินเสร็จสิ้น |
| MSG-P2-001 | Error | An outbound file or an outbox delivery moves to the exception queue after the retry limit (RWB-E1-007, RWB-TE-006) | {item} was not delivered to {interface} after {count} attempts. It is in the exception queue. | ระบบส่ง {item} ไปยัง {interface} ไม่สำเร็จหลังจากพยายาม {count} ครั้ง รายการนี้อยู่ในคิวรายการผิดปกติ |
| MSG-P2-002 | Error | Contract test finds a source field that differs from the interface specification (RWB-E1-051) | Field {field} in {interface} does not match the interface specification: expected {expected}, found {found}. | ฟิลด์ {field} ใน {interface} ไม่ตรงกับข้อกำหนดอินเทอร์เฟซ: ต้องเป็น {expected} แต่พบ {found} |
| MSG-P2-003 | Warning | Weekly flag report, flag past its removal date (RWB-E1-047) | Flag {flag} passed its removal date on {date}. Owner: {owner}. Remove the flag and its old code path. | แฟล็ก {flag} เลยวันที่ต้องนำออกแล้วเมื่อวันที่ {date} ผู้รับผิดชอบ: {owner} กรุณานำแฟล็กและโค้ดเดิมออก |
| MSG-P2-004 | Error | A feed or scheduled job failed, a file is missing, or a job runs past its alert threshold (RWB-E1-051, RWB-E1-056) | {job} failed at {time} for business date {date}. Follow run book {runbook}. | งาน {job} ล้มเหลวเมื่อเวลา {time} สำหรับวันที่ทำการ {date} กรุณาดำเนินการตามคู่มือ {runbook} |
| MSG-P2-005 | Error | Pipeline finds a job without a catalog row or a run book with the six sections (RWB-E1-056) | Job {job} has no run book with the six sections. Missing: {section}. | งาน {job} ยังไม่มีคู่มือการดำเนินงานครบหกหัวข้อ ขาด: {section} |
| MSG-P2-006 | Error | A rerun or a second start of a job or load that is already running (RWB-E1-014, RWB-E1-056, RWB-E1-017, RWB-E2-010, RWB-TE-004, RWB-E1-051, RWB-E2-001, RWB-E2-007) | {job} is already running. Wait for it to finish before you run it again. | งาน {job} กำลังทำงานอยู่ กรุณารอให้เสร็จก่อนสั่งทำงานอีกครั้ง |
| MSG-P2-007 | Information | Case creation held because no load passed its checks (RWB-E2-001) | Case creation for {date} is held until a load passes its checks. {count} accounts are waiting. | ระงับการสร้างกรณีของวันที่ {date} ไว้จนกว่าข้อมูลจะผ่านการตรวจสอบ มีบัญชีรออยู่ {count} บัญชี |
| MSG-P2-008 | Warning | Plan status shown from the stored value because ACE returned none or did not answer (RWB-E2-002) | The ACE plan status is from {date}. Today's status was not returned. | สถานะแผนจาก ACE เป็นข้อมูล ณ วันที่ {date} ยังไม่ได้รับสถานะของวันนี้ |
| MSG-P2-009 | Warning | A checklist document is missing from the credit approval pack (RWB-E2-006) | The credit approval pack is missing {item}. Add it to the case before you submit in NLEADS. | ชุดเอกสารขออนุมัติสินเชื่อยังขาด {item} กรุณาเพิ่มในกรณีก่อนส่งใน NLEADS |
| MSG-P2-010 | Error | NLEADS result already recorded on the treatment (RWB-E2-006) | The NLEADS result for this treatment was recorded on {date}. | ผลจาก NLEADS ของแนวทางแก้ไขหนี้นี้ได้บันทึกแล้วเมื่อวันที่ {date} |
| MSG-P2-011 | Information | Task text, approved booking not found in the ALS load (RWB-E2-007) | No booking for treatment {treatment} was found in the ALS load for {date}. Book it in ALS. Accounts not booked: {accounts}. | ไม่พบการบันทึกแนวทางแก้ไขหนี้ {treatment} ในข้อมูล ALS ของวันที่ {date} กรุณาบันทึกใน ALS บัญชีที่ยังไม่บันทึก: {accounts} |
| MSG-P2-012 | Warning | Task text and treatment note, a booked term differs from the approved term (RWB-E2-007) | The booked {term} is {booked}. The approved {term} is {approved}. | {term} ที่บันทึกคือ {booked} แต่ {term} ที่อนุมัติคือ {approved} |
| MSG-P2-013 | Warning | EFS hand-over reconciliation difference above the alert threshold (RWB-E2-023) | {count} EFS hand-overs for {date} do not match a case ({pct} percent). See the data quality exceptions. | รายการส่งต่อจาก EFS ของวันที่ {date} จำนวน {count} รายการไม่ตรงกับกรณี ({pct} เปอร์เซ็นต์) กรุณาดูรายการผิดปกติด้านคุณภาพข้อมูล |
| MSG-P2-014 | Error | Sign-off refused, fewer clean days in a row than required (RWB-E2-023) | {count} clean days in a row so far. Sign-off needs {required}. | ขณะนี้มีวันที่ข้อมูลตรงกันต่อเนื่อง {count} วัน การลงนามต้องมี {required} วัน |
| MSG-P2-015 | Confirmation | Manual file handling retired (RWB-E2-023) | Manual EFS file handling ended on {date}. The sign-off is recorded. | ยกเลิกการจัดการไฟล์ EFS ด้วยมือแล้วเมื่อวันที่ {date} ระบบได้บันทึกการลงนามแล้ว |
| MSG-P2-016 | Error | Change to a feature flag key that does not exist (RWB-E1-047) | Flag {flag} does not exist. | ไม่พบแฟล็ก {flag} |
| MSG-P2-017 | Information | Customer holds no other product (RWB-E2-003) | The customer holds no other product with the bank in the customer profile of {date}. | ลูกหนี้ไม่มีผลิตภัณฑ์อื่นกับธนาคารตามข้อมูลลูกค้า ณ วันที่ {date} |
| MSG-P2-018 | Error | NLEADS approval level below the level the delegation of authority requires (RWB-E2-006) | The NLEADS approval is at level {level}. This plan needs level {required} or higher. | การอนุมัติใน NLEADS อยู่ที่ระดับ {level} แผนนี้ต้องได้รับอนุมัติระดับ {required} ขึ้นไป |
| MSG-P2-019 | Error | Sign-off for an interface whose manual handling is already retired (RWB-E2-023) | Manual handling for {interface} was already retired on {date}. | การจัดการ {interface} ด้วยมือได้ยกเลิกแล้วเมื่อวันที่ {date} |
| MSG-P2-020 | Error | The caller is not in the approved callers list (RWB-E2-036) | {caller} is not approved to place cases on queues. | {caller} ไม่ได้รับอนุมัติให้จัดกรณีเข้าคิว |
| MSG-P2-021 | Error | A placement for a case with an open deviation (RWB-E2-036) | This case has an open deviation and stays with the deviation handler. | กรณีนี้มีเหตุผิดปกติที่ยังไม่ปิด จึงยังอยู่กับผู้ดูแลเหตุผิดปกติ |
| MSG-P2-022 | Error | Sending again an outbox delivery that is not in the exception queue (RWB-TE-006) | Only an item in the exception queue can be sent again. | ส่งซ้ำได้เฉพาะรายการที่อยู่ในคิวรายการผิดปกติเท่านั้น |
| MSG-P2-023 | Warning | The case has no next action or no due date (RWB-E2-035) | This case has no next action. It is on the exception list for {team}. | กรณีนี้ยังไม่มีงานถัดไป และอยู่ในรายการผิดปกติของ {team} |
| MSG-P2-024 | Error | A placement for a case already in the target queue (RWB-E2-036) | This case is already in {queue}. | กรณีนี้อยู่ใน {queue} แล้ว |
| MSG-P2-025 | Error | Queue placement called while its feature flag is off (RWB-E2-036) | Queue placement by models and agents is switched off. | การจัดกรณีเข้าคิวโดยแบบจำลองและเอเจนต์ถูกปิดอยู่ |
| MSG-P3-001 | Error | A transfer without a reason | Choose a reason for the transfer. | กรุณาเลือกเหตุผลในการโอนงาน |
| MSG-P3-002 | Error | Transfer to an owner at the caseload cap | {owner} is at the caseload cap. Choose another owner or the team queue. | {owner} มีจำนวนกรณีเต็มแล้ว กรุณาเลือกผู้รับผิดชอบคนอื่นหรือคิวของทีม |
| MSG-P3-003 | Warning | A timer will expire within its warning period | {timer} ends on {date}. | {timer} จะครบกำหนดในวันที่ {date} |
| MSG-P3-004 | Information | Case on hold for a deviation | This case is on hold for {deviation}. The prescription date is still {date}. | กรณีนี้ถูกระงับไว้เนื่องจาก {deviation} วันขาดอายุความยังคงเป็นวันที่ {date} |
| MSG-P3-005 | Error | A move not allowed from the current state | This case cannot move to {state} from {current}. | กรณีนี้ไม่สามารถเปลี่ยนจาก {current} ไปยัง {state} ได้ |
| MSG-P3-011 | Information | Allocation summary, cases in overflow (RWB-E1-020) | {count} new cases are waiting in the overflow queue for {team}. Every owner is at the caseload cap. | มีกรณีใหม่ {count} รายการรออยู่ในคิวสำรองของ {team} เนื่องจากผู้รับผิดชอบทุกคนมีจำนวนกรณีเต็มแล้ว |
| MSG-P3-012 | Information | Allocation summary, no row matched (RWB-E1-020) | {count} new cases matched no allocation row and are in the exception queue. | มีกรณีใหม่ {count} รายการที่ไม่ตรงกับเกณฑ์การจัดสรร และอยู่ในคิวรายการผิดปกติ |
| MSG-P3-013 | Error | Allocation not recorded (RWB-E1-020) | The case was not allocated because the decision could not be recorded. It will be tried again in the next run. | ระบบยังไม่จัดสรรกรณีนี้ เนื่องจากบันทึกการตัดสินใจไม่สำเร็จ ระบบจะดำเนินการอีกครั้งในรอบถัดไป |
| MSG-P3-014 | Error | One or more rule tests fail in the rule table test harness (RWB-TE-005) | Rule version {version} failed {count} of {total} rule tests. | เกณฑ์ฉบับ {version} ไม่ผ่านการทดสอบ {count} จาก {total} รายการ |
| MSG-P3-015 | Error | Rollback called when no earlier version of the table exists (RWB-E1-019, RWB-E1-029, RWB-E1-042) | There is no earlier version of {table} to return to. | ไม่มีฉบับก่อนหน้าของ {table} ให้ย้อนกลับ |
| MSG-P3-016 | Error | Schema drift, a checksum mismatch, a migration lint failure, a refused clean or undo, or a failed migration (RWB-E1-044) | Schema check failed in {schema}: {object}. The deployment was stopped. | การตรวจสอบโครงสร้างฐานข้อมูล {schema} ไม่ผ่าน: {object} ระบบหยุดการติดตั้งแล้ว |
| MSG-P3-017 | Information | My queue or a team queue has no case for the person and filters (RWB-E2-011) | There are no cases in this queue. | ไม่มีกรณีในคิวนี้ |
| MSG-P3-018 | Information | A case has no running, paused or expired timer (RWB-E2-015) | There are no running timers on this case. | กรณีนี้ไม่มีการนับเวลาที่กำลังดำเนินอยู่ |
| MSG-P3-019 | Information | No timeline item on the case matches the filter (RWB-E2-016) | Nothing on this case matches the filter. | ไม่พบรายการของกรณีนี้ที่ตรงกับตัวกรอง |
| MSG-P3-020 | Information | No case meets the case list filters (RWB-E1-031) | No cases match these filters. Change a filter to see more. | ไม่พบกรณีที่ตรงกับตัวกรอง กรุณาเปลี่ยนตัวกรองเพื่อดูเพิ่มเติม |
| MSG-P3-021 | Error | Case list export above the row limit (RWB-E1-031) | The export holds at most {max} rows. Narrow the filters and try again. | การส่งออกทำได้สูงสุด {max} รายการ กรุณาจำกัดตัวกรองแล้วลองใหม่อีกครั้ง |
| MSG-P3-022 | Error | Approval of a version with a missing checklist item or a FAILED test result (RWB-E2-041) | The change cannot be approved: {item} is missing or failed. | ไม่สามารถอนุมัติการเปลี่ยนแปลงได้ เนื่องจาก {item} ยังไม่มีหรือไม่ผ่าน |
| MSG-P3-023 | Warning | One section of the case record view cannot be shown (RWB-E1-023, RWB-E1-035) | {section} cannot be shown now. The rest of the case is shown. | ไม่สามารถแสดง {section} ได้ในขณะนี้ ระบบแสดงข้อมูลส่วนอื่นของกรณีแล้ว |
| MSG-P3-024 | Information | A section of the case record view, or the interaction ledger of a case, has nothing to show (RWB-E2-034, RWB-E1-023) | Nothing is recorded in {section} yet. | ยังไม่มีข้อมูลใน {section} |
| MSG-P3-025 | Error | Yearly case number range used up (RWB-E1-018) | Case numbers for {year} are used up. New cases are on hold until the range is extended. | เลขที่กรณีของปี {year} ถูกใช้ครบแล้ว การสร้างกรณีใหม่ถูกระงับไว้จนกว่าจะขยายช่วงเลขที่ |
| MSG-P3-026 | Warning | No service level or legal period found for a case (RWB-E1-028) | No {item} is set for {scope}. The timer did not start. | ยังไม่ได้กำหนด {item} สำหรับ {scope} ระบบจึงยังไม่เริ่มนับเวลา |
| MSG-P3-027 | Error | A reference data or rule version load fails a check (schema, valid from in the past, duplicate key, removed product with open cases, overlap, unreachable or default row, test cases), or no version is in force for a table an engine needs (RWB-E1-073, RWB-E1-043, RWB-E1-025) | The {table} load was refused: {check}. The version in force is unchanged. | ระบบไม่รับข้อมูล {table} เนื่องจาก {check} ฉบับที่ใช้งานอยู่ยังไม่เปลี่ยนแปลง |
| MSG-P3-028 | Warning | Service level breach alert to the team manager (RWB-E1-030) | {count} cases in {queue} are past their service level. | มี {count} กรณีใน {queue} ที่เกินระยะเวลามาตรฐานแล้ว |
| MSG-P3-029 | Error | Queue measure snapshot does not reconcile to the case list (RWB-E1-030) | The queue measures for {date} were not published: {check}. | ระบบยังไม่เผยแพร่ตัวชี้วัดคิวงานของวันที่ {date} เนื่องจาก {check} |
| MSG-P3-030 | Information | A scheduled job ran for a business date after a missed run (RWB-TE-007) | {job} ran for {date} after a missed run. | งาน {job} ของวันที่ {date} ทำงานแล้วหลังจากรอบที่ขาดไป |
| MSG-P3-031 | Error | A scheduled job waits on a dependency, misses its deadline, or has more missed dates than the catch-up limit (RWB-TE-007) | {job} for {date} has not completed: {reason}. | งาน {job} ของวันที่ {date} ยังไม่เสร็จ: {reason} |
| MSG-P3-032 | Error | A required parameter has no value for the environment at start-up (RWB-E1-042) | Parameter {name} has no value for {environment}. The service did not start. | พารามิเตอร์ {name} ยังไม่มีค่าสำหรับ {environment} ระบบจึงไม่เริ่มทำงาน |
| MSG-P3-033 | Error | A transfer rule refuses a manual transfer or reassignment (RWB-E2-012) | Rule {rule} does not allow this transfer. | เกณฑ์ {rule} ไม่อนุญาตให้โอนงานนี้ |
| MSG-P3-034 | Error | A product has no required parameter or service level row, at load or at run time (RWB-E1-045) | {product} has no {parameter} row. Add it before the load. | {product} ยังไม่มีค่า {parameter} กรุณาเพิ่มก่อนนำเข้าข้อมูล |
| MSG-P3-035 | Warning | A bulk transfer or reassignment where some cases were refused (RWB-E2-012) | {done} of {total} cases were moved. The others show the reason on their row. | โอนงานแล้ว {done} จาก {total} กรณี กรณีที่เหลือแสดงเหตุผลไว้ในแต่ละแถว |
| MSG-P3-036 | Error | The Temporal frontend is unreachable, so a workflow start or a signal fails (RWB-E1-071, RWB-E2-043) | The workflow service is not available. Try again in a few minutes. | ระบบเวิร์กโฟลว์ไม่พร้อมใช้งาน กรุณาลองใหม่ในอีกไม่กี่นาที |
| MSG-P3-037 | Warning | A workflow has failed, or has not moved for the stuck window, and the alert fires (RWB-E2-037) | Workflow {workflowId} has failed or has not moved for {hours} hours. | เวิร์กโฟลว์ {workflowId} ล้มเหลวหรือไม่มีความคืบหน้ามาเป็นเวลา {hours} ชั่วโมง |
| MSG-P3-038 | Error | A workflow change fails the replay test against recorded histories in the pipeline (RWB-E2-040) | The workflow change fails the replay test against recorded histories: {detail}. | การเปลี่ยนแปลงเวิร์กโฟลว์ไม่ผ่านการทดสอบเล่นซ้ำกับประวัติที่บันทึกไว้: {detail} |
| MSG-P4-001 | Error | Sign-in with no Workbench role | You have no Recovery Workbench role. Ask your team manager to request one. | คุณยังไม่มีสิทธิ์ใช้งาน Recovery Workbench กรุณาติดต่อผู้จัดการทีมเพื่อขอสิทธิ์ |
| MSG-P4-002 | Error | An action outside the role's permission | You cannot {action} here. Your role does not include it. | คุณไม่สามารถ{action}ได้ เนื่องจากบทบาทของคุณไม่มีสิทธิ์นี้ |
| MSG-P4-003 | Error | A record outside the role's scope | This case is not in your scope. | กรณีนี้ไม่อยู่ในขอบเขตงานของคุณ |
| MSG-P4-004 | Warning | Break-glass access is active | Emergency access is on until {time}. Every action is recorded. | กำลังใช้สิทธิ์เข้าถึงกรณีฉุกเฉินถึง {time} ทุกการกระทำจะถูกบันทึก |
| MSG-P4-005 | Error | Token without a second factor in the amr claim (RWB-E1-022) | Sign in again with your second factor. The Workbench needs multi-factor authentication. | กรุณาเข้าสู่ระบบอีกครั้งด้วยการยืนยันตัวตนขั้นที่สอง Workbench ต้องใช้การยืนยันตัวตนแบบหลายปัจจัย |
| MSG-P4-006 | Error | A role pair in the role conflict table is held in one session (RWB-E1-022) | Your roles {role} and {otherRole} cannot be held together. Access is refused and the security administrator has been told. | บทบาท {role} และ {otherRole} ของคุณไม่สามารถถือร่วมกันได้ ระบบปฏิเสธการเข้าใช้งานและแจ้งผู้ดูแลความปลอดภัยแล้ว |
| MSG-P4-007 | Error | Break-glass requested without an approved bank IAM grant (RWB-E1-039) | Emergency access needs an approved break-glass request in the bank IAM with an open incident. | การเข้าถึงกรณีฉุกเฉินต้องมีคำขอสิทธิ์เข้าถึงกรณีฉุกเฉินที่ได้รับอนุมัติในระบบ IAM ของธนาคาร พร้อมเลขที่เหตุการณ์ที่ยังเปิดอยู่ |
| MSG-P4-008 | Error | Partner firm suspended, exited the panel or past its contract end (RWB-E2-019) | Your firm's access to the Recovery Workbench has ended. Contact your SCB partner manager. | สิทธิ์การเข้าใช้ Recovery Workbench ของบริษัทคุณสิ้นสุดแล้ว กรุณาติดต่อผู้ดูแลคู่ค้าของธนาคาร |
| MSG-P5-001 | Error | Upload of a file type not allowed | This file type cannot be stored. Use PDF, JPG or PNG. | ไม่สามารถจัดเก็บไฟล์ประเภทนี้ได้ กรุณาใช้ไฟล์ PDF, JPG หรือ PNG |
| MSG-P5-002 | Error | Change to a write-once legal document | Legal documents cannot be changed. Add a new version instead. | ไม่สามารถแก้ไขเอกสารทางกฎหมายได้ กรุณาเพิ่มเป็นฉบับใหม่ |
| MSG-P5-003 | Information | Low-confidence extraction sent for review | Some fields need checking. The document is in the review queue. | มีข้อมูลบางรายการที่ต้องตรวจสอบ เอกสารอยู่ในคิวรอตรวจสอบแล้ว |
| MSG-P5-004 | Warning | An original document is overdue back | {document} is due back from {holder} since {date}. | {document} ครบกำหนดส่งคืนจาก {holder} ตั้งแต่วันที่ {date} |
| MSG-P5-005 | Error | The case chosen for an intake item is closed (RWB-E1-054) | Case {case} is closed. Choose an open case. | กรณี {case} ปิดแล้ว กรุณาเลือกกรณีที่ยังเปิดอยู่ |
| MSG-P5-006 | Error | The chosen document type is not in the type list in force (RWB-E1-054) | {value} is not a document type in force. Choose a type from the list. | {value} ไม่ใช่ประเภทเอกสารที่ใช้งานอยู่ กรุณาเลือกประเภทจากรายการ |
| MSG-P5-007 | Error | A file is refused at intake (job record line) (RWB-E1-057) | {source} file {file} was not taken in: {reason}. It is in the {folder} folder. | ไม่ได้รับไฟล์ {file} จาก {source} เนื่องจาก {reason} ไฟล์อยู่ในโฟลเดอร์ {folder} |
| MSG-P5-008 | Warning | Two document intake runs in a row fail on one channel (RWB-E1-057) | Document intake failed twice in a row for {channel}. Check the interface and job monitor. | การรับเอกสารจาก {channel} ไม่สำเร็จสองครั้งติดต่อกัน กรุณาตรวจสอบที่หน้าติดตามระบบเชื่อมต่อและงานประมวลผล |
| MSG-P5-009 | Error | A required merge field has no value (RWB-E2-026) | {template} cannot be generated. {field} has no value on the case. | ไม่สามารถสร้างเอกสาร {template} ได้ เนื่องจากยังไม่มีข้อมูล {field} ในกรณีนี้ |
| MSG-P5-010 | Error | No current template version approved by Legal for the product and language (RWB-E2-026) | {template} has no version approved by Legal for {product} in {language}. | แม่แบบ {template} ยังไม่มีฉบับที่ฝ่ายกฎหมายอนุมัติสำหรับ {product} ภาษา {language} |
| MSG-P5-011 | Error | Generation requested for a treatment that is not approved or not open (RWB-E2-026) | Documents can be generated only for an approved {treatment} that is still open. | สร้างเอกสารได้เฉพาะ {treatment} ที่ได้รับอนุมัติแล้วและยังไม่ปิด |
| MSG-P5-012 | Confirmation | A generated set is sent for signature (RWB-E2-017) | {count} documents were sent for signature. | ส่งเอกสาร {count} ฉบับเพื่อลงนามแล้ว |
| MSG-P5-013 | Error | Send with a document not reviewed or made from an old template version (RWB-E2-017) | {document} cannot be sent yet: {reason}. | ยังไม่สามารถส่ง {document} ได้ เนื่องจาก {reason} |
| MSG-P5-014 | Error | Correction of a locked merge field (RWB-E2-017) | {field} comes from the approved treatment and cannot be changed here. | {field} มาจากแนวทางแก้ไขหนี้ที่ได้รับอนุมัติแล้ว จึงแก้ไขที่หน้านี้ไม่ได้ |
| MSG-P5-015 | Warning | Field captures accepted with no GPS position (RWB-E2-024) | {count} files have no location. They are on the case without a position. | มีไฟล์ {count} ไฟล์ที่ไม่มีข้อมูลตำแหน่ง ไฟล์ถูกบันทึกในกรณีโดยไม่มีพิกัด |
| MSG-P5-016 | Error | An uploaded file fails the malware scan (RWB-E1-026) | This file was not stored because the malware scan found a threat. It is held in quarantine. | ระบบไม่ได้จัดเก็บไฟล์นี้ เนื่องจากการตรวจสอบมัลแวร์พบภัยคุกคาม ไฟล์ถูกกักไว้แล้ว |
| MSG-P5-017 | Error | A file is above the size limit (RWB-E1-024) | This file is larger than {size} MB and cannot be stored. | ไฟล์นี้มีขนาดเกิน {size} MB จึงไม่สามารถจัดเก็บได้ |
| MSG-P5-018 | Information | A page is below the OCR quality threshold on a document of a known case (RWB-E1-049) | Page {page} of {document} on case {case} could not be read. Scan it again and send it to the document hub. | ระบบอ่านหน้า {page} ของ {document} ในกรณี {case} ไม่ได้ กรุณาสแกนใหม่และส่งเข้าศูนย์เอกสาร |
| MSG-P5-019 | Error | The access log write for a search is not confirmed (RWB-E1-033) | The search was not run because it could not be recorded. Try again in a few minutes. | ระบบยังไม่ค้นหา เนื่องจากบันทึกการค้นหาไม่สำเร็จ กรุณาลองใหม่อีกครั้งในอีกสักครู่ |
| MSG-P5-020 | Error | A role whose masking rules hide personal data searches a personal field or free text (RWB-E1-033) | Your role cannot search on {field} because it holds personal data. | บทบาทของคุณไม่สามารถค้นหาด้วย {field} ได้ เนื่องจากเป็นข้อมูลส่วนบุคคล |
| MSG-P5-021 | Information | More documents match than the search result limit (RWB-E1-033) | More than {count} documents match. Narrow the search to see them all. | มีเอกสารที่ตรงกันมากกว่า {count} รายการ กรุณาระบุเงื่อนไขให้แคบลงเพื่อดูทั้งหมด |
| MSG-P5-022 | Error | The malware scanning service does not answer during an upload (RWB-E1-041) | The malware scan is not available, so the file was not stored. Try again in a few minutes. | ระบบตรวจสอบมัลแวร์ไม่พร้อมใช้งาน จึงยังไม่ได้จัดเก็บไฟล์ กรุณาลองใหม่อีกครั้งในอีกสักครู่ |
| MSG-P5-023 | Warning | Required documents are missing on the case (RWB-E1-040) | {count} required documents are missing for this case: {types}. | กรณีนี้ยังขาดเอกสารที่ต้องมี {count} รายการ: {types} |
| MSG-P5-024 | Information | The same file and type are uploaded again to a case (RWB-E1-026) | This file is already on the case as {document}. | ไฟล์นี้มีอยู่ในกรณีแล้วในชื่อ {document} |
| MSG-P5-025 | Error | A new version is added to a superseded version (RWB-E1-024) | This is not the latest version of the document. Open the latest version to add a new one. | เอกสารนี้ไม่ใช่ฉบับล่าสุด กรุณาเปิดฉบับล่าสุดเพื่อเพิ่มฉบับใหม่ |
| MSG-P6-001 | Error | Contact attempted while a contact stop is in force | Contact with this customer is stopped for {reason}. | ระงับการติดต่อลูกหนี้รายนี้ เนื่องจาก {reason} |
| MSG-P6-002 | Error | Message to a channel without consent | The customer has not consented to {channel}. Use another channel. | ลูกหนี้ยังไม่ได้ให้ความยินยอมสำหรับช่องทาง {channel} กรุณาใช้ช่องทางอื่น |
| MSG-P6-003 | Warning | Template withdrawn (R-LIT-04) | The {template} template has been withdrawn. The notice is on hold until Legal approves a new version. | แม่แบบ {template} ถูกยกเลิกแล้ว หนังสือนี้จะถูกระงับไว้จนกว่าฝ่ายกฎหมายจะอนุมัติฉบับใหม่ |
| MSG-P6-004 | Confirmation | Notice dispatched | {notice} was sent for registered mail on {date}. | ส่ง{notice}ทางไปรษณีย์ลงทะเบียนแล้วเมื่อวันที่ {date} |
| MSG-P6-005 | Error | A template version with no Legal approval is set current or asked for at generation (RWB-E1-034, RWB-E1-046, RWB-E1-052) | {template} version {version} has no Legal approval. It cannot be used. | {template} ฉบับที่ {version} ยังไม่ได้รับอนุมัติจากฝ่ายกฎหมาย จึงไม่สามารถใช้งานได้ |
| MSG-P6-006 | Error | A template uses a merge field that is not in the merge field catalog (RWB-E1-046, RWB-E1-034) | {template} uses the merge field {field}, which is not in the merge field catalog. The load was refused. | {template} ใช้ช่องข้อมูล {field} ซึ่งไม่มีในรายการช่องข้อมูลสำหรับผสานเอกสาร ระบบไม่รับการนำเข้า |
| MSG-P6-007 | Warning | A notice is held because a required merge value is empty on the case (RWB-E1-052) | {notice} for case {case} is on hold. {field} has no value on the case. | {notice} ของกรณี {case} ถูกระงับไว้ เนื่องจาก {field} ยังไม่มีข้อมูลในกรณีนี้ |
| MSG-P6-008 | Warning | A notice is refused, undeliverable or has no proof inside the proof window (RWB-E2-021) | {notice} for case {case} was not served: {reason}. The case is in your queue to choose another service method. | {notice} ของกรณี {case} ส่งไม่สำเร็จ: {reason} กรณีนี้อยู่ในคิวของคุณเพื่อเลือกวิธีการส่งแบบอื่น |
| MSG-P6-009 | Error | E-signature is requested for a document whose template requires a wet ink signature (RWB-E2-018) | Legal requires a wet ink signature for {document}. Use the branch or paper path. | ฝ่ายกฎหมายกำหนดให้ลงนามด้วยลายมือชื่อจริงสำหรับ {document} กรุณาใช้ช่องทางสาขาหรือเอกสารกระดาษ |
| MSG-P6-010 | Error | A template body file of a type that is not allowed is uploaded (RWB-E1-034) | This template file type cannot be loaded. Use {types}. | ไม่สามารถนำเข้าไฟล์แม่แบบประเภทนี้ได้ กรุณาใช้ไฟล์ {types} |
| MSG-P7-001 | Error | Approval above the approver's limit | This needs approval at level {level}. It has been sent to {approver}. | รายการนี้ต้องได้รับอนุมัติในระดับ {level} ระบบได้ส่งให้ {approver} แล้ว |
| MSG-P7-002 | Error | Approver prepared the decision | You prepared this decision, so you cannot approve it. | คุณเป็นผู้จัดทำรายการนี้ จึงไม่สามารถอนุมัติได้ |
| MSG-P7-003 | Error | Decision log write failed (principle 5) | The action was not taken because the decision could not be recorded. Try again in a few minutes. | ระบบยังไม่ดำเนินการ เนื่องจากบันทึกการตัดสินใจไม่สำเร็จ กรุณาลองใหม่อีกครั้งในอีกสักครู่ |
| MSG-P7-004 | Confirmation | Decision approved | Approved. The case moves to {state}. | อนุมัติแล้ว กรณีนี้ไปยังขั้นตอน {state} |
| MSG-P7-005 | Error | Override without a reason | Enter the reason you are not following the recommendation. | กรุณาระบุเหตุผลที่ไม่ดำเนินการตามข้อเสนอแนะ |
| MSG-P7-006 | Warning | A decision input is past its age limit | {input} is {days} days old, past its limit. Refresh it before you decide. | ข้อมูล {input} มีอายุ {days} วัน เกินกำหนด กรุณาปรับปรุงข้อมูลก่อนตัดสินใจ |
| MSG-P7-007 | Information | Nightly hash chain check passed (RWB-TE-008) | The decision log check for {date} passed: {count} entries checked. The last hash is {hash}. | การตรวจสอบบันทึกการตัดสินใจของวันที่ {date} ผ่าน ตรวจสอบแล้ว {count} รายการ ค่าแฮชล่าสุดคือ {hash} |
| MSG-P7-008 | Error | The chain verifier found a break (RWB-E1-008, RWB-TE-008) | The decision log check for {date} found a break at entry {entryId}. Entries from that entry on cannot be relied on until Compliance reviews them. | การตรวจสอบบันทึกการตัดสินใจของวันที่ {date} พบความไม่ต่อเนื่องที่รายการ {entryId} รายการตั้งแต่รายการนี้เป็นต้นไปยังใช้อ้างอิงไม่ได้จนกว่าฝ่ายกำกับดูแลจะตรวจสอบ |
| MSG-P7-009 | Error | Decision log record refused for a missing or invalid field (service log and incident) (RWB-E1-027) | The decision record was refused: {field} is missing or not valid. | ระบบไม่รับบันทึกการตัดสินใจ เนื่องจาก {field} ไม่มีข้อมูลหรือไม่ถูกต้อง |
| MSG-P7-010 | Error | No delegation limit row covers the decision and product (RWB-E1-038, RWB-E2-013) | No approval limit covers {decision} for {product}. The item is held and Risk has been told. | ไม่มีวงเงินอนุมัติที่ครอบคลุม {decision} สำหรับ {product} รายการนี้ถูกระงับไว้และได้แจ้งฝ่ายบริหารความเสี่ยงแล้ว |
| MSG-P7-011 | Information | An approval passed its service level, or had no holder, and moved to a new approver (RWB-E2-013) | {decision} on case {caseNo} passed its service level and is now with you for approval. | {decision} ของกรณี {caseNo} เกินระยะเวลาที่กำหนดแล้ว และส่งมาให้คุณพิจารณาอนุมัติ |
| MSG-P7-012 | Warning | An entry returned by a query does not match the chain (RWB-E2-005) | Entry {entryId} does not match the decision log chain. Do not rely on it until Compliance has reviewed it. | รายการ {entryId} ไม่ตรงกับห่วงโซ่บันทึกการตัดสินใจ กรุณาอย่าใช้อ้างอิงจนกว่าฝ่ายกำกับดูแลจะตรวจสอบ |
| MSG-P7-013 | Warning | The nightly hash chain check did not complete (RWB-TE-008) | The decision log check for {date} did not complete. The chain was last confirmed on {lastDate}. | การตรวจสอบบันทึกการตัดสินใจของวันที่ {date} ไม่เสร็จสมบูรณ์ ห่วงโซ่ได้รับการยืนยันครั้งล่าสุดเมื่อวันที่ {lastDate} |
| MSG-P8-001 | Information | Payment matching run summary with unmatched payments (RWB-E2-008, RWB-E2-027) | {count} payments for {date} matched no plan and are on the exception list. | การชำระเงิน {count} รายการของวันที่ {date} ไม่ตรงกับแผนการชำระใด และอยู่ในรายการผิดปกติ |
| MSG-P8-002 | Error | Payment matching cannot run because no matching rule is in force (RWB-E2-008) | Payment matching for {date} did not run: no matching rule is in force. | ระบบไม่ได้จับคู่การชำระเงินของวันที่ {date} เนื่องจากไม่มีเกณฑ์การจับคู่ที่มีผลบังคับใช้ |
| MSG-P9-001 | Warning | The baseline for a business date is published again (RWB-E1-013) | The baseline for {date} is frozen. It cannot be published again. | ข้อมูลฐานของวันที่ {date} ถูกล็อกแล้ว ไม่สามารถเผยแพร่ซ้ำได้ |
| MSG-P9-002 | Warning | The dashboard case count differs from the case list and the publish is held (RWB-E2-009) | The case count on the dashboard ({count}) does not match the case list ({listCount}) for {date}. The publish is held. | จำนวนกรณีบนแดชบอร์ด ({count}) ไม่ตรงกับรายการกรณี ({listCount}) ของวันที่ {date} ระบบระงับการเผยแพร่ไว้ |
| MSG-P9-003 | Warning | A measure has no approved definition in force (RWB-E1-013) | {measure} has no approved definition. It is not published. | {measure} ยังไม่มีนิยามที่ได้รับอนุมัติ จึงไม่ถูกเผยแพร่ |
| MSG-S2-001 | Error | Settlement below the floor without approval (R-SET-05) | The offer is below the floor of {floor}. It has been sent for approval. | ข้อเสนอต่ำกว่าราคาขั้นต่ำ {floor} ระบบได้ส่งเพื่อขออนุมัติแล้ว |
| MSG-S2-002 | Warning | Payoff figure stale (R-SET-03) | The payoff is from {date}. A new figure has been requested. | ยอดปิดบัญชีเป็นข้อมูล ณ วันที่ {date} ระบบได้ขอยอดใหม่แล้ว |
| MSG-S2-003 | Information | Offer validity ending | The offer to the customer ends on {date}. | ข้อเสนอแก่ลูกหนี้จะสิ้นสุดในวันที่ {date} |
| MSG-S4-001 | Error | Pack incomplete at filing | The pack is missing {item}. Add it before filing. | เอกสารประกอบการฟ้องยังขาด {item} กรุณาเพิ่มก่อนยื่นฟ้อง |
| MSG-S4-002 | Warning | Prescription date near | The claim on this case expires on {date}. File before then. | สิทธิเรียกร้องของกรณีนี้จะขาดอายุความในวันที่ {date} กรุณายื่นฟ้องก่อนวันดังกล่าว |
| MSG-S5-001 | Error | Floor price below the approver's limit | The floor is {pct} of fair market value, below the {limit} this level may approve. | ราคาขั้นต่ำคิดเป็น {pct} ของมูลค่าตลาดที่เป็นธรรม ต่ำกว่า {limit} ที่ระดับนี้อนุมัติได้ |
| MSG-S5-002 | Warning | Appraisal older than one year | The appraisal is from {date}, more than a year ago. Order a new one before pricing. | ราคาประเมินเป็นข้อมูล ณ วันที่ {date} เกินหนึ่งปีแล้ว กรุณาสั่งประเมินใหม่ก่อนกำหนดราคา |
| MSG-S6-001 | Error | Account with an open deviation selected for a lot (R-DS-02) | {account} has an open deviation and cannot be sold. | บัญชี {account} มีเหตุผิดปกติที่ยังไม่ปิด จึงไม่สามารถขายได้ |
| MSG-S7-001 | Error | Write-off without the tax criteria version (R-WO-03) | The scan is on hold until Finance publishes the tax criteria. | ระงับการคัดเลือกไว้จนกว่าฝ่ายการเงินจะประกาศเกณฑ์ภาษี |
| MSG-S8-001 | Information | Deviation flagged | {deviation} was raised. The case is with {handler}. | มีการแจ้ง{deviation} กรณีนี้อยู่ที่ {handler} |

# 5. Open point

| Decision | What is needed | Answer used until decided |
|---|---|---|
| DL10 | The Thai name for each field, label and message | The business lead drafts per module one epic ahead; Legal and Compliance approve |
