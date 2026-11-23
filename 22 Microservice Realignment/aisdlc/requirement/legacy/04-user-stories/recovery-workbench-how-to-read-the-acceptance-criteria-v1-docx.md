<!-- source: 04 User stories/Recovery Workbench How To Read The Acceptance Criteria v1.docx -->
<!-- converted: 2026-11-16 from DOCX -->

> **Source:** `04 User stories/Recovery Workbench How To Read The Acceptance Criteria v1.docx`  
> **Converted from:** DOCX

Recovery Workbench

How to read the acceptance criteria

SCB Collections and Recovery. Henka Group.

Every user story ends in a set of acceptance criteria. They are the test the build must pass, and they are written to one pattern. Once you know the pattern, every story in the set reads the same way.

ทุกสตอรีจบด้วยเกณฑ์ยอมรับ ซึ่งเป็นสิ่งที่งานพัฒนาต้องผ่าน และเขียนด้วยรูปแบบเดียวกันทั้งหมด เมื่อเข้าใจรูปแบบนี้แล้ว จะอ่านได้ทุกสตอรีในชุดเอกสาร

A scenario has three parts

Each scenario is one case to prove. Every line starts with a word that says what the line is for.

แต่ละสถานการณ์ทดสอบคือหนึ่งกรณีที่ต้องพิสูจน์ ทุกบรรทัดขึ้นต้นด้วยคำที่บอกหน้าที่ของบรรทัดนั้น

| Keyword | Reading label | ภาษาไทย | What the line is for |
|---|---|---|---|
| Given | Setup | สิ่งที่ต้องมีอยู่ก่อน | What is already true before the test starts. Nobody does it during the test. |
| When | Action | การกระทำ | The one action that starts the test. Each scenario has one of these. |
| Then | Result | ผลที่ต้องได้ | What must be true after the action. There are often several, and every one must hold. |

Every line states its own role

A line used to start with And, which meant it took its meaning from the line above. Those are gone. A line that is a second result now starts with Then, and a line that is a second precondition starts with Given. You never have to look upward to know what a line is doing.

เดิมบางบรรทัดขึ้นต้นด้วย And ซึ่งต้องย้อนไปดูบรรทัดก่อนหน้าจึงจะเข้าใจ ตอนนี้ไม่มีแล้ว บรรทัดที่เป็นผลลัพธ์เพิ่มเติมจะขึ้นต้นด้วย Then และบรรทัดที่เป็นเงื่อนไขเพิ่มเติมจะขึ้นต้นด้วย Given จึงไม่ต้องย้อนขึ้นไปอ่านบรรทัดบนอีก

The result says who acts

A result names the actor and leads with the verb. "The load is refused" is now "the system refuses the load". The meaning is the same; the sentence says who does it.

บรรทัดผลลัพธ์จะระบุผู้กระทำและขึ้นต้นด้วยคำกริยา เช่น "The load is refused" เปลี่ยนเป็น "the system refuses the load" ความหมายเหมือนเดิม แต่บอกชัดว่าใครเป็นผู้กระทำ

A worked example

This is AC7 from RWB-E1-001, the story that creates the recovery tables.

ตัวอย่างนี้คือ AC7 ของสตอรี RWB-E1-001

| Label | ภาษาไทย | The line | What it is telling you |
|---|---|---|---|
| Setup | สิ่งที่ต้องมีอยู่ก่อน | a catalog load file gives DP06 two systems of record, "CCMS; SVAF" | The file already exists and is wrong in this way. You do not build this; you assume it. |
| Setup | สิ่งที่ต้องมีอยู่ก่อน | the same file gives DP11 no owner user ID | A second fault in the same file. Both faults are present at once. |
| Action | การกระทำ | the reference data administrator loads the file | The single action. A person with that role loads it. |
| Result | ผลที่ต้องได้ | the system refuses the whole file and writes no row | All or nothing. One bad row stops the entire file. |
| Result | ผลที่ต้องได้ | the system returns MSG-P1-003 once for DP06 and once for DP11 | Two messages, one per fault. Click the code in the hub for its exact wording in Thai and English. |
| Result | ผลที่ต้องได้ | data_product still holds the rows of the version in force | The previous good data is untouched. |

The sentence patterns that repeat

These patterns cover most of the result lines in the set.

รูปแบบประโยคเหล่านี้ครอบคลุมบรรทัดผลลัพธ์ส่วนใหญ่ในชุดเอกสาร

| Pattern | ภาษาไทย |
|---|---|
| the system writes {X} to {Y} | ระบบเขียน {X} ลงใน {Y} |
| the system writes no {X} | ระบบไม่เขียน {X} |
| the system refuses {X} with {MSG} | ระบบไม่รับ {X} พร้อมข้อความ {MSG} |
| the system refuses {X} in full | ระบบไม่รับ {X} ทั้งรายการ |
| the system stores {X} | ระบบจัดเก็บ {X} |
| the system raises {X} | ระบบแจ้ง {X} |
| the system places the case in queue {Q} | ระบบจัดกรณีเข้าคิว {Q} |
| the system returns {N} with {MSG} | ระบบคืนค่า {N} พร้อมข้อความ {MSG} |
| the case moves to {STATE} | กรณีเปลี่ยนไปยังขั้นตอน {STATE} |
| the case stays in {STATE} | กรณียังคงอยู่ในขั้นตอน {STATE} |
| nothing changes | ไม่มีการเปลี่ยนแปลง |
| {X} is unchanged | {X} ไม่เปลี่ยนแปลง |
| {X} is in force | {X} มีผลบังคับใช้อยู่ |
| {X} holds {N} rows | {X} มี {N} แถว |
| {X} shows {Y} | {X} แสดง {Y} |
| {X} passes / {X} fails | {X} ผ่าน / {X} ไม่ผ่าน |
| naming {X} | โดยระบุ {X} |
| for business date {D} | สำหรับวันที่ทำการ {D} |
| within {N} seconds | ภายใน {N} วินาที |
| at least {N} / at most {N} | อย่างน้อย {N} / ไม่เกิน {N} |
| exactly one {X} | {X} เพียงหนึ่งเดียว |
| {X} is on the exception list | {X} อยู่ในรายการผิดปกติ |

The codes you will see

Codes name a rule, a field or a message. In the project hub, click any code and its full wording opens under the line you are reading.

รหัสต่าง ๆ ใช้อ้างถึงกฎ ฟิลด์ หรือข้อความ ในโปรเจกต์ฮับ สามารถคลิกที่รหัสเพื่อดูเนื้อหาเต็มได้ทันทีใต้บรรทัดที่กำลังอ่าน

| Prefix | English | ภาษาไทย |
|---|---|---|
| REQ- | Requirement | ข้อกำหนด |
| BR- | Business rule | กฎทางธุรกิจ |
| VR- | Validation rule | กฎการตรวจสอบข้อมูล |
| SC- | System constraint | ข้อจำกัดของระบบ |
| AC- | Acceptance code, main flow | รหัสเกณฑ์ยอมรับ เส้นทางหลัก |
| AC-EXC- | Acceptance code, exception flow | รหัสเกณฑ์ยอมรับ กรณีผิดปกติ |
| AC-BG- | Acceptance code, background event | รหัสเกณฑ์ยอมรับ เหตุการณ์เบื้องหลัง |
| DF- | Data field | ฟิลด์ข้อมูล |
| MSG- | Message, written in Thai and English | ข้อความระบบ มีทั้งภาษาไทยและอังกฤษ |
| LOV- | List of values | รายการค่าที่อนุญาต |
| DL / DT | Open decision / technical decision | ประเด็นที่ยังไม่ตัดสินใจ / การตัดสินใจทางเทคนิค |
| RWB- | User story | ยูสเซอร์สตอรี |

Where to read more

The project hub opens each story with its acceptance criteria already labelled Setup, Action and Result. The button marked ไทย turns on the Thai meaning of the words in each line.

โปรเจกต์ฮับจะแสดงเกณฑ์ยอมรับของแต่ละสตอรีพร้อมป้ายกำกับ Setup, Action และ Result และปุ่ม ไทย จะเปิดคำแปลของคำศัพท์ในแต่ละบรรทัด

The glossary file holds the words, the sentence patterns and the codes, with Thai for each. Its Thai follows the wording already used in the Workbench message standard, so a word means the same thing on the screen as it does in a story.

ไฟล์อภิธานศัพท์รวบรวมคำศัพท์ รูปแบบประโยค และรหัสต่าง ๆ พร้อมคำแปลภาษาไทย โดยใช้คำตามมาตรฐานข้อความของระบบ เพื่อให้คำเดียวกันมีความหมายตรงกันทั้งบนหน้าจอและในสตอรี

If a line is still unclear, the squad lead should raise it against the story key. The wording is changed once, in the story, so every reader gets the same correction.

หากยังมีบรรทัดที่ไม่ชัดเจน หัวหน้าทีมสามารถแจ้งโดยอ้างอิงรหัสสตอรี เพื่อแก้ไขถ้อยคำที่ต้นทางเพียงครั้งเดียว ผู้อ่านทุกคนจะได้รับฉบับที่แก้ไขแล้วเหมือนกัน
