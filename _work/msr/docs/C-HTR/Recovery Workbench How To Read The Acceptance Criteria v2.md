SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

# Recovery Workbench

## How to read the acceptance criteria

SCB Collections and Recovery. Henka Group.

| Item | Detail |
|---|---|
| Document | Recovery Workbench how to read the acceptance criteria |
| Version | 2 |
| Date | 22 November 2026 |
| Supersedes | Version 1. The source gives no date and no status; the version is read from the file name (CG-C-HTR-1; ASM-C-HTR-1) |
| Prepared by | Henka Group |
| Applies to | Every reader of a Recovery Workbench story: the squads, the ACE team, the platform team, QA and the business |
| Decision | D-RCV-60: adopt Architecture v5 and realign the documents and stories |
| Status | Draft. No approval of this version is recorded (ASM-C-HTR-2) |
| Change | 2, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash |

## Change log

| Version | Date | Change |
|---|---|---|
| 2 | 22 November 2026 | D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash. Adds How the set is sliced, The origin tag at the end of every scenario, The AC number inside the tag and Reading the slices of one legacy story, and extends A worked example and Where to read more. The sections A scenario has three parts, Every line states its own role, The result says who acts, The sentence patterns that repeat and The codes you will see are kept word for word with their Thai text |
| 1 | Not specified in the source documents (CG-C-HTR-1; ASM-C-HTR-1) | The reading pattern as issued: the three parts of a scenario, the role of each line, the actor in the result, one worked example, the repeating sentence patterns and the code prefixes. The source gives no version, date or status; the version is read from the file name (CG-C-HTR-1; ASM-C-HTR-1) |

Every user story ends in a set of acceptance criteria. They are the test the build must pass, and they are written to one pattern. Once you know the pattern, every story in the set reads the same way.

ทุกสตอรีจบด้วยเกณฑ์ยอมรับ ซึ่งเป็นสิ่งที่งานพัฒนาต้องผ่าน และเขียนด้วยรูปแบบเดียวกันทั้งหมด เมื่อเข้าใจรูปแบบนี้แล้ว จะอ่านได้ทุกสตอรีในชุดเอกสาร

This version adds one idea to the pattern. A legacy story no longer maps to one story: it maps to a set of slices, one per service and work type, and every scenario now ends with a tag that says whether it comes from the legacy story or was added by the realignment. Four sections are new or extended for that: How the set is sliced, The origin tag at the end of every scenario, The AC number inside the tag and Reading the slices of one legacy story. The rest of the guide reads as it did.

## How the set is sliced

A story in this set is one slice of the work: the work one team type does for one service, and the smallest thing that can be built, tested and released on its own. A legacy story that asked several services to change becomes one story per service and work type, and each of those stories carries the acceptance criteria that belong to it. This version of the set holds 1,034 slices over 358 keys, 341 of them legacy stories and 17 new, and the slices fall into 288 contract stories, 513 app development stories, 11 ACE DB stories, 18 infrastructure stories, 57 DevOps stories and 147 integration stories (CG-C-HTR-4; ASM-C-HTR-4).

A story key says which slice you are reading. It has four parts, and a fifth for the delta copy of a preserved story.

| Part | Values | Example |
|---|---|---|
| RWB | Always RWB | RWB |
| Scope | P1 to P10 and S1 to S9 for the 19 services, PLT for a platform epic, ITG for an integration epic | ITG |
| Legacy compact | The legacy key without its dashes: E1001 for RWB-E1-001, TE001 for RWB-TE-001, AD003 for RWB-AD-003. N001 onwards is a new platform story and W1J01 the new integration harness | E1001 |
| Work type | CON, APP, DB, INF, OPS or ITG | ITG |
| -2 | The delta copy of a preserved story; the copy without -2 stays the as-built story | -2 |

So RWB-P3-E1018-APP is the app development slice of RWB-E1-018 on rwb-case, and RWB-PLT-TE001-APP is the preserved technical enabler RWB-TE-001 with RWB-PLT-TE001-APP-2 as its delta. A reader who knows the legacy key can find every slice of it from its key.

| Work type | Key ends | What the slice proves | Suggested owner |
|---|---|---|---|
| Contract | -CON | What the service publishes and consumes: the request, the response, the event, the error and the timeout. A contract story is always Day 1 and has no build dependency | TechX (suggested; any team may pick up this story) |
| App development | -APP | The behaviour inside one service, built against the contract stories and their fakes | TechX (suggested; any team may pick up this story) |
| ACE DB | -DB | The service's own schema, its migration and its grants | ACE team (suggested; any team may pick up this story) |
| Infrastructure | -INF | The environment, the database instance and the deployment the service needs | SCB IT infrastructure (suggested; any team may pick up this story) |
| DevOps | -OPS | The pipeline, the monitoring and the run tasks of the service | DevOps team (suggested; any team may pick up this story) |
| Integration | -ITG | The real cross-service behaviour: two or more services, the topic and the workflow. Integration dependencies sit only here | TechX (suggested; any team may pick up this story); a harness or NFR story reads QA team (suggested; any team may pick up this story) |

RWB-E1-001, the story that creates the recovery tables, is one legacy story and five slices: RWB-P1-E1001-APP on rwb-source-data, RWB-P7-E1001-APP on rwb-decision, RWB-P4-E1001-APP on rwb-access, RWB-P8-E1001-APP on rwb-payment and RWB-ITG-E1001-ITG across them. Read the five together as one story whose criteria have been sorted by owner.

Six stories are kept word for word, because they are built or in build: RWB-TE-001, RWB-TE-002, RWB-TE-003, RWB-E1-042, RWB-E1-043 and RWB-E1-044. The slice with the base key holds the legacy text as built, and the microservice change sits in the -2 copy or in a platform contract or DevOps story. In a preserved story sections 1 to 11, 14 to 16, 18 and 19 are the as-built text, and sections 12 and 13 are marked as the monolith.

## A scenario has three parts

Each scenario is one case to prove. Every line starts with a word that says what the line is for.

แต่ละสถานการณ์ทดสอบคือหนึ่งกรณีที่ต้องพิสูจน์ ทุกบรรทัดขึ้นต้นด้วยคำที่บอกหน้าที่ของบรรทัดนั้น

| Keyword | Reading label | ภาษาไทย | What the line is for |
|---|---|---|---|
| Given | Setup | สิ่งที่ต้องมีอยู่ก่อน | What is already true before the test starts. Nobody does it during the test. |
| When | Action | การกระทำ | The one action that starts the test. Each scenario has one of these. |
| Then | Result | ผลที่ต้องได้ | What must be true after the action. There are often several, and every one must hold. |


## Every line states its own role

A line used to start with And, which meant it took its meaning from the line above. Those are gone. A line that is a second result now starts with Then, and a line that is a second precondition starts with Given. You never have to look upward to know what a line is doing.

เดิมบางบรรทัดขึ้นต้นด้วย And ซึ่งต้องย้อนไปดูบรรทัดก่อนหน้าจึงจะเข้าใจ ตอนนี้ไม่มีแล้ว บรรทัดที่เป็นผลลัพธ์เพิ่มเติมจะขึ้นต้นด้วย Then และบรรทัดที่เป็นเงื่อนไขเพิ่มเติมจะขึ้นต้นด้วย Given จึงไม่ต้องย้อนขึ้นไปอ่านบรรทัดบนอีก

## The result says who acts

A result names the actor and leads with the verb. "The load is refused" is now "the system refuses the load". The meaning is the same; the sentence says who does it.

บรรทัดผลลัพธ์จะระบุผู้กระทำและขึ้นต้นด้วยคำกริยา เช่น "The load is refused" เปลี่ยนเป็น "the system refuses the load" ความหมายเหมือนเดิม แต่บอกชัดว่าใครเป็นผู้กระทำ

## A worked example

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

In this version the same scenario sits in RWB-ITG-E1001-ITG, the integration slice of RWB-E1-001. The scenario line keeps its number, AC7, and adds the origin tag at the end: (legacy RWB-E1-001 AC7). The table above reads exactly as it did.

## The origin tag at the end of every scenario

Every scenario starts with Scenario, the number of the criterion and a short name, and ends with the origin in brackets. The tag answers one question: was this line promised before the realignment, or is it new? There are only two tags.

| Tag | Written like this | What it tells you |
|---|---|---|
| Legacy origin | (legacy RWB-E1-001 AC7) | The scenario is AC7 of RWB-E1-001 and was written before the realignment. Its meaning is unchanged; only the actor and the sentence shape follow the pattern above. AC7 is the same scenario in every place it appears |
| New origin | (new, D-RCV-60) | The scenario was added by the realignment and has no earlier text. The line is the whole requirement, and there is nothing older to compare it with |

Nothing else ends a scenario. A line with no tag, or with a third kind of tag, is a defect in the story and is raised against the story key.

## The AC number inside the tag

A story numbers its scenarios AC1, AC2 and so on. A scenario taken from a legacy story keeps the number it has there, so the numbers in a slice can have gaps. In RWB-ITG-E1001-ITG the inherited scenarios are AC2, AC3 and AC7; AC1 and AC4 to AC11 are in RWB-P1-E1001-APP. The gap is the reading help: it shows that another slice of the same legacy story owns the missing numbers, and that ACn names one scenario and is not a count.

A new scenario takes the next free number in its story. In RWB-ITG-E1001-ITG the new scenarios are AC12 to AC15, after AC11, the last number of RWB-E1-001. A story with no legacy ancestor starts at AC1, and every one of its scenarios is new.

| The line starts | The tag | The reading |
|---|---|---|
| Scenario: AC2 Dictionary published | (legacy RWB-E1-001 AC2) | Inherited from the legacy story, with its number and its meaning |
| Scenario: AC7 Catalog row with two systems of record is refused | (legacy RWB-E1-001 AC7) | The worked example above, in the story that carries it now |
| Scenario: AC12 Every one of the 92 tables resolves to exactly one owning schema | (new, D-RCV-60) | Added by the realignment; there is no legacy text for it |
| Scenario: AC15 The same catalog file loaded twice writes nothing the second time | (new, D-RCV-60) | Added by the realignment, and numbered after the last legacy number |

## Reading the slices of one legacy story

Read the slices of a legacy story in the order a service needs them: the contract stories first, because they are Day 1 and everything else builds against them; then the app development, DB, infrastructure and DevOps slices of each service; then the integration story, which is the only place the real cross-service behaviour is proven. RWB-E1-001 has no contract story; its five slices are four app development stories and one integration story.

| Slice | Work type | Legacy scenarios it carries | New scenarios |
|---|---|---|---|
| RWB-P1-E1001-APP | APP | AC1, AC4, AC5, AC6, AC8, AC9, AC10, AC11 | None |
| RWB-P4-E1001-APP | APP | None, the five authority tables are new work | AC1 to AC11 |
| RWB-P7-E1001-APP | APP | None, the six decision and rules tables are new work | AC1 to AC11 |
| RWB-P8-E1001-APP | APP | None, the proceeds table is new work | AC1 to AC11 |
| RWB-ITG-E1001-ITG | ITG | AC2, AC3, AC7 | AC12 to AC15 |

The count is the check. RWB-E1-001 has 11 legacy scenarios, the table accounts for all 11, one slice each, and the 37 new scenarios are added around them. When two slices of one legacy story claim the same ACn, the set is wrong and the story key is raised.

## The sentence patterns that repeat

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


## The codes you will see

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


## Where to read more

The project hub opens each story with its acceptance criteria already labelled Setup, Action and Result. The button marked ไทย turns on the Thai meaning of the words in each line.

โปรเจกต์ฮับจะแสดงเกณฑ์ยอมรับของแต่ละสตอรีพร้อมป้ายกำกับ Setup, Action และ Result และปุ่ม ไทย จะเปิดคำแปลของคำศัพท์ในแต่ละบรรทัด

The glossary file holds the words, the sentence patterns and the codes, with Thai for each. Its Thai follows the wording already used in the Workbench message standard, so a word means the same thing on the screen as it does in a story.

ไฟล์อภิธานศัพท์รวบรวมคำศัพท์ รูปแบบประโยค และรหัสต่าง ๆ พร้อมคำแปลภาษาไทย โดยใช้คำตามมาตรฐานข้อความของระบบ เพื่อให้คำเดียวกันมีความหมายตรงกันทั้งบนหน้าจอและในสตอรี

If a line is still unclear, the squad lead should raise it against the story key. The wording is changed once, in the story, so every reader gets the same correction.

หากยังมีบรรทัดที่ไม่ชัดเจน หัวหน้าทีมสามารถแจ้งโดยอ้างอิงรหัสสตอรี เพื่อแก้ไขถ้อยคำที่ต้นทางเพียงครั้งเดียว ผู้อ่านทุกคนจะได้รับฉบับที่แก้ไขแล้วเหมือนกัน

Every slice is listed with its work type, its wave and its release in the Service Story Catalog v1, and the Legacy map sheet of that file names the new stories for every legacy key, so a reader who starts from a legacy key can find every slice of it. The Story Build Order v3 gives the order the slices are built in, the Day-1 Work Allocation v1 names the work that can start on the first day, and the Dependency Map v4 shows which story waits for which.

The four new sections, How the set is sliced, The origin tag at the end of every scenario, The AC number inside the tag and Reading the slices of one legacy story, are written in English. The Thai reading of them is not specified in the source documents (CG-C-HTR-3; ASM-C-HTR-3).
