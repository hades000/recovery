<!-- source: 04 User stories/Recovery Workbench Acceptance Criteria Glossary v1.xlsx -->
<!-- converted: 2026-11-16 from XLSX -->

> **Source:** `04 User stories/Recovery Workbench Acceptance Criteria Glossary v1.xlsx`  
> **Converted from:** XLSX

## Keywords

| Keywords |  |  |  |
|---|---|---|---|
| Every acceptance criteria line starts with one of these words. The word tells you what the line is for. คำแรกของทุกบรรทัดบอกหน้าที่ของบรรทัดนั้น |  |  |  |
| Keyword | Reading label | ภาษาไทย | What the line is doing |
| Given | Setup | สิ่งที่ต้องมีอยู่ก่อน | What is already true before the test starts. It is not an action and nobody does it during the test. |
| When | Action | การกระทำ | The one action that starts the test. Each scenario has one When. |
| Then | Result | ผลที่ต้องได้ | What must be true after the action. A scenario can have many Then lines, and every one of them must hold. |
| Scenario | Scenario | สถานการณ์ทดสอบ | One case to prove. The AC number in the title, such as AC3, is how it is referred to elsewhere. |

## Sentence frames

| Sentence frames |  |  |
|---|---|---|
| The acceptance criteria repeat a small number of sentence patterns. Learn these and most lines read themselves. ประโยคในเกณฑ์ยอมรับใช้รูปแบบซ้ำกันไม่กี่แบบ |  |  |
| English pattern | ภาษาไทย | Example from a story |
| the system writes {X} | ระบบเขียน {X} | Then the system writes 12 dq_exception rows |
| the system writes {X} to {Y} | ระบบเขียน {X} ลงใน {Y} | Then the system writes the result to the decision log |
| the system writes {X} with {Y} | ระบบเขียน {X} พร้อมข้อมูล {Y} | Then the system writes one entry with rule ID "ALLOC-014" |
| the system writes no {X} | ระบบไม่เขียน {X} | Then the system writes no row |
| nothing is written | ไม่มีการเขียนข้อมูลใด | Then nothing is written |
| the system refuses {X} | ระบบไม่รับ {X} | Then the system refuses the load |
| the system refuses {X} in full | ระบบไม่รับ {X} ทั้งรายการ | Then the system refuses the load in full |
| refuses {X} with {MSG} | ไม่รับ {X} พร้อมข้อความ {MSG} | Then the system refuses the load with MSG-P1-002 |
| the system stores {X} | ระบบจัดเก็บ {X} | Then the system stores the document on case "RW-2026-000123" |
| the system raises {X} | ระบบแจ้ง {X} | Then the system raises an incident |
| the system sends {X} to {Y} | ระบบส่ง {X} ไปยัง {Y} | Then the system sends the file to the interface |
| the system holds {X} in {Y} | ระบบพัก {X} ไว้ใน {Y} | Then the system holds the 3 records in dq_exception |
| the system places the case in queue {Q} | ระบบจัดกรณีเข้าคิว {Q} | Then the system places the case in queue "MTG-BKK-CO" |
| the system creates no {X} | ระบบไม่สร้าง {X} | Then the system creates no case for A-5002 |
| the system returns {N} with {MSG} | ระบบคืนค่า {N} พร้อมข้อความ {MSG} | Then the system returns 409 with MSG-GEN-004 |
| the system records {X} | ระบบบันทึก {X} | Then the system records the rollback with the caller and the time |
| the system publishes {X} | ระบบเผยแพร่ {X} | Then the system publishes the copy |
| the system retires {X} | ระบบยกเลิกการใช้ {X} | Then the system retires the old copy |
| the system gives the case to {U} | ระบบมอบกรณีให้ {U} | Then the system gives the case to U-03 |
| the system does not {X} | ระบบไม่ {X} | Then the system does not start |
| the case moves to {STATE} | กรณีเปลี่ยนไปยังขั้นตอน {STATE} | Then the case moves to "IN_LITIGATION" |
| the case stays in {STATE} | กรณียังคงอยู่ในขั้นตอน {STATE} | Then the case stays in "NEW" |
| nothing changes | ไม่มีการเปลี่ยนแปลง | Then nothing changes |
| {X} is unchanged | {X} ไม่เปลี่ยนแปลง | Then the row counts are unchanged |
| {X} is in force | {X} มีผลบังคับใช้อยู่ | Given version "DOA-2026.11" is in force |
| {X} stays in force | {X} ยังคงมีผลบังคับใช้ | Then the version in force stays |
| {X} holds {N} rows | {X} มี {N} แถว | Then data_product holds 14 rows |
| {X} shows {Y} | {X} แสดง {Y} | Then the job monitor shows the failed step |
| the response is {N} | ผลตอบกลับคือ {N} | Then the response is 200 |
| the build fails with "{msg}" | การ build ไม่ผ่าน พร้อมข้อความ "{msg}" | Then the build fails with "no data dictionary entry" |
| the test fails with "{msg}" | การทดสอบไม่ผ่าน พร้อมข้อความ "{msg}" | Then the test fails with "physical type date expected" |
| {X} passes | {X} ผ่าน | Then check "REC-08" passes |
| {X} fails | {X} ไม่ผ่าน | Then the pipeline stage fails |
| the user sees {X} | ผู้ใช้เห็น {X} | Then the user sees the case list |
| the officer sees {X} on the screen | เจ้าหน้าที่เห็น {X} บนหน้าจอ | Then the officer sees the queue on the screen |
| {X} is on the exception list | {X} อยู่ในรายการผิดปกติ | Then the payment is on the exception list |
| {X} is in the exception queue | {X} อยู่ในคิวรายการผิดปกติ | Then the item is in the exception queue |
| naming {X} | โดยระบุ {X} | Then the system refuses the load naming "business date" |
| with reason {R} | พร้อมเหตุผล {R} | Then the entry carries the reason "RULE_GAP" |
| for business date {D} | สำหรับวันที่ทำการ {D} | Then JOB-15 is rerun for business date 2026-11-27 |
| within {N} seconds | ภายใน {N} วินาที | Then the screen opens within 2 seconds |
| at least {N} | อย่างน้อย {N} | Then at least 20 feedback entries are counted |
| at most {N} | ไม่เกิน {N} | Then the export holds at most 10,000 rows |
| no {X} | ไม่มี {X} | Then no instance is restarted |
| every {X} | {X} ทุกรายการ | Then every record passes the load checks |
| each {X} | {X} แต่ละรายการ | Then each row has exactly one owner |
| the same {X} | {X} เดียวกัน | Then the same call is refused |
| again | อีกครั้ง | When the pipeline runs again in SIT |
| {X} is not available | {X} ไม่พร้อมใช้งาน | Given the malware scan is not available |
| the timer starts | เริ่มนับเวลา | Then the timer starts |
| the timer ends on {D} | ครบกำหนดในวันที่ {D} | Then the timer ends on 2026-12-15 |
| past its service level | เกินระยะเวลามาตรฐาน | Then the case is past its service level |
| {X} is approved | {X} ได้รับอนุมัติ | Given the treatment is approved |
| needs approval at level {L} | ต้องได้รับอนุมัติระดับ {L} | Then the item needs approval at level 3 |
| exactly one {X} | {X} เพียงหนึ่งเดียว | Then each row has exactly one system of record |

## Words

| Words |  |  |  |
|---|---|---|---|
| The words that carry the meaning, in order of how often they appear in the acceptance criteria. คำที่พบบ่อยในเกณฑ์ยอมรับ |  |  |  |
| English | ภาษาไทย | Kind | What it means here |
| case | กรณี | noun | A recovery case. The unit of work in the Workbench. |
| cases | กรณี (พหูพจน์) | noun | More than one case. English adds s; Thai does not. |
| queue | คิว | noun | A list of work waiting for a team or a person. |
| exception queue | คิวรายการผิดปกติ | noun | Where items go when they do not pass a check. |
| exception list | รายการผิดปกติ | noun | The list of items that did not pass a check. |
| load | การโหลดข้อมูล | noun | One run that brings a file of data into the Workbench. |
| loads | โหลดข้อมูล | verb | Brings the data in. |
| row | แถว | noun | One line of a table or a file. |
| rows | แถว (พหูพจน์) | noun | More than one row. |
| field | ฟิลด์ | noun | One named item of data in a record. |
| entry | รายการ | noun | One record written into a log. |
| decision log | บันทึกการตัดสินใจ | noun | The append-only record of every decision. |
| interaction ledger | บันทึกประวัติการติดต่อ | noun | The record of every contact with a customer. |
| rule | เกณฑ์ | noun | A business rule the system applies. |
| version | ฉบับ | noun | One issued version of a rule, table or document. |
| in force | มีผลบังคับใช้ | phrase | The version that applies right now. |
| data product | ผลิตภัณฑ์ข้อมูล | noun | One of the 14 named sets of recovery data. |
| data dictionary | พจนานุกรมข้อมูล | noun | The list of every field, its type and its owner. |
| system of record | ระบบต้นทางหลัก | noun | The one system that holds the true value. |
| owner | ผู้รับผิดชอบ | noun | The named person or role accountable for it. |
| status | สถานะ | noun | The current condition of a record. |
| state | ขั้นตอน | noun | Where the case sits in its journey. |
| result | ผลลัพธ์ | noun | What the action produced. |
| run | รอบการทำงาน | noun | One execution of a job or a load. |
| runs | ทำงาน | verb | Executes. |
| job | งาน | noun | A scheduled piece of processing. |
| run book | คู่มือการดำเนินงาน | noun | The instructions for operating a job. |
| business date | วันที่ทำการ | noun | The banking day the data belongs to, not the clock date. |
| file | ไฟล์ | noun | A file taken in or sent out. |
| document | เอกสาร | noun | A document held against a case. |
| notice | หนังสือ | noun | A formal letter to a customer. |
| template | แม่แบบ | noun | The approved pattern a notice is made from. |
| treatment | แนวทางแก้ไขหนี้ | noun | The agreed way of resolving the debt. |
| offer | ข้อเสนอ | noun | What is put to the customer. |
| settlement | การประนอมหนี้ | noun | An agreement to close for less than the full amount. |
| plan | แผนการชำระ | noun | The schedule the customer agrees to pay on. |
| payment | การชำระเงิน | noun | Money received. |
| promise | คำรับปากชำระ | noun | A commitment by the customer to pay. |
| customer | ลูกค้า | noun | The bank customer. |
| debtor | ลูกหนี้ | noun | The customer who owes. |
| party | คู่กรณี | noun | A person or company connected to the case. |
| account | บัญชี | noun | The loan or facility account. |
| collateral | หลักประกัน | noun | Security held against the debt. |
| asset | ทรัพย์สิน | noun | Property taken or held for sale. |
| appraisal | ราคาประเมิน | noun | The valuation of an asset. |
| floor | ราคาขั้นต่ำ | noun | The lowest price allowed. |
| bid | การเสนอราคา | noun | An offer to buy at auction. |
| claim | สิทธิเรียกร้อง | noun | The bank legal claim. |
| court | ศาล | noun | The court. |
| litigation | การฟ้องคดี | noun | Legal action. |
| deviation | เหตุผิดปกติ | noun | A case that falls outside the normal path. |
| incident | เหตุขัดข้อง | noun | A technical failure that is raised and tracked. |
| alert | การแจ้งเตือน | noun | A warning sent to a person or a team. |
| service level | ระยะเวลามาตรฐาน | noun | The time a step is allowed to take. |
| timer | การนับเวลา | noun | A clock the system runs against a case. |
| escalation | การส่งต่อระดับสูงขึ้น | noun | Passing the case up when time runs out. |
| allocation | การจัดสรรงาน | noun | Deciding who gets the case. |
| transfer | การโอนงาน | noun | Moving a case to another owner or team. |
| role | บทบาท | noun | What a user is allowed to do. |
| scope | ขอบเขตงาน | noun | The set of cases a user may see. |
| permission | สิทธิ์ | noun | A single right granted to a role. |
| break-glass | สิทธิ์เข้าถึงกรณีฉุกเฉิน | noun | Emergency access, approved and fully recorded. |
| approval | การอนุมัติ | noun | A decision to allow something. |
| approver | ผู้อนุมัติ | noun | The person who approves. |
| sign-off | การลงนาม | noun | Formal acceptance. |
| officer | เจ้าหน้าที่ | noun | The person working the case. |
| team manager | ผู้จัดการทีม | noun | The manager of a collections or recovery team. |
| administrator | ผู้ดูแลระบบ | noun | The person who administers the Workbench. |
| data steward | ผู้ดูแลข้อมูล | noun | The person accountable for a data product. |
| partner | คู่ค้า | noun | An outside agency or law firm. |
| agent | เอเจนต์ | noun | An AI agent in the Workbench. |
| model | แบบจำลอง | noun | A scoring or prediction model. |
| confidence | ระดับความเชื่อมั่น | noun | How sure the model is. |
| sample | ชุดตัวอย่าง | noun | The set of records an agent is tested on. |
| evaluation | การประเมิน | noun | A test run of an agent against a sample. |
| screen | หน้าจอ | noun | A page of the Workbench. |
| filter | ตัวกรอง | noun | A condition that narrows a list. |
| export | การส่งออก | noun | Taking data out to a file. |
| dashboard | แดชบอร์ด | noun | The screen of measures. |
| measure | ตัวชี้วัด | noun | A published number. |
| baseline | ข้อมูลฐาน | noun | The agreed starting figures. |
| reconciliation | การกระทบยอด | noun | Checking two sets of numbers agree. |
| check | การตรวจสอบ | noun | One test the data must pass. |
| control total | ยอดควบคุม | noun | A total used to prove a file is complete. |
| intake | การรับเข้า | noun | Taking a document or file in. |
| outbox | คิวรายการส่งออก | noun | Where outbound messages wait. |
| event | เหตุการณ์ | noun | A message published when something happens. |
| interface | อินเทอร์เฟซ | noun | A connection to another system. |
| parameter | พารามิเตอร์ | noun | A setting held outside the code. |
| reference data | ข้อมูลอ้างอิง | noun | Lists and tables loaded, not coded. |
| catalog | แค็ตตาล็อก | noun | The list of data products and their owners. |
| schema | โครงสร้างฐานข้อมูล | noun | The database structure. |
| migration | สคริปต์ปรับโครงสร้างฐานข้อมูล | noun | A script that changes the schema. |
| pipeline | ขั้นตอนการติดตั้งอัตโนมัติ | noun | The build and deploy chain. |
| build | การ build | noun | Compiling and testing the code. |
| hash | ค่าแฮช | noun | The value that proves a record was not altered. |
| chain | ห่วงโซ่ | noun | Records linked so a change can be detected. |
| archive | การเก็บถาวร | noun | Moving data to long term storage. |
| retention | ระยะเวลาเก็บรักษา | noun | How long a record must be kept. |
| personal data | ข้อมูลส่วนบุคคล | noun | Data covered by PDPA. |
| consent | ความยินยอม | noun | The customer permission to be contacted. |
| channel | ช่องทาง | noun | How the customer is contacted. |
| writes | เขียน | verb | Puts a record into a table or a log. |
| refuses | ไม่รับ | verb | Rejects it. Nothing is saved. |
| holds | มี | verb | Contains. "the table holds 14 rows" means it contains 14 rows. |
| holds (keeps back) | พักไว้ | verb | Keeps an item back from processing. |
| shows | แสดง | verb | Displays on a screen or report. |
| names | ระบุชื่อ | verb | States which one. |
| naming | โดยระบุ | verb | Stating which one, in the same sentence. |
| carries | มีข้อมูล | verb | Contains this detail. |
| moves | เปลี่ยนไปยัง | verb | Changes to another state or owner. |
| stays | ยังคงอยู่ | verb | Does not change. |
| keeps | คงไว้ | verb | Does not remove. |
| raises | แจ้ง | verb | Creates an incident or an alert. |
| returns | คืนค่า | verb | Sends back, usually an API code. |
| calls | เรียกใช้ | verb | Invokes another service. |
| places | จัดเข้า | verb | Puts the case into a queue. |
| retires | ยกเลิกการใช้ | verb | Takes out of use, keeping the record. |
| publishes | เผยแพร่ | verb | Makes available to others. |
| applies | ใช้ | verb | Puts a rule or a migration into effect. |
| passes | ผ่าน | verb | Meets the check. |
| fails | ไม่ผ่าน | verb | Does not meet the check. |
| matches | ตรงกับ | verb | Agrees with. |
| reconciles | กระทบยอดตรงกัน | verb | Two sets of numbers agree. |
| rerun | ทำงานซ้ำ | verb | Run again. |
| rolls back | ย้อนกลับ | verb | Undoes the change. |
| sees | เห็น | verb | What appears to the user. |
| acts | ดำเนินการ | verb | Takes the action. |
| arrives | มาถึง | verb | Is received. |
| no | ไม่มี | word | None at all. "no row is written" means zero rows. |
| nothing | ไม่มีสิ่งใด | word | Not anything. |
| not | ไม่ | word | Negative. |
| cannot | ไม่สามารถ | word | Is not allowed or not able. |
| every | ทุก | word | All of them, without exception. |
| each | แต่ละ | word | One by one. |
| exactly | พอดี | word | That number, no more and no less. |
| at least | อย่างน้อย | phrase | That number or more. |
| at most | ไม่เกิน | phrase | That number or less. |
| within | ภายใน | word | Inside that time or that limit. |
| within (time) | ภายในเวลา | phrase | Before that much time has passed. |
| again | อีกครั้ง | word | A second time. |
| still | ยังคง | word | As before, unchanged. |
| same | เดียวกัน | word | Not a different one. |
| other | อื่น | word | A different one. |
| whole / in full | ทั้งรายการ | phrase | The entire file, not part of it. |
| unchanged | ไม่เปลี่ยนแปลง | word | Exactly as it was. |
| due | ครบกำหนด | word | The date it must happen by. |
| past | เกิน | word | Later than the limit. |
| open | ยังไม่ปิด | word | Still active. |
| closed | ปิดแล้ว | word | Finished. |
| valid | ถูกต้อง | word | Passes its rules. |
| empty | ไม่มีข้อมูล | word | Holds no value. |
| true / false | จริง / เท็จ | word | The two values of a yes-no field. |
| per | ต่อ | word | For each one. |
| against | เทียบกับ | word | Compared with. |
| by | โดย | word | Who did it, or the method used. |
| with | พร้อมกับ | word | Carrying this detail as well. |
| from | จาก | word | The source. |
| to | ไปยัง | word | The destination. |
| before | ก่อน | word | Earlier than. |
| after | หลังจาก | word | Later than. |
| in a row | ติดต่อกัน | phrase | One after another with no break. |
| on hold | ถูกระงับไว้ | phrase | Stopped until something else happens. |
| switched off | ถูกปิดอยู่ | phrase | Turned off by a setting. |
| read-only | อ่านได้อย่างเดียว | phrase | Can be read, cannot be changed. |
| append-only | เพิ่มได้อย่างเดียว | phrase | Records can be added, never changed or deleted. |
| idempotent | ทำซ้ำได้ผลเดิม | phrase | Running it twice gives the same result as once. |
| end to end | ตั้งแต่ต้นจนจบ | phrase | The whole path from start to finish. |

## Code prefixes

| Code prefixes |  |  |  |
|---|---|---|---|
| What the codes in a story mean. Click any code in the project hub to read its full wording. ความหมายของรหัสที่ปรากฏในสตอรี |  |  |  |
| Prefix | English | ภาษาไทย | What it is |
| REQ- | Requirement | ข้อกำหนด | A numbered program requirement the story answers. |
| BR- | Business rule | กฎทางธุรกิจ | A rule of the business the build must follow. |
| VR- | Validation rule | กฎการตรวจสอบข้อมูล | A check on a value before it is accepted. |
| SC- | System constraint | ข้อจำกัดของระบบ | A limit the system imposes. |
| AC- | Acceptance code, main flow | รหัสเกณฑ์ยอมรับ เส้นทางหลัก | The normal path through the scenario. |
| AC-ALT- | Acceptance code, alternate flow | รหัสเกณฑ์ยอมรับ เส้นทางรอง | A different but valid path. |
| AC-EXC- | Acceptance code, exception flow | รหัสเกณฑ์ยอมรับ กรณีผิดปกติ | What happens when something fails. |
| AC-BG- | Acceptance code, background event | รหัสเกณฑ์ยอมรับ เหตุการณ์เบื้องหลัง | Something the system does with no person involved. |
| DF- | Data field | ฟิลด์ข้อมูล | One field in the data dictionary. |
| MSG- | Message | ข้อความระบบ | A message shown to a user, in Thai and English. |
| LOV- | List of values | รายการค่าที่อนุญาต | The allowed values for a field. |
| FEAT- | Feature | ฟีเจอร์ | A feature of a module. |
| DL | Open decision | ประเด็นที่ยังไม่ตัดสินใจ | A decision still to be made. |
| DT | Technical decision | การตัดสินใจทางเทคนิค | A technical decision already taken. |
| RWB- | User story | ยูสเซอร์สตอรี | A story key, such as RWB-E1-001. |
